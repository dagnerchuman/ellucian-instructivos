(function() {
  var themeBtn = document.getElementById('theme-toggle');
  var searchInput = document.getElementById('search-input');
  var chips = document.querySelectorAll('.filter-chip');
  var cards = document.querySelectorAll('.card');
  var sections = document.querySelectorAll('.center-section');
  var noResults = document.getElementById('no-results');

  // Alternar tema
  if (themeBtn) {
    themeBtn.addEventListener('click', function() {
      var cur = document.documentElement.getAttribute('data-theme') || 'light';
      var next = cur === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', next);
      try { localStorage.setItem('archify-theme', next); } catch (_) {}
    });
  }

  // Inicializar conteos reales de los chips según las tarjetas en el DOM
  chips.forEach(function(chip) {
    var filter = chip.getAttribute('data-filter');
    var label = chip.textContent.trim();
    var count = filter === 'all' ? cards.length : document.querySelectorAll('.card[data-center="' + filter + '"]').length;
    chip.textContent = label + ' (' + count + ')';
  });

  var currentFilter = 'all';

  // Sanitización de autocompletado del navegador (evitar que inserte correos institucionales guardados)
  function limpiarAutofillEmail() {
    if (!searchInput) return;
    var v = searchInput.value || '';
    if (v.indexOf('@') !== -1 || v.toLowerCase().indexOf('katherin') !== -1) {
      searchInput.value = '';
    }
  }
  limpiarAutofillEmail();
  setTimeout(limpiarAutofillEmail, 60);
  setTimeout(limpiarAutofillEmail, 300);
  setTimeout(limpiarAutofillEmail, 800);

  function aplicarFiltros() {
    if (!searchInput) return;
    limpiarAutofillEmail();
    var raw = (searchInput.value || '').trim();
    if (raw.indexOf('@') !== -1 || raw.toLowerCase().indexOf('katherin') !== -1) {
      searchInput.value = '';
      raw = '';
    }
    var q = raw.toLowerCase();
    var visibleTotal = 0;

    sections.forEach(function(sec) {
      var centerId = sec.getAttribute('data-center');
      var secMatchesCenter = (currentFilter === 'all' || currentFilter === centerId);
      var visibleInSec = 0;

      var secCards = sec.querySelectorAll('.card');
      secCards.forEach(function(c) {
        var title = c.getAttribute('data-title') || '';
        var cap = c.getAttribute('data-cap') || '';
        var num = c.getAttribute('data-num') || '';
        var matchesSearch = !q || title.indexOf(q) !== -1 || cap.indexOf(q) !== -1 || num === q;

        if (secMatchesCenter && matchesSearch) {
          c.classList.remove('hidden');
          visibleInSec++;
          visibleTotal++;
        } else {
          c.classList.add('hidden');
        }
      });

      sec.querySelectorAll('.phase-group').forEach(function(grupo) {
        var visibles = grupo.querySelectorAll('.card:not(.hidden)').length;
        grupo.classList.toggle('hidden', visibles === 0);
      });

      if (visibleInSec === 0) {
        sec.classList.add('hidden');
      } else {
        sec.classList.remove('hidden');
      }
    });

    if (noResults) {
      if (visibleTotal === 0) {
        noResults.classList.add('visible');
      } else {
        noResults.classList.remove('visible');
      }
    }
  }

  function setFilter(filterId, updateUrl) {
    currentFilter = filterId || 'all';
    chips.forEach(function(c) {
      if (c.getAttribute('data-filter') === currentFilter) {
        c.classList.add('active');
      } else {
        c.classList.remove('active');
      }
    });
    aplicarFiltros();
    if (updateUrl) {
      var newHash = (currentFilter === 'all') ? '' : '#sec-' + currentFilter;
      var curPath = window.location.pathname.endsWith('/') ? window.location.pathname : (window.location.pathname + '/');
      if (window.location.hash !== newHash) {
        if (history.replaceState) {
          history.replaceState(null, '', curPath + (newHash ? newHash : ''));
        } else {
          window.location.hash = newHash;
        }
      }
    }
  }

  function leerHash() {
    var h = (window.location.hash || '').replace('#', '');
    if (h) {
      var targetCenter = h.replace('sec-', '');
      var matchingChip = document.querySelector('.filter-chip[data-filter="' + targetCenter + '"]');
      if (matchingChip) {
        setFilter(targetCenter, false);
        return;
      }
    }
    setFilter('all', false);
  }

  chips.forEach(function(chip) {
    chip.addEventListener('click', function() {
      var f = chip.getAttribute('data-filter') || 'all';
      setFilter(f, true);
    });
  });

  if (searchInput) {
    searchInput.addEventListener('input', aplicarFiltros);
    searchInput.addEventListener('change', aplicarFiltros);
  }
  window.addEventListener('hashchange', leerHash);
  leerHash();
})();

// Carga progresiva (lazy loading) con indicador visual para miniaturas SVG
(function initThumbLazyLoading() {
  var lazyImgs = document.querySelectorAll('.thumb img[data-src]');
  if (!lazyImgs.length) return;

  function resolveThumbnailUrl(dataSrc) {
    if (!dataSrc || dataSrc.startsWith('http') || dataSrc.startsWith('data:') || dataSrc.startsWith('/')) {
      return dataSrc;
    }
    var path = window.location.pathname;
    if (!path.endsWith('/') && !path.endsWith('.html')) {
      return path + '/' + dataSrc;
    }
    return dataSrc;
  }

  function markLoaded(img) {
    var parent = img.closest('.thumb');
    if (parent) parent.classList.add('loaded');
    img.classList.add('is-loaded');
  }

  if ('IntersectionObserver' in window) {
    var observer = new IntersectionObserver(function (entries, obs) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          var img = entry.target;
          var dataSrc = img.getAttribute('data-src');
          if (dataSrc) {
            var targetSrc = resolveThumbnailUrl(dataSrc);
            img.onload = function () {
              markLoaded(img);
            };
            img.onerror = function () {
              var parent = img.closest('.thumb');
              if (parent) parent.classList.add('loaded', 'error');
            };
            img.src = targetSrc;
            img.removeAttribute('data-src');
            if (img.complete && img.naturalWidth > 0) {
              markLoaded(img);
            }
          }
          obs.unobserve(img);
        }
      });
    }, {
      rootMargin: '300px 0px 300px 0px',
      threshold: 0.01
    });

    lazyImgs.forEach(function (img) {
      observer.observe(img);
    });
  } else {
    lazyImgs.forEach(function (img) {
      var dataSrc = img.getAttribute('data-src');
      if (dataSrc) {
        img.src = resolveThumbnailUrl(dataSrc);
        img.removeAttribute('data-src');
      }
      markLoaded(img);
    });
  }
})();
