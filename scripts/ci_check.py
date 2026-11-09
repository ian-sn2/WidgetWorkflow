#!/usr/bin/env python3
"""The checks every pull request runs (.github/workflows/checks.yml).

    python scripts/ci_check.py                     # what CI runs
    python scripts/ci_check.py --update-baseline   # after fixing or accepting failures
    python scripts/ci_check.py --phone 390x844     # the phone check at one size
    python scripts/ci_check.py --phone 320x568 --update-baseline

1. The three test suites must report 0 failing.
2. Every page that embeds the engine (examples/ and solutions/) is checked
   with check_file.py. A page fails CI when it reports a FAIL that is not in
   scripts/ci_baseline.json -- the example pages carry failures from before
   the caption cap (CLAUDE.md rule 9), and those are recorded there rather
   than blocking every pull request. A page with no baseline entry, such as a
   new one, must be at 0 FAIL. An "engine" failure (an embedded copy that is
   not byte-identical to engine/) is never baselined: re-embed the page.

Ian, 2026-11-09: run the checks automatically so a broken page or an engine
clash between sessions is caught at the pull request, not after it merges.

3. With --phone WxH, mobile_check.py instead loads every page at that size and
   presses every scenario, step and Back button. Its problems (a page that
   scrolls sideways, a figure wider than its column, a button under 44px, a
   button that does nothing, an engine error) are compared the same way,
   against scripts/ci_phone_baseline.json. This is the one check that drives
   the widgets: check_file.py reads them and never presses anything, and every
   `calcs` widget was once dead on load while it passed.

Only the standard library for 1 and 2, so that job needs nothing installed;
3 needs Playwright and Chromium.
"""
import json
import os
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASELINE = ROOT / "scripts" / "ci_baseline.json"
PHONE_BASELINE = ROOT / "scripts" / "ci_phone_baseline.json"
TESTS = ["test_check_file.py", "test_curve_shapes.py", "test_widget_text.py"]
ENGINE_MARK = re.compile(r"sd-graph\.js v\d+\.\d+")


def gh(kind, msg):
    """A GitHub Actions annotation, and plain text everywhere else."""
    print("::%s::%s" % (kind, msg) if "GITHUB_ACTIONS" in os.environ else "%s: %s" % (kind.upper(), msg))


def pages():
    out = []
    for d in ("examples", "solutions"):
        for f in sorted((ROOT / d).glob("*.html")):
            if ENGINE_MARK.search(f.read_text(encoding="utf-8", errors="replace")):
                out.append(f)
    return out


def fails(page):
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "check_file.py"), str(page)],
                       capture_output=True, text=True, cwd=ROOT)
    lines = [l.rstrip() for l in r.stdout.splitlines() if l.startswith("FAIL")]
    return lines, r.stdout


def phone_problems(size):
    """mobile_check.py's problems per page, each keyed so a pixel or two of
    font difference between machines does not read as a new problem."""
    w, h = size.lower().split("x")
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "mobile_check.py"),
                        "--width", w, "--height", h, "--settle", "250"]
                       + [str(p) for p in pages()], capture_output=True, text=True, cwd=ROOT)
    if r.returncode != 0 or "problem(s) at" not in r.stdout:
        print(r.stdout[-3000:], r.stderr[-3000:])
        raise SystemExit("mobile_check.py did not finish")
    out, page, widget = {}, None, ""
    names = {p.name: p.relative_to(ROOT).as_posix() for p in pages()}
    for line in r.stdout.splitlines():
        m = re.match(r"=== (\S+)\s+@", line)
        if m:
            page = names[m.group(1)]; out[page] = []; continue
        m = re.match(r"  (w\d+) ", line)
        if m:
            widget = m.group(1); continue
        m = re.match(r"\s+(page|fit|tap|reach|live)\s+(.*)", line)
        if m and page:
            kind, text = m.groups()
            if kind in ("fit", "tap", "reach"):
                text = widget + " " + text
            text = re.sub(r"[+-]?\d+(\.\d+)?px", "#px", text)
            text = re.sub(r"\d+ms", "#ms", text)
            out[page].append("%s %s" % (kind, " ".join(text.split())))
    return out, r.stdout


def phone(size, update):
    key = size.lower()
    allbase = json.loads(PHONE_BASELINE.read_text()) if PHONE_BASELINE.exists() else {}
    base = allbase.get(key, {})
    got, raw = phone_problems(size)
    bad = 0
    for page, lines in got.items():
        fresh = [l for l in lines if l not in set(base.get(page, []))]
        print("%-70s %d problem(s)%s" % (page, len(lines), "" if not fresh else "  <- %d new" % len(fresh)))
        if fresh and not update:
            bad += 1
            for l in fresh:
                gh("error", "%s @%s: %s" % (page, key, l))
    if update:
        allbase[key] = {p: sorted(set(l)) for p, l in got.items()}
        PHONE_BASELINE.write_text(json.dumps(allbase, indent=1, ensure_ascii=False) + "\n")
        print("phone baseline written for %s: %d known problems"
              % (key, sum(len(v) for v in allbase[key].values())))
        return 0
    print("\n%s" % ("phone check passes at %s" % key if not bad else "%d page(s) with new phone problems" % bad))
    return 1 if bad else 0


def main():
    update = "--update-baseline" in sys.argv[1:]
    if "--phone" in sys.argv[1:]:
        return phone(sys.argv[sys.argv.index("--phone") + 1], update)
    bad = 0
    tests_bad = 0

    for t in TESTS:
        r = subprocess.run([sys.executable, str(ROOT / "scripts" / t)], capture_output=True, text=True, cwd=ROOT)
        last = (r.stdout.strip().splitlines() or ["(no output)"])[-1]
        ok = r.returncode == 0 and last.strip() == "0 failing"
        print("%-22s %s" % (t, last.strip()))
        if not ok:
            bad += 1; tests_bad += 1
            gh("error", "%s: %s" % (t, last.strip()))
            print("\n".join(l for l in r.stdout.splitlines() if l.startswith("FAIL")))

    base = json.loads(BASELINE.read_text()) if BASELINE.exists() else {}
    new_base = {}
    for page in pages():
        rel = page.relative_to(ROOT).as_posix()
        got, out = fails(page)
        engine = [l for l in got if re.match(r"FAIL\s+engine\b", l)]
        known = set(base.get(rel, []))
        fresh = [l for l in got if l not in known or l in engine]
        new_base[rel] = sorted(l for l in got if l not in engine)
        summary = (out.strip().splitlines() or [""])[-1]
        print("%-70s %s%s" % (rel, summary, "" if not fresh else "  <- %d new" % len(fresh)))
        if fresh and not update:
            bad += 1
            for l in fresh:
                gh("error", "%s: %s" % (rel, " ".join(l.split())))
        if engine:
            bad += 1

    if update:
        BASELINE.write_text(json.dumps(new_base, indent=1, ensure_ascii=False) + "\n")
        print("baseline written: %d pages, %d known failures"
              % (len(new_base), sum(len(v) for v in new_base.values())))
        return 1 if tests_bad else 0
    print("\n%s" % ("all checks pass" if not bad else "%d check(s) failed" % bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
