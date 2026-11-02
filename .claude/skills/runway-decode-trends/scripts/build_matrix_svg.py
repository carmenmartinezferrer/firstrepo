"""
Two-axis quadrant matrix builder for Runway Decode Trend Report pieces.

Why this exists: this exact chart (trend alignment vs colour intensity,
split into four real quadrants) got hand-derived from scratch multiple
times in the NYFW SS27 session before it became a skill. The pixel math
is fiddly (rescale each axis to its own real min/max, not an assumed
0-100, place the quadrant divider at the real threshold, keep labels from
overlapping) and easy to get subtly wrong under time pressure. Doing it
once, correctly, as code removes that risk.

Usage:
    from build_matrix_svg import build_matrix

    alignment = {"Coach": 5.3, "Ralph Lauren": 5.0, ...}   # house -> score
    colour = {"Ulla Johnson": 62, "Conner Ives": 49, ...}   # house -> % non-neutral
    svg, groups = build_matrix(alignment, colour, align_thresh=3.7, colour_thresh=34)
    print(svg)          # paste straight into the chart-block
    print(groups)        # {"HH": [...], "HL": [...], "LH": [...], "LL": [...]}
    # use groups to write the chart-note and the findings paragraph accurately

Design notes (read CLAUDE.md's "Two-axis matrix charts" section for the
full reasoning, this is the short version):

- Each axis rescales to its own actual min and max, never an assumed
  0-100. A narrow-range metric (say a composite score that only spans
  single digits to twenty-something) plotted on an assumed full scale
  crushes all the real variation into one corner.
- The quadrant threshold on each axis is whatever value actually splits
  the season roughly in half, not a round number chosen for its own sake.
  Pass align_thresh / colour_thresh explicitly, don't guess a midpoint
  from min/max, real data is rarely symmetric.
- Dot colour is assigned by which of the four quadrants a house falls
  into (pink/black/gold/navy), never by a single axis alone. A single-axis
  colouring just repeats information the dot's position already shows.
- Label collisions are the one thing this script does NOT fully solve.
  It nudges labels right/left based on which half of the chart the dot
  sits in, but two dots that are genuinely close together (same house
  scoring near-identically on both axes as another) will still need a
  manual dy nudge via the `label_overrides` argument. Check the rendered
  chart before publishing, don't assume the auto-layout is perfect.
"""

import math


GROUP_COLOR = {"HH": "#D6447A", "HL": "#111114", "LH": "#B8963E", "LL": "#1B2A4A"}

# plot area, matches the established DFB template (viewBox 0 0 680 540)
X0, X1 = 90, 650
Y0, Y1 = 20, 470  # Y0 = top (high value), Y1 = bottom (low value)


def _xpos(value, vmin, vmax):
    return X0 + (value - vmin) / (vmax - vmin) * (X1 - X0)


def _ypos(value, vmin, vmax):
    # inverted: higher value -> smaller y (toward the top)
    return Y1 - (value - vmin) / (vmax - vmin) * (Y1 - Y0)


def build_matrix(alignment, colour, align_thresh, colour_thresh, label_overrides=None):
    """
    alignment, colour: dict[house] -> float, same keys.
    align_thresh, colour_thresh: the real values that split the season
        roughly in half on each axis (compute these from the actual data,
        don't guess).
    label_overrides: optional dict[house] -> (dx, dy, anchor) to hand-fix
        a label that collides with a neighbour after eyeballing the
        rendered chart. anchor is "start" (default, label to the right
        of the dot) or "end" (label to the left).

    Returns (svg_fragment, groups) where svg_fragment is the full
    <svg>...</svg> block (paste inside a .chart-block div, right after
    the .chart-subtitle) and groups is {"HH": [...], "HL": [...],
    "LH": [...], "LL": [...]} for writing the chart-note and findings
    paragraph from real group membership rather than guessing.
    """
    houses = list(alignment.keys())
    assert set(houses) == set(colour.keys()), "alignment and colour must cover the same houses"

    a_vals = list(alignment.values())
    c_vals = list(colour.values())
    amin, amax = min(a_vals), max(a_vals)
    cmin, cmax = min(c_vals), max(c_vals)

    divider_x = _xpos(align_thresh, amin, amax)
    divider_y = _ypos(colour_thresh, cmin, cmax)

    label_overrides = label_overrides or {}
    default_offset = (8, -3, "start")

    groups = {"HH": [], "HL": [], "LH": [], "LL": []}
    points = {}
    for house in houses:
        a, c = alignment[house], colour[house]
        hi_a = a >= align_thresh
        hi_c = c >= colour_thresh
        g = ("HH" if hi_a and hi_c else "HL" if hi_a else "LH" if hi_c else "LL")
        groups[g].append(house)
        x, y = _xpos(a, amin, amax), _ypos(c, cmin, cmax)
        points[house] = (x, y, g)

    parts = []
    parts.append(f'<rect x="{divider_x:.0f}" y="{Y0}" width="{X1-divider_x:.0f}" height="{divider_y-Y0:.0f}" fill="#D6447A" opacity="0.07"/>')
    parts.append(f'<rect x="{X0}" y="{Y0}" width="{divider_x-X0:.0f}" height="{divider_y-Y0:.0f}" fill="#B8963E" opacity="0.08"/>')
    parts.append(f'<rect x="{divider_x:.0f}" y="{divider_y:.0f}" width="{X1-divider_x:.0f}" height="{Y1-divider_y:.0f}" fill="#111114" opacity="0.05"/>')
    parts.append(f'<rect x="{X0}" y="{divider_y:.0f}" width="{divider_x-X0:.0f}" height="{Y1-divider_y:.0f}" fill="#1B2A4A" opacity="0.08"/>')
    parts.append(f'<line x1="{X0}" y1="{Y0}" x2="{X0}" y2="{Y1}" stroke="#E8E8E8" stroke-width="1"/>')
    parts.append(f'<line x1="{X0}" y1="{Y1}" x2="{X1}" y2="{Y1}" stroke="#E8E8E8" stroke-width="1"/>')
    parts.append(f'<line x1="{divider_x:.0f}" y1="{Y0}" x2="{divider_x:.0f}" y2="{Y1}" stroke="#cfcac3" stroke-width="1" stroke-dasharray="3,3"/>')
    parts.append(f'<line x1="{X0}" y1="{divider_y:.0f}" x2="{X1}" y2="{divider_y:.0f}" stroke="#cfcac3" stroke-width="1" stroke-dasharray="3,3"/>')

    label_x = divider_x + 8
    parts.append(f'<text x="{label_x:.0f}" y="40" font-family="Century Gothic, sans-serif" font-size="12" font-weight="700" fill="#D6447A">SEASON-LED, COLOUR-FORWARD</text>')
    parts.append(f'<text x="98" y="40" font-family="Century Gothic, sans-serif" font-size="12" font-weight="700" fill="#96751f">INDEPENDENT, COLOUR-FORWARD</text>')
    parts.append(f'<text x="{label_x:.0f}" y="455" font-family="Century Gothic, sans-serif" font-size="12" font-weight="700" fill="#555">SEASON-LED, NEUTRAL</text>')
    parts.append(f'<text x="98" y="455" font-family="Century Gothic, sans-serif" font-size="12" font-weight="700" fill="#1B2A4A">INDEPENDENT, NEUTRAL</text>')
    parts.append(f'<text x="{X0}" y="495" font-family="Century Gothic, sans-serif" font-size="13" font-weight="600" fill="#333">Low alignment</text>')
    parts.append(f'<text x="530" y="495" font-family="Century Gothic, sans-serif" font-size="13" font-weight="600" fill="#333">High alignment</text>')
    parts.append(f'<text x="15" y="16" font-family="Century Gothic, sans-serif" font-size="13" font-weight="600" fill="#333">High colour</text>')
    parts.append(f'<text x="15" y="480" font-family="Century Gothic, sans-serif" font-size="13" font-weight="600" fill="#333">Low colour</text>')

    # sort right-to-left so the auto anchor-flip near the right edge reads naturally
    for house in sorted(points, key=lambda h: -points[h][0]):
        x, y, g = points[house]
        color = GROUP_COLOR[g]
        if house in label_overrides:
            dx, dy, anchor = label_overrides[house]
        elif x > X1 - 40:
            dx, dy, anchor = -10, -3, "end"
        else:
            dx, dy, anchor = default_offset
        anchor_attr = f' text-anchor="{anchor}"' if anchor == "end" else ""
        parts.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="{color}"/>'
            f'<text x="{x+dx:.1f}" y="{y+dy:.1f}"{anchor_attr} '
            f'font-family="Century Gothic, sans-serif" font-size="13" font-weight="500" fill="#222">{house}</text>'
        )

    svg = (
        '<svg class="matrix-svg" viewBox="0 0 680 540" preserveAspectRatio="none">\n  '
        + '\n  '.join(parts)
        + '\n</svg>'
    )
    return svg, groups


if __name__ == "__main__":
    # smoke test with made-up numbers, run this after editing the script
    # to sanity-check the output still parses as valid-looking SVG
    demo_align = {"A": 5.3, "B": 5.0, "C": 4.5, "D": 2.6}
    demo_colour = {"A": 62, "B": 15, "C": 41, "D": 18}
    svg, groups = build_matrix(demo_align, demo_colour, align_thresh=4.0, colour_thresh=34)
    print(groups)
    print(svg[:200], "...")
