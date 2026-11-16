/* Listen: any notes page spoken aloud, section by section, from a bar pinned to the bottom of the screen.
   While it talks, the bullet, table row or paragraph it is talking about is highlighted, and the page scrolls to keep
   it in view. Tapping a block that has narration jumps the audio to it. Headings are never restyled.
   The clips and their timings come from narrate.py: [{s: audio, d: seconds, h: heading index, t: title,
   seg: [[start second, block number or -1], ...]}], and each block carries data-ls="<number>". */
(function () {
  var clips; try { clips = JSON.parse(document.getElementById('ls-audio').textContent); } catch (e) { return; }
  if (!clips || !clips.length) return;
  var RATES = [1, 1.25, 1.5, 0.85], rate = 0, i = 0, aud = new Audio(), open = false, lit = null, cur = -2, userAt = 0, where = {};
  clips.forEach(function (c, ci) { (c.seg || []).forEach(function (s, si) { if (s[1] >= 0 && !(s[1] in where)) where[s[1]] = [ci, si]; }); });
  try { i = Math.min(+localStorage.getItem('ls-at:' + location.pathname) || 0, clips.length - 1); } catch (e) {}
  function heads() { return Array.prototype.filter.call(document.querySelectorAll('h1, h2'), function (h) { return !h.closest('.toc-box, .ls-bar'); }); }
  function el(tag, cls, html, parent) { var e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; if (parent) parent.appendChild(e); return e; }
  function btn(cls, html, label, parent) { var b = el('button', cls, html, parent); b.type = 'button'; b.setAttribute('aria-label', label); return b; }

  var pill = btn('ls-pill', '&#127911; Listen', 'Listen to this chapter', document.body);
  var bar = el('div', 'ls-bar', null, document.body); bar.hidden = true; bar.setAttribute('role', 'region'); bar.setAttribute('aria-label', 'Chapter audio');
  var prev = btn('', '&#9198;', 'Previous section', bar), play = btn('ls-play', '&#9654;', 'Play', bar), next = btn('', '&#9197;', 'Next section', bar);
  var mid = el('div', 'ls-mid', null, bar), title = el('div', 'ls-title', '', mid), track = el('div', 'ls-track', '<i></i>', mid);
  var speed = btn('ls-speed', '1×', 'Playback speed', bar), close = btn('', '&#10005;', 'Close the audio bar', bar);
  var total = clips.reduce(function (a, c) { return a + c.d; }, 0);

  function fmt(s) { s = Math.round(s); return Math.floor(s / 60) + ':' + ('0' + s % 60).slice(-2); }
  function calm() { return window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches; }
  /* follow along: bring el into the middle of the screen, unless the reader has just scrolled somewhere themselves */
  function follow(e) {
    if (!e || Date.now() - userAt < 4000) return;
    var r = e.getBoundingClientRect(), top = 70, bottom = window.innerHeight - 110;
    if (r.top >= top && r.bottom <= bottom) return;
    e.scrollIntoView({ behavior: calm() ? 'auto' : 'smooth', block: r.height > bottom - top ? 'start' : 'center' });
  }
  ['wheel', 'touchmove', 'keydown'].forEach(function (ev) {
    window.addEventListener(ev, function (e) { if (!e.target.closest || !e.target.closest('.ls-bar')) userAt = Date.now(); }, { passive: true });
  });
  function light(block) {
    if (lit === block) return;
    if (lit) lit.classList.remove('ls-hi');
    lit = block; if (lit) lit.classList.add('ls-hi');
  }
  function passage(force) {            /* which passage of this section is being spoken, and what it is about */
    var seg = clips[i].seg; if (!seg) return;
    var t = aud.currentTime || 0, k = 0;
    for (var j = 0; j < seg.length; j++) if (seg[j][0] <= t + 0.05) k = j;
    if (k === cur && !force) return; cur = k;
    var block = seg[k][1] >= 0 ? document.querySelector('[data-ls="' + seg[k][1] + '"]') : null;
    light(block);
    follow(block || (k === 0 ? heads()[clips[i].h] : null));
  }
  function status() {
    var left = clips.slice(i).reduce(function (a, c) { return a + c.d; }, 0) - (aud.currentTime || 0);
    title.textContent = (i + 1) + '/' + clips.length + ' · ' + clips[i].t + ' · ' + fmt(Math.max(left, 0) / RATES[rate]) + ' left';
    prev.disabled = i === 0; next.disabled = i === clips.length - 1;
  }
  function load(j, go, at) {
    i = j; cur = -2; aud.src = clips[i].s; aud.playbackRate = RATES[rate];
    if (at) aud.currentTime = at;
    status(); if (!clips[i].seg) follow(heads()[clips[i].h]);
    try { localStorage.setItem('ls-at:' + location.pathname, i); } catch (e) {}
    if (go) { var p = aud.play(); if (p && p.catch) p.catch(function () {}); }
  }
  function label() { var on = !aud.paused; play.innerHTML = on ? '&#10074;&#10074;' : '&#9654;'; play.setAttribute('aria-label', on ? 'Pause' : 'Play'); }
  aud.addEventListener('play', label); aud.addEventListener('pause', label);
  aud.addEventListener('timeupdate', function () { track.firstChild.style.width = (aud.currentTime / (aud.duration || clips[i].d) * 100) + '%'; status(); passage(false); });
  aud.addEventListener('ended', function () { if (i < clips.length - 1) load(i + 1, true); else { label(); light(null); } });
  play.onclick = function () { if (aud.paused) { var p = aud.play(); if (p && p.catch) p.catch(function () {}); } else aud.pause(); };
  prev.onclick = function () { userAt = 0; load(Math.max(i - 1, 0), !aud.paused); };
  next.onclick = function () { userAt = 0; load(Math.min(i + 1, clips.length - 1), !aud.paused); };
  speed.onclick = function () { rate = (rate + 1) % RATES.length; aud.playbackRate = RATES[rate]; speed.textContent = RATES[rate] + '×'; status(); };
  track.onclick = function (ev) { var r = track.getBoundingClientRect(); userAt = 0; aud.currentTime = (ev.clientX - r.left) / r.width * (aud.duration || clips[i].d); };
  /* tap a narrated block to hear it from there */
  document.addEventListener('click', function (ev) {
    if (!open || !ev.target.closest) return;
    if (ev.target.closest('a, button, summary, input, .df-term, .ls-bar, .pmw, .tpw, .sdg')) return;
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
  close.onclick = function () { aud.pause(); open = false; bar.hidden = true; pill.hidden = false; document.body.classList.remove('ls-open'); light(null); };
  pill.title = 'About ' + Math.round(total / 60) + ' minutes';
  window.__ls = { clips: clips, audio: aud, lit: function () { return lit; } };
})();
