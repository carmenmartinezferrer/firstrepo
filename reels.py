#!/usr/bin/env python3
"""Turn Substack articles into Instagram/TikTok Reels scripts using the DFB Reels Formula.

Examples:
    python reels.py https://yourname.substack.com/p/some-post
    python reels.py --latest 3 https://yourname.substack.com
    python reels.py --file draft.md
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from typing import List, Literal, Optional
from urllib.parse import urlparse

import anthropic
import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parent
FORMULA_PATH = ROOT / "prompts" / "dfb_reels_formula.md"
DEFAULT_MODEL = "claude-opus-5"
HTTP_HEADERS = {"User-Agent": "Mozilla/5.0 (DFB reels generator)"}


# ---------------------------------------------------------------------------
# Article loading
# ---------------------------------------------------------------------------

@dataclass
class Article:
    title: str
    subtitle: str
    url: str
    date: str
    text: str
    paywalled: bool = False


def html_to_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "button", "form"]):
        tag.decompose()
    # Keep headings / list items on their own lines so structure survives.
    lines = []
    for el in soup.find_all(["h1", "h2", "h3", "h4", "p", "li", "blockquote", "figcaption", "pre"]):
        text = el.get_text(" ", strip=True)
        if not text:
            continue
        if el.name in ("h1", "h2", "h3", "h4"):
            text = f"\n## {text}"
        elif el.name == "li":
            text = f"- {text}"
        elif el.name == "figcaption":
            text = f"[Image caption: {text}]"
        lines.append(text)
    if not lines:
        return soup.get_text("\n", strip=True)
    return "\n\n".join(lines).strip()


def split_substack_url(url: str) -> tuple[str, Optional[str]]:
    """Return (origin, slug) for a Substack post or publication URL."""
    if not url.startswith("http"):
        url = "https://" + url
    parsed = urlparse(url)
    origin = f"{parsed.scheme}://{parsed.netloc}"
    match = re.search(r"/p/([^/?#]+)", parsed.path)
    return origin, (match.group(1) if match else None)


def fetch_post(url: str) -> Article:
    origin, slug = split_substack_url(url)
    if not slug:
        raise SystemExit(f"Not a Substack post URL (expected .../p/<slug>): {url}")

    # Substack's public post API works for both *.substack.com and custom domains.
    resp = requests.get(f"{origin}/api/v1/posts/{slug}", headers=HTTP_HEADERS, timeout=30)
    if resp.ok:
        data = resp.json()
        return Article(
            title=data.get("title") or slug,
            subtitle=data.get("subtitle") or "",
            url=data.get("canonical_url") or url,
            date=(data.get("post_date") or "")[:10],
            text=html_to_text(data.get("body_html") or ""),
            paywalled=data.get("audience") not in (None, "everyone"),
        )

    # Fallback: scrape the public page.
    resp = requests.get(url, headers=HTTP_HEADERS, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    body = soup.select_one("div.available-content") or soup.select_one("div.body.markup") or soup
    title = soup.find("h1")
    subtitle = soup.select_one("h3.subtitle")
    return Article(
        title=title.get_text(strip=True) if title else slug,
        subtitle=subtitle.get_text(strip=True) if subtitle else "",
        url=url,
        date="",
        text=html_to_text(str(body)),
        paywalled=soup.select_one("div.paywall") is not None,
    )


def latest_post_urls(publication_url: str, count: int) -> List[str]:
    origin, _ = split_substack_url(publication_url)
    resp = requests.get(
        f"{origin}/api/v1/archive",
        params={"sort": "new", "offset": 0, "limit": count},
        headers=HTTP_HEADERS,
        timeout=30,
    )
    if resp.ok:
        posts = [p for p in resp.json() if p.get("slug")]
        return [p.get("canonical_url") or f"{origin}/p/{p['slug']}" for p in posts[:count]]

    # Fallback: RSS feed.
    resp = requests.get(f"{origin}/feed", headers=HTTP_HEADERS, timeout=30)
    resp.raise_for_status()
    root = ET.fromstring(resp.content)
    return [item.findtext("link") for item in root.iter("item")][:count]


def load_file(path: str) -> Article:
    p = Path(path)
    raw = p.read_text(encoding="utf-8")
    text = html_to_text(raw) if p.suffix.lower() in (".html", ".htm") else raw
    first_line = next((line.lstrip("# ").strip() for line in text.splitlines() if line.strip()), p.stem)
    return Article(title=first_line, subtitle="", url=str(p), date="", text=text)


# ---------------------------------------------------------------------------
# Output schema
# ---------------------------------------------------------------------------

class Beat(BaseModel):
    act: Literal["Inicio", "Nudo", "Desenlace"] = Field(description="Which of the three acts this beat belongs to (formula section 6).")
    beat: str = Field(description="Beat name from the formula, e.g. Hook, Thesis, Evidence 1, Reveal.")
    timing: str = Field(description="Time range, e.g. '0-3s'.")
    voiceover: str = Field(description="Exactly what to say out loud in this beat.")
    on_screen_text: str = Field(description="Short text overlay (max ~8 words). Must work with sound off.")
    visual: str = Field(description="What's on screen: talking head, B-roll, runway clip, chart, screenshot, etc.")
    attention_peak: int = Field(description="Interest level 0-5 of this beat. Peaks in the Nudo should climb toward the close (section 6).")
    peak_reason: str = Field(description="Why this beat holds attention (e.g. 'debunks a myth', 'surprising number'), or '' if it's pure setup.")


class SentenceComponent(BaseModel):
    part: str = Field(description="A fragment of the sentence.")
    role: str = Field(description="What the fragment is, e.g. characteristic, result, context, problem, data, contrast.")


class SentenceCheck(BaseModel):
    sentence: str = Field(description="One sentence from the full script, verbatim.")
    components: List[SentenceComponent]
    goal: str = Field(description="What the sentence makes the viewer feel or want (curiosity, surprise, recognition, urgency...).")


class DataPoint(BaseModel):
    claim: str = Field(description="A factual claim, number, brand move or date used in the script.")
    source: str = Field(description="Quote or paraphrase from the article that supports it, or 'NEEDS DATA'.")
    status: Literal["from_article", "needs_data"]


class Reel(BaseModel):
    format: Literal["Master DFB Formula", "Comparison Reveal"]
    series: str = Field(description="Content series, e.g. 'Shift I'm Seeing', 'Stop Calling Everything a Trend', 'Catwalk Decode', 'Brand Case Study'.")
    angle: str = Field(description="One-sentence summary of the tension/angle this Reel takes.")
    hook_on_screen_text: str = Field(description="The sound-off hook text shown in the first frame.")
    beats: List[Beat]
    full_script: str = Field(description="Full voiceover as one continuous read, ~30 seconds (about 75-90 words).")
    sentence_breakdown: List[SentenceCheck] = Field(description="Every sentence of full_script broken into components with a goal (section 6, layer 3). Sentences without a goal must have been cut before this point.")
    cut_lines: List[str] = Field(description="Lines you drafted but removed because they had no goal. Empty if none.")
    quotable_close: str = Field(description="The one line you want quoted in the comments.")
    comment_prompt: str = Field(description="Optional question to drive comments; empty string if none.")
    caption: str = Field(description="Instagram caption: 2-4 short lines, ending with a soft CTA to the Substack article.")
    hashtags: List[str]
    data_check: List[DataPoint] = Field(description="Every factual claim in the script and where it came from.")


class ReelPack(BaseModel):
    article_summary: str = Field(description="2-3 sentences: the article's core argument and its strongest data.")
    reels: List[Reel]
    filming_notes: List[str] = Field(description="Practical notes: B-roll to gather, charts to screenshot, data to confirm before posting.")


# ---------------------------------------------------------------------------
# Generation
# ---------------------------------------------------------------------------

SYSTEM_INSTRUCTIONS = """You write short-form video scripts (Instagram Reels / TikTok, ~30 seconds, 9:16) for DFB, a fashion data analyst's Substack. You turn one Substack article into Reels that follow the DFB Reels Formula below exactly.

How to work:
- Mine the article for its tension (a myth to correct, a lazy take to push back on, a "this isn't random" pattern), its named evidence (brands, dates, events, collections) and its hard numbers.
- Follow the beat structure and timing of the requested formula. No greetings, no "hey guys". The hook must work with sound off.
- Apply section 6 to every Reel: map the beats onto three acts (inicio with context and a problem, nudo ordered around attention peaks, desenlace with a conclusion or CTA), make the attention peaks climb toward the close instead of front-loading the best fact, and break every sentence into components with a goal. Cut any sentence with no goal.
- Speak as the analyst: specific, confident, receipts over vibes. Short spoken sentences — this is read aloud.
- Use only facts that appear in the article. Never invent statistics, dates, brand moves or percentages. If a beat needs a number or example the article doesn't have, write a clear bracketed placeholder like [NEEDS DATA: % change in orange SKUs vs last fall] and mark it needs_data in data_check.
- Make each Reel take a genuinely different angle on the article, not a rewording of the same script.
- Write in the same language as the article unless told otherwise.

<dfb_reels_formula>
{formula}
</dfb_reels_formula>"""


def build_request(article: Article, n_master: int, n_comparison: int, language: Optional[str], notes: Optional[str]) -> str:
    wanted = []
    if n_master:
        wanted.append(f"{n_master} Reel(s) using the Master DFB Formula (section 3)")
    if n_comparison:
        wanted.append(f"{n_comparison} Reel(s) using the Comparison Reveal formula (section 4)")
    parts = [f"Write {' and '.join(wanted)} from this article."]
    if n_comparison:
        parts.append("For a Comparison Reveal, only use it if the article contains (or clearly implies) two approaches to compare; otherwise build the closest honest version and flag missing data.")
    if language:
        parts.append(f"Write the scripts in {language}.")
    if notes:
        parts.append(f"Extra direction from the creator: {notes}")
    if article.paywalled:
        parts.append("Note: this post is paywalled, so the text below may be only the free preview.")
    header = "\n".join(
        line for line in [
            f"Title: {article.title}",
            f"Subtitle: {article.subtitle}" if article.subtitle else "",
            f"Published: {article.date}" if article.date else "",
            f"URL: {article.url}",
        ] if line
    )
    return "\n".join(parts) + f"\n\n<article>\n{header}\n\n{article.text}\n</article>"


def generate(client: anthropic.Anthropic, model: str, effort: str, article: Article, **kwargs) -> ReelPack:
    system = SYSTEM_INSTRUCTIONS.format(formula=FORMULA_PATH.read_text(encoding="utf-8"))
    # Streaming avoids HTTP timeouts on long outputs (several Reels + sentence breakdowns).
    with client.messages.stream(
        model=model,
        max_tokens=64000,
        # The formula is identical on every call, so cache it.
        system=[{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": build_request(article, **kwargs)}],
        thinking={"type": "adaptive"},
        output_config={"effort": effort},
        output_format=ReelPack,
        # If a safety classifier declines, retry server-side on Anthropic's recommended fallback model.
        extra_headers={"anthropic-beta": "server-side-fallback-2026-07-01"},
        extra_body={"fallbacks": "default"},
    ) as stream:
        response = stream.get_final_message()
    if response.stop_reason == "refusal":
        raise RuntimeError(f"Claude declined this article: {response.stop_details}")
    if response.stop_reason == "max_tokens":
        raise RuntimeError("Output was cut off (max_tokens). Try asking for fewer Reels at once.")
    if response.parsed_output is None:
        raise RuntimeError("Claude did not return a valid Reel pack.")
    return response.parsed_output


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

def render_markdown(article: Article, pack: ReelPack) -> str:
    out = [f"# Reels: {article.title}", ""]
    if article.url:
        out.append(f"Source: {article.url}" + (f" ({article.date})" if article.date else ""))
    out += ["", f"> {pack.article_summary}", ""]

    for i, reel in enumerate(pack.reels, 1):
        out += [
            "---",
            "",
            f"## Reel {i}: {reel.series} — {reel.format}",
            "",
            f"**Angle:** {reel.angle}",
            "",
            f"**Hook (on-screen, frame 1):** {reel.hook_on_screen_text}",
            "",
            "| Act | Beat | Time | Voiceover | On-screen text | Visual | Peak |",
            "|---|---|---|---|---|---|---|",
        ]
        for b in reel.beats:
            peak = "●" * max(0, min(b.attention_peak, 5)) + (f" {b.peak_reason}" if b.peak_reason else "")
            cells = [b.act, b.beat, b.timing, b.voiceover, b.on_screen_text, b.visual, peak]
            out.append("| " + " | ".join(c.replace("|", "/").replace("\n", " ") for c in cells) + " |")
        out += [
            "",
            "**Full script (read-through):**",
            "",
            reel.full_script,
            "",
            "**Sentence breakdown (every line has a job):**",
            "",
        ]
        for sc in reel.sentence_breakdown:
            parts = " + ".join(f"{c.part} _[{c.role}]_" for c in sc.components)
            out.append(f"- {parts} → **{sc.goal}**")
        if reel.cut_lines:
            out += ["", "**Cut (no goal):**", ""] + [f"- ~~{line}~~" for line in reel.cut_lines]
        out += [
            "",
            f"**Quotable close:** {reel.quotable_close}",
        ]
        if reel.comment_prompt:
            out.append(f"**Comment prompt:** {reel.comment_prompt}")
        out += [
            "",
            "**Caption:**",
            "",
            reel.caption,
            "",
            " ".join(h if h.startswith("#") else f"#{h}" for h in reel.hashtags),
            "",
            "**Data check:**",
            "",
        ]
        for d in reel.data_check:
            mark = "✅" if d.status == "from_article" else "⚠️ NEEDS DATA"
            out.append(f"- {mark} {d.claim} — _{d.source}_")
        out.append("")

    if pack.filming_notes:
        out += ["---", "", "## Filming notes", ""]
        out += [f"- {n}" for n in pack.filming_notes]
        out.append("")
    return "\n".join(out)


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:60] or "article"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Generate Reels scripts from Substack articles using the DFB Reels Formula.")
    parser.add_argument("url", nargs="?", help="Substack post URL, or publication URL when used with --latest.")
    parser.add_argument("--file", help="Use a local .md/.txt/.html file instead of a URL (e.g. drafts or paid posts).")
    parser.add_argument("--latest", type=int, metavar="N", help="Generate for the N most recent posts of the publication.")
    parser.add_argument("--master", type=int, default=2, help="Number of Master DFB Formula Reels per article (default 2).")
    parser.add_argument("--comparison", type=int, default=1, help="Number of Comparison Reveal Reels per article (default 1).")
    parser.add_argument("--language", help="Script language (default: same as the article).")
    parser.add_argument("--notes", help="Extra direction, e.g. 'focus on the Prada data' or 'more playful hooks'.")
    parser.add_argument("--out", default="output", help="Output folder (default: output/).")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"Claude model (default {DEFAULT_MODEL}).")
    parser.add_argument("--effort", default="high", choices=["low", "medium", "high", "xhigh", "max"])
    args = parser.parse_args(argv)

    if not args.file and not args.url:
        parser.error("give a Substack URL or --file")
    if args.master + args.comparison < 1:
        parser.error("ask for at least one Reel")

    if args.file:
        articles = [load_file(args.file)]
    elif args.latest:
        articles = [fetch_post(u) for u in latest_post_urls(args.url, args.latest)]
    else:
        articles = [fetch_post(args.url)]

    client = anthropic.Anthropic()
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    failures = 0
    for article in articles:
        if len(article.text) < 200:
            print(f"⚠️  Skipping '{article.title}': almost no text found (paywalled or empty?). Try --file.", file=sys.stderr)
            failures += 1
            continue
        print(f"🎬 Generating Reels for: {article.title}", file=sys.stderr)
        try:
            pack = generate(
                client, args.model, args.effort, article,
                n_master=args.master, n_comparison=args.comparison,
                language=args.language, notes=args.notes,
            )
        except (anthropic.APIError, RuntimeError) as e:
            print(f"❌ {article.title}: {e}", file=sys.stderr)
            failures += 1
            continue

        base = out_dir / slugify(article.title)
        base.with_suffix(".md").write_text(render_markdown(article, pack), encoding="utf-8")
        base.with_suffix(".json").write_text(json.dumps(pack.model_dump(), indent=2, ensure_ascii=False), encoding="utf-8")
        needs = sum(d.status == "needs_data" for r in pack.reels for d in r.data_check)
        print(f"   ✅ {len(pack.reels)} Reels → {base.with_suffix('.md')}" + (f"  ({needs} data gaps to fill)" if needs else ""), file=sys.stderr)

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
