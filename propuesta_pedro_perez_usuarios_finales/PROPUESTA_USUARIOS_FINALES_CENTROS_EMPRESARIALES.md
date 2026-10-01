# PROPUESTA INSTITUCIONAL: IDENTIFICACIÓN DE USUARIOS FINALES PARA ELLUCIAN BANNER
## CAPACIDAD: CENTROS EMPRESARIALES USS (IDIOMAS, COMPUTACIÓN Y EMPRENDIMIENTO)

> [!CAUTION]
> **ESTADO DEL DOCUMENTO: BORRADOR DE TRABAJO INTERNO (CONFIDENCIAL)**  
> **NO ENVIAR AÚN A PEDRO PÉREZ MARTINTO.**  
> Este documento contiene el mapeo funcional preliminar. Se mantendrá en reserva hasta culminar las pruebas integrales pendientes de: **Asignación formal de docentes (`SIAINST`), Carga horaria lectiva (`SIAASGN`), Ponderaciones de notas (`SHAGCOM`), Asistencia por Autoservicio y Pase a historia (`SHRROLL`)**.

---

### Metadatos del Documento
* **Para:** Pedro Carlos Pérez Martinto (`pedro.perez@uss.edu.pe`) - Coordinador de Implementación Ellucian Banner USS
* **Elaborado por:** Dagner Anibal Chuman Lluen - Coordinación Operativa de Centros Empresariales
* **Alcance:** Exclusivamente **Centros Empresariales (Nivel 5)**:
  1. **Centro de Idiomas** (Inglés: BASIC I..III, INTERMEDIATE I..III).
  2. **Centro de Computación** (Informática: Ofimática ESEC y Especialidades ESEP).
  3. **Centro de Emprendimiento** (Cursos de planes de negocio y proyectos).
* **Fecha de corte de pruebas:** Octubre 2026

---

## 1. Justificación y Alcance de los Centros Empresariales

Los Centros Empresariales de la Universidad Señor de Sipán tienen una dinámica académica particular en Banner Student:
1. **Población Mixta:** Atienden tanto a público externo/participantes libres como a estudiantes regulares de **Pregrado** que deben cumplir con los cursos de Idiomas, Computación y Emprendimiento como **requisito obligatorio de egreso** (Instructivo Capacidad 8).
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

### B. Procesos Pendientes por Configurar y Probar (Lo que falta)
* [ ] **Parametrización de Docentes en `SIAINST`:** Configuración de atributos, departamentos y elegibilidad para dictar en los centros.
* [ ] **Carga Lectiva en `SIAASGN`:** Registro de horas semanales frente a grupo y reemplazo definitivo de las planillas Excel de control de horas docentes.
* [ ] **Esquema de Notas en `SHAGCOM`:** Configuración de componentes de calificación (teoría, práctica, examen final) y regla de inhabilitación por inasistencia (`ATTRGRD` < 70%).
* [ ] **Flujo en Autoservicio Docente:** Pruebas reales de toma de asistencia diaria y carga de actas de notas por parte de los profesores de los 3 centros.
* [ ] **Cierre de Periodo con `SHRROLL`:** Pase de calificaciones finales al historial permanente del alumno (`SHACRSE`).

---

## 3. Clasificación de Usuarios Finales (Niveles A, B, C, D)

Conforme a la metodología solicitada por Pedro Pérez Martinto, se clasifica al personal de los Centros Empresariales:

```
[Nivel C: Power User] ------------> Dagner Anibal Chuman Lluen (Supervisa y audita)
         │
         ├──> [Nivel A: Directos] --> Asistentes de Matrícula (Backoffice) + Docentes (Autoservicio)
         │
         ├──> [Nivel B: Consulta] --> Coordinadores Académicos (Idiomas, Computación, Emprendimiento)
         │
         └──> [Nivel D: Indirectos]-> Dirección de Centros + Decanos de Pregrado (Egresos)
```

### Detalle por Nivel:

#### Nivel C: Usuario Clave (*Power User*)
* **Quién es:** **Dagner Anibal Chuman Lluen** (Responsable Funcional de Centros Empresariales).
* **Rol en la implementación:** Conoce a fondo el modelo de punta a punta, valida parametrizaciones, lidera pruebas integrales en TEST y capacita a los operadores.
* **Pantallas Banner:** Todas las transacciones de los 3 centros (`SSASECT`, `GOAMTCH`, `SAAQUIK`, `SFAREGS`, `SMARQCM`, `GJAPCTL`, `SIAASGN`).
* **Tipo de Capacitación:** **Avanzada / Experto / Soporte de 2do Nivel**.

#### Nivel A: Usuarios Finales Directos
* **Quiénes son:**
  1. **Asistentes de Matrícula y Operadores de Centro:** Personal administrativo encargado de atender al público, crear personas, admitir y matricular en los periodos mensuales.
  2. **Docentes de los 3 Centros (Idiomas, Computación, Emprendimiento):** Profesores que dictan clases en las distintas partes de periodo.
* **Operaciones diarias:**
  - Asistentes: `GOAMTCH` (Personas), `SAAQUIK` (Admisión), `SFAREGS` (Matrícula), `SSASECQ` (Consulta de cupos).
  - Docentes: Portal Autoservicio Banner (asistencia diaria, registro de notas de evaluación continua y actas finales).
* **Tipo de Capacitación:**
  - Asistentes: **Avanzada Operativa**.
  - Docentes: **Básica / Funcional (Autoservicio)**.

#### Nivel B: Usuarios Finales de Consulta
* **Quiénes son:** Coordinadores Académicos de cada área (Coordinador de Idiomas, Coordinador de Computación/Informática, Coordinador de Emprendimiento) y personal de informes/atención al estudiante.
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
| **Registro / Matrícula** | Asistente de Matrícula | Asistente Operativo - Idiomas | **A** | `GOAMTCH`, `SAAQUIK`, `SFAREGS`, `SSASECQ` | Alta (Mensual) | **Alta** | **Avanzada (Backoffice)** |
| **Registro / Matrícula** | Asistente de Matrícula | Asistente Operativo - Computación | **A** | `GOAMTCH`, `SAAQUIK`, `SFAREGS`, `SSASECQ` | Alta (Mensual) | **Alta** | **Avanzada (Backoffice)** |
| **Registro / Matrícula** | Asistente de Matrícula | Asistente Operativo - Emprendimiento | **A** | `GOAMTCH`, `SAAQUIK`, `SFAREGS`, `SSASECQ` | Alta (Mensual) | **Alta** | **Avanzada (Backoffice)** |
| **Cuerpo Docente** | Docente | Docentes de Idiomas (Inglés) | **A** | Autoservicio Docente (Asistencia y Calificaciones) | Diaria / Semanal | **Alta** | **Básica (Autoservicio)** |
| **Cuerpo Docente** | Docente | Docentes de Computación (Ofimática/Espec.) | **A** | Autoservicio Docente (Asistencia y Calificaciones) | Diaria / Semanal | **Alta** | **Básica (Autoservicio)** |
| **Cuerpo Docente** | Docente | Docentes de Emprendimiento | **A** | Autoservicio Docente (Asistencia y Calificaciones) | Diaria / Semanal | **Alta** | **Básica (Autoservicio)** |
| **Coordinación Académica**| Coordinador de Centro | Coordinador de Idiomas | **B** | `SSASECQ`, `SGASTDN`, `SMICRLT`, `SOATERM` | Media | **Media** | **Intermedia (Consulta)** |
| **Coordinación Académica**| Coordinador de Centro | Coordinador de Computación | **B** | `SSASECQ`, `SGASTDN`, `SMICRLT`, `SOATERM` | Media | **Media** | **Intermedia (Consulta)** |
| **Coordinación Académica**| Coordinador de Centro | Coordinador de Emprendimiento | **B** | `SSASECQ`, `SGASTDN`, `SMICRLT`, `SOATERM` | Media | **Media** | **Intermedia (Consulta)** |
| **Dirección** | Directivo | Dirección de Centros Empresariales | **D** | Reportes gerenciales, avance de metas y egreso | Mensual | **Baja** | **Informativa / Ejecutiva** |

---

## 5. Próximos Pasos antes de Remitir a Pedro Pérez

1. **Ejecutar Pruebas de Docentes en TEST:**
   - Crear 2 docentes de prueba adicionales y habilitar estatus en `SIAINST`.
   - Asignar carga lectiva en `SIAASGN` y validar que no genere advertencias de sobrecarga.
2. **Probar Cierre de Notas:**
   - Ingresar notas de prueba simulando desaprobados por nota y por inasistencia (< 70%).
   - Correr proceso `SHRROLL` para verificar que la nota se traslade a `SHACRSE`.
3. **Validación de Nombres Reales:**
   - Una vez que la Jefatura asigne los nombres de los asistentes y coordinadores definitivos de cada centro, reemplazar los roles genéricos por los nombres propios en la matriz.
4. **Emisión de la versión final:**
   - Generar el entregable en PDF formal con la plantilla USS para respuesta oficial a Pedro Pérez.
