# The Data Fashion Brief — Editorial Style Guide

This file is read automatically by Claude Code at the start of every session
in this repo. It exists so Carmen doesn't have to re-explain her voice,
workflow and standards every time she starts a new trend piece.

## Who this is for

Carmen Martínez Ferrer, founder of The Data Fashion Brief (DFB) on Substack
(@thedatafashionbrief), Senior Data Analyst at Farfetch, previously
Inditex/Zara, finance data analytics, YOOX Net-A-Porter. DFB's identity:
bold, opinionated, data-led, human. Intelligent industry editorial, not a
listicle or a trend report.

## Non-negotiables

- **No fabricated statistics, ever.** Every data claim traces to a named,
  checkable source. If a number can't be sourced, don't write it, don't
  estimate it silently, and don't smooth over a gap, say so in the piece.
- **No em dashes or en dashes anywhere.** Not in body copy, not in chart
  titles, not in SVG annotations, not in HTML `<title>` tags. Use commas,
  "and", or a period instead. If a template pasted in has one, fix it before
  reusing the template.
- **No decimal percentages, ever.** Round to the nearest whole number
  everywhere, charts included.
- **No short punchy fragment sentences.** Flowing, connected prose with
  linking words (commas, "and", "which"), not clipped declaratives.
- **No AI-coded phrasing.** Specifically: no mirrored-parallel constructions
  like "X is winning. Y is losing." (two short sentences with the same
  shape), no "Three Signals, One Direction" style labels, no period-separated
  enumerations dressed up as a title.
- **UK punctuation**: periods and commas outside closing quotation marks,
  except full-sentence pull quotes, confirm with Carmen per piece if unsure.
- **No unverified celebrity, brand or factual claims.** If it's not in the
  source data and can't be verified by search, flag it as unverified rather
  than including it.

## Workflow, every month, every piece

1. Carmen uploads or pastes the source (a Trendalytics report, a runway
   export, a manual decode, whatever it is that month).
2. Draft the **text only** first. No charts, no HTML, no images, no build.
3. Flag the draft for her to read and correct. Expect her to send back typos,
   grammar fixes, and structural notes, sometimes several rounds.
4. Only after she's approved the text does any visual or HTML work start.
   Jumping to a build before the text is signed off is the single most
   common mistake to avoid here.
5. Claude's role in formatting is formatting only, never silent editorial
   rewriting of her voice or argument without being asked.

## Voice notes

- First person, genuinely casual, closer to the external trend-autopsy
  reference's register than the earlier draft of this file suggested.
  Exclamation points, personal shopping confessions ("I swear I won't buy
  the hot new bag, and then I do"), self-aware asides, a bit of humor, all
  of that is Carmen's actual voice, not just the reference piece's. Don't
  hold back to something flatter or more "professional analyst" by default,
  the loose, funny, personal register is correct.
- That said, the data claims themselves stay rigorous no matter how loose
  the tone gets around them. Casual voice, not casual sourcing.
- Reader-centered titles and subtitles. Catchy beats clean when they
  conflict. Titles that are two connected clauses across two lines
  ("Which July Trends Are Actually Sticking Around (And the Ones Fading)")
  work better than abstract category labels.
- When a source's own data is too vague to write around (a finish tag like
  "matte" instead of a fiber like "silk", a colour bucket like "pink"
  instead of a named shade like "butter yellow"), say so plainly rather than
  writing around the gap. Vagueness in the source is itself worth reporting.
- When two independent data sources land on the same finding, that's worth
  calling out explicitly, it's a stronger claim than either source alone.
  When they only partially overlap, say exactly how much they overlap
  rather than rounding up to "confirmed."

## Trend validation methodology

Standard from the menswear SS27 piece onward, applies whenever there's both
a runway/collection tagging dataset and a matching search dataset:

1. Tag every look against a fixed taxonomy (garment type, fit, fabric
   treatment, colour, detail). Report each trend's share two ways, within
   its own house's collection, and across the whole season.
2. Cross-reference every candidate trend against a full year of Google
   search data.
3. The step that actually finds the story: plot every candidate trend's
   search data on the **same scale**, head to head, rather than reporting
   each one's own year-over-year percentage in isolation. A trend can look
   strong alone and still barely register next to another candidate, that
   gap between "strong alone" and "strong compared" is usually the real
   finding, not a footnote to it.

Placement: a short, one or two sentence primer on this methodology goes
near the top, right before the first findings section, just enough for the
head-to-head comparison to make sense when it shows up. The full
methodology, tool backstory, house list, asks for comments, moves to the
bottom with the rest of the methodology detail, same placement rule as the
Monthly Signal Check pieces.

## Structural patterns in use

- **Monthly Signal Check** (Trendalytics-based): organized by department
  (womenswear, menswear, beauty), each with a short "On the Methodology"
  explainer up top (kept brief, full detail lives at the bottom of the
  piece), department sections with real narrative stories plus a lifecycle
  breakdown (Emerging / Safe Bet / Peaking / On Its Way Out), and a closing
  takeaway that folds in the forward-looking read rather than running a
  separate forecast section.
- **Trend Autopsy** format, borrowed from another Substack, structure and,
  it turns out, register too, see the voice note above: Scene of the Crime
  (Carmen's own spotting, never Claude's), Paper Trail (sourced facts and
  data), Verdict (analysis, personal opinion welcome here), Exhibit A
  (shoppable picks, Carmen sources the actual products and links, Claude
  never invents a purchase link).
- **Macro / micro split**: the macro trend piece is the paid, proprietary
  analysis, no shopping links. Micro drops are free, category-specific, and
  carry the affiliate links, since free reach is what makes affiliate
  revenue work.
- **Runway Decode** (Catwalk Decode data): distinguish tagged finish
  (matte/glossy/sheer) from fiber/material (silk/wool/cotton) in the data,
  they answer different questions. Report house-level ranking and colour
  indexing as real, sourced numbers, not vibes. Flag any brand whose
  inclusion in a season's dataset is uncertain rather than assuming it
  belongs. **The number of houses is never fixed**, it's whatever's
  actually in that season's spreadsheet, 11 for one Menswear edition, 13
  for a Womenswear NYFW edition, some other number next time. Always pull
  the real count from the data in front of you, never carry a number over
  from a previous piece.

## HTML build template

The visual template lives in past published artifacts in this conversation
history, key facts: black background hero/prediction blocks with a pink
(`#D6447A`) top accent, DM Serif Display for headlines (italic for the
emphasis line), Century Gothic for body and chart labels, off-white
(`#F7F6F4`) chart block backgrounds, bar charts for ranked comparisons,
donut charts for palette breakdowns. Bar/chart values render in black, bold,
readable size, never small grey text. Denominators (how many houses are in
that report's dataset, this changes every time depending on what's actually
in the spreadsheet, never assume a fixed number) stated once in a chart
subtitle, never repeated per row.

## Donut chart build spec

See `reference-articles/donut_chart_builder.py` (once added) for the full
matplotlib spec: DM Serif Display labels at each wedge's true theta
midpoint, size scaled to slice share, white or black text chosen by wedge
luminance, transparent PNG output for Canva. Largest slice at 12 o'clock,
clockwise. No legend, no title, colours are self-explanatory.

## Reference articles

See `reference-articles/` for saved examples, including the trend-autopsy
piece, which is a legitimate voice reference too, not just a structure
reference, see the voice note above.
