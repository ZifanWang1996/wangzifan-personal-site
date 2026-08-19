#!/usr/bin/env python3
"""Screenshot hellletloosevietnam.blog -> WebP thumbnail for card #29."""
import asyncio, os
from PIL import Image
from playwright.async_api import async_playwright

URL = "https://hellletloosevietnam.blog/"
NAME = "29-hllv"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
RAW = "/root/projects/zf-wang-personal-site/_thumbs_raw"
OUT = "/root/projects/zf-wang-personal-site/thumbs"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            executable_path="/usr/bin/google-chrome",
            args=["--no-sandbox", "--disable-dev-shm-usage"],
        )
        ctx = await browser.new_context(user_agent=UA, viewport={"width": 1280, "height": 800}, device_scale_factor=1, locale="en-US")
        page = await ctx.new_page()
        await page.goto(URL, wait_until="domcontentloaded", timeout=25000)
        await page.wait_for_timeout(2500)
        await page.evaluate("window.scrollTo(0,0)")
        await page.screenshot(path=f"{RAW}/{NAME}.png", full_page=False)
        await browser.close()
    # PIL-based center-crop to 640x400 (north gravity)
    im = Image.open(f"{RAW}/{NAME}.png")
    w, h = im.size
    scale = 640 / w
    new_h = int(h * scale)
    im = im.resize((640, new_h), Image.LANCZOS)
    im = im.crop((0, 0, 640, min(400, new_h)))
    im = im.convert("RGB")
    im.save(f"{OUT}/{NAME}.webp", "WEBP", quality=82)
    print(f"DONE: {NAME}.webp dims={im.size} bytes={os.path.getsize(OUT + '/' + NAME + '.webp')}")

asyncio.run(main())
