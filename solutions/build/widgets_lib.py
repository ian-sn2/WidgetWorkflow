"""Widget shapes the exam solutions keep needing. Symbolic figures live on
110 x 110 axes with S: q = p and D: q = 100 - p, equilibrium at (50, 50),
the engine's own convention. Every numeric figure takes its numbers as
arguments and asserts the arithmetic it draws."""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / 'scripts'))
from curve_shapes import cross

# ------------------------------------------------------------- symbolic ----
def S_pts(d=0):      # q = p + d
    lo = max(8, 8 + d); hi = min(100, 100 + d)
    return [[lo, lo - d], [hi, hi - d]]
def D_pts(d=0):      # q = 100 + d - p, stopping short of the Q axis
    top = [8, 92 + d]; bot = [95 + d, 5]
    if top[1] > 100: top = [d, 100]
    return [top, bot]
def D_label(**k): return dict({"ldx": 6, "ldy": -8}, **k)

def shift(curve, d, title, lede, steps):
    return {"preset": "shift", "shift": curve, "dir": d, "title": title, "lede": lede, "steps": steps}

def four(title, lede="Pick a figure. Each shows one curve moving and the equilibrium it leads to."):
    return {"preset": "shift", "static": True, "title": title, "lede": lede, "scenarios": {
        "A": {"label": "Figure A", "shift": "D", "dir": "right", "caption": "Demand shifts right, from D₁ to D₂, and the equilibrium moves up along S."},
        "B": {"label": "Figure B", "shift": "D", "dir": "left", "caption": "Demand shifts left, from D₁ to D₂, and the equilibrium moves down along S."},
        "C": {"label": "Figure C", "shift": "S", "dir": "left", "caption": "Supply shifts left, from S₁ to S₂, and the equilibrium moves up along D."},
        "D": {"label": "Figure D", "shift": "S", "dir": "right", "caption": "Supply shifts right, from S₁ to S₂, and the equilibrium moves down along D."}}}

def dbl(demand, supply, title, lede, steps, bigger=None):
    """Both curves shift. bigger = None -> two compare panels; 'demand' or
    'supply' -> one panel with that shift the larger."""
    c = {"preset": "double", "demand": demand, "supply": supply, "title": title, "lede": lede, "steps": steps}
    if bigger is None:
        c.update({"compare": True, "big": 30, "small": 12, "arrowD": 12,
                  "headings": ["Larger Shift of Supply", "Larger Shift of Demand"]})
    else:
        c.update({"dD": 30 if bigger == "demand" else 12, "dS": 30 if bigger == "supply" else 12})
    return c

def two_market(h1, kind1, h2, dir2, title, lede, steps):
    """Market 1 changes (kind1: 'Dleft', 'Dright', or 'Pup' = a price rise read
    along S); market 2's supply shifts dir2. Five steps."""
    d = 24
    p1 = {"heading": h1, "axes": {"xmax": 110, "ymax": 110}}
    if kind1 == "Pup":
        # A price rise read along S. No movement arrow: between two readings
        # this close an arrow is all head (the checker says so at 16px), and
        # the chapter rule is that the dots and the caption carry the movement.
        # Four steps, so the price rise and the shift each change the drawing.
        p1["curves"] = [{"id": "D", "label": "D", "pts": D_pts(), **D_label()}, {"id": "S", "label": "S", "pts": S_pts()}]
        p1["points"] = [{"q": 50, "p": 50, "pl": "P₁", "ql": "Q₁"}, {"q": 66, "p": 66, "pl": "P₂", "ql": "Q₂", "color": "red", "at": 1}]
    else:
        dd = -d if kind1 == "Dleft" else d
        e2 = cross(D_pts(dd), S_pts())
        p1["curves"] = [{"id": "S", "label": "S", "pts": S_pts()},
                        {"id": "D1", "label": "D₁", "pts": D_pts(), **D_label()},
                        {"id": "D2", "label": "D₂", "pts": D_pts(dd), "color": "red", "from": "D1", "at": 1,
                         "arrowP": 60 if dd < 0 else 40, **D_label()}]
        p1["points"] = [{"q": 50, "p": 50, "pl": "P₁", "ql": "Q₁"}, {"q": e2[0], "p": e2[1], "pl": "P₂", "ql": "Q₂", "color": "red", "at": 2}]
    ds = -d if dir2 == "left" else d
    e3 = cross(D_pts(), S_pts(ds))
    a2 = 2 if kind1 == "Pup" else 3     # the step the second market's supply moves
    p2 = {"heading": h2, "axes": {"xmax": 110, "ymax": 110},
          "curves": [{"id": "D", "label": "D", "pts": D_pts(), **D_label()},
                     {"id": "S1", "label": "S₁", "pts": S_pts()},
                     {"id": "S2", "label": "S₂", "pts": S_pts(ds), "color": "red", "from": "S1", "at": a2, "arrowP": 88 if ds < 0 else 70}],
          "points": [{"q": 50, "p": 50, "pl": "P₁", "ql": "Q₁"}, {"q": e3[0], "p": e3[1], "pl": "P₂", "ql": "Q₂", "color": "red", "at": a2 + 1}]}
    assert len(steps) == a2 + 2
    return {"title": title, "lede": lede, "panels": [p1, p2], "steps": steps}

def _cs(P, Q): return [[0, P], [0, 100], [Q, P]]
def _ps(P, Q): return [[0, P], [0, 0], [Q, P]]

def surplus_shift(curve, d, show, title, lede, steps):
    """One curve shifts; the named surplus (CS, PS or total) is shaded before
    and after. Four steps: start + areas, shift, new equilibrium, new areas."""
    dd = 24 if d == "right" else -24
    if curve == "D":
        curves = [{"id": "S", "label": "S", "pts": S_pts()}, {"id": "D1", "label": "D₁", "pts": D_pts(), **D_label()},
                  {"id": "D2", "label": "D₂", "pts": D_pts(dd), "color": "red", "from": "D1", "at": 1, "arrowP": 40 if dd > 0 else 60, **D_label()}]
        e2 = cross(D_pts(dd), S_pts()); top2 = 100 + dd
    else:
        curves = [{"id": "D", "label": "D", "pts": D_pts(), **D_label()}, {"id": "S1", "label": "S₁", "pts": S_pts()},
                  {"id": "S2", "label": "S₂", "pts": S_pts(dd), "color": "red", "from": "S1", "at": 1, "arrowP": 70 if dd > 0 else 88}]
        e2 = cross(D_pts(), S_pts(dd)); top2 = 100
    q2, p2 = e2
    areas = []
    def cs(P, Q, top, at, until=None, lab="CS"):
        a = {"pts": [[0, P], [0, top], [Q, P]], "label": lab, "color": "teal"}
        if at: a["at"] = at
        if until is not None: a["until"] = until
        return a
    def ps(P, Q, at, until=None, lab="PS", bottom=0):
        a = {"pts": [[0, P], [0, bottom], [Q, P]], "label": lab, "color": "orange"}
        if at: a["at"] = at
        if until is not None: a["until"] = until
        return a
    s_bottom2 = -dd if curve == "S" else 0     # the shifted S meets the P axis at p = -d
    if show in ("CS", "TS"): areas += [cs(50, 50, 100, 0, 3), cs(p2, q2, top2, 3)]
    if show in ("PS", "TS"): areas += [ps(50, 50, 0, 3), ps(p2, q2, 3, bottom=s_bottom2)]
    pts = [{"q": 50, "p": 50, "pl": "P₁", "ql": "Q₁"}, {"q": q2, "p": p2, "pl": "P₂", "ql": "Q₂", "color": "red", "at": 2}]
    assert len(steps) == 4
    return {"title": title, "lede": lede, "axes": {"xmax": 110, "ymax": 110}, "curves": curves, "areas": areas, "points": pts, "steps": steps}

def ceiling(pc, title, lede, steps, dwl=True, tag="Price ceiling", xname=None, yname=None, pl=None):
    """A control price below equilibrium: the two readings, the shortage, and
    (dwl) the deadweight triangle. Steps: start; ceiling; readings + shortage;
    [deadweight loss]."""
    qs, qd = pc, 100 - pc
    c = {"title": title, "lede": lede, "axes": {"xmax": 110, "ymax": 110},
         "curves": [{"id": "D", "label": "D", "pts": D_pts(), **D_label()}, {"id": "S", "label": "S", "pts": S_pts()}],
         "hlines": [{"p": pc, "tag": tag, "at": 1, "showP": False}],
         "points": [{"q": 50, "p": 50, "pl": "P₁", "ql": "Q₁"},
                    {"q": qs, "p": pc, "guides": "q", "ql": "Qₛ", "pl": pl or "Pᶜ", "at": 2},
                    {"q": qd, "p": pc, "guides": "q", "ql": "Qᴅ", "showP": False, "at": 2}],
         "braces": [{"p": pc, "q1": qs, "q2": qd, "label": "Shortage", "below": "in", "at": 2}],
         "steps": steps}
    if xname: c["axes"]["x"] = xname
    if yname: c["axes"]["y"] = yname
    if dwl:
        c["areas"] = [{"pts": [[qs, pc], [qs, 100 - qs], [50, 50]], "label": "DWL", "color": "red", "at": 3}]
        c["points"][1]["hiAt"] = 3
        c["points"].append({"q": qs, "p": 100 - qs, "guides": False, "showP": False, "showQ": False, "at": 3})
    assert len(steps) == (4 if dwl else 3)
    return c

def ceilings_compare(title, lede):
    """Summer 2023 Q16: four rent ceilings against a $1,500 equilibrium. The
    rent axis is in dollars ($1,500 at 50 on the engine's scale); quantities
    are symbolic."""
    def sc(label, dollars, caption):
        # $1,500 at 50 and $12.50 a unit either side of it. At $30 a unit (a
        # scale from zero) the $1,400 ceiling sat 3 units under the market
        # rent and its deadweight loss was a sliver (Ian, 2026-11-05). The
        # axis names only $1,500, so its scale is the figure's to choose.
        # ($10 a unit put the $1,200 ceiling's shortage brace on the Q axis.)
        p = round(50 + (dollars - 1500) / 12.5, 1)
        base = {"label": label, "caption": caption,
                "curves": [{"id": "D", "label": "D", "pts": D_pts(), **D_label()}, {"id": "S", "label": "S", "pts": S_pts()}],
                "points": [{"q": 50, "p": 50, "pl": "$1,500", "ql": "Q₁"}]}
        if p < 50:
            qs = p
            base["hlines"] = [{"p": p, "tag": "$%s ceiling" % format(dollars, ","), "showP": False}]
            base["points"][0].update({"guides": "p", "showQ": False}); del base["points"][0]["ql"]
            base["points"] += [{"q": qs, "p": p, "guides": "q", "ql": "Qₛ", "showP": False}, {"q": 100 - p, "p": p, "guides": "q", "ql": "Qᴅ", "showP": False},
                               {"q": qs, "p": 100 - qs, "guides": False, "showP": False, "showQ": False}]
            # a ceiling just under the market rent leaves a sliver, named from outside
            base["areas"] = [{"pts": [[qs, p], [qs, 100 - qs], [50, 50]], "label": "DWL", "color": "red", **({"lp": [p - 7, 50]} if p > 38 else {})}]
            base["braces"] = [{"p": p, "q1": qs, "q2": 100 - p, "label": "Shortage", "below": "in"}]
        elif p > 50:
            base["hlines"] = [{"p": min(p, 92), "tag": "$%s ceiling" % format(dollars, ","), "tagq": 28, "showP": False}]
        else:
            base["hlines"] = [{"p": p, "tag": "$1,500 ceiling", "showP": False}]
        return base
    return {"title": title, "lede": lede, "axes": {"xmax": 110, "ymax": 110, "y": "Rent"}, "scenarios": {
        "a": sc("$2,800 ceiling", 2800, "A ceiling above the $1,500 equilibrium rent does not bind. The market clears at $1,500 and there is no deadweight loss."),
        "b": sc("$1,500 ceiling", 1500, "A ceiling at the equilibrium rent changes nothing: the quantity rented is still Q₁, so there is no deadweight loss."),
        "c": sc("$1,400 ceiling", 1400, "At $1,400 landlords offer fewer apartments than at the market rent, so some units that would have been rented are not. That lost surplus is the deadweight loss."),
        "d": sc("$1,200 ceiling", 1200, "At $1,200 the quantity supplied falls further still, so more trades are lost and the deadweight loss is the largest of the four.")}}

def ceiling_demand_up(title, lede, steps):
    """A rent ceiling, then demand rises: the quantity rented stays at Qₛ and
    the deadweight loss grows."""
    pc = 30; qs = pc; dd = 24
    e2 = cross(D_pts(dd), S_pts())
    return {"title": title, "lede": lede, "axes": {"xmax": 110, "ymax": 110, "y": "Rent"},
            "curves": [{"id": "S", "label": "S", "pts": S_pts()}, {"id": "D1", "label": "D₁", "pts": D_pts(), **D_label()},
                       {"id": "D2", "label": "D₂", "pts": D_pts(dd), "color": "red", "from": "D1", "at": 2, "arrowP": 80, **D_label()}],
            "hlines": [{"p": pc, "tag": "Ceiling", "tagq": 50, "showP": False}],
            "points": [{"q": 50, "p": 50, "pl": "P₁", "ql": "Q₁"},
                       {"q": qs, "p": pc, "guides": "q", "ql": "Qₛ", "pl": "Pᶜ"},
                       {"q": qs, "p": 100 - qs, "guides": False, "showP": False, "showQ": False, "at": 1},
                       {"q": e2[0], "p": e2[1], "pl": "P₂", "ql": "Q₂", "color": "red", "at": 3},
                       {"q": qs, "p": 100 + dd - qs, "guides": False, "showP": False, "showQ": False, "at": 3}],
            "areas": [{"pts": [[qs, pc], [qs, 100 - qs], [50, 50]], "label": "DWL", "color": "red", "at": 1, "until": 3},
                      {"pts": [[qs, pc], [qs, 100 + dd - qs], [e2[0], e2[1]]], "label": "DWL", "color": "red", "at": 3}],
            "steps": steps}

def floor_labor(title, lede, steps):
    pf = 64; qd, qs = 100 - pf, pf
    return {"title": title, "lede": lede, "axes": {"xmax": 110, "ymax": 110, "x": "Labor", "y": "Wage"},
            "curves": [{"id": "D", "label": "D", "pts": D_pts(), **D_label()}, {"id": "S", "label": "S", "pts": S_pts()}],
            "hlines": [{"p": pf, "tag": "Minimum wage", "at": 1, "showP": False}],
            "points": [{"q": 50, "p": 50, "pl": "W₁", "ql": "L₁"},
                       {"q": qd, "p": pf, "guides": "q", "ql": "Lᴅ", "pl": "Wᵐ", "at": 2},
                       {"q": qs, "p": pf, "guides": "q", "ql": "Lₛ", "showP": False, "at": 2}],
            "braces": [{"p": pf, "q1": qd, "q2": qs, "label": "Unemployment", "at": 2}],
            "steps": steps}

def p1_by_dot(pn, i=0, **at):
    """Name a panel's equilibrium P₁ beside its dot instead of on the price
    axis, where a price a few units away would crowd it. `pl` goes as well
    as `showP`: the engine prints a point's `pl` on the axis whatever `showP`
    says, which is how the first version of this drew P₁ twice. Its
    horizontal guide goes too, since it would end at a blank spot on the
    axis (CLAUDE.md: a guide needs a number at its foot)."""
    pt = pn["points"][i]; pt.pop("pl", None)
    pt.update({"showP": False, "label": "P₁", "guides": "q"}, **at)
    return pn

def tax(title, lede, steps, scenarios=True, t=30):
    """A tax on sellers shifts S up by t. With scenarios, an inelastic (steep)
    and an elastic (flat) demand curve, same tax, so the split is seen."""
    def panel(D, dlabel):
        S1 = S_pts(); S2 = [[8, 8 + t], [100 - t - 6, 94]]      # p = q + t, stopping short of S's end
        e1 = cross(D, S1); e2 = cross(D, S2)
        q2, pb = e2; ps = pb - t; w = e1[0] - q2
        return {"curves": [{"id": "D", "label": "D", "pts": D, **D_label()},
                           {"id": "S1", "label": "S", "pts": S1},
                           {"id": "S2", "label": "S + tax", "pts": S2, "color": "red", "from": "S1", "at": 1, "arrowP": 84, "dimAt": 2}],
                "points": [{"q": e1[0], "p": e1[1], "pl": "P₁", "ql": "Q₁"},
                           {"q": q2, "p": pb, "pl": "Pᵇ", "ql": "Q₂", "color": "red", "at": 2},
                           {"q": q2, "p": ps, "pl": "Pˢ", "guides": "p", "showQ": False, "at": 2}],
                "vbraces": [{"p1": ps, "p2": pb, "q": q2, "label": "Tax", "side": "left", "at": 2}],
                "areas": [{"pts": [[q2, pb], [e1[0], e1[1]], [q2, ps]], "label": "DWL", "color": "red",
                           "lp": [q2 + w * 0.3, (pb + ps) / 2.0 + 6] if w >= 12 else [q2 + w / 2.0, ps - 9], "at": 3}]}
    base = {"title": title, "lede": lede, "axes": {"xmax": 110, "ymax": 110}, "steps": steps}
    if not scenarios:
        base.update(panel(D_pts(), "D")); return base
    steep = [[30, 100], [70, 8]]       # slope -2.3 through (50, 50)
    flat = [[8, 60.5], [100, 37.5]]    # slope -1/4 through (50, 50)
    for D in (steep, flat): assert abs(cross(D, S_pts())[0] - 50) < 1.5
    # Whichever side bears less of the tax has its price close to P₁ -- the
    # sellers' on the steep curve, the buyers' on the flat one -- so the two
    # would crowd the price axis. P₁ is named beside its dot instead.
    st = p1_by_dot(panel(steep, "D"), dx=10, dy=4)
    el = p1_by_dot(panel(flat, "D"), dx=12, dy=18)
    base["scenarios"] = {"in": dict({"label": "Inelastic demand (steep)"}, **st),
                         "el": dict({"label": "Elastic demand (flat)"}, **el)}
    return base

def subsidy(title, lede, steps, s=20):
    S1 = S_pts(); S2 = [[8 + s, 8], [100, 100 - s]]         # p = q - s
    e2 = cross(D_pts(), S2); q2, pc = e2; pp = pc + s
    # P₁ sits between Pᶜ and Pᵖ, a few units from each, so it is named
    # beside its dot rather than on the crowded axis.
    return p1_by_dot({"title": title, "lede": lede, "axes": {"xmax": 110, "ymax": 110},
            "curves": [{"id": "D", "label": "D", "pts": D_pts(), **D_label()}, {"id": "S1", "label": "S", "pts": S1},
                       {"id": "S2", "label": "S − subsidy", "pts": S2, "color": "red", "from": "S1", "at": 1, "arrowP": 30, "dimAt": 2}],
            "points": [{"q": 50, "p": 50, "pl": "P₁", "ql": "Q₁"},
                       {"q": q2, "p": pc, "pl": "Pᶜ", "ql": "Q₂", "color": "red", "at": 2},
                       {"q": q2, "p": pp, "pl": "Pᵖ", "guides": "p", "showQ": False, "at": 2}],
            "vbraces": [{"p1": pc, "p2": pp, "q": q2, "label": "Subsidy", "at": 2}],
            "steps": steps}, dx=10, dy=4)

def quota(title, lede, steps, qq=30, binding=True):
    if not binding:
        return {"title": title, "lede": lede, "axes": {"xmax": 110, "ymax": 110},
                "curves": [{"id": "D", "label": "D", "pts": D_pts(), **D_label()}, {"id": "S", "label": "S", "pts": S_pts()},
                           {"id": "Q", "label": "Quota", "pts": [[66, 8], [66, 100]], "color": "red", "at": 1, "ldx": 4, "ldy": -4}],
                "points": [{"q": 50, "p": 50, "pl": "P₁", "ql": "Q₁"}], "steps": steps}
    pq = 100 - qq; ps = qq
    return {"title": title, "lede": lede, "axes": {"xmax": 110, "ymax": 110},
            "curves": [{"id": "D", "label": "D", "pts": D_pts(), **D_label()}, {"id": "S", "label": "S", "pts": S_pts()},
                       {"id": "Q", "label": "Quota", "pts": [[qq, 8], [qq, 100]], "color": "red", "at": 1, "ldx": 4, "ldy": -4}],
            "points": [{"q": 50, "p": 50, "pl": "P₁", "ql": "Q₁"},
                       {"q": qq, "p": pq, "pl": "P₂", "ql": "Qᵠ", "guides": "p", "showQ": False, "color": "red", "at": 2},
                       {"q": qq, "p": ps, "guides": False, "showP": False, "showQ": False, "at": 3}],
            "areas": [{"pts": [[qq, pq], [50, 50], [qq, ps]], "label": "DWL", "color": "red", "lp": [qq + 7, 56], "at": 3}],
            "steps": steps}

def trade(kind, title, lede, steps):
    """imports: world price below P₁; exports: above. Steps: no trade with
    CS/PS; world price and the two readings; trade and the new areas."""
    pw = 30 if kind == "imports" else 70
    qs, qd = pw, 100 - pw
    lo, hi = min(qs, qd), max(qs, qd)
    c = {"title": title, "lede": lede, "axes": {"xmax": 110, "ymax": 110},
         "curves": [{"id": "D", "label": "D", "pts": D_pts(), **D_label()}, {"id": "S", "label": "S", "pts": S_pts()}],
         "hlines": [{"p": pw, "tag": "World price", "at": 1, "showP": False}],
         "points": [{"q": 50, "p": 50, "pl": "P₁", "ql": "Q₁"},
                    {"q": qs, "p": pw, "guides": "q", "ql": "Qₛ", "pl": "Pᵂ", "at": 1},
                    {"q": qd, "p": pw, "guides": "q", "ql": "Qᴅ", "showP": False, "at": 1}],
         "areas": [{"pts": _cs(50, 50), "label": "CS", "color": "teal", "until": 2},
                   {"pts": _ps(50, 50), "label": "PS", "color": "orange", "until": 2},
                   {"pts": _cs(pw, qd), "label": "CS", "color": "teal", "at": 2},
                   {"pts": _ps(pw, qs), "label": "PS", "color": "orange", "at": 2}],
         "braces": [{"p": pw, "q1": lo, "q2": hi, "label": "Imports" if kind == "imports" else "Exports",
                     "below": True if kind == "imports" else None, "at": 2}],
         "steps": steps}
    if c["braces"][0]["below"] is None: del c["braces"][0]["below"]
    assert len(steps) == 3
    return c

def tariff(title, lede, steps, kind="tariff", pw=30, t=12):
    pt = pw + t
    qs1, qd1 = pw, 100 - pw
    qs2, qd2 = pt, 100 - pt
    band = "Tariff\nrevenue" if kind == "tariff" else "Importers'\nprofit"
    c = {"title": title, "lede": lede, "axes": {"xmax": 110, "ymax": 110},
         "curves": [{"id": "D", "label": "D", "pts": D_pts(), **D_label()}, {"id": "S", "label": "S", "pts": S_pts()}],
         "hlines": [{"p": pw, "tag": "World price", "showP": False},
                    {"p": pt, "tag": "World price + tariff" if kind == "tariff" else "Price with quota", "showP": False, "at": 1}],
         "points": [{"q": qs1, "p": pw, "guides": "q", "ql": "Qₛ", "pl": "Pᵂ"},
                    {"q": qd1, "p": pw, "guides": "q", "ql": "Qᴅ", "showP": False},
                    {"q": qs2, "p": pt, "guides": "q", "ql": "Qₛ′", "pl": "Pᵀ" if kind == "tariff" else "Pᵠ", "at": 1},
                    {"q": qd2, "p": pt, "guides": "q", "ql": "Qᴅ′", "showP": False, "at": 1}],
         "areas": [{"pts": _cs(pw, qd1), "label": "CS", "color": "teal", "until": 2},
                   {"pts": _ps(pw, qs1), "label": "PS", "color": "orange", "until": 2},
                   {"pts": _cs(pt, qd2), "label": "CS", "color": "teal", "at": 2},
                   {"pts": _ps(pt, qs2), "label": "PS", "color": "orange", "at": 2},
                   {"pts": [[qs2, pw], [qs2, pt], [qd2, pt], [qd2, pw]], "label": band.replace("\n", " "), "color": "navy", "lp": [50, pw - 10], "at": 3},
                   {"pts": [[qs1, pw], [qs2, pt], [qs2, pw]], "label": "", "color": "red", "at": 3},
                   {"pts": [[qd2, pw], [qd2, pt], [qd1, pw]], "label": "", "color": "red", "at": 3}],
         "braces": [{"p": pw, "q1": qs1, "q2": qd1, "label": "Imports before", "below": True, "until": 1},
                    {"p": pt, "q1": qs2, "q2": qd2, "label": "Imports after", "below": True, "at": 1}],
         "steps": steps}
    assert len(steps) == 4
    return c

def vertical_demand(title, lede, steps=None, caption=None, shift=False):
    c = {"title": title, "lede": lede, "axes": {"xmax": 110, "ymax": 110},
         "curves": [{"id": "D", "label": "D", "pts": [[50, 8], [50, 100]], "ldx": 6, "ldy": -4}]}
    if shift:
        c["curves"] += [{"id": "S1", "label": "S₁", "pts": S_pts()},
                        {"id": "S2", "label": "S₂", "pts": S_pts(-24), "color": "red", "from": "S1", "at": 1, "arrowP": 88}]
        c["points"] = [{"q": 50, "p": 50, "pl": "P₁", "ql": "Q₁", "guides": "p"}, {"q": 50, "p": 74, "pl": "P₂", "guides": "p", "showQ": False, "color": "red", "at": 2}]
        c["steps"] = steps
    else:
        c["points"] = [{"q": 50, "p": 50, "dot": False, "ql": "Q₁", "guides": False}]
        c["caption"] = caption
    return c

def horizontal_demand(title, lede, caption):
    return {"title": title, "lede": lede, "axes": {"xmax": 110, "ymax": 110},
            "curves": [{"id": "D", "label": "D", "pts": [[8, 50], [100, 50]]}],
            "points": [{"q": 50, "p": 50, "dot": False, "pl": "P₁", "guides": "p", "showQ": False}],
            "caption": caption}

def steep_vs_flat(title, lede, steps):
    """Supply shifts left against an inelastic (steep) and an elastic (flat)
    demand curve: the price rises more on the steep one."""
    steep = [[30, 100], [70, 8]]; flat = [[8, 64], [100, 33.3]]
    def sc(label, D):
        e1 = cross(D, S_pts()); e2 = cross(D, S_pts(-24))
        return {"label": label,
                "curves": [{"id": "D", "label": "D", "pts": D, **D_label()}, {"id": "S1", "label": "S₁", "pts": S_pts()},
                           {"id": "S2", "label": "S₂", "pts": S_pts(-24), "color": "red", "from": "S1", "at": 1, "arrowP": 88}],
                "points": [{"q": e1[0], "p": e1[1], "pl": "P₁", "ql": "Q₁"}, {"q": e2[0], "p": e2[1], "pl": "P₂", "ql": "Q₂", "color": "red", "at": 2}]}
    return {"title": title, "lede": lede, "axes": {"xmax": 110, "ymax": 110}, "steps": steps,
            # On the flat curve the price barely rises, so P₁ and P₂ would
            # share the axis: P₁ is named beside its dot.
            "scenarios": {"in": sc("Inelastic demand (steep)", steep),
                          "el": p1_by_dot(sc("Elastic demand (flat)", flat), dx=10, dy=16)}}

def tr_test(title, lede, steps):
    return {"title": title, "lede": lede, "link": False, "panels": [
        {"heading": "Demand", "axes": {"xmax": 120, "ymax": 120},
         "curves": [{"id": "D", "label": "D", "pts": [[0, 110], [110, 0]], "ldx": -123, "ldy": -45}],
         "points": [{"q": 0, "p": 110, "label": "E = ∞", "dx": 9, "dy": -4, "guides": False, "showP": False, "showQ": False},
                    {"q": 110, "p": 0, "label": "E = 0", "dx": 9, "dy": -6, "guides": False, "showP": False, "showQ": False},
                    {"q": 55, "p": 55, "label": "E = 1", "at": 1, "dx": 10, "dy": -10, "guides": False, "showP": False, "showQ": False},
                    {"q": 30, "p": 80, "label": "E > 1", "at": 2, "dx": 10, "dy": -10, "guides": False, "showP": False, "showQ": False},
                    {"q": 80, "p": 30, "label": "E < 1", "at": 3, "dx": 10, "dy": -10, "guides": False, "showP": False, "showQ": False}]},
        {"heading": "Total Revenue", "axes": {"x": "Q", "y": "TR", "xmax": 120, "ymax": 120},
         "curves": [{"id": "TR", "label": "", "pts": [[0, 0], [20, 65.5], [40, 101.8], [55, 110], [70, 101.8], [90, 65.5], [110, 0]], "curved": True}],
         "points": [{"q": 55, "p": 110, "at": 1, "guides": False, "showP": False, "showQ": False}]}],
        "steps": steps}

def along_line(title, lede, steps):
    return {"title": title, "lede": lede, "axes": {"xmax": 110, "ymax": 110},
            "curves": [{"id": "D", "label": "D", "pts": [[0, 100], [100, 0]], "lstart": True, "ldx": 10, "ldy": -6}],
            "points": [{"q": 10, "p": 90, "label": "E > 1", "at": 1, "dx": 10, "dy": -8, "guides": False, "showP": False, "showQ": False},
                       {"q": 50, "p": 50, "label": "E = 1", "at": 2, "dx": 10, "dy": -8, "guides": False, "showP": False, "showQ": False},
                       {"q": 90, "p": 10, "label": "E < 1", "at": 3, "dx": 10, "dy": -8, "guides": False, "showP": False, "showQ": False}],
            "steps": steps}

def movement(title, lede, steps):
    return {"title": title, "lede": lede, "axes": {"xmax": 110, "ymax": 110},
            "curves": [{"id": "D", "label": "D", "pts": D_pts(), **D_label()}],
            "points": [{"q": 60, "p": 40, "pl": "P₁", "ql": "Q₁"}, {"q": 36, "p": 64, "pl": "P₂", "ql": "Q₂", "color": "red", "at": 1}],
            "moves": [{"from": [57, 43], "to": [39, 61], "at": 1, "offset": 14}],
            "steps": steps}

def msb_msc(title, lede, steps=None, caption=None, shift=None, mark=None):
    """Symbolic efficient quantity. shift='MSCdown' moves MSC right. mark =
    (q, msb, msc) names readings at one quantity (numeric axes)."""
    if mark:
        q, b, c_ = mark
        xmax, ymax = q * 2.2, max(b, c_) * 1.8
        MSB = [[0, b + 0.4 * b], [xmax, b - 0.4 * b * (xmax - q) / q]]
        MSC = [[0, c_ - 0.4 * c_], [xmax, c_ + 0.4 * c_ * (xmax - q) / q]]
        e = cross(MSB, MSC)
        return {"title": title, "lede": lede, "axes": {"xmax": xmax, "ymax": ymax, "money": True},
                "curves": [{"id": "MSB", "label": "MSB", "pts": MSB, "ldx": 6, "ldy": -6}, {"id": "MSC", "label": "MSC", "pts": MSC}],
                "points": [{"q": q, "p": b, "guides": "q"}, {"q": q, "p": c_, "guides": "p", "showQ": False},
                           {"q": e[0], "p": e[1], "ql": "Efficient", "guides": "q", "showP": False, "color": "red", "at": 1}],
                "steps": steps}
    MSB = [[8, 92], [95, 5]]; MSC = S_pts()
    c = {"title": title, "lede": lede, "axes": {"xmax": 110, "ymax": 110},
         "curves": [{"id": "MSB", "label": "MSB", "pts": MSB, "ldx": 6, "ldy": -8}, {"id": "MSC1", "label": "MSC" if not shift else "MSC₁", "pts": MSC}],
         "points": [{"q": 50, "p": 50, "ql": "Efficient", "guides": "q", "showP": False}]}
    if shift == "MSCdown":
        e2 = cross(MSB, S_pts(24))
        c["curves"].append({"id": "MSC2", "label": "MSC₂", "pts": S_pts(24), "color": "red", "from": "MSC1", "at": 1, "arrowP": 70})
        c["points"][0]["ql"] = "Q₁"
        c["points"].append({"q": e2[0], "p": e2[1], "ql": "Q₂", "guides": "q", "showP": False, "color": "red", "at": 2})
        c["steps"] = steps
    else:
        c["caption"] = caption
    return c

# -------------------------------------------------------------- numeric ----
def midpoint(qa, pa, qb, pb, title, lede, steps, unit="units", E=None):
    """Two readings on a demand curve and the midpoint elasticity."""
    dq, dp = qb - qa, pb - pa
    mq, mp = (qa + qb) / 2.0, (pa + pb) / 2.0
    pq, pp = 100.0 * dq / mq, 100.0 * dp / mp
    e = abs(pq / pp)
    if E is not None: assert abs(e - E) < 0.006, (e, E)
    slope = dp / float(dq)
    qlo, qhi = min(qa, qb), max(qa, qb)
    span = qhi - qlo
    x0, x1 = qlo - 0.75 * span, qhi + 0.5 * span
    y0, y1 = pa + slope * (x0 - qa), pa + slope * (x1 - qa)
    xmax = qhi + 1.0 * span; ymax = max(y0, y1) * 1.12
    fmtq = lambda v: ("%g" % v)
    fmtp = lambda v: ("$%g" % v) if v == int(v) else ("$%.2f" % v)
    pct = lambda v: ("%g%%" % round(v, 2))
    A, B = ([qa, pa], [qb, pb]) if pb > pa else ([qb, pb], [qa, pa])   # A is the higher-price point
    up = A if A[0] == qa else B
    c = {"title": title, "lede": lede, "axes": {"xmax": round(xmax, 2), "ymax": round(ymax, 2), "money": True},
         "curves": [{"id": "D", "label": "D", "pts": [[round(x0, 2), round(y0, 2)], [round(x1, 2), round(y1, 2)]], "ldx": 6, "ldy": -8}],
         "points": [{"q": qa, "p": pa, "label": "A", "dx": 9, "dy": -9}, {"q": qb, "p": pb, "label": "B", "dx": 9, "dy": -9}],
         "braces": [{"p": 0, "q1": qlo, "q2": qhi, "label": "%s %s, a %s %s" % (fmtq(abs(dq)), "more" if dq > 0 else "fewer", pct(abs(pq)), "rise" if dq > 0 else "fall"), "below": True, "at": 1}],
         "vbraces": [{"p1": min(pa, pb), "p2": max(pa, pb), "q": qlo, "label": "%s %s, a %s %s" % (fmtp(abs(dp)), "less" if dp < 0 else "more", pct(abs(pp)), "fall" if dp < 0 else "rise"), "side": "left", "at": 2}],
         "calcs": [{"text": "%%ΔQ = %s ÷ %s = %s" % (fmtq(abs(dq)), fmtq(mq), pct(abs(pq))), "at": 1},
                   {"text": "%%ΔP = %s ÷ %s = %s" % (fmtp(abs(dp)), fmtp(mp), pct(abs(pp))), "at": 2},
                   {"text": "Elasticity = %s ÷ %s = %s" % (pct(abs(pq)), pct(abs(pp)), ("%.2f" % e).rstrip("0").rstrip(".") if e != int(e) else "%d" % e), "at": 2}],
         "steps": steps}
    return c

def ppf_table(pts, labels, i0, i1, xname, yname, xunit, yunit, title, lede, steps, cost):
    """Points of a table on a frontier; the move from pts[i0] to pts[i1]."""
    (x0, y0), (x1, y1) = pts[i0], pts[i1]
    gain, lose = x1 - x0, y0 - y1
    assert gain > 0 and lose > 0
    per = lose / float(gain)
    assert abs(per - cost) < 1e-9, (per, cost)
    xmax = max(p[0] for p in pts) * 1.35; ymax = max(p[1] for p in pts) * 1.12
    xt = sorted(set(p[0] for p in pts)); yt = sorted(set(p[1] for p in pts))
    c = {"title": title, "lede": lede,
         "axes": {"x": xname, "y": yname, "xmax": round(xmax, 1), "ymax": round(ymax, 1), "xticks": xt, "yticks": yt},
         "curves": [{"id": "PPF", "label": "", "pts": [list(p) for p in pts], "curved": len(pts) > 2}],
         "points": [], "moves": [{"from": [x0, y0], "to": [x1, y1], "at": 1, "offset": -15}],
         "braces": [{"p": ymax * 0.05, "q1": x0, "q2": x1, "label": "%g %s gained" % (gain, xunit), "below": True, "at": 1}],
         "vbraces": [{"p1": y1, "p2": y0, "label": "%g %s given up" % (lose, yunit), "left": True, "at": 2}],
         "calcs": [{"text": "Cost of one %s = %g %s ÷ %g %s = %s %s" % (xunit.rstrip("s"), lose, yunit, gain, xunit, ("%g" % per), yunit), "at": 2}],
         "steps": steps}
    for i, (p, lab) in enumerate(zip(pts, labels)):
        pt = {"q": p[0], "p": p[1], "label": lab}
        if p[0] == 0 or p[1] == 0: pt.update({"dx": 8, "dy": -6, "guides": False})
        else: pt.update({"dx": -22, "dy": 15})
        c["points"].append(pt)
    return c

def ppf_two(a, b, xname, yname, xunit, yunit, title, lede, steps, cost):
    """Two stated points on a frontier, a straight segment between them."""
    (x0, y0), (x1, y1) = a, b
    gain, lose = x1 - x0, y0 - y1
    per = lose / float(gain); assert abs(per - cost) < 1e-9, (per, cost)
    xmax = x1 * 1.45; ymax = y0 * 1.18
    return {"title": title, "lede": lede,
            "axes": {"x": xname, "y": yname, "xmax": round(xmax, 1), "ymax": round(ymax, 1)},
            "curves": [{"id": "PPF", "label": "PPF", "pts": [[x0, y0], [x1, y1]], "lstart": True, "ldx": -8, "ldy": -10}],
            "points": [{"q": x0, "p": y0, "label": "A", "dx": -22, "dy": 15}, {"q": x1, "p": y1, "label": "B", "dx": -22, "dy": 15}],
            "moves": [{"from": [x0, y0], "to": [x1, y1], "at": 1, "offset": -15}],
            "braces": [{"p": ymax * 0.05, "q1": x0, "q2": x1, "label": "%g %s gained" % (gain, xunit), "below": True, "at": 1}],
            "vbraces": [{"p1": y1, "p2": y0, "label": "%g %s given up" % (lose, yunit), "left": True, "at": 2}],
            "calcs": [{"text": "Cost of one %s = %g %s ÷ %g %s = %g %s" % (xunit.rstrip("s") if xunit != "loaves" else "loaf", lose, yunit, gain, xunit, per, yunit), "at": 2}],
            "steps": steps}

def ppf_shift(xname, yname, title, lede, steps):
    return {"title": title, "lede": lede, "axes": {"x": xname, "y": yname, "xmax": 125, "ymax": 125},
            "curves": [{"id": "PPF1", "label": "PPF₁", "pts": [[0, 90], [90, 0]], "ldx": -30, "ldy": 15},
                       {"id": "PPF2", "label": "PPF₂", "pts": [[0, 115], [115, 0]], "color": "red", "from": "PPF1", "at": 1, "arrowP": 45, "ldx": 9, "ldy": -8}],
            "steps": steps}

def ppf_points(title, lede, caption):
    return {"title": title, "lede": lede, "axes": {"x": "Good X", "y": "Good Y", "xmax": 110, "ymax": 110},
            "curves": [{"id": "PPF", "label": "PPF", "pts": [[0, 100], [30, 94], [60, 78], [85, 48], [100, 0]], "curved": True, "ldx": 6, "ldy": -6}],
            "points": [{"q": 35, "p": 40, "label": "Attainable,\ninefficient", "dx": 10, "dy": 4, "guides": False, "showP": False, "showQ": False},
                       {"q": 60, "p": 78, "label": "On the frontier", "dx": 10, "dy": 4, "guides": False, "showP": False, "showQ": False},
                       {"q": 92, "p": 90, "label": "Unattainable", "dx": 10, "dy": 4, "guides": False, "showP": False, "showQ": False}],
            "caption": caption}

def ppf_bowed(xname, yname, title, lede, steps):
    pts = [[0, 100], [25, 95], [50, 80], [75, 50], [100, 0]]
    return {"title": title, "lede": lede, "axes": {"x": xname, "y": yname, "xmax": 110, "ymax": 110},
            "curves": [{"id": "PPF", "label": "", "pts": pts, "curved": True}],
            "points": [{"q": 25, "p": 95, "label": "A", "dx": -22, "dy": 15, "guides": False, "showP": False, "showQ": False},
                       {"q": 50, "p": 80, "label": "B", "dx": -22, "dy": 15, "guides": False, "showP": False, "showQ": False},
                       {"q": 75, "p": 50, "label": "C", "dx": -22, "dy": 15, "guides": False, "showP": False, "showQ": False}],
            "moves": [{"from": [25, 95], "to": [50, 80], "at": 1, "offset": -15}, {"from": [50, 80], "to": [75, 50], "at": 2, "offset": -15}],
            "vbraces": [{"p1": 80, "p2": 95, "label": "Less soda\ngiven up", "left": True, "at": 1, "until": 2},
                        {"p1": 50, "p2": 80, "label": "More soda\ngiven up", "left": True, "at": 2}],
            "braces": [{"p": 5, "q1": 25, "q2": 50, "label": "Extra pizza", "below": True, "at": 1, "until": 2},
                       {"p": 5, "q1": 50, "q2": 75, "label": "Extra pizza", "below": True, "at": 2}],
            "steps": steps}
