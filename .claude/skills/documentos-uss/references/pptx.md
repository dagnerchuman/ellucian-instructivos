# Presentaciones PPTX

Parte de la skill `documentos-uss` (el mapa está en su `SKILL.md`).

## Presentaciones PPTX
En `scripts/pptx/`:
- **`ussdeck.py`:** arma la estructura desde la plantilla.
  - `build_structure`, `build_cover`, `build_div`, `set_flow_boxes`, `finalize`, `to_pdf`.
  - Diapositivas base: portada = slide1, flujo = slide5, texto = slide3, divisor = slide6, configuración = slide7, cierre = slide23.
- **`pptlib.py`:** piezas nativas y editables.
  - Texto enriquecido; tablas nativas `a:tbl` con tamaño de letra automático (`fit_sz`).
  - Tarjetas, chevrones y conectores (polilínea `custGeom` con flecha).
  - Clase `Slide`.

**Requisitos:**
- **La plantilla del usuario no está en el repositorio.** Pídela o usa `USS_PPT_TEMPLATE`.
- Los scripts de la skill `pptx`, que se detectan solos.

**Geometría de la plantilla:**
- Título en y 0,24 M EMU.
- Área útil de y 0,9 M a 5,85 M.
- Logo USS abajo a la izquierda (y 6,15 M) y logo Ellucian abajo a la derecha (x 10,2 M).

**Para que abra sin «reparar»,** `finalize()` ya hace lo siguiente:
- limpia con `clean.py`;
- quita `xml:space`;
- da `creationId` únicos;
- escribe `[Content_Types].xml` primero en el zip;
- no incluye entradas de carpeta;
- reemplaza el pie «Elaborado por: …» por el autor.

**Después de generar:**
- Valida con `validate.py` de la skill pptx.
- Convierte a PDF (`to_pdf`) y revisa los PNG.
- Avisa al usuario de que no se pudo abrir en PowerPoint real.
