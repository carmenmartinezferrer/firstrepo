"""Pantone-style swatch cards for the Colour Combination series.

Two cards per look (the look's two most striking colours, three where a third is clearly there), every line of
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
    ('11-moschino-look-03', 'MOSCHINO SS27', 'Look 3', [('Chocolate Plum', '#53383B'), ('Jade', '#2EBEAC'), ('Sunshine Yellow', '#FAD82F')]),
    ('12-moschino-look-07', 'MOSCHINO SS27', 'Look 7', [('Scarlet', '#D00F2D'), ('Marigold', '#F1A438')]),
    ('13-moschino-look-12', 'MOSCHINO SS27', 'Look 12', [('Rust', '#8F2D20'), ('Lemon Yellow', '#E9D54A'), ('Raspberry', '#E33850')]),
    ('14-moschino-look-29', 'MOSCHINO SS27', 'Look 29', [('Lime', '#9DD156'), ('Oxblood', '#412E31'), ('Cream', '#E3DBCD')]),
    ('15-roberto-cavalli-look-07', 'ROBERTO CAVALLI SS27', 'Look 7', [('Magenta', '#812156'), ('Leopard Gold', '#B19E74')]),
    ('16-bottega-veneta-look-16', 'BOTTEGA VENETA SS27', 'Look 16', [('Violet', '#5A3777'), ('Orchid Pink', '#D5A0B7')]),
    ('17-bottega-veneta-look-17', 'BOTTEGA VENETA SS27', 'Look 17', [('Candy Pink', '#E3BEDA'), ('Butter Yellow', '#E8C796'), ('Sky Blue', '#A6BAE8')]),
    ('18-bottega-veneta-look-18', 'BOTTEGA VENETA SS27', 'Look 18', [('Lavender', '#B49FCC'), ('Cream', '#E2D6CB'), ('Red', '#C12C39')]),
    ('19-saint-laurent-look-06', 'SAINT LAURENT SS27', 'Look 6', [('Gold', '#D6AC59'), ('Honey', '#9A6033')]),
    ('20-roberto-cavalli-look-28', 'ROBERTO CAVALLI SS27', 'Look 28', [('Lilac', '#BBA9C3'), ('Berry', '#6F3844')]),
    ('21-dries-van-noten-look-40', 'DRIES VAN NOTEN SS27', 'Look 40', [('Sage', '#A6AE8F'), ('Chartreuse', '#B6A003'), ('Lilac', '#C394B2')]),
    ('22-dries-van-noten-look-13', 'DRIES VAN NOTEN SS27', 'Look 13', [('Gold', '#CC9E6B'), ('Teal', '#547C78')]),
    ('23-brand-tbc', 'BRAND TBC SS27', 'Look TBC', [('Black', '#131413'), ('Petrol Teal', '#01656A'), ('Off White', '#E1DFD8')]),
    ('24-balenciaga-look-36', 'BALENCIAGA SS27', 'Look 36', [('Tomato Red', '#CD3929'), ('Sky Blue', '#8099CD'), ('Charcoal', '#4B4544')]),
    ('25-balenciaga-look-49', 'BALENCIAGA SS27', 'Look 49', [('Bubblegum Pink', '#F299AE'), ('Khaki', '#BA9463')]),
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
