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

### The wider press (every week, after the eight outlets)

The eight outlets miss things. Run a second sweep of the past 7 days across: Bloomberg, Reuters and the FT (all paywalled, so search for their figures as quoted by others), Jing Daily (China), FashionNetwork, the UK trade press (Drapers, Retail Gazette, TheIndustry.fashion), Glossy / Modern Retail, and the week's company results releases (search "<company> Q3 results" for whoever reported). One search per outlet is enough. Carmen asked for this after a week when the eight outlets missed the FT's €251bn luxury market-value figure and the Birkin resale premium shrinking.

Also use this sweep to **check earlier shifts**: if new data contradicts something a previous pack said (a premium that was "stable" is now falling), that correction is itself a shift candidate, and say so in the copy.

### Don't repeat last week

Find last week's doc in the Drive folder (section 4) and read it with `read_file_content`. Don't reuse a shift unless there is genuinely new data, and if there is, lead with what's new.

## 2. Pick the five shifts

Exactly **5**. The series name is **shifts**, never "signals".

**A shift is a change in behaviour, not a reading of one event.** Test every shift line: does it describe something now true of the industry or the customer that wasn't before? "The hire is the tell" fails. "A creative director no longer gets time to build" passes. "The Chinese shopper hasn't stopped buying, she has moved down the price ladder" passes. If the line only explains this week's news, it isn't the shift yet; keep asking what changed.

**Reference set (8 Nov 2026, as Carmen stated them after the carousel review).** Match this level:
- Kering: a creative director no longer gets time to build. Vaccarello had ten years, McGirr three, Piccioli under eighteen months. Kering gives a vision 18 months to sell, then buys back the one that did (Rose worked with Demna at Balenciaga 2015 to 2018).
- American brands: the Chinese shopper hasn't stopped buying, she has moved down the price ladder. The growth now goes to $200, not €2,000.
- Hand-drawn Christmas: the customer craves things that took effort to make. It's the same pull behind the 80s nostalgia and maximalism. Loewe got there first (three Ghibli capsules, 2021 to 2023).
- Closures: the middle has no cushion left. Depend on one distributor or on footfall and you're one partner away from closing.
- Spain: the brands grew up abroad, so the Spanish shopper is now the customer they can most afford to lose.

Each names who changed (a group, a shopper, a market), what they now do, and the number that proves it. Don't reuse these lines in later weeks unless the story genuinely moves on; use them as the bar.

A shift qualifies when it has all three:
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
- **Spell out why it's news.** Don't lean on context the reader may not have. Write "Hermès was the one luxury house still growing through the slowdown. Not anymore", not "Even Hermès is slowing". Carmen asked for exactly this fix.
- **Name the measure and its scope.** A market index is not a company's sales: Acotex's figure is "fashion retail sales in Spain, the whole market", not "Inditex in Spain" or Mango's Spain sales. Write "the Spanish market". A region is not a country: "Asia excluding Japan" stays "Asia excluding Japan". Say what the number measures the first time you use it, and carry the publisher's own explanation when it gives one (Acotex blamed September 2026 on warm weather delaying autumn buying, October on uncertainty and shoppers waiting for Black Friday).
- **Concrete, checkable claims only.** No abstract aphorisms like "control is getting more expensive than growth": Carmen rejected exactly that kind of line. Every reading points at something specific.
- **Hyphens with spaces** ( - ), never em dashes. No bullet points inside a shift. No URLs in the copy.
- **Banned phrases:** "in the fashion industry", "it's important to note", "moreover", "furthermore", "additionally", "this raises questions about", "in today's landscape", "game-changer", and any meta-reference to "this article" or "this newsletter".
- British or American spelling: follow her recent posts.

### 3.1 Substack: "This Week in Fashion Data"

```
This Week in Fashion Data #DD/MM

<One subtitle sentence naming all five shifts in plain words.>

01 <Headline = the verdict, max 10 words>
<90-120 words: what happened (the numbers), then "Why:" the mechanism in one or two sentences, then "The shift:" one sentence naming what changed and for whom, then the closing question.>

02 …
(through 05)
```

Each paragraph has four parts, in order: the facts, the **why** (one or two sentences starting "Why:" or "Why now:"), **"The shift:"** (one sentence, explicit, naming what changed and for whom), and the question. Carmen's readers said the old version gave the facts but not the why or the shift; the explicit "The shift:" sentence is the fix, and it is also what the carousel slide ends on. **90-120 words per shift.** Cut rather than pad. No "worth digging into" lines here: research ideas go in Behind the scenes.

End the Substack section with a `Tags` line: 6-8 Substack tags, comma-separated. Always include `Fashion`, `Luxury`, `Fashion Industry`, `Data`, `Retail`; then 2-3 tags for this week's biggest names or themes (a brand, a group, a market). Example: `Tags: Fashion, Luxury, Fashion Industry, Data, Retail, Kering, Dior, Inditex`.

The post title must survive an email subject line on a phone (about 45 characters), so keep the weekly title short and fixed, and put the week's hook in the subtitle (under 90 characters shows in the preview). Carmen's chosen pair, once she confirms it, goes here.

### 3.2 Instagram carousel: lead with the shift

A reader told Carmen the carousel was "talking about data points, not shifts". The Substack paragraphs explain each shift; the slides were listing numbers. The carousel carries the shifts, the Reel carries the numbers (3.3). They are not the same script.

```
Slide 1
I'm a fashion data analyst.
These are the 5 shifts I'm seeing in fashion right now.

Slide 2
1. <Headline = the verdict, max 8 words, no number>
<Body: number, mechanism, consequence, in that order, max three sentences.>
**<Shift line: the last sentence of the Substack paragraph, the "so what" before the question.>**
Chart: <2-3 numbers for native Canva bars or tiles, with source; mark the highlight>

… (slides 3-6 for shifts 2-5)

Slide 7
<A short close in her voice, e.g. "Which one are you seeing too?"> Full breakdown on my Substack - link in bio.

Caption
<2-4 short lines, first person, chatty, with one number and a soft pointer to the Substack. No hashtag block unless she asks for one.>
```

Rules:
1. **Headline = the verdict, not the count.** "Kering is rewinding, not resetting." "China isn't the problem, the price is." "Hand-drawn is now a claim you can get caught on." "The brands in the middle are one partner away from closing." "Spanish brands are winning everywhere except Spain." The number ("a third creative director in four weeks", "+35%") goes in the body or on the chart, never in the headline.
2. **Every slide ends on the shift line, in bold, introduced by "The shift:".** It is the "The shift:" sentence from the Substack paragraph, and it names a change in behaviour (section 2), never a reading of one event. "The shift: a creative director no longer gets time to build." "The shift: the Chinese shopper has moved down the price ladder." "The shift: the middle has no cushion left." "The shift: the Spanish shopper is now the customer Spanish brands can most afford to lose." It must work with the number covered up.
3. **Body = number + mechanism + consequence**, in that order, max three sentences. Cut any sentence that is none of the three.
4. **Never repeat the headline's idea as a number in the body.** That space is for the shift.
5. **List slides end on the pattern.** When a slide lists cases (closures, exits), the last bullet is "One pattern." plus the mechanism, not a fourth case. The weakest case moves to the Substack.
6. **Name the exception** when one case doesn't fit ("Loewe makes sense: three Ghibli capsules since 2021, it would have done this AI debate or not"). It makes the pattern credible.
7. **Chart line under every slide:** two or three numbers that can be drawn as native bars or tiles in Canva, each with its source, and the highlight marked. Only numbers that are in the Substack text or Behind the scenes.
8. **Like against like on every chart:** same region, same measure, same period. Ralph Lauren China +35% sits next to Louis Vuitton's Chinese clients down mid-teens (drawn at -15%, starred as "mid-teens"), not next to Gucci worldwide. Worldwide figures go in the body. **Never add an unconfirmed number to complete a chart**: a single-source figure stays off the chart even if it would make the bars line up.

**Check before handing over:** for each slide, cover the number. Can a reader still say what changed, for whom, and why it matters? If not, rewrite the headline or add the shift line.

### 3.3 Instagram Reel (about 45 seconds): keep the numbers

**The voice says the shift, the screen shows the number.** Each beat's voiceover is the shift line (the behaviour change), spoken plainly; the on-screen text carries that shift's number. **One spoken number in the whole Reel**, the hard stat, placed at the peak (the last beat before the close). Everything else is shown, not said. It does not reuse the carousel's slide copy.

Use the DFB Reels method from `.claude/skills/dfb-reels/references/formula.md`, section 3 (Master formula) and section 6 (three acts, rising attention peaks, every sentence has a job), adapted to a five-shift list:

- **Hook (0-3s):** "I'm a fashion data analyst, and these are the 5 shifts I'm seeing right now." Or a sharper tension-first line if the week has one. The on-screen hook text has to work with the sound off.
- **Five beats (about 7s each):** one spoken sentence or two per shift, the shift itself, with its number on screen. **Order them so the attention peaks climb**: the beat with the spoken hard stat goes last.
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
