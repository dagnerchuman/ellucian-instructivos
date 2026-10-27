
# Instrucciones para agentes (Antigravity, Claude Code u otros)

## El proyecto

- **Usuario:** Dagner Anibal Chuman Lluen, de los **Centros Empresariales** de la Universidad Señor de Sipán (USS): Idiomas/Inglés, Computación/Informática y Emprendimiento.
- **Qué hace:** documenta y prueba cómo pasan del sistema actual **SEUSS** a **Ellucian Banner Student**.
- **Este repositorio:** instructivos de Ellucian (PPTX, carpetas `CAPACIDAD n`) y un visor web (`visor_instructivos/`, que se publica solo desde la rama `main` en https://centros-empresariales-ellucian.vercel.app, antes en Netlify con `publish = "."`; lo de otras ramas no sale en el sitio).
- **Todo por carpetas:**
  - `centros/<centro>/` (`idiomas`, `computacion`, `emprendimiento`): `datos.json` (**fuente única** de los datos del centro), `README.md` (ficha) y `diagramas/` (HTML interactivo, PNG claro y oscuro, SVG). Lo común va en `centros/comun/`.
  - `herramientas/`: solo código: generador de diagramas (Archify), conversor de instructivos a imágenes (`diapositivas.py`, ADR-022), validador y sincronizador de skills.
  - `docs/`: entregables por tipo (`dudas/`, `afiches/`, `capacitacion/`, `arquitectura/`, `presentaciones/`, `fuentes/`, `propuesta-usuarios-finales/`).
  - Mapa completo y «dónde va algo nuevo»: `README.md` de la raíz y ADR-023.
- **Idioma:** responde **en español**, simple y directo.

## Primero: la base de conocimiento

Está en `conocimiento/`: `README.md`, `manifest.json` (qué existe) y `decisiones/` (los ADR: por qué se decidió cada cosa).

- **Antes de trabajar:** lee el manifest y los ADR **aceptados** del tema.
- **Un ADR aceptado es una restricción.** Si la tarea lo contradice, **detente y pide revisión explícita** al usuario; nunca lo pases por alto en silencio.
- **Al terminar:** devuelve lo aprendido. Va al registro (C##, U##…), a un ADR nuevo o actualizado si se decidió algo, a `datos.json` o al manifest. Luego ejecuta `python3 herramientas/validar_conocimiento.py`, que debe quedar con 0 errores.

## Enrutamiento de skills (carga progresiva, ADR-024)

Antes de actuar, cruza el pedido con esta tabla. Elige **una skill principal**; si la tarea necesita otra, encadénala después, nunca todas a la vez. Lee su `SKILL.md` solo cuando vayas a ejecutar el flujo y, de sus `references/` o `scripts/`, abre solo el archivo de la subtarea (el mapa está en la sección siguiente). Si nada coincide, trabaja con lo general, sin abrir skills que no vienen al caso.

| Si el usuario… | Skill principal | Se encadena después |
|---|---|---|
| Pregunta cómo se hace algo en Banner para los centros (periodo, curso, NRC, malla, matrícula, notas, CAPP) | `arquitectura-centros-empresariales` (abre la guía `references/` del paso) | `centro-<centro>` si es de uno solo |
| Habla solo de un centro (Computación y sus rutas XP, Idiomas, Emprendimiento) | `centro-computacion`, `centro-idiomas` o `centro-emprendimiento` (datos en `centros/<centro>/datos.json`) | `arquitectura-centros-empresariales` para el flujo común |
| Manda una captura de Banner o pregunta «qué pongo aquí» o qué significa un error | `workflow-consultas-banner` | `centro-<centro>` |
| Va a entrar a TEST y pide los pasos o un checklist para validar | `workflow-pruebas-test` | `centro-<centro>` |
| Trae notas, fotos, minutas, chats o correcciones de una reunión | `workflow-procesar-reunion` | `preguntas-y-dudas-centros` (registro) |
| Pide preparar preguntas o el Word de dudas, o pregunta qué está confirmado | `preguntas-y-dudas-centros` | `documentos-uss` para el Word |
| Pide un PDF, PPT, Word, Excel, afiche o resumen | `documentos-uss` | `workflow-entregables-uss` para revisar antes de entregar |
| Pide un diagrama del sitio o cambia un dato que sale en los diagramas | `workflow-diagramas-archify` | — |
| Pide un video | `hyperframes` (piloto en `herramientas/videos/`) | — |

- **Antes de afirmar** algo del proyecto, busca en `registro.md` (C##, U##…), no lo leas completo.
- **Respuestas limpias:** no copies el contenido de una skill en la respuesta. Di la decisión, la acción y la cita («instructivo 5.3, diap. 23», «C124», «ADR-009»); los archivos, con enlace relativo del repositorio.
- **Validación final:** `python3 herramientas/validar_conocimiento.py` con 0 errores; además, la de la skill usada (`generar.py` para diagramas, revisión visual para PDF y PPTX).
- **Descripción de una skill nueva:** fórmula «Qué hace… Cuándo usarla… Cuándo no usarla…» en el `description` del `SKILL.md`, con las palabras que diría el usuario.

## Mapa de la memoria del proyecto (abre solo lo que la tarea necesita)

Está en `.agents/skills/` y es igual a `.claude/skills/`. Son archivos Markdown y cualquier agente puede leerlos. Después de editar una skill, cópiala a la otra carpeta con `python3 herramientas/sincronizar_skills.py --desde agents` (o `--desde claude`). `--check` solo revisa.

1. `.claude/skills/arquitectura-centros-empresariales/SKILL.md`: modelo, periodos, flujo, reglas de trabajo. Referencias en `references/`:
   - Guías operativas paso a paso (según pestañas): `01-creacion-nrc.md`, `02-creacion-de-persona.md`, `03-admision-y-asignacion-al-programa.md`, `04-matricula-en-el-nrc.md`, `05-notas-asigna-docente.md`;
   - Apoyos y consultas: `ref-busqueda-nrc.md`, `ref-admision-capp.md`, `ref-autoservicio-matricula.md`, `ref-acreditacion-computacion.md` (rutas de aprendizaje de Computación), `ref-ruta-inscripcion-y-curso-nuevo.md` (inscribir en la ruta y crear cursos);
   - Documentos de marco: `00-flujo-de-inicio-a-fin.md`, `ref-periodos-y-cronograma.md`, `ref-reglas-ellucian.md`, `ref-paginas-banner.md`, `ref-glosario.md`, `ref-mapa-instructivos.md`, `ref-migracion-r2.md`.
2. `.claude/skills/preguntas-y-dudas-centros/registro.md`: lo **confirmado** (C##), lo **resuelto** con los instructivos (R##), las **dudas abiertas** para Ellucian (E##) y para la USS (U##), y los supuestos descartados (S##). **Mantenlo actualizado.** El método para procesar notas de reuniones está en su `SKILL.md`.
3. `.claude/skills/documentos-uss/SKILL.md`: preferencias del usuario y cómo generar PDF, PPTX y Excel con formato USS.
   - `scripts/pdf/`: pipeline HTML → Chromium; el ejemplo de referencia es `ejemplo_centros.py`.
   - `scripts/pptx/`: piezas para presentaciones con la plantilla USS.
   - `fuentes/`: generadores de todos los entregables hechos.
   - `references/entregables.md`: lista de los entregables.
4. `.claude/skills/workflow-consultas-banner/SKILL.md`: resolver dudas de pantallas Banner (SSASECT, SOATERM, etc.) con citas de instructivos.
5. `.claude/skills/workflow-entregables-uss/SKILL.md`: pipeline y control de calidad de entregables PDF, PPTX y Excel.
6. `.claude/skills/workflow-procesar-reunion/SKILL.md`: procesar notas y minutas de Zoom/reuniones y actualizar registro.md.
7. `.claude/skills/workflow-pruebas-test/SKILL.md`: guía y checklist para pruebas integrales en Banner TEST.
8. `.claude/skills/centro-idiomas/`, `centro-computacion/` y `centro-emprendimiento/`: lo propio de cada centro (antes `centro-ingles` y `centro-informatica`).
9. `.claude/skills/workflow-diagramas-archify/SKILL.md`: diagramas paso a paso por centro con Archify. **No los edites a mano:** cambia `centros/<centro>/datos.json` o `herramientas/diagramas/plantillas.py` y ejecuta `python3 herramientas/diagramas/generar.py`.

## Buscar evidencia en los instructivos

```bash
python3 .claude/skills/arquitectura-centros-empresariales/scripts/buscar_instructivos.py "texto o regex" [--archivo 5.3] [--max 10]
python3 .claude/skills/arquitectura-centros-empresariales/scripts/buscar_instructivos.py --diapositiva "5.3_4.1.4.1.6" 23
```

Cita así: «instructivo 5.3, diap. 23».

## Reglas clave

- **Fuentes:**
  - «**Hoy en SEUSS**» es lo que dice el usuario; no lo interpretes.
  - «**En Ellucian**» es lo que dicen los instructivos, con cita.
  - Todo lo demás es una **duda**: va al registro.
- **No inventes datos de la USS** (códigos de campus, escuelas, programas, nombres de cursos). Si usas un dato ilustrativo, márcalo «de ejemplo».
- **Siglas y códigos**, siempre con su significado entre paréntesis: «NRC (Número de Referencia de Curso)», «SSASECT (Programar NRC)».
- **En los documentos:**
  - pocas tablas;
  - ejemplos de los **tres centros**;
  - estructura «Hoy en SEUSS / En Ellucian / Resultado»;
  - **todas las dudas al final**;
  - autor «Elaborado por: Dagner Anibal Chuman Lluen».
- **Periodos:** año + 5 + secuencia (1 verano, 4 semestre I, 6 semestre II). SEUSS 2026-0 / I / II equivale a 202651 / 202654 / 202656.
- **Inglés:** en SEUSS, quien desaprueba BASIC I no pasa a BASIC II, salvo con examen de suficiencia. Banner lo reproduce con el prerrequisito en «Fatal».
- **No uses** «periodo de 3 meses» para SEUSS: el usuario no lo confirmó. (En Computación, la modalidad Regular de dictado dura 3 meses por curso, C67).

## Referencia Rápida en Memoria (Quick Reference)

> Resumen. Si algo de aquí no coincide con `centros/<centro>/datos.json`, manda `datos.json`: corrige este resumen.

- **Identificadores por Centro (Confirmados en Banner TEST):**
  - **Computación (Informática):** Nivel alumno: `C` (STVLEVL) | Escuela/College: `EM` | Campus: `S` (Chiclayo) | Programa: `CMEMC38` | Mayor: `ACXP` | Depto: `EMCI` | Grado: `000000` | Materia: `ESEC` (Word `00678` NRC 10018, Excel `00679` NRC 10019, `00650`) | Regla currículo: `ECOM-01` (Lib_Area `MC38-01`) | Modos calificación: Catálogo `V`, SHAGRDE `V` (resuelto U20) | **NO rinde** examen de suficiencia (C36) | Partes de periodo: `CGE` / `X01` a `X07` | **Costos y modalidades (C67):** Cursos 1..4 S/ 420 (Regular 3m, Intensivo 2m, Super Intensivo 1m), Taller de certificación S/ 340 (1m fijo). Elección terminal: Curso 4 o Taller.
  - **Idiomas (Inglés):** Nivel alumno: `I` (STVLEVL) | Escuela/College: `EM` | Campus: `S` | Depto: `EMID` | Programas: `IMEMI03` (Acreditación) e `IMEMI05` (TEST con cuotas) | Malla/Área: `MI03-01` (Básicos) / `MI03-02` (Intermedios) | Grado: `000000` | Materia: `ESEP` (C59; también Portugués Posgrado) | Cursos: BASIC I (`02456`), BASIC II (`02457`), BASIC III (`02458`), INTERMEDIATE I (`02693`), INTERMEDIATE II (`02721`), INTERMEDIATE III (`02997`), BEGINNERS I (`04821` NRC 10005) (HT: 4, HP: 3) | Ligas: Teórico Virtual (Sección `AT`, `SAUVIR`, Calificable=Sí, Dispensa=No, Liga `TA`) + Práctica Presencial (Sección `AC1`, Posgrado `SPOSGR`, Calificable=No, Dispensa=Sí, Liga `PA`) + Prácticas Virtuales (Secciones `AC2`/`AC3`, `SAUVIR`, Calificable=No, Dispensa=Sí, Liga `PA`) | **SÍ rinde** examen de suficiencia en `SOATEST` (C11, R03) | Partes de periodo: `IGE` / `I01` a `I12` (ej. `I10`) | **Costos oficiales (C69):** Basic I..II e Intermedio I..II (2 meses, Licencia S/ 80 + Costo S/ 420 = S/ 500); Basic III e Intermedio III (3 meses, Licencia S/ 80 + Costo S/ 560 = S/ 640). Licencia digital X228 fija S/ 80 | **Cuotas SCADETL/SSADETL (C68, C70-C75):** Cuotas diferenciadas si se indica Campus en regla de currículo; si queda en blanco aplica a todos los campus en general. Periodo 202754 probado con NRC 10001 y 10005 (Beginners I matriculado por Autoservicio con estatus RW en SFAREGQ y tasado con éxito en TSAAREV con X032 y X228 por S/ 500, C70-C75).
  - **Emprendimiento:** Nivel alumno: `M` (STVLEVL) | Escuela/College: `EM` | Campus: `S` | Grado: `000000` | Materia: `ESGE` (ej. ESGE 00117) | Todos los grupos duran 10 semanas fijas (P02 y P03 se superponen) | Partes de periodo: `EGE` / `P01` a `P06`.
- **Periodos y Horas:**
  - Códigos: `202651` (verano 2026-0), `202654` (semestre 2026-I), `202656` (semestre 2026-II), `202751` (verano 2027), `202754` (semestre 2027-I).
  - Hora académica en Banner: Factor de duración en `SIATERM` (uno por periodo). En SEUSS: 45 min día, 50 min noche, 60 min presencial.
- **Cadena de Pantallas Banner:**
  - NRC: `SSASECT` (búsqueda: `SSASECQ`, reservas: `SSARRES`, detalle: `SSADETL`)
  - Finanzas / Cuotas de curso y sección: `SCADETL` / `SSADETL` (códigos `X032`, `X228` en bloque `SCRFEES`; reglas de currículo para campus diferenciado o general en blanco) → Población: `GLRSLCT` / `GLAEXTR` → Estimación masiva: `SFRFASC` en `GJAPCTL` → Cuentas: `TSAAREV` (periodo) / `TSADETL` (histórico global) | **Exenciones y Categorías (C77):** Descuentos por categorías socioeconómicas (`TSQEXPT`/`TSAEXPT`: Categoría 1, 2...) son **exclusivos de Pregrado y Posgrado**. En Centros Empresariales **NO HAY CATEGORÍAS** (el único descuento aplicable es por **Pago al Contado**). Planes de pago en catálogo **`STVRATE`** (`CUO01` contado, `CUO02..CUO06`, `CUO1D` diferido 1 cuota, `CUOD3..CUOD5` diferidos). Plan de pagos `I1`/`I3` en `TSAISTC` (`PPLP`/`PPLC`/recargo 5% `A171`, C76); asignación automática por tarifa en **`TSAISTA`** (`CUO03` → plan `I3`) y reglas de cuotas, porcentajes y fechas en **`TSAISTR`** (33.33% y código `X032`, C79); ejecución batch **`TSPISTA`** en `GJAPCTL`, activación en **`TSAISTL`** y cronograma exacto en **`TSAISTP`** (3 cuotas `PPLC` por S/ 420.00 de enseñanza `X032`, C80); flexibilidad de cuotas intra-mes en `TSAISTR` (C81); chat de coordinación ratifica programa `IMEMI03` oficial, inscripción sin pago previo como estándar Banner, GAP de Finanzas para cuotas y estimación en línea en `SOATERM` (C82).
  - Persona: `GOAMTCH` (crea ID `S00...`) → Admisión y Tarifa: `SAAADMS` (asigna tarifa de cuotas `STVRATE`: `CUO01..CUO04` en pestaña *Datos de cuotas*, C78) / `SAAQUIK` / `SGASTDN`
  - Matrícula: `SFAREGS` (código `RE` inscribe en ventanilla, `DD` retira y libera cupo) / Autoservicio Alumnos (`RW` inscribe en web, `DW` retira) | Consulta rápida: `SFAREGQ` | Retenciones: `SOAHOLD` / `STVHLDD`
  - Carga docente: `SIAASGN` (reemplaza planillas Excel)
  - Calificaciones y Cierre: `SFASLST` (ingreso docente) → `SHAGRDE` (escalas) → `GJAPCTL` ejecuta `SHRROLL` (cierre actas e historia)
  - Auditoría curricular: `SMARQCM` / `SMICRLT` (CAPP y avance).

## Mapa Mental de Capacidades e Instructivos (Cap 1 al 11)

- **CAPACIDAD 1: Diseño Curricular** → Periodos (`STVTERM`, `SOATERM`), Cursos catálogo (`SCACRSE`, `SCADETL`), Prerrequisitos y suficiencia (`SCAPREQ`, `SOATEST`), Mallas y programas (`SMAPROG`, `SMAAREA`).
- **CAPACIDAD 3: Admisión y Convalidaciones** → Solicitudes de admisión (`SAAADMS`, `SAAQUIK`), Requisitos de ingreso, Convalidación y equivalencias externas (`SHATRNS`).
- **CAPACIDAD 4: Gestión del Estudiante** → Estados de permanencia (`SGASTDN`), Retenciones administrativas (`SOAHOLD`, `STVHLDD`), Solicitudes de servicio (`SVASVPR`).
- **CAPACIDAD 5: Carga Docente, Programación e Inscripción** → Personas naturales (`GOAMTCH`, `SPAIDEN`), Información docente (`SIAINST`), Carga lectiva (`SIAASGN`), Programar NRC (`SSASECT`, `SSADETL`, `SSARRES`, `SSAPREQ`), Inscripción backoffice (`SFAREGS`).
- **CAPACIDAD 6: Asignar Docentes y Horarios** → Horarios y aulas (`GORINTG`, `SAUVIR`), Docente principal y % responsabilidad en NRC (`SSASECT`).
- **CAPACIDAD 7: Calificaciones y Cierre de Periodo** → Plan de evaluación (`SHAGCOM`), Ingreso de notas (`SFASLST` y Autoservicio), Escalas vigesimales (`SHAGRDE`), Cierre masivo a historia académica (`SHRROLL` en `GJAPCTL`).
- **CAPACIDAD 8: Egreso y Auditoría Curricular (CAPP)** → Evaluación de avance y requisitos de egreso (`SMARQCM`, `SMICRLT`, `SMRBCMP`).
- **CAPACIDAD 9: Tutoría y Asesoría** → Asignación de tutores (`SIAINST`, `SGAADVR`).
- **CAPACIDAD 10: Solicitudes de Servicio Estudiantiles** → Configuración y atención de quejas/trámites (`SVASVPR`).
- **CAPACIDAD 11: Finanzas y Cobranzas** → Códigos de cuota por curso (`SCADETL` > `SCRFEES`), Definición de cobro por curso (`SFARGFE`), Cuentas de alumnos (`TSAAREV`), Caja (`TVACAJA`).

## Los 5 Pasos Operativos de los Centros (Guía Maestra sin búsquedas)

1. **Paso 1: CREACIÓN DE NRC (`SSASECT` / `SSASECQ`)**
   - Acceso: `SSASECT` con Periodo (ej. `202656`) y NRC (o crear nuevo).
   - Encabezado: Materia (`ESEC` / `ESGE`), Curso (`00650` / `00117`), Sección (`A`, `B`, `DC1`), Parte de periodo (`X01..X07`, `I01..I12`, `P01..P06`).
   - Pestaña *Enrollment Details*: Aforo máximo (`Maximum`). Si hay reservas por programa: configurar en `SSARRES`.
   - Pestaña *Meeting Times*: Horario, días y Aula virtual oficial (`SAUVIR` / `SALA VIRT.`).
   - Pestaña *Faculty*: Docente principal (ID institucional, ej. `100582059`), 100% responsabilidad.
2. **Paso 2: CREACIÓN DE PERSONA (`GOAMTCH`)**
   - Acceso: `GOAMTCH` con origen `PERS_NATU` (Persona Natural).
   - Ingresar DNI y nombres/apellidos. Botón *«Marcar-Duplicar»* → *«Crear nuevo»* → *«Guardar»*.
   - Genera ID institucional con prefijo `S` (ej. `S00581081`).
   - Requisitos obligatorios: Dirección institucional (`PP`), Teléfono móvil (`MOV`), Correo personal (`PER1`).
3. **Paso 3: ADMISIÓN, ASIGNACIÓN AL PROGRAMA Y TARIFA DE CUOTAS (`SAAADMS` / `SAAQUIK` / `SGASTDN`)**
   - Acceso: `SAAADMS` (permite asignar en pestaña *Datos de cuotas* la tarifa `STVRATE` ej. `CUO04` 4 cuotas o `CUO01` contado, C78), `SAAQUIK` (rápida) o `SGASTDN` (pestaña *Curricula*).
   - Parámetros: Periodo (ej. `202656`), Nivel alumno (`C` Computación, `I` Idiomas, `M` Emprendimiento), Campus `S` (Chiclayo), Escuela `EM`, Grado `000000`.
   - Programa: ej. `CMEMC38` → autocompleta Mayor `ACXP`, Depto `EMCI`, Estatus `INPROGRESS` o `AS` (Activo).
4. **Paso 4: MATRÍCULA Y RETIROS EN EL NRC (`SFAREGS`)**
   - Acceso: `SFAREGS` con Periodo e ID del alumno.
   - Bloque 1: Autorizar plan de estudios en estatus elegible (`EL`).
   - Bloque 2 (*Información de curso*): Ingresar NRC. Código `RE` inscribe formalmente.
   - Retiro / Drop: Código `DD` (*Drop/Delete*) retira la matrícula y **libera la vacante automáticamente en SSASECT** (`Remaining` suma 1).
   - Bloqueo por mora: Si tiene retención en `SOAHOLD` / `STVHLDD`, `SFAREGS` emite error fatal bloqueando la inscripción.
5. **Paso 5: NOTAS Y CIERRE DE ACTAS (`SFASLST` → `GJAPCTL` / `SHRROLL`)**
   - Registro de notas: Docente ingresa en `SFASLST` (o Autoservicio) con Modo `V` (nota mínima aprobatoria `11`; `≤10` e `INH` desaprueban).
   - Cierre oficial de periodo: En `GJAPCTL` ejecutar `SHRROLL` (con Periodo y NRC). Banner pasa las calificaciones a historia académica (*Rolled to Academic History*).
   - Auditoría CAPP: `SMARQCM` / `SMICRLT` audita cumplimiento curricular; notas reprobadas van a *«Curso no usado»* y bloquean el avance.
