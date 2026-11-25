# Cómo manejar Banner TEST con el navegador (para cualquier agente)

Método con el que se hicieron las pruebas del 28 y 29/10/2026 (C153 a C167) en `experience-test.elluciancloud.com/ussipantest`. Sirve igual para Claude (navegador integrado) y para Antigravity (su navegador): las acciones son las mismas, clic, escribir, tecla, captura y zoom. Si una pantalla no se comporta como aquí, se toma una captura y se dice lo que se ve, sin suponer.

## 1. Reglas de trabajo con el usuario
1. **El agente deja escrito, el usuario guarda.** El agente abre la página, llena los campos y se detiene. Escribe: «Dagner, haz esto: pulsa GUARDAR» y lo que debe salir. El usuario guarda y responde «Ya guardé» o «Salió error». No se cierra el navegador entre pasos (C165).
2. **Nunca guardar sin permiso.** El usuario lo pidió desde la primera prueba («pregúntame ¿prosigo? antes de cada guardado»). En SCAPPRQ, además, el control de permisos le bloquea el guardado a Claude (C164).
3. **Después de cada «Ya guardé», captura.** Se lee el aviso de arriba a la derecha: verde *Saved successfully (n rows saved)* o *Los alumnos ya están inscritos*; rojo *\*ERROR\**. Se le dice al usuario si guardó o no y por qué.
4. **Se anota en el registro** lo que pasó (C##) con el mensaje exacto de Banner; las filas temporales se apuntan para borrarlas al final.
5. **Antes de llenar la respuesta de dudas, consulta tú mismo en TEST** (C214). Si algo se puede ver en Banner sin guardar (una configuración, un NRC, un proceso), se abre y se mira; no se le pregunta al usuario lo que TEST ya dice. Al usuario solo se le pregunta lo que es decisión suya (qué código usar, quién lo hace) o lo que no está en TEST. Lo dijo así: «¿por qué te haces tantas dudas? Mejor entra a revisar tú mismo en el TEST».
6. **Solo Ellucian Experience (sin barra morada), C222.** El usuario lo pidió el 20/11/2026: «sin la barra morada mejor», y se molestó cuando se abrió Banner Admin directo en otra pestaña para leer y comprobar. No se usa `banneradmin-test…` ni para consultar: otro NRC o un guardado se revisan en Experience, desde la Banner Search Card.
7. **Antes de pedir (o hacer) el guardado, revisa todos los campos con zoom** (C222): en SSASECT faltaron la **sección** y el **socio de integración** (`OPLMS`) y el usuario tuvo que avisar. Compara campo por campo con un NRC del mismo curso. Si un campo da error, el foco se queda en él y lo siguiente que se escribe cae ahí: llena un campo a la vez.
8. **Una captura del usuario puede estar cortada.** Antes de decir que algo «no está» o «falta», mira el contador de abajo («Registro 1 de 20») y cuenta las filas visibles; las columnas de la derecha también pueden faltar. En C213 se dijo que el NRC 10041 no tenía encuesta porque la captura no mostraba las dos últimas filas: estaba (C214). Si no se ve todo, se dice «en la captura no se ve» y se revisa en TEST.

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
| Menú «Relacionado» (por ejemplo GJAPCTL › Revisar salida [GJIREVO]) | **⋮** de arriba › Relacionado. El icono de la hoja con + es BDM y da una advertencia de ApplicationXtender (C194) |
| **Leer la pantalla como texto** (C217; **ya no se usa**, el usuario prefiere Experience, C222) | En Experience, Banner va dentro de un marco de otro dominio y solo se lee con capturas. Abriendo Banner Admin directo, `https://banneradmin-test.usspesaas.elluciancloud.com/BannerAdmin?form=<PÁGINA>` (misma sesión de Google), «leer el texto de la página» trae todos los campos, también las columnas ocultas, y las listas largas se leen poniendo 50 por página y desplazando la lista. Cada página abierta así empieza una sesión nueva (SOADEST o TOADEST otra vez) |
| Bloque que ⏬ no alcanza («Función inválida») | Bajar con la rueda: así se ve «Total de ingreso» en SFAREGS (C194) |

Referencia en una ventana de 800 × 670 (comprobar siempre con captura): Ir y «Comenzar de nuevo» ≈ (767, 102); ⏬ ≈ (67, 657); ⏫ ≈ (21, 657); GUARDAR ≈ (760, 657); en SFAREGS, + del bloque «Información de curso» ≈ (695, 406).

## 4. Recetas probadas (un archivo por tema)

Abre solo el archivo del tema que vas a probar. Cada receta supone las reglas y los movimientos de las secciones 1 a 3.

| Tema | Archivo | Recetas |
|---|---|---|
| Matrícula en SFAREGS | [recetas/matricula-sfaregs.md](recetas/matricula-sfaregs.md) | Matricular a un alumno en un NRC; Dar de baja; Agregar el programa del centro a un alumno |
| Mallas, prerrequisitos e historia | [recetas/mallas-y-prerrequisitos.md](recetas/mallas-y-prerrequisitos.md) | Leer o cambiar SCAPPRQ; Buscar un alumno con un curso en su historia; Ver una malla |
| NRC | [recetas/nrc-ssasect.md](recetas/nrc-ssasect.md) | Crear un NRC; Completar el horario y el docente de un NRC ya creado; Regla de asistencia de un NRC |
| Notas, asistencia y cierre | [recetas/notas-y-cierre.md](recetas/notas-y-cierre.md) | Cargar la fórmula de un NRC; Pasar lista y enviar la asistencia al libro; Pase a historia de un NRC |
| Encuesta docente (TESS) | [recetas/encuesta-docente-tess.md](recetas/encuesta-docente-tess.md) | Revisar la encuesta docente de un NRC |
| Caja, Finanzas (no es de los centros) | [recetas/caja-tvacaja.md](recetas/caja-tvacaja.md) | TOADEST, cargos en TVACAJA, códigos de pago, perfil de cajero |

Una receta nueva va al archivo de su tema; si no encaja en ninguno, se crea otro en `recetas/` y se agrega una fila aquí.

## 5. Incidencias y salida
- **SOADEST** al abrir SFAREGS en una sesión nueva (clic, 1 s, escribir, Tab y 2 s por campo: escrito de corrido solo toma el primero, C194): DATABASE en los cinco campos (Horarios, Facturas, Históricos académicos, Ingresos, Cumplimiento) y abrir SFAREGS otra vez desde la lupa. **No hace falta guardar** (GUARDAR da «Función inválida», C158; probado sin guardar en C185).
- **«Otra sesión de inscripción está en progreso»:** alguien recargó con cambios pendientes; se esperan unos minutos (C158).
- **«Llave inválida… LIMPIAR DATOS»** al volver al bloque clave con algo a medio cambiar: recargar la página sin guardar (se pierde solo lo no guardado) y esperar el candado si sale.
- **Tras guardar en SFAREGS** la página puede volver sola al bloque clave con el aviso de inscritos: es normal.
- **«El uso de la página de inscripciones está prohibida para este periodo…»** al abrir SFAREGS: arrastró el periodo de la página anterior (por ejemplo 202444 de SCAPPRQ) y lo vació. Escribir el periodo de matrícula.
- **«La persona no es alumno, no se puede inscribir»** con un ID correcto: el ID no se validó (no sale el nombre al lado). Clic en el ID, borrar el último carácter, escribirlo y Tab.
- **Con «Ver currículos actuales/activos» marcado** desaparece el bloque «Plan de estudios de ingreso» y la fila nueva puede quedar **sin plan**: revisar la columna Plan de estudios antes de pedir el guardado (C170).
- **TOADEST** al abrir TVACAJA, TGAUPRF u otra página de cuentas por cobrar (C217): `DATABASE` en Facturas, Recibos y Resumen de alumno y cerrar con la X; Banner vuelve solo a la página pedida. No se guarda.
- **Sesión de Banner vencida:** pide iniciar sesión con Google; lo hace el usuario, nunca el agente.

## 6. Datos de prueba en TEST (29/10/2026, actualizado el 04/11/2026)
- **Alumno:** Arnold Vaca `S00912438` (Medicina `1PCSP15`, plan 1; `CMEMC38`; `IMEMI03` en el plan 4). En 202744 tiene los NRC 10001 a 10008 de otra persona: **no se tocan**.
- **Arnold Vaca en 202656:** el 10045 quedó en **DD** el 31-OCT-2026 (C189); el 10042 y el 10043 siguen con RE.
- **Alumno de Emprendimiento:** `S00912627` «ALUMNO / PRUEBA, EMPRENDIMIENTO U.» (`MMEMM01`, plan 1), matriculado con RE en el 10047 (C245 a C247). Es de prueba: se puede usar.
- **Otro alumno:** `100582059` (`CMEMC44`); desde el 04/11/2026 SFAREGS le muestra «Retenciones: Y» (C194). **Alumno de Nidia:** `A00010005` (catálogo 202444; Basic I con 80 en 202646; en 202744 tiene 10023, 10024, 10022 y 10007; avisar a Nidia antes de usarlo).
- **NRC:** 10045 (202656, X06, Computación; miércoles 15:30–17:10, SAUVIR / SALA-VIRT, docente 100582059, malla `MC44-01` › `ECOM-03`, fórmula en SHAGCOM y regla 3 de SOAATRK desde el 30/10, C180 a C182). **Prueba completa:** notas 85 → 17, pase a historia (jobs 7994 y 7995) y 17 en SHACRSE (C188 a C190). También 10042 y 10043 (Basic I, 202656, I10), 10020 a 10022 (202744, T1, pregrado).
- **SOATERM 202656** (solo consulta, C182): En progreso sin marcar, Permitir ✓, Plan de estudios requerido ✓; las demás casillas sin marcar; secuencia de inicio de NRC 10046.
- **Acceso a TEST:** https://experience-test.elluciancloud.com/ussipantest, también en el botón «Banner TEST» de la galería y del visor del sitio (C178). Cada persona entra con su cuenta de Google.
- Lo que quedó en TEST y falta limpiar: sección 4 de la guía de restricciones y C167.
