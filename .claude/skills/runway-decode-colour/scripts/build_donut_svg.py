"""
Inline SVG donut builder for Runway Decode Colour Index pieces (season
palette + per-brand palettes). This is the same wedge math as
reference-articles/donut_chart_builder.py, which targets matplotlib/PNG
output for Canva, this version targets inline SVG for the live HTML
artifact. Keep the two specs consistent with each other, if one changes
(label placement, luminance threshold, font-size tiers), check whether
the other should change too.

No legend, no title inside the chart, ever, colours are self-explanatory
and percentages render inside the wedges. This was an explicit, repeated
correction from Carmen in the session this skill was extracted from,
adding a side legend back "for clarity" is the single most likely way
this skill gets misused, don't do it.

Usage:
    from build_donut_svg import build_donut

    # season donut: bigger ring
    season = [("Navy", "#1B2340", 16), ("Brown", "#6B4A35", 14), ...]  # sums to 100
    svg = build_donut(season, cx=110, cy=110, r=90, stroke_w=40, big=True)

    # brand donut: smaller ring, same function
    brand = [("Black", "#1A1A1A", 18), ("Chocolate/Brown", "#5A3E28", 15), ...]
    svg = build_donut(brand, cx=66, cy=66, r=55, stroke_w=22, big=False)

    # if a brand's known colours don't sum to 100 (partial data), pass
    # remainder_pct for the leftover share as an unlabelled filler wedge
    # rather than pretending the known slices are the whole palette
    svg = build_donut(partial_brand, cx=66, cy=66, r=55, stroke_w=22, big=False, remainder_pct=23)
"""

import math

REMAINDER_HEX = "#E3DFDA"
BLACK = "#141114"
WHITE = "#ffffff"


def _luminance(hexv):
    h = hexv.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return (0.299 * r + 0.587 * g + 0.114 * b) / 255


def _text_color(hexv):
    return WHITE if _luminance(hexv) < 0.55 else BLACK


def _font_size(pct, big):
    # season donut (big=True) runs at roughly double the brand-card scale
    if big:
        if pct >= 15:
            return 16
        if pct >= 8:
            return 13
        if pct >= 5:
            return 11
        return 9
    else:
        if pct >= 15:
            return 10
        if pct >= 8:
            return 9
        if pct >= 5:
            return 7
        return 6


def build_donut(slices, cx, cy, r, stroke_w, big, remainder_pct=0):
    """
    slices: list of (name, hex, pct) tuples, largest first, name is for
        your own reference only, it is never rendered on the chart.
    cx, cy, r, stroke_w: ring geometry. Established sizes: season donut
        cx=cy=110, r=90, stroke_w=40 (220x220 viewBox); brand donut
        cx=cy=66, r=55, stroke_w=22 (132x132 viewBox).
    big: True for the season-scale font tiers, False for brand-card scale.
    remainder_pct: unlabelled filler wedge for the unknown share of a
        brand whose full palette isn't decoded yet. Coloured
        #E3DFDA (pale neutral), no percentage label, since it doesn't
        represent one real named colour.

    Percentages should sum to 100 once remainder_pct is included. This
    function does not silently normalise a mismatched total, if your
    slices plus remainder don't add to 100, fix the input data rather
    than let the chart quietly misrepresent the season.
    """
    total = sum(p for _, _, p in slices) + remainder_pct
    assert abs(total - 100) < 0.5, f"slices + remainder must sum to ~100, got {total}"

    circumference = 2 * math.pi * r
    parts = []
    cum = 0.0
    for _, hexv, pct in slices:
        seg_len = circumference * pct / 100
        parts.append(
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{hexv}" '
            f'stroke-width="{stroke_w}" stroke-dasharray="{seg_len:.1f} {circumference-seg_len:.1f}" '
            f'stroke-dashoffset="-{circumference*cum/100:.1f}" transform="rotate(-90 {cx} {cy})"/>'
        )
        cum += pct
    if remainder_pct > 0:
        seg_len = circumference * remainder_pct / 100
        parts.append(
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{REMAINDER_HEX}" '
            f'stroke-width="{stroke_w}" stroke-dasharray="{seg_len:.1f} {circumference-seg_len:.1f}" '
            f'stroke-dashoffset="-{circumference*cum/100:.1f}" transform="rotate(-90 {cx} {cy})"/>'
        )
        cum += remainder_pct

    # labels at each wedge's TRUE angular midpoint, not a cumulative-sum
    # position, that bug stacks every label at the top of the ring
    cum = 0.0
    for _, hexv, pct in slices:
        fm = (cum + pct / 2) / 100
        theta = fm * 360
        x = cx + r * math.sin(math.radians(theta))
        y = cy - r * math.cos(math.radians(theta))
        size = _font_size(pct, big)
        color = _text_color(hexv)
        parts.append(
            f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="middle" dominant-baseline="central" '
            f'font-family="\'DM Serif Display\', serif" font-weight="700" font-size="{size}" '
            f'fill="{color}">{int(round(pct))}%</text>'
        )
        cum += pct

    size_attr = int(cx * 2)
    return f'<svg width="{size_attr}" height="{size_attr}" viewBox="0 0 {size_attr} {size_attr}">' + "".join(parts) + "</svg>"


if __name__ == "__main__":
    demo = [("Navy", "#1B2340", 40), ("Brown", "#6B4A35", 35), ("Gold", "#D9A949", 25)]
    svg = build_donut(demo, cx=110, cy=110, r=90, stroke_w=40, big=True)
    assert svg.startswith("<svg") and svg.endswith("</svg>")
    print("ok,", len(svg), "chars")
