---
name: other-charts
description: Build a figure that is not a supply-and-demand style plot - flow charts, circular flow, project networks (CPM/PERT), payoff matrices, repeated games, amortization, figure tables, financial calculator widgets, and hand-built page charts (step-by-step steppers, colored networks, normal/beta curves, Gantt charts, pies, path charts). Use when a source figure is a diagram, network, grid, calculator screen, or a chart Ian wants made interactive or colored outside the graph engine.
---

> **Files:** every path below (`scripts/…`, `docs/…`, `engine/…`, `examples/…`, `CLAUDE.md`) is in this plugin's root folder, two levels up from this skill (`../../scripts/…`), at the same place it sits in the WidgetWorkflow repo.

# Other types of charts

Pick the first route that fits.

## 1. An sd-graph diagram widget (JSON, like any widget: `widget-basics`)
| Source figure | Widget (section in `docs/engine-reference.md`) |
|---|---|
| Chain of boxes, supply chain, channel | `flow`; `vertical: true` if the page reads top to bottom; `spans` brace a run |
| Circular flow of income | `flow` with `cycle: true` |
| Open-market diagram | chain `flow`, two-way link, `plain` nodes |
| CPM/PERT network | `network` (`show` steps the passes and critical path; `style: "ellipse"`; `aoa: true`; `panels`) |
| Payoff matrix | `matrix` (marks with `given`) |
| Same game year after year | `plays` |
| Loan amortization | `amort` |
| A figure's own table beside a plot | `table.plain` |
| Histogram, bar chart | rectangular `areas` |

## 2. An HP 10bII+ calculator widget (any calculator screenshot)
- Engine: `engine/hp10bii.css`/`.js`. `apply_widgets.py` embeds them when a map entry carries `"hp"`. Kinds: `tvm`, `cf` (NPV, IRR, `PI`), `amort`, `stat`, `keys`; options `alt`, `then`, `occurrence`.
- Follow the notes' convention: P/YR set, N in periods, I/YR annual. Amortization rounds to four places.
- Verify with `python scripts/check_calc_widgets.py PAGE.html [--all-alts]` (compares `data-expect`; strip it from the delivery). Build: `scripts/fin3403/`.

## 3. A hand-built page chart (Ian's own chapters, at his request)
Copy an existing build:

| Build | Makes |
|---|---|
| `scripts/man4504/transport.py` | Transportation-table **stepper** (Option A, the chosen design) |
| `scripts/man4504/project_mgmt.py` + `.css` + `.js` | Colored CPM network, crashing, node legend, beta/normal curves, Gantt, PERT calculator; `--patch` updates a converted file |
| `scripts/mar3023/chapter22_pert.py` | PERT path chart, opening on the whole chart; `--patch` |
| `scripts/ree3043/chapter17.py` | Pies, bars, filters, hoverable tree, timeline |
| `scripts/mcb4503/module13.py` | Interactive pie |

Rules for these:
- **The stepper is the default** for a worked calculation.
- Every number is computed and **asserted** against the notes.
- A step changes the drawing.
- **No layout shift**: stack the captions in one grid cell.
- **Width**: a widget spans about 75–80% of the page on desktop (`width: 78%`) and the full width on phones, and its figure scales with it rather than keeping a fixed pixel size (Ian, 2026-11-12).
- Labels sit **inside** their shape, or outside with a leader ending on it, **measured in Chromium**.
- Re-lay out top to bottom on phones.
- No instruction text in captions, and no repeating the prose that follows.
- Keep the original image in `<noscript>`.
- Tables get class `financial` against the house CSS.

## 4. Neither
A pictorial diagram (a shipping network, a conflict tree) is a static HTML figure through `apply_widgets.py`'s `{"html": block}`. A tree diagram, photo or published chart stays an image with `<!-- KEEP: why -->` before it.
