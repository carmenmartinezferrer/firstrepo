# One 2 x 2 photo grid per colour slide (full-bleed 4:5, 2160 x 2700), four looks from that colour group,
# each cropped to 4:5 around the person (centre taken from the cut-out's bounding box).
# Usage: python3 build_photo_grids.py <scratch dir> <draft dir>
import sys
from PIL import Image
S, D = sys.argv[1], sys.argv[2]
GRIDS = {'1-black': ['l17', 'l14', 'l19', 'l18'], '2-blue-navy': ['l30b', 'l35', 'l15', 'l16'],
         '3-nude-cream-white': ['l13', 'l20', 'l21', 'l01'], '4-brown-burgundy': ['l11', 'l32', 'l45', 'l07'],
         '5-green-gold': ['l12', 'l31', 'l24', 'l43'], '6-everything-else': ['l04', 'l29', 'l22', 'l38']}
def crop(n):
    im = Image.open(f'{S}/src/{n}.png').convert('RGB'); W, H = im.size
    try: bb = Image.open(f'{S}/cut/{n}_full.png').getbbox()
    except FileNotFoundError: bb = (W * .2, 0, W * .8, H)
    cx = (bb[0] + bb[2]) / 2; pw, ph = bb[2] - bb[0], bb[3] - bb[1]
    # window: 4:5, as large as the photo allows, but no wider than needed to hold the person with some air
    h = min(H, W * 5 / 4); w = h * 4 / 5
    need_w = max(pw * 1.15, ph * 1.08 * 4 / 5)
    if need_w < w: w = max(need_w, W * .45 if W > H else need_w); h = w * 5 / 4
    x0 = min(max(cx - w / 2, 0), W - w); cy = (bb[1] + bb[3]) / 2; y0 = min(max(cy - h / 2, 0), H - h)
    return im.crop((int(x0), int(y0), int(x0 + w), int(y0 + h))).resize((1080, 1350), Image.LANCZOS)
for g, ns in GRIDS.items():
    c = Image.new('RGB', (2160, 2700))
    for k, n in enumerate(ns): c.paste(crop(n), ((k % 2) * 1080, (k // 2) * 1350))
    c.save(f'{D}/canva/grid-{g}.jpg', quality=90)
