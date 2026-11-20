# Preguntas frecuentes de operación: Docente, asistencia y evaluación docente

Respuestas cortas para el asistente IA y para cualquier agente, tomadas de lo probado en TEST (NRC 10044 y 10045) y del registro. Cada pregunta es un fragmento de la base del asistente (C197). Si la respuesta no está aquí ni en el registro, se dice «No lo sé» (ruta de escape).

Tema de este archivo: docente en SSASECT, carga SIAASGN, Pasar lista, notas y asistencia en el Autoservicio, encuesta TESS. Los otros temas están en los demás `ref-preguntas-frecuentes-*.md` (índice en el `SKILL.md` de esta skill).

### ¿Cómo se configura y aplica la evaluación docente (encuesta TESS)?
Es una encuesta que los alumnos responden por NRC para evaluar a su docente; da puntos de calidad por docente, NRC y área. En orden:
1. **SVACTES:** por materia y curso, desde un periodo, cada **código de horario** con su **código TESC** e «Indicador de anónima». En la USS, **A** (`EVALD_A`) es la del **docente de teoría** (horario `TEO`) y **B**, la del **docente de práctica** (usuario, C211).
2. **SVADTES:** por periodo y parte de periodo, la fecha de inicio y fin para responder; vale para todos los NRC de esa parte. Si no se guarda nada en SVADTES, la encuesta toma las fechas de la parte de periodo del NRC (en 202744: PGE desde el 19-NOV-2026, parte 1 desde el 01-ENE-2027; C214).
3. **SVPTESS** (GJAPCTL, impresora DATABASE): asigna la encuesta a los NRC; 01 periodo obligatorio, 02 a 04 materia, curso o NRC, 05 reporte detallado, 06 eliminar asignaciones previas.
4. **SVPSTSS** (GJAPCTL): asigna la encuesta a los alumnos de esos NRC; 5 crear retención Y/N, 6 y 7 fechas de la retención, 8 reporte detallado. La retención sale de GTVSDAX `HOLDTYPE`.
5. El alumno responde en el **Autoservicio** (Encuestas docentes › docente y NRC › Completar).
6. **SVITESS:** avance por NRC, docente y alumnos que respondieron.
7. **SVPTQPC** (GJAPCTL): calcula los puntos de calidad; 01 periodo obligatorio, 02 NRC, 03 docente, 04 código de TESS.
8. **SVATSGA:** permisos de Control o de Resultados por escuela, departamento o materia; el docente ve sus resultados en el Autoservicio.

La configuración previa de la encuesta (respuestas SVVACOD y SVAPVAC, preguntas SVAQCOD, áreas SVVTEQA, código SVVTSSC y estructura SVASDEF) es de toda la universidad. Fuente: instructivo 6.2.5, diap. 9 a 67. En TEST, SVITESS de 202744 ya lista 20 NRC de pregrado con `EVALD_A` (también los de horario `PRA`), del 19-NOV-2026 al 25-JUL-2027 y con 0 respuestas; la columna Origen en **A** quiere decir **anónima** (C212). **Aún no se prueba en TEST** con los centros (C211); por confirmar la encuesta B de práctica y quién corre los procesos.

### ¿Cómo asigno el docente a un NRC en SSASECT?
SSASECT › periodo › NRC › **Ir** › pestaña «Instructor y horas de reunión». Primero el horario (bloque «Fechas de reunión»: día, hora en 24 horas sin dos puntos, por ejemplo 1530 a 1710; el indicador de sesión 01 lo pone Banner). Luego, en el bloque **Instructor**, sesión 01 › **ID** del docente › Tab: Banner trae el nombre, carga 1.000, responsabilidad 100 y marca **principal**; porcentaje de sesión 100. Guardar: «Saved successfully» (C180; instructivo 6.2.1, diap. 15 y 19). El indicador de sobrepaso del docente se marca solo si sale «Conflicto de horario del instructor» y se revisó la hoja (6.2.1, diap. 20).

### ¿Cómo reviso la carga del docente en SIAASGN?
SIAASGN › ID del docente › periodo › **Ir**: una asignación por página (por ejemplo «10 de 10»); cada una muestra NRC, sesión, principal, carga de trabajo, responsabilidad y contacto semanal. Con **⏬** dos veces se llega al **resumen de la carga** (horas crédito, carga educativa, contacto semanal, periodo FTE). La alerta «Reglas activas de carga de trabajo del docente no definidas para este periodo» no impide consultar: 202656 no tiene reglas de carga y por eso el análisis por criterio sale vacío (C29, C194; E20).

### ¿Qué regla necesita un NRC para salir en Pasar lista del docente?
Una regla en **SOAATRK** del periodo: parte de periodo, materia y curso, **NRC**, «Desplegar clase» ✓, unidad de control **Presente/Ausente**, «Control de asistencia a clases» ✓ y las fechas de la parte. Sin ella, el NRC no sale en Autoservicio Docentes › Control de asistencia (C101, C182).

### ¿Cómo ingresa el docente las notas en el Autoservicio?
Autoservicio Docentes › tarjeta «Detalle de Notas y Asistencia» › **Ingresar calificaciones** › Libro de calificaciones › buscar el NRC › clic en la fila › **Componentes** › elegir el componente › esperar a que se active **Lista de alumnos** › Puntaje (por ejemplo 85 de 100) › **Guardar**. La calificación aparece al guardar (85 % → 17 con VIG_11). Para el siguiente componente: atrás, buscar el NRC y Componentes otra vez. La nota final sale en «Calificaciones compuestas» (C187, C119).

### ¿Cómo paso la asistencia al libro de calificaciones?
El porcentaje no pasa solo. En Pasar lista, el docente usa **Clase › «Actualizar la asistencia en el libro de calificaciones»** y confirma con **Sí** (instructivo 7.1.1, diap. 56 y 57). Después, en el libro, el componente **ATTRGRD** queda con 0 calificaciones restantes y el puntaje de asistencia; con 70 % o más es APRO (escala AST_70) (C119, C186).
