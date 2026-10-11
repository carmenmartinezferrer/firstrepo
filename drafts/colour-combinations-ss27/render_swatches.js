const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const dir = process.argv[2], dest = process.argv[3];
  const names = JSON.parse(fs.readFileSync(dir + '/swatches.json'));
  const b = await chromium.launch();
  const pg = await b.newPage({ viewport: { width: 1600, height: 1200 }, deviceScaleFactor: 2 });
  for (const n of names) {
    await pg.goto('file://' + dir + '/' + n + '.html');
    await pg.evaluate(() => document.fonts.ready);
    await pg.waitForTimeout(500);
    await (await pg.$('#chart')).screenshot({ path: dest + '/' + n + '.png' });
  }
  await b.close();
})();
