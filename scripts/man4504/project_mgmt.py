"""MAN4504 Exam 3, Chapter 3 (Rest of Project Management): figures to code, in colour.

    python scripts/man4504/project_mgmt.py SOURCE.html OUTDIR

Every number the widgets show is computed here from the activity table and
checked against the values the notes print (the ES/EF/LS/LF table, the path
lengths, the crashed network, the PERT table, the z-values), so a figure
cannot drift from the prose beside it.
"""
import json, math, os, sys
from decimal import Decimal, ROUND_HALF_UP

IMG = "https://smokinnotes.s3.us-east-1.amazonaws.com/public/man4504-253-exam3-chapter3-"

# ---------------------------------------------------------------- the CPM network
DUR = {"Start": 0, "A": 2, "B": 3, "C": 2, "D": 4, "E": 4, "F": 3, "G": 5, "H": 2}
PRED = {"Start": [], "A": ["Start"], "B": ["Start"], "C": ["A"], "D": ["A", "B"], "E": ["C"], "F": ["C"],
        "G": ["D", "E"], "H": ["F", "G"]}
ORDER = ["Start", "A", "B", "C", "D", "E", "F", "G", "H"]
POS = {"Start": [0, 1], "A": [1, 0], "B": [1, 2], "C": [2, 0], "D": [2, 2], "E": [2.75, 1], "F": [3.5, 0],
       "G": [3.5, 2], "H": [4.5, 1]}
EDGES = [(p, n) for n in ORDER for p in PRED[n]]
SUCC = {n: [m for m in ORDER if n in PRED[m]] for n in ORDER}


def cpm(dur):
    es, ef, ls, lf = {}, {}, {}, {}
    for n in ORDER:
        es[n] = max((ef[p] for p in PRED[n]), default=0); ef[n] = es[n] + dur[n]
    end = max(ef.values())
    for n in reversed(ORDER):
        lf[n] = min((ls[s] for s in SUCC[n]), default=end); ls[n] = lf[n] - dur[n]
    return es, ef, ls, lf


ES, EF, LS, LF = cpm(DUR)
# the notes' Step 5 table, row by row: ES, EF, LS, LF, slack
TABLE = {"A": (0, 2, 0, 2, 0), "B": (0, 3, 1, 4, 1), "C": (2, 4, 2, 4, 0), "D": (3, 7, 4, 8, 1),
         "E": (4, 8, 4, 8, 0), "F": (4, 7, 10, 13, 6), "G": (8, 13, 8, 13, 0), "H": (13, 15, 13, 15, 0)}
for n, row in TABLE.items():
    assert (ES[n], EF[n], LS[n], LF[n], LS[n] - ES[n]) == row, n
    assert LF[n] - EF[n] == LS[n] - ES[n]
CRIT = [n for n in ORDER if n != "Start" and LS[n] == ES[n]]
assert CRIT == ["A", "C", "E", "G", "H"]


def paths(n="Start"):
    if not SUCC[n]: return [[n]]
    return [[n] + p for s in SUCC[n] for p in paths(s)]


PATHS = [p[1:] for p in paths()]
PATH_LEN = {"→".join(p): sum(DUR[x] for x in p) for p in PATHS}
assert PATH_LEN == {"A→C→F→H": 9, "A→C→E→G→H": 15, "A→D→G→H": 13, "B→D→G→H": 14}, PATH_LEN

# crashing A by one week (the notes' crashed network)
DUR_X = dict(DUR, A=1)
XES, XEF, XLS, XLF = cpm(DUR_X)
CRASHED = {"A": (0, 1, 0, 1), "B": (0, 3, 0, 3), "C": (1, 3, 1, 3), "D": (3, 7, 3, 7), "E": (3, 7, 3, 7),
           "F": (3, 6, 9, 12), "G": (7, 12, 7, 12), "H": (12, 14, 12, 14)}
for n, row in CRASHED.items(): assert (XES[n], XEF[n], XLS[n], XLF[n]) == row, n
XCRIT = [n for n in ORDER if n != "Start" and XLS[n] == XES[n]]
assert XCRIT == ["A", "B", "C", "D", "E", "G", "H"]
CRASH = {"A": (2, 1, 22000, 22750), "B": (3, 1, 30000, 34000), "C": (2, 1, 26000, 27000), "D": (4, 3, 48000, 49000),
         "E": (4, 2, 56000, 58000), "F": (3, 2, 30000, 30500), "G": (5, 2, 80000, 84500), "H": (2, 1, 16000, 19000)}
PER_WEEK = {n: (cc - nc) // (nt - ct) for n, (nt, ct, nc, cc) in CRASH.items()}
assert PER_WEEK == {"A": 750, "B": 2000, "C": 1000, "D": 1000, "E": 1000, "F": 500, "G": 1500, "H": 3000}
assert min(CRIT, key=PER_WEEK.get) == "A"


def edge_key(a, b): return f"{a}>{b}"


def is_crit_edge(a, b, es, ef, ls, lf):
    """an arrow is on a critical path when both ends have no slack and the tail's finish is the head's start"""
    ok = lambda n: n == "Start" or ls[n] == es[n]
    return ok(a) and ok(b) and ef[a] == es[b]


def F(s): return f'<span class="f">{s}</span>'
def B(s): return f'<span class="b">{s}</span>'


ALL4 = ["es", "ef", "ls", "lf"]


def node_state(n, v, cls="", use=()):
    return {"v": v, "cls": cls, "use": list(use)}


def start_state():
    return node_state("Start", ALL4)


def forward_steps():
    caps = {
        None: ("Start the forward pass",
               "The Start node has an early start, early finish, late start and late finish of 0 by definition, and a "
               "duration of 0. Each activity's duration goes at the bottom of its node, since we already have those estimates."),
        "A": ("Activity A", "A's only predecessor is Start, so A's early start is Start's early finish, 0. "
                            "Its early finish is its early start plus its duration."),
        "B": ("Activity B", "B's only predecessor is also Start, so B's early start is 0 as well."),
        "C": ("Activity C", "C has one immediate predecessor, A, so C can start as soon as A finishes, at week 2."),
        "D": ("Activity D: two predecessors", "D cannot start until both A and B are finished. A finishes at 2 and B at 3, "
                                              "so the larger of the two early finishes, 3, is D's early start."),
        "E": ("Activity E", "E's only predecessor is C, which finishes at week 4."),
        "F": ("Activity F", "F's only predecessor is also C, so F can start at week 4 too."),
        "G": ("Activity G: two predecessors", "G needs both D and E. D finishes at 7 and E at 8, so G waits for the later one."),
        "H": ("Activity H: the end of the project", "H needs both F and G. F finishes at 7 and G at 13, so H starts at 13 and "
                                                    "finishes at 15. The project's earliest completion time is 15 weeks."),
    }
    steps, done = [], ["Start"]
    for cur in [None] + ORDER[1:]:
        st = {"n": {}, "e": {}}
        if cur: done.append(cur)
        for n in ORDER:
            v = ALL4 if n == "Start" else (["es", "ef"] if n in done else [])
            st["n"][n] = node_state(n, v)
        if cur:
            ps = PRED[cur]
            st["n"][cur]["cls"] = "cur-f"
            for p in ps:
                st["n"][p]["use"] = ["ef"]; st["e"][edge_key(p, cur)] = "f"
            if len(ps) == 1:
                calc = f"{F('ES')} = {F('EF')} of {ps[0]} = {ES[cur]}"
            else:
                calc = (f"{F('ES')} = max(" + ", ".join(f"{F('EF')} of {p}" for p in ps) + ") = max("
                        + ", ".join(str(EF[p]) for p in ps) + f") = {ES[cur]}")
            calc += f"<br>{F('EF')} = {F('ES')} + duration = {ES[cur]} + {DUR[cur]} = {EF[cur]}"
            st["calc"] = calc
        h, body = caps[cur]
        st["cap"] = f"<b class='pm-h'>{h}</b>{body}"
        steps.append(st)
    return steps


def backward_steps():
    seq = ["H", "F", "G", "E", "C", "D", "B", "A"]
    caps = {
        "H": ("Activity H: the last activity", "To finish the project by its early finish, the last activity's late finish "
                                               "must equal its early finish, 15 weeks. Subtract the duration for the late start."),
        "F": ("Activity F", "F comes immediately before just one activity, H, so F's late finish is H's late start."),
        "G": ("Activity G", "G also comes immediately before only H."),
        "E": ("Activity E", "E comes immediately before only G, so E must finish by G's late start."),
        "C": ("Activity C: two followers", "C comes before both E and F, so it must finish in time for the earlier of their "
                                           "late starts. E's is 4 and F's is 10, so C's late finish is 4."),
        "D": ("Activity D", "D comes immediately before only G."),
        "B": ("Activity B", "B comes immediately before only D."),
        "A": ("Activity A: two followers", "A comes before both C and D. C's late start is 2 and D's is 4, so A must "
                                           "finish by week 2. That completes the backward pass."),
    }
    steps, done = [], []
    for cur in seq:
        done.append(cur)
        st = {"n": {n: node_state(n, ALL4 if (n == "Start" or n in done) else ["es", "ef"]) for n in ORDER}, "e": {}}
        st["n"][cur]["cls"] = "cur-b"
        ss = SUCC[cur]
        for s in ss:
            st["n"][s]["use"] = ["ls"]; st["e"][edge_key(cur, s)] = "b"
        if not ss:
            st["n"][cur]["use"] = ["ef"]
            calc = f"{B('LF')} = {F('EF')} = {LF[cur]}"
        elif len(ss) == 1:
            calc = f"{B('LF')} = {B('LS')} of {ss[0]} = {LF[cur]}"
        else:
            calc = (f"{B('LF')} = min(" + ", ".join(f"{B('LS')} of {s}" for s in ss) + ") = min("
                    + ", ".join(str(LS[s]) for s in ss) + f") = {LF[cur]}")
        calc += f"<br>{B('LS')} = {B('LF')} − duration = {LF[cur]} − {DUR[cur]} = {LS[cur]}"
        st["calc"] = calc
        h, body = caps[cur]
        st["cap"] = f"<b class='pm-h'>{h}</b>{body}"
        steps.append(st)
    return steps


def full_state(es, ef, ls, lf, dur, slack=True, crit=True):
    st = {"n": {n: node_state(n, ALL4) for n in ORDER}, "e": {}}
    if dur is not DUR: st["dur"] = {n: d for n, d in dur.items()}
    st["vals"] = {n: [es[n], ef[n], ls[n], lf[n]] for n in ORDER}
    if slack: st["slack"] = {n: ls[n] - es[n] for n in ORDER if n != "Start"}
    if crit:
        for n in ORDER:
            if n != "Start" and ls[n] == es[n]: st["n"][n]["cls"] = "crit"
        for a, b in EDGES:
            if is_crit_edge(a, b, es, ef, ls, lf): st["e"][edge_key(a, b)] = "crit"
    return st


def paths_views():
    views = []
    st = full_state(ES, EF, LS, LF, DUR)
    st["label"] = "Critical path"
    st["cap"] = ("<b class='pm-h'>Slack and the critical path</b>Slack = " + B("LS") + " − " + F("ES") +
                 ". A, C, E, G and H have none, so they form the critical path, drawn in red. "
                 "B and D each have 1 week of slack and F has 6.")
    views.append(st)
    for p in PATHS:
        key = "→".join(p)
        s = {"n": {n: node_state(n, ALL4, "path" if n in p else "dim") for n in ORDER}, "e": {}}
        s["n"]["Start"]["cls"] = "path"
        chain = ["Start"] + p
        for a, b in EDGES:
            s["e"][edge_key(a, b)] = "path" if any(chain[i] == a and chain[i + 1] == b for i in range(len(chain) - 1)) else "dim"
        tot = PATH_LEN[key]
        s["label"] = f"{' → '.join(p)}"
        s["cap"] = (f"<b class='pm-h'>{' → '.join(p)}: {tot} weeks</b>"
                    + " + ".join(f"{DUR[x]} ({x})" for x in p) + f" = {tot} weeks. "
                    + ("This is the longest path, so it is the critical path." if tot == 15
                       else f"That is {15 - tot} week{'s' if 15 - tot != 1 else ''} shorter than the critical path."))
        views.append(s)
    return views


def crash_views():
    a = full_state(ES, EF, LS, LF, DUR)
    a["label"] = "Normal times: 15 weeks"
    a["cap"] = ("<b class='pm-h'>Before crashing</b>One critical path, A → C → E → G → H, at 15 weeks. Of its activities, "
                "A has the lowest crash cost per week ($750), so A is the one to crash.")
    b = full_state(XES, XEF, XLS, XLF, DUR_X)
    b["label"] = "A crashed by 1 week: 14 weeks"
    b["crashed"] = ["A"]
    b["cap"] = ("<b class='pm-h'>After crashing A by 1 week</b>A now takes 1 week, so everything that follows it can start a week "
                "sooner and the project takes 14 weeks. B and D have lost their slack, so B → D → G → H is now critical too: "
                "there are two critical paths.")
    return [a, b]


def build_steps():
    show = [["Start", "A", "B"], ["Start", "A", "B", "C", "D"], ORDER]
    caps = [
        "We begin with a dummy Start node, just so the network has a starting point, and draw arrows from it to the "
        "activities with no predecessors: A and B.",
        "Next, we draw an arrow from A to each activity that A precedes (C and D), and from B to each activity that "
        "B precedes (D).",
        "We continue the same way until every activity is connected. This is the completed network.",
    ]
    steps, prev = [], set()
    for i, vis in enumerate(show):
        st = {"n": {}, "e": {}, "cap": caps[i]}
        for n in ORDER:
            st["n"][n] = node_state(n, [], "" if n in vis else "hide")
            if n in vis and n not in prev and i: st["n"][n]["cls"] = "new"
        for a, b in EDGES:
            k = edge_key(a, b)
            if a in vis and b in vis:
                st["e"][k] = "new" if (i and not (a in prev and b in prev)) else ""
            else:
                st["e"][k] = "hide"
        prev = set(vis); steps.append(st)
    return steps


NET = {"nodes": {n: {"pos": POS[n], "d": DUR[n]} for n in ORDER}, "edges": [list(e) for e in EDGES],
       "vals": {n: [ES[n], EF[n], LS[n], LF[n]] for n in ORDER}}

# ---------------------------------------------------------------- AON vs AOA
CASES = [
    ("B cannot begin before A is complete, and C cannot begin before B is complete.",
     {"A": [40, 70], "B": [130, 70], "C": [220, 70]}, [["A", "B"], ["B", "C"]],
     {"n0": [30, 70], "n1": [110, 70], "n2": [190, 70], "n3": [270, 70]},
     [["n0", "n1", "A", -1], ["n1", "n2", "B", -1], ["n2", "n3", "C", -1]]),
    ("C cannot begin before both A and B are complete.",
     {"A": [60, 35], "B": [60, 115], "C": [160, 75]}, [["A", "C"], ["B", "C"]],
     {"n0": [40, 30], "n1": [40, 120], "n2": [150, 75], "n3": [260, 75]},
     [["n0", "n2", "A", -1], ["n1", "n2", "B", 1], ["n2", "n3", "C", -1]]),
    ("Neither B nor C can begin before A is complete.",
     {"A": [60, 75], "B": [160, 35], "C": [160, 115]}, [["A", "B"], ["A", "C"]],
     {"n0": [40, 75], "n1": [150, 75], "n2": [260, 30], "n3": [260, 120]},
     [["n0", "n1", "A", -1], ["n1", "n2", "B", -1], ["n1", "n3", "C", 1]]),
    ("Neither C nor D can begin until both A and B are complete.",
     {"A": [60, 35], "B": [60, 115], "C": [180, 35], "D": [180, 115]}, [["A", "C"], ["A", "D"], ["B", "C"], ["B", "D"]],
     {"n0": [40, 30], "n1": [40, 120], "n2": [150, 75], "n3": [260, 30], "n4": [260, 120]},
     [["n0", "n2", "A", -1], ["n1", "n2", "B", 1], ["n2", "n3", "C", -1], ["n2", "n4", "D", 1]]),
    ("C cannot begin until A and B are complete, and D cannot begin until B is complete.",
     {"A": [60, 35], "B": [60, 115], "C": [180, 35], "D": [180, 115]}, [["A", "C"], ["B", "C"], ["B", "D"]],
     {"n0": [40, 35], "n1": [150, 35], "n2": [260, 35], "n3": [40, 115], "n4": [150, 115], "n5": [260, 115]},
     [["n0", "n1", "A", -1], ["n1", "n2", "C", -1], ["n3", "n4", "B", 1], ["n4", "n5", "D", 1], ["n4", "n1", "Dummy", 1, 1]]),
    ("B cannot begin before A is complete, C cannot begin before A is complete, and D cannot begin before B and C are complete.",
     {"A": [40, 50], "B": [140, 50], "D": [240, 50], "C": [140, 125]}, [["A", "B"], ["B", "D"], ["A", "C"], ["C", "D"]],
     {"n0": [25, 45], "n1": [105, 45], "n2": [195, 45], "n3": [275, 45], "n4": [150, 125]},
     [["n0", "n1", "A", -1], ["n1", "n2", "B", -1], ["n2", "n3", "D", -1], ["n1", "n4", "Dummy", 1, 1], ["n4", "n2", "C", 1]]),
]
CONV = {"cases": [{"rule": r, "aon": {"nodes": an, "edges": ae}, "aoa": {"nodes": on, "edges": oe}}
                  for r, an, ae, on, oe in CASES]}
# the seven-row (A-H) example, both ways
AOA_FULL = {"nodes": {"n0": [0, 1], "n1": [1, 0], "n2": [1, 2], "n3": [2, 0], "n4": [2, 2], "n5": [3, 1], "n6": [4, 1]},
            "edges": [["n0", "n1", "A", -1], ["n0", "n2", "B", 1], ["n1", "n2", "Dummy", -1, 1], ["n1", "n3", "C", -1],
                      ["n2", "n4", "D", 1], ["n3", "n4", "E", -1], ["n3", "n5", "F", -1], ["n4", "n5", "G", 1],
                      ["n5", "n6", "H", -1]]}
# AOA check: an activity's arrow starts where all its predecessors' arrows (or dummies) end
def _before(node):
    s = set()
    for f, t, lab, *rest in AOA_FULL["edges"]:
        if t == node:
            s |= _before(f)
            if lab != "Dummy": s.add(lab)
    return s
for f, t, lab, *rest in AOA_FULL["edges"]:
    if lab == "Dummy": continue
    direct = {p for p in PRED[lab] if p != "Start"}
    assert direct <= _before(f), (lab, direct, _before(f))

# ---------------------------------------------------------------- Gantt charts
GANTT = [("Design", 0.33, 5.67), ("Prototype", 2.0, 4.0), ("Test", 3.33, 5.67), ("Revise", 3.5, 5.88),
         ("Production", 5.33, 8.67)]
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
GCOL = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"]


def gantt_static():
    cols = "".join(f"<span>{m}</span>" for m in MONTHS)
    rows = ""
    for (name, a, b), c in zip(GANTT, GCOL):
        rows += (f'<div class="pg-row"><span class="pg-lab">{name}</span><div class="pg-track">'
                 f'<span class="pg-bar" style="left:{a / 12 * 100:.2f}%;width:{(b - a) / 12 * 100:.2f}%;background:{c}"></span></div></div>')
    return (f'<div class="pmw pm-gantt" role="img" aria-label="Gantt chart of a product development project: design from January '
            f'to June, a prototype in March and April, testing and revision from April to June, and production from June to September.">'
            f'<p class="pm-title">Gantt Chart: New Product Project</p><div class="pg-scroll"><div class="pg-grid">'
            f'<div class="pg-row pg-head"><span class="pg-lab"></span><div class="pg-track pg-months">{cols}</div></div>{rows}</div></div>'
            f'<noscript></noscript></div>')


def es_ls_gantt():
    rows = []
    for n in ORDER[1:]:
        rows.append({"id": n, "d": DUR[n], "es": ES[n], "ef": EF[n], "ls": LS[n], "lf": LF[n], "crit": n in CRIT})
    return {"rows": rows, "end": 15, "views": [
        {"label": "Early start schedule", "key": "es",
         "cap": "<b class='pm-h'>Every activity at its early start</b>Each bar runs from " + F("ES") + " to " + F("EF") +
                ". The dashed box after a bar is its slack: how far it could slip before it holds up the project."},
        {"label": "Late start schedule", "key": "ls",
         "cap": "<b class='pm-h'>Every activity at its late start</b>Each bar runs from " + B("LS") + " to " + B("LF") +
                ", the latest it can run without delaying the 15-week finish. The slack now sits before the bar. "
                "Critical activities (red) do not move between the two schedules."}]}

# ---------------------------------------------------------------- PERT
PERT = {"A": (1, 2, 3), "B": (2, 3, 4), "C": (1, 2, 3), "D": (2, 4, 6), "E": (1, 4, 7), "F": (1, 2, 9), "G": (3, 4, 11),
        "H": (1, 2, 3)}
T_PRINT = {"A": 2, "B": 3, "C": 2, "D": 4, "E": 4, "F": 3, "G": 5, "H": 2}
V_PRINT = {"A": "0.11", "B": "0.11", "C": "0.11", "D": "0.44", "E": "1.00", "F": "1.78", "G": "1.78", "H": "0.11"}
V_STEP = {"A": "(1 ÷ 3)", "B": "(1 ÷ 3)", "C": "(1 ÷ 3)", "D": "(2 ÷ 3)", "E": "(1)", "F": "(4 ÷ 3)", "G": "(4 ÷ 3)",
          "H": "(1 ÷ 3)"}


def q2(x): return str(Decimal(str(x)).quantize(Decimal("0.01"), ROUND_HALF_UP))


def pert_data():
    acts = []
    for n, (a, m, b) in PERT.items():
        s = a + 4 * m + b
        assert s % 6 == 0 and s // 6 == T_PRINT[n] == DUR[n], n
        v = ((b - a) / 6) ** 2
        assert q2(v) == V_PRINT[n], n
        al, be = 1 + 4 * (m - a) / (b - a), 1 + 4 * (b - m) / (b - a)
        xs = [a + (b - a) * i / 80 for i in range(81)]
        ys = [(x - a) ** (al - 1) * (b - x) ** (be - 1) for x in xs]
        top = max(ys)
        acts.append({"id": n, "a": a, "m": m, "b": b, "t": T_PRINT[n], "v": V_PRINT[n], "crit": n in CRIT,
                     "pts": [[round(x, 3), round(y / top, 4)] for x, y in zip(xs, ys)],
                     "tcalc": f"t = [{a} + 4({m}) + {b}] ÷ 6 = {s} ÷ 6 = <b>{T_PRINT[n]}</b>",
                     "vcalc": f"v = [({b} − {a}) ÷ 6]² = {V_STEP[n]}² = <b>{V_PRINT[n]}</b>"})
    mu = sum(T_PRINT[n] for n in CRIT); var = sum(float(V_PRINT[n]) for n in CRIT)
    assert mu == 15 and q2(var) == "3.11" and q2(math.sqrt(var)) == "1.76"
    return {"acts": acts, "xmax": 12}


def phi(z): return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def deadline_data():
    states = []
    for i in range(18):
        x = 11 + 0.5 * i
        z = Decimal(str((x - 15) / 1.76)).quantize(Decimal("0.01"), ROUND_HALF_UP)
        states.append({"x": x, "z": float(z), "p": f"{phi(float(z)):.5f}"})
    s16 = next(s for s in states if s["x"] == 16)
    assert s16["z"] == 0.57 and s16["p"] == "0.71566"
    return {"states": states, "start": states.index(s16)}


def ninety_nine():
    assert f"{phi(2.33):.4f}" == "0.9901" and abs(phi(2.32) - .99) > abs(phi(2.33) - .99)
    x = Decimal("2.33") * Decimal("1.76")
    assert str(x.quantize(Decimal("0.01"), ROUND_HALF_UP)) == "4.10"
    return {"steps": [
        {"z": 2.33, "lab": "? weeks", "cap": "<b class='pm-h'>The area we want</b>We want the deadline that leaves 0.99 of the "
                                            "curve to its left: a 99% chance of finishing by then."},
        {"z": 2.33, "lab": "μ + 2.33σ", "cap": "<b class='pm-h'>Find z</b>The closest probability to 0.99 in the normal table is "
                                               "0.9901, at z = 2.33. So the deadline sits 2.33 standard deviations above the mean."},
        {"z": 2.33, "lab": "19.10 weeks", "cap": "<b class='pm-h'>Convert z to weeks</b>x = zσ + μ = (2.33)(1.76) + 15 = 4.10 + 15 = "
                                                 "<b>19.10 weeks</b>."}]}


def bands():
    return {"views": [{"k": k, "label": f"±{k}σ", "pct": p,
                       "cap": f"About <b>{p}</b> of outcomes fall within {k} standard deviation{'s' if k > 1 else ''} of the mean."}
                      for k, p in ((1, "68%"), (2, "95%"), (3, "99.7%"))]}


# ---------------------------------------------------------------- static SVG figures
def node_legend():
    """the node-labelling convention, as code, in the widgets' colours"""
    R = 84; cx, cy = 230, 142; xl = R * 0.36
    def yc(x): return math.sqrt(R * R - x * x)
    vx, vy = 0.64 * R, 0.38 * R          # centre of each corner cell: the label sits inside its own shading
    def edge(sx, sy):                    # where a leader meets the circle, on the line out through the cell's centre
        d = math.hypot(vx, vy); return cx + sx * vx / d * R, cy + sy * vy / d * R
    s = [f'<svg viewBox="0 0 460 286" class="pm-legend-svg" role="img" aria-label="An activity node: earliest start top left, '
         f'earliest finish top right, latest start bottom left, latest finish bottom right, the activity label at the top '
         f'centre and its duration at the bottom centre.">',
         f'<defs><clipPath id="pm-lg-clip"><circle cx="{cx}" cy="{cy}" r="{R}"/></clipPath></defs>',
         f'<g clip-path="url(#pm-lg-clip)"><rect x="{cx - R}" y="{cy - R}" width="{R - xl}" height="{R}" class="cf"/>'
         f'<rect x="{cx + xl}" y="{cy - R}" width="{R - xl}" height="{R}" class="cf"/>'
         f'<rect x="{cx - R}" y="{cy}" width="{R - xl}" height="{R}" class="cb"/>'
         f'<rect x="{cx + xl}" y="{cy}" width="{R - xl}" height="{R}" class="cb"/></g>',
         f'<circle cx="{cx}" cy="{cy}" r="{R}" class="ring"/>',
         f'<line x1="{cx - xl:.1f}" y1="{cy - yc(xl):.1f}" x2="{cx - xl:.1f}" y2="{cy + yc(xl):.1f}" class="div"/>',
         f'<line x1="{cx + xl:.1f}" y1="{cy - yc(xl):.1f}" x2="{cx + xl:.1f}" y2="{cy + yc(xl):.1f}" class="div"/>',
         f'<line x1="{cx - R}" y1="{cy}" x2="{cx - xl:.1f}" y2="{cy}" class="div"/><line x1="{cx + xl:.1f}" y1="{cy}" x2="{cx + R}" y2="{cy}" class="div"/>',
         f'<text x="{cx - vx:.1f}" y="{cy - vy:.1f}" class="vf">ES</text><text x="{cx + vx:.1f}" y="{cy - vy:.1f}" class="vf">EF</text>',
         f'<text x="{cx - vx:.1f}" y="{cy + vy:.1f}" class="vb">LS</text><text x="{cx + vx:.1f}" y="{cy + vy:.1f}" class="vb">LF</text>',
         f'<text x="{cx}" y="{cy - vy:.1f}" class="lab">A</text><text x="{cx}" y="{cy + 0.5 * R:.1f}" class="dur">2</text>']
    calls = [  # text, x, y, anchor, leader from, leader to (a point on the node's edge), colour
        ("Earliest Start", 14, 40, "start", (112, 50), edge(-1, -1), "f"),
        ("Earliest Finish", 446, 40, "end", (348, 50), edge(1, -1), "f"),
        ("Latest Start", 14, 252, "start", (100, 240), edge(-1, 1), "b"),
        ("Latest Finish", 446, 252, "end", (360, 240), edge(1, 1), "b"),
        ("Activity label", cx, 22, "middle", (cx, 33), (cx, cy - vy - 0.36 * 30 - 9), "k"),   # ends just above the A
        ("Duration", cx, 276, "middle", (cx, 264), (cx, cy + 0.5 * R + 0.36 * 19 + 8), "k")]   # ends just below the 2
    for t, x, y, anc, (x1, y1), (x2, y2), c in calls:
        s.append(f'<line x1="{x1}" y1="{y1}" x2="{x2:.1f}" y2="{y2:.1f}" class="lead {c}"/>')
        s.append(f'<circle cx="{x2:.1f}" cy="{y2:.1f}" r="3" class="dot {c}"/>')
        s.append(f'<text x="{x}" y="{y}" class="call {c}" text-anchor="{anc}">{t}</text>')
    s.append("</svg>")
    return ('<div class="pmw pm-legend"><p class="pm-title">How Each Node Is Labeled</p>' + "".join(s) +
            '<p class="pm-key"><span class="kf">The forward pass</span> fills the top corners; '
            '<span class="kb">backward pass</span> fills the bottom corners.</p></div>')


def beta_figure():
    """a right-skewed activity-time curve: a and b are its 1st and 99th percentiles, m its peak (lognormal shape)"""
    sig, mu = 0.42, 0.0
    a, b = math.exp(mu - 2.326 * sig), math.exp(mu + 2.326 * sig)
    m = math.exp(mu - sig * sig)
    lo, hi = a * 0.2, b + 0.10 * (b - a)
    W, H, L, Rm, T, Bm = 640, 250, 20, 20, 16, 196
    pdf = lambda x: math.exp(-(math.log(x) - mu) ** 2 / (2 * sig * sig)) / (x * sig * math.sqrt(2 * math.pi))
    top = pdf(m)
    X = lambda x: L + (x - lo) / (hi - lo) * (W - L - Rm)
    Y = lambda y: Bm - y / top * (Bm - T)
    xs = [lo + (hi - lo) * i / 400 for i in range(401)]
    curve = [(X(x), Y(pdf(x))) for x in xs]
    path = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in curve)
    def area(x0, x1):
        pts = [x0 + (x1 - x0) * i / 40 for i in range(41)]
        return (f"M{X(x0):.1f},{Bm + 3.6} L{X(x0):.1f},{Y(pdf(x0)):.1f} " + " ".join(f"L{X(x):.1f},{Y(pdf(x)):.1f}" for x in pts) + f" L{X(x1):.1f},{Bm + 3.6} Z")
    def centroid(x0, x1):   # a point inside a tail for the leader to land on
        xm = x0 + (x1 - x0) * (0.75 if x0 < m else 0.15)
        return X(xm), Bm - (Bm - Y(pdf(xm))) * 0.35
    FS, LH = 12.5, 15
    def box(x, y, lines, anchor):   # the label's box: x is the anchor, y the first baseline
        w = max(len(l) for l in lines) * FS * 0.56
        x0 = x if anchor == "start" else x - w
        return x0, y - FS * 0.8, x0 + w, y + LH * (len(lines) - 1) + FS * 0.25
    def clear_of_curve(bx, gap=6):
        x0, y0, x1, y1 = bx
        return x0 >= 2 and x1 <= W - 2 and y0 >= 2 and all(not (x0 - gap <= cx <= x1 + gap and cy <= y1 + gap) for cx, cy in curve)
    def place(lines, anchor, xs_try):
        for y in range(T + 12, Bm - 40, 4):
            for x in xs_try:
                if clear_of_curve(box(x, y, lines, anchor)): return x, y
        raise AssertionError(lines)
    left = ["1% chance of", "finishing", "before a"]; right = ["1% chance of", "finishing after b"]
    lx, ly = place(left, "start", [10, 14, 18])          # above the curve, at the left
    rx, ry = place(right, "end", [W - 10, W - 14, W - 18])
    lb, rb = box(lx, ly, left, "start"), box(rx, ry, right, "end")
    lt, rt = centroid(lo, a), centroid(b, hi)
    def note(x, y, lines, anchor):
        out = f'<text x="{x:.1f}" y="{y}" class="note" text-anchor="{anchor}">'
        for i, l in enumerate(lines):
            l = l.replace(" a", ' <tspan font-style="italic">a</tspan>').replace(" b", ' <tspan font-style="italic">b</tspan>')
            out += f'<tspan x="{x:.1f}" dy="{0 if i == 0 else LH}">{l}</tspan>'
        return out + "</text>"
    s = (f'<svg viewBox="0 0 {W} {H}" class="pm-beta-svg" role="img" aria-label="A right-skewed beta distribution of an '
         f'activity time: the optimistic time a near the left tail, the most likely time m at the peak, and the pessimistic '
         f'time b far out in the long right tail, with a 1% chance of finishing before a and a 1% chance of finishing after b.">'
         f'<path d="{path}" class="curve"/>'
         f'<line x1="{L - 8}" y1="{Bm + 2.5}" x2="{W - Rm + 8}" y2="{Bm + 2.5}" class="axis"/>'
         f'<path d="{area(lo, a)}" class="tail"/><path d="{area(b, hi)}" class="tail"/>'
         f'<line x1="{X(m):.1f}" y1="{T}" x2="{X(m):.1f}" y2="{Bm + 2.5}" class="mline"/>'
         f'<line x1="{X(a):.1f}" y1="{Y(pdf(a)) - 2:.1f}" x2="{X(a):.1f}" y2="{Bm + 6}" class="tick"/>'
         f'<line x1="{X(b):.1f}" y1="{Y(pdf(b)) - 2:.1f}" x2="{X(b):.1f}" y2="{Bm + 6}" class="tick"/>'
         f'<text x="{max(X(a), 62):.1f}" y="{Bm + 22}" class="xl">Optimistic (<tspan font-style="italic">a</tspan>)</text>'
         f'<text x="{max(X(m), X(a) + 120):.1f}" y="{Bm + 22}" class="xl">Most likely (<tspan font-style="italic">m</tspan>)</text>'
         f'<text x="{min(X(b), W - 62):.1f}" y="{Bm + 22}" class="xl">Pessimistic (<tspan font-style="italic">b</tspan>)</text>'
         + note(lx, ly, left, "start") + note(rx, ry, right, "end") +
         f'<line x1="{(lb[0] + lb[2]) / 2:.1f}" y1="{lb[3] + 3:.1f}" x2="{lt[0]:.1f}" y2="{lt[1]:.1f}" class="lead"/>'
         f'<line x1="{(rb[0] + rb[2]) / 2:.1f}" y1="{rb[3] + 3:.1f}" x2="{rt[0]:.1f}" y2="{rt[1]:.1f}" class="lead"/>'
         f'</svg>')
    return ('<div class="pmw pm-beta"><p class="pm-title">The Beta Distribution of an Activity Time</p>' + s + '</div>')


# ---------------------------------------------------------------- page assets
CSS = open(os.path.join(os.path.dirname(__file__), "project_mgmt.css"), encoding="utf-8").read()
RUNTIME = open(os.path.join(os.path.dirname(__file__), "project_mgmt.js"), encoding="utf-8").read()


def noscript(nums):
    return "".join(f'<noscript><img src="{IMG}{n}" alt="" class="image-wide-60 content-image"></noscript>' for n in nums)


def widget(kind, cfg, title, fallback=(), extra_cls=""):
    js = json.dumps(cfg, ensure_ascii=False).replace("</", "<\\/")
    return (f'<div class="pmw {extra_cls}" data-pm="{kind}">\n<p class="pm-title">{title}</p>\n'
            f'<div class="pm-body"></div>\n{noscript(fallback)}\n<script type="application/json">{js}</script>\n</div>')


def img_tag(t, num):
    a = t.index(f'<img src="{IMG}{num}')
    return t[a:t.index("/>", a) + 2]


def swap(t, old, new, count=1):
    assert t.count(old) == count, (old[:80], t.count(old))
    return t.replace(old, new)


def between(t, start, end, new, keep_end=True):
    a = t.index(start); b = t.index(end, a)
    if not keep_end: b += len(end)
    return t[:a] + new + t[b:]


def chapter(src):
    t = open(src, encoding="utf-8").read()
    # head: the live house script (it builds the table of contents)
    t = swap(t, "content/sn25-v5.js", "studyguide/sn25-v2.js")
    t = t.replace("</head>", CSS + "\n<style>@media (max-width:600px){table{display:block;overflow-x:auto !important;"
                  "-webkit-overflow-scrolling:touch} mjx-container{display:inline-block !important;max-width:100%;"
                  "overflow-x:auto;overflow-y:hidden;vertical-align:middle}}</style>\n</head>", 1)

    # content corrections (Ian, 2026-11-11)
    t = swap(t, "the precedence relationships between the following seven tasks:",
             "the precedence relationships between the following eight tasks:")
    t = swap(t, "The area under the curve to the right of the mean is the probability that the activity will get done later than "
                "the most likely time. The area under the curve to the left of the mean is the probability",
             "The area under the curve to the right of the most likely time is the probability that the activity will get done "
             "later than the most likely time. The area under the curve to the left of the most likely time is the probability")
    t = swap(t, "<strong>=norm.dist(z, true)</strong>", "<strong>=NORM.S.DIST(z, TRUE)</strong>")
    t = swap(t, "<strong>=norm.dist(0.57, true)</strong>", "<strong>=NORM.S.DIST(0.57, TRUE)</strong>")
    t = swap(t, "Therefore, we have two choices: (1) we can crash Activity G, which is common to both critical paths, or (2)",
             "Therefore, we have two choices: (1) we can crash an activity that is common to both critical paths (G or H), or (2)")
    t = swap(t, "<td>Activity G</td>\n<td>$1,500</td>\n</tr>\n",
             "<td>Activity G</td>\n<td>$1,500</td>\n</tr>\n<tr>\n<td>Activity H</td>\n<td>$3,000</td>\n</tr>\n")
    assert PER_WEEK["H"] == 3000 and PER_WEEK["G"] == 1500
    # after crashing G as well: still two critical paths, both 13 weeks
    g2 = dict(DUR_X, G=4); e2, f2, l2, _ = cpm(g2)
    lens = {"→".join(p): sum(g2[x] for x in p) for p in PATHS}
    assert max(f2.values()) == 13 and sorted(k for k, v in lens.items() if v == 13) == ["A→C→E→G→H", "B→D→G→H"], lens
    t = swap(t, "The result in this case would be three critical paths.",
             "The result in this case would still be two critical paths, A → C → E → G → H and B → D → G → H, each taking 13 weeks.")

    # Gantt chart
    t = swap(t, "which may look something like the one on the next page.", "which may look something like the one below.")
    t = swap(t, img_tag(t, "01-gantt"), gantt_static().replace("<noscript></noscript>", ""))

    # AON vs AOA, six cases (two figures) in one widget
    t = swap(t, img_tag(t, "02-aon"), widget("conv", CONV, "Activity-on-Node vs. Activity-on-Arrow", ["02-aon-aoa-conventions-basic.png"]))
    t = swap(t, "Dummy activities are represented by dashed lines. Consider the following examples:</p>",
             "Dummy activities are represented by dashed lines. Cases 5 and 6 above each need one.</p>")
    t = swap(t, img_tag(t, "03-aon") + "\n", "")
    # the eight-activity example, both conventions
    full = {"net": NET, "aoa": AOA_FULL, "views": [{"label": "Activity-on-Node", "kind": "aon"},
                                                   {"label": "Activity-on-Arrow", "kind": "aoa"}]}
    t = swap(t, img_tag(t, "04-aon"), widget("both", full, "The Same Project, Both Ways", ["04-aon-aoa-complete-network.png"]))

    # Step 3: building the network
    a = t.index('<p>We begin with a "dummy" start node')
    b = t.index("<h2>Step 4:")
    old = t[a:b]
    assert all(f"chapter3-0{i}-" in old for i in (5, 6, 7))
    t = t[:a] + widget("net", {"net": NET, "style": "plain", "steps": build_steps()}, "Drawing the Network",
                       ["07-network-complete-structure.png"]) + "\n\n" + t[b:]

    # node convention
    t = swap(t, img_tag(t, "08-node"), node_legend())

    # forward pass
    a = t.index("<p>So, let's apply these rules to our network. We start with the")
    b = t.index("<h2>Backward Pass</h2>")
    old = t[a:b]
    assert all(f"chapter3-{i:02d}-" in old for i in range(9, 15))
    t = t[:a] + ("<p>Let's apply these rules to our network, one node at a time, from left to right.</p>\n\n"
                 + widget("net", {"net": NET, "style": "full", "steps": forward_steps(), "phase": "f"}, "The Forward Pass",
                          ["14-forward-pass-complete.png"]) + "\n\n") + t[b:]

    # backward pass
    a = t.index("<p>Let's apply these rules to our network. We start with the final node")
    b = t.index("<p>Note that some projects have more than one final node")
    old = t[a:b]
    assert all(f"chapter3-{i:02d}-" in old for i in range(15, 21))
    t = t[:a] + ("<p>Let's apply these rules to our network, one node at a time, from right to left.</p>\n\n"
                 + widget("net", {"net": NET, "style": "full", "steps": backward_steps(), "phase": "b"}, "The Backward Pass",
                          ["20-backward-pass-complete.png"]) + "\n\n") + t[b:]

    # critical path and the four paths
    t = swap(t, img_tag(t, "21-critical"), widget("net", {"net": NET, "style": "full", "views": paths_views()},
                                                  "The Critical Path and Every Path Through the Network",
                                                  ["21-critical-path-diagram.png"]))

    # Step 6: early-start and late-start Gantt charts
    anchor = "for the project to get done on time.</p>"
    t = swap(t, anchor, anchor + "\n\n" + widget("gantt", es_ls_gantt(), "Milwaukee Paper's Schedule as Gantt Charts"))

    # PERT
    t = swap(t, img_tag(t, "22-beta"), beta_figure())
    t = swap(t, img_tag(t, "23-normal"), widget("bands", bands(), "The Normal Distribution", ["23-normal-distribution.png"]))
    a = t.index("<p>We could use this information to calculate the expected time (t) for each activity:</p>")
    b = t.index("<p>We can show our calculations on the table:</p>")
    old = t[a:b]
    assert old.count("<strong>") == 16 and "1.78" in old
    t = t[:a] + ("<p>We could use this information to calculate the expected time (t) and the variance (v) of each activity:</p>\n\n"
                 + widget("pert", pert_data(), "Expected Time and Variance, Activity by Activity") + "\n\n") + t[b:]
    t = swap(t, img_tag(t, "24-prob"), widget("deadline", deadline_data(), "Probability of Finishing by the Deadline",
                                             ["24-probability-16-weeks.png"]))
    t = swap(t, img_tag(t, "25-prob"), widget("ninety", ninety_nine(), "The Deadline for a 99% Chance",
                                             ["25-probability-99-percent.png"]))

    # crashing
    t = swap(t, img_tag(t, "26-crashed"), widget("net", {"net": NET, "style": "full", "views": crash_views()},
                                                 "Crashing Activity A by One Week", ["26-crashed-network.png"]))

    t = t.replace("</body>", RUNTIME + "\n</body>", 1)
    left = [l for l in t.split("\n") if "<img" in l and "<noscript>" not in l]
    assert not left, left
    return t


def patch(path, out):
    """bring a file this script already converted up to the current figures, leaving every other edit in it alone"""
    import re
    t = open(path, encoding="utf-8").read()
    subs = [
        (r"<style>\n\.pmw \{.*?</style>", CSS),
        (r"<script>\n\(function \(\) \{\n  var NS = 'http://www\.w3\.org/2000/svg', uid = 0;.*?</script>", RUNTIME),
        (r'<div class="pmw pm-legend">.*?</p></div>', node_legend()),
        (r'<div class="pmw pm-beta">.*?</svg></div>', beta_figure()),
    ]
    for pat, new in subs:
        t, n = re.subn(pat, lambda m: new, t, count=1, flags=re.S)
        assert n == 1, pat[:40]
    open(out, "w", encoding="utf-8").write(t); print("patched", path, "->", out)


if __name__ == "__main__":
    if sys.argv[1] == "--patch":
        patch(sys.argv[2], sys.argv[3]); sys.exit()
    src, outdir = sys.argv[1:3]; os.makedirs(outdir, exist_ok=True)
    p = os.path.join(outdir, "MAN4504-263-Exam3-Chapter3-RestofProjectManagement-Full.html")
    open(p, "w", encoding="utf-8").write(chapter(src)); print("wrote", p)
    print("checks passed: ES/EF/LS/LF table, slack, critical path, 4 path lengths, crashed network, crash costs,",
          "PERT t and v, mu 15, var 3.11, sd 1.76, z 0.57 -> 0.71566, z 2.33 -> 19.10")
