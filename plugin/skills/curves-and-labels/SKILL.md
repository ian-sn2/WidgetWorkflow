---
name: curves-and-labels
description: Draw curves and place labels in an sd-graph widget - generating curve shapes, equilibrium crossings, shading, braces, arrows, guides, ticks, and placing curve, point and area labels so nothing collides. Use when drawing or fixing the geometry of a graph, or when a label sits on a curve, axis, arrow or another label.
---

> **Files:** every path below (`scripts/…`, `docs/…`, `engine/…`, `examples/…`, `CLAUDE.md`) is in this plugin's root folder, two levels up from this skill (`../../scripts/…`), at the same place it sits in the WidgetWorkflow repo.

# Drawing curves and placing labels

Schema: `curves`, `points`, `areas`, `moves`, `hlines`, `braces`, `vbraces` and "Geometry, for placing labels by hand" in `docs/engine-reference.md`. The settled conventions are CLAUDE.md's "Drawing conventions"; the essentials are below.

## Curves: generate them, never type them
`scripts/curve_shapes.py` (run `python scripts/test_curve_shapes.py` after changing it):
- `cross`: name every crossing and build equilibrium dots from it. Typed coordinates drift off the curve.
- `cost_family` (MC through both average minima), `tangent_to_line`/`tangent_to_hyperbola` (touch, never cross), `on_hyperbola` (points on the curve's own samples), `supply_fan`, `lorenz`, `hug`, `around`.
- A point sits on one of its curve's own sample points. A curve runs to the plot's edge (or a meaningful end: an intercept, the axis) and well past the point it is drawn for (~0.45× to 6× its x).
- Clip the axes to the region used. `assert` every relationship in the build.

## Look
- Black original curve, red shifted curve, every arrow red. The original of a shift pair is drawn at full weight (no `thin`); the engine fades it once the shift arrives.
- Shading: consumer surplus teal, producer surplus orange, gains from trade teal, deadweight loss red, revenue navy. Two pieces of one surplus take `edge: true`.
- One guide per quantity (`guides: "p"`/`"q"`), each with a number at its foot. Draw the equilibrium guide once per widget.
- A dot wherever a price meets a curve the source marks, the control price included, and no extra dots.
- Arrows: a shift arrow's `arrowP` lies inside both curves; a gap under ~18px is written ("+$2T"), not arrowed; arrows stand 3–4px off the lines they separate; no arrow over the dashed guides.
- `SRAS`/`LRAS`. One superscript letter after P; `_{...}` for word subscripts. Copy the source's own labels, capitals and subscripts.

## Labels (CLAUDE.md hard rule 5: nothing touches a curve, an axis line or its own curve)
- **Area labels**: `python scripts/place_labels.py`. Check which it did: centred is the answer unless the shape is a sliver.
- **Curve labels**: `python scripts/place_curve_labels.py`. Use one offset for a series; where it reports nowhere clear, change the drawing (run the curve further, or `lstart`).
- A label stays on the thing it names. Fade the crossing curve (`dimAt`) rather than moving the label off its brace.
- A brace's label sits at its midpoint, beside it; braces sit against their price line (`below: "in"`/`"axis"`/`true`), where the source draws them. Wrap long names with `\n`.
- A point's name sits level with its dot, to the right (`dx 12, dy 4`).
- `boxed: true` only where no gap exists (Lorenz years), never over a wedge.

Then render and look at every step (`widget-qa`).
