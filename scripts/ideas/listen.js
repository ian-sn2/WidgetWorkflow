/* Listen: any notes page spoken aloud, section by section, from a bar pinned to the bottom of the screen.
   While it talks, the bullet, table row or paragraph it is talking about is highlighted, and the page scrolls to keep
   it in view. Tapping a block that has narration jumps the audio to it. Headings are never restyled.
   The clips and their timings come from narrate.py: [{s: audio, d: seconds, h: heading index, t: title,
   seg: [[start second, block numbers], ...]}], and each block carries data-ls="<number>". The bar has a list of the
   sections to jump between, and a list of speeds from 0.85x to 2x; the speed chosen is remembered. */
(function () {
  var src = document.getElementById('ls-audio'), clips; try { clips = JSON.parse(src.textContent); } catch (e) { return; }
  if (!clips || !clips.length) return;
  var HSEL = src.getAttribute('data-heads') || 'h1, h2';     /* which headings the audio is divided at */
  var RATES = [0.85, 1, 1.25, 1.5, 1.75, 2], rate = 1, i = 0, aud = new Audio(), open = false, lit = null, cur = -2, userAt = 0, where = {};
  function ids(s) { return [].concat(s[1]).filter(function (b) { return b >= 0; }); }   /* a passage speaks for no block, one, or several */
  clips.forEach(function (c, ci) { (c.seg || []).forEach(function (s, si) { ids(s).forEach(function (b) { if (!(b in where)) where[b] = [ci, si]; }); }); });
  try { i = Math.min(+localStorage.getItem('ls-at:' + location.pathname) || 0, clips.length - 1); } catch (e) {}
  try { var saved = RATES.indexOf(+localStorage.getItem('ls-rate')); if (saved >= 0) rate = saved; } catch (e) {}
  function heads() { return Array.prototype.filter.call(document.querySelectorAll(HSEL), function (h) { return !h.closest('.toc-box, .ls-bar'); }); }
  function el(tag, cls, html, parent) { var e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; if (parent) parent.appendChild(e); return e; }
  function btn(cls, html, label, parent) { var b = el('button', cls, html, parent); b.type = 'button'; b.setAttribute('aria-label', label); return b; }

  var pill = btn('ls-pill', '&#127911; Listen', 'Listen to this chapter', document.body);
  var bar = el('div', 'ls-bar', null, document.body); bar.hidden = true; bar.setAttribute('role', 'region'); bar.setAttribute('aria-label', 'Chapter audio');
  var list = btn('ls-list', '&#9776;', 'Choose a section', bar);
  var prev = btn('ls-skip', '&#9198;', 'Previous section', bar), play = btn('ls-play', '&#9654;', 'Play', bar), next = btn('ls-skip', '&#9197;', 'Next section', bar);
  var mid = el('div', 'ls-mid', null, bar), title = el('div', 'ls-title', '', mid), track = el('div', 'ls-track', '<i></i>', mid);
  var speed = btn('ls-speed', RATES[rate] + '×', 'Playback speed', bar), close = btn('', '&#10005;', 'Close the audio bar', bar);
  var menu = el('div', 'ls-menu', null, document.body); menu.hidden = true; menu.setAttribute('role', 'menu');
  var total = clips.reduce(function (a, c) { return a + c.d; }, 0);

  function fmt(s) { s = Math.round(s); return Math.floor(s / 60) + ':' + ('0' + s % 60).slice(-2); }
  function calm() { return window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches; }
  /* follow along: bring el into the middle of the screen, unless the reader has just scrolled somewhere themselves */
  function follow(e) {            /* e: an element, or a range of text */
    if (!e || Date.now() - userAt < 4000) return;
    var r = e.getBoundingClientRect(), top = 70, bottom = window.innerHeight - 110;
    if (!r.height || (r.top >= top && r.bottom <= bottom)) return;
    var to = r.height > bottom - top ? r.top - top : (r.top + r.bottom) / 2 - (top + bottom) / 2;
    window.scrollBy({ top: to, behavior: calm() ? 'auto' : 'smooth' });
  }
  ['wheel', 'touchmove', 'keydown'].forEach(function (ev) {
    window.addEventListener(ev, function (e) { if (!e.target.closest || !e.target.closest('.ls-bar')) userAt = Date.now(); }, { passive: true });
  });
  function light(blocks) {
    (lit || []).forEach(function (b) { b.classList.remove('ls-hi'); });
    lit = blocks && blocks.length ? blocks : null;
    (lit || []).forEach(function (b) { b.classList.add('ls-hi'); });
  }

  /* ---- following the words: the sentence being spoken is marked, and a marker moves through it word by word ----
     Marks are drawn with the browser's highlight ranges, so the page's own markup is never touched. Where the browser
     has no such ranges, or a paragraph's text is not what was recorded (a formula redrawn by MathJax), the paragraph
     highlight alone is shown. */
  var HL = (window.CSS && CSS.highlights && window.Highlight) ? { sent: new Highlight(), word: new Highlight() } : null, maps = {}, fine = null, raf = 0;
  if (HL) { CSS.highlights.set('ls-sent', HL.sent); CSS.highlights.set('ls-word', HL.word); document.documentElement.classList.add('ls-fine'); }
  function charmap(id, block) {       /* the block's text as the recorder saw it: spaces collapsed, nested lists left out */
    if (id in maps) return maps[id];
    var w = document.createTreeWalker(block, NodeFilter.SHOW_TEXT), n, nodes = [], offs = [], text = '', space = false;
    while ((n = w.nextNode())) {
      var inner = n.parentNode.closest('ul, ol');
      if (inner && inner !== block && block.contains(inner)) continue;
      for (var k = 0, v = n.nodeValue; k < v.length; k++) {
        if (/\s/.test(v[k])) { space = text.length > 0; continue; }
        if (space) { text += ' '; nodes.push(n); offs.push(k - 1 >= 0 ? k - 1 : 0); space = false; }
        text += v[k]; nodes.push(n); offs.push(k);
      }
    }
    return (maps[id] = { text: text, nodes: nodes, offs: offs });
  }
  function span(m, a, b) {
    a = Math.max(0, Math.min(a, m.text.length - 1)); b = Math.max(a + 1, Math.min(b, m.text.length));
    var r = document.createRange(); r.setStart(m.nodes[a], m.offs[a]); r.setEnd(m.nodes[b - 1], m.offs[b - 1] + 1); return r;
  }
  function unmark() { if (HL) { HL.sent.clear(); HL.word.clear(); } }
  function words(m, c0, c1) {         /* each word of the sentence with a weight for how long it takes to say */
    var out = [], re = /[^\s\u2014]+\u2014?/g, x, t = m.text.slice(c0, c1), sum = 0;
    while ((x = re.exec(t))) {
      var wd = x[0], wt = wd.replace(/[^A-Za-z]/g, '').length + 2.5 * wd.replace(/\D/g, '').length + (/[,;:)]$/.test(wd) ? 2.5 : 0) + 1;
      sum += wt; out.push([c0 + x.index, c0 + x.index + wd.length, sum]);
    }
    return out;
  }
  function tick() {
    raf = 0; if (!fine) return;
    var t = aud.currentTime || 0, S = fine.sents, j = 0;
    for (var q = 0; q < S.length; q++) if (S[q][0] <= t + 0.02) j = q;
    if (j !== fine.j) {
      fine.j = j; fine.w = -1; fine.words = words(fine.m, S[j][1], S[j][2]);
      HL.sent.clear(); var r = span(fine.m, S[j][1], S[j][2]); HL.sent.add(r); follow(r);
    }
    var W = fine.words, end = (j + 1 < S.length ? S[j + 1][0] : fine.end) - 0.25, len = Math.max(end - S[j][0], 0.4);
    if (W.length) {
      var at = Math.min(Math.max((t - S[j][0]) / len, 0), 0.999) * W[W.length - 1][2], k = 0;
      while (k < W.length - 1 && W[k][2] <= at) k++;
      if (k !== fine.w) { fine.w = k; HL.word.clear(); HL.word.add(span(fine.m, W[k][0], W[k][1])); }
    }
    if (!aud.paused) raf = requestAnimationFrame(tick);
  }
  function passage(force) {            /* which passage of this section is being spoken, and what it is about */
    var seg = clips[i].seg; if (!seg) return;
    var t = aud.currentTime || 0, k = 0;
    for (var j = 0; j < seg.length; j++) if (seg[j][0] <= t + 0.05) k = j;
    if (k === cur && !force) { if (fine && !raf) tick(); return; }
    cur = k;
    var blocks = ids(seg[k]).map(function (b) { return document.querySelector('[data-ls="' + b + '"]'); }).filter(Boolean);
    light(blocks); unmark(); fine = null;
    if (HL && seg[k][2] && blocks.length === 1) {
      var m = charmap(ids(seg[k])[0], blocks[0]);
      if (m.text.length === seg[k][3]) fine = { m: m, sents: seg[k][2], end: k + 1 < seg.length ? seg[k + 1][0] : clips[i].d, j: -1, w: -1, words: [] };
    }
    if (!fine && HL && blocks.length === 1 && /^H[1-4]$/.test(blocks[0].tagName)) {      /* a heading is always marked while it is read: its words, never its box */
      var all = document.createRange(); all.selectNodeContents(blocks[0]); HL.sent.add(all);
    }
    if (fine) tick(); else follow(blocks[0] || (k === 0 ? heads()[clips[i].h] : null));
  }
  function status() {
    var left = clips.slice(i).reduce(function (a, c) { return a + c.d; }, 0) - (aud.currentTime || 0);
    title.textContent = (i + 1) + '/' + clips.length + ' · ' + clips[i].t + ' · ' + fmt(Math.max(left, 0) / RATES[rate]) + ' left';
    prev.disabled = i === 0; next.disabled = i === clips.length - 1;
  }
  function load(j, go, at) {
    i = j; cur = -2; aud.preload = 'metadata'; aud.src = clips[i].s; aud.defaultPlaybackRate = aud.playbackRate = RATES[rate];
    if (at) {            /* audio fetched from a server is not there yet: ask now, and ask again once its length is known */
      var want = at, again = function () { aud.removeEventListener('loadedmetadata', again); if (Math.abs(aud.currentTime - want) > 1) aud.currentTime = want; };
      try { aud.currentTime = at; } catch (e) {}
      aud.addEventListener('loadedmetadata', again);
    }
    status(); if (!clips[i].seg) follow(heads()[clips[i].h]);
    try { localStorage.setItem('ls-at:' + location.pathname, i); } catch (e) {}
    if (go) { var p = aud.play(); if (p && p.catch) p.catch(function () {}); }
  }
  function label() { var on = !aud.paused; play.innerHTML = on ? '&#10074;&#10074;' : '&#9654;'; play.setAttribute('aria-label', on ? 'Pause' : 'Play'); }
  aud.addEventListener('play', function () { label(); if (fine && !raf) tick(); }); aud.addEventListener('pause', label);
  aud.addEventListener('error', function () { title.textContent = 'The audio could not be loaded. Check the connection and press play again.'; });
  aud.addEventListener('timeupdate', function () { track.firstChild.style.width = (aud.currentTime / (aud.duration || clips[i].d) * 100) + '%'; status(); passage(false); });
  aud.addEventListener('ended', function () { if (i < clips.length - 1) load(i + 1, true); else { label(); light(null); unmark(); fine = null; } });
  play.onclick = function () { if (aud.paused) { var p = aud.play(); if (p && p.catch) p.catch(function () {}); } else aud.pause(); };
  prev.onclick = function () { userAt = 0; load(Math.max(i - 1, 0), !aud.paused); };
  next.onclick = function () { userAt = 0; load(Math.min(i + 1, clips.length - 1), !aud.paused); };
  /* one pop-up above the bar, used for both lists: the sections of the chapter, and the playback speeds */
  function shut() { menu.hidden = true; menu.dataset.kind = ''; list.setAttribute('aria-expanded', 'false'); speed.setAttribute('aria-expanded', 'false'); }
  function pop(kind, opener, rows, chosen, pick) {
    if (!menu.hidden && menu.dataset.kind === kind) { shut(); return; }
    shut(); menu.textContent = ''; menu.dataset.kind = kind; menu.className = 'ls-menu ls-' + kind;
    el('div', 'ls-menu-h', kind === 'speed' ? 'Speed' : 'Sections', menu);
    rows.forEach(function (r, j) {
      var b = btn('', r, '', menu); b.removeAttribute('aria-label'); b.setAttribute('role', 'menuitemradio'); b.setAttribute('aria-checked', j === chosen ? 'true' : 'false');
      b.onclick = function () { shut(); pick(j); };
    });
    menu.hidden = false; opener.setAttribute('aria-expanded', 'true');
  }
  function setRate(j) { rate = j; aud.defaultPlaybackRate = aud.playbackRate = RATES[rate]; speed.textContent = RATES[rate] + '×'; status(); try { localStorage.setItem('ls-rate', RATES[rate]); } catch (e) {} }
  speed.onclick = function () {
    pop('speed', speed, RATES.map(function (r) { return '<b>' + r + '×</b><span>' + (r === 1 ? 'normal' : fmt(total / r) + ' in all') + '</span>'; }), rate, setRate);
  };
  list.onclick = function () {
    pop('sections', list, clips.map(function (c, j) { return '<b>' + (j + 1) + '. ' + c.t.replace(/</g, '&lt;') + '</b><span>' + fmt(c.d / RATES[rate]) + '</span>'; }), i,
      function (j) { userAt = 0; load(j, true); });
  };
  document.addEventListener('keydown', function (ev) { if (ev.key === 'Escape') shut(); });
  document.addEventListener('click', function (ev) { if (!menu.hidden && ev.target.closest && !ev.target.closest('.ls-menu, .ls-list, .ls-speed')) shut(); }, true);
  track.onclick = function (ev) { var r = track.getBoundingClientRect(); userAt = 0; aud.currentTime = (ev.clientX - r.left) / r.width * (aud.duration || clips[i].d); };
  /* tap a narrated block to hear it from there */
  document.addEventListener('click', function (ev) {
    if (!open || !ev.target.closest) return;
    if (ev.target.closest('a, button, summary, input, .df-term, .ls-bar, .ls-menu, .pmw, .tpw, .sdg, .pertw')) return;
    var b = ev.target.closest('[data-ls]'); if (!b) return;
    var w = where[b.getAttribute('data-ls')]; if (!w) return;
    userAt = 0;
    if (w[0] === i) { aud.currentTime = clips[i].seg[w[1]][0]; if (aud.paused) play.onclick(); passage(true); }
    else load(w[0], true, clips[w[0]].seg[w[1]][0]);
  });
  pill.onclick = function () {
    open = true; bar.hidden = false; pill.hidden = true; document.body.classList.add('ls-open');
    /* start from the section on screen, not from the top */
    var hs = heads(), best = i, y = 1e9;
    clips.forEach(function (c, j) { var h = hs[c.h]; if (!h) return; var t = h.getBoundingClientRect().top; if (t > -40 && t < y) { y = t; best = j; } });
    if (y < window.innerHeight) i = best;
    userAt = 0; load(i, true);
  };
  close.onclick = function () { shut(); aud.pause(); open = false; bar.hidden = true; pill.hidden = false; document.body.classList.remove('ls-open'); light(null); unmark(); fine = null; };
  pill.innerHTML = '&#127911; Listen &middot; ' + Math.max(1, Math.round(total / 60 / RATES[rate])) + ' min';     /* say how long before anyone presses it */
  window.__ls = { clips: clips, audio: aud, lit: function () { return lit && lit[0]; }, fine: function () { return fine; }, marks: function () { return HL ? [HL.sent.size, HL.word.size] : null; } };
})();
