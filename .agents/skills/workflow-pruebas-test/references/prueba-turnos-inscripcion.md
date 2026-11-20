# Prueba de turnos de inscripción (SFARCTT, SFARCTL, SFARGRP, SFRGRUP), guardada para más tarde

El usuario pidió el 19/11/2026: «lo de fecha de inscripción SFARCTT también guárdalo para más tarde hacer las pruebas… control de prioridad de inscripción: cuando el conteo de grupo es 0 es porque no le hemos asignado a ningún estudiante… revisa el Excel… en SFARGRP hay individual, y cargar masivamente inscripciones de un grupo» (C209). **Aún no se prueba:** el usuario dirá cuándo. No se guarda nada en TEST sin que lo pida.

Fuente: instructivo 5.4 «Inscripción de cursos por lista de espera», diap. 48 a 88 (ya en el asistente).

## Cómo funciona

Un **turno** es un rango de fechas y horas en que un grupo de alumnos puede inscribirse.

| Orden | Página | Qué se hace | Lámina |
|---|---|---|---|
| 1 | **SFARCTT** Control de prioridad de inscripción | Periodo › «+» › fecha y hora de inicio y de fin (HHMM, 24 horas) › **número de prioridad** (único) › guardar. Una prioridad puede tener varios rangos (dos turnos) | diap. 50 a 52 |
| 2 | **SFARCTL** Control de grupo de inscripción | Periodo › «+» › prioridad de SFARCTT › **código de grupo** (hasta 10 caracteres) › guardar. Una prioridad, un grupo; un grupo no va en dos prioridades. **«Conteo de grupo»** = cuántos alumnos tienen el grupo: **0 mientras no se asigne a nadie** | diap. 54 y 55 |
| 3a | **SFARGRP** Grupo de inscripción de alumnos (uno por uno) | ID del alumno y periodo › elegir el grupo › abajo salen las fechas y horas de su turno › guardar | diap. 57 a 60 |
| 3b | **SFRGRUP** (en masa, desde GJAPCTL) | Impresora DATABASE; parámetros 01 periodo, 02 grupo, 03 máximo por grupo, 04 a 07 nivel, grado, tipo de alumno, **atributo de alumno**; 11 a 14 selección de población; **15 modo A (auditar) o U (actualizar)**. Con selección de población solo van 01, 02 y 11 a 15. Resultado en GJIREVO (.lis con los registros creados) y se consulta en SFARGRP | diap. 76 a 88 |

La selección de población para SFRGRUP se arma igual que `POB_CICLO_B` (GLRAPPL › GLRSLCT › GJAJFLU › GJRPSIM › GLAEXTR, C202 a C204; también en el 5.4, diap. 62 a 74).

## Datos de la hoja «Est Ciclo Cierre» del Plan V7 (captura del usuario, 19/11/2026)

**Turnos** (páginas anotadas en la hoja: SFARCTT, SFARCTL, SFRGRUP):

| Prioridad | Fecha inicio | Hora inicio | Hora fin | Fecha fin | Grupo |
|---|---|---|---|---|---|
| 2 | 19/11/2026 | 0:00 (`0000`) | 20:00 (`2000`) | 20/11/2026 | `GRUPO_1` |
| 3 | 19/11/2026 | 0:00 (`0000`) | 20:00 (`2000`) | 20/11/2026 | `GRUPO_2` |
| — | — | — | — | — | `GRUPO_3` (sin prioridad aún) |

**NRC del periodo 202744** en la misma hoja: `ESEP 02568` NRC 10040 (lunes 08:00); `ESGE 00051` NRC 10039 (martes); `ESGE 00054` NRC 10042 (miércoles); `ESGE 00209` NRC 10038 (jueves); `ESGE 00260` «Personal Branding» NRC 10041 (lunes 08:00). No se copian los alumnos de la hoja.

## Pasos de la prueba (cuando el usuario lo diga)

1. **SFARCTT** periodo 202744 (por confirmar): consultar qué prioridades hay; crear 2 y 3 con las fechas y horas de la tabla si no existen.
2. **SFARCTL**: prioridad 2 › `GRUPO_1`, prioridad 3 › `GRUPO_2`. Conteo de grupo en 0.
3. **SFARGRP individual:** un alumno › `GRUPO_1` › ver su turno abajo › guardar. El conteo de `GRUPO_1` pasa a 1.
4. **SFRGRUP masivo:** `GRUPO_2` con una selección de población (¿`POB_CICLO_B`?), primero en modo **A** (auditar) y revisar el .lis; luego en **U**. Revisar en SFARCTL que el conteo suba y en SFARGRP el grupo de un ID.
5. **Inscripción:** un alumno con turno intenta inscribirse por autoservicio dentro y fuera de su rango.

## Preguntas abiertas

- ¿Periodo 202744 o 202746 (el plan dice matrícula 202746)?
- ¿Por qué empieza en la prioridad 2? ¿Ya hay una prioridad 1? ¿Qué prioridad lleva `GRUPO_3`?
- ¿Para el SFRGRUP masivo se usa `POB_CICLO_B` u otra selección?
- ¿Lo hace la jefatura o Registros Académicos? Los turnos son de toda la inscripción del periodo; la jefatura solo debería tocar lo de sus alumnos.
