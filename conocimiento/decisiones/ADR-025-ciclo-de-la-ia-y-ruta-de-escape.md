---
id: ADR-025
titulo: Todo archivo se abre y se evalúa antes de entregarlo, y todo dato lleva su fuente o un «No lo sé»
estado: aceptado
fecha: 2026-10-29
fuentes: [C155, C146, C151]
temas: [agentes, memoria, entregables]
---
# ADR-025 · Ciclo de la IA y ruta de escape

## Contexto
El 28/10 se publicaron en el sitio pasos de SCACRSE con datos dichos con seguridad pero errados: periodo 202656 en vez de 000000 y créditos fijos en vez de variables (C146). También se dieron pasos para crear el NRC 10045 con menos campos que la guía del proyecto (C151). El usuario enseñó dos reglas para el agente (C155):
- el **ciclo de la IA**: generar el archivo, evaluarlo (fórmulas y datos), corregir si falla, y abrir y verificar todo lo creado;
- la **ruta de escape**: responder solo con base en las fuentes, citar la sección exacta y decir «No lo sé» cuando el dato no está.

## Decisión
- Hay dos skills **transversales**, `ciclo-de-la-ia` y `ruta-de-escape`. Se aplican en todo pedido, junto a la skill principal de la tabla de enrutamiento (ADR-024).
- **Ciclo de la IA:** un archivo está terminado cuando se abrió y se evaluó (datos contra la fuente, fórmulas recalculadas, vista revisada) y pasó. Si falla, se corrige la fuente, se regenera y se vuelve a evaluar.
- **Ruta de escape:** cada dato lleva su cita (C##, instructivo y diapositiva, ADR, archivo y sección, o sección del documento del usuario). Si no hay fuente, se dice «No lo sé», dónde se buscó y cómo averiguarlo. Si el usuario pide «solo con base en este documento», solo vale ese documento.

## Alternativas descartadas
- **Meterlas en `workflow-entregables-uss` o `preguntas-y-dudas-centros`:** valen para cualquier archivo y cualquier respuesta, no solo para entregables o para el registro.
- **Contarlas como skill principal en la tabla:** ADR-024 pide una principal por pedido; estas no buscan el dato ni generan el archivo, solo deciden cuándo algo está listo y qué se puede afirmar.

## Consecuencias
- Las respuestas citan más y dicen «No lo sé» más seguido, sin rellenar con valores plausibles.
- Cada entrega toma un paso más (abrir y evaluar), y a cambio no se publican archivos sin revisar.

## Criterio de salida
Que el usuario cambie el método, o que una de las dos reglas choque con otra decisión aceptada.

## Relacionado
- [ADR-024](ADR-024-enrutamiento-de-skills.md) · [ADR-018](ADR-018-base-de-conocimiento.md)
- Skills `ciclo-de-la-ia` y `ruta-de-escape`
