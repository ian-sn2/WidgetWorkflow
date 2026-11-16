"""Recorded narration for a page.

    python scripts/ideas/narrate.py steps   <page with the Play add-on> [--report DIR]    one clip per step of every stepper
    python scripts/ideas/narrate.py listen  <any notes page> <out page> [--report DIR]    one clip per h1/h2 section + the Listen bar

WHAT IS SAID. The voice does not read the page. It speaks a script written for the ear, kept in
scripts/ideas/narration/<page name>.json (see narration/README.md for how one is written):
    {"steps":    {"<widget title>": ["what to say on step 1", ...]},
     "sections": {"<h1/h2 text>":   [["<words found in the bullet, row or paragraph this is about>", "what to say"], ...]}}
Each section passage names the block it talks about, so the Listen bar can highlight that block and scroll to it.
A page with no script file is read as written (the old behaviour).
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
generic pronouncer that gets the stress of some words wrong ("subcontract"). A word that is still said wrong is fixed
in narration/pronounce.json, as "word": "phonemes".
NARRATE_VOICE picks the voice (default af_heart). For a paid studio voice, replace the body of _voice().
Clips are embedded in the page as data URIs so a demo is one file; in production they would sit on S3 beside the images.
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
CACHE = pathlib.Path(tempfile.gettempdir()) / 'narrate-cache'
KOKORO = pathlib.Path(os.environ.get('KOKORO_DIR', '~/.cache/kokoro')).expanduser()
VOICE = os.environ.get('NARRATE_VOICE', 'af_heart')
RATE = 24000
LISTEN_SPEED = 1.1          # a whole chapter is spoken a little faster than a single step is
_kokoro = None

# ---------------------------------------------------------------- text
# reading a page as written (no script): symbols into words
SAY = [(r'\bES\b', 'early start'), (r'\bEF\b', 'early finish'), (r'\bLS\b', 'late start'), (r'\bLF\b', 'late finish'),
       ('→', ' to '), ('−', ' minus '), ('÷', ' divided by '), ('×', ' times '), ('=', ' equals '), ('≤', ' at most '),
       (r'\$(\d[\d,]*\d|\d)', r'\1 dollars'), (r' \+ ', ' plus '), ('σ', ' sigma '), ('μ', ' mu '), (r'\)\(', ' times '), ('>', ' over '),
       (r'\bwk\b', 'week'), ('--', ' none '), ('&', ' and '), (r'\bvs\.', 'versus'),
       (r'\be\.g\.,?', 'for example,'), (r'\bi\.e\.,?', 'that is,'), ('—', ', '), ('–', ' to '), ('%', ' percent'), ('[“”"]', '')]
# A neural voice reads a lone capital A as the word "a". Where it is a name (Activity A, "A finishes at 2"), spell it
# the way the voice says the letter. A sentence that opens with A followed by an ordinary word keeps the article.
AFTER_LETTER = ('finishes|has|is|and|to|now|cannot|can|was|starts|takes|by|at|crashed|runs|had|or|equals|minus|plus|will|must|'
                'needs|could|would|does|did|were|are|comes|goes|gets|then|with|only|still|also|itself|alone|first|again|\\d')
LETTER_A = [re.compile(r'(?<![.!?:]\s)(?<!^)\bA\b(?!\'s)(?![a-z])'), re.compile(r'\bA\b(?=[,.;:)]|\s+(?:%s)\b)' % AFTER_LETTER)]
BANNED = ('the transcript', 'the lecture', 'the recording', 'on the board', 'the slides', 'his slide', 'the file')


LETTER = 'Aeigh'                        # stands in for a capital A that is a name; phonemes() gives it the letter's sound
_g2p = None


def pronounce_fixes():
    f = HERE / 'narration' / 'pronounce.json'
    return {k: v for k, v in json.loads(f.read_text(encoding='utf8')).items() if not k.startswith('_')} if f.exists() else {}


def prep(text):
    """a written script, ready for the voice: a capital A that is a name is marked as the letter"""
    text = re.sub(r'[ \t]+', ' ', text).strip()
    for pat in LETTER_A:
        text = pat.sub(LETTER, text)
    return text


def phonemes(text, say_with):
    """text -> Kokoro phonemes, word by word, so one word's sound can be set without disturbing its neighbours.
    (misaki's inline [word](/phonemes/) syntax dropped the word after it: the listening check caught a missing 'finish'.)"""
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        _, tokens = say_with(text)
    fixes, out = pronounce_fixes(), []
    for t in tokens:
        p = t.phonemes or ''
        if t.text == LETTER:
            p = 'ˈA'
        elif t.text.lower() in fixes:
            p = fixes[t.text.lower()]
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


def say(text):
    """page text read as written"""
    for a, b in SAY:
        text = re.sub(a, b, text)
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'\s+([,.;:])', r'\1', text)
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
    CACHE.mkdir(exist_ok=True)
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


def paragraphs(text):
    return [p.strip() for p in text.split('\n') if p.strip()]


TAKES = []        # every paragraph recorded in this run, for the listening check: (where, as written, samples)


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
    if not report_dir:
        return
    import hear
    if not hear.available():
        print('          listening check skipped: no speech-recognition model on this machine (see hear.py)')
        return
    flagged = hear.audit(TAKES)
    n, minutes = hear.report(page_name, TAKES, flagged, report_dir)
    print('          listening check: %d of %d paragraphs matched their script; %d to listen to (%.1f of %.1f minutes)' % (
        len(TAKES) - n, len(TAKES), n, sum(len(f[5]) for f in flagged) / RATE / 60, minutes))


def encode(samples):
    """samples -> {'s': data URI of an MP3, 'd': seconds}"""
    import soundfile
    with tempfile.TemporaryDirectory() as tmp:
        soundfile.write(tmp + '/a.wav', samples, RATE)
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', tmp + '/a.wav', '-af', 'loudnorm=I=-18:TP=-2',
                        '-ac', '1', '-ar', str(RATE), '-b:a', '40k', tmp + '/a.mp3'], check=True)
        data = pathlib.Path(tmp + '/a.mp3').read_bytes()
    return {'s': 'data:audio/mpeg;base64,' + base64.b64encode(data).decode(), 'd': round(len(samples) / RATE, 2)}


def script_for(page_name):
    f = HERE / 'narration' / (pathlib.Path(page_name).stem + '.json')
    if not f.exists():
        return {}
    d = json.loads(f.read_text(encoding='utf8'))
    if 'steps_from' in d:                   # another edition of the chapter carries the same widget: use its step scripts
        d['steps'] = json.loads((HERE / 'narration' / (d['steps_from'] + '.json')).read_text(encoding='utf8'))['steps']
    return d


def inject(page_html, tag_id, data, extra=''):
    assert page_html.count('</body>') == 1 and ('id="%s"' % tag_id) not in page_html
    block = '<script type="application/json" id="%s">%s</script>\n%s' % (tag_id, json.dumps(data).replace('</', '<\\/'), extra)
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
BLOCK = re.compile(r'<(li|tr|p|h3|h4)\b[^>]*>(.*?)</\1>', re.S)


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


def listen_scripted(s, written):
    """-> (the page with each spoken-about block tagged data-ls, the clips, a list of thin passages to review)"""
    masked = re.sub(r'<(script|style|noscript)\b.*?</\1>', lambda m: ' ' * len(m.group(0)), s, flags=re.S)
    body = masked.index('<body')
    heads = [h for h in HEAD.finditer(masked) if h.start() > body]
    titles = [plain(h.group(2)) for h in heads]
    assert set(titles) == set(written), 'headings without a script: %s; scripts without a heading: %s' % (
        sorted(set(titles) - set(written)), sorted(set(written) - set(titles)))
    tags, data, thin, gap = {}, [], [], np.zeros(int(0.15 * RATE), dtype=np.float32)
    spoken = on_page = 0
    for k, h in enumerate(heads):
        end = heads[k + 1].start() if k + 1 < len(heads) else masked.index('</body>')
        title, passages = titles[k], written[titles[k]]
        if not passages:                                    # "Glossary": [] -- declared as not narrated; the bar goes on to the next section
            continue
        # the blocks a reader sees in this section; a block that is part of a widget's own chrome is not narrated line by line
        blocks = [dict(at=m.start(), tag=m.group(1), text=plain(m.group(2)), head='<th' in m.group(2), said='')
                  for m in BLOCK.finditer(masked, h.end(), end) if not WIDGET_PARTS.search(masked[m.start():masked.index('>', m.start())])]
        widgets = {m.group(1): m.start() for m in re.finditer(r'<div class="(tpw|pertw|pmw|sdg)\b', masked[h.end():end])}
        configs = ' '.join(re.findall(r'<script type="application/json">(.*?)</script>', s[h.end():end], flags=re.S))   # a widget's own numbers
        check(' '.join(p[1] for p in passages), plain(masked[h.end():end]) + ' ' + configs, title)
        audio, seg, at = [], [], 0
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
        for b in blocks:                                    # nothing a reader sees goes unspoken
            if b['tag'] not in ('li', 'p', 'tr') or not b['text'].strip(' |'):
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
        data.append(dict(encode(np.concatenate(audio)), h=k, t=title, seg=seg))
        spoken += sum(len(p[1].split()) for p in passages)
        on_page += len(plain(masked[h.end():end]).split())
    # listening must not take longer than reading: the script may not outgrow the text it speaks for
    print('          %d words spoken for %d words on the page (%d%%)' % (spoken, on_page, round(100 * spoken / max(on_page, 1))))
    assert spoken <= 1.2 * on_page, 'the script is %d words for %d words of page: over the 120%% budget, tighten it' % (spoken, on_page)
    for start in sorted(tags, reverse=True):                 # tag each block, last first so the offsets stay true
        close = s.index('>', start)
        s = s[:close] + ' data-ls="%d"' % tags[start] + s[close:]
    return s, data, thin


def narrate_listen(src, out, report_dir=None):
    s = pathlib.Path(src).read_text(encoding='utf8')
    written = script_for(pathlib.Path(src).name).get('sections')
    thin = []
    if written:
        s, data, thin = listen_scripted(s, written)
    else:
        p = Sections()
        p.feed(s)
        data = [dict(encode(speak(say(sec['title'].strip().rstrip(':.') + '. ' + unmath(html.unescape(sec['text']))), sec['title'].strip())), h=i,
                     t=re.sub(r'\s+', ' ', sec['title']).strip()) for i, sec in enumerate(p.secs)]
    extra = '<style>\n' + (HERE / 'listen.css').read_text() + '</style>\n<script>\n' + (HERE / 'listen.js').read_text() + '</script>\n'
    pathlib.Path(out).write_text(inject(s, 'ls-audio', data, extra), encoding='utf8')
    print('listen  ', pathlib.Path(out).name, len(data), 'sections,', sum(len(c.get('seg', [])) for c in data), 'passages,',
          '%.1f min of audio' % (sum(c['d'] for c in data) / 60), '' if written else '(read as written)')
    for t in thin:
        print('          thin passage, worth a read:', t)
    listening_check(pathlib.Path(out).name, report_dir)


if __name__ == '__main__':
    rep = sys.argv[sys.argv.index('--report') + 1] if '--report' in sys.argv else None
    if sys.argv[1] == 'steps':
        narrate_steps(sys.argv[2], rep)
    else:
        narrate_listen(sys.argv[2], sys.argv[3], rep)
