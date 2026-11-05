"""MAR3023 Exam 3 (Fall '26), Chapter 2 final, SVG editions, 2026-11-05.

Yesterday's three Part 1 SVG editions carry everything above today's date pill
unchanged (Ian: "copy/paste everything from the old folder above the date pill
for today"). Today's material comes from the Final FULL, with its five pictures
drawn: Porter's grid and the SWOT matrix as 2x2 grids, the share-ROI chart as a
widget, the share-of-voice pies as flat SVG pies. Balanced and Concise carry a
condensed version of today's material written here.

    python scripts/mar3023/chapter2_final.py OLD_FULL_SVG OLD_BAL_SVG OLD_CON_SVG FINAL_FULL OUTDIR
"""
import sys, os, re, math
sys.path.insert(0, os.path.dirname(__file__))
from pricing import widget, AX, cap, text, INK, GOLDC, PALEG, sub1, replace_img
from figs import fig, grid2x2

DATE = '<p class="date">Thursday, 11/5/26</p>'
BANNER = re.compile(r'\s*<p style="text-align: center; font-size: 125%;"><strong>Dr\. Cooke will wrap up.*?</p>', re.S)
MJX = '<style>mjx-container[display="true"] { max-width: 100%; overflow-x: auto; overflow-y: hidden; }</style>\n</head>'

# ---------------------------------------------------------------- today's figures, in the source's own tints
def clear_labels(s):
    """The grid sets its column and row labels in 13px italic at weight 500, which reads thin (Ian, 2026-11-05):
    upright, 15px, weight 700 here, and the two axis titles a size up. Only these figures; the helper is shared."""
    n = s.count('font-size="13" font-weight="500" fill="#1c2a44" font-style="italic"') + s.count('font-size="13" font-style="italic" fill="#1c2a44"')
    assert n == 4, n
    s = s.replace('font-size="13" font-weight="500" fill="#1c2a44" font-style="italic"', 'font-size="15" font-weight="700" fill="#1c2a44"')
    s = s.replace('font-size="13" font-style="italic" fill="#1c2a44"', 'font-size="15" font-weight="700" fill="#1c2a44"')
    return s.replace('font-size="15" font-weight="800"', 'font-size="17" font-weight="800"')
def porter():
    return grid2x2(["Cost\nLeadership", "Differentiation", "Cost\nFocus", "Differentiation\nFocus"],
                   fills=["#fbe3d4", "#e4f1f4", "#f8c9ad", "#cfe6ea"], fs=16,
                   top="Source of Competitive Advantage", cols=["Lower Cost", "Differentiation"],
                   left="Competitive Scope", rows=["Broad Target", "Narrow Target"], cell=160,
                   aria="Porter's generic strategies: with a broad target, cost leadership or differentiation; with a narrow target, cost focus or differentiation focus")["html"]
def swot():
    return grid2x2(["Strength", "Opportunity", "Weakness", "Threat"],
                   fills=["#bfe5ea", "#ddd6ea", "#f9c4c4", "#d5d9de"], fs=17,
                   cols=["Internal", "External"], rows=["Good", "Bad"], cell=150,
                   aria="SWOT matrix: strengths and weaknesses are internal, opportunities and threats external; strengths and opportunities are good, weaknesses and threats bad")["html"]
ROI_PTS = [[9, 10], [18, 14], [27, 20], [37, 27], [46, 33], [56, 40]]
ROI = {"title": "Market Share and Return on Investment", "axes": AX("\nMarket share (%)", "Average ROI", xmax=64, ymax=52, pct="y", xticks=[10, 20, 30, 40, 50, 60], yticks=[10, 40]),
       "curves": [{"id": "r", "label": "", "pts": ROI_PTS, "color": "gold"}],
       "points": [{"q": q, "p": p, "guides": False, "showP": False, "showQ": False} for q, p in ROI_PTS],
       "caption": cap("The higher a business's market share, the higher its average return on investment.")}

def slice_path(cx, cy, r, a0, a1, fill):
    x0, y0 = cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0))
    x1, y1 = cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1))
    big = 1 if a1 - a0 > 180 else 0
    return f'<path d="M{cx} {cy} L{x0:.1f} {y0:.1f} A{r} {r} 0 {big} 1 {x1:.1f} {y1:.1f} Z" fill="{fill}" stroke="#fff" stroke-width="2"/>'
def pie(cx, cy, r, base, extra, title, ex_label):
    """A flat pie: the firm's base share clockwise from twelve o'clock, any added share just before it."""
    b = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#f4efdc" stroke="{INK}" stroke-width="1.2"/>'
    b += slice_path(cx, cy, r, -90, -90 + base * 3.6, GOLDC)
    am = math.radians(-90 + base * 1.8); b += text(cx + r * .58 * math.cos(am), cy + r * .58 * math.sin(am) + 6, f"{base}%", 17, color="#fff")
    if extra:
        b += slice_path(cx, cy, r, -90 - extra * 3.6, -90, PALEG)
        am = math.radians(-90 - extra * 1.8); b += text(cx + r * .66 * math.cos(am), cy + r * .66 * math.sin(am) + 5, ex_label, 14)
    b += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{INK}" stroke-width="1.2"/>'
    rows = title.count("\n") + 1
    b += text(cx, cy - r - 18 - (rows - 1) * 18, title, 15, lh=18)
    return b
def pies(left, right, aria):
    b = pie(150, 172, 100, *left) + pie(460, 172, 100, *right)
    return fig(610, 285, b, aria, 560)["html"]
PIES_KEEP = lambda: pies((30, 0, "Market Share\nto Maintain", ""), (30, 0, "Share of Marketing Effort\n(Share of Voice)", ""),
                         "Maintenance objective: a 30 percent market share is held with a 30 percent share of voice")
PIES_GROW = lambda: pies((30, 10, "Desired Growth\nin Market Share", "+10%"), (30, 15, "Required Increase in\nMarketing Effort\n(Share of Voice)", "+15%"),
                         "Growth objective: growing market share by 10 points, from 30 to 40 percent, needs 15 more points of share of voice, from 30 to 45 percent")

def draw(t):
    t = replace_img(t, "04-porter-generic-strategies.png", clear_labels(porter()))
    t = replace_img(t, "05-swot-matrix.png", clear_labels(swot()))
    t = replace_img(t, "06-market-share-roi-correlation.png", widget(ROI))
    t = replace_img(t, "07-maintenance-objective-pies.png", PIES_KEEP())
    t = replace_img(t, "08-growth-objective-pies.png", PIES_GROW())
    return t

def today_full(final):
    """Today's material from the Final FULL, with the two markup fixes it needed."""
    t = final[final.index(DATE):final.index("</body>")]
    t = sub1(t, "<strong><u>s</u>trengths, <u>w</u>eaknesses, <u>o</u>pportunities,</strong> and <strong><u>t</u>hreats</strong>",
             "<strong>strengths, weaknesses, opportunities,</strong> and <strong>threats</strong>", "swot u")
    t = sub1(t, "marketing is the investment made to produce sales.</li>\n</ul>\n\n<ul>\n", "marketing is the investment made to produce sales.</li>\n", "budget lists")
    assert "<u>" not in t and "Dr." not in t
    return t

# ---------------------------------------------------------------- the Balanced cut of today's material
def rep(t, prefix, new):
    """Replace the whole <p> or <li> that starts with `prefix`."""
    i = t.index(prefix); assert t.count(prefix) == 1, prefix
    tag = "</p>" if t.rfind("<p", 0, i) > t.rfind("<li", 0, i) else None
    j = t.index("</p>", i) if tag else min(x for x in (t.find("</li>", i), t.find("<img", i), t.find("<ul>", i), t.find("<p>", i), t.find("<div", i)) if x > 0)
    return t[:i] + new + t[j:]
def today_balanced(full):
    t = full
    t = rep(t, "For a corporation, \"long range\" means", "For a corporation, \"long range\" means only about three to five years, but every plan starts from the one-year plan.")
    t = rep(t, "<strong>Executive Summary</strong>", "<strong>Executive Summary</strong> – One-page overview of the year's goals; it sits first but is written last.")
    t = rep(t, "<strong>Budget</strong> –", "<strong>Budget</strong> – The projected costs of marketing operations.")
    t = rep(t, "Typical contents: strengths are capabilities", "Strengths include capabilities, competitive advantages, and people; weaknesses include missing capabilities and cash-flow problems; opportunities come from market developments and trends; threats include political, economic, and legislative changes. The same external development can be a threat or an opportunity, depending on how the firm plays it.")
    t = rep(t, "A SWOT analysis is only the starting point", "A SWOT analysis is only a starting point—a snapshot. It does not make the decisions.")
    t = rep(t, "PetSmart shows the sequence in practice.", "PetSmart shows the sequence in practice. The pet industry was projected to grow by about $500 billion by 2030, but unevenly: food was barely growing while services, veterinary care, and pharmaceuticals grew quickly. Research showed why: people now see themselves as <strong>pet parents</strong>, treating pets as family and spending accordingly. PetSmart built its mission around that segment—its associates \"help bring pet parents closer to their pets so they can live more fulfilled lives\"—with three priorities: Delight the customer, Operate with excellence, Grow pet services (\"DOG\").")
    t = rep(t, "Objectives must carry a specific, measurable target", "Objectives must carry a specific, measurable target—\"grow sales revenue by 10%,\" not \"grow sales revenue.\" PetSmart's goals are the model: support the health of 6 million pets a year and, by 2030, cut emissions intensity 30% and divert 75% of waste from landfills. Two objectives can pull against each other (a 20% revenue increase and a 5% profit increase are hard to achieve at once). Marketing objectives typically focus on one of three priorities:")
    t = rep(t, "<strong>Market Share</strong> – Often called", "<strong>Market Share</strong> – Often called the \"master objective\": market power raises barriers to entry, brand awareness lowers promotion costs, loyalty adds customer lifetime value, and higher share correlates with higher return on investment (ROI). Share also sets each product's strategy: grow early in the life cycle, maintain later, and harvest or divest once share declines.\n    \n    ")
    t = rep(t, "Reynolds (formerly R.J. Reynolds Tobacco)", "Reynolds (formerly R.J. Reynolds Tobacco) shows the logic: marketing support goes to \"drive brands\" such as Camel, Pall Mall, and Newport to grow their share, while \"other brands\" such as Doral get limited support and their profits fund what comes next.")
    t = rep(t, "A marketing program blends strategy and tactics", "A marketing program blends strategy and tactics through the <strong>marketing mix (4 P's)</strong>. Research in the <em>Harvard Business Review</em> asked which elements of the mix raise profitability by more than 1% when increased by 1%. Five did, ranked by impact:")
    t = rep(t, "<strong>Sales Force (Promotion)</strong>", "<strong>Sales Force (Promotion)</strong> – The end of the funnel, so investment there has an outsized effect, especially in B2B. The smart investment is selling time: salespeople spend only about 36% of their time selling, so removing administrative burdens pays off.")
    t = rep(t, "<strong>New Products (Product)</strong>", "<strong>New Products (Product)</strong> – Without new products there are no new sales, because every product eventually dies. R&amp;D spending shows where future sales are expected; the U.S. and China far outspend everyone else, and Amazon, Alphabet, Meta, and Microsoft lead among companies.")
    t = rep(t, "<strong>Product Quality (Product)</strong>", "<strong>Product Quality (Product)</strong> – Quality builds trust and repeat purchase and cuts complaints and returns, raising ROI.")
    t = rep(t, "Price and place showed no effect.", "Price and place showed no effect: price was measured as price-cutting, and channels vary too much to measure in a survey.")
    t = rep(t, "Under the <strong>affordable approach</strong>", "Under the <strong>affordable approach</strong>, companies spend whatever they believe they can afford. It is easy but risky, because it treats marketing as an expense rather than an investment and cuts advertising when sales are low, often when support is most needed.")
    t = rep(t, "Under the <strong>percentage of sales approach</strong>", "Under the <strong>percentage of sales approach</strong>, a firm allocates a fixed percentage of past or projected sales to marketing. It is common, but a bad year starves the next year's marketing, and the logic is backwards: marketing is the investment that produces sales, not the result of them.")
    t = rep(t, "Under the <strong>optimization approach</strong>", "Under the <strong>optimization approach</strong>, marketers find the point at which the marginal revenue from marketing equals its marginal cost. It is the best method in principle, but learning those returns takes experiments most firms cannot run.")
    t = rep(t, "Under the <strong>objective and task approach</strong>", "Under the <strong>objective and task approach</strong>, firms identify specific objectives, outline the tasks required to meet them, and estimate each task's cost; the sum is the budget. It is called \"zero-based budgeting\" because each task starts from zero rather than last year's figure. It is labor-intensive but popular because it links the budget to the firm's goals.")
    t = rep(t, "The 1.5 figure is a rule of thumb", "The 1.5 figure is a rule of thumb that holds up across industries: added voice is never perfectly efficient, so the firm adds half again. Keep the two measures separate—market share is about sales, share of voice about spending.")
    t = rep(t, "A marketing plan should include <strong>contingency plans</strong>", "A marketing plan should include <strong>contingency plans</strong>—predefined actions the firm will take if key assumptions change during the year, such as tariffs, the economy, or supply chain conditions. In practice they are if-then rules set in advance: if a sub-goal is missed by a given date, the rule says what changes.")
    return t

# ---------------------------------------------------------------- the Concise cut of today's material
CONCISE_TODAY = DATE + '''

<h1>Planning Phase of the Strategic Marketing Process</h1>

<p><strong>Output metrics</strong> measure results (revenue growth from new products); <strong>input metrics</strong> track resources invested (new ideas in development). Use both for a full picture of innovation performance.</p>

<h2>Competing Planning Perspectives</h2>

<p><strong>Porter's generic business strategies</strong> – four approaches any firm can use for competitive advantage:</p>

<table>
  <thead><tr><th>Competitive Scope</th><th>Lower Cost</th><th>Differentiation</th></tr></thead>
  <tbody>
    <tr><td><b>Broad target</b></td><td><b>Cost leadership</b> (Walmart, Southwest)</td><td><b>Differentiation</b> (Apple, Nike)</td></tr>
    <tr><td><b>Narrow target</b></td><td><b>Cost focus</b> (IKEA)</td><td><b>Differentiation focus</b> (Chobani)</td></tr>
  </tbody>
</table>

<p><strong>Blue ocean strategy</strong> combines differentiation and low cost by creating new, uncontested markets (Uber, Airbnb, Amazon, Apple). Its <b>Four Actions Grid</b>: <b>eliminate</b> and <b>reduce</b> (lower costs); <b>raise</b> and <b>create</b> (increase differentiation).</p>

<h2>The Annual Marketing Plan</h2>

<p>Long-range plans cover 2–5 years for top executives; the <strong>annual marketing plan</strong> covers one year and includes:</p>

<table>
  <thead><tr><th>Element</th><th>What It Covers</th></tr></thead>
  <tbody>
    <tr><td><b>Executive summary</b></td><td>One-page overview; first in the plan, written last</td></tr>
    <tr><td><b>Situation analysis</b></td><td>Current position, often a SWOT</td></tr>
    <tr><td><b>Objectives</b></td><td>Specific, measurable goals (summit and back safely)</td></tr>
    <tr><td><b>Strategy</b></td><td>The general approach (the route)</td></tr>
    <tr><td><b>Tactics</b></td><td>Concrete actions (food, tents, oxygen)</td></tr>
    <tr><td><b>Budget</b></td><td>Projected marketing costs</td></tr>
    <tr><td><b>Timing</b></td><td>Timeline for each step</td></tr>
    <tr><td><b>Contingency plans</b></td><td>If-then rules for a changed environment</td></tr>
  </tbody>
</table>

<h2>Situation Analysis (SWOT)</h2>

<table>
  <thead><tr><th></th><th>Internal</th><th>External</th></tr></thead>
  <tbody>
    <tr><td><b>Favorable</b></td><td><b>Strengths</b> (Tesla: brand value)</td><td><b>Opportunities</b> (Tesla: new markets, autonomy)</td></tr>
    <tr><td><b>Unfavorable</b></td><td><b>Weaknesses</b> (Tesla: manufacturing delays)</td><td><b>Threats</b> (Tesla: rival EV makers)</td></tr>
  </tbody>
</table>

<p>The same external development can be a threat or an opportunity. SWOT is a snapshot; it does not make the decisions.</p>

<h2>Segments, Value Proposition, and Objectives</h2>

<ul>
  <li>After the SWOT, identify segments, choose targets, and position. PetSmart targets <strong>pet parents</strong>, who treat pets as family.</li>
  <li>A <strong>customer value proposition</strong> must be <b>relevant</b>, <b>specific</b>, and <b>distinctive</b> (its <strong>points of difference</strong>).</li>
  <li>Objectives need a measurable target ("grow sales 10%"). They focus on <b>sales revenue</b>, <b>profit</b>, or <b>market share</b>, the "master objective" because it raises barriers to entry, lowers promotion cost, builds loyalty, and correlates with higher ROI.</li>
  <li>Market share strategies: <b>growth</b>, <b>maintenance</b>, <b>harvest</b>, <b>divest</b>. Reynolds grows its "drive brands" and harvests "other brands" such as Doral.</li>
</ul>

<div class="exam-tip">
    <h4>EXAM TIP: Marketing Objectives</h4>
    <p>Be able to identify which of these strategies is being demonstrated in a given example.</p>
</div>

<h2>Marketing Program Formulation</h2>

<p>Elements of the mix that raise profitability by more than 1% per 1% increase, ranked: <b>sales force</b> (salespeople spend only ~36% of their time selling), <b>new products</b>, <b>product quality</b>, <b>advertising</b>, <b>sales promotion</b>. Price (measured as price-cutting) and place showed no effect.</p>

<h2>Budgeting for the Marketing Effort</h2>

<table>
  <thead><tr><th>Approach</th><th>How It Works</th><th>Drawback</th></tr></thead>
  <tbody>
    <tr><td><b>Affordable</b></td><td>Spend what the firm can afford</td><td>Treats marketing as an expense; cuts it when sales fall</td></tr>
    <tr><td><b>Percentage of sales</b></td><td>Fixed % of past or projected sales</td><td>Backwards logic; a bad year starves the next</td></tr>
    <tr><td><b>Optimization</b></td><td>Marginal revenue = marginal cost</td><td>Needs experiments few firms can run</td></tr>
    <tr><td><b>Objective and task</b></td><td>Sum the cost of each task needed to meet objectives ("zero-based")</td><td>Labor-intensive, but links budget to goals</td></tr>
    <tr><td><b>Competitive parity</b></td><td>Match or beat competitors' spending</td><td>Assumes rivals' budgets are right</td></tr>
  </tbody>
</table>

<p><strong>Share of voice</strong> = firm's marketing expense ÷ industry marketing expense.</p>
<ul>
  <li><b>Maintenance objective</b>: share of voice = market share (30% share → 30% voice).</li>
  <li><b>Growth objective</b>: the <strong>1.5 rule of thumb</strong>.</li>
</ul>

<p>\\[\\Delta \\text{ Share of voice} = 1.5 \\times \\Delta \\text{ Market share}\\]</p>

<p>Example: growing share from 30% to 40% (+10) needs +15 points of voice, or 45%; once at 40%, scale back to 40%.</p>

<div class="exam-tip">
    <h4>EXAM TIP: 1.5 Rule</h4>
    <p>The required increase in share of voice is 1.5 times the desired growth in market share.</p>
</div>

<h2>Contingency Plans and Planning Lessons</h2>

<ul>
  <li><strong>Contingency plans</strong> are if-then rules made <b>during</b> planning, when decisions can be objective.</li>
  <li>Good plans have measurable goals, realistic assumptions, and simple, specific language, and they involve the people who will carry them out.</li>
  <li>Common problems: wrong assumptions about the environment, losing focus on customers, overlong plans, and excluding frontline managers.</li>
</ul>

'''
CONCISE_GLOSS = '''    <tr><td><b>Output and input metrics</b></td><td>Results achieved versus resources invested</td></tr>
    <tr><td><b>Generic business strategy</b></td><td>Porter's cost leadership, differentiation, cost focus, or differentiation focus</td></tr>
    <tr><td><b>Blue ocean strategy</b></td><td>Creating uncontested markets that combine differentiation and low cost</td></tr>
    <tr><td><b>Annual marketing plan</b></td><td>One-year roadmap of goals, strategies, tactics, budget, and timing</td></tr>
    <tr><td><b>Situation analysis (SWOT)</b></td><td>Internal strengths and weaknesses, external opportunities and threats</td></tr>
    <tr><td><b>Customer value proposition</b></td><td>The relevant, specific, distinctive benefits a firm promises</td></tr>
    <tr><td><b>Share of voice</b></td><td>Firm's marketing expense ÷ industry marketing expense</td></tr>
    <tr><td><b>1.5 rule of thumb</b></td><td>Raise share of voice by 1.5 times the desired market share gain</td></tr>
    <tr><td><b>Contingency plan</b></td><td>Predefined actions if key assumptions change</td></tr>
'''
CONCISE_TAKE = '''  <li>Porter: broad or narrow target × lower cost or differentiation; blue ocean creates a new market instead.</li>
  <li>Objectives are set by the mountain metaphor: objectives are the summit, strategy the route, tactics the gear.</li>
  <li>Strengths and weaknesses are internal; opportunities and threats are external.</li>
  <li>Market share is the master objective; grow, maintain, harvest, or divest by life-cycle stage.</li>
  <li>The sales force has the largest profit effect of any mix element; price-cutting has none.</li>
  <li>Objective and task budgeting links spending to goals; competitive parity uses share of voice.</li>
  <li>Maintain: voice = share. Grow: Δ voice = 1.5 × Δ share (30% → 40% share needs 45% voice).</li>
'''

def build(old_full, old_bal, old_con, final, outdir):
    rd = lambda p: open(p, encoding="utf-8").read()
    final = rd(final); today = today_full(final)
    outs = {}
    for name, old, part in (("FULL", old_full, today), ("Balanced", old_bal, today_balanced(today))):
        t = BANNER.sub("", rd(old), 1); assert "Dr. Cooke will wrap up" not in t and DATE not in t
        i = t.index("</body>"); t = t[:i].rstrip() + "\n\n" + draw(part).rstrip() + "\n\n" + t[i:]
        outs[name] = t
    t = BANNER.sub("", rd(old_con), 1); assert "Dr. Cooke will wrap up" not in t
    t = sub1(t, "<h2>Glossary</h2>", CONCISE_TODAY + "<h2>Glossary</h2>", "concise today")
    gl = t.index("<h2>Glossary</h2>"); j = t.index("  </tbody>", gl); t = t[:j] + CONCISE_GLOSS + t[j:]
    kt = t.index("<h2>Key Takeaways</h2>"); j = t.index("</ul>", kt); t = t[:j] + CONCISE_TAKE + t[j:]
    t = sub1(t, "Objectives are set by the mountain metaphor: objectives are the summit", "The mountain metaphor: objectives are the summit", "takeaway wording")
    if "@media (max-width:600px){table" not in t:
        t = sub1(t, "</head>", "<style>@media (max-width:600px){table{display:block;overflow-x:auto}}</style>\n</head>", "concise tables")
    outs["Concise"] = t
    for name, t in outs.items():
        if 'mjx-container[display="true"]' not in t: t = sub1(t, "</head>", MJX, "mjx " + name)
        assert t.count(DATE) == 1 and "<u>" not in t
        p = os.path.join(outdir, f"MAR3023-263-Exam3-Chapter2-Final-{name}.html")
        open(p, "w", encoding="utf-8").write(t); print("wrote", p)

if __name__ == "__main__":
    build(*sys.argv[1:6])
