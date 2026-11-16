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
    var base = solve(delta);
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
    var stat = H('div', 'pm-stat', body), capbox = H('div', 'pm-caps', body), cap = H('div', 'pm-cap on', capbox);
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
      var diff = S.T - base.T, s = '<span><b>' + wk(S.T) + '</b> to finish' + (diff ? ' <em class="' + (diff > 0 ? 'bad' : 'good') + '">' + (diff > 0 ? '+' : '−') + Math.abs(diff) + '</em>' : '') + '</span>';
      if (crash) s += '<span>Crash cost <b>' + money(cost(delta)) + '</b></span>';
      else if (M.deadline) s += '<span class="' + (S.T > M.deadline ? 'bad' : 'good') + '">' + (S.T > M.deadline ? '&#10007; misses' : '&#10003; meets') + ' the ' + M.deadline + '-week deadline</span>';
      if (list(delta)) s += '<span class="chg">' + list(delta) + '</span>';
      stat.innerHTML = s;
      cap.innerHTML = text || (why ? explain(why[0], why[1], S) : M.intro);
      undo.disabled = !hist.length;
    }
    undo.onclick = function () { if (hist.length) { delta = JSON.parse(hist.pop()); ctl.buttons.forEach(function (b) { b.setAttribute('aria-pressed', 'false'); }); draw('<b class="pm-h">Last change undone</b>' + pathsText(solve(delta)), null); } };
    ctl.set(0);
    var lastW = fig.clientWidth;
    if (window.ResizeObserver) new ResizeObserver(function () { if (Math.abs(fig.clientWidth - lastW) > 4) { lastW = fig.clientWidth; var keep = cap.innerHTML; draw(keep, null); } }).observe(fig);
  };

