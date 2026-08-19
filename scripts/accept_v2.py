#!/usr/bin/env python3
"""Multi-viewport acceptance + overflow probe + screenshots for v2 upgrade."""
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
            # neutralize smooth scrolling so programmatic jumps are instant
            await page.evaluate("document.documentElement.style.scrollBehavior='auto'")
            # trigger all reveals by scrolling full height
            height = await page.evaluate("document.body.scrollHeight")
            for y in range(0, height, 400):
                await page.evaluate(f"window.scrollTo(0,{y})")
                await page.wait_for_timeout(60)
            await page.evaluate("window.scrollTo(0,document.body.scrollHeight)")
            await page.wait_for_timeout(900)
            await page.evaluate("window.scrollTo(0,0)")
            await page.wait_for_timeout(400)

            probe = await page.evaluate("""() => ({
              scrollW: document.documentElement.scrollWidth,
              clientW: document.documentElement.clientWidth,
              thumbs: document.querySelectorAll('.site-shot img').length,
              badges: document.querySelectorAll('.site-badge').length,
              dates: document.querySelectorAll('.site-date').length,
              tlItems: document.querySelectorAll('.tl-item').length,
              tlRail: !!document.querySelector('.tl-rail'),
              tlScroll: document.querySelector('.tl-rail') ? document.querySelector('.tl-rail').scrollWidth > document.querySelector('.tl-rail').clientWidth : false,
              logLines: document.querySelectorAll('.log-line').length,
              fxScript: !!document.querySelector('script[data-ui="fx"]'),
              glow: !!document.querySelector('.glow-dot'),
              cardsVisible: [...document.querySelectorAll('.site')].filter(c => !c.classList.contains('hide')).length,
              imgsBroken: [...document.querySelectorAll('.site-shot img')].filter(i => !i.complete || i.naturalWidth === 0).length,
            })""")
            overflow = probe["scrollW"] > probe["clientW"]
            shot = f"/tmp/v2_{w}x{h}.jpg"
            await page.screenshot(path=shot, full_page=False, type="jpeg", quality=72)
            # also mid-page shot of ledger area
            await page.evaluate("document.querySelector('#work').scrollIntoView()")
            await page.wait_for_timeout(500)
            await page.screenshot(path=f"/tmp/v2_{w}x{h}_work.jpg", full_page=False, type="jpeg", quality=72)
            results[f"{w}x{h}"] = {"errors": errors, "overflow": overflow, **probe, "shot": shot}
            await ctx.close()
        await browser.close()
    print(json.dumps(results, indent=1, ensure_ascii=False))
    bad = [k for k, v in results.items() if v["errors"] or v["overflow"] or v["imgsBroken"]]
    sys.exit(1 if bad else 0)

asyncio.run(main())
