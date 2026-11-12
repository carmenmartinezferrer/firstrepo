---
name: trendalytics-forecast-decode
description: >
  Turn a Trendalytics forecast report (the Womenswear Forecast PDF, a
  seasonal colour or trend report, any Trendalytics export where every
  item arrives with one data point) into The Data Fashion Brief's "Stop
  Calling Everything a Trend, Forecast Edition": a trends piece, a colour
  piece, or both, with charts, an Instagram carousel and Reels. Use this
  whenever Carmen uploads or pastes a Trendalytics report, forecast PDF or
  "the FW27 forecast" and wants an article, charts or posts from it, even
  if she doesn't name the tool ("here's the forecast for next autumn, do
  the article", "the colour part of the Trendalytics report", "what does
  the forecast say about fabrics"). Not for her own runway tagging
  spreadsheets: those are `runway-decode-trends` and
  `runway-decode-colour`, which this skill borrows chart code from.
---

# Trendalytics forecast decode

The forecast equivalents of the two Runway Decode skills. Same voice, same
chart style, same non-negotiables (read the repo root `CLAUDE.md` first),
but the input is a **report someone else made**, not Carmen's own tagging,
so the job is different: explain where the report's numbers come from,
put them on one scale a reader can compare, add Carmen's own Google
Trends pulls where the report leaves gaps, and check the report against
her runway dataset and the press.

Reference implementation: the FW27 pair, `drafts/fw27-forecast-trendalytics-draft.md`
(trends, 24 items) and `drafts/fw27-forecast-colour-draft.md` (colour, 12
colours), with charts in `drafts/fw27-forecast-charts/`, the carousel in
`drafts/fw27-forecast-instagram/` and the Reels in `drafts/fw27-forecast-reels.md`.
Carmen approved the final texts of both, so they are the register to match.

## Which piece(s)

Decide with Carmen at the start, from what the report contains:

- **Report has colours and trends** (the seasonal Womenswear Forecast does:
  three aesthetics, each with colours, fabrics or prints, runway references
  and key items): **two separate Substack pieces**, one for the trends, one
  for the colours, each pointing to the other. Carmen chose this on FW27
  ("one article for trends and another for colours"), a single combined
  piece got too long.
- **Colours only**: the colour piece alone, built with the colour steps below.
- **Trends only**: the trends piece alone.

Both pieces carry the series title "Stop Calling Everything a Trend" plus
an edition name ("Fall/Winter 2027 Forecast Edition", "Fall/Winter 2027
Colour Edition").

## Step 1: read the report properly

1. `pdftotext -layout report.pdf out.txt` for the text and
   `pdfimages -png report.pdf images/img` for the pictures (keep the
   images for reference, their rights are not cleared for publishing, say
   so in the notes).
2. Build the item table: every named item with its exact printed data
   point, the aesthetic it belongs to, and the kind of number it is. On
   FW27 there were six kinds: search volume ("extreme" 78k), change in
   searches on last year, change in market adoption on last year, TikTok
   views (sometimes a weekly rate), growth among key influencers, and a
   "most saturated in luxury" label with no number at all. **No item gets
   more than one number**, which is the central problem of the piece.
3. Sample hex codes from the report's own colour swatches (render the
   page at 150dpi, average a 40px block at each swatch centre). Note the
   report's colour names; Carmen may rename one (FW27: "russet red"
   became "dark red" because that's what people search), and once she
   does, every chart, slide and caption uses her name.

## Step 2: explain where the numbers come from

Readers (and Carmen, the first time) don't know what "up 21% in market
adoption to LY" means, so both pieces carry a short explanation near the
top and a fuller one at the bottom. The wording Carmen approved:

> Trendalytics is a trend intelligence platform that pulls demand data
> from across the internet, Google searches, TikTok, Instagram and
> Pinterest, plus what retailers actually have on their shelves, and
> combines it all into one view per colour or item. From there it looks
> for patterns: how big the search volume is right now, how fast it is
> growing or declining, and how that compares with the same point last
> year, and it then cross-references the data with what is actually being
> said about the colour, in the press, on blogs, on Reddit, as a second
> layer. What lands in the report, though, is one number per colour.

Glossary for the full methodology: search volume (absolute, period and
country not stated, say so), change in searches on last year, market
adoption (how many retailers carry an item compared with last year),
TikTok views, growth among key influencers (its tracked panel), the
luxury-saturation label (no number). Always add that the method is
described as Trendalytics presents it and the report prints only the
final figures, because the PDF itself has no methodology page.

**Name Trendalytics once in the intro and once in the methodology.** Not
in every paragraph, not in chart titles or subtitles, not as "the
forecast" or "the forecaster" on charts either. Carmen asked for this
twice. The caption of an Instagram post credits it once at the end.

## Step 3: trends piece

Structure (see the FW27 draft): hero title and subtitle, Carmen's intro,
"Methodology, the short version", one section per aesthetic with the
report's reasoning for the aesthetic in her words, the key items and
fabrics with their numbers, then the same-scale sections, the Paris
cross-check, the takeaway, full methodology, sources.

The same-scale rule from `runway-decode-trends` applies with a twist:
items can only be compared with items that share a metric, so **group the
items by metric and plot each group on one scale** (search growth chart,
market adoption chart), plus one chart that shows the metric mix itself
(how many items carry each kind of number), because the mix is a finding:
it tells the reader how little of the report is actually comparable. Do
not build the alignment matrix for a forecast piece, Carmen said no.

Cross-check against the dfb-data runway dataset (`dfb-dataset` skill,
`build/<season>/<city>.xlsx`): which forecast items the previous season's
runway already showed, as a share of all looks, with the real house
names. State plainly that it is a different season, so it shows what the
runway can already see, not whether the forecast is right.

## Step 4: colour piece

Built with the `runway-decode-colour` chart code where it fits, but the
structure is the forecast's:

1. Carmen's intro (she wrote the FW27 one herself, keep hers word for word
   when she gives one).
2. Short methodology with the Trendalytics explanation above.
3. **One section per palette, and each must say why the palette is called
   that**: the reasoning behind the aesthetic (quiet luxury growing up,
   dressing in things you can feel, gorpcore growing up and bringing an
   umbrella), in Carmen's words, from her notes or the report's. She
   rejected a draft that listed colours without this context.
4. **Colours in percentages, never raw volumes or view counts in the
   body.** "35K searches" and "196M views" tell the reader nothing. Use
   share of combined searches for the volume colours, % change on last
   year for the growth colours, and ask Carmen for her own Google Trends
   year-on-year pull for every colour so all of them sit on one scale
   (she supplied all twelve on FW27). TikTok views only as context in
   prose, never on a chart.
5. "Same scale" section: all colours on one growth chart, each bar in its
   own hex, plus the share donut for the volume colours.
6. In The Press callouts where the industry is already talking about a
   colour (WGSN and Coloro key colours, Who What Wear, Coveteur), every
   claim linked.
7. Runway cross-check: the previous season's palette from the dataset
   (season donut, the houses already wearing the forecast colours), with a
   family-match caveat (plum and lilac both count as purple).
8. Takeaway, full methodology, sources.

Charts (`scripts/build_charts.py`, `scripts/build_visuals.py`,
`scripts/render_cards.js`, all copied from the FW27 build, adapt the
data tables at the top):
- Twelve-colour growth bars, each bar its own colour, ranked.
- Share-of-searches donut (DFB donut spec).
- **Palette swatch rows** (`runway-decode-colour/scripts/build_palette_rows.py`):
  one row per palette, the colours as blocks with the number inside,
  biggest mover first. Carmen loved this one; it replaced three separate
  palette cards.
- Previous-season donut and house grid from the colour skill.
- Palette card titles small (38px), 3x render, no source line on the
  chart (sources live in the piece). Drop any "what the last season
  already wore" chart that repeats the house grid.

## Step 5: the text loop

Text only first, charts after approval, as always. Expect Carmen to ask
for it shorter at least twice ("shorter without losing info"), which means
cutting repetition and the methodology detail from the top, not cutting
numbers. Keep a NOTES block at the bottom of the draft listing: numbers
she still has to confirm (a period behind a growth figure, a shade name),
placeholder links, image rights.

## Step 6: Instagram and Reels

- **Colour carousel**: the colour palette carousel type in
  `dfb-carousel` (dfb-data repo): native Canva donut, ranked bars, mood
  rings and palette swatch rows, every wedge and label editable. Copy her
  "Colour palette" design (`DAHXm5VB6sQ`), never edit it.
- **Trends carousel**: the standard dfb-carousel story format, one slide
  per metric group, PNG charts with labels left as Canva text.
- **Reels**: `dfb-reels`, one Reel per piece, saved to Google Drive in
  DFB > Reels. The colour Reel is built on the one-scale growth story.
- Captions (`scripts/build_slides.py` has the FW27 pair): source credited
  once at the end, never on the slides.

## Step 7: the per-aesthetic carousels (one per mood, posted through the week)

Built for FW27 after the first five-trend carousel: Carmen asked for one
carousel per aesthetic, in the format of her Paris SS27 trends carousel
(`DAHXUHfg7lM`), with Pinterest images, cutouts on the cover and the
template's bold runs. Final versions: Heritage Craft, retitled "craft aesthetic" on the slides at Carmen's request, same name on the cover and in every kicker, `DAHarROPkn0`,
Sensory Riot `DAHarQgNZpw`, Veiled Performance `DAHare78O1k`.

**Images.** Carmen keeps one Pinterest board per mood. Pull the board
with its RSS feed (`https://www.pinterest.com/<user>/<board-slug>.rss`,
then `i.pinimg.com/originals/...` for each pin), make a contact sheet,
pick. A single pin link (`pin.it/...`) resolves to `pinterest.co.uk`,
which the proxy blocks; fetch `https://www.pinterest.com/pin/<id>/` with
a browser user agent instead and grep the `originals` URL.

**Build.** Copy the Paris template fresh for every mood (never edit the
original), the copy keeps the same page and element IDs. Then, per page:
- Cover: `find_and_replace_text` on the title keeps its two runs; Carmen
  writes it "Stop calling everything a trend: FW27" + the mood name in
  lowercase pink. Four cutout slots sit above the photo grid; fill them
  with `scripts/cutout_outline.py` PNGs (big one left, three smaller
  across), then `layer_element` to front for the big cutout, the dark
  overlay, the title and the DFB mark, in that order. The template's old
  48px subtitle box (`LBg7sRfJc2KhcL96`) is reused as the one-line
  explanation of the mood under the title ("the mood for people who want
  clothes that look made by hand").
- Slides 2 to 6: kicker, title, four photos with their small labels, and
  the body. The body texts are multi-run (bold data lead, normal
  explanation, bold closer; slide 2 is 45px with underlined phrases), so
  rewrite them with one `find_and_replace_text` per run, never
  `replace_text`, which flattens the formatting. Widen labels to 220 and
  any title or kicker that wraps to 860.
- Slide 7 is the mood's colour bar chart, slide 8 "Comment FW27".

**Framing (Carmen's rules after three rounds).**
- Each slide is a code of the aesthetic, not a product: the title is the
  trend named the way the forecast names it ("Natural fibers, FW27",
  "Jacquard, FW27", "Embellishment, FW27"), never a description I made
  up ("Collars and lace" was rejected).
- The kicker explains the mood every time: "Heritage Craft, the handmade
  mood, code 3". The cover carries the explanation line too.
- The photos set the mood, the body names every other trend visible in
  them with its own number: the key item's forecast figure first (bold),
  then the fabrics or neighbours in the other three photos with their
  figures (Paris share, Lectra, search growth), then the closer. No
  photo on a slide without a number somewhere in the text that explains
  why it is there.
- Captions D/E/F list the five codes with one number each.

**Canva mechanics that bit.** Editing transactions expire after a few
minutes idle and die on worker restarts; open, send every page in one
go, commit immediately, and re-read the kicker of each page before
re-sending anything. `format_text` needs a `formatting` object and still
would not change the font size on the reused subtitle box, so the cover
line stays at the template's 48px; break it into two lines by hand.
Parallel edit calls do apply, but check the result before committing.

## Lessons from FW27 (don't repeat)

- Trendalytics named everywhere: strip it to intro and methodology.
- Volumes and views in the body: percentages only.
- Palette sections without the "why it's called that": always add it.
- Three palette cards when one swatch-row chart does the job.
- Pasted PNG donut in Canva: she wants to edit the chunks, build natively.
- Colour name drift between article and slides (russet red vs dark red):
  grep every output for the report's name before handing over.
- Hero `<br><em>` escaped in HTML: build the title HTML directly.
- Chart titles overflowing: width rule `max(1000, 100+n*150, 110+len(title)*31)`.
- Carousel slides whose photos don't match the text: pick photos for the
  mood, then write the body so every photo's trend has its number.
- Slide titles invented by me ('Collars and lace'): use the forecast's
  own trend names.

## Hand-over

Every draft ends with the sources list, every link, Carmen's uploads and
DFB data marked "no public link". Commit to main, push, and record Canva
links in the Instagram captions file.
