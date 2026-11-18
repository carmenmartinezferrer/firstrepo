"""Search charts for the Chinese jacket piece. Each Google Trends export was
pulled on its own, so every line is indexed to its own peak week (100):
the charts compare timing, never size, and every subtitle says so."""
import csv, datetime, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
PINK, BLACK = "#D6447A", "#111114"
CSS = f"""
@font-face {{ font-family:'DM Serif Display'; src:url('file://{REPO}/reference-articles/DMSerifDisplay-Regular.ttf'); }}
@font-face {{ font-family:'Century Gothic'; src:local('Century Gothic'), url('file://{REPO}/carousel/creative-director-exits/fonts/Questrial.ttf'); }}
body {{ margin:0; background:#fff; }}
.block {{ width:1000px; background:#F7F6F4; padding:38px 44px 34px; box-sizing:border-box; font-family:'Century Gothic',sans-serif; }}
h2 {{ font-family:'DM Serif Display',serif; font-weight:400; font-size:34px; line-height:1.15; margin:0 0 10px; color:#111114; }}
.sub {{ font-size:15px; color:#222; margin:0 0 22px; line-height:1.45; }}
.note {{ font-size:15px; color:#222; font-weight:500; margin:16px 0 0; line-height:1.45; }}
.src {{ font-size:12px; color:#555; margin:10px 0 0; }}
svg {{ width:100%; height:auto; display:block; }}
"""
def load(name):
    with open(os.path.join(HERE, "data", name + ".csv")) as f:
        r = list(csv.reader(f))
    return [(a, int(b)) for a, b in r[1:]]

def chart(series, marks=()):
    """series: list of (label, colour, rows). marks: (series_idx, week_idx, text, dx, dy, anchor)."""
    n = len(series[0][2]); x0, x1, y0, y1 = 50, 890, 50, 330
    xp = lambda i: x0 + i / (n - 1) * (x1 - x0)
    yp = lambda v: y1 - v / 100 * (y1 - y0)
    F = "font-family=\"Century Gothic, sans-serif\""
    out = [f'<svg viewBox="0 0 912 372" xmlns="http://www.w3.org/2000/svg">']
    for v in (0, 50, 100):
        dash = '' if v == 0 else ' stroke-dasharray="2,4"'
        out.append(f'<line x1="{x0}" y1="{yp(v)}" x2="{x1}" y2="{yp(v)}" stroke="#D9D7D2" stroke-width="1"{dash}/>')
        out.append(f'<text x="{x0-9}" y="{yp(v)+4}" text-anchor="end" {F} font-size="13" fill="#222">{v}</text>')
    seen = set()
    for i, (d, _) in enumerate(series[0][2]):
        dt = datetime.datetime.strptime(d, "%Y-%m-%d")
        if (dt.year, dt.month) not in seen:
            seen.add((dt.year, dt.month))
            if i == 0 or dt.day <= 7:
                lab = dt.strftime("%b") + (" " + dt.strftime("%Y") if dt.month == 1 or i == 0 else "")
                if i == 0: continue
                out.append(f'<text x="{xp(i):.1f}" y="{y1+22}" text-anchor="middle" {F} font-size="13" fill="#222">{lab}</text>')
    lx = x0
    for label, col, rows in series:
        out.append(f'<circle cx="{lx+6}" cy="18" r="6" fill="{col}"/><text x="{lx+19}" y="23" {F} font-size="15" font-weight="500" fill="#222">{label}</text>')
        lx += 40 + len(label) * 9
    for label, col, rows in reversed(series):
        pts = " ".join(f"{xp(i):.1f},{yp(v):.1f}" for i, (_, v) in enumerate(rows))
        out.append(f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="{3 if col==PINK else 2.4}" stroke-linejoin="round"/>')
    for si, wi, text, dx, dy, anchor in marks:
        col = series[si][1]; v = series[si][2][wi][1]
        out.append(f'<circle cx="{xp(wi):.1f}" cy="{yp(v):.1f}" r="5" fill="{col}" stroke="#F7F6F4" stroke-width="2"/>')
        out.append(f'<text x="{xp(wi)+dx:.1f}" y="{yp(v)+dy:.1f}" text-anchor="{anchor}" {F} font-size="13" font-weight="500" fill="#222">{text}</text>')
    out.append("</svg>")
    return "\n".join(out)

def idx(rows, date): return [d for d, _ in rows].index(date)

cm, mj, qp, oj, ci = (load(x) for x in ("chinamaxxing", "mandarin_jacket", "qipao", "opera_jacket", "conner_ives"))
UNIT = "Weekly Google searches, worldwide, November 2025 to November 2026. Each line is indexed to its own highest week, which is 100, so the chart compares timing and not size."
SRC = "Source: Google Trends, pulled by The Data Fashion Brief on 18 November 2026."
charts = [
 dict(name="01_meme_then_jacket", title="The meme peaked in February, and the jacket followed seven weeks later",
      sub=UNIT, svg=chart([("mandarin jacket", PINK, mj), ("chinamaxxing", BLACK, cm)],
        [(1, idx(cm, "2026-02-22"), "22 Feb", -10, -2, "end"), (0, idx(mj, "2026-04-12"), "12 Apr", 0, -12, "middle")]),
      note="Searches for chinamaxxing peak in the week of 22 February 2026 and searches for mandarin jacket in the week of 12 April 2026."),
 dict(name="02_lunar_new_year", title="Qipao and opera jacket both peak at Lunar New Year, and qipao stays high all summer",
      sub=UNIT, svg=chart([("qipao", PINK, qp), ("opera jacket", BLACK, oj)],
        [(0, idx(qp, "2026-02-15"), "15 Feb, both terms", -10, 4, "end")]),
      note="Both terms hit their highest week of the year in the week of 15 February 2026."),
 dict(name="03_conner_ives", title="Searches for Conner Ives are at their highest of the year this autumn",
      sub="Weekly Google searches for conner ives, worldwide, November 2025 to November 2026. The line is indexed to its own highest week, which is 100.",
      svg=chart([("conner ives", PINK, ci)],
        [(0, idx(ci, "2026-09-13"), "13 Sep, New York show week", -10, -4, "end"), (0, idx(ci, "2026-10-25"), "25 Oct", -10, 4, "end")]),
      note="The latest four weeks average 64, against 23 in the first four weeks of the period, which is almost three times higher."),
]
os.makedirs(os.path.join(HERE, "html"), exist_ok=True)
for c in charts:
    html = f'<!doctype html><html><head><meta charset="utf-8"><title>{c["title"]}</title><style>{CSS}</style></head><body><div class="block"><h2>{c["title"]}</h2><p class="sub">{c["sub"]}</p>{c["svg"]}<p class="note">{c["note"]}</p><p class="src">{SRC}</p></div></body></html>'
    assert "—" not in html and "–" not in html
    open(os.path.join(HERE, "html", c["name"] + ".html"), "w").write(html)
json.dump([c["name"] for c in charts], open(os.path.join(HERE, "html", "manifest.json"), "w"))
print("built", len(charts))
