import numpy as np, json, sys, glob, os
from PIL import Image, ImageDraw
from skimage.color import rgb2lab, lab2rgb
from scipy.cluster.vq import kmeans2
S = sys.argv[1]; K = 5
CFG = json.load(open(f'{S}/cfg.json'))
PEOPLE = {'l06': [('l06', .47, 1)], 'l07': [('l07', 0, .5), ('l08', .5, 1)], 'l27': [('l27', .36, .62), ('l28', .62, 1)],
          'l38': [('l38', 0, .5), ('l39', .5, 1)]}
res = {}; sheets = []; PIX = {}; NAMES = json.load(open(f'{S}/names.json'))
for f in sorted(glob.glob(f'{S}/cut/*_full.png')):
    img = os.path.basename(f)[:3]
    a0 = np.array(Image.open(f).convert('RGBA')); cl0 = np.array(Image.open(f'{S}/fam/{img}_cloth.png')) > 128
    bb = Image.fromarray(a0).getbbox(); a = a0[bb[1]:bb[3], bb[0]:bb[2]]; cl = cl0[bb[1]:bb[3], bb[0]:bb[2]]
    lab = rgb2lab(a[..., :3] / 255.); H, W = a.shape[:2]
    L, A, B = lab[..., 0], lab[..., 1], lab[..., 2]; C = np.hypot(A, B); hh = (np.degrees(np.arctan2(B, A)) + 360) % 360
    for n, x0, x1 in PEOPLE.get(img, [(img, 0, 1)]):
        c = CFG.get(n, {})
        m = a[..., 3] > 200; xs = np.zeros_like(m); xs[:, int(x0 * W):int(x1 * W)] = True; m = m & xs
        mode = c.get('mode', 'cloth')
        if mode == 'cloth': use = m & cl
        elif mode == 'all': use = m.copy()
        else:
            band = np.zeros_like(m); band[int(.03 * H):int(.09 * H)] = True
            sk = m & band & (A > 6) & (B > 8) & (L > 25) & (L < 85)
            skin = np.median(lab[sk], 0) if sk.sum() > 50 else np.array([60, 15, 20])
            d = np.linalg.norm(lab - skin, axis=2)
            skinlike = (hh >= 40) & (hh < 78) & (C >= 14) & (C <= 50) & (L >= 28) & (L <= 88)
            if mode == 'nude': skinlike = d < c.get('tol', 10)
            use = m & (d >= c.get('tol', 10)) & ~skinlike
        use[:int(c.get('ytop', .12 if mode != 'cloth' else 0) * H)] = False
        use[int(c.get('ybot', 1) * H):] = False
        pts = lab[use]
        np.random.seed(0); cen, lbl = kmeans2(pts, K, minit='++', seed=0)
        cnt = np.bincount(lbl, minlength=K) / len(lbl) * 100
        rgb = (np.clip(lab2rgb(cen[None])[0], 0, 1) * 255).round().astype(int)
        hx = ['#%02X%02X%02X' % tuple(r) for r in rgb]
        res[n] = {'clusters': [{'i': int(i), 'share': round(float(cnt[i]), 1), 'hex': hx[i], 'lab': cen[i].round(0).tolist()} for i in np.argsort(-cnt)], 'cover': round(float(use.sum() / max(m.sum(), 1)), 2)}
        order = list(np.argsort(-cnt)); nm = NAMES[n]; famap = np.full((H, W), '', dtype=object); idxm = np.full((H, W), -1); idxm[use] = lbl
        yy = np.arange(H)[:, None] * np.ones((1, W))
        for j, i in enumerate(order):
            v = nm[j]
            if not v: continue
            if isinstance(v, list):
                famap[(idxm == i) & (yy < v[2] * H)] = v[0]; famap[(idxm == i) & (yy >= v[2] * H)] = v[1]
            else: famap[idxm == i] = v
        tot = (famap != '').sum(); sh = {k: float((famap == k).sum() / tot * 100) for k in set(famap[famap != ''])}
        sh3 = {k: v for k, v in sorted(sh.items(), key=lambda x: -x[1])[:3] if v >= 5}; t3 = sum(sh3.values())
        res[n]['top3'] = {k: round(v / t3 * 100, 1) for k, v in sh3.items()}
        for k in sh3: PIX.setdefault(k, []).append(a[famap == k][:, :3][::5])
        vis = np.full((H, W, 3), 255, np.uint8); vis[m] = (255, 0, 255); idx = np.zeros((H, W), int); idx[use] = lbl; 
        for i in range(K): vis[use & (idx == i)] = rgb[i]
        sw = Image.new('RGB', (90, H), 'white'); d = ImageDraw.Draw(sw); y = 0
        for j, i in enumerate(np.argsort(-cnt)):
            hgt = H // K; d.rectangle((0, y, 90, y + hgt - 4), fill=tuple(int(v) for v in rgb[i])); d.text((4, y + 4), f'{j}:{cnt[i]:.0f}', fill='white' if cen[i][0] < 55 else 'black'); y += hgt
        x0p, x1p = int(x0 * W), int(x1 * W)
        pair = Image.new('RGB', (2 * (x1p - x0p) + 90, H), (0, 200, 0)); cu = Image.fromarray(a).crop((x0p, 0, x1p, H)); pair.paste(cu, (0, 0), cu); pair.paste(Image.fromarray(vis).crop((x0p, 0, x1p, H)), (x1p - x0p, 0)); pair.paste(sw, (2 * (x1p - x0p), 0))
        pair = pair.resize((max(1, pair.width * 320 // H), 320)); ImageDraw.Draw(pair).text((3, 3), n, fill='yellow'); sheets.append(pair)
json.dump(res, open(f'{S}/km/km.json', 'w'), indent=1)
hexes = {}
for k, l in PIX.items():
    med = np.median(rgb2lab(np.concatenate(l)[None] / 255.)[0], 0); r_ = (np.clip(lab2rgb(med[None, None])[0, 0], 0, 1) * 255).round().astype(int); hexes[k] = '#%02X%02X%02X' % tuple(r_)
json.dump(hexes, open(f'{S}/km/hexes.json', 'w'))
tot = {}
for n in res:
    for k, v in res[n]['top3'].items(): tot[k] = tot.get(k, 0) + v / len(res)
print(len(res), 'looks'); print(sorted(tot.items(), key=lambda x: -x[1])); print(hexes)
rows, row, x = [], [], 0
for p in sheets:
    if x + p.width > 1950: rows.append(row); row, x = [], 0
    row.append(p); x += p.width + 6
rows.append(row)
for s in range(0, len(rows), 3):
    R = rows[s:s + 3]; cs = Image.new('RGB', (1950, 326 * len(R)), 'white')
    for j, r in enumerate(R):
        x = 0
        for p in r: cs.paste(p, (x, j * 326)); x += p.width + 6
    cs.save(f'{S}/km/sheet{s // 3}.jpg', quality=88)
for n, r in res.items(): print(n, r['top3'])
