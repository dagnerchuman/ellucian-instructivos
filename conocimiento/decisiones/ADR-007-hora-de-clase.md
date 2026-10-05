---
id: ADR-007
titulo: La hora de clase es de 45 minutos de día y 50 de noche
estado: aceptado
fecha: 2026-09-26
fuentes: [C05, S02, R07, E01, U09]
temas: [horas, carga]
---
# ADR-007 · La hora de clase es de 45 minutos de día y 50 de noche

## Contexto
En una nota se escribió «40–45 minutos» (S02). El usuario lo corrigió: 45 minutos de día y 50 de noche, y las dos cuentan como 1 hora. Existe además una hora presencial de 60 minutos (C05). En Banner, SIATERM tiene **un solo** factor de duración por periodo (R07).

## Decisión
Se documenta la hora de clase como **45 min (día) / 50 min (noche) = 1 hora**, siempre con los minutos al lado. El nombre de cada hora (pedagógica o cronológica) queda por confirmar (U09).

## Alternativas descartadas
- **40–45 minutos (S02):** corregido por el usuario.

## Consecuencias
- Hasta que Ellucian responda E01, la carga en SIAASGN puede no reflejar la diferencia entre día y noche.

## Criterio de salida
La respuesta de Ellucian a E01 (cómo configurar dos duraciones) o la de la USS a U09.

## Relacionado
- [ADR-011](ADR-011-carga-lectiva.md)
