# Guía Oficial: Auditoría y Cumplimiento Curricular CAPP (SMARQCM, SMICRLT, GJAPCTL)

Esta guía documenta el procedimiento probado y validado en el ambiente **TEST de la USS** (29/09/2026) y basado en el **Instructivo 7.2.4 (Diapositivas 30 a 55)** para auditar el cumplimiento de la malla curricular de los estudiantes de Centros Empresariales (Idiomas, Computación y Emprendimiento), permitiendo que en el Autoservicio el alumno visualice qué asignaturas tiene pendientes y cuáles ya aprobó.

---

## 1. FASE 1: Auditoría Individual de Malla

Permite auditar el avance curricular de un estudiante específico en tiempo real.

### Paso 1: Apertura de Solicitud en SMARQCM
* **Página:** **SMARQCM (Solicitud de Cumplimiento de Grado)**.
* **Encabezado (Bloque Clave):**
  * **ID:** Ingresar el ID del alumno (ej. `100582059` o `S00581081`).
  * **Tipo de Solicitud (*Request Type*):** Ingresar `+` (para crear una solicitud nueva).
  * **Periodo (*Term*):** Ingresar el periodo activo (ej. `202656`).
  * **Modo:** Seleccionar `ONLINE`.
  * Presionar el botón azul **«Ir»** (arriba a la derecha).

### Paso 2: Extracción del Currículo del Alumno
* En la barra de menú superior, hacer clic en **`Herramientas` (*Tools*)** $\rightarrow$ **`Copiar del Registro del Alumno` (*Copy from Student Record*)**.
* El sistema hereda automáticamente la estructura curricular activa desde `SGASTDN`:
  * **Programa:** `CMEMC38` (o el programa del centro correspondiente).
  * **Major (Especialidad):** `ACXP` (Acreditación en Computación).
  * **Nivel:** `C` (Computación) / `I` (Idiomas) / `M` (Emprendimiento).
  * **Sede:** `S` (Sipán).
  * **Escuela:** `EM` (o la escuela respectiva).
* Presionar **«Guardar»** (`F10` o botón abajo a la derecha). El sistema confirma: `*1 row saved*`.

### Paso 3: Compilación del Motor CAPP
* En la barra de menú superior, hacer clic en **`Herramientas` (*Tools*)** $\rightarrow$ **`Enviar para Procesamiento` (*Submit for Processing*)**.
* El motor CAPP compila las reglas curriculares y genera el número correlativo de auditoría (*Request Number*).

### Paso 4: Consulta de Resultados en SMICRLT
* En el menú **`Relacionado` (*Related*)**, hacer clic en **`Resultados de Cumplimiento` (*Compliance Results*)** o digitar directamente **`SMICRLT`** con el número de solicitud asignado.
* **Resultado:** Muestra el reporte al 0% de avance (para ingresantes), listando las asignaturas obligatorias pendientes (ej. `ESEC 00650`) y los créditos requeridos para certificar.

---

## 2. FASE 2: Auditoría Masiva por Lotes (Proceso Batch)

Permite correr el compilador CAPP para toda una cohorte o población de estudiantes matriculados en los centros.

### Paso 1: Invocación del Proceso en GJAPCTL
* **Página:** **GJAPCTL (Control de Procesos)**.
* **Encabezado:**
  * **Proceso:** **`SMRBCMP`** (*Compliance Batch Process*).
  * **Conjunto de Parámetros:** Dejar en blanco / Default.
  * Presionar el botón azul **«Ir»**.

### Paso 2: Configuración de Salida (Bloque Impresora)
* **Impresora (*Printer*):** Ingresar **`DATABASE`** (para almacenar la salida en el repositorio del sistema).
* **Secuencia de Ejecución (*Run Sequence*):** Dejar en blanco.
* Presionar botón «Sección siguiente» (`Page Down`).

### Paso 3: Configuración de Parámetros de Población
| Parámetro | Valor Estándar | Significado Operativo |
|---|---|---|
| **Par 01** | `202656` | Periodo lectivo evaluado |
| **Par 02** | `P` | Selección por Población |
| **Par 03 - 06** | `GLISLST` | Regla de población institucional |
| **Par 07** | `S` | Origen de datos: Estudiante (*Student*) |
| **Par 08 - 20** | `N` | Banderas (*flags*) de formato estándar |

### Paso 4: Despacho a Cola de Procesamiento
* Marcar la opción **«Submit»** y hacer clic en **«Guardar»** (`F10`).
* El sistema encola el trabajo y emite el identificador de ejecución (*Job Number*, archivo `smrbcmp_xxxxxx.lis`).

### Paso 5: Verificación de Bitácora en GJIREVO
* Ingresar a **`GJIREVO`** (*Revisar Salida de Proceso*).
* Consultar el archivo `.lis` correspondiente al Job Number emitido.
* **Resultado:** La bitácora certifica que el lote de estudiantes fue evaluado con éxito sin errores de sintaxis en las reglas CAPP.
