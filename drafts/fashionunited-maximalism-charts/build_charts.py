# FashionUnited maximalism piece, Paris SS27. Same chart style as the denim FashionUnited
# charts (white background, dark bars, pink highlight on the season average, Playfair title,
# unit stated in the subtitle, source line at the bottom). Reuses the denim script's helpers.
# Usage: python3 build_charts.py <out_dir>
#        NODE_PATH=$(npm root -g) node ../../.claude/skills/runway-decode-trends/scripts/render_png.js <out_dir> <png_dest>
# Figures: Paris SS27 colour index notes (neutral share and pink share per house, Colour mix
# donut and Overview tabs) and the maximalism reel data check (embellished share, Looks tab).
import sys, os, json
OUT = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(f'{HERE}/../fashionunited-denim-charts/build_charts.py').read()
src = src[:src.index('charts = []')]
# the peak annotation divides by the preceding year's value, which is 0 for low-volume terms
src = src.replace('chg = half_up(100 * (series[pk][1] / series[pk][2] - 1))', 'chg = half_up(100 * (series[pk][1] / series[pk][2] - 1)) if series[pk][2] else None')
src = src.replace('p.append(f\'<text x="{px+18:.1f}" y="{py+4:.1f}" font-family="{SANS}" font-size="30" fill="{INK}">+{chg}% vs last year</text>\')', 'lab = \'peak\'\n    p.append(f\'<text x="{px+18:.1f}" y="{py+4:.1f}" font-family="{SANS}" font-size="30" fill="{INK}">{lab}</text>\')')
assert 'if series[pk][2] else None' in src and "lab = 'peak'" in src
exec(src)   # helpers and constants only, none of the denim charts

PARIS_SRC = 'Source: The Data Fashion Brief runway tagging, Paris Fashion Week SS27'
charts = []

# 1. Neutral share of each house's palette, every house, season average highlighted
neutral = [('Lanvin', 89), ('Celine', 81), ('Balenciaga', 74), ('Chloé', 72), ('Dior', 67),
           ('Isabel Marant', 66), ('Tom Ford', 63), ('Chanel', 62), ('Maison Margiela', 60),
           ('Stella McCartney', 55), ('Loewe', 45), ('Lacoste', 42), ('Valentino', 40),
           ('Miu Miu', 35), ('Balmain', 34), ('Dries Van Noten', 22), ('season average', 56)]
charts.append(hbar_chart('01-neutral-by-house', 'Where Paris stayed neutral',
    "% of each house's colour palette in black, white, cream, grey or brown, vs the season average",
    neutral, PARIS_SRC + ', colour mix', highlight=(len(neutral) - 1,)))
# wide vertical version of the same chart, in case the editor prefers it
charts.append(bar_chart('01b-neutral-by-house-wide', 'Where Paris stayed neutral',
    "% of each house's colour palette in black, white, cream, grey or brown, vs the season average",
    neutral, PARIS_SRC + ', colour mix', highlight=(len(neutral) - 1,)))

# 2. Pink share of each house's palette, houses at 7% or more (same cut as the Substack chart)
pink = [('Isabel Marant', 16), ('Valentino', 13), ('Stella McCartney', 9), ('Chloé', 8),
        ('Dior', 8), ('Dries Van Noten', 8), ('Balenciaga', 7), ('season average', 5)]
charts.append(bar_chart('02-pink-by-house', 'Where the pink actually lives',
    "% of each house's colour palette that is pink, vs the season average",
    pink, PARIS_SRC + ', colour mix', highlight=(len(pink) - 1,)))

# 3. Embellished share of each house's looks. PROVISIONAL: only the three leaders and the
#    season average are in the notes, the other 13 houses come from the Looks tab.
emb = [('Dior', 70), ('Chloé', 69), ('Isabel Marant', 60), ('season average', 31)]
charts.append(bar_chart('03-embellishment-by-house', 'Where the decoration lives',
    "% of each house's looks with at least one embellishment, vs the season average",
    emb, PARIS_SRC + ', Looks tab', highlight=(len(emb) - 1,)))

# 4. Paris season palette, ranked (colour index season numbers, rounded slices)
palette = [('black', 21), ('white and cream', 17), ('brown and beige', 11), ('green and olive', 8),
           ('grey', 7), ('pink', 5), ('blue', 5), ('yellow and gold', 5), ('navy', 4),
           ('floral print', 4), ('orange and rust', 3), ('graphic print', 3), ('red', 2),
           ('animal print', 2), ('purple', 1), ('burgundy', 1), ('other print', 1)]
charts.append(hbar_chart('04-paris-palette', 'The Paris palette, more than half neutral',
    "% of the season's colour palette in each colour family, every look split across up to three colours",
    palette, PARIS_SRC + ', colour mix', highlight=(0, 1, 2, 4)))

# 5. Season donut with a title: the colour index donut inlined under a FashionUnited head,
#    no legend, as on the Substack version (Carmen's call).
import re as _re
donut = open(f'{HERE}/../paris-ss27-colour/donut-season.svg').read()
inner = donut[donut.index('>') + 1:donut.rindex('</svg>')]
slices = _re.findall(r'fill="(#[0-9A-Fa-f]{6})"[^>]*><title>([^<]+)</title>', donut)
W, H = 1300, 1180
p = head(W, H, 'The Paris palette, more than half neutral',
         "% of the season's colour palette in each colour family, every look split across up to three colours")
p.append(f'<svg x="{(W-820)/2}" y="200" width="820" height="820" viewBox="-2 -2 814 814">{inner}</svg>')
p.append(f'<text x="40" y="{H-30}" font-family="{SANS}" font-size="20" fill="{INK}">{html.escape(PARIS_SRC + ", colour mix")}</text>')
p.append('</svg>')
charts.append(('05-paris-palette-donut', '\n'.join(p), H))

# 6 to 8. Google Trends, past year vs preceding year, one chart per term (separate exports, each
#    scaled to its own peak, so they are compared with their own prior year, never with each other).
GT = 'Source: The Data Fashion Brief analysis of Google Trends, worldwide, 26 Oct 2025 to 25 Oct 2026'
def yoy(name, csvname, term, title):
    s = load_series(f'{HERE}/data/{csvname}.csv')
    above = sum(1 for _, a, c in s if a > c)
    pk = max(s, key=lambda r: r[1])
    import datetime as _dt
    pk_m = _dt.date.fromisoformat(pk[0]).strftime('%B')
    note = f'Peaked in {pk_m}; latest week {s[-1][1]} vs {s[-1][2]} a year earlier; above the preceding year in {above} of {len(s)} weeks.'
    return line_chart(name, title, f'weekly search interest in "{term}", Google Trends 0 to 100 scale',
                      s, 'past year', 'preceding year', note, GT)
charts.append(yoy('06-quiet-luxury-year-on-year', 'quiet_luxury', 'quiet luxury', 'Quiet luxury peaked, then fell back'))
charts.append(yoy('07-80s-luxury-year-on-year', '80s_luxury', '80s luxury', 'Eighties luxury had a spring moment'))
charts.append(yoy('08-chunky-belt-year-on-year', 'chunky_belt', 'chunky belt', 'The chunky belt spiked twice'))

# 9. Quiet luxury, cropped from its May peak to the latest week (Carmen: show the peak and the now)
ql = load_series(f'{HERE}/data/quiet_luxury.csv')
pk_i = max(range(len(ql)), key=lambda i: ql[i][1])
crop = ql[pk_i:]
charts.append(line_chart('09-quiet-luxury-peak-to-now', 'Quiet luxury, from its peak to now',
    'weekly search interest in "quiet luxury", Google Trends 0 to 100 scale, May to October 2026',
    crop, 'past year', 'preceding year',
    f'From 100 in the week of 10 May to {crop[-1][1]} in the latest week, below the {crop[-1][2]} of the same week a year earlier.',
    GT))

# 10. Eighties luxury and chunky belt, last year vs this year, average weekly interest, with growth
def avg(name):
    s = load_series(f'{HERE}/data/{name}.csv')
    return sum(r[2] for r in s) / len(s), sum(r[1] for r in s) / len(s)
groups = [('80s luxury', *avg('80s_luxury')), ('chunky belt', *avg('chunky_belt'))]
W, H = 1300, 900
p = head(W, H, 'The loud terms had their biggest year',
         'average weekly search interest, Google Trends index, preceding year vs past year')
p.append(f'<rect x="60" y="165" width="34" height="34" fill="{DARK}"/><text x="108" y="191" font-family="{SANS}" font-size="25" fill="{INK}">preceding year</text>')
p.append(f'<rect x="330" y="165" width="34" height="34" fill="{PINK}"/><text x="378" y="191" font-family="{SANS}" font-size="25" fill="{INK}">past year</text>')
top, base, bw, gap = 300, 700, 150, 30
scale = (base - top - 60) / max(v for _, a, b in groups for v in (a, b))
for gi, (lab, last, this) in enumerate(groups):
    gx = 200 + gi * 600
    for k, (v, col) in enumerate(((last, DARK), (this, PINK))):
        x = gx + k * (bw + gap)
        bh = v * scale
        p.append(f'<rect x="{x}" y="{base-bh:.1f}" width="{bw}" height="{bh:.1f}" fill="{col}"/>')
        p.append(f'<text x="{x+bw/2:.1f}" y="{base-bh-14:.1f}" text-anchor="middle" font-family="{SANS}" font-size="40" fill="{INK}">{half_up(v)}</text>')
    growth = half_up(100 * (this / last - 1))
    cx = gx + bw + gap / 2
    p.append(f'<text x="{cx:.1f}" y="{base-this*scale-70:.1f}" text-anchor="middle" font-family="{SANS}" font-size="30" fill="{PINK}">+{growth}% vs last year</text>')
    p.append(f'<text x="{cx:.1f}" y="{base+46}" text-anchor="middle" font-family="{SANS}" font-size="28" fill="{INK}">"{lab}"</text>')
p.append(f'<line x1="150" y1="{base}" x2="{W-150}" y2="{base}" stroke="#BDBDBD" stroke-width="1.5"/>')
p.append(f'<text x="50" y="{H-80}" font-family="{SANS}" font-size="25" fill="{INK}">Each term is indexed to its own peak, so compare each with its own prior year, not with the other.</text>')
p.append(f'<text x="40" y="{H-30}" font-family="{SANS}" font-size="20" fill="{INK}">{html.escape(GT)}</text>')
p.append('</svg>')
charts.append(('10-loud-terms-year-on-year', '\n'.join(p), H))

FONTS = '<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,500;0,700;1,500&family=Questrial&display=swap" rel="stylesheet">'
manifest = []
for name, svg, h in charts:
    assert '–' not in svg and '—' not in svg
    open(f'{OUT}/{name}.svg', 'w').write(svg)
    open(f'{OUT}/{name}.html', 'w').write(f'<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>body{{margin:0;background:#fff}}</style></head><body>{svg}</body></html>')
    manifest.append({'name': name, 'h': h})
json.dump(manifest, open(f'{OUT}/manifest.json', 'w'))
print([n for n, _, _ in charts])
