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

## Cursos conocidos (CONFIRMADOS en TEST y Programación — C11, C60)

| Nivel | Código Catálogo | Título Oficial | HT / HP | Malla Curricular | Prerrequisito |
|---|---|---|---|---|---|
| **BASIC I** | `ESEP 02456` | Basic I | 4 HT / 3 HP | `MI03-01` | Ninguno (ingreso) |
| **BASIC II** | `ESEP 02457` | Basic Ii | 4 HT / 3 HP | `MI03-01` | BASIC I aprobado o Suficiencia |
| **BASIC III** | `ESEP 02458` | Basic Iii | 4 HT / 3 HP | `MI03-01` | BASIC II aprobado |
| **INTERMEDIATE I** | `ESEP 02693` | Intermediate I | 4 HT / 3 HP | `MI03-02` | BASIC III aprobado |
| **INTERMEDIATE II** | `ESEP 02721` | Intermediate Ii | 4 HT / 3 HP | `MI03-02` | INTERMEDIATE I aprobado |
| **INTERMEDIATE III** | `ESEP 02997` | Intermediate Iii | 4 HT / 3 HP | `MI03-02` | INTERMEDIATE II aprobado |

> Modo de calificar oficial en catálogo SSASECT: **Modo `C` (Escala Centesimal)** (confirmado C60).

## Regla de prerrequisitos (CONFIRMADA — C11, R09)

En SEUSS, quien desaprueba BASIC I **NO puede pasar a BASIC II** salvo con examen de suficiencia. En Ellucian:

1. **SCAPREQ / SSAPREQ:** se configura el prerrequisito «BASIC I aprobado **o** examen de suficiencia con puntaje mínimo».
2. **SOATERM:** la verificación de prerrequisitos se pone en **Fatal** → SFAREGS bloquea la inscripción.
3. **SOATEST:** se registra el puntaje del examen de suficiencia.
4. **SFPPROJ:** la proyección con verificación de prerrequisitos **no ofrece** BASIC II si no hay BASIC I aprobado o examen.
5. **SFAROVR:** un sobrepaso administrativo puede saltar la regla.

**Idiomas como prerrequisito de pregrado (29/10, C159 a C164):** en **SCAPPRQ** del programa de pregrado (por ejemplo Medicina `1PCSP15`, versión 202444) Nidia Beltrán puso «malla **Y (** `ESEP 02456` **O** `02457` **O** `02458` **)**» (Basic I a III) y, más adelante, Intermediate I a III (`ESEP 02693`, `02721`, `02997`), sin nivel ni calificación: basta con haberlo cursado. El correquisito no sirve, porque pregrado y centros van en periodos distintos. Guía y prueba en [ref-restricciones-y-prerrequisitos-por-programa.md](../arquitectura-centros-empresariales/references/ref-restricciones-y-prerrequisitos-por-programa.md).

## Ligas: Teórico Virtual + 3 Opciones de Práctica (CONFIRMADO C60, R18, ADR-019)
- Cada curso de Idiomas se programa mediante un esquema **Uno a Muchos**: 1 sección teórica principal ligada a 3 secciones prácticas.
- **Teórico Principal (Sección `AT` · Virtual `SAUVIR`):**
  - Horas: 4 créditos totales.
  - Indicadores: **Calificable = Sí**, **Dispensa de colegiatura = No** (cobra la matrícula/cuota).
  - En `SSASECT`: Identificador de liga = **`TA`**.
  - En `SSADETL`: Conector de liga vinculado = **`PA`**.
- **Prácticas Asociadas (`AC1` Presencial Posgrado / `AC2` y `AC3` Virtuales):**
  - Horas: 0 créditos generados.
  - Indicadores: **Calificable = No**, **Dispensa de colegiatura = Sí** (no duplica el cobro).
  - En `SSASECT`: Identificador de liga = **`PA`**.
  - En `SSADETL`: Conector de liga vinculado = **`TA`**.
- **Comportamiento en Matrícula (`SFAREGS` y Autoservicio):**
  - Con ligas en **Fatal** en `SOATERM`, el estudiante debe inscribir obligatoriamente el teórico `AT` junto a **una de las tres opciones de práctica** (`AC1`, `AC2` o `AC3`).
  - Si intenta inscribir solo el teórico, Banner emite: `Error de enlace de sección: Requiere componente ligado (Link Error: PA Required)`.

### NRCs reales probados en TEST (202656 · Parte I10)
- **BASIC III (`ESEP 02458`):**
  - Teórico `10010` (AT · Virtual SAUVIR): Lunes 18:00–20:30 · Dagner Chuman (`100582059`). Liga `TA` $\rightarrow$ `PA`.
  - Práctica `10011` (AC1 · Presencial Posgrado A-31): Martes 20:00–23:20 · Jossymar Cabanillas (`S00912435`). Liga `PA` $\rightarrow$ `TA`.
  - Práctica `10013` (AC2 · Virtual SAUVIR): Sábado 18:00–20:30 · Arnold Vaca (`S00912438`). Liga `PA` $\rightarrow$ `TA`.
  - Práctica `10024` (AC3 · Virtual SAUVIR): Miércoles 08:00–11:20 · Willy Valverde (`S00912437`). Liga `PA` $\rightarrow$ `TA`.
- **INTERMEDIATE I (`ESEP 02693`):**
  - Teórico `10030` (AT · Virtual SAUVIR): Viernes 08:00–11:20 · Dagner Chuman (`100582059`). Liga `TA` $\rightarrow$ `PA`.
  - Práctica `10031` (AC1 · Presencial Posgrado A-31): Jueves 18:00–20:30 · Maria Puelles (`100122229`). Liga `PA` $\rightarrow$ `TA`.
  - Práctica `10032` (AC2 · Virtual SAUVIR): Domingo 14:00–17:20 · Arnold Vaca (`S00912438`). Liga `PA` $\rightarrow$ `TA`.
  - Práctica `10033` (AC3 · Virtual SAUVIR): Sábado 14:00–17:20 · Arnold Vaca (`S00912438`). Liga `PA` $\rightarrow$ `TA`.
- **INTERMEDIATE II (`ESEP 02721`):**
  - Teórico `10034` (AT · Virtual SAUVIR): Sábado 08:00–11:20 · Arnold Vaca (`S00912438`). Liga `TA` $\rightarrow$ `PA`.
  - Práctica `10035` (AC1 · Presencial Posgrado A-41): Viernes 18:00–20:30 · Jossymar Cabanillas (`S00912435`). Liga `PA` $\rightarrow$ `TA`.
  - Práctica `10036` (AC2 · Virtual SAUVIR): Miércoles 18:00–20:30 · Jossymar Cabanillas (`S00912435`). Liga `PA` $\rightarrow$ `TA`.
  - Práctica `10037` (AC3 · Virtual SAUVIR): Jueves 08:00–11:20 · Willy Valverde (`S00912437`). Liga `PA` $\rightarrow$ `TA`.
- **INTERMEDIATE III (`ESEP 02997`):**
  - Teórico `10038` (AT · Virtual SAUVIR): Lunes 14:00–17:20 · Dagner Chuman (`100582059`). Liga `TA` $\rightarrow$ `PA`.
  - Práctica `10039` (AC1 · Presencial Posgrado A-51): Sábado 08:00–11:20 · Rosa Ocampo (`100448074`). Liga `PA` $\rightarrow$ `TA`.
  - Práctica `10040` (AC2 · Virtual SAUVIR): Domingo 08:00–11:20 · Arnold Vaca (`S00912438`). Liga `PA` $\rightarrow$ `TA`.
  - Práctica `10041` (AC3 · Virtual SAUVIR): Viernes 14:00–17:30 · Jossymar Cabanillas (`S00912435`). Liga `PA` $\rightarrow$ `TA`.

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
