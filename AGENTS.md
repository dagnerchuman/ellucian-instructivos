# Instrucciones para agentes (Antigravity, Claude Code u otros)

## El proyecto
- **Usuario:** Dagner Anibal Chuman Lluen, de los **Centros Empresariales** de la Universidad Señor de Sipán (USS): Idiomas/Inglés, Computación/Informática y Emprendimiento.
- **Qué hace:** documenta y prueba cómo pasan del sistema actual **SEUSS** a **Ellucian Banner Student**.
- **Este repositorio:** instructivos de Ellucian (PPTX, carpetas `CAPACIDAD n`) y un visor web (`visor_instructivos/`, que Netlify publica con `publish = "."`).
- **Idioma:** responde **en español**, simple y directo.

## Antes de responder, lee la memoria del proyecto
Está en `.claude/skills/`. Son archivos Markdown y cualquier agente puede leerlos.

1. `.claude/skills/arquitectura-centros-empresariales/SKILL.md`: modelo, periodos, flujo, reglas de trabajo. Referencias en `references/`:
   - `guia-crear-nrc.md`: crear un NRC en SSASECT campo por campo, con lo visto en TEST;
   - `reglas-ellucian.md`: qué dice Ellucian, con cita del instructivo y la diapositiva;
   - `periodos-y-cronograma.md`, `flujo-de-inicio-a-fin.md`, `paginas-banner.md`, `migracion-r2.md`, `glosario.md` y `mapa-instructivos.md`.
2. `.claude/skills/preguntas-y-dudas-centros/registro.md`: lo **confirmado** (C##), lo **resuelto** con los instructivos (R##), las **dudas abiertas** para Ellucian (E##) y para la USS (U##), y los supuestos descartados (S##). **Mantenlo actualizado.** El método para procesar notas de reuniones está en su `SKILL.md`.
3. `.claude/skills/documentos-uss/SKILL.md`: preferencias del usuario y cómo generar PDF, PPTX y Excel con formato USS.
   - `scripts/pdf/`: pipeline HTML → Chromium; el ejemplo de referencia es `ejemplo_centros.py`.
   - `scripts/pptx/`: piezas para presentaciones con la plantilla USS.
   - `fuentes/`: generadores de todos los entregables hechos.
   - `references/entregables.md`: lista de los entregables.

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
