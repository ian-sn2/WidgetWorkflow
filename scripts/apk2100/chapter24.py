#!/usr/bin/env python3
"""APK2100 Exam 4, Chapter 24 (the urinary system): the Full reformatted, and its Balanced and Concise.

    python scripts/apk2100/chapter24.py SOURCE_FULL.html OUTDIR

* Full: formatting only, the wording untouched (asserted word for word): the live house script and
  head order, a doctype, the pipeline's AUDIT notes out, and lists made valid -- paragraphs and an
  image that sat directly inside a <ul>, outside any <li>, now stand as page text.
* Balanced: the Full with checked cuts (each must match exactly once), every image, number and date kept.
* Concise: bullets and tables on the Full's own h1/h2 headings, then Glossary and Key Takeaways.

Ian, 2026-11-20.
"""
import re
import sys
import pathlib

LIVE_JS = "https://smokinnotes.s3.us-east-1.amazonaws.com/studyguide/sn25-v2.js"
OLD_JS = "https://smokinnotes.s3.us-east-1.amazonaws.com/content/sn25-v5.js"
CSS = '<link rel="stylesheet" href="https://smokinnotes.s3.us-east-1.amazonaws.com/content/sn25-v6.css">'
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"> <link rel="preconnect" '
         'href="https://fonts.gstatic.com" crossorigin> <link href="https://fonts.googleapis.com/css2?'
         'family=Red+Hat+Display:wght@300;400;500;600;700;800;900&amp;display=swap" rel="stylesheet">')


def rep(t, a, b):
    n = t.count(a)
    assert n == 1, (n, a[:100])
    return t.replace(a, b)


def words(html):
    body = html[html.index("<body"):]
    body = re.sub(r"<(script|style)\b.*?</\1>|<!--.*?-->", " ", body, flags=re.S)
    return re.sub(r"<[^>]+>", " ", body).split()


def headings(html, levels="12"):
    return [(m.group(1), re.sub(r"<[^>]+>", "", m.group(2)).strip())
            for m in re.finditer(r"<h([%s])[^>]*>(.*?)</h\1>" % levels, html, re.S)]


# ------------------------------------------------------------------ Full --

def full(src):
    t = src
    if not t.lstrip().lower().startswith("<!doctype"):
        t = "<!DOCTYPE html>\n" + t
    t = rep(t, OLD_JS, LIVE_JS)
    t = rep(t, FONTS + "\n" + CSS, CSS + "\n" + FONTS)
    t = re.sub(r"<!-- [A-Z ]+AUDIT:.*?-->\n?", "", t)
    t = re.sub(r"<body>\n\n\n\n", "<body>\n\n", t)
    t = rep(t, "<i>urogenital diaphragm</i>", "<em>urogenital diaphragm</em>")
    # The renal-corpuscle bullet: its Bowman's-capsule paragraphs and image sat directly in the <ul>,
    # outside any <li>. The bullet ends after its own text; they follow as page text, and the tubular
    # section is its own one-item list as before.
    t = rep(t, """similar to the choroid plexus in the brain.</li>


<p>When you look at the Bowman's capsule""", """similar to the choroid plexus in the brain.</li>
</ul>

<p>When you look at the Bowman's capsule""")
    t = rep(t, """whatever is pulled back across the tubule wall into the peritubular capillaries is returned to the body.</p>
</ul>
<ul>
  <li><strong>Tubular section</strong>""", """whatever is pulled back across the tubule wall into the peritubular capillaries is returned to the body.</p>

<ul>
  <li><strong>Tubular section</strong>""")
    # one stray indented paragraph
    t = rep(t, "\n  <p>Students often confuse the terms renal pelvis", "\n\n<p>Students often confuse the terms renal pelvis")
    assert words(t) == words(src), "the Full's wording changed"
    return t


# -------------------------------------------------------------- Balanced --

def balanced(f):
    t = f
    cuts = [
        # duplicated or side remarks; every figure, number and date stays
        (" In cadaveric views, this same pathway is visible as the ureter travels across the surface of the psoas and approaches the bifurcation of the common iliac artery into its internal and external branches. In many dissections, the urinary bladder is cut open to show its interior, so the urethra may not be visible.", ""),
        (" For example, the brain is protected by a bony case called a skull and the lungs and heart are protected by the ribcage, sternum, vertebrae, and thick musculature.", ""),
        (" In rougher contact sports, such as football, a strong blow can still bruise the kidneys or cause significant pain, but the most severe injuries—such as a torn vascular attachment—are typically associated with major trauma like a car accident or a fall onto a hard or sharp surface. For this reason, kidney punches are illegal moves in boxing.", " For this reason, kidney punches are illegal moves in boxing."),
        ("""<p>Dr. Ahlgren noted that she and her husband both train in martial arts and often watch UFC fights, and they cringe whenever a strike comes close to the kidney region because they know how dangerous kidney trauma can be. Even a glancing blow in this area can cause significant pain, and a harder strike can lead to more serious injury.</p>

""", ""),
        (" (You can use the 3D models in lab to get a better idea of what they look like.)", ""),
        ("<p>Students often confuse the terms renal pelvis, renal sinus, and renal hilum, so be sure to understand the difference between them. The renal sinus", "<p>The renal sinus"),
        (" Glomerular capillaries are fenestrated because clefts alone would not let material out quickly enough.", ""),
        (" Note that the blood is still oxygenated when it leaves the glomerulus; the glomerulus is simply where the blood gets filtered.", ""),
        (" (The vasa recta are still a type of peritubular capillaries, they are just given a more specific name because they have a structural difference when compared to normal peritubular capillaries.)", ""),
        (" This comparison is meant to highlight the unusual \"capillary-bed-to-capillary-bed\" organization in the kidney.", ""),
        (" However, they do have a lot of receptors that receive signals that regulate the movement of substances.", ""),
        (" Diagrams often stretch the nephron out from left to right, but that is not anatomically accurate. In reality the tubule folds back so that the distal tubule passes directly between the afferent and efferent arterioles of its own renal corpuscle.", ""),
        (" The blood that is not filtered exits the renal corpuscle through the efferent arteriole.", ""),
        (" This relationship can be seen when tracing the ureters from the level of L2 down toward the pelvis.", ""),
        (" (At first, you might find this unnecessary because the kidneys are placed high so it makes sense for the urine to just drain down the ureters. The smooth muscle is necessary because of where the ureters drain into the urinary bladder.)", ""),
        ("<p>Passing a kidney stone can be extremely painful. Some stones can also be surprisingly large, which may require medical procedures to break them into smaller pieces before they can pass through the ureter or urethra. Stones are made of different substances, so they vary in appearance. A stone hurts", "<p>A stone hurts"),
        (" Stones can be broken into pieces to be passed, or retrieved directly.", ""),
        (" This example highlights how kidney stones can pose serious risks beyond pain by increasing the likelihood of infection.", ""),
        (" This creates a space where the bladder lies below the peritoneal lining even though it is not considered retroperitoneal.", ""),
        (" Because of this functional relationship, exercises that target both the pelvic floor (such as Kegels) and surrounding musculature (such as squats) can help improve stability and support.", ""),
        (" This condition illustrates how structural changes in the kidney can significantly disrupt its ability to regulate fluid balance and remove waste.", ""),
    ]
    for a, b in cuts:
        t = rep(t, a, b)
    assert t.count("<img") == f.count("<img")
    assert headings(t) == headings(f)
    assert re.findall(r'class="date">([^<]*)', t) == re.findall(r'class="date">([^<]*)', f)
    share = len(words(t)) / len(words(f))
    assert 0.75 <= share <= 0.95, share
    return t


# --------------------------------------------------------------- Concise --

CONCISE_BODY = """
<h1>Introduction to the Urinary System</h1>

<ul>
  <li><b>Urinary system:</b> eliminates wastes and regulates the chemical constancy and volume of the blood (and so of all body fluids); balances water, acids, bases and electrolytes; helps regulate blood pressure.</li>
  <li><b>Organs:</b> two kidneys → two ureters → urinary bladder → urethra.</li>
  <li><b>Kidneys:</b> superior lumbar region of the posterior abdominal wall, deep to ribs 11 and 12 (floating ribs, so only partial bony protection). The right kidney sits lower because the liver pushes it down. The adrenal glands sit on top but are not urinary organs.</li>
  <li>The water in urine comes from blood plasma, so making urine is also how the kidneys regulate solute concentrations and blood volume.</li>
</ul>

<h2>How Well Protected Is the Kidney?</h2>

<ul>
  <li>The kidneys are <b>retroperitoneal</b>: no peritoneal cushioning or mesenteries, so they lie directly against the posterior abdominal wall and are easier to injure.</li>
  <li>You can live with one kidney but not without both.</li>
  <li>Together they receive about <b>20% of cardiac output</b> at rest, so a deep laceration or torn vascular attachment bleeds fast.</li>
  <li>Trauma ranges from a bruise (a direct blow) to a laceration (a much stronger impact) to a torn vascular attachment (major trauma such as a car accident or high fall). Kidney punches are illegal in boxing.</li>
</ul>

<table>
  <thead><tr><th>Protective layer</th><th>What it does</th></tr></thead>
  <tbody>
    <tr><td><b>Renal (fibrous) capsule</b></td><td>Thick capsule wrapped around each kidney.</td></tr>
    <tr><td><b>Perirenal fat</b></td><td>Fat layer cushioning the kidney.</td></tr>
    <tr><td><b>Renal fascia</b></td><td>Anterior and posterior bands that hold the kidney in place.</td></tr>
  </tbody>
</table>

<h2>Gross Anatomy of the Kidney</h2>

<ul>
  <li><b>Renal cortex</b> (light outer region) and <b>renal medulla</b> (striped inner region); <b>renal columns</b> anchor the cortex into the medulla.</li>
  <li>The medulla = <b>renal pyramids</b> + renal columns. The tip of each pyramid is a <b>renal papilla</b>.</li>
  <li>Drainage: papilla → <b>minor calyx</b> → <b>major calyx</b> → <b>renal pelvis</b> (top of the funnel) → ureter (the narrow spout).</li>
</ul>

<table>
  <thead><tr><th>Often confused</th><th>What it is</th></tr></thead>
  <tbody>
    <tr><td><b>Renal sinus</b></td><td>Internal cavity holding fat, vessels, nerves, the major calyces and the renal pelvis.</td></tr>
    <tr><td><b>Renal pelvis</b></td><td>Funnel-shaped collecting region receiving urine from the major calyces.</td></tr>
    <tr><td><b>Renal hilum (hilus)</b></td><td>External indentation where vessels, nerves and the ureter enter or leave.</td></tr>
  </tbody>
</table>

<div class="exam-tip">
  <h4>EXAM TIP: Structural Terminology</h4>
  <p>Renal pelvis, renal sinus and renal hilum are three different structures. Know the difference.</p>
</div>

<h2>Microscopic Anatomy of the Kidney</h2>

<p>The <b>nephron</b> is the kidney's smallest functional unit: a renal corpuscle plus a tubular section.</p>

<table>
  <thead><tr><th>Part</th><th>Key points</th></tr></thead>
  <tbody>
    <tr><td><b>Renal corpuscle</b> (cortex only)</td><td><b>Glomerulus</b> (tuft of fenestrated capillaries) inside the <b>glomerular (Bowman's) capsule</b>. Parietal layer = simple squamous epithelium; visceral layer = <b>podocytes</b>, whose interlocking processes act like a strainer.</td></tr>
    <tr><td><b>Filtration membrane</b></td><td>Every layer filtrate crosses: capillary wall (fenestrations and clefts) → slits between podocyte processes → capsular space. Similar in plan to the respiratory membrane.</td></tr>
    <tr><td><b>Tubular section</b></td><td>Proximal convoluted tubule → loop of Henle → distal convoluted tubule → collecting duct.</td></tr>
  </tbody>
</table>

<ul>
  <li>The capsular space opens into the proximal convoluted tubule, so filtrate is technically outside the body: what stays in the tubule becomes urine; what is reabsorbed into the peritubular capillaries returns to the body.</li>
</ul>

<p class="date">Friday, 11/20/26</p>

<h1>Introduction to the Urinary System (Continued)</h1>

<h3>Two Kinds of Nephrons:</h3>
<table>
  <thead><tr><th>Type</th><th>Share</th><th>Loop of Henle</th></tr></thead>
  <tbody>
    <tr><td><b>Cortical</b></td><td>About 90–95%</td><td>Ends near the cortex–medulla junction; corpuscle high in the cortex.</td></tr>
    <tr><td><b>Juxtamedullary</b></td><td>The rest</td><td>Dips deep into the medulla; corpuscle low in the cortex. More important for producing urine.</td></tr>
  </tbody>
</table>

<h3>Blood Flow Through the Nephron:</h3>
<ul>
  <li><b>Afferent arteriole</b> → glomerulus → <b>efferent arteriole</b>. Blood leaving is still oxygenated (filtration, not gas exchange), so it leaves through an arteriole, which has smooth muscle to regulate flow. The afferent arteriole is usually slightly wider.</li>
  <li>Efferent arteriole → <b>peritubular capillaries</b> (around the convoluted tubules) or the <b>vasa recta</b> (long, straight, ordered capillaries along the loops of Henle of juxtamedullary nephrons) → veins.</li>
  <li>Two capillary beds in series (glomerular, then peritubular) form a <b>portal system</b>, like the hepatic portal system.</li>
</ul>

<div class="exam-tip">
  <h4>EXAM TIP: Vasa Recta Association</h4>
  <p>The vasa recta are associated only with the loops of Henle of juxtamedullary nephrons.</p>
</div>

<h3>Path of Filtrate:</h3>
<p>Proximal convoluted tubule → descending limb of the loop of Henle → ascending limb → distal convoluted tubule → collecting duct → <b>papillary duct</b> → minor calyx (now final urine) → major calyx → renal pelvis → ureter → bladder → urethra.</p>

<table>
  <thead><tr><th>Tubule</th><th>Cells</th><th>Reabsorption</th></tr></thead>
  <tbody>
    <tr><td><b>Proximal convoluted tubule</b></td><td>Microvilli and many mitochondria</td><td>Largely unregulated</td></tr>
    <tr><td><b>Distal convoluted tubule</b></td><td>Few or no microvilli, fewer mitochondria, many receptors</td><td>Highly regulated by signals from the blood</td></tr>
  </tbody>
</table>

<h2>The Juxtaglomerular Apparatus</h2>

<ul>
  <li>The <b>juxtaglomerular apparatus</b> (juxtaglomerular complex) is where the distal convoluted tubule loops back between the afferent and efferent arterioles of its own corpuscle. It regulates blood flow into the glomerulus, and so urine output, blood volume and blood pressure.</li>
</ul>

<table>
  <thead><tr><th>Cell</th><th>Where</th><th>Job</th></tr></thead>
  <tbody>
    <tr><td><b>Macula densa cells</b></td><td>Wall of the distal tubule (modified epithelium)</td><td>Sense NaCl in the filtrate. High NaCl (much filtration) → signal that constricts the afferent arteriole → less filtered.</td></tr>
    <tr><td><b>Granular cells</b></td><td>Mostly the afferent arteriole (modified smooth muscle)</td><td>Secrete hormones that dilate or constrict the afferent arteriole.</td></tr>
  </tbody>
</table>

<p>More filtration → more urine → lower blood volume → lower blood pressure.</p>

<h2>Basic Processes of Urine Production</h2>

<table>
  <thead><tr><th>Step</th><th>Where</th><th>What happens</th></tr></thead>
  <tbody>
    <tr><td><b>1. Filtration</b></td><td>Renal corpuscle</td><td>Blood pressure pushes plasma into Bowman's capsule. Relatively non-specific; no blood cells or proteins. About 20% of what enters is filtered; about 80% leaves through the efferent arteriole.</td></tr>
    <tr><td><b>2. Reabsorption</b></td><td>Tubule → peritubular capillaries</td><td>Valuable materials (such as water) returned to the blood selectively.</td></tr>
    <tr><td><b>3. Secretion</b></td><td>Peritubular capillaries → tubule</td><td>Substances that were not filtered are moved into the tubule selectively.</td></tr>
  </tbody>
</table>

<h2>The Ureters</h2>

<ul>
  <li>Run from the renal pelvis (about L2) to the posterior-inferior wall of the bladder, passing over the sacroiliac joint region. About 10 inches long.</li>
  <li>Stretch triggers <b>peristalsis</b> in their circular smooth muscle, which pumps urine into the bottom of the bladder against the pressure of the urine already there.</li>
  <li>They enter the bladder at an angle; as the bladder fills, pressure compresses the openings and prevents reflux toward the kidneys.</li>
  <li>Textbook pictures often show the ureters entering the top of the bladder; they actually enter the bottom, posterior part.</li>
  <li><b>Kidney stones</b> form from salts and other materials. A stone hurts in the ureter (the wall contracts on it), usually not in the bladder, and again in the urethra (it scrapes the narrow tube). Large stones are removed or broken up. Stones lodged in the renal pelvis can become sites of repeated infection and kidney failure.</li>
</ul>

<h2>The Urinary Bladder</h2>

<ul>
  <li>Hollow organ of smooth muscle that stores urine; its outer smooth muscle is the <b>detrusor muscle</b> (not voluntary).</li>
  <li>Lies behind the pubic symphysis, below the peritoneum (which drapes over it). The female bladder is somewhat smaller, with the uterus on top of it. A very full bladder can be palpated above the pubic symphysis.</li>
  <li>Internal features: <b>rugae</b> (folds that flatten as it fills) and the <b>trigone</b> (triangle between the two ureteral openings and the internal urethral orifice; a common site of infection).</li>
  <li>On lab models, sex the model first: on a male model, the hollow muscular organ behind the pubic symphysis is the bladder, not a uterus.</li>
</ul>

<h2>The Urethra</h2>

<table>
  <thead><tr><th>Sphincter</th><th>Muscle</th><th>Control</th></tr></thead>
  <tbody>
    <tr><td><b>Internal urethral sphincter</b></td><td>Smooth muscle at the base of the bladder</td><td>Autonomic (relaxes with parasympathetic activity)</td></tr>
    <tr><td><b>External urethral sphincter</b></td><td>Skeletal muscle in the urogenital diaphragm (part of the pelvic floor)</td><td>Voluntary: "holding it"</td></tr>
  </tbody>
</table>

<table>
  <thead><tr><th>Sex</th><th>Urethra</th></tr></thead>
  <tbody>
    <tr><td><b>Males</b></td><td>Long, three regions: <b>prostatic</b> (intermediate), <b>membranous</b> (very short, through the urogenital diaphragm) and <b>spongy</b> (very long, through the corpus spongiosum to the external urethral orifice). The two sphincters are separated by the prostatic urethra.</td></tr>
    <tr><td><b>Females</b></td><td>Much shorter, no regions; sphincters close together. UTIs are more common because the urethra is short and near the anus.</td></tr>
  </tbody>
</table>

<ul>
  <li>The pelvic floor and diaphragm work together to raise abdominopelvic pressure and stabilize the core. Pelvic floor openings, posterior to anterior: anus, vaginal orifice (females), urethral orifice. A weak pelvic floor can cause leakage when running, coughing, laughing or sneezing.</li>
</ul>

<h2>The Process of Micturition</h2>

<ul>
  <li><b>Micturition</b> starts with stretch: sensory neurons in the stretched detrusor signal the <b>pontine micturition center</b> in the pons, which weighs it against higher brain centers.</li>
  <li>Urination needs three things: open the external sphincter, open the internal sphincter, and squeeze the bladder.</li>
</ul>

<table>
  <thead><tr><th>Neurons</th><th>At rest</th><th>During urination</th></tr></thead>
  <tbody>
    <tr><td><b>Sympathetic</b></td><td>Keep detrusor relaxed, internal sphincter closed</td><td>Inhibited</td></tr>
    <tr><td><b>Parasympathetic</b></td><td>Inactive</td><td>Contract detrusor, relax internal sphincter ("rest and digest")</td></tr>
    <tr><td><b>Somatic</b> (to external sphincter)</td><td>Keep it closed</td><td>Inhibited in the spinal cord (stop releasing acetylcholine)</td></tr>
  </tbody>
</table>

<h2>Clinical Example: Polycystic Kidney Disease</h2>

<ul>
  <li><b>Polycystic kidney disease</b>: a genetic condition in which fluid-filled cysts greatly enlarge the kidneys and impair their function.</li>
  <li>In the case described, each diseased kidney weighed roughly 11 pounds; the donor kidney went in first, and the diseased kidneys were removed about six months later.</li>
  <li>Severe cases may need dialysis and eventually a transplant.</li>
</ul>

<h2>Glossary</h2>

<table>
  <thead><tr><th>Term</th><th>Definition</th></tr></thead>
  <tbody>
    <tr><td><b>Retroperitoneal</b></td><td>Lying behind the peritoneal cavity, against the posterior abdominal wall.</td></tr>
    <tr><td><b>Renal cortex / medulla</b></td><td>The light outer region and the striped inner region of the kidney.</td></tr>
    <tr><td><b>Renal pyramid / papilla</b></td><td>A cone of medulla, and its tip, which drains into a minor calyx.</td></tr>
    <tr><td><b>Renal pelvis</b></td><td>Funnel collecting urine from the major calyces and narrowing into the ureter.</td></tr>
    <tr><td><b>Renal sinus</b></td><td>Internal cavity holding fat, vessels, nerves and the renal pelvis.</td></tr>
    <tr><td><b>Renal hilum</b></td><td>External indentation where vessels, nerves and the ureter enter or leave.</td></tr>
    <tr><td><b>Nephron</b></td><td>The kidney's smallest functional unit: renal corpuscle plus tubular section.</td></tr>
    <tr><td><b>Glomerulus</b></td><td>Tuft of fenestrated capillaries in the renal corpuscle where blood is filtered.</td></tr>
    <tr><td><b>Podocytes</b></td><td>Visceral-layer cells of Bowman's capsule whose interlocking processes strain the filtrate.</td></tr>
    <tr><td><b>Vasa recta</b></td><td>Straight peritubular capillaries along the loops of Henle of juxtamedullary nephrons.</td></tr>
    <tr><td><b>Portal system</b></td><td>Two capillary beds in series.</td></tr>
    <tr><td><b>Juxtaglomerular apparatus</b></td><td>Contact point of the distal tubule and afferent arteriole that regulates glomerular blood flow.</td></tr>
    <tr><td><b>Macula densa cells</b></td><td>Distal-tubule cells that sense NaCl in the filtrate.</td></tr>
    <tr><td><b>Granular cells</b></td><td>Afferent-arteriole cells that secrete hormones that dilate or constrict it.</td></tr>
    <tr><td><b>Detrusor muscle</b></td><td>The smooth muscle of the bladder wall.</td></tr>
    <tr><td><b>Trigone</b></td><td>Triangle between the ureteral openings and the internal urethral orifice.</td></tr>
    <tr><td><b>Micturition</b></td><td>Urination.</td></tr>
    <tr><td><b>Pontine micturition center</b></td><td>Center in the pons that coordinates urination.</td></tr>
  </tbody>
</table>

<h2>Key Takeaways</h2>

<ul>
  <li>The kidneys regulate blood volume, blood pressure and the chemical constancy of body fluids, not just urine.</li>
  <li>The kidneys are retroperitoneal and poorly protected, and receive about 20% of resting cardiac output.</li>
  <li>Renal sinus, renal pelvis and renal hilum are three distinct structures.</li>
  <li>The renal corpuscle stays in the cortex; only the loop of Henle reaches into the medulla.</li>
  <li>About 90–95% of nephrons are cortical, but juxtamedullary nephrons matter more for urine.</li>
  <li>The vasa recta go only with the loops of Henle of juxtamedullary nephrons.</li>
  <li>Glomerular plus peritubular capillaries form a portal system.</li>
  <li>Urine is made by filtration, reabsorption and secretion, in that order; only about 20% of incoming blood is filtered.</li>
  <li>Macula densa cells sense NaCl; granular cells change afferent arteriole diameter.</li>
  <li>The ureters enter the bottom, posterior wall of the bladder, and peristalsis pushes urine in.</li>
  <li>The internal urethral sphincter is smooth muscle (autonomic); the external is skeletal muscle (voluntary).</li>
  <li>Urination: sympathetic and somatic output inhibited, parasympathetic output contracts the detrusor.</li>
</ul>
"""


def concise(f):
    head = f[:f.index("<body>") + len("<body>")]
    head = rep(head, "</head>", """<style>
/* phones: a wide table scrolls in its own box instead of pushing the page sideways */
@media (max-width: 600px) { table { display: block; overflow-x: auto !important; max-width: 100%; } }
</style>
</head>""")
    t = head + "\n" + CONCISE_BODY + "\n</body>\n</html>\n"
    assert headings(t) == headings(f) + [("2", "Glossary"), ("2", "Key Takeaways")], headings(t)
    for h3 in re.findall(r"<h3>(.*?)</h3>", t):
        assert h3.endswith(":"), h3
    assert "Ahlgren" not in t and "<img" not in t
    for n in ("ribs 11 and 12", "20% of cardiac output", "90–95%", "About 20%", "about 80%", "L2", "10 inches", "11 pounds", "six months"):
        assert n in t, n
    return t


def main(src, out):
    out = pathlib.Path(out)
    out.mkdir(parents=True, exist_ok=True)
    f = full(open(src, encoding="utf-8").read())
    b = balanced(f)
    c = concise(f)
    base = "APK2100-263-Exam4-Chapter24-"
    for name, html in (("Full", f), ("Balanced", b), ("Concise", c)):
        (out / f"{base}{name}.html").write_text(html, encoding="utf-8")
        print(f"{base}{name}.html: {len(words(html))} words")


if __name__ == "__main__":
    main(*sys.argv[1:3])
