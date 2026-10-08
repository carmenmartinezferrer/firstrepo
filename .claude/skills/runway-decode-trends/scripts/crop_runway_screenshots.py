"""Cut the runway photo out of phone screenshots of a runway app.

Drops the status bar, the house/season header, the LOOK n/N bar and the
next look peeking in below, keeping only the main photo at full width so
the whole model stays in frame head to toe.

Usage: python3 crop_runway_screenshots.py <in_dir> <out_dir>
Works on every .jpg/.png in <in_dir>, writes same-named .jpg to <out_dir>.
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image

src, dst = Path(sys.argv[1]), Path(sys.argv[2])
dst.mkdir(parents=True, exist_ok=True)
for f in sorted(p for p in src.iterdir() if p.suffix.lower() in {".jpg", ".jpeg", ".png"}):
    im = Image.open(f).convert("RGB")
    a = np.asarray(im).astype(int)
    # UI rows are almost entirely white, photo rows aren't
    photo = (a.min(axis=2) > 240).mean(axis=1) < 0.6
    best, start = (0, 0, 0), None
    for y, p in enumerate(list(photo) + [False]):
        if p and start is None:
            start = y
        if not p and start is not None:
            if y - start > best[0]:
                best = (y - start, start, y)
            start = None
    _, top, bottom = best  # longest run = the main photo
    # trim 3px all round to lose any anti-aliased UI edge
    im.crop((3, top + 3, im.width - 3, bottom - 3)).save(dst / f"{f.stem}.jpg", quality=95)
    print(f.name, "->", (top, bottom))
