"""Pull DFB's public Substack data (no login) into substack_posts.csv and print a summary.

    python3 media-kit/fetch_substack.py [--dry-run] [--raw]

Needs network access to thedatafashionbrief.substack.com and substack.com. Substack has no
official API; these are the public endpoints its own website uses, so field names can change.
--raw saves the raw JSON responses to media-kit/.substack_raw/ so a session can inspect them.

Private stats (open rate, views, exact subscribers) are NOT public: they come from the owner's
Stats-page screenshots in Drive (see .claude/skills/dfb-media-kit/references/substack.md).
"""
import csv
import json
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).parent
PUB = "https://thedatafashionbrief.substack.com"
HANDLE = "thedatafashionbrief"
UA = {"User-Agent": "Mozilla/5.0 (media kit stats; owner's own publication)"}


def get(url):
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"Substack returned {e.code} for {url}")
    except urllib.error.URLError as e:
        sys.exit(f"Could not reach {url} ({e.reason}). Is the host allowed under Network access?")


def find_counts(obj, path=""):
    """Walk a JSON object and yield any subscriber/follower-looking numbers with their key path."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            p = f"{path}.{k}" if path else k
            if isinstance(v, (int, float)) and any(w in k.lower() for w in ("subscriber", "follower")):
                yield p, v
            else:
                yield from find_counts(v, p)
    elif isinstance(obj, list):
        for i, v in enumerate(obj[:5]):
            yield from find_counts(v, f"{path}[{i}]")


def main():
    raw = "--raw" in sys.argv
    posts, offset = [], 0
    while True:
        batch = get(f"{PUB}/api/v1/archive?sort=new&offset={offset}&limit=50")
        if not batch:
            break
        posts += batch
        offset += len(batch)
        if len(batch) < 50:
            break
    profile = get(f"https://substack.com/api/v1/user/{HANDLE}/public_profile")

    if raw:
        out = HERE / ".substack_raw"
        out.mkdir(exist_ok=True)
        (out / "archive.json").write_text(json.dumps(posts, indent=2))
        (out / "public_profile.json").write_text(json.dumps(profile, indent=2))

    rows = [{
        "date": (p.get("post_date") or "")[:10],
        "title": p.get("title"),
        "url": p.get("canonical_url"),
        "audience": p.get("audience"),
        "likes": p.get("reaction_count"),
        "comments": p.get("comment_count"),
        "restacks": p.get("restacks"),
    } for p in posts]
    print(f"{len(rows)} posts, newest {rows[0]['date'] if rows else '-'}")
    for r in sorted(rows, key=lambda r: -(r["likes"] or 0))[:5]:
        print(f"  top: {r['likes']} likes · {r['comments']} comments · {r['restacks']} restacks  {r['title']}")
    print("public counts found on the profile:")
    for k, v in find_counts(profile):
        print(f"  {k} = {v}")

    if "--dry-run" in sys.argv:
        return
    with (HERE / "substack_posts.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ["date"])
        w.writeheader()
        w.writerows(rows)
    print("wrote", HERE / "substack_posts.csv")


if __name__ == "__main__":
    main()
