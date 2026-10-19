---
name: dfb-weekly-shifts
description: Builds Carmen's weekly "5 shifts in fashion" pack for The Data Fashion Brief (DFB) from the past week's fashion-business newsletters (BoF, Vogue Business, WWD, Retail Dive, Puck's Line Sheet, Modem Online, Modaes, All Things Fashion Tech) plus her own recent Substack posts, and saves it to Google Drive. One Google Doc with three copy-paste pieces - a Substack section (5 shifts, briefly explained), an Instagram carousel ("I'm a fashion data analyst. These are the 5 shifts I'm seeing in fashion right now"), and a Reel script. Use it for the Sunday scheduled run and whenever she asks for the weekly shifts, weekly briefing, "this week in fashion data", the five shifts, the shifts carousel or the weekly reel, even if she doesn't name the skill.
---

# DFB Weekly Shifts

Carmen is a fashion data analyst. Every week she posts the same three things, built from the same five shifts:

1. **Substack**: "This Week in Fashion Data", with 5 shifts, each briefly explained.
2. **Instagram carousel**: "I'm a fashion data analyst. These are the 5 shifts I'm seeing in fashion right now." One shift per slide, one or two sentences.
3. **Instagram Reel**: a spoken version of the same 5 shifts.

She copies and pastes the output. She doesn't want to edit it, so all three pieces have to be finished and publishable as written: right length, right voice, no notes to self inside them, and no placeholders. Anything that is only for her (sources, caveats, what nearly made the list) goes in a separate section at the bottom of the doc.

## 1. Research the week (past 7 days)

### Gmail first (her inbox is the best source for these)

| What | Gmail query |
|---|---|
| Vogue Business | `from:vogue@mail.vogue.com newer_than:8d` |
| All Things Fashion Tech | `from:allthingsfashiontech@substack.com newer_than:8d` (skip the "Job Board" issues) |
| The Business of Fashion | `from:businessoffashion.com newer_than:8d` |
| **Carmen's own posts** | `from:thedatafashionbrief newer_than:15d` (her sections send from `thedatafashionbrief+trends@substack.com` and `thedatafashionbrief+behind-the-fashion-data@substack.com`) |

Search results only show previews, so open the relevant threads with `get_thread` (`PLAIN_TEXT`) before using them. If Gmail errors or asks to re-authenticate, carry on with web search for every source, and say so in the "Behind the scenes" section and in the final report. Never skip the disclosure.

### The web, for all eight outlets

Search each outlet's coverage from the past 7 days, even when Gmail worked for it: BoF, Vogue Business, WWD, Retail Dive (fashion only), Puck's Line Sheet (Lauren Sherman), Modem Online, Modaes, All Things Fashion Tech. Use WebSearch, because WebFetch is blocked for several of these domains (substack.com, fashionunited). If an outlet published nothing relevant that week, skip it. Don't force it.

### Don't repeat last week

Find last week's doc in the Drive folder (section 4) and read it with `read_file_content`. Don't reuse a shift unless there is genuinely new data, and if there is, lead with what's new.

## 2. Pick the five shifts

Exactly **5**. A shift qualifies when it has all three:
- **A pattern**: more than one source, company or data point points the same way. Name the category-level pattern, not just the company ("fast fashion is getting regulated", not "Shein's IPO").
- **A hard number or a named quote**: a percentage, a euro or dollar figure, a share, a date.
- **An angle**: a real reading of what it means, not a summary of the news.

**Recap her own posts.** Carmen's own data counts as a source. If she published a finding in the last two weeks (a colour index, a denim share, a trend count), one shift can come back to it (two at most), ideally tied to this week's news ("I tracked X on the runway, and this week Y happened"). Write those in first person ("my Paris colour index found…"). Use only the numbers that are in her post.

Order the five from sharpest to softest for the Substack version. The Reel reorders them (section 3.3).

**Never invent or round a number.** DFB's credibility is the whole brand. If a shift needs a number you can't verify, drop the shift and pick another.

## 3. Write the three pieces

### Voice (all three pieces)

- **Thesis first.** The opening line is the claim, and the number comes in the first or second sentence.
- **Direct, no hedging.** Say what it means.
- **End on a question or a provocation** (Substack shifts and the Reel close).
- **Concrete, checkable claims only.** No abstract aphorisms like "control is getting more expensive than growth": Carmen rejected exactly that kind of line. Every reading points at something specific.
- **Hyphens with spaces** ( - ), never em dashes. No bullet points inside a shift. No URLs in the copy.
- **Banned phrases:** "in the fashion industry", "it's important to note", "moreover", "furthermore", "additionally", "this raises questions about", "in today's landscape", "game-changer", and any meta-reference to "this article" or "this newsletter".
- British or American spelling: follow her recent posts.

### 3.1 Substack: "This Week in Fashion Data"

```
This Week in Fashion Data #DD/MM

<One subtitle sentence naming all five shifts in plain words.>

01 <Shift headline, max 10 words>
<60-90 words: thesis, number, reading, closing question.>

02 …
(through 05)
```

Briefly explained means **60-90 words per shift**. Cut rather than pad. No "worth digging into" lines here: research ideas go in Behind the scenes.

### 3.2 Instagram carousel

```
Slide 1
I'm a fashion data analyst.
These are the 5 shifts I'm seeing in fashion right now.

Slide 2
1. <Headline, max 8 words>
<1-2 sentences, max 30 words, led by one number (two at most).>

… (slides 3-6 for shifts 2-5)

Slide 7
<A short close in her voice, e.g. "Which one are you seeing too?"> Full breakdown on my Substack - link in bio.

Caption
<2-4 short lines, first person, chatty, with one number and a soft pointer to the Substack. No hashtag block unless she asks for one.>
```

Each slide has to stand on its own when read in two seconds. Lead with the number when the number is the story.

### 3.3 Instagram Reel (about 45 seconds)

Use the DFB Reels method from `.claude/skills/dfb-reels/references/formula.md`, section 3 (Master formula) and section 6 (three acts, rising attention peaks, every sentence has a job), adapted to a five-shift list:

- **Hook (0-3s):** "I'm a fashion data analyst, and these are the 5 shifts I'm seeing right now." Or a sharper tension-first line if the week has one. The on-screen hook text has to work with the sound off.
- **Five beats (about 7s each):** one spoken sentence or two per shift, each with its number. **Order them so the attention peaks climb**: put the most surprising number last, not first.
- **Close (last 3-5s):** one quotable line plus "follow for the data behind the drama" or a question to drive comments.
- 110-130 spoken words in total. Short sentences. No greeting.

Format it as a table: `Time | Voiceover | On-screen text`. Then the full read-through script and a 2-3 line caption.

### 3.4 Behind the scenes (for Carmen only, last section of the doc)

- **Sources per shift:** outlet plus headline or newsletter subject (no URLs needed).
- **Sources this week:** which of the eight outlets had usable material, whether Gmail was accessible, and which of her own posts were recapped.
- **Worth digging into:** one line per shift, a research or long-form angle she could take further (Substack deep dive or FashionUnited piece).
- **Nearly made it:** 2-3 stories that didn't qualify, one line each.

## 4. Save to Google Drive

- **Folder:** "DFB / Weekly Briefings", folder ID `1OmNOBqzof3F_lMj-os1yI8UD2eIeD4xv`. If that ID fails, search Drive for `title = 'Weekly Briefings' and mimeType = 'application/vnd.google-apps.folder'`.
- **Title:** `DFB Weekly Shifts — Week of <DD Month YYYY>`, using the run's date (the Sunday).
- **Body:** plain text, in this order, with each heading on its own line: `SUBSTACK`, `CAROUSEL`, `REEL`, `BEHIND THE SCENES`.
- **Call:** `create_file` with `parentId` = the folder, `contentMimeType: "text/plain"`, `textContent`, and **no** `disableConversionToGoogleType`. Drive converts plain text into a native Google Doc. Don't pass `application/vnd.google-apps.document` as the content type together with content: Drive rejects that ("requires an external mime type").
- If that call errors, retry **once** with `disableConversionToGoogleType: true` (this saves a .txt file) and say it's a .txt fallback in the report.
- Before saving, write the full text to a scratch file, so nothing is lost if the Drive call fails.

## 5. Report

End with 3-4 lines:
- The doc link.
- The five shift headlines.
- Which outlets had usable content, and whether Gmail was accessible.
- Anything Carmen should check before posting (e.g. a number from a single source).
