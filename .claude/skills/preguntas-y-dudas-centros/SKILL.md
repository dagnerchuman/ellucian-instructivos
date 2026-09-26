---
name: preguntas-y-dudas-centros
description: Registro vivo de preguntas, dudas y decisiones del proyecto Centros Empresariales USS en Ellucian Banner, con el método para procesar notas de reuniones o Zoom. Úsala cuando el usuario mande notas, fotos de apuntes o capturas de una reunión, traiga respuestas de Ellucian o de la USS, pida preparar preguntas, o diga «rectificar», «confirmar», «ver si permite» o «cómo es el proceso». Mantén actualizado registro.md.
---

# Preguntas y dudas: Centros Empresariales

El registro está en [registro.md](registro.md) y es la memoria del proyecto:
- lo que el usuario confirmó;
- lo que se resolvió con los instructivos;
- lo que sigue abierto, para Ellucian o para la USS.

**Léelo antes de responder** sobre cualquier tema del proyecto. **Actualízalo** cada vez que algo cambie.

## Cómo procesar notas de una reunión o del Zoom
Las notas suelen llegar como fotos de apuntes a mano, sin texto.
1. **Transcribe** cada línea tal cual y clasifícala:
   - **Dato**: algo que se hace hoy.
   - **Verificar**: dicen «rectificar» o «confirmar».
   - **Pregunta**: dicen «ver si permite» o «cómo es».
2. **Separa las fuentes:**
   - Las notas del usuario describen lo que se hace **hoy en SEUSS**.
   - La respuesta se busca en los instructivos (**En Ellucian**) con `arquitectura-centros-empresariales/scripts/buscar_instructivos.py`, citando instructivo y diapositiva.
3. **Responde con ejemplos concretos por centro**: Inglés, Informática y Emprendimiento. Usa grupos reales del cronograma (I04, X03, P02…) y marca como «de ejemplo» todo dato inventado.
4. **Si los instructivos no lo dicen**, es una **duda**:
   - Dale un ID nuevo en el registro (E## para Ellucian, U## para la USS).
   - Anota la fecha y de dónde salió.
5. **En el entregable, pon todas las dudas al final**, separadas en «Para Ellucian» y «Para la USS». El usuario lo pidió así el 26/09/2026.
6. **Actualiza registro.md:**
   - Mueve lo confirmado a «Confirmado por el usuario» o a «Resuelto con los instructivos», con la fecha.
   - Si cambia un supuesto, lista los entregables que hay que corregir.

## Cuando llega una respuesta
- **Del usuario o de la USS:** pasa la duda a «Confirmado» con la fecha y la fuente (quién lo dijo y en qué reunión). Revisa qué entregables usan el supuesto anterior y ofrece corregirlos.
- **De Ellucian:** igual, y anota si contradice un instructivo.
- **Si el usuario dice que no sabe algo:** no lo uses como hecho. Pásalo a «Supuestos descartados» o déjalo como duda. Ejemplo: el «periodo de 3 meses».

## Estilo de las preguntas
- Una pregunta = una decisión. Cortas, con el dato concreto (minutos, grupo, página).
- Indica a qué ejemplo o página remite, por ejemplo «(ver ejemplos I-2 y X-3)».
- Ordénalas por impacto: primero lo que bloquea la configuración (periodos, horas, CAPP) y después los detalles.
