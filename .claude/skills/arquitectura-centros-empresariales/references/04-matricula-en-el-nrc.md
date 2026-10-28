# Guía Oficial: Matrícula e Inscripción de Alumno en un NRC (SFAREGS)

Procedimiento oficial probado y validado en el ambiente **TEST de la USS** (29/09/2026) para inscribir a un estudiante en un NRC mediante backoffice en Banner.

> **Orden obligatorio de Banner:** conserva el orden de campos de cada pantalla y no adelantes datos dependientes. En el encabezado de SFAREGS, el periodo se ingresa primero, luego el ID del alumno y al final el plan de estudios.

---

## 1. Acceso a la página
* **Página:** **SFAREGS (Inscripción de Curso de Alumno)**.
* Se escribe `SFAREGS` en el buscador general de Banner (arriba a la izquierda).

---

## 2. Bloque Clave (Encabezado)
1. **Periodo:** Ingresar el periodo académico (ej. `202656`).
2. **ID:** Ingresar el ID oficial del estudiante (ej. `S00581081`).
3. **Plan de estudios, al final:** completar este campo después del periodo y del ID. Si se ingresa antes, puede aparecer un error como «no existe la tabla o vista» u otro error.
   - No asumir que el plan siempre es `1`; elegir el que corresponda al alumno y esté disponible.
4. Presionar el botón azul **«Ir»** (arriba a la derecha).

**Orden obligatorio del encabezado:** periodo → ID del alumno → plan de estudios. El periodo es el primer dato requerido.

---

## 3. Autorización del Plan de Estudios
1. En el bloque superior **«INFORMACIÓN DE INGRESO»**, verificar que el campo **Estatus** tenga **`EL`** (*Inscripción Autorizada*).
2. En el bloque del medio **«PLAN DE ESTUDIOS DE INGRESO»**:
   * En la columna **Plan de estudios:** ingresar el plan del alumno, el mismo del encabezado. No asumir `1`: en la prueba del 29/09 fue `1` y con el NRC 10044 fue `4` (C100).
   * En la columna **Estatus de ingreso:** ingresar **`EL`**.
3. **Paso crítico de confirmación:**  
   Hacer clic en el botón azul **«GUARDAR»** (abajo a la derecha) para autorizar este plan en el periodo.

---

## 4. Navegación a la Sección de Cursos (Atajo Clave)
1. Para pasar a la tabla de cursos sin bloqueos, hacer clic en el botón de **Sección siguiente**:  
   👉 **`⤓`** *(ubicado en la esquina inferior izquierda de la pantalla, o con el atajo de teclado `Option + Fn + Flecha Abajo` en Mac)*.
2. El cursor se posicionará automáticamente dentro de la casilla **`NRC`**.

---

## 5. Registro del NRC y Guardado Final
1. En la columna **`NRC`**, escribir el número del curso:  
   👉 **`1021`** *(o el NRC a inscribir)*.
2. Presionar la tecla **Tab** en el teclado.  
   *Banner autocompletará la Materia (`ESEC`), Curso (`00650`), Sección (`B`), Título y Horas crédito.*
3. Hacer clic en el botón azul **«GUARDAR»** (abajo a la derecha).

---

## Si sale «Las reglas del estatus de inscripción al curso no están definidas para la parte de periodo» (C154)
Falta **SFARSTS** para ese periodo y esa parte: ahí se habilitan RE y DD (y RW y DW para autoservicio) con fecha de inicio y fin, para **cada** parte de periodo de SOATERM (5.4, diap. 27–28). Lo configura Registros. Mientras tanto: pulsar ↺ (o «Limpiar registro») para quitar la fila y usar un NRC de una parte que sí esté configurada.

## 6. Resultado y Verificación
* El curso quedará registrado en la tabla con estatus **`RE`** o **`RW`** (*Registrado*).
* En **SSASECQ**, el NRC `1021` actualizará su cupo:
  * **Cupo Real:** sube de `0` a `1`.
  * **Cupo Restante:** baja de `2` a `1`.
