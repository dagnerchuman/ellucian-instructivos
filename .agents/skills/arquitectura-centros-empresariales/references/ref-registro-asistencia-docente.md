# Registrar asistencia como docente

## Acceso y pasos
1. En el portal **Faculty (Autoservicio Docente)**, abre **Ingreso de asistencia**. *(instructivo 10.4.2.4.5 Configuración de Autoservicio, diap. 16)*
2. Busca el **NRC** y la sesión de clase correspondiente; pulsa **Pasar lista**. *(instructivo 7.1.1 Gestionar la asistencia a clases, diap. 44)*
3. En la lista, marca a cada alumno para la fecha seleccionada: **✓ verde** = presente y **− rojo** = ausente. Solo se permiten fechas pasadas, no futuras. *(instructivo 7.1.1, diap. 45–46)*
4. Banner calcula el porcentaje de asistencia mientras se registran las marcas. *(instructivo 7.1.1, diap. 47)*
5. **Actualizar todo** permite marcar masivamente registros vacíos o a todos como presentes/ausentes. No usar estas opciones sin revisar a quién se aplicará cada marca. *(instructivo 7.1.1, diap. 48)*

## Requisitos si algo no aparece
- El docente debe tener disponible el proceso `ENTERATTEND` en Autoservicio. El acceso puede depender de la relación docente-alumno o de que sea instructor principal en `SSASECT`. *(instructivo 7.1.1, diap. 14–15)*
- El periodo debe tener configuradas en `SOATERM` las fechas de acceso docente a Autoservicio. *(instructivo 7.1.1, diap. 12)*
- La regla de asistencia de la sesión del NRC debe estar activa, con **Desplegar clase**, **Control de asistencia**, unidad de control y fechas de inicio/fin. Se configura por cada sesión. *(instructivo 7.1.1, diap. 42)*
- Si `SHAGCOM` muestra el error «Debe configurar los controles del libro de calificaciones en SHAEGBC», configura primero el calendario de calificaciones en **`SHAEGBC`**: periodo → **Ir** → fecha abierta y fecha de corte institucionales → guardar; luego regresa a `SHAGCOM`. *(instructivo 7.1.4, diap. 40–43)*

## Estado de validación
**Actualización 23/10/2026 (C101, C102):** con una regla en **`SOAATRK`** para el NRC 10044 (202656, X06, ESEC 00684; Desplegar clase, unidad Presente/Ausente, Control de asistencia, del 07-SEP al 31-OCT-2026), el NRC ya aparece en **Faculty › Control de asistencia › Lista de cursos › Pasar lista** y Banner calcula el porcentaje. **Captura de calificaciones › Libro de calificaciones › Componentes** también abre el NRC. Sin la regla de SOAATRK, la lista de asistencia sale vacía. **Envío a `ATTRGRD` (C103):** el 86 % de Pasar lista no apareció solo en el libro de calificaciones; `ATTRGRD` sigue con 1 calificación restante en Componentes. Según el instructivo 7.1.0, el docente envía el porcentaje y TI debe tener activos `GORICCR` (ATTENDANCE_TRACKING, ENABLE.GRADEBOOK.UPDATE), `GORRSQL` (ATTR_UPDATE_GRADEBOOK) y una razón con atributo CA en `STVGCHG` (U32). Lo que sigue es la observación anterior:

El instructivo documenta el procedimiento de Faculty, pero en la prueba actual de la USS la tarjeta **Faculty Grading** mostró error y **Ingreso de asistencia** abrió una lista sin NRC disponibles. Por tanto, no guiar al usuario a esa tarjeta como solución actualmente operativa ni afirmar que la asistencia está disponible para el NRC consultado.

La ruta administrativa de búsqueda y los términos validados para el estado actual de TEST están en [ref-busqueda-asistencia-banner.md](ref-busqueda-asistencia-banner.md). No alterar reglas existentes ni guardar cambios hasta confirmar que se está en el periodo/NRC correcto y entender el alcance.
