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
exec(src[:src.index('charts = []')])   # helpers and constants only, none of the denim charts

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
#    with a small legend on the right so the slices can be named without a caption.
import re as _re
donut = open(f'{HERE}/../paris-ss27-colour/donut-season.svg').read()
inner = donut[donut.index('>') + 1:donut.rindex('</svg>')]
slices = _re.findall(r'fill="(#[0-9A-Fa-f]{6})"[^>]*><title>([^<]+)</title>', donut)
W, H = 1700, 1180
p = head(W, H, 'The Paris palette, more than half neutral',
         "% of the season's colour palette in each colour family, every look split across up to three colours")
p.append(f'<svg x="60" y="200" width="820" height="820" viewBox="-2 -2 814 814">{inner}</svg>')
lx, ly = 980, 250
for i, (col, lab) in enumerate(slices):
    name, pct = lab.rsplit(' ', 1)
    name = name.replace('/', ' and ').lower()
    y = ly + i * 46
    stroke = ' stroke="#D0CCC5" stroke-width="1"' if col.upper() == '#EDEAE3' else ''
    p.append(f'<rect x="{lx}" y="{y-22}" width="30" height="30" fill="{col}"{stroke}/>')
    p.append(f'<text x="{lx+46}" y="{y+1}" font-family="{SANS}" font-size="26" fill="{INK}">{html.escape(name)}</text>')
    p.append(f'<text x="{lx+560}" y="{y+1}" text-anchor="end" font-family="{SANS}" font-size="26" fill="{INK}">{html.escape(pct)}</text>')
p.append(f'<text x="40" y="{H-30}" font-family="{SANS}" font-size="20" fill="{INK}">{html.escape(PARIS_SRC + ", colour mix")}</text>')
p.append('</svg>')
charts.append(('05-paris-palette-donut', '\n'.join(p), H))

FONTS = '<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,500;0,700;1,500&family=Questrial&display=swap" rel="stylesheet">'
manifest = []
for name, svg, h in charts:
    assert '–' not in svg and '—' not in svg
    open(f'{OUT}/{name}.svg', 'w').write(svg)
    open(f'{OUT}/{name}.html', 'w').write(f'<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>body{{margin:0;background:#fff}}</style></head><body>{svg}</body></html>')
    manifest.append({'name': name, 'h': h})
json.dump(manifest, open(f'{OUT}/manifest.json', 'w'))
print([n for n, _, _ in charts])
