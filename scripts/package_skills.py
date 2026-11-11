#!/usr/bin/env python3
"""Zip each project skill in .claude/skills/ for upload to claude.ai (Settings > Capabilities > Skills).

    python scripts/package_skills.py OUTDIR

In the repo a skill points at files by repo path (scripts/check_file.py, docs/engine-reference.md).
A claude.ai chat has no repo, so each zip carries the files its skill uses at those same relative
paths, plus CLAUDE.md, which the skills cite for the full rules. Re-run after changing a skill or
any file it bundles.
"""
import pathlib, sys, zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
ENGINE = ["engine/sd-graph.js", "engine/sd-graph.css"]
HP = ["engine/hp10bii.js", "engine/hp10bii.css"]
REF = ["docs/engine-reference.md"]
CHECK = ["scripts/check_file.py", "scripts/em_widths.py"]
MAN = ["scripts/man4504/transport.py", "scripts/man4504/project_mgmt.py", "scripts/man4504/project_mgmt.css",
       "scripts/man4504/project_mgmt.js"]

BUNDLES = {
    "widget-basics": ENGINE + REF + ["scripts/embed_engine.py", "examples/ECO2013-Widgets-All.html"] + CHECK,
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
                                                       "scripts/widget_text.py", "scripts/test_widget_text.py"],
    "widget-qa": ENGINE + CHECK + ["scripts/test_check_file.py", "scripts/place_labels.py", "scripts/embed_engine.py", "scripts/render_widgets.py",
                                   "scripts/mobile_check.py", "scripts/check_calc_widgets.py", "scripts/measure_em.py"],
    "review-notes": CHECK + ["scripts/mobile_check.py"],
}

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
            zf.writestr(f"{name}/SKILL.md", head + sep + NOTE + body)
            for f in sorted(set(files + ["CLAUDE.md"])):
                src = ROOT / f
                assert src.exists(), f
                zf.write(src, f"{name}/{f}")
        print(f"{z.name}: {len(set(files)) + 2} files, {z.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main(sys.argv[1])
