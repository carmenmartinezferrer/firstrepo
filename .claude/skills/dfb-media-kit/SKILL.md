---
name: dfb-media-kit
description: Builds and refreshes the two-page media kit PDF for The Data Fashion Brief (DFB, @thedatafashionbrief, a fashion data analyst on Instagram and Substack). It pulls Instagram stats from Metricool (or the Instagram API token), takes Substack numbers and partnerships from the owner's files, rebuilds the PDF in the owner-approved two-page structure, and updates the Canva copy. Use this whenever the user wants to update, refresh, rebuild or check the media kit, pull Instagram or Substack stats for brands, add a new partnership or collaboration, change what the kit shows (engagement window, growth, reach vs views), or run or fix the 15-day media kit routine. Trigger even on casual asks like "update my media kit", "new numbers for brands", "add ASOS to my collabs", "how's my growth this month".
---

# DFB Media Kit

A **two-page** PDF media kit (US Letter; page 1 = the pitch, page 2 = the numbers) for The Data Fashion Brief, refreshed every 15 days
(1st and 15th of the month). Everything lives in `media-kit/` in this repo.

The owner wants this to run with almost no work on her side. Never make numbers up: every figure
comes from Metricool, the Instagram API, or something the owner gave you. If a number can't be
sourced, keep the last known value and say so.

## Files

| File | What it is |
|---|---|
| `media-kit/data.json` | Every number, link and partnership on the page. **Edit this, never the HTML.** |
| `media-kit/build.py` | data.json → HTML → PDF (headless Chromium), then font subsetting and compression (~94 KB, keeps links). Run `CHROMIUM_PATH=/opt/pw-browsers/chromium python3 media-kit/build.py`. Needs `pip install playwright pymupdf`. |
| `media-kit/fetch_instagram.py` | Instagram API fetcher (token route, see below). `--dry-run` prints without writing. |
| `media-kit/stats_history.csv` | One row per refresh: date, Substack subscribers and followers, Instagram followers, source. This builds the follower history, because no source backfills it. |
| `media-kit/instagram_posts.csv` | Written by the fetcher: every post since launch, with lifetime insights. |
| `media-kit/fonts/` | DM Serif Display and Jost (static weights made from the variable font with fontTools; the variable font bloated the PDF). |
| `media-kit/reference_2026-09-07.pdf` | The owner's original September kit. The layout must stay faithful to it. |

After every rebuild, open the PDF at 110 dpi (`pymupdf` `get_pixmap`) and **look at it**. Check:
it's exactly 2 pages, no text overflows or wraps badly, all links are there (27 as of 27 Sep 2026).
In data.json, lists joined with " · " must stay wrappable: brand names use `&nbsp;` inside a name
only, never around the separators.

## Kit structure (approved by the owner, 27 Sep 2026): keep this order
Two pages, US Letter. **Page 1 sells, page 2 proves.** Every block, its data.json key and its
source are listed below. Don't add, remove or reorder blocks without the owner's OK. When she
changes the structure, update this section and the Design log.

**Both pages: header and footer**
- Header: "The Data *Fashion* Brief" · @thedatafashionbrief · Media Kit · {month} · **London** ·
  tagline "Decoding fashion through data." · links to Instagram, Substack, LinkedIn, FashionUnited
  and the email (`brand`, `month`, `location`, `links`).
- Footer: "For partnerships and collaborations · **Rates on request**" and hi@datafashionbrief.com
  (`rates`). **Never print prices.**

**Page 1: the pitch**
1. **Hero:** photo (`photo`, a placeholder until she sends one) · **unique angle** line (`angle`,
   a draft until she confirms it) · bio (`bio`) · "Based in London · Writing for FashionUnited,
   featured by Lyst" · **reader quote** (`quote`: "Your newsletters are always on point…",
   credited "Substack reader").
2. **At a glance** (100% organic): total followers (Instagram + Substack followers; never add
   subscribers on top) · Instagram followers · Substack followers · Substack subscribers ·
   Instagram engagement (90 days).
3. **Audience:** gender · age (women) · top markets (Instagram countries).
4. **Past collaborations:** logo tiles (`collaborations`: name, url, logo). Brands come from the
   Partnerships tab of her sheet; a tile links to the post when there is one. Brand-name wordmarks
   until she sends logo files. **No results or metrics from past collabs** (her decision).
5. **As featured in** (`press`): FashionUnited (contributing author) · Lyst Insights "London
   Calling: The Homecoming Edition" · Lyst Insights "The Fall Fashion Forecast".
6. **Content pillars** (`pillars`) and **Work with me** (`ways`), as chips.

**Page 2: the numbers**, one section per platform
7. **Instagram** (`instagram`): tiles for followers · engagement rate · save rate · send rate ·
   avg. views/post (rates over the last 90 days, pooled; header note `window_note`) → growth chart
   of **followers at each month end** with month-on-month % (last 4 bars) + countries donut +
   30-day reach and views line → top post → examples with links (brand collabs first).
8. **Substack** (`substack`): tiles for followers · subscribers · avg. open rate · avg.
   views/post (last 90 days) → growth chart of **subscribers at each month end, from 01/26**, with
   month-on-month % + countries donut → top newsletter → examples with links.

## Page content and the decisions behind it

- **Header, bio and links:** fixed and stored in data.json.
- **Instagram tiles:** followers · engagement rate · save rate · send rate · **avg. views/post**.
  - The owner agreed on **views, not reach**. Average reach per post fell during fashion month
    (9,774 over 30 days) while views stayed strong; views are honest and brands understand them.
- **Engagement, save and send rates are pooled:** sum(interactions) / sum(reach), and the same
  for saves and shares, over **feed posts and carousels only (no Reels)**. This reproduces the
  September kit (10.34%); the 60-day pooled figure was 10.28%. Don't switch to per-post averages.
- **Window:** 90 days is the target. Metricool only holds posts from 27 Jul 2026, so until the
  token route has run (or until late October), use the longest window available and **label it**,
  e.g. "last 60 days".
- **Growth:** "0 → 21K followers since launching in January 2026 · 100% organic", monthly bars,
  and **month-on-month % labels** on recent bars. Known month-ends:
  05/26 3,386 · 06/26 4,961 · 07/26 6,104 · 08/26 ">15K" (the exact figure is unknown; ask the
  owner if it matters) · 27 Sep 21,107. Jul→Aug was +146%, Aug→Sep +41%. From September on,
  take month-end followers from stats_history.csv.
- **Top post:** all-time best by reach. Currently the "#whimsymaxxing" post (95,951 reach ·
  9.7% engagement, from the API on 27 Sep 2026). Replace it only if a newer post beats it.
- **Reach and views line** ("28 Aug – 27 Sep 2026: 229,490 reach · 697,005 views"): account
  totals for the last 30 days from the token (the API caps these at 30 days). Metricool can't
  produce this line.
- **Audience:** follower gender (women vs men, ignoring unknown), age bands for women (18-24 …
  55-64, as a % of all women, with 13-17 and 65+ left off), and top 5 countries + Other.
- **Substack:** followers, subscribers, open rate, views per post, a monthly subscriber chart
  (with month-on-month labels), and the top newsletter. **There is no API.** Public data comes from
  `media-kit/fetch_substack.py`; private stats come from the owner's Stats screenshots in Drive.
  **Read `references/substack.md` for the full process.**
- **Past collaborations:** from the owner's sheet "260921_DFB_Growth.xlsx" (Drive file id
  `1aThD5Mrdzw-WVYpaPa8OKNQrI7VuzWck`), in the **Partnerships** tab. List brand names only.
  **Never show the Money or Clothes columns** (fees and gifted value are private). Posts that have
  links go into the Instagram "Examples: Brand collabs 1 2 3 …" line. Strip the `?utm_…` parts
  from links.

## Getting Instagram data

### Which source to use
**Use the Instagram API token first** (full post history since January, 90-day window). Fall back
to Metricool if the token fails or has expired, and cross-check the two on overlapping posts
when the token is first used.

### 1. Metricool connector (backup; confirmed working 27 Sep 2026)
Brand id **7118813** (timezone Europe/London). Call `getAnalyticsDataByMetrics` with ISO dates.
- Posts: `IGPO02` date, `IGPO03` caption, `IGPO06` url, `IGPO12` interactions, `IGPO14` reach,
  `IGPO15` saved, `IGPO27` shares, `IGPO28` views
- Reels: `IGRE02, IGRE06, IGRE09, IGRE11, IGRE12, IGRE21, IGRE23` (the same fields for Reels)
- Followers: `IGEV01`, only populated on the latest day
- Countries: `IGDP01, IGDP02` (shares as fractions)
- Age and gender: `IGAG01, IGAG02, IGAG03` (F / M / U counts)

Limits: posts only from 27 Jul 2026 onwards; no follower history; `IGEV19` (avg reach per post)
matches our per-post-average reach.

### 2. Instagram API token (primary; full history since January)
The owner set up the app "The data fashion brief stats" (App ID 1067770032751216,
Business type) with **Instagram API with Instagram Login**. She is an Instagram tester, and the
token is stored in the cloud environment as a Bearer credential for `graph.instagram.com` (or as
`INSTAGRAM_ACCESS_TOKEN`). New sessions only; `graph.instagram.com` must be in the allowed
domains. Run `python3 media-kit/fetch_instagram.py --dry-run` first and check the numbers against
Metricool before writing anything.
- **The token lasts 60 days from ~27 Sep 2026, so it expires around 26 Nov 2026.** Remind the
  owner at least a week before. It's renewed in the app dashboard: Instagram → API setup with
  Instagram login → Generate token.
- The Facebook Pages route (`META_ACCESS_TOKEN`, graph.facebook.com) **failed**: the DFB Page
  never showed up in `me/accounts`. Don't send the owner back down that path.
- Never ask the owner to paste a token into the chat.

## Canva
The current design is **`DAHWa9-H9ck`** (https://www.canva.com/d/k9U2S6Uza7kFPvk), the two-page kit imported 27 Sep 2026 from commit 63627d9. The PDF import loses some spacing (words run together in the bio, the Substack followers tile slips up next to the heading), so the PDF in the repo is the version to send brands. To update it:
commit and push the new PDF, then `import-design-from-url` with the raw GitHub URL **pinned to the
commit SHA** (`https://raw.githubusercontent.com/carmenmartinezferrer/firstrepo/<sha>/media-kit/media_kit.pdf`),
with `intended_design_type: us_letter`. This creates a new design. Verify it with `read-design`,
record the new id here and in the README, and tell the owner she can delete the old one.

## Design changes
The design lives in `media-kit/build.py` (HTML and CSS), and the content lives in `data.json`.
Canva is only a copy re-imported from the PDF, so **edits made by hand in Canva are lost at the
next refresh.** When the owner asks for a design change:
1. Make it in build.py or data.json.
2. Rebuild, check it's still one page, and send her a preview image. Wait for her OK.
3. Commit, push, update Canva, and add a line under "Design log" below so future refreshes keep it.

### Design log
- 2026-09-27: reader quote on page 1 (`quote` in data.json). The growth charts show the **running total at each month end** (followers for Instagram, subscribers for Substack) with month-on-month %; the Substack chart starts at 01/26. The header note for each platform is `window_note`.
- 2026-09-27: v2, two pages, agreed with the owner. Page 1: header with London, photo (placeholder until she sends one; `photo` in data.json), unique-angle line (a draft, to be confirmed), bio, at-a-glance tiles (total followers = IG + Substack followers, no double-counting with subscribers), audience (gender, age of women, top IG markets), past collaborations as logo tiles (brand-name wordmarks until she sends logo files; `logo`/`url` per brand; linked when a post exists), As featured in (FashionUnited, 2 Lyst Insights articles), content pillars, work with me, "Rates on request". Page 2: a separate Instagram section and Substack section, each with tiles, month-on-month growth labels on the last 4 bars (≈ when based on a ">" value), countries, top post or newsletter, and examples. **No results from past collabs on the kit** (owner's decision).
- 2026-09-27: rebuilt from the September 2026 PDF (DM Serif Display + Jost, pink #d54479 family,
  US Letter, one page); added "Brand collabs" examples and new partnerships.

## Delivery and known blocks
- **Canva PDF download is blocked:** `export-download.canva.com` is denied by the network policy.
- **Drive upload through the connector is blocked:** the base64 upload of the ~94 KB PDF was
  stopped by a safety check. Don't retry it. The target folder is **DFB / Media Kit**
  (`1SniTWO4JHFE0kdoKuPbTLDGyV5RYSDY8`). Send the PDF to the owner in chat (SendUserFile) and
  tell her to drop it in the folder.

## The 15-day refresh, step by step
1. Pull the Instagram data (token first, Metricool as fallback) and add a row to
   stats_history.csv.
2. Substack: run fetch_substack.py and read the newest Stats screenshot (references/substack.md). Check the partnerships sheet for new rows. Keep the last
   values if there's nothing new.
3. Update data.json, rebuild, and look at the PDF.
4. Commit and push, re-import into Canva, send the PDF to the owner, and give her a short summary
   of what changed, with any number that moved a lot explained.
5. Check when the token expires.
