---
name: runway-colour-combos
description: Build Runway Colour Combos, DFB's Instagram carousel series that breaks single runway looks into their two or three most striking colours. From Vogue Runway app screenshots Carmen sends, it cuts the model out (transparent PNG), samples each garment's hex code from the photo, renders Pantone-style swatch cards in Century Gothic, fills the Canva carousel (cover, one slide per colour combination, a closing Google search slide with a this year vs last year bar chart), and gives feedback on the deck. Use this whenever Carmen sends runway screenshots and asks for "the colour combination", "the palette", "remove the background", "just the model", swatches or hex codes, mentions Runway Colour Combos, or shares a Canva carousel link plus a Google Trends CSV for a colour, even if she doesn't name the series. Not for the full Runway Decode Colour Index built from tagged data (that's `runway-decode-colour`).
---

# Runway Colour Combos

An Instagram series, free reach, not a Substack piece. One carousel per colour story (e.g. purple), built from single looks. The format Carmen settled on reads like an equation: **colour chip + colour chip = the look**, e.g. "Rust + Lemon Yellow = Moschino SS27", with "Would you wear it?" in the caption, not on the image.

The CLAUDE.md non-negotiables still apply to every word on a slide: no em or en dashes (write "Oct to Dec 2025"), whole-number percentages, no unsourced claims, and the source list at the end of every handover.

## 1. Pick the colours (per look)

- Two colours by default, the two biggest, most contrasting garment blocks. Add a third only when it's clearly there (a third garment block, or an accessory that carries the look like Moschino's yellow bag or Bottega's red clutch). Never four, the equation stops reading on a phone.
- Prints have no single colour. Name the print's dominant tone ("Leopard Gold", the light ground of the print) and say so.
- Monochrome looks (Saint Laurent all gold) aren't a combination. Offer "Gold + Gold" or a tonal framing instead of inventing contrast.
- Name colours descriptively (Rust, Butter Yellow, Oxblood). Never present them as Pantone names or Pantone codes.
- If a screenshot has no Vogue Runway header (already cut out, cropped), ask for designer and look number. Label it "Brand TBC" until she answers, never guess the house.

## 2. Cut out the model

`scripts/cutout.py <out_dir> <model> <screenshots...>` crops the app chrome automatically, removes the background, keeps the largest shape and writes a magenta contact sheet `check.jpg`. **Always look at check.jpg before using anything.**

Model choice, learned the hard way:
- `isnet-general-use` first. It keeps bags, totes and props.
- Switch to `u2net_human_seg` when other models or audience sit right behind (Dries, Loewe), or a pale garment blends into a pale floor (it lost Balenciaga's white trousers with isnet).
- When human_seg drops an accessory (Balenciaga 53's tote), go back to isnet for that look and clean the background bits by colour.

Fixes that recur, all done on the crop-space `<name>_full.png`:
- **Person behind the model**: polygon cut on a gridded zoom (draw 50px gridlines with coordinates, read the boundary off the picture), then remove leftover slivers by colour (dark top, beige trousers) inside a narrow strip only.
- **Accessory overlapping a background person** (Loewe 22 bag over the man's legs): hand-draw a polygon round the accessory, union both models' masks inside it, remove the other person's colours outside it, fill holes only inside the accessory polygon. Filling holes everywhere refills the background you just removed.
- **Glossy runway reflection** (Cavalli): cut every row below the shoe soles.
- **Black background halo round hair**: drop near-black pixels in a 5px edge band, hair region only. Applied to the whole body it eats leopard spots and tassels.
- **Coloured set pieces** (Balenciaga coral sculpture): remove saturated sculpture hues only in zones beside the body, never globally, a global orange filter ate the yellow blazer's shadows.
- **Floor colour cast on fabric** (Valentino trousers lit pink by a red carpet) is real, leave it. Only remove the floor itself.
- Check every fix at post size on a light background, and zoom where you cut. A "fix" that makes things worse happens often enough to always re-check.

## 3. Sample the hex codes

`scripts/sample_colour.py <name>_full.png x0,y0,x1,y1 hue sat val` gives the median of matching pixels in a box. `... patch x,y` reads one spot with its HSV so you can set the filter.

- Hue filter per garment, and keep skin out of the box or the filter. If fewer than a few hundred pixels match, the box or filter is wrong.
- Uploads are sRGB (checked), so the hex is what the photo holds. Runway lighting often makes it darker or duller than it looks on Carmen's phone (Valentino purple, Bottega violet, Jil Sander pastels). Keep the measured value and say so, offering the lit-side value as an alternative. Don't silently brighten.
- Shiny fabric (gold foil, satin) reflects the room: sample the mid-tone, not highlights.

## 4. Render the swatch cards

Write a `looks.json`, then `scripts/build_swatches.py looks.json <html_dir>` and `node scripts/render_swatches.js <html_dir> <png_dir>` (Playwright, `NODE_PATH=$(npm root -g)`). Card layout matches the Paris SS27 Pantone cards: chip on top, house tag, colour name, hex, look number. Every line in Century Gothic; in the cloud container it isn't installed, so Questrial renders as the stand-in, say so.

Outputs go in `drafts/colour-combinations-<season>/models/` and `/swatches/`, numbered in the order she sent the looks, committed and pushed each batch.

## 5. Fill the Canva carousel

Carmen's deck (1080 x 1350, portrait) is: cover with the colour story and a few cutouts; one slide per combination titled "Purple + Red" style, cutouts left, swatch cards right, "Colour analysis" top right; a closing data slide. Read it with `read-design` (thumbnails for every page), edit inside one transaction, **show the preview and get her OK before `commit`**.

Closing search slide:
- `scripts/search_change.py <trends.csv>` gives the period averages. A 12-month Google Trends export holds only about 13 weeks of the earlier year, so label bars with the real periods ("Oct to Dec 2025" vs "Jan to Oct 2026") and use the % the data gives. When Carmen quotes a different figure (she said 20%, the file gave 23%), use the data's number and tell her why.
- The Canva chart element can't be edited through the API. Delete it and draw two rectangles to scale (taller bar = higher average), lighter tint for the earlier period, the slide's accent colour for the current one, value above each bar, period label below, a big "+N%" beside, and a small unit/source line: "Average weekly Google search interest for \"term\", worldwide, on Google's 0 to 100 scale. Source: Google Trends, <dates>."
- Added text comes in Canva's default font; the API can't set fonts, so flag it for her to switch to the deck font.
- Title and body come from real, linkable press (e.g. Refinery29 counting purple in "well over 20" NYFW SS27 collections). Pair the press claim with the search number, and if season-wide data disagrees (Tfashion ranks black and white first), keep the press line honest ("having a moment", not "the colour of the season" as fact).
- Flag when the search term is generic ("purple" is also Prince, mattresses, sports teams): spikes may not be fashion. Suggest "purple dress" or a Shopping filter next time.

## 6. Feedback on the deck

Check every slide for: titles matching the colours actually shown, swatch labels hidden under cutouts, inconsistent elements across slides (a missing "Colour analysis" tag), text too small to read on a phone, empty space on the cover, cards or hex codes that don't match the looks shown, a caption CTA, and an unsourced claim on the cover. Give feedback as a short list, slide by slide, with the fix.

## 7. Handover

Table of looks and hex codes, what needed hand cleanup and why, anything to confirm (brand TBC, colour choices, brighter alternatives), the usual standing notes (hex from photo not Pantone, Questrial stand-in, images need a licence before posting: Launchmetrics or brand press offices), then the source list with links, her screenshots marked "your uploads, no public link".
