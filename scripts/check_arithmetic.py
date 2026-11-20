#!/usr/bin/env python3
"""Recompute every calculation a page writes out, and report the ones that do not add up.

    python scripts/check_arithmetic.py PAGE.html [PAGE.html ...]     # exit 1 on any wrong result
    python scripts/check_arithmetic.py PAGE.html --show              # also list every calculation checked

It reads the page's prose and its LaTeX (\\( \\) and \\[ \\]), finds runs like "2 + 2 + 4 + 5 + 2 = 15",
"[1 + 4(2) + 3] ÷ 6 = 12 ÷ 6 = 2", "(2.33)(1.76) + 15 = 4.10 + 15 = 19.10", "√3.11 = 1.76" or
"\\frac{16 - 15}{1.76} = 0.57", and checks each "=" against the side before it. A stated result passes
when it is the true value rounded to the places it is written with, so "1 ÷ 1.76 = 0.57" passes and
"0.58" would not. Words and variables end a run, so "z = (x − μ)/σ" and "Slack = LS − ES" are skipped:
only arithmetic on written numbers is checked.

Ian, 2026-11-12, after a day of arithmetic slips found by hand in the project management chapter.
It cannot catch a wrong count in words ("seven tasks" for eight); that still needs reading.
"""
import html, math, re, sys

TAG = re.compile(r"<[^>]+>")
SKIP = re.compile(r"<(script|style)\b.*?</\1>|<!--.*?-->", re.S | re.I)


def page_text(src):
    src = SKIP.sub(" ", src)
    src = re.sub(r"<sup>\s*([0-9.]+)\s*</sup>", r"^\1", src)          # (1 ÷ 3)<sup>2</sup>
    src = re.sub(r"<br\s*/?>|</(p|li|td|th|div|h\d|tr)>", "\n", src, flags=re.I)
    return html.unescape(TAG.sub(" ", src))


def tex_to_plain(t):
    t = t.replace("{,}", ",")                                    # 26{,}666.67
    for _ in range(4):   # nested \frac
        t = re.sub(r"\\[dt]?frac\s*\{([^{}]*)\}\s*\{([^{}]*)\}", r"((\1)/(\2))", t)
    t = re.sub(r"\\sqrt\s*\{([^{}]*)\}", r"√(\1)", t)
    t = re.sub(r"\^\s*\{([^{}]*)\}", r"^(\1)", t)
    for a, b in ((r"\times", "×"), (r"\cdot", "×"), (r"\div", "÷"), (r"\left", ""), (r"\right", ""), (r"\$", "$"),
                 (r"\,", ""), (r"\;", " "), (r"\%", "%"), (r"\quad", "  "), (r"\qquad", "  ")):
        t = t.replace(a, b)
    t = re.sub(r"\\mathbf\{([^{}]*)\}|\\text\{([^{}]*)\}|\\mathrm\{([^{}]*)\}",
               lambda m: next(g for g in m.groups() if g is not None), t)
    return t.replace("{", "(").replace("}", ")")


def normalise(t):
    t = re.sub(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", lambda m: " " + tex_to_plain(m.group(1) or m.group(2)) + " ", t, flags=re.S)
    t = re.sub(r"\(\s*[A-Za-z][^()]{0,30}\)", " ", t)            # "3 (B) + 4 (D)": labels, not factors
    t = t.replace("−", "-").replace("–", "‐").replace("×", "*").replace("÷", "/").replace("·", "*")
    t = t.replace("[", "(").replace("]", ")").replace("²", "^2").replace("$", "")
    t = re.sub(r"(?<=\d),(?=\d{3}\b)", "", t)                    # 105,700
    return t


NUM = r"\d+(?:\.\d+)?"
RUN = re.compile(r"[0-9.()+\-*/^√ ]*[0-9)]")                       # a stretch of arithmetic


def evaluate(expr):
    e = expr.strip()
    if not re.search(r"\d", e) or not re.search(r"[+\-*/^√]|\)\s*\(|\d\s*\(", e):
        return None                                               # a bare number states nothing
    e = re.sub(r"(\d|\))\s*\(", r"\1*(", e)                       # 4(2), (2.33)(1.76)
    e = re.sub(r"√\s*\(", "math.sqrt(", e)
    e = re.sub(r"√\s*(" + NUM + ")", r"math.sqrt(\1)", e)
    e = e.replace("^", "**")
    if e.count("(") != e.count(")"):
        return None
    try:
        v = eval(e, {"__builtins__": {}, "math": math})
    except Exception:
        return None
    return float(v) if isinstance(v, (int, float)) else None


def matches(value, stated, rounded_inputs=False):
    """the stated number is the value rounded to the places it shows; where the inputs are themselves
    rounded decimals (266.67 for 266.666...), the result may also be the exact one, within 0.1%"""
    places = len(stated.split(".")[1]) if "." in stated else 0
    if abs(value - float(stated)) <= 0.5 * 10 ** -places + 1e-9:
        return True
    return rounded_inputs and abs(value - float(stated)) <= 0.001 * max(abs(value), abs(float(stated)))


LABEL = re.compile(r"^\s*([A-Za-z][A-Za-z ()^\\]{1,40}?)\s*=\s*(.*)$")


def joined(lines):
    """a calculation set out over several lines, each starting "Total Cost =", is one chain"""
    out, label = [], None
    for line in lines:
        if not line.strip():
            continue                                              # a blank line does not end the chain
        m = LABEL.match(line)
        if m and label == m.group(1).strip() and out:
            out[-1] = out[-1] + " = " + m.group(2)
            continue
        label = m.group(1).strip() if m else None
        out.append(line)
    return [l for l in out if l.strip()]


def chains(text):
    """yield (left expression, right side) for every '=' joining two stretches of arithmetic"""
    for line in joined(normalise(text).splitlines()):
        parts = line.split("=")
        for i in range(len(parts) - 1):
            left = RUN.findall(parts[i].rstrip() + " ")
            m = re.match(r"\s*(" + RUN.pattern + r")(\s*%)?", parts[i + 1])
            if not left or not m:
                continue
            lhs = left[-1]
            # the left stretch must end right at the "=", or it belongs to other text
            if not parts[i].rstrip().endswith(lhs.rstrip()):
                continue
            yield lhs.strip(), m.group(1).strip(), bool(m.group(2)), line.strip()


def check(text):
    checked, wrong = [], []
    for lhs, rhs, pct, line in chains(text):
        lv = evaluate(lhs)
        if lv is None:
            continue
        rounded = bool(re.search(r"\d\.\d", lhs))
        stated = rhs.lstrip("-")
        if re.fullmatch(NUM, stated):
            sign = "-" if rhs.startswith("-") else ""
            ok = matches(lv, sign + stated, rounded) or (pct and matches(lv * 100, sign + stated, rounded))
        else:
            rv = evaluate(rhs)
            if rv is None:
                continue
            ok = abs(lv - rv) <= max(1e-6, 0.006 * max(abs(lv), abs(rv), 1))   # a rounded step in a chain
        (checked if ok else wrong).append((lhs, rhs, round(lv, 6), line[:140]))
    return checked, wrong


def main(argv):
    show = "--show" in argv
    files = [a for a in argv if not a.startswith("--")]
    bad = 0
    for f in files:
        checked, wrong = check(page_text(open(f, encoding="utf-8").read()))
        print(f"{f}: {len(checked) + len(wrong)} calculations, {len(wrong)} wrong")
        for lhs, rhs, v, line in wrong:
            print(f"  WRONG  {lhs} = {rhs}   (it is {v:g})\n         in: {line}")
        if show:
            for lhs, rhs, v, _ in checked:
                print(f"  ok     {lhs} = {rhs}")
        bad += len(wrong)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
