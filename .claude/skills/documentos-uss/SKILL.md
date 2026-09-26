---
name: documentos-uss
description: Cómo producir los entregables del proyecto Centros Empresariales USS (PDF, presentaciones PPTX, diagramas y planillas Excel) con el formato y el estilo que pide el usuario Dagner Anibal Chuman Lluen. Úsala siempre que pida un PDF, un resumen, una presentación o diapositivas, un diagrama, una tabla o una planilla sobre Banner o los centros, o cuando diga «hazme el PDF», «pásame el ppt» o «resumen».
---

# Entregables con formato USS

## Lo que el usuario pide (preferencias aprendidas)
- **Idioma:** español, sencillo y directo. El usuario escribe informal y con apuro; entiende lo que quiere decir.
- **«Mientras más resumido, mejor»** y **«poco a poco»**: un tema por entrega.
- **Pocas tablas** («me pones varias tablas que me pierdo»). Prefiere:
  - tarjetas por tema;
  - flujos con flechas;
  - **ejemplos concretos por centro**: Inglés, Informática y Emprendimiento, **los tres siempre**; una vez se olvidó uno y hubo que agregarlo.
  - Tablas, solo pequeñas o de referencia.
- **Estructura fija** de cada tema:
  - «**Hoy en SEUSS**»: lo que se hace ahora, según el usuario.
  - «**En Ellucian**»: lo que dicen los instructivos, con cita.
  - Ejemplos y un «Resultado».
- **Todas las dudas al final**, separadas en «Para Ellucian» y «Para la USS».
- **Siglas y códigos siempre con su significado entre paréntesis.** Ejemplo: «NRC (Número de Referencia de Curso)», «SSASECT (Programar NRC)». Lo pidió el 26/09/2026.
  - `explicar(html)` de `common.py` lo hace solo en cada tarjeta, la primera vez que aparece el término; SEUSS, solo una vez en todo el documento.
  - `glosario_html()` arma el glosario, que va antes de las dudas.
  - Si usas un término nuevo, agrégalo a `SIGLAS` o `PAGINAS`.
- **«Hoy en SEUSS» es lo que el usuario dice que se hace hoy; no lo interpretes.** Ejemplo del 26/09: en SEUSS, quien desaprueba BASIC I **no** pasa a BASIC II (salvo con examen de suficiencia). Se había escrito «¿pasa automático?», y el usuario lo corrigió.
- **Autor:** «Elaborado por: Dagner Anibal Chuman Lluen», en la portada y en el pie. También en los metadatos del PDF.
- **Formato USS:**
  - morado **#7030A0** (oscuro #5C2193); verdes **#4EA72E** y **#92D050**;
  - logos de la USS y de Ellucian;
  - para las presentaciones, la plantilla «Ppt USS 2026».
  - Color por centro: Inglés **#7030A0**, Informática **#0E8A5F** (en gráficos #1BAF7A), Emprendimiento **#C2501C** (en gráficos #EB6834).
- **PDF por defecto.** Presentaciones solo si las pide. Mientras «te estoy alimentando» con información, **no generes diapositivas**.
  - El PPTX **debe abrir sin «reparar»** en PowerPoint.
- **Datos inventados:** márcalos siempre «de ejemplo». Nunca los presentes como datos de la USS.
- **Nombre de archivo en MAYÚSCULAS:** `TEMA - SUBTEMA - CENTROS EMPRESARIALES.pdf`. Entrégalo con SendUserFile para que lo vea en el panel.
- **Antes de escribir,** carga las skills `arquitectura-centros-empresariales` (datos) y `preguntas-y-dudas-centros` (qué está confirmado y qué no).

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

## Presentaciones PPTX
En `scripts/pptx/`:
- **`ussdeck.py`:** arma la estructura desde la plantilla.
  - `build_structure`, `build_cover`, `build_div`, `set_flow_boxes`, `finalize`, `to_pdf`.
  - Diapositivas base: portada = slide1, flujo = slide5, texto = slide3, divisor = slide6, configuración = slide7, cierre = slide23.
- **`pptlib.py`:** piezas nativas y editables.
  - Texto enriquecido; tablas nativas `a:tbl` con tamaño de letra automático (`fit_sz`).
  - Tarjetas, chevrones y conectores (polilínea `custGeom` con flecha).
  - Clase `Slide`.

**Requisitos:**
- **La plantilla del usuario no está en el repositorio.** Pídela o usa `USS_PPT_TEMPLATE`.
- Los scripts de la skill `pptx`, que se detectan solos.

**Geometría de la plantilla:**
- Título en y 0,24 M EMU.
- Área útil de y 0,9 M a 5,85 M.
- Logo USS abajo a la izquierda (y 6,15 M) y logo Ellucian abajo a la derecha (x 10,2 M).

**Para que abra sin «reparar»,** `finalize()` ya hace lo siguiente:
- limpia con `clean.py`;
- quita `xml:space`;
- da `creationId` únicos;
- escribe `[Content_Types].xml` primero en el zip;
- no incluye entradas de carpeta;
- reemplaza el pie «Elaborado por: …» por el autor.

**Después de generar:**
- Valida con `validate.py` de la skill pptx.
- Convierte a PDF (`to_pdf`) y revisa los PNG.
- Avisa al usuario de que no se pudo abrir en PowerPoint real.

## Excel
- Genera con `openpyxl` y fórmulas reales: COUNTIFS, fechas con TODAY.
- Las listas desplegables van en una hoja oculta «Listas».
- Recalcula con LibreOffice: `recalc.py` de la skill xlsx. Si falta, instala con `apt-get install -y libreoffice-calc`.
- Verifica que haya **0 errores** de fórmula.
- **No** mates `soffice` con `pkill -f soffice`: mata también la shell.

## Entregables hechos hasta ahora
Lista, estructura y qué supuestos usa cada uno: [references/entregables.md](references/entregables.md). Si un supuesto cambia (ver el registro de dudas), ofrece corregir los entregables afectados.
