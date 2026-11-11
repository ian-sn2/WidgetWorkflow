#!/usr/bin/env python3
"""Package the project skills in .claude/skills/ for claude.ai.

    python scripts/package_skills.py --plugin          # write plugin/ (claude.ai syncs it from GitHub)
    python scripts/package_skills.py --check-plugin    # exit 1 if plugin/ is out of date (CI runs this)
    python scripts/package_skills.py OUTDIR            # one zip per skill, for a manual upload

The plugin is how the skills reach claude.ai without uploads (Ian, 2026-11-12): the repo is a plugin
marketplace (.claude-plugin/marketplace.json) with one plugin, plugin/, holding all seven skills and one
shared copy of the files they use. Added once in claude.ai (Customize > Plugins > Add marketplace,
ian-sn2/WidgetWorkflow, Sync automatically), it updates itself when the default branch changes. Its
version is bumped whenever its content changes, so a sync that waits for a new version sees one.

In the repo a skill points at files by repo path (scripts/check_file.py, docs/engine-reference.md).
A claude.ai chat has no repo, so each zip carries the files its skill uses at those same relative
paths, plus CLAUDE.md, which the skills cite for the full rules. Re-run after changing a skill or
any file it bundles.
"""
import json, pathlib, re, sys, zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
ENGINE = ["engine/sd-graph.js", "engine/sd-graph.css"]
HP = ["engine/hp10bii.js", "engine/hp10bii.css"]
REF = ["docs/engine-reference.md"]
CHECK = ["scripts/check_file.py", "scripts/em_widths.py"]
MAN = ["scripts/man4504/transport.py", "scripts/man4504/project_mgmt.py", "scripts/man4504/project_mgmt.css",
       "scripts/man4504/project_mgmt.js"]

BUNDLES = {
    "widget-basics": ENGINE + REF + ["scripts/embed_engine.py"] + CHECK,
    "curves-and-labels": ENGINE + REF + CHECK + ["scripts/curve_shapes.py", "scripts/test_curve_shapes.py",
                                                 "scripts/place_labels.py", "scripts/place_curve_labels.py"],
    "other-charts": ENGINE + HP + REF + MAN + ["scripts/embed_engine.py", "scripts/apply_widgets.py",
                                              "scripts/check_calc_widgets.py", "scripts/mobile_check.py",
                                              "scripts/mar3023/chapter22_pert.py", "scripts/ree3043/chapter17.py",
                                              "scripts/mcb4503/module13.py"],
    "study-guide-editions": CHECK + MAN + ["scripts/man4504/project_mgmt_editions.py", "scripts/man4504/transport_editions.py",
                                           "scripts/ree3043/chapter17.py", "scripts/ree3043/chapter17_editions.py",
                                           "scripts/mar3023/concise2.py", "scripts/mar3023/balanced2.py",
                                           "scripts/mar3023/chapter22_concise_headings.py"],
    "chapter-conversion": ENGINE + HP + REF + CHECK + ["docs/conversion-prompt-v7.md", "scripts/embed_engine.py",
                                                       "scripts/apply_widgets.py", "scripts/doc_headings.py",
                                                       "scripts/doc_formulas.py", "scripts/transcript_diff.py",
                                                       "scripts/widget_text.py", "scripts/test_widget_text.py",
                                                       "scripts/build_chapters.py"],
    "widget-qa": ENGINE + CHECK + ["scripts/check_arithmetic.py", "scripts/test_check_arithmetic.py",
                                   "scripts/build_chapters.py", "scripts/test_check_file.py", "scripts/place_labels.py", "scripts/embed_engine.py", "scripts/render_widgets.py",
                                   "scripts/mobile_check.py", "scripts/check_calc_widgets.py", "scripts/measure_em.py"],
    "review-notes": CHECK + ["scripts/mobile_check.py", "scripts/check_arithmetic.py"],
}

# claude.ai's skill upload rejects an .html file (widget-basics failed on the example page, 2026-11-11),
# so the example page travels as its 20 widget configs, which are what the skill uses it for.
EXAMPLE = "examples/ECO2013-Widgets-All.html"
GENERATED = {"widget-basics": {"examples/ECO2013-Widgets-All.configs.json": "example_configs"}}


def example_configs():
    t = (ROOT / EXAMPLE).read_text(encoding="utf-8")
    out = []
    for b in re.findall(r'<div class="sdg"><script type="application/json">(.*?)</script>', t, flags=re.S):
        try: c = json.loads(b)
        except ValueError: continue   # the "{ ...config... }" placeholder in the page's own comment
        out.append(c)
    assert len(out) == 20, len(out)
    return json.dumps(out, ensure_ascii=False, indent=1)


NOTE = ("\n> **Files:** every path below (`scripts/…`, `docs/…`, `engine/…`, `CLAUDE.md`) is inside this skill's "
        "folder, at the same place it sits in the WidgetWorkflow repo.\n")


def main(out):
    out = pathlib.Path(out); out.mkdir(parents=True, exist_ok=True)
    skills = sorted(p.name for p in (ROOT / ".claude/skills").iterdir() if (p / "SKILL.md").exists())
    assert skills == sorted(BUNDLES), (skills, sorted(BUNDLES))   # every skill is packaged, and only real ones
    for name, files in BUNDLES.items():
        text = (ROOT / ".claude/skills" / name / "SKILL.md").read_text(encoding="utf-8")
        head, sep, body = text.partition("\n---\n")   # after the frontmatter
        assert sep and head.startswith("---\n"), name
        z = out / f"{name}.zip"
        with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
            gen = GENERATED.get(name, {})
            for path in gen:   # point the skill at the generated stand-in for the page
                body = body.replace(EXAMPLE, path)
            assert EXAMPLE not in body or not gen, name
            zf.writestr(f"{name}/SKILL.md", head + sep + NOTE + body)
            for path, fn in gen.items():
                zf.writestr(f"{name}/{path}", globals()[fn]())
            for f in sorted(set(files + ["CLAUDE.md"])):
                src = ROOT / f
                assert src.exists(), f
                assert src.suffix != ".html", f   # the upload rejects HTML files
                zf.write(src, f"{name}/{f}")
        print(f"{z.name}: {len(set(files)) + 2} files, {z.stat().st_size // 1024} KB")


PLUGIN = ROOT / "plugin"
PLUGIN_NAME = "smokin-notes-widgets"
PLUGIN_DESC = ("Smokin' Notes study-guide widgets: creating widgets, drawing curves and placing labels, other chart "
               "types, Full/Balanced/Concise editions, chapter conversion, checks before delivery, and reviews.")
PLUGIN_NOTE = ("\n> **Files:** every path below (`scripts/…`, `docs/…`, `engine/…`, `examples/…`, `CLAUDE.md`) is in "
               "this plugin's root folder, two levels up from this skill (`../../scripts/…`), at the same place it "
               "sits in the WidgetWorkflow repo.\n")


def plugin_files():
    """every file the plugin holds, path -> bytes, apart from the version stamp"""
    out = {}
    for name, files in BUNDLES.items():
        text = (ROOT / ".claude/skills" / name / "SKILL.md").read_text(encoding="utf-8")
        head, sep, body = text.partition("\n---\n")
        assert sep and head.startswith("---\n"), name
        gen = GENERATED.get(name, {})
        for path in gen:
            body = body.replace(EXAMPLE, path)
        out[f"skills/{name}/SKILL.md"] = (head + sep + PLUGIN_NOTE + body).encode()
        for path, fn in gen.items():
            out[path] = globals()[fn]().encode()
        for f in files + ["CLAUDE.md"]:
            assert (ROOT / f).exists() and not f.endswith(".html"), f
            out[f] = (ROOT / f).read_bytes()
    return out


def plugin_tree():
    import hashlib
    files = plugin_files()
    digest = hashlib.sha256(b"".join(k.encode() + b"\0" + v for k, v in sorted(files.items()))).hexdigest()[:16]
    stamp = PLUGIN / ".content-hash"
    old = json.loads((PLUGIN / ".claude-plugin/plugin.json").read_text())["version"] if stamp.exists() else "1.0.0"
    major, minor, patch = (int(x) for x in old.split("."))
    same = stamp.exists() and stamp.read_text().strip() == digest
    version = old if same else f"{major}.{minor}.{patch + 1}"
    meta = {"name": PLUGIN_NAME, "version": version, "description": PLUGIN_DESC, "author": {"name": "Smokin' Notes"}}
    files[".claude-plugin/plugin.json"] = (json.dumps(meta, indent=2) + "\n").encode()
    files[".content-hash"] = (digest + "\n").encode()
    market = {"name": "smokin-notes", "owner": {"name": "Smokin' Notes"},
              "plugins": [{"name": PLUGIN_NAME, "source": "./plugin", "description": PLUGIN_DESC, "version": version}]}
    return files, (json.dumps(market, indent=2) + "\n").encode()


def write_plugin():
    import shutil
    files, market = plugin_tree()
    if PLUGIN.exists():
        shutil.rmtree(PLUGIN)
    for rel, data in files.items():
        (PLUGIN / rel).parent.mkdir(parents=True, exist_ok=True)
        (PLUGIN / rel).write_bytes(data)
    (ROOT / ".claude-plugin").mkdir(exist_ok=True)
    (ROOT / ".claude-plugin/marketplace.json").write_bytes(market)
    print(f"plugin/: {len(files)} files, version {json.loads(files['.claude-plugin/plugin.json'])['version']}")


def check_plugin():
    files, market = plugin_tree()
    have = {p.relative_to(PLUGIN).as_posix(): p.read_bytes() for p in PLUGIN.rglob("*")
            if p.is_file() and "__pycache__" not in p.parts} if PLUGIN.exists() else {}   # caches from running its tests
    mk = ROOT / ".claude-plugin/marketplace.json"
    stale = sorted(set(files) ^ set(have)) + sorted(k for k in files if k in have and files[k] != have[k])
    if not mk.exists() or mk.read_bytes() != market:
        stale.append(".claude-plugin/marketplace.json")
    if stale:
        print("plugin/ is out of date with .claude/skills/ or the files it bundles: run "
              "python scripts/package_skills.py --plugin and commit. Differs: " + ", ".join(stale[:8]))
        return 1
    print("plugin/ is up to date")
    return 0


if __name__ == "__main__":
    if sys.argv[1] == "--plugin":
        write_plugin()
    elif sys.argv[1] == "--check-plugin":
        sys.exit(check_plugin())
    else:
        main(sys.argv[1])
