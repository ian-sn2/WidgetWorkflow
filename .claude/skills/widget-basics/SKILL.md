---
name: widget-basics
description: Create an interactive widget for a notes page - what a widget is, writing its JSON config, steps and scenario buttons, titles and captions, where it goes in the page, embedding the engine and the noscript fallback. Use whenever a figure is being turned into a widget or a widget's structure (steps, buttons, captions) is being changed.
---

# Creating a widget

A widget is a `<div class="sdg">` holding a JSON config; `engine/sd-graph.js` (v2.68) draws it. **Write JSON, never hand-written SVG or JS** (CLAUDE.md hard rule 2). A figure the schema cannot express is an engine feature request in `docs/open-issues.md`, or, for Ian's own chapters where he has asked, a hand-built chart (`other-charts`).

## Steps
1. **Look at the source figure.** `curl` the `<img src>` (public on S3) and match the *figure*, not the paragraph beside it: keep everything it draws, and add nothing.
2. **Pick a shape** from `examples/ECO2013-Widgets-All.html`: schedule + curve, movement along vs. shift, schedule shift with per-row arrows, surplus/shortage, two markets, symbolic presets. Check the schema in `docs/engine-reference.md` (top level, steps, scenarios, panel, presets).
3. **Numbers come from the source only**: user message > notes prose > notes labels > transcript > image > alt text. With none stated, draw symbolically (`pl`/`ql`, 110 × 110, equilibrium at [50, 50]).
4. **Draw it** (`curves-and-labels`).
5. **Embed and check**: `python scripts/embed_engine.py FILE` (the engine is never typed by hand; the head carries `<!--SDG-ENGINE-->`), then `widget-qa`.

## Steps and scenarios
- `at`/`until` are step indexes; **step 0 is the opening state** and `until` is exclusive. **Every step must change the drawing**; a static figure takes a `caption` instead of `steps`.
- **Cases of one lesson share one widget with scenario buttons** (surplus + shortage, increase + decrease, the four shifts). One market before/after a change is one panel with steps; two different markets are two panels.
- A value arrives with its step, so a stepped numeric figure carries its readings on points, not `xticks`/`yticks`.

## Words
- Title and panel headings in **Title Case**; ledes, captions and steps in sentence case.
- Captions: 1–3 complete sentences, **≤ 200 characters** (260 when showing three or more numbers of working), saying something the surrounding prose does not. No "Before –/After –", no fragments.
- Never mention the source ("the slides", "in class") or instruct the reader ("hover over…").

## Placement
The widget replaces the `<img>` where it stood; keep any `<!-- IMAGE POSITION -->` comment. Map-driven placement for whole chapters: `scripts/apply_widgets.py` (`chapter-conversion`).

**Changing the engine itself** follows CLAUDE.md hard rule 1: bump the version comment, update `docs/engine-reference.md`, update `check_file.py`'s geometry copy in the same commit, and re-embed every example.
