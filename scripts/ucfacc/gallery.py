"""Render every figure and widget of the set to PNG for review."""
import os, sys, json, re
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "mar3203"))
import graphs, figs
from common import LOOK
OUT = os.environ.get("UCF_OUT", "/tmp/claude-0/-home-user-WidgetWorkflow/18e4fdac-d634-5a6b-a05e-3dc28e88a03b/scratchpad/ucf2/gallery"); os.makedirs(OUT, exist_ok=True)
ENG = os.path.join(os.path.dirname(__file__), "..", "..", "engine")
ITEMS = {"COST3": graphs.COST3, "COST3_3173": graphs.COST3_3173, "IPHONE": graphs.IPHONE, "STEPS": graphs.STEPS, "RANGES": graphs.RANGES, "LEARN": graphs.LEARN, "PHONE": graphs.PHONE,
         "HIGHLOW": graphs.HIGHLOW, "SCATTER": graphs.SCATTER, "SWOT": graphs.SWOT, "BCG": graphs.BCG, "STYLES": graphs.STYLES, "CVF": graphs.CVF, "CONFLICT": graphs.CONFLICT, "ASSETS": graphs.ASSETS, "LIABS": graphs.LIABS,
         "eq": figs.accounting_equation(), "se": figs.se_flow(), "dc": figs.debit_credit(), "cycle": figs.accounting_cycle(), "fraud": figs.fraud_triangle(), "ctrlsum": figs.controls_summary(), "stmts": figs.statements_flow(),
         "budget": figs.master_budget(), "wip": figs.wip_flow(), "mgmt": figs.management_pyramid(), "sys": figs.systems_view(), "tree": figs.decision_tree(), "wheel": figs.diversity_wheel(), "carroll": figs.carroll(), "maslow": figs.maslow(), "ctrlpyr": figs.controls_pyramid()}
def block(e):
    if "html" in e: return e["html"]
    return '<div class="sdg"><script type="application/json">' + json.dumps(e, ensure_ascii=False).replace("</", "<\\/") + "</script></div>"
page = ['<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Red+Hat+Display:wght@400;500;600;700;800&display=swap" rel="stylesheet">',
        '<link rel="stylesheet" href="https://studyknight.s3.us-east-1.amazonaws.com/content/sk26-v1.css"><style>' + open(ENG + "/sd-graph.css").read() + LOOK + 'body{max-width:900px} .item{margin:20px 0;border-top:1px dashed #ccc;padding-top:8px} .item p{font-size:14px;color:#888;margin:0 0 6px}</style></head><body>']
page.append(figs.FIGCSS)
for k, e in ITEMS.items(): page.append(f'<div class="item" id="{k}"><p>{k}</p>{block(e)}<div style="clear:both"></div></div>')
page.append('<script>' + open(ENG + "/sd-graph.js").read() + '</script></body></html>')
open(OUT + "/gallery.html", "w").write("\n".join(page))
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium", proxy={"server": os.environ["HTTPS_PROXY"]}); pg = b.new_page(viewport={"width": 960, "height": 900})
    pg.goto("file://" + OUT + "/gallery.html"); pg.wait_for_timeout(2500)
    errs = pg.evaluate("[...document.querySelectorAll('.sdg')].filter(d=>!d.querySelector('svg')).map(d=>d.closest('.item').id)")
    print("widgets without an svg:", errs)
    for k in ITEMS:
        el = pg.query_selector(f"#{k}"); el.scroll_into_view_if_needed()
        n = len(el.query_selector_all(".sdg-scen button"))
        if n:
            for i in range(n):
                el.query_selector_all(".sdg-scen button")[i].click(); pg.wait_for_timeout(250); el.screenshot(path=f"{OUT}/{k}-s{i}.png")
        else:
            el.screenshot(path=f"{OUT}/{k}.png")
            for bt in el.query_selector_all(".sdg-ctrl button"):
                if "Next" in bt.inner_text(): bt.click(); pg.wait_for_timeout(250); el.screenshot(path=f"{OUT}/{k}-step1.png")
    b.close()
print(sorted(os.listdir(OUT)))
