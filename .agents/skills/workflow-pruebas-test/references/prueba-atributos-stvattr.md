# Prueba de atributos de curso (STVATTR) para los centros

Preparada el 19/11/2026 a pedido del usuario: «anda viendo lo de atributos STVATTR para poder hacer una prueba nada más» (C207, C208). Es **una sola prueba**, en el alcance de la jefatura de los centros: no se tocan cosas de Registros Académicos ni de Admisión sin su visto bueno. **No se guarda nada en TEST sin que el usuario lo pida** (sección 1 de `manejo-banner-test.md`).

## Qué es un atributo de curso

Un código de 4 caracteres que marca cursos que comparten algo («electivo», «taller»). La malla puede pedir «N cursos con el atributo X» **sin listar curso por curso** en la regla, y el CAPP cuenta cualquier curso que lo tenga (instructivo 1.2.2, diap. 5 y 22).

| Paso | Página | Qué se hace | Lámina |
|---|---|---|---|
| 1 | **STVATTR** | Crear el código (4 caracteres) y su descripción (hasta 30) | 1.2.2, diap. 11; 6.1.2, diap. 9 |
| 2 | **SCADETL** › pestaña «Atributos de grado» | Materia, curso y periodo desde el que rige; insertar el atributo y guardar | 6.1.2, diap. 20 y 21; 1.2.2, diap. 14 |
| 3 | **SMAAREA** › regla del área › Detalles | En la condición, columna «Atributo de curso» (sin materia ni curso) | 1.2.2, diap. 18 a 21 |
| 4 | **SMARQCM** › SMICRLT | Correr el CAPP de un alumno y ver si la regla se cumple con el curso que tiene el atributo | 7.2.4, diap. 30 a 41 |

El NRC creado después hereda los atributos del catálogo en SSADETL (5.3, diap. 37).

**No confundir:** el **atributo de curso** (STVATTR, columna «Atributo de curso» de SMAAREA) no es el **atributo de alumno** (columna «Atributo de alumno» de la misma regla, y el parámetro 07 de SFRGRUP o la regla de SFAMHRS). Esta prueba es solo del de curso.

## Lo que ya hay en TEST (20/11/2026, solo consulta, C218)

El usuario: «enlazamos los atributos con los cursos y Finanzas enlaza ese mismo atributo, pero con el código de detalle de pago… solo revisa». Se revisó sin guardar nada.

- **STVATTR ya tiene códigos de los centros** (65 en total): `COM1` a `COM3` (Computación plan antiguo y rutas), `C011` a `C074` (Computación I a IV), `ING1` «Basic I-II / Intermedio I-II» a `ING6`, `NIV1` a `NIV4` «Nivel n Centros Empresariales», `EEMP`, `EMPR`, `EL01` a `EL03`, `E001` a `E003`, `EXLA` a `EXLI`, entre otros. **No hace falta crear uno** para la prueba: se elige uno de estos.
- **SCADETL › Atributos de grado** (periodo 000000): `ESEP 02456` Basic I tiene **`ING1`**. `ESEC 00684` Diseño Web y el taller `ESEC 00697` **no tienen atributo**.
- **SCADETL › Códigos de cuota:** vacíos en Basic I y en Diseño Web. Los `X032` (S/ 420) y `X228` (S/ 80) de Basic I que se vieron en C68 ya no están.
- **SSADETL del NRC 10001** (Basic I, 202754): cuotas de sección vacías; el atributo de la sección es **`C011` «Computación I»**, no `ING1` como el curso. Parece puesto a mano: hay que avisar a quien lo creó.
- **SFARGFE, tipo de regla `ATTR`, captura Regular:** **ninguna regla** en 202754, 202656 ni 202744 (pregrado). En 202754 tampoco hay reglas por Nivel ni por Campus. No se revisó la captura «Precobrar».

**Conclusión:** en TEST, Finanzas **todavía no** enlaza los atributos con un código de cargo, y de los cursos revisados solo Basic I tiene su atributo. El código que Finanzas pondría en SFARGFE es de **cargo** (como `X032`), no de pago (`M001`…): instructivo 11.1.1, diap. 74 a 80.

## Caso propuesto: la regla `ECOM-04` de la malla `MC42-01` (XP 05)

Encaja con lo que quedó pendiente en C174: `ECOM-04` «Computación IV» debía cambiar `ESEC 00682` por los **talleres `00696` a `00700`**. En vez de poner los 5 talleres uno por uno, se marca cada taller con un atributo y la regla pide el atributo.

1. **Antes (solo consulta):** abrir STVATTR y buscar si ya hay un código de taller o de los centros. Anotar los existentes; no inventar uno si ya hay. Revisar en SCADETL › «Atributos de grado» de `ESEC 00696` qué atributos tiene.
2. **STVATTR:** si no existe, crear un código de 4 caracteres (nombre por decidir con el usuario, p. ej. `TCOM` «Taller de Computación»).
3. **SCADETL:** para **un** taller (p. ej. `ESEC 00696`), periodo desde 000000 o desde el que rija la malla, insertar el atributo y guardar.
4. **SMAAREA `MC42-01`** (versión 202454) › `ECOM-04`: agregar una condición con «Atributo de curso» = el código nuevo. Dejar la fila `00682` hasta ver el resultado, o quitarla si el usuario lo decide.
5. **CAPP:** SMARQCM de un alumno de XP 05 que tenga ese taller en historia o en curso («Usar cursos en progreso»), y revisar en SMICRLT que `ECOM-04` se cumple con el taller.

**Resultado esperado:** el taller con el atributo cuenta en `ECOM-04` sin estar listado en la regla. Si sale «no cumplido», revisar el periodo desde el que rige el atributo en SCADETL y el catálogo con que se evaluó (SMICRLT, 7.1.9 diap. 64).

**Para deshacer:** quitar la condición de `ECOM-04`, quitar el atributo del curso en SCADETL. El código de STVATTR puede quedar (otros podrían usarlo); borrarlo solo si nadie lo usa.

## Preguntas abiertas (para el usuario)

- ¿Quién crea códigos en **STVATTR**? Es una tabla de validación de toda la institución; lo más probable es que sea Registros Académicos (los cursos los crea Registros, C147). Si la jefatura no tiene permiso, la prueba se limita a consultar y a la regla de SMAAREA con un atributo que ya exista.
- ¿Qué código y descripción usar?
- ¿Con qué alumno de XP 05 se corre el CAPP?
