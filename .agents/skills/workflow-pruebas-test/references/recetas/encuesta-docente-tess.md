# Recetas de TEST: Encuesta docente (TESS)

Recetas probadas en Banner TEST (SVACTES, SVADTES, SVITESS y SSASECT, solo consulta). Antes, lee las reglas, cómo moverse en Banner y las incidencias en [manejo-banner-test.md](../manejo-banner-test.md): **nunca se guarda sin permiso del usuario**.

### Revisar la encuesta docente de un NRC (solo consulta, C214)
1. Las páginas abren directo con `…/BannerSearchCard/BannerAdmin%3Fform%3D<PÁGINA>` (SVACTES, SVADTES, SVITESS, SSASECT), sin pasar por la lupa.
2. **SVACTES:** materia › Tab › curso › Tab › periodo › Tab › Ir. Sale cada código de horario (`TEO`, `PRA`) con su código TESC y «anónima». Para otro curso: «Comenzar de nuevo», el curso queda seleccionado y se escribe encima.
3. **SVADTES:** periodo › ••• de «Parte de periodo» abre SOBPTRM con las partes y sus fechas › doble clic en una › Ir. Si dice *«Query caused no records to be retrieved»*, esa parte **no tiene fechas propias**: las que se ven son las de la parte, sugeridas y sin guardar. Salir sin guardar (al navegar, descartar los cambios).
4. **SVITESS:** periodo › Ir. Una fila por NRC y docente; con la rueda a la derecha salen número de alumnos, respuestas, fechas, origen, **Anónima** y **Estado** (`A` Activo). Sin fechas en SVADTES, la encuesta toma las de la parte de periodo del NRC.
5. **SSASECT** del NRC: «Información de sección de curso» da el tipo de horario y la parte de periodo; «Instructor y horas de reunión», el docente. No se copian nombres de docentes ni alumnos al registro.
