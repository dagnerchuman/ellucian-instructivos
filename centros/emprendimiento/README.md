<!-- Archivo generado por herramientas/diagramas/generar.py: no lo edites a mano. -->
# Centro de Emprendimiento

Ficha generada desde [`datos.json`](datos.json), que es la fuente única de los datos de este centro. Lo marcado «por confirmar» todavía no se verificó en TEST.

## Diagramas paso a paso
| N.º | Diagrama | Archivos |
|---|---|---|
| 1 | Recorrido completo en Banner | [HTML](diagramas/01-recorrido-completo/emprendimiento-01-recorrido-completo.html) · [PNG claro](diagramas/01-recorrido-completo/emprendimiento-01-recorrido-completo-claro.png) · [PNG oscuro](diagramas/01-recorrido-completo/emprendimiento-01-recorrido-completo-oscuro.png) · [SVG](diagramas/01-recorrido-completo/emprendimiento-01-recorrido-completo.svg) |
| 2 | Crear un NRC paso a paso (SSASECT) | [HTML](diagramas/02-crear-nrc/emprendimiento-02-crear-nrc.html) · [PNG claro](diagramas/02-crear-nrc/emprendimiento-02-crear-nrc-claro.png) · [PNG oscuro](diagramas/02-crear-nrc/emprendimiento-02-crear-nrc-oscuro.png) · [SVG](diagramas/02-crear-nrc/emprendimiento-02-crear-nrc.svg) |
| 3 | Persona y admisión paso a paso | [HTML](diagramas/03-persona-y-admision/emprendimiento-03-persona-y-admision.html) · [PNG claro](diagramas/03-persona-y-admision/emprendimiento-03-persona-y-admision-claro.png) · [PNG oscuro](diagramas/03-persona-y-admision/emprendimiento-03-persona-y-admision-oscuro.png) · [SVG](diagramas/03-persona-y-admision/emprendimiento-03-persona-y-admision.svg) |
| 4 | Estados de la matrícula en el NRC | [HTML](diagramas/04-estados-de-la-matricula/emprendimiento-04-estados-de-la-matricula.html) · [PNG claro](diagramas/04-estados-de-la-matricula/emprendimiento-04-estados-de-la-matricula-claro.png) · [PNG oscuro](diagramas/04-estados-de-la-matricula/emprendimiento-04-estados-de-la-matricula-oscuro.png) · [SVG](diagramas/04-estados-de-la-matricula/emprendimiento-04-estados-de-la-matricula.svg) |
| 5 | Notas, asistencia y cierre de actas | [HTML](diagramas/05-notas-y-cierre/emprendimiento-05-notas-y-cierre.html) · [PNG claro](diagramas/05-notas-y-cierre/emprendimiento-05-notas-y-cierre-claro.png) · [PNG oscuro](diagramas/05-notas-y-cierre/emprendimiento-05-notas-y-cierre-oscuro.png) · [SVG](diagramas/05-notas-y-cierre/emprendimiento-05-notas-y-cierre.svg) |
| 6 | Casuísticas de matrícula | [HTML](diagramas/06-casuisticas-de-matricula/emprendimiento-06-casuisticas-de-matricula.html) · [PNG claro](diagramas/06-casuisticas-de-matricula/emprendimiento-06-casuisticas-de-matricula-claro.png) · [PNG oscuro](diagramas/06-casuisticas-de-matricula/emprendimiento-06-casuisticas-de-matricula-oscuro.png) · [SVG](diagramas/06-casuisticas-de-matricula/emprendimiento-06-casuisticas-de-matricula.svg) |
| 7 | Casuísticas de notas y cierre | [HTML](diagramas/07-casuisticas-de-notas-y-cierre/emprendimiento-07-casuisticas-de-notas-y-cierre.html) · [PNG claro](diagramas/07-casuisticas-de-notas-y-cierre/emprendimiento-07-casuisticas-de-notas-y-cierre-claro.png) · [PNG oscuro](diagramas/07-casuisticas-de-notas-y-cierre/emprendimiento-07-casuisticas-de-notas-y-cierre-oscuro.png) · [SVG](diagramas/07-casuisticas-de-notas-y-cierre/emprendimiento-07-casuisticas-de-notas-y-cierre.svg) |

## Códigos en Banner
| Concepto | Código | Nota |
|---|---|---|
| Nivel (STVLEVL) | `M` | Emprendimiento |
| Escuela | `EM` | Centros Empresariales |
| Campus | `S` | Sede Chiclayo |
| Grado | `000000` | No otorga grado |
| Programa | por confirmar |  |
| Mayor | por confirmar |  |
| Departamento | por confirmar |  |
| Materia | `ESGE` | Cursos de Emprendimiento |
| Escala de notas | escala por confirmar |  |
| Parte general | `EGE` | grupos P01–P06 en 2026 |

## Lo propio de este centro
- Todos los grupos duran 10 semanas
- P02 y P03 se dictan al mismo tiempo: un participante podría estar en dos grupos
- P03 empieza en 202651 y termina en el semestre I: manda la parte de periodo, no la fecha de fin

## Grupos 2026 (Todos los grupos duran 10 semanas; P02 y P03 se dictan al mismo tiempo)
| Grupo | Periodo | Fechas | Semanas |
|---|---|---|---|
| P01 | 202651 | 07/01 – 15/03/2026 | 10 |
| P02 | 202651 | 04/02 – 12/04/2026 | 10 |
| P03 | 202651 | 11/03 – 17/05/2026 | 10 |
| P04 | 202654 | 06/05 – 12/07/2026 | 10 |
| P05 | 202656 | 05/08 – 11/10/2026 | 10 |
| P06 | 202656 | 30/09 – 06/12/2026 | 10 |

## NRC en TEST
- NRC **1025**: ESGE 00117, sección A. Solo carga docente: sesión 02, no principal (1,98 h/sem, 19,8 h, FTE 0,04).

## Los 18 scripts (18 por probar · 1 por definir · 1 validado)
| Script | Nombre | Estado | Evidencia o pendiente |
|---|---|---|---|
| 01 | Matrícula regular | por probar | Matrícula con un programa de nivel M |
| 02 | Matrícula especial con sobrepasos | por probar | Sobrepaso de cupo |
| 03 | Matrícula por convalidación | por probar | Convalidar módulos de emprendimiento |
| 04 | Matrícula por examen de suficiencia | por definir | ¿Aplica examen de suficiencia? (U21) |
| 05 | Curso especial para egresados | por probar | Grupo intensivo para egresados |
| 06 | Dos programas en simultáneo | por probar | Pregrado + Emprendimiento |
| 07 | Tres programas en simultáneo | por probar | Tres programas en simultáneo |
| 08 | Retiro de matrícula (DD) | por probar | Retiro con DD |
| 09 | Suspensión y reactivación | por probar | Suspensión y reactivación |
| 10 | Retorno por desaprobado | por probar | Depende de U02 (orden de los cursos) |
| 11 | Apertura de periodo | por probar | Partes P01–P06 en un periodo nuevo |
| 12 | Cierre de periodo | por probar | SHRROLL con la escala del nivel M |
| 13 | Procesamiento de calificaciones | por probar | Escala y modo de calificación del nivel M |
| 14 | Cierre de curso | por probar | Cierre de curso |
| 15 | Ampliación de cupos y reservas | por probar | Ampliación de cupo |
| 16 | División de grupos y traslado | por probar | Traslado entre P02 y P03, que se cruzan |
| 17 | Gestión de horarios y cruces | por probar | Cruces por grupos simultáneos |
| 18-A | Auditoría de carga docente | validado | NRC 1025 aparece en la carga del docente (SIAASGN) |
| 18-B | Retenciones y bloqueo de matrícula | por probar | Retención que bloquea la matrícula |
| 18-C | Solicitud de servicio o queja | por probar | Solicitud o queja |

## Por confirmar
- **U02**: ¿Los cursos tienen orden o son independientes?
- **U05**: Nombres oficiales de los cursos, pesos de evaluación y nota aprobatoria
- **U21**: ¿Rinde examen de suficiencia o solo aplica a Idiomas?
- **TEST**: Programa, mayor, departamento y escala de notas del nivel M: verificar en TEST
