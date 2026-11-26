// Builds the "typing SQL on a laptop" video from the laptop illustration.
// Usage: node make_typing_video.js <frames_dir> <out_dir>
// Needs: playwright (Chromium) and ffmpeg.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const [, , framesDir, outDir] = process.argv;
fs.mkdirSync(framesDir, { recursive: true });
fs.mkdirSync(outDir, { recursive: true });

const FPS = 30;
const LINES = ["SELECT brand, colour", "FROM runway_looks", "WHERE season = 'SS27';"];
const KW = [6, 4, 5]; // number of keyword characters per line (shown in pink)
const CHAR_W = 20.4; // JetBrains Mono at 34px is 0.6em wide
const X0 = 262;
const BASE = [275, 325, 375];

// Timeline: when each character appears (seconds)
const events = []; // {t, n}
let t = 0.6; // idle cursor before typing starts
let n = 0;
const lineEnds = [];
for (let li = 0; li < LINES.length; li++) {
  for (let ci = 0; ci < LINES[li].length; ci++) {
    t += 0.05 + 0.04 * (((n * 37) % 7) / 6); // 0.05 to 0.09 seconds per key, uneven like a real typist
    n += 1;
    events.push({ t, n });
  }
  lineEnds.push(n);
  t += 0.4; // pause at the end of each line
}
const total = LINES.reduce((a, l) => a + l.length, 0);
const duration = t + 2.0; // hold the finished query
const frames = Math.ceil(duration * FPS);

function stateAt(time) {
  let typed = 0;
  let last = 0;
  for (const e of events) {
    if (e.t <= time) { typed = e.n; last = e.t; }
  }
  const idle = time - last;
  const typing = typed > 0 && typed < total && idle < 0.25;
  const cursorOn = typing ? true : Math.floor(time / 0.5) % 2 === 0;
  return { typed, cursorOn };
}

function layout(typed) {
  // split the typed count over the lines, and find the cursor line
  let remaining = typed;
  const parts = [];
  for (let li = 0; li < LINES.length; li++) {
    const take = Math.min(remaining, LINES[li].length);
    parts.push(LINES[li].slice(0, take));
    remaining -= take;
  }
  // the cursor sits on the first line that is not finished (it jumps to the next line when a line ends)
  let cursorLine = LINES.findIndex((l, i) => parts[i].length < l.length);
  if (cursorLine === -1) cursorLine = LINES.length - 1;
  return { parts, cursorLine };
}

const html = `<html><body style="margin:0;background:transparent">
<svg id="s" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 820 400" width="820" height="400">
  <g transform="translate(-130,-170)">
    <rect x="210" y="190" width="660" height="330" rx="24" fill="#111111"/>
    <rect x="232" y="212" width="616" height="286" rx="10" fill="#1E1E1E"/>
    <g font-family="'JetBrains Mono', 'DejaVu Sans Mono', monospace" font-size="34" style="white-space:pre">
      <text x="262" y="275"><tspan id="k0" fill="#D6447A" font-weight="700"></tspan><tspan id="r0" fill="#FFFFFF"></tspan></text>
      <text x="262" y="325"><tspan id="k1" fill="#D6447A" font-weight="700"></tspan><tspan id="r1" fill="#FFFFFF"></tspan></text>
      <text x="262" y="375"><tspan id="k2" fill="#D6447A" font-weight="700"></tspan><tspan id="r2" fill="#FFFFFF"></tspan></text>
    </g>
    <rect id="cur" x="262" y="247" width="16" height="34" fill="#D6447A"/>
    <rect x="150" y="520" width="780" height="26" rx="13" fill="#BDBDBD"/>
  </g>
</svg></body></html>`;

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 820, height: 400 }, deviceScaleFactor: 2 });
  await page.setContent(html);
  const cache = new Map();
  for (let f = 0; f < frames; f++) {
    const { typed, cursorOn } = stateAt(f / FPS);
    const key = `${typed}-${cursorOn ? 1 : 0}`;
    const file = path.join(framesDir, `f_${String(f + 1).padStart(4, '0')}.png`);
    if (!cache.has(key)) {
      const { parts, cursorLine } = layout(typed);
      const cx = X0 + parts[cursorLine].length * CHAR_W;
      const cy = BASE[cursorLine] - 28;
      await page.evaluate(({ parts, KW, cx, cy, cursorOn }) => {
        parts.forEach((p, i) => {
          document.getElementById('k' + i).textContent = p.slice(0, KW[i]);
          document.getElementById('r' + i).textContent = p.slice(KW[i]);
        });
        const c = document.getElementById('cur');
        c.setAttribute('x', cx);
        c.setAttribute('y', cy);
        c.setAttribute('opacity', cursorOn ? '1' : '0');
      }, { parts, KW, cx, cy, cursorOn });
      await page.screenshot({ path: file, omitBackground: true, clip: { x: 0, y: 0, width: 820, height: 400 } });
      cache.set(key, file);
    } else {
      try { fs.unlinkSync(file); } catch (e) {}
      fs.linkSync(cache.get(key), file);
    }
  }
  await browser.close();

  const mp4 = path.join(outDir, 'laptop-typing.mp4');
  const webm = path.join(outDir, 'laptop-typing-transparent.webm');
  execSync(`ffmpeg -y -loglevel error -framerate ${FPS} -i ${framesDir}/f_%04d.png -f lavfi -i color=white:s=1640x800:r=${FPS} -filter_complex "[1][0]overlay=shortest=1,format=yuv420p" -c:v libx264 -crf 16 -movflags +faststart ${mp4}`);
  execSync(`ffmpeg -y -loglevel error -framerate ${FPS} -i ${framesDir}/f_%04d.png -c:v libvpx-vp9 -pix_fmt yuva420p -b:v 0 -crf 30 -auto-alt-ref 0 ${webm}`);
  console.log('frames', frames, 'seconds', duration.toFixed(1));
})();
