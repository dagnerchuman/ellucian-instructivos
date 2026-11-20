# Preguntas frecuentes de operación: Notas, historia académica y PGA

Respuestas cortas para el asistente IA y para cualquier agente, tomadas de lo probado en TEST (NRC 10044 y 10045) y del registro. Cada pregunta es un fragmento de la base del asistente (C197). Si la respuesta no está aquí ni en el registro, se dice «No lo sé» (ruta de escape).

Tema de este archivo: pase a historia SHRROLL, historia, repetidos, PGA, componentes SHAGCOM y suficiencia. Los otros temas están en los demás `ref-preguntas-frecuentes-*.md` (índice en el `SKILL.md` de esta skill).

### ¿Cómo hago el pase a historia (SHRROLL)?
Cuando todos los docentes calificaron (libro de calificaciones o carga administrativa) y la nota final está calculada en SFASLST, Registros Académicos pasa las notas a la historia académica con el proceso **SHRROLL** en **GJAPCTL** (Control de envío de proceso). Pasos (instructivo 7.1.9, diap. 22 a 29):
1. **GJAPCTL** › proceso `SHRROLL` (Grade Roll To Academic History) › **Ir** (diap. 22).
2. Impresora **DATABASE** y pase al bloque de parámetros; si no se ven los 10, amplíe los registros por página (diap. 23).
3. **Valores de parámetro** (diap. 24): 01 Código de periodo (R), por ejemplo `202656`; 02 y 03 rango de fechas de inscripción (O; en las pruebas, vacíos); 04 parte de periodo, `%` para todas (R); 05 NRC, uno o `%` para todos (R); 06 ID del usuario que lo corre (R); **07 modo: A auditoría (no graba) o U actualizar (graba)** (R); 08 impresión: A todo o E solo errores (R); 09 periodo de calificaciones (O), el mismo periodo; 10 pasar el título largo de la sección: Y o N (R).
4. Envío **Enviar** › **Guardar** (diap. 25): Banner da el número de proceso o job (diap. 26).
5. ⋮ › **Relacionado** › **Revisar salida (GJIREVO)** (diap. 27); Banner trae el proceso y el número; en Nombre de archivo, los tres puntos › el `shrroll_<job>.lis` (diap. 28) › Ir: el reporte (diap. 29).
Primero se corre en **A** y se lee el reporte; si está bien, otra vez en **U**. El reporte debe decir **«Rolled to Academic History»** por alumno, **«Deg Created»** (crea el registro de grado del plan de estudios, ver SHADEGR) y «RECORD COUNT» con el número de alumnos. Probado: NRC 10044, jobs 7761 (A) y 7762 (U); NRC 10045, 7994 (A) y 7995 (U) con 10 = N (C121, C122, C190). El «API Error: Invalid study path sequence for outcome» viene de un plan inactivo del alumno de prueba y no impide el pase (C121). En la demostración de Registros del 19/11/2026 (periodo 202646, NRC 10173) se usó 04 `%`, 05 `%` y 10 `Y` (C199).

### ¿Cómo sé si la nota ya pasó a la historia académica?
En **SFASLST** (periodo y NRC), la columna **«Pasada»** queda marcada en cada alumno después del SHRROLL en modo U; antes del pase está vacía (C190, C199; instructivo 7.1.6). La nota se ve en **SHACRSE** (o SHATCKN) del alumno. En modo A (auditoría) no se marca nada, porque no graba.

### ¿Dónde veo el registro de grado que crea SHRROLL («Deg Created»)?
En **SHADEGR**: ID del alumno › secuencia de grado › Ir (instructivo 4.4.4.1.5, diap. 23 y 24). El registro masivo lo crea el mismo SHRROLL del cierre de periodo (4.4.4.1.5, diap. 26 y 27): por eso el reporte de GJIREVO dice «Deg Created» en cada plan de estudios activo del alumno (C121). Los programas de los centros reciben un registro de grado `000000` (sin grado) (C121, E10). El registro individual se crea desde SGASTDN › Currículos › «Pasar a resultados» (4.4.4.1.5, diap. 20 a 22). Qué hace el centro con ese registro (certificado) sigue por confirmar.

### ¿Dónde veo la auditoría del cierre de curso (pase a historia)?
La auditoría es correr **SHRROLL en modo A** (auditoría): revisa el pase a historia sin grabar. Pasos (instructivo 7.1.9, diap. 22 a 29): **GJAPCTL** › proceso SHRROLL › Ir (diap. 22); impresora **DATABASE** y parámetros, con el 07 en **A** (diap. 23); Enviar y Guardar, Banner da el número de job (diap. 25). El resultado se ve en **GJIREVO**: en GJAPCTL, ⋮ › **Relacionado** › **Revisar salida** (diap. 27); elija el archivo `shrroll_<job>.lis` y lea el reporte (diap. 29): debe decir «Rolled to Academic History» y «RECORD COUNT» con el número de alumnos. Si está bien, se corre otra vez con el 07 en **U** (actualizar), que sí graba. Con el NRC 10044, jobs 7761 (A) y 7762 (U); con el 10045, 7994 (A) y 7995 (U) (C121, C122, C190). Después, la nota se ve en SHACRSE y la casilla «Pasada» en SFASLST (C190). No confundir con **SMRBCMP**: es el CAPP masivo del cierre de periodo (avance curricular, resultados en SMICRLT; 7.1.9), no la auditoría del curso. El cierre de curso del Script 14 sigue por probar en TEST.

### ¿Dónde veo la nota en la historia académica del alumno?
En **SHACRSE** › ID › periodo › Ir: muestra cada curso con su calificación, modo y horas. Ojo: SHACRSE arrastra el ID de la página anterior; cámbielo (C190). Con el periodo vacío lista toda la historia del alumno. La misma nota se ve en **SHATCKN**, que es la página que muestra el instructivo 7.1.6 (diap. 19); una corrección después del pase a historia se hace ahí (C124, C194). En **SFASLST**, después del pase, la casilla «Pasada» queda marcada (C190).

### ¿Qué pasa en la historia académica cuando un alumno repite un curso? ¿Se borra la nota desaprobada?
No se borra: Banner **incluye o excluye** cada intento según las reglas de repetidos (C200). Ejemplo explicado por Registros: desaprueba Matemática I en el periodo I y la aprueba en el periodo II; en la historia, el intento desaprobado queda marcado para **no contar en el PGA** (promedio general acumulado) y el aprobado sí cuenta. Lo marca el proceso **SHRRPTS** (Identificar cursos repetidos, GJAPCTL; instructivo 7.2.2, diap. 15 a 22) según las reglas de **SHARPTR** (Reglas de curso repetido/múltiple, por periodo y nivel: qué cursos se consideran repetidos y cuál cuenta, Primera aprobatoria, Máxima, Última o Mayor o última, y si en el PGA cuentan Todo o Seleccionado; 7.2.2, diap. 9 a 14). En **SHATCKN** cada curso muestra el indicador de repetición con las opciones **Ninguno, Excluir, Incluir e Incluir PGA**, y el **plan de estudios** al que pertenece (más a la derecha del bloque Detalle de curso); el plan sale de los currículos del alumno en **SGASTDN** (C200). Después, **SHRCGPA** calcula los promedios (7.2.2, diap. 24 a 31). Ninguno de estos procesos se ha probado aún con un NRC de los centros (U54).

### ¿Cuántas veces puede llevar un alumno el mismo curso?
Lo define el campo **Límite** (de repetición) del curso en **SCACRSE**: «la cantidad de veces que el estudiante podrá repetir las asignaturas» (instructivo 1.1.4, diap. 22, punto 17). La regla de SHARPTR decide cuál de los intentos cuenta cuando se llega a ese límite (7.2.2, diap. 11). En los cursos de los centros revisados en TEST (ESEC 00701, Basic I, Emprendimiento I) el Límite está **vacío** (C145, C146). Cuántas veces se permite en los centros sigue por confirmar (U54).

### ¿Cómo calculo el PGA en GJAPCTL (SHRCGPA)?
El PGA (promedio general acumulado) lo calcula Registros Académicos con el proceso **SHRCGPA** en **GJAPCTL**, después del cierre de periodo, del pase a historia (SHRROLL) y de marcar los repetidos (SHRRPTS) (C200; instructivo 7.2.2, diap. 24 a 34). Pasos:
1. **GJAPCTL** › proceso `SHRCGPA` › **Ir** (diap. 25).
2. Impresora **DATABASE** y pase al bloque de parámetros (diap. 26).
3. **Valores de parámetro** (diap. 27): 01 periodo (R); **02 población** (R): `a` todos los alumnos del periodo, `r` solo los alumnos cuyas historias ya se pasaron, `c` los de un archivo colector; 03 identificador de selección, 04 código de aplicación y 05 ID del creador (O), solo si se corre para una selección de población.
4. Pase al siguiente bloque, **Enviar** y **Guardar** (diap. 28): Banner da el número de proceso.
5. ⋮ › **Relacionado** › **Revisar salida (GJIREVO)** › el archivo `.lis` › Ir (diap. 29 a 31).
El resultado se consulta en SHATERM (ver la pregunta siguiente). No se ha corrido aún en TEST con un NRC de los centros (U54).

### ¿Dónde veo el PGA (promedio general acumulado) del alumno?
Según Registros Académicos, en **SHATERM** se ve el PGA del periodo y el global del alumno, **por plan de estudios** (C200). Que Banner lo lleve por plan de estudios depende de **SHACTRL** › «Procesar PGA por plan de estudios» (instructivo 7.1.9, diap. 19). El promedio lo calcula **SHRCGPA** después del cierre de periodo y del pase a historia (7.2.2, diap. 24 a 34). SHATERM no aparece en los instructivos de Ellucian.

### ¿Puedo copiar los componentes de SHAGCOM de un NRC a otro?
Sí. En **SHAGCOM** del NRC que está vacío, bloque «Asignación de escala de calificación», pulsa **«Copiar componentes»**: en la ventana pon el **Periodo de origen** y el **NRC origen** que ya tiene el plan de evaluación y pulsa **«Copiar de origen»**. Se copian la escala de arriba y todos los componentes con su peso, «calificadas de», «Debe aprobar» y escala, incluido ATTRGRD. Sirve cuando varios NRC llevan los mismos componentes calificables, aunque sean de otro curso. Visto en TEST el 20/11/2026: del NRC 10040 al 10039 (202744) se copiaron `VIG14_N1_S`, 1_RA1 y 2_RA2 al 50 % y ATTRGRD con AST_70 (C210). **Por confirmar:** si después hay que pulsar Guardar. Revisa luego que la escala de arriba sea la de la nota final (C120, C123).

### ¿Emprendimiento rinde examen de suficiencia?
**No lo sé: está por confirmar (U21).** Lo confirmado es que Computación no rinde suficiencia y que la suficiencia aplica a Idiomas para saltar a BASIC II (C36, C11).
