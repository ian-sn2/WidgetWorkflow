"""MAR3203 Exam 2: Project Management, Processes, Capacity Management."""
from common import *

# ================================================================ Project Management
def pm_cycle():
    b = ""
    boxes = [(300, 64, "Project Planning", "Establish objectives\nCreate work breakdown"),
             (470, 260, "Project Scheduling", "Activity start and end times\nEstablish network"),
             (130, 260, "Project Controlling", "Monitor resources\nRevise plan and shift\nresources if needed")]
    for x, y, h, body in boxes:
        b += f'<rect x="{x-105}" y="{y-44}" width="210" height="88" rx="14" fill="{PALEG}" stroke="{INK}" stroke-width="1.6"/>'
        b += text(x, y - 20, h, 14) + text(x, y - 1, body, 11.5, bold=False, lh=14)
    # arrows round the ring: planning -> scheduling -> controlling -> planning
    b += path("M408 100 A170 170 0 0 1 492 208", sw=3.4, color=GOLDC)
    b += path("M450 312 A170 170 0 0 1 150 312", sw=3.4, color=GOLDC)
    b += path("M108 208 A170 170 0 0 1 192 100", sw=3.4, color=GOLDC)
    return svg(600, 416, b, "The continuous cycle of project planning, scheduling and controlling", 600)  # the bottom arc reaches y = 402
PMCYCLE = html(pm_cycle(), True)

def net(nodes, edges, **kw):
    """nodes: {id: (x, y)} or {id: (x, y, es, ef, ls, lf)}; edges: list of 'A>B' or (a, b, opts)"""
    ns = []
    for k, v in nodes.items():
        d = {"id": k, "x": v[0], "y": v[1]}
        if len(v) > 2: d.update(es=v[2], ef=v[3])
        if len(v) > 4: d.update(ls=v[4], lf=v[5])
        if len(v) > 6: d["dur"] = v[6]
        ns.append(d)
    es = []
    for e in edges:
        if isinstance(e, str): a, b = e.split(">"); es.append({"from": a, "to": b})
        else: es.append(dict({"from": e[0], "to": e[1]}, **e[2]))
    return dict({"nodes": ns, "edges": es}, **kw)

simple = {"title": "A Simple Network Diagram", "network": net({"B": (84, 14), "A": (84, 86), "C": (50, 50), "D": (12, 50)}, ["B>C", "A>C", "C>D"], h=200),
          "caption": cap("C waits for both A and B to finish, and D waits for C.")}
complex_ = {"title": "A Network With Crossed Dependencies", "network": net({"A": (16, 18), "B": (16, 82), "C": (84, 18), "D": (84, 82)}, ["A>C", "A>D", "B>C", "B>D"], h=200),
            "caption": cap("Neither C nor D can start until both A and B are complete, so every arrow has to be read, not just the straight ones.")}

def aon_aoa(aon_nodes, aon_edges, aoa_nodes, aoa_edges, h=170):
    return {"panels": [dict(net(aon_nodes, aon_edges), heading="Activity-on-Node (AON)", w=300, h=h, r=18),
                       dict(net(aoa_nodes, aoa_edges), heading="Activity-on-Arrow (AOA)", aoa=True, w=300, h=h, r=16)]}
def aoa_e(a, b, lab, **o): return (a, b, dict({"label": lab}, **o))
EX = {
 "e1": ("Example 1", "B cannot begin before A is complete, and C cannot begin before B is complete.",
        aon_aoa({"A": (14, 50), "B": (50, 50), "C": (86, 50)}, ["A>B", "B>C"],
                {"1": (8, 50), "2": (36, 50), "3": (64, 50), "4": (92, 50)}, [aoa_e("1", "2", "A"), aoa_e("2", "3", "B"), aoa_e("3", "4", "C")])),
 "e2": ("Example 2", "C cannot begin before both A and B are complete.",
        aon_aoa({"A": (20, 22), "B": (20, 78), "C": (72, 50)}, ["A>C", "B>C"],
                {"1": (8, 22), "2": (8, 78), "3": (55, 50), "4": (92, 50)}, [aoa_e("1", "3", "A"), aoa_e("2", "3", "B"), aoa_e("3", "4", "C")])),
 "e3": ("Example 3", "Neither B nor C can begin before A is complete.",
        aon_aoa({"A": (22, 50), "B": (76, 20), "C": (76, 80)}, ["A>B", "A>C"],
                {"1": (8, 50), "2": (45, 50), "3": (88, 18), "4": (88, 82)}, [aoa_e("1", "2", "A"), aoa_e("2", "3", "B"), aoa_e("2", "4", "C")])),
 "e4": ("Example 4", "Neither C nor D can begin until both A and B are complete.",
        aon_aoa({"A": (20, 22), "B": (20, 78), "C": (76, 22), "D": (76, 78)}, ["A>C", "A>D", "B>C", "B>D"],
                {"1": (8, 20), "2": (8, 80), "3": (50, 50), "4": (92, 20), "5": (92, 80)}, [aoa_e("1", "3", "A"), aoa_e("2", "3", "B"), aoa_e("3", "4", "C"), aoa_e("3", "5", "D")])),
}
EX2 = {
 "e5": ("Example 5", "C cannot begin until A and B are complete, and D cannot begin until B is complete.",
        aon_aoa({"A": (20, 22), "B": (20, 78), "C": (76, 22), "D": (76, 78)}, ["A>C", "B>C", "B>D"],
                {"1": (8, 20), "2": (50, 20), "3": (92, 20), "4": (8, 80), "5": (50, 80), "6": (92, 80)},
                [aoa_e("1", "2", "A"), aoa_e("2", "3", "C"), aoa_e("4", "5", "B"), aoa_e("5", "6", "D"), aoa_e("5", "2", "Dummy", dashed=True, loff=30)], h=190)),
 "e6": ("Example 6", "B cannot begin before A is complete, C cannot begin before A is complete, and D cannot begin before B and C are complete.",
        aon_aoa({"A": (10, 25), "B": (45, 25), "D": (84, 25), "C": (45, 82)}, ["A>B", "B>D", "A>C", "C>D"],
                {"1": (6, 25), "2": (32, 25), "3": (62, 25), "4": (92, 25), "5": (50, 85)},
                [aoa_e("1", "2", "A"), aoa_e("2", "3", "B"), aoa_e("3", "4", "D"), aoa_e("2", "5", "Dummy", dashed=True, loff=-26, ldx=-6), aoa_e("5", "3", "C", loff=16)], h=200)),
}
def examples(exs, title):
    return {"title": title, "lede": "The same precedence rule drawn both ways; a dashed arrow is a dummy activity.",
            "scenarios": {k: {"label": lab, "network": nw, "caption": cap(txt)} for k, (lab, txt, nw) in exs.items()}}
aon1 = examples(EX, "AON and AOA Conventions, Examples 1–4")
aon2 = examples(EX2, "AON and AOA With Dummy Activities, Examples 5–6")

BIG = {"A": (6, 50, 0, 20, 0, 20, 20), "C": (30, 14, 20, 27, 24, 31, 7), "B": (30, 86, 20, 28, 20, 28, 8), "D": (55, 86, 28, 31, 28, 31, 3), "E": (76, 50, 31, 35, 31, 35, 4), "F": (95, 16, 35, 38, 35, 38, 3)}
BIG_E = [("A", "C", {}), ("A", "B", {"crit": True}), ("B", "D", {"crit": True}), ("C", "E", {}), ("D", "E", {"crit": True}), ("E", "F", {"crit": True})]
big_plain = {"title": "The Project Network", "network": net({k: v[:2] for k, v in BIG.items()}, [(a, b, {}) for a, b, _ in BIG_E], h=240),
             "caption": cap("Two paths run from A to F: through C, or through B and D. At least one of them is the critical path.")}
def nodeconv():
    b = f'<circle cx="300" cy="150" r="95" fill="#fff" stroke="{INK}" stroke-width="2.2"/>'
    b += path("M265 62 V238 M335 62 V238 M205 150 H265 M335 150 H395", sw=1.4, head=False)
    b += text(300, 142, "A", 30, color=NAVY) + text(300, 225, "2", 20, color=NAVY)
    b += text(235, 140, "ES", 20, color=NAVY) + text(365, 140, "EF", 20, color=NAVY) + text(235, 200, "LS", 20, color=NAVY) + text(365, 200, "LF", 20, color=NAVY)
    # every leader stops at the circle's rim, outside the lettering it points at (Ian, 2026-10-26: lines were crossing ES, EF and LS)
    calls = [(233, 83, 150, 40, "Earliest\nStart", "end"), (367, 83, 450, 40, "Earliest\nFinish", "start"), (386, 110, 500, 110, "Activity\nLabel", "start"),
             (233, 217, 150, 268, "Latest\nStart", "end"), (367, 217, 450, 268, "Latest\nFinish", "start"), (300, 245, 300, 285, "Activity\nDuration", "middle")]
    for x1, y1, x2, y2, t, anc in calls:
        b += arrow(x2, y2 - 4 if y2 < y1 else y2 - 16, x1, y1, sw=1.3, head=False)
        b += text(x2, y2 + (4 if anc == "middle" else -14 if y2 < y1 else 2), t, 13, anchor=anc, lh=15)
    return svg(600, 320, b, "The node convention: earliest start and finish in the top half, latest start and finish in the bottom half, the activity label in the centre and its duration beneath", 520)
NODECONV = html(nodeconv())
big_filled = {"title": "The Completed Network", "network": dict(net(BIG, BIG_E, style="ellipse", h=250), show={"ef": 1, "lf": 2, "crit": 3}),
              "steps": [cap("Each activity's duration sits under its name; the four times fill in as the passes run."),
                        cap("The forward pass runs left to right: an activity's ES is the latest EF among the activities it waits for, and EF = ES + duration."),
                        cap("The backward pass runs right to left from F's finish at 38: LF is the earliest LS of what follows, and LS = LF − duration."),
                        cap("Only C has slack (LS − ES = 24 − 20 = 4). The path A → B → D → E → F has none, so it is the critical path, 38 weeks long.")]}

SM = {"A": (4, 50), "B": (22, 50), "C": (50, 22), "D": (50, 78), "E": (76, 50), "F": (97, 50)}   # wide and shallow: corner times clear of the arrows (Ian, 2026-10-26)
SM_E = ["A>B", "B>C", "B>D", "C>E", "D>E", "E>F"]
FWD = {"A": (0, 3), "B": (3, 4), "C": (4, 6), "D": (4, 7), "E": (7, 11), "F": (11, 16)}
BWD = {"A": (0, 3), "B": (3, 4), "C": (5, 7), "D": (4, 7), "E": (7, 11), "F": (11, 16)}
def sm_nodes(fwd=None, bwd=None):
    out = {}
    for k, (x, y) in SM.items():
        v = [x, y]
        if fwd: v += list(fwd[k])
        if bwd: v += list(bwd[k])
        out[k] = tuple(v)
    return out
CRIT = {"A>B", "B>D", "D>E", "E>F"}
def sm_edges(crit=False): return [(e.split(">")[0], e.split(">")[1], {"crit": True} if crit and e in CRIT else {}) for e in SM_E]
ex_plain = {"title": "The Example Network", "network": net(sm_nodes(), sm_edges(), h=220),
            "caption": cap("A leads to B, B splits into C and D, both of which feed E, and E leads to F.")}
ex_fwd = {"title": "The Forward Pass", "network": dict(net(sm_nodes(FWD), sm_edges(), h=240, legend=True), show={"ef": 1}),
          "steps": [cap("Start at A with ES = 0; every EF is ES plus the activity's time."),
                    cap("E waits for both C (EF 6) and D (EF 7), so its ES is the later one, 7. The project finishes when F does, at 16.")]}
ex_bwd = {"title": "The Backward Pass", "network": dict(net(sm_nodes(FWD, BWD), sm_edges(), h=240), show={"lf": 1}),
          "steps": [cap("The forward pass gave every ES and EF; the latest times come from working back from F."),
                    cap("F's LF is its EF, 16, and LS = LF − time. B feeds both C (LS 5) and D (LS 4), so B's LF is the earlier one, 4.")]}
ex_crit = {"title": "The Critical Path", "network": dict(net(sm_nodes(FWD, BWD), sm_edges(crit=True), h=240), show={"crit": 1}),
           "steps": [cap("Slack is LS − ES. Every activity has zero slack except C, whose LS of 5 is a week after its ES of 4."),
                     cap("The zero-slack activities A → B → D → E → F form the critical path, and its 16 weeks is the project's length.")]}
CR_F = {"A": (0, 3), "B": (3, 4), "C": (4, 6), "D": (4, 6), "E": (6, 10), "F": (10, 15)}
ex_crash = {"title": "After Crashing D by One Week", "network": net(sm_nodes(CR_F, CR_F), [(a, b, {"crit": True}) for a, b, _ in sm_edges()], h=240),
            "caption": cap("With D cut to two weeks, C and D both finish at 6, so every activity has zero slack: there are now two critical paths and the project takes 15 weeks.")}
PM = {"mar3203-exam2-pm-01-project-planning-scheduling-controlling-cycle.png": PMCYCLE, "mar3203-exam2-pm-02-network-diagram-abcd-simple.png": simple,
      "mar3203-exam2-pm-03-network-diagram-abcd-complex.png": complex_, "mar3203-exam2-pm-04-aon-aoa-examples-1-2.png": aon1,
      "mar3203-exam2-pm-06-aon-aoa-examples-5-6-dummy.png": aon2, "mar3203-exam2-pm-07-network-diagram-abcdef-cpm.png": big_plain,
      "mar3203-exam2-pm-08-node-convention-diagram.png": NODECONV, "mar3203-exam2-pm-09-network-diagram-abcdef-filled-values.png": big_filled,
      "mar3203-exam2-pm-10-network-diagram-example-abcdef.png": ex_plain, "mar3203-exam2-pm-11-network-diagram-forward-pass.png": ex_fwd,
      "mar3203-exam2-pm-12-network-diagram-backward-pass.png": ex_bwd, "mar3203-exam2-pm-13-network-diagram-critical-path-highlighted.png": ex_crit,
      "mar3203-exam2-pm-14-network-diagram-post-crash-d.png": ex_crash}
PM_ANCH = [{"after": "<p>Node convention (ES | EF over LS | LF):</p>", "widget": big_filled, "comment": "the worked CPM network, after the convention it uses"}]

# ================================================================ Processes
# The diagonal y = 104 - m(x - 2) through the three focus boxes, drawn only in the gaps between them,
# so it never runs through a box's name (Ian, 2026-10-26). Entry and exit points are solved, not typed.
PPM_BOXES = [((4, 30), (82, 104)), ((38, 64), (50, 72)), ((76, 102), (8, 30))]
def _ppm_cross(box):
    (x0, x1), (y0, y1) = box; m = 98 / 102
    f = lambda x: 104 - m * (x - 2); g = lambda y: 2 + (104 - y) / m
    pts = [(x, f(x)) for x in (x0, x1) if y0 <= f(x) <= y1] + [(g(y), y) for y in (y0, y1) if x0 <= g(y) <= x1]
    pts = sorted(set((round(x, 1), round(y, 1)) for x, y in pts)); assert len(pts) == 2, pts
    return pts
_c = [_ppm_cross(b) for b in PPM_BOXES]
PPM_SEGS = [[list(_c[0][1]), list(_c[1][0])], [list(_c[1][1]), list(_c[2][0])]]   # exit of one box to entry of the next
ppm = {"title": "Product-Process Matrix",
       "axes": {"x": "\nVolume", "y": "Variety", "xmax": 110, "ymax": 110, "bg": False},
       "curves": [{"id": "diag%d" % i, "label": "", "pts": seg, "dashed": True, "thin": True, "color": "grey"} for i, seg in enumerate(PPM_SEGS)],
       "areas": [{"pts": [[4, 82], [4, 104], [30, 104], [30, 82]], "color": "gold", "opacity": 0.4, "edge": True, "label": "Process\nFocus"},
                 {"pts": [[38, 50], [38, 72], [64, 72], [64, 50]], "color": "gold", "opacity": 0.4, "edge": True, "label": "Repetitive\nFocus"},
                 {"pts": [[76, 8], [76, 30], [102, 30], [102, 8]], "color": "gold", "opacity": 0.4, "edge": True, "label": "Product\nFocus"},
                 {"pts": [[72, 82], [72, 104], [104, 104], [104, 82]], "color": "gold", "opacity": 0.4, "edge": True, "label": "Mass\nCustomization"}],
       "points": [{"q": 2, "p": 0, "dot": False, "guides": False, "showP": False, "ql": "Low"}, {"q": 106, "p": 0, "dot": False, "guides": False, "showP": False, "ql": "High"},
                  {"q": 0, "p": 4, "dot": False, "guides": False, "showQ": False, "pl": "Low"}, {"q": 0, "p": 104, "dot": False, "guides": False, "showQ": False, "pl": "High"}],
       "caption": cap("Each step down the diagonal gives up some variety for a lot more volume; the corner box is the one strategy that tries to keep both.")}

def lab_flow():
    b = ""
    b += f'<rect x="8" y="12" width="92" height="236" rx="4" fill="none" stroke="{GREY}" stroke-width="1.2" stroke-dasharray="4 3"/>'
    for i, nm in enumerate("ABC"):
        b += circle(54, 50 + i * 74, 26, f"Source\n{nm}", fill="#dff1f3", fs=11, lh=12)
        b += arrow(80, 50 + i * 74 - (i - 1) * 10, 160, 112, sw=2.2)
    b += circle(196, 112, 34, "Process", fill="#f9cfb3", fs=12)
    b += arrow(230, 112, 296, 112, sw=2.2)
    b += diamond(348, 112, 100, 64, "Need\nseparation?", fs=10)
    b += arrow(398, 112, 468, 112, sw=2.2)
    b += circle(506, 112, 32, "Sep.", fill="#f9cfb3", fs=13)
    b += arrow(538, 112, 610, 112, sw=2.2)
    b += circle(648, 112, 32, "Dist.", fill="#f9cfb3", fs=13)
    b += arrow(680, 112, 752, 112, sw=2.2)
    b += circle(790, 112, 32, "Test", fill="#f9cfb3", fs=13)
    b += arrow(822, 112, 892, 112, sw=2.2)
    b += circle(934, 112, 34, "Comm.", fill="#dff1f3", fs=12)
    b += path("M348 80 V30 H648 V78", sw=2.2)
    b += path("M790 144 V232 H732", sw=2.2)   # test -> post-test; the stray stub past the junction is gone (Ian, 2026-10-26)
    b += circle(700, 232, 32, "Post-\ntest", fill="#f9cfb3", fs=12, lh=13)
    b += arrow(668, 232, 614, 232, sw=2.2)
    b += f'<polygon points="542,210 614,210 578,262" fill="#d9cbe6" stroke="{INK}" stroke-width="1.4"/>' + text(578, 226, "Storage", 11)
    b += arrow(540, 232, 470, 232, sw=2.2)
    b += diamond(420, 232, 94, 60, "Retest?", fs=11)
    b += path("M373 232 H196 V150", sw=2.2)
    # legend in a row under the chart (Ian, 2026-10-26: beside it, the whole drawing shrank to fit the column)
    ly = 300
    b += f'<polygon points="60,{ly-11} 88,{ly-11} 74,{ly+11}" fill="#d9cbe6" stroke="{INK}" stroke-width="1"/>' + text(100, ly + 4, "= Inventory/Buffer", 13, anchor="start")
    b += arrow(290, ly, 318, ly, sw=2) + text(330, ly + 4, "= Direction of Flow", 13, anchor="start")
    b += f'<polygon points="534,{ly-14} 548,{ly} 534,{ly+14} 520,{ly}" fill="#fbf1c7" stroke="{INK}" stroke-width="1"/>' + text(560, ly + 4, "= Decision", 13, anchor="start")
    b += f'<circle cx="704" cy="{ly}" r="14" fill="#f9cfb3" stroke="{INK}" stroke-width="1"/>' + text(730, ly + 4, "= Process/Activity", 13, anchor="start")
    return svg(1000, 330, b, "A flowchart of work through a lab: three sources feed a process, a separation decision, separation, distribution and a test; failed tests go to a post-test, storage and a retest decision that loops back to the process", 1000)
LABFLOW = html(lab_flow(), True)

def tfmap(rows, cols, cells, arrows_, title_days):
    """rows: list of row names; cols: list of day labels; cells: (row, col, text, kind) kind in box/circle; arrows_: list of (r1,c1,r2,c2)"""
    CW, RH, X0, Y0 = 92, 72, 150, 20
    W = X0 + CW * len(cols) + 10; H = Y0 + RH * len(rows) + 70
    b = ""
    for r, name in enumerate(rows): b += text(X0 - 12, Y0 + r * RH + RH / 2 + 5, name, 13, anchor="end", lh=15)
    for r in range(len(rows) + 1): b += f'<line x1="{X0}" y1="{Y0 + r*RH}" x2="{X0 + CW*len(cols)}" y2="{Y0 + r*RH}" stroke="#c9c9c9" stroke-width="1"/>'
    for c in range(len(cols) + 1): b += f'<line x1="{X0 + c*CW}" y1="{Y0}" x2="{X0 + c*CW}" y2="{Y0 + RH*len(rows)}" stroke="#c9c9c9" stroke-width="1"/>'
    pos = {}
    for r, c, t, kind in cells:
        cx, cy = X0 + c * CW + CW / 2, Y0 + r * RH + RH / 2; pos[(r, c)] = (cx, cy)
        if kind == "circle": b += circle(cx, cy, 24, t, fill="#fbf1c7", fs=11)
        else: b += box(cx - 30, cy - 24, 60, 48, t, fill=(PALEG if "Order" not in t and "Receive" not in t else "#dff1f3"), fs=11, rx=4, lh=13)
    for r1, c1, r2, c2 in arrows_:
        (x1, y1), (x2, y2) = pos[(r1, c1)], pos[(r2, c2)]
        if c1 == c2: b += arrow(x1, y1 + 26, x2, y2 - 28, sw=3) if r2 > r1 else arrow(x1, y1 - 26, x2, y2 + 28, sw=3)
        elif r1 == r2: b += arrow(x1 + 32, y1, x2 - 34, y2, sw=3)
        elif r2 > r1: b += path(f"M{x1} {y1 + 26} V{y2} H{x2 - 34}", sw=3)
        else: b += path(f"M{x1 + 32} {y1} H{x2} V{y2 + 28}", sw=3)
    for c, d in enumerate(cols): b += text(X0 + c * CW + CW / 2, Y0 + RH * len(rows) + 22, d, 12)
    yb = Y0 + RH * len(rows) + 50
    b += path(f"M{X0 + 8} {yb} H{X0 + CW*len(cols) - 8} M{X0 + 8} {yb} l12 -7 M{X0 + 8} {yb} l12 7 M{X0 + CW*len(cols) - 8} {yb} l-12 -7 M{X0 + CW*len(cols) - 8} {yb} l-12 7", sw=2.2, head=False)
    b += f'<rect x="{(X0 + CW*len(cols)/2) - 40}" y="{yb - 11}" width="80" height="22" fill="#fff"/>' + text(X0 + CW * len(cols) / 2, yb + 5, title_days, 14, italic=True)
    return svg(W, H, b, f"A time-function map taking {title_days} from order to receipt", 700)
ROWS = ["Customer", "Sales", "Production\nControl", "Plant A", "Warehouse", "Plant B", "Transport"]
BASE = tfmap(ROWS, ["12 Days", "13 Days", "1 Day", "4 Days", "1 Day", "10 Days", "1 Day", "0 Day", "1 Day"],
             [(0, 0, "Order\nProduct", "box"), (1, 0, "Process\nOrder", "box"), (2, 1, "Wait", "circle"), (3, 2, "Print", "box"), (4, 3, "Wait", "circle"), (6, 4, "Move", "circle"),
              (4, 5, "Wait", "circle"), (5, 6, "Extrude", "box"), (4, 7, "Wait", "circle"), (6, 8, "Move", "circle"), (0, 8, "Receive\nProduct", "box")],
             [(0, 0, 1, 0), (1, 0, 2, 1), (2, 1, 3, 2), (3, 2, 4, 3), (4, 3, 6, 4), (6, 4, 4, 5), (4, 5, 5, 6), (5, 6, 4, 7), (4, 7, 6, 8), (6, 8, 0, 8)], "43 Days")
TARGET = tfmap(["Customer", "Sales", "Production\nControl", "Plant A", "Warehouse", "Transport"], ["1 Day", "2 Days", "1 Day", "1 Day", "1 Day", "1 Day", "1 Day"],
               [(0, 0, "Order\nProduct", "box"), (1, 0, "Process\nOrder", "box"), (2, 1, "Wait", "circle"), (3, 2, "Print", "box"), (3, 4, "Extrude", "box"), (4, 5, "Wait", "circle"), (5, 6, "Move", "circle"), (0, 6, "Receive\nProduct", "box")],
               [(0, 0, 1, 0), (1, 0, 2, 1), (2, 1, 3, 2), (3, 2, 3, 4), (3, 4, 4, 5), (4, 5, 5, 6), (5, 6, 0, 6)], "8 Days")
TF_BASE, TF_TARGET = html(BASE), html(TARGET)

def process_chart():
    syms = ["○", "⇨", "□", "✚", "▽"]
    rows = [("", "---", 4, "Meat Patty in Storage"), ("1.5", "0.05", 1, "Transfer to Broiler"), ("", "2.50", 0, "Broiler"), ("", "0.05", 2, "Visual Inspection"), ("1.0", "0.05", 1, "Transfer to Rack"),
            ("", "0.15", 4, "Temporary Storage"), ("0.5", "0.10", 1, "Obtain Buns, Lettuce, etc."), ("", "0.20", 0, "Assemble Order"), ("0.5", "0.05", 1, "Place in Finish Rack")]
    h = ('<div class="sk-wrap"><table class="sk-tbl financial" style="font-size:.9em"><tr><th colspan="7" style="font-size:1.15em;letter-spacing:.5px">PROCESS CHART &nbsp;·&nbsp; Present Method</th></tr>'
         '<tr><th>Distance<br>(feet)</th><th>Time<br>(minutes)</th><th colspan="5">Chart Symbols</th><th rowspan="2" style="display:none"></th></tr>'
         '<tr><th></th><th></th>' + "".join(f'<th style="font-size:1.1em">{s}</th>' for s in syms) + '</tr>')
    # header fix: the description column
    h = h.replace('<th colspan="5">Chart Symbols</th><th rowspan="2" style="display:none"></th></tr>', '<th colspan="5">Chart Symbols</th><th rowspan="2">Process Description</th></tr>')
    for dist, t, k, desc in rows:
        t = t.replace("---", "&#8209;&#8209;&#8209;")
        h += f'<tr><td>{dist}</td><td>{t}</td>' + "".join(f'<td{" class=hl" if i == k else ""} style="font-size:1.1em">{s}</td>' for i, s in enumerate(syms)) + f'<td class="lbl" style="background:#fff">{desc}</td></tr>'
    h += '<tr><td><b>3.5</b></td><td><b>3.15</b></td><td><b>2</b></td><td><b>4</b></td><td><b>1</b></td><td><b>&#8209;&#8209;&#8209;</b></td><td><b>2</b></td><td class="lbl" style="background:#fff">TOTALS</td></tr></table></div>'
    h += '<p style="text-align:center;font-size:.9em;margin-top:-8px">○ Operation &nbsp; ⇨ Transportation &nbsp; □ Inspection &nbsp; ✚ Delay &nbsp; ▽ Storage</p>'
    return h
PROCCHART = html(process_chart())

def blueprint():
    b = ""
    cols = ["Personal Greeting", "Service Diagnosis", "Perform Service", "Friendly Close"]
    for i, c in enumerate(cols): b += text(150 + i * 250, 22, c, 14, italic=True)
    b += f'<line x1="40" y1="118" x2="1040" y2="118" stroke="{INK}" stroke-width="1.6"/><line x1="60" y1="508" x2="1040" y2="508" stroke="{INK}" stroke-width="1.6"/>'
    b += text(14, 72, "Level 1", 12, anchor="start") + text(14, 300, "Level 2", 12, anchor="start") + text(14, 620, "Level 3", 12, anchor="start")
    E = lambda cx, cy, t, fill="#f9cfb3": ellipse(cx, cy, 115, 30, t, fill=fill, fs=13, lh=15)
    b += E(170, 78, "Customer Arrives\nfor Service", "#dff1f3") + E(920, 78, "Customer\nDeparts", "#dff1f3")
    b += E(170, 210, "Warm Greeting and\nObtain Service Request") + diamond(355, 268, 96, 74, "Standard\nRequest", fs=11) + E(475, 190, "Determine\nSpecifics")
    b += diamond(475, 320, 150, 106, "Can Service\nBe Done, and\nDoes Customer\nApprove?", fs=10.5, lh=12) + E(670, 212, "Notify Customer\nand Recommend\nAlternative Provider")
    b += E(920, 192, "Customer\nPays Bill") + E(920, 430, "Notify Customer\nthat the Car Is Ready") + E(170, 410, "Direct Customer\nto Waiting Room")
    b += E(685, 552, "Perform\nRequired Work") + E(685, 685, "Prepare\nInvoice")
    # flow lines
    b += arrow(170, 108, 170, 180, sw=1.4) + path("M170 240 V268 H306", sw=1.4) + path("M355 233 V190 H356", sw=1.4) + arrow(475, 220, 475, 272, sw=1.4)
    b += path("M540 320 H670 V244", sw=1.4) + path("M670 180 V78 H800", sw=1.4) + text(600, 310, "NO", 11) + text(338, 216, "NO", 11)
    b += path("M355 303 V545 H565", sw=1.4) + path("M475 367 V545", sw=1.4, head=False) + text(368, 540, "YES", 11) + text(492, 540, "YES", 11)
    b += path("M355 303 V525 H170 V442", sw=1.4) + path("M685 582 V655", sw=1.4) + path("M805 685 H920 V462", sw=1.4) + arrow(920, 400, 920, 224, sw=1.4) + arrow(920, 162, 920, 110, sw=1.4)
    for cx, cy in [(170, 145), (170, 487), (355, 487), (475, 487), (685, 612), (855, 685), (920, 290), (920, 355)]:
        b += f'<circle cx="{cx}" cy="{cy}" r="17" fill="{INK}"/>'
    b += f'<circle cx="60" cy="720" r="14" fill="{INK}"/>' + text(82, 725, "= Potential Failure Point", 12, anchor="start")
    return svg(1060, 745, b, "A service blueprint for an automobile repair shop across four stages and three levels of customer contact, with potential failure points marked", 1000)
BLUEPRINT = html(blueprint())

def equipment():
    b = text(330, 28, "Selecting\nEquipment", 20, lh=22)
    b += f'<polygon points="300,70 360,70 360,170 385,170 330,215 275,170 300,170" fill="#fff" stroke="{GREY}" stroke-width="2"/>'
    fans = [("Flexibility", 150, 215, 95, 215, "#1a8ad6"), ("Cost", 215, 300, 170, 345, "#2aa3a3"), ("Quality", 290, 335, 275, 400, "#7bbf8e"),
            ("Market\nStability", 370, 335, 385, 400, "#b8a98c"), ("Facility\nCapabilities", 445, 300, 500, 345, "#e08a8a"), ("Cash Flow", 510, 215, 575, 215, "#d62828")]
    for nm, x1, y1, x2, y2, col in fans:
        dx, dy = x2 - x1, y2 - y1; L = math.hypot(dx, dy); ux, uy = dx / L, dy / L
        hx, hy = x2 - ux * 22, y2 - uy * 22
        b += f'<line x1="{x1}" y1="{y1}" x2="{hx:.1f}" y2="{hy:.1f}" stroke="{col}" stroke-width="9" stroke-linecap="round"/>'
        b += f'<polygon points="{x2},{y2} {hx - uy*13:.1f},{hy + ux*13:.1f} {hx + uy*13:.1f},{hy - ux*13:.1f}" fill="{col}"/>'
        tx, ty = x2 + (0 if "\n" in nm else (-10 if x2 < 330 else 10)), y2 + (30 if y2 > 300 else 5)
        b += text(tx, ty, nm, 15, anchor=("middle" if "\n" in nm else ("end" if x2 < 330 else "start")), color=col, lh=17)
    return svg(660, 470, b, "Six factors fan out from selecting equipment: flexibility, cost, quality, market stability, facility capabilities and cash flow", 520)
EQUIP = html(equipment())
PR = {"mar3203-exam2-processes-01-product-process-matrix-diagram.png": ppm, "mar3203-exam2-processes-02-flowchart-lab-work-materials.png": LABFLOW,
      "mar3203-exam2-processes-03-time-function-map-baseline-aluminum-cans.png": TF_BASE, "mar3203-exam2-processes-04-time-function-map-target-aluminum-cans.png": TF_TARGET,
      "mar3203-exam2-processes-05-process-chart-hot-dog-production.png": PROCCHART, "mar3203-exam2-processes-06-service-blueprint-automobile-repair-shop.png": BLUEPRINT,
      "mar3203-exam2-processes-07-selecting-equipment-factors-diagram.png": EQUIP}
PPM_TABLE = html('<table class="sk-tbl financial"><tr><th>Process strategy</th><th>Variety</th><th>Volume</th></tr><tr><td class="lbl">Process focus</td><td>High</td><td>Low</td></tr><tr><td class="lbl">Repetitive focus</td><td>Moderate</td><td>Moderate</td></tr><tr><td class="lbl">Product focus</td><td>Low</td><td>High</td></tr><tr><td class="lbl">Mass customization</td><td>High</td><td>High</td></tr></table>', True)
# the Concise already tabulates the strategies right under this paragraph, so it gets nothing (Ian, 2026-10-26)
PR_ANCH = []
PR_ANCH_TABLE = [{"after": "maps the relationship between a product's <b>variety</b> and <b>volume</b> characteristics", "html": PPM_TABLE["html"], "comment": "the matrix, after the paragraph that defines it"}]

# ================================================================ Capacity
DEM = lambda x: 20 + 0.6 * x
def cap_case(name, steps, caption, wedges):
    """steps: capacity plateaus (x1, x2, level) drawn dashed; wedges: the gold polygons between plateau and demand"""
    curves = [{"id": "dem", "label": "", "pts": [[6, DEM(6)], [98, DEM(98)]]}]
    for i, (x1, x2, lv) in enumerate(steps):
        curves.append({"id": "c%d" % i, "label": "", "pts": [[x1, 0], [x1, lv], [x2, lv], [x2, 0]], "dashed": True, "thin": True})
    return {"label": name, "curves": curves, "areas": [{"pts": w, **GOLD, "label": ""} for w in wedges], "caption": cap(caption),
            "points": [label(30, 94, "New capacity", 0, 0, color="gold"), label(80, 92, "Demand", 0, 0)]}
def lead(steps): return [[[x1, DEM(x1)], [x1, lv], [x2, lv], [x2, DEM(x2)]] for x1, x2, lv in steps]
def lag(steps): return [[[x1, DEM(x1)], [x2, DEM(x2)], [x2, lv], [x1, lv]] for x1, x2, lv in steps]
def avg(steps): return [[[x1, DEM(x1)], [x1, lv], [(lv - 20) / 0.6, lv]] for x1, x2, lv in steps]
capacity = {"title": "Four Ways to Add Capacity Against a Rising Demand",
            "axes": {"x": " ", "y": "Demand", "xmax": 110, "ymax": 100, "bg": False},
            "scenarios": {
                "lead_inc": cap_case("Leading, incremental", [(30, 50, 52), (50, 70, 64)], "Capacity is added a step at a time, each step ahead of the demand it serves, so the shaded wedges are spare capacity.", lead([(30, 50, 52), (50, 70, 64)])),
                "lag_inc": cap_case("Lagging, incremental", [(30, 50, 38), (50, 70, 50)], "Each step is added only once demand has already passed it, so the shaded wedges are unmet demand rather than spare capacity.", lag([(30, 50, 38), (50, 70, 50)])),
                "lead_one": cap_case("Leading, one step", [(30, 70, 64)], "One large investment lifts capacity above demand for the whole period; the shaded wedge is capacity waiting for demand to catch up.", lead([(30, 70, 64)])),
                "avg_inc": cap_case("Average, incremental", [(30, 50, 46), (50, 70, 58)], "Each step straddles the demand line, so the firm is briefly long and then briefly short, staying closest to demand overall.", avg([(30, 50, 46), (50, 70, 58)]))}}
for k, to in {"lead_inc": [44, 55], "lag_inc": [40, 47], "lead_one": [44, 67], "avg_inc": [36, 49]}.items():
    capacity["scenarios"][k]["moves"] = [{"from": [44, 86], "to": to, "color": "ink", "offset": 0}]
TR = lambda q: 1.6 * q; TC = lambda q: 40 + 0.8 * q
BEQ = 40 / 0.8
breakeven = {"title": "Break-Even Analysis",
             "axes": {"x": "Quantity", "y": "$", "xmax": 110, "ymax": 180, "bg": False},
             "curves": [{"id": "tr", "label": "TR", "pts": [[0, 0], [100, TR(100)]], "color": "gold"}, {"id": "tc", "label": "TC", "pts": [[0, 40], [100, TC(100)]], "color": "red"}],
             "areas": [{"pts": [[0, 0], [0, 40], [BEQ, TC(BEQ)]], "color": "red", "at": 1},
                       {"pts": [[BEQ, TR(BEQ)], [100, TR(100)], [100, TC(100)]], "color": "gold", "opacity": 0.45, "at": 2}],
             "points": [{"q": BEQ, "p": TR(BEQ), "guides": "q", "showP": False, "ql": "Break-Even\nPoint", "color": "gold"}],
             "vbraces": [{"q": 0, "p1": 0, "p2": 40, "label": "Fixed\nCosts", "left": True}],
             # the signs were unreadable inside the thin wedges (Ian, 2026-10-26); they ride the braces, whose labels are set large
             "braces": [{"q1": 4, "q2": BEQ - 3, "p": 0, "label": "Loss (−)", "below": True}, {"q1": BEQ + 3, "q2": 92, "p": 0, "label": "Profit (+)", "below": True}],
             "steps": [cap("Total cost starts at the fixed costs and climbs at the variable cost per unit; total revenue starts at zero and climbs at the price."),
                       cap("Below the break-even point revenue is under cost, and the gap between the two lines is a loss."),
                       cap("Above it revenue is over cost, and the gap is operating income; the point itself is where profit is zero.")]}
CAP = {"mar3203-exam2-capacity-management-01-leading-demand-incremental-.png": capacity,
       "mar3203-exam2-capacity-management-02-lagging-demand-incremental-.png": {"keep": "folded into the four-strategy widget above"},
       "mar3203-exam2-capacity-management-03-leading-demand-one-step-exp.png": {"keep": "folded into the four-strategy widget above"},
       "mar3203-exam2-capacity-management-04-average-capacity-incrementa.png": {"keep": "folded into the four-strategy widget above"},
       "mar3203-exam2-capacity-management-07-breakeven-chart-total-reven.png": breakeven}
CAP_ANCH = []   # the strategy table and the break-even formula carry the Concise on their own (Ian, 2026-10-26)
CAP_ANCH_ALL = [{"after": "<td><b>Leading demand — one-step</b></td>", "widget": capacity, "comment": "the four strategies, after their table"},
            {"after": "<li><b>Variable costs (V):</b> change with output (materials, hourly labor, packaging).</li>", "widget": breakeven, "comment": "the break-even chart, after the definitions"}]

for f in (PMCYCLE, NODECONV, LABFLOW, TF_BASE, TF_TARGET, PROCCHART, BLUEPRINT, EQUIP): assert "<script" not in f["html"]
write_map("Exam2-ProjectMgmt", PM); write_map("Exam2-ProjectMgmt-Concise", {}, PM_ANCH)
write_map("Exam2-Processes", PR); write_map("Exam2-Processes-Concise", {}, PR_ANCH)
write_map("Exam2-CapacityMgmt", CAP); write_map("Exam2-CapacityMgmt-Concise", {}, CAP_ANCH)
