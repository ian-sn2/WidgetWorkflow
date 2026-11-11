"""MAN4504 Exam 3, Aggregate Planning: Balanced and Concise editions of both widget options.

    python scripts/man4504/transport_editions.py SOURCE-FULL.html OUTDIR

Balanced: the Full (as transport.py builds it, per option) with side remarks and repeated examples trimmed.
Concise: rewritten as tables and bullets; the transportation-method widget stays, since the text cannot show
the table being filled without it. Every number is the source's, and the method costs are recomputed here.
"""
import os, re, sys

sys.path.insert(0, os.path.dirname(__file__))
import transport as T  # noqa: E402


def rep(t, old, new, n=1):
    assert t.count(old) == n, (old[:90], t.count(old))
    return t.replace(old, new)


def words(html):
    body = html[html.index("<body>"):]
    body = re.sub(r"<script.*?</script>|<style>.*?</style>|<noscript>.*?</noscript>", " ", body, flags=re.S)
    return len(re.sub(r"<[^>]+>", " ", body).split())


# ------------------------------------------------------------------ the graphical methods, recomputed
DEM = [900, 700, 800, 1200, 1500, 1100]; DAYS = [22, 18, 21, 21, 22, 20]
assert sum(DEM) == 6200 and sum(DAYS) == 124
inv, ends = 0, []
for d, n in zip(DEM, DAYS): inv += 50 * n - d; ends.append(inv)
assert ends == [200, 400, 650, 500, 100, 0] and sum(ends) * 5 == 9250
M1 = 9250 + 10 * 80 * 124; M2 = 1488 * 20 + 7.6 * 80 * 124; M3 = 99200 + 9000 + 9600
assert (M1, round(M2), M3) == (108450, 105152, 117800) and 38 * 124 == 4712 and 6200 - 4712 == 1488


# ------------------------------------------------------------------ Balanced
def balanced(t):
    t = rep(t, "<p>Snapper, a maker of lawn and garden equipment, illustrates why aggregate forecasts are more dependable. The company sells roughly 180 different models, ranging from backyard mowers to golf course equipment, and it cannot say with confidence which model will be the hot seller. It is, however, quite good at forecasting totals: for example, about 150,000 units in January, which is roughly 25% more than February, with March sales slipping a little under 10% from February's level.</p>",
            "<p>Snapper, which sells about 180 models of lawn and garden equipment, cannot say which model will be the hot seller, but it forecasts total monthly units well. That is why planning is done in aggregate.</p>")
    t = rep(t, "<p>In industry, this activity is usually called S&amp;P planning rather than aggregate planning. The name describes what it does: it brings the sales side (how many units marketing expects customers to buy) together with the production side (how many units the firm can make). Neither side alone sets the plan, because a firm can sell only the lower of what customers want and what it is able to produce. The aim is to line the two up, and to do so at a low cost.</p>",
            "<p>The industry name, S&amp;P planning, says what it does: it lines up the sales side (what customers will buy) with the production side (what the firm can make), at a low cost, since a firm can sell only the lower of the two.</p>")
    t = rep(t, " An aggregate plan for an automobile manufacturer might specify how many automobiles to make overall. Likewise, a candy manufacturer might plan in pounds of candy and a potato chip maker in total chips, without regard to flavors or package sizes. An automaker with separate plants might go only as far as splitting SUVs from sedans.",
            " A candy maker might plan in pounds of candy, regardless of flavor.")
    t = rep(t, "<p>These inputs build on one another. What customers want and what the firm is capable of producing determine which products it offers. The process chosen to make those products (e.g., an automated line versus manual labor) determines capacity, such as 20 skateboard decks or 96 sandwiches per hour at each facility. Marketing then forecasts how much customers will want. When the two do not line up (say customers want 5,000 units in the first quarter and the firm can make only 2,000), planners look for other sources of supply, such as subcontracting or producing early and stockpiling. Apple, for example, often has new phones packaged a couple of weeks before a launch to absorb the initial spike in demand. Planners must also confirm that raw materials and a large enough workforce will be in place, because any one of these inputs could become the bottleneck.</p>",
            "<p>These inputs build on one another: the products and process set capacity, marketing forecasts demand, and where the two do not line up, planners look to subcontracting or producing early and stockpiling (Apple packages new phones weeks before launch). Materials and workforce must also be in place, since any input can become the bottleneck.</p>")
    t = rep(t, "<p>The resulting aggregate plan works like a budget authorization. It tells plant and line managers how much to produce in the period and which resources they are approved to use, such as regular-time production with no overtime, roughly 20% overtime paid at time and a half, or hiring ahead of a need expected in a later period.</p>",
            "<p>The aggregate plan works like a budget authorization: it tells managers how much to produce and which resources (overtime, hiring) they may use.</p>")
    t = rep(t, " Most other topics in this course sit at one of two extremes: either strategic decisions (e.g., approving a budget to expand a plant's capacity by 20% and leaving the details to engineers) or short-term operational details (e.g., how many seconds it takes to drill a skateboard deck). Aggregate planning is the course's main example of planning in the middle, where directors and a vice president of operations plan several months to a year ahead.",
            " It is the course's main example of planning in the middle, between strategic decisions and short-term operational details.")
    t = rep(t, " For example, a maker of vitamins or powdered supplements might produce a full year's supply in a two-week run and use the freed-up time to make other products.", "")
    t = rep(t, " A large employer that loses about 1% of its people each month to resignations and retirements can trim its workforce by around 4% simply by freezing hiring and not replacing those who leave.",
            " A hiring freeze shrinks the workforce through attrition alone.")
    t = rep(t, " Many clothing brands have their designs sewn to specification by outside shops, and Apple subcontracts the manufacturing of its phones. The brand still stands behind the quality, which requires close relationships with the suppliers.",
            " Apple, for example, subcontracts the manufacturing of its phones.")
    t = rep(t, " At lunchtime, Subway cannot make sandwiches fast enough, and customers with a short lunch break leave when the line is long. A discount of about a dollar for buying before 10 a.m. moves some of those customers to a slow period, so the store sells more sandwiches overall. Similarly, Disney sells discounted passes to Florida residents with blackout dates on its most popular days.",
            " That moved customers out of the lunch rush, when people left long lines. Disney's discounted Florida-resident passes have blackout dates on its busiest days.")
    t = rep(t, " Toothpaste shows the opposite case. If a shopper's usual brand is out of stock, the shopper buys another brand that day. For the company, the best outcome is one lost sale, and the worst is that the shopper prefers the competitor's product and never returns. Because holding costs for such items are low and the penalty for running out is high, firms deliberately overstock them. Back-ordering makes sense only when customers do not penalize the firm for making them wait.",
            " Toothpaste is the opposite case: a shopper whose brand is out buys another, so firms overstock such cheap-to-hold items. Back-ordering makes sense only when customers do not penalize the firm for waiting.")
    t = rep(t, "<p>No single option above is likely to be optimal by itself, in part because company policies limit how far each one can be pushed. For example, the stockroom may hold only 200 units, the firm may be unwilling to lay anyone off and so can shrink only through attrition, and hiring and firing are both expensive. Planners therefore piece several options together, looking for a plan that complies with all company policies and produces at a low cost.</p>",
            "<p>No single option is likely to be optimal, partly because company policies (stockroom space, no layoffs) limit each one, so planners combine several into a low-cost plan that follows every policy.</p>")
    t = rep(t, " While this strategy is cheaper, there may be other considerations. For example, the subcontractor might turn out to be a competitor later or lead to brand image problems.",
            " It is cheaper, though the subcontractor could later become a competitor.")
    t = rep(t, " (For example, none of these plans involved the use of overtime labor.) Moreover, firms should think about the nonmonetary costs of certain plans. For example, laying workers off takes a psychological toll on the remaining workers.",
            " Firms should also weigh nonmonetary costs, such as the toll layoffs take on the remaining workers.")
    return t


# ------------------------------------------------------------------ Concise
def table(head, rows):
    h = "".join(f"<th>{c}</th>" for c in head)
    r = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>\n" for row in rows)
    return f"<table>\n<thead><tr>{h}</tr></thead>\n<tbody>\n{r}</tbody>\n</table>"


def concise_body(mode):
    how = ("Step through it to see the table built and filled one source at a time."
           if mode == "stepper" else "Work through its tabs: how each cost is built, then how each month is filled.")
    terms = T.cost_terms()
    return f"""
<h1>The Nature of Aggregate Planning</h1>

<ul>
<li><strong>Aggregate planning</strong> (in industry, <b>sales and production (S&amp;P) planning</b>): planning intermediate-term production in aggregate units (how many cars, not how many blue sedans), because totals forecast better than individual items.</li>
<li><b>Goal</b>: meet forecast demand at minimum cost over the planning period by adjusting production rates, labor, inventory, overtime, and subcontracting.</li>
<li><b>Requirements</b>: a logical aggregate unit; an aggregate demand forecast; a way to determine costs; a model combining forecasts and costs.</li>
<li>The plan feeds the master production schedule and MRP, which break it down by product.</li>
</ul>

{table(["Horizon", "Who plans", "Examples"], [
    ["Long range (over 1 year)", "Top executives", "R&amp;D, new products, capital investment, facility location"],
    ["<b>Intermediate (3–18 months)</b>", "Operations managers", "Sales and production planning, employment, inventory, subcontracting (<b>aggregate planning</b>)"],
    ["Short range (under 3 months)", "Managers, supervisors, foremen", "Job assignments, ordering, scheduling, overtime"]])}

<h1>Aggregate Planning Strategies</h1>

<h3>Capacity Options (Supply Side)</h3>

{table(["Option", "Drawbacks"], [
    ["<b>Change inventory levels</b>: build stock in slow periods", "Holding costs; shortages if demand runs high; not possible for services"],
    ["<b>Hire or lay off</b>: match workforce to demand", "Hiring, training, and separation costs; lower productivity and morale"],
    ["<b>Overtime or idle time</b>: vary hours of a constant workforce", "Overtime premiums and fatigue; idle time to absorb; only small changes"],
    ["<b>Subcontract</b>", "Cost; quality and delivery risk; exposes customers to a competitor"],
    ["<b>Part-time workers</b>", "Best for low-skilled labor; poor fit for skilled work"]])}

<h3>Demand Options</h3>

{table(["Option", "Drawbacks"], [
    ["<b>Influence demand</b>: promotions and off-peak discounts", "Uncertain response; may not balance demand and capacity"],
    ["<b>Back-order</b> in high-demand periods", "Customers wait; goodwill and sales lost; works only with few substitutes"],
    ["<b>Counter-seasonal mix</b> (jet-ski engines in summer, snowmobile engines in winter)", "May take the firm outside its expertise"]])}

<h1>Methods of Aggregate Planning</h1>

<ul>
<li><strong>Chase strategy</strong>: match output to each period's demand (common, often the only option, in services).</li>
<li><strong>Level strategy</strong>: uniform daily production, with inventory or idle time as the buffer.</li>
<li><strong>Mixed strategy</strong>: a combination, usually best; finding it takes trial and error.</li>
<li><strong>Graphical methods</strong>: trial-and-error comparisons of demand with capacity; easy, but not optimal.</li>
</ul>

<div class="exam-tip">
<h4>EXAM TIP: Work Many Practice Problems</h4>
<p>The routine problems hide small rules (inventory carried in, charging for a workforce change at the start). The exam has no wrinkle that is not also in the practice questions.</p>
</div>

<h3>Example: Roofing Shingles</h3>

{table(["Month", "Demand", "Production days", "Demand per day"],
       [[m, f"{d:,}", n, r] for m, d, n, r in zip(["Jan", "Feb", "Mar", "Apr", "May", "Jun"], DEM, DAYS, [41, 39, 38, 57, 68, 55])] + [["<b>Total</b>", "<b>6,200</b>", "<b>124</b>", ""]])}

<p>Costs: carrying $5 per unit per month; subcontracting $20 per unit; labor $80 per day per worker (1.6 labor-hours per unit); raising the daily rate $300 per unit; lowering it $600 per unit.</p>

{table(["Method", "Working", "Total cost"], [
    ["1. Pure level (average, 6,200 ÷ 124 = 50 per day)", "Ending inventory 1,850 × $5 = $9,250; 10 workers × $80 × 124 days = $99,200", "$108,450"],
    ["2. Level at the minimum (38 per day) + subcontracting", "7.6 workers × $80 × 124 = $75,392; 6,200 − 4,712 = 1,488 subcontracted × $20 = $29,760", "<b>$105,152</b> (lowest)"],
    ["3. Pure chase (hiring and layoffs)", "Production $99,200 + hiring $9,000 + layoffs $9,600", "$117,800"]])}

<h2>Transportation Method of Linear Programming</h2>

<p>An optimizing method: supply (by period and source) in the rows, demand periods in the columns, and the unit cost in each cell. A tire maker has regular time at $40, overtime at $50, and subcontracting at $70 per tire; 100 tires in beginning inventory; $2 per tire per month carrying cost; and no back-ordering.</p>

{table(["", "March", "April", "May"], [["<b>Demand</b>", "800", "1,000", "750"], ["Regular capacity", "700", "700", "700"],
                                       ["Overtime", "50", "50", "50"], ["Subcontracting", "150", "150", "130"]])}

<ul>
<li>Capacity 2,680 + 100 inventory exceeds demand of 2,550, so a <b>dummy column</b> takes the 230 unused units at $0.</li>
<li>Each cell costs the source's price plus $2 for every month held; cells that would need back-ordering are blocked.</li>
<li>Fill each month's demand from the cheapest source with units left, earlier months' production included. {how}</li>
</ul>

{T.widget(mode)}

<ul>
<li><b>The plan</b>: March: 100 from inventory + 700 regular. April: 700 regular, 50 overtime, 150 subcontracted in April, plus 50 overtime and 50 subcontracted in March and held a month. May: 700 regular + 50 overtime.</li>
<li><b>Total cost</b> = {" + ".join(f"{q:,}({u})" for q, u in terms)} = <b>{T.money(T.TOTAL_COST)}</b>.</li>
<li>The method gives a starting plan; the stepping-stone method or Excel's Solver can confirm or improve it.</li>
</ul>

<div class="exam-tip">
<h4>EXAM TIP: Reading Aggregate Production Plans</h4>
<p>A question about the <em>period of production</em> (made, ordered, delivered) reads a <b>row</b>; one about the <em>period of demand</em> (sold, used to meet demand) reads a <b>column</b>. April demand met by subcontracting: 50 + 150 = 200 (April column). March overtime paid for: 50 (March overtime row).</p>
</div>

<h2>Other Methods</h2>

<ul>
<li><strong>Management coefficients model</strong>: a regression on managers' past decisions; objective and consistent, but assumes past trends continue and past decisions were good.</li>
<li>Services: controlling labor cost is critical, and an on-call labor resource covers unexpected demand.</li>
</ul>

{table(["Method", "Strength", "Weakness"], [
    ["Graphical", "Easy; handles policies and constraints", "Usually not optimal"],
    ["Transportation (linear programming)", "Finds the optimum", "Linear relationships only"],
    ["Management coefficients", "Objective, easy to use", "Only as good as the past data"]])}

<h2>Glossary</h2>

{table(["Term", "Definition"], [
    ["<b>Aggregate planning</b>", "Intermediate-term planning of total production to meet demand at minimum cost"],
    ["<b>Chase strategy</b>", "Matching output to each period's demand"],
    ["<b>Level strategy</b>", "Uniform production, buffered by inventory or idle time"],
    ["<b>Mixed strategy</b>", "A combination of capacity and demand options"],
    ["<b>Graphical methods</b>", "Trial-and-error comparison of demand with capacity"],
    ["<b>Transportation method</b>", "Linear-programming table of supply sources against demand periods"],
    ["<b>Dummy column</b>", "Column that absorbs unused capacity at zero cost"],
    ["<b>Management coefficients model</b>", "Regression model built on managers' past decisions"]])}

<h2>Key Takeaways</h2>

<ul>
<li>Aggregate planning covers 3 to 18 months, in aggregate units, at minimum cost.</li>
<li>Capacity options change supply; demand options shift or reshape demand.</li>
<li>In the shingle example, the level-at-minimum plan with subcontracting is cheapest at $105,152.</li>
<li>Transportation method: carrying cost grows with every month held; no back-ordering blocks later production meeting earlier demand; a dummy column balances supply and demand.</li>
<li>The tire plan costs $105,700.</li>
<li>Production period → row; demand period → column.</li>
</ul>
"""


def concise(src, mode):
    full = T.chapter(src, mode)
    head = full[:full.index("<body>") + len("<body>")]
    head = head.replace("</head>", T.CSS + "\n</head>", 1) if T.CSS not in head else head
    return head + "\n" + concise_body(mode) + "\n" + T.RUNTIME + "\n</body>\n</html>\n"


if __name__ == "__main__":
    src, out = sys.argv[1:3]; os.makedirs(out, exist_ok=True)
    for mode, tag in (("stepper", "OptionA-Stepper"), ("explorer", "OptionB-Explorer")):
        full = T.chapter(src, mode)
        for name, t in (("BALANCED", balanced(full)), ("CONCISE", concise(src, mode))):
            p = os.path.join(out, f"MAN4504-263-Exam3-AggregatePlanning-{name}-{tag}.html")
            open(p, "w", encoding="utf-8").write(t)
            print(f"wrote {os.path.basename(p)}: {words(t)} words ({words(t) / words(full):.0%} of Full's {words(full)})")
