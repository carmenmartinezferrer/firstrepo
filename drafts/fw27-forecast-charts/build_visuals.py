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

PALETTES = {
 'heritage-craft': ('Heritage Craft', [
   ('russet red', '#7B3330', 'dark red: "high" search volume of 35k'),
   ('plum purple', '#583759', 'plum purple: searches up 39% on last year'),
   ('forest green', '#254117', 'forest green: "extreme" search volume of 57k'),
   ('chestnut brown', '#7C533C', 'chestnut brown: 196M views on TikTok')]),
 'sensory-riot': ('Sensory Riot', [
   ('chartreuse', '#C7D344', 'chartreuse: 149M views on TikTok'),
   ('fuchsia', '#FF278A', 'fuchsia: "extreme" search volume of 84k'),
   ('lilac', '#927EC3', 'lilac: "extreme" search volume of 103k'),
   ('cobalt blue', '#4C80FD', 'cobalt blue: searches up 14% on last year')]),
 'veiled-performance': ('Veiled Performance', [
   ('marigold', '#DFAA4F', 'marigold: "extreme" search volume of 126k'),
   ('moss green', '#7E8C53', 'moss green: searches up 23% on last year'),
   ('dove grey', '#838384', 'dove grey: searches up 43% on last year'),
   ('terracotta clay', '#D38377', 'terracotta: searches up 7% on last year')]),
}
STRIPS = {
 'heritage-craft': ('Heritage Craft', [('runway-chanel.png', 'Chanel'), ('runway-ralph-lauren.png', 'Ralph Lauren'), ('runway-acne-studios.png', 'Acne Studios')]),
 'sensory-riot': ('Sensory Riot', [('runway-dries-van-noten.png', 'Dries Van Noten'), ('runway-dolce-gabbana.png', 'Dolce & Gabbana'), ('runway-valentino.png', 'Valentino')]),
 'veiled-performance': ('Veiled Performance', [('runway-jane-wade.png', 'Jane Wade'), ('runway-chloe.png', 'Chloé'), ('runway-lacoste.png', 'Lacoste')]),
}

def page(body, w):
    return (f'<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>body{{margin:0;background:#fff}}'
            f'#card{{width:{w}px;background:#fff;box-sizing:border-box;padding:40px 50px 30px;font-family:{SANS};color:{INK}}}'
            f'h1{{font-family:{SERIF};font-weight:700;font-size:56px;margin:0 0 10px;line-height:1.1}}'
            f'.sub{{font-size:25px;color:{MUTED};margin:0 0 36px}} .src{{font-size:20px;margin-top:34px}}'
            '.row{display:flex;gap:28px} .sw{flex:1} .sq{height:200px;border-radius:2px}'
            f'.nm{{font-size:25px;margin:16px 0 4px}} .hx{{font-size:20px;color:{MUTED};margin:0 0 8px}} .dp{{font-size:20px;line-height:1.3}}'
            '.look{flex:1;position:relative} .look img{width:100%;height:440px;object-fit:cover;object-position:top;display:block}'
            f'.chip{{position:absolute;left:0;bottom:0;background:{PINK};color:#fff;font-size:20px;letter-spacing:1px;text-transform:uppercase;padding:8px 14px}}'
            f'</style></head><body><div id="card">{body}</div></body></html>')

manifest = []
for key, (name, cols) in PALETTES.items():
    sw = ''.join(f'<div class="sw"><div class="sq" style="background:{hx}"></div><div class="nm">{html.escape(n)}</div>'
                 f'<div class="hx">{hx}</div><div class="dp">{html.escape(dp)}</div></div>' for n, hx, dp in cols)
    body = (f'<h1>{name.lower()}, the palette</h1><p class="sub">the four colours Trendalytics names for this aesthetic, hex sampled from the report\'s own swatches, with the one data point it gives each</p>'
            f'<div class="row">{sw}</div><div class="src">Source: Trendalytics, Womenswear Forecast Fall/Winter 2027 (October 2026). Colour names and data points as printed.</div>')
    fn = f'06-palette-{key}'
    open(f'{OUT}/{fn}.html', 'w').write(page(body, 1000)); manifest.append(fn)
for key, (name, looks) in STRIPS.items():
    lk = ''.join(f'<div class="look"><img src="images/{f}"><div class="chip">{html.escape(h)}</div></div>' for f, h in looks)
    body = (f'<h1>{name.lower()}, on the SS27 runway</h1><p class="sub">the three shows Trendalytics names as early indicators for this aesthetic</p>'
            f'<div class="row">{lk}</div><div class="src">Images: runway photographs as reproduced in the Trendalytics FW27 forecast. Houses as named by Trendalytics.</div>')
    fn = f'07-runway-{key}'
    open(f'{OUT}/{fn}.html', 'w').write(page(body, 1000)); manifest.append(fn)
json.dump(manifest, open(f'{OUT}/cards.json', 'w')); print(manifest)
