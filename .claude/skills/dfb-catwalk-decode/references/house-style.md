# DFB house style

## Brand
- **Colours:** black, white, and pink `#D6447A`. Use the pink sparingly, as the accent: Canva trend bars, one highlight per chart at most.
- **Type:** DM Serif Display for titles and chart numbers, Century Gothic for body text. The Canva template already carries its own fonts, so keep them.
- **Voice:** analyst, not reviewer. Lead with the number, then the reading.

## Caption format (ONLY when asked)

```
Para 1: verdict + the dominant silhouette stat.
Para 2: the material/palette tension, with 2–3 stats.
Para 3 (optional): the finale or the twist.
The codes are: X, Y, Z.

#Brand #SS27 #CatwalkDecode #FashionData #DFB #PFW @brandhandle
```
- Swap the fashion week tag to match: `#LFW`, `#MFW`, `#PFW`, `#NYFW`.
- Brand hashtag: no spaces (`#SaintLaurent`). Handle: the house's official Instagram handle. If unsure, write `@[handle?]` rather than guessing.

## Donut spec (one collection) — LOCKED

- figsize (9, 9), transparent background, dpi 300, `bbox_inches="tight"`.
- `ax.pie(startangle=90, counterclock=False, wedgeprops={"width": 0.42, "edgecolor": "none"})`.
- Wedges with **luminance > 0.82** get a `#D0CCC5` outline, linewidth 1.2.
- % label inside each wedge at radius 0.79, in DM Serif Display.
- Label size by share: **42** (≥15%), **32** (≥8%), **22** (≥5%), **14** (below 5%).
- Label colour: **white if luminance < 0.55**, otherwise black.
- Wedge colour = the actual colour, or a representative hex for prints and materials.
- Luminance = WCAG relative luminance (sRGB linearised; 0.2126 R + 0.7152 G + 0.0722 B). This matches the Balmain template donut: white text on tan and olive, black on mint and ivory.

`scripts/dfb_charts.py donut` implements this exactly. Don't restyle it.

## Bar spec (cross-brand)

> ⚠️ **PENDING: Carmen's locked bar chart spec hasn't been pasted yet.** `scripts/dfb_charts.py bars` uses a provisional DFB-styled default (horizontal bars, sorted, % labels at the bar end, `#1a1a1a` text, no spines). When the locked spec arrives, replace the `bars()` function and this section with it.

**White-text variant (`--white`)**, for dark backgrounds. This part is locked:
- Every `#1a1a1a` becomes `#FFFFFF`.
- Axis ticks and axis labels become `#D0CCC5`.
- Dark bars (luminance < 0.18) get the `#D0CCC5` outline. In the normal variant it's the pale bars that get it.
