# Catálogo Oficial de Casuísticas y Scripts de Pruebas: Centros Empresariales (CCEE)

Este documento define el catálogo de los **18 scripts operativos y casuísticas** que la Universidad Señor de Sipán (USS) requiere validar en **Ellucian Banner Student** para los tres Centros Empresariales: **Idiomas (Inglés)**, **Computación (Informática)** y **Emprendimiento**.

---

## Matriz de Scripts y Páginas Banner

| # | Script / Casuística | Páginas Banner | Descripción y Flujo Operativo |
|---|---|---|---|
| **01** | **Matrícula regular** | `SFAREGS` / Autoservicio Alumnos | Matrícula ordinaria backoffice o web. Autorización de plan `EL`, ingreso de NRC, asignación de estatus `RE` y tasación inmediata de cuotas (`Immediate assessment`). *(Validado en TEST 29/09 y 01/10)*. |
| **02** | **Matrícula especial** | `SFASRPO` → `SFAREGS` | Registro que requiere sobrepaso administrativo por cruce de horario, tope de créditos o requisitos especiales. Se otorga permiso en SFASRPO y se procesa en SFAREGS. |
| **03** | **Matrícula por convalidación** | `SHATRNS` → `SHATFAC` → `CAPP` | Convalidación de asignaturas de informática, idiomas o emprendimiento de otras instituciones o planes antiguos. Se asienta nota/crédito externo y CAPP acredita el requisito curricular. |
| **04** | **Matrícula por examen de suficiencia** | `SOATEST` → `SCAPREQ` / `SSAPREQ` → `SFAREGS` | Alumno rinde examen de suficiencia (ej. Inglés). Se registra puntaje en `SOATEST`. La regla de prerrequisitos permite matricular directamente el nivel superior (ej. BASIC II) sin haber cursado el anterior. |
| **05** | **Curso especial para egresados** | `SSASECT` → `SGASTDN` → `SFAREGS` | NRC intensivo o modular creado en partes de periodo especiales para bachilleres/egresados que necesitan cumplir la acreditación de idioma/computación para titulación. |
| **06** | **Matrículas para dos programas en simultáneo** | `SGASTDN` → `SFAREGS` | Alumno que cursa Pregrado (`Level 1`, Study Path 1) y Computación o Idiomas (`Level C/I`, Study Path 2). Se matriculan asignaturas en ambos expedientes de forma independiente en el mismo periodo. |
| **07** | **Matrículas para tres programas en simultáneo** | `SGASTDN` → `SFAREGS` | Alumno activo en Pregrado, Idiomas y Computación en paralelo (Study Paths 1, 2 y 3). Cada centro factura y evalúa según su propia regla de cuotas y horario. |
| **08** | **Eliminación / Retiro de matrícula** | `SFAREGS` | Desinscripción o retiro de un curso (código `DD` Drop/Delete o `DW` Drop Web) antes de la fecha límite. Libera automáticamente el cupo en el NRC (`Actual` disminuye). |
| **09** | **Reactivación de matrícula** | `SGASTDN` → `SFAREGS` | Reactivación de un participante cuyo expediente o matrícula quedó inactivo o suspendido temporalmente. Se restablece estatus `AS` y se reinscribe el NRC. |
| **10** | **Retorno automático a ciclo anterior** | `SFASLST` → `SHRROLL` → `SFPPROJ` | Alumno desaprueba un módulo (ej. BASIC I o Computación I). Al rolar la nota desaprobatoria, la proyección y prerrequisito fatal lo obligan a repetir el módulo previo antes de avanzar. |
| **11** | **Apertura de periodo** | `SOATERM` → `STVTERM` → `SOAPRPT` | Configuración del nuevo periodo (ej. 202656, 202751), habilitación de partes de periodo mensuales (`I01..I12`, `X01..X07`, `P01..P06`) y ventanas de fechas de matrícula. |
| **12** | **Cierre de periodo** | `SOATERM` → `SHRROLL` → `SMRBCMP` | Cierre de fechas límite de ingreso de notas docentes, pase masivo de calificaciones a historia académica con `SHRROLL` y auditoría CAPP masiva de avance curricular. |
| **13** | **Procesamiento de calificaciones** | `SHAGCOM` → `SFASLST` / Autoservicio | Ponderación de evaluaciones, ingreso de notas parciales y finales por parte del docente (o backoffice en `SFASLST`), control de inhabilitados por inasistencia (`INH` con < 70%). *(Instructivo 7.1.6)*. |
| **14** | **Cierre de curso** | `SSASECT` → `SFASLST` | Cierre administrativo y acta definitiva del NRC. Estatus de sección pasa a cerrado y se bloquea cualquier modificación posterior de notas sin trámite de rectificación. |
| **15** | **Ampliación de cupos** | `SSASECT` (`Enrollment Details` / `Reserved Seats`) | Incremento de la capacidad máxima de un NRC cuando se satura la demanda (ej. de 2 a 25 vacantes). Actualización inmediata de vacantes disponibles en `SSASECQ`. |
| **16** | **División de grupos** | `SSASECT` → `SFAREGS` | Cuando un grupo sobrepasa el aforo del aula/laboratorio: se crea una sección espejo (Sección B o C), se copian parámetros y se realiza traslado masivo de alumnos de un NRC a otro. |
| **17** | **Gestión de horarios** | `SSASECT` → `SIAFAVL` → `SLARSLT` | Programación de bloques de reunión (días, horas 24h, aulas/laboratorios físicos o virtuales) y control de cruces de horario de docentes y estudiantes. |
| **18** | **Otros requerimientos especiales** | `SIAASGN`, `SVASVPR`, `SOAHOLD` | Asignación y control de carga docente lectiva (reemplazo de Excel), trámite de quejas/reclamos estudiantiles y aplicación de sanciones disciplinarias. |

---

## Estado de Validación en TEST (Al 02/10/2026)

* **Completados y validados:**
  * **Script 01 (Matrícula regular):** Validado al 100% con los estudiantes `S00581081` y `S00581091` en NRC `1021` (periodo `202656`).
  * **Script 15 (Gestión de cupos y reservas):** Probado y validado en SSASECT (`SSARRES`), resolviendo errores de cupo nulo y logrando ocupación de 2/2.
  * **Script 06 (Doble programa pregrado / centros):** Probado al admitir al alumno con Study Path 2/4 en `202656`.
  * **Script 13 (Procesamiento de calificaciones):** Probado y validado en `SFASLST` registrando notas aprobatorias (16) y desaprobatorias (10) para el NRC `1021`.
  * **Script 08 (Eliminación / Retiro de matrícula):** Validado al 100% en `SFAREGS` aplicando estatus `DD` al estudiante `S00581091` en NRC `1021`, auditando en `SSASECT` la liberación automática de vacante (`Actual` de 2 a 1, `Remaining` de 0 a 1).
  * **Script 18-A (Auditoría de carga docente):** Validado al 100% en `SIAASGN` con el docente Dagner Chuman (`100582059`) en `202656`, auditando 4 secciones asignadas en Computación (`ESEC`), Especiales (`ESEP`) y Emprendimiento (`ESGE`), demostrando el cálculo nativo de horas semanales, horas de contacto y FTE sin matrices Excel.
  * **Script 18-B (Retenciones y bloqueo de matrícula):** Validado al 100% aplicando en `SOAHOLD` la retención `TT` (*Mora cuota CCEE*), activando la casilla *Inscripción* en `STVHLDD` y auditando en `SFAREGS` el bloqueo fatal de ingreso (`*ERROR* La persona tiene retenciones, no se puede inscribir`).

  * **Script 12 / 14 (Cierre de actas y pase a historia con SHRROLL):** Validado al 100% en `GJAPCTL` (Jobs 8113 y 8114 exitosos) tras resolver la incidencia **`U20`** agregando el Modo **`V`** a las notas de Nivel `C` en `SHAGRDE`. Cierre definitivo y actas completadas.
  * **Script 03 (Matrícula por convalidación externa):** Validado al 100% con la estudiante `S00581111` (*Ana Rojas Vera*), convalidando curso externo `IST150` en `SHATRNS` y pasando a historia académica con registro de grado en `SHRROLL` (Job 8113).
  * **Script 10 (Retorno obligatorio tras desaprobado):** Validado al 100% en CAPP individual (`SMARQCM` → `SMICRLT` / `SMIPOUT`) con `S00581108` (*Carlos Torres Mendoza*, nota 08): Requerimientos y Áreas en «No cumple», créditos ganados 0/4 y curso `ESEC 00650` catalogado como «Curso no usado» (reprobado).
  * **Script 16 (División de grupos / Traslado de sección):** Validado al 100% en `SFAREGS` trasladando a María Ramírez (`S00581109`) de NRC 1026 (`DD`) a NRC 1021 (`RE`), resolviendo `Reserve Closed` ampliando cupo CMEMC38 en `SSARRES` (`SSASECT`) y confirmada en lista `SFASLST`.
  * **Script 09 (Suspensión y reactivación de matrícula):** Validado al 100% comprobando bloqueo fatal de inscripción bajo estatus inactivo (`IS`/`SU`) y restitución inmediata de elegibilidad académica al reactivar como activo (`AS`) en `SGASTDN` / `SFAREGS`.

* **Próximos scripts pendientes (Para siguientes sesiones):**
  * **Script 02:** Matrícula especial con sobrepasos (`SFASRPO` → `SFAREGS`).
  * **Script 04 (Exclusivo Idiomas):** Matrícula por examen de suficiencia (`SOATEST` → `SFAREGS`).
  * **Script 05:** Curso especial para egresados (`SSASECT` → `SFAREGS`).
  * **Script 07:** Tres programas en simultáneo (`SGASTDN` → `SFAREGS`).
  * **Script 11:** Apertura de nuevo periodo (`SOATERM` → `STVTERM`).
  * **Script 17:** Gestión de horarios y cruces (`SSASECT` → `SLARSLT`).
  * **Script 18-C:** Solicitud de servicio / queja estudiantil (`SVASVPR`).
