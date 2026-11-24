---
id: ADR-026
titulo: Desde 2027 el periodo de los centros es año + 2 + secuencia (202721)
estado: aceptado
fecha: 2026-11-24
fuentes: [C238]
temas: [periodos]
---
# ADR-026 · Desde 2027 el periodo de los centros es año + 2 + secuencia (202721)

## Contexto
[ADR-005](ADR-005-periodos.md) fijó para los centros el código año + 5 + secuencia (202651, 202654, 202656) y dejó como criterio de salida «que Registros Académicos defina otra codificación para 2027». Esos periodos fueron de TEST.

El 24/11/2026 el usuario, asignado a la Capacidad 01 para producción, dijo que producción empieza con **202721**, que es de Centros Empresariales, que los tres centros lo comparten y que lo crea Registros Académicos «como hasta ahora»; «41» es pregrado de verano (C238). En TEST, 202721 es «Verano 2027 - Cent.Empresarial», del 01-ENE-2027 al 31-MAR-2027.

## Decisión
- Desde 2027, el periodo de los centros es **año + 2 + secuencia**, y **1 es verano**: `202721`.
- Es un solo periodo para Idiomas, Computación y Emprendimiento; cada grupo es una parte de periodo ([ADR-006](ADR-006-partes-de-periodo.md)).
- Lo crea **Registros Académicos** (STVTERM y SOATERM). Las partes y sus fechas salen de las mallas de cada jefatura.
- El periodo de un grupo lo sigue decidiendo su **fecha de inicio**, no la de fin.

## Alternativas descartadas
- **Seguir con año + 5 (202751, 202754):** era la regla de TEST 2026. En TEST quedan esos códigos, pero no van a producción.

## Consecuencias
- Lo que el repositorio dice de 202651, 202654 y 202656 es de TEST.
- Falta confirmar el código del semestre I (en TEST está 202724 «2027-I Centro Empresariales», del 01-ABR-2027 al 31-JUL-2027) y el del semestre II (U56).
- Quién hace cada paso de la Capacidad 1 en producción, además del periodo, sigue abierto (U57).

## Criterio de salida
Que Registros Académicos cambie la codificación o separe el periodo por centro.

## Relacionado
- [ADR-005](ADR-005-periodos.md) (reemplazado) · [ADR-006](ADR-006-partes-de-periodo.md) · U56, U57 y U58 · E34 a E40
- Flujos: `centros/comun/diagramas/01-capacidad-1-periodo-202721/` y `centros/comun/diagramas/02-capacidad-1-ruta-despues-del-periodo/`
