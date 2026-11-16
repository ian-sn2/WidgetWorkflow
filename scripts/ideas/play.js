/* Play: turns any step-by-step widget into a narrated animation.
   It adds nothing to the widget's own code: it finds the widget's Next button and caption,
   presses Next on a timer and reads each caption aloud with the browser's built-in voice.
   #video=N (N from 1) shows widget N alone, full screen, and plays it: that is what the
   video recorder films. */
(function () {
  var KINDS = [
    { root: '.pmw', bar: '.pm-bar', next: '.pm-next', back: '.pm-back', cap: '.pm-cap.on', title: '.pm-title' },
    { root: '.tpw', bar: '.tp-bar', next: '.tp-next', back: '.tp-back', cap: 'div.tp-cap', title: '.tp-title' }
  ];
  var synth = window.speechSynthesis, players = [], current = null;
  var SAY = [[/\bES\b/g, 'early start'], [/\bEF\b/g, 'early finish'], [/\bLS\b/g, 'late start'], [/\bLF\b/g, 'late finish'],
    [/→/g, ' to '], [/−/g, ' minus '], [/÷/g, ' divided by '], [/×/g, ' times '], [/=/g, ' equals '], [/≤/g, ' at most '],
    [/\$(\d[\d,]*)/g, '$1 dollars'], [/\bwk\b/g, 'week'], [/--/g, ' none ']];

  function spoken(el) {
    var c = el.cloneNode(true);
    Array.prototype.forEach.call(c.querySelectorAll('br, b.pm-h, .pm-calc, li, p, div'), function (n) { n.insertAdjacentText('afterend', '. '); });
    var t = c.textContent.replace(/\s+/g, ' ').replace(/\.\s*\./g, '.').trim();
    SAY.forEach(function (p) { t = t.replace(p[0], p[1]); });
    return t;
  }
  function words(t) { return t.split(/\s+/).length; }

  function make(root, k) {
    var next = root.querySelector(k.next), back = root.querySelector(k.back);
    if (!next || !back || root.dataset.play) return;
    root.dataset.play = '1';
    var bar = next.parentNode;
    var play = document.createElement('button'); play.type = 'button'; play.className = 'pv-play';
    var voice = document.createElement('button'); voice.type = 'button'; voice.className = 'pv-voice';
    var prog = document.createElement('div'); prog.className = 'pv-prog'; prog.innerHTML = '<i></i>';
    bar.insertBefore(play, bar.firstChild); bar.appendChild(voice);
    bar.parentNode.insertBefore(prog, bar.nextSibling);
    var on = false, sound = !!synth, timer = null, token = 0;
    try { if (localStorage.getItem('pv-sound') === '0') sound = false; } catch (e) {}

    function label() {
      play.innerHTML = on ? '&#10074;&#10074; Pause' : (next.disabled ? '&#8635; Replay' : '&#9654; Play');
      play.setAttribute('aria-label', on ? 'Pause the walkthrough' : 'Play the walkthrough');
      voice.innerHTML = sound ? '&#128266;' : '&#128263;';
      voice.setAttribute('aria-label', sound ? 'Narration on. Turn narration off' : 'Narration off. Turn narration on');
      voice.hidden = !synth;
    }
    function bar_(ms) {
      var i = prog.firstChild; i.style.transition = 'none'; i.style.width = '0';
      void i.offsetWidth; i.style.transition = 'width ' + ms + 'ms linear'; i.style.width = '100%';
    }
    function stop() {
      on = false; token++; clearTimeout(timer); if (synth) synth.cancel();
      prog.firstChild.style.transition = 'none'; prog.firstChild.style.width = '0';
      root.classList.remove('pv-on'); if (current === api) current = null; label();
    }
    function advance(my) {
      if (my !== token) return;
      if (next.disabled) { stop(); root.dispatchEvent(new CustomEvent('pv-done', { bubbles: true })); return; }
      auto = true; next.click(); auto = false; say();
    }
    function say() {
      var my = ++token, cap = root.querySelector(k.cap), t = cap ? spoken(cap) : '', n = words(t);
      var silent = Math.max(2400, n * 290 + 1300), cap_ms = n * 520 + 4000;
      clearTimeout(timer);
      if (sound && synth && synth.getVoices().length) {
        synth.cancel();
        var u = new SpeechSynthesisUtterance(t); u.rate = 1.02; u.lang = 'en-US';
        u.onend = function () { clearTimeout(timer); timer = setTimeout(function () { advance(my); }, 450); };
        bar_(n * 400 + 600); synth.speak(u);
        timer = setTimeout(function () { advance(my); }, cap_ms);   /* a voice that never reports its end */
      } else {
        bar_(silent); timer = setTimeout(function () { advance(my); }, silent);
      }
    }
    var auto = false;
    function start() {
      if (current && current !== api) current.stop();
      current = api; on = true; root.classList.add('pv-on');
      if (next.disabled) { auto = true; while (!back.disabled) back.click(); auto = false; }
      label(); say();
    }
    play.onclick = function () { if (on) stop(); else start(); };
    voice.onclick = function () {
      sound = !sound; try { localStorage.setItem('pv-sound', sound ? '1' : '0'); } catch (e) {}
      label(); if (on) say();
    };
    [next, back].forEach(function (b) { b.addEventListener('click', function () { if (!auto && on) stop(); else if (!on) label(); }); });
    var api = { root: root, start: start, stop: stop, mute: function () { sound = false; label(); } };
    players.push(api); label();
  }

  function boot() {
    KINDS.forEach(function (k) { Array.prototype.forEach.call(document.querySelectorAll(k.root), function (r) { make(r, k); }); });
    var m = /video=(\d+)/.exec(location.hash);
    if (m && players[+m[1] - 1]) {
      var p = players[+m[1] - 1], stage = document.createElement('div');
      stage.className = 'pv-stage'; document.body.appendChild(stage); stage.appendChild(p.root);
      document.body.classList.add('pv-mode');
      p.mute(); p.root.addEventListener('pv-done', function () { window.__pvDone = true; });
      window.__pvCount = players.length;
      setTimeout(function () { window.__pvStarted = true; p.start(); }, 900);
    }
  }
  window.addEventListener('pagehide', function () { if (synth) synth.cancel(); });
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();
