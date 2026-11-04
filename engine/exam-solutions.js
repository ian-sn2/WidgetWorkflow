/* ===== exam-solutions.js v0.31 =====
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

    // A bookmark button at the left of each question's heading, boxed like
    // the strip's numbers (Ian, 2026-10-27; a ribbon rather than a star, this
    // being a study guide). A bookmarked number in the strip wears the ribbon
    // draped over its top edge, so a student can find the question again. Bookmarks are kept in this browser's localStorage, a
    // per-viewer convenience, and the page works without it.
    var STAR_KEY = 'sol-stars:' + location.pathname;
    var stars = {};
    try { stars = JSON.parse(localStorage.getItem(STAR_KEY) || '{}') || {}; } catch (e) { stars = {}; }
    function saveStars() { try { localStorage.setItem(STAR_KEY, JSON.stringify(stars)); } catch (e) {} }
    secs.forEach(function (sec) {
      var q = sec.querySelector('.sol-q'); if (!q) return;
      var btn = document.createElement('button'); btn.type = 'button'; btn.className = 'sol-star';
      btn.innerHTML = '<svg viewBox="0 0 16 20" width="13" height="17" aria-hidden="true"><path d="M3 1.5h10a1 1 0 0 1 1 1V18l-6-4-6 4V2.5a1 1 0 0 1 1-1z"/></svg>';
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
      q.insertBefore(btn, q.firstChild);
    });

    // Questions a reader has opened are remembered in this browser, so the
    // menu can say how much of a semester or topic has been reviewed (Ian,
    // 2026-11-04). A question counts as reviewed once it has been shown.
    var SEEN_KEY = 'sol-seen:' + location.pathname;
    var seen = {};
    try { seen = JSON.parse(localStorage.getItem(SEEN_KEY) || '{}') || {}; } catch (e) { seen = {}; }
    function saveSeen() { try { localStorage.setItem(SEEN_KEY, JSON.stringify(seen)); } catch (e) {} }
    function seenCount(term, exam, topic) {
      return secs.filter(function (s) {
        return (!term || s.dataset.term === term) && (!exam || s.dataset.exam === exam) && (!topic || s.dataset.topic === topic) && seen[s.id];
      }).length;
    }

    var terms = uniq(secs.map(function (s) { return s.dataset.term; }))
      .sort(function (a, b) { return b.localeCompare(a); });            // newest first
    // Nothing is chosen until it is clicked (Ian, 2026-11-04): the menu
    // opens with no card lit, the exam row appears once a semester is picked
    // and the topic row once an exam is. A deep link fills the selection in.
    var state = { term: '', exam: '', topic: '', idx: 0, view: 'menu' };

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
      if (state.view === 'menu') return;          // the menu fills in by clicks only
      if (terms.indexOf(state.term) < 0) state.term = terms[0];
      var exams = examsFor(state.term);
      if (exams.indexOf(state.exam) < 0) state.exam = exams[0];
      if (state.topic && topicsFor(state.term, state.exam).indexOf(state.topic) < 0) state.topic = '';
    }

    // The picker is a panel of buttons, always open (Ian, 2026-11-04: "make
    // it more interactive ... buttons of which exams to go to"): three rows
    // of cards -- semester, exam, topic -- each card naming its choice and
    // how many questions it holds, the chosen one filled navy. Under it a
    // status line names the selection and a bar shows how far along the
    // reader is.
    // Two views (Ian, 2026-11-04): the menu -- a greeting and the card panel,
    // which is the page as it opens -- and the questions, where the panel is
    // gone and a bar at the top carries "Back to menu", the selection and
    // the progress. Picking a topic card is what starts the questions.
    var menu = document.createElement('div'); menu.className = 'sol-menu';
    var hello = document.createElement('p'); hello.className = 'sol-hello';
    hello.textContent = 'Hello! Select which semester, exam, and topics you would like to practice.';
    var picker = document.createElement('div'); picker.className = 'sol-picker';
    menu.appendChild(hello); menu.appendChild(picker);
    mount.appendChild(menu);
    var top = document.createElement('div'); top.className = 'sol-top';
    var back = document.createElement('button'); back.type = 'button'; back.className = 'sol-back'; back.textContent = '\u2039 Back to menu';
    function toMenu() { state.view = 'menu'; state.term = ''; state.exam = ''; state.topic = ''; state.topicChosen = false; state.idx = 0; render(); window.scrollTo(0, 0); }
    // (render() puts the one exam back when the page has only one.)
    back.addEventListener('click', toMenu);
    var status = document.createElement('div'); status.className = 'sol-status';
    var statusText = document.createElement('div'); statusText.className = 'sol-status-text';
    var progress = document.createElement('div'); progress.className = 'sol-progress';
    var progressBar = document.createElement('div'); progressBar.className = 'sol-progress-bar';
    progress.appendChild(progressBar); status.appendChild(statusText); status.appendChild(progress);
    // Previous and Next flank the question count at the bar's right, and the
    // strip of question numbers runs along the bar's second row, so nothing
    // sits under the question box (Ian, 2026-11-04).
    var pager = document.createElement('div'); pager.className = 'sol-pager';
    var prev = document.createElement('button'); prev.type = 'button'; prev.className = 'sol-prev'; prev.textContent = '\u2039 Prev';
    var count = document.createElement('span'); count.className = 'sol-status-n';
    var next = document.createElement('button'); next.type = 'button'; next.className = 'sol-next'; next.textContent = 'Next \u203a';
    pager.appendChild(prev); pager.appendChild(count); pager.appendChild(next);
    var strip = document.createElement('div'); strip.className = 'sol-strip';
    top.appendChild(back); top.appendChild(status); top.appendChild(pager); top.appendChild(strip);
    mount.appendChild(top);

    function countFor(term, exam, topic) {
      return secs.filter(function (s) {
        return (!term || s.dataset.term === term) && (!exam || s.dataset.exam === exam) && (!topic || s.dataset.topic === topic);
      }).length;
    }
    function allExams() {
      return uniq(secs.map(function (s) { return s.dataset.exam; })).sort(function (a, b) { return examOrder(a) - examOrder(b); });
    }
    function allTopics(term, exam) {
      return uniq(secs.filter(function (s) { return (!term || s.dataset.term === term) && (!exam || s.dataset.exam === exam); })
                      .map(function (s) { return s.dataset.topic; }))
        .sort(function (a, b) { return (topicRank(a) - topicRank(b)) || a.localeCompare(b); });
    }
    function stage(name, hint, items, pick) {
      var d = document.createElement('div'); d.className = 'sol-stage';
      var h = document.createElement('div'); h.className = 'sol-stage-k';
      h.innerHTML = '<span>' + name + '</span>' + (hint ? '<small>' + hint + '</small>' : '');
      d.appendChild(h);
      var row = document.createElement('div'); row.className = 'sol-cards';
      items.forEach(function (it) {
        var btn = document.createElement('button'); btn.type = 'button'; btn.className = 'sol-card';
        btn.setAttribute('aria-pressed', it.current ? 'true' : 'false');
        var pct = it.count ? Math.round(100 * (it.seen || 0) / it.count) : 0;
        btn.innerHTML = '<span class="sol-card-l">' + it.label + '</span>' +
          (it.count != null ? '<span class="sol-card-n">' + it.count + ' question' + (it.count === 1 ? '' : 's') +
            (it.seen ? ' \u00b7 ' + pct + '% reviewed' : '') + '</span>' +
            '<span class="sol-card-bar"><span style="width:' + pct + '%"></span></span>' : '');
        if (it.seen && it.seen === it.count) btn.classList.add('is-done');
        btn.addEventListener('click', function () { pick(it.value); });
        row.appendChild(btn);
      });
      d.appendChild(row);
      return d;
    }


    // The strip of question numbers (Ian, 2026-10-27): the current one
    // filled, a bookmarked one wearing the ribbon, a reviewed one tinted.
    // On the first question Previous has nothing to go to and is not drawn;
    // on the last, Next becomes Finish and returns to the menu, where the
    // cards show what has been reviewed (Ian, 2026-11-04).
    var lastIdx = 0;
    function forward() { if (state.idx >= lastIdx) toMenu(); else { state.idx++; render(); } }
    prev.addEventListener('click', function () { if (state.idx > 0) { state.idx--; render(); } });
    next.addEventListener('click', forward);
    document.addEventListener('keydown', function (e) {
      if (e.target && /^(INPUT|TEXTAREA|SELECT)$/.test(e.target.tagName)) return;
      if (state.view !== 'questions') return;
      if (e.key === 'ArrowRight') forward();
      if (e.key === 'ArrowLeft' && state.idx > 0) { state.idx--; render(); }
    });

    // The questions open once a semester, an exam and a topic are all chosen,
    // in whatever order; a choice that leaves one missing just lights up.
    function maybeStart() {
      if (state.term && state.exam && state.topicChosen) { state.view = 'questions'; render(); window.scrollTo(0, 0); }
      else render();
    }

    function render() {
      settle();
      picker.innerHTML = '';
      var T = state.term, E = state.exam;
      picker.appendChild(stage('Semester', '',
        terms.map(function (t) { return { value: t, label: termName(t), count: countFor(t, E, state.topic), seen: seenCount(t, E, state.topic), current: t === state.term }; }),
        function (v) { state.term = v; state.idx = 0; maybeStart(); }));
      // One page per exam is the plan (Ian's boss, 2026-11-04), so a page
      // carrying a single exam has it chosen already and shows no row for it.
      var exams = allExams();
      if (exams.length === 1 && !state.exam) state.exam = exams[0];
      if (exams.length > 1) picker.appendChild(stage('Exam', '',
        exams.map(function (e) { return { value: e, label: examName(e), count: countFor(T, e, state.topic), seen: seenCount(T, e, state.topic), current: e === state.exam }; }),
        function (v) { state.exam = v; state.idx = 0; maybeStart(); }));
      picker.appendChild(stage('Topic', '',
        [{ value: '', label: 'Full Exam', count: countFor(T, E, ''), seen: seenCount(T, E, ''), current: !!state.topicChosen && !state.topic }].concat(
          allTopics(T, E).map(function (t) { return { value: t, label: t, count: countFor(T, E, t), seen: seenCount(T, E, t), current: t === state.topic }; })),
        function (v) { state.topic = v; state.topicChosen = true; state.idx = 0; maybeStart(); }));

      var inMenu = state.view === 'menu';
      menu.hidden = !inMenu; top.hidden = inMenu;
      var list = secs.filter(function (s) {
        return state.term && state.exam && s.dataset.term === state.term && s.dataset.exam === state.exam &&
               (!state.topic || s.dataset.topic === state.topic);
      });
      if (state.idx >= list.length) state.idx = Math.max(0, list.length - 1);
      if (!inMenu && list[state.idx] && !seen[list[state.idx].id]) { seen[list[state.idx].id] = 1; saveSeen(); }
      secs.forEach(function (s) {
        var show = !inMenu && s === list[state.idx];
        if (show && s.hidden) { s.classList.remove('sol-in'); void s.offsetWidth; s.classList.add('sol-in'); }
        s.hidden = !show;
      });
      statusText.innerHTML = '<strong>' + termName(state.term) + '</strong> \u00b7 ' + examName(state.exam) + ' \u00b7 ' + (state.topic || 'Full Exam');
      count.textContent = list.length ? 'Question ' + (state.idx + 1) + ' of ' + list.length : '';
      progressBar.style.width = list.length ? (100 * (state.idx + 1) / list.length).toFixed(1) + '%' : '0%';
      groups.forEach(function (g) { g.hidden = !g.querySelector('section.sol:not([hidden])'); });
      // the box for the question goes under the picker, the nav under it
      if (list[state.idx]) mount.appendChild(list[state.idx]);
      strip.innerHTML = '';
      // Each button carries the question's own number (from its id, ...-q24),
      // not its position in the selection: under a topic filter the ninth
      // question shown may be question 24 (Ian, 2026-10-27).
      list.forEach(function (sec, i) {
        var m = /-q(\d+)$/.exec(sec.id);
        var btn = document.createElement('button'); btn.type = 'button'; btn.textContent = m ? m[1] : String(i + 1);
        btn.className = 'sol-num' + (stars[sec.id] ? ' is-starred' : '') + (seen[sec.id] ? ' is-seen' : '');
        btn.setAttribute('aria-pressed', i === state.idx ? 'true' : 'false');
        btn.setAttribute('aria-label', 'Question ' + btn.textContent);
        btn.addEventListener('click', function () { state.idx = i; render(); });
        strip.appendChild(btn);
      });
      lastIdx = list.length - 1;
      prev.classList.toggle('is-off', state.idx <= 0);
      var atEnd = state.idx >= lastIdx;
      next.textContent = atEnd ? 'Finish \u2713' : 'Next \u203a';
      next.classList.toggle('sol-finish', atEnd);

      var hash = inMenu ? '#' : '#' + state.term + '/' + state.exam + '/' + encodeURIComponent(state.topic || '') + '/' + (state.idx + 1);
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
          state.view = 'questions'; state.topicChosen = true;
          render();
          return true;
        }
        return false;
      }
      var parts = h.split('/');
      if (terms.indexOf(parts[0]) < 0) return false;
      state.view = 'questions'; state.topicChosen = true;
      state.term = parts[0]; state.exam = parts[1] || ''; state.topic = parts[2] || '';
      state.idx = Math.max(0, (parseInt(parts[3], 10) || 1) - 1);
      render();
      return true;
    }

    if (!fromHash()) render();

    // No quiz: this is a list of worked solutions, the right choice marked
    // and the solution in the open (Ian's manager, 2026-11-02).

    // Widgets inside a solution are drawn small and without their box, to
    // save vertical space, and each carries a Fullscreen button that lifts
    // it into an overlay at full size (Ian, 2026-11-04). The widget's own
    // node is moved, so its step and scenario state come with it.
    var fsOverlay = null, fsHome = null, fsWidget = null;
    function closeFs() {
      if (!fsOverlay) return;
      fsHome.parentNode.insertBefore(fsWidget, fsHome); fsHome.remove();
      fsOverlay.remove(); fsOverlay = fsHome = fsWidget = null;
      document.body.classList.remove('sol-fs-open');
    }
    function openFs(w) {
      closeFs();
      fsWidget = w; fsHome = document.createElement('div'); fsHome.className = 'sol-fs-home';
      w.parentNode.insertBefore(fsHome, w);
      fsOverlay = document.createElement('div'); fsOverlay.className = 'sol-fs';
      var panel = document.createElement('div'); panel.className = 'sol-fs-panel';
      var close = document.createElement('button'); close.type = 'button'; close.className = 'sol-fs-close'; close.textContent = '\u2715 Close';
      close.addEventListener('click', closeFs);
      panel.appendChild(close); panel.appendChild(w); fsOverlay.appendChild(panel);
      fsOverlay.addEventListener('click', function (e) { if (e.target === fsOverlay) closeFs(); });
      document.body.appendChild(fsOverlay); document.body.classList.add('sol-fs-open');
      close.focus();
    }
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeFs(); });
    // A - / + pair steps the figure size (Ian, 2026-11-04); the choice is
    // kept in this browser and applies to every figure on the page.
    // The middle of five sizes by default, two steps either way (Ian,
    // 2026-11-04).
    // Sizes are shares of the solution box's width (Ian, 2026-11-04): the
    // fifth fills it, the fourth is 75% of it, the third -- the default -- is
    // half, then 37.5% and 25%. A share, not a pixel count, so the same
    // setting looks the same on every screen. The stored key changed with the
    // default: a size pressed under an earlier build stayed in the browser.
    var SIZES = [25, 37.5, 50, 75, 100], SIZE_KEY = 'sol-size-3';
    var sizeIdx = 2;
    try { var sv = parseInt(localStorage.getItem(SIZE_KEY), 10); if (sv >= 0 && sv < SIZES.length) sizeIdx = sv; } catch (e) {}
    var allWidgets = [].slice.call(document.querySelectorAll('section.sol .sdg'));
    function applySize() {
      allWidgets.forEach(function (w) {
        w.style.setProperty('--fig', SIZES[sizeIdx] + '%');
        var ctl = w.querySelector('.sol-size');
        if (ctl) { ctl.querySelector('.sol-minus').disabled = sizeIdx === 0; ctl.querySelector('.sol-plus').disabled = sizeIdx === SIZES.length - 1; }
      });
    }
    // only a press is remembered, never the default
    function stepSize(d) { sizeIdx = Math.max(0, Math.min(SIZES.length - 1, sizeIdx + d)); applySize(); try { localStorage.setItem(SIZE_KEY, String(sizeIdx)); } catch (e) {} }
    // The widget's own step controls (Back, Next step, Start over and the
    // counter) are docked into the same strip as the size buttons, as arrow
    // and restart icons, so nothing sits under the plot (Ian, 2026-11-04).
    // The engine rebuilds a widget when its scenario changes, which makes a
    // fresh control row, so an observer docks it again each time.
    function dock(w) {
      // the engine's rebuild empties the widget, strip included: put it back
      var tools = w.solTools;
      if (tools.parentNode !== w) w.insertBefore(tools, w.firstChild);
      // the engine's new row is the one to dock; a row left in the strip by
      // an earlier build is stale and goes
      var rows = [].slice.call(w.querySelectorAll('.sdg-ctrl'));
      var fresh = rows.filter(function (r) { return r.parentNode !== tools; })[0];
      if (!fresh) return;
      rows.forEach(function (r) { if (r !== fresh && r.parentNode === tools) r.remove(); });
      tools.insertBefore(fresh, tools.firstChild);
    }
    allWidgets.forEach(function (w) {
      var ctl = document.createElement('div'); ctl.className = 'sol-tools';
      var minus = document.createElement('button'); minus.type = 'button'; minus.className = 'sol-minus'; minus.textContent = '\u2212'; minus.title = 'Smaller'; minus.setAttribute('aria-label', 'Smaller figure');
      var plus = document.createElement('button'); plus.type = 'button'; plus.className = 'sol-plus'; plus.textContent = '+'; plus.title = 'Larger'; plus.setAttribute('aria-label', 'Larger figure');
      var btn = document.createElement('button'); btn.type = 'button'; btn.className = 'sol-fs-btn';
      btn.innerHTML = '<svg viewBox="0 0 16 16" width="12" height="12" aria-hidden="true"><path d="M2 6V2h4M14 6V2h-4M2 10v4h4M14 10v4h-4" fill="none" stroke="currentColor" stroke-width="1.8"/></svg> Fullscreen';
      minus.addEventListener('click', function () { stepSize(-1); });
      plus.addEventListener('click', function () { stepSize(1); });
      btn.addEventListener('click', function () { openFs(w); });
      var size = document.createElement('div'); size.className = 'sol-size';
      size.appendChild(minus); size.appendChild(plus); size.appendChild(btn);
      ctl.appendChild(size);
      w.solTools = ctl;
      dock(w);
      new MutationObserver(function () { dock(w); }).observe(w, { childList: true, subtree: true });
    });
    applySize();
    // leaving the question closes an overlay with it
    prev.addEventListener('click', closeFs); next.addEventListener('click', closeFs); back.addEventListener('click', closeFs);
    window.addEventListener('hashchange', function () { fromHash(); });
  });
})();
