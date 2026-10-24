(function() {
  var themeBtn = document.getElementById('theme-toggle');
  var searchInput = document.getElementById('search-input');
  var chips = document.querySelectorAll('.filter-chip');
  var cards = document.querySelectorAll('.card');
  var sections = document.querySelectorAll('.center-section');
  var noResults = document.getElementById('no-results');

  // Alternar tema
  themeBtn.addEventListener('click', function() {
    var cur = document.documentElement.getAttribute('data-theme') || 'dark';
    var next = cur === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    try { localStorage.setItem('archify-theme', next); } catch (_) {}
  });

  // Inicializar conteos reales de los chips según las tarjetas en el DOM
  chips.forEach(function(chip) {
    var filter = chip.getAttribute('data-filter');
    var label = chip.textContent.trim();
    var count = filter === 'all' ? cards.length : document.querySelectorAll('.card[data-center="' + filter + '"]').length;
    chip.textContent = label + ' (' + count + ')';
  });

  var currentFilter = 'all';

  function aplicarFiltros() {
    var q = (searchInput.value || '').trim().toLowerCase();
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

    if (visibleTotal === 0) {
      noResults.classList.add('visible');
    } else {
      noResults.classList.remove('visible');
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
      if (window.location.hash !== newHash) {
        if (history.replaceState) {
          history.replaceState(null, '', window.location.pathname + (newHash ? newHash : ''));
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

  searchInput.addEventListener('input', aplicarFiltros);
  window.addEventListener('hashchange', leerHash);
  leerHash();
})();
