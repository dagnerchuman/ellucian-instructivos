# Restricción por programa (SSARRES) y prerrequisito por programa (SCAPPRQ)

Lo probado en Banner TEST el 29/10/2026 y lo que dijo Nidia Beltrán (consultora de Ellucian) en la reunión de ese día. Detalle y capturas en el registro: C149 a C168, R23, R25, E29, E31, E32, U49 y U50.

## Qué se usa para qué

| Necesidad | Página | Estado |
|---|---|---|
| Que un NRC del centro solo lo lleven ciertos programas (por ejemplo, una ruta XP) | **SSARRES** (un NRC) o **SCARRES** (el curso) › Grado y programa › **Incluir** | Probado (C156, C157) |
| Que un curso de pregrado exija antes un curso del centro (acreditación) | **SCAPPRQ** (por programa de pregrado y versión) | Probado: la fila de Idiomas, sola, bloquea (C163, C165); el Basic «en curso» no cuenta (C166); sin la fila, se inscribe (C167) |
| Amarrar el curso del centro como **correquisito** | SCADETL | **No sirve:** exige el mismo periodo y pregrado (terminación 44) y centros (terminación 54) van en periodos distintos (R22, R24, C159). Ellucian explorará un mismo periodo o partes de periodo (C168, U51): choca con el ADR-005 |

## 1. Restricción de programa en SSARRES

1. **SOATERM** del periodo › «Verificación de errores de inscripción» › **Programa en Fatal**. Si está en «No verificar», la restricción no bloquea (C149). En 202656 está en Fatal desde el 28/10 (C150); en 202744, en No verificar (C162). Lo decide Registros, porque afecta a los tres centros.
2. **SSARRES** › periodo y NRC › Ir › pestaña **Grado y programa** › «Restricciones de programa» › **Incluir** › `+` › código del programa (Banner trae la descripción) › **GUARDAR** (*Saved successfully*).
3. **Prueba en SFAREGS:**
   - alumno **sin** el programa incluido → *«El horario del alumno tiene errores…»*, mensaje **«Program Restriction»**, bandera **«Error fatal»**: no se guarda (C156);
   - alumno **con** el programa → se guarda; SSASECT › Información de ingreso sube «Real» (C156).
4. **El currículo de pregrado también cuenta** (E29, C157): con Incluir `1PCSP15` (Medicina), Arnold Vaca, que en el centro tiene `CMEMC38`, entró a un NRC de nivel C. Sus dos currículos estaban en el **mismo plan de estudios 1**; falta probar con planes distintos.

## 2. Prerrequisito por programa en SCAPPRQ

### Cómo lo configuró Nidia (C159 a C161)
- **Dónde:** SCAPPRQ «Restricciones de prerrequisito de catálogo y de puntaje de examen», con clave **Programa** (de pregrado, por ejemplo `1PCSP15` Medicina) y **Periodo**. Lista los cursos del programa que tienen prerrequisitos, cada uno con método «Básico».
- **Regla:** a cada curso del ciclo se le suma el curso del centro: *prerrequisitos de la malla* **Y (** curso de Idiomas **O** curso de Idiomas **O** curso de Idiomas **)**.
  - Anatomía I `ESEC 00017` = `ESEC 00055` (11) Y ( Basic I `ESEP 02456` O Basic II `02457` O Basic III `02458` ).
  - Farmacología `ESEC 00218` = `ESEC 00019` Y `00169` Y `00278` (11) Y ( Intermediate I `ESEP 02693` O II `02721` O III `02997` ).
  - Según Nidia, se repite hasta el 4.º ciclo; desde el 5.º entra Computación (C161).
  - **Regla del resumen de Ellucian (C168):** desde el 2.º ciclo, al menos un curso de Idiomas; desde el 5.º, Computación; desde el 7.º, Emprendimiento. Falta confirmar el alcance por ciclo (U49).
- **Y, O y paréntesis** (R25; 1.1.5, diap. 18 y 19): «Y» exige las dos filas, «O» basta una, la primera fila no lleva conector y los paréntesis agrupan.
- **Sin nivel ni calificación** en las filas de Idiomas = basta con **haberlo cursado**; con calificación, hay que aprobarlo. Debe estar en la **historia académica**: no es una inscripción simultánea (C159).
- SCAPPRQ **no figura** en los 83 instructivos; solo SCAPREQ (1.1.5).

### Cómo leer SCAPPRQ sin equivocarse (C162, C164)
1. En el bloque clave van el programa y **el periodo de la versión** que se quiere ver (por ejemplo 202444 o 202644), no el periodo de la matrícula.
2. Si se pone otro periodo (por ejemplo 202744), Banner abre la versión vigente para ese periodo y avisa *«“De periodo” no es igual al periodo en el bloque clave; oprimir DUPLICAR-REGISTRO o COPIAR…»*. En ese estado **no deja moverse entre filas y el bloque de prerrequisitos sale vacío**: no sirve para leer.
3. Abajo de la lista se ven «De periodo» y «A periodo» de la versión. Para pasar de curso en curso: clic en una fila y flecha ↓ o ↑.

### Versiones: lo más importante (C162)
- La regla de Nidia está **solo en la versión 202444** (de 202444 a 202544), la del catálogo 2024.
- La **versión 202644** (de 202644 a 999999), la que abre SCAPPRQ para 202744 y la del catálogo de Arnold (202646), **no tiene el Basic**: Anatomía I solo pide `ESEC 00055`.
- Hay que copiar la regla a cada versión (202544, 202644) y confirmar si la matrícula usa la versión del **catálogo del alumno** o la del **periodo de matrícula** (E32).

### Paso a paso de la prueba (C163, C164)
1. **SOATERM 202744** › Verificación de errores › **Prerrequisitos en Fatal** (ya lo está). «En progreso» está sin marcar: un curso en curso no cuenta (R10).
2. **NRC de prueba en SSASECT 202744** › Crear NRC: materia y curso, sección **T1**, campus **SCH**, estatus **A**, tipo **TEO**, método **PRES** (Banner propone VIRT), parte **1**, horas crédito y de cobro (el curso es variable) › GUARDAR › Información de ingreso: Máximo y Proyectado **5** › GUARDAR. Creados: **10020** (`ESEC 00017`), **10021** (`ESEC 00008`), **10022** (`ESEC 00044`).
3. **SFAREGS 202744** (si pide SOADEST, ver la sección 3) › alumno › fila nueva en «Información de curso» con el NRC, RE y plan 1 › GUARDAR.
4. **Resultado** con `A00010005` (alumno de Nidia, catálogo 202444) en el NRC 10020: **«Prerequisite and Test Score error»**, **Error fatal**, no se guardó (Real 0).
5. «Ver detalle de resultados» no dice qué fila falló (*«No hay ningún detalle disponible…»*). **SSAPREQ del NRC está vacío**: el bloqueo viene de **SCAPPRQ**.
6. Todos los cursos que están en SCAPPRQ de Medicina tienen prerrequisitos de la malla, y en TEST nadie ha cursado `ESEC 00055`; los del primer ciclo (por ejemplo Biología Celular `ESEC 00044`) no están en la lista. Para aislar Idiomas hubo que agregar un curso sin prerrequisitos.
7. **Aislar Idiomas (C165).** Claude deja escrito y **el usuario pulsa GUARDAR** (a Claude el control de permisos le bloquea guardar en SCAPPRQ, C164):
   - SCAPPRQ › `1PCSP15` › periodo `202644` › Ir › «Información de curso» › `+` › `ESEC` `00044` › GUARDAR;
   - con esa fila marcada, ⏬ al bloque de prerrequisitos › clic en «Materia» › `ESEP`, curso `02456`, sin nivel ni calificación › GUARDAR;
   - SFAREGS 202744 › Arnold Vaca (`S00912438`) › fila nueva con el **NRC 10022** › GUARDAR → **«Prerequisite and Test Score error»**, no se guarda; SSAPREQ del 10022 vacío. **La fila de Idiomas, sola, bloquea.**
8. **Basic I «en curso» (C166).**
   - SFAREGS **202656** › Arnold › Currículos › fila nueva: programa `IMEMI03` (desde ••• › «Reglas de currículo base por programa»), campo `IDIN`, departamento `EMID` › el usuario guarda. Banner lo deja en el plan de estudios 4.
   - Inscripción 202656 › **NRC 10042** (Basic I, BT) y **10043** (BC1), RE, parte I10. Con el plan 4 sale *«No existe el registro del estatus del ingreso para este plan de estudios»*: se usa el **plan 1** › el usuario guarda (*«Los alumnos ya están inscritos»*).
   - SFAREGS **202744** › fila nueva con el **NRC 10022** › el usuario guarda → **«Prerequisite In Progress»**, **Error fatal**, no se guarda.
   - **Lectura:** Banner ve el Basic en curso de otro periodo, pero no lo acepta porque «En progreso» está sin marcar en SOATERM 202744 (R10). El mensaje es distinto del de quien no lo cursó (paso 7).
9. **Limpieza y prueba de control (C167).**
   - SCAPPRQ `1PCSP15` 202644 › `ESEC 00044` › bloque de prerrequisitos › «–» en `ESEP 02456` › el usuario guarda; luego «–» en `ESEC 00044` › el usuario guarda (quedan 71 cursos).
   - SFAREGS 202744 › Arnold › NRC 10022 › el usuario guarda → **se inscribe sin error**. El bloqueo de los pasos 7 y 8 venía solo de la fila de Idiomas.
   - **La baja no se pudo hacer:** en 202744, parte 1, SFARSTS solo tiene **RE** (SFQRSTS); DD da *«El estatus “DD” es inválido…»* y un RE no se borra (sección 3). Para probar bajas en un periodo de pregrado, Registros tiene que agregar DD en SFARSTS.
10. **Pendiente:** decidir si se marca «En progreso» en el SOATERM de pregrado (vale para todos los prerrequisitos del periodo); copiar la regla a las versiones 202544 y 202644 (E32).

## 3. Incidencias de SFAREGS en el navegador integrado (C158)
- **SOADEST** aparece al abrir SFAREGS en una sesión nueva: llenar los cinco campos con **DATABASE**. GUARDAR da «Función inválida» (no se guarda, queda en la sesión); después abrir SFAREGS desde el buscador de la misma página.
- **Fila con error:** no se puede quitar (*«No es posible eliminar un registro con un estatus que afecta ingreso/estimación»*) ni salir (*«Llave inválida… LIMPIAR DATOS»*). Si se recarga la página, sale *«Otra sesión de inscripción está en progreso para este ID y periodo»*: es por el F5; **se esperan unos minutos** y se libera.
- **Tras guardar**, el cursor queda en «Total de ingreso › Cuotas» y «Comenzar de nuevo» da «Función inválida»: recargar la página (la matrícula ya quedó guardada).
- Si un campo no toma lo escrito: clic, tecla Fin, borrar con retroceso, esperar y escribir de nuevo. Doble clic en un campo abre su lista de valores.

## 4. Lo que quedó en TEST (29/10/2026)
- **NRC 10045** (202656, `ESEC 00701`): parte **X06** (no X07, que no tiene SFARSTS); SSARRES con Incluir `CMEMC44` y `1PCSP15`; Arnold Vaca y `100582059` inscritos con RE. En X06, RE y DD valen hasta el 31-OCT-2026.
- **NRC 10020 y 10021** (202744, sección T1): sin alumnos. **10022**: Arnold Vaca (C167).
- **Arnold Vaca** (`S00912438`): currículo `IMEMI03` (plan 4) y NRC **10042** y **10043** (Basic I) con RE en 202656 (C166); NRC **10022** con RE en 202744, sin poder darlo de baja (C167).
- **SCAPPRQ `1PCSP15` 202644:** sin las filas temporales; se borraron el 29/10 (C167).
- **SOATERM 202656:** Programa en Fatal (C149 dice devolverlo a «No verificar» al terminar).
- La limpieza espera la decisión del usuario.

## Preguntas abiertas
- **Ellucian:** E29 (planes distintos), E31 (¿conviene marcar «En progreso»?, desaprobado), E32 (versión que aplica, concurrencia, calificación 75, bloque de área para Computación), E33 (recargo del 5 %, periodos compartidos, correquisito entre partes).
- **USS:** U49 (qué nivel, desde qué ciclo, a qué cursos y con qué nota), U50 (primero paga y luego se inscribe: confirmado en C168, falta Faber), U51 (¿unificar periodos?, ADR-005), U43 (cómo se amarra la acreditación).
