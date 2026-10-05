---
name: workflow-diagramas-archify
description: Cómo crear, corregir y regenerar los diagramas interactivos paso a paso de los Centros Empresariales (HTML de Archify, PNG claro y oscuro, SVG) por centro. Úsala cuando el usuario pida un diagrama, flujo, mapa de estados o casuísticas, diga «Archify» o «diagramas_flujo», cambie un dato de un centro (programa, materia, NRC, escala, estado de un script) o pida actualizar las imágenes.
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
| Índices | `centros/README.md`, `centros/index.html` y `centros/<centro>/README.md`, generados por `generar.py` |

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
| 6 | Notas y pase a historia (SHAGRDE → SHAGCOM → Autoservicio → SHRROLL → SMICRLT) | workflow |
| 7+ | Una casuística por diagrama, en el orden de `datos.json › casuisticas` | workflow |

`generar.py` borra solo las carpetas `NN-tema` que ya no corresponden a ninguna plantilla (no toca `anterior-…`).

## Regenerar
```bash
bash herramientas/diagramas/instalar_archify.sh            # una vez por máquina o sesión
python3 herramientas/diagramas/generar.py                  # todo: 43 diagramas + índices
python3 herramientas/diagramas/generar.py idiomas --solo 4 # un diagrama de un centro
python3 herramientas/diagramas/generar.py --sin-imagenes   # más rápido: solo JSON + HTML
```
- Cada diagrama pasa por `archify finalize` con calidad *showcase*: esquema, geometría, legibilidad, revisión estricta y prueba en Chromium.
- Si falla, `generar.py` imprime el diagnóstico y el arreglo sugerido. Corrige la plantilla, no el HTML.
- En Windows (Antigravity) funciona igual con `python` y `node`. Para la prueba en navegador, define `ARCHIFY_CHROME` con la ruta de Chrome.

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

## Al terminar
1. Mira al menos el PNG claro de cada diagrama cambiado (Read).
2. Si cambió una skill, ejecuta `python3 herramientas/sincronizar_skills.py --desde claude`.
3. Anota en `registro.md` las decisiones nuevas.
