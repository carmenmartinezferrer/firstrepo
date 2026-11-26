"""Generates the three concept illustrations (statistics, what data analytics is,
how a data project works) as 1080x1920 SVGs on a white background.
Usage: python3 -I make_concepts.py <out_dir>
"""
import math
import random
import sys

OUT = sys.argv[1]
SANS = "font-family=\"'Century Gothic', 'TeX Gyre Adventor', 'URW Gothic', Arial, sans-serif\""
PINK, BLACK, NUDE, GREY = "#D6447A", "#111111", "#E3CDB8", "#BDBDBD"


def svg(title, body, label):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920" width="1080" height="1920" '
        f'role="img" aria-label="{label}">\n  <title>{title}</title>\n'
        f'  <rect width="1080" height="1920" fill="#FFFFFF"/>\n{body}</svg>\n'
    )


def text(x, y, s, size=32, weight=400, fill="#222222", anchor="start", extra=""):
    return (f'  <text x="{x}" y="{y}" {SANS} font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}" {extra}>{s}</text>\n')


def header(title, subtitle):
    return text(540, 150, title, 64, 700, "#111111", "middle") + text(540, 215, subtitle, 32, 400, "#777777", "middle")


def badge(x, y, n):
    return (f'  <circle cx="{x}" cy="{y}" r="28" fill="{PINK}"/>\n'
            + text(x, y + 13, str(n), 36, 700, "#FFFFFF", "middle"))


def arrow_down(x, y1, y2):
    return (f'  <line x1="{x}" y1="{y1}" x2="{x}" y2="{y2 - 22}" stroke="{PINK}" stroke-width="8" '
            f'stroke-dasharray="14 10" stroke-linecap="round"/>\n'
            f'  <polygon points="{x - 24},{y2 - 26} {x + 24},{y2 - 26} {x},{y2}" fill="{PINK}"/>\n')


def check(cx, cy, r, color=PINK, w=None):
    w = w or r * 0.22
    return (f'  <circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}"/>\n'
            f'  <path d="M{cx - r * 0.45:.1f} {cy + r * 0.03:.1f} L{cx - r * 0.1:.1f} {cy + r * 0.38:.1f} '
            f'L{cx + r * 0.5:.1f} {cy - r * 0.36:.1f}" fill="none" stroke="#FFFFFF" stroke-width="{w:.1f}" '
            f'stroke-linecap="round" stroke-linejoin="round"/>\n')


# ---------------------------------------------------------------- 1. statistics
def statistics():
    b = header("Statistics", "telling what's real from what's luck")
    # panel 1: average and spread
    b += badge(100, 330, 1) + text(150, 343, "The average and the spread", 38, 700)
    pts = []
    for x in range(140, 941, 8):
        y = 700 - 300 * math.exp(-0.5 * ((x - 540) / 120) ** 2)
        pts.append(f"{x},{y:.1f}")
    line = " ".join(pts)
    b += f'  <polygon points="140,700 {line} 940,700" fill="{PINK}" fill-opacity="0.18"/>\n'
    b += f'  <polyline points="{line}" fill="none" stroke="{PINK}" stroke-width="8" stroke-linejoin="round"/>\n'
    b += '  <line x1="120" y1="700" x2="960" y2="700" stroke="#222222" stroke-width="5" stroke-linecap="round"/>\n'
    b += '  <line x1="540" y1="410" x2="540" y2="700" stroke="#111111" stroke-width="4" stroke-dasharray="12 10"/>\n'
    b += text(540, 395, "average", 30, 700, "#111111", "middle")
    b += ('  <line x1="425" y1="600" x2="655" y2="600" stroke="#111111" stroke-width="5" stroke-linecap="round"/>\n'
          '  <polygon points="418,600 440,588 440,612" fill="#111111"/>\n'
          '  <polygon points="662,600 640,588 640,612" fill="#111111"/>\n')
    b += text(540, 645, "spread", 28, 400, "#222222", "middle", 'paint-order="stroke" stroke="#F8DFE8" stroke-width="14" stroke-linejoin="round"')
    b += text(540, 750, "most values sit near the middle, a few sit far out", 28, 400, "#777777", "middle")
    # panel 2: sample vs everyone
    b += badge(100, 850, 2) + text(150, 863, "A sample stands in for everyone", 38, 700)
    sample = {(1, 0), (5, 1), (9, 0), (12, 2), (3, 3), (7, 3), (10, 4), (2, 5), (6, 5)}
    for j in range(6):
        for i in range(14):
            cx, cy = 176 + 56 * i, 960 + 56 * j
            col = PINK if (i, j) in sample else "#D9D9D9"
            b += f'  <circle cx="{cx}" cy="{cy}" r="16" fill="{col}"/>\n'
    b += f'  <circle cx="170" cy="1310" r="14" fill="{PINK}"/>\n' + text(200, 1320, "the sample you measured", 28)
    b += '  <circle cx="650" cy="1310" r="14" fill="#D9D9D9"/>\n' + text(680, 1320, "everyone you didn't", 28)
    # panel 3: real or luck
    b += badge(100, 1410, 3) + text(150, 1423, "Real difference, or luck?", 38, 700)
    base = 1780
    b += f'  <line x1="200" y1="{base}" x2="880" y2="{base}" stroke="#222222" stroke-width="5" stroke-linecap="round"/>\n'
    b += f'  <rect x="200" y="1520" width="680" height="80" fill="{PINK}" fill-opacity="0.12"/>\n'
    b += f'  <rect x="320" y="{base - 200}" width="140" height="200" fill="{GREY}"/>\n'
    b += f'  <rect x="620" y="{base - 250}" width="140" height="250" fill="{PINK}"/>\n'
    for cx, lo, hi in ((390, 1520, 1640), (690, 1460, 1600)):
        b += (f'  <line x1="{cx}" y1="{lo}" x2="{cx}" y2="{hi}" stroke="#111111" stroke-width="5"/>\n'
              f'  <line x1="{cx - 22}" y1="{lo}" x2="{cx + 22}" y2="{lo}" stroke="#111111" stroke-width="5" stroke-linecap="round"/>\n'
              f'  <line x1="{cx - 22}" y1="{hi}" x2="{cx + 22}" y2="{hi}" stroke="#111111" stroke-width="5" stroke-linecap="round"/>\n')
    b += text(390, 1825, "A", 30, 700, "#111111", "middle") + text(690, 1825, "B", 30, 700, "#111111", "middle")
    b += text(540, 1875, "if the ranges overlap, the gap could just be luck", 28, 400, "#777777", "middle")
    return svg("Statistics", b, "Statistics: the average and the spread, a sample standing in for everyone, and whether a gap is real or luck")


# ---------------------------------------------------------------- 2. data analytics
def analytics():
    b = header("What data analytics is", "turning data into decisions")
    # stage 1: messy dots
    b += badge(100, 330, 1) + text(150, 343, "Messy data", 38, 700)
    rnd = random.Random(7)
    placed = []
    palette = [PINK, BLACK, NUDE, GREY]
    while len(placed) < 64:
        x, y = rnd.uniform(150, 930), rnd.uniform(390, 600)
        if all((x - px) ** 2 + (y - py) ** 2 > 30 ** 2 for px, py, _ in placed):
            placed.append((x, y, rnd.choice(palette)))
    for x, y, c in placed:
        b += f'  <circle cx="{x:.0f}" cy="{y:.0f}" r="11" fill="{c}"/>\n'
    b += arrow_down(540, 640, 700)
    # stage 2: sorted
    b += badge(100, 760, 2) + text(150, 773, "Cleaned and sorted", 38, 700)
    for r, c in enumerate(palette):
        for i in range(12):
            b += f'  <circle cx="{342 + 36 * i}" cy="{840 + 52 * r}" r="11" fill="{c}"/>\n'
    b += arrow_down(540, 1020, 1080)
    # stage 3: patterns
    b += badge(100, 1140, 3) + text(150, 1153, "Patterns show up", 38, 700)
    base = 1400
    b += f'  <line x1="200" y1="{base}" x2="880" y2="{base}" stroke="#222222" stroke-width="5" stroke-linecap="round"/>\n'
    for cx, h, c in ((300, 90, PINK), (440, 220, BLACK), (580, 140, NUDE), (720, 180, GREY)):
        b += f'  <rect x="{cx - 45}" y="{base - h}" width="90" height="{h}" fill="{c}"/>\n'
    b += arrow_down(540, 1425, 1485)
    # stage 4: decision
    b += badge(100, 1545, 4) + text(150, 1558, "A decision someone can make", 38, 700)
    b += '  <rect x="160" y="1600" width="760" height="120" rx="30" fill="#FFFFFF" stroke="#222222" stroke-width="6"/>\n'
    b += check(240, 1660, 36)
    b += text(305, 1672, "what do we back next?", 36, 700, "#111111")
    # four questions
    b += text(540, 1790, "the four questions analytics answers", 28, 400, "#777777", "middle")
    pills = [("what happened", 250, False), ("why", 110, False), ("what next", 190, False), ("what to do", 210, True)]
    total = sum(w for _, w, _ in pills) + 18 * (len(pills) - 1)
    x = 540 - total / 2
    for label, w, hot in pills:
        fill = PINK if hot else "#FFFFFF"
        stroke = PINK if hot else "#111111"
        tcol = "#FFFFFF" if hot else "#111111"
        b += f'  <rect x="{x:.0f}" y="1815" width="{w}" height="58" rx="29" fill="{fill}" stroke="{stroke}" stroke-width="4"/>\n'
        b += text(f"{x + w / 2:.0f}", 1853, label, 26, 700, tcol, "middle")
        x += w + 18
    return svg("What data analytics is", b, "Data analytics: messy data becomes cleaned data, then patterns, then a decision")


# ---------------------------------------------------------------- 3. how a data project works
def project():
    b = header("How a data project works", "five steps, and then you go round again")
    steps = [
        ("Ask the right question", "what decision is this for?"),
        ("Find and clean the data", "where it lives and what's missing"),
        ("Analyse it", "patterns, comparisons, the basic stats"),
        ("Tell the story", "a chart and a clear answer"),
        ("Decide, then check", "did it work? what's the next question?"),
    ]
    cx = 170
    centers = [400, 650, 900, 1150, 1400]
    for i, ((head, sub), cy) in enumerate(zip(steps, centers)):
        b += f'  <circle cx="{cx}" cy="{cy}" r="78" fill="#FFFFFF" stroke="#222222" stroke-width="6"/>\n'
        b += f'  <circle cx="{cx - 62}" cy="{cy - 62}" r="24" fill="{PINK}"/>\n' + text(cx - 62, cy - 51, str(i + 1), 28, 700, "#FFFFFF", "middle")
        b += text(290, cy - 8, head, 40, 700, "#111111") + text(290, cy + 38, sub, 30, 400, "#777777")
        if i < len(steps) - 1:
            b += arrow_down(cx, cy + 86, centers[i + 1] - 86)
    # icons
    c1, c2, c3, c4, c5 = centers
    b += text(cx, c1 + 36, "?", 100, 700, PINK, "middle")
    b += (f'  <rect x="{cx - 30}" y="{c2 - 26}" width="60" height="56" fill="{BLACK}"/>\n'
          f'  <ellipse cx="{cx}" cy="{c2 + 30}" rx="30" ry="10" fill="{BLACK}"/>\n'
          f'  <ellipse cx="{cx}" cy="{c2 - 26}" rx="30" ry="10" fill="#333333"/>\n'
          f'  <path d="M{cx - 30} {c2 - 2} A30 10 0 0 0 {cx + 30} {c2 - 2}" fill="none" stroke="{PINK}" stroke-width="5"/>\n'
          f'  <path d="M{cx - 30} {c2 + 16} A30 10 0 0 0 {cx + 30} {c2 + 16}" fill="none" stroke="{PINK}" stroke-width="5"/>\n')
    b += (f'  <rect x="{cx - 40}" y="{c3 - 2}" width="22" height="38" fill="{BLACK}"/>\n'
          f'  <rect x="{cx - 11}" y="{c3 - 26}" width="22" height="62" fill="{BLACK}"/>\n'
          f'  <rect x="{cx + 18}" y="{c3 - 50}" width="22" height="86" fill="{PINK}"/>\n'
          f'  <line x1="{cx - 48}" y1="{c3 + 38}" x2="{cx + 48}" y2="{c3 + 38}" stroke="#222222" stroke-width="5" stroke-linecap="round"/>\n')
    b += (f'  <rect x="{cx - 44}" y="{c4 - 34}" width="88" height="62" rx="16" fill="{BLACK}"/>\n'
          f'  <polygon points="{cx - 20},{c4 + 24} {cx - 34},{c4 + 48} {cx + 4},{c4 + 24}" fill="{BLACK}"/>\n'
          f'  <circle cx="{cx - 18}" cy="{c4 - 3}" r="6" fill="#FFFFFF"/><circle cx="{cx}" cy="{c4 - 3}" r="6" fill="#FFFFFF"/><circle cx="{cx + 18}" cy="{c4 - 3}" r="6" fill="#FFFFFF"/>\n')
    b += check(cx, c5, 40)
    # loop back to the start
    b += (f'  <path d="M960 {c5} C1040 {c5} 1040 {c1} 972 {c1}" fill="none" stroke="{PINK}" stroke-width="8" '
          f'stroke-dasharray="14 10" stroke-linecap="round"/>\n'
          f'  <polygon points="950,{c1} 980,{c1 - 16} 980,{c1 + 16}" fill="{PINK}"/>\n')
    b += text(1054, 900, "and go round again", 28, 400, "#777777", "middle", 'transform="rotate(-90 1054 900)"')
    b += text(540, 1650, "the question comes first, the chart comes last", 30, 400, "#777777", "middle")
    return svg("How a data project works", b, "A data project in five steps: ask, find and clean data, analyse, tell the story, decide and check, then repeat")


for name, fn in (("concept-statistics", statistics), ("concept-data-analytics", analytics), ("concept-data-project", project)):
    open(f"{OUT}/{name}.svg", "w", encoding="utf-8").write(fn())
    print("wrote", name)
