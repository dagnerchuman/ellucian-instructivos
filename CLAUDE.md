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

Responde en español. Antes de trabajar en el proyecto, usa estas skills:
- `arquitectura-centros-empresariales`: modelo, periodos, flujo, páginas de Banner, reglas con cita y buscador de instructivos.
- `centro-idiomas`, `centro-computacion` y `centro-emprendimiento`: lo propio de cada centro. Sus datos están en `centros/<centro>/datos.json`.
- `preguntas-y-dudas-centros`: qué está confirmado, qué se resolvió y qué dudas siguen abiertas (`registro.md`). Mantenlo actualizado.
- `documentos-uss`: preferencias del usuario y cómo generar PDF, PPTX y Excel con formato USS.
- `workflow-consultas-banner`: resolver dudas de pantallas Banner (SSASECT, SOATERM, SFAREGS, etc.) con citas de instructivos.
- `workflow-entregables-uss`: pipeline de generación y validación de PDF, PPTX y Excel USS sin errores.
- `workflow-diagramas-archify`: diagramas interactivos paso a paso por centro (HTML, PNG y SVG) con Archify.
- `workflow-procesar-reunion`: procesar notas y minutas de Zoom/reuniones y actualizar registro.md.
- `workflow-pruebas-test`: guía y checklist de pruebas integrales en Banner TEST.

**Skills:** se editan en `.claude/skills/` y luego se copian a `.agents/skills/` con `python3 herramientas/sincronizar_skills.py --desde claude`. Si las editó Antigravity, usa `--desde agents`. Para comprobar que estén iguales, usa `--check`.

**Diagramas:** no se editan a mano. Se cambia `centros/<centro>/datos.json` o `herramientas/diagramas/plantillas.py` y se ejecuta `python3 herramientas/diagramas/generar.py`.

`AGENTS.md` tiene lo mismo, para otros agentes (por ejemplo Antigravity).

**Git:** los cambios del visor ya se subieron a `main` cuando el usuario lo pidió. No publiques en `main` sin que lo pida.
