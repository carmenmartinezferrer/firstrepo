# Instagram carousel slides (1080x1350) for the FW27 forecast colour post and trends post.
# Numbers as printed in the forecast PDF; Paris SS27 figures from the DFB tagging in this repo.
# Usage: python3 build_slides.py . && NODE_PATH=$(npm root -g) node render_slides.js . .
import html, json, sys
sys.dont_write_bytecode = True
OUT = sys.argv[1]
PINK, INK, MUTED, OFF, OUTLINE = '#D6447A', '#1a1a1a', '#6B6B6B', '#F7F6F4', '#D0CCC5'

def lum(hx):
    r, g, b = (int(hx[i:i+2], 16) / 255 for i in (1, 3, 5))
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)

HC = [('russet red', '#7B3330', 'searches +50% this year vs last'), ('plum purple', '#583759', 'searches +60% this year vs last'),
      ('forest green', '#254117', 'searches +50% this year vs last'), ('chestnut brown', '#7C533C', 'searches +10%, but 196M TikTok views')]
SR = [('chartreuse', '#C7D344', 'searches +10%, but 149M TikTok views'), ('fuchsia', '#FF278A', 'searches +20% this year vs last'),
      ('lilac', '#927EC3', 'searches +10% this year vs last'), ('cobalt blue', '#4C80FD', 'searches +30% this year vs last')]
VP = [('marigold', '#DFAA4F', 'searches +30%, and the most searched of the twelve'), ('moss green', '#7E8C53', 'searches +60% this year vs last'),
      ('dove grey', '#838384', 'searches +30% this year vs last'), ('terracotta', '#D38377', 'searches +10% this year vs last')]
GROWTH = {'russet red': 50, 'plum purple': 60, 'forest green': 50, 'chestnut brown': 10, 'chartreuse': 10, 'fuchsia': 20, 'lilac': 10, 'cobalt blue': 30,
          'marigold': 30, 'moss green': 60, 'dove grey': 30, 'terracotta': 10}
AES = [('Heritage Craft', 'stealth wealth with an artisanal touch', HC),
       ('Sensory Riot', 'maximalism, bold colour, clashing prints', SR),
       ('Veiled Performance', 'sportswear meets rugged utility', VP)]


import math
def ring(groups, R=400, w=0.42, gap=3.0, label_r=None, size=1000, font=26, show_names=True, values=None, vfont=30):
    """groups: list of lists of (name, hex). Equal wedges, a small gap between groups, largest arc starting at 12 o'clock, clockwise.
    A colour map, not a share chart: every wedge is the same size on purpose."""
    n = sum(len(g) for g in groups); ng = len(groups)
    span = (360 - gap * (ng if ng > 1 else 0)) / n
    cx = cy = size / 2; r_out = R; r_in = R * (1 - w); lr = label_r or (R + 48)
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" width="{size}" height="{size}" overflow="visible" style="overflow:visible">']
    a = -90.0
    for g in groups:
        for name, hx in g:
            a0, a1 = a, a + span
            p0 = (cx + r_out * math.cos(math.radians(a0)), cy + r_out * math.sin(math.radians(a0)))
            p1 = (cx + r_out * math.cos(math.radians(a1)), cy + r_out * math.sin(math.radians(a1)))
            q1 = (cx + r_in * math.cos(math.radians(a1)), cy + r_in * math.sin(math.radians(a1)))
            q0 = (cx + r_in * math.cos(math.radians(a0)), cy + r_in * math.sin(math.radians(a0)))
            large = 1 if span > 180 else 0
            d = f'M{p0[0]:.1f} {p0[1]:.1f} A{r_out} {r_out} 0 {large} 1 {p1[0]:.1f} {p1[1]:.1f} L{q1[0]:.1f} {q1[1]:.1f} A{r_in} {r_in} 0 {large} 0 {q0[0]:.1f} {q0[1]:.1f} Z'
            stroke = f' stroke="{OUTLINE}" stroke-width="2"' if lum(hx) > 0.82 else ''
            out.append(f'<path d="{d}" fill="{hx}"{stroke}/>')
            if values and name in values:
                mm = math.radians((a0 + a1) / 2); vr = (r_out + r_in) / 2
                vx, vy = cx + vr * math.cos(mm), cy + vr * math.sin(mm)
                vcol = '#FFFFFF' if lum(hx) < 0.55 else '#000000'
                out.append(f'<text x="{vx:.1f}" y="{vy + vfont*0.35:.1f}" text-anchor="middle" font-family="Arimo, Arial, sans-serif" font-size="{vfont}" fill="{vcol}">+{values[name]}%</text>')
            if show_names:
                m = math.radians((a0 + a1) / 2); lx, ly = cx + lr * math.cos(m), cy + lr * math.sin(m)
                anchor = 'start' if math.cos(m) > 0.25 else ('end' if math.cos(m) < -0.25 else 'middle')
                out.append(f'<text x="{lx:.1f}" y="{ly + font*0.35:.1f}" text-anchor="{anchor}" font-family="Century Gothic, Questrial, sans-serif" font-size="{font}" fill="{INK}">{html.escape(name)}</text>')
            a = a1
        a += gap
    out.append('</svg>'); return '\n'.join(out)

def donut(items, size=810):
    """Carmen's locked DFB donut: ring 42% of radius, largest wedge at 12 o'clock clockwise, whole-number %
    labels inside at 79% of the radius, 42px if >= 15, 32px if >= 8, else 24, white if luminance < 0.55."""
    total = sum(v for _, v, _ in items); R = size / 2; r_in = R * 0.58; cx = cy = R
    pct = [round(100 * v / total) for _, v, _ in items]
    diff = 100 - sum(pct); pct[0] += diff
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" width="{size}" height="{size}">']
    a = -90.0
    for (name, v, hx), p in zip(items, pct):
        span = 360 * p / 100; a0, a1 = a, a + span
        P = lambda r, ang: (cx + r * math.cos(math.radians(ang)), cy + r * math.sin(math.radians(ang)))
        p0, p1, q1, q0 = P(R, a0), P(R, a1), P(r_in, a1), P(r_in, a0)
        large = 1 if span > 180 else 0
        d = f'M{p0[0]:.1f} {p0[1]:.1f} A{R} {R} 0 {large} 1 {p1[0]:.1f} {p1[1]:.1f} L{q1[0]:.1f} {q1[1]:.1f} A{r_in} {r_in} 0 {large} 0 {q0[0]:.1f} {q0[1]:.1f} Z'
        stroke = f' stroke="{OUTLINE}" stroke-width="1.2"' if lum(hx) > 0.82 else ''
        out.append(f'<path d="{d}" fill="{hx}"{stroke}/>')
        fs = 42 if p >= 15 else (32 if p >= 8 else 24)
        lx, ly = P(R * 0.79, (a0 + a1) / 2)
        col = '#FFFFFF' if lum(hx) < 0.55 else '#000000'
        out.append(f'<text x="{lx:.1f}" y="{ly + fs * 0.35:.1f}" text-anchor="middle" font-family="Arimo, Arial, sans-serif" font-size="{fs}" fill="{col}">{p}%</text>')
        a = a1
    out.append('</svg>'); return '\n'.join(out), pct

CSS = f'''
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Questrial&display=swap');
body{{margin:0;background:#fff}}
#slide{{width:1080px;height:1350px;box-sizing:border-box;padding:84px 72px 72px;background:#fff;color:{INK};font-family:'Century Gothic','Questrial',sans-serif;position:relative;overflow:hidden;display:flex;flex-direction:column}}
#slide.dark{{background:#000;color:#fff}}
.kicker{{color:{PINK};text-transform:uppercase;letter-spacing:3px;font-size:22px;margin:0 0 22px}}
h1{{font-family:'DM Serif Display',Georgia,serif;font-weight:400;font-size:72px;line-height:1.05;margin:0 0 22px}}
h1 em{{font-style:italic;color:{PINK}}}
h2{{font-family:'DM Serif Display',Georgia,serif;font-weight:400;font-size:56px;line-height:1.08;margin:0 0 14px}}
.sub{{font-size:28px;line-height:1.35;color:{MUTED};margin:0 0 40px}} .dark .sub{{color:#bbb}}
.body{{font-size:30px;line-height:1.4}}
.grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:18px;margin-top:10px}}
.grid .sq{{aspect-ratio:1;border-radius:4px}} .grid .nm{{font-size:22px;margin-top:10px;line-height:1.2}}
.rowlab{{font-family:'DM Serif Display',Georgia,serif;font-size:34px;margin:34px 0 10px}}
.sw4{{display:grid;grid-template-columns:1fr 1fr;gap:28px;flex:1}}
.sw4 .sq{{height:300px;border-radius:4px}} .sw4 .nm{{font-family:'DM Serif Display',Georgia,serif;font-size:40px;margin:14px 0 2px}}
.sw4 .hx{{font-size:22px;color:{MUTED}}} .sw4 .dp{{font-size:26px;margin-top:6px}}
.bars{{display:flex;flex-direction:column;gap:44px;flex:1;justify-content:center}}
.bar{{display:grid;grid-template-columns:270px 1fr 150px;align-items:center;gap:18px}}
.bar .lab{{font-size:28px;line-height:1.15;text-align:right}} .bar .track{{height:92px}} .bar .fill{{height:100%;border-radius:3px}}
.bar .val{{font-family:'DM Serif Display',Georgia,serif;font-size:44px}}
.small .bar{{grid-template-columns:300px 1fr 150px;gap:16px}} .small .bar .track{{height:44px}} .small .bar{{gap:16px}} .bars.small{{gap:26px}} .small .bar .lab{{font-size:25px}} .small .bar .val{{font-size:36px}}
.foot{{font-size:20px;color:{MUTED};margin-top:auto;padding-top:24px}} .dark .foot{{color:#999}}
.big{{font-family:'DM Serif Display',Georgia,serif;font-size:150px;line-height:1;margin:10px 0 0}}
.stat{{display:flex;align-items:baseline;gap:22px;margin:18px 0}} .stat .n{{font-family:'DM Serif Display',Georgia,serif;font-size:84px;min-width:300px}} .stat .t{{font-size:28px;line-height:1.3}}
.pill{{display:inline-block;background:{PINK};color:#fff;padding:10px 22px;font-size:24px;letter-spacing:2px;text-transform:uppercase;margin-top:auto}}
.list{{font-size:30px;line-height:1.45;margin:0;padding-left:0;list-style:none}} .list li{{margin-bottom:22px}} .list b{{font-family:'DM Serif Display',Georgia,serif;font-weight:400;font-size:38px;display:block}}
.pg{{position:absolute;right:72px;top:84px;font-size:22px;color:{MUTED}}}
.ringwrap{{flex:1;display:flex;align-items:center;justify-content:center}} .ringwrap svg{{width:940px;height:940px;overflow:visible}} .ringwrap.small svg{{width:620px;height:620px}} .ringwrap.donut svg{{width:700px;height:700px}}
.grp{{display:flex;justify-content:space-between;font-size:22px;color:{MUTED};margin-top:-10px}} .grp b{{color:{INK};font-weight:normal}}
'''

def page(inner, dark=False):
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div id="slide" class="{"dark" if dark else ""}">{inner}</div></body></html>'

def swatch(hx, cls='sq'):
    border = f'border:2px solid {OUTLINE};' if lum(hx) > 0.82 else ''
    return f'<div class="{cls}" style="background:{hx};{border}"></div>'

def bars(items, fmt, colour=lambda i, it: None, small=False):
    vmax = max(v for _, v, *_ in items)
    rows = ''
    for i, it in enumerate(items):
        lab, v = it[0], it[1]
        col = colour(i, it) or ('#3A3A3A' if i else PINK)
        border = f'border:2px solid {OUTLINE};' if lum(col) > 0.82 else ''
        rows += f'<div class="bar"><div class="lab">{html.escape(lab)}</div><div class="track"><div class="fill" style="width:{100*v/vmax:.1f}%;background:{col};{border}"></div></div><div class="val">{fmt(v)}</div></div>'
    return f'<div class="bars{" small" if small else ""}">{rows}</div>'

slides = {}
# ---------- Carousel A: colour ----------

cover_ring = ring([[(n, hx) for n, hx, _ in cols] for _, _, cols in AES], R=300, w=0.5, label_r=340, font=26, values=GROWTH, vfont=28)
slides['A1-cover'] = page(f'<p class="kicker">Stop calling everything a trend</p><h1>The <em>Fall/Winter 2027</em> colours, and how fast each one is growing</h1><p class="sub" style="margin-bottom:0">Twelve colours, three moods, one ring. The number in each wedge is the growth in Google searches this year against last.</p><div class="ringwrap">{cover_ring}</div><div class="grp"><span><b>Heritage Craft</b> top right</span><span><b>Sensory Riot</b> bottom</span><span><b>Veiled Performance</b> top left</span></div><div class="foot">Wedges are the same size on purpose: this is a colour map with growth written on it, not a share chart.</div>')
g12 = sorted([(n, GROWTH[n], hx) for _, _, cols in AES for n, hx, _ in cols], key=lambda x: -x[1])
slides['A2-growth-all'] = page(f'<p class="kicker">Same scale, all twelve</p><h2>Plum and moss green are the climbers, four colours barely move</h2><p class="sub">% change in Google searches this year vs last, all twelve colours on one scale.</p>{bars(g12, lambda v: f"+{v}%", colour=lambda i, it: it[2], small=True)}<div class="pg">2/7</div>')
for k, (name, desc, cols) in enumerate(AES, start=3):
    r4 = ring([[(n, hx) for n, hx, _ in cols]], R=330, w=0.46, gap=0, label_r=390, font=34)
    legend = ''.join(f'<div style="display:flex;align-items:center;gap:14px;font-size:24px;line-height:1.25"><span style="display:inline-block;width:26px;height:26px;border-radius:50%;background:{hx};flex:none"></span><span><b style="font-family:\'DM Serif Display\',Georgia,serif;font-weight:normal;font-size:26px">{n}</b> <span style="color:{MUTED}">{hx}</span><br>{d}</span></div>' for n, hx, d in cols)
    slides[f'A{k}-{name.lower().replace(" ", "-")}'] = page(f'<p class="kicker">{name}</p><h2>{desc}</h2><div class="ringwrap small" style="flex:none;margin:30px 0 40px">{r4}</div><div style="display:grid;grid-template-columns:1fr 1fr;gap:22px 28px;margin-top:auto">{legend}</div><div class="pg">{k}/7</div>')

vol = [('marigold', 126, '#DFAA4F'), ('lilac', 103, '#927EC3'), ('fuchsia', 84, '#FF278A'), ('forest green', 57, '#254117'), ('dark red', 35, '#7B3330')]
dsvg, dpct = donut(vol)
dleg = ''.join('<div style="display:flex;align-items:center;gap:12px;font-size:24px"><span style="display:inline-block;width:24px;height:24px;border-radius:50%;background:' + hx + ';flex:none"></span><span><b style="font-family:DM Serif Display,Georgia,serif;font-weight:normal;font-size:26px">' + n + '</b> <span style="color:' + MUTED + '">' + str(v) + 'k searches</span></span></div>' for (n, v, hx), p in zip(vol, dpct))
dsmall = dsvg.replace('width="810" height="810"', 'width="740" height="740"')
cover_title = "Growth is one thing, volume is another: the five with a published search volume"
cover_foot = "% = each colour's share of the combined searches for the five colours that come with a search volume. The other seven have no published volume."
slides['A6-search-share'] = page('<p class="kicker">And by volume</p><h1>' + cover_title + '</h1><div class="ringwrap donut" style="flex:none;margin:10px 0 30px">' + dsvg + '</div><div style="display:grid;grid-template-columns:1fr 1fr;gap:16px 24px;margin-top:auto">' + dleg + '</div><div class="foot">' + cover_foot + '</div><div class="pg">6/7</div>')
print('donut shares', dict(zip([n for n,_,_ in vol], dpct)))
_unused = (f'<p class="kicker">Ordered by searches</p><h2>Marigold is the most searched of the twelve</h2><p class="sub">Search volume, in thousands of searches. Only five of the twelve colours come with one.</p>{bars(vol, lambda v: f"{v}k", colour=lambda i, it: it[2])}<div class="foot">No period or country is published for these volumes, so they are quoted as given.</div><div class="pg">5/7</div>')
gro = [('dove grey', 43, '#838384'), ('plum purple', 39, '#583759'), ('moss green', 23, '#7E8C53'), ('cobalt blue', 14, '#4C80FD'), ('terracotta', 7, '#D38377')]
slides['A7-close'] = page(f'<p class="kicker">The takeaway</p><h2>The ones that exist, and the ones that are moving</h2><div class="stat"><div class="n">+60%</div><div class="t">plum purple and moss green, the fastest climbers</div></div><div class="stat"><div class="n">+10%</div><div class="t">lilac, chartreuse, chestnut brown and terracotta</div></div><p class="body" style="margin-top:30px">Twelve colours, three different yardsticks in the forecast, not one measured twice. So I pulled all twelve myself: plum and moss green up 60%, dark red and forest green up 50%, and four colours up just 10%.</p><p class="body" style="margin-top:20px">A colour whose searches grew 10% in a year is not a forecast, it is a colour that exists. My bet: marigold for volume, plum for growth.</p><div class="pill">Full piece on Substack</div><div class="pg">7/7</div>', dark=True)

# ---------- Carousel B: trends ----------
slides['B1-cover'] = page(f'<p class="kicker">Stop calling everything a trend</p><h1>The <em>Fall/Winter 2027</em> trends you\'ll see on next year\'s runways, ranked by the numbers</h1><p class="sub">A forecast gave me 36 trends. I put every one on the same scale to see which are actually moving.</p><div class="big" style="color:{PINK}">36</div><p class="body">named trends, six different yardsticks, zero measured twice</p><div class="foot">The Data Fashion Brief</div>')
aes_items = [('Heritage Craft', 'plaid, lace, painterly florals, tweed', 'Mary Jane pumps, jacquard jackets, paisley scarves, slim suiting'),
             ('Sensory Riot', 'feather trim, animal stripes, lustrous silk, graphic prints', 'daytime boa, fringe skirt, sculptural wedges, embellished jeans'),
             ('Veiled Performance', 'nylon and PVC, acid wash denim, landscape graphics, camo', 'drawstring pants, nylon bag, funnel neck jacket, rain boots')]
lis = ''.join(f'<li><b>{a}</b>Fabrics: {f}.<br>Key items: {k}.</li>' for a, f, k in aes_items)
slides['B2-aesthetics'] = page(f'<p class="kicker">The three aesthetics</p><h2>What the forecast says FW27 is made of</h2><ul class="list">{lis}</ul><div class="foot">Swipe for which of these the numbers actually back.</div><div class="pg">2/7</div>')
sg = [('fringe skirts', 71), ('paisley scarves', 64), ('jacquard jackets', 61), ('dove grey', 43), ('plum purple', 39), ('fur scarves', 30), ('moss green', 23), ('wedges', 23), ('acid wash denim', 21), ('cobalt blue', 14), ('terracotta', 7)]
slides['B3-search-growth'] = page(f'<p class="kicker">Same scale, head to head</p><h2>Fringe skirts are the top search mover</h2><p class="sub">% change in searches vs last year, for the eleven items measured that way.</p>{bars(sg, lambda v: f"+{v}%", small=True)}<div class="pg">3/7</div>')
ma = [('artistic florals', 178), ('slim suits', 133), ('graphic prints', 51), ('camouflage', 43), ('nylon', 38), ('feather trim', 36), ('nylon bags', 28), ('landscape graphics', 26), ('embellished jeans', 23), ('plaid', 21)]
slides['B4-market-adoption'] = page(f'<p class="kicker">Same scale, head to head</p><h2>Florals and slim suits are the two real jumps</h2><p class="sub">% change vs last year in market adoption, for the ten items measured that way.</p>{bars(ma, lambda v: f"+{v}%", small=True)}<div class="pg">4/7</div>')
slides['B5-unrankable'] = page(f'<p class="kicker">The numbers that compare with nothing</p><h2>Nine items come with a yardstick too rare to rank</h2><div class="stat"><div class="n">+888%</div><div class="t">funnel neck jackets, among key influencers. Base size not given.</div></div><div class="stat"><div class="n">+87%</div><div class="t">rain boots, same measure. Drawstring pants +33%.</div></div><div class="stat"><div class="n">196M</div><div class="t">TikTok views for chestnut brown. Chartreuse 149M, Mary Jane pumps 3M, zebra print "5M a week".</div></div><div class="stat"><div class="n">none</div><div class="t">tweed and silk are "most saturated in luxury", with no number at all.</div></div><div class="foot">888% from almost nothing is exactly how a funnel neck starts to look like a movement.</div><div class="pg">5/7</div>')
pc = [('silk (all types)', 28), ('tweed', 5), ('lace', 4), ('denim', 4), ('nylon', 4), ('animal print', 3), ('brocade / jacquard', 2)]
slides['B6-paris'] = page(f'<p class="kicker">My own runway check</p><h2>What the Paris SS27 runway already shows</h2><p class="sub">% of all Paris SS27 looks that include each forecast fabric, from my tagging of 16 houses and 997 looks.</p>{bars(pc, lambda v: f"{v}%")}<div class="foot">Silk is where the forecast and my data agree. Tweed is 5% of looks and almost all Chanel, which put it in 42% of its own collection.</div><div class="pg">6/7</div>')
slides['B7-close'] = page(f'<p class="kicker">The takeaway</p><h2>Thirty-six trends, six yardsticks, zero measured twice</h2><ul class="list" style="margin-top:20px"><li><b>Heritage Craft</b>strongest shared numbers, weakest colours.</li><li><b>Sensory Riot</b>most outside agreement: fringe has search, retail and the runway behind it.</li><li><b>Veiled Performance</b>the biggest single search number (marigold) and the weakest everything else.</li></ul><p class="body" style="margin-top:10px">My bet for the shops: the fringe skirt.</p><div class="pill">Full piece on Substack</div><div class="pg">7/7</div>', dark=True)

for name, h in slides.items():
    assert '—' not in h and '–' not in h, name
    open(f'{OUT}/{name}.html', 'w').write(h)
json.dump(list(slides), open(f'{OUT}/slides.json', 'w')); print(list(slides))
