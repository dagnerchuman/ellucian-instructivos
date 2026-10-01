# Guía Oficial: Asignación de Plan (SGASTDN) y Matrícula por Autoservicio Alumnos

Procedimiento oficial probado y validado en el ambiente **TEST de la USS** (30/09/2026) para:
1. Asignar el plan curricular de Centros Empresariales en **SGASTDN** (Admisión / Registros Académicos).
2. Comprender el rol de CAPP y la Proyección Académica.
3. Inscribir asignaturas / NRCs por **Autoservicio Alumnos** desde Ellucian Experience.

---

## 1. Fase Previa en Backoffice: Asignación de Plan en SGASTDN
* **Página:** **SGASTDN (Registro General del Estudiante)**.
* **Bloque clave:**
  * **ID:** ID del estudiante (ej. `100582059` - Dagner Anibal Chuman Lluen).
  * **Periodo:** `202656` (2026-II Seg. Per. Idi. Com. Emp.).
  * Clic en el botón **«Ir»**.
* **Pestaña Curricula (Currículos) - Bloque CURRICULUM:**
  * **Estatus de Actividad:** `ACTIVE`.
  * **Ruta de Estudio (Study Path):** `2` (o correlativo según corresponda).
  * **Programa:** `CMEMC38` («Acreditación Computación XP 01»).
  * **Nivel:** `C` («Computación»).
  * **College (Escuela):** `EM` («Centros Empresariales»).
  * **Campus:** `S` («Sede de Chiclayo»).
  * **Grado:** `000000` («No otorga grado»).
* **Sub-bloque FIELD OF STUDY (Campo de Estudio):**
  * **Tipo:** `MAJOR`.
  * **Estatus:** `INPROGRESS`.
  * **Campo de Estudio (Field of Study):** `ACXP` («Acreditación en Computación XP»).
  * **Departamento:** `EMCI` («Jef. de Centro de Informática»).
  * **Catálogo:** `202656`.
* **Guardar:** Clic en **«GUARDAR»** (abajo a la derecha) → Mensaje de confirmación: `Saved successfully (2 rows saved)`.

---

## 2. Flujo Institucional: CAPP y Proyección
1. **Admisiones:** Asigna el plan de estudios inicial en `SGASTDN` (o mediante `SAAQUIK`).
2. **Registros Académicos:** Actualiza la malla curricular o realiza cambios de versión/plan si aplica.
3. **Ejecución del CAPP (Auditoría Curricular):** Enlaza la malla curricular asignada con la historia del estudiante. Evalúa cursos y notas aprobadas, pasando al récord académico las asignaturas cumplidas y determinando qué materias quedan pendientes.
4. **Proyección Académica (SFPPROJ):** Ejecuta la proyección del periodo para que el sistema identifique exactamente qué cursos y prerrequisitos están habilitados para que el estudiante los matricule.

---

## 3. Consulta de Plan de Estudios (¿Dónde buscar si está registrado?)
* **En Backoffice (Gestión interna):**
  * **SGASTDN:** Poner Periodo e ID → Pestaña *Curricula* → Verificar línea `ACTIVE` con el Programa (`CMEMC38`).
  * **SFAREGS:** Poner Periodo e ID → Bloque *Plan de estudios de ingreso* → Verificar planes asignados (Plan 1, Plan 2).
* **En Autoservicio (Alumno / Portal Web):**
  * En el menú de **Autoservicio Alumnos** → Tarjeta **«Perfil del estudiante»** (*Student Profile*): muestra Nivel, Programa activo y estado académico.

---

## 4. Matrícula en NRC por Autoservicio Alumnos (Ellucian Experience)
1. **Ingreso al Portal:**
   * Entrar a **Ellucian Experience TEST** (`experience-test.elluciancloud.com/ussipantest`).
   * En el menú lateral o categorías, ingresar a **«Autoservicio Alumnos»**.
2. **Acceso al Dashboard de Matrícula:**
   * Localizar la tarjeta **«Matrícula»**.
   * Hacer clic en el botón verde **«OPEN REGISTRATION DASHBOARD»** (*Abrir panel de registro*).
3. **Módulo de Inscripción:**
   * En la pantalla *«Registration - What would you like to do?»*, hacer clic en:
     👉 **«Register for Classes»** *(Inscribirse a clases)*.
4. **Seleccionar Periodo:**
   * Elegir del desplegable: **`202656 - 2026-II Seg. Per. Idi. Com. Emp.`**.
   * Presionar **Continue** *(Continuar)*.
5. **Ingreso del NRC:**
   * Hacer clic en la pestaña superior **«Enter CRNs»** *(Ingresar NRCs)*.
   * Escribir el NRC a matricular (ej. **`1021`** para Ofimática Word 365).
   * Hacer clic en **«Add to Summary»** *(Añadir al resumen)*.
6. **Confirmación y Envío:**
   * En el panel inferior derecho (*Summary*), verificar que aparezca la materia en estado *Pending*.
   * Hacer clic en el botón **«Submit»** *(Enviar)*.
   * El estado cambiará a **«Registered»** (*Inscrito vía web*) y el cupo en el NRC se descontará en tiempo real.
