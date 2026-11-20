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
6. The free allowance, read from Google's pricing page on 2026-11-18: the first **1,000,000 characters each month**
   with Chirp 3: HD voices cost nothing; after that it is US$30 per million characters. Spaces count as characters.

## Free characters, the $300 trial credit, and the card

These are three separate things, used in this order:

1. **The monthly free characters.** The first million each month are simply not charged. They never appear as
   spending, which is why the trial credit still reads $0 used after a 45,000-character chapter.
2. **The $300 trial credit.** Only usage *past* the free million in a month is priced, and while the trial lasts
   that price is taken from the credit. A second million characters in one month would take $30 of it. The credit
   expires at the end of the trial whether or not it was used.
3. **The card.** Charged only after the trial has ended (and the account upgraded) *and* a month goes past the
   free million.

The builder stops itself at 900,000 characters a month, so on its default setting it never reaches step 2. To
record more than that in a month, raise `GOOGLE_TTS_MONTHLY_LIMIT`; the cost is then $30 per extra million.

## What Google keeps

Nothing, by its own statement ("Google does not log any customer Cloud TTS text or audio data", data-logging
page, read 2026-11-18). The service is stateless: text goes up, audio comes back in the same response, and no
file is created in the Google Cloud project. The recordings exist in two places only: `~/.cache/narrate` on the
machine that ran the build, and the page (or, in production, the S3 folder beside the images).

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

## Serving the audio from a Google Cloud Storage bucket

A chapter's audio is about 10 MB. Inside the page it makes a 13 MB file; served from a bucket the page is under
100 KB and the audio streams. The bucket is `sntext2speech`, in the same Google Cloud project as the voice.

One-time setup of a bucket (done 2026-11-18): **Cloud Storage > Buckets > Create**, a US region (us-east1,
us-west1 or us-central1 count toward the free allowance), Standard class, *Enforce public access prevention*
off; then the bucket's **⋮ > Edit access > Add principal** `allUsers` with the role **Storage Object Viewer**.
Leave Hierarchical namespace and Rapid Cache off. Drive is not a substitute: it is not built to stream to a page.

Building a page for the bucket:

```bash
NARRATE_ENGINE=google NARRATE_VOICE=en-US-Chirp3-HD-Charon python scripts/ideas/narrate.py listen <chapter>.html out/<chapter>.html --read --sections h1 --audio-dir out/listen-audio --audio-url https://storage.googleapis.com/sntext2speech/listen-audio
```

That writes `out/listen-audio/<chapter>/` with one MP3 per section. Drag the `listen-audio` folder onto the bucket's
**top level** and the page plays. The console uploads into whichever folder is open, and can stay inside a path after
a delete, which is how the first upload ended up at `audio/audio/`: click the bucket's name in the breadcrumb first,
so it reads only `Buckets > sntext2speech`. The folder's name in the bucket has to match the end of `--audio-url`. Each file's name ends in a fingerprint of its
contents, so a re-recorded section gets a new address; old files can be deleted from the bucket at leisure.

The speech key cannot write to a bucket, so the upload is by hand for now. From a computer signed in with
`gcloud auth login`, `gcloud storage cp -r out/listen-audio gs://sntext2speech/` does the same.

Free each month (Google's free-tier page, read 2026-11-18): 5 GB stored in a US region and 100 GB downloaded
from North America, which is about 500 chapters stored and 10,000 complete listens. Past that, about $0.02 per
GB-month stored and $0.12 per GB downloaded.

## More than one voice, and a summary beside the full read

```bash
NARRATE_ENGINE=google python scripts/ideas/narrate.py listen <chapter>.html out/<chapter>.html --sections h1 --voices Aoede,Kore,Charon --also-read Charon
```

`--voices` records the page in each voice named (the first is what a listener hears until they choose another).
`--also-read` adds, on a page that has a summary script, a read-as-written recording in the voices named. With
more than one recording the bar gains a reader button beside the skip buttons, listing the versions and the
voices; changing either keeps the listener's place, and both choices are remembered on the device.

Every recording is billed in full: characters cannot be shared between voices. A summary is about a third of a
full read, so three voices of a summary cost about what one voice of the full read does. With `--audio-dir`, each
file's name carries its version and voice.

## Hard words

Before a paragraph is recorded, every rare word in it is looked up and the voice is told how to say it
(`pronounce.py`: the built-in dictionary, then Wiktionary, then a prefix plus a known word). The listening report
lists what was taught and from where, with a clip of each looked-up word said on its own. A name no dictionary
has, or a word still said wrong, goes in `scripts/ideas/narration/pronounce.json` once and is right in every
chapter after that. Wiktionary has to be an allowed site for the live look-up (`en.wiktionary.org`); without it
the built-in dictionary and the two files are still used.

```bash
python scripts/ideas/pronounce.py heterochrony cichlids "Van Valen"
```

## The swap list and its tests

Abbreviations and symbols are turned into words before the voice sees them. The rules that apply everywhere are
in `narrate.say()` (Roman numerals after a numbering word, subscripts, Greek letters, ÷ = − %, money, ranges,
pounds, arithmetic written tight, and any number with a thousands separator spelled out in words, because the
voice read "4,712 units" as "four, seven twelve"). One-off abbreviations go in `narration/say.json` ("FSBO": "fizz-bo"), which
needs no code change. `python scripts/ideas/test_narration.py` checks them, starting from the five-passage test
sheet; run it after changing either.

## Things to check on the first real recording

* The automatic listening check (`--report`, on by default in `build_demos.py`) flags any paragraph the new voice
  says differently from the script. A capital "A" used as a name (Activity A) is the likeliest thing to be misread.
* The pace. The builder asks Google for 1.1x on Listen pages; if a voice refuses a pace, the builder records at
  normal speed and adjusts it locally.
