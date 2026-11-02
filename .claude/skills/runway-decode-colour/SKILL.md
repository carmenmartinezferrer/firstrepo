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

**Voice**: read `reference-articles/nyfw-ss27-trend-report-final.md`
before drafting. It's the Trend Report half of this same season, not this
piece, but it's Carmen's own final approved copy and the tone anchor for
both halves of a Runway Decode pair, this piece should read like the same
person wrote it on the same day, casual asides, rhetorical-question
subheads, personal links to her own past pieces, a direct question to the
reader before the sign-off, not a flatter or more "complete report"
register just because this piece is more chart-dense.

`reference-articles/external-trend-autopsy-format-example.md` is a
second, secondary voice reference, a different Substack's piece,
structure not relevant here (it's the Trend Autopsy format, not Runway
Decode), but CLAUDE.md confirms it's a legitimate register match too.

Reference implementation: NYFW SS27, "The Colour Index." If you want a
finished example before building, that piece is the ground truth this
skill was extracted from.

## Standard from Paris SS27 onward (overrides older structure below where they differ)

Carmen set these on the Paris SS27 colour piece. Apply them every time.

**Data.** Every colour number comes from the workbook's **Colour mix donut**
tab (each look split across up to three colours by coverage, slices add to
100, colours never merged into each other, prints are their own slices).
Use `Level` = fashion week for the season, `Level` = house per show. Use
**Colour shades (detail)** to name the shades behind a slice (ballet pink,
lipstick red, butter), and the **Overview** tab for each house's neutral
share. Check every palette sums to 100 before building. Watch for shades
filed under an unexpected family (Paris filed butter under white/cream,
not yellow) and say so in the prose.

**Donuts, locked spec (Carmen's "DFB colour-palette donut").** Built by
`scripts/build_donuts.py` + `scripts/render_donuts.js`, which implement it
exactly:
- Ring width 42% of the radius (hole 58%), square canvas, transparent
  background, outer radius 405 on an 810 box.
- Largest wedge starts at 12 o'clock, clockwise, largest to smallest,
  whole-number %s, wedge colour is the family's hex, no gaps.
- Wedges with WCAG luminance > 0.82 get a 1.2px `#D0CCC5` outline.
- Labels: only the %, at the wedge's angular midpoint at 79% of the radius,
  42px if >= 15%, 32px if >= 8%, 24px otherwise (20px allowed for 1 to 2%),
  white if luminance < 0.55 else black, font Arimo/Arial (Canva's default
  sans). A label that doesn't fit its arc is left off.
- 0% slices are dropped. No names, no legend, no title on the donut.
- If Carmen wants it native in Canva, the same geometry is in her guide:
  1080 x 1350 page, 810 x 810 box at top 270 left 135, one SVG path per
  wedge, brand line, title "Colour palette", footnote on what % means.

**House grid and swatch grid** (`scripts/build_grids.py` +
`scripts/render_grids.js`), white background, same type style as the bar
charts (bold Playfair title, Century Gothic subtitle and source line,
house names in italic Playfair):
- House donut grid in **rows of 4**, delivered as one full image and as two
  halves of 8 (easier in Substack). Render at 2x, not 1x (1x looked low
  quality) and not 3x (files got too big).
- Swatch grid: a season-average row on top, then one row per house, top
  five colours in the same order as its donut, % inside each block. Print
  slices carry a small "floral print" / "graphic print" tag, because their
  blended hex otherwise reads as a plain colour.

**Every chart says what its numbers measure**, in the subtitle: "% =
share of each house's total colour on the runway", "% of each house's
colour palette that is pink, vs the season average". Never a bare %.

**Deep dive.** For each main colour, list houses at 1.5x the season
average or more, then check the named shades: two houses can lead the
same family with different colours (Paris: Isabel Marant's pale pink vs
Valentino's fuchsia, Lacoste's khaki vs Loewe's jade), and that is usually
the more interesting sentence. When press coverage names a palette, compare
it to the data and say where they disagree (Paris: Miu Miu reviews named
navy but not brown, which was 20% of its palette).

**Keep in sync with the trend report** for the same season: neutral share,
the lead colours, the pink/green/red house numbers. Grep both drafts.

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

## Closing deliverables, every piece

Once the text and every chart are finalized and approved, the piece
isn't done until three more things are handed over, without being
asked each time:

1. **Meta description / alt text for every chart and image** in the
   piece, one per visual (the season donut, every per-house donut, the
   swatch grid, and anything else visual).
2. **Tags for the Substack post.**
3. **An SEO meta description for the article** (roughly 150 to 160
   characters, no em or en dashes, no decimal percentages, no
   AI-coded phrasing, same as everywhere else in the piece).
