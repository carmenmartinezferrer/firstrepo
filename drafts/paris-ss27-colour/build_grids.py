# House donut grid (rows of 4) and swatch grid, DFB white chart style.
# Usage: python3 build_grids.py <SS27-paris.xlsx> <out_dir>   (run build_donuts.py first, same out_dir)
#   then: NODE_PATH=$(npm root -g) node render_grids.js <out_dir> <png_dest>
import sys, json, html, math
import pandas as pd
sys.dont_write_bytecode = True
DATA, OUT = sys.argv[1], sys.argv[2]
INK, MUTED = '#222222', '#6B6B6B'
SERIF = "'Playfair Display', Georgia, serif"
SANS = "'Century Gothic', 'Questrial', sans-serif"
FONTS = ('<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,500'
         '&family=Questrial&family=Arimo&display=swap" rel="stylesheet">')
SRC = 'Source: The Data Fashion Brief runway tagging, Paris Fashion Week SS27, colour mix'

def lum(h):
    h = h.lstrip('#'); c = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]

def slug(n): return 'donut-' + n.lower().replace(' ', '-').replace('é', 'e')

def page(title, subtitle, body, width):
    return (f'<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>'
            f'body{{margin:0;background:#fff}} #chart{{width:{width}px;padding:56px 60px 40px;box-sizing:border-box;background:#fff;color:{INK}}}'
            f'h1{{font-family:{SERIF};font-weight:700;font-size:58px;margin:0;line-height:1.1}}'
            f'.sub{{font-family:{SANS};font-size:26px;color:{MUTED};margin:14px 0 44px}}'
            f'.src{{font-family:{SANS};font-size:20px;margin-top:40px}}'
            f'.name{{font-family:{SERIF};font-style:italic;font-weight:500;color:{INK}}}'
            f'</style></head><body><div id="chart"><h1>{html.escape(title)}</h1><div class="sub">{html.escape(subtitle)}</div>'
            f'{body}<div class="src">{html.escape(SRC)}</div></div></body></html>')

c = pd.read_excel(DATA, sheet_name='Colour mix donut')
c['pct'] = c['Share pct'].round().astype(int)
houses = sorted(c[c.Level == 'house'].House.unique())

# 1. Donut grid, 4 per row, names under each, donut SVGs inlined (vector sharp)
def donut_grid(hs, name):
    cells = ''.join(
        f'<div style="text-align:center"><div style="width:100%">{open(f"{OUT}/{slug(h)}.svg").read().replace("width=\"814\" height=\"814\"", "width=\"100%\"")}</div>'
        f'<div class="name" style="font-size:34px;margin-top:14px">{html.escape(h)}</div></div>' for h in hs)
    body = f'<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:48px 56px">{cells}</div>'
    return name, page('house by house', "% = share of each house's total colour on the runway", body, 1600)

# 2. Swatch grid: house name beside its top five colours, same order as its donut
def swatch_grid(hs, name, season_row=True):
    rows = []
    groups = ([('Season', c[c.Level == 'fashion week'])] if season_row else []) + [(h, c[(c.Level == 'house') & (c.House == h)]) for h in hs]
    for h, g in groups:
        g = g[g.pct > 0].sort_values(['pct', 'Looks'], ascending=False).head(5)
        blocks = ''
        for _, r in g.iterrows():
            tc = '#FFFFFF' if lum(r.Hex) < 0.55 else '#000000'
            edge = 'box-shadow:inset 0 0 0 1.2px #D0CCC5;' if lum(r.Hex) > 0.82 else ''
            blocks += (f'<div style="background:{r.Hex};{edge}height:92px;display:flex;align-items:flex-end;padding:0 0 12px 14px;'
                       f'font-family:Arimo,Arial,sans-serif;font-size:26px;color:{tc}">{r.pct}%'
                       + (f'<span style="font-size:18px;margin-left:10px;opacity:.9">{html.escape(r.Colour.lower())}</span>' if 'print' in r.Colour.lower() else '')
                       + '</div>')
        blocks += ''.join('<div></div>' for _ in range(5 - len(g)))
        label = 'Season average' if h == 'Season' else h
        weight = 'font-weight:700;font-style:normal;' if h == 'Season' else ''
        rows.append(f'<div class="name" style="font-size:34px;{weight}align-self:center">{html.escape(label)}</div>{blocks}')
    body = ('<div style="display:grid;grid-template-columns:300px repeat(5,1fr);gap:10px 8px">' + ''.join(rows) + '</div>')
    return name, page('the top five colours, house by house', "% = share of each house's total colour, top five colours, largest first", body, 1600)

charts = [donut_grid(houses, 'grid-donuts-all'),
          donut_grid(houses[:8], 'grid-donuts-1-of-2'),
          donut_grid(houses[8:], 'grid-donuts-2-of-2'),
          swatch_grid(houses, 'grid-swatches')]
for n, p in charts:
    open(f'{OUT}/{n}.html', 'w').write(p)
json.dump([n for n, _ in charts], open(f'{OUT}/grids.json', 'w'))
print([n for n, _ in charts])
