# Preguntas frecuentes de operación: Selección de población y procesos masivos

Respuestas cortas para el asistente IA y para cualquier agente, tomadas de lo probado en TEST (NRC 10044 y 10045) y del registro. Cada pregunta es un fragmento de la base del asistente (C197). Si la respuesta no está aquí ni en el registro, se dice «No lo sé» (ruta de escape).

Tema de este archivo: GLRSLCT, GJAJFLU, GJRPSIM, GLAEXTR y CAPP masivo SMRBCMP. Los otros temas están en los demás `ref-preguntas-frecuentes-*.md` (índice en el `SKILL.md` de esta skill).

### ¿Qué es una selección de población y en qué páginas se arma?
Es una lista de ID de Banner (alumnos) guardada con un nombre, para correr un proceso masivo solo sobre ese grupo. Por ejemplo, la estimación de cuotas SFRFASC de cuentas por cobrar (C73), o el cálculo del PGA SHRCGPA solo para ese grupo (parámetros 03 identificador de selección, 04 aplicación y 05 creador; instructivo 7.2.2, diap. 27). Se arma con estas páginas (instructivo 7.1.10; C202):
1. **GLRAPPL**, código de aplicación: el grupo al que pertenece la selección (ej. `CAPP`), con su descripción y el origen de los datos, *student* (diap. 9 y 10).
2. **GLRSLCT**, código de selección de población: se crea el **ID de selección** dentro de esa aplicación, con su descripción (diap. 11 y 12). Aquí también se definen las reglas, si la lista sale por reglas.
3. Los ID entran de una de tres formas:
   - **a mano** en **GLAEXTR** (diap. 14 y 15);
   - **por archivo .csv**: **GJAJFLU** sube el archivo al servidor y **GJRPSIM** carga sus ID en la selección ya creada en GLRSLCT (diap. 17 a 24);
   - **por reglas**: la condición se escribe en GLRSLCT y se ejecuta **GLBDATAJ** (diap. 27 a 36).
4. **GLAEXTR**: se revisa quiénes quedaron en la selección (aplicación + ID de selección + creador) (diap. 25 y 37).

El orden lo dio el usuario y coincide con el instructivo. La carga **por CSV ya se probó en TEST** (C203); a mano y por reglas, aún no (C202).

### ¿Cómo cargo una selección de población desde un archivo .csv (GJAJFLU y GJRPSIM)?
**Probado en TEST el 19/11/2026** con la selección `POB_CICLO_B` de la aplicación `STUDENT`: 11 alumnos cargados, 0 duplicados y 0 inválidos (C203). Pasos (instructivo 7.1.10, diap. 17 a 25):
1. **Archivo .csv**: una columna con el encabezado `ID` y un ID de Banner por fila. Dele un nombre corto; en la prueba, `PRUEBA.csv`.
2. **GLRSLCT**: aplicación, **ID de selección** y **ID de creador** › **Ir** › descripción › **Guardar** (diap. 11 y 12). En la prueba: `STUDENT`, `POB_CICLO_B`, «Población prueba ciclo B», sin «Manual» y sin reglas, porque los ID vienen del archivo. Si la aplicación ya existe, como `STUDENT`, no hace falta GLRAPPL.
3. **GJAJFLU** (cargar el archivo al servidor): Trabajo **GJRPSIM** › **Ir** (diap. 18). Con el botón de la carpeta elija el .csv; «Nombre de archivo» y «Nombre de archivo para 'guardar como'» quedan con el nombre del archivo › **Guardar**. Sale «Guardado con suceso (1 registros guardados)» y la **Ruta del archivo** (en la prueba, `/u05/jobsub/PRUEBA.csv`; diap. 19).
4. **GJAPCTL** › proceso **GJRPSIM** (Importar lista de ID o PIDM) › **Ir** (diap. 20). Impresora **DATABASE** (diap. 21).
5. **Valores de parámetro** 01 a 09 (diap. 22 y 23):

   | N.º | Parámetro | Prueba en TEST (C203) | Lámina |
   |---|---|---|---|
   | 01 | ID de la aplicación | `STUDENT` | `CAPP` |
   | 02 | ID de la selección | `POB_CICLO_B` | `CAPP_01` |
   | 03 | ID del creador: **el mismo de GLRSLCT**, no el de quien sube el archivo | el creador de la selección | el usuario |
   | 04 | Indicador del sistema: S sistema o M manual | `S` | `S` |
   | 05 | Tipo de dato del archivo: I = ID o P = PIDM | `I` | `I` |
   | 06 | Ruta o nombre del archivo: basta el nombre, porque GJAJFLU lo dejó en el directorio de trabajos | `PRUEBA.csv` | `CAPP_01.csv` |
   | 07 | Depurar todo registro anterior de la selección: Y o N | `N` | `N` |
   | 08 | Verificar el ID como ID anterior: Y o N | `N` | `N` |
   | 09 | Verificar el ID con el apellido: Y o N | `N` | `N` |

6. **Enviar** › **Guardar** (diap. 24). Revise la salida en **GJIREVO** › `gjrpsim_<job>.lis`: «Total number of records processed from data file», «Duplicate records found» e «Invalid records found» con su lista (en la prueba: job 8379, 11, 0 y 0).
7. Revise en **GLAEXTR** los ID cargados: aplicación, selección y creador › **Ir** (diap. 25). En la prueba salieron los 11 alumnos con **Indicador de sistema = Sistema** (por el 04 en `S`), «Registro 1 de 11»; arriba están «Eliminar todos», «Ordenar por nombre / por ID» y «Ordenar primero registros manuales» (C204).

Lo que hay que guardar para usar la selección después: **aplicación, ID de selección, creador y nombre del archivo**. Si el 07 va en `Y`, la carga borra lo que ya tenía la selección, manual y de sistema. Con `N`, agrega. Un ID que no existe en Banner sale en «Invalid List».

### ¿Cómo corro el CAPP masivo (SMRBCMP) para una selección de población?
El CAPP masivo evalúa el avance curricular de todos los alumnos de una selección de población. Es el paso B7 de la prueba B. Pasos (instructivo 7.2.4, diap. 43 a 53; C204):
1. **GJAPCTL** › proceso **SMRBCMP** (Proc. de cumplimiento p/lotes) › **Ir** (diap. 43). Impresora **DATABASE** (diap. 44).
2. **Valores de parámetro**: son 20; amplíe los registros por página o pase a la página 2 (diap. 45 a 47):

   | N.º | Parámetro | En TEST, 19/11/2026 (C204) | Qué dice el instructivo |
   |---|---|---|---|
   | 01 | Periodo a procesar | `202744` | el periodo a evaluar (R) |
   | 02 | Modo de ejecución | `P` | **P** población, **C** compilación (solicitudes individuales pendientes, sin selección) o **H** solo impresión (R) |
   | 03 | Código de aplicación | `STUDENT` | obligatorio con modo P |
   | 04 | Identificador de selección | `POB_CICLO_B` | obligatorio con modo P |
   | 05 | ID de creador | el creador de la selección | obligatorio con modo P |
   | 06 | ID de usuario | quien ejecuta el proceso | obligatorio con modo P |
   | 07 | Origen del currículo | `S` | `S` |
   | 08 | Estatus de grado | vacío | código de STVDEGS (O) |
   | 09 | ¿Copia impresa de población? | vacío | Y o N (O) |
   | 10 | ID de impresora | vacío | en blanco |
   | 11 | Tipo impresión de cumplimiento | vacío | (O) |
   | 12 | Enviar a asesores | `N` | generalmente N |
   | 13 a 16 | Solo asesor principal, tipo de asesor, jerarquía y fecha de dirección | vacíos | en blanco |
   | 17 | Criterio de ordenamiento | vacío | N nombre, Z código postal, P programa (O) |
   | 18 | ID de sesión | vacío | en blanco |
   | 19 | Predefinir código de parámetro | `BATCH` | el código predefinido de **SMADFLT** para el CAPP masivo |
   | 20 | Crear datos SAP | `N` | `N` |

3. Pase al bloque Envío: **Enviar** › **Guardar** (diap. 48 y 49). «Guardar parámetros como» con un nombre deja los valores listos para la próxima vez. Banner da el número de proceso (diap. 50).
4. ⋮ › **Relacionado** › **Revisar salida (GJIREVO)** › el `.lis` (diap. 51 a 53). El CAPP masivo tarda: mientras corre, sale el aviso de error «No hay salidas guardadas…», que desaparece al terminar (diap. 52). El detalle por alumno se ve en **SMICRLT**.

**Probado en TEST el 19/11/2026** con la selección `POB_CICLO_B` (C204, C205):
- Al guardar con «Guardar parámetros como» sin nombre, Banner avisa «Guardando los valores actuales del parámetro como los predefinidos a nivel de usuario»: la próxima vez SMRBCMP abre con esos valores. Luego da el **número de secuencia**.
- En **GJIREVO**, el proceso deja cuatro archivos: `smrbcmp_<job>.lis` (el reporte), `smrbcmp_<job>.log`, `smrcmjx_<job>.log` y `gjrjlis_<job>.log`. Se abre el **.lis**.
- El .lis es el «Batch Compliance Control Report»: una línea por alumno con ID, nombre, programa, **REQ#** (número de solicitud de cumplimiento) y el mensaje **«Compliance run 19-NOV-26»**. En la prueba salieron los 11 alumnos.
- Cada alumno queda con una **solicitud de cumplimiento** en **SMARQCM** (en la prueba, la n.º 3, periodo de evaluación 202744, originador `AUTO` «Generado Automáticamente», con «Usar cursos en progreso», «Crear registros de área no usada», «Crear cursos/atributos no usados» y «Crear registros de rechazo»). El detalle del avance se ve en **SMICRLT**.
- Este CAPP del periodo es el insumo de la **proyección** (SFPPROJ): por eso va antes.

**Permisos para ejecutar el CAPP** (C206): **GJAPCTL** (enviar el proceso), **GUQINTF** (enviar/ejecutar el proceso), **GURINSO** (proceso que inserta los resultados en la base de datos), **GJIREVO** (consultar los resultados) y **GJRRPTS** (proceso de ejemplo ejecutado). Si al correr SMRBCMP falta alguno, hay que pedirlo.

### ¿Cómo armo una selección de población por reglas o a mano?
- **A mano (GLAEXTR):** aplicación, ID de selección y creador › **Ir**. Escriba cada ID o búsquelo con los tres puntos › **Guardar** (instructivo 7.1.10, diap. 14 y 15).
- **Por reglas (GLRSLCT):**
  1. En la selección, escriba Seleccionar `SORLCUR_PIDM` y De `SORLCUR`, la tabla de planes de estudio del alumno (diap. 27).
  2. Busque el elemento de datos, por ejemplo `SORLCUR_PROGRAM` (diap. 28 y 29).
  3. Ponga el operador `=` y el valor, en la lámina el programa `ICOMD103PR` › **Guardar** (diap. 30).
  4. **Cierre la página** para que la regla quede lista (diap. 31).
  5. Ejecútela en **GJAPCTL** › **GLBDATAJ** (extracción de la selección) › impresora DATABASE (diap. 32 y 33). Los parámetros 01 (ID de selección), 06 (código de aplicación), 07 (creador) y 08 (reporte de detalle, `Y`) son obligatorios. El 02 al 05 sirven para unir (U), cruzar (I) o restar (M) dos selecciones en una nueva (diap. 34; el título de esa lámina dice GJRPSIM por error: son los parámetros de GLBDATAJ).
  6. **Enviar** › **Guardar** (diap. 35). En **GJIREVO** el .lis dice cuántos ID se seleccionaron (464 en la lámina; diap. 36). Revise la lista en **GLAEXTR** (diap. 37).

**Aún no se prueba en TEST** (C202): los pasos son los del instructivo 7.1.10.
