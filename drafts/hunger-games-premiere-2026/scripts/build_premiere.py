# Hunger Games: Sunrise on the Reaping premiere (New York) colour share:
# event palette donut + cut-outs grouped by lead colour, each with its colour bar.
# Usage: python3 build_premiere.py <scratch dir with cut/ and km/km.json> <draft dir>
import sys, json, math, html, numpy as np
from PIL import Image
S, D = sys.argv[1], sys.argv[2]
r = {n: v['top3'] for n, v in json.load(open(f'{S}/km/km.json')).items()}
NAME = {'K': 'black', 'BL': 'blue & navy', 'BE': 'beige & nude', 'W': 'white & cream', 'BR': 'brown', 'GR': 'green',
        'G': 'yellow & gold', 'U': 'burgundy', 'P': 'pink', 'S': 'grey & silver', 'PU': 'purple', 'R': 'red'}
# display hex per family, picked from the looks themselves (thumbnail medians come out too muddy to read on a chart)
HEX = {'K': '#1A1A1A', 'BL': '#1F2466', 'BE': '#D8BFA8', 'W': '#EFE8DA', 'BR': '#5A3A2A', 'GR': '#5E7F3A',
       'G': '#D9B062', 'U': '#5A1F2B', 'P': '#E38AA6', 'S': '#A3A6AA', 'PU': '#A18EB1', 'R': '#C9565C'}
looks = sorted(r); tot = {}
for n in looks:
    for f, p in r[n].items(): tot[f] = tot.get(f, 0) + p / len(looks)
fl = {f: math.floor(v) for f, v in tot.items()}
for f in sorted(tot, key=lambda f: -(tot[f] - fl[f]))[:100 - sum(fl.values())]: fl[f] += 1
pal = sorted([(f, fl[f]) for f in fl], key=lambda x: -tot[x[0]])
lead = {n: max(r[n], key=r[n].get) for n in looks}
json.dump({'looks_measured': len(looks), 'palette': [(NAME[f], p, HEX[f]) for f, p in pal], 'raw': {NAME[f]: round(v, 2) for f, v in tot.items()},
           'lead_counts': {NAME[f]: sum(1 for n in looks if lead[n] == f) for f in fl},
           'looks': {n: {NAME[f]: p for f, p in r[n].items()} for n in looks}}, open(f'{D}/charts/premiere-colour-data.json', 'w'), indent=1)
src = open('.claude/skills/runway-decode-colour/scripts/build_donuts.py').read()
exec(src[:src.index("c = pd.read_excel")].split('DATA, OUT = sys.argv[1], sys.argv[2]')[1])
svg, total = donut([(NAME[f].title(), p, HEX[f]) for f, p in pal])
FONT = '<link href="https://fonts.googleapis.com/css2?family=Arimo&display=swap" rel="stylesheet">'
open(f'{D}/charts/donut-hunger-games-premiere.html', 'w').write(f'<!doctype html><html><head><meta charset="utf-8">{FONT}<style>html,body{{margin:0;background:transparent}}</style></head><body>{svg}</body></html>')
# cut-out images: one per photo; a photo with two measured people carries both bars side by side
IMG = {'l06': [('l06', .47, 1)], 'l07': [('l07', 0, .5), ('l08', .5, 1)], 'l27': [('l27', .36, .62), ('l28', .62, 1)], 'l38': [('l38', 0, .5), ('l39', .5, 1)]}
GROUPS = [('1-black', ['K']), ('2-blue-navy', ['BL']), ('3-nude-cream-white', ['BE', 'W']), ('4-brown-burgundy', ['BR', 'U']),
          ('5-green-gold', ['GR', 'G']), ('6-everything-else', ['P', 'S', 'PU', 'R'])]
H, BAR = 640, 18
def tile(img):
    a = Image.open(f'{S}/cut/{img}_full.png').convert('RGBA'); a = a.crop(a.getbbox()); ppl = IMG.get(img, [(img, 0, 1)])
    a = a.crop((int(ppl[0][1] * a.width), 0, a.width, a.height)); a.save(f'{D}/models/{img}.png')
    im = a.resize((max(1, a.width * H // a.height), H), Image.LANCZOS); w = im.width
    t = Image.new('RGBA', (w, H + 12 + BAR), (0, 0, 0, 0)); t.alpha_composite(im, (0, 0)); x = 0
    for k, (n, _, _) in enumerate(ppl):
        pw = w // len(ppl) - (6 if len(ppl) > 1 else 0); xx = x
        for f, p in sorted(r[n].items(), key=lambda q: -q[1]):
            ww = round(pw * p / 100); t.paste(Image.new('RGBA', (max(ww, 1), BAR), tuple(int(HEX[f][i:i+2], 16) for i in (1, 3, 5)) + (255,)), (xx, H + 12)); xx += ww
        x += w // len(ppl) + (6 if len(ppl) > 1 else 0)
    return t
imgs = sorted({n if n not in ('l08', 'l28', 'l39') else {'l08': 'l07', 'l28': 'l27', 'l39': 'l38'}[n] for n in looks})
tiles = {i: tile(i) for i in imgs}
order = [f for f, _ in pal]; out = {}
for g, fams in GROUPS:
    members = sorted([i for i in imgs if lead[i] in fams], key=lambda i: (order.index(lead[i]), -r[i][lead[i]]))
    out[g] = members
    for i in members: tiles[i].save(f'{D}/charts/tile-{i}.png')
    per = math.ceil(len(members) / (2 if len(members) > 5 else 1)); rows = [members[k:k + per] for k in range(0, len(members), per)]
    W = max(sum(tiles[i].width for i in row) + 24 * (len(row) - 1) for row in rows); TH = H + 12 + BAR
    c = Image.new('RGBA', (W, len(rows) * TH + (len(rows) - 1) * 50), (255, 255, 255, 255)); y = 0
    for row in rows:
        x = (W - (sum(tiles[i].width for i in row) + 24 * (len(row) - 1))) // 2
        for i in row: c.alpha_composite(tiles[i], (x, y)); x += tiles[i].width + 24
        y += TH + 50
    c.convert('RGB').save(f'{D}/charts/group-{g}.png')
json.dump(out, open(f'{D}/charts/groups.json', 'w'), indent=1)
print([(NAME[f], p) for f, p in pal]); print({g: len(m) for g, m in out.items()}, sum(len(m) for m in out.values()), 'photos')
