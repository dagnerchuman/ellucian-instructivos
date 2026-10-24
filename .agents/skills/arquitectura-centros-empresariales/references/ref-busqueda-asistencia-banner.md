# Buscar la configuración de asistencia con perfil administrativo

## Estado observado en TEST
- Antes del 23/10, **Faculty Grading** daba error y la lista de asistencia salía sin secciones (C89). **Causa encontrada:** faltaba la regla de control de asistencia en **`SOAATRK`**. Con la regla del NRC 10044, el NRC aparece en **Pasar lista** y en el **Libro de calificaciones** (C101, C102).
- La **Banner Search Card** con perfil **Super Role Admin** sigue sirviendo para revisar la configuración.

## Términos documentados para buscar
Buscar uno por uno en la tarjeta **Banner Search Card**:

### Si `SHAGCOM` muestra «Debe configurar los controles del libro de calificaciones»
1. Busca y abre **`SHAEGBC`**. Este error se refiere al calendario de ingreso de calificaciones, no a la regla de asistencia del NRC.
2. En `SHAEGBC`, ingresa primero el **periodo** y pulsa **Ir**. Luego define la **fecha abierta** y la **fecha de corte** para el ingreso docente de calificaciones; guarda. Las fechas deben ser las que autorice la institución: no inventarlas. *(instructivo 7.1.4 Ingresar calificaciones a través de Autoservicio, diap. 40–41)*
3. Después regresa a `SHAGCOM` e ingresa periodo y NRC para asignar el plan de evaluación. El calendario `SHAEGBC` del periodo es un prerrequisito de `SHAGCOM`. *(instructivo 7.1.4, diap. 43)*
4. Para que la asistencia se transfiera al libro, el componente `ATTRGRD` se configura aparte en `SHAGCOM`; el instructivo indica que el docente envía la asistencia al libro de calificaciones y que no es necesario hacerlo cada sesión, idealmente al final del curso. *(instructivo 7.1.0 Usar Componente Asistencia, diap. 30)*

### Si estás configurando el control diario de un NRC
1. **`SOAATMT`** — reglas de control de asistencia para un NRC y sus sesiones. En el encabezado se ingresan periodo y NRC; luego se revisa la regla correspondiente a cada sesión. *(instructivo 7.1.1 Gestionar la asistencia a clases, diap. 40–42)*
2. **`SOAATRK`** — reglas de control de asistencia a nivel de periodo, parte de periodo, curso o NRC. *(instructivo 7.1.1, diap. 34–38)*
3. **`ENTERATTEND`** — proceso cuyo acceso debe estar habilitado para el perfil docente en Autoservicio; buscarlo para revisar el acceso, no como pantalla de pase de lista. *(instructivo 7.1.1, diap. 14–15)*

También se pueden probar las frases **“Control de asistencia”**, **“Attendance Tracking”** y **“Gestionar la asistencia a clases”**. Son términos derivados de los títulos del instructivo; no está confirmado que el buscador de este ambiente los resuelva.

## Límite
Los términos identifican configuraciones diferentes: `SHAEGBC` es calendario de ingreso de calificaciones; `SOAATMT`/`SOAATRK` son reglas de control de asistencia; `ENTERATTEND` es acceso al proceso de Autoservicio. Encontrar una página no demuestra que el registro diario esté habilitado ni que un NRC aparezca en Faculty. Buscar sin guardar cambios; antes de editar fechas o reglas, confirmar el periodo, NRC y los valores aprobados por la institución.

La ruta Faculty descrita por Ellucian sí documenta **Ingreso de asistencia → NRC/sesión → Pasar lista → marcar presentes/ausentes** *(instructivo 10.4.2.4.5, diap. 16; 7.1.1, diap. 44–48)*, y en TEST funciona una vez creada la regla en `SOAATRK` (C101). En la USS la opción se llama **Control de asistencia › Lista de cursos › Pasar lista**.
