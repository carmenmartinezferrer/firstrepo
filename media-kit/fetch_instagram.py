"""Pull Instagram stats from the Meta Graph API into data.json and stats_history.csv.

    META_ACCESS_TOKEN=... python3 media-kit/fetch_instagram.py [--dry-run]

Needs an Instagram professional account linked to a Facebook Page, and a token with
instagram_basic, instagram_manage_insights and pages_read_engagement. IG_USER_ID is optional;
it is looked up from the token's Pages when unset.

Metric definitions (per post, averaged over posts from the last 30 days):
  engagement rate = total interactions / reach    save rate = saves / reach
  send rate       = shares / reach                avg. reach = mean reach per post
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
API = "https://graph.facebook.com/" + os.environ.get("META_API_VERSION", "v23.0")
TOKEN = os.environ.get("META_ACCESS_TOKEN")


def get(path, **params):
    params["access_token"] = TOKEN
    url = f"{API}/{path}?{urllib.parse.urlencode(params)}"
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"Meta API error on {path}: {e.read().decode()[:500]}")


def ig_user_id():
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
    if not TOKEN:
        sys.exit("Set META_ACCESS_TOKEN (see media-kit/README.md).")
    uid = ig_user_id()
    now = datetime.now(timezone.utc)
    since = now - timedelta(days=30)

    profile = get(uid, fields="username,followers_count")
    followers = profile["followers_count"]
    acct = total(uid, "reach,views", since, now)

    media = get(f"{uid}/media", fields="id,caption,permalink,timestamp", limit=50)["data"]
    posts = []
    for m in media:
        if datetime.strptime(m["timestamp"], "%Y-%m-%dT%H:%M:%S%z") < since:
            continue
        ins = {r["name"]: r["values"][0]["value"] for r in
               get(f"{m['id']}/insights", metric="reach,saved,shares,total_interactions")["data"]}
        if ins.get("reach"):
            posts.append({**m, **ins})
    if not posts:
        sys.exit("No posts with insights in the last 30 days.")

    def avg(key):
        return sum(p[key] / p["reach"] for p in posts) / len(posts) * 100

    top = max(posts, key=lambda p: p["reach"])
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
                   [f"{round(sum(p['reach'] for p in posts) / len(posts)):,}", "avg. reach"]]
    ig["growth_title"] = [f"{fmt_k(followers)} followers", " since launching in January 2026"]
    month = now.strftime("%m/%y")
    ig["growth"] = [g for g in ig["growth"] if g[0] != month] + [[month, followers, fmt_k(followers)]]
    ig["countries"] = [[c[0], pct(v, n_c)] for c, v in top5] + [["Other", 100 - sum(pct(v, n_c) for _, v in top5)]]
    ig["period"] = [f"{since:%-d %b} – {now:%-d %b %Y}: ", f"{acct.get('reach', 0):,} reach", f"{acct.get('views', 0):,} views"]
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
    row["source"] = "meta graph api" if not row["source"] else row["source"] + " + meta graph api"
    with hist.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["date", "substack_subscribers", "substack_followers", "instagram_followers", "source"])
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    main()
