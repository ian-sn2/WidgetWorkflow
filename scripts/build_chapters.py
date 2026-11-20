#!/usr/bin/env python3
"""Rebuild every chapter kept in chapters/ from its sources, into build/chapters/ (git-ignored).

    python scripts/build_chapters.py                 # every chapter
    python scripts/build_chapters.py MAN4504         # chapters whose path contains MAN4504
    python scripts/build_chapters.py --check         # also run check_arithmetic.py on every output

A chapter is a folder chapters/<COURSE>/<chapter>/ holding source/ (the files Ian sent, unchanged) and
chapter.json: "steps" is a list of commands run from the repo root, each a script path (or "copy")
followed by its arguments, with {source} and {out} filled in; "outputs" names the files the steps must
leave in {out}. The builds assert their own numbers (the $105,700 total, the 15-week critical path), so
a passing build is a checked one. Only sources are committed; the finished editions are rebuilt.

Ian, 2026-11-12: keep the sources in the repo so a container reset no longer loses them and nothing
has to be uploaded twice.
"""
import json, pathlib, shutil, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "build" / "chapters"


def chapters(filters):
    for meta in sorted((ROOT / "chapters").glob("*/*/chapter.json")):
        rel = meta.parent.relative_to(ROOT / "chapters").as_posix()
        if not filters or any(f in rel for f in filters):
            yield rel, meta.parent, json.loads(meta.read_text(encoding="utf-8"))


def build(rel, folder, spec):
    out = OUT / rel
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    fill = lambda a: a.replace("{source}", str(folder / "source")).replace("{out}", str(out))
    for step in spec["steps"]:
        args = [fill(a) for a in step]
        if args[0] == "copy":
            shutil.copyfile(args[1], args[2]); continue
        r = subprocess.run([sys.executable, str(ROOT / args[0])] + args[1:], cwd=ROOT, capture_output=True, text=True)
        if r.returncode:
            return [f"{step[0]} failed:\n{(r.stdout + r.stderr).strip()[-1500:]}"]
    return [f"missing output {o}" for o in spec["outputs"] if not (out / o).exists()]


def main(argv):
    check = "--check" in argv
    filters = [a for a in argv if not a.startswith("--")]
    bad = 0
    for rel, folder, spec in chapters(filters):
        problems = build(rel, folder, spec)
        if not problems and check:
            outs = [str(OUT / rel / o) for o in spec["outputs"]]
            r = subprocess.run([sys.executable, str(ROOT / "scripts" / "check_arithmetic.py")] + outs,
                               cwd=ROOT, capture_output=True, text=True)
            if r.returncode:
                problems.append(r.stdout.strip())
        print(("ok    " if not problems else "FAIL  ") + rel + ("" if not problems else "\n  " + "\n  ".join(problems)))
        bad += bool(problems)
    print(f"{bad} chapter(s) failed" if bad else "all chapters built")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
