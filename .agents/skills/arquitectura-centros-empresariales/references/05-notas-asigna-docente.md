# Guía Operativa: Asignación Docente, Carga Lectiva y Calificaciones

Esta guía documenta el procedimiento y los requisitos para la asignación de docentes a los NRCs de los Centros Empresariales (Idiomas, Computación y Emprendimiento), el cálculo de su carga horaria, el registro de notas y asistencia por Autoservicio, y el posterior pase a historia académica.

> **Orden de Banner:** sigue la secuencia de pasos y campos documentada para cada pantalla de este flujo. No adelantes campos ni extrapoles a una pantalla el orden de otra; si falta el orden obligatorio, indícalo como pendiente de confirmar.

---

## 1. Estado Actual en Pruebas TEST
* **Comprobado:** Creación del docente en `GOAMTCH` (ej. `S00580901`, Liliana Ocampo) y asignación básica en la pestaña «Horario e instructores» de `SSASECT` con 100% de responsabilidad y marca de principal.
* **Pendiente de parametrización institucional:**
  1. Habilitación de contratos y atributos docentes en `SIAINST`.
  2. Asignación y balance formal de carga lectiva en `SIAASGN` (reemplazo de matrices Excel de horas).
  3. Carga del esquema de ponderaciones de notas en `SHAGCOM`.
  4. Pruebas integrales de cierre de actas con `SHRROLL`.

---

## 1-B. Flujo probado en TEST (NRC 10044, Diseño Web, 23/10/2026)
1. **SSASECT:** crear el NRC. Proyectado va antes de «Lugares reservados»; con el aula virtual, `O` en «Indicador de sobrepaso» del horario; docente principal al 100 % (C97).
2. **SHAEGBC → SHAGCOM:** calendario del periodo y plan de evaluación del sílabo. `ATTRGRD` va con peso 0, Debe aprobar y su escala de asistencia (C98). **La escala de arriba del plan («Asignación de escala de calificación») es la del curso, `VIG_11`, no `AST_70`:** esa escala manda en la nota final; con `AST_70` arriba, la final salió APRO y así pasó a la historia (C120, C123; 7.1.4, diap. 44).
3. **SFAREGS:** el alumno necesita un currículo del nivel del curso. Se puede agregar en la pestaña **Currículos** (`+`, programa, Tab, Guardar) y luego autorizar ese plan de estudios con `EL` antes de inscribir el NRC (C100).
4. **SOAATRK:** regla de control de asistencia para el periodo, la parte, el curso o el NRC. **Sin ella, el NRC no aparece en el control de asistencia de Faculty** (C101).
5. **Faculty › Control de asistencia › Pasar lista:** marcas presente/ausente en fechas pasadas; Banner calcula el porcentaje (C101).
6. **Faculty › Captura de calificaciones › Libro de calificaciones › Componentes:** puntaje sobre 100 → Banner propone la nota vigesimal (85 → 17); guardar con «Captura Original - OE». El alumno lo ve en **Autoservicio › Ver calificaciones › Componentes** (C102, C103).
7. **ATTRGRD:** el porcentaje de asistencia no pasa solo: el docente lo envía en Pasar lista › **Clase › «Actualizar la asistencia en el libro de calificaciones»** › Sí. Validado con el NRC 10044: 57,14 → INH y 85,71 → APRO (C119).

## 2. Flujo Completo Paso a Paso

### Paso 1: Habilitación del Docente en SIAINST
* **Página:** **SIAINST (Información de la Facultad / Docente)**.
* **Parámetros:** ID del Docente + Periodo (ej. `202656`).
* **Verificaciones obligatorias:**
  * Estatus de facultad marcado como **Activo**.
  * Elegibilidad para dictar en la materia correspondiente (`ESEC`, `ESEP`, `ENGL`, etc.).

### Paso 2: Asignación al NRC en SSASECT
* En la pestaña **«Horario e instructores»**, subpestaña **«Instructor»**:
  * Ingresar el ID del docente en la grilla.
  * Colocar porcentaje de responsabilidad: `100%`.
  * Marcar la casilla **«Principal»**.
  * Guardar cambios (3er guardado de SSASECT).

### Paso 3: Asignación y Auditoría de Carga en SIAASGN
* **Quién aprueba (USS, C47):** el jefe del centro asigna al docente en el NRC y da su visto bueno a la carga; luego el **Vicerrectorado Académico** la revisa y aprueba. La constancia va fuera de Banner (C48): oficio en la intranet de la USS (asunto, detalle, observación y adjunto), con número de oficio; el Vicerrector emite la resolución.
* **Página:** **SIAASGN (Asignaciones de la Facultad)**.
* Permite verificar la sumatoria de horas lectivas que acumula el docente en todas sus secciones asignadas durante el periodo:
  * Horas semanales de contacto frente a grupo.
  * Horas crédito acumuladas.
  * Control contra sobrecarga o cruces de horario.

### Paso 4: Configuración de Componentes de Evaluación en SHAGCOM
* **Página:** **SHAGCOM (Componentes de Calificación de Sección)**.
* Define la estructura de evaluación del curso (ej. Examen Teórico, Práctica de Laboratorio, Proyecto Final).
* **Regla de inasistencia:** Configurar el componente `ATTRGRD` para que el alumno con menos del 70% de asistencia quede inhabilitado con estatus `INH`.

### Paso 5: Registro por Autoservicio Docente
* El docente ingresa al portal institucional con sus credenciales Banner.
* Visualiza su lista de NRCs asignados en el periodo.
* **Operaciones diarias:**
  * Registro de asistencia diaria de los participantes.
  * Ingreso de notas parciales y finales.

### Paso 6: Cierre de Actas y Pase a Historia (SHRROLL)
* **Página:** **SHRROLL (Pase a Historia Académica por Lotes)**.
* Una vez que el docente asienta las calificaciones definitivas, Registros Académicos ejecuta `SHRROLL` para transferir las notas de la sección al historial permanente del estudiante (`SHACRSE`), habilitando su avance curricular en CAPP.
