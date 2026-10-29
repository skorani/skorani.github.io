#!/usr/bin/env python3
"""
Optional pre-release checks for the website (not needed to publish).

Checks accessibility (axe-core), titles and metadata, headings, internal links
and anchors, email links, old-URL redirects, keyboard focus, colour contrast of
controls in default/hover/focus states, reduced motion, and the copy-email
button. Lists external links at the end for a manual or curl check.

Setup (once):  python3 -m venv ~/.venvs/site && ~/.venvs/site/bin/pip install playwright
Run:           bundle exec jekyll serve          (in one terminal)
               ~/.venvs/site/bin/python tools/verify_site.py   (in another)
Uses your installed Google Chrome. Exit code 1 if any check fails.
"""
import pathlib
import json, sys, urllib.parse, urllib.request
from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:4000"
ROOT = pathlib.Path(__file__).resolve().parents[1]
AXE_FILE = ROOT / "review" / "axe-4.10.2.min.js"
if not AXE_FILE.exists():
    AXE_FILE.parent.mkdir(parents=True, exist_ok=True)
    AXE_FILE.write_bytes(urllib.request.urlopen("https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.10.2/axe.min.js").read())
AXE = AXE_FILE.read_text()
PAGES = ["/", "/services/", "/services/llm-evaluation-health-check/", "/services/graphrag-readiness-assessment/",
         "/services/knowledge-graph-prototype-sprint/", "/speaking/", "/writing/", "/404.html"]
REDIRECTS = {"/Activities.html": "/speaking/", "/Publications.html": "/writing/#research",
             "/Resource.html": "/#open-data", "/teaching.html": "/#about", "/blog.html": "/writing/", "/docs/": "/"}
EMAIL = "samira.korani@gmail.com"
results = {"fail": [], "info": []}

def fail(msg): results["fail"].append(msg); print("FAIL", msg)
def info(msg): results["info"].append(msg); print("ok  ", msg)

CONTRAST_JS = """
(el) => {
  const parse = c => { const m = c.match(/rgba?\\(([^)]+)\\)/); if (!m) return null;
    const p = m[1].split(/[ ,\\/]+/).filter(Boolean).map(Number); return {r:p[0], g:p[1], b:p[2], a: p.length > 3 ? p[3] : 1}; };
  const lum = c => { const f = v => { v /= 255; return v <= 0.04045 ? v/12.92 : Math.pow((v+0.055)/1.055, 2.4); };
    return 0.2126*f(c.r) + 0.7152*f(c.g) + 0.0722*f(c.b); };
  const blend = (top, bottom) => ({r: top.r*top.a + bottom.r*(1-top.a), g: top.g*top.a + bottom.g*(1-top.a), b: top.b*top.a + bottom.b*(1-top.a), a: 1});
  let layers = []; let n = el;
  while (n && n.nodeType === 1) { const bg = parse(getComputedStyle(n).backgroundColor); if (bg && bg.a > 0) layers.push(bg); if (bg && bg.a === 1) break; n = n.parentElement; }
  let bg = {r:255,g:255,b:255,a:1}; for (let i = layers.length - 1; i >= 0; i--) bg = blend(layers[i], bg);
  const cs = getComputedStyle(el); const fg = blend(parse(cs.color), bg);
  const ratio = (a, b) => { const [x, y] = [lum(a), lum(b)].sort((p, q) => q - p); return (x + 0.05) / (y + 0.05); };
  const out = {text: ratio(fg, bg)};
  const oc = parse(cs.outlineColor);
  if (cs.outlineStyle !== 'none' && oc) {
    // outline sits outside the element (offset), so compare against the parent's background
    let pl = []; let q = el.parentElement;
    while (q && q.nodeType === 1) { const b2 = parse(getComputedStyle(q).backgroundColor); if (b2 && b2.a > 0) pl.push(b2); if (b2 && b2.a === 1) break; q = q.parentElement; }
    let pbg = {r:255,g:255,b:255,a:1}; for (let i = pl.length - 1; i >= 0; i--) pbg = blend(pl[i], pbg);
    out.outline = ratio(blend(oc, pbg), pbg); out.outlineWidth = parseFloat(cs.outlineWidth);
  }
  const bc = parse(cs.borderTopColor);
  if (parseFloat(cs.borderTopWidth) > 0 && bc && bc.a > 0) out.border = ratio(blend(bc, bg), (() => { let pl=[]; let q=el.parentElement; while(q&&q.nodeType===1){const b2=parse(getComputedStyle(q).backgroundColor); if(b2&&b2.a>0) pl.push(b2); if(b2&&b2.a===1) break; q=q.parentElement;} let pbg={r:255,g:255,b:255,a:1}; for(let i=pl.length-1;i>=0;i--) pbg=blend(pl[i],pbg); return pbg; })());
  return out;
}
"""

with sync_playwright() as p:
    browser = p.chromium.launch(channel="chrome")

    # ---------- 1. axe-core at desktop and phone widths ----------
    for width in (1440, 320):
        ctx = browser.new_context(viewport={"width": width, "height": 900})
        pg = ctx.new_page()
        for path in PAGES:
            pg.goto(BASE + path, wait_until="networkidle")
            pg.evaluate("document.querySelectorAll('details').forEach(d => d.open = true)")
            pg.add_script_tag(content=AXE)
            res = pg.evaluate("""async () => { const r = await axe.run(document, {runOnly: {type: 'tag', values: ['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa','best-practice']}, resultTypes: ['violations','incomplete']});
              return {v: r.violations.map(v => ({id: v.id, impact: v.impact, n: v.nodes.length, targets: v.nodes.slice(0,3).map(x => x.target.join(' '))})),
                      inc: r.incomplete.map(v => ({id: v.id, n: v.nodes.length})), passes: r.passes.length}; }""")
            if res["v"]:
                for v in res["v"]: fail(f"axe {width}px {path}: {v['id']} ({v['impact']}) x{v['n']} {v['targets']}")
            else:
                info(f"axe {width}px {path}: 0 violations, {res['passes']} rule groups passed; needs review: {[(i['id'], i['n']) for i in res['inc']]}")
        ctx.close()

    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    pg = ctx.new_page()

    # ---------- 2. Structure, metadata, ids, images, links ----------
    internal, external, mailtos = set(), set(), []
    for path in PAGES:
        pg.goto(BASE + path, wait_until="networkidle")
        d = pg.evaluate("""() => ({
          title: document.title, lang: document.documentElement.lang,
          desc: document.querySelector('meta[name=description]')?.content,
          canonical: document.querySelector('link[rel=canonical]')?.href,
          og: document.querySelector('meta[property="og:image"]')?.content,
          tw: document.querySelector('meta[name="twitter:card"]')?.content,
          h1: document.querySelectorAll('h1').length,
          headings: Array.from(document.querySelectorAll('h1,h2,h3,h4,h5,h6')).map(h => +h.tagName[1]),
          dupIds: (() => { const c = {}; document.querySelectorAll('[id]').forEach(e => c[e.id] = (c[e.id]||0)+1); return Object.keys(c).filter(k => c[k] > 1); })(),
          imgs: Array.from(document.images).map(i => ({src: i.getAttribute('src'), alt: i.getAttribute('alt')})),
          links: Array.from(document.querySelectorAll('a')).map(a => ({href: a.getAttribute('href'), abs: a.href, name: (a.innerText || a.getAttribute('aria-label') || '').trim()})),
          buttons: Array.from(document.querySelectorAll('button')).map(b => ({type: b.getAttribute('type'), name: b.innerText.trim()})),
          jsonld: Array.from(document.querySelectorAll('script[type="application/ld+json"]')).map(s => s.textContent)
        })""")
        if not d["title"].startswith("Samira Korani |"): fail(f"{path}: title does not lead with name: {d['title']}")
        if not d["desc"] or len(d["desc"]) < 50: fail(f"{path}: weak description")
        if not d["canonical"] or not d["canonical"].startswith("https://skorani.github.io/"): fail(f"{path}: canonical {d['canonical']}")
        if not d["og"] or not d["og"].endswith("og-image.png"): fail(f"{path}: og:image {d['og']}")
        if d["tw"] != "summary_large_image": fail(f"{path}: twitter card")
        if d["h1"] != 1: fail(f"{path}: {d['h1']} h1 elements")
        skips = [(a, b) for a, b in zip(d["headings"], d["headings"][1:]) if b > a + 1]
        if skips: fail(f"{path}: heading level skips {skips}")
        if d["dupIds"]: fail(f"{path}: duplicate ids {d['dupIds']}")
        for im in d["imgs"]:
            if not im["alt"]: fail(f"{path}: image without alt {im['src']}")
        for b in d["buttons"]:
            if b["type"] != "button" or not b["name"]: fail(f"{path}: button issue {b}")
        for l in d["links"]:
            h = l["href"]
            if not h or h == "#" or h.startswith("javascript"): fail(f"{path}: empty/dead link {l}")
            elif h.startswith("mailto:"): mailtos.append((path, l["name"], h))
            elif l["abs"].startswith(BASE): internal.add(l["abs"])
            else: external.add(l["abs"])
            if not l["name"]: fail(f"{path}: link without text {h}")
        for j in d["jsonld"]:
            obj = json.loads(j)
            info(f"{path}: JSON-LD {obj['@type']} sameAs={obj.get('sameAs')}")
        info(f"{path}: title='{d['title']}', lang={d['lang']}, h1=1, headings ok, {len(d['links'])} links, {len(d['imgs'])} images")

    # internal links and fragments
    for url in sorted(internal):
        base, _, frag = url.partition("#")
        try:
            st = urllib.request.urlopen(base).status
        except Exception as e:
            fail(f"internal link {url}: {e}"); continue
        if frag:
            pg.goto(base, wait_until="domcontentloaded")
            if not pg.evaluate("f => !!document.getElementById(f)", frag): fail(f"missing anchor #{frag} on {base}")
    info(f"{len(internal)} internal link targets resolve (status 200, anchors present)")

    # mailto checks
    subjects = {}
    for path, name, h in mailtos:
        u = urllib.parse.urlparse(h)
        if u.path != EMAIL: fail(f"mailto to wrong address {h}")
        q = urllib.parse.parse_qs(u.query, keep_blank_values=True)
        plain = name.split("\n")[0] in (EMAIL, "Open in your email app")
        if not plain and "subject" not in q: fail(f"{path}: '{name.splitlines()[0]}' email link has no subject")
        subjects.setdefault(q.get("subject", ["(none)"])[0], set()).add(name.split("\n")[0])
    for s, names in subjects.items(): info(f"mailto subject '{s}' <- {sorted(names)}")

    # ---------- 3. Redirect stubs ----------
    for old, new in REDIRECTS.items():
        pg.goto(BASE + old); pg.wait_for_function("old => location.pathname !== old", arg=old, timeout=5000); pg.wait_for_load_state()
        landed = pg.url.replace(BASE, "")
        if landed != new: fail(f"redirect {old} -> {landed}, expected {new}")
        else: info(f"redirect {old} -> {landed}")

    # ---------- 4. Keyboard focus walk on the homepage ----------
    pg.goto(BASE + "/", wait_until="networkidle")
    pg.keyboard.press("Tab")
    first = pg.evaluate("() => ({cls: document.activeElement.className, vis: document.activeElement.getBoundingClientRect().top >= 0})")
    if first["cls"] != "skip-link" or not first["vis"]: fail(f"first Tab stop is not a visible skip link: {first}")
    else: info("first Tab stop: visible 'Skip to main content' link")
    pg.keyboard.press("Enter")
    if pg.evaluate("document.activeElement.id") != "main": fail("skip link does not move focus to main")
    else: info("skip link moves focus to <main>")
    pg.goto(BASE + "/", wait_until="networkidle")
    seen, problems, stops = set(), [], 0
    for i in range(200):
        pg.keyboard.press("Tab")
        pg.wait_for_timeout(700)  # let smooth scrolling settle before checking visibility
        el = pg.evaluate("""() => { const e = document.activeElement; const cs = getComputedStyle(e); const r = e.getBoundingClientRect();
          return {key: e.tagName + '|' + (e.getAttribute('href') || '') + '|' + e.innerText.slice(0, 40), tag: e.tagName,
                  outline: cs.outlineStyle, ow: parseFloat(cs.outlineWidth), inView: r.bottom > 0 && r.top < innerHeight && r.width > 0}; }""")
        if el["tag"] == "BODY" or el["key"] in seen: break
        seen.add(el["key"]); stops += 1
        if el["outline"] == "none" or el["ow"] < 2: problems.append(("no visible outline", el["key"]))
        if not el["inView"]: problems.append(("focused element not in view", el["key"]))
        c = pg.evaluate(CONTRAST_JS, pg.evaluate_handle("document.activeElement"))
        if c.get("outline", 0) < 3: problems.append((f"focus outline contrast {c.get('outline')}", el["key"]))
    for pr in problems: fail(f"keyboard: {pr}")
    info(f"keyboard: {stops} Tab stops on the homepage, each with a >=2px outline of >=3:1 contrast, scrolled into view" if not problems else f"keyboard: {stops} stops")

    # ---------- 5. Hover/focus/default contrast of interactive controls ----------
    checks = [("/", ".hero .button:not(.button--secondary)"), ("/", ".hero .button--secondary"), ("/", ".site-nav a"),
              ("/", ".evidence__item a"), ("/", ".contact .button--inverse"), ("/", ".contact .button--inverse-outline"),
              ("/", ".contact__email-actions a"), ("/", ".copy-button"), ("/", ".site-footer a"), ("/", ".faq summary"),
              ("/", ".offer .button"), ("/", ".card__links a"), ("/", ".arrow-link")]
    worst = {}
    for path, sel in checks:
        pg.goto(BASE + path, wait_until="networkidle")
        loc = pg.locator(sel).first
        for state in ("default", "hover", "focus"):
            pg.mouse.move(0, 0)
            if state == "hover": loc.hover()
            if state == "focus": loc.focus()
            pg.wait_for_timeout(200)
            c = loc.evaluate(CONTRAST_JS.replace("(el) =>", "(el) =>", 1))
            key = f"{sel} [{state}]"
            worst[key] = c
            if c["text"] < 4.5: fail(f"contrast {key}: text {c['text']:.2f}")
            if state == "focus" and c.get("outline", 0) < 3: fail(f"contrast {key}: focus outline {c.get('outline')}")
            if "border" in c and sel.endswith(("secondary", "inverse-outline", "copy-button")) and c["border"] < 3:
                fail(f"contrast {key}: control border {c['border']:.2f}")
    info("control contrast (text / focus outline / border): " + "; ".join(
        f"{k} {v['text']:.1f}" + (f"/{v['outline']:.1f}" if 'outline' in v else "") + (f"/b{v['border']:.1f}" if 'border' in v else "") for k, v in worst.items()))

    # ---------- 6. Reduced motion ----------
    rm = browser.new_context(viewport={"width": 1440, "height": 900}, reduced_motion="reduce")
    rp = rm.new_page(); rp.goto(BASE + "/", wait_until="networkidle")
    r = rp.evaluate("() => ({sb: getComputedStyle(document.documentElement).scrollBehavior, td: getComputedStyle(document.querySelector('.button')).transitionDuration, anims: document.getAnimations().length})")
    if r["sb"] != "auto" or any(float(x.strip()[:-1]) > 0 for x in r["td"].split(",")): fail(f"reduced motion not honoured {r}")
    else: info(f"reduced motion: scroll-behavior={r['sb']}, button transition={r['td']}, running animations={r['anims']}")
    rm.close()
    np_ = browser.new_context(viewport={"width": 1440, "height": 900}).new_page(); np_.goto(BASE + "/", wait_until="networkidle")
    info(f"default motion: scroll-behavior={np_.evaluate('getComputedStyle(document.documentElement).scrollBehavior')}, running animations={np_.evaluate('document.getAnimations().length')}")

    # ---------- 7. Copy-email button: success, failure, unsupported ----------
    ok = browser.new_context(viewport={"width": 1440, "height": 900}, permissions=["clipboard-read", "clipboard-write"])
    op = ok.new_page(); op.goto(BASE + "/", wait_until="networkidle")
    btn = op.locator(".copy-button")
    if not btn.is_visible(): fail("copy button hidden in a secure context with clipboard support")
    btn.click(); op.wait_for_timeout(300)
    status = op.locator("#copy-status").inner_text(); clip = op.evaluate("navigator.clipboard.readText()")
    if status != "Email address copied." or clip != EMAIL: fail(f"copy success path: status={status!r} clipboard={clip!r}")
    else: info(f"copy success path: status '{status}', clipboard contains {clip}")
    op.evaluate("() => { navigator.clipboard.writeText = () => Promise.reject(new Error('denied')); }")
    op.locator("#copy-status").evaluate("e => e.textContent = ''")
    btn.click(); op.wait_for_timeout(300)
    status = op.locator("#copy-status").inner_text()
    if "Couldn't copy" not in status: fail(f"copy failure path status={status!r}")
    else: info(f"copy failure path: status '{status}'")
    ok.close()
    un = browser.new_context(viewport={"width": 1440, "height": 900})
    un.add_init_script("Object.defineProperty(navigator, 'clipboard', {value: undefined})")
    up = un.new_page(); up.goto(BASE + "/", wait_until="networkidle")
    if up.locator(".copy-button").is_visible(): fail("copy button visible without clipboard support")
    else: info("no Clipboard API: copy button stays hidden; email text and mailto link remain")
    un.close()

    # ---------- 8. No-JavaScript rendering ----------
    nj = browser.new_context(viewport={"width": 1440, "height": 900}, java_script_enabled=False)
    njp = nj.new_page(); njp.goto(BASE + "/", wait_until="networkidle")
    info(f"JavaScript disabled: page renders, copy button visible={njp.locator('.copy-button').is_visible()}, mailto links={njp.locator('a[href^=mailto]').count()}")
    nj.close()

    # ---------- 9. Page weight ----------
    wp = browser.new_context(viewport={"width": 1440, "height": 900}).new_page()
    requested = []
    wp.on("request", lambda r: requested.append(r.url))
    wp.goto(BASE + "/", wait_until="networkidle")
    wp.locator("#about img").scroll_into_view_if_needed(); wp.wait_for_timeout(500)
    size = sum(len(urllib.request.urlopen(u).read()) for u in requested if u.startswith(BASE))
    third_party = [u for u in requested if not u.startswith(BASE)]
    info(f"homepage: {len(requested)} requests, {size/1024:.0f} KB uncompressed, third-party requests: {third_party or 'none'}")

    browser.close()

print("\nEXTERNAL LINKS:")
for e in sorted(external): print(e)
print(f"\nSUMMARY: {len(results['fail'])} failures, {len(results['info'])} checks passed")
sys.exit(1 if results["fail"] else 0)
