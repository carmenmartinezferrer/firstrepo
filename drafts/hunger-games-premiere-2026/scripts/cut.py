import sys, os, glob, numpy as np
from PIL import Image
from rembg import remove, new_session
from scipy import ndimage
S, model = sys.argv[1], sys.argv[2]
names = sys.argv[3:] or [os.path.basename(f)[:-4] for f in sorted(glob.glob(f'{S}/src/*.png'))]
s = new_session(model); prev = []
for n in names:
    im = Image.open(f'{S}/src/{n}.png').convert('RGB')
    a = np.array(remove(im, session=s, post_process_mask=True))
    m = a[..., 3] > 128; lab, k = ndimage.label(m)
    if k:
        sz = ndimage.sum(m, lab, range(1, k + 1)); keep = np.isin(lab, [i + 1 for i in range(k) if sz[i] > 0.04 * sz.max()])
        a[..., 3] = np.where(keep, a[..., 3], 0)
    Image.fromarray(a).save(f'{S}/cut/{n}_full.png')
    bg = Image.new('RGBA', im.size, (0, 255, 0, 255)); bg.alpha_composite(Image.fromarray(a))
    prev.append((n, bg.convert('RGB').resize((im.width * 330 // im.height, 330))))
for i in range(0, len(prev), 16):
    P = prev[i:i + 16]; c = Image.new('RGB', (sum(p.width + 6 for _, p in P), 330), 'white'); x = 0
    for _, p in P: c.paste(p, (x, 0)); x += p.width + 6
    c.save(f'{S}/cut/check_{model[:5]}_{i // 16}.jpg', quality=85); print([n for n, _ in P])
