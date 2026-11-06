"""Build the 'creative director exits 2026' carousel: a cover plus one line-chart slide per house.

Usage: python3 build.py <html_out_dir>   then   node render.js <html_out_dir> <png_out_dir>
Data: Google Trends monthly exports in data/ (Carmen's own downloads, 6 Nov 2026).
Every number on a slide is computed from those files, none is typed in by hand except dates from press.
"""
import sys, os, csv, datetime as dt

HERE = os.path.dirname(os.path.abspath(__file__))
PINK, INK, PANEL = "#D6447A", "#222", "#F7F6F4"
LAST_FULL = dt.date(2026, 10, 1)      # November 2026 is a partial month in the exports, so the line stops here
AXIS_END = dt.date(2026, 11, 30)

def d(s): return dt.date.fromisoformat(s)

HOUSES = [
 dict(slug="balenciaga", term="Balenciaga", n=1, exit_txt="5 Nov 2026", start="2021-11-01",
      hire="2025-05-19", hire_lbl="May 2025", exit="2026-11-05", exit_lbl="Nov 2026", peak=("2022-11-01", "Nov 2022: 100"),
      ticks=[2022, 2023, 2024, 2025, 2026],
      title="Balenciaga hired Pierpaolo Piccioli in May 2025 and he left in November 2026",
      body="Searches for the house barely moved in the 18 months in between, averaging {tenure} against {before} in the year before he arrived, and its biggest month was still November 2022, which at 100 was more than double the best month under Piccioli."),
 dict(slug="alexander-mcqueen", term="Alexander McQueen", n=2, exit_txt="15 Oct 2026", start="2021-11-01",
      hire="2023-10-03", hire_lbl="Oct 2023", exit="2026-10-15", exit_lbl="Oct 2026", peak=None,
      ticks=[2022, 2023, 2024, 2025, 2026],
      title="Alexander McQueen hired Seán McGirr in October 2023 and he left in October 2026",
      body="Searches averaged {tenure} during his three years against {before} in the year before, but the line had been sliding since 2022, well before he arrived, so the fall cannot be pinned on him."),
 dict(slug="calvin-klein", term="Calvin Klein", n=3, exit_txt="15 Oct 2026", start="2021-11-01",
      hire="2024-05-30", hire_lbl="May 2024", exit="2026-10-15", exit_lbl="Oct 2026", peak=("2026-05-01", "May 2026: 100"),
      ticks=[2022, 2023, 2024, 2025, 2026],
      title="Calvin Klein hired Veronica Leoni in May 2024 and parted ways with her in October 2026",
      body="Searches averaged {tenure} during her time there against {before} in the year before, but that average is lifted by two spring 2026 months at 97 and 100, and without them it drops to {ex_spike}, slightly below where it started."),
 dict(slug="saint-laurent", term="Saint Laurent", n=4, exit_txt="9 Oct 2026", start="2015-01-01",
      hire="2016-04-01", hire_lbl="Apr 2016", exit="2026-10-09", exit_lbl="Oct 2026", peak=("2026-04-01", "Apr 2026: 100"),
      ticks=[2016, 2018, 2020, 2022, 2024, 2026],
      title="Saint Laurent hired Anthony Vaccarello in April 2016 and he left in October 2026",
      body="Searches for the house averaged {tenure} across his ten and a half years against {before} in the year before he started, and they reached their highest point of all in April 2026, six months before the exit was announced."),
 dict(slug="diesel", term="Diesel", n=5, exit_txt="18 Sep 2026", start="2021-11-01",
      hire=None, hire_lbl=None, exit="2026-09-18", exit_lbl="Sep 2026", peak=("2026-03-01", "Mar 2026: 100"),
      ticks=[2022, 2023, 2024, 2025, 2026],
      title="Diesel hired Glenn Martens in October 2020 and he left in September 2026",
      body="Searches sat around 50 for most of 2024 and then climbed to their highest point of 100 in March 2026, six months before the exit was announced, while Martens carries on at Maison Margiela."),
]

def load(slug):
    rows = list(csv.reader(open(os.path.join(HERE, "data", slug + ".csv"), encoding="utf-8")))[1:]
    return {d(r[0]): int(r[1]) for r in rows}

def mean(v): return sum(v) / len(v)

def stats(h, s):
    """Whole-number averages: the 12 months before the hire month, and hire month up to the month before the exit."""
    if not h["hire"]: return {}
    hm = d(h["hire"]).replace(day=1)
    em = d(h["exit"]).replace(day=1)
    before_start = dt.date(hm.year - 1, hm.month, 1)
    before = [v for t, v in s.items() if before_start <= t < hm]
    ten = [v for t, v in s.items() if hm <= t < em]
    out = dict(before=round(mean(before)), tenure=round(mean(ten)))
    out["ex_spike"] = round(mean([v for t, v in s.items() if hm <= t < em and t not in (dt.date(2026, 4, 1), dt.date(2026, 5, 1))]))
    return out

CSS = f"""
@font-face{{font-family:'DM Serif Display';src:url('file://{HERE}/fonts/DMSerifDisplay-Regular.ttf');}}
@font-face{{font-family:'Questrial';src:url('file://{HERE}/fonts/Questrial.ttf');}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{width:1080px;height:1350px;position:relative;overflow:hidden;font-family:'Century Gothic','Questrial',sans-serif;color:{INK};background:#fff}}
.bar{{position:absolute;left:0;top:0;width:1080px;height:14px;background:{PINK}}}
.kicker{{position:absolute;left:60px;top:62px;font-size:22px;letter-spacing:.16em;text-transform:uppercase;color:{PINK}}}
.title{{position:absolute;left:60px;top:108px;width:960px;font-family:'DM Serif Display',serif;font-size:62px;line-height:1.1;color:#000}}
.body{{position:absolute;left:60px;top:326px;width:960px;font-size:29px;line-height:1.42}}
.panel{{position:absolute;left:60px;top:560px;width:960px;height:640px;background:{PANEL}}}
.note{{position:absolute;left:60px;top:1214px;width:960px;font-size:19px;line-height:1.4}}
.handle{{position:absolute;left:60px;top:1308px;font-size:19px;letter-spacing:.06em;color:{PINK}}}
.page{{position:absolute;right:60px;top:1308px;font-size:19px}}
"""

def page(inner, bg="#fff"):
    return f"<!doctype html><html><head><meta charset='utf-8'><title>DFB creative director exits</title><style>{CSS}body{{background:{bg}}}</style></head><body>{inner}</body></html>"

def chart_svg(h, s):
    W, H = 960, 640
    L, R, T, B = 80, 36, 92, 56
    pw, ph = W - L - R, H - T - B
    t0, t1 = d(h["start"]), AXIS_END
    X = lambda t: L + (t - t0).days / (t1 - t0).days * pw
    Y = lambda v: T + (1 - v / 100) * ph
    o = [f"<svg xmlns='http://www.w3.org/2000/svg' width='{W}' height='{H}' viewBox='0 0 {W} {H}' font-family=\"'Questrial','Century Gothic',sans-serif\">"]
    for v in (0, 50, 100):
        o.append(f"<line x1='{L}' x2='{L+pw}' y1='{Y(v):.1f}' y2='{Y(v):.1f}' stroke='#BDBDBD' stroke-width='1.5' stroke-dasharray='6 6'/>")
        o.append(f"<text x='{L-14}' y='{Y(v)+7:.1f}' font-size='22' fill='{INK}' text-anchor='end'>{v}</text>")
    ex = X(d(h["exit"]))
    hx = X(d(h["hire"])) if h["hire"] else L
    o.append(f"<rect x='{hx:.1f}' y='{T}' width='{ex-hx:.1f}' height='{ph}' fill='{PINK}' fill-opacity='.13'/>")
    pts = [(t, v) for t, v in sorted(s.items()) if d(h["start"]) <= t <= LAST_FULL]
    path = " ".join(f"{'M' if i == 0 else 'L'}{X(t):.1f},{Y(v):.1f}" for i, (t, v) in enumerate(pts))
    o.append(f"<path d='{path}' fill='none' stroke='{PINK}' stroke-width='4.5' stroke-linejoin='round' stroke-linecap='round'/>")
    ly = T - 26
    if h["hire"]:
        o.append(f"<line x1='{hx:.1f}' x2='{hx:.1f}' y1='{T-14}' y2='{T+ph}' stroke='#000' stroke-width='2.5'/>")
        anchor = "start" if hx - L < 190 else "end"
        tx = hx + 10 if anchor == "start" else hx - 10
        o.append(f"<text x='{tx:.1f}' y='{ly}' font-size='23' fill='{INK}' text-anchor='{anchor}'>Hired {h['hire_lbl']}</text>")
    else:
        o.append(f"<text x='{L+4}' y='{ly}' font-size='23' fill='{INK}'>Hired Oct 2020, before this chart starts</text>")
    o.append(f"<line x1='{ex:.1f}' x2='{ex:.1f}' y1='{T-14}' y2='{T+ph}' stroke='#000' stroke-width='2.5'/>")
    o.append(f"<text x='{ex-10:.1f}' y='{ly}' font-size='23' fill='{INK}' text-anchor='end'>Left {h['exit_lbl']}</text>")
    if h["peak"]:
        pt, lbl = d(h["peak"][0]), h["peak"][1]
        px, py = X(pt), Y(s[pt])
        o.append(f"<circle cx='{px:.1f}' cy='{py:.1f}' r='8' fill='{PINK}' stroke='#fff' stroke-width='3'/>")
        right = px < L + pw * 0.5
        halo = '#F3DFE4' if hx <= px <= ex else PANEL   # band colour inside the tenure, panel colour outside
        o.append(f"<text x='{px+(16 if right else -16):.1f}' y='{py+8:.1f}' font-size='22' fill='{INK}' stroke='{halo}' stroke-width='7' paint-order='stroke' text-anchor='{'start' if right else 'end'}'>{lbl}</text>")
    lt, lv = pts[-1]
    o.append(f"<circle cx='{X(lt):.1f}' cy='{Y(lv):.1f}' r='6' fill='{PINK}'/>")
    for y in h["ticks"]:
        x = X(dt.date(y, 1, 1))
        o.append(f"<line x1='{x:.1f}' x2='{x:.1f}' y1='{T+ph}' y2='{T+ph+8}' stroke='{INK}' stroke-width='1.5'/>")
        o.append(f"<text x='{x:.1f}' y='{T+ph+36}' font-size='22' fill='{INK}' text-anchor='middle'>{y}</text>")
    o.append("</svg>")
    return "".join(o)

def slide(h, s, st):
    body = h["body"].format(**st) if st else h["body"]
    note = (f"Google search interest for “{h['term']}”, worldwide, monthly. 100 is the house’s own highest month in the period shown, "
            f"so the lines cannot be compared between houses. The line stops at October 2026 because November is not a full month yet. Source: Google Trends.")
    return page(f"<div class='bar'></div><div class='kicker'>{h['exit_txt']} · exit {h['n']} of 5</div>"
                f"<div class='title'>{h['title']}</div><div class='body'>{body}</div>"
                f"<div class='panel'>{chart_svg(h, s)}</div><div class='note'>{note}</div>"
                f"<div class='handle'>@thedatafashionbrief</div><div class='page'>{h['n']+1} / 6</div>")

COVER_ROWS = [  # newest exit first, same order as the slides
 ("5 Nov", "Balenciaga", "Pierpaolo Piccioli, 18 months"),
 ("15 Oct", "Alexander McQueen", "Seán McGirr, 3 years"),
 ("15 Oct", "Calvin Klein", "Veronica Leoni, over 2 years"),
 ("9 Oct", "Saint Laurent", "Anthony Vaccarello, over 10 years"),
 ("18 Sep", "Diesel", "Glenn Martens, almost 6 years"),
]

def cover():
    rows = "".join(
        f"<div style='position:absolute;left:0;top:{i*118}px;width:960px;height:118px'>"
        f"<div style='position:absolute;left:0;top:14px;width:150px;font-size:26px;color:{PINK};letter-spacing:.04em'>{dte}</div>"
        f"<div style='position:absolute;left:160px;top:27px;width:22px;height:22px;border-radius:50%;background:{PINK};box-shadow:0 0 0 6px #000'></div>"
        f"<div style='position:absolute;left:214px;top:0;font-family:\"DM Serif Display\",serif;font-size:50px;color:#fff'>{house}</div>"
        f"<div style='position:absolute;left:214px;top:62px;font-size:25px;color:#fff'>{who}</div></div>"
        for i, (dte, house, who) in enumerate(COVER_ROWS))
    line = f"<div style='position:absolute;left:170px;top:38px;width:3px;height:{4*118}px;background:{PINK}'></div>"
    inner = (f"<div class='bar'></div><div class='kicker'>Creative director exits · 18 Sep to 5 Nov 2026</div>"
             f"<div style='position:absolute;left:60px;top:112px;width:960px;font-family:\"DM Serif Display\",serif;font-size:104px;line-height:1.04;color:#fff'>5 creative directors left in 7 weeks</div>"
             f"<div style='position:absolute;left:60px;top:392px;width:900px;font-size:30px;line-height:1.42;color:#fff'>Here is where each house’s Google searches went while they were in charge.</div>"
             f"<div style='position:absolute;left:60px;top:560px;width:960px;height:600px'>{line}{rows}</div>"
             f"<div style='position:absolute;left:60px;top:1236px;font-size:26px;color:#fff'>Swipe for the five search lines →</div>"
             f"<div class='handle' style='top:1296px'>@thedatafashionbrief</div><div class='page' style='top:1296px;color:#fff'>1 / 6</div>")
    return page(inner, bg="#000")

if __name__ == "__main__":
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    open(os.path.join(out, "00-cover.html"), "w", encoding="utf-8").write(cover())
    for h in HOUSES:
        s = load(h["slug"]); st = stats(h, s)
        print(h["slug"], st)
        open(os.path.join(out, f"{h['n']:02d}-{h['slug']}.html"), "w", encoding="utf-8").write(slide(h, s, st))
