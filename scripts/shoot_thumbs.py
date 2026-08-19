#!/usr/bin/env python3
"""Batch screenshot 28 product sites -> WebP thumbnails for zf-wang-personal-site."""
import asyncio, json, os, subprocess, sys
from playwright.async_api import async_playwright

SITES = [
    ("01-aistorynest", "https://aistorynest.mom/"),
    ("02-buildahooper", "https://buildahooper.best/"),
    ("03-falloutday", "https://falloutday.online/"),
    ("04-palworldmap", "https://palworldmap.best/"),
    ("05-codexskin", "https://codexskin.space/"),
    ("06-llmstxt", "https://llmstxt.best/"),
    ("07-allwishes", "https://allwishescometrue.site/"),
    ("08-taskbarhero", "https://taskbarherowiki.best/"),
    ("09-chinesecoins", "https://chinesecashcoins.wiki/"),
    ("10-rotcheck", "https://rotcheck.cyou/"),
    ("11-spiritvale", "https://spiritvale.blog/"),
    ("12-dragonsword", "https://dragonswordawakening.fun/"),
    ("13-copyplaintext", "https://copyplaintext.com/"),
    ("14-isitdown", "https://isitdown.click/"),
    ("15-sleepsuntil", "https://howmanysleepsuntil.rest/"),
    ("16-cashflow", "https://cashflow.lifestyle/"),
    ("17-zhuzhiliao", "https://zhuzhiliao.buzz/"),
    ("18-shiftatmidnight", "https://shiftatmidnight.blog/"),
    ("19-mergeanuke", "https://mergeanuke.space/"),
    ("20-aiscanner", "https://aiscanner.run/"),
    ("21-rspeditor", "https://rspeditor.app/"),
    ("22-matcha-rmf", "https://remove-matcha-filter.com/"),
    ("23-deepseekharness", "https://deepseekharness.site/"),
    ("24-polskipilkarz", "https://polskipilkarzsymulator.online/"),
    ("25-burncd", "https://burncd.xyz/"),
    ("26-matchafilter", "https://matchafilter.cc/"),
    ("27-craveloop", "https://foodnevercomes.online/"),
    ("28-niulai", "https://niulai.blog/"),
]

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
RAW = "/root/projects/zf-wang-personal-site/_thumbs_raw"
OUT = "/root/projects/zf-wang-personal-site/thumbs"

async def shoot(page, name, url, results):
    png = f"{RAW}/{name}.png"
    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=25000)
        await page.wait_for_timeout(2500)  # let fonts/lazy images settle
        # dismiss common cookie banners by scrolling a bit
        await page.evaluate("window.scrollTo(0,0)")
        await page.screenshot(path=png, full_page=False)
        results[name] = "ok"
    except Exception as e:
        results[name] = f"FAIL: {type(e).__name__}: {str(e)[:120]}"

async def main():
    os.makedirs(RAW, exist_ok=True)
    os.makedirs(OUT, exist_ok=True)
    results = {}
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            executable_path="/usr/bin/google-chrome",
            args=["--no-sandbox", "--disable-dev-shm-usage"],
        )
        ctx = await browser.new_context(
            user_agent=UA,
            viewport={"width": 1280, "height": 800},
            device_scale_factor=1,
            locale="en-US",
        )
        page = await ctx.new_page()
        # sequential to keep memory sane; 28 sites * ~4s ≈ 2min
        for name, url in SITES:
            await shoot(page, name, url, results)
            print(f"{name}: {results[name]}", flush=True)
        await browser.close()
    # convert to webp 640x400
    for name, _ in SITES:
        png = f"{RAW}/{name}.png"
        webp = f"{OUT}/{name}.webp"
        if os.path.exists(png):
            r = subprocess.run(
                ["convert", png, "-resize", "640x400^", "-gravity", "north",
                 "-extent", "640x400", "-quality", "82", webp],
                capture_output=True, text=True)
            if r.returncode != 0:
                # fallback: python pillow
                try:
                    from PIL import Image
                    im = Image.open(png)
                    im = im.resize((640, 400), Image.LANCZOS)
                    im.save(webp, "WEBP", quality=82)
                except Exception as e2:
                    results[name] += f" | webp-fail: {e2}"
    ok = sum(1 for v in results.values() if v == "ok")
    print(f"\nDONE: {ok}/{len(SITES)} ok")
    fails = {k: v for k, v in results.items() if v != "ok"}
    if fails:
        print("FAILURES:")
        print(json.dumps(fails, indent=2, ensure_ascii=False))

asyncio.run(main())
