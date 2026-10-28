/* Zoom y lupa para las láminas de los visores (guía de cada paso y asistente IA).
   Solo agranda la imagen: la rueda, el pellizco del touchpad (ctrl + rueda) y el gesto de Safari se
   detienen aquí para que el navegador no agrande toda la página.
   Uso: var z = window.CCEEZoom(img);  z.reset();  z.zoom(1.25);  — se reinicia solo al cambiar la imagen. */
(function () {
  if (window.CCEEZoom) return;
  var MIN = 1, MAX = 4, LUPA_R = 95;  // más de 4× solo agranda los píxeles: las láminas miden 1600 px

  window.CCEEZoom = function (img) {
    if (img.__cceeZoom) return img.__cceeZoom;
    var zona = document.createElement('div');
    zona.className = 'zi-zona';
    img.parentNode.insertBefore(zona, img);
    zona.appendChild(img);
    img.draggable = false;

    var barra = document.createElement('div');
    barra.className = 'zi-barra';
    barra.innerHTML =
      '<button type="button" data-zi="menos" title="Alejar (tecla −)" aria-label="Alejar">−</button>' +
      '<button type="button" data-zi="reset" class="zi-pct" title="Tamaño original (tecla 0)">100 %</button>' +
      '<button type="button" data-zi="mas" title="Acercar (tecla +)" aria-label="Acercar">+</button>' +
      '<button type="button" data-zi="lupa" class="zi-lupa-btn" title="Lupa: pase el mouse sobre la imagen; la rueda cambia el aumento" aria-pressed="false">' +
      '<svg viewBox="0 0 24 24" width="14" height="14" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5" fill="none" stroke="currentColor" stroke-width="2.2"/>' +
      '<path d="M15.5 15.5 21 21" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/></svg> Lupa</button>';
    zona.appendChild(barra);

    var lupa = document.createElement('div');
    lupa.className = 'zi-lupa';
    lupa.hidden = true;
    zona.appendChild(lupa);

    var s = 1, tx = 0, ty = 0, lupaOn = false, lupaK = 2.5;
    var punteros = {}, arrastre = null, pinza = null, gestoBase = 1;

    function limitar() {
      var w = zona.clientWidth, h = zona.clientHeight;
      tx = Math.min(0, Math.max(w - w * s, tx));
      ty = Math.min(0, Math.max(h - h * s, ty));
    }
    function pintar() {
      limitar();
      img.style.transform = s === 1 ? '' : 'translate(' + tx + 'px,' + ty + 'px) scale(' + s + ')';
      zona.classList.toggle('zi-zoom', s > 1);
      barra.querySelector('.zi-pct').textContent = Math.round(s * 100) + ' %';
    }
    function zoomEn(f, cx, cy) {
      var r = zona.getBoundingClientRect();
      var x = cx === undefined ? r.width / 2 : cx - r.left;
      var y = cy === undefined ? r.height / 2 : cy - r.top;
      var nuevo = Math.min(MAX, Math.max(MIN, s * f));
      tx = x - (x - tx) * (nuevo / s);
      ty = y - (y - ty) * (nuevo / s);
      s = nuevo;
      if (s === 1) { tx = 0; ty = 0; }
      pintar();
    }
    function reset() { s = 1; tx = 0; ty = 0; pintar(); }

    function moverLupa(e) {
      var r = img.getBoundingClientRect();
      var x = e.clientX - r.left, y = e.clientY - r.top;
      if (x < 0 || y < 0 || x > r.width || y > r.height) { lupa.hidden = true; return; }
      var z = zona.getBoundingClientRect();
      lupa.hidden = false;
      lupa.style.left = (e.clientX - z.left - LUPA_R) + 'px';
      lupa.style.top = (e.clientY - z.top - LUPA_R) + 'px';
      lupa.style.backgroundImage = 'url("' + (img.currentSrc || img.src) + '")';
      lupa.style.backgroundSize = (r.width * lupaK) + 'px ' + (r.height * lupaK) + 'px';
      lupa.style.backgroundPosition = (LUPA_R - x * lupaK) + 'px ' + (LUPA_R - y * lupaK) + 'px';
    }
    function alternarLupa() {
      lupaOn = !lupaOn;
      if (lupaOn) reset();
      lupa.hidden = true;
      zona.classList.toggle('zi-con-lupa', lupaOn);
      barra.querySelector('[data-zi="lupa"]').setAttribute('aria-pressed', lupaOn ? 'true' : 'false');
    }

    function accion(a) {
      if (lupaOn && a !== 'lupa') alternarLupa();
      if (a === 'mas') zoomEn(1.4);
      else if (a === 'menos') zoomEn(1 / 1.4);
      else if (a === 'reset') reset();
      else if (a === 'lupa') alternarLupa();
    }
    // Si la página atiende los clics antes (captura), puede llamar a ctl.accion(data-zi) por su cuenta.
    barra.addEventListener('click', function (e) {
      var b = e.target.closest('[data-zi]');
      if (!b) return;
      e.preventDefault();
      e.stopPropagation();
      accion(b.getAttribute('data-zi'));
    });

    // Rueda y pellizco del touchpad (llega como rueda con ctrlKey): acercan en el punto del cursor.
    zona.addEventListener('wheel', function (e) {
      e.preventDefault();
      if (lupaOn) {
        lupaK = Math.min(6, Math.max(1.5, lupaK * Math.exp(-e.deltaY * 0.002)));
        moverLupa(e);
        return;
      }
      zoomEn(Math.exp(-e.deltaY * (e.ctrlKey ? 0.01 : 0.0018)), e.clientX, e.clientY);
    }, { passive: false });
    // Safari (Mac) manda el pellizco como gesto propio.
    zona.addEventListener('gesturestart', function (e) { e.preventDefault(); gestoBase = s; }, { passive: false });
    zona.addEventListener('gesturechange', function (e) {
      e.preventDefault();
      if (!lupaOn) zoomEn((gestoBase * e.scale) / s, e.clientX, e.clientY);
    }, { passive: false });
    zona.addEventListener('gestureend', function (e) { e.preventDefault(); }, { passive: false });

    zona.addEventListener('dblclick', function (e) {
      if (e.target.closest('.zi-barra') || lupaOn) return;
      e.preventDefault();
      if (s > 1.05) reset(); else zoomEn(2.5, e.clientX, e.clientY);
    });

    // Arrastrar para mover; con dos dedos, pellizcar (pantallas táctiles).
    zona.addEventListener('pointerdown', function (e) {
      if (e.target.closest('.zi-barra')) return;
      punteros[e.pointerId] = { x: e.clientX, y: e.clientY };
      var ids = Object.keys(punteros);
      if (ids.length === 2) {
        var a = punteros[ids[0]], b = punteros[ids[1]];
        pinza = { d: Math.hypot(a.x - b.x, a.y - b.y), s: s };
        arrastre = null;
      } else if (s > 1 && !lupaOn) {
        arrastre = { x: e.clientX - tx, y: e.clientY - ty };
        zona.setPointerCapture(e.pointerId);
        zona.classList.add('zi-arrastrando');
      }
    });
    zona.addEventListener('pointermove', function (e) {
      if (lupaOn) { moverLupa(e); return; }
      if (!punteros[e.pointerId]) return;
      punteros[e.pointerId] = { x: e.clientX, y: e.clientY };
      var ids = Object.keys(punteros);
      if (pinza && ids.length === 2) {
        var a = punteros[ids[0]], b = punteros[ids[1]];
        zoomEn((pinza.s * Math.hypot(a.x - b.x, a.y - b.y) / pinza.d) / s, (a.x + b.x) / 2, (a.y + b.y) / 2);
      } else if (arrastre) {
        tx = e.clientX - arrastre.x;
        ty = e.clientY - arrastre.y;
        pintar();
      }
    });
    function soltar(e) {
      delete punteros[e.pointerId];
      if (Object.keys(punteros).length < 2) pinza = null;
      arrastre = null;
      zona.classList.remove('zi-arrastrando');
    }
    zona.addEventListener('pointerup', soltar);
    zona.addEventListener('pointercancel', soltar);
    zona.addEventListener('pointerleave', function () { if (lupaOn) lupa.hidden = true; });

    img.addEventListener('load', reset);  // imagen nueva (otra lámina, recorte o completa): vuelve al 100 %
    var ctl = { reset: reset, zoom: function (f) { zoomEn(f); }, accion: accion, zona: zona };
    img.__cceeZoom = ctl;
    return ctl;
  };
})();
