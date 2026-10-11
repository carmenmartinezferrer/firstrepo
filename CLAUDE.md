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

6. Every time a draft or new version of any piece is handed over, end it
   with a bullet-point list of every source used in the piece, each with
   its link (Carmen's standing request). Her own uploads and DFB's
   unpublished data are listed too, marked "no public link".

7. Reels scripts also go into a Google Doc in Carmen's Drive, always in
   the **DFB > Reels** folder (see `.claude/skills/dfb-reels`).

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
- Real press coverage belongs in every piece where it's genuinely relevant,
  not just as colour but as an honest check: does the raw season number
  and what the industry is actually saying line up, or is a modest season
  average hiding a concentrated story at a few specific houses (the red
  colour finding in the NYFW piece is the reference case, 9% season-wide
  read as safe until two houses at double that average explained why the
  press was calling it a real story). Say which it is, don't just quote
  the coverage alongside the number and leave the reader to reconcile them.

## Source-data consistency across pieces

When a season's underlying data changes (a corrected palette, a house
added or removed, a rebuilt metric), every piece drawing on that same
season needs the same check, not just the piece the correction started
in. This has actually gone wrong once: the NYFW Colour Index season
palette was corrected first, and the NYFW Trend Report's own colour
section kept citing the old numbers for several more turns until Carmen
caught it by eye. Before calling any piece finished, grep the other
pieces sharing that dataset for the same figures, don't assume a fix in
one place propagated.

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

Chart build: an SVG line chart, both series plotted on the same 0 to 100
scale (Google Trends' own scale, no rescaling needed), pink for the piece's
lead trend, black for the comparison, light dashed gridlines at 0/50/100,
month tick labels along the x-axis, a one-line chart-note stating the
concrete finding (e.g. "X runs higher than Y in N of the last M weeks").
Confirmed working for both the menswear SS27 piece and the NYFW SS27 piece.
Where an alignment score or ranking is built from real per-item data
(spreadsheet columns, not estimates), prefer combining a couple of the
season's actual biggest silhouette and material signals into one simple
average over relying on a single category, and say plainly in the
methodology section exactly which categories feed the score, since that
composition can and does change piece to piece as the season's real
headline findings become clearer through drafts.

**Do not mix broad-baseline and narrow-baseline signals in one unweighted
average.** A fabric-finish category like matte or sheer sits at 60 to 90%
for most houses, while a specific named trend (a silhouette, a garment
detail) sits at single digits to maybe 25%. Averaged together with equal
weight, the broad category alone decides almost the whole score, the
narrow ones barely move it, which quietly turns a "several trends
combined" score back into a single-category ranking wearing a bigger
number. This happened in the NYFW piece: adding matte and sheer into the
same average as wide-leg trouser, midi skirt and the smaller silhouettes
buried a house (Khaite) that was genuinely strong on the named trends
because its matte share was low. The fix was dropping the broad
fabric-finish categories and scoring only the specific named trends,
which sit on a comparable scale to each other. Before combining any
signals into one average, sanity-check their natural ranges are actually
comparable, not just their labels.

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
  from a previous piece. Two Claude Code skills capture the build logic
  for this pattern in full: `.claude/skills/runway-decode-trends` (materials,
  silhouettes, search validation, the alignment matrix) and
  `.claude/skills/runway-decode-colour` (season palette, per-house donuts,
  swatch grid, the colour deep dive), each with reusable chart-building
  scripts. Use them rather than re-deriving the matrix/donut pixel math
  from scratch, that's exactly the kind of thing that went wrong more
  than once before they existed.
- **"Stop Calling Everything a Trend"** is the recurring series title, not
  a structural format on its own. It gets reused across whatever the
  underlying data source is that month, a Pinterest report, Trendalytics,
  a Runway Decode export, always paired with an edition name (e.g. "NYFW
  Edition"). Don't confuse it with the piece's actual structure, which
  still follows whichever pattern above actually fits the data.
- **Personal Essay** (no data, no charts): career reflections, learnings
  from a fashion week, a personal take on the industry. Not every piece
  is a data piece, the non-negotiables about not fabricating facts and
  not writing short punchy fragments still apply, but there's no
  taxonomy, no tagging, no methodology section, personal opinion is the
  whole point rather than something a chart earns the right to include.
  `.claude/skills/dfb-personal-essay` captures the build logic, which
  references point to use for voice versus structure.

- **Runway Colour Combos** (Instagram carousel series): single runway looks
  broken into their two or three most striking colours, "chip + chip = the
  look", model cutouts, Pantone-style swatch cards with photo-sampled hex
  codes, and a closing Google search slide. `.claude/skills/runway-colour-combos`
  holds the build logic and scripts (cutout, colour sampling, swatch cards,
  search change).

- **FashionUnited article** (trade publication, not Substack): DFB data
  rewritten as neutral, news-led trade journalism, third person, DFB
  cited as a source, licensed images only (PR, AFP, Launchmetrics).
  `.claude/skills/fashionunited-article` holds the editor's standing
  feedback and the structure, the published quiet luxury piece in
  `reference-articles/` is the reference.

## HTML build template

The visual template lives in past published artifacts in this conversation
history, key facts: black background hero/prediction blocks with a pink
(`#D6447A`) top accent, DM Serif Display for headlines (italic for the
emphasis line), Century Gothic for body and chart labels, off-white
(`#F7F6F4`) chart block backgrounds, bar charts for ranked comparisons,
donut charts for palette breakdowns. Bar/chart labels and values render dark
(around `#222`, not pure black), readable size, medium weight (500 for
values, 400 for labels), never bold and never light grey. Bold black was
tried and came back too heavy, light grey was tried first and came back too
faint, `#222` at medium weight is the settled answer. Denominators (how
many houses are in that report's dataset) don't belong in charts at all,
not even once per subtitle, that was tried and reversed. State the house
count once in the body prose (the methodology section is the natural spot)
and keep every chart title and subtitle free of house-count numbers
entirely.

**Every chart says what its numbers measure.** A bare "44%" is never enough: the subtitle (or an axis
note) must state the unit in plain words, e.g. "% of houses that showed each piece at least once",
"% of all looks that include each material", "% of each house's colour palette", "18x = 18 times
more often than normal". Interpretive lines ("tweed is mostly Chanel") go in the title or the prose,
never in place of the unit. Carmen asked for this explicitly on the Paris SS27 charts.

**"In The Press" callouts**: a distinct off-white block, thin pink left
border, small pink uppercase label ("In The Press") above the paragraph,
sits right after the prose finding it backs up, not bundled into the main
paragraph. Every claim inside one needs a real link. Use it for the
industry-resonance check described in the voice notes above.

**Two-axis matrix charts** (trend alignment against colour intensity, or
any similar two-variable comparison): split into four real quadrants at
whatever point actually divides the season roughly in half on each axis,
not a round number for its own sake. Scale each axis to the metric's own
actual min and max, not an assumed 0 to 100, a narrow-range metric (a
composite score that only spans single digits to twenty-something,
say) plotted on an assumed full scale crushes all the real variation into
one corner of the chart. Shade each quadrant faintly and give
it a real descriptive label (e.g. "Season-Led, Colour-Forward"), and colour
each dot by which quadrant it falls into. Do not colour dots by a single
axis alone (e.g. above/below the midpoint on just one variable), that
repeats information the dot's position already shows rather than adding a
second dimension.

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
