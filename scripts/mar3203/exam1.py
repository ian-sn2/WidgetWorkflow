"""MAR3203 Exam 1: Operations & Productivity, Forecasting, Inventory, Z-table."""
from common import *

# ================================================================ Operations
def ford():
    b = ""
    # the two big flow arrows above, the two-way one below
    b += path("M100 60 H520 V38 L600 80 L520 122 V100 H100 Z", color=INK, head=False, fill="#dcc864", sw=1.4)
    b += text(350, 85, "Goods and services", 14)
    b += path("M600 150 H180 V128 L100 170 L180 212 V190 H600 Z", color=INK, head=False, fill="#fbf1c7", sw=1.4)
    b += text(390, 175, "Returns and money", 14)
    cols = [("Tier 2 Suppliers", "Rubber harvesters\nMetal manufacturers\nLeather producers"), ("Tier 1 Suppliers", "Tire producers\nEngine manufacturers\nSeat producers"), ("Retailers", "Ford\n(Automotive retailer)")]
    for i, (h, body) in enumerate(cols):
        x = 30 + i * 225
        b += f'<rect x="{x}" y="240" width="200" height="130" rx="12" fill="#fff" stroke="{INK}" stroke-width="1.6"/>'
        b += f'<rect x="{x}" y="240" width="200" height="40" rx="12" fill="{GOLDC}" stroke="{INK}" stroke-width="1.6"/><rect x="{x}" y="262" width="200" height="18" fill="{GOLDC}"/>'
        b += text(x + 100, 266, h, 15, color="#fff")
        b += text(x + 100, 310, body, 12.5, bold=False, lh=17)
        if i < 2: b += arrow(x + 204, 320, x + 221, 320, sw=3)
    b += path("M130 420 H570 M130 420 l12 -9 M130 420 l12 9 M570 420 l-12 -9 M570 420 l-12 9", sw=2.2, head=False)
    b += text(350, 450, "Information and Planning", 14)
    return svg(700, 470, b, "A supply chain for Ford: tier 2 suppliers to tier 1 suppliers to the retailer; goods and services flow right, returns and money flow left, information and planning flow both ways", 640)
FORD = html(ford(), True)

def pie():
    parts = [("Management", 52, GOLDC), ("Capital", 38, "#e3cf7a"), ("Labor", 10, "#f3e8bd")]
    cx, cy, r = 200, 125, 105; a0 = -90; b = ""
    for name, pct, fill in parts:
        a1 = a0 + pct * 3.6
        x0, y0 = cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0))
        x1, y1 = cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1))
        b += f'<path d="M{cx} {cy} L{x0:.1f} {y0:.1f} A{r} {r} 0 {1 if pct > 50 else 0} 1 {x1:.1f} {y1:.1f} Z" fill="{fill}" stroke="#fff" stroke-width="2"/>'
        am = math.radians((a0 + a1) / 2); k = {"Management": 0.46, "Capital": 0.6, "Labor": 0.7}[name]; lx, ly = cx + r * k * math.cos(am), cy + r * k * math.sin(am)  # the wide name sits well inside its slice (Ian, 2026-10-26)
        b += text(lx, ly, f"{name}\n{pct}%", 13, lh=16)
        a0 = a1
    return svg(400, 250, b, "Contributions to productivity growth: management 52 percent, capital 38 percent, labor 10 percent", 360)
PIE = html(pie())

LC = bell(55, 16, 100, -3.2, 3.2, 0.2, xlo=1, xhi=109)
def lc_div(x): return {"id": "d%g" % x, "label": "", "pts": [[x, 0], [x, interp(LC, x)]], "dashed": True, "thin": True}
lifecycle = {"title": "The Product Life Cycle",
             "axes": {"x": "Time", "y": "Sales", "xmax": 110, "ymax": 112, "bg": False},
             "curves": [{"id": "lc", "label": "", "pts": LC, "curved": True, "color": "gold"}, lc_div(28), lc_div(50), lc_div(72)],
             # the phase names sit above the curve, over their own band (Ian, 2026-10-23: inside, the curve ran through them)
             "areas": [{"pts": under(LC, None, 28), "color": "gold", "opacity": 0.2},
                       {"pts": under(LC, 28, 50), "color": "gold", "opacity": 0.35},
                       {"pts": under(LC, 50, 72), "color": "gold", "opacity": 0.5},
                       {"pts": under(LC, 72, None), "color": "gold", "opacity": 0.35}],
             "points": [label(2, 44, "Introduction"), label(33, 102, "Growth"), label(61, 110, "Maturity"), label(86, 56, "Decline")],
             "caption": cap("Sales climb through introduction and growth, level off at maturity and fall in decline, so the production run lengthens and then shortens again.")}

def global2x2():
    b = text(320, 24, "Global Operations Strategies", 17)  # centred over the grid, which spans x 150-490 (Ian, 2026-10-26)
    b += f'<rect x="150" y="40" width="340" height="230" rx="18" fill="#fff" stroke="{INK}" stroke-width="2"/>'
    cells = [(165, 55, "Global strategy"), (325, 55, "Transnational\nstrategy"), (165, 160, "International\nstrategy"), (325, 160, "Multidomestic\nstrategy")]
    for x, y, t in cells: b += box(x, y, 150, 95, t, fill=PALEG, fs=14, rx=12)
    b += path("M110 60 V250 M110 60 l-9 14 M110 60 l9 14 M110 250 l-9 -14 M110 250 l9 -14", sw=2.2, head=False)
    b += text(110, 52, "High", 12) + text(110, 268, "Low", 12) + text(55, 155, "Cost\nReduction", 13, lh=16)
    b += path("M170 300 H470 M170 300 l14 -9 M170 300 l14 9 M470 300 l-14 -9 M470 300 l-14 9", sw=2.2, head=False)
    b += text(150, 304, "Low", 12, anchor="end") + text(490, 304, "High", 12, anchor="start") + text(320, 332, "Local Responsiveness", 13)
    return svg(520, 345, b, "Four global operations strategies on a grid of cost reduction against local responsiveness: international low on both, global high cost reduction, multidomestic high responsiveness, transnational high on both", 520)
GLOBAL = html(global2x2())

OPS = {"ucf-mar3203-operations-exam1-01-ford-supply-chain.png": FORD, "ucf-mar3203-operations-exam1-02-productivity-pie-chart.png": PIE,
       "ucf-mar3203-operations-exam1-03-product-life-cycle.png": lifecycle, "ucf-mar3203-operations-exam1-04-global-operations.png": GLOBAL}
OPS_ANCH = [{"after": "<b>Supply chain management</b>: coordinating operations processes across a network of businesses.</p>", "html": CSS + ford(), "comment": "the Ford supply chain"},
            {"after": "<tr><td><b>Decline</b></td><td>Cost control; reduce capacity</td><td>Overcapacity risk</td></tr>", "widget": lifecycle, "comment": "the life cycle, after its table"},
            {"after": "<tr><td><b>Transnational</b></td><td>High</td><td>High</td><td>HQs worldwide; moves materials/labor/ideas across borders (P&amp;G)</td></tr>", "html": global2x2(), "comment": "the strategy grid, after its table"}]

# ================================================================ Forecasting
ZONE = [[0, 10], [10, 16], [25, 24], [40, 36], [55, 50], [65, 62], [72, 76], [78, 88], [84, 94], [92, 92], [98, 78], [96, 60], [86, 46], [70, 36], [50, 26], [30, 17], [12, 12], [0, 10]]
zone = {"title": "The Zone of Uncertainty",
        "axes": {"x": "Time", "y": "Demand", "xmax": 110, "ymax": 110, "bg": False},
        "areas": [{"pts": ZONE, "color": "gold", "opacity": 0.55, "label": ""}],
        "curves": [{"id": "exp", "label": "", "pts": [[0, 10], [72, 64]], "dashed": True}],
        "moves": [{"from": [74, 65.5], "to": [86, 74.5], "color": "ink", "offset": 0}],
        "points": [label(20, 70, "zone of\nuncertainty", 0, 0), label(78, 100, "Expected\ndemand", 0, 0)],
        "caption": cap("The further ahead the forecast reaches, the wider the band of possible demand around the expected path.")}

YEARS = list(range(2000, 2011))
CONST = [500, 455, 478, 531, 511, 499, 476, 501, 531, 490, 499]
TREND = [390, 400, 420, 435, 425, 460, 450, 475, 510, 500, 525]
SEAS = [300, 310, 425, 500, 515, 450, 390, 375, 450, 520, 435, 380]
def series(xs, ys, color="gold"):
    return {"curves": [{"id": "s", "label": "", "pts": [[x, y] for x, y in zip(xs, ys)], "color": color}], "points": dots(list(zip(xs, ys)))}
# no source picture for the cyclical case (Ian asked for one, 2026-10-23): the years are the series' own axis,
# the demand axis carries no numbers, and the shape is a long irregular swing rather than a calendar repeat
CYC = [470, 500, 540, 520, 480, 430, 410, 440, 500, 560, 530]
patterns = {"title": "Four Time-Series Patterns", "lede": "Plot the data first: the pattern decides the method.",
            "axes": {"x": "\nYear", "y": "Demand", "xmin": 1999.5, "xmax": 2010.5, "ymin": 350, "ymax": 650, "xticks": [2000, 2002, 2004, 2006, 2008, 2010], "yticks": [350, 400, 450, 500, 550, 600, 650], "years": True, "grid": True, "bg": False},
            "scenarios": {
                "const": dict(series(YEARS, CONST), label="Constant mean", caption=cap("Demand wanders a little above and below one level, with nothing to it but random variation.")),
                "trend": dict(series(YEARS, TREND), label="Trend", axes={"x": "\nYear", "y": "Demand", "xmin": 1999.5, "xmax": 2010.5, "ymin": 350, "ymax": 550, "xticks": [2000, 2002, 2004, 2006, 2008, 2010], "yticks": [350, 390, 430, 470, 510, 550], "years": True, "grid": True, "bg": False},
                              caption=cap("Demand still bounces period to period, but the bounces ride a steady upward trend.")),
                "seas": dict(series(list(range(1, 13)), SEAS), label="Seasonal", axes={"x": "\nMonth", "y": "Demand", "xmin": 0.5, "xmax": 12.5, "ymin": 200, "ymax": 600, "xticks": list(range(1, 13)), "yticks": [200, 300, 400, 500, 600], "grid": True, "bg": False},
                             caption=cap("Demand peaks in spring and again in autumn and dips between, a pattern tied to the calendar rather than a trend.")),
                "cyc": dict(series(YEARS, CYC), label="Cyclical", axes={"x": "\nYear", "y": "Demand", "xmin": 1999.5, "xmax": 2010.5, "ymin": 350, "ymax": 650, "xticks": [2000, 2002, 2004, 2006, 2008, 2010], "years": True, "grid": True, "bg": False},
                            caption=cap("Demand rises and falls in long swings of no fixed length, following the business cycle rather than the calendar."))}}
BOB = [10000, 18600, 7100, 4200, 10500, 19420, 7000, 4900, 11200, 19400, 7250, 4100, 10800, 18500, 6710, 4605]
bobs = {"title": "Bob's River Place Attendance 2013–2016",
        "axes": {"x": "\nPeriod", "y": "Attendance (thousands)", "xmin": 0, "xmax": 16.5, "ymax": 25, "xticks": [2, 4, 6, 8, 10, 12, 14, 16], "yticks": [5, 10, 15, 20, 25], "grid": True, "bg": False},
        "curves": [{"id": "b", "label": "", "pts": [[i + 1, v / 1000] for i, v in enumerate(BOB)], "curved": True, "color": "gold"}],
        "points": dots([(i + 1, v / 1000) for i, v in enumerate(BOB)]),
        "caption": cap("Attendance peaks every fourth period, the summers, and bottoms out each winter; the peaks sit at about the same height, so the pattern is seasonal around a constant mean.")}
CUST = [(1, 520.2), (2, 540.3), (3, 550.6), (4, 570.1), (5, 600.55), (6, 608.52)]
C_AX = {"x": "\nPeriod", "y": "Customers (thousands)", "xmin": 0.5, "xmax": 7.5, "ymin": 500, "ymax": 620, "xticks": [1, 2, 3, 4, 5, 6, 7], "yticks": [500, 520, 540, 560, 580, 600, 620], "grid": True, "bg": False}
customers = {"title": "Number of Customers Over Time", "axes": C_AX,
             "curves": [{"id": "c", "label": "", "pts": [list(p) for p in CUST], "curved": True, "color": "gold"}], "points": dots(CUST),
             "caption": cap("Customers rose every period from 520,200 in period 1 to 608,520 in period 6, an upward trend a line can summarise.")}
def trend_y(x): return 18.339 * x + 500.86
customers_trend = {"title": "Number of Customers Over Time, With a Trendline", "axes": C_AX,
                   "curves": [{"id": "c", "label": "", "pts": [list(p) for p in CUST], "curved": True, "color": "gold"},
                              {"id": "t", "label": "", "pts": [[1, round(trend_y(1), 2)], [6, round(trend_y(6), 2)]], "dashed": True, "color": "red", "at": 1}],
                   "points": dots(CUST) + [label(4.3, 548, "y = 18339x + 500860", color="red", at=1)],
                   "steps": [cap("The six periods of customer counts, joined in order."),
                             cap("The fitted trendline y = 18339x + 500860 tracks the series closely, with small period-to-period variations either side of it.")]}
def excel_p3():
    rows = ['<tr><td colspan="6" style="text-align:left;font-weight:700;border:0;padding-top:8px">SUMMARY OUTPUT</td></tr>',
            '<tr><th colspan="2">Regression Statistics</th><td colspan="4" style="border:0"></td></tr>']
    for k, v, note in [("Multiple R", "0.989713323", ""), ("R Square", "0.979532462", "high R², close to 1: the equation explains almost all of the data"), ("Adjusted R Square", "0.974415578", ""), ("Standard Error", "5544.69824", ""), ("Observations", "6", "")]:
        cls = ' class="hi"' if note else ""
        rows.append(f'<tr><td style="text-align:left">{k}</td><td{cls}>{v}' + (f'<br><span style="font-size:.74em;color:#1a6fb0;font-weight:700">{note}</span>' if note else "") + '</td><td colspan="4" style="border:0"></td></tr>')
    rows.append('<tr><td colspan="6" style="text-align:left;font-weight:700;border:0;padding-top:8px">ANOVA</td></tr><tr><th></th><th>df</th><th>SS</th><th>MS</th><th>F</th><td style="border:0"></td></tr>')
    for r in [("Regression", "1", "5885306036", "5.89E+09", "191.4314"), ("Residual", "4", "122974714.3", "30743679", ""), ("Total", "5", "6008280750", "", "")]:
        rows.append("<tr>" + "".join(f'<td{" style=text-align:left" if i == 0 else ""}>{v}</td>' for i, v in enumerate(r)) + '<td style="border:0"></td></tr>')
    rows.append('<tr><th></th><th>Coefficients</th><th>Standard Error</th><th>t Stat</th><th>P-value</th><td style="border:0"></td></tr>')
    for r, note in [(("Intercept", "500860", "5161.833146", "97.03142", "6.76E-08"), "Y-intercept (b₀)"), (("X Variable 1", "18338.57143", "1325.436393", "13.83587", "0.000158"), "Slope (b)")]:
        rows.append(f'<tr><td style="text-align:left">{r[0]}</td><td class="hi">{r[1]}<br><span style="font-size:.74em;color:#1a6fb0;font-weight:700">{note}</span></td>' + "".join(f"<td>{v}</td>" for v in r[2:]) + '<td style="border:0"></td></tr>')
    return '<div class="sk-wrap"><table class="sk-tbl financial" style="font-size:.85em">' + "".join(rows) + "</table></div>"
EXCEL = html(excel_p3())
HR = [(55.6, 163), (18.25, 75), (38.4, 110), (69.31, 155), (51.2, 152), (78.1, 189), (15.6, 65), (45.7, 121), (56.8, 135), (39.7, 105)]
def yhat(x): return 0.00189 * x * 1000 + 38.4233
assert round(yhat(55.75), 2) == 143.79
HR_AX = {"x": "\nMedian Annual Income ($ thousands)", "y": "Monthly Revenue ($ millions)", "xmax": 90, "ymax": 200, "xticks": [10, 20, 30, 40, 50, 60, 70, 80, 90], "yticks": [50, 100, 150, 200], "grid": True, "bg": False}
hardrock = {"title": "Median Annual Income and Monthly Revenue at 10 Hard Rock Cafe Locations", "axes": HR_AX,
            "curves": [{"id": "fit", "label": "", "pts": [[10, round(yhat(10), 2)], [85, round(yhat(85), 2)]], "dashed": True, "thin": True, "color": "gold"}],
            "points": dots(HR) + [{"q": 55.75, "p": 143.79, "color": "red", "guides": False, "showP": False, "showQ": False, "label": "($55,750,\n$143.79 million)", "dx": 10, "dy": 18, "at": 1}],
            "steps": [cap("The ten locations and the fitted line ŷ = 0.00189x + 38.4233."), cap("At a median income of $55,750 the line predicts $143.79 million, so the predicted point sits exactly on the line.")]}
DEM = [616, 460, 716, 1402, 806, 512, 930, 1606, 940, 650, 1108, 1972, 1200, 956, 685, 2420, 1275, 1016, 1372, 2690]
def tl(x): return 59.23 * x + 544.68
demand20 = {"title": "Demand Over Time",
            "axes": {"x": "\nPeriod", "y": "Number of Customers", "xmin": 0, "xmax": 21, "ymax": 3000, "xticks": [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21], "yticks": [500, 1000, 1500, 2000, 2500, 3000], "grid": True, "bg": False},
            "curves": [{"id": "d", "label": "", "pts": [[i + 1, v] for i, v in enumerate(DEM)], "color": "gold"},
                       {"id": "t", "label": "", "pts": [[1, round(tl(1), 1)], [20, round(tl(20), 1)]], "at": 1}],
            "points": dots([(i + 1, v) for i, v in enumerate(DEM)]) + [label(8.5, 2900, "y = 59.23x + 544.68", at=1)],
            "steps": [cap("Twenty quarters of demand: every fourth quarter spikes, and the spikes grow."),
                      cap("The regression line y = 59.23x + 544.68 carries the trend; each quarter sits above or below it in a repeating pattern, which is the seasonal index.")]}
FC = {"mar3203-exam1-forecasting-01-demand-uncertainty-zone-chart.png": zone, "mar3203-exam1-forecasting-02-demand-constant-mean-chart-2.png": {"drop": "folded into the three-pattern widget after the list"},
      "mar3203-exam1-forecasting-03-demand-trend-chart-2.png": {"drop": "folded into the three-pattern widget after the list"}, "mar3203-exam1-forecasting-04-demand-seasonal-chart-2.png": {"drop": "folded into the three-pattern widget after the list"},
      "mar3203-exam1-forecasting-05-bobs-river-place-attendance-2013-2016-2.png": bobs, "mar3203-exam1-forecasting-06-number-of-customers-over-time-chart-2.png": customers,
      "mar3203-exam1-forecasting-07-excel-data-function.png": EXCEL, "mar3203-exam1-forecasting-10-number-of-customers-trendline-chart-2.png": customers_trend,
      "mar3203-exam1-forecasting-08-hard-rock-cafe-scatter-plot-2.png": hardrock, "mar3203-exam1-forecasting-09-demand-over-time-seasonal-trend-chart-2.png": demand20}
FC_CONCISE = {"mar3203-exam1-forecasting-07-excel-data-function.png": html(excel_p3(), True)}
# Full and Balanced: the one widget stands after the list of all four patterns (Ian, 2026-10-23), so the three pictures inside the list go
FC_FULL_ANCH = [{"after": "<li><em>Demand is patterned cyclically</em>", "lead": "<h4>EXAM TIP: Plotting Data</h4>", "widget": patterns, "comment": "the demand patterns, after the list that introduces all four, under the plotting tip moved out of item 1"}]
FC_ANCH = [{"after": "<h4>EXAM TIP: Plotting Data</h4>", "widget": patterns, "comment": "the three patterns, after the list that names them"},
           {"after": "<h4>EXAM TIP: Trendline Function</h4>", "widget": customers_trend, "comment": "the trendline, after the exam tip that introduces it"}]

# ================================================================ Inventory
abc = {"title": "ABC Analysis",
       "axes": {"x": "\nPercentage of Inventory", "y": "Percentage of Annual Expenses", "xmax": 105, "ymax": 100, "xticks": [10, 20, 30, 40, 50, 60, 70, 80, 90, 100], "yticks": [10, 20, 30, 40, 50, 60, 70, 80, 90, 100], "bg": False},
       "areas": [{"pts": [[0, 0], [0, 80], [20, 80], [20, 0]], "color": "gold", "opacity": 0.75, "edge": True, "label": "A", "lp": [10, 86]},
                 {"pts": [[20, 0], [20, 17], [50, 17], [50, 0]], "color": "gold", "opacity": 0.45, "edge": True, "label": "B", "lp": [35, 23]},
                 {"pts": [[50, 0], [50, 8], [100, 8], [100, 0]], "color": "gold", "opacity": 0.22, "edge": True, "label": "C", "lp": [75, 14]}],
       "caption": cap("A items are a fifth of the inventory but four fifths of the annual spend; C items are half the inventory and under a tenth of the spend.")}
saw = {"title": "Inventory Level Over Time Under an EOQ Model",
       "axes": {"x": "Time", "y": "Inventory Level", "xmax": 110, "ymax": 110, "bg": False},
       "areas": [{"pts": [[0, 0], [0, 90], [33, 0]], "color": "gold", "opacity": 0.25, "edge": True, "label": ""},
                 {"pts": [[33, 0], [33, 90], [66, 0]], "color": "gold", "opacity": 0.45, "edge": True, "label": ""},
                 {"pts": [[66, 0], [66, 90], [99, 0]], "color": "gold", "opacity": 0.65, "edge": True, "label": ""}],
       "hlines": [{"p": 45, "pl": "", "tag": "Average\nInventory (Q/2)", "tagq": 80, "dashed": True, "showP": False, "color": "ink"}],
       "points": [{"q": 0, "p": 90, "dot": False, "guides": False, "showQ": False, "pl": "Q"}],
       "caption": cap("Inventory falls steadily to zero, an order of Q arrives and refills it, and the cycle repeats, so the average on hand is Q/2.")}
H, S_, D_ = 0.8, 1800, 1.0
EOQC = [[q, round(H * q / 2, 2)] for q in range(5, 111, 5)]
ORDC = [[q, round(S_ / q, 2)] for q in range(8, 101, 2)]
TOTC = [[q, round(H * q / 2 + S_ / q, 2)] for q in range(8, 101, 2)]
EOQ = math.sqrt(2 * S_ / H)
eoq = {"title": "EOQ: Where Total Cost Is Lowest",
       "axes": {"x": "\nOrder Quantity (Q)", "y": "Annual Cost", "xmax": 118, "ymax": 240, "bg": False},
       "curves": [{"id": "tc", "label": "Total Cost", "pts": TOTC, "curved": True, "color": "gold", "ldy": -9},
                  {"id": "hc", "label": "Holding Cost", "pts": [[0, 0], [100, 40]], "color": "grey", "ldy": 2},
                  {"id": "oc", "label": "Ordering Cost", "pts": ORDC, "curved": True, "ldy": 2}],
       "points": [{"q": round(EOQ, 1), "p": round(H * EOQ / 2 + S_ / EOQ, 1), "guides": "q", "showP": False, "ql": "EOQ"}],
       "caption": cap("Holding cost rises with the order size and ordering cost falls with it; their sum is lowest where the two cross, which is the EOQ.")}
INV = {"mar3203-exam1-ch12-02-abc-analysis-bar-chart-annual-expenses-in.png": abc, "mar3203-exam1-ch12-03-eoq-inventory-level-over-time-sawtooth-di.png": saw, "mar3203-exam1-ch12-04-eoq-total-cost-holding-ordering-cost-grap.png": eoq}
INV_ANCH = [{"after": "<h4>EXAM TIP: 80/20 Rule</h4>", "widget": abc, "comment": "ABC analysis, after the 80/20 tip"},
            {"after": "<h4>EXAM TIP: Quantity Discounts</h4>", "widget": eoq, "comment": "the EOQ cost curves, before the formulas"}]

# ================================================================ Z-table
ZB = bell(0, 1, 100, -3.6, 3.6, 0.2)
zcurve = {"title": "The Standard Normal Curve",
          "axes": {"x": "z", "y": " ", "xmin": -3.8, "xmax": 3.8, "ymax": 112, "bg": False},
          "curves": [{"id": "z", "label": "", "pts": ZB, "curved": True}, {"id": "mid", "label": "", "pts": [[0, 0], [0, 100]], "dashed": True, "thin": True}],
          "areas": [{"pts": under(ZB, None, 0), **GOLD, "label": ""}],
          "moves": [{"from": [-2.3, 72], "to": [-0.95, 30], "color": "ink", "offset": 0}],   # the head lands inside the shaded area, not on the curve (Ian, 2026-10-26)
          "points": [label(-3.3, 86, "P(z ≤ 0)", 0, 0)] + [{"q": k, "p": 0, "dot": False, "guides": False, "showP": False, "ql": lab} for k, lab in [(-3, "−3σ"), (-2, "−2σ"), (-1, "−1σ"), (0, "μ = 0"), (1, "+1σ"), (2, "+2σ"), (3, "+3σ")]],
          "caption": cap("Every entry in the table is an area like this one, measured from the far left up to the z in question.")}
ZT = {}
import math as _m
def _phi(z): return 0.5 * (1 + _m.erf(z / _m.sqrt(2)))
def ztable(rows, hl=None, first=False):
    """rows: list of z tenths (e.g. 0.8..1.8); hl: (row, col-tenth pair) lookup to mark"""
    out = ['<div class="sk-wrap"><table class="sk-tbl financial"><tr><th><i>z</i></th>' + "".join(f'<th{" class=hl" if hl and c in hl["cols"] else ""}>{c:.2f}</th>' for c in [i / 100 for i in range(10)]) + "</tr>"]
    for i, z in enumerate(rows):
        cells = []
        for c in range(10):
            v = _phi(z + c / 100)
            cls = ""
            if hl:
                if abs(z - hl["row"]) < 1e-9 and c / 100 in hl["cols"]: cls = ' class="hl"'
                elif abs(z - hl["row"]) < 1e-9 and c / 100 < min(hl["cols"]): cls = ' class="hi"'
                elif c / 100 in hl["cols"] and z < hl["row"]: cls = ' class="hi"'
            cells.append(f"<td{cls}>{v:.4f}</td>")
        out.append(f'<tr{" class=alt" if i % 2 == 0 else ""}><td class="lbl">{z:.1f}</td>' + "".join(cells) + "</tr>")
    return "".join(out) + "</table></div>"
ZFULL = html(ztable([i / 10 for i in range(0, 21)]), True)
ZARROWS = html(ztable([i / 10 for i in range(8, 19)], hl={"row": 1.6, "cols": [0.04, 0.05]}))
ZTB = {"mar3203-exam1-ztable-01-standard-normal-curve-pz-less-equal-zero.png": zcurve, "mar3203-exam1-ztable-02-z-table.png": ZFULL, "mar3203-exam1-ztable-03-z-table-arrows.png": ZARROWS}
ZT_ANCH = [{"after": "<li>Total area under the curve : 1.00; left half (z ≤ 0) : 0.50.</li>", "widget": zcurve, "comment": "the standard normal curve, after the list that states its halves"},
           {"after": "\\[z = \\frac{1.64 + 1.65}{2} = 1.645\\]", "html": CSS + ztable([i / 10 for i in range(8, 19)], hl={"row": 1.6, "cols": [0.04, 0.05]}), "comment": "the lookup, after the example that reads it"}]

for f in (FORD, PIE, GLOBAL, EXCEL, ZFULL, ZARROWS): assert "<script" not in f["html"]
write_map("Exam1-OperationsProductivity", OPS)
write_map("Exam1-OperationsProductivity-Concise", {}, OPS_ANCH)
write_map("Exam1-Forecasting", FC, FC_FULL_ANCH)
write_map("Exam1-Forecasting-Concise", FC_CONCISE, FC_ANCH)
write_map("Exam1-InventoryMgmt", INV)
write_map("Exam1-InventoryMgmt-Concise", {}, INV_ANCH)
write_map("Exam1-ZTableSupplement", ZTB)
write_map("Exam1-ZTableSupplement-Concise", {}, ZT_ANCH)
