# Canva look collage (article imagery)

The runway-look collage that runs inside a Runway Decode Trend Report:
six runway photos, each with a small pink pill label naming the trend
and the designer. Carmen sends the photos and says (or the photo shows)
which trend and house each one is, Claude fills a copy of the Canva
template with them.

This is visual work, so per CLAUDE.md's workflow it happens only after
the piece's text is approved, and the trend names on the labels should
match the wording the approved text and charts use.

## The template

- Canva design `DAHXacUhDOM`, title "PFW pics", one 800 x 1000 page.
- Edit link: https://www.canva.com/design/DAHXacUhDOM/Ow_jTTWRRftiu5iNYnHD-Q/edit
- **Never edit the template itself.** Always `copy-design` it first and
  work on the copy, renamed for the piece (e.g. "PFW SS27 looks").

Six image frames (add a second page with the same layout when there are
more than six looks) in two staggered rows, each with its own text label.
Slot numbers run in reading order, top row left to right, then bottom
row left to right. Element IDs below are from the template at the time
this was written, a copy can come back with different IDs, so always
re-read the copy with `read-design` and match frames to labels by
position (the label sits on or just inside its frame's corner), not by
these IDs.

| Slot | Position | Image frame | Label | Label text in the template |
|---|---|---|---|---|
| 1 | top left | `LBx3h3RWnc3JSYbS` | `LB3V16fRP4BqtX82` | Pencil skirt / Chanel |
| 2 | top middle | `LBbLBmqV7g7FmZLX` | `LB3RDRLK4x98GRXT` | Pencil skirt / Tom Ford |
| 3 | top right | `LBR5sh9nN086YwKk` | `LB1G6DdbBtjclfWk` | Wide leg trouser / Celine |
| 4 | bottom left | `LBtPSXPmp5VC076f` | `LB0PLf6C1NTDR5Km` | Single breasted blazer / Dior |
| 5 | bottom middle | `LBLdH2wH084VZTGm` | `LBYryJCmZCPjzm3n` | Tom Ford / Straight leg |
| 6 | bottom right | `LB24kCjbfhb84bJn` | `LB27gnG4PrZN67Hq` | Wide leg trouser / Stella McCartney |

The frames overlap on purpose (slot 2 sits over slots 1 and 3, slot 5
over 4 and 6), keep the layering as it is.

## Label format

- Two lines, **trend on line 1, designer on line 2**, separated by a
  newline: `Wide leg trouser\nCeline`. Slot 5 in the template has the
  order reversed ("Tom Ford / Straight leg"), that's a template slip,
  not a second style, write it the standard way and mention the fix.
- Trend in sentence case, using the same name the piece's text and
  charts use (usually the spreadsheet's Type value), e.g. "Wide leg
  trouser", not a new paraphrase.
- Designer as the house is normally written (Celine, Stella McCartney,
  Chanel), the same spelling as the rest of the piece.
- No em or en dashes in labels, same rule as everywhere else.
- Change only the characters. Keep the existing font, size, white
  colour, pink pill and centring. If a long name wraps badly, widen the
  label with `resize_element` (width only) rather than shrinking text.

## Who decides the trend and designer

- Carmen tells Claude, or the photo itself shows it in readable text (a
  show caption, a watermark, a filename like `chanel-ss27-look-12.jpg`).
- **Never identify the designer from the clothes alone.** Guessing a
  house from how a look appears is exactly the unverified claim
  CLAUDE.md rules out. If the photo carries no readable credit and
  Carmen didn't say, ask.
- Claude can suggest the trend from what's visibly in the photo (a wide
  leg trouser is a wide leg trouser), but say it's a suggestion and
  check it against the piece's taxonomy before writing it on the label.
- Before building, reply with the full slot plan (slot, photo, trend,
  designer) so she can correct it in one pass.

## Cropping the photos first

Carmen usually sends phone screenshots from a runway app, with the
status bar, the house and season header, the "LOOK n/N" bar and the top
of the next look still in them. Before uploading, run
`scripts/crop_runway_screenshots.py <in_dir> <out_dir>`, which keeps
only the runway photo. Then check a contact sheet by eye: **the whole
model has to be visible, head to toe**, nothing cut at the head or
the shoes. The house name in the header is the designer credit, so read
and note it before cropping it away.

The same rule holds inside Canva: when placing a photo in a frame, the
whole model stays in view, so crop the frame's image box to fit the
model's full height rather than letting Canva fill the frame and cut
off the feet.

## Getting the photos into Canva

- Photo sent in chat or sitting in the repo (a local file): call
  `create-upload-url`, then POST the raw bytes:
  `curl -sS -X POST -H "Content-Type: application/octet-stream" --data-binary @photo.jpg "<upload_url>"`.
  The response holds the asset ID. One URL per file, get a fresh URL for
  each photo and for any retry.
- Photo at a public HTTPS link: `upload-asset-from-url` instead.
- Name each asset `<house> <trend> <season>` so it's findable later in
  her Canva uploads.

## Build steps

1. `copy-design` the template, `update_title` on the copy to the piece's
   name.
2. `read-design` the copy with `open_transaction: true` and
   `thumbnails`, map frames to labels by position as above.
3. Per slot: `update_fill` on the frame with the uploaded asset
   (`asset_type: image`, alt text "<Designer> <season> runway look,
   <trend>"), then `replace_text` on its label.
4. Check the returned thumbnail. The default fill can cut off heads or
   shoes, and the whole model must be visible, so `crop_media` to
   reframe any photo where she isn't fully in view head to toe.
5. If Carmen sent fewer than six looks, ask whether to drop the empty
   frames (`delete_element` on frame and label) or keep the template
   photos there, never leave a template photo under a new label.
6. Show Carmen the preview thumbnail and get her OK **before**
   `finalize: commit`, a commit can't be undone. Then give her the
   copy's edit link.
7. Export only if she asks for a file (PNG for Substack is the usual
   ask), and add the collage's alt text to the closing deliverables list
   in SKILL.md.

## Learned on the Paris SS27 build

- **Network:** uploads POST to `www.canva.com`, which the cloud
  environment blocks by default. Carmen has allowed it in her
  environment's network settings. If a new environment gets a 403 on the
  upload, she needs to allow it again.
- **Photos sent while Claude is mid-reply** only arrive as pictures, not
  files, so they can't be uploaded. Ask her to resend them in a message
  of their own.
- **One page per trend group, one copy of the template per page.** Fill
  each copy, then join them with `merge-designs`. Canva accepts only one
  operation per merge call, so create the new design with page 1, then
  append each further page with its own `modify_existing_design` call.
- **Fewer than six looks on a page:** delete the spare frames and labels
  and make the rest bigger. Two looks go side by side and staggered.
  Three go in one staggered row. Four go in a staggered 2 x 2 grid of
  frames about 270 x 405. Move each label along with its frame.
- **Whole model in view:** the photos are about 0.666 wide to 1 tall,
  so set each frame to that shape (`resize_element`), then
  `crop_media` the image box to the full frame from 0,0.
- **Order:** Carmen wanted the fabric trends first (wool and silk, then
  chiffon, lace and sequins, then embroidery), followed by the garment
  trends.
- **Designer unknown:** if the screenshot is cut off above the house
  name, put only the trend on the label and ask. She confirmed each one
  (Lanvin, Loewe, Chloé) during the build.
