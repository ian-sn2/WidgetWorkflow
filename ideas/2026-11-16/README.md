# Idea demos, 2026-11-16

Open `SUMMARY.html` first (`SUMMARY.txt` is the same text, ready to paste). Each folder is a working demo built on the
Exam 3 files from SentToClaude.zip.

| Folder | What to try |
|---|---|
| `ALL-IDEAS-send-these/` | **The pages to forward.** One page per chapter with every idea that applies to it. Project Management (Full): Play, what-if labs, animation, tap-to-define. Aggregate Planning (Concise): Listen, Play, animation, tap-to-define. MAR3023 Chapter 22 (Concise): Listen, tap-to-define. |
| `1-Play-NarratedWalkthrough/` | Press Play on "The Forward Pass"; the speaker button turns the voice off. The `.mp4` is the same widget filmed by `scripts/ideas/record_video.py`. |
| `2-WhatIf-Lab/` | Open "Try it" under Step 6, tap B, then D. In the crash lab, tap F, then G. |
| `3-Tap-To-Define/` | Tap any term with a dotted underline. |
| `4-Listen-AnyPage/` | Tap Listen at the bottom right. The line being spoken is highlighted and followed; tap a line to jump to it. |
| `5-Animated-MAN4504/` | All six MAN4504 pages, animated. `Animated-widgets-preview.mp4` is a 40-second tour. |
| `listen-samples/` | Two sections of the MAR3023 audio: tables introduced with their columns, and the PERT chart explained. |
| `narration-check/` | What the automatic listener found for each narrated page: a short report, and one clip of only the passages it wants a person to hear. |

Rebuild: `python scripts/ideas/build_demos.py <unpacked zip> ideas/2026-11-16` (add `--only-all`, `--only-listen`, ... for one part).

To record with Google's Chirp 3: HD voices instead, see `scripts/ideas/GOOGLE-VOICE-SETUP.md`.

The default voice is Kokoro (open source, offline). Once per machine: `pip install kokoro-onnx soundfile numpy`, then put
`kokoro-v1.0.onnx` and `voices-v1.0.bin` (kokoro-onnx GitHub releases, "model-files-v1.0") in `~/.cache/kokoro/`.
What the voice says is in `scripts/ideas/narration/`; its README is the prompt for writing a new chapter's script.
