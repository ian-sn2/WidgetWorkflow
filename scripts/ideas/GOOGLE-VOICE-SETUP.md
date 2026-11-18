# Recording narration with Google's Chirp 3: HD voices

The builder can record with Google Cloud Text-to-Speech instead of the offline voice. Nothing else changes: the
scripts, the build checks, the highlighting and the automatic listening check all work the same.

## One-time setup in Google Cloud (about ten minutes)

Menu names in the Google Cloud console change from time to time; the search box at the top finds each of these.

1. Go to console.cloud.google.com and **create a project** (for example "study-guide-voice").
2. **Link a billing account** to it. Google asks for a card even though our volume sits inside the free allowance.
3. Search for **Cloud Text-to-Speech API** and press **Enable**.
4. Go to **APIs & Services > Credentials > Create credentials > API key**. Then edit the key and, under
   **API restrictions**, restrict it to **Cloud Text-to-Speech API** only, so the key can do nothing else.
5. Go to **Billing > Budgets & alerts** and create a budget of a few dollars with email alerts. A budget warns; it
   does not stop charges. The builder's own monthly limit (below) is what stops them.
6. Check the free allowance for Chirp 3: HD on the official pricing page (cloud.google.com/text-to-speech/pricing).
   It was reported as 1,000,000 characters a month when this was written.

## Giving the builder the key

Never paste the key into a chat, a file in this repository, or a page.

* **On your own computer:** set it for the terminal session, `export GOOGLE_TTS_KEY=...` (or add it to your
  shell profile).
* **In a Claude cloud session:** ask Claude to request the Google key. A secure form opens; the key is stored on
  the session's environment and attached to requests to `texttospeech.googleapis.com` without Claude seeing it.

## Using it

```bash
NARRATE_ENGINE=google python scripts/ideas/narrate.py voices
```

```bash
NARRATE_ENGINE=google NARRATE_VOICE=en-US-Chirp3-HD-Aoede python scripts/ideas/narrate.py sample "A share point is 1 percent of total industry sales." sample.mp3
```

```bash
NARRATE_ENGINE=google NARRATE_VOICE=en-US-Chirp3-HD-Aoede python scripts/ideas/build_demos.py <unpacked zip> ideas/2026-11-16
```

The first lists the voices the key can use. The second records one clip, to compare voices by ear. The third
builds the pages with the chosen voice.

## What keeps it free

* **Kept takes.** Every recorded paragraph is saved in `~/.cache/narrate`. Rebuilding a study guide sends Google
  only the paragraphs whose script changed. Do not delete that folder casually: it is the recordings.
* **A monthly limit.** The builder tallies the characters it sends each calendar month in
  `~/.cache/narrate/google-usage.json` and stops, before sending, when the next paragraph would pass
  `GOOGLE_TTS_MONTHLY_LIMIT` (default 900,000). Each build prints the month's total.
* **Volume.** A Concise chapter with its Play steps is about 12,000 characters, so the default limit is about 75
  chapters a month.

## Things to check on the first real recording

* The automatic listening check (`--report`, on by default in `build_demos.py`) flags any paragraph the new voice
  says differently from the script. A capital "A" used as a name (Activity A) is the likeliest thing to be misread.
* The pace. The builder asks Google for 1.1x on Listen pages; if a voice refuses a pace, the builder records at
  normal speed and adjusts it locally.
