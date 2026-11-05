"""Exam 3 widget shapes: firms, market structures, games, factor markets,
inequality and externalities. Symbolic like Exam 1's (no numbers on the axes
unless the question states them), and every relationship a figure exists to
show is asserted, not eyeballed:

* MC is the exact derivative of total cost wherever MR = MC has to hold at a
  point the figure marks (monopoly, monopolistic competition), so the
  tangency and the profit-maximizing output are arithmetic.
* The competitive-firm figures use curve_shapes.cost_family, the house shape
  for MC, AVC and ATC, and every marked output is one of the samples.
* Every crossing is solved, never typed."""
import math, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / 'scripts'))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from curve_shapes import cross, cost_family, lorenz
from widgets_lib import S_pts, D_pts, D_label, shift, four, dbl

R = lambda v: round(v, 2)

def solve(f, lo, hi):
    """The root of f on [lo, hi] by bisection; f must change sign."""
    flo = f(lo); assert flo * f(hi) <= 0, (lo, hi, flo, f(hi))
    for _ in range(80):
        mid = (lo + hi) / 2.0
        if (f(mid) > 0) == (flo > 0): lo, flo = mid, f(mid)
        else: hi = mid
    return (lo + hi) / 2.0

def curve_of(f, xs):
    return [[R(x), R(f(x))] for x in sorted(set(R(x) for x in xs))]

# ------------------------------------------------- labor-market shifts ----
def gshift(curve, d, title, lede, steps, x="Quantity of Labor", y="Wage Rate", pl=("W₁", "W₂"), ql=("L₁", "L₂")):
    """One curve shifts on axes the presets cannot relabel. Three steps:
    start, shift, new equilibrium."""
    dd = 24 if d == "right" else -24          # 24, not 20: W₁ and W₂ need room on the axis
    if curve == "D":
        curves = [{"id": "S", "label": "S", "pts": S_pts()}, {"id": "D1", "label": "D₁", "pts": D_pts(), **D_label()},
                  {"id": "D2", "label": "D₂", "pts": D_pts(dd), "color": "red", "from": "D1", "at": 1, "arrowP": 80 if dd > 0 else 60, **D_label()}]
        e2 = cross(D_pts(dd), S_pts())
    else:
        curves = [{"id": "D", "label": "D", "pts": D_pts(), **D_label()}, {"id": "S1", "label": "S₁", "pts": S_pts()},
                  {"id": "S2", "label": "S₂", "pts": S_pts(dd), "color": "red", "from": "S1", "at": 1, "arrowP": 70 if dd > 0 else 88}]
        e2 = cross(D_pts(), S_pts(dd))
    assert len(steps) == 3
    return {"title": title, "lede": lede, "axes": {"xmax": 110, "ymax": 110, "x": x, "y": y}, "curves": curves,
            "points": [{"q": 50, "p": 50, "pl": pl[0], "ql": ql[0]},
                       {"q": R(e2[0]), "p": R(e2[1]), "pl": pl[1], "ql": ql[1], "color": "red", "at": 2}],
            "steps": steps}

# --------------------------------------------------------- payoff games ----
VERB = {"Lower prices": "cutting", "Don't lower prices": "not cutting",
        "Set low prices": "with low prices", "Set high prices": "with high prices"}
IF = {"Lower prices": "cuts its prices", "Don't lower prices": "does not cut",
      "Set low prices": "sets low prices", "Set high prices": "sets high prices"}
# What the grid itself prints: the papers' phrases are too long for a cell
# heading, and "Set low prices" ran into "Set high prices" beside it.
GRID = {"Lower prices": "Cut prices", "Don't lower prices": "Don't cut",
        "Set low prices": "Low prices", "Set high prices": "High prices"}
PICK = {"Lower prices": "cuts", "Don't lower prices": "does not cut",
        "Set low prices": "sets low prices", "Set high prices": "sets high prices"}

def game(cells, labels, answer):
    """cells[i][j] = (Target, Walmart) in $ millions; rows are Walmart's
    choices and columns Target's, as the papers lay them out. Five steps:
    the grid, then the four comparisons the written solution makes, in its
    order. The dominant strategies the comparisons find are checked against
    the solution's own letter."""
    A, B = labels
    m = lambda v: "$%g million" % v
    grid = [[["T: " + m(t), "W: " + m(w)] for (t, w) in row] for row in cells]
    marks, steps = [], ["Each cell gives Target's profit (T) and Walmart's (W) for one pair of choices."]
    # Walmart's best reply to each Target choice (a column, Walmart's line)
    wbest = []
    for j in range(2):
        w0, w1 = cells[0][j][1], cells[1][j][1]
        assert w0 != w1
        i = 0 if w0 > w1 else 1; wbest.append(i)
        marks += [{"col": j, "who": "b", "given": True, "at": 1 + j, "until": 2 + j},
                  {"cell": [i, j], "who": "b", "pick": True, "at": 1 + j, "until": 2 + j}]
        s = "If Target %s, Walmart makes %s %s and %s %s, so it %s." % (
            IF[labels[j]], m(w0), VERB[A], m(w1), VERB[B], PICK[labels[i]])
        steps.append(s)
    w_dom = wbest[0] == wbest[1]
    steps[2] += (" Either way it %s: a dominant strategy." % PICK[labels[wbest[0]]] if w_dom else
                 " Its best choice depends on Target's: no dominant strategy.")
    tbest = []
    for i in range(2):
        t0, t1 = cells[i][0][0], cells[i][1][0]
        assert t0 != t1
        j = 0 if t0 > t1 else 1; tbest.append(j)
        marks += [{"row": i, "who": "a", "given": True, "at": 3 + i, "until": 4 + i},
                  {"cell": [i, j], "who": "a", "pick": True, "at": 3 + i, "until": 4 + i}]
        s = "If Walmart %s, Target makes %s %s and %s %s, so it %s." % (
            IF[labels[i]], m(t0), VERB[A], m(t1), VERB[B], PICK[labels[j]])
        steps.append(s)
    t_dom = tbest[0] == tbest[1]
    steps[4] += (" Either way it %s: a dominant strategy." % PICK[labels[tbest[0]]] if t_dom else
                 " Its best choice depends on Walmart's: no dominant strategy.")
    got = {(True, False): "a", (False, True): "b", (True, True): "c", (False, False): "d"}[(w_dom, t_dom)]
    assert got == answer, (got, answer, cells)
    for s in steps: assert len(s) <= 200, (len(s), s)
    return {"title": "The Pricing Game Between Target and Walmart",
            "lede": "Hold one firm's choice fixed and compare the other firm's two payoffs.",
            "matrix": {"rows": {"player": "WALMART", "labels": [GRID[l] for l in labels]},
                       "cols": {"player": "TARGET", "labels": [GRID[l] for l in labels]},
                       "cells": grid, "marks": marks},
            "steps": steps}

# ------------------------------------------------------ competitive firm ----
AVC, ATC, MCc = None, None, None
_avc_min, _atc_min = (40, 30), (55, 45)
_h = _avc_min[0] - 16
_a = (_atc_min[1] - _avc_min[1]) / float((_atc_min[0] - _h) ** 2 - (_avc_min[0] - _h) ** 2)
_k = _avc_min[1] - _a * (_avc_min[0] - _h) ** 2
mc_f = lambda q: _a * (q - _h) ** 2 + _k
atc_f = lambda q: 0.032 * (q - _atc_min[0]) ** 2 + _atc_min[1]
avc_f = lambda q: 0.018 * (q - _avc_min[0]) ** 2 + _avc_min[1]
q_at_price = lambda P: _h + math.sqrt((P - _k) / _a)       # on MC's rising arm

def _firm_curves(extra_q=(), avc=False):
    qs = list(extra_q)
    avcs, atcs, mcs = cost_family(_avc_min, _atc_min,
                                  avc_xs=[14, 24, 32, 40, 50, 58, 66] + qs,
                                  atc_xs=[13, 23, 35, 45, 55, 67, 79, 93] + qs,
                                  mc_xs=[10, 18, 24, 32, 40, 48, 55, 65, 73] + qs)
    srt = lambda l: sorted({tuple(p) for p in l})
    cur = [{"id": "MC", "label": "MC", "pts": [list(p) for p in srt(mcs) if p[1] <= 104], "curved": True},
           {"id": "ATC", "label": "ATC", "pts": [list(p) for p in srt(atcs) if p[1] <= 104], "curved": True}]
    if avc: cur.append({"id": "AVC", "label": "AVC", "pts": [list(p) for p in srt(avcs)], "curved": True})
    return cur

def _price_line(P, ident, label, at=None, until=None, color=None):
    c = {"id": ident, "label": label, "pts": [[4, R(P)], [100, R(P)]]}
    if at is not None: c["at"] = at
    if until is not None: c["until"] = until
    if color: c["color"] = color
    return c

def firm_rect(P, q, color, label, at=None, until=None):
    c = R(atc_f(q))
    a = {"pts": [[0, R(P)], [R(q), R(P)], [R(q), c], [0, c]], "label": label, "color": color, "edge": True}
    if at is not None: a["at"] = at
    if until is not None: a["until"] = until
    return a

def comp_firm(title, lede, steps, prices, labels=("P₁", "P₂"), rect=True, avc=False, move=False, cur_q=None):
    """A price-taking firm at one or two prices. Step k shows prices[k]'s
    line, the output where MC meets it, and (rect) the profit or loss."""
    qs = [R(q_at_price(P)) for P in prices]
    extra = qs + ([cur_q] if cur_q else [])
    c = {"title": title, "lede": lede, "axes": {"xmax": 110, "ymax": 110, "y": "Price and Cost"},
         "curves": _firm_curves(extra, avc), "points": [], "areas": [], "steps": steps}
    n = len(prices)
    for k, (P, q) in enumerate(zip(prices, qs)):
        at = k if k else None; until = k + 1 if k + 1 < n else None
        c["curves"].append(_price_line(P, "P%d" % k, "%s = MR" % labels[k], at=at, until=until, color="red" if k else None))
        pt = {"q": q, "p": R(P), "pl": labels[k], "ql": "Q%s" % "₁₂"[k] if n > 1 else "Q*"}
        if k: pt.update({"color": "red", "at": k})
        elif n == 1 and not (rect and abs(P - atc_f(q)) > 0.5): pt["at"] = 1
        if until: pt["until"] = until
        c["points"].append(pt)
        if rect and abs(P - atc_f(q)) > 0.5:
            kind = ("Profit", "teal") if P > atc_f(q) else ("Loss", "red")
            c["areas"].append(firm_rect(P, q, kind[1], kind[0], at=at if at else 1, until=until))
            c["points"].append({"q": q, "p": R(atc_f(q)), "guides": False, "showP": False, "showQ": False, **({"at": at} if at else {"at": 1}), **({"until": until} if until else {})})
    if cur_q:
        c["points"].insert(0, {"q": cur_q, "p": R(mc_f(cur_q)), "label": "Now", "dx": -34, "dy": 4, "guides": "q", "ql": "22", "showP": False})
        # no movement arrow: it would lie along MC between two dots, and the
        # dots and the caption already carry the move
    if not c["areas"]: del c["areas"]
    return c

def shutdown(title, lede, steps):
    """MC, AVC and ATC with the shutdown point at AVC's minimum and a price
    below it."""
    P = 14.0
    c = {"title": title, "lede": lede, "axes": {"xmax": 110, "ymax": 110, "y": "Price and Cost"},
         "curves": _firm_curves(avc=True) + [_price_line(P, "P", "P", at=1)],
         "points": [{"q": _avc_min[0], "p": _avc_min[1], "label": "Shutdown point", "dx": 10, "dy": 18, "guides": False, "showP": False, "showQ": False},
                    {"q": _atc_min[0], "p": _atc_min[1], "guides": False, "showP": False, "showQ": False}],
         "steps": steps}
    assert P < _avc_min[1]
    return c

# ---------------------------------------------- market beside the firm ----
def mkt_firm(kind, title, lede, steps):
    """The market (left) and one firm (right) on one price scale.
    kind: 'up_sr' demand rises, firm earns a profit (3 steps);
          'up_lr' demand rises, then entry returns price to ATC's minimum (5);
          'entry' a profit draws entry and price falls to the minimum (4);
          'exit'  a loss drives exit and price rises, the loss shrinking (4)."""
    pmin = _atc_min[1]                     # 45: the long-run price
    sl = 0.9
    if kind == "exit":
        P0 = 32.0
    elif kind == "entry":
        P0 = 56.0
    else:
        P0 = pmin
    # market: S p = sl*q, D p = 2*P0 - sl*q, so the two cross at (P0/sl, P0)
    S1 = [[8, R(sl * 8)], [110, R(sl * 110)]]
    Dm = lambda top: [[4, R(top - sl * 4)], [R(top / sl - 4), R(sl * 4)]]
    D1 = Dm(2 * P0)
    e1 = cross(D1, S1)
    mkt = {"heading": "The Market", "axes": {"xmax": 120, "ymax": 110},
           "curves": [{"id": "S1", "label": "S₁" if kind != "up_sr" else "S", "pts": S1},
                      {"id": "D1", "label": "D₁" if kind in ("up_sr", "up_lr") else "D", "pts": D1}],
           "points": [{"q": R(e1[0]), "p": R(e1[1]), "pl": "P₁", "ql": "Q₁"}]}
    firm = {"heading": "One Firm", "axes": {"xmax": 110, "ymax": 110, "y": "Price and Cost"}, "curves": [], "points": [], "areas": []}
    seq = []                                # (price, step it arrives)
    if kind in ("up_sr", "up_lr"):
        D2 = Dm(2 * P0 + 24)
        e2 = cross(D2, S1); P1 = e2[1]
        mkt["curves"].append({"id": "D2", "label": "D₂", "pts": D2, "color": "red", "from": "D1", "at": 1, "arrowP": 70})
        mkt["points"].append({"q": R(e2[0]), "p": R(P1), "pl": "P₂", "ql": "Q₂", "color": "red", "at": 1, **({"until": 4} if kind == "up_lr" else {})})
        seq = [(P0, 0), (P1, 2)]                # the firm answers the new price a step later
        if kind == "up_lr":
            # entry until the price is back at the minimum of ATC
            q3 = (2 * P0 + 24 - pmin) / sl                 # D2 at the old price
            d = q3 - pmin / sl
            S2 = [[R(8 + d), R(sl * 8)], [110, R(sl * (110 - d))]]
            # above every guide: at 30 the arrow ran across Q₁'s
            mkt["curves"].append({"id": "S2", "label": "S₂", "pts": S2, "color": "red", "from": "S1", "at": 3, "arrowP": 72})
            mkt["points"].append({"q": R(q3), "p": R(pmin), "pl": "P₁", "ql": "Q₃", "color": "red", "at": 4, "showP": False})
            seq.append((pmin, 4))
    else:
        target = pmin if kind == "entry" else 43.0          # exit: losses shrink, not vanish
        dq = (2 * P0 - target) / sl - target / sl              # the supply shift that lands there
        S2 = [[R(max(8, 8 + dq)), R(sl * max(8, 8 + dq) - sl * dq)], [110, R(sl * (110 - dq))]]
        e2 = cross(D1, S2); P1 = e2[1]
        mkt["curves"].append({"id": "S2", "label": "S₂", "pts": S2, "color": "red", "from": "S1", "at": 1, "arrowP": 30 if kind == "entry" else 70})
        mkt["points"].append({"q": R(e2[0]), "p": R(P1), "pl": "P₂", "ql": "Q₂", "color": "red", "at": 2})
        seq = [(P0, 0), (P1, 2)]
        if kind == "entry": assert abs(P1 - pmin) < 0.6, P1
        else: assert P0 < P1 < pmin, P1
    qx = [R(q_at_price(P)) for P, _ in seq]
    firm["curves"] = _firm_curves(qx)
    for k, ((P, at), q) in enumerate(zip(seq, qx)):
        until = seq[k + 1][1] if k + 1 < len(seq) else None
        lab = "P₁" if abs(P - P0) < 0.01 else "P₂"
        ln = _price_line(P, "F%d" % k, "%s = MR" % lab, at=at or None, until=until, color="red" if k else None)
        firm["curves"].append(ln)
        pt = {"q": q, "p": R(P), "pl": lab, "ql": "q%s" % "₁₂₃"[k]}
        if k: pt.update({"color": "red", "at": at})
        if until is not None: pt["until"] = until
        if abs(P - pmin) < 0.01 and k: pt["pl"] = "P₁"; pt["showP"] = False; pt["ql"] = "q₁"; pt["showQ"] = False
        firm["points"].append(pt)
        gap = P - atc_f(q)
        if abs(gap) > 0.8:
            kind_ = ("Profit", "teal") if gap > 0 else ("Loss", "red")
            a_at = at if at else 0
            a = firm_rect(P, q, kind_[1], kind_[0], at=a_at or None, until=until)
            firm["areas"].append(a)
            firm["points"].append({"q": q, "p": R(atc_f(q)), "guides": False, "showP": False, "showQ": False,
                                   **({"at": at} if at else {}), **({"until": until} if until is not None else {})})
    if not firm["areas"]: del firm["areas"]
    return {"title": title, "lede": lede, "link": False, "panels": [mkt, firm], "steps": steps}

# ---------------------------------------- cost curves with an exact MC ----
class Cost:
    """ATC = a(q - m)^2 + c; MC = d(q * ATC)/dq exactly, so it cuts ATC at
    ATC's minimum and MR = MC wherever the figure says it does."""
    def __init__(self, a=0.02, m=60.0, c=40.0):
        self.a, self.m, self.c = a, m, c
    def atc(self, q): return self.a * (q - self.m) ** 2 + self.c
    def mc(self, q): return self.atc(q) + q * 2 * self.a * (q - self.m)
    def slope(self, q): return 2 * self.a * (q - self.m)
    def curves(self, extra=(), atc_x=(12, 20, 30, 40, 50, 60, 72, 84, 96), mc_x=(16, 24, 32, 40, 48, 56, 64, 70, 76)):
        assert abs(self.mc(self.m) - self.atc(self.m)) < 1e-9
        a = curve_of(self.atc, list(atc_x) + list(extra)); m = curve_of(self.mc, list(mc_x) + [x for x in extra if x >= 16])
        return [{"id": "MC", "label": "MC", "pts": [p for p in m if p[1] <= 104], "curved": True},
                {"id": "ATC", "label": "ATC", "pts": [p for p in a if p[1] <= 104], "curved": True}]

def _line(A, b, x0=0, x1=None, ymin=2):
    x1 = x1 if x1 is not None else (A - ymin) / b
    return [[R(x0), R(A - b * x0)], [R(x1), R(A - b * x1)]]

def monopoly(title, lede, steps, show=("profit",)):
    """A single-price monopoly: Qm where MR = MC, Pm on demand, and as asked
    the economic profit, the competitive output where D meets MC, and the
    deadweight loss between them."""
    C = Cost(); b = 0.8; qm = 45.0
    A = C.mc(qm) + 2 * b * qm
    pm = A - b * qm
    qc = solve(lambda q: (A - b * q) - C.mc(q), qm + 1, 90); pc = A - b * qc
    assert pm > C.atc(qm)
    D = _line(A, b, 0, (A - 12) / b); MRl = _line(A, 2 * b, 0, (A - 8) / (2 * b))
    c = {"title": title, "lede": lede, "axes": {"xmax": 112, "ymax": 110, "y": "Price and Cost"},
         "curves": C.curves((qm, qc)) + [{"id": "D", "label": "D", "pts": D}, {"id": "MR", "label": "MR", "pts": MRl}],
         "points": [{"q": R(qm), "p": R(C.mc(qm)), "guides": "q", "ql": "Qᴍ", "showP": False},
                    {"q": R(qm), "p": R(pm), "pl": "Pᴍ", "guides": "p", "showQ": False, "at": 1}],
         "areas": [], "steps": steps}
    at = 2
    if "profit" in show:
        ca = C.atc(qm)
        c["areas"].append({"pts": [[0, R(pm)], [R(qm), R(pm)], [R(qm), R(ca)], [0, R(ca)]], "label": "Profit", "color": "teal", "edge": True, "at": at})
        c["points"].append({"q": R(qm), "p": R(ca), "guides": False, "showP": False, "showQ": False, "at": at})
        at += 1
    if "dwl" in show:
        c["points"].append({"q": R(qc), "p": R(pc), "pl": "Pᴄ", "ql": "Qᴄ", "color": "red", "at": at})
        c["areas"].append({"pts": [[R(qm), R(pm)], [R(qc), R(pc)], [R(qm), R(C.mc(qm))]], "label": "DWL", "color": "red", "at": at + 1})
        c["points"][1]["hiAt"] = at + 1
        c["points"][0]["hiAt"] = at + 1
        at += 2
    if not c["areas"]: del c["areas"]
    assert len(steps) == at, (len(steps), at)
    return c

def natural_monopoly(title, lede, order, steps):
    """D, MR, a flat MC and ATC = MC + F/q falling across the market.
    Scenarios: unregulated (MR = MC, profit), marginal-cost pricing (P = MC,
    loss) and average-cost pricing (P = ATC, normal profit, deadweight loss).
    order names the scenarios in the order the buttons appear."""
    mc = 20.0; F = 700.0
    atc = lambda q: mc + F / q
    D = [[0, 100], [88, 12]]; MRl = [[0, 100], [46, 8]]
    qu = 40.0; pu = 100 - qu
    qmc = 80.0; pmc = mc
    qa = 70.0; pa = 100 - qa
    assert abs(100 - 2 * qu - mc) < 1e-9 and abs(atc(qa) - pa) < 1e-9 and atc(qmc) > pmc
    xs = [9, 12, 16, 22, 30, 40, 50, 60, 70, 80, 92]
    base = [{"id": "D", "label": "D", "pts": D}, {"id": "MR", "label": "MR", "pts": MRl},
            {"id": "ATC", "label": "ATC", "pts": [[x, R(atc(x))] for x in xs if atc(x) <= 104], "curved": True},
            {"id": "MC", "label": "MC", "pts": [[4, mc], [106, mc]]}]
    sc = {
     "unreg": {"label": "Unregulated", "steps": steps["unreg"],
               "points": [{"q": qu, "p": mc, "guides": "q", "ql": "Q", "showP": False},
                          {"q": qu, "p": pu, "pl": "P", "guides": "p", "showQ": False, "at": 1},
                          {"q": qu, "p": R(atc(qu)), "guides": False, "showP": False, "showQ": False, "at": 2}],
               "areas": [{"pts": [[0, pu], [qu, pu], [qu, R(atc(qu))], [0, R(atc(qu))]], "label": "Profit", "color": "teal", "edge": True, "at": 2}]},
     "mc": {"label": "Marginal-cost pricing", "steps": steps["mc"],
            "points": [{"q": qmc, "p": pmc, "pl": "P = MC", "ql": "Q", "at": 1},
                       {"q": qmc, "p": R(atc(qmc)), "label": "ATC", "dx": 10, "dy": -6, "guides": False, "showP": False, "showQ": False, "at": 2}],
            "areas": [{"pts": [[0, R(atc(qmc))], [qmc, R(atc(qmc))], [qmc, pmc], [0, pmc]], "label": "Loss", "color": "red", "edge": True, "at": 2}]},
     "atc": {"label": "Average-cost pricing", "steps": steps["atc"],
             "points": [{"q": qa, "p": pa, "pl": "P = ATC", "ql": "Q", "at": 1},
                        {"q": qmc, "p": pmc, "guides": "q", "ql": "Q*", "showP": False, "at": 2}],
             "areas": [{"pts": [[qa, pa], [qmc, pmc], [qa, mc]], "label": "DWL", "color": "red", "at": 2}]},
    }
    out = {"title": title, "lede": lede, "axes": {"xmax": 110, "ymax": 110, "y": "Price and Cost"}, "curves": base,
           "scenarios": {k: sc[k] for k in order}}
    return out

def moncomp(title, lede, steps, entry=False):
    """Monopolistic competition in the long run: demand tangent to ATC at the
    output where MR = MC, so price equals ATC and profit is zero. entry=True
    starts from a short-run profit on a higher demand curve, which new firms
    then push down to the tangency."""
    C = Cost(); q0 = 40.0
    b = -C.slope(q0); A = C.atc(q0) + b * q0
    assert abs((A - 2 * b * q0) - C.mc(q0)) < 1e-9          # MR = MC at the tangency
    D2 = _line(A, b, 0, (A - 12) / b); MR2 = _line(A, 2 * b, 0, (A - 8) / (2 * b))
    extra = [q0]
    if entry:
        A1 = A + 12
        q1 = solve(lambda q: (A1 - 2 * b * q) - C.mc(q), 41, 70); p1 = A1 - b * q1
        assert p1 > C.atc(q1)
        extra.append(q1)
        D1 = _line(A1, b, 0, (A1 - 12) / b); MR1 = _line(A1, 2 * b, 0, (A1 - 8) / (2 * b))
    c = {"title": title, "lede": lede, "axes": {"xmax": 110, "ymax": 110, "y": "Price and Cost"},
         "curves": C.curves(extra), "points": [], "steps": steps}
    if entry:
        # One MR at a time: the two end side by side on the Q axis, where
        # neither name has room, and the demand shift is the lesson.
        c["curves"] += [{"id": "D1", "label": "D₁", "pts": D1}, {"id": "MR1", "label": "MR₁", "pts": MR1, "until": 1},
                        {"id": "D2", "label": "D₂", "pts": D2, "color": "red", "from": "D1", "at": 1, "arrowP": 80},
                        {"id": "MR2", "label": "MR₂", "pts": MR2, "color": "red", "at": 1}]
        c["points"] += [{"q": R(q1), "p": R(p1), "pl": "P₁", "ql": "Q₁", "until": 2},
                        {"q": R(q1), "p": R(C.atc(q1)), "guides": False, "showP": False, "showQ": False, "until": 2},
                        {"q": q0, "p": R(A - b * q0), "pl": "P₂", "ql": "Q₂", "color": "red", "at": 2}]
        c["areas"] = [{"pts": [[0, R(p1)], [R(q1), R(p1)], [R(q1), R(C.atc(q1))], [0, R(C.atc(q1))]], "label": "Profit", "color": "teal", "edge": True, "until": 1}]
        assert len(steps) == 3
    else:
        c["curves"] += [{"id": "D", "label": "D", "pts": D2}, {"id": "MR", "label": "MR", "pts": MR2}]
        c["points"] += [{"q": q0, "p": R(C.mc(q0)), "guides": "q", "ql": "Q", "showP": False},
                        {"q": q0, "p": R(A - b * q0), "pl": "P = ATC", "guides": "p", "showQ": False, "at": 1},
                        {"q": q0, "p": R(C.mc(q0)), "pl": "MC", "guides": "p", "showQ": False, "at": 2}]
        assert len(steps) == 3
    return c

# ------------------------------------------------------------- labor ----
def labor_supply_bend(title, lede, steps):
    """A backward-bending labor supply curve: the substitution effect wins at
    low wages, the income effect at high ones. The turning wage is a divider,
    not a reading."""
    pts = [[14, 6], [30, 20], [44, 34], [54, 48], [59, 60], [59, 70], [54, 82], [46, 94]]
    turn = [60, 65]
    return {"title": title, "lede": lede, "axes": {"xmax": 110, "ymax": 110, "x": "Hours of Work", "y": "Wage Rate"},
            "curves": [{"id": "S", "label": "S", "pts": pts, "curved": True}],
            "points": [{"q": turn[0], "p": turn[1], "dot": False, "guides": "p", "divider": True, "showP": False, "showQ": False},
                       {"q": 44, "p": 34, "label": "Substitution effect\nis stronger", "dx": 12, "dy": 26, "guides": False, "showP": False, "showQ": False, "at": 1},
                       {"q": 54, "p": 82, "label": "Income effect\nis stronger", "dx": 12, "dy": 4, "guides": False, "showP": False, "showQ": False, "at": 2}],
            "steps": steps}

def skill_supply(title, lede, steps):
    lo = [[4, 12], [104, 62]]; hi = [[4, 52], [104, 102]]          # p = 0.5q + 10, and 40 above it
    q = 20
    return {"title": title, "lede": lede, "axes": {"xmax": 110, "ymax": 110, "x": "Quantity of Labor", "y": "Wage Rate"},
            "curves": [{"id": "SL", "label": "S_{Low}", "pts": lo},
                       {"id": "SH", "label": "S_{High}", "pts": hi, "color": "red", "at": 1}],
            "vbraces": [{"p1": 0.5 * q + 10, "p2": 0.5 * q + 50, "q": q, "label": "Cost of\nskill", "at": 2}],
            "points": [{"q": q, "p": 0.5 * q + 10, "guides": False, "showP": False, "showQ": False, "at": 2},
                       {"q": q, "p": 0.5 * q + 50, "guides": False, "showP": False, "showQ": False, "at": 2}],
            "steps": steps}

# ----------------------------------------------------------- inequality ----
def lorenz_move(title, lede, steps, direction="away"):
    a, b = lorenz(2.0), lorenz(3.4)
    first, second = (a, b) if direction == "away" else (b, a)
    return {"title": title, "lede": lede,
            "axes": {"xmax": 100, "ymax": 100, "pct": True, "x": "Cumulative Share\nof Households", "y": "Cumulative Share\nof Income"},
            "curves": [{"id": "EQ", "label": "", "pts": [[0, 0], [100, 100]], "thin": True},
                       {"id": "L1", "label": "", "pts": first, "curved": True},
                       {"id": "L2", "label": "", "pts": second, "curved": True, "color": "red", "at": 1}],
            "points": [{"q": 50, "p": 50, "label": "Line of equality", "boxed": True, "dot": False, "dx": -12, "dy": -12, "guides": False, "showP": False, "showQ": False},
                       {"q": first[4][0], "p": first[4][1], "label": "L₁", "boxed": True, "dot": False, "dx": 6, "dy": -4, "guides": False, "showP": False, "showQ": False},
                       {"q": second[7][0], "p": second[7][1], "label": "L₂", "boxed": True, "dot": False, "dx": 6, "dy": -4, "guides": False, "showP": False, "showQ": False, "at": 1}],
            "steps": steps}

# --------------------------------------------------------- externalities ----
def ext_cost(title, lede, steps, tax=False):
    """Pollution: MSC lies above the private MC by the marginal external
    cost. The market produces where D = MC; efficiency is where D = MSC."""
    # Lines at 0.6 rather than 1: the brace's name sits between MC and MSC,
    # and on parallel 45-degree lines a 30-unit gap is too narrow to hold it.
    gap = 30; q_b = 14
    D = [[4, R(95 - 0.9 * 4)], [100, R(95 - 0.9 * 100)]]
    MC = [[4, R(10 + 0.6 * 4)], [104, R(10 + 0.6 * 104)]]
    MSC = [[4, R(10 + gap + 0.6 * 4)], [100, R(10 + gap + 0.6 * 100)]]
    em = cross(D, MC); ee = cross(D, MSC)
    c = {"title": title, "lede": lede, "axes": {"xmax": 110, "ymax": 110},
         "curves": [{"id": "D", "label": "D = MB", "pts": D, "ldx": 6, "ldy": -8},
                    {"id": "MC", "label": "S = MC", "pts": MC},
                    {"id": "MSC", "label": "MSC", "pts": MSC, "color": "red", "at": 1}],
         "points": [{"q": R(em[0]), "p": R(em[1]), "ql": "Qᴍ", "pl": "Pᴍ"},
                    {"q": R(ee[0]), "p": R(ee[1]), "ql": "Q*", "pl": "P*", "color": "red", "at": 2},
                    {"q": R(em[0]), "p": R(em[1] + gap), "guides": False, "showP": False, "showQ": False, "at": 3}],
         "vbraces": [{"p1": R(10 + 0.6 * q_b), "p2": R(10 + gap + 0.6 * q_b), "q": q_b, "label": "MEC", "at": 1}],
         "areas": [{"pts": [[R(ee[0]), R(ee[1])], [R(em[0]), R(em[1] + gap)], [R(em[0]), R(em[1])]], "label": "DWL", "color": "red", "at": 3}],
         "steps": steps}
    c["points"][0]["hiAt"] = 3; c["points"][1]["hiAt"] = 3
    assert len(steps) == 4
    return c

def ext_benefit(title, lede, steps):
    gap = 30; q_b = 92
    mb = lambda q: 90 - 0.6 * q
    D = [[4, R(mb(4))], [104, R(mb(104))]]
    MSB = [[R((90 + gap - 104) / 0.6), 104], [104, R(mb(104) + gap)]]
    S = [[4, R(10 + 0.9 * 4)], [100, R(10 + 0.9 * 100)]]
    em = cross(D, S); ee = cross(MSB, S)
    c = {"title": title, "lede": lede, "axes": {"xmax": 110, "ymax": 110},
         "curves": [{"id": "S", "label": "S = MC = MSC", "pts": S},
                    {"id": "D", "label": "D = MB", "pts": D, "ldx": 6, "ldy": -8},
                    {"id": "MSB", "label": "MSB", "pts": MSB, "color": "red", "at": 1, "ldx": 6, "ldy": -8}],
         "points": [{"q": R(em[0]), "p": R(em[1]), "ql": "Qᴍ", "pl": "Pᴍ"},
                    {"q": R(ee[0]), "p": R(ee[1]), "ql": "Q*", "guides": "q", "showP": False, "color": "red", "at": 2},
                    {"q": R(em[0]), "p": R(mb(em[0]) + gap), "guides": False, "showP": False, "showQ": False, "at": 3}],
         "vbraces": [{"p1": R(mb(q_b)), "p2": R(mb(q_b) + gap), "q": q_b, "label": "MEB", "at": 1}],
         "areas": [{"pts": [[R(em[0]), R(em[1])], [R(em[0]), R(mb(em[0]) + gap)], [R(ee[0]), R(ee[1])]], "label": "DWL", "color": "red", "at": 3}],
         "steps": steps}
    c["points"][0]["hiAt"] = 3; c["points"][1]["hiAt"] = 3
    assert len(steps) == 4
    return c

# ------------------------------------------------- rent ceiling and PS ----
def ceiling_ps(title, lede, steps):
    pc = 30; qs, qd = pc, 100 - pc
    return {"title": title, "lede": lede, "axes": {"xmax": 110, "ymax": 110, "y": "Rent"},
            "curves": [{"id": "D", "label": "D", "pts": D_pts(), **D_label()}, {"id": "S", "label": "S", "pts": S_pts()}],
            "hlines": [{"p": pc, "tag": "Rent ceiling", "at": 1, "showP": False}],
            "points": [{"q": 50, "p": 50, "pl": "P₁", "ql": "Q₁"},
                       {"q": qs, "p": pc, "guides": "q", "ql": "Qₛ", "pl": "Pᶜ", "at": 1},
                       {"q": qd, "p": pc, "guides": "q", "ql": "Qᴅ", "showP": False, "at": 1}],
            "areas": [{"pts": [[0, 50], [0, 0], [50, 50]], "label": "PS", "color": "orange", "until": 2},
                      {"pts": [[0, pc], [0, 0], [qs, pc]], "label": "PS", "color": "orange", "at": 2}],
            "braces": [{"p": pc, "q1": qs, "q2": qd, "label": "Shortage", "below": "in", "at": 1}],
            "steps": steps}


def jane(title, lede, steps):
    """MC = $35 and ATC = $40 at 40 garages, the question's numbers, on an
    exact cost family: ATC = a(q - m)^2 + c with a(40 - m) = -1/16 makes
    MC(40) = ATC(40) - 5, and m = 50 puts 40 on MC's rising arm."""
    m = 50.0; a = 1 / (16 * (m - 40)); c = 40 - a * (40 - m) ** 2
    C = Cost(a, m, c)
    assert abs(C.atc(40) - 40) < 1e-9 and abs(C.mc(40) - 35) < 1e-9
    assert C.mc(41) > C.mc(40)                       # rising: 40 is a maximum, not a minimum
    atc = curve_of(C.atc, [12, 20, 30, 40, 50, 60, 70, 80])
    mc = [p for p in curve_of(C.mc, [26, 30, 34, 40, 46, 52, 58, 64, 70]) if p[1] <= 62]
    return {"title": title, "lede": lede, "axes": {"xmax": 90, "ymax": 64, "y": "Price and Cost", "x": "Garages per Week", "money": True},
            "curves": [{"id": "MC", "label": "MC", "pts": mc, "curved": True}, {"id": "ATC", "label": "ATC", "pts": atc, "curved": True},
                       {"id": "P", "label": "P = MR = $35", "pts": [[3, 35], [86, 35]]}],
            "points": [{"q": 40, "p": 35, "ql": "40", "showP": False, "guides": "q"},
                       {"q": 40, "p": 40, "pl": "$40", "guides": "p", "showQ": False, "at": 1}],
            "areas": [{"pts": [[0, 40], [40, 40], [40, 35], [0, 35]], "label": "Loss", "color": "red", "edge": True, "at": 1}],
            "steps": steps}
