"""Build the two-page DFB media kit PDF from data.json (page 1: the pitch, page 2: the numbers).

    python media-kit/build.py            # writes media-kit/media_kit.html and media_kit.pdf

Edit data.json (numbers, partnerships, links) and re-run; the layout never changes.
"""
import json
import math
import os
from html import escape
from pathlib import Path

HERE = Path(__file__).parent
PINKS = ["#f0b8cc", "#e485a7", "#d54479", "#a02e59", "#6e1f3c"]
GREY = "#c8c8c3"
DOT = "&nbsp;·&nbsp;"
WIDE = "&nbsp;&nbsp;·&nbsp;&nbsp;"


def donut(slices, colors, size=58, hole=0.5):
    """Inline-SVG donut. slices: [(label, pct)], colors aligned with slices."""
    r, c = size / 2, size / 2
    rin = r * hole
    total = sum(p for _, p in slices) or 1
    out, a0 = [], -math.pi / 2
    for (_, p), col in zip(slices, colors):
        a1 = a0 + 2 * math.pi * p / total
        large = 1 if a1 - a0 > math.pi else 0
        pts = [(c + r * math.cos(a0), c + r * math.sin(a0)), (c + r * math.cos(a1), c + r * math.sin(a1)),
               (c + rin * math.cos(a1), c + rin * math.sin(a1)), (c + rin * math.cos(a0), c + rin * math.sin(a0))]
        d = (f"M{pts[0][0]:.2f},{pts[0][1]:.2f} A{r},{r} 0 {large} 1 {pts[1][0]:.2f},{pts[1][1]:.2f} "
             f"L{pts[2][0]:.2f},{pts[2][1]:.2f} A{rin},{rin} 0 {large} 0 {pts[3][0]:.2f},{pts[3][1]:.2f} Z")
        out.append(f'<path d="{d}" fill="{col}"/>')
        a0 = a1
    return f'<svg width="{size}pt" height="{size}pt" viewBox="0 0 {size} {size}">{"".join(out)}</svg>'


def legend(slices, colors):
    rows = "".join(f'<div><i style="background:{col}"></i>{escape(lab)} <b>{p}%</b></div>'
                   for (lab, p), col in zip(slices, colors))
    return f'<div class="legend">{rows}</div>'


def country_colors(countries):
    return [GREY if lab == "Other" else PINKS[min(i, 4)] for i, (lab, _) in enumerate(countries)]


def bars(growth, max_h=44):
    top = max(v for _, v, _ in growth)
    n = len(growth)
    cells = []
    for i, (month, v, label) in enumerate(growth):
        from_end = n - 1 - i
        col = PINKS[3] if from_end == 0 else PINKS[2] if from_end <= 2 else PINKS[1] if from_end <= 5 else PINKS[0]
        h = max(1.5, max_h * v / top)
        cells.append(f'<div class="bar"><b>{escape(label)}</b><span style="height:{h:.1f}pt;background:{col}"></span>'
                     f'<em>{escape(month)}</em></div>')
    return f'<div class="bars">{"".join(cells)}</div>'


def examples(items):
    parts = []
    for label, urls in items:
        nums = " ".join(f'<a href="{escape(u)}">{k}</a>' for k, u in enumerate(urls, 1))
        parts.append(f"{escape(label)} {nums}")
    return f'<div class="examples">Examples: {WIDE.join(parts)}</div>'


def num(label, v):
    """Approximate values (">15K") are marked so growth % derived from them reads as approximate."""
    return v, label.startswith(">")


def mom_labels(growth, last=4):
    """Month-on-month % for the last `last` bars, e.g. '+41%'; '≈' when either side is approximate."""
    out = [""] * len(growth)
    for i in range(max(1, len(growth) - last), len(growth)):
        (_, a, la), (_, b, lb) = growth[i - 1], growth[i]
        if a:
            approx = "≈" if (la.startswith(">") or lb.startswith(">")) else ""
            out[i] = f"{approx}{(b - a) / a * 100:+.0f}%"
    return out


def bars_mom(growth, max_h=86):
    top = max(v for _, v, _ in growth)
    n, moms = len(growth), mom_labels(growth)
    cells = []
    for i, (month, v, label) in enumerate(growth):
        from_end = n - 1 - i
        col = PINKS[3] if from_end == 0 else PINKS[2] if from_end <= 2 else PINKS[1] if from_end <= 5 else PINKS[0]
        h = max(1.5, max_h * v / top)
        mom = f'<i>{escape(moms[i])}</i>' if moms[i] else "<i></i>"
        cells.append(f'<div class="bar">{mom}<b>{escape(label)}</b><span style="height:{h:.1f}pt;background:{col}"></span>'
                     f'<em>{escape(month)}</em></div>')
    return f'<div class="bars">{"".join(cells)}</div>'


def platform(name, p, sub_label):
    tiles = "".join(f'<div class="tile"><b>{escape(v)}</b><span>{escape(l)}</span></div>' for v, l in p["tiles"])
    window = f'<small class="win">Engagement, save &amp; send rates: {escape(p["window"])}</small>' if p.get("window") else ""
    period = ""
    if p.get("period"):
        pre, a, b = p["period"]
        period = f'<div class="period">{escape(pre)}<b>{escape(a)}</b>{DOT}<b>{escape(b)}</b></div>'
    cc = country_colors(p["countries"])
    t = p["top"]
    return f"""
<section class="plat" style="margin-top:10pt">
  <h2>{name} <small>{escape(p["sub"])}</small> <span class="pill">100% ORGANIC GROWTH</span>{window}</h2>
  <div class="tiles">{tiles}</div>
  <div class="card chart">
    <div class="ctitle"><b>{escape(p["growth_title"][0])}</b>{escape(p["growth_title"][1])}
      <span class="mom">{sub_label} · month-on-month growth</span></div>
    <div class="crow">{bars_mom(p["growth"])}<div class="donut">{donut(p["countries"], cc)}{legend(p["countries"], cc)}</div></div>
    {period}
  </div>
  <div class="card top"><span class="pill">{escape(t["label"])}</span><b>{escape(t["stats"]).replace("·", "&nbsp;·&nbsp;")}</b>
    <span class="ttl">{escape(t["title"])}</span></div>
  {examples(p["examples"])}
</section>"""


def first_num(tile_value):
    digits = "".join(ch for ch in tile_value if ch.isdigit() or ch == ".")
    n = float(digits or 0)
    return n * 1000 if "K" in tile_value else n


def build_html(d):
    b = d["brand"]
    links = WIDE.join(f'<a href="{escape(u)}">{escape(l)}</a>' for l, u in d["links"])
    links += f'{WIDE}<a href="mailto:{b["email"]}">{b["email"]}</a>'
    a = d["audience"]
    gcol = [PINKS[2], "#090909"]
    acol = PINKS[: len(a["age"])]
    ig, ss = d["instagram"], d["substack"]
    ig_f = ig["growth"][-1][1]
    ss_f = first_num(ss["tiles"][0][0])
    total = int((ig_f + ss_f) // 1000)
    glance = [(f"{total}K+", "total followers across Instagram &amp; Substack"),
              (ig["tiles"][0][0], "Instagram followers"), (ss["tiles"][0][0], "Substack followers"),
              (ss["tiles"][1][0], "Substack subscribers"), (ig["tiles"][1][0], f"Instagram engagement ({escape(ig.get('window', ''))})")]
    glance_html = "".join(f'<div class="tile"><b>{v}</b><span>{l}</span></div>' for v, l in glance)
    photo = (f'<img class="photo" src="{escape(d["photo"])}">' if d.get("photo")
             else '<div class="photo ph">photo</div>')
    markets = WIDE.join(f'{escape(c)} <b>{p}%</b>' for c, p in ig["countries"] if c != "Other")
    pillars = "".join(f'<span class="chip">{escape(x.strip())}</span>' for x in d["pillars"].split("·"))
    ways = "".join(f'<span class="chip">{escape(x.strip())}</span>' for x in d["ways"].split("·"))
    def logo(c):
        inner = (f'<img src="{escape(c["logo"])}" alt="{escape(c["name"])}">' if c.get("logo")
                 else f'<span>{escape(c["name"])}</span>')
        return (f'<a class="logo" href="{escape(c["url"])}">{inner}<sup>↗</sup></a>' if c.get("url")
                else f'<div class="logo">{inner}</div>')
    logos = "".join(logo(c) for c in d["collaborations"])
    press = "".join(f'<a class="press" href="{escape(x["url"])}"><b>{escape(x["outlet"])}</b><span>{escape(x["title"])}</span></a>'
                    for x in d["press"])
    head = f"""<header>
  <div><h1>{escape(b["name_before"])}<i>{escape(b["name_accent"])}</i>{escape(b["name_after"])}</h1>
    <div class="meta">{escape(b["handle"])}{WIDE}Media Kit{WIDE}{escape(d["month"])}{WIDE}{escape(d["location"])}</div></div>
  <div class="right"><div class="tag">{escape(b["tagline"])}</div><div class="links">{links}</div></div>
</header>"""
    foot = f"""<footer><div class="bottom"><span>For partnerships and collaborations{WIDE}<b>{escape(d["rates"])}</b></span>
  <a href="mailto:{b["email"]}">{b["email"]}</a></div></footer>"""
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>Media Kit</title>
<link href="fonts/fonts.css" rel="stylesheet">
<style>
@page {{ size: letter; margin: 0 }}
* {{ box-sizing: border-box; margin: 0; padding: 0 }}
body {{ font-family: Jost, sans-serif; color: #24231f; font-size: 7.5pt; background: #fff;
       -webkit-print-color-adjust: exact; print-color-adjust: exact }}
.page {{ width: 612pt; height: 792pt; padding: 36pt; display: flex; flex-direction: column; overflow: hidden; break-after: page }}
.page:last-child {{ break-after: auto }}
a {{ color: #d6447a; text-decoration: none }}
b {{ font-weight: 700 }}
header {{ display: flex; justify-content: space-between; align-items: flex-end; border-bottom: 1.5pt solid #090909; padding-bottom: 6pt }}
h1 {{ font-family: 'DM Serif Display', serif; font-weight: 400; font-size: 22.5pt; line-height: 1; color: #000 }}
h1 i {{ color: #d6447a }}
.meta {{ color: #52514e; font-size: 7.9pt; margin-top: 5pt }}
.right {{ text-align: right }}
.tag {{ font-family: 'DM Serif Display', serif; font-style: italic; font-size: 9.4pt; color: #52514e; margin-bottom: 6pt }}
.links {{ font-size: 7.1pt }}
h2 {{ font-family: 'DM Serif Display', serif; font-weight: 400; font-size: 12pt; color: #000; display: flex; align-items: center; gap: 6pt; margin: 12pt 0 6pt }}
h2 small {{ font-family: Jost; font-size: 7.1pt; color: #898781 }}
h2 .win {{ margin-left: auto; color: #898781 }}
h3 {{ font-size: 6.8pt; letter-spacing: .08em; color: #898781; font-weight: 700; margin-bottom: 5pt; text-transform: uppercase }}
.pill {{ background: #d54479; color: #fff; font-family: Jost; font-weight: 700; font-size: 6.4pt; letter-spacing: .06em;
         padding: 2.5pt 7pt; border-radius: 3.5pt; line-height: 1 }}
.hero {{ display: flex; gap: 16pt; margin-top: 14pt; align-items: stretch }}
.photo {{ width: 118pt; height: 148pt; border-radius: 4.5pt; object-fit: cover; flex: none }}
.photo.ph {{ background: #f6e3ea; color: #a02e59; display: flex; align-items: center; justify-content: center;
            font-family: 'DM Serif Display', serif; font-style: italic; font-size: 12pt }}
.angle {{ font-family: 'DM Serif Display', serif; font-size: 17pt; line-height: 1.2; color: #000; margin-bottom: 9pt }}
.angle i {{ color: #d6447a }}
.bio {{ font-size: 8.2pt; line-height: 1.5 }}
.based {{ margin-top: 8pt; font-size: 7.5pt; color: #52514e }}
.tiles {{ display: flex; gap: 6pt }}
.tile, .card {{ background: #fbfbfa; border: .75pt solid rgba(9,9,9,.09); border-radius: 4.5pt }}
.tile {{ flex: 1; height: 45pt; padding: 7pt 10pt; display: flex; flex-direction: column; justify-content: space-between }}
.tile b {{ font-size: 15pt; color: #0a0a0a; line-height: 1 }}
.tile span {{ font-size: 6.8pt; color: #52514e }}
.card {{ margin-top: 3.75pt }}
.aud {{ display: flex; gap: 30pt; align-items: flex-start }}
.aud .donut {{ width: auto }}
.markets {{ font-size: 7.9pt; line-height: 1.9 }}
.chips {{ display: flex; flex-wrap: wrap; gap: 4pt }}
.chip {{ border: .75pt solid rgba(9,9,9,.15); border-radius: 10pt; padding: 3pt 8pt; font-size: 7.3pt }}
.logos {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 6pt }}
.logo {{ position: relative; height: 34pt; background: #fbfbfa; border: .75pt solid rgba(9,9,9,.09); border-radius: 4.5pt;
         display: flex; align-items: center; justify-content: center; color: #0a0a0a }}
.logo span {{ font-family: 'DM Serif Display', serif; font-size: 12pt; letter-spacing: .02em }}
.logo img {{ max-height: 20pt; max-width: 80%; object-fit: contain }}
.logo sup {{ position: absolute; top: 3pt; right: 5pt; color: #d6447a; font-size: 7pt }}
.pressrow {{ display: flex; gap: 6pt }}
.press {{ flex: 1; background: #fbfbfa; border: .75pt solid rgba(9,9,9,.09); border-radius: 4.5pt; padding: 7pt 10pt; color: #24231f }}
.press b {{ display: block; font-family: 'DM Serif Display', serif; font-weight: 400; font-size: 11pt; color: #000 }}
.press span {{ font-size: 7.1pt; color: #d6447a }}
.two {{ display: grid; grid-template-columns: 1fr 1fr; gap: 22pt }}
.chart {{ padding: 9pt 12pt 10pt }}
.ctitle {{ font-size: 7.9pt; display: flex; gap: 6pt; align-items: baseline }} .ctitle b {{ color: #d54479 }}
.ctitle .mom {{ margin-left: auto; font-size: 6.8pt; color: #898781 }}
.crow {{ display: flex; align-items: flex-end; gap: 14pt; margin-top: 4pt }}
.bars {{ flex: 1; display: flex; align-items: flex-end; gap: 6pt; height: 118pt }}
.bar {{ flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: flex-end }}
.bar i {{ font-style: normal; font-size: 6.6pt; font-weight: 700; color: #d54479; min-height: 8pt }}
.bar b {{ font-size: 7.9pt; color: #0a0a0a; margin-bottom: 3pt }}
.bar span {{ width: 100%; border-radius: 2pt 2pt 0 0 }}
.bar em {{ font-style: normal; font-size: 6.8pt; color: #52514e; margin-top: -3pt; line-height: 1 }}
.donut {{ display: flex; align-items: center; gap: 8pt; width: 150pt; align-self: center }}
.plat .donut svg {{ width: 72pt; height: 72pt }}
.legend div {{ font-size: 6.8pt; line-height: 1.55; display: flex; align-items: center; gap: 4pt }}
.legend i {{ width: 5pt; height: 5pt; border-radius: 1pt; display: inline-block }}
.period {{ color: #898781; font-size: 7.1pt; margin-top: 5pt }}
.period b {{ color: #52514e; font-weight: 600 }}
.top {{ display: flex; align-items: center; gap: 12pt; padding: 4.5pt 11pt; font-size: 7.9pt }}
.ttl {{ color: #24231f }}
.top b {{ font-size: 9pt; color: #0a0a0a }}
.examples {{ font-size: 6.8pt; color: #898781; margin: 4pt 0 0 }}
.examples a {{ font-weight: 600; padding: 0 1.5pt }}
.spacer {{ flex: 1; min-height: 10pt }}
footer {{ border-top: .75pt solid #090909; padding-top: 8pt }}
.bottom {{ display: flex; justify-content: space-between; font-size: 7.5pt; color: #52514e }}
.bottom b {{ color: #d54479 }}
.bottom a {{ color: #000; font-weight: 700; font-size: 9pt }}
</style></head><body>
<div class="page">
{head}
<div class="hero">
  {photo}
  <div><p class="angle">{escape(d["angle"])}</p><p class="bio">{escape(d["bio"])}</p>
    <p class="based">Based in <b>{escape(d["location"])}</b>{WIDE}Writing for FashionUnited, featured by Lyst</p></div>
</div>
<h2>At a glance <span class="pill">100% ORGANIC GROWTH</span></h2>
<div class="tiles">{glance_html}</div>
<h2>Audience</h2>
<div class="aud">
  <div><h3>Gender</h3><div class="donut">{donut(a["gender"], gcol, 54)}{legend(a["gender"], gcol)}</div></div>
  <div><h3>Age (women)</h3><div class="donut">{donut(a["age"], acol, 54)}{legend(a["age"], acol)}</div></div>
  <div><h3>Top markets (Instagram)</h3><div class="markets">{markets}</div></div>
</div>
<h2>Past collaborations</h2>
<div class="logos">{logos}</div>
<h2>As featured in</h2>
<div class="pressrow">{press}</div>
<div class="two">
  <div><h2>Content pillars</h2><div class="chips">{pillars}</div></div>
  <div><h2>Work with me</h2><div class="chips">{ways}</div></div>
</div>
<div class="spacer"></div>
{foot}
</div>
<div class="page">
{head}
{platform("Instagram", ig, "followers")}
{platform("Substack", ss, "subscribers")}
<div class="spacer"></div>
{foot}
</div>
</body></html>"""


def main():
    from playwright.sync_api import sync_playwright

    data = json.loads((HERE / "data.json").read_text())
    html_path = HERE / "media_kit.html"
    html_path.write_text(build_html(data))
    exe = os.environ.get("CHROMIUM_PATH")
    with sync_playwright() as pw:
        browser = pw.chromium.launch(**({"executable_path": exe} if exe else {}))
        page = browser.new_page()
        page.goto(html_path.resolve().as_uri(), wait_until="networkidle")
        page.evaluate("document.fonts.ready")
        page.pdf(path=str(HERE / "media_kit.pdf"), format="Letter", print_background=True, prefer_css_page_size=True)
        try:  # shrink: subset fonts and recompress (keeps links)
            import pymupdf
            pdf = pymupdf.open(HERE / "media_kit.pdf")
            pdf.subset_fonts()
            pdf.save(HERE / "media_kit.min.pdf", garbage=4, deflate=True, deflate_fonts=True, clean=True, use_objstms=1)
            pdf.close()
            (HERE / "media_kit.min.pdf").replace(HERE / "media_kit.pdf")
        except ImportError:
            pass
        page.set_viewport_size({"width": 816, "height": 1056})
        page.screenshot(path=str(HERE / "media_kit_preview.png"), full_page=True)
        browser.close()
    print("wrote", HERE / "media_kit.pdf")


if __name__ == "__main__":
    main()
