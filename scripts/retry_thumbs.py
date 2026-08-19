#!/usr/bin/env python3
"""Retry failed screenshots with fresh context per site; then convert all PNGs to WebP via PIL."""
import asyncio, os, glob
from PIL import Image
from playwright.async_api import async_playwright

RETRY = [
    ("24-polskipilkarz", "https://polskipilkarzsymulator.online/"),
    ("25-burncd", "https://burncd.xyz/"),
    ("26-matchafilter", "https://matchafilter.cc/"),
    ("27-craveloop", "https://foodnevercomes.online/"),
    ("28-niulai", "https://niulai.blog/"),
]
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
RAW = "/root/projects/zf-wang-personal-site/_thumbs_raw"
OUT = "/root/projects/zf-wang-personal-site/thumbs"

async def shoot_one(browser, name, url):
    png = f"{RAW}/{name}.png"
    for attempt in range(3):
        ctx = await browser.new_context(user_agent=UA, viewport={"width": 1280, "height": 800}, locale="en-US")
        page = await ctx.new_page()
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=30000)
            await page.wait_for_timeout(2800)
            await page.evaluate("window.scrollTo(0,0)")
            await page.wait_for_timeout(300)
            await page.screenshot(path=png, full_page=False)
            await ctx.close()
            return "ok"
        except Exception as e:
            await ctx.close()
            if attempt == 2:
                return f"FAIL: {type(e).__name__}: {str(e)[:100]}"
            await asyncio.sleep(2)

async def main():
    os.makedirs(RAW, exist_ok=True)
    os.makedirs(OUT, exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path="/usr/bin/google-chrome",
                                          args=["--no-sandbox", "--disable-dev-shm-usage"])
        for name, url in RETRY:
            r = await shoot_one(browser, name, url)
            print(f"{name}: {r}", flush=True)
        await browser.close()
    # convert ALL raw pngs -> webp 640x400 (north-crop)
    n = 0
    for png in sorted(glob.glob(f"{RAW}/*.png")):
        webp = f"{OUT}/{os.path.splitext(os.path.basename(png))[0]}.webp"
        im = Image.open(png).convert("RGB")
        w, h = im.size
        scale = max(640 / w, 400 / h)
        im2 = im.resize((round(w * scale), round(h * scale)), Image.LANCZOS)
        # crop from top (north) to 640x400
        left = (im2.width - 640) // 2
        im3 = im2.crop((left, 0, left + 640, 400))
        im3.save(webp, "WEBP", quality=82, method=6)
        n += 1
    print(f"webp converted: {n}")
    missing = [os.path.basename(p) for p in sorted(glob.glob(f"{OUT}/*.webp"))]
    print(f"total webp: {len(missing)}")

asyncio.run(main())
