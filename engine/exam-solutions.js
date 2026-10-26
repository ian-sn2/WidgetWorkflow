/* ===== exam-solutions.js v0.5 =====
   The shell around a page of worked exam questions. Each question is a
   <section class="sol"> carrying data-term, data-exam and data-topic, grouped
   under a <div class="sol-group"> (one per term and exam) whose <h2> the house
   script lists in its table of contents. This builds three collapsible boxes, styled like the house table of
   contents, into the first <div class="sol-shell">: semester, exam, topic, hides every
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

    // Three collapsible boxes, each built the way the house script builds its
    // table of contents (a <details class="toc-box"> with a bold summary and a
    // list of links): one for the semester, one for the exam, one for the
    // topic (Ian, 2026-10-26: "separate sections ... so it won't show
    // everything all at once"). Each summary names the current choice, the
    // list inside holds only that box's choices, and picking one closes it.
    var boxes = {};
    ['Semester', 'Exam', 'Topic'].forEach(function (name) {
      var box = document.createElement('details'); box.className = 'toc-box sol-box';
      var summary = document.createElement('summary'); box.appendChild(summary);
      var nav = document.createElement('nav'); box.appendChild(nav);
      mount.appendChild(box);
      boxes[name] = { box: box, summary: summary, nav: nav };
    });
    var count = document.createElement('p'); count.className = 'sol-count'; mount.appendChild(count);

    function fill(name, current, items, pick) {
      var b = boxes[name];
      b.summary.innerHTML = '';
      var st = document.createElement('strong');
      st.textContent = '\ud83d\udcd8 ' + name + ': ' + current;
      b.summary.appendChild(st);
      b.nav.innerHTML = '';
      var ul = document.createElement('ul'); ul.style.lineHeight = '1.8';
      items.forEach(function (it) {
        var li = document.createElement('li'), a = document.createElement('a');
        a.href = '#'; a.textContent = it.label;
        if (it.current) { li.className = 'sol-current'; a.setAttribute('aria-current', 'true'); }
        a.addEventListener('click', function (e) { e.preventDefault(); b.box.open = false; pick(it.value); });
        li.appendChild(a); ul.appendChild(li);
      });
      b.nav.appendChild(ul);
    }

    function render() {
      settle();
      fill('Semester', termName(state.term),
        terms.map(function (t) { return { value: t, label: termName(t), current: t === state.term }; }),
        function (v) { state.term = v; state.exam = ''; state.topic = ''; render(); });
      fill('Exam', examName(state.exam),
        examsFor(state.term).map(function (e) { return { value: e, label: examName(e), current: e === state.exam }; }),
        function (v) { state.exam = v; state.topic = ''; render(); });
      fill('Topic', state.topic || 'All topics',
        [{ value: '', label: 'All topics', current: !state.topic }].concat(
          topicsFor(state.term, state.exam).map(function (t) { return { value: t, label: t, current: t === state.topic }; })),
        function (v) { state.topic = v; render(); });

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
      count.textContent = shown + ' question' + (shown === 1 ? '' : 's') + ' \u00b7 ' +
        termName(state.term) + ', ' + examName(state.exam) + (state.topic ? ', ' + state.topic : '');

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

    // Quiz behaviour (Ian, 2026-10-26): a choice is clicked, it turns green
    // or red, the right one is shown, and the solution stays behind its own
    // click. data-answer holds the letter(s) the solution gives -- "a d" where
    // the key accepts either -- so a section with none is left as plain text.
    secs.forEach(function (sec) {
      var ok = (sec.dataset.answer || '').split(/\s+/).filter(Boolean);
      var items = [].slice.call(sec.querySelectorAll('ol.sol-choices > li'));
      if (!ok.length || !items.length) return;
      var done = false;
      items.forEach(function (li, i) {
        var letter = 'abcde'.charAt(i);
        li.tabIndex = 0; li.setAttribute('role', 'button');
        function pick() {
          if (done) return; done = true;
          var right = ok.indexOf(letter) >= 0;
          sec.classList.add('sol-answered');
          items.forEach(function (it, j) {
            it.tabIndex = -1;
            if (ok.indexOf('abcde'.charAt(j)) >= 0) it.classList.add('sol-right');
          });
          if (!right) li.classList.add('sol-wrong');
          var note = document.createElement('p'); note.className = 'sol-verdict ' + (right ? 'is-right' : 'is-wrong');
          note.textContent = right ? 'Correct.' : 'Not quite. The answer is (' + ok.join(' or ') + ').';
          var det = sec.querySelector('details.sol-answer');
          sec.insertBefore(note, det);
        }
        li.addEventListener('click', pick);
        li.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); pick(); } });
      });
    });
    window.addEventListener('hashchange', function () { fromHash(); });
  });
})();
