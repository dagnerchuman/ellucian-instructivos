# Lo que dice Ellucian (con cita)

Todas las citas se verificaron con `scripts/buscar_instructivos.py`. Formato: instructivo, diapositiva. Úsalas en la columna «En Ellucian».

## Horas de clase y carga docente
- **SIATERM, factor de duración:** «la equivalencia de minutos para la hora académica. En este caso se dice que la hora de clase equivale a 50 minutos». Hay **un solo valor por periodo**. *(5.2 Carga de trabajo docente, diap. 12)*
- **SIATERM, factor FTE:** «cada 50 horas equivalen a 1 FTE». Si se deja vacío, no hay análisis por FTE en SIAASGN. *(5.2, diap. 12)*
- **SSASECT:** «según las horas que se cargan en el horario de cada sesión, el sistema muestra el cálculo automático de las horas por semana… se basa en una hora académica definida en SIATERM». *(5.3 Oferta horaria, diap. 30)*
- El horario se registra con hora de inicio y fin (formato 24 h) y días de la semana. También puede tomarse de los módulos predefinidos en STVMEET. *(5.3, diap. 29 y 31)*
- **Consecuencia:** SEUSS usa 45 min de día y 50 min de noche; Ellucian permite un solo factor por periodo. Un solo valor no cuadra con los dos turnos:
  - con 50: 90 min de día dan 1,8 horas y no 2;
  - con 45: 100 min de noche dan 2,2 horas y no 2.
  - **Duda E01.**
- No aparece un campo para una hora de 60 minutos. **Duda E03.**

### Regla de carga (SIAFLRT) y regla de contrato (SIAFLCT): dos formas de medir (R19)
- **Por regla de carga de trabajo:**
  - es el tipo de asignación: docente, investigador, pasante, en comisión administrativa;
  - una por docente en SIAINST; sus rangos van en **SIAFLRT** por periodo;
  - se analiza en **SIAASGN**, con todos los NRC del docente. *(5.2 Carga de trabajo, diap. 7, 16 a 19 y 21 a 27)*
- **Por contrato:**
  - es el tipo de contrato: tiempo completo, tiempo parcial, por horas, honorarios;
  - va en el bloque «Contrato de docente» de SIAINST, con su «Regla». Un docente puede tener **varios contratos**, uno «predefinido» *(5.2 Información de docentes, diap. 19)*;
  - sus rangos van en **SIAFLCT** por periodo y tipo de contrato; los periodos que cuentan van en SIAFCTR;
  - se analiza en **SIACONA**. *(diap. 29 a 34 y 36 a 42)*
- **Cada NRC tributa a un contrato:** campo «Tipo de contrato» en SIAASGN. Así se separa la carga de un docente con más de un contrato. *(diap. 24, 25 y 38)*
- **El instructivo no las hace excluyentes:** «de igual forma, la evaluación… puede ser realizada en función al tipo de contrato». *(diap. 43)* Si se usan las dos, o solo una, lo decide la USS (U28; a Ellucian, E20).
- **Rangos:** los de «Carga de trabajo» (educativa, no educativa, total y FTE) se usan para el docente a tiempo completo o de planta. Los de horas crédito y horas de contacto sirven para todos. *(diap. 18, 19, 31 y 32)*
- **FTE:** el factor FTE de SIATERM es uno por periodo; en el ejemplo, 50 horas = 1 FTE. *(diap. 12)* En Centros, los especialistas (`ES`) van a tiempo completo con 48 horas, incluidas sus funciones administrativas, y los facilitadores (`FC`) a tiempo parcial, de 14 a 23 horas (C54, C56). Pregrado queda fuera porque está en otros periodos (C55). Como el factor FTE es por periodo, en los periodos de Centros podría ir en 48 (ADR-020, propuesto; E20).

## Docentes en el NRC
- «Un NRC puede tener uno o más docentes… pudiendo haber simultáneamente dos o tres docentes, pero siempre definiendo uno de ellos como el docente **principal**». *(6.2.1 Asignar docentes, diap. 21)*
- Cada docente tiene su % de responsabilidad, su % de sesión y un «indicador de principal» (solo uno). *(6.2.1, diap. 19)*
- Si hay más de un docente, cada sesión lleva un indicador distinto (01, 02, 03). *(5.3, diap. 29)*
- **Cruce de horario:** Banner impide asignar al docente, salvo que se marque el **indicador de sobrepaso**. *(6.2.1, diap. 19 y 20)*
- Un docente puede estar en varios NRC; su carga se ve en **SIAASGN** (5.2).
- SLQMEET consulta salones disponibles y SIAFAVL la disponibilidad del docente. *(6.2.1 Espacios físicos y Docentes)*

## Prerrequisitos, exámenes y sobrepasos
- «La inscripción de un curso puede estar condicionada por una o más asignaturas que deben haber sido cursadas y/o **aprobadas** antes de inscribirlos». *(1.1.5, diap. 5)*
- «**Examen de curso**: elemento que no es un curso pero que se constituye como prerequisito de una asignatura. Por ejemplo: **suficiencia en idioma**». *(1.1.5, diap. 8)*
- **SCAPREQ** (prerrequisitos y puntajes de examen del catálogo) combina:
  - código de examen con puntaje;
  - curso con **calificación mínima**;
  - «Y/O» y paréntesis. *(1.1.5, diap. 18 y 19)*
- **SSAPREQ** (prerrequisitos del NRC): el NRC hereda lo de SCAPREQ y puede ajustarse. Ejemplo del instructivo: «el estudiante debe haber aprobado ACCT 0110 o ACC0 0400». *(5.3, diap. 41 y 42)*
- **SOATERM** (Control de periodo), pestaña «Verificación de errores de inscripción»: «Prerrequisitos: en la inscripción se valida que el estudiante no inscriba cursos o NRC sin haber cumplido los prerrequisitos». Las opciones son **Fatal** o No verificar. *(5.4 Inscripción por backoffice, diap. 14 y 15)*
  - Fatal = no puede inscribir; Alerta = inscribe con advertencia; No verificar. *(5.4 Sobrepasos, diap. 10)*
  - SFAREGS muestra el error en el campo «Mensaje» del NRC. *(5.4 Sobrepasos, diap. 37)*
- **SOATERM, casilla «En progreso»:** si se marca, el curso que se está llevando cuenta como completo para el prerrequisito. «Una vez que un curso es calificado, ya no es considerado en progreso, y luego es verificado contra las reglas en SSAPREQ». *(1.1.2, diap. 18 y 19)* Importa en los grupos seguidos de Inglés (duda E13).
- **Proyección:** SFPPROJ tiene el parámetro «¿Verif de prerrequisito? Y/N». *(5.4 Proyección, diap. 34)*
- **SOATEST** (puntajes de examen del estudiante): código, puntaje y fecha del examen. *(3.2.2, diap. 14)* Los códigos de examen están en STVTESC.
- **SFAROVR** (permisos de sobrepaso de inscripción): permite inscribir a pesar de un error Fatal (prerrequisito, horas, nivel, programa…). Se da por NRC o por materia-curso. *(5.4 Sobrepasos, diap. 19 a 21 y 42)*
- **Límite de repetición:** SOATERM puede controlar cuántas veces se repite un curso, según el catálogo. *(5.4 Inscripción por backoffice, diap. 17)*
- **Inglés, desaprueba BASIC I** (SEUSS: no pasa, salvo con examen de suficiencia; ver C11):
  - Banner hace **lo mismo** con el prerrequisito «BASIC I aprobado **o** examen» y la verificación en Fatal.
  - Sin examen: error y no se inscribe. Con puntaje en SOATEST: se inscribe.
  - El único camino distinto es un sobrepaso (SFAROVR): definir quién lo da (U10).
  - Dudas: E04 (cómo queda BASIC I en CAPP) y E13 («En progreso»).

## Ligas: NRC del mismo curso que se matriculan juntos (R18)
- **Qué son:** si un curso tiene más de un tipo de horario en SCACRSE (por ejemplo, Teoría y Práctica), sus NRC se unen con **ligas** para que el alumno los matricule juntos. En Inglés: el NRC teórico + el club de conversación (C52, ADR-019). *(5.3_4.1.4.1.9 Crear Ligas, diap. 9 y 11)*
- **Liga principal:** el NRC del tipo de horario principal (la teoría). **Liga secundaria:** el de práctica, laboratorio o taller. *(diap. 9)*
- **Créditos y cobro:**
  - el principal va con las horas crédito del curso, «Calificable» marcado y sin «Dispensa de colegiatura y cuotas»;
  - el secundario va con **0 horas crédito**, sin «Calificable» y con «Dispensa de colegiatura y cuotas» marcada. *(diap. 12)*
- **SSASECT:** pestaña «Información de sección de curso», bloque «Indicadores de clase», campo **«Identificador de liga»** (2 caracteres que recuerden el tipo de horario: `TE` Teoría, `PR` Práctica). *(diap. 14 y 15)*
- **SSADETL:** pestaña «Correquisitos y ligas de sección», campo **«Conector de liga»**: en cada NRC va la liga del otro. *(diap. 16 a 18; 5.3_4.1.4.1.6, diap. 36)*
- **Escenarios:**
  - uno a muchos: un teórico con varios clubes a elegir;
  - muchos a muchos sin restricción;
  - muchos a muchos con restricción: cada teórico con su club. *(diap. 20 a 22)*
- **Matrícula:**
  - SOATERM tiene la verificación «Ligas», en Fatal o No verificar *(5.4_4.1.4.1.12, diap. 15)*;
  - el sobrepaso es la casilla «Enlaces» de SFAROVR *(5.4_4.1.4.1.15, diap. 21)*;
  - en el Autoservicio el alumno ve las «Secciones ligadas» *(5.3_4.1.4.1.9, diap. 24)*.

## Notas
1. **Escalas** en SHAGRDE y SHAGSCH (7.1.3).
2. **Plan de evaluación por NRC** en **SHAGCOM**, que carga Registros Académicos. *(7.1.4, diap. 5 y 44 a 54)*
   - Cada componente tiene peso %, subcomponentes y escala.
   - Casilla «debe ser aprobado para que el estudiante apruebe la asignatura». *(7.1.4, diap. 47)*
   - Solo pasan a la historia las notas finales. *(7.1.4, diap. 48)*
3. **Fechas:** SOATERM define las fechas en que el docente accede al autoservicio y carga notas. *(7.1.4, diap. 17)* Además, el perfil del docente necesita el proceso ENTERGRADES (7.1.4, diap. 20).
4. **El docente registra** en autoservicio (7.1.4). **El estudiante consulta** según SOATERM; se puede restringir por NRC en SSAWSEC (7.1.5).
5. **Correcciones:**
   - por backoffice en SFASLST (7.1.6);
   - si ya pasó a historia, en SHATCKN;
   - incompletas en SHAGRDE y SHRCINC (7.1.7);
   - extemporáneas, con fechas de reestimación en SHAEGBC (7.1.8).
6. **Cierre:** SHRROLL pasa las notas a la historia académica; luego se ejecuta el CAPP masivo con SMRBCMP (7.1.9).

## Asistencia
- El docente toma asistencia por NRC y sesión (7.1.1 y 7.1.2).
- Puede **decidir la aprobación**: componente **ATTRGRD** en el plan de evaluación, con peso 0, «Debe pasar» y su propia escala. *(7.1.0, diap. 29; 7.1.4, diap. 55)*
- Ejemplo del instructivo: mínimo 70%; de 0 a 69,99% da la nota **INH** (desaprobado). *(7.1.0, diap. 21 a 23)*
- Configuración técnica:
  - GORICCR: ATTENDANCE_TRACKING / ENABLE.GRADEBOOK.UPDATE.
  - GORRSQL: regla SQL del porcentaje.
  - GTVSQPA y GORSQPA: parámetros.
  - STVGCHG: razón de cambio. *(7.1.0)*

## Aula virtual (LMS)
- El campo **Socio de integración** de SSASECT vincula el NRC al LMS. Los códigos están en GTVINTP y las reglas en GORINTG. *(6.2.4, diap. 10, 11 y 14)*
- Está documentado que los datos del NRC **van** al aula virtual. **No** está documentado que las notas **regresen** a Banner. **Duda E02.**

## Egreso (por qué los centros importan a pregrado)
- «Egresado: estudiante que ha cumplido todos los requerimientos académicos de la malla curricular, incluido los requisitos de **idiomas, computación y emprendimiento**». *(08_4.1.4.1.5, diap. 13)*
- El cambio masivo a **EG (Egresado)** se hace cuando el estudiante «cumplió con su malla curricular, idiomas, emprendimiento y computación». *(08_4.4.4.1.5, diap. 42)*
- Requisitos que no son cursos (cocurriculares): capacidad 8.3.

## Programación del NRC (otros)
- **Cupos reservados:** en SSASECT, pestaña Lugares reservados. Se empieza con una regla «nula» obligatoria; luego se agregan cupos por nivel, campus, programa, atributo o cohorte. *(5.3, diap. 28)*
- **Secciones ligadas:** teoría y laboratorio que se llevan juntas.
- **Lista cruzada:** cursos distintos dictados juntos (SSAXLST). *(5.3, diap. 12; 5.3_4.1.4.1.8)*
- La **parte de periodo** del NRC sale de SOATERM. Hay que verificar horas crédito y horas de cobro. *(5.3, diap. 23)*

## CAPP y proyección (resumen)
- **Configuración:** SMAPROG (programa), SMAAREA (áreas y reglas), SMADFLT (ONLINE/BATCH), STVCPRT / SMACPRT / SHAGPAR / SMAWCRL.
- **Ejecución:** SMARQCM (individual), SMRBCMP (masivo). **Resultado:** SMICRLT.
- **Proyección:** SFPPROJ, SFAPROJ, SFALPROJ. Con «restringir a cursos proyectados» en SOATERM, solo se inscribe lo proyectado. *(7.2.4; 5.4_4.1.4.1.6)*

## Reemplazo de un docente a mitad del curso (reunión 28/09)
1. **SPAIDEN**, pestaña Biográfica: fecha de fallecimiento y casilla «Fallecido». *(5.1.1, diap. 40)*
2. **SIAINST:** estatus del docente (códigos en STVFCST). *(5.2 Información de docentes, diap. 10 y 18)*
3. **SSASECT:** asignar al nuevo docente en la sesión del NRC, marcarlo como principal y ajustar el % de responsabilidad y de sesión. *(6.2.1, diap. 19 y 21)*
4. **Notas:** el nuevo docente debe estar asignado al NRC. Si la regla PRIMINSTR es «Y», solo el principal registra notas; con «N», todos los docentes asignados. *(7.1.4, diap. 21 y 24)*
5. **Carga:** se ve en SIAASGN: horas semanales × semanas del NRC. *(5.2 Carga, diap. 18)*
- **No documentado:** si el docente anterior se deja o se elimina, qué pasa con sus notas y con la encuesta de evaluación docente (duda E14).

## Planes curriculares: orden de dependencias (reunión 28/09)
- **El orden:** cursos en SCACRSE › malla y versión en SMAPROG y SMAAREA › equivalencias en SCADETL o SMAAREA › regla curricular (SOACURR) activa para admisiones, gestión del alumno, historia académica y evaluación de grado › admisión › NRC › tutores y CAPP.
- **Citas:**
  - Sin cursos no hay NRC: 5.3, diap. 53.
  - Los cursos nuevos se crean antes de cambiar las áreas; un área nueva, antes de cambiar el programa: 1.3.1, diap. 5.
  - Los cursos equivalentes deben existir antes; Ellucian recomienda cargar las equivalencias por malla: 1.2.3, diap. 6 y 15.
  - La admisión trae la regla de currículo del programa: 1.1.3, diap. 34; 3.2.1, diap. 15 y 25.

## Tutores o asesores (capacidad 9)
- **Habilitar:** SIAINST, casilla Asesor, vigente desde un periodo. Tipos de asesor en STVADVR. *(9.1.1, diap. 20 y 24)*
- **Asignar:**
  - individual en SGAADVR (desde un periodo);
  - masivo con reglas en SGAAVRL y el proceso SGPADVA (por programa, cohorte, atributo, deporte…). *(9.1.1, diap. 27 y 30 a 35)*
- **Acceso en el autoservicio:** reglas de SOAFACS (proceso disponible, todos los accesos, NIP) y perfil del alumno para asesoría. *(9.1.1, diap. 9, 10 y 36)*
- **El asesor en asistencia y notas:** puede actuar si tiene una relación de asesor con el alumno en SGAADVR. *(7.1.1, diap. 15)*

## Quejas, denuncias y sanciones (casuísticas del 28/09)
- **Queja como solicitud de servicio:**
  - El estudiante la presenta por autoservicio (categoría y servicio) y agrega comentarios mientras no esté cerrada. *(4.3.2, diap. 10 y 12)*
  - El área la atiende en SVASVPR: estado, fecha estimada, comentarios internos que el estudiante no ve. *(4.3.2, diap. 18 y 20)*
  - Configuración:
    - SVVSRCA: categorías;
    - SVVSRVC: servicios;
    - SVVSRVS: estados;
    - SVVCHNL: canal;
    - SVVRQST: tipos;
    - STVWSSO: opciones;
    - SVVSRCT: controles;
    - STVRADM: roles;
    - SVARSRV: reglas (tipo de persona, rol, retención que lo impide);
    - SVASRAD: datos extra.
    *(4.3.1, diap. 10 a 25)*
- **Denuncia ante Gobierno de Personas:** Banner Student no la genera ni la envía por sí solo. Los procesos de personal no están en los instructivos (dudas E17 y E18).
- **Evaluación docente:** es una encuesta de los estudiantes por NRC (SVPTESS, SVPSTSS) cuyos resultados se ven en el autoservicio. Da indicadores; no es una queja. *(6.2.5, diap. 5 y 68)*
- **Seguimiento del estudiante:**
  - SPACMNT: comentarios por tipo y fecha; la USS no tiene tipos definidos. *(5.1.1, diap. 46)*
  - Estado académico por promedio y horas, con regla de dificultad académica. *(7.2.3, diap. 5 y 19)*
  - Comunicaciones masivas a una población con BCM. *(10.2, diap. 102)*
  - No hay alertas tempranas en los instructivos (duda E19).
- **Sanción disciplinaria del estudiante:**
  - Estado del plan en SGASTDN: «Suspendido» (temporal) o «Expulsado» (definitivo); ninguno permite inscripción. *(3.2.7, diap. 9 y 42)*
  - Retención en SOAHOLD (tipos en STVHLDD; por plan en SGASTHD): no se borra, se le pone fecha de fin. *(5.2.1, diap. 19; 5.2.2, diap. 24)*
  - Puede impedir presentar solicitudes de servicio. *(4.3.1, diap. 21)*
  - Para egresar no debe tener retenciones. *(08_4.4.4.1.5, diap. 42)*

