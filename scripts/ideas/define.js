/* Tap to define: every glossary term in the running text becomes tappable and shows its definition in a small card.
   The terms come from the chapter's own Glossary (the builder copies them in as JSON), so it works on any edition of
   any chapter and adds no height to the page. A term is marked once per section, never inside a heading, a table of
   definitions, a widget, a link or a formula, and the text itself is not restyled beyond a dotted underline. */
(function () {
  var terms; try { terms = JSON.parse(document.getElementById('df-terms').textContent); } catch (e) { return; }
  if (!terms || !terms.length) return;
  function norm(s) { return s.toLowerCase().replace(/[\s -]+/g, ' ').trim(); }
  function esc(s) { return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }
  var by = {}; terms.forEach(function (t) { by[norm(t[0])] = t; });
  function find(word) { var k = norm(word); return by[k] || by[k.replace(/es$/, '')] || by[k.replace(/s$/, '')]; }
  var alts = terms.map(function (t) { return t[0]; }).sort(function (a, b) { return b.length - a.length; })
    .map(function (t) { return esc(t).replace(/[\s-]+/g, '[\\s\\u00a0-]+') + '(?:es|s)?'; });
  var re = new RegExp('(^|[^A-Za-z0-9])(' + alts.join('|') + ')(?![A-Za-z0-9])', 'i');
  var SKIP = 'h1,h2,h3,h4,h5,a,button,summary,script,style,noscript,code,pre,svg,input,textarea,select,label,mjx-container,' +
    '.pmw,.tpw,.sdg,.pertw,.hp10,.toc-box,.ls-bar,.ls-pill,.df-pop,.df-term,.video-section,.dz-bar';

  /* the text nodes of the page in reading order, each with the section it belongs to */
  var walker = document.createTreeWalker(document.body, NodeFilter.SHOW_ELEMENT | NodeFilter.SHOW_TEXT), n, sec = 0, gloss = false, jobs = [];
  while ((n = walker.nextNode())) {
    if (n.nodeType === 1) { if (/^H[12]$/.test(n.tagName) && !n.closest('.toc-box')) { sec++; gloss = /^glossary$/i.test(n.textContent.trim()); } continue; }
    if (gloss || !n.nodeValue || n.nodeValue.length < 3 || /\\[(\[]|\$/.test(n.nodeValue)) continue;
    if (!n.parentNode || n.parentNode.closest(SKIP)) continue;
    jobs.push([n, sec]);
  }
  var seen = {};
  jobs.forEach(function (job) {
    var node = job[0], s = job[1], m;
    while (node && (m = re.exec(node.nodeValue))) {
      var t = find(m[2]), start = m.index + m[1].length;
      var rest = node.splitText(start), after = rest.splitText(m[2].length);
      if (t && !seen[s + '|' + t[0]]) {
        seen[s + '|' + t[0]] = 1;
        var span = document.createElement('span'); span.className = 'df-term'; span.tabIndex = 0;
        span.setAttribute('role', 'button'); span.setAttribute('aria-expanded', 'false'); span.dataset.term = t[0];
        rest.parentNode.replaceChild(span, rest); span.appendChild(rest);
      }
      node = after;
    }
  });

  var pop = document.createElement('div'); pop.className = 'df-pop'; pop.hidden = true; pop.setAttribute('role', 'tooltip'); pop.id = 'df-pop';
  document.body.appendChild(pop);
  var shown = null;
  function hide() { if (shown) shown.setAttribute('aria-expanded', 'false'); shown = null; pop.hidden = true; }
  function show(el) {
    var t = by[norm(el.dataset.term)]; if (!t) return;
    if (shown === el) { hide(); return; }
    hide(); shown = el; el.setAttribute('aria-expanded', 'true'); el.setAttribute('aria-describedby', 'df-pop');
    pop.textContent = ''; var b = document.createElement('b'); b.textContent = t[0]; pop.appendChild(b); pop.appendChild(document.createTextNode(t[1]));
    pop.hidden = false;
    var r = el.getBoundingClientRect(), w = Math.min(340, window.innerWidth - 24); pop.style.width = w + 'px';
    var left = Math.max(12, Math.min(r.left + r.width / 2 - w / 2, window.innerWidth - w - 12)), h = pop.offsetHeight;
    var below = r.bottom + 8 + h < window.innerHeight - 8 || r.top - 8 - h < 8;
    pop.style.left = (left + window.scrollX) + 'px';
    pop.style.top = ((below ? r.bottom + 8 : r.top - 8 - h) + window.scrollY) + 'px';
  }
  document.addEventListener('click', function (ev) {
    var el = ev.target.closest && ev.target.closest('.df-term');
    if (el) { ev.stopPropagation(); show(el); } else if (!ev.target.closest || !ev.target.closest('.df-pop')) hide();
  }, true);
  document.addEventListener('keydown', function (ev) {
    if (ev.key === 'Escape') hide();
    else if ((ev.key === 'Enter' || ev.key === ' ') && ev.target.classList && ev.target.classList.contains('df-term')) { ev.preventDefault(); show(ev.target); }
  });
  window.addEventListener('resize', hide);
  window.__df = { count: document.querySelectorAll('.df-term').length };
})();
