import sys, glob, os, numpy as np
from PIL import Image
from rembg import new_session
S = sys.argv[1]; s = new_session('u2net_cloth_seg')
for f in sorted(glob.glob(f'{S}/src/*.png')):
    n = os.path.basename(f)[:-4]; im = Image.open(f).convert('RGB')
    ms = s.predict(im)
    m = np.zeros((im.height, im.width), bool)
    for x in ms: m |= np.array(x.convert('L').resize(im.size)) > 128
    Image.fromarray((m * 255).astype(np.uint8)).save(f'{S}/fam/{n}_cloth.png')
