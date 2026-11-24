// Banco de preguntas del asistente: ¿cada pregunta recupera la fuente que la responde?
// Uso: node herramientas/diagramas/probar_asistente.mjs [--fallas] [--solo categoria]
// Corre la misma búsqueda local de asistente_ia.js (recuperarEvidencia) sobre asistente_conocimiento.js.
import { readFileSync, readdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import vm from 'node:vm';

const AQUI = dirname(fileURLToPath(import.meta.url));
const RAIZ = join(AQUI, '..', '..');
const args = process.argv.slice(2);
const verFallas = args.includes('--fallas');
const solo = args.includes('--solo') ? args[args.indexOf('--solo') + 1] : null;

// 1. La búsqueda del asistente, tal cual está en el asset (de normalizar() a recuperarEvidencia()).
const ctx = { window: {}, console };
vm.createContext(ctx);
vm.runInContext(readFileSync(join(AQUI, 'assets/asistente_conocimiento.js'), 'utf8'), ctx);
const src = readFileSync(join(AQUI, 'assets/asistente_ia.js'), 'utf8');
const desde = src.indexOf('    function normalizar(');
const hasta = src.indexOf('    // Contexto de la conversación');
if (desde < 0 || hasta < 0) throw new Error('No se encontró la búsqueda en asistente_ia.js');
vm.runInContext(src.slice(desde, src.lastIndexOf('    // ----', hasta)) +
  '\nthis.recuperar = recuperarEvidencia; this.normalizar = normalizar;', ctx);
const base = ctx.window.CCEE_KNOWLEDGE;

// 2. Las preguntas: las escritas a mano y las que se arman solas.
const preguntas = JSON.parse(readFileSync(join(AQUI, 'preguntas_prueba.json'), 'utf8')).preguntas
  .map((p) => ({ ...p, cat: 'coloquiales' }));

const REFS = join(RAIZ, '.claude/skills/arquitectura-centros-empresariales/references');
for (const archivo of readdirSync(REFS).filter((a) => a.startsWith('ref-preguntas-'))) {
  const texto = readFileSync(join(REFS, archivo), 'utf8');
  for (const m of texto.matchAll(/^###\s+(.+)$/gm)) {
    preguntas.push({ q: m[1], espera: [archivo], top: 1, cat: 'frecuentes (título exacto)' });
    // Como la escribe la gente: sin tildes, signos ni mayúsculas.
    const suelta = ctx.normalizar(m[1]).replace(/[¿?¡!«»()]/g, '').replace(/\s+/g, ' ').trim();
    preguntas.push({ q: suelta, espera: [archivo], top: 1, cat: 'frecuentes (sin tildes)' });
  }
}

// Instructivos: por su nombre completo del catálogo («como registrar la oferta horaria de los cursos») y por su código
// («que dice el instructivo 8.1»). Varios comparten código (5.3, 5.4, 8.1, 10.2): vale cualquiera de ellos.
const catalogo = ctx.window.CCEE_INSTRUCTIVOS || [];
const rutaDe = Object.fromEntries(base.filter((f) => f.instructivo).map((f) => [f.instructivo, f.fuente]));
for (const c of catalogo) {
  preguntas.push({ q: 'como ' + ctx.normalizar(c.nombre), espera: [rutaDe[c.id]], top: 3, cat: 'instructivos (por tema)' });
}
for (const codigo of [...new Set(catalogo.map((c) => c.codigo))]) {
  const mismos = catalogo.filter((c) => c.codigo === codigo).map((c) => rutaDe[c.id]);
  preguntas.push({ q: 'que dice el instructivo ' + codigo, espera: mismos, top: 2, cat: 'instructivos (por número)' });
}

// Páginas de Banner que salen como título de pantalla en los instructivos: «para qué sirve SCASYLB».
const codigos = new Set();
base.filter((f) => f.fuente.endsWith('.pptx')).forEach((f) => {
  const t = (f.texto.match(/^## (.+)$/m) || [])[1] || '';
  (t.match(/\b[GSTF][A-Z]{5,7}\b/g) || []).forEach((c) => codigos.add(c));
});
for (const c of codigos) preguntas.push({ q: 'para que sirve ' + c, codigo: c, top: 1, cat: 'páginas de Banner' });

// 3. Correr y medir.
const porCat = {};
const fallas = [];
for (const p of preguntas) {
  if (solo && !p.cat.startsWith(solo)) continue;
  const r = ctx.recuperar(p.q);
  const tope = r.slice(0, p.top || 1);
  const ok = p.vacio ? r.length === 0 : p.codigo
    ? tope.some((f) => f.texto.includes(p.codigo))
    // «archivo#texto»: además del archivo, el fragmento debe traer ese texto (una pregunta frecuente concreta).
    // Con «todas», cada fuente esperada debe salir (una pregunta con dos temas: «textos o cartas»).
    : p.espera[p.todas ? 'every' : 'some']((e) => tope.some((f) => { const [archivo, trozo] = e.split('#');
      return f.fuente.includes(archivo) && (!trozo || ctx.normalizar(f.texto).includes(trozo)); }));
  const c = (porCat[p.cat] ||= { ok: 0, total: 0 });
  c.total++;
  if (ok) c.ok++;
  else fallas.push({ cat: p.cat, q: p.q, espera: p.vacio ? '(sin evidencia)' : p.codigo || p.espera.join(' | '), obtuvo: r.map((f) => f.fuente.split('/').pop()).join(' · ') || '(nada)' });
}
let ok = 0, total = 0;
for (const [cat, c] of Object.entries(porCat)) {
  ok += c.ok; total += c.total;
  console.log(`${String(Math.round((100 * c.ok) / c.total)).padStart(3)} %  ${String(c.ok).padStart(4)}/${String(c.total).padEnd(4)} ${cat}`);
}
console.log(`${String(Math.round((100 * ok) / total)).padStart(3)} %  ${String(ok).padStart(4)}/${String(total).padEnd(4)} TOTAL`);
if (verFallas) for (const f of fallas) console.log(`\n✗ [${f.cat}] ${f.q}\n   espera: ${f.espera}\n   obtuvo: ${f.obtuvo}`);
