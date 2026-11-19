"""Picture grid of traditional Chinese theatrical jackets and women's robes
from The Met's Open Access collection (public domain), in the DFB white card
style. Titles and dates are the museum's own, from met/met_objects.json.
Usage: python3 build_met_grid.py && NODE_PATH=$(npm root -g) node \\
  ../../.claude/skills/trendalytics-forecast-decode/scripts/render_cards.js $(pwd)/html $(pwd)"""
import html, json, os
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "html"); os.makedirs(OUT, exist_ok=True)
INK, MUTED = '#222222', '#6B6B6B'
SERIF = "'Playfair Display', Georgia, serif"; SANS = "'Century Gothic', 'Questrial', 'Avenir', sans-serif"
FONTS = '<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Questrial&display=swap" rel="stylesheet">'
objs = json.load(open(os.path.join(HERE, "met", "met_objects.json")))
cells = "".join(f'<div class="c"><div class="im"><img src="file://{HERE}/met/{o["objectID"]}.jpg"></div>'
                f'<div class="nm">{html.escape(o["title"])}</div><div class="dt">China, {html.escape(o["objectDate"])}</div></div>' for o in objs)
page = (f'<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>body{{margin:0;background:#fff}}'
        f'#card{{width:1200px;background:#fff;box-sizing:border-box;padding:40px 50px 30px;font-family:{SANS};color:{INK}}}'
        f'h1{{font-family:{SERIF};font-weight:700;font-size:44px;margin:0 0 8px;line-height:1.1}}'
        f'.sub{{font-size:22px;color:{MUTED};margin:0 0 34px}} .src{{font-size:18px;margin-top:26px}}'
        '.g{display:grid;grid-template-columns:repeat(3,1fr);gap:30px 28px} .im{height:262px;background:#fff;display:flex;align-items:center;justify-content:center;overflow:hidden}'
        '.im img{width:100%;height:100%;object-fit:cover}'
        f'.nm{{font-family:{SERIF};font-weight:700;font-size:22px;margin:14px 0 4px;line-height:1.2}} .dt{{font-size:18px;color:{MUTED}}}'
        f'</style></head><body><div id="card"><h1>the originals, from stage jackets to everyday robes</h1>'
        '<p class="sub">Chinese theatrical jackets and women\'s robes, 18th to early 20th century, as catalogued by the museum</p>'
        f'<div class="g">{cells}</div>'
        '<div class="src">Images: The Metropolitan Museum of Art, New York, Open Access (public domain)</div></div></body></html>')
assert "—" not in page and "–" not in page
open(f"{OUT}/06-traditional-chinese-dress-met.html", "w").write(page)
json.dump(["06-traditional-chinese-dress-met"], open(f"{OUT}/cards.json", "w"))
