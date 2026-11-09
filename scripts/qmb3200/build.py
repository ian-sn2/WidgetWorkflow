#!/usr/bin/env python3
"""QMB3200 (UCF, StudyKnight): every image that is a drawing or a table becomes
an sd-graph figure or HTML. Writes maps/<chapter>.json for apply_widgets.py,
keyed by the image file names of both the Exam 1 and the Exam 2 folders."""
import json, math, pathlib
HERE = pathlib.Path(__file__).resolve().parent
MAPS = HERE / "maps"; MAPS.mkdir(exist_ok=True)

def cap(s, n=200):
    assert len(s) <= n, (len(s), s); return s
NOPT = {"guides": False, "showP": False, "showQ": False}
def dots(pts, color=None):
    return [dict({"q": x, "p": y}, **NOPT, **({"color": color} if color else {})) for x, y in pts]

# ---------------------------------------------------------------- bell curves
MU, SIG = 55, 14
def bell(mu=MU, sig=SIG, peak=100, lo=-3.6, hi=3.6, step=0.2):
    pts = []
    k = lo
    while k <= hi + 1e-9:
        x = mu + k * sig
        if 1.5 <= x <= 108.5:   # a curve stays inside the plot, never past the axis
            pts.append([round(x, 2), round(peak * math.exp(-k * k / 2), 2)])
        k += step
    return pts
def _interp(pts, x):
    for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
        if xa <= x <= xb:
            return round(ya + (yb - ya) * (x - xa) / (xb - xa), 2)
    raise ValueError(x)
def under(pts, x1=None, x2=None):
    """polygon under the bell between x1 and x2 (default whole), cut at exactly x1 and x2"""
    sel = [p for p in pts if (x1 is None or p[0] > x1) and (x2 is None or p[0] < x2)]
    if x1 is not None: sel = [[round(x1, 2), _interp(pts, x1)]] + sel
    if x2 is not None: sel = sel + [[round(x2, 2), _interp(pts, x2)]]
    return [[sel[0][0], 0]] + sel + [[sel[-1][0], 0]]
B = bell()
BELL_AX = {"x": "x", "y": "f(x)", "xmax": 110, "ymax": 112, "bg": False}
EMP_AX = dict(BELL_AX, ymin=-14)
bell_mu_sigma = {
    "title": "The Normal Distribution",
    "axes": BELL_AX,
    "curves": [{"id": "f", "label": "", "pts": B, "curved": True}],
    "areas": [{"pts": under(B), "color": "gold", "opacity": 0.55, "label": ""}],
    "moves": [{"from": [MU - 1, 61], "to": [MU - SIG + 2.5, 61], "color": "ink", "offset": 0}, {"from": [MU + 1, 61], "to": [MU + SIG - 2.5, 61], "color": "ink", "offset": 0}],
    "points": [{"q": MU, "p": 0, "dot": False, "guides": False, "showP": False, "ql": "μ"},
               {"q": MU, "p": 66, "dot": False, "label": "σ", "dx": -4, "dy": 0, **NOPT}],
    "caption": cap("The curve is symmetric about its mean μ, and its width is set by the standard deviation σ. The total area under it is 1."),
}
def sd_labels():
    out = []
    for k, lab in [(-3, "μ−3σ"), (-2, "μ−2σ"), (-1, "μ−σ"), (0, "μ"), (1, "μ+σ"), (2, "μ+2σ"), (3, "μ+3σ")]:
        out.append({"q": MU + k * SIG, "p": 106, "dot": False, "guides": "q", "showP": False, "ql": lab})
    return out
def band(k, y, text, at):
    x1, x2 = MU - k * SIG, MU + k * SIG
    return ({"pts": under(B, x1, x2), "color": "gold", "opacity": 0.22, "label": "", "at": at},
            [{"from": [MU - 3, y], "to": [x1 + 1, y], "color": "ink", "offset": 0, "at": at},
             {"from": [MU + 3, y], "to": [x2 - 1, y], "color": "ink", "offset": 0, "at": at}],
            {"q": MU, "p": y, "dot": False, "label": text, "dx": -17, "dy": -7, "boxed": True, "at": at, **NOPT})
a1, m1, l1 = band(1, 50, "68.26%", 1); a2, m2, l2 = band(2, 9, "95.44%", 2); a3, m3, l3 = band(3, -8, "99.72%", 3)
empirical = {
    "title": "The Empirical Rule",
    "axes": EMP_AX,
    "curves": [{"id": "f", "label": "", "pts": B, "curved": True}],
    "areas": [a1, a2, a3],
    "moves": m1 + m2 + m3,
    "points": sd_labels() + [l1, l2, l3],
    "steps": [cap("A normal random variable's values spread symmetrically about μ, marked here at one, two and three standard deviations either side."),
              cap("68.26% of the values lie within one standard deviation of the mean, between μ − σ and μ + σ."),
              cap("95.44% lie within two standard deviations, between μ − 2σ and μ + 2σ."),
              cap("99.72% lie within three standard deviations, between μ − 3σ and μ + 3σ. Almost nothing lies beyond.")],
}
def three_curves(labels, title, caption):
    return {"title": title, "axes": BELL_AX,
            "curves": [{"id": "inf", "label": "", "pts": bell(sig=10, peak=100), "curved": True},
                       {"id": "ten", "label": "", "pts": bell(sig=13, peak=77), "curved": True, "color": "gold"},
                       {"id": "four", "label": "", "pts": bell(sig=17, peak=59), "curved": True, "color": "grey"}],
            "points": [{"q": 84, "p": 100, "dot": False, "label": labels[0], **NOPT},
                       {"q": 84, "p": 88, "dot": False, "label": labels[1], "color": "gold", **NOPT},
                       {"q": 84, "p": 76, "dot": False, "label": labels[2], "color": "grey", **NOPT}],
            "caption": cap(caption)}
sampling = three_curves(["n = ∞ (n > 30)", "n = 10", "n = 4"], "Sampling Distributions of the Sample Mean",
                        "The larger the sample, the tighter the sampling distribution of the sample mean around μ and the closer it comes to the normal curve.")
tdist = three_curves(["df = ∞ (df > 30)", "df = 10", "df = 4"], "The t-Distribution",
                     "At df = 4 the tails carry far more probability than at df = ∞, which is why t's critical values are larger than z's.")
Z = 1.96
ci = {
    "title": "A 95% Confidence Interval",
    "axes": {"x": " ", "y": " ", "xmax": 110, "ymax": 112, "bg": False},
    "curves": [{"id": "f", "label": "", "pts": B, "curved": True}],
    "areas": [{"pts": under(B, MU - Z * SIG, MU + Z * SIG), "color": "gold", "opacity": 0.55, "label": ".9500", "lp": [MU, 40]},
              {"pts": under(B, None, MU - Z * SIG), "color": "gold", "opacity": 0.22, "label": ""},
              {"pts": under(B, MU + Z * SIG, None), "color": "gold", "opacity": 0.22, "label": ""}],
    "points": [{"q": MU - Z * SIG, "p": 0, "dot": False, "guides": False, "showP": False, "ql": "−z_{α/2}"},
               {"q": MU + Z * SIG, "p": 0, "dot": False, "guides": False, "showP": False, "ql": "z_{α/2}"},
               {"q": MU, "p": 0, "dot": False, "guides": False, "showP": False, "ql": "p\u0305"},
               {"q": MU - 2.8 * SIG, "p": 22, "dot": False, "label": "α/2", "dx": -6, "dy": 0, **NOPT},
               {"q": MU + 2.6 * SIG, "p": 22, "dot": False, "label": "α/2", "dx": -6, "dy": 0, **NOPT}],
    "caption": cap("The middle .9500 of the sampling distribution lies between the two critical z values; each shaded tail holds α/2 = .025."),
}
def rejection(title, tails, caption):
    """tails: list of (side, label) with side 'lo' or 'hi'"""
    zc = 1.645 if len(tails) == 1 else Z
    areas, pts = [], [{"q": MU, "p": 106, "dot": False, "guides": "q", "showP": False, "ql": "μ₀"}]
    moves = []
    lo, hi = None, None
    for side, lab in tails:
        if side == "lo":
            lo = MU - zc * SIG
            areas.append({"pts": under(B, None, lo), "color": "gold", "opacity": 0.22, "label": ""})
            pts.append({"q": MU - 3.4 * SIG, "p": 44, "dot": False, "label": lab, "dx": 0, "dy": 0, **NOPT})
            moves.append({"from": [MU - 3.0 * SIG, 34], "to": [MU - 2.5 * SIG, 10], "color": "ink", "offset": 0})
        else:
            hi = MU + zc * SIG
            areas.append({"pts": under(B, hi, None), "color": "gold", "opacity": 0.22, "label": ""})
            pts.append({"q": MU + 1.9 * SIG, "p": 44, "dot": False, "label": lab, "dx": 0, "dy": 0, **NOPT})
            moves.append({"from": [MU + 2.6 * SIG, 34], "to": [MU + 2.25 * SIG, 11], "color": "ink", "offset": 0})
    areas.insert(0, {"pts": under(B, lo, hi), "color": "gold", "opacity": 0.55, "label": ""})
    return {"title": title, "axes": {"x": "hypothesized\nmean", "y": " ", "xmax": 110, "ymax": 112, "bg": False},
            "curves": [{"id": "f", "label": "", "pts": B, "curved": True}], "areas": areas, "points": pts, "moves": moves, "caption": cap(caption)}
reject_two = rejection("A Two-Tailed Test", [("lo", "rejection\nregion α/2"), ("hi", "rejection\nregion α/2")],
                       "H₀ is rejected if the sample value falls in either tail; each rejection region holds α/2 of the distribution.")
reject_lower = rejection("A Lower-Tail Test", [("lo", "rejection\nregion α")],
                         "The whole of α sits in the lower tail, so the critical value is less extreme than a two-tailed test's.")
reject_upper = rejection("An Upper-Tail Test", [("hi", "rejection\nregion α")],
                         "The whole of α sits in the upper tail, so the critical value is less extreme than a two-tailed test's.")
def scen(w, label):
    sc = {k: w[k] for k in ("areas", "points", "moves", "caption")}; sc["label"] = label; return sc
reject_scen = {"title": "Rejection Regions", "lede": "Pick the form of the alternative hypothesis.",
               "axes": reject_two["axes"], "curves": reject_two["curves"],
               "scenarios": {"two": scen(reject_two, "Two-Tailed"), "lower": scen(reject_lower, "Lower-Tail"), "upper": scen(reject_upper, "Upper-Tail")}}

# ---------------------------------------------------------------- correlation
def strip_band(pts, slope, c1, c2):
    """two dashed lines y = slope x + c clipped to the plot"""
    out = []
    for c in (c1, c2):
        xs = [x for x in (2, 104) ]
        seg = []
        for x in range(2, 117, 2):
            y = slope * x + c
            if 2 <= y <= 146: seg.append([x, round(y, 1)])
        out.append({"id": "b%g" % c, "label": "", "pts": [seg[0], seg[-1]], "dashed": True, "thin": True, "color": "grey"})
    return out
SP = [[10, 14], [18, 22], [24, 20], [30, 36], [36, 40], [42, 50], [48, 56], [50, 46], [56, 62], [62, 68], [70, 66], [76, 80], [84, 86], [90, 92]]
WP = [[12, 44], [16, 62], [22, 30], [30, 70], [34, 52], [38, 24], [46, 60], [50, 42], [56, 84], [62, 36], [68, 70], [76, 50], [84, 78], [90, 60]]
SN = [[s[0], 104 - s[1]] for s in SP]
WN = [[w[0], 104 - w[1]] for w in WP]
def inside(pts, slope, c1, c2, margin=3):
    """every point sits at least `margin` units inside both band lines"""
    lo, hi = sorted((c1, c2))
    for x, y in pts:
        c = y - slope * x
        assert lo + margin <= c <= hi - margin, (x, y, c, lo, hi)
for _pts, _sl, _c1, _c2 in ((SP, 1, 14, -14), (WP, 1, 50, -34), (SN, -1, 118, 90), (WN, -1, 138, 54)):
    inside(_pts, _sl, _c1, _c2)
def sc_case(label, pts, slope, c1, c2, r, rx):
    return {"label": label, "curves": strip_band(pts, slope, c1, c2), "points": dots(pts),
            "caption": None}
scatter4 = {
    "title": "Strong and Weak Correlations",
    "lede": "The tighter the band the points fall in, the closer r is to 1 or −1.",
    "axes": {"x": "x", "y": "y", "xmax": 120, "ymax": 150, "bg": False},
    "scenarios": {
        "sp": {"label": "Strong positive", "curves": strip_band(SP, 1, 14, -14), "points": dots(SP) + [{"q": 72, "p": 40, "dot": False, "label": "r ≥ 0.7", **NOPT}],
               "caption": cap("The points hug a rising line, so r is close to 1: at least 0.7.")},
        "wp": {"label": "Weak positive", "curves": strip_band(WP, 1, 50, -34), "points": dots(WP) + [{"q": 82, "p": 24, "dot": False, "label": "r ≤ 0.5", **NOPT}],
               "caption": cap("The points rise only loosely, so r is positive but small: no more than 0.5.")},
        "sn": {"label": "Strong negative", "curves": strip_band(SN, -1, 118, 90), "points": dots(SN) + [{"q": 72, "p": 70, "dot": False, "label": "r ≤ −0.7", **NOPT}],
               "caption": cap("The points hug a falling line, so r is close to −1: at most −0.7.")},
        "wn": {"label": "Weak negative", "curves": strip_band(WN, -1, 138, 54), "points": dots(WN) + [{"q": 82, "p": 86, "dot": False, "label": "r ≥ −0.5", **NOPT}],
               "caption": cap("The points fall only loosely, so r is negative but small: no less than −0.5.")},
    },
}

# ---------------------------------------------------------------- Hard Rock
HR = [("London", 55.6, 163), ("Cancun", 18.25, 75), ("Reykjavik", 38.4, 110), ("Washington, D.C.", 69.31, 155), ("Chicago", 51.2, 152),
      ("Singapore", 78.1, 189), ("Bangkok", 15.6, 65), ("Miami", 45.7, 121), ("Paris", 56.8, 135), ("Barcelona", 39.7, 105)]
B1, B0 = 0.00189, 38.4233           # the prose's line, x in dollars
def yhat(x_thousands): return B1 * x_thousands * 1000 + B0
assert round(yhat(55.75), 2) == 143.79
HR_AX = {"x": "\nMedian Annual Income ($ thousands)", "y": "Monthly Revenue ($ millions)", "xmax": 90, "ymax": 200,
         "xticks": [10, 20, 30, 40, 50, 60, 70, 80, 90], "yticks": [50, 100, 150, 200], "grid": True, "bg": False}
hr_line = {"id": "fit", "label": "", "pts": [[10, round(yhat(10), 2)], [85, round(yhat(85), 2)]], "dashed": True, "thin": True, "color": "gold"}
hardrock = {"title": "Median Annual Income and Monthly Revenue at 10 Hard Rock Cafe Locations",
            "axes": HR_AX, "curves": [hr_line], "points": dots([(x, y) for _, x, y in HR]),
            "caption": cap("Each dot is one location; the dotted line is the least-squares line through them, rising with income.")}
hardrock_pred = {"title": "A Predicted Value on the Line", "axes": HR_AX, "curves": [hr_line],
                 "points": dots([(x, y) for _, x, y in HR]) + [{"q": 55.75, "p": 143.79, "color": "red", "guides": False, "showP": False, "showQ": False,
                                                                       "label": "($55,750,\n$143.79 million)", "dx": 10, "dy": 18, "at": 1}],
                 "steps": [cap("The ten locations and the fitted line ŷ = 0.00189x + 38.4233."),
                           cap("At a median income of $55,750 the line predicts $143.79 million, so the predicted point sits exactly on it.")]}
# error distributions: a lobe standing on the line at x = 30 and x = 50
def lobe(x0, y0, spread=20, half=20, reach=14):
    pts = []
    t = -half
    while t <= half + 1e-9:
        pts.append([round(x0 + reach * math.exp(-(t / (spread / 2.2)) ** 2), 2), round(y0 + t, 2)]); t += 2
    return pts
def line_y(x): return 30 + 0.5 * x
err_curves, err_areas, err_pts, err_moves = [], [], [], []
for x0, name, tail in ((28, "$30", [72, 29]), (62, "$50", [74, 33])):
    y0 = line_y(x0); L = lobe(x0, y0)
    err_moves.append({"from": tail, "to": [x0 + 8, y0 - 9], "color": "ink", "offset": 0})
    err_curves.append({"id": "stem%d" % x0, "label": "", "pts": [[x0, y0 - 22], [x0, y0 + 22]], "thin": True})
    err_curves.append({"id": "lobe%d" % x0, "label": "", "pts": L, "curved": True, "thin": True})
    err_areas.append({"pts": [[x0, y0]] + [p for p in L if p[1] <= y0 + 1e-9][::-1] + [[x0, y0 - 20]], "color": "gold", "opacity": 0.45, "label": ""})
    err_pts.append({"q": x0, "p": y0, "guides": False, "showP": False, "ql": name})
error_dist = {"title": "Error Probability Distributions",
              "axes": {"x": "\nMedian Annual Income ($ thousands)", "y": "Monthly Revenue ($ millions)", "xmax": 100, "ymax": 100, "bg": False},
              "curves": [{"id": "line", "label": "", "pts": [[8, line_y(8)], [92, line_y(92)]], "color": "gold"}] + err_curves,
              "areas": err_areas,
              "moves": err_moves,
              "points": err_pts + [{"q": 73, "p": 30, "dot": False, "label": "Error probability\ndistributions", "dx": 4, "dy": 10, **NOPT}],
              "caption": cap("At every income the actual revenue scatters around the line's value, with the same bell-shaped spread and a mean of zero.")}

# ---------------------------------------------------------------- GRE
GRE = [(3.0, 55, 250), (3.1, 58, 260), (3.4, 60, 271), (3.3, 65, 275), (3.3, 55, 279), (3.2, 70, 281), (3.4, 80, 285), (3.1, 56, 290), (3.0, 71, 295), (2.9, 59, 295),
       (3.3, 62, 297), (3.4, 65, 298), (3.4, 70, 299), (3.5, 74, 300), (3.6, 76, 300), (3.7, 69, 301), (3.5, 78, 303), (3.7, 80, 305), (3.8, 82, 307), (3.4, 84, 308),
       (3.5, 80, 310), (3.6, 75, 311), (3.8, 76, 312), (3.9, 86, 312), (3.3, 80, 314), (3.7, 95, 315), (3.6, 90, 315), (3.8, 90, 318), (3.8, 100, 319), (3.9, 89, 320)]
assert len(GRE) == 30
gre_two = {"title": "GRE Score Against Each Predictor", "link": False,
           "panels": [{"heading": "GPA", "axes": {"x": "GPA", "y": "GRE Score", "xmin": 2.8, "xmax": 4.0, "ymin": 240, "ymax": 325,
                                                   "xticks": [3.0, 3.2, 3.4, 3.6, 3.8], "yticks": [260, 280, 300, 320], "bg": False},
                       "points": dots([(g, s) for g, h, s in GRE])},
                      {"heading": "Cumulative Study Hours", "axes": {"x": "Study Hours", "y": "GRE Score", "xmin": 50, "xmax": 105, "ymin": 240, "ymax": 325,
                                                                      "xticks": [60, 70, 80, 90], "yticks": [260, 280, 300, 320], "bg": False},
                       "points": dots([(h, s) for g, h, s in GRE])}],
           "caption": cap("The hours plot is the tighter of the two, which is why study hours turns out the stronger predictor.")}

# ---------------------------------------------------------------- Part 3
PROFIT = [(0, -22), (1, -19), (2, -5), (3, 2), (4, 6), (5, 11), (6, 18), (7, 16), (8, 11), (9, 3), (10, -2)]
def quad(x): return -1.0443 * x * x + 12.952 * x - 26.483
QC = [[round(x / 4, 2), round(quad(x / 4), 2)] for x in range(0, 42)]
parabola = {"title": "Output and Profit", "axes": {"x": "\nOutput (1000s)", "y": "Profit (1000s)", "xmax": 12, "ymin": -30, "ymax": 28, "cross": [0, 0],
                                                   "xticks": [2, 4, 6, 8, 10, 12], "yticks": [-30, -20, -10, 10, 20], "bg": False},
            "curves": [{"id": "q", "label": "", "pts": QC, "curved": True, "color": "gold"}],
            "points": dots(PROFIT) + [{"q": 5.2, "p": 25, "dot": False, "label": "y = −1.0443x² + 12.952x − 26.483", "dx": 0, "dy": 0, **NOPT}],
            "caption": cap("Profit rises with output, peaks near 6,000 units and falls again, so a downward-opening parabola fits where a line cannot.")}
CUST = [(1, 520.2), (2, 540.3), (3, 550.6), (4, 570.1), (5, 600.55), (6, 608.52)]
C_AX = {"x": "\nPeriod", "y": "Customers (thousands)", "xmin": 0.5, "xmax": 7.5, "ymin": 500, "ymax": 620, "xticks": [1, 2, 3, 4, 5, 6, 7],
        "yticks": [500, 520, 540, 560, 580, 600, 620], "grid": True, "bg": False}
customers = {"title": "Number of Customers Over Time", "axes": C_AX,
             "curves": [{"id": "c", "label": "", "pts": [list(p) for p in CUST], "curved": True, "color": "gold"}],
             "points": dots(CUST),
             "caption": cap("Customers rose every period from 520,200 in period 1 to 608,520 in period 6, an upward trend a line can summarise.")}
def trend(x): return 18.339 * x + 500.86
customers_trend = {"title": "Number of Customers Over Time, With a Trendline", "axes": C_AX,
                   "curves": [{"id": "c", "label": "", "pts": [list(p) for p in CUST], "curved": True, "color": "gold"},
                              {"id": "t", "label": "", "pts": [[1, round(trend(1), 2)], [6, round(trend(6), 2)]], "dashed": True, "color": "red", "at": 1}],
                   "points": dots(CUST) + [{"q": 4.3, "p": 548, "dot": False, "label": "y = 18339x + 500860", "dx": 0, "dy": 0, "color": "red", "at": 1, **NOPT}],
                   "steps": [cap("The six periods of customer counts, joined in order."),
                             cap("The fitted trendline y = 18339x + 500860 tracks the series closely, with small period-to-period variations either side of it.")]}

# ---------------------------------------------------------------- HTML figures
CSS = """<style>
  .sk-fig { margin: 18px auto; max-width: 640px; }
  .sk-fig svg { display: block; width: 100%; height: auto; font-family: 'Red Hat Display', sans-serif; }
  .sk-fig-venn { max-width: 230px; margin: 14px auto; }
  .sk-fig-right { float: right; width: 42%; max-width: 300px; margin: 0 0 10px 20px; }
  .xl { border-collapse: collapse; margin: 18px auto; font-size: 0.9em; font-family: 'Red Hat Display', sans-serif; background: #fff; max-width: 100%; }
  .xl th, .xl td { padding: 4px 10px; border: 0; text-align: right; white-space: nowrap; }
  .xl th { font-style: italic; font-weight: 600; text-align: center; border-bottom: 1px solid #333; }
  .xl td:first-child, .xl th:first-child { text-align: left; font-style: normal; }
  .xl .xl-head td { font-weight: 700; text-align: left; padding-top: 10px; }
  .xl .xl-rule td { border-top: 1px solid #333; }
  .xl .xl-rule td.nb { border: 0; }
  .xl td, .xl-grid td { font-weight: 400 !important; }
  .xl .xl-head td, .xl-grid tr:first-child td { font-weight: 700 !important; }
  .xl-grid td:first-child { font-weight: 500 !important; }
  .xl .xl-last td { border-bottom: 1px solid #333; }
  .xl .hl { outline: 2px solid #d62828; outline-offset: -2px; }
  .xl .hl-green { outline: 2px solid #2e8b57; outline-offset: -2px; }
  .xl .hl-purple { outline: 2px solid #7a3e9d; outline-offset: -2px; }
  .xl .hl-orange { outline: 2px solid #d8641c; outline-offset: -2px; }
  .xl .hl-yellow { outline: 2px solid #e6c300; outline-offset: -2px; }
  .xl .hl-blue { outline: 2px solid #1a8ad6; outline-offset: -2px; }
  .xl .note { display: block; font-size: 0.74em; font-weight: 700; color: #d62828; white-space: normal; width: 200px; max-width: 100%; margin-left: auto; line-height: 1.2; }
  .xl .note.green { color: #2e8b57; } .xl .note.purple { color: #7a3e9d; } .xl .note.orange { color: #d8641c; } .xl .note.yellow { color: #a08900; } .xl .note.blue { color: #1a6fb0; }
  .xl-wrap { overflow-x: auto; }
  .xl-grid { border-collapse: collapse; margin: 18px auto; font-size: 0.9em; font-family: 'Red Hat Display', sans-serif; background: #fff; }
  .xl-grid th, .xl-grid td { border: 1px solid #c9c9c9; padding: 4px 12px; text-align: right; }
  .xl-grid th { background: #f2f2f2; color: #555; font-weight: 500; text-align: center; }
  .xl-grid td:first-child { background: #f2f2f2; color: #555; text-align: center; }
  .xl-grid tr:first-child td { font-weight: 700; text-align: left; }
  .xl-grid .hl { outline: 2px solid #d62828; outline-offset: -2px; }
  @media (max-width: 640px) { .sk-fig-right { float: none; width: 100%; max-width: 300px; margin: 18px auto; } .xl, .xl-grid { font-size: 0.8em; } .xl th, .xl td { padding: 3px 6px; } }
</style>"""
def venn(union):
    body = ('<text x="150" y="22" text-anchor="middle" font-size="17" font-weight="800" fill="#1c2a44">Sample space S</text>'
            '<rect x="6" y="34" width="288" height="150" rx="16" fill="#efe7c3" stroke="#1c2a44" stroke-width="2.4"/>')
    if union:
        body += ('<circle cx="110" cy="110" r="56" fill="#dcc864" stroke="#1c2a44" stroke-width="2.2"/>'
                 '<circle cx="190" cy="110" r="56" fill="#f3ecd0" fill-opacity="0.85" stroke="#1c2a44" stroke-width="2.2"/>'
                 '<text x="96" y="120" text-anchor="middle" font-size="26" font-weight="800" fill="#1c2a44">A</text>'
                 '<text x="206" y="120" text-anchor="middle" font-size="26" font-weight="800" fill="#1c2a44">B</text>')
        lab = "Sample space S holding two overlapping circles A and B; their union is everything inside either circle"
    else:
        body += ('<circle cx="100" cy="110" r="56" fill="#dcc864" stroke="#1c2a44" stroke-width="2.2"/>'
                 '<text x="100" y="120" text-anchor="middle" font-size="26" font-weight="800" fill="#1c2a44">A</text>'
                 '<text x="222" y="120" text-anchor="middle" font-size="26" font-weight="800" fill="#1c2a44">A’</text>')
        lab = "Sample space S holding a circle A; everything outside the circle is its complement A prime"
    return f'<figure class="sk-fig sk-fig-venn"><svg viewBox="0 0 300 190" role="img" aria-label="{lab}">{body}</svg></figure>'
VENN_COMP, VENN_UNION = venn(False), venn(True)
CORR_LINE = ('<figure class="sk-fig"><svg viewBox="0 0 600 120" role="img" aria-label="A number line from minus one to one; the left half, toward minus one, is negative correlation and the right half, toward one, positive correlation">'
             '<defs><linearGradient id="skcl" x1="0" x2="1"><stop offset="0" stop-color="#f4a3a3"/><stop offset="0.5" stop-color="#f4f4f4"/><stop offset="1" stop-color="#a9cdf3"/></linearGradient></defs>'
             '<path d="M20,60 L90,8 L90,36 L510,36 L510,8 L580,60 L510,112 L510,84 L90,84 L90,112 Z" fill="url(#skcl)"/>'
             '<line x1="30" y1="86" x2="570" y2="86" stroke="#1c2a44" stroke-width="2.4"/>'
             '<line x1="30" y1="72" x2="30" y2="100" stroke="#1c2a44" stroke-width="2.4"/><line x1="300" y1="72" x2="300" y2="100" stroke="#1c2a44" stroke-width="2.4"/><line x1="570" y1="72" x2="570" y2="100" stroke="#1c2a44" stroke-width="2.4"/>'
             '<text x="30" y="118" text-anchor="middle" font-size="16" font-weight="800" fill="#1c2a44">-1</text><text x="300" y="118" text-anchor="middle" font-size="16" font-weight="800" fill="#1c2a44">0</text><text x="570" y="118" text-anchor="middle" font-size="16" font-weight="800" fill="#1c2a44">1</text>'
             '<text x="150" y="52" text-anchor="middle" font-size="15" font-weight="800" fill="#1c2a44"><tspan x="150" dy="0">Negative</tspan><tspan x="150" dy="18">Correlation</tspan></text>'
             '<text x="450" y="52" text-anchor="middle" font-size="15" font-weight="800" fill="#1c2a44"><tspan x="450" dy="0">Positive</tspan><tspan x="450" dy="18">Correlation</tspan></text>'
             '</svg></figure>')

def xl(stats, anova, coefs, notes=None, hl=None, sig=True, label_cols=("df", "SS", "MS", "F", "Significance F")):
    """an Excel SUMMARY OUTPUT as a table. hl: {(section,row,col): class}; notes: {(section,row,col): (text, cls)}"""
    hl = hl or {}; notes = notes or {}
    def cell(sec, r, c, v, tag="td", extra=""):
        cls = hl.get((sec, r, c)); n = notes.get((sec, r, c))
        s = f'<{tag}{" class=\"" + cls + "\"" if cls else ""}{extra}>{v}'
        if n: s += f'<span class="note {n[1]}">{n[0]}</span>'
        return s + f"</{tag}>"
    rows = ['<tr class="xl-head"><td colspan="6">SUMMARY OUTPUT</td></tr>', '<tr class="xl-rule"><th colspan="2">Regression Statistics</th><td colspan="4" class="nb"></td></tr>']
    for i, (k, v) in enumerate(stats):
        rows.append("<tr" + (' class="xl-last"' if i == len(stats) - 1 else "") + ">" + cell("s", i, 0, k) + cell("s", i, 1, v) + '<td colspan="4"></td></tr>')
    rows.append('<tr class="xl-head"><td colspan="6">ANOVA</td></tr>')
    rows.append('<tr class="xl-rule"><th></th>' + "".join(f"<th>{c}</th>" for c in label_cols[:5 if sig else 4]) + ("" if sig else "<td></td>") + "</tr>")
    for i, r in enumerate(anova):
        rows.append("<tr" + (' class="xl-last"' if i == len(anova) - 1 else "") + ">" + "".join(cell("a", i, j, v) for j, v in enumerate(r)) + ("<td></td>" * (6 - len(r))) + "</tr>")
    rows.append('<tr class="xl-rule"><th></th><th>Coefficients</th><th>Standard Error</th><th>t Stat</th><th>P-value</th><td></td></tr>')
    for i, r in enumerate(coefs):
        rows.append("<tr" + (' class="xl-last"' if i == len(coefs) - 1 else "") + ">" + "".join(cell("c", i, j, v) for j, v in enumerate(r)) + "<td></td></tr>")
    return '<div class="xl-wrap"><table class="xl financial">' + "".join(rows) + "</table></div>"
GRE_STATS = [("Multiple R", "0.818538277"), ("R Square", "0.67000491"), ("Adjusted R Square", "0.645560829"), ("Standard Error", "10.51371343"), ("Observations", "30")]
GRE_ANOVA = [("Regression", "2", "6059.636075", "3029.818", "27.4097", "3.16119E-07"), ("Residual", "27", "2984.530592", "110.5382"), ("Total", "29", "9044.166667")]
GRE_COEF = [("Intercept", "180.3224956", "26.21717241", "6.87803", "2.17E-07"), ("GPA", "14.78296833", "10.66585776", "1.386008", "0.177086"), ("Study Hours", "0.896580592", "0.241621025", "3.710689", "0.000947")]
XL13 = xl(GRE_STATS, GRE_ANOVA, GRE_COEF,
          hl={("s", 1, 1): "hl", ("a", 0, 2): "hl-green", ("a", 1, 2): "hl-purple", ("a", 2, 2): "hl-orange", ("c", 0, 1): "hl-yellow", ("c", 1, 1): "hl-yellow", ("c", 2, 1): "hl-yellow"},
          notes={("s", 1, 1): ("= SSR / SST", ""), ("a", 0, 2): ("SSR", "green"), ("a", 1, 2): ("SSE", "purple"), ("a", 2, 2): ("SST", "orange"),
                 ("c", 0, 1): ("b₀", "yellow"), ("c", 1, 1): ("b₁", "yellow"), ("c", 2, 1): ("b₂", "yellow")})
XL14 = xl(GRE_STATS, GRE_ANOVA, GRE_COEF, hl={("a", 1, 3): "hl"}, notes={("a", 1, 3): ("MSE", "")})
XL15 = xl(GRE_STATS, GRE_ANOVA, GRE_COEF, hl={("a", 0, 5): "hl"})
XL16 = ('<div class="xl-wrap"><table class="xl financial"><tr class="xl-rule"><th></th><th>Coefficients</th><th>Standard Error</th><th>t Stat</th><th>P-value</th></tr>'
        '<tr><td>Intercept</td><td>180.3224956</td><td>26.21717241</td><td>6.87803</td><td>2.17E-07</td></tr>'
        '<tr><td>GPA</td><td class="hl">14.78296833</td><td class="hl">10.66585776</td><td class="hl">1.386008</td><td class="hl-blue">0.177086</td></tr>'
        '<tr class="xl-last"><td>Study Hours</td><td class="hl">0.896580592</td><td class="hl">0.241621025</td><td class="hl">3.710689</td><td class="hl-blue">0.000947</td></tr></table></div>')
XL17 = ('<div class="xl-wrap"><table class="xl-grid financial"><tr><th></th><th>A</th><th>B</th><th>C</th><th>D</th></tr>'
        '<tr><td>1</td><td>GPA</td><td>Study Hours</td><td class="hl">Gender</td><td>GRE Score</td></tr>'
        + "".join(f'<tr><td>{i + 2}</td><td>{g}</td><td>{h}</td><td class="hl">{1 if s == "Male" else 0}</td><td>{sc}</td></tr>'
                  for i, (g, h, s, sc) in enumerate([("3.0", 55, "Male", 250), ("3.1", 58, "Female", 260), ("3.4", 60, "Female", 271), ("3.3", 65, "Male", 275), ("3.3", 55, "Female", 279), ("3.2", 70, "Female", 281), ("3.4", 80, "Male", 285)]))
        + "</table></div>")
XL18 = xl([("Multiple R", "0.818683325"), ("R Square", "0.670242387"), ("Adjusted R Square", "0.632193432"), ("Standard Error", "10.71013684"), ("Observations", "30")],
          [("Regression", "3", "6061.783856", "2020.595", "17.61526", "1.89993E-06"), ("Residual", "26", "2982.382811", "114.707"), ("Total", "29", "9044.166667")],
          [("Intercept", "180.6711061", "26.82821589", "6.734369", "3.81E-07"), ("GPA", "14.69695608", "10.88329103", "1.350415", "0.188521"),
           ("Study Hours", "0.899511684", "0.247065459", "3.640783", "0.001184"), ("Gender", "-0.537198402", "3.92585908", "-0.13684", "0.892215")],
          hl={("c", 3, j): "hl" for j in range(5)})
XL_P3 = xl([("Multiple R", "0.989713323"), ("R Square", "0.979532462"), ("Adjusted R Square", "0.974415578"), ("Standard Error", "5544.69824"), ("Observations", "6")],
           [("Regression", "1", "5885306036", "5.89E+09", "191.4314"), ("Residual", "4", "122974714.3", "30743679"), ("Total", "5", "6008280750")],
           [("Intercept", "500860", "5161.833146", "97.03142", "6.76E-08"), ("X Variable 1", "18338.57143", "1325.436393", "13.83587", "0.000158")],
           hl={("s", 1, 1): "hl-blue", ("c", 0, 1): "hl-blue", ("c", 1, 1): "hl-blue"},
           notes={("s", 1, 1): ("high R², close to 1: the equation explains almost all of the data", "blue"), ("c", 0, 1): ("y-intercept (b₀)", "blue"), ("c", 1, 1): ("slope (b₁)", "blue")},
           sig=False)
for f in (CSS, VENN_COMP, VENN_UNION, CORR_LINE, XL13, XL14, XL15, XL16, XL17, XL18, XL_P3):
    assert "<script" not in f

# ---------------------------------------------------------------- maps
def html(block, first=False): return {"html": (CSS if first else "") + block}
P1 = {"01": html(VENN_COMP, True), "02": html(VENN_UNION), "03": bell_mu_sigma, "04": empirical}
P1_NAMES = {"01": ["qmb3200-final-p1-01-venn-diagram-complement-a-aprime.png", "qmb3200-final-exam-part1-01-venn-diagram-complement-a-aprime.png"],
            "02": ["qmb3200-final-p1-02-venn-diagram-union-a-b-overlapping.png", "qmb3200-final-exam-part1-02-venn-diagram-union-a-b.png"],
            "03": ["qmb3200-final-p1-03-normal-distribution-bell-curve-mu-sigma.png", "qmb3200-final-exam-part1-03-normal-distribution-bell-curve-mu-sigma.png"],
            "04": ["qmb3200-final-p1-04-empirical-rule-normal-curve-68-95-99.png", "qmb3200-final-exam-part1-04-empirical-rule-normal-distribution-68-95-99.png"]}
P2 = {"01": sampling, "02": ci, "03": tdist, "04": reject_two, "05": reject_lower, "06": reject_upper, "07": html(CORR_LINE, True), "08": scatter4,
      "09": hardrock, "10": hardrock_pred, "11": error_dist, "12": gre_two, "13": html(XL13), "14": html(XL14), "15": html(XL15), "16": html(XL16), "17": html(XL17), "18": html(XL18)}
P2_NAMES = {k: ["qmb3200-final-p2-%s-%s.png" % (k, n)] for k, n in [("01", "sampling-distribution-normal-curves-n-values"), ("02", "confidence-interval-bell-curve-95-percent"), ("03", "t-distribution-curves-df-values"),
            ("04", "two-tailed-hypothesis-rejection-regions"), ("05", "lower-tail-hypothesis-rejection-region"), ("06", "upper-tail-hypothesis-rejection-region"), ("07", "correlation-coefficient-number-line"),
            ("08", "four-scatterplots-correlation-strong-weak"), ("09", "hard-rock-scatterplot-income-revenue"), ("10", "hard-rock-regression-predicted-point"), ("11", "error-probability-distributions-regression"),
            ("12", "gre-scatterplots-gpa-study-hours"), ("13", "excel-regression-output-gre-summary-2"), ("14", "excel-regression-output-gre-mse-highlight-2"), ("15", "excel-regression-output-significance-f-highlighted"),
            ("16", "excel-output-gpa-study-hours-pvalues"), ("17", "excel-gender-dummy-variable-input"), ("18", "excel-regression-output-gender-included")]}
P3 = {"01": parabola, "02": customers, "03": html(XL_P3, True), "04": customers_trend}
P3_NAMES = {"01": ["qmb3200-final-p3-01-quadratic-parabola-output-profit-chart.png", "brook03-qmb3200-finalpt3-01-quadratic-parabola-output-profit-chart.png"],
            "02": ["qmb3200-final-p3-02-number-of-customers-over-time-line-chart.png", "brook03-qmb3200-finalpt3-02-number-of-customers-over-time-line-chart.png"],
            "03": ["qmb3200-final-p3-03-excel-regression-output-annotated.png", "brook03-qmb3200-finalpt3-04-excel-regression-output.png"],
            "04": ["qmb3200-final-p3-04-number-of-customers-over-time-with-trendline.png", "brook03-qmb3200-finalpt3-03-number-of-customers-trendline-chart.png"]}
def build_map(cfgs, names, anchors, exam, concise_imgs):
    # an anchor's `after` may differ per exam (the two Concise files word the exam tip differently)
    anchors = [dict(a, after=a["after"][exam] if isinstance(a["after"], list) else a["after"]) for a in anchors]
    images = {}
    for k, cfg in cfgs.items():
        nm = names[k][exam] if len(names[k]) > 1 else names[k][0]
        if concise_imgs is None or nm in concise_imgs: images[nm] = cfg
    return {"images": images, "anchors": anchors}
# The Concise carries a widget only where its own text introduces it.
ANCH = {
    "Part1": [{"after": "<tr><td>μ ± 3σ</td><td>99.72%</td></tr>", "widget": empirical, "comment": "the empirical rule, after its table"}],
    "Part2": [{"after": "<h2>Test Statistics and Rejection Rules</h2>", "widget": reject_scen, "comment": "rejection regions, after the heading's table"},
              {"after": "r = −1: perfect negative; r = 0: no linear correlation; r = 1: perfect positive.</li>", "html": CSS + CORR_LINE, "comment": "the correlation number line"}],
    "Part3": [{"after": ["<h4>EXAM TIP: Trendline in Excel</h4>", "<h4>EXAM TIP: Excel Trendline</h4>"], "widget": customers_trend, "comment": "the trendline, after the exam tip, where the Full places its figure"}],
}
CONCISE_IMGS = {"Part1": set(), "Part2": set(), "Part3": {"qmb3200-final-p3-03-excel-regression-output-annotated.png", "brook03-qmb3200-finalpt3-04-excel-regression-output.png"}}
for part, cfgs, names in (("Part1", P1, P1_NAMES), ("Part2", P2, P2_NAMES), ("Part3", P3, P3_NAMES)):
    for exam in (0, 1):
        m = build_map(cfgs, names, ANCH[part], exam, None)
        (MAPS / f"{part}-Exam{exam + 1}.json").write_text(json.dumps(m, ensure_ascii=False, indent=1))
        mc = build_map(cfgs, names, ANCH[part], exam, CONCISE_IMGS[part])
        (MAPS / f"{part}-Exam{exam + 1}-Concise.json").write_text(json.dumps(mc, ensure_ascii=False, indent=1))
        print(part, exam + 1, len(m["images"]), len(mc["images"]))
