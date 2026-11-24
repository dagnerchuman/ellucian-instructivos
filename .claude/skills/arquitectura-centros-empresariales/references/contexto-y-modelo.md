# Centros Empresariales en Banner: contexto, modelo y flujos

Parte de la skill `arquitectura-centros-empresariales` (el mapa está en su `SKILL.md`).

## Contexto
- **Usuario:** Dagner Anibal Chuman Lluen, de la Universidad Señor de Sipán (USS). Trabaja en **Centros Empresariales**. Escribe en español informal; responde en español.
- **Proyecto:** la USS pasa del sistema anterior **SEUSS** a **Ellucian Banner Student**. El alcance del usuario es solo Centros Empresariales (nivel **5**):
  - **Idiomas**, que es sobre todo Inglés;
  - **Computación**, también llamada Informática;
  - **Emprendimiento**.
- **Este repositorio:** tiene los instructivos de Ellucian (PPTX) por capacidad y un visor web (`visor_instructivos/`, publicado en Netlify). Mapa en [references/ref-mapa-instructivos.md](ref-mapa-instructivos.md).
- **Fuentes de verdad:**
  - Lo que dicen los instructivos se presenta como **«En Ellucian»**.
  - Lo que el usuario cuenta que se hace hoy se presenta como **«Hoy en SEUSS»**.
  - Todo lo demás es una **duda**. Regístrala con la skill `preguntas-y-dudas-centros`.

## El modelo en un minuto
- **Periodo:** desde 2027 (producción), año + 2 + secuencia; **202721** es el verano 2027, compartido por los tres centros y creado por Registros (ADR-026, C238).
  - En TEST 2026 fue año + 5 + secuencia (1 = verano, 4 = semestre I, 6 = semestre II): SEUSS 2026-0, 2026-I y 2026-II equivalen a 202651, 202654 y 202656 (ADR-005, reemplazado).
- **Parte de periodo:** cada grupo que empieza en un mes es una parte de periodo con sus propias fechas (STVPTRM, SOATERM).
  - Idiomas: I01 a I12 en 2026 (parte general IGE).
  - Computación: X01 a X07 en 2026 (CGE).
  - Emprendimiento: P01 a P06 en 2026 (EGE).
  - Son los grupos del cronograma 2026. Si en otro año hay más grupos, el código sigue la misma secuencia; no está confirmado hasta qué número.
- **Curso y NRC:** el curso del catálogo (SCACRSE) se programa como **NRC = sección** (SSASECT) dentro de una parte de periodo. El NRC tiene cupo, horario, docentes, reglas y aula virtual.
- **Recorrido del participante:**
  1. Persona (SPAIDEN).
  2. Admisión (SAAQUIK / SAAADMS).
  3. Estudiante (SGASTDN).
  4. CAPP y proyección.
  5. Inscripción (SFAREGS).
  6. Cobro (TSAAREV).
  7. Notas y asistencia (autoservicio).
  8. Cierre (SHRROLL) y paso a la historia académica.
  9. Siguiente nivel.
- **Egreso de pregrado:** idiomas, computación y emprendimiento son **requisitos de egreso** (instructivo 8). Por eso los centros también atienden a estudiantes de pregrado.

## Flujos que dio el usuario
- **Flujo que confirmó en la conversación:**
  1. Periodos/semestres y carga lectiva (Registros Académicos).
  2. Admisión: primero postulantes CEPRE, luego estudiantes.
  3. Tutoría (Registros Académicos).
  4. NRC = secciones; las registran las escuelas.
  5. Jefatura.
  6. Cada docente.
  7. Finanzas.
- **Flujo de su hoja del Zoom:**
  1. Periodos.
  2. Planes curriculares.
  3. Carga lectiva y Registros Académicos (secciones = NRC, horarios).
  4. Matrícula.
  5. Enseñanza-aprendizaje (notas y asistencia).
- **Pruebas que pidieron en el Zoom:** periodos, generación de mallas y programas, creación de NRC, matrículas por backoffice y por autoservicio.

El flujo completo de 7 fases y 17 pasos está en [references/00-flujo-de-inicio-a-fin.md](00-flujo-de-inicio-a-fin.md).

## Datos y diagramas por centro (carpeta `centros/`)
- **Fuente única de datos:** `centros/<centro>/datos.json`, con `<centro>` = `idiomas`, `computacion` o `emprendimiento`. Lo común (periodos, escuela, campus y el catálogo de los 18 scripts) está en `centros/comun/datos.json`. Un `null` significa «por confirmar».
- **Diagramas paso a paso:** `centros/<centro>/diagramas/NN-tema/`, en HTML interactivo, PNG claro y oscuro, y SVG. El comparativo de los tres centros está en `centros/comun/diagramas/00-tres-centros/`, y el índice en `centros/README.md`.
- Para cambiar o regenerar un diagrama, usa la skill `workflow-diagramas-archify`.
- **Skills de cada centro:** `centro-idiomas`, `centro-computacion` y `centro-emprendimiento`.
