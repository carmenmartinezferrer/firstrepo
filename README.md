# The Data Fashion Brief: content studio

Everything Carmen publishes for DFB is built from this repo with Claude Code. Start every session on the **`main`** branch.

**Not sure what to say, or which skill does what? Read [`GUIDE.md`](GUIDE.md).** It lists every skill, what to attach and example prompts.

| Skill (`.claude/skills/…`) | What it makes |
|---|---|
| `dfb-catwalk-decode` | Instagram catwalk decode from Vogue Runway screenshots: palette, silhouettes, materials, codes, caption, Canva |
| `dfb-reels` | Reels / TikTok scripts from a Substack post (DFB Reels Formula) |
| `dfb-substack` | Regular Substack posts and the "Behind The Data Fashion Brief" series |
| `dfb-weekly-shifts` | The Sunday "5 shifts in fashion" pack: Substack + carousel + Reel, saved to Drive |
| `runway-colour-combos` | Runway Colour Combos carousel: model cut-outs, hex swatches, Canva |
| `runway-decode-trends` | Runway Decode Trend Report for Substack (materials, silhouettes, search chart, matrix) |
| `runway-decode-colour` | Runway Decode Colour Index for Substack (season palette, donuts, over-indexing) |
| `fashionunited-article` | Trade articles for FashionUnited in its house voice |
| `dfb-personal-essay` | Personal, no-data essays |
| `dfb-media-kit` | The two-page media kit PDF and its Canva copy, refreshed on the 1st and 15th |
| `calendar-assistant` | Deadlines, meetings and reminders into Notion and Google Calendar |

`CLAUDE.md` is the editorial style guide (voice, non-negotiables, workflow) that applies to every skill.

The research dataset (tagging shows look by look) and the two Canva carousel skills live in the separate repo **`dfb-data`**.

## Folders

| Folder | What's in it |
|---|---|
| `exports/` | Finished outputs: palette PNGs per season, Substack drafts, series images |
| `drafts/` | Work in progress per piece (charts, models, swatches, article drafts) |
| `reference-articles/` | Carmen's approved pieces, used as voice references |
| `media-kit/` | The media kit data, build script, fonts and PDF |
| `carousel/`, `outreach/`, `prompts/` | Carousel plans, outreach tracker, the Reels formula |

---

## DFB Reels Generator (command line)

Turns your Substack articles into ~30-second Reels scripts that follow the **DFB Reels Formula** (`prompts/dfb_reels_formula.md`).

For each article you get a Markdown file (plus JSON) in `output/` with:

- **2 × Master DFB Formula Reels** (Hook → Thesis → Evidence 1 → Evidence 2 → Hard stat → Zoom out → Close), each with a different angle
- **1 × Comparison Reveal Reel** (guess which brand won → reveal → mechanism)
- A beat-by-beat table per Reel: act (inicio / nudo / desenlace), timing, voiceover, on-screen text (works with sound off), visual/B-roll, and an **attention-peak** score so you can see the interest climbing toward the close
- A **sentence breakdown**: every line split into its components (characteristic, result, data…) with the goal it serves, plus any lines that were cut for having no goal
- A full read-through script, quotable close, comment prompt, caption, and hashtags
- A **data check**: every claim is traced back to the article. Anything the formula needs but the article doesn't have shows up as `[NEEDS DATA: …]` — the generator never makes up numbers.
- Filming notes (B-roll to gather, charts to screenshot, data to confirm)

### Setup

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...   # from https://console.anthropic.com
```

### Usage

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

### Updating the formula

Edit `prompts/dfb_reels_formula.md`. The generator reads it on every run.

### Catwalk decode skill

`.claude/skills/dfb-catwalk-decode/` turns Vogue Runway screenshots into a DFB catwalk decode: look count, palette / silhouette / material shares, trends and "The codes are: …", donut and bar charts (`scripts/dfb_charts.py`), and a filled copy of the Canva "Catwalk analysis" template. The season log with trackers and pending brands lives in `references/season-log.md`.

### Weekly shifts skill

`.claude/skills/dfb-weekly-shifts/` builds the Sunday pack: five fashion shifts from the week's newsletters (BoF, Vogue Business, WWD, Retail Dive, Puck, Modem Online, Modaes, All Things Fashion Tech) plus your own recent Substack posts, written three ways (Substack section, "I'm a fashion data analyst, these are the 5 shifts I'm seeing" carousel, and a Reel script). It saves one Google Doc to Drive › DFB / Weekly Briefings, and a scheduled task runs it every Sunday morning.
