# Usage: python3 build_charts.py <out_dir>   (writes .svg + .html per chart + manifest.json)
#        NODE_PATH=$(npm root -g) node ../../.claude/skills/runway-decode-trends/scripts/render_png.js <out_dir> <png_dest>
# Same chart style as the Paris SS27 Runway Decode charts (runway-decode-trends skill):
# white background, vertical bars, dark grey with one pink highlight, bold Playfair title,
# Century Gothic/Questrial labels, unit stated in every subtitle, source line at the bottom.
# Runway figures are Carmen's Paris SS27 denim decode and the NYFW SS27 piece; search
# figures come from the three Google Trends exports in data/.
import sys, html, json, csv, re, datetime, os
OUT = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))

PINK, DARK, INK, MUTED, BLACK, NEG = '#D6447A', '#3A3A3A', '#222222', '#6B6B6B', '#111114', '#B5473F'
SERIF = "'Playfair Display', Georgia, serif"
SANS = "'Century Gothic', 'Questrial', 'Avenir', sans-serif"

def half_up(v):
    # round half up (Python's round() sends 62.5 to 62, the article says 63)
    import math
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

def head(W, h, title, subtitle):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}" height="{h}">',
            f'<rect width="{W}" height="{h}" fill="#FFFFFF"/>',
            f'<text x="50" y="78" font-family="{SERIF}" font-weight="700" font-size="56" fill="{INK}">{html.escape(title)}</text>',
            f'<text x="50" y="124" font-family="{SANS}" font-size="25" fill="{MUTED}">{html.escape(subtitle)}</text>']

def bar_chart(name, title, subtitle, items, source, fmt=lambda v: f'{half_up(v)}%', highlight=(0,)):
    """items: (label, value); values may be negative (bars drop below the baseline).
    highlight: indexes drawn in pink, everything else dark grey."""
    n = len(items)
    W = max(1000, 100 + n * 150)
    top, plot_h, left, right = 175, 360, 50, 50
    slot = min((W - left - right) / n, 165)
    x0 = (W - slot * n) / 2
    bw = min(150, slot * 0.84)
    vmax = max(max(v for _, v in items), 0)
    vmin = min(min(v for _, v in items), 0)
    usable = plot_h - 70
    scale = usable / (vmax - vmin)
    base = top + 70 + vmax * scale          # y of the zero line
    bottom = base + (-vmin) * scale          # lowest bar end
    wn = max(8, int(slot / 12.5))
    vs = min(42, round(slot * 0.34))
    label_lines = max(len(wrap(l, wn)) for l, _ in items)
    h = int(bottom + 46 + label_lines * 31 + 80)
    p = head(W, h, title, subtitle)
    for i, (lab, v) in enumerate(items):
        cx = x0 + slot * (i + 0.5)
        bh = abs(v) * scale
        y = base - bh if v >= 0 else base
        col = PINK if i in highlight else DARK
        p.append(f'<rect x="{cx-bw/2:.1f}" y="{y:.1f}" width="{bw:.1f}" height="{bh:.1f}" fill="{col}"/>')
        vy = base - bh - 14 if v >= 0 else base + bh + vs + 4
        p.append(f'<text x="{cx:.1f}" y="{vy:.1f}" text-anchor="middle" font-family="{SANS}" font-size="{vs}" fill="{INK}">{html.escape(fmt(v))}</text>')
        ly = bottom + 44 + (vs + 14 if vmin < 0 else 0)  # every label on one line, below the lowest value
        for j, line in enumerate(wrap(lab, wn)):
            p.append(f'<text x="{cx:.1f}" y="{ly+j*31:.1f}" text-anchor="middle" font-family="{SANS}" font-size="25" fill="{INK}">{html.escape(line)}</text>')
    p.append(f'<line x1="{x0-10:.1f}" y1="{base:.1f}" x2="{x0+slot*n+10:.1f}" y2="{base:.1f}" stroke="#BDBDBD" stroke-width="1.5"/>')
    if vmin < 0:
        h += 50
        p[0] = p[0].replace(f'viewBox="0 0 {W} {h-50}" width="{W}" height="{h-50}"', f'viewBox="0 0 {W} {h}" width="{W}" height="{h}"')
        p[1] = f'<rect width="{W}" height="{h}" fill="#FFFFFF"/>'
    p.append(f'<text x="40" y="{h-30}" font-family="{SANS}" font-size="20" fill="{INK}">{html.escape(source)}</text>')
    p.append('</svg>')
    return name, '\n'.join(p), h


def hbar_chart(name, title, subtitle, items, source, fmt=lambda v: f'{half_up(v)}%', highlight=(0,)):
    """Horizontal ranked list: label on the left, bar, value at the bar end. Values may be negative."""
    W, left_lab, right_pad, row, top = 1300, 360, 150, 74, 190
    n = len(items)
    vmax = max(max(v for _, v in items), 0); vmin = min(min(v for _, v in items), 0)
    plot_w = W - left_lab - right_pad - (110 if vmin < 0 else 0)
    scale = plot_w / (vmax - vmin)
    zero = left_lab + (110 if vmin < 0 else 0) + (-vmin) * scale
    h = top + n * row + 90
    p = head(W, h, title, subtitle)
    for i, (lab, v) in enumerate(items):
        y = top + i * row
        bh = 50
        col = PINK if i in highlight else DARK
        op = ''
        if v < 0:
            col, op = NEG, ' opacity="0.6"'  # declines in a muted red, softened
        x = zero if v >= 0 else zero - abs(v) * scale
        p.append(f'<text x="{left_lab-24}" y="{y+bh/2+9:.1f}" text-anchor="end" font-family="{SANS}" font-size="28" fill="{INK}">{html.escape(lab)}</text>')
        p.append(f'<rect x="{x:.1f}" y="{y}" width="{abs(v)*scale:.1f}" height="{bh}" fill="{col}"{op}/>')
        if v >= 0:
            p.append(f'<text x="{zero+v*scale+14:.1f}" y="{y+bh/2+12:.1f}" font-family="{SANS}" font-size="34" fill="{INK}">{html.escape(fmt(v))}</text>')
        else:
            p.append(f'<text x="{x-14:.1f}" y="{y+bh/2+12:.1f}" text-anchor="end" font-family="{SANS}" font-size="34" fill="{NEG}">{html.escape(fmt(v))}</text>')
    p.append(f'<line x1="{zero:.1f}" y1="{top-12}" x2="{zero:.1f}" y2="{top+n*row-12}" stroke="#BDBDBD" stroke-width="1.5"/>')
    p.append(f'<text x="40" y="{h-30}" font-family="{SANS}" font-size="20" fill="{INK}">{html.escape(source)}</text>')
    p.append('</svg>')
    return name, '\n'.join(p), h

def smooth_path(pts):
    """Catmull-Rom spline through the points, as an SVG cubic path."""
    d = f'M{pts[0][0]:.1f},{pts[0][1]:.1f}'
    for i in range(len(pts) - 1):
        p0 = pts[i - 1] if i else pts[i]; p1 = pts[i]; p2 = pts[i + 1]
        p3 = pts[i + 2] if i + 2 < len(pts) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f' C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}'
    return d

def load_series(path):
    rows = list(csv.reader(open(path)))[1:]
    return [(r[0], int(r[1]), int(r[2])) for r in rows]

def line_chart(name, title, subtitle, series, lead_name, compare_name, note, source):
    """Two weekly series on Google Trends' own 0 to 100 scale, pink lead, black comparison,
    dashed gridlines at 0/50/100, month ticks, one-line chart note (CLAUDE.md spec)."""
    W, h = 1200, 760
    x0, x1, y0, y1 = 110, 1150, 270, 590
    n = len(series)
    xp = lambda i: x0 + i / (n - 1) * (x1 - x0)
    yp = lambda v: y1 - v / 100 * (y1 - y0)
    p = head(W, h, title, subtitle)
    p.append(f'<line x1="44" y1="180" x2="84" y2="180" stroke="{PINK}" stroke-width="5"/><text x="98" y="189" font-family="{SANS}" font-size="25" fill="{INK}">{html.escape(lead_name)}</text>')
    lx = 98 + len(lead_name) * 14 + 50
    p.append(f'<line x1="{lx}" y1="180" x2="{lx+40}" y2="180" stroke="{PINK}" stroke-width="4" stroke-dasharray="9,7" opacity="0.45"/><text x="{lx+54}" y="189" font-family="{SANS}" font-size="25" fill="{INK}">{html.escape(compare_name)}</text>')
    for v in (0, 50, 100):
        dash = '' if v == 0 else ' stroke-dasharray="4,6"'
        p.append(f'<line x1="{x0}" y1="{yp(v):.1f}" x2="{x1}" y2="{yp(v):.1f}" stroke="#D9D9D9" stroke-width="1.5"{dash}/>')
        p.append(f'<text x="{x0-16}" y="{yp(v)+8:.1f}" text-anchor="end" font-family="{SANS}" font-size="22" fill="{INK}">{v}</text>')
    prev = smooth_path([(xp(i), yp(r[2])) for i, r in enumerate(series)])
    cur = smooth_path([(xp(i), yp(r[1])) for i, r in enumerate(series)])
    p.append(f'<path d="{prev}" fill="none" stroke="{PINK}" stroke-width="3.5" stroke-dasharray="10,8" opacity="0.45"/>')
    p.append(f'<path d="{cur}" fill="none" stroke="{PINK}" stroke-width="4.5"/>')
    pk = max(range(n), key=lambda i: series[i][1])
    chg = half_up(100 * (series[pk][1] / series[pk][2] - 1))
    px, py = xp(pk), yp(series[pk][1])
    p.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="8" fill="{PINK}"/>')
    p.append(f'<text x="{px+18:.1f}" y="{py+4:.1f}" font-family="{SANS}" font-size="30" fill="{INK}">+{chg}% vs last year</text>')
    seen, ticks = set(), []
    for i, (d, _, _) in enumerate(series):
        dt = datetime.datetime.strptime(d, '%Y-%m-%d')
        if (dt.year, dt.month) not in seen:
            seen.add((dt.year, dt.month)); ticks.append((i, dt.strftime('%b')))
    for i, lab in ticks[::2]:
        p.append(f'<text x="{xp(i):.1f}" y="{y1+40}" text-anchor="middle" font-family="{SANS}" font-size="22" fill="{INK}">{lab}</text>')
    p.append(f'<text x="50" y="{h-80}" font-family="{SANS}" font-size="25" fill="{INK}">{html.escape(note)}</text>')
    p.append(f'<text x="40" y="{h-30}" font-family="{SANS}" font-size="20" fill="{INK}">{html.escape(source)}</text>')
    p.append('</svg>')
    return name, '\n'.join(p), h

PARIS = 'Source: The Data Fashion Brief runway tagging, Paris Fashion Week SS27'
BOTH = 'Source: The Data Fashion Brief runway tagging, New York and Paris Fashion Week SS27'
GT = 'Source: The Data Fashion Brief analysis of Google Trends, worldwide, Oct 2025 to Oct 2026'
charts = []

# 1. Denim by house, Paris (Carmen's decode; Margiela confirmed 14). Houses at 1 to 2% left out,
#    their exact shares aren't in the decode.
charts.append(bar_chart('01-denim-by-house', 'where the denim lives in paris',
    "% of each house's own looks that include denim, vs the Paris average",
    [('Stella McCartney', 16), ('Maison Margiela', 14), ('Balenciaga', 11), ('Tom Ford', 11),
     ('Miu Miu', 8), ('Isabel Marant', 4), ('Paris average', 4)], PARIS, highlight=(6,)))

# 2. Reach: share of houses/shows with denim, Paris 10 of 16, NYFW 5 of 13
charts.append(bar_chart('02-denim-reach-by-city', 'denim reached most of paris',
    '% of houses that showed denim at least once',
    [('Paris', 100 * 10 / 16), ('New York', 100 * 5 / 13)], BOTH))

# 3. What the denim was, Paris: share of the 44 denim pieces
charts.append(bar_chart('03-denim-by-piece', 'the jean does the work',
    '% of all Paris denim pieces that are each type of piece',
    [('trousers', 100 * 33 / 44), ('jackets', 100 * 4 / 44), ('skirts', 100 * 4 / 44)], PARIS))

# 4. Fit and leg, Paris: share of the 44 denim pieces
charts.append(bar_chart('04-denim-fit', 'relaxed, straight, full length',
    '% of all Paris denim pieces with each fit or leg shape',
    [('relaxed fit', 100 * 34 / 44), ('full length', 100 * 29 / 44), ('straight leg', 100 * 21 / 44),
     ('wide leg', 100 * 7 / 44), ('skinny', 100 * 1 / 44)], PARIS))

# 5. Wash, Paris: share of the 44 denim pieces
charts.append(bar_chart('05-denim-by-wash', 'mid-wash leads',
    '% of all Paris denim pieces in each wash',
    [('mid-wash', 100 * 24 / 44), ('indigo', 100 * 7 / 44), ('white and off-white', 100 * 6 / 44),
     ('charcoal', 100 * 3 / 44)], PARIS))

# 6 to 8. Top searches file (seed assumed "jeans", confirm with Carmen)
top = {r['query']: (int(r['search interest']), int(r['increase percent'].rstrip('%')))
       for r in csv.DictReader(open(f'{HERE}/data/top_jeans_searches.csv'))}
styles = ['straight jeans', 'baggy jeans', 'skinny jeans', 'wide leg jeans', 'bootcut jeans',
          'barrel jeans', 'flare jeans', 'mom jeans']
lab = lambda q: q.replace(' jeans', '')
charts.append(hbar_chart('06-most-searched-styles', 'straight beats barrel in search',
    "search interest as a % of the most searched jeans query (men's jeans)",
    [(lab(q), top[q][0]) for q in styles], GT,
    highlight=(0, styles.index('barrel jeans'))))
growth = ['straight fit jeans', 'straight leg jeans', 'straight jeans', 'barrel jeans', 'bootcut jeans',
          'skinny jeans', 'wide leg jeans', 'baggy jeans', 'mom jeans', 'flared jeans']
charts.append(hbar_chart('07-fastest-growing-styles', 'the straight leg is growing fastest',
    '% change in search interest vs the previous period, by jeans style',
    [(lab(q), top[q][1]) for q in growth], GT, fmt=lambda v: f'{"+" if v > 0 else ""}{half_up(v)}%',
    highlight=(0, 1, 2)))
brands = ["levi's jeans", 'calvin klein jeans', 'gap jeans', 'old navy', 'h&m', 'zara jeans']
blab = {"levi's jeans": "Levi's", 'calvin klein jeans': 'Calvin Klein', 'gap jeans': 'Gap',
        'old navy': 'Old Navy', 'h&m': 'H&M', 'zara jeans': 'Zara'}
charts.append(hbar_chart('08-brand-searches', 'heritage denim names grow fastest',
    '% change in search interest vs the previous period, brand searches within jeans',
    [(blab[q], top[q][1]) for q in brands], GT, fmt=lambda v: f'+{half_up(v)}%', highlight=(0, 1)))
colours = ['brown jeans', 'light blue jeans', 'white jeans', 'black jeans', 'blue jeans']
charts.append(hbar_chart('09-colour-searches', 'lighter and warmer washes rise',
    '% change in search interest vs the previous period, by jeans colour',
    [(lab(q), top[q][1]) for q in colours], GT, fmt=lambda v: f'+{half_up(v)}%', highlight=(0, 1, 2)))

# 10. Barrel jeans, past year vs preceding year
b = load_series(f'{HERE}/data/barrel_jeans.csv')
above = sum(1 for _, a, c in b if a > c)
charts.append(line_chart('10-barrel-year-on-year', 'the barrel is maturing, not fading',
    'weekly search interest in "barrel jeans", Google Trends 0 to 100 scale',
    b, 'past year', 'preceding year',
    f'Above the preceding year in {above} of the last {len(b)} weeks, and at {b[-1][1]} vs {b[-1][2]} in the latest week.',
    GT))

FONTS = '<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,500;0,700;1,500&family=Questrial&display=swap" rel="stylesheet">'
manifest = []
for name, svg, h in charts:
    assert '–' not in svg and '—' not in svg
    open(f'{OUT}/{name}.svg', 'w').write(svg)
    open(f'{OUT}/{name}.html', 'w').write(f'<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>body{{margin:0;background:#fff}}</style></head><body>{svg}</body></html>')
    manifest.append({'name': name, 'h': h})
json.dump(manifest, open(f'{OUT}/manifest.json', 'w'))
print([n for n, _, _ in charts])
