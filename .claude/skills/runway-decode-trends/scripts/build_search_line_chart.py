"""
Search-validation line chart, the "same scale head to head" comparison
from the menswear SS27 piece (see CLAUDE.md's Trend validation
methodology section). Confirmed working on the menswear and NYFW SS27
pieces before becoming a skill.

Input is raw Google Trends CSV rows (worldwide, "Past year" column),
one per trend being compared, all already on Trends' own 0-100 scale,
so no rescaling is needed, that's what makes this a legitimate
"same-scale" comparison rather than something dressed up to look like
one.

Usage:
    from build_search_line_chart import build_line_chart, load_trends_csv

    lead = load_trends_csv("slip_dress.csv", value_col="slip dress Past year")
    compare = load_trends_csv("midi_skirt.csv", value_col="midi skirt Past year")
    svg, stats = build_line_chart(lead, compare, lead_name="Slip dress", compare_name="Midi skirt")
    print(svg)
    print(stats)  # {"lead_higher_weeks": 50, "total_weeks": 53, "lead_offpeak_avg": 24.7, ...}

    Use `stats` to write the chart-note honestly, e.g.
    f"{lead_name} runs higher than {compare_name} in {stats['lead_higher_weeks']} "
    f"of the last {stats['total_weeks']} weeks."
    Don't round or estimate these, they come straight from the data.
"""

import csv
import datetime


def load_trends_csv(path, value_col):
    """Returns a list of (date_str, value) tuples, in file order."""
    rows = []
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append((row["Time"], int(row[value_col])))
    return rows


def build_line_chart(lead, compare, lead_name, compare_name):
    """
    lead, compare: list of (date_str, value) tuples, same length, same
        dates, values already 0-100 (Google Trends' own scale).
    lead_name, compare_name: labels for the legend and stats dict.
    """
    assert len(lead) == len(compare), "both series must cover the same weeks"
    n = len(lead)

    x0, x1 = 50, 660
    y0, y1 = 30, 280  # y0 = top (value 100), y1 = bottom (value 0)

    def xpos(i):
        return x0 + i / (n - 1) * (x1 - x0)

    def ypos(v):
        return y1 - (v / 100) * (y1 - y0)

    lead_pts = " ".join(f"{xpos(i):.1f},{ypos(v):.1f}" for i, (_, v) in enumerate(lead))
    compare_pts = " ".join(f"{xpos(i):.1f},{ypos(v):.1f}" for i, (_, v) in enumerate(compare))

    # month tick labels: first occurrence of each new month
    seen = set()
    ticks = []
    for i, (d, _) in enumerate(lead):
        dt = datetime.datetime.strptime(d, "%Y-%m-%d")
        key = (dt.year, dt.month)
        if key not in seen:
            seen.add(key)
            ticks.append((i, dt.strftime("%b")))
    # thin to roughly every other month if there are more than ~8 ticks,
    # a year of weekly data produces 12-13 otherwise and they'll collide
    if len(ticks) > 8:
        ticks = ticks[::2]

    tick_svg = "\n  ".join(
        f'<text x="{xpos(i):.1f}" y="300" text-anchor="middle" font-family="Century Gothic, sans-serif" font-size="10" fill="#888">{label}</text>'
        for i, label in ticks
    )

    svg = f'''<svg class="matrix-svg" viewBox="0 0 680 330" preserveAspectRatio="none">
  <line x1="50" y1="30" x2="50" y2="280" stroke="#E8E8E8" stroke-width="1"/>
  <line x1="50" y1="280" x2="660" y2="280" stroke="#E8E8E8" stroke-width="1"/>
  <line x1="50" y1="155" x2="660" y2="155" stroke="#E8E8E8" stroke-width="1" stroke-dasharray="2,3"/>
  <line x1="50" y1="30" x2="660" y2="30" stroke="#E8E8E8" stroke-width="1" stroke-dasharray="2,3"/>
  <text x="42" y="284" text-anchor="end" font-family="Century Gothic, sans-serif" font-size="11" fill="#888">0</text>
  <text x="42" y="159" text-anchor="end" font-family="Century Gothic, sans-serif" font-size="11" fill="#888">50</text>
  <text x="42" y="34" text-anchor="end" font-family="Century Gothic, sans-serif" font-size="11" fill="#888">100</text>
  <polyline points="{compare_pts}" fill="none" stroke="#111114" stroke-width="2"/>
  <polyline points="{lead_pts}" fill="none" stroke="#D6447A" stroke-width="2.4"/>
  {tick_svg}
  <circle cx="30" cy="10" r="5" fill="#D6447A"/><text x="40" y="14" font-family="Century Gothic, sans-serif" font-size="12" font-weight="500" fill="#222">{lead_name}</text>
  <circle cx="150" cy="10" r="5" fill="#111114"/><text x="160" y="14" font-family="Century Gothic, sans-serif" font-size="12" font-weight="500" fill="#222">{compare_name}</text>
</svg>'''

    lead_vals = [v for _, v in lead]
    compare_vals = [v for _, v in compare]
    stats = {
        "lead_higher_weeks": sum(1 for lv, cv in zip(lead_vals, compare_vals) if lv > cv),
        "total_weeks": n,
        "lead_avg": sum(lead_vals) / n,
        "compare_avg": sum(compare_vals) / n,
        "lead_peak": max(lead_vals),
        "compare_peak": max(compare_vals),
        "lead_latest": lead_vals[-1],
        "compare_latest": compare_vals[-1],
    }
    return svg, stats


if __name__ == "__main__":
    # smoke test: synthetic data, no real file needed
    demo_lead = [(f"2025-{m:02d}-01", 20 + m) for m in range(1, 13)]
    demo_compare = [(f"2025-{m:02d}-01", 10 + m) for m in range(1, 13)]
    svg, stats = build_line_chart(demo_lead, demo_compare, "Lead trend", "Compare trend")
    print(stats)
    assert "<svg" in svg and "</svg>" in svg
    print("ok")
