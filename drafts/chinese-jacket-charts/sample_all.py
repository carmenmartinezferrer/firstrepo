"""Samples every swatch with the runway-colour-combos skill script
(median of hue-filtered pixels, mid-tones, nothing brightened)."""
import subprocess, json, os
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
SK = os.path.join(HERE, "..", "..", ".claude", "skills", "runway-colour-combos", "scripts", "sample_colour.py")
WHITE = ("0,360", "0,0.14", "0.6,1"); DARK = ("0,360", "0,1", "0,0.25")
# slug, house, look, [(name, photo, frac box, hue, sat, val)]
L = [
 ("01-conner-ives-ivory-coat", "CONNER IVES", "Ivory embroidered coat", [
   ("Ivory", "conner-ives-1", (.72,.62,.9,.75), *WHITE),
   ("Blossom Pink", "conner-ives-1", (.1,.55,.95,1), "-30,10", "0.25,1", "0.6,1"),
   ("Fox Fur", "conner-ives-1", (.38,.4,.62,.6), "20,50", "0.1,0.5", "0.5,1")]),
 ("02-conner-ives-gold-coat", "CONNER IVES", "Gold crane coat", [
   ("Gold", "conner-ives-4", (.2,.2,.85,.95), "38,65", "0.18,0.7", "0.6,1"),
   ("Coral", "conner-ives-4", (.28,.3,.6,.68), "-20,20", "0.3,1", "0.55,1")]),
 ("03-conner-ives-camel-coat", "CONNER IVES", "Camel coat with yellow embroidery", [
   ("Camel", "conner-ives-3", (.72,.42,.78,.85), "0,360", "0,0.4", "0.5,1"),
   ("Butter Yellow", "conner-ives-3", (.24,.27,.4,.42), "35,60", "0.3,1", "0.6,1")]),
 ("04-conner-ives-beige-coat", "CONNER IVES", "Beige coat with white fox", [
   ("Dark Beige", "conner-ives-5", (.44,.72,.58,.92), "25,60", "0.08,0.5", "0.6,1"),
   ("Blue Grey", "conner-ives-5", (.56,.25,.74,.65), "180,250", "0.08,1", "0.5,0.98")]),
 ("05-the-garment", "THE GARMENT SS27", "Mandarin collar jacket", [("Off-White", "the-garment", (.44,.26,.6,.44), *WHITE)]),
 ("06-christian-cowan", "CHRISTIAN COWAN SS27", "Cropped jacket, frog closures", [
   ("Off-White", "cowan", (.33,.24,.43,.4), "0,360", "0,0.2", "0.6,1"),
   ("Black", "cowan", (.44,.5,.56,.75), *DARK)]),
 ("07-ralph-lauren", "RALPH LAUREN SS27", "Jacquard cutaway jacket", [
   ("Ivory", "ralph-lauren", (.42,.23,.58,.38), *WHITE),
   ("Navy", "ralph-lauren", (.4,.52,.5,.75), "200,250", "0.2,1", "0,0.35")]),
 ("08-susan-fang", "SUSAN FANG SS27", "Lace qipao-style dress", [("White", "susan-fang", (.44,.22,.56,.42), *WHITE)]),
 ("09-mame-kurogouchi", "MAME KUROGOUCHI SS27", "Tunic with knot closures", [
   ("White", "mame-kurogouchi-po", (.42,.38,.58,.58), *WHITE),
   ("Ink", "mame-kurogouchi-po", (.38,.23,.62,.29), "0,360", "0,1", "0,0.35")]),
 ("10-alberta-ferretti", "ALBERTA FERRETTI SS27", "Satin pajama suit", [("Champagne", "ferretti", (.4,.25,.6,.45), "20,70", "0.03,0.4", "0.6,1")]),
 ("11-onori", "ONORI SS27", "Mandarin collar dress", [("Pale Yellow", "onori", (.42,.26,.58,.48), "35,70", "0.08,0.6", "0.6,1")]),
 ("12-kim-shui", "KIM SHUI SS27", "Jacquard top and skirt", [
   ("Pale Gold", "kim-shui", (.4,.27,.6,.48), "20,60", "0.08,0.6", "0.6,1"),
   ("Blossom Pink", "kim-shui", (.36,.25,.64,.52), "-40,5", "0.15,1", "0.6,1")]),
 ("13-ao-yes", "AO YES SS27", "Floral blouse", [("Blush Cream", "ao-yes-po", (.38,.24,.58,.4), "0,360", "0,0.3", "0.55,1")]),
 ("14-hui", "HUI SS27", "Top with frog closures", [("Sage", "hui", (.4,.25,.58,.37), "50,120", "0.05,0.5", "0.5,1")]),
 ("15-elie-saab", "ELIE SAAB SS27", "Cropped jacket and skirt", [
   ("Olive", "elie-saab", (.4,.23,.6,.34), "40,90", "0.15,1", "0.2,0.6"),
   ("Pastel Green", "elie-saab", (.4,.5,.58,.72), "50,140", "0.08,0.6", "0.5,1")]),
]
looks = []
for slug, house, look, cols in L:
    out = []
    for name, photo, (a, b, c, d), h, s, v in cols:
        p = os.path.join(HERE, "photos", photo + ".png"); W, H = Image.open(p).size
        box = f"{int(a*W)},{int(b*H)},{int(c*W)},{int(d*H)}"
        r = subprocess.run(["python3", "-I", SK, p, box, h, s, v], capture_output=True, text=True).stdout.strip()
        print(f"{slug:32s} {name:14s} {r}")
        hx, n = r.split()[0], int(r.split()[2])
        assert n >= 300, (slug, name, n)
        out.append([name, hx])
    looks.append({"slug": slug, "house": house, "look": look, "colours": out})
json.dump(looks, open(os.path.join(HERE, "data", "looks.json"), "w"), indent=1)
