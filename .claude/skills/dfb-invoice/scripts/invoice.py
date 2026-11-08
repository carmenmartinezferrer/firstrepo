"""Build a DFB invoice PDF from a small JSON file.

    python .claude/skills/dfb-invoice/scripts/invoice.py invoices/draft.json
    python .claude/skills/dfb-invoice/scripts/invoice.py invoices/draft.json --number DFB-2026-007

Reads Carmen's own details from invoices/profile.json, the job from the JSON you pass in,
works out every total itself (Decimal, never typed by hand), numbers the invoice from
invoices/log.csv, writes invoices/<number>.pdf and appends a row to the log.
Needs: pip install playwright pymupdf   (Chromium path: CHROMIUM_PATH or /opt/pw-browsers/chromium)
"""
import argparse
import csv
import json
import os
import re
import sys
from datetime import date, datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP
from html import escape
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
FONTS = REPO / "media-kit" / "fonts"
INVOICES = REPO / "invoices"
SYMBOLS = {"EUR": "€", "GBP": "£", "USD": "$"}
PINK = "#D6447A"
DASHES = (chr(0x2014), chr(0x2013))  # em and en dash: never allowed in anything DFB sends out


def money(x):
    return Decimal(x).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def fmt(x, cur):
    sym = SYMBOLS.get(cur, cur + " ")
    return f"{sym}{x:,.2f}"


def long_date(d):
    return f"{d.day} {d.strftime('%B %Y')}"


def lines(text):
    return "".join(f"<div>{escape(l)}</div>" for l in (text or "").splitlines() if l.strip())


def check_no_dashes(*blobs):
    for b in blobs:
        if any(d in b for d in DASHES):
            sys.exit("An em or en dash is in the invoice text. Replace it with a comma, 'and' or a full stop.")


def next_number(log, year):
    nums = []
    if log.exists():
        with log.open(newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                m = re.fullmatch(rf"DFB-{year}-(\d+)", row["number"])
                if m:
                    nums.append(int(m.group(1)))
    return f"DFB-{year}-{(max(nums) + 1 if nums else 1):03d}"


def build_html(inv, prof):
    cur = inv["currency"]
    rows = "".join(
        f"<tr><td>{escape(i['description'])}</td><td class='n'>{i['qty']:g}</td>"
        f"<td class='n'>{fmt(i['unit'], cur)}</td><td class='n'>{fmt(i['amount'], cur)}</td></tr>"
        for i in inv["items"]
    )
    vat_row = (f"<tr><td>VAT ({inv['vat_rate']:g}%)</td><td class='n'>{fmt(inv['vat'], cur)}</td></tr>"
               if inv["vat_rate"] else "")
    po = f"<div><b>Your reference</b> {escape(inv['po_ref'])}</div>" if inv.get("po_ref") else ""
    vat_note = f"<p class='note'>{escape(inv['vat_note'])}</p>" if inv.get("vat_note") else ""
    notes = f"<p class='note'>{escape(inv['notes'])}</p>" if inv.get("notes") else ""
    c = inv["client"]
    pay = "".join(
        f"<div><b>{k}</b> {escape(prof[key])}</div>"
        for k, key in (("Account holder", "account_holder"), ("IBAN", "iban"), ("BIC", "bic"), ("Bank", "bank"))
        if prof.get(key)
    )
    tax = f"<div>{escape(prof['tax_id_label'])}: {escape(prof['tax_id'])}</div>" if prof.get("tax_id") else ""
    ctax = f"<div>VAT ID: {escape(c['vat_id'])}</div>" if c.get("vat_id") else ""
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>Invoice {inv['number']}</title>
<link href="{FONTS.as_uri()}/fonts.css" rel="stylesheet">
<style>
@page {{ size: A4; margin: 0 }}
* {{ box-sizing: border-box; margin: 0; padding: 0 }}
body {{ font-family: Jost, sans-serif; color: #24231f; font-size: 10pt; line-height: 1.5; padding: 22mm 20mm 18mm }}
.top {{ border-top: 3pt solid {PINK}; padding-top: 10mm; display: flex; justify-content: space-between }}
h1 {{ font-family: 'DM Serif Display', serif; font-weight: 400; font-size: 34pt; line-height: 1; color: #000 }}
.brand {{ font-family: 'DM Serif Display', serif; font-style: italic; font-size: 12pt; color: #52514e; margin-top: 4pt }}
.meta {{ text-align: right; font-size: 9.5pt }} .meta b {{ color: #898781; font-weight: 600; margin-right: 4pt }}
.parties {{ display: flex; gap: 20mm; margin-top: 14mm }} .parties > div {{ flex: 1 }}
h3 {{ font-size: 8pt; letter-spacing: .1em; text-transform: uppercase; color: #898781; font-weight: 700; margin-bottom: 3pt }}
.name {{ font-weight: 600; font-size: 11pt }}
table {{ width: 100%; border-collapse: collapse; margin-top: 14mm }}
th {{ font-size: 8pt; letter-spacing: .1em; text-transform: uppercase; color: #898781; text-align: left; font-weight: 700;
     padding: 0 0 4pt; border-bottom: .75pt solid #24231f }}
th.n, td.n {{ text-align: right }}
td {{ padding: 7pt 0; border-bottom: .5pt solid #dddcd8; vertical-align: top }}
td:first-child {{ width: 52% }}
.totals {{ margin-left: auto; width: 48%; margin-top: 6mm }} .totals table {{ margin-top: 0 }}
.totals td {{ border: 0; padding: 3pt 0 }}
.totals tr.grand td {{ border-top: .75pt solid #24231f; padding-top: 7pt; font-family: 'DM Serif Display', serif; font-size: 17pt; color: #000 }}
.totals tr.grand td:last-child {{ color: {PINK} }}
.pay {{ margin-top: 14mm; padding: 6mm; background: #f7f6f4; border-left: 2.5pt solid {PINK}; font-size: 9.5pt }}
.pay b {{ display: inline-block; width: 28mm; color: #52514e; font-weight: 600 }}
.note {{ margin-top: 6mm; font-size: 9pt; color: #52514e }}
.foot {{ position: fixed; bottom: 12mm; left: 20mm; right: 20mm; font-size: 8pt; color: #898781; display: flex; justify-content: space-between }}
</style></head><body>
<div class="top">
  <div><h1>Invoice</h1><div class="brand">The Data Fashion Brief</div></div>
  <div class="meta">
    <div><b>Invoice no.</b> {inv['number']}</div>
    <div><b>Issued</b> {long_date(inv['date'])}</div>
    <div><b>Due</b> {long_date(inv['due'])}</div>
    {po}
  </div>
</div>
<div class="parties">
  <div><h3>From</h3><div class="name">{escape(prof['name'])}</div>{lines(prof['address'])}{tax}<div>{escape(prof['email'])}</div></div>
  <div><h3>Billed to</h3><div class="name">{escape(c['name'])}</div>{lines(c.get('address'))}{ctax}{('<div>' + escape(c['email']) + '</div>') if c.get('email') else ''}</div>
</div>
<table><thead><tr><th>Description</th><th class="n">Qty</th><th class="n">Unit price</th><th class="n">Amount</th></tr></thead>
<tbody>{rows}</tbody></table>
<div class="totals"><table>
  <tr><td>Subtotal</td><td class="n">{fmt(inv['subtotal'], cur)}</td></tr>
  {vat_row}
  <tr class="grand"><td>Total due</td><td class="n">{fmt(inv['total'], cur)}</td></tr>
</table></div>
{vat_note}
<div class="pay"><h3>How to pay</h3>{pay}<div><b>Reference</b> {inv['number']}</div></div>
{notes}
<div class="foot"><span>The Data Fashion Brief · @thedatafashionbrief</span><span>{inv['number']}</span></div>
</body></html>"""


def html_to_pdf(html_path, pdf_path):
    from playwright.sync_api import sync_playwright
    exe = os.environ.get("CHROMIUM_PATH") or ("/opt/pw-browsers/chromium" if Path("/opt/pw-browsers/chromium").exists() else None)
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=exe, args=["--no-sandbox"]) if exe else p.chromium.launch()
        pg = b.new_page()
        pg.goto(html_path.as_uri())
        pg.evaluate("document.fonts.ready")
        pg.pdf(path=str(pdf_path), format="A4", print_background=True, prefer_css_page_size=True)
        b.close()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("job", help="JSON file describing this invoice (see SKILL.md)")
    ap.add_argument("--number", help="force an invoice number instead of the next free one")
    ap.add_argument("--profile", default=str(INVOICES / "profile.json"))
    ap.add_argument("--out-dir", default=str(INVOICES))
    ap.add_argument("--no-log", action="store_true", help="build the PDF without adding a row to log.csv")
    a = ap.parse_args()

    prof_path = Path(a.profile)
    if not prof_path.exists():
        sys.exit(f"No seller profile at {prof_path}. Copy invoices/profile.example.json to invoices/profile.json "
                 "and fill in Carmen's real details first. Never invent them.")
    prof = json.loads(prof_path.read_text(encoding="utf-8"))
    job = json.loads(Path(a.job).read_text(encoding="utf-8"))
    for k in ("name", "address", "email"):
        if not prof.get(k) or "TODO" in str(prof[k]):
            sys.exit(f"profile.json is missing a real '{k}'.")
    if not prof.get("iban") or "TODO" in prof["iban"]:
        sys.exit("profile.json has no real IBAN, so there is nowhere to pay. Ask Carmen for it.")

    issued = date.fromisoformat(job["date"]) if job.get("date") else date.today()
    due = date.fromisoformat(job["due_date"]) if job.get("due_date") else issued + timedelta(days=int(job.get("due_days", 30)))
    cur = job.get("currency") or prof.get("currency") or sys.exit("No currency given in the job or the profile.")
    vat_rate = Decimal(str(job.get("vat_rate", 0)))
    if not job.get("items"):
        sys.exit("The invoice has no line items.")

    items, subtotal = [], Decimal(0)
    for it in job["items"]:
        qty, unit = Decimal(str(it.get("quantity", 1))), money(it["unit_price"])
        amount = money(qty * unit)
        subtotal += amount
        items.append({"description": it["description"], "qty": float(qty), "unit": unit, "amount": amount})
    vat = money(subtotal * vat_rate / 100)
    inv = {
        "number": a.number or next_number(Path(a.out_dir) / "log.csv", issued.year), "date": issued, "due": due,
        "currency": cur, "client": job["client"], "items": items, "subtotal": subtotal,
        "vat_rate": float(vat_rate), "vat": vat, "total": subtotal + vat,
        "po_ref": job.get("po_ref", ""), "vat_note": job.get("vat_note", ""), "notes": job.get("notes", ""),
    }
    check_no_dashes(json.dumps(job, ensure_ascii=False), json.dumps(prof, ensure_ascii=False))

    out = Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    pdf = out / f"{inv['number']}.pdf"
    if pdf.exists() and not a.number:
        sys.exit(f"{pdf} already exists.")
    html = out / f".{inv['number']}.html"
    html.write_text(build_html(inv, prof), encoding="utf-8")
    try:
        html_to_pdf(html, pdf)
    finally:
        html.unlink(missing_ok=True)

    if not a.no_log:
        log = out / "log.csv"
        new = not log.exists()
        with log.open("a", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            if new:
                w.writerow(["number", "issued", "due", "client", "currency", "subtotal", "vat", "total", "status", "file"])
            w.writerow([inv["number"], issued, due, inv["client"]["name"], cur, subtotal, vat, inv["total"], "sent-pending", pdf.name])
    print(f"{inv['number']}  {fmt(inv['total'], cur)}  due {long_date(due)}  ->  {pdf}")


if __name__ == "__main__":
    main()
