---
name: fashionunited-article
description: >
  Write or adapt a trend analysis article for FashionUnited, the
  independent B2B fashion trade publication Carmen contributes to, built
  on The Data Fashion Brief's runway and search data but written in
  FashionUnited's neutral, news-led house voice rather than DFB's
  first-person Substack register. Use this whenever Carmen mentions
  FashionUnited, "the trade piece", "the article for the editor", a
  pitch or version two for FashionUnited, or asks to turn a DFB trend
  report, colour index or Runway Decode finding into a piece for a news
  or trade outlet, even if she doesn't name the publication. Also trigger
  when she pastes editor feedback on a FashionUnited draft and wants a
  revision. If she wants the Substack version itself, that's
  `runway-decode-trends`, `runway-decode-colour` or `dfb-personal-essay`
  instead.
---

# FashionUnited Article

Turns DFB's data work into a piece FashionUnited can publish as
independent trade journalism. Read the repo root `CLAUDE.md` first: every
non-negotiable there (no fabricated statistics, no em or en dashes, no
decimal percentages, no short punchy fragments, no AI-coded mirrored
constructions, UK punctuation, no unverified claims, text before any
visuals) still applies here without exception. What changes is the
**voice and the structure**, which are FashionUnited's, not DFB's.

Reference implementation: Carmen's published quiet luxury to colour
piece, saved at `reference-articles/fashionunited-quiet-luxury-colour-published.md`.
Read it before drafting. It's the ground truth for register, section
shape, how DFB is referred to, the methodology note and the credit
lines. The data underneath usually comes from a finished DFB piece built
with `runway-decode-trends` or `runway-decode-colour`, reuse its figures
exactly, and grep that piece for every number you carry over so a
correction made there isn't missed here (CLAUDE.md's source-data
consistency rule).

## The editor's standing feedback

These came from FashionUnited's editor on the menswear SS27 bag trend
draft (version one) and are the house rules for every piece, not one-off
notes:

1. **One main focus, held throughout.** The draft moved between several
   topics and the angle got lost. Pick the single story (e.g. the
   menswear bag trend) and keep every section serving it. If the piece
   is genuinely broader (an SS27 menswear trend analysis), make that
   breadth explicit in the title, the introduction and the structure
   itself, rather than letting a narrow title sit on a wide piece.
2. **Lead with the news.** FashionUnited is a news platform, so the
   newest, most newsworthy development goes first, then a deeper
   analysis of that news, then related trends and broader context. Not
   the DFB habit of building up to the finding.
3. **No first person, no self-promotion.** No "I", no "my tool", no
   "my analysis". DFB is cited in the third person as a source, the
   same way any other source would be ("according to The Data Fashion
   Brief's analysis", "based on The Data Fashion Brief's analysis of
   Copenhagen Fashion Week SS27"). Methodology is described neutrally
   ("The Data Fashion Brief built an AI-assisted tool that..."), not
   sold.
4. **Neutral, independent language.** The editor likes Carmen's energy,
   keep the momentum and the confident argument, but strip anything that
   reads as promotional or marketing-led: no exclamation points, no
   shopping confessions, no "obsessed", no hype adjectives, no calls to
   subscribe or follow, no rhetorical question to the reader as a
   sign-off. This is the one place CLAUDE.md's loose, funny voice note
   does **not** apply.
5. **Image rights.** FashionUnited can only publish:
   - images supplied by official PR teams or the fashion houses
     themselves, with the photo credit they specify,
   - AFP images (licensed),
   - Launchmetrics runway images (subscribed), credited as
     `©Launchmetrics/spotlight`,
   - DFB's own charts, credited `The Data Fashion Brief`.

   Never suggest Instagram screenshots, Pinterest images, street style
   found online, Getty, Vogue Runway or any other unlicensed source.
   Claude doesn't source images, it lists the slots and what each should
   show, Carmen pulls them from Launchmetrics, AFP or the brand's press
   office.

6. **Every draft ends with a sources list.** Carmen's own standing rule:
   whenever a version of the article is handed over, close it with a
   bullet-point list of every source used anywhere in the piece, each
   with its link, grouped by what it backs up (runway data, search data,
   company results, press). DFB's own unpublished data and Carmen's
   uploaded files are listed too, named plainly, with "no public link"
   where there isn't one. Never drop the list because a source was
   already cited in an earlier turn.

## How it differs from the DFB version

| | DFB Substack | FashionUnited |
|---|---|---|
| Voice | first person, casual, funny | third person, neutral, analytical |
| Opening | hook, scene, personal angle | the news, stated plainly |
| Order | build-up to the finding | news, then analysis, then context |
| DFB's role | "my tool", "I tagged" | a cited source, third person |
| Methodology | primer up top, full detail at bottom | one italic note after the first chart |
| Close | question to the reader, sign-off | forward look for the industry |
| Images | anything Carmen chooses | PR, AFP, Launchmetrics, DFB charts only |
| Shopping | Exhibit A, affiliate links | none |
| Percentages | "20%" | "20 percent" |

## Structure

Follow the published reference's shape:

1. **News-led introduction** (one or two paragraphs, no heading): what
   is happening now and why it matters, with the single angle named in
   the first paragraph. Context for the reader who doesn't follow the
   trend comes in the same paragraph, briefly, as in the reference's
   quiet luxury opener, not as a separate preamble.
2. **The evidence** (sentence-case subheading, e.g. "The colour has
   evidence"): the DFB runway finding, attributed to The Data Fashion
   Brief, with named houses and their real shares. Chart slot, then the
   italic methodology note, then a runway image slot.
3. **Deeper analysis**: why this season, who else is doing it (named
   collections, dates, places, all verifiable), search data on the same
   scale where it exists, with the head-to-head finding stated
   concretely. In The Press style corroboration lives here as linked
   prose, not a DFB callout block.
4. **Related trends or broader context** (its own subheading, e.g. "A
   closer look at quiet luxury's actual customer"): earnings, consumer
   segments, historical precedent, only where it serves the main angle.
   Every company figure needs a named, checkable source (results
   release, earnings report).
5. **What this means for brands and retailers**: the closing section,
   forward-looking and practical for a B2B reader, ending on the next
   real test (the next fashion week, the next earnings season) and a
   measured read of where things stand. Hedge honestly ("a signal, not a
   verdict") when the data is one season deep.

Subheadings are sentence case, descriptive and reader-facing, never
DFB-style series labels ("Stop Calling Everything a Trend") and never
the Trend Autopsy section names.

## Title and standfirst

Propose two or three title options. News-led and specific, naming the
trend and the season or event ("Colour returns as quiet luxury fades,
Copenhagen SS27 data shows"), neutral rather than clickbait. If the
piece is broad, the title says so. Offer a one-sentence standfirst under
each title option.

## Methodology note

One italic paragraph straight after the first DFB chart, starting
`*Methodology:`, in the third person, covering: what the tool does
(AI-assisted, scans every look, tags by garment type, fit, fabric,
colour), the two ways each trend is measured (within a house, across the
season), and the full list of houses. Pull the house list and count from
the actual season's data, never from a previous piece. If search data is
used, add one sentence naming Google Trends and the period.

## Image and chart slots

In the draft, mark every visual as a bracketed slot with its caption and
credit line in the exact published format:

```
[Chart: <what it shows>]
Credits: The Data Fashion Brief

[Image: <house> SS27 ready to wear, look(s) showing <the point>]
<Caption, e.g. Jacquemus SS27, Ready to Wear>
Credits: ©Launchmetrics/spotlight
```

For brand-supplied images, write `Credits: <house>` and flag that Carmen
needs to request them from the press office and confirm the exact credit
line they want. Captions follow the same no-dash rule as body copy (the
reference's "Jacquemus SS27 - Ready to Wear" hyphen is better as a
comma). Chart titles and subtitles still carry no house counts, per
CLAUDE.md.

## Numbers

- Write "percent" in full, as FashionUnited does, not "%".
- CLAUDE.md's no-decimals rule stands: round to whole numbers. Company
  results are the one judgement call, the published reference kept
  Brunello Cucinelli's "9.5 percent reported, 13.3 percent at constant
  currency" exactly as the company reported them. Default to rounding
  ("up about 10 percent reported, 13 percent at constant currency") and
  ask Carmen per piece if she wants the reported decimals kept.
- Every figure that isn't DFB's own needs a source Carmen can link for
  the editor. If one can't be verified by search, flag it in the
  delivery notes rather than writing it in.

## Workflow

1. Get the source: the finished DFB piece and its data, plus any editor
   feedback or brief for this specific article.
2. Confirm the single angle with Carmen before drafting if the source
   supports more than one, the editor's first note is exactly this.
3. Draft **text only**, in the structure above, with bracketed image
   and chart slots. No HTML, no chart builds.
4. Deliver alongside the draft: the title options, a list of every
   non-DFB claim with its source link (or flagged as unverified), and
   the image slots with the licensed source each should come from.
5. Expect rounds of edits from Carmen and then from the editor. When
   editor feedback arrives, apply it as written and add any new
   standing rule to the "editor's standing feedback" list in this file
   so it carries into the next piece.
6. Before handing over, run a final check on the draft: no "I", "my",
   "we", no exclamation points, no em or en dashes, no "%", no decimals
   unless Carmen approved them, every image credited with a licensed
   source, title matches the actual scope of the piece.

## What Claude doesn't do here

- Doesn't rewrite Carmen's argument, it reshapes order and register to
  fit the publication and flags what it changed.
- Doesn't source, download or embed images.
- Doesn't add shopping or affiliate links.
- Doesn't invent quotes, brand statements or press coverage to fill a
  section.
