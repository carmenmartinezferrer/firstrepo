"""Pantone-style swatch cards for the Colour Combination series.

Two cards per look (the look's two most striking colours), every line of
text in Century Gothic (Questrial as the web fallback when Century Gothic
isn't installed). Hex codes are sampled from the runway photo itself, the
median of each garment's pixels, so they are photo colours, not official
Pantone matches. Rendered to PNG by render_swatches.js.
"""
import json, sys

out = sys.argv[1]
LOOKS = [
    ('01-tory-burch-look-01', 'TORY BURCH SS27', 'Look 1', [('Teal Green', '#0A7C7F'), ('Turquoise', '#32B1E2')]),
    ('02-tory-burch-look-15', 'TORY BURCH SS27', 'Look 15', [('Violet', '#342476'), ('Tomato Red', '#D7423F')]),
    ('03-conner-ives-look-07', 'CONNER IVES SS27', 'Look 7', [('Lime', '#AFCB3C'), ('Black', '#19181A')]),
    ('04-conner-ives-look-08', 'CONNER IVES SS27', 'Look 8', [('Lavender', '#9E8CBE'), ('Poppy Red', '#E82B3C')]),
    ('05-conner-ives-look-14', 'CONNER IVES SS27', 'Look 14', [('Aqua', '#ADDEDC'), ('Cherry Red', '#EB052C')]),
    ('06-burberry-look-01', 'BURBERRY SS27', 'Look 1', [('Dusty Rose', '#B57571'), ('Stone Grey', '#A5958A')]),
    ('07-jil-sander-look-41', 'JIL SANDER SS27', 'Look 41', [('Powder Blue', '#BECDD3'), ('Ivory', '#DBDBCE')]),
    ('08-jil-sander-look-55', 'JIL SANDER SS27', 'Look 55', [('Khaki', '#8D836F'), ('Bubblegum Pink', '#D57690')]),
    ('09-jil-sander-look-60', 'JIL SANDER SS27', 'Look 60', [('Butter Yellow', '#DCD3A4'), ('Dove Grey', '#B3B5AE')]),
    ('10-gucci-look-06', 'GUCCI SS27', 'Look 6', [('Sage Green', '#818F68'), ('Black', '#161715')]),
]
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
for slug, house, look, cols in LOOKS:
    for i, (name, hx) in enumerate(cols, 1):
        n = f'{slug}-colour-{i}-{name.lower().replace(" ", "-")}'
        open(f'{out}/{n}.html', 'w').write(page(card(house, look, name, hx)))
        names.append(n)
    n = f'{slug}-pair'
    open(f'{out}/{n}.html', 'w').write(page('<div class="pair">' + ''.join(card(house, look, *c) for c in cols) + '</div>'))
    names.append(n)
json.dump(names, open(f'{out}/swatches.json', 'w'))
