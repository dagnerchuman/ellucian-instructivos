# Archify: regenerar y reglas para no romper la validación

Parte de la skill `workflow-diagramas-archify` (el mapa está en su `SKILL.md`).

## Regenerar
```bash
bash herramientas/diagramas/instalar_archify.sh            # una vez por máquina o sesión
python3 herramientas/diagramas/generar.py                  # solo lo que cambió (JSON + HTML + índices, sin imágenes)
python3 herramientas/diagramas/generar.py idiomas --solo 4 # un diagrama de un centro
python3 herramientas/diagramas/generar.py --forzar         # todo de nuevo: Archify compila las 87 páginas (varios minutos)
python3 herramientas/diagramas/generar.py --con-imagenes   # opcional: PNG y SVG de las páginas que cambiaron o no los tienen (lento)
```
- **Solo rehace la hoja que cambió (C234).** Pasada 1: Archify compila un diagrama solo si cambió su especificación (sale de `datos.json` y `plantillas.py`), si falta su HTML o si cambió el motor Archify. Pasada 2: la inyección (guía, navegación, asistente) se salta la página si no cambió nada de lo que lleva dentro (los `*.py` del generador, los assets incrustados, los `datos.json`, el catálogo de diapositivas, la lista de páginas y las capturas de TEST) y no reescribe un archivo que queda igual. La última línea dice cuántas páginas compiló Archify, cuántas se escribieron y cuántas quedaron sin cambios.
- **Tiempos (23/11/2026):** sin cambios, 1 a 2 s y ningún archivo escrito; un valor de un `datos.json`, unos 15 s (una página); solo el asistente, ninguna página. Antes, cada corrida tardaba de 4 a 10 minutos.
- **Memoria local en `herramientas/.cache/`** (en `.gitignore`, no se sube): `paginas.json` (firma y hash de cada página) y `pptx/` (textos y cajas de cada instructivo; se releen solo si cambia el PPTX o el código que lo lee). Si una página parece vieja, usa `--forzar` o borra esa carpeta.
- Si Archify falla en una página, su especificación y su HTML anteriores quedan como estaban, y la próxima corrida lo vuelve a intentar.
- Cada diagrama pasa por `archify finalize` con calidad *showcase*: esquema, geometría, legibilidad, revisión estricta y prueba en Chromium.
- Si falla, `generar.py` imprime el diagnóstico y el arreglo sugerido. Corrige la plantilla, no el HTML.
- En Windows (Antigravity) funciona igual con `python` y `node`. Para la prueba en navegador, define `ARCHIFY_CHROME` con la ruta de Chrome. En la nube de Claude Code: `ARCHIFY_CHROME=/opt/pw-browsers/chromium-*/chrome-linux64/chrome`; sin esa variable, `finalize` falla y deja HTML incompletos (no los subas: `git checkout -- centros/*/diagramas`).
- Si cambia la numeración (se agrega, quita o reordena una casuística), regenera **con imágenes**: las carpetas nuevas no traen PNG ni SVG y la galería las muestra vacías.
- **Requisito Playwright para `--con-imagenes`** (C176): en la Mac del usuario no está instalado. Se instala fuera del repositorio (`PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 npm install playwright` en el scratchpad) y se exporta con `NODE_PATH=<carpeta>/node_modules node herramientas/diagramas/exportar.mjs <html>`; usa el Google Chrome del sistema.
- **Archify acepta columnas 0 a 5** (`col` y `toCol` ≤ 5, C176): con más pasos, dos o tres comparten columna en carriles distintos. En la Demostración 1, SFAREGS, Autoservicio y SHRROLL van en la columna 5 y la fase «Matricular, dictar y cerrar» empieza en la columna de SFAREGS.
- **`mainPath` no puede volver a una columna anterior** (C192): un flujo en renglones (una fila por fase, cada una desde la columna 0) va sin `mainPath` (`flujo(..., camino_principal=False)`) y la flecha que baja de una fila a la siguiente lleva `fromSide: bottom` y `toSide: top`; si no, Archify da «moves backward» y «ambiguous-corridor». Así está el flujo de la prueba del NRC 10045.
- **Requisito `python-pptx`** (`pip install python-pptx`): sin él, `generar.py` deja **vacías las líneas de las láminas** en las guías de los diagramas, sin avisar (`texto_diapositiva` devuelve `[]`). En la Mac del usuario faltaba (30/10/2026, C171); revisa el diff de `GUIA_MAP` antes de subir. Si además cambian las WebP de `visor_instructivos/diapositivas` sin haber tocado los instructivos, son recodificaciones: `git checkout -- visor_instructivos`.
- **El asistente se carga como archivo (C234):** cada página y la galería enlazan `assets/asistente_ia.css` y `asistente_ia.js`, igual que la base (`asistente_conocimiento.js` y `asistente_diapositivas.js`). Si solo cambia el asistente, no se regenera ninguna página: basta recargar. Si cambió una skill o un instructivo, `generar.py` rehace la base (o solo `generar_conocimiento_asistente.py`). Ya no hace falta el reemplazo del bloque en cada HTML de C171.

## Reglas de Archify aprendidas (para no romper la validación)
- **Rejilla:** columnas `0..5` en flujos y `0..4` en estados (lifecycle, con 4 carriles como máximo). Un nodo por carril y columna; para apilar dos, usa `yOffset` (±46).
- **Textos:**
  - título del nodo de hasta unos 20 caracteres con `ancho=140`;
  - las etiquetas (`tag`) cortas: no caben más de unos 38 caracteres;
  - etiquetas de flecha de 1 a 3 palabras.
- **Tamaño:**
  - **ancho** total ≤ 1240 px (≤ 1162 si hay texto de 7,5 px);
  - **alto:** si el lienzo es alto y angosto, ensánchalo (nodos más anchos) o agrega una pila con `yOffset`, que activa el desplazamiento vertical.
- **Flechas:**
  - ni cruces ni corredores compartidos;
  - primero deja la ruta automática; fija `fromSide`/`toSide` solo cuando haga falta;
  - si Archify dice que una ruta fijada es inviable, quita el lado que indica.
- **Secuencia:** ancho ≤ 1085 px y relación ancho/alto ≥ 1,55; mensajes cada 28 px, sin notas (se superponen con la etiqueta siguiente). Lo que hace cada paso va en la tarjeta «Qué hace cada paso».
