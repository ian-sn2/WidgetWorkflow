"""MAR3023 Exam 3 (Fall '26): the pricing chapter (13-14) makeover and the two
Chapter 2 Part 1 versions, 2026-11-04. House files (sn25-v6), so the engine is
embedded through the placeholder and the frameless look rides in a <style>.

    python scripts/mar3023/pricing.py SRC13.html SRC2.html OUTDIR
"""
import sys, os, re, json, subprocess
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "mar3203")); sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "ucfacc"))
from common import cap, label, LOOK, svg, box, text, arrow, INK, GOLDC, PALEG, RED
from figs import FIGCSS, fig
REPO = os.path.join(os.path.dirname(__file__), "..", "..")

def AX(x, y, **k): return dict({"x": x, "y": y, "xmax": 110, "ymax": 110, "bg": False}, **k)
def widget(cfg): return '<div class="sdg"><script type="application/json">' + json.dumps(cfg, ensure_ascii=False).replace("</", "<\\/") + "</script></div>"

# ---------------------------------------------------------------- chapter 13-14 figures
# TR = q, TC = 35 + 0.5q: they cross at (70, 70)
BREAKEVEN = {"title": "Breakeven Analysis", "lede": "Total revenue against total cost as quantity sold rises.",
    "axes": AX("\nQuantity sold", "Revenue\nand cost ($)"),
    "curves": [{"id": "tr", "label": "Total revenue", "pts": [[0, 0], [95, 95]], "color": "gold", "ldy": -10},
               {"id": "tc", "label": "Total cost", "pts": [[0, 30], [95, 68]], "color": "ink", "ldx": 12, "ldy": -8}],
    "points": [{"q": 50, "p": 50, "pl": "Breakeven\nprice", "ql": "Breakeven\nquantity", "label": "Breakeven\npoint", "dx": -72, "dy": -14, "at": 1},
               {"q": 0, "p": 30, "dot": True, "guides": False, "showQ": False, "pl": "Fixed\ncost", "at": 0}],
    "areas": [{"pts": [[50, 50], [95, 95], [95, 68]], "color": "teal", "opacity": 0.45, "label": "Profit", "lp": [84, 74], "at": 2},
              {"pts": [[0, 0], [50, 50], [0, 30]], "color": "red", "opacity": 0.35, "label": "Loss", "lp": [15, 26], "at": 2}],
    "vbraces": [{"p1": 30, "p2": 68, "q": 98, "label": "Variable\ncosts", "at": 0}, {"p1": 0, "p2": 30, "q": 98, "label": "Fixed\ncosts", "at": 0}],
    "steps": [cap("Total revenue starts at the origin, since every unit made is sold; total cost starts at the fixed cost and climbs at the unit variable cost."),
              cap("Where the two lines cross, revenue just covers cost: that quantity and that price are the breakeven point."),
              cap("Left of the breakeven point the firm loses money; right of it, every extra unit sold adds to profit.")]}
SK = [[x, round(54 + 46 * 2.718 ** (-(x - 3) / 14), 2)] for x in range(3, 97, 4)]
PEN = [[x, round(46 - 40 * 2.718 ** (-(x - 3) / 14), 2)] for x in range(3, 97, 4)]
SKIM = {"title": "Market Skimming and Market Penetration", "lede": "Two starting points for a price that moves toward the same equilibrium.",
    "axes": AX("Time", "Price"),
    "curves": [{"id": "s", "label": "Market\nSkimming", "pts": SK, "curved": True, "color": "gold", "lstart": True, "ldx": 44, "ldy": 0},
               {"id": "p", "label": "Market\nPenetration", "pts": PEN, "curved": True, "color": "ink", "lstart": True, "ldx": 48, "ldy": -22}],
    "hlines": [{"p": 50, "label": "Eventual\nequilibrium\nprice", "dashed": True, "color": "grey"}],
    "caption": cap("Skimming starts high and lowers the price as the least price-sensitive buyers are served; penetration starts low and raises it as the brand takes hold.")}
BB = [[26, 98], [34, 84], [44, 70], [54, 58], [62, 46], [65, 34], [61, 22], [52, 13], [42, 8]]
PRESTIGE = {"title": "The Backward-Bending Demand Curve", "lede": "For a prestige good, cutting the price only raises demand up to a point.",
    "axes": AX("Quantity demanded", "Price"),
    "curves": [{"id": "d", "label": "Demand", "pts": BB, "curved": True, "color": "ink", "ldx": 40, "ldy": 0}],
    "areas": [{"pts": [[61.4, 53.6], [63.3, 56.7], [63.4, 61.3], [61.9, 66.9], [58.8, 73.0], [54.4, 79.1], [49.2, 84.4], [43.7, 88.5], [38.5, 91.0], [33.9, 91.7], [30.6, 90.4], [28.7, 87.3], [28.6, 82.7], [30.1, 77.1], [33.2, 71.0], [37.6, 64.9], [42.8, 59.6], [48.3, 55.5], [53.5, 53.0], [58.1, 52.3]], "color": "gold", "opacity": 0.35, "label": "The firm wants to keep its\nprice in this part of the curve", "lp": [76, 94]}],
    "caption": cap("Above the bend, a lower price sells more; below it, a lower price makes buyers doubt the product and demand falls away.")}
CHANNEL = {"flow": {"vertical": True, "nodes": ["Manufacturer", "Wholesaler", "Retailer", "Consumer"], "links": ["", "", ""]}, "title": "A Longer Channel",
    "caption": "The manufacturer sells through a distributor, so two markups sit between its price and the consumer's."}
def fixed_cost_fig():
    b = text(120, 26, "Fixed Costs", 15) + f'<rect x="80" y="40" width="80" height="230" fill="{PALEG}" stroke="{INK}" stroke-width="1.4"/>'
    b += f'<rect x="80" y="246" width="80" height="24" fill="{GOLDC}" stroke="{INK}" stroke-width="1.4"/>' + text(120, 263, "$20", 13, color="#fff")
    b += text(180, 48, "$4,000", 15, anchor="start") + f'<line x1="162" y1="258" x2="230" y2="200" stroke="{INK}" stroke-width="1.2"/>'
    b += text(236, 196, "Contribution (gross margin)", 14, anchor="start") + text(236, 216, "= Price − Variable cost", 13, anchor="start", bold=False) + text(236, 236, "= $28 − $8 = $20 per room", 13, anchor="start", bold=False)
    b += text(236, 262, "200 rooms × $20 = $4,000", 13, anchor="start", bold=False)
    return fig(520, 290, b, "A bar of $4,000 fixed costs, with the $20 contribution from one room marked at its foot: 200 rooms at $20 cover it", 440, "narrow", True)
def markup_fig():
    b = f'<rect x="100" y="20" width="110" height="110" fill="{GOLDC}" stroke="{INK}" stroke-width="1.4"/>' + text(155, 82, "50%", 16, color="#fff")
    b += f'<rect x="100" y="130" width="110" height="110" fill="{PALEG}" stroke="{INK}" stroke-width="1.4"/>' + text(155, 192, "50%", 16)
    b += text(76, 136, "$2,000", 13, anchor="end") + f'<line x1="84" y1="20" x2="84" y2="240" stroke="{INK}" stroke-width="1"/><line x1="84" y1="20" x2="92" y2="20" stroke="{INK}" stroke-width="1"/><line x1="84" y1="240" x2="92" y2="240" stroke="{INK}" stroke-width="1"/>'
    b += text(230, 70, "Markup: $1,000", 14, anchor="start") + text(230, 90, "extra revenue from the sale, to pay rent and", 12, anchor="start", bold=False) + text(230, 106, "salaries and leave some profit", 12, anchor="start", bold=False)
    b += text(230, 180, "Cost of goods: $1,000", 14, anchor="start") + text(230, 200, "what the retailer paid for the jacket", 12, anchor="start", bold=False)
    return fig(560, 256, b, "A $2,000 selling price split in half: $1,000 of markup over $1,000 cost of goods", 470, "narrow")
UNBUNDLE = '''
<table class="financial unbundle">
  <thead><tr><th>Caterpillar’s unbundled price</th><th></th></tr></thead>
  <tbody>
    <tr class="ub-head"><td colspan="2">Competing brand</td></tr>
    <tr><td class="ub-indent">Purchase price</td><td class="ub-amt">$200,000</td></tr>
    <tr class="ub-gap"><td colspan="2"></td></tr>
    <tr class="ub-head"><td colspan="2">Caterpillar brand</td></tr>
    <tr><td class="ub-indent">Equivalent value</td><td class="ub-amt">$200,000</td></tr>
    <tr><td class="ub-indent">More durability</td><td class="ub-amt">30,000</td></tr>
    <tr><td class="ub-indent">More reliability</td><td class="ub-amt">20,000</td></tr>
    <tr><td class="ub-indent">Faster service</td><td class="ub-amt">20,000</td></tr>
    <tr class="ub-rule"><td class="ub-indent">Longer warranty</td><td class="ub-amt">+ 10,000</td></tr>
    <tr class="ub-total"><td class="ub-indent">Total value</td><td class="ub-amt">$280,000</td></tr>
    <tr class="ub-rule"><td class="ub-indent">Discount</td><td class="ub-amt">− 40,000</td></tr>
    <tr class="ub-total ub-final"><td class="ub-indent">Purchase price</td><td class="ub-amt">$240,000</td></tr>
  </tbody>
</table>
<style>
  table.unbundle { border-collapse: collapse; margin: 18px auto; width: 380px; max-width: 100%; font-size: 17px; background: #fff; border: 1px solid #d9dee6; border-radius: 10px; overflow: hidden; }
  table.unbundle th { background: #1A49B3; color: #fff; font-weight: 600; text-align: left; padding: 9px 14px; font-size: 15px; }
  table.unbundle td { padding: 5px 14px; line-height: 1.35; }
  table.unbundle .ub-head td { font-weight: 700; color: #1A49B3; padding-top: 10px; }
  table.unbundle .ub-indent { padding-left: 28px; }
  table.unbundle .ub-amt { text-align: right; white-space: nowrap; font-variant-numeric: tabular-nums; width: 110px; }
  table.unbundle .ub-gap td { padding: 3px; }
  table.unbundle .ub-rule td.ub-amt { border-bottom: 1px solid #2B343C; }
  table.unbundle .ub-total td { font-weight: 700; }
  table.unbundle .ub-final td { padding-bottom: 12px; }
  table.unbundle .ub-final td.ub-amt { border-bottom: 3px double #2B343C; }
</style>'''
VIDEO_CSS = '''.video-section { width: 100%; margin: 14px auto; border: 1px solid #cfe0f5; border-radius: 10px; overflow: hidden; background: #fff; }
.video-section-header { background: #EFF7FF; color: #1A49B3; padding: 10px 20px; font-size: 17px; font-weight: 700; cursor: pointer; list-style: none; display: flex; justify-content: center; align-items: center; position: relative; user-select: none; }
.video-section-header::before { content: "▶"; font-size: 12px; margin-right: 10px; }
.video-section-header:hover { background: #e2eefb; }
.video-section-header::-webkit-details-marker { display: none; }
.expand-icon { position: absolute; right: 18px; font-size: 12px; transition: transform 0.3s ease; }
.video-section[open] .expand-icon { transform: rotate(180deg); }
.video-content { padding: 18px; text-align: center; background: #fff; }
.video-embed-wrapper { width: min(100%, 720px); margin: 0 auto; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,0.12); }
.video-embed-wrapper iframe { border-radius: 8px; }
.download-section { margin-top: 14px; }
.download-btn { display: inline-block; background: #1A49B3; color: #fff; padding: 9px 20px; text-decoration: none; border-radius: 999px; font-weight: 600; font-size: 15px; }
.download-btn:hover { background: #143a8f; color: #fff; text-decoration: none; }'''

def sub1(t, old, new, name):
    assert t.count(old) == 1, (name, t.count(old)); return t.replace(old, new)
def img_re(base): return re.compile(r'<img[^>]*' + re.escape(base) + r'[^>]*/?>', re.S)
def replace_img(t, base, html):
    m = img_re(base).findall(t); assert len(m) == 1, (base, len(m)); return img_re(base).sub(lambda _: html, t, 1)
def finish(t, out):
    """Engine after the house script, the frameless look after the engine, then write."""
    t = sub1(t, '<script src="https://smokinnotes.s3.us-east-1.amazonaws.com/studyguide/sn25-v2.js"></script>', '<script src="https://smokinnotes.s3.us-east-1.amazonaws.com/studyguide/sn25-v2.js"></script>\n<!--SDG-ENGINE-->', "house script")
    open(out, "w", encoding="utf-8").write(t)
    r = subprocess.run([sys.executable, REPO + "/scripts/embed_engine.py", out], capture_output=True, text=True); assert r.returncode == 0, r.stdout + r.stderr
    t = open(out, encoding="utf-8").read()
    t = sub1(t, "</head>", "<style>\n/* widget look */\n" + LOOK.strip() + "\n</style>\n</head>", "head end")
    open(out, "w", encoding="utf-8").write(t)

def chapter13(src, out):
    t = open(src, encoding="utf-8").read()
    # the six black-background pictures become drawings and widgets
    t = replace_img(t, "01-breakeven-analysis-graph.png", widget(BREAKEVEN))
    t = replace_img(t, "02-fixed-costs-contribution-chart.png", fixed_cost_fig()["html"])
    t = replace_img(t, "03-markup-price-breakdown.png", markup_fig()["html"])
    t = replace_img(t, "04-skimming-penetration-graph.png", widget(SKIM))
    t = replace_img(t, "05-backward-bending-demand-curve.png", widget(PRESTIGE))
    t = replace_img(t, "06-distribution-channel-diagram.png", widget(CHANNEL))
    # the unbundling example as one statement-style table
    start = t.index('<table class="financial">\n<tr class="total">\n<td><strong>Competing Brand</strong>'); end = t.index("</table>", t.index("Purchase Price</td>")) + len("</table>")
    t = t[:start] + UNBUNDLE.strip() + t[end:]
    # the reference-price list: the second item was never closed and a stray </li> followed the list
    t = sub1(t, "and it works by shifting the internal reference price.\n\n</ul>\n<p>For example, when you look for a product", "and it works by shifting the internal reference price.</li>\n</ul>\n<p>For example, when you look for a product", "ref list")
    t = sub1(t, 'called <strong>sticker shock</strong>.</p>\n</li>\n', 'called <strong>sticker shock</strong>.</p>\n', "stray li")
    # student-facing text does not attribute content to its source (CLAUDE.md rule 4)
    t = sub1(t, "Dr. Cooke noted that pricing has been intentionally taught at the end", "Pricing is intentionally taught at the end", "cooke 1")
    t = sub1(t, "<p><i>This segment is on the final marketing mix variable: price.", '<p id="intro-note"><i>This segment is on the final marketing mix variable: price.', "blurb id")
    # the house script puts its table of contents before the first <h1>, which leaves the blurb above it; this
    # handler is registered after that one, so it runs after it and moves the box above the blurb
    t = sub1(t, "</head>", "<script>document.addEventListener('DOMContentLoaded', function () { var b = document.getElementById('intro-note'), t = document.querySelector('details.toc-box'); if (b && t) b.parentNode.insertBefore(t, b); });</script>\n</head>", "blurb script")
    t = sub1(t, "The lecture solves for price given a quantity;", "Here we solve for price given a quantity;", "lecture")
    t = sub1(t, "<li><em>Backlash</em> – Dr. Cooke noted that a year or two ago Wendy's", "<li><em>Backlash</em> – A year or two ago Wendy's", "cooke 2")
    finish(t, out)

# ---------------------------------------------------------------- chapter 2, the two graphs
EXP = [[x, round(8 + 92 * (3.0 / (x + 2.5)) ** 0.9, 2)] for x in [1, 2, 3, 5, 7, 10, 14, 18, 24, 30, 38, 48, 60, 75, 90, 100]]
EXPERIENCE = {"title": "The Experience Curve", "axes": AX("Cumulative units produced", "Cost\nper unit"),
    "curves": [{"id": "e", "label": "", "pts": EXP, "curved": True, "color": "gold"}],
    "caption": cap("Each doubling of cumulative output cuts the unit cost by a fixed percentage, so the curve drops steeply at first and then flattens.")}
import math
SR = [[x, round(6 + 92 / (1 + math.exp(-(x - 50) / 9)), 2)] for x in range(2, 101, 4)]
SALES = {"title": "The Sales Response Function", "axes": AX("Annual marketing effort ($)", "Annual sales\nrevenue ($)"),
    "curves": [{"id": "s", "label": "", "pts": SR, "curved": True, "color": "gold"}],
    "caption": cap("Sales respond slowly to the first marketing dollars, rise fastest in the middle range, and flatten once the market is saturated.")}
def modern_head(t):
    # the current house head: the Red Hat Display font links, then the v6 stylesheet (the file had neither, so its text set in a fallback font)
    t = re.sub(r'<link rel="stylesheet" href="https://smokinnotes\.s3\.us-east-1\.amazonaws\.com/content/sn25-v5\.css">',
               '<link rel="preconnect" href="https://fonts.googleapis.com">\n    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n    <link href="https://fonts.googleapis.com/css2?family=Red+Hat+Display:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">\n    <link rel="stylesheet" href="https://smokinnotes.s3.us-east-1.amazonaws.com/content/sn25-v6.css">', t, 1)
    t = re.sub(r'<script src="https://smokinnotes\.s3\.us-east-1\.amazonaws\.com/content/sn25-v5\.js"></script>', '<script src="https://smokinnotes.s3.us-east-1.amazonaws.com/studyguide/sn25-v2.js"></script>', t, 1)
    assert "sn25-v6.css" in t and "studyguide/sn25-v2.js" in t, "head"
    return t
def bcg_fig():
    """The BCG matrix drawn: the four quadrants in the picture's own tints, a simple icon in each."""
    x0, y0, c = 120, 70, 150; b = ""
    tints = ["#d9d3ea", "#f8c9ad", "#e8dbb6", "#bfe0ea"]; names = ["Question Mark", "Star", "Dog", "Cash Cow"]
    for i in range(4):
        x = x0 + (i % 2) * c; y = y0 + (i // 2) * c
        b += f'<rect x="{x}" y="{y}" width="{c}" height="{c}" fill="{tints[i]}" stroke="#fff" stroke-width="3"/>'
        b += text(x + c / 2, y + c - 16, names[i], 15)
    cx, cy = x0 + c / 2, y0 + c / 2
    b += f'<text x="{cx}" y="{cy + 22}" text-anchor="middle" font-size="78" font-weight="800" fill="#7a6ea6">?</text>'
    import math
    cx, cy = x0 + 1.5 * c, y0 + c / 2 - 6; pts = []
    for k in range(10):
        r = 44 if k % 2 == 0 else 18; a = -math.pi / 2 + k * math.pi / 5; pts.append(f"{cx + r*math.cos(a):.1f},{cy + r*math.sin(a):.1f}")
    b += f'<polygon points="{" ".join(pts)}" fill="#f26b1f" stroke="#c74e0e" stroke-width="2"/>'
    # the dog: a round head, two floppy ears, eyes, a nose
    cx, cy = x0 + c / 2, y0 + 1.5 * c - 8
    b += f'<ellipse cx="{cx - 34}" cy="{cy + 4}" rx="12" ry="24" fill="#a9754a"/><ellipse cx="{cx + 34}" cy="{cy + 4}" rx="12" ry="24" fill="#a9754a"/>'
    b += f'<circle cx="{cx}" cy="{cy}" r="34" fill="#d9ab7c" stroke="#a9754a" stroke-width="2"/>'
    b += f'<circle cx="{cx - 12}" cy="{cy - 6}" r="4" fill="#2b343c"/><circle cx="{cx + 12}" cy="{cy - 6}" r="4" fill="#2b343c"/><ellipse cx="{cx}" cy="{cy + 10}" rx="7" ry="5" fill="#2b343c"/>'
    # the cash cow, in the dog's style: a round white face with black patches, ears and horns, a pink muzzle, a coin held under its chin
    cx, cy = x0 + 1.5 * c, y0 + 1.5 * c - 12
    b += f'<ellipse cx="{cx - 36}" cy="{cy - 4}" rx="13" ry="9" fill="#e8c7c7" stroke="#2b343c" stroke-width="1.5"/><ellipse cx="{cx + 36}" cy="{cy - 4}" rx="13" ry="9" fill="#e8c7c7" stroke="#2b343c" stroke-width="1.5"/>'
    b += f'<path d="M {cx - 22} {cy - 26} q -14 -16 -4 -28 q 10 10 12 22 z" fill="#e9d8a6" stroke="#2b343c" stroke-width="1.5"/><path d="M {cx + 22} {cy - 26} q 14 -16 4 -28 q -10 10 -12 22 z" fill="#e9d8a6" stroke="#2b343c" stroke-width="1.5"/>'
    b += f'<ellipse cx="{cx}" cy="{cy}" rx="34" ry="32" fill="#fff" stroke="#2b343c" stroke-width="2"/>'
    # one patch over each eye, mirror images of each other
    b += f'<path d="M {cx - 28} {cy - 16} q 8 -14 22 -8 q 2 12 -8 18 q -12 2 -14 -10 z" fill="#2b343c"/><path d="M {cx + 28} {cy - 16} q -8 -14 -22 -8 q -2 12 8 18 q 12 2 14 -10 z" fill="#2b343c"/>'
    b += f'<circle cx="{cx - 11}" cy="{cy - 4}" r="4" fill="#2b343c"/><circle cx="{cx + 11}" cy="{cy - 4}" r="4" fill="#2b343c"/>'
    b += f'<ellipse cx="{cx}" cy="{cy + 14}" rx="18" ry="11" fill="#f2b8c6" stroke="#2b343c" stroke-width="1.5"/><circle cx="{cx - 6}" cy="{cy + 14}" r="2.2" fill="#2b343c"/><circle cx="{cx + 6}" cy="{cy + 14}" r="2.2" fill="#2b343c"/>'
    b += f'<circle cx="{cx + 26}" cy="{cy + 30}" r="15" fill="#3f8fa6" stroke="#2b6f84" stroke-width="2"/><text x="{cx + 26}" y="{cy + 36}" text-anchor="middle" font-size="18" font-weight="800" fill="#fff">$</text>'
    # the axes
    b += text(x0 + c, 24, "Relative Market Share (RMS)", 15)
    b += f'<text x="{x0 + c/2}" y="52" text-anchor="middle" font-size="13" fill="{INK}"><tspan font-weight="800">Low</tspan> (&lt; 1)</text><text x="{x0 + 1.5*c}" y="52" text-anchor="middle" font-size="13" fill="{INK}"><tspan font-weight="800">High</tspan> (&gt; 1)</text>'
    b += f'<text transform="translate(36 {y0 + c}) rotate(-90)" text-anchor="middle" font-size="15" font-weight="800" fill="{INK}">Market Growth Rate</text>'
    b += f'<text transform="translate(92 {y0 + c/2}) rotate(-90)" text-anchor="middle" font-size="13" fill="{INK}"><tspan font-weight="800">High</tspan> (&gt; 10%)</text><text transform="translate(92 {y0 + 1.5*c}) rotate(-90)" text-anchor="middle" font-size="13" fill="{INK}"><tspan font-weight="800">Low</tspan> (&lt; 10%)</text>'
    return fig(440, 390, b, "The BCG matrix: question marks and stars in high-growth markets, dogs and cash cows in low-growth ones; stars and cash cows hold high relative market share", 400, "narrow", True)

def chapter2(src, outA, outB):
    t = modern_head(open(src, encoding="utf-8").read())
    t = sub1(t, "Dr. Cooke noted that Google restructured under Alphabet", "Google restructured under Alphabet", "cooke ch2")
    # the opening paragraph goes under the table of contents and above the first heading, never in the contents
    t = sub1(t, "<p>We have finished our discussion of the 4 P's of the marketing mix,", '<p id="intro-note"><i>We have finished our discussion of the 4 P\'s of the marketing mix,', "ch2 blurb")
    i = t.index('<p id="intro-note">'); j = t.index("</p>", i); t = t[:j] + "</i></p>" + t[j + 4:]
    t = sub1(t, "</head>", "<script>document.addEventListener('DOMContentLoaded', function () { var b = document.getElementById('intro-note'), t = document.querySelector('details.toc-box'); if (b && t) b.parentNode.insertBefore(t, b); });</script>\n</head>", "ch2 blurb script")
    open(outA, "w", encoding="utf-8").write(t)   # version A: as it is, images kept
    b = replace_img(t, "01-bcg-matrix.png", bcg_fig()["html"])
    b = replace_img(b, "02-experience-curve.png", widget(EXPERIENCE))
    b = replace_img(b, "03-sales-response-curve.png", widget(SALES))
    finish(b, outB)

if __name__ == "__main__":
    src13, src2, outdir = sys.argv[1:4]; os.makedirs(outdir, exist_ok=True)
    chapter13(src13, os.path.join(outdir, "MAR3023-263-Exam3-Ch13-Ch14-FULL.html"))
    chapter2(src2, os.path.join(outdir, "MAR3023-263-Exam3-Chapter2-Part1-FULL.html"), os.path.join(outdir, "MAR3023-263-Exam3-Chapter2-Part1-FULL-svg.html"))
    print("written to", outdir)
