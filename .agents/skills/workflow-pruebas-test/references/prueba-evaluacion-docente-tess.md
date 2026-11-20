# Prueba de la evaluación docente (encuesta TESS), desde cero

El usuario la pidió el 20/11/2026, con una captura de SVACTES y la lista de páginas: «A docente de teoría, B docente de la práctica… después haremos más pruebas… tú tienes que hacer todo desde 0» (C211). **Aún no se prueba.** El usuario dice cuándo; no se guarda nada en TEST sin que lo pida.

Fuente: instructivo 6.2.5 «Gestionar la evaluación docente», diap. 9 a 67 (ya en el asistente, «Pasos en imágenes»).

## Qué es

Una encuesta que los alumnos responden por NRC para evaluar a su docente. TESS significa *Teaching Effectiveness Survey*. Da indicadores (puntos de calidad) por docente, NRC y área; no es una queja (6.2.5, diap. 5 y 68). Se puede poner una **retención** al alumno mientras no responda.

**Regla del usuario:** la encuesta va por **tipo de horario** del NRC. **A** (`EVALD_A`) es la del **docente de teoría** y **B**, la del **docente de la práctica**.

## Lo que ya está en TEST (captura del 20/11/2026)

**SVACTES**, materia `ESEP` «Estudios de especialidad», curso `02568`, periodo 202744: de periodo 000000 a 999999, código de horario **`TEO`** «Teórico» › código TESC **`EVALD_A`** «Evaluación docente A», **Indicador de anónima marcado**. Captura en `docs/fuentes/banner-test/capturas/2026-11-20-c211-svactes-esep-02568-teo-evald-a.webp`.

**SVITESS** del periodo 202744 (C212): 20 NRC de pregrado con `EVALD_A`, **también los de horario `PRA`**; fechas del 19-NOV-2026 al 25-JUL-2027 (dos NRC desde el 01-ENE-2027), 0 respuestas, origen A (A = anónima, por el indicador de SVACTES; usuario). O sea, SVPTESS ya se corrió en 202744 y la encuesta B de práctica aún no se usa. SVITESS tiene además las columnas Anónima y Estado (A, Activo), C214. Captura en `docs/fuentes/banner-test/capturas/2026-11-20-c212-svitess-202744.webp` (sin los datos de los docentes).

## Orden completo

**Parte 1, configuración de la encuesta** (una vez para toda la universidad; en TEST ya existe `EVALD_A`, así que solo se consulta):

| Paso | Página | Qué se define | Lámina |
|---|---|---|---|
| 1 | SVVACOD | Códigos de respuesta y su tipo: MS selección múltiple, MO opción múltiple, OP pregunta abierta | 9 a 11 |
| 2 | SVAPVAC | Opciones de cada código y sus **puntos de calidad** | 12 y 13 |
| 3 | SVAQCOD | Catálogo de preguntas, cada una con su código de respuesta | 14 |
| 4 | SVVTEQA | Áreas que agrupan las preguntas | 15 |
| 5 | SVVTSSC | Código de la encuesta (`EVALD_A`, `EVALD_B`…) y presentación vertical u horizontal | 16 |
| 6 | SVASDEF | Estructura de la encuesta: secuencia, pregunta, **peso / base del peso** (porcentaje) y área | 19 a 24 |

**Parte 2, aplicar la encuesta en un periodo** (las 7 páginas que dio el usuario, en orden de uso):

| Paso | Página | Qué se hace | Lámina |
|---|---|---|---|
| 7 | **SVACTES** | Por **materia y curso**, desde un periodo: cada **código de horario** (TEO, práctica…) con su **código TESC** y si es **anónima** | 27 y 28 |
| 8 | **SVADTES** | Por **periodo y parte de periodo**: fecha de inicio y fin para responder. Vale para **todos los NRC de esa parte** | 25 y 26 |
| 9 | **SVPTESS** (GJAPCTL) | Asigna la encuesta a los **NRC**. Impresora DATABASE; 01 periodo (obligatorio), 02 materia, 03 curso, 04 NRC, 05 reporte detallado Y/N, 06 eliminar las asignaciones previas Y/N. Con solo 01, 05 y 06 corre para todo el periodo | 29 a 33 |
| 10 | (opcional) STVHLDD y GTVSDAX `HOLDTYPE` | La retención que tendrá el alumno mientras no responda | 34 y 35 |
| 11 | **SVPSTSS** (GJAPCTL) | Asigna la encuesta a los **alumnos** de esos NRC. 1 periodo, 2 materia, 3 curso, 4 NRC, **5 crear retención Y/N**, 6 y 7 fechas de la retención (DD-MMM-AAAA, no antes de hoy), 8 reporte detallado. Salida en GJIREVO | 36 a 44 |
| 12 | Autoservicio del alumno | Encuestas docentes › periodo › docente y NRC › responder todo › **Completar** › estado «Completa» | 46 a 52 |
| 13 | **SVITESS** | Consulta por periodo: avance por NRC, docente, alumnos inscritos y alumnos que respondieron | 58 y 59 |
| 14 | **SVPTQPC** (GJAPCTL) | Calcula los puntos de calidad. 01 periodo (obligatorio); 02 NRC, 03 ID del docente, 04 código de TESS opcionales | 54 a 57 |
| 15 | **SVATSGA** | Permisos para ver: por ID de la persona, de **Control** o de **Resultados**, por escuela, división, departamento o materia | 61 y 62 |
| 16 | Autoservicio del docente | El docente ve sus resultados por periodo | 63 a 67 |

**Ojo:** en el instructivo, la descripción del parámetro 5 de SVPSTSS («Crear retención») está copiada de la del 8 (reporte detallado). Vale el nombre: 5 decide si se crea la retención.

## Caso propuesto para los centros (cuando el usuario lo diga)

1. **Consultar** (sin guardar): SVVTSSC para ver `EVALD_A`, `EVALD_B` y otros códigos; SVASDEF de `EVALD_A` para ver sus preguntas; SVACTES de un curso de los centros (por ejemplo `ESEC 00684`) para ver si ya tiene encuesta.
2. **SVACTES** del curso del centro: el tipo de horario de su NRC (por confirmar cuál usan los NRC de los centros) › `EVALD_A` si es teoría o la B si es práctica; anónima marcada.
3. **SVADTES** del periodo y la parte del NRC (por ejemplo 202656, X06): fechas en que se puede responder.
4. **SVPTESS** solo para ese NRC (01, 04, 05 `Y`, 06 `N`), revisar el .log y el .lis.
5. **SVPSTSS** solo para ese NRC, sin retención (5 `N`), 8 `Y`; revisar en GJIREVO que salga el alumno con su encuesta.
6. El alumno de prueba responde en el autoservicio y la marca «Completa».
7. **SVITESS** para ver que figure como respondida; **SVPTQPC** con 01 y 02 (el NRC).
8. **SVATSGA** solo si hace falta que la jefatura vea los resultados de sus docentes.

## Preguntas abiertas

- ¿Cuál es el código TESC del docente de práctica: `EVALD_B`? El horario de práctica es `PRA`, pero en SVITESS de 202744 los NRC `PRA` tienen `EVALD_A` (C212): ¿falta crear la B en SVACTES?
- Resuelto en TEST (C214): los 5 NRC de la hoja «Est Ciclo Cierre» tienen encuesta (10041 incluido). Como **SVADTES no tiene fechas** para 202744, la encuesta toma las de la **parte de periodo** del NRC: PGE desde el 19-NOV-2026, parte 1 desde el 01-ENE-2027. 10039, 10040 y 10042 ya tienen 1 respuesta.
- ¿Qué tipo de horario tienen los NRC de los centros, y una sola encuesta o teoría y práctica?
- ¿Quién corre SVPTESS, SVPSTSS y SVPTQPC: Registros o la jefatura? ¿La jefatura tendrá permiso en SVATSGA para ver los resultados de sus docentes?
- ¿Se pone retención a los alumnos de los centros que no respondan?
