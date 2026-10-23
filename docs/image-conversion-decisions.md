# Deciding what an image becomes

How a source image is classified and what it turns into, step by step. This
is the procedure used on the UCF sets (ECO, FIN3403, QMB3200, MAR3203) and,
with the house-format rules on top, on the UF files. Written 2026-10-23 so
it can be set beside another conversion process and compared.

## 0. Before deciding anything, gather four things

1. **The image itself.** Fetch it from S3 and look at it. The alt text and
   the file name describe it badly as often as well, and a picture of a
   table is not a graph however its name reads.
2. **The prose on both sides of it.** The paragraph before says what the
   figure is for; the paragraph after often reads values off it. This
   decides whether numbers are available and what the figure must show.
3. **The `<!-- IMAGE POSITION -->` comment** above it, which says where the
   author meant it to sit. It stays in the output whatever happens.
4. **The Concise edition's text**, if there is one, to see whether that
   edition introduces the figure at all (step 6).

## 1. Classify the picture

Every image falls into one of these; the class decides the tool.

| What the picture is | Becomes | Tool |
|---|---|---|
| A plot: axes with curves, points, shaded areas, guides | an interactive figure | `sd-graph` widget (JSON) |
| A chart: bar, histogram, Pareto, control chart, scatter, line over time | an interactive figure | `sd-graph` (bars are rectangular `areas`) |
| A pie | a drawing | inline SVG |
| A chain of boxes with arrows, or a ring (cycle, PDCA, circular flow) | a `flow` widget | `sd-graph` `flow`, horizontal or vertical, `cycle` for a ring |
| A project network (activities, precedence, ES/EF/LS/LF, critical path) | a `network` widget | `sd-graph` `network` |
| A payoff matrix, a year-by-year game table | an interactive grid | `sd-graph` `matrix` / `years` |
| A flowchart, fishbone, decision tree, service blueprint, spoke diagram, Venn, number line, spectrum arrow, 2×2 grid | a static drawing | inline SVG placed through the map's `{"html": …}` entry |
| A picture of a table or spreadsheet (Excel output, z-table, process chart, check sheet) | the table itself | HTML table, same cells highlighted |
| A picture of a formula or a worked calculation | the calculation | HTML with the formula |
| A financial-calculator screenshot | a calculator | `hp10bii` widget |
| A photograph, logo, screenshot of software other than its data, published chart with its own source credit, population tree | stays a picture | `<img>` kept, with `<!-- KEEP: why -->` |

Two rules sit over the table:

* **Anything drawable is drawn** (Ian, 2026-10-16). A static chart is still
  converted, with a caption instead of steps; "widget" to the reader means
  interaction, but the drawing is wanted either way, because text scales,
  can be edited for a new semester and matches the page's font.
* **A figure that is not becoming a drawing stays exactly the image it
  is.** Not a table, not a list, not prose. The `<img>` tag, its classes
  and alt text carry over untouched, and the KEEP comment records why.

## 2. Check the engine can express it

The plot classes are only widgets if the engine's JSON schema can draw
them. The test is to try: curves through the source's points, areas for the
shading, `hlines` for control limits, braces for a gap, `axes.xmin`/`ymin`
for a clipped origin, `cross` for axes that meet inside the plot.

* If a feature is missing and the figure recurs (project networks did, in
  nine pictures of one chapter), it is an **engine feature request**: the
  engine grows (with a version bump, a reference entry and a re-embed into
  every example), never the notes file.
* If the figure is a one-off drawing with no data behind it, it is an
  **inline SVG** figure through the `html` entry.
* **Never** hand-written SVG or JavaScript inside a widget, and never a
  widget that is really bespoke code. The widget is JSON or it is not a
  widget.

## 3. Decide the interaction: static, steps, or scenarios

* **Static with a caption** when the printed picture is one state.
* **Steps** when the picture genuinely builds: a trendline arriving on its
  data, a predicted point landing on the line, the loss and profit wedges
  after the revenue line, the forward pass then the backward pass. Every
  step must change the drawing; a caption that advances while the picture
  holds still reads as a broken button, and the checker fails it.
* **Scenario buttons** when the source prints several pictures of one
  lesson: the four demand patterns, the four capacity strategies, the three
  rejection regions, the four scatterplots, the bullwhip levels. Those
  pictures become one widget and the others are folded into it (step 6).
* **Two panels** only for two *different* things side by side (the X-bar
  chart beside the R chart, AON beside AOA). The same market before and
  after a change is one panel with steps, because a widget can animate
  what paper has to print twice.

## 4. Find the numbers, in this order

User message, then the chapter's prose, then the figure's own labels, then
the transcript, then the image, then the alt text.

* Every coordinate, tick and caption number must come from one of those.
  Where the prose gives none, the figure is drawn **symbolically** (word
  axis titles, no ticks) rather than with invented values.
* A chart whose values exist only in the picture (a Pareto's bar heights, a
  scatter's points) is read off the image, and the changelog says so.
* A figure that contradicts itself is drawn on the prose's numbers and the
  changelog says why. A figure that is merely a different example from the
  prose keeps its own numbers: each widget follows its own figure.
* A reading that belongs to a later step comes from its point, not from a
  tick, so a stepped numeric figure usually has no ticks at all.

## 5. Draw the figure, not the paragraph

* Match the **figure**: a picture showing five ticks and three areas keeps
  all of them even where the text discusses one. Draw nothing the source
  does not draw; extra curves and extra dots are clutter.
* Copy the source's own words, capitalisation and subscripts for titles,
  panel headings and curve names.
* Colours: the house teal/orange/red/navy on UF files; the school's theme
  on another publisher's files (UCF gold, white and black, in shades),
  with red kept only where the source itself is red.
* Labels never touch a line, an axis or a curve's own name. Area and curve
  labels are placed by script against the checker's geometry, not by eye,
  and a label that cannot be placed is a drawing to change.
* Generate shapes (bells, cost families, tangencies, crossings) from
  formulas; never type coordinates a formula can produce.

## 6. Decide where it goes, edition by edition

* **Full and Balanced**: the widget replaces the image in place. When
  several images fold into one scenario widget, the widget takes the first
  image's place and the others are either kept as pictures with a KEEP
  comment or, if the author prefers, dropped (`{"drop": …}`) with the
  widget anchored after the passage that introduces all the cases.
* **Concise**: a widget only where the Concise's own text introduces the
  figure, anchored after that line, table row or exam tip. A figure the
  Concise never mentions gets nothing, not even a table of its numbers.
  Never two widgets back to back with no text between.
* An exam tip that belongs with the figure sits above the widget, not
  below it.
* On another publisher's files nothing else changes: not prose, not
  headings, not markup, not the title. The apply script proves the output
  differs from the source only in the widgets and the TOC script line.
  Anything wrong in the source goes on the checklist.

## 7. Verify before calling it converted

1. `check_file.py`: JSON, label collisions, caption length, steps that
   change nothing, ticks that pre-empt a step, source words in
   student-facing text.
2. `render_widgets.py`: a screenshot of every widget, scenario and step,
   reviewed by eye for what the geometry cannot see.
3. `mobile_check.py` at 390px and 320px: nothing scrolls sideways, every
   button is tappable, the plot and its buttons fit on one screen.
4. A rebuilt file is diffed against the source by the apply script every
   time; a stray change refuses to write.

## 8. Record the decision

Every image gets one line in the chapter's changelog: what it was, what it
became, and any judgement in it (numbers read off the image, cases folded,
a figure kept and why). The checklist for the set lists what is new and
what was found in the sources but not changed.

## Where the judgement calls are

Comparing this against another process, these are the points where two
careful people could decide differently:

* Whether a static chart is worth converting at all, or only interactive
  ones (here: everything drawable).
* Whether a diagram is drawn as a widget of the engine or as a one-off SVG
  (here: engine when the shape recurs, SVG when it is a one-off).
* Whether pictures of tables become tables (here: yes, always).
* Whether missing numbers are read off the image or the figure goes
  symbolic (here: read off the image for a chart whose point is its data,
  symbolic for a conceptual graph).
* Whether several pictures of one lesson become one widget (here: yes).
* Whether the output may touch anything but the figures (here: on another
  publisher's file, no).
* Whether a figure carries a title and a caption of its own (here: yes,
  with a 200-character cap on the caption; the frameless look under
  discussion would drop both).
