# Usage: python3 build_charts.py <SS27-paris.xlsx> <out_dir>  (writes .svg + .html per chart)
#        NODE_PATH=$(npm root -g) node render_png.js <out_dir> <png_dest>  (2x PNGs, Google Fonts)
import sys, html, json
sys.dont_write_bytecode = True
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '.claude', 'skills', 'runway-decode-trends', 'scripts'))
import pandas as pd
from build_matrix_svg import build_matrix

DATA = sys.argv[1]; OUT = sys.argv[2]
x = pd.read_excel(DATA, sheet_name=None)
t = x['Trends']; fw = t[t.Level == 'fashion week']; hs = t[t.Level == 'house']
TOTAL_HOUSES = int(x['Overview'].query('Level=="fashion week"').Houses.iloc[0])

PINK, DARK, INK, MUTED = '#D6447A', '#3A3A3A', '#222222', '#6B6B6B'
SERIF = "'Playfair Display', Georgia, serif"
SANS = "'Century Gothic', 'Questrial', 'Avenir', sans-serif"
W = 1000

def fw_share(cat, val):
    r = fw[(fw.Category == cat) & (fw.Value == val)]
    return float(r['Share pct'].iloc[0])

def fw_houses_pct(cat, val):
    r = fw[(fw.Category == cat) & (fw.Value == val)]
    return 100 * int(r.Houses.iloc[0]) / TOTAL_HOUSES

def wrap(label, n=14):
    # break on spaces, and also after '/' or '-' so 'boxy/oversized' can wrap
    import re
    parts = re.findall(r'[^\s/-]+[/-]?|\s+', label)
    toks, lines, cur = [], [], ''
    for t in parts:
        if t.isspace(): toks.append(' ')
        else: toks.append(t)
    for t in toks:
        if t == ' ':
            cur += ' '; continue
        if cur.strip() and len(cur.rstrip() + ('' if cur.endswith(('/', '-')) else ' ') + t) > n:
            lines.append(cur.strip()); cur = t
        else:
            cur = cur + t
    lines.append(cur.strip())
    return lines

def bar_chart(name, title, subtitle, items, source, fmt=lambda v: f'{round(v)}%', highlight=0):
    """items: list of (label, value). One bar in pink (index `highlight`), rest dark."""
    n = len(items)
    W = max(1000, 100 + n * 150)  # wider canvas for many bars so labels never touch
    top, plot_h, left, right = 175, 360, 50, 50
    base = top + plot_h
    slot = min((W - left - right) / n, 165)
    x0 = (W - slot * n) / 2
    bw = min(150, slot * 0.84)
    vmax = max(v for _, v in items)
    wn = max(8, int(slot / 12.5))
    vs = min(42, round(slot * 0.34))
    label_lines = max(len(wrap(l, wn)) for l, _ in items)
    h = base + 46 + label_lines * 31 + 80
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}" height="{h}">',
         f'<rect width="{W}" height="{h}" fill="#FFFFFF"/>',
         f'<text x="{left}" y="78" font-family="{SERIF}" font-weight="700" font-size="56" fill="{INK}">{html.escape(title)}</text>',
         f'<text x="{left}" y="124" font-family="{SANS}" font-size="25" fill="{MUTED}">{html.escape(subtitle)}</text>']
    for i, (lab, v) in enumerate(items):
        cx = x0 + slot * (i + 0.5)
        bh = (v / vmax) * (plot_h - 70)
        col = PINK if i == highlight else DARK
        p.append(f'<rect x="{cx-bw/2:.1f}" y="{base-bh:.1f}" width="{bw:.1f}" height="{bh:.1f}" fill="{col}"/>')
        p.append(f'<text x="{cx:.1f}" y="{base-bh-14:.1f}" text-anchor="middle" font-family="{SANS}" font-size="{vs}" fill="{INK}">{html.escape(fmt(v))}</text>')
        for j, line in enumerate(wrap(lab, wn)):
            p.append(f'<text x="{cx:.1f}" y="{base+44+j*31}" text-anchor="middle" font-family="{SANS}" font-size="25" fill="{INK}">{html.escape(line)}</text>')
    p.append(f'<line x1="{x0-10:.1f}" y1="{base}" x2="{x0+slot*n+10:.1f}" y2="{base}" stroke="#BDBDBD" stroke-width="1.5"/>')
    p.append(f'<text x="{left-10}" y="{h-30}" font-family="{SANS}" font-size="20" fill="{INK}">{html.escape(source)}</text>')
    p.append('</svg>')
    return name, '\n'.join(p), h

SRC = 'Source: The Data Fashion Brief runway tagging, Paris Fashion Week SS27'
charts = []

# 1. Materials, share of looks by material family
fams = [('tailoring wool', 'wool'), ('silk & satin', 'silk & satin'), ('cotton & linen', 'cotton & linen'),
        ('knit & jersey', 'knit & jersey'), ('sheer & airy', 'sheer & airy'), ('leather & skins', 'leather & skins')]
charts.append(bar_chart('01-materials-share-of-looks', 'wool runs paris',
    '% of all Paris looks that include each material',
    [(lab, fw_share('material family', v)) for v, lab in fams], SRC + ', share of looks'))

# 2. Wool by weave
weaves = [('wool suiting', 'suiting wool'), ('tweed', 'tweed'), ('wool crepe', 'wool crepe'), ('bouclé', 'bouclé')]
charts.append(bar_chart('02-wool-by-weave', 'wool, by weave',
    '% of all Paris looks that include each type of wool',
    [(lab, fw_share('material', v)) for v, lab in weaves], SRC + ', share of looks'))

# 3. Silhouettes, share of houses
sil = [('skirt: pencil skirt', 'pencil skirt'), ('trouser: straight', 'straight trouser'), ('trouser: wide-leg', 'wide-leg trouser'),
       ('dress: slip dress', 'slip dress'), ('coat: trench', 'trench coat'), ('shorts: bermuda', 'bermuda shorts'), ('jacket: bomber', 'bomber jacket')]
charts.append(bar_chart('03-silhouettes-share-of-houses', 'the pencil skirt reached every house',
    '% of houses that showed each piece at least once',
    [(lab, fw_houses_pct('garment', v)) for v, lab in sil], SRC + ', share of houses'))

# 4. Smaller silhouettes, share of houses
small = [('skirt: pleated skirt', 'pleated skirt'), ('skirt: tiered/ruffled skirt', 'tiered skirt'), ('jacket: biker jacket', 'biker jacket'),
         ('top: corset/bustier', 'corset'), ('dress: halter dress', 'halter dress'), ('shorts: hot pants', 'hot pants'),
         ('skirt: bubble/puffball skirt', 'bubble skirt'), ('trouser: cargo', 'cargo trouser')]
charts.append(bar_chart('04-smaller-silhouettes', 'the smaller silhouettes',
    '% of houses that showed each piece at least once',
    [(lab, fw_houses_pct('garment', v)) for v, lab in small], SRC + ', share of houses'))

def hbar_chart(name, title, subtitle, items, source, fmt=lambda v: f'{round(v)}%', highlight=0):
    """Instagram carousel version: 1080 x 1350 (4:5), horizontal bars, big type."""
    W, H = 1080, 1350
    left, right = 64, 64
    top = 300                      # first bar row starts here
    foot = 96                      # space for the source line
    n = len(items)
    row = (H - top - foot) / n
    bh = row * 0.62
    label_w = 330                  # label column, right-aligned to the bars
    x0 = left + label_w + 24
    vmax = max(v for _, v in items)
    bar_max = W - right - x0 - 110 # leave room for the value after the bar
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
         f'<rect width="{W}" height="{H}" fill="#FFFFFF"/>',
         f'<text x="{left}" y="120" font-family="{SERIF}" font-weight="700" font-size="76" fill="{INK}">{html.escape(title)}</text>']
    for j, line in enumerate(wrap(subtitle, 56)):
        p.append(f'<text x="{left}" y="{180 + j*40}" font-family="{SANS}" font-size="32" fill="{MUTED}">{html.escape(line)}</text>')
    for i, (lab, v) in enumerate(items):
        cy = top + row * (i + 0.5)
        w = max(4, v / vmax * bar_max)
        col = PINK if i == highlight else DARK
        p.append(f'<rect x="{x0}" y="{cy - bh/2:.1f}" width="{w:.1f}" height="{bh:.1f}" fill="{col}"/>')
        p.append(f'<text x="{x0 + w + 16:.1f}" y="{cy:.1f}" dominant-baseline="central" font-family="{SANS}" font-size="40" fill="{INK}">{html.escape(fmt(v))}</text>')
        lines = wrap(lab, 16)
        for j, line in enumerate(lines):
            ly = cy + (j - (len(lines) - 1) / 2) * 36
            p.append(f'<text x="{x0 - 20}" y="{ly:.1f}" text-anchor="end" dominant-baseline="central" font-family="{SANS}" font-size="33" fill="{INK}">{html.escape(line)}</text>')
    p.append(f'<line x1="{x0}" y1="{top - 10}" x2="{x0}" y2="{H - foot + 6}" stroke="#BDBDBD" stroke-width="2"/>')
    for j, line in enumerate(wrap(source, 62)):
        p.append(f'<text x="{left}" y="{H - 52 + j*28}" font-family="{SANS}" font-size="22" fill="{INK}">{html.escape(line)}</text>')
    p.append('</svg>')
    return name, '\n'.join(p), H

# Ranked sections (Carmen, Paris SS27): top 10 + next 5, by share of all looks
def ranked(cat, skip=()):
    d = fw[(fw.Category == cat) & (~fw.Value.isin(skip))].sort_values('Looks', ascending=False)
    return [(v, float(sh)) for v, sh in zip(d.Value, d['Share pct'])]
def clean(v):
    # 'trouser: straight' -> 'straight trouser', keep the noun so the label says what the piece is
    if ': ' not in v: return v
    piece, typ = v.split(': ', 1)
    special = {'coat: trench': 'trench coat', 'jacket: bomber': 'bomber jacket', 'top: polo': 'polo shirt'}
    if v in special: return special[v]
    if piece in ('trouser', 'shorts') and piece not in typ: return f'{typ} {piece}'
    return typ
mats = ranked('material', skip=('other',))
gars = ranked('garment', skip=('skirt: other', 'top: other', 'shorts: other', 'knitwear: other'))
shps = ranked('silhouette')
LOOKS = SRC + ', share of looks'
charts.append(bar_chart('10-top-materials', 'top 10 materials',
    '% of all Paris looks that include each material', [(clean(v), x) for v, x in mats[:10]], LOOKS))
charts.append(bar_chart('11-next-materials', 'the next five materials',
    '% of all Paris looks that include each material', [(clean(v), x) for v, x in mats[10:15]], LOOKS))
charts.append(bar_chart('12-top-garments', 'top 10 pieces',
    '% of all Paris looks that include each piece', [(clean(v), x) for v, x in gars[:10]], LOOKS))
charts.append(bar_chart('13-next-garments', 'the next five pieces',
    '% of all Paris looks that include each piece', [(clean(v), x) for v, x in gars[10:15]], LOOKS))
charts.append(bar_chart('14-top-shapes', 'top 10 shapes',
    '% of all Paris looks with each overall silhouette', [(clean(v), x) for v, x in shps[:10]], LOOKS))
charts.append(hbar_chart('20-insta-top-materials', 'top 10 materials',
    '% of all Paris looks that include each material', [(clean(v), x) for v, x in mats[:10]], LOOKS))
charts.append(hbar_chart('21-insta-top-pieces', 'top 10 pieces',
    '% of all Paris looks that include each piece', [(clean(v), x) for v, x in gars[:10]], LOOKS))
charts.append(hbar_chart('22-insta-top-shapes', 'top 10 shapes',
    '% of all Paris looks with each overall silhouette', [(clean(v), x) for v, x in shps[:10]], LOOKS))
print('materials', mats[:15]); print('garments', gars[:15]); print('shapes', shps)

# 5. Over-index pairings that crossed houses
o = x['Over-index']
def idx(cat, val, on):
    r = o[(o.Category == cat) & (o.Value == val) & (o['Sits on'] == on)]
    return float(r.Index.iloc[0]) / 100
pairs = [('wool crepe shift dress', idx('material', 'wool crepe', 'dress: shift dress')),
         ('tulle column dress', idx('material', 'tulle', 'dress: column dress')),
         ('crochet knit top', idx('material', 'crochet', 'knitwear: knit top')),
         ('aqua pencil skirt', idx('colour shade', 'aqua', 'skirt: pencil skirt')),
         ('croc leather pencil skirt', idx('material', 'croc/embossed leather', 'skirt: pencil skirt')),
         ('silk satin corset', idx('material', 'silk satin', 'top: corset/bustier'))]
pairs.sort(key=lambda kv: -kv[1])
charts.append(bar_chart('05-unexpected-pairings', "the pairings I didn't see coming",
    'how many times more often than normal each pairing appears (18x = 18 times)',
    pairs, SRC + ', over-index vs the season mix', fmt=lambda v: f'{round(v)}x',
    highlight=[l for l, _ in pairs].index('wool crepe shift dress')))

# 6. Pink by house vs season (colour mix)
c = x['Colour mix donut']
pk = c[(c.Colour == 'Pink')]
season = float(pk[pk.Level == 'fashion week']['Share pct'].iloc[0])
houses = pk[pk.Level == 'house'].sort_values('Share pct', ascending=False)
items = [(r.House, float(r['Share pct'])) for r in houses.itertuples() if r._9 >= 7] if False else \
        [(r.House, float(r['Share pct'])) for _, r in houses.iterrows() if float(r['Share pct']) >= 7]
items.append(('season average', season))
charts.append(bar_chart('06-pink-by-house', 'where the pink actually lives',
    "% of each house's colour palette that is pink, vs the season average",
    items, SRC + ', colour mix', highlight=len(items) - 1))

# 7. Matrix, restyled on white
vals = ['skirt: pencil skirt', 'trouser: wide-leg', 'dress: slip dress', 'coat: trench', 'shorts: bermuda', 'jacket: bomber']
d = hs[(hs.Category == 'garment') & (hs.Value.isin(vals))].pivot_table(index='House', columns='Value', values='Share pct', fill_value=0)
align = d[vals].mean(axis=1).to_dict()
ov = x['Overview'].query('Level=="house"').set_index('House')
colour = (100 - ov['Neutral pct mix']).astype(float).to_dict()
import statistics as st
svg_m, groups = build_matrix(align, colour, align_thresh=6.3, colour_thresh=st.median(colour.values()), label_overrides={'Lanvin': (8, 16, 'start')})
inner = svg_m.split('>', 1)[1].rsplit('</svg>', 1)[0]
inner = inner.replace('Century Gothic, sans-serif', "Century Gothic, Questrial, sans-serif")
import re
for old, new in [('SEASON-LED, COLOUR-FORWARD', 'TRENDY &amp; COLOURFUL'),
                 ('INDEPENDENT, COLOUR-FORWARD', 'OWN PATH &amp; COLOURFUL'),
                 ('SEASON-LED, NEUTRAL', 'TRENDY &amp; NEUTRAL'),
                 ('INDEPENDENT, NEUTRAL', 'OWN PATH &amp; NEUTRAL'),
                 ('Low alignment', 'Less trendy'), ('High alignment', 'More trendy'),
                 ('High colour', 'More colour'), ('Low colour', 'More neutral')]:
    inner = inner.replace('>' + old + '<', '>' + new + '<')
assert 'OWN PATH &amp; COLOURFUL' in inner
inner = re.sub(r'font-size="(\d+)"', lambda m: f'font-size="{round(int(m.group(1))*1.3)}"', inner)
inner = inner.replace('dy="15"', 'dy="19"')
mh = 820
msvg = '\n'.join([f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {mh}" width="{W}" height="{mh}">',
    f'<rect width="{W}" height="{mh}" fill="#FFFFFF"/>',
    f'<text x="50" y="78" font-family="{SERIF}" font-weight="700" font-size="56" fill="{INK}">trendiness vs colour</text>',
    f'<text x="50" y="124" font-family="{SANS}" font-size="25" fill="{MUTED}">across: trendiness (% of looks in the six key pieces), up: % of palette in colour</text>',
    f'<g transform="translate(110,165) scale(1.15)">{inner}</g>',
    f'<text x="40" y="{mh-30}" font-family="{SANS}" font-size="20" fill="{INK}">{html.escape(SRC)}</text>',
    '</svg>'])
charts.append(('07-alignment-matrix', msvg, mh))

FONTS = '<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,500;0,700;1,500&family=Questrial&display=swap" rel="stylesheet">'
manifest = []
for name, svg, h in charts:
    open(f'{OUT}/{name}.svg', 'w').write(svg)
    page = f'<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>body{{margin:0;background:#fff}}</style></head><body>{svg}</body></html>'
    open(f'{OUT}/{name}.html', 'w').write(page)
    manifest.append({'name': name, 'h': h})
json.dump(manifest, open(f'{OUT}/manifest.json', 'w'))
print(groups)
print([(n, ) for n, _, _ in charts])
print('pink items', items)
