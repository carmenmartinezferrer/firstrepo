"""Pantone-style swatch cards for Runway Colour Combos.

Usage: python3 build_swatches.py looks.json <html_out_dir>
  then: NODE_PATH=$(npm root -g) node render_swatches.js <html_out_dir> <png_out_dir>
looks.json: [{"slug": "13-moschino-look-12", "house": "MOSCHINO SS27", "look": "Look 12",
              "colours": [["Rust", "#8F2D20"], ["Lemon Yellow", "#E9D54A"]]}, ...]
One card per colour plus a <slug>-pair group card. All text Century Gothic
(Questrial web fallback). Hex codes are photo samples, never call them Pantone codes.
"""
import json, sys
looks, out = json.load(open(sys.argv[1])), sys.argv[2]
FONTS = '<link href="https://fonts.googleapis.com/css2?family=Questrial&display=swap" rel="stylesheet">'
CSS = """
body{margin:0;background:#fff;font-family:'Century Gothic','Questrial',sans-serif}
#chart{display:inline-block;padding:40px;background:#fff}
.card{width:300px;background:#fff;box-shadow:0 1px 6px rgba(0,0,0,.14);display:inline-block;vertical-align:top}
.chip{height:300px}
.info{padding:16px 18px 20px;color:#222}
.tag{font-size:13px;letter-spacing:.14em;color:#555}
.name{font-size:28px;margin:8px 0 4px}
.hex{font-size:20px;letter-spacing:.06em}
.look{font-size:15px;color:#555;margin-top:8px}
.pair{display:flex;gap:28px}
"""
def card(house, look, name, hx):
    return (f'<div class="card"><div class="chip" style="background:{hx}"></div>'
            f'<div class="info"><div class="tag">{house}</div><div class="name">{name}</div>'
            f'<div class="hex">{hx}</div><div class="look">{look}</div></div></div>')
def page(body):
    return f'<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>{CSS}</style></head><body><div id="chart">{body}</div></body></html>'
names = []
for L in looks:
    for i, (name, hx) in enumerate(L['colours'], 1):
        n = f"{L['slug']}-colour-{i}-{name.lower().replace(' ', '-')}"
        open(f'{out}/{n}.html', 'w').write(page(card(L['house'], L['look'], name, hx))); names.append(n)
    n = f"{L['slug']}-pair"
    open(f'{out}/{n}.html', 'w').write(page('<div class="pair">' + ''.join(card(L['house'], L['look'], *c) for c in L['colours']) + '</div>'))
    names.append(n)
json.dump(names, open(f'{out}/swatches.json', 'w'))
