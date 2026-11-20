# Archify: regenerar y reglas para no romper la validación

Parte de la skill `workflow-diagramas-archify` (el mapa está en su `SKILL.md`).

## Regenerar
```bash
bash herramientas/diagramas/instalar_archify.sh            # una vez por máquina o sesión
python3 herramientas/diagramas/generar.py                  # todo: 84 diagramas (JSON + HTML + índices, sin imágenes)
python3 herramientas/diagramas/generar.py idiomas --solo 4 # un diagrama de un centro
python3 herramientas/diagramas/generar.py --con-imagenes   # opcional: exportar también PNG y SVG (lento)
```
- Cada diagrama pasa por `archify finalize` con calidad *showcase*: esquema, geometría, legibilidad, revisión estricta y prueba en Chromium.
- Si falla, `generar.py` imprime el diagnóstico y el arreglo sugerido. Corrige la plantilla, no el HTML.
- En Windows (Antigravity) funciona igual con `python` y `node`. Para la prueba en navegador, define `ARCHIFY_CHROME` con la ruta de Chrome. En la nube de Claude Code: `ARCHIFY_CHROME=/opt/pw-browsers/chromium-*/chrome-linux64/chrome`; sin esa variable, `finalize` falla y deja HTML incompletos (no los subas: `git checkout -- centros/*/diagramas`).
- Si cambia la numeración (se agrega, quita o reordena una casuística), regenera **con imágenes**: las carpetas nuevas no traen PNG ni SVG y la galería las muestra vacías.
- **Requisito Playwright para `--con-imagenes`** (C176): en la Mac del usuario no está instalado. Se instala fuera del repositorio (`PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 npm install playwright` en el scratchpad) y se exporta con `NODE_PATH=<carpeta>/node_modules node herramientas/diagramas/exportar.mjs <html>`; usa el Google Chrome del sistema.
- **Archify acepta columnas 0 a 5** (`col` y `toCol` ≤ 5, C176): con más pasos, dos o tres comparten columna en carriles distintos. En la Demostración 1, SFAREGS, Autoservicio y SHRROLL van en la columna 5 y la fase «Matricular, dictar y cerrar» empieza en la columna de SFAREGS.
- **`mainPath` no puede volver a una columna anterior** (C192): un flujo en renglones (una fila por fase, cada una desde la columna 0) va sin `mainPath` (`flujo(..., camino_principal=False)`) y la flecha que baja de una fila a la siguiente lleva `fromSide: bottom` y `toSide: top`; si no, Archify da «moves backward» y «ambiguous-corridor». Así está el flujo de la prueba del NRC 10045.
- **Requisito `python-pptx`** (`pip install python-pptx`): sin él, `generar.py` deja **vacías las líneas de las láminas** en las guías de los diagramas, sin avisar (`texto_diapositiva` devuelve `[]`). En la Mac del usuario faltaba (30/10/2026, C171); revisa el diff de `GUIA_MAP` antes de subir. Si además cambian las WebP de `visor_instructivos/diapositivas` sin haber tocado los instructivos, son recodificaciones: `git checkout -- visor_instructivos`.
- **Si solo cambió el asistente** (`assets/asistente_ia.js`), no hace falta regenerar todo: reemplaza en cada `centros/**/*.html` el bloque anterior del asistente (el de `git show HEAD:herramientas/diagramas/assets/asistente_ia.js`) por el nuevo, y ejecuta `python3 herramientas/diagramas/generar_conocimiento_asistente.py` para la base (C171).

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
