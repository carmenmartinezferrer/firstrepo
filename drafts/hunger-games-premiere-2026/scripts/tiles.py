import sys, glob, os, numpy as np, json
from PIL import Image, ImageDraw
from scipy import ndimage
U, OUT = sys.argv[1], sys.argv[2]
meta = {}; thumbs = []
for f in sorted(glob.glob(f'{U}/*-image.png')):
    k = os.path.basename(f)[:4]
    im = Image.open(f).convert('RGB'); a = np.asarray(im).astype(int)
    # gutters / page background: near-uniform light grey or white
    bg = (np.abs(a - a.mean(-1, keepdims=True)).max(-1) < 4) & (a.mean(-1) > 236)
    fg = ~bg
    fg = ndimage.binary_opening(fg, np.ones((9, 9)))
    lab, n = ndimage.label(fg)
    i = 0
    for sl in ndimage.find_objects(lab):
        y0, y1, x0, x1 = sl[0].start, sl[0].stop, sl[1].start, sl[1].stop
        h, w = y1 - y0, x1 - x0
        if h < 300 or w < 200 or y0 < 150: continue
        fill = (lab[sl] > 0).mean()
        if fill < 0.8: continue
        t = im.crop((x0, y0, x1, y1)); name = f'{k}_{i}'; i += 1
        t.save(f'{OUT}/{name}.png'); meta[name] = [x0, y0, x1, y1]
        th = t.resize((max(1, t.width * 300 // t.height), 300)) if t.height > t.width else t.resize((300, max(1, t.height * 300 // t.width)))
        c = Image.new('RGB', (max(th.width, 110), 330), 'white'); c.paste(th.crop((0, 0, th.width, 300)), (0, 30)); ImageDraw.Draw(c).text((2, 8), f'{name} {w}x{h}', fill='black')
        thumbs.append(c)
json.dump(meta, open(f'{OUT}/meta.json', 'w'))
# contact sheets
rows, row, x = [], [], 0
for t in thumbs:
    if x + t.width > 1900: rows.append(row); row, x = [], 0
    row.append(t); x += t.width + 8
rows.append(row)
per = 3
for s in range(0, len(rows), per):
    R = rows[s:s + per]; c = Image.new('RGB', (1900, 334 * len(R)), 'white')
    for j, r in enumerate(R):
        x = 0
        for t in r: c.paste(t, (x, j * 334)); x += t.width + 8
    c.save(f'{OUT}/sheet{s // per}.jpg', quality=85)
print(len(thumbs), 'tiles', len(rows), 'rows')
