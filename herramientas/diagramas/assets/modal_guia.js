(function () {
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
      legacy: 'archify_ultimo_paso_' + path,
      path: path
    };
  }

  // Detección de si estamos en el diagrama 2: Crear el NRC (en cualquier centro)
  function esFlujoCrearNrc() {
    var p = (window.location.pathname || '').toLowerCase();
    return p.indexOf('02-crear-el-nrc') !== -1 || p.indexOf('crear-el-nrc') !== -1;
  }

  // Estado de visibilidad de los pasos finales (horario/docente y consulta) en Crear el NRC.
  function estanPasosPosterioresVisibles() {
    if (!esFlujoCrearNrc()) return true;
    var keys = obtenerStorageKeys();
    var val = localStorage.getItem('archify_mostrar_posteriores_' + keys.current);
    if (val === 'true') return true;
    if (val === 'false') return false;
    // Por defecto ocultos (false), a menos que el usuario ya haya alcanzado s5 o s6 (maxIdx >= 4)
    var maxIdx = -1;
    try {
      var raw = localStorage.getItem(keys.max);
      if (raw !== null) maxIdx = parseInt(raw, 10);
    } catch (_) { }
    return maxIdx >= 4;
  }

  function setPasosPosterioresVisibles(visible) {
    if (!esFlujoCrearNrc()) return;
    var keys = obtenerStorageKeys();
    try {
      localStorage.setItem('archify_mostrar_posteriores_' + keys.current, visible ? 'true' : 'false');
    } catch (_) { }
    aplicarVisibilidadPasosPosteriores(visible);
  }

  function marcarEncabezadoFasePosterior(svg) {
    if (!svg) return;
    var texts = svg.querySelectorAll('text');
    for (var i = 0; i < texts.length; i++) {
      var t = texts[i];
      if (t.textContent && t.textContent.indexOf('Consulta oficial') !== -1) {
        t.classList.add('phase-posterior-header');
        var mask = t.previousElementSibling;
        if (mask && mask.tagName && mask.tagName.toLowerCase() === 'rect') {
          mask.classList.add('phase-posterior-header');
          var line = mask.previousElementSibling;
          if (line && line.tagName && line.tagName.toLowerCase() === 'line') {
            line.classList.add('phase-posterior-header');
          }
        }
        break;
      }
    }
  }

  function aplicarVisibilidadPasosPosteriores(visible) {
    var svg = document.querySelector('.diagram-container > svg') || document.querySelector('svg');
    if (!svg) return;

    if (!esFlujoCrearNrc()) {
      svg.removeAttribute('data-ocultar-posteriores');
      svg.classList.remove('ocultar-posteriores');
      return;
    }

    if (visible === undefined) {
      visible = estanPasosPosterioresVisibles();
    }

    if (!visible) {
      svg.setAttribute('data-ocultar-posteriores', 'true');
    } else {
      svg.removeAttribute('data-ocultar-posteriores');
    }
    svg.classList.remove('ocultar-posteriores');

    marcarEncabezadoFasePosterior(svg);
    asegurarPlaceholderPosterioresSvg(svg);
    actualizarBotonesAlternanciaPosteriores(visible);
  }

  function asegurarPlaceholderPosterioresSvg(svg) {
    if (!svg || !esFlujoCrearNrc()) return;
    var existing = svg.querySelector('#placeholder-posteriores-svg');
    if (existing) return existing;

    var ns = "http://www.w3.org/2000/svg";
    var g = document.createElementNS(ns, "g");
    g.id = "placeholder-posteriores-svg";
    g.setAttribute("class", "placeholder-pasos-posteriores");
    g.setAttribute("tabindex", "0");
    g.setAttribute("role", "button");
    g.setAttribute("aria-label", "Desplegar pasos posteriores: horario y consulta oficial");

    var rect = document.createElementNS(ns, "rect");
    rect.setAttribute("x", "760");
    rect.setAttribute("y", "86");
    rect.setAttribute("width", "328");
    rect.setAttribute("height", "68");
    rect.setAttribute("rx", "6");
    g.appendChild(rect);

    var textTitle = document.createElementNS(ns, "text");
    textTitle.setAttribute("x", "924");
    textTitle.setAttribute("y", "116");
    textTitle.setAttribute("class", "placeholder-title");
    textTitle.setAttribute("text-anchor", "middle");
    textTitle.setAttribute("font-size", "10");
    textTitle.setAttribute("font-weight", "600");
    textTitle.textContent = "➕ Pasos 5 y 6: horario y consulta";
    g.appendChild(textTitle);

    var textSub = document.createElementNS(ns, "text");
    textSub.setAttribute("x", "924");
    textSub.setAttribute("y", "136");
    textSub.setAttribute("class", "placeholder-sub");
    textSub.setAttribute("text-anchor", "middle");
    textSub.setAttribute("font-size", "7.5");
    textSub.setAttribute("font-weight", "500");
    textSub.textContent = "Clic para ver · Horario/docente y consulta oficial";
    g.appendChild(textSub);

    svg.appendChild(g);

    g.addEventListener("click", function (e) {
      e.preventDefault();
      e.stopPropagation();
      setPasosPosterioresVisibles(true);
      actualizarProgresoDiagrama();
    });

    return g;
  }

  function actualizarBotonesAlternanciaPosteriores(visible) {
    if (!esFlujoCrearNrc()) return;

    // 1. Botón en la toolbar superior
    var toolbar = document.querySelector('.toolbar .toolbar-session-group');
    if (toolbar) {
      var btnPost = toolbar.querySelector('#btn-toggle-post-crear-nrc');
      if (!btnPost) {
        btnPost = document.createElement('button');
        btnPost.type = 'button';
        btnPost.id = 'btn-toggle-post-crear-nrc';
        btnPost.className = 'btn-tb-toggle-post';
        toolbar.appendChild(btnPost);
        btnPost.addEventListener('click', function (e) {
          e.preventDefault();
          e.stopPropagation();
          var vis = estanPasosPosterioresVisibles();
          setPasosPosterioresVisibles(!vis);
          actualizarProgresoDiagrama();
        });
      }
      btnPost.innerHTML = visible
        ? '<span class="tb-post-icon">👁️</span> <span class="tb-post-txt">Ocultar pasos 5 y 6</span>'
        : '<span class="tb-post-icon">👁️</span> <span class="tb-post-txt">Pasos 5 y 6 (Horario y consulta)</span>';
      btnPost.title = visible
        ? 'Ocultar horario/docente y consulta oficial'
        : 'Mostrar horario/docente y consulta oficial en el diagrama';
    }

    // Limpiar badge anterior si existía
    var oldBadge = document.getElementById('badge-posteriores-canvas');
    if (oldBadge) oldBadge.remove();
  }

  // Marcar en el SVG qué pasos están completados, cuál es el actual y cuáles están pendientes (despintados)
  function actualizarProgresoDiagrama(nodeIdForzado) {
    var svg = document.querySelector('.diagram-container > svg') || document.querySelector('svg');
    if (!svg) return;

    var nodeIds = obtenerIdsNodosDiagrama();
    if (!nodeIds.length) return;

    var keys = obtenerStorageKeys();
    var currentId = nodeIdForzado;

    var rawMax = null;
    var rawCurrent = null;
    try {
      rawMax = localStorage.getItem(keys.max);
      rawCurrent = localStorage.getItem(keys.current) || sessionStorage.getItem(keys.legacy);
    } catch (_) { }

    if (!currentId) {
      currentId = rawCurrent;
    }

    // Si se reinició o no hay ningún progreso guardado, DESPINTAR TODO (todo en 'pending')
    if (!currentId && rawMax === null) {
      window.__ultimoPasoEscogido = null;
      window.__guiaMaxUnlocked = 0;

      for (var i = 0; i < nodeIds.length; i++) {
        var gNode = svg.querySelector('g[data-node-id="' + nodeIds[i] + '"]');
        if (!gNode) continue;
        gNode.setAttribute('data-step-state', 'pending');
        gNode.removeAttribute('data-ultimo-escogido');
        gNode.removeAttribute('data-focus-selected');
        gNode.removeAttribute('data-focus-match');
      }

      var edgePaths = svg.querySelectorAll('path[data-edge-from][data-edge-to]');
      for (var e = 0; e < edgePaths.length; e++) {
        edgePaths[e].setAttribute('data-step-edge', 'pending');
      }

      svg.removeAttribute('data-focus-active');
      actualizarControlesSesion(-1, -1, nodeIds);
      aplicarVisibilidadPasosPosteriores();
      return;
    }

    var maxIdx = rawMax !== null ? parseInt(rawMax, 10) : 0;
    if (isNaN(maxIdx) || maxIdx < 0) maxIdx = 0;
    if (maxIdx >= nodeIds.length) maxIdx = nodeIds.length - 1;

    if (!currentId || nodeIds.indexOf(currentId) === -1) {
      currentId = nodeIds[maxIdx] || nodeIds[0];
    }

    var currIdx = nodeIds.indexOf(currentId);
    if (currIdx === -1) currIdx = 0;

    if (currIdx > maxIdx) {
      maxIdx = currIdx;
    }

    try {
      localStorage.setItem(keys.current, currentId);
      localStorage.setItem(keys.max, String(maxIdx));
      sessionStorage.setItem(keys.legacy, currentId);
    } catch (_) { }

    window.__ultimoPasoEscogido = currentId;
    window.__guiaMaxUnlocked = Math.max(window.__guiaMaxUnlocked || 0, maxIdx);

    for (var j = 0; j < nodeIds.length; j++) {
      var nId = nodeIds[j];
      var gNodeAct = svg.querySelector('g[data-node-id="' + nId + '"]');
      if (!gNodeAct) continue;

      if (j === currIdx) {
        gNodeAct.setAttribute('data-step-state', 'current');
        gNodeAct.setAttribute('data-ultimo-escogido', 'true');
      } else if (j <= maxIdx) {
        gNodeAct.setAttribute('data-step-state', 'completed');
        gNodeAct.removeAttribute('data-ultimo-escogido');
      } else {
        gNodeAct.setAttribute('data-step-state', 'pending');
        gNodeAct.removeAttribute('data-ultimo-escogido');
      }
    }

    var edges = svg.querySelectorAll('path[data-edge-from][data-edge-to]');
    for (var k = 0; k < edges.length; k++) {
      var edge = edges[k];
      var toId = edge.getAttribute('data-edge-to');
      var toIdx = nodeIds.indexOf(toId);
      if (toIdx !== -1 && toIdx <= maxIdx) {
        edge.setAttribute('data-step-edge', 'completed');
      } else {
        edge.setAttribute('data-step-edge', 'pending');
      }
    }

    actualizarControlesSesion(currIdx, maxIdx, nodeIds);
    aplicarVisibilidadPasosPosteriores();
  }

  function actualizarControlesSesion(currIdx, maxIdx, nodeIds) {
    if (!nodeIds || !nodeIds.length) return;

    // Si quedó un contenedor anterior en flow-nav-top, removerlo para limpiar el header
    var oldNavCtrl = document.querySelector('.flow-nav-top .flow-nav-session-ctrl');
    if (oldNavCtrl) oldNavCtrl.remove();

    var toolbar = document.querySelector('.toolbar');
    if (!toolbar) return;

    var ctrlWrap = toolbar.querySelector('.toolbar-session-group');
    if (!ctrlWrap) {
      ctrlWrap = document.createElement('div');
      ctrlWrap.className = 'toolbar-group toolbar-session-group';
      toolbar.insertBefore(ctrlWrap, toolbar.firstChild);
    }

    var isReviewingPast = (currIdx < maxIdx);
    var targetMaxId = nodeIds[maxIdx];
    var maxTitle = (GUIA_MAP[targetMaxId] && (GUIA_MAP[targetMaxId].fase || GUIA_MAP[targetMaxId].pantalla)) || ('Paso ' + (maxIdx + 1));

    var resumeHtml = '';
    if (isReviewingPast) {
      resumeHtml = '<button type="button" class="btn-tb-resume" data-ir-paso="' + escapeHtml(targetMaxId) + '" title="Volver al último paso alcanzado: ' + escapeHtml(maxTitle) + '">' +
        '<span class="tb-resume-icon">⏩</span> <span class="tb-resume-txt">Ir al último (Paso ' + (maxIdx + 1) + ')</span>' +
        '</button>';
    }

    var resetHtml = '<button type="button" class="btn-tb-reset" id="btn-flow-reset-top" title="Reiniciar progreso del flujo al Paso 1">' +
      '<span class="tb-reset-icon">↺</span> <span class="tb-reset-txt">Reiniciar</span>' +
      '</button>';

    ctrlWrap.innerHTML = resumeHtml + resetHtml;

    var btnReset = ctrlWrap.querySelector('#btn-flow-reset-top');
    if (btnReset) {
      btnReset.addEventListener('click', function (e) {
        e.preventDefault();
        e.stopPropagation();
        window.confirmarReinicioProgreso();
      });
    }

    var btnResume = ctrlWrap.querySelector('.btn-tb-resume');
    if (btnResume) {
      btnResume.addEventListener('click', function (e) {
        e.preventDefault();
        e.stopPropagation();
        window.irAPaso(targetMaxId, true);
      });
    }
  }

  function marcarUltimoPasoEnDiagrama(nodeId) {
    if (!nodeId) return;
    actualizarProgresoDiagrama(nodeId);
  }

  function asegurarOverlayReinicio() {
    var overlay = document.getElementById('guia-reset-overlay');
    if (overlay) return overlay;

    overlay = document.createElement('div');
    overlay.id = 'guia-reset-overlay';
    overlay.className = 'guia-confirm-overlay guia-reset-overlay';
    overlay.hidden = true;
    overlay.setAttribute('hidden', '');
    overlay.innerHTML = '<div class="guia-confirm-modal" role="dialog" aria-modal="true">' +
      '<div class="guia-confirm-header">' +
      '<span class="guia-confirm-icon" style="color:#ef4444;">↺</span>' +
      '<h4 class="guia-confirm-title">Reiniciar progreso del flujo</h4>' +
      '</div>' +
      '<p class="guia-confirm-body">' +
      '¿Deseas <strong>limpiar todo el progreso</strong> de este flujo y comenzar de nuevo desde el <strong>Paso 1</strong>?' +
      '</p>' +
      '<p class="guia-confirm-sub" style="font-size:0.75rem; color:#94a3b8; margin:0;">' +
      'Se desmarcarán los pasos completados y las validaciones guardadas.' +
      '</p>' +
      '<div class="guia-confirm-actions">' +
      '<button type="button" class="btn-confirm-seguir" id="btn-cancel-reset">Cancelar</button>' +
      '<button type="button" class="btn-confirm-pasar btn-danger-reset" id="btn-accept-reset" style="background:#ef4444 !important; border-color:#dc2626 !important; color:#fff !important;">Sí, reiniciar todo</button>' +
      '</div>' +
      '</div>';

    document.body.appendChild(overlay);

    var btnCancel = overlay.querySelector('#btn-cancel-reset');
    if (btnCancel) {
      btnCancel.addEventListener('click', function (e) {
        e.stopPropagation();
        cerrarModalConfirmacionReinicio();
      });
    }

    var btnAccept = overlay.querySelector('#btn-accept-reset');
    if (btnAccept) {
      btnAccept.addEventListener('click', function (e) {
        e.stopPropagation();
        cerrarModalConfirmacionReinicio();
        window.reiniciarProgresoDiagrama();
      });
    }

    overlay.addEventListener('click', function (e) {
      if (e.target === overlay) {
        e.stopPropagation();
        cerrarModalConfirmacionReinicio();
      }
    });

    return overlay;
  }

  window.confirmarReinicioProgreso = function () {
    var overlay = asegurarOverlayReinicio();
    overlay.hidden = false;
    overlay.removeAttribute('hidden');
    var btnCancel = overlay.querySelector('#btn-cancel-reset');
    if (btnCancel) btnCancel.focus();
  };

  function cerrarModalConfirmacionReinicio() {
    var overlay = document.getElementById('guia-reset-overlay');
    if (overlay) {
      overlay.hidden = true;
      overlay.setAttribute('hidden', '');
    }
  }

  window.reiniciarProgresoDiagrama = function () {
    var keys = obtenerStorageKeys();
    try {
      localStorage.removeItem(keys.current);
      localStorage.removeItem(keys.max);
      localStorage.removeItem('archify_mostrar_posteriores_' + keys.current);
      sessionStorage.removeItem(keys.legacy);
    } catch (_) { }

    // 1. Limpiar variables de estado en memoria
    window.__guiaMaxUnlocked = 0;
    window.__guiaChecks = {};
    window.__ultimoPasoEscogido = null;

    // 2. Cerrar el modal si estaba abierto y limpiar el foco de Archify SIN hacer clic en el Paso 1
    cerrarModalConfirmacionValidacion();
    var chip = document.getElementById('focus-chip');
    var b = document.getElementById('guia-modal-backdrop');
    if (b) b.classList.remove('active');
    document.body.classList.remove('has-guia-open');

    if (chip) {
      chip.classList.remove('tiene-guia');
      var clearBtn = document.getElementById('btn-focus-clear');
      if (clearBtn) clearBtn.click();
      chip.hidden = true;
      chip.setAttribute('hidden', '');
    }

    var idElem = document.getElementById('focus-id');
    if (idElem) idElem.textContent = '';

    // 3. Si estamos en Crear el NRC, volver a ocultar los 2 pasos posteriores (s5 y s6)
    if (esFlujoCrearNrc()) {
      setPasosPosterioresVisibles(false);
    }

    // 4. Despintar todos los nodos y flechas del diagrama sin abrir ningún modal
    actualizarProgresoDiagrama(null);
    mantenerFlujoCompleto();
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
      window.Archify.view.reveal = function () {
        mantenerFlujoCompleto();
        return false;
      };
      if (typeof window.Archify.view.frameDesktop === 'function') {
        window.Archify.view.frameDesktop = function () { return false; };
      }
    }
  }

  // Mantener el flujo BPM al 100% (sin zoom automático de Archify ni estrechamiento de contenedor)
  function mantenerFlujoCompleto() {
    neutralizarCamaraArchify();
    if (window.Archify && window.Archify.view && typeof window.Archify.view.reset === 'function') {
      try {
        window.Archify.view.reset({ automatic: true });
      } catch (_) { }
    }

    try {
      document.documentElement.removeAttribute('data-reader-narrow');
      document.documentElement.removeAttribute('data-reader-overflow');
      document.documentElement.style.removeProperty('--archify-reader-width');
      document.documentElement.style.removeProperty('--archify-diagram-max-width');
    } catch (_) { }

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
      btnSeguir.addEventListener('click', function (e) {
        e.stopPropagation();
        cerrarModalConfirmacionValidacion();
        resaltarFilasPendientes();
      });
    }

    var btnPasar = overlay.querySelector('#btn-confirm-pasar');
    if (btnPasar) {
      btnPasar.addEventListener('click', function (e) {
        e.stopPropagation();
        var callback = window.__confirmValidationCallback;
        cerrarModalConfirmacionValidacion();
        if (typeof callback === 'function') {
          callback();
        }
      });
    }

    overlay.addEventListener('click', function (e) {
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
    rows.forEach(function (row) {
      row.classList.remove('pendiente-atencion');
      void row.offsetWidth;
      row.classList.add('pendiente-atencion');
    });
    if (rows.length > 0) {
      try {
        rows[0].scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      } catch (_) { }
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

  window.irAPaso = function (targetNodeId, forzarSinValidar) {
    if (!targetNodeId) return;
    var idElem = document.getElementById('focus-id');
    var currentId = idElem ? (idElem.textContent || '').trim() : '';
    var nodeIds = obtenerIdsNodosDiagrama();
    if (!nodeIds.length) nodeIds = Object.keys(GUIA_MAP);
    var currentIndex = nodeIds.indexOf(currentId);
    var targetIndex = nodeIds.indexOf(targetNodeId);

    // Revelar automáticamente pasos posteriores si el objetivo es s5 o s6 en Crear el NRC
    if (esFlujoCrearNrc() && (targetNodeId === 's5' || targetNodeId === 's6')) {
      setPasosPosterioresVisibles(true);
    }

    var maxUnlocked = (typeof window.__guiaMaxUnlocked === 'number') ? window.__guiaMaxUnlocked : 0;
    // Solo validar si se intenta avanzar a un paso NUEVO que no ha sido desbloqueado todavía
    if (targetIndex > currentIndex && targetIndex > maxUnlocked && !forzarSinValidar) {
      var val = obtenerEstadoValidacionPaso(currentId);
      if (!val.completo) {
        mostrarModalConfirmacionValidacion(val.pendientes, val.total, function () {
          window.irAPaso(targetNodeId, true);
        });
        return;
      }
    }

    actualizarProgresoDiagrama(targetNodeId);
    var nodeElem = document.querySelector('[data-node-id="' + targetNodeId + '"]');
    if (nodeElem) {
      nodeElem.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
      setTimeout(function () {
        mantenerFlujoCompleto();
        actualizarModalGuia();
        actualizarProgresoDiagrama(targetNodeId);
      }, 30);
    }
  };

  window.navegarPaso = function (offset, forzarSinValidar) {
    var idElem = document.getElementById('focus-id');
    if (!idElem) return;
    var currentId = (idElem.textContent || '').trim();
    var nodeIds = obtenerIdsNodosDiagrama();
    if (!nodeIds.length) nodeIds = Object.keys(GUIA_MAP);
    var currentIndex = nodeIds.indexOf(currentId);
    if (currentIndex === -1) return;

    // Al avanzar desde s4 en Crear el NRC, revelar los pasos posteriores
    if (offset > 0 && currentId === 's4' && esFlujoCrearNrc()) {
      setPasosPosterioresVisibles(true);
    }

    var maxUnlocked = (typeof window.__guiaMaxUnlocked === 'number') ? window.__guiaMaxUnlocked : 0;
    if (offset > 0 && (currentIndex + offset) > maxUnlocked && !forzarSinValidar) {
      var val = obtenerEstadoValidacionPaso(currentId);
      if (!val.completo) {
        mostrarModalConfirmacionValidacion(val.pendientes, val.total, function () {
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
        setTimeout(function () {
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
      stepKeys.forEach(function (k, idx) {
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

    if (currentIndex < maxUnlocked) {
      var targetMaxId = stepKeys[maxUnlocked];
      var sInfoMax = GUIA_MAP[targetMaxId];
      var maxLabel = sInfoMax ? (sInfoMax.fase || sInfoMax.pantalla || ('Paso ' + (maxUnlocked + 1))) : ('Paso ' + (maxUnlocked + 1));
      html += '<div class="guia-banner-revision">';
      html += '<div class="banner-rev-info">';
      html += '<span class="banner-rev-icon">👀</span>';
      html += '<span>Estás revisando el <strong>Paso ' + (currentIndex + 1) + '</strong>. Tu avance guardado está en el <strong>Paso ' + (maxUnlocked + 1) + '</strong> (' + escapeHtml(maxLabel) + ').</span>';
      html += '</div>';
      html += '<button type="button" class="btn-banner-ir-ultimo" data-ir-paso="' + escapeHtml(targetMaxId) + '" title="Volver al último paso desbloqueado">';
      html += '<span>Continuar en Paso ' + (maxUnlocked + 1) + '</span> ⏩';
      html += '</button>';
      html += '</div>';
    }

    if (info.instrucciones && info.instrucciones.length > 0) {
      html += '<div class="guia-tabla-wrap"><table class="guia-tabla">';
      html += '<thead><tr><th class="th-num">#</th><th>Campo / Acción</th><th>Valor</th><th>Ejemplo</th><th>Tipo</th><th>Detalle Operativo</th></tr></thead>';
      html += '<tbody>';

      var checks = (window.__guiaChecks && window.__guiaChecks[nodeId]) || {};

      info.instrucciones.forEach(function (item, rIdx) {
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

      html += '<div class="guia-pie-right-actions" style="display:inline-flex; align-items:center; gap:0.45rem;">';
      if (currentIndex < maxUnlocked) {
        var targetMaxId = stepKeys[maxUnlocked];
        html += '<button type="button" class="btn-pie-resume" data-ir-paso="' + escapeHtml(targetMaxId) + '" title="Volver al último paso alcanzado">';
        html += '<span>Paso ' + (maxUnlocked + 1) + '</span> <span class="resume-arrow">⏩</span>';
        html += '</button>';
      }
      if (hasNext) {
        var btnNextTxt = 'Siguiente';
        if (nodeId === 's4' && esFlujoCrearNrc()) {
          btnNextTxt = 'Horario y consulta';
        }
        html += '<button type="button" class="guia-nav-btn btn-pie-next primary" data-nav-paso="1" title="Avanzar al siguiente paso">';
        html += '<span>' + escapeHtml(btnNextTxt) + '</span>';
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
      btnReset.addEventListener('click', function (e) {
        e.stopPropagation();
        window.confirmarReinicioProgreso();
      });
    }

    var btnCopy = topbar.querySelector('.btn-copy');
    btnCopy.addEventListener('click', function (e) {
      e.stopPropagation();
      var idElem = document.getElementById('focus-id');
      var nodeId = (idElem ? idElem.textContent : '').trim();
      var base = window.location.href.split('#')[0];
      var url = nodeId ? (base + '#focus=' + encodeURIComponent(nodeId)) : base;
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(url).then(function () {
          var txt = topbar.querySelector('.btn-copy-txt');
          var orig = txt.textContent;
          txt.textContent = '¡Copiado!';
          setTimeout(function () { txt.textContent = orig; }, 1600);
        });
      }
    });

    var btnClose = topbar.querySelector('.chip-btn-close');
    btnClose.addEventListener('click', function (e) {
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
      b.addEventListener('click', function (e) {
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
      setTimeout(function () {
        marcarUltimoPasoEnDiagrama(window.__ultimoPasoEscogido);
      }, 40);
      setTimeout(function () {
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

    setTimeout(function () {
      mantenerFlujoCompleto();
      var activePill = card.querySelector('.guia-step-pill.active');
      if (activePill) {
        try {
          activePill.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' });
        } catch (_) { }
      }
    }, 50);
  }

  document.addEventListener('DOMContentLoaded', function () {
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
      var svgObserver = new MutationObserver(function () {
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
      var htmlObserver = new MutationObserver(function () {
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
      btnPresent.addEventListener('click', function () {
        if (!document.fullscreenElement) {
          if (document.documentElement.requestFullscreen) {
            document.documentElement.requestFullscreen().catch(function (_) { });
          }
        } else {
          if (document.exitFullscreen) {
            document.exitFullscreen().catch(function (_) { });
          }
        }
        setTimeout(function () {
          syncPresentButton();
        }, 80);
      });
    }

    document.addEventListener('fullscreenchange', function () {
      if (!document.fullscreenElement && window.Archify && window.Archify.presentation) {
        if (typeof window.Archify.presentation.exit === 'function') {
          window.Archify.presentation.exit();
        }
      }
      setTimeout(syncPresentButton, 60);
    });

    document.addEventListener('webkitfullscreenchange', function () {
      setTimeout(syncPresentButton, 60);
    });

    window.addEventListener('resize', function () {
      syncPresentButton();
    });

    var target = document.getElementById('focus-id');
    if (target) {
      var observer = new MutationObserver(actualizarModalGuia);
      observer.observe(target, { childList: true, characterData: true, subtree: true });
    }

    document.addEventListener('click', function (e) {
      var btnTogglePost = e.target.closest('#btn-toggle-post-crear-nrc, #badge-posteriores-canvas');
      if (btnTogglePost) {
        e.preventDefault();
        e.stopPropagation();
        var vis = estanPasosPosterioresVisibles();
        setPasosPosterioresVisibles(!vis);
        actualizarProgresoDiagrama();
        return;
      }

      var legendEntry = e.target.closest('[data-legend-kind]');
      if (legendEntry && esFlujoCrearNrc()) {
        var kind = legendEntry.getAttribute('data-legend-kind');
        if (kind === 'security') {
          e.preventDefault();
          e.stopPropagation();
          setPasosPosterioresVisibles(true);
          window.irAPaso('s5', true);
          return;
        } else if (kind === 'database') {
          e.preventDefault();
          e.stopPropagation();
          setPasosPosterioresVisibles(true);
          window.irAPaso('s6', true);
          return;
        } else if (kind === 'backend') {
          e.preventDefault();
          e.stopPropagation();
          window.irAPaso('s1', true);
          return;
        }
      }

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
        setTimeout(function () {
          mantenerFlujoCompleto();
          actualizarModalGuia();
          if (nId) marcarUltimoPasoEnDiagrama(nId);
        }, 15);
        setTimeout(function () {
          mantenerFlujoCompleto();
          actualizarModalGuia();
          if (nId) marcarUltimoPasoEnDiagrama(nId);
        }, 70);
        setTimeout(function () {
          mantenerFlujoCompleto();
          if (nId) marcarUltimoPasoEnDiagrama(nId);
        }, 200);
        setTimeout(function () {
          mantenerFlujoCompleto();
          if (nId) marcarUltimoPasoEnDiagrama(nId);
        }, 450);
      }
    });

    document.addEventListener('keydown', function (e) {
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
      setTimeout(function () {
        actualizarModalGuia();
        mantenerFlujoCompleto();
        if (hashNodeId) marcarUltimoPasoEnDiagrama(hashNodeId);
      }, 70);
      setTimeout(function () {
        actualizarModalGuia();
        mantenerFlujoCompleto();
        if (hashNodeId) marcarUltimoPasoEnDiagrama(hashNodeId);
      }, 250);
    }
  });
})();
