# Narration scripts

One JSON file per page, named after the page. The voice speaks the script, not the page.

```json
{
  "steps":    { "<widget title>": ["what to say on step 1", "step 2", "..."] },
  "sections": { "<h1 or h2 text>": [["<words found in the block this passage is about>", "what to say"], ["", "a passage about no one block"]] },
  "steps_from": "<another page's file name, no .json>"
}
```

`steps` narrates a step-by-step widget (the Play button and the recorded video). `sections` narrates a whole
page (the Listen bar): one list per heading, in reading order, one passage per bullet, paragraph or table row.
The first string of a passage is copied from the page; the builder finds the first `li`, `tr`, `p`, `h3` or `h4`
in that section containing it, and the Listen bar highlights and scrolls to that block while the passage plays.
For a table row use the first cell followed by ` |` (`"Brand manager |"`). `steps_from` reuses another edition's
step scripts when the same widget appears on both.

## How to write one (this is the prompt for Claude each semester)

Write for the ear, as a tutor talking one student through the page.

* **Do not read the page.** Say what the bullet means. Fragments become sentences; `=` and `→` become words.
* **Vary the sentences.** Short ones land a point. Ask the question the student should be asking, then answer it.
  Use contractions. One idea per sentence. This is what gives the voice its rise and fall: it has no other control.
* **Cover everything, tables included.** One passage per row, in the order the page shows them, so the highlight
  walks down the table.
* **Every number comes from that step or section of the page**, written as digits (`105,152 dollars`, `1.5 percent`).
  The build stops on a number the page does not print there. Spell out counts of things (`three paths`).
* **Never mention a source** (the transcript, the lecture, the slides, the recording, the board, the file).
* Write money as `40 dollars`, percentages as `10 percent`, and abbreviations the way they are said (`ROI`, `CMO`
  are spelled out by the voice; `PERT` is read as a word).
* A capital `A` used as a name (Activity A) is handled by the builder. Avoid opening a sentence with the article
  "A" followed by a verb-like word ("A first look..."), which would be misread as the letter.

Check a new script without recording anything: run the build with a missing model folder
(`KOKORO_DIR=/nonexistent`) or read the assertion it stops on.
