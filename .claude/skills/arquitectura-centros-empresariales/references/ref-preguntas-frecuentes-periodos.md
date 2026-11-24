# Preguntas frecuentes de operación: Periodos y partes de periodo

Respuestas cortas para el asistente IA y para cualquier agente, tomadas de los instructivos 1.1.1 y 1.1.2 (Capacidad 1), de lo visto en TEST y del registro. Cada pregunta es un fragmento de la base del asistente (C197, C237, C238). Si la respuesta no está aquí ni en el registro, se dice «No lo sé» (ruta de escape).

**Desde el 24/11/2026 la meta es producción, que empieza con 202721 (C238, ADR-026).** Los periodos de 2026 (202651, 202654 y 202656) fueron de TEST y se citan como historia.

Tema de este archivo: qué son el periodo y la parte de periodo, cuáles usan los centros y quién los crea. El periodo 202721 en detalle está en `ref-preguntas-frecuentes-periodo-202721.md`; cómo se crean y configuran en Banner (STVTERM, STVPTRM, SOATERM, SSAEXCL), en `ref-preguntas-frecuentes-periodos-configuracion.md`; el cronograma 2026 de TEST, en `ref-periodos-y-cronograma.md`.

### ¿Qué es un periodo académico en Banner?
Es el lapso en que la institución hace sus actividades académicas: admisión, matrícula, notas, asistencia, graduación y procesos financieros (instructivo 1.1.1, diap. 10 y 23). El código se crea en **STVTERM** y el periodo se habilita en **SOATERM**: inscripción, partes de periodo y fechas web (1.1.2). En producción, los centros empiezan con **202721**, el verano 2027 (ADR-026).

### ¿Cuál es la estructura de los periodos en los centros?
Tiene dos niveles (ADR-026, ADR-006):
- **Periodo:** 6 dígitos. Desde 2027 es año + 2 + secuencia: `202721` es el verano 2027. Lo comparten los tres centros (C238). En TEST 2026 fue año + 5 (`202651`, `202654`, `202656`; ADR-005, reemplazado).
- **Parte de periodo:** un grupo dentro del periodo, con sus fechas (`I01`…, `X01`…, `P01`…).

En Banner se arma con STVACYR (años), STVTRMT (tipos de periodo), STVPTRM (partes) y STVTERM (periodos), y se habilita en SOATERM (instructivo 1.1.1, diap. 13 a 23; 1.1.2). Paso a paso con capturas: `centros/comun/diagramas/01-capacidad-1-periodo-202721/`.

### ¿Cómo se codifica un periodo de los centros?
Tiene 6 dígitos: **año (4) + nivel (1) + secuencia (1)** (instructivo 1.1.1, diap. 12).
- Desde 2027, el nivel de los centros es **2**: `202721` es el verano 2027 (C238, ADR-026). «41» es pregrado de verano (`202741`).
- Secuencia **1** = verano. En TEST, el semestre I 2027 de los centros es `202724`; falta confirmarlo para producción, igual que el semestre II (U56).
- En TEST 2026 el nivel era **5**: 2026-0 = `202651`, 2026-I = `202654` y 2026-II = `202656` (C04, C45, ADR-005, reemplazado).

### ¿Qué periodos usan los centros?
- **202721** («Verano 2027 - Cent.Empresarial»): del 01-ENE al 31-MAR-2027. Es el primero de producción y lo comparten los tres centros (C238).
- **202724** («2027-I Centro Empresariales», 01-ABR a 31-JUL-2027) existe en TEST; falta confirmar que sea el de producción (U56).
- En TEST 2026 se usaron 202651, 202654 y 202656. En TEST también quedan 202751 y 202754, de la regla de 2026; no van a producción (ADR-026).

Pregrado usa otros, por ejemplo 202741 (verano) o 202744.

### ¿Cuántos periodos tienen los centros al año?
- En TEST 2026 fueron **tres**: verano (…51), semestre I (…54) y semestre II (…56), como 2026-0, 2026-I y 2026-II de SEUSS (C04, ADR-005).
- En 2027: **202721** (verano) está confirmado; en TEST está 202724 para el semestre I y aún no se conoce el código del semestre II (U56).
- Los grupos de cada mes no son periodos: son **partes de periodo** (ADR-006).
- La duración la da cada periodo en STVTERM: 202721 va de enero a marzo de 2027 (C238). No se habla de «periodos de 3 meses» para SEUSS (S01).

### ¿Quién crea el periodo?
**Registros Académicos**, «como hasta ahora» (C238): crea el código en STVTERM y lo habilita en SOATERM, con sus partes, fechas web y feriados (C06).
- Las partes y sus fechas salen de las mallas de cada jefatura (C238, U58).
- Desde el 24/11/2026 el usuario está asignado a la Capacidad 01 y debe conocer el proceso. Quién hace cada paso además del periodo está por confirmar (U57).
- Después, el centro crea los NRC de sus grupos, cada uno en su parte de periodo (5.3).
- Los tres centros comparten el periodo, así que un cambio afecta a todos (C143).

### ¿Qué es una parte de periodo y para qué sirve?
Es un rango de fechas dentro del periodo. Tiene sus propias fechas de clases, de adición y retiro y de ingreso de notas (1.1.1, diap. 10).

En los centros, **cada grupo es una parte de periodo** (ADR-006). Así se abren cursos cada mes sin crear un periodo por mes. Los códigos están en STVPTRM (C140):
- Idiomas: `IGE` e `I01` a `I12`.
- Computación: `CGE` y `X01` a `X12`.
- Emprendimiento: `EGE` y `P01` a `P12`.

En 202721 se usan `I01` a `I04`, `P01` y `P02`, `X01` a `X03` y la parte `1` (C238). Cada NRC se programa en una parte en SSASECT y toma sus fechas (5.3, diap. 23).

### ¿Qué diferencia hay entre periodo y parte de periodo?
- El **periodo** (por ejemplo `202721`) es el lapso completo. Lo comparten los tres centros y su código se crea en STVTERM.
- La **parte** (por ejemplo `X01`) es un grupo dentro del periodo, con sus fechas: en 202721, X01 va del 04-ENE al 27-FEB-2027, en 8 semanas (C238). Su código se crea en STVPTRM.

Las fechas de cada parte se ponen por periodo en SOATERM (C140). Si un cambio es para un solo grupo, se cambia la parte y no el periodo (C143).

### ¿Qué partes tenía el periodo 202656 en TEST?
Fue un periodo de TEST 2026. Tenía 14 partes (C141):
- Generales: `CGE`, `EGE`, `IGE` y `1`, del 01-AGO al 31-DIC-2026 (16 semanas).
- Idiomas: `I08` a `I12`. Emprendimiento: `P05` y `P06`.
- Computación: `X05` (03-AGO a 30-AGO, 4 semanas), `X06` (07-SEP a 31-OCT, 8) y `X07` (02-NOV a 13-DIC, 6).

Para matricular en una parte también hacen falta sus reglas en SFARSTS: X06 las tiene y X07 no (C154, C156). Las partes de 202721 están en `ref-preguntas-frecuentes-periodo-202721.md`.

### ¿Qué es la parte de periodo X06 y qué fechas tiene?
En TEST 2026 fue una parte de 202656 que usó Computación («Computación Grupo 06»): del **07-SEP al 31-OCT-2026**, 8 semanas. En SFARSTS tiene los estatus DD, DW, RE y RW en esas fechas; la X07 no tiene reglas (C154, C156). Las partes se definen en STVPTRM y sus fechas en SOATERM (C140). 202721 no usa X06.

### ¿A qué periodo pertenece un grupo que empieza en un periodo y termina en el siguiente?
Al periodo de su **fecha de inicio**, no al de su fecha de fin (ADR-005, ADR-026).
- Un grupo que empieza en julio y termina en agosto es del periodo de julio (en TEST 2026, 202654).
- En 202721, I04 (01-FEB a 30-ABR-2027) es de 202721 aunque termina después del 31-MAR; falta saber si Banner lo admite sin problema (E34).
- En TEST 2026, P03 (11-MAR a 17-MAY-2026) era de 202651.

### ¿Los periodos de los centros son los mismos que los de pregrado?
**No.** Los centros usan sus propios periodos: 202721 en el verano 2027; pregrado usa 202741 en el mismo verano (C238). En TEST 2026 también eran distintos (202646, 202744; C162, C199).
- Por eso el correquisito no sirve entre un curso de centro y uno de pregrado: exige el mismo periodo (R22, R24).
- La carga docente de los centros se mide solo en sus periodos (C55).

Ellucian estudia unificar los periodos para usar correquisitos (U51). Eso choca con el ADR-026.

### ¿Qué periodo es el verano 2027 y qué tiene configurado?
Es **202721** («Verano 2027 - Cent.Empresarial»), del 01-ENE al 31-MAR-2027 (C238, ADR-026). En TEST:
- Partes: I01 a I04, P01 y P02, X01 a X03 y 1.
- Inscripción web del 16-NOV-2026 al 14-MAR-2027; acceso docente del 01-ENE al 06-JUN-2027.
- Inscripción permitida y con plan requerido; NRC desde 10012.

El detalle está en `ref-preguntas-frecuentes-periodo-202721.md`. 202751, que se vio en 2026 (C45), sigue en TEST pero no va a producción.
