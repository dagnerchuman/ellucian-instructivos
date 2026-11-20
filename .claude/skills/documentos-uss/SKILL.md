---
name: documentos-uss
description: >-
  Qué hace: preferencias del usuario (Dagner Anibal Chuman Lluen) y generadores de los entregables
  con formato USS: PDF, presentaciones PPTX, Word de preguntas y planillas Excel, con sus fuentes en
  fuentes/ y las piezas en scripts/. Cuándo usarla: siempre que pida un PDF, un PPT o diapositivas,
  un Word, un resumen, un afiche, una tabla o una planilla, o diga «hazme el PDF» o «pásame el ppt»;
  es la skill principal de todo entregable. Cuándo no usarla: diagramas Archify del sitio
  (workflow-diagramas-archify), videos (hyperframes), ni mientras el usuario solo está «alimentando»
  información (entonces no se generan diapositivas).
---

# Entregables con formato USS

## Mapa de la skill: abre solo el archivo que necesitas

| Si necesitas… | Abre |
|---|---|
| Hacer o corregir un PDF (plantilla, fuentes, `common.py`, revisión visual) | [references/pdf.md](references/pdf.md) |
| Hacer o corregir un PPTX (`ussdeck.py`, `pptlib.py`) | [references/pptx.md](references/pptx.md) |
| El Word de preguntas para responder y devolver, un Excel, o un diagrama paso a paso (que va por Archify) | [references/word-excel-y-diagramas.md](references/word-excel-y-diagramas.md) |

## Lo que el usuario pide (preferencias aprendidas)
- **Idioma:** español, sencillo y directo. El usuario escribe informal y con apuro; entiende lo que quiere decir.
- **«Mientras más resumido, mejor»** y **«poco a poco»**: un tema por entrega.
- **Pocas tablas** («me pones varias tablas que me pierdo»). Prefiere:
  - tarjetas por tema;
  - flujos con flechas;
  - **ejemplos concretos por centro**: Inglés, Informática y Emprendimiento, **los tres siempre**; una vez se olvidó uno y hubo que agregarlo.
  - Tablas, solo pequeñas o de referencia.
- **Estructura fija** de cada tema:
  - «**Hoy en SEUSS**»: lo que se hace ahora, según el usuario.
  - «**En Ellucian**»: lo que dicen los instructivos, con cita.
  - Ejemplos y un «Resultado».
- **Todas las dudas al final**, separadas en «Para Ellucian» y «Para la USS».
- **Siglas y códigos siempre con su significado entre paréntesis.** Ejemplo: «NRC (Número de Referencia de Curso)», «SSASECT (Programar NRC)». Lo pidió el 26/09/2026.
  - `explicar(html)` de `common.py` lo hace solo en cada tarjeta, la primera vez que aparece el término; SEUSS, solo una vez en todo el documento.
  - `glosario_html()` arma el glosario, que va antes de las dudas.
  - Si usas un término nuevo, agrégalo a `SIGLAS` o `PAGINAS`.
- **«Hoy en SEUSS» es lo que el usuario dice que se hace hoy; no lo interpretes.** Ejemplo del 26/09: en SEUSS, quien desaprueba BASIC I **no** pasa a BASIC II (salvo con examen de suficiencia). Se había escrito «¿pasa automático?», y el usuario lo corrigió.
- **Autor:** «Elaborado por: Dagner Anibal Chuman Lluen», en la portada y en el pie. También en los metadatos del PDF.
- **Formato USS:**
  - morado **#7030A0** (oscuro #5C2193); verdes **#4EA72E** y **#92D050**;
  - logos de la USS y de Ellucian;
  - para las presentaciones, la plantilla «Ppt USS 2026».
  - Color por centro: Inglés **#7030A0**, Informática **#0E8A5F** (en gráficos #1BAF7A), Emprendimiento **#C2501C** (en gráficos #EB6834).
- **«Buen PDF como PPT, sé profesional»:** cuando pide los dos, genera el mismo contenido desde un solo módulo de datos (como `casos_data.py`) para que el PDF y el PPTX coincidan. En el PPTX, las siglas también llevan su significado entre paréntesis y hay una diapositiva de glosario.
- **PDF por defecto.** Presentaciones solo si las pide. Mientras «te estoy alimentando» con información, **no generes diapositivas**.
  - El PPTX **debe abrir sin «reparar»** en PowerPoint.
- **Datos inventados:** márcalos siempre «de ejemplo». Nunca los presentes como datos de la USS.
- **Nombre de archivo en MAYÚSCULAS:** `TEMA - SUBTEMA - CENTROS EMPRESARIALES.pdf`. Entrégalo con SendUserFile para que lo vea en el panel.
- **Antes de escribir,** carga las skills `arquitectura-centros-empresariales` (datos) y `preguntas-y-dudas-centros` (qué está confirmado y qué no).

## Generadores originales
En `fuentes/` están los scripts con los que se hizo cada entregable, con todos sus datos y textos. Úsalos para corregir o regenerar un entregable. Lee antes `fuentes/LEEME.md`: hay rutas que ajustar.

## Entregables hechos hasta ahora
Lista, estructura y qué supuestos usa cada uno: [references/entregables.md](references/entregables.md). Si un supuesto cambia (ver el registro de dudas), ofrece corregir los entregables afectados.
