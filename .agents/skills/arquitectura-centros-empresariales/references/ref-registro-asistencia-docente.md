# Registrar asistencia como docente

## Acceso y pasos
1. En el **Autoservicio docente** (pestaña **Autoservicio Docentes**, tarjeta **«Detalle de Notas y Asistencia»** › **Ingresar asistencia**), abre **Control de asistencia › Lista de cursos** (el instructivo la llama «Ingreso de asistencia»). La tarjeta «Faculty Grading» da error y no hace falta (C119). *(instructivo 10.4.2.4.5 Configuración de Autoservicio, diap. 16; C101)*
2. Busca el **NRC** y la sesión de clase correspondiente; pulsa **Pasar lista**. *(instructivo 7.1.1 Gestionar la asistencia a clases, diap. 44)*
3. En la lista, marca a cada alumno para la fecha seleccionada: **✓ verde** = presente y **− rojo** = ausente. Solo se permiten fechas pasadas, no futuras. *(instructivo 7.1.1, diap. 45–46)*
4. Banner calcula el porcentaje de asistencia mientras se registran las marcas. *(instructivo 7.1.1, diap. 47)*
5. **Actualizar todo** permite marcar masivamente registros vacíos o a todos como presentes/ausentes. No usar estas opciones sin revisar a quién se aplicará cada marca. **No envía nada al libro.** *(instructivo 7.1.1, diap. 48)*
6. Al terminar el periodo, cuando el porcentaje ya considera todas las sesiones, pulsa **Clase › «Actualizar la asistencia en el libro de calificaciones»** y confirma el paso del porcentaje al componente de calificaciones (`ATTRGRD`). *(instructivo 7.1.1, diap. 56–57; R21)*

## Requisitos si algo no aparece
- El docente debe tener disponible el proceso `ENTERATTEND` en Autoservicio. El acceso puede depender de la relación docente-alumno o de que sea instructor principal en `SSASECT`. *(instructivo 7.1.1, diap. 14–15)*
- El periodo debe tener configuradas en `SOATERM` las fechas de acceso docente a Autoservicio. *(instructivo 7.1.1, diap. 12)*
- La regla de asistencia de la sesión del NRC debe estar activa, con **Desplegar clase**, **Control de asistencia**, unidad de control y fechas de inicio/fin. Se configura por cada sesión. *(instructivo 7.1.1, diap. 42)*
- Si `SHAGCOM` muestra el error «Debe configurar los controles del libro de calificaciones en SHAEGBC», configura primero el calendario de calificaciones en **`SHAEGBC`**: periodo → **Ir** → fecha abierta y fecha de corte institucionales → guardar; luego regresa a `SHAGCOM`. *(instructivo 7.1.4, diap. 40–43)*

## Estado de validación
- **Validado en TEST (C101–C107, 23–24/10/2026)** con el NRC 10044 (202656, X06, ESEC 00684):
  - la regla en **`SOAATRK`** (Desplegar clase, unidad Presente/Ausente, Control de asistencia, del 07-SEP al 31-OCT-2026) hace que el NRC aparezca en **Pasar lista**; sin ella, la lista sale vacía;
  - **Captura de calificaciones › Libro de calificaciones › Componentes** registra las notas (85 de 100 → 17);
  - con asistencia de 43 %, `ATTRGRD` («Debe aprobar», `AST_70`) deja la nota compuesta en **INH**, y **SFASLST** muestra INH sin escribir nada en «Calificaciones finales».
- **Envío al libro validado (C119, 26/10/2026):** con el paso 6 (**Clase › «Actualizar la asistencia en el libro de calificaciones» › Sí**), `ATTRGRD` toma el porcentaje de Pasar lista: 57,14 → INH y 85,71 → APRO, con razón «Faltas Inasistencia - CA». **No pasa solo:** si el docente no lo envía, `ATTRGRD` se queda con el último valor enviado. La configuración de TI (`GORICCR` en Y, `GORRSQL` activa, `STVGCHG` con CA; C104) funciona. Resuelve U32.
- **Notas:** Ingresar calificaciones › Captura de calificaciones del docente › Libro de calificaciones › Componentes (C119).
- **Antes (C89):** sin la regla de SOAATRK, Faculty Grading daba error y la lista de asistencia no mostraba NRC.

La ruta administrativa de búsqueda está en [ref-busqueda-asistencia-banner.md](ref-busqueda-asistencia-banner.md). No alterar reglas existentes ni guardar cambios sin confirmar el periodo y el NRC.
