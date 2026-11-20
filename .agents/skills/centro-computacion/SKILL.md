---
name: centro-computacion
description: >-
  Qué hace: datos y pruebas del Centro de Computación (Informática, Protech XP) en Banner: nivel C,
  programas XP 01 a 07 (rutas de aprendizaje, CMEMC38 a CMEMC44), materia ESEC, partes X01 a X07,
  NRC 10018, 10019, 10044 y 10045 (prueba completa con capturas), flujo validado en TEST, acreditación,
  costos y errores frecuentes de los
  usuarios finales; sus datos están en centros/computacion/datos.json. Cuándo usarla: la tarea es
  solo de Computación o Informática (rutas, NRC 10044, CMEMC, ESEC, reunión con el jefe del Centro de
  Informática). Cuándo no usarla: lo que vale igual para los tres centros
  (arquitectura-centros-empresariales) ni Idiomas o Emprendimiento.
---

# Centro de Computación (Informática) — Arquitectura Específica

> Este skill contiene la data confirmada y específica del **Centro de Informática** (también llamado **Computación**).
> Para la arquitectura general de los tres centros, ver `arquitectura-centros-empresariales`.
>
> **Carpeta del centro:** `centros/computacion/`
> - `datos.json` es la **fuente única** de los datos de esta página (códigos, grupos, NRC, personas de TEST, estado de los scripts y dudas). Si un dato cambia, cámbialo allí y en esta skill, y regenera los diagramas.
> - `diagramas/` tiene 27 flujos paso a paso en HTML interactivo, PNG claro y oscuro, y SVG: seis flujos base y los 21 scripts que aplican (el 04 no aplica, C36). Ver la skill `workflow-diagramas-archify`.

## Mapa de la skill: abre solo el archivo que necesitas

| Si necesitas… | Abre |
|---|---|
| Rutas de aprendizaje XP, costos y certificados; mallas `MC42`/`MC44` en SMAPROG y SMAAREA; prerrequisitos y orden de cursos | [references/acreditacion-protech-xp-y-mallas.md](references/acreditacion-protech-xp-y-mallas.md) |
| Qué cursos, NRC (10044, 10045…) y alumnos de prueba hay en TEST | [references/datos-de-test.md](references/datos-de-test.md) |
| Cómo se validó el NRC 10044 (Diseño Web) y el 10045 (Google) con capturas, e incidencias resueltas | [references/pruebas-validadas.md](references/pruebas-validadas.md) |
| Estado de cada script de Computación, dónde quedamos y qué falta probar | [references/scripts-y-pendientes.md](references/scripts-y-pendientes.md) |

## Identificadores en Banner

| Concepto | Código | Descripción |
|---|---|---|
| **Nivel de alumno** | `C` | Computación (STVLEVL) |
| **Escuela / College** | `EM` | Centros Empresariales |
| **Campus** | `S` | Sede de Chiclayo |
| **Programa** | `CMEMC38` | Acreditación Computación XP 01 |
| **Campo de estudio mayor** | `ACXP` | Acreditación en Computación XP |
| **Departamento** | `EMCI` | Jef. de Centro de Informática |
| **Grado** | `000000` | No otorga grado |
| **Materia del catálogo** | `ESEC` | Escuela EM — cursos de Computación |
| **Regla de currículo base** | `ECOM-01` | Primera regla del área MC38-01 «Ciclo I»; en TEST se describe «Computación I», nombre del Plan Tradicional, no de la ruta (C175) |
| **Modo de calificación (catálogo)** | `V` | Vigesimal regular |
| **Modo de calificación (SHAGRDE Nivel C)** | `V` (además de `P`) | Se agregó `V` el 02/10 (U20), pero no a todas las notas: el 17 solo tenía `P` hasta el 26/10 (C124). Revisar de 00 a 20 e INH |

### Curso nuevo en SCACRSE (C146)
Lo crea **Registros Académicos**; el centro, solo si le dan acceso (C147). Periodo `000000` (Del periodo 000000 · A periodo 999999, como todos los cursos reales); Escuela `EM`; Departamento `EMCI`; Estatus `A`; UEC o crédito y Cobro **variables** `0 O 1` (Inferior 0, indicador O, Superior 1); Teoría `1` y Laboratorio `1` (HT 1, HP 1) y Contacto `2`; con «Sección siguiente» (↓): Nivel `C` (CEU sin marcar); Modo `V` «Vigesimal Estándar» predefinido; Tipo de horario `TEO` y `PRA`, los dos `VIRT` y carga de trabajo `1` (C148). Lo más seguro: **Copiar** de `ESEC 00684` (Diseño Web) y dejar las horas como vengan (U45). En el ejemplo ESEC 00701 (C145) solo estaba mal «Del periodo» (202656 en vez de 000000).

## Partes de periodo (Computación)

| Parte | Periodo | Fechas | Semanas |
|---|---|---|---|
| X01 | 202651 | 12/1 – 22/2/2026 | 6 |
| X02 | 202651 | 23/2 – 22/3/2026 | 4 |
| X03 | 202654 | 6/4 – 31/5/2026 | 8 |
| X04 | 202654 | 1/6 – 12/7/2026 | 6 |
| X05 | 202656 | 3/8 – 30/8/2026 | 4 |
| X06 | 202656 | 7/9 – 31/10/2026 | 8 |
| X07 | 202656 | 2/11 – 13/12/2026 | 6 |

Parte de periodo general: **CGE**.

## Escala de notas (SHAGRDE, Nivel C)

| Nota | Aprueba | Gana créditos | Observación |
|---|---|---|---|
| 11–20 | ✅ Sí | ✅ Sí | Nota mínima aprobatoria: **11** |
| 00–10 | ❌ No | ❌ No | Desaprobado |
| INH | ❌ No | ❌ No | Inhabilitado por inasistencia (< 70%) |

## Errores frecuentes de los usuarios finales (no son dudas)
| Mensaje o síntoma | Causa | Qué hacer |
|---|---|---|
| La nota final sale APRO o INH en lugar de un número | En SHAGCOM, la escala de arriba es `AST_70` | Poner `VIG_11` arriba; `AST_70` solo en el componente ATTRGRD (C120, C123) |
| `ATTRGRD` vacío o con un porcentaje viejo | El docente no envió la asistencia | Pasar lista › Clase › «Actualizar la asistencia en el libro de calificaciones» › Sí (C119) |
| «El modo de calificar no es válido para la calificación ingresada» (SHATCKN, SFASLST) o «No Substitute Grade Found» (SHRROLL) | En SHAGRDE, esa nota del nivel C no tiene el modo `V` | Agregar `V` en «Modos de calificar válidos» de esa nota (C34, C124) |
| «El elemento está protegido contra actualización» en SFASLST | La nota ya pasó a la historia | Corregir en SHATCKN con una secuencia nueva (C123) |
| «API Error: Invalid study path sequence for outcome» en el .lis de SHRROLL | El alumno tiene un plan de estudios inactivo | No impide el pase de la nota (C121) |
