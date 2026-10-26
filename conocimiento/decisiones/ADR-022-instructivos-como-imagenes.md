---
id: ADR-022
titulo: Los instructivos se muestran como imágenes WebP y cada paso de las guías trae su diapositiva
estado: aceptado
fecha: 2026-10-24
fuentes: [C109, C112, C114]
temas: [visor, diagramas, instructivos]
---
# ADR-022 · Los instructivos se muestran como imágenes WebP

## Contexto
El visor leía cada PPTX en el navegador (pptx-browser): descargaba de 2 a 8 MB por instructivo y lo dibujaba con diferencias frente al original. El usuario pidió convertir los instructivos a imágenes y que la guía de cada paso de los diagramas muestre la diapositiva que le corresponde (C109).

## Decisión
- `herramientas/diapositivas.py` convierte cada PPTX (PPTX → PDF con LibreOffice → WebP de 1600 px) en `visor_instructivos/diapositivas/<id>/NNN.webp`, con el índice `indice.js`. Los `<id>` son los de `visor_instructivos/data.js`.
- El visor usa las imágenes cuando el instructivo está en el índice; si falta, vuelve a leer el PPTX. El PPTX sigue disponible para descargar y las carpetas `CAPACIDAD n/` no se mueven (ADR-015).
- Cada paso de los diagramas de los tres centros muestra sus diapositivas (C112). Cuáles van en cada paso se define en `herramientas/diagramas/diapositivas_pasos.py`: por paso en los flujos base y por pantalla en las casuísticas. La guía muestra un **recorte** sin título, banda lateral ni pie, y al ampliar ofrece la diapositiva completa y el enlace al visor (`?p=<id>&d=<n>`).
- El recorte se calcula con la posición de los elementos de cada lámina, leída del PPTX; no con proporciones fijas, porque los instructivos no comparten un mismo diseño.
- Si una página de Banner no sale en ningún instructivo, el paso muestra una lámina de **referencia** donde el instructivo ve lo mismo, siempre rotulada como tal; nunca se presenta como la página del paso. Un paso fuera de Banner dice por qué no tiene lámina (C114).
- El asistente usa las mismas láminas: debajo de una respuesta con pasos ofrece «Ver los pasos en imágenes» (C114).

## Alternativas descartadas
- **Seguir leyendo el PPTX en el navegador:** lento y con diferencias de dibujo.
- **Capturas a mano:** no se pueden regenerar ni mantener al día.

## Consecuencias
- El sitio carga una imagen por diapositiva en lugar del PPTX completo.
- El repositorio crece unos 50 KB por diapositiva (cerca de 3 850 diapositivas). Si un PPTX cambia, se vuelve a ejecutar `herramientas/diapositivas.py`, que solo convierte los que cambiaron.
- Todos los pasos en Banner tienen lámina (propia o de referencia); solo los pasos fuera de Banner quedan sin ella, con un aviso.
- Si una lámina se recorta mal, se le pone `caja` propia en `diapositivas_pasos.py`.

## Criterio de salida
Que Ellucian entregue los instructivos en otro formato, o que el peso de las imágenes en Netlify o GitHub sea un problema.

## Relacionado
- [ADR-003](ADR-003-diagramas-generados.md) · [ADR-015](ADR-015-visor-y-rutas.md) · [ADR-021](ADR-021-asistente-conocimiento-local-y-modo-seguro.md)
