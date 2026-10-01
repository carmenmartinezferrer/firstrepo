#!/usr/bin/env python3
"""DFB catwalk charts: locked donut spec, cross-brand bars, and a decode sanity check.

  python dfb_charts.py check  decode.json
  python dfb_charts.py canva  decode.json
  python dfb_charts.py canva-donut decode.json
  python dfb_charts.py donut  decode.json --field palette --out palette.png [--square]
  python dfb_charts.py bars   tracker.json --out midi.png [--white]

decode.json follows examples/saint-laurent-ss27.json. tracker.json is
{"title": "...", "items": [{"label": "Prada", "pct": 82, "hex": "#..."(optional)}]}.
"""
import argparse
import json
import math
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import font_manager  # noqa: E402

SKILL_DIR = Path(__file__).resolve().parent.parent
FONT_PATH = SKILL_DIR / "assets" / "fonts" / "DMSerifDisplay-Regular.ttf"

PINK = "#D6447A"
INK = "#1a1a1a"
OUTLINE = "#D0CCC5"
# Neutral ramp for categories that have no real colour (silhouettes).
NEUTRALS = ["#111111", "#3A3A3A", "#5E5E5E", "#8A8A8A", "#B0ADA8",
            "#D0CCC5", "#E8E5E0", "#F5F3EF", "#2B2B2B", "#747474"]


def serif():
    if FONT_PATH.exists():
        font_manager.fontManager.addfont(str(FONT_PATH))
        return font_manager.FontProperties(fname=str(FONT_PATH))
    print(f"warning: {FONT_PATH} missing, falling back to default serif", file=sys.stderr)
    return font_manager.FontProperties(family="serif")


def luminance(hex_colour):
    """WCAG relative luminance, 0 (black) to 1 (white)."""
    h = hex_colour.lstrip("#")
    rgb = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def label_size(pct):
    if pct >= 15:
        return 42
    if pct >= 8:
        return 32
    return 24  # small wedges stay readable (Carmen: "small but not super small")


def colours_for(items):
    return [it.get("hex") or NEUTRALS[i % len(NEUTRALS)] for i, it in enumerate(items)]


def donut(items, out, square=False):
    """Locked DFB donut spec — see references/house-style.md."""
    font = serif()
    pcts = [it["pct"] for it in items]
    cols = colours_for(items)

    fig, ax = plt.subplots(figsize=(9, 9))
    fig.patch.set_alpha(0)
    wedges, _ = ax.pie(
        pcts, colors=cols, startangle=90, counterclock=False,
        wedgeprops={"width": 0.42, "edgecolor": "none"},
    )
    for w, col, pct in zip(wedges, cols, pcts):
        if luminance(col) > 0.82:
            w.set_edgecolor(OUTLINE)
            w.set_linewidth(1.2)
        ang = math.radians((w.theta1 + w.theta2) / 2)
        x, y = 0.79 * math.cos(ang), 0.79 * math.sin(ang)
        ax.text(x, y, f"{pct:g}%", ha="center", va="center",
                fontproperties=font, fontsize=label_size(pct),
                color="white" if luminance(col) < 0.55 else "black")
    ax.set_aspect("equal")
    if square:
        ax.set_xlim(-1.05, 1.05)
        ax.set_ylim(-1.05, 1.05)
        fig.savefig(out, dpi=300, transparent=True)
    else:
        fig.savefig(out, dpi=300, transparent=True, bbox_inches="tight")
    plt.close(fig)


def bars(items, out, title=None, white=False):
    """Cross-brand bars.

    PROVISIONAL layout — replace with Carmen's locked bar spec when it arrives.
    The --white variant rules are locked: #1a1a1a -> #FFFFFF, ticks/labels -> #D0CCC5,
    dark bars (luminance < 0.18) outlined instead of pale bars.
    """
    font = serif()
    items = sorted(items, key=lambda it: it["pct"])
    labels = [it["label"] for it in items]
    pcts = [it["pct"] for it in items]
    cols = [it.get("hex") or INK for it in items]
    text = "#FFFFFF" if white else INK
    axis = OUTLINE if white else INK

    fig, ax = plt.subplots(figsize=(9, max(4, 0.6 * len(items) + 1.5)))
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")
    rects = ax.barh(labels, pcts, color=cols, height=0.62)
    for r, col, pct in zip(rects, cols, pcts):
        lum = luminance(col)
        if (white and lum < 0.18) or (not white and lum > 0.82):
            r.set_edgecolor(OUTLINE)
            r.set_linewidth(1.2)
        ax.text(r.get_width() + max(pcts) * 0.015, r.get_y() + r.get_height() / 2,
                f"{pct:g}%", va="center", fontproperties=font, fontsize=18, color=text)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.tick_params(axis="y", length=0, colors=axis, labelsize=13)
    ax.set_xticks([])
    ax.set_xlim(0, max(pcts) * 1.15)
    if title:
        ax.set_title(title, loc="left", fontproperties=font, fontsize=26, color=text, pad=16)
    fig.savefig(out, dpi=300, transparent=True, bbox_inches="tight")
    plt.close(fig)


# Words that don't make two rows "the same thing" (colours, connectors, garment-neutral words).
NOT_FABRIC = {"and", "with", "over", "plus", "gold", "black", "white", "silver", "bronze", "brown",
              "pink", "red", "blue", "grey", "gray", "navy", "cream", "ivory", "dress", "jacket",
              "skirt", "coat", "long", "short", "mini", "midi", "maxi"}


# Words that name the same thing as a fabric ("Denim" vs "Shirt + jeans", "Tailoring" vs "Suit").
SYNONYMS = {"jean": "denim", "jeans": "denim", "suit": "tailoring", "suits": "tailoring",
            "suiting": "tailoring", "tailored": "tailoring"}


def fabric_words(label):
    import re
    words = (w for w in re.split(r"[^a-zà-ÿ]+", label.lower()) if len(w) >= 4 and w not in NOT_FABRIC)
    return {SYNONYMS.get(w, w) for w in words}


def similar(a, b):
    """True when a material and a silhouette name the same thing ("Knit" / "Knit sweater")."""
    wa, wb = fabric_words(a), fabric_words(b)
    return any(x[:4] == y[:4] for x in wa for y in wb)  # knit / knitted / knitwear


def canva_rows(decode, report=None):
    """Silhouette + material merged, ranked by share (stable on ties). Top 8 for Canva pages 3-4.

    A row that repeats a higher-ranked row from the other list (same fabric word) is skipped and the
    next row moves up, unless it has "keep": true in the decode.
    """
    merged = [dict(it, kind=k) for k in ("silhouette", "material") for it in decode.get(k, [])]
    chosen = []
    for it in sorted(merged, key=lambda it: -it["pct"]):
        dup = next((c for c in chosen if c["kind"] != it["kind"] and similar(c["label"], it["label"])), None)
        if dup and not it.get("keep"):
            if report is not None:
                report.append(f"skipped '{it['label']}' {it['pct']:g}% (repeats '{dup['label']}' {dup['pct']:g}%)")
            continue
        chosen.append(it)
        if len(chosen) == 8:
            break
    return chosen


def bar_geometry(rows):
    """Pink bar shapes for one Canva page (see references/canva-template.md)."""
    top_pct = max(it["pct"] for it in rows)
    out = []
    for i, it in enumerate(rows):
        width = max(6, round(90 * it["pct"] / top_pct))
        out.append({"left": 908 - width, "top": round(982.6 + 41.37 * i), "width": width, "height": 24})
    return out


def canva(decode):
    skipped = []
    rows = canva_rows(decode, skipped)
    for n, page in ((3, rows[:4]), (4, rows[4:8])):
        if not page:
            continue
        print(f"Page {n}")
        print("  names: " + json.dumps("\n".join(it["label"] for it in page), ensure_ascii=False))
        print("  pcts:  " + json.dumps("\n".join(f"{it['pct']:g}%" for it in page)))
        for it, g in zip(page, bar_geometry(page)):
            print(f"  {it['pct']:>3g}%  {it['kind']:<10} {it['label']:<34} bar {g}")
    for line in skipped:
        print("Skipped as similar: " + line)


def canva_donut(items):
    """Native Canva donut: one insert_shape per wedge + one add_text per label (page 2).

    Same geometry as the locked spec (width 0.42, labels at r=0.79, clockwise from 12 o'clock),
    sized to the template: centre (540, 675), outer radius 405, drawn in an 810x810 box at (135, 270).
    """
    R, c, box_left, box_top = 405, 405, 135, 270
    r = R * (1 - 0.42)

    def pt(rad, th):
        return c + rad * math.sin(th), c - rad * math.cos(th)

    total, acc, out = sum(it["pct"] for it in items), 0, []
    for it, col in zip(items, colours_for(items)):
        t0 = acc / total * 2 * math.pi
        acc += it["pct"]
        t1 = acc / total * 2 * math.pi
        large = 1 if t1 - t0 > math.pi else 0
        (x0, y0), (x1, y1), (x2, y2), (x3, y3) = pt(R, t0), pt(R, t1), pt(r, t1), pt(r, t0)
        d = (f"M{x0:.2f} {y0:.2f}A{R} {R} 0 {large} 1 {x1:.2f} {y1:.2f}"
             f"L{x2:.2f} {y2:.2f}A{r:.2f} {r:.2f} 0 {large} 0 {x3:.2f} {y3:.2f}Z")
        shape = {"type": "insert_shape", "top": box_top, "left": box_left, "width": 810, "height": 810,
                 "view_box_width": 810, "view_box_height": 810, "color": col.upper(), "path": d}
        if luminance(col) > 0.82:
            shape.update(stroke_color=OUTLINE, stroke_weight=1.2)
        lx, ly = pt(0.79 * R, (t0 + t1) / 2)
        size = label_size(it["pct"])
        w = 200 if size >= 32 else 100
        label = {"text": f"{it['pct']:g}%", "left": round(box_left + lx - w / 2), "top": round(box_top + ly - size * 0.5),
                 "width": w, "font_size": size, "color": "#FFFFFF" if luminance(col) < 0.55 else "#000000"}
        out.append({"label": it["label"], "shape": shape, "text": label})
    return out


def check(decode):
    problems = []
    for field in ("palette", "silhouette", "material"):
        items = decode.get(field)
        if not items:
            problems.append(f"{field}: missing")
            continue
        total = sum(it["pct"] for it in items)
        if abs(total - 100) > 1:
            problems.append(f"{field}: sums to {total}, not 100")
        elif total != 100:
            print(f"ℹ️  {field}: sums to {total} (equal counts kept equal %), footnote it")
        pcts = [it["pct"] for it in items]
        if pcts != sorted(pcts, reverse=True):
            problems.append(f"{field}: not ranked largest first")
    for it in decode.get("palette", []):
        if not it.get("hex"):
            problems.append(f"palette '{it['label']}': no hex")
    top = canva_rows(decode)
    if len(top) < 8:
        problems.append(f"Canva: only {len(top)} silhouette + material rows, template expects 8")
    for it in top:
        if len(it["label"]) > 30:
            problems.append(f"Canva row '{it['label']}': over 30 chars, will crowd the bars")
    looks = decode.get("looks")
    if looks:
        for field in ("palette", "silhouette", "material"):
            for it in decode.get(field, []):
                n = round(it["pct"] * looks / 100)
                if abs(n * 100 / looks - it["pct"]) >= 1 and not it.get("approx"):
                    problems.append(f"{field} '{it['label']}': {it['pct']}% matches no whole number of {looks} looks")
    for p in problems:
        print("⚠️ ", p)
    if not problems:
        print("✅ decode passes: sums, ranking, hexes, Canva rows")
    return not problems


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check")
    c.add_argument("json")
    cv = sub.add_parser("canva", help="rows and bar geometry for Canva pages 3-4")
    cv.add_argument("json")
    cd = sub.add_parser("canva-donut", help="native Canva shapes + labels for the page 2 donut")
    cd.add_argument("json")
    cd.add_argument("--field", default="palette")
    d = sub.add_parser("donut")
    d.add_argument("json")
    d.add_argument("--field", default="palette")
    d.add_argument("--out", required=True)
    d.add_argument("--square", action="store_true", help="square canvas for the Canva 1040x1040 frame")
    b = sub.add_parser("bars")
    b.add_argument("json")
    b.add_argument("--out", required=True)
    b.add_argument("--white", action="store_true")
    a = ap.parse_args()

    data = json.loads(Path(a.json).read_text())
    if a.cmd == "check":
        sys.exit(0 if check(data) else 1)
    if a.cmd == "canva":
        canva(data)
        return
    if a.cmd == "canva-donut":
        print(json.dumps(canva_donut(data[a.field]), indent=1, ensure_ascii=False))
        return
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    if a.cmd == "donut":
        donut(data[a.field], a.out, square=a.square)
    else:
        bars(data["items"], a.out, title=data.get("title"), white=a.white)
    print(a.out)


if __name__ == "__main__":
    main()
