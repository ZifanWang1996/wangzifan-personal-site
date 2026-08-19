#!/usr/bin/env python3
"""v4 multi-viewport acceptance: count chips, ledger chip, HLLV card, overflow probe."""
import asyncio, json, sys
from playwright.async_api import async_playwright

URL = "file:///root/projects/zf-wang-personal-site/index.html"
VIEWPORTS = [(1440, 900), (390, 844), (320, 568)]

async def main():
    results = {}
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            executable_path="/usr/bin/google-chrome",
            args=["--no-sandbox", "--disable-dev-shm-usage"],
        )
        for w, h in VIEWPORTS:
            ctx = await browser.new_context(viewport={"width": w, "height": h}, device_scale_factor=1)
            page = await ctx.new_page()
            errors = []
            page.on("pageerror", lambda e: errors.append(str(e)))
            page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
            await page.goto(URL, wait_until="load")
            await page.evaluate("document.documentElement.style.scrollBehavior='auto'")
            height = await page.evaluate("document.body.scrollHeight")
            for y in range(0, height, 400):
                await page.evaluate(f"window.scrollTo(0,{y})")
                await page.wait_for_timeout(40)
            await page.wait_for_timeout(300)

            # wait for scramble/decode animation on timeline title to settle
            for _ in range(120):
                tl = await page.evaluate("document.querySelector('#timeline-title')?.textContent")
                if tl == "37 天，29 次真实上线。":
                    break
                await page.wait_for_timeout(100)
            d = await page.evaluate("""() => {
              const chips = [...document.querySelectorAll('.filter')].map(b => ({
                f: b.dataset.filter, c: b.dataset.count, text: b.textContent,
                rect: b.getBoundingClientRect(), overflow: b.scrollWidth > b.clientWidth + 2
              }));
              const cards = [...document.querySelectorAll('.site')];
              const hllv = cards.find(c => c.textContent.includes('HLLV Field Manual'));
              const img = hllv ? hllv.querySelector('img') : null;
              const h = document.documentElement;
              return {
                cards: cards.length,
                chips,
                ledgerChip: !!document.querySelector('.ledger-count'),
                hllvFound: !!hllv,
                imgLoaded: img ? img.complete && img.naturalWidth > 0 : false,
                hScrollOverflow: h.scrollWidth > h.clientWidth + 2,
                timeline: document.querySelector('#timeline-title')?.textContent,
                statusAfterGame: (() => {
                  const g = document.querySelector('[data-filter="game"]');
                  g.click();
                  const t = document.querySelector('#visibleCount').textContent;
                  document.querySelector('[data-filter="all"]').click();
                  return t;
                })()
              };
            }""")
            d["errors"] = errors
            results[f"{w}x{h}"] = d
            await page.screenshot(path=f"/tmp/v4_accept_{w}x{h}.png", full_page=True)
            await ctx.close()
        await browser.close()

    ok = True
    for vp, d in results.items():
        checks = {
            "29 cards": d["cards"] == 29,
            "5 chips": len(d["chips"]) == 5,
            "chip counts": [c["c"] for c in d["chips"]] == ["29", "3", "10", "9", "7"],
            "button text clean": [c["text"] for c in d["chips"]] == ["全部", "AI 产品", "游戏与内容", "实用工具", "创意实验"],
            "no chip overflow": not any(c["overflow"] for c in d["chips"]),
            "ledger chip": d["ledgerChip"],
            "hllv card": d["hllvFound"],
            "hllv img loaded": d["imgLoaded"],
            "no h overflow": not d["hScrollOverflow"],
            "timeline 29": d["timeline"] == "37 天，29 次真实上线。",
            "game filter status": d["statusAfterGame"] == "游戏与内容",
            "no JS errors": len(d["errors"]) == 0,
        }
        fails = [k for k, v in checks.items() if not v]
        if fails:
            ok = False
        print(f"[{vp}] {'PASS' if not fails else 'FAIL: ' + str(fails)}  errors={d['errors'][:2]}")
    print(json.dumps({vp: {k: v for k, v in d.items() if k in ("cards", "timeline", "statusAfterGame", "hllvFound", "imgLoaded")} for vp, d in results.items()}, ensure_ascii=False))
    sys.exit(0 if ok else 1)

asyncio.run(main())
