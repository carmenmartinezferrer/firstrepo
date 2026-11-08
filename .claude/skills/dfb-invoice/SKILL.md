---
name: dfb-invoice
description: Creates a ready-to-send invoice PDF for Carmen (The Data Fashion Brief, DFB) for brand partnerships, sponsored posts, FashionUnited commissions, consulting or any other paid work. It numbers the invoice, works out subtotal, VAT and total itself, applies DFB's look, saves the PDF to invoices/ and logs it. Use this whenever Carmen asks for an invoice, a bill, "invoice X for the carousel", "bill FashionUnited", "send them an invoice for 800", a credit note or corrected invoice, or asks what she has invoiced so far, even if she doesn't say "skill".
---

# DFB Invoice

Makes a one-page A4 invoice PDF in DFB's look (pink top rule, DM Serif Display title, Jost body) from a few details,
and keeps a running log. Everything lives in `invoices/` in this repo; the builder is
`.claude/skills/dfb-invoice/scripts/invoice.py`.

## Non-negotiables

- **Never invent money or identity details.** Amounts, VAT rate, client legal name and address, Carmen's tax number
  and IBAN all come from Carmen or from files she gave you. If one is missing, ask. A wrong IBAN or VAT line on an
  invoice is worse than a delay.
- **Never decide the VAT treatment yourself.** Whether VAT is charged, 0 or reverse-charge depends on where Carmen
  and the client are based, and she has to confirm it. Ask once per client, then remember it in `invoices/clients.json`.
  If it is a reverse-charge or exempt case, put her exact wording in `vat_note`.
- **No em dashes or en dashes** anywhere on the invoice (the script refuses to build if one is present), and no decimal
  percentages in the copy. Money keeps its two decimals, that is a price and not a percentage.
- **Only the amounts Carmen states.** Totals are computed by the script from quantity and unit price, never typed by hand.
- **Bank details and invoices never go into git.** This repo is public. `profile.json`, `clients.json`, `log.csv` and every
  invoice PDF are in `.gitignore`: never `git add -f` them, never paste an IBAN into a commit, a PR or a GitHub comment.
  Hand the PDF over in chat. Only the script, the skill, the templates and `example-job.json` are committed.
- **Drafts only leave the repo when she says so.** Building the PDF is safe. Emailing it to a client is a separate step
  she has to ask for, and then it goes as a Gmail draft for her to read, never sent directly.

## Files

| File | What it is |
|---|---|
| `invoices/profile.json` | Carmen's own details: name, address, tax ID, account holder, IBAN, BIC, bank, bank address, default currency, `number_style` (`year-month` gives 2026-11, her own scheme) and optional default `style`. **Built from her answers or from an invoice she uploaded**, template in `profile.example.json`. |
| `invoices/clients.json` | Optional memory of each client's legal name, address, VAT ID, email, usual VAT treatment and payment terms, so she doesn't repeat them. |
| `invoices/log.csv` | One row per invoice: number, dates, client, currency, subtotal, VAT, total, status, file. Statuses: `sent-pending`, `paid`, `overdue`, `cancelled`. |
| `invoices/<number>.pdf` | The invoices. Numbers run on from the log, never reuse or skip one. Default `DFB-2026-001`, or `2026-11` with `year-month`. |
| `invoices/example-job.json` | The job format, copy it. |

## Workflow

1. **First ever use:** `invoices/profile.json` doesn't exist. Ask Carmen for her legal name, address, email, tax number
   (and its label, e.g. NIF), account holder, IBAN, BIC, bank and usual currency, or read them off an earlier invoice she
   uploads, and write the file. It is git-ignored, so in a fresh cloud session it won't be there: ask for an earlier
   invoice or the details again. The script stops with a clear message if the IBAN is still a TODO.
2. **Collect the job.** Needed: client (legal name, address, VAT ID if they have one, billing email), what the work was
   (one line per deliverable, in plain words the client will recognise, e.g. "Sponsored Instagram carousel, runway
   colour combos"), quantity and unit price per line, currency, VAT treatment, payment terms (default 30 days), and
   their PO or reference if any. Anything that's in `clients.json` or earlier in the chat you don't need to ask again.
   Missing ones: ask in one short message, not one question at a time.
3. **Write the job JSON** (copy `invoices/example-job.json`, save as e.g. `invoices/draft.json`, delete it after).
4. **Build:** `python .claude/skills/dfb-invoice/scripts/invoice.py invoices/draft.json`
   (needs `pip install playwright pymupdf`, Chromium is at `/opt/pw-browsers/chromium`, the script finds it).
   `--number DFB-2026-007` to force a number, `--no-log` for a throwaway test.
5. **Look at the PDF** (`pymupdf`, 80 dpi): one page, client block and totals correct, nothing cut off.
   Re-read the total against the amounts she gave you.
6. **Hand it over:** the PDF, then a two-line summary (number, client, total, due date). Ask whether she wants a Gmail
   draft to the client with it attached. Don't offer anything else.
7. **Do not commit the invoice, log or profile** (public repo, see above). Send the PDF to her with SendUserFile.

## Other things she may ask

- **"What have I invoiced?" / "who hasn't paid?"** Read `invoices/log.csv`, list by status, flag any `sent-pending` past
  its due date as overdue and say how many days. Totals per currency, never mixed.
- **"X paid"** Change that row's status to `paid`. Never edit amounts in the log.
- **Correction or credit note:** don't edit an issued invoice. Build a new one with a negative quantity or unit price,
  `notes` saying which invoice number it corrects, and mark the original `cancelled` only if she says so.
- **Deadlines:** if she mentions a payment due date she wants tracked, hand it to the `calendar-assistant` skill.

## Job JSON fields

`client` (name, address with `\n` line breaks, vat_id, email), `date` (ISO, default today), `due_days` (default 30) or
`due_date`, `currency` (EUR, GBP, USD or any code), `po_ref`, `vat_rate` (whole number, 0 for none), `vat_note`, `notes`,
`items` (list of `description`, `quantity`, `unit_price`), `style` (`dfb` is the designed look, `plain` is her plain
layout that FashionUnited already gets, `--style` on the command line overrides it).

## FashionUnited

Standing details are in `invoices/clients.json`: Hoogoorddreef 56, 1101 BE Amsterdam, euros, 180 per article, `plain` style,
no VAT. One line per article: `Article for FashionUnited: "<exact published title>", published on <date>`. The title and
publication date come from Carmen or the published page, never guessed. Her old invoices used a dash before "published", use a comma.
