"""Overview palette card. Hex codes come from the runway-colour-combos sampling script
(see data/palette.json), never Pantone codes."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
P = json.load(open(os.path.join(HERE, "data", "palette.json")))
CSS = f"""
@font-face {{ font-family:'DM Serif Display'; src:url('file://{REPO}/reference-articles/DMSerifDisplay-Regular.ttf'); }}
@font-face {{ font-family:'Century Gothic'; src:local('Century Gothic'), url('file://{REPO}/carousel/creative-director-exits/fonts/Questrial.ttf'); }}
body {{ margin:0; background:#fff; }}
.block {{ width:1200px; background:#F7F6F4; padding:40px 44px 34px; box-sizing:border-box; font-family:'Century Gothic',sans-serif; color:#222; }}
h2 {{ font-family:'DM Serif Display',serif; font-weight:400; font-size:36px; line-height:1.15; margin:0 0 10px; color:#111114; }}
.sub {{ font-size:15px; margin:0 0 26px; line-height:1.45; }}
.lab {{ font-size:13px; letter-spacing:.14em; text-transform:uppercase; color:#D6447A; margin:22px 0 12px; font-weight:500; }}
.row {{ display:grid; gap:14px; }}
.card {{ background:#fff; box-shadow:0 1px 5px rgba(0,0,0,.12); }}
.chip {{ height:110px; }}
.info {{ padding:10px 12px 12px; }}
.name {{ font-size:15px; font-weight:500; }}
.house {{ font-size:12px; color:#555; margin-top:2px; }}
.hex {{ font-size:13px; letter-spacing:.05em; margin-top:4px; }}
.src {{ font-size:12px; color:#555; margin:20px 0 0; }}
"""
def card(name, hx, house=""):
    h = f'<div class="house">{house}</div>' if house else ""
    return f'<div class="card"><div class="chip" style="background:{hx}"></div><div class="info"><div class="name">{name}</div>{h}<div class="hex">{hx}</div></div></div>'
ci = "".join(card(n, h) for n, h in P["conner_ives"])
ss = "".join(card(c, h, house) for house, c, h in P["ss27"])
title = "Ivory, butter yellow and blossom pink are the colours of the Asian-inspired jacket"
html = f'''<!doctype html><html><head><meta charset="utf-8"><title>{title}</title><style>{CSS}</style></head><body><div class="block">
<h2>{title}</h2>
<p class="sub">Each swatch is a colour sampled from a photo of the piece, shown with its hex code. These are mid-tones as the photo holds them, so runway lighting can make them duller than in real life, and they are not Pantone codes.</p>
<div class="lab">Conner Ives coats, satin, fur and embroidery</div><div class="row" style="grid-template-columns:repeat(9,1fr)">{ci}</div>
<div class="lab">SS27 runways, main garment colours</div><div class="row" style="grid-template-columns:repeat(7,1fr)">{ss}</div>
<p class="src">Source: photos collected by The Data Fashion Brief (Conner Ives) and runway images from FashionUnited, credit Launchmetrics/spotlight (SS27).</p>
</div></body></html>'''
assert "—" not in html and "–" not in html
open(os.path.join(HERE, "html", "04_palette.html"), "w").write(html)
