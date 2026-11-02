"""Pantone-style swatch cards for the Paris SS27 season palette.

One card per solid colour slice of the season Colour mix donut (prints left
out, their hex is a blend, not a colour), largest share first. Writes one
HTML per card plus a grid, rendered to PNG by render_grids.js.
"""
import json, sys, pandas as pd

xlsx, out = sys.argv[1], sys.argv[2]
c = pd.read_excel(xlsx, sheet_name='Colour mix donut')
s = c[(c.Level == 'fashion week') & ~c.Colour.str.contains('print', case=False)]
s = s.sort_values('Looks', ascending=False)
s = s[s['Share pct'] >= 1]

FONTS = ('<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500'
         '&family=Questrial&display=swap" rel="stylesheet">')
CSS = """
body{margin:0;background:#fff;font-family:'Century Gothic','Questrial',sans-serif}
#chart{display:inline-block;padding:40px;background:#fff}
.card{width:300px;background:#fff;box-shadow:0 1px 6px rgba(0,0,0,.14);display:inline-block}
.chip{height:300px}
.info{padding:16px 18px 20px;color:#222}
.tag{font-size:13px;letter-spacing:.14em;color:#555}
.name{font-family:'Playfair Display',serif;font-size:30px;font-weight:500;margin:6px 0 4px}
.hex{font-size:20px;letter-spacing:.06em}
.pct{font-size:15px;color:#555;margin-top:8px}
.grid{display:grid;grid-template-columns:repeat(5,300px);gap:28px}
h1{font-family:'Playfair Display',serif;font-weight:500;font-size:52px;margin:0 0 6px;color:#222}
.sub{font-size:22px;color:#444;margin-bottom:34px}
.src{font-size:16px;color:#555;margin-top:30px}
"""

def card(r):
    name = r.Colour.replace('/', ' / ')
    return (f'<div class="card"><div class="chip" style="background:{r.Hex}"></div>'
            f'<div class="info"><div class="tag">PARIS SS27</div><div class="name">{name}</div>'
            f'<div class="hex">{r.Hex.upper()}</div>'
            f'<div class="pct">{int(r["Share pct"])}% of the Paris palette</div></div></div>')

def page(body):
    return f'<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>{CSS}</style></head><body><div id="chart">{body}</div></body></html>'

names = []
for i, (_, r) in enumerate(s.iterrows(), 1):
    n = f'pantone-{i:02d}-' + r.Colour.lower().replace('/', '-').replace(' ', '-')
    open(f'{out}/{n}.html', 'w').write(page(card(r)))
    names.append(n)
grid = ('<h1>The Paris SS27 palette</h1>'
        '<div class="sub">every solid colour on the Paris runway, with its share of the season palette (% of all colour across every look)</div>'
        '<div class="grid">' + ''.join(card(r) for _, r in s.iterrows()) + '</div>'
        '<div class="src">Source: DFB runway tagging of Paris Fashion Week SS27. Prints are left out, each hex is the blend of that colour\'s shades.</div>')
open(f'{out}/pantone-grid.html', 'w').write(page(grid))
names.append('pantone-grid')
json.dump(names, open(f'{out}/grids.json', 'w'))
print(s[['Colour', 'Hex', 'Share pct']].to_string())
