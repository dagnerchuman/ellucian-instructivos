# Cómo manejar Banner TEST con el navegador (para cualquier agente)

Método con el que se hicieron las pruebas del 28 y 29/10/2026 (C153 a C167) en `experience-test.elluciancloud.com/ussipantest`. Sirve igual para Claude (navegador integrado) y para Antigravity (su navegador): las acciones son las mismas, clic, escribir, tecla, captura y zoom. Si una pantalla no se comporta como aquí, se toma una captura y se dice lo que se ve, sin suponer.

## 1. Reglas de trabajo con el usuario
1. **El agente deja escrito, el usuario guarda.** El agente abre la página, llena los campos y se detiene. Escribe: «Dagner, haz esto: pulsa GUARDAR» y lo que debe salir. El usuario guarda y responde «Ya guardé» o «Salió error». No se cierra el navegador entre pasos (C165).
2. **Nunca guardar sin permiso.** El usuario lo pidió desde la primera prueba («pregúntame ¿prosigo? antes de cada guardado»). En SCAPPRQ, además, el control de permisos le bloquea el guardado a Claude (C164).
3. **Después de cada «Ya guardé», captura.** Se lee el aviso de arriba a la derecha: verde *Saved successfully (n rows saved)* o *Los alumnos ya están inscritos*; rojo *\*ERROR\**. Se le dice al usuario si guardó o no y por qué.
4. **Se anota en el registro** lo que pasó (C##) con el mensaje exacto de Banner; las filas temporales se apuntan para borrarlas al final.

## 2. Por qué sale rápido
- **Encadenar acciones** en un solo lote: clic → esperar 1 s → escribir → Tab → esperar 3 s → captura. Banner valida cada campo al salir de él: tras Tab o Ir, esperar 2 a 5 s antes de la captura.
- **Capturas pequeñas y zoom.** Para comprobar un campo basta un zoom de esa franja; no hace falta leer la página entera. El texto de Banner está dentro de un marco: «leer el texto de la página» devuelve casi nada, así que se lee con capturas.
- **Dejar que Banner llene.** En SFAREGS basta escribir el NRC y pulsar Tab: Banner trae materia, curso, sección, estatus RE, nivel, parte de periodo, método y campus, y salta solo al plan de estudios.
- **Tener a mano los datos de prueba** (sección 6), para no buscarlos cada vez.

## 3. Moverse en una página de Banner 9

| Acción | Cómo |
|---|---|
| Abrir una página | Lupa de arriba a la derecha › escribir el código (SFAREGS, SCAPPRQ…) › clic en el resultado. Con el enlace directo (`…/BannerAdmin?form=SFAREGS…`) a veces pide SOADEST (sección 5) |
| Llenar el bloque clave | En el orden de la pantalla (C86, C87): en SFAREGS, periodo → ID → plan. Clic en el campo siguiente para que valide y luego **Ir** (arriba a la derecha) |
| Campo que no toma lo escrito | Clic › esperar 1 s › Fin › retroceso varias veces › esperar › escribir › comprobar con zoom antes de seguir |
| Volver al bloque clave | El mismo botón de arriba a la derecha (flecha circular, «Comenzar de nuevo») |
| Pasar al bloque siguiente o anterior | Botones **⏬** y **⏫** de abajo a la izquierda. Un clic en una fila no siempre mueve el foco al bloque: usar ⏬ |
| Agregar una fila | Con el foco en el bloque, **+** de su encabezado: la fila nueva queda debajo de la actual |
| Borrar una fila | Seleccionarla › **–** de su encabezado: desaparece y el contador baja; se aplica al GUARDAR. Primero el detalle y luego el maestro, cada uno con su guardado (SCAPPRQ: el prerrequisito y después el curso, C167) |
| Ver columnas ocultas | Rueda horizontal sobre la tabla (Estatus, Parte de periodo, Plan, Mensaje) |
| Ver el error de una fila | Clic en la fila: debajo salen «Bandera de error», «Tipo de estatus» y «Mensaje». «Ver detalle de resultados» casi nunca dice más (C163, C166) |
| Lista de valores | **•••** del campo. Doble clic también la abre. **Intro** dentro de la lista elige la primera fila, aunque no sea la buscada (C164). **ANULAR** cierra sin elegir |
| Cerrar un aviso | Clic sobre el aviso |

Referencia en una ventana de 800 × 670 (comprobar siempre con captura): Ir y «Comenzar de nuevo» ≈ (767, 102); ⏬ ≈ (67, 657); ⏫ ≈ (21, 657); GUARDAR ≈ (760, 657); en SFAREGS, + del bloque «Información de curso» ≈ (695, 406).

## 4. Recetas probadas

### Matricular a un alumno en un NRC (SFAREGS)
1. SFAREGS › periodo › ID › Ir.
2. ⏬ dos veces hasta «Información de curso» › **+** › NRC › Tab › plan de estudios (el que tenga registro en «Plan de estudios de ingreso»; si no, sale *«No existe el registro del estatus del ingreso para este plan de estudios»*, C166) › Tab.
3. Si queda una fila vacía al final, se deja: no se guarda.
4. El usuario guarda. Correcto: *«Los alumnos ya están inscritos»*. Para comprobarlo, volver a abrir con Ir.
5. Error: *«El horario del alumno tiene errores»*; el motivo está en la columna Mensaje («Program Restriction», «Prerequisite and Test Score error», «Prerequisite In Progress»). Esa fila ya no se puede quitar: recargar la página y esperar el candado (sección 5).

### Dar de baja (SFAREGS)
- Columna Estatus › DD › Tab. Si sale *«El estatus “DD” es inválido…»*, la parte de periodo no tiene DD en SFARSTS. Con ••• en Estatus se abre SFQRSTS con los estatus permitidos (en 202744, parte 1, solo RE). Un RE no se borra (C158, C167).

### Agregar el programa del centro a un alumno (SFAREGS › Currículos)
- Fila nueva › programa desde **••• › «Reglas de currículo base por programa»** › fila del campus › OK; campo de estudio y departamento. Escribir el programa a mano y pulsar Intro arrastra datos de otro currículo (C153, C166).

### Leer o cambiar SCAPPRQ
- Programa + **periodo de la versión** (202444, 202644), no el de la matrícula (C164) › Ir › clic en el curso › ⏬ al bloque de prerrequisitos. Agregar: **+** › materia, curso, sin nivel ni calificación si basta haberlo cursado.

### Buscar un alumno con un curso en su historia (SHACRSE)
- SHACRSE › ID › **periodo vacío** › Ir: todos sus cursos con periodo, NRC, nota y modo. Así se encontró a `A00010005` con Basic I (C170). Solo consulta.

### Crear un NRC (SSASECT)
- Ver la guía [ref-restricciones-y-prerrequisitos-por-programa.md](../../arquitectura-centros-empresariales/references/ref-restricciones-y-prerrequisitos-por-programa.md), paso 2 de la sección 2.

## 5. Incidencias y salida
- **SOADEST** al abrir SFAREGS en una sesión nueva: DATABASE en los cinco campos; GUARDAR da «Función inválida»; abrir SFAREGS otra vez desde la lupa (C158).
- **«Otra sesión de inscripción está en progreso»:** alguien recargó con cambios pendientes; se esperan unos minutos (C158).
- **«Llave inválida… LIMPIAR DATOS»** al volver al bloque clave con algo a medio cambiar: recargar la página sin guardar (se pierde solo lo no guardado) y esperar el candado si sale.
- **Tras guardar en SFAREGS** la página puede volver sola al bloque clave con el aviso de inscritos: es normal.
- **«El uso de la página de inscripciones está prohibida para este periodo…»** al abrir SFAREGS: arrastró el periodo de la página anterior (por ejemplo 202444 de SCAPPRQ) y lo vació. Escribir el periodo de matrícula.
- **«La persona no es alumno, no se puede inscribir»** con un ID correcto: el ID no se validó (no sale el nombre al lado). Clic en el ID, borrar el último carácter, escribirlo y Tab.
- **Con «Ver currículos actuales/activos» marcado** desaparece el bloque «Plan de estudios de ingreso» y la fila nueva puede quedar **sin plan**: revisar la columna Plan de estudios antes de pedir el guardado (C170).
- **Sesión de Banner vencida:** pide iniciar sesión con Google; lo hace el usuario, nunca el agente.

## 6. Datos de prueba en TEST (29/10/2026)
- **Alumno:** Arnold Vaca `S00912438` (Medicina `1PCSP15`, plan 1; `CMEMC38`; `IMEMI03` en el plan 4). En 202744 tiene los NRC 10001 a 10008 de otra persona: **no se tocan**.
- **Otro alumno:** `100582059` (`CMEMC44`). **Alumno de Nidia:** `A00010005` (catálogo 202444; Basic I con 80 en 202646; en 202744 tiene 10023, 10024, 10022 y 10007; avisar a Nidia antes de usarlo).
- **NRC:** 10045 (202656, X06, Computación), 10042 y 10043 (Basic I, 202656, I10), 10020 a 10022 (202744, T1, pregrado).
- Lo que quedó en TEST y falta limpiar: sección 4 de la guía de restricciones y C167.
