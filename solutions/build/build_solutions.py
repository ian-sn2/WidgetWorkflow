"""Assemble the ECO2023 Exam 1 detailed-solutions page from the uploaded exams,
the written solutions, and the widgets map. Run from the repo root:

    python3 -I build_solutions.py <upload dir> <out file>
"""
import html, json, pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from widgets_f24 import W as WIDGETS_F24
from widgets_rest import W as WIDGETS_REST
from paraphrase import P as PARAPHRASE

U = pathlib.Path(sys.argv[1]); OUT = pathlib.Path(sys.argv[2])
EXAMS = [  # term code, name, exam html, solutions heading, questions to keep
    ("243", "Fall 2024",   "FALL 2024 Midterm 1A.html",  "Fall 2024",   range(1, 31)),
    ("233", "Fall 2023",   "FALL 2023 Midterm 1.html",   "Fall 2023",   range(1, 41)),
    ("232", "Summer 2023", "Summer 2023 Midterm 1.html", "Summer 2023", range(1, 31)),
    ("231", "Spring 2023", "SPRING 2023 Midterm 1.html", "Spring 2023", range(1, 41)),
    ("222", "Summer 2022", "Summer 2022 Midterm 1.html", "Summer 2022", range(1, 31)),
]
WIDGETS = dict(WIDGETS_REST, **{"243": WIDGETS_F24})

# ---------------------------------------------------------------- exams ----
def parse_exam(path):
    h = path.read_text(encoding="utf-8")
    body = h[h.find("<body>"):] if "<body>" in h else h
    toks = re.findall(r"<p>.*?</p>|<blockquote>.*?</blockquote>|<table>.*?</table>", body, re.S)
    qs, cur, pre = {}, None, []
    for t in toks:
        m = re.match(r"<p>(\d+)\) (.*)</p>$", t, re.S)
        if m:
            cur = {"n": int(m.group(1)), "stem": [m.group(2).strip()], "choices": [], "pre": pre}
            qs[cur["n"]] = cur; pre = []; continue
        if cur is None: continue
        c = re.match(r"<p>([A-E])\) (.*)</p>$", t, re.S)
        if c and not pre:
            cur["choices"].append(c.group(2).strip()); continue
        if t.startswith("<table>") or "<img" in t:
            pre.append(t); continue
        if t.startswith("<blockquote>") and not cur["choices"]:
            cur["stem"].append(t); continue
        if not cur["choices"] and t.startswith("<p>") and "____" not in t and len(t) < 400:
            cur["stem"].append(t)
    return qs

def table_html(t):
    rows = re.findall(r"<tr[^>]*>(.*?)</tr>", t, re.S)
    out = []
    for i, r in enumerate(rows):
        cells = re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", r, re.S)
        cells = [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", c)).strip() for c in cells]
        tag = "th" if i == 0 else "td"
        out.append("<tr>" + "".join("<%s>%s</%s>" % (tag, c, tag) for c in cells) + "</tr>")
    return "<table>\n" + "\n".join(out) + "\n</table>"

def stem_html(q):
    parts = []
    for s in q["stem"]:
        if s.startswith("<blockquote>"):
            items = re.findall(r"<p>(.*?)</p>", s, re.S)
            parts.append("<ol class=\"sol-sub\" type=\"i\">" + "".join(
                "<li>%s</li>" % re.sub(r"^(i|ii|iii|iv)\.\s*", "", it.strip()) for it in items) + "</ol>")
        elif s.startswith("<p>"):
            parts.append(s)
        else:
            parts.append("<p>%s</p>" % s)
    return "\n".join(parts)

# ------------------------------------------------------------ solutions ----
def parse_solutions(path):
    s = path.read_text(encoding="utf-8"); body = s[s.find("<body>"):]
    parts = re.split(r"(<h1>.*?</h1>)", body); out = {}
    for i in range(1, len(parts), 2):
        name = re.sub("<.*?>", "", parts[i]).split(" Midterm")[0]
        ol = re.search(r"<ol>(.*?)</ol>", parts[i + 1], re.S).group(1)
        items, depth, start = [], 0, None
        for m in re.finditer(r"<(/?)(li|ol|ul)\b[^>]*>", ol):
            close, tag = m.group(1), m.group(2)
            if tag == "li" and not close and depth == 0: start = m.end()
            if tag in ("ol", "ul"): depth += -1 if close else 1
            if tag == "li" and close and depth == 0 and start is not None:
                items.append(ol[start:m.start()].strip()); start = None
        out[name] = items
    return out

# ---------------------------------------------------------------- topics ----
def topic(text):
    t = re.sub("<.*?>", " ", text).lower()
    if "answer a for this question" in t or "freebie" in t or "email the grader" in t: return "Free Point"
    if re.search(r"\b(import|export|tariff|quota on)\b", t): return "International Trade"
    if re.search(r"\b(tax|taxes|taxed|ceiling|floor|rent control|production quota|minimum wage|subsid|sanction)", t): return "Government Intervention"
    if re.search(r"\b(ppf|production possibilit|production efficient|production inefficient|opportunity cost|capital stock|unattainable|attainable|immigrat)", t): return "The PPF"
    if re.search(r"elastic|total revenue|percent|%", t): return "Elasticity"
    if re.search(r"surplus|deadweight|efficien|marginal social|marginal benefit|marginal cost|invisible hand|fair", t): return "Efficiency and Equity"
    return "Supply and Demand"

# ------------------------------------------------------------------ page ----
HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ECO2023 Exam 1 Detailed Solutions</title>
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

def section(term, exam, q, sol, wmap):
    tp = topic(" ".join(q["stem"]) + " " + " ".join(q["choices"]))
    sid = "eco2023-%s-e%s-q%d" % (term, exam, q["n"])
    pre = []
    for p in q["pre"]:
        if "<img" in p:
            if q["n"] in wmap and wmap[q["n"]][0] == "stem": pre.append(widget(wmap[q["n"]][1]))
            else: pre.append("<!-- FIGURE: %s -->" % html.escape(re.search(r'alt="([^"]*)"', p).group(1) if re.search(r'alt="([^"]*)"', p) else "exam figure"))
        elif p.startswith("<table>"): pre.append('<div class="sol-table">\n' + table_html(p) + "\n</div>")
    # The question in our own words (paraphrase.py), the right choice(s)
    # marked, and the solution in the open: this is a list of worked
    # solutions, not a re-presentation of the paper (Ian, 2026-11-02).
    stem_p, choices_p = PARAPHRASE[term][q["n"]]
    assert len(choices_p) == len(q["choices"]), (term, q["n"])
    body = sol.strip()
    # Summer 2022's solutions start with the letter and no <p>: wrap the run
    # of text before the first block tag, so there is a paragraph to follow.
    if not body.startswith("<p"):
        j = min([k for k in (body.find("<p"), body.find("<ul"), body.find("<ol")) if k >= 0] or [len(body)])
        body = "<p>" + body[:j].strip() + "</p>\n" + body[j:]
    if q["n"] in wmap and wmap[q["n"]][0] == "solution":
        # under the first paragraph (the answer letter and its first sentence)
        i = body.find("</p>")
        assert i >= 0, (term, q["n"])
        i += 4
        body = body[:i] + "\n" + widget(wmap[q["n"]][1]) + body[i:]
    m = re.match(r"\s*(?:<p>)?<strong>\(([a-e](?:,\s*[a-e])*)\)</strong>", sol)
    answer = re.findall(r"[a-e]", m.group(1)) if m else []
    assert answer, (term, q["n"], sol[:60])
    choices = "".join('<li%s>%s</li>' % (' class="sol-right"' if "abcde"[i] in answer else "", c)
                      for i, c in enumerate(choices_p))
    return """<section class="sol" id="%s" data-term="%s" data-exam="%s" data-topic="%s">
<p class="sol-q"><b>Question %d · %s</b></p>
%s<p>%s</p>
<ol class="sol-choices" type="A">%s</ol>
<div class="sol-answer"><p class="sol-answer-k">Solution</p>
%s
</div>
</section>
""" % (sid, term, exam, html.escape(tp), q["n"], tp, ("\n".join(pre) + "\n") if pre else "", stem_p, choices, body)

def main():
    sols = parse_solutions(U / "Detailed Solutions HTML" / "ECO2023-263-Exam1-DetailedSolutions-Full.html")
    out = [HEAD]; count = 0; topics = {}
    for term, name, exam_file, sol_key, keep in EXAMS:
        qs = parse_exam(U / "exam-text" / exam_file)
        items = sols[sol_key]
        assert len(items) == len(list(keep)), (name, len(items), len(list(keep)))
        out.append('<div class="sol-group" data-term="%s" data-exam="1">\n<h2>Exam 1 · %s</h2>\n' % (term, name))
        for n in keep:
            q = qs[n]
            # the "answer A" question every paper ends with is not a question
            if topic(" ".join(q["stem"]) + " " + " ".join(q["choices"])) == "Free Point":
                continue
            sec = section(term, "1", q, items[n - 1], WIDGETS.get(term, {}))
            out.append(sec); count += 1
            topics.setdefault(name, {}).setdefault(topic(" ".join(q["stem"]) + " " + " ".join(q["choices"])), []).append(n)
        out.append("</div>\n")
    out.append("</body>\n</html>\n")
    OUT.write_text("".join(out), encoding="utf-8")
    print("wrote", OUT, count, "questions")
    for name, tp in topics.items():
        print(name, {k: v for k, v in sorted(tp.items())})

main()
