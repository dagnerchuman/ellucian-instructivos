---
name: workflow-pruebas-test
description: Guía de ejecución, casos de prueba y checklist para pruebas integrales en el ambiente Banner TEST (experience-test.elluciancloud.com/ussipantest). Cubre creación de NRCs, admisión, matrícula, notas, y casuísticas de docentes, quejas y sanciones.
---

# Workflow: Pruebas Integrales en Banner TEST

Este workflow guía y audita la ejecución de pruebas en el ambiente **TEST de Ellucian Banner** (`experience-test.elluciancloud.com/ussipantest`).

## 1. Alcance de Pruebas de los Centros
- **Periodos activos:** 202651 (verano), 202654 (semestre I), 202656 (semestre II).
- **Entidades:** Participantes regulares y de pregrado (que subsanan requisitos de egreso).
- **Centros:** Idiomas (Inglés), Computación (Informática) y Emprendimiento.

## 2. Checklist de Pruebas Básicas

### A. Catálogo y Reglas CAPP
- [ ] Verificar existencia del curso en **SCACRSE** (ej. ESEC 00650 «Ofimática Word 365»).
- [ ] Verificar prerrequisitos en **SCAPREQ** (si exige curso previo o examen de suficiencia).
- [ ] Verificar mallas y reglas en **SMAAREA** (ej. MC38-01 «Ciclo I», regla ECOM-01 «Computación I»).

### B. Programación del NRC (SSASECT)
- [ ] Elegir el periodo correspondiente según fecha de inicio (ej. 202656).
- [ ] Asignar la parte de periodo correcta (X05..X07 para Computación, I08..I12 para Idiomas, P05..P06 para Emprendimiento).
- [ ] Verificar créditos fijos y horas de cobro (sin marcar dispensa).
- [ ] Definir cupo máximo en «Información de ingreso de sección».
- [ ] Registrar bloque de reunión (días, horas inicio/fin en 24h, sesión 01).
- [ ] Asignar docente activo en **SIAINST** con su % de responsabilidad y marca de principal.
- [ ] Guardar y anotar el número de NRC generado.

### C. Admisión e Inscripción
- [ ] Buscar persona en **GOAMTCH** para evitar duplicados de ID.
- [ ] Crear admisión rápida con **SAAQUIK** o solicitud formal en **SAAADMS**.
- [ ] Crear/actualizar registro de estudiante en **SGASTDN**.
- [ ] Inscribir en el NRC mediante **SFAREGS**:
  - Probar caso regular: inscripción exitosa.
  - Probar bloqueo de prerrequisito (Fatal): estudiante sin BASIC I no debe permitir inscribir BASIC II.
  - Probar convalidación/suficiencia: ingresar puntaje en **SOATEST** y reintentar inscripción en SFAREGS.

### D. Enseñanza-Aprendizaje y Cierre
- [ ] Configurar plan de evaluación en **SHAGCOM** (componentes y pesos).
- [ ] Registrar notas y asistencia por autoservicio docente.
- [ ] Probar impacto de inasistencia: estudiante con < 70% de asistencia debe recibir nota INH (desaprobado) vía componente ATTRGRD.
- [ ] Ejecutar pase a historia académica con **SHRROLL**.
- [ ] Ejecutar CAPP masivo con **SMRBCMP** para verificar actualización del estatus del alumno.

## 3. Casuísticas Complejas para Pruebas Integrales
- **Caso D-1 (Fallecimiento de docente a mitad de curso):** Marcar fallecido en SPAIDEN, inactivar en SIAINST, reasignar nuevo docente en SSASECT, verificar traspaso de notas y carga en SIAASGN.
- **Caso D-2 (Docente separado por medida disciplinaria):** Inactivar estatus en SIAINST, desvincular de SSASECT con reemplazo inmediato, registrar retención administrativa.
- **Caso E-1 / Q-1 (Quejas de estudiantes contra docente):** Registrar solicitud de servicio en autoservicio, tramitar en **SVASVPR** con comentarios confidenciales.
- **Caso Q-3 (Sanción disciplinaria a estudiante):** Cambiar estado en **SGASTDN** a «Suspendido» o «Expulsado», registrar retención en **SOAHOLD**. Verificar que SFAREGS bloquee cualquier intento de matrícula.

## 4. Scripts Oficiales de Centros Empresariales (CCEE)
Documento de referencia exhaustivo: `ref-scripts-ccee-casuisticas.md`.

1. **Matrícula regular** (`SFAREGS` / Autoservicio Alumnos) - *Validado en TEST (29/09 y 01/10)*.
2. **Matrícula especial** (`SFASRPO` → `SFAREGS`).
3. **Matrícula por convalidación** (`SHATRNS` → `SHATFAC` → `CAPP`).
4. **Matrícula por examen de suficiencia** (`SOATEST` → `SCAPREQ` / `SSAPREQ` → `SFAREGS`).
5. **Curso especial para egresados** (`SSASECT` → `SGASTDN` → `SFAREGS`).
6. **Matrículas para dos programas en simultáneo** (`SGASTDN` → `SFAREGS`) - *Validado en TEST*.
7. **Matrículas para tres programas en simultáneo** (`SGASTDN` → `SFAREGS`).
8. **Eliminación / Retiro de matrícula** (`SFAREGS` con código `DD`/`DW`).
9. **Reactivación de matrícula** (`SGASTDN` → `SFAREGS`).
10. **Retorno automático a un ciclo anterior** (`SFASLST` → `SHRROLL` → `SFPPROJ`).
11. **Apertura de periodo** (`SOATERM` → `STVTERM` → `SOAPRPT`).
12. **Cierre de periodo** (`SOATERM` → `SHRROLL` → `SMRBCMP`).
13. **Procesamiento de calificaciones** (`SHAGCOM` → `SFASLST` / Autoservicio Docente).
14. **Cierre de curso** (`SSASECT` → `SFASLST`).
15. **Ampliación de cupos** (`SSASECT` `Enrollment Details` / `Reserved Seats`) - *Validado en TEST*.
16. **División de grupos** (`SSASECT` → `SFAREGS`).
17. **Gestión de horarios** (`SSASECT` → `SIAFAVL` → `SLARSLT`).
18. **Otros requerimientos especiales** (`SIAASGN`, `SVASVPR`, `SOAHOLD`).

## 5. Prueba de carga por contrato (ADR-020, propuesto)
Cubre lo que falta del script 5.2: la labor no educativa y SIACONA. Sirve también para decidir si se mide por contrato o por regla de carga (U28-d).
1. **Tablas:**
   - en STVFCNT ya están `ES` y `FC` (C57);
   - en STVCNTR crea un código de regla para cada uno (6 caracteres; por ejemplo `ESP48` y `FAC23`, **de ejemplo**);
   - en STVNIST crea los tipos de labor no educativa (4 caracteres; por ejemplo `MATR` matrícula, `COOR` coordinación y `ATEN` atención a estudiantes, **de ejemplo**).
2. **SIATERM:** en el periodo de Centros (por ejemplo 202656), el factor FTE en 48.
3. **SIAFLCT (cómo llenarlo; instructivo 5.2 Carga de trabajo, diap. 29 a 32):**
   - **Antes:** el código de regla debe existir en STVCNTR, o SIAFLCT no lo acepta.
   - **Bloque llave:**
     - Periodo `202656`;
     - «Copiar «De periodo»» **vacío**: en SFAROVR, poner algo ahí dio error (C42);
     - Tipo de contrato `ES`;
     - **Ir**.
   - **Bloque «Reglas de periodo de contrato de docente»:** marca **Activo** y en **Código de regla de contrato** pon `ESP48`.
   - **Rangos:** solo **«Total de carga de trabajo»**, con Inferior 48 y Superior 48. Lo demás queda vacío; en el ejemplo del instructivo, el rango FTE va vacío. **GUARDAR.**
   - **Facilitador:**
     - vuelve al bloque llave con ⟲ y pon el tipo de contrato `FC`;
     - Activo y regla `FAC23`;
     - solo **«Horas de contacto semanal»**, con Inferior 14 y Superior 23. **GUARDAR.**
   - **Si Banner exige los demás rangos,** pon 0 en Inferior y el tope (48 o 23) en Superior.
   - **Siguiente pantalla:** **SIAFCTR**, para indicar qué periodos cuenta cada contrato (diap. 33 y 34).
4. **SIAINST:** al docente `100582059`, en el bloque «Contrato de docente», el contrato `ES` con su regla y la marca de predefinido.
5. **SIAASGN:**
   - en cada NRC, «Tipo de contrato» `ES`;
   - en la labor no educativa, una fila por función (`MATR`, `COOR`, `ATEN`), con su «Carga de trabajo» y su «Contacto semanal».
6. **SIACONA:** con contrato `ES`, el periodo y el docente:
   - ¿queda debajo (U), dentro o encima (O) de las 48 horas?
   - ¿la carga educativa que viene del catálogo cuadra con las horas por semana?
7. **Para comparar:** en SIAASGN mira también el análisis por regla de carga (SIAFLRT). Con las dos pantallas a la vista se decide cuál es más clara para el jefe, que revisa la carga y da el visto bueno (ADR-011).
