# DOSSIER MAESTRO DE CAPACITACIÓN INSTITUCIONAL: CAPACIDADES 1, 5 Y 7

## Ellucian Banner Student — Universidad Señor de Sipán (USS)

**Autor:** Dagner Anibal Chuman Lluen
**Alcance:** Institucional General (Pregrado, Posgrado y Centros Empresariales)

---

## 1. MARCO Y REGLAS DE NEGOCIO INSTITUCIONALES USS

1. **Escala de Calificaciones:**

   - Escala Vigesimal Oficial: **0 a 20**.
   - Nota mínima aprobatoria: **11**.
   - Notas desaprobatorias: **<= 10** y condición **INH** (Inhabilitado por inasistencia).
   - Modo de calificación en Banner: Modo **V** en `SHAGRDE` y catálogo `SCACRSE`.
2. **Estructura y Codificación de Periodos Académicos (`STVTERM`):**

   - Formato estándar: **[Año (4 dígitos)] + [5] + [Secuencia (1 dígito)]**.
   - Ejemplos USS:
     - `202651`: Periodo Verano (2026-0).
     - `202654`: Semestre Académico I (2026-I).
     - `202656`: Semestre Académico II (2026-II).
     - `202751`: Periodo Verano (2027-0).
3. **Partes de Periodo (`STVPTRM` / `SOATERM`):**

   - En Pregrado Regular: Parte completa `1` (16 semanas) o submódulos.
   - En Posgrado: Partes modulares.
   - En Centros Empresariales:
     - Computación: `CGE` / `X01` a `X07`.
     - Idiomas (Inglés): `IGE` / `I01` a `I12`.
     - Emprendimiento: `EGE` / `P01` a `P06` (10 semanas fijas).
4. **Duración de la Hora Académica:**

   - En Banner se configura en `SIATERM` mediante el *Factor de Duración* (un solo valor por periodo académico).

---

## 2. CAPACIDAD 1: DISEÑO Y ESTRUCTURA CURRICULAR

### 2.1 Definición de Periodos y Control de Fechas

- **`STVTERM` (Tabla de Validación de Periodos):** Crea el código y descripción del periodo (ej. `202654` - Semestre 2026-I), año académico y fechas globales de inicio y fin.
- **`STVPTRM` (Partes de Periodo):** Define las subdivisiones temporales dentro del periodo general.
- **`SOATERM` (Control de Periodo):**
  - Asocia las partes de periodo al ciclo con sus fechas exactas de inicio y fin.
  - Habilita las fechas de inscripción web (Autoservicio Banner SSB).
  - Configura el control de acceso a calificaciones por parte de los docentes.
  - Pestaña **«Verificación de errores de inscripción»**: define las reglas fatales o de alerta para prerrequisitos, límites de repetición y cruces de horario. Casilla clave: *«En progreso»* (permite que una materia en curso cuente temporalmente como prerrequisito cumplido).

### 2.2 Catálogo General de Cursos

- **`SCACRSE` (Catálogo de Cursos):**
  - Código de Materia (Subject) y Número de Curso (ej. `ESEC 00678`, `MED 0101`).
  - Título formal y título abreviado.
  - Horas de contacto: Horas Teóricas (HT), Horas Prácticas (HP) y Horas Laboratorio (HL).
  - Unidades de Crédito: Mínimo, máximo o fijo.
  - Nivel académico permitido (`C` Computación, `I` Idiomas, `M` Emprendimiento, `U` Pregrado, `G` Posgrado).
  - Modo de calificación predeterminado: `V` (Vigesimal).

### 2.3 Prerrequisitos, Corequisitos y Restricciones

- **`SCAPREQ` (Prerrequisitos de Catálogo):**
  - Define qué asignaturas deben estar aprobadas antes de cursar la materia.
  - Calificación mínima requerida (ej. 11 en modo V).
  - Combinación lógica con operadores booleanos `AND` / `OR` y paréntesis.
  - Incorporación de pruebas de suficiencia o exámenes de nivelación (`SOATEST`, ej. suficiencia en idiomas).
- **`SSAPREQ` (Prerrequisitos del NRC):**
  - Permite heredar o ajustar las restricciones curriculares a nivel de sección específica.

### 2.4 Programas Académicos y Mallas Curriculares (CAPP)

- **`SMAPROG` (Malla del Programa):** Configuración del plan de estudios oficial de una carrera o especialidad.
- **`SMAAREA` (Áreas de Cumplimiento Curricular):** Agrupa las materias obligatorias, electivas y requisitos de egreso que evaluará el motor CAPP.
- **`SMAPRLE` / `SOACURR`:** Reglas curriculares y asignación de programas válidos por facultad, campus y nivel.

---

## 3. CAPACIDAD 5: CARGA DOCENTE, PROGRAMACIÓN ACADÉMICA E INSCRIPCIÓN

### 3.1 Gestión de Personas y Alumnos

- **`GOAMTCH` (Búsqueda y Creación de Persona Natural):**
  - Origen: `PERS_NATU`.
  - Búsqueda por DNI/Documento y nombres para evitar duplicidad en la base de datos.
  - Generación del ID institucional único con prefijo `S` (ej. `S00581081`).
  - Registro de datos de contacto mínimos: Dirección institucional (`PP`), Teléfono móvil (`MOV`), Correo electrónico personal (`PER1`).
- **`SPAIDEN` (Identificación General):** Mantenimiento de nombres, apellidos y documentos de identidad.
- **`SGASTDN` (Registro del Estudiante):**
  - Asignación de programa de estudios (`Curricula`), estatus de admisión, campus (`S` Chiclayo) y nivel.

### 3.2 Gestión del Profesorado y Carga Lectiva

- **`SIAINST` (Información de Docentes):**
  - Habilita a la persona como docente institucional (`Docente: Sí`).
  - Tipo de docente, departamento académico y tipo de contrato (tiempo completo, tiempo parcial, por horas).
- **`SIAFLRT` / `SIAFLCT`:** Reglas de carga máxima y mínima por tipo de asignación y contrato.
- **`SIAASGN` (Carga de Trabajo Docente):**
  - Visualización consolidada de todos los NRC asignados al docente en un periodo.
  - Cálculo de horas crédito, horas de contacto semanales y porcentaje de responsabilidad.
- **`SIACONA` (Análisis por Contrato):** Auditoría de cumplimiento de carga según el contrato firmado.

### 3.3 Programación de la Oferta Académica (NRCs)

- **`SSASECT` (Programación de Secciones de Curso):**
  - **Bloque Clave:** Periodo (`202654`) y NRC (automático o asignado).
  - **Encabezado:** Materia, Curso, Sección (`A`, `B`, `01`), Campus (`S`), Escuela y Parte de Periodo.
  - **Pestaña *Enrollment Details*:** Cupo máximo (`Maximum`), reserva de vacantes.
  - **Pestaña *Meeting Times*:** Días de la semana, hora de inicio y fin (formato 24h), aula física (`GORINTG`) o aula virtual (`SAUVIR`).
  - **Pestaña *Faculty*:** Asignación del docente principal (indicador obligatorio de docente principal y % de responsabilidad).
- **`SSARRES` (Reservas de Inscripción):**
  - Reserva cupos específicos para determinadas carreras, escuelas o planes de estudio dentro de un mismo NRC.
- **`SSADETL` (Ligas y Enlaces de Curso):**
  - Configura ligas obligatorias entre clases teóricas y prácticas/laboratorios (ej. Teoría liga `TA` + Práctica liga `PA`).
- **`SSAXLST` (Listas Cruzadas):**
  - Permite agrupar dos o más NRCs de diferentes cursos en un mismo horario, aula y docente con un cupo total compartido.

### 3.4 Inscripción Académica y Matrícula

- **`SFAREGS` (Inscripción por Backoffice):**
  - Consulta y matrícula administrativa por ID de estudiante y Periodo.
  - Código de acción **`RE`** (*Registered*): Inscribe al estudiante y consume 1 vacante en el NRC.
  - Código de acción **`DD`** (*Drop/Delete*): Retira al estudiante del NRC y **libera la vacante de inmediato en `SSASECT`** (`Remaining` suma 1).
- **`SFASRPO` (Permisos de Sobrepaso de Inscripción):**
  - Permite autorizar excepciones puntuales a un alumno: sobrepaso de cupo (*Capacity Override*), sobrepaso de prerrequisito (*Prerequisite Override*) o sobrepaso de cruce de horario (*Time Conflict Override*).
- **`SOAHOLD` (Retenciones Administrativas / Financieras):**
  - Códigos de retención (`STVHLDD`) que impiden la inscripción, consulta de notas o emisión de certificados en caso de mora económica o sanción académica.

---

## 4. CAPACIDAD 7: CALIFICACIONES, ASISTENCIA Y CIERRE DE PERIODO

### 4.1 Plan de Evaluación y Asistencia

- **`SHAGCOM` (Componentes de Evaluación):**
  - Define las ponderaciones oficiales de los criterios evaluativos (ej. Examen Parcial 30%, Trabajos 30%, Examen Final 40%).
- **Gestión de Asistencia:**
  - Registro de asistencia diaria de los alumnos a través del portal de Autoservicio Docente (Banner SSB).
  - Cálculo de porcentaje de inasistencias para aplicación automática de inhabilitación (`INH`).

### 4.2 Registro y Gestión de Calificaciones

- **Autoservicio Docente (Banner SSB):**
  - Canal principal donde el profesor registra las notas parciales y finales de sus NRCs asignados dentro de los plazos establecidos en `SOATERM`.
- **`SFASLST` (Lista de Clase y Calificaciones Backoffice):**
  - Pantalla administrativa de respaldo para revisar o ingresar calificaciones oficiales por parte de Registros Académicos.
  - Validación de escala vigesimal (rango 0 a 20).
  - Manejo de calificaciones incompletas (`INC`) o inhabilitados (`INH`).

### 4.3 Escalas de Calificación (`SHAGRDE`)

- Configuración de la escala vigesimal USS:
  - Valores numéricos del 0 al 20.
  - Indicador de aprobado/desaprobado (Aprobado >= 11; Reprobado <= 10).
  - Indicador de conteo de créditos para el promedio ponderado.

### 4.4 Proceso de Cierre de Periodo y Pase a Historia Académica

- **`GJAPCTL` ejecutando el proceso masivo `SHRROLL`:**
  - Es el proceso oficial que traslada las notas registradas en `SFASLST` hacia la **Historia Académica Oficial** del estudiante (`SHATERM` y `SHACRSE`).
  - Una vez ejecutado `SHRROLL`, las actas quedan cerradas y las notas se vuelven inmutables para el docente (cualquier modificación posterior requiere rectificación formal en `SHATRAM` o `SHACRSE`).

### 4.5 Auditoría Curricular y Avance de Egreso (CAPP)

- **`SMARQCM` (Auditoría CAPP Individual) / `SMRBCMP` (Auditoría Masiva):**
  - Evalúa la historia académica del estudiante contra la malla curricular (`SMAPROG`/`SMAAREA`).
- **`SMICRLT` (Resultado de Cumplimiento Curricular):**
  - Muestra los requerimientos cumplidos (cursos aprobados), requerimientos pendientes y la sección de *«Cursos No Usados»* (asignaturas desaprobadas o electivos excedentes).

---

## 5. RESUMEN DE LA SECUENCIA OPERATIVA COMPLETA (1 → 5 → 7)

```
[1. SOATERM] Apertura de Periodo y Fechas
      ↓
[2. SCACRSE / SCAPREQ] Catálogo de Cursos y Prerrequisitos
      ↓
[3. SIAINST / SIAASGN] Registro y Asignación de Docentes
      ↓
[4. SSASECT / SSARRES] Creación de NRC, Horario, Aulas y Cupos
      ↓
[5. GOAMTCH / SGASTDN] Registro de Persona y Asignación de Programa
      ↓
[6. SFAREGS / SSB] Matrícula en NRC (Código RE)
      ↓
[7. SFASLST / SSB] Dictado y Registro de Calificaciones por Docente
      ↓
[8. GJAPCTL · SHRROLL] Pase Masivo a Historia Académica
      ↓
[9. SMICRLT] Auditoría CAPP y Avance de Egreso
```
