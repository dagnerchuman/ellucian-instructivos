# Instrucciones para agentes (Antigravity, Claude Code u otros)

## El proyecto

- **Usuario:** Dagner Anibal Chuman Lluen, de los **Centros Empresariales** de la Universidad Señor de Sipán (USS): Idiomas/Inglés, Computación/Informática y Emprendimiento.
- **Qué hace:** documenta y prueba cómo pasan del sistema actual **SEUSS** a **Ellucian Banner Student**.
- **Este repositorio:** instructivos de Ellucian (PPTX, carpetas `CAPACIDAD n`) y un visor web (`visor_instructivos/`, que Netlify publica solo desde la rama `main`, con `publish = "."`; lo de otras ramas no sale en el sitio).
- **Todo por carpetas:**
  - `centros/<centro>/` (`idiomas`, `computacion`, `emprendimiento`): `datos.json` (**fuente única** de los datos del centro), `README.md` (ficha) y `diagramas/` (HTML interactivo, PNG claro y oscuro, SVG). Lo común va en `centros/comun/`.
  - `herramientas/`: generador de diagramas (Archify) y sincronizador de skills.
  - `docs/`: documentos sueltos.
- **Idioma:** responde **en español**, simple y directo.

## Primero: la base de conocimiento
Está en `conocimiento/`: `README.md`, `manifest.json` (qué existe) y `decisiones/` (los ADR: por qué se decidió cada cosa).
- **Antes de trabajar:** lee el manifest y los ADR **aceptados** del tema.
- **Un ADR aceptado es una restricción.** Si la tarea lo contradice, **detente y pide revisión explícita** al usuario; nunca lo pases por alto en silencio.
- **Al terminar:** devuelve lo aprendido. Va al registro (C##, U##…), a un ADR nuevo o actualizado si se decidió algo, a `datos.json` o al manifest. Luego ejecuta `python3 herramientas/validar_conocimiento.py`, que debe quedar con 0 errores.

## Antes de responder, lee la memoria del proyecto

Está en `.agents/skills/` y es igual a `.claude/skills/`. Son archivos Markdown y cualquier agente puede leerlos. Después de editar una skill, cópiala a la otra carpeta con `python3 herramientas/sincronizar_skills.py --desde agents` (o `--desde claude`). `--check` solo revisa.

1. `.claude/skills/arquitectura-centros-empresariales/SKILL.md`: modelo, periodos, flujo, reglas de trabajo. Referencias en `references/`:
   - Guías operativas paso a paso (según pestañas): `01-creacion-nrc.md`, `02-creacion-de-persona.md`, `03-admision-y-asignacion-al-programa.md`, `04-matricula-en-el-nrc.md`, `05-notas-asigna-docente.md`;
   - Apoyos y consultas: `ref-busqueda-nrc.md`, `ref-admision-capp.md`, `ref-autoservicio-matricula.md`;
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
- **No uses** «periodo de 3 meses» para SEUSS: el usuario no lo confirmó.

## Referencia Rápida en Memoria (Quick Reference)

> Resumen. Si algo de aquí no coincide con `centros/<centro>/datos.json`, manda `datos.json`: corrige este resumen.

- **Identificadores por Centro (Confirmados en Banner TEST):**
  - **Computación (Informática):** Nivel alumno: `C` (STVLEVL) | Escuela/College: `EM` | Campus: `S` (Chiclayo) | Programa: `CMEMC38` | Mayor: `ACXP` | Depto: `EMCI` | Grado: `000000` | Materia: `ESEC` (ej. ESEC 00650) | Regla currículo: `ECOM-01` | Modos calificación: Catálogo `V`, SHAGRDE `V` (resuelto U20) | **NO rinde** examen de suficiencia (C36) | Partes de periodo: `CGE` / `X01` a `X07`.
  - **Idiomas (Inglés):** Nivel alumno: `I` (STVLEVL) | Escuela/College: `EM` | Campus: `S` | Grado: `000000` | Cursos: BASIC I..III, INTERMEDIATE I..III (prerrequisitos en Fatal) | **SÍ rinde** examen de suficiencia en `SOATEST` (C11, R03) | Partes de periodo: `IGE` / `I01` a `I12`.
  - **Emprendimiento:** Nivel alumno: `M` (STVLEVL) | Escuela/College: `EM` | Campus: `S` | Grado: `000000` | Materia: `ESGE` (ej. ESGE 00117) | Todos los grupos duran 10 semanas fijas (P02 y P03 se superponen) | Partes de periodo: `EGE` / `P01` a `P06`.
- **Periodos y Horas:**
  - Códigos: `202651` (verano 2026-0), `202654` (semestre 2026-I), `202656` (semestre 2026-II), `202751` (verano 2027).
  - Hora académica en Banner: Factor de duración en `SIATERM` (uno por periodo). En SEUSS: 45 min día, 50 min noche, 60 min presencial.
- **Cadena de Pantallas Banner:**
  - NRC: `SSASECT` (búsqueda: `SSASECQ`, reservas: `SSARRES`)
  - Persona: `GOAMTCH` (crea ID `S00...`) → Admisión: `SAAQUIK` / `SGASTDN`
  - Matrícula: `SFAREGS` (código `RE` inscribe, `DD` retira y libera cupo) | Retenciones: `SOAHOLD` / `STVHLDD`
  - Carga docente: `SIAASGN` (reemplaza planillas Excel)
  - Calificaciones y Cierre: `SFASLST` (ingreso docente) → `SHAGRDE` (escalas) → `GJAPCTL` ejecuta `SHRROLL` (cierre actas e historia)
  - Auditoría curricular: `SMARQCM` / `SMICRLT` (CAPP y avance).

## Mapa Mental de Capacidades e Instructivos (Cap 1 al 11)
- **CAPACIDAD 1: Diseño Curricular** → Periodos (`STVTERM`, `SOATERM`), Cursos catálogo (`SCACRSE`), Prerrequisitos y suficiencia (`SCAPREQ`, `SOATEST`), Mallas y programas (`SMAPROG`, `SMAAREA`).
- **CAPACIDAD 3: Admisión y Convalidaciones** → Solicitudes de admisión (`SAAADMS`, `SAAQUIK`), Requisitos de ingreso, Convalidación y equivalencias externas (`SHATRNS`).
- **CAPACIDAD 4: Gestión del Estudiante** → Estados de permanencia (`SGASTDN`), Retenciones administrativas (`SOAHOLD`, `STVHLDD`), Solicitudes de servicio (`SVASVPR`).
- **CAPACIDAD 5: Carga Docente, Programación e Inscripción** → Personas naturales (`GOAMTCH`, `SPAIDEN`), Información docente (`SIAINST`), Carga lectiva (`SIAASGN`), Programar NRC (`SSASECT`, `SSARRES`, `SSAPREQ`), Inscripción backoffice (`SFAREGS`).
- **CAPACIDAD 6: Asignar Docentes y Horarios** → Horarios y aulas (`GORINTG`, `SAUVIR`), Docente principal y % responsabilidad en NRC (`SSASECT`).
- **CAPACIDAD 7: Calificaciones y Cierre de Periodo** → Plan de evaluación (`SHAGCOM`), Ingreso de notas (`SFASLST` y Autoservicio), Escalas vigesimales (`SHAGRDE`), Cierre masivo a historia académica (`SHRROLL` en `GJAPCTL`).
- **CAPACIDAD 8: Egreso y Auditoría Curricular (CAPP)** → Evaluación de avance y requisitos de egreso (`SMARQCM`, `SMICRLT`, `SMRBCMP`).
- **CAPACIDAD 9: Tutoría y Asesoría** → Asignación de tutores (`SIAINST`, `SGAADVR`).
- **CAPACIDAD 10: Solicitudes de Servicio Estudiantiles** → Configuración y atención de quejas/trámites (`SVASVPR`).
- **CAPACIDAD 11: Finanzas y Cobranzas** → Definición de cobro por curso (`SFARGFE`), Cuentas de alumnos (`TSAAREV`), Caja (`TVACAJA`).

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
3. **Paso 3: ADMISIÓN Y ASIGNACIÓN AL PROGRAMA (`SAAQUIK` / `SGASTDN`)**
   - Acceso: `SAAQUIK` (rápida) o `SGASTDN` (pestaña *Curricula*).
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


