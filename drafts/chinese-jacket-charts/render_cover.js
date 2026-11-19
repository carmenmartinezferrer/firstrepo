const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1456, height: 1048 }, deviceScaleFactor: 2 });
  await p.goto('file://' + path.join(__dirname, 'html', '00-cover.html'));
  await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(600);
  await (await p.$('#card')).screenshot({ path: path.join(__dirname, '00-cover.png') });
  await b.close();
})();
