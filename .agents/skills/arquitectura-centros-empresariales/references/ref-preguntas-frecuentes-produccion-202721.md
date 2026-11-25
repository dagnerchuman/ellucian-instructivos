# Preguntas frecuentes de operación: NRC de producción del verano 202721

Respuestas cortas para el asistente IA y para cualquier agente, tomadas de la hoja «NRC VERANO 202721 CENTROS EMPRESARIALES» tal como estaba el 25/11/2026 (C242). El usuario la sigue llenando mientras se carga la data de producción, así que es una foto de ese día. Las pestañas «NRC PROD-…» son lo que se carga; las «PROPUESTA…», lo que todavía se propone. Cada pregunta es un fragmento de la base del asistente. Si la respuesta no está aquí ni en el registro, se dice «No lo sé» (ruta de escape).

Tema de este archivo: los NRC, cursos, códigos, partes y horarios de producción en 202721. Las fórmulas de calificación están en `ref-preguntas-frecuentes-formulas-de-calificacion.md`; el periodo 202721 tal como está en TEST, en `ref-preguntas-frecuentes-periodo-202721.md`. Estos datos todavía no pasan a `centros/<centro>/datos.json`: el usuario dirá cuándo.

### ¿Qué NRC hay en producción en 202721?
Según la hoja de NRC de producción del 25/11/2026 (C242), se cargan **23 NRC** en el periodo `202721`, del `1002` al `1025`, en una sola numeración para los tres centros (el periodo es uno solo, ADR-026):
- **Emprendimiento:** 15 NRC, parte `P02`: `1002`, `1006`, `1009` y `1010` (Emprendimiento I); `1011` a `1014` y `1016` (II); `1017` a `1021` y `1023` (III).
- **Computación:** 4 NRC, parte `X02`: `1003` y `1007` (Computación II); `1008` y `1024` (Computación III).
- **Idiomas:** 4 NRC de Basic I, parte `I03`: `1004`, `1015`, `1022` y `1025`; la sección I todavía no tiene NRC.

La hoja aún no trae docentes, y todos los NRC cobran («COBRA: SI»). Emprendimiento y Computación van en el aula virtual `SAUVIR` / `SALA-VIRT`; para Idiomas la hoja no trae aula.

### ¿Qué NRC y horarios tiene Emprendimiento en 202721?
Programa `MMEMM01`, departamento `EMEM`, parte `P02`, aula `SAUVIR` / `SALA-VIRT` y HT 4 (C242). Todos son de dos días por semana, 2 horas cada día:
- **Emprendimiento I** (`ESGE 00499`, regla `MM01-01`): `1002` sección E, Lun y Jue 15:30–17:30 · `1006` F, Mar y Vie 19:00–21:00 · `1009` G, Mié y Sáb 09:00–11:00 · `1010` H, Mar y Vie 16:00–18:00.
- **Emprendimiento II** (`ESGE 00500`, regla `MM01-02`): `1011` F, Lun y Jue 09:00–11:00 · `1012` G, Mar y Vie 15:30–17:30 · `1013` H, Mié y Vie 19:00–21:00 · `1014` I, Mar y Sáb 09:00–11:00 · `1016` J, Lun y Vie 16:00–18:00.
- **Emprendimiento III** (`ESGE 00501`, regla `MM01-03`): `1017` G, Lun y Jue 19:00–21:00 · `1018` H, Mar y Vie 15:30–17:30 · `1019` I, Mié y Vie 19:00–21:00 · `1020` J, Mar y Sáb 09:00–11:00 · `1021` K, Lun y Vie 16:00–18:00 · `1023` L, Mar y Jue 09:00–11:00.

### ¿Qué NRC y horarios tiene Computación en 202721?
Programa `CMEMC13`, departamento `EMCI`, parte `X02`, aula `SAUVIR` / `SALA-VIRT`, HT 9 y HP 0 (C242):
- **Computación II** (`ESEP 05023`, regla `MC13-03`): `1003` sección B, Lun, Mié y Vie 19:00–22:00 · `1007` C, Mar, Jue y Sáb 19:00–22:00.
- **Computación III** (`ESEP 05024`, regla `MC13-04`): `1008` C, Lun, Mié y Vie 19:00–22:00 · `1024` D, Mar, Jue y Sáb 08:00–11:00.

**Propuesta, por confirmar** (pestaña «PROPUESTA NRC PROD-COMPUTACION», 20 filas):
- Computación II y III con `ESEP 06629` y `06630` (U59). El `1003` serviría también a `CMEMC08` y `CMEMC09`; el `1007`, a `CMEMC12`; y una sección D nueva de Computación II, a `CMEMC11`.
- ProTech XP para `CMEMC38`, `CMEMC39`, `CMEMC40` y `CMEMC44`, en `X02`: Ofimática Word 365 (`ESEC 02492`, secciones A, B y C), Ofimática Excel 365 (`ESEC 02493`, A, B y C) y Diseño con Canva (`ESEC 02494`, A, B, C y D).
- Microsoft Excel Asociado (`ESEC 02496`, para `CMEMC38` a `CMEMC44`), AutoCAD 2D (`ESEC 02497`) y AutoCAD 3D (`ESEC 02499`), estos dos para `CMEMC41`, `CMEMC42` y `CMEMC43`: una sección A cada uno y la parte por definir (U60).

### ¿Qué NRC y horarios tiene Idiomas en 202721?
Programa `IMEMI03`, departamento `EMID`, HT 8 (C242). En la pestaña «NRC PROD-IDIOMAS» solo está Basic I (`ESEP 06083`, regla `MI03-01`, parte `I03`):
- `1004` sección E, Lun, Mié y Vie 14:00–16:00 · `1015` F, Lun y Vie 16:30–19:30 · `1022` G, Sáb y Dom 14:00–17:00 · `1025` H, Lun, Mar y Jue 16:00–18:00.
- La sección I todavía no tiene NRC; la propuesta le pone Lun, Mié y Vie 19:00–21:00.

La hoja no trae aula para Idiomas.

**Propuesta, por confirmar:** 70 secciones (pestaña «PROPUESTA NRC PROD-IDIOMAS»). En `I03`: Basic I (`ESEP 06083`, 10 secciones), Basic II (`06084`, 15), Intermediate I (`06086`, 10) e Intermediate II (`06087`, 10). En `I04`: Basic III (`06085`, 13) e Intermediate III (`06088`, 12). Los básicos van en la regla `MI03-01`; los intermedios, en `MI03-02`.

### ¿Qué códigos de curso nuevos se usan en producción y cuáles eran los de TEST?
En producción no se usan los cursos de TEST (C242):

| Curso | En TEST | En producción 202721 |
|---|---|---|
| Emprendimiento I, II y III | `ESGE 00117`, `00118` y `00119` (HT 1, HP 2) | `ESGE 00499`, `00500` y `00501` (HT 4) |
| Basic I, II y III | `ESEP 02456`, `02457` y `02458` (HT 4, HP 3) | `ESEP 06083`, `06084` y `06085` (HT 8) |
| Intermediate I, II y III | `ESEP 02693`, `02721` y `02997` (HT 4, HP 3) | `ESEP 06086`, `06087` y `06088` (HT 8) |
| Computación II y III | No se vieron | `ESEP 05023` y `05024` (HT 9, HP 0); la propuesta dice `06629` y `06630` (U59) |
| Ofimática Word 365 | `ESEC 00650` y `00678` | `ESEC 02492` (propuesta) |
| Ofimática Excel 365 | `ESEC 00679` | `ESEC 02493` (propuesta) |
| Diseño con Canva | `ESEC 00680` | `ESEC 02494` (propuesta) |
| Microsoft Excel Asociado | `ESEC 00682` | `ESEC 02496` (propuesta) |
| AutoCAD 2D y 3D | No se vieron | `ESEC 02497` y `02499` (propuesta) |

Computación II y III van con la materia `ESEP`, aunque son del departamento `EMCI`; en TEST, Computación usaba `ESEC` (U18).

### ¿Qué parte de periodo usa cada centro en 202721?
En la hoja de producción (C242):
- **Idiomas:** `I03` para Basic I y II e Intermediate I y II; `I04` para Basic III e Intermediate III. En la pestaña de producción solo está Basic I; lo demás sale de la propuesta.
- **Computación:** `X02`. La propuesta deja Excel Asociado y AutoCAD sin parte (U60).
- **Emprendimiento:** `P02`.

En TEST, 202721 tiene las partes `I01` a `I04`, `X01` a `X03`, `P01` y `P02` (C238). Faltan las fechas de cada parte (U58).
