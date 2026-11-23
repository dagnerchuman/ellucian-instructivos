# Word de preguntas, Excel y diagramas

Parte de la skill `documentos-uss` (el mapa está en su `SKILL.md`).

## Word de preguntas (para responder y devolver)
- Cuando pida las preguntas para una reunión en Word: `fuentes/preguntas/build_preguntas.py` arma un `.docx` con un título por pregunta (su código E## o U##), «Lo que ya sabemos» y un recuadro «Respuesta». Los textos salen del registro; solo se eligen y ordenan los bloques.
- Va en `docs/dudas/` con nombre en mayúsculas. Revisa el PDF que sale de LibreOffice y valida con `validate.py` de la skill docx.
- Cuando lo devuelva respondido: `fuentes/preguntas/leer_respuestas.py` lista las respuestas por código; pásalas al registro (skill `preguntas-y-dudas-centros`).
- **Corregir un dato en un Word ya entregado** (el de una reunión con fecha): no lo regeneres. El generador toma los textos del registro de hoy y cambia las preguntas que se resolvieron después. Corrige el generador y aplica al `.docx` solo esas líneas (los `<w:t>` del párrafo y la fila del glosario); compara el texto antes y después con `textutil -convert txt` (C236).

## Excel
- Genera con `openpyxl` y fórmulas reales: COUNTIFS, fechas con TODAY.
- Las listas desplegables van en una hoja oculta «Listas».
- Recalcula con LibreOffice: `recalc.py` de la skill xlsx. Si falta, instala con `apt-get install -y libreoffice-calc`.
- Verifica que haya **0 errores** de fórmula.
- **No** mates `soffice` con `pkill -f soffice`: mata también la shell.

## Diagramas interactivos paso a paso (Archify)
- Cuando el usuario pida un diagrama, un flujo o un mapa de estados, primero revisa los que ya existen en `centros/<centro>/diagramas/`. Hay 7 por centro y un comparativo; el índice está en `centros/README.md`.
- Se entregan en **HTML interactivo** (claro y oscuro, animación, vistas guiadas, menú «Exportar»), **PNG claro**, **PNG oscuro** y **SVG**. Para un PDF o una presentación, usa el PNG claro.
- **No se editan a mano.** Se cambia `centros/<centro>/datos.json` o `herramientas/diagramas/plantillas.py` y se regenera; el detalle está en la skill `workflow-diagramas-archify`.
- El diagrama A3 en PDF (`fuentes/diag/build_diagrama.py`) es la versión anterior, común a los tres centros. Para trabajar por centro, usa los de Archify.
