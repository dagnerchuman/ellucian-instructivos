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

## Docentes en el NRC
- «Un NRC puede tener uno o más docentes… pudiendo haber simultáneamente dos o tres docentes, pero siempre definiendo uno de ellos como el docente **principal**». *(6.2.1 Asignar docentes, diap. 21)*
- Cada docente tiene su % de responsabilidad, su % de sesión y un «indicador de principal» (solo uno). *(6.2.1, diap. 19)*
- Si hay más de un docente, cada sesión lleva un indicador distinto (01, 02, 03). *(5.3, diap. 29)*
- **Cruce de horario:** Banner impide asignar al docente, salvo que se marque el **indicador de sobrepaso**. *(6.2.1, diap. 19 y 20)*
- Un docente puede estar en varios NRC; su carga se ve en **SIAASGN** (5.2).
- SLQMEET consulta salones disponibles y SIAFAVL la disponibilidad del docente. *(6.2.1 Espacios físicos y Docentes)*

## Prerrequisitos, exámenes y sobrepasos
- «**Examen de curso**: elemento que no es un curso pero que se constituye como prerequisito de una asignatura. Por ejemplo: **suficiencia en idioma**». *(1.1.5, diap. 8)*
- **SCAPREQ** (catálogo) combina código de examen con puntaje, curso con calificación mínima, «Y/O» y paréntesis. *(1.1.5, diap. 18 y 19)*
  - En el NRC se ve y se ajusta en **SSAPREQ** (5.3).
- **SOATEST:** registra el código, el puntaje y la fecha del examen. *(3.2.2, diap. 14)* Los códigos de examen están en STVTESC.
- **SFAROVR:** permisos de sobrepaso por periodo (códigos en STVROVR). Pueden saltarse restricciones de nivel, prerrequisitos, horas, programa, correquisitos, ligas, duplicados, entre otras. *(5.4 Sobrepasos, diap. 19 a 22)*
- **Consecuencia para Inglés (desaprueba BASIC I):**
  - A) Repite BASIC I.
  - B) Rinde un examen de suficiencia: el puntaje se registra en SOATEST y se configura «BASIC I **o** examen» en SCAPREQ. Banner lo soporta.
  - C) Pase automático: no está en los instructivos; solo con sobrepaso o quitando el prerrequisito. **Dudas U01 y E04.**

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
