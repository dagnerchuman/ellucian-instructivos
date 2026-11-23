// Exporta PNG claro/oscuro y SVG de un diagrama Archify con Chrome por CDP (sin Playwright).
// Uso: node exportar-cdp.mjs <url-http-del-html> <base-de-salida>
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

const [url, base] = process.argv.slice(2);
const chrome = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const perfil = fs.mkdtempSync(path.join(os.tmpdir(), 'cdp-'));
const port = 9333;
const proc = spawn(chrome, ['--headless=new', `--remote-debugging-port=${port}`, `--user-data-dir=${perfil}`, '--window-size=1600,1000', 'about:blank'], { stdio: 'ignore' });
const espera = (ms) => new Promise((r) => setTimeout(r, ms));

let ws;
for (let i = 0; i < 50; i++) {
  try {
    const t = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json();
    const p = t.find((x) => x.type === 'page');
    if (p) { ws = new WebSocket(p.webSocketDebuggerUrl); break; }
  } catch (_) {}
  await espera(200);
}
await new Promise((r) => ws.addEventListener('open', r));
let id = 0; const pend = new Map();
ws.addEventListener('message', (e) => { const m = JSON.parse(e.data); if (m.id && pend.has(m.id)) { pend.get(m.id)(m); pend.delete(m.id); } });
const cdp = (method, params = {}) => new Promise((r) => { const i = ++id; pend.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });
const evalu = async (expr) => { const r = await cdp('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true }); if (r.result.exceptionDetails) throw new Error(JSON.stringify(r.result.exceptionDetails)); return r.result.result.value; };

const capturar = `
  window.__salida = null;
  const orig = HTMLAnchorElement.prototype.click;
  HTMLAnchorElement.prototype.click = function () {
    if (this.download) { fetch(this.href).then(r => r.blob()).then(b => new Promise(res => { const fr = new FileReader(); fr.onload = () => res(fr.result); fr.readAsDataURL(b); })).then(d => { window.__salida = d; }); return; }
    return orig.call(this);
  };`;

async function exportar(tema, formato, destino) {
  await cdp('Page.navigate', { url: `${url}?theme=${tema}` });
  for (let i = 0; i < 100; i++) { await espera(200); if (await evalu(`!!(window.Archify && window.Archify.exportMenu && document.querySelector('.diagram-container svg'))`)) break; }
  await evalu(`(async () => { if (typeof window.Archify.waitForStableLayout === 'function') await window.Archify.waitForStableLayout(); return 1; })()`);
  await evalu(capturar);
  await evalu(`(window.Archify.exportMenu.run(${JSON.stringify(formato)}), 1)`);
  let d = null;
  for (let i = 0; i < 300 && !d; i++) { await espera(200); d = await evalu('window.__salida'); }
  if (!d) throw new Error(`sin descarga ${formato} ${tema}`);
  fs.writeFileSync(destino, Buffer.from(d.split(',')[1], 'base64'));
  console.log(destino, Math.round(fs.statSync(destino).size / 1024), 'KB');
}

await cdp('Page.enable'); await cdp('Runtime.enable');
try {
  await exportar('light', 'png', `${base}-claro.png`);
  await exportar('light', 'svg', `${base}.svg`);
  await exportar('dark', 'png', `${base}-oscuro.png`);
} finally { ws.close(); proc.kill(); }
