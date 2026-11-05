ECO2023-261-Exam3-DetailedSolutions-Full.html

# ECO2023 Exam 3 detailed solutions — changelog

Built 2026-11-05 from `SentToClaude.zip`: four Final Exam papers with their
keys (Spring 2020, Fall 2020, Spring 2021, Summer 2021) and the written
solutions `ECO2023-261-Exam3-DS-Full.html`. Same page shape, shell and rules
as Exam 1 (`docs/exam-solutions-brief.md`).

## What is on the page

* **117 questions, 78 widgets.** Each paper's closing "answer A" point is
  dropped, as on Exam 1. Semesters run newest first.
* **13 topics.** The five Exam 1 topics that recur (The PPF, Supply and Demand,
  Elasticity, Government Intervention, International Trade) and eight Exam 3
  chapters in the textbook's order: Perfect Competition, Monopoly,
  Monopolistic Competition, Oligopoly, Externalities, Public Goods and Common
  Resources, Labor Markets, Inequality. Topics are assigned by hand in
  `solutions/build/paraphrase3.py`, not by keyword: the chapters share
  vocabulary, and a keyword rule filed monopoly questions under costs.
  Efficiency and Equity has no Exam 3 question, so it shows no card.
* **Every question is paraphrased**, numbers, choice counts and choice order
  kept, as on Exam 1. Every solution letter matches its answer key.

## Widgets

* **New shapes**, in `solutions/build/widgets_lib3.py`: the competitive firm
  (MC, ATC, AVC, the price line, profit or loss), the market beside one firm
  (demand rising, entry, exit), monopoly against competition with the
  deadweight loss, natural-monopoly regulation with unregulated, marginal-cost
  and average-cost buttons, monopolistic competition in the long run and after
  entry, the payoff game, labor-market shifts on wage and labor axes, the
  backward-bending labor supply curve, high- against low-skilled labor supply,
  Lorenz curves, external cost and external benefit, and a rent ceiling's
  effect on producer surplus.
* **Exact where it matters.** In the monopoly and monopolistic-competition
  figures MC is the derivative of total cost, so MR = MC at the marked output
  and the long-run demand curve touches ATC exactly there. Both are asserted.
  The competitive-firm figures use `curve_shapes.cost_family`.
* **Payoff games replace both the paper's table and the solution's
  pictures.** Each of the eight game questions had the grid as a table in the
  question and again as five images in the solution, one per step of the
  written argument. One stepped payoff-matrix widget now sits in the question
  where the table was, opening on the same grid, and the five images go. Its
  captions are computed from the payoffs, and the dominant strategies it
  finds are asserted against the solution's letter. The grid heads its rows
  and columns "Cut prices / Don't cut" or "Low prices / High prices", because
  the papers' longer phrases ran together in the cell headings.
* **The three four-panel figures** (Fall 2020 Q3, Spring 2020 Q3, Spring 2021
  Q25) are the Exam 1 "Figure A–D" widget in place of the image.
* **Numbers from the question only.** Jane's Garage (Spring 2020 Q17) is
  drawn on cost curves solved so that MC is $35 and ATC is $40 at 40 garages.
  The minimum-wage figure (Spring 2020 Q27) is labelled $13.25 and $15.00.
  Everything else is symbolic.

## Decisions to review

* **File name.** The page follows Exam 1's pattern,
  `ECO2023-261-Exam3-DetailedSolutions-Full.html`, rather than the
  `-DS-Full` of the file supplied.
* **Exam number.** The papers are headed "Final Exam" and the solutions
  "Midterm 3". The page calls it Exam 3.
* **Topic order.** Exam 3's chapters follow the Exam 1 topics, in the
  textbook's chapter order.
* **Short answer.** Summer 2021 Q1 has no choices. It is shown with its three
  parts and the solution's three answers, under the Labor Markets topic.
* **`<u>` removed** from the game solutions' "Step 1:" labels, which are
  already bold. The house format never underlines.
* **One sentence of the solutions reworded, eight times.** Each game solution
  opened with "The payoff matrix we were given was as follows:" over a
  picture that is now gone. It reads "The payoff matrix is the one shown with
  the question."
* **Profit is shaded teal and a loss red.** No convention existed for either.

## Flagged for Ian, not changed

* **A named professor.** Spring 2020 Q14's solution says "Dr. Rush discussed
  the Coase theorem in terms of…". That attributes content to whoever taught
  it, and naming people is your call.
* **The answer key disagreement.** Summer 2021 Q11's solution carries an
  editor's note that the posted key gives (B) and the solution argues (D).
  The page marks (D), as the solution does. The key file supplied here also
  marks D.
* **Firm names** from the papers are kept where the solutions use them:
  Knight's dog-vacuuming service and medicinal wheat company, Thomas's
  restaurant and wheat, Bob's Lawn Care, Jane's Garage Cleaning, Billy Bob's
  BBQ. "Prof." is dropped from Knight in the paraphrase.

## Checks

* `check_file.py`: 0 FAIL. The warnings are listed in the session reply; most
  are shared Exam 1 shapes (tariff revenue, the PPF points, tax readings).

* **Labels nothing covers (engine v2.57, 2026-11-05).** Every dashed guide is cut out around each label inside the plot and carries on past it, every in-plot label has a halo in the plot colour, and curve and area names are drawn above the curves and points. This came from the review marks on the tax, rent-ceiling and trade figures.

* **Bookmarks in the menu (shell v0.39, 2026-11-05).** A bookmarked question puts a ribbon count on its semester card, on Full Exam and on its topic card, and the menu gains a Bookmarks row listing each one by semester, question number and topic. A click there opens the question in its semester's Full Exam.
