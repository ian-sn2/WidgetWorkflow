ECO2023-263-Exam1-DetailedSolutions-Full.html

Built 2026-10-26 from the zip Ian sent: five Exam 1 papers (Fall 2024, Fall
2023, Summer 2023, Spring 2023, Summer 2022), their answer keys, and the
written solutions in `ECO2023-263-Exam1-DetailedSolutions-Full.html`. The
written solutions are carried over as they were, every `<strong>`, `<em>` and
centred formula included; the question stems and choices come from the exam
papers; widgets were added to Fall 2024 only. See `docs/exam-solutions-brief.md`
for the page's shape.

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

## Widgets (Fall 2024, 16)

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

`check_file.py`: 0 FAIL, 8 WARN -- `$21` against `$19` and the brace near its
guides on the midpoint figure (the Elasticity chapter's own figure reports the
same), the 90 and 100 ticks on the frontier, two calcs lines the solution also
states, and the `images`/`dates` lines that do not apply to a solutions page.

Browser checks ran on a copy with the shell script removed and every
`<details>` open: `render_widgets.py` 16 widgets, 57 states, no engine errors,
no arrow problems; `mobile_check.py` 0 problems at 390px and at 320 × 568; the
shell's exam, semester and topic buttons and its hash links were driven in
Chromium with no page errors.
