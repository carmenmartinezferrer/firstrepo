# DFB colour-palette donut, locked spec (Carmen, Paris SS27 onward).
# Usage: python3 build_donuts.py <SS27-paris.xlsx> <out_dir>
#   then: NODE_PATH=$(npm root -g) node render_donuts.js <out_dir> <png_dest>
# Source: 'Colour mix donut' tab, whole-number Share pct, largest first.
# Geometry follows the Canva-native recipe: 810 x 810 box, R = 405, inner
# radius 0.58 R, 0 deg = 12 o'clock, clockwise, labels at 0.79 R.
import sys, math, json, html
import pandas as pd

DATA, OUT = sys.argv[1], sys.argv[2]
R, RI, C = 405.0, 0.58 * 405.0, 405.0
LABEL_R = 0.79 * R

def lum(h):
    h = h.lstrip('#'); c = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]

def size(p): return 42 if p >= 15 else 32 if p >= 8 else 24

def fits(p, s):
    return 2 * math.pi * LABEL_R * p / 100 >= 0.6 * s * len(f'{p}%') + 6

def pt(r, t):
    a = math.radians(t)
    return C + r * math.sin(a), C - r * math.cos(a)

def donut(rows):
    """rows: [(name, pct, hex)] largest first, pct whole numbers summing to ~100."""
    rows = [r for r in rows if r[1] > 0]          # a 0% slice has no arc to draw
    total = sum(p for _, p, _ in rows)
    parts, labels, t0 = [], [], 0.0
    for name, p, hx in rows:
        t1 = t0 + 360.0 * p / total
        large = 1 if t1 - t0 > 180 else 0
        (ox0, oy0), (ox1, oy1) = pt(R, t0), pt(R, t1)
        (ix1, iy1), (ix0, iy0) = pt(RI, t1), pt(RI, t0)
        d = (f'M {ox0:.2f} {oy0:.2f} A {R} {R} 0 {large} 1 {ox1:.2f} {oy1:.2f} '
             f'L {ix1:.2f} {iy1:.2f} A {RI:.1f} {RI:.1f} 0 {large} 0 {ix0:.2f} {iy0:.2f} Z')
        stroke = ' stroke="#D0CCC5" stroke-width="1.2"' if lum(hx) > 0.82 else ''
        parts.append(f'<path d="{d}" fill="{hx}"{stroke}><title>{html.escape(name)} {p}%</title></path>')
        s = size(p)
        if not fits(p, s) and p <= 2 and fits(p, 20): s = 20
        if fits(p, s):
            lx, ly = pt(LABEL_R, (t0 + t1) / 2)
            col = '#FFFFFF' if lum(hx) < 0.55 else '#000000'
            labels.append(f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="middle" dominant-baseline="central" '
                          f'font-family="Arimo, Arial, sans-serif" font-size="{s}" fill="{col}">{p}%</text>')
        t0 = t1
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="-2 -2 814 814" width="814" height="814">'
            + ''.join(parts) + ''.join(labels) + '</svg>'), total

c = pd.read_excel(DATA, sheet_name='Colour mix donut')
c['pct'] = c['Share pct'].round().astype(int)
jobs = {'season': c[c.Level == 'fashion week']}
for house, g in c[c.Level == 'house'].groupby('House'):
    jobs[house] = g
FONT = '<link href="https://fonts.googleapis.com/css2?family=Arimo&display=swap" rel="stylesheet">'
manifest, report = [], {}
for name, g in jobs.items():
    g = g.sort_values(['pct', 'Looks'], ascending=False)
    rows = list(zip(g.Colour, g.pct, g.Hex))
    svg, total = donut(rows)
    slug = 'donut-' + name.lower().replace(' ', '-').replace('é', 'e')
    open(f'{OUT}/{slug}.svg', 'w').write(svg)
    open(f'{OUT}/{slug}.html', 'w').write(f'<!doctype html><html><head><meta charset="utf-8">{FONT}'
        f'<style>html,body{{margin:0;background:transparent}}</style></head><body>{svg}</body></html>')
    manifest.append({'name': slug, 'house': name})
    report[name] = {'total': total, 'rows': [(n, int(p)) for n, p, _ in rows]}
json.dump(manifest, open(f'{OUT}/manifest.json', 'w'))
json.dump(report, open(f'{OUT}/report.json', 'w'), ensure_ascii=False, indent=1)
print({k: v['total'] for k, v in report.items()})
