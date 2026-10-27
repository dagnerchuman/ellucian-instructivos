---
name: workflow-diagramas-archify
description: >-
  Qué hace: crear, corregir y regenerar los diagramas interactivos paso a paso de cada centro (HTML de
  Archify, PNG claro y oscuro, SVG) desde centros/<centro>/datos.json y
  herramientas/diagramas/plantillas.py, sin editarlos a mano. Cuándo usarla: pide un diagrama, flujo,
  mapa de estados o casuística del sitio, dice «Archify» o «diagramas_flujo», cambia un dato de un
  centro que sale en los diagramas, o hay que actualizar las imágenes o el asistente del sitio.
  Cuándo no usarla: un BPM o flujo dentro de un PDF o PPT (documentos-uss) ni las diapositivas de los
  instructivos (herramientas/diapositivas.py).
---

# Workflow: diagramas paso a paso con Archify

Los diagramas se **generan**: no se editan a mano ni el HTML ni el JSON de salida. Si cambia un dato o un paso, se cambia la fuente y se regenera.

## Dónde está cada cosa
| Qué | Dónde |
|---|---|
| Datos de cada centro (fuente única) | `centros/<centro>/datos.json` (`idiomas`, `computacion`, `emprendimiento`). `null` = «por confirmar» |
| Datos comunes y catálogo de los scripts | `centros/comun/datos.json` |
| Plantillas de los diagramas (el flujo, igual para los tres) | `herramientas/diagramas/plantillas.py` |
| Lectura de datos y textos derivados | `herramientas/diagramas/centro.py` |
| Generador (JSON → `finalize` → imágenes) | `herramientas/diagramas/generar.py` |
| Exportación PNG/SVG (menú «Exportar» del HTML con Playwright) | `herramientas/diagramas/exportar.mjs` |
| Motor Archify (MIT, versión fija, no se sube) | `herramientas/diagramas/instalar_archify.sh` → `herramientas/diagramas/.archify/` |
| Salida | `centros/<centro>/diagramas/NN-tema/<centro>-NN-tema.{workflow,sequence}.json`, `.html`, `-claro.png`, `-oscuro.png`, `.svg` |
| Índices | `centros/README.md`, `centros/index.html` y `centros/<centro>/README.md`, generados por `generar.py` (`indices.py`) |
| Guías paso a paso (modal de cada nodo) | `herramientas/diagramas/guias_operativas.py`: las claves (`n1`, `s3`, `c2`…) son los `id` de los nodos de la plantilla |
| Asistente IA de las páginas | `herramientas/diagramas/assets/asistente_ia.js` (instrucciones, formato y modo seguro) y `asistente_conocimiento.js` (base local, se regenera sola) |

## Tres reglas de diseño (pedido del usuario, 05/10)
1. **Un solo flujo por diagrama.** Los pasos van en una línea, sin ramas ni casos en paralelo. Los errores y las variantes van en las tarjetas («Si sale un error», «Si no deja matricular»). Cada casuística tiene su propio diagrama.
2. **Un solo código por paso.** El título del nodo es una sola página de Banner (`SSASECT`) o, fuera de Banner, un solo término (`Oficio`, `Autoservicio`). Debajo va la acción (verbo + objeto) y en la etiqueta el dato de TEST. Nunca «SCACRSE · SMAAREA».
3. **Un solo término por concepto** (`TERMINOS` en `plantillas.py`): alumno (no participante ni estudiante), NRC (no sección ni grupo), parte (X07), matrícula (no inscripción), cupo (no vacante), pase a historia (no cierre de actas), retención, carga lectiva.

## Diagramas por centro
| N.º | Tema | Tipo Archify |
|---|---|---|
| 0 | El mismo flujo en los tres centros (`centros/comun`) | workflow |
| 1 | Recorrido completo: quién hace cada paso (alumno, asistente, jefe, Banner, docente, Registros, Vicerrectorado) | sequence |
| 2 | Crear el NRC (SOATERM → SCACRSE → SSASECT ×3 → SSASECQ) | workflow |
| 3 | Carga lectiva (SIAINST → SSASECT → SIAASGN → Oficio → Resolución) | workflow |
| 4 | Persona y admisión (GOAMTCH → SAAQUIK → SGASTDN) | workflow |
| 5 | Matrícula en el NRC (SSASECQ → SFAREGS → TSAAREV → SFASLST) | workflow |
| 6 | Notas y pase a historia, flujo probado con el NRC 10044 (SHAEGBC → SHAGCOM → SOAATRK → Autoservicio: pasar lista → Autoservicio: notas → SFASLST → SHRROLL). Los datos de la prueba salen de `datos.json › flujo_notas_test` | workflow |
| 7 | Solo si el centro tiene `ligas` en `datos.json` (hoy, Idiomas): Ligas, NRC teórico + club (SCACRSE → SSASECT ×2 → SSADETL → SFAREGS) | workflow |
| 7 u 8+ | Un script por diagrama: **todos los que aplican al centro** (no van los «no aplica» ni los «por definir»), agrupados por fase y en el orden del proceso: `datos.json › casuisticas` tiene `periodo`, `matricula` y `notas` (C113) | workflow |

**Datos de Computación en otros centros (C113):** las plantillas de los scripts (`CASOS`, `EXTRA_CASOS`) traen los datos con que se probó en Computación. En Idiomas y Emprendimiento, `plantillas.caso()` quita la etiqueta del paso si trae un dato de esas pruebas (`RE_DATO_COMPUTACION`: alumnos S005…, NRC 10xx, CMEMC…, jobs, docente) o la escala vigesimal donde la escala es otra (`RE_ESCALA_V`), y la guía de Excel se muestra como «Referencia: así se probó en Computación (TEST)». Los casos que en un centro son otra cosa tienen flujo propio y no llevan esa guía (`CASO_PROPIO`: Idiomas 02, 05 y 10). El 13 y el 19 toman la escala del centro (`escala_calificacion`).

## Galería ordenada por fases
`centros/index.html` y las tablas de los README muestran cada centro en cuatro grupos: **Flujos base** (1 a 6, más ligas), **Abrir el periodo**, **Matrícula** y **Notas y cierre**. La fase de cada script sale de `datos.json › casuisticas`; para mover un script de fase o de orden, se cambia allí y se regenera con imágenes.

`generar.py` borra solo las carpetas `NN-tema` que ya no corresponden a ninguna plantilla (no toca `anterior-…`).

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

## Reglas del proyecto que los diagramas cumplen
- **El centro siempre visible:** en el nombre del archivo, en el título («Centro de Computación · 2. …») y en el subtítulo (nivel, programa, materia, grupos). Nunca un diagrama «de los tres» con datos de uno solo.
- **Autor:** «Elaborado por: Dagner Anibal Chuman Lluen» en el subtítulo.
- **Tarjetas al pie:** «Probado en TEST», «En Ellucian (instructivos)» con cita, «Lo propio del centro» y «Por confirmar» (las dudas, al final).
- **No inventar códigos:** lo que no está en `datos.json` se muestra «por confirmar». Los datos de ejemplo se marcan «(ejemplo)».
- **Interfaz en español:** `meta.locale = "es"` con el catálogo `examples/locales/es.json` de Archify.

## Diapositivas en cada paso de la guía (ADR-022)
- `python3 herramientas/diapositivas.py` convierte los instructivos a WebP en `visor_instructivos/diapositivas/<id>/` (solo los que faltan o cambiaron; `--solo <texto>` para uno). El visor las usa en lugar del PPTX.
- **Qué lámina va en cada paso (C112):** `herramientas/diagramas/diapositivas_pasos.py`. `INSTRUCTIVOS` da el `<id>` de cada instructivo; `TEMAS` agrupa las láminas por tema (`ssasect_crear`, `sfaregs_retiro`, `pasar_lista`…); `BASE` asigna temas a los pasos de los flujos base (`crear-el-nrc` › `s1`…) y `REGLAS` a los pasos de las casuísticas según la pantalla y palabras de la fase o el hito (por ejemplo, SFAREGS con «retiro» → `sfaregs_retiro`). Una guía también puede traer su propia lista `"diapositivas": [{"instructivo": "5.3", "n": 21}]`, que manda sobre las reglas.
- **Recorte:** `inyectar_modales.py` llama a `diapositivas.recorte()`, que guarda `recortes/NNN.webp` y su firma `NNN.caja`. La caja sale de la posición de los elementos de la lámina (`caja_contenido`): sin título, banda lateral ni pie. Si un recuadro desborda su forma, el borde de abajo baja; si un borde parte las letras de un título, lo baja hasta una fila limpia o mete el título entero. Si cambias la forma de recortar, sube `VERSION_RECORTE` para rehacer todos.
- Si aun así una lámina sale mal, agrega `"caja": [izquierda, arriba, derecha, abajo]` (proporciones) a esa diapositiva. Ese recorte se guarda aparte (`NNN-<caja>.webp`) para no pisar el automático, que otros pasos pueden usar con la misma lámina. Hoy ninguna lámina lo necesita. Revisa los recortes con una hoja de contacto antes de subirlos.
- **Cómo se ve (C110):** fila de láminas con ‹ ›, barra visible y rueda horizontal. Al ampliar: imagen en 3/4 y, a la izquierda, «Su guía»: la fila cuyo campo es un paso numerado de la lámina lleva **el mismo número verde de la captura** (`inyectar_modales._marcas`, C111); las demás llevan círculo y ✓ al validarse. Para evitar un número equivocado, usa `"sin_marca": [campo]` en la diapositiva. El texto numerado de la lámina (`diapositivas.texto_diapositiva`) va plegado en «Ver el texto de la diapositiva»: ya se lee en la imagen.
- **Cobertura (C114):** todos los pasos en Banner de los 84 diagramas tienen lámina. Las páginas que no salen en ningún instructivo (SSASECQ, SHATFAC, SHASMRY, SHATERM, SMIPOUT) usan una lámina de **referencia** con su nota (`_ref(nota, láminas)` en `TEMAS`; el modal la muestra en una franja ámbar). Un paso sin lámina recibe `sin_lamina` en `inyectar_modales._resolver_diapositivas` y el modal explica el motivo (hoy solo los 12 pasos fuera de Banner). Para un tema nuevo, busca las láminas con `buscar_instructivos.py`, agrégalas a `TEMAS` y enlázalas en `BASE` o `REGLAS`.
- **Recorrido completo (C114):** la guía de cada actor sale de `plantillas.guia_recorrido()` (pasos que hace o recibe, en orden) y sus láminas de `diapositivas_pasos.RECORRIDO`.
- **Asistente (C114):** `generar.py` escribe `assets/asistente_diapositivas.js` (`diapositivas_pasos.escribir_indice_asistente()`): las láminas por página de Banner. Debajo de una respuesta con pasos, el asistente muestra «Ver los pasos en imágenes» y elige la lámina de cada paso por su página y las palabras del texto.
- **Memoria del asistente (C117):** `asistente_ia.js` guarda `historial` (pregunta, tema y respuesta). `consultaConContexto()` une la pregunta al tema anterior si es un seguimiento (`esSeguimiento()`: «y», «pero», «eso», «cuáles son», «dime»…) o si es corta y sola no encuentra evidencia; `turnosPrevios()` manda a Groq los 3 últimos turnos. Al cambiar la búsqueda (`recuperarEvidencia`, `sinonimosBusqueda`), compara las fuentes de un banco de preguntas antes y después: ninguna respuesta que ya funcionaba debe perder su fuente.
- **Recorrido automático (C116):** `modal_guia.js › iniciarRecorrido()` abre los pasos con `irAPaso(paso, true)` cada N segundos (`#sel-recorrido-seg`); el control flotante `#recorrido-flotante` atiende el clic en la fase de captura de `window`, porque Archify cierra el paso con un clic fuera de la guía. En pantalla completa, `ajustarGuiaPresentacion()` sube la guía hasta la leyenda.
- **Auditoría:** antes de subir, abre cada diagrama en Chromium y haz clic en cada paso: debe haber filas de guía, láminas que cargan (o el aviso de paso fuera de Banner) y ningún error de JavaScript.

## Tono de las guías y del asistente (pedido del usuario, 24/10)
- **Guías paso a paso:** lenguaje profesional, imperativo formal (ingrese, pulse, verifique), sin emojis, sin exclamaciones ni palabras completas en mayúsculas. Cada fila cita su fuente (C##, U##, instructivo y diapositiva).
- **Asistente:** responde primero en una o dos oraciones; luego, si aplica, «Pasos» numerados con la página de Banner al inicio de cada paso, «Validado en TEST», «Según el instructivo» y «Por confirmar». Siempre con fuentes; sin evidencia local, no consulta al modelo (ADR-021).

## Al terminar
1. Mira al menos el PNG claro de cada diagrama cambiado (Read).
2. Si cambió una skill, ejecuta `python3 herramientas/sincronizar_skills.py --desde claude`.
3. Anota en `registro.md` las decisiones nuevas.
