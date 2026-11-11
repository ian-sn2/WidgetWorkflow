---
name: review-notes
description: Review files Ian has written or edited (a chapter, a Concise or Balanced edition, a module zip) and report the problems without changing anything. Use when Ian asks to "check", "double check", "review" or "are there any issues in" his files.
---

> **Files:** every path below (`scripts/…`, `docs/…`, `engine/…`, `examples/…`, `CLAUDE.md`) is in this plugin's root folder, two levels up from this skill (`../../scripts/…`), at the same place it sits in the WidgetWorkflow repo.

# Reviewing Ian's files

**Report and change nothing** unless he asks for the fix (Ian, 2026-10-12). Folders marked `x-ignore` are out of scope; skip them without comment.

## Report in this order, most costly first
1. **Broken widgets and wrong heading structure.** Load the page and press every control (`widget-qa`). A Concise must keep the Full's h1/h2 headings.
2. **Layout and page errors.** Sideways scrolling at 390/320px, a lost class date, a missing or duplicated TOC (the `sn25-v5.js` vs `studyguide/sn25-v2.js` head script), house-CSS clashes.
3. **Wrong or contradictory content.** Recompute every number the page states.
4. **Missing information.** Compare with the Full or the source.
5. **Housekeeping.** `<u>` tags, stray markup, a source-revealing phrase ("the slides", "in class").

## Judge each edition by what it is meant to be
- **Full**: the source as converted.
- **Balanced**: close to Full.
- **Concise**: rewritten, usually without images, `<h3>` expected; widgets only where needed.

## Not findings
Glossary and Key Takeaways as `<h2>`; an `<h3>` ending in a colon on a Concise page; a `<title>` carrying course and term (it comes from Ian's boss). Mention a named professor as a question for Ian, not as an error.

When a fix is requested, keep it minimal and give a copy-paste block if he pasted the original.
