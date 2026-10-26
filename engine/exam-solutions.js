/* ===== exam-solutions.js v0.1 =====
   The shell around a page of worked exam questions. Each question is a
   <section class="sol"> carrying data-term, data-exam and data-topic, grouped
   under a <div class="sol-group"> (one per term and exam) whose <h2> the house
   script lists in its table of contents. This builds three rows of buttons --
   exam, semester, topic -- into the first <div class="sol-shell">, hides every
   section the selection does not match, and keeps the selection in the URL
   hash so a link lands on one exam.

   The graphs themselves are ordinary sd-graph.js widgets; nothing here draws.
   scripts/embed_engine.py inserts this in place of the SOL-SHELL placeholder,
   which is never written out here: the script would find it twice. */
(function () {
  var SEASON = { '1': 'Spring', '2': 'Summer', '3': 'Fall' };
  function termName(code) {
    code = String(code);
    var m = /^(\d\d)([123])$/.exec(code);
    return m ? SEASON[m[2]] + ' 20' + m[1] : code;
  }
  function examName(e) { return /^\d+$/.test(e) ? 'Exam ' + e : e; }
  function examOrder(e) { return /^\d+$/.test(e) ? +e : 99; }
  function uniq(list) {
    var out = [];
    list.forEach(function (x) { if (out.indexOf(x) < 0) out.push(x); });
    return out;
  }

  document.addEventListener('DOMContentLoaded', function () {
    var mount = document.querySelector('.sol-shell');
    if (!mount) return;
    var secs = [].slice.call(document.querySelectorAll('section.sol'));
    var groups = [].slice.call(document.querySelectorAll('.sol-group'));
    if (!secs.length) return;

    var terms = uniq(secs.map(function (s) { return s.dataset.term; }))
      .sort(function (a, b) { return b.localeCompare(a); });            // newest first
    var state = { term: terms[0], exam: '', topic: '' };

    function examsFor(term) {
      return uniq(secs.filter(function (s) { return s.dataset.term === term; })
                      .map(function (s) { return s.dataset.exam; }))
        .sort(function (a, b) { return examOrder(a) - examOrder(b); });
    }
    function topicsFor(term, exam) {
      return uniq(secs.filter(function (s) { return s.dataset.term === term && s.dataset.exam === exam; })
                      .map(function (s) { return s.dataset.topic; }));
    }
    function settle() {
      var exams = examsFor(state.term);
      if (exams.indexOf(state.exam) < 0) state.exam = exams[0];
      if (state.topic && topicsFor(state.term, state.exam).indexOf(state.topic) < 0) state.topic = '';
    }

    function row(label, items, current, pick) {
      var r = document.createElement('div'); r.className = 'sol-row';
      var k = document.createElement('span'); k.className = 'sol-k'; k.textContent = label;
      var b = document.createElement('div'); b.className = 'sol-btns';
      items.forEach(function (it) {
        var btn = document.createElement('button');
        btn.type = 'button';
        btn.textContent = it.label;
        btn.setAttribute('aria-pressed', it.value === current ? 'true' : 'false');
        btn.addEventListener('click', function () { pick(it.value); });
        b.appendChild(btn);
      });
      r.appendChild(k); r.appendChild(b);
      return r;
    }

    function render() {
      settle();
      mount.innerHTML = '';
      // Exam first, then the semester it was set in, then the topic: the
      // order Ian asked for (2026-10-26). A semester's exams come from the
      // sections, so a term that only has an Exam 1 shows one exam button.
      mount.appendChild(row('Exam', examsFor(state.term).map(function (e) { return { value: e, label: examName(e) }; }),
        state.exam, function (v) { state.exam = v; state.topic = ''; render(); }));
      mount.appendChild(row('Semester', terms.map(function (t) { return { value: t, label: termName(t) }; }),
        state.term, function (v) { state.term = v; state.exam = ''; state.topic = ''; render(); }));
      var topics = [{ value: '', label: 'All topics' }].concat(
        topicsFor(state.term, state.exam).map(function (t) { return { value: t, label: t }; }));
      mount.appendChild(row('Topic', topics, state.topic, function (v) { state.topic = v; render(); }));

      var shown = 0;
      secs.forEach(function (s) {
        var on = s.dataset.term === state.term && s.dataset.exam === state.exam &&
                 (!state.topic || s.dataset.topic === state.topic);
        s.hidden = !on;
        if (on) shown++;
      });
      groups.forEach(function (g) {
        g.hidden = !g.querySelector('section.sol:not([hidden])');
      });
      var c = document.createElement('p'); c.className = 'sol-count';
      c.textContent = shown + ' question' + (shown === 1 ? '' : 's') + ' · ' +
        termName(state.term) + ', ' + examName(state.exam) + (state.topic ? ', ' + state.topic : '');
      mount.appendChild(c);

      var hash = '#' + state.term + '/' + state.exam + (state.topic ? '/' + encodeURIComponent(state.topic) : '');
      if (location.hash !== hash && history.replaceState) history.replaceState(null, '', hash);
    }

    // A link may carry a selection (#263/2/Government%20Intervention) or the
    // id of a heading or question the house table of contents points at. A
    // hidden heading would scroll nowhere, so its group is selected first.
    function fromHash() {
      var h = decodeURIComponent(location.hash.slice(1));
      if (!h) return false;
      var el = document.getElementById(h);
      if (el) {
        var sec = el.closest('section.sol') || el.closest('.sol-group');
        var src = sec && (sec.matches('section.sol') ? sec : sec.querySelector('section.sol'));
        if (src) {
          state.term = src.dataset.term; state.exam = src.dataset.exam; state.topic = '';
          render();
          el.scrollIntoView();
          return true;
        }
        return false;
      }
      var parts = h.split('/');
      if (terms.indexOf(parts[0]) < 0) return false;
      state.term = parts[0]; state.exam = parts[1] || ''; state.topic = parts[2] || '';
      render();
      return true;
    }

    if (!fromHash()) render();
    window.addEventListener('hashchange', function () { fromHash(); });
  });
})();
