"""Build the delivery: every chapter's Full, Balanced and Concise with the
approved figures (build.CH), the live TOC script and Option A spacing
(tight.css), under short Windows-safe paths. Then CHECKLIST.md and one
changelog per changed chapter."""
import os, sys, json, glob, re, subprocess, shutil
import build, figs
from common import LOOK
S = build.SRC; D = S + "/deliver/UCF Accounting & Management"; REPO = build.REPO
TIGHT = open(S + "/tools/tight.css").read()
COURSE = {"a - ACG2021": "ACG2021", "c - ACG2071": "ACG2071", "d- ACG3173": "ACG3173", "i - MAN3025": "MAN3025"}
def short(rel):
    parts = rel.split("/")[1:]; out = []   # drop the unpack folder (acg2071/, man3025/)
    for p in parts:
        p = p.replace(" - DONE", "")
        for k, v in COURSE.items():
            if p.startswith(k): p = v
        out.append(p)
    return "/".join(out)
if os.path.isdir(D): shutil.rmtree(D)
by_folder = {v[0]: k for k, v in build.CH.items()}
rows = []; log = []
files = sorted(f for f in glob.glob(S + "/**/*.html", recursive=True) if all(x not in f for x in ("/x - ", "/x-", "Ignore", "Old Version", "Processed", "/out/", "/tight/", "/deliver/", "/gallery/", "/review/", "/spacing/", "/tools/")) and re.search(r"-(Full|Balanced|Concise)\.html$", f))
for f in files:
    chap = os.path.basename(os.path.dirname(f)); key = next((k for fo, k in by_folder.items() if chap.startswith(fo)), None)
    ed = re.search(r"-(Full|Balanced|Concise)\.html$", f).group(1)
    if key and ed != "Concise":
        m = json.load(open(f"{S}/maps/{key}.json"))
    else:
        m = {"images": {}, "anchors": [], "style": LOOK}
    m["page_style"] = TIGHT
    mp = f"{S}/maps/_deliver.json"; json.dump(m, open(mp, "w"), ensure_ascii=False)
    out = D + "/" + short(os.path.relpath(f, S)); os.makedirs(os.path.dirname(out), exist_ok=True)
    r = subprocess.run([sys.executable, REPO + "/scripts/apply_widgets.py", f, mp, out, "--toc"], capture_output=True, text=True)
    if r.returncode:
        print("!!", os.path.basename(f), (r.stdout + r.stderr).strip().splitlines()[-1][:200]); continue
    if key == "ACG2071-E1-CostBehavior" and ed != "Concise":
        t = open(out, encoding="utf-8").read()
        old, new = (("None of the following cost graphs represents this situation.", "None of the cost graphs above represents this situation.") if ed == "Full" else ("None of these cost graphs represent this:", "None of the cost graphs above represent this."))
        assert t.count(old) == 1; open(out, "w", encoding="utf-8").write(t.replace(old, new))
    n = int(re.search(r"(\d+) widgets", r.stdout).group(1)); nfig = open(out, encoding="utf-8").read().count('<figure class="sk-fig')
    rows.append((short(os.path.relpath(f, S)), ed, key, n, nfig))
print(len(rows), "files written")
json.dump(rows, open(S + "/deliver/rows.json", "w"))
