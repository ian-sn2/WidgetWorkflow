"""Static SVG figures for the ACG2021 / ACG2071 / ACG3173 / MAN3025 UCF set
(2026-10-27): 2x2 grids, pyramids, spoke diagrams, trees and rings -- the
pictures the decision table calls "a static drawing". Helpers come from the
MAR3203 build so every drawing shares one look."""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "mar3203"))
from common import (svg, box, circle, ellipse, arrow, path, text, html, INK, GOLDC, PALEG, GREY, RED, CSS)

FIGCSS = CSS.replace("</style>", """
  .sk-fig.right { float: right; width: 40%; max-width: 420px; margin: 4px 0 10px 22px; }
  .sk-fig.narrow { max-width: 420px; }
  .sk-fig.tiny { max-width: 300px; }
  @media (max-width: 700px) { .sk-fig.right { float: none; width: 100%; margin: 12px auto; } }
</style>""")
import itertools
_uid = itertools.count(1)
def fig(w, h, body, aria, maxw=None, cls="", first=False):
    # one marker id per figure: a page shows several figures, and the deck keeps most of them hidden, where a
    # shared "skah" marker in a display:none section paints no arrowhead anywhere (Ian saw no arrows, 2026-10-27)
    s = svg(w, h, body, aria, maxw, cls).replace("skah", "skah%d" % next(_uid))
    return {"html": (FIGCSS if first else "") + s}
DEEP, MID, PALE, FAINT = "#c9a633", "#dcc470", "#efe3b0", "#f8f1d8"

# ------------------------------------------------------------- 2 x 2 grids
def grid2x2(cells, fills=None, top=None, left=None, cols=None, rows=None, bottom=None, right=None,
            w=460, h=400, cell=150, fs=15, aria="", oval=None, maxw=420, cls="narrow", first=False):
    """cells: TL, TR, BL, BR. top/left/bottom/right: axis titles. cols/rows: the two labels along each axis."""
    x0 = 120 if left else 50; y0 = 90 if top else 40
    b = ""
    fills = fills or [PALE, FAINT, PALE, FAINT]
    for i, (t, f) in enumerate(zip(cells, fills)):
        x = x0 + (i % 2) * cell; y = y0 + (i // 2) * cell
        b += box(x, y, cell, cell, t, fill=f, fs=fs, rx=0, lh=fs + 3)
    if top: b += text(x0 + cell, y0 - 60, top, 15, bold=True)
    if cols: b += text(x0 + cell / 2, y0 - 22, cols[0], 13, bold=False, italic=True) + text(x0 + cell * 1.5, y0 - 22, cols[1], 13, bold=False, italic=True)
    if left: b += f'<text transform="translate({x0 - 80} {y0 + cell}) rotate(-90)" text-anchor="middle" font-size="15" font-weight="800" fill="{INK}">{left}</text>'
    if rows:
        for j, r in enumerate(rows):
            b += f'<text transform="translate({x0 - 30} {y0 + cell * (j + 0.5)}) rotate(-90)" text-anchor="middle" font-size="13" font-style="italic" fill="{INK}">{r}</text>'
    if bottom: b += text(x0 + cell, y0 + 2 * cell + 34, bottom, 15)
    if right: b += f'<text transform="translate({x0 + 2 * cell + 40} {y0 + cell}) rotate(90)" text-anchor="middle" font-size="15" font-weight="800" fill="{INK}">{right}</text>'
    if oval: b += ellipse(x0 + cell, y0 + cell, 92, 38, oval, fill="#fff", fs=15)
    W = x0 + 2 * cell + (70 if right else 40); H = y0 + 2 * cell + (56 if bottom else 30)
    return fig(W, H, b, aria, maxw, cls, first)

# ------------------------------------------------------------- pyramids
def pyramid(levels, w=440, h=330, fills=None, numbered=False, aria="", maxw=380, cls="narrow", first=False, fs=15, weights=None, dashed_after=None):
    """levels top to bottom, each a text. A triangle cut into bands. The apex band is sized to its own name: the
    shortest band in which the name sits vertically centred without touching the sides, at the largest size up to
    two points under `fs` (Ian, 2026-10-27: centred in its band, the line moved up)."""
    n = len(levels); fills = fills or [DEEP, MID, PALE, FAINT, "#fcf8ea"][:n]
    cx, top, base, bw = w / 2, 16, h - 16, w - 40; H = base - top
    def apex_height(size):   # the band height that puts the name's top where the triangle is wide enough for it
        need = (0.56 * size * len(levels[0]) + 12) * H / bw   # distance below the apex at which the width clears the name
        return 2 * (need + 0.37 * size)
    size0 = fs - 2   # a step below the other names: centred in the tip, a full-size name would need half the pyramid
    h0 = apex_height(size0); rest = (H - h0) / (n - 1)
    edges = [top, top + h0] + [top + h0 + rest * k for k in range(1, n)]
    b = ""
    for i, (t, fl) in enumerate(zip(levels, fills)):
        y1, y2 = edges[i], edges[i + 1]
        w1 = bw * (y1 - top) / H; w2 = bw * (y2 - top) / H
        b += f'<polygon points="{cx - w1/2:.1f},{y1:.1f} {cx + w1/2:.1f},{y1:.1f} {cx + w2/2:.1f},{y2:.1f} {cx - w2/2:.1f},{y2:.1f}" fill="{fl}" stroke="{INK}" stroke-width="1.4"/>'
        if dashed_after == i: b += f'<line x1="{cx - w2/2:.1f}" y1="{y2:.1f}" x2="{cx + w2/2:.1f}" y2="{y2:.1f}" stroke="#fff" stroke-width="1.6" stroke-dasharray="6 5"/>'
        ym = (y1 + y2) / 2; size = size0 if i == 0 else fs
        b += text(cx, ym + size * 0.37, t, size, lh=size + 2)
        if numbered:
            wm = bw * (ym - top) / H; b += text(cx - wm / 2 - 14, ym + 4, str(n - i), 12, bold=True, color=GREY)
    return fig(w, h, b, aria, maxw, cls, first)

def vbrace(x, y1, y2, side="left", sw=1.8):
    """A curly brace from y1 to y2 whose tip points to `side` at x (the tip is 10px out from the arms)."""
    d = -10 if side == "left" else 10; m = (y1 + y2) / 2
    return path(f"M {x - d} {y1} C {x - d/2} {y1} {x} {y1} {x} {y1 + 10} L {x} {m - 10} C {x} {m - 2} {x + d/2} {m} {x + d} {m} C {x + d/2} {m} {x} {m + 2} {x} {m + 10} L {x} {y2 - 10} C {x} {y2} {x - d/2} {y2} {x - d} {y2}", head=False, sw=sw)
def hbrace(x1, x2, y, tip="up", sw=1.8):
    """A curly brace from x1 to x2 at y, its tip pointing up (over a run of boxes) or down."""
    d = -10 if tip == "up" else 10; m = (x1 + x2) / 2
    return path(f"M {x1} {y - d} C {x1} {y - d/2} {x1} {y} {x1 + 10} {y} L {m - 10} {y} C {m - 2} {y} {m} {y + d/2} {m} {y + d} C {m} {y + d/2} {m + 2} {y} {m + 10} {y} L {x2 - 10} {y} C {x2} {y} {x2} {y - d/2} {x2} {y - d}", head=False, sw=sw)

# ------------------------------------------------------------- spokes
def spoke(center, items, w=520, h=420, r=52, aria="", maxw=440, cls="narrow", first=False, dark_center=True):
    cx, cy, R = w / 2, h / 2, min(w, h) / 2 - r - 6
    b = ""
    for i, t in enumerate(items):
        a = -math.pi / 2 + 2 * math.pi * i / len(items)
        x, y = cx + R * math.cos(a), cy + R * math.sin(a)
        b += arrow(cx + 70 * math.cos(a), cy + 70 * math.sin(a), x - (r + 2) * math.cos(a), y - (r + 2) * math.sin(a), sw=2.5, head=False)
        b += circle(x, y, r, t, fill=PALE, fs=12.5, lh=14)
    b += circle(cx, cy, 70, center, fill=INK if dark_center else PALE, fs=16, lh=19) if not dark_center else \
         f'<circle cx="{cx}" cy="{cy}" r="70" fill="{INK}"/>' + text(cx, cy + 5 - (center.count("\n")) * 9.5, center, 16, color="#fff", lh=19)
    return fig(w, h, b, aria, maxw, cls, first)

# ------------------------------------------------------------- ACG2021
def accounting_equation():
    b = text(300, 34, "Assets = Liabilities + Stockholders’ Equity", 20, color="#1f3a7a")
    b += arrow(78, 90, 78, 46, sw=1.8) + text(78, 112, "Business’s\nresources", 12.5, bold=False, color="#1f3a7a", lh=15)
    b += arrow(340, 90, 300, 46, sw=1.8) + arrow(340, 90, 445, 46, sw=1.8) + text(340, 112, "Claims to\nresources", 12.5, bold=False, color="#1f3a7a", lh=15)
    return fig(600, 140, b, "The accounting equation: assets are the business's resources; liabilities and stockholders' equity are claims to them", 520, "narrow", True)
def se_flow():
    b = text(300, 30, "", 1)
    b += f'<text x="300" y="30" text-anchor="middle" font-size="16" font-weight="800" fill="{INK}"><tspan fill="#1f3a7a">Stockholders’ equity</tspan> = Paid in capital (stock) + Retained earnings</text>'
    b += arrow(478, 42, 420, 86) + arrow(478, 42, 478, 86) + arrow(478, 42, 536, 86)
    b += text(478, 106, "Revenue – Expenses – Dividends", 15, color="#1f3a7a")
    b += arrow(420, 116, 462, 150) + arrow(536, 116, 494, 150)
    b += text(478, 170, "Net Income", 15, color="#1f3a7a")
    return fig(760, 190, b, "Stockholders' equity is paid-in capital plus retained earnings; retained earnings grow by revenue less expenses and dividends, which is net income", 620, "", False)
def taccount(x, y, title, w=130, up_left=True, fs=12):
    """A T-account with a debit and a credit column and an arrow in each: up on the increase side."""
    b = text(x + w / 2, y, title, fs, color="#1f3a7a")
    b += f'<line x1="{x}" y1="{y + 8}" x2="{x + w}" y2="{y + 8}" stroke="{INK}" stroke-width="1.4"/>'
    b += f'<line x1="{x + w/2}" y1="{y + 8}" x2="{x + w/2}" y2="{y + 70}" stroke="{INK}" stroke-width="1.4"/>'
    b += text(x + w / 4, y + 23, "Debit", 11, color="#1f3a7a") + text(x + 3 * w / 4, y + 23, "Credit", 11, color="#1f3a7a")
    for k, (cx, up) in enumerate([(x + w / 4, up_left), (x + 3 * w / 4, not up_left)]):
        col = GOLDC if up else "#e06666"
        pts = f"{cx},{y+34} {cx+10},{y+47} {cx+5},{y+47} {cx+5},{y+68} {cx-5},{y+68} {cx-5},{y+47} {cx-10},{y+47}" if up else \
              f"{cx},{y+68} {cx+10},{y+55} {cx+5},{y+55} {cx+5},{y+34} {cx-5},{y+34} {cx-5},{y+55} {cx-10},{y+55}"
        b += f'<polygon points="{pts}" fill="{col}" stroke="{INK}" stroke-width="0.8"/>'
    return b
def debit_credit():
    b = ""
    b += text(100, 24, "Assets", 13, color="#1f3a7a") + text(222, 60, "=", 24) + text(340, 24, "Liabilities", 13, color="#1f3a7a") + text(462, 60, "+", 24) + text(600, 24, "Stockholders’ Equity", 13, color="#1f3a7a")
    b += taccount(40, 34, "", up_left=True) + taccount(280, 34, "", up_left=False) + taccount(540, 34, "", up_left=False)
    b += arrow(600, 112, 450, 150) + arrow(600, 112, 740, 150)
    b += text(445, 170, "Common Stock", 12, color="#1f3a7a") + text(595, 216, "+", 24) + text(740, 170, "Retained Earnings", 12, color="#1f3a7a")
    b += taccount(385, 180, "", up_left=False) + taccount(680, 180, "", up_left=False)
    b += arrow(740, 258, 330, 300) + arrow(740, 258, 600, 300) + arrow(740, 258, 800, 300)
    b += text(330, 320, "Revenue", 12, color="#1f3a7a") + text(470, 366, "−", 24) + text(600, 320, "Expenses", 12, color="#1f3a7a") + text(700, 366, "−", 24) + text(800, 320, "Dividends", 12, color="#1f3a7a")
    b += taccount(270, 330, "", up_left=False) + taccount(540, 330, "", up_left=True) + taccount(740, 330, "", up_left=True)
    b += f'<rect x="525" y="304" width="350" height="110" fill="none" stroke="{RED}" stroke-width="2"/>'
    b += vbrace(22, 14, 268, "left", 2.2) + text(30, 138, "permanent\naccounts", 12, anchor="start", bold=True, italic=True, color="#1f3a7a", lh=14)
    b += vbrace(22, 304, 412, "left", 2.2) + text(30, 354, "temporary\naccounts", 12, anchor="start", bold=True, italic=True, color="#1f3a7a", lh=14)
    return fig(900, 425, b, "Debits increase assets, expenses and dividends; credits increase liabilities, stockholders' equity, common stock, retained earnings and revenue. Revenue, expenses and dividends are temporary accounts", 820, "", True)
def accounting_cycle():
    steps = ["Beginning of\nAccounting\nPeriod", "Transactions", "Record Journal\nEntries", "Post to Ledger", "Unadjusted\nTrial\nBalance", "Adjusting\nEntries",
             "Adjusted\nTrial\nBalance", "Income\nStatement", "Statement of\nStockholders’\nEquity", "Balance Sheet", "Cash Flow\nStatement", "Closing\nEntries"]
    cx, cy, R, n, fs = 360, 320, 250, len(steps), 10.5; b = ""
    # each name sits on the ring; the arrow from one name runs along the ring and points at the next (Ian, 2026-10-27)
    def half_angle(t, a):
        lines = t.split("\n"); wd = 0.56 * fs * max(len(l) for l in lines); ht = len(lines) * (fs + 1.5)
        return ((wd / 2) * abs(math.sin(a)) + (ht / 2) * abs(math.cos(a)) + 7) / R   # the name's reach along the ring's tangent
    angs = [-math.pi / 2 + 2 * math.pi * i / n for i in range(n)]
    for i, t in enumerate(steps):
        a = angs[i]; lx, ly = cx + R * math.cos(a), cy + R * math.sin(a)
        b += text(lx, ly + 4 - t.count("\n") * (fs + 1.5) / 2, t, fs, lh=fs + 1.5)
        a1 = angs[(i + 1) % n]; s0 = a + half_angle(t, a); s1 = a1 + (2 * math.pi if i == n - 1 else 0) - half_angle(steps[(i + 1) % n], a1)
        if s1 - s0 > 0.08:
            b += path(f"M {cx + R*math.cos(s0):.1f} {cy + R*math.sin(s0):.1f} A {R} {R} 0 0 1 {cx + R*math.cos(s1):.1f} {cy + R*math.sin(s1):.1f}", sw=1.7, color=GOLDC)
    b += text(cx, cy - 10, "The\nAccounting\nCycle", 17, lh=21)
    return fig(720, 640, b, "The accounting cycle as a ring: transactions, journal entries, ledger, unadjusted trial balance, adjusting entries, adjusted trial balance, the four statements, closing entries, and round again", 520, "narrow", True)
def fraud_triangle():
    A, Bp, C = (330, 20), (30, 290), (630, 290); cx, cy = 330, 200
    b = f'<polygon points="{A[0]},{A[1]} {C[0]},{C[1]} {Bp[0]},{Bp[1]}" fill="{PALE}" stroke="{INK}" stroke-width="1.5"/>'
    for P in (A, Bp, C): b += f'<line x1="{cx}" y1="{cy}" x2="{P[0]}" y2="{P[1]}" stroke="{INK}" stroke-width="1.2"/>'
    def rot(x, y, ang, first, rest):
        return (f'<text transform="translate({x} {y}) rotate({ang})" text-anchor="middle" font-size="13" font-weight="600" fill="{INK}"><tspan font-weight="900" font-size="14">{first}</tspan>{rest}</text>')
    # each name sits at the centroid of its own region, turned to run along that region's outer side
    b += rot(228, 160, -42, "Motivation", " – the need or") + rot(240, 176, -42, "", "pressure to commit fraud")
    b += rot(432, 160, 42, "Opportunity", " – the right situation") + rot(420, 176, 42, "", "occurs for fraud to take place")
    b += f'<text x="330" y="250" text-anchor="middle" font-size="13" font-weight="600" fill="{INK}"><tspan font-weight="900" font-size="14">Rationalization</tspan> – justification for</text>' + text(330, 267, "committing the fraud", 13, bold=False)
    return fig(660, 300, b, "The fraud triangle: motivation, opportunity and rationalization", 560, "", True)
def controls_summary():
    b = box(230, 10, 140, 30, "Internal Controls", fill=PALE, fs=13) + arrow(300, 40, 300, 58, sw=2.4)
    b += box(170, 60, 260, 30, "Prevent fraud and safeguard assets", fill=INK, fs=12.5, color="#fff") + arrow(300, 90, 300, 110, sw=2.4)
    b += f'<polygon points="300,112 180,212 420,212" fill="{MID}" stroke="{INK}" stroke-width="1.4"/>'
    b += text(300, 150, "Monitoring\nControl Activities\nRisk Assessment\nControl Environment", 11.5, lh=15)
    b += hbrace(40, 560, 240, "up", 2)
    for i, t in enumerate(["Reconciliations", "Separation\nof Duties", "Employee\nIncentives", "Authorizations"]):
        b += box(40 + i * 135, 262, 120, 44, t, fill=PALE, fs=12, lh=14)
    return fig(600, 318, b, "Internal controls prevent fraud and safeguard assets through the four-level framework and four kinds of control: reconciliations, separation of duties, employee incentives and authorizations", 520, "narrow", False)
def statements_flow():
    return {"flow": {"nodes": [{"text": "Income\nStatement", "w": 0.9}, {"text": "Statement of\nStockholders’ Equity", "w": 1.5}, {"text": "Balance\nSheet", "w": 0.9}, {"text": "Cash Flow\nStatement", "w": 0.9}], "links": [{"style": "arrow"}, {"style": "arrow"}, {"style": "arrow"}]},
            "title": "The Four Financial Statements", "caption": "Net income flows into the statement of stockholders’ equity, its ending balances into the balance sheet, and the cash balance is explained by the cash flow statement."}

# ------------------------------------------------------------- ACG2071
def master_budget():
    b = ""
    def B(x, y, w, t, fs=11.5): return box(x, y, w, 40, t, fill=PALE, fs=fs, lh=13, rx=10)
    A = lambda x1, y1, x2, y2: arrow(x1, y1, x2, y2, sw=2)
    b += B(230, 10, 120, "Sales Budget") + A(290, 50, 290, 64)
    b += B(230, 66, 120, "Production\nBudget") + A(290, 106, 290, 132)
    b += f'<line x1="150" y1="120" x2="430" y2="120" stroke="{INK}" stroke-width="2"/>'
    for x, t in [(90, "Direct\nMaterials\nBudget"), (230, "Direct\nLabor\nBudget"), (370, "Manufacturing\nOverhead\nBudget")]:
        if x != 230: b += A(x + 60, 120, x + 60, 132)
        b += box(x, 134, 120, 50, t, fill=PALE, fs=11, lh=12.5, rx=10)
        b += f'<line x1="{x + 60}" y1="184" x2="{x + 60}" y2="198" stroke="{INK}" stroke-width="2"/>'
    b += f'<line x1="150" y1="198" x2="430" y2="198" stroke="{INK}" stroke-width="2"/>' + A(290, 198, 290, 210)
    b += B(230, 212, 120, "SG&A Budget") + A(290, 252, 290, 266)
    b += B(230, 268, 120, "Budgeted\nIncome\nStatement", 11) + A(290, 308, 290, 336)
    for x, t in [(30, "Capital\nExpenditure\nBudget"), (230, "Cash\nBudget"), (430, "Budgeted\nBalance\nSheet")]:
        b += box(x, 338, 120, 50, t, fill=PALE, fs=11, lh=12.5, rx=10)
    b += A(150, 363, 228, 363) + A(350, 363, 428, 363)
    b += vbrace(30, 12, 308, "left", 1.6) + f'<text transform="translate(12 160) rotate(-90)" text-anchor="middle" font-size="11" font-style="italic" font-weight="700" fill="{INK}">operating budgets</text>'
    b += hbrace(30, 550, 398, "down", 1.6) + text(290, 426, "financial budgets", 11, bold=True, italic=True)
    return fig(600, 436, b, "The master budget for a manufacturer: the sales budget drives production, the three manufacturing budgets and SG&A into the budgeted income statement, then the capital expenditure, cash and budgeted balance sheet budgets", 500, "narrow", True)
def wip_flow():
    b = ""
    for i, t in enumerate(["Raw\nMaterials\nInventory", "WIP\nInventory", "Finished\nGoods\nInventory", "Cost of\nGoods Sold\n(COGS)"]):
        x = 20 + i * 190; b += box(x, 20, 130, 64, t, fill=DEEP if i != 1 else PALE, fs=12.5, lh=14, rx=6, color=INK)
        if i < 3: b += f'<polygon points="{x+136},{44} {x+166},{44} {x+166},{36} {x+186},{52} {x+166},{68} {x+166},{60} {x+136},{60}" fill="{INK}"/>'
    b += text(561, 14, "SALE", 12)
    b += f'<line x1="275" y1="84" x2="275" y2="209" stroke="{INK}" stroke-width="1.8"/>' + arrow(275, 209, 298, 209, sw=1.8)
    b += text(338, 206, "Subsidiary\nAccounts", 10.5, bold=True, lh=12) + vbrace(392, 100, 318, "left", 1.8)
    for t, y in [("Product 1\nDirect materials\nDirect labor\nOverhead", 100), ("Product 2\nDirect materials\nDirect labor\nOverhead", 170), ("Product 99\nDirect materials\nDirect labor\nOverhead", 262)]:
        b += box(408, y, 130, 56, t, fill=DEEP, fs=10.5, lh=12, rx=4)
    b += text(473, 248, "• • •", 12)
    return fig(760, 330, b, "Costs flow from raw materials to work in process to finished goods and, on sale, to cost of goods sold; each product has its own subsidiary WIP account of direct materials, direct labor and overhead", 640, "", True)

# ------------------------------------------------------------- MAN3025
def management_pyramid():
    A, L, R = (210, 30), (20, 300), (400, 300); b = f'<polygon points="{A[0]},{A[1]} {R[0]},{R[1]} {L[0]},{L[1]}" fill="{FAINT}" stroke="{INK}" stroke-width="2"/>'
    levels = [("Top Managers", 0.16), ("Middle\nManagers", 0.34), ("First-Line\nManagers", 0.53), ("Team Leaders", 0.71), ("Nonmanagerial\nEmployees", 0.88)]
    prev = 0
    for i, (t, f) in enumerate(levels):
        y = A[1] + (300 - A[1]) * f; half = (y - A[1]) * (190 / 270)
        if i < 4: b += f'<line x1="{210 - half}" y1="{y}" x2="{210 + half}" y2="{y}" stroke="{INK}" stroke-width="1.6"/>'
        ym = (A[1] + (300 - A[1]) * prev + y) / 2; xr = 210 + (ym - A[1]) * (190 / 270) + 12
        b += text(xr, ym + 4 - t.count("\n") * 7, t, 13, anchor="start", bold=True, lh=15); prev = f
    for k, t in enumerate(["R&D", "Marketing", "Finance", "Production", "HR"]):
        x = 58 + k * 76
        if k: b += f'<line x1="{210}" y1="{A[1] + 8}" x2="{x - 38}" y2="300" stroke="#8fa3d9" stroke-width="1"/>'
        b += text(x, 320, t, 11)
    return fig(560, 330, b, "The management pyramid: top, middle and first-line managers, team leaders and nonmanagerial employees, sliced vertically into functional areas", 480, "narrow", True)
def systems_view():
    b = text(60, 44, "Inputs", 15) + arrow(100, 40, 186, 40, sw=2.6) + box(190, 12, 180, 56, "Transformation\nProcesses", fill=PALE, fs=14, lh=17) + arrow(372, 40, 456, 40, sw=2.6) + text(510, 44, "Outputs", 15)
    b += path("M 510 56 L 510 100 L 60 100 L 60 58", dashed=True, sw=2.2) + text(285, 118, "Feedback", 13, italic=True)
    return fig(580, 130, b, "The systems viewpoint: inputs go through transformation processes to outputs, and feedback returns to the inputs", 520, "narrow", True)
def decision_tree():
    b = ""
    def q(x, y, t, fs=11.5): return text(x, y, t, fs, anchor="start", lh=13)
    b += q(10, 160, "Is the action\nlegal?")
    b += arrow(90, 148, 150, 112) + text(112, 118, "YES", 8) + arrow(90, 165, 150, 204) + text(106, 202, "NO", 8)
    b += q(156, 96, "Does the action\nmaximize\nshareholder\nvalue?") + q(156, 214, "Don’t do it.")
    b += arrow(262, 86, 322, 44) + text(288, 56, "YES", 8) + arrow(262, 120, 322, 184) + text(280, 170, "NO", 8)
    b += q(328, 42, "Is the action\nethical?") + text(328, 72, "(Weigh the effect on the\ncommunity, customers,\nemployees, supplier, and the\nenvironment against the\nbenefit to shareholders.)", 7.5, anchor="start", bold=False, lh=9)
    b += q(328, 176, "Would it be\nethical to not\ntake the action?") + text(328, 220, "(Weigh the cost imposed on\nshareholders against the\nbenefit to other stakeholders.)", 7.5, anchor="start", bold=False, lh=9)
    b += arrow(446, 36, 492, 20) + text(468, 18, "YES", 8) + q(498, 24, "Do it.")
    b += arrow(446, 50, 492, 84) + text(456, 82, "NO", 8) + q(498, 88, "Don’t do it.")
    b += arrow(446, 174, 492, 160) + text(466, 160, "YES", 8) + q(498, 164, "Don’t do it.")
    b += arrow(446, 192, 492, 236) + text(454, 230, "NO", 8) + q(498, 228, "Do it, but\ndisclose the\neffect to\nshareholders.")
    return fig(600, 290, b, "A decision tree for a managerial decision: is it legal, does it maximize shareholder value, is it ethical, and would it be ethical not to act", 640, "", True)
def diversity_wheel():
    b = ""
    for r, t, dy in [(170, "Organizational\nDimensions", -150), (128, "External\nDimensions", -108), (86, "Internal\nDimensions", -66), (40, "Personality", 4)]:
        b += f'<circle cx="200" cy="200" r="{r}" fill="none" stroke="{INK}" stroke-width="2"/>' + text(200, 200 + dy, t, 12, lh=14)
    return fig(400, 400, b, "The diversity wheel: personality at the centre, then internal, external and organizational dimensions", 340, "tiny", True)
def carroll():
    return pyramid(["Philanthropic", "Ethical", "Legal", "Economic"], w=640, h=300, fills=[DEEP, MID, PALE, FAINT], dashed_after=2,
                   aria="Carroll's pyramid of corporate social responsibility: economic, legal, ethical and philanthropic responsibilities", cls="right", maxw=None, first=True, fs=15)
def maslow():
    return pyramid(["Self-Actualization", "Esteem", "Social", "Safety", "Physiological"], fills=[DEEP, MID, PALE, FAINT, "#fff"],
                   aria="Maslow's hierarchy of needs from physiological at the base to self-actualization at the top", first=True, fs=15, w=640, h=300)
def controls_pyramid():
    return pyramid(["Monitoring", "Control Activities", "Risk Assessment", "Control Environment"], w=640, h=300, fills=[FAINT, PALE, MID, DEEP], numbered=True,
                   aria="The internal-control framework as a pyramid: control environment, risk assessment, control activities, monitoring", maxw=480, fs=16)
