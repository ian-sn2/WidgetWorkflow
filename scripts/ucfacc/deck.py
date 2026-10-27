"""The review deck for the ACG/MAN set: one card per proposed change, the
current picture beside the proposed drawing, approve / disapprove / comment
saved to the artifact's store (the MAR3203 deck's template, 2026-10-26)."""
import os, re, json, glob, html as H, base64
import build, figs
S = build.SRC; R = S + "/review"; os.makedirs(R, exist_ok=True)
ENG = os.path.join(build.REPO, "engine")
URLS = {u.split("/")[-1]: u for u in open(S + "/tools/img_urls.txt").read().split()}
NAMES = {"ACG2021-E1-M1": "ACG2021 · Exam 1 Module 1 (and Exam 2 Module 1, the same file)", "ACG2021-E1-M2": "ACG2021 · Exam 1 Module 2 (and Exam 2 Module 2)", "ACG2021-E2-M3": "ACG2021 · Exam 2 Module 3",
         "ACG2021-E3-M1": "ACG2021 · Exam 3 Module 1", "ACG2071-E1-CostBehavior": "ACG2071 · Exam 1 Cost Behavior", "ACG2071-E3-FPA": "ACG2071 · Exam 3 Financial Planning", "ACG2071-E3-SCA": "ACG2071 · Exam 3 Standard Costing",
         "ACG3173-E2-CVP": "ACG3173 · Exam 2 CVP Analysis", "MAN3025-Ch1": "MAN3025 · Chapter 1", "MAN3025-Ch2": "MAN3025 · Chapter 2", "MAN3025-Ch3": "MAN3025 · Chapter 3", "MAN3025-Ch6": "MAN3025 · Chapter 6",
         "MAN3025-Ch7": "MAN3025 · Chapter 7", "MAN3025-Ch8": "MAN3025 · Chapter 8", "MAN3025-Ch11": "MAN3025 · Chapter 11", "MAN3025-Ch12": "MAN3025 · Chapter 12", "MAN3025-Ch13": "MAN3025 · Chapter 13"}
TITLES = {"01-accounting-equation": "The Accounting Equation", "03-asset-accounts": "Asset Accounts", "04-liability-accounts": "Liability Accounts", "05-stockholders-equity-flow": "Stockholders’ Equity Flow", "06-financial-statements-flow": "The Four Financial Statements",
          "debit-credit-diagram": "Debits and Credits by Account Type", "accounting-cycle-diagram": "The Accounting Cycle", "fraud-triangle": "The Fraud Triangle", "pyramid-framework": "Internal Control Framework", "chapter-summary": "Internal Controls Summary",
          "01-variable-cost.png": "Three Cost Behavior Patterns (replaces 3 pictures)", "02-iphone": "A Cell Phone Plan as a Mixed Cost", "04-relevant-ranges": "Relevant Ranges", "05-step-costs": "Step and Curvilinear Costs (replaces 2 pictures)", "08-high-low": "The High-Low Method (replaces 2 pictures)",
          "09-scatterplot": "High-Low Method Example (2 steps)",  "11-phone-bill": "The Phone Bill", "12-learning-curve": "Learning Curve", "master-budget": "The Master Budget", "wip-inventory": "Cost Flow Through WIP",
          "mod5-01-variable": "Three Cost Behavior Patterns (replaces 3 pictures)", "mod5-04-relevant": "Relevant Ranges", "management-pyramid": "The Management Pyramid", "systems-viewpoint": "The Systems Viewpoint", "carroll": "Carroll’s CSR Pyramid (floats right)", "swot": "SWOT Grid",
          "bcg": "BCG Matrix (floats right)", "decision-tree": "Ethical Decision Tree", "decision-making-styles": "Decision-Making Styles", "competing-values": "Competing Values Framework", "diversity-wheel": "The Diversity Wheel", "maslow": "Maslow’s Hierarchy", "conflict-handling": "Conflict-Handling Styles"}
def title_for(base):
    for k, v in TITLES.items():
        if k in base: return v
    return base
def context(key, base):
    folder = build.CH[key][0]
    d = [x for x in glob.glob(S + "/**/" + folder + " - DONE", recursive=True) if "/out/" not in x and "/tight/" not in x][0]
    t = open(glob.glob(d + "/*-Full.html")[0], encoding="utf-8").read()
    m = re.search(r"<img\b[^>]*" + re.escape(base), t, re.S)
    if not m: return ""
    before = re.sub(r"<!--.*?-->", " ", t[max(0, m.start() - 600):m.start()], flags=re.S); before = re.sub(r"<[^>]+>", " ", before); before = re.sub(r"\s+", " ", H.unescape(before)).strip()
    return "…" + before[-220:]
def block(e):
    if "html" in e: return e["html"]
    return '<div class="sdg"><script type="application/json">' + json.dumps(e, ensure_ascii=False).replace("</", "<\\/") + "</script></div>"
cards = []
ROUND2 = {"06-financial-statements": "Round 2: the links are now plain arrows, left to right.",
          "debit-credit": "Round 2: proper curly braces on the left, the +, = and − signs set at 24px; the two page screenshots under the figure show its size in the actual file at desktop and phone width.",
          "accounting-cycle-diagram": "Round 3: the arrowheads were there but the deck was swallowing them (every figure shared one arrowhead definition and the hidden cards won). Each figure has its own now, so the heads show here as they do in the file.",
          "fraud-triangle": "Round 3: the three names are set heavier (900 weight, 14px) and the rest of each phrase at 13px semibold.",
          "pyramid-framework": "Round 3: Monitoring is the same size as the other names, in a taller apex band.",
          "chapter-summary": "Round 3: the arrowheads show now (the deck was hiding them, see the accounting-cycle card). the brace is a real curly brace with its tip up toward the triangle, and the arrows are heavier.",
          "01-variable-cost.png": "Round 3: the dashed line from the origin is gone. The Mixed case now marks the two components as braces at the right end: the fixed part from the axis up to the dashed level, the variable part from there up to the line.",
          "09-scatterplot": "Round 3: the (1, $40) label sits right beside its circle.",
          "10-standard-cost": "Round 2: the picture is removed and the sentence before it now reads “None of the cost graphs above represents this situation.” (Balanced: “…represent this.”)",
          "master-budget": "Round 3: the arrowheads show now (the deck was hiding them, see the accounting-cycle card). an arrow into every box, a curly brace down the left for the operating budgets and one under the bottom row for the financial budgets.",
          "wip-inventory": "Round 3: SALE sits over the arrow from Finished Goods to COGS, and the line from WIP runs down and arrows into the brace holding the subsidiary accounts.",
          "mod5-01-variable": "Round 3: the Mixed case marks the fixed and variable components as braces at the right end, the variable one being the part above the dashed fixed level.",
          "management-pyramid": "Round 2: every level name is the same size and weight.",
          "maslow": "Round 3: Self-Actualization is set as large as the apex band allows, close to the other names, clear of the sides.",
          "systems-viewpoint": "Round 3: the arrowheads show now (the deck was hiding them, see the accounting-cycle card). heavier arrows with clear heads, including the feedback arrow back up into Inputs.",
          "carroll": "Round 3: Philanthropic is set as large as the apex allows without touching the sides, the same size as the other names.",
          "decision-tree": "Round 3: the No branch is back where it was; the note is wrapped narrower and the branches start further right, so nothing crosses it.",
          "01-accounting-equation": "Round 2: kept as the picture, as asked."}
def card(id, chapter, title, html, desc="", kind="figure"):
    for k, v in ROUND2.items():
        if k in id: desc = v
    cards.append({"id": re.sub(r"[^A-Za-z0-9_.~-]+", "-", id)[:120], "chapter": chapter, "edition": "Full + Balanced", "kind": kind, "title": title, "flags": [], "desc": desc, "html": html})
def img(base, w="100%"):
    data = base64.b64encode(open(S + "/imgcache/" + base, "rb").read()).decode()   # embedded: the viewer blocks other hosts
    return f'<img src="data:image/png;base64,{data}" alt="" style="max-width:{w};height:auto;display:block;margin:0 auto 8px;background:#fff">'
seen = set()
for key, (folder, images) in build.CH.items():
    if images is None or key in ("ACG2021-E2-M1", "ACG2021-E2-M2"): continue
    drops = [b for b, e in images.items() if isinstance(e, dict) and "drop" in e]
    for base, e in images.items():
        if isinstance(e, dict) and "drop" in e:
            if "10-standard-cost" in base:
                card(key + "-" + base, NAMES[key], "Standard cost graphs — picture removed, sentence reworded", f'<div class="pair"><div><h5>Now</h5>{img(base)}</div><div><h5>Proposed</h5><p class="ctx">The picture goes. The sentence before it, “None of the following cost graphs represents this situation.”, becomes “None of the cost graphs above represents this situation.” — the three-pattern widget earlier in the chapter draws the same three graphs.</p></div></div><p class="ctx">{H.escape(context(key, base))}</p>', kind="drop")
            continue
        if isinstance(e, dict) and "keep" in e:
            card(key + "-" + base, NAMES[key], title_for(base), f'<div class="pair"><div><h5>Now</h5>{img(base)}</div><div><h5>Proposed</h5><p class="ctx">Stays as the picture.</p></div></div><p class="ctx">{H.escape(context(key, base))}</p>', kind="keep")
            continue
        now = img(base)
        mine = [d for d in drops if (base.endswith("01-variable-cost.png") and ("13-fixed" in d or "14-mixed" in d or "02-fixed" in d or "03-mixed" in d)) or (base.endswith("05-step-costs-2.png") and "06-curv" in d) or (base.endswith("08-high-low-method-graphs.png") and "15-high-low" in d)]
        if mine: now += '<p class="ctx">Also removed, as cases of this widget’s buttons:</p>' + "".join(img(d, "60%") for d in mine)
        after = block(e).replace(figs.FIGCSS, "")
        if "debit-credit" in base:
            for nm, lab in (("desktop", "In the Full file at 1280px wide"), ("phone", "At 390px (phone)")):
                after += f'<p class="ctx">{lab}:</p><img src="data:image/png;base64,' + base64.b64encode(open(f"{S}/gallery/dc-inpage-{nm}.png", "rb").read()).decode() + '" alt="" style="width:100%;border:1px solid #ddd;display:block">'
        card(key + "-" + base, NAMES[key], title_for(base), f'<div class="pair"><div><h5>Now</h5>{now}</div><div><h5>Proposed</h5>{after}</div></div><p class="ctx">{H.escape(context(key, base))}</p>')
# spacing cards
def pair_img(name): return '<img src="data:image/jpeg;base64,' + base64.b64encode(open(f"{S}/spacing/{name}-pair.jpg", "rb").read()).decode() + '" alt="before and after" style="width:100%;display:block;margin:6px 0 14px;border:1px solid #ddd">'
t1 = json.load(open(S + "/tools/tight.json")); t2 = json.load(open(S + "/tools/tight2.json"))
def pct(rows, ed, a=1, b=2): rr = [r for r in rows if ed in r[0]] if ed else rows; x = sum(r[a] for r in rr); y = sum(r[b] for r in rr); return f"{100 * (x - y) / x:.0f}%"
r1 = [r for r in t1 if r[0] == 1000]; r1 = [(r[1], r[2], r[3]) for r in r1]
tbl = lambda rows: f'<table class="sv"><tr><th></th><th>Full</th><th>Balanced</th><th>Concise</th><th>All files</th></tr><tr><td>Shorter by</td><td>{pct(rows,"Full")}</td><td>{pct(rows,"Balanced")}</td><td>{pct(rows,"Concise")}</td><td>{pct(rows,"")}</td></tr></table>'
css1 = open(S + "/tools/tight.css").read(); css2 = open(S + "/tools/tight2.css").read()
card("spacing-1", "Every chapter · page spacing", "Option A: tighter spacing, same text size", f'<p class="ctx">One <code>&lt;style&gt;</code> block in each file’s head, over the StudyKnight sheet: list items 4px apart instead of 10, paragraph gaps 10px, heading banners and tip boxes with less padding, table cells 8×12px instead of 16×20, display formulas with 8px margins. Text size and line height unchanged. Measured on all 144 files at 1000px wide:</p>{tbl(r1)}<p class="ctx">Left: now. Right: with the block. Same scroll position, four sample pages.</p>' + "".join(pair_img(k + "-tight") for k in ("man-full", "acg-concise", "pc-full", "acg3173-full")) + f'<details><summary>The CSS</summary><pre>{H.escape(css1)}</pre></details>', kind="spacing")
card("spacing-2", "Every chapter · page spacing", "Option B: Option A plus 17px text at line-height 1.5", f'<p class="ctx">Option A’s block plus body text at 17px / 1.5 instead of 18px / 1.6. The prose itself is most of every page, so this is where the bigger saving is, at the cost of a slightly denser read:</p>{tbl(t2)}' + "".join(pair_img(k + "-tight2") for k in ("man-full", "acg-concise", "pc-full", "acg3173-full")) + f'<details><summary>The extra CSS</summary><pre>{H.escape(css2)}</pre></details>', kind="spacing")
card("head-toc", "Every chapter · head", "Swap the table-of-contents script for the live one", '<p class="ctx">Every file loads <code>content/sn25-v5.js</code>, which builds its 📖 OPEN BOOK table of contents at the very top of the page. The live script, <code>studyguide/sn25-v2.js</code>, builds the 📘 BLUE BOOK box before the first heading and is what the other UCF sets were switched to. No other head change: the StudyKnight stylesheet, fonts and MathJax stay.</p>', kind="head")
json.dump([{k: v for k, v in c.items() if k != "html"} for c in cards], open(R + "/cards.json", "w"), ensure_ascii=False, indent=1)
print(len(cards), "cards")
META = json.dumps([{k: v for k, v in c.items() if k != "html"} for c in cards], ensure_ascii=False).replace("</", "<\\/")
slots = "".join(f'<section class="slot" id="slot-{i}" hidden>{c["html"]}</section>' for i, c in enumerate(cards))
from common import LOOK
page = open(os.path.join(os.path.dirname(__file__), "review_template.html"), encoding="utf-8").read()
page = page.replace("/*ENGINE_CSS*/", open(ENG + "/sd-graph.css").read() + "\n" + LOOK).replace("/*FIG_CSS*/", figs.FIGCSS.replace("<style>", "").replace("</style>", "")).replace("<!--SLOTS-->", slots).replace("/*META*/", META).replace("/*ENGINE_JS*/", open(ENG + "/sd-graph.js").read().replace("</script", "<\\/script"))
open(R + "/ucf-acc-review.html", "w", encoding="utf-8").write(page); print(len(page) // 1024, "KB")
