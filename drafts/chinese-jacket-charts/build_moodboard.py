"""Moodboard for the maximalism point, eight pins from Carmen's Pinterest
board "Asianmaxxing aesthetic" (https://uk.pinterest.com/user_ih0009/asianmaxxing-aesthetic/),
in the DFB white card style. The pins carry no creator credit, so the images
stay out of git (see .gitignore) and need permission or credit before publishing.
Usage: python3 build_moodboard.py && NODE_PATH=$(npm root -g) node \\
  ../../.claude/skills/trendalytics-forecast-decode/scripts/render_cards.js $(pwd)/html $(pwd)"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "html"); os.makedirs(OUT, exist_ok=True)
INK, MUTED = '#222222', '#6B6B6B'
SERIF = "'Playfair Display', Georgia, serif"; SANS = "'Century Gothic', 'Questrial', 'Avenir', sans-serif"
FONTS = '<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Questrial&display=swap" rel="stylesheet">'
PINS = ["04", "05", "13", "18", "15", "17", "07", "12"]
cells = "".join(f'<div class="im"><img src="file://{HERE}/pinterest/pin-{n}.jpg"></div>' for n in PINS)
page = (f'<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>body{{margin:0;background:#fff}}'
        f'#card{{width:1200px;background:#fff;box-sizing:border-box;padding:40px 50px 30px;font-family:{SANS};color:{INK}}}'
        f'h1{{font-family:{SERIF};font-weight:700;font-size:44px;margin:0 0 8px;line-height:1.1}}'
        f'.sub{{font-size:22px;color:{MUTED};margin:0 0 34px}} .src{{font-size:18px;margin-top:26px}}'
        '.g{display:grid;grid-template-columns:repeat(4,1fr);gap:22px} .im{height:380px;overflow:hidden}'
        '.im img{width:100%;height:100%;object-fit:cover;object-position:top}'
        '</style></head><body><div id="card"><h1>satin, jacquard, fur and embroidery, all at once</h1>'
        '<p class="sub">how the Asian-inspired jacket is actually being worn, from my Pinterest board</p>'
        f'<div class="g">{cells}</div>'
        '<div class="src">Images: pins saved to The Data Fashion Brief\'s Pinterest board "Asianmaxxing aesthetic", original creators not credited on the pins</div></div></body></html>')
assert "—" not in page and "–" not in page
open(f"{OUT}/07-asianmaxxing-moodboard.html", "w").write(page)
json.dump(["07-asianmaxxing-moodboard"], open(f"{OUT}/cards.json", "w"))
