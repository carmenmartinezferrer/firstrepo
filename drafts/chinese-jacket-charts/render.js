const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const dir = path.join(__dirname, 'html');
  const b = await chromium.launch();
  const pg = await b.newPage({ viewport: { width: 1000, height: 800 }, deviceScaleFactor: 2 });
  for (const n of JSON.parse(fs.readFileSync(path.join(dir, 'manifest.json')))) {
    await pg.goto('file://' + path.join(dir, n + '.html'));
    await pg.evaluate(() => document.fonts.ready);
    await pg.waitForTimeout(300);
    await (await pg.$('.block')).screenshot({ path: path.join(__dirname, n + '.png') });
  }
  await b.close();
})();
