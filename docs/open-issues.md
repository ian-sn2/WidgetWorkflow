# Open issues

Checkboxes. Keep `CLAUDE.md`'s status paragraph in sync with this file.

Cleared out on 2026-11-09: every item was checked against the engine (v2.69),
prompt v7 and the repo, and the ones already done moved to *Closed* at the
bottom with what closed them. The full wording of every closed item is in
this file's git history (`git log -p docs/open-issues.md`).

---

## Ian's calls

Nothing here can be settled from the repo.

- [ ] **Upload `Checking-fixed/sn25-v6.css` to S3 as `content/sn25-v6.css`.**
      It adds the phone rule that lets a wide prose table scroll inside its own
      box instead of pushing the page sideways. Until it is live, a chapter
      with a wide prose table scrolls the page on a phone: the AD-AS summary
      table by 99px at 390px and 169px at 320px, the AE consumption table by
      18px at 320px, four example chapters by a few pixels at 320px, and
      `ECO2023-263-SupplyAndDemand.html` by 61px at 390px. The phone check
      records these in `scripts/ci_phone_baseline.json`. It is the house
      sheet's 16px/20px cell padding on the chapters' own tables, not a widget.
- [ ] The 2026-10-12 review's priority 3–5 items (content, missing
      information, housekeeping) are on Ian's checklist,
      https://claude.ai/artifact/NWBQ4YoLGbnMKbdonVFDyF; some are ticked there.
- [ ] **Where do finished files get published?** An S3 path, the LMS, or
      somewhere else.
- [ ] **Is document 2 a different course from document 1?** `1 - ECO2013 …` is
      Dr. Knight's; `03-ECO2023-Fall26-Exam1-PPF.docx` is Dr. Rush's, with its
      own numbering and examples. The output is named
      `ECO2023-263-ThePPF.html` from the file name; if that is wrong the name
      changes before publication.
- [ ] **The PPF document contradicts itself about the freshman → senior
      shift.** One paragraph says study skills improved more, the next says
      socializing. The widget follows the drawing (socializing); recorded in
      `docs/changelogs/the-ppf-changelog.md`.
- [ ] **The ECO2023 chapter 7 figures disagree about the quota market** -- the
      prose and figure 06 say 30 / 100, figure 07 says 40 / 70 with a 30M
      quota, figure 08 says 50 / 100 with a 50M quota and leaves demand at its
      free-trade quantity. Each widget follows its own figure (Ian,
      2026-09-30). Worth correcting in the artwork.
- [ ] **Does the two-movement-arrow rule apply to an equilibrium-shift
      widget?** The prompt's final checklist says every surplus or shortage
      walkthrough ends with two movement arrows; its pattern table treats
      "equilibrium shift" as a different pattern with no `moves`. The checker
      reads the rule as surplus/shortage only. If that is wrong, the template
      gains `moves` and the 263 file has two widgets to fix.
- [ ] **Should the solutions start open?** They are shown in the open now;
      `<details open>` was the alternative.
- [ ] **Do published pages need `<div id="sticky-header">`?** The house script
      tracks the current heading only when one is present, and no house file
      carries it.
- [ ] **The 2026-10-07 arrow findings in the supply-and-demand examples.**
      `render_widgets.py` measures arrows centre to centre against 4px (about
      1.3px of visible gap), and never against axes or labels; edge to edge
      would surface three movement-arrow contacts in ECO2013 supply and demand.
      In ECO2023 supply and demand widget 8 the demand arrow crosses Point 1's
      guide at every usable price and the supply arrow sits 2.8px from S₂. A
      larger `dS`, or no supply arrow, would settle both. Changing the measure
      changes what passes, so it is Ian's.

## Files left as delivered (fix only when asked)

The standing rule (CLAUDE.md rule 9 and *Reviewing Ian's work*): files written
before a rule are reported, not rewritten. `scripts/ci_baseline.json` holds
their checker failures so CI blocks only new ones.

- [ ] **Caption length.** The examples carry captions over rule 9's cap from
      before it existed: International Trade 1, Allocative Efficiency 6,
      Elasticity 4, ECO2023 Supply and Demand 10, The PPF 11. The ones showing
      their working already get the 260-character cap.
- [ ] **`ECO2013-Widgets-All.html` (the 9/11 prototype)** fails the caption
      rules (eight "Before – / After –" prefixes, four "Price up, quantity up"),
      its apples widget puts six brace labels on curves (`below: true` fixes
      it), and it carries 24 ticks ahead of their step. Worth a pass only if it
      is ever published rather than kept as a reference.
- [ ] **Ticks ahead of their step** in
      `ECO2013-263-TradeoffsComparativeAdvantageTheMarketSystem.html`: 11, in
      widgets 1, 2 and 7. The fix is to drop each tick and let the point print
      its value at its own step.
- [ ] **Three label overlaps in `ECO2013-263-GovernmentIntervention.html`**
      (a `PS` on a supply curve and two `DWL`s), measurable since v2.44.

## Prompt (v7 → v8)

- [ ] **The final checklist still forbids "class".** Since 2026-11-09 a
      professor and what happened in class are fine (CLAUDE.md rule 4), but
      v7's last paragraph says no caption, label or paragraph mentions a
      "class". A v8 should drop it, so an unattended run does not reword notes
      Ian wants kept.
- [ ] **The head order.** v7 step 0 lists the two preconnects and the font link
      before `sn25-v6.css`; the house files put the stylesheet first, then the
      three font links on one line (Ian's block, 2026-09-17). `check_file.py`
      warns on the old order rather than failing it.
- [ ] **Exam tip titles.** Ian's convention is a short topic phrase
      ("Opportunity Costs Calculation") and the block goes *after* the
      paragraph it comments on. v7 says "EXAM TIP: Short title", placed where
      it sits in the PDF.
- [ ] **No PPF pattern or template.** Steps 3–5 are supply and demand only, so
      every PPF config is hand-built from the engine reference. A PPF row, a
      worked template, and the ruling below would fix it.
- [ ] **A curved frontier cannot reach an axis unless the intercepts are
      stated.** Extending a curve to invented intercepts breaks rule 3; v7
      permits extending a straight line along itself and says nothing about
      curves.
- [ ] **Word input is named only for transcripts.** Notes supplied as a .docx
      are handled as mode (a). A v8 could say how to read a Word table, its
      MathType equations (`doc_formulas.py`) and its headings
      (`doc_headings.py`).
- [ ] **Figure mode is specified but not implemented.** A config with no
      `axes` still throws in v2.69 (`Cannot read properties of undefined
      (reading 'x')`, checked 2026-11-09). Process diagrams are `flow` widgets
      or static HTML now (CLAUDE.md, 2026-10-19/21), so the likelier fix is to
      cut figure mode from the prompt rather than build it.
- [ ] **v7 must keep forbidding questions** even though `CLAUDE.md` allows them
      here: it runs unattended in Cowork. A deliberate divergence, not a bug.

## Engine gaps

Each is a feature no figure has yet needed badly enough; the workaround is
in brackets.

- [ ] **A cost table cannot link to its plot.** The schedule shape takes
      `[price, q1, q2…]`; a cost table (Q, AVC, ATC, MC per row) is the other
      way round. `byq: true` or a transposed `rows` would do it (2026-10-12).
      [A static table.]
- [ ] **Stacked panels.** The growth chapter stacks the labor market above the
      production function with one dashed line through both. [Two panels
      across, the output panel with `guides:"p"` and `showQ:false`.] Do not
      re-propose stacking two-panel widgets in general: built as v2.32 and
      reverted, far too tall.
- [ ] **Three or more panels.** [Scenario buttons, CLAUDE.md rule 10.]
- [ ] **A unit suffix on a tick** (120M, $35B, $19T). [Units in the axis
      title.]
- [ ] **A brace without drop guides.** [The slope triangle's legs as
      `thin`+`dashed` segments.]
- [ ] **A curve label at a chosen point.** Only the first or last point,
      nudged. [`lstart`, and `place_curve_labels.py` for the offset.]
- [ ] **A vertical shift arrow (`arrowQ`).** [A `moves` arrow between the two
      lines, CLAUDE.md.]
- [ ] **A `moves` arrow cannot stop short of its chord's end.** [Fake the `to`
      coordinate.]
- [ ] **No `vlines`.** [Guides; `divider: true` where a line separates
      regions.] Low priority.
- [ ] **A region bounded by a `curved` pair cannot be filled.** `areas` are
      straight-edged polygons. [Sample the curve into the polygon.]
- [ ] **Two-panel subscripts are 6.3px.** A two-panel widget renders at about
      half scale. The untried fix is the subscript itself (`.72em` at weight
      600 under a 700–800 parent); `docs/decisions-and-history.md`, 2026-09-29,
      has the measurements.

## Checks

- [ ] **`check_file.py` skips preset widgets**, because the engine computes
      their geometry, so only a render catches a preset defect (v2.7's brace
      was found that way). Expand the preset in the checker, or require the
      render pass for any file using one.
- [ ] **Arrow against guide** was tried and dropped: it fired ten times on
      correct work. Telling "crosses a guide" (fine) from "runs along one"
      (not) needs a parallelism test, not a distance test.
- [ ] **A solutions mode for `check_file.py`**: quiet the `images` and `dates`
      warnings, which every solutions page reports and none can act on.
      (`mobile_check.py` opens every question itself since 2026-11-09;
      `render_widgets.py` does not yet.)
- [ ] **Equations push three example chapters sideways on a phone** once
      MathJax has typeset them (Government Intervention, Tradeoffs, ECO2023
      Elasticity), and at 320px the Tradeoffs page zooms out far enough that
      its step buttons cannot be pressed. Found by the first CI run of the
      phone check, 2026-11-09; this container never loads MathJax, so no
      earlier check saw it. The house stylesheet's call, like the wide prose
      tables: `mjx-container[display="true"] { overflow-x: auto }` in
      `sn25-v6.css` would fix every chapter at once.

## Environment

- [ ] **LibreOffice here has no Writer module**, so `soffice` fails on every
      Word file. `antiword`/`catdoc` read `.doc`; `.docx` is parsed directly.
- [ ] The rest of `eco-widgets.zip` never arrived (the 30 reference PNGs,
      `ECO2013-Sample.html`, the GEB3373 precedent, the earlier changelogs).
      What matters is here.

## Exam solutions

- [ ] Topic tags on the four earlier Exam 1 papers are from the keyword pass
      and not yet read through; Fall 2024's and all of Exam 3's are by hand.
- [ ] Exam 2, and ECO2013's exams. The shell needs nothing new for them.

---

## Closed

What closed each, newest first. Full text in git history.

- **Exam 3 detailed solutions** -- built 2026-11-05 (117 questions, 78 widgets).
- **The solutions generators** live in `solutions/build/` now, not scratch
  space; Exam 3 reused them.
- **The named-person check and its gaps** -- removed 2026-11-09 (CLAUDE.md
  rule 4): a professor, named or not, is fine.
- **`render_widgets.py` needs Playwright** -- in CLAUDE.md's opening paragraph.
- **A `flow` widget for process diagrams** -- v2.57/v2.58, with cycles, two-way
  links (2026-10-19) and vertical chains (v2.60–v2.62). The open-market
  figures are `flow` widgets.
- **A price axis that does not start at 0** -- `axes.ymin`/`axes.xmin`, v2.63.
- **Point labels are one line** -- `\n` wraps a point's label since v2.34.
- **No area fill / the attainable region / the total-revenue rectangle** --
  `areas`, v2.11, outlined with `edge` since v2.18.
- **No automatic collision detection** -- by design: `check_file.py`,
  `place_labels.py` and `place_curve_labels.py` do it, and v2.69 cuts guides
  round labels.
- **`content/sn25-v6.js` returns 403 / the written-in contents / the TOC in
  the prompt** -- the head uses the live `studyguide/sn25-v2.js` (2026-09-21),
  no example carries a written-in TOC, `check_file.py` fails the pair, and v7
  step 0 says all of it.
- **Reorder the head of `ECO2013-263-SupplyAndDemand.html`** -- redone at Ian's
  ask, 2026-10-05.
- **Two shipped examples with arrows over guides** (ECO2013 supply and
  demand) -- redone 2026-10-05; `render_widgets.py` reports none.
- **A payoff matrix / a repeated-game years table** -- v2.39/v2.40 and v2.48.
- **Heading levels, `antiword` dropping text boxes, a semester swap, the brace
  curl, the shift arrow on a spline, row-arrow thresholds, the preset gap
  brace, the schedule-shift's fourth arrow, PPF axis titles, vertical braces,
  the checker's own tests, arrows against curves** -- all closed before
  2026-10-12; see git history.
- **The schedule table's first column is the y-axis good** -- documented,
  not a defect (renaming would break every config).
