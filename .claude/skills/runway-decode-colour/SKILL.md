---
name: runway-decode-colour
description: >
  Build a Runway Decode Colour Index for The Data Fashion Brief (season
  colour palette, per-house colour breakdowns as donuts and a swatch
  grid, and a per-colour over-indexing deep dive), from a runway colour
  export or Carmen's manual colour decode. Use this whenever Carmen
  uploads or references colour-tagged runway data (a "Colour Hex" sheet,
  a colours CSV, or a manual decode with per-brand colour percentages
  and hex codes) and wants a colour index, palette breakdown, or "which
  house over-indexed on X colour" piece, even if she just says "give me
  the colour piece" or pastes new season colour data without naming this
  skill directly. Also trigger if she asks to rebuild the season palette,
  add or swap a house's donut, fix the colour deep dive, or check whether
  a colour finding (like a season-wide colour reading as more or less
  prominent than press coverage suggests) matches the raw data.
---

# Runway Decode Colour Index

Builds the colour-only half of a Runway Decode pair (the other half is
`runway-decode-trends`, the materials/silhouettes/matrix piece). Read the
repo root `CLAUDE.md` first, every non-negotiable, voice note, and HTML
template rule there applies here, this skill only adds the
format-specific structure and chart logic on top of it.

Reference implementation: NYFW SS27, "The Colour Index." If you want a
finished example before building, that piece is the ground truth this
skill was extracted from.

## Before you start

- **Confirm the house list and count** the same way `runway-decode-trends`
  does, never carry a number over from a previous piece or a previous
  section of the same piece. If this piece is being built alongside a
  Trend Report for the same season, the two pieces' house counts must
  match, or state plainly why they don't (a house present in one dataset
  but missing colour data in the other is a real, sayable gap, not
  something to quietly paper over).
- **Where is the colour data actually coming from?** A spreadsheet's own
  "Colour Hex" sheet and Carmen's own manual visual decode are two
  different sources with potentially different scope (a house present in
  one might be missing from the other, or flagged wrong-season in one and
  not the other). If they disagree, that's worth surfacing to Carmen, not
  resolving silently by picking one.
- **Never trust an uploaded image's colours or percentages without
  Carmen identifying what it is.** A donut chart with no legend (by design,
  see the build spec below) tells you hex values and percentages but not
  which brand or season it belongs to. If Carmen sends a screenshot or
  exported chart image to replace or supplement data, ask which house or
  which season palette it is before using it, don't guess from context.

## Structure

1. **Season palette**: one donut, built with
   `scripts/build_donut_svg.py` at the season scale (`cx=cy=110, r=90,
   stroke_w=40, big=True`). No legend, ever, percentages render inside
   the wedges.
2. **Per-house palettes**: a grid of donuts, one per house, brand scale
   (`cx=cy=66, r=55, stroke_w=22, big=False`). If a house's full colour
   breakdown isn't available, either leave it out of the grid and say so
   in prose, or render only the known slices plus an unlabelled
   `remainder_pct` filler wedge, never invent a percentage to fill the
   gap.
3. **Swatch grid**: brand name (italic serif) beside five solid colour
   blocks per row, the same top colours as that house's donut, in the
   same order. This is a second, faster-to-scan view of the same real
   numbers, not a different dataset, keep the two in sync.
4. **The deep dive**: for each of the season's main colours, rank which
   houses over-indexed on it against the season average, using real
   per-house percentages (from the manual decode or colours CSV), not
   the spreadsheet's broader fabric-finish-style categories, those answer
   a different question. State the season average once, in the card
   title, not repeated per row.
5. **Prediction/takeaway block** and **methodology footer**, per the
   standard template in CLAUDE.md.

## Keeping this in sync with the Trend Report piece

If a Trend Report piece for the same season has its own brief colour
paragraph (per `runway-decode-trends`'s structure, step 6), that
paragraph's numbers need to match this piece's season palette exactly.
This went wrong once already: the season palette got corrected here
first, and the Trend Report kept citing the old numbers for several more
turns until Carmen caught it by eye. Before calling either piece
finished, grep the other one for the same figures.

## Donut build spec, in full

See `reference-articles/donut_chart_builder.py` for the matplotlib/PNG
version of this same spec (used for Carmen's Canva exports) and read the
docstring in `scripts/build_donut_svg.py` in this skill for the inline
SVG version used in the live HTML piece. Keep the two consistent:
largest slice at 12 o'clock, clockwise, labels at each wedge's true
angular midpoint (never a cumulative-sum position), font size scaled to
slice share, white or black label text chosen by wedge luminance, no
legend, no title, colours are self-explanatory.
