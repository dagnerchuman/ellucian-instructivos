# Instrucciones para agentes (Antigravity, Claude Code u otros)

## El proyecto
- **Usuario:** Dagner Anibal Chuman Lluen, de los **Centros Empresariales** de la Universidad Señor de Sipán (USS): Idiomas/Inglés, Computación/Informática y Emprendimiento.
- **Qué hace:** documenta y prueba cómo pasan del sistema actual **SEUSS** a **Ellucian Banner Student**.
- **Este repositorio:** instructivos de Ellucian (PPTX, carpetas `CAPACIDAD n`) y un visor web (`visor_instructivos/`, que Netlify publica con `publish = "."`).
- **Idioma:** responde **en español**, simple y directo.

## Antes de responder, lee la memoria del proyecto
Está en `.agents/skills/` (y sincronizada en `.claude/skills/`). Son archivos Markdown y cualquier agente puede leerlos.

1. `.claude/skills/arquitectura-centros-empresariales/SKILL.md`: modelo, periodos, flujo, reglas de trabajo. Referencias en `references/`:
   - Guías operativas paso a paso (según pestañas): `01-creacion-nrc.md`, `02-creacion-de-persona.md`, `03-admision-y-asignacion-al-programa.md`, `04-matricula-en-el-nrc.md`, `05-notas-asigna-docente.md`;
   - Apoyos y consultas: `ref-busqueda-nrc.md`, `ref-admision-capp.md`, `ref-autoservicio-matricula.md`;
   - Documentos de marco: `00-flujo-de-inicio-a-fin.md`, `ref-periodos-y-cronograma.md`, `ref-reglas-ellucian.md`, `ref-paginas-banner.md`, `ref-glosario.md`, `ref-mapa-instructivos.md`, `ref-migracion-r2.md`.
2. `.claude/skills/preguntas-y-dudas-centros/registro.md`: lo **confirmado** (C##), lo **resuelto** con los instructivos (R##), las **dudas abiertas** para Ellucian (E##) y para la USS (U##), y los supuestos descartados (S##). **Mantenlo actualizado.** El método para procesar notas de reuniones está en su `SKILL.md`.
3. `.claude/skills/documentos-uss/SKILL.md`: preferencias del usuario y cómo generar PDF, PPTX y Excel con formato USS.
   - `scripts/pdf/`: pipeline HTML → Chromium; el ejemplo de referencia es `ejemplo_centros.py`.
   - `scripts/pptx/`: piezas para presentaciones con la plantilla USS.
   - `fuentes/`: generadores de todos los entregables hechos.
   - `references/entregables.md`: lista de los entregables.
4. `.claude/skills/workflow-consultas-banner/SKILL.md`: resolver dudas de pantallas Banner (SSASECT, SOATERM, etc.) con citas de instructivos.
5. `.claude/skills/workflow-entregables-uss/SKILL.md`: pipeline y control de calidad de entregables PDF, PPTX y Excel.
6. `.claude/skills/workflow-procesar-reunion/SKILL.md`: procesar notas y minutas de Zoom/reuniones y actualizar registro.md.
7. `.claude/skills/workflow-pruebas-test/SKILL.md`: guía y checklist para pruebas integrales en Banner TEST.

## Buscar evidencia en los instructivos
```bash
python3 .claude/skills/arquitectura-centros-empresariales/scripts/buscar_instructivos.py "texto o regex" [--archivo 5.3] [--max 10]
python3 .claude/skills/arquitectura-centros-empresariales/scripts/buscar_instructivos.py --diapositiva "5.3_4.1.4.1.6" 23
```
Cita así: «instructivo 5.3, diap. 23».

## Reglas clave
- **Fuentes:**
  - «**Hoy en SEUSS**» es lo que dice el usuario; no lo interpretes.
  - «**En Ellucian**» es lo que dicen los instructivos, con cita.
  - Todo lo demás es una **duda**: va al registro.
- **No inventes datos de la USS** (códigos de campus, escuelas, programas, nombres de cursos). Si usas un dato ilustrativo, márcalo «de ejemplo».
- **Siglas y códigos**, siempre con su significado entre paréntesis: «NRC (Número de Referencia de Curso)», «SSASECT (Programar NRC)».
- **En los documentos:**
  - pocas tablas;
  - ejemplos de los **tres centros**;
  - estructura «Hoy en SEUSS / En Ellucian / Resultado»;
  - **todas las dudas al final**;
  - autor «Elaborado por: Dagner Anibal Chuman Lluen».
- **Periodos:** año + 5 + secuencia (1 verano, 4 semestre I, 6 semestre II). SEUSS 2026-0 / I / II equivale a 202651 / 202654 / 202656.
- **Inglés:** en SEUSS, quien desaprueba BASIC I no pasa a BASIC II, salvo con examen de suficiencia. Banner lo reproduce con el prerrequisito en «Fatal».
- **No uses** «periodo de 3 meses» para SEUSS: el usuario no lo confirmó.
- **Git:** no publiques en `main` sin que el usuario lo pida.
