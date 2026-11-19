# Plan de Pruebas Integrales USS V7.0 (Ellucian)

Resumen de la hoja de Google «USS - Plan Pruebas Integrales_V7.0.xlsx» que el usuario compartió el 19/11/2026 (C201). Es el plan que siguen la USS y Ellucian en TEST. El usuario dirá paso a paso qué prueba se hace y cuándo: **esto es para estar informado, no para ejecutar nada por cuenta propia**. Los estados son los del 19/11/2026; antes de citarlos, pide al usuario el estado al día.

No se copian aquí las hojas con datos de alumnos («Estudiantes», «Val Estudiantes», «Est Ciclo Cierre»): solo se dice qué contienen.

## Estructura del plan

| Hoja | Qué es |
|---|---|
| Estrategia | BackOffice: las áreas (Procesos Académicos, Cuentas por Cobrar) preparan y validan la configuración. FrontOffice: ciclo del **estudiante nuevo** (de la admisión a la matrícula del segundo semestre) y del **estudiante antiguo** (de la matrícula del semestre siguiente a la graduación, con solicitudes de servicio); lo financiero va dentro de la matrícula |
| Extensiones | Los GAP (desarrollos fuera de Banner): CRM ONIX (GAP-001), grados y títulos, prácticas preprofesionales, diplomas, sílabos (GAP-016), pasarelas de pago BBVA y BCP, planes de pago, conciliación bancaria, facturación electrónica, primera cuota, repositorio documental |
| BackOffice - A | A1 a A21: configuración previa (periodos, espacios, reglas curriculares, CAPP, cohortes, docentes, catálogo, NRC, inscripción, calificaciones, asistencia, cuentas por cobrar) |
| Prueba B | **Ciclo 0: calificaciones y cierre de periodo** (B1 a B9), con alumnos antiguos |
| Prueba C | Alumnos nuevos: admisión (ONIX), cohorte, becas, contratos, encabezado y RATE, cargos, pago, bloque, correo, turnos, autoservicio (C1 en adelante) |
| Prueba D | Ciclo de verano: fin de periodo, matrícula, pagos, asistencia y notas, evaluación docente, devoluciones |
| Prueba E | Periodo regular de pregrado (mismo esquema que D) |
| Prueba F | Periodo regular de pregrado de Medicina (con atributo de nivelado y reglas de bloque) |
| Prueba G | Periodo regular de posgrado |
| Prueba H - USS | Casos propios de la USS: programa nuevo, admisión y **Capacidad 05: Idiomas, Computación y Emprendimiento** (H28 a H38) |
| Periodos | Periodo de cierre regular **202646**; periodo de matrícula regular **202746**, parte **PGE**, del 08-oct-2026 al 07-mar-2027 |
| Programas Cursos, Estudiantes, Val Estudiantes, Est Ciclo Cierre | Datos de prueba (alumnos y cursos). Est Ciclo Cierre: los 11 alumnos del NRC **10173** (ESEC 00642, periodo 202646) de varios programas de pregrado |

## Prueba B: calificaciones y cierre de periodo (la que está en curso)

| Paso | Qué | Páginas | Estado al 19/11 | Dónde está en la base |
|---|---|---|---|---|
| B1 | NRC del periodo 202646 | SSASECT, SSARRES, SSADETL, SSAXLST, SHAGCOM | Exitoso | 01-creacion-nrc.md |
| B2 | Inscribir 10 alumnos antiguos de varios programas, sin afectar la cuenta corriente | SFAREGS | Exitoso | ref-preguntas-frecuentes-operacion.md |
| B3 | Notas finales de los 10 alumnos | SFASLST | Exitoso | instructivo 7.1.6 |
| B4 | Pase a historia | SFASLST, SHRROLL | Exitoso | C199 (NRC 10173, «Pasada» marcada, «Deg Created») |
| B5 | Verificación de cursos repetidos | SHRRPTS | Exitoso | C200; instructivo 7.2.2, diap. 15 a 22 |
| B6 | Cálculo del promedio (PGA) | SHRCGPA (GJAPCTL) | **Pendiente** | 7.2.2, diap. 24 a 31; parámetro 02: `a`, `r` o `c` |
| B7 | CAPP masivo o individual | SMRBCMP, SMARQCM | **En curso** (19/11: SMRBCMP en modo P con `POB_CICLO_B`, periodo 202744, C204) | 7.1.9 (SMRBCMP); 7.2.4 (SMARQCM, resultado en SMICRLT) |
| B8 | Proyecciones | SFPPROJ | **Pendiente** | por cargar en la base |
| B9 | Validación de promedios y proyecciones | SHATERM | **Pendiente** | C200 (PGA global y por plan de estudios) |

**Selección de población de la prueba B:** el 19/11/2026 Registros cargó por CSV la selección `POB_CICLO_B` (aplicación `STUDENT`) con 11 alumnos, sin duplicados ni inválidos (C203). Pasos en `arquitectura-centros-empresariales/references/ref-preguntas-frecuentes-operacion.md`. Se usó en B7 (SMRBCMP, modo P, C204); por confirmar si también en B6 (SHRCGPA, parámetros 03 a 05).

El orden de fin de periodo se repite en D, E, F y G: SGAMSTU (ingresante a regular) › **SHRRPTS** › **SHRCGPA** › **SMRBCMP / SMARQCM** › **SFPPROJ** › **SHATERM** (promedios, estados académicos y proyecciones).

## Prueba H: lo de los Centros Empresariales (Capacidad 05)

| Paso | Qué | Páginas |
|---|---|---|
| H28 | Agregar el programa de Idiomas al alumno | SGASTDN / SAAADMS |
| H29 | Agregar el programa de Computación al alumno | SGASTDN / SAAADMS |
| H30 | Agregar el programa de Emprendimiento al alumno | SGASTDN / SAAADMS |
| H31 | Cambiar la malla curricular a un alumno | SGASTDN / SAAADMS |
| H32 | NRC de Idiomas con ligas de uno a muchos | SSASECT, SSADETL |
| H33 | Restricciones de los NRC por nivel (pregrado, posgrado…) | SSARRES |
| H34 | NRC de Computación, malla nueva (cursos electivos) | SSASECT |
| H35 | Matrícula por autoservicio en 1 curso de Idiomas | (la hoja dice SMARQCM) |
| H36 | Matrícula por autoservicio en 2 cursos de Computación, para un alumno ya matriculado en Idiomas | (la hoja dice SMARQCM) |
| H37 | Sílabos | GAP-USS |
| H38 | Componentes calificables de cursos extracurriculares | SHAGCOM |
| H39 a H42 | Asistencia y notas del docente por autoservicio (Moodle), consulta del alumno | Autoservicio |
| H43 a H46 | Lista de espera, CAPP individual, CAPP tras una modificación académica, cursos usados y no usados | Autoservicio |
| H47 a H49 | Tipos de horas de práctica en el NRC, convalidaciones, educación continua | SSASECT, SAAADMS, SGASTDN, SFAREGS |

H1 a H15 crean un programa nuevo de punta a punta (STVTERM, partes, SOATERM, STVMAJR, STVDEGC, SMAPRLE, SOACURR, STVSUBJ, STVCOLL, SCACRSE, SCARRES, SMAALIB/SMAAREA/SMAPROG, equivalencias, SCAPPRQ, malla para exámenes de suficiencia). Mucho de eso ya se probó con los centros: ver las guías de `arquitectura-centros-empresariales` y el registro (C140 a C200).

## Cómo usar esta guía

- Cuando el usuario diga «vamos con la B6» (o cualquier paso), abre la fila, busca en el registro y en las preguntas frecuentes lo ya probado, y prepara el checklist con la lámina del instructivo. No ejecutes ni guardes en TEST sin que lo pida (sección 1 de `manejo-banner-test.md`).
- Lo que se pruebe se devuelve al registro con su C## y, si sirve al asistente, como pregunta frecuente.
