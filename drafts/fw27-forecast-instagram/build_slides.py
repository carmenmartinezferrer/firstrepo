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

HC = [('russet red', '#7B3330', 'search volume 35k'), ('plum purple', '#583759', 'searches +39% on last year'),
      ('forest green', '#254117', 'search volume 57k'), ('chestnut brown', '#7C533C', '196M TikTok views')]
SR = [('chartreuse', '#C7D344', '149M TikTok views'), ('fuchsia', '#FF278A', 'search volume 84k'),
      ('lilac', '#927EC3', 'search volume 103k'), ('cobalt blue', '#4C80FD', 'searches +14% on last year')]
VP = [('marigold', '#DFAA4F', 'search volume 126k'), ('moss green', '#7E8C53', 'searches +23% on last year'),
      ('dove grey', '#838384', 'searches +43% on last year'), ('terracotta', '#D38377', 'searches +7% on last year')]
AES = [('Heritage Craft', 'stealth wealth with an artisanal touch', HC),
       ('Sensory Riot', 'maximalism, bold colour, clashing prints', SR),
       ('Veiled Performance', 'sportswear meets rugged utility', VP)]

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
grid = ''.join(f'<div>{swatch(hx)}<div class="nm">{n}</div></div>' for _, _, cols in AES for n, hx, _ in cols)
slides['A1-cover'] = page(f'<p class="kicker">Stop calling everything a trend</p><h1>The 12 colours you\'ll see on the <em>Fall/Winter 2027</em> runways</h1><p class="sub">Three aesthetics, four colours each. Swipe for why these twelve, and which ones are actually being searched.</p><div class="grid">{grid}</div><div class="foot">The Data Fashion Brief</div>')
for k, (name, desc, cols) in enumerate(AES, start=2):
    sw = ''.join(f'<div>{swatch(hx)}<div class="nm">{n}</div><div class="hx">{hx}</div><div class="dp">{d}</div></div>' for n, hx, d in cols)
    slides[f'A{k}-{name.lower().replace(" ", "-")}'] = page(f'<p class="kicker">{name}</p><h2>{desc}</h2><p class="sub">The four colours of this aesthetic, and the one number behind each.</p><div class="sw4">{sw}</div><div class="foot">Hex sampled from the forecast\'s own swatches. Data points as printed in the forecast.</div><div class="pg">{k}/7</div>')
vol = [('marigold', 126, '#DFAA4F'), ('lilac', 103, '#927EC3'), ('fuchsia', 84, '#FF278A'), ('forest green', 57, '#254117'), ('dark red', 35, '#7B3330')]
slides['A5-search-volume'] = page(f'<p class="kicker">Ordered by searches</p><h2>Marigold is the most searched of the twelve</h2><p class="sub">Search volume, in thousands of searches. Only five of the twelve colours come with one.</p>{bars(vol, lambda v: f"{v}k", colour=lambda i, it: it[2])}<div class="foot">The forecast gives no period or country for these volumes, so they are quoted as printed.</div><div class="pg">5/7</div>')
gro = [('dove grey', 43, '#838384'), ('plum purple', 39, '#583759'), ('moss green', 23, '#7E8C53'), ('cobalt blue', 14, '#4C80FD'), ('terracotta', 7, '#D38377')]
slides['A6-search-growth'] = page(f'<p class="kicker">Ordered by search growth</p><h2>Dove grey is the fastest climber, terracotta barely moved</h2><p class="sub">% change in searches vs last year, for the five colours measured that way.</p>{bars(gro, lambda v: f"+{v}%", colour=lambda i, it: it[2])}<div class="foot">A colour whose searches grew 7% in a year is not a forecast, it is a colour that exists.</div><div class="pg">6/7</div>')
slides['A7-close'] = page(f'<p class="kicker">And the last two</p><h2>Chestnut brown and chartreuse only have TikTok views</h2><div class="stat"><div class="n">196M</div><div class="t">views for chestnut brown</div></div><div class="stat"><div class="n">149M</div><div class="t">views for chartreuse</div></div><p class="body" style="margin-top:30px">Twelve colours, three different yardsticks, not one colour measured twice. That is why I line them up on one scale before I call any of them a trend.</p><p class="body" style="margin-top:20px">On my own Paris SS27 tagging, red was 2% of the palette and purple 1%. The runway is not where the Heritage Craft signal is coming from yet.</p><div class="pill">Full piece on Substack</div><div class="pg">7/7</div>', dark=True)

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
