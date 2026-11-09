"""MCB4503 Exam 4 Module 13 (Fall '26), 2026-11-09: sharper figures and an interactive phage-family pie.

Four soft figures point at Real-ESRGAN x4 versions (the "-hd" PNGs, uploaded beside the originals); the
phage-family pie becomes a hoverable chart. Seven families under 60 genomes fold into one "Other" slice,
whose legend row lists them: slivers under 1% cannot be hovered or read.

    python scripts/mcb4503/module13.py SRC.html OUT.html
"""
import sys, os, math, html

HD = ["01-mycovirus-genome-types", "02-giant-virus-structure", "04-bacteriophage-diversity", "09-archaeal-virus-morphologies2"]
PIE_IMG = "mcb4503-253-exam4-module13-05-phage-family-pie-chart.png"

# Counts as printed on the source chart. The five smallest slices carry no names on the chart; they are matched
# to the legend's last five entries in its own order, largest first, which is how the chart's legend is laid out.
MAIN = [("Siphoviridae", 4759, "#2a78d6"), ("Myoviridae", 1402, "#eb6834"), ("Podoviridae", 1012, "#1baf7a"),
        ("Unclassified", 479, "#eda100"), ("Microviridae", 441, "#e87ba4"), ("Herelleviridae", 199, "#008300")]
TAIL = [("Inoviridae", 57), ("Ackermannviridae", 51), ("Tectiviridae", 16), ("Leviviridae", 11),
        ("Cystoviridae", 5), ("Corticoviridae", 4), ("Plasmaviridae", 1)]
OTHER = ("Other families", sum(n for _, n in TAIL), "#8a8f98")
TOTAL = sum(n for _, n, _ in MAIN) + OTHER[1]
assert TOTAL == 8437, TOTAL

def pct(n): return f"{100 * n / TOTAL:.1f}%"
def fmt(n): return f"{n:,}"

def pie_widget():
    slices = MAIN + [OTHER]
    cx = cy = 150; r = 140; a = -90.0; paths = ""
    for i, (name, n, col) in enumerate(slices):
        sweep = 360 * n / TOTAL; a1 = a + sweep
        x0, y0 = cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))
        x1, y1 = cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1))
        d = f"M{cx} {cy} L{x0:.2f} {y0:.2f} A{r} {r} 0 {1 if sweep > 180 else 0} 1 {x1:.2f} {y1:.2f} Z"
        mid = math.radians(a + sweep / 2); lab = ""
        if n / TOTAL >= 0.10:   # a share is printed on its own slice only where it fits; the legend carries the rest
            k = 0.62
            lab = f'<text x="{cx + r*k*math.cos(mid):.1f}" y="{cy + r*k*math.sin(mid) + 5:.1f}" text-anchor="middle">{pct(n)}</text>'
        paths += (f'<g class="pp-s" data-i="{i}" style="--dx:{6*math.cos(mid):.2f}px;--dy:{6*math.sin(mid):.2f}px">'
                  f'<path d="{d}" fill="{col}"/>{lab}</g>')
        a = a1
    rows = ""
    for i, (name, n, col) in enumerate(slices):
        nm = name if i == len(slices) - 1 or name == "Unclassified" else f"<i>{name}</i>"
        sub = ""
        if i == len(slices) - 1:
            sub = '<span class="pp-tail">' + ", ".join(f"<i>{t}</i> {fmt(c)}" for t, c in TAIL) + "</span>"
        rows += (f'<div class="pp-row" data-i="{i}" tabindex="0" role="button" aria-label="{html.escape(name)}: {fmt(n)} genomes, {pct(n)}">'
                 f'<span class="pp-sw" style="background:{col}"></span><span class="pp-nm">{nm}{sub}</span>'
                 f'<span class="pp-n">{fmt(n)}</span><span class="pp-p">{pct(n)}</span></div>')
    detail = {i: (name, fmt(n), pct(n)) for i, (name, n, _) in enumerate(slices)}
    js_detail = "[" + ",".join(f'["{d[0]}","{d[1]}","{d[2]}"]' for d in detail.values()) + "]"
    return f'''<div class="phage-pie" id="phage-pie">
<style>
.phage-pie {{ --ink:#1c2a44; --muted:#5b6474; --rule:#dfe3ea; max-width:760px; margin:18px auto; padding:16px 18px 12px; background:#fff; border:1px solid var(--rule); border-radius:10px; box-sizing:border-box; font-family:"Red Hat Display", system-ui, sans-serif; color:var(--ink); clear:both; }}
.phage-pie * {{ box-sizing:border-box; }}
.phage-pie .pp-title {{ font-weight:800; font-size:1.02rem; margin:0 0 2px; text-align:center; }}
.phage-pie .pp-lede {{ font-size:.86rem; color:var(--muted); margin:0 0 10px; text-align:center; }}
.phage-pie .pp-body {{ display:flex; gap:22px; align-items:center; }}
.phage-pie svg {{ flex:0 0 46%; width:46%; height:auto; display:block; overflow:visible; }}
.phage-pie .pp-s path {{ stroke:#fff; stroke-width:2; transition:opacity .15s, transform .15s; cursor:pointer; }}
.phage-pie .pp-s text {{ font-size:14px; font-weight:800; fill:#fff; pointer-events:none; transition:opacity .15s; paint-order:stroke; stroke:rgba(0,0,0,.25); stroke-width:2px; }}
.phage-pie .pp-s.on path {{ transform:translate(var(--dx), var(--dy)); }}
.phage-pie.has-on .pp-s:not(.on) {{ opacity:.28; }}
.phage-pie .pp-side {{ flex:1 1 auto; min-width:0; }}
.phage-pie .pp-read {{ min-height:3.1em; margin:0 0 8px; padding:6px 10px; border-left:4px solid var(--rule); font-size:.92rem; line-height:1.35; }}
.phage-pie .pp-read b {{ font-weight:800; }}
.phage-pie .pp-row {{ display:grid; grid-template-columns:14px 1fr auto 3.6em; gap:8px; align-items:start; padding:4px 6px; border-radius:6px; font-size:.9rem; line-height:1.3; cursor:pointer; outline:none; }}
.phage-pie .pp-row:hover, .phage-pie .pp-row.on, .phage-pie .pp-row:focus-visible {{ background:#f1f4f9; }}
.phage-pie .pp-row:focus-visible {{ box-shadow:0 0 0 2px #2a78d6 inset; }}
.phage-pie .pp-sw {{ width:12px; height:12px; border-radius:3px; margin-top:3px; }}
.phage-pie .pp-n, .phage-pie .pp-p {{ text-align:right; font-variant-numeric:tabular-nums; }}
.phage-pie .pp-p {{ color:var(--muted); }}
.phage-pie .pp-tail {{ display:block; font-size:.78rem; color:var(--muted); margin-top:2px; }}
.phage-pie .pp-src {{ font-size:.78rem; color:var(--muted); text-align:right; margin:10px 0 0; }}
@media (max-width:600px) {{ .phage-pie .pp-body {{ flex-direction:column; gap:10px; }} .phage-pie svg {{ width:78%; flex-basis:auto; }} .phage-pie .pp-side {{ width:100%; }} .phage-pie .pp-row {{ min-height:36px; }} }}
@media (prefers-reduced-motion: reduce) {{ .phage-pie .pp-s path, .phage-pie .pp-s text {{ transition:none; }} }}
</style>
<p class="pp-title">Sequenced Phage Genomes by Family</p>
<p class="pp-lede">Hover over or tap a slice or a family name to see its count.</p>
<div class="pp-body">
<svg viewBox="-10 -10 320 320" role="img" aria-label="Pie chart of {fmt(TOTAL)} sequenced phage genomes by family: Siphoviridae {fmt(4759)}, Myoviridae {fmt(1402)}, Podoviridae {fmt(1012)}, unclassified {fmt(479)}, Microviridae {fmt(441)}, Herelleviridae {fmt(199)}, and seven other families {fmt(OTHER[1])}">{paths}</svg>
<div class="pp-side">
<p class="pp-read" aria-live="polite"></p>
{rows}
</div>
</div>
<p class="pp-src">From <i>Phage Diversity, Genomics, &amp; Phylogeny</i>, Nature (3 Feb 2020)</p>
<script>
(function () {{
  var root = document.getElementById('phage-pie'), D = {js_detail}, TOTAL = "{fmt(TOTAL)}";
  var read = root.querySelector('.pp-read'), pinned = null;
  function rest() {{ read.innerHTML = '<b>' + TOTAL + '</b> sequenced phage genomes in all. <i>Siphoviridae</i> alone make up more than half.'; read.style.borderLeftColor = ''; }}
  function show(i) {{
    root.classList.toggle('has-on', i !== null);
    root.querySelectorAll('[data-i]').forEach(function (el) {{ el.classList.toggle('on', i !== null && +el.dataset.i === i); }});
    if (i === null) {{ rest(); return; }}
    var d = D[i], sw = root.querySelector('.pp-row[data-i="' + i + '"] .pp-sw');
    var name = (d[0] === 'Unclassified' || d[0] === 'Other families') ? d[0] : '<i>' + d[0] + '</i>';
    read.innerHTML = '<b>' + name + '</b>: ' + d[1] + ' genomes, ' + d[2] + ' of the total' + (d[0] === 'Other families' ? ' (seven small families, listed below).' : '.');
    read.style.borderLeftColor = sw.style.background;
  }}
  root.querySelectorAll('[data-i]').forEach(function (el) {{
    var i = +el.dataset.i;
    el.addEventListener('mouseenter', function () {{ if (pinned === null) show(i); }});
    el.addEventListener('mouseleave', function () {{ if (pinned === null) show(null); }});
    el.addEventListener('click', function () {{ pinned = (pinned === i) ? null : i; show(pinned); }});
    el.addEventListener('keydown', function (e) {{ if (e.key === 'Enter' || e.key === ' ') {{ e.preventDefault(); pinned = (pinned === i) ? null : i; show(pinned); }} }});
    el.addEventListener('focus', function () {{ if (pinned === null) show(i); }});
    el.addEventListener('blur', function () {{ if (pinned === null) show(null); }});
  }});
  rest();
}})();
</script>
</div>'''

def build(src, out):
    t = open(src, encoding="utf-8").read()
    # the current house head: font links and the v6 stylesheet in place of v5, and the live study-guide script,
    # which builds the table of contents, in place of content/sn25-v5.js
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "mar3023"))
    from pricing import modern_head
    t = modern_head(t)
    assert "sn25-v5" not in t, "old head left"
    assert t.count("<u>not</u>") == 1; t = t.replace("<u>not</u>", "<b>not</b>")   # the house format never underlines
    for n in HD:
        old = f"mcb4503-253-exam4-module13-{n}.png"; assert t.count(old) == 1, old
        t = t.replace(old, f"mcb4503-253-exam4-module13-{n}-hd.png")
    i = t.index(PIE_IMG); s = t.rindex("<img", 0, i); e = t.index("/>", i) + 2
    t = t[:s] + pie_widget() + t[e:]
    assert PIE_IMG not in t and t.count('id="phage-pie"') == 1
    open(out, "w", encoding="utf-8").write(t); print("wrote", out)

if __name__ == "__main__":
    build(*sys.argv[1:3])
