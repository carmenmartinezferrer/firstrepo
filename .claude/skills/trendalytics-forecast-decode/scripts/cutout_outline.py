"""White-outlined model cutout for the per-aesthetic carousel covers.

Usage: python3 -I cutout_outline.py input.jpg output.png

Cuts the person out with rembg (u2net_human_seg), keeps only the largest
connected blob, fills holes, crops to the figure, and draws a white
outline around it (about 1% of the figure height, minimum 6px), on a
transparent background. Upload the PNG to Canva and drop it into one of
the four cutout slots of the cover (see SKILL.md, per-aesthetic carousel).

Needs: pip install "rembg[cpu]" scipy pillow numpy
"""
import sys
import numpy as np
from PIL import Image
from rembg import remove, new_session
from scipy import ndimage

src, dst = sys.argv[1], sys.argv[2]
session = new_session('u2net_human_seg')
im = Image.open(src).convert('RGB')
if im.width > 1400:
    im = im.resize((1400, int(im.height * 1400 / im.width)))
a = np.array(remove(im, session=session, post_process_mask=True))
m = a[..., 3] > 128
lab, n = ndimage.label(m)
sz = ndimage.sum(m, lab, range(1, n + 1))
keep = ndimage.binary_fill_holes(lab == np.argmax(sz) + 1)
a[..., 3] = np.where(keep, a[..., 3], 0)
res = Image.fromarray(a)
res = res.crop(res.getbbox())
r = max(6, int(res.height * 0.012))
alpha = np.array(res)[..., 3] > 128
dil = ndimage.binary_dilation(alpha, iterations=r)
pad = r + 4
W, H = res.width + 2 * pad, res.height + 2 * pad
outline = np.zeros((H, W, 4), np.uint8)
outline[pad:pad + res.height, pad:pad + res.width][dil] = (255, 255, 255, 255)
out = Image.fromarray(outline)
out.alpha_composite(res, (pad, pad))
out.save(dst)
print(dst, out.size, 'mask share', round(float(m.mean()), 2))
