# Consulta de asistencia por docente, curso y sesión

## Componente de asistencia en el libro de calificaciones
- En el plan de evaluación de cada NRC, configurar el componente de asistencia con el nombre obligatorio **`ATTRGRD`** desde **SHAGCOM (Plan de evaluación del NRC)**. *(instructivo 7.1.4 Ingresar calificaciones a través de Autoservicio, diap. 55)*
- El componente lleva peso **0.00**, la casilla **Debe Pasar** y una escala propia de asistencia. La nota aprobatoria de esa escala debe corresponder al porcentaje mínimo de asistencia requerido para aprobar el curso. *(instructivos 7.1.0 Usar Componente Asistencia, diap. 29; 7.1.4, diap. 55)*
- En Computación, el mínimo confirmado es **70 % de asistencia** (C63); se mantiene separado de la nota mínima aprobatoria **11** del modo vigesimal `V` (ADR-009).
- `ATTRGRD` es la configuración del componente dentro del libro de calificaciones; no es el nombre de la opción que abre el control diario de asistencia.
- En el NRC `10026` de Computación (periodo `202656`), el usuario confirma que completó y validó en TEST el flujo `SHAEGBC` → `SHAGCOM` (C95). La fila `ATTRGRD` usa peso `0.00`, **Debe aprobar** y escala propia de asistencia correspondiente al `70 %`, distinta de `VIG_11`, que se mantiene como escala regular.
- En el bloque superior de SHAGCOM, «Escala de calificación» es la escala **que predominará** en los componentes; cada componente puede usar otra, por ejemplo la de asistencia. *(7.1.4, diap. 44 y 49)* En el NRC `10044` quedó `AST_70` arriba, aunque cuatro de los cinco componentes usan `VIG_11` (C98).
- El Autoservicio docente solo lista los NRC que el docente tiene asignados, **con plan de evaluación y con alumnos inscritos**. *(7.1.4, diap. 58 y 63)*

## Docente: ingresar y revisar la asistencia diaria
- Desde la página de inicio de **Faculty (Autoservicio Docente)**, el menú ofrece **Control de asistencia del docente**. *(instructivo 10.4.2.4.5 Configuración de Autoservicio, diap. 12)*
- En los enlaces de autoservicio de Facultad, la opción aparece como **Ingreso de asistencia**. *(instructivo 10.4.2.4.5, diap. 16)*
- El docente debe tener habilitado el proceso **ENTERATTEND** en el Autoservicio. El acceso por relación requiere que sea docente de una sección (NRC) en la que el alumno esté inscrito; no es obligatorio que sea el docente principal. Si la regla exige acceso de principal, sí debe tener ese indicador en **SSASECT**. *(instructivo 7.1.1 Gestionar la asistencia a clases, diap. 14 y 15)*
- El control se organiza por NRC y sesión de clase. *(instructivo 7.1.1, diap. 8)*

## Si no aparece el NRC, la sesión o la opción
- El periodo debe tener fechas de acceso docente en Autoservicio configuradas en **SOATERM**. *(instructivo 7.1.1, diap. 12)*
- Debe existir una regla de control activa para la sesión del NRC, con **Desplegar clase** y **Control de asistencia** activos, unidad de control y fechas de inicio/fin configuradas; se repite por cada sesión. *(instructivo 7.1.1, diap. 42)*
- El proceso **ENTERATTEND** debe estar disponible para el perfil docente en Autoservicio. La regla de acceso puede requerir relación docente-alumno o que el docente sea principal. *(instructivo 7.1.1, diap. 14 y 15)*
- Estos requisitos y la secuencia de la interfaz están documentados, pero **la ejecución del registro todavía debe probarse en el ambiente TEST de la USS**. No afirmar que ya fue probada ni que el NRC 10020 está habilitado para asistencia.
- `ATTRGRD` configura cómo la asistencia interviene en la calificación; no es el control diario. Solo incluirlo si preguntan por la configuración de calificaciones o por el componente de asistencia.
