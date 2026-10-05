---
name: centro-emprendimiento
description: Arquitectura específica del Centro de Emprendimiento de la USS en Ellucian Banner. Partes de periodo P01-P06, materia ESGE, NRC 1025 probado en TEST y diagramas paso a paso (centros/emprendimiento). Úsala siempre que se trabaje exclusivamente con Emprendimiento.
---

# Centro de Emprendimiento — Arquitectura Específica

> Este skill contiene la data confirmada y específica del **Centro de Emprendimiento**.
> Para la arquitectura general de los tres centros, ver `arquitectura-centros-empresariales`.
>
> **Carpeta del centro:** `centros/emprendimiento/`
> - `datos.json` es la **fuente única** de los datos de este centro. Lo que allí está en `null` sigue **por confirmar** en TEST y en los diagramas se muestra así.
> - `diagramas/` tiene 14 diagramas paso a paso (un flujo y un código por paso) (HTML interactivo, PNG claro y oscuro, SVG). Ver la skill `workflow-diagramas-archify`.

## Identificadores en Banner

| Concepto | Código | Descripción |
|---|---|---|
| **Nivel de alumno** | `M` | Emprendimiento (STVLEVL) |
| **Escuela / College** | `EM` | Centros Empresariales |
| **Campus** | `S` | Sede de Chiclayo |
| **Programa** | *(por confirmar)* | Acreditación Emprendimiento |
| **Campo de estudio mayor** | *(por confirmar)* | Acreditación en Emprendimiento |
| **Departamento** | *(por confirmar)* | Jef. de Centro de Emprendimiento |
| **Grado** | `000000` | No otorga grado |
| **Materia del catálogo** | `ESGE` | Cursos de Emprendimiento |

> ⚠ Los identificadores exactos de Programa, Campo de Estudio y Departamento para Emprendimiento **no han sido verificados completamente en TEST** todavía. Lo que sí se confirmó es que la materia es `ESGE` y el Nivel es `M`.

## Partes de periodo (Emprendimiento)

Todos los grupos duran **10 semanas**. Hay grupos que se dictan al mismo tiempo (P02 y P03 se superponen).

| Parte | Periodo | Fechas |
|---|---|---|
| P01 | 202651 | 7/1 – 15/3/2026 |
| P02 | 202651 | 4/2 – 12/4/2026 |
| P03 | 202651 | 11/3 – 17/5/2026 *(termina ya en semestre I)* |
| P04 | 202654 | 6/5 – 12/7/2026 |
| P05 | 202656 | 5/8 – 11/10/2026 |
| P06 | 202656 | 30/9 – 6/12/2026 |

Parte de periodo general: **EGE**.

**Nota importante:** P03 empieza en el periodo 202651 (verano) pero termina el 17/5, ya dentro del rango de 202654 (semestre I). La parte de periodo decide el periodo, **no** la fecha de fin.

## Cursos conocidos

> ⚠ Los **nombres reales** de los cursos de Emprendimiento **no se conocen** (duda U05). El cronograma solo dice «TODOS».

| Materia | Curso | Nombre (en TEST) | Créditos |
|---|---|---|---|
| ESGE | 00117 | *(nombre por confirmar)* | — |

## NRCs probados en TEST (periodo 202656)

| NRC | Materia/Curso | Sección | Parte | Docente | Estado |
|---|---|---|---|---|---|
| **1025** | ESGE 00117 | A | — | Dagner Chuman (100582059), Sesión 02 (no principal) | Auditado en SIAASGN (1,98 h/sem, 19,8 h tot, FTE 0,04) |

> El NRC 1025 fue auditado en SIAASGN (Script 18-A) pero **no se han hecho pruebas de matrícula, notas ni cierre específicas de Emprendimiento**.

## Escala de notas

> Pendiente de verificar en `SHAGRDE` para **Nivel M** (Emprendimiento). La nota aprobatoria y el modo de calificación **no están confirmados** para este centro.

## Prerrequisitos y orden de cursos

> **Duda U02 abierta:** No se sabe si los cursos de Emprendimiento tienen orden (uno requiere aprobar otro) o son todos independientes.

## Scripts por validar (específicos de Emprendimiento)

| Script | Nombre | Particularidad Emprendimiento |
|---|---|---|
| 01 | Matrícula regular | Validar con programa de Emprendimiento (Nivel M) |
| 13 | Procesamiento de notas | Validar escala y modo de calificación Nivel M |
| 05 | Curso especial para egresados | Grupos modulares intensivos P01-P06 de 10 semanas |
| 03 | Convalidación | Convalidar módulos de emprendimiento |

## Dudas abiertas específicas de Emprendimiento

| ID | Duda |
|---|---|
| **U02** | ¿Los cursos tienen orden secuencial o son todos independientes? |
| **U05** | Nombres reales de los cursos, pesos de evaluación y nota aprobatoria |
| **E01** | Hora de clase 45 min (día) / 50 min (noche) en un mismo periodo |

## Particularidades de Emprendimiento

1. **Grupos simultáneos:** P02 y P03 se superponen en el cronograma, lo que implica que un participante podría estar en dos grupos a la vez (o que son secciones paralelas del mismo curso).
2. **Duración uniforme:** todos los grupos duran exactamente 10 semanas, a diferencia de Idiomas (8/12-13 semanas) y Computación (4-8 semanas).
3. **Materia ESGE vs ESEC/ESEP:** Emprendimiento usa la materia `ESGE` (General), distinta de `ESEC` (Computación) y `ESEP` (Especiales/CE).
