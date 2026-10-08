---
name: runway-decode-trends
description: >
  Build a Runway Decode Trend Report for The Data Fashion Brief (materials,
  silhouettes, a search-validated head-to-head comparison, and a
  trend-alignment-vs-colour-intensity matrix), from a runway tagging
  spreadsheet plus Carmen's own manual material decode. Use this whenever
  Carmen uploads or references a runway/collection tagging export (a
  Catwalk Decode or similar per-item spreadsheet with columns like Look,
  Piece, Type, Fit, Fabric Treatment, Colour) and wants a trend report,
  materials/silhouettes writeup, or "what actually held up" piece built
  from it, even if she just says "give me the trend report" or pastes a
  new season's data without naming this skill directly. Also trigger if
  she asks to rebuild, extend, or fix the alignment matrix, add a search
  comparison chart, or find real house names behind a silhouette/material
  count on an existing Runway Decode Trend Report piece. Also trigger
  when she sends runway photos to fill the Canva look-collage template
  (the "PFW pics" design, six looks each labelled trend and designer),
  even if she just says "put these in the collage" or "fill the
  imagery for the article".
---

# Runway Decode Trend Report

Builds the trend-report half of a Runway Decode pair (the other half is
`runway-decode-colour`, the colour-only piece). Read the repo root
`CLAUDE.md` first, every non-negotiable, voice note, and HTML template
rule there applies here without exception, this skill only adds the
format-specific structure and chart logic on top of it.

Reference implementation: the NYFW SS27 piece, "Stop Calling Everything a
Trend: NYFW Edition." If you want to see a finished example before
building, that piece (and the session that built it) is the ground truth
this skill was extracted from.

## Voice, in practice

CLAUDE.md's voice notes describe the register, this is what it actually
looks like on the page. **Read
`reference-articles/nyfw-ss27-trend-report-final.md` before drafting text
for this piece type**, it's Carmen's own final, approved copy for this
exact format, not a structure-only reference, match its register
directly. A few tics worth noticing there:

- A mid-section pivot before getting specific: "Ok, ok… silk is the most
  dominant, but in what shape, what form, what is made of silk?" Stating
  the headline finding, then immediately undercutting its own vagueness
  before drilling in, rather than just listing the specifics cold.
- Rhetorical questions as subheads: "The slip dress and midi skirt
  comparison: which one wins?" A section title can ask the question the
  section then complicates or half-answers.
- Naming and linking her own past pieces inline, as a personal thread
  through the newsletter, not just an external citation.
- A short, plain sentence flagging what's deliberately out of scope
  rather than pretending the piece is total: "Anyway, I will post a
  specific post about colour." Don't pad out a section to look complete,
  say what's coming later instead.
- Ending on a direct question to the reader, before the standard sign-off
  block, not just a closing summary line.
- Stretched-word emphasis ("biiiiig") used sparingly, maybe once a piece,
  not a running tic.

A second file, `reference-articles/external-trend-autopsy-format-example.md`,
is a different Substack's piece, saved originally for a different format
(Trend Autopsy: Scene of the Crime / Paper Trail / Verdict / Exhibit A,
not this one). Don't borrow its structure for a Runway Decode piece, but
CLAUDE.md's voice notes confirm it's a legitimate voice reference too,
the same casual, personal, funny register applies here. If the NYFW
reference above ever feels thin for a particular passage, that file is
the second place to check the register against, voice only, not shape.
This same reference file is also the tone anchor for `runway-decode-colour`,
both pieces should read like the same person wrote them on the same day.

## Standard from Paris SS27 onward (overrides older structure below where they differ)

Carmen set these on the Paris SS27 piece. Apply them every time.

**The workbook (multi-tab Catwalk Decode export).** If it has a `Read me`
tab, read it first. Use the tabs in this order:
1. **Trends** is the main tab for every "% of looks" and "how many
   houses" claim (filter `Level` = fashion week for the season,
   `Level` = house for one show, then filter `Category`).
2. **Colour mix donut** for every colour number (never the Dominant
   colour donut, which only exists to compare with Instagram decodes).
3. **Over-index** for an "unexpected pairings" section (see below).
4. **Garments** only for piece-level questions ("what fabric were the
   pencil skirts made in") and for naming which houses sit behind a
   number. Never use it for a % of looks.
Fiber-level materials are now in the data itself, so no separate manual
material decode is needed unless Carmen supplies one.

**Three ranked sections, each charted.** All ranked by share of looks:
1. **Materials** (`Category` = material): a top 10 chart, then a "next
   five" chart (ranks 11 to 15).
2. **Silhouettes by piece** (`Category` = garment): a top 10 chart, then
   a "next five" chart.
3. **Silhouettes by shape** (`Category` = silhouette): a top 10 chart,
   plus a "next five" only if five more shapes with real share exist.
Leave catch-all tags ("other", "skirt: other", "top: other") out of the
rankings. Garment labels keep their noun ("straight trouser", "bermuda
shorts", "trench coat", not "straight", "bermuda", "trench"). Flag vague
tags in the prose ("cotton (unspecified)" can be the second biggest
material and the source can't say what kind, say so).

**Don't reuse the previous piece's framing.** Rank the real data first and
write the headline from that. Paris almost repeated NYFW's "silk went
everywhere" line when the data said wool led and silk was a clear second.

**Group pieces only when the grouping is a real story, and say it's
yours.** Example: lingerie-style tops (bandeau, corset/bustier, crop top,
bodysuit, camisole, plus "bra" in outfit descriptions, because bras are not
a separate garment type) added up to 12% of Paris looks while each piece
alone was 2 to 3%. State the grouping in the methodology and flag any
known undercount.

**Unexpected pairings section (Over-index tab).** Index / 100 = "N times
more often than normal". Only pairings on 4+ pieces. Drop the obvious ones
(corsetry on a corset, bubble hem on a bubble skirt). Split into "crossed
houses" (2+ houses) and "pure house signature" (one house), and use
Garments to name the houses. Chart the crossed-houses ones.

**Chart style (replaces the off-white blocks for bar charts).** White
background, vertical bars, dark grey (`#3A3A3A`) with one pink (`#D6447A`)
highlight bar, title in bold Playfair Display (lowercase, catchy),
subtitle and labels in Century Gothic (Questrial as the free fallback
when rendering), percentages in Century Gothic (not italic serif), source
line at the bottom, bars close together, label text big (titles about
56px, labels 25px, values about 40px on a 1000px canvas, widen the canvas
rather than shrink text when there are 8 or more bars so labels never
touch). Render PNG at 2x with Playwright, Chromium is preinstalled.
Reference implementation: `scripts/build_bar_charts_paris_ss27.py` +
`scripts/render_png.js` (the Paris-specific chart list is at the bottom of
that script, the `bar_chart()` function and label wrapping are reusable).

**Every chart says what its number measures**, in the subtitle, in plain
words: "% of all Paris looks that include each material", "% of houses
that showed each piece at least once", "% of each house's colour palette
that is pink, vs the season average", "18x = 18 times more often than
normal". A bare "44%" is never enough. Interpretive lines go in the title
or the prose, never in place of the unit.

**Draft markers name the chart file and its unit**, e.g.
`[CHART: 10-top-materials.png, % of all Paris looks that include each material]`.

## Before you start

Confirm with Carmen, don't assume:
- **How many houses, and which ones.** Never carry a count over from a
  previous piece. Pull it from the actual spreadsheet in front of you.
  If a house's inclusion looks uncertain (wrong season, a name that
  doesn't match the rest of the dataset, a sheet that looks like a
  different market), flag it and ask before including or excluding it.
  This happened repeatedly in the reference session (Cos turned out to be
  Fall 2026 London, not the season being analysed) and it will happen
  again with other datasets.
- **What material data exists, and where.** The spreadsheet's own Fabric
  Treatment column is usually a *finish* (matte, glossy, sheer, textured,
  opaque), not a *fiber* (silk, wool, cotton, cashmere). If Carmen wants
  fiber-level material findings, that almost always comes from a separate
  manual decode she provides, not the spreadsheet, and it may not cover
  every house. Say plainly which houses are missing from a fiber-level
  chart rather than filling the gap with the spreadsheet's finish data.

## Structure

1. **Hero**: title and subtitle in Carmen's voice (see CLAUDE.md's voice
   notes, catchy over clean, two connected clauses across two lines
   beats an abstract label). If this is a "Stop Calling Everything a
   Trend" edition, the title is `Stop Calling Everything a Trend: <Edition>`.
2. **Methodology primer**: one short paragraph, right after the hero,
   before the first findings section. States the tagging approach in one
   or two sentences. The full methodology detail goes at the very bottom,
   see CLAUDE.md's Trend validation methodology section for the exact
   placement rule.
3. **Materials** (from Paris SS27: top 10 + next five by share of looks,
   see the standard above; the older version was) a house-presence bar chart (share of houses featuring
   each material), a wool-or-equivalent by-weave breakdown, and an
   "In The Press" callout that gets specific about *what shape* the
   season's lead material actually takes (a garment, an accessory, a
   detail), not just naming the fiber again. See CLAUDE.md's "In The
   Press" callout spec for the exact box styling.
4. **Silhouettes** (from Paris SS27: by piece and by shape, top 10 + next
   five each, see the standard above; the older version was) a share-of-houses bar chart, an "In The Press"
   callout, and a smaller-silhouettes chart for trends too small for the
   main chart but real (2+ houses). For the smaller-silhouettes chart,
   pull the actual house names for each entry straight from the
   spreadsheet's Type/Piece columns, the same way you'd compute any other
   share, never guess or leave a "(put houses here)" placeholder. Exact
   type matching matters, "denim jacket" and "oversized denim jacket" are
   different Type values and will give you different house lists.
5. **Search validation** (only if Carmen has provided Google Trends CSVs,
   don't fabricate this layer if she hasn't): use
   `scripts/build_search_line_chart.py` to build the head-to-head line
   chart, both trends on the Trends' own 0-100 scale. This is the "same
   scale, head to head" step from CLAUDE.md's Trend validation
   methodology, the whole point is that a trend which looks strong alone
   can barely register next to another, or a trend that's the bigger
   *runway* number can be the smaller *search* number, and that gap is
   usually the actual finding. Write the finding honestly: if runway and
   search data disagree, say they disagree, don't paper over it by
   claiming they "tell the same story" when the numbers show otherwise.
6. **Colour** (brief, one paragraph): the season's colour-weight headline
   only, the full per-house breakdown belongs in the `runway-decode-colour`
   piece, not duplicated here. If a raw season-wide colour average looks
   "safe" while a couple of houses build a much larger share of their own
   palette around it, that's usually the real story, say so, see CLAUDE.md's
   voice note on this exact pattern (the NYFW red finding is the reference
   case: 9% season-wide, but two houses at 12 and 16%, which is what real
   press coverage was actually responding to).
7. **The trend alignment matrix**: use `scripts/build_matrix_svg.py`.
   Read the docstring in that script before building this chart, it
   explains the two failure modes already hit once in the reference
   session:
   - Averaging a broad fabric-finish category (60-90% baseline for most
     houses) into the same score as specific named trends (single digits
     to ~25%) lets the broad category dominate and silently turns a
     "several trends combined" score back into a single-category ranking.
     Score alignment only from signals on a comparable scale, specific
     named silhouettes and garment details, not fabric finishes.
   - Each axis rescales to its own actual min/max, never an assumed
     0-100, and the quadrant threshold on each axis is wherever the real
     data actually splits roughly in half, not a round number.
   Use the script's returned `groups` dict to write the chart-note and
   the findings paragraph, don't hand-write the quadrant membership from
   memory, that's exactly how the reference session ended up with text
   contradicting the chart at one point.
8. **Takeaway**: the closing black block, folds the forward-looking read
   in rather than running a separate forecast section (see CLAUDE.md's
   Monthly Signal Check pattern, same rule applies here).
9. **Methodology footer**: full detail, house list, which chart used
   which formula and why, whether the search-validation layer has been
   run and for which trends specifically. If the alignment formula
   changes between drafts (it likely will, more than once, this happened
   three times in the reference session), say so plainly rather than
   silently overwriting the description of an earlier version.

## Article imagery: the Canva look collage

The runway photos that run in the piece go into a fixed Canva template,
six looks, each with a pink label giving the trend and the designer.
Read `canva-look-collage.md` in this folder before touching it, it has
the template ID, the slot map, the label format, and the rule that the
designer is never guessed from the clothes. Like every visual step, it
starts only once the text is approved.

## House-count rule

Per CLAUDE.md: house-count denominators don't belong in any chart title
or subtitle, not even once. State the count once in prose, the
methodology section is the natural spot.

## Closing deliverables, every piece

Once the text and every chart are finalized and approved, the piece
isn't done until three more things are handed over, without being
asked each time:

1. **Meta description / alt text for every chart and image** in the
   piece, one per visual.
2. **Tags for the Substack post.**
3. **An SEO meta description for the article** (roughly 150 to 160
   characters, no em or en dashes, no decimal percentages, no
   AI-coded phrasing, same as everywhere else in the piece).

If the Canva look collage was built, its alt text belongs in item 1.
