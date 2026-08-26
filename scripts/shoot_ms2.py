#!/usr/bin/env python3
"""Shoot mortalshell2.quest first screen -> assets/projects/project-33.webp (400x250)."""
import asyncio
from playwright.async_api import async_playwright
from PIL import Image

URL = "https://mortalshell2.quest/"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36"
RAW = "/root/projects/zf-wang-personal-site/_thumbs_raw/33-mortalshell2.png"
OUT = "/root/projects/zf-wang-personal-site/assets/projects/project-33.webp"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            executable_path="/usr/bin/google-chrome",
            args=["--no-sandbox", "--disable-dev-shm-usage"],
        )
        page = await browser.new_page(viewport={"width": 1440, "height": 900}, user_agent=UA)
        await page.goto(URL, wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(3000)
        await page.evaluate("window.scrollTo(0,0)")
        await page.screenshot(path=RAW, full_page=False)
        await browser.close()
    im = Image.open(RAW)
    # center-crop to 16:10 then Lanczos resize to 400x250 (no distortion)
    w, h = im.size
    target_ratio = 400 / 250
    if w / h > target_ratio:
        new_w = int(h * target_ratio)
        im = im.crop(((w - new_w) // 2, 0, (w + new_w) // 2, h))
    else:
        new_h = int(w / target_ratio)
        im = im.crop((0, 0, w, new_h))
    im = im.resize((400, 250), Image.LANCZOS)
    im.save(OUT, "WEBP", quality=85)
    print("saved", OUT, im.size)

asyncio.run(main())
