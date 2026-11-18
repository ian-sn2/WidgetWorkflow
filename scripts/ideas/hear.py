"""The automatic listener: transcribe recorded narration and compare it with the script.

Nobody should have to listen to twenty minutes of audio to know a page was read correctly. Each recorded paragraph is
run through speech recognition (Whisper small.en, offline) and the words heard are compared with the words written.
Paragraphs that differ are listed in a report and joined into one short clip, so a person hears only those.

It cannot judge tone. It does catch a misread number, a letter read as a word, a dropped or garbled phrase.

Setup once per machine: pip install sherpa-onnx, and unpack sherpa-onnx-whisper-small.en (sherpa-onnx GitHub releases,
"asr-models") into ~/.cache/asr/. Without it the build still runs and says the check was skipped.
"""
import difflib
import hashlib
import json
import os
import pathlib
import re
import subprocess
import tempfile

import numpy as np

MODEL = pathlib.Path(os.environ.get('ASR_DIR', '~/.cache/asr/sherpa-onnx-whisper-small.en')).expanduser()
CACHE = pathlib.Path(os.environ.get('NARRATE_CACHE', '~/.cache/narrate')).expanduser()
RATE = 24000
FLAG_BELOW = 0.93            # share of words that must match before a paragraph is left alone
_rec = None
WORDS = {'zero': '0', 'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5', 'six': '6', 'seven': '7', 'eight': '8', 'nine': '9',
         'ten': '10', 'eleven': '11', 'twelve': '12', 'first': '1st', 'second': '2nd', 'third': '3rd', 'ok': 'okay', 'versus': 'vs'}


def available():
    try:
        import sherpa_onnx  # noqa: F401
    except ImportError:
        return False
    return (MODEL / 'small.en-encoder.int8.onnx').exists()


def _decode(samples):
    global _rec
    import sherpa_onnx
    if _rec is None:
        _rec = sherpa_onnx.OfflineRecognizer.from_whisper(encoder=str(MODEL / 'small.en-encoder.int8.onnx'), decoder=str(MODEL / 'small.en-decoder.int8.onnx'),
                                                           tokens=str(MODEL / 'small.en-tokens.txt'), num_threads=4)
    s = _rec.create_stream()
    s.accept_waveform(RATE, samples.astype('float32'))
    _rec.decode_stream(s)
    return s.result.text.strip()


def transcribe(samples):
    """samples -> the words heard. Whisper takes 30 seconds at most, so a longer take is cut at its quietest moment."""
    CACHE.mkdir(exist_ok=True)
    f = CACHE / ('asr-' + hashlib.sha1(samples.tobytes()).hexdigest()[:20] + '.json')
    if f.exists():
        return json.loads(f.read_text())
    if len(samples) > 27 * RATE:
        lo, hi, win = len(samples) // 3, 2 * len(samples) // 3, int(0.15 * RATE)
        energy = np.convolve(samples[lo:hi] ** 2, np.ones(win) / win, mode='valid')
        cut = lo + int(np.argmin(energy)) + win // 2
        text = transcribe(samples[:cut]) + ' ' + transcribe(samples[cut:])
    else:
        text = _decode(samples)
    f.write_text(json.dumps(text))
    return text


def norm(text):
    """words only, so '105,152 dollars' and '$105,152' and 'two weeks' and '2 weeks' compare equal"""
    t = text.lower()
    t = t.replace('$', ' ')                                 # where the word "dollars" falls is the listener's choice, not an error
    t = re.sub(r'(\d),(?=\d{3})', r'\1', t).replace('%', ' percent').replace('&', ' and ')
    t = re.sub(r"[’']", '', t)
    t = re.sub(r'(?<![\d.])\.(?=\d)', '0.', t)               # ".06" is 0.06
    t = re.sub(r'(?<=\d)\.(?=\d)', '_', t)                 # keep the decimal point through the punctuation strip
    t = re.sub(r'[^a-z0-9_]+', ' ', t).replace('_', '.')
    out = []
    words = [WORDS.get(w, w) for w in t.split()]
    k = 0
    while k < len(words):                                   # "point zero six" and "0.06" are the same number
        if words[k] == 'point' and k + 1 < len(words) and words[k + 1].isdigit() and len(words[k + 1]) == 1:
            j = k + 1
            while j < len(words) and words[j].isdigit() and len(words[j]) == 1:
                j += 1
            head = words.pop(k - 1) if k and words[k - 1].isdigit() else None
            if head is not None:
                k, j = k - 1, j - 1
            words[k:j] = [(head or '0') + '.' + ''.join(words[k + 1:j])]
        k += 1
    for w in words:
        if w in ('dollar', 'dollars'):
            continue
        if re.fullmatch(r'\d+\.\d+', w):
            w = w.rstrip('0').rstrip('.')                  # 0.00 is 0, 4.10 is 4.1
        out.append(w[:-1] if len(w) > 3 and w.endswith('s') and not w[-2].isdigit() else w)      # plurals do not count as errors
    return out


def compare(written, heard):
    a, b = norm(written), norm(heard)
    m = difflib.SequenceMatcher(None, a, b, autojunk=False)
    def stem(ws):
        return re.sub(r'(es|s|e)$', '', ''.join(ws))      # "on to" / "onto", "March's" / "marches": the same sound
    ops = [o for o in m.get_opcodes() if o[0] != 'equal' and stem(a[o[1]:o[2]]) != stem(b[o[3]:o[4]])]
    diffs = [(' '.join(a[i1:i2]) or '(nothing)', ' '.join(b[j1:j2]) or '(nothing)') for op, i1, i2, j1, j2 in ops]
    same = len(a) - sum(i2 - i1 for op, i1, i2, j1, j2 in ops)
    return (same / max(len(a), 1)), diffs


def serious(diff):
    """one wrong number or one wrong content word is worth hearing, however long the paragraph around it"""
    written, heard = diff
    if re.search(r'\d', written + heard):
        return True
    return any(len(w) >= 5 for w in written.split()) or len(written.split()) >= 2


def is_term(diff):
    """a name or technical word the listener spelled its own way (Gillooly as "galloulli", prezygotic as "presygotic"):
    a long word, heard as something starting with the same letter. The voice may well have said it right; a recognizer
    cannot tell, so these are collected and each is heard once, not once per paragraph."""
    w, h = diff[0].replace(' ', ''), diff[1].replace(' ', '')
    if '(' in w + h or re.search(r'\d', w + h):
        return False
    return len(w) >= 6 and w[0] == h[0]


def audit(items):
    """items: [(where, paragraph as written, samples)] -> [(where, written, heard, score, wrong, terms, samples)]
    wrong: differences that look like a wrong word or number. terms: names and technical words spelled differently."""
    found = []
    for where, written, samples in items:
        heard = transcribe(samples)
        score, diffs = compare(written, heard)
        terms = [d for d in diffs if is_term(d)]
        rest = [d for d in diffs if not is_term(d)]
        wrong = [d for d in rest if serious(d)] or (rest if rest and score < FLAG_BELOW else [])
        if wrong or terms:
            found.append((where, written, heard, score, wrong, terms, samples))
    return found


def sentence(written, samples, phrase):
    """the one sentence of a take that contains the phrase, cut out of the recording"""
    import narrate
    sents = narrate.sentences(written)
    starts = narrate.sentence_starts(samples, sents)
    for k, sent in enumerate(sents):
        if phrase in ' '.join(norm(sent)):
            a, b = int(starts[k] * RATE), int(starts[k + 1] * RATE) if k + 1 < len(starts) else len(samples)
            return samples[max(0, a - int(0.05 * RATE)):b]
    return samples


def word_list(taught, unknown):
    """-> [(word, ipa or None, (respelling, source, clip))], the plain word once (cichlid and cichlids are one line)"""
    import pronounce
    rows = {}
    for w, (ipa, entry) in taught.items():
        src = entry['from']
        base = re.search(r', as (\S+) \+ \w+$', src)
        if base:
            w, src = base.group(1), src[:base.start()]
            ipa = pronounce.lookup(w)['ipa']
        rows.setdefault(w, (w, ipa, (pronounce.respell(ipa), src, entry.get('clip'))))
    for w in unknown:
        rows.setdefault(w, (w, None, ('', 'not found', None)))
    order = lambda r: (r[2][1] == 'dictionary', r[1] is None, r[0])          # hand-entered and looked-up words first: those are the ones to hear
    return sorted(rows.values(), key=order)


def report(page_name, items, found, folder, words=(), said=()):
    """a text report, and one clip holding only the sentences a person should hear: each wrong-looking difference, and
    each name or technical term once. -> (wrong, distinct terms, minutes in the clip, minutes recorded)"""
    import soundfile
    folder = pathlib.Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    stem = pathlib.Path(page_name).stem
    minutes = sum(len(x) for _, _, x in items) / RATE / 60
    wrong = [f for f in found if f[4]]
    terms = {}                                  # written term -> [times heard differently, spellings heard, first take it is in]
    for f in found:
        for w, h in f[5]:
            t = terms.setdefault(w, [0, [], f])
            t[0] += 1
            if h not in t[1]:
                t[1].append(h)
    cuts = [sentence(f[1], f[6], d[0]) for f in wrong for d in f[4][:1]] + [sentence(t[2][1], t[2][6], w) for w, t in terms.items()]
    reel = sum(len(c) + int(0.8 * RATE) for c in cuts) / RATE / 60
    clean = len(items) - len(found)
    lines = ['Automatic listening check: ' + page_name, '',
             '%d takes recorded (%.1f minutes). %d were heard exactly as written.' % (len(items), minutes, clean),
             '%d have a word or number that may be wrong. %d names or technical terms were spelled differently by the listener.' % (len(wrong), len(terms)),
             'To listen to: %.1f minutes, in %s (one sentence for each item below, in this order).' % (reel, stem + '.listen-to-these.mp3'), '',
             'WORDS OR NUMBERS THAT MAY BE WRONG', '']
    for n, (where, written, heard, score, wr, _, _) in enumerate(wrong, 1):
        lines += ['%d. %s' % (n, where), '   written: ' + written, '   heard:   ' + heard,
                  '   differs: ' + '; '.join('"%s" heard as "%s"' % d for d in wr), '']
    if not wrong:
        lines += ['   none', '']
    lines += ['NAMES AND TECHNICAL TERMS (the listener cannot spell these; hear each once and judge the pronunciation)', '']
    for n, (w, (count, heard, f)) in enumerate(terms.items(), len(wrong) + 1):
        lines.append('%d. %s: heard as %s%s' % (n, w, ', '.join('"%s"' % h for h in heard[:4]), ' (%d times)' % count if count > 1 else ''))
    if not terms:
        lines.append('   none')
    if words:
        new = [w for w in words if w[1] and w[2][1] != 'dictionary']
        known = [w for w in words if w[1] and w[2][1] == 'dictionary']
        lost = [w for w in words if not w[1]]
        lines += ['', 'HARD WORDS: LOOKED UP AND TAUGHT TO THE VOICE', '',
                  'Every rare word was looked up before recording and the voice was told how to say it.',
                  '%d came from the built-in dictionary. %d came from Wiktionary, were built from a prefix and a known word, or were entered by hand:' % (len(known), len(new)),
                  'hear those once in %s (each word said alone, in this order). A wrong one is corrected in' % (stem + '.hard-words.mp3'),
                  'scripts/ideas/narration/pronounce.json and is then right in every chapter.', '']
        for w, ipa, (spelled, src, clip) in new:
            lines.append('   %-18s %-26s /%s/   %s%s' % (w, spelled, ipa, src, '   (recorded clip on Wiktionary: File:%s)' % clip if clip else ''))
        lines += ['', '   from the dictionary: ' + ', '.join('%s (%s)' % (w, sp) for w, _, (sp, _, _) in known)]
        if lost:
            lines += ['', 'NO PRONUNCIATION FOUND: the voice guessed these. They are at the end of the same clip. Add the ones it gets wrong to pronounce.json.', '',
                      '   ' + ', '.join(w for w, _, _ in lost)]
    (folder / (stem + '.listening-check.txt')).write_text('\n'.join(lines) + '\n', encoding='utf8')
    clip = folder / (stem + '.listen-to-these.mp3')
    if cuts:
        gap = np.zeros(int(0.8 * RATE), dtype=np.float32)
        with tempfile.TemporaryDirectory() as tmp:
            soundfile.write(tmp + '/a.wav', np.concatenate([np.concatenate([c, gap]) for c in cuts]), RATE)
            subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', tmp + '/a.wav', '-ac', '1', '-b:a', '48k', str(clip)], check=True)
    elif clip.exists():
        clip.unlink()
    clip = folder / (stem + '.hard-words.mp3')
    if said:
        gap = np.zeros(int(0.6 * RATE), dtype=np.float32)
        with tempfile.TemporaryDirectory() as tmp:
            soundfile.write(tmp + '/a.wav', np.concatenate([np.concatenate([c, gap]) for _, c in said]), RATE)
            subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', tmp + '/a.wav', '-ac', '1', '-b:a', '48k', str(clip)], check=True)
    elif clip.exists():
        clip.unlink()
    return len(wrong), len(terms), reel, minutes
