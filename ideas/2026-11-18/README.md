# First run with Google's Chirp 3: HD voice, 2026-11-18

`BSC2010-263-Exam3-Module5-Final-Full.html` (not committed: it carries about 41 minutes of audio, 13 MB) is the
Full chapter with the Listen bar. The whole chapter is read as written in the Chirp voice "Charon" (Ian's pick
from the six samples).

What the page does:

* **Sections.** The audio is divided at the chapter's four `<h1>` headings. The ☰ button lists them with their
  lengths; picking one starts it.
* **Speed.** The speed button offers 0.85× to 2× and shows how long the whole chapter takes at each. The choice is
  remembered on that device.
* **Following along.** The paragraph being read is tinted, the sentence in it is highlighted, and the word being
  spoken is marked inside the sentence. The page scrolls to keep the sentence in view. Tapping any paragraph
  starts the reading there. A heading's words are highlighted while it is read; its box is never restyled.

| Folder | What it is |
|---|---|
| `google-voice-samples/` | The same passage in six Chirp voices, to choose from. |
| `test-passages/` | Ian's five test passages (Roman numerals, Greek letters, a formula, table rows, a long paragraph) recorded in Charon, with what the voice was given and what the automatic listener heard. |
| `narration-check/` | The automatic listener's report, a clip of only the sentences it wants a person to hear, and a clip of each looked-up hard word said on its own. |

Hard words (names, technical terms) are looked up before recording and the voice is told how to say them:
`scripts/ideas/pronounce.py`. What was taught, and from which source, is in the report.

Rebuild (records only what is not already kept in `~/.cache/narrate`):

```bash
NARRATE_ENGINE=google NARRATE_VOICE=en-US-Chirp3-HD-Charon python scripts/ideas/narrate.py listen <the chapter>.html ideas/2026-11-18/<the chapter>.html --read --sections h1 --report ideas/2026-11-18/narration-check
```

`NARRATE_VOICE` is the only thing to change for another voice; the whole chapter is then recorded again (about
45,000 characters).

`--read` reads the page as written and needs no script. `--sections h1` divides the audio at `<h1>` only (the
default divides at `<h2>` as well). Without `--read`, the builder looks for a script in
`scripts/ideas/narration/`; a condensed 16-minute script for this chapter is there
(`BSC2010-263-Exam3-Module5-Final-Full.json`) if a short version is wanted.

How the word timing is found: the voice returns no timings, so the builder finds each sentence's start from the
pauses in the recording, and the word marker moves through the sentence in proportion to the words' lengths. The
sentence is exact to a fraction of a second; the word is an estimate and can run a word ahead or behind.
