# PROPUESTA INSTITUCIONAL: IDENTIFICACIÓN DE USUARIOS FINALES PARA ELLUCIAN BANNER
## CAPACIDAD: CENTROS EMPRESARIALES USS (IDIOMAS, COMPUTACIÓN Y EMPRENDIMIENTO)

> [!CAUTION]
> **ESTADO DEL DOCUMENTO: BORRADOR DE TRABAJO INTERNO (CONFIDENCIAL)**  
> **NO ENVIAR AÚN A PEDRO PÉREZ MARTINTO.**  
> Este documento contiene el mapeo funcional preliminar. Se mantendrá en reserva hasta culminar las pruebas integrales pendientes de: **Asignación formal de docentes (`SIAINST`), Ponderaciones de notas (`SHAGCOM`) y Asistencia y notas por Autoservicio docente**. La carga lectiva (`SIAASGN`) y el pase a historia (`SHRROLL`) ya se validaron en TEST.

---

### Metadatos del Documento
* **Para:** Pedro Carlos Pérez Martinto (`pedro.perez@uss.edu.pe`) - Coordinador de Implementación Ellucian Banner USS
* **Elaborado por:** Dagner Anibal Chuman Lluen - Coordinación Operativa de Centros Empresariales
* **Alcance:** Exclusivamente **Centros Empresariales (Nivel 5)**:
  1. **Centro de Idiomas** (Inglés: BASIC I..III, INTERMEDIATE I..III).
  2. **Centro de Computación** (Informática: Ofimática ESEC y Especialidades ESEP).
  3. **Centro de Emprendimiento** (Cursos de planes de negocio y proyectos).
* **Fecha de corte de pruebas:** 05/10/2026

---

## 1. Justificación y Alcance de los Centros Empresariales

Los Centros Empresariales de la Universidad Señor de Sipán tienen una dinámica académica particular en Banner Student:
1. **Población Mixta (quiénes se matriculan):**
   - **Población de la universidad:** estudiantes de **Pregrado** y **Posgrado** de la USS. En Pregrado, Idiomas, Computación y Emprendimiento son **requisito obligatorio de egreso** (Instructivo Capacidad 8).
   - **Externos:** personas que no son de Pregrado ni de Posgrado de la USS: público en general y estudiantes o egresados de otras universidades. Se registran como persona nueva (`GOAMTCH`) y se admiten en el programa del centro (`SAAQUIK`).
2. **Ciclos Mensuales y Flexibles:** A diferencia de las carreras semestrales, los centros operan con múltiples partes de periodo al año:
   - Idiomas: `IGE` / partes `I01` a `I12`.
   - Computación: `CGE` / partes `X01` a `X07`.
   - Emprendimiento: `EGE` / partes `P01` a `P06`.
3. **Flujo de Matrícula Continua:** Requiere agilidad extrema en la admisión rápida (`SAAQUIK`) y la inscripción directa en sección (`SFAREGS`).

---

## 2. Estado de Validación en TEST (Qué está listo vs. Qué falta)

Antes de consolidar el padrón definitivo de personal a capacitar, se deja constancia del estatus técnico de la capacidad:

### A. Procesos Validados al 100% en Banner TEST
* [x] **Creación y Oferta de NRCs (`SSASECT`, `SSASECQ`):** Programación con los 3 hitos de guardado (datos de curso, aforo de vacantes y horario).
* [x] **Alta de Persona Natural (`GOAMTCH`):** Registro de identidad, homonimias (regla de los 3 clics) y generación de IDs oficiales (`S########`).
* [x] **Admisión Rápida (`SAAQUIK`):** Registro con nivel `C`/`I`/`M` y vinculación a malla curricular base (`CMEMC38`, regla 649).
* [x] **Matrícula Backoffice (`SFAREGS`):** Inscripción en NRC con desbloqueo crítico mediante estatus `EL` y consumo real de vacantes.
* [x] **Auditoría Curricular CAPP (`SMARQCM`, `SMICRLT`, `GJAPCTL`, `GJIREVO`):** Verificación individual y por lotes (`SMRBCMP`) para reflejar avance en autoservicio.
* [x] **Carga Lectiva en `SIAASGN`:** Docente de prueba con sus NRC, horas y FTE (Computación, Script 18-A).
* [x] **Notas y Cierre con `SHRROLL`:** Notas aprobatorias, desaprobatorias e `INH`; pase a historia con los jobs 8113 y 8114 en `GJAPCTL` (Computación, Scripts 12 a 14).
* [x] **Sobrepasos:** Cruce de horario del docente en `SSASECT` y sobrepaso de cupo con `SFAROVR`/`SFASRPO` (Computación, Scripts 02 y 17).

### Avance por centro (scripts de prueba, corte 05/10/2026)
| Centro | Validados | Pendientes | Nota |
| :--- | :--- | :--- | :--- |
| **Computación** | 17 de 19 (el 04 no aplica) | 05 (curso para egresados) y 07 (tres programas) | Ambos esperan datos de la USS |
| **Emprendimiento** | 1 (18-A, carga docente) | Los demás por probar; el 04 por definir | Falta confirmar el programa en TEST |
| **Idiomas** | 0 | Todos por probar | Falta confirmar programa y materia en TEST |

Las pruebas de Computación sirven de modelo: el flujo en Banner es el mismo para los tres centros y solo cambian los códigos.

### B. Procesos Pendientes por Configurar y Probar (Lo que falta)
* [ ] **Parametrización de Docentes en `SIAINST`:** Configuración de atributos, departamentos y elegibilidad para dictar en los centros.
* [ ] **Esquema de Notas en `SHAGCOM`:** Configuración de componentes de calificación (teoría, práctica, examen final) y regla de inhabilitación por inasistencia (`ATTRGRD`; el 70 % es el ejemplo del instructivo, el mínimo real está por confirmar).
* [ ] **Flujo en Autoservicio Docente:** Pruebas reales de toma de asistencia diaria y carga de actas de notas por parte de los profesores de los 3 centros.

---

## 3. Clasificación de Usuarios Finales (Niveles A, B, C, D)

Conforme a la metodología solicitada por Pedro Pérez Martinto, se clasifica al personal de los Centros Empresariales:

```
[Nivel C: Power User] ------------> Dagner Anibal Chuman Lluen (Supervisa y audita)
         │
         ├──> [Nivel A: Directos] --> Jefes, Especialistas y Asistentes (Backoffice), otros con permisos + Docentes (Autoservicio)
         │
         ├──> [Nivel B: Consulta] --> Personal de informes y atención al estudiante
         │
         └──> [Nivel D: Indirectos]-> Dirección de Centros + Decanos de Pregrado (Egresos)
```

### Usuarios administrativos de los centros
Son los **jefes, especialistas y asistentes** de cada centro, **o cualquier otra persona a la que se le den permisos** en Banner. Ellos operan la matrícula de toda la población del centro: estudiantes de Pregrado y Posgrado de la USS y externos.

### Detalle por Nivel:

#### Nivel C: Usuario Clave (*Power User*)
* **Quién es:** **Dagner Anibal Chuman Lluen** (Responsable Funcional de Centros Empresariales).
* **Rol en la implementación:** Conoce a fondo el modelo de punta a punta, valida parametrizaciones, lidera pruebas integrales en TEST y capacita a los operadores.
* **Pantallas Banner:** Todas las transacciones de los 3 centros (`SSASECT`, `GOAMTCH`, `SAAQUIK`, `SFAREGS`, `SMARQCM`, `GJAPCTL`, `SIAASGN`).
* **Tipo de Capacitación:** **Avanzada / Experto / Soporte de 2do Nivel**.

#### Nivel A: Usuarios Finales Directos
* **Quiénes son:**
  1. **Jefes, Especialistas, Asistentes y personal con permisos:** Personal administrativo encargado de atender al público, crear personas, admitir y matricular en los periodos mensuales, tanto a estudiantes de la USS (Pregrado y Posgrado) como a externos.
  2. **Docentes de los 3 Centros (Idiomas, Computación, Emprendimiento):** Profesores que dictan clases en las distintas partes de periodo.
* **Operaciones diarias:**
  - Jefes, Especialistas y Asistentes: `GOAMTCH` (Personas), `SAAQUIK` (Admisión), `SFAREGS` (Matrícula), `SSASECQ` (Consulta de cupos).
  - Docentes: Portal Autoservicio Banner (asistencia diaria, registro de notas de evaluación continua y actas finales).
* **Tipo de Capacitación:**
  - Jefes, Especialistas y Asistentes: **Avanzada Operativa**. Los jefes, además, consultan cupos, estatus y avance (`SSASECQ`, `SGASTDN`, `SMICRLT`, `SOATERM`).
  - Docentes: **Básica / Funcional (Autoservicio)**.

#### Nivel B: Usuarios Finales de Consulta
* **Quiénes son:** Personal de informes y atención al estudiante que solo consulta. Los jefes de centro no van aquí: también matriculan, así que son Nivel A.
* **Operaciones:** Consultar cupos de secciones abiertas (`SSASECQ`), revisar si un alumno tiene condición activa (`SGASTDN`) y auditar el avance de cursos para egreso (`SMICRLT`).
* **Tipo de Capacitación:** **Intermedia / Reportería y Consulta**.

#### Nivel D: Usuarios Finales Indirectos
* **Quiénes son:** Dirección General de Centros Empresariales, Vicerrectorado Académico, Decanos de Facultades y Directores de Escuelas Profesionales.
* **Relación con el sistema:** No digitan transacciones operativas, pero consumen reportes consolidados de egreso (si los alumnos de pregrado cumplieron con inglés y computación para graduarse) y analítica de recaudación.
* **Tipo de Capacitación:** **Informativa / Ejecutiva**.

---

## 4. Matriz Maestra para Plan de Capacitación Institucional

| Área | Rol | Perfil / Puesto Sugerido | Nivel | Funcionalidad Banner | Frecuencia | Criticidad | Capacitación Requerida |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Centros Empresariales** | Responsable Funcional / *Power User* | Dagner Anibal Chuman Lluen | **C** | Flujos 1 al 7 completos (`SSASECT`, `GOAMTCH`, `SAAQUIK`, `SFAREGS`, `CAPP`, `SIAASGN`) | Diaria | **Crítica** | **Avanzada / Especializada** |
| **Administrativa** | Especialista | Especialista de Idiomas | **A** | `GOAMTCH`, `SAAQUIK`, `SFAREGS`, `SFASRPO`, `SSASECQ` | Alta (Mensual) | **Alta** | **Avanzada (Backoffice)** |
| **Administrativa** | Especialista | Especialista de Computación | **A** | `GOAMTCH`, `SAAQUIK`, `SFAREGS`, `SFASRPO`, `SSASECQ` | Alta (Mensual) | **Alta** | **Avanzada (Backoffice)** |
| **Administrativa** | Especialista | Especialista de Emprendimiento | **A** | `GOAMTCH`, `SAAQUIK`, `SFAREGS`, `SFASRPO`, `SSASECQ` | Alta (Mensual) | **Alta** | **Avanzada (Backoffice)** |
| **Administrativa** | Asistente | Asistente de Idiomas | **A** | `GOAMTCH`, `SAAQUIK`, `SFAREGS`, `SSASECQ` | Alta (Mensual) | **Alta** | **Avanzada (Backoffice)** |
| **Administrativa** | Asistente | Asistente de Computación | **A** | `GOAMTCH`, `SAAQUIK`, `SFAREGS`, `SSASECQ` | Alta (Mensual) | **Alta** | **Avanzada (Backoffice)** |
| **Administrativa** | Asistente | Asistente de Emprendimiento | **A** | `GOAMTCH`, `SAAQUIK`, `SFAREGS`, `SSASECQ` | Alta (Mensual) | **Alta** | **Avanzada (Backoffice)** |
| **Administrativa** | Otro personal con permisos | Según los permisos que se le asignen | **A** | Las pantallas que cubran sus permisos | Según asignación | **Media** | **Según funciones** |
| **Cuerpo Docente** | Docente | Docentes de Idiomas (Inglés) | **A** | Autoservicio Docente (Asistencia y Calificaciones) | Diaria / Semanal | **Alta** | **Básica (Autoservicio)** |
| **Cuerpo Docente** | Docente | Docentes de Computación (Ofimática/Espec.) | **A** | Autoservicio Docente (Asistencia y Calificaciones) | Diaria / Semanal | **Alta** | **Básica (Autoservicio)** |
| **Cuerpo Docente** | Docente | Docentes de Emprendimiento | **A** | Autoservicio Docente (Asistencia y Calificaciones) | Diaria / Semanal | **Alta** | **Básica (Autoservicio)** |
| **Administrativa** | Jefe de Centro | Jefe de Idiomas | **A** | `GOAMTCH`, `SAAQUIK`, `SFAREGS`, `SFASRPO`, `SSASECQ`, `SGASTDN`, `SMICRLT`, `SOATERM` | Alta (Mensual) | **Alta** | **Avanzada (Backoffice)** |
| **Administrativa** | Jefe de Centro | Jefe de Computación | **A** | `GOAMTCH`, `SAAQUIK`, `SFAREGS`, `SFASRPO`, `SSASECQ`, `SGASTDN`, `SMICRLT`, `SOATERM` | Alta (Mensual) | **Alta** | **Avanzada (Backoffice)** |
| **Administrativa** | Jefe de Centro | Jefe de Emprendimiento | **A** | `GOAMTCH`, `SAAQUIK`, `SFAREGS`, `SFASRPO`, `SSASECQ`, `SGASTDN`, `SMICRLT`, `SOATERM` | Alta (Mensual) | **Alta** | **Avanzada (Backoffice)** |
| **Dirección** | Directivo | Dirección de Centros Empresariales | **D** | Reportes gerenciales, avance de metas y egreso | Mensual | **Baja** | **Informativa / Ejecutiva** |

---

## 5. Próximos Pasos antes de Remitir a Pedro Pérez

1. **Ejecutar Pruebas de Docentes en TEST:**
   - Crear 2 docentes de prueba adicionales y habilitar estatus en `SIAINST`.
   - Probar asistencia y notas desde el Autoservicio docente.
2. **Plan de Evaluación:**
   - Definir quién carga `SHAGCOM` (Registros Académicos o el centro) y probarlo.
   - *Ya validado en Computación:* desaprobados por nota e `INH`, y pase a historia con `SHRROLL`.
3. **Validación de Nombres Reales:**
   - Una vez que la Jefatura asigne los nombres de los jefes, especialistas, asistentes y demás personal con permisos de cada centro, reemplazar los roles genéricos por los nombres propios en la matriz.
4. **Emisión de la versión final:**
   - Generar el entregable en PDF formal con la plantilla USS para respuesta oficial a Pedro Pérez.
