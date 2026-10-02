---
name: centro-informatica
description: Arquitectura específica del Centro de Informática (Computación) de la USS en Ellucian Banner. Datos confirmados en TEST, NRCs creados, alumnos matriculados, notas registradas y scripts validados. Úsala siempre que se trabaje exclusivamente con Computación/Informática.
---

# Centro de Informática (Computación) — Arquitectura Específica

> Este skill contiene la data confirmada y específica del **Centro de Informática** (también llamado **Computación**).
> Para la arquitectura general de los tres centros, ver `arquitectura-centros-empresariales`.

## Identificadores en Banner

| Concepto | Código | Descripción |
|---|---|---|
| **Nivel de alumno** | `C` | Computación (STVLEVL) |
| **Escuela / College** | `EM` | Centros Empresariales |
| **Campus** | `S` | Sede de Chiclayo |
| **Programa** | `CMEMC38` | Acreditación Computación XP 01 |
| **Campo de estudio mayor** | `ACXP` | Acreditación en Computación XP |
| **Departamento** | `EMCI` | Jef. de Centro de Informática |
| **Grado** | `000000` | No otorga grado |
| **Materia del catálogo** | `ESEC` | Escuela EM — cursos de Computación |
| **Regla de currículo base** | `ECOM-01` | Computación I (área MC38-01, Ciclo I) |
| **Modo de calificación (catálogo)** | `V` | Vigesimal regular |
| **Modo de calificación (SHAGRDE Nivel C)** | `P` | Vigesimal especial (**⚠ Incidencia U20**) |

## Partes de periodo (Computación)

| Parte | Periodo | Fechas | Semanas |
|---|---|---|---|
| X01 | 202651 | 12/1 – 22/2/2026 | 6 |
| X02 | 202651 | 23/2 – 22/3/2026 | 4 |
| X03 | 202654 | 6/4 – 31/5/2026 | 8 |
| X04 | 202654 | 1/6 – 12/7/2026 | 6 |
| X05 | 202656 | 3/8 – 30/8/2026 | 4 |
| X06 | 202656 | 7/9 – 31/10/2026 | 8 |
| X07 | 202656 | 2/11 – 13/12/2026 | 6 |

Parte de periodo general: **CGE**.

## Cursos conocidos

> ⚠ Los **nombres reales** de los cursos de Computación **no se conocen** (duda U05). El cronograma solo dice «TODOS».

| Materia | Curso | Nombre (en TEST) | Créditos |
|---|---|---|---|
| ESEC | 00650 | Ofimática Word 365 | — |
| ESEC | 00651–00657 | (otros cursos del ciclo I, sin nombre confirmado) | — |

## Escala de notas (SHAGRDE, Nivel C)

| Nota | Aprueba | Gana créditos | Observación |
|---|---|---|---|
| 11–20 | ✅ Sí | ✅ Sí | Nota mínima aprobatoria: **11** |
| 00–10 | ❌ No | ❌ No | Desaprobado |
| INH | ❌ No | ❌ No | Inhabilitado por inasistencia (< 70%) |

## NRCs creados en TEST (periodo 202656)

| NRC | Materia/Curso | Sección | Parte | Cupo | Docente | Estado |
|---|---|---|---|---|---|---|
| **1021** | ESEC 00650 | B | X07 | 2 | Dagner Chuman (100582059) | Validado: matrícula, notas, retiro |
| **1024** | ESEC 00650 | C | — | — | Dagner Chuman (100582059) | Activo (auditado en SIAASGN) |
| **1026** | ESEC 00650 | D | X07 | 1 | Dagner Chuman (100582059) | Creado para convalidación (C31) |

## Alumnos creados / usados en TEST

| ID Banner | Nombre | Tipo | Scripts donde participó |
|---|---|---|---|
| **S00581081** | (Alumno 1 - Centros) | Alumno regular de Computación | 01, 06, 13 (nota 16 = Aprobado) |
| **S00581091** | (Alumno 2 - Pregrado+Centros) | Doble programa (pregrado + centros) | 01, 06, 08 (retirado DD), 13 (nota 10 = Desaprobado), 18-B (retención TT) |
| **S00581108** | CARLOS TORRES MENDOZA | Nuevo, limpio para convalidación | 32 (persona creada en GOAMTCH) |
| **100582059** | Dagner Chuman (DCHUMAN) | Usuario institucional / docente | 18-A, autoservicio, docente principal |

## Scripts validados para Computación (al 02/10/2026)

| Script | Nombre | Estado | Evidencia |
|---|---|---|---|
| 01 | Matrícula regular | ✅ Validado | 2/2 alumnos en NRC 1021 |
| 06 | Doble programa | ✅ Validado | S00581091 con Study Paths 2/3/4 |
| 08 | Retiro de matrícula (DD) | ✅ Validado | S00581091 retirado, cupo liberado |
| 13 | Procesamiento de calificaciones | ✅ Validado | Notas 16 y 10 en SFASLST |
| 15 | Gestión de cupos y reservas | ✅ Validado | SSARRES con regla CMEMC38 + nula |
| 18-A | Auditoría de carga docente | ✅ Validado | SIAASGN: 4 NRCs, horas y FTE |
| 18-B | Retenciones y bloqueo | ✅ Validado | SOAHOLD TT, error fatal en SFAREGS |

## Incidencias abiertas

| ID | Descripción | Impacto |
|---|---|---|
| **U20** | Modo de calificación V (catálogo) vs P (SHAGRDE Nivel C) → SHRROLL falla con «No Substitute Grade Found» | Bloquea el pase a historia académica |

## Prerrequisitos y orden de cursos

> **Duda U02 abierta:** No se sabe si los cursos de Informática tienen orden (uno requiere aprobar otro) o son todos independientes. A diferencia de Inglés, no hay confirmación de prerrequisitos secuenciales.
