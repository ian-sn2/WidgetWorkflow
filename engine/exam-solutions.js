/* ===== exam-solutions.js v0.11 =====
   The shell around a page of worked exam questions. Each question is a
   <section class="sol"> carrying data-term, data-exam and data-topic, grouped
   under a <div class="sol-group"> (one per term and exam) whose <h2> the house
   script lists in its table of contents. This builds one collapsible box, styled like the house table of
   contents, into the first <div class="sol-shell">, with three stages in
   order -- semester, exam, topic -- hides every
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
  // Ian's order for the topics (2026-10-26); the frontier comes first because
  // it is the course's first chapter. Anything else sorts after, by name.
  var TOPIC_ORDER = ['The PPF', 'Supply and Demand', 'Elasticity', 'Efficiency and Equity', 'Government Intervention', 'International Trade'];
  function topicRank(t) { var i = TOPIC_ORDER.indexOf(t); return i < 0 ? TOPIC_ORDER.length : i; }
  function uniq(list) {
    var out = [];
    list.forEach(function (x) { if (out.indexOf(x) < 0) out.push(x); });
    return out;
  }

  document.addEventListener('DOMContentLoaded', function () {
    var mount = document.querySelector('.sol-shell');
    if (!mount) return;
    // The house script builds its own table of contents at the top of every
    // page, listing the h2 under each semester. On a solutions page the
    // picker below is the table of contents, so the house one goes (Ian,
    // 2026-10-26: "we don't need the top toc"). Its listener ran first, so
    // the box is there to remove.
    document.querySelectorAll('details.toc-box:not(.sol-box)').forEach(function (t) { t.remove(); });
    var secs = [].slice.call(document.querySelectorAll('section.sol'));
    var groups = [].slice.call(document.querySelectorAll('.sol-group'));
    if (!secs.length) return;

    // A bookmark ribbon drapes over the top edge of the question's box
    // (Ian, 2026-10-27; a ribbon rather than a star, this being a study
    // guide, and over the box rather than beside the heading): the number in
    // the strip carries the same ribbon, so a student can find it again. Bookmarks are kept in this browser's localStorage, a
    // per-viewer convenience, and the page works without it.
    var STAR_KEY = 'sol-stars:' + location.pathname;
    var stars = {};
    try { stars = JSON.parse(localStorage.getItem(STAR_KEY) || '{}') || {}; } catch (e) { stars = {}; }
    function saveStars() { try { localStorage.setItem(STAR_KEY, JSON.stringify(stars)); } catch (e) {} }
    secs.forEach(function (sec) {
      var q = sec.querySelector('.sol-q'); if (!q) return;
      var btn = document.createElement('button'); btn.type = 'button'; btn.className = 'sol-star';
      btn.innerHTML = '<svg viewBox="0 0 16 22" width="18" height="26" aria-hidden="true"><path d="M1 0h14v21l-7-5-7 5z"/></svg>';
      function paint() {
        var on = !!stars[sec.id];
        btn.setAttribute('aria-pressed', on ? 'true' : 'false');
        btn.title = on ? 'Remove bookmark' : 'Bookmark this question';
        sec.classList.toggle('sol-starred', on);
      }
      btn.addEventListener('click', function () {
        if (stars[sec.id]) delete stars[sec.id]; else stars[sec.id] = 1;
        saveStars(); paint(); render();
      });
      paint();
      sec.appendChild(btn);
    });

    var terms = uniq(secs.map(function (s) { return s.dataset.term; }))
      .sort(function (a, b) { return b.localeCompare(a); });            // newest first
    var state = { term: terms[0], exam: '', topic: '', idx: 0 };

    function examsFor(term) {
      return uniq(secs.filter(function (s) { return s.dataset.term === term; })
                      .map(function (s) { return s.dataset.exam; }))
        .sort(function (a, b) { return examOrder(a) - examOrder(b); });
    }
    function topicsFor(term, exam) {
      return uniq(secs.filter(function (s) { return s.dataset.term === term && s.dataset.exam === exam; })
                      .map(function (s) { return s.dataset.topic; }))
        .sort(function (a, b) { return (topicRank(a) - topicRank(b)) || a.localeCompare(b); });
    }
    function settle() {
      var exams = examsFor(state.term);
      if (exams.indexOf(state.exam) < 0) state.exam = exams[0];
      if (state.topic && topicsFor(state.term, state.exam).indexOf(state.topic) < 0) state.topic = '';
    }

    // One collapsible box, built the way the house script builds its table of
    // contents (a <details class="toc-box"> with a bold summary), holding three
    // stages in order: semester, then exam, then topic (Ian, 2026-10-26: "1
    // toc, and then you select the semester, which then makes you select an
    // exam, and then topics"). A later stage lists only what the earlier
    // choices allow, and the summary names the whole selection.
    var box = document.createElement('details'); box.className = 'toc-box sol-box';
    var summary = document.createElement('summary'); box.appendChild(summary);
    var nav = document.createElement('nav'); box.appendChild(nav);
    mount.appendChild(box);
    // One question at a time (Ian, 2026-10-26: "a self-contained box ... that
    // would not require any scrolling"): the picker, then the current
    // question in its own box, then Previous / Next. The page holds every
    // section; the shell shows one.
    var bar = document.createElement('div'); bar.className = 'sol-nav';
    var prev = document.createElement('button'); prev.type = 'button'; prev.textContent = '\u2039 Previous';
    // A strip of question numbers under the box (Ian, 2026-10-27), the
    // current one filled, an answered one edged green or red. Previous and
    // Next sit at its ends.
    var strip = document.createElement('div'); strip.className = 'sol-strip';
    var next = document.createElement('button'); next.type = 'button'; next.textContent = 'Next \u203a';
    bar.appendChild(prev); bar.appendChild(strip); bar.appendChild(next);
    prev.addEventListener('click', function () { if (state.idx > 0) { state.idx--; render(); } });
    next.addEventListener('click', function () { state.idx++; render(); });
    document.addEventListener('keydown', function (e) {
      if (e.target && /^(INPUT|TEXTAREA|SELECT)$/.test(e.target.tagName)) return;
      if (e.key === 'ArrowRight') { state.idx++; render(); }
      if (e.key === 'ArrowLeft' && state.idx > 0) { state.idx--; render(); }
    });

    function stage(n, name, items, pick) {
      var d = document.createElement('div'); d.className = 'sol-stage';
      var h = document.createElement('p'); h.className = 'sol-stage-k';
      h.textContent = n + '. ' + name; d.appendChild(h);
      var ul = document.createElement('ul');
      items.forEach(function (it) {
        var li = document.createElement('li'), a = document.createElement('a');
        a.href = '#'; a.textContent = it.label;
        if (it.current) { li.className = 'sol-current'; a.setAttribute('aria-current', 'true'); }
        a.addEventListener('click', function (e) { e.preventDefault(); pick(it.value); });
        li.appendChild(a); ul.appendChild(li);
      });
      d.appendChild(ul);
      return d;
    }

    function render() {
      settle();
      summary.innerHTML = '';
      var st = document.createElement('strong');
      st.textContent = '\ud83d\udcd8 ' + termName(state.term) + ' \u00b7 ' + examName(state.exam) + ' \u00b7 ' + (state.topic || 'All topics');
      summary.appendChild(st);
      nav.innerHTML = '';
      nav.appendChild(stage(1, 'Semester',
        terms.map(function (t) { return { value: t, label: termName(t), current: t === state.term }; }),
        function (v) { state.term = v; state.exam = ''; state.topic = ''; state.idx = 0; render(); }));
      nav.appendChild(stage(2, 'Exam',
        examsFor(state.term).map(function (e) { return { value: e, label: examName(e), current: e === state.exam }; }),
        function (v) { state.exam = v; state.topic = ''; state.idx = 0; render(); }));
      nav.appendChild(stage(3, 'Topic',
        [{ value: '', label: 'All topics', current: !state.topic }].concat(
          topicsFor(state.term, state.exam).map(function (t) { return { value: t, label: t, current: t === state.topic }; })),
        function (v) { state.topic = v; state.idx = 0; render(); }));

      var list = secs.filter(function (s) {
        return s.dataset.term === state.term && s.dataset.exam === state.exam &&
               (!state.topic || s.dataset.topic === state.topic);
      });
      if (state.idx >= list.length) state.idx = Math.max(0, list.length - 1);
      secs.forEach(function (s) { s.hidden = s !== list[state.idx]; });
      groups.forEach(function (g) { g.hidden = !g.querySelector('section.sol:not([hidden])'); });
      // the box for the question goes under the picker, the nav under it
      if (list[state.idx]) mount.appendChild(list[state.idx]);
      mount.appendChild(bar);
      strip.innerHTML = '';
      list.forEach(function (sec, i) {
        var btn = document.createElement('button'); btn.type = 'button'; btn.textContent = String(i + 1);
        btn.className = 'sol-num' + (sec.dataset.result ? ' is-' + sec.dataset.result : '') + (stars[sec.id] ? ' is-starred' : '');
        btn.setAttribute('aria-pressed', i === state.idx ? 'true' : 'false');
        btn.setAttribute('aria-label', 'Question ' + (i + 1));
        btn.addEventListener('click', function () { state.idx = i; render(); });
        strip.appendChild(btn);
      });
      prev.disabled = state.idx <= 0; next.disabled = state.idx >= list.length - 1;

      var hash = '#' + state.term + '/' + state.exam + '/' + encodeURIComponent(state.topic || '') + '/' + (state.idx + 1);
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
          state.idx = secs.filter(function (s) { return s.dataset.term === state.term && s.dataset.exam === state.exam; }).indexOf(src);
          render();
          return true;
        }
        return false;
      }
      var parts = h.split('/');
      if (terms.indexOf(parts[0]) < 0) return false;
      state.term = parts[0]; state.exam = parts[1] || ''; state.topic = parts[2] || '';
      state.idx = Math.max(0, (parseInt(parts[3], 10) || 1) - 1);
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
          sec.dataset.result = right ? 'right' : 'wrong';
          var me = strip.querySelector('[aria-pressed="true"]');
          if (me) me.classList.add('is-' + sec.dataset.result);
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
