---
name: centro-computacion
description: Arquitectura específica del Centro de Computación (Informática) de la USS en Ellucian Banner. Datos confirmados en TEST, NRCs creados, alumnos matriculados, notas registradas, scripts validados y diagramas paso a paso (centros/computacion). Úsala siempre que se trabaje exclusivamente con Computación/Informática.
---

# Centro de Computación (Informática) — Arquitectura Específica

> Este skill contiene la data confirmada y específica del **Centro de Informática** (también llamado **Computación**).
> Para la arquitectura general de los tres centros, ver `arquitectura-centros-empresariales`.
>
> **Carpeta del centro:** `centros/computacion/`
> - `datos.json` es la **fuente única** de los datos de esta página (códigos, grupos, NRC, personas de TEST, estado de los 18 scripts y dudas). Si un dato cambia, cámbialo allí y en esta skill, y regenera los diagramas.
> - `diagramas/` tiene los 7 diagramas paso a paso en HTML interactivo, PNG claro y oscuro, y SVG: recorrido, NRC, persona y admisión, estados de la matrícula, notas y cierre, y dos de casuísticas. Ver la skill `workflow-diagramas-archify`.

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
| **Modo de calificación (SHAGRDE Nivel C)** | `V` (además de `P`) | Se agregó `V` el 02/10: incidencia U20 resuelta |

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
| **1026** | ESEC 00650 | D | X07 | 4 | Dagner Chuman (100582059) | Script 15 validado (aforo 1 a 4). 2 inscritos: S00581109 y S00581108 |

## Alumnos creados / usados en TEST

| ID Banner | Nombre | Tipo | Scripts donde participó |
|---|---|---|---|
| **S00581081** | (Alumno 1 - Centros) | Alumno regular de Computación | 01, 06, 13 (nota 16 = Aprobado) |
| **S00581091** | (Alumno 2 - Pregrado+Centros) | Doble programa (pregrado + centros) | 01, 06, 08 (retirado DD), 13 (nota 10 = Desaprobado), 18-B (retención TT) |
| **S00581108** | CARLOS TORRES MENDOZA | Admitido CMEMC38 / Matriculado 1026 | 01, 15 (inscrito en NRC 1026 - Casuística Desaprueba) |
| **S00581109** | MARIA RAMIREZ GARCIA | Admitida CMEMC38 / Matriculada 1026 | 01, 15 (inscrita en NRC 1026 - Casuística Aprueba) |
| **S00581110** | JUAN FLORES CASTILLO | Creado en GOAMTCH | Casuística Inhabilitado (INH) |
| **S00581111** | ANA ROJAS VERA | Creada en GOAMTCH | Casuística Convalidación Externa (SHATRNS) |
| **100582059** | Dagner Chuman (DCHUMAN) | Usuario institucional / docente | 18-A, autoservicio, docente principal |

## Matriz de los 18 Scripts de Computación (Estado al 02/10/2026)

| # | Script / Casuística | Páginas Banner | Estado | Evidencia en TEST |
|---|---|---|---|---|
| **01** | Matrícula regular | `SFAREGS` | ✅ Validado | NRC 1021 (S00581081/S00581091) y NRC 1026 (S00581109/S00581108). |
| **02** | Matrícula especial (sobrepasos) | `SFAROVR` → `SFASRPO` → `SFAREGS` | ✅ **Validado (05/10)** | Regla `CAPACIDAD` (casilla *Capacidad*) en `SFAROVR` 202656. `S00581110` (Juan Flores), admitido con `CMEMC38` y con permiso `CAPACIDAD` en `SFASRPO`, quedó inscrito con **RE** en el NRC 1021 lleno (2/2). Con `S00581108` salió *«Duplicate Course with Section 1026»* porque ya tenía ESEC 00650. |
| **03** | Matrícula por convalidación | `SHATRNS` → `SHATFAC` | ✅ Validado | S00581111 (Ana Rojas) convalidada con IST150 (nota 16, modo P) y rolada a historia. |
| **04** | Matrícula por examen suficiencia | `SOATEST` → `SFAREGS` | 🚫 **NO APLICA** | Confirmado por usuario (C36): Computación **NO** rinde examen de suficiencia (exclusivo de Idiomas). |
| **05** | Curso especial para egresados | `SSASECT` → `SFAREGS` | ⏳ **PENDIENTE** | Sección modular/intensiva para alumnos bachilleres/egresados. |
| **06** | Doble programa simultáneo | `SGASTDN` → `SFAREGS` | ✅ Validado | S00581091 con Pregrado (L1) y Computación (LC) en paralelo. |
| **07** | Tres programas simultáneos | `SGASTDN` → `SFAREGS` | ⏳ **PENDIENTE** | Alumno activo en Pregrado (L1), Idiomas (LI) y Computación (LC). |
| **08** | Retiro de matrícula (DD) | `SFAREGS` | ✅ Validado | S00581091 retirado DD del NRC 1021; vacante liberada automáticamente. |
| **09** | Reactivación de matrícula | `SGASTDN` → `SFAREGS` | ✅ **Validado** | Probado ciclo de suspensión en `SGASTDN`/`SFAREGS` (bloqueo por inactivo y reactivación inmediata a `AS`). |
| **10** | Retorno obligatorio por desaprobado | `SMARQCM` → `SMICRLT` | ✅ **Validado** | S00581108 (nota 08 rolada) auditado en CAPP: Requerimientos y Áreas en «No cumple», créditos usados 0/4, curso `ESEC 00650` clasificado como «Curso no usado» (reprobado). |
| **11** | Apertura de nuevo periodo | `SOATERM` → `STVTERM` | ⏳ **PENDIENTE** | Habilitar partes de periodo X01..X07 en nuevo periodo (ej. 202751). |
| **12** | Cierre de periodo / actas | `GJAPCTL` (`SHRROLL`) | ✅ Validado | Jobs 8113 y 8114 exitosos con pase masivo a historia académica. |
| **13** | Procesamiento de calificaciones | `SFASLST` | ✅ Validado | Registro de notas 16, 10, 08 e INH en actas de NRC 1021 y 1026. |
| **14** | Cierre de curso | `SSASECT` → `SFASLST` | ✅ Validado | Cierre y paso oficial a historia completado con `SHRROLL`. |
| **15** | Ampliación de cupos y reservas | `SSASECT` (`SSARRES`) | ✅ Validado | NRC 1021 (aforo 2/2) y NRC 1026 (error *Closed*, ampliación 1 a 4). |
| **16** | División de grupos / Traslado | `SSASECT` → `SFAREGS` | ✅ **Validado** | María Ramírez (`S00581109`) trasladada de NRC 1026 (`DD`) a NRC 1021 (`RE`), resolviendo `Reserve Closed` ampliando cupo CMEMC38 y confirmada en `SFASLST`. |
| **17** | Gestión de horarios y cruces | `SSASECT` | ✅ **Validado (05/10)** | NRC 1021 y 1026 con el mismo bloque y docente: SSASECT dio «*ERROR* Conflicto de horario del instructor para 100582059. ¿Crear sobrepaso?»; con OK quedó «Indicador de sobrepaso». El cruce del alumno en SFAREGS no se pudo probar (ver C41). |
| **18-A** | Auditoría de carga docente | `SIAASGN` | ✅ Validado | Docente DCHUMAN con 4 NRCs (horas semanales, contacto y FTE nativos). |
| **18-B** | Retenciones y bloqueo fatal | `SOAHOLD` / `STVHLDD` | ✅ Validado | Retención TT bloqueando matrícula en SFAREGS (*ERROR*). |
| **18-C** | Solicitud de servicio / queja | Autoservicio → `SVASVPR` | ✅ **Validado (05/10)** | Mecanismo validado con `CER` (Certificado): el alumno (100582059) crea la solicitud en el Autoservicio y se atiende en `SVASVPR` (estatus, comentario interno y comentario de respuesta). `SVASVPR` no deja crear solicitudes (*«Función inválida»*). **No existe un servicio de queja**: hay 17 en SVVSRVC, todos de carpetas, certificado y constancia (U14). |

---

## 📋 Checklist de Scripts Pendientes para Próximas Sesiones

> **Instrucción para el agente:** A medida que se ejecute cada prueba, marca con `[x]` el script correspondiente y actualiza la evidencia arriba.

- [x] **Script 10 — Retorno obligatorio tras desaprobado (`SMARQCM` → `SMICRLT`):**
  - *Contexto:* Carlos Torres Mendoza (`S00581108`) con nota `08` rolada en `ESEC 00650`.
  - *Evidencia:* CAPP individual arrojó «No cumple» en requerimientos y áreas, 0 créditos obtenidos y curso enviado a «Cursos no usados» (02/10/2026).
- [x] **Script 16 — División de grupos / Traslado de sección (`SFAREGS`):**
  - *Contexto:* Reubicación de participantes de una sección saturada a una sección espejo o cambio de horario.
  - *Evidencia:* María Ramírez (`S00581109`) retirada con `DD` del NRC 1026 e inscrita con `RE` en NRC 1021, auditada en `SFASLST` (02/10/2026).
- [x] **Script 02 — Matrícula especial con sobrepasos (`SFAROVR` → `SFASRPO` → `SFAREGS`):**
  - *Evidencia (05/10):* `S00581110` inscrito con RE en el NRC 1021 lleno gracias al sobrepaso `CAPACIDAD`.
  - *Opcional:* prueba de control con un alumno sin permiso («Closed»); devolver el 1021 a máximo 3 y reserva general 1.
- [ ] **Script 07 — Tres programas en simultáneo (`SGASTDN` → `SFAREGS`):**
  - *Contexto:* Alumno multiescuela (Pregrado + Idiomas + Computación).
  - *Paso:* Crear Study Path 1 (Pregrado `1`), Study Path 2 (Idiomas `I`) y Study Path 3 (Computación `C`) en `SGASTDN`. Inscribir un NRC en cada programa en `SFAREGS`.
- [x] **Script 09 — Reactivación de matrícula (`SGASTDN` → `SFAREGS`):**
  - *Contexto:* Participante que suspendió estudios y retorna.
  - *Evidencia:* Bloqueo de inscripción con estatus inactivo (`IS`/`SU`) y reactivación inmediata a `AS` en `SGASTDN` / `SFAREGS` (02/10/2026).
- [ ] **Pendiente del Script 16:** verificar que el traslado no duplique ni pierda el cobro (TSAAREV).
- [ ] **Script 05 — Curso especial para egresados (`SSASECT` → `SFAREGS`):**
  - *Contexto:* Módulo intensivo de acreditación rápida para graduandos.
  - *Paso:* Programar NRC en parte de periodo intensiva y matricular bachiller.
- [ ] **Script 11 — Apertura de periodo (`SOATERM` → `STVTERM`):**
  - *Contexto:* Parametrización del nuevo periodo académico (ej. `202751`).
  - *Paso:* Configurar fechas de inicio/fin y partes de periodo `X01` a `X07`.
- [x] **Script 17 — Gestión de horarios y cruces (`SSASECT`):**
  - *Evidencia (05/10):* conflicto del docente detectado en el NRC 1021; se resolvió con el sobrepaso del instructor.
  - *Pendiente opcional:* cruce del alumno en SFAREGS con un alumno sin retención, con estatus activo y con ambos NRC sin rolar.
- [x] **Script 18-C — Solicitudes de servicio (Autoservicio → `SVASVPR`):**
  - *Evidencia (05/10):* solicitud CER creada en el Autoservicio y atendida en SVASVPR. Falta que la USS cree el servicio de quejas (U14).
---

## Incidencias resueltas

| ID | Descripción | Solución aplicada y confirmada |
|---|---|---|
| **U20** | Modo de calificación V (catálogo) vs P (SHAGRDE Nivel C) | **RESUELTA (02/10):** Se añadió el Modo `V` (*Vigesimal Regular*) a las notas del Nivel `C` en `SHAGRDE` (Instructivo 7.1.3 diap. 16). `SHRROLL` procesó de inmediato el cierre del NRC 1026 con 100% de éxito. |

## Prerrequisitos y orden de cursos

> **Duda U02 abierta:** No se sabe si los cursos de Informática tienen orden (uno requiere aprobar otro) o son todos independientes. A diferencia de Inglés, no hay confirmación de prerrequisitos secuenciales.
