# Guía Oficial: Cómo Generar una Persona desde Cero en Banner (GOAMTCH)

Esta guía documenta el procedimiento probado y validado en el ambiente **TEST de la USS** (29/09/2026) para registrar a una persona natural nueva y generar su ID oficial de Banner.

---

## 1. Acceso a la página
* **Página:** **GOAMTCH (Captura de Coincidencia Común)**.
* También se abre automáticamente cuando estás en **SPAIDEN** o **SAAQUIK** y haces clic en el botón **`+`** (Insertar persona nueva en el campo ID).

---

## 2. Bloque Clave (Encabezado)
1. **ID:** Mantener el valor automático **`GENERATED`**.
2. **Origen de coincidencia:** Presionar `•••` y seleccionar:  
   👉 **`PERS_NATU`** (*Persona Natural*).
3. Presionar el botón azul **«Ir»** (arriba a la derecha).

---

## 3. Formulario de Captura de Datos (Campos Obligatorios y Recomendados)

| Campo | Valor / Ejemplo | Nota importante |
|---|---|---|
| **Apellido** | `APELLIDO1 / APELLIDO2` | Separar ambos apellidos con una barra `/` |
| **Nombre** | `NOMBRE UNO` | Primer nombre |
| **Segundo nombre** | `NOMBRE DOS` | Opcional |
| **Tipo de dirección** | `PP` (*Dirección principal*) | **OBLIGATORIO** para que Banner no rechace el guardado |
| **Calle línea 1** | `Av. Principal 123` | **OBLIGATORIO** si se define tipo de dirección |
| **País** | `PE` (*Perú*) | Código de país |
| **NSS/NIT** | `88776655` | DNI de la persona (8 dígitos) |
| **Fecha de nacimiento** | Día `06`, Mes `03`, Año `2000` | **El año debe tener 4 dígitos (YYYY)** |
| **Género** | `M` (*Male*) o `F` (*Female*) | Seleccionar de la lista con `•••` |
| **Tipo de teléfono** | `MOV` (*Teléfono Móvil*) | Recomendado |
| **Teléfono** | `999` `999` `999` | 3 bloques de números |
| **Tipo de correo-e** | `PER1` (*Correo Personal 1*) | Recomendado |
| **Correo electrónico** | `correo@gmail.com` | Dirección de correo válida |

---

## 4. Proceso de Validación y Guardado (3 clics obligatorios)

1. **Clic 1:** Presionar el botón con borde azul **«Marcar-Duplicar»** *(columna izquierda)*.  
   *Banner analiza la base de datos para confirmar que no exista otra persona con el mismo DNI o nombres.*
2. **Clic 2:** Presionar el botón **«Crear nuevo»** *(se habilitará en la columna derecha)*.  
   *Confirma que se registrará un consecutivo completamente nuevo.*
3. **Clic 3:** Presionar el botón azul **«GUARDAR»** *(abajo a la derecha)*.

---

## 5. Resultado Exitoso
Banner emitirá el mensaje en verde en la esquina superior derecha:
> *«ID generado: **S########** (ej. `S00581081`). Creó registro de identificación. Registro biográfico creado; Registro de dirección creado; Registro de teléfono creado; Registro de correo electrónico creado.»*

**Estructura del ID en la USS:** Prefijo **`S`** seguido de 8 dígitos correlativos (ej. `S00581081`).
