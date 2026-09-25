"""
Donut chart build spec — DFB Catwalk Decode
Saved verbatim from Carmen's spec. Standard methodology for all future
NYFW / Catwalk Decode donut charts (palette, silhouette, material).

Setup
- Library: Python + matplotlib
- Font: DM Serif Display, downloaded once, loaded via FontProperties(fname=...)
- Figure size: (9, 9), transparent background throughout, PNG output at dpi 300

Ring shape
- ax.pie() with wedgeprops width=0.42 (outer radius 1.0, inner radius 0.58)
- startangle=90, counterclock=False, largest slice at 12 o'clock, reads clockwise
- No gaps between wedges

Colours
- Each wedge's fill is the real hex for what it represents, self-explanatory,
  no legend needed
- Pale wedges (luminance > 0.82) get a thin #D0CCC5 outline so they don't
  vanish on a white Canva background

Percentage labels
- DM Serif Display, placed at each wedge's true theta midpoint (theta1/theta2
  average), NOT from cumulative sums — that bug stacks every label at the top
- Radius 0.79 (centre of the ring)
- Size scales with slice share: >=15% -> 42pt, >=8% -> 32pt, >=5% -> 22pt, <5% -> 14pt
- Text colour by wedge luminance: <0.55 -> white, else black
- Format "{int(round(pct))}%", no decimals

Nothing else on the chart. No colour names, no category labels, no legend, no title.

Data-entry rules
- Order slices largest first
- Percentages must sum to 100
- 6-10 slices is the sweet spot for one Catwalk Decode chart
- Palette charts: hex is the actual colour bucket
- Silhouette/material charts: hex is chosen to evoke the fabric/garment feel
  (leather -> dark brown, silk -> champagne, wool -> charcoal)
"""

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np

font_path = "DMSerifDisplay-Regular.ttf"  # sits alongside this script
dm_serif = fm.FontProperties(fname=font_path)


def font_size(pct):
    if pct >= 15: return 42
    elif pct >= 8: return 32
    elif pct >= 5: return 22
    else: return 14


def _rgb(hex_color):
    h = hex_color.lstrip('#')
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def text_color(hex_color):
    r, g, b = _rgb(hex_color)
    lum = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    return 'white' if lum < 0.55 else 'black'


def needs_outline(hex_color):
    r, g, b = _rgb(hex_color)
    lum = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    return lum > 0.82


def build_donut(data, filename):
    """
    data: list of (label, pct, hex_color) tuples, ordered largest first.
    Labels aren't rendered, they're just for reference.
    """
    pcts = [d[1] for d in data]
    colors = [d[2] for d in data]

    fig, ax = plt.subplots(figsize=(9, 9), facecolor='none')
    ax.set_facecolor('none')

    wedges, _ = ax.pie(
        pcts, colors=colors,
        startangle=90, counterclock=False,
        wedgeprops=dict(width=0.42, edgecolor='none'),
    )

    for w, c in zip(wedges, colors):
        if needs_outline(c):
            w.set_edgecolor('#D0CCC5')
            w.set_linewidth(1.2)

    for w, pct, color in zip(wedges, pcts, colors):
        theta_mid = (w.theta1 + w.theta2) / 2
        angle_rad = np.deg2rad(theta_mid)
        r = 0.79
        x, y = r * np.cos(angle_rad), r * np.sin(angle_rad)
        ax.text(
            x, y, f"{int(round(pct))}%",
            ha='center', va='center',
            fontproperties=dm_serif,
            fontsize=font_size(pct),
            color=text_color(color),
        )

    ax.set_aspect('equal')
    plt.tight_layout()
    plt.savefig(filename, transparent=True, dpi=300,
                bbox_inches='tight', facecolor='none')
    plt.close()
