"""Film a step-by-step widget playing itself, and write an MP4.

    python scripts/ideas/record_video.py <page.html> <widget number, from 1> <out.mp4> [--size 1280x720]

The page must carry the Play add-on (build_demos.py adds it). The widget is shown alone on a
16:9 stage, plays every step with its caption, and the recording stops when it reaches the end.
If the page carries recorded narration (narrate.py steps), each clip is laid under its step; otherwise the film is silent.
"""
import base64
import json
import pathlib
import subprocess
import sys
import tempfile
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from mobile_check import launch_kwargs  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

page_path, n, out = pathlib.Path(sys.argv[1]).resolve(), int(sys.argv[2]), sys.argv[3]
w, h = (int(x) for x in (sys.argv[sys.argv.index('--size') + 1] if '--size' in sys.argv else '1280x720').split('x'))

with tempfile.TemporaryDirectory() as tmp, sync_playwright() as pw:
    browser = pw.chromium.launch(**launch_kwargs())
    page = browser.new_context(viewport={'width': w, 'height': h}).new_page()
    page.goto(page_path.as_uri() + '#video=%d' % n)
    page.wait_for_function('window.__pvStarted === true', timeout=30000)
    # frames are taken as fast as the browser gives them, and each is held for exactly as long as it stood
    off = time.time() - page.evaluate('performance.now()') / 1000    # page clock -> wall clock
    frames, t0, tail = [], time.time(), None
    while True:
        f = pathlib.Path(tmp) / ('f%05d.jpg' % len(frames))
        t = time.time()
        page.screenshot(path=str(f), type='jpeg', quality=92)
        frames.append((f, t))
        if tail is None and page.evaluate('window.__pvDone === true'):
            tail = time.time() + 1.5            # hold the finished picture a moment
        if tail is not None and time.time() > tail:
            break
        assert time.time() - t0 < 900, 'the widget never reached its last step'
    log = page.evaluate('window.__pvLog || []')
    clips = page.evaluate('''() => { try { return JSON.parse(document.getElementById("pv-audio").textContent)[%d] } catch (e) { return null } }''' % (n - 1))
    browser.close()
    lst = pathlib.Path(tmp) / 'frames.txt'
    with open(lst, 'w') as fh:
        for i, (f, t) in enumerate(frames):
            nxt = frames[i + 1][1] if i + 1 < len(frames) else t + 0.1
            fh.write("file '%s'\nduration %.3f\n" % (f, nxt - t))
        fh.write("file '%s'\n" % frames[-1][0])
    video = ['-f', 'concat', '-safe', '0', '-i', str(lst)]
    enc = ['-vf', 'fps=24,scale=trunc(iw/2)*2:trunc(ih/2)*2', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '22', '-movflags', '+faststart']
    if clips and log:     # lay each step's recorded clip under the moment that step appeared
        ins, flt = [], []
        for j, (step, t) in enumerate(log):
            f = pathlib.Path(tmp) / ('a%03d.mp3' % j)
            f.write_bytes(base64.b64decode(clips[step]['s'].split(',', 1)[1]))
            ins += ['-i', str(f)]
            flt.append('[%d:a]adelay=%d:all=1[a%d]' % (j + 1, max(0, round((off + t / 1000 - frames[0][1]) * 1000)), j))
        flt.append(''.join('[a%d]' % j for j in range(len(log))) + 'amix=inputs=%d:normalize=0[a]' % len(log))
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error'] + video + ins + ['-filter_complex', ';'.join(flt), '-map', '0:v', '-map', '[a]']
                       + enc + ['-c:a', 'aac', '-b:a', '96k', out], check=True)
    else:
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error'] + video + enc + [out], check=True)
print('wrote', out, round(pathlib.Path(out).stat().st_size / 1024), 'KB')
