"""Remove the background from Vogue Runway app screenshots, keep only the model.

Usage: python3 -I cutout.py <out_dir> <model> <screenshot> [<screenshot> ...]
  model: isnet-general-use (default choice, keeps bags and props)
         u2net_human_seg   (use when other models or audience sit right behind,
                            or a pale garment blends into a pale floor)

Crops the phone UI away first (photo band between the header and the
LOOK n/N bar, found by scanning for the first and last rows that are not
flat white or flat black), keeps only the largest connected shape, fills
holes, writes <name>.png (tight bbox, transparent) and a magenta-background
contact sheet check.jpg to eyeball before using anything.
Models live in ~/.u2net (download from the rembg GitHub releases if missing).
"""
import sys, os, numpy as np
from PIL import Image
from rembg import remove, new_session
from scipy import ndimage

def photo_band(im):
    # app chrome rows are perfectly flat (pure white or pure black); photo
    # rows always carry some noise, even a pale floor or a black runway
    a = np.asarray(im.convert('L')).astype(int)
    flat = (a.max(axis=1) - a.min(axis=1)) <= 3
    best, start = (0, 0), None
    for y, f in enumerate(list(flat) + [True]):
        if not f and start is None:
            start = y
        elif f and start is not None:
            if y - start > best[1] - best[0]:
                best = (start, y - 1)
            start = None
    return best

def largest(a):
    m = a[..., 3] > 128
    lab, n = ndimage.label(m)
    if n == 0:
        return a
    sz = ndimage.sum(m, lab, range(1, n + 1))
    a[..., 3] = np.where(ndimage.binary_fill_holes(lab == np.argmax(sz) + 1), a[..., 3], 0)
    return a

out, model, files = sys.argv[1], sys.argv[2], sys.argv[3:]
os.makedirs(out, exist_ok=True)
s = new_session(model)
prev = []
for f in files:
    im = Image.open(f).convert('RGB')
    y0, y1 = photo_band(im)
    crop = im.crop((0, y0, im.width, y1 + 1))
    a = largest(np.array(remove(crop, session=s, post_process_mask=True)))
    res = Image.fromarray(a)
    name = os.path.splitext(os.path.basename(f))[0]
    res.save(f'{out}/{name}_full.png')            # crop-space copy, for coordinate fixes
    res.crop(res.getbbox()).save(f'{out}/{name}.png')
    bg = Image.new('RGBA', res.size, (255, 0, 255, 255)); bg.alpha_composite(res)
    prev.append(bg.convert('RGB').resize((res.width // 2, res.height // 2)))
W = sum(p.width + 10 for p in prev); H = max(p.height for p in prev)
c = Image.new('RGB', (W, H), 'white'); x = 0
for p in prev:
    c.paste(p, (x, 0)); x += p.width + 10
c.save(f'{out}/check.jpg')
print('wrote', len(files), 'cutouts and', f'{out}/check.jpg')
