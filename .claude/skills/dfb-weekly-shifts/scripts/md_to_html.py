#!/usr/bin/env python3
"""Convert the weekly pack (.md with # / ## / **bold** / ---) to simple HTML for a Drive upload.

Usage: python3 md_to_html.py pack.md pack.html
Then upload pack.html with create_file (contentMimeType text/html, base64Content as a
sha256 file reference, no disableConversionToGoogleType). Drive turns it into a Google Doc
and keeps the bold.
"""
import html
import re
import sys


def inline(s):
    s = html.escape(s, quote=False)
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)


def convert(src):
    out = ['<html><head><meta charset="utf-8"></head><body style="font-family:Arial;font-size:11pt">']
    for line in src.split("\n"):
        if not line.strip():
            continue
        if line.startswith("# "):
            out.append(f"<h1>{inline(line[2:])}</h1>")
        elif line.startswith("## "):
            out.append(f"<h2>{inline(line[3:])}</h2>")
        elif line.strip() == "---":
            out.append("<hr>")
        else:
            out.append(f"<p>{inline(line)}</p>")
    out.append("</body></html>")
    return "\n".join(out)


if __name__ == "__main__":
    src_path, dst_path = sys.argv[1], sys.argv[2]
    with open(src_path, encoding="utf-8") as f:
        src = f.read()
    with open(dst_path, "w", encoding="utf-8") as f:
        f.write(convert(src))
    print("wrote", dst_path)
