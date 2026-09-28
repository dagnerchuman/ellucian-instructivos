# Registro de preguntas, dudas y decisiones

Última actualización: **28/09/2026** (cierre de la sesión: el usuario pasa a trabajar en Antigravity IDE). Alcance: Centros Empresariales de la USS (Idiomas/Inglés, Computación/Informática, Emprendimiento) en Ellucian Banner.

---

## 1. Confirmado por el usuario
| ID | Qué | Fecha | Fuente |
|---|---|---|---|
| C01 | El alcance es solo Centros Empresariales: **Idiomas, Informática (Computación) y Emprendimiento**. «Somos de idiomas, informática y emprendimiento». | sep 2026 | Usuario |
| C02 | El **catálogo de cursos y programas lo diseña el centro, cada mes**. | sep 2026 | Usuario |
| C03 | Hoy la **carga docente se hace en Excel**; debe pasar al sistema, como indican los instructivos. | sep 2026 | Usuario |
| C04 | Periodos: **SEUSS 2026-0 (verano), 2026-I y 2026-II = 202651, 202654 y 202656**. El verano 2027 = 202751. | 26/09/2026 | Notas del Zoom |
| C05 | Hora de clase: **45 min de día y 50 min de noche**; en los dos casos cuenta como 1 hora. Hay además una hora «presencial» de **60 min**, como la hora de trabajo. | 26/09/2026 | Usuario (ver U09 por los nombres) |
| C06 | Flujo del usuario (7 pasos): periodos y carga lectiva (RA) → admisión (postulantes CEPRE → estudiantes) → tutoría (RA) → NRC = secciones, las registran las escuelas → jefatura → docente → finanzas. | sep 2026 | Usuario |
| C07 | Flujo de la hoja del Zoom: periodos → planes curriculares → carga lectiva y RA (secciones = NRC, horarios) → matrícula → enseñanza-aprendizaje (notas, asistencia). | 26/09/2026 | Notas del Zoom |
| C08 | Pruebas que pidieron: periodos → generación de mallas y programas → creación de NRC → matrículas (backoffice y autoservicio). | 26/09/2026 | Notas del Zoom |
| C09 | En Ellucian las **secciones = NRC**. | 26/09/2026 | Notas del Zoom |
| C10 | Lo que anota el usuario del Zoom es **lo que se hace hoy en SEUSS**; lo que se quiere es confirmar cómo será en Ellucian. | 26/09/2026 | Usuario |
| C11 | **Inglés en SEUSS:** si desaprueba BASIC I, sale desaprobado y **no puede pasar a BASIC II**. La única forma de pasar sin aprobarlo es rendir un **examen de suficiencia**. Lo que se quiere confirmar es si Ellucian tiene un requisito que lo bloquee, o si permite pasar con el examen. | 26/09/2026 | Usuario (corrigió el ejemplo I-4) |
| C12 | **Formato:** toda sigla o término entre paréntesis debe llevar su significado, por ejemplo «NRC (Número de Referencia de Curso)». | 26/09/2026 | Usuario |
| C13 | Reunión del 28/09 (alcance general de la USS, no solo los centros): (a) en un grupo de la maestría en Educación falleció el docente a mitad del curso: se reemplaza, y debe estar en las pruebas integrales; (b) hay programas en rediseño sin equivalencias, sin cursos y sin nueva versión; (c) posgrado envió su plan pero los cursos no están cargados en Registros Académicos, lo que pone en riesgo 20271; (d) ofrecer algo sin información impacta desde la capacidad 3 (admisión) y todo termina en Registros Académicos; (e) ¿cómo trabajarán los tutores? | 28/09/2026 | Usuario |
| C14 | Hay que sumar **casuísticas** a las pruebas integrales, además de la muestra de estudiantes: docente separado («hasta aquí no puede dictar clases»); docente que no gestiona estrategias para un estudiante con problemas; estudiante que se queja de desprecio del docente; denuncia ante Gobierno de Personas (¿lo genera Ellucian?). | 28/09/2026 | Usuario |
| C15 | **Práctica en TEST (28/09):** el usuario creó un NRC de **ESEC 00650 «Ofimática Word 365»** en el periodo **202656**, sección **B**. En TEST existen el periodo 202656 y el curso en el catálogo. En SMAAREA, la regla **ECOM-01 «Computación I»** (área MC38-01 «Ciclo I») se cumple con uno de los cursos ESEC 00650 a 00657. Detalle en `arquitectura-centros-empresariales/references/guia-crear-nrc.md`. | 28/09/2026 | Capturas del usuario |

## 2. Resuelto con los instructivos
Detalle y citas en `arquitectura-centros-empresariales/references/reglas-ellucian.md`.

| ID | Pregunta | Respuesta | Cita |
|---|---|---|---|
| R01 | ¿Varios docentes en un curso? | **Sí**: 2 o 3 por NRC, uno **principal**, con % de responsabilidad y de sesión. | 6.2.1 Asignar docentes, diap. 19 y 21 |
| R02 | ¿Un docente en varios cursos? | **Sí**; su carga se ve en SIAASGN. Si hay cruce de horario, Banner lo impide salvo con el indicador de sobrepaso. | 6.2.1, diap. 19 y 20; 5.2 |
| R03 | ¿El examen de suficiencia puede ser requisito? | **Sí**: «examen de curso, por ejemplo suficiencia en idioma» en SCAPREQ, con puntaje, curso y Y/O. El puntaje se registra en SOATEST. | 1.1.5, diap. 8 y 18; 3.2.2, diap. 14 |
| R04 | ¿Cómo se validan las notas? | Plan de evaluación (SHAGCOM) → fechas (SOATERM) → docente por autoservicio → correcciones (SFASLST, SHATCKN) → cierre (SHRROLL) → CAPP masivo. | 7.1.3 a 7.1.9 |
| R05 | ¿La asistencia cuenta para aprobar? | Puede contar: componente ATTRGRD con peso 0 y «debe pasar». El ejemplo del instructivo usa 70% (debajo, nota INH). | 7.1.0, diap. 21 a 29 |
| R06 | ¿Cómo se vincula el aula virtual? | Campo «Socio de integración» en SSASECT (GTVINTP, GORINTG); los datos del NRC **salen** al aula virtual. | 6.2.4, diap. 10 a 14 |
| R07 | ¿Cómo se define la hora académica? | Factor de duración en SIATERM, en minutos, **uno por periodo**; SSASECT calcula las horas por semana con ese valor. | 5.2, diap. 12; 5.3, diap. 30 |
| R08 | ¿Por qué importan los centros a pregrado? | Idiomas, computación y emprendimiento son requisitos para ser **egresado** (EG). | 08_4.1.4.1.5, diap. 13; 08_4.4.4.1.5, diap. 42 |
| R09 | ¿Ellucian bloquea BASIC II si BASIC I está desaprobado? | **Sí.** El prerrequisito «BASIC I aprobado **o** examen de suficiencia con puntaje mínimo» va en SCAPREQ y el NRC lo hereda en SSAPREQ. Con la verificación «Prerrequisitos» en **Fatal** (SOATERM), SFAREGS no lo inscribe. Con el puntaje en SOATEST, sí. La proyección (SFPPROJ) con verificación de prerrequisitos tampoco le ofrece BASIC II. Un sobrepaso (SFAROVR) puede saltar la regla. | 1.1.5, diap. 5 y 18; 5.3, diap. 41 y 42; 5.4 backoffice, diap. 14 y 15; 5.4 sobrepasos, diap. 10, 20, 21 y 37; 5.4 proyección, diap. 34; 3.2.2, diap. 14 |
| R10 | ¿Un curso en curso cuenta para el prerrequisito? | Solo si se marca **«En progreso»** en SOATERM: el curso en curso cuenta como completo. Cuando se califica, se revisa contra SSAPREQ. | 1.1.2, diap. 18 y 19 |
| R11 | ¿Cómo se reemplaza a un docente a mitad del curso? | Se registra el fallecimiento en SPAIDEN (fecha y casilla «Fallecido»). Se cambia el estatus en SIAINST (códigos en STVFCST). Se asigna al nuevo docente en SSASECT como principal, con su % de responsabilidad y de sesión. Para registrar notas debe estar asignado al NRC; si PRIMINSTR = Y, solo el principal registra notas. Su carga se ve en SIAASGN. | 5.1.1, diap. 40; 5.2 Información de docentes, diap. 10 y 18; 6.2.1, diap. 19 y 21; 7.1.4, diap. 21 y 24; 5.2 Carga, diap. 18 |
| R12 | ¿Qué pasa si un programa no tiene su plan completo? | Todo depende del orden: cursos en el catálogo (SCACRSE) › malla y versión (SMAPROG, SMAAREA) › equivalencias (SCADETL o SMAAREA) › regla curricular activa para admisiones (SOACURR). Sin cursos no hay NRC (5.3, diap. 53). Los cursos nuevos se crean antes de cambiar las áreas (1.3.1, diap. 5). Los equivalentes deben existir antes (1.2.3, diap. 6 y 15). La admisión trae la regla de currículo del programa (1.1.3, diap. 34; 3.2.1, diap. 15 y 25). | ver citas |
| R13 | ¿Cómo trabajan los tutores? | El docente se marca como asesor en SIAINST (vigente desde un periodo); los tipos de asesor van en STVADVR. Se asigna uno por uno en SGAADVR, o de forma masiva con SGAAVRL y SGPADVA (por programa, cohorte o atributo). Lo que ve en el autoservicio lo define SOAFACS. | 9.1.1, diap. 9, 10, 20, 24, 27 y 30 a 36 |
| R14 | ¿Cómo se registra una queja de un estudiante? | Como **solicitud de servicio**. El estudiante la presenta por autoservicio y agrega comentarios; el área la atiende en SVASVPR con estado, fecha estimada y comentarios internos. Hay que configurar la categoría, el servicio, los estados, los roles y a quién va dirigido. Los instructivos no traen un servicio de queja ya hecho. | 4.3.1, diap. 10 a 25; 4.3.2, diap. 10, 12, 18 y 20 |
| R15 | ¿Ellucian genera la denuncia ante Gobierno de Personas? | **No por sí solo.** Banner Student registra la solicitud y define para quién está disponible; los procesos de personal (investigación, sanción al docente) no están en los instructivos de Banner Student. | 4.3.1, diap. 18, 19 y 22 |
| R16 | Estudiante con dificultades o sancionado | Seguimiento en SPACMNT (sin tipos definidos hoy en la USS); estado académico por promedio y horas (7.2.3); comunicaciones con BCM. Sanción: estado del plan «Suspendido» o «Expulsado» en SGASTDN, más una retención en SOAHOLD (no se borra: se le pone fecha de fin). No hay alertas tempranas en los instructivos. | 5.1.1, diap. 46; 7.2.3, diap. 5 y 19; 3.2.7, diap. 9 y 42; 5.2.1, diap. 19 |

## 3. Dudas abiertas para Ellucian
| ID | Duda | Desde | Origen |
|---|---|---|---|
| E01 | Hora de clase de **45 min (día)** y **50 min (noche)** en el mismo periodo: ¿cómo se configura si SIATERM tiene un solo factor de duración? ¿Se ajustan a mano las horas del NRC en SSASECT? | 26/09 | Notas del Zoom |
| E02 | Aula virtual: ¿las **notas regresan** a Banner? ¿Qué datos salen (NRC, docente, participantes, plan de evaluación)? | 26/09 | Notas del Zoom |
| E03 | Hora de **60 minutos**: si se necesita (carga o pago del docente), ¿dónde se registra? | 26/09 | Usuario |
| E04 | Si un participante pasa a BASIC II con **examen de suficiencia**, ¿cómo queda BASIC I en la historia y en CAPP: pendiente o reconocido? | 26/09 | Ejemplo I-4 |
| E13 | Casilla **«En progreso»** de SOATERM: con grupos seguidos (I04 termina el 31/5 e I06 empieza el 1/6), ¿se marca? Si se marca y luego desaprueba BASIC I, ¿Banner lo retira de BASIC II o se hace a mano? | 26/09 | Instructivo 1.1.2 |
| E14 | Reemplazo de docente: ¿el docente anterior se deja en el NRC con su % (historial y pago) o se elimina? ¿Qué pasa con sus notas ya registradas y con la encuesta de evaluación docente? | 28/09 | Reunión 28/09 |
| E15 | ¿Qué se hace si un programa no tiene su plan completo (cursos, versión, equivalencias) al abrir 20271? | 28/09 | Reunión 28/09 |
| E16 | Tutores: ¿qué ve el tutor en el autoservicio si el programa del estudiante no tiene su malla cargada? | 28/09 | Reunión 28/09 |
| E17 | ¿Las solicitudes de servicio pueden avisar por correo o asignarse a Gobierno de Personas? ¿Hay integración con su sistema? | 28/09 | Casuísticas |
| E18 | ¿Cómo se define quién atiende cada servicio y quién puede ver una queja (confidencialidad)? | 28/09 | Casuísticas |
| E19 | ¿Banner tiene alertas tempranas por faltas o notas bajas, o solo reportes y comunicaciones? | 28/09 | Casuísticas |
| E05 | ¿Los programas de los tres centros tendrán su **malla en CAPP** (SMAPROG, SMAAREA)? Si no, ¿cómo funciona la inscripción proyectada? | 25/09 | PDF «Lo que entiendo» |
| E06 | ¿Se migra la historia de los centros? ¿A qué periodos de Banner van los cursos llevados en SEUSS? | 25/09 | PDF «Lo que entiendo» |
| E07 | ¿Qué incluye la «Carga LD01 con equivalencias»? ¿Tiene cursos de los centros? | 25/09 | Zoom de migración |
| E08 | ¿La muestra de validación incluye participantes de los centros? ¿Cuántos y quién los elige? (propuesta: 16 por centro) | 25/09 | Validación |
| E09 | ¿Quién ejecuta SMARQCM y SFPPROJ en TEST, Ellucian o la USS? ¿Hay accesos? | 25/09 | Validación |
| E10 | ¿El certificado de los centros se registra como grado (SHADEGR)? | 25/09 | Diagrama y validación |
| E11 | ¿Cuándo se define el formato del Issue log? ¿Sirve la propuesta de la planilla? | 25/09 | Validación |
| E12 | ¿Insight puede dar los totales por centro para conciliar con SEUSS? | 25/09 | Validación |

## 4. Dudas abiertas para la USS
| ID | Duda | Desde | Origen |
|---|---|---|---|
| U01 | Examen de suficiencia de Inglés: ¿qué **puntaje mínimo** se exige y quién lo registra en Banner (SOATEST)? La regla ya está confirmada (C11). | 26/09 | Ejemplo I-4 |
| U10 | ¿Quién podrá dar **sobrepasos** de prerrequisito (SFAROVR)? En SEUSS ese camino no existe. | 26/09 | Ejemplo I-4 |
| U11 | Validación contra legado: ¿quién saca de SEUSS los **totales por centro** (TI o Registros Académicos) y con qué **fecha de corte**? Debe ser la misma de la extracción que migró Ellucian, o los totales no cuadrarán. | 28/09 | Pregunta del usuario sobre la validación contra legado |
| U12 | ¿Quién termina los planes en rediseño y el de posgrado (cursos, versión, equivalencias) y con qué fecha límite antes de 20271? | 28/09 | Reunión 28/09 |
| U13 | «20271»: ¿es el primer periodo de 2027 de posgrado? ¿Cuál es su código de 6 dígitos? | 28/09 | Reunión 28/09 |
| U14 | ¿Qué área recibe las quejas contra docentes y cómo se protege al estudiante? ¿Se crea en Banner un servicio de «queja o denuncia» o se atiende fuera? | 28/09 | Casuísticas |
| U15 | ¿Qué tipos de comentario de seguimiento (SPACMNT) usarán los tutores? | 28/09 | Casuísticas |
| U16 | ¿Quién decide separar a un docente y cómo se avisa a Registros Académicos? | 28/09 | Casuísticas |
| U17 | ¿Qué código de **campus** se usa para los NRC de los centros? | 28/09 | SSASECT en TEST |
| U18 | ¿Qué son las escuelas **EM** y **CE** del catálogo? ¿Por qué existen **ESEC 00650** (EM) y **ESEP 00650** (CE) con el mismo número? ¿Cuál programa el Centro de Informática? | 28/09 | SSASECT en TEST |
| U19 | ¿Qué programa es **MC38** y qué significa el nivel **C** en SMAAREA? ¿Esa regla ECOM-01 es el requisito de computación de pregrado? | 28/09 | SMAAREA en TEST |
| U02 | Informática y Emprendimiento: ¿los cursos tienen orden (uno pide aprobar otro) o todos son independientes? | 26/09 | PDF de ejemplos |
| U03 | ¿Qué **asistencia mínima** se exige para aprobar? (el instructivo usa 70% como ejemplo) | 26/09 | PDF de ejemplos |
| U04 | ¿Quién carga el **plan de evaluación** de cada NRC: Registros Académicos (como dice el instructivo) o el centro? | 26/09 | PDF de ejemplos |
| U05 | Nombres reales de los cursos de **Informática y Emprendimiento**, pesos de evaluación y nota aprobatoria. En los PDF son de ejemplo: Excel Básico e Intermedio, Speaking/Writing, pitch final, aprueba con 14. | 26/09 | PDF de ejemplos |
| U06 | Admisión de los centros: ¿es manual por SAAQUIK? ¿Quién inscribe, Registros o el participante por autoservicio? | 25/09 | Tema 4 y diagrama |
| U07 | ¿La **tutoría** aplica a los centros? | 25/09 | Diagrama |
| U08 | ¿Qué aprueba **Jefatura**? ¿Los sobrepasos (SFAROVR)? | 25/09 | Diagrama |
| U09 | **Nombres de las horas.** El 26/09 el usuario dijo «pedagógica = presencial, 60 min» y «cronológica = 45 min de día / 50 de noche = 1 hora». En su nota del Zoom estaba al revés («40–45 / 50 min → h. académicas; 1 hora → h. cronológicas»), y en el uso común la hora pedagógica es la de 45/50 y la cronológica la de 60. En los PDF se usan sus nombres, siempre con los minutos al lado. Confirmar. | 26/09 | Usuario |

## 5. Supuestos descartados o por corregir
| ID | Supuesto | Estado | Entregables afectados |
|---|---|---|---|
| S01 | «En SEUSS un periodo duraba 3 meses». Salió de un mensaje del usuario, pero el 26/09 dijo: «eso la verdad yo ni lo sé». | **No usar.** Lo confirmado son 3 periodos al año (C04). | «PERIODO ACADÉMICO - ANTES Y DESPUÉS» (columna «antes» ilustrativa, 4 periodos de 3 meses). En la validación, las menciones a «cursos de periodos de 3 meses». Ofrecer corregir. |
| S02 | Horas de día «40–45 min». | Reemplazado por **45 min** (usuario, 26/09). | — |
| S03 | «Si desaprueba BASIC I, ¿pasa **automático** a BASIC II?» y «pasa al ciclo III». Fue una lectura equivocada de la nota del Zoom. | **Descartado:** en SEUSS no pasa (C11). | «NOTAS DE LA REUNIÓN - RESPUESTAS» (pág. 2) todavía lo plantea así; el PDF de ejemplos ya está corregido (I-4). |
