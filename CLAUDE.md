# Instructivos Ellucian: USS Centros Empresariales

El usuario, Dagner Anibal Chuman Lluen, trabaja en los **Centros Empresariales** de la Universidad Señor de Sipán: Idiomas/Inglés, Computación/Informática y Emprendimiento. Está documentando cómo pasan de SEUSS a Banner.

## Estructura del repositorio
| Carpeta | Qué hay |
|---|---|
| `CAPACIDAD n/` | Instructivos de Ellucian Banner (PPTX) y scripts de prueba de la USS. No se mueven: el visor depende de sus rutas |
| `visor_instructivos/` | Visor web, que Netlify publica con `publish = "."` |
| `centros/` | **Todo lo propio de cada centro**, en `idiomas/`, `computacion/` y `emprendimiento/`: `datos.json` (fuente única), `README.md` (ficha) y `diagramas/` (HTML, PNG, SVG). Lo común va en `comun/`. Índice: `centros/README.md`; galería: `centros/index.html` |
| `herramientas/` | `diagramas/` (generador Archify) y `sincronizar_skills.py` |
| `docs/` | Documentos sueltos: propuesta de usuarios finales y la skill de Computación exportada |
| `.claude/skills/` y `.agents/skills/` | Memoria de los agentes; las dos carpetas son iguales |

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
