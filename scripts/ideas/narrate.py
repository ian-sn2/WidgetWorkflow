"""Recorded narration for a page.

    python scripts/ideas/narrate.py steps   <page with the Play add-on> [--report DIR]    one clip per step of every stepper
    python scripts/ideas/narrate.py listen  <any notes page> <out page> [--report DIR] [--read] [--sections h1]
                                            one clip per section + the Listen bar; --sections h1 divides the audio at h1 only

WHAT IS SAID. The voice does not read the page. It speaks a script written for the ear, kept in
scripts/ideas/narration/<page name>.json (see narration/README.md for how one is written):
    {"steps":    {"<widget title>": ["what to say on step 1", ...]},
     "sections": {"<h1/h2 text>":   [["<words found in the bullet, row or paragraph this is about>", "what to say"], ...]}}
Each section passage names the block it talks about, so the Listen bar can highlight that block and scroll to it.
A page with no script file, or any page given --read, is read as written: the whole text, paragraph by paragraph, each
highlighted as it is spoken. That suits a Full edition, whose text is already in sentences, and needs no writing at all.
These checks stop the build, so a script can be trusted without being listened to:
  * every number spoken is a number printed in that step or section of the page, and no script mentions a source;
  * every bullet, paragraph and table row of a section has a passage, and every number in it is spoken;
  * every table is introduced by a passage on its header row that names each of its columns;
  * the script is no more than 120% of the words of the text it speaks for, so listening is not longer than reading.
A section whose script is an empty list ("Glossary": []) is declared as not narrated.
With --report DIR the recording is also transcribed by hear.py and compared with the script; the paragraphs that do
not match are written to a report and joined into one short clip to listen to.

HOW IT IS SAID. Each paragraph is recorded as one continuous take at one speed, so the voice carries its own rhythm
from sentence to sentence. (Recording a sentence at a time, each at its own speed, sounded choppy.)

THE VOICE is one function, _voice(). It uses Kokoro, an open-source neural voice that runs offline at no cost per use:
    pip install kokoro-onnx soundfile
    put kokoro-v1.0.onnx and voices-v1.0.bin (kokoro-onnx GitHub releases, "model-files-v1.0") in ~/.cache/kokoro
    pip install --only-binary=:all: misaki num2words spacy && python -m spacy download en_core_web_sm
The last line is Kokoro's own dictionary-based pronunciation (misaki). Without it the voice still works, through a
generic pronouncer that gets the stress of some words wrong ("subcontract").
HARD WORDS are looked up before they are recorded and the voice is told how to say them: pronounce.py. A word still
said wrong, or a name no dictionary has, goes in narration/pronounce.json and is right in every chapter after that.
NARRATE_VOICE picks the voice (default af_heart).
NARRATE_ENGINE=google records with Google Cloud's Chirp 3: HD voices instead (voice_google.py, GOOGLE-VOICE-SETUP.md).
Either way every take is kept in ~/.cache/narrate, so a rebuild sends only the paragraphs whose script changed.
Clips are embedded in the page as data URIs so a demo is one file. For a real page, `listen ... --audio-dir FOLDER
--audio-url ADDRESS` writes them as files to be served from a bucket instead (GOOGLE-VOICE-SETUP.md).
"""
import base64
import hashlib
import html
import json
import os
import pathlib
import re
import subprocess
import sys
import tempfile
from html.parser import HTMLParser

import numpy as np

HERE = pathlib.Path(__file__).parent
CACHE = pathlib.Path(os.environ.get('NARRATE_CACHE', '~/.cache/narrate')).expanduser()     # every take, kept: a rebuild re-records only what changed
KOKORO = pathlib.Path(os.environ.get('KOKORO_DIR', '~/.cache/kokoro')).expanduser()
ENGINE = os.environ.get('NARRATE_ENGINE', 'kokoro')          # kokoro: offline and free.  google: Chirp 3: HD, see voice_google.py
VOICE = os.environ.get('NARRATE_VOICE', 'af_heart' if ENGINE == 'kokoro' else 'en-US-Chirp3-HD-Aoede')
RATE = 24000
LISTEN_SPEED = 1.1          # a whole chapter is spoken a little faster than a single step is
_kokoro = None

# ---------------------------------------------------------------- text
# reading a page as written (no script): symbols into words
SAY = [(r'\bES\b', 'early start'), (r'\bEF\b', 'early finish'), (r'\bLS\b', 'late start'), (r'\bLF\b', 'late finish'),
       ('→', ' to '), ('−', ' minus '), ('÷', ' divided by '), ('×', ' times '), ('=', ' equals '), ('≤', ' at most '),
       (r'\$(\d[\d,]*\d|\d)(?!\.\d|\d)', r'\1 dollars'), (r' \+ ', ' plus '), ('σ', ' sigma '), ('μ', ' mu '), (r'\)\(', ' times '), ('>', ' over '),
       (r'\bwk\b', 'week'), ('--', ' none '), ('&', ' and '), (r'\bvs\.', 'versus'),
       (r'\be\.g\.,?', 'for example,'), (r'\bi\.e\.,?', 'that is,'), ('—', ', '), (r'(?<=\d)–(?=\d)', ' to '), (r'\s–\s', ': '), ('–', ', '),
       ('%', ' percent'), ('°C', ' degrees Celsius'), ('°F', ' degrees Fahrenheit'), ('…', '.'), ('[“”"]', '')]
# A neural voice reads a lone capital A as the word "a". Where it is a name (Activity A, "A finishes at 2"), spell it
# the way the voice says the letter. A sentence that opens with A followed by an ordinary word keeps the article.
AFTER_LETTER = ('finishes|has|is|and|to|now|cannot|can|was|starts|takes|by|at|crashed|runs|had|or|equals|minus|plus|will|must|'
                'needs|could|would|does|did|were|are|comes|goes|gets|then|with|only|still|also|itself|alone|first|again|\\d')
LETTER_A = [re.compile(r'(?<![.!?:]\s)(?<!^)\bA\b(?!\'s)(?![a-z])'), re.compile(r'\bA\b(?=[,.;:)]|\s+(?:%s)\b)' % AFTER_LETTER)]
BANNED = ('the transcript', 'the lecture', 'the recording', 'on the board', 'the slides', 'his slide', 'the file')


LETTER = 'Aeigh'                        # stands in for a capital A that is a name; phonemes() gives it the letter's sound
_g2p = None


def prep(text):
    """a written script, ready for the voice: a capital A that is a name is marked as the letter"""
    text = re.sub(r'[ \t]+', ' ', text).strip()
    for pat in LETTER_A:
        text = pat.sub(LETTER, text)
    return GROUPED.sub(grouped, text)       # 12,000 goes to the voice in words, in a script as well as in page text


def phonemes(text, say_with):
    """text -> Kokoro phonemes, word by word, so one word's sound can be set without disturbing its neighbours.
    (misaki's inline [word](/phonemes/) syntax dropped the word after it: the listening check caught a missing 'finish'.)"""
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        _, tokens = say_with(text)
    import pronounce
    out = []
    for t in tokens:
        p = t.phonemes or ''
        if t.text == LETTER:
            p = 'ˈA'
        elif pronounce.fixed(t.text):
            p = pronounce.fixed(t.text)
        if re.fullmatch(r'[A-Za-z]\.', t.text) and not p.endswith('.'):
            p += '.'                    # "Now C. C has to wait": the full stop after a single letter is a pause, not an abbreviation
        out.append(p + t.whitespace)
    return ''.join(out)


def g2p():
    """Kokoro's own pronouncer, or None if it is not installed"""
    global _g2p
    if _g2p is None:
        try:
            import espeakng_loader
            from phonemizer.backend.espeak.wrapper import EspeakWrapper
            EspeakWrapper.set_library(espeakng_loader.get_library_path())
            EspeakWrapper.set_data_path(espeakng_loader.get_data_path())
            from misaki import en, espeak
            _g2p = en.G2P(trf=False, british=False, fallback=espeak.EspeakFallback(british=False))
        except Exception as e:          # the build still records, with the generic pronouncer
            print('          dictionary pronunciation unavailable (%s): using the generic pronouncer' % type(e).__name__)
            _g2p = False
    return _g2p or None


GREEK = {'α': 'alpha', 'β': 'beta', 'γ': 'gamma', 'δ': 'delta', 'Δ': 'delta ', 'ε': 'epsilon', 'θ': 'theta', 'κ': 'kappa', 'λ': 'lambda', 'π': 'pi',
         'ρ': 'rho', 'τ': 'tau', 'φ': 'phi', 'χ': 'chi', 'ψ': 'psi', 'ω': 'omega', 'Ω': 'omega'}
# a Roman numeral is a number only after a word that numbers things: CN V is "C N five", vitamin D and plan X are letters
NUMBERED = (r'CN|cranial nerves?|types?|class(?:es)?|phases?|stages?|grades?|factors?|complex(?:es)?|photosystems?|chapters?|parts?|sections?|'
            r'units?|modules?|world war|steps?|groups?|levels?|categor(?:y|ies)|tiers?|titles?|articles?|appendix|exams?|tables?|figures?')
ROMAN = re.compile(r'\b(%s)(\s+)([IVX]+)\b' % NUMBERED, re.I)
ROMAN_NEXT = re.compile(r'(\b(?:%s)\s+\d+(?:(?:,|,?\s+and|,?\s+or|\s+to|\s+through)\s+\d+)*(?:,|,?\s+and|,?\s+or|\s+to|\s+through)\s+)([IVX]+)\b' % NUMBERED, re.I)
DIGITS = 'zero one two three four five six seven eight nine'.split()


def roman(letters):
    """'XII' -> 12, or None if the letters are not a Roman numeral written the usual way"""
    vals, total = {'I': 1, 'V': 5, 'X': 10}, 0
    for k, ch in enumerate(letters):
        v = vals[ch]
        total += -v if k + 1 < len(letters) and vals[letters[k + 1]] > v else v
    back = ''.join(n * ch for n, ch in zip(divmod(total, 10), ('X', ''))) if total < 40 else None
    units = ['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX'][total % 10] if total < 40 else ''
    return total if back is not None and 'X' * (total // 10) + units == letters else None


SMALL = ('zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen').split()
TENS = 'twenty thirty forty fifty sixty seventy eighty ninety'.split()


def in_words(n):
    """4712 -> 'four thousand seven hundred twelve' (American: no "and")"""
    if n < 20:
        return SMALL[n]
    if n < 100:
        return TENS[n // 10 - 2] + ('-' + SMALL[n % 10] if n % 10 else '')
    if n < 1000:
        return SMALL[n // 100] + ' hundred' + (' ' + in_words(n % 100) if n % 100 else '')
    for size, name in ((10 ** 12, 'trillion'), (10 ** 9, 'billion'), (10 ** 6, 'million'), (1000, 'thousand')):
        if n >= size:
            return in_words(n // size) + ' ' + name + (' ' + in_words(n % size) if n % size else '')


def grouped(m):
    """a number written with thousands separators, in words. Given "4,712 units" in digits the voice said "four, seven
    twelve" (heard as "for 712"; the same sentence in words came back right), and a wrong number is the worst error
    a study guide can make aloud. A year has no comma and is left to the voice."""
    words = in_words(int(m.group(1).replace(',', '')))
    return words + (' point ' + ' '.join(DIGITS[int(c)] for c in m.group(2)) if m.group(2) else '')


GROUPED = re.compile(r'(?<![\d.,])(\d{1,3}(?:,\d{3})+)(?:\.(\d+))?(?![\d,]*\d)')


def swaps():
    f = HERE / 'narration' / 'say.json'
    return [(k, v) for k, v in json.loads(f.read_text(encoding='utf8')).items() if not k.startswith('_')] if f.exists() else []


def say(text):
    """page text read as written: symbols, abbreviations and numerals turned into the words a person would say"""
    for k, v in sorted(swaps(), key=lambda kv: -len(kv[0])):
        text = re.sub(r'(?<![A-Za-z])' + re.escape(k) + r'(?![A-Za-z])', v, text)
    text = ROMAN.sub(lambda m: m.group(0) if roman(m.group(3)) is None else m.group(1) + m.group(2) + str(roman(m.group(3))), text)
    while True:                                 # "CN IX and X": the numerals after the first are numbers too
        new = ROMAN_NEXT.sub(lambda m: m.group(0) if roman(m.group(2)) is None else m.group(1) + str(roman(m.group(2))), text)
        if new == text:
            break
        text = new
    text = re.sub(r'[₀-₉]+', lambda m: ' ' + ' '.join(str(ord(c) - 0x2080) for c in m.group(0)) + ' ', text)       # V₁ is "V one", CO₂ "C O two"
    text = re.sub(r'[%s]' % ''.join(GREEK), lambda m: GREEK[m.group(0)], text)
    text = re.sub(r'(?<![\d.,])0\.(\d+)(?![\d])', lambda m: 'point ' + ' '.join(DIGITS[int(c)] for c in m.group(1)), text)   # 0.06 is "point zero six"
    text = re.sub(r'\$\s+(?=\d)', '$', text)                                    # "$ 600" in a table cell
    text = re.sub(r'(?<=\d)\((\d[\d,.]*)\)', r' times \1', text)                # 700(40) is "700 times 40"
    text = re.sub(r'(?<=[\d)a-z])\s*\+\s*(?=[\d($])', ' plus ', text)            # 28,000+2,600
    text = re.sub(r'(?<![\w)])\+(?=\d)', 'plus ', text)                          # +200 in a table
    text = re.sub(r'#\s*of\b', 'Number of', text)
    text = re.sub(r'#(?=\d)', 'number ', text)
    text = re.sub(r'(?<=[A-Za-z])\s/\s(?=[A-Za-z])', ' or ', text)                # Hiring / Layoffs
    text = re.sub(r'(?<=\d)\s*lbs?\.(?=\s+[A-Z])', ' pounds.', text)
    text = re.sub(r'(?<=\d)\s*lbs?\b\.?', ' pounds', text)
    for a, b in SAY:
        text = re.sub(a, b, text)
    text = GROUPED.sub(grouped, text)
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'\s+([,.;:)])', r'\1', text)
    return re.sub(r'\.\s*\.', '.', text)


def nums(text):
    return {n.replace(',', '').rstrip('.') for n in re.findall(r'\d[\d,]*(?:\.\d+)?', text)}


def check(script, source, where):
    """rule 3 and rule 4, mechanically: no number the page does not print here, and no mention of a source"""
    extra = nums(script) - nums(source)
    assert not extra, '%s: the script says %s, which this part of the page does not print' % (where, sorted(extra))
    low = script.lower()
    for b in BANNED:
        assert b not in low, '%s: the script mentions "%s"' % (where, b)


# ---------------------------------------------------------------- voice
def _voice(sentence, speed):
    """one sentence -> samples at RATE. The only function that knows which voice is used."""
    global _kokoro
    CACHE.mkdir(parents=True, exist_ok=True)
    if ENGINE == 'google':
        import voice_google
        import pronounce
        text = sentence.replace(LETTER, 'A')
        hard, unknown = pronounce.for_text(text)
        for phrase, ipa, entry in hard:
            TAUGHT.setdefault(phrase.lower(), (ipa, entry))
        UNKNOWN.update(unknown)
        told = ''.join('|%s=%s' % (ph.lower(), ipa) for ph, ipa, _ in sorted(hard))       # a take is re-recorded when what it is told changes
        f = CACHE / (hashlib.sha1(('google|%s|%.2f|%s%s' % (VOICE, speed, text, told)).encode()).hexdigest()[:20] + '.npy')
        if not f.exists():
            np.save(f, voice_google.synthesize(text, VOICE, speed, [(ph, ipa) for ph, ipa, _ in hard]))
        return np.load(f)
    assert ENGINE == 'kokoro', 'NARRATE_ENGINE must be kokoro or google, not %r' % ENGINE
    model = next((KOKORO / n for n in ('kokoro-v1.0.onnx', 'kokoro-v1.0.int8.onnx') if (KOKORO / n).exists()), None)
    say_with = g2p() if model else None
    f = CACHE / (hashlib.sha1(('%s|%.2f|%s|%s' % (VOICE, speed, 'misaki2' if say_with else 'espeak', sentence)).encode()).hexdigest()[:20] + '.npy')
    if f.exists():
        return np.load(f)
    if model:
        from kokoro_onnx import Kokoro
        _kokoro = _kokoro or Kokoro(str(model), str(KOKORO / 'voices-v1.0.bin'))
        if say_with:
            samples, rate = _kokoro.create(phonemes(sentence, say_with), voice=VOICE, speed=speed, is_phonemes=True)
        else:
            samples, rate = _kokoro.create(sentence.replace(LETTER, 'eigh'), voice=VOICE, speed=speed, lang='en-us')
        assert rate == RATE
    else:                                   # no model on this machine: the basic system voice, so a build still completes
        import soundfile
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(['pico2wave', '-l', 'en-US', '-w', tmp + '/a.wav', sentence.replace(LETTER, 'A')], check=True)
            subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', tmp + '/a.wav', '-ar', str(RATE), tmp + '/b.wav'], check=True)
            samples, _ = soundfile.read(tmp + '/b.wav', dtype='float32')
    samples = np.asarray(samples, dtype=np.float32)
    np.save(f, samples)
    return samples


def learn(text):
    """look up, once and before anything is recorded, the hard words in what is about to be read"""
    import pronounce
    said = pronounce.prepare(re.sub(r'<(script|style)\b.*?</\1>|<[^>]+>', ' ', text, flags=re.S))
    if said:
        print('          ' + said)


def paragraphs(text):
    return [p.strip() for p in text.split('\n') if p.strip()]


TAKES = []        # every paragraph recorded in this run, for the listening check: (where, as written, samples)
TAUGHT = {}       # hard word as written, lower case -> (IPA, where it came from): what the voice was told in this run
UNKNOWN = set()   # rare words no source has a pronunciation for: the voice guessed


def speak(text, where='', speed=1.0, beat=0.35):
    """a passage -> samples. A line break in the text starts a new take after a short beat."""
    out = []
    for par in paragraphs(text):
        take = _voice(prep(par), speed)
        TAKES.append((where, par, take))
        out += [take, np.zeros(int(beat * RATE), dtype=np.float32)]
    return np.concatenate(out) if out else np.zeros(1, dtype=np.float32)


def listening_check(page_name, report_dir):
    """transcribe everything recorded for this page and report what does not match its script"""
    if ENGINE == 'google':
        import voice_google
        print('          ' + voice_google.summary())
    if not report_dir:
        return
    import hear
    if not hear.available():
        print('          listening check skipped: no speech-recognition model on this machine (see hear.py)')
        return
    found = hear.audit(TAKES)
    words = hear.word_list(TAUGHT, UNKNOWN)
    # each word that did not come from the built-in dictionary, said once on its own: the ones worth a person's ear
    said = [(w, _voice(prep(w.capitalize() + '.'), 1.0)) for w, ipa, (_, source, _) in words if source != 'dictionary'] if ENGINE == 'google' else []
    wrong, terms, reel, minutes = hear.report(page_name, TAKES, found, report_dir, words, said)
    if words:
        print('          hard words: %d looked up and taught to the voice, %d with no pronunciation found (left to the voice)'
              % (sum(1 for w in words if w[1]), sum(1 for w in words if not w[1])))
    print('          listening check: %d of %d takes heard exactly as written; %d with a word or number that may be wrong; '
          '%d names or terms to hear once (%.1f of %.1f minutes to listen to)' % (len(TAKES) - len(found), len(TAKES), wrong, terms, reel, minutes))


def encode(samples):
    """samples -> {'s': data URI of an MP3, 'd': seconds}"""
    import soundfile
    with tempfile.TemporaryDirectory() as tmp:
        soundfile.write(tmp + '/a.wav', samples, RATE)
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', tmp + '/a.wav', '-af', 'loudnorm=I=-18:TP=-2',
                        '-ac', '1', '-ar', str(RATE), '-b:a', '32k', tmp + '/a.mp3'], check=True)
        data = pathlib.Path(tmp + '/a.mp3').read_bytes()
    return {'s': 'data:audio/mpeg;base64,' + base64.b64encode(data).decode(), 'd': round(len(samples) / RATE, 2)}


def host_audio(data, page_name, folder, base_url):
    """take each section's audio out of the page and write it as a file, to be served from a bucket. The page then holds
    only the addresses, and is a few hundred KB instead of 13 MB. A file's name carries a fingerprint of its contents, so
    a re-recorded section gets a new address and no browser plays a stale copy. -> (files, bytes)"""
    import urllib.parse
    stem = pathlib.Path(page_name).stem
    out = pathlib.Path(folder) / stem
    out.mkdir(parents=True, exist_ok=True)
    for old in out.glob(stem + '-*.mp3'):               # this page's files from an earlier build
        old.unlink()
    total = 0
    for n, c in enumerate(data, 1):
        raw = base64.b64decode(c['s'].split(',', 1)[1])
        name = '%s-%d-%s.mp3' % (stem, n, hashlib.sha1(raw).hexdigest()[:8])
        (out / name).write_bytes(raw)
        c['s'] = '%s/%s/%s' % (base_url.rstrip('/'), urllib.parse.quote(stem), name)
        total += len(raw)
    return len(data), total


def script_for(page_name):
    f = HERE / 'narration' / (pathlib.Path(page_name).stem + '.json')
    if not f.exists():
        return {}
    d = json.loads(f.read_text(encoding='utf8'))
    if 'steps_from' in d:                   # another edition of the chapter carries the same widget: use its step scripts
        d['steps'] = json.loads((HERE / 'narration' / (d['steps_from'] + '.json')).read_text(encoding='utf8'))['steps']
    return d


def inject(page_html, tag_id, data, extra='', attrs=''):
    assert page_html.count('</body>') == 1 and ('id="%s"' % tag_id) not in page_html
    block = '<script type="application/json" id="%s"%s>%s</script>\n%s' % (tag_id, attrs, json.dumps(data).replace('</', '<\\/'), extra)
    return page_html.replace('</body>', block + '</body>')


# ---------------------------------------------------------------- steps: one clip per step of every stepper
WALK = '''() => window.__pv.players.map(p => {
  while (!p.back.disabled) p.back.click();
  const out = [];
  for (;;) { out.push(window.__pv.spoken(p.root.querySelector(p.k.cap))); if (p.next.disabled) break; p.next.click(); }
  while (!p.back.disabled) p.back.click();
  const t = p.root.querySelector('.pm-title, .tp-title');
  return { title: t ? t.textContent.trim() : '', steps: out }; })'''


def narrate_steps(path, report_dir=None):
    sys.path.insert(0, str(HERE.parent))
    from mobile_check import launch_kwargs
    from playwright.sync_api import sync_playwright
    path = pathlib.Path(path).resolve()
    with sync_playwright() as pw:
        b = pw.chromium.launch(**launch_kwargs())
        pg = b.new_page()
        pg.goto(path.as_uri())
        pg.wait_for_function('window.__pv && window.__pv.players.length > 0', timeout=30000)
        widgets = pg.evaluate(WALK)
        b.close()
    written = script_for(path.name).get('steps', {})
    learn(json.dumps(written, ensure_ascii=False))
    unused = set(written) - {w['title'] for w in widgets}
    assert not unused, 'scripts for widgets this page does not have: %s' % sorted(unused)
    data, as_written = [], []
    for w in widgets:
        lines = written.get(w['title'])
        if lines is None:
            as_written.append(w['title'])
            data.append([encode(speak(say(c), '%s, step %d' % (w['title'], i + 1))) for i, c in enumerate(w['steps'])])
            continue
        assert len(lines) == len(w['steps']), '%s: %d scripts for %d steps' % (w['title'], len(lines), len(w['steps']))
        for i, (line, cap) in enumerate(zip(lines, w['steps'])):
            check(line, cap, '%s, step %d' % (w['title'], i + 1))
        data.append([encode(speak(line, '%s, step %d' % (w['title'], i + 1))) for i, line in enumerate(lines)])
    path.write_text(inject(path.read_text(encoding='utf8'), 'pv-audio', data), encoding='utf8')
    print('narrated', path.name, len(data), 'widgets,', sum(len(w) for w in data), 'steps, %.0f s of audio' % sum(c['d'] for w in data for c in w),
          ('(read as written: %s)' % ', '.join(as_written)) if as_written else '')
    listening_check(path.name, report_dir)


# ---------------------------------------------------------------- listen: one clip per section of any notes page
SKIP_TAGS = {'script', 'style', 'noscript', 'table', 'iframe', 'button', 'svg', 'figure', 'summary'}
SKIP_CLASS = re.compile(r'\b(video-section|download-section|pertw|pmw|tpw|sdg|toc-box|date|hp10)\b')
VOID = {'img', 'br', 'hr', 'input', 'meta', 'link', 'source', 'col', 'wbr'}
HEAD = re.compile(r'<(h[12])\b[^>]*>(.*?)</\1>', re.S)
# a list item's block is its own text, up to any list nested inside it, so a nested item is found by its own words
BLOCK = re.compile(r'<(tr|p|h3|h4)\b[^>]*>(.*?)</\1>|<(li)\b[^>]*>((?:(?!<li\b|</li>|<ul\b|<ol\b).)*)', re.S)


class Sections(HTMLParser):
    """The page's h1/h2 sections as plain reading text, for a page with no script: tables, widgets and videos are left out."""
    def __init__(self):
        super().__init__()
        self.secs, self.skip, self.inhead, self.body = [], 0, False, False

    def handle_starttag(self, tag, attrs):
        if tag == 'body':
            self.body = True
        if tag in VOID:
            return
        if self.skip:
            self.skip += 1
            return
        if tag in SKIP_TAGS or SKIP_CLASS.search(dict(attrs).get('class') or ''):
            self.skip = 1
        elif tag in ('h1', 'h2'):
            self.secs.append({'level': tag, 'title': '', 'text': ''})
            self.inhead = True

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if self.skip:
            self.skip -= 1
            return
        if tag in ('h1', 'h2'):
            self.inhead = False
        elif tag in ('p', 'li', 'h3', 'h4', 'div') and self.secs and not self.secs[-1]['text'].rstrip().endswith(('.', ':', '?', '!')):
            self.secs[-1]['text'] = self.secs[-1]['text'].rstrip() + '. '

    def handle_data(self, data):
        if self.skip or not self.body or not self.secs:
            return
        self.secs[-1]['title' if self.inhead else 'text'] += data


def unmath(text):
    """LaTeX in the running text, turned into words a voice can read."""
    for _ in range(4):
        text = re.sub(r'\\d?frac\{([^{}]*)\}\{([^{}]*)\}', r' \1 divided by \2 ', text)
        text = re.sub(r'\\(?:text|mathrm|textbf|mathbf)\{([^{}]*)\}', r'\1', text)
        text = re.sub(r'\\sqrt\{([^{}]*)\}', r' the square root of \1 ', text)
    for a, b in ((r'\\times', ' times '), (r'\\div', ' divided by '), (r'\\cdot', ' times '), (r'\\%', ' percent'), (r'\\\$', '$'),
                 (r'\\(?:sigma)', ' sigma '), (r'\\(?:mu)', ' mu '), (r'\\[()\[\]]', ' '), (r'\\[a-zA-Z]+', ' '), (r'[{}]', ' '), (r'\^2', ' squared'), (r'_', ' ')):
        text = re.sub(a, b, text)
    return text


def plain(fragment):
    """HTML -> the text a reader sees, table cells separated by ' | '"""
    t = re.sub(r'</?(?:b|strong|em|i|span|a|u|sub|sup)\b[^>]*>', '', fragment)      # inline tags leave no gap: <b>Term</b>: stays Term:
    t = re.sub(r'</t[dh]>', ' | ', t)
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', t))).strip()


WIDGET_PARTS = re.compile(r'class="[^"]*\b(?:tp|pt|pm|sdg|hp)-|class="[^"]*\bdate\b')
STOP = set('the a an and or of to in on at by for with from is are was were be it its this that these those as than then so but not no '
           'can may will each per which who whom into over under only also such etc via'.split())


def content_words(text):
    return {w for w in re.findall(r'[a-z]{3,}', text.lower()) if w not in STOP}


def coverage(block, said):
    """share of the block's words the passage also uses, comparing the first four letters (Jan / January, cost / costs)"""
    want, got = content_words(block), content_words(said)
    if len(want) < 3:
        return 1.0                      # a row of numbers: the number check already covers it
    return sum(1 for w in want if any(g.startswith(w[:4]) or w.startswith(g[:4]) for g in got)) / len(want)


def listen_scripted(s, written, summary=False, group=None):
    """-> (the page with each spoken-about block tagged data-ls, the clips, a list of thin passages to review)
    summary=True is a declared condensed narration ("mode": "summary" in the script), for a Full edition that would run
    45 minutes if everything were spoken: a block may go unspoken and not every number is said. What is said must still
    be on the page.
    group=('h1',) gives one clip per h1 with the h2 sections inside it, and each heading is spoken (and its words
    highlighted) as the listener reaches it, so someone who is not looking at the page knows where they are."""
    masked = re.sub(r'<(script|style|noscript)\b.*?</\1>', lambda m: ' ' * len(m.group(0)), s, flags=re.S)
    body = masked.index('<body')
    heads = [h for h in HEAD.finditer(masked) if h.start() > body]
    parts = []          # (index of the heading among those the audio is divided at, title, samples, seg) per narrated heading
    titles = [plain(h.group(2)) for h in heads]
    assert set(titles) == set(written), 'headings without a script: %s; scripts without a heading: %s' % (
        sorted(set(titles) - set(written)), sorted(set(written) - set(titles)))
    tags, data, thin, gap = {}, [], [], np.zeros(int(0.15 * RATE), dtype=np.float32)
    spoken = on_page = seen = touched = 0
    for k, h in enumerate(heads):
        end = heads[k + 1].start() if k + 1 < len(heads) else masked.index('</body>')
        title, passages = titles[k], written[titles[k]]
        if not passages:                                    # "Glossary": [] -- declared as not narrated; the bar goes on to the next section
            continue
        # the blocks a reader sees in this section; a block that is part of a widget's own chrome is not narrated line by line
        blocks = [dict(at=m.start(), tag=m.group(1) or m.group(3), text=plain(m.group(2) or m.group(4) or ''), head='<th' in (m.group(2) or ''), said='')
                  for m in BLOCK.finditer(masked, h.end(), end) if not WIDGET_PARTS.search(masked[m.start():masked.index('>', m.start())])]
        widgets = {m.group(1): m.start() for m in re.finditer(r'<div class="(tpw|pertw|pmw|sdg)\b', masked[h.end():end])}
        configs = ' '.join(re.findall(r'<script type="application/json">(.*?)</script>', s[h.end():end], flags=re.S))   # a widget's own numbers
        check(' '.join(p[1] for p in passages), plain(masked[h.end():end]) + ' ' + configs, title)
        audio, seg, at = [], [], 0
        if group:
            part = np.concatenate([speak(say(title).rstrip(':.') + '.', title, speed=LISTEN_SPEED, beat=0.25), gap])
            seg.append([0, [tags.setdefault(h.start(), len(tags))]])
            audio.append(part)
            at += len(part)
        for anchors, text in passages:
            bids = []
            for anchor in ([anchors] if isinstance(anchors, str) else anchors):     # one passage may speak for several blocks
                if anchor.startswith('@'):                  # a passage about a whole widget: "@pertw"
                    assert anchor[1:] in widgets, '%s: no %s widget in this section' % (title, anchor[1:])
                    bids.append(tags.setdefault(h.end() + widgets[anchor[1:]], len(tags)))
                    on_page += 90                           # a widget's content is not in the page's text, so it earns its own words
                elif anchor:
                    hit = [b for b in blocks if anchor in b['text']]
                    assert hit, '%s: nothing in this section contains "%s"' % (title, anchor)
                    hit[0]['said'] += ' ' + text
                    bids.append(tags.setdefault(hit[0]['at'], len(tags)))
            part = np.concatenate([speak(text, title, speed=LISTEN_SPEED, beat=0.25), gap])
            seg.append([round(at / RATE, 2), bids])
            audio.append(part)
            at += len(part)
        seen += sum(1 for b in blocks if b['tag'] in ('li', 'p', 'tr') and b['text'].strip(' |'))
        touched += sum(1 for b in blocks if b['said'])
        for b in blocks:                                    # nothing a reader sees goes unspoken
            if summary or b['tag'] not in ('li', 'p', 'tr') or not b['text'].strip(' |'):
                continue
            assert b['said'], '%s: no passage for this %s: "%s"' % (title, b['tag'], b['text'][:90])
            missing = nums(b['text']) - nums(b['said'])
            assert not missing, '%s: the passage for "%s" never says %s' % (title, b['text'][:60], sorted(missing))
            if b['head']:                                   # a table is introduced by naming its columns
                cols = [c for c in (x.strip() for x in b['text'].split('|')) if c]
                unnamed = [c for c in cols if not all(w.lower() in b['said'].lower() for w in re.findall(r'[A-Za-z]{3,}', c))]
                assert not unnamed, '%s: the table introduction does not name the column(s) %s' % (title, unnamed)
            else:
                got = coverage(b['text'], b['said'])
                if got < 0.5:
                    thin.append('%s | %d%% of its words | %s' % (title, round(got * 100), b['text'][:80]))
        parts.append((k, title, np.concatenate(audio), seg))
        spoken += sum(len(p[1].split()) for p in passages)
        on_page += len(plain(masked[h.end():end]).split())
    # listening must not take longer than reading: the script may not outgrow the text it speaks for
    print('          %d words spoken for %d words on the page (%d%%)' % (spoken, on_page, round(100 * spoken / max(on_page, 1)))
          + ('; condensed narration, %d of %d paragraphs and bullets referenced' % (touched, seen) if summary else ''))
    assert spoken <= 1.2 * on_page, 'the script is %d words for %d words of page: over the 120%% budget, tighten it' % (spoken, on_page)
    if group:                                               # one clip per heading of the chosen level, the sections under it joined on
        tops = [k for k, h in enumerate(heads) if h.group(1) in group]
        for n, top in enumerate(tops):
            mine = [p for p in parts if top <= p[0] < (tops[n + 1] if n + 1 < len(tops) else len(heads))]
            if not mine:
                continue
            audio, seg, at = [], [], 0
            for _, _, samples, sg in mine:
                seg += [[round(t + at / RATE, 2), bids] for t, bids in sg]
                audio.append(samples)
                at += len(samples)
            data.append(dict(encode(np.concatenate(audio)), h=n, t=titles[top], seg=seg))
    else:
        data = [dict(encode(samples), h=k, t=title, seg=seg) for k, title, samples, seg in parts]
    for start in sorted(tags, reverse=True):                 # tag each block, last first so the offsets stay true
        close = s.index('>', start)
        s = s[:close] + ' data-ls="%d"' % tags[start] + s[close:]
    return s, data, thin


def takes(text, limit=480):
    """a long paragraph, cut into takes of a few sentences each, so no single recording is a minute long"""
    out, cur = [], ''
    for sent in sentences(text):
        if cur and len(cur) + len(sent) > limit:
            out.append(cur)
            cur = ''
        cur = (cur + ' ' + sent).strip()
    return '\n'.join(out + [cur]) if cur else '\n'.join(out)


BLOCK_H2 = re.compile(BLOCK.pattern.replace('(tr|p|h3|h4)', '(tr|p|h2|h3|h4)'), re.S)      # when the audio is divided at h1 only


SENT = re.compile(r'(?<=[.!?])\s+(?=[A-Z0-9(])')
NOT_AN_END = re.compile(r'(?:^|[\s(])(?:Dr|Mr|Mrs|Ms|Prof|St|vs|Fig|No|ca|cf|approx|e\.g|i\.e|[A-Z])\.$')


def sentences(text):
    """a passage -> its sentences. "Dr. Gillooly" and "E. coli" are not two sentences: the voice does not pause there,
    so a split there puts the highlight a sentence out for the rest of the paragraph."""
    out = []
    for piece in SENT.split(text):
        if out and NOT_AN_END.search(out[-1]):
            out[-1] += ' ' + piece
        else:
            out.append(piece)
    return out


def sentence_starts(samples, sents):
    """when each sentence of a take begins, in seconds, read from the pauses that are actually in the recording.
    Each boundary is first guessed from the share of characters spoken so far, then moved to the nearest real pause."""
    if len(sents) < 2:
        return [0.0]
    dur, fr = len(samples) / RATE, int(0.01 * RATE)
    env = np.sqrt(np.convolve(samples.astype(np.float64) ** 2, np.ones(fr) / fr, 'same'))[::fr]
    quiet, gaps, i = env < 0.035 * env.max(), [], 0
    while i < len(quiet):
        if quiet[i]:
            j = i
            while j < len(quiet) and quiet[j]:
                j += 1
            if i > 0 and j < len(quiet) and (j - i) >= 10:          # a pause of 0.1 s or more, not the silence at either end
                gaps.append((i * 0.01, j * 0.01))
            i = j
        else:
            i += 1
    share, out, first = np.cumsum([len(x) for x in sents]) / sum(len(x) for x in sents), [0.0], 0
    for k in range(len(sents) - 1):
        guess = share[k] * dur
        best = max(((b - a) - 0.07 * abs((a + b) / 2 - guess), n) for n, (a, b) in enumerate(gaps)
                   if n >= first and abs((a + b) / 2 - guess) < 3.0 and b > out[-1] + 0.3) if any(
                   n >= first and abs((a + b) / 2 - guess) < 3.0 and b > out[-1] + 0.3 for n, (a, b) in enumerate(gaps)) else None
        if best:
            first = best[1] + 1
            out.append(round(gaps[best[1]][1], 2))               # the sentence starts where the pause ends
        else:
            out.append(round(max(guess, out[-1] + 0.2), 2))
    return out


def page_ranges(spoken, page, sents):
    """where each spoken sentence sits in the page's own text: (start, end) character offsets.
    The spoken text is the page text with symbols turned into words, so the two are lined up character by character."""
    import difflib
    blocks = difflib.SequenceMatcher(None, spoken, page, autojunk=False).get_matching_blocks()

    def to_page(i):
        for a, b, n in blocks:
            if i < a:
                return b
            if i < a + n:
                return b + (i - a)
        return len(page)
    out, pos = [], 0
    for sent in sents:
        at = spoken.find(sent, pos)
        at = pos if at < 0 else at
        pos = at + len(sent)
        c0, c1 = to_page(at), min(len(page), to_page(pos - 1) + 1)
        while c0 < c1 and page[c0].isspace():
            c0 += 1
        out.append((c0, max(c1, c0)))
    return out


def listen_read(s, levels=('h1', 'h2')):
    """The whole page read as written, with no script: every heading, paragraph, bullet and table row, in page order,
    each one highlighted while it is spoken. For a Full edition, whose text is already in sentences. A table row is read
    with its column names, so a cell is never heard without knowing what it is."""
    masked = re.sub(r'<(script|style|noscript)\b.*?</\1>', lambda m: ' ' * len(m.group(0)), s, flags=re.S)
    body = masked.index('<body')
    heads = [h for h in HEAD.finditer(masked) if h.start() > body and h.group(1) in levels]
    block = BLOCK if 'h2' in levels else BLOCK_H2            # an h2 inside an h1 section is read out as a title, and can be jumped to
    tags, data, gap, spoken = {}, [], np.zeros(int(0.15 * RATE), dtype=np.float32), 0

    def said(blocks):
        cols, out, last = [], [], 0
        for m in blocks:
            if WIDGET_PARTS.search(masked[m.start():masked.index('>', m.start())]):
                continue
            tag, text = m.group(1) or m.group(3), plain(m.group(2) or m.group(4) or '')
            if tag == 'tr':
                if '<table' in masked[last:m.start()]:
                    cols = []                           # a new table: the last one's column names are not this one's
                last = m.end()
                cells = ['none' if re.fullmatch(r'[-–—]+', c.strip()) else c.strip() for c in text.split('|')][:-1]
                if '<th' in (m.group(2) or ''):
                    cols = cells
                    text = 'This table has ' + ('the columns ' + ', '.join(c for c in cols if c) if len([c for c in cols if c]) > 1 else 'one column') + '.'
                elif not cols and len(cells) == 2 and all(cells):
                    text = '%s: %s' % tuple(cells)       # no header row, two columns: a name and its value
                else:
                    text = '. '.join(('%s: %s' % (cols[i], c) if i < len(cols) and cols[i] and i else c) for i, c in enumerate(cells) if c)
            page = text if tag in ('p', 'li', 'h2', 'h3', 'h4') else None      # a block whose words can be followed in the page's own text
            text = say(unmath(text))
            if not re.search(r'[A-Za-z0-9]', text):
                continue
            out.append((m.start(), text if text.endswith(('.', '?', '!', ':')) else text + '.', page))
        return out

    for k, h in enumerate(heads):
        end = heads[k + 1].start() if k + 1 < len(heads) else masked.index('</body>')
        title = plain(h.group(2))
        before = said(block.finditer(masked, body, h.start())) if k == 0 else []      # anything above the first heading is read first
        # the heading is a passage like any other: its words are highlighted while it is read (Ian, 2026-11-18), its box is not restyled
        passages = before + [(h.start(), say(title).rstrip(':.') + '.', title)] + said(block.finditer(masked, h.end(), end))
        audio, seg, at = [], [], 0
        for where, text, page in passages:
            bids = [] if where is None else [tags.setdefault(where, len(tags))]
            start, sents, times, beat = at, [], [], np.zeros(int(0.25 * RATE), dtype=np.float32)
            for par in paragraphs(takes(text)):                 # one recording per few sentences, timed sentence by sentence
                take = _voice(prep(par), LISTEN_SPEED)
                TAKES.append((title, par, take))
                these = sentences(par)
                sents += these
                times += [round(at / RATE + t, 2) for t in sentence_starts(take, these)]
                audio += [take, beat]
                at += len(take) + len(beat)
            audio.append(gap)
            at += len(gap)
            entry = [round(start / RATE, 2), bids]
            if page is not None:                                # [time, start, end] for each sentence, and the length of the text they index
                entry += [[[t, c0, c1] for t, (c0, c1) in zip(times, page_ranges(text, page, sents))], len(page)]
            seg.append(entry)
            spoken += len(text)
        data.append(dict(encode(np.concatenate(audio)), h=k, t=title, seg=seg))
    for start in sorted(tags, reverse=True):
        close = s.index('>', start)
        s = s[:close] + ' data-ls="%d"' % tags[start] + s[close:]
    print('          read as written: %d paragraphs, bullets and rows, %s characters spoken' % (len(tags), format(spoken, ',')))
    return s, data


def narrate_listen(src, out, report_dir=None, read=False, levels=('h1', 'h2'), audio=None, group=None):
    s = pathlib.Path(src).read_text(encoding='utf8')
    learn(s if read else json.dumps(script_for(pathlib.Path(src).name), ensure_ascii=False))
    written = None if read else script_for(pathlib.Path(src).name).get('sections')
    thin = []
    if written:
        s, data, thin = listen_scripted(s, written, summary=script_for(pathlib.Path(src).name).get('mode') == 'summary', group=group)
    else:
        s, data = listen_read(s, levels)
    hosted = host_audio(data, pathlib.Path(out).name, *audio) if audio else None
    extra = '<style>\n' + (HERE / 'listen.css').read_text() + '</style>\n<script>\n' + (HERE / 'listen.js').read_text() + '</script>\n'
    heads_attr = ' data-heads="%s"' % ', '.join(levels if not written else group or ('h1', 'h2'))
    pathlib.Path(out).write_text(inject(s, 'ls-audio', data, extra, heads_attr), encoding='utf8')
    print('listen  ', pathlib.Path(out).name, len(data), 'sections,', sum(len(c.get('seg', [])) for c in data), 'passages,',
          '%.1f min of audio' % (sum(c['d'] for c in data) / 60), '' if written else '(read as written)')
    if hosted:
        print('          audio: %d files, %.1f MB, in %s; the page expects them at %s' % (hosted[0], hosted[1] / 1e6, pathlib.Path(audio[0]) / pathlib.Path(out).stem, audio[1]))
    for t in thin:
        print('          thin passage, worth a read:', t)
    listening_check(pathlib.Path(out).name, report_dir)


if __name__ == '__main__':
    rep = sys.argv[sys.argv.index('--report') + 1] if '--report' in sys.argv else None
    if sys.argv[1] == 'voices':                 # which Google voices this key can use
        import voice_google
        for name, gender in voice_google.voices():
            print(name, gender.lower())
    elif sys.argv[1] == 'sample':               # one clip in the current engine and voice, to compare by ear
        clip = encode(speak(sys.argv[2]))
        pathlib.Path(sys.argv[3]).write_bytes(base64.b64decode(clip['s'].split(',', 1)[1]))
        print('wrote', sys.argv[3], '%.1f s' % clip['d'], 'engine', ENGINE, 'voice', VOICE)
        listening_check(sys.argv[3], None)
    elif sys.argv[1] == 'steps':
        narrate_steps(sys.argv[2], rep)
    else:
        lv = tuple(sys.argv[sys.argv.index('--sections') + 1].split(',')) if '--sections' in sys.argv else ('h1', 'h2')
        # --audio-dir FOLDER --audio-url ADDRESS: write the audio as files for a bucket instead of inside the page
        au = (sys.argv[sys.argv.index('--audio-dir') + 1], sys.argv[sys.argv.index('--audio-url') + 1]) if '--audio-dir' in sys.argv else None
        # for a scripted page, --sections is also what asks for one clip per heading of that level, headings spoken
        narrate_listen(sys.argv[2], sys.argv[3], rep, read='--read' in sys.argv, levels=lv, audio=au, group=lv if '--sections' in sys.argv else None)
