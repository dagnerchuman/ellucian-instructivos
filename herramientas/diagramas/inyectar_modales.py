"""Inyecta guías operativas interactivas directamente en el modal (Pasaporte semántico) de los diagramas Archify.

Al hacer clic sobre cualquier nodo del flujo en el navegador, el modal lateral `#focus-chip`
despliega la ficha operativa completa (paso a paso, campos, valores, guardados F10 y atajos),
eliminando la necesidad de tarjetas largas de texto al pie de página.
"""
import json
import re
from pathlib import Path
from guias_operativas import obtener_guia, GUIAS_BASE, GUIAS_SCRIPTS
from plantillas import TITULOS, CAPACIDADES

CSS_MODAL = """
/* === DISEÑO RESPONSIVO Y GUÍA OPERATIVA (PASAPORTE SEMÁNTICO) === */

/* --- 0. BARRAS DE NAVEGACIÓN Y PAGINACIÓN ENTRE FLUJOS --- */
.flow-nav-top {
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  flex-wrap: wrap !important;
  gap: 0.65rem !important;
  padding: 0.5rem 0.85rem !important;
  margin-bottom: 1.25rem !important;
  margin-right: 21.5rem !important;
  background: var(--toolbar-bg, rgba(15, 23, 42, 0.75)) !important;
  border: 1px solid var(--panel-border, #334155) !important;
  border-radius: 0.75rem !important;
  backdrop-filter: blur(12px) !important;
  -webkit-backdrop-filter: blur(12px) !important;
  font-family: system-ui, -apple-system, sans-serif !important;
  font-size: 0.82rem !important;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.18) !important;
  position: relative !important;
  z-index: 25 !important;
}

[data-theme="light"] .flow-nav-top {
  background: rgba(255, 255, 255, 0.9) !important;
  border-color: rgba(203, 213, 225, 0.8) !important;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05) !important;
}

@media (max-width: 900px) {
  .flow-nav-top {
    margin-right: 0 !important;
    margin-bottom: 0.75rem !important;
  }
}

.flow-nav-left {
  display: flex !important;
  align-items: center !important;
  flex-wrap: wrap !important;
  gap: 0.5rem !important;
}

.flow-nav-right {
  display: flex !important;
  align-items: center !important;
  gap: 0.45rem !important;
}

.btn-flow-centros {
  display: inline-flex !important;
  align-items: center !important;
  gap: 0.45rem !important;
  padding: 0.35rem 0.75rem !important;
  border-radius: 0.5rem !important;
  background: var(--toolbar-bg, #1e293b) !important;
  color: var(--text, #fff) !important;
  border: 1px solid var(--panel-border, #334155) !important;
  font-weight: 600 !important;
  font-size: 0.8rem !important;
  text-decoration: none !important;
  transition: all 0.18s ease !important;
  cursor: pointer !important;
}

.btn-flow-centros:hover {
  background: var(--toolbar-hover, #334155) !important;
  border-color: #a78bfa !important;
  color: #fff !important;
  transform: translateX(-2px) !important;
}

.flow-nav-sep {
  color: var(--text-dim, #64748b) !important;
  opacity: 0.6 !important;
  font-size: 0.75rem !important;
}

.flow-nav-center-tag {
  display: inline-flex !important;
  align-items: center !important;
  gap: 0.4rem !important;
  font-weight: 600 !important;
  color: var(--text, #fff) !important;
  padding: 0.2rem 0.55rem !important;
  border-radius: 0.4rem !important;
  background: rgba(148, 163, 184, 0.1) !important;
  font-size: 0.78rem !important;
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
}

.flow-nav-select {
  appearance: none !important;
  -webkit-appearance: none !important;
  background: var(--toolbar-bg, #1e293b) !important;
  color: var(--text, #fff) !important;
  border: 1px solid var(--panel-border, #334155) !important;
  border-radius: 0.5rem !important;
  padding: 0.35rem 1.6rem 0.35rem 0.65rem !important;
  font-size: 0.8rem !important;
  font-weight: 500 !important;
  cursor: pointer !important;
  outline: none !important;
  max-width: 250px !important;
  text-overflow: ellipsis !important;
  white-space: nowrap !important;
  overflow: hidden !important;
  transition: border-color 0.18s ease !important;
}

.flow-nav-select:hover,
.flow-nav-select:focus {
  border-color: #a78bfa !important;
}

.flow-nav-select-arrow {
  position: absolute !important;
  right: 0.55rem !important;
  pointer-events: none !important;
  font-size: 0.75rem !important;
  color: var(--text-muted, #94a3b8) !important;
}

.flow-btn-top {
  display: inline-flex !important;
  align-items: center !important;
  gap: 0.35rem !important;
  padding: 0.35rem 0.65rem !important;
  border-radius: 0.5rem !important;
  font-weight: 600 !important;
  font-size: 0.78rem !important;
  text-decoration: none !important;
  border: 1px solid var(--panel-border, #334155) !important;
  background: var(--toolbar-bg, #1e293b) !important;
  color: var(--text, #fff) !important;
  transition: all 0.18s ease !important;
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

.flow-nav-counter {
  font-size: 0.78rem !important;
  color: var(--text-muted, #94a3b8) !important;
  padding: 0 0.25rem !important;
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

/* --- 1. HEADER & TOOLBAR RESPONSIVO --- */
.header {
  padding-right: 22rem !important;
  margin-bottom: 1rem !important;
  position: relative !important;
}

.header-row {
  display: flex !important;
  justify-content: flex-start !important;
  align-items: center !important;
  gap: 0.75rem !important;
}

.header h1 {
  margin: 0 !important;
  font-size: clamp(1.15rem, 2.2vw, 1.6rem) !important;
  line-height: 1.3 !important;
  text-align: left !important;
  word-break: break-word !important;
}

.subtitle {
  text-align: left !important;
  font-size: clamp(0.72rem, 1.3vw, 0.82rem) !important;
  line-height: 1.55 !important;
  color: var(--text-muted) !important;
  margin: 0.35rem 0 0 !important;
  max-width: 58rem !important;
}

.toolbar {
  position: absolute !important;
  top: 1.25rem !important;
  right: 1.5rem !important;
  left: auto !important;
  margin: 0 !important;
  z-index: 30 !important;
  display: flex !important;
  align-items: center !important;
  gap: 0.35rem !important;
}

@media (max-width: 900px) {
  body {
    padding: 0.75rem !important;
  }
  .header {
    padding-right: 0 !important;
  }
  .toolbar {
    position: relative !important;
    top: auto !important;
    right: auto !important;
    left: auto !important;
    width: 100% !important;
    justify-content: flex-end !important;
    margin-bottom: 0.75rem !important;
    overflow-x: auto !important;
    padding-bottom: 0.35rem !important;
    scrollbar-width: thin;
  }
  .toolbar .preset-menu,
  .toolbar .export-menu {
    position: fixed !important;
    top: auto !important;
    bottom: 4.5rem !important;
    left: 1rem !important;
    right: 1rem !important;
    width: auto !important;
    max-width: none !important;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5) !important;
    z-index: 100 !important;
  }
}

/* --- 2. CONTROLES DEL LIENZO (DIAGRAM-NAV) --- */
.diagram-container {
  position: relative !important;
  border-radius: 0.85rem !important;
}

@media (max-width: 800px) {
  .diagram-container {
    overflow-x: auto !important;
    -webkit-overflow-scrolling: touch !important;
  }
}

@media (max-width: 640px) {
  .diagram-nav {
    bottom: 0.5rem !important;
    right: 0.5rem !important;
    max-width: calc(100% - 1rem) !important;
    overflow-x: auto !important;
    gap: 0.25rem !important;
    padding: 0.25rem !important;
    background: var(--toolbar-bg) !important;
    backdrop-filter: blur(12px) !important;
    border-radius: 0.5rem !important;
  }
  .diagram-nav button {
    min-width: 2.2rem !important;
    height: 2.2rem !important;
    padding: 0 0.35rem !important;
    font-size: 0.7rem !important;
  }
}

/* --- 3. TARJETAS INFORMATIVAS INFERIORES (.CARDS) --- */
.cards {
  display: grid !important;
  grid-template-columns: repeat(auto-fill, minmax(min(20rem, 100%), 1fr)) !important;
  gap: 1.15rem !important;
  margin-top: 1.75rem !important;
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
  transition: transform 0.15s ease, box-shadow 0.15s ease !important;
}

.card:hover {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15) !important;
}

.card h3 {
  font-size: 0.875rem !important;
  font-weight: 700 !important;
  letter-spacing: 0.02em !important;
}

.card ul {
  margin: 0.65rem 0 0 !important;
  padding-left: 1.2rem !important;
  font-size: 0.775rem !important;
  line-height: 1.55 !important;
  color: var(--text) !important;
}

.card li {
  margin-bottom: 0.4rem !important;
}

.card li:last-child {
  margin-bottom: 0 !important;
}

/* --- 4. MODAL / GUÍA OPERATIVA PASO A PASO (.FOCUS-CHIP) WIZARD DE ALTA GAMA --- */
.focus-chip {
  transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.15s ease, max-height 0.25s ease !important;
}

/* Modal amplio y espacioso tipo Wizard centrado en pantalla con altura dinámica */
.focus-chip.tiene-guia {
  position: fixed !important;
  left: 50% !important;
  top: 50% !important;
  transform: translate(-50%, -50%) !important;
  width: min(74rem, calc(100vw - 2rem)) !important;
  max-width: 76rem !important;
  height: auto !important;
  min-height: min(30rem, 62vh) !important;
  max-height: min(90vh, calc(100vh - 2rem)) !important;
  display: flex !important;
  flex-direction: column !important;
  align-items: stretch !important;
  justify-content: space-between !important;
  overflow: hidden !important;
  border-radius: 1rem !important;
  box-shadow: 0 32px 90px rgba(0, 0, 0, 0.75), 0 0 0 1px var(--frontend-stroke) !important;
  backdrop-filter: blur(25px) !important;
  -webkit-backdrop-filter: blur(25px) !important;
  z-index: 95 !important;
  background: var(--panel, #0f172a) !important;
  margin: 0 !important;
  padding: 0 !important;
}

/* Modo acoplado a la derecha en escritorio */
.focus-chip.tiene-guia.docked-right {
  position: fixed !important;
  left: auto !important;
  right: 1.25rem !important;
  top: 1.25rem !important;
  bottom: 1.25rem !important;
  transform: none !important;
  width: min(46rem, calc(52vw - 1.5rem)) !important;
  max-width: 48rem !important;
  height: calc(100vh - 2.5rem) !important;
  max-height: calc(100vh - 2.5rem) !important;
}

/* Modo Minimizado (Píldora flotante inferior) */
.focus-chip.tiene-guia.chip-minimized {
  position: fixed !important;
  left: 50% !important;
  top: auto !important;
  bottom: 1.5rem !important;
  transform: translateX(-50%) !important;
  width: min(38rem, calc(100vw - 2rem)) !important;
  min-width: 20rem !important;
  max-width: calc(100vw - 2rem) !important;
  min-height: 3.1rem !important;
  max-height: 3.1rem !important;
  height: 3.1rem !important;
  overflow: hidden !important;
  box-shadow: 0 12px 35px rgba(0, 0, 0, 0.5), 0 0 0 1px var(--frontend-stroke) !important;
}

/* Ocultar ruido técnico y elementos nativos de Archify */
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

/* Estructura del Head de Archify: columna de ancho 100% real */
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
  height: 100% !important;
  max-height: 100% !important;
  flex: 1 1 auto !important;
  min-height: 0 !important;
  overflow: hidden !important;
  background: transparent !important;
  box-sizing: border-box !important;
}

/* Barra superior unificada de extremo a extremo */
.guia-modal-topbar {
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  flex-wrap: nowrap !important;
  gap: 0.75rem !important;
  width: 100% !important;
  box-sizing: border-box !important;
  padding: 0.6rem 1.15rem !important;
  background: linear-gradient(135deg, rgba(30, 41, 59, 0.94), rgba(15, 23, 42, 0.99)) !important;
  border-bottom: 1px solid rgba(148, 163, 184, 0.22) !important;
  flex-shrink: 0 !important;
  z-index: 30 !important;
  user-select: none !important;
}

html:not([data-theme="dark"]) .guia-modal-topbar {
  background: linear-gradient(135deg, #ffffff, #f1f5f9) !important;
  border-bottom-color: #cbd5e1 !important;
}

.guia-modal-brand {
  display: flex !important;
  align-items: center !important;
  gap: 0.6rem !important;
  min-width: 0 !important;
  flex: 1 1 auto !important;
}

.guia-brand-badge {
  font-size: 0.66rem !important;
  font-weight: 800 !important;
  text-transform: uppercase !important;
  letter-spacing: 0.05em !important;
  padding: 0.2rem 0.55rem !important;
  border-radius: 0.35rem !important;
  background: #4338ca !important;
  color: #ffffff !important;
  flex-shrink: 0 !important;
}

.guia-brand-title {
  font-size: 0.88rem !important;
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
  display: inline-flex !important;
  align-items: center !important;
  justify-content: flex-end !important;
  gap: 0.4rem !important;
  flex-shrink: 0 !important;
  margin-left: auto !important;
}

.chip-btn-ctrl {
  background: rgba(148, 163, 184, 0.12) !important;
  border: 1px solid rgba(148, 163, 184, 0.28) !important;
  color: var(--toolbar-text, #e2e8f0) !important;
  border-radius: 0.45rem !important;
  padding: 0.26rem 0.6rem !important;
  font-size: 0.72rem !important;
  font-weight: 600 !important;
  cursor: pointer !important;
  display: inline-flex !important;
  align-items: center !important;
  gap: 0.32rem !important;
  transition: all 0.15s ease !important;
  line-height: 1.2 !important;
  white-space: nowrap !important;
}

html:not([data-theme="dark"]) .chip-btn-ctrl {
  color: #334155 !important;
  background: #ffffff !important;
  border-color: #cbd5e1 !important;
}

.chip-btn-ctrl:hover {
  background: rgba(148, 163, 184, 0.25) !important;
  color: #ffffff !important;
  border-color: var(--frontend-stroke) !important;
}

html:not([data-theme="dark"]) .chip-btn-ctrl:hover {
  background: #f1f5f9 !important;
  color: #0f172a !important;
}

.chip-btn-close {
  width: 1.75rem !important;
  height: 1.75rem !important;
  border-radius: 50% !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  font-size: 0.95rem !important;
  line-height: 1 !important;
  padding: 0 !important;
  background: rgba(239, 68, 68, 0.14) !important;
  border: 1px solid rgba(239, 68, 68, 0.35) !important;
  color: #f87171 !important;
  cursor: pointer !important;
  transition: all 0.15s ease !important;
  margin-left: 0.2rem !important;
  flex-shrink: 0 !important;
}

.chip-btn-close:hover {
  background: #ef4444 !important;
  color: #ffffff !important;
  border-color: #ef4444 !important;
  transform: scale(1.06) !important;
}

/* Contenedor intermedio de Archify sin scroll propio para delegarlo al cuerpo */
.focus-chip.tiene-guia .relationship-lens-copy {
  width: 100% !important;
  max-width: 100% !important;
  box-sizing: border-box !important;
  min-width: 0 !important;
  min-height: 0 !important;
  display: flex !important;
  flex-direction: column !important;
  flex: 1 1 auto !important;
  overflow: hidden !important;
  padding: 0 !important;
  margin: 0 !important;
  position: relative !important;
}

.focus-chip.chip-minimized .guia-modal-topbar {
  border-bottom: none !important;
  cursor: pointer;
}

.focus-chip.chip-minimized .relationship-lens-copy,
.focus-chip.chip-minimized .guia-operativa-card {
  display: none !important;
}

/* Tarjeta principal: divide en cuerpo con scroll (.guia-body-scroll) y footer fijo (.guia-footer-sticky) */
.guia-operativa-card {
  margin: 0 !important;
  padding: 0 !important;
  border: none !important;
  background: transparent !important;
  display: flex !important;
  flex-direction: column !important;
  justify-content: space-between !important;
  flex: 1 1 auto !important;
  width: 100% !important;
  height: 100% !important;
  min-height: 0 !important;
  box-sizing: border-box !important;
  overflow: hidden !important;
}

.guia-body-scroll {
  flex: 1 1 auto !important;
  min-height: 0 !important;
  overflow-y: auto !important;
  overflow-x: hidden !important;
  padding: 0.65rem 1.15rem 0.75rem 1.15rem !important;
  box-sizing: border-box !important;
  scrollbar-width: thin !important;
}

/* Stepper de Fases Interactivo Horizontal Compacto */
.guia-stepper-wrap {
  overflow-x: auto !important;
  scrollbar-width: thin !important;
  -webkit-overflow-scrolling: touch !important;
  padding: 0.1rem 0 0.45rem 0 !important;
  margin-bottom: 0.55rem !important;
  border-bottom: 1px solid rgba(148, 163, 184, 0.16) !important;
}

.guia-stepper-track {
  display: flex !important;
  align-items: center !important;
  gap: 0.35rem !important;
  min-width: max-content !important;
}

.guia-step-pill {
  display: inline-flex !important;
  align-items: center !important;
  gap: 0.35rem !important;
  background: rgba(148, 163, 184, 0.1) !important;
  border: 1px solid rgba(148, 163, 184, 0.22) !important;
  color: var(--text-muted, #94a3b8) !important;
  padding: 0.24rem 0.68rem !important;
  border-radius: 999px !important;
  font-size: 0.72rem !important;
  font-weight: 600 !important;
  cursor: pointer !important;
  transition: all 0.18s ease !important;
  white-space: nowrap !important;
  flex-shrink: 0 !important;
}

html:not([data-theme="dark"]) .guia-step-pill {
  background: #f1f5f9 !important;
  border-color: #cbd5e1 !important;
  color: #64748b !important;
}

.guia-step-pill:hover {
  border-color: #38bdf8 !important;
  color: var(--toolbar-text, #f1f5f9) !important;
  background: rgba(56, 189, 248, 0.15) !important;
}

.guia-step-pill.active {
  background: linear-gradient(135deg, #4338ca, #3b82f6) !important;
  border-color: #60a5fa !important;
  color: #ffffff !important;
  font-weight: 700 !important;
  box-shadow: 0 3px 10px rgba(59, 130, 246, 0.35) !important;
}

.guia-step-pill.past {
  background: rgba(16, 185, 129, 0.12) !important;
  border-color: rgba(16, 185, 129, 0.3) !important;
  color: #34d399 !important;
}

html:not([data-theme="dark"]) .guia-step-pill.past {
  background: #ecfdf5 !important;
  color: #059669 !important;
  border-color: #a7f3d0 !important;
}

.guia-step-pill.locked {
  opacity: 0.42 !important;
  cursor: not-allowed !important;
  background: rgba(148, 163, 184, 0.05) !important;
  border: 1px dashed rgba(148, 163, 184, 0.28) !important;
  color: var(--text-muted, #94a3b8) !important;
  pointer-events: none !important;
  user-select: none !important;
}

html:not([data-theme="dark"]) .guia-step-pill.locked {
  background: #f8fafc !important;
  border-color: #cbd5e1 !important;
  color: #94a3b8 !important;
}

.pill-badge {
  width: 1.1rem !important;
  height: 1.1rem !important;
  border-radius: 50% !important;
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

/* Barra de progreso integrada debajo del stepper */
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

.guia-nav-btn {
  background: rgba(148, 163, 184, 0.15) !important;
  border: 1px solid rgba(148, 163, 184, 0.3) !important;
  color: var(--toolbar-text, #f1f5f9) !important;
  padding: 0.4rem 0.85rem !important;
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

html:not([data-theme="dark"]) .guia-nav-btn {
  color: #0f172a !important;
  background: #ffffff !important;
  border-color: #cbd5e1 !important;
}

.guia-nav-btn:hover:not(:disabled) {
  background: rgba(148, 163, 184, 0.28) !important;
  border-color: var(--frontend-stroke) !important;
  transform: translateY(-1px) !important;
}

.guia-nav-btn.primary,
html:not([data-theme="dark"]) .guia-nav-btn.primary {
  background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
  color: #ffffff !important;
  border-color: #3b82f6 !important;
  box-shadow: 0 4px 14px rgba(37, 99, 235, 0.4) !important;
}

.guia-nav-btn.primary:hover:not(:disabled) {
  background: linear-gradient(135deg, #1d4ed8, #1e40af) !important;
  border-color: #60a5fa !important;
}

.guia-nav-btn:disabled {
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
  gap: 0.5rem !important;
  margin-bottom: 0.55rem !important;
  padding: 0.42rem 0.8rem !important;
  border-radius: 0.55rem !important;
  background: rgba(30, 41, 59, 0.45) !important;
  border: 1px solid rgba(148, 163, 184, 0.18) !important;
}

html:not([data-theme="dark"]) .guia-fase-hero {
  background: #f8fafc !important;
  border-color: #e2e8f0 !important;
}

.guia-fase-main {
  display: flex !important;
  align-items: center !important;
  gap: 0.55rem !important;
  flex-wrap: wrap !important;
}

.guia-pantalla-pill {
  font-size: 0.72rem !important;
  font-weight: 800 !important;
  padding: 0.2rem 0.55rem !important;
  border-radius: 0.32rem !important;
  background: #0284c7 !important;
  color: #ffffff !important;
  letter-spacing: 0.03em !important;
}

.guia-fase-title {
  margin: 0 !important;
  font-size: 0.88rem !important;
  font-weight: 700 !important;
  color: var(--toolbar-text, #f8fafc) !important;
}

html:not([data-theme="dark"]) .guia-fase-title {
  color: #0f172a !important;
}

.guia-hito-badge {
  display: inline-flex !important;
  align-items: center !important;
  gap: 0.35rem !important;
  font-size: 0.72rem !important;
  font-weight: 700 !important;
  padding: 0.22rem 0.65rem !important;
  border-radius: 0.4rem !important;
  background: rgba(16, 185, 129, 0.15) !important;
  border: 1px solid rgba(16, 185, 129, 0.35) !important;
  color: #34d399 !important;
}

html:not([data-theme="dark"]) .guia-hito-badge {
  background: #d1fae5 !important;
  color: #065f46 !important;
  border-color: #6ee7b7 !important;
}

/* Tabla 4 Columnas Densa y Optimizada */
.guia-tabla-wrap {
  width: 100% !important;
  overflow-x: auto !important;
  border-radius: 0.55rem !important;
  border: 1px solid rgba(148, 163, 184, 0.18) !important;
  background: rgba(15, 23, 42, 0.45) !important;
  margin-bottom: 0.25rem !important;
}

html:not([data-theme="dark"]) .guia-tabla-wrap {
  background: #ffffff !important;
  border-color: #cbd5e1 !important;
}

.guia-tabla {
  width: 100% !important;
  border-collapse: collapse !important;
  font-size: 0.74rem !important;
  text-align: left !important;
}

.guia-tabla th {
  background: rgba(30, 41, 59, 0.8) !important;
  color: #94a3b8 !important;
  font-weight: 700 !important;
  text-transform: uppercase !important;
  font-size: 0.64rem !important;
  letter-spacing: 0.04em !important;
  padding: 0.48rem 0.75rem !important;
  border-bottom: 1px solid rgba(148, 163, 184, 0.18) !important;
}

.guia-tabla th.th-num, .guia-tabla td.guia-td-num {
  width: 3.2rem !important;
  text-align: center !important;
  vertical-align: middle !important;
  padding: 0.45rem 0.25rem !important;
}
.guia-tabla th:nth-child(2), .guia-tabla td:nth-child(2) { width: 19% !important; }
.guia-tabla th:nth-child(3), .guia-tabla td:nth-child(3) { width: 24% !important; }
.guia-tabla th:nth-child(4), .guia-tabla td:nth-child(4) { width: 14% !important; }
.guia-tabla th:nth-child(5), .guia-tabla td:nth-child(5) { width: 38% !important; }

/* Botón de paso enumerado interactivo */
.guia-check-btn {
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
  width: 1.55rem !important;
  height: 1.55rem !important;
  border-radius: 50% !important;
  font-size: 0.72rem !important;
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
  transform: scale(1.05) !important;
}

html:not([data-theme="dark"]) .guia-tabla th {
  background: #f1f5f9 !important;
  color: #475569 !important;
  border-bottom-color: #cbd5e1 !important;
}

.guia-tabla td {
  padding: 0.45rem 0.75rem !important;
  border-bottom: 1px solid rgba(148, 163, 184, 0.12) !important;
  vertical-align: top !important;
}

.guia-tabla tr:last-child td {
  border-bottom: none !important;
}

.guia-campo {
  font-weight: 700 !important;
  color: #f8fafc !important;
  word-break: break-word !important;
}

html:not([data-theme="dark"]) .guia-campo {
  color: #0f172a !important;
}

/* Valores inteligentes */
.guia-valor {
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace !important;
  font-weight: 600 !important;
  color: #38bdf8 !important;
  background: rgba(56, 189, 248, 0.12) !important;
  padding: 0.15rem 0.45rem !important;
  border-radius: 0.35rem !important;
  display: inline-block !important;
  word-break: break-word !important;
  font-size: 0.72rem !important;
}

html:not([data-theme="dark"]) .guia-valor {
  color: #0284c7 !important;
  background: #e0f2fe !important;
}

.guia-valor.valor-vacio {
  background: rgba(245, 158, 11, 0.18) !important;
  color: #fbbf24 !important;
  border: 1px solid rgba(245, 158, 11, 0.45) !important;
  font-weight: 700 !important;
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
  font-weight: 700 !important;
}

html:not([data-theme="dark"]) .guia-valor.valor-accion {
  background: #e0e7ff !important;
  color: #4338ca !important;
  border-color: #c7d2fe !important;
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
  font-size: 0.72rem !important;
  word-break: break-word !important;
  line-height: 1.48 !important;
}

html:not([data-theme="dark"]) .guia-detalle {
  color: #334155 !important;
}

/* Footer Inferior Permanente Anclado a la Base del Modal (Fuera del Scroll) */
.guia-footer-sticky {
  flex-shrink: 0 !important;
  width: 100% !important;
  box-sizing: border-box !important;
  margin: 0 !important;
  padding: 0.65rem 1.15rem !important;
  background: rgba(15, 23, 42, 0.96) !important;
  border-top: 1px solid rgba(148, 163, 184, 0.22) !important;
  display: grid !important;
  grid-template-columns: auto 1fr auto !important;
  align-items: center !important;
  gap: 0.75rem !important;
  z-index: 40 !important;
  backdrop-filter: blur(16px) !important;
  -webkit-backdrop-filter: blur(16px) !important;
  box-shadow: 0 -4px 16px rgba(0, 0, 0, 0.28) !important;
}

html:not([data-theme="dark"]) .guia-footer-sticky {
  background: rgba(255, 255, 255, 0.98) !important;
  border-top-color: #cbd5e1 !important;
  box-shadow: 0 -4px 14px rgba(0, 0, 0, 0.06) !important;
}

.btn-pie-next {
  min-width: 9rem !important;
  max-width: 22rem !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  text-align: left !important;
  gap: 0.65rem !important;
  padding: 0.38rem 0.85rem !important;
  border-radius: 0.55rem !important;
  overflow: hidden !important;
  flex-shrink: 0 !important;
}

.btn-next-body {
  display: flex !important;
  flex-direction: column !important;
  min-width: 0 !important;
  overflow: hidden !important;
  line-height: 1.22 !important;
}

.btn-next-kicker {
  font-size: 0.64rem !important;
  font-weight: 800 !important;
  letter-spacing: 0.04em !important;
  text-transform: uppercase !important;
  opacity: 0.92 !important;
  white-space: nowrap !important;
}

.btn-next-title {
  font-size: 0.73rem !important;
  font-weight: 600 !important;
  overflow: hidden !important;
  text-overflow: ellipsis !important;
  white-space: nowrap !important;
  opacity: 0.96 !important;
}

.btn-next-arrow {
  font-size: 1.05rem !important;
  font-weight: 800 !important;
  flex-shrink: 0 !important;
  line-height: 1 !important;
}

.guia-pie-status {
  font-size: 0.74rem !important;
  color: var(--text-muted, #94a3b8) !important;
  font-weight: 600 !important;
  text-align: center !important;
  white-space: nowrap !important;
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

/* Ajuste cuando el modal está acoplado a la derecha */
.focus-chip.tiene-guia.docked-right .btn-pie-next {
  max-width: 15rem !important;
}

.focus-chip.tiene-guia.docked-right .btn-next-title {
  max-width: 8rem !important;
}

/* Modo móvil y tablets (< 768px) */
@media (max-width: 768px) {
  .focus-chip,
  .focus-chip.tiene-guia {
    position: fixed !important;
    left: 0 !important;
    right: 0 !important;
    bottom: 0 !important;
    top: auto !important;
    transform: none !important;
    width: 100vw !important;
    max-width: 100vw !important;
    height: 90vh !important;
    max-height: 90vh !important;
    border-radius: 1.15rem 1.15rem 0 0 !important;
    box-shadow: 0 -12px 40px rgba(0, 0, 0, 0.5), 0 0 0 1px var(--frontend-stroke) !important;
    margin: 0 !important;
    z-index: 100 !important;
  }

  .guia-modal-topbar {
    padding: 0.5rem 0.8rem !important;
    gap: 0.45rem !important;
  }

  .guia-brand-title {
    font-size: 0.78rem !important;
  }

  .guia-topbar-actions .btn-dock {
    display: none !important;
  }

  .btn-min-txt,
  .btn-copy-txt {
    display: none !important;
  }

  .chip-btn-ctrl {
    padding: 0.24rem 0.48rem !important;
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

  .btn-pie-prev {
    grid-area: prev !important;
    width: 100% !important;
    font-size: 0.72rem !important;
    padding: 0.4rem 0.5rem !important;
  }

  .btn-pie-next,
  .guia-pie-final {
    grid-area: next !important;
    min-width: 0 !important;
    max-width: 100% !important;
    width: 100% !important;
    font-size: 0.72rem !important;
    padding: 0.4rem 0.6rem !important;
    text-align: center !important;
  }

  .guia-campo {
    word-break: normal !important;
    margin-bottom: 0.2rem !important;
    font-size: 0.78rem !important;
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

  window.irAPaso = function(targetNodeId) {
    if (!targetNodeId) return;
    var stepKeys = Object.keys(GUIA_MAP);
    var targetIdx = stepKeys.indexOf(targetNodeId);
    if (targetIdx !== -1 && targetIdx > (window.__guiaMaxUnlocked || 0)) {
      return;
    }
    var nodeElem = document.querySelector('[data-node-id="' + targetNodeId + '"]');
    if (nodeElem) {
      nodeElem.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
      try {
        nodeElem.scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'center' });
      } catch (_) {}
      setTimeout(actualizarModalGuia, 40);
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
      var nodeElem = document.querySelector('[data-node-id="' + targetNodeId + '"]');
      if (nodeElem) {
        nodeElem.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
        try {
          nodeElem.scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'center' });
        } catch (_) {}
        setTimeout(actualizarModalGuia, 40);
      }
    }
  };

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
      html += '<thead><tr><th class="th-num">#</th><th>Campo / Acción</th><th>Valor / Ejemplo</th><th>Tipo</th><th>Detalle Operativo</th></tr></thead>';
      html += '<tbody>';
      
      var checks = (window.__guiaChecks && window.__guiaChecks[nodeId]) || {};

      info.instrucciones.forEach(function(item, rIdx) {
        var rowNum = rIdx + 1;
        var isChecked = !!checks[rIdx];
        var isCritico = (item.tipo || '').toLowerCase().indexOf('crítico') !== -1 || (item.tipo || '').toLowerCase().indexOf('guardado') !== -1;
        var tagClass = isCritico ? 'guia-tipo-tag critico' : 'guia-tipo-tag';
        var valorTxt = item.valor || '';
        var vLower = valorTxt.toLowerCase();

        var valClass = 'guia-valor';
        var valorDisplay = escapeHtml(valorTxt);
        if (vLower.indexOf('blanco') !== -1) {
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
        html += '<td><span class="' + tagClass + '">' + escapeHtml(item.tipo || '') + '</span></td>';
        html += '<td class="guia-detalle">' + escapeHtml(item.detalle || '') + '</td>';
        html += '</tr>';
      });
      html += '</tbody></table></div>';
    }

    html += '</div>';

    if (totalSteps > 1) {
      var pct = Math.round(((currentIndex + 1) / totalSteps) * 100);
      html += '<div class="guia-footer-sticky">';
      html += '<button type="button" class="guia-nav-btn btn-pie-prev" ' + (hasPrev ? 'data-nav-paso="-1"' : 'disabled') + '>← Paso anterior</button>';
      html += '<div class="guia-pie-status">Paso ' + (currentIndex + 1) + ' de ' + totalSteps + ' · ' + pct + '% completado</div>';
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
    var head = chip.querySelector('.relationship-lens-head');
    if (!head) return;

    var topbar = head.querySelector('.guia-modal-topbar');
    if (topbar) return;

    topbar = document.createElement('div');
    topbar.className = 'guia-modal-topbar';
    topbar.innerHTML = '<div class="guia-modal-brand">' +
      '<span class="guia-brand-badge">BANNER TEST</span>' +
      '<span class="guia-brand-title">Guía Operativa Paso a Paso</span>' +
      '</div>' +
      '<div class="guia-topbar-actions">' +
      '<button type="button" class="chip-btn-ctrl btn-dock" title="Alternar entre modal amplio centrado y panel lateral derecho">◨ <span class="btn-dock-txt">Acoplar lateral</span></button>' +
      '<button type="button" class="chip-btn-ctrl btn-min" title="Minimizar a píldora flotante">─ <span class="btn-min-txt">Minimizar</span></button>' +
      '<button type="button" class="chip-btn-ctrl btn-copy" title="Copiar enlace directo a este paso">🔗 <span class="btn-copy-txt">Copiar enlace</span></button>' +
      '<button type="button" class="chip-btn-close" title="Cerrar ventana">✕</button>' +
      '</div>';

    head.insertBefore(topbar, head.firstChild);

    var btnDock = topbar.querySelector('.btn-dock');
    btnDock.addEventListener('click', function(e) {
      e.stopPropagation();
      var isDocked = chip.classList.toggle('docked-right');
      chip.classList.remove('chip-minimized');
      topbar.querySelector('.btn-dock-txt').textContent = isDocked ? 'Centrar amplio' : 'Acoplar lateral';
    });

    var btnMin = topbar.querySelector('.btn-min');
    btnMin.addEventListener('click', function(e) {
      e.stopPropagation();
      var isMin = chip.classList.toggle('chip-minimized');
      topbar.querySelector('.btn-min-txt').textContent = isMin ? 'Expandir' : 'Minimizar';
    });

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
      var clearBtn = document.getElementById('btn-focus-clear');
      if (clearBtn) clearBtn.click();
      else chip.hidden = true;
    });

    topbar.addEventListener('click', function(e) {
      if (chip.classList.contains('chip-minimized') && !e.target.closest('button')) {
        chip.classList.remove('chip-minimized');
        topbar.querySelector('.btn-min-txt').textContent = 'Minimizar';
      }
    });
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
      return;
    }

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

    chip.classList.add('tiene-guia');
    card.innerHTML = renderGuiaHtml(info, nodeId);

    var scrollBody = card.querySelector('.guia-body-scroll');
    if (scrollBody) {
      scrollBody.scrollTop = 0;
    }

    setTimeout(function() {
      var activePill = card.querySelector('.guia-step-pill.active');
      if (activePill) {
        try {
          activePill.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' });
        } catch (_) {}
      }
    }, 60);
  }

  document.addEventListener('DOMContentLoaded', function() {
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
        setTimeout(actualizarModalGuia, 20);
        setTimeout(actualizarModalGuia, 120);
      }
    });

    document.addEventListener('keydown', function(e) {
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.target.tagName === 'SELECT') return;
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

    actualizarModalGuia();
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
        btn_prev_top = f'''<a href="{flujo_ant['url']}" class="flow-btn-top prev" title="Flujo anterior: {flujo_ant['titulo']}">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="15 18 9 12 15 6"></polyline></svg>
        <span>Anterior</span>
      </a>'''
    else:
        btn_prev_top = '''<span class="flow-btn-top prev disabled" title="Primer flujo de este centro">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="15 18 9 12 15 6"></polyline></svg>
        <span>Anterior</span>
      </span>'''

    if flujo_sig:
        btn_next_top = f'''<a href="{flujo_sig['url']}" class="flow-btn-top next primary" title="Siguiente flujo: {flujo_sig['titulo']}">
        <span>Siguiente</span>
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"></polyline></svg>
      </a>'''
    else:
        btn_next_top = '''<span class="flow-btn-top next disabled" title="Último flujo de este centro">
        <span>Siguiente</span>
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
        <span class="flow-nav-center-tag">
          <span class="flow-center-dot" style="background:{color_centro}"></span>
          {nombre_centro}
        </span>
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

    # Tarjetas pie (Bottom)
    if flujo_ant:
        card_prev = f'''<a href="{flujo_ant['url']}" class="flow-bottom-card prev" title="Ir al flujo anterior: {flujo_ant['titulo']}">
          <div class="flow-card-badge">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="15 18 9 12 15 6"></polyline></svg>
            <span>Flujo anterior</span>
          </div>
          <div class="flow-card-num-title">
            <span class="flow-card-num">{flujo_ant['num']:02d}</span>
            <span class="flow-card-title">{flujo_ant['titulo']}</span>
          </div>
          <div class="flow-card-meta">{flujo_ant['cap'] or 'Capacidades Banner'}</div>
        </a>'''
    else:
        card_prev = '''<div class="flow-bottom-card prev placeholder">
          <div class="flow-card-badge"><span>Inicio del recorrido</span></div>
          <div class="flow-card-title muted">Este es el primer flujo del centro</div>
        </div>'''

    if flujo_sig:
        card_next = f'''<a href="{flujo_sig['url']}" class="flow-bottom-card next primary-accent" title="Avanzar al siguiente flujo: {flujo_sig['titulo']}">
          <div class="flow-card-badge">
            <span>Siguiente flujo</span>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"></polyline></svg>
          </div>
          <div class="flow-card-num-title">
            <span class="flow-card-num">{flujo_sig['num']:02d}</span>
            <span class="flow-card-title">{flujo_sig['titulo']}</span>
          </div>
          <div class="flow-card-meta">{flujo_sig['cap'] or 'Capacidades Banner'}</div>
        </a>'''
    else:
        card_next = f'''<div class="flow-bottom-card next placeholder">
          <div class="flow-card-badge"><span>Fin del recorrido</span></div>
          <div class="flow-card-title muted">¡Completaste todos los flujos de {nombre_centro}!</div>
        </div>'''

    html_nav_bottom = f'''<!-- === FLOW NAV BOTTOM === -->
    <nav class="flow-nav-bottom-section" aria-label="Paginación de flujos al pie">
      <div class="flow-bottom-container">
        <div class="flow-bottom-col prev-col">
          {card_prev}
        </div>
        <div class="flow-bottom-col hub-col">
          <a href="{url_centros}" class="flow-bottom-hub-btn" title="Ver galería y todos los flujos de {nombre_centro}">
            <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect x="3" y="3" width="7" height="7"></rect>
              <rect x="14" y="3" width="7" height="7"></rect>
              <rect x="14" y="14" width="7" height="7"></rect>
              <rect x="3" y="14" width="7" height="7"></rect>
            </svg>
            <span>Ver todos los flujos ({nombre_centro})</span>
          </a>
        </div>
        <div class="flow-bottom-col next-col">
          {card_next}
        </div>
      </div>
    </nav>
    <!-- === /FLOW NAV BOTTOM === -->'''

    return {
        "nav_top": html_nav_top,
        "nav_bottom": html_nav_bottom,
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

    # Inyectar navegación inferior antes de <nav class="node-outline
    if '<nav class="node-outline' in contenido:
        contenido = contenido.replace('<nav class="node-outline', f'{nav_data["nav_bottom"]}\n    <nav class="node-outline', 1)
    elif '</div>\n  </div>' in contenido:
        contenido = contenido.replace('</div>\n  </div>', f'{nav_data["nav_bottom"]}\n  </div>', 1)

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
