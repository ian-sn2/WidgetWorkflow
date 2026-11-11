<script>
(function () {
  var NS = 'http://www.w3.org/2000/svg', uid = 0;
  function E(tag, a, p) { var e = document.createElementNS(NS, tag); if (a) for (var k in a) e.setAttribute(k, a[k]); if (p) p.appendChild(e); return e; }
  function T(p, x, y, s, c) { var t = E('text', { x: x, y: y, 'class': c }, p); t.textContent = s; return t; }
  function H(tag, c, p, html) { var e = document.createElement(tag); if (c) e.className = c; if (html != null) e.innerHTML = html; if (p) p.appendChild(e); return e; }
  function f1(n) { return Math.round(n * 10) / 10; }

  /* ---------- controls ---------- */
  function caps(body, list) {
    var box = H('div', 'pm-caps', body); box.setAttribute('aria-live', 'polite');
    var items = list.map(function (h) { return H('div', 'pm-cap', box, h); });
    return function (i) { items.forEach(function (d, j) { d.classList.toggle('on', i === j); }); };
  }
  function stepper(body, n, go) {
    var bar = H('div', 'pm-bar', body);
    var back = H('button', 'pm-back', bar, '&#9664; Back'), cnt = H('span', 'pm-count', bar), next = H('button', 'pm-next', bar, 'Next &#9654;');
    back.type = next.type = 'button';
    var dots = H('div', 'pm-dots'); dots.setAttribute('aria-hidden', 'true');
    for (var k = 0; k < n; k++) H('span', '', dots);
    var i = 0;
    function set(j) {
      i = j; back.disabled = i === 0; next.disabled = i === n - 1; cnt.textContent = 'Step ' + (i + 1) + ' of ' + n;
      Array.prototype.forEach.call(dots.children, function (d, m) { d.classList.toggle('on', m <= i); });
      go(i);
    }
    back.onclick = function () { if (i > 0) set(i - 1); };
    next.onclick = function () { if (i < n - 1) set(i + 1); };
    return { set: set, dots: dots };
  }
  function views(body, labels, go, cls) {
    var bar = H('div', 'pm-bar pm-views ' + (cls || ''), body); bar.setAttribute('role', 'group');
    var bs = labels.map(function (l, i) { var b = H('button', '', bar, l); b.type = 'button'; b.onclick = function () { set(i); }; return b; });
    function set(i) { bs.forEach(function (b, j) { b.setAttribute('aria-pressed', i === j ? 'true' : 'false'); }); go(i); }
    return { set: set, buttons: bs };
  }

  /* ---------- graph drawing ---------- */
  function arrow(g, x1, y1, x2, y2, r1, r2, cls, label, side, dashed) {
    var dx = x2 - x1, dy = y2 - y1, L = Math.sqrt(dx * dx + dy * dy), ux = dx / L, uy = dy / L;
    var big = /crit|path/.test(cls), hl = big ? 11 : 9, hw = big ? 5.5 : 4.4;
    var sx = x1 + ux * (r1 + 3), sy = y1 + uy * (r1 + 3), tx = x2 - ux * (r2 + 3), ty = y2 - uy * (r2 + 3);
    var bx = tx - ux * hl, by = ty - uy * hl;
    var gg = E('g', { 'class': 'e ' + (cls || '') }, g);
    E('line', { x1: f1(sx), y1: f1(sy), x2: f1(bx + ux), y2: f1(by + uy), 'class': 'e-l' + (dashed ? ' dash' : '') }, gg);
    E('polygon', { points: [f1(tx) + ',' + f1(ty), f1(bx - uy * hw) + ',' + f1(by + ux * hw), f1(bx + uy * hw) + ',' + f1(by - ux * hw)].join(' '), 'class': 'e-h' }, gg);
    if (label) {
      var off = dashed ? 22 : 13, mx = (sx + tx) / 2 + (-uy) * off * (side || -1), my = (sy + ty) / 2 + ux * off * (side || -1);
      if (dashed) { var t = T(gg, f1(mx), f1(my - 6), 'Dummy', 'e-t dm'); T(gg, f1(mx), f1(my + 7), 'activity', 'e-t dm'); }
      else T(gg, f1(mx), f1(my), label, 'e-t');
    }
    return gg;
  }

  var GEO = { full: { R: 36, SX: 130, SY: 114, M: 46, VX: 96, VY: 106 }, plain: { R: 21, SX: 104, SY: 64, M: 30 }, aoa: { R: 14, SX: 112, SY: 62, M: 30 } };

  function fullNode(g, clip, R, id, d, vals, ns, crashed) {
    var gr = E('g', { 'class': 'n ' + (ns.cls || '') }, g);
    var v = ns.v || [], has = function (k) { return v.indexOf(k) >= 0; };
    if (/cur-/.test(ns.cls || '')) E('circle', { r: R + 5, 'class': 'n-halo' }, gr);
    E('circle', { r: R, 'class': 'n-bg' }, gr);
    var xl = R * 0.34, yl = Math.sqrt(R * R - xl * xl), w = R - xl;
    var cg = E('g', { 'clip-path': 'url(#' + clip + ')' }, gr);
    if (has('es')) { E('rect', { x: -R, y: -R, width: w, height: R, 'class': 'cf' }, cg); E('rect', { x: xl, y: -R, width: w, height: R, 'class': 'cf' }, cg); }
    if (has('ls')) { E('rect', { x: -R, y: 0, width: w, height: R, 'class': 'cb' }, cg); E('rect', { x: xl, y: 0, width: w, height: R, 'class': 'cb' }, cg); }
    (ns.use || []).forEach(function (k) {
      E('rect', { x: (k === 'es' || k === 'ls') ? -R : xl, y: (k === 'es' || k === 'ef') ? -R : 0, width: w, height: R, 'class': 'cu' }, cg);
    });
    E('line', { x1: -xl, y1: -yl, x2: -xl, y2: yl, 'class': 'n-div' }, gr);
    E('line', { x1: xl, y1: -yl, x2: xl, y2: yl, 'class': 'n-div' }, gr);
    E('line', { x1: -R, y1: 0, x2: -xl, y2: 0, 'class': 'n-div' }, gr);
    E('line', { x1: xl, y1: 0, x2: R, y2: 0, 'class': 'n-div' }, gr);
    E('circle', { r: R, 'class': 'n-c' }, gr);
    T(gr, 0, f1(-R * 0.36), id, 'n-l' + (id === 'Start' ? ' n-ls' : ''));
    T(gr, 0, f1(R * 0.6), String(d), 'n-d' + (crashed ? ' n-x' : ''));
    var cx = R * 0.61, cy = R * 0.37, at = { es: [-cx, -cy, 'vf', 0], ef: [cx, -cy, 'vf', 1], ls: [-cx, cy, 'vb', 2], lf: [cx, cy, 'vb', 3] };
    v.forEach(function (k) { var p = at[k]; T(gr, f1(p[0]), f1(p[1]), String(vals[p[3]]), 'n-v ' + p[2]); });
    return gr;
  }
  function plainNode(g, R, id, ns, kind) {
    var gr = E('g', { 'class': 'n ' + kind + ' ' + (ns.cls || '') }, g);
    E('circle', { r: R, 'class': 'n-bg' }, gr); E('circle', { r: R, 'class': 'n-c' }, gr);
    if (kind === 'plain') T(gr, 0, 0, id, 'n-l' + (id === 'Start' ? ' n-ls' : ''));
    return gr;
  }

  /* a network in (column,row) units, laid out across, or down on a narrow screen */
  function network(holder, net, st, style, aoa, reserve) {
    var g = GEO[style], vertical = style === 'full' && holder.clientWidth < 560;
    var nodes = aoa ? aoa.nodes : null, P = {}, W = 0, Hh = 0, id, PS = {}, maxc = 0;
    var src = aoa ? nodes : net.nodes, room = st.slack || reserve, side = vertical && room ? 100 : g.M;
    for (id in src) {
      var pos = aoa ? src[id] : src[id].pos, x, y;
      if (vertical) { x = side + pos[1] * g.VY; y = g.M + pos[0] * g.VX; } else { x = g.M + pos[0] * g.SX; y = g.M + pos[1] * g.SY; }
      P[id] = [x, y]; PS[id] = pos; maxc = Math.max(maxc, pos[0]); W = Math.max(W, x + side); Hh = Math.max(Hh, y + g.M);
    }
    if (style === 'full' && (!vertical || room)) Hh += vertical ? 16 : 10;
    holder.innerHTML = '';
    var svg = E('svg', { viewBox: '0 0 ' + W + ' ' + Hh, 'class': 'pm-fig', role: 'img', 'aria-label': 'Project network' }, holder);
    svg.style.maxWidth = W + 'px'; svg.style.margin = '0 auto';
    var clip = 'pmclip' + (++uid), defs = E('defs', {}, svg), cp = E('clipPath', { id: clip }, defs); E('circle', { r: g.R }, cp);
    var ge = E('g', {}, svg), gn = E('g', {}, svg);
    if (aoa) {
      aoa.edges.forEach(function (e) { var a = P[e[0]], b = P[e[1]]; arrow(ge, a[0], a[1], b[0], b[1], g.R, g.R, '', e[2], e[3], e[4]); });
      for (id in P) { var q = plainNode(gn, g.R, id, {}, 'aoa'); q.setAttribute('transform', 'translate(' + P[id][0] + ',' + P[id][1] + ')'); }
      return;
    }
    var en = st.e || {}, segs = [];
    net.edges.forEach(function (e) {
      var k = e[0] + '>' + e[1], c = en[k] || '';
      if (c === 'hide') return;
      var a = P[e[0]], b = P[e[1]];
      arrow(ge, a[0], a[1], b[0], b[1], g.R, g.R, c); segs.push([a[0], a[1], b[0], b[1]]);
    });
    function clear(x, y, w, h) {   /* does a w x h box centred at x,y stay inside the panel and off every arrow? */
      if (x - w / 2 < 1 || x + w / 2 > W - 1 || y + h / 2 > Hh - 1) return false;
      for (var nid in P) { var dx = Math.max(Math.abs(P[nid][0] - x) - w / 2, 0), dy = Math.max(Math.abs(P[nid][1] - y) - h / 2, 0); if (Math.sqrt(dx * dx + dy * dy) < g.R + 2) return false; }
      return segs.every(function (q) {
        for (var k = 0; k <= 60; k++) {
          var px = q[0] + (q[2] - q[0]) * k / 60, py = q[1] + (q[3] - q[1]) * k / 60;
          if (Math.abs(px - x) < w / 2 + 2 && Math.abs(py - y) < h / 2 + 2) return false;
        }
        return true;
      });
    }
    for (id in P) {
      var ns = st.n ? st.n[id] : {}, gr;
      if (ns && ns.cls === 'hide') continue;
      if (style === 'full') {
        var vals = (st.vals || net.vals)[id], d = st.dur ? st.dur[id] : net.nodes[id].d;
        gr = fullNode(gn, clip, g.R, id, d, vals, ns || {}, st.crashed && st.crashed.indexOf(id) >= 0);
      } else gr = plainNode(gn, g.R, id, ns || {}, 'plain');
      gr.setAttribute('transform', 'translate(' + P[id][0] + ',' + P[id][1] + ')');
      if (st.slack && id in st.slack) {
        var s = st.slack[id], bw = 54, bh = 17, sx, sy;
        if (vertical) {   /* beside the node on its outer side, or under the last one */
          if (PS[id][1] === 2) { sx = g.R + bw / 2 + 4; sy = 0; }
          else if (PS[id][0] === maxc) { sx = 0; sy = g.R + 13; }
          else { sx = -g.R - bw / 2 - 4; sy = 0; }
        }
        else { sx = 0; sy = g.R + 13; }
        var tries = [[sx, sy], [sx - 16, sy], [sx + 16, sy], [sx - 30, sy], [sx + 30, sy], [sx, sy + 8], [sx - 24, sy + 6]];
        for (var q = 0; q < tries.length; q++) if (clear(P[id][0] + tries[q][0], P[id][1] + tries[q][1], bw, bh)) { sx = tries[q][0]; sy = tries[q][1]; break; }
        var sg = E('g', { 'class': 'sl' + (s === 0 ? ' z' : ''), transform: 'translate(' + f1(P[id][0] + sx) + ',' + f1(P[id][1] + sy) + ')' }, gn);
        E('rect', { x: -bw / 2, y: -bh / 2, width: bw, height: bh, rx: 8 }, sg);
        T(sg, 0, 0, 'Slack ' + s, '');
      }
    }
  }

  function small(holder, spec, kind) {
    var R = kind === 'aon' ? 20 : 13;
    var svg = E('svg', { viewBox: '0 0 300 160', 'class': 'pm-fig', role: 'img', 'aria-label': kind === 'aon' ? 'Activity-on-node drawing' : 'Activity-on-arrow drawing' }, holder);
    svg.style.maxWidth = '360px'; svg.style.margin = '0 auto';
    var ge = E('g', {}, svg), gn = E('g', {}, svg), P = spec.nodes;
    spec.edges.forEach(function (e) { var a = P[e[0]], b = P[e[1]]; arrow(ge, a[0], a[1], b[0], b[1], R, R, '', kind === 'aoa' ? e[2] : null, e[3], e[4]); });
    for (var id in P) { var q = plainNode(gn, R, id, {}, kind === 'aon' ? 'plain' : 'aoa'); q.setAttribute('transform', 'translate(' + P[id][0] + ',' + P[id][1] + ')'); }
  }

  function key(body, items) {
    var k = H('div', 'pm-key', body);
    items.forEach(function (it) { H('span', '', k, it); });
  }
  var K = {
    f: '<span class="sw" style="background:var(--fwd-bg);border:1px solid var(--fwd)"></span>Forward pass (ES, EF)',
    b: '<span class="sw" style="background:var(--bwd-bg);border:1px solid var(--bwd)"></span>Backward pass (LS, LF)',
    u: '<span class="sw" style="background:var(--use)"></span>Value used in this step',
    c: '<i style="color:var(--crit)"></i>Critical path',
    p: '<i style="color:var(--path)"></i>Selected path',
    s: '<span class="sw" style="background:var(--slack-bg);border:1px solid var(--slack-rule)"></span>Slack'
  };

  /* ---------- widgets ---------- */
  var W = {};
  W.net = function (body, M) {
    var list = M.steps || M.views, fig = H('div', 'pm-figwrap'), cur = 0, anyS = list.some(function (s) { return s.slack; });
    var capHtml = list.map(function (s) { return s.cap + (s.calc ? '<div class="pm-calc">' + s.calc + '</div>' : ''); });
    var ctl = M.steps ? stepper(body, list.length, show) : views(body, list.map(function (s) { return s.label; }), show);
    var setCap = caps(body, capHtml);
    body.appendChild(fig);
    if (M.style === 'full') key(body, M.steps ? [K.f, K.b, K.u] : (list.some(function (s) { return s.slack; }) ? [K.c, K.s].concat(M.views && M.views.length > 2 ? [K.p] : []) : []));
    if (ctl.dots) body.appendChild(ctl.dots);
    function show(i) { cur = i; setCap(i); network(fig, M.net, list[i], M.style, null, anyS); }
    ctl.set(0);
    var lastW = fig.clientWidth;
    if (window.ResizeObserver) new ResizeObserver(function () { if (Math.abs(fig.clientWidth - lastW) > 4) { lastW = fig.clientWidth; network(fig, M.net, list[cur], M.style, null, anyS); } }).observe(fig);
  };
  W.both = function (body, M) {
    var fig = H('div', 'pm-figwrap');
    var ctl = views(body, M.views.map(function (v) { return v.label; }), function (i) {
      var st = { n: {}, e: {} };
      if (M.views[i].kind === 'aon') network(fig, M.net, st, 'plain'); else network(fig, M.net, st, 'aoa', M.aoa);
    });
    body.appendChild(fig); ctl.set(0);
  };
  W.conv = function (body, M) {
    var setCap = caps(body, M.cases.map(function (c, i) { return '<span class="pm-rule">' + (i + 1) + ') ' + c.rule + '</span>'; }));
    var grid = H('div', 'pm-conv'), l = H('div', '', grid), r = H('div', '', grid);
    var ctl = views(body, M.cases.map(function (c, i) { return 'Case ' + (i + 1); }), function (i) {
      setCap(i); l.innerHTML = '<p class="pm-sub">Activity-on-Node (AON)</p>'; r.innerHTML = '<p class="pm-sub aoa">Activity-on-Arrow (AOA)</p>';
      small(l, M.cases[i].aon, 'aon'); small(r, M.cases[i].aoa, 'aoa');
    });
    body.insertBefore(ctl.buttons[0].parentNode, body.firstChild);
    body.appendChild(grid); ctl.set(0);
  };
  W.gantt = function (body, M) {
    var setCap = caps(body, M.views.map(function (v) { return v.cap; }));
    var sc = H('div', 'pg-scroll', body), grid = H('div', 'pg-grid pg-rows', sc), bars = [];
    M.rows.forEach(function (r) {
      var row = H('div', 'pg-row', grid);
      H('span', 'pg-lab', row, r.id + ' <small>(' + r.d + ' wk)</small>');
      var tr = H('div', 'pg-track', row), sl = r.ls - r.es;
      var s = sl ? H('span', 'pg-s', tr, sl + ' wk') : null, b = H('span', 'pg-b' + (r.crit ? ' crit' : ''), tr);
      b.style.width = (r.d / M.end * 100) + '%'; if (s) s.style.width = (sl / M.end * 100) + '%';
      bars.push({ r: r, b: b, s: s });
    });
    var ax = H('div', 'pg-row pg-axis', grid); H('span', 'pg-lab', ax, 'Week'); var at = H('div', 'pg-track', ax);
    for (var w = 0; w <= M.end; w++) { var t = H('span', '', at, String(w)); t.style.left = (w / M.end * 100) + '%'; }
    key(body, ['<span class="sw" style="background:var(--crit)"></span>Critical activity', '<span class="sw" style="background:var(--fwd)"></span>Activity with slack', K.s]);
    var ctl = views(body, M.views.map(function (v) { return v.label; }), function (i) {
      setCap(i); var k = M.views[i].key;
      bars.forEach(function (o) {
        var st = k === 'es' ? o.r.es : o.r.ls, fin = st + o.r.d;
        o.b.style.left = (st / M.end * 100) + '%'; o.b.textContent = st + '–' + fin;
        if (o.s) o.s.style.left = ((k === 'es' ? o.r.ef : o.r.es) / M.end * 100) + '%';
      });
    });
    body.insertBefore(ctl.buttons[0].parentNode, body.firstChild);
    ctl.set(0);
  };

  /* ---------- curves ---------- */
  var PDF0 = 1 / Math.sqrt(2 * Math.PI);
  function pdf(z) { return Math.exp(-z * z / 2) * PDF0; }
  function bellSVG(holder, o) {
    var Wd = 600, Hd = 214, L = 22, Rr = 22, B = 166, Tp = 14, zmin = -3.6, zmax = 3.6;
    function X(z) { return L + (z - zmin) / (zmax - zmin) * (Wd - L - Rr); }
    function Y(p) { return B - p / PDF0 * (B - Tp); }
    holder.innerHTML = '';
    var svg = E('svg', { viewBox: '0 0 ' + Wd + ' ' + Hd, 'class': 'pm-fig', role: 'img', 'aria-label': o.aria || 'Normal curve' }, holder);
    svg.style.maxWidth = '560px'; svg.style.margin = '0 auto';
    function area(a, b) {
      var d = 'M' + f1(X(a)) + ',' + B, n = 60;
      for (var i = 0; i <= n; i++) { var z = a + (b - a) * i / n; d += ' L' + f1(X(z)) + ',' + f1(Y(pdf(z))); }
      return d + ' L' + f1(X(b)) + ',' + B + ' Z';
    }
    if (o.shade) E('path', { d: area(o.shade[0], o.shade[1]), 'class': 'crv-fill' }, svg);
    if (o.tail) E('path', { d: area(o.tail[0], zmax), 'class': 'crv-tail' }, svg);
    var d = '', n = 160;
    for (var i = 0; i <= n; i++) { var z = zmin + (zmax - zmin) * i / n; d += (i ? ' L' : 'M') + f1(X(z)) + ',' + f1(Y(pdf(z))); }
    E('line', { x1: L - 10, y1: B, x2: Wd - Rr + 10, y2: B, 'class': 'ax' }, svg);
    (o.lines || []).forEach(function (l) {   /* a marked deadline stands at least 60px tall, wherever the curve is */
      var top = l.cls ? Math.min(Y(pdf(l.z)), B - 60) : Y(pdf(l.z));
      E('line', { x1: f1(X(l.z)), y1: f1(top), x2: f1(X(l.z)), y2: B, 'class': 'gd' + (l.cls ? ' ' + l.cls : '') }, svg);
    });
    (o.ticks || []).forEach(function (z) { E('line', { x1: f1(X(z)), y1: B, x2: f1(X(z)), y2: B + 5, 'class': 'tk' }, svg); });
    E('path', { d: d, 'class': 'crv' }, svg);
    (o.labels || []).forEach(function (l) {
      T(svg, f1(Math.min(Math.max(X(l.z), 40), Wd - 50)), B + 21, l.t, 'tl');
      if (l.s) T(svg, f1(Math.min(Math.max(X(l.z), 40), Wd - 50)), B + 39, l.s, 'tl sm');
    });
    if (o.big) T(svg, f1(X(o.big[0])), f1(o.big[1]), o.big[2], 'big halo');
    if (o.tail && o.tail[1]) {   /* the tail's own name, off to the right with a leader into it */
      var tz = o.tail[0] + 0.35, tyy = B - (B - Y(pdf(tz))) * 0.4;
      E('line', { x1: f1(X(3.05)), y1: f1(B - 58), x2: f1(X(tz)), y2: f1(tyy), 'class': 'lead tail' }, svg);
      T(svg, f1(X(3.05)), f1(B - 64), o.tail[1], 'mk tailtxt');
    }
    if (o.dim) {   /* a dimension arrow between two z values, named above */
      var x0 = X(o.dim[0]) + 2, x1 = X(o.dim[1]) - 2, yy = B - 6;
      E('line', { x1: f1(x0 + 6), y1: yy, x2: f1(x1 - 6), y2: yy, 'class': 'dim' }, svg);
      E('polygon', { points: f1(x0) + ',' + yy + ' ' + f1(x0 + 8) + ',' + (yy - 4) + ' ' + f1(x0 + 8) + ',' + (yy + 4), 'class': 'dimh' }, svg);
      E('polygon', { points: f1(x1) + ',' + yy + ' ' + f1(x1 - 8) + ',' + (yy - 4) + ' ' + f1(x1 - 8) + ',' + (yy + 4), 'class': 'dimh' }, svg);
      /* the name sits in the tall part of the shaded area, two lines, clear of the curve */
      T(svg, f1(X(0.82)), yy - 30, o.dim[2][0], 'mk dimtxt big2');
      T(svg, f1(X(0.82)), yy - 13, o.dim[2][1], 'mk dimtxt');
    }
    if (o.call) {
      var zt = Math.max(-3.2, o.call[1]), ty = (B + Y(pdf(zt))) / 2, tx = X(-2.55);
      E('line', { x1: f1(tx + 14), y1: 54, x2: f1(X(zt)), y2: f1(ty), 'class': 'lead' }, svg);
      T(svg, f1(tx), 44, o.call[0], 'big');
    }
  }
  function zlab(z) { return (z < 0 ? '−' : '') + Math.abs(z).toFixed(2); }

  W.bands = function (body, M) {
    var fig = H('div', 'pm-figwrap'), setCap;
    var ctl = views(body, M.views.map(function (v) { return v.label + ' · ' + v.pct; }), function (i) {
      var v = M.views[i], k = v.k, labels = [], lines = [];
      for (var j = -3; j <= 3; j++) { lines.push({ z: j }); labels.push({ z: j, t: j === 0 ? 'μ' : 'μ ' + (j < 0 ? '−' : '+') + ' ' + Math.abs(j) + 'σ' }); }
      bellSVG(fig, { shade: [-k, k], lines: lines, labels: labels, big: [0, 112, v.pct], aria: 'Normal curve with ' + v.pct + ' of the area within ' + k + ' standard deviations of the mean' });
      setCap(i);
    });
    setCap = caps(body, M.views.map(function (v) { return v.cap; }));
    body.appendChild(fig); ctl.set(0);
  };
  W.deadline = function (body, M) {
    var S = M.states, row = H('div', 'pm-slider', body);
    H('label', '', row, 'Deadline');
    var inp = H('input', '', row); inp.type = 'range'; inp.min = 0; inp.max = S.length - 1; inp.step = 1; inp.value = M.start;
    var out = H('output', '', row);
    inp.setAttribute('aria-label', 'Deadline in weeks');
    var cap = H('div', 'pm-caps', body), c1 = H('div', 'pm-cap on', cap); cap.setAttribute('aria-live', 'polite');
    var fig = H('div', 'pm-figwrap', body);
    function show() {
      var s = S[+inp.value], x = s.x, xs = (x % 1 ? x.toFixed(1) : String(x)), z = s.z;
      out.textContent = xs + ' weeks';
      inp.setAttribute('aria-valuetext', xs + ' weeks');
      c1.innerHTML = '<b class="pm-h">' + (+s.p * 100).toFixed(3) + '% chance of finishing within ' + xs + ' weeks</b>' +
        'z = (' + xs + ' − 15) ÷ 1.76 = ' + zlab(z) + ', and the normal table gives P(z ≤ ' + zlab(z) + ') = <b>' + s.p + '</b>.';
      var lab = [{ z: 0, t: 'μ', s: '15 weeks' }];
      if (Math.abs(z) > 0.6) lab.push({ z: z, t: 'μ ' + (z < 0 ? '−' : '+') + ' ' + Math.abs(z).toFixed(2) + 'σ', s: xs + ' weeks' });
      else if (z !== 0) { lab[0] = { z: 0, t: 'μ', s: '' }; lab.push({ z: z + (z > 0 ? 0.55 : -0.55), t: 'μ ' + (z < 0 ? '−' : '+') + ' ' + Math.abs(z).toFixed(2) + 'σ', s: xs + ' weeks' }); }
      var bx = Math.max(-3.6, Math.min(z, 3.6));
      bellSVG(fig, { shade: [-3.6, bx], lines: [{ z: 0 }, { z: bx }], labels: lab, call: [s.p, Math.min(bx - 0.45, -0.9)],
        aria: 'Normal curve shaded to the left of ' + xs + ' weeks: probability ' + s.p });
    }
    inp.addEventListener('input', show); show();
  };
  W.ninety = function (body, M) {
    var fig = H('div', 'pm-figwrap'), setCap;
    var ctl = stepper(body, M.steps.length, function (i) {
      setCap(i); var s = M.steps[i], z = s.z, o = { shade: [-3.6, z], call: ['0.99', -0.9] };
      if (i === 0) {          /* the area we want: the deadline is still unknown */
        o.lines = [{ z: 0 }, { z: z, cls: 'q' }];
        o.labels = [{ z: 0, t: 'μ', s: '15 weeks' }, { z: z, t: '?', s: 'deadline' }];
        o.aria = 'Normal curve with 0.99 of the area shaded up to an unknown deadline';
      } else if (i === 1) {   /* find z: the 0.01 left over, and the axis in z units */
        o.lines = [{ z: 0 }, { z: z, cls: 'b' }]; o.tail = [z, '0.01']; o.ticks = [1, 2, 3];
        o.labels = [{ z: 0, t: 'z = 0' }, { z: 1, t: '1' }, { z: z, t: 'z = 2.33', s: 'P = 0.9901' }];
        o.aria = 'Normal curve: 0.99 to the left of z = 2.33 and 0.01 to its right';
      } else {                /* convert to weeks: 2.33 standard deviations above the mean */
        o.lines = [{ z: 0 }, { z: z, cls: 'b' }]; o.tail = [z, ''];
        o.labels = [{ z: 0, t: 'μ = 15 weeks' }, { z: z, t: 'x = 19.10 weeks' }];
        o.dim = [0, z, ['4.10 weeks', '2.33 × 1.76']];
        o.aria = 'Normal curve: the deadline 19.10 weeks lies 4.10 weeks above the 15-week mean';
      }
      bellSVG(fig, o);
    });
    setCap = caps(body, M.steps.map(function (s) { return s.cap; }));
    body.appendChild(fig); body.appendChild(ctl.dots); ctl.set(0);
  };
  W.pert = function (body, M) {
    var fig = H('div', 'pm-figwrap'), setCap;
    var ctl = views(body, M.acts.map(function (a) { return a.id; }), function (i) {
      setCap(i); var a = M.acts[i], Wd = 600, Hd = 196, L = 30, Rr = 20, B = 140, Tp = 26;
      function X(x) { return L + x / M.xmax * (Wd - L - Rr); } function Y(y) { return B - y * (B - Tp); }
      fig.innerHTML = '';
      var svg = E('svg', { viewBox: '0 0 ' + Wd + ' ' + Hd, 'class': 'pm-fig', role: 'img', 'aria-label': 'Activity ' + a.id + ': a = ' + a.a + ', m = ' + a.m + ', b = ' + a.b + ', expected time ' + a.t + ' weeks' }, fig);
      svg.style.maxWidth = '580px'; svg.style.margin = '0 auto';
      var d = 'M' + f1(X(a.a)) + ',' + B;
      a.pts.forEach(function (p) { d += ' L' + f1(X(p[0])) + ',' + f1(Y(p[1])); });
      E('path', { d: d + ' L' + f1(X(a.b)) + ',' + B + ' Z', 'class': 'crv-fill' }, svg);
      E('path', { d: 'M' + a.pts.map(function (p) { return f1(X(p[0])) + ',' + f1(Y(p[1])); }).join(' L'), 'class': 'crv' }, svg);
      E('line', { x1: L - 8, y1: B, x2: Wd - Rr + 6, y2: B, 'class': 'ax' }, svg);
      for (var w = 0; w <= M.xmax; w++) { E('line', { x1: f1(X(w)), y1: B, x2: f1(X(w)), y2: B + 5, 'class': 'tk' }, svg); T(svg, f1(X(w)), B + 20, String(w), 'tl sm'); }
      T(svg, Wd - Rr, B + 40, 'weeks', 'tl sm');
      E('line', { x1: f1(X(a.m)), y1: Tp, x2: f1(X(a.m)), y2: B, 'class': 'gd' }, svg);
      E('line', { x1: f1(X(a.t)), y1: Tp - 6, x2: f1(X(a.t)), y2: B, 'class': 'gd t' }, svg);
      T(svg, f1(X(a.t)), Tp - 12, a.t === a.m ? 't = m = ' + a.t : 't = ' + a.t, 'mk t');
      [['a', a.a], ['m', a.m], ['b', a.b]].forEach(function (p) { T(svg, f1(X(p[1])), B + 40, p[0] + ' = ' + p[1], 'mk'); });
    }, 'pm-acts');
    ctl.buttons.forEach(function (b, i) { if (M.acts[i].crit) { b.classList.add('crit'); b.title = 'On the critical path'; } });
    setCap = caps(body, M.acts.map(function (a) {
      return '<b class="pm-h">Activity ' + a.id + (a.crit ? '<span class="pm-crit-tag">critical path</span>' : '') + '</b>' +
        '<div class="pm-calc" style="border:0;margin:0;padding:0">' + a.tcalc + '<br>' + a.vcalc + '</div>';
    }));
    body.appendChild(fig);
    key(body, ['<i style="color:var(--fwd)"></i>Expected time t', '<i style="color:var(--ink);border-top-style:dashed"></i>Most likely time m', '<span class="sw" style="background:var(--crit-bg);border:1px solid var(--crit)"></span>Critical-path activity']);
    ctl.set(0);
  };

  function boot() {
    Array.prototype.forEach.call(document.querySelectorAll('.pmw[data-pm]'), function (w) {
      if (w.dataset.ready) return; w.dataset.ready = '1';
      var M = JSON.parse(w.querySelector('script[type="application/json"]').textContent), body = w.querySelector('.pm-body');
      try { W[w.dataset.pm](body, M); } catch (err) { body.textContent = ''; if (window.console) console.error(err); }
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();
</script>