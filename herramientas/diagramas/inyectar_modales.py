"""Inyecta guías operativas interactivas directamente en el modal (Pasaporte semántico) de los diagramas Archify.

Al hacer clic sobre cualquier nodo del flujo en el navegador, el contenedor 
despliega la ficha operativa completa en Vista Dividida (Flujo BPM arriba + Guía abajo al 100% de ancho)
o en modo flotante/lateral, manteniendo siempre visible y responsivo el diagrama BPM.
"""
# ======================= BLOQUE 1: imports y constantes (reemplaza las 5 primeras líneas de import) =======================
import html
import json
import re
from pathlib import Path
from guias_operativas import obtener_guia, GUIAS_BASE, GUIAS_SCRIPTS
from plantillas import TITULOS, CAPACIDADES, guia_casuistica_de

# "plantillas": la guía de las casuísticas sale de plantillas.py (CASOS + EXTRA_CASOS) y pisa a GUIAS_SCRIPTS.
# "curada": manda GUIAS_SCRIPTS y solo se generan los nodos que le falten.
PRIORIDAD_CASUISTICAS = "plantillas"
SIN_GUIA_ESPERADO = ("tres-centros", "recorrido-completo")
ADVERTENCIAS = []

CENTROS_NAV = [
    ("idiomas", "Centro de Idiomas", "#8b5cf6"),
    ("computacion", "Centro de Computación", "#10b981"),
    ("emprendimiento", "Centro de Emprendimiento", "#f59e0b"),
    ("comun", "Los tres centros (común)", "#7030A0"),
]
RE_SCRIPT = re.compile(r"script-(\d{2}(?:-[a-z])?)-", re.I)
RE_PREFIJO = re.compile(r"^[a-z]+-\d{2}-")

CSS_MODAL = """
/* === DISEÑO RESPONSIVO Y GUÍA OPERATIVA (PASAPORTE SEMÁNTICO) === */

/* Modo Presentación: Ocultar barras de navegación y pie para pantalla completa limpia */
html[data-present="true"] .flow-nav-top,
html[data-present="true"] .flow-nav-bottom-section {
  display: none !important;
}

html[data-present="true"]:not([data-embed="true"]) body {
  padding: 0.25rem 0.75rem !important;
}

html[data-present="true"] .header {
  margin-bottom: 0.15rem !important;
  padding: 0 !important;
}

/* Asegurar que el botón de presentación de Archify muestre texto visible */
.toolbar #btn-present {
  display: inline-flex !important;
  align-items: center !important;
  gap: 0.35rem !important;
}

.toolbar #present-label {
  display: inline-block !important;
  font-size: 0.72rem !important;
}

/* --- 0. BARRAS DE NAVEGACIÓN Y PAGINACIÓN ENTRE FLUJOS --- */
/* CRÍTICO: Neutralizar la regla global `svg { min-width: min(900px, 100%); width: 100%; }` de Archify */
.flow-nav-top svg,
.flow-nav-bottom-section svg {
  width: 14px !important;
  height: 14px !important;
  min-width: 14px !important;
  max-width: 14px !important;
  display: inline-block !important;
  flex: 0 0 14px !important;
  transform: none !important;
  transition: none !important;
}

.flow-bottom-hub-btn svg {
  width: 16px !important;
  height: 16px !important;
  min-width: 16px !important;
  max-width: 16px !important;
  flex: 0 0 16px !important;
}

.flow-nav-top {
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  flex-wrap: wrap !important;
  gap: 0.45rem 0.85rem !important;
  width: 100% !important;
  box-sizing: border-box !important;
  padding: 0.32rem 0.85rem !important;
  margin: 0 0 0.35rem 0 !important;
  background: var(--toolbar-bg, rgba(15, 23, 42, 0.82)) !important;
  border: 1px solid var(--panel-border, #334155) !important;
  border-radius: 0.65rem !important;
  backdrop-filter: blur(12px) !important;
  -webkit-backdrop-filter: blur(12px) !important;
  font-family: system-ui, -apple-system, sans-serif !important;
  font-size: 0.8rem !important;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.18) !important;
  position: relative !important;
  z-index: 25 !important;
}

[data-theme="light"] .flow-nav-top {
  background: rgba(255, 255, 255, 0.94) !important;
  border-color: rgba(203, 213, 225, 0.85) !important;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05) !important;
}

.flow-nav-left {
  display: flex !important;
  align-items: center !important;
  flex-wrap: wrap !important;
  gap: 0.55rem !important;
  min-width: 0 !important;
  flex: 1 1 auto !important;
}

.flow-nav-right {
  display: flex !important;
  align-items: center !important;
  justify-content: flex-end !important;
  gap: 0.5rem !important;
  flex-shrink: 0 !important;
  margin-left: auto !important;
}

.btn-flow-centros {
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  gap: 0.45rem !important;
  padding: 0.36rem 0.78rem !important;
  border-radius: 0.5rem !important;
  background: var(--toolbar-bg, #1e293b) !important;
  color: var(--text, #fff) !important;
  border: 1px solid var(--panel-border, #334155) !important;
  font-weight: 600 !important;
  font-size: 0.8rem !important;
  line-height: 1.2 !important;
  text-decoration: none !important;
  transition: all 0.18s ease !important;
  cursor: pointer !important;
  white-space: nowrap !important;
  flex: 0 0 auto !important;
  width: auto !important;
}

.btn-flow-centros:hover {
  background: var(--toolbar-hover, #334155) !important;
  border-color: #a78bfa !important;
  color: #fff !important;
  transform: translateX(-2px) !important;
}

[data-theme="light"] .btn-flow-centros:hover {
  color: #0f172a !important;
}

.flow-nav-sep {
  color: var(--text-dim, #64748b) !important;
  opacity: 0.6 !important;
  font-size: 0.75rem !important;
  user-select: none !important;
  flex: 0 0 auto !important;
}

.flow-nav-center-tag {
  display: inline-flex !important;
  align-items: center !important;
  gap: 0.42rem !important;
  font-weight: 600 !important;
  color: var(--text, #fff) !important;
  padding: 0.28rem 0.65rem !important;
  border-radius: 0.45rem !important;
  background: rgba(148, 163, 184, 0.12) !important;
  font-size: 0.78rem !important;
  line-height: 1.2 !important;
  white-space: nowrap !important;
  flex: 0 0 auto !important;
}

.flow-center-dot {
  width: 8px !important;
  height: 8px !important;
  border-radius: 50% !important;
  display: inline-block !important;
  flex-shrink: 0 !important;
}

.flow-nav-select-wrap {
  position: relative !important;
  display: inline-flex !important;
  align-items: center !important;
  min-width: 220px !important;
  max-width: 440px !important;
  flex: 1 1 320px !important;
}

.flow-nav-select-wrap.flow-nav-select-center-wrap {
  min-width: 215px !important;
  max-width: 265px !important;
  flex: 0 1 240px !important;
}

.flow-nav-select {
  appearance: none !important;
  -webkit-appearance: none !important;
  background: var(--toolbar-bg, #1e293b) !important;
  color: var(--text, #fff) !important;
  border: 1px solid var(--panel-border, #334155) !important;
  border-radius: 0.5rem !important;
  padding: 0.38rem 1.85rem 0.38rem 0.75rem !important;
  font-size: 0.8rem !important;
  font-weight: 500 !important;
  line-height: 1.25 !important;
  cursor: pointer !important;
  outline: none !important;
  width: 100% !important;
  text-overflow: ellipsis !important;
  white-space: nowrap !important;
  overflow: hidden !important;
  transition: border-color 0.18s ease !important;
}

.flow-nav-select:hover,
.flow-nav-select:focus {
  border-color: #a78bfa !important;
}

.flow-nav-select.flow-nav-select-center {
  padding-left: 1.65rem !important;
  font-weight: 600 !important;
}

.flow-nav-select-arrow {
  position: absolute !important;
  right: 0.6rem !important;
  top: 50% !important;
  transform: translateY(-50%) !important;
  pointer-events: none !important;
  font-size: 0.75rem !important;
  color: var(--text-muted, #94a3b8) !important;
  line-height: 1 !important;
}

.flow-btn-top {
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  gap: 0.38rem !important;
  padding: 0.36rem 0.75rem !important;
  border-radius: 0.5rem !important;
  font-weight: 600 !important;
  font-size: 0.78rem !important;
  line-height: 1.2 !important;
  text-decoration: none !important;
  border: 1px solid var(--panel-border, #334155) !important;
  background: var(--toolbar-bg, #1e293b) !important;
  color: var(--text, #fff) !important;
  transition: all 0.18s ease !important;
  white-space: nowrap !important;
  flex: 0 0 auto !important;
  width: auto !important;
}

.flow-btn-top:hover:not(.disabled) {
  background: var(--toolbar-hover, #334155) !important;
  border-color: #a78bfa !important;
  transform: translateY(-1px) !important;
}

.flow-btn-top.primary {
  background: #7030A0 !important;
  border-color: #8b5cf6 !important;
  color: #fff !important;
}

.flow-btn-top.primary:hover:not(.disabled) {
  background: #5c2193 !important;
  box-shadow: 0 2px 10px rgba(112, 48, 160, 0.4) !important;
}

.flow-btn-top.disabled {
  opacity: 0.38 !important;
  cursor: not-allowed !important;
  pointer-events: none !important;
}

.flow-btn-top .flow-btn-num {
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  font-weight: 700 !important;
  font-size: 0.72rem !important;
  background: rgba(148, 163, 184, 0.22) !important;
  padding: 0.08rem 0.34rem !important;
  border-radius: 0.32rem !important;
  line-height: 1.1 !important;
  font-variant-numeric: tabular-nums !important;
}

.flow-btn-top.primary .flow-btn-num {
  background: rgba(255, 255, 255, 0.25) !important;
  color: #fff !important;
}

.flow-btn-top .flow-btn-txt {
  max-width: 240px !important;
  overflow: hidden !important;
  text-overflow: ellipsis !important;
  white-space: nowrap !important;
  font-weight: 500 !important;
  font-size: 0.76rem !important;
}

@media (max-width: 1250px) {
  .flow-btn-top .flow-btn-txt {
    max-width: 150px !important;
  }
}

@media (max-width: 950px) {
  .flow-btn-top .flow-btn-txt {
    display: none !important;
  }
}

.flow-nav-counter {
  font-size: 0.78rem !important;
  color: var(--text-muted, #94a3b8) !important;
  padding: 0 0.3rem !important;
  white-space: nowrap !important;
  flex: 0 0 auto !important;
}

.flow-nav-counter strong {
  color: var(--text, #fff) !important;
}

/* --- BOTTOM NAV CARDS --- */
.flow-nav-bottom-section {
  margin-top: 2rem !important;
  margin-bottom: 2.5rem !important;
  padding-top: 1.5rem !important;
  border-top: 1px dashed var(--panel-border, rgba(148, 163, 184, 0.2)) !important;
  font-family: system-ui, -apple-system, sans-serif !important;
}

.flow-bottom-container {
  display: grid !important;
  grid-template-columns: 1fr auto 1fr !important;
  gap: 1.25rem !important;
  align-items: stretch !important;
}

@media (max-width: 850px) {
  .flow-bottom-container {
    grid-template-columns: 1fr !important;
    gap: 0.85rem !important;
  }
}

.flow-bottom-card {
  display: flex !important;
  flex-direction: column !important;
  gap: 0.35rem !important;
  padding: 1rem 1.25rem !important;
  background: var(--panel, rgba(15, 23, 42, 0.6)) !important;
  border: 1px solid var(--panel-border, #1e293b) !important;
  border-radius: 0.85rem !important;
  text-decoration: none !important;
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
  color: var(--text, #fff) !important;
  min-height: 90px !important;
  justify-content: center !important;
}

.flow-bottom-card:hover:not(.placeholder) {
  border-color: #a78bfa !important;
  transform: translateY(-3px) !important;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3) !important;
}

.flow-bottom-card.primary-accent {
  background: linear-gradient(135deg, rgba(112, 48, 160, 0.18) 0%, rgba(15, 23, 42, 0.75) 100%) !important;
  border-color: rgba(139, 92, 246, 0.45) !important;
}

[data-theme="light"] .flow-bottom-card.primary-accent {
  background: linear-gradient(135deg, rgba(112, 48, 160, 0.08) 0%, rgba(255, 255, 255, 0.95) 100%) !important;
  border-color: rgba(112, 48, 160, 0.3) !important;
}

.flow-bottom-card.primary-accent:hover {
  border-color: #a78bfa !important;
  box-shadow: 0 8px 26px rgba(112, 48, 160, 0.35) !important;
}

.flow-bottom-card.placeholder {
  opacity: 0.45 !important;
  cursor: default !important;
  border-style: dashed !important;
}

.flow-card-badge {
  display: inline-flex !important;
  align-items: center !important;
  gap: 0.4rem !important;
  font-size: 0.72rem !important;
  font-weight: 700 !important;
  text-transform: uppercase !important;
  letter-spacing: 0.05em !important;
  color: #a78bfa !important;
}

.flow-bottom-card.prev .flow-card-badge {
  color: var(--text-muted, #94a3b8) !important;
}

.flow-card-num-title {
  display: flex !important;
  align-items: baseline !important;
  gap: 0.6rem !important;
}

.flow-card-num {
  font-family: "JetBrains Mono", monospace !important;
  font-weight: 800 !important;
  font-size: 1.15rem !important;
  color: #34d399 !important;
}

.flow-card-title {
  font-size: 0.95rem !important;
  font-weight: 700 !important;
  color: var(--text, #fff) !important;
  line-height: 1.3 !important;
}

.flow-card-title.muted {
  font-size: 0.85rem !important;
  font-weight: normal !important;
  color: var(--text-muted, #94a3b8) !important;
}

.flow-card-meta {
  font-size: 0.74rem !important;
  color: var(--text-muted, #94a3b8) !important;
}

.flow-bottom-hub-btn {
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  gap: 0.5rem !important;
  padding: 0.85rem 1.15rem !important;
  border-radius: 0.75rem !important;
  background: var(--toolbar-bg, #1e293b) !important;
  border: 1px solid var(--panel-border, #334155) !important;
  color: var(--text, #fff) !important;
  font-weight: 600 !important;
  font-size: 0.82rem !important;
  text-decoration: none !important;
  white-space: nowrap !important;
  height: 100% !important;
  box-sizing: border-box !important;
  transition: all 0.2s ease !important;
}

.flow-bottom-hub-btn:hover {
  background: var(--toolbar-hover, #334155) !important;
  border-color: #a78bfa !important;
  transform: translateY(-2px) !important;
}

/* Reducción global de espaciado para que todo entre ordenado en una sola pantalla */
body {
  padding: 0.45rem 1.15rem 1.25rem 1.15rem !important;
  --archify-page-top: 0.45rem !important;
}

body.has-guia-open {
  padding: 0.45rem 1.15rem 1.25rem 1.15rem !important;
  --archify-page-top: 0.45rem !important;
  overflow: hidden !important;
}

/* --- 1. HEADER DE LA PÁGINA & TOOLBAR INTEGRADOS Y SIN SUPERPOSICIÓN --- */
.header,
html[data-present="true"] .header {
  display: grid !important;
  grid-template-columns: minmax(0, 1fr) auto !important;
  grid-template-areas:
    "title toolbar"
    "subtitle toolbar" !important;
  align-items: center !important;
  column-gap: 1.15rem !important;
  row-gap: 0.15rem !important;
  padding: 0 !important;
  margin-bottom: 0.35rem !important;
  position: relative !important;
  width: 100% !important;
}

body.has-guia-open .header {
  margin-bottom: 0.35rem !important;
}

.header-row {
  grid-area: title !important;
  display: flex !important;
  justify-content: flex-start !important;
  align-items: center !important;
  gap: 0.65rem !important;
  min-width: 0 !important;
  margin-bottom: 0 !important;
}

.header h1 {
  margin: 0 !important;
  font-size: clamp(1.05rem, 1.8vw, 1.38rem) !important;
  line-height: 1.25 !important;
  text-align: left !important;
  word-break: break-word !important;
}

body.has-guia-open .header h1 {
  font-size: clamp(1.05rem, 1.8vw, 1.38rem) !important;
}

.subtitle {
  grid-area: subtitle !important;
  text-align: left !important;
  font-size: clamp(0.7rem, 1.1vw, 0.78rem) !important;
  line-height: 1.35 !important;
  color: var(--text-muted) !important;
  margin: 0 0 0 1.25rem !important;
  max-width: 68rem !important;
}

/* El toolbar vive dentro de la celda derecha del Grid de .header y jamás pisa el título */
.header .toolbar,
html[data-present="true"] .header .toolbar,
body > .toolbar {
  grid-area: toolbar !important;
  position: static !important;
  top: auto !important;
  right: auto !important;
  left: auto !important;
  margin: 0 !important;
  z-index: 30 !important;
  display: flex !important;
  align-items: center !important;
  justify-content: flex-end !important;
  gap: 0.4rem !important;
  align-self: center !important;
}

@media (max-width: 960px) {
  body {
    padding: 0.6rem !important;
  }
  .flow-nav-top {
    padding: 0.4rem 0.65rem !important;
    margin-bottom: 0.5rem !important;
  }
  .flow-nav-left,
  .flow-nav-right {
    width: 100% !important;
    justify-content: space-between !important;
  }
  .flow-nav-select-wrap {
    flex: 1 1 180px !important;
  }
  .flow-nav-select {
    max-width: 100% !important;
  }
  .header,
  html[data-present="true"] .header {
    grid-template-columns: 1fr !important;
    grid-template-areas:
      "toolbar"
      "title"
      "subtitle" !important;
    row-gap: 0.35rem !important;
  }
  .header .toolbar,
  body > .toolbar {
    width: 100% !important;
    justify-content: flex-end !important;
    margin-bottom: 0.2rem !important;
    overflow-x: auto !important;
  }
  .subtitle {
    margin-left: 0 !important;
  }
}

/* --- 2. CONTENEDOR Y LIENZO DEL DIAGRAMA BPM 100% ESTABLES Y RESPONSIVOS --- */
/* Bloqueo total del contenedor general para evitar que Archify lo estreche al detectar scroll */
.container,
html .container,
body .container,
html[data-reader-narrow="true"] .container,
html[data-reader-narrow="true"] body .container,
body.has-guia-open .container {
  width: 100% !important;
  max-width: 100% !important;
  margin: 0 auto !important;
}

.diagram-container,
html[data-present="true"]:not([data-embed="true"]) .diagram-container {
  position: relative !important;
  border-radius: 0.75rem !important;
  display: flex !important;
  flex-direction: column !important;
  align-items: stretch !important;
  justify-content: flex-start !important;
  width: 100% !important;
  max-width: 100% !important;
  padding: 0.45rem 0.85rem 0.25rem 0.85rem !important;
  overflow: visible !important;
}

body.has-guia-open .diagram-container {
  padding: 0.45rem 0.85rem 0.25rem 0.85rem !important;
}

/* El SVG del flujo BPM mantiene SIEMPRE el 100% de ancho y su altura proporcional exacta */
/* BLOQUEO CRÍTICO: NUNCA transform (zoom/pan), NUNCA clip-path (recorte), NUNCA encogerse */
.diagram-container > svg,
html .diagram-container > svg,
body .diagram-container > svg,
body.has-guia-open .diagram-container > svg,
html[data-reader-narrow="true"] .diagram-container > svg,
html[data-reader-narrow="true"] body .diagram-container > svg,
html[data-present="true"] .diagram-container > svg,
html[data-present="true"] body.has-guia-open .diagram-container > svg,
.diagram-container svg[data-focus-active],
.diagram-container svg[data-view-scale] {
  width: 100% !important;
  min-width: 100% !important;
  max-width: 100% !important;
  height: auto !important;
  min-height: auto !important;
  max-height: none !important;
  transform: none !important;
  clip-path: none !important;
  display: block !important;
  margin: 0 auto !important;
  flex: none !important;
}

/* Mantener todos los pasos del diagrama BPM claramente visibles cuando un paso está seleccionado */
.diagram-container svg[data-focus-active] [data-node-id],
.diagram-container svg[data-focus-active] [data-edge-from] {
  opacity: 0.65 !important;
}

.diagram-container svg[data-focus-active] [data-focus-match] {
  opacity: 0.95 !important;
}

.diagram-container svg[data-focus-active] [data-focus-selected] {
  opacity: 1 !important;
  filter: drop-shadow(0 0 10px var(--frontend-stroke)) !important;
}

/* Detalle técnico y tag inferior ([data-detail="fine"]) siempre visible por defecto en todos los nodos */
.diagram-container svg [data-detail="fine"],
.diagram-container svg [data-detail="context"],
.diagram-container svg [data-detail],
svg [data-detail="fine"],
svg [data-detail="context"],
svg [data-detail] {
  opacity: 1 !important;
  visibility: visible !important;
  pointer-events: auto !important;
}

.diagram-container svg [data-detail="fine"] {
  font-weight: 600 !important;
}

.diagram-container svg [data-detail-anchor],
svg [data-detail-anchor] {
  transform: none !important;
}

.diagram-container svg[data-focus-active] [data-node-id] [data-detail="fine"],
.diagram-container svg[data-focus-active] [data-node-id] [data-detail="context"] {
  opacity: 1 !important;
  visibility: visible !important;
}

/* ==========================================================================
   ESTADOS DE PROGRESO DEL FLUJO BPM (STEPPER / COMPLETADO VS PENDIENTE)
   Solo se colorean los pasos ya realizados/desbloqueados; por defecto solo el primero.
   ========================================================================== */

/* Nodos PENDIENTES (aún no alcanzados): sin color de fondo, borde discontinuo neutro */
.diagram-container svg g[data-step-state="pending"] > rect:not(.c-mask),
svg g[data-step-state="pending"] > rect:not(.c-mask),
g[data-step-state="pending"] > rect:not(.c-mask) {
  fill: rgba(30, 41, 59, 0.45) !important;
  stroke: #475569 !important;
  stroke-width: 1.3px !important;
  stroke-dasharray: 5, 4 !important;
  filter: none !important;
  transition: all 0.25s ease !important;
}

html[data-theme="light"] .diagram-container svg g[data-step-state="pending"] > rect:not(.c-mask),
html[data-theme="light"] svg g[data-step-state="pending"] > rect:not(.c-mask),
html[data-theme="light"] g[data-step-state="pending"] > rect:not(.c-mask) {
  fill: #f8fafc !important;
  stroke: #cbd5e1 !important;
  stroke-width: 1.3px !important;
  stroke-dasharray: 5, 4 !important;
  filter: none !important;
}

/* Sigil / ícono en gris neutro en pendientes */
g[data-step-state="pending"] .semantic-sigil,
g[data-step-state="pending"] .semantic-sigil circle,
g[data-step-state="pending"] .semantic-sigil path,
g[data-step-state="pending"] .semantic-sigil ellipse,
g[data-step-state="pending"] .semantic-sigil rect {
  stroke: #64748b !important;
  fill: none !important;
  color: #64748b !important;
  opacity: 0.65 !important;
}

g[data-step-state="pending"] .sigil-fill {
  fill: #64748b !important;
}

html[data-theme="light"] g[data-step-state="pending"] .semantic-sigil,
html[data-theme="light"] g[data-step-state="pending"] .semantic-sigil circle,
html[data-theme="light"] g[data-step-state="pending"] .semantic-sigil path,
html[data-theme="light"] g[data-step-state="pending"] .semantic-sigil ellipse,
html[data-theme="light"] g[data-step-state="pending"] .semantic-sigil rect {
  stroke: #94a3b8 !important;
  fill: none !important;
  color: #94a3b8 !important;
  opacity: 0.75 !important;
}

html[data-theme="light"] g[data-step-state="pending"] .sigil-fill {
  fill: #94a3b8 !important;
}

/* Textos de nodos pendientes en gris neutro legible (sin colores verdes/rojos/morados) */
g[data-step-state="pending"] text.t-primary,
g[data-step-state="pending"] text[data-node-label] {
  fill: #94a3b8 !important;
  font-weight: 600 !important;
  opacity: 0.8 !important;
}

html[data-theme="light"] g[data-step-state="pending"] text.t-primary,
html[data-theme="light"] g[data-step-state="pending"] text[data-node-label] {
  fill: #475569 !important;
  font-weight: 600 !important;
  opacity: 0.85 !important;
}

g[data-step-state="pending"] text.t-muted,
g[data-step-state="pending"] text[data-detail="context"] {
  fill: #64748b !important;
  opacity: 0.65 !important;
}

html[data-theme="light"] g[data-step-state="pending"] text.t-muted,
html[data-theme="light"] g[data-step-state="pending"] text[data-detail="context"] {
  fill: #64748b !important;
  opacity: 0.75 !important;
}

/* El tercer renglón (detalle técnico) en pendientes es visible pero neutro */
g[data-step-state="pending"] text[data-detail="fine"],
g[data-step-state="pending"] text[class*="t-"] {
  fill: #64748b !important;
  font-weight: 500 !important;
  opacity: 0.6 !important;
}

html[data-theme="light"] g[data-step-state="pending"] text[data-detail="fine"],
html[data-theme="light"] g[data-step-state="pending"] text[class*="t-"] {
  fill: #64748b !important;
  font-weight: 500 !important;
  opacity: 0.75 !important;
}

/* Hover en nodos pendientes */
g[data-step-state="pending"]:hover > rect:not(.c-mask) {
  stroke: #94a3b8 !important;
  stroke-dasharray: none !important;
  fill: rgba(148, 163, 184, 0.12) !important;
}

html[data-theme="light"] g[data-step-state="pending"]:hover > rect:not(.c-mask) {
  stroke: #94a3b8 !important;
  stroke-dasharray: none !important;
  fill: #f1f5f9 !important;
}

/* Nodos COMPLETADOS (ya hechos): conservan sus fondos y bordes de color nativos bien definidos */
g[data-step-state="completed"] > rect:not(.c-mask) {
  stroke-width: 2.2px !important;
  stroke-dasharray: none !important;
  transition: all 0.25s ease !important;
}

/* Nodo ACTUAL (donde se quedaron): COLOREADO y resaltado con pulso ámbar / oro */
g[data-step-state="current"] > rect:not(.c-mask),
g[data-ultimo-escogido="true"] > rect:not(.c-mask) {
  stroke: #f59e0b !important;
  stroke-width: 3.5px !important;
  stroke-dasharray: none !important;
  fill: rgba(245, 158, 11, 0.22) !important;
  filter: drop-shadow(0 0 14px rgba(245, 158, 11, 0.9)) !important;
  animation: pulsoUltimoEscogido 2.4s infinite ease-in-out !important;
}

html[data-theme="light"] g[data-step-state="current"] > rect:not(.c-mask),
html[data-theme="light"] g[data-ultimo-escogido="true"] > rect:not(.c-mask) {
  stroke: #d97706 !important;
  fill: rgba(245, 158, 11, 0.16) !important;
  filter: drop-shadow(0 0 10px rgba(217, 119, 6, 0.75)) !important;
}

/* Nodos completados y actual siempre con opacidad plena */
.diagram-container svg[data-focus-active] g[data-step-state="completed"],
.diagram-container svg[data-focus-active] g[data-step-state="current"],
g[data-step-state="completed"],
g[data-step-state="current"] {
  opacity: 1 !important;
}

/* Flechas conectoras hacia pasos pendientes: atenuadas en gris */
path[data-step-edge="pending"] {
  stroke: #475569 !important;
  stroke-dasharray: 4, 3 !important;
  opacity: 0.45 !important;
}

html[data-theme="light"] path[data-step-edge="pending"] {
  stroke: #94a3b8 !important;
  stroke-dasharray: 4, 3 !important;
  opacity: 0.65 !important;
}

/* Flechas entre pasos completados/activos: bien coloreadas y continuas */
path[data-step-edge="completed"] {
  stroke: #10b981 !important;
  stroke-dasharray: none !important;
  opacity: 1 !important;
  stroke-width: 2px !important;
}

/* Barra de herramientas inferior del lienzo (.diagram-nav) */
html[data-present="true"] .diagram-nav {
  display: none !important;
}

@media (max-width: 768px) {
  .diagram-container {
    padding: 0.75rem !important;
  }
  .diagram-container > svg {
    min-width: 0 !important;
  }
}

/* --- 3. TARJETAS INFORMATIVAS INFERIORES (.CARDS) --- */
.cards {
  display: grid !important;
  grid-template-columns: repeat(auto-fill, minmax(min(20rem, 100%), 1fr)) !important;
  gap: 1.15rem !important;
  margin-top: 1.5rem !important;
}

/* Ocultar en modo presentación para pantalla limpia */
html[data-present="true"] .cards,
html[data-present="true"] .flow-nav-bottom-section {
  display: none !important;
}

@media (min-width: 1300px) {
  .cards {
    grid-template-columns: repeat(auto-fit, minmax(21rem, 1fr)) !important;
  }
}

@media (max-width: 768px) {
  .cards {
    grid-template-columns: 1fr !important;
    gap: 0.85rem !important;
    margin-top: 1.25rem !important;
  }
}

.card {
  padding: 1.1rem 1.25rem !important;
  border-radius: 0.75rem !important;
  background: var(--panel) !important;
  border: 1px solid var(--panel-border) !important;
}

/* --- 4. GUÍA OPERATIVA PASO A PASO (.FOCUS-CHIP.TIENE-GUIA) --- */

/* MODO 1 (PANTALLA NORMAL): Ventana Modal Centrada Flotante con su mismo ancho amplio */
html:not([data-present="true"]) .focus-chip.tiene-guia,
html:not([data-present="true"]) .focus-chip.tiene-guia[hidden] {
  position: fixed !important;
  left: 50% !important;
  top: 50% !important;
  transform: translate(-50%, -50%) !important;
  width: min(76rem, calc(100vw - 2.5rem)) !important;
  max-width: 78rem !important;
  height: min(84vh, 640px) !important;
  max-height: 88vh !important;
  min-height: 320px !important;
  margin: 0 !important;
  padding: 0 !important;
  display: flex !important;
  flex-direction: column !important;
  align-items: stretch !important;
  justify-content: flex-start !important;
  overflow: hidden !important;
  border-radius: 0.85rem !important;
  border: 1.5px solid var(--frontend-stroke, #0891b2) !important;
  box-shadow: 0 25px 80px -10px rgba(0, 0, 0, 0.75), 0 0 0 1px rgba(255, 255, 255, 0.14) !important;
  background: var(--panel, #0f172a) !important;
  z-index: 99 !important;
  box-sizing: border-box !important;
  animation: modalGuiaFadeIn 0.16s ease-out !important;
}

@keyframes modalGuiaFadeIn {
  from {
    opacity: 0;
    transform: translate(-50%, -47%) scale(0.98);
  }
  to {
    opacity: 1;
    transform: translate(-50%, -50%) scale(1);
  }
}

html:not([data-theme="dark"]):not([data-present="true"]) .focus-chip.tiene-guia {
  background: #ffffff !important;
  border-color: #0284c7 !important;
  box-shadow: 0 25px 80px -10px rgba(15, 23, 42, 0.28), 0 0 0 1px rgba(15, 23, 42, 0.1) !important;
}

/* Telón de fondo (Backdrop) del Modal: SOLO en Pantalla Normal */
.guia-modal-backdrop {
  position: fixed !important;
  inset: 0 !important;
  background: rgba(15, 23, 42, 0.6) !important;
  backdrop-filter: blur(3px) !important;
  -webkit-backdrop-filter: blur(3px) !important;
  z-index: 97 !important;
  display: none;
  cursor: pointer;
  animation: backdropFadeIn 0.16s ease-out !important;
}

.guia-modal-backdrop.active {
  display: block !important;
}

html[data-present="true"] .guia-modal-backdrop,
:fullscreen .guia-modal-backdrop {
  display: none !important;
}

@keyframes backdropFadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* MODO 2 (PANTALLA COMPLETA / PRESENTACIÓN): Tabla abajo del flujo BPM con scroll */
html[data-present="true"] .focus-chip.tiene-guia,
html[data-present="true"] .focus-chip.tiene-guia[hidden],
:fullscreen .focus-chip.tiene-guia,
:fullscreen .focus-chip.tiene-guia[hidden] {
  position: relative !important;
  left: auto !important;
  right: auto !important;
  top: auto !important;
  bottom: auto !important;
  transform: none !important;
  width: 100% !important;
  max-width: 100% !important;
  height: clamp(340px, calc(100vh - 240px), 560px) !important;
  max-height: calc(100vh - 210px) !important;
  min-height: 290px !important;
  margin: 0.25rem 0 0 0 !important;
  padding: 0 !important;
  display: flex !important;
  flex-direction: column !important;
  align-items: stretch !important;
  justify-content: flex-start !important;
  overflow: hidden !important;
  border-radius: 0.75rem !important;
  border: 1.5px solid var(--frontend-stroke, #0891b2) !important;
  box-shadow: 0 12px 36px rgba(15, 23, 42, 0.22) !important;
  background: var(--panel, #0f172a) !important;
  z-index: 40 !important;
  box-sizing: border-box !important;
  animation: none !important;
}

html[data-present="true"] body.has-guia-open .diagram-container {
  height: auto !important;
  max-height: none !important;
  padding: 0.15rem 0.65rem 0.1rem 0.65rem !important;
  overflow: visible !important;
}

html[data-present="true"]:not([data-theme="dark"]) .focus-chip.tiene-guia {
  background: #ffffff !important;
  border-color: #0284c7 !important;
}

/* Ocultar elementos nativos de Archify que no pertenecen a la Guía Operativa */
.focus-chip.tiene-guia .relationship-lens-eyebrow,
.focus-chip.tiene-guia #focus-detail,
.focus-chip.tiene-guia #focus-passport-meta,
.focus-chip.tiene-guia #focus-reach,
.focus-chip.tiene-guia #focus-evidence,
.focus-chip.tiene-guia .relationship-lens-list,
.focus-chip.tiene-guia #relationship-lens-list,
.focus-chip.tiene-guia #btn-focus-relations,
.focus-chip.tiene-guia .relationship-lens-drag-handle,
.focus-chip.tiene-guia #relationship-lens-title,
.focus-chip.tiene-guia #focus-summary,
.focus-chip.tiene-guia > .relationship-lens-head > .relationship-lens-actions {
  display: none !important;
}

/* Estructura interna de la Guía */
.focus-chip.tiene-guia .relationship-lens-head {
  display: flex !important;
  flex-direction: column !important;
  align-items: stretch !important;
  justify-content: flex-start !important;
  padding: 0 !important;
  margin: 0 !important;
  border: none !important;
  width: 100% !important;
  max-width: 100% !important;
  flex: 1 1 0% !important;
  height: calc(100% - 33px) !important;
  max-height: calc(100% - 33px) !important;
  min-height: 0 !important;
  overflow: hidden !important;
  background: transparent !important;
}

/* Barra superior de la Guía (Topbar) */
.guia-modal-topbar {
  display: grid !important;
  grid-template-columns: minmax(0, 1fr) auto !important;
  align-items: center !important;
  column-gap: 0.75rem !important;
  width: 100% !important;
  box-sizing: border-box !important;
  padding: 0.22rem 0.85rem !important;
  height: 33px !important;
  min-height: 33px !important;
  max-height: 33px !important;
  background: linear-gradient(135deg, rgba(30, 41, 59, 0.96), rgba(15, 23, 42, 0.99)) !important;
  border-bottom: 1px solid rgba(148, 163, 184, 0.24) !important;
  flex: 0 0 33px !important;
  z-index: 35 !important;
  user-select: none !important;
}

html:not([data-theme="dark"]) .guia-modal-topbar {
  background: linear-gradient(135deg, #ffffff, #f1f5f9) !important;
  border-bottom-color: #cbd5e1 !important;
}

.guia-modal-brand {
  display: flex !important;
  align-items: center !important;
  gap: 0.55rem !important;
  min-width: 0 !important;
  overflow: hidden !important;
}

.guia-brand-badge {
  font-size: 0.62rem !important;
  font-weight: 800 !important;
  text-transform: uppercase !important;
  letter-spacing: 0.05em !important;
  padding: 0.16rem 0.48rem !important;
  border-radius: 0.32rem !important;
  background: #4338ca !important;
  color: #ffffff !important;
  flex-shrink: 0 !important;
}

.guia-brand-title {
  font-size: 0.82rem !important;
  font-weight: 700 !important;
  color: var(--toolbar-text, #f8fafc) !important;
  white-space: nowrap !important;
  overflow: hidden !important;
  text-overflow: ellipsis !important;
}

html:not([data-theme="dark"]) .guia-brand-title {
  color: #0f172a !important;
}

.guia-topbar-actions {
  display: flex !important;
  align-items: center !important;
  justify-content: flex-end !important;
  gap: 0.4rem !important;
  flex-shrink: 0 !important;
  justify-self: end !important;
}

.focus-chip .guia-topbar-actions .chip-btn-ctrl {
  background: rgba(148, 163, 184, 0.14) !important;
  border: 1px solid rgba(148, 163, 184, 0.3) !important;
  color: var(--toolbar-text, #e2e8f0) !important;
  border-radius: 0.42rem !important;
  padding: 0.22rem 0.58rem !important;
  font-size: 0.71rem !important;
  font-weight: 600 !important;
  cursor: pointer !important;
  display: inline-flex !important;
  align-items: center !important;
  gap: 0.3rem !important;
  transition: all 0.15s ease !important;
  line-height: 1.2 !important;
  white-space: nowrap !important;
}

html:not([data-theme="dark"]) .focus-chip .guia-topbar-actions .chip-btn-ctrl {
  color: #334155 !important;
  background: #ffffff !important;
  border-color: #cbd5e1 !important;
}

.focus-chip .guia-topbar-actions .chip-btn-ctrl:hover {
  background: rgba(148, 163, 184, 0.28) !important;
  color: #ffffff !important;
  border-color: var(--frontend-stroke) !important;
}

html:not([data-theme="dark"]) .focus-chip .guia-topbar-actions .chip-btn-ctrl:hover {
  background: #f1f5f9 !important;
  color: #0f172a !important;
}

.focus-chip .guia-topbar-actions .chip-btn-close {
  width: 1.6rem !important;
  height: 1.6rem !important;
  border-radius: 50% !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  font-size: 0.88rem !important;
  line-height: 1 !important;
  padding: 0 !important;
  background: rgba(239, 68, 68, 0.14) !important;
  border: 1px solid rgba(239, 68, 68, 0.35) !important;
  color: #f87171 !important;
  cursor: pointer !important;
  transition: all 0.15s ease !important;
  margin-left: 0.15rem !important;
  flex-shrink: 0 !important;
}

.focus-chip .guia-topbar-actions .chip-btn-close:hover {
  background: #ef4444 !important;
  color: #ffffff !important;
  border-color: #ef4444 !important;
  transform: scale(1.06) !important;
}

.focus-chip.tiene-guia .relationship-lens-copy {
  width: 100% !important;
  max-width: 100% !important;
  box-sizing: border-box !important;
  min-width: 0 !important;
  min-height: 0 !important;
  height: 100% !important;
  max-height: 100% !important;
  display: flex !important;
  flex-direction: column !important;
  flex: 1 1 0% !important;
  overflow: hidden !important;
  padding: 0 !important;
  margin: 0 !important;
}

.guia-operativa-card {
  margin: 0 !important;
  padding: 0 !important;
  border: none !important;
  background: transparent !important;
  display: flex !important;
  flex-direction: column !important;
  justify-content: space-between !important;
  flex: 1 1 0% !important;
  width: 100% !important;
  height: 100% !important;
  max-height: 100% !important;
  min-height: 0 !important;
  box-sizing: border-box !important;
  overflow: hidden !important;
}

/* Contenedor vertical de la guía: Stepper y Hero fijos, Tabla con scroll propio */
.guia-body-scroll {
  flex: 1 1 0% !important;
  min-height: 0 !important;
  max-height: calc(100% - 36px) !important;
  height: calc(100% - 36px) !important;
  display: flex !important;
  flex-direction: column !important;
  align-items: stretch !important;
  justify-content: flex-start !important;
  overflow: hidden !important;
  padding: 0.28rem 0.75rem 0.2rem 0.75rem !important;
  box-sizing: border-box !important;
}

/* Stepper de Fases Interactivo Horizontal */
.guia-stepper-wrap {
  overflow-x: auto !important;
  scrollbar-width: thin !important;
  -webkit-overflow-scrolling: touch !important;
  padding: 0 0 0.2rem 0 !important;
  margin-bottom: 0.22rem !important;
  border-bottom: 1px solid rgba(148, 163, 184, 0.16) !important;
  flex: 0 0 auto !important;
}

.guia-stepper-track {
  display: flex !important;
  align-items: center !important;
  gap: 0.3rem !important;
  min-width: max-content !important;
}

.focus-chip .guia-step-pill {
  display: inline-flex !important;
  align-items: center !important;
  gap: 0.3rem !important;
  background: rgba(148, 163, 184, 0.1) !important;
  border: 1px solid rgba(148, 163, 184, 0.22) !important;
  color: var(--text-muted, #94a3b8) !important;
  padding: 0.18rem 0.58rem !important;
  border-radius: 999px !important;
  font-size: 0.7rem !important;
  font-weight: 600 !important;
  cursor: pointer !important;
  transition: all 0.18s ease !important;
  white-space: nowrap !important;
  flex-shrink: 0 !important;
}

html:not([data-theme="dark"]) .focus-chip .guia-step-pill {
  background: #f1f5f9 !important;
  border-color: #cbd5e1 !important;
  color: #64748b !important;
}

.focus-chip .guia-step-pill:hover {
  border-color: #38bdf8 !important;
  color: var(--toolbar-text, #f1f5f9) !important;
  background: rgba(56, 189, 248, 0.15) !important;
}

.focus-chip .guia-step-pill.active {
  background: linear-gradient(135deg, #4338ca, #3b82f6) !important;
  border-color: #60a5fa !important;
  color: #ffffff !important;
  font-weight: 700 !important;
  box-shadow: 0 3px 10px rgba(59, 130, 246, 0.35) !important;
}

.focus-chip .guia-step-pill.past {
  background: rgba(16, 185, 129, 0.12) !important;
  border-color: rgba(16, 185, 129, 0.3) !important;
  color: #34d399 !important;
}

html:not([data-theme="dark"]) .focus-chip .guia-step-pill.past {
  background: #ecfdf5 !important;
  color: #059669 !important;
  border-color: #a7f3d0 !important;
}

.focus-chip .guia-step-pill.locked {
  opacity: 0.42 !important;
  cursor: not-allowed !important;
  background: rgba(148, 163, 184, 0.05) !important;
  border: 1px dashed rgba(148, 163, 184, 0.28) !important;
  color: var(--text-muted, #94a3b8) !important;
  pointer-events: none !important;
  user-select: none !important;
}

html:not([data-theme="dark"]) .focus-chip .guia-step-pill.locked {
  background: #f8fafc !important;
  border-color: #cbd5e1 !important;
  color: #94a3b8 !important;
}

.pill-badge {
  min-width: 1.15rem !important;
  height: 1.15rem !important;
  padding: 0 0.2rem !important;
  border-radius: 999px !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  font-size: 0.62rem !important;
  font-weight: 800 !important;
  background: rgba(255, 255, 255, 0.2) !important;
}

.guia-step-pill.past .pill-badge {
  background: rgba(16, 185, 129, 0.25) !important;
  color: #10b981 !important;
}

.guia-step-pill.locked .pill-badge {
  background: rgba(148, 163, 184, 0.2) !important;
  color: #94a3b8 !important;
  font-size: 0.58rem !important;
}

.stepper-arrow {
  color: rgba(148, 163, 184, 0.4) !important;
  font-size: 0.8rem !important;
  user-select: none !important;
  flex-shrink: 0 !important;
}

.stepper-arrow.past {
  color: #10b981 !important;
}

.stepper-arrow.locked {
  opacity: 0.25 !important;
}

.guia-stepper-progress {
  width: 100% !important;
  height: 3px !important;
  background: rgba(148, 163, 184, 0.2) !important;
  border-radius: 2px !important;
  overflow: hidden !important;
  margin-top: 0.38rem !important;
}

.guia-progress-fill {
  height: 100% !important;
  background: linear-gradient(90deg, #38bdf8, #34d399) !important;
  border-radius: 2px !important;
  transition: width 0.25s ease !important;
}

.focus-chip .guia-nav-btn {
  background: rgba(148, 163, 184, 0.15) !important;
  border: 1px solid rgba(148, 163, 184, 0.3) !important;
  color: var(--toolbar-text, #f1f5f9) !important;
  padding: 0.42rem 0.9rem !important;
  border-radius: 0.48rem !important;
  font-size: 0.75rem !important;
  font-weight: 700 !important;
  cursor: pointer !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  gap: 0.35rem !important;
  transition: all 0.15s ease !important;
  white-space: nowrap !important;
}

html:not([data-theme="dark"]) .focus-chip .guia-nav-btn {
  color: #0f172a !important;
  background: #ffffff !important;
  border-color: #cbd5e1 !important;
}

.focus-chip .guia-nav-btn:hover:not(:disabled) {
  background: rgba(148, 163, 184, 0.28) !important;
  border-color: var(--frontend-stroke) !important;
  transform: translateY(-1px) !important;
}

.focus-chip .guia-nav-btn.primary,
html:not([data-theme="dark"]) .focus-chip .guia-nav-btn.primary {
  background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
  color: #ffffff !important;
  border-color: #3b82f6 !important;
  box-shadow: 0 4px 14px rgba(37, 99, 235, 0.4) !important;
}

.focus-chip .guia-nav-btn.primary:hover:not(:disabled) {
  background: linear-gradient(135deg, #1d4ed8, #1e40af) !important;
  border-color: #60a5fa !important;
}

.focus-chip .guia-nav-btn:disabled {
  opacity: 0.38 !important;
  cursor: not-allowed !important;
  transform: none !important;
}

/* Hero de Fase actual e Hito Compacto */
.guia-fase-hero {
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  flex-wrap: wrap !important;
  gap: 0.35rem !important;
  margin-bottom: 0.2rem !important;
  padding: 0.2rem 0.55rem !important;
  border-radius: 0.45rem !important;
  background: rgba(30, 41, 59, 0.45) !important;
  border: 1px solid rgba(148, 163, 184, 0.18) !important;
  flex: 0 0 auto !important;
}

html:not([data-theme="dark"]) .guia-fase-hero {
  background: #f8fafc !important;
  border-color: #e2e8f0 !important;
}

.guia-fase-main {
  display: flex !important;
  align-items: center !important;
  gap: 0.45rem !important;
  flex-wrap: wrap !important;
}

.guia-fase-actions {
  display: flex !important;
  align-items: center !important;
  gap: 0.4rem !important;
  flex-wrap: wrap !important;
}

.btn-toggle-validar-todos {
  display: inline-flex !important;
  align-items: center !important;
  gap: 0.28rem !important;
  font-size: 0.68rem !important;
  font-weight: 700 !important;
  padding: 0.16rem 0.52rem !important;
  border-radius: 0.32rem !important;
  border: 1px solid rgba(148, 163, 184, 0.28) !important;
  background: rgba(148, 163, 184, 0.12) !important;
  color: var(--toolbar-text, #e2e8f0) !important;
  cursor: pointer !important;
  transition: all 0.15s ease !important;
  white-space: nowrap !important;
}

.btn-toggle-validar-todos:hover {
  background: rgba(148, 163, 184, 0.25) !important;
  border-color: #38bdf8 !important;
  color: #38bdf8 !important;
}

html:not([data-theme="dark"]) .btn-toggle-validar-todos {
  background: #f1f5f9 !important;
  border-color: #cbd5e1 !important;
  color: #334155 !important;
}

html:not([data-theme="dark"]) .btn-toggle-validar-todos:hover {
  background: #e2e8f0 !important;
  color: #0284c7 !important;
  border-color: #0284c7 !important;
}

.btn-toggle-validar-todos.todos-completos {
  background: rgba(16, 185, 129, 0.15) !important;
  border-color: rgba(16, 185, 129, 0.35) !important;
  color: #34d399 !important;
}

html:not([data-theme="dark"]) .btn-toggle-validar-todos.todos-completos {
  background: #d1fae5 !important;
  border-color: #6ee7b7 !important;
  color: #065f46 !important;
}

.guia-pantalla-pill {
  font-size: 0.68rem !important;
  font-weight: 800 !important;
  padding: 0.15rem 0.45rem !important;
  border-radius: 0.3rem !important;
  background: #0284c7 !important;
  color: #ffffff !important;
  letter-spacing: 0.03em !important;
}

.guia-fase-title {
  margin: 0 !important;
  font-size: 0.8rem !important;
  font-weight: 700 !important;
  color: var(--toolbar-text, #f8fafc) !important;
}

html:not([data-theme="dark"]) .guia-fase-title {
  color: #0f172a !important;
}

.guia-hito-badge {
  display: inline-flex !important;
  align-items: center !important;
  gap: 0.3rem !important;
  font-size: 0.68rem !important;
  font-weight: 700 !important;
  padding: 0.15rem 0.5rem !important;
  border-radius: 0.32rem !important;
  background: rgba(16, 185, 129, 0.15) !important;
  border: 1px solid rgba(16, 185, 129, 0.35) !important;
  color: #34d399 !important;
}

html:not([data-theme="dark"]) .guia-hito-badge {
  background: #d1fae5 !important;
  color: #065f46 !important;
  border-color: #6ee7b7 !important;
}

/* --- 5. TABLA DE 6 COLUMNAS CON SCROLL VERTICAL PROPIO Y THEAD STICKY --- */
.guia-tabla-wrap {
  width: 100% !important;
  flex: 1 1 0% !important;
  min-height: 120px !important;
  overflow-y: auto !important;
  overflow-x: auto !important;
  border-radius: 0.5rem !important;
  border: 1px solid rgba(148, 163, 184, 0.22) !important;
  background: rgba(15, 23, 42, 0.45) !important;
  margin-bottom: 0.15rem !important;
  scrollbar-width: thin !important;
  scrollbar-color: #0284c7 rgba(15, 23, 42, 0.45) !important;
  -webkit-overflow-scrolling: touch !important;
}

.guia-tabla-wrap::-webkit-scrollbar {
  -webkit-appearance: none !important;
  width: 9px !important;
  height: 8px !important;
  display: block !important;
}

.guia-tabla-wrap::-webkit-scrollbar-track {
  background: rgba(15, 23, 42, 0.55) !important;
  border-radius: 4px !important;
}

.guia-tabla-wrap::-webkit-scrollbar-thumb {
  background: #0284c7 !important;
  border-radius: 4px !important;
  border: 2px solid rgba(15, 23, 42, 0.6) !important;
  min-height: 36px !important;
}

.guia-tabla-wrap::-webkit-scrollbar-thumb:hover {
  background: #38bdf8 !important;
}

html:not([data-theme="dark"]) .guia-tabla-wrap {
  background: #ffffff !important;
  border-color: #cbd5e1 !important;
  scrollbar-color: #0284c7 #f1f5f9 !important;
}

html:not([data-theme="dark"]) .guia-tabla-wrap::-webkit-scrollbar-track {
  background: #f1f5f9 !important;
}

html:not([data-theme="dark"]) .guia-tabla-wrap::-webkit-scrollbar-thumb {
  background: #0284c7 !important;
  border-color: #ffffff !important;
}

.guia-tabla {
  width: 100% !important;
  min-width: 44rem !important;
  border-collapse: collapse !important;
  font-size: 0.72rem !important;
  text-align: left !important;
  table-layout: fixed !important;
}

.guia-tabla thead th {
  position: sticky !important;
  top: 0 !important;
  z-index: 25 !important;
  background: #1e293b !important;
  color: #94a3b8 !important;
  font-weight: 700 !important;
  text-transform: uppercase !important;
  font-size: 0.64rem !important;
  letter-spacing: 0.04em !important;
  padding: 0.35rem 0.55rem !important;
  border-bottom: 2px solid rgba(148, 163, 184, 0.32) !important;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.25) !important;
  white-space: nowrap !important;
}

html:not([data-theme="dark"]) .guia-tabla thead th {
  background: #f1f5f9 !important;
  color: #334155 !important;
  border-bottom-color: #cbd5e1 !important;
  box-shadow: 0 2px 4px rgba(15, 23, 42, 0.08) !important;
}

.guia-tabla td {
  padding: 0.25rem 0.55rem !important;
  border-bottom: 1px solid rgba(148, 163, 184, 0.12) !important;
  vertical-align: middle !important;
}

.guia-tabla tr:last-child td {
  border-bottom: none !important;
}

.guia-tabla th.th-num,
.guia-tabla td.guia-td-num {
  width: 34px !important;
  min-width: 34px !important;
  max-width: 34px !important;
  text-align: center !important;
  padding: 0.25rem 0.2rem !important;
}

.guia-tabla th:nth-child(2), .guia-tabla td:nth-child(2) { width: 17% !important; min-width: 120px !important; }
.guia-tabla th:nth-child(3), .guia-tabla td:nth-child(3) { width: 15% !important; min-width: 110px !important; }
.guia-tabla th:nth-child(4), .guia-tabla td:nth-child(4) { width: 16% !important; min-width: 115px !important; }
.guia-tabla th:nth-child(5), .guia-tabla td:nth-child(5) { width: 12% !important; min-width: 90px !important; }
.guia-tabla th:nth-child(6), .guia-tabla td:nth-child(6) { width: 40% !important; min-width: 210px !important; }

/* Botón de paso enumerado interactivo */
.focus-chip .guia-check-btn {
  background: transparent !important;
  border: none !important;
  padding: 0 !important;
  margin: 0 !important;
  cursor: pointer !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  outline: none !important;
}

.guia-check-btn .num-badge {
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  width: 1.45rem !important;
  height: 1.45rem !important;
  border-radius: 50% !important;
  font-size: 0.7rem !important;
  font-weight: 800 !important;
  background: rgba(148, 163, 184, 0.16) !important;
  color: #cbd5e1 !important;
  border: 1px solid rgba(148, 163, 184, 0.3) !important;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

html:not([data-theme="dark"]) .guia-check-btn .num-badge {
  background: #f1f5f9 !important;
  color: #475569 !important;
  border-color: #cbd5e1 !important;
}

.guia-check-btn:hover .num-badge {
  background: rgba(56, 189, 248, 0.25) !important;
  border-color: #38bdf8 !important;
  color: #38bdf8 !important;
  transform: scale(1.1) !important;
}

/* Fila interactiva de la tabla de pasos */
.guia-fila-paso {
  cursor: pointer !important;
  transition: background-color 0.15s ease, outline 0.15s ease !important;
}

.guia-fila-paso:hover {
  background: rgba(56, 189, 248, 0.07) !important;
}

html:not([data-theme="dark"]) .guia-fila-paso:hover {
  background: #f1f5f9 !important;
}

/* Fila marcada como completada */
.guia-fila-paso.completada {
  background: rgba(16, 185, 129, 0.08) !important;
}

html:not([data-theme="dark"]) .guia-fila-paso.completada {
  background: #f0fdf4 !important;
}

.guia-fila-paso.completada:hover {
  background: rgba(16, 185, 129, 0.14) !important;
}

html:not([data-theme="dark"]) .guia-fila-paso.completada:hover {
  background: #e2fbf0 !important;
}

.guia-fila-paso.completada .guia-check-btn .num-badge {
  background: #10b981 !important;
  color: #ffffff !important;
  border-color: #059669 !important;
  box-shadow: 0 0 10px rgba(16, 185, 129, 0.45) !important;
}

/* Atención de filas pendientes cuando se solicita seguir validando */
@keyframes pulsoPendiente {
  0% { background-color: rgba(245, 158, 11, 0.4); transform: scale(1); }
  25% { transform: scale(1.006); }
  50% { background-color: rgba(245, 158, 11, 0.55); }
  100% { background-color: rgba(245, 158, 11, 0.12); transform: scale(1); }
}

tr.guia-fila-paso.pendiente-atencion {
  animation: pulsoPendiente 0.75s ease-in-out !important;
  outline: 2px solid #f59e0b !important;
  outline-offset: -2px !important;
}

.guia-campo {
  font-weight: 700 !important;
  color: #f8fafc !important;
  font-size: 0.72rem !important;
  line-height: 1.25 !important;
}

html:not([data-theme="dark"]) .guia-campo {
  color: #0f172a !important;
}

/* Valores inteligentes: white-space nowrap para evitar cortar SSASECT o (Vacío) */
.guia-valor {
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace !important;
  font-weight: 700 !important;
  color: #38bdf8 !important;
  background: rgba(56, 189, 248, 0.14) !important;
  padding: 0.16rem 0.48rem !important;
  border-radius: 0.35rem !important;
  display: inline-flex !important;
  align-items: center !important;
  gap: 0.28rem !important;
  white-space: nowrap !important;
  word-break: normal !important;
  font-size: 0.72rem !important;
  line-height: 1.2 !important;
}

.guia-valor.valor-largo {
  white-space: normal !important;
}

html:not([data-theme="dark"]) .guia-valor {
  color: #0284c7 !important;
  background: #e0f2fe !important;
}

.guia-valor.valor-vacio {
  background: rgba(245, 158, 11, 0.18) !important;
  color: #fbbf24 !important;
  border: 1px solid rgba(245, 158, 11, 0.45) !important;
}

html:not([data-theme="dark"]) .guia-valor.valor-vacio {
  background: #fef3c7 !important;
  color: #b45309 !important;
  border-color: #fde68a !important;
}

.guia-valor.valor-accion {
  background: rgba(99, 102, 241, 0.2) !important;
  color: #a5b4fc !important;
  border: 1px solid rgba(99, 102, 241, 0.45) !important;
}

html:not([data-theme="dark"]) .guia-valor.valor-accion {
  background: #e0e7ff !important;
  color: #4338ca !important;
  border-color: #c7d2fe !important;
}

.guia-ejemplo {
  font-size: 0.72rem !important;
  line-height: 1.3 !important;
  color: var(--text, #e2e8f0) !important;
}

html:not([data-theme="dark"]) .guia-ejemplo {
  color: #334155 !important;
}

.ejemplo-badge {
  display: inline-block !important;
  background: rgba(148, 163, 184, 0.1) !important;
  border: 1px solid rgba(148, 163, 184, 0.22) !important;
  padding: 0.14rem 0.45rem !important;
  border-radius: 0.32rem !important;
  font-size: 0.71rem !important;
  line-height: 1.25 !important;
}

html:not([data-theme="dark"]) .ejemplo-badge {
  background: #f1f5f9 !important;
  border-color: #cbd5e1 !important;
  color: #334155 !important;
}

.guia-tipo-tag {
  font-size: 0.62rem !important;
  font-weight: 600 !important;
  padding: 0.14rem 0.42rem !important;
  border-radius: 0.3rem !important;
  background: rgba(148, 163, 184, 0.15) !important;
  color: #cbd5e1 !important;
  display: inline-block !important;
  white-space: nowrap !important;
}

html:not([data-theme="dark"]) .guia-tipo-tag {
  color: #475569 !important;
  background: #f1f5f9 !important;
}

.guia-tipo-tag.critico {
  background: rgba(16, 185, 129, 0.2) !important;
  color: #34d399 !important;
  border: 1px solid rgba(16, 185, 129, 0.4) !important;
}

html:not([data-theme="dark"]) .guia-tipo-tag.critico {
  background: #d1fae5 !important;
  color: #065f46 !important;
  border-color: #6ee7b7 !important;
}

.guia-detalle {
  color: #94a3b8 !important;
  font-size: 0.71rem !important;
  line-height: 1.35 !important;
}

html:not([data-theme="dark"]) .guia-detalle {
  color: #334155 !important;
}

/* Footer Inferior Permanente Anclado a la Base */
.guia-footer-sticky {
  flex: 0 0 36px !important;
  width: 100% !important;
  box-sizing: border-box !important;
  margin: 0 !important;
  padding: 0.22rem 0.85rem !important;
  height: 36px !important;
  min-height: 36px !important;
  max-height: 36px !important;
  background: rgba(15, 23, 42, 0.98) !important;
  border-top: 1px solid rgba(148, 163, 184, 0.22) !important;
  display: grid !important;
  grid-template-columns: auto minmax(0, 1fr) auto !important;
  align-items: center !important;
  gap: 0.6rem !important;
  z-index: 40 !important;
  backdrop-filter: blur(16px) !important;
  -webkit-backdrop-filter: blur(16px) !important;
}

html:not([data-theme="dark"]) .guia-footer-sticky {
  background: rgba(255, 255, 255, 0.98) !important;
  border-top-color: #cbd5e1 !important;
}

.focus-chip .btn-pie-next {
  min-width: 6.8rem !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  gap: 0.45rem !important;
  padding: 0.38rem 1.05rem !important;
  border-radius: 0.48rem !important;
  font-size: 0.8rem !important;
  font-weight: 700 !important;
  flex-shrink: 0 !important;
  white-space: nowrap !important;
  text-decoration: none !important;
}

.focus-chip .btn-pie-prev {
  min-width: 6.5rem !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  gap: 0.38rem !important;
  padding: 0.38rem 0.95rem !important;
  border-radius: 0.48rem !important;
  font-size: 0.78rem !important;
  font-weight: 600 !important;
  flex-shrink: 0 !important;
  white-space: nowrap !important;
}

.btn-next-arrow {
  font-size: 0.95rem !important;
  font-weight: 800 !important;
  flex-shrink: 0 !important;
  line-height: 1 !important;
}

/* Modal de confirmación de validación de pasos */
.guia-confirm-overlay {
  position: absolute !important;
  inset: 0 !important;
  z-index: 100 !important;
  background: rgba(15, 23, 42, 0.72) !important;
  backdrop-filter: blur(5px) !important;
  -webkit-backdrop-filter: blur(5px) !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  padding: 1rem !important;
  border-radius: 0.75rem !important;
  animation: fadeInModal 0.15s ease-out !important;
}

.guia-confirm-overlay[hidden] {
  display: none !important;
}

.guia-confirm-modal {
  background: #1e293b !important;
  border: 1px solid rgba(245, 158, 11, 0.4) !important;
  border-radius: 0.75rem !important;
  box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.65), 0 0 0 1px rgba(255, 255, 255, 0.08) !important;
  max-width: 25rem !important;
  width: 100% !important;
  padding: 1.15rem 1.25rem !important;
  display: flex !important;
  flex-direction: column !important;
  gap: 0.75rem !important;
}

html:not([data-theme="dark"]) .guia-confirm-modal {
  background: #ffffff !important;
  border-color: rgba(245, 158, 11, 0.5) !important;
  box-shadow: 0 20px 35px -8px rgba(15, 23, 42, 0.25), 0 0 0 1px rgba(0, 0, 0, 0.06) !important;
}

.guia-confirm-header {
  display: flex !important;
  align-items: center !important;
  gap: 0.55rem !important;
}

.guia-confirm-icon {
  font-size: 1.35rem !important;
  line-height: 1 !important;
  flex-shrink: 0 !important;
}

.guia-confirm-title {
  margin: 0 !important;
  font-size: 0.95rem !important;
  font-weight: 700 !important;
  color: #f8fafc !important;
}

html:not([data-theme="dark"]) .guia-confirm-title {
  color: #0f172a !important;
}

.guia-confirm-body {
  font-size: 0.82rem !important;
  color: #cbd5e1 !important;
  line-height: 1.4 !important;
  margin: 0 !important;
}

html:not([data-theme="dark"]) .guia-confirm-body {
  color: #475569 !important;
}

.guia-confirm-body strong {
  color: #f59e0b !important;
  font-weight: 700 !important;
}

.guia-confirm-question {
  font-size: 0.82rem !important;
  font-weight: 600 !important;
  color: #e2e8f0 !important;
  margin: 0 !important;
}

html:not([data-theme="dark"]) .guia-confirm-question {
  color: #1e293b !important;
}

.guia-confirm-actions {
  display: flex !important;
  align-items: center !important;
  justify-content: flex-end !important;
  gap: 0.55rem !important;
  margin-top: 0.35rem !important;
}

.btn-confirm-seguir {
  padding: 0.42rem 0.9rem !important;
  font-size: 0.78rem !important;
  font-weight: 600 !important;
  border-radius: 0.42rem !important;
  border: 1px solid rgba(255, 255, 255, 0.16) !important;
  background: rgba(255, 255, 255, 0.08) !important;
  color: #f1f5f9 !important;
  cursor: pointer !important;
  transition: all 0.15s ease !important;
}

.btn-confirm-seguir:hover {
  background: rgba(255, 255, 255, 0.18) !important;
  color: #ffffff !important;
}

html:not([data-theme="dark"]) .btn-confirm-seguir {
  background: #f1f5f9 !important;
  border-color: #cbd5e1 !important;
  color: #334155 !important;
}

html:not([data-theme="dark"]) .btn-confirm-seguir:hover {
  background: #e2e8f0 !important;
  color: #0f172a !important;
}

.btn-confirm-pasar {
  padding: 0.42rem 1rem !important;
  font-size: 0.78rem !important;
  font-weight: 700 !important;
  border-radius: 0.42rem !important;
  border: none !important;
  background: #f59e0b !important;
  color: #0f172a !important;
  cursor: pointer !important;
  transition: all 0.15s ease !important;
}

.btn-confirm-pasar:hover {
  background: #d97706 !important;
  color: #ffffff !important;
}

.guia-pie-status {
  font-size: 0.72rem !important;
  color: var(--text-muted, #94a3b8) !important;
  font-weight: 600 !important;
  text-align: center !important;
  white-space: nowrap !important;
  overflow: hidden !important;
  text-overflow: ellipsis !important;
}

html:not([data-theme="dark"]) .guia-pie-status {
  color: #64748b !important;
}

.guia-pie-final {
  font-size: 0.78rem !important;
  font-weight: 700 !important;
  color: #34d399 !important;
  text-align: right !important;
  white-space: nowrap !important;
}

html:not([data-theme="dark"]) .guia-pie-final {
  color: #059669 !important;
}

/* Modo móvil y tablets (< 768px) */
@media (max-width: 768px) {
  .guia-modal-topbar {
    padding: 0.55rem 0.85rem !important;
    column-gap: 0.5rem !important;
  }

  .guia-brand-title {
    font-size: 0.78rem !important;
  }

  .btn-copy-txt {
    display: none !important;
  }

  .focus-chip .guia-topbar-actions .chip-btn-ctrl {
    padding: 0.26rem 0.5rem !important;
  }

  .guia-body-scroll {
    padding: 0.55rem 0.8rem 0.65rem 0.8rem !important;
  }

  .guia-footer-sticky {
    padding: 0.55rem 0.8rem !important;
    grid-template-columns: 1fr 1fr !important;
    grid-template-areas:
      "status status"
      "prev next" !important;
    gap: 0.42rem !important;
  }

  .guia-pie-status {
    grid-area: status !important;
    font-size: 0.7rem !important;
  }

  .focus-chip .btn-pie-prev {
    grid-area: prev !important;
    width: 100% !important;
    font-size: 0.72rem !important;
    padding: 0.42rem 0.5rem !important;
  }

  .focus-chip .btn-pie-next,
  .guia-pie-final {
    grid-area: next !important;
    min-width: 0 !important;
    max-width: 100% !important;
    width: 100% !important;
    font-size: 0.72rem !important;
    padding: 0.42rem 0.6rem !important;
    text-align: center !important;
  }

  .guia-tabla {
    min-width: 0 !important;
  }

  .guia-tabla,
  .guia-tabla thead,
  .guia-tabla tbody,
  .guia-tabla tr,
  .guia-tabla td,
  .guia-tabla th {
    display: block !important;
    width: 100% !important;
  }

  .guia-tabla thead {
    display: none !important;
  }

  .guia-tabla tr {
    margin-bottom: 0.5rem !important;
    padding: 0.5rem 0.65rem !important;
    border-radius: 0.45rem !important;
    background: rgba(30, 41, 59, 0.45) !important;
    border: 1px solid rgba(148, 163, 184, 0.18) !important;
  }

  html:not([data-theme="dark"]) .guia-tabla tr {
    background: rgba(241, 245, 249, 0.9) !important;
    border-color: rgba(203, 213, 225, 0.8) !important;
  }

  .guia-tabla td {
    padding: 0.18rem 0 !important;
    border-bottom: none !important;
    width: 100% !important;
  }
}

/* ==========================================================================
   ÚLTIMO PASO/NODO BPM SELECCIONADO POR EL USUARIO
   Se resalta de un color distintivo (ámbar/oro eléctrico) para que al salir
   del modal el usuario reconozca de inmediato qué paso fue el último escogido.
   ========================================================================== */
g[data-ultimo-escogido="true"] {
  opacity: 1 !important;
  cursor: pointer !important;
}

g[data-ultimo-escogido="true"] > rect:not(.c-mask) {
  stroke: #f59e0b !important;
  stroke-width: 3.5px !important;
  stroke-dasharray: none !important;
  fill: rgba(245, 158, 11, 0.22) !important;
  filter: drop-shadow(0 0 14px rgba(245, 158, 11, 0.9)) !important;
  transition: stroke 0.25s ease, fill 0.25s ease, filter 0.25s ease !important;
  animation: pulsoUltimoEscogido 2.4s infinite ease-in-out !important;
}

@keyframes pulsoUltimoEscogido {
  0%, 100% {
    stroke: #f59e0b;
    filter: drop-shadow(0 0 8px rgba(245, 158, 11, 0.7));
  }
  50% {
    stroke: #fbbf24;
    filter: drop-shadow(0 0 18px rgba(251, 191, 36, 1)) drop-shadow(0 0 6px rgba(245, 158, 11, 0.85));
  }
}

html[data-theme="light"] g[data-ultimo-escogido="true"] > rect:not(.c-mask) {
  stroke: #d97706 !important;
  fill: rgba(245, 158, 11, 0.16) !important;
  filter: drop-shadow(0 0 10px rgba(217, 119, 6, 0.75)) !important;
}

/* Ícono / sigil dentro del nodo escogido */
g[data-ultimo-escogido="true"] .semantic-sigil circle,
g[data-ultimo-escogido="true"] .semantic-sigil path,
g[data-ultimo-escogido="true"] .sigil-fill {
  stroke: #f59e0b !important;
  fill: #f59e0b !important;
}

/* Textos dentro del nodo escogido */
g[data-ultimo-escogido="true"] text.t-primary {
  font-weight: 700 !important;
}

g[data-ultimo-escogido="true"] text[data-detail="fine"] {
  fill: #fbbf24 !important;
  font-weight: 700 !important;
}

html[data-theme="light"] g[data-ultimo-escogido="true"] text[data-detail="fine"] {
  fill: #b45309 !important;
}
"""


JS_SCRIPT_TEMPLATE = r"""
<style>
__CSS__
</style>
<script>
(function() {
  var GUIA_MAP = __GUIA_JSON__;
  window.__SIGUIENTE_FLUJO = __SIGUIENTE_FLUJO_JSON__;
  window.__ANTERIOR_FLUJO = __ANTERIOR_FLUJO_JSON__;
  window.__VOLVER_CENTROS_URL = "__VOLVER_CENTROS_URL__";

  window.__guiaMaxUnlocked = window.__guiaMaxUnlocked || 0;
  window.__guiaChecks = window.__guiaChecks || {};
  window.__ultimoPasoEscogido = null;

  // Obtener la lista ordenada de ids de nodos del flujo actual
  function obtenerIdsNodosDiagrama() {
    var svg = document.querySelector('.diagram-container > svg') || document.querySelector('svg');
    if (!svg) return [];
    var nodes = svg.querySelectorAll('g[data-node-id]');
    var ids = [];
    for (var i = 0; i < nodes.length; i++) {
      var nId = nodes[i].getAttribute('data-node-id');
      if (nId && ids.indexOf(nId) === -1) {
        ids.push(nId);
      }
    }
    return ids;
  }

  // Claves de almacenamiento para progreso persistente
  function obtenerStorageKeys() {
    var path = window.location.pathname || 'default';
    return {
      current: 'archify_paso_actual_' + path,
      max: 'archify_paso_max_' + path,
      legacy: 'archify_ultimo_paso_' + path
    };
  }

  // Marcar en el SVG qué pasos están completados (coloreados), cuál es el actual (destacado) y cuáles están pendientes (sin colorear)
  function actualizarProgresoDiagrama(nodeIdForzado) {
    var svg = document.querySelector('.diagram-container > svg') || document.querySelector('svg');
    if (!svg) return;

    var nodeIds = obtenerIdsNodosDiagrama();
    if (!nodeIds.length) return;

    var keys = obtenerStorageKeys();
    var currentId = nodeIdForzado;

    if (!currentId) {
      try {
        currentId = localStorage.getItem(keys.current) || sessionStorage.getItem(keys.legacy);
      } catch (_) {}
    }

    // Por defecto colorear el primer paso si el usuario entra por primera vez
    if (!currentId || nodeIds.indexOf(currentId) === -1) {
      currentId = nodeIds[0];
    }

    var currIdx = nodeIds.indexOf(currentId);
    if (currIdx === -1) currIdx = 0;

    var maxIdx = 0;
    try {
      var rawMax = localStorage.getItem(keys.max);
      maxIdx = rawMax !== null ? parseInt(rawMax, 10) : 0;
    } catch (_) {}
    if (isNaN(maxIdx) || maxIdx < currIdx) {
      maxIdx = currIdx;
    }

    // Guardar para que al volver sepan dónde se quedaron
    try {
      localStorage.setItem(keys.current, currentId);
      localStorage.setItem(keys.max, String(maxIdx));
      sessionStorage.setItem(keys.legacy, currentId);
    } catch (_) {}

    window.__ultimoPasoEscogido = currentId;
    window.__guiaMaxUnlocked = Math.max(window.__guiaMaxUnlocked || 0, maxIdx);

    // Asignar data-step-state a cada nodo:
    // - index === currIdx: current (resaltado ámbar)
    // - index <= maxIdx: completed (coloreado nativo)
    // - index > maxIdx: pending (sin color, gris neutro discontinuo)
    for (var i = 0; i < nodeIds.length; i++) {
      var nId = nodeIds[i];
      var gNode = svg.querySelector('g[data-node-id="' + nId + '"]');
      if (!gNode) continue;

      if (i === currIdx) {
        gNode.setAttribute('data-step-state', 'current');
        gNode.setAttribute('data-ultimo-escogido', 'true');
      } else if (i <= maxIdx) {
        gNode.setAttribute('data-step-state', 'completed');
        gNode.removeAttribute('data-ultimo-escogido');
      } else {
        gNode.setAttribute('data-step-state', 'pending');
        gNode.removeAttribute('data-ultimo-escogido');
      }
    }

    // Asignar data-step-edge a las flechas: completed (verde continuo) vs pending (gris discontinuo)
    var edgePaths = svg.querySelectorAll('path[data-edge-from][data-edge-to]');
    for (var e = 0; e < edgePaths.length; e++) {
      var edge = edgePaths[e];
      var toId = edge.getAttribute('data-edge-to');
      var toIdx = nodeIds.indexOf(toId);
      if (toIdx !== -1 && toIdx <= maxIdx) {
        edge.setAttribute('data-step-edge', 'completed');
      } else {
        edge.setAttribute('data-step-edge', 'pending');
      }
    }
  }

  function marcarUltimoPasoEnDiagrama(nodeId) {
    if (!nodeId) return;
    actualizarProgresoDiagrama(nodeId);
  }

  window.reiniciarProgresoDiagrama = function() {
    var keys = obtenerStorageKeys();
    try {
      localStorage.removeItem(keys.current);
      localStorage.removeItem(keys.max);
      sessionStorage.removeItem(keys.legacy);
    } catch (_) {}
    window.__guiaMaxUnlocked = 0;
    var nodeIds = obtenerIdsNodosDiagrama();
    if (nodeIds.length) {
      window.irAPaso(nodeIds[0]);
    } else {
      actualizarProgresoDiagrama();
    }
  };

  // Integrar el .toolbar dentro de .header para que nunca choque con .flow-nav-top ni con h1
  function acomodarHeaderPagina() {
    var header = document.querySelector('.container > .header');
    var toolbar = document.querySelector('body > .toolbar');
    if (header && toolbar && toolbar.parentNode !== header) {
      header.appendChild(toolbar);
    }
  }

  function neutralizarCamaraArchify() {
    if (window.Archify && window.Archify.view) {
      window.Archify.view.reveal = function() {
        mantenerFlujoCompleto();
        return false;
      };
      if (typeof window.Archify.view.frameDesktop === 'function') {
        window.Archify.view.frameDesktop = function() { return false; };
      }
    }
  }

  // Mantener el flujo BPM al 100% (sin zoom automático de Archify ni estrechamiento de contenedor)
  function mantenerFlujoCompleto() {
    neutralizarCamaraArchify();
    if (window.Archify && window.Archify.view && typeof window.Archify.view.reset === 'function') {
      try {
        window.Archify.view.reset({ automatic: true });
      } catch (_) {}
    }

    try {
      document.documentElement.removeAttribute('data-reader-narrow');
      document.documentElement.removeAttribute('data-reader-overflow');
      document.documentElement.style.removeProperty('--archify-reader-width');
      document.documentElement.style.removeProperty('--archify-diagram-max-width');
    } catch (_) {}

    var svg = document.querySelector('.diagram-container > svg');
    if (svg) {
      svg.style.setProperty('transform', 'none', 'important');
      svg.style.setProperty('clip-path', 'none', 'important');
      svg.removeAttribute('data-view-scale');
    }
  }

  function estaEnPresentacion() {
    return document.documentElement.getAttribute('data-present') === 'true' ||
           !!document.fullscreenElement ||
           !!document.webkitFullscreenElement ||
           !!document.mozFullScreenElement ||
           !!document.msFullscreenElement;
  }

  function obtenerEstadoValidacionPaso(nodeId) {
    if (!nodeId || !GUIA_MAP[nodeId]) return { total: 0, checked: 0, pendientes: 0, completo: true };
    var inst = GUIA_MAP[nodeId].instrucciones || [];
    var total = inst.length;
    if (total === 0) return { total: 0, checked: 0, pendientes: 0, completo: true };
    var checks = (window.__guiaChecks && window.__guiaChecks[nodeId]) || {};
    var checked = 0;
    for (var i = 0; i < total; i++) {
      if (checks[i]) checked++;
    }
    return {
      total: total,
      checked: checked,
      pendientes: total - checked,
      completo: checked === total
    };
  }

  function asegurarOverlayConfirmacion(chip) {
    var overlay = chip.querySelector(':scope > .guia-confirm-overlay');
    if (overlay) return overlay;

    var oldOverlay = chip.querySelector('.guia-confirm-overlay');
    if (oldOverlay) oldOverlay.remove();

    overlay = document.createElement('div');
    overlay.className = 'guia-confirm-overlay';
    overlay.hidden = true;
    overlay.setAttribute('hidden', '');
    overlay.innerHTML = '<div class="guia-confirm-modal" role="dialog" aria-modal="true">' +
      '<div class="guia-confirm-header">' +
      '<span class="guia-confirm-icon">⚠️</span>' +
      '<h4 class="guia-confirm-title">Validación de pasos</h4>' +
      '</div>' +
      '<p class="guia-confirm-body">' +
      'Aún tienes <strong id="guia-confirm-pendientes">0</strong> pasos sin marcar en esta etapa.' +
      '</p>' +
      '<p class="guia-confirm-question">¿Deseas pasar sin validar los pasos o quedarte para seguir validando?</p>' +
      '<div class="guia-confirm-actions">' +
      '<button type="button" class="btn-confirm-seguir" id="btn-confirm-seguir">Seguir validando</button>' +
      '<button type="button" class="btn-confirm-pasar" id="btn-confirm-pasar">Pasar sin validar →</button>' +
      '</div>' +
      '</div>';

    chip.appendChild(overlay);

    var btnSeguir = overlay.querySelector('#btn-confirm-seguir');
    if (btnSeguir) {
      btnSeguir.addEventListener('click', function(e) {
        e.stopPropagation();
        cerrarModalConfirmacionValidacion();
        resaltarFilasPendientes();
      });
    }

    var btnPasar = overlay.querySelector('#btn-confirm-pasar');
    if (btnPasar) {
      btnPasar.addEventListener('click', function(e) {
        e.stopPropagation();
        var callback = window.__confirmValidationCallback;
        cerrarModalConfirmacionValidacion();
        if (typeof callback === 'function') {
          callback();
        }
      });
    }

    overlay.addEventListener('click', function(e) {
      if (e.target === overlay) {
        e.stopPropagation();
        cerrarModalConfirmacionValidacion();
        resaltarFilasPendientes();
      }
    });

    return overlay;
  }

  function mostrarModalConfirmacionValidacion(pendientes, total, onConfirmPasar) {
    var chip = document.getElementById('focus-chip');
    if (!chip) return;
    var overlay = asegurarOverlayConfirmacion(chip);
    var pElem = overlay.querySelector('#guia-confirm-pendientes');
    if (pElem) {
      pElem.textContent = pendientes + (total ? (' de ' + total) : '');
    }
    window.__confirmValidationCallback = onConfirmPasar;
    overlay.hidden = false;
    overlay.removeAttribute('hidden');
    var btnSeguir = overlay.querySelector('#btn-confirm-seguir');
    if (btnSeguir) btnSeguir.focus();
  }

  function cerrarModalConfirmacionValidacion() {
    var chip = document.getElementById('focus-chip');
    if (!chip) return;
    var overlay = chip.querySelector('.guia-confirm-overlay');
    if (overlay) {
      overlay.hidden = true;
      overlay.setAttribute('hidden', '');
    }
    window.__confirmValidationCallback = null;
  }

  function resaltarFilasPendientes() {
    var rows = document.querySelectorAll('.guia-fila-paso:not(.completada)');
    rows.forEach(function(row) {
      row.classList.remove('pendiente-atencion');
      void row.offsetWidth;
      row.classList.add('pendiente-atencion');
    });
    if (rows.length > 0) {
      try {
        rows[0].scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      } catch (_) {}
    }
  }

  function toggleValidarTodosPaso(nodeId) {
    if (!nodeId || !GUIA_MAP[nodeId]) return;
    var inst = GUIA_MAP[nodeId].instrucciones || [];
    if (!inst.length) return;
    window.__guiaChecks = window.__guiaChecks || {};
    window.__guiaChecks[nodeId] = window.__guiaChecks[nodeId] || {};
    var val = obtenerEstadoValidacionPaso(nodeId);
    var nuevoEstado = !val.completo;
    for (var r = 0; r < inst.length; r++) {
      window.__guiaChecks[nodeId][r] = nuevoEstado;
    }
    actualizarModalGuia();
  }

  window.irAPaso = function(targetNodeId, forzarSinValidar) {
    if (!targetNodeId) return;
    var idElem = document.getElementById('focus-id');
    var currentId = idElem ? (idElem.textContent || '').trim() : '';
    var nodeIds = obtenerIdsNodosDiagrama();
    if (!nodeIds.length) nodeIds = Object.keys(GUIA_MAP);
    var currentIndex = nodeIds.indexOf(currentId);
    var targetIndex = nodeIds.indexOf(targetNodeId);

    if (targetIndex > currentIndex && !forzarSinValidar) {
      var val = obtenerEstadoValidacionPaso(currentId);
      if (!val.completo) {
        mostrarModalConfirmacionValidacion(val.pendientes, val.total, function() {
          window.irAPaso(targetNodeId, true);
        });
        return;
      }
    }

    actualizarProgresoDiagrama(targetNodeId);
    var nodeElem = document.querySelector('[data-node-id="' + targetNodeId + '"]');
    if (nodeElem) {
      nodeElem.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
      setTimeout(function() {
        mantenerFlujoCompleto();
        actualizarModalGuia();
        actualizarProgresoDiagrama(targetNodeId);
      }, 30);
    }
  };

  window.navegarPaso = function(offset, forzarSinValidar) {
    var idElem = document.getElementById('focus-id');
    if (!idElem) return;
    var currentId = (idElem.textContent || '').trim();
    var nodeIds = obtenerIdsNodosDiagrama();
    if (!nodeIds.length) nodeIds = Object.keys(GUIA_MAP);
    var currentIndex = nodeIds.indexOf(currentId);
    if (currentIndex === -1) return;

    if (offset > 0 && !forzarSinValidar) {
      var val = obtenerEstadoValidacionPaso(currentId);
      if (!val.completo) {
        mostrarModalConfirmacionValidacion(val.pendientes, val.total, function() {
          window.navegarPaso(offset, true);
        });
        return;
      }
    }

    var nextIndex = currentIndex + offset;
    if (nextIndex >= 0 && nextIndex < nodeIds.length) {
      var targetNodeId = nodeIds[nextIndex];
      actualizarProgresoDiagrama(targetNodeId);
      var nodeElem = document.querySelector('[data-node-id="' + targetNodeId + '"]');
      if (nodeElem) {
        nodeElem.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
        setTimeout(function() {
          mantenerFlujoCompleto();
          actualizarModalGuia();
          actualizarProgresoDiagrama(targetNodeId);
        }, 30);
      }
    }
  };

  function desglosarValorYEjemplo(item) {
    if (item.ejemplo !== undefined && item.ejemplo !== null && String(item.ejemplo).trim() !== '') {
      return { valor: item.valor || '', ejemplo: item.ejemplo };
    }
    var raw = (item.valor || '').trim();
    if (!raw) return { valor: '', ejemplo: '-' };

    var rLower = raw.toLowerCase();
    if (rLower.indexOf('dejar en blanco') !== -1 || rLower.indexOf('totalmente vacío') !== -1) {
      return { valor: '(Vacío)', ejemplo: 'Dejar en blanco para nuevo' };
    }
    if (rLower === 'clic en «crear nrc»' || rLower.indexOf('crear nrc') !== -1) {
      return { valor: 'Crear NRC', ejemplo: 'Clic en botón azul' };
    }
    if (rLower.indexOf('botón «guardar»') !== -1 || rLower.indexOf('f10') !== -1) {
      return { valor: 'F10 (Guardar)', ejemplo: 'Presionar F10 o botón Guardar' };
    }

    var matchEj = raw.match(/^([^(]+?)\s*\((ej\.?|ejemplo:?)\s*([^)]+)\)$/i);
    if (matchEj) {
      return { valor: matchEj[1].trim(), ejemplo: matchEj[3].trim() };
    }

    var matchParen = raw.match(/^([^(]+?)\s*\((o\s+[^)]+)\)$/i);
    if (matchParen) {
      return { valor: matchParen[1].trim(), ejemplo: matchParen[2].trim() };
    }

    var matchSimpleParen = raw.match(/^([A-Za-z0-9_\-\s]{1,12})\s*\(([^)]+)\)$/);
    if (matchSimpleParen && matchSimpleParen[2].length < 35) {
      return { valor: matchSimpleParen[1].trim(), ejemplo: matchSimpleParen[2].trim() };
    }

    return { valor: raw, ejemplo: '-' };
  }

  function renderGuiaHtml(info, nodeId) {
    if (!info) return '';
    var stepKeys = Object.keys(GUIA_MAP);
    var currentIndex = stepKeys.indexOf(nodeId);
    var totalSteps = stepKeys.length;
    var hasPrev = currentIndex > 0;
    var hasNext = currentIndex < totalSteps - 1;
    var nextNode = hasNext ? stepKeys[currentIndex + 1] : null;
    var nextTitle = nextNode && GUIA_MAP[nextNode] ? (GUIA_MAP[nextNode].fase || GUIA_MAP[nextNode].pantalla || 'Paso siguiente') : '';

    var maxUnlocked = (typeof window.__guiaMaxUnlocked === 'number') ? window.__guiaMaxUnlocked : 0;
    if (currentIndex > maxUnlocked) {
      window.__guiaMaxUnlocked = currentIndex;
      maxUnlocked = currentIndex;
    }

    var html = '<div class="guia-body-scroll">';

    if (totalSteps > 1) {
      var progressPct = Math.round(((currentIndex + 1) / totalSteps) * 100);
      html += '<div class="guia-stepper-wrap">';
      html += '<div class="guia-stepper-track" role="tablist" aria-label="Fases del flujo">';
      stepKeys.forEach(function(k, idx) {
        var sInfo = GUIA_MAP[k];
        var isAct = (k === nodeId);
        var isPast = (idx < currentIndex);
        var isLocked = (idx > maxUnlocked);
        var label = sInfo.fase ? sInfo.fase.replace(/^Paso\s*\d+:\s*/i, '') : (sInfo.pantalla || ('Paso ' + (idx + 1)));

        var pillClass = 'guia-step-pill';
        if (isAct) pillClass += ' active';
        else if (isPast) pillClass += ' past';
        else if (isLocked) pillClass += ' locked';

        var badgeTxt;
        if (isPast) badgeTxt = '✓';
        else if (isLocked) badgeTxt = '🔒 ' + (idx + 1);
        else badgeTxt = (idx + 1);

        if (isLocked) {
          html += '<button type="button" class="' + pillClass + '" disabled title="Paso ' + (idx + 1) + ' bloqueado. Haz clic en Siguiente para avanzar.">';
          html += '<span class="pill-badge">' + badgeTxt + '</span>';
          html += '<span>' + escapeHtml(label) + '</span>';
          html += '</button>';
        } else {
          html += '<button type="button" class="' + pillClass + '" data-ir-paso="' + escapeHtml(k) + '" title="Ir al paso ' + (idx + 1) + ': ' + escapeHtml(label) + '">';
          html += '<span class="pill-badge">' + badgeTxt + '</span>';
          html += '<span>' + escapeHtml(label) + '</span>';
          html += '</button>';
        }

        if (idx < totalSteps - 1) {
          var arrowClass = 'stepper-arrow' + (isPast ? ' past' : (isLocked ? ' locked' : ''));
          html += '<span class="' + arrowClass + '">›</span>';
        }
      });
      html += '</div>';
      html += '<div class="guia-stepper-progress"><div class="guia-progress-fill" style="width:' + progressPct + '%;"></div></div>';
      html += '</div>';
    }

    html += '<div class="guia-fase-hero">';
    html += '<div class="guia-fase-main">';
    if (info.pantalla) {
      html += '<span class="guia-pantalla-pill">' + escapeHtml(info.pantalla) + '</span>';
    }
    if (info.fase) {
      html += '<h3 class="guia-fase-title">' + escapeHtml(info.fase) + '</h3>';
    }
    html += '</div>';

    html += '<div class="guia-fase-actions">';
    if (info.instrucciones && info.instrucciones.length > 0) {
      var valPaso = obtenerEstadoValidacionPaso(nodeId);
      var toggleBtnClass = 'btn-toggle-validar-todos' + (valPaso.completo ? ' todos-completos' : '');
      var toggleBtnTxt = valPaso.completo ? '↺ Desmarcar todos' : '☑ Validar todo';
      var toggleBtnTitle = valPaso.completo ? 'Desmarcar todos los pasos de esta etapa' : 'Marcar todos los pasos de esta etapa como completados';
      html += '<button type="button" class="' + toggleBtnClass + '" data-toggle-todos="' + escapeHtml(nodeId) + '" title="' + toggleBtnTitle + '">' + toggleBtnTxt + '</button>';
    }
    if (info.hito) {
      html += '<div class="guia-hito-badge">🎯 ' + escapeHtml(info.hito) + '</div>';
    }
    html += '</div>';
    html += '</div>';

    if (info.instrucciones && info.instrucciones.length > 0) {
      html += '<div class="guia-tabla-wrap"><table class="guia-tabla">';
      html += '<thead><tr><th class="th-num">#</th><th>Campo / Acción</th><th>Valor</th><th>Ejemplo</th><th>Tipo</th><th>Detalle Operativo</th></tr></thead>';
      html += '<tbody>';
      
      var checks = (window.__guiaChecks && window.__guiaChecks[nodeId]) || {};

      info.instrucciones.forEach(function(item, rIdx) {
        var rowNum = rIdx + 1;
        var isChecked = !!checks[rIdx];
        var isCritico = (item.tipo || '').toLowerCase().indexOf('crítico') !== -1 || (item.tipo || '').toLowerCase().indexOf('guardado') !== -1;
        var tagClass = isCritico ? 'guia-tipo-tag critico' : 'guia-tipo-tag';
        
        var desglosado = desglosarValorYEjemplo(item);
        var valorTxt = desglosado.valor || '';
        var ejemploTxt = desglosado.ejemplo || '';
        var vLower = valorTxt.toLowerCase();

        var valClass = 'guia-valor';
        if (valorTxt.length > 26) {
          valClass += ' valor-largo';
        }
        var valorDisplay = escapeHtml(valorTxt);
        if (vLower.indexOf('vacío') !== -1 || vLower.indexOf('blanco') !== -1) {
          valClass += ' valor-vacio';
          valorDisplay = '⚠️ ' + valorDisplay;
        } else if (vLower.indexOf('clic') !== -1 || vLower.indexOf('guardar') !== -1 || vLower.indexOf('f10') !== -1) {
          valClass += ' valor-accion';
          valorDisplay = '👆 ' + valorDisplay;
        }

        var rowClass = 'guia-fila-paso' + (isChecked ? ' completada' : '');

        html += '<tr class="' + rowClass + '" data-row-idx="' + rIdx + '">';
        html += '<td class="guia-td-num">';
        html += '<button type="button" class="guia-check-btn" data-check-row="' + rIdx + '" title="Paso ' + rowNum + ': Clic para marcar/desmarcar como completado">';
        html += '<span class="num-badge">' + (isChecked ? '✓' : rowNum) + '</span>';
        html += '</button>';
        html += '</td>';
        html += '<td class="guia-campo">' + escapeHtml(item.campo || '') + '</td>';
        html += '<td><span class="' + valClass + '">' + valorDisplay + '</span></td>';
        html += '<td class="guia-ejemplo">' + (ejemploTxt && ejemploTxt !== '-' ? ('<span class="ejemplo-badge">' + escapeHtml(ejemploTxt) + '</span>') : '<span style="opacity:0.4;">—</span>') + '</td>';
        html += '<td><span class="' + tagClass + '">' + escapeHtml(item.tipo || '') + '</span></td>';
        html += '<td class="guia-detalle">' + escapeHtml(item.detalle || '') + '</td>';
        html += '</tr>';
      });
      html += '</tbody></table></div>';
    }

    html += '</div>';

    if (totalSteps > 1) {
      var pct = Math.round(((currentIndex + 1) / totalSteps) * 100);
      var numFilas = (info.instrucciones && info.instrucciones.length) || 0;
      var statusExtra = numFilas > 5 ? (' · ' + numFilas + ' pasos') : '';
      html += '<div class="guia-footer-sticky">';
      html += '<button type="button" class="guia-nav-btn btn-pie-prev" ' + (hasPrev ? 'data-nav-paso="-1"' : 'disabled') + ' title="Volver al paso anterior">← Anterior</button>';
      html += '<div class="guia-pie-status">Paso ' + (currentIndex + 1) + ' de ' + totalSteps + ' (' + pct + '%)' + statusExtra + '</div>';
      if (hasNext) {
        html += '<button type="button" class="guia-nav-btn btn-pie-next primary" data-nav-paso="1" title="Avanzar al siguiente paso">';
        html += '<span>Siguiente</span>';
        html += '<span class="btn-next-arrow">→</span>';
        html += '</button>';
      } else {
        if (window.__SIGUIENTE_FLUJO && window.__SIGUIENTE_FLUJO.url) {
          html += '<a href="' + escapeHtml(window.__SIGUIENTE_FLUJO.url) + '" class="guia-nav-btn btn-pie-next primary" style="text-decoration:none;" title="Pasar al siguiente flujo">';
          html += '<span>Siguiente flujo</span>';
          html += '<span class="btn-next-arrow">→</span>';
          html += '</a>';
        } else {
          html += '<a href="' + escapeHtml(window.__VOLVER_CENTROS_URL || '#') + '" class="guia-nav-btn btn-pie-next" style="text-decoration:none;" title="Volver a la galería de Centros">';
          html += '<span>Finalizar</span>';
          html += '<span class="btn-next-arrow">✓</span>';
          html += '</a>';
        }
      }
      html += '</div>';
    }

    return html;
  }

  function escapeHtml(str) {
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  function asegurarBarraControles(chip) {
    var topbar = chip.querySelector(':scope > .guia-modal-topbar');
    if (topbar) return;

    var oldTopbar = chip.querySelector('.guia-modal-topbar');
    if (oldTopbar) oldTopbar.remove();

    topbar = document.createElement('div');
    topbar.className = 'guia-modal-topbar';
    topbar.innerHTML = '<div class="guia-modal-brand">' +
      '<span class="guia-brand-badge">BANNER TEST</span>' +
      '<span class="guia-brand-title">Guía Operativa Paso a Paso</span>' +
      '</div>' +
      '<div class="guia-topbar-actions">' +
      '<button type="button" class="chip-btn-ctrl btn-reset-progreso" title="Reiniciar progreso del flujo al Paso 1">↺ <span class="btn-reset-txt">Reiniciar</span></button>' +
      '<button type="button" class="chip-btn-ctrl btn-copy" title="Copiar enlace directo a este paso">🔗 <span class="btn-copy-txt">Copiar enlace</span></button>' +
      '<button type="button" class="chip-btn-close" title="Cerrar modal (Esc)">✕</button>' +
      '</div>';

    chip.insertBefore(topbar, chip.firstChild);

    var btnReset = topbar.querySelector('.btn-reset-progreso');
    if (btnReset) {
      btnReset.addEventListener('click', function(e) {
        e.stopPropagation();
        window.reiniciarProgresoDiagrama();
      });
    }

    var btnCopy = topbar.querySelector('.btn-copy');
    btnCopy.addEventListener('click', function(e) {
      e.stopPropagation();
      var idElem = document.getElementById('focus-id');
      var nodeId = (idElem ? idElem.textContent : '').trim();
      var base = window.location.href.split('#')[0];
      var url = nodeId ? (base + '#focus=' + encodeURIComponent(nodeId)) : base;
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(url).then(function() {
          var txt = topbar.querySelector('.btn-copy-txt');
          var orig = txt.textContent;
          txt.textContent = '¡Copiado!';
          setTimeout(function() { txt.textContent = orig; }, 1600);
        });
      }
    });

    var btnClose = topbar.querySelector('.chip-btn-close');
    btnClose.addEventListener('click', function(e) {
      e.stopPropagation();
      cerrarModalGuia();
    });
  }

  function asegurarBackdrop() {
    var b = document.getElementById('guia-modal-backdrop');
    if (!b) {
      b = document.createElement('div');
      b.id = 'guia-modal-backdrop';
      b.className = 'guia-modal-backdrop';
      b.setAttribute('aria-hidden', 'true');
      b.addEventListener('click', function(e) {
        e.stopPropagation();
        cerrarModalGuia();
      });
      document.body.appendChild(b);
    }
    return b;
  }

  function cerrarModalGuia() {
    cerrarModalConfirmacionValidacion();
    var chip = document.getElementById('focus-chip');
    var b = document.getElementById('guia-modal-backdrop');
    if (b) b.classList.remove('active');
    document.body.classList.remove('has-guia-open');
    if (chip) {
      chip.classList.remove('tiene-guia');
      var clearBtn = document.getElementById('btn-focus-clear');
      if (clearBtn) clearBtn.click();
      else chip.hidden = true;
    }
    mantenerFlujoCompleto();

    // Mantener seleccionado en el diagrama el último paso escogido con su color distintivo
    if (window.__ultimoPasoEscogido) {
      marcarUltimoPasoEnDiagrama(window.__ultimoPasoEscogido);
      setTimeout(function() {
        marcarUltimoPasoEnDiagrama(window.__ultimoPasoEscogido);
      }, 40);
      setTimeout(function() {
        marcarUltimoPasoEnDiagrama(window.__ultimoPasoEscogido);
      }, 140);
    }
  }

  function actualizarModalGuia() {
    var chip = document.getElementById('focus-chip');
    var idElem = document.getElementById('focus-id');
    if (!chip || !idElem) return;

    asegurarBarraControles(chip);
    asegurarOverlayConfirmacion(chip);

    var nodeId = (idElem.textContent || '').trim();
    var card = document.getElementById('guia-operativa-box');

    if (!nodeId || !GUIA_MAP[nodeId]) {
      if (card) card.remove();
      chip.classList.remove('tiene-guia');
      var b = document.getElementById('guia-modal-backdrop');
      if (b) b.classList.remove('active');
      document.body.classList.remove('has-guia-open');
      return;
    }

    marcarUltimoPasoEnDiagrama(nodeId);

    var info = GUIA_MAP[nodeId];
    var prevScroll = 0;
    var prevBodyScroll = 0;
    if (!card) {
      card = document.createElement('div');
      card.id = 'guia-operativa-box';
      card.className = 'guia-operativa-card';
      var copy = chip.querySelector('.relationship-lens-copy');
      if (copy) {
        copy.appendChild(card);
      } else {
        chip.appendChild(card);
      }
    } else {
      var oldWrap = card.querySelector('.guia-tabla-wrap');
      if (oldWrap) prevScroll = oldWrap.scrollTop;
      var oldBody = card.querySelector('.guia-body-scroll');
      if (oldBody) prevBodyScroll = oldBody.scrollTop;
    }

    chip.hidden = false;
    chip.removeAttribute('hidden');
    chip.classList.add('tiene-guia');
    chip.classList.remove('docked-right', 'floating-modal', 'chip-minimized');
    chip.style.removeProperty('top');
    chip.style.removeProperty('left');

    var isPresent = estaEnPresentacion();
    var b = asegurarBackdrop();
    if (!isPresent) {
      b.classList.add('active');
    } else {
      b.classList.remove('active');
    }
    document.body.classList.add('has-guia-open');

    var titleElem = chip.querySelector('.guia-brand-title');
    if (titleElem && info && info.titulo) {
      titleElem.textContent = info.titulo;
    }

    card.innerHTML = renderGuiaHtml(info, nodeId);

    var tablaWrap = card.querySelector('.guia-tabla-wrap');
    if (tablaWrap && prevScroll > 0) {
      tablaWrap.scrollTop = prevScroll;
    }
    var scrollBody = card.querySelector('.guia-body-scroll');
    if (scrollBody && prevBodyScroll > 0) {
      scrollBody.scrollTop = prevBodyScroll;
    }

    setTimeout(function() {
      mantenerFlujoCompleto();
      var activePill = card.querySelector('.guia-step-pill.active');
      if (activePill) {
        try {
          activePill.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' });
        } catch (_) {}
      }
    }, 50);
  }

  document.addEventListener('DOMContentLoaded', function() {
    acomodarHeaderPagina();

    // Forzar nivel de detalle completo (full) para que los textos inferiores (data-detail="fine") se muestren en todos los nodos
    var dc = document.querySelector('.diagram-container');
    if (dc) {
      dc.setAttribute('data-detail-level', 'full');
    }

    // Interceptar Archify.view.reveal para evitar que haga zoom y descoloque el flujo BPM
    neutralizarCamaraArchify();

    // Observador continuo para neutralizar estilos de cámara inline en el SVG
    var svg = document.querySelector('.diagram-container > svg');
    if (svg && window.MutationObserver) {
      var svgObserver = new MutationObserver(function() {
        if (svg.style.transform && svg.style.transform !== 'none') {
          svg.style.setProperty('transform', 'none', 'important');
        }
        if (svg.style.clipPath && svg.style.clipPath !== 'none') {
          svg.style.setProperty('clip-path', 'none', 'important');
        }
      });
      svgObserver.observe(svg, { attributes: true, attributeFilter: ['style', 'data-view-scale'] });
    }

    // Observador para neutralizar el reductor de ancho adaptativo de Archify y detectar modo presentación
    if (window.MutationObserver) {
      var htmlObserver = new MutationObserver(function() {
        if (estaEnPresentacion()) {
          cerrarModalGuia();
        }
        if (document.documentElement.hasAttribute('data-reader-narrow')) {
          document.documentElement.removeAttribute('data-reader-narrow');
        }
        if (document.documentElement.hasAttribute('data-reader-overflow')) {
          document.documentElement.removeAttribute('data-reader-overflow');
        }
        if (document.documentElement.style.getPropertyValue('--archify-reader-width')) {
          document.documentElement.style.removeProperty('--archify-reader-width');
        }
        if (document.documentElement.style.getPropertyValue('--archify-diagram-max-width')) {
          document.documentElement.style.removeProperty('--archify-diagram-max-width');
        }
      });
      htmlObserver.observe(document.documentElement, { attributes: true, attributeFilter: ['data-reader-narrow', 'data-reader-overflow', 'data-present', 'style'] });
    }

    var btnPresent = document.getElementById('btn-present');
    function syncPresentButton() {
      var isPresent = estaEnPresentacion();
      var b = document.getElementById('guia-modal-backdrop');
      if (b) {
        if (isPresent) {
          b.classList.remove('active');
        } else {
          var chip = document.getElementById('focus-chip');
          if (chip && !chip.hidden && chip.classList.contains('tiene-guia')) {
            b.classList.add('active');
          }
        }
      }
    }
    if (btnPresent) {
      btnPresent.addEventListener('click', function() {
        if (!document.fullscreenElement) {
          if (document.documentElement.requestFullscreen) {
            document.documentElement.requestFullscreen().catch(function(_) {});
          }
        } else {
          if (document.exitFullscreen) {
            document.exitFullscreen().catch(function(_) {});
          }
        }
        setTimeout(function() {
          syncPresentButton();
        }, 80);
      });
    }

    document.addEventListener('fullscreenchange', function() {
      if (!document.fullscreenElement && window.Archify && window.Archify.presentation) {
        if (typeof window.Archify.presentation.exit === 'function') {
          window.Archify.presentation.exit();
        }
      }
      setTimeout(syncPresentButton, 60);
    });

    document.addEventListener('webkitfullscreenchange', function() {
      setTimeout(syncPresentButton, 60);
    });

    window.addEventListener('resize', function() {
      syncPresentButton();
    });

    var target = document.getElementById('focus-id');
    if (target) {
      var observer = new MutationObserver(actualizarModalGuia);
      observer.observe(target, { childList: true, characterData: true, subtree: true });
    }

    document.addEventListener('click', function(e) {
      var btnIr = e.target.closest('[data-ir-paso]');
      if (btnIr) {
        e.preventDefault();
        e.stopPropagation();
        var targetId = btnIr.getAttribute('data-ir-paso');
        window.irAPaso(targetId);
        return;
      }

      var btnNav = e.target.closest('[data-nav-paso]');
      if (btnNav) {
        e.preventDefault();
        e.stopPropagation();
        var offset = parseInt(btnNav.getAttribute('data-nav-paso'), 10);
        window.navegarPaso(offset);
        return;
      }

      var btnToggleTodos = e.target.closest('[data-toggle-todos]');
      if (btnToggleTodos) {
        e.preventDefault();
        e.stopPropagation();
        var nId = btnToggleTodos.getAttribute('data-toggle-todos');
        toggleValidarTodosPaso(nId);
        return;
      }

      var btnCheck = e.target.closest('[data-check-row]');
      if (btnCheck) {
        e.preventDefault();
        e.stopPropagation();
        var idElem = document.getElementById('focus-id');
        var nodeId = (idElem ? idElem.textContent : '').trim();
        var rowIdx = parseInt(btnCheck.getAttribute('data-check-row'), 10);
        window.__guiaChecks = window.__guiaChecks || {};
        window.__guiaChecks[nodeId] = window.__guiaChecks[nodeId] || {};
        window.__guiaChecks[nodeId][rowIdx] = !window.__guiaChecks[nodeId][rowIdx];
        actualizarModalGuia();
        return;
      }

      var trPaso = e.target.closest('tr.guia-fila-paso');
      if (trPaso && !e.target.closest('button, a, input')) {
        var rowIdx = parseInt(trPaso.getAttribute('data-row-idx'), 10);
        var idElem = document.getElementById('focus-id');
        var nodeId = (idElem ? idElem.textContent : '').trim();
        window.__guiaChecks = window.__guiaChecks || {};
        window.__guiaChecks[nodeId] = window.__guiaChecks[nodeId] || {};
        window.__guiaChecks[nodeId][rowIdx] = !window.__guiaChecks[nodeId][rowIdx];
        actualizarModalGuia();
        return;
      }

      var node = e.target.closest('[data-node-id]');
      if (node) {
        var nId = node.getAttribute('data-node-id');
        if (nId) {
          marcarUltimoPasoEnDiagrama(nId);
        }
        neutralizarCamaraArchify();
        mantenerFlujoCompleto();
        setTimeout(function() {
          mantenerFlujoCompleto();
          actualizarModalGuia();
          if (nId) marcarUltimoPasoEnDiagrama(nId);
        }, 15);
        setTimeout(function() {
          mantenerFlujoCompleto();
          actualizarModalGuia();
          if (nId) marcarUltimoPasoEnDiagrama(nId);
        }, 70);
        setTimeout(function() {
          mantenerFlujoCompleto();
          if (nId) marcarUltimoPasoEnDiagrama(nId);
        }, 200);
        setTimeout(function() {
          mantenerFlujoCompleto();
          if (nId) marcarUltimoPasoEnDiagrama(nId);
        }, 450);
      }
    });

    document.addEventListener('keydown', function(e) {
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.target.tagName === 'SELECT') return;
      if (e.key === 'Escape') {
        var chip = document.getElementById('focus-chip');
        if (chip) {
          var confirmOverlay = chip.querySelector('.guia-confirm-overlay');
          if (confirmOverlay && !confirmOverlay.hidden) {
            e.preventDefault();
            cerrarModalConfirmacionValidacion();
            resaltarFilasPendientes();
            return;
          }
          if (!chip.hidden && chip.classList.contains('tiene-guia')) {
            e.preventDefault();
            cerrarModalGuia();
            return;
          }
        }
      }
      if (e.altKey && e.key === 'ArrowRight' && window.__SIGUIENTE_FLUJO && window.__SIGUIENTE_FLUJO.url) {
        e.preventDefault();
        window.location.href = window.__SIGUIENTE_FLUJO.url;
        return;
      }
      if (e.altKey && e.key === 'ArrowLeft' && window.__ANTERIOR_FLUJO && window.__ANTERIOR_FLUJO.url) {
        e.preventDefault();
        window.location.href = window.__ANTERIOR_FLUJO.url;
        return;
      }
      var chip = document.getElementById('focus-chip');
      if (!chip || chip.hidden || !chip.classList.contains('tiene-guia')) return;
      if (e.key === 'ArrowRight') {
        e.preventDefault();
        window.navegarPaso(1);
      } else if (e.key === 'ArrowLeft') {
        e.preventDefault();
        window.navegarPaso(-1);
      }
    });

    mantenerFlujoCompleto();

    // Inicializar el progreso: colorear el actual/completados y dejar pendientes los no alcanzados
    actualizarProgresoDiagrama();
    setTimeout(actualizarProgresoDiagrama, 60);
    setTimeout(actualizarProgresoDiagrama, 250);

    actualizarModalGuia();
    if (window.location.hash && window.location.hash.indexOf('focus=') !== -1) {
      var matchFocus = window.location.hash.match(/focus=([^&]+)/);
      if (matchFocus && matchFocus[1]) {
        var hashNodeId = decodeURIComponent(matchFocus[1]);
        marcarUltimoPasoEnDiagrama(hashNodeId);
      }
      setTimeout(function() {
        actualizarModalGuia();
        mantenerFlujoCompleto();
        if (hashNodeId) marcarUltimoPasoEnDiagrama(hashNodeId);
      }, 70);
      setTimeout(function() {
        actualizarModalGuia();
        mantenerFlujoCompleto();
        if (hashNodeId) marcarUltimoPasoEnDiagrama(hashNodeId);
      }, 250);
    }
  });
})();
</script>
"""


# ======================= BLOQUE 2: resolución de la guía (reemplaza obtener_guia_para_slug) =======================
def detectar_script(slug):
    """'computacion-09-script-18-b-tiene-deuda' → '18-B' (antes fallaba: buscaba 'script-18-B' en minúsculas)."""
    m = RE_SCRIPT.search(slug)
    return m.group(1).upper() if m else None


def ids_nodos_en_html(contenido):
    """Ids de los nodos del SVG, en orden. Llamar DESPUÉS de quitar la inyección previa: el JS también
    contiene la cadena data-node-id=" y contaminaría la lista."""
    ids = []
    for m in re.finditer(r'<g\b[^>]*\bdata-node-id="([^"]+)"', contenido):
        if m.group(1) not in ids:
            ids.append(m.group(1))
    return ids


def _guia_curada(slug, id_centro, sid):
    try:
        g = obtener_guia(slug, id_centro)
    except Exception:
        g = None
    if g:
        return g
    if sid:
        for k, v in GUIAS_SCRIPTS.items():
            if str(k).upper() == sid:
                return v
        return None
    limpio = RE_PREFIJO.sub("", slug)  # quita "<centro>-NN-"
    if limpio in GUIAS_BASE:
        return GUIAS_BASE[limpio]
    if slug in GUIAS_BASE:
        return GUIAS_BASE[slug]
    for k, v in GUIAS_BASE.items():
        if k in limpio:
            return v
    return None


def _normalizar(info):
    """Garantiza campo, tipo y detalle en cada fila (la tabla siempre pinta 6 columnas).
    No toca 'ejemplo': si falta, el JS lo deduce de 'valor'."""
    out = dict(info)
    filas = []
    for it in out.get("instrucciones") or []:
        f = dict(it)
        for k, defecto in (("campo", "—"), ("tipo", "Acción"), ("detalle", "—")):
            if not f.get(k):
                f[k] = defecto
        f.setdefault("valor", "")
        filas.append(f)
    out["instrucciones"] = filas
    return out


def _validar_y_ordenar(guia, ids_nodos, slug):
    """Deja solo nodos que existen en el SVG y los ordena como el recorrido (c0, c1… cr). Así el botón
    «Siguiente» nunca apunta a un paso sin nodo y el stepper no se queda trabado."""
    if not ids_nodos:
        return {k: _normalizar(v) for k, v in guia.items()}
    fuera = [k for k in guia if k not in ids_nodos]
    if fuera:
        ADVERTENCIAS.append(f"{slug}: nodos de la guía que no existen en el diagrama (se descartan): {fuera}")
    validas = [k for k in guia if k in ids_nodos]
    if guia and not validas:
        ADVERTENCIAS.append(f"{slug}: ningún nodo de la guía coincide con el diagrama; ids del diagrama: {ids_nodos}")
    elif validas:
        faltan = [n for n in ids_nodos if n not in guia]
        if faltan:
            ADVERTENCIAS.append(f"{slug}: nodos del diagrama sin guía: {faltan}")
    elif not any(s in slug for s in SIN_GUIA_ESPERADO):
        ADVERTENCIAS.append(f"{slug}: sin guía operativa; se verá el pasaporte nativo de Archify")

    def orden(k):
        m = re.search(r"(\d+)$", k)
        return (int(m.group(1)) if m else 10 ** 6, ids_nodos.index(k))

    return {k: _normalizar(guia[k]) for k in sorted(validas, key=orden)}


def obtener_guia_para_slug(slug, id_centro="", ids_nodos=None):
    """Guía {id_de_nodo: ficha} del flujo, validada contra los nodos reales del SVG."""
    sid = detectar_script(slug)
    guia = dict(_guia_curada(slug, id_centro, sid) or {})
    if sid:  # casuísticas: se completan (o se imponen) desde plantillas.py
        generada = guia_casuistica_de(id_centro, sid)
        for nid, info in generada.items():
            curada = guia.get(nid)
            if PRIORIDAD_CASUISTICAS == "plantillas" or not (curada and curada.get("instrucciones")):
                guia[nid] = info
    return _validar_y_ordenar(guia, ids_nodos, slug)


# ======================= BLOQUE 3: navegación (reemplaza construir_navegacion_flujos) =======================
def _listar_flujos(carpeta_diagramas):
    flujos = []
    if not carpeta_diagramas.is_dir():
        return flujos
    for s in sorted(p for p in carpeta_diagramas.glob("[0-9][0-9]-*") if p.is_dir()):
        htmls = sorted(s.glob("*.html"))
        if htmls:
            flujos.append((s, htmls[0]))
    return flujos


def _destino_en_centro(c_id, carpeta_actual, carpeta_centros):
    """Mismo flujo (por slug, no por número) en otro centro; si no existe, su primer flujo; si no, el índice.
    Antes se comparaba la carpeta completa «NN-slug» y, al cambiar la numeración (p. ej. por Ligas),
    caía siempre en el primer flujo: de ahí los saltos raros."""
    flujos = _listar_flujos(carpeta_centros / c_id / "diagramas")
    slug_actual = carpeta_actual.name[3:]
    for s, h in flujos:
        if s.name[3:] == slug_actual:
            return f"../../../{c_id}/diagramas/{s.name}/{h.name}"
    if flujos:
        s, h = flujos[0]
        return f"../../../{c_id}/diagramas/{s.name}/{h.name}"
    return f"../../../index.html#sec-{c_id}"


def _html_nav_bottom(flujo_ant, flujo_sig, url_centros):
    def tarjeta(f, clase, etiqueta):
        if not f:
            texto = "Primer flujo del centro" if clase == "prev" else "Último flujo del centro"
            return (f'<div class="flow-bottom-card {clase} placeholder"><span class="flow-card-badge">{etiqueta}</span>'
                    f'<span class="flow-card-title muted">{texto}</span></div>')
        acento = " primary-accent" if clase == "next" else ""
        meta = f'<span class="flow-card-meta">{html.escape(f["cap"])}</span>' if f["cap"] else ""
        titulo = html.escape(f["titulo"])
        return (f'<a href="{html.escape(f["url"])}" class="flow-bottom-card {clase}{acento}" title="{f["num"]:02d}. {titulo}">'
                f'<span class="flow-card-badge">{etiqueta}</span>'
                f'<span class="flow-card-num-title"><span class="flow-card-num">{f["num"]:02d}</span>'
                f'<span class="flow-card-title">{titulo}</span></span>{meta}</a>')

    return ('<!-- === FLOW NAV BOTTOM === -->\n'
            '<section class="flow-nav-bottom-section" aria-label="Navegación entre flujos">\n'
            '  <div class="flow-bottom-container">\n'
            f'    {tarjeta(flujo_ant, "prev", "← Flujo anterior")}\n'
            f'    <a href="{url_centros}" class="flow-bottom-hub-btn" title="Volver a la galería de Centros">🏛️ Volver a Centros</a>\n'
            f'    {tarjeta(flujo_sig, "next", "Flujo siguiente →")}\n'
            '  </div>\n'
            '</section>\n'
            '<!-- === /FLOW NAV BOTTOM === -->')


def construir_navegacion_flujos(ruta_html):
    """Barra superior, tarjetas inferiores y datos de anterior/siguiente.
    Ruta esperada: centros/<centro>/diagramas/NN-slug/<archivo>.html"""
    carpeta_diagrama = ruta_html.parent
    carpeta_centros = ruta_html.parents[3]
    nombre = ruta_html.parents[2].name
    nombres = {c[0]: c for c in CENTROS_NAV}
    id_centro = nombre if nombre in nombres else "comun"
    _, nombre_centro, color_centro = nombres[id_centro]
    url_centros = f"../../../index.html#sec-{id_centro}"

    opciones_centros = []
    for c_id, c_nom, _ in CENTROS_NAV:
        if c_id == id_centro:
            destino = f"../{carpeta_diagrama.name}/{ruta_html.name}"
        else:
            destino = _destino_en_centro(c_id, carpeta_diagrama, carpeta_centros)
        sel = ' selected="selected"' if c_id == id_centro else ""
        opciones_centros.append(f'<option value="{destino}"{sel}>{html.escape(c_nom)}</option>')
    select_centros = "\n            ".join(opciones_centros)

    flujos = []
    for s, h in _listar_flujos(carpeta_diagrama.parent):
        slug_s = s.name[3:]
        flujos.append({
            "num": int(s.name[:2]), "slug": slug_s,
            "titulo": TITULOS.get(slug_s, slug_s.replace("-", " ").capitalize()),
            "cap": CAPACIDADES.get(slug_s, ""),
            "url": f"../{s.name}/{h.name}",
            "is_curr": s.resolve() == carpeta_diagrama.resolve(),
        })
    curr_idx = next((i for i, f in enumerate(flujos) if f["is_curr"]), 0)
    total = len(flujos)
    flujo_ant = flujos[curr_idx - 1] if curr_idx > 0 else None
    flujo_sig = flujos[curr_idx + 1] if curr_idx < total - 1 else None

    opciones_flujos = []
    for f in flujos:
        sel = ' selected="selected"' if f["is_curr"] else ""
        opciones_flujos.append(f'<option value="{f["url"]}"{sel}>{f["num"]:02d}. {html.escape(f["titulo"])}</option>')
    select_flujos = "\n          ".join(opciones_flujos)

    chevron_izq = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="15 18 9 12 15 6"></polyline></svg>'
    chevron_der = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"></polyline></svg>'
    if flujo_ant:
        t = html.escape(flujo_ant["titulo"])
        btn_prev = (f'<a href="{flujo_ant["url"]}" class="flow-btn-top prev" title="Flujo anterior: {flujo_ant["num"]:02d}. {t}">'
                    f'{chevron_izq}<span class="flow-btn-num">{flujo_ant["num"]:02d}</span><span class="flow-btn-txt">{t}</span></a>')
    else:
        btn_prev = (f'<span class="flow-btn-top prev disabled" title="Primer flujo de este centro">{chevron_izq}'
                    '<span class="flow-btn-txt">Inicio</span></span>')
    if flujo_sig:
        t = html.escape(flujo_sig["titulo"])
        btn_next = (f'<a href="{flujo_sig["url"]}" class="flow-btn-top next primary" title="Siguiente flujo: {flujo_sig["num"]:02d}. {t}">'
                    f'<span class="flow-btn-num">{flujo_sig["num"]:02d}</span><span class="flow-btn-txt">{t}</span>{chevron_der}</a>')
    else:
        btn_next = ('<span class="flow-btn-top next disabled" title="Último flujo de este centro">'
                    f'<span class="flow-btn-txt">Fin</span>{chevron_der}</span>')

    nav_top = f'''<!-- === FLOW NAV TOP === -->
    <nav class="flow-nav-top" aria-label="Navegación entre flujos">
      <div class="flow-nav-left">
        <a href="{url_centros}" class="btn-flow-centros" title="Volver a la galería principal de Centros Empresariales">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12"></line><polyline points="12 19 5 12 12 5"></polyline></svg>
          <span>Volver a Centros</span>
        </a>
        <span class="flow-nav-sep">/</span>
        <div class="flow-nav-select-wrap flow-nav-select-center-wrap">
          <span class="flow-center-dot" style="position:absolute; left:0.65rem; top:50%; transform:translateY(-50%); z-index:2; pointer-events:none; background:{color_centro};"></span>
          <select class="flow-nav-select flow-nav-select-center" onchange="if(this.value) window.location.href=this.value" title="Cambiar a otro Centro Empresarial">
            {select_centros}
          </select>
          <span class="flow-nav-select-arrow">▾</span>
        </div>
        <span class="flow-nav-sep">/</span>
        <div class="flow-nav-select-wrap">
          <select class="flow-nav-select" onchange="if(this.value) window.location.href=this.value" title="Cambiar a otro flujo del centro">
            {select_flujos}
          </select>
          <span class="flow-nav-select-arrow">▾</span>
        </div>
      </div>
      <div class="flow-nav-right">
        {btn_prev}
        <span class="flow-nav-counter">Flujo <strong>{curr_idx + 1}</strong> de {total}</span>
        {btn_next}
      </div>
    </nav>
    <!-- === /FLOW NAV TOP === -->'''

    return {
        "nav_top": nav_top,
        "nav_bottom": _html_nav_bottom(flujo_ant, flujo_sig, url_centros),
        "flujo_ant": flujo_ant,
        "flujo_sig": flujo_sig,
        "url_centros": url_centros,
    }


# ======================= BLOQUE 4: inyección (reemplaza inyectar_en_html e inyectar_todos) =======================
def _limpiar_inyeccion_previa(contenido):
    contenido = re.sub(r"\s*<style>\s*/\* === (?:DISEÑO RESPONSIVO|GUÍA OPERATIVA).*?</script>", "", contenido, flags=re.DOTALL)
    for marca in ("FLOW NAV TOP", "FLOW NAV BOTTOM"):
        contenido = re.sub(rf"\s*<!-- === {marca} === -->.*?<!-- === /{marca} === -->", "", contenido, flags=re.DOTALL)
    # Limpiar cualquier residuo previo en etiquetas de nodos o flechas
    contenido = re.sub(r'\s+data-step-state="[^"]*"', '', contenido)
    contenido = re.sub(r'\s+data-ultimo-escogido="[^"]*"', '', contenido)
    contenido = re.sub(r'\s+data-step-edge="[^"]*"', '', contenido)
    return contenido


def _json_seguro(obj):
    """JSON para incrustar en <script>: «</» se escapa para que un texto no cierre el script."""
    return json.dumps(obj, ensure_ascii=False).replace("</", "<\\/")


def inyectar_en_html(ruta_html, slug):
    """Inyecta CSS, navegación superior/inferior y la guía operativa; se puede ejecutar varias veces."""
    nombre = ruta_html.parents[2].name
    id_centro = nombre if nombre in ("idiomas", "computacion", "emprendimiento") else ""
    nav = construir_navegacion_flujos(ruta_html)

    contenido = _limpiar_inyeccion_previa(ruta_html.read_text(encoding="utf-8"))
    nodo_ids = ids_nodos_en_html(contenido)
    guia = obtener_guia_para_slug(slug, id_centro, nodo_ids)

    if re.search(r'<div class="header"', contenido):
        contenido = re.sub(r'(<div class="header"[^>]*>)', lambda m: nav["nav_top"] + "\n    " + m.group(1), contenido, count=1)
    else:
        ADVERTENCIAS.append(f"{slug}: no se encontró <div class=\"header\">; no se inyectó la barra superior")

    bloque = (
        JS_SCRIPT_TEMPLATE
        .replace("__CSS__", CSS_MODAL)
        .replace("__GUIA_JSON__", _json_seguro(guia))
        .replace("__SIGUIENTE_FLUJO_JSON__", _json_seguro(nav["flujo_sig"]))
        .replace("__ANTERIOR_FLUJO_JSON__", _json_seguro(nav["flujo_ant"]))
        .replace("__VOLVER_CENTROS_URL__", nav["url_centros"])
    )
    extra = nav["nav_bottom"] + "\n" + bloque
    i = contenido.rfind("</body>")
    contenido = contenido[:i] + extra + "\n" + contenido[i:] if i != -1 else contenido + "\n" + extra

    ruta_html.write_text(contenido, encoding="utf-8")
    return True


def inyectar_todos():
    raiz = Path(__file__).resolve().parent.parent.parent
    cont = 0
    ADVERTENCIAS.clear()
    for html_file in sorted((raiz / "centros").glob("**/diagramas/**/*.html")):
        if inyectar_en_html(html_file, html_file.stem):
            cont += 1
    print(f"Inyección completada en {cont} diagramas HTML.")
    if ADVERTENCIAS:
        print(f"\n⚠ {len(ADVERTENCIAS)} advertencias de guías:")
        for a in ADVERTENCIAS:
            print("  -", a)
    return cont


if __name__ == "__main__":
    inyectar_todos()
