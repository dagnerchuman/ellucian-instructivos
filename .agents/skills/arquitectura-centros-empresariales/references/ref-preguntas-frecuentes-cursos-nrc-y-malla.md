# Preguntas frecuentes de operación: Cursos, malla y periodos

Respuestas cortas para el asistente IA y para cualquier agente, tomadas de lo probado en TEST (NRC 10044 y 10045) y del registro. Cada pregunta es un fragmento de la base del asistente (C197). Si la respuesta no está aquí ni en el registro, se dice «No lo sé» (ruta de escape).

Tema de este archivo: SCACRSE, SMAAREA, atributos, parte X06, periodos e Inglés. Los otros temas están en los demás `ref-preguntas-frecuentes-*.md` (índice en el `SKILL.md` de esta skill).

### ¿Qué es un atributo de curso (STVATTR) y para qué sirve en la malla?
Es un código de 4 caracteres que marca cursos que comparten algo (por ejemplo «electivo» o «taller»). Se crea en **STVATTR** (código y descripción de hasta 30 caracteres), se pone a cada curso en **SCADETL** › pestaña **«Atributos de grado»** (materia, curso y periodo desde el que rige › insertar › guardar) y la malla lo pide en **SMAAREA** › regla › Detalles, columna **«Atributo de curso»**, sin poner materia ni curso. Así el CAPP cuenta cualquier curso con ese atributo **sin listar curso por curso** en la regla (instructivo 1.2.2, diap. 5, 11, 14 y 18 a 22; 6.1.2, diap. 9, 20 y 21). El NRC hereda los atributos del catálogo en SSADETL (5.3, diap. 37). No es lo mismo que el **atributo de alumno** (otra columna de SMAAREA, y el parámetro 07 de SFRGRUP). **En TEST (C218):** STVATTR ya tiene 65 códigos de los centros (`COM1` a `COM3`, `C011` a `C074`, `ING1` a `ING6`, `NIV1` a `NIV4`…), así que no hace falta crear uno. La prueba propuesta es marcar los talleres de Computación y pedir el atributo en `ECOM-04` de `MC42-01` (C174, C208); quién crea códigos en STVATTR está por confirmar.


### ¿Finanzas ya enlazó los atributos de curso con un código de pago o cargo?
**En TEST, todavía no** (revisado sin guardar el 20/11/2026, C218). El enlace se hace en **SFARGFE** con tipo de regla **`ATTR`**: el atributo del curso › un **código de detalle de cargo** (como `X032` Basic I), no de pago; los de pago (`M001` Efectivo…) se usan en la caja (instructivo 11.1.1, diap. 74 a 80). Lo que se vio:
- **SFARGFE** `ATTR`, captura Regular: sin reglas en 202754, 202656 ni 202744; en 202754 tampoco por Nivel ni Campus.
- **SCADETL** › Atributos de grado: Basic I (`ESEP 02456`) tiene `ING1`; Diseño Web (`ESEC 00684`) y el taller `ESEC 00697`, ninguno. Los códigos de cuota de Basic I están vacíos (los `X032` y `X228` de C68 ya no están).
- **SSADETL** del NRC 10001 (Basic I, 202754): sin cuotas de sección y con atributo `C011` «Computación I», distinto del `ING1` del curso.
Por confirmar con Finanzas si lo hicieron en producción o con otra regla. Capturas en `docs/fuentes/banner-test/capturas/` (C218).

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

### ¿Cuál es el orden de los cursos de Inglés y tienen prerrequisito?
Sí. Idiomas usa **prerrequisito Fatal**: quien desaprueba BASIC I no pasa a BASIC II, salvo con **examen de suficiencia** (C11, R09). La cadena es BASIC I → BASIC II → BASIC III → INTERMEDIATE I → INTERMEDIATE II → INTERMEDIATE III; BASIC I → BASIC II está confirmado y el resto se asume igual (datos.json de Idiomas). En Banner va en SCAPREQ/SSAPREQ con la verificación en Fatal en SOATERM. Computación, en cambio, no tiene orden entre los cursos de la ruta (C191).
