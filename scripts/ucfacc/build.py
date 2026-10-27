"""Maps for the ACG2021 / ACG2071 / ACG3173 / MAN3025 UCF chapters and the
apply step: python build.py  (UCF_SRC = the unpacked set, UCF_OUT = output).
Only the widgets change (CLAUDE.md, the UCF rule); --toc swaps the head's
script for the live table-of-contents one."""
import os, sys, json, glob, subprocess, re
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "mar3203"))
import graphs, figs
from common import LOOK
SRC = os.environ.get("UCF_SRC", "/tmp/claude-0/-home-user-WidgetWorkflow/18e4fdac-d634-5a6b-a05e-3dc28e88a03b/scratchpad/ucf2")
OUT = os.environ.get("UCF_OUT", SRC + "/out"); MAPS = SRC + "/maps"; os.makedirs(MAPS, exist_ok=True)
REPO = os.path.join(os.path.dirname(__file__), "..", "..")
F = figs
def drop(why): return {"drop": why}
P = "acg2021-exam1-"; C = "acg2071-exam1-cost-behavior-"; M3 = "acg3173-exam2-mod5-"
CH = {  # key: (folder substring, {image basename: entry})
 "ACG2021-E1-M1": ("01 - UCF ACG2021 Exam 1 Module 1", {P + "01-accounting-equation-diagram.png": F.accounting_equation(), P + "03-asset-accounts-diagram.png": graphs.ASSETS, P + "04-liability-accounts-diagram.png": graphs.LIABS,
                                                      P + "05-stockholders-equity-flow.png": F.se_flow(), P + "06-financial-statements-flow.png": F.statements_flow()}),
 "ACG2021-E2-M1": ("03 - UCF ACG2021 Exam 2 Module 1", None),   # same file as E1-M1
 "ACG2021-E1-M2": ("02 - UCF ACG2021 Exam 1 Module 2", {"acg2021-exam1-accounting-cycle-01-debit-credit-diagram.png": F.debit_credit()}),
 "ACG2021-E2-M2": ("03 - UCF ACG2021 Exam 2 Module 2", None),
 "ACG2021-E2-M3": ("03 - UCF ACG2021 Exam 2 Module 3", {"acg2021-exam2-chapter03-01-accounting-cycle-diagram.png": F.accounting_cycle()}),
 "ACG2021-E3-M1": ("04 - UCG ACG2021 Exam 3 Module 1", {"acg2021-exam3-internal-controls-01-fraud-triangle.png": F.fraud_triangle(), "acg2021-exam3-internal-controls-02-pyramid-framework-2.png": F.controls_pyramid(),
                                                      "acg2021-exam3-internal-controls-03-chapter-summary-2.png": F.controls_summary()}),
 "ACG2071-E1-CostBehavior": ("03 - ACG2071 UCF Exam 1 CostBehavior", {C + "01-variable-cost.png": graphs.COST3, C + "13-fixed-costs.png": drop("the Fixed case of the three-pattern widget above"), C + "14-mixed-costs.png": drop("the Mixed case of the three-pattern widget above"),
                                                                      C + "02-iphone-cost-graph.png": graphs.IPHONE, C + "04-relevant-ranges.png": graphs.RANGES, C + "05-step-costs-2.png": graphs.STEPS, C + "06-curvilinear-costs.png": drop("the Curvilinear case of the step-and-curvilinear widget above"),
                                                                      C + "08-high-low-method-graphs.png": graphs.HIGHLOW, C + "15-high-low-method-outliers.png": drop("the outlier case of the high-low widget above"), C + "09-scatterplot-example.png": graphs.SCATTER,
                                                                      C + "10-standard-cost-graphs.png": graphs.STD3, C + "11-phone-bill-graph.png": graphs.PHONE, C + "12-learning-curve.png": graphs.LEARN}),
 "ACG2071-E3-FPA": ("01 - ACG2071 UCF Exam 3 FinancialPlanningAnalysis", {"acg2071-exam3-ch09-01-master-budget-diagram-manufacturer.png": F.master_budget()}),
 "ACG2071-E3-SCA": ("02 - ACG2071 UCF Exam 3 StandardyCostingAnalysis", {"acg2071-exam3-ch10-01-wip-inventory-flow-diagram.png": F.wip_flow()}),
 "ACG3173-E2-CVP": ("02 - ACG3173 UCF Exam 2 ManagerialAccountingCVPAnalysis", {M3 + "01-variable-cost-graph.png": graphs.COST3_3173, M3 + "02-fixed-cost-graph.png": drop("the Fixed case of the three-pattern widget above"),
                                                                                M3 + "03-mixed-cost-graph.png": drop("the Mixed case of the three-pattern widget above"), M3 + "04-relevant-ranges-graph.png": graphs.RANGES_3173}),
 "MAN3025-Ch1": ("01 - Chapter 1", {"cs1-chapter01-01-management-pyramid-levels-functional-areas.png": F.management_pyramid()}),
 "MAN3025-Ch2": ("02 - Chapter 2", {"cs2-chapter02-01-systems-viewpoint-inputs-transformation-outputs-feedback-diagram.png": F.systems_view()}),
 "MAN3025-Ch3": ("03 - Chapter 3", {"cs3-ch03-summary-01-carroll-pyramid-philanthropic-ethical-legal-economic.png": F.carroll()}),
 "MAN3025-Ch6": ("04 - Chapter 06", {"cs7-ch06-01-swot-analysis-grid.png": graphs.SWOT, "cs7-ch06-02-bcg-matrix-grid.png": graphs.BCG}),
 "MAN3025-Ch7": ("05 - Chapter 07", {"cs5-chapter07-summary-01-decision-tree-ethical-managerial-flowchart-2.png": F.decision_tree(), "cs5-chapter07-summary-02-decision-making-styles-matrix-value-orientation-ambiguity-2.png": graphs.STYLES}),
 "MAN3025-Ch8": ("01 - Chapter 8", {"cs8-3-chapter08-01-competing-values-framework-grid.png": graphs.CVF}),
 "MAN3025-Ch11": ("04 - Chapter 11", {"cs12-ch11-01-diversity-wheel-concentric-circles-diagram.png": F.diversity_wheel()}),
 "MAN3025-Ch12": ("05 - Chapter 12", {"cs13-ch12-motivation-01-maslow-hierarchy-pyramid.png": F.maslow()}),
 "MAN3025-Ch13": ("03 - Chapter 13", {"cs15-5-chapter13-01-conflict-handling-styles-grid.png": graphs.CONFLICT}),
}
CH["ACG2021-E2-M1"] = (CH["ACG2021-E2-M1"][0], CH["ACG2021-E1-M1"][1]); CH["ACG2021-E2-M2"] = (CH["ACG2021-E2-M2"][0], CH["ACG2021-E1-M2"][1])
def normalise(images):
    """One copy of the figure stylesheet per file, on the first HTML entry."""
    out, first = {}, True
    for k, e in images.items():
        if isinstance(e, dict) and "html" in e:
            h = e["html"].replace(figs.FIGCSS, "").replace(figs.CSS, "")
            out[k] = {"html": (figs.FIGCSS if first else "") + h}; first = False
        else: out[k] = e
    return out
def main(keys=None):
    for key, (folder, images) in CH.items():
        if keys and key not in keys: continue
        dirs = [d for d in glob.glob(SRC + "/**/" + folder + " - DONE", recursive=True) if os.path.isdir(d) and "Processed" not in d and "/tight/" not in d and "/out/" not in d]
        assert len(dirs) == 1, (key, dirs); d = dirs[0]
        m = {"images": normalise(images), "anchors": [], "style": LOOK}
        mp = f"{MAPS}/{key}.json"; json.dump(m, open(mp, "w"), ensure_ascii=False, indent=1)
        for ed in ("Full", "Balanced"):
            f = [x for x in glob.glob(d + f"/*-{ed}.html") if "Ignore" not in x]; assert len(f) == 1, (key, ed, f); f = f[0]
            od = OUT + "/" + os.path.relpath(d, SRC); os.makedirs(od, exist_ok=True)
            r = subprocess.run([sys.executable, REPO + "/scripts/apply_widgets.py", f, mp, od + "/" + os.path.basename(f), "--toc"], capture_output=True, text=True)
            tail = (r.stdout + r.stderr).strip().splitlines()[-1:] if (r.stdout + r.stderr).strip() else [""]
            print(f"{key:26s} {ed:9s} rc={r.returncode} {tail[0][:110]}")
            if r.returncode: print(r.stdout[-800:], r.stderr[-800:])
if __name__ == "__main__": main(sys.argv[1:] or None)
