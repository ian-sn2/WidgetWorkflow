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
<ol class="sol-choices" type="A"><li>…</li>…</ol>
<details class="sol-answer"><summary>Solution</summary>
<p><strong>(d)</strong> …the written solution…</p>
<div class="sdg"><script type="application/json">{…}</script></div>   ← the widget, where there is one
…
</details>
</section>
…
</div>
```

The shell reads `data-term`, `data-exam` and `data-topic` off the sections and
builds one collapsible box styled like the house table of contents -- a
`<details class="toc-box">` whose summary names the whole selection -- with
three stages inside it in order, **Semester, then Exam, then Topic**, each a
row of choices with the current one filled navy; a later stage lists only
what the earlier choices allow. It hides all but the current one, and keeps the selection in the URL hash
(`#243/1/Elasticity/3`: term, exam, topic, question position), so a link lands
on one question. A hash that
names a heading or a question (`#eco2023-243-e1-q13`, which is what the house
table of contents links to) selects that question's exam and semester first,
so a link to a hidden heading never scrolls to nothing. Terms are the usual
codes (YY + 1 spring, 2 summer, 3 fall) and the shell names them.

**The question is a quiz.** Each choice is clickable: the one picked turns
green or red, the right one is shown green, and a line under the list says
which letter is correct. The letter comes from `data-answer` on the section,
which the build reads off the written solution's own "(c)"; a question with
none stays plain text. **The solution is behind a click** after that: each
`<details>` starts closed. One attribute (`open`) reverses that for the whole
file; it is Ian's call.

**Solutions are set tight.** The house sheet gives every paragraph and list
item 10px to 20px of margin at 1.6 line height, which made a worked answer
twice as tall as it needed to be; inside `.sol-answer` the shell's stylesheet
halves that, and a figure there is 440px wide rather than 580.

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
shows -- which here is the point. **The browser scripts need the solutions
open and the shell off:** `render_widgets.py` and `mobile_check.py` press
buttons, a closed `<details>` hides them, and the shell hides every exam but
one. Make a copy with the shell `<script>` removed and `open` on every
`<details>` and run them on that (the changelog shows the three lines).

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
