# Builds drafts/fw27-forecast-build.html from the draft markdown + the chart/visual PNGs.
# Usage: python3 build_html.py ../fw27-forecast-trendalytics-draft.md ../fw27-forecast-build.html
import re, sys, html
sys.dont_write_bytecode = True
src, dst = sys.argv[1], sys.argv[2]
COLOUR = 'colour' in src
md = open(src, encoding='utf-8').read()
md = re.sub(r'<!--.*?-->', '', md, flags=re.S).strip()
for bad in ('–', '—'):
    assert bad not in md
C = 'fw27-forecast-charts/'
PINK, OFF = '#D6447A', '#F7F6F4'

ITEMS = {
 'Heritage Craft': [('item-mary-jane-pumps.png', 'Mary Jane pumps', '3M views on TikTok'), ('item-jacquard-jacket.png', 'Jacquard jacket', 'searches up 61% on last year'),
                    ('item-paisley-scarf.png', 'Paisley scarf', 'searches up 64% on last year'), ('item-tailored-suiting.png', 'Tailored suiting', 'slim suits up 133% in market adoption')],
 'Sensory Riot': [('item-daytime-boa.png', 'Daytime boa', 'fur scarves up 30% in searches'), ('item-fringe-skirt.png', 'Fringe skirt', 'searches up 71% on last year'),
                  ('item-sculptural-wedges.png', 'Sculptural wedges', 'searches up 23% on last year'), ('item-embellished-jeans.png', 'Embellished jeans', 'up 23% in market adoption')],
 'Veiled Performance': [('item-drawstring-pants.png', 'Drawstring pants', 'up 33% among key influencers'), ('item-nylon-bag.png', 'Nylon bag', 'up 28% in market adoption'),
                        ('item-funnel-neck-jacket.png', 'Funnel neck jacket', 'up 888% among key influencers'), ('item-rain-boots.png', 'Rain boots', 'up 87% among key influencers')],
}
SLUG = {'Heritage Craft': 'heritage-craft', 'Sensory Riot': 'sensory-riot', 'Veiled Performance': 'veiled-performance'}

def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r'\[([^\]]+)\]\((LINK[^)]*)\)', r'<a href="#" class="todo" title="\2">\1</a>', t)
    t = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', t)
    t = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', t)
    return t

def visuals_for(aesthetic):
    if COLOUR: return ''
    s = SLUG[aesthetic]
    items = ''.join(f'<figure class="item"><img src="{C}images/{f}" alt="{html.escape(n)}, Trendalytics FW27 key item"><figcaption><strong>{html.escape(n)}</strong><br>{html.escape(d)}</figcaption></figure>' for f, n, d in ITEMS[aesthetic])
    return (f'<figure class="chart"><img src="{C}07-runway-{s}.png" alt="The three SS27 runway looks Trendalytics names for {aesthetic}"></figure>'
            f'<div class="items">{items}</div>')

doc_title = re.search(r'^# (.+)$', md, re.M).group(1)
out, lines, i, current = [], md.split('\n'), 0, None
title_done = False
while i < len(lines):
    l = lines[i]
    if l.startswith('# '):
        t = l[2:]; i += 1
        sub = ''
        while i < len(lines) and not lines[i].strip(): i += 1
        if i < len(lines) and lines[i].startswith('## '):
            sub = lines[i][3:]; i += 1
        out.append(f'<header class="hero"><p class="kicker">Runway Decode, forecast edition</p><h1>{html.escape(t.split(": ")[0])}:<br><em>{html.escape(t.split(": ",1)[1])}</em></h1><p class="sub">{inline(sub)}</p></header><main>')
        continue
    if l.startswith('## '):
        if current and current in ITEMS: out.append(visuals_for(current)); current = None
        h = l[3:]
        if h == 'The Takeaway': out.append('</main><section class="takeaway"><h2>The Takeaway</h2>'); current = 'TAKEAWAY'
        elif h == 'Full methodology': out.append('</section><footer class="method"><h2>Full methodology</h2>'); current = 'METHOD'
        elif h == 'Sources': out.append('<h2>Sources</h2>')
        else: out.append(f'<h2>{inline(h)}</h2>')
        i += 1; continue
    if l.startswith('### '):
        if current and current in ITEMS: out.append(visuals_for(current)); current = None
        h = l[4:]
        for a in ITEMS:
            if h.startswith(a + ':') and not COLOUR: current = a
        out.append(f'<h3>{inline(h)}</h3>'); i += 1; continue
    m = re.match(r'\[CHART: ([^,]+), (.+)\]', l)
    if m:
        out.append(f'<figure class="chart"><img src="{C}{m.group(1)}" alt="{html.escape(m.group(2))}"><figcaption>{html.escape(m.group(2))}</figcaption></figure>'); i += 1; continue
    if l.startswith('> '):
        q = []
        while i < len(lines) and lines[i].startswith('>'):
            q.append(lines[i][1:].strip()); i += 1
        body = ' '.join(x for x in q if x and x != '**In The Press**')
        out.append(f'<aside class="press"><span class="label">In The Press</span><p>{inline(body)}</p></aside>'); continue
    if l.startswith('- '):
        li = []
        while i < len(lines) and lines[i].startswith('- '):
            li.append(f'<li>{inline(lines[i][2:])}</li>'); i += 1
        out.append('<ul>' + ''.join(li) + '</ul>'); continue
    if l.strip():
        out.append(f'<p>{inline(l)}</p>')
    i += 1
out.append('</footer>')

css = f'''
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Questrial&display=swap');
:root{{--pink:{PINK};--off:{OFF};--ink:#222}}
body{{margin:0;background:#fff;color:var(--ink);font-family:'Century Gothic','Questrial','Avenir',sans-serif;font-size:18px;line-height:1.6}}
.hero,.takeaway{{background:#000;color:#fff;border-top:6px solid var(--pink);padding:56px 24px 48px}}
.hero .kicker{{color:var(--pink);text-transform:uppercase;letter-spacing:2px;font-size:13px;margin:0 0 18px}}
h1,h2,h3{{font-family:'DM Serif Display',Georgia,serif;font-weight:400;line-height:1.15}}
.hero h1{{font-size:46px;margin:0 0 18px;max-width:900px}} .hero h1 em{{font-style:italic;color:var(--pink)}}
.hero .sub{{font-size:22px;max-width:820px;margin:0;color:#ddd}}
main,.method{{max-width:760px;margin:0 auto;padding:24px 24px 40px}}
h2{{font-size:34px;margin:48px 0 10px}} h3{{font-size:26px;margin:36px 0 8px}}
a{{color:var(--pink)}} a.todo{{border-bottom:2px dashed var(--pink);text-decoration:none}}
figure.chart{{background:var(--off);margin:28px 0;padding:18px;border-radius:2px}}
figure.chart img{{width:100%;display:block}} figcaption{{font-size:14px;color:#555;margin-top:10px}}
.press{{background:var(--off);border-left:4px solid var(--pink);padding:18px 22px;margin:26px 0}}
.press .label{{display:block;color:var(--pink);text-transform:uppercase;letter-spacing:2px;font-size:12px;margin-bottom:8px}}
.press p{{margin:0;font-size:16px}}
.items{{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin:0 0 30px}}
.item{{margin:0}} .item img{{width:100%;aspect-ratio:3/4;object-fit:cover;object-position:top;display:block}}
.item figcaption{{font-size:13px;line-height:1.35}}
.palettes figure.chart{{margin:18px 0}}
.takeaway{{padding:48px 24px}} .takeaway h2,.takeaway ul,.takeaway p{{max-width:760px;margin-left:auto;margin-right:auto}}
.takeaway h2{{margin-top:0;color:#fff}} .takeaway li{{margin-bottom:10px}}
.method{{font-size:15px;color:#444}} .method h2{{font-size:26px}}
@media (max-width:640px){{.items{{grid-template-columns:repeat(2,1fr)}} .hero h1{{font-size:34px}}}}
'''
page = f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(doc_title)}</title><style>{css}</style></head><body>{"".join(out)}</body></html>'
assert '—' not in page and '–' not in page
open(dst, 'w', encoding='utf-8').write(page); print('wrote', dst, len(page))
