"""MAR3023 Fall '26, Exam 3, Chapter 22: the PERT chart image as an interactive chart, in all three editions.

    python scripts/mar3023/chapter22_pert.py FULL BALANCED CONCISE OUTDIR

The chart is the source figure redrawn: six milestones, durations in months on the arrows, the critical path
in the figure's teal. One button per path highlights it and adds up its months. The prose around it lists the
paths and explains the critical path, so the widget only shows and sums; it does not explain again.
"""
import json, os, sys

IMG = "https://smokinnotes.s3.us-east-1.amazonaws.com/public/mar3023-253-exam3-chapter22-01-pert-chart-diagram.png"
NODES = {"A": "Prototype", "B": "Market\nResearch", "C": "Build\nProduction\nFacility", "D": "Develop Ad\nCampaign",
         "E": "Redesign\nProduct", "F": "Launch"}
EDGES = [("A", "B", 5), ("A", "C", 7), ("B", "D", 5), ("B", "E", 2), ("C", "E", 4), ("D", "F", 2), ("E", "F", 4)]


def paths(n="A"):
    nxt = [b for a, b, _ in EDGES if a == n]
    return [[n]] if not nxt else [[n] + p for b in nxt for p in paths(b)]


DUR = {(a, b): d for a, b, d in EDGES}
PATHS = [(p, sum(DUR[(p[i], p[i + 1])] for i in range(len(p) - 1))) for p in paths()]
# the notes: A-B-D-F 12, A-B-E-F 11, A-C-E-F 15 (critical)
assert {"".join(p): t for p, t in PATHS} == {"ABDF": 12, "ABEF": 11, "ACEF": 15}, PATHS
CRIT = max(PATHS, key=lambda x: x[1])
assert "".join(CRIT[0]) == "ACEF" and CRIT[1] == 15

# two layouts: across (wide screens) and down (phones). x, y, label side; edge label side per layout
LAYOUT = {
    "h": {"w": 660, "h": 326, "R": 25,
          "n": {"A": [62, 165, "below"], "B": [240, 82, "above"], "C": [240, 228, "below"], "D": [440, 82, "above"],
                "E": [440, 228, "below"], "F": [600, 165, "below"]},
          "e": {"AB": -1, "AC": 1, "BD": -1, "BE": -1, "CE": -1, "DF": -1, "EF": -1}},
    "v": {"w": 392, "h": 590, "R": 25,
          "n": {"A": [196, 46, "right"], "B": [116, 196, "left"], "C": [276, 196, "right"], "D": [116, 380, "left"],
                "E": [276, 380, "right"], "F": [196, 530, "right"]},
          "e": {"AB": 1, "AC": -1, "BD": 1, "BE": -1, "CE": -1, "DF": 1, "EF": -1}},
}


def model():
    views = [{"label": "Whole chart", "path": [], "crit": False, "whole": True,
              "cap": "All three paths from prototype (A) to launch (F)."}]
    order = sorted(PATHS, key=lambda x: "".join(x[0]))
    for p, t in order:
        crit = p == CRIT[0]
        steps = " + ".join(str(DUR[(p[i], p[i + 1])]) for i in range(len(p) - 1))
        views.append({"label": " → ".join(p), "path": p, "crit": crit,
                      "cap": f"<b>{' → '.join(p)}:</b> {steps} = <b>{t} months</b>" + (" (the critical path)" if crit else "")})
    start = 0   # opens on the whole chart; the critical path shows only when its button is pressed
    return {"nodes": NODES, "edges": [[a, b, d, a + b in {"AC", "CE", "EF"}] for a, b, d in EDGES], "layout": LAYOUT,
            "views": views, "start": start}


CSS = r"""<style>
.pertw { --ink:#1c2a44; --muted:#5b6474; --rule:#cfd6e2; --soft:#f1f4f9; --crit:#0e6f73; --node:#d9f5f5; --node-rule:#8fcfd1; --sel:#2a78d6;
  max-width:760px; margin:20px auto; padding:14px 16px 12px; background:#fff; border:1px solid #dfe3ea; border-radius:10px;
  box-sizing:border-box; font-family:"Red Hat Display", system-ui, sans-serif; color:var(--ink); clear:both; }
.pertw * { box-sizing:border-box; }
.pertw .pt-title { font-weight:800; font-size:1.02rem; margin:0 0 8px; text-align:center; }
.pertw .pt-bar { display:flex; flex-wrap:wrap; justify-content:center; gap:6px; margin:0 0 8px; }
.pertw button { font:inherit; font-size:.85rem; font-weight:700; min-height:40px; padding:6px 14px; border:1px solid var(--rule);
  border-radius:999px; background:#fff; color:var(--ink); cursor:pointer; }
.pertw button.crit { border-color:var(--crit); color:var(--crit); }
.pertw button[aria-pressed="true"] { background:var(--sel); border-color:var(--sel); color:#fff; }
.pertw button.crit[aria-pressed="true"] { background:var(--crit); border-color:var(--crit); }
.pertw button:focus-visible { outline:3px solid #2a78d6; outline-offset:2px; }
.pertw .pt-caps { display:grid; margin:0 0 6px; }
.pertw .pt-cap { grid-area:1 / 1; visibility:hidden; padding:7px 12px; border-left:4px solid var(--sel); background:var(--soft);
  border-radius:0 6px 6px 0; font-size:.92rem; text-align:left; }
.pertw .pt-cap.crit { border-left-color:var(--crit); } .pertw .pt-cap.whole { border-left-color:var(--rule); }
.pertw button.whole[aria-pressed="true"] { background:var(--ink); border-color:var(--ink); }
.pertw .pt-cap.on { visibility:visible; }
.pertw svg { display:block; width:100%; height:auto; margin:0 auto; }
.pertw svg text { font-family:"Red Hat Display", system-ui, sans-serif; }
.pertw .nd circle { fill:var(--node); stroke:var(--node-rule); stroke-width:1.5; }
.pertw .nd.on circle { stroke:var(--sel); stroke-width:3; } .pertw .nd.on.crit circle { stroke:var(--crit); }
.pertw .nd .id { font-size:19px; font-weight:800; fill:var(--ink); text-anchor:middle; dominant-baseline:central; }
.pertw .nd .nm { font-size:13px; font-weight:800; fill:var(--ink); }
.pertw .ed line { stroke:#5fa9ad; stroke-width:1.6; } .pertw .ed polygon { fill:#5fa9ad; }
.pertw .ed .du { font-size:16px; font-weight:700; fill:#3f9ca1; text-anchor:middle; dominant-baseline:central; }
.pertw .ed.cp line { stroke:var(--crit); stroke-width:5; } .pertw .ed.cp polygon { fill:var(--crit); } .pertw .ed.cp .du { fill:var(--crit); }
.pertw .ed.on line { stroke:var(--sel); stroke-width:5; } .pertw .ed.on polygon { fill:var(--sel); } .pertw .ed.on .du { fill:var(--sel); font-weight:800; }
.pertw .ed.on.cp line { stroke:var(--crit); } .pertw .ed.on.cp polygon { fill:var(--crit); } .pertw .ed.on.cp .du { fill:var(--crit); }
.pertw .ed.off { opacity:.35; } .pertw .nd.off { opacity:.45; }
.pertw .time line { stroke:#6b7f78; stroke-width:1.5; } .pertw .time polygon { fill:#6b7f78; } .pertw .time text { font-size:12px; font-weight:700; fill:#6b7f78; }
.pertw .pt-key { display:flex; justify-content:center; gap:16px; flex-wrap:wrap; margin:6px 0 0; font-size:.78rem; color:var(--muted); }
.pertw .pt-key i { display:inline-block; width:22px; border-top:5px solid; vertical-align:middle; margin-right:6px; border-radius:3px; }
@media (max-width:600px) { .pertw { padding:12px 8px; } .pertw button { padding:6px 10px; font-size:.8rem; } }
@media (max-width:600px) { table { display:block; overflow-x:auto !important; -webkit-overflow-scrolling:touch; }
  mjx-container { display:inline-block !important; max-width:100%; overflow-x:auto; overflow-y:hidden; vertical-align:middle; }
  li, p { overflow-wrap:break-word; } }
</style>"""

RUNTIME = r"""<script>
(function () {
  var NS = 'http://www.w3.org/2000/svg';
  function E(t, a, p) { var e = document.createElementNS(NS, t); for (var k in a) e.setAttribute(k, a[k]); if (p) p.appendChild(e); return e; }
  function r1(n) { return Math.round(n * 10) / 10; }
  function draw(fig, M, v) {
    var L = M.layout[fig.clientWidth < 540 ? 'v' : 'h'], R = L.R, P = L.n, on = {}, onN = {};
    for (var i = 0; i < v.path.length; i++) { onN[v.path[i]] = 1; if (i) on[v.path[i - 1] + v.path[i]] = 1; }
    fig.innerHTML = '';
    var svg = E('svg', { viewBox: '0 0 ' + L.w + ' ' + L.h, role: 'img', 'aria-label': 'PERT chart, path ' + v.label + ' highlighted' }, fig);
    svg.style.maxWidth = L.w + 'px';
    if (L === M.layout.h) {   /* the source's time arrow along the bottom */
      var tg = E('g', { 'class': 'time' }, svg), ty = L.h - 12;
      E('line', { x1: 30, y1: ty, x2: L.w - 30, y2: ty }, tg);
      E('polygon', { points: (L.w - 22) + ',' + ty + ' ' + (L.w - 34) + ',' + (ty - 5) + ' ' + (L.w - 34) + ',' + (ty + 5) }, tg);
      var tt = E('text', { x: L.w - 40, y: ty - 7, 'text-anchor': 'end' }, tg); tt.textContent = 'Time';
    }
    M.edges.forEach(function (e) {
      var a = P[e[0]], b = P[e[1]], k = e[0] + e[1], dx = b[0] - a[0], dy = b[1] - a[1], d = Math.sqrt(dx * dx + dy * dy), ux = dx / d, uy = dy / d;
      var whole = !v.path.length, cp = e[3] && v.crit;
      var cls = 'ed' + (cp ? ' cp' : '') + (whole ? '' : on[k] ? ' on' : ' off'), g = E('g', { 'class': cls }, svg), thick = !whole && on[k];
      var hl = thick ? 13 : 9, hw = thick ? 7 : 4.5, sx = a[0] + ux * (R + 2), sy = a[1] + uy * (R + 2), tx = b[0] - ux * (R + 3), ty2 = b[1] - uy * (R + 3), bx = tx - ux * hl, by = ty2 - uy * hl;
      E('line', { x1: r1(sx), y1: r1(sy), x2: r1(bx + ux), y2: r1(by + uy) }, g);
      E('polygon', { points: [r1(tx) + ',' + r1(ty2), r1(bx - uy * hw) + ',' + r1(by + ux * hw), r1(bx + uy * hw) + ',' + r1(by - ux * hw)].join(' ') }, g);
      var s = L.e[k], mx = (sx + tx) / 2 - uy * 14 * s, my = (sy + ty2) / 2 + ux * 14 * s;
      var t = E('text', { x: r1(mx), y: r1(my), 'class': 'du' }, g); t.textContent = e[2];
    });
    Object.keys(P).forEach(function (id) {
      var p = P[id], g = E('g', { 'class': 'nd' + (!v.path.length ? '' : onN[id] ? ' on' : ' off') + (v.crit ? ' crit' : ''), transform: 'translate(' + p[0] + ',' + p[1] + ')' }, svg);
      E('circle', { r: R }, g); var t = E('text', { x: 0, y: 0, 'class': 'id' }, g); t.textContent = id;
      var lines = M.nodes[id].split('\n'), lh = 15, side = p[2], x = 0, y, anc = 'middle';
      if (side === 'below') y = R + 15;
      else if (side === 'above') y = -R - 9 - (lines.length - 1) * lh;
      else { x = side === 'left' ? -R - 8 : R + 8; anc = side === 'left' ? 'end' : 'start'; y = -(lines.length - 1) * lh / 2 + 4; }
      var nm = E('text', { x: x, y: y, 'class': 'nm', 'text-anchor': anc }, g);
      lines.forEach(function (ln, i) { var s = E('tspan', { x: x, dy: i ? lh : 0 }, nm); s.textContent = ln; });
    });
  }
  function boot(w) {
    if (w.dataset.ready) return; w.dataset.ready = '1';
    var M = JSON.parse(w.querySelector('script[type="application/json"]').textContent), body = w.querySelector('.pt-body');
    var bar = document.createElement('div'); bar.className = 'pt-bar'; bar.setAttribute('role', 'group'); body.appendChild(bar);
    var caps = document.createElement('div'); caps.className = 'pt-caps'; caps.setAttribute('aria-live', 'polite'); body.appendChild(caps);
    var fig = document.createElement('div'); body.appendChild(fig);
    var key = document.createElement('div'); key.className = 'pt-key'; key.innerHTML = '<span><i style="color:var(--crit)"></i>Critical path</span><span><i style="color:var(--sel)"></i>Selected path</span>'; body.appendChild(key);
    var cur = M.start, btns = [], cs = [];
    M.views.forEach(function (v, i) {
      var b = document.createElement('button'); b.type = 'button'; b.textContent = v.label; if (v.crit) b.className = 'crit'; if (v.whole) b.className = 'whole';
      b.onclick = function () { set(i); }; bar.appendChild(b); btns.push(b);
      var c = document.createElement('div'); c.className = 'pt-cap' + (v.crit ? ' crit' : '') + (v.whole ? ' whole' : ''); c.innerHTML = v.cap; caps.appendChild(c); cs.push(c);
    });
    function set(i) { cur = i; btns.forEach(function (b, j) { b.setAttribute('aria-pressed', i === j ? 'true' : 'false'); }); cs.forEach(function (c, j) { c.classList.toggle('on', i === j); }); draw(fig, M, M.views[i]); }
    set(cur);
    var lastW = fig.clientWidth;
    if (window.ResizeObserver) new ResizeObserver(function () { if (Math.abs(fig.clientWidth - lastW) > 4) { lastW = fig.clientWidth; draw(fig, M, M.views[cur]); } }).observe(fig);
  }
  function all() { Array.prototype.forEach.call(document.querySelectorAll('.pertw'), function (w) { try { boot(w); } catch (e) { if (window.console) console.error(e); } }); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', all); else all();
})();
</script>"""


def widget():
    js = json.dumps(model(), ensure_ascii=False).replace("</", "<\\/")
    return (f'<div class="pertw">\n<p class="pt-title">PERT Chart: New Product Launch</p>\n<div class="pt-body"></div>\n'
            f'<noscript><img src="{IMG}" alt="PERT chart: prototype (A) to launch (F), critical path A to C to E to F" '
            f'class="image-wide-70 content-image"></noscript>\n<script type="application/json">{js}</script>\n</div>')


def swap(t, old, new):
    assert t.count(old) == 1, (old[:70], t.count(old)); return t.replace(old, new)


def edition(src, kind):
    t = open(src, encoding="utf-8").read()
    if kind in ("Full", "Balanced"):
        a = t.index(f'<img src="{IMG}"'); b = t.index("/>", a) + 2
        t = t[:a] + widget() + t[b:]
        if kind == "Full":
            t = swap(t, "In the PERT chart on the previous page,", "In the PERT chart above,")
    else:   # Concise: the path list below names letters from a chart the edition never shows, so the chart goes above it
        t = swap(t, "<h3>PERT Chart Example:</h3>\n", "<h3>PERT Chart Example:</h3>\n\n" + widget() + "\n")
    t = t.replace("</head>", CSS + "\n</head>", 1)
    t = t.replace("</body>", RUNTIME + "\n</body>", 1)
    assert t.count('class="pertw"') == 1 and t.count(f'<img src="{IMG}"') == 1   # only the noscript copy remains
    return t


if __name__ == "__main__":
    full, bal, con, out = sys.argv[1:5]; os.makedirs(out, exist_ok=True)
    for src, kind in ((full, "Full"), (bal, "Balanced"), (con, "Concise")):
        p = os.path.join(out, f"MAR3023-Fall26-Exam3-Chapter22-{kind}.html")
        open(p, "w", encoding="utf-8").write(edition(src, kind)); print("wrote", p)
    print("checks passed: paths 12, 11, 15; critical path A-C-E-F")
