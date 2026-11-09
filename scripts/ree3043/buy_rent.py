"""REE3043 homeownership chapter: the buy-vs-rent figure as an sd-graph widget.

The source draws one symbolic line crossing zero at the break-even holding
period, with a callout and two braces. The prose states the base case's
values at 3, 4, 5 and 6 years and the break-even year of three sensitivity
cases, so the widget carries the base case on its stated numbers and the
three cases as scenario buttons with only their break-even year marked
(rule 3: nothing else about those lines is stated, so nothing else is drawn).

    python3 scripts/ree3043/buy_rent.py SOURCE.html OUT.html
"""
import json, re, sys, pathlib, subprocess
HERE = pathlib.Path(__file__).resolve().parent; REPO = HERE.parent.parent

# base case, $ thousands, from the prose: +9,504 at 3 years, +3,529 at 4, -2,303 at 5, -7,995 at 6
BASE = [(3, 9.504), (4, 3.529), (5, -2.303), (6, -7.995)]
m = (BASE[-1][1] - BASE[0][1]) / (BASE[-1][0] - BASE[0][0])          # about -5.83 a year
line = lambda x, x0, y0: round(y0 + m * (x - x0), 3)
BE = round(BASE[0][0] - BASE[0][1] / m, 2)                            # where the fitted line crosses zero
assert 4 < BE < 5, BE                                                  # "unless the home is held for more than 4 years"
for x, y in BASE: assert abs(line(x, 3, 9.504) - y) < 0.35, (x, y)    # the stated values lie on one line

def case(label, be, caption, labels=()):
    # the figure is symbolic: a gentle line through zero at the break-even year, spanning the plot
    # (the base case's stated values are written at their years; the heights are the line's, not a $ scale)
    s = 9 / max(be - 0.5, 10.3 - be)
    cur = [[0.5, round(-s * (0.5 - be), 3)], [10.3, round(-s * (10.3 - be), 3)]]
    return {"label": label,
            "curves": [{"id": "d", "label": "", "pts": cur}],
            "points": [{"q": be, "p": 0, "guides": False, "showP": False, "showQ": False, "color": "red"}] + [dict(l, p=round(-s * (l["q"] - be), 3)) for l in labels],
            "braces": [{"q1": be + 0.35, "q2": 10.2, "p": 0, "label": "Owning\nPreferred", "color": "red"},
                       {"q1": 0.6, "q2": be - 0.35, "p": 0, "label": "Renting\nPreferred", "below": "in", "color": "red"}],
            "caption": caption}
def val(x):
    # the four stated years are marked on the line; their values are in the caption, where they fit
    return {"q": x, "guides": False, "showP": False, "showQ": False}
base = case("Base case", BE,
            "Owning costs $9,504 more than renting over 3 years and $3,529 more over 4, but $2,303 less over 5 and $7,995 less over 6, so the line crosses zero just past 4 years.",
            labels=[val(3), val(4), val(5), val(6)])
cfg = {"title": "PV of Cost of Owning − PV of Cost of Renting",
       "lede": "Above zero, owning costs more than renting over the holding period; below zero, it costs less.",
       "axes": {"x": "\nHolding Period (Years)", "y": "$", "xmin": 0, "xmax": 10.5, "ymin": -12, "ymax": 12, "xticks": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], "cross": [0, 0], "bg": False},
       "scenarios": {
           "base": base,
           "rent": case("Rent of $1,600", 3, "With rent at $1,600 instead of $1,300, renting is dearer every year, so owning wins after only about 3 years."),
           "appr": case("5% appreciation", 2, "With the house appreciating 5% a year instead of 2%, the gain on sale offsets the transaction costs sooner, and owning wins after about 2 years."),
           "stdd": case("Standard deduction", 8, "Deducting mortgage interest and property taxes at a 0% rate, as a household taking the standard deduction does, stretches the break-even to about 8 years.")}}
sys.path.insert(0, str(REPO / "scripts/mar3203"))
try:
    from common import LOOK          # the frameless sheet the UCF sets use
except Exception:
    LOOK = ""
WIDGET = '<div class="sdg"><script type="application/json">%s</script></div>' % json.dumps(cfg, ensure_ascii=False).replace("</", "<\\/")

def main(src_path, out_path):
    src = pathlib.Path(src_path).read_text(encoding="utf-8")
    fig = re.search(r'<div class="content-image" style="max-width: 580px; margin: 18px auto;">\s*<svg.*?</svg>\s*</div>', src, re.S)
    assert fig, "the inline SVG figure was not found"
    out = src[:fig.start()] + "<!-- IMAGE POSITION: the buy-vs-rent graph, after the paragraph that introduces it -->\n" + WIDGET + src[fig.end():]
    house = re.search(r'[ \t]*<script src="https://smokinnotes\.s3\.us-east-1\.amazonaws\.com/studyguide/sn25-v2\.js"></script>\n', out)
    assert house, "house script line not found"
    out = out[:house.end()] + "<!--SDG-ENGINE-->\n" + out[house.end():]
    assert out.count("<!--SDG-ENGINE-->") == 1 and out.count('<div class="sdg"') == 1
    pathlib.Path(out_path).write_text(out, encoding="utf-8")
    subprocess.run([sys.executable, str(REPO / "scripts/embed_engine.py"), out_path], check=True)
    if LOOK:
        # the frameless look (Ian, 2026-10-26, "cleaner"): one <style> after the engine's own blocks, engine untouched
        out = pathlib.Path(out_path).read_text(encoding="utf-8")
        i = out.index("</script>", out.index("sd-graph.js v2.")) + len("</script>")
        out = out[:i] + "\n<style>\n/* widget look */\n" + LOOK.strip() + "\n</style>" + out[i:]
        pathlib.Path(out_path).write_text(out, encoding="utf-8")
    print("wrote", out_path)
if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
