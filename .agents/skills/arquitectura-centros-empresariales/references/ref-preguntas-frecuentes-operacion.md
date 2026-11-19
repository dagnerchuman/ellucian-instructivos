# Preguntas frecuentes de operación en Banner (Centros Empresariales)

Respuestas cortas para el asistente IA y para cualquier agente, tomadas de lo probado en TEST (NRC 10044 y 10045) y del registro. Cada pregunta es un fragmento de la base del asistente (C197). Si la respuesta no está aquí ni en el registro, se dice «No lo sé» (ruta de escape).

### En SFAREGS sale «No se ha completado la configuración requerida». ¿Qué hago?
Banner pide **SOADEST** la primera vez que se abre SFAREGS en una sesión nueva. Escriba **DATABASE** en los cinco campos (Horarios, Facturas, Históricos académicos, Ingresos y Cumplimiento) y abra SFAREGS otra vez desde la lupa, **sin guardar SOADEST**: así entra (C185). Si pulsa GUARDAR en SOADEST, Banner responde «\*ERROR\* Función inválida»; no hace falta guardar (C158).

### ¿Cómo doy de baja a un alumno de un NRC con DD y hasta cuándo se puede?
SFAREGS › periodo › ID › **Ir** (si sale SOADEST, ver la pregunta anterior). Baje con **⏬** hasta «Información de curso» (un clic en la tabla no mueve el foco), cambie el **Estatus** del NRC de **RE a DD** y pulse Tab: las horas bajan a 0.000. Al guardar salen «Estimación de cuota procesada» y «Los alumnos ya están inscritos…»; al reabrir, el NRC queda en DD (C189). El DD vale mientras la **parte de periodo** lo permita en SFARSTS: en 202656, la **X06** tiene DD, DW, RE y RW del **07-SEP al 31-OCT-2026** y la X07 no tiene reglas (C156). Si sale «El estatus "DD" es inválido…», esa parte no tiene DD. Un RE no se borra: se cambia a DD.

### ¿Cómo hago el pase a historia (SHRROLL)?
Lo corre Registros Académicos en **GJAPCTL › proceso SHRROLL** con impresora DATABASE. Parámetros: 01 periodo (`202656`), 04 parte (`%`, todas), 05 NRC, 06 usuario, **07 modo: A primero (auditoría, no graba) y luego U (actualizar, graba)**, 08 `A`, 09 periodo de calificaciones y 10 `N`. Cada envío da un job (con el NRC 10045: 7994 en modo A y 7995 en modo U). El reporte se lee en **GJIREVO** (GJAPCTL › ⋮ › Relacionado › Revisar salida): debe decir «Rolled to Academic History» y «RECORD COUNT 1» (C121, C122, C190). El «API Error: Invalid study path sequence for outcome» viene de un plan inactivo del alumno de prueba y no impide el pase (C121).

### ¿Dónde veo la nota en la historia académica del alumno?
En **SHACRSE** › ID › periodo › Ir: muestra cada curso con su calificación, modo y horas. Ojo: SHACRSE arrastra el ID de la página anterior; cámbielo (C190). Con el periodo vacío lista toda la historia del alumno. La misma nota se ve en **SHATCKN**, que es la página que muestra el instructivo 7.1.6 (diap. 19); una corrección después del pase a historia se hace ahí (C124, C194). En **SFASLST**, después del pase, la casilla «Pasada» queda marcada (C190).

### ¿Cómo asigno el docente a un NRC en SSASECT?
SSASECT › periodo › NRC › **Ir** › pestaña «Instructor y horas de reunión». Primero el horario (bloque «Fechas de reunión»: día, hora en 24 horas sin dos puntos, por ejemplo 1530 a 1710; el indicador de sesión 01 lo pone Banner). Luego, en el bloque **Instructor**, sesión 01 › **ID** del docente › Tab: Banner trae el nombre, carga 1.000, responsabilidad 100 y marca **principal**; porcentaje de sesión 100. Guardar: «Saved successfully» (C180; instructivo 6.2.1, diap. 15 y 19). El indicador de sobrepaso del docente se marca solo si sale «Conflicto de horario del instructor» y se revisó la hoja (6.2.1, diap. 20).

### ¿Cómo reviso la carga del docente en SIAASGN?
SIAASGN › ID del docente › periodo › **Ir**: una asignación por página (por ejemplo «10 de 10»); cada una muestra NRC, sesión, principal, carga de trabajo, responsabilidad y contacto semanal. Con **⏬** dos veces se llega al **resumen de la carga** (horas crédito, carga educativa, contacto semanal, periodo FTE). La alerta «Reglas activas de carga de trabajo del docente no definidas para este periodo» no impide consultar: 202656 no tiene reglas de carga y por eso el análisis por criterio sale vacío (C29, C194; E20).

### ¿Cómo pongo un curso en la malla (SMAAREA)?
La malla es el **LIB_AREA** del programa: sin ella el curso no sale en Proyecciones ni cuenta en CAPP (C172, C181). Pasos: **SMAPROG** del programa (por ejemplo `CMEMC44`, XP 07) para ver su área (`MC44-01`). Luego **SMAAREA** › área › **periodo de la versión** (202454, no el de la matrícula; escríbalo a mano porque Intro en la lista elige 999999) › Ir › ⏫ una vez a «Anexo de curso/atributo» › regla (por ejemplo `ECOM-03`) › Regla › clic en Detalles › **+** › materia y curso › Guardar. Banner numera la condición al guardar (C173, C181). En producción se usa «Copiar» a una versión nueva (ref-ruta-inscripcion-y-curso-nuevo.md).

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
