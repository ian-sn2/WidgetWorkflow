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

Hard words are looked up before recording and the voice is told how to say them (`../pronounce.py`).
`pronounce.json` is the list entered by hand: names and terms no dictionary has, and anything said wrong, as
`"word": {"ipa": "...", "from": "where it came from"}`. `learned.json` is written by the builder: what it looked
up on Wiktionary, so each word is asked for once. Both apply to every chapter.

`"mode": "summary"` declares a condensed narration for a Full edition: a block may go unspoken and not every
number is said, but what is said must still be on the page. Built with `--sections h1`, a scripted page gets one
clip per `<h1>` and each heading is spoken as the listener reaches it. A summary is the preferred style (2026-11-20):
about a third of the length and the characters of reading the page as written (`--read`).

## How to write one (this is the prompt for Claude each semester)

Write for the ear, as a tutor talking one student through the page.

* **Do not read the page, and do not chop it up.** Say what the bullet means in connected sentences. Each passage is
  recorded as one continuous take, so a run of two-word sentences sounds choppy; a line break starts a new take
  after a short beat (use one inside any passage longer than about 60 words).
* **Keep it shorter than reading.** The build stops if a script is more than 120% of the words of the text it
  speaks for. No warm-up ("Here is a worked example"), no restating. A Concise chapter should come to 7 to 9 minutes.
* **Do not narrate the Glossary.** Give it an empty list (`"Glossary": []`): every term is already defined where
  it comes up. Key Takeaways is a recap: group several bullets under one passage by giving a list of anchors,
  `[["first bullet", "second bullet"], "one passage for both"]`.
* **Leave nothing else out.** Every bullet, paragraph and table row gets a passage, in page order, and every number
  in it is spoken. The build stops otherwise.
* **Introduce every table.** Its first passage is anchored to the header row and names each column ("For each
  method, it gives the focus and the use"). Each row then says which column a value belongs to ("Its focus is ...
  Its use is ..."), so the listener never hears a cell without knowing what it is.
* **Explain a widget, do not skip it.** Anchor a passage to the widget itself with `@pertw`, `@tpw`, `@pmw` or
  `@sdg` and describe what it shows: what the rows, columns, nodes or axes are, then the values.
* **Every number comes from that step or section of the page**, written as digits (`105,152 dollars`, `1.5 percent`).
  Spell out counts of things (`three paths`).
* **Never mention a source** (the transcript, the lecture, the slides, the recording, the board, the file).
* Do not put "too", "to" or "for" straight after a number ("at 0 too" is heard as "zero two"): say "as well" or "also".
* Write money as `40 dollars`, percentages as `10 percent`. `ROI`, `CMO`, `MRP` are spelled out by the voice;
  `PERT` is read as a word. A capital `A` used as a name (Activity A) is handled by the builder.

## Checking a recording without listening to all of it

`narrate.py ... --report DIR` transcribes every recorded paragraph with speech recognition (`hear.py`) and compares
it with the script. It writes `<page>.listening-check.txt`, listing each paragraph where a number or a content word
was heard differently, and `<page>.listen-to-these.mp3`, which is only those paragraphs. Review is: read the script
(the build has already checked its numbers and its coverage), then play that one clip.
