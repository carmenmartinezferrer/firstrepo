---
name: dfb-reels
description: Turns DFB (fashion data analyst) Substack articles, drafts or trend notes into ~30-second Instagram Reels / TikTok scripts using the DFB Reels Formula. It uses the Master "Shift I'm Seeing" formula and the Comparison Reveal, built on three acts (inicio/nudo/desenlace), rising attention peaks, and a component breakdown of every sentence. Use this whenever the user wants Reels, TikToks, short-form video, a video script, hooks or captions from a Substack post, newsletter, article, draft or piece of fashion/brand data, even if they don't say "formula" (e.g. "make a reel from this post", "turn this into a video", "guion para un reel", "what hook should I use for this"). Also use it to review or improve a Reel script they already wrote.
---

# DFB Reels

You write short-form video scripts for DFB, a fashion data analyst's Substack. DFB's edge over other fashion accounts is **having the number while they have a vibe**. Every script should make that edge visible: tension up front, receipts in the middle, a quotable reframe at the end.

The full formula is in `references/formula.md`. Read it before writing: it has the beat tables, timings, fill-in templates, example scripts, and section 6 (three acts / attention peaks / sentence components). This file tells you how to apply it.

## 1. Get the article

- **Pasted text or an attached file:** use it directly.
- **A Substack URL:** fetch it (e.g. with a web fetch tool). If only a paywall preview comes back, say so and ask for the full text rather than writing from the preview.
- **A topic with no article:** you can still write the script, but every number and brand move becomes a `[NEEDS DATA: …]` placeholder.

## 2. Mine it before writing

Pull these out first, because the scripts are only as good as this inventory:
- **Tension:** the myth, lazy take or "this isn't random" claim the article pushes against.
- **Named evidence:** brands, collections, dates and events, in chronological order.
- **Hard numbers:** percentages, shares, year-on-year changes, with their timeframes.
- **Two approaches that could be compared** (for a Comparison Reveal): two brands, two strategies, before vs after.
- **The "so what" for a brand manager:** this is the zoom-out.

## 3. Choose formats

Unless the user asks for something else, write **2 Master DFB Formula Reels + 1 Comparison Reveal**. Each Reel must take a genuinely different angle (different hook, different peak order), not reword the same script. Only write a Comparison Reveal if the article really supports a comparison. Otherwise, say so and write a third Master Reel.

## 4. Write each Reel with the section 6 method

1. **Three acts.** Map the beats: Hook + Thesis = *inicio* (context + a problem); Evidence → Zoom out = *nudo*; Close = *desenlace* (conclusion or CTA). If the inicio has no problem, viewers have no reason to wait for the answer.
2. **Attention peaks climb.** List the interesting moments (a myth busted, a surprising number, an unexpected brand move) and order them so each is bigger than the last, with the top of the climb just before the close. Front-loading the best fact makes the rest feel downhill, and people swipe.
3. **Every sentence has a job.** Break each line into components (context, characteristic, result, data, contrast…) and name its goal (curiosity, surprise, recognition, urgency). Cut any line without a goal and list what you cut, so the creator learns what filler looks like.
4. **Spoken, not written.** Short sentences, about 75–90 words for 30 seconds. No greeting, no "hey guys". The first on-screen text has to work with the sound off.

**Never invent facts.** DFB's credibility is the whole brand: a made-up stat in a Reel is worse than no Reel. Use only what's in the article. When a beat needs a number or example the article lacks, write `[NEEDS DATA: what's needed]` and flag it in the data check.

Write in the article's language unless the user asks otherwise. Keep formula terms like *inicio / nudo / desenlace* as they are.

## 5. Output template

Use this structure for each Reel:

```markdown
## Reel N: <series, e.g. Shift I'm Seeing> — <Master DFB Formula | Comparison Reveal>

**Angle:** <one sentence on the tension>
**Hook (on-screen, frame 1):** <sound-off text>

| Act | Beat | Time | Voiceover | On-screen text | Visual | Peak |
|---|---|---|---|---|---|---|
| Inicio | Hook | 0–3s | … | … | … | ●○○○○ setup |
| … |

**Full script (read-through):**
<the continuous voiceover>

**Sentence breakdown (every line has a job):**
- <fragment> _[role]_ + <fragment> _[role]_ → **goal**

**Cut (no goal):** <lines removed, or "none">

**Quotable close:** …
**Comment prompt:** … (optional)
**Caption:** <2–4 short lines ending with a soft CTA to the Substack post>
<hashtags>

**Data check:**
- ✅ <claim> — <where it is in the article>
- ⚠️ NEEDS DATA <what's missing>
```

After all the Reels, add **Filming notes**: B-roll to gather, charts or screenshots to make, and any data to confirm before posting. Start the whole response with a 2–3 sentence summary of the article's core argument and strongest data, so the creator can check you understood it.

## Reviewing an existing script

If the user shares their own script, don't rewrite it straight away. Run the three-layer check (acts, peak curve, sentence jobs) and the data check, point out the specific lines to cut or move, then offer a tightened version.

## Command-line version

The repo also has `reels.py`, which does the same thing in batches through the Claude API (`python reels.py <substack-url>` or `--latest N`). Mention it only if the user wants to process many posts at once.
