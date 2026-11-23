# Checklist de pruebas básicas, casuísticas y scripts CCEE

Parte de la skill `workflow-pruebas-test` (el mapa está en su `SKILL.md`).

## 2. Checklist de Pruebas Básicas

### A. Catálogo y Reglas CAPP
- [ ] Verificar existencia del curso en **SCACRSE** (ej. ESEC 00650 «Ofimática Word 365»).
- [ ] Verificar prerrequisitos en **SCAPPRQ**, por programa y periodo de la versión (si exige curso previo o examen de suficiencia). La USS los configura ahí, no en SCAPREQ como enseña el instructivo 1.1.5 (C233).
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
- [ ] Si **SHAGCOM** muestra «Debe configurar los controles del libro de calificaciones en SHAEGBC», buscar **SHAEGBC**, ingresar el periodo, pulsar **Ir**, y configurar fecha abierta/fecha de corte autorizadas antes de volver a SHAGCOM. No inventar fechas. (Instructivo 7.1.4, diap. 40–43.)
- [x] **Script 19 — Computación (validado 23/10/2026):** el usuario confirma que completó y validó en TEST el flujo **SHAEGBC** → **SHAGCOM** para 202656 / NRC 10026 (ESEC 00697, X06). `ATTRGRD`: peso 0.00, **Debe Pasar**, escala propia de asistencia del 70 %; la escala regular `VIG_11` mantiene la nota mínima 11. (Instructivos 7.1.0, diap. 29–30; 7.1.4, diap. 40–43 y 55; C27, C63, C95.)
- [x] **Regla de asistencia en `SOAATRK` (C101, 23/10):** sin una regla del periodo para la parte, el curso o el NRC, el NRC no aparece en Faculty › Control de asistencia. Ejemplo que funcionó: 202656, X06, ESEC 00684, NRC 10044, Desplegar clase ✓, unidad Presente/Ausente, Control de asistencia ✓, del 07-SEP al 31-OCT-2026.
- [ ] **Asistencia docente (referencia):** desde **Banner Search Card** con perfil **Super Role Admin**, buscar `SOAATMT` (reglas por NRC/sesión), `SOAATRK` (reglas por periodo/parte/curso/NRC) y `ENTERATTEND` (proceso de acceso a Autoservicio). Son términos respaldados por el instructivo, pero su disponibilidad en TEST debe comprobarse; no guardar cambios sin verificar periodo y NRC.
- [x] **Faculty › Control de asistencia › Pasar lista** funciona con el NRC 10044 una vez creada la regla en SOAATRK (C101): calcula el porcentaje (86 %).
- [x] **Faculty › Captura de calificaciones › Libro de calificaciones › Componentes** abre el NRC 10044 y guarda notas: TA1 85 de 100 → **17**, visible en el Autoservicio del alumno › Ver calificaciones › Componentes (C102, C103).
- [x] Completar TA2, PA y EF y revisar «Calificaciones compuestas»: con los cuatro en 85 y `ATTRGRD` en 43, porcentaje final 85 y **calificación final INH** (C105).
- [x] La nota compuesta pasa sola a la lista de clase: **SFASLST muestra INH** (C107). «Calificaciones finales» sale «Completado» y sin alumnos para escribir (C106).
- [x] Rolar con `SHRROLL`: NRC 10044 (jobs 7761 y 7762, C121) y NRC 10045 (jobs 7994 en modo A y 7995 en modo U, C190). Con `VIG_11` arriba en SHAGCOM y asistencia ≥ 70 %, la final sale 17 (C188).
- [x] **`ATTRGRD`:** el porcentaje de Pasar lista **no pasa solo**: el docente lo envía con **Clase › «Actualizar la asistencia en el libro de calificaciones» › Sí** (7.1.1, diap. 56–57). Validado con el NRC 10044: 57,14 → INH y 85,71 → APRO (C119). Requiere `GORICCR`, `GORRSQL` y `STVGCHG` con CA (C104).
- [x] Probar impacto de inasistencia: con `ATTRGRD` 43 (< 70 %), la calificación compuesta del NRC 10044 salió **INH** aunque los componentes daban 85 (C105).
- [x] Ejecutar pase a historia académica con **SHRROLL** (C121, C190): primero modo A, se lee el reporte en GJIREVO, y luego modo U.
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
4. **Matrícula por examen de suficiencia** (`SOATEST` → `SCAPPRQ` → `SFAREGS`).
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
