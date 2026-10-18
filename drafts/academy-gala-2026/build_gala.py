# Academy Museum Gala 2026 colour share: event palette donut + colour-ordered lineup.
# Input: fam.json (per-look top-3 colour families, from the pixel classifier) and
# the per-look family maps (<look>_fam.png) next to it; cutouts in models/.
import sys, json, math, re, html, numpy as np
from PIL import Image
from skimage.color import rgb2lab, lab2rgb
FAMDIR, OUT = sys.argv[1], sys.argv[2]
r = json.load(open(f'{FAMDIR}/fam.json'))
looks = sorted(r)
# event palette: every look weighs the same, average of its top-3 shares
tot = {}
for n in looks:
    for f, p in r[n]['top3'].items(): tot[f] = tot.get(f, 0) + p / len(looks)
fl = {f: math.floor(v) for f, v in tot.items()}
for f in sorted(tot, key=lambda f: -(tot[f] - fl[f]))[:100 - sum(fl.values())]: fl[f] += 1
# family hex = median colour of every pixel classified into that family
VIS = {"black":"#1A1A1A","white & cream":"#EFE8DA","grey & silver":"#A3A6AA","red":"#C8202A","pink":"#E889A6",
       "orange":"#E8743B","yellow & gold":"#D9B34A","beige & nude":"#CDB497","brown":"#6B4128","green":"#9DBE8F",
       "blue & teal":"#3F7F93","purple":"#7B3F99"}
px = {f: [] for f in VIS}
for n in looks:
    a = np.array(Image.open(f'{FAMDIR}/{n}_full.png').convert('RGBA')); bb = Image.fromarray(a).getbbox()
    a = a[bb[1]:bb[3], bb[0]:bb[2]]; v = np.array(Image.open(f'{FAMDIR}/{n}_fam.png').convert('RGB'))
    for f, hx in VIS.items():
        c = np.array([int(hx[i:i+2], 16) for i in (1, 3, 5)]); m = (v == c).all(-1) & (a[..., 3] > 200)
        if f in r[n]['top3'] and m.sum(): px[f].append(a[m][:, :3][::7])
hexes = {}
for f, l in px.items():
    if not l: continue
    lab = rgb2lab(np.concatenate(l)[None] / 255.)[0]; med = np.median(lab, 0)
    rgb = (np.clip(lab2rgb(med[None, None])[0, 0], 0, 1) * 255).round().astype(int); hexes[f] = '#%02X%02X%02X' % tuple(rgb)
pal = sorted([(f, fl[f], hexes[f]) for f in fl if fl[f] > 0], key=lambda x: -x[1])
lead = {n: max(r[n]['top3'], key=r[n]['top3'].get) for n in looks}
json.dump({'palette': pal, 'raw': {f: round(v, 2) for f, v in tot.items()},
           'lead_counts': {f: sum(1 for n in looks if lead[n] == f) for f in fl},
           'looks': {n: r[n]['top3'] for n in looks}}, open(f'{OUT}/gala-colour-data.json', 'w'), indent=1)
# donut, DFB locked spec (same geometry as runway-decode-colour/scripts/build_donuts.py)
src = open('.claude/skills/runway-decode-colour/scripts/build_donuts.py').read()
exec(src[:src.index("c = pd.read_excel")].split('DATA, OUT = sys.argv[1], sys.argv[2]')[1])
svg, total = donut([(f.title(), p, h) for f, p, h in pal])
FONT = '<link href="https://fonts.googleapis.com/css2?family=Arimo&display=swap" rel="stylesheet">'
open(f'{OUT}/donut-academy-gala-2026.html', 'w').write(f'<!doctype html><html><head><meta charset="utf-8">{FONT}<style>html,body{{margin:0;background:transparent}}</style></head><body>{svg}</body></html>')
json.dump([{'name': 'donut-academy-gala-2026', 'house': 'event'}], open(f'{OUT}/manifest.json', 'w'))
# lineup: grouped by each look's lead colour, groups in palette order, biggest share first
order = [f for f, _, _ in pal]
seq = sorted(looks, key=lambda n: (order.index(lead[n]), -r[n]['top3'][lead[n]]))
json.dump(seq, open(f'{OUT}/lineup-order.json', 'w'))
H, BAR, GAP, PER = 520, 16, 18, 11
tiles = []
for n in seq:
    im = Image.open(f'{OUT}/../models/{n}.png').convert('RGBA'); im = im.resize((max(1, im.width * H // im.height), H), Image.LANCZOS)
    w = max(im.width, 60); t = Image.new('RGBA', (w, H + 10 + BAR), (0, 0, 0, 0)); t.alpha_composite(im, ((w - im.width) // 2, 0))
    x = 0
    for f, p in sorted(r[n]['top3'].items(), key=lambda x: -x[1]):
        ww = round(w * p / 100); c = tuple(int(hexes[f][i:i+2], 16) for i in (1, 3, 5)) + (255,)
        t.paste(Image.new('RGBA', (max(ww, 1), BAR), c), (x, H + 10)); x += ww
    tiles.append(t)
rows = [tiles[i:i + PER] for i in range(0, len(tiles), PER)]
W = max(sum(t.width for t in row) + GAP * (len(row) - 1) for row in rows)
canvas = Image.new('RGBA', (W, len(rows) * (H + 10 + BAR) + (len(rows) - 1) * 50), (0, 0, 0, 0))
y = 0
for row in rows:
    x = (W - (sum(t.width for t in row) + GAP * (len(row) - 1))) // 2
    for t in row: canvas.alpha_composite(t, (x, y)); x += t.width + GAP
    y += H + 10 + BAR + 50
canvas.save(f'{OUT}/lineup-by-colour-transparent.png')
bg = Image.new('RGBA', canvas.size, (255, 255, 255, 255)); bg.alpha_composite(canvas); bg.convert('RGB').save(f'{OUT}/lineup-by-colour.png')
# also one strip per row, easier to place in Canva
for i, row in enumerate(rows):
    w = sum(t.width for t in row) + GAP * (len(row) - 1); c = Image.new('RGBA', (w, H + 10 + BAR), (0, 0, 0, 0)); x = 0
    for t in row: c.alpha_composite(t, (x, 0)); x += t.width + GAP
    c.save(f'{OUT}/lineup-row-{i + 1}-transparent.png')
print(pal); print(seq)
