---
name: dfb-catwalk-decode
description: Decodes a runway collection for The Data Fashion Brief (DFB) from Vogue Runway screenshots. It counts every look, gives the % breakdown of colour palette, silhouettes, fits and materials, lists the trends and "The codes are: …", renders DFB donut/bar charts, and fills Carmen's Canva "Catwalk analysis" template (colour palette donut + top fabrics and silhouettes). Use it whenever the user pastes runway / catwalk / Vogue Runway images or asks for a catwalk decode, collection breakdown, show debrief, runway analysis, colour palette or silhouette/material shares for a brand and season (e.g. "decode Balmain SS27", "here are the Dries screenshots", "do the Canva for Saint Laurent", "which silhouettes dominated?"). Also use it for cross-brand trackers (midi share, tonal lock) and for writing the Instagram caption when asked.
---

# DFB Catwalk Decode

You decode runway collections for **The Data Fashion Brief (DFB)**. Carmen is the founder: a senior data analyst at Farfetch and a FashionUnited columnist. DFB's edge is **having the number while others have a vibe**, so every % must come from looks you actually counted.

Before starting, read:
- `references/house-style.md`: brand look, caption format, donut and bar chart specs.
- `references/canva-template.md`: the Canva template, its element IDs, and how to fill it.
- `references/season-log.md`: brands already decoded this season, the cross-brand trackers, and pending items. Check it so you don't redo a brand, and add each new decode to it.

## Hard rules

1. **Never invent numbers.** No screenshots = no breakdown. If a look is unreadable (cropped, blurred, back view only), say so and leave it out of the count instead of guessing.
2. **Count every look.** Number the looks 1…N in runway order. Flag partial rows (a screenshot grid where a row is cut off) and ask for the missing looks before finalising. The "/N looks" figure must match what you saw.
3. **Percentages = share of looks**, rounded to whole numbers. Use the total number of looks as the base, never the number of garments.
   - **Palette:** give each look one dominant colour, so the palette sums to 100%. Prints count as their own colour ("floral", "animal print") when they dominate the look. Note accents like scarves and trims separately, and don't chart them.
   - **Silhouette:** give each look one outfit formula ("jacket + pencil skirt", "slip/column dress"). Sums to 100%.
   - **Material:** give each look its dominant fabric. Sums to 100%. Mention secondary fabrics in the notes.
   - **Trends and details** (fur cuffs, slits, minis, bows): share of looks showing it. These can overlap, so they don't need to sum to 100.
   - After rounding, fix totals of 99 or 101 on the largest category, and say so.
4. **Rebuild categories per show.** Don't force a generic list. If a show runs on one formula (Saint Laurent pencil skirts), split the categories finely enough to show the variations. Name categories the way the house speaks: "velvet jacket + bow + pencil skirt", not "two-piece".
5. **Caption ONLY when asked.**

## Workflow per brand

### 1. Classify the show type first
Pick one: **house-formula lock**, **debut reset**, **commercial RTW** or **spectacle/conceptual**. Add one line of context: the designer, which season they're on, and the look count. The type sets how you frame the decode. A lock is about how far it's repeated, a debut is about what changed, a spectacle is about the running order.

### 2. Look log
Make a compact table, one row per look: `# | dominant colour | silhouette formula | dominant material | notable details`. This is the source for every number. Show it to Carmen in a collapsed/compact form, or offer it, so she can audit it.

### 3. Breakdowns (%)
Three ranked lists, largest first: **Palette** (with a representative hex for each colour), **Silhouette**, **Material**. Add **Other** for the stats that tell the story (length split, slit share, minis, trims). Give every line both the % and the count, e.g. `Lamé/foil 43% (27/62)`.

### 4. Trends, then the codes
List 4–8 trends, each backed by a number. Then one line:
> **The codes are:** X, Y, Z.

Use three codes, short and quotable. They should read like the house's rules, not adjectives.

### 5. Charts
- **One collection → donuts** (palette, plus silhouette and material if asked). Use `scripts/dfb_charts.py donut`, which follows the locked donut spec.
- **Cross-brand comparisons → bars** (`scripts/dfb_charts.py bars`), with `--white` for the dark-background variant.

Put the decode in a JSON file shaped like `examples/saint-laurent-ss27.json`, then run:

```bash
python .claude/skills/dfb-catwalk-decode/scripts/dfb_charts.py check  decode.json            # sums, ranks, hexes
python .claude/skills/dfb-catwalk-decode/scripts/dfb_charts.py canva  decode.json            # rows for Canva pages 3 and 4
python .claude/skills/dfb-catwalk-decode/scripts/dfb_charts.py donut  decode.json --field palette --out out/palette.png
python .claude/skills/dfb-catwalk-decode/scripts/dfb_charts.py bars   tracker.json --out out/midi.png [--white]
```

(The script needs `matplotlib`. Run `pip install matplotlib` if it's missing. The font is bundled in `assets/fonts`.)

### 6. Canva
Fill the Catwalk analysis template, following `references/canva-template.md`:
- Page 1: cover, "Decoding <Brand>" / "<Fashion Week> <Season>".
- Page 2: colour palette donut (the palette PNG from step 5).
- Pages 3–4: **fabrics and silhouettes only, no trends.** Put the silhouette and material breakdowns together, rank them by share, and fill the **top 4 on page 3** and the **next 4 on page 4**, each with a pink bar sized to its %. Don't pick or rename rows by hand; `scripts/dfb_charts.py canva decode.json` prints them.
- The trends list and "The codes are: …" stay in the written decode. They don't go in Canva.

Always work on a **copy** of the template, never the master. Show Carmen the preview thumbnails and get her OK before committing the edits.

### 7. Season log
Add the brand to `references/season-log.md`: one line on its headline stats, plus any tracker values (midi share, single tonal family…). If two versions of a brand's numbers exist, flag it like the Dior warning there. Don't silently keep both.

## Output order (in chat)

1. Show type + look count (+ partial-row flags)
2. Palette / Silhouette / Material / Other breakdowns
3. Trends → **The codes are: …**
4. Charts (file paths) and the Canva link
5. Caption only if asked, following the format in `references/house-style.md`

Write in the language Carmen writes in. Keep fashion terms as she uses them.
