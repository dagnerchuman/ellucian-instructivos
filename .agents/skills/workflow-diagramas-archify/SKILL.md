---
name: workflow-diagramas-archify
description: >-
  Qué hace: crear, corregir y regenerar los diagramas interactivos paso a paso de cada centro (HTML de
  Archify, PNG claro y oscuro, SVG) desde centros/<centro>/datos.json y
  herramientas/diagramas/plantillas.py, sin editarlos a mano. Cuándo usarla: pide un diagrama, flujo,
  mapa de estados o casuística del sitio, dice «Archify» o «diagramas_flujo», cambia un dato de un
  centro que sale en los diagramas, hay que actualizar las imágenes o el asistente del sitio, o
  poner cuadros y números en las capturas de TEST de una prueba (anotar_capturas.py).
  Cuándo no usarla: un BPM o flujo dentro de un PDF o PPT (documentos-uss) ni las diapositivas de los
  instructivos (herramientas/diapositivas.py).
---

# Workflow: diagramas paso a paso con Archify

Los diagramas se **generan**: no se editan a mano ni el HTML ni el JSON de salida. Si cambia un dato o un paso, se cambia la fuente y se regenera.

## Mapa de la skill: abre solo el archivo que necesitas

| Si necesitas… | Abre |
|---|---|
| Regenerar los diagramas (`generar.py`) y los errores de Archify que ya se aprendieron | [references/regenerar-y-reglas-archify.md](references/regenerar-y-reglas-archify.md) |
| Qué diagramas tiene cada centro y cómo está ordenada la galería por fases | [references/diagramas-por-centro.md](references/diagramas-por-centro.md) |
| Láminas de los instructivos en cada paso, números verdes, «Pasos en imágenes» del asistente (`diapositivas_pasos.py`) | [references/diapositivas-y-laminas.md](references/diapositivas-y-laminas.md) |

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

## Reglas del proyecto que los diagramas cumplen
- **El centro siempre visible:** en el nombre del archivo, en el título («Centro de Computación · 2. …») y en el subtítulo (nivel, programa, materia, grupos). Nunca un diagrama «de los tres» con datos de uno solo.
- **Autor:** «Elaborado por: Dagner Anibal Chuman Lluen» en el subtítulo.
- **Tarjetas al pie:** «Probado en TEST», «En Ellucian (instructivos)» con cita, «Lo propio del centro» y «Por confirmar» (las dudas, al final).
- **No inventar códigos:** lo que no está en `datos.json` se muestra «por confirmar». Los datos de ejemplo se marcan «(ejemplo)».
- **Interfaz en español:** `meta.locale = "es"` con el catálogo `examples/locales/es.json` de Archify.

## Tono de las guías y del asistente (pedido del usuario, 24/10)
- **Guías paso a paso:** lenguaje profesional, imperativo formal (ingrese, pulse, verifique), sin emojis, sin exclamaciones ni palabras completas en mayúsculas. Cada fila cita su fuente (C##, U##, instructivo y diapositiva).
- **Asistente:** responde primero en una o dos oraciones; luego, si aplica, «Pasos» numerados con la página de Banner al inicio de cada paso, «Validado en TEST», «Según el instructivo» y «Por confirmar». Siempre con fuentes; sin evidencia local, no consulta al modelo (ADR-021).

## Al terminar
1. Mira al menos el PNG claro de cada diagrama cambiado (Read).
2. Si cambió una skill, ejecuta `python3 herramientas/sincronizar_skills.py --desde claude`.
3. Anota en `registro.md` las decisiones nuevas.
