#!/usr/bin/env python3
"""DFB catwalk charts: locked donut spec, cross-brand bars, and a decode sanity check.

  python dfb_charts.py check  decode.json
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
    if pct >= 5:
        return 22
    return 14


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


def check(decode):
    problems = []
    for field in ("palette", "silhouette", "material"):
        items = decode.get(field)
        if not items:
            problems.append(f"{field}: missing")
            continue
        total = sum(it["pct"] for it in items)
        if abs(total - 100) > 0:
            problems.append(f"{field}: sums to {total}, not 100")
        pcts = [it["pct"] for it in items]
        if pcts != sorted(pcts, reverse=True):
            problems.append(f"{field}: not ranked largest first")
    for it in decode.get("palette", []):
        if not it.get("hex"):
            problems.append(f"palette '{it['label']}': no hex")
    top = decode.get("canva_top", [])
    if top:
        if len(top) != 8:
            problems.append(f"canva_top: {len(top)} rows, template expects 8")
        for it in top:
            if len(it["label"]) > 30:
                problems.append(f"canva_top '{it['label']}': over 30 chars, will crowd the bars")
    looks = decode.get("looks")
    if looks:
        for field in ("palette", "silhouette", "material"):
            for it in decode.get(field, []):
                n = it["pct"] * looks / 100
                if abs(n - round(n)) > 0.35 and not it.get("approx"):
                    problems.append(f"{field} '{it['label']}': {it['pct']}% of {looks} = {n:.1f} looks, check the count")
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
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    if a.cmd == "donut":
        donut(data[a.field], a.out, square=a.square)
    else:
        bars(data["items"], a.out, title=data.get("title"), white=a.white)
    print(a.out)


if __name__ == "__main__":
    main()
