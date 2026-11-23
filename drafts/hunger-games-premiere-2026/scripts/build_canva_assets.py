# Canva assets for the premiere colour report: one transparent strip per colour slide
# (cut-outs with their colour bars), cleaned of carpet/backdrop leftovers, plus four cover photos.
# Usage: python3 build_canva_assets.py <scratch dir> <draft dir>
import sys, json, math, numpy as np
from PIL import Image
from skimage.color import rgb2lab
from scipy import ndimage
S, D = sys.argv[1], sys.argv[2]
data = json.load(open(f'{D}/charts/premiere-colour-data.json')); groups = json.load(open(f'{D}/charts/groups.json'))
HEX = {n: h for n, _, h in data['palette']}; r = data['looks']
IMG = {'l06': [('l06', .47, 1)], 'l07': [('l07', 0, .5), ('l08', .5, 1)], 'l27': [('l27', .36, .62), ('l28', .62, 1)], 'l38': [('l38', 0, .5), ('l39', .5, 1)]}
def clean(img):
    a = np.array(Image.open(f'{S}/cut/{img}_full.png').convert('RGBA')); bb = Image.fromarray(a).getbbox()
    a = a[bb[1]:bb[3], bb[0]:bb[2]]; H, W = a.shape[:2]
    lab = rgb2lab(a[..., :3] / 255.); C = np.hypot(lab[..., 1], lab[..., 2]); h = (np.degrees(np.arctan2(lab[..., 2], lab[..., 1])) + 360) % 360
    yy = np.arange(H)[:, None] * np.ones((1, W)); xx = np.ones((H, 1)) * np.arange(W)[None]
    carpet = (yy > .86 * H) & (h > 290) & (h < 335) & (C > 22) & (img not in ('l30', 'l35', 'l34'))         # purple carpet at the feet
    gold = (yy > .93 * H) & (h > 60) & (h < 100) & (C > 30) & (img in ('l24', 'l26', 'l13'))  # gold carpet lettering
    kill = carpet | gold
    if img == 'l35': kill |= (yy < .166 * H) & ((xx < .44 * W) | (xx > .555 * W))   # backdrop lettering above the wings
    a[kill, 3] = 0
    m = a[..., 3] > 128; lb, k = ndimage.label(m)
    if k:
        sz = ndimage.sum(m, lb, range(1, k + 1)); keep = np.isin(lb, [i + 1 for i in range(k) if sz[i] > 0.02 * sz.max()]); a[~keep, 3] = 0
    im = Image.fromarray(a); ppl = IMG.get(img, [(img, 0, 1)])
    im = im.crop((int(ppl[0][1] * im.width), 0, im.width, im.height)); im = im.crop(im.getbbox())
    im.save(f'{D}/models/{img}.png'); return im, ppl
def tile(img, H, BAR):
    a, ppl = clean(img); im = a.resize((max(1, round(a.width * H / a.height)), H), Image.LANCZOS); w = im.width
    t = Image.new('RGBA', (w, H + BAR * 2), (0, 0, 0, 0)); t.alpha_composite(im, (0, 0)); gap = 8 if len(ppl) > 1 else 0
    for k, (n, _, _) in enumerate(ppl):
        pw = (w - gap * (len(ppl) - 1)) // len(ppl); x = k * (pw + gap)
        for f, p in sorted(r[n].items(), key=lambda q: -q[1]):
            ww = round(pw * p / 100); t.paste(Image.new('RGBA', (max(ww, 1), BAR), tuple(int(HEX[f][i:i+2], 16) for i in (1, 3, 5)) + (255,)), (x, H + BAR)); x += ww
    return t
BW, BH, GAP, RG = 1728, 1500, 36, 60     # 2x the 864 x 750 slot on the slide
for g, members in groups.items():
    asp = {}
    for i in members:
        a = Image.open(f'{S}/cut/{i}_full.png'); bb = a.getbbox(); ppl = IMG.get(i, [(i, 0, 1)]); asp[i] = (bb[2] - bb[0]) * (1 - ppl[0][1]) / (bb[3] - bb[1])
    best = None
    for nrows in (1, 2, 3):
        per = math.ceil(len(members) / nrows); rows = [members[k:k + per] for k in range(0, len(members), per)]
        # every row has the same cut-out height h: limited by width of the widest row and by total height
        hw = min((BW - GAP * (len(row) - 1)) / sum(asp[i] for i in row) for row in rows)
        hh = (BH - RG * (len(rows) - 1)) / len(rows) / 1.06
        h = min(hw, hh)
        if not best or h > best[0]: best = (h, rows)
    h, rows = best; H = int(h); BAR = max(10, int(H * .03)); TH = H + 2 * BAR
    c = Image.new('RGBA', (BW, len(rows) * TH + RG * (len(rows) - 1)), (0, 0, 0, 0)); y = 0
    for row in rows:
        ts = [tile(i, H, BAR) for i in row]; x = (BW - (sum(t.width for t in ts) + GAP * (len(ts) - 1))) // 2
        for t in ts: c.alpha_composite(t, (max(x, 0), y)); x += t.width + GAP
        y += TH + RG
    c = c.crop(c.getbbox()); c.save(f'{D}/canva/strip-{g}.png'); print(g, c.size, [len(x) for x in rows])
# cover: four photos cropped to the 540 x 675 quadrant (4:5)
for k, (t, box) in enumerate([('73c5_0', None), ('abe7_0', None), ('5536_0', None), ('7e04_top', None)]):
    im = Image.open(f'{S}/tiles/{t}.png').convert('RGB'); w, hgt = im.size; tw = min(w, hgt * 4 / 5); th = tw * 5 / 4
    x0 = (w - tw) / 2; y0 = min(max(0, hgt * .02), hgt - th); im.crop((int(x0), int(y0), int(x0 + tw), int(y0 + th))).resize((1080, 1350), Image.LANCZOS).save(f'{D}/canva/cover-{k + 1}.jpg', quality=92)
