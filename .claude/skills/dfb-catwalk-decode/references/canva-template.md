# Canva "Catwalk analysis" template

- **Template design ID:** `DAHWx3H429E`
- **Link:** https://www.canva.com/design/DAHWx3H429E/3z7tLxGQryuHxAcHl4MSBg/edit
- **Format:** 4 pages, 1080 × 1350 px (Instagram portrait carousel). The current content is the Balmain SS27 example.
- **No autofill fields** (`get-design-dataset` returns `{}`), so fill it with `edit-design` operations.

## Never edit the master
1. `copy-design` with `design_id: DAHWx3H429E` gives you a new design ID. Do every step below on that copy.
2. `read-design` on the copy with `open_transaction: true`, `fields: ["design_content","thumbnails"]`. Element IDs stay the same in a copy, but **re-read the locators from the copy anyway**. Use the IDs below only as a guide to which element is which. If Carmen has changed the template, trust what you read.

## Page map (element IDs from the master)

### Page 1: cover `PBBQJ0BwVRVl4Bmv`
| Element | ID | Content |
|---|---|---|
| Title (white) | `LB5j5kG38NQzZKBL` | `Decoding  Balmain` ⏎ `Paris Fashion Week SS27 ` |
| DFB logo | `LBpWbsCqCyslC6XM` | leave |

- Use `find_and_replace_text` on the title: `Balmain` → brand, and `Paris Fashion Week SS27` → `<City> Fashion Week <Season>`. This keeps the two text sizes. Keep the double space after "Decoding" as it is.
- The cover photo is the **page background**. The Canva tools can't swap it reliably, so tell Carmen to drop in the hero look herself. Suggest which look: the opener, the finale, or the most "codes" look.

### Page 2: colour palette `PBCtVl2vf06NcN17`
| Element | ID | Content |
|---|---|---|
| Brand line | `LBpvzwSpjtgNCL0f` | `Balmain • Paris FW SS27 ` |
| Title | `LBf6t4cPL179fzmV` | `Colour palette` (leave) |
| Donut image frame | `LBRyWf5xH0FWszNX` | 1040 × 1040 image fill |
| Footnote | `LBvMSpmWrlz7Y9z1` | `*% is share of colour: proportion of total looks with that colour` (leave) |

To swap the donut:
1. Render it: `python scripts/dfb_charts.py donut decode.json --field palette --out palette.png --square`. `--square` pads the image to a square so it fits the 1040 × 1040 frame without cropping.
2. `create-upload-url` gives a single-use URL. Then upload the file:
   `curl -sS -X POST -H "Content-Type: application/octet-stream" --data-binary @palette.png "<upload_url>"`
   Take the asset ID from the response.
3. Run `edit-design` `update_fill` on locator `PBCtVl2vf06NcN17-LBRyWf5xH0FWszNX` with `asset_type: image`, the asset ID, and `alt_text: "<Brand> <Season> colour palette donut"`.

### Pages 3 and 4: fabrics and silhouettes `PBpLhH5S1vzmmPzd`, `PBRzJ6lSQHfwq4Dm`
Page 3 holds trends ranked 1–4, page 4 holds 5–8. Merge silhouettes and materials into one list and rank it by share. Make sure at least one of each appears in the top 8.

| Element | Page 3 ID | Page 4 ID | Content |
|---|---|---|---|
| Brand line | `LBRncXL3q4lJtlJn` | `LBPdJ9HDvLr35Qqh` | `Balmain • Paris FW SS27 ` |
| Trend names (4 lines) | `LB2YkwJSQ69V8DHx` | `LBTChQClk36Pr5F2` | `name1\nname2\nname3\nname4` |
| Percentages (4 lines, right-aligned) | `LBGzPckYMnPYMTsQ` | `LBKbrsNhbMVlcqDW` | `27%\n24%\n17%\n16%` |
| Pink bar **chart** | `LBZcZmnHKmmqPc9K` | `LB8Nsj5RRFXztrVf` | native Canva chart, **not editable by API** |
| Column headers | `LB4X5f4KRjQZC3Jc` / `LBx5S9KNGWNsbLNW` | `LBLy2gHyCvRfy0pH` / `LBc8RT4cm01vNySY` | `TREND • SS27`, `SHARE OF COLLECTION`. Swap the season if it isn't SS27. |

- Trend names: `replace_text` with the 4 lines joined by `\n`. Use sentence case ("Jacket + pencil skirt", "Lamé and foil"). Keep each name **≤ 30 characters** so it doesn't run into the bars.
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
