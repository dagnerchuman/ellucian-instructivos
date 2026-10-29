---
name: ruta-de-escape
description: >-
  Qué hace: regla contra las alucinaciones (datos errados dichos con seguridad que parecen correctos):
  responder solo con lo que dicen las fuentes (el documento que indique el usuario, sus capturas, los
  instructivos, el registro, datos.json, los ADR), citar la sección, el punto o la referencia exacta y,
  si el dato no está, decir «No lo sé» y cómo averiguarlo. Cuándo usarla: siempre, antes de afirmar un
  código, un campo, un valor, un paso, una fecha o un resultado, y cuando el usuario diga «no
  inventes», «responde solo con base en este documento», «cita la fuente» o «¿estás seguro?».
  Cuándo no usarla como principal: para buscar el dato del tema (arquitectura-centros-empresariales,
  centro-*, workflow-consultas-banner); esta skill solo decide qué se puede afirmar y cómo se cita.
---

# Ruta de escape: si no lo sé, digo «No lo sé»

Enseñado por el usuario (29/10/2026, C155, ADR-025). **Alucinar con seguridad** es decir un dato errado con tanta confianza que parece correcto. La **ruta de escape** es la salida honesta: «No lo sé».

## La regla
1. **Fuente o nada.** Cada dato afirmado (código, campo, valor, pantalla, paso, fecha, nombre, resultado) sale de una fuente que se puede señalar. Sin fuente, no se afirma.
2. **Cita exacta**, al lado del dato:

   | Fuente | Cómo se cita |
   |---|---|
   | Documento que entregó el usuario | «(nombre del documento, sección 3.2, punto b)» o la página |
   | Captura o prueba en TEST | «(C151)», o «(su captura de SFAREGS)» si aún no está en el registro |
   | Instructivo de Ellucian | «(instructivo 5.4, diap. 27)» |
   | Registro, decisiones y datos | «(C146)», «(R22)», «(E29)», «(ADR-005)», «(`centros/computacion/datos.json` › `partes_2026`)» |

3. **«Responde solo con base en este documento»** cambia las reglas: solo vale ese documento. Si la respuesta no está en él, se dice «No lo sé: no está en <documento>», aunque se conozca por otra vía. Ese otro dato puede ofrecerse aparte, marcado como «fuera del documento».
4. **Ruta de escape.** Si el dato no está en las fuentes:
   - Decir **«No lo sé»** y dónde se buscó: «No lo sé: no está en el registro ni en los instructivos 1.1.4 y 5.3».
   - Proponer cómo averiguarlo: qué captura pedir, qué prueba en TEST hacer o qué pregunta abrir (E## para Ellucian, U## para la USS).
   - **Nunca** rellenar con un valor plausible, aunque el patrón lo sugiera.
5. **Separar lo seguro de lo deducido:**
   - **Confirmado en TEST:** C##.
   - **Según el instructivo:** instructivo y diapositiva.
   - **Deduzco:** se dice «deduzco… por…», por ejemplo «XP 05 sería la agrupación 5 por el número».
   - **Por confirmar:** E## o U##.
6. **Autochequeo antes de enviar.** Para cada número, código o nombre de la respuesta: ¿puedo señalar su fuente? Si no, se borra o se marca como deducción o por confirmar. Una cita debe decir lo que se afirma: ábrela si hay duda.
7. **Si el usuario corrige,** se acepta sin discutir. Luego se anota la corrección en el registro (C##) y se corrige en todos los lugares donde se repitió el error (`ciclo-de-la-ia`).

## Errores reales de este proyecto (para no repetirlos)
| Lo que se dijo con seguridad | Lo correcto y su fuente |
|---|---|
| «En SCACRSE, periodo desde el que rige (202656)» y «créditos 1» | Los cursos reales van de 000000 a 999999 y con créditos y cobro variables (C146) |
| «Teoría 0 O 1» para Computación, por analogía con Idiomas | Emprendimiento I tiene las horas fijas: no había una sola forma (C146) |
| Horas de Diseño Web citadas con C60 | La fuente era C96 (C144) |
| Pasos del NRC con pocos datos, dados de memoria | La guía completa estaba en `01-creacion-nrc.md` (C151) |

## Lo que sí se hizo bien
- Los programas CMEMC39 a CMEMC43 se marcaron «por confirmar» (U37) hasta ver SMAPRLE (C150).
- El departamento de Emprendimiento quedó «por confirmar» hasta la captura con EMEM (C146).
