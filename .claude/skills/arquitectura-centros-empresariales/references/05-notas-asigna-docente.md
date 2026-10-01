# Guía Operativa: Asignación Docente, Carga Lectiva y Calificaciones

Esta guía documenta el procedimiento y los requisitos para la asignación de docentes a los NRCs de los Centros Empresariales (Idiomas, Computación y Emprendimiento), el cálculo de su carga horaria, el registro de notas y asistencia por Autoservicio, y el posterior pase a historia académica.

---

## 1. Estado Actual en Pruebas TEST
* **Comprobado:** Creación del docente en `GOAMTCH` (ej. `S00580901`, Liliana Ocampo) y asignación básica en la pestaña «Horario e instructores» de `SSASECT` con 100% de responsabilidad y marca de principal.
* **Pendiente de parametrización institucional:**
  1. Habilitación de contratos y atributos docentes en `SIAINST`.
  2. Asignación y balance formal de carga lectiva en `SIAASGN` (reemplazo de matrices Excel de horas).
  3. Carga del esquema de ponderaciones de notas en `SHAGCOM`.
  4. Pruebas integrales de cierre de actas con `SHRROLL`.

---

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
