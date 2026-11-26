"""Search bar charts and palette cards for the Asian-inspired jacket piece,
in the DFB white chart style (Playfair Display bold lowercase title, Century
Gothic / Questrial labels, white background, dark grey bars with one pink
highlight). bar_chart() is adapted from
.claude/skills/trendalytics-forecast-decode/scripts/build_charts.py, extended
to draw bars below the baseline for negative values.
Every number is a % change between two periods of the same search term, so
terms are never compared with each other on size.
Hex codes come from data/looks.json (sample_all.py, which calls the
runway-colour-combos sampling script).
Usage: python3 build_charts.py && NODE_PATH=$(npm root -g) node \
  ../../.claude/skills/trendalytics-forecast-decode/scripts/render_cards.js $(pwd)/html $(pwd)"""
import csv, datetime, html, json, os, re
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "html"); os.makedirs(OUT, exist_ok=True)
PINK, DARK, INK, MUTED = '#D6447A', '#3A3A3A', '#222222', '#6B6B6B'
SERIF = "'Playfair Display', Georgia, serif"
SANS = "'Century Gothic', 'Questrial', 'Avenir', sans-serif"
FONTS = '<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Questrial&display=swap" rel="stylesheet">'
SRC = 'Source: Google Trends, worldwide'

def load(n):
    r = list(csv.reader(open(os.path.join(HERE, "data", n + ".csv"))))
    return [(a, int(b)) for a, b in r[1:]]

def wrap(label, n=14):
    lines, cur = [], ''
    for t in label.split(' '):
        if cur and len(cur + ' ' + t) > n: lines.append(cur); cur = t
        else: cur = (cur + ' ' + t).strip()
    lines.append(cur); return lines

def bar_chart(name, title, subtitle, items, highlight=0):
    """items: [(label, value)], value may be negative. subtitle: one plain line saying what the % measures."""
    n = len(items); fmt = lambda v: f'{round(v):+d}%'
    W = max(1000, 100 + n * 150, 110 + len(title) * 31, 110 + len(subtitle) * 13)
    top, plot_h, left, right = 175, 360, 50, 50
    slot = min((W - left - right) / n, 190); x0 = (W - slot * n) / 2; bw = min(150, slot * 0.84)
    vmax = max(0, max(v for _, v in items)); vmin = min(0, min(v for _, v in items))
    pos_room = 60 if vmax > 0 else 0; neg_room = 55 if vmin < 0 else 0
    scale = (plot_h - pos_room - neg_room) / (vmax - vmin)
    base = top + pos_room + vmax * scale; bottom = top + plot_h
    wn = max(8, int(slot / 12.5)); vs = min(42, round(slot * 0.34))
    label_lines = max(len(wrap(l, wn)) for l, _ in items)
    h = bottom + 46 + label_lines * 31 + 80
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}" height="{h}">', f'<rect width="{W}" height="{h}" fill="#FFFFFF"/>',
         f'<text x="{left}" y="78" font-family="{SERIF}" font-weight="700" font-size="56" fill="{INK}">{html.escape(title)}</text>',
         f'<text x="{left}" y="124" font-family="{SANS}" font-size="25" fill="{MUTED}">{html.escape(subtitle)}</text>']
    for i, (lab, v) in enumerate(items):
        cx = x0 + slot * (i + 0.5); bh = abs(v) * scale; col = PINK if i == highlight else DARK
        y = base - bh if v >= 0 else base
        p.append(f'<rect x="{cx-bw/2:.1f}" y="{y:.1f}" width="{bw:.1f}" height="{max(bh, 2):.1f}" fill="{col}"/>')
        vy = base - bh - 14 if v >= 0 else base + bh + vs * 0.95
        p.append(f'<text x="{cx:.1f}" y="{vy:.1f}" text-anchor="middle" font-family="{SANS}" font-size="{vs}" fill="{INK}">{fmt(v)}</text>')
        for j, line in enumerate(wrap(lab, wn)):
            p.append(f'<text x="{cx:.1f}" y="{bottom+44+j*31}" text-anchor="middle" font-family="{SANS}" font-size="25" fill="{INK}">{html.escape(line)}</text>')
    p.append(f'<line x1="{x0-10:.1f}" y1="{base:.1f}" x2="{x0+slot*n+10:.1f}" y2="{base:.1f}" stroke="#BDBDBD" stroke-width="1.5"/>')
    p.append(f'<text x="{left-10}" y="{h-30}" font-family="{SANS}" font-size="20" fill="{INK}">{html.escape(SRC)}</text></svg>')
    return name, "\n".join(p)

# Year on year search growth, this year vs last year. These five figures are Carmen's own
# readings from Google Trends (given 19 Nov 2026). The exports in data/ only cover the last
# 12 months, so they cannot reproduce a full year on year figure: replace this list from a
# two-year export once she sends it, and state the exact periods in the article's methodology.
YOY = [("mandarin jacket", 180), ("fur trim jacket", 160), ("opera jacket", 130), ("faux fur jacket", 30), ("conner ives", 30)]
SRC = 'Source: Google Trends'
charts = [
 bar_chart("01-search-year-on-year", "mandarin jacket searches are up 180%",
           "% change in Google searches, this year vs last year", YOY, highlight=0),
]
def page(body, w):
    return (f'<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>body{{margin:0;background:#fff}}'
            f'#card{{width:{w}px;background:#fff;box-sizing:border-box;padding:40px 50px 30px;font-family:{SANS};color:{INK}}}'
            f'h1{{font-family:{SERIF};font-weight:700;font-size:38px;margin:0 0 8px;line-height:1.1}}'
            f'.sub{{font-size:22px;color:{MUTED};margin:0 0 34px}} .src{{font-size:20px;margin-top:10px}}'
            '.row{display:grid;grid-template-columns:repeat(4,1fr);gap:28px 28px} .sq{height:200px;border-radius:2px}'
            f'.nm{{font-family:{SERIF};font-weight:700;font-size:28px;margin:16px 0 4px}} .hx{{font-size:19px;color:{MUTED};margin:0 0 8px}} .dp{{font-size:21px;line-height:1.3;margin-bottom:14px}}'
            f'</style></head><body><div id="card">{body}</div></body></html>')
looks = json.load(open(os.path.join(HERE, "data", "looks.json")))
def sw(n, hx, dp): return f'<div class="sw"><div class="sq" style="background:{hx}"></div><div class="nm">{html.escape(n.lower())}</div><div class="hx">{hx}</div><div class="dp">{html.escape(dp)}</div></div>'
ci_sw, ss_sw = [], []
for l in looks:
    for n, hx in l["colours"]:
        if l["house"] == "CONNER IVES": ci_sw.append(sw(n, hx, l["look"].lower()))
        else: ss_sw.append(sw(n, hx, l["house"].replace(" SS27", "").title()))
SUB = 'each square is a colour sampled from a photo of the piece, with its hex code (not a Pantone code)'
cards = [("04-palette-conner-ives", f'<h1>conner ives, the palette</h1><p class="sub">{SUB}</p><div class="row">{"".join(ci_sw)}</div><div class="src">Source: photos collected by The Data Fashion Brief</div>'),
         ("05-palette-ss27-runways", f'<h1>the ss27 runways, the palette</h1><p class="sub">{SUB}</p><div class="row">{"".join(ss_sw)}</div><div class="src">Source: runway images in FashionUnited\'s SS27 edit, credit Launchmetrics/spotlight</div>')]
names = []
for name, svg in charts:
    pg = f'<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>body{{margin:0;background:#fff}}</style></head><body><div id="card" style="display:inline-block">{svg}</div></body></html>'
    assert "—" not in pg and "–" not in pg; open(f"{OUT}/{name}.html", "w").write(pg); names.append(name)
for name, body in cards:
    pg = page(body, 1000); assert "—" not in pg and "–" not in pg; open(f"{OUT}/{name}.html", "w").write(pg); names.append(name)
json.dump(names, open(f"{OUT}/cards.json", "w")); print(names)
