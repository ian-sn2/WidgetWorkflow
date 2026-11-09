# Building the detailed-solutions pages

These scripts turn an exam folder (the papers and keys as Word files, plus the
written solutions HTML) into a page in `solutions/`. The widget shapes they
draw are the reusable part: a new paper on the same chapters needs its numbers
and a choice of shape per question, not new drawing code.

| File | What it holds |
|---|---|
| `widgets_lib.py` | Exam 1 shapes: shifts, both-curve shifts, surplus, ceilings, floors, taxes, subsidies, quotas, trade, tariffs, elasticity, PPF |
| `widgets_lib3.py` | Exam 3 shapes: the competitive firm, market beside firm, monopoly, natural-monopoly regulation, monopolistic competition, payoff games, labor markets, Lorenz curves, externalities |
| `widgets_f24.py`, `widgets_rest.py`, `widgets_ex3.py` | Which shape each question gets, with its captions |
| `paraphrase.py`, `paraphrase3.py` | Every question in our own words; Exam 3's file also holds the topic of each question |
| `build_solutions.py`, `build_exam3.py`, `exam3_parse.py` | Read the papers and solutions and assemble the page |

Every relationship a figure exists to show is an `assert` in the shape that
draws it: MR = MC at the monopoly output, demand tangent to ATC in the long
run, the payoff game's dominant strategies matching the solution's letter. A
build that would draw one wrong stops.

## Exam 3

The papers are converted with pandoc first, into `<upload>/exam-text/`:

```
for f in "<upload>/Final Exam/"*.docx; do pandoc "$f" -t html -o "<upload>/exam-text/$(basename "${f%.docx}").html"; done
```

Then, from the repository root:

```
OUT=solutions/ECO2023-261-Exam3-DetailedSolutions-Full.html
python3 -I solutions/build/build_exam3.py <upload> $OUT
python3 scripts/place_curve_labels.py $OUT --apply
python3 scripts/place_labels.py $OUT --apply
python3 scripts/embed_engine.py $OUT
python3 scripts/check_file.py $OUT
```

The two placers search for clear label positions against the checker's own
geometry and take a few minutes over 78 widgets.

## Exam 1

```
python3 -I solutions/build/build_solutions.py <upload> solutions/ECO2023-263-Exam1-DetailedSolutions-Full.html
python3 scripts/embed_engine.py solutions/ECO2023-263-Exam1-DetailedSolutions-Full.html
```
