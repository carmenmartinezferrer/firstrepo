"""Substack cover for the Asian-inspired jacket piece, 1456 x 1048.
Image: Theatrical jacket with grapevines, China, 18th century, The Met Open
Access (public domain), met/69006.jpg.
Usage: python3 build_cover.py && node render_cover.js"""
import os
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
page = f'''<!doctype html><html><head><meta charset="utf-8"><title>Cover</title>
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Questrial&display=swap" rel="stylesheet">
<style>
body{{margin:0;background:#fff}}
#card{{width:1456px;height:1048px;background:#fff;position:relative;overflow:hidden;font-family:'Century Gothic','Questrial',sans-serif;color:#1a1a1a}}
.txt{{position:absolute;left:70px;top:44px;right:70px}}
.k{{font-size:22px;letter-spacing:.2em;color:#D6447A;text-transform:uppercase;margin-bottom:20px}}
h1{{font-family:'DM Serif Display',serif;font-weight:400;font-size:82px;line-height:1.04;margin:0}}
h1 em{{color:#D6447A;font-style:italic}}
.im{{position:absolute;left:0;right:0;bottom:0;height:630px;overflow:hidden}}
.im img{{width:100%;height:100%;object-fit:cover;object-position:50% 46%}}
.cap{{position:absolute;right:22px;bottom:14px;font-size:15px;color:#fff;text-shadow:0 0 6px rgba(0,0,0,.55)}}
</style></head><body><div id="card">
<div class="txt"><div class="k">The Data Fashion Brief</div>
<h1>The jacket you'll keep seeing<br>in <em>2027</em> is probably in a<br><em>vintage shop</em> near you</h1></div>
<div class="im"><img src="file://{HERE}/met/69006.jpg"><div class="cap">Theatrical jacket, China, 18th century. The Met, public domain</div></div>
</div></body></html>'''
assert "—" not in page and "–" not in page
os.makedirs(os.path.join(HERE, "html"), exist_ok=True)
open(os.path.join(HERE, "html", "00-cover.html"), "w").write(page)
