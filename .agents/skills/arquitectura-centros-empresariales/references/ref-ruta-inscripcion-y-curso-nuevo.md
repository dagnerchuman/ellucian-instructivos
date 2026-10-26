# Guía: inscribir a un alumno en su ruta de aprendizaje y crear un curso nuevo (Computación)

Repaso para la reunión del 27/10/2026 con el jefe del Centro de Informática (C126). Junta lo probado en TEST (C17, C19, C71, C86, C100) con los instructivos de Ellucian. Las rutas están en [ref-acreditacion-computacion.md](ref-acreditacion-computacion.md).

## Idea clave
Escuela profesional del alumno → **ruta de aprendizaje** (agrupación 1 a 7) → **programa XP** en Banner (`CMEMC38` = XP 01 … `CMEMC44` = XP 07) → cursos de esa ruta. Un curso nuevo se «asigna a las escuelas» agregándolo a la **malla de los programas XP** de las rutas que lo llevan (SMAAREA) y, si se quiere impedir que otros lo lleven, con una **restricción de programa** (SCARRES).

## A. Inscribir al alumno en su ruta
| N.º | Página | Qué hacer | Fuente |
|---|---|---|---|
| 1 | Lámina de rutas | Ubicar la escuela del alumno y su ruta (por ejemplo, Ing. de Software → ruta 5 o 7, U37) | C125 |
| 2 | **GOAMTCH** | Solo si la persona no existe: ID `GENERATED`, origen `PERS_NATU`, apellidos con `/`, dirección `PP`, teléfono `MOV`, correo `PER1`; «Marcar-Duplicar» y guardar. Un alumno de pregrado ya existe: se salta | 02-creacion-de-persona.md; C17, C32 |
| 3 | **SAAQUIK** | ID, periodo (`202656`), nivel `C` › Ir. Tipo de alumno, estatus `AS`, residencia `R`. Currículo, prioridad 1: Programa › `•••` › «Reglas de currículo base por programa» › el programa XP de su ruta › OK. Banner pone mayor `ACXP` y departamento `EMCI`. Guardar | 03-admision-y-asignacion-al-programa.md; C19 |
| 3b | **SFAREGS › Currículos** | Otra forma: agregar el currículo del centro al alumno que ya tiene otro programa: `+`, programa y Tab | C100 |
| 4 | **SGASTDN** | Verificar que el alumno tenga el plan de estudios del centro activo, además del de pregrado | Script 06 |
| 5 | **SFAREGS** | Periodo → ID → plan de estudios (no asumir `1`) › Ir; estatus `EL` en «Información de ingreso» y en el plan; Guardar; `⤓`; NRC, Tab; Guardar. Queda `RE` | 04-matricula-en-el-nrc.md; C86, C100 |
| 5b | **Autoservicio del alumno** | El alumno elige su plan del centro, pestaña **Proyecciones** (SFPPROJ), agrega el NRC y pulsa **Enviar**: queda `RW` | ref-autoservicio-matricula.md; C71 |
| 6 | **TSAAREV** | El cargo del curso aparece en la cuenta corriente (en línea o con SFRFASC por lotes) | C73 a C75, C82 |
| 7 | **SMARQCM** | CAPP: el curso cuenta en el área de su programa XP | Script 10 |

**Hoy en SEUSS:** Campus Virtual › Procesos en línea › Matrícula en línea › logo del Centro de Informática › modalidad › curso y sección › modalidad de pago (lámina 3).

## B. Crear un curso nuevo
| N.º | Página | Qué hacer | Fuente |
|---|---|---|---|
| 1 | **SCACRSE** (bloque clave) | Materia `ESEC`, **número nuevo** (revisar el último que existe; en TEST el más alto conocido es `00700`), periodo desde el que rige. Recomendado: **Copiar** de un curso parecido (por ejemplo `ESEC 00684`) | 1.1.4, diap. 20 |
| 2 | **SCACRSE** › Detalles | Título; escuela `EM`; departamento `EMCI`; estatus activo | 1.1.4, diap. 21 |
| 3 | **SCACRSE** › Horas | Créditos (UEC) y créditos de cobro; horas de teoría y laboratorio (en Computación HT 1 y HP 1) | 1.1.4, diap. 22; C60 |
| 4 | **SCACRSE** › Nivel | `C` (Computación) | 1.1.4, diap. 23 |
| 5 | **SCACRSE** › Modo de calificar | `V`, marcado como predefinido | 1.1.4, diap. 24; C35 |
| 6 | **SCACRSE** › Tipo de horario | El tipo de horario y su método educativo; la carga de trabajo es la que verá el docente en SSASECT | 1.1.4, diap. 25 |
| 7 | **SCADETL** | Cuotas del curso (como `X032` en Idiomas) y equivalencias si las tiene | C68; 1.2.3 |
| 8 | **SSASECT** | Programar el NRC del curso nuevo en el periodo | 01-creacion-nrc.md |

## C. Asignar el curso a las escuelas (a sus rutas)
| N.º | Página | Qué hacer | Fuente |
|---|---|---|---|
| 1 | **SMAAREA** | Por cada programa XP de las rutas que llevan el curso: abrir su área (por ejemplo `MC38-01`), periodo; si cambia la malla, **Copiar** al periodo nuevo; en «Anexos de curso/atributo de área», en la regla del área, **Insertar** la materia `ESEC` y el número del curso; Guardar | 1.2.1, diap. 23–25; 1.3.1, diap. 10–13 |
| 2 | **SMAPROG** | Revisar que el área esté en la malla del programa, con calificación mínima | 1.2.1, diap. 31 |
| 3 | **SCARRES** (opcional) | Restricción de inscripción: **Programa** › Incluir los programas XP de esas rutas (o campo de estudio, nivel) para que nadie más lo matricule | 1.1.5, diap. 23–25 |
| 4 | **SMARQCM** | Correr el CAPP de un alumno de prueba de esa ruta y ver que el curso cuente | Script 10 |

- **Orden:** el curso se crea **antes** de cambiar las áreas (1.3.1, diap. 5; R12).
- En SSASECT se puede restringir un NRC puntual con **SSARRES**; SCARRES restringe el curso para todos sus NRC.

## Por confirmar
U35 (4 talleres o 4.º curso), U37 (código de cada ruta y cómo se elige si la escuela está en dos rutas), U40 (quién crea los cursos en SCACRSE y las áreas en SMAAREA), U41 (si se usará SCARRES para limitar los cursos a su ruta).
