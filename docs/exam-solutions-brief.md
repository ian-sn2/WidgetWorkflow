# Exam solutions — project brief

Started 2026-10-26, on Ian's ask: a second kind of page beside the chapter
notes, carrying detailed solutions to past exam questions, with a live widget
wherever the reasoning is a graph, and toggles for the exam, the semester it
was set in, and the topic. Mostly for the ECO classes.

## What a solutions page is

One self-contained HTML file per course and exam, in `solutions/`, named the
way Ian's own output was: `ECO2023-263-Exam1-DetailedSolutions-Full.html`
(263 is the term it is published in, not the exams' terms). It carries the
house head, the engine, and the **solutions shell** -- `engine/exam-solutions.js`
and `.css`, embedded by `scripts/embed_engine.py` in place of
`<!--SOL-SHELL-->` the same way the engine fills `<!--SDG-ENGINE-->`.

The head carries MathJax (the same three lines Ian's own solutions file had),
because the written solutions set their formulas as `\[ … \]`. The CDN it
loads from is not reachable from this container, so the formulas cannot be
checked here; Ian's browser renders them.

The body is:

```html
<h1>ECO2023 Exam 1 Detailed Solutions</h1>
<p>…one line of instructions…</p>
<div class="sol-shell"></div>                      ← the shell builds the buttons here

<div class="sol-group" data-term="243" data-exam="1">
<h2>Exam 1 · Fall 2024</h2>                        ← the house script lists these in its TOC
<section class="sol" id="eco2023-243-e1-q13" data-term="243" data-exam="1" data-topic="The PPF">
<p class="sol-q"><b>Question 13 · The PPF</b></p>
<div class="sol-table"><table>…</table></div>      ← anything the exam printed above the question
<p>…the question…</p>
<ol class="sol-choices" type="A"><li>…</li><li class="sol-right">…</li>…</ol>
<div class="sol-answer"><p class="sol-answer-k">Solution</p>
<p><strong>(d)</strong> …the written solution…</p>
<div class="sdg"><script type="application/json">{…}</script></div>   ← the widget, where there is one
…
</div>
</section>
…
</div>
```

The shell reads `data-term`, `data-exam` and `data-topic` off the sections and
opens on a **menu**: a greeting and a panel of buttons, three rows of cards,
**Semester, then Exam, then Topic** (Ian, 2026-11-04: a home screen that goes
away once chosen, to save vertical space). Nothing is lit until it is
clicked: the exam row appears once a semester is chosen and the topic row
once an exam is. Each
card naming its choice and how many questions it holds, the chosen one
filled navy; a later row lists only what the earlier choices allow. Topics
run in Ian's order (The PPF first, then Supply and Demand, Elasticity,
Efficiency and Equity, Government Intervention, International Trade). Picking
a topic card opens the **questions view**: the menu is gone and a bar at the
top carries a "Back to menu" button, a status line naming the selection, and
a progress bar. A link with a selection in its hash opens on the questions.

Under the picker the shell shows **one question at a time** in its own box
(Ian, 2026-10-26: a self-contained box that needs no scrolling until a
solution is opened). Under the box sit Previous and Next with a strip of
question numbers between them: the current one filled navy, an answered one
green or red, a bookmarked one carrying a red ribbon. A bookmark button at the left of
the question's heading, boxed like a strip number, marks it, and the strip's
number then wears the ribbon draped over its top edge; bookmarks are kept in the browser's
localStorage, so they survive a reload on that device and nowhere else, and
the page works without it. The arrow keys step too. The page holds every
section and the shell hides all but the current one.

The selection lives in the URL hash (`#243/1/Elasticity/3`: term, exam,
topic, question position), so a link lands on one question. A hash that names
a question or a heading (`#eco2023-243-e1-q13`) selects that question's
semester and exam first. Terms are the usual codes (YY + 1 spring, 2 summer,
3 fall) and the shell names them.

**It is a list of worked solutions, not a practice exam** (Ian's manager,
2026-11-02). The question is shown for context with its right choice marked
green, and the solution sits under it in the open; nothing is clicked to
check an answer. The letter comes from the written solution's own "(c)".

**The questions are paraphrased.** Every stem and every choice is restated in
our own words (`solutions/paraphrase-eco2023-exam1.py`, which the build
reads), keeping each number, the
count of choices and their order, because the written solutions refer to
choices by letter and to the numbers by value. Nothing is copied from the
papers.

**Solutions are set tight.** The house sheet gives every paragraph and list
item 10px to 20px of margin at 1.6 line height, which made a worked answer
twice as tall as it needed to be; inside `.sol-answer` the shell's stylesheet
halves that. **A figure in a solution has no box of its own** (Ian,
2026-11-04): no border, no paper ground, a 400px plot by default, and three
controls at its top right: − and + step the plot through 300, 400, 520 and
660px (remembered in the browser, for every figure on the page), and
Fullscreen lifts the widget into an overlay at 760px with its step and
scenario state intact, closed by its button, Escape, a click outside, or
moving to another question.

## Where the widgets go

A widget lives in one of two places:

* **In the question**, in place of a figure the exam printed. Fall 2024's
  question 24 prints four panels and asks which one shows the change; the
  widget is a static `shift` preset with a scenario button per figure, and
  its captions describe each figure without answering the question.
* **In the solution**, under the answer letter, where the solution's
  reasoning is a graph: a shift, a two-market chain, a surplus area, a move
  along a frontier. The widget's steps walk the same argument the prose makes,
  and its captions say the arithmetic the student needs to redo it.

Everything a widget draws is the exam's or the written solution's own number.
The total-revenue widget draws the $10 → $8, 100 → 110 example because the
solution works that example; it would not draw one of its own.

The single-shift questions -- most of any Exam 1 -- are `shift` presets with
four steps written for the question (the preset's own captions end in
"Price up, quantity up", which rule 9 bans). A both-curves-shift question is
a `double` preset with `compare: true`, two panels differing only in which
shift is larger, which is the whole of why the answer is "cannot be
determined". The arrow height on those is set (`big: 30, small: 12, arrowD: 12`) because the
preset's own choice crossed the new equilibrium's guides on both.

## Topics

Each question carries one topic, assigned by a keyword pass over its stem and
choices and then read: The PPF, Supply and Demand, Elasticity, Efficiency and
Equity, Government Intervention, International Trade. The "answer A" question
every paper ends with is left out of the page (Ian, 2026-10-26). The
assignment is a judgement and is listed per exam in the changelog for Ian to
overrule.

## Checks

The same ones as a chapter. `check_file.py` runs on the page unchanged;
`images` and `dates` warn because a solutions page has neither, and the calcs
warnings are the written solution stating the same arithmetic the widget
shows -- which here is the point. **The browser scripts need the shell off:**
`render_widgets.py` and `mobile_check.py` press buttons, and the shell hides
every question but one. Make a copy with the shell `<script>` removed and run
them on that.

## Still to do

* The widget generators (`widgets_lib.py`: one function per lesson, from a
  single shift to a tariff) and the per-paper maps are in the session's
  scratch space beside the exam papers; the changelog lists every shape and
  the questions it is on. They belong in `scripts/` once a second exam shows
  which parts are general.
* Exams 2 and 3, and ECO2013. The shell needs nothing new for them: a new
  `sol-group` with its `data-exam`, and the Exam row grows a button.
* A `check_file.py` mode for a solutions page, so `images` and `dates` stay
  quiet and the step and label checks run on the opened copy.
