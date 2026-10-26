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

FONTS = '<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,500;0,700;1,500&family=Questrial&display=swap" rel="stylesheet">'
manifest = []
for name, svg, h in charts:
    assert '–' not in svg and '—' not in svg
    open(f'{OUT}/{name}.svg', 'w').write(svg)
    open(f'{OUT}/{name}.html', 'w').write(f'<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>body{{margin:0;background:#fff}}</style></head><body>{svg}</body></html>')
    manifest.append({'name': name, 'h': h})
json.dump(manifest, open(f'{OUT}/manifest.json', 'w'))
print([n for n, _, _ in charts])
