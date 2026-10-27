"""sd-graph configs for the cost-behavior figures in ACG2071 (Exam 1, Cost
Behavior) and ACG3173 (Exam 2, CVP), and the 2x2 grids and spoke diagrams
for MAN3025 and ACG2021. Symbolic axes: every number drawn is one the
picture prints."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "mar3203"))
from common import cap, label, NOPT
from figs import grid2x2, spoke, PALE, FAINT, MID, DEEP

def AX(x, y, **k): return dict({"x": x, "y": y, "xmax": 110, "ymax": 110, "bg": False}, **k)
def line(pts, color="gold", **k): return dict({"id": "c", "label": "", "pts": pts, "color": color}, **k)
def tip(x1, y1, x2, y2, color="gold"): return {"from": [x1, y1], "to": [x2, y2], "color": color, "offset": 0}   # the arrowhead the picture puts on the line
VAR = {"curves": [line([[0, 0], [95, 95]])]}
FIX = {"curves": [line([[0, 55], [95, 55]])]}
DASH = {"id": "f", "label": "", "pts": [[0, 35], [95, 35]], "color": "ink", "dashed": True, "thin": True}       # the fixed component
VDASH = {"id": "v", "label": "", "pts": [[0, 0], [55, 32.4]], "color": "ink", "dashed": True, "thin": True}    # the variable component, the same slope from the origin
MIX = {"curves": [line([[0, 35], [95, 91]]), DASH, VDASH]}

def patterns(xv, xf, xm, lab_var, lab_fix, title="Three Cost Behavior Patterns"):
    return {"title": title, "lede": "Total cost against the activity that drives it.",
            "axes": AX(xv, "Total\nCost"),
            "scenarios": {"var": {"label": "Variable", "axes": AX(xv, "Total\nVariable Cost"), **VAR, "points": [label(52, 104, lab_var)],
                                  "caption": cap("A variable cost starts at the origin and rises in a straight line: with no activity there is no cost, and each unit adds the same amount.")},
                          "fix": {"label": "Fixed", "axes": AX(xf, "Total\nFixed Cost"), **FIX, "points": [label(50, 66, lab_fix)],
                                  "caption": cap("A fixed cost is a horizontal line: rent is the same whether one cup or a thousand are sold.")},
                          "mix": {"label": "Mixed", "axes": AX(xm, "Total\nCost"), **MIX, "points": [label(78, 44, "fixed cost\ncomponent", 0, 0), label(36, 6, "variable cost component", 0, 0)],
                                  "caption": cap("A mixed cost starts above the origin at its fixed part and rises from there at the variable rate per unit.")}}}
COST3 = patterns("Cups of coffee", "Cups of coffee", "Cups of coffee", "Total Variable Cost =\n$0.10 × (# of cups)", "Total Fixed Cost = $450")
COST3_3173 = patterns("Cups of Coffee", "Cups of Coffee", "Miles", "Total Variable Cost =\n$0.10 × Volume", "Total Fixed Cost = $450")
IPHONE = {"title": "A Cell Phone Plan as a Mixed Cost", "axes": AX("Length (in months)", "Total\nCost"), "curves": [line([[0, 35], [95, 91]]), DASH],
          "points": [{"q": 0, "p": 35, "dot": False, "guides": False, "showQ": False, "pl": "$900"}],
          "caption": cap("The $900 phone is paid whatever the plan's length; the $35 a month climbs with it, so total cost is $35x + $900.")}
STEPS = {"title": "Step and Curvilinear Costs", "lede": "Two further shapes a total-cost graph can take.",
         "axes": AX("Volume (units)", "Total\nCost"),
         "scenarios": {"step": {"label": "Step cost", "axes": dict(AX("\nVolume (units)", "Total\nCost"), xmax=400),
                                "curves": [line([[0, 22], [100, 22], [100, 44], [200, 44], [200, 66], [300, 66], [300, 88], [395, 88]])],
                                "points": [{"q": q, "p": p, "dot": False, "guides": "q", "showP": False} for q, p in [(100, 44), (200, 66), (300, 88)]],
                                "caption": cap("Each extra 100 units of capacity needs another factory, so depreciation holds flat and then jumps: cost rises in steps, not a line.")},
                       "curv": {"label": "Curvilinear cost", "axes": AX("Pollution (tons)", "Total\nCost"),
                                "curves": [line([[x, round(x * x / 100, 2)] for x in range(0, 101, 5)], curved=True)],
                                "caption": cap("A curvilinear cost rises faster and faster, the way a regulator's charge grows with each extra ton of pollution.")}}}
RR_X = [[0, 20], [25, 46], [55, 46], [80, 54], [100, 104]]
def ranges(xlab, title="Relevant Ranges"):
    bands = [(0, 25, 0.75), (25, 55, 0.55), (55, 80, 0.35), (80, 100, 0.2)]
    return {"title": title, "axes": AX(xlab, "Total\nCost"),
            "areas": [{"pts": [[a, 0], [a, 100], [b, 100], [b, 0]], "color": "gold", "opacity": o, "label": ""} for a, b, o in bands],
            "curves": [line(RR_X, color="ink")],
            "points": [label((a + b) / 2, 106, "↓", 0, 0) for a, b, o in bands],
            "caption": cap("Within each shaded range the line is straight, so the variable cost per unit and the total fixed cost hold; crossing into the next range changes both.")}
RANGES = ranges("Volume (units)"); RANGES_3173 = ranges("Years")
LC = [[x, round(100 / x * 6, 2)] for x in [6, 7, 8, 9, 10, 12, 14, 17, 20, 25, 30, 40, 50, 65, 80, 100]]
LEARN = {"title": "Learning Curve", "axes": AX("Cumulative Output (in units)", "Average Labor Time\nper unit (in hours)"), "curves": [line(LC, curved=True)],
         "caption": cap("The labor time per unit falls steeply at first and then flattens: each unit takes less than the last, by less and less.")}
PHONE = {"title": "The Phone Bill", "axes": dict(AX("GB of data", "Total\nCost"), xmax=400),
         "curves": [line([[0, 30], [200, 30], [385, 86.6]])],
         "hlines": [{"p": 30, "pl": "$30", "showP": True, "dashed": False, "color": "none", "tag": "", "until": 0}],
         "points": [{"q": 200, "p": 30, "dot": False, "guides": "q", "showP": False}, {"q": 0, "p": 30, "dot": False, "guides": False, "showQ": False, "pl": "$30"}, label(240, 88, "$0.05 per GB", 0, 0)],
         "caption": cap("The bill is flat at $30 until 200 GB and then climbs at $0.05 a gigabyte: a mixed cost whose variable part only starts past the cap.")}
PHONE.pop("hlines")
HL_PTS = [[14, 20], [20, 30], [24, 42], [28, 36], [33, 50], [36, 44], [40, 62], [44, 54], [46, 68], [52, 60], [56, 84]]
def highlow(outlier=False):
    pts = [p[:] for p in HL_PTS]
    if outlier: pts[-1] = [60, 100]
    lo, hi = pts[0], pts[-1]
    m = (hi[1] - lo[1]) / (hi[0] - lo[0]); x1, x2 = lo[0] - 6, hi[0] + 6
    return {"axes": AX("Cost Driver", "Total\nCost"), "curves": [line([[x1, lo[1] - 6 * m], [x2, hi[1] + 6 * m]], color="ink", thin=True)],
            "points": [{"q": q, "p": p, "dot": True, "guides": False, "showP": False, "showQ": False, "color": "gold"} for q, p in pts[1:-1]] +
                      [{"q": lo[0], "p": lo[1], "dot": True, "guides": False, "showP": False, "showQ": False, "label": "low point", "dx": 36, "dy": 12},
                       {"q": hi[0], "p": hi[1], "dot": True, "guides": False, "showP": False, "showQ": False, "label": "high point", "dx": 60, "dy": 4}]}
HIGHLOW = {"title": "The High-Low Method", "lede": "The cost line is drawn straight through the highest and lowest points.",
           "axes": AX("Cost Driver", "Total\nCost"),
           "scenarios": {"ok": {"label": "A clear pattern", **highlow(), "caption": cap("The line through the highest and lowest points runs through the middle of the scatter, so its slope is a fair variable cost per unit.")},
                         "out": {"label": "An outlier high point", **highlow(True), "caption": cap("When the high point sits far from the group the line tilts to reach it, and the cost equation it gives will not fit the rest of the data.")}}}
CAKES = [[1, 40], [3, 95], [4, 150], [6, 180], [7, 240], [9, 230], [10, 290], [12, 320], [15, 400]]
SCATTER = {"title": "High-Low Method Example", "axes": {"x": "Cakes", "y": "Total\nCost", "xmax": 17, "ymax": 450, "bg": False, "money": True},
           "points": [{"q": q, "p": p, "dot": True, "guides": False, "showP": False, "showQ": False, "color": "gold"} for q, p in CAKES[1:-1]] +
                     [{"q": 1, "p": 40, "dot": True, "guides": False, "showP": False, "showQ": False, "label": "(1, $40)", "dx": 42, "dy": 4},
                      {"q": 15, "p": 400, "dot": True, "guides": False, "showP": False, "showQ": False, "label": "(15, $400)", "dx": -62, "dy": -8}],
           "caption": cap("Total cost against cakes baked, with the lowest and highest activity levels marked.")}
STD3 = {"drop": "the three-pattern widget above already draws them; the sentence before now says so (Ian, 2026-10-27)"}

# ------------------------------------------------------------- grids and spokes
SWOT = grid2x2(["Strength", "Opportunity", "Weakness", "Threat"], fills=[PALE, FAINT, "#e9e9e9", "#f4f4f4"], cols=["Internal", "External"], rows=["Good", "Bad"],
               aria="SWOT: strengths and weaknesses are internal, opportunities and threats external; strengths and opportunities good, weaknesses and threats bad", first=True)
BCG = grid2x2(["Question\nMark", "Star", "Dog", "Cash Cow"], fills=[FAINT, PALE, "#f4f4f4", MID], top="Market Share", left="Market Growth Rate", cols=["Low", "High"], rows=["High", "Low"],
              aria="The BCG matrix: question marks and stars have high market growth, dogs and cash cows low; stars and cash cows have high market share", cls="right", maxw=None)
STYLES = grid2x2(["Analytical", "Conceptual", "Directive", "Behavioral"], fills=[PALE, FAINT, "#e9e9e9", "#f4f4f4"], left="Tolerance for Ambiguity", rows=["High", "Low"],
                 bottom="Value Orientation", cols=["Task & Technical", "People & Social"], aria="Four decision-making styles by tolerance for ambiguity and value orientation", first=True)
CVF = grid2x2(["Clan\nCulture", "Adhocracy\nCulture", "Hierarchy\nCulture", "Market\nCulture"], fills=[PALE, FAINT, "#e9e9e9", "#f4f4f4"],
              top="Flexibility\nand Discretion", bottom="Stability\nand Control", left="Internal Focus\nand Integration", right="External Focus\nand Differentiation",
              aria="The competing values framework: clan, adhocracy, hierarchy and market cultures", first=True)
CONFLICT = grid2x2(["Obliging", "Integrating", "Avoiding", "Dominating"], fills=[FAINT, PALE, "#f4f4f4", "#e9e9e9"], top="Concern for Self", left="Concern for Others",
                   cols=["Low", "High"], rows=["High", "Low"], oval="Compromising", aria="Five conflict-handling styles by concern for self and for others", first=True)
ASSETS = spoke("Asset\nAccounts", ["Cash", "Accounts\nReceivable", "Notes\nReceivable", "Inventory", "Supplies", "Prepaid\nExpenses", "Property,\nPlant, and\nEquipment"],
               aria="Asset accounts: cash, accounts receivable, notes receivable, inventory, supplies, prepaid expenses, property plant and equipment")
LIABS = spoke("Liability\nAccounts", ["Accounts\nPayable", "Salaries\nPayable", "Notes\nPayable", "Interest\nPayable", "Utilities\nPayable", "Unearned\nRevenues"],
              aria="Liability accounts: accounts, salaries, notes, interest and utilities payable, and unearned revenues")
