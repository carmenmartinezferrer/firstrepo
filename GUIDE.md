# DFB skills guide: which repo, which branch, what to say

Last checked: 2 November 2026. Everything below was read from the actual branches, not from memory.

---

## 0. Why you keep getting lost (read this once)

Every Claude Code web session does two things:

1. It **starts from a branch you pick** when you create the session (the dropdown next to the repo name). If you don't pick one, it uses the repo's default branch.
2. It **saves its work on a new branch** called `claude/<two-random-words>`, and that branch is never merged back unless you (or Claude) open and merge a pull request.

Skills only load from the `.claude/skills/` folder of **the branch the session started from**. So the skills you see depend entirely on which branch you picked.

Since 1 October nothing has been merged. The result today:

| Repo | Default branch | Skills on the default branch | Skills that only exist on other branches |
|---|---|---|---|
| `firstrepo` | `claude/busy-einstein-eini0p` (there is no `main`) | 2 (catwalk decode, reels) | 10 more, spread over 7 branches |
| `dfb-data` | `main` | 1 (dataset), but only one show of data | 2 more skills and 16 shows of data on 5 branches |

That is the whole problem: when you start a session on the default branch, 10 of your 12 content skills are not there, and Claude either improvises or says it can't.

**Short-term fix:** use the cheat sheet in section 2 to start on the right branch.
**Long-term fix:** merge every branch into one (section 6). Then the branch question disappears and this guide shrinks to "which prompt".

---

## 1. Your repos

| Repo | What it is | Use it for |
|---|---|---|
| **`carmenmartinezferrer/firstrepo`** | The content studio. All the writing, Reels, carousel, Canva, media kit and calendar skills. | Anything you publish or send: Instagram decodes, Reels, Substack, FashionUnited, weekly shifts, media kit, calendar. |
| **`carmenmartinezferrer/dfb-data`** | The research dataset. One JSON per show, tagged look by look, built into Excel workbooks. Plus the two Canva carousel skills. | Tagging a show for Substack analysis, answering "what % of Paris SS27 was…", building a data carousel in Canva. |
| `carmenmartinezferrer/dfb-trend-tagger` | The DFB Trend Tagger web page (one `index.html`, GitHub Pages). No skills. | Only when you want to change the tagger tool itself. |
| `carmenmartinezferrer/thedatafashionbrief` | Old, last touched May 2026. No skills. | Ignore. |

Rule of thumb: **Instagram and publishing = firstrepo. Tagging looks and dataset questions = dfb-data.**

---

## 2. Cheat sheet: "I want to…"

Pick the row, start the session on that repo and branch, then use one of the prompts from section 4.

| I want to… | Skill | Repo | Start the session on this branch |
|---|---|---|---|
| Decode a runway show for Instagram (palette %, silhouettes, codes, caption, Canva) | `dfb-catwalk-decode` | firstrepo | `claude/wizardly-knuth-wqx45j` (has the current Canva template ID; see the warning in 4.1) |
| Turn a Substack post into Reels scripts | `dfb-reels` | firstrepo | `claude/pinterest-summer-2026-trends-wkwxq6` (newest version, saves to Drive) or any branch |
| Write or edit a regular Substack post, or a "Behind The Data Fashion Brief" edition | `dfb-substack` | firstrepo | `claude/blissful-tesla-xi20u5` |
| Get the Sunday "5 shifts" pack (Substack + carousel + Reel) | `dfb-weekly-shifts` | firstrepo | `claude/dfb-weekly-research-jxozhm` (newest, with the wider-press sweep) |
| Build a Runway Colour Combos carousel (model cut-outs, hex swatches) | `runway-colour-combos` | firstrepo | `claude/blissful-tesla-xi20u5` or `claude/pinterest-summer-2026-trends-wkwxq6` (same version) |
| Write a Runway Decode Trend Report for Substack (materials, silhouettes, search chart, matrix) | `runway-decode-trends` | firstrepo | `claude/pinterest-summer-2026-trends-wkwxq6` |
| Write a Runway Decode Colour Index for Substack (season palette, house donuts, over-indexing) | `runway-decode-colour` | firstrepo | `claude/pinterest-summer-2026-trends-wkwxq6` |
| Write a FashionUnited trade article (or revise one from editor feedback) | `fashionunited-article` | firstrepo | `claude/pinterest-summer-2026-trends-wkwxq6` |
| Write a personal essay (career, fashion week learnings, no charts) | `dfb-personal-essay` | firstrepo | `claude/pinterest-summer-2026-trends-wkwxq6` |
| Refresh the media kit PDF and Canva (1st and 15th) | `dfb-media-kit` | firstrepo | `claude/adoring-bohr-tfqlfp` |
| Put a deadline, meeting or reminder in Notion / Google Calendar | `calendar-assistant` | firstrepo | `claude/adoring-euler-fw5j2s` |
| Tag a show into the research dataset (for Substack numbers) | `dfb-dataset` | dfb-data | `claude/peaceful-lamport-gou66k` (has all 16 Paris SS27 shows; `main` only has Chanel) |
| Build a data carousel in Canva (Google Trends, results, dataset) | `dfb-carousel` | dfb-data | `claude/bold-pascal-hboypv` |
| Build a personal / "Behind DFB" carousel in Canva | `dfb-personal-carousel` | dfb-data | `claude/adoring-euler-fw5j2s` |

One branch covers the most ground: **`claude/pinterest-summer-2026-trends-wkwxq6`** holds 6 skills (reels, colour combos, decode trends, decode colour, FashionUnited, personal essay) plus the editorial style guide (`CLAUDE.md`) and your reference articles. But it does **not** have catwalk decode, Substack, weekly shifts, media kit or calendar.

---

## 3. How to start a session on the right branch

**In the Claude Code web app (claude.ai/code):**

1. New session → choose the repo (`firstrepo` or `dfb-data`).
2. Open the branch selector (it shows the default branch name) and pick the branch from the cheat sheet.
3. Type your prompt. The skill loads automatically when your message matches its description, so you don't need to name it. Naming it does no harm: "use the dfb-reels skill".

**If you forgot, or you're already in a session on the wrong branch,** paste this as your first message (replace the branch and skill):

```
Fetch and check out origin/claude/pinterest-summer-2026-trends-wkwxq6, then read
.claude/skills/fashionunited-article/SKILL.md and follow it for this task.
```

Claude can read the skill file and follow it even though it wasn't loaded at startup.

**At the end of a session,** if you want the work kept, say: "commit and push" (always safe) and, if the work should become the new normal, "open a pull request into the default branch". Until merged, the next session won't see it.

---

## 4. Skill by skill: what it needs, what to say

Prompts are examples. Casual wording works; what matters is that the inputs are there.

### 4.1 `dfb-catwalk-decode` (Instagram decode)

- **Repo / branch:** firstrepo / `claude/wizardly-knuth-wqx45j`
- **Attach:** every Vogue Runway screenshot of the show, in runway order, with the Vogue Runway header visible (brand, city, season are read from it). Don't crop off rows.
- **Connectors:** Canva (to fill the "Catwalk analysis" template).
- **Prompts:**
  - "Decode Balmain SS27. Here are the screenshots." *(paste images)*
  - "Here are the Dries screenshots, do the full decode and the Canva."
  - "Which silhouettes dominated at Chanel? Palette and materials too, with the caption."
  - "Midi tracker: add Valentino and give me the cross-brand bar chart."
- **You get:** show type + look count, palette / silhouette / material %, trends, "The codes are: …", the palette donut PNG in `exports/<season>/`, the Canva copy filled, the caption in your voice.
- **Warnings:**
  - The original Canva template `DAHWx3H429E` was **deleted on 30 Oct**. The new master is `DAHZS6ez0MM`. Only the `wizardly-knuth` branch knows this. On any other branch, say in your prompt: "the Canva template is DAHZS6ez0MM, work on a copy".
  - The SS27 decodes for Celine, Chanel, Chloé, Isabel Marant, Loewe, Miu Miu, Mugler and Valentino live only on `claude/sweet-turing-b1i9ud`, together with a newer house-style note (no emoji bullet lists in captions). The Prada SS21 decode lives only on `wizardly-knuth`. Merging these two branches is the first item in section 6.
  - Season log still flags Dior SS27 as having two sets of numbers, and Balmain and Dries as pending.

### 4.2 `dfb-reels` (Reels / TikTok scripts)

- **Repo / branch:** firstrepo / `claude/pinterest-summer-2026-trends-wkwxq6` for the newest version. The older version is on every branch, so this one always works.
- **Attach:** the Substack URL, or paste the text (paywalled posts need the text pasted), or a draft.
- **Connectors:** Google Drive (newest version saves a Google Doc to DFB > Reels).
- **Prompts:**
  - "Make Reels from this post: https://thedatafashionbrief.substack.com/p/…"
  - "Turn this draft into a video script, 2 master formula + 1 comparison reveal." *(paste text)*
  - "Guion para un reel de este artículo, en español."
  - "Review my Reel script, don't rewrite it, tell me what to cut." *(paste script)*
- **You get:** 2 Master "Shift I'm Seeing" Reels + 1 Comparison Reveal, each as a beat table (act, time, voiceover, on-screen text, visual, attention peak), full read-through, sentence breakdown, caption, data check with `[NEEDS DATA]` flags, filming notes.
- **Batch option:** `python reels.py --latest 3 https://thedatafashionbrief.substack.com` on your computer (needs an Anthropic API key).

### 4.3 `dfb-substack` (regular Substack posts)

- **Repo / branch:** firstrepo / `claude/blissful-tesla-xi20u5`
- **Attach:** your notes, a voice-note transcript, a rough draft, or the data you want to use. Topic only = Claude asks for your angle first.
- **Prompts:**
  - "Write a Substack post about Prada's Q3 results. Here are my notes." *(paste)*
  - "Turn this voice note into an article." *(paste transcript)*
  - "Edit my draft, keep my wording, just fix what's unclear." *(paste)*
  - "Behind The Data Fashion Brief this week: how I got into fashion data. Give me the article, the Reel and the carousel."
  - "What should I call this post? Three options and a subtitle."
- **You get:** post (title, subtitle, body, sign-off), title alternatives, things to check, 1 to 3 illustration ideas. For the Behind DFB series: article + Reel + 6 to 8 slide carousel.
- **Rules it enforces:** never names your current employer, never your university, no invented numbers, British spelling.

### 4.4 `dfb-weekly-shifts` (Sunday pack)

- **Repo / branch:** firstrepo / `claude/dfb-weekly-research-jxozhm`
- **Attach:** nothing. It reads your Gmail newsletters and searches the web.
- **Connectors:** Gmail, Google Drive (saves to DFB / Weekly Briefings), web search.
- **Prompts:**
  - "Weekly shifts for this week."
  - "This week in fashion data, the five shifts, and save the doc."
  - "Run the weekly shifts but make shift 3 about the Hermès slowdown."
- **You get:** one Google Doc with SUBSTACK (5 shifts, 60 to 90 words each), CAROUSEL (7 slides), REEL (about 45 seconds), BEHIND THE SCENES (sources, nearly-made-it), plus a 3 to 4 line report in chat.
- **Note:** the version on `claude/blissful-tesla-xi20u5` is missing the wider-press sweep (FT, Bloomberg, Jing Daily, Drapers…) that you asked for on 1 Nov. Use `dfb-weekly-research`.

### 4.5 `runway-colour-combos` (Instagram colour carousel)

- **Repo / branch:** firstrepo / `claude/blissful-tesla-xi20u5` or `claude/pinterest-summer-2026-trends-wkwxq6` (identical)
- **Attach:** Vogue Runway app screenshots of single looks (header visible so Claude knows brand and look number). Optionally a Google Trends CSV for the closing slide.
- **Connectors:** Canva.
- **Prompts:**
  - "Colour combinations for these looks." *(paste screenshots)*
  - "Remove the background and give me the hex codes for these three."
  - "Purple carousel: here are 6 looks and the Google Trends CSV for 'purple dress'. Fill the Canva deck."
  - "Feedback on the deck before I post."
- **You get:** model cut-outs (transparent PNG), sampled hex per garment, Pantone-style swatch cards, the Canva carousel filled, a handover table and the standing notes (hex from photo not Pantone, image licences).

### 4.6 `runway-decode-trends` (Substack trend report)

- **Repo / branch:** firstrepo / `claude/pinterest-summer-2026-trends-wkwxq6`
- **Attach:** the tagging spreadsheet (from dfb-data, e.g. `build/SS27/SS27-paris.xlsx`, or a Catwalk Decode export) and a Google Trends export for the search comparison. Runway photos if you want the Canva look collage filled.
- **Prompts:**
  - "Trend report for Paris SS27 from this workbook. Text only first." *(attach xlsx)*
  - "Stop Calling Everything a Trend: Milan edition. Here's the data."
  - "Add the search comparison chart: midi skirt vs slip dress, same scale."
  - "Put these six looks in the PFW collage."
- **Workflow it follows:** text first, you correct it, then charts and HTML. It will not build visuals before you approve the text.

### 4.7 `runway-decode-colour` (Substack colour index)

- **Repo / branch:** firstrepo / `claude/pinterest-summer-2026-trends-wkwxq6`
- **Attach:** the colour data: the workbook's "Colour mix donut" tab, a colours CSV, or your manual per-brand colour %.
- **Prompts:**
  - "Give me the colour piece for Paris SS27." *(attach data)*
  - "Rebuild the season palette and swap in the Loewe donut."
  - "Does the red finding hold up against what the press said?"
- **You get:** season palette, per-house donuts, swatch grid, per-colour over-indexing deep dive, in the same voice as the trend report.

### 4.8 `fashionunited-article` (trade article)

- **Repo / branch:** firstrepo / `claude/pinterest-summer-2026-trends-wkwxq6`
- **Attach:** the finished DFB piece the data comes from, and any editor feedback.
- **Prompts:**
  - "FashionUnited version of the maximalism piece, about 600 words, four image slots."
  - "The editor sent this feedback on the denim draft, revise it." *(paste feedback)*
  - "Pitch for FashionUnited from the Paris colour index."
- **Rules it enforces:** news first, third person, DFB cited as a source, no first person, no other outlet names in the body, no exclamation points, licensed images only (PR, AFP, Launchmetrics).

### 4.9 `dfb-personal-essay` (no-data pieces)

- **Repo / branch:** firstrepo / `claude/pinterest-summer-2026-trends-wkwxq6`
- **Attach:** your story notes. It will ask what the actual story is, not just the topic.
- **Prompts:**
  - "I want to write something more personal about what I learned this fashion week."
  - "An essay about my career, Zara to Net-a-Porter to now. Not analytical."
- **You get:** a narrative piece in your loose, funny register, no methodology section, facts still checked.

### 4.10 `dfb-media-kit` (15-day refresh)

- **Repo / branch:** firstrepo / `claude/adoring-bohr-tfqlfp` (the only branch with `media-kit/`)
- **Attach:** nothing for a normal refresh. New Substack stats = the Stats screenshot in Drive. New partnership = the row in your 260921_DFB_Growth sheet.
- **Connectors:** Instagram API token (`graph.instagram.com`), Google Drive, Canva. Not Metricool (your 19 Oct instruction).
- **Prompts:**
  - "Refresh the media kit."
  - "Media kit: Substack is at 8.3k subscribers, update it."
  - "Add DeMellier as a partnership and rebuild."
  - "Typo check on the Canva media kit."
- **You get:** updated `media-kit/data.json` and `stats_history.csv`, the 2-page PDF sent in chat, Canva numbers updated in place, a short summary of what moved.
- **Deadline:** the Instagram token **expires around 26 November 2026**. Renew it in the app dashboard (Instagram → API setup with Instagram login → Generate token) and store it in the environment, never paste it in chat.

### 4.11 `calendar-assistant`

- **Repo / branch:** firstrepo / `claude/adoring-euler-fw5j2s`
- **Connectors:** Notion ("My Calendar" database), Google Calendar.
- **Prompts:**
  - "FashionUnited wants the maximalism piece by Friday."
  - "Call with Patricia Tuesday at 3."
  - "What's due this week?"
  - "I sent the article" / "Move the denim deadline to the 12th."
- **You get:** one or two lines confirming the item, the exact date and the Notion link. DFB posts go to the Posting calendar, ideas to Idea cards, freelance deadlines to My Calendar.

### 4.12 `dfb-dataset` (research dataset)

- **Repo / branch:** dfb-data / `claude/peaceful-lamport-gou66k` (16 Paris SS27 shows). `main` has only Chanel. Prada SS21 is only on `claude/determined-noether-opp02p`.
- **Attach:** one house per message: the house name + its Vogue Runway screenshots.
- **Prompts:**
  - "Dior SS27." *(paste screenshots)*
  - "Add Lanvin, Paris SS27, here are the looks."
  - "What share of Paris SS27 looks were black? With counts."
  - "Fix Chanel SS27: look 14 is tweed, not bouclé."
- **You get:** the look log to check, `data/<season>/<city>/<house>.json`, rebuilt workbooks (`build/SS27/SS27-paris.xlsx` sent to you), palette slices, top materials and formulas, committed and pushed.
- **Not this skill:** charts, captions, Canva. Those are `dfb-catwalk-decode` in firstrepo.

### 4.13 `dfb-carousel` (data carousel in Canva)

- **Repo / branch:** dfb-data / `claude/bold-pascal-hboypv`
- **Attach:** a Google Trends CSV, company results, or the dataset numbers. Cut-out images if you have them.
- **Connectors:** Canva.
- **Prompts:**
  - "Carousel on the ballet flat, here's the Trends export." *(attach CSV)*
  - "DeMellier carousel: made in Spain, +65% revenue, searches 4x. Build it in Canva."
  - "5 slides, title asks the question, last slide answers it."
- **You get:** the slide plan for your OK, then the Canva design (5 slides, 6 max), charts as PNGs with labels left as Canva elements, caption, and `carousels/<yyyy-mm>-<slug>/README.md`.

### 4.14 `dfb-personal-carousel` (Behind DFB carousel in Canva)

- **Repo / branch:** dfb-data / `claude/adoring-euler-fw5j2s`
- **Attach:** your photos (HEIC is fine) and the story.
- **Connectors:** Canva.
- **Prompts:**
  - "Personal carousel: how I got into fashion data without a tech degree."
  - "Hi, I'm Carmen re-intro carousel for 30k, here are my photos."
- **You get:** 6 to 9 slides from the "Every decision in fashion is based on data" reference design, caption, README in `carousels/`.

---

## 5. Routines and dates

| When | What | Where |
|---|---|---|
| Every Sunday | Weekly shifts pack | firstrepo, `claude/dfb-weekly-research-jxozhm` |
| 1st and 15th | Media kit refresh | firstrepo, `claude/adoring-bohr-tfqlfp` |
| Around 26 Nov 2026 | Instagram API token expires. Renew a week before. | Instagram app dashboard |
| Every decode | Add the brand to `season-log.md`, export the palette PNG | firstrepo |
| Every show tagged | Rebuild and push `build/` | dfb-data |

---

## 6. The tangles to fix (so this guide gets shorter)

All of this disappears if the branches are merged into one. In order of value:

1. **firstrepo: merge `sweet-turing` + `wizardly-knuth` into the default branch.** Then one catwalk-decode branch has all 11 SS27 decodes, Prada SS21, the current Canva template ID and the latest house style.
2. **firstrepo: merge `dfb-weekly-research`, `blissful-tesla`, `adoring-euler`, `adoring-bohr`.** They are all built on top of the default branch, so they should merge cleanly. That brings Substack, weekly shifts, colour combos, calendar and the media kit together.
3. **firstrepo: merge `pinterest-summer-2026-trends`.** This one needs care: it was built on a much older base, deleted `README.md` and `.gitignore`, and has no catwalk-decode folder. Its `CLAUDE.md` (editorial style guide) is worth keeping as the repo's style guide for every skill.
4. **firstrepo: rename the default branch to `main`.** A default branch called `claude/busy-einstein-eini0p` is part of why this is confusing.
5. **dfb-data: merge `peaceful-lamport` (16 shows) + `determined-noether` (Prada SS21) + `bold-pascal` + `adoring-euler` + `blissful-tesla` into `main`.** Rebuild `build/` once after merging rather than resolving conflicts in the generated Excel files.
6. **Decide where the carousel skills live.** `dfb-carousel` and `dfb-personal-carousel` are in dfb-data because they use the dataset, but every other publishing skill is in firstrepo. One repo for all skills would mean one branch to remember.

After that, the cheat sheet becomes: **firstrepo `main` for everything you publish, dfb-data `main` for tagging shows.**
