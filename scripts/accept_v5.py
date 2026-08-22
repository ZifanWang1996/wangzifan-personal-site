#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["playwright==1.62.0"]
# ///
"""Multi-viewport acceptance for the current portfolio release.

Run reproducibly with: uv run scripts/accept_v5.py
The script serves the checkout containing itself over a loopback HTTP server.
"""

import asyncio
import json
import sys
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[1]
VIEWPORTS = [(1440, 900), (390, 844), (320, 568)]
EXPECTED_COLS = {"1440x900": 3, "390x844": 1, "320x568": 1}
EXPECTED_META = ["32 · 已上线", "AI 模型证据站", "2026-08-22"]
EXPECTED_CTA_ARIA = "访问 OxAlpha 项目（新窗口）"


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        _ = (format, args)
        return


async def main():
    handler = partial(QuietHandler, directory=str(ROOT))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    server_thread = Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    base_url = f"http://127.0.0.1:{server.server_port}/"
    url = f"{base_url}index.html"
    results = {}

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                executable_path="/usr/bin/google-chrome",
                args=["--no-sandbox", "--disable-dev-shm-usage"],
            )
            for w, h in VIEWPORTS:
                mobile = w < 500
                ctx = await browser.new_context(
                    viewport={"width": w, "height": h},
                    device_scale_factor=1,
                    is_mobile=mobile,
                    has_touch=mobile,
                )
                page = await ctx.new_page()
                errors = []
                network_errors = []
                page.on("pageerror", lambda e, out=errors: out.append(str(e)))
                page.on(
                    "console",
                    lambda m, out=errors: out.append(m.text) if m.type == "error" else None,
                )
                page.on(
                    "requestfailed",
                    lambda r, out=network_errors: out.append(
                        f"requestfailed {r.url}: {r.failure}"
                    )
                    if r.url.startswith(base_url)
                    else None,
                )
                page.on(
                    "response",
                    lambda r, out=network_errors: out.append(f"HTTP {r.status} {r.url}")
                    if r.url.startswith(base_url) and r.status >= 400
                    else None,
                )

                response = await page.goto(url, wait_until="load")
                assert response is not None and response.status == 200
                assert "text/html" in (await response.header_value("content-type") or "")
                await page.evaluate("document.documentElement.style.scrollBehavior='auto'")
                height = await page.evaluate("document.body.scrollHeight")
                for y in range(0, height, 400):
                    await page.evaluate(f"window.scrollTo(0,{y})")
                    await page.wait_for_timeout(40)
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await page.wait_for_timeout(300)
                await page.wait_for_timeout(700)

                d = await page.evaluate(
                    """() => {
                      const cards = [...document.querySelectorAll('.site')];
                      const first = cards[0];
                      const firstRect = first.getBoundingClientRect();
                      const secondRect = cards[1].getBoundingClientRect();
                      const gridCols = getComputedStyle(document.querySelector('.sites')).gridTemplateColumns.split(' ').length;
                      const names = cards.map(c => c.querySelector('h3')?.textContent.replace(/\\u200b/g, '').trim());
                      const tlNames = [...document.querySelectorAll('.tl-names')].flatMap(g =>
                        [...g.querySelectorAll('span')].map(s => s.textContent.trim()));
                      const allImgs = [...document.querySelectorAll('.site img')];
                      const cta = first.querySelector('.site-link');
                      const tool = document.querySelector('[data-filter="tool"]');
                      tool.click();
                      const visible = cards.filter(c => !c.classList.contains('hide'));
                      const toolProbe = {
                        status: document.querySelector('#visibleCount').textContent,
                        count: visible.length,
                        oxalphaVisible: visible.some(c => c.querySelector('h3')?.textContent.trim() === 'OxAlpha'),
                        pressed: tool.getAttribute('aria-pressed'),
                      };
                      document.querySelector('[data-filter="all"]').click();
                      return {
                        cards: cards.length,
                        firstTitle: names[0],
                        lastTitle: names[names.length - 1],
                        names, tlNames,
                        firstMeta: [...first.querySelectorAll('.site-meta span')].map(s => s.textContent.trim()),
                        firstDescription: first.querySelector('p')?.textContent.trim(),
                        firstIsSpotlight: firstRect.width > secondRect.width * 1.5,
                        firstHasLatestBadge: !!first.querySelector('.site-latest'),
                        newBadges: document.querySelectorAll('.site-new').length,
                        gridCols,
                        allImgsLoaded: allImgs.every(i => i.complete && i.naturalWidth > 0),
                        revealedCount: cards.filter(c => c.classList.contains('in')).length,
                        hScrollOverflow: document.documentElement.scrollWidth > document.documentElement.clientWidth + 2,
                        toolProbe,
                        firstCtaText: cta?.textContent.trim(),
                        firstCtaAria: cta?.getAttribute('aria-label'),
                        firstCtaHref: cta?.href,
                        firstCtaTarget: cta?.target,
                        firstCtaRel: cta?.rel,
                        firstCtaHeight: cta?.getBoundingClientRect().height || 0,
                        timelineAria: document.querySelector('#timeline-title')?.getAttribute('aria-label'),
                        timelineRegionAria: document.querySelector('.tl-rail')?.getAttribute('aria-label'),
                      };
                    }"""
                )

                rail = page.locator(".tl-rail")
                await rail.focus()
                before = await rail.evaluate("el => el.scrollLeft")
                await page.keyboard.press("ArrowRight")
                await page.wait_for_timeout(160)
                after = await rail.evaluate("el => el.scrollLeft")
                d["timelineKeyboardMoved"] = after > before

                first = page.locator(".site").first
                await page.evaluate("window.scrollTo(0, 0)")
                await page.screenshot(path=f"/tmp/v5_accept_{w}x{h}_top.png", full_page=False)
                await first.scroll_into_view_if_needed()
                await page.wait_for_timeout(120)
                await page.screenshot(
                    path=f"/tmp/v5_accept_{w}x{h}_project32.png", full_page=False
                )
                await first.screenshot(path=f"/tmp/v5_accept_{w}x{h}_project32_full-card.png")

                if (w, h) == (390, 844):
                    link = first.locator(".site-link")
                    async with page.expect_popup(timeout=20_000) as popup_info:
                        await link.tap()
                    popup = await popup_info.value
                    await popup.wait_for_load_state("domcontentloaded", timeout=30_000)
                    d["touchTargetUrl"] = popup.url
                    d["touchTargetTitle"] = await popup.title()
                    await popup.close()

                d["errors"] = errors
                d["networkErrors"] = network_errors
                results[f"{w}x{h}"] = d
                await ctx.close()
            await browser.close()
    finally:
        server.shutdown()
        server.server_close()
        server_thread.join(timeout=2)

    ok = True
    for vp, d in results.items():
        checks = {
            "32 cards": d["cards"] == 32,
            "first is OxAlpha": d["firstTitle"] == "OxAlpha",
            "last is AIStoryNest": d["lastTitle"] == "AIStoryNest",
            "timeline == card order": d["tlNames"] == d["names"],
            "OxAlpha metadata exact": d["firstMeta"] == EXPECTED_META,
            "OxAlpha description evidence": all(
                phrase in d["firstDescription"]
                for phrase in ("API", "约 1M 上下文", "可复现证据")
            ),
            "spotlight wider than card (multi-col only)": d["gridCols"] == 1
            or d["firstIsSpotlight"],
            "latest badge on spotlight": d["firstHasLatestBadge"],
            "new badges == 9": d["newBadges"] == 9,
            f"grid cols == {EXPECTED_COLS[vp]}": d["gridCols"] == EXPECTED_COLS[vp],
            "all imgs loaded": d["allImgsLoaded"],
            "all 32 scroll reveals fired": d["revealedCount"] == 32,
            "no horizontal overflow": not d["hScrollOverflow"],
            "tool filter status": d["toolProbe"]["status"] == "实用工具",
            "tool filter count == 10": d["toolProbe"]["count"] == 10,
            "OxAlpha visible under tool": d["toolProbe"]["oxalphaVisible"],
            "tool aria-pressed": d["toolProbe"]["pressed"] == "true",
            "CTA visible text": d["firstCtaText"] == "访问项目 ↗",
            "CTA accessible name": d["firstCtaAria"] == EXPECTED_CTA_ARIA,
            "CTA exact HTTPS URL": d["firstCtaHref"] == "https://oxalpha.site/",
            "CTA safe new window": d["firstCtaTarget"] == "_blank"
            and set(d["firstCtaRel"].split()) >= {"noopener", "noreferrer"},
            "mobile CTA >= 44px": d["firstCtaHeight"] >= 44
            if vp != "1440x900"
            else d["firstCtaHeight"] > 0,
            "stable timeline accessible name": d["timelineAria"]
            == "42 天，32 次真实上线。",
            "named timeline region": d["timelineRegionAria"] == "上线时间线，可横向滚动",
            "timeline keyboard scroll": d["timelineKeyboardMoved"],
            "no JS errors": not d["errors"],
            "no same-origin request/HTTP errors": not d["networkErrors"],
        }
        if vp == "390x844":
            checks["390px real touch reaches OxAlpha"] = d.get("touchTargetUrl", "").startswith(
                "https://oxalpha.site/"
            ) and d.get("touchTargetTitle", "").startswith("Ox Alpha AI")
        fails = [name for name, passed in checks.items() if not passed]
        if fails:
            ok = False
        print(f"[{vp}] {'PASS' if not fails else 'FAIL: ' + str(fails)}")

    keep = (
        "cards",
        "firstTitle",
        "lastTitle",
        "firstMeta",
        "gridCols",
        "newBadges",
        "toolProbe",
        "firstCtaAria",
        "firstCtaHeight",
        "revealedCount",
        "timelineKeyboardMoved",
        "touchTargetUrl",
        "touchTargetTitle",
        "errors",
        "networkErrors",
    )
    print(
        json.dumps(
            {vp: {key: value for key, value in data.items() if key in keep} for vp, data in results.items()},
            ensure_ascii=False,
        )
    )
    return 0 if ok else 1


raise SystemExit(asyncio.run(main()))
