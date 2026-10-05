---
id: ADR-013
titulo: Las quejas se atenderían como solicitudes de servicio (SVASVPR)
estado: propuesto
fecha: 2026-10-05
fuentes: [R14, R15, C44, U14]
temas: [quejas, autoservicio]
---
# ADR-013 · Las quejas se atenderían como solicitudes de servicio (SVASVPR)

## Contexto
Hay casuísticas de alumnos que se quejan de un docente (C14). Los instructivos proponen hacerlo con solicitudes de servicio (R14), pero en TEST no existe un servicio de queja (C44).

## Decisión (propuesta)
La queja se registraría como **solicitud de servicio**: el alumno la crea en el Autoservicio y el área la atiende en SVASVPR. El mecanismo ya se validó con el servicio `CER` (Script 18-C).

## Alternativas descartadas
- **Crear la solicitud en SVASVPR:** Banner no lo permite («Función inválida»).

## Consecuencias
- La denuncia ante Gobierno de Personas no la genera Banner (R15).

## Criterio de salida
La respuesta de la USS a U14: si crea el servicio de queja en SVVSRVC o atiende las quejas fuera de Banner. Con esa respuesta, este ADR pasa a `aceptado` o a `descartado`.

## Relacionado
- Skill `workflow-pruebas-test`
