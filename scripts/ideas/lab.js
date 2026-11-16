  /* ---------- what-if lab: tap an activity to delay it or crash it, and the whole network is re-solved ----------
     Lives inside the page's own widget engine (it uses network(), views(), key()), as one more widget kind.
     M.mode "delay": each tap adds a week to the activity. M.mode "crash": each tap takes a week off, down to
     the activity's crash time, at its crash cost per week. Every number shown is computed from the durations
     by the forward and backward pass. */
  W.lab = function (body, M) {
    var net = M.net, ids = Object.keys(net.nodes), crash = M.mode === 'crash', delta = {}, hist = [], fig = H('div', 'pm-figwrap');
    ids.forEach(function (id) { delta[id] = 0; });
    function solve(dl) {
      var d = {}, es = {}, ef = {}, ls = {}, lf = {}, T = 0, changed = true, guard = 0;
      ids.forEach(function (id) { d[id] = net.nodes[id].d + (crash ? -dl[id] : dl[id]); es[id] = 0; ef[id] = d[id]; });
      while (changed && guard++ < 50) {
        changed = false;
        net.edges.forEach(function (e) { if (ef[e[0]] > es[e[1]]) { es[e[1]] = ef[e[0]]; ef[e[1]] = es[e[1]] + d[e[1]]; changed = true; } });
      }
      ids.forEach(function (id) { T = Math.max(T, ef[id]); });
      ids.forEach(function (id) { lf[id] = T; ls[id] = T - d[id]; });
      changed = true; guard = 0;
      while (changed && guard++ < 50) {
        changed = false;
        net.edges.forEach(function (e) { if (ls[e[1]] < lf[e[0]]) { lf[e[0]] = ls[e[1]]; ls[e[0]] = lf[e[0]] - d[e[0]]; changed = true; } });
      }
      var slack = {}, vals = {}, crit = {}, ce = {}, paths = [];
      ids.forEach(function (id) { vals[id] = [es[id], ef[id], ls[id], lf[id]]; if (id !== 'Start') slack[id] = ls[id] - es[id]; crit[id] = ls[id] === es[id]; });
      net.edges.forEach(function (e) { if (crit[e[0]] && crit[e[1]] && ef[e[0]] === es[e[1]]) ce[e[0] + '>' + e[1]] = 'crit'; });
      (function walk(id, sofar) {
        var outs = net.edges.filter(function (e) { return e[0] === id && ce[e[0] + '>' + e[1]]; });
        if (!outs.length) { if (ef[id] === T && sofar.length) paths.push(sofar.join(' → ')); return; }
        outs.forEach(function (e) { walk(e[1], sofar.concat(e[1])); });
      })('Start', []);
      return { d: d, vals: vals, slack: slack, crit: crit, ce: ce, T: T, paths: paths };
    }
    var base = solve(delta), prev = null, shownT = base.T, shownCost = 0;
    var MAXW = crash ? base.T + 1 : base.T + 5;
    function motion() { return !(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches); }
    function count(el, from, to, fmt) {   /* a number that runs to its new value instead of jumping */
      if (!el) return; if (from === to || !motion()) { el.textContent = fmt(to); return; }
      var t0 = null; (function step(ts) { if (t0 === null) t0 = ts; var k = Math.min((ts - t0) / 600, 1), e = 1 - Math.pow(1 - k, 3);
        el.textContent = fmt(Math.round(from + (to - from) * e)); if (k < 1) requestAnimationFrame(step); })(performance.now());
    }
    function animate(S, hit) {   /* the change travels: forward along the arrows, then back, then the critical path starts to flow */
      var svg = fig.querySelector('svg'), gs = fig.querySelectorAll('svg g.n'), es = fig.querySelectorAll('svg g.e'), maxc = 0, NSV = 'http://www.w3.org/2000/svg';
      ids.forEach(function (id) { maxc = Math.max(maxc, net.nodes[id].pos[0]); });
      net.edges.forEach(function (e, i) {
        var g = es[i]; if (!g) return;
        if (S.ce[e[0] + '>' + e[1]]) {   /* white dashes running along every critical arrow, in the direction of the work */
          var l = g.querySelector('.e-l'), f = l.cloneNode(false); f.setAttribute('class', 'e-flow'); g.appendChild(f);
          if (prev && !prev.ce[e[0] + '>' + e[1]]) g.classList.add('newcrit');
        }
        if (prev && hit && JSON.stringify(prev.vals[e[1]]) !== JSON.stringify(S.vals[e[1]])) { g.classList.add('wave'); g.style.setProperty('--d', (net.nodes[e[0]].pos[0] * 0.16) + 's'); }
      });
      if (!prev) return;
      ids.forEach(function (id, i) {
        var g = gs[i]; if (!g) return; var col = net.nodes[id].pos[0], tv = g.querySelectorAll('.n-v');
        g.style.setProperty('--d', (col * 0.16 + 0.1) + 's'); g.style.setProperty('--db', (maxc * 0.16 + 0.35 + (maxc - col) * 0.16) + 's');
        [0, 1, 2, 3].forEach(function (k) { if (tv[k] && prev.vals[id][k] !== S.vals[id][k]) tv[k].classList.add('chg'); });
        if (id === hit) { g.classList.add('hit'); var ring = document.createElementNS(NSV, 'circle'); ring.setAttribute('r', 36); ring.setAttribute('class', 'burst'); g.insertBefore(ring, g.firstChild); }
        if (S.crit[id] && !prev.crit[id] && id !== 'Start') g.classList.add('newcrit');
        if (!S.crit[id] && prev.crit[id]) g.classList.add('uncrit');
      });
      Array.prototype.forEach.call(fig.querySelectorAll('svg g.sl'), function (b, i) {
        var id = ids.filter(function (q) { return q !== 'Start'; })[i];
        if (id && prev.slack[id] !== S.slack[id]) { b.classList.add('chg'); b.style.setProperty('--db', (maxc * 0.16 + 0.5 + (maxc - net.nodes[id].pos[0]) * 0.16) + 's'); }
      });
    }
    function money(n) { return '$' + n.toLocaleString('en-US'); }
    function wk(n) { return n + (n === 1 ? ' week' : ' weeks'); }
    function cost(dl) { var c = 0; ids.forEach(function (id) { if (dl[id]) c += dl[id] * M.crash[id].cost; }); return c; }
    function list(dl) {
      return ids.filter(function (id) { return dl[id]; }).map(function (id) { return id + ' ' + (crash ? '−' : '+') + dl[id]; }).join(', ');
    }
    function pathsText(S) { return (S.paths.length > 1 ? 'Critical paths: ' : 'Critical path: ') + S.paths.join(' and ') + '.'; }

    var ctl = views(body, M.presets.map(function (p) { return p.label; }), function (i) {
      ids.forEach(function (id) { delta[id] = M.presets[i].set[id] || 0; }); hist = [];
      draw(M.presets[i].cap || null, null);
    });
    var undo = H('button', 'pm-undo', ctl.buttons[0].parentNode, '&#8630; Undo'); undo.type = 'button';
    var stat = H('div', 'pm-stat', body), meter = H('div', 'pm-meter', body, '<i class="base"></i><i class="fill"></i>' + (M.deadline ? '<i class="dl"><b>deadline</b></i>' : '') + '<span class="lab"></span>'), capbox = H('div', 'pm-caps', body), cap = H('div', 'pm-cap on', capbox);
    capbox.setAttribute('aria-live', 'polite');
    body.appendChild(fig);
    H('p', 'pm-hint', body, crash ? 'Tap an activity to crash it by one week.' : 'Tap an activity to make it run one week late.');
    key(body, [K.c, K.s, '<span class="sw" style="background:#fff;border:2px solid var(--crit)"></span>Changed duration']);

    function explain(id, before, after) {
      var h, t;
      if (crash) {
        h = id + ' crashed by 1 week for ' + money(M.crash[id].cost);
        if (after.T < before.T) t = 'The project is down to ' + wk(after.T) + '. ';
        else if (!before.crit[id]) t = id + ' was not on a critical path, so the ' + money(M.crash[id].cost) + ' bought no time: still ' + wk(after.T) + '. ';
        else t = 'Only one critical path got shorter. Another still takes ' + wk(after.T) + ', so the finish did not move. ';
      } else {
        h = id + ' runs 1 week late';
        if (after.T > before.T) t = id + ' had no slack left, so the whole project slips to ' + wk(after.T) + '. ';
        else {
          t = id + ' had ' + wk(before.slack[id]) + ' of slack to absorb it, so the project still finishes in ' + wk(after.T) + '. ';
          var lost = ids.filter(function (q) { return q !== 'Start' && after.crit[q] && !before.crit[q]; });
          if (lost.length) t += lost.join(' and ') + (lost.length > 1 ? ' have' : ' has') + ' no slack left now. ';
        }
      }
      return '<b class="pm-h">' + h + '</b>' + t + pathsText(after);
    }
    function draw(text, why) {
      var S = solve(delta), st = { n: {}, e: S.ce, dur: S.d, vals: S.vals, slack: S.slack, crashed: ids.filter(function (id) { return delta[id]; }) };
      ids.forEach(function (id) { st.n[id] = { v: ['es', 'ef', 'ls', 'lf'], cls: S.crit[id] && id !== 'Start' ? 'crit' : '', use: [] }; });
      network(fig, net, st, 'full', null, true);
      var gs = fig.querySelectorAll('svg g.n');
      ids.forEach(function (id, i) {
        if (id === 'Start' || !gs[i]) return;
        var g = gs[i], full = crash ? S.d[id] <= M.crash[id].min : delta[id] >= 3;
        g.classList.add('tap'); if (full) g.classList.add('full');
        g.setAttribute('tabindex', '0'); g.setAttribute('role', 'button');
        g.setAttribute('aria-label', 'Activity ' + id + ', ' + wk(S.d[id]) + (crash ? '. Crash by one week' : '. Delay by one week'));
        function act() {
          if (full) { cap.innerHTML = '<b class="pm-h">' + id + ' cannot change any further</b>' + (crash ? 'Its crash time is ' + wk(M.crash[id].min) + ', the shortest it can be made.' : 'Three weeks late is as far as this goes.'); return; }
          var before = solve(delta); hist.push(JSON.stringify(delta)); delta[id]++;
          ctl.buttons.forEach(function (b) { b.setAttribute('aria-pressed', 'false'); });
          draw(null, [id, before]);
        }
        g.addEventListener('click', act);
        g.addEventListener('keydown', function (ev) { if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); act(); } });
      });
      if (motion()) animate(S, why ? why[0] : null);
      prev = S;
      var late = M.deadline && S.T > M.deadline;
      meter.querySelector('.fill').style.width = (S.T / MAXW * 100) + '%';
      meter.querySelector('.fill').className = 'fill' + (late ? ' bad' : (S.T < base.T ? ' good' : ''));
      meter.querySelector('.base').style.left = (base.T / MAXW * 100) + '%';
      if (M.deadline) meter.querySelector('.dl').style.left = (M.deadline / MAXW * 100) + '%';
      var lab = meter.querySelector('.lab'); lab.style.left = (S.T / MAXW * 100) + '%'; lab.className = 'lab' + (late ? ' bad' : '');
      count(lab, shownT, S.T, function (n) { return 'week ' + n; }); shownT = S.T;
      var diff = S.T - base.T, s = '<span><b>' + wk(S.T) + '</b> to finish' + (diff ? ' <em class="' + (diff > 0 ? 'bad' : 'good') + '">' + (diff > 0 ? '+' : '−') + Math.abs(diff) + '</em>' : '') + '</span>';
      if (crash) s += '<span>Crash cost <b class="cost"></b></span>';
      else if (M.deadline) s += '<span class="' + (S.T > M.deadline ? 'bad' : 'good') + '">' + (S.T > M.deadline ? '&#10007; misses' : '&#10003; meets') + ' the ' + M.deadline + '-week deadline</span>';
      if (list(delta)) s += '<span class="chg">' + list(delta) + '</span>';
      stat.innerHTML = s;
      if (crash) { count(stat.querySelector('.cost'), shownCost, cost(delta), money); shownCost = cost(delta); }
      cap.innerHTML = text || (why ? explain(why[0], why[1], S) : M.intro);
      undo.disabled = !hist.length;
    }
    undo.onclick = function () { if (hist.length) { delta = JSON.parse(hist.pop()); ctl.buttons.forEach(function (b) { b.setAttribute('aria-pressed', 'false'); }); draw('<b class="pm-h">Last change undone</b>' + pathsText(solve(delta)), null); } };
    ctl.set(0);
    var lastW = fig.clientWidth;
    if (window.ResizeObserver) new ResizeObserver(function () { if (Math.abs(fig.clientWidth - lastW) > 4) { lastW = fig.clientWidth; var keep = cap.innerHTML; draw(keep, null); } }).observe(fig);
  };

