# Charts for "Stop Calling Everything a Trend: Fall/Winter 2027 Forecast Edition".
# Every number is as printed in the Trendalytics Womenswear Forecast FW27 PDF
# (October 2026) or in the Paris SS27 tagging already used in this repo.
# Usage: python3 build_charts.py <out_dir>   then
#        NODE_PATH=$(npm root -g) node ../../.claude/skills/runway-decode-trends/scripts/render_png.js <out_dir> <out_dir>
import sys, html, json, re
sys.dont_write_bytecode = True
OUT = sys.argv[1]

PINK, DARK, INK, MUTED = '#D6447A', '#3A3A3A', '#222222', '#6B6B6B'
SERIF = "'Playfair Display', Georgia, serif"
SANS = "'Century Gothic', 'Questrial', 'Avenir', sans-serif"

def wrap(label, n=14):
    parts = re.findall(r'[^\s/-]+[/-]?|\s+', label)
    toks = [' ' if t.isspace() else t for t in parts]
    lines, cur = [], ''
    for t in toks:
        if t == ' ':
            cur += ' '; continue
        if cur.strip() and len(cur.rstrip() + ('' if cur.endswith(('/', '-')) else ' ') + t) > n:
            lines.append(cur.strip()); cur = t
        else:
            cur = cur + t
    lines.append(cur.strip())
    return lines

def bar_chart(name, title, subtitle, items, source, fmt=lambda v: f'{round(v)}%', highlight=0, sub=None, colours=None):
    """items: list of (label, value). One bar pink (index `highlight`), rest dark.
    sub: optional list of muted sub-labels (the aesthetic each item belongs to)."""
    n = len(items)
    W = max(1000, 100 + n * 150, 110 + len(title) * 31)  # never let the title run off the canvas
    top, plot_h, left, right = 175, 360, 50, 50
    base = top + plot_h
    slot = min((W - left - right) / n, 165)
    x0 = (W - slot * n) / 2
    bw = min(150, slot * 0.84)
    vmax = max(v for _, v in items)
    wn = max(8, int(slot / 12.5))
    vs = min(42, round(slot * 0.34))
    label_lines = max(len(wrap(l, wn)) for l, _ in items)
    sub_lines = max(len(wrap(s, wn + 2)) for s in sub) if sub else 0
    h = base + 46 + label_lines * 31 + sub_lines * 24 + 80
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}" height="{h}">',
         f'<rect width="{W}" height="{h}" fill="#FFFFFF"/>',
         f'<text x="{left}" y="78" font-family="{SERIF}" font-weight="700" font-size="56" fill="{INK}">{html.escape(title)}</text>',
         f'<text x="{left}" y="124" font-family="{SANS}" font-size="25" fill="{MUTED}">{html.escape(subtitle)}</text>']
    for i, (lab, v) in enumerate(items):
        cx = x0 + slot * (i + 0.5)
        bh = (v / vmax) * (plot_h - 70)
        col = colours[i] if colours else (PINK if i == highlight else DARK)
        p.append(f'<rect x="{cx-bw/2:.1f}" y="{base-bh:.1f}" width="{bw:.1f}" height="{bh:.1f}" fill="{col}"/>')
        p.append(f'<text x="{cx:.1f}" y="{base-bh-14:.1f}" text-anchor="middle" font-family="{SANS}" font-size="{vs}" fill="{INK}">{html.escape(fmt(v))}</text>')
        lines = wrap(lab, wn)
        for j, line in enumerate(lines):
            p.append(f'<text x="{cx:.1f}" y="{base+44+j*31}" text-anchor="middle" font-family="{SANS}" font-size="25" fill="{INK}">{html.escape(line)}</text>')
        if sub:
            for k, line in enumerate(wrap(sub[i], wn + 2)):
                p.append(f'<text x="{cx:.1f}" y="{base+44+label_lines*31+k*24-4}" text-anchor="middle" font-family="{SANS}" font-size="19" fill="{MUTED}">{html.escape(line)}</text>')
    p.append(f'<line x1="{x0-10:.1f}" y1="{base}" x2="{x0+slot*n+10:.1f}" y2="{base}" stroke="#BDBDBD" stroke-width="1.5"/>')
    if source: p.append(f'<text x="{left-10}" y="{h-30}" font-family="{SANS}" font-size="20" fill="{INK}">{html.escape(source)}</text>')
    p.append('</svg>')
    return name, '\n'.join(p), h

SRC = 'Source: Trendalytics, Womenswear Forecast Fall/Winter 2027 (October 2026)'
HC, SR, VP = 'Heritage Craft', 'Sensory Riot', 'Veiled Performance'
charts = []

# 1. Search volume, every item that comes with one (thousands)
vol = [('marigold', 126, VP), ('lilac', 103, SR), ('fuchsia', 84, SR), ('forest green', 57, HC), ('dark red', 35, HC)]
colour_vol = bar_chart('08-colour-search-volume', 'marigold is the most searched',
    'search volume, in thousands of searches, for the five colours measured that way',
    [(l, v) for l, v, _ in vol], '', fmt=lambda v: f'{round(v)}k',
    highlight=0, sub=[a for _, _, a in vol], colours=['#DFAA4F', '#927EC3', '#FF278A', '#254117', '#7B3330'])

# 2. Year on year change in searches
gro = [('fringe skirts', 71, SR), ('paisley scarves', 64, HC), ('jacquard jackets', 61, HC),
       ('fur scarves', 30, SR), ('wedges', 23, SR), ('acid wash denim', 21, VP)]
charts.append(bar_chart('02-search-growth', 'fringe skirts are the top search mover',
    '% change in searches vs last year, as printed in the report',
    [(l, v) for l, v, _ in gro], SRC + ', searches vs last year', fmt=lambda v: f'+{round(v)}%',
    highlight=0, sub=[a for _, _, a in gro]))

# 3. Year on year change in market adoption
ado = [('artistic florals', 178, HC), ('slim suits', 133, HC), ('graphic prints', 51, SR),
       ('camouflage', 43, VP), ('nylon', 38, VP), ('feather trim', 36, SR), ('nylon bags', 28, VP),
       ('landscape graphics', 26, VP), ('embellished jeans', 23, SR), ('plaid', 21, HC)]
charts.append(bar_chart('03-market-adoption', 'florals and slim suits are the real jumps',
    "% change vs last year in the report's market adoption measure",
    [(l, v) for l, v, _ in ado], SRC + ', market adoption vs last year', fmt=lambda v: f'+{round(v)}%',
    highlight=0, sub=[a for _, _, a in ado]))

# 4. How the 36 items are measured
mix = [('market adoption vs last year', 10), ('searches vs last year', 6), ('influencer growth', 3),
       ('TikTok views', 2), ('"most saturated", no number', 2), ('search volume', 1)]
assert sum(v for _, v in mix) == 24
charts.append(bar_chart('04-metric-mix', 'six yardsticks, no item measured twice',
    'number of the 24 named trends (colours aside) measured each way',
    mix, SRC + ', count of items per measure', fmt=lambda v: f'{round(v)}', highlight=4))

# 5. Paris SS27 cross-check, share of looks (DFB tagging, 16 houses, 997 looks)
par = [('silk (all types)', 28), ('tweed', 5), ('lace', 4), ('denim', 4), ('nylon', 4),
       ('animal print', 3), ('brocade/jacquard', 2)]
charts.append(bar_chart('05-paris-cross-check', 'what the spring runway can already see',
    '% of all Paris SS27 looks that include each material',
    par, 'Source: The Data Fashion Brief runway tagging, Paris Fashion Week SS27, share of looks', highlight=0))

charts.append(colour_vol)
cgro = [('dove grey', 43, VP), ('plum purple', 39, HC), ('moss green', 23, VP), ('cobalt blue', 14, SR), ('terracotta', 7, VP)]
charts.append(bar_chart('09-colour-search-growth', 'dove grey climbs, terracotta barely moves',
    '% change in searches vs last year, for the five colours measured that way',
    [(l, v) for l, v, _ in cgro], '', fmt=lambda v: f'+{round(v)}%',
    highlight=0, sub=[a for _, _, a in cgro], colours=['#838384', '#583759', '#7E8C53', '#4C80FD', '#D38377']))
fam = [('brown & beige', 11, 'chestnut brown'), ('green & olive', 8, 'forest, moss'), ('grey', 7, 'dove grey'),
       ('pink', 5, 'fuchsia'), ('blue', 5, 'cobalt'), ('yellow & gold', 5, 'marigold, chartreuse'),
       ('orange & rust', 3, 'terracotta'), ('red', 2, 'russet'), ('purple', 1, 'plum, lilac')]
charts.append(bar_chart('10-paris-families', 'what paris ss27 already wore',
    '% of the Paris SS27 colour palette in each forecast colour family',
    [(l, v) for l, v, _ in fam], 'Source: The Data Fashion Brief runway tagging, Paris Fashion Week SS27, colour mix, 16 houses',
    highlight=1, sub=[a for _, _, a in fam],
    colours=['#7C533C', '#254117', '#838384', '#FF278A', '#4C80FD', '#DFAA4F', '#D38377', '#7B3330', '#583759']))

growth12 = [('plum purple', 60, HC, '#583759'), ('moss green', 60, VP, '#7E8C53'), ('dark red', 50, HC, '#7B3330'), ('forest green', 50, HC, '#254117'),
            ('cobalt blue', 30, SR, '#4C80FD'), ('marigold', 30, VP, '#DFAA4F'), ('dove grey', 30, VP, '#838384'), ('fuchsia', 20, SR, '#FF278A'),
            ('lilac', 10, SR, '#927EC3'), ('chartreuse', 10, SR, '#C7D344'), ('chestnut brown', 10, HC, '#7C533C'), ('terracotta', 10, VP, '#D38377')]
charts.append(bar_chart('12-colour-growth-all', 'plum and moss green are the climbers',
    '% change in Google searches this year vs last, all twelve colours on one scale',
    [(l, v) for l, v, _, _ in growth12], '', fmt=lambda v: f'+{round(v)}%',
    sub=[a for _, _, a, _ in growth12], colours=[c for _, _, _, c in growth12]))

FONTS = '<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,500;0,700;1,500&family=Questrial&display=swap" rel="stylesheet">'
manifest = []
for name, svg, h in charts:
    for bad in ('–', '—'):
        assert bad not in svg, name
    open(f'{OUT}/{name}.svg', 'w').write(svg)
    page = f'<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>body{{margin:0;background:#fff}}</style></head><body>{svg}</body></html>'
    open(f'{OUT}/{name}.html', 'w').write(page)
    manifest.append({'name': name, 'h': h})
json.dump(manifest, open(f'{OUT}/manifest.json', 'w'))
print([n for n, _, _ in charts])
