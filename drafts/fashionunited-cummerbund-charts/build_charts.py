# Usage: python3 build_charts.py <out_dir>   (writes .svg + .html per chart + manifest.json)
#        NODE_PATH=$(npm root -g) node ../../.claude/skills/runway-decode-trends/scripts/render_png.js <out_dir> <png_dest>
# Same chart style as the FashionUnited denim charts (../fashionunited-denim-charts/build_charts.py):
# white background, dark grey bars with one pink highlight, bold Playfair title, Century Gothic
# labels, unit stated in every subtitle, source line at the bottom.
# Runway figures are Carmen's Paris SS27 tagging (as published in The Nod, 29 Oct 2026);
# search figures come from her Google Trends export in data/ (worldwide, monthly, 5 years).
import sys, html, json, csv, math, os
OUT = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))

PINK, DARK, INK, MUTED = '#D6447A', '#3A3A3A', '#222222', '#6B6B6B'
SERIF = "'Playfair Display', Georgia, serif"
SANS = "'Century Gothic', 'Questrial', 'Avenir', sans-serif"

def half_up(v):
    return int(math.floor(abs(v) + 0.5)) * (1 if v >= 0 else -1)

def wrap(label, n=14):
    words, lines, cur = label.split(), [], ''
    for w in words:
        if cur and len(cur) + 1 + len(w) > n:
            lines.append(cur); cur = w
        else:
            cur = f'{cur} {w}'.strip()
    lines.append(cur)
    return lines

def title_lines(title, W):
    return wrap(title, int((W - 100) / 29))

def head(W, h, title, subtitle):
    lines = title_lines(title, W)
    dy = 64 * (len(lines) - 1)
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}" height="{h}">',
           f'<rect width="{W}" height="{h}" fill="#FFFFFF"/>']
    for i, line in enumerate(lines):
        out.append(f'<text x="50" y="{78 + 64*i}" font-family="{SERIF}" font-weight="700" font-size="56" fill="{INK}">{html.escape(line)}</text>')
    out.append(f'<text x="50" y="{124 + dy}" font-family="{SANS}" font-size="25" fill="{MUTED}">{html.escape(subtitle)}</text>')
    return out, dy

def bar_chart(name, title, subtitle, items, source, fmt=lambda v: f'{half_up(v)}%', highlight=(0,), W=None):
    n = len(items)
    W = W or max(1000, 100 + n * 150)
    out, dy = head(W, 0, title, subtitle)
    top, plot_h = 175 + dy, 360
    slot = min((W - 100) / n, 190)
    x0 = (W - slot * n) / 2
    bw = min(150, slot * 0.8)
    vmax = max(v for _, v in items)
    scale = (plot_h - 70) / vmax
    base = top + plot_h
    wn = max(8, int(slot / 12.5))
    label_lines = max(len(wrap(l, wn)) for l, _ in items)
    h = int(base + 46 + label_lines * 31 + 80)
    p, _ = head(W, h, title, subtitle)
    for i, (lab, v) in enumerate(items):
        cx = x0 + slot * (i + 0.5)
        bh = v * scale
        col = PINK if i in highlight else DARK
        p.append(f'<rect x="{cx-bw/2:.1f}" y="{base-bh:.1f}" width="{bw:.1f}" height="{bh:.1f}" fill="{col}"/>')
        p.append(f'<text x="{cx:.1f}" y="{base-bh-14:.1f}" text-anchor="middle" font-family="{SANS}" font-size="42" fill="{INK}">{html.escape(fmt(v))}</text>')
        for j, line in enumerate(wrap(lab, wn)):
            p.append(f'<text x="{cx:.1f}" y="{base+44+j*31:.1f}" text-anchor="middle" font-family="{SANS}" font-size="25" fill="{INK}">{html.escape(line)}</text>')
    p.append(f'<line x1="{x0-10:.1f}" y1="{base:.1f}" x2="{x0+slot*n+10:.1f}" y2="{base:.1f}" stroke="#BDBDBD" stroke-width="1.5"/>')
    p.append(f'<text x="40" y="{h-30}" font-family="{SANS}" font-size="20" fill="{INK}">{html.escape(source)}</text>')
    p.append('</svg>')
    return name, '\n'.join(p), h

def line_chart(name, title, subtitle, series, note, source, ref=None, marks=()):
    """One monthly series on Google Trends' own 0 to 100 scale, pink line, dashed gridlines at
    0/50/100, a tick per year, optional dashed reference level, one-line chart note."""
    W, h = 1200, 740
    x0, x1, y0, y1 = 110, 1150, 230, 560
    n = len(series)
    xp = lambda i: x0 + i / (n - 1) * (x1 - x0)
    yp = lambda v: y1 - v / 100 * (y1 - y0)
    p, _ = head(W, h, title, subtitle)
    for v in (0, 50, 100):
        dash = '' if v == 0 else ' stroke-dasharray="4,6"'
        p.append(f'<line x1="{x0}" y1="{yp(v):.1f}" x2="{x1}" y2="{yp(v):.1f}" stroke="#D9D9D9" stroke-width="1.5"{dash}/>')
        p.append(f'<text x="{x0-16}" y="{yp(v)+8:.1f}" text-anchor="end" font-family="{SANS}" font-size="22" fill="{INK}">{v}</text>')
    if ref:
        lab, val = ref
        p.append(f'<line x1="{x0}" y1="{yp(val):.1f}" x2="{x1}" y2="{yp(val):.1f}" stroke="{DARK}" stroke-width="2" stroke-dasharray="10,8"/>')
        p.append(f'<text x="{x0+10}" y="{yp(val)+30:.1f}" font-family="{SANS}" font-size="22" fill="{INK}">{html.escape(lab)}</text>')
    d = 'M' + ' L'.join(f'{xp(i):.1f},{yp(v):.1f}' for i, (_, v) in enumerate(series))
    p.append(f'<path d="{d}" fill="none" stroke="{PINK}" stroke-width="4.5" stroke-linejoin="round"/>')
    val = dict(series)
    for dte, anchor, dx, dy in marks:
        i = [d for d, _ in series].index(dte)
        prev = val[f'{int(dte[:4]) - (int(dte[:4]) - 2024)}{dte[4:]}']   # same month of 2024, the flat baseline year
        chg = half_up(100 * (val[dte] / prev - 1))
        p.append(f'<circle cx="{xp(i):.1f}" cy="{yp(val[dte]):.1f}" r="8" fill="{PINK}"/>')
        for k, line in enumerate((f'April {dte[:4]}', f'+{chg}% vs April 2024')):
            p.append(f'<text x="{xp(i)+dx:.1f}" y="{yp(val[dte])+dy+k*30:.1f}" text-anchor="{anchor}" font-family="{SANS}" font-size="24" fill="{INK}">{line}</text>')
    for i, (dte, _) in enumerate(series):
        if dte[5:7] == '01':
            p.append(f'<line x1="{xp(i):.1f}" y1="{y1}" x2="{xp(i):.1f}" y2="{y1+8}" stroke="#BDBDBD" stroke-width="1.5"/>')
            p.append(f'<text x="{xp(i):.1f}" y="{y1+40}" text-anchor="middle" font-family="{SANS}" font-size="22" fill="{INK}">{dte[:4]}</text>')
    p.append(f'<text x="50" y="{h-80}" font-family="{SANS}" font-size="25" fill="{INK}">{html.escape(note)}</text>')
    p.append(f'<text x="40" y="{h-30}" font-family="{SANS}" font-size="20" fill="{INK}">{html.escape(source)}</text>')
    p.append('</svg>')
    return name, '\n'.join(p), h

PARIS = 'Source: The Data Fashion Brief runway tagging, Paris Fashion Week SS27'
GT = 'Source: The Data Fashion Brief analysis of Google Trends, worldwide, Nov 2021 to Nov 2026'
charts = []

# 1. The waist in Paris: share of collections (figures as Carmen gave them, checked by her)
charts.append(bar_chart('01-waist-in-paris', 'The waist is back in Paris',
    '% of Paris collections that showed each at least once',
    [('belted waists and corset-style tops', 88), ('cummerbund or wide waist sash', 38)],
    PARIS, highlight=(1,), W=1000))

# 2 and 3. Search: monthly series, and January to November averages by year
rows = [(r[0], int(r[1])) for r in list(csv.reader(open(f'{HERE}/data/cummerbund_worldwide_5y.csv')))[1:]]
avg = lambda y, months: sum(v for d, v in rows if d[:4] == str(y) and int(d[5:7]) in months) / len(months)
a2024 = avg(2024, range(1, 13))
since = [(d, v) for d, v in rows if d >= '2025-08-01']
assert all(v > a2024 for _, v in since)
jan_nov = range(1, 12)
years = [(str(y), avg(y, jan_nov)) for y in (2022, 2023, 2024, 2025, 2026)]
up24 = half_up(100 * (years[4][1] / years[2][1] - 1)); up25 = half_up(100 * (years[4][1] / years[3][1] - 1))
print('2026 vs 2024', up24, '2026 vs 2025', up25, [(y, round(v, 1)) for y, v in years])
charts.append(line_chart('02-cummerbund-search', 'Search interest has settled higher',
    'monthly search interest in "cummerbund", Google Trends 0 to 100 scale',
    rows, f'January to November 2026 averages {up24}% above 2024 and {up25}% above 2025.', GT,
    ref=('2024 average', a2024),
    marks=(('2025-04-01', 'end', -18, 4), ('2026-04-01', 'middle', 0, -50))))

charts.append(bar_chart('03-search-by-year', 'A higher level since 2025',
    'average monthly search interest in "cummerbund", January to November, Google Trends 0 to 100 scale',
    years, GT, fmt=lambda v: f'{half_up(v)}', highlight=(4,), W=1300))

FONTS = '<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,500;0,700;1,500&family=Questrial&display=swap" rel="stylesheet">'
manifest = []
for name, svg, h in charts:
    assert '–' not in svg and '—' not in svg
    open(f'{OUT}/{name}.svg', 'w').write(svg)
    open(f'{OUT}/{name}.html', 'w').write(f'<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>body{{margin:0;background:#fff}}</style></head><body>{svg}</body></html>')
    manifest.append({'name': name, 'h': h})
json.dump(manifest, open(f'{OUT}/manifest.json', 'w'))
print([n for n, _, _ in charts])
