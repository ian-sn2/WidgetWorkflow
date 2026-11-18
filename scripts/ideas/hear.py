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
    t = re.sub(r'(?<=\d)\.(?=\d)', '_', t)                 # keep the decimal point through the punctuation strip
    t = re.sub(r'[^a-z0-9_]+', ' ', t).replace('_', '.')
    out = []
    for w in t.split():
        w = WORDS.get(w, w)
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


def audit(items):
    """items: [(where, paragraph as written, samples)] -> [(where, written, heard, score, diffs, samples)] for the ones to hear"""
    flagged = []
    for where, written, samples in items:
        heard = transcribe(samples)
        score, diffs = compare(written, heard)
        if score < FLAG_BELOW or any(serious(d) for d in diffs):
            flagged.append((where, written, heard, score, diffs, samples))
    return flagged


def report(page_name, items, flagged, folder):
    """a text report of every paragraph that did not match, and one clip of just those paragraphs"""
    import soundfile
    folder = pathlib.Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    stem = pathlib.Path(page_name).stem
    minutes = sum(len(s) for _, _, s in items) / RATE / 60
    lines = ['Automatic listening check: ' + page_name, '',
             '%d paragraphs recorded (%.1f minutes). %d matched their script. %d to listen to (%.1f minutes, in %s).' % (
                 len(items), minutes, len(items) - len(flagged), len(flagged), sum(len(f[5]) for f in flagged) / RATE / 60, stem + '.listen-to-these.mp3'),
             'A paragraph is listed when a number or a content word was heard differently, or fewer than %d%% of its words matched.' % round(FLAG_BELOW * 100),
             'Some of these are the listener mishearing, not the voice: that is what the clip is for.', '']
    for n, (where, written, heard, score, diffs, _) in enumerate(flagged, 1):
        lines += ['%d. %s  (%d%% matched)' % (n, where, round(score * 100)), '   written: ' + written, '   heard:   ' + heard,
                  '   differs: ' + '; '.join('"%s" heard as "%s"' % d for d in diffs), '']
    (folder / (stem + '.listening-check.txt')).write_text('\n'.join(lines), encoding='utf8')
    clip = folder / (stem + '.listen-to-these.mp3')
    if flagged:
        gap = np.zeros(int(0.8 * RATE), dtype=np.float32)
        with tempfile.TemporaryDirectory() as tmp:
            soundfile.write(tmp + '/a.wav', np.concatenate([np.concatenate([f[5], gap]) for f in flagged]), RATE)
            subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', tmp + '/a.wav', '-ac', '1', '-b:a', '48k', str(clip)], check=True)
    elif clip.exists():
        clip.unlink()
    return len(flagged), minutes
