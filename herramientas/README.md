# Herramientas

| Herramienta | Para qué | Uso |
|---|---|---|
| `diagramas/` | Genera los diagramas paso a paso de cada centro (HTML interactivo, PNG claro y oscuro, SVG) a partir de `centros/<centro>/datos.json` | `bash herramientas/diagramas/instalar_archify.sh` y luego `python3 herramientas/diagramas/generar.py` |
| `validar_conocimiento.py` | Revisa la base de conocimiento: enlaces, ADR, manifest, `datos.json`, espejo de skills y datos sensibles | `python3 herramientas/validar_conocimiento.py` (`--estricto` cuenta los avisos como error) |
| `sincronizar_skills.py` | Mantiene iguales `.claude/skills` (Claude Code) y `.agents/skills` (Antigravity) | `--check` revisa · `--desde claude` o `--desde agents` copia en espejo |

## diagramas/
| Archivo | Qué hace |
|---|---|
| `generar.py` | Orquesta todo: escribe la especificación, la valida y compila con `archify finalize`, exporta las imágenes y arma los índices |
| `plantillas.py` | Los 14 diagramas por centro (6 flujos y una casuística por diagrama) y el comparativo. Reglas: un solo flujo, un código por paso y el glosario `TERMINOS` |
| `centro.py` | Lee `datos.json` y arma los textos cortos. Un `null` se muestra como «por confirmar» |
| `indices.py` | `centros/README.md`, `centros/index.html` y la ficha `README.md` de cada centro |
| `exportar.mjs` | Usa el menú «Exportar» del HTML (Playwright y Chromium) para sacar el PNG claro, el PNG oscuro y el SVG |
| `instalar_archify.sh` | Descarga Archify en una versión fija a `diagramas/.archify/`, que no se sube al repositorio |

**Requisitos:**
- Python 3;
- Node 18 o más;
- Playwright con Chromium. Para la prueba en navegador de Archify, define `ARCHIFY_CHROME` con la ruta de Chrome si no la encuentra solo.

**Archify:** © tt-a1i y Cocoon AI, licencia MIT, <https://github.com/tt-a1i/archify>. Se usa sin cambios.

El detalle (reglas de diseño, cómo agregar un diagrama, qué hacer si falla) está en la skill `workflow-diagramas-archify`.
