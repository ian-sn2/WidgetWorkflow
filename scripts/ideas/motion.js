/* Motion for the MAN4504 widgets (see motion.css). An add-on: it reads the widgets' drawings and never changes their code.
   It does four things CSS alone cannot: starts a widget's entry when the widget is first seen, numbers nodes and arrows
   in the order work flows so a path is traced start to finish, notices which table cells changed, and sweeps the
   deadline slider once so the reader sees it can be moved. */
(function () {
  if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  if (!window.IntersectionObserver || !window.MutationObserver) return;
  document.documentElement.classList.add('mv');
  var each = function (list, fn) { Array.prototype.forEach.call(list, fn); };

  /* ---- the order of flow: --i on every node and arrow, left to right (top to bottom on a phone) ---- */
  function decorate(svg, flow) {
    if (svg.dataset.mv) return; svg.dataset.mv = '1';
    var vb = (svg.getAttribute('viewBox') || '0 0 2 1').split(/\s+/), down = +vb[3] > +vb[2] * 1.15, keys = [], items = [];
    each(svg.querySelectorAll('g.n'), function (g) {
      var m = /translate\(([-\d.]+)[ ,]+([-\d.]+)\)/.exec(g.getAttribute('transform') || ''); if (!m) return;
      items.push([g, down ? +m[2] : +m[1]]);
    });
    each(svg.querySelectorAll('g.e'), function (g) {
      var l = g.querySelector('.e-l'); if (!l) return;
      items.push([g, +(down ? l.getAttribute('y1') : l.getAttribute('x1')) - 30]);   /* an arrow goes with the node it leaves */
      if (flow && /\b(crit|path)\b/.test(g.getAttribute('class')) && !g.querySelector('.e-flow')) {
        var f = l.cloneNode(false); f.setAttribute('class', 'e-flow'); g.appendChild(f);   /* dashes that run along the path */
      }
    });
    items.forEach(function (it) { var k = Math.round(it[1] / 40); if (keys.indexOf(k) < 0) keys.push(k); });
    keys.sort(function (a, b) { return a - b; });
    items.forEach(function (it) { it[0].style.setProperty('--i', keys.indexOf(Math.round(it[1] / 40))); });
  }
  each(document.querySelectorAll('.pmw[data-pm]'), function (w) {
    if (w.dataset.pm === 'lab') return;            /* the what-if lab animates itself */
    var body = w.querySelector('.pm-body'); if (!body) return;
    var run = function () { each(body.querySelectorAll('svg'), function (s) { decorate(s, w.dataset.pm === 'net'); }); };
    run(); new MutationObserver(run).observe(body, { childList: true, subtree: true });
  });
  each(document.querySelectorAll('.pm-beta-svg .curve'), function (p) { p.setAttribute('pathLength', '1'); });

  /* ---- transportation table: pop a quantity when it is written, flash a total when it changes ---- */
  each(document.querySelectorAll('.tpw'), function (w) {
    var last = new WeakMap(), sc = w.querySelector('.tp-scroll'), cap = w.querySelector('div.tp-cap'), ready = false;
    function kick(el, cls) { el.classList.remove(cls); void el.offsetWidth; el.classList.add(cls); }
    function scan() {
      each(w.querySelectorAll('.tp-q, td.tp-cap, td.tp-dem'), function (el) {
        var now = el.textContent, was = last.get(el); last.set(el, now);
        if (!ready || was === undefined || was === now || !now) return;
        kick(el, el.classList.contains('tp-q') ? 'mv-pop' : 'mv-chg');
      });
      ready = true;
    }
    if (sc) { scan(); new MutationObserver(scan).observe(sc, { childList: true, subtree: true, characterData: true }); }
    if (cap) new MutationObserver(function () { kick(cap, 'mv-chg'); }).observe(cap, { childList: true });
  });

  /* ---- the deadline slider moves by itself once, from the left to where it starts ---- */
  function sweep(w) {
    var inp = w.querySelector('input[type=range]'); if (!inp || inp.dataset.mv) return; inp.dataset.mv = '1';
    var to = +inp.value, from = +inp.min || 0, t0 = null, stop = false;
    if (to - from < 2) return;
    ['pointerdown', 'keydown', 'touchstart'].forEach(function (ev) { inp.addEventListener(ev, function () { stop = true; }, { once: true }); });
    function put(v) { inp.value = v; inp.dispatchEvent(new Event('input', { bubbles: true })); }
    put(from);
    setTimeout(function () {
      requestAnimationFrame(function step(ts) {
        if (stop) return; if (t0 === null) t0 = ts;
        var k = Math.min((ts - t0) / 1600, 1), e = k < .5 ? 2 * k * k : 1 - Math.pow(-2 * k + 2, 2) / 2, v = Math.round(from + (to - from) * e);
        if (+inp.value !== v) put(v);
        if (k < 1) requestAnimationFrame(step); else if (+inp.value !== to) put(to);
      });
    }, 350);
  }

  /* ---- a widget's entry plays when it is first seen, not while it is still below the screen ---- */
  var widgets = document.querySelectorAll('.pmw, .tpw');
  function seen(w) { w.classList.remove('mv-wait'); w.classList.add('mv-in'); if (w.dataset.pm === 'deadline') sweep(w); }
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { io.unobserve(e.target); seen(e.target); } });
  }, { threshold: 0.2 });
  each(widgets, function (w) {
    if (w.dataset.pm === 'lab') return;
    if (w.getBoundingClientRect().top > window.innerHeight) w.classList.add('mv-wait');
    io.observe(w);
  });
  function all() { each(widgets, function (w) { if (w.classList.contains('mv-wait')) seen(w); }); }
  window.addEventListener('beforeprint', all);
  window.__mv = { showAll: all };
})();
