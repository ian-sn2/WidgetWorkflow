"""Parse the ECO2023 Exam 3 papers (pandoc HTML of the Final Exam .docx files)
and Ian's written solutions. Imported by build_exam3.py; run alone it prints
every question compactly and cross-checks the solutions' letters against the
answer keys."""
import html, pathlib, re, sys

TERMS = [  # code, name, paper, key, heading in the solutions
    ("212", "Summer 2021", "Summer 2021 Final", "Summer 2021 Final Key",  "Summer 2021"),
    ("211", "Spring 2021", "Spring 2021 Final", "Spring 2021 Final Key",  "Spring 2021"),
    ("203", "Fall 2020",   "Fall 2020 Final",   "Fall 2020 Final Keys",   "Fall 2020"),
    ("201", "Spring 2020", "Spring 2020 Final", "Spring 2020 Final Key",  "Spring 2020"),
]

def text(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()

def parse_paper(path):
    h = path.read_text(encoding="utf-8")
    h = h[h.find("<body>"):] if "<body>" in h else h
    h = re.sub(r"</?blockquote>", "", h)
    toks = re.findall(r"<table\b.*?</table>|<p>.*?</p>", h, re.S)
    qs, order, cur, pend = {}, [], None, []
    for t in toks:
        m = re.match(r"<p>(\d+)\) (.*)</p>$", t, re.S)
        if m:
            n = int(m.group(1))
            if n in qs: n = order[-1] + 1          # Summer 2021 prints "20)" twice
            stem = re.sub(r"^(sp21|UFsu21)\s*", "", text(m.group(2)))
            cur = {"n": n, "stem": stem, "choices": [], "pre": pend}
            qs[n] = cur; order.append(n); pend = []
            continue
        c = re.match(r"<p>(?:<mark>)?([A-E])\) (.*)</p>$", t, re.S)
        if c and cur is not None and not pend:
            cur["choices"].append((c.group(1), text(c.group(2)), "<mark>" in t)); continue
        if t.startswith("<table") or "<img" in t:
            pend.append(t); continue
        if cur is not None and not cur["choices"] and not pend:
            s = text(t)
            if s: cur["stem"] += " | " + s
    return qs

def parse_solutions(path):
    s = path.read_text(encoding="utf-8")
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
    body = s[s.find("<body>"):]
    parts = re.split(r"(<h1>.*?</h1>)", body); out = {}
    for i in range(1, len(parts), 2):
        name = text(parts[i]).split(" Midterm")[0]
        seg = parts[i + 1]
        items, depth, start = [], 0, None
        for m in re.finditer(r"<(/?)(li|ol|ul)\b[^>]*>", seg):
            close, tag = m.group(1), m.group(2)
            if tag in ("ol", "ul"):
                depth += -1 if close else 1; continue
            if depth != 1: continue
            if not close: start = m.end()
            elif start is not None: items.append(seg[start:m.start()].strip()); start = None
        out[name] = items
    return out

def answer_of(sol):
    m = re.match(r"\s*(?:<p>)?\s*<strong>\s*\(([a-e](?:,\s*[a-e])*)\)\s*</strong>", sol)
    return re.findall(r"[a-e]", m.group(1)) if m else []

if __name__ == "__main__":
    U = pathlib.Path(sys.argv[1])
    sols = parse_solutions(U / "ECO2023-261-Exam3-DS-Full.html")
    for code, name, paper, key, head in TERMS:
        qs = parse_paper(U / "exam-text" / (paper + ".html"))
        ks = parse_paper(U / "exam-text" / (key + ".html"))
        items = sols[head]
        print("#####", code, name, len(qs), "questions,", len(items), "solutions")
        for n in sorted(qs):
            q = qs[n]; a = answer_of(items[n - 1]) if n - 1 < len(items) else []
            k = [c[0].lower() for c in ks.get(n, {"choices": []})["choices"] if c[2]]
            flag = "" if (not k or k == a) else "   <<< key %s vs solution %s" % (k, a)
            pre = " [PRE: %s]" % ", ".join("table" if p.startswith("<table") else "figure" for p in q["pre"]) if q["pre"] else ""
            print("%d) %s%s" % (n, q["stem"], pre))
            for L, c, _ in q["choices"]: print("   %s) %s" % (L, c))
            print("   => %s%s" % ("".join(a) or "?", flag))
