# Recetas de TEST: Mallas, prerrequisitos e historia

Recetas probadas en Banner TEST (SCAPPRQ, SHACRSE, SMAPROG y SMAAREA). Antes, lee las reglas, cómo moverse en Banner y las incidencias en [manejo-banner-test.md](../manejo-banner-test.md): **nunca se guarda sin permiso del usuario**.

### Leer o cambiar SCAPPRQ
- Programa + **periodo de la versión** (202444, 202644), no el de la matrícula (C164) › Ir › clic en el curso › ⏬ al bloque de prerrequisitos. Agregar: **+** › materia, curso, sin nivel ni calificación si basta haberlo cursado.

### Buscar un alumno con un curso en su historia (SHACRSE)
- SHACRSE › ID › **periodo vacío** › Ir: todos sus cursos con periodo, NRC, nota y modo. Así se encontró a `A00010005` con Basic I (C170). Solo consulta.

### Ver una malla (SMAPROG y SMAAREA, solo consulta)
- **SMAPROG** › programa (por ejemplo `CMEMC44`) › periodo (el de la prueba) › Ir: versión, modelo y totales. Sus áreas están en el bloque «Anexos de área de programa» (⏬ unas 8 veces).
- **SMAAREA** › área (por ejemplo `MC44-01`) › periodo › Ir › **⏫ una vez** desde el primer bloque lleva directo a «Anexo de curso/atributo de área» (las reglas). Con una regla seleccionada, botón **Regla**: el detalle muestra materia y curso de cada condición; **Regresar** vuelve. Si la tabla quedó corrida a la derecha, desplázala a la izquierda para ver Materia y curso (C172).
- Para cambiar de área: «Comenzar de nuevo» (arriba a la derecha) › borrar el área › escribir la nueva › Tab › Ir.
- **Agregar un curso a una regla** (C173): SMAAREA con el **periodo de la versión** (por ejemplo 202454, no el de la matrícula) › Anexo › regla › **Regla** › clic en una fila de Detalles › **+** de Detalles › Materia › Tab › curso › Tab › el usuario guarda. La columna «Condición» se numera sola al guardar.
- **Varios cursos en una regla** (C174): un **+** por cada curso; la fila nueva sale debajo de la última (cada fila, unos 18 px más abajo). Después de cada Tab, espera 2 s a que Banner valide el curso. Antes de pedir el guardado, revisa con zoom que estén todas las filas («Registro n de n»). Una regla por guardado.
- **Quitar un curso de una regla:** clic en la fila › **–** de Detalles (al lado del +) › el usuario guarda. Sin probar todavía: es lo que falta en `MC42-01` › `ECOM-04` (C174).
- **Comprobar:** después de guardar, «Comenzar de nuevo» › misma área y periodo de la versión › Ir › regla › Regla. Si el usuario recargó la página, hay que volver a entrar a SMAAREA. También sirve **Regresar** › la misma regla › **Regla** (C181).
- **El periodo se escribe a mano:** un doble o triple clic en el campo abre la lista «Códigos de periodos del catálogo», y su Intro elige la primera fila (999999). Clic › Fin › borrar › escribir (C181).
