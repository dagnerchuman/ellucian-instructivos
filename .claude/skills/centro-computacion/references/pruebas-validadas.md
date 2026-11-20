# Computación: pruebas de punta a punta ya validadas

Parte de la skill `centro-computacion` (el mapa está en su `SKILL.md`).

## ✅ Flujo completo validado: Diseño Web, NRC 10044 (23–26/10/2026)
> **Dónde está «Faculty»:** pestaña **Autoservicio Docentes**, tarjeta **«Detalle de Notas y Asistencia»**: **Ingresar asistencia** (Pasar lista) e **Ingresar calificaciones** (Libro de calificaciones). La tarjeta «Faculty Grading» da error y no hace falta (C119).

Prueba de punta a punta, desde la creación del NRC hasta la nota, con el usuario como docente **y** alumno (C96–C103).

| # | Paso | Página | Estado | Evidencia |
|---|---|---|---|---|
| 1 | Crear NRC | `SSASECT` | ✅ | NRC **10044**: ESEC 00684 «Diseño Web», A, X06, sesión M, VIRT, modo V, cupo 40 (Proyectado antes de «Lugares reservados»). SAUVIR / SALA-VIRT con `O` en «Indicador de sobrepaso» (C97). Horario cambiado a jueves por la tarde por el cruce con el 10042 |
| 2 | Plan de evaluación | `SHAGCOM` | ✅ | TA1 0.15 · TA2 0.15 · PA 0.40 · EF 0.30 con `VIG_11` (aprobatoria 55 de 100) + `ATTRGRD` 0.00, Debe aprobar, `AST_70` (aprobatoria 70). Peso final 1.00 (C98). Por revisar: el bloque superior quedó en `AST_70` |
| 3 | Programa del alumno | `SFAREGS › Currículos` | ✅ | A `100582059` se le agregó con `+`, programa y Tab el plan de estudios 4: `CMEMC44` «Acreditación Computación XP 07», nivel C (C100; U31: ¿CMEMC44 o CMEMC38?) |
| 4 | Matrícula | `SFAREGS` | ✅ | Plan 4 en `EL` y NRC 10044 en RE. «Estimación de cuota procesada» |
| 5 | Regla de asistencia | `SOAATRK` | ✅ | **Va primero**: 202656, X06, ESEC 00684, NRC 10044, Desplegar clase, Presente/Ausente, Control de asistencia, del 07-SEP al 31-OCT-2026 (C101) |
| 6 | Pasar lista | Faculty › Control de asistencia | ✅ | 86 % (ausente el jueves 22-OCT) (C101) |
| 7 | Notas por componente | Faculty › Libro de calificaciones › Componentes | ✅ | TA1, TA2, PA y EF con 85 de 100 (→ 17), visibles en el Autoservicio del alumno (C102, C103, C105) |
| 8 | Asistencia a `ATTRGRD` | Pasar lista › **Clase › «Actualizar la asistencia en el libro de calificaciones»** › Sí | ✅ | No pasa sola: la envía el docente. Al enviarla, `ATTRGRD` tomó 57,14 → INH y luego 85,71 → APRO (C119; U32 resuelta). Requiere GORICCR en Y, GORRSQL activa y STVGCHG con CA (C104) |
| 9 | Nota final | Calificaciones compuestas → `SFASLST` | ✅ | Compuesta: porcentaje 85 y **INH** (C105). «Calificaciones finales» no pide nada: la nota pasa sola al backoffice y **SFASLST muestra INH** (C106, C107) |
| 9b | Escala de arriba en SHAGCOM | `SHAGCOM` › Asignación de escala de calificación | ✅ | Con `AST_70` arriba, la nota final salió **APRO** en SFASLST (C120). **Comprobado con el NRC 10045:** con `VIG_11` arriba y asistencia 100 %, la final llega **17** (C181, C188) |
| 10 | Pase a historia | `GJAPCTL` › `SHRROLL`; salida en `GJIREVO` | ✅ | Modo A (job 7761) y modo U (job **7762**): «Rolled to Academic History» y «Deg Created» por cada plan del alumno, más un «API Error» por un plan inactivo (C121, C122). Por confirmar la nota que quedó (17 o APRO, C120) |
| 11 | Corregir la nota en la historia | `SHATCKN` (Insertar secuencia: 17, modo V, razón de corrección) | ✅ | Primero se agregó el modo `V` al 17 del nivel C en `SHAGRDE` (solo tenía `P`). SHACRSE muestra **17** (C124) |

## ✅ Prueba completa con capturas: Google, NRC 10045 (30/10 a 04/11/2026)
El «ejemplo de prueba 2» de la Demostración 1 (`datos.json › demostraciones › ejemplo_prueba_2`): 14 pasos hechos en TEST, con su tabla campo por campo y 66 capturas, 65 con cuadros morados y números verdes como las láminas (C180–C195). En el sitio: Demostración 1 › «Para estudiar» › «Prueba en TEST» (flujo de Archify, cada nodo abre su ficha en un modal) y la página propia `00-demostracion-1-prueba-nrc-10045`.

| # | Página | Lo que quedó |
|---|---|---|
| 1–3 | `SSASECT` | 202656 › 10045 › Ir; miércoles 15:30–17:10, SAUVIR / SALA-VIRT con `O`; docente 100582059, principal, 100 % (C180) |
| 4 | `SIAASGN` | El 10045 es la asignación 10 de 10; resumen: 10 horas crédito, carga educativa 22; sin reglas de carga en 202656 (C180, C194) |
| 5 | `SMAAREA` | `ESEC 00701` en `MC44-01` › `ECOM-03` (versión 202454), condición 2; SMAPROG CMEMC44 tiene solo esa área (C181, C194) |
| 6 | `SHAGCOM` | `VIG_11` arriba; TA1 0.15 · TA2 0.15 · PA 0.40 · EF 0.30 + `ATTRGRD` 0.00, Debe aprobar, `AST_70` (C181) |
| 7 | `SOAATRK` | Regla 3: X06, ESEC 00701, NRC 10045, Presente/Ausente, del 07-SEP al 31-OCT-2026 (C182) |
| 8 | `SFAREGS` | 100582059 con RE, plan 4 (CMEMC44); SOADEST con DATABASE sin guardar (C185) |
| 9–10 | Autoservicio | Asistencia 100 % enviada al libro (ATTRGRD APRO); TA1, TA2, PA y EF 85 → 17 cada uno (C186, C187) |
| 11 | `SFASLST` | Final **17**, modo V (C188) |
| 12 | `SFAREGS` | Arnold Vaca: RE → **DD** el 31-OCT-2026 (último día del DD en la X06), «No contar en ingreso» / «Eliminado» (C189, C194) |
| 13 | `GJAPCTL` › `SHRROLL` | Job 7994 en modo A y 7995 en modo U: «Rolled to Academic History», RECORD COUNT 1 (C190) |
| 14 | `SHACRSE` | ESEC 00701 «Google» con **17**, modo V; en SFASLST, «Pasada» ✓; en SHATCKN, secuencia 1 con 17 (C190, C194) |

## Incidencias resueltas

| ID | Descripción | Solución aplicada y confirmada |
|---|---|---|
| **U20** | Modo de calificación V (catálogo) vs P (SHAGRDE Nivel C) | **RESUELTA (02/10):** Se añadió el Modo `V` (*Vigesimal Regular*) a las notas del Nivel `C` en `SHAGRDE` (Instructivo 7.1.3 diap. 16). `SHRROLL` procesó de inmediato el cierre del NRC 1026 con 100% de éxito. |
