# Archify: diagramas por centro y galería

Parte de la skill `workflow-diagramas-archify` (el mapa está en su `SKILL.md`).

## Diagramas por centro
| N.º | Tema | Tipo Archify |
|---|---|---|
| 0 | **Demostraciones para reuniones** (`datos.json › demostraciones`): un caso real de TEST en el orden curso › NRC › docente › fórmula › alumno, con su guion. Van primero (`00-demostracion-…`) y la galería les da su grupo. Hoy: Computación, «Demostración 1 · Diseño Web de punta a punta (NRC 10044)» (C134) | workflow |
| 0 | **Prueba en TEST de una demostración** (`demostraciones › ejemplo_prueba_2`): su propio flujo, `00-demostracion-N-prueba-nrc-<NRC>`, justo después de la demostración (C192). Una fila por fase (`fases`), un nodo por paso con su `etiqueta` y sus `laminas`; al abrir el paso, su tabla (`tabla`, más «Banner respondió» y la `nota`), «Así quedó en TEST» con las `capturas` (mismo visor con zoom de las láminas) y «Así se ve en Banner». Hoy: NRC 10045, 14 pasos | workflow |
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

**Dirección de la galería (C235):** se abre como `centros/index.html` o `centros/`. Con una barra de más (`index.html/`), el navegador toma el archivo por carpeta: miniaturas en blanco, y «HTML interactivo» lleva a `index.html/computacion/…`, que Five Server responde con «[object Object]». La galería quita esa barra sola al cargar (script del `<head>` en `assets/indice_galeria.html`).
