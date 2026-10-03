---
name: arquitectura-centros-empresariales
description: Arquitectura y contexto del proyecto de los Centros Empresariales de la Universidad Señor de Sipán (Idiomas/Inglés, Computación/Informática y Emprendimiento) en Ellucian Banner Student. Úsala siempre que se hable de centros empresariales, SEUSS, Banner, periodos 2026xx, partes de periodo, NRC, carga docente, CAPP, notas, asistencia, matrícula, migración R2 o de los instructivos de este repositorio, aunque el usuario no lo pida explícitamente.
---

# Arquitectura: Centros Empresariales USS en Ellucian Banner

## Contexto
- **Usuario:** Dagner Anibal Chuman Lluen, de la Universidad Señor de Sipán (USS). Trabaja en **Centros Empresariales**. Escribe en español informal; responde en español.
- **Proyecto:** la USS pasa del sistema anterior **SEUSS** a **Ellucian Banner Student**. El alcance del usuario es solo Centros Empresariales (nivel **5**):
  - **Idiomas**, que es sobre todo Inglés;
  - **Computación**, también llamada Informática;
  - **Emprendimiento**.
- **Este repositorio:** tiene los instructivos de Ellucian (PPTX) por capacidad y un visor web (`visor_instructivos/`, publicado en Netlify). Mapa en [references/mapa-instructivos.md](references/mapa-instructivos.md).
- **Fuentes de verdad:**
  - Lo que dicen los instructivos se presenta como **«En Ellucian»**.
  - Lo que el usuario cuenta que se hace hoy se presenta como **«Hoy en SEUSS»**.
  - Todo lo demás es una **duda**. Regístrala con la skill `preguntas-y-dudas-centros`.

## El modelo en un minuto
- **Periodo:** año + nivel 5 + secuencia (1 = verano, 4 = semestre I, 6 = semestre II).
  - SEUSS 2026-0, 2026-I y 2026-II equivalen a **202651, 202654 y 202656**.
  - El verano 2027 será **202751**.
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

El flujo completo de 7 fases y 17 pasos está en [references/00-flujo-de-inicio-a-fin.md](references/00-flujo-de-inicio-a-fin.md).

## Datos y diagramas por centro (carpeta `centros/`)
- **Fuente única de datos:** `centros/<centro>/datos.json`, con `<centro>` = `idiomas`, `computacion` o `emprendimiento`. Lo común (periodos, escuela, campus y el catálogo de los 18 scripts) está en `centros/comun/datos.json`. Un `null` significa «por confirmar».
- **Diagramas paso a paso:** `centros/<centro>/diagramas/NN-tema/`, en HTML interactivo, PNG claro y oscuro, y SVG. El comparativo de los tres centros está en `centros/comun/diagramas/00-tres-centros/`, y el índice en `centros/README.md`.
- Para cambiar o regenerar un diagrama, usa la skill `workflow-diagramas-archify`.
- **Skills de cada centro:** `centro-idiomas`, `centro-computacion` y `centro-emprendimiento`.

## Guías operativas paso a paso (siguiendo las pestañas de trabajo del usuario)
| N° | Pestaña / Guía Operativa | Archivo |
|---|---|---|
| **1** | **1.CREACION NRC** (SSASECT) | [references/01-creacion-nrc.md](references/01-creacion-nrc.md) |
| **—** | BUSQUEDA NRC (SSASECQ) | [references/ref-busqueda-nrc.md](references/ref-busqueda-nrc.md) |
| **2** | **2.CREACION DE PERSONA** (GOAMTCH) | [references/02-creacion-de-persona.md](references/02-creacion-de-persona.md) |
| **3** | **3.ADMISION Y ASIGNACION AL PROGRAMA** (SAAQUIK) | [references/03-admision-y-asignacion-al-programa.md](references/03-admision-y-asignacion-al-programa.md) |
| **4** | **4.MATRICULA EN EL NRC** (SFAREGS) | [references/04-matricula-en-el-nrc.md](references/04-matricula-en-el-nrc.md) |
| **—** | ADMISION CAPP (SMARQCM / SMRBCMP) | [references/ref-admision-capp.md](references/ref-admision-capp.md) |
| **5** | **5.NOTAS ASIGNA DOCENTE** (SIAASGN / SHAGCOM) | [references/05-notas-asigna-docente.md](references/05-notas-asigna-docente.md) |

## Documentos de referencia complementarios
| Tema | Archivo |
|---|---|
| Flujo de inicio a fin: fases, pasos, responsables y páginas | [references/00-flujo-de-inicio-a-fin.md](references/00-flujo-de-inicio-a-fin.md) |
| Matrícula por autoservicio del estudiante | [references/ref-autoservicio-matricula.md](references/ref-autoservicio-matricula.md) |
| Periodos, partes de periodo y cronograma 2026 de los tres centros | [references/ref-periodos-y-cronograma.md](references/ref-periodos-y-cronograma.md) |
| Qué dice Ellucian sobre horas, docentes, notas, asistencia y egreso | [references/ref-reglas-ellucian.md](references/ref-reglas-ellucian.md) |
| Directorio de páginas de Banner por proceso y número de instructivo | [references/ref-paginas-banner.md](references/ref-paginas-banner.md) |
| Glosario de siglas y páginas explicadas (para usar entre paréntesis) | [references/ref-glosario.md](references/ref-glosario.md) |
| Mapa de instructivos PPTX del repositorio por capacidad | [references/ref-mapa-instructivos.md](references/ref-mapa-instructivos.md) |
| Parámetros y umbrales de la Migración R2 | [references/ref-migracion-r2.md](references/ref-migracion-r2.md) |

## Buscar evidencia en los instructivos
```bash
S=.claude/skills/arquitectura-centros-empresariales/scripts/buscar_instructivos.py
python3 $S "factor de duración"                  # busca en todos los PPTX (regex, sin mayúsculas)
python3 $S "SOATEST|suficiencia" --archivo 1.1.5  # solo un instructivo
python3 $S --diapositiva "6.2.1 Asignar Docentes" 21   # texto completo de una diapositiva
python3 $S --listar                              # 83 instructivos y cuántas diapositivas tiene cada uno
```
Cita siempre así: «instructivo 5.2 Carga de trabajo docente, diap. 12». El número de diapositiva es el que se ve en PowerPoint.

## Cómo ayudar mientras el usuario trabaja en Banner
- Suele mandar **capturas de la pantalla** y preguntar «¿qué pongo aquí?».
- Responde corto, **campo por campo**, en el orden de la pantalla. Cita la diapositiva del instructivo y di qué hacer si algo no aparece.
- Si no conoces un código de la USS (campus, escuela, programa), dilo y explica cómo buscarlo con «•••». No lo inventes.

## Reglas de trabajo
- **No inventes datos de la USS.** Si no está en los instructivos ni lo dijo el usuario, es una duda. Si usas un dato ilustrativo (nombre de curso, peso de una nota, horario), márcalo «de ejemplo».
- **Nombres de cursos:**
  - De Inglés sí se conocen: BASIC I, II y III; INTERMEDIATE I, II y III.
  - De Computación y Emprendimiento no: el cronograma solo dice «TODOS».
- **Inglés:** en SEUSS, quien desaprueba BASIC I no pasa a BASIC II, salvo con examen de suficiencia. Banner lo reproduce con el prerrequisito en Fatal (ver R09 del registro).
- **No uses «periodo de 3 meses» para SEUSS.** El usuario dijo que no lo sabe. Lo confirmado es que SEUSS tiene 3 periodos al año (0, I y II).
- **Horas:**
  - Según el usuario, la hora de clase dura 45 min de día y 50 min de noche, y cada una cuenta como 1 hora. En Ellucian se llama «hora académica»: es el factor de duración de SIATERM, **un solo valor por periodo**.
  - Ojo con los nombres: están en duda. Revisa la duda U09 del registro.
- **Temas documentados** (presentación + PDF), según la numeración de la conversación con el usuario:
  - Hechos: 0 flujo general, 1 periodos, 2 programación de NRC, 2.1 reglas del NRC, 3 docentes y 4 admisión.
  - Pendientes: 5 inscripción, 6 tutoría, 7 jefatura, 8 docente (asistencia y notas) y 9 finanzas.
  - La lista de entregables está en la skill `documentos-uss`.
