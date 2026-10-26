/* ===== exam-solutions.js v0.3 =====
   The shell around a page of worked exam questions. Each question is a
   <section class="sol"> carrying data-term, data-exam and data-topic, grouped
   under a <div class="sol-group"> (one per term and exam) whose <h2> the house
   script lists in its table of contents. This builds a collapsible picker, styled like the house table of
   contents, into the first <div class="sol-shell">: exams, then semesters,
   then the chosen semester's topics, hides every
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

    // The picker is a collapsible box built the way the house script builds
    // its table of contents (Ian, 2026-10-26: "kind of like how our toc does
    // it"): a <details class="toc-box"> whose summary names what is showing,
    // holding a nested list -- exams, then semesters, then the chosen
    // semester's topics -- each entry a link that sets the selection.
    var box = document.createElement('details'); box.className = 'toc-box sol-box';
    var summary = document.createElement('summary'); box.appendChild(summary);
    var nav = document.createElement('nav'); box.appendChild(nav);
    mount.appendChild(box);

    function link(text, on, current) {
      var li = document.createElement('li'), a = document.createElement('a');
      a.href = '#'; a.textContent = text;
      if (current) { li.className = 'sol-current'; a.setAttribute('aria-current', 'true'); }
      a.addEventListener('click', function (e) { e.preventDefault(); on(); });
      li.appendChild(a);
      return li;
    }

    function render() {
      settle();
      summary.innerHTML = '';
      var st = document.createElement('strong');
      st.textContent = '\ud83d\udcd8 ' + examName(state.exam) + ' \u00b7 ' + termName(state.term) + ' \u00b7 ' + (state.topic || 'All topics');
      summary.appendChild(st);

      nav.innerHTML = '';
      var ul = document.createElement('ul'); ul.style.lineHeight = '1.8';
      var exams = uniq(secs.map(function (s) { return s.dataset.exam; }))
        .sort(function (a, b) { return examOrder(a) - examOrder(b); });
      exams.forEach(function (e) {
        var termsFor = terms.filter(function (t) { return examsFor(t).indexOf(e) >= 0; });
        var li = link(examName(e), function () {
          state.exam = e; if (termsFor.indexOf(state.term) < 0) state.term = termsFor[0]; state.topic = ''; render();
        }, e === state.exam);
        li.firstChild.style.fontWeight = 'bold';
        var sub = document.createElement('ul');
        termsFor.forEach(function (t) {
          var tli = link(termName(t), function () { state.term = t; state.exam = e; state.topic = ''; render(); },
                         e === state.exam && t === state.term);
          if (e === state.exam && t === state.term) {
            var tul = document.createElement('ul');
            tul.appendChild(link('All topics', function () { state.topic = ''; render(); }, !state.topic));
            topicsFor(t, e).forEach(function (tp) {
              tul.appendChild(link(tp, function () { state.topic = tp; render(); }, state.topic === tp));
            });
            tli.appendChild(tul);
          }
          sub.appendChild(tli);
        });
        li.appendChild(sub);
        ul.appendChild(li);
      });
      nav.appendChild(ul);

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
      var old = nav.querySelector('.sol-count'); if (old) old.remove();
      var c = document.createElement('p'); c.className = 'sol-count';
      c.textContent = shown + ' question' + (shown === 1 ? '' : 's') + ' · ' +
        termName(state.term) + ', ' + examName(state.exam) + (state.topic ? ', ' + state.topic : '');
      nav.appendChild(c);

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
