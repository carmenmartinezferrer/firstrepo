# Substack stats for the DFB media kit

Substack has **no official API and no Claude connector**. The owner chose **A + B** (27 Sep 2026):
public data automatically, plus one Stats screenshot from her every 15 days. **Don't** ask for her
Substack session cookie: it gives full account access (publishing, settings, subscriber emails),
breaks often, and is against Substack's rules. She decided against it.

## A. Public data: `media-kit/fetch_substack.py`
- Needs `substack.com` and `thedatafashionbrief.substack.com` in the environment's allowed domains
  (these apply to new sessions only).
- `python3 media-kit/fetch_substack.py --dry-run --raw` prints posts and any public
  subscriber/follower counts, and saves the raw JSON to `media-kit/.substack_raw/` (git-ignored).
  **The first time, inspect the raw JSON** and fix the field names in the script if Substack uses
  different ones. It was written without network access and hasn't been run yet.
- Without `--dry-run`, it writes `media-kit/substack_posts.csv` (date, title, url, likes,
  comments, restacks).
- Public counts are often rounded ("7K+"). **Exact numbers come from B.**

## B. Stats screenshots from the owner (in Drive)
- Folder: **DFB / Media Kit / Substack stats**, Drive id `19Haium6oDIzEnvdBjz7t0zlHVTKUetWi`.
- She uploads a screenshot of her Substack dashboard **Stats** page (and, if she likes, the
  Subscribers page) around the 1st and 15th of each month.
- Find the newest one with Google Drive `search_files` (`parentId = '19Haium6oDIzEnvdBjz7t0zlHVTKUetWi'`,
  newest `createdTime`), then read it with `read_file_content` (images are supported).
- Take from it: **total subscribers, followers, open rate, views per post** (or total views ÷
  posts, if that's what's shown), and the top newsletter if visible. Write down the screenshot's
  date. If a number isn't visible, keep the last value and tell her which one was missing.
- If there's no screenshot newer than the last refresh, don't guess: keep the last values and remind her.

## Into the kit
- `data.json` → `substack.tiles`: followers, subscribers, avg. open rate, avg. views/post.
- `substack.growth`: add or replace the current month's bar with the exact subscriber count
  (`[MM/YY, number, label]`); month-on-month labels are computed automatically.
- `substack.top`: the top newsletter (views · open rate). Replace it only with a better, confirmed one.
- `stats_history.csv`: fill substack_subscribers and substack_followers for the refresh date.
- Current values (27 Sep 2026, reported by the owner): >12K followers, 7.3K subscribers,
  32.7% open rate, 2,193 avg. views/post.
