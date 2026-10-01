# DFB house style

## Brand
- **Colours:** black, white, and pink `#D6447A`. Use the pink sparingly, as the accent: Canva trend bars, one highlight per chart at most.
- **Type:** DM Serif Display for titles and chart numbers, Century Gothic for body text. The Canva template already carries its own fonts, so keep them.
- **Voice:** analyst, not reviewer. Lead with the number, then the reading.

## Caption format (every decode)

Write it in Carmen's voice: first person, chatty, opinionated, with every claim backed by a number from the decode. Use this reference caption (Dior SS27) as the model:

```
@dior catwalk decode SS27 Paris Fashion Week

Ok ok ok guys, this one was a difficult one to classify. I've never seen materials this delicate, even on the blazers. Chiffon and tulle make up 32% of the fabric, more than suiting and tweed, and even the tailoring feels like it could float away.

The signature is a blazer (any type) or jacket over a mini ruffle skirt. But also ruffles and tweed.

When @jonathan.anderson goes soft, he goes all the way, with unstructured dresses at 13% and cardigans over full tulle skirts at 11%.

The palette stays 70% neutral, and very Anderson. So butter yellow and soft blues, pinks, greens…

The codes are: the blazer (in any shape, form, material) as the base, froth as the variable, the ruffle as the #jonathananderson signature.

I'm very into shrunken blazers atm and I've seen 14% of them on the runway.
```

Structure:
1. **Line 1:** `@<brandhandle> catwalk decode <Season> <City> Fashion Week`.
2. **Hook:** a casual opener ("Ok ok ok guys…") plus the headline stat, usually the top material or the big surprise.
3. **The signature:** the silhouette formula that defines the show, in plain words.
4. **The designer:** tag them (`@designerhandle`) with 2 supporting stats.
5. **The palette:** the neutral share as a % (black, white, cream, beige, brown and grey count as neutrals), plus the accent colours.
6. `The codes are: X, Y, Z.`, with the designer as a hashtag inside the codes line where it fits (`#jonathananderson`).
7. **Personal closing line:** Carmen's own take, plus one stat. This is her opinion, so draft one and mark it **(your take: edit)** so she can swap it.

Rules:
- Every % must come from the decode. Never round up for drama.
- Handles: use the house's and the designer's official Instagram handles. If unsure, write `@[handle?]`.
- No hashtag block at the end unless Carmen asks for one. The reference caption has none.

## Donut spec (one collection) — LOCKED

- figsize (9, 9), transparent background, dpi 300, `bbox_inches="tight"`.
- `ax.pie(startangle=90, counterclock=False, wedgeprops={"width": 0.42, "edgecolor": "none"})`.
- Wedges with **luminance > 0.82** get a `#D0CCC5` outline, linewidth 1.2.
- % label inside each wedge at radius 0.79, in DM Serif Display.
- Label size by share: **42** (≥15%), **32** (≥8%), **24** for everything smaller. Never smaller than 24: small wedges must still be readable (Carmen's rule, updated from 22/14).
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
