# DFB Reels Generator

Turns your Substack articles into ~30-second Reels scripts that follow the **DFB Reels Formula** (`prompts/dfb_reels_formula.md`).

For each article you get a Markdown file (plus JSON) in `output/` with:

- **2 × Master DFB Formula Reels** (Hook → Thesis → Evidence 1 → Evidence 2 → Hard stat → Zoom out → Close), each with a different angle
- **1 × Comparison Reveal Reel** (guess which brand won → reveal → mechanism)
- A beat-by-beat table per Reel: act (inicio / nudo / desenlace), timing, voiceover, on-screen text (works with sound off), visual/B-roll, and an **attention-peak** score so you can see the interest climbing toward the close
- A **sentence breakdown**: every line split into its components (characteristic, result, data…) with the goal it serves, plus any lines that were cut for having no goal
- A full read-through script, quotable close, comment prompt, caption, and hashtags
- A **data check**: every claim is traced back to the article. Anything the formula needs but the article doesn't have shows up as `[NEEDS DATA: …]` — the generator never makes up numbers.
- Filming notes (B-roll to gather, charts to screenshot, data to confirm)

## Setup

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...   # from https://console.anthropic.com
```

## Usage

```bash
# One post
python reels.py https://yourname.substack.com/p/your-post-slug

# Your 3 most recent posts
python reels.py --latest 3 https://yourname.substack.com

# A draft or a paid post (paste the text into a file first)
python reels.py --file draft.md
```

Options:

| Flag | What it does |
|---|---|
| `--master N` | Number of Master Formula Reels (default 2) |
| `--comparison N` | Number of Comparison Reveal Reels (default 1; use `0` to skip) |
| `--language Spanish` | Write scripts in a specific language (default: same as the article) |
| `--notes "..."` | Extra direction, e.g. `"focus on the Prada numbers"` or `"more provocative hooks"` |
| `--out folder` | Where to save results (default `output/`) |
| `--effort low…max` | How hard Claude thinks (default `high`) |
| `--model` | Claude model (default `claude-opus-5`) |

Paid posts: Substack only exposes the free preview publicly, so use `--file` with the full text.

## Updating the formula

Edit `prompts/dfb_reels_formula.md`. The generator reads it on every run.
