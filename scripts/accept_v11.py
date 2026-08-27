#!/usr/bin/env python3
"""Real-browser V11 acceptance matrix bound to the exact public artifact."""

import argparse
from functools import partial
import json
import os
import shutil
import tempfile
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright

from prepare_public_artifact import candidate_digest, public_files


ROOT = Path(__file__).resolve().parents[1]
VIEWPORTS = (
    ("desktop-1440", 1440, 900),
    ("desktop-1024", 1024, 768),
    ("tablet-768", 768, 1024),
    ("mobile-390", 390, 844),
    ("mobile-320", 320, 568),
    ("edge-759", 759, 800),
    ("edge-760", 760, 800),
    ("edge-761", 761, 800),
)
INTERACTION_NAMES = {"desktop-1440", "mobile-390", "mobile-320"}
SCREENSHOT_NAMES = {
    "desktop-1440",
    "desktop-1024",
    "tablet-768",
    "mobile-390",
    "mobile-320",
}


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        return


def settle(page) -> None:
    page.evaluate(
        """async () => {
          if (document.fonts && document.fonts.ready) await document.fonts.ready;
          await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
        }"""
    )


def stable_fragment(page, selector: str) -> dict:
    same = 0
    previous = None
    value = {}
    for _ in range(40):
        value = page.eval_on_selector(
            selector,
            """el => {
              const r = el.getBoundingClientRect();
              return {top: Math.round(r.top), bottom: Math.round(r.bottom),
                      y: Math.round(scrollY), height: Math.round(document.documentElement.scrollHeight)};
            }""",
        )
        current = (value["top"], value["bottom"], value["y"], value["height"])
        same = same + 1 if current == previous else 0
        if same >= 3:
            break
        previous = current
        page.wait_for_timeout(100)
    return value


def geometry(page) -> dict:
    return page.evaluate(
        """() => {
          const root = document.documentElement;
          const visible = el => {
            const s = getComputedStyle(el), r = el.getBoundingClientRect();
            return s.display !== 'none' && s.visibility !== 'hidden' && r.width > 0 && r.height > 0;
          };
          const selectors = 'a,button,input,select,img,h1,h2,h3,p,article,section';
          const out = [...document.querySelectorAll(selectors)].filter(visible).map(el => {
            const r = el.getBoundingClientRect(); return {el, r};
          }).filter(({r}) => r.left < -1 || r.right > root.clientWidth + 1).map(({el,r}) => ({
            tag: el.tagName, cls: el.className || '', text: (el.textContent || '').trim().slice(0,80),
            left: Math.round(r.left), right: Math.round(r.right), width: Math.round(r.width)
          })).slice(0,30);
          const rangeOwners = [...document.querySelectorAll(
            '.title-line,.ledger-filter,.nav-cta,.latest-card h3,.case-card h3,#wechat-value,.method-grid h3'
          )].filter(visible).flatMap(el => {
            const owner = el.getBoundingClientRect();
            const range = document.createRange(); range.selectNodeContents(el);
            return [...range.getClientRects()].filter(r => r.width > 0)
              .filter(r => r.left < owner.left - 1 || r.right > owner.right + 1).map(r => ({
                text:(el.textContent||'').trim().slice(0,80),
                owner:[Math.round(owner.left),Math.round(owner.right)],
                line:[Math.round(r.left),Math.round(r.right)]
              }));
          });
          const targets = [...document.querySelectorAll(
            '.button,.ledger-filter,#ledger-more,input,select,.nav-cta'
          )].filter(visible).map(el => {
            const r=el.getBoundingClientRect();
            return {text:(el.textContent||el.getAttribute('aria-label')||'').trim().slice(0,50),
                    w:Math.round(r.width),h:Math.round(r.height)};
          });
          const hero = document.querySelector('.hero');
          const primary = document.querySelector('.hero .button-primary');
          const heroMetric = hero && primary ? (() => {
            const hr=hero.getBoundingClientRect(), pr=primary.getBoundingClientRect();
            return {top:Math.round(hr.top),bottom:Math.round(hr.bottom),primaryTop:Math.round(pr.top),
                    primaryBottom:Math.round(pr.bottom),
                    primaryFullyInFirstViewport:pr.top>=0&&pr.bottom<=innerHeight};
          })() : null;
          return {
            viewport:[innerWidth,innerHeight,devicePixelRatio],
            clientWidth:root.clientWidth, scrollWidth:root.scrollWidth,
            overflow:root.scrollWidth > root.clientWidth,
            outOfBounds:out, ownerCrossings:rangeOwners,
            titleLines:[...document.querySelectorAll('.title-line')].map(el => {
              const range=document.createRange(); range.selectNodeContents(el);
              return {text:el.textContent,lines:[...range.getClientRects()].map(r=>({
                top:Math.round(r.top),left:Math.round(r.left),right:Math.round(r.right),height:Math.round(r.height)
              }))};
            }),
            hero:heroMetric,
            targetMin:targets.length ? {
              width:Math.min(...targets.map(x=>x.w)),height:Math.min(...targets.map(x=>x.h)),items:targets
            } : null
          };
        }"""
    )


def decode_images(page) -> list[dict]:
    images = page.locator("img")
    results = []
    for index in range(images.count()):
        image = images.nth(index)
        image.scroll_into_view_if_needed()
        page.wait_for_timeout(60)
        decode_error = None
        try:
            image.evaluate("img => img.decode()", timeout=10000)
        except Exception as exc:  # Browser error text belongs in the report.
            decode_error = str(exc).splitlines()[0]
        state = image.evaluate(
            """img => ({src:img.getAttribute('src'),loading:img.loading,complete:img.complete,
                         natural:[img.naturalWidth,img.naturalHeight]})"""
        )
        state["decodeError"] = decode_error
        results.append(state)
    return results


def interactions(page, context, origin: str, width: int, height: int) -> dict:
    result = {}
    page.goto(f"{origin}/?flow={width}", wait_until="domcontentloaded")
    settle(page)
    result["defaultVisible"] = page.locator("[data-ledger-id]:visible").count()
    page.locator('[data-ledger-filter="ai"]').click()
    result["ai"] = {
        "visible": page.locator("[data-ledger-id]:visible").count(),
        "count": page.locator("#ledger-count").inner_text(),
    }
    page.locator('[data-ledger-filter="all"]').click()
    page.locator("#ledger-search").fill("oxalpha")
    result["search"] = {
        "visible": page.locator("[data-ledger-id]:visible").count(),
        "ids": page.locator("[data-ledger-id]:visible").evaluate_all(
            "els=>els.map(el=>el.dataset.ledgerId)"
        ),
    }
    page.locator("#ledger-search").fill("")
    page.locator("#ledger-status").select_option("offline")
    result["offline"] = {
        "visible": page.locator("[data-ledger-id]:visible").count(),
        "ids": page.locator("[data-ledger-id]:visible").evaluate_all(
            "els=>els.map(el=>el.dataset.ledgerId)"
        ),
    }
    page.locator("#ledger-status").select_option("all")
    page.locator("#ledger-more").click()
    result["expanded"] = {
        "visible": page.locator("[data-ledger-id]:visible").count(),
        "aria": page.locator("#ledger-more").get_attribute("aria-expanded"),
    }

    context.grant_permissions(["clipboard-read", "clipboard-write"], origin=origin)
    page.locator("[data-copy-value]").scroll_into_view_if_needed()
    page.locator("[data-copy-value]").click()
    page.wait_for_function("document.querySelector('#copy-status').textContent.includes('已复制')")
    result["copySuccess"] = {
        "button": page.locator("[data-copy-value]").inner_text(),
        "status": page.locator("#copy-status").inner_text(),
    }

    page.reload(wait_until="domcontentloaded")
    settle(page)
    page.evaluate(
        """() => {
          Object.defineProperty(navigator, 'clipboard', {configurable:true,
            value:{writeText:async()=>{throw new Error('denied')}}});
          document.execCommand = () => false;
        }"""
    )
    page.locator("[data-copy-value]").scroll_into_view_if_needed()
    page.locator("[data-copy-value]").click()
    page.wait_for_function("document.querySelector('.manual-copy').hidden === false")
    result["copyFailure"] = page.evaluate(
        """() => ({
          button:document.querySelector('[data-copy-value]').textContent,
          status:document.querySelector('#copy-status').textContent,
          manualHidden:document.querySelector('.manual-copy').hidden,
          selected:document.querySelector('.manual-copy input').selectionStart === 0 &&
                   document.querySelector('.manual-copy input').selectionEnd ===
                   document.querySelector('.manual-copy input').value.length,
          focused:document.activeElement === document.querySelector('.manual-copy input')
        })"""
    )

    page.goto(f"{origin}/?skip={width}", wait_until="domcontentloaded")
    settle(page)
    page.keyboard.press("Tab")
    result["skipBefore"] = page.evaluate("document.activeElement.className")
    page.keyboard.press("Enter")
    page.wait_for_timeout(150)
    result["skipAfter"] = page.evaluate("({id:document.activeElement.id,hash:location.hash})")

    page.goto(f"{origin}/?fragment={width}", wait_until="domcontentloaded")
    settle(page)
    trigger = '.site-header a[href="#selected"]' if width > 760 else '.hero a[href="#selected"]'
    page.locator(trigger).click()
    target = stable_fragment(page, "#selected")
    result["fragment"] = {
        **target,
        "hash": page.evaluate("location.hash"),
        "intersects": target["bottom"] > 0 and target["top"] < height,
    }
    return result


def assert_view(name, width, height, geom, images, task) -> list[str]:
    failures = []
    if geom["viewport"][0] != width or geom["viewport"][1] != height:
        failures.append(f"viewport mismatch {geom['viewport']} requested {(width, height)}")
    if geom["overflow"] or geom["scrollWidth"] > geom["clientWidth"]:
        failures.append(f"document overflow {geom['scrollWidth']}>{geom['clientWidth']}")
    if geom["outOfBounds"]:
        failures.append(f"out of bounds {geom['outOfBounds'][:3]}")
    if geom["ownerCrossings"]:
        failures.append(f"text crosses owner {geom['ownerCrossings'][:3]}")
    if geom["targetMin"] and geom["targetMin"]["height"] < 44:
        failures.append(f"target height below 44px: {geom['targetMin']}")
    if width == 320 and (not geom["hero"] or not geom["hero"]["primaryFullyInFirstViewport"]):
        failures.append(f"320px primary CTA is not fully visible: {geom['hero']}")
    bad_images = [
        image for image in images
        if image["decodeError"] or not image["complete"] or image["natural"][0] <= 0
    ]
    if bad_images:
        failures.append(f"bad images {bad_images}")
    if task:
        expected = {
            "defaultVisible": task["defaultVisible"] == 9,
            "ai": task["ai"] == {"visible": 3, "count": "3 / 33"},
            "search": task["search"] == {"visible": 1, "ids": ["32"]},
            "offline": task["offline"] == {"visible": 1, "ids": ["24"]},
            "expanded": task["expanded"] == {"visible": 33, "aria": "true"},
            "copySuccess": task["copySuccess"]["button"] == "已复制 ✓"
            and "已复制" in task["copySuccess"]["status"],
            "copyFailure": task["copyFailure"]["button"] == "复制微信号"
            and not task["copyFailure"]["manualHidden"]
            and task["copyFailure"]["selected"]
            and task["copyFailure"]["focused"],
            "skip": task["skipBefore"] == "skip-link"
            and task["skipAfter"] == {"id": "main-content", "hash": "#main-content"},
            "fragment": task["fragment"]["hash"] == "#selected"
            and task["fragment"]["intersects"],
        }
        failures.extend(
            f"task failed: {key} => {task}" for key, passed in expected.items() if not passed
        )
    return failures


def launch_browser(playwright):
    executable = os.environ.get("CHROME_BIN") or shutil.which("google-chrome")
    kwargs = {"headless": True, "args": ["--no-sandbox"]}
    if executable:
        kwargs["executable_path"] = executable
    return playwright.chromium.launch(**kwargs)


def run_matrix(origin: str, output: Path, site_root: Path) -> dict:
    files = public_files(site_root)
    report = {
        "candidateSha256": candidate_digest(site_root),
        "publicFileCount": len(files),
        "origin": origin,
        "viewports": [],
        "motion": [],
        "noJavaScript": {},
    }
    with sync_playwright() as playwright:
        browser = launch_browser(playwright)
        for name, width, height in VIEWPORTS:
            mobile = width <= 390
            context = browser.new_context(
                viewport={"width": width, "height": height},
                device_scale_factor=2 if mobile else 1,
                is_mobile=mobile,
                has_touch=mobile,
            )
            page = context.new_page()
            console_errors = []
            page_errors = []
            request_failures = []
            bad_responses = []
            page.on(
                "console",
                lambda message, bucket=console_errors: bucket.append(
                    {"type": message.type, "text": message.text}
                ) if message.type == "error" else None,
            )
            page.on("pageerror", lambda exc, bucket=page_errors: bucket.append(str(exc)))
            page.on(
                "requestfailed",
                lambda request, bucket=request_failures: bucket.append(
                    {"url": request.url, "error": request.failure}
                ),
            )
            page.on(
                "response",
                lambda response, bucket=bad_responses: bucket.append(
                    {"url": response.url, "status": response.status}
                ) if response.url.startswith(origin) and response.status >= 400 else None,
            )
            response = page.goto(f"{origin}/?matrix={name}", wait_until="domcontentloaded")
            settle(page)
            title = page.title()
            marker = page.locator(".brand strong").inner_text()
            geom = geometry(page)
            images = decode_images(page)
            page.evaluate("scrollTo(0,0)")
            settle(page)
            task = interactions(page, context, origin, width, height) if name in INTERACTION_NAMES else None
            if name in SCREENSHOT_NAMES:
                page.goto(f"{origin}/?shot={name}", wait_until="domcontentloaded")
                settle(page)
                decode_images(page)
                page.evaluate("scrollTo(0,0)")
                settle(page)
                # Chromium's full-page stitch can project an offscreen fixed skip link into a tile.
                # Keyboard behavior is tested above; hide only the unfocused link in visual evidence.
                page.add_style_tag(content=".skip-link:not(:focus){display:none!important}")
                page.screenshot(path=str(output / f"{name}.png"), full_page=True)

            failures = []
            if not response or response.status != 200:
                failures.append(f"homepage status {response.status if response else None}")
            if title != "王子凡（ZF Wang）— 一人产品工作室" or marker != "ZF WANG":
                failures.append(f"identity mismatch {title} / {marker}")
            failures.extend(assert_view(name, width, height, geom, images, task))

            privacy = page.goto(
                f"{origin}/privacy.html?matrix={name}", wait_until="domcontentloaded"
            )
            settle(page)
            privacy_geom = geometry(page)
            page.evaluate("scrollTo(0, 0)")
            page.keyboard.press("Tab")
            privacy_skip_before = page.locator(":focus").get_attribute("class")
            page.keyboard.press("Enter")
            settle(page)
            privacy_skip_after = page.evaluate(
                "() => ({id: document.activeElement && document.activeElement.id, hash: location.hash})"
            )
            privacy_skip = {
                "before": privacy_skip_before,
                "after": privacy_skip_after,
            }
            if not privacy or privacy.status != 200 or page.title() != "隐私说明 — ZF Wang":
                failures.append("privacy identity/status")
            if (
                privacy_geom["overflow"]
                or privacy_geom["outOfBounds"]
                or privacy_geom["ownerCrossings"]
            ):
                failures.append(f"privacy geometry {privacy_geom}")
            if privacy_skip != {
                "before": "skip-link",
                "after": {"id": "privacy-content", "hash": "#privacy-content"},
            }:
                failures.append(f"privacy skip focus {privacy_skip}")
            same_origin_failures = [
                failure for failure in request_failures
                if urlparse(failure["url"]).netloc == urlparse(origin).netloc
            ]
            if console_errors:
                failures.append(f"console errors {console_errors}")
            if page_errors:
                failures.append(f"page errors {page_errors}")
            if same_origin_failures:
                failures.append(f"same-origin request failures {same_origin_failures}")
            if bad_responses:
                failures.append(f"same-origin HTTP errors {bad_responses}")
            report["viewports"].append(
                {
                    "name": name,
                    "requested": [width, height],
                    "geometry": geom,
                    "imageStates": images,
                    "tasks": task,
                    "privacyGeometry": privacy_geom,
                    "privacySkip": privacy_skip,
                    "consoleErrors": console_errors,
                    "pageErrors": page_errors,
                    "requestFailures": request_failures,
                    "badResponses": bad_responses,
                    "failures": failures,
                }
            )
            context.close()

        for reduced in (False, True):
            context = browser.new_context(
                viewport={"width": 390, "height": 844},
                reduced_motion="reduce" if reduced else "no-preference",
            )
            context.add_init_script(
                """(() => {
                  const real=window.requestAnimationFrame.bind(window); window.__qaRaf=0;
                  window.requestAnimationFrame=(cb)=>real((ts)=>{window.__qaRaf++;cb(ts)});
                })();"""
            )
            page = context.new_page()
            page.goto(f"{origin}/?motion={reduced}", wait_until="domcontentloaded")
            settle(page)
            baseline = page.evaluate("window.__qaRaf")
            page.wait_for_timeout(1200)
            after = page.evaluate("window.__qaRaf")
            report["motion"].append(
                {
                    "reduced": reduced,
                    "baseline": baseline,
                    "after": after,
                    "sustainedDelta": after - baseline,
                }
            )
            context.close()

        context = browser.new_context(
            viewport={"width": 390, "height": 844}, java_script_enabled=False
        )
        page = context.new_page()
        response = page.goto(f"{origin}/?no-js=1", wait_until="domcontentloaded")
        report["noJavaScript"] = {
            "status": response.status if response else None,
            "hero": page.locator("#hero-title").count(),
            "featured": page.locator("[data-featured-card]").count(),
            "ledger": page.locator("[data-ledger-id]").count(),
            "visibleLedger": page.locator("[data-ledger-id]:visible").count(),
            "visibleLedgerTools": page.locator(".ledger-tools:visible").count(),
            "visibleLedgerMore": page.locator("#ledger-more:visible").count(),
            "visibleCopyButton": page.locator("[data-copy-value]:visible").count(),
        }
        context.close()
        browser.close()

    report["failures"] = [
        f"{item['name']}: {failure}"
        for item in report["viewports"]
        for failure in item["failures"]
    ]
    report["failures"].extend(
        f"motion reduced={item['reduced']} sustained rAF {item['sustainedDelta']}"
        for item in report["motion"]
        if item["sustainedDelta"] != 0
    )
    expected_no_js = {
        "status": 200,
        "hero": 1,
        "featured": 6,
        "ledger": 33,
        "visibleLedger": 33,
        "visibleLedgerTools": 0,
        "visibleLedgerMore": 0,
        "visibleCopyButton": 0,
    }
    if report["noJavaScript"] != expected_no_js:
        report["failures"].append(
            f"no-JavaScript core content mismatch {report['noJavaScript']}"
        )
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site-dir", type=Path, default=ROOT)
    parser.add_argument("--evidence-dir", type=Path)
    args = parser.parse_args()
    site_root = args.site_dir.resolve()
    output = (
        args.evidence_dir.resolve()
        if args.evidence_dir
        else Path(tempfile.mkdtemp(prefix="wangzifan-v11-qa-"))
    )
    output.mkdir(parents=True, exist_ok=True)

    handler = partial(QuietHandler, directory=str(site_root))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    origin = f"http://127.0.0.1:{server.server_port}"
    try:
        report = run_matrix(origin, output, site_root)
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)

    report_path = output / "report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    summary = {
        "candidateSha256": report["candidateSha256"],
        "publicFileCount": report["publicFileCount"],
        "viewports": [
            {
                "name": item["name"],
                "viewport": item["geometry"]["viewport"],
                "scroll": [item["geometry"]["clientWidth"], item["geometry"]["scrollWidth"]],
                "out": len(item["geometry"]["outOfBounds"]),
                "ownerCrossings": len(item["geometry"]["ownerCrossings"]),
                "images": len(item["imageStates"]),
                "failures": item["failures"],
            }
            for item in report["viewports"]
        ],
        "motion": report["motion"],
        "noJavaScript": report["noJavaScript"],
        "failureCount": len(report["failures"]),
        "report": str(report_path),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    raise SystemExit(1 if report["failures"] else 0)


if __name__ == "__main__":
    main()
