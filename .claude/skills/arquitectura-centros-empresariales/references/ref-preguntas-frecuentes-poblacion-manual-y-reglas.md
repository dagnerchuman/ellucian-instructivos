# Preguntas frecuentes de operación: Selección de población a mano y por reglas

Respuestas cortas para el asistente IA y para cualquier agente, tomadas de la prueba en TEST del 26/11/2026 (C253) y del instructivo 7.1.10 «Generar selecciones de población». Cada pregunta es un fragmento de la base del asistente (C197). Si la respuesta no está aquí ni en el registro, se dice «No lo sé» (ruta de escape).

Tema de este archivo: crear la selección en GLRSLCT y llenarla a mano (GLAEXTR) o por reglas (GLBDATA). La carga por archivo .csv (GJAJFLU y GJRPSIM) y el CAPP masivo están en `ref-preguntas-frecuentes-poblacion-y-procesos-masivos.md`.

### ¿Cómo creo una selección de población a mano (GLRSLCT y GLAEXTR)?
**Probado en TEST el 26/11/2026** con la selección `POB_CE_MANUAL` de la aplicación `STUDENT`: 2 alumnos de prueba, guardados como **Manual** (C253). Pasos (instructivo 7.1.10, diap. 11 a 15):
1. **GLRSLCT**: Aplicación `STUDENT` › Tab › ID de selección, un nombre nuevo (por ejemplo `POB_CE_MANUAL`) › el ID de creador sale solo con su usuario › **Ir**.
2. Si la selección es nueva, todo sale vacío. Escriba la **Descripción** (hasta 30 caracteres; lo demás se corta) y marque **Manual**. Deje Seleccionar, De y Reglas vacíos › **Guardar**: sale «Transacción procesada».
3. **GLAEXTR**: Aplicación, ID de selección y creador › **Ir**. La primera vez sale «Query caused no records to be retrieved», porque la lista está vacía.
4. Escriba el **ID** del alumno y pulse Tab: Banner trae el **Nombre**. Para otro alumno, **+** del bloque y el siguiente ID.
5. **Guardar**: «Saved successfully (2 rows saved)». Cada fila queda con **Indicador de sistema = Manual**.

Sirve para pocos alumnos. Para muchos, use la carga por .csv o las reglas.

### ¿Cómo creo una selección de población por reglas (GLRSLCT)?
**Probado en TEST el 26/11/2026** con `POB_CE_REGLAS`: todos los alumnos del programa `CMEMC38` (C253). Pasos (instructivo 7.1.10, diap. 27 a 31):
1. **GLRSLCT**: Aplicación `STUDENT`, ID de selección nuevo (`POB_CE_REGLAS`) › **Ir** › Descripción («Poblacion reglas CMEMC38»), **sin** marcar Manual.
2. Con ⏬ pase a **Definición**: Seleccionar `SORLCUR_PIDM` y De `SORLCUR` (la tabla de planes de estudio del alumno).
3. Con ⏬ pase a **Reglas**: Objeto o elemento de datos `SORLCUR_PROGRAM` › Tab › en **Operador** elija `=` (es una lista: con el foco en ella, escriba `=`) › Tab › **Valor** `'CMEMC38'`, **con comillas simples**, como en la lámina (`'ICOMD103PR'`).
4. **Guardar**: «Transacción procesada».
5. **Salga de la página con Ctrl+Q** para compilar la regla (ver la pregunta siguiente).
6. Ejecute **GLBDATA** en GJAPCTL y revise la lista en **GLAEXTR**.

### ¿Por qué GLBDATA dice «La selección 1 … no ha sido compilada»?
Porque la regla de GLRSLCT se guardó pero no se compiló. **Pasó en TEST el 26/11/2026** (C253): se salió de GLRSLCT con la lupa de búsqueda de páginas y la regla quedó sin compilar. La compilación ocurre **al salir de GLRSLCT con Ctrl+Q** (la lámina 31 dice «es fundamental que después de guardar cierre la página»): sale la ventana **GUQINTF** con «Ejecutando compilación de selección de población; por favor, espere» y Banner vuelve al inicio. Después se envía GLBDATA otra vez y ya corre. Cada vez que cambie la regla, guarde y vuelva a salir con Ctrl+Q.

### ¿Qué parámetros lleva GLBDATA (Population Selection Extract)?
**GJAPCTL** › Proceso **GLBDATA** › **Ir**. La impresora ya sale en **DATABASE** (instructivo 7.1.10, diap. 32 a 35; el instructivo lo llama GLBDATAJ). En la prueba del 26/11/2026 (C253):

| N.º | Parámetro | Prueba en TEST | Qué es |
|---|---|---|---|
| 01 | Selection Identifier 1 | `POB_CE_REGLAS` | la selección por reglas (obligatorio) |
| 02 | Selection Identifier 2 | vacío | otra selección, solo para unir o cruzar |
| 03 | New Selection Identifier | vacío | la selección nueva que sale de unir o cruzar |
| 04 | Description for new selection | vacío | su descripción |
| 05 | Union/Intersection/Minus | vacío | U unir, I cruzar o M restar las selecciones 1 y 2 |
| 06 | Application Code | `STUDENT` | obligatorio |
| 07 | Creator ID of Selection ID | el creador de la selección | obligatorio |
| 08 | Detail Execution Report | `N` | opcional: `Y` imprime el SQL para depurar |

Luego ⏬ al bloque Envío › **Enviar** › **Guardar**. En la prueba salió «Número de secuencia: 8758».

### ¿Cómo reviso quiénes quedaron en la selección por reglas?
En **GLAEXTR**: aplicación, ID de selección y creador › **Ir** (diap. 37). En la prueba del 26/11/2026 salieron **17 alumnos** de `CMEMC38`, «Registro 1 de 17», todos con **Indicador de sistema = Sistema** (los cargó el proceso, no una persona). El .lis del trabajo está en **GJIREVO** (diap. 36).

Una regla sobre `SORLCUR_PROGRAM` trae a todo el que tenga o haya tenido ese programa en su historia de planes de estudio, sin mirar el periodo. Si necesita solo los activos o de un periodo, agregue otra regla con **Y/O** (por ejemplo, sobre el periodo o el estatus); eso aún no se prueba.

### ¿Qué diferencia hay entre Manual y Sistema en GLAEXTR?
**Manual**: el ID se escribió en GLAEXTR. **Sistema**: lo cargó un proceso, GLBDATA (reglas) o GJRPSIM con el parámetro 04 en `S` (C204, C253). Con «Ordenar primero registros manuales» los manuales salen arriba, y «Eliminar todos» vacía la lista.
