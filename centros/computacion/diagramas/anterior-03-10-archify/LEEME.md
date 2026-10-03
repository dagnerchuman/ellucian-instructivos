# Versión anterior (03/10/2026)

Primeros diagramas hechos con Archify en la carpeta `diagramas_flujo/`. Se guardan aquí solo como referencia histórica.

**Por qué se reemplazaron:**
- **Mezclaban centros.** El título decía «Centros Empresariales» y el carril «Idiomas / Informática / Emprendimiento», pero todos los datos eran de Computación: CMEMC38, ACXP, modo V, NRC 1021 y 1026, job 8114.
- **Orden del flujo maestro distinto al de Ellucian.** El CAPP y la carga docente aparecían después de la matrícula. Además, el autoservicio salía como un paso posterior al backoffice, cuando es una alternativa.
- **Casuísticas encadenadas.** Mostraban casos independientes como un solo flujo, por ejemplo «traslado → convalidación».
- **Imágenes recortadas.** Los PNG eran capturas de pantalla de 1920×945 y el carril Docente salía cortado.
- **Enlaces rotos.** El README apuntaba a `file:///e:/...`.

**Lo vigente** está en `centros/<centro>/diagramas/`. Se genera con `python3 herramientas/diagramas/generar.py`; el índice completo está en `centros/README.md`.

Si ya no la necesitas, puedes borrar esta carpeta: el historial de git la conserva (commit `1419241`).
