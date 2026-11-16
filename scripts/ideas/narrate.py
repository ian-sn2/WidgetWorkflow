"""Recorded narration for a page.

    python scripts/ideas/narrate.py steps   <page with the Play add-on>     one clip per step of every step-by-step widget
    python scripts/ideas/narrate.py listen  <any notes page> <out page>     one clip per h1/h2 section, plus the Listen bar

WHAT IS SAID. The voice does not read the page. It speaks a script written for the ear, kept in
scripts/ideas/narration/<page name>.json (see narration/README.md for how one is written):
    {"steps":    {"<widget title>": ["what to say on step 1", ...]},
     "sections": {"<h1/h2 text>":   [["<words found in the bullet, row or paragraph this is about>", "what to say"], ...]}}
Each section passage names the block it talks about, so the Listen bar can highlight that block and scroll to it.
A page with no script file is read as written (the old behaviour).
Two checks stop the build: every number spoken must be a number in that step or section of the page, and no script
may mention a source.

HOW IT IS SAID. One sentence at a time, each at its own pace (a question slower and followed by a beat, a short
punch-line slower still, a long sentence a little quicker), with a longer pause between passages.

THE VOICE is one function, _voice(). It uses Kokoro, an open-source neural voice that runs offline at no cost per use:
    pip install kokoro-onnx soundfile
    put kokoro-v1.0.onnx and voices-v1.0.bin (kokoro-onnx GitHub releases, "model-files-v1.0") in ~/.cache/kokoro
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


def prep(text):
    """a written script, ready for the voice"""
    text = re.sub(r'[ \t]+', ' ', text).strip()
    for pat in LETTER_A:
        text = pat.sub('eigh', text)
    return text


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
    f = CACHE / (hashlib.sha1(('%s|%.2f|%s' % (VOICE, speed, sentence)).encode()).hexdigest()[:20] + '.npy')
    if f.exists():
        return np.load(f)
    model = next((KOKORO / n for n in ('kokoro-v1.0.onnx', 'kokoro-v1.0.int8.onnx') if (KOKORO / n).exists()), None)
    if model:
        from kokoro_onnx import Kokoro
        _kokoro = _kokoro or Kokoro(str(model), str(KOKORO / 'voices-v1.0.bin'))
        samples, rate = _kokoro.create(sentence, voice=VOICE, speed=speed, lang='en-us')
        assert rate == RATE
    else:                                   # no model on this machine: the basic system voice, so a build still completes
        import soundfile
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(['pico2wave', '-l', 'en-US', '-w', tmp + '/a.wav', sentence.replace('eigh', 'A')], check=True)
            subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', tmp + '/a.wav', '-ar', str(RATE), tmp + '/b.wav'], check=True)
            samples, _ = soundfile.read(tmp + '/b.wav', dtype='float32')
    samples = np.asarray(samples, dtype=np.float32)
    np.save(f, samples)
    return samples


def pace(sentence):
    """-> (speed, pause after in seconds). This is where the delivery stops being even."""
    n = len(sentence.split())
    if sentence.endswith('?'):
        return 0.95, 0.45
    if n <= 4:
        return 0.90, 0.40
    if sentence.endswith('!'):
        return 1.03, 0.30
    if n >= 22:
        return 1.04, 0.30
    return 1.0, 0.28


def speak(text):
    """a passage -> samples, spoken a sentence at a time; a line break in the text is a longer beat"""
    out = []
    for par in [p for p in text.split('\n') if p.strip()]:
        for sent in re.split(r'(?<=[.!?])\s+(?=[A-Z0-9])', par.strip()):
            speed, pause = pace(sent)
            out += [_voice(prep(sent), speed), np.zeros(int(pause * RATE), dtype=np.float32)]
        out.append(np.zeros(int(0.35 * RATE), dtype=np.float32))
    return np.concatenate(out) if out else np.zeros(1, dtype=np.float32)


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


def narrate_steps(path):
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
            data.append([encode(speak(say(c))) for c in w['steps']])
            continue
        assert len(lines) == len(w['steps']), '%s: %d scripts for %d steps' % (w['title'], len(lines), len(w['steps']))
        for i, (line, cap) in enumerate(zip(lines, w['steps'])):
            check(line, cap, '%s, step %d' % (w['title'], i + 1))
        data.append([encode(speak(line)) for line in lines])
    path.write_text(inject(path.read_text(encoding='utf8'), 'pv-audio', data), encoding='utf8')
    print('narrated', path.name, len(data), 'widgets,', sum(len(w) for w in data), 'steps, %.0f s of audio' % sum(c['d'] for w in data for c in w),
          ('(read as written: %s)' % ', '.join(as_written)) if as_written else '')


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


def listen_scripted(s, written):
    """-> (the page with each spoken-about block tagged data-ls, the clips). Every heading needs a script."""
    masked = re.sub(r'<(script|style|noscript)\b.*?</\1>', lambda m: ' ' * len(m.group(0)), s, flags=re.S)
    body = masked.index('<body')
    heads = [h for h in HEAD.finditer(masked) if h.start() > body]
    titles = [plain(h.group(2)) for h in heads]
    assert set(titles) == set(written), 'headings without a script: %s; scripts without a heading: %s' % (
        sorted(set(titles) - set(written)), sorted(set(written) - set(titles)))
    tags, data, gap = {}, [], np.zeros(int(0.5 * RATE), dtype=np.float32)
    for k, h in enumerate(heads):
        end = heads[k + 1].start() if k + 1 < len(heads) else masked.index('</body>')
        blocks = [(m.start(), plain(m.group(2))) for m in BLOCK.finditer(masked, h.end(), end)]
        passages = written[titles[k]]
        check(' '.join(p[1] for p in passages), plain(masked[h.end():end]), titles[k])
        audio, seg, at = [], [], 0
        for anchor, text in passages:
            bid = -1
            if anchor:
                hit = [b for b in blocks if anchor in b[1]]
                assert hit, '%s: nothing in this section contains "%s"' % (titles[k], anchor)
                bid = tags.setdefault(hit[0][0], len(tags))
            part = np.concatenate([speak(text), gap])
            seg.append([round(at / RATE, 2), bid])
            audio.append(part)
            at += len(part)
        data.append(dict(encode(np.concatenate(audio)), h=k, t=titles[k], seg=seg))
    for start in sorted(tags, reverse=True):                 # tag each block, last first so the offsets stay true
        close = s.index('>', start)
        s = s[:close] + ' data-ls="%d"' % tags[start] + s[close:]
    return s, data


def narrate_listen(src, out):
    s = pathlib.Path(src).read_text(encoding='utf8')
    written = script_for(pathlib.Path(src).name).get('sections')
    if written:
        s, data = listen_scripted(s, written)
    else:
        p = Sections()
        p.feed(s)
        data = [dict(encode(speak(say(sec['title'].strip().rstrip(':.') + '. ' + unmath(html.unescape(sec['text']))))), h=i,
                     t=re.sub(r'\s+', ' ', sec['title']).strip()) for i, sec in enumerate(p.secs)]
    extra = '<style>\n' + (HERE / 'listen.css').read_text() + '</style>\n<script>\n' + (HERE / 'listen.js').read_text() + '</script>\n'
    pathlib.Path(out).write_text(inject(s, 'ls-audio', data, extra), encoding='utf8')
    print('listen  ', pathlib.Path(out).name, len(data), 'sections,', sum(len(c.get('seg', [])) for c in data), 'passages,',
          '%.1f min of audio' % (sum(c['d'] for c in data) / 60), '' if written else '(read as written)')


if __name__ == '__main__':
    if sys.argv[1] == 'steps':
        narrate_steps(sys.argv[2])
    else:
        narrate_listen(sys.argv[2], sys.argv[3])
