# Guía: inscribir a un alumno en su ruta de aprendizaje, asignar el curso a los programas (malla) y crear el NRC (Computación)

Repaso para la reunión del 27/10/2026 con el jefe del Centro de Informática (C126, corregido en C127). Junta lo probado en TEST (C17, C19, C71, C86, C100) con los instructivos de Ellucian. Las rutas están en [ref-acreditacion-computacion.md](ref-acreditacion-computacion.md).

## Idea clave (corregida por el jefe del Centro de Informática, C127)
Escuela profesional del alumno → **ruta de aprendizaje** (agrupación 1 a 7) → **programa XP** en Banner (`CMEMC38` = XP 01 … `CMEMC44` = XP 07) → cursos de esa ruta.
- **Asignar las escuelas a las rutas lo hace Pregrado**, no el centro.
- El centro **crea el NRC** (no «un curso nuevo»): antes mira **a qué malla va el alumno**; el curso tiene que estar en la malla del programa XP. Si no está, **hay que hacer la malla y la programación** (sección C).
- **«Asignar programas»** (no «asignar escuelas») es poner el curso en la **malla de los programas XP**: SMAPROG (áreas del programa) y SMAAREA (cursos del área), secciones C y C2.
- **SSARRES no asigna programas:** son las **restricciones de inscripción** del NRC (incluir o excluir por nivel, programa, campus, atributo o cohorte); se usan solo si hay que limitar el NRC (C128).

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

## C. Si el curso no está en la malla: hacer la malla y la programación
**Quién:** el curso lo crea **Registros Académicos**; el centro, solo si le dan acceso. Para el go-live se capacitará a todos por la cantidad de mallas que hay que actualizar (Liliana Ocampo, Ellucian, C147).

| N.º | Página | Qué hacer | Fuente |
|---|---|---|---|
| 1 | **SCACRSE** (encabezado) | Materia `ESEC`, **número nuevo** (revisar el último que existe; en TEST el más alto conocido es `00700`) y periodo **`000000`**: los cursos reales quedan **Del periodo 000000 · A periodo 999999** (C135, C146). Recomendado: **Copiar** de un curso real del centro (`ESEC 00684`) | 1.1.4, diap. 20 |
| 2 | **SCACRSE** › Detalles | Título; escuela `EM`; departamento `EMCI`; estatus activo | 1.1.4, diap. 21 |
| 3 | **SCACRSE** › Horas | **UEC o crédito y Cobro, siempre variables:** Inferior `0`, indicador `O`, Superior = créditos (`0 O 1`); permiten fijar las horas en el NRC (5.3, diap. 25), y en el NRC de teoría quedan en 1. **Teoría y Laboratorio:** las horas del sílabo (HT 1, HP 1; Contacto 2, lo calcula Banner). En los cursos reales hay dos formas: Basic I las tiene variables (`0 O 4`, `0 O 3`, `0 O 7`) y Emprendimiento I fijas (`1`, `2`, `3`); si se copia de `ESEC 00684`, se dejan como vengan | 1.1.4, diap. 22; C96, C146 |
| 4 | **SCACRSE** › Nivel | Guardar y **«Sección siguiente»** (↓, abajo a la izquierda) › «Nivel de curso»: `C` (Computación), CEU sin marcar | 1.1.4, diap. 23; C148 |
| 5 | **SCACRSE** › Modo de calificar | «Sección siguiente» › `V` «Vigesimal Estándar», **Predefinido** | 1.1.4, diap. 24; C35, C148 |
| 6 | **SCACRSE** › Tipo de horario | «Sección siguiente» › dos filas: `TEO` Teórico y `PRA` Práctico, método educativo `VIRT` y carga de trabajo `1` en cada una (la que verá el docente en SSASECT); sobrecarga y carga ajustada vacías. Guardar | 1.1.4, diap. 25; C148 |
| 7 | **SCADETL** | Cuotas del curso (como `X032` en Idiomas) y equivalencias si las tiene | C68; 1.2.3 |
| 8 | **SSASECT** | Programar el NRC del curso nuevo en el periodo | 01-creacion-nrc.md |

## C2. Agregar el curso a la malla de las rutas
| N.º | Página | Qué hacer | Fuente |
|---|---|---|---|
| 1 | **SMAAREA** | Por cada programa XP de las rutas que llevan el curso: abrir su área (por ejemplo `MC38-01`), periodo; si cambia la malla, **Copiar** al periodo nuevo; en «Anexos de curso/atributo de área», en la regla del área, **Insertar** la materia `ESEC` y el número del curso; Guardar | 1.2.1, diap. 23–25; 1.3.1, diap. 10–13 |
| 2 | **SMAPROG** | Revisar que el área esté en la malla del programa, con calificación mínima | 1.2.1, diap. 31 |
| 3 | **SCARRES** (opcional) | Restricción de inscripción: **Programa** › Incluir los programas XP de esas rutas (o campo de estudio, nivel) para que nadie más lo matricule | 1.1.5, diap. 23–25 |
| 4 | **SMARQCM** | Correr el CAPP de un alumno de prueba de esa ruta y ver que el curso cuente | Script 10 |

- **Orden:** el curso se crea **antes** de cambiar las áreas (1.3.1, diap. 5; R12).
- En SSASECT se puede restringir un NRC puntual con **SSARRES**; SCARRES restringe el curso para todos sus NRC.

## B. Crear el NRC
| N.º | Página | Qué hacer | Fuente |
|---|---|---|---|
| 1 | **SMAPROG / SMAAREA** | Ver a qué malla va el alumno: el curso debe estar en el área de su programa XP | 1.2.1, diap. 23–25 |
| 2 | **SOATERM** | Periodo y parte de periodo habilitados para programar (X05 a X07 en 202656) | 5.3, diap. 15–16 |
| 3 | **SSASECT** › encabezado | Periodo · NRC vacío · **Crear NRC** (o **Copiar NRC**) | 5.3, diap. 19 |
| 4 | **SSASECT** › Información de sección | Materia ESEC y número · sección · campus S · estatus activo · tipo de horario · modo V · parte de periodo · **Guardar** antes de cambiar de pestaña | 5.3, diap. 20–26; C97 |
| 5 | **SSASECT** › Información de ingreso | Cupo en **Proyectado** antes de «Lugares reservados» · Guardar | 5.3, diap. 27–28; C97 |
| 6 | **SSASECT** › Instructor y horas | CLAS, horario 24 h, días, sesión 01 · SAUVIR / SALA VIRT. con **O** en sobrepaso · docente principal 100 % · Guardar | 5.3, diap. 29–30; C97 |
| 7 | **SSARRES** (solo si hace falta) | **Restricciones de inscripción**, no asignación de programas: incluir o excluir por nivel, programa, campus, atributo o cohorte; las heredadas del catálogo (SCARRES) se ajustan aquí | 5.3, diap. 44, 46–51 |
| 8 | **SFAREGS** | Probar: un alumno de otro programa no debe poder matricularse | Por probar |

## Por confirmar
U35 (4 talleres o 4.º curso), U37 (código de cada ruta; las escuelas las asigna Pregrado), U40 (quién hace la malla y la programación cuando el curso no está), U41 (¿se pondrán restricciones de programa en los NRC con SSARRES?).
