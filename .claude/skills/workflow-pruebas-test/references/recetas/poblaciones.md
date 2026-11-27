# Recetas: selección de población (GLRSLCT, GLAEXTR, GLBDATA)

Parte de `manejo-banner-test.md` (secciones 1 a 3: reglas, lotes y movimientos). Probadas en TEST el 26/11/2026 (C253); la carga por .csv es de C203. Pasos completos y parámetros: `arquitectura-centros-empresariales/references/ref-preguntas-frecuentes-poblacion-manual-y-reglas.md`.

## 1. Población a mano
1. GLRSLCT: Aplicación `STUDENT` › **Tab** y esperar 3 s › ID de selección nuevo › **Ir**. Si lo escrito cae en otro campo (pasó dos veces), borrar con Fin y retroceso y escribir un campo a la vez: en estas páginas Cmd+A no selecciona el texto.
2. Descripción (máximo 30 caracteres), **Manual** marcado › GUARDAR («Transacción procesada»).
3. GLAEXTR: aplicación, selección › **Ir** (vacía la primera vez) › ID › Tab (sale el nombre) › **+** para el siguiente › GUARDAR.

## 2. Población por reglas
1. GLRSLCT como arriba, **sin** Manual. ⏬ Definición: `SORLCUR_PIDM` / `SORLCUR`. ⏬ Reglas: `SORLCUR_PROGRAM` › Tab › en Operador escribir `=` (es una lista nativa: el clic no la despliega) › Tab › `'CMEMC38'` con comillas › GUARDAR.
2. **Salir con Ctrl+Q** (clic en una zona vacía primero): compila en GUQINTF y vuelve al inicio. Si se sale con la lupa, GLBDATA da «no ha sido compilada».
3. GJAPCTL › GLBDATA (la página recuerda el último proceso: si sale «GLBDATAGLBDATA», borrar lo repetido) › Ir › ⏬ › 01 selección, 06 `STUDENT`, 07 creador, 08 `N` › ⏬ › clic en **Enviar** › GUARDAR › número de secuencia.
4. GLAEXTR: la lista con indicador Sistema.

## 3. Capturas
Usuario (creador, «Usuario» del pie, parámetro 07) y la columna Nombre se tapan antes de guardar en `docs/fuentes/banner-test/capturas/`.
