"""Inyecta guías operativas interactivas directamente en el modal (Pasaporte semántico) de los diagramas Archify.

Al hacer clic sobre cualquier nodo del flujo en el navegador, el modal lateral `#focus-chip`
despliega la ficha operativa completa (paso a paso, campos, valores, guardados F10 y atajos),
eliminando la necesidad de tarjetas largas de texto al pie de página.
"""
import json
import re
from pathlib import Path
from guias_operativas import obtener_guia, GUIAS_BASE, GUIAS_SCRIPTS

CSS_MODAL = """
/* === DISEÑO RESPONSIVO Y GUÍA OPERATIVA (PASAPORTE SEMÁNTICO) === */

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
    /* 2 a 3 columnas equilibradas para evitar columnas angostas aplastadas */
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
  min-height: min(30rem, 60vh) !important;
  max-height: min(92vh, calc(100vh - 1.5rem)) !important;
  display: flex !important;
  flex-direction: column !important;
  overflow: hidden !important;
  border-radius: 1rem !important;
  box-shadow: 0 32px 90px rgba(0, 0, 0, 0.75), 0 0 0 1px var(--frontend-stroke) !important;
  backdrop-filter: blur(25px) !important;
  -webkit-backdrop-filter: blur(25px) !important;
  z-index: 95 !important;
  background: var(--panel, #0f172a) !important;
  margin: 0 !important;
}

/* Modo acoplado a la derecha en escritorio */
.focus-chip.tiene-guia.docked-right {
  position: fixed !important;
  left: auto !important;
  right: 1.25rem !important;
  top: 1.25rem !important;
  bottom: 1.25rem !important;
  transform: none !important;
  width: min(44rem, calc(50vw - 1.5rem)) !important;
  max-width: 46rem !important;
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
  width: auto !important;
  min-width: 22rem !important;
  max-width: calc(100vw - 3rem) !important;
  max-height: 3.2rem !important;
  height: 3.2rem !important;
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

/* Estructura del Head de Archify */
.focus-chip.tiene-guia .relationship-lens-head {
  display: flex !important;
  flex-direction: column !important;
  padding: 0 !important;
  margin: 0 !important;
  border: none !important;
  width: 100% !important;
  height: 100% !important;
  max-height: 100% !important;
  overflow: hidden !important;
  background: transparent !important;
}

/* Barra superior unificada esbelta */
.guia-modal-topbar {
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  padding: 0.45rem 1rem !important;
  background: linear-gradient(135deg, rgba(30, 41, 59, 0.85), rgba(15, 23, 42, 0.98)) !important;
  border-bottom: 1px solid rgba(148, 163, 184, 0.18) !important;
  flex-shrink: 0 !important;
  z-index: 10 !important;
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
}

.guia-brand-badge {
  font-size: 0.66rem !important;
  font-weight: 800 !important;
  text-transform: uppercase !important;
  letter-spacing: 0.05em !important;
  padding: 0.18rem 0.5rem !important;
  border-radius: 0.35rem !important;
  background: #4338ca !important;
  color: #ffffff !important;
}

.guia-brand-title {
  font-size: 0.84rem !important;
  font-weight: 700 !important;
  color: var(--toolbar-text, #f8fafc) !important;
}

html:not([data-theme="dark"]) .guia-brand-title {
  color: #0f172a !important;
}

.guia-topbar-actions {
  display: inline-flex !important;
  align-items: center !important;
  gap: 0.35rem !important;
}

.chip-btn-ctrl {
  background: rgba(148, 163, 184, 0.12) !important;
  border: 1px solid rgba(148, 163, 184, 0.25) !important;
  color: var(--toolbar-text, #e2e8f0) !important;
  border-radius: 0.45rem !important;
  padding: 0.22rem 0.55rem !important;
  font-size: 0.7rem !important;
  font-weight: 600 !important;
  cursor: pointer !important;
  display: inline-flex !important;
  align-items: center !important;
  gap: 0.3rem !important;
  transition: all 0.15s ease !important;
  line-height: 1.2 !important;
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
  width: 1.7rem !important;
  height: 1.7rem !important;
  border-radius: 50% !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  font-size: 1rem !important;
  line-height: 1 !important;
  padding: 0 !important;
  background: rgba(239, 68, 68, 0.12) !important;
  border: 1px solid rgba(239, 68, 68, 0.3) !important;
  color: #f87171 !important;
  cursor: pointer !important;
  transition: all 0.15s ease !important;
  margin-left: 0.25rem !important;
}

.chip-btn-close:hover {
  background: #ef4444 !important;
  color: #ffffff !important;
  border-color: #ef4444 !important;
  transform: scale(1.08) !important;
}

/* Cuerpo con scroll suave y padding compacto */
.focus-chip.tiene-guia .relationship-lens-copy {
  width: 100% !important;
  min-width: 0 !important;
  display: flex !important;
  flex-direction: column !important;
  flex: 1 1 auto !important;
  overflow-y: auto !important;
  overflow-x: hidden !important;
  padding: 0.5rem 1rem 0 1rem !important;
  scrollbar-width: thin !important;
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

.guia-operativa-card {
  margin: 0 !important;
  padding: 0 !important;
  border: none !important;
  background: transparent !important;
  display: flex !important;
  flex-direction: column !important;
  flex: 1 1 auto !important;
}

/* Stepper de Fases Interactivo Horizontal Compacto */
.guia-stepper-wrap {
  overflow-x: auto !important;
  scrollbar-width: thin !important;
  -webkit-overflow-scrolling: touch !important;
  padding: 0.1rem 0 0.4rem 0 !important;
  margin-bottom: 0.45rem !important;
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
  padding: 0.22rem 0.65rem !important;
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

.stepper-arrow {
  color: rgba(148, 163, 184, 0.4) !important;
  font-size: 0.8rem !important;
  user-select: none !important;
  flex-shrink: 0 !important;
}

.stepper-arrow.past {
  color: #10b981 !important;
}

/* Barra de progreso integrada debajo del stepper */
.guia-stepper-progress {
  width: 100% !important;
  height: 3px !important;
  background: rgba(148, 163, 184, 0.2) !important;
  border-radius: 2px !important;
  overflow: hidden !important;
  margin-top: 0.35rem !important;
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
  padding: 0.35rem 0.75rem !important;
  border-radius: 0.45rem !important;
  font-size: 0.74rem !important;
  font-weight: 700 !important;
  cursor: pointer !important;
  display: inline-flex !important;
  align-items: center !important;
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
  opacity: 0.35 !important;
  cursor: not-allowed !important;
  transform: none !important;
}

/* Hero de Fase actual e Hito Compacto */
.guia-fase-hero {
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  flex-wrap: wrap !important;
  gap: 0.45rem !important;
  margin-bottom: 0.45rem !important;
  padding: 0.35rem 0.75rem !important;
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
  gap: 0.5rem !important;
  flex-wrap: wrap !important;
}

.guia-pantalla-pill {
  font-size: 0.72rem !important;
  font-weight: 800 !important;
  padding: 0.18rem 0.5rem !important;
  border-radius: 0.3rem !important;
  background: #0284c7 !important;
  color: #ffffff !important;
  letter-spacing: 0.03em !important;
}

.guia-fase-title {
  margin: 0 !important;
  font-size: 0.86rem !important;
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
  padding: 0.22rem 0.6rem !important;
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
  margin-bottom: 0.45rem !important;
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
  padding: 0.45rem 0.75rem !important;
  border-bottom: 1px solid rgba(148, 163, 184, 0.18) !important;
}

.guia-tabla th:nth-child(1), .guia-tabla td:nth-child(1) { width: 18% !important; }
.guia-tabla th:nth-child(2), .guia-tabla td:nth-child(2) { width: 24% !important; }
.guia-tabla th:nth-child(3), .guia-tabla td:nth-child(3) { width: 14% !important; }
.guia-tabla th:nth-child(4), .guia-tabla td:nth-child(4) { width: 44% !important; }

html:not([data-theme="dark"]) .guia-tabla th {
  background: #f1f5f9 !important;
  color: #475569 !important;
  border-bottom-color: #cbd5e1 !important;
}

.guia-tabla td {
  padding: 0.4rem 0.75rem !important;
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
  padding: 0.14rem 0.45rem !important;
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
  padding: 0.12rem 0.4rem !important;
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
  line-height: 1.45 !important;
}

html:not([data-theme="dark"]) .guia-detalle {
  color: #334155 !important;
}

/* Sticky Footer Inferior Permanente Esbelto */
.guia-footer-sticky {
  position: sticky !important;
  bottom: 0 !important;
  left: 0 !important;
  right: 0 !important;
  background: rgba(15, 23, 42, 0.96) !important;
  padding: 0.55rem 1rem !important;
  margin: 0.65rem -1rem 0 -1rem !important;
  border-top: 1px solid rgba(148, 163, 184, 0.2) !important;
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  gap: 0.75rem !important;
  z-index: 40 !important;
  backdrop-filter: blur(16px) !important;
  -webkit-backdrop-filter: blur(16px) !important;
  box-shadow: 0 -4px 16px rgba(0, 0, 0, 0.35) !important;
}

html:not([data-theme="dark"]) .guia-footer-sticky {
  background: rgba(255, 255, 255, 0.98) !important;
  border-top-color: #cbd5e1 !important;
  box-shadow: 0 -4px 14px rgba(0, 0, 0, 0.06) !important;
}

.btn-pie-next {
  min-width: 12rem !important;
  justify-content: center !important;
  font-size: 0.78rem !important;
  padding: 0.42rem 1.1rem !important;
  border-radius: 0.5rem !important;
}

.guia-pie-status {
  font-size: 0.74rem !important;
  color: var(--text-muted, #94a3b8) !important;
  font-weight: 600 !important;
}

html:not([data-theme="dark"]) .guia-pie-status {
  color: #64748b !important;
}

.guia-pie-final {
  font-size: 0.78rem !important;
  font-weight: 700 !important;
  color: #34d399 !important;
}

/* Modo móvil */
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
    border-radius: 1.25rem 1.25rem 0 0 !important;
    box-shadow: 0 -12px 40px rgba(0, 0, 0, 0.5), 0 0 0 1px var(--frontend-stroke) !important;
    margin: 0 !important;
    z-index: 100 !important;
  }

  .guia-modal-topbar {
    padding: 0.45rem 0.75rem !important;
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
    padding: 0.2rem 0.4rem !important;
  }

  .focus-chip.tiene-guia .relationship-lens-copy {
    padding: 0.5rem 0.75rem 0 0.75rem !important;
  }

  .guia-footer-sticky {
    padding: 0.55rem 0.75rem !important;
    margin: auto -0.75rem 0 -0.75rem !important;
  }

  .btn-pie-next {
    min-width: auto !important;
    flex: 1 !important;
    font-size: 0.74rem !important;
    padding: 0.42rem 0.65rem !important;
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

  window.irAPaso = function(targetNodeId) {
    if (!targetNodeId) return;
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
    var nextIndex = currentIndex + offset;
    if (nextIndex >= 0 && nextIndex < stepKeys.length) {
      window.irAPaso(stepKeys[nextIndex]);
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

    var html = '';

    // 1. Stepper horizontal interactivo con todas las fases y barrita de progreso integrada
    if (totalSteps > 1) {
      var progressPct = Math.round(((currentIndex + 1) / totalSteps) * 100);
      html += '<div class="guia-stepper-wrap">';
      html += '<div class="guia-stepper-track" role="tablist" aria-label="Fases del flujo">';
      stepKeys.forEach(function(k, idx) {
        var sInfo = GUIA_MAP[k];
        var isAct = (k === nodeId);
        var isPast = (idx < currentIndex);
        var label = sInfo.fase ? sInfo.fase.replace(/^Paso\s*\d+:\s*/i, '') : (sInfo.pantalla || ('Paso ' + (idx + 1)));

        var pillClass = 'guia-step-pill';
        if (isAct) pillClass += ' active';
        else if (isPast) pillClass += ' past';

        var badgeTxt = isPast ? '✓' : (idx + 1);

        html += '<button type="button" class="' + pillClass + '" data-ir-paso="' + escapeHtml(k) + '" title="Ir al paso ' + (idx + 1) + ': ' + escapeHtml(label) + '">';
        html += '<span class="pill-badge">' + badgeTxt + '</span>';
        html += '<span>' + escapeHtml(label) + '</span>';
        html += '</button>';

        if (idx < totalSteps - 1) {
          var arrowClass = 'stepper-arrow' + (isPast ? ' past' : '');
          html += '<span class="' + arrowClass + '">›</span>';
        }
      });
      html += '</div>';
      html += '<div class="guia-stepper-progress"><div class="guia-progress-fill" style="width:' + progressPct + '%;"></div></div>';
      html += '</div>';
    }

    // 2. Hero de fase actual y pantalla Banner compacto
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

    // 3. Tabla de instrucciones operativas compacta con valores inteligentes
    if (info.instrucciones && info.instrucciones.length > 0) {
      html += '<div class="guia-tabla-wrap"><table class="guia-tabla">';
      html += '<thead><tr><th>Campo / Acción</th><th>Valor / Ejemplo</th><th>Tipo</th><th>Detalle Operativo</th></tr></thead>';
      html += '<tbody>';
      info.instrucciones.forEach(function(item) {
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

        html += '<tr>';
        html += '<td class="guia-campo">' + escapeHtml(item.campo || '') + '</td>';
        html += '<td><span class="' + valClass + '">' + valorDisplay + '</span></td>';
        html += '<td><span class="' + tagClass + '">' + escapeHtml(item.tipo || '') + '</span></td>';
        html += '<td class="guia-detalle">' + escapeHtml(item.detalle || '') + '</td>';
        html += '</tr>';
      });
      html += '</tbody></table></div>';
    }

    // 4. Sticky Footer inferior permanente esbelto
    if (totalSteps > 1) {
      var pct = Math.round(((currentIndex + 1) / totalSteps) * 100);
      html += '<div class="guia-footer-sticky">';
      html += '<button type="button" class="guia-nav-btn btn-pie-prev" ' + (hasPrev ? 'data-nav-paso="-1"' : 'disabled') + '>← Paso anterior</button>';
      html += '<div class="guia-pie-status">Paso ' + (currentIndex + 1) + ' de ' + totalSteps + ' · ' + pct + '% completado</div>';
      if (hasNext) {
        html += '<button type="button" class="guia-nav-btn btn-pie-next primary" data-nav-paso="1">Siguiente: ' + escapeHtml(nextTitle) + ' →</button>';
      } else {
        html += '<span class="guia-pie-final">✓ Flujo completado con éxito</span>';
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
      var url = nodeId ? (base + '#' + encodeURIComponent(nodeId)) : base;
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

    // Reset de scroll al inicio del paso
    var copyElem = chip.querySelector('.relationship-lens-copy');
    if (copyElem) {
      copyElem.scrollTop = 0;
    }

    // Centrar suavemente la píldora activa en el Stepper horizontal
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

      var node = e.target.closest('[data-node-id]');
      if (node) {
        setTimeout(actualizarModalGuia, 20);
        setTimeout(actualizarModalGuia, 120);
      }
    });

    // Atajos de teclado para navegación paso a paso
    document.addEventListener('keydown', function(e) {
      var chip = document.getElementById('focus-chip');
      if (!chip || chip.hidden || !chip.classList.contains('tiene-guia')) return;
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
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


def inyectar_en_html(ruta_html, slug):
    """Inyecta el CSS responsivo y JS de la guía operativa en el HTML generado."""
    ruta_str = str(ruta_html).lower()
    id_centro = "idiomas" if "idiomas" in ruta_str else ("computacion" if "computacion" in ruta_str else ("emprendimiento" if "emprendimiento" in ruta_str else ""))
    guia = obtener_guia_para_slug(slug, id_centro) or {}

    contenido = ruta_html.read_text(encoding="utf-8")
    if "/* === DISEÑO RESPONSIVO" in contenido or "guia-operativa-card" in contenido:
        # Ya está inyectado, limpiar versión anterior
        contenido = re.sub(r"<style>\s*/\* === (?:DISEÑO RESPONSIVO|GUÍA OPERATIVA).*?<\/script>", "", contenido, flags=re.DOTALL)

    guia_json = json.dumps(guia, ensure_ascii=False)
    bloque = JS_SCRIPT_TEMPLATE.replace("__CSS__", CSS_MODAL).replace("__GUIA_JSON__", guia_json)

    if "</body>" in contenido:
        nuevo_contenido = contenido.replace("</body>", f"{bloque}\n</body>")
    else:
        nuevo_contenido = contenido + "\n" + bloque

    ruta_html.write_text(nuevo_contenido, encoding="utf-8")
    return True

