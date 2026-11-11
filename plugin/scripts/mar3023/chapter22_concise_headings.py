"""MAR3023 Fall '26 Chapter 22: give the Concise edition the Full's h1/h2 headings.

    python scripts/mar3023/chapter22_concise_headings.py FULL.html CONCISE.html OUT.html

Renames the four headings the Concise reworded, gives "Executing the Marketing Program" its own section again
(its two bullets had been folded into Planning vs. Implementation), and restores "Marketing Yourself: You, Inc."
as a short section. Nothing else in the file changes; the result must list exactly the Full's headings.
"""
import re, sys


def rep(t, old, new):
    assert t.count(old) == 1, (old[:80], t.count(old))
    return t.replace(old, new)


def headings(t):
    return re.findall(r"<h[12]>([^<]*)</h[12]>", t[t.index("<body>"):])


def fix(full, t):
    for old, new in (("Resource Allocation — Share Point Analysis", "Resource Allocation (Budgets)"),
                     ("Measuring Results", "Measuring Results and Identifying Deviations"),
                     ("Marketing Audit and ROI Tools", "The Marketing Audit"),
                     ("Corrective Action and Contingency Plans", "Taking Corrective Action (Contingency Plans)")):
        t = rep(t, f"<h2>{old}</h2>", f"<h2>{new}</h2>")
    # strategy vs. tactics back under their own heading, ahead of Planning vs. Implementation
    strat = "    <li><b>Marketing strategy</b>: how to achieve a goal (target market + marketing program)</li>\n"
    tact = "    <li><b>Marketing tactics</b>: day-to-day operational decisions executing the strategy</li>\n"
    t = rep(t, strat + tact, "")
    t = rep(t, "<h2>Planning vs. Implementation</h2>",
            "<h2>Executing the Marketing Program</h2>\n\n<ul>\n" + strat + tact
            + "    <li>Even the best plan fails without strong execution.</li>\n</ul>\n\n<h2>Planning vs. Implementation</h2>")
    you = """<h1>Marketing Yourself: You, Inc.</h1>

<p>The strategic marketing process applied to a job search, with each student as a brand (meant more for career decisions than for the exam):</p>

<ul>
    <li><b>Objectives</b>: money, experience, advancement, fulfillment, and work-life balance, then a personal mission statement</li>
    <li><b>Plan</b>: segmentation, targeting, and positioning; situation analysis; strategy; tactics; budget; timing; contingency plan</li>
</ul>

<table>
    <thead>
        <tr><th>Marketing mix</th><th>Applied to you</th></tr>
    </thead>
    <tbody>
        <tr><td><b>Product (you)</b></td><td>Assess strengths and weaknesses; fill gaps with skills or certifications; get an honest "audit" from a mentor; packaging (dress, grooming, demeanor)</td></tr>
        <tr><td><b>Promotion</b></td><td>Résumé and cover letters (advertising); LinkedIn (public relations); the interview (personal selling, with a thank-you follow-up)</td></tr>
        <tr><td><b>Place</b></td><td>Flexibility on location widens options</td></tr>
        <tr><td><b>Price</b></td><td>Know the going salary; adjust for what you bring</td></tr>
    </tbody>
</table>

<ul>
    <li><b>Personal branding</b>: the three C's: competencies, character, communication</li>
    <li>Largest sources of entry-level marketing jobs: sales and retailing; graduate options include a master's in marketing research, an MBA, and a specialized master's in marketing</li>
</ul>

"""
    t = rep(t, "<h2>Glossary</h2>", you + "<h2>Glossary</h2>")
    assert headings(t) == headings(full) + ["Glossary", "Key Takeaways"], headings(t)
    return t


if __name__ == "__main__":
    full, con, out = sys.argv[1:4]
    f = open(full, encoding="utf-8").read(); c = open(con, encoding="utf-8").read()
    open(out, "w", encoding="utf-8").write(fix(f, c)); print("wrote", out)
