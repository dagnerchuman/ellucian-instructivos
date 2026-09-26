# Registro de preguntas, dudas y decisiones

Última actualización: **26/09/2026**. Alcance: Centros Empresariales de la USS (Idiomas/Inglés, Computación/Informática, Emprendimiento) en Ellucian Banner.

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

## 3. Dudas abiertas para Ellucian
| ID | Duda | Desde | Origen |
|---|---|---|---|
| E01 | Hora de clase de **45 min (día)** y **50 min (noche)** en el mismo periodo: ¿cómo se configura si SIATERM tiene un solo factor de duración? ¿Se ajustan a mano las horas del NRC en SSASECT? | 26/09 | Notas del Zoom |
| E02 | Aula virtual: ¿las **notas regresan** a Banner? ¿Qué datos salen (NRC, docente, participantes, plan de evaluación)? | 26/09 | Notas del Zoom |
| E03 | Hora de **60 minutos**: si se necesita (carga o pago del docente), ¿dónde se registra? | 26/09 | Usuario |
| E04 | Si un participante pasa a BASIC II **sin examen**, ¿cómo queda BASIC I en la historia y en CAPP? | 26/09 | Notas del Zoom |
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
| U01 | Inglés: si un alumno desaprueba **BASIC I** (ciclo II) y pasa al ciclo III, ¿rinde **examen de suficiencia** o pasa a BASIC II **automático**? Si hay examen, ¿cuál es el puntaje mínimo? | 26/09 | Notas del Zoom |
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
