/* Listen: any notes page read aloud, section by section, from a bar pinned to the bottom of the screen.
   It needs nothing from the page but its h1/h2 headings, so it works on every chapter of every course. */
(function () {
  var clips; try { clips = JSON.parse(document.getElementById('ls-audio').textContent); } catch (e) { return; }
  if (!clips || !clips.length) return;
  var RATES = [1, 1.25, 1.5, 0.85], rate = 0, i = 0, aud = new Audio(), open = false;
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
  function mark(scroll) {
    var hs = heads(), h = hs[clips[i].h];
    hs.forEach(function (x) { x.classList.remove('ls-now'); });
    if (h) { h.classList.add('ls-now'); if (scroll) h.scrollIntoView({ behavior: 'smooth', block: 'start' }); }
    var left = clips.slice(i).reduce(function (a, c) { return a + c.d; }, 0) - (aud.currentTime || 0);
    title.textContent = (i + 1) + '/' + clips.length + ' · ' + clips[i].t + ' · ' + fmt(Math.max(left, 0) / RATES[rate]) + ' left';
    prev.disabled = i === 0; next.disabled = i === clips.length - 1;
    try { localStorage.setItem('ls-at:' + location.pathname, i); } catch (e) {}
  }
  function load(j, go, scroll) {
    i = j; aud.src = clips[i].s; aud.playbackRate = RATES[rate]; mark(scroll);
    if (go) { var p = aud.play(); if (p && p.catch) p.catch(function () {}); }
  }
  function label() { var on = !aud.paused; play.innerHTML = on ? '&#10074;&#10074;' : '&#9654;'; play.setAttribute('aria-label', on ? 'Pause' : 'Play'); }
  aud.addEventListener('play', label); aud.addEventListener('pause', label);
  aud.addEventListener('timeupdate', function () { track.firstChild.style.width = (aud.currentTime / (aud.duration || clips[i].d) * 100) + '%'; mark(false); });
  aud.addEventListener('ended', function () { if (i < clips.length - 1) load(i + 1, true, true); else label(); });
  play.onclick = function () { if (aud.paused) { var p = aud.play(); if (p && p.catch) p.catch(function () {}); } else aud.pause(); };
  prev.onclick = function () { load(Math.max(i - 1, 0), !aud.paused, true); };
  next.onclick = function () { load(Math.min(i + 1, clips.length - 1), !aud.paused, true); };
  speed.onclick = function () { rate = (rate + 1) % RATES.length; aud.playbackRate = RATES[rate]; speed.textContent = RATES[rate] + '×'; mark(false); };
  track.onclick = function (ev) { var r = track.getBoundingClientRect(); aud.currentTime = (ev.clientX - r.left) / r.width * (aud.duration || clips[i].d); };
  pill.onclick = function () {
    open = true; bar.hidden = false; pill.hidden = true; document.body.classList.add('ls-open');
    /* start from the section on screen, not from the top */
    var hs = heads(), best = i, y = 1e9;
    clips.forEach(function (c, j) { var h = hs[c.h]; if (!h) return; var t = h.getBoundingClientRect().top; if (t > -40 && t < y) { y = t; best = j; } });
    if (y < window.innerHeight) i = best;
    load(i, true, false);
  };
  close.onclick = function () { aud.pause(); open = false; bar.hidden = true; pill.hidden = false; document.body.classList.remove('ls-open'); heads().forEach(function (x) { x.classList.remove('ls-now'); }); };
  pill.title = 'About ' + Math.round(total / 60) + ' minutes';
  window.__ls = { clips: clips, audio: aud };
})();
