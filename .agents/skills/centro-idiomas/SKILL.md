---
name: centro-idiomas
description: Arquitectura específica del Centro de Idiomas (Inglés) de la USS en Ellucian Banner. Cursos conocidos (BASIC I-III, INTERMEDIATE I-III), prerrequisitos secuenciales confirmados, examen de suficiencia, partes de periodo I01-I12 y diagramas paso a paso (centros/idiomas). Úsala siempre que se trabaje exclusivamente con Idiomas/Inglés.
---

# Centro de Idiomas (Inglés) — Arquitectura Específica

> Este skill contiene la data confirmada y específica del **Centro de Idiomas** (enfocado en **Inglés**).
> Para la arquitectura general de los tres centros, ver `arquitectura-centros-empresariales`.
>
> **Carpeta del centro:** `centros/idiomas/`
> - `datos.json` es la **fuente única** de los datos de este centro. Lo que allí está en `null` sigue **por confirmar** en TEST y en los diagramas se muestra así.
> - `diagramas/` tiene 14 diagramas paso a paso (un flujo y un código por paso) (HTML interactivo, PNG claro y oscuro, SVG). Ver la skill `workflow-diagramas-archify`.

## Identificadores en Banner

| Concepto | Código | Descripción |
|---|---|---|
| **Nivel de alumno** | `I` | Idiomas (STVLEVL) |
| **Escuela / College** | `EM` | Centros Empresariales |
| **Campus** | `S` | Sede de Chiclayo |
| **Programa** | *(por confirmar)* | Acreditación Idiomas (pendiente de verificar en TEST) |
| **Campo de estudio mayor** | *(por confirmar)* | Acreditación en Idiomas |
| **Departamento** | *(por confirmar)* | Jef. de Centro de Idiomas |
| **Grado** | `000000` | No otorga grado |
| **Materia del catálogo** | *(por confirmar — probablemente `ESEI` o similar)* | Cursos de Idiomas |

> ⚠ Los identificadores exactos de Programa, Campo de Estudio y Departamento para Idiomas **no han sido verificados en TEST** todavía. Solo se han confirmado los de Computación (CMEMC38 / ACXP / EMCI).

## Partes de periodo (Idiomas)

| Parte | Periodo | Niveles I–II | Niveles III |
|---|---|---|---|
| I01 | 202651 | 5/1 – 15/2 (6 sem) | 5/1 – 31/3 (12 sem) |
| I02 | 202651 | 2/2 – 29/3 (8 sem) | 2/2 – 30/4 (13 sem) |
| I03 | 202651 | 2/3 – 26/4 (8 sem) | 2/3 – 31/5 (13 sem) |
| I04 | 202654 | 6/4 – 31/5 (8 sem) | 6/4 – 30/6 (12 sem) |
| I05 | 202654 | 4/5 – 28/6 (8 sem) | 4/5 – 31/7 (13 sem) |
| I06 | 202654 | 1/6 – 26/7 (8 sem) | 1/6 – 31/8 (13 sem) |
| I07 | 202654 | 6/7 – 30/8 (8 sem) | 6/7 – 30/9 (13 sem) |
| I08 | 202656 | 3/8 – 27/9 (8 sem) | 3/8 – 31/10 (13 sem) |
| I09 | 202656 | 7/9 – 31/10 (8 sem) | 7/9 – 30/11 (12 sem) |
| I10 | 202656 | 5/10 – 29/11 (8 sem) | 5/10 – 31/12 (13 sem) |
| I11 | 202656 | 2/11 – 27/12 (8 sem) | 2/11 – 31/1/2027 (13 sem) |
| I12 | 202656 | 7/12 – 31/1/2027 (8 sem) | 7/12 – 28/2/2027 (12 sem) |

Parte de periodo general: **IGE**.

**Nota importante:** Los niveles I y II de Inglés duran **8 semanas** (I01 solo 6), y los niveles III duran **12 o 13 semanas**. Esto significa que un mismo grupo de Inglés puede tener NRCs con duraciones distintas en la misma parte de periodo.

## Cursos conocidos (CONFIRMADOS — C11)

| Nivel | Curso (nombre SEUSS) | Prerrequisito |
|---|---|---|
| **BASIC I** | — | Ninguno (entrada) |
| **BASIC II** | — | BASIC I aprobado **o** Examen de suficiencia |
| **BASIC III** | — | BASIC II aprobado (asumido) |
| **INTERMEDIATE I** | — | BASIC III aprobado (asumido) |
| **INTERMEDIATE II** | — | INTERMEDIATE I aprobado (asumido) |
| **INTERMEDIATE III** | — | INTERMEDIATE II aprobado (asumido) |

> Los códigos de materia y curso en el catálogo (`SCACRSE`) para Idiomas **no han sido verificados en TEST** todavía.

## Regla de prerrequisitos (CONFIRMADA — C11, R09)

En SEUSS, quien desaprueba BASIC I **NO puede pasar a BASIC II** salvo con examen de suficiencia. En Ellucian:

1. **SCAPREQ / SSAPREQ:** se configura el prerrequisito «BASIC I aprobado **o** examen de suficiencia con puntaje mínimo».
2. **SOATERM:** la verificación de prerrequisitos se pone en **Fatal** → SFAREGS bloquea la inscripción.
3. **SOATEST:** se registra el puntaje del examen de suficiencia.
4. **SFPPROJ:** la proyección con verificación de prerrequisitos **no ofrece** BASIC II si no hay BASIC I aprobado o examen.
5. **SFAROVR:** un sobrepaso administrativo puede saltar la regla.

## Egresados (Script 05, C50)
- El egresado **no se matricula en un curso**: se le activa la plataforma (fuera de Banner; nombre por confirmar, el usuario escribió «Alticia»).
- La nota de la plataforma se pone **igual en BASIC I, BASIC II, etc.**, como un examen de suficiencia. El costo del servicio es distinto.
- En Banner se crea **un solo NRC** y la nota se pasa **a mano**.
- Falta (U24): en qué página se pasa la nota a cada BASIC, el nombre de la plataforma y el servicio de cobro.

## Examen de suficiencia

| Aspecto | Detalle | Duda abierta |
|---|---|---|
| Página Banner | SOATEST (Puntajes de Examen) | — |
| Puntaje mínimo | **No confirmado** | **U01** |
| Quién lo registra | **No confirmado** | **U01** |
| Efecto en CAPP | ¿BASIC I queda pendiente o reconocido? | **E04** |

## Escala de notas

> Pendiente de verificar en `SHAGRDE` para **Nivel I** (Idiomas). La nota aprobatoria **no está confirmada** para este centro. Se asume similar a Computación (mín. 11 sobre 20) pero debe validarse en TEST.

## NRCs creados en TEST

> ⚠ **Ningún NRC de Idiomas ha sido creado en TEST todavía.** Todas las pruebas hasta el 02/10/2026 se realizaron con cursos de Computación (ESEC 00650).

## Scripts por validar (específicos de Inglés)

| Script | Nombre | Particularidad Idiomas |
|---|---|---|
| 04 | Examen de suficiencia | Registrar puntaje en SOATEST, validar que SFAREGS permita BASIC II |
| 10 | Retorno a ciclo anterior | Desaprueba BASIC I → prerrequisito fatal → no puede ir a BASIC II |
| 03 | Convalidación | Convalidar niveles de Inglés de otra institución |

## Dudas abiertas específicas de Inglés

| ID | Duda |
|---|---|
| **U01** | Puntaje mínimo del examen de suficiencia y quién lo registra |
| **E01** | Hora de clase 45 min (día) / 50 min (noche) en un mismo periodo |
| **E04** | Si pasa con examen de suficiencia, ¿cómo queda BASIC I en la historia y en CAPP? |
| **E13** | Casilla «En progreso» de SOATERM con grupos seguidos (I04 termina 31/5, I06 empieza 1/6) |
