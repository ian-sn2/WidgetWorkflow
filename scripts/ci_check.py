#!/usr/bin/env python3
"""The checks every pull request runs (.github/workflows/checks.yml).

    python scripts/ci_check.py                     # what CI runs
    python scripts/ci_check.py --update-baseline   # after fixing or accepting failures

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

Only the standard library, so CI needs nothing installed.
"""
import json
import os
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASELINE = ROOT / "scripts" / "ci_baseline.json"
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


def main():
    update = "--update-baseline" in sys.argv[1:]
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
