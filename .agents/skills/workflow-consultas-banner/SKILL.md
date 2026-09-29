---
name: workflow-consultas-banner
description: Guía de ejecución y workflow para resolver consultas de pantallas de Ellucian Banner Student (SSASECT, SOATERM, SFAREGS, SIAINST, SIAASGN, SMAAREA, etc.), capturas de pantalla del usuario o dudas de "qué pongo aquí". Usa los 83 instructivos oficiales del repositorio.
---

# Workflow: Consultas y Soporte en Vivo de Pantallas Banner

Este workflow se activa cuando el usuario envía una captura de pantalla, pregunta qué valor ingresar en un campo específico de Banner o necesita el procedimiento exacto para una transacción en el ambiente TEST o PRODUCCIÓN.

## 1. Entrada típica
- Capturas de pantalla con recuadros o dudas: «¿qué pongo aquí?», «¿qué significa este error?».
- Dudas de parametrización en páginas como SSASECT, SOATERM, SFAREGS, SIAINST, SCACRSE, etc.

## 2. Pasos de resolución
1. **Identificar la página y el bloque:**
   - Detectar el código de 7 letras de Banner (ej. SSASECT, SOATERM, SIAINST).
   - Identificar en qué pestaña o bloque se encuentra el cursor.

2. **Búsqueda inmediata de evidencia en instructivos:**
   - Ejecutar la búsqueda en los 83 PPTX usando el script indexador:
     ```bash
     python3 .claude/skills/arquitectura-centros-empresariales/scripts/buscar_instructivos.py "término exacto o página"
     ```
   - Si se conoce el instructivo (ej. 5.3 para SSASECT):
     ```bash
     python3 .claude/skills/arquitectura-centros-empresariales/scripts/buscar_instructivos.py --archivo 5.3 "nombre del campo"
     ```
   - Ver la diapositiva completa de referencia:
     ```bash
     python3 .claude/skills/arquitectura-centros-empresariales/scripts/buscar_instructivos.py --diapositiva "5.3_4.1.4.1.6" <num_diapositiva>
     ```

3. **Estructura de respuesta obligatoria:**
   - **Respuesta corta y directa**, campo por campo, en el orden exacto en que aparecen en la pantalla.
   - **Cita formal:** «instructivo X.X [Nombre], diap. YY».
   - **Manejo de códigos USS:**
     - Si el código es conocido (ej. periodo 202656, partes I01..I12, X01..X07, P01..P06), dar el código exacto.
     - Si el código específico de la USS no está confirmado (ej. campus, códigos internos de escuela EM vs CE): **NO INVENTAR**. Indicar cómo buscarlo presionando el botón «•••» de la pantalla.
     - Si hay una duda abierta en `registro.md` relacionada con este campo (ej. U09 sobre horas, U17 sobre campus), alertar al usuario.

4. **Verificación de dependencias previas:**
   - Recordar siempre qué debe existir antes de llenar esa pantalla (ej. para crear un NRC en SSASECT, el curso debe existir en SCACRSE y la parte de periodo en SOATERM).
