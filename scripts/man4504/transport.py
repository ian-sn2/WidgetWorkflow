"""MAN4504 Exam 3, Aggregate Planning: the transportation-method example as an interactive table, 2026-11-11.

Ian's readme: the nine table images make the section very long; replace them with a step-by-step widget,
one or two options, and make sure every number is right. Two options, each written as a whole chapter:

  A  stepper  - one table that fills in as the reader presses Next: layout, costs column by column,
                then the cheapest-first allocation one source at a time, and the dummy column
  B  explorer - the finished table with tabs: how each cost is built, how each column is filled
                (a ranked list of sources), and a "read the plan" mode for the row/column exam questions

Every number is computed here from the example's givens and asserted against what the notes print, so the
widget cannot drift from the prose. The section's prose that only narrated the images moves into the widget.

    python scripts/man4504/transport.py SRC.html OUTDIR
"""
import sys, os, json, html

# ---------------------------------------------------------------- the example, from the notes
CARRY = 2
ROWS = [  # id, period, source, capacity, base cost, period index (inventory is on hand at the start of March)
    ("inv", "", "Beginning inventory", 100, 0, 0),
    ("mR", "March", "Regular", 700, 40, 0), ("mO", "March", "Overtime", 50, 50, 0), ("mS", "March", "Subcontract", 150, 70, 0),
    ("aR", "April", "Regular", 700, 40, 1), ("aO", "April", "Overtime", 50, 50, 1), ("aS", "April", "Subcontract", 150, 70, 1),
    ("yR", "May", "Regular", 700, 40, 2), ("yO", "May", "Overtime", 50, 50, 2), ("yS", "May", "Subcontract", 130, 70, 2)]
COLS = [("mar", "March", 800, 0), ("apr", "April", 1000, 1), ("may", "May", 750, 2)]
DUMMY = ("dum", "Unused capacity (dummy)", None, None)

def cost(r, c):
    """None where back-ordering would be needed (demand before production)."""
    if c[0] == "dum": return 0
    return None if c[3] < r[5] else r[4] + CARRY * (c[3] - r[5])

def name(r): return "Beginning inventory" if r[0] == "inv" else f"{r[1]} {r[2].lower()}"

def held(r, c):
    """the source's name, saying so when it is an earlier month's production carried forward"""
    m = c[3] - r[5]
    if r[0] == "inv" and m == 0: return name(r)
    return name(r) + (f" (held {m} month{'s' if m > 1 else ''})" if m else "")

def solve():
    left = {r[0]: r[3] for r in ROWS}; alloc = {}; log = []
    for c in COLS:
        need = c[2]
        for r in sorted((r for r in ROWS if cost(r, c) is not None), key=lambda r: cost(r, c)):
            if need == 0: break
            q = min(left[r[0]], need)
            if q:
                alloc[(r[0], c[0])] = q; left[r[0]] -= q; need -= q; log.append((c, r, q, cost(r, c), need))
        assert need == 0, c
    dummy = {r[0]: left[r[0]] for r in ROWS if left[r[0]]}
    for k, q in dummy.items(): alloc[(k, "dum")] = q
    return alloc, log, dummy

ALLOC, LOG, DUMMY_FILL = solve()
TOTAL_D = sum(c[2] for c in COLS); TOTAL_CAP = sum(r[3] for r in ROWS if r[0] != "inv"); INV = ROWS[0][3]
DUMMY_UNITS = TOTAL_CAP + INV - TOTAL_D
TOTAL_COST = sum(q * cost(next(r for r in ROWS if r[0] == rk), next(c for c in COLS + [DUMMY] if c[0] == ck)) for (rk, ck), q in ALLOC.items())
# the notes' own numbers
assert (TOTAL_D, TOTAL_CAP, DUMMY_UNITS) == (2550, 2680, 230)
assert ALLOC == {("inv", "mar"): 100, ("mR", "mar"): 700, ("aR", "apr"): 700, ("aO", "apr"): 50, ("mO", "apr"): 50, ("aS", "apr"): 150,
                 ("mS", "apr"): 50, ("yR", "may"): 700, ("yO", "may"): 50, ("mS", "dum"): 100, ("yS", "dum"): 130}, ALLOC
assert TOTAL_COST == 105700
assert [cost(ROWS[k], COLS[2]) for k in (0, 1, 2, 3, 4)] == [4, 44, 54, 74, 42]
assert sum(ALLOC.get((r, "apr"), 0) for r in ("mS", "aS")) == 200 and sum(ALLOC.get(("mO", c), 0) for c in ("mar", "apr", "may")) == 50   # the notes' two reading examples

def money(n): return f"${n:,}"

def cost_terms():
    """Each filled cell's units and unit cost, in the notes' order: row by row, then month by month."""
    order = [r[0] for r in ROWS]; cols = [c[0] for c in COLS]
    keys = sorted((k for k in ALLOC if k[1] != "dum"), key=lambda k: (order.index(k[0]), cols.index(k[1])))
    return [(ALLOC[k], cost(next(r for r in ROWS if r[0] == k[0]), next(c for c in COLS if c[0] == k[1]))) for k in keys]

# the notes print the sum as 100(0)+700(40)+50(52)+50(72)+700(40)+50(50)+150(70)+700(40)+50(50)
assert cost_terms() == [(100, 0), (700, 40), (50, 52), (50, 72), (700, 40), (50, 50), (150, 70), (700, 40), (50, 50)], cost_terms()

# ---------------------------------------------------------------- option A: the stepper's states
def states():
    S = []; costs = set(); alloc = {}; left = {r[0]: r[3] for r in ROWS}; dleft = {c[0]: c[2] for c in COLS + [DUMMY] if c[2]}; dleft["dum"] = DUMMY_UNITS
    done = set()
    def push(title, text, hi=(), hirows=(), hicols=()):
        S.append({"title": title, "text": text, "costs": sorted(costs), "alloc": {f"{k[0]}|{k[1]}": v for k, v in alloc.items()},
                  "left": dict(left), "dleft": dict(dleft), "done": sorted(done), "hi": [f"{a}|{b}" for a, b in hi], "hirows": list(hirows), "hicols": list(hicols)})
    push("Set up the table",
         f"Demand periods run across the top and sources of supply down the side. Total demand is 800 + 1,000 + 750 = <b>2,550</b>. "
         f"Capacity is (700 + 50 + 150) + (700 + 50 + 150) + (700 + 50 + 130) = <b>2,680</b>, plus <b>100</b> units of beginning inventory. "
         f"A dummy column for unused capacity takes the <b>{DUMMY_UNITS}</b> extra units so that supply equals demand. With no back-ordering, "
         "a period's production cannot meet an earlier period's demand, so those cells are blacked out.", hicols=["dum"])
    costs.add("mar"); push("Costs: March demand",
         "Meeting March demand costs only the source's own price: <b>$0</b> from beginning inventory, <b>$40</b> on regular time, <b>$50</b> on overtime, <b>$70</b> subcontracted.", hicols=["mar"])
    costs.add("apr"); push("Costs: April demand",
         "April production meeting April demand costs the same base prices. Beginning inventory and March production held until April add the <b>$2</b> carrying cost: $2, $42, $52 and $72.", hicols=["apr"])
    costs.add("may"); costs.add("dum"); push("Costs: May demand and unused capacity",
         "May production costs its base price; April production held one month adds <b>$2</b>; inventory and March production held two months add <b>$4</b>. "
         "The dummy column costs <b>$0</b>: unused capacity is never produced.", hicols=["may", "dum"])
    for c in COLS:
        steps = [x for x in LOG if x[0] is c]
        cands = sorted((r for r in ROWS if cost(r, c) is not None and left[r[0]]), key=lambda r: cost(r, c))
        menu = ("Sources that can still supply " + c[1] + ", cheapest first, including earlier months' production held in inventory: "
                + ", ".join(f"{held(r, c)} ${cost(r, c)}" for r in cands) + ". ")
        for k, (cc, r, q, unit, need) in enumerate(steps):
            alloc[(r[0], c[0])] = q; left[r[0]] -= q; dleft[c[0]] -= q
            first = ("Fill each demand column from left to right, always from the cheapest source with capacity left. " if c[0] == "mar" else "") + menu if k == 0 else ""
            more = (f"<b>{need:,}</b> units of {c[1]} demand still to fill." if need else f"{c[1]} demand is met.")
            part = f" Only {q:,} of its {r[3]:,} units are needed, so {left[r[0]]:,} stay available." if left[r[0]] and q < r[3] else ""
            push(f"{c[1]}: {held(r, c)}", f"{first}Next cheapest source with units left: <b>{held(r, c)}</b> at <b>${unit}</b>. Take <b>{q:,}</b> units.{part} {more}",
                 hi=[(r[0], c[0])], hirows=[r[0]], hicols=[c[0]])
        done.add(c[0])
    for rk, q in DUMMY_FILL.items():
        alloc[(rk, "dum")] = q; left[rk] -= q; dleft["dum"] -= q
    done.add("dum")
    push("Unused capacity",
         "Every month's demand is met. The capacity nobody used goes to the dummy column: <b>100</b> units of March subcontracting and <b>130</b> of May subcontracting, "
         f"{DUMMY_UNITS} in all. Supply and demand now balance.", hi=[(k, "dum") for k in DUMMY_FILL], hicols=["dum"])
    # the total cost and how to read the plan are the prose right after the widget, so the widget stops here
    return S

# ---------------------------------------------------------------- option B: the explorer's text
def explorer_data():
    why = {}
    for r in ROWS:
        for c in COLS + [DUMMY]:
            u = cost(r, c)
            if u is None: continue
            if c[0] == "dum": t = "Unused capacity costs nothing: it is never produced."
            elif c[3] == r[5]: t = f"{name(r)} meets {c[1]} demand with no holding: {money(r[4])}." if r[0] != "inv" else "Inventory on hand meets March demand at no cost."
            else:
                m = c[3] - r[5]
                t = f"{money(r[4])} to produce{' (already on hand)' if r[0] == 'inv' else ''} + {m} month{'s' if m > 1 else ''} × $2 carrying = {money(u)}."
            why[f"{r[0]}|{c[0]}"] = f"<b>{name(r)} → {c[1]}:</b> {t}"
    fills = {}
    for c in COLS:
        rows = []
        for cc, r, q, unit, need in [x for x in LOG if x[0] is c]:
            rows.append([held(r, c), unit, q, need])
        fills[c[0]] = rows
    return {"why": why, "fills": fills, "dummy": [[name(next(r for r in ROWS if r[0] == k)), q] for k, q in DUMMY_FILL.items()]}

# ---------------------------------------------------------------- the widget
CSS = r"""<style>
.tpw { --ink:#1c2a44; --muted:#5b6474; --rule:#cfd6e2; --soft:#f1f4f9; --hi:#fff4c2; --blue:#1d4f94; max-width:760px; margin:20px auto; padding:16px 16px 14px; background:#fff; border:1px solid #dfe3ea; border-radius:10px; box-sizing:border-box; font-family:"Red Hat Display", system-ui, sans-serif; color:var(--ink); clear:both; }
.tpw * { box-sizing:border-box; }
.tpw .tp-title { font-weight:800; font-size:1.02rem; margin:0 0 2px; text-align:center; }
.tpw .tp-lede { font-size:.85rem; color:var(--muted); margin:0 0 10px; text-align:center; }
.tpw .tp-bar { display:flex; flex-wrap:wrap; align-items:center; justify-content:center; gap:6px; margin:0 0 8px; }
.tpw button { font:inherit; font-size:.85rem; font-weight:700; min-height:40px; padding:6px 14px; border:1px solid var(--rule); border-radius:999px; background:#fff; color:var(--ink); cursor:pointer; }
.tpw button[aria-pressed="true"], .tpw button.tp-next { background:var(--ink); border-color:var(--ink); color:#fff; }
.tpw button:disabled { opacity:.4; cursor:default; }
.tpw button:focus-visible { outline:3px solid #2a78d6; outline-offset:2px; }
.tpw .tp-count { font-size:.8rem; color:var(--muted); min-width:6.5em; text-align:center; }
.tpw .tp-cap { margin:0 0 10px; padding:8px 12px; border-left:4px solid var(--blue); background:var(--soft); border-radius:0 6px 6px 0; font-size:.9rem; line-height:1.45; min-height:4.4em; }
.tpw .tp-cap b.tp-h { display:block; font-size:.92rem; margin-bottom:2px; }
.tpw .tp-scroll { overflow-x:auto; -webkit-overflow-scrolling:touch; }
.tpw table.tp { border-collapse:separate; border-spacing:0; margin:0 auto; font-size:.82rem; font-variant-numeric:tabular-nums; width:100%; min-width:430px; background:transparent; }
.tpw table.tp th, .tpw table.tp td, .tpw table.tp tr { padding:0 !important; border:0 !important; background:transparent !important; color:var(--ink) !important; text-align:center; vertical-align:middle; box-shadow:none !important; }
.tpw table.tp tr:nth-child(even) td, .tpw table.tp tr:nth-child(odd) td, .tpw table.tp td:first-child, .tpw table.tp th:first-child { background:transparent !important; font-weight:inherit; }
.tpw table.tp thead th { font-weight:800 !important; font-size:.8rem; padding:4px 2px 6px !important; line-height:1.15; }
.tpw table.tp thead th.tp-sub { font-weight:600 !important; font-size:.72rem; color:var(--muted) !important; }
.tpw table.tp .tp-rl { text-align:left !important; padding:0 6px 0 0 !important; white-space:nowrap; font-weight:600 !important; font-size:.8rem; }
.tpw .tp-per { display:inline-block; min-width:3.1em; margin-right:4px; padding:1px 5px; border-radius:4px; font-size:.68rem; font-weight:800; color:#fff; background:#5b6474; text-align:center; }
.tpw .tp-per.p0 { background:#1c2a44; } .tpw .tp-per.p1 { background:#2f6fbf; } .tpw .tp-per.p2 { background:#5b6474; }
.tpw table.tp td.tp-c { position:relative; height:44px; min-width:62px; border:1px solid var(--rule) !important; background:#fff !important; transition:background .2s; }
.tpw td.tp-c .tp-u { position:absolute; top:0; right:0; min-width:24px; padding:1px 4px; border-left:1px solid var(--rule); border-bottom:1px solid var(--rule); font-size:.7rem; font-weight:700; color:var(--ink); background:#fff; line-height:1.3; }
.tpw td.tp-c .tp-u.off { visibility:hidden; }
.tpw td.tp-c .tp-q { position:absolute; left:6px; bottom:3px; font-size:.95rem; font-weight:800; }
.tpw td.tp-c .tp-q.dash { color:#aab3c2; font-weight:600; }
.tpw table.tp tr td.tp-x.tp-x { background:#2b343c !important; border:1px solid #2b343c !important; }
.tpw table.tp tr td.tp-x.tp-note { color:#fff !important; font-size:.68rem; font-weight:600; line-height:1.25; padding:6px !important; }
.tpw table.tp td.tp-c.col { background:#eef4fd !important; }
.tpw table.tp tr.rowhi td.tp-c { background:#eef4fd !important; }
.tpw table.tp td.tp-c.hi { background:var(--hi) !important; }
.tpw table.tp td.tp-cap, .tpw table.tp td.tp-dem { font-weight:800 !important; font-size:.86rem; padding:0 4px !important; white-space:nowrap; }
.tpw table.tp td.tp-dem { padding-top:6px !important; }
.tpw s { color:#9aa3b2; font-weight:600; margin-right:3px; }
.tpw .tp-done { color:#9aa3b2; text-decoration:line-through; font-weight:600; }
.tpw .tp-dots { display:flex; justify-content:center; gap:4px; margin:10px 0 0; flex-wrap:wrap; }
.tpw .tp-dots span { width:7px; height:7px; border-radius:50%; background:#d5dbe5; }
.tpw .tp-dots span.on { background:var(--blue); }
.tpw .tp-list { margin:6px 0 0; padding:0; list-style:none; counter-reset:tp; }
.tpw .tp-list li { counter-increment:tp; display:grid; grid-template-columns:1.6em 1fr auto auto; gap:8px; align-items:center; padding:3px 0; font-size:.86rem; border-bottom:1px dashed #e3e7ee; }
.tpw .tp-list li::before { content:counter(tp) "."; color:var(--muted); font-weight:700; }
.tpw .tp-list .tp-cost { color:var(--muted); font-variant-numeric:tabular-nums; }
.tpw .tp-list .tp-take { font-weight:800; font-variant-numeric:tabular-nums; text-align:right; }
.tpw [data-r], .tpw [data-colhead], .tpw td.tp-c[data-k] { cursor:pointer; }
.tpw.tp-read td.tp-c[data-k], .tpw.tp-cost td.tp-c[data-k] { cursor:pointer; }
@media (max-width:600px) { .tpw { padding:12px 8px; } .tpw .tp-cap { font-size:.85rem; } .tpw table.tp { font-size:.76rem; } .tpw td.tp-c { min-width:54px; height:40px; } }
@media (prefers-reduced-motion: reduce) { .tpw * { transition:none !important; } }
</style>"""

RUNTIME = r"""<script>
(function () {
  function table(root, M) {
    var t = '<table class="tp financial"><thead><tr><th class="tp-rl"></th>';
    M.cols.forEach(function (c) { t += '<th data-colhead="' + c.id + '">' + c.label + '</th>'; });
    t += '<th class="tp-sub">Total<br>available</th></tr></thead><tbody>';
    var blocked = {};
    M.rows.forEach(function (r, ri) {
      t += '<tr data-row="' + r.id + '"><th class="tp-rl" data-r="' + r.id + '">' + (r.per ? '<span class="tp-per p' + r.t + '">' + r.per.slice(0, 3) + '</span>' : '') + r.src + '</th>';
      M.cols.forEach(function (c) {
        var k = r.id + '|' + c.id, u = M.cost[k];
        if (u === null) {
          if (!blocked[c.id]) {   // one black block per column, spanning every row that cannot serve it
            var span = M.rows.filter(function (q) { return M.cost[q.id + '|' + c.id] === null; }).length;
            t += '<td class="tp-x' + (c.id === 'mar' ? ' tp-note' : '') + '" rowspan="' + span + '">' + (c.id === 'mar' ? 'No back-ordering' : '') + '</td>';
            blocked[c.id] = 1;
          }
        } else {
          t += '<td class="tp-c" data-k="' + k + '"><span class="tp-u">' + (r.id === 'inv' && c.id === 'dum' ? '&nbsp;' : u) + '</span><span class="tp-q"></span></td>';
        }
      });
      t += '<td class="tp-cap" data-cap="' + r.id + '"></td></tr>';
    });
    t += '<tr><th class="tp-rl">Total demand</th>';
    M.cols.forEach(function (c) { t += '<td class="tp-dem" data-dem="' + c.id + '"></td>'; });
    t += '<td></td></tr></tbody></table>';
    root.querySelector('.tp-scroll').innerHTML = t;
  }
  function paint(root, M, S) {
    root.querySelectorAll('td.tp-c').forEach(function (td) {
      var k = td.dataset.k, col = k.split('|')[1], q = S.alloc[k], u = td.querySelector('.tp-u'), qq = td.querySelector('.tp-q');
      u.classList.toggle('off', S.costs.indexOf(col) < 0);
      if (q) { qq.textContent = q.toLocaleString('en-US'); qq.className = 'tp-q'; }
      else if (S.done.indexOf(col) >= 0) { qq.textContent = '--'; qq.className = 'tp-q dash'; }
      else { qq.textContent = ''; qq.className = 'tp-q'; }
      td.classList.toggle('hi', S.hi.indexOf(k) >= 0);
      td.classList.toggle('col', S.hicols.indexOf(col) >= 0);
    });
    root.querySelectorAll('tr[data-row]').forEach(function (tr) { tr.classList.toggle('rowhi', S.hirows.indexOf(tr.dataset.row) >= 0 && S.hi.length === 0); });
    M.rows.forEach(function (r) {
      var left = S.left[r.id], cell = root.querySelector('[data-cap="' + r.id + '"]');
      cell.innerHTML = left === r.cap ? r.cap.toLocaleString('en-US') : (left === 0 ? '<span class="tp-done">' + r.cap.toLocaleString('en-US') + '</span>' : '<s>' + r.cap.toLocaleString('en-US') + '</s>' + left.toLocaleString('en-US'));
    });
    M.cols.forEach(function (c) {
      var left = S.dleft[c.id], cell = root.querySelector('[data-dem="' + c.id + '"]');
      cell.innerHTML = left === 0 ? '<span class="tp-done">' + c.dem.toLocaleString('en-US') + '</span>' : (left === c.dem ? c.dem.toLocaleString('en-US') : '<s>' + c.dem.toLocaleString('en-US') + '</s>' + left.toLocaleString('en-US'));
    });
  }
  function stepper(root, M) {
    table(root, M);
    var i = 0, cap = root.querySelector('.tp-cap'), back = root.querySelector('.tp-back'), next = root.querySelector('.tp-next'), count = root.querySelector('.tp-count'), dots = root.querySelector('.tp-dots');
    dots.innerHTML = M.steps.map(function () { return '<span></span>'; }).join('');
    function go(k) {
      i = Math.max(0, Math.min(M.steps.length - 1, k)); var S = M.steps[i];
      paint(root, M, S);
      cap.innerHTML = '<b class="tp-h">' + S.title + '</b>' + S.text;
      count.textContent = 'Step ' + (i + 1) + ' of ' + M.steps.length;
      back.disabled = i === 0; next.disabled = i === M.steps.length - 1;
      dots.querySelectorAll('span').forEach(function (d, j) { d.classList.toggle('on', j <= i); });
    }
    back.addEventListener('click', function () { go(i - 1); });
    next.addEventListener('click', function () { go(i + 1); });
    root.addEventListener('keydown', function (e) { if (e.key === 'ArrowRight') go(i + 1); if (e.key === 'ArrowLeft') go(i - 1); });
    go(0);
  }
  function explorer(root, M) {
    table(root, M);
    var cap = root.querySelector('.tp-cap'), tabs = root.querySelectorAll('.tp-bar button'), mode = 'costs', final = M.final;
    function base(extra) {
      var S = { costs: ['mar', 'apr', 'may', 'dum'], alloc: {}, left: {}, dleft: {}, done: [], hi: [], hirows: [], hicols: [] };
      M.rows.forEach(function (r) { S.left[r.id] = r.cap; }); M.cols.forEach(function (c) { S.dleft[c.id] = c.dem; });
      return Object.assign(S, extra || {});
    }
    function full(extra) { return Object.assign(base({ alloc: final.alloc, left: final.left, dleft: final.dleft, done: ['mar', 'apr', 'may', 'dum'] }), extra || {}); }
    function fill(colId) {
      var label = M.cols.filter(function (c) { return c.id === colId; })[0].label, alloc = {}, done = [], left = {}, dleft = {}, order = ['mar', 'apr', 'may', 'dum'];
      M.rows.forEach(function (r) { left[r.id] = r.cap; }); M.cols.forEach(function (c) { dleft[c.id] = c.dem; });
      for (var j = 0; j <= order.indexOf(colId); j++) {   // the plan as it stands once this column is filled
        Object.keys(final.alloc).forEach(function (k) { var p = k.split('|'); if (p[1] === order[j]) { alloc[k] = final.alloc[k]; left[p[0]] -= final.alloc[k]; dleft[p[1]] -= final.alloc[k]; } });
        done.push(order[j]);
      }
      var hi = Object.keys(alloc).filter(function (k) { return k.split('|')[1] === colId; });
      paint(root, M, base({ alloc: alloc, left: left, dleft: dleft, done: done, hi: hi, hicols: [colId] }));
      if (colId === 'dum') {
        cap.innerHTML = '<b class="tp-h">Unused capacity</b>Once every month is filled, what is left goes to the dummy column at $0:<ol class="tp-list">' +
          M.dummyRows.map(function (x) { return '<li><span>' + x[0] + '</span><span class="tp-cost">$0</span><span class="tp-take">' + x[1] + '</span></li>'; }).join('') + '</ol>';
        return;
      }
      cap.innerHTML = '<b class="tp-h">Filling ' + label + ' demand (' + M.cols.filter(function (c) { return c.id === colId; })[0].dem.toLocaleString('en-US') + ' units), cheapest source first</b>Earlier months\' leftover production counts as a source too, at its cost plus $2 a month held.<ol class="tp-list">' +
        M.fills[colId].map(function (x) { return '<li><span>' + x[0] + '</span><span class="tp-cost">$' + x[1] + '</span><span class="tp-take">' + x[2].toLocaleString('en-US') + '</span></li>'; }).join('') + '</ol>';
    }
    function setMode(m) {
      mode = m; tabs.forEach(function (b) { b.setAttribute('aria-pressed', b.dataset.mode === m ? 'true' : 'false'); });
      root.classList.toggle('tp-read', m === 'read'); root.classList.toggle('tp-cost', m === 'costs');
      if (m === 'costs') { paint(root, M, base({ done: [] })); cap.innerHTML = '<b class="tp-h">How each cost is built</b>Each cell is the source\'s price plus $2 for every month the tire is held. Tap any cell to see its sum.'; }
      else if (m === 'read') { paint(root, M, full()); cap.innerHTML = '<b class="tp-h">Reading the plan</b>Tap a <b>row</b> name for everything produced by one source in one period, or a <b>column</b> name for everything that meets one month\'s demand.'; }
      else if (m === 'total') { paint(root, M, full({ hi: Object.keys(final.alloc).filter(function (k) { return k.split('|')[1] !== 'dum'; }) })); cap.innerHTML = '<b class="tp-h">Total cost</b>' + M.totalText; }
      else fill(m);
    }
    tabs.forEach(function (b) { b.addEventListener('click', function () { setMode(b.dataset.mode); }); });
    root.querySelector('.tp-scroll').addEventListener('click', function (e) {
      if (mode === 'costs') {
        var td = e.target.closest('td.tp-c'); if (!td) return;
        paint(root, M, base({ done: [], hi: [td.dataset.k] })); cap.innerHTML = M.why[td.dataset.k];
      } else if (mode === 'read') {
        var rh = e.target.closest('[data-r]'), ch = e.target.closest('[data-colhead]');
        if (rh) {
          var id = rh.dataset.r, r = M.rows.filter(function (x) { return x.id === id; })[0], ks = Object.keys(final.alloc).filter(function (k) { return k.split('|')[0] === id && k.split('|')[1] !== 'dum'; });
          var used = ks.reduce(function (s, k) { return s + final.alloc[k]; }, 0);
          paint(root, M, full({ hi: ks, hirows: [id] }));
          cap.innerHTML = '<b class="tp-h">Row: ' + (r.per ? r.per + ' ' + r.src.toLowerCase() : r.src) + '</b>A period of <b>production</b>: read across the row. ' + used.toLocaleString('en-US') + ' units are used' +
            (ks.length ? ' (' + ks.map(function (k) { return final.alloc[k].toLocaleString('en-US') + ' for ' + M.cols.filter(function (c) { return c.id === k.split('|')[1]; })[0].label; }).join(', ') + ')' : '') + '.';
        } else if (ch && ch.dataset.colhead !== 'dum') {
          var cid = ch.dataset.colhead, c = M.cols.filter(function (x) { return x.id === cid; })[0], ks2 = Object.keys(final.alloc).filter(function (k) { return k.split('|')[1] === cid; });
          paint(root, M, full({ hi: ks2, hicols: [cid] }));
          cap.innerHTML = '<b class="tp-h">Column: ' + c.label + ' demand</b>A period of <b>demand</b>: read down the column. ' + ks2.map(function (k) {
            var r = M.rows.filter(function (x) { return x.id === k.split('|')[0]; })[0]; return final.alloc[k].toLocaleString('en-US') + ' from ' + (r.per ? r.per + ' ' + r.src.toLowerCase() : r.src.toLowerCase()); }).join(', ') + ' = ' + c.dem.toLocaleString('en-US') + '.';
        }
      }
    });
    setMode('costs');
  }
  document.querySelectorAll('.tpw[data-mode]').forEach(function (root) {
    try { var M = JSON.parse(root.querySelector('script[type="application/json"]').textContent); (root.dataset.mode === 'stepper' ? stepper : explorer)(root, M); }
    catch (e) { if (window.console) console.error('transportation widget', e); }
  });
})();
</script>"""

def model():
    M = {"rows": [{"id": r[0], "per": r[1], "src": r[2] if r[0] != "inv" else "Beginning inv.", "cap": r[3], "t": r[5]} for r in ROWS],
         "cols": [{"id": c[0], "label": c[1], "dem": c[2]} for c in COLS] + [{"id": "dum", "label": "Unused (dummy)", "dem": DUMMY_UNITS}],
         "cost": {f"{r[0]}|{c[0]}": cost(r, c) for r in ROWS for c in COLS + [DUMMY]}}
    left = {r[0]: r[3] for r in ROWS}; dleft = {c[0]: c[2] for c in COLS}; dleft["dum"] = DUMMY_UNITS
    for (rk, ck), q in ALLOC.items(): left[rk] -= q; dleft[ck] -= q
    assert all(v == 0 for v in left.values()) and all(v == 0 for v in dleft.values())
    M["final"] = {"alloc": {f"{k[0]}|{k[1]}": v for k, v in ALLOC.items()}, "left": left, "dleft": dleft}
    return M

FALLBACK = '<noscript><img src="https://smokinnotes.s3.us-east-1.amazonaws.com/public/man4504-253-exam3-chapter12-10-transportation-final-solution.png" alt="Complete transportation table with all allocations" class="image-wide-75 content-image"></noscript>'

def widget(mode):
    M = model()
    if mode == "stepper":
        M["steps"] = states()
        body = ('<div class="tp-bar"><button type="button" class="tp-back">◀ Back</button><span class="tp-count"></span><button type="button" class="tp-next">Next ▶</button></div>\n'
                '<div class="tp-cap" aria-live="polite"></div>\n<div class="tp-scroll"></div>\n<div class="tp-dots" aria-hidden="true"></div>')
        title, lede = "The Transportation Method, Step by Step", "Press Next to build the table and the plan one step at a time."
    else:
        M.update(explorer_data())
        terms = cost_terms()
        M["totalText"] = " + ".join(f"{q:,}({u})" for q, u in terms) + f" = <b>{money(TOTAL_COST)}</b>."
        M["dummyRows"] = M.pop("dummy")
        tabs = [("costs", "1. Costs"), ("mar", "2. March"), ("apr", "3. April"), ("may", "4. May"), ("dum", "5. Unused")]
        body = ('<div class="tp-bar" role="group" aria-label="Step">' + "".join(f'<button type="button" data-mode="{m}">{l}</button>' for m, l in tabs) + '</div>\n'
                '<div class="tp-cap" aria-live="polite"></div>\n<div class="tp-scroll"></div>')
        title, lede = "The Transportation Method: Tire Example", "Work through the tabs in order."
    js = json.dumps(M, ensure_ascii=False).replace("</", "<\\/")
    return (f'<div class="tpw" data-mode="{mode}" tabindex="-1">\n<p class="tp-title">{title}</p>\n<p class="tp-lede">{lede}</p>\n{body}\n'
            f'{FALLBACK}\n<script type="application/json">{js}</script>\n</div>')

# ---------------------------------------------------------------- the chapter
INTRO = ("<p>We set the problem up as a table: demand periods across the top, sources of supply down the side, "
         "and the cost of each pairing in the corner of its cell. Then we fill each month's demand from its cheapest available sources. "
         "{how}</p>")

def chapter(src, mode):
    t = open(src, encoding="utf-8").read()
    a = t.index("<h2>Step 1: Set Up the Table</h2>")
    b = t.index("<p>This table depicts a possible aggregate production plan.")
    old = t[a:b]
    for must in ("chapter12-02-", "chapter12-10-", "Luckily, we have already added in a dummy column"):
        assert must in old, must
    how = ("The widget below builds the table and the plan one step at a time." if mode == "stepper"
           else "Work through the widget's tabs in order: how the costs are built and how each month is filled.")
    new = ("<h2>Setting Up and Solving the Table</h2>\n\n" + INTRO.format(how=how) + "\n\n" + CSS + "\n" + widget(mode) + "\n\n")
    t = t[:a] + new + t[b:]
    t = t.replace("</body>", RUNTIME + "\n</body>", 1)
    # the chapter's own wide tables scroll inside their box on a phone; the widget's table already does
    t = t.replace("</head>", '<style>@media (max-width:600px){table:not(.tp){display:block;overflow-x:auto !important;-webkit-overflow-scrolling:touch} mjx-container{display:inline-block !important;max-width:100%;overflow-x:auto;overflow-y:hidden;vertical-align:middle}}</style>\n</head>', 1)
    assert t.count("chapter12-0") == 1 and "chapter12-10-" in t   # the flowchart stays; only the noscript fallback remains of the table images
    return t

if __name__ == "__main__":
    src, outdir = sys.argv[1:3]; os.makedirs(outdir, exist_ok=True)
    for mode, tag in (("stepper", "OptionA-Stepper"), ("explorer", "OptionB-Explorer")):
        p = os.path.join(outdir, f"MAN4504-263-Exam3-AggregatePlanning-FULL-{tag}.html")
        open(p, "w", encoding="utf-8").write(chapter(src, mode)); print("wrote", p)
    print(f"checks passed: demand {TOTAL_D}, capacity {TOTAL_CAP} + {INV}, dummy {DUMMY_UNITS}, total cost {money(TOTAL_COST)}")
