# Instructivos Ellucian: USS Centros Empresariales

El usuario, Dagner Anibal Chuman Lluen, trabaja en los **Centros Empresariales** de la Universidad Señor de Sipán: Idiomas/Inglés, Computación/Informática y Emprendimiento. Está documentando cómo pasan de SEUSS a Banner.

## Estructura del repositorio
Mapa completo y «dónde va algo nuevo» en `README.md` (raíz) y ADR-023. En la raíz solo van instrucciones, la publicación del sitio y las carpetas de trabajo.

| Carpeta | Qué hay |
|---|---|
| `CAPACIDAD n/` | Instructivos de Ellucian Banner (PPTX) y scripts de prueba de la USS. No se mueven: el visor depende de sus rutas |
| `visor_instructivos/` | Visor web. El sitio se publica desde la rama `main` en https://centros-empresariales-ellucian.vercel.app (antes Netlify, `publish = "."`); lo que está en otras ramas o solo en local no sale en el sitio. Muestra las diapositivas como imágenes de `diapositivas/`, generadas con `herramientas/diapositivas.py` (ADR-022) |
| `centros/` | **Todo lo propio de cada centro**, en `idiomas/`, `computacion/` y `emprendimiento/`: `datos.json` (fuente única), `README.md` (ficha) y `diagramas/` (HTML, PNG, SVG). Lo común va en `comun/`. Índice: `centros/README.md`; galería: `centros/index.html` |
| `herramientas/` | Solo código: `diagramas/` (generador Archify), `diapositivas.py` (instructivos a imágenes WebP), `validar_conocimiento.py`, `sincronizar_skills.py` y `videos/` (piloto de HyperFrames) |
| `conocimiento/` | Base de conocimiento: `manifest.json`, ADR en `decisiones/` y auditorías. Se abre en Obsidian |
| `docs/` | Entregables por tipo: `dudas/` (preguntas en Word para responder y devolver), `afiches/`, `capacitacion/`, `arquitectura/`, `presentaciones/`, `fuentes/` (CSV de la guía operativa) y `propuesta-usuarios-finales/`. Índice: `docs/README.md` |
| `.claude/skills/` y `.agents/skills/` | Memoria de los agentes; las dos carpetas son iguales |

## Base de conocimiento (léela primero)
Está en `conocimiento/`: `README.md`, `manifest.json` (qué existe) y `decisiones/` (los ADR: por qué se decidió cada cosa).
- **Antes de trabajar:** lee el manifest y los ADR **aceptados** del tema.
- **Un ADR aceptado es una restricción.** Si la tarea lo contradice, **detente y pide revisión explícita** al usuario; nunca lo pases por alto en silencio.
- **Al terminar:** devuelve lo aprendido. Va al registro (C##, U##…), a un ADR nuevo o actualizado si se decidió algo, a `datos.json` o al manifest. Luego ejecuta `python3 herramientas/validar_conocimiento.py`, que debe quedar con 0 errores.

Responde en español.

## Enrutamiento de skills (carga progresiva, ADR-024)
Antes de actuar, cruza el pedido con esta tabla. Elige **una skill principal**; si la tarea necesita otra, encadénala después, nunca todas a la vez. Lee su `SKILL.md` solo cuando vayas a ejecutar el flujo y, de sus `references/` o `scripts/`, abre solo el archivo de la subtarea. Si nada coincide, trabaja con lo general, sin abrir skills que no vienen al caso.

| Si el usuario… | Skill principal | Se encadena después |
|---|---|---|
| Pregunta cómo se hace algo en Banner para los centros (periodo, curso, NRC, malla, matrícula, notas, CAPP) | `arquitectura-centros-empresariales` (abre la guía `references/` del paso) | `centro-<centro>` si es de uno solo |
| Habla solo de un centro (Computación y sus rutas XP, Idiomas, Emprendimiento) | `centro-computacion`, `centro-idiomas` o `centro-emprendimiento` (datos en `centros/<centro>/datos.json`) | `arquitectura-centros-empresariales` para el flujo común |
| Manda una captura de Banner o pregunta «qué pongo aquí» o qué significa un error | `workflow-consultas-banner` | `centro-<centro>` |
| Va a entrar a TEST y pide los pasos o un checklist para validar, o pide que el agente haga la prueba en TEST con el navegador | `workflow-pruebas-test` (con el navegador, abre `references/manejo-banner-test.md`) | `centro-<centro>` |
| Trae notas, fotos, minutas, chats o correcciones de una reunión | `workflow-procesar-reunion` | `preguntas-y-dudas-centros` (registro) |
| Pide preparar preguntas o el Word de dudas, o pregunta qué está confirmado | `preguntas-y-dudas-centros` | `documentos-uss` para el Word |
| Pide un PDF, PPT, Word, Excel, afiche o resumen | `documentos-uss` | `workflow-entregables-uss` para revisar antes de entregar |
| Pide un diagrama del sitio o cambia un dato que sale en los diagramas | `workflow-diagramas-archify` | — |
| Pide un video | `hyperframes` (piloto en `herramientas/videos/`) | — |
| Crea o cambia cualquier archivo (PDF, PPT, Word, Excel, `datos.json`, diagrama, página del sitio) | La skill del tipo de archivo | `ciclo-de-la-ia` al final: abrir, evaluar, corregir |
| Pide «no inventes», «responde solo con base en este documento», «cita la fuente» o «¿estás seguro?» | `ruta-de-escape` | La skill del tema |

- **Siempre (ADR-025):** `ruta-de-escape` para cada dato (fuente citada o «No lo sé») y `ciclo-de-la-ia` para cada archivo (genera → evalúa → corrige). Son transversales: no reemplazan a la skill principal.
- **Antes de afirmar** algo del proyecto, busca en `registro.md` (C##, U##…), no lo leas completo.
- **Respuestas limpias:** no copies el contenido de una skill en la respuesta. Di la decisión, la acción y la cita («instructivo 5.3, diap. 23», «C124», «ADR-009»); los archivos, con enlace relativo del repositorio.
- **Validación final:** `python3 herramientas/validar_conocimiento.py` con 0 errores; además, la de la skill usada (`generar.py` para diagramas, revisión visual para PDF y PPTX).
- **Descripción de una skill nueva:** fórmula «Qué hace… Cuándo usarla… Cuándo no usarla…» en el `description` del `SKILL.md`, con las palabras que diría el usuario.

**Skills:** se editan en `.claude/skills/` y luego se copian a `.agents/skills/` con `python3 herramientas/sincronizar_skills.py --desde claude`. Si las editó Antigravity, usa `--desde agents`. Para comprobar que estén iguales, usa `--check`.

**Diagramas:** no se editan a mano. Se cambia `centros/<centro>/datos.json` o `herramientas/diagramas/plantillas.py` y se ejecuta `python3 herramientas/diagramas/generar.py`.

`AGENTS.md` tiene lo mismo, para otros agentes (por ejemplo Antigravity).

**Git:** los cambios del visor ya se subieron a `main` cuando el usuario lo pidió. No publiques en `main` sin que lo pida.
