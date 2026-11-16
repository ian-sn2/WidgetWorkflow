"""Recorded narration for a page.

    python scripts/ideas/narrate.py steps   <page with the Play add-on>     one clip per step of every step-by-step widget
    python scripts/ideas/narrate.py listen  <any notes page> <out page>     one clip per h1/h2 section, plus the Listen bar

The voice is one function, tts(). Here it is the offline SVOX Pico voice (apt: libttspico-utils), a stand-in.
For a studio voice, replace the body of tts() with one call to a text-to-speech service; nothing else changes.
Clips are embedded in the page as data URIs so a demo is one file; in production they would sit on S3 beside the images.
"""
import base64
import hashlib
import html
import json
import pathlib
import re
import subprocess
import sys
import tempfile
from html.parser import HTMLParser

HERE = pathlib.Path(__file__).parent
CACHE = pathlib.Path(tempfile.gettempdir()) / 'narrate-cache'
SAY = [(r'\bES\b', 'early start'), (r'\bEF\b', 'early finish'), (r'\bLS\b', 'late start'), (r'\bLF\b', 'late finish'),
       ('→', ' to '), ('−', ' minus '), ('÷', ' divided by '), ('×', ' times '), ('=', ' equals '), ('≤', ' at most '),
       (r'\$(\d[\d,]*)', r'\1 dollars'), (r'\bwk\b', 'week'), ('--', ' none '), ('&', ' and '), (r'\bvs\.', 'versus'),
       (r'\be\.g\.,?', 'for example,'), (r'\bi\.e\.,?', 'that is,'), ('—', ', '), ('–', ' to '), ('%', ' percent'), ('[“”"]', '')]


def say(text):
    for a, b in SAY:
        text = re.sub(a, b, text)
    return re.sub(r'\s+', ' ', text).strip()


def tts(text, wav):
    """text -> a WAV file. The only function that knows which voice is used."""
    subprocess.run(['pico2wave', '-l', 'en-US', '-w', str(wav), text], check=True)


def clip(text):
    """-> {'s': data URI of an MP3, 'd': seconds}. Long text is spoken a few sentences at a time and joined."""
    CACHE.mkdir(exist_ok=True)
    key = hashlib.sha1(text.encode()).hexdigest()[:16]
    mp3 = CACHE / (key + '.mp3')
    if not mp3.exists():
        parts, cur = [], ''
        for sent in re.split(r'(?<=[.!?:;])\s+', text):
            if cur and len(cur) + len(sent) > 380:
                parts.append(cur)
                cur = ''
            cur = (cur + ' ' + sent).strip()
        if cur:
            parts.append(cur)
        with tempfile.TemporaryDirectory() as tmp:
            lst = pathlib.Path(tmp) / 'l.txt'
            with open(lst, 'w') as fh:
                for i, part in enumerate(parts):
                    wav = pathlib.Path(tmp) / ('%04d.wav' % i)
                    tts(part, wav)
                    fh.write("file '%s'\n" % wav)
            subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', str(lst),
                            '-af', 'loudnorm=I=-18:TP=-2', '-ac', '1', '-ar', '22050', '-b:a', '32k', str(mp3)], check=True)
    dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(mp3)],
                               capture_output=True, text=True, check=True).stdout)
    return {'s': 'data:audio/mpeg;base64,' + base64.b64encode(mp3.read_bytes()).decode(), 'd': round(dur, 2)}


def inject(page_html, tag_id, data, extra=''):
    assert page_html.count('</body>') == 1 and ('id="%s"' % tag_id) not in page_html
    block = '<script type="application/json" id="%s">%s</script>\n%s' % (tag_id, json.dumps(data).replace('</', '<\\/'), extra)
    return page_html.replace('</body>', block + '</body>')


# ---------------------------------------------------------------- steps: one clip per caption of every stepper
WALK = '''() => window.__pv.players.map(p => {
  while (!p.back.disabled) p.back.click();
  const out = [];
  for (;;) { out.push(window.__pv.spoken(p.root.querySelector(p.k.cap))); if (p.next.disabled) break; p.next.click(); }
  while (!p.back.disabled) p.back.click();
  return out; })'''


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
        scripts = pg.evaluate(WALK)
        b.close()
    data = [[clip(say(t)) for t in widget] for widget in scripts]
    path.write_text(inject(path.read_text(encoding='utf8'), 'pv-audio', data), encoding='utf8')
    secs = sum(c['d'] for w in data for c in w)
    print('narrated', path.name, len(data), 'widgets,', sum(len(w) for w in data), 'steps, %.0f s of audio' % secs)


# ---------------------------------------------------------------- listen: one clip per section of any notes page
SKIP_TAGS = {'script', 'style', 'noscript', 'table', 'iframe', 'button', 'svg', 'figure', 'summary'}
SKIP_CLASS = re.compile(r'\b(video-section|download-section|pertw|pmw|tpw|sdg|toc-box|date|hp10)\b')
VOID = {'img', 'br', 'hr', 'input', 'meta', 'link', 'source', 'col', 'wbr'}


class Sections(HTMLParser):
    """The page's h1/h2 sections as plain reading text: tables, widgets, videos and scripts are left out."""
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


def narrate_listen(src, out):
    s = pathlib.Path(src).read_text(encoding='utf8')
    p = Sections()
    p.feed(s)
    data, words = [], 0
    for i, sec in enumerate(p.secs):
        body = unmath(html.unescape(sec['text']))
        text = say(sec['title'].strip().rstrip(':.') + '. ' + body).replace('. .', '.')
        words += len(text.split())
        data.append(dict(clip(text), h=i, t=re.sub(r'\s+', ' ', sec['title']).strip()))
    extra = '<style>\n' + (HERE / 'listen.css').read_text() + '</style>\n<script>\n' + (HERE / 'listen.js').read_text() + '</script>\n'
    pathlib.Path(out).write_text(inject(s, 'ls-audio', data, extra), encoding='utf8')
    print('listen  ', pathlib.Path(out).name, len(data), 'sections,', words, 'words, %.1f min of audio' % (sum(c['d'] for c in data) / 60))


if __name__ == '__main__':
    if sys.argv[1] == 'steps':
        narrate_steps(sys.argv[2])
    else:
        narrate_listen(sys.argv[2], sys.argv[3])
