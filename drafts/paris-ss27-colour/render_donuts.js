const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const dir = process.argv[2], dest = process.argv[3];
  const m = JSON.parse(fs.readFileSync(dir + '/manifest.json'));
  const b = await chromium.launch();
  const pg = await b.newPage({ viewport: { width: 814, height: 814 }, deviceScaleFactor: 2 });
  for (const c of m) {
    await pg.goto('file://' + dir + '/' + c.name + '.html');
    await pg.evaluate(() => document.fonts.ready);
    await pg.waitForTimeout(300);
    await (await pg.$('svg')).screenshot({ path: dest + '/' + c.name + '.png', omitBackground: true });
  }
  await b.close();
})();
