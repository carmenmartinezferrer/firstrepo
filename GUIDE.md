# DFB skills guide: which repo, what to say

Last updated: 8 November 2026, added the `dfb-invoice` skill.

---

## 0. The two rules

1. **Always start a session on the `main` branch.** Both repos. Every skill now lives there.
2. **At the end of a session, say "merge this into main".** Claude Code saves each session's work on its own `claude/<two-words>` branch. Until it's merged, the next session won't see it. If you forget, nothing is lost: the work sits on that branch and the next session can merge it.

Which repo:

| Repo | Use it for |
|---|---|
| **`firstrepo`** | Everything you publish or send: Instagram decodes, Reels, Substack, FashionUnited, weekly shifts, media kit, calendar, invoices. 12 skills. |
| **`dfb-data`** | Tagging shows into the research dataset, dataset questions, and the two Canva carousel skills. 3 skills. |

`dfb-trend-tagger` is the tagger web page and `thedatafashionbrief` is old. Neither has skills.

---

## 1. Cheat sheet: "I want to…"

| I want to… | Repo | Skill | Say something like |
|---|---|---|---|
| Decode a runway show for Instagram | firstrepo | `dfb-catwalk-decode` | "Decode Balmain SS27" + screenshots |
| Turn a Substack post into Reels | firstrepo | `dfb-reels` | "Make Reels from this post" + link or text |
| Write or edit a Substack post, or a Behind DFB edition | firstrepo | `dfb-substack` | "Write a Substack post about…" + notes |
| The Sunday "5 shifts" pack | firstrepo | `dfb-weekly-shifts` | "Weekly shifts for this week" |
| A Runway Colour Combos carousel (cut-outs, hex swatches) | firstrepo | `runway-colour-combos` | "Colour combinations for these looks" + screenshots |
| A Runway Decode Trend Report for Substack | firstrepo | `runway-decode-trends` | "Trend report for Paris SS27, text first" + workbook |
| A Runway Decode Colour Index for Substack | firstrepo | `runway-decode-colour` | "The colour piece for Paris SS27" + colour data |
| A FashionUnited article or a revision | firstrepo | `fashionunited-article` | "FashionUnited version of the maximalism piece" |
| A personal essay, no charts | firstrepo | `dfb-personal-essay` | "Something more personal about…" |
| Refresh the media kit (1st and 15th) | firstrepo | `dfb-media-kit` | "Refresh the media kit" |
| Put a deadline or meeting in Notion / Google Calendar | firstrepo | `calendar-assistant` | "FashionUnited wants the piece by Friday" |
| Make an invoice, or see what I've invoiced | firstrepo | `dfb-invoice` | "Invoice FashionUnited 600 euros for the maximalism piece" |
| Tag a show into the dataset | dfb-data | `dfb-dataset` | "Dior SS27" + screenshots, one house per message |
| Ask the dataset a question | dfb-data | `dfb-dataset` | "What share of Paris SS27 looks were black?" |
| A data carousel in Canva (Trends CSV, results) | dfb-data | `dfb-carousel` | "Carousel on the ballet flat" + CSV |
| A personal / Behind DFB carousel in Canva | dfb-data | `dfb-personal-carousel` | "Personal carousel: how I got into fashion data" + photos |

You don't need to name the skill. It loads when your message matches. Naming it ("use dfb-reels") also works.

---

## 2. Skill by skill: what it needs, what to say

### 2.1 `dfb-catwalk-decode` (Instagram decode)

- **Attach:** every Vogue Runway screenshot of the show, in runway order, header visible (brand, city and season are read from it). Don't crop off rows.
- **Connectors:** Canva.
- **Prompts:**
  - "Decode Balmain SS27. Here are the screenshots."
  - "Here are the Dries screenshots, do the full decode and the Canva."
  - "Which silhouettes dominated at Chanel? Palette and materials too, with the caption."
  - "Midi tracker: add Valentino and give me the cross-brand bar chart."
- **You get:** show type + look count, palette / silhouette / material %, trends, "The codes are: …", the palette donut PNG in `exports/<season>/`, the Canva copy filled, the caption in your voice.
- **Open items in the season log:** Dior SS27 has two sets of numbers to reconcile. Balmain and Dries Van Noten are still pending screenshots.
- **Canva template:** the current master is `DAHZS6ez0MM` (the old `DAHWx3H429E` was deleted on 30 Oct). The skill works on a copy.

### 2.2 `dfb-reels` (Reels / TikTok scripts)

- **Attach:** the Substack URL, or paste the text (paywalled posts need the text), or your draft.
- **Connectors:** Google Drive (saves a Google Doc to DFB > Reels).
- **Prompts:**
  - "Make Reels from this post: https://thedatafashionbrief.substack.com/p/…"
  - "Turn this draft into a video script, 2 master formula + 1 comparison reveal."
  - "Guion para un reel de este artículo, en español."
  - "Review my Reel script, don't rewrite it, tell me what to cut."
- **You get:** 2 Master "Shift I'm Seeing" Reels + 1 Comparison Reveal as beat tables (act, time, voiceover, on-screen text, visual, attention peak), read-through, sentence breakdown, caption, data check with `[NEEDS DATA]` flags, filming notes.
- **Batch option:** `python reels.py --latest 3 https://thedatafashionbrief.substack.com` on your computer (needs an Anthropic API key).

### 2.3 `dfb-substack` (regular Substack posts)

- **Attach:** notes, a voice-note transcript, a rough draft, or the data. Topic only = Claude asks for your angle first.
- **Prompts:**
  - "Write a Substack post about Prada's Q3 results. Here are my notes."
  - "Turn this voice note into an article."
  - "Edit my draft, keep my wording, just fix what's unclear."
  - "Behind The Data Fashion Brief this week: how I got into fashion data. Article, Reel and carousel."
  - "What should I call this post? Three options and a subtitle."
- **You get:** post (title, subtitle, body, sign-off), title alternatives, things to check, 1 to 3 illustration ideas. Behind DFB = article + Reel + 6 to 8 slide carousel.
- **Rules it enforces:** never names your current employer or university, no invented numbers, British spelling.

### 2.4 `dfb-weekly-shifts` (Sunday pack)

- **Attach:** nothing. It reads your Gmail newsletters, searches the eight outlets plus the wider press, and reads last week's doc so it doesn't repeat.
- **Connectors:** Gmail, Google Drive (DFB / Weekly Briefings), web search.
- **Prompts:**
  - "Weekly shifts for this week."
  - "This week in fashion data, the five shifts, save the doc."
  - "Run the weekly shifts but make shift 3 about the Hermès slowdown."
- **You get:** one Google Doc with SUBSTACK (5 shifts, 60 to 90 words each), CAROUSEL (7 slides), REEL (about 45 seconds), BEHIND THE SCENES, plus a 3 to 4 line report in chat.

### 2.5 `runway-colour-combos` (Instagram colour carousel)

- **Attach:** Vogue Runway app screenshots of single looks, header visible. Optionally a Google Trends CSV for the closing slide.
- **Connectors:** Canva.
- **Prompts:**
  - "Colour combinations for these looks."
  - "Remove the background and give me the hex codes for these three."
  - "Purple carousel: 6 looks and the Trends CSV for 'purple dress'. Fill the Canva deck."
  - "Feedback on the deck before I post."
- **You get:** model cut-outs (transparent PNG), sampled hex per garment, Pantone-style swatch cards, the Canva carousel filled, a handover table and the standing notes (hex from photo not Pantone, image licences).

### 2.6 `runway-decode-trends` (Substack trend report)

- **Attach:** the tagging workbook from dfb-data (`build/SS27/SS27-paris.xlsx`) or a Catwalk Decode export, plus a Google Trends export for the search comparison. Runway photos if you want the Canva look collage filled.
- **Prompts:**
  - "Trend report for Paris SS27 from this workbook. Text only first."
  - "Stop Calling Everything a Trend: Milan edition. Here's the data."
  - "Add the search comparison chart: midi skirt vs slip dress, same scale."
  - "Put these six looks in the PFW collage."
- **Workflow it follows:** text first, you correct it, then charts and HTML. No visuals before you approve the text.

### 2.7 `runway-decode-colour` (Substack colour index)

- **Attach:** the colour data: the workbook's "Colour mix donut" tab, a colours CSV, or your manual per-brand colour %.
- **Prompts:**
  - "Give me the colour piece for Paris SS27."
  - "Rebuild the season palette and swap in the Loewe donut."
  - "Does the red finding hold up against what the press said?"
- **You get:** season palette, per-house donuts, swatch grid, per-colour over-indexing deep dive.

### 2.8 `fashionunited-article` (trade article)

- **Attach:** the finished DFB piece the data comes from, and any editor feedback.
- **Prompts:**
  - "FashionUnited version of the maximalism piece, about 600 words, four image slots."
  - "The editor sent this feedback on the denim draft, revise it."
  - "Pitch for FashionUnited from the Paris colour index."
- **Rules it enforces:** news first, third person, DFB cited as a source, no other outlet names in the body, no exclamation points, licensed images only.

### 2.9 `dfb-personal-essay` (no-data pieces)

- **Attach:** your story notes. It will ask what the actual story is.
- **Prompts:**
  - "I want to write something more personal about what I learned this fashion week."
  - "An essay about my career, Zara to Net-a-Porter to now. Not analytical."

### 2.10 `dfb-media-kit` (15-day refresh)

- **Attach:** nothing for a normal refresh. New Substack stats = the Stats screenshot in Drive. New partnership = the row in your 260921_DFB_Growth sheet.
- **Connectors:** Instagram API token (`graph.instagram.com`), Google Drive, Canva. Not Metricool.
- **Prompts:**
  - "Refresh the media kit."
  - "Media kit: Substack is at 8.3k subscribers, update it."
  - "Add DeMellier as a partnership and rebuild."
  - "Typo check on the Canva media kit."
- **You get:** updated `media-kit/data.json` and `stats_history.csv`, the 2-page PDF in chat, Canva numbers updated in place, a short summary of what moved.
- **Deadline:** the Instagram token **expires around 26 November 2026**. Renew it in the app dashboard (Instagram → API setup with Instagram login → Generate token) and store it in the environment, never in chat.

### 2.11 `calendar-assistant`

- **Connectors:** Notion ("My Calendar"), Google Calendar.
- **Prompts:**
  - "FashionUnited wants the maximalism piece by Friday."
  - "Call with Patricia Tuesday at 3."
  - "What's due this week?"
  - "I sent the article" / "Move the denim deadline to the 12th."
- **You get:** one or two lines confirming the item, the exact date and the Notion link. DFB posts go to the Posting calendar, ideas to Idea cards, freelance deadlines to My Calendar.

### 2.12 `dfb-dataset` (research dataset, repo `dfb-data`)

- **Attach:** one house per message: the house name + its Vogue Runway screenshots.
- **Prompts:**
  - "Dior SS27." + screenshots
  - "Add Lanvin, Paris SS27, here are the looks."
  - "What share of Paris SS27 looks were black? With counts."
  - "Fix Chanel SS27: look 14 is tweed, not bouclé."
  - "Give me the Paris report."
- **You get:** the look log to check, `data/<season>/<city>/<house>.json`, rebuilt workbooks (`build/SS27/SS27-paris.xlsx`), palette slices, top materials and formulas, committed and pushed.
- **In the dataset now:** 16 Paris SS27 shows (1,037 looks with Prada SS21). Balmain, Dior and Dries Van Noten are tagged here even though their Instagram decodes are still pending in firstrepo.
- **Not this skill:** charts, captions, Canva. Those are `dfb-catwalk-decode` in firstrepo.

### 2.13 `dfb-invoice` (invoices PDF)

- **Attach:** nothing, just the job. First time only, Claude asks for your legal name, address, tax number and IBAN and saves them in `invoices/profile.json` (keep the repo private). Per client it needs their legal name, address, VAT ID if any, what the work was, the amount and whether VAT applies. You confirm the VAT treatment, Claude never decides it.
- **Prompts:**
  - "Invoice FashionUnited 600 euros for the maximalism piece."
  - "Invoice [brand]: 1 sponsored carousel at 850 and 2 story sets at 120 each, 30 days."
  - "Who hasn't paid me yet?" / "ASOS paid."
  - "Credit note for invoice DFB-2026-003."
- **You get:** a one-page PDF in `invoices/` (numbered `DFB-2026-001`, `-002`, ...), totals worked out by the script, a row in `invoices/log.csv`, and an offer to draft the email to the client in Gmail (a draft, never sent for you).

### 2.13 `dfb-carousel` (data carousel in Canva, repo `dfb-data`)

- **Attach:** a Google Trends CSV, company results, or dataset numbers. Cut-out images if you have them.
- **Connectors:** Canva.
- **Prompts:**
  - "Carousel on the ballet flat, here's the Trends export."
  - "DeMellier carousel: made in Spain, +65% revenue, searches 4x. Build it in Canva."
  - "5 slides, title asks the question, last slide answers it."
- **You get:** the slide plan for your OK, the Canva design (5 slides, 6 max), charts as PNGs with labels left as Canva elements, caption, and `carousels/<yyyy-mm>-<slug>/README.md`.

### 2.14 `dfb-personal-carousel` (Behind DFB carousel in Canva, repo `dfb-data`)

- **Attach:** your photos (HEIC is fine) and the story.
- **Connectors:** Canva.
- **Prompts:**
  - "Personal carousel: how I got into fashion data without a tech degree."
  - "Hi, I'm Carmen re-intro carousel for 30k, here are my photos."
- **You get:** 6 to 9 slides from the "Every decision in fashion is based on data" reference design, caption, README in `carousels/`.

---

## 3. Routines and dates

| When | What | Repo |
|---|---|---|
| Every Sunday | Weekly shifts pack | firstrepo |
| 1st and 15th | Media kit refresh | firstrepo |
| Around 26 Nov 2026 | Instagram API token expires. Renew a week before. | Instagram app dashboard |
| Every decode | Brand added to `season-log.md`, palette PNG exported | firstrepo |
| Every show tagged | `build/` rebuilt and pushed | dfb-data |

---

## 4. If a session can't find a skill

Paste this as your first message (change the skill name):

```
Read .claude/skills/dfb-reels/SKILL.md and follow it for this task.
```

If the skill folder isn't there at all, you started on an old branch. Say: "Fetch origin/main and check it out", then try again.

---

## 5. Still to decide

- **One repo for all skills?** `dfb-carousel` and `dfb-personal-carousel` sit in dfb-data because they use the dataset; every other publishing skill is in firstrepo. Moving them to firstrepo would mean one repo to remember for anything you publish.
- **Default branch of firstrepo.** It is still named `claude/busy-einstein-eini0p` on GitHub (it now has the same content as `main`). Switching the default to `main` is one setting: GitHub → firstrepo → Settings → Default branch.
