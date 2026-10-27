---
trigger: always_on
description: "Reglas de trabajo y modelo de los Centros Empresariales USS en Banner"
---

# Reglas de Trabajo: Centros Empresariales USS en Ellucian Banner

## 1. Identidad y Contexto
- **Usuario:** Dagner Anibal Chuman Lluen.
- **Área:** Centros Empresariales de la Universidad Señor de Sipán (USS):
  - **Idiomas** (Inglés: BASIC I..III, INTERMEDIATE I..III).
  - **Computación** (Informática: materia ESEC; ESEP es de la escuela CE y está por confirmar, U18).
  - **Emprendimiento**.
- **Proyecto:** Migración del sistema legado **SEUSS** a **Ellucian Banner Student**.
- **Idioma:** Español directo, claro y sin rodeos.

## 2. Separación Estricta de Fuentes de Verdad
1. **«Hoy en SEUSS»**: Lo que dice el usuario que se hace actualmente. No reinterpretarlo.
2. **«En Ellucian»**: Lo que dicen los 83 instructivos oficiales del repositorio. Citar siempre instructivo y diapositiva: «instructivo X.X [Nombre], diap. YY».
3. **«Duda abierta»**: Todo lo que no esté en los instructivos ni confirmado por el usuario. Registrar en `.claude/skills/preguntas-y-dudas-centros/registro.md` (E## para Ellucian, U## para USS).
4. **Prohibido inventar datos de la USS**: Códigos de campus, escuelas, programas o nombres de cursos no confirmados no deben inventarse. Si se usa un dato ilustrativo, marcar claramente como «de ejemplo».

## 3. Modelo Académico de los Centros
- **Periodos (6 dígitos):** Año + 5 (Centros) + Secuencia (1 = verano, 4 = semestre I, 6 = semestre II).
  - 2026-0 = `202651` | 2026-I = `202654` | 2026-II = `202656` | 2027-0 = `202751` | 2027-I = `202754`.
  - **No usar** «periodos de 3 meses» (supuesto descartado S01). En Computación, la modalidad Regular de dictado dura 3 meses por curso (C67).
- **Partes de periodo:**
  - Idiomas: `IGE` / `I01` a `I12`.
  - Computación: `CGE` / `X01` a `X07`.
  - Emprendimiento: `EGE` / `P01` a `P06`.
- **Cursos y NRCs:**
  - El curso del catálogo (**SCACRSE**) se programa como NRC en una parte de periodo en **SSASECT**.
  - Horas crédito y horas cobro se heredan del catálogo.
  - La hora académica se calcula con el factor de duración de **SIATERM** (minutos fijos por periodo).
- **Prerrequisitos en Inglés:**
  - Si desaprueba BASIC I, no pasa a BASIC II salvo con examen de suficiencia en **SOATEST**. En Banner se implementa con regla en **SCAPREQ** / **SSAPREQ** y verificación en **Fatal** en **SOATERM**.

## 4. Estándar de Documentos y Entregables
- Siempre incluir ejemplos de los **tres centros** (Idiomas, Computación, Emprendimiento).
- Estructura fija: «Hoy en SEUSS» / «En Ellucian» / «Resultado».
- Pocas tablas; preferir tarjetas por tema y diagramas de flujo.
- Siglas y nombres de páginas siempre con su significado entre paréntesis en la primera mención: «NRC (Número de Referencia de Curso)», «SSASECT (Programar NRC)».
- Todas las dudas al final, separadas en «Para Ellucian» y «Para la USS».
- Autor obligatorio: «Elaborado por: Dagner Anibal Chuman Lluen».
- Paleta USS: Morado `#7030A0` / `#5C2193`, Verdes `#4EA72E` y `#92D050`. Colores por centro: Idiomas `#7030A0`, Informática `#0E8A5F`, Emprendimiento `#C2501C`.
- En presentaciones PPTX: deben abrir limpiamente en PowerPoint sin requerir reparación.
- En hojas Excel: fórmulas dinámicas verificadas con 0 errores.

## 5. Referencia Rápida en Memoria (Quick Reference)
> Fuente única de los datos de cada centro: `centros/<centro>/datos.json`. Si este resumen no coincide, manda `datos.json`. Los diagramas paso a paso están en `centros/<centro>/diagramas/`; no se editan a mano, se regeneran con `python3 herramientas/diagramas/generar.py`.

- **Computación (Informática):** Nivel alumno: `C` (STVLEVL) | Escuela: `EM` | Campus: `S` (Chiclayo) | Programa: `CMEMC38` | Mayor: `ACXP` | Depto: `EMCI` | Grado: `000000` | Materia: `ESEC` (ej. ESEC 00650) | Regla currículo: `ECOM-01` | Modos calificación: Catálogo `V`, SHAGRDE `V` (resuelto U20) | **NO rinde** examen de suficiencia (C36) | Partes: `CGE` / `X01` a `X07` | **Costos (C67):** Cursos 1..4 S/ 420 (Regular 3m, Intensivo 2m, Super Intensivo 1m), Taller de certificación S/ 340 (1m). Elección terminal: Curso 4 o Taller.
- **Idiomas (Inglés):** Nivel alumno: `I` (STVLEVL) | Escuela: `EM` | Campus: `S` | Grado: `000000` | Cursos conocidos: BASIC I..III, INTERMEDIATE I..III (prerrequisitos en Fatal), BEGINNERS I (`04821` NRC 10005) | **SÍ rinde** examen de suficiencia en `SOATEST` (C11, R03) | Partes: `IGE` / `I01` a `I12` | **Costos oficiales (C69):** Basic I..II e Intermedio I..II (2 meses, Licencia S/ 80 + Costo S/ 420 = S/ 500); Basic III e Intermedio III (3 meses, Licencia S/ 80 + Costo S/ 560 = S/ 640). Licencia digital X228 fija S/ 80 | **Cuotas SCADETL/SSADETL (C68, C70-C75):** Cuotas diferenciadas si se indica Campus en regla de currículo; si queda en blanco aplica a todos los campus en general. Periodo 202754 probado con NRC 10001 y 10005 (Beginners I matriculado por Autoservicio con estatus RW en SFAREGQ y tasado con éxito en TSAAREV con X032 y X228 por S/ 500, C70-C75).
- **Emprendimiento:** Nivel alumno: `M` (STVLEVL) | Escuela: `EM` | Campus: `S` | Grado: `000000` | Materia: `ESGE` (ej. ESGE 00117) | Todos los grupos duran 10 semanas fijas (P02 y P03 se superponen) | Partes: `EGE` / `P01` a `P06`.
- **Periodos:** `202651` (verano 2026-0), `202654` (semestre 2026-I), `202656` (semestre 2026-II), `202751` (verano 2027), `202754` (semestre 2027-I).
- **Pantallas clave:** `SSASECT` (NRC/aforo/reservas `SSARRES`, detalle `SSADETL`) → `SCADETL` / `SSADETL` (cuotas por curso/sección `SCRFEES`, campus diferenciado o general en blanco) → Población: `GLRSLCT` / `GLAEXTR` → Estimación masiva: `SFRFASC` en `GJAPCTL` → `GOAMTCH` (persona `S00...`) → `SAAADMS` (tarifa de cuota `STVRATE` en pestaña *Datos de cuotas*, C78) / `SAAQUIK`/`SGASTDN` (admisión/plan) → `SFAREGS` (`RE` matricula en ventanilla, `DD` retira y libera vacante) / Autoservicio Alumnos (`RW` inscribe en web, `DW` retira) → `SFAREGQ` (consulta rápida de inscripción) → `SOAHOLD` (retenciones) → `TSAAREV` (periodo) / `TSADETL` (histórico global) | **Exenciones y Categorías (C77):** Descuentos por categorías socioeconómicas (`TSQEXPT`/`TSAEXPT`) son **exclusivos de Pregrado y Posgrado**; en Centros Empresariales **NO HAY CATEGORÍAS** (único descuento es por **Pago al Contado**). Catálogo **`STVRATE`** define códigos de planes de cuotas (`CUO01` al contado, `CUO02..CUO06`, `CUO1D` diferido 1 cuota, `CUOD3..CUOD5` diferidos). Plan de pagos `I1`/`I3` en `TSAISTC` (`PPLP`/`PPLC`/recargo 5% `A171`, C76); asignación automática por tarifa en **`TSAISTA`** (`CUO03` → plan `I3`) y reglas de cuotas, porcentajes y fechas en **`TSAISTR`** (33.33% y código `X032`, C79); ejecución batch **`TSPISTA`** en `GJAPCTL`, activación en **`TSAISTL`** y cronograma exacto en **`TSAISTP`** (3 cuotas `PPLC` por S/ 420.00 de enseñanza `X032`, C80); flexibilidad de cuotas en `TSAISTR` intra-mes (C81); chat de coordinación ratifica programa `IMEMI03` oficial, inscripción sin pago previo como estándar Banner, GAP de Finanzas para cuotas y estimación en línea en `SOATERM` (C82) → `SIAASGN` (carga docente) → `SFASLST` (notas) → `GJAPCTL` / `SHRROLL` (cierre actas e historia) → `SMARQCM`/`SMICRLT` (CAPP).

## 6. Mapa Mental de Capacidades (Cap 1 al 11)
- **CAP 1:** Diseño Curricular (`STVTERM`, `SOATERM`, `SCACRSE`, `SCAPREQ`, `SOATEST`, `SMAPROG`, `SMAAREA`).
- **CAP 3:** Admisión y Convalidaciones (`SAAADMS`, `SAAQUIK`, `SHATRNS`).
- **CAP 4:** Gestión del Estudiante (`SGASTDN`, `SOAHOLD`, `STVHLDD`, `SVASVPR`).
- **CAP 5:** Carga Docente, Programación e Inscripción (`GOAMTCH`, `SPAIDEN`, `SIAINST`, `SIAASGN`, `SSASECT`, `SSARRES`, `SFAREGS`).
- **CAP 6:** Asignar Docentes y Horarios (`GORINTG`, `SAUVIR`, docentes en `SSASECT`).
- **CAP 7:** Calificaciones y Cierre de Periodo (`SHAGCOM`, `SFASLST`, `SHAGRDE`, `SHRROLL` en `GJAPCTL`).
- **CAP 8:** Egreso y CAPP (`SMARQCM`, `SMICRLT`, `SMRBCMP`).
- **CAP 9:** Tutoría y Asesoría (`SGAADVR`).
- **CAP 10:** Solicitudes y Servicios (`SVASVPR`).
- **CAP 11:** Finanzas y Cobranzas (`SFARGFE`, `TSAAREV`, `TVACAJA`).

## 7. Los 5 Pasos Operativos de los Centros (Guía Maestra)
1. **Paso 1: Creación de NRC (`SSASECT` / `SSASECQ`):** Periodo (`202656`), Materia (`ESEC`/`ESGE`), Curso, Sección, Parte de periodo (`X01..X07`, `I01..I12`, `P01..P06`), Aforo y reservas (`SSARRES`), Horario con Aula virtual (`SAUVIR`), Docente principal en *Faculty*.
2. **Paso 2: Creación de Persona (`GOAMTCH`):** Origen `PERS_NATU`, Marcar-Duplicar → Crear nuevo → Guardar (genera ID `S0058xxxx`). Requisitos: Dirección (`PP`), Móvil (`MOV`), Correo (`PER1`).
3. **Paso 3: Admisión, Asignación de Plan y Tarifa de Cuotas (`SAAADMS` / `SAAQUIK` / `SGASTDN`):** Periodo, Nivel (`C`/`I`/`M`), Campus `S`, Escuela `EM`, Grado `000000`, Programa `CMEMC38` (autocompleta Mayor `ACXP`, Depto `EMCI`, Estatus `INPROGRESS`/`AS`). En `SAAADMS` pestaña *Datos de cuotas* se vincula la tarifa de cuotas `STVRATE` (`CUO04` 4 cuotas o `CUO01` contado, C78).
4. **Paso 4: Matrícula y Retiros en el NRC (`SFAREGS`):** Autorizar plan (`EL`), ingresar NRC con código `RE` (inscribe). Si se retira: código `DD` libera la vacante automáticamente en `SSASECT`. Si tiene retención en `SOAHOLD`, bloquea con error fatal.
5. **Paso 5: Notas y Cierre de Actas (`SFASLST` → `GJAPCTL` / `SHRROLL`):** Docente califica en `SFASLST` con Modo `V` (aprueba ≥11, desaprueba ≤10). Cierre masivo en `GJAPCTL` ejecutando `SHRROLL` para rolar a historia académica. Auditoría en CAPP con `SMARQCM`/`SMICRLT`.

## 8. Base de conocimiento
- Antes de trabajar, lee `conocimiento/README.md`, `conocimiento/manifest.json` y los ADR aceptados del tema en `conocimiento/decisiones/`.
- Un ADR aceptado es una restricción. Si la tarea lo contradice, detente y pide revisión explícita al usuario.
- Al terminar, actualiza el registro, el ADR, `datos.json` o el manifest según corresponda. Después ejecuta `python3 herramientas/validar_conocimiento.py` (0 errores).

## 9. Enrutamiento de skills (carga progresiva, ADR-024)
- Antes de actuar, cruza el pedido con la tabla «Enrutamiento de skills» de `AGENTS.md` y elige **una skill principal**; si hace falta otra, encadénala después.
- Lee el `SKILL.md` solo al ejecutar el flujo y, de `references/` o `scripts/`, solo el archivo de la subtarea. Si ninguna skill coincide, no abras ninguna.
- No copies el contenido de una skill en la respuesta: di la decisión, la acción y la cita (instructivo y diapositiva, C##, ADR).
