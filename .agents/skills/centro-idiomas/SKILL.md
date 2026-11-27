---
name: centro-idiomas
description: >-
  Qué hace: datos y pruebas del Centro de Idiomas (Inglés) en Banner: nivel I, materia ESEP, BASIC I
  a III e INTERMEDIATE I a III, prerrequisito secuencial en «Fatal», examen de suficiencia en
  SOATEST, ligas del NRC teórico y el club, partes I01 a I12, cuotas X032 y X228; sus datos están en
  centros/idiomas/datos.json. Cuándo usarla: la tarea es solo de Idiomas o Inglés (cursos, ligas,
  suficiencia, egresados, programas IMEMI). Cuándo no usarla: lo que vale igual para los tres
  centros (arquitectura-centros-empresariales) ni Computación o Emprendimiento.
---

# Centro de Idiomas (Inglés) — Arquitectura Específica

> Este skill contiene la data confirmada y específica del **Centro de Idiomas** (enfocado en **Inglés**).
> Para la arquitectura general de los tres centros, ver `arquitectura-centros-empresariales`.
>
> **Carpeta del centro:** `centros/idiomas/`
> - `datos.json` es la **fuente única** de los datos de este centro. Lo que allí está en `null` sigue **por confirmar** en TEST y en los diagramas se muestra así.
> - `pruebas-test.md` es la **guía de pruebas en TEST**: 6 bloques que cierran los 20 scripts de Idiomas. Empieza por el bloque 0 (descubrir los códigos, U25).
> - `diagramas/` tiene 29 diagramas paso a paso (un flujo y un código por paso; HTML interactivo, PNG claro y oscuro, SVG): 6 flujos base, el de **ligas** (n.º 7) y los 22 scripts. En los scripts que solo se probaron en Computación, sus datos aparecen como «Referencia: así se probó en Computación»; el 02 (sobrepaso de prerrequisito, U10), el 05 (egresados, C50) y el 10 (prerrequisito Fatal) tienen flujo propio de Idiomas (C113). Ver la skill `workflow-diagramas-archify`.

## Mapa de la skill: abre solo el archivo que necesitas

| Si necesitas… | Abre |
|---|---|
| Cursos de Inglés, la regla de prerrequisitos (Basic → Intermediate…) y las ligas teórico virtual + práctica, con los NRC probados | [references/cursos-prerrequisitos-y-ligas.md](references/cursos-prerrequisitos-y-ligas.md) |
| NRC creados en TEST, scripts por validar y dudas abiertas de Inglés | [references/test-scripts-y-dudas.md](references/test-scripts-y-dudas.md) |

## Identificadores en Banner

| Concepto | Código | Descripción |
|---|---|---|
| **Nivel de alumno** | `I` | Idiomas (STVLEVL) |
| **Escuela / College** | `EM` | Centros Empresariales |
| **Campus** | `S` | Sede de Chiclayo |
| **Programa** | `IMEMI03` | Acreditación Idiomas (confirmado C60) |
| **Campo de estudio mayor** | `MI03-01` / `MI03-02` | Malla Idiomas Básicos / Intermedios (confirmado C60) |
| **Departamento** | `EMID` | Jefatura de Centro de Idiomas (confirmado C60) |
| **Grado** | `000000` | No otorga grado |
| **Materia del catálogo** | `ESEP` | Estudios de Especialidad - Idiomas / Posgrado (confirmado C59, C60) |

> ✅ Los identificadores de Idiomas (`IMEMI03`, `EMID`, `MI03-01`, `ESEP`) fueron confirmados en TEST y en la hoja oficial de programación de NRCs (C60).

> **Producción 202721 (C242, foto del 25/11/2026):** cursos nuevos, Basic I a III `ESEP 06083` a `06085` e Intermediate I a III `06086` a `06088` (HT 8), en las partes `I03` e `I04`; NRC de Basic I `1004`, `1015`, `1022` y `1025`. Detalle en `arquitectura-centros-empresariales/references/ref-preguntas-frecuentes-produccion-202721.md`; fórmulas A1-B1 y A2-B2, en `ref-preguntas-frecuentes-formulas-de-calificacion.md`. Todavía no van a `datos.json`: la hoja se sigue llenando.

> **Plan de evaluación A1-B1 en PROD (C254, 27/11/2026):** base en el NRC **1004**: componentes CI 55 y PO 45 con **subcomponentes** (SHAGCOM › Detalles), escala `CEN_100`. Se copia a los demás NRC A1-B1 con «Copiar componentes» (lleva los subcomponentes). Receta en `workflow-pruebas-test/references/recetas/notas-y-cierre.md`.

### Curso en SCACRSE: así está Basic I (C146)
`ESEP 02456` «Basic I» en TEST: Del periodo `000000` · A periodo `999999`; Escuela `EM`; Departamento `EMID`; Estatus `A`; prerrequisito «Básico o ninguno»; horas **variables** (Inferior · indicador · Superior): UEC o crédito `0 O 1`, Cobro `0 O 1`, Teoría `0 O 4`, Laboratorio `0 O 3`, Otro `Ninguno`, Contacto `0 O 7`; Límite de repetición vacío. Es el modelo para un curso nuevo de Idiomas: **Copiar** de él y cambiar el título. A diferencia de Emprendimiento I (horas fijas), Basic I tiene también la teoría, el laboratorio y el contacto variables.

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
