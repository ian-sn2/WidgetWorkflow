---
name: widget-qa
description: Check a notes file before delivery - mechanical checks, rendered screenshots, phone-size and interaction testing, label-fit measurement and the test suites. Use after any change to a notes file, widget, edition or checker script, and before sending files to Ian.
---

# Checking before delivery

## Static checks (under a second; run after every change)
```
python scripts/embed_engine.py FILE.html                    # engine copy must be byte-identical
python scripts/check_file.py FILE.html                      # must be 0 FAIL; read the WARNs too
python scripts/check_file.py FILE.html --source SOURCE.html # whenever it was built from another file (catches lost class dates)
python scripts/check_file.py FILE.html --no-head            # another publisher's file
```
After changing a checker or helper: `python scripts/test_check_file.py`, `python scripts/test_curve_shapes.py`, `python scripts/test_widget_text.py` (all 0 failing). `check_file.py` holds a copy of the engine's geometry: an engine margin change needs both edits in one commit.

## Browser checks (seconds each; run once the static checks pass)
```
python scripts/render_widgets.py FILE.html -o shots           # every widget × scenario × step; LOOK at every PNG
python scripts/mobile_check.py FILE.html --width 390
python scripts/mobile_check.py FILE.html --width 320 --height 568
python scripts/check_calc_widgets.py FILE.html                # calculator widgets
```
- `pip install playwright` once per container; Chromium is at `/opt/pw-browsers/chromium`. Never run `playwright install`.
- **Render what the reader loads**: pass the agent proxy (`HTTPS_PROXY`) so the house stylesheet and script arrive. If MathJax's CDN is blocked, serve `npm pack mathjax@3.2.2` locally through `page.route`, or raw TeX will fake a sideways-scroll failure.
- **Drive every control.** A check that never presses a button is not checking it.
- **Measure, don't eyeball.** Label inside its cell or shape (`getBBox`, digit height ≈ 0.72em), labels clear of arrows and nodes, widget height constant across steps (no layout shift), `documentElement.scrollWidth` equal to the viewport at 900, 390 and 320px.
- Images that lazy-load must be forced eager before measuring page height.

## Never
Edit an embedded engine copy (re-embed instead), commit `shots/`, or "fix" a known finding in `examples/` without checking `docs/open-issues.md` first.
