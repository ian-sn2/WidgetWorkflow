"""Shared pieces for the MAR3203 (UCF operations management) build: the
house-neutral CSS the HTML figures ride on, SVG helpers, the bell curve, and
the map writer. Every chapter module imports from here."""
import json, math, os, pathlib

WORK = pathlib.Path(os.environ.get("MAR_WORK", pathlib.Path(__file__).resolve().parent))
MAPS = WORK / "maps"; MAPS.mkdir(exist_ok=True)

def cap(s, n=200):
    assert len(s) <= n, (len(s), s); return s
NOPT = {"guides": False, "showP": False, "showQ": False}
def dots(pts, **extra):
    return [dict({"q": x, "p": y}, **NOPT, **extra) for x, y in pts]
def label(q, p, text, dx=0, dy=0, **extra):
    return dict({"q": q, "p": p, "dot": False, "label": text, "dx": dx, "dy": dy}, **NOPT, **extra)
GOLD = {"color": "gold", "opacity": 0.55}
PALE = {"color": "gold", "opacity": 0.22}

# ---------------------------------------------------------------- bells
def bell(mu, sig, peak=100, lo=-3.6, hi=3.6, step=0.2, xlo=None, xhi=None):
    pts, k = [], lo
    while k <= hi + 1e-9:
        x = mu + k * sig
        if (xlo is None or x >= xlo) and (xhi is None or x <= xhi):
            pts.append([round(x, 3), round(peak * math.exp(-k * k / 2), 2)])
        k += step
    return pts
def interp(pts, x):
    for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
        if xa <= x <= xb: return round(ya + (yb - ya) * (x - xa) / (xb - xa), 2)
    raise ValueError(x)
def under(pts, x1=None, x2=None, base=0):
    # a bound outside the curve's own range is the whole curve on that side
    if x1 is not None and x1 <= pts[0][0]: x1 = None
    if x2 is not None and x2 >= pts[-1][0]: x2 = None
    sel = [p for p in pts if (x1 is None or p[0] > x1) and (x2 is None or p[0] < x2)]
    if x1 is not None: sel = [[round(x1, 3), interp(pts, x1)]] + sel
    if x2 is not None: sel = sel + [[round(x2, 3), interp(pts, x2)]]
    return [[sel[0][0], base]] + sel + [[sel[-1][0], base]]

# ---------------------------------------------------------------- HTML figures
CSS = """<style>
  .sk-fig { margin: 18px auto; max-width: 640px; }
  .sk-fig svg { display: block; width: 100%; height: auto; font-family: 'Red Hat Display', 'Segoe UI', sans-serif; }
  .sk-fig figcaption { text-align: center; font-size: 0.9em; color: #444; margin-top: 6px; }
  .sk-tbl { border-collapse: collapse; margin: 18px auto; font-family: 'Red Hat Display', 'Segoe UI', sans-serif; font-size: 0.9em; background: #fff; max-width: 100%; }
  .sk-tbl th, .sk-tbl td { border: 1px solid #c9c9c9; padding: 4px 9px; text-align: center; }
  .sk-tbl th { background: #1c2a44; color: #fff; font-weight: 700; }
  .sk-tbl td.lbl { text-align: left; font-weight: 700; background: #fbf3d2; }
  .sk-tbl td.hl { background: #c9a633; color: #fff; font-weight: 700; }
  .sk-tbl td.hi { background: #efe3b0; }
  .sk-tbl tr.alt td { background: #f7f0d8; }
  .sk-tbl tr.alt td.hl { background: #c9a633; }
  .sk-wrap { overflow-x: auto; max-width: 100%; display: block; }
  .sk-wrap .sk-tbl { margin-left: 0; margin-right: 0; }
  @media (max-width: 640px) { .sk-wrap .sk-tbl { font-size: 0.62em; } .sk-wrap .sk-tbl th, .sk-wrap .sk-tbl td { padding: 2px 3px; } .sk-wrap .sk-tbl td br { display: none; } .sk-wrap .sk-tbl td span { display: block; } }
  .sk-tally { font-family: 'Courier New', monospace; letter-spacing: 1px; font-size: 1.05em; }
  @media (max-width: 640px) { .sk-tbl { font-size: 0.78em; } .sk-tbl th, .sk-tbl td { padding: 3px 5px; } }
</style>"""
INK, NAVY, GOLDC, PALEG, GREY, RED = "#1c2a44", "#002060", "#c9a633", "#efe3b0", "#8a94a6", "#d62828"
def svg(w, h, body, aria, maxw=None, cls=""):
    style = f' style="max-width:{maxw}px"' if maxw else ""
    return (f'<figure class="sk-fig {cls}"{style}><svg viewBox="0 0 {w} {h}" role="img" aria-label="{aria}">'
            '<defs><marker id="skah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0 0 L10 5 L0 10 z" fill="{INK}"/></marker></defs>' + body + '</svg></figure>')
def box(x, y, w, h, text, fill=PALEG, stroke=INK, fs=13, rx=8, bold=True, color=INK, lh=15, sw=1.6):
    rows = text.split("\n"); y0 = y + h / 2 + 4.5 - (len(rows) - 1) * lh / 2
    t = "".join(f'<tspan x="{x + w/2}" dy="{0 if i == 0 else lh}">{r}</tspan>' for i, r in enumerate(rows))
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
            f'<text x="{x + w/2}" y="{y0}" text-anchor="middle" font-size="{fs}" font-weight="{800 if bold else 500}" fill="{color}">{t}</text>')
def ellipse(cx, cy, rx, ry, text, fill=PALEG, stroke=INK, fs=12, lh=14, color=INK):
    rows = text.split("\n"); y0 = cy + 4.5 - (len(rows) - 1) * lh / 2
    t = "".join(f'<tspan x="{cx}" dy="{0 if i == 0 else lh}">{r}</tspan>' for i, r in enumerate(rows))
    return (f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{stroke}" stroke-width="1.6"/>'
            f'<text x="{cx}" y="{y0}" text-anchor="middle" font-size="{fs}" font-weight="800" fill="{color}">{t}</text>')
def circle(cx, cy, r, text, fill=PALEG, stroke=INK, fs=12, lh=14):
    return ellipse(cx, cy, r, r, text, fill, stroke, fs, lh)
def diamond(cx, cy, w, h, text, fill="#fbf1c7", fs=10, lh=12):
    rows = text.split("\n"); y0 = cy + 4 - (len(rows) - 1) * lh / 2
    t = "".join(f'<tspan x="{cx}" dy="{0 if i == 0 else lh}">{r}</tspan>' for i, r in enumerate(rows))
    return (f'<polygon points="{cx},{cy-h/2} {cx+w/2},{cy} {cx},{cy+h/2} {cx-w/2},{cy}" fill="{fill}" stroke="{INK}" stroke-width="1.5"/>'
            f'<text x="{cx}" y="{y0}" text-anchor="middle" font-size="{fs}" font-weight="700" fill="{INK}">{t}</text>')
def arrow(x1, y1, x2, y2, sw=1.8, color=INK, dashed=False, head=True):
    d = f' stroke-dasharray="6 4"' if dashed else ""
    m = ' marker-end="url(#skah)"' if head else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{sw}"{d}{m}/>'
def path(d, sw=1.8, color=INK, head=True, dashed=False, fill="none"):
    m = ' marker-end="url(#skah)"' if head else ""; dd = ' stroke-dasharray="6 4"' if dashed else ""
    return f'<path d="{d}" fill="{fill}" stroke="{color}" stroke-width="{sw}"{dd}{m} stroke-linejoin="round"/>'
def text(x, y, s, fs=13, anchor="middle", bold=True, color=INK, lh=15, italic=False):
    rows = s.split("\n")
    t = "".join(f'<tspan x="{x}" dy="{0 if i == 0 else lh}">{r}</tspan>' for i, r in enumerate(rows))
    st = ' font-style="italic"' if italic else ""
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{fs}" font-weight="{800 if bold else 500}" fill="{color}"{st}>{t}</text>'
def html(block, first=False):
    return {"html": (CSS if first else "") + block}

# The frameless look (Ian, 2026-10-26, after comparing against a colleague's
# inline-SVG file): no navy frame, no paper, no inner box, the caption a plain
# centred line, the buttons quiet pills. Applied from the map through
# apply_widgets.py's "style" key, so the engine itself is untouched.
LOOK = """
.sdg { border:0; background:transparent; padding:0; margin:14px auto 18px; }
.sdg h4 { font-size:.95rem; text-align:center; margin:0 0 2px; }
.sdg .sdg-lede { text-align:center; margin:0 0 8px; font-size:.88rem; }
.sdg figure { border:0; background:transparent; padding:0; }
.sdg .sdg-scen, .sdg .sdg-ctrl { justify-content:center; gap:6px; }
.sdg .sdg-scen { margin-bottom:6px; }
.sdg .sdg-scen button, .sdg .sdg-ctrl button { flex:0 1 auto; border:1px solid #c9d2e3; border-radius:999px; background:#fff; color:#1c2a44; padding:4px 12px; font-size:.82rem; font-weight:600; }
.sdg .sdg-scen button[aria-pressed="true"] { background:#1c2a44; border-color:#1c2a44; color:#fff; }
.sdg .sdg-ctrl { margin-top:4px; }
.sdg .sdg-step { font-size:.8rem; color:#555; }
.sdg .sdg-cap { background:transparent; border-left:0; padding:0; margin:4px auto 0; max-width:580px; font-size:.88rem; text-align:center; color:#444; }
.sdg .sdg-cap:not([aria-live]) { display:none; }
"""
# A static widget's caption is hidden by the look sheet (Ian, 2026-10-26: they
# take up too much space); it stays in the JSON, so the checker still reads it
# and a stepped widget keeps its live caption, which is what drives the steps.
def write_map(name, images, anchors=()):
    (MAPS / f"{name}.json").write_text(json.dumps({"images": images, "anchors": list(anchors), "style": LOOK}, ensure_ascii=False, indent=1))
    print(f"{name}: {len(images)} images, {len(anchors)} anchors")
