# DFB Media Kit

A PDF media kit, designed in Canva and refreshed every 15 days (on the 1st and 15th of the month).

- `stats_history.csv`: one row per update, used to show audience growth over time.

## Where the numbers come from
- **Instagram**: pulled automatically from the Meta Graph API. This needs a system-user
  access token saved in the cloud environment as `META_ACCESS_TOKEN`.
- **Substack**: Substack has no official stats API. Every 15 days, drop a subscriber CSV export
  or a screenshot of the Stats page into the "DFB Media Kit" Google Drive folder.
