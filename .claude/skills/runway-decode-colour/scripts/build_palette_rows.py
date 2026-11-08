# Palette swatch rows: one row per palette (or mood, or season), its colours as solid blocks
# in the house-by-house swatch grid style, the number printed inside each block.
# Carmen asked for exactly this on the FW27 colour edition: "the 3 colours in this style,
# 3 colours in one line", meaning the three forecast palettes, one line each.
# Usage: python3 build_palette_rows.py <rows.json> <out_dir>
#   then: NODE_PATH=$(npm root -g) node render_grids.js <out_dir> <png_dest>
# rows.json:
# {"name": "13-palette-rows", "title": "...", "subtitle": "...", "source": "..." or "",
#  "value_fmt": "+{v}%", "sort": true,
#  "rows": [{"label": "Heritage Craft", "colours": [["russet red", "#7B3330", 50], ...]}, ...]}
# The number is whatever the row measures (growth, share), the subtitle must say which in
# plain words. No decimals, no dashes, no house or palette counts in title or subtitle.
import sys, json, html
sys.dont_write_bytecode = True
SPEC, OUT = sys.argv[1], sys.argv[2]
spec = json.load(open(SPEC))
INK, MUTED = '#222222', '#6B6B6B'
SERIF = "'Playfair Display', Georgia, serif"
SANS = "'Century Gothic', 'Questrial', sans-serif"
FONTS = ('<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,500'
         '&family=Questrial&family=Arimo&display=swap" rel="stylesheet">')

def lum(h):
    h = h.lstrip('#'); c = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]

ncols = max(len(r['colours']) for r in spec['rows'])
fmt = spec.get('value_fmt', '{v}%')
rows = ''
for r in spec['rows']:
    cols = sorted(r['colours'], key=lambda c: -c[2]) if spec.get('sort', True) else r['colours']
    blocks = ''
    for name, hx, v in cols:
        tc = '#FFFFFF' if lum(hx) < 0.55 else '#000000'
        edge = 'box-shadow:inset 0 0 0 1.2px #D0CCC5;' if lum(hx) > 0.82 else ''
        blocks += (f'<div style="background:{hx};{edge}height:150px;display:flex;flex-direction:column;justify-content:flex-end;'
                   f'padding:0 0 14px 16px;font-family:Arimo,Arial,sans-serif;color:{tc}">'
                   f'<div style="font-size:32px;line-height:1">{html.escape(fmt.format(v=round(v)))}</div>'
                   f'<div style="font-size:20px;opacity:.92;margin-top:8px">{html.escape(name.lower())}</div></div>')
    blocks += ''.join('<div></div>' for _ in range(ncols - len(cols)))
    rows += f'<div class="name" style="font-size:34px;align-self:center">{html.escape(r["label"])}</div>{blocks}'
src = f'<div class="src">{html.escape(spec["source"])}</div>' if spec.get('source') else ''
page = (f'<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>'
        f'body{{margin:0;background:#fff}} #chart{{width:1600px;padding:56px 60px 40px;box-sizing:border-box;background:#fff;color:{INK}}}'
        f'h1{{font-family:{SERIF};font-weight:700;font-size:58px;margin:0;line-height:1.1}}'
        f'.sub{{font-family:{SANS};font-size:26px;color:{MUTED};margin:14px 0 44px}}'
        f'.src{{font-family:{SANS};font-size:20px;margin-top:40px}}'
        f'.name{{font-family:{SERIF};font-style:italic;font-weight:500;color:{INK}}}'
        f'</style></head><body><div id="chart"><h1>{html.escape(spec["title"])}</h1><div class="sub">{html.escape(spec["subtitle"])}</div>'
        f'<div style="display:grid;grid-template-columns:330px repeat({ncols},1fr);gap:12px 8px">{rows}</div>{src}</div></body></html>')
open(f'{OUT}/{spec["name"]}.html', 'w').write(page)
json.dump([spec['name']], open(f'{OUT}/grids.json', 'w'))
print(spec['name'])
