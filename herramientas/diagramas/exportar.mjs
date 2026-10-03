// Exporta cada diagrama Archify a imágenes, usando el mismo menú «Export» del HTML:
//   <nombre>-claro.png y <nombre>-oscuro.png (PNG nítido del diagrama completo)
//   <nombre>.svg (vectorial, cambia solo entre claro y oscuro)
//
// Uso: node herramientas/diagramas/exportar.mjs ruta/al/diagrama.html [...]
// Requiere Playwright con Chromium (PLAYWRIGHT_BROWSERS_PATH o el Chromium del sistema).
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import path from 'node:path';
import fs from 'node:fs';
import { pathToFileURL } from 'node:url';

function cargarPlaywright() {
  const require = createRequire(import.meta.url);
  try { return require('playwright'); } catch (_) { /* sigue con la instalación global */ }
  const global = execSync('npm root -g').toString().trim();
  return require(path.join(global, 'playwright'));
}

const { chromium } = cargarPlaywright();
const archivos = process.argv.slice(2);
if (!archivos.length) {
  console.error('Uso: node exportar.mjs diagrama.html [...]');
  process.exit(2);
}

async function exportar(page, html, formato, destino) {
  const [descarga] = await Promise.all([
    page.waitForEvent('download', { timeout: 60000 }),
    page.evaluate((f) => window.Archify.exportMenu.run(f), formato),
  ]);
  await descarga.saveAs(destino);
}

async function abrir(browser, html, tema) {
  const page = await browser.newPage({ viewport: { width: 1600, height: 1000 }, acceptDownloads: true });
  await page.goto(`${pathToFileURL(path.resolve(html)).href}?theme=${tema}`);
  await page.waitForFunction(() => window.Archify && window.Archify.exportMenu && document.querySelector('.diagram-container svg'));
  if (await page.evaluate(() => typeof window.Archify.waitForStableLayout === 'function')) {
    await page.evaluate(() => window.Archify.waitForStableLayout());
  }
  return page;
}

const browser = await chromium.launch();
let fallas = 0;
for (const html of archivos) {
  const base = html.replace(/\.html$/i, '');
  try {
    for (const [tema, sufijo] of [['light', 'claro'], ['dark', 'oscuro']]) {
      const page = await abrir(browser, html, tema);
      await exportar(page, html, 'png', `${base}-${sufijo}.png`);
      if (tema === 'light') await exportar(page, html, 'svg', `${base}.svg`);
      await page.close();
    }
    const kb = (f) => Math.round(fs.statSync(f).size / 1024);
    console.log(`IMÁGENES  ${path.basename(base)}  claro ${kb(`${base}-claro.png`)} KB · oscuro ${kb(`${base}-oscuro.png`)} KB · svg ${kb(`${base}.svg`)} KB`);
  } catch (err) {
    fallas += 1;
    console.error(`FALLA  ${html}: ${err.message}`);
  }
}
await browser.close();
process.exit(fallas ? 1 : 0);
