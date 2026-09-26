// Imprime un HTML a PDF con Chromium: A4, pie con título, autor y numeración.
// Uso: node render.js entrada.html salida.pdf "Título del pie" [A4|A3-horizontal]
const path = require('path');
const { execSync } = require('child_process');

function loadPlaywright() {
  try { return require('playwright'); } catch (e) { /* sigue */ }
  const roots = [];
  try { roots.push(execSync('npm root -g').toString().trim()); } catch (e) { /* sigue */ }
  roots.push('/opt/node22/lib/node_modules', '/usr/local/lib/node_modules', '/usr/lib/node_modules');
  for (const r of roots) {
    try { return require(path.join(r, 'playwright')); } catch (e) { /* sigue */ }
  }
  throw new Error('No se encontró playwright. Instálalo con: npm i -g playwright (Chromium ya viene en /opt/pw-browsers).');
}

const fs = require('fs');
const { chromium } = loadPlaywright();
const [, , htmlFile, pdfFile, title = '', size = 'A4'] = process.argv;

// El pie se dibuja aparte y no ve las fuentes de la página: se incrustan en base64.
const face = (w, f) => `@font-face{font-family:InterStatic;font-weight:${w};src:url(data:font/ttf;base64,${
  fs.readFileSync(path.join(__dirname, 'fonts', f)).toString('base64')})}`;
const footer = `<style>${face(400, 'InterStatic-Regular.ttf')}${face(700, 'InterStatic-Bold.ttf')}</style>
<div style="width:100%;padding:0 13mm;font-family:InterStatic,sans-serif;font-size:6.8pt;color:#6B6B76;
            display:flex;justify-content:space-between;align-items:center;-webkit-print-color-adjust:exact;">
  <span>${title}</span>
  <span>Elaborado por: <b style="color:#5C2193">Dagner Anibal Chuman Lluen</b></span>
  <span>Página <span class="pageNumber"></span> de <span class="totalPages"></span></span>
</div>`;

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + path.resolve(htmlFile), { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  const fmt = size === 'A3-horizontal' ? { format: 'A3', landscape: true } : { format: 'A4' };
  await page.pdf({
    path: pdfFile, ...fmt, printBackground: true,
    margin: { top: '12mm', bottom: '15mm', left: '13mm', right: '13mm' },
    displayHeaderFooter: true, headerTemplate: '<div></div>', footerTemplate: footer,
  });
  await browser.close();
})();
