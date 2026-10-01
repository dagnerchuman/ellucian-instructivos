# Generadores originales de los entregables (septiembre de 2026)

Estos son los scripts con los que se hicieron los PDF, PPTX y Excel de `references/entregables.md`. Se guardan como **memoria del contenido**: cada uno tiene en listas de Python los datos, textos, citas y tablas de su entregable.

**Aviso:** se escribieron en una carpeta temporal de la sesión (`scratchpad/uss/...`).
- Algunos importan `ussdeck` y `pptlib`: usa las versiones portables de `../scripts/pptx/`.
- Otros importan `common`: usa la versión nueva de `../scripts/pdf/`, que tiene `explicar()` y el glosario. El `capp/common.py` de aquí es la versión antigua.
- Otros leen la plantilla `programacion.pptx`, que no está en el repositorio (se la pide al usuario).
- Para regenerar, ajusta las rutas y los `sys.path`.

| Archivo | Entregable |
|---|---|
| `build0.py` | 0. FLUJO GENERAL (PPTX) |
| `build21.py` | 2.1 PROGRAMACIÓN DE ASIGNATURAS: correquisitos, prerrequisitos y restricciones |
| `build3.py` | 3. DOCENTES |
| `build4.py` | 4. ADMISIÓN |
| `resumen/build_resumen.py` | RESUMEN DE PROCESOS BANNER (TEMAS 1 A 4), en PDF |
| `antes/build_antes.py` | PERIODO ACADÉMICO: ANTES Y DESPUÉS (supuesto S01 por corregir) |
| `valid/build_valid.py`, `valid/new_sections.py` | VALIDACIÓN DE LA MIGRACIÓN (PDF) |
| `valid/build_xlsx.py` | PLANILLA DE REVISIÓN: MIGRACIÓN R2 (Excel) |
| `capp/build_capp.py` | CAPP EXPLICADO |
| `capp/build_ejec.py` | MIGRACIÓN R2: LO QUE ENTIENDO |
| `capp/build_notas.py` | NOTAS DE LA REUNIÓN: RESPUESTAS |
| `capp/build_ing_inf.py` | Versión anterior de INGLÉS, INFORMÁTICA Y EMPRENDIMIENTO. La vigente es `../scripts/pdf/ejemplo_centros.py` |
| `diag/build_diagrama.py` | DIAGRAMA DE INICIO A FIN (PDF A3) |
| `build_ppts.py` | PPTX de validación, CAPP, lo que entiendo y diagrama |
| `reunion28/build_reunion28.py` | RESUMEN DE LA REUNIÓN 28-09 |
| `casos/casos_data.py`, `casos/build_pdf.py`, `casos/build_pptx.py` | CASUÍSTICAS PARA LAS PRUEBAS INTEGRALES (PDF + PPTX con los mismos datos) |
