# Arquitectura Operativa y Scripts de Prueba Avanzados: Centros Empresariales USS en Ellucian Banner Student

**Elaborado por: Dagner Anibal Chuman Lluen**  
**Centros Empresariales USS:** Centro de Idiomas (Inglés), Centro de Computación (Informática) y Centro de Emprendimiento.  
**Fecha:** 22 de octubre de 2026  
**Entorno de referencia:** Ellucian Banner Student TEST (`experience-test.elluciancloud.com/ussipantest`) y SEUSS.

---

## 1. Instrucción Maestra: Por Qué Centros Empresariales NO es tan Complejo como Pregrado y Posgrado

En las coordinaciones institucionales suele generarse confusión cuando se mezclan conceptos financieros, contables y académicos. Para el equipo de los Centros Empresariales es fundamental tener total claridad sobre la frontera de responsabilidades y la agilidad del modelo:

### A. La Frontera de Responsabilidad: Académica vs. Finanzas
* **Lo que hace el Centro Empresarial (Académico):**
  1. Diseña la programación académica y partes de periodo (`X01..X07`, `I01..I12`, `P01..P06`).
  2. Crea y programa los NRC (Número de Referencia de Curso) en **SSASECT** (Programar NRC) con aforos y docentes.
  3. Asigna la carga lectiva a los docentes en **SIAASGN** (Asignaciones de la facultad) y revisa horarios sin cruces.
  4. Atiende matrículas asistidas en **SFAREGS** (Inscripción de estudiantes) o habilita el Autoservicio Alumnos (`RW`).
  5. Asienta y controla calificaciones en **SFASLST** (Lista de clase) y aprueba actas para su cierre masivo con **SHRROLL** (Pase de calificaciones a historia académica).
* **Lo que hace Créditos, Cobranzas y Finanzas (Económico):**
  1. Define las tarifas de cuotas en **STVRATE** (Código de tasa de cuotas) y códigos de detalle de cobro en **SCADETL** / **SSADETL**.
  2. Diseña los planes de fraccionamiento en **TSAISTA** / **TSAISTR** y corre la asignación batch con **TSPISTA**.
  3. Ejecuta la estimación de cuotas en línea en **SOATERM** o masiva en **SFRFASC** en **GJAPCTL**.
  4. Recauda pagos en caja institucional (**TVACAJA**) o pasarela electrónica.
* **Por qué Centros debe conocerlo:** Porque ante una duda de un estudiante que diga *«me matriculé en la web pero no me sale cuánto pagar»*, el coordinador debe saber que en Banner la matrícula es inmediata (`RW`) y que la selección de cuotas se hace mediante el **GAP de Finanzas**, sin que el Centro tenga que manipular cuentas corrientes.

### B. Comparativa: Pregrado/Posgrado vs. Centros Empresariales

| Dimensión | Pregrado y Posgrado | Centros Empresariales (Idiomas, Computación, Emprendimiento) |
|---|---|---|
| **Estructura Curricular** | Carreras de 5 años (10 ciclos) o maestrías de 2-3 años. Mallas con electivos, menciones y créditos transferibles. | Módulos cortos de 1 a 3 meses (Super Intensivo 1m, Intensivo 2m, Regular 3m). Secuencia lineal directa. |
| **Categorías Socioeconómicas** | **SÍ existen:** 5 o más escalas socioeconómicas (Categoría 1, 2, 3...) configuradas en **TSQEXPT** / **TSAEXPT** calculadas por crédito matriculado. | **NO HAY CATEGORÍAS (C77):** La tarifa es plana institucional por curso (S/ 420 o S/ 560 + S/ 80 de licencia en Idiomas; S/ 420 en Computación; S/ 340 en Taller). |
| **Descuentos Aplicables** | Convenios, becas, traslados, escalas y descuentos especiales. | **Únicamente Descuento por Pago al Contado (C77).** |
| **Condición de Inscripción** | Puede tener bloqueos financieros complejos por créditos mínimos o pensiones acumuladas. | **Inscripción directa (C82):** El alumno se inscribe en la web (`RW`) y Banner asienta la deuda contable en **TSAAREV** automáticamente. |
| **Requisitos de Grado** | Tesis, jurados, sustentación, publicación y carpetas de Bachiller y Título en **SHADEGR**. | Certificación modular o acreditación interna; no otorga grado académico (`Grado 000000`). |

---

## 2. Horarios Masivos, Exámenes y Eliminación de Aplazados

### A. Programación Masiva de Horarios (Ej. 20 horarios entre Lunes y Martes)
* **Hoy en SEUSS:** Se asignaban planillas manuales en Excel con riesgo constante de duplicar aulas virtuales o sobrecargar docentes en horarios simultáneos.
* **En Ellucian Banner:** Cada grupo u horario es un NRC (Número de Referencia de Curso) independiente en **SSASECT** (Programar NRC):
  - Se vincula a su parte de periodo exacta (ej. `I04`, `X01`, `P02`).
  - En la pestaña *Meeting Times* se asigna el día (Lunes, Martes), rango de hora exacta y aula virtual oficial **`SAUVIR`** (SALA VIRT.).
  - En la pestaña *Faculty* se asigna el ID institucional del docente (ej. `100582059`) al 100% de responsabilidad.
  - **Protección antifallos nativa:** Banner audita en tiempo real que ningún docente esté asignado a dos NRCs en el mismo bloque horario (Script 17, C41), evitando solapamientos docentes.

### B. Exámenes: Desaparición de «Aplazados» y Funcionamiento en Banner
* **Hoy en SEUSS:** Existían tres figuras de evaluación extraordinaria: *Extemporáneo*, *Sustitutorio* y *Aplazado*.
* **En Ellucian Banner:**
  1. **El Examen de «Aplazado» ya NO existe:** Banner Student no cuenta con una figura aislada o acta de 'aplazado'.
  2. **Examen Sustitutorio:** Es una evaluación de recuperación formalmente contemplada en el Plan de Evaluación de **SHAGCOM** (Componentes de calificación de curso). Reemplaza automáticamente la nota más baja de teoría o evaluación continua según la fórmula vigesimal (`V`) o centesimal (`C`).
  3. **Examen Extemporáneo:** Es una evaluación concedida a un alumno que justificó documentadamente su inasistencia a una evaluación regular. Se ingresa en la columna correspondiente del acta en **SFASLST** (Lista de clase) o se tramita como solicitud de servicio en **SVASVPR** (Procesamiento de solicitud de servicio).
  4. **Examen de Suficiencia:** Se gestiona en **SOATEST** (Información de examen). **Aplica exclusivamente a Idiomas** para exonerar o avanzar niveles (C11, R03). En **Computación NO aplica examen de suficiencia** (confirmado C36).

---

## 3. Integración con el Aula Virtual OpenLMS (Moodle) y Rectificación de Notas

### A. Circuito de Integración Banner ↔ OpenLMS
1. **Paso 1 (Creación y Enrolamiento):** Cuando el Centro crea el NRC en **SSASECT** con aula **`SAUVIR`** y asigna al docente en **SIAASGN**, el integrador oficial (ILP - Intelligent Learning Platform) aprovisiona el aula virtual en OpenLMS (Moodle), enrolando automáticamente al docente y a los alumnos inscritos en **SFAREGS** (`RW` o `RE`).
2. **Paso 2 (Evaluación en OpenLMS):** El docente califica tareas, foros y exámenes en el libro de calificaciones de Moodle.
3. **Paso 3 (Traspaso a Banner):** Al finalizar el curso, las calificaciones finales se sincronizan hacia Banner y se asientan en la pantalla de actas **SFASLST** (Lista de clase).

### B. ¿Qué Ocurre si hay un Cambio de Nota en OpenLMS?
* **Caso 1: Cambio ANTES del cierre de actas con SHRROLL:**
  - Si el docente corrige una nota en OpenLMS mientras el periodo académico sigue abierto en Banner, el cambio se actualiza en **SFASLST**. Al ejecutar masivamente **SHRROLL** (Pase de calificaciones a historia académica) en **GJAPCTL**, la nota corregida rola limpiamente a la historia académica oficial.
* **Caso 2: Cambio DESPUÉS del cierre de actas con SHRROLL:**
  - Si la calificación ya fue rolada (*Rolled to Academic History = Y*), **OpenLMS (Moodle) NO puede sobreescribir la historia académica de Banner automáticamente**.
  - **Procedimiento institucional:** Se requiere un trámite administrativo de **Rectificación de Calificación**. El expediente pasa a Registros Académicos, quienes asientan la corrección formal directamente en el módulo de historia académica de Banner en **SHATCKN** (Calificación de sección de término de estudiante) / **SHARHSO**, dejando trazabilidad del cambio y usuario responsable.

---

## 4. Auditoría Curricular CAPP y Prerrequisitos Cruzados

### A. ¿CAPP se Evalúa por Curso Individual o por Programa?
* **En Ellucian Banner:** CAPP (**SMARQCM** - Auditoría curricular / **SMICRLT** - Resultados de auditoría) evalúa el **PROGRAMA COMPLETO** (**SMAPROG**) y sus **ÁREAS CURRICULARES** (**SMAAREA**), no asignaturas sueltas.
  - En Idiomas evalúa si completó el área de Básicos (`MI03-01`) o Intermedios (`MI03-02`).
  - En Computación evalúa el cumplimiento de la regla `ECOM-01` en el área `MC38-01`.
  - Si el alumno desaprueba un curso (ej. nota ≤ 10 en modo V), CAPP clasifica la asignatura reprobada en la pestaña **«Cursos no usados»** (Script 10, C37) y marca el requerimiento como *No cumple*.
  - A partir de este diagnóstico de CAPP, el proceso de proyección (**SFPPROJ**) habilita en el Autoservicio Alumnos el curso exacto que le toca llevar en la pestaña *Proyecciones*.

### B. Prerrequisitos Cruzados: ¿Desaprobar Basic I Bloquea Pregrado?
* **Pregunta frecuente:** *«Si un alumno de Ingeniería o Derecho desaprueba Basic I en Idiomas, ¿se le bloquea la matrícula en su carrera de Pregrado?»*
* **Respuesta oficial y técnica:** **¡NO, EN ABSOLUTO!**
  - **Aislamiento por Nivel (STVLEVL):** Pregrado es Nivel **`1`** e Idiomas es Nivel **`I`**.
  - La regla de prerrequisito en condición **Fatal** configurada en **SOATERM** / **SCAPREQ** opera estrictamente dentro del programa de Idiomas: solo le impide inscribirse a **Basic II (`ESEP 02457`)** hasta que apruebe Basic I o rinda suficiencia en **SOATEST**.
  - En Pregrado, el estudiante puede matricularse normalmente en sus cursos de 4.º, 5.º o 6.º ciclo de carrera.
  - **El único punto de contacto es al Egreso (Graduación):** La malla curricular de Pregrado exige en CAPP la acreditación del idioma para tramitar la Carpeta de Grado de Bachiller en **SHADEGR** (Grados y reconocimientos de estudiante, R20). Si no culminó el idioma exigido, CAPP de Pregrado marcará *«Requisito de acreditación de idiomas: No cumple»*, frenando la emisión del grado hasta que regularice su situación en el Centro de Idiomas.

---

## 5. Nuevos Scripts de Prueba y Flujo BPM para Centros Empresariales

Para complementar los Scripts 01 al 18 ya probados, se formulan cuatro nuevos scripts de prueba integral:

### 📋 Script 19: Exámenes Sustitutorios y Extemporáneos en Banner
* **Objetivo:** Validar la configuración del Plan de Evaluación sin figura de aplazados y el reemplazo automático de notas por examen sustitutorio.
* **Pantallas:** **SHAGCOM** (Componentes de calificación) → **SFASLST** (Ingreso de notas) → **GJAPCTL** / **SHRROLL** (Cierre).
* **Casuística:** Alumno con notas regulares 08 y 10. Rinde examen sustitutorio y obtiene 14. Banner recalcula la nota final sustituyendo el 08 y aprobando la asignatura en acta.
* **Resultado:** Acta cerrada con nota final aprobada y 0 menciones a aplazados.

### 📋 Script 20: Sincronización OpenLMS (Moodle) y Rectificación Post-Cierre
* **Objetivo:** Verificar la ingesta de notas desde Moodle y el protocolo ante rectificaciones post-rolado.
* **Pantallas:** OpenLMS (Moodle) → **SFASLST** (Verificación previa) → **SHRROLL** (Rolado) → **SHATCKN** (Rectificación histórica).
* **Casuística:** Curso cerrado con nota 10 en historia académica. Solicitud docente de rectificación aprobada por jefatura. Registros Académicos actualiza en **SHATCKN** a nota 13 sin alterar el resto de NRCs.
* **Resultado:** Auditoría en historia académica con nota rectificada y registro de auditoría.

### 📋 Script 21: Aislamiento de Prerrequisitos entre Centros y Pregrado
* **Objetivo:** Demostrar que la reprobación en un Centro Empresarial no frena la matrícula de Pregrado y auditar el control al egreso en CAPP.
* **Pantallas:** **SFAREGS** (Nivel I con nota 08) → **SFAREGS** (Nivel 1 matricula ciclo regular con éxito) → **SMARQCM** (CAPP Pregrado audita requisito de acreditación).
* **Casuística:** Estudiante reprueba Basic I en Idiomas. Al día siguiente accede a Autoservicio Alumnos e inscribe 22 créditos de su carrera de Ingeniería sin ningún error fatal. Al simular CAPP de egreso, la regla de acreditación figura pendiente.
* **Resultado:** Aislamiento exitoso entre programas y control estricto de graduación en CAPP.

### 📋 Script 22: Flujo Finanzas vs. Académico (GAP de Cuotas y Matrícula en Línea)
* **Objetivo:** Validar la inscripción sin bloqueo de caja y la tasación de cargos en cuenta corriente con estimación en línea.
* **Pantallas:** Autoservicio Alumnos (**RW**) → **SFAREGQ** (Auditoría inmediata) → **SOATERM** (Estimación en línea activa) → **TSAAREV** (Verificación de saldo S/ 500.00).
* **Casuística:** Estudiante nuevo ingresa al portal web, inscribe NRC 10005 (Beginners I). Queda formalmente matriculado (`RW`) y en su estado de cuenta aparece al instante la liquidación de enseñanza (`X032` S/ 420) y licencia digital (`X228` S/ 80) lista para pago inmediato o selección de cuotas por el GAP.
* **Resultado:** Cero fricción entre matrícula académica y pasarela de cobros.

---

## 6. Dudas Abiertas

### A. Para Ellucian
* **E22:** ¿El conector ILP (Intelligent Learning Platform) entre OpenLMS y Banner en la USS está configurado para traspaso bidireccional continuo o por ejecución programada batch?
* **E23:** ¿Qué especificación técnica y servicio API utilizará el GAP de Finanzas para actualizar la tarifa de cuotas (`STVRATE`) seleccionada por el alumno desde el portal web?

### B. Para la USS
* **U29:** ¿Un estudiante que eligió una modalidad de pago (ej. 3 cuotas) para su primer curso (ej. parte de periodo I04), puede cambiar su modalidad de pago si inicia un segundo curso en otra parte de periodo dentro del mismo semestre (ej. I05)? *(Planteada por Sandra Valdiviezo el 22/10/2026)*.
* **U30:** ¿Cuál será el plazo máximo institucional otorgado a los docentes de Centros Empresariales para solicitar rectificaciones de nota en **SHATCKN** tras el cierre de actas con **SHRROLL**?
