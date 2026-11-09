"""REE3043 Fall '26, Chapter 17 (Sources of Commercial Debt and Equity Capital), 2026-11-09.

Two versions, per the readme Ian sent with the chapter:
  normal  - the chapter as written, with the house head and the markup fixed
  charts  - the same, plus interactive charts and diagrams drawn from the lecture deck's exhibits

Every number in the charts is printed in the deck (Exhibits 17-1 to 17-4) and agrees with the chapter's prose
(17.8T total, 54/30/8/8, 38% debt, 29%/71%, 78%/22%, banks 57% of private and 45% of all debt).

    python scripts/ree3043/chapter17.py SRC.html OUTDIR
"""
import sys, os, json, html as H

def sub1(t, old, new, what):
    assert t.count(old) == 1, (what, t.count(old)); return t.replace(old, new)

HEAD_OLD_CSS = '<link rel="stylesheet" href="https://smokinnotes.s3.us-east-1.amazonaws.com/content/sn25-v5.css">'
HEAD_NEW_CSS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
                '    <link href="https://fonts.googleapis.com/css2?family=Red+Hat+Display:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">\n'
                '    <link rel="stylesheet" href="https://smokinnotes.s3.us-east-1.amazonaws.com/content/sn25-v6.css">')

def normal(t):
    """The house head, a MathJax config that parses, and the markup fixes. No wording changes."""
    t = sub1(t, HEAD_OLD_CSS, HEAD_NEW_CSS, "css")
    t = sub1(t, '<script src="https://smokinnotes.s3.us-east-1.amazonaws.com/content/sn25-v5.js"></script>',
             '<script src="https://smokinnotes.s3.us-east-1.amazonaws.com/studyguide/sn25-v2.js"></script>', "js")
    # inlineMath: [['\','\']] is a JavaScript syntax error, so the whole config script failed to run
    t = sub1(t, "inlineMath: [['\\','\\']]", "inlineMath: [['\\\\(','\\\\)']]", "mathjax")
    # the LLC exam tip sat between </li> and </ul>, inside the list; it goes after the list
    tip = t[t.index('<div class="exam-tip">\n    <h4>EXAM TIP: Preferred Ownership Form</h4>'):]
    tip = tip[:tip.index("</div>") + 6]
    t = sub1(t, "    </li>\n\n\n" + tip + "\n\n</ul>\n", "    </li>\n</ul>\n\n" + tip + "\n", "llc tip")
    # the two aside boxes carried bare text under their headings
    for h4 in ("How Liquidity Actually Works in Open-End Funds", "Life-Cycle of a Closed-End Fund"):
        i = t.index(f"<h4>{h4}</h4>") + len(f"<h4>{h4}</h4>"); j = t.index("</div>", i)
        body = t[i:j].strip(); t = t[:i] + "\n        <p>" + body + "</p>\n        " + t[j:]
    t = t.replace("’", "'")  # one curly apostrophe in an otherwise straight-quoted file ("today's market")
    assert "sn25-v5" not in t and "<u>" not in t
    return t

# ---------------------------------------------------------------- the charts version
CSS = r"""<style>
.crev { --ink:#1c2a44; --muted:#5b6474; --rule:#dfe3ea; --soft:#f1f4f9; max-width:760px; margin:20px auto; padding:16px 18px 14px; background:#fff; border:1px solid var(--rule); border-radius:10px; box-sizing:border-box; font-family:"Red Hat Display", system-ui, sans-serif; color:var(--ink); clear:both; }
.crev * { box-sizing:border-box; }
.crev .cv-title { font-weight:800; font-size:1.02rem; margin:0 0 2px; text-align:center; }
.crev .cv-lede { font-size:.86rem; color:var(--muted); margin:0 0 12px; text-align:center; }
.crev .cv-tabs { display:flex; flex-wrap:wrap; justify-content:center; gap:6px; margin:0 0 12px; }
.crev .cv-tabs button { font:inherit; font-size:.85rem; font-weight:600; padding:6px 14px; min-height:36px; border:1px solid var(--rule); border-radius:999px; background:#fff; color:var(--ink); cursor:pointer; }
.crev .cv-tabs button[aria-pressed="true"] { background:var(--ink); border-color:var(--ink); color:#fff; }
.crev .cv-read { min-height:2.9em; margin:12px 0 0; padding:6px 10px; border-left:4px solid var(--rule); font-size:.92rem; line-height:1.35; }
.crev .cv-read b { font-weight:800; }
.crev .cv-src { font-size:.76rem; color:var(--muted); text-align:right; margin:10px 0 0; }
.crev svg, .crev svg * { outline:none; }
/* pie */
.crev .cv-body { display:flex; gap:22px; align-items:flex-start; }
.crev .cv-pie { flex:0 0 44%; width:44%; height:auto; display:block; overflow:visible; }
.crev .cv-s path { stroke:#fff; stroke-width:2; cursor:pointer; transition:opacity .15s, transform .15s; }
.crev .cv-s.on path { transform:translate(var(--dx), var(--dy)); }
.crev.has-on .cv-s:not(.on) { opacity:.3; }
.crev .cv-pie text { pointer-events:none; }
.crev .cv-side { flex:1 1 auto; min-width:0; }
.crev .cv-row { display:grid; grid-template-columns:14px 1fr auto 3.4em; gap:8px; align-items:center; padding:5px 6px; border-radius:6px; font-size:.9rem; cursor:pointer; outline:none; }
.crev .cv-row:hover, .crev .cv-row.on { background:var(--soft); }
.crev .cv-row:focus-visible { box-shadow:0 0 0 2px #2a78d6 inset; }
.crev .cv-sw { width:12px; height:12px; border-radius:3px; }
.crev .cv-v, .crev .cv-p { text-align:right; font-variant-numeric:tabular-nums; }
.crev .cv-p { color:var(--muted); }
/* bars */
.crev .cv-bar { display:grid; grid-template-columns:minmax(0, 13em) 1fr 5.2em; gap:10px; align-items:center; padding:4px 6px; border-radius:6px; font-size:.88rem; cursor:pointer; outline:none; }
.crev .cv-bar:hover, .crev .cv-bar.on { background:var(--soft); }
.crev .cv-bar:focus-visible { box-shadow:0 0 0 2px #2a78d6 inset; }
.crev .cv-bar .cv-l { line-height:1.25; }
.crev .cv-bar .cv-track { height:16px; }
.crev .cv-bar .cv-fill { height:100%; border-radius:0 4px 4px 0; min-width:3px; transition:opacity .15s; }
.crev.has-on .cv-bar:not(.on) .cv-fill { opacity:.3; }
.crev .cv-bar.hide { display:none; }
.crev .cv-key { display:flex; flex-wrap:wrap; gap:14px; justify-content:center; font-size:.82rem; color:var(--muted); margin:8px 0 0; }
.crev .cv-key span::before { content:""; display:inline-block; width:10px; height:10px; border-radius:2px; margin-right:6px; background:var(--c); vertical-align:-1px; }
/* split bar */
.crev .cv-split { display:flex; gap:2px; height:56px; border-radius:6px; overflow:hidden; }
.crev .cv-seg { display:flex; align-items:center; justify-content:center; color:#fff; font-weight:800; font-size:.95rem; cursor:pointer; outline:none; transition:opacity .15s; text-align:center; line-height:1.2; padding:0 6px; }
.crev.has-on .cv-seg:not(.on) { opacity:.35; }
/* risk ladder */
.crev .cv-ladder { display:flex; gap:14px; align-items:stretch; }
.crev .cv-axis { flex:0 0 26px; position:relative; border-radius:13px; background:linear-gradient(to top, #cfe0f7, #1d4f94); }
.crev .cv-axis::before { content:""; position:absolute; top:-10px; left:50%; transform:translateX(-50%); border:8px solid transparent; border-bottom:10px solid #1d4f94; border-top:0; }
.crev .cv-axis span { position:absolute; left:50%; top:50%; transform:translate(-50%, -50%) rotate(-90deg); white-space:nowrap; font-size:.72rem; font-weight:700; color:#fff; text-align:center; line-height:1.15; }
.crev .cv-rungs { flex:1 1 auto; display:flex; flex-direction:column; gap:8px; }
.crev .cv-rung { display:grid; grid-template-columns:14px 1fr; gap:10px; align-items:start; margin-left:calc(var(--k) * 6%); padding:8px 12px; border-radius:8px; background:var(--soft); border-left:4px solid var(--c); font-size:.88rem; line-height:1.35; }
.crev .cv-dot { width:12px; height:12px; border-radius:50%; background:var(--c); margin-top:4px; }
.crev .cv-tag { font-size:.74rem; font-weight:700; color:#fff; background:#5b6474; border-radius:999px; padding:1px 8px; margin-left:4px; white-space:nowrap; }
.crev .cv-desc { color:var(--muted); }
/* static figures */
.crev .cv-fig { width:100%; height:auto; display:block; }
.crev .cv-tree { font-size:.86rem; }
.crev .cv-tree ul { list-style:none; margin:0; padding:0 0 0 22px; position:relative; }
.crev .cv-tree > ul { padding-left:0; }
.crev .cv-tree li { position:relative; padding:4px 0 4px 0; }
.crev .cv-tree ul ul li::before { content:""; position:absolute; left:-14px; top:0; bottom:0; border-left:2px solid var(--rule); }
.crev .cv-tree ul ul li:last-child::before { bottom:auto; height:18px; }
.crev .cv-tree ul ul li::after { content:""; position:absolute; left:-14px; top:18px; width:12px; border-top:2px solid var(--rule); }
.crev .cv-node { display:inline-block; padding:4px 10px; border-radius:6px; background:var(--soft); border:1px solid var(--rule); font-weight:600; }
.crev .cv-node.hot { background:#1d4f94; border-color:#1d4f94; color:#fff; }
.crev .cv-node.warm { background:#e3edfb; border-color:#9ec0ee; }
.crev .cv-node small { font-weight:500; color:var(--muted); }
.crev .cv-node.hot small { color:#dbe7f8; }
.crev .cv-steps { display:grid; grid-template-columns:repeat(3, 1fr); gap:10px; }
.crev .cv-step { border:1px solid var(--rule); border-radius:8px; padding:10px 12px; background:var(--soft); font-size:.86rem; line-height:1.35; }
.crev .cv-step b { display:block; font-size:.92rem; margin-bottom:4px; }
.crev .cv-step .cv-n { display:inline-flex; width:24px; height:24px; border-radius:50%; background:#1d4f94; color:#fff; font-weight:800; font-size:.8rem; align-items:center; justify-content:center; margin-bottom:6px; }
.crev .cv-step .cv-split { height:30px; margin-top:8px; }
.crev .cv-step .cv-seg { font-size:.78rem; cursor:default; }
@media (max-width:600px) {
  .crev { padding:14px 12px 12px; }
  .crev .cv-body { flex-direction:column; gap:10px; }
  .crev .cv-pie { width:76%; flex-basis:auto; }
  .crev .cv-side { width:100%; }
  .crev .cv-bar { grid-template-columns:minmax(0, 8.5em) 1fr 4.6em; font-size:.82rem; }
  .crev .cv-steps { grid-template-columns:1fr; }
  .crev .cv-rung { margin-left:0; }
  .crev .cv-axis span { font-size:.66rem; }
  .crev .cv-row, .crev .cv-bar { min-height:36px; }
}
@media (prefers-reduced-motion: reduce) { .crev * { transition:none !important; } }
</style>"""

RUNTIME = r"""<script>
(function () {
  function fmtB(v) { return '$' + v.toLocaleString('en-US') + (v >= 1000 ? ' billion' : ' billion'); }
  function fmtT(v) { return '$' + v.toFixed(1) + ' trillion'; }
  function pct(v, t) { return Math.round(100 * v / t) + '%'; }
  function wire(root, items, show) {
    var pinned = null;
    items.forEach(function (el) {
      var i = +el.dataset.i;
      el.addEventListener('mouseenter', function () { if (pinned === null) show(i); });
      el.addEventListener('mouseleave', function () { if (pinned === null) show(null); });
      el.addEventListener('click', function () { pinned = (pinned === i) ? null : i; show(pinned); });
      el.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); pinned = (pinned === i) ? null : i; show(pinned); } });
      el.addEventListener('focus', function () { if (pinned === null) show(i); });
      el.addEventListener('blur', function () { if (pinned === null) show(null); });
    });
    return function () { pinned = null; };
  }
  function mark(root, i) {
    root.classList.toggle('has-on', i !== null);
    root.querySelectorAll('[data-i]').forEach(function (el) { el.classList.toggle('on', i !== null && +el.dataset.i === i); });
  }
  var NS = 'http://www.w3.org/2000/svg';
  function pie(root, D) {
    var tabs = root.querySelector('.cv-tabs'), svg = root.querySelector('.cv-pie'), side = root.querySelector('.cv-rows'), read = root.querySelector('.cv-read');
    function draw(v) {
      var V = D.views[v], tot = V.slices.reduce(function (s, x) { return s + x.v; }, 0), a = -Math.PI / 2, cx = 150, cy = 150, r = 140, r0 = 78;
      svg.innerHTML = ''; side.innerHTML = '';
      V.slices.forEach(function (s, i) {
        var sw = 2 * Math.PI * s.v / tot, a1 = a + sw, big = sw > Math.PI ? 1 : 0, m = a + sw / 2;
        var p = function (rr, ang) { return (cx + rr * Math.cos(ang)).toFixed(2) + ' ' + (cy + rr * Math.sin(ang)).toFixed(2); };
        var g = document.createElementNS(NS, 'g'); g.setAttribute('class', 'cv-s'); g.dataset.i = i;
        g.style.setProperty('--dx', (6 * Math.cos(m)).toFixed(2) + 'px'); g.style.setProperty('--dy', (6 * Math.sin(m)).toFixed(2) + 'px');
        var path = document.createElementNS(NS, 'path');
        path.setAttribute('d', 'M' + p(r, a) + ' A' + r + ' ' + r + ' 0 ' + big + ' 1 ' + p(r, a1) + ' L' + p(r0, a1) + ' A' + r0 + ' ' + r0 + ' 0 ' + big + ' 0 ' + p(r0, a) + ' Z');
        path.setAttribute('fill', s.c); g.appendChild(path);
        if (s.v / tot >= 0.12) {
          var t = document.createElementNS(NS, 'text'), rr = (r + r0) / 2;
          t.setAttribute('x', (cx + rr * Math.cos(m)).toFixed(1)); t.setAttribute('y', (cy + rr * Math.sin(m) + 5).toFixed(1));
          t.setAttribute('text-anchor', 'middle'); t.setAttribute('fill', '#fff'); t.setAttribute('font-size', '15'); t.setAttribute('font-weight', '800');
          t.textContent = pct(s.v, tot); g.appendChild(t);
        }
        svg.appendChild(g); a = a1;
        var row = document.createElement('div'); row.className = 'cv-row'; row.dataset.i = i; row.tabIndex = 0; row.setAttribute('role', 'button');
        row.setAttribute('aria-label', s.l + ': ' + fmtB(s.v) + ', ' + pct(s.v, tot));
        row.innerHTML = '<span class="cv-sw" style="background:' + s.c + '"></span><span>' + s.l + '</span><span class="cv-v">' + fmtB(s.v).replace(' billion', 'B') + '</span><span class="cv-p">' + pct(s.v, tot) + '</span>';
        side.appendChild(row);
      });
      var c1 = document.createElementNS(NS, 'text'), c2 = document.createElementNS(NS, 'text');
      [[c1, 142, 22, 800], [c2, 166, 12, 500]].forEach(function (q) { q[0].setAttribute('x', 150); q[0].setAttribute('y', q[1]); q[0].setAttribute('text-anchor', 'middle'); q[0].setAttribute('font-size', q[2]); q[0].setAttribute('font-weight', q[3]); q[0].setAttribute('fill', '#1c2a44'); svg.appendChild(q[0]); });
      function show(i) {
        mark(root, i);
        if (i === null) { c1.textContent = fmtT(tot / 1000); c2.textContent = 'total U.S. CRE'; read.innerHTML = V.rest; read.style.borderLeftColor = ''; return; }
        var s = V.slices[i]; c1.textContent = pct(s.v, tot); c2.textContent = s.l.toLowerCase();
        read.innerHTML = '<b>' + s.l + '</b>: ' + fmtB(s.v) + ', ' + pct(s.v, tot) + ' of the total. ' + (s.n || ''); read.style.borderLeftColor = s.c;
      }
      wire(root, Array.prototype.slice.call(root.querySelectorAll('[data-i]')), show); show(null);
    }
    D.views.forEach(function (V, v) {
      var b = document.createElement('button'); b.type = 'button'; b.textContent = V.name; b.setAttribute('aria-pressed', v === 0 ? 'true' : 'false');
      b.addEventListener('click', function () { tabs.querySelectorAll('button').forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); }); draw(v); });
      tabs.appendChild(b);
    });
    if (D.views.length < 2) tabs.remove();
    draw(0);
  }
  function bars(root, D) {
    var box = root.querySelector('.cv-rows'), read = root.querySelector('.cv-read'), tabs = root.querySelector('.cv-tabs');
    var max = Math.max.apply(null, D.items.map(function (x) { return x.v; })), tot = D.total || D.items.reduce(function (s, x) { return s + x.v; }, 0);
    D.items.forEach(function (x, i) {
      var row = document.createElement('div'); row.className = 'cv-bar'; row.dataset.i = i; row.dataset.g = x.g || ''; row.tabIndex = 0; row.setAttribute('role', 'button');
      var val = D.unit === 'T' ? '$' + x.v.toFixed(1) + 'T' : '$' + x.v.toLocaleString('en-US') + 'B';
      row.setAttribute('aria-label', x.l + ': ' + val);
      row.innerHTML = '<span class="cv-l">' + x.l + '</span><span class="cv-track"><span class="cv-fill" style="display:block;width:' + (100 * x.v / max).toFixed(1) + '%;background:' + x.c + '"></span></span><span class="cv-v">' + val + '</span>';
      box.appendChild(row);
    });
    function show(i) {
      mark(root, i);
      if (i === null) { read.innerHTML = D.rest; read.style.borderLeftColor = ''; return; }
      var x = D.items[i]; read.innerHTML = '<b>' + x.l + '</b>: ' + (D.unit === 'T' ? fmtT(x.v) : fmtB(x.v)) + (D.share ? ', ' + pct(x.v, tot) + ' of ' + D.share : '') + '. ' + (x.n || ''); read.style.borderLeftColor = x.c;
    }
    var reset = wire(root, Array.prototype.slice.call(box.children), show); show(null);
    if (D.filters) {
      D.filters.forEach(function (f, k) {
        var b = document.createElement('button'); b.type = 'button'; b.textContent = f.name; b.setAttribute('aria-pressed', k === 0 ? 'true' : 'false');
        b.addEventListener('click', function () {
          tabs.querySelectorAll('button').forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
          box.querySelectorAll('.cv-bar').forEach(function (r) { r.classList.toggle('hide', !!f.g && r.dataset.g !== f.g); });
          reset(); show(null); if (f.rest) read.innerHTML = f.rest;
        });
        tabs.appendChild(b);
      });
    } else if (tabs) tabs.remove();
  }
  function split(root, D) {
    var read = root.querySelector('.cv-read'), segs = Array.prototype.slice.call(root.querySelectorAll('.cv-seg'));
    function show(i) {
      mark(root, i);
      if (i === null) { read.innerHTML = D.rest; read.style.borderLeftColor = ''; return; }
      var x = D.items[i]; read.innerHTML = '<b>' + x.l + '</b>: ' + fmtB(x.v) + ', ' + pct(x.v, D.total) + ' of private CRE equity. ' + x.n; read.style.borderLeftColor = x.c;
    }
    wire(root, segs, show); show(null);
  }
  document.querySelectorAll('.crev[data-kind]').forEach(function (root) {
    try {
      var D = JSON.parse(root.querySelector('script[type="application/json"]').textContent);
      ({ pie: pie, bars: bars, split: split })[root.dataset.kind](root, D);
    } catch (e) { if (window.console) console.error('chart', root.id, e); }
  });
})();
</script>"""

def box(id_, kind, title, lede, data, inner, src="Exhibit data: Federal Reserve Flow of Funds and NAREIT, year-end 2024"):
    js = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    return (f'<div class="crev" id="{id_}" data-kind="{kind}">\n<p class="cv-title">{title}</p>\n<p class="cv-lede">{lede}</p>\n'
            f'{inner}\n<p class="cv-src">{src}</p>\n<script type="application/json">{js}</script>\n</div>')

BLUE, BLUE_D, ORANGE, ORANGE_D, GREY = "#4f92e3", "#1d4f94", "#ef8550", "#b8400f", "#9aa6b5"

def asset_classes():
    items = [("Corporate equities and mutual funds", 70.3), ("Owner-occupied housing", 48.1), ("U.S. Treasury securities", 28.1),
             ("Commercial real estate", 17.8), ("Corporate and foreign bonds", 16.1), ("Municipal securities", 4.2)]
    D = {"unit": "T", "items": [{"l": l, "v": v, "c": ORANGE_D if l.startswith("Commercial") else GREY,
                                 "n": "Investible CRE only: it leaves out property owned by governments and by companies outside real estate." if l.startswith("Commercial") else ""} for l, v in items],
         "rest": "<b>Commercial real estate</b> is a large market, about a quarter the size of the stock market. Hover over or tap a bar."}
    return box("cre-assets", "bars", "U.S. Asset Classes by Market Value", "Year-end 2024, in trillions of dollars (Exhibit 17-1).", D,
               '<div class="cv-rows"></div>\n<div class="cv-read" aria-live="polite"></div>')

def quadrants():
    PE, PD, UE, UD = 9654, 5278, 1461, 1454
    D = {"views": [
        {"name": "Four quadrants", "rest": "Hover over or tap a slice. <b>Private equity</b> is the largest quadrant by far; the two public quadrants are about 8% each.",
         "slices": [{"l": "Public equity", "v": UE, "c": BLUE, "n": "Mostly listed REITs."},
                    {"l": "Private equity", "v": PE, "c": BLUE_D, "n": "The largest category of CRE ownership."},
                    {"l": "Public debt", "v": UD, "c": ORANGE, "n": "CMBS and REIT unsecured debt."},
                    {"l": "Private debt", "v": PD, "c": ORANGE_D, "n": "Mortgages held by banks, life insurers and other lenders."}]},
        {"name": "Debt vs. equity", "rest": "About <b>38% debt and 62% equity</b>: on average, $0.38 of every dollar of CRE value is borrowed.",
         "slices": [{"l": "Equity", "v": PE + UE, "c": BLUE_D, "n": "Many owners, such as pension funds, hold properties free and clear."},
                    {"l": "Debt", "v": PD + UD, "c": ORANGE_D, "n": "The average loan-to-value ratio is about 38%."}]},
        {"name": "Private vs. public", "rest": "Most CRE capital, debt and equity alike, is held <b>privately</b> rather than traded on an exchange.",
         "slices": [{"l": "Private", "v": PE + PD, "c": "#34495e", "n": "Private equity plus private debt."},
                    {"l": "Public", "v": UE + UD, "c": "#9fb3c8", "n": "Public equity plus public debt."}]}]}
    assert PE + PD + UE + UD == 17847
    return box("cre-quadrants", "pie", "Who Finances U.S. Commercial Real Estate?", "$17.8 trillion of investible CRE, split three ways (Exhibit 17-2).", D,
               '<div class="cv-tabs" role="group" aria-label="View"></div>\n<div class="cv-body">\n<svg class="cv-pie" viewBox="-10 -10 320 320" role="img" aria-label="Pie chart of U.S. commercial real estate value: private equity $9,654 billion (54%), private debt $5,278 billion (30%), public equity $1,461 billion (8%), public debt $1,454 billion (8%)"></svg>\n<div class="cv-side"><div class="cv-rows"></div><div class="cv-read" aria-live="polite"></div></div>\n</div>')

def private_split():
    I, N = 2783, 6871; T = I + N; assert T == 9654
    D = {"total": T, "items": [{"l": "Institutional-quality properties", "v": I, "c": BLUE_D, "n": "Pension funds, foreign investors, life insurers, PERE funds, endowments and other large investors."},
                               {"l": "Non-institutional properties", "v": N, "c": BLUE, "n": "Owned mostly by the \"great investor masses\" through local LLC syndications."}],
         "rest": "Of <b>$9.65 trillion</b> in private CRE equity, less than a third is in institutional-quality property. Hover over or tap a segment."}
    segs = (f'<div class="cv-split"><div class="cv-seg" data-i="0" tabindex="0" role="button" style="flex:{I};background:{BLUE_D}">29%</div>'
            f'<div class="cv-seg" data-i="1" tabindex="0" role="button" style="flex:{N};background:{BLUE}">71%</div></div>'
            f'<div class="cv-key"><span style="--c:{BLUE_D}">Institutional quality ($2.78T)</span><span style="--c:{BLUE}">Non-institutional ($6.87T)</span></div>')
    return box("cre-private", "split", "Private CRE Equity by Property Quality", "Year-end 2024, in billions of dollars (Exhibit 17-3).", D,
               segs + '\n<div class="cv-read" aria-live="polite"></div>')

def debt_holders():
    items = [("Banks and savings associations", 3014, "pri", "The largest single holder: 57% of private and about 45% of all CRE debt."),
             ("Life insurance companies", 780, "pri", "Very active lenders; about 12% of all CRE debt."),
             ("GSEs (Fannie Mae and Freddie Mac)", 591, "pri", "Active multifamily lenders."),
             ("Non-government-backed CMBS", 514, "pub", "\"Private-label\" CMBS, typically issued by large banks."),
             ("Agency and GSE-backed CMBS", 473, "pub", "All multifamily."),
             ("Equity REIT unsecured debt", 467, "pub", "About one-third of public CRE debt."),
             ("Other", 371, "pri", ""),
             ("Federal, state and local governments", 210, "pri", ""),
             ("Mortgage REITs", 186, "pri", ""),
             ("Private debt funds", 112, "pri", "A fast-growing source of bridge loans for transitional properties."),
             ("Pension funds", 14, "pri", "")]
    assert sum(v for _, v, g, _ in items if g == "pri") == 5278 and sum(v for _, v, g, _ in items if g == "pub") == 1454
    D = {"unit": "B", "total": 6732, "share": "all CRE debt",
         "items": [{"l": l, "v": v, "g": g, "c": ORANGE_D if g == "pri" else ORANGE, "n": n} for l, v, g, n in items],
         "rest": "<b>$6.73 trillion</b> of CRE debt: 78% is held privately, 22% trades publicly. Hover over or tap a bar.",
         "filters": [{"name": "All holders", "g": ""},
                     {"name": "Private (78%)", "g": "pri", "rest": "<b>Private CRE debt: $5.28 trillion.</b> Banks and savings associations hold 57% of it."},
                     {"name": "Public (22%)", "g": "pub", "rest": "<b>Public CRE debt: $1.45 trillion.</b> CMBS make up about two-thirds; REIT unsecured bonds the rest."}]}
    key = f'<div class="cv-key"><span style="--c:{ORANGE_D}">Privately held</span><span style="--c:{ORANGE}">Publicly traded</span></div>'
    return box("cre-debt", "bars", "Who Holds U.S. Commercial Real Estate Debt?", "Investment holdings, not loan originations; year-end 2024, in billions of dollars (Exhibit 17-4).", D,
               '<div class="cv-tabs" role="group" aria-label="Filter"></div>\n<div class="cv-rows"></div>\n' + key + '\n<div class="cv-read" aria-live="polite"></div>')

def tree():
    return ('<div class="crev" id="cre-tree">\n<p class="cv-title">Where CRE Equity Fits in the Capital Markets</p>\n'
            '<p class="cv-lede">Commercial real estate is an alternative asset class, owned through private or public markets.</p>\n<div class="cv-tree"><ul>'
            '<li><span class="cv-node">Cash</span> <span class="cv-node">Bonds</span> <span class="cv-node">Stocks</span></li>'
            '<li><span class="cv-node">Alternatives</span><ul>'
            '<li><span class="cv-node hot">Commercial real estate</span><ul>'
            '<li><span class="cv-node warm">Private market <small>(85% to 90% of CRE equity)</small></span><ul>'
            '<li><span class="cv-node">Direct investment</span></li>'
            '<li><span class="cv-node">Through intermediaries</span><ul>'
            '<li><span class="cv-node">JVs, LLCs, etc.</span></li>'
            '<li><span class="cv-node">PERE funds</span><ul><li><span class="cv-node">Open-end funds</span></li><li><span class="cv-node">Closed-end funds</span></li></ul></li>'
            '</ul></li></ul></li>'
            '<li><span class="cv-node warm">Public market</span><ul><li><span class="cv-node">Listed REITs</span></li></ul></li>'
            '</ul></li>'
            '<li><span class="cv-node">Hedge funds</span></li><li><span class="cv-node">Infrastructure</span></li>'
            '</ul></li></ul></div>\n</div>')

def risk_return():
    """A ladder in HTML rather than a scaled drawing: on a phone a drawing's captions shrink to about 8px."""
    rungs = [("Opportunistic", "Development projects and distressed situations; required returns of 20% or more are possible.", "Closed-end", BLUE_D, 3),
             ("Value-added", "Properties that need renovation or re-leasing; intermediate risk and return.", "Closed-end", "#2f6fbf", 2),
             ("Core-plus", "Otherwise core properties with some added risk, such as higher vacancy or weaker tenants.", "", BLUE, 1),
             ("Core", "Stabilized, high-quality properties with strong leases in large metros; required returns of about 8% to 9%.", "Open-end", "#9fc3ef", 0)]
    rows = "".join(f'<div class="cv-rung" style="--k:{k};--c:{c}"><span class="cv-dot"></span><div><b>{n}</b>'
                   + (f' <span class="cv-tag">{tag} funds</span>' if tag else "") + f'<br><span class="cv-desc">{d}</span></div></div>' for n, d, tag, c, k in rungs)
    return ('<div class="crev" id="cre-risk">\n<p class="cv-title">Private Equity Real Estate Fund Strategies</p>\n<p class="cv-lede">Each step up the ladder takes on more risk for a higher expected return.</p>\n'
            f'<div class="cv-ladder"><div class="cv-axis"><span>More risk,<br>higher expected return</span></div><div class="cv-rungs">{rows}</div></div>\n</div>')

def lifecycle():
    phases = [("Fundraising", "about 1 year", "Investors commit capital between the first and final close.", "#5b6474", 1),
              ("Investment period", "often 2 to 3 years", "The manager issues capital calls and buys assets.", "#2f6fbf", 2.5),
              ("Harvesting period", "to the end of the fund's life", "Assets are operated, improved and sold; capital goes back to investors.", BLUE_D, 5)]
    cells = "".join(f'<div class="cv-step" style="border-top:4px solid {c}"><b>{n}</b><span style="color:#5b6474;font-size:.82rem">{d}</span><br>{t}</div>' for n, d, t, c, _ in phases)
    return ('<div class="crev" id="cre-life">\n<p class="cv-title">Life Cycle of a Closed-End PERE Fund</p>\n<p class="cv-lede">A finite life of 7 to 10 years, which the manager may extend by a year or two.</p>\n'
            f'<div class="cv-steps">{cells}</div>\n</div>')

def waterfall():
    steps = [("1", "Return of capital", "100% of distributable cash goes to the limited partners until their contributed equity is returned.", [("LPs 100%", 1, BLUE_D)]),
             ("2", "Preferred return", "Still 100% to the limited partners, until their cumulative IRR reaches the preferred return (commonly 7% to 8%).", [("LPs 100%", 1, BLUE_D)]),
             ("3", "Carried interest", "Remaining cash is split, often 80% to the limited partners and 20% to the general partner.", [("LPs 80%", 80, BLUE_D), ("GP 20%", 20, ORANGE_D)])]
    cells = ""
    for n, h, t, segs in steps:
        bar = "".join(f'<div class="cv-seg" style="flex:{w};background:{c}">{l}</div>' for l, w, c in segs)
        cells += f'<div class="cv-step"><span class="cv-n">{n}</span><b>{h}</b>{t}<div class="cv-split">{bar}</div></div>'
    return ('<div class="crev" id="cre-waterfall">\n<p class="cv-title">A Standard Distribution Waterfall</p>\n<p class="cv-lede">Each tier is paid in full before cash flows to the next.</p>\n'
            f'<div class="cv-steps">{cells}</div>\n</div>')

def charts(t):
    t = normal(t)
    first = True
    def put(t, anchor, html, what, after=True):
        nonlocal first
        block = (CSS + "\n" if first else "") + html; first = False
        i = t.index(anchor) if t.count(anchor) == 1 else None
        assert i is not None, (what, t.count(anchor))
        j = i + len(anchor) if after else i
        return t[:j] + "\n\n" + block + "\n\n" + t[j:]
    t = put(t, "because they are not available for investors to purchase.</p>", asset_classes(), "assets")
    t = put(t, "<li>8% in publicly traded mortgage debt</li>\n</ul>", quadrants(), "quadrants")
    t = put(t, "are held by vehicles that do not trade on a stock exchange.</p>", tree(), "tree")
    t = put(t, "<h4>Life-Cycle of a Closed-End Fund</h4>", "", "noop") if False else t
    i = t.index("<h4>Life-Cycle of a Closed-End Fund</h4>"); j = t.index("</div>", i) + 6
    t = t[:j] + "\n\n" + lifecycle() + "\n" + t[j:]
    t = put(t, "The general partner's share is disproportionate to its small equity co-investment by design—tying general partner pay to performance.</p>", waterfall(), "waterfall")
    t = put(t, "Their investments include development projects and distressed situations.</li>\n        </ul>", risk_return(), "risk")
    t = put(t, "or non-institutional quality properties:</p>", private_split(), "private")
    i = t.index("<h4>EXAM TIP: Commercial Debt Structure</h4>"); j = t.index("</div>", i) + 6
    t = t[:j] + "\n\n" + debt_holders() + "\n" + t[j:]
    t = sub1(t, "</body>", RUNTIME + "\n</body>", "runtime")
    return t

def build(src, outdir):
    t = open(src, encoding="utf-8").read()
    for sub, fn in (("Normal", normal), ("Charts", charts)):
        d = os.path.join(outdir, f"REE3043-Ch17-{sub}"); os.makedirs(d, exist_ok=True)
        p = os.path.join(d, "REE3043-Fall26-Chapter17-Full.html"); open(p, "w", encoding="utf-8").write(fn(t)); print("wrote", p)

if __name__ == "__main__":
    build(*sys.argv[1:3])
