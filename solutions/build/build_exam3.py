"""Assemble the ECO2023 Exam 3 detailed-solutions page from the papers, the
written solutions, the paraphrases and the widget map. Run from the repo root:

    python3 -I build_exam3.py <upload dir> <out file>
"""
import html, json, pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import exam3_parse as E
from paraphrase3 import P as PARA, TOPIC, FREE
from widgets_ex3 import W as WIDGETS

U = pathlib.Path(sys.argv[1]); OUT = pathlib.Path(sys.argv[2])
EXAM = "3"

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ECO2023 Exam 3 Detailed Solutions</title>
    <link rel="stylesheet" href="https://smokinnotes.s3.us-east-1.amazonaws.com/content/sn25-v6.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Red+Hat+Display:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    <script src="https://smokinnotes.s3.us-east-1.amazonaws.com/studyguide/sn25-v2.js"></script>
    <script>
    MathJax = {
        tex: {
            displayMath: [['\\\\[','\\\\]']],
            inlineMath: [['\\\\(','\\\\)']]
        }
    };
    </script>
    <script async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>
<!--SDG-ENGINE-->
<!--SOL-SHELL-->
</head>
<body>
<h1>Detailed Solutions</h1>
<div class="sol-shell"></div>
"""

def widget(cfg):
    return '<div class="sdg"><script type="application/json">%s</script></div>' % json.dumps(cfg, ensure_ascii=False, separators=(",", ":"))

def table_html(t):
    rows = re.findall(r"<tr[^>]*>(.*?)</tr>", t, re.S)
    out = []
    for i, r in enumerate(rows):
        cells = re.findall(r"<t([hd])([^>]*)>(.*?)</t[hd]>", r, re.S)
        tag = "th" if i == 0 or cells and cells[0][0] == "h" else "td"
        tds = []
        for _, attrs, body in cells:
            span = re.search(r'colspan="(\d+)"', attrs)
            tds.append("<%s%s>%s</%s>" % (tag, ' colspan="%s"' % span.group(1) if span else "", E.text(body), tag))
        out.append("<tr>" + "".join(tds) + "</tr>")
    return '<div class="sol-table">\n<table>\n' + "\n".join(out) + "\n</table>\n</div>"

IMG = re.compile(r'(?:<p>\s*)?<img\b[^>]*eco2023-261-exam3[^>]*>(?:\s*</p>)?', re.S)

def section(term, q, sol, wmap):
    n = q["n"]; tp = TOPIC[term][n]
    sid = "eco2023-%s-e%s-q%d" % (term, EXAM, n)
    w = wmap.get(n)
    pre = []
    for p in q["pre"]:
        if "<img" in p:
            assert w and w[0] == "stem", (term, n)
            pre.append(widget(w[1]))
        elif p.startswith("<table"):
            pre.append(table_html(p))
    stem, choices = PARA[term][n]
    body = sol.strip()
    if not body.startswith("<p"):
        j = min([k for k in (body.find("<p"), body.find("<ul"), body.find("<ol")) if k >= 0] or [len(body)])
        body = "<p>" + body[:j].strip() + "</p>\n" + body[j:]
    # The house format never underlines; the solutions' "Step 1:" labels are
    # already bold, so the underline simply goes.
    body = re.sub(r"</?u>", "", body)
    imgs = IMG.findall(body)
    if w and w[0] == "matrix":
        # The written solution walks the game through five pictures of the
        # grid; the widget steps through the same five, so it takes the first
        # picture's place and the other four go.
        assert len(imgs) == 5, (term, n, len(imgs))
        first = [True]
        def sub(m):
            if first[0]: first[0] = False; return widget(w[1])
            return ""
        body = IMG.sub(sub, body)
    else:
        assert not imgs, (term, n, "unplaced solution images")
    if w and w[0] == "solution":
        i = body.find("</p>"); assert i >= 0, (term, n)
        body = body[:i + 4] + "\n" + widget(w[1]) + body[i + 4:]
    if choices is None:                       # the one short-answer question
        ch_html = ""
    else:
        answer = E.answer_of(sol)
        assert answer, (term, n, sol[:60])
        assert len(choices) == len(q["choices"]), (term, n)
        ch_html = '<ol class="sol-choices" type="A">%s</ol>\n' % "".join(
            '<li%s>%s</li>' % (' class="sol-right"' if "abcde"[i] in answer else "", c) for i, c in enumerate(choices))
    return """<section class="sol" id="%s" data-term="%s" data-exam="%s" data-topic="%s">
<p class="sol-q"><b>Question %d · %s</b></p>
%s%s
%s<div class="sol-answer"><p class="sol-answer-k">Solution</p>
%s
</div>
</section>
""" % (sid, term, EXAM, html.escape(tp), n, tp, ("\n".join(pre) + "\n") if pre else "",
       stem if stem.startswith("<p") else "<p>%s</p>" % stem if "<ol" not in stem else
       "<p>%s</p>%s" % (stem[:stem.find("<ol")], stem[stem.find("<ol"):]), ch_html, body)

def main():
    sols = E.parse_solutions(U / "ECO2023-261-Exam3-DS-Full.html")
    out = [HEAD]; count = 0; nw = 0; topics = {}
    for code, name, paper, key, head in E.TERMS:
        qs = E.parse_paper(U / "exam-text" / (paper + ".html"))
        items = sols[head]
        assert len(items) == len(qs), (name, len(items), len(qs))
        wmap = WIDGETS.get(code, {})
        assert not set(wmap) - set(qs), (code, set(wmap) - set(qs))
        out.append('<div class="sol-group" data-term="%s" data-exam="%s">\n<h2>Exam %s · %s</h2>\n' % (code, EXAM, EXAM, name))
        for n in sorted(qs):
            if n == FREE[code]: continue          # the "answer A" point each paper ends with
            out.append(section(code, qs[n], items[n - 1], wmap)); count += 1
            nw += n in wmap
            topics.setdefault(name, {}).setdefault(TOPIC[code][n], []).append(n)
        out.append("</div>\n")
    out.append("</body>\n</html>\n")
    OUT.write_text("".join(out), encoding="utf-8")
    print("wrote", OUT, count, "questions,", nw, "widgets")
    for name, tp in topics.items():
        print(name, {k: v for k, v in sorted(tp.items())})

main()
