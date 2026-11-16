"""Build the 2026-11-16 idea demos from the chapter files Ian sent.

    python scripts/ideas/build_demos.py <unpacked SentToClaude folder> <output folder> [--only-play --only-all ...]

1. Play        every step-by-step widget gets a Play button, narration and step motion (add-on only)
2. What-if lab the CPM network can be delayed or crashed by tapping it (one new widget kind)
3. Define      every glossary term in the text is tappable and shows its definition (any page)
4. Listen      any page read aloud section by section from a bar pinned to the bottom (recorded voice)
5. Motion      every MAN4504 widget animated, in all three editions of both chapters (plus the labs)
6. All         one page per chapter carrying every idea that applies to it: the pages to send
Every edit asserts that it landed; nothing else in a chapter is touched.
"""
import html
import json
import subprocess
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
SRC, OUT = Path(sys.argv[1]), Path(sys.argv[2])
PM = '03 - MAN4504 Exam 3 Project Management-DONE-Moved/MAN4504-263-Exam3-Chapter3-ProjectManagement-Full.html'
AP = '02 - MAN4504 Exam 3 Aggregate Planning-DONE-Processed/MAN4504-263-Exam3-AggregatePlanning-OptionA-Stepper/MAN4504-263-Exam3-AggregatePlanning-%s.html'


def read(name):
    return (HERE / name).read_text(encoding='utf8')


def once(s, old, new):
    assert s.count(old) == 1, (s.count(old), old[:70])
    return s.replace(old, new)


def add_play(s):
    block = '<style>\n' + read('play.css') + '</style>\n<script>\n' + read('play.js') + '</script>\n'
    return once(s, '</body>', block + '</body>')


# ---------------------------------------------------------------- 1. Play
def build_play():
    out = OUT / '1-Play-NarratedWalkthrough'
    out.mkdir(parents=True, exist_ok=True)
    for src in (PM, AP % 'FULL'):
        s = add_play((SRC / src).read_text(encoding='utf8'))
        (out / Path(src).name).write_text(s, encoding='utf8')
        print('play  ', Path(src).name)
        subprocess.run([sys.executable, str(HERE / 'narrate.py'), 'steps', str(out / Path(src).name), '--report', str(OUT / 'narration-check')], check=True)


# ---------------------------------------------------------------- 2. What-if lab
def solve(nodes, edges, dur):
    es, ef = {}, {}
    for n in nodes:                      # the chapter's node order is already topological
        es[n] = max([ef[a] for a, b in edges if b == n] or [0])
        ef[n] = es[n] + dur[n]
    T = max(ef.values())
    ls, lf = {}, {}
    for n in reversed(nodes):
        lf[n] = min([ls[b] for a, b in edges if a == n] or [T])
        ls[n] = lf[n] - dur[n]
    return {n: [es[n], ef[n], ls[n], lf[n]] for n in nodes}, T


def with_lab(s):
    """the page with its crash picture turned into the crash lab, and the folded delay lab added under Step 6"""
    # the crash widget the chapter already has: its network, and its two views with their captions
    m = re.search(r'<div class="pmw " data-pm="net">\s*<p class="pm-title">Crashing Activity A by One Week</p>.*?</script>\s*</div>', s, flags=re.S)
    assert m, 'crash widget not found'
    old = json.loads(re.search(r'<script type="application/json">(.*?)</script>', m.group(0), flags=re.S).group(1))
    net = {'nodes': old['net']['nodes'], 'edges': old['net']['edges'], 'vals': old['net']['vals']}
    nodes = list(net['nodes'])
    dur = {n: net['nodes'][n]['d'] for n in nodes}

    # crash data, read from the chapter's own table: activity, normal, crash time, costs, cost per week
    table = s[s.index('<h2>Project Crashing Example'):]
    rows = re.findall(r'<tr>\s*<td>([A-H])</td>\s*<td>(\d+)</td>\s*<td>(\d+)</td>\s*<td>[\d,]+</td>\s*<td>[\d,]+</td>\s*<td>([\d,]+)</td>', table)
    assert len(rows) == 8, rows
    crash = {a: {'min': int(c), 'cost': int(k.replace(',', ''))} for a, n, c, k in rows}
    for a, n, c, k in rows:
        assert int(n) == dur[a], (a, n, dur[a])

    # the solver must reproduce every number the chapter prints, before and after crashing A
    vals, T = solve(nodes, net['edges'], dur)
    assert vals == net['vals'] and T == 15, 'baseline does not match the chapter'
    d2 = dict(dur, A=1)
    vals2, T2 = solve(nodes, net['edges'], d2)
    assert vals2 == old['views'][1]['vals'] and T2 == 14, 'crash A does not match the chapter'
    _, T3 = solve(nodes, net['edges'], dict(d2, G=4))
    assert T3 == 13 and crash['A']['cost'] + crash['G']['cost'] == 2250
    for pair, total in ((('G',), 1500), (('H',), 3000), (('C', 'B'), 3000), (('C', 'D'), 2000), (('E', 'B'), 3000), (('E', 'D'), 2000)):
        dd = dict(d2)
        for p in pair:
            dd[p] -= 1
        assert solve(nodes, net['edges'], dd)[1] == 13 and sum(crash[p]['cost'] for p in pair) == total, pair
    _, Tb = solve(nodes, net['edges'], dict(dur, B=4))
    _, Tbd = solve(nodes, net['edges'], dict(dur, B=4, D=5))
    assert Tb == 15 and Tbd == 16

    crash_cfg = {
        'mode': 'crash', 'net': net, 'crash': crash,
        'intro': old['views'][0]['cap'],
        'presets': [
            {'label': 'Normal times', 'set': {}, 'cap': old['views'][0]['cap']},
            {'label': 'Crash A', 'set': {'A': 1}, 'cap': old['views'][1]['cap']},
            {'label': 'Crash A, then G', 'set': {'A': 1, 'G': 1},
             'cap': "<b class='pm-h'>After crashing A, then G<\\/b>G is on both critical paths, so one more week off G shortens both. The project takes 13 weeks for $750 + $1,500 = $2,250, and A → C → E → G → H and B → D → G → H are both still critical.".replace('<\\/b>', '</b>')},
        ],
    }
    delay_cfg = {
        'mode': 'delay', 'net': net, 'deadline': 16,
        'intro': "<b class='pm-h'>On schedule</b>The project takes 15 weeks. B and D each show 1 week of slack, but it is the same week: they share the path B → D → G → H.",
        'presets': [
            {'label': 'On schedule', 'set': {}},
            {'label': 'B one week late', 'set': {'B': 1},
             'cap': "<b class='pm-h'>B runs 1 week late</b>B's week of slack absorbs it, so the project still takes 15 weeks. But D's slack is gone too: B → D → G → H is now a second critical path."},
            {'label': 'B and D both late', 'set': {'B': 1, 'D': 1},
             'cap': "<b class='pm-h'>B and D each run 1 week late</b>The path they share had only 1 week to give. The second late week pushes the whole project to 16 weeks, and B → D → G → H is the only critical path."},
        ],
    }

    def widget(title, cfg):
        return ('<div class="pmw " data-pm="lab">\n<p class="pm-title">' + title + '</p>\n<div class="pm-body"></div>\n'
                '<script type="application/json">' + json.dumps(cfg, ensure_ascii=False).replace('</', '<\\/') + '</script>\n</div>')

    # (a) the two-view crash picture becomes the crash lab: same two views, same captions, plus free play
    s = s.replace(m.group(0), widget('Crash the Project Yourself', crash_cfg))
    assert 'Crash the Project Yourself' in s
    # (b) a folded-away delay lab under the sentence it lets the reader test
    anchor = 'be delayed a week without delaying the entire project.</p>'
    s = once(s, anchor, anchor + '\n\n<details class="pm-try">\n<summary>Try it <span>&middot; make an activity run late and watch the slack</span></summary>\n'
             + widget('What Happens If an Activity Runs Late?', delay_cfg) + '\n</details>')
    # the new widget kind goes into the page's own engine, and its styles beside the engine's
    s = once(s, '  function boot() {\n    Array.prototype.forEach.call(document.querySelectorAll(\'.pmw[data-pm]\')', read('lab.js') + '  function boot() {\n    Array.prototype.forEach.call(document.querySelectorAll(\'.pmw[data-pm]\')')
    s = once(s, '</head>', '<style>\n' + read('lab.css') + '</style>\n</head>')
    return s


def build_lab():
    out = OUT / '2-WhatIf-Lab'
    out.mkdir(parents=True, exist_ok=True)
    (out / Path(PM).name).write_text(with_lab((SRC / PM).read_text(encoding='utf8')), encoding='utf8')
    print('lab   ', Path(PM).name)


# ---------------------------------------------------------------- 3. Tap to define (works on any notes page)
MAR = '01 - MAR3023 Exam 3 Chapter 22-DONE - Posted/MAR3023-Fall26-Exam3-Chapter22-PERT-DONE/MAR3023-Fall26-Exam3-Chapter22-WithPERT-%s.html'
PMC = PM.replace('-Full.html', '-Concise.html')


def glossary(concise):
    """the chapter's own Glossary table, from its Concise edition -> [[term, definition], ...]"""
    s = (SRC / concise).read_text(encoding='utf8')
    m = re.search(r'<h2[^>]*>\s*Glossary\s*</h2>\s*<table.*?</table>', s, flags=re.S)
    assert m, 'no Glossary table in ' + concise
    def text(x): return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', x))).strip()
    rows = [(text(a), text(b)) for a, b in re.findall(r'<tr>\s*<td[^>]*>(.*?)</td>\s*<td[^>]*>(.*?)</td>\s*</tr>', m.group(0), flags=re.S)]
    assert len(rows) >= 5, rows
    return [[t, d if d.endswith('.') else d + '.'] for t, d in rows]


def add_define(s, concise):
    block = ('<script type="application/json" id="df-terms">' + json.dumps(glossary(concise), ensure_ascii=False).replace('</', '<\\/') + '</script>\n'
             '<style>\n' + read('define.css') + '</style>\n<script>\n' + read('define.js') + '</script>\n')
    return once(s, '</body>', block + '</body>')


def build_define():
    out = OUT / '3-Tap-To-Define'
    out.mkdir(parents=True, exist_ok=True)
    for src, concise in ((MAR % 'Full', MAR % 'Concise'), (PM, PMC), (AP % 'FULL', AP % 'CONCISE')):
        (out / Path(src).name).write_text(add_define((SRC / src).read_text(encoding='utf8'), concise), encoding='utf8')
        print('define', Path(src).name, len(glossary(concise)), 'terms')


# ---------------------------------------------------------------- 4. Listen (works on any notes page)
def build_listen():
    out = OUT / '4-Listen-AnyPage'
    out.mkdir(parents=True, exist_ok=True)
    for src in (MAR % 'Concise', AP % 'CONCISE'):
        subprocess.run([sys.executable, str(HERE / 'narrate.py'), 'listen', str(SRC / src), str(out / Path(src).name), '--report', str(OUT / 'narration-check')], check=True)


# ---------------------------------------------------------------- 5. Motion on every MAN4504 widget, all editions
def build_motion():
    block = '<style>\n' + read('motion.css') + '</style>\n<script>\n' + read('motion.js') + '</script>\n'
    pm_dir = Path(PM).parent
    jobs = [('Project Management', pm_dir / ('MAN4504-263-Exam3-Chapter3-ProjectManagement-%s.html' % e)) for e in ('Full', 'Balanced', 'Concise')]
    jobs += [('Aggregate Planning', Path(AP % e)) for e in ('FULL', 'BALANCED', 'CONCISE')]
    for folder, src in jobs:
        s = (SRC / src).read_text(encoding='utf8')
        labs = 'Crashing Activity A by One Week' in s          # the Concise has no crash picture, so no lab
        if labs:
            s = with_lab(s)
        s = once(s, '</body>', block + '</body>')
        out = OUT / '5-Animated-MAN4504' / folder
        out.mkdir(parents=True, exist_ok=True)
        (out / src.name).write_text(s, encoding='utf8')
        print('motion', src.name, '+ what-if labs' if labs else '')


# ---------------------------------------------------------------- 6. Everything together: the pages to send
def add_motion(s):
    return once(s, '</body>', '<style>\n' + read('motion.css') + '</style>\n<script>\n' + read('motion.js') + '</script>\n</body>')


def build_all():
    """one page per chapter carrying every idea that applies to it"""
    out = OUT / 'ALL-IDEAS-send-these'
    out.mkdir(parents=True, exist_ok=True)
    narrate = str(HERE / 'narrate.py')
    # Project Management, Full: what-if labs + motion + Play with narration + tap to define
    f = out / Path(PM).name
    f.write_text(add_play(add_motion(add_define(with_lab((SRC / PM).read_text(encoding='utf8')), PMC))), encoding='utf8')
    subprocess.run([sys.executable, narrate, 'steps', str(f)], check=True)
    # Aggregate Planning, Concise: Listen with highlighting + motion + Play with narration + tap to define
    f = out / Path(AP % 'CONCISE').name
    f.write_text(add_play(add_motion(add_define((SRC / (AP % 'CONCISE')).read_text(encoding='utf8'), AP % 'CONCISE'))), encoding='utf8')
    subprocess.run([sys.executable, narrate, 'steps', str(f)], check=True)
    subprocess.run([sys.executable, narrate, 'listen', str(f), str(f)], check=True)
    # MAR3023 Chapter 22, Concise: Listen with highlighting + tap to define (it has no step-by-step widget)
    f = out / Path(MAR % 'Concise').name
    f.write_text(add_define((SRC / (MAR % 'Concise')).read_text(encoding='utf8'), MAR % 'Concise'), encoding='utf8')
    subprocess.run([sys.executable, narrate, 'listen', str(f), str(f)], check=True)
    print('all   ', [x.name for x in sorted(out.glob('*.html'))])


ONLY = [a[7:] for a in sys.argv if a.startswith('--only-')]
for name, fn in (('play', build_play), ('lab', build_lab), ('define', build_define), ('listen', build_listen), ('motion', build_motion), ('all', build_all)):
    if not ONLY or name in ONLY:
        fn()
