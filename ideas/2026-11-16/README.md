# Idea demos, 2026-11-16

Open `SUMMARY.html` first. Each folder holds a working demo built on the Exam 3 files from SentToClaude.zip.

| Folder | Open | Try |
|---|---|---|
| `1-Play-NarratedWalkthrough/` | the Project Management page, "The Forward Pass" | press Play; the speaker button turns the voice on or off. The `.mp4` is the same widget filmed by `scripts/ideas/record_video.py`. |
| `2-WhatIf-Lab/` | the Project Management page, Step 6 and Project Crashing | open "Try it", tap B, then D. In the crash lab, tap F, then G. |
| `3-Depth-Switch/` | the Aggregate Planning page | use Short / Medium / Full at the top, and "More detail" under a section. |
| `4-Listen-AnyPage/` | either page | tap Listen at the bottom right; skip sections, change speed. Works on any page with headings. |

| `5-Animated-MAN4504/` | all six MAN4504 pages (both chapters, Full / Balanced / Concise) | scroll: each widget animates when it comes on screen and on every button press. `Animated-widgets-preview.mp4` is a 40-second tour. The Full and Balanced Project Management pages also carry the what-if labs. |
| `voice-samples/` | five MP3s of one caption | `0` is the old stand-in; `1` to `4` are Kokoro voices. `1` (heart) is the one used in the demos. |

The voice is Kokoro, an open-source neural voice that runs offline (`tts()` in `scripts/ideas/narrate.py`).
Setup once per machine: `pip install kokoro-onnx soundfile`, then put `kokoro-v1.0.int8.onnx` and `voices-v1.0.bin`
(from the kokoro-onnx GitHub releases, "model-files-v1.0") in `~/.cache/kokoro/`. `NARRATE_VOICE=am_michael` picks another voice.
`2-WhatIf-Lab/WhatIf-Lab-motion-preview.mp4` is a short screen capture of the lab's animation.

Rebuild: `python scripts/ideas/build_demos.py <unpacked zip> ideas/2026-11-16`
