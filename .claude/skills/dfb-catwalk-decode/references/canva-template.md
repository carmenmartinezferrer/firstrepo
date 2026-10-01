# Canva "Catwalk analysis" template

- **Template design ID:** `DAHWx3H429E`
- **Link:** https://www.canva.com/design/DAHWx3H429E/3z7tLxGQryuHxAcHl4MSBg/edit
- **Format:** 4 pages, 1080 × 1350 px (Instagram portrait carousel). The current content is the Balmain SS27 example.
- **No autofill fields** (`get-design-dataset` returns `{}`), so fill it with `edit-design` operations.

## Brand name, fashion week and season come from the screenshots
Take the brand from the pasted pictures: the Vogue Runway header or caption ("Saint Laurent Spring 2027 Ready-to-Wear"), the show backdrop, or Carmen's message. Take the city and season from the same place (Spring 2027 = SS27, Fall 2027 = AW27). If the screenshots don't show the brand or the season clearly, **ask, don't guess.** Spell the name the house's way (Saint Laurent, MM6 Maison Margiela, Dries Van Noten).

Every brand and week mention in the template must be replaced. Nothing from the previous brand should be left:
- **Title** (cover): `Decoding  <Brand>` ⏎ `<City> Fashion Week <Season>`
- **Mini title** (brand line on pages 2, 3 and 4): `<Brand> • <City> FW <Season> `
- **Column header** (pages 3 and 4): `TREND • <Season>`
- **Design name:** `<Brand> <Season> catwalk decode`

Before showing the preview, `read-design` the transaction's `design_content` and search it for the old brand name ("Balmain" in the master, or whatever brand the copy started from). It must return nothing.

## Never edit the master — no need to paste the template each time
The skill duplicates the master template by its ID every time, so Carmen never has to paste it again. Only if she makes a new template (or the link changes) should this ID be updated.
1. `copy-design` with `design_id: DAHWx3H429E` gives you a new design ID. Do every step below on that copy.
2. `read-design` on the copy with `open_transaction: true`, `fields: ["design_content","thumbnails"]`. Element IDs stay the same in a copy, but **re-read the locators from the copy anyway**. Use the IDs below only as a guide to which element is which. If Carmen has changed the template, trust what you read.

## Page map (element IDs from the master)

### Page 1: cover `PBBQJ0BwVRVl4Bmv`
| Element | ID | Content |
|---|---|---|
| Title (white) | `LB5j5kG38NQzZKBL` | `Decoding  Balmain` ⏎ `Paris Fashion Week SS27 ` |
| DFB logo | `LBpWbsCqCyslC6XM` | leave |

- Use `find_and_replace_text` on the title: `Balmain` → brand, and `Paris Fashion Week SS27` → `<City> Fashion Week <Season>`. This keeps the two text sizes. Keep the double space after "Decoding" as it is.
- The template cover has **no photo** (white text on a white page). Carmen adds the hero look herself, so tell her which one: the opener, the finale, or the most "codes" look.

### Page 2: colour palette `PBCtVl2vf06NcN17`
| Element | ID | Content |
|---|---|---|
| Mini title (brand line) | `LBpvzwSpjtgNCL0f` | `Balmain • Paris FW SS27 ` → `replace_text` with `<Brand> • <City> FW <Season> ` |
| Title | `LBf6t4cPL179fzmV` | `Colour palette` (leave) |
| Donut image frame | `LBRyWf5xH0FWszNX` | 1040 × 1040 image fill |
| Footnote | `LBvMSpmWrlz7Y9z1` | `*% is share of colour: proportion of total looks with that colour` (leave) |

To swap the donut, **draw it natively in Canva**. This is tested and works. (A PNG upload doesn't work from cloud sessions: the network policy blocks `www.canva.com`.)
1. Run `python scripts/dfb_charts.py canva-donut decode.json`. For each wedge it gives an `insert_shape` operation (SVG arc path, colour, and outline for pale wedges) and a label (text, position, size, colour).
2. In one `edit-design` call on page 2: `delete_element` the image frame `PBCtVl2vf06NcN17-LBRyWf5xH0FWszNX`, then add every wedge `insert_shape` (with `page_id`), then an `add_text` for every label (`text`, `top`, `left`, `width`).
3. Take the new label locators from the response. In a second call, `format_text` each one with `font_size`, `color`, `text_align: "center"` and `line_height: 1`.
4. Check the thumbnail. Every label should sit in the middle of its wedge.
- **Font:** the Canva tools can't set a font family, so the labels come out in Canva's default font. To get DM Serif Display, select the labels in Canva and change the font (one click).
- **Local session with Canva access:** you can instead upload the PNG (`donut --square`, then `create-upload-url`, POST the bytes, then `update_fill` on the frame). That keeps DM Serif Display, but the donut is no longer editable in Canva.

### Pages 3 and 4: fabrics and silhouettes `PBpLhH5S1vzmmPzd`, `PBRzJ6lSQHfwq4Dm`
These pages show **fabrics and silhouettes only, not trends.** Put the `silhouette` and `material` breakdowns together into one list ranked by share. Page 3 = ranks 1–4, page 4 = ranks 5–8. Use the labels exactly as they appear in the decode. When two rows tie, keep them in decode order. Get the rows from `python scripts/dfb_charts.py canva decode.json`.

**No near-duplicates.** If a material and a silhouette are basically the same thing ("Knit" and "Knit sweater", "Velvet" and "Velvet jacket + bow", "Leather" and "Leather separates"), only the one with the higher share goes in Canva and the next row moves up. On a tie, the silhouette stays. The `canva` command does this by matching fabric words, and prints a "Skipped as similar" line for each row it drops. Read that list: if a skip is wrong (the two rows really are different stories), add `"keep": true` to that row in the decode and re-run. If two rows should be skipped but weren't, tell Carmen and drop the smaller one by hand.

| Element | Page 3 ID | Page 4 ID | Content |
|---|---|---|---|
| Mini title (brand line) | `LBRncXL3q4lJtlJn` | `LBPdJ9HDvLr35Qqh` | `Balmain • Paris FW SS27 ` → `replace_text` with `<Brand> • <City> FW <Season> ` |
| Trend names (4 lines) | `LB2YkwJSQ69V8DHx` | `LBTChQClk36Pr5F2` | `name1\nname2\nname3\nname4` |
| Percentages (4 lines, right-aligned) | `LBGzPckYMnPYMTsQ` | `LBKbrsNhbMVlcqDW` | `27%\n24%\n17%\n16%` |
| Pink bar **chart** | `LBZcZmnHKmmqPc9K` | `LB8Nsj5RRFXztrVf` | native Canva chart, **not editable by API** |
| Column headers | `LB4X5f4KRjQZC3Jc` / `LBx5S9KNGWNsbLNW` | `LBLy2gHyCvRfy0pH` / `LBc8RT4cm01vNySY` | `TREND • SS27`, `SHARE OF COLLECTION`. Swap the season if it isn't SS27. |

- Trend names: `replace_text` with the 4 lines joined by `\n`. If a name is over 30 characters, the `canva` command flags it because it will run into the bars. In that case, shorten the label in the decode itself, so the chat and Canva stay identical.
- Percentages: `replace_text`, e.g. `29%\n13%\n11%\n11%`.
- **Bars.** The native chart can't take new data through the API, so:
  1. `delete_element` the chart.
  2. `insert_shape` one pink rectangle per row: `path: "M0 0H100V100H0Z"`, `view_box_width: 100`, `view_box_height: 100`, `color: "#D6447A"`, `corner_rounding: 2`.
  3. Geometry. Bars are right-aligned at x = 908, and the longest bar on **each page** is 90 px wide:
     - `width = max(6, round(90 * pct / page_max_pct))`
     - `left = 908 - width`
     - `height = 24`
     - `top = round(982.6 + 41.37 * i)` for row i = 0…3 (these match the 1.4 line height of the 29.55 px text starting at y = 973.9)
  4. Check the thumbnail. Each bar should sit on the same line as its text. If the bars are off, nudge `top` and re-check.
  - If Carmen would rather keep the native chart, leave it and give her the 8 values to paste into Canva's chart data panel.

## Finish
1. `update_title` → `<Brand> <Season> catwalk decode`.
2. `read-design` the transaction with `thumbnails` for pages 1–4, and show them to Carmen.
3. Only after she approves: `edit-design` with `finalize: "commit"`. Give her the edit link from `design_metadata.urls.edit_url`.
4. If she wants files: `get-export-formats`, then `export-design` as PNG (all pages) for Instagram.
