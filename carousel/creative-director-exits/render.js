// node render.js <html_dir> <png_dir>  : screenshots every .html at 1080x1350
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
(async () => {
  const [src, out] = process.argv.slice(2); fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
  for (const f of fs.readdirSync(src).filter(f => f.endsWith('.html')).sort()) {
    await p.goto('file://' + path.resolve(src, f)); await p.evaluate(() => document.fonts.ready);
    await p.screenshot({ path: path.join(out, f.replace('.html', '.png')) }); console.log('wrote', f);
  }
  await b.close();
})();
