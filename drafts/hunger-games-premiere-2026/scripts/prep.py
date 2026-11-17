import sys, json
from PIL import Image
S = sys.argv[1]
# name: (tile, crop box or None)
L = {
 'l01': ('0d25_2', None), 'l02': ('22af_0', None), 'l03': ('22af_1', None), 'l04': ('22af_2', None),
 'l05': ('22af_8', None), 'l06': ('22af_3', None),  # couple, right person measured
 'l07': ('22af_4', None),  # couple fur: split
 'l09': ('22af_6', None), 'l10': ('22af_7', None), 'l11': ('3283_0', None), 'l12': ('3919_0', None),
 'l13': ('5536_0', None), 'l14': ('3c80_0', (250, 0, 1224, 816)), 'l15': ('3c80_1', None), 'l16': ('3c80_2', None),
 'l17': ('4aa7_0', None), 'l18': ('4e8d_0', (300, 0, 950, 816)), 'l19': ('4e8d_top', (0, 0, 600, 750)),
 'l20': ('5518_0', None), 'l21': ('5518_1', None), 'l22': ('5518_2', (300, 0, 1000, 816)),
 'l23': ('7334_0', None), 'l24': ('7334_1', None), 'l25': ('7334_2', None), 'l26': ('7334_3', None),
 'l27': ('7334_4', None),  # trio: woman + pinstripe man measured
 'l29': ('73c5_0', None), 'l30': ('abe7_0', None), 'l31': ('7e04_top', None), 'l32': ('83d9_0', None),
 'l33': ('83d9_2', None), 'l34': ('83d9_3', (300, 0, 1224, 874)), 'l35': ('bb45_1', None),
 'l36': ('d127_0', None), 'l37': ('d127_1', None), 'l38': ('d127_3', None), 'l40': ('d127_4', None),
 'l41': ('d127_5', None), 'l42': ('d127_6', None), 'l43': ('d127_7', None), 'l44': ('d127_8', None),
 'l45': ('e364_1', None),
}
for n, (t, box) in L.items():
    im = Image.open(f'{S}/tiles/{t}.png').convert('RGB')
    if box: im = im.crop(box)
    if im.height < 1100:  # upscale small thumbnails so the matting model has more to work with
        k = 1100 / im.height; im = im.resize((round(im.width * k), 1100), Image.LANCZOS)
    im.save(f'{S}/src/{n}.png')
