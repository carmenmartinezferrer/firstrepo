"""Learning staircase on a white 1080x1920 canvas: four steps and three steps.
Usage: python3 -I make_learning_bars.py <out_dir>
"""
import sys
OUT = sys.argv[1]
SANS = "font-family=\"'Century Gothic', 'TeX Gyre Adventor', 'URW Gothic', Arial, sans-serif\""
BLACK, PINK = "#111111", "#D6447A"

def build(name, labels, title):
    n = len(labels)
    width = 840 if n == 3 else 880
    bw = width // n
    x0 = (1080 - bw * n) // 2
    base = 1650
    step = (820 - 220) // (n - 1) if n > 1 else 0
    low = 220 if n == 4 else 300
    top = 820 if n == 4 else 820
    hs = [low + (top - low) * i // (n - 1) for i in range(n)]
    out = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920" width="1080" height="1920" role="img" '
           f'aria-label="{title}">\n  <title>{title}</title>\n  <rect width="1080" height="1920" fill="#FFFFFF"/>\n')
    out += f'  <text x="540" y="170" text-anchor="middle" {SANS} font-size="64" font-weight="700" fill="#111111">learn to code, step by step</text>\n'
    out += f'  <text x="540" y="238" text-anchor="middle" {SANS} font-size="32" fill="#777777">each one builds on the last</text>\n'
    for i, (lab, h) in enumerate(zip(labels, hs)):
        x = x0 + i * bw
        fill = PINK if i == n - 1 else BLACK
        out += f'  <rect x="{x}" y="{base - h}" width="{bw}" height="{h}" fill="{fill}"/>\n'
        out += f'  <text x="{x + bw // 2}" y="{base - h + 80}" text-anchor="middle" {SANS} font-size="44" font-weight="700" fill="#FFFFFF">{lab}</text>\n'
    for i in range(1, n):
        x = x0 + i * bw
        out += f'  <line x1="{x}" y1="{base - hs[i]}" x2="{x}" y2="{base}" stroke="#FFFFFF" stroke-width="4"/>\n'
    out += f'  <line x1="{x0 - 30}" y1="{base}" x2="{x0 + bw * n + 30}" y2="{base}" stroke="#222222" stroke-width="6" stroke-linecap="round"/>\n'
    out += '</svg>\n'
    open(f'{OUT}/{name}.svg', 'w', encoding='utf-8').write(out)

build('learning-bars-4', ['SQL', 'Python', 'Excel', 'AI tools'], 'Learning path: SQL, Python, Excel, AI tools')
build('learning-bars-3', ['Python', 'Excel', 'AI tools'], 'Learning path: Python, Excel, AI tools')
print('ok')
