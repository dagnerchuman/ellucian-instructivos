---
name: workflow-entregables-uss
description: Protocolo y pipeline de generación de entregables oficiales USS (PDF mediante Chromium/Playwright, presentaciones PPTX nativas sin errores de reparación y hojas Excel con fórmulas). Cumple las directrices estrictas de diseño, paleta morada/verde, autoría de Dagner Chuman y control de calidad visual.
---

# Workflow: Generación y Validación de Entregables USS

Este workflow rige la creación de documentos oficiales para el proyecto de migración a Ellucian Banner de los Centros Empresariales de la USS.

## 1. Reglas Maestras de Contenido y Estilo
- **Idioma:** Español directo, claro y ejecutivo.
- **Enfoque modular:** «Poco a poco», un tema por entrega. «Mientras más resumido, mejor».
- **Pocas tablas:** Priorizar tarjetas temáticas, bloques visuales y diagramas de flujo con conectores.
- **Estructura fija:**
  1. «**Hoy en SEUSS**» (hechos vigentes según usuario).
  2. «**En Ellucian**» (lo que indican los instructivos con cita).
  3. **Ejemplos por centro** (Idiomas, Informática y Emprendimiento, **los tres siempre**).
  4. «**Resultado**» operativo.
  5. **Glosario** de siglas y códigos explicados.
  6. **Todas las dudas al final**, clasificadas en «Para Ellucian» y «Para la USS».
- **Siglas y códigos:** Siempre acompañadas de su significado entre paréntesis en la primera aparición (ej. «NRC (Número de Referencia de Curso)», «SSASECT (Programar NRC)»).
- **Autoría:** «Elaborado por: Dagner Anibal Chuman Lluen» en portada, pie de página y metadatos.
- **Paleta USS:**
  - Principal: Morado USS `#7030A0` (oscuro `#5C2193`), Verde USS `#4EA72E` y `#92D050`.
  - Idiomas: `#7030A0`.
  - Informática: `#0E8A5F` (gráficos `#1BAF7A`).
  - Emprendimiento: `#C2501C` (gráficos `#EB6834`).

## 2. Pipeline de Generación por Tipo

### A. Documentos PDF (HTML → Chromium)
- **Base técnica:** `.claude/skills/documentos-uss/scripts/pdf/`:
  - `common.py`: Portada (`header`), secciones (`section`), tablas (`table`), formato (`fmt`), glosario (`glosario_html`), renderizador (`render`).
  - `render.js`: Motor Chromium A4 / A3-horizontal con inyección de fuentes base64.
  - Fuentes: `InterStatic` (400, 500, 600, 700) y `Montserrat`.
  - Ejemplo maestro: `ejemplo_centros.py`.
- **Control de Calidad Visual:**
  - Ejecutar `check_pdf(ruta_pdf, png_dir=...)` para revisar metadatos y renderizar PNGs de cada página.
  - Verificar:
    - 0 títulos huérfanos al pie de página (usar `<div class="keep">`).
    - Sin tarjetas cortadas por salto de página.
    - Sin glifos incompatibles (Inter no soporta flechas complejas ni símbolos como ≥, ▲; usar texto, «›» o SVG embebido).
    - Nombre del archivo en MAYÚSCULAS: `TEMA - SUBTEMA - CENTROS EMPRESARIALES.pdf`.

### B. Presentaciones PPTX (Plantilla USS 2026)
- **Base técnica:** `.claude/skills/documentos-uss/scripts/pptx/`:
  - `ussdeck.py` y `pptlib.py`.
  - Diapositivas nativas con elementos vectoriales editables.
- **Regla crítica de reparación:**
  - El archivo PPTX debe abrir limpiamente en PowerPoint sin requerir reparación ni recuperación de XML.
  - Se garantiza mediante `finalize()`: limpieza de `xml:space`, identificadores únicos `creationId`, orden en `[Content_Types].xml` y sin entradas vacías de carpeta en el zip.

### C. Hojas de Cálculo Excel
- **Herramienta:** `openpyxl`.
- Fórmulas vivas (COUNTIFS, SUM, TODAY).
- Lista de validaciones en hoja oculta `Listas`.
- Verificación de 0 errores de fórmula (`#VALUE!`, `#REF!`, `#N/A`).
