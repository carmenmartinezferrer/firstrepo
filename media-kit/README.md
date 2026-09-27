# DFB Media Kit

A one-page PDF media kit (`media_kit.pdf`), refreshed every 15 days (on the 1st and 15th of the month).
The layout matches `reference_2026-09-07.pdf`.

```bash
pip install playwright pymupdf
CHROMIUM_PATH=/opt/pw-browsers/chromium python3 media-kit/build.py
```

- `data.json`: every number, link and partnership on the page. Edit it and re-run the build.
- `build.py`: turns `data.json` into HTML and prints it to PDF with headless Chromium.
- `fonts/`: DM Serif Display and Jost (Google Fonts, OFL), bundled so the build works offline.

- `stats_history.csv`: one row per update, used to show audience growth over time.

## Where the numbers come from
- **Instagram**: pulled automatically from the Meta Graph API. This needs a system-user
  access token saved in the cloud environment as `META_ACCESS_TOKEN`.
- **Substack**: Substack has no official stats API. Every 15 days, drop a subscriber CSV export
  or a screenshot of the Stats page into the "DFB Media Kit" Google Drive folder.
