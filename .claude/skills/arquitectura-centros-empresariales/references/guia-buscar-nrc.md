# Guía: Cómo buscar y consultar un NRC creado en Banner (SSASECQ)

Esta guía documenta el procedimiento oficial paso a paso para localizar cualquier NRC (Número de Referencia de Curso) ya creado en el sistema cuando no se recuerda su número de 5 dígitos (o 4 dígitos en TEST).

## 1. Acceso a la pantalla de consulta
* **Página:** **SSASECQ (Consulta de Sección de Horario)**.
* Se accede escribiendo `SSASECQ` en el buscador general de Banner (arriba a la izquierda) o desde el menú relacionado de `SSASECT`.

---

## 2. Bloque de Filtros (Filtro Básico)

Al ingresar, el bloque **«CONSULTA DE SECCIÓN DE HORARIO»** muestra las opciones de búsqueda:

1. **Periodo:** Ingresar el periodo académico correspondiente (ej. `202656`).
2. **Agregar campos de búsqueda:**
   Por defecto, la pantalla suele mostrar solo *Periodo*, *Parte de periodo*, *Inscripción de/a* y *NRC*.
   Para filtrar por curso específico, se debe usar el desplegable:
   * Ubicar la casilla gris: **«Agregar otro campo...»** (con la flecha `v` hacia abajo).
   * Hacer clic y seleccionar los campos necesarios:
     * **`Materia`**: Se agrega la casilla. Ingresar el código (ej. `ESEC` o `ESEP`).
     * **`Curso`**: Se agrega la casilla. Ingresar el código numérico (ej. `00650`).
     * **`Sección`**: Se agrega la casilla. Ingresar la letra (ej. `B`).
3. **Ejecutar la consulta:**
   * Hacer clic en el botón azul **«Ir»** (ubicado a la derecha, debajo del bloque de filtros, al lado de «Limpiar todo»).

---

## 3. Lectura de Resultados en la Tabla

La tabla inferior muestra los NRC que coinciden con los filtros aplicados:

* **Columnas principales:**
  * **Periodo:** (ej. `202656`).
  * **Parte de periodo:** Identifica el grupo mensual (ej. `X07` para Computación, `I08` para Idiomas).
  * **NRC:** El número único generado por Banner (en TEST se han visto correlativos como `1015`, `1016`, `1017`, `1021`).
  * **Materia:** (ej. `ESEC`).
  * **Curso:** (ej. `00650`).
  * **Sección:** (ej. `B`).
  * **Título:** (ej. *Ofimática Word 365*).
* **Navegación:**
  * Si hay muchos registros, usar el paginador inferior (*«Registro 1 de 21»*, *«1 de 3 páginas»*).
  * Desplazar la barra horizontal para ver las columnas de la derecha (cupos, estado, horario).

---

## 4. Retorno a SSASECT para edición o verificación
Una vez identificado el número de NRC:
1. Ir a **SSASECT (Programar NRC)**.
2. Ingresar el **Periodo** (`202656`) y el **NRC** encontrado.
3. Presionar el botón azul **«Ir»** para acceder a la configuración completa del curso (horarios, cupos, aulas y docentes).
