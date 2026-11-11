---
name: study-guide-editions
description: Make the Balanced and Concise editions of a chapter from its Full edition, including which widgets carry over, heading rules and word targets. Use when Ian asks for "balanced and concise versions", or when fixing an edition's structure.
---

> **Files:** every path below (`scripts/…`, `docs/…`, `engine/…`, `examples/…`, `CLAUDE.md`) is in this plugin's root folder, two levels up from this skill (`../../scripts/…`), at the same place it sits in the WidgetWorkflow repo.

# Full, Balanced and Concise

| Edition | What it is | Widgets |
|---|---|---|
| **Full** | The chapter as converted | All |
| **Balanced** | The Full trimmed (~75–90% of its words): repetition, side remarks and duplicated tables cut; every figure, table and number kept | All |
| **Concise** | Rewritten as bullets and tables (~20–30%), ending with `<h2>Glossary</h2>` and `<h2>Key Takeaways</h2>` | Only where the text is hard to grasp without it |

## Rules
- **The Concise keeps the Full's `<h1>`/`<h2>` headings exactly**: same wording, same order, none merged or dropped. Add Glossary and Key Takeaways at the end, and `<h3>` subheads (often ending in a colon) where they help. **Assert it in the build**: `headings(concise) == headings(full) + ["Glossary", "Key Takeaways"]`.
- **Concise widget test** (Ian, 2026-10-26): keep a widget only if the concept is complex and the text cannot carry it (a CPM pass with its four times, a stepper filling a table, a financial calculator). A simple diagram goes; a figure with data becomes a table.
- **Never two widgets back to back** with no text between them.
- **Class dates**: Full and Balanced keep every `<p class="date">` (`check_file.py --source` fails a lost one). Concise pages may leave them out (Ian's call).
- Paraphrase in original wording. Don't name the professor in rewritten Concise text.
- Every number in a Concise comes from the Full. Recompute and assert the totals in the build.
- A Balanced is produced by checked `rep()` cuts on the Full, each asserting it matched once, so the edition rebuilds whenever the Full changes.

## Existing builds to copy
`scripts/man4504/project_mgmt_editions.py`, `scripts/man4504/transport_editions.py`, `scripts/ree3043/chapter17_editions.py`, `scripts/mar3023/concise2.py`, `scripts/mar3023/balanced2.py`, and `scripts/mar3023/chapter22_concise_headings.py` (fixes an existing Concise's headings).

Check every edition with the `widget-qa` skill.
