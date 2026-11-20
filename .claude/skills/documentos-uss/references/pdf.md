# PDF: HTML impreso con Chromium

Parte de la skill `documentos-uss` (el mapa está en su `SKILL.md`).

## PDF: HTML impreso con Chromium
Todo está en `scripts/pdf/`:

| Archivo | Qué hace |
|---|---|
| `common.py` | `header()` (portada), `section()`, `table()`, `fmt()`, `chips()`, `explicar()` y `glosario_html()` (significado de siglas y páginas), `render()` (HTML → PDF + metadatos), `check_pdf()` (control de calidad) |
| `base.css` | Estilos base (variables de color, portada, secciones, tablas) |
| `render.js` | Playwright/Chromium; A4 (o `A3-horizontal` para diagramas); pie con título, autor y página |
| `fonts/` | InterStatic (Inter estático 400/500/600/700) y Montserrat (400/700), licencia OFL. Se cargan con @font-face y no hace falta instalarlas |
| `img/` | Logos USS y Ellucian |
| `ejemplo_centros.py` | **Ejemplo completo** del estilo preferido: tarjetas SEUSS/Ellucian, ejemplos por centro, cálculo de notas, flujos y dudas al final. Cópialo como punto de partida |

```bash
cd .claude/skills/documentos-uss/scripts/pdf
python3 ejemplo_centros.py /ruta/salida.pdf     # genera el ejemplo y corre check_pdf()
```
Para un documento nuevo, copia `ejemplo_centros.py` a tu carpeta de trabajo, fuera del repositorio. Agrega `scripts/pdf` a `sys.path` para importar `common`, y cambia los datos y el CSS extra.

Requisitos: `node` con `playwright` (Chromium en /opt/pw-browsers) y `pymupdf` (`pip install pymupdf` si falta).

**En la Mac del usuario** (30/10/2026) no hay ninguno de los dos. Sin tocar el sistema, en una carpeta de trabajo:
```bash
npm install playwright-core                                   # en la carpeta de trabajo
PLAYWRIGHT_BROWSERS_PATH=$PWD/browsers node node_modules/playwright-core/cli.js install chromium
python3 -m venv venv && venv/bin/pip install pymupdf
PLAYWRIGHT_BROWSERS_PATH=<carpeta>/browsers NODE_PATH=<carpeta>/node_modules <carpeta>/venv/bin/python generador.py
```
`render.js` acepta `playwright-core` y, si no hay Chromium, usa el Google Chrome instalado; pero con Chrome el **pie sale en Times** (no carga la fuente incrustada) y `check_pdf` lo marca: usa el Chromium de Playwright.

### Control de calidad (siempre, antes de entregar)
1. `check_pdf(ruta, png_dir=...)`:
   - Revisa las páginas y el autor.
   - Avisa si algún texto salió con otra fuente: significa que Inter no tiene ese glifo.
   - Genera un PNG por página.
2. **Mira los PNG** con Read. Busca:
   - títulos huérfanos al pie de página: usa `<div class="keep">` para mantenerlos juntos;
   - tarjetas cortadas;
   - textos desbordados;
   - páginas casi vacías.
3. **Glifos que Inter NO tiene:** → ① ② ✓ ✗ ≥ ▲.
   - Usa texto, «›», el SVG `ARROW` del ejemplo o formas CSS.
   - Sí funcionan: « » – — · × ÷ ›.
4. **En grids de CSS,** envuelve el texto mixto en `<div>`. Si no, cada `<b>` se vuelve una celda aparte.
5. **Nombres de clase CSS:** no reutilices los de `base.css` con otro significado. Ya pasó dos veces:
   - `.st` chocó y se renombró a `.stp`;
   - `.sub` volvió oscuro el subtítulo de la portada y se renombró a `.subn`.
