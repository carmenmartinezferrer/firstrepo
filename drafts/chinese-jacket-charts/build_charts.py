"""Search charts for the Asian-inspired jacket piece, built with the
runway-decode-trends skill's build_search_line_chart.py.
Each Google Trends export was pulled on its own, so every line is indexed to
its own peak week (100): the charts compare timing, never size, and every
subtitle says so."""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(REPO, ".claude", "skills", "runway-decode-trends", "scripts"))
from build_search_line_chart import build_line_chart, load_trends_csv
CSS = f"""
@font-face {{ font-family:'DM Serif Display'; src:url('file://{REPO}/reference-articles/DMSerifDisplay-Regular.ttf'); }}
@font-face {{ font-family:'Century Gothic'; src:local('Century Gothic'), url('file://{REPO}/carousel/creative-director-exits/fonts/Questrial.ttf'); }}
body {{ margin:0; background:#fff; }}
.block {{ width:1000px; background:#F7F6F4; padding:38px 44px 34px; box-sizing:border-box; font-family:'Century Gothic',sans-serif; }}
h2 {{ font-family:'DM Serif Display',serif; font-weight:400; font-size:34px; line-height:1.15; margin:0 0 10px; color:#111114; }}
.sub {{ font-size:15px; color:#222; margin:0 0 22px; line-height:1.45; }}
.note {{ font-size:15px; color:#222; font-weight:500; margin:16px 0 0; line-height:1.45; }}
.src {{ font-size:12px; color:#555; margin:10px 0 0; }}
.matrix-svg {{ width:100%; height:440px; display:block; }}
"""
def load(n): return load_trends_csv(os.path.join(HERE, "data", n + ".csv"), value_col=n.replace("_", " "))
def peak(rows): return max(rows, key=lambda r: r[1])[0]
UNIT = "Weekly Google searches, worldwide, November 2025 to November 2026. Each line is indexed to its own highest week, which is 100, so the chart compares timing and not size."
SRC = "Source: Google Trends, pulled by The Data Fashion Brief on 18 November 2026."
mj, cm, qp, oj, ci = (load(x) for x in ("mandarin_jacket", "chinamaxxing", "qipao", "opera_jacket", "conner_ives"))
specs = [
 ("01_meme_then_jacket", "The meme peaked in February, and the jacket followed seven weeks later", mj, cm, "Mandarin jacket", "Chinamaxxing",
  lambda s: f"Searches for chinamaxxing peak in the week of 22 February 2026 and searches for mandarin jacket in the week of 12 April 2026."),
 ("02_lunar_new_year", "Qipao and opera jacket both peak at Lunar New Year, and qipao stays high all summer", qp, oj, "Qipao", "Opera jacket",
  lambda s: "Both terms hit their highest week of the year in the week of 15 February 2026."),
 ("03_conner_ives", "As the jacket cooled, searches for Conner Ives climbed to their highest of the year", ci, mj, "Conner Ives", "Mandarin jacket",
  lambda s: "Searches for Conner Ives peak in the week of 25 October 2026, after a first jump in the week of 13 September, the week of the New York show."),
]
assert peak(cm) == "2026-02-22" and peak(mj) == "2026-04-12" and peak(qp) == peak(oj) == "2026-02-15" and peak(ci) == "2026-10-25"
os.makedirs(os.path.join(HERE, "html"), exist_ok=True); names = []
for name, title, lead, comp, ln, cn, note in specs:
    svg, stats = build_line_chart(lead, comp, ln, cn)
    html = f'<!doctype html><html><head><meta charset="utf-8"><title>{title}</title><style>{CSS}</style></head><body><div class="block"><h2>{title}</h2><p class="sub">{UNIT}</p>{svg}<p class="note">{note(stats)}</p><p class="src">{SRC}</p></div></body></html>'
    assert "—" not in html and "–" not in html
    open(os.path.join(HERE, "html", name + ".html"), "w").write(html); names.append(name)
json.dump(names, open(os.path.join(HERE, "html", "manifest.json"), "w"))
