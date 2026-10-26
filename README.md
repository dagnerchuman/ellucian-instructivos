# Instructivos Ellucian · Centros Empresariales USS

Documentación y pruebas del paso de **SEUSS** a **Ellucian Banner Student** en los Centros Empresariales de la Universidad Señor de Sipán: **Idiomas** (Inglés), **Computación** (Informática) y **Emprendimiento**.

- **Sitio:** https://centros-empresariales-ellucian.vercel.app (se publica desde la rama `main`).
- **Elaborado por:** Dagner Anibal Chuman Lluen.

## Mapa del repositorio

| Carpeta | Qué hay | Regla |
|---|---|---|
| `CAPACIDAD 1/` … `CAPACIDAD 11/` | Instructivos de Ellucian (PPTX) y scripts de prueba de la USS | No se mueven ni se renombran: el visor depende de sus rutas ([ADR-015](conocimiento/decisiones/ADR-015-visor-y-rutas.md)) |
| `visor_instructivos/` | El sitio: visor de instructivos con las diapositivas como imágenes (`diapositivas/`) | Las imágenes se generan con `herramientas/diapositivas.py` ([ADR-022](conocimiento/decisiones/ADR-022-instructivos-como-imagenes.md)) |
| `centros/` | Lo propio de cada centro en `idiomas/`, `computacion/` y `emprendimiento/`: `datos.json` (fuente única), ficha `README.md` y `diagramas/`. Lo común, en `comun/` | Los diagramas no se editan a mano: se cambia `datos.json` o la plantilla y se regenera ([ADR-003](conocimiento/decisiones/ADR-003-diagramas-generados.md)) |
| `conocimiento/` | Base de conocimiento: `manifest.json` (qué existe), `decisiones/` (los ADR) y auditorías. Se abre en Obsidian | Un ADR aceptado es una restricción ([ADR-018](conocimiento/decisiones/ADR-018-base-de-conocimiento.md)) |
| `herramientas/` | Solo código que genera o revisa: diagramas (Archify), diapositivas, validador, espejo de skills y el piloto de video | Los datos de entrada no van aquí: van en `docs/fuentes/` |
| `docs/` | Entregables y documentos, por tipo: `dudas/`, `afiches/`, `capacitacion/`, `arquitectura/`, `presentaciones/`, `fuentes/` y `propuesta-usuarios-finales/` | Índice en [`docs/README.md`](docs/README.md) |
| `.claude/skills/` y `.agents/skills/` | Memoria de los agentes (Claude Code y Antigravity). El registro de dudas está en `preguntas-y-dudas-centros/registro.md` | Se editan en `.claude/skills/` y se copian con `python3 herramientas/sincronizar_skills.py --desde claude` ([ADR-014](conocimiento/decisiones/ADR-014-skills-espejo.md)) |

**En la raíz** solo quedan las instrucciones (`README.md`, `CLAUDE.md` para Claude Code, `AGENTS.md` para otros agentes), la publicación del sitio (`index.html`, que redirige al visor; `_redirects` y `netlify.toml`, de cuando se publicaba en Netlify) y `skills-lock.json` (skills de video instaladas en `.agents/skills`). Detalle en [ADR-023](conocimiento/decisiones/ADR-023-estructura-del-repositorio.md).

## Cómo fluye la información

```
Reuniones, chats y pruebas en TEST
        │
        ▼
registro.md (C## confirmado · R## resuelto · E## / U## dudas) ──► conocimiento/decisiones (ADR)
        │
        ▼
centros/<centro>/datos.json ──► herramientas/diagramas/generar.py ──► centros/<centro>/diagramas (HTML, PNG, SVG)
        │                                                        └──► Asistente IA (base local)
        ▼
.claude/skills/documentos-uss/fuentes ──► docs/ (PDF, Word, PPTX)
```

## Dónde va algo nuevo

| Si es… | Va en… |
|---|---|
| Un dato de un centro (programa, curso, NRC, escala) | `centros/<centro>/datos.json`, y luego se regeneran los diagramas |
| Algo que confirmó el usuario, Ellucian o la USS | El registro (`C##`) y, si se eligió entre alternativas, un ADR |
| Una duda nueva | El registro (`E##` para Ellucian, `U##` para la USS) |
| Un PDF, Word o PPTX para entregar | `docs/<tipo>/`, con su generador en `.claude/skills/documentos-uss/fuentes/` |
| Un Excel o CSV descargado que sirve de fuente | `docs/fuentes/` |
| Un script que genera o revisa algo | `herramientas/` |

## Comandos

```bash
bash herramientas/diagramas/instalar_archify.sh   # una vez por máquina
python3 herramientas/diagramas/generar.py          # diagramas, galería y base del asistente
python3 herramientas/validar_conocimiento.py       # debe quedar con 0 errores
python3 herramientas/sincronizar_skills.py --check # .claude/skills y .agents/skills iguales
```
