/**
 * ELLUCIAN INSTRUCTIVOS - WORKSPACE EXPLORER & HD PPTX CANVAS VIEWER
 * Uses pptx-browser (Canvas renderer) for pixel-perfect slide rendering
 * with theme colors, gradient backgrounds, images, and layout inheritance.
 */

const STORAGE_KEY = 'ellucian_instructivos_state_v8';
const DEFAULT_PRES_ID = '1.1.1_Definir_la_estructura_de_los_periodos_acade_micos';

/**
 * Recursively sort tree nodes naturally (1, 2, ..., 9, 10, 11)
 */
function naturalSortTree(nodes) {
  if (!nodes || !Array.isArray(nodes)) return;
  nodes.sort((a, b) => (a.name || '').localeCompare(b.name || '', undefined, { numeric: true, sensitivity: 'base' }));
  nodes.forEach(n => {
    if (n.children && Array.isArray(n.children)) {
      naturalSortTree(n.children);
    }
  });
}

/**
 * Recursively extracts all folder paths in the tree
 */
function getAllFolderPaths(nodes) {
  const paths = [];
  function recurse(list) {
    if (!list || !Array.isArray(list)) return;
    for (const node of list) {
      if (node.type === 'directory' || (node.children && node.children.length > 0)) {
        if (node.path) paths.push(node.path);
        recurse(node.children);
      }
    }
  }
  recurse(nodes);
  return paths;
}

/**
 * Returns default clean state with all top-level capacity folders open
 */
function getDefaultState() {
  const defaultExpanded = new Set();

  if (typeof APP_TREE !== 'undefined' && APP_TREE.children) {
    // Open all top-level capacity folders (CAPACIDAD 1, 3, 4, 5, 6, 7, 8, 9, 10, 11)
    APP_TREE.children.forEach(node => {
      if (node.type === 'directory' && node.path) {
        defaultExpanded.add(node.path);
      }
    });
  }

  // Also ensure default presentation path is expanded
  defaultExpanded.add('CAPACIDAD 1');
  defaultExpanded.add('CAPACIDAD 1/1.1 Diseño Curricular');

  return {
    currentId: DEFAULT_PRES_ID,
    currentSlide: 0,
    currentView: 'slides',
    renderer: null,
    thumbnailsVisible: false,
    expandedFolders: defaultExpanded
  };
}

/**
 * Loads saved state from localStorage (persisted on F5)
 */
function loadPersistedState() {
  // If URL has ?reset or #reset, force clean default
  if (typeof window !== 'undefined' && window.location && (window.location.search?.includes('reset') || window.location.hash?.includes('reset'))) {
    try {
      localStorage.removeItem(STORAGE_KEY);
      sessionStorage.removeItem(STORAGE_KEY);
    } catch (e) {}
    if (window.history?.replaceState) {
      window.history.replaceState(null, '', window.location.pathname);
    }
    return getDefaultState();
  }

  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) {
      const parsed = JSON.parse(raw);
      if (parsed && parsed.currentId) {
        // Validate presentation exists if metadata loaded
        if (typeof PRESENTATIONS === 'undefined' || PRESENTATIONS[parsed.currentId]) {
          const expanded = (Array.isArray(parsed.expandedFolders) && parsed.expandedFolders.length > 0)
            ? new Set(parsed.expandedFolders)
            : getDefaultState().expandedFolders;

          // Always ensure all top-level capacity folders are opened on startup
          if (typeof APP_TREE !== 'undefined' && APP_TREE.children) {
            APP_TREE.children.forEach(cap => {
              if (cap.type === 'directory' && cap.path) {
                expanded.add(cap.path);
              }
            });
          }

          return {
            currentId: parsed.currentId,
            currentSlide: typeof parsed.currentSlide === 'number' && parsed.currentSlide >= 0 ? parsed.currentSlide : 0,
            currentView: 'slides',
            renderer: null,
            thumbnailsVisible: false,
            expandedFolders: expanded
          };
        }
      }
    }
  } catch (err) {
    console.warn('Error reading persisted state:', err);
  }

  return getDefaultState();
}

function initApp() {
  // 1. Natural sort of tree items (CAPACIDAD 1..9, 10, 11)
  if (typeof APP_TREE !== 'undefined' && APP_TREE.children) {
    naturalSortTree(APP_TREE.children);
  }

  // 2. Load state (from F5 persistence or clean default)
  const state = {
    ...loadPersistedState(),
    zoom: 1.0,
    panX: 0,
    panY: 0,
    handMode: false
  };

  // Ensure all top-level capacity folders are open on startup
  if (typeof APP_TREE !== 'undefined' && APP_TREE.children) {
    APP_TREE.children.forEach(cap => {
      if (cap.type === 'directory' && cap.path) {
        state.expandedFolders.add(cap.path);
      }
    });
  }

  // Also ensure parents of current presentation are expanded
  ensureAncestorsExpanded(state.currentId);

  const elements = {
    appContainer: document.getElementById('app-container'),
    sidebar: document.getElementById('sidebar'),
    sidebarOverlay: document.getElementById('sidebar-overlay'),
    btnToggleSidebar: document.getElementById('btn-toggle-sidebar'),
    btnExpandSidebar: document.getElementById('btn-expand-sidebar'),
    btnCloseSidebarMobile: document.getElementById('btn-close-sidebar-mobile'),
    btnCollapseAll: document.getElementById('btn-collapse-all'),
    btnResetDefault: document.getElementById('btn-reset-default'),
    searchInput: document.getElementById('search-input'),
    searchClear: document.getElementById('search-clear'),
    explorerTree: document.getElementById('explorer-tree'),
    currentTitle: document.getElementById('current-title'),
    breadcrumbs: document.getElementById('breadcrumbs'),
    viewSlides: document.getElementById('view-slides'),
    
    // Stage & Canvas
    presentationStage: document.getElementById('presentation-stage'),
    slideViewport: document.getElementById('slide-viewport'),
    slideCanvasWrapper: document.getElementById('slide-canvas-wrapper'),
    slideCanvas: document.getElementById('slide-canvas'),
    loadingOverlay: document.getElementById('loading-overlay'),
    loadingMsg: document.getElementById('loading-msg'),
    
    // Floating Zoom & Pan HUD Toolbar
    slideZoomToolbar: document.getElementById('slide-zoom-toolbar'),
    btnToolHand: document.getElementById('btn-tool-hand'),
    btnZoomOut: document.getElementById('btn-zoom-out'),
    btnZoomReset: document.getElementById('btn-zoom-reset'),
    zoomLevelText: document.getElementById('zoom-level-text'),
    btnZoomIn: document.getElementById('btn-zoom-in'),
    btnZoomFit: document.getElementById('btn-zoom-fit'),
    
    // Slide Controls
    btnPrevSlide: document.getElementById('btn-prev-slide'),
    btnNextSlide: document.getElementById('btn-next-slide'),
    btnFirstSlide: document.getElementById('btn-first-slide'),
    btnPrev: document.getElementById('btn-prev'),
    btnNext: document.getElementById('btn-next'),
    btnLastSlide: document.getElementById('btn-last-slide'),
    slideCounter: document.getElementById('slide-counter'),
    
    // Actions & Strip
    thumbnailStrip: document.getElementById('thumbnail-strip'),
    btnToggleThumbs: document.getElementById('btn-toggle-thumbs'),
    thumbsLabel: document.getElementById('thumbs-label'),
    btnTopFullscreen: document.getElementById('btn-top-fullscreen'),
    btnFooterFullscreen: document.getElementById('btn-footer-fullscreen'),
    btnDownloadPptx: document.getElementById('btn-download-pptx')
  };

  // =========================================================================
  // STATE PERSISTENCE HELPERS
  // =========================================================================

  function saveState() {
    try {
      const payload = {
        currentId: state.currentId,
        currentSlide: state.currentSlide,
        currentView: state.currentView,
        expandedFolders: Array.from(state.expandedFolders)
      };
      localStorage.setItem(STORAGE_KEY, JSON.stringify(payload));
    } catch (e) {
      console.warn('Error saving state:', e);
    }
  }

  function resetToDefault() {
    try {
      localStorage.removeItem(STORAGE_KEY);
      sessionStorage.removeItem(STORAGE_KEY);
    } catch (e) {}

    const def = getDefaultState();
    state.currentId = def.currentId;
    state.currentSlide = def.currentSlide;
    state.currentView = def.currentView;
    state.expandedFolders = def.expandedFolders;

    ensureAncestorsExpanded(state.currentId);
    renderTree(elements.searchInput.value);
    elements.viewSlides.classList.add('active');
    loadPresentation(state.currentId, 0);
  }

  function ensureAncestorsExpanded(presId) {
    if (typeof PRESENTATIONS === 'undefined') return;
    const pres = PRESENTATIONS[presId];
    if (!pres || !pres.path) return;

    const parts = pres.path.split('/');
    let acc = '';
    for (let i = 0; i < parts.length - 1; i++) {
      acc = acc ? `${acc}/${parts[i]}` : parts[i];
      state.expandedFolders.add(acc);
    }
  }

  // =========================================================================
  // TREE NAVIGATION & EXPLORER
  // =========================================================================

  function renderTree(filterQuery = '') {
    elements.explorerTree.innerHTML = '';
    const q = filterQuery.toLowerCase().trim();

    if (typeof APP_TREE === 'undefined' || !APP_TREE.children) {
      elements.explorerTree.innerHTML = '<div class="empty-desc" style="padding: 16px; color:#94a3b8;">Cargando instructivos...</div>';
      return;
    }

    APP_TREE.children.forEach(capNode => {
      const nodeEl = createTreeNode(capNode, q);
      if (nodeEl) {
        elements.explorerTree.appendChild(nodeEl);
      }
    });

    updateActiveTreeItem(state.currentId);
  }

  function createTreeNode(node, filterQuery = '') {
    const isDir = node.type === 'directory';
    const isFile = node.type === 'file';

    if (filterQuery) {
      if (isFile) {
        const matchTitle = node.name.toLowerCase().includes(filterQuery);
        const pres = (typeof PRESENTATIONS !== 'undefined') ? PRESENTATIONS[node.id] : null;
        const matchForms = pres && pres.forms && pres.forms.some(f => f.toLowerCase().includes(filterQuery));
        if (!matchTitle && !matchForms) return null;
      } else if (isDir) {
        const matchedChildren = [];
        if (node.children) {
          node.children.forEach(c => {
            const childNode = createTreeNode(c, filterQuery);
            if (childNode) matchedChildren.push(childNode);
          });
        }
        if (matchedChildren.length === 0 && !node.name.toLowerCase().includes(filterQuery)) {
          return null;
        }
      }
    }

    const container = document.createElement('div');
    container.className = 'tree-node';

    const itemEl = document.createElement('div');
    itemEl.className = 'tree-item';
    if (isFile) {
      itemEl.setAttribute('data-id', node.id);
      if (node.id === state.currentId) {
        itemEl.classList.add('active');
      }
    }

    if (isDir) {
      const chevron = document.createElement('span');
      chevron.className = 'tree-chevron';
      const isExpanded = filterQuery ? true : state.expandedFolders.has(node.path);
      if (isExpanded) chevron.classList.add('expanded');
      chevron.innerHTML = `<svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"/></svg>`;
      itemEl.appendChild(chevron);

      const icon = document.createElement('span');
      icon.className = 'tree-icon folder-icon';
      icon.innerHTML = isExpanded
        ? `<svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><path d="M19 20H5a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h5l2 2h7a2 2 0 0 1 2 2v2H6a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h13a2 2 0 0 0 2-2v-5h2v5a2 2 0 0 1-2 2z"/></svg>`
        : `<svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><path d="M10 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2h-8l-2-2z"/></svg>`;
      itemEl.appendChild(icon);
    } else {
      const spacer = document.createElement('span');
      spacer.style.width = '14px';
      spacer.style.flexShrink = '0';
      itemEl.appendChild(spacer);

      const icon = document.createElement('span');
      icon.className = 'tree-icon file-icon';
      icon.innerHTML = `<svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/></svg>`;
      itemEl.appendChild(icon);
    }

    const label = document.createElement('span');
    label.className = 'tree-label';
    label.textContent = node.name.replace('.pptx', '');
    label.title = node.name;
    itemEl.appendChild(label);

    if (isFile && node.size) {
      const badge = document.createElement('span');
      badge.className = 'slide-badge';
      badge.textContent = node.size;
      itemEl.appendChild(badge);
    }

    container.appendChild(itemEl);

    if (isDir) {
      const childrenWrapper = document.createElement('div');
      childrenWrapper.className = 'tree-children';
      const isExpanded = filterQuery ? true : state.expandedFolders.has(node.path);
      if (isExpanded) childrenWrapper.classList.add('expanded');

      if (node.children) {
        node.children.forEach(c => {
          const childNode = createTreeNode(c, filterQuery);
          if (childNode) childrenWrapper.appendChild(childNode);
        });
      }

      container.appendChild(childrenWrapper);

      itemEl.addEventListener('click', (e) => {
        e.stopPropagation();
        const currentlyExpanded = childrenWrapper.classList.contains('expanded');
        const chevron = itemEl.querySelector('.tree-chevron');
        const folderIcon = itemEl.querySelector('.folder-icon');
        if (currentlyExpanded) {
          childrenWrapper.classList.remove('expanded');
          chevron?.classList.remove('expanded');
          if (folderIcon) {
            folderIcon.innerHTML = `<svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><path d="M10 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2h-8l-2-2z"/></svg>`;
          }
          state.expandedFolders.delete(node.path);
        } else {
          childrenWrapper.classList.add('expanded');
          chevron?.classList.add('expanded');
          if (folderIcon) {
            folderIcon.innerHTML = `<svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><path d="M19 20H5a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h5l2 2h7a2 2 0 0 1 2 2v2H6a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h13a2 2 0 0 0 2-2v-5h2v5a2 2 0 0 1-2 2z"/></svg>`;
          }
          state.expandedFolders.add(node.path);
        }
        saveState();
      });
    } else if (isFile) {
      itemEl.addEventListener('click', (e) => {
        e.stopPropagation();
        updateActiveTreeItem(node.id);
        loadPresentation(node.id, 0);
        if (window.innerWidth <= 768) {
          closeMobileSidebar();
        }
      });
    }

    return container;
  }

  function updateActiveTreeItem(id) {
    document.querySelectorAll('.tree-item.active').forEach(el => el.classList.remove('active'));
    const item = document.querySelector(`.tree-item[data-id="${id}"]`);
    if (item) {
      item.classList.add('active');
      item.scrollIntoView?.({ behavior: 'smooth', block: 'nearest' });
    }
  }

  // =========================================================================
  // PRESENTATION LOADING (pptx-browser Canvas Renderer)
  // =========================================================================

  async function loadPresentation(presId, targetSlide = 0) {
    if (typeof PRESENTATIONS === 'undefined') return;
    const pres = PRESENTATIONS[presId];
    if (!pres) return;

    state.currentId = presId;
    state.currentSlide = targetSlide;
    ensureAncestorsExpanded(presId);
    saveState();

    // Update Title and Breadcrumbs
    const displayName = pres.title || pres.name.replace('.pptx', '');
    elements.currentTitle.textContent = displayName;
    
    const parts = pres.path.split('/');
    elements.breadcrumbs.innerHTML = `
      <span class="breadcrumb-item">${parts[0] || 'Capacidad'}</span>
      <span class="breadcrumb-sep">/</span>
      ${parts.length > 2 ? `<span class="breadcrumb-item">${parts[1]}</span><span class="breadcrumb-sep">/</span>` : ''}
      <span class="breadcrumb-current">${displayName}</span>
    `;

    // Ensure path is NFC normalized for standard Linux/Netlify web servers
    const normalizedPath = (pres.path || '').normalize('NFC');
    const fileUrl = '/' + encodeURI(normalizedPath);
    elements.btnDownloadPptx.href = fileUrl;
    elements.btnDownloadPptx.download = pres.name;

    // Show loading spinner
    elements.loadingOverlay.style.display = 'flex';
    elements.loadingMsg.textContent = `Cargando "${displayName}"...`;
    elements.thumbnailStrip.innerHTML = '';
    elements.slideCounter.innerHTML = '<span class="slide-cur">--</span><span class="slide-sep">/</span><span class="slide-tot">--</span>';

    try {
      // Destroy previous renderer to free memory & blob URLs
      if (state.renderer) {
        state.renderer.destroy();
        state.renderer = null;
      }

      // Fetch the PPTX file with automatic fallback handling
      let res = await fetch(fileUrl);
      if (!res.ok) {
        // Fallback 1: relative to parent (if running inside /visor_instructivos/)
        const fallbackRelative = '../' + encodeURI(normalizedPath);
        const resFb1 = await fetch(fallbackRelative);
        if (resFb1.ok) {
          res = resFb1;
        } else {
          // Fallback 2: try NFD normalized
          const fallbackNfd = '/' + encodeURI((pres.path || '').normalize('NFD'));
          const resFb2 = await fetch(fallbackNfd);
          if (resFb2.ok) {
            res = resFb2;
          }
        }
      }
      if (!res.ok) {
        throw new Error(`HTTP ${res.status}: No se encontró el archivo PPTX.`);
      }
      const arrayBuffer = await res.arrayBuffer();

      // Create fresh pptx-browser renderer
      const { PptxRenderer } = window.PptxBrowser;
      if (!PptxRenderer) {
        throw new Error('El motor de renderizado PPTX no está disponible.');
      }

      const renderer = new PptxRenderer();
      await renderer.load(arrayBuffer, (progress, msg) => {
        const pct = Math.round(progress * 100);
        elements.loadingMsg.textContent = `Cargando "${displayName}"... ${pct}%`;
      });

      state.renderer = renderer;

      elements.loadingOverlay.style.display = 'none';
      const totalSlides = renderer.slideCount || 1;
      const initialSlide = Math.max(0, Math.min(targetSlide, totalSlides - 1));
      await renderSlide(initialSlide);
      await renderThumbnails();
      updateActiveTreeItem(presId);
    } catch (err) {
      console.error('Error cargando PPTX:', err);
      elements.loadingOverlay.style.display = 'flex';
      elements.loadingOverlay.innerHTML = `
        <div class="empty-state">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#ef4444" stroke-width="2" style="margin-bottom: 12px;">
            <circle cx="12" cy="10" r="10"/>
            <line x1="12" y1="8" x2="12" y2="12"/>
            <line x1="12" y1="16" x2="12.01" y2="16"/>
          </svg>
          <h3 style="color:#fff; margin-bottom:8px; font-size:16px;">${displayName}</h3>
          <p style="color:#94a3b8; max-width:440px; margin-bottom:18px; font-size:13px; line-height:1.5;">${err.message || 'Error al procesar el archivo PowerPoint.'}</p>
          <a href="${fileUrl}" class="control-btn primary" download="${pres.name}">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
            Descargar PPTX Original
          </a>
        </div>
      `;
    }
  }

  // =========================================================================
  // SLIDE RENDERING & NAVIGATION (Canvas-based)
  // =========================================================================

  async function renderSlide(slideIdx) {
    if (!state.renderer) return;
    const total = state.renderer.slideCount;
    if (!total || total === 0) return;

    const idx = Math.max(0, Math.min(slideIdx, total - 1));
    state.currentSlide = idx;
    saveState();

    // Reset zoom and pan when changing slides so each slide starts centered
    resetZoomAndPan(false);

    // Render the slide onto the canvas at high resolution
    const renderWidth = Math.min(1920, window.innerWidth * window.devicePixelRatio);
    await state.renderer.renderSlide(idx, elements.slideCanvas, renderWidth);

    // Update Counter
    elements.slideCounter.innerHTML = `<span class="slide-cur">${idx + 1}</span><span class="slide-sep">/</span><span class="slide-tot">${total}</span>`;
    elements.slideCounter.title = `Diapositiva ${idx + 1} de ${total}`;

    // Update Buttons State
    const isFirst = idx === 0;
    const isLast = idx === total - 1;

    elements.btnPrevSlide.disabled = isFirst;
    elements.btnNextSlide.disabled = isLast;
    elements.btnPrev.disabled = isFirst;
    elements.btnNext.disabled = isLast;
    elements.btnFirstSlide.disabled = isFirst;
    elements.btnLastSlide.disabled = isLast;

    // Update active thumbnail
    updateActiveThumbnail(idx);
  }

  async function nextSlide() {
    if (!state.renderer) return;
    if (state.currentSlide < state.renderer.slideCount - 1) {
      await renderSlide(state.currentSlide + 1);
    }
  }

  async function prevSlide() {
    if (!state.renderer) return;
    if (state.currentSlide > 0) {
      await renderSlide(state.currentSlide - 1);
    }
  }

  async function firstSlide() {
    await renderSlide(0);
  }

  async function lastSlide() {
    if (!state.renderer) return;
    await renderSlide(state.renderer.slideCount - 1);
  }

  // =========================================================================
  // THUMBNAILS FILMSTRIP (Canvas-based)
  // =========================================================================

  async function renderThumbnails() {
    if (!state.renderer) return;
    elements.thumbnailStrip.innerHTML = '';

    try {
      const canvases = await state.renderer.renderAllSlides(240);
      canvases.forEach((cvs, idx) => {
        const card = document.createElement('div');
        card.className = 'thumb-card' + (idx === state.currentSlide ? ' active' : '');
        card.id = `thumb-${idx}`;
        card.title = `Ir a diapositiva ${idx + 1}`;

        // Style the mini-canvas
        cvs.style.width = '100%';
        cvs.style.height = '100%';
        cvs.style.display = 'block';
        cvs.style.pointerEvents = 'none';

        const badge = document.createElement('span');
        badge.className = 'thumb-number';
        badge.textContent = `${idx + 1}`;

        card.appendChild(cvs);
        card.appendChild(badge);

        card.addEventListener('click', async () => {
          await renderSlide(idx);
        });

        elements.thumbnailStrip.appendChild(card);
      });

      updateActiveThumbnail(state.currentSlide);
    } catch (err) {
      console.warn('Error al generar miniaturas:', err);
    }
  }

  function updateActiveThumbnail(idx) {
    document.querySelectorAll('.thumb-card.active').forEach(c => c.classList.remove('active'));
    const activeCard = document.getElementById(`thumb-${idx}`);
    if (activeCard) {
      activeCard.classList.add('active');
      activeCard.scrollIntoView?.({ behavior: 'smooth', block: 'nearest', inline: 'center' });
    }
  }

  function toggleThumbnails() {
    state.thumbnailsVisible = !state.thumbnailsVisible;
    if (state.thumbnailsVisible) {
      elements.thumbnailStrip.classList.remove('collapsed');
      elements.thumbsLabel.textContent = 'Ocultar Miniaturas';
      elements.btnToggleThumbs?.classList.add('active');
      updateActiveThumbnail(state.currentSlide);
    } else {
      elements.thumbnailStrip.classList.add('collapsed');
      elements.thumbsLabel.textContent = 'Miniaturas';
      elements.btnToggleThumbs?.classList.remove('active');
    }
  }

  // =========================================================================
  // FULLSCREEN MODE
  // =========================================================================

  function toggleFullscreen() {
    if (!document.fullscreenElement) {
      elements.presentationStage.requestFullscreen().catch(err => {
        console.warn('Error pantalla completa:', err);
      });
    } else {
      document.exitFullscreen().catch(() => {});
    }
  }

  // =========================================================================
  // ZOOM & PAN (HAND TOOL) SYSTEM
  // =========================================================================

  function applyCanvasTransform() {
    if (!elements.slideCanvas) return;
    const { panX, panY, zoom } = state;
    elements.slideCanvas.style.transform = `translate3d(${panX}px, ${panY}px, 0px) scale(${zoom})`;
    if (elements.zoomLevelText) {
      elements.zoomLevelText.textContent = `${Math.round(zoom * 100)}%`;
    }
    updateCursorState();
  }

  function setZoom(newZoom, pointerX = null, pointerY = null) {
    const clamped = Math.max(0.5, Math.min(3.5, Math.round(newZoom * 100) / 100));
    if (Math.abs(state.zoom - clamped) < 0.001) return;

    // En desktop al usar zoom (> 100%), cerrar automáticamente las miniaturas para máximo espacio
    if (clamped > 1.0 && state.thumbnailsVisible && window.innerWidth > 768) {
      state.thumbnailsVisible = false;
      elements.thumbnailStrip.classList.add('collapsed');
      elements.thumbsLabel.textContent = 'Miniaturas';
      elements.btnToggleThumbs?.classList.remove('active');
    }

    if (clamped <= 1.0) {
      state.panX = 0;
      state.panY = 0;
    } else if (pointerX !== null && pointerY !== null) {
      const ratio = clamped / state.zoom;
      state.panX = pointerX - (pointerX - state.panX) * ratio;
      state.panY = pointerY - (pointerY - state.panY) * ratio;
    }

    state.zoom = clamped;
    applyCanvasTransform();
  }

  function zoomIn(step = 0.25) {
    setZoom(state.zoom + step);
  }

  function zoomOut(step = 0.25) {
    setZoom(state.zoom - step);
  }

  function resetZoomAndPan(animate = true) {
    state.zoom = 1.0;
    state.panX = 0;
    state.panY = 0;
    if (!animate && elements.slideCanvas) {
      elements.slideCanvas.style.transition = 'none';
      applyCanvasTransform();
      requestAnimationFrame(() => {
        if (elements.slideCanvas) {
          elements.slideCanvas.style.transition = 'transform 0.18s cubic-bezier(0.16, 1, 0.3, 1)';
        }
      });
    } else {
      applyCanvasTransform();
    }
  }

  function toggleHandMode(forceValue) {
    state.handMode = typeof forceValue === 'boolean' ? forceValue : !state.handMode;
    if (elements.btnToolHand) {
      elements.btnToolHand.classList.toggle('active', state.handMode);
    }
    updateCursorState();
  }

  function updateCursorState() {
    if (!elements.slideCanvasWrapper) return;
    const canPan = state.handMode || state.zoom > 1.02;
    if (canPan) {
      elements.slideCanvasWrapper.classList.add('can-drag');
    } else {
      elements.slideCanvasWrapper.classList.remove('can-drag');
    }
  }

  let isDragging = false;
  let dragStartX = 0;
  let dragStartY = 0;
  let initialPanX = 0;
  let initialPanY = 0;

  function initZoomAndPan() {
    const wrapper = elements.slideCanvasWrapper;
    if (!wrapper) return;

    // Mouse Drag (Left button)
    wrapper.addEventListener('mousedown', (e) => {
      if (e.button !== 0) return;
      if (e.target.closest('#slide-zoom-toolbar') || e.target.closest('.nav-arrow')) return;

      const canPan = state.handMode || state.zoom > 1.02;
      if (!canPan) return;

      isDragging = true;
      dragStartX = e.clientX;
      dragStartY = e.clientY;
      initialPanX = state.panX;
      initialPanY = state.panY;

      wrapper.classList.add('is-panning');
      if (elements.slideCanvas) {
        elements.slideCanvas.style.transition = 'none';
      }
      e.preventDefault();
    });

    window.addEventListener('mousemove', (e) => {
      if (!isDragging) return;
      const dx = e.clientX - dragStartX;
      const dy = e.clientY - dragStartY;
      state.panX = initialPanX + dx;
      state.panY = initialPanY + dy;
      applyCanvasTransform();
    });

    window.addEventListener('mouseup', () => {
      if (!isDragging) return;
      isDragging = false;
      wrapper.classList.remove('is-panning');
      if (elements.slideCanvas) {
        elements.slideCanvas.style.transition = 'transform 0.18s cubic-bezier(0.16, 1, 0.3, 1)';
      }
      updateCursorState();
    });

    // Touch support (1 finger pan, 2 fingers pinch to zoom)
    let initialPinchDist = null;
    let initialPinchZoom = 1.0;

    wrapper.addEventListener('touchstart', (e) => {
      if (e.target.closest('#slide-zoom-toolbar') || e.target.closest('.nav-arrow')) return;
      if (e.touches.length === 1) {
        const canPan = state.handMode || state.zoom > 1.02;
        if (!canPan) return;
        isDragging = true;
        dragStartX = e.touches[0].clientX;
        dragStartY = e.touches[0].clientY;
        initialPanX = state.panX;
        initialPanY = state.panY;
        if (elements.slideCanvas) elements.slideCanvas.style.transition = 'none';
      } else if (e.touches.length === 2) {
        isDragging = false;
        initialPinchDist = Math.hypot(
          e.touches[0].clientX - e.touches[1].clientX,
          e.touches[0].clientY - e.touches[1].clientY
        );
        initialPinchZoom = state.zoom;
      }
    }, { passive: true });

    wrapper.addEventListener('touchmove', (e) => {
      if (e.touches.length === 1 && isDragging) {
        const dx = e.touches[0].clientX - dragStartX;
        const dy = e.touches[0].clientY - dragStartY;
        state.panX = initialPanX + dx;
        state.panY = initialPanY + dy;
        applyCanvasTransform();
        e.preventDefault();
      } else if (e.touches.length === 2 && initialPinchDist) {
        const dist = Math.hypot(
          e.touches[0].clientX - e.touches[1].clientX,
          e.touches[0].clientY - e.touches[1].clientY
        );
        const factor = dist / initialPinchDist;
        setZoom(initialPinchZoom * factor);
        e.preventDefault();
      }
    }, { passive: false });

    wrapper.addEventListener('touchend', () => {
      isDragging = false;
      initialPinchDist = null;
      if (elements.slideCanvas) {
        elements.slideCanvas.style.transition = 'transform 0.18s cubic-bezier(0.16, 1, 0.3, 1)';
      }
    }, { passive: true });

    // Trackpad Pinch or Ctrl + Wheel Zoom, or 2-Finger Pan
    wrapper.addEventListener('wheel', (e) => {
      if (e.ctrlKey || e.metaKey) {
        e.preventDefault();
        const rect = wrapper.getBoundingClientRect();
        const cx = e.clientX - (rect.left + rect.width / 2);
        const cy = e.clientY - (rect.top + rect.height / 2);
        const delta = -e.deltaY;
        if (delta > 0) {
          setZoom(state.zoom + 0.15, cx, cy);
        } else {
          setZoom(state.zoom - 0.15, cx, cy);
        }
      } else if (state.handMode || state.zoom > 1.02) {
        e.preventDefault();
        state.panX -= e.deltaX;
        state.panY -= e.deltaY;
        applyCanvasTransform();
      }
    }, { passive: false });

    // Double-click to Toggle Zoom
    wrapper.addEventListener('dblclick', (e) => {
      if (e.target.closest('#slide-zoom-toolbar') || e.target.closest('.nav-arrow')) return;
      if (state.zoom > 1.05) {
        resetZoomAndPan();
      } else {
        const rect = wrapper.getBoundingClientRect();
        const cx = e.clientX - (rect.left + rect.width / 2);
        const cy = e.clientY - (rect.top + rect.height / 2);
        setZoom(1.6, cx, cy);
      }
    });

    // Toolbar Buttons Click Handlers
    elements.btnToolHand?.addEventListener('click', (e) => {
      e.stopPropagation();
      toggleHandMode();
    });

    elements.btnZoomIn?.addEventListener('click', (e) => {
      e.stopPropagation();
      zoomIn(0.25);
    });

    elements.btnZoomOut?.addEventListener('click', (e) => {
      e.stopPropagation();
      zoomOut(0.25);
    });

    elements.btnZoomReset?.addEventListener('click', (e) => {
      e.stopPropagation();
      resetZoomAndPan();
    });

    elements.btnZoomFit?.addEventListener('click', (e) => {
      e.stopPropagation();
      resetZoomAndPan();
    });
  }

  // =========================================================================
  // EVENT LISTENERS & SHORTCUTS
  // =========================================================================

  // Slide Navigation Controls
  elements.btnPrevSlide.addEventListener('click', () => prevSlide());
  elements.btnNextSlide.addEventListener('click', () => nextSlide());
  elements.btnPrev.addEventListener('click', () => prevSlide());
  elements.btnNext.addEventListener('click', () => nextSlide());
  elements.btnFirstSlide.addEventListener('click', () => firstSlide());
  elements.btnLastSlide.addEventListener('click', () => lastSlide());

  // Fullscreen Buttons
  elements.btnTopFullscreen.addEventListener('click', toggleFullscreen);
  elements.btnFooterFullscreen.addEventListener('click', toggleFullscreen);

  // Thumbnails Toggle
  elements.btnToggleThumbs.addEventListener('click', toggleThumbnails);

  // Global Keyboard Navigation
  window.addEventListener('keydown', (e) => {
    // 1. Detect Hard Reload or Reset Shortcuts:
    // Cmd+Shift+R (Mac), Ctrl+Shift+R (Win/Linux), Ctrl+F5, Cmd+Shift+3 / Ctrl+Shift+3
    const isCmdShiftR = (e.metaKey || e.ctrlKey) && e.shiftKey && (e.key === 'r' || e.key === 'R');
    const isCtrlF5 = e.ctrlKey && e.key === 'F5';
    const isShift3 = (e.metaKey || e.ctrlKey) && e.shiftKey && (e.key === '3' || e.key === '#');

    if (isCmdShiftR || isCtrlF5) {
      try {
        localStorage.removeItem(STORAGE_KEY);
        sessionStorage.removeItem(STORAGE_KEY);
      } catch (err) {}
      return; // let native reload happen with cleaned storage
    }

    if (isShift3) {
      e.preventDefault();
      resetToDefault();
      return;
    }

    if (document.activeElement === elements.searchInput) return;

    switch (e.key) {
      case 'ArrowRight':
      case 'ArrowDown':
      case 'PageDown':
      case ' ':
        e.preventDefault();
        nextSlide();
        break;
      case 'ArrowLeft':
      case 'ArrowUp':
      case 'PageUp':
        e.preventDefault();
        prevSlide();
        break;
      case 'Home':
        e.preventDefault();
        firstSlide();
        break;
      case 'End':
        e.preventDefault();
        lastSlide();
        break;
      case 'f':
      case 'F':
        e.preventDefault();
        toggleFullscreen();
        break;
      case 'h':
      case 'H':
        e.preventDefault();
        toggleHandMode();
        break;
      case '+':
      case '=':
        if (!e.metaKey && !e.ctrlKey) {
          e.preventDefault();
          zoomIn(0.25);
        }
        break;
      case '-':
      case '_':
        if (!e.metaKey && !e.ctrlKey) {
          e.preventDefault();
          zoomOut(0.25);
        }
        break;
      case '0':
        if (!e.metaKey && !e.ctrlKey) {
          e.preventDefault();
          resetZoomAndPan();
        }
        break;
      case 'b':
      case 'B':
        if (e.metaKey || e.ctrlKey) {
          e.preventDefault();
          toggleSidebar();
        }
        break;
    }
  }, true);

  // Sidebar Toggles & Mobile Drawer
  function openMobileSidebar() {
    elements.sidebar.classList.remove('collapsed');
    if (elements.sidebarOverlay) elements.sidebarOverlay.classList.add('active');
  }

  function closeMobileSidebar() {
    elements.sidebar.classList.add('collapsed');
    if (elements.sidebarOverlay) elements.sidebarOverlay.classList.remove('active');
  }

  function toggleSidebar() {
    if (window.innerWidth <= 768) {
      if (elements.sidebar.classList.contains('collapsed')) {
        openMobileSidebar();
      } else {
        closeMobileSidebar();
      }
    } else {
      elements.sidebar.classList.toggle('collapsed');
      const isCollapsed = elements.sidebar.classList.contains('collapsed');
      elements.btnExpandSidebar.style.display = isCollapsed ? 'flex' : 'none';
      if (elements.sidebarOverlay) elements.sidebarOverlay.classList.remove('active');
    }
  }

  elements.btnToggleSidebar?.addEventListener('click', toggleSidebar);
  elements.btnExpandSidebar?.addEventListener('click', toggleSidebar);
  elements.btnCloseSidebarMobile?.addEventListener('click', closeMobileSidebar);
  elements.sidebarOverlay?.addEventListener('click', closeMobileSidebar);

  elements.btnCollapseAll.addEventListener('click', () => {
    if (state.expandedFolders.size > 0) {
      state.expandedFolders.clear();
      elements.btnCollapseAll.title = 'Expandir todas las carpetas';
    } else {
      if (typeof APP_TREE !== 'undefined' && APP_TREE.children) {
        getAllFolderPaths(APP_TREE.children).forEach(p => state.expandedFolders.add(p));
      }
      elements.btnCollapseAll.title = 'Colapsar todas las carpetas';
    }
    saveState();
    renderTree(elements.searchInput.value);
  });

  elements.btnResetDefault?.addEventListener('click', () => {
    resetToDefault();
  });

  // Search filter
  elements.searchInput.addEventListener('input', (e) => {
    const val = e.target.value;
    elements.searchClear.style.display = val ? 'flex' : 'none';
    renderTree(val);
  });

  elements.searchClear.addEventListener('click', () => {
    elements.searchInput.value = '';
    elements.searchClear.style.display = 'none';
    renderTree('');
  });

  // =========================================================================
  // INITIALIZATION
  // =========================================================================

  initZoomAndPan();
  ensureAncestorsExpanded(state.currentId);
  renderTree();
  elements.viewSlides.classList.add('active');

  // En mobile: miniaturas abiertas por defecto a petición del usuario
  if (window.innerWidth <= 768) {
    state.thumbnailsVisible = true;
  }

  if (!state.thumbnailsVisible) {
    elements.thumbnailStrip.classList.add('collapsed');
    elements.thumbsLabel.textContent = 'Miniaturas';
    elements.btnToggleThumbs?.classList.remove('active');
  } else {
    elements.thumbnailStrip.classList.remove('collapsed');
    elements.thumbsLabel.textContent = 'Ocultar Miniaturas';
    elements.btnToggleThumbs?.classList.add('active');
  }

  // Mobile Touch Gestures (Swipe Left/Right to advance or return slide)
  let touchStartX = 0;
  let touchStartY = 0;
  let touchStartTime = 0;

  elements.slideViewport?.addEventListener('touchstart', (e) => {
    if (e.touches.length === 1) {
      touchStartX = e.touches[0].clientX;
      touchStartY = e.touches[0].clientY;
      touchStartTime = Date.now();
    }
  }, { passive: true });

  elements.slideViewport?.addEventListener('touchend', (e) => {
    if (state.zoom > 1.05) return; // Allow natural panning when zoomed
    if (!e.changedTouches || e.changedTouches.length === 0) return;
    const diffX = e.changedTouches[0].clientX - touchStartX;
    const diffY = e.changedTouches[0].clientY - touchStartY;
    const time = Date.now() - touchStartTime;

    if (time < 500 && Math.abs(diffX) > 40 && Math.abs(diffX) > Math.abs(diffY) * 1.3) {
      if (diffX < 0) {
        nextSlide();
      } else {
        prevSlide();
      }
    }
  }, { passive: true });

  // On Mobile: Collapse sidebar by default so presentation is immediately visible
  if (window.innerWidth <= 768) {
    elements.sidebar.classList.add('collapsed');
    elements.btnExpandSidebar.style.display = 'flex';
  }

  window.addEventListener('resize', () => {
    if (window.innerWidth > 768) {
      if (elements.sidebarOverlay) elements.sidebarOverlay.classList.remove('active');
      const isCollapsed = elements.sidebar.classList.contains('collapsed');
      elements.btnExpandSidebar.style.display = isCollapsed ? 'flex' : 'none';
    } else {
      elements.btnExpandSidebar.style.display = 'flex';
    }
  });

  loadPresentation(state.currentId, state.currentSlide);
}

// Ensure execution whether DOM is loading or already ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initApp);
} else {
  initApp();
}
