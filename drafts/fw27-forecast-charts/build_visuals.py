# Palette cards and runway strips for the FW27 forecast edition.
# Hex codes sampled from the swatches on pages 4, 8 and 12 of the Trendalytics PDF
# (rendered at 150dpi, 40px block average at each swatch centre). Data points as printed.
# Usage: python3 build_visuals.py . && NODE_PATH=$(npm root -g) node render_cards.js . .
import html, json, sys
sys.dont_write_bytecode = True
OUT = sys.argv[1]
PINK, INK, MUTED = '#D6447A', '#222222', '#6B6B6B'
FONTS = '<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Questrial&display=swap" rel="stylesheet">'
SERIF = "'Playfair Display', Georgia, serif"
SANS = "'Century Gothic', 'Questrial', 'Avenir', sans-serif"


import math
def _lum(hx):
    r, g, b = (int(hx[i:i+2], 16) / 255 for i in (1, 3, 5))
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)
def donut_svg(items, size=810):
    total = sum(v for _, v, _ in items); R = size / 2; r_in = R * 0.58; cx = cy = R
    pct = [round(100 * v / total) for _, v, _ in items]; pct[0] += 100 - sum(pct)
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" width="{size}" height="{size}">']
    a = -90.0
    for (name, v, hx), p in zip(items, pct):
        span = 360 * p / 100; a0, a1 = a, a + span
        P = lambda r, ang: (cx + r * math.cos(math.radians(ang)), cy + r * math.sin(math.radians(ang)))
        p0, p1, q1, q0 = P(R, a0), P(R, a1), P(r_in, a1), P(r_in, a0)
        large = 1 if span > 180 else 0
        d = f'M{p0[0]:.1f} {p0[1]:.1f} A{R} {R} 0 {large} 1 {p1[0]:.1f} {p1[1]:.1f} L{q1[0]:.1f} {q1[1]:.1f} A{r_in} {r_in} 0 {large} 0 {q0[0]:.1f} {q0[1]:.1f} Z'
        out.append(f'<path d="{d}" fill="{hx}"/>')
        fs = 42 if p >= 15 else (32 if p >= 8 else 24); lx, ly = P(R * 0.79, (a0 + a1) / 2)
        col = '#FFFFFF' if _lum(hx) < 0.55 else '#000000'
        out.append(f'<text x="{lx:.1f}" y="{ly + fs * 0.35:.1f}" text-anchor="middle" font-family="Arimo, Arial, sans-serif" font-size="{fs}" fill="{col}">{p}%</text>')
        a = a1
    out.append('</svg>'); return '\n'.join(out), pct

PALETTES = {
 'heritage-craft': ('Heritage Craft', [
   ('russet red', '#7B3330', ''),
   ('plum purple', '#583759', ''),
   ('forest green', '#254117', ''),
   ('chestnut brown', '#7C533C', '196M views on TikTok')]),
 'sensory-riot': ('Sensory Riot', [
   ('chartreuse', '#C7D344', '149M views on TikTok'),
   ('fuchsia', '#FF278A', ''),
   ('lilac', '#927EC3', ''),
   ('cobalt blue', '#4C80FD', '')]),
 'veiled-performance': ('Veiled Performance', [
   ('marigold', '#DFAA4F', ''),
   ('moss green', '#7E8C53', ''),
   ('dove grey', '#838384', ''),
   ('terracotta clay', '#D38377', '')]),
}
STRIPS = {
 'heritage-craft': ('Heritage Craft', [('runway-chanel.png', 'Chanel'), ('runway-ralph-lauren.png', 'Ralph Lauren'), ('runway-acne-studios.png', 'Acne Studios')]),
 'sensory-riot': ('Sensory Riot', [('runway-dries-van-noten.png', 'Dries Van Noten'), ('runway-dolce-gabbana.png', 'Dolce & Gabbana'), ('runway-valentino.png', 'Valentino')]),
 'veiled-performance': ('Veiled Performance', [('runway-jane-wade.png', 'Jane Wade'), ('runway-chloe.png', 'Chloé'), ('runway-lacoste.png', 'Lacoste')]),
}

def page(body, w):
    return (f'<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>body{{margin:0;background:#fff}}'
            f'#card{{width:{w}px;background:#fff;box-sizing:border-box;padding:40px 50px 30px;font-family:{SANS};color:{INK}}}'
            f'h1{{font-family:{SERIF};font-weight:700;font-size:38px;margin:0 0 8px;line-height:1.1}}'
            f'.sub{{font-size:22px;color:{MUTED};margin:0 0 34px}} .src{{font-size:20px;margin-top:34px}}'
            '.row{display:flex;gap:28px} .sw{flex:1} .sq{height:200px;border-radius:2px}'
            f'.nm{{font-family:{SERIF};font-weight:700;font-size:28px;margin:16px 0 4px}} .hx{{font-size:19px;color:{MUTED};margin:0 0 8px}} .dp{{font-size:21px;line-height:1.3}}'
            '.look{flex:1;position:relative;border-radius:22px;overflow:hidden} .look img{width:100%;height:440px;object-fit:cover;object-position:top;display:block}'
            f'.chip{{position:absolute;left:14px;bottom:14px;background:{PINK};color:#fff;font-size:20px;letter-spacing:1px;text-transform:uppercase;padding:8px 14px;border-radius:12px}}'
            f'</style></head><body><div id="card">{body}</div></body></html>')

manifest = []
for key, (name, cols) in PALETTES.items():
    sw = ''.join(f'<div class="sw"><div class="sq" style="background:{hx}"></div><div class="nm">{html.escape(n)}</div>'
                 f'<div class="hx">{hx}</div><div class="dp">{html.escape(dp)}</div></div>' for n, hx, dp in cols)
    body = (f'<h1>{name.lower()}, the palette</h1><p class="sub">the four colours of this aesthetic</p>'
            f'<div class="row">{sw}</div>')
    fn = f'06-palette-{key}'
    open(f'{OUT}/{fn}.html', 'w').write(page(body, 1000)); manifest.append(fn)
for key, (name, looks) in STRIPS.items():
    lk = ''.join(f'<div class="look"><img src="images/{f}"><div class="chip">{html.escape(h)}</div></div>' for f, h in looks)
    body = (f'<h1>{name.lower()}: what\'s new on the runway</h1><p class="sub">the three SS27 shows named as early indicators of this mood</p>'
            f'<div class="row">{lk}</div>')
    fn = f'07-runway-{key}'
    open(f'{OUT}/{fn}.html', 'w').write(page(body, 1000)); manifest.append(fn)

ITEMS = {
 'heritage-craft': ('Heritage Craft', [('item-mary-jane-pumps.png', 'Mary Jane pumps', '3M views on TikTok'), ('item-jacquard-jacket.png', 'Jacquard jacket', ''), ('item-paisley-scarf.png', 'Paisley scarf', ''), ('item-tailored-suiting.png', 'Tailored suiting', 'slim suits up 133% in market adoption')]),
 'sensory-riot': ('Sensory Riot', [('item-daytime-boa.png', 'Daytime boa', 'fur scarf searches up 30% on last year'), ('item-fringe-skirt.png', 'Fringe skirt', ''), ('item-sculptural-wedges.png', 'Sculptural wedges', ''), ('item-embellished-jeans.png', 'Embellished jeans', 'up 23% in market adoption')]),
 'veiled-performance': ('Veiled Performance', [('item-drawstring-pants.png', 'Drawstring pants', 'up 33% among key influencers'), ('item-nylon-bag.png', 'Nylon bag', 'up 28% in market adoption'), ('item-funnel-neck-jacket.png', 'Funnel neck jacket', 'up 888% among key influencers, base not stated'), ('item-rain-boots.png', 'Rain boots', 'up 87% among key influencers')]),
}
for key, (name, items) in ITEMS.items():
    it = ''.join(f'<div class="sw"><div class="look"><img src="pinterest/items/{f.replace("item-","").replace(".png",".jpg")}" style="height:340px"></div><div class="nm" style="font-size:26px;margin-top:14px">{html.escape(n)}</div><div class="dp" style="font-size:20px;color:{MUTED}">{html.escape(d)}</div></div>' for f, n, d in items)
    body = (f'<h1>{name.lower()}: what\'s new, key items</h1><p class="sub">the one number the forecast gives each piece, as printed, each on its own measure; pictures from my Pinterest board, the closest look to each piece</p>'
            f'<div class="row">{it}</div>')
    fn = f'18-items-{key}'
    open(f'{OUT}/{fn}.html', 'w').write(page(body, 1000)); manifest.append(fn)

# 22. All nine runway looks in one tall picture, one row per mood, from Carmen's Pinterest boards
RUNWAY = {
 'Heritage Craft': [('pinterest/runway/heritage-1.jpg', ''), ('pinterest/runway/heritage-2.jpg', ''), ('pinterest/runway/heritage-3.jpg', '')],
 'Sensory Riot': [('pinterest/runway/sensory-valentino.jpg', 'Valentino'), ('pinterest/runway/sensory-dolce-gabbana.jpg', 'Dolce & Gabbana'), ('pinterest/runway/sensory-prada.jpg', 'Prada')],
 'Veiled Performance': [('pinterest/runway/veiled-lacoste.jpg', 'Lacoste'), ('pinterest/runway/veiled-chloe.jpg', 'Chloé'), ('pinterest/runway/veiled-miu-miu.jpg', 'Miu Miu')],
}
rows = ''
for name, looks in RUNWAY.items():
    lk = ''.join(f'<div class="look"><img src="{f}">' + (f'<div class="chip">{html.escape(h)}</div>' if h else '') + '</div>' for f, h in looks)
    rows += f'<div class="nm" style="font-size:30px;margin:26px 0 12px">{html.escape(name)}</div><div class="row">{lk}</div>'
body = (f'<h1>what\'s new on the runway</h1><p class="sub">SS27 looks that already carry each mood, three per palette</p>{rows}')
open(f'{OUT}/22-runway-all.html', 'w').write(page(body, 1000)); manifest.append('22-runway-all')
vol = [('dove grey', 202, '#838384'), ('marigold', 177, '#DFAA4F'), ('chartreuse', 124, '#C7D344'), ('terracotta', 123, '#D38377'), ('plum purple', 103, '#583759'), ('lilac', 101, '#927EC3'), ('fuchsia', 69, '#FF278A'), ('forest green', 55, '#254117'), ('cobalt blue', 43, '#4C80FD'), ('chestnut brown', 43, '#7C533C'), ('dark red', 37, '#7B3330'), ('moss green', 37, '#7E8C53')]  # search volume, last 3 months, thousands, Carmen's platform export; dove grey=dark grey, plum purple=deep purple, chestnut brown=dark brown, moss green=dark green
dsvg, dpct = donut_svg(vol)
leg = ''.join(f'<div style="display:flex;align-items:center;gap:12px;font-size:23px;margin-bottom:14px"><span style="display:inline-block;width:22px;height:22px;border-radius:50%;background:{hx}"></span><span><b style="font-family:{SERIF};font-size:25px">{n}</b> <span style="color:{MUTED}">{p}% of searches</span></span></div>' for (n, _, hx), p in zip(vol, dpct))
body = (f'<h1>grey first, marigold second</h1><p class="sub">% = each colour\'s share of the combined searches over the last three months, all twelve colours. Dove grey, plum purple, chestnut brown and moss green use the nearest search term (dark grey, deep purple, dark brown, dark green).</p>'
        '<div class="row" style="align-items:center"><div style="flex:0 0 520px">' + dsvg.replace('width="810" height="810"', 'width="520" height="520"') + '</div><div style="flex:1">' + leg + '</div></div>')
open(f'{OUT}/11-colour-search-share.html', 'w').write(page(body, 1000)); manifest.append('11-colour-search-share')
donuts = [('paris/donut-lacoste.png', 'Lacoste'), ('paris/donut-loewe.png', 'Loewe'), ('paris/donut-miu-miu.png', 'Miu Miu'), ('paris/donut-valentino.png', 'Valentino')]
dk = ''.join(f'<div style="flex:1;text-align:center"><img src="{f}" style="width:100%"><div style="font-family:{SERIF};font-style:italic;font-size:30px;margin-top:8px">{html.escape(n)}</div></div>' for f, n in donuts)
body = (f'<h1>the paris houses already wearing fw27</h1><p class="sub">% = share of each house\'s total colour on the Paris SS27 runway, colour mix method</p>'
        f'<div class="row">{dk}</div><div class="src">Source: The Data Fashion Brief runway tagging, Paris Fashion Week SS27, colour mix</div>')
open(f'{OUT}/paris/grid-houses-fw27.html', 'w').write(page(body, 1000).replace('src="paris/', 'src="'))
manifest.append('paris/grid-houses-fw27')
json.dump(manifest, open(f'{OUT}/cards.json', 'w')); print(manifest)
