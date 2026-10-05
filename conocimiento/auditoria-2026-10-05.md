# Auditoría del 05/10/2026

Al escribir los 18 ADR y correr el validador por primera vez aparecieron documentos desactualizados y reglas que contradecían decisiones vigentes. Aquí queda qué se encontró y qué se hizo.

## Corregido

| # | Qué se encontró | Arreglo |
|---|---|---|
| 1 | La skill `arquitectura-centros-empresariales` enlazaba `references/mapa-instructivos.md`, que se renombró a `ref-mapa-instructivos.md` | Enlace corregido |
| 2 | `01-creacion-nrc.md` enlazaba `guia-buscar-nrc.md`, que hoy es `ref-busqueda-nrc.md` | Enlace corregido |
| 3 | Idiomas y Emprendimiento tenían una duda con id «TEST» en `datos.json`, que no existía en el registro | Nueva duda **U25** |
| 4 | U06 («¿quién matricula?») seguía abierta, aunque C46 ya la responde en parte | Marcada «en parte» con C46 y [ADR-010](decisiones/ADR-010-usuarios-y-poblacion.md) |
| 5 | U08 («¿qué aprueba Jefatura?») seguía abierta, aunque C47 ya la responde en parte | Marcada «en parte» con C47 y [ADR-011](decisiones/ADR-011-carga-lectiva.md) |
| 6 | U18 preguntaba qué es la escuela EM, aunque C23 ya la nombra «Centros Empresariales» | U18 cita C23 |
| 7 | La regla de Antigravity decía «Computación: ESEC/ESEP», pero ESEP es de la escuela CE y no está confirmado (U18) | Regla corregida |
| 8 | El `_leeme` de las casuísticas en los `datos.json` hablaba de los diagramas 6 y 7, que ya no existen desde el rediseño (C49) | Texto actualizado |
| 9 | `centros/comun/datos.json` decía «actualizado 2026-10-03» | Fecha actualizada |

## Pendiente de decidir

| # | Qué se encontró | Qué falta |
|---|---|---|
| 10 | **Contradicción:** en el flujo del usuario (C06) la carga lectiva es de Registros Académicos; el 05/10 se confirmó que la asigna el jefe y la aprueba el Vicerrectorado (C47, C48) | Duda **U26** para la USS |
| 11 | Las entradas C15 a C23 del registro citan guías con nombres viejos: `guia-crear-nrc.md`, `guia-crear-persona.md`, `guia-admision-saaquik.md`, `guia-matricula-sfaregs.md`, `guia-autoservicio-matricula.md` y `guia-buscar-nrc.md`. Hoy son `01-creacion-nrc.md`, `02-creacion-de-persona.md`, `03-admision-y-asignacion-al-programa.md`, `04-matricula-en-el-nrc.md`, `ref-autoservicio-matricula.md` y `ref-busqueda-nrc.md` | Son entradas históricas: se dejan como están y esta tabla sirve de equivalencia |
| 12 | Las skills todavía usan sinónimos que [ADR-004](decisiones/ADR-004-glosario-unico.md) desaconseja: «participante» (19 veces en 11 archivos), «inscripción» (53 en 17), «cierre de actas» (6 en 4) y «vacante» (7 en 4) | Cambiarlos poco a poco, cuando se edite cada skill. Los mensajes de Banner se citan tal cual |
