---
name: workflow-pruebas-test
description: >-
  Qué hace: guía, casos de prueba y checklist para ejecutar pruebas integrales en Banner TEST
  (experience-test.elluciancloud.com/ussipantest): NRC, admisión, matrícula, asistencia, notas, pase
  a historia y casuísticas de docentes, quejas y sanciones, y cómo operar TEST con el navegador
  (references/manejo-banner-test.md). Cuándo usarla: el usuario va a entrar a TEST, pide «los pasos
  de lo que tenemos que validar», un checklist, el orden de una prueba de punta a punta o «hazlo tú
  en TEST con el navegador», o documentar una prueba con capturas para el sitio. Cuándo no usarla:
  explicar un campo o un error de una pantalla
  (workflow-consultas-banner) ni datos ya validados de un centro (centro-*).
---

# Workflow: Pruebas Integrales en Banner TEST

Este workflow guía y audita la ejecución de pruebas en el ambiente **TEST de Ellucian Banner** (`experience-test.elluciancloud.com/ussipantest`).

> **Plan de Pruebas Integrales V7.0 (USS y Ellucian):** qué pruebas hay (A a H), cuáles pasaron y cuáles faltan, y la parte de los Centros Empresariales (H28 a H38), en [references/plan-pruebas-integrales-v7.md](references/plan-pruebas-integrales-v7.md). El usuario dice qué paso toca; no se ejecuta por cuenta propia (C201).

> **Pruebas preparadas, por hacer cuando el usuario lo diga:** atributos de curso con STVATTR, SCADETL y SMAAREA ([references/prueba-atributos-stvattr.md](references/prueba-atributos-stvattr.md), C208) y turnos de inscripción con SFARCTT, SFARCTL, SFARGRP y SFRGRUP ([references/prueba-turnos-inscripcion.md](references/prueba-turnos-inscripcion.md), C209) y la evaluación docente con la encuesta TESS, desde la configuración hasta los resultados ([references/prueba-evaluacion-docente-tess.md](references/prueba-evaluacion-docente-tess.md), C211). Solo lo que le toca a la jefatura de los centros.

> **Si el agente opera TEST con el navegador** (Claude, Antigravity u otro): primero lee [references/manejo-banner-test.md](references/manejo-banner-test.md). Ahí están el reparto «el agente deja escrito, el usuario guarda», cómo moverse entre bloques, las incidencias (C169) y el índice de recetas. Cada receta está en `references/recetas/`, un archivo por tema (matrícula, mallas, NRC, notas y cierre, encuesta docente): abre solo el del tema que vas a probar.

## Mapa de la skill: abre solo el archivo que necesitas

| Si necesitas… | Abre |
|---|---|
| Checklist A a D (catálogo, NRC, admisión, enseñanza y cierre), casuísticas complejas y scripts oficiales de los centros | [references/checklist-pruebas-basicas.md](references/checklist-pruebas-basicas.md) |
| Carga masiva de alumnos de un contrato (ADR-020) | [references/prueba-carga-por-contrato.md](references/prueba-carga-por-contrato.md) |
| Restricción por programa (SSARRES) y acreditación como prerrequisito, prueba del 29/10 | [references/prueba-restriccion-por-programa.md](references/prueba-restriccion-por-programa.md) |
| Llevar las capturas de una prueba al sitio (cuadros morados, números verdes, flujo de Archify) | [references/documentar-prueba-con-capturas.md](references/documentar-prueba-con-capturas.md) |

## 1. Alcance de Pruebas de los Centros
- **Periodos activos:** 202651 (verano), 202654 (semestre I), 202656 (semestre II).
- **Entidades:** Participantes regulares y de pregrado (que subsanan requisitos de egreso).
- **Centros:** Idiomas (Inglés), Computación (Informática) y Emprendimiento.
