#!/usr/bin/env python3
"""v6 multi-viewport acceptance: launch console hero + v5 grid intact."""
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
            await page.wait_for_timeout(2400)  # canvas + full telemetry cascade (500+i*260)
            d = await page.evaluate("""(vh) => {
              const host = document.querySelector('[data-launch]');
              const cv = host.querySelector('.orbit-canvas');
              const cards = document.querySelectorAll('.site');
              const px = host.querySelectorAll('.px');
              const lines = host.querySelectorAll('.tele-line');
              const tm = document.getElementById('tminus');
              const h = document.documentElement;
              const heroRect = host.getBoundingClientRect();
              // sample whole canvas for painted pixels (orbits + stars)
              const ctx2 = cv.getContext('2d');
              const img = ctx2.getImageData(0, 0, cv.width, cv.height).data;
              let lit = 0; for (let i = 3; i < img.length; i += 4) if (img[i] > 8) lit++;
              return {
                heroH: Math.round(heroRect.height), vh,
                canvasSized: cv.width > 0 && cv.height > 0,
                canvasLit: lit > 0,
                pxCount: px.length,
                teleCount: lines.length,
                teleShown: [...lines].filter(l => l.classList.contains('on')).length,
                tminus: tm ? tm.textContent : null,
                cards: cards.length,
                firstCard: cards[0].querySelector('h3')?.textContent.trim(),
                bridge: !!document.querySelector('.launch-bridge'),
                hScrollOverflow: h.scrollWidth > h.clientWidth + 2,
              };
            }""", h)
            d["errors"] = errors
            key = f"{w}x{h}"
            results[key] = d
            await page.screenshot(path=f"/tmp/v6_accept_{w}x{h}.png")
            await ctx.close()
        await browser.close()

    ok = True
    for vp, d in results.items():
        checks = {
            "hero fills viewport (desktop only)": vp == "1440x900" and (d["heroH"] >= d["vh"] - 96) or vp != "1440x900",
            "canvas sized": d["canvasSized"],
            "canvas painted": d["canvasLit"],
            "32 matrix": d["pxCount"] == 32,
            "5 telemetry": d["teleCount"] == 5,
            "telemetry shown": d["teleShown"] == 5,
            "tminus ticking": bool(d["tminus"]) and d["tminus"] != "--:--:--",
            "32 cards intact": d["cards"] == 32,
            "first card OxAlpha": d["firstCard"] == "OxAlpha",
            "bridge present": d["bridge"],
            "no h overflow": not d["hScrollOverflow"],
            "no JS errors": len(d["errors"]) == 0,
        }
        fails = [k for k, v in checks.items() if not v]
        if fails: ok = False
        print(f"[{vp}] {'PASS' if not fails else 'FAIL: ' + str(fails)}  tminus={d['tminus']}  errors={d['errors'][:2]}")
    print(json.dumps({vp: {k: v for k, v in d.items() if k in ("heroH","vh","canvasLit","pxCount","teleShown","tminus","cards","firstCard")} for vp, d in results.items()}, ensure_ascii=False))
    sys.exit(0 if ok else 1)

asyncio.run(main())
