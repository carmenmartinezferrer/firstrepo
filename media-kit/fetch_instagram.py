"""Pull Instagram stats from the Meta Graph API into data.json and stats_history.csv.

    META_ACCESS_TOKEN=... python3 media-kit/fetch_instagram.py [--dry-run]

Preferred: INSTAGRAM_ACCESS_TOKEN from "API setup with Instagram login" (permissions
instagram_business_basic + instagram_business_manage_insights); needs graph.instagram.com.
Alternative: META_ACCESS_TOKEN via Facebook Login (instagram_basic, instagram_manage_insights,
pages_show_list, pages_read_engagement) with the account linked to a Page; needs graph.facebook.com.

Metric definitions (feed posts and carousels from the last WINDOW_DAYS days, default 90, pooled
like the Sept 2026 kit): engagement = sum(interactions) / sum(reach), save rate = sum(saves) /
sum(reach), send rate = sum(shares) / sum(reach), avg. views/post = mean views per post.
"""
import csv
import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).parent
# Two ways in: INSTAGRAM_ACCESS_TOKEN (Instagram API with Instagram Login, no Facebook Page
# needed, served from graph.instagram.com) or META_ACCESS_TOKEN (Facebook Login, via a Page).
VERSION = os.environ.get("META_API_VERSION", "v23.0")
# When no token variable is set, requests go to graph.instagram.com without one and rely on the
# environment's API credential (Bearer) being attached to that host by the network proxy.
TOKEN = os.environ.get("INSTAGRAM_ACCESS_TOKEN") or os.environ.get("META_ACCESS_TOKEN")
IG_LOGIN = not os.environ.get("META_ACCESS_TOKEN")
LAUNCH = "2026-01-01"
API = f"https://graph.instagram.com/{VERSION}" if IG_LOGIN else f"https://graph.facebook.com/{VERSION}"


def get(path, **params):
    if TOKEN:
        params["access_token"] = TOKEN
    url = f"{API}/{path}?{urllib.parse.urlencode(params)}"
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"Meta API error on {path}: {e.read().decode()[:500]}")
    except urllib.error.URLError as e:
        sys.exit(f"Could not reach {API} ({e.reason}). Is the host allowed under Network access?")


def ig_user_id():
    if IG_LOGIN:
        return get("me", fields="user_id")["user_id"]
    if os.environ.get("IG_USER_ID"):
        return os.environ["IG_USER_ID"]
    for page in get("me/accounts", fields="instagram_business_account")["data"]:
        if page.get("instagram_business_account"):
            return page["instagram_business_account"]["id"]
    sys.exit("No Instagram professional account is linked to a Facebook Page this token can see.")


def total(uid, metric, since, until):
    rows = get(f"{uid}/insights", metric=metric, period="day", metric_type="total_value",
               since=int(since.timestamp()), until=int(until.timestamp()))["data"]
    return {r["name"]: r["total_value"]["value"] for r in rows}


def demographics(uid, breakdown):
    rows = get(f"{uid}/insights", metric="follower_demographics", period="lifetime",
               metric_type="total_value", breakdown=breakdown)["data"]
    out = {}
    for res in rows[0]["total_value"]["breakdowns"][0]["results"]:
        out[tuple(res["dimension_values"])] = res["value"]
    return out


def pct(part, whole):
    return round(100 * part / whole) if whole else 0


def fmt_k(n):
    return f">{n // 1000}K" if n >= 10000 else f"{n:,}"


def main():
    uid = ig_user_id()
    now = datetime.now(timezone.utc)
    since = now - timedelta(days=int(os.environ.get("WINDOW_DAYS", "90")))
    since30 = now - timedelta(days=30)

    profile = get(uid, fields="username,followers_count")
    followers = profile["followers_count"]
    acct = total(uid, "reach,views", since30, now)  # account totals: the API caps these at 30 days

    # Every post since launch, with lifetime insights; kept in instagram_posts.csv for history.
    media, page = [], get(f"{uid}/media", fields="id,caption,permalink,timestamp,media_type", limit=100)
    while True:
        media += page["data"]
        nxt = page.get("paging", {}).get("next")
        if not nxt:
            break
        with urllib.request.urlopen(nxt, timeout=30) as r:
            page = json.load(r)
    history = []
    for m in media:
        ins = {}
        for metrics in ("reach,saved,shares,total_interactions,views", "reach,saved,total_interactions"):
            try:  # very old or unusual media can reject some metrics; fall back to fewer
                ins = {r["name"]: r["values"][0]["value"] for r in get(f"{m['id']}/insights", metric=metrics)["data"]}
                break
            except SystemExit:
                continue
        history.append({**m, **ins})
    posts = [p for p in history if p.get("reach") and p.get("media_type") != "VIDEO"
             and datetime.strptime(p["timestamp"], "%Y-%m-%dT%H:%M:%S%z") >= since]
    if not posts:
        sys.exit("No posts with insights in the window.")

    def avg(key):  # pooled: total of the metric / total reach, same method as the Sept 2026 kit
        return sum(p.get(key, 0) for p in posts) / sum(p["reach"] for p in posts) * 100

    # All-time best by reach (not just the window): feed posts and carousels since the January 2026 launch.
    top = max((p for p in history if p.get("reach") and p.get("media_type") != "VIDEO"
               and p["timestamp"] >= LAUNCH), key=lambda p: p["reach"])
    countries = demographics(uid, "country")
    ag = demographics(uid, "age,gender")
    n_c = sum(countries.values())
    top5 = sorted(countries.items(), key=lambda kv: -kv[1])[:5]
    women = {k[0]: v for k, v in ag.items() if k[1] == "F"}
    men = sum(v for k, v in ag.items() if k[1] == "M")
    n_w = sum(women.values())

    data = json.loads((HERE / "data.json").read_text())
    ig = data["instagram"]
    ig["tiles"] = [[fmt_k(followers), "followers"], [f"{avg('total_interactions'):.2f}%", "engagement rate"],
                   [f"{avg('saved'):.2f}%", "save rate"], [f"{avg('shares'):.2f}%", "send rate"],
                   [f"{round(sum(p.get('views', 0) for p in posts) / len(posts)):,}", "avg. views/post"]]
    ig["growth_title"] = [f"{fmt_k(followers)} followers", " since launching in January 2026"]
    month = now.strftime("%m/%y")
    ig["growth"] = [g for g in ig["growth"] if g[0] != month] + [[month, followers, fmt_k(followers)]]
    ig["countries"] = [[c[0], pct(v, n_c)] for c, v in top5] + [["Other", 100 - sum(pct(v, n_c) for _, v in top5)]]
    ig["period"] = [f"{since30:%-d %b} – {now:%-d %b %Y}: ", f"{acct.get('reach', 0):,} reach", f"{acct.get('views', 0):,} views"]
    caption = (top.get("caption") or "").strip().split("\n")[0][:90]
    ig["top"] = {"label": "TOP POST", "title": caption,
                 "stats": f"{top['reach']:,} reach  ·  {100 * top['total_interactions'] / top['reach']:.1f}% engagement"}
    data["audience"]["gender"] = [["Women", pct(n_w, n_w + men)], ["Men", pct(men, n_w + men)]]
    bands = ["18-24", "25-34", "35-44", "45-54", "55-64"]
    data["audience"]["age"] = [[b, pct(women.get(b, 0), n_w)] for b in bands]
    data["month"] = now.strftime("%B %Y")

    print(json.dumps({"followers": followers, "tiles": ig["tiles"], "period": ig["period"],
                      "top": ig["top"], "countries": ig["countries"], "audience": data["audience"]}, indent=2))
    if "--dry-run" in sys.argv:
        return
    with (HERE / "instagram_posts.csv").open("w", newline="") as f:
        cols = ["timestamp", "media_type", "permalink", "reach", "views", "total_interactions", "saved", "shares"]
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(sorted(history, key=lambda p: p["timestamp"]))
    (HERE / "data.json").write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    hist = HERE / "stats_history.csv"
    rows = list(csv.DictReader(hist.open()))
    today = date.today().isoformat()
    row = next((r for r in rows if r["date"] == today), None)
    if row is None:
        prev = rows[-1] if rows else {}
        row = {"date": today, "substack_subscribers": prev.get("substack_subscribers", ""),
               "substack_followers": prev.get("substack_followers", ""), "source": ""}
        rows.append(row)
    row["instagram_followers"] = followers
    if "meta graph api" not in row["source"]:
        row["source"] = "meta graph api" if not row["source"] else row["source"] + " + meta graph api"
    with hist.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["date", "substack_subscribers", "substack_followers", "instagram_followers", "source"])
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    main()
