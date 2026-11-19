# Preguntas frecuentes de operación en Banner (Centros Empresariales)

Respuestas cortas para el asistente IA y para cualquier agente, tomadas de lo probado en TEST (NRC 10044 y 10045) y del registro. Cada pregunta es un fragmento de la base del asistente (C197). Si la respuesta no está aquí ni en el registro, se dice «No lo sé» (ruta de escape).

### En SFAREGS sale «No se ha completado la configuración requerida». ¿Qué hago?
Banner pide **SOADEST** la primera vez que se abre SFAREGS en una sesión nueva. Escriba **DATABASE** en los cinco campos (Horarios, Facturas, Históricos académicos, Ingresos y Cumplimiento) y abra SFAREGS otra vez desde la lupa, **sin guardar SOADEST**: así entra (C185). Si pulsa GUARDAR en SOADEST, Banner responde «\*ERROR\* Función inválida»; no hace falta guardar (C158).

### ¿Cómo doy de baja a un alumno de un NRC con DD y hasta cuándo se puede?
SFAREGS › periodo › ID › **Ir** (si sale SOADEST, ver la pregunta anterior). Baje con **⏬** hasta «Información de curso» (un clic en la tabla no mueve el foco), cambie el **Estatus** del NRC de **RE a DD** y pulse Tab: las horas bajan a 0.000. Al guardar salen «Estimación de cuota procesada» y «Los alumnos ya están inscritos…»; al reabrir, el NRC queda en DD (C189). El DD vale mientras la **parte de periodo** lo permita en SFARSTS: en 202656, la **X06** tiene DD, DW, RE y RW del **07-SEP al 31-OCT-2026** y la X07 no tiene reglas (C156). Si sale «El estatus "DD" es inválido…», esa parte no tiene DD. Un RE no se borra: se cambia a DD.

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

### ¿Cómo asigno el docente a un NRC en SSASECT?
SSASECT › periodo › NRC › **Ir** › pestaña «Instructor y horas de reunión». Primero el horario (bloque «Fechas de reunión»: día, hora en 24 horas sin dos puntos, por ejemplo 1530 a 1710; el indicador de sesión 01 lo pone Banner). Luego, en el bloque **Instructor**, sesión 01 › **ID** del docente › Tab: Banner trae el nombre, carga 1.000, responsabilidad 100 y marca **principal**; porcentaje de sesión 100. Guardar: «Saved successfully» (C180; instructivo 6.2.1, diap. 15 y 19). El indicador de sobrepaso del docente se marca solo si sale «Conflicto de horario del instructor» y se revisó la hoja (6.2.1, diap. 20).

### ¿Cómo reviso la carga del docente en SIAASGN?
SIAASGN › ID del docente › periodo › **Ir**: una asignación por página (por ejemplo «10 de 10»); cada una muestra NRC, sesión, principal, carga de trabajo, responsabilidad y contacto semanal. Con **⏬** dos veces se llega al **resumen de la carga** (horas crédito, carga educativa, contacto semanal, periodo FTE). La alerta «Reglas activas de carga de trabajo del docente no definidas para este periodo» no impide consultar: 202656 no tiene reglas de carga y por eso el análisis por criterio sale vacío (C29, C194; E20).

### ¿Cómo pongo un curso en la malla (SMAAREA)?
La malla es el **LIB_AREA** del programa: sin ella el curso no sale en Proyecciones ni cuenta en CAPP (C172, C181). Pasos: **SMAPROG** del programa (por ejemplo `CMEMC44`, XP 07) para ver su área (`MC44-01`). Luego **SMAAREA** › área › **periodo de la versión** (202454, no el de la matrícula; escríbalo a mano porque Intro en la lista elige 999999) › Ir › ⏫ una vez a «Anexo de curso/atributo» › regla (por ejemplo `ECOM-03`) › Regla › clic en Detalles › **+** › materia y curso › Guardar. Banner numera la condición al guardar (C173, C181). En producción se usa «Copiar» a una versión nueva (ref-ruta-inscripcion-y-curso-nuevo.md).

### ¿Qué pasos tiene SCACRSE para crear un curso?
SCACRSE es el catálogo de cursos: el curso se crea una sola vez y rige hasta 999999; el NRC de cada periodo se crea después en SSASECT (C144). Solo si el curso no existe (instructivo 1.1.4, diap. 20 a 25):
1. Encabezado: **Materia** (STVSUBJ, por ejemplo ESEC), **Curso** (número, por ejemplo 00701) y **Periodo `000000`** en los cursos reales, no un periodo como 202656 (C146; diap. 20).
2. Detalles: **Título**, **Escuela EM** (Centros Empresariales), **Departamento** del centro (EMCI Computación, EMID Idiomas, EMEM Emprendimiento) y **Estatus A** (activo); método de prerrequisito «Básico o ninguno» (C145, C146; diap. 21).
3. Horas: **UEC o crédito** y **Cobro** siempre variables: inferior 0, indicador **O** y superior = créditos (Computación 0 O 1); Teoría, Laboratorio y Contacto según el sílabo (Computación 1, 1 y 2) (C146; diap. 22).
4. Con **«Sección siguiente»** (↓): **Nivel de curso** `C` Computación (diap. 23); **Modo de calificar** `V` Vigesimal, marcado como Predefinido (diap. 24); **Tipo de horario** `TEO` y `PRA`, método educativo `VIRT`, carga de trabajo 1.000 (diap. 25) (C148).
Lo más seguro es **Copiar** un curso real del mismo centro y cambiar lo propio (C146). Hoy los cursos los crea Registros Académicos (C147). Las horas de Diseño Web (ESEC 00684) siguen por confirmar (U45).

### ¿Quién crea los cursos nuevos en SCACRSE?
Hoy los crea **Registros Académicos**; el centro solo si le dan acceso. Para el go-live se capacitará a todos por la cantidad de mallas a actualizar (C147, chat con Liliana Ocampo de Ellucian; U40 resuelta). El centro crea el **NRC** (SSASECT) de un curso que ya existe.

### ¿Qué es la parte de periodo X06 y qué fechas tiene?
Es una de las partes del periodo 202656 que usa Computación («Computación Grupo 06»): del **07-SEP al 31-OCT-2026**, 8 semanas. En SFARSTS tiene los estatus DD, DW, RE y RW en esas fechas; la X07 no tiene reglas (C154, C156). Las partes se definen en STVPTRM y sus fechas en SOATERM (C140).

### ¿Qué periodos usan los centros?
Los centros tienen periodos propios, que terminan en 51, 54 y 56: **202651** (2026-0, verano, grupos de enero a marzo), **202654** (2026-I, abril a julio) y **202656** (2026-II, agosto a diciembre); en 2027, 202751 y 202754 (datos.json común; ADR-005). Pregrado usa otros (por ejemplo 202644).

### ¿Qué regla necesita un NRC para salir en Pasar lista del docente?
Una regla en **SOAATRK** del periodo: parte de periodo, materia y curso, **NRC**, «Desplegar clase» ✓, unidad de control **Presente/Ausente**, «Control de asistencia a clases» ✓ y las fechas de la parte. Sin ella, el NRC no sale en Autoservicio Docentes › Control de asistencia (C101, C182).

### ¿Cómo ingresa el docente las notas en el Autoservicio?
Autoservicio Docentes › tarjeta «Detalle de Notas y Asistencia» › **Ingresar calificaciones** › Libro de calificaciones › buscar el NRC › clic en la fila › **Componentes** › elegir el componente › esperar a que se active **Lista de alumnos** › Puntaje (por ejemplo 85 de 100) › **Guardar**. La calificación aparece al guardar (85 % → 17 con VIG_11). Para el siguiente componente: atrás, buscar el NRC y Componentes otra vez. La nota final sale en «Calificaciones compuestas» (C187, C119).

### ¿Cómo paso la asistencia al libro de calificaciones?
El porcentaje no pasa solo. En Pasar lista, el docente usa **Clase › «Actualizar la asistencia en el libro de calificaciones»** y confirma con **Sí** (instructivo 7.1.1, diap. 56 y 57). Después, en el libro, el componente **ATTRGRD** queda con 0 calificaciones restantes y el puntaje de asistencia; con 70 % o más es APRO (escala AST_70) (C119, C186).

### ¿Cuál es el orden de los cursos de Inglés y tienen prerrequisito?
Sí. Idiomas usa **prerrequisito Fatal**: quien desaprueba BASIC I no pasa a BASIC II, salvo con **examen de suficiencia** (C11, R09). La cadena es BASIC I → BASIC II → BASIC III → INTERMEDIATE I → INTERMEDIATE II → INTERMEDIATE III; BASIC I → BASIC II está confirmado y el resto se asume igual (datos.json de Idiomas). En Banner va en SCAPREQ/SSAPREQ con la verificación en Fatal en SOATERM. Computación, en cambio, no tiene orden entre los cursos de la ruta (C191).

### ¿Emprendimiento rinde examen de suficiencia?
**No lo sé: está por confirmar (U21).** Lo confirmado es que Computación no rinde suficiencia y que la suficiencia aplica a Idiomas para saltar a BASIC II (C36, C11).
