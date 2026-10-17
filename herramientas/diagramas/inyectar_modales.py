"""Inyecta guías operativas interactivas directamente en el modal (Pasaporte semántico) de los diagramas Archify.

Al hacer clic sobre cualquier nodo del flujo en el navegador, el contenedor `#focus-chip`
despliega la ficha operativa completa en Vista Dividida (Flujo BPM arriba + Guía abajo al 100% de ancho)
o en modo flotante/lateral, manteniendo siempre visible y responsivo el diagrama BPM.
"""
import json
import re
from pathlib import Path
from guias_operativas import obtener_guia, GUIAS_BASE, GUIAS_SCRIPTS
from plantillas import TITULOS, CAPACIDADES

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
  opacity: 0.58 !important;
}

.diagram-container svg[data-focus-active] [data-focus-match] {
  opacity: 0.9 !important;
}

.diagram-container svg[data-focus-active] [data-focus-selected] {
  opacity: 1 !important;
  filter: drop-shadow(0 0 10px var(--frontend-stroke)) !important;
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

/* Fila marcada como completada */
.guia-fila-paso.completada {
  background: rgba(16, 185, 129, 0.08) !important;
}

html:not([data-theme="dark"]) .guia-fila-paso.completada {
  background: #f0fdf4 !important;
}

.guia-fila-paso.completada .guia-check-btn .num-badge {
  background: #10b981 !important;
  color: #ffffff !important;
  border-color: #059669 !important;
  box-shadow: 0 0 10px rgba(16, 185, 129, 0.45) !important;
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
  min-width: 8.5rem !important;
  max-width: 22rem !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  text-align: left !important;
  gap: 0.55rem !important;
  padding: 0.26rem 0.75rem !important;
  border-radius: 0.48rem !important;
  overflow: hidden !important;
  flex-shrink: 0 !important;
}

.btn-next-body {
  display: flex !important;
  flex-direction: column !important;
  min-width: 0 !important;
  overflow: hidden !important;
  line-height: 1.2 !important;
}

.btn-next-kicker {
  font-size: 0.62rem !important;
  font-weight: 800 !important;
  letter-spacing: 0.04em !important;
  text-transform: uppercase !important;
  opacity: 0.92 !important;
  white-space: nowrap !important;
}

.btn-next-title {
  font-size: 0.71rem !important;
  font-weight: 600 !important;
  overflow: hidden !important;
  text-overflow: ellipsis !important;
  white-space: nowrap !important;
  opacity: 0.96 !important;
}

.btn-next-arrow {
  font-size: 0.95rem !important;
  font-weight: 800 !important;
  flex-shrink: 0 !important;
  line-height: 1 !important;
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

  // Marcar en el SVG del diagrama el último paso/nodo BPM escogido con un color distintivo persistente
  function marcarUltimoPasoEnDiagrama(nodeId) {
    if (!nodeId) return;
    window.__ultimoPasoEscogido = nodeId;
    try {
      sessionStorage.setItem('archify_ultimo_paso_' + window.location.pathname, nodeId);
    } catch (_) {}

    var svg = document.querySelector('.diagram-container > svg') || document.querySelector('svg');
    if (!svg) return;

    var nodosPrevios = svg.querySelectorAll('[data-ultimo-escogido="true"]');
    for (var i = 0; i < nodosPrevios.length; i++) {
      if (nodosPrevios[i].getAttribute('data-node-id') !== nodeId) {
        nodosPrevios[i].removeAttribute('data-ultimo-escogido');
      }
    }

    var targetNode = svg.querySelector('[data-node-id="' + nodeId + '"]');
    if (targetNode) {
      targetNode.setAttribute('data-ultimo-escogido', 'true');
    }
  }

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

  window.irAPaso = function(targetNodeId) {
    if (!targetNodeId) return;
    marcarUltimoPasoEnDiagrama(targetNodeId);
    var stepKeys = Object.keys(GUIA_MAP);
    var targetIdx = stepKeys.indexOf(targetNodeId);
    if (targetIdx !== -1 && targetIdx > (window.__guiaMaxUnlocked || 0)) {
      return;
    }
    var nodeElem = document.querySelector('[data-node-id="' + targetNodeId + '"]');
    if (nodeElem) {
      nodeElem.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
      setTimeout(function() {
        mantenerFlujoCompleto();
        actualizarModalGuia();
        marcarUltimoPasoEnDiagrama(targetNodeId);
      }, 30);
    }
  };

  window.navegarPaso = function(offset) {
    var idElem = document.getElementById('focus-id');
    if (!idElem) return;
    var currentId = (idElem.textContent || '').trim();
    var stepKeys = Object.keys(GUIA_MAP);
    var currentIndex = stepKeys.indexOf(currentId);
    if (currentIndex === -1) return;

    // Al avanzar con Siguiente, marcar completadas todas las filas del paso actual
    if (offset > 0 && currentId && GUIA_MAP[currentId]) {
      window.__guiaChecks[currentId] = window.__guiaChecks[currentId] || {};
      var curInst = GUIA_MAP[currentId].instrucciones || [];
      for (var r = 0; r < curInst.length; r++) {
        window.__guiaChecks[currentId][r] = true;
      }
    }

    var nextIndex = currentIndex + offset;
    if (nextIndex >= 0 && nextIndex < stepKeys.length) {
      if (nextIndex > (window.__guiaMaxUnlocked || 0)) {
        window.__guiaMaxUnlocked = nextIndex;
      }
      var targetNodeId = stepKeys[nextIndex];
      marcarUltimoPasoEnDiagrama(targetNodeId);
      var nodeElem = document.querySelector('[data-node-id="' + targetNodeId + '"]');
      if (nodeElem) {
        nodeElem.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
        setTimeout(function() {
          mantenerFlujoCompleto();
          actualizarModalGuia();
          marcarUltimoPasoEnDiagrama(targetNodeId);
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
    if (info.hito) {
      html += '<div class="guia-hito-badge">🎯 ' + escapeHtml(info.hito) + '</div>';
    }
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
      var statusExtra = numFilas > 5 ? (' · ' + numFilas + ' pasos (scroll ↓)') : '';
      html += '<div class="guia-footer-sticky">';
      html += '<button type="button" class="guia-nav-btn btn-pie-prev" ' + (hasPrev ? 'data-nav-paso="-1"' : 'disabled') + '>← Paso anterior</button>';
      html += '<div class="guia-pie-status">Paso ' + (currentIndex + 1) + ' de ' + totalSteps + ' (' + pct + '%)' + statusExtra + '</div>';
      if (hasNext) {
        var cleanNext = nextTitle.replace(/^Paso\s*\d+:\s*/i, '');
        var nextStepNum = currentIndex + 2;
        html += '<button type="button" class="guia-nav-btn btn-pie-next primary" data-nav-paso="1" title="Avanzar al Paso ' + nextStepNum + ': ' + escapeHtml(cleanNext) + '">';
        html += '<span class="btn-next-body">';
        html += '<span class="btn-next-kicker">Siguiente · Paso ' + nextStepNum + '</span>';
        html += '<span class="btn-next-title">' + escapeHtml(cleanNext) + '</span>';
        html += '</span>';
        html += '<span class="btn-next-arrow">→</span>';
        html += '</button>';
      } else {
        if (window.__SIGUIENTE_FLUJO && window.__SIGUIENTE_FLUJO.url) {
          var sigNum = window.__SIGUIENTE_FLUJO.num;
          var sigNumTxt = (sigNum < 10 ? '0' : '') + sigNum;
          html += '<a href="' + escapeHtml(window.__SIGUIENTE_FLUJO.url) + '" class="guia-nav-btn btn-pie-next primary" style="text-decoration:none;" title="Pasar al flujo ' + sigNumTxt + ': ' + escapeHtml(window.__SIGUIENTE_FLUJO.titulo) + '">';
          html += '<span class="btn-next-body">';
          html += '<span class="btn-next-kicker">¡Paso final! Siguiente flujo →</span>';
          html += '<span class="btn-next-title">' + sigNumTxt + '. ' + escapeHtml(window.__SIGUIENTE_FLUJO.titulo) + '</span>';
          html += '</span>';
          html += '<span class="btn-next-arrow">🚀</span>';
          html += '</a>';
        } else {
          html += '<a href="' + escapeHtml(window.__VOLVER_CENTROS_URL || '#') + '" class="guia-nav-btn btn-pie-next" style="text-decoration:none;" title="Volver a la galería de Centros">';
          html += '<span class="btn-next-body">';
          html += '<span class="btn-next-kicker">✓ Fin del recorrido</span>';
          html += '<span class="btn-next-title">Volver a Centros</span>';
          html += '</span>';
          html += '<span class="btn-next-arrow">🏛️</span>';
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
      '<button type="button" class="chip-btn-ctrl btn-copy" title="Copiar enlace directo a este paso">🔗 <span class="btn-copy-txt">Copiar enlace</span></button>' +
      '<button type="button" class="chip-btn-close" title="Cerrar modal (Esc)">✕</button>' +
      '</div>';

    chip.insertBefore(topbar, chip.firstChild);

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
    if (tablaWrap) {
      tablaWrap.scrollTop = 0;
    }
    var scrollBody = card.querySelector('.guia-body-scroll');
    if (scrollBody) {
      scrollBody.scrollTop = 0;
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
        if (chip && !chip.hidden && chip.classList.contains('tiene-guia')) {
          e.preventDefault();
          cerrarModalGuia();
          return;
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

    // Restaurar el último paso escogido previamente si existe en sessionStorage
    var storedLast = null;
    try {
      storedLast = sessionStorage.getItem('archify_ultimo_paso_' + window.location.pathname);
    } catch (_) {}
    if (storedLast) {
      marcarUltimoPasoEnDiagrama(storedLast);
      setTimeout(function() {
        marcarUltimoPasoEnDiagrama(storedLast);
      }, 100);
      setTimeout(function() {
        marcarUltimoPasoEnDiagrama(storedLast);
      }, 350);
    }

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


def obtener_guia_para_slug(slug, id_centro=""):
    """Devuelve el diccionario de nodos y pasos para el slug dado y el centro."""
    guia = obtener_guia(slug, id_centro)
    if guia:
        return guia
    if slug in GUIAS_BASE:
        return GUIAS_BASE[slug]
    for k, v in GUIAS_BASE.items():
        if k in slug:
            return v
    for s_id, s_map in GUIAS_SCRIPTS.items():
        if f"script-{s_id}" in slug or f"script_{s_id}" in slug:
            return s_map
    return None


def construir_navegacion_flujos(ruta_html):
    """Calcula la navegación anterior/siguiente y datos para la barra superior y pie."""
    carpeta_diagrama = ruta_html.parent
    carpeta_diagramas = carpeta_diagrama.parent
    carpeta_centros = carpeta_diagramas.parent.parent

    ruta_str = str(ruta_html).lower()
    if "idiomas" in ruta_str:
        id_centro = "idiomas"
        nombre_centro = "Centro de Idiomas"
        color_centro = "#8b5cf6"
    elif "computacion" in ruta_str:
        id_centro = "computacion"
        nombre_centro = "Centro de Computación"
        color_centro = "#10b981"
    elif "emprendimiento" in ruta_str:
        id_centro = "emprendimiento"
        nombre_centro = "Centro de Emprendimiento"
        color_centro = "#f59e0b"
    else:
        id_centro = "comun"
        nombre_centro = "Centros Empresariales"
        color_centro = "#7030A0"

    url_centros = f"../../../index.html#sec-{id_centro}"

    # Construir opciones del selector de Centros (Idiomas, Computación, Emprendimiento, Común)
    centros_lista = [
        ("idiomas", "Centro de Idiomas", "#8b5cf6", "🟣"),
        ("computacion", "Centro de Computación", "#10b981", "🟢"),
        ("emprendimiento", "Centro de Emprendimiento", "#f59e0b", "🟠"),
        ("comun", "Los tres centros (común)", "#7030A0", "🔄"),
    ]
    centros_options_html = []
    for c_id, c_nom, c_col, c_ico in centros_lista:
        is_c_curr = (c_id == id_centro)
        sel_c = ' selected="selected"' if is_c_curr else ""
        lbl_c = f"{c_ico} {c_nom}" + (" (Actual)" if is_c_curr else "")
        if is_c_curr:
            target_c_url = f"../{carpeta_diagrama.name}/{ruta_html.name}"
        else:
            c_diag_dir = carpeta_centros / c_id / "diagramas"
            matching_dir = c_diag_dir / carpeta_diagrama.name
            if matching_dir.is_dir() and next(matching_dir.glob("*.html"), None):
                matching_html = next(matching_dir.glob("*.html")).name
                target_c_url = f"../../../{c_id}/diagramas/{carpeta_diagrama.name}/{matching_html}"
            else:
                primeros = sorted([p for p in c_diag_dir.glob("[0-9][0-9]-*") if p.is_dir() and next(p.glob("*.html"), None)])
                if primeros:
                    primer_html = next(primeros[0].glob("*.html")).name
                    target_c_url = f"../../../{c_id}/diagramas/{primeros[0].name}/{primer_html}"
                else:
                    target_c_url = f"../../../index.html#sec-{c_id}"
        centros_options_html.append(f'<option value="{target_c_url}"{sel_c}>{lbl_c}</option>')
    select_centros_options = "\n            ".join(centros_options_html)

    subs = sorted([
        p for p in carpeta_diagramas.glob("[0-9][0-9]-*")
        if p.is_dir() and next(p.glob("*.html"), None) is not None
    ])

    flujos = []
    for s in subs:
        html_file = next(s.glob("*.html"))
        num = int(s.name[:2])
        slug_s = s.name[3:]
        titulo = TITULOS.get(slug_s, slug_s.replace("-", " ").capitalize())
        cap = CAPACIDADES.get(slug_s, "")
        rel_url = f"../{s.name}/{html_file.name}"
        is_curr = (s.resolve() == carpeta_diagrama.resolve())
        flujos.append({
            "num": num,
            "slug": slug_s,
            "titulo": titulo,
            "cap": cap,
            "url": rel_url,
            "is_curr": is_curr,
            "folder": s.name,
            "filename": html_file.name,
        })

    curr_idx = -1
    for i, f in enumerate(flujos):
        if f["is_curr"]:
            curr_idx = i
            break

    if curr_idx == -1 and flujos:
        curr_idx = 0

    total_flujos = len(flujos)
    flujo_actual = flujos[curr_idx] if curr_idx >= 0 else None
    num_actual = curr_idx + 1
    flujo_ant = flujos[curr_idx - 1] if curr_idx > 0 else None
    flujo_sig = flujos[curr_idx + 1] if curr_idx < total_flujos - 1 else None

    # Opciones para el select dropdown
    options_html = []
    for f in flujos:
        selected = ' selected="selected"' if f["is_curr"] else ""
        label = f"{f['num']:02d}. {f['titulo']}"
        if f["is_curr"]:
            label += " (Actual)"
        options_html.append(f'<option value="{f["url"]}"{selected}>{label}</option>')
    select_options = "\n          ".join(options_html)

    # Botones top
    if flujo_ant:
        btn_prev_top = f'''<a href="{flujo_ant['url']}" class="flow-btn-top prev" title="Flujo anterior: {flujo_ant['num']:02d}. {flujo_ant['titulo']}">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="15 18 9 12 15 6"></polyline></svg>
        <span class="flow-btn-num">{flujo_ant['num']:02d}</span>
        <span class="flow-btn-txt">{flujo_ant['titulo']}</span>
      </a>'''
    else:
        btn_prev_top = '''<span class="flow-btn-top prev disabled" title="Primer flujo de este centro">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="15 18 9 12 15 6"></polyline></svg>
        <span class="flow-btn-txt">Inicio</span>
      </span>'''

    if flujo_sig:
        btn_next_top = f'''<a href="{flujo_sig['url']}" class="flow-btn-top next primary" title="Siguiente flujo: {flujo_sig['num']:02d}. {flujo_sig['titulo']}">
        <span class="flow-btn-num">{flujo_sig['num']:02d}</span>
        <span class="flow-btn-txt">{flujo_sig['titulo']}</span>
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"></polyline></svg>
      </a>'''
    else:
        btn_next_top = '''<span class="flow-btn-top next disabled" title="Último flujo de este centro">
        <span class="flow-btn-txt">Fin</span>
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"></polyline></svg>
      </span>'''

    html_nav_top = f'''<!-- === FLOW NAV TOP === -->
    <nav class="flow-nav-top" aria-label="Navegación entre flujos">
      <div class="flow-nav-left">
        <a href="{url_centros}" class="btn-flow-centros" title="Volver a la galería principal de Centros Empresariales">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <line x1="19" y1="12" x2="5" y2="12"></line>
            <polyline points="12 19 5 12 12 5"></polyline>
          </svg>
          <span>Volver a Centros</span>
        </a>
        <span class="flow-nav-sep">/</span>
        <div class="flow-nav-select-wrap flow-nav-select-center-wrap">
          <span class="flow-center-dot" style="position:absolute; left:0.65rem; top:50%; transform:translateY(-50%); z-index:2; pointer-events:none; background:{color_centro};"></span>
          <select class="flow-nav-select flow-nav-select-center" onchange="if(this.value) window.location.href=this.value" title="Cambiar a otro Centro Empresarial">
            {select_centros_options}
          </select>
          <span class="flow-nav-select-arrow">▾</span>
        </div>
        <span class="flow-nav-sep">/</span>
        <div class="flow-nav-select-wrap">
          <select class="flow-nav-select" onchange="if(this.value) window.location.href=this.value" title="Cambiar a otro flujo del centro">
            {select_options}
          </select>
          <span class="flow-nav-select-arrow">▾</span>
        </div>
      </div>
      <div class="flow-nav-right">
        {btn_prev_top}
        <span class="flow-nav-counter">Flujo <strong>{num_actual}</strong> de {total_flujos}</span>
        {btn_next_top}
      </div>
    </nav>
    <!-- === /FLOW NAV TOP === -->'''

    return {
        "nav_top": html_nav_top,
        "nav_bottom": "",
        "flujo_ant": flujo_ant,
        "flujo_sig": flujo_sig,
        "num_actual": num_actual,
        "total_flujos": total_flujos,
        "url_centros": url_centros,
    }


def inyectar_en_html(ruta_html, slug):
    """Inyecta el CSS responsivo, navegación entre flujos y JS de la guía operativa en el HTML generado."""
    ruta_str = str(ruta_html).lower()
    id_centro = "idiomas" if "idiomas" in ruta_str else ("computacion" if "computacion" in ruta_str else ("emprendimiento" if "emprendimiento" in ruta_str else ""))
    guia = obtener_guia_para_slug(slug, id_centro) or {}

    nav_data = construir_navegacion_flujos(ruta_html)

    contenido = ruta_html.read_text(encoding="utf-8")
    if "/* === DISEÑO RESPONSIVO" in contenido or "guia-operativa-card" in contenido:
        contenido = re.sub(r"<style>\s*/\* === (?:DISEÑO RESPONSIVO|GUÍA OPERATIVA).*?<\/script>", "", contenido, flags=re.DOTALL)
    contenido = re.sub(r"\s*<!-- === FLOW NAV TOP === -->.*?<!-- === /FLOW NAV TOP === -->", "", contenido, flags=re.DOTALL)
    contenido = re.sub(r"\s*<!-- === FLOW NAV BOTTOM === -->.*?<!-- === /FLOW NAV BOTTOM === -->", "", contenido, flags=re.DOTALL)

    # Inyectar navegación superior antes de <div class="header">
    if '<div class="header">' in contenido:
        contenido = contenido.replace('<div class="header">', f'{nav_data["nav_top"]}\n    <div class="header">', 1)

    guia_json = json.dumps(guia, ensure_ascii=False)
    sig_json = json.dumps(nav_data["flujo_sig"], ensure_ascii=False) if nav_data["flujo_sig"] else "null"
    ant_json = json.dumps(nav_data["flujo_ant"], ensure_ascii=False) if nav_data["flujo_ant"] else "null"

    bloque = (
        JS_SCRIPT_TEMPLATE
        .replace("__CSS__", CSS_MODAL)
        .replace("__GUIA_JSON__", guia_json)
        .replace("__SIGUIENTE_FLUJO_JSON__", sig_json)
        .replace("__ANTERIOR_FLUJO_JSON__", ant_json)
        .replace("__VOLVER_CENTROS_URL__", nav_data["url_centros"])
    )

    if "</body>" in contenido:
        nuevo_contenido = contenido.replace("</body>", f"{bloque}\n</body>")
    else:
        nuevo_contenido = contenido + "\n" + bloque

    ruta_html.write_text(nuevo_contenido, encoding="utf-8")
    return True


def inyectar_todos():
    """Inyecta guías y navegación en todos los archivos HTML existentes en centros/."""
    raiz = Path(__file__).resolve().parent.parent.parent
    centros_dir = raiz / "centros"
    cont = 0
    for html_file in sorted(centros_dir.glob("**/diagramas/**/*.html")):
        slug = html_file.stem
        if inyectar_en_html(html_file, slug):
            cont += 1
    print(f"Inyección completada en {cont} diagramas HTML.")
    return cont


if __name__ == "__main__":
    inyectar_todos()