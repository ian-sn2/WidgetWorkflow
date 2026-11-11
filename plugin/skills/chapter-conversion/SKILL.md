---
name: chapter-conversion
description: Convert a chapter (notes HTML, PDF, Word file or lecture transcript) into a Smokin' Notes HTML file with widgets in place of its graph images - house head, headings, formulas, image maps, changelog - or update an existing file for a new semester. Use when Ian sends a chapter, a module zip or a transcript to convert, another publisher's (UCF/StudyKnight) files, or a message like "this semester it's hotdogs, demand shifts right by 20".
---

> **Files:** every path below (`scripts/…`, `docs/…`, `engine/…`, `examples/…`, `CLAUDE.md`) is in this plugin's root folder, two levels up from this skill (`../../scripts/…`), at the same place it sits in the WidgetWorkflow repo.

# Converting a chapter

The procedure is `docs/conversion-prompt-v7.md` (steps 0, 0T, 0C, 1–8); `/convert` starts it. In this repo you may **ask when a wrong guess is costly** (a number, which graphs to convert, which reading of a figure), batched. Decide everything else and flag it in the changelog.

## First: file the sources
Put the files Ian sent, unchanged, in `chapters/<COURSE>/<chapter>/source/`, and write `chapter.json` (build steps with `{source}`/`{out}`, and the outputs). `python scripts/build_chapters.py <filter>` builds into `build/chapters/`. Only sources are committed.

## Inputs
- **Word file**: `python scripts/doc_headings.py FILE` for the heading levels; use exactly that list. `python scripts/doc_formulas.py FILE` for MathType equations (`--check NOTES.html` audits the output). A `.doc` needs both `antiword` and `catdoc`, since antiword drops floating text boxes (exam tips, worked examples).
- **Transcript**: paraphrase, and never name the source ("the lecture", "in class", "the slides").

## House format (CLAUDE.md hard rule 7)
- Head: Red Hat Display font, `content/sn25-v6.css`, `studyguide/sn25-v2.js` (builds the TOC, so no written-in TOC), then `<!--SDG-ENGINE-->`. **Leave the `<title>` exactly as given.**
- `<p class="date">` per class date; `<h1>`/`<h2>` only (`<h3>` on Concise pages); `.exam-tip` with `<h4>`; Glossary and Key Takeaways are `<h2>`s.
- `<strong>` for vocabulary terms in text you write; **the source's own `<strong>` stays**. A displayed definition is a centred `<strong>\( … \)</strong>`.
- **Names**: keep a named professor and list it in the changelog. Whether it publishes is Ian's call.

## Images
- Each graph becomes a widget (`widget-basics`, `curves-and-labels`, `other-charts`). Anything else stays the image it is, with `<!-- KEEP: why -->` before it.
- **Map-driven placement**: `python scripts/apply_widgets.py SOURCE.html MAP.json OUT.html [--anchors] [--toc]`. It replaces only mapped images and refuses to write a file that differs in anything else.
- **Other publishers (UCF/StudyKnight)**: only the widgets change, plus the TOC script swap (`--toc`). Their own head, stylesheet and title stay; check with `check_file.py --no-head`.

## Finish
Run `python scripts/embed_engine.py FILE`, then the `widget-qa` checks. Deliver the file plus a changelog whose first line is `COURSE-TERMCODE-Topic.html` (Fall 2026 = 263). Return individual files, not a zip, unless asked for a set.

## Semester swaps (an existing file, a new term)
1. **Find out whether anything changed**: `python scripts/transcript_diff.py FILE.html t1.txt [t2.txt…] [--quiet]`. Trust UNSUPPORTED lines; "stated" only means not obviously changed. Look an unsupported number up in the source; never edit it to taste.
2. **Words only**: `python scripts/widget_text.py FILE.html --json > semester.json`, edit, then `--apply semester.json`. Coordinates and step wiring are never touched. Run `python scripts/test_widget_text.py` after changing the script.
3. **Numbers changed**: rebuild those widgets; the default output is patch blocks (`=== REPLACE / === WITH / === END`).
