---
name: workflow-procesar-reunion
description: Procedimiento para procesar apuntes de reuniones, minutas, notas manuscritas, transcripciones de Zoom o aclaraciones de Dagner sobre Centros Empresariales. Actualiza registro.md con trazabilidad completa (C##, R##, E##, U##, S##) y evalúa impacto en entregables.
---

# Workflow: Procesamiento de Notas de Reuniones y Zoom

Este workflow procesa toda información nueva proveniente de reuniones con el equipo de la USS, sesiones de Zoom con Ellucian o apuntes personales del usuario.

## 1. Entrada típica
- Fotos de libretas o notas a mano tomadas durante el Zoom.
- Transcripciones de audio o mensajes de chat con novedades de la migración.
- Nuevas políticas académicas o aclaraciones de procesos operativos de los Centros.

## 2. Pasos de ejecución

### Paso 1: Transcripción y Clasificación
Transcribir cada punto de la nota tal cual fue expresado y clasificarlo en:
- **[Dato]**: Práctica real actual contada por el usuario o equipo USS.
- **[Verificar]**: Puntos donde dijeron «confirmar», «rectificar» o «revisar».
- **[Pregunta / Duda]**: Puntos con «ver si permite», «cómo se hace en Banner» o incertidumbre.

### Paso 2: Separación Estricta de Fuentes
- **«Hoy en SEUSS»**: Lo que el usuario o la USS declara que se hace actualmente. No reinterpretarlo ni asumir reglas no dichas.
- **«En Ellucian»**: Contrastar cada punto buscando evidencia en los 83 instructivos PPTX mediante:
  ```bash
  python3 .claude/skills/arquitectura-centros-empresariales/scripts/buscar_instructivos.py "termino_clave"
  ```
- Si Ellucian lo resuelve: Citar instructivo y diapositiva exacta.
- Si no está en los instructivos: Se cataloga como duda abierta.

### Paso 3: Análisis de Casos por Centro
Generar ejemplos concretos para los 3 centros obligatoriamente:
- **Idiomas (Inglés)**: Periodo general IGE, partes I01..I12, cursos BASIC I..III, INTERMEDIATE I..III.
- **Computación (Informática)**: Periodo CGE, partes X01..X07, cursos ofimática/específicos.
- **Emprendimiento**: Periodo EGE, partes P01..P06, cursos de planes de negocio/proyectos.

### Paso 4: Actualización Atómica de `registro.md`
Actualizar directamente `.claude/skills/preguntas-y-dudas-centros/registro.md`:
1. **Confirmado por el usuario (C##)**: Asignar nuevo ID correlativo si el usuario valida un hecho.
2. **Resuelto con los instructivos (R##)**: Si el instructivo explica cómo opera Banner.
3. **Dudas abiertas para Ellucian (E##)**: Preguntas técnicas de configuración o comportamiento de Banner no documentadas.
4. **Dudas abiertas para la USS (U##)**: Decisiones de política interna de la USS (puntajes mínimos, quién aprueba sobrepasos, quién carga notas, etc.).
5. **Supuestos descartados (S##)**: Mover aquí cualquier supuesto previo que haya resultado falso o no confirmado (ej. «periodo de 3 meses»).

### Paso 5: Matriz de Impacto en Entregables
Consultar `.claude/skills/documentos-uss/references/entregables.md`:
- Si un supuesto cambió (ej. de 40-45 min a 45 min), listar los entregables afectados.
- Alertar al usuario sobre los documentos que requieren regeneración.

## Base de conocimiento
- Una decisión con alternativas descartadas va también como ADR en `conocimiento/decisiones/`.
- Antes de anotar, revisa si contradice un ADR aceptado; si es así, pregunta al usuario.
- Al final ejecuta `python3 herramientas/validar_conocimiento.py`.
