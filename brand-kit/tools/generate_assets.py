#!/usr/bin/env python3
"""
Regenerate the brand-kit logo, favicon and social-image files.

Optional. The generated files are committed, so you only need this if you
change the palette, the symbol geometry, the name or the descriptor text.

Setup (once, in any folder outside the repository):
    python3 -m venv ~/.venvs/brand
    ~/.venvs/brand/bin/pip install fonttools brotli pillow playwright

Run from the repository root (uses your installed Google Chrome):
    ~/.venvs/brand/bin/python brand-kit/tools/generate_assets.py
"""
import base64
import io
import pathlib

from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parents[2]
KIT = ROOT / "brand-kit"
LOGO = KIT / "logo"
SOCIAL = KIT / "social"
FONT = KIT / "fonts" / "ibm-plex-sans-latin-var.woff2"

NAME = "Samira Korani"
DESCRIPTOR = "Knowledge Graphs · GraphRAG · LLM Evaluation"

# Keep in sync with brand-kit/tokens.css
IVORY, WHITE, INK = "#F7F5EF", "#FFFFFF", "#14252B"
TEAL, SLATE, SAGE = "#075E54", "#52646A", "#D8DFDA"

SCHEMES = {
    "light": dict(name=INK, desc=SLATE, edge=TEAL, node=TEAL),
    "dark-bg": dict(name=IVORY, desc=SAGE, edge=SAGE, node=IVORY),
    "mono-ink": dict(name=INK, desc=INK, edge=INK, node=INK),
    "mono-white": dict(name=WHITE, desc=WHITE, edge=WHITE, node=WHITE),
}

NAME_SIZE = 40
NAME_TRACKING = -0.4   # -0.01em
DESC_TRACKING = 0.15
STACK_GAP = 9          # space between name baseline and descriptor cap height
PAD = 2                # safety margin inside each SVG, not the clear space


# ---------------------------------------------------------------- fonts ----

def static_woff2(weight):
    """Static instance of the variable font, subset to Latin-1, as woff2 bytes."""
    font = TTFont(FONT)
    font = instancer.instantiateVariableFont(font, {"wght": weight})
    options = subset.Options()
    options.flavor = "woff2"
    options.layout_features = ["kern", "liga", "calt"]
    sub = subset.Subsetter(options)
    sub.populate(unicodes=list(range(0x20, 0x7F)) + list(range(0xA0, 0x100)))
    sub.subset(font)
    buf = io.BytesIO()
    font.flavor = "woff2"
    font.save(buf)
    return buf.getvalue()


def font_css(weights):
    rules = []
    for w, data in weights.items():
        b64 = base64.b64encode(data).decode()
        rules.append(
            '@font-face{font-family:"IBM Plex Sans";font-weight:%d;'
            'src:url(data:font/woff2;base64,%s) format("woff2")}' % (w, b64)
        )
    return "".join(rules)


# --------------------------------------------------------------- symbol ----

def k_graph(edge, node, *, stroke, r, hub_r, x0, x1, y0, y1, hub=True):
    """The letter K drawn as a small graph: a hub node with three relationships."""
    ym = (y0 + y1) / 2
    lines = [(x0, y0, x0, y1), (x0, ym, x1, y0), (x0, ym, x1, y1)]
    nodes = [(x0, y0, r), (x0, y1, r), (x1, y0, r), (x1, y1, r)]
    if hub:
        nodes.append((x0, ym, hub_r))
    out = ['<g fill="none" stroke="%s" stroke-width="%s" stroke-linecap="round">' % (edge, stroke)]
    out += ['<line x1="%s" y1="%s" x2="%s" y2="%s"/>' % ln for ln in lines]
    out.append('</g><g fill="%s">' % node)
    out += ['<circle cx="%s" cy="%s" r="%s"/>' % n for n in nodes]
    out.append("</g>")
    return "".join(out)


def symbol_plain(edge, node):
    return k_graph(edge, node, stroke=2.6, r=3, hub_r=3.6, x0=9.75, x1=22.25, y0=6, y1=26)


def symbol_tile(small=False, square=False):
    rx = 0 if square else 7
    bg = '<rect width="32" height="32" rx="%s" fill="%s"/>' % (rx, TEAL)
    if small:  # tuned for 16px: no hub dot, heavier strokes
        g = k_graph(SAGE, IVORY, stroke=2.8, r=3.1, hub_r=0, x0=10.5, x1=21.5, y0=8.5, y1=23.5, hub=False)
    else:
        g = k_graph(SAGE, IVORY, stroke=2.2, r=2.4, hub_r=2.9, x0=11.25, x1=20.75, y0=9, y1=23)
    return bg + g


def svg_doc(w, h, body, title, extra_defs=""):
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
        'role="img" aria-label="{t}"><title>{t}</title>{d}{b}</svg>\n'
    ).format(w=fmt(w), h=fmt(h), t=title, d=extra_defs, b=body)


def fmt(v):
    return ("%.2f" % v).rstrip("0").rstrip(".")


# ------------------------------------------------------------- measure ----

MEASURE_JS = """
async ([name, desc, nameSize, nameTrack, descTrack]) => {
  await document.fonts.ready;
  const c = document.createElement('canvas').getContext('2d');
  const m = (txt, weight, size, track) => {
    c.font = `${weight} ${size}px "IBM Plex Sans"`;
    c.letterSpacing = `${track}px`;
    const r = c.measureText(txt);
    return {left: r.actualBoundingBoxLeft, right: r.actualBoundingBoxRight,
            ascent: r.actualBoundingBoxAscent, descent: r.actualBoundingBoxDescent};
  };
  return {name: m(name, 600, nameSize, nameTrack), desc1: m(desc, 400, 1, 0),
          descTrackProbe: m(desc, 400, 100, descTrack * 100 / 15)};
}
"""


def measure(page, desc_size):
    return page.evaluate(
        """async ([desc, size, track]) => {
            await document.fonts.ready;
            const c = document.createElement('canvas').getContext('2d');
            c.font = `400 ${size}px "IBM Plex Sans"`;
            c.letterSpacing = `${track}px`;
            const r = c.measureText(desc);
            return {left: r.actualBoundingBoxLeft, right: r.actualBoundingBoxRight,
                    ascent: r.actualBoundingBoxAscent, descent: r.actualBoundingBoxDescent};
        }""",
        [DESCRIPTOR, desc_size, DESC_TRACKING],
    )


# ---------------------------------------------------------------- main ----

def main():
    LOGO.mkdir(parents=True, exist_ok=True)
    SOCIAL.mkdir(parents=True, exist_ok=True)
    weights = {600: static_woff2(600), 400: static_woff2(400)}
    css_both = font_css(weights)
    css_name = font_css({600: weights[600]})
    var_b64 = base64.b64encode(FONT.read_bytes()).decode()

    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome")
        page = browser.new_page()
        page.set_content(
            '<style>@font-face{font-family:"IBM Plex Sans";font-weight:100 700;'
            'src:url(data:font/woff2;base64,%s) format("woff2")}</style>'
            '<p style="font-family:\'IBM Plex Sans\';font-weight:600">%s</p>'
            '<p style="font-family:\'IBM Plex Sans\';font-weight:400">%s</p>' % (var_b64, NAME, DESCRIPTOR)
        )
        metrics = page.evaluate(MEASURE_JS, [NAME, DESCRIPTOR, NAME_SIZE, NAME_TRACKING, DESC_TRACKING])
        nm = metrics["name"]
        name_w = nm["left"] + nm["right"]
        # Size the descriptor so it spans the same width as the name (a justified lockup).
        desc_size = round(name_w / (metrics["desc1"]["left"] + metrics["desc1"]["right"]) * 0.995, 2)
        desc_size = max(13.0, min(desc_size, 16.0))
        dm = measure(page, desc_size)
        desc_w = dm["left"] + dm["right"]

        name_base = PAD + nm["ascent"]
        desc_base = name_base + STACK_GAP + dm["ascent"]
        stack_h = desc_base + dm["descent"] + PAD
        stack_w = max(name_w, desc_w) + 2 * PAD
        name_only_h = name_base + PAD  # no descenders in the name

        def name_text(x, y, color):
            return ('<text x="%s" y="%s" fill="%s" font-family="\'IBM Plex Sans\', \'Helvetica Neue\', Arial, sans-serif" '
                    'font-weight="600" font-size="%s" letter-spacing="%s">%s</text>'
                    % (fmt(x), fmt(y), color, NAME_SIZE, NAME_TRACKING, NAME))

        def desc_text(x, y, color):
            return ('<text x="%s" y="%s" fill="%s" font-family="\'IBM Plex Sans\', \'Helvetica Neue\', Arial, sans-serif" '
                    'font-weight="400" font-size="%s" letter-spacing="%s">%s</text>'
                    % (fmt(x), fmt(y), color, fmt(desc_size), DESC_TRACKING, DESCRIPTOR.replace("·", "&#183;")))

        files = {}
        # Symbol
        for scheme, c in SCHEMES.items():
            files["symbol-%s.svg" % scheme] = svg_doc(32, 32, symbol_plain(c["edge"], c["node"]), "Samira Korani symbol")
        files["symbol-tile.svg"] = svg_doc(32, 32, symbol_tile(), "Samira Korani")
        files["favicon.svg"] = svg_doc(32, 32, symbol_tile(small=True), "Samira Korani")

        # Wordmarks and lockup
        sym_size = stack_h - 2 * PAD
        gap = sym_size * 0.34
        lock_w = PAD + sym_size + gap + max(name_w, desc_w) + PAD
        for scheme, c in SCHEMES.items():
            style = "<defs><style>%s</style></defs>"
            files["wordmark-name-%s.svg" % scheme] = svg_doc(
                name_w + 2 * PAD, name_only_h,
                name_text(PAD + nm["left"], name_base, c["name"]),
                NAME, style % css_name)
            files["wordmark-descriptor-%s.svg" % scheme] = svg_doc(
                stack_w, stack_h,
                name_text(PAD + nm["left"], name_base, c["name"]) + desc_text(PAD + dm["left"], desc_base, c["desc"]),
                "%s, %s" % (NAME, DESCRIPTOR), style % css_both)
            tx = PAD + sym_size + gap
            sym = '<svg x="%s" y="%s" width="%s" height="%s" viewBox="0 0 32 32">%s</svg>' % (
                fmt(PAD), fmt(PAD), fmt(sym_size), fmt(sym_size), symbol_plain(c["edge"], c["node"]))
            files["lockup-%s.svg" % scheme] = svg_doc(
                lock_w, stack_h,
                sym + name_text(tx + nm["left"], name_base, c["name"]) + desc_text(tx + dm["left"], desc_base, c["desc"]),
                "%s, %s" % (NAME, DESCRIPTOR), style % css_both)

        for fname, svg in files.items():
            (LOGO / fname).write_text(svg, encoding="utf-8")

        # Raster exports
        def render(svg_markup, w, h, out, bg=None, scale=1):
            pg = browser.new_page(viewport={"width": int(w), "height": int(h)}, device_scale_factor=scale)
            background = bg or "transparent"
            pg.set_content('<html><body style="margin:0;background:%s">'
                           '<div style="width:%dpx;height:%dpx">%s</div></body></html>'
                           % (background, w, h,
                              svg_markup.replace("<svg ", '<svg style="display:block;width:100%;height:100%" ', 1)))
            pg.wait_for_timeout(100)
            pg.screenshot(path=str(out), omit_background=bg is None)
            pg.close()

        render(files["favicon.svg"], 16, 16, LOGO / "favicon-16.png")
        render(files["symbol-tile.svg"], 32, 32, LOGO / "favicon-32.png")
        render(files["symbol-tile.svg"], 48, 48, LOGO / "favicon-48.png")
        render(svg_doc(32, 32, symbol_tile(square=True), "Samira Korani"), 180, 180, LOGO / "apple-touch-icon.png")
        render(files["symbol-tile.svg"], 512, 512, LOGO / "symbol-tile-512.png")
        # Square, full-bleed avatar for Medium, LinkedIn or GitHub (they crop to a circle)
        render(svg_doc(32, 32, symbol_tile(square=True), "Samira Korani"), 1024, 1024, LOGO / "avatar-1024.png")
        render(files["lockup-light.svg"], round(lock_w * 1.5), round(stack_h * 1.5), LOGO / "lockup-light@2x.png", scale=2)
        render(files["lockup-dark-bg.svg"], round(lock_w * 1.5), round(stack_h * 1.5), LOGO / "lockup-dark-bg@2x.png", scale=2)

        # favicon.ico with hand-tuned 16px and standard 32/48px images
        imgs = [Image.open(LOGO / n).convert("RGBA") for n in ("favicon-16.png", "favicon-32.png", "favicon-48.png")]
        imgs[2].save(LOGO / "favicon.ico", format="ICO", sizes=[(16, 16), (32, 32), (48, 48)], append_images=imgs[:2])

        # Social sharing image, rendered from its HTML source
        og = browser.new_page(viewport={"width": 1200, "height": 630}, device_scale_factor=1)
        og.goto((SOCIAL / "og-image.html").as_uri())
        og.evaluate("document.fonts.ready")
        og.wait_for_timeout(200)
        og.screenshot(path=str(SOCIAL / "og-image.png"))
        browser.close()

    print("descriptor size %.2f, name width %.1f, descriptor width %.1f" % (desc_size, name_w, desc_w))
    for f in sorted(LOGO.iterdir()):
        print("%7d  %s" % (f.stat().st_size, f.relative_to(ROOT)))


if __name__ == "__main__":
    main()
