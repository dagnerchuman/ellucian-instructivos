# Periodos, partes de periodo y cronograma 2026

Fuentes:
- Instructivos 1.1.1 y 1.1.2 (STVTERM, STVPTRM, SOATERM).
- Presentación «Tema 1: Periodos» de Centros Empresariales, con el cronograma académico 2026.
- Notas del Zoom del usuario (equivalencia con SEUSS).

## Código del periodo
6 dígitos: **año (4) + nivel (1) + secuencia (1)**.
- Nivel **5** = Centros Empresariales.
- Secuencia **1** = ciclo de verano, **4** = semestre I, **6** = semestre II.

| SEUSS (hoy) | Nombre | Ellucian | Meses |
|---|---|---|---|
| 2026-0 | Verano | **202651** | ene – mar |
| 2026-I | Primer periodo | **202654** | abr – jul |
| 2026-II | Segundo periodo | **202656** | ago – dic |
| 2027-0 | Verano 2027 | **202751** | ene – mar 2027 |

Ejemplo del Tema 1: «para el periodo 2026-I de Centros Empresariales, en Ellucian se codifica 2026 5 4».

## Partes de periodo
Una parte de periodo es un rango de fechas dentro del periodo. Tiene sus propias fechas de inicio y fin de clases, de adición y retiro y de ingreso de notas (instructivo 1.1.1, diap. 10).
- Código de máximo 3 caracteres (STVPTRM). Debe existir la parte **1** («Periodo completo»).
- Cada NRC se asigna a una parte de periodo en SSASECT y hereda sus fechas (instructivo 5.3, diap. 23).
- La parte de periodo decide el periodo, **no** la fecha de fin: un grupo puede terminar después de que empezó el siguiente periodo.

| Centro | General | Grupos |
|---|---|---|
| Idiomas | IGE | I01 … I12 (Idiomas Grupo 01…12) |
| Computación | CGE | X01 … X12 |
| Emprendimiento | EGE | P01 … P12 |

## Cronograma 2026: Idiomas
Cada grupo abre 6 cursos: BASIC I, II y III e INTERMEDIATE I, II y III.
- Los niveles I y II duran 8 semanas; en I01, 6 semanas.
- Los niveles III duran 12 o 13 semanas.

| Grupo | Periodo | Niveles I y II | Niveles III |
|---|---|---|---|
| I01 | 202651 | 5/1 – 15/2/2026 (6 sem) | 5/1 – 31/3/2026 (12 sem) |
| I02 | 202651 | 2/2 – 29/3/2026 (8) | 2/2 – 30/4/2026 (13) |
| I03 | 202651 | 2/3 – 26/4/2026 (8) | 2/3 – 31/5/2026 (13) |
| I04 | 202654 | 6/4 – 31/5/2026 (8) | 6/4 – 30/6/2026 (12) |
| I05 | 202654 | 4/5 – 28/6/2026 (8) | 4/5 – 31/7/2026 (13) |
| I06 | 202654 | 1/6 – 26/7/2026 (8) | 1/6 – 31/8/2026 (13) |
| I07 | 202654 | 6/7 – 30/8/2026 (8) | 6/7 – 30/9/2026 (13) |
| I08 | 202656 | 3/8 – 27/9/2026 (8) | 3/8 – 31/10/2026 (13) |
| I09 | 202656 | 7/9 – 31/10/2026 (8) | 7/9 – 30/11/2026 (12) |
| I10 | 202656 | 5/10 – 29/11/2026 (8) | 5/10 – 31/12/2026 (13) |
| I11 | 202656 | 2/11 – 27/12/2026 (8) | 2/11/2026 – 31/1/2027 (13) |
| I12 | 202656 | 7/12/2026 – 31/1/2027 (8) | 7/12/2026 – 28/2/2027 (12) |

## Cronograma 2026: Computación
Cada grupo abre «TODOS» los cursos; los nombres de los cursos **no se conocen**.

| Grupo | Periodo | Fechas | Semanas |
|---|---|---|---|
| X01 | 202651 | 12/1 – 22/2/2026 | 6 |
| X02 | 202651 | 23/2 – 22/3/2026 | 4 |
| X03 | 202654 | 6/4 – 31/5/2026 | 8 |
| X04 | 202654 | 1/6 – 12/7/2026 | 6 |
| X05 | 202656 | 3/8 – 30/8/2026 | 4 |
| X06 | 202656 | 7/9 – 31/10/2026 | 8 |
| X07 | 202656 | 2/11 – 13/12/2026 | 6 |

## Cronograma 2026: Emprendimiento
Cada grupo abre «TODOS» los cursos y siempre dura 10 semanas. Hay grupos que se dictan al mismo tiempo (por ejemplo, P02 y P03).

| Grupo | Periodo | Fechas |
|---|---|---|
| P01 | 202651 | 7/1 – 15/3/2026 |
| P02 | 202651 | 4/2 – 12/4/2026 |
| P03 | 202651 | 11/3 – 17/5/2026 (termina ya en el semestre I) |
| P04 | 202654 | 6/5 – 12/7/2026 |
| P05 | 202656 | 5/8 – 11/10/2026 |
| P06 | 202656 | 30/9 – 6/12/2026 |

## Páginas de configuración (Tema 1)
- STVPTRM: códigos de parte de periodo.
- STVACYR: años académicos; son obligatorios 0000 y 9999.
- STVTRMT: tipos de periodo.
- STVTERM: periodos.
- SOATERM: fechas de partes, fechas web, «Control de periodo web maestro».
- SSAEXCL: feriados y excepciones de clases.
