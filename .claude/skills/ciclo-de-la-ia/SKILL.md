---
name: ciclo-de-la-ia
description: >-
  Qué hace: método «Genera → Evalúa → Corrige» para todo archivo que produce el agente (PDF, PPTX,
  Word, Excel, datos.json, registro, diagramas y páginas del sitio): después de crearlo lo abre,
  evalúa sus datos y fórmulas contra la fuente, verifica que se vea bien y, si algo falla, corrige la
  fuente, regenera y vuelve a evaluar hasta que pase. Cuándo usarla: siempre que se cree o cambie un
  archivo, y cuando el usuario diga «ábrelo», «evalúalo», «verifica», «revisa que esté bien» o
  «corrígelo». Cuándo no usarla como principal: para decidir qué contenido lleva un entregable
  (documentos-uss) o qué dato es el correcto (ruta-de-escape); se encadena al final de la skill que
  generó el archivo.
---

# El ciclo de la IA: Genera → Evalúa → Corrige

Enseñado por el usuario (29/10/2026, C155, ADR-025). Un archivo **no está terminado** cuando se crea: está terminado cuando se abrió, se evaluó y pasó.

```
GENERA (el archivo) → EVALÚA (datos, fórmulas, vista) → ¿falla algo? → CORRIGE (la fuente) → vuelve a EVALUAR
                                                     └─ no ─→ REPORTA lo que se verificó y cómo
```

## 1. Genera
- Con el generador del proyecto, no a mano lo que se genera: `generar.py` para diagramas, los `build_*.py` de `documentos-uss/fuentes/` para PDF, PPTX y Word, y `datos.json` para los datos de cada centro.
- Anota de qué fuente sale cada dato (C##, instructivo y diapositiva, captura, `datos.json`). Sin fuente, el dato no entra (`ruta-de-escape`).

## 2. Evalúa: abrir el archivo de verdad
Lee, renderiza o ejecuta el archivo. Que el script haya terminado sin error no cuenta como revisión.

| Archivo | Cómo se abre y se evalúa |
|---|---|
| **PDF** | `pdfinfo` (páginas, autor); `pdftotext` para buscar el texto y los datos clave; `pdftoppm -r 60 -png` y **mirar cada página** (cortes, páginas casi vacías, tablas partidas); `check_pdf()` de `documentos-uss/scripts/pdf/common.py`. Compara con la versión anterior (`git show HEAD:<ruta>`): si cambió el número de páginas o aparecen avisos nuevos, averigua por qué |
| **PPTX / DOCX** | Abrir con `python-pptx` o `python-docx` (que no esté corrupto); `soffice --headless --convert-to pdf` y mirar las páginas como un PDF; que abra sin «reparar» (`workflow-entregables-uss`) |
| **Excel** | Las fórmulas se **recalculan**: `soffice --headless --convert-to xlsx` y luego `openpyxl` con `data_only=True`. Ninguna celda con `#REF!`, `#DIV/0!`, `#VALUE!` o `#NAME?`; cada total se **recalcula aparte** (por ejemplo, los pesos de SHAGCOM suman 100 %: 15 + 15 + 40 + 30) |
| **datos.json** | `json.load`; campos del contrato de `conocimiento/manifest.json`; sangría 2 (un `git diff --stat` enorme delata un cambio de formato); luego `python3 herramientas/diagramas/generar.py` |
| **Diagramas y sitio** | `generar.py` con **0 fallas y 0 advertencias**; abrir las páginas en Chromium (Playwright): sin errores de JavaScript, sin 404 ni desborde horizontal, en claro, oscuro y celular; captura de pantalla y **mirarla** |
| **Registro, skills, ADR** | `python3 herramientas/validar_conocimiento.py` (0 errores) y `python3 herramientas/sincronizar_skills.py --check` |
| **Pasos para TEST** | Antes de darlos, compararlos con la guía de `references/` (por ejemplo, `01-creacion-nrc.md` tiene **todos** los campos de SSASECT) y con lo ya probado (C##). No resumir campos obligatorios |

**Evalúa también los datos, no solo el formato:** cada número, código, fecha y nombre del archivo se compara con su fuente. Una cita (C##) tiene que decir lo que se afirma.

## 3. Corrige
- Corrige la **fuente** (plantilla, `datos.json`, generador), nunca solo la salida.
- Regenera y **vuelve a evaluar todo el archivo**, no solo la parte cambiada.
- Si el error se repite en otros lugares (sitio, PDF, skills, registro), corrígelo en todos: búscalo con `grep`.
- Si tras tres vueltas sigue fallando, detente y dile al usuario qué falla y qué intentaste.

## 4. Reporta
Di qué verificaste y cómo, con resultados concretos («85 diagramas, 0 fallas», «9 páginas, revisada la 3», «pesos = 100 %»). Nunca «debería funcionar». Si algo no se pudo verificar (por ejemplo, el sitio publicado desde este entorno), dilo.

## Lecciones de este proyecto
| Qué pasó | Qué lo habría evitado |
|---|---|
| Se publicaron pasos de SCACRSE con «periodo desde el que rige 202656» y créditos fijos; los cursos reales van de 000000 a 999999 y con créditos variables (C146) | Evaluar el dato contra un curso real antes de publicar |
| Los pasos para crear el NRC 10045 traían menos campos que la guía (C151) | Compararlos con `01-creacion-nrc.md` antes de darlos |
| Se citó C60 para las horas de Diseño Web, pero la fuente era C96 (C144) | Abrir la cita y confirmar que dice lo afirmado |
| El pie del modal se cortaba en celular (C132) | Mirar la captura a 390 px de ancho |
| `datos.json` se escribió con sangría 1 y el diff fue enorme | Revisar `git diff --stat` antes de subir |
