/* Depth switch: one page holds the Concise, Balanced and Full text of every section.
   The bar at the top sets the whole page; the link under a section changes that section only. */
(function () {
  var ORDER = ['c', 'b', 'f'], NAME = { c: 'Short', b: 'Medium', f: 'Full' };
  var secs = Array.prototype.slice.call(document.querySelectorAll('.dz')), bar = document.querySelector('.dz-bar');
  if (!bar) return;
  var btns = Array.prototype.slice.call(bar.querySelectorAll('button[data-d]')), time = bar.querySelector('.dz-time');

  function has(sec, d) { return !!sec.querySelector(':scope > .dz-v[data-d="' + d + '"]'); }
  function nearest(sec, d) {   /* the asked-for depth, or the next longer one this section has, or the next shorter */
    var i = ORDER.indexOf(d), j;
    for (j = i; j < 3; j++) if (has(sec, ORDER[j])) return ORDER[j];
    for (j = i; j >= 0; j--) if (has(sec, ORDER[j])) return ORDER[j];
    return null;
  }
  function show(sec, d) {
    d = nearest(sec, d); if (!d) return;
    sec.dataset.now = d;
    Array.prototype.forEach.call(sec.querySelectorAll(':scope > .dz-v'), function (v) { v.hidden = v.dataset.d !== d; });
    var more = sec.querySelector(':scope > .dz-more'); if (!more) return;
    var i = ORDER.indexOf(d), up = null, down = null, j;
    for (j = i + 1; j < 3; j++) if (has(sec, ORDER[j])) { up = ORDER[j]; break; }
    for (j = i - 1; j >= 0; j--) if (has(sec, ORDER[j])) { down = ORDER[j]; break; }
    more.innerHTML = '';
    [[down, '− Less'], [up, '+ More detail']].forEach(function (p) {
      if (!p[0]) return;
      var b = document.createElement('button'); b.type = 'button'; b.textContent = p[1];
      b.setAttribute('aria-label', p[1].slice(2) + ' on this section (' + NAME[p[0]] + ')');
      b.onclick = function () { keep(sec, function () { show(sec, p[0]); }); mixed(); };
      more.appendChild(b);
    });
  }
  function keep(anchor, fn) {   /* change the page without moving what the reader is looking at */
    var el = anchor.previousElementSibling || anchor, y = el.getBoundingClientRect().top;
    fn(); window.scrollBy(0, el.getBoundingClientRect().top - y);
  }
  function minutes() {
    var w = 0; secs.forEach(function (s) { var v = s.querySelector(':scope > .dz-v:not([hidden])'); if (v) w += +v.dataset.w || 0; });
    time.textContent = 'about ' + Math.max(1, Math.round(w / 200)) + ' min read';
  }
  function mixed() {
    var seen = {}; secs.forEach(function (s) { seen[s.dataset.want || ''] = 1; });
    minutes();
  }
  function all(d, anchor) {
    var go = function () { secs.forEach(function (s) { s.dataset.want = d; show(s, d); }); };
    if (anchor) keep(anchor, go); else go();
    btns.forEach(function (b) { b.setAttribute('aria-pressed', b.dataset.d === d ? 'true' : 'false'); });
    try { localStorage.setItem('dz-depth', d); } catch (e) {}
    minutes();
  }
  btns.forEach(function (b) {
    b.onclick = function () {
      var top = null;   /* the first section still on screen stays where it is */
      for (var i = 0; i < secs.length; i++) { if (secs[i].getBoundingClientRect().bottom > 60) { top = secs[i]; break; } }
      all(b.dataset.d, top);
    };
  });
  var start = 'c'; try { start = localStorage.getItem('dz-depth') || 'c'; } catch (e) {}
  if (/depth=([cbf])/.test(location.hash)) start = RegExp.$1;
  all(start, null);
})();
