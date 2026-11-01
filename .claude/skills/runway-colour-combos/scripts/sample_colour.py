"""Sample a garment's hex code from a cutout, median of the pixels that match.

Usage: python3 -I sample_colour.py <cutout_full.png> x0,y0,x1,y1 hue_lo,hue_hi sat_lo,sat_hi val_lo,val_hi
  Box is in the crop-space image (<name>_full.png from cutout.py).
  Hue in degrees (a negative lo wraps round red, e.g. -20,15), sat/val 0 to 1.
  Black: hue 0,360 sat 0,1 val 0,0.18.  Greys/whites: sat 0,0.12.
Also: python3 -I sample_colour.py <png> patch x,y   (median of a 20px patch,
with its HSV, to sanity check what a filter should be).
Prints the hex and how many pixels matched; under a few hundred means the
filter or box is wrong, look again before trusting it.
"""
import sys, numpy as np, colorsys
from PIL import Image
a = np.array(Image.open(sys.argv[1]).convert('RGBA'))
if sys.argv[2] == 'patch':
    x, y = map(int, sys.argv[3].split(','))
    p = a[y-10:y+10, x-10:x+10, :3].reshape(-1, 3); m = np.median(p, 0).astype(int)
    print('#%02X%02X%02X' % tuple(m), [round(v, 2) for v in colorsys.rgb_to_hsv(*(m / 255))]); sys.exit()
x0, y0, x1, y1 = map(int, sys.argv[2].split(','))
hr = list(map(float, sys.argv[3].split(','))); sr = list(map(float, sys.argv[4].split(','))); vr = list(map(float, sys.argv[5].split(',')))
px = a[y0:y1, x0:x1]; px = px[px[..., 3] > 230][:, :3] / 255.
hsv = np.array([colorsys.rgb_to_hsv(*p) for p in px]); h = hsv[:, 0] * 360
if hr[0] < 0: h = np.where(h > 180, h - 360, h)
sel = (h >= hr[0]) & (h <= hr[1]) & (hsv[:, 1] >= sr[0]) & (hsv[:, 1] <= sr[1]) & (hsv[:, 2] >= vr[0]) & (hsv[:, 2] <= vr[1])
med = (np.median(px[sel], 0) * 255).round().astype(int)
print('#%02X%02X%02X' % tuple(med), 'matched', int(sel.sum()), 'of', len(px))
