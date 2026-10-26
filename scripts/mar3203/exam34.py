"""MAR3203 Exam 3 (Quality Management, SPC) and Exam 4 (Supply Chain Management, Supply Chain Analytics)."""
from common import *

# ================================================================ Quality Management
# four stacked cost bands under a falling total-cost curve; the layers are read off the artwork
XS = list(range(0, 101, 5))
def band(y0, y1, k):
    """a layer boundary that eases from y0 at the left to y1 at the right"""
    return [round(y0 + (y1 - y0) * (x / 100) ** k, 2) for x in XS]
L1 = band(18, 8, 1.1); L2 = band(42, 22, 1.2); L3 = band(74, 44, 1.3); TOP = [round(v, 2) for v in band(100, 56, 2.2)]
def layer(lo, hi): return [[x, lo[i]] for i, x in enumerate(XS)] + [[x, hi[i]] for i, x in enumerate(XS)][::-1]
qcost = {"title": "Quality-Associated Costs",
         "axes": {"x": " ", "y": " ", "xmax": 110, "ymax": 112, "bg": False},
         # the band names are ink point labels, not area labels, which the engine sets in the band's own gold (Ian, 2026-10-26: "camouflaged")
         "areas": [{"pts": layer([0] * len(XS), L1), "color": "gold", "opacity": 0.2}, {"pts": layer(L1, L2), "color": "gold", "opacity": 0.35},
                   {"pts": layer(L2, L3), "color": "gold", "opacity": 0.5}, {"pts": layer(L3, TOP), "color": "gold", "opacity": 0.65}],
         "points": [label(8, 9, "Appraisal"), label(8, 30, "Prevention"), label(8, 52, "Internal Failure"), label(8, 76, "External Failure")],
         "curves": [{"id": "tc", "label": "Total Cost", "pts": [[x, TOP[i]] for i, x in enumerate(XS)], "curved": True, "color": "red", "ldx": -8, "ldy": -10}],
         "caption": cap("External failure is the thickest band and the dearest; as prevention and appraisal do their work, the total cost of quality falls.")}

def tqm_flow():
    rows = [("Organizational\nPractices", "What will the organization accomplish?", "Leadership, mission statement, standard\noperating procedures, staff training and support", 0.18),
            ("Quality\nPrinciples", "How will the organization accomplish its TQM goals?", "Continuous improvement, customer satisfaction\nfocus, JIT, benchmarking, TQM techniques", 0.38),
            ("Employee\nFulfillment", "Will employee attitudes accomplish company objectives?", "Employee empowerment and motivation,\norganizational commitment", 0.62),
            ("Customer\nSatisfaction", "Do organizational practices have a competitive advantage?", "Winning orders, company reputation, repeat\ncustomers", 0.85)]
    b = ""
    for i, (h, q, a, shade) in enumerate(rows):
        y = 10 + i * 140   # a 40px gap between rows, so the arrow can be a proper arrow rather than a squashed chevron (Ian, 2026-10-26)
        fill = f"rgba(201,166,51,{shade})"; dark = shade > 0.5
        b += f'<rect x="10" y="{y}" width="190" height="100" rx="12" fill="{fill}" stroke="{INK}" stroke-width="1.2"/>'
        b += text(105, y + 44, h, 16, color=("#fff" if dark else INK), lh=20)
        b += f'<rect x="220" y="{y}" width="500" height="100" rx="12" fill="#fff" stroke="{GOLDC}" stroke-width="2"/>'
        b += text(236, y + 28, q, 13, anchor="start", italic=True, bold=False) + text(262, y + 54, "➤  " + a, 12.5, anchor="start", bold=False, lh=16)
        if i < 3: b += f'<polygon points="660,{y+102} 676,{y+102} 676,{y+124} 692,{y+124} 668,{y+138} 644,{y+124} 660,{y+124}" fill="{GOLDC}" fill-opacity="{0.4 + 0.2*i}" stroke="{INK}" stroke-width="0.8"/>'
    return svg(730, 550, b, "The flow of activities in TQM: organizational practices lead to quality principles, employee fulfillment and customer satisfaction", 700)
TQM = html(tqm_flow(), True)

def cycle_fig(items, title, aria, r=150):
    """boxes round a ring with a gold arc arrow between neighbours (PDCA, DMAIC)"""
    n = len(items); cx, cy = 320, 220; b = ""
    for i in range(n):
        a0 = -90 + i * 360 / n + 20; a1 = -90 + (i + 1) * 360 / n - 20
        x0, y0 = cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0))
        x1, y1 = cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1))
        b += path(f"M{x0:.1f} {y0:.1f} A{r} {r} 0 0 1 {x1:.1f} {y1:.1f}", sw=4, color=GOLDC)
    fills = ["#1c2a44", "#c9a633", "#b5651d", "#a63d1e", "#8a6d1b", "#6b4f1a"]
    for i, (h, body) in enumerate(items):
        ang = math.radians(-90 + i * 360 / n); bx, by = cx + r * math.cos(ang), cy + r * math.sin(ang)
        rows = body.split("\n"); hh = 40 + 15 * len(rows)
        b += f'<rect x="{bx-92:.1f}" y="{by-hh/2:.1f}" width="184" height="{hh}" rx="12" fill="{fills[i % len(fills)]}"/>'
        b += text(bx, by - hh / 2 + 24, h, 16, color="#fff") + text(bx, by - hh / 2 + 42, body, 11.5, color="#fff", bold=False, lh=14)
    return svg(640, 460, b, aria, 600)
PDCA = html(cycle_fig([("Plan.", "Identify the process defect and\nmake a plan for improvement."), ("Do.", "Experiment with the\nimprovement strategy."),
                       ("Check.", "Evaluate the effectiveness\nof the plan."), ("Act.", "Implement the plan and\ncontinuously document its progress.")],
                      "PDCA", "The plan, do, check, act cycle of continuous improvement"))
DMAIC = html(cycle_fig([("Define.", "Identify customer priorities.\nDetermine metrics of quality\nperformance."), ("Measure.", "Evaluate process defects.\nCollect data from customers."),
                        ("Analyze.", "Identify the root causes of\nquality variation, often\nthrough experimental testing."), ("Improve.", "Design potential solutions to\nminimize variation. Rework\nexisting procedures if necessary."),
                        ("Control.", "Implement statistical process\ncontrol standards and\nprocedures. Inform employees.")],
                       "DMAIC", "The DMAIC cycle: define, measure, analyze, improve, control", r=178))
QM = {"mar3203-exam3-quality-management-01-quality-associated-costs-graph.png": qcost, "mar3203-exam3-quality-management-02-tqm-flow-of-activities-chart.png": TQM,
      "mar3203-exam3-quality-management-03-pdca-cycle-diagram.png": PDCA, "mar3203-exam3-quality-management-04-dmaic-methodology-cycle-diagra.png": DMAIC}
QM_ANCH = []   # the cost bands only picture what the tip says (Ian, 2026-10-26)
QM_ANCH_ALL = [{"after": "<h4>EXAM TIP: Quality-Associated Costs</h4>", "widget": qcost, "comment": "the cost bands, after the tip about them"}]   # the PDCA ring is a diagram: dropped from the Concise (Ian, 2026-10-26)

# ================================================================ SPC
def movie_flow():
    b = box(10, 20, 240, 70, "Arrival", fill="#dfe6e8", fs=15, rx=10)
    hexa = lambda cx, cy, t: f'<polygon points="{cx-130},{cy} {cx-90},{cy-36} {cx+90},{cy-36} {cx+130},{cy} {cx+90},{cy+36} {cx-90},{cy+36}" fill="{PALEG}" stroke="{INK}" stroke-width="1.4"/>' + text(cx, cy + 5, t, 15)
    b += hexa(560, 55, "Buy Tickets") + hexa(200, 265, "Buy Food") + hexa(560, 265, "Watch Movie") + box(830, 380, 240, 70, "Leave", fill="#dfe6e8", fs=15, rx=10)
    b += arrow(254, 55, 424, 55, sw=2) + text(340, 44, "wait", 13)
    b += arrow(560, 91, 560, 224, sw=2) + path("M560 150 H200 V224", sw=2) + text(380, 140, "wait", 13)
    b += arrow(332, 265, 424, 265, sw=2) + path("M560 301 V415 H824", sw=2)
    return svg(1080, 460, b, "A flow diagram for a movie theater: arrival, a wait, buy tickets, then buy food or go straight to the movie, then leave", 640)
MOVIE = html(movie_flow(), True)
def check_sheet():
    def tally(n):
        out = ""
        while n >= 5: out += "<s>||||</s> "; n -= 5
        return out + "|" * n
    rows = [("Dropped calls", [3, 3, 3, 4]), ("Poor battery life", [1, 4, 8, 13]), ("Slow speed", [0, 2, 6, 16])]
    h = '<div class="sk-wrap"><table class="sk-tbl financial"><tr><th></th><th>6 months</th><th>1 year</th><th>1.5 years</th><th>2 years</th></tr>'
    for i, (name, ns) in enumerate(rows):
        h += f'<tr{" class=alt" if i % 2 == 0 else ""}><td class="lbl"><i>{name}</i></td>' + "".join(f'<td class="sk-tally">{tally(n)}</td>' for n in ns) + "</tr>"
    return h + "</table></div>"
CHECK = html(check_sheet())
pareto = {"title": "Analyzing Quality Failures at a Fast-Food Restaurant",
          "axes": {"x": "\nIssue", "y": "Number of Failures", "xmax": 5.9, "ymax": 15, "yticks": [2, 4, 6, 8, 10, 12, 14], "bg": False},
          "areas": [{"pts": [[x - 0.3, 0], [x - 0.3, v], [x + 0.3, v], [x + 0.3, 0]], **GOLD, "edge": True, "label": ""} for x, v in [(0.7, 14), (2.2, 8), (3.7, 7), (5.2, 1)]],
          "points": [{"q": q, "p": 0, "dot": False, "guides": False, "showP": False, "ql": lab} for q, lab in [(0.7, "Long wait"), (2.2, "Late employee"), (3.7, "Wrong order"), (5.2, "No parking")]],
          "caption": cap("Sorted from most to least frequent, the long wait alone accounts for almost half of the failures, so it is the cause to fix first.")}
histo = {"title": "Check-Out Times at Publix",
         "axes": {"x": "\nWait time (minutes)", "y": "# of people per hour", "xmax": 5.4, "ymax": 25, "yticks": [5, 10, 15, 20, 25], "grid": True, "bg": False},
         "areas": [{"pts": [[i, 0], [i, v], [i + 1, v], [i + 1, 0]], **GOLD, "edge": True, "label": str(v), "lp": [i + 0.5, v - 2 if v > 5 else v + 2]} for i, v in enumerate([8, 23, 17, 10, 3])],
         "points": [{"q": i + 0.5, "p": 0, "dot": False, "guides": False, "showP": False, "ql": lab} for i, lab in enumerate(["[0, 1.5]", "(1.5, 3]", "(3, 4.5]", "(4.5, 6]", "(6, 7.5]"])],
         "caption": cap("Most shoppers wait between one and a half and four and a half minutes; waits over six minutes are rare.")}
def fishbone():
    b = f'<line x1="0" y1="325" x2="790" y2="325" stroke="{INK}" stroke-width="2" marker-end="url(#skah)"/>' + box(800, 292, 150, 64, "Effect", fill="#dfe6e8", fs=16)
    for x_top, lab in [(190, "Environment"), (530, "Management")]:
        b += box(x_top - 125, 4, 250, 60, lab, fs=16) + arrow(x_top, 66, x_top + 145, 322, sw=1.6)
    for x_bot, lab in [(185, "People"), (520, "Machinery")]:
        b += box(x_bot - 75, 578, 150, 60, lab, fs=16) + arrow(x_bot, 576, x_bot + 145, 328, sw=1.6)
    b += arrow(0, 118, 210, 118, sw=1.3) + arrow(55, 190, 110, 118, sw=1.3) + arrow(55, 218, 260, 218, sw=1.3)
    b += arrow(375, 183, 580, 183, sw=1.3) + text(455, 170, "Primary Cause", 13) + arrow(455, 255, 500, 183, sw=1.3) + text(395, 240, "Secondary\nCause", 12, lh=14)
    b += arrow(55, 430, 262, 430, sw=1.3) + arrow(110, 505, 165, 430, sw=1.3)
    b += arrow(410, 400, 622, 400, sw=1.3) + arrow(400, 480, 450, 400, sw=1.3) + arrow(500, 480, 550, 400, sw=1.3)
    return svg(960, 650, b, "The outline of a fishbone diagram: environment, management, people and machinery bones running into the effect, with primary and secondary causes along each bone", 640)
FISH = html(fishbone())
VAC = [[10, 22], [18, 32], [26, 23], [32, 48], [44, 36], [44, 62], [56, 64], [58, 55], [68, 68], [76, 58], [84, 92], [92, 82]]
scatter = {"title": "Productivity Against Vacation Days", "axes": {"x": "Number of Vacation Days", "y": "Productivity", "xmax": 110, "ymax": 110, "bg": False},
           "points": dots(VAC, color="gold"), "caption": cap("Productivity rises with vacation days across the points, a positive relationship, which is not the same as one causing the other.")}
CC = [[6, 78], [16, 64], [24, 90], [34, 32], [44, 72], [56, 50], [66, 60], [76, 74], [86, 32]]
control = {"title": "A Control Chart", "axes": {"x": " ", "y": " ", "xmax": 100, "ymax": 110, "bg": False},
           "curves": [{"id": "s", "label": "", "pts": CC, "color": "gold"}],
           "points": [d for i, d in enumerate(dots(CC, color="gold")) if i not in (1, 3, 5)] ,
           "hlines": [{"p": 100, "pl": "", "tag": "Upper Control Limit", "tagq": 60, "tagdy": -6, "dashed": True, "showP": False, "color": "ink"},
                      {"p": 50, "pl": "", "tag": "Target Level", "tagq": 60, "tagdy": 15, "showP": False, "color": "ink"},
                      {"p": 8, "pl": "", "tag": "Lower Control Limit", "tagq": 60, "tagdy": -6, "dashed": True, "showP": False, "color": "ink"}],
           "caption": cap("The samples wander either side of the target but never beyond the two control limits, so the process is in control.")}
def variation(title, peaks, caption):
    """five sideways-offset bells climbing a time axis; peaks are heights, the assignable case has a wandering mean"""
    curves, areas = [], []
    for i, (xc, pk, sig) in enumerate(peaks):
        base = 8 + i * 12
        pts = [[round(xc + k * sig, 2), round(base + pk * math.exp(-k * k / 2), 2)] for k in [j / 10 for j in range(-20, 21, 2)]]
        curves.append({"id": "b%d" % i, "label": "", "pts": pts, "curved": True, "color": "gold"})
        areas.append({"pts": [[pts[0][0], base]] + pts + [[pts[-1][0], base]], "color": "gold", "opacity": 0.3, "label": ""})
        curves.append({"id": "m%d" % i, "label": "", "pts": [[xc, base], [xc, base + pk]], "thin": True, "color": "gold"})
    return {"title": title, "axes": {"x": "Weight", "y": "Frequency", "xmax": 120, "ymax": 110, "bg": False},
            "curves": curves + [{"id": "t", "label": "Time", "pts": [[4, 6], [116, 62]], "thin": True, "color": "grey"}], "areas": areas, "caption": cap(caption)}
random_var = variation("Random Variation", [(22, 36, 7), (40, 36, 7), (58, 36, 7), (76, 36, 7), (94, 36, 7)],
                       "Sample after sample, the weights spread the same way about the same centre: natural variation, which is expected and cannot be controlled.")
assign_var = variation("Assignable Variation", [(22, 36, 7), (40, 52, 4.5), (58, 24, 10), (76, 30, 9), (94, 46, 5.5)],
                       "The spread and the centre shift from one sample to the next: a cause is at work, and it can be found and fixed.")
XB = [[8, 70], [18, 38], [28, 86], [38, 52], [48, 72], [58, 34], [68, 48], [78, 60], [88, 42]]
RB = [[10, 54], [22, 44], [34, 50], [46, 62], [58, 40], [70, 52], [82, 58], [94, 68]]
xbar_r = {"title": "X-bar and R Charts", "link": False,
          "panels": [{"heading": "X-bar Chart", "axes": {"x": "sample means", "y": " ", "xmax": 100, "ymax": 110, "bg": False}, "points": dots(XB, color="gold"),
                      "hlines": [{"p": 92, "pl": "", "tag": "UCL_{x}", "tagq": 101, "showP": False, "color": "ink"}, {"p": 52, "pl": "", "tag": "x̿", "tagq": 101, "dashed": True, "showP": False, "color": "ink"}, {"p": 14, "pl": "", "tag": "LCL_{x}", "tagq": 101, "showP": False, "color": "ink"}]},
                     {"heading": "R-Chart", "axes": {"x": "sample ranges", "y": " ", "xmax": 100, "ymax": 110, "bg": False}, "points": dots(RB, color="gold"),
                      "hlines": [{"p": 92, "pl": "", "tag": "UCL_{R}", "tagq": 101, "showP": False, "color": "ink"}, {"p": 52, "pl": "", "tag": "R̄", "tagq": 101, "dashed": True, "showP": False, "color": "ink"}, {"p": 14, "pl": "", "tag": "LCL_{R}", "tagq": 101, "showP": False, "color": "ink"}]}],
          "caption": cap("The X-bar chart watches the sample means and the R-chart the sample ranges; a point past a control limit on either is a signal to look for a cause.")}
MEANS = [2.05, 1.725, 1.95, 2.2, 3.15]; RANGES = [0.5, 0.6, 0.6, 0.5, 0.6]
tooth = {"title": "Toothpaste Fluoride: X-bar and R Charts", "link": False,
         "panels": [{"heading": "X-bar Chart", "axes": {"x": "\nSample", "y": "Sample Means", "xmin": 0, "xmax": 6.6, "ymin": 1.5, "ymax": 3.4, "xticks": [1, 2, 3, 4, 5], "bg": False},
                     "points": dots([(i + 1, m) for i, m in enumerate(MEANS)], color="gold"),
                     "hlines": [{"p": 2.6238, "pl": "", "tag": "UCL = 2.6238", "tagq": 1.1, "tagdy": -6, "dashed": True, "showP": False, "color": "ink"}, {"p": 2.215, "pl": "", "tag": "x̿ = 2.215", "tagq": 5.9, "tagdy": -6, "showP": False, "color": "ink"},
                                {"p": 1.8062, "pl": "", "tag": "LCL = 1.8062", "tagq": 3.6, "tagdy": 14, "dashed": True, "showP": False, "color": "ink"}]},
                    {"heading": "R-Chart", "axes": {"x": "\nSample", "y": "Sample Ranges", "xmin": 0, "xmax": 6.6, "ymin": -0.2, "ymax": 1.5, "xticks": [1, 2, 3, 4, 5], "bg": False},
                     "points": dots([(i + 1, r) for i, r in enumerate(RANGES)], color="gold"),
                     "hlines": [{"p": 1.2768, "pl": "", "tag": "UCL = 1.2768", "tagq": 1.1, "tagdy": -6, "dashed": True, "showP": False, "color": "ink"}, {"p": 0.56, "pl": "", "tag": "R̄ = 0.56", "tagq": 5.9, "tagdy": -6, "showP": False, "color": "ink"},
                                {"p": 0.0, "pl": "", "tag": "LCL = 0.0", "tagq": 1.1, "tagdy": 14, "dashed": True, "showP": False, "color": "ink"}]}],
         "caption": cap("The R-chart stays quiet because every sample spreads about the same; the trouble is in where the means sit, which only the X-bar chart shows.")}
NB = bell(55, 14, 100, -3.6, 3.6, 0.2, xlo=1.5, xhi=108.5)
normal = {"title": "The Normal Distribution", "axes": {"x": "x", "y": "f(x)", "xmax": 110, "ymax": 112, "bg": False},
          "curves": [{"id": "f", "label": "", "pts": NB, "curved": True}], "areas": [{"pts": under(NB), **GOLD, "label": ""}],
          "moves": [{"from": [54, 61], "to": [43.5, 61], "color": "ink", "offset": 0}, {"from": [56, 61], "to": [66.5, 61], "color": "ink", "offset": 0}],
          "points": [{"q": 55, "p": 0, "dot": False, "guides": False, "showP": False, "ql": "μ"}, label(55, 66, "σ", -4, 0)],
          "caption": cap("The curve is symmetric about its mean μ, and its width is set by the standard deviation σ; the total area under it is 1.")}
def sd_labels():
    return [{"q": 55 + k * 14, "p": 106, "dot": False, "guides": "q", "showP": False, "ql": lab} for k, lab in [(-3, "μ−3σ"), (-2, "μ−2σ"), (-1, "μ−σ"), (0, "μ"), (1, "μ+σ"), (2, "μ+2σ"), (3, "μ+3σ")]]
def eband(k, y, txt, at):
    x1, x2 = 55 - k * 14, 55 + k * 14
    return ({"pts": under(NB, x1, x2), **PALE, "label": "", "at": at},
            [{"from": [52, y], "to": [x1 + 1, y], "color": "ink", "offset": 0, "at": at}, {"from": [58, y], "to": [x2 - 1, y], "color": "ink", "offset": 0, "at": at}],
            label(55, y, txt, -17, -7, boxed=True, at=at))
a1, m1, l1 = eband(1, 50, "68.26%", 1); a2, m2, l2 = eband(2, 9, "95.44%", 2); a3, m3, l3 = eband(3, -8, "99.72%", 3)
empirical = {"title": "The Empirical Rule", "axes": {"x": "x", "y": "f(x)", "xmax": 110, "ymin": -14, "ymax": 112, "bg": False},
             "curves": [{"id": "f", "label": "", "pts": NB, "curved": True}], "areas": [a1, a2, a3], "moves": m1 + m2 + m3, "points": sd_labels() + [l1, l2, l3],
             "steps": [cap("A normal random variable's values spread symmetrically about μ, marked here at one, two and three standard deviations either side."),
                       cap("68.26% of the values lie within one standard deviation of the mean, between μ − σ and μ + σ."),
                       cap("95.44% lie within two standard deviations, between μ − 2σ and μ + 2σ."),
                       cap("99.72% lie within three standard deviations, between μ − 3σ and μ + 3σ. Almost nothing lies beyond.")]}
CLX = bell(66.34, 0.0125, 100, -3.6, 3.6, 0.2)
clorox = {"title": "Is the Clorox Process Capable?",
          "axes": {"x": "\nEthanol content", "y": " ", "xmin": 66.30, "xmax": 66.38, "ymax": 112, "xticks": [66.31, 66.32, 66.33, 66.34, 66.35, 66.36, 66.37], "bg": False},
          "curves": [{"id": "f", "label": "", "pts": CLX, "curved": True}, {"id": "m", "label": "", "pts": [[66.34, 0], [66.34, 100]], "dashed": True, "thin": True},
                     {"id": "lsl", "label": "LSL", "pts": [[66.32, 0], [66.32, 106]], "lstart": False, "color": "ink"}, {"id": "usl", "label": "USL", "pts": [[66.36, 0], [66.36, 106]], "color": "ink"}],
          "areas": [{"pts": under(CLX, 66.32, 66.36), **GOLD, "label": ""}],
          "caption": cap("The mean sits on target, but the tails of the natural variation run past both specification limits, so the process is not capable of meeting them.")}
def cp_case(name, sig, txt, cap_txt, bad):
    B = bell(55, sig, 100, -3.6, 3.6, 0.2, xlo=1.5, xhi=108.5)
    return {"label": name, "curves": [{"id": "f", "label": "", "pts": B, "curved": True}, {"id": "lsl", "label": "LSL", "pts": [[25, 0], [25, 96]], "lstart": True, "color": "ink", "ldy": 14},
                                      {"id": "usl", "label": "USL", "pts": [[85, 0], [85, 96]], "lstart": True, "color": "ink", "ldy": 14}],
            "areas": [{"pts": under(B, 25, 85), **GOLD, "label": ""}] + ([{"pts": under(B, None, 25), "color": "red", "label": ""}, {"pts": under(B, 85, None), "color": "red", "label": ""}] if bad else []),
            "points": [{"q": 55, "p": 0, "dot": False, "guides": False, "showP": False, "ql": "x̄"}, label(60, 104, txt, 0, 0)],
            "caption": cap(cap_txt)}
cpk = {"title": "Process Capability: Specification Limits Against Natural Variation", "lede": "The same specification limits, three different spreads.",
       "axes": {"x": " ", "y": " ", "xmax": 110, "ymax": 112, "bg": False},
       "scenarios": {"lt1": cp_case("Cₚ < 1", 15, "Cₚ < 1", "The natural variation spills past both limits: defective goods are frequently produced.", True),
                     "eq1": cp_case("Cₚ = 1", 10, "Cₚ = 1", "The ±3σ spread just fits between the limits: defective goods are rarely produced, about 0.27% of the time.", False),
                     "gt1": cp_case("Cₚ ≥ 1.33", 7.5, "Cₚ ≥ 1.33", "The spread sits well inside the limits: defective goods are almost never produced.", False)}}
SPC = {"mar3203-exam3-spc-01-movie-theater-flow-chart.png": MOVIE, "mar3203-exam3-spc-15-check-sheet.png": CHECK, "mar3203-exam3-spc-02-pareto-chart-fast-food.png": pareto,
       "mar3203-exam3-spc-03-histogram-checkout-publix-2.png": histo, "mar3203-exam3-spc-04-fishbone-diagram-outline.png": FISH, "mar3203-exam3-spc-05-scatter-plot-productivity-vacation.png": scatter,
       "mar3203-exam3-spc-06-control-chart-example.png": control, "mar3203-exam3-spc-07-random-variation-distribution.png": random_var, "mar3203-exam3-spc-08-assignable-variation-distribution.png": assign_var,
       "mar3203-exam3-spc-09-xbar-rchart-example.png": xbar_r, "mar3203-exam3-spc-10-xbar-rchart-toothpaste.png": tooth, "mar3203-exam3-spc-11-normal-distribution-curve.png": normal,
       "mar3203-exam3-spc-12-empirical-rule-normal-distribution.png": empirical, "mar3203-exam3-spc-13-process-capability-clorox.png": clorox, "mar3203-exam3-spc-14-cp-cpk-diagram.png": cpk}
TOOTH_TABLE = html('<table class="sk-tbl financial"><tr><th>Sample</th><th>1</th><th>2</th><th>3</th><th>4</th><th>5</th><th>Limits</th></tr><tr><td class="lbl">Mean (x̄)</td><td>2.05</td><td class=hl>1.725</td><td>1.95</td><td>2.2</td><td class=hl>3.15</td><td>UCL 2.6238 · x̿ 2.215 · LCL 1.8062</td></tr><tr><td class="lbl">Range (R)</td><td>0.5</td><td>0.6</td><td>0.6</td><td>0.5</td><td>0.6</td><td>UCL 1.2768 · R̄ 0.56 · LCL 0</td></tr></table>', True)
# the Concise keeps the toothpaste table; the empirical-rule and Cp pictures repeat what its text says (Ian, 2026-10-26)
SPC_ANCH = [{"after": "<p>Samples 2 and 5 fall outside X-bar control limits → process is <b>out of control</b>. R-chart alone would miss this shift.</p>", "html": TOOTH_TABLE["html"], "comment": "the toothpaste charts, after the worked example's conclusion"}]
SPC_ANCH_ALL = [            {"after": "<li>±3\\(\\sigma\\): 99.72% of values</li>", "widget": empirical, "comment": "the empirical rule, after the list that states it"},
            {"after": "<tr><td><em>C</em><sub>p</sub> &gt; 1</td><td>Process capable (&gt;1.33 is ideal)</td></tr>", "widget": cpk, "comment": "the three capability cases, after their table"}]

# ================================================================ Supply Chain Management
def chain_net():
    b = ""
    cols = [(40, "Suppliers’\nsuppliers", [60, 160, 260, 360], 22), (210, "Direct\nsuppliers", [130, 290], 40), (500, "Distributors", [130, 290], 40), (660, "Retailers", [60, 160, 260, 360], 22)]
    for x, title, ys, r in cols:
        b += text(x, 22, title, 13, lh=15)
        for y in ys: b += f'<ellipse cx="{x}" cy="{y + 40}" rx="{r + 10}" ry="{r}" fill="{PALEG if r < 30 else GOLDC}" stroke="{INK}" stroke-width="1.2"/>'
    b += box(285, 170, 140, 60, "Manufacturer\n(focal firm)", fill=GOLDC, fs=13, color="#fff", rx=10)
    for y in (100, 200): b += arrow(72, y, 160, 170, sw=1.2)
    for y in (300, 400): b += arrow(72, y, 160, 330, sw=1.2)
    b += arrow(262, 170, 282, 192, sw=1.2) + arrow(262, 330, 282, 208, sw=1.2) + arrow(428, 192, 448, 170, sw=1.2) + arrow(428, 208, 448, 330, sw=1.2)
    for y in (100, 200): b += arrow(552, 170, 628, y, sw=1.2)
    for y in (300, 400): b += arrow(552, 330, 628, y, sw=1.2)
    return svg(720, 440, b, "A supply chain network: suppliers' suppliers feed direct suppliers, which feed the manufacturer, the focal firm, which supplies distributors and then retailers", 640)
CHAIN = html(chain_net(), True)
def pricing_spectrum():
    b = path("M400 40 H740 V20 L790 60 L740 100 V80 H400 Z", color=INK, head=False, fill="#dcc864", sw=1.4) + text(595, 65, "Cost-based price model", 14)
    b += path("M350 40 H200 V20 L150 60 L200 100 V80 H350 Z", color=INK, head=False, fill="#dfe6e8", sw=1.4) + text(275, 65, "Competitive bidding", 14)
    b += f'<rect x="362" y="22" width="4" height="76" fill="#dfe6e8" stroke="{INK}" stroke-width="1"/><rect x="386" y="22" width="4" height="76" fill="#dcc864" stroke="{INK}" stroke-width="1"/>'
    b += text(376, 124, "Market-based\nprice model", 12, lh=14)
    b += text(72, 48, "Short-term\nsupplier\nrelationships", 13, lh=15, anchor="middle") + text(870, 48, "Long-term\nsupplier\nrelationships", 13, lh=15, anchor="middle")
    return svg(940, 150, b, "A spectrum of pricing models: competitive bidding for short-term supplier relationships, a market-based price model in the middle, a cost-based price model for long-term relationships", 700)
PRICING = html(pricing_spectrum())
def hyper(a, b_, k): return [[x, round(a + b_ / (x ** k), 2)] for x in range(6, 101, 4)]
RESP = [[x, round(10 + 420 / (x + 2) ** 1.0, 2)] for x in range(8, 100, 4)]
resp = {"title": "Response Time and the Number of Facilities", "axes": {"x": "Number of facilities", "y": "Time", "xmax": 110, "ymax": 110, "bg": False},
        "curves": [{"id": "rt", "label": "Response Time", "pts": RESP, "curved": True, "color": "gold", "lstart": True, "ldx": 60, "ldy": -14}],
        "caption": cap("Each added facility brings customers closer and cuts the response time, with the biggest gains coming from the first few.")}
FAC = [[x, round(12 + 0.0055 * x * x, 2)] for x in range(6, 101, 4)]
INVC = [[x, round(8 + 22 * (1 - math.exp(-x / 30)) - 0.04 * x, 2)] for x in range(6, 101, 4)]
TRN = [[x, round(14 + 0.012 * (x - 60) ** 2, 2)] for x in range(6, 101, 4)]
TLC = [[x, round(FAC[i][1] + INVC[i][1] + TRN[i][1], 2)] for i, x in enumerate(range(6, 101, 4))]
lowest = min(TLC, key=lambda p: p[1])
costs = {"title": "Total Logistics Cost and the Number of Facilities", "axes": {"x": "Number of facilities", "y": "Cost", "xmax": 125, "ymax": 120, "bg": False},
         "curves": [{"id": "tlc", "label": "Total logistics\ncost", "pts": TLC, "curved": True, "color": "red"}, {"id": "fac", "label": "Facility costs", "pts": FAC, "curved": True, "color": "ink"},
                    {"id": "inv", "label": "Inventory costs", "pts": INVC, "curved": True, "color": "gold", "ldy": 14}, {"id": "trn", "label": "Transportation\ncosts", "pts": TRN, "curved": True, "color": "grey", "ldy": -14}],   # flipped (Ian, 2026-10-26)
         "points": [{"q": lowest[0], "p": lowest[1], "guides": "p", "showQ": False, "showP": False, "color": "red", "label": "Lowest cost", "dx": -40, "dy": -14}],
         "caption": cap("Facility costs rise and transportation costs fall as facilities are added, with inventory in between; their sum dips to a lowest point and then rises again.")}
REV = [[x, round(20 + 70 * (1 - math.exp(-x / 38)), 2)] for x in range(6, 101, 4)]
TLC2 = [[x, round(44 - 0.9 * x + 0.011 * x * x, 2)] for x in range(6, 101, 4)]
best = max(range(len(REV)), key=lambda i: REV[i][1] - TLC2[i][1]); bx = REV[best][0]
profit = {"title": "Revenue, Cost and Profit Against the Number of Facilities", "axes": {"x": "Number of facilities", "y": "$$$", "xmax": 125, "ymax": 110, "bg": False},
          "curves": [{"id": "rev", "label": "Revenue", "pts": REV, "curved": True, "color": "gold"}, {"id": "tlc", "label": "Total logistics\ncost", "pts": TLC2, "curved": True, "color": "red"},
                     {"id": "opt", "label": "", "pts": [[bx, 0], [bx, TLC2[best][1] - 2]], "dashed": True, "thin": True}],   # the guide stops under the cost curve; the arrow carries the gap above it
          # a two-headed arrow between the curves at the best count, named beside it, in place of the brace (Ian, 2026-10-26: "not very aesthetic")
          "moves": [{"from": [bx, TLC2[best][1] + 3], "to": [bx, REV[best][1] - 3], "color": "ink", "offset": 0}, {"from": [bx, REV[best][1] - 3], "to": [bx, TLC2[best][1] + 3], "color": "ink", "offset": 0}],
          "points": [label(bx + 3, (TLC2[best][1] + REV[best][1]) / 2, "Max profit")],
          "caption": cap("Profit is the gap between revenue and total logistics cost, and it is widest at the number of facilities marked by the dashed line.")}
SCM = {"mar3203-exam4-scm-01-supply-chain-diagram-flows.png": CHAIN, "mar3203-exam4-scm-03-pricing-model-spectrum-diagram.png": PRICING,
       "mar3203-exam4-scm-04-response-time-facilities-graph.png": resp, "mar3203-exam4-scm-05-cost-facilities-graph.png": costs, "mar3203-exam4-scm-06-revenue-cost-profit-facilities-graph.png": profit}
facilities = {"title": "Facilities, Response Time, Cost and Profit", "lede": "What happens as a distribution network adds facilities.",
              "axes": resp["axes"],
              "scenarios": {"resp": dict(label="Response time", axes=resp["axes"], curves=resp["curves"], caption=resp["caption"]),
                            "cost": dict(label="Cost", axes=costs["axes"], curves=costs["curves"], points=costs["points"], caption=costs["caption"]),
                            "profit": dict(label="Revenue and profit", axes=profit["axes"], curves=profit["curves"], moves=profit["moves"], points=profit["points"], caption=profit["caption"])}}
SCM_ANCH = []   # the effects table carries it (Ian, 2026-10-26)
SCM_ANCH_ALL = [
            {"after": "<tr><td><strong>Response time</strong></td><td>Decreases (facilities closer to consumers)</td></tr>", "widget": facilities, "comment": "the three facility curves, after the criteria table"}]

# ================================================================ Supply Chain Analytics
def wave(amp, freq, phase, base=40, noise=None):
    return [[x, round(base + amp * math.sin(freq * x / 100 * 2 * math.pi + phase) + (noise(x) if noise else 0), 2)] for x in range(2, 101, 3)]
BW = {"cust": ("Customer", wave(5, 1.2, 0.3, 36), "Customers buy at a steady rate, with only small swings."),
      "ret": ("Retailer", wave(14, 1.3, -0.8, 42), "The retailer reads a small rise as the start of a trend and orders more than it sells."),
      "whl": ("Wholesale", wave(24, 1.6, -0.5, 50), "The wholesaler sees the retailer's larger swings and orders larger still."),
      "mfg": ("Manufacture", wave(38, 2.6, -1.2, 52), "By the manufacturer the orders whip from near zero to the top of the chart, far from the demand that started it.")}
bullwhip = {"title": "The Bullwhip Effect", "lede": "Order quantity over time at each level, moving upstream from the customer.",
            "axes": {"x": "Time", "y": "Order\nQuantity", "xmax": 105, "ymax": 110, "bg": False},
            "scenarios": {k: {"label": lab, "curves": [{"id": "o", "label": "", "pts": pts, "curved": True, "color": "gold"}], "caption": cap(c)} for k, (lab, pts, c) in BW.items()}}
def nodes_fig():
    b = box(20, 20, 150, 110, "Decision", fill="#e3cf7a", fs=16, rx=0, sw=4)
    b += f'<circle cx="330" cy="75" r="56" fill="#e3cf7a" stroke="{INK}" stroke-width="6"/>' + text(330, 71, "Chance\nEvent", 16, lh=18)
    return svg(420, 150, b, "A square decision node and a circular chance-event node", 360)
NODES = html(nodes_fig(), True)   # the first figure carries the sheet; without it the figures sat left (Ian, 2026-10-26)
def tree_fig():
    b = f'<rect x="20" y="170" width="80" height="80" fill="#e3cf7a" stroke="{INK}" stroke-width="5"/>'
    b += path("M100 180 L240 90", sw=2, head=False) + path("M100 240 L240 310", sw=2, head=False)
    for cy, labs in [(90, ("No failure", "Failure")), (310, ("≤ 1 Fail", "Both Fail"))]:
        b += f'<circle cx="270" cy="{cy}" r="34" fill="#e3cf7a" stroke="{INK}" stroke-width="5"/>'
        b += path(f"M300 {cy - 12} L420 {cy - 50} H640", sw=2, head=False) + path(f"M300 {cy + 12} L420 {cy + 50} H640", sw=2, head=False)
        b += text(540, cy - 56, labs[0], 15) + text(540, cy + 70, labs[1], 15)
    b += text(140, 104, "One supplier", 12, italic=True, bold=False) + text(140, 318, "Two suppliers", 12, italic=True, bold=False)   # 28px clear of the branch lines (Ian, 2026-10-26)
    return svg(660, 400, b, "A decision tree: a square decision node branches to two chance nodes, one supplier with the outcomes no failure or failure, two suppliers with the outcomes at most one fails or both fail", 560)
TREE = html(tree_fig())
SCA = {"mar3203-exam4-supply-chain-analytics-01-bullwhip-effect-diagra.png": bullwhip, "mar3203-exam4-supply-chain-analytics-02-decision-chance-nodes.png": NODES,
       "mar3203-exam4-supply-chain-analytics-03-decision-tree-supplier.png": TREE}
SCA_ANCH = []   # the tip explains the bullwhip without the picture (Ian, 2026-10-26)
SCA_ANCH_ALL = [{"after": "<h4>EXAM TIP: Bullwhip Effect Causes and Solutions</h4>", "widget": bullwhip, "comment": "the bullwhip, after the tip about its causes"}]

for f in (TQM, PDCA, DMAIC, MOVIE, CHECK, FISH, CHAIN, PRICING, NODES, TREE): assert "<script" not in f["html"]
write_map("Exam3-QualityMgmt", QM); write_map("Exam3-QualityMgmt-Concise", {}, QM_ANCH)
write_map("Exam3-SPC", SPC); write_map("Exam3-SPC-Concise", {}, SPC_ANCH)
write_map("Exam3-JITLeanOps", {}, []); write_map("Exam3-JITLeanOps-Concise", {}, [])
write_map("Exam4-SupplyChainMgmt", SCM); write_map("Exam4-SupplyChainMgmt-Concise", {}, SCM_ANCH)
write_map("Exam4-SupplyChainAnalytics", SCA); write_map("Exam4-SupplyChainAnalytics-Concise", {}, SCA_ANCH)
