ECO2023-263-Exam1-DetailedSolutions-Full.html

Built 2026-10-26 from the zip Ian sent: five Exam 1 papers (Fall 2024, Fall
2023, Summer 2023, Spring 2023, Summer 2022), their answer keys, and the
written solutions in `ECO2023-263-Exam1-DetailedSolutions-Full.html`. The
written solutions are carried over as they were, every `<strong>`, `<em>` and
centred formula included; the question stems and choices come from the exam
papers. Fall 2024 got its widgets on the first pass and the other four papers
on the second (same day, at Ian's ask), 120 widgets in all. See
`docs/exam-solutions-brief.md` for the page's shape.

## What is in it

170 questions under five semesters, each with its stem, its choices, and its
written solution behind a "Solution" click. The shell filters by exam (one so
far), semester and topic.

| semester | questions kept | dropped |
| --- | --- | --- |
| Fall 2024 | 1–30 | — |
| Fall 2023 | 1–40 | — |
| Summer 2023 | 1–30 | 31, a three-part written question with no key and no solution |
| Spring 2023 | 1–40 | 41, the extra-credit confidence question |
| Summer 2022 | 1–30 | 31, the same three-part written question |

Solution letters were checked against the keys for form A: Fall 2024 and
Spring 2023 match the key files, Summer 2022 and Summer 2023 match the marked
answers in the "Answers" papers. **Fall 2023 has no key in the zip** -- the
"Answers (1)" paper marks only question 11 -- so its letters are the written
solutions' own. Spring 2023 question 10 is "(a, d)" in the solutions and
"A or D" in the key.

## Widgets

| semester | widgets |
| --- | --- |
| Fall 2024 | 16 |
| Fall 2023 | 30 |
| Summer 2023 | 21 |
| Spring 2023 | 27 |
| Summer 2022 | 26 |

### Fall 2024 (16)

| Q | where | what |
| --- | --- | --- |
| 2 | solution | midpoint elasticity: A (46, $21), B (54, $19); braces and the three lines of working arrive with their steps; 1.60 |
| 3, 11, 16, 18, 19, 21, 27 | solution | single-shift presets with four captions written for the question |
| 5 | solution | two panels: gasoline demand left, then diesel supply left, five steps |
| 7, 25 | solution | `double` + `compare`: the two panels that make "cannot be determined" visible; `big: 30, small: 12, arrowD: 12` because the preset's arrow crossed the new guides |
| 9 | solution | total revenue test on the solution's own $10 → $8, 100 → 110 example; the two revenue rectangles |
| 13 | solution | the table's five points as a bowed frontier, B to C, 2 cans per bar |
| 14 | solution | a horizontal demand curve at P₁, static |
| 17 | solution | PPF₁ to PPF₂ outward |
| 24 | question | the exam's four-panel figure as one widget with a button per figure; captions describe, they do not answer |

Not drawn, on purpose: 4 (one multiplication), 26 ($19 is the answer),
and the concept questions (1, 6, 8, 10, 12, 15, 20, 22, 23, 28, 29). 15 and 28
could take a deadweight-loss figure later.

### The other four papers (104)

The shapes are generators in the build (`widgets_lib.py`), one per lesson,
so a question is one line naming the shape and its captions. Symbolic
figures carry no numbers; the numeric ones assert the exam's arithmetic.

| shape | what it draws | used on |
| --- | --- | --- |
| single shift | the `shift` preset with four captions written for the question | every "the price of X rises and the quantity..." question: F23 3, 7, 12, 19, 23, 25, 34, 35, 37 · Su23 8, 13, 21, 25 · Sp23 3, 7, 12, 22, 23, 26, 37 · Su22 5, 8, 13, 14, 16, 21, 22, 25 |
| both shift | `double` + `compare` (two panels) where the answer is "cannot be determined"; one panel with the larger shift sized where the question says which is larger | F23 16, 29, 32 · Su23 11, 15 · Sp23 5, 14, 19, 32 · Su22 11 |
| four figures | the exam's four-panel figure as one widget, a button per figure, in the question | F23 26 · Su23 23 · Sp23 24 · Su22 23 |
| two markets | complements in production: a demand shift or a price rise in one market, then a supply shift in the other, five steps | Su23 4 · Sp23 9 · Su22 24 |
| midpoint | the two readings, both braces, three lines of working | F23 6 · Sp23 6 · Su23 18 · Su22 18 |
| frontier | a table's points on a bowed frontier, or the two stated points on a segment, with the move and both braces | Sp23 38 · Su23 26 · Su22 26 |
| frontier concepts | outward shift; points on, inside and beyond; rising opportunity cost on a bowed frontier | Su23 19, 27 · Sp23 15, 29 · Su22 7 |
| surplus areas | one curve shifts and CS, PS or total surplus is shaded before and after | F23 9 · Su23 1 · Sp23 34 · Su22 6 |
| price ceiling | the two readings, the shortage, the deadweight triangle; a variant where demand then rises; four rent ceilings as buttons | F23 14, 22 · Su23 16 · Sp23 25 · Su22 9 |
| minimum wage | a floor in the labor market with the unemployment brace | F23 17 |
| tax | supply shifts up by the tax, the wedge between Pᵇ and Pˢ, the deadweight triangle; with steep and flat demand as buttons where the question is who pays or how much quantity falls | F23 2, 13 · Su23 29 · Sp23 13, 18, 36 · Su22 15, 17 |
| subsidy | supply shifts down by the subsidy, the wedge the other way | Sp23 17 |
| production quota | a cap below Q₁ with the price read off demand and the deadweight triangle; a cap above Q₁ that changes nothing | F23 4 · Sp23 4 · Su22 27 |
| trade | world price below or above P₁, CS and PS before and after, the imports or exports brace | F23 27, 39 · Su23 20 · Su22 1 (both cases as buttons) |
| tariff / import quota | the domestic price lifted above the world price, the smaller imports, the revenue band (or importers' profit) and the two red triangles | F23 31, 33 · Su23 24 · Sp23 31, 39 · Su22 10, 20 |
| efficient quantity | MSB against MSC, with MSC shifting (F23 5) or the two stated readings at one quantity (F23 36) | F23 5, 20-style concept, 36 · Su23 17 · Su22 12 |
| elasticity concepts | the total revenue hump; elasticity along a straight line; a vertical or horizontal demand curve; steep against flat demand under the same supply shift | F23 21, 30 · Su23 2, 7 · Sp23 27 · Su22 2, 4, 29 |
| movement along | a price change as a move along the demand curve | F23 28 · Su23 9 |

Not drawn, on purpose: the definition and arithmetic questions (income and
cross elasticity, "a pure number", the proportion of income, who bears a tax
in words, comparative advantage, the "(i) and (ii)" statement questions) and
Spring 2023 question 28, whose two readings put the efficient quantity at
zero when drawn as straight lines, which would mislead.

Three decisions in the drawings: a tariff's revenue band is named just
below the band rather than inside it (the band is 12 units tall and its
corners are marked); the tax and subsidy wedges fade the shifted supply
curve on the step the brace is read (`dimAt`), the chapter rule for a label
that has nowhere else to go; and the "both shift" panels use a 30-unit
larger shift and a 12-unit smaller one with the demand arrow at p = 12,
because the preset's own arrow crossed the new equilibrium's guides.

## Topics as assigned

Fall 2024 -- PPF: 1, 13, 17, 29 · Elasticity: 2, 4, 8, 9, 14, 22, 23 ·
Supply and Demand: 3, 5, 7, 11, 16, 18, 19, 21, 24, 25, 27 · Efficiency and
Equity: 6, 15, 20, 26, 28 · Government Intervention: 10, 12 · Free Point: 30.
(10 is "increasing opportunity cost", keyed on "taxes" in its choices, and 12
is the fairness question keyed on "income tax"; both read better as PPF and
Efficiency and Equity -- Ian's call, and a one-attribute edit.)

The other four exams are tagged by the same keyword pass and not yet read
through; the counts are in the build log and the tags are on each section.

## Decisions to review

* **The choices are a quiz** (Ian, 2026-10-26): click one and it turns green
  or red, the right one shows green, and the solution stays behind its own
  click. Spring 2023 question 10 accepts (a) or (d), as the key does.
* **The picker is one collapsible box** in the style of the table of
  contents, with three stages inside: Semester, then Exam, then Topic.
* **Solutions are set tighter than a chapter**: half the house margins, and
  figures at 440px inside a solution.

* **Solutions start closed.** `open` on every `<details class="sol-answer">`
  shows them all.
* **Title** is "ECO2023 Exam 1 Detailed Solutions"; the file Ian sent was
  titled "ECO2023 Summer 2023 Exam 1 Solutions", which named one of its five
  exams.
* **The professor's name** is on every exam paper's cover and in the Fall
  2023 solution for question 14 (the Taylor Swift question names him in the
  stem). Both are left as the source has them; neither is in a caption.
* Fall 2024 question 24 keeps no `<img>`: the widget is the figure. The other
  four exams' four-panel figure questions (Fall 2023 26, Summer 2023 23, Spring
  2023 24, Summer 2022 23) carry a `<!-- FIGURE: … -->` comment where the
  image was and will take the same widget.
* Spring 2023 question 38's table and Fall 2024 question 13's are HTML tables
  in a scrolling box, because the house stylesheet's full-width, 16px-padded
  table ran 32px past a 320px screen.

## Checks

`check_file.py`: 0 FAIL, 110 WARN. The warnings are of four kinds: an area
label near a dashed guide (DWL, CS, PS and the tariff band, which sit beside
the guides that bound them); `P₁` crowded against `Pᵇ` or `Pˢ` on the tax
figures, where a small wedge is the lesson; the midpoint figures' price labels
and brace; and the `images`, `dates`, `calcs` and `prose` lines that do not
apply to a solutions page or are the written solution stating the same
arithmetic the widget shows.

Browser checks ran on a copy with the shell script removed and every
`<details>` open: `render_widgets.py` over all 120 widgets, `mobile_check.py`
at 390px and at 320 × 568, and the picker and quiz driven in Chromium; the
results are in the commit message of the push that carried them.
