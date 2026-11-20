# Computación: matriz de scripts y pendientes

Parte de la skill `centro-computacion` (el mapa está en su `SKILL.md`).

## Matriz de Scripts de Computación (actualizada al 23/10/2026)

| # | Script / Casuística | Páginas Banner | Estado | Evidencia en TEST |
|---|---|---|---|---|
| **01** | Matrícula regular | `SFAREGS` | ✅ Validado | NRC 1021 (S00581081/S00581091) y NRC 1026 (S00581109/S00581108). |
| **02** | Matrícula especial (sobrepasos) | `SFAROVR` → `SFASRPO` → `SFAREGS` | ✅ **Validado (05/10)** | Regla `CAPACIDAD` (casilla *Capacidad*) en `SFAROVR` 202656. `S00581110` (Juan Flores), admitido con `CMEMC38` y con permiso `CAPACIDAD` en `SFASRPO`, quedó inscrito con **RE** en el NRC 1021 lleno (2/2). Con `S00581108` salió *«Duplicate Course with Section 1026»* porque ya tenía ESEC 00650. |
| **03** | Matrícula por convalidación | `SHATRNS` → `SHATFAC` | ✅ Validado | S00581111 (Ana Rojas) convalidada con IST150 (nota 16, modo P) y rolada a historia. |
| **04** | Matrícula por examen suficiencia | `SOATEST` → `SFAREGS` | 🚫 **NO APLICA** | Confirmado por usuario (C36): Computación **NO** rinde examen de suficiencia (exclusivo de Idiomas). |
| **05** | Curso especial para egresados | `SSASECT` → `SFAREGS` | ⏳ **PENDIENTE** | Sección modular/intensiva para alumnos bachilleres/egresados. |
| **06** | Doble programa simultáneo | `SGASTDN` → `SFAREGS` | ✅ Validado | S00581091 con Pregrado (L1) y Computación (LC) en paralelo. |
| **07** | Tres programas simultáneos | `SGASTDN` → `SFAREGS` | ⏳ **PENDIENTE** | Alumno activo en Pregrado (L1), Idiomas (LI) y Computación (LC). |
| **08** | Retiro de matrícula (DD) | `SFAREGS` | ✅ Validado | S00581091 retirado DD del NRC 1021; vacante liberada automáticamente. |
| **09** | Reactivación de matrícula | `SGASTDN` → `SFAREGS` | ✅ **Validado** | Probado ciclo de suspensión en `SGASTDN`/`SFAREGS` (bloqueo por inactivo y reactivación inmediata a `AS`). |
| **10** | Retorno obligatorio por desaprobado | `SMARQCM` → `SMICRLT` | ✅ **Validado** | S00581108 (nota 08 rolada) auditado en CAPP: Requerimientos y Áreas en «No cumple», créditos usados 0/4, curso `ESEC 00650` clasificado como «Curso no usado» (reprobado). |
| **11** | Apertura de nuevo periodo | `STVTERM` → `SOATERM` → `SSASECT` | ✅ **Validado (05/10)** | `202751` («2027-V Verano Idi.Com.Emp.») ya existía: inscripción permitida, modelo básico + proyectado, web maestro activo, primer NRC 1000, inscripción web del 20-SEP-2026 al 15-MAR-2027 y acceso docente del 03-ENE al 05-ABR-2027. Partes: **X01 12-ENE→22-FEB-2027 (6 sem)**, P01, I01 y 1. Se creó un NRC de prueba ESEC 00650 A en X01. **Falta X02** (U22). |
| **12** | Cierre de periodo / actas | `GJAPCTL` (`SHRROLL`) | ✅ Validado | Jobs 8113 y 8114 exitosos con pase masivo a historia académica. |
| **13** | Procesamiento de calificaciones | `SFASLST` | ✅ Validado | Registro de notas 16, 10, 08 e INH en actas de NRC 1021 y 1026. |
| **14** | Cierre de curso | `SSASECT` → `SFASLST` | ✅ Validado | Cierre y paso oficial a historia completado con `SHRROLL`. |
| **15** | Ampliación de cupos y reservas | `SSASECT` (Detalles de ingreso / Lugares reservados) | ✅ Validado | NRC 1021 (aforo 2/2) y NRC 1026 (error *Closed*, ampliación 1 a 4). |
| **16** | División de grupos / Traslado | `SSASECT` → `SFAREGS` | ✅ **Validado** | María Ramírez (`S00581109`) trasladada de NRC 1026 (`DD`) a NRC 1021 (`RE`), resolviendo `Reserve Closed` ampliando cupo CMEMC38 y confirmada en `SFASLST`. |
| **17** | Gestión de horarios y cruces | `SSASECT` | ✅ **Validado (05/10)** | NRC 1021 y 1026 con el mismo bloque y docente: SSASECT dio «*ERROR* Conflicto de horario del instructor para 100582059. ¿Crear sobrepaso?»; con OK quedó «Indicador de sobrepaso». El cruce del alumno en SFAREGS no se pudo probar (ver C41). |
| **18-A** | Auditoría de carga docente | `SIAASGN` | ✅ Validado | Docente DCHUMAN con 4 NRCs (horas semanales, contacto y FTE nativos). |
| **18-B** | Retenciones y bloqueo fatal | `SOAHOLD` / `STVHLDD` | ✅ Validado | Retención TT bloqueando matrícula en SFAREGS (*ERROR*). |
| **18-C** | Solicitud de servicio / queja | Autoservicio → `SVASVPR` | ✅ **Validado (05/10)** | Mecanismo validado con `CER` (Certificado): el alumno (100582059) crea la solicitud en el Autoservicio y se atiende en `SVASVPR` (estatus, comentario interno y comentario de respuesta). `SVASVPR` no deja crear solicitudes (*«Función inválida»*). **No existe un servicio de queja**: hay 17 en SVVSRVC, todos de carpetas, certificado y constancia (U14). |
| **19** | Calendario de calificaciones y componente `ATTRGRD` | `SHAEGBC` → `SHAGCOM` | ✅ **Validado (23/10)** | El usuario confirma que completó y validó en TEST el flujo para el periodo 202656, NRC 10026 (`ESEC 00697`, X06). `ATTRGRD`: peso 0.00, **Debe aprobar** y escala de asistencia del 70 %, separada de `VIG_11`. Nota mínima regular del curso: 11 (C95). |

---

## ▶️ Dónde quedamos (05/10/2026)
- **19 de 21 scripts aplicables validados** (el 04 no aplica). Pendientes: 05 y 07.
- **Faltan 05 y 07:**
  1. Script 05: en Idiomas el egresado no lleva el curso (C50, ADR-012). ¿Computación trabaja igual? (U24)
  2. Script 07: ya no hay que esperar a la USS. Se cierra en el **bloque 2 de `centros/idiomas/pruebas-test.md`**, al agregar el programa de Idiomas a `S00581091`.
  3. U22: ¿se agregan X02 y los demás grupos del verano 2027 en 202751?
  4. U14: ¿quién crea el servicio de quejas en SVVSRVC?
- **Para ordenar en TEST:**
  - retención de S00581081;
  - estatus de S00581109 en SGASTDN;
  - el NRC 1021 sigue con máximo 2 y reserva general 0 desde el Script 02;
  - NRC de prueba en 202751/X01 (número por anotar).
- **Al retomar:** seguir con las pruebas de Idiomas (`centros/idiomas/pruebas-test.md`); cierran también el Script 07 de Computación.

## 📋 Checklist de Scripts Pendientes para Próximas Sesiones

> **Instrucción para el agente:** A medida que se ejecute cada prueba, marca con `[x]` el script correspondiente y actualiza la evidencia arriba.

- [x] **Script 10 — Retorno obligatorio tras desaprobado (`SMARQCM` → `SMICRLT`):**
  - *Contexto:* Carlos Torres Mendoza (`S00581108`) con nota `08` rolada en `ESEC 00650`.
  - *Evidencia:* CAPP individual arrojó «No cumple» en requerimientos y áreas, 0 créditos obtenidos y curso enviado a «Cursos no usados» (02/10/2026).
- [x] **Script 16 — División de grupos / Traslado de sección (`SFAREGS`):**
  - *Contexto:* Reubicación de participantes de una sección saturada a una sección espejo o cambio de horario.
  - *Evidencia:* María Ramírez (`S00581109`) retirada con `DD` del NRC 1026 e inscrita con `RE` en NRC 1021, auditada en `SFASLST` (02/10/2026).
- [x] **Script 02 — Matrícula especial con sobrepasos (`SFAROVR` → `SFASRPO` → `SFAREGS`):**
  - *Evidencia (05/10):* `S00581110` inscrito con RE en el NRC 1021 lleno gracias al sobrepaso `CAPACIDAD`.
  - *Opcional:* prueba de control con un alumno sin permiso («Closed»); devolver el 1021 a máximo 3 y reserva general 1.
- [ ] **Script 07 — Tres programas en simultáneo (`SGASTDN` → `SFAREGS`):**
  - *Contexto:* Alumno multiescuela (Pregrado + Idiomas + Computación).
  - *Paso:* Crear Study Path 1 (Pregrado `1`), Study Path 2 (Idiomas `I`) y Study Path 3 (Computación `C`) en `SGASTDN`. Inscribir un NRC en cada programa en `SFAREGS`.
- [x] **Script 09 — Reactivación de matrícula (`SGASTDN` → `SFAREGS`):**
  - *Contexto:* Participante que suspendió estudios y retorna.
  - *Evidencia:* Bloqueo de inscripción con estatus inactivo (`IS`/`SU`) y reactivación inmediata a `AS` en `SGASTDN` / `SFAREGS` (02/10/2026).
- [ ] **Pendiente del Script 16:** verificar que el traslado no duplique ni pierda el cobro (TSAAREV).
- [ ] **Script 05 — Curso especial para egresados (`SSASECT` → `SFAREGS`):**
  - *Contexto:* Módulo intensivo de acreditación rápida para graduandos.
  - *Paso:* Programar NRC en parte de periodo intensiva y matricular bachiller.
- [x] **Script 11 — Apertura de periodo (`SOATERM` → `SSASECT`):**
  - *Evidencia (05/10):* 202751 con la parte X01; NRC de prueba creado en X01. No se usó «Copiar de periodo» porque el periodo ya estaba configurado.
  - *Duda U22:* falta X02 (y I02, I03, P02, P03) en 202751.
- [x] **Script 17 — Gestión de horarios y cruces (`SSASECT`):**
  - *Evidencia (05/10):* conflicto del docente detectado en el NRC 1021; se resolvió con el sobrepaso del instructor.
  - *Pendiente opcional:* cruce del alumno en SFAREGS con un alumno sin retención, con estatus activo y con ambos NRC sin rolar.
- [x] **Script 18-C — Solicitudes de servicio (Autoservicio → `SVASVPR`):**
  - *Evidencia (05/10):* solicitud CER creada en el Autoservicio y atendida en SVASVPR. Falta que la USS cree el servicio de quejas (U14).
---
