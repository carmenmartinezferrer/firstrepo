"""Build the one-page DFB media kit PDF from data.json.

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


def platform(name, p):
    tiles = "".join(f'<div class="tile"><b>{escape(v)}</b><span>{escape(l)}</span></div>' for v, l in p["tiles"])
    period = ""
    if p.get("period"):
        pre, a, b = p["period"]
        period = f'<div class="period">{escape(pre)}<b>{escape(a)}</b>{DOT}<b>{escape(b)}</b></div>'
    cc = country_colors(p["countries"])
    t = p["top"]
    return f"""
<section>
  <h2>{name} <small>{escape(p["sub"])}</small> <span class="pill">100% ORGANIC GROWTH</span></h2>
  <div class="tiles">{tiles}</div>
  <div class="card chart">
    <div class="ctitle"><b>{escape(p["growth_title"][0])}</b>{escape(p["growth_title"][1])}</div>
    <div class="crow">{bars(p["growth"])}<div class="donut">{donut(p["countries"], cc)}{legend(p["countries"], cc)}</div></div>
    {period}
  </div>
  <div class="card top"><span class="pill">{escape(t["label"])}</span><b>{escape(t["stats"]).replace("·", "&nbsp;·&nbsp;")}</b>
    <span class="ttl">{escape(t["title"])}</span></div>
  {examples(p["examples"])}
</section>"""


def build_html(d):
    b = d["brand"]
    links = WIDE.join(f'<a href="{escape(u)}">{escape(l)}</a>' for l, u in d["links"])
    links += f'{WIDE}<a href="mailto:{b["email"]}">{b["email"]}</a>'
    a = d["audience"]
    gcol = [PINKS[2], "#090909"]
    acol = PINKS[: len(a["age"])]
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>Media Kit</title>
<link href="fonts/fonts.css" rel="stylesheet">
<style>
@page {{ size: letter; margin: 0 }}
* {{ box-sizing: border-box; margin: 0; padding: 0 }}
body {{ width: 612pt; height: 792pt; padding: 36pt; font-family: Jost, sans-serif; color: #24231f; font-size: 7.5pt;
       display: flex; flex-direction: column; background: #fff; -webkit-print-color-adjust: exact; print-color-adjust: exact }}
a {{ color: #d6447a; text-decoration: none }}
b {{ font-weight: 700 }}
header {{ display: flex; justify-content: space-between; align-items: flex-end; border-bottom: 1.5pt solid #090909; padding-bottom: 6pt }}
h1 {{ font-family: 'DM Serif Display', serif; font-weight: 400; font-size: 22.5pt; line-height: 1; color: #000 }}
h1 i {{ color: #d6447a }}
.meta {{ color: #52514e; font-size: 7.9pt; margin-top: 5pt }}
.right {{ text-align: right }}
.tag {{ font-family: 'DM Serif Display', serif; font-style: italic; font-size: 9.4pt; color: #52514e; margin-bottom: 6pt }}
.links {{ font-size: 7.1pt }}
.bio {{ font-size: 7.9pt; line-height: 1.45; margin: 8pt 0 8pt }}
h2 {{ font-family: 'DM Serif Display', serif; font-weight: 400; font-size: 12pt; color: #000; display: flex; align-items: center; gap: 6pt; margin-bottom: 6pt }}
h2 small {{ font-family: Jost; font-size: 7.1pt; color: #898781 }}
.pill {{ background: #d54479; color: #fff; font-family: Jost; font-weight: 700; font-size: 6.4pt; letter-spacing: .06em;
         padding: 2.5pt 7pt; border-radius: 3.5pt; line-height: 1 }}
.tiles {{ display: flex; gap: 6pt }}
.tile, .card {{ background: #fbfbfa; border: .75pt solid rgba(9,9,9,.09); border-radius: 4.5pt }}
.tile {{ flex: 1; height: 45pt; padding: 7pt 10pt; display: flex; flex-direction: column; justify-content: space-between }}
.tile b {{ font-size: 15pt; color: #0a0a0a; line-height: 1 }}
.tile span {{ font-size: 6.8pt; color: #52514e }}
.card {{ margin-top: 3.75pt }}
.chart {{ padding: 7pt 12pt 8pt }}
.ctitle {{ font-size: 7.9pt }} .ctitle b {{ color: #d54479 }}
.crow {{ display: flex; align-items: flex-end; gap: 14pt; margin-top: 4pt }}
.bars {{ flex: 1; display: flex; align-items: flex-end; gap: 6pt; height: 64pt }}
.bar {{ flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: flex-end }}
.bar b {{ font-size: 7.9pt; color: #0a0a0a; margin-bottom: 3pt }}
.bar span {{ width: 100%; border-radius: 2pt 2pt 0 0 }}
.bar em {{ font-style: normal; font-size: 6.8pt; color: #52514e; margin-top: -3pt; line-height: 1 }}
.donut {{ display: flex; align-items: center; gap: 8pt; width: 150pt; align-self: center }}
.legend div {{ font-size: 6.8pt; line-height: 1.55; display: flex; align-items: center; gap: 4pt }}
.legend i {{ width: 5pt; height: 5pt; border-radius: 1pt; display: inline-block }}
.period {{ color: #898781; font-size: 7.1pt; margin-top: 5pt }}
.period b {{ color: #52514e; font-weight: 600 }}
.top {{ display: flex; align-items: center; gap: 12pt; padding: 4.5pt 11pt; font-size: 7.9pt }}
.ttl {{ color: #24231f }}
.top b {{ font-size: 9pt; color: #0a0a0a }}
.examples {{ font-size: 6.8pt; color: #898781; margin: 4pt 0 7pt }}
.examples a {{ font-weight: 600; padding: 0 1.5pt }}
.aud {{ display: flex; gap: 40pt; margin-top: 2pt }}
.aud h3, footer h3 {{ font-size: 6.8pt; letter-spacing: .08em; color: #898781; font-weight: 700; margin-bottom: 5pt }}
.aud .donut {{ width: auto }}
.spacer {{ flex: 1; min-height: 12pt }}
footer {{ border-top: .75pt solid #090909; padding-top: 8pt }}
.cols {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 24pt; font-size: 6.8pt; line-height: 1.5 }}
.bottom {{ display: flex; justify-content: space-between; margin-top: 10pt; font-size: 7.1pt; color: #52514e }}
.bottom a {{ color: #000; font-weight: 700 }}
</style></head><body>
<header>
  <div><h1>{escape(b["name_before"])}<i>{escape(b["name_accent"])}</i>{escape(b["name_after"])}</h1>
    <div class="meta">{escape(b["handle"])}{WIDE}Media Kit{WIDE}{escape(d["month"])}</div></div>
  <div class="right"><div class="tag">{escape(b["tagline"])}</div><div class="links">{links}</div></div>
</header>
<p class="bio">{escape(d["bio"])}</p>
{platform("Instagram", d["instagram"])}
{platform("Substack", d["substack"])}
<section>
  <h2>Audience</h2>
  <div class="aud">
    <div><h3>GENDER</h3><div class="donut">{donut(a["gender"], gcol, 54)}{legend(a["gender"], gcol)}</div></div>
    <div><h3>AGE (WOMEN)</h3><div class="donut">{donut(a["age"], acol, 54)}{legend(a["age"], acol)}</div></div>
  </div>
</section>
<div class="spacer"></div>
<footer>
  <div class="cols">
    <div><h3>CONTENT PILLARS</h3>{escape(d["pillars"]).replace("  ·  ", "&nbsp;&nbsp;·&nbsp; ")}</div>
    <div><h3>PAST COLLABORATIONS</h3>{"&nbsp;&nbsp;·&nbsp; ".join(escape(c).replace(" ", "&nbsp;") for c in d["collaborations"])}</div>
    <div><h3>WAYS TO COLLABORATE</h3>{escape(d["ways"]).replace("  ·  ", "&nbsp;&nbsp;·&nbsp; ")}</div>
  </div>
  <div class="bottom"><span>For partnerships and collaborations</span><a href="mailto:{b["email"]}">{b["email"]}</a></div>
</footer>
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
        page.set_viewport_size({"width": 816, "height": 1056})
        page.screenshot(path=str(HERE / "media_kit_preview.png"), full_page=True)
        browser.close()
    print("wrote", HERE / "media_kit.pdf")


if __name__ == "__main__":
    main()
