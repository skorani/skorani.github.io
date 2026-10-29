#!/usr/bin/env python3
"""
Optional: full-page screenshots of the website at phone, tablet and desktop widths.
Run while `bundle exec jekyll serve` is running:
    ~/.venvs/site/bin/python tools/screenshots.py              # 320, 768 and 1440 px, all pages
    ~/.venvs/site/bin/python tools/screenshots.py 375 home     # one width, one page
Needs: pip install playwright pillow. Images go to review/screenshots/ (not committed).
"""
import pathlib
import sys
from playwright.sync_api import sync_playwright
OUT = pathlib.Path(__file__).resolve().parents[1] / "review" / "screenshots"
OUT.mkdir(parents=True, exist_ok=True)
BASE = "http://127.0.0.1:4000"
pages = {"home": "/", "services": "/services/", "speaking": "/speaking/", "writing": "/writing/", "404": "/404.html"}
widths = [int(w) for w in sys.argv[1].split(",")] if len(sys.argv) > 1 else [320, 768, 1440]
only = sys.argv[2].split(",") if len(sys.argv) > 2 else list(pages)
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome")
    for w in widths:
        ctx = b.new_context(viewport={"width": w, "height": 900}, device_scale_factor=1)
        pg = ctx.new_page()
        for name in only:
            pg.goto(BASE + pages[name], wait_until="networkidle")
            pg.evaluate("document.fonts.ready")
            pg.add_style_tag(content="html{scroll-behavior:auto!important}")
            pg.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager')")
            pg.evaluate("window.scrollTo(0, 0)")
            pg.wait_for_timeout(300)
            pg.wait_for_function("Array.from(document.images).every(i => i.complete)")
            overflow = pg.evaluate("document.documentElement.scrollWidth - window.innerWidth")
            total = pg.evaluate("document.documentElement.scrollHeight")
            if total <= 16000:
                pg.screenshot(path=f"{OUT}/{name}-{w}.png", full_page=True)
            else:  # Chrome caps full-page captures at 16384px: stitch viewport shots
                from PIL import Image
                import io
                vh = 900
                canvas = Image.new("RGB", (w, total))
                y = 0
                while y < total:
                    pg.evaluate(f"window.scrollTo(0, {y})")
                    pg.wait_for_timeout(120)
                    actual = pg.evaluate("window.scrollY")
                    shot = Image.open(io.BytesIO(pg.screenshot()))
                    canvas.paste(shot, (0, actual))
                    y += vh
                canvas.save(f"{OUT}/{name}-{w}.png")
            print(name, w, "overflow:", overflow, "height:", pg.evaluate("document.documentElement.scrollHeight"))
        ctx.close()
    b.close()
