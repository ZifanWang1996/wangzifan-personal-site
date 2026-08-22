#!/usr/bin/env python3
"""v5 multi-viewport acceptance: newest-first grid, spotlight, badges, motion."""
import asyncio, json, sys
from playwright.async_api import async_playwright

URL = "file:///root/projects/zf-wang-personal-site/index.html"
VIEWPORTS = [(1440, 900), (390, 844), (320, 568)]
EXPECTED_COLS = {"1440x900": 3, "390x844": 1, "320x568": 1}

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
            await page.wait_for_timeout(600)  # let scroll-in reveals + scramble settle

            d = await page.evaluate("""() => {
              const cards = [...document.querySelectorAll('.site')];
              const first = cards[0];
              const firstRect = first.getBoundingClientRect();
              const second = cards[1];
              const secondRect = second.getBoundingClientRect();
              const gridCols = getComputedStyle(document.querySelector('.sites')).gridTemplateColumns.split(' ').length;
              const names = cards.map(c => c.querySelector('h3')?.textContent.replace(/\\u200b/g, '').trim());
              const tlNames = [...document.querySelectorAll('.tl-names')].flatMap(g =>
                [...g.querySelectorAll('span')].map(s => s.textContent.trim()));
              const img = first.querySelector('img');
              const allImgs = [...document.querySelectorAll('.site img')];
              const h = document.documentElement;
              return {
                cards: cards.length,
                firstTitle: names[0],
                lastTitle: names[names.length - 1],
                names, tlNames,
                firstIsSpotlight: firstRect.width > secondRect.width * 1.5,
                firstHasLatestBadge: !!first.querySelector('.site-latest'),
                newBadges: document.querySelectorAll('.site-new').length,
                gridCols,
                imgLoaded: img ? img.complete && img.naturalWidth > 0 : false,
                allImgsLoaded: allImgs.every(i => i.complete && i.naturalWidth > 0),
                revealedCount: cards.filter(c => c.classList.contains('in')).length,
                hScrollOverflow: h.scrollWidth > h.clientWidth + 2,
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
            key = f"{w}x{h}"
            results[key] = d
            await page.screenshot(path=f"/tmp/v5_accept_{w}x{h}.png", full_page=True)
            await ctx.close()
        await browser.close()

    ok = True
    for vp, d in results.items():
        checks = {
            "31 cards": d["cards"] == 31,
            "first is Sinking City 2": d["firstTitle"] == "The Sinking City 2 Field Guide",
            "last is AIStoryNest": d["lastTitle"] == "AIStoryNest",
            "timeline == card order": d["tlNames"] == d["names"],
            "spotlight wider than card (multi-col only)": d["gridCols"] == 1 or d["firstIsSpotlight"],
            "latest badge on spotlight": d["firstHasLatestBadge"],
            "new badges > 0": d["newBadges"] > 0,
            f"grid cols == {EXPECTED_COLS[vp]}": d["gridCols"] == EXPECTED_COLS[vp],
            "spotlight img loaded": d["imgLoaded"],
            "all imgs loaded": d["allImgsLoaded"],
            "scroll reveals fired": d["revealedCount"] > 0,
            "no h overflow": not d["hScrollOverflow"],
            "game filter status": d["statusAfterGame"] == "游戏与内容",
            "no JS errors": len(d["errors"]) == 0,
        }
        fails = [k for k, v in checks.items() if not v]
        if fails:
            ok = False
        print(f"[{vp}] {'PASS' if not fails else 'FAIL: ' + str(fails)}  errors={d['errors'][:2]}")
    print(json.dumps({vp: {k: v for k, v in d.items() if k in ("cards", "firstTitle", "lastTitle", "gridCols", "newBadges", "statusAfterGame", "allImgsLoaded", "revealedCount")} for vp, d in results.items()}, ensure_ascii=False))
    sys.exit(0 if ok else 1)

asyncio.run(main())
