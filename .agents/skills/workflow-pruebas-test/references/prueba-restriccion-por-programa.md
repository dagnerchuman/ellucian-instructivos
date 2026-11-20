# Prueba de restricción por programa y acreditación como prerrequisito (29/10/2026)

Parte de la skill `workflow-pruebas-test` (el mapa está en su `SKILL.md`).

## 6. Restricción por programa y acreditación como prerrequisito (29/10/2026)
Guía completa: [ref-restricciones-y-prerrequisitos-por-programa.md](../../arquitectura-centros-empresariales/references/ref-restricciones-y-prerrequisitos-por-programa.md).
- [x] **SSARRES › Incluir programa** bloquea con «Program Restriction» (Error fatal) a quien no lo tiene, **solo si** SOATERM tiene Programa en Fatal (C149, C156).
- [x] El **currículo de pregrado** también cuenta para la restricción de programa, con los dos currículos en el mismo plan (C157, E29).
- [x] **SCAPPRQ** bloquea la matrícula con «Prerequisite and Test Score error» (Error fatal) a quien no cumple (NRC 10020, C163).
- [x] La parte de Idiomas **sola** bloquea: `ESEC 00044` con solo `ESEP 02456` en SCAPPRQ 202644; Arnold rechazado en el NRC 10022 (C165). En SCAPPRQ guarda el usuario; Claude deja escrito.
- [x] Borrar las dos filas temporales de SCAPPRQ 202644 (`ESEC 00044` y `ESEP 02456`) y hacer la prueba de control: sin la fila, Arnold se inscribe en el 10022 (C167). En 202744 no hay DD en SFARSTS: el 10022 quedó con RE.
- [x] Basic «en curso» en un periodo de centros: Arnold con 10042 y 10043 en 202656; en el 10022 de 202744 sale «Prerequisite In Progress» (Error fatal), porque «En progreso» está sin marcar en SOATERM 202744 (C166, R10).
- [x] Caso positivo: con Basic I en la historia, el alumno de Nidia se inscribe; la matrícula usa la versión de SCAPPRQ de su catálogo (C170, E32).
- [ ] Copiar la regla de Nidia de la versión 202444 a 202544 y 202644 (C170).
- **Antes de empezar:** SFARSTS de la parte del NRC (C154); SOADEST con DATABASE si SFAREGS lo pide; no recargar la página con una fila en error (C158).
