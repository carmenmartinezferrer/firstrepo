---
name: dfb-personal-essay
description: >
  Write a personal essay or reflection piece for The Data Fashion Brief,
  career stories, learnings from a fashion week, a personal take on the
  industry, not a data-driven trend report or colour index. Use this
  whenever Carmen wants to write about her own career (Zara/Inditex,
  YOOX Net-A-Porter, Farfetch), a reflection on something she noticed or
  learned at a fashion week or in the industry, or any piece explicitly
  NOT meant to be backed by tagged data or charts, even if she just says
  "I want to write something more personal," "a learnings piece," "an
  essay about my career," or "not that analytical." If she brings a
  spreadsheet, a CSV, or asks for a trend report or colour breakdown,
  that's `runway-decode-trends` or `runway-decode-colour` instead, not
  this skill.
---

# DFB Personal Essay

Writes the non-analytical half of DFB's output, no tagging, no charts,
no methodology section. Read the repo root `CLAUDE.md` first, every
non-negotiable and voice note there still applies here, especially the
ones about not fabricating facts and not writing short punchy fragment
sentences. This skill only adds what's different about this format:
less chart-dense, more narrative, personal opinion isn't just welcome,
it's the whole point.

## How this is different from Runway Decode

`runway-decode-trends` and `runway-decode-colour` exist to prove a
reading of real data against the reader's assumptions. This skill exists
to do the opposite job: tell a true story about Carmen's own experience,
career, or a moment she noticed, with no spreadsheet behind it and no
obligation to back every line with a sourced number. The non-negotiables
about fabricated statistics and unverified claims still apply to
anything stated as fact (a real company she worked at, a real event, a
real figure she names), but the piece as a whole doesn't need a
methodology section, a tagging taxonomy, or a chart to be legitimate.
Don't force data into this format just because it's available, and
don't force this format's looseness into a Runway Decode piece. They're
different jobs.

## Voice, in practice

CLAUDE.md's voice notes apply at full strength here, more than in the
chart-heavy pieces, since there's no data to counterbalance the loose,
funny, personal register against. Exclamation points, personal shopping
confessions, self-aware asides, humour, all of it, unhedged.

`reference-articles/external-trend-autopsy-format-example.md` is the
primary structure and voice reference for this skill, it's the closest
existing reference to a personal, narrative register, read it before
drafting. `reference-articles/nyfw-ss27-trend-report-final.md` is a
secondary voice-only reference, useful for tics like the "Ok, ok…"
pivot and ending on a direct question to the reader, but don't borrow
its data-report structure for this format.

## Before you start

- **Ask what the actual story is**, not just the topic. "A piece about
  my career" or "learnings from fashion week" is a topic, not a story.
  Push for the specific moment, decision, mistake, or realisation the
  piece is actually built around, the same way a Trend Autopsy needs a
  real "Scene of the Crime," a personal essay needs a real scene too,
  even though nothing here gets tagged or charted.
- **Confirm which facts need to stay factual.** A personal essay still
  can't invent a company she didn't work at, a number she didn't earn,
  or a quote nobody said. If a detail is a half-remembered impression
  rather than a hard fact, say so in the piece rather than stating it as
  certain, the same honesty standard as everywhere else in CLAUDE.md,
  just applied to a memory instead of a dataset.
- **Don't default to the Trend Autopsy's Exhibit A section** (shoppable
  picks). This format doesn't need one unless Carmen specifically wants
  product recommendations attached to the story.

## Structure

There's no fixed template the way Runway Decode has one, a personal
essay's shape follows its story, not a chart sequence. A loose shape
that tends to work, borrowed from the external reference's own pacing:

1. **A real scene or moment**, specific enough that the reader can
   picture it, not an abstract topic sentence ("I've been thinking about
   my career lately" is weaker than naming the actual meeting, show, or
   moment that's actually prompting the piece).
2. **The reflection itself**, what she noticed, learned, got wrong,
   changed her mind about. This is where personal opinion carries the
   piece, not data.
3. **What it means beyond the one moment**, the same "zoom out" instinct
   as the data pieces, but reasoned from experience and judgement rather
   than a chart.
4. **A close that lands on a line worth quoting**, and, per CLAUDE.md's
   established pattern, often a direct question to the reader before the
   standard sign-off block.

## What stays the same as every other DFB piece

UK punctuation, no em or en dashes, no decimal percentages if a number
does appear, no AI-coded mirrored-parallel sentence constructions, and
Claude's role stays formatting and structure only, never silently
rewriting Carmen's actual argument or memory of what happened.
