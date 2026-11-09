#!/usr/bin/env python3
"""Insert engine/sd-graph.css and engine/sd-graph.js into a notes file's <head>.

    python scripts/embed_engine.py examples/ECO2013-263-SupplyAndDemand.html

This is the "calling program" the conversion prompt refers to. The model never
types the engine: it emits a single placeholder line in the <head>,

    <!--SDG-ENGINE-->

directly after the sn25-v6.js script line, and this script replaces that line
with a <style> block and a <script> block holding the engine verbatim.

Run with no placeholder present and the file already carrying an embedded
engine, it replaces those two blocks with the current engine instead -- that is
the re-embed step after any change to engine/ (CLAUDE.md hard rule 1).

The embedded copies are byte-identical to engine/, header comment included;
scripts/check_file.py verifies that.

A solutions page (solutions/) also carries the shell that filters its questions
by semester, exam and topic. It emits a second placeholder,

    <!--SOL-SHELL-->

and this script fills it from engine/exam-solutions.css and .js the same way;
with no placeholder, an embedded shell is replaced by the current one. A notes
file carries neither and is untouched by this half.
"""

import argparse
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CSS_SRC = ROOT / "engine" / "sd-graph.css"
JS_SRC = ROOT / "engine" / "sd-graph.js"

PLACEHOLDER = "<!--SDG-ENGINE-->"
SHELL_CSS_SRC = ROOT / "engine" / "exam-solutions.css"
SHELL_JS_SRC = ROOT / "engine" / "exam-solutions.js"
SHELL_PLACEHOLDER = "<!--SOL-SHELL-->"
SHELL_CSS_BLOCK = re.compile(r"[ \t]*<style>\s*\n\.sol-shell \{.*?\n</style>\n?", re.S)
SHELL_JS_BLOCK = re.compile(r"[ \t]*<script>\s*\n/\* ===== exam-solutions\.js.*?\n</script>\n?", re.S)
# An embedded engine is a <style> block whose first rule is .sdg, and a <script>
# block that is the engine's header comment or its IIFE.
CSS_BLOCK = re.compile(r"[ \t]*<style>\s*\n\.sdg \{.*?\n</style>\n?", re.S)
JS_BLOCK = re.compile(r"[ \t]*<script>\s*\n(?:/\* ===== sd-graph\.js|\(function \(\) \{).*?\n</script>\n?", re.S)
HOSTED = re.compile(
    r'[ \t]*(?:<link[^>]*sd-graph\.css[^>]*>|<script[^>]*src=["\'][^"\']*sd-graph\.js["\'][^>]*>\s*</script>)\s*\n?',
    re.I)


def blocks(css_src=CSS_SRC, js_src=JS_SRC):
    css = css_src.read_text(encoding="utf-8").rstrip("\n")
    js = js_src.read_text(encoding="utf-8").rstrip("\n")
    return "<style>\n%s\n</style>\n<script>\n%s\n</script>\n" % (css, js)


def embed_shell(out):
    """Fill or refresh the solutions shell; returns (text, note or None)."""
    n = out.count(SHELL_PLACEHOLDER)
    if n > 1:
        sys.exit("%d %s lines; expected at most one" % (n, SHELL_PLACEHOLDER))
    shell = blocks(SHELL_CSS_SRC, SHELL_JS_SRC)
    if n == 1:
        out = re.sub(r"[ \t]*" + re.escape(SHELL_PLACEHOLDER) + r"[ \t]*\n?",
                     lambda _m: shell, out, count=1)
        return out, "replaced the %s placeholder" % SHELL_PLACEHOLDER
    if SHELL_CSS_BLOCK.search(out) or SHELL_JS_BLOCK.search(out):
        out = SHELL_CSS_BLOCK.sub("", out)
        out = SHELL_JS_BLOCK.sub("", out)
        out = out.replace("</head>", shell + "</head>", 1)
        return out, "re-embedded over the existing solutions shell"
    return out, None


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", help="notes HTML file to embed into")
    ap.add_argument("-n", "--dry-run", action="store_true", help="report, do not write")
    args = ap.parse_args()

    path = pathlib.Path(args.file)
    if not path.exists():
        sys.exit("no such file: %s" % path)
    src = path.read_text(encoding="utf-8")
    engine = blocks()

    had_placeholder = PLACEHOLDER in src
    had_embedded = bool(CSS_BLOCK.search(src)) or bool(JS_BLOCK.search(src))

    out = HOSTED.sub("", src)
    n_hosted = len(HOSTED.findall(src))

    if had_placeholder:
        if src.count(PLACEHOLDER) > 1:
            sys.exit("%s has %d %s lines; expected exactly one"
                     % (path, src.count(PLACEHOLDER), PLACEHOLDER))
        # The engine goes in through a lambda, never as a replacement
        # string: re.sub reads escapes in a replacement, so a literal
        # backslash-n anywhere in the engine -- split('\\n') in the brace
        # label code -- comes out as a real newline and breaks the JS
        # string it was inside. The page then throws before drawing a
        # single widget, and the only visible symptom is a syntax error.
        out = re.sub(r"[ \t]*" + re.escape(PLACEHOLDER) + r"[ \t]*\n?",
                     lambda _m: engine, out, count=1)
        how = "replaced the %s placeholder" % PLACEHOLDER
    elif had_embedded:
        out = CSS_BLOCK.sub("", out)
        out = JS_BLOCK.sub("", out)
        if "</head>" not in out:
            sys.exit("%s has no </head>" % path)
        out = out.replace("</head>", engine + "</head>", 1)
        how = "re-embedded over the existing engine"
    else:
        if "</head>" not in out:
            sys.exit("%s has no </head> and no %s placeholder" % (path, PLACEHOLDER))
        out = out.replace("</head>", engine + "</head>", 1)
        how = "inserted the engine before </head>"

    out, shell_note = embed_shell(out)
    if shell_note:
        how += "; " + shell_note

    note = "%s%s" % (how, ", removed %d hosted reference(s)" % n_hosted if n_hosted else "")

    if args.dry_run:
        print("would embed into %s: %s" % (path, note))
        return 0
    if out == src:
        print("%s already up to date" % path)
        return 0
    path.write_text(out, encoding="utf-8")
    print("%s: %s" % (path, note))
    return 0


if __name__ == "__main__":
    sys.exit(main())
