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
  count on an existing Runway Decode Trend Report piece.
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
3. **Materials**: a house-presence bar chart (share of houses featuring
   each material), a wool-or-equivalent by-weave breakdown, and an
   "In The Press" callout that gets specific about *what shape* the
   season's lead material actually takes (a garment, an accessory, a
   detail), not just naming the fiber again. See CLAUDE.md's "In The
   Press" callout spec for the exact box styling.
4. **Silhouettes**: a share-of-houses bar chart, an "In The Press"
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
