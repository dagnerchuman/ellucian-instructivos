# Recetas de TEST: Notas, asistencia y cierre


> **Dirección del Autoservicio (25/11/2026, C249):** ya no lleva el puerto `:8100` (con él responde 503 «No valid route»). Si la tarjeta de Experience no abre la ventana, entra directo por la dirección sin puerto.

Recetas probadas en Banner TEST (fórmula en SHAGCOM, pasar lista y notas en el Autoservicio, pase a historia SHRROLL). Antes, lee las reglas, cómo moverse en Banner y las incidencias en [manejo-banner-test.md](../manejo-banner-test.md): **nunca se guarda sin permiso del usuario**.

### Cargar la fórmula de un NRC (SHAGCOM, C181)
1. SHAGCOM › periodo y NRC › Ir. Si el plan está vacío, Banner pide primero la escala: «Ingresar la escala de calificación antes de continuar».
2. Arriba, «Escala de calificación» **`VIG_11`** (no `AST_70`: con ella la final sale APRO, C120 y C123) › Tab › el usuario guarda.
3. Clic en Secuencia de la primera fila. Por cada componente: secuencia › Tab › nombre › Tab › descripción › Tab › peso › Tab, **esperando 1 a 2 s después de cada Tab**. Si se escribe seguido, Banner corre los campos. Un clic en otra celda no mueve el foco: Tab o Shift+Tab y, para reemplazar, Cmd+A.
4. Siga con Tab por la fila hasta «Nota aprobatoria»: la escala la hereda de arriba y la aprobatoria se llena sola (55 con `VIG_11`). El siguiente componente se agrega con el **+** del bloque.
5. `ATTRGRD`: peso 0, «Debe aprobar» con la barra espaciadora, escala `AST_70` (Cmd+A y escribir); la aprobatoria pasa sola a 70.
6. El usuario guarda: *Saved successfully (5 rows saved)* y «Total de peso final» 1.00. Plan del 10044 y del 10045: TA1 0.15, TA2 0.15, PA 0.40, EF 0.30 (C98).

### Pasar lista y enviar la asistencia al libro (Autoservicio docente, C186)
1. Abra `https://facultyssb-test.usspesaas.elluciancloud.com/FacultySelfService/ssb/facultyAttendanceTracking` (el botón «Ingresar asistencia» abre una ventana aparte) › **Pasar lista** del NRC.
2. Solo se marca la **columna de la fecha elegida** (resaltada a la derecha): pulse su encabezado o ‹ › y luego el círculo. Cada clic se guarda solo; el usuario autoriza las marcas antes.
3. Clase › «Actualizar la asistencia en el libro de calificaciones» › el usuario pulsa **Sí**.
4. Comprobar en `…/FacultySelfService/ssb/gradeEntry#/gradebook` › NRC › Componentes › ATTRGRD › Lista de alumnos.
5. **Solo el docente principal pone notas (C250):** como secundario, el componente sale «sólo de lectura»; se cambia el principal en SSASECT. Si la fórmula no tiene `ATTRGRD`, el paso 3 da «El componente de la calificación no existe» y no pasa nada al libro (C251).
6. **Notas (C187):** en el libro, buscar el NRC (la lista se duplica al recargar) › Componentes › componente › esperar a que se active «Lista de alumnos» › puntaje › Guardar (con permiso). La calificación sale al guardar. Para el siguiente componente: atrás y otra vez. Al final, «Calificaciones compuestas» muestra el porcentaje y la nota final.

### Pase a historia de un NRC (GJAPCTL › SHRROLL, C190)
1. GJAPCTL › Proceso `SHRROLL` › Tab › Ir (espere a que cargue la página antes de escribir). ⏬ al bloque de parámetros › Tab al valor del 01 › flecha abajo para cada fila: 01 periodo, 04 `%`, 05 NRC, 06 usuario, 07 **A**, 08 `A`, 09 periodo de calificaciones, 10 `N`. Envío: «Enviar».
2. Clic en el bloque Envío y GUARDAR (si el foco está en los parámetros: «Debe estar en BLOQUE DE ENVÍO…», C252): sale «Arc Log: shrroll_N.log Arch List: shrroll_N.lis».
3. GJIREVO › SHRROLL › N › `shrroll_N.lis` › Ir: «Rolled to Academic History» por alumno y plan; en la página 2, Report Mode y RECORD COUNT.
4. Si está bien, lo mismo con 07 = **U** (graba). Comprobar en SHACRSE (cambie el ID que arrastra) y en SFASLST («Comenzar de nuevo» › Ir para refrescar): «Pasada» ✓.
