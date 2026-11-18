"""Search line charts and palette cards for the Asian-inspired jacket piece,
in the DFB white chart style (Playfair Display bold lowercase title, Century
Gothic / Questrial labels, white background), same constants as
.claude/skills/trendalytics-forecast-decode/scripts/build_charts.py and
build_visuals.py. Hex codes come from data/looks.json (sample_all.py, which
calls the runway-colour-combos sampling script).
Each Google Trends export was pulled on its own, so every line is indexed to
its own busiest week: the charts compare timing, never size.
Usage: python3 build_charts.py && NODE_PATH=$(npm root -g) node render.js"""
import csv, datetime, html, json, os
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "html"); os.makedirs(OUT, exist_ok=True)
PINK, DARK, INK, MUTED = '#D6447A', '#3A3A3A', '#222222', '#6B6B6B'
SERIF = "'Playfair Display', Georgia, serif"
SANS = "'Century Gothic', 'Questrial', 'Avenir', sans-serif"
FONTS = '<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Questrial&display=swap" rel="stylesheet">'
SRC = 'Source: Google Trends, worldwide, weekly, November 2025 to November 2026'
UNIT = ['weekly Google searches, worldwide. 100 = each term\'s own busiest week,', 'so the chart compares when each one peaked, not how big it is']

def load(n):
    r = list(csv.reader(open(os.path.join(HERE, "data", n + ".csv"))))
    return [(a, int(b)) for a, b in r[1:]]

def line_chart(name, title, series, marks):
    """series: [(label, colour, rows)], first one is the lead. marks: [(series_idx, date, text, anchor, dx, dy)]"""
    W = max(1000, 110 + len(title) * 31); left, right, top, ph = 110, 60, 285, 400
    base = top + ph; n = len(series[0][2]); h = base + 150
    xp = lambda i: left + i / (n - 1) * (W - left - right); yp = lambda v: base - v / 100 * ph
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}" height="{h}">', f'<rect width="{W}" height="{h}" fill="#FFFFFF"/>',
         f'<text x="50" y="78" font-family="{SERIF}" font-weight="700" font-size="56" fill="{INK}">{html.escape(title)}</text>']
    for j, l in enumerate(UNIT):
        p.append(f'<text x="50" y="{124 + j * 32}" font-family="{SANS}" font-size="25" fill="{MUTED}">{html.escape(l)}</text>')
    lx = 50
    for lab, col, _ in series:
        p.append(f'<circle cx="{lx + 10}" cy="{222}" r="10" fill="{col}"/><text x="{lx + 30}" y="231" font-family="{SANS}" font-size="25" fill="{INK}">{html.escape(lab)}</text>')
        lx += 70 + len(lab) * 14
    for v in (0, 50, 100):
        p.append(f'<line x1="{left}" y1="{yp(v)}" x2="{W - right}" y2="{yp(v)}" stroke="#BDBDBD" stroke-width="{1.5 if v == 0 else 1}"{"" if v == 0 else " stroke-dasharray=\"3,6\""}/>')
        p.append(f'<text x="{left - 16}" y="{yp(v) + 8}" text-anchor="end" font-family="{SANS}" font-size="22" fill="{INK}">{v}</text>')
    seen = set()
    for i, (d, _) in enumerate(series[0][2]):
        dt = datetime.datetime.strptime(d, "%Y-%m-%d")
        if (dt.year, dt.month) not in seen:
            seen.add((dt.year, dt.month))
            if i and dt.month % 2 == 1:
                p.append(f'<text x="{xp(i):.1f}" y="{base + 40}" text-anchor="middle" font-family="{SANS}" font-size="22" fill="{INK}">{dt.strftime("%b")}{" " + str(dt.year) if dt.month == 1 else ""}</text>')
    for lab, col, rows in reversed(series):
        pts = " ".join(f"{xp(i):.1f},{yp(v):.1f}" for i, (_, v) in enumerate(rows))
        p.append(f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="{5 if col == PINK else 4}" stroke-linejoin="round" stroke-linecap="round"/>')
    for si, date, text, anchor, dx, dy in marks:
        rows = series[si][2]; i = [d for d, _ in rows].index(date); v = rows[i][1]
        p.append(f'<circle cx="{xp(i):.1f}" cy="{yp(v):.1f}" r="8" fill="{series[si][1]}" stroke="#FFFFFF" stroke-width="3"/>')
        p.append(f'<text x="{xp(i) + dx:.1f}" y="{yp(v) + dy:.1f}" text-anchor="{anchor}" font-family="{SANS}" font-size="22" fill="{INK}">{html.escape(text)}</text>')
    p.append(f'<text x="40" y="{h - 30}" font-family="{SANS}" font-size="20" fill="{INK}">{SRC}</text></svg>')
    return name, "\n".join(p)

mj, cm, qp, oj, ci = (load(x) for x in ("mandarin_jacket", "chinamaxxing", "qipao", "opera_jacket", "conner_ives"))
pk = lambda rows: max(rows, key=lambda r: r[1])[0]
assert pk(cm) == "2026-02-22" and pk(mj) == "2026-04-12" and pk(qp) == pk(oj) == "2026-02-15" and pk(ci) == "2026-10-25"
charts = [
 line_chart("01-meme-then-jacket", "the meme came first, then the jacket", [("mandarin jacket", PINK, mj), ("chinamaxxing", DARK, cm)],
            [(1, "2026-02-22", "22 Feb", "end", -16, 6), (0, "2026-04-12", "12 Apr", "middle", 0, -20)]),
 line_chart("02-lunar-new-year", "qipao stays high long after lunar new year", [("qipao", PINK, qp), ("opera jacket", DARK, oj)],
            [(0, "2026-02-15", "15 Feb, both peak", "end", -16, 6)]),
 line_chart("03-conner-ives", "conner ives climbs as the jacket cools", [("conner ives", PINK, ci), ("mandarin jacket", DARK, mj)],
            [(0, "2026-09-13", "13 Sep, New York show week", "end", -16, 2), (0, "2026-10-25", "25 Oct", "end", -16, 6)]),
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
