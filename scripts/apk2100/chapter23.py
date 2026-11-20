#!/usr/bin/env python3
"""APK2100 Exam 4, Chapter 23 (the digestive system): the Full reformatted, and its Balanced and Concise.

    python scripts/apk2100/chapter23.py SOURCE_FULL.html OUTDIR

* Full: formatting only, the wording untouched (asserted word for word): a doctype, the live house
  script, the stylesheet ahead of the fonts, the pipeline's AUDIT notes out, and the two class dates
  that sat inside the muscularis-externa bullet moved out to the page beside the paragraphs they
  start (the wall-layers list then resumes at the serosa).
* Balanced: about half the Full, the length and approach of the API Balanced (Ian, 2026-11-20):
  each paragraph cut to what the exam needs, analogies and asides dropped; every heading, image, list,
  box, number and date kept.
* Concise: in the layout of the API Concise editions Ian sends (Ian, 2026-11-20): definition tables,
  short fragment bullets, a Glossary table and Key Takeaways, about a fifth of the Full; the Full's
  own h1/h2 headings, and one figure, the wall cross-section its exam tip asks students to know.

Ian, 2026-11-20.
"""
import re
import sys
import pathlib

LIVE_JS = "https://smokinnotes.s3.us-east-1.amazonaws.com/studyguide/sn25-v2.js"
OLD_JS = "https://smokinnotes.s3.us-east-1.amazonaws.com/content/sn25-v5.js"


def rep(t, a, b):
    n = t.count(a)
    assert n == 1, (n, a[:100])
    return t.replace(a, b)


def para(t, start, new):
    """Replace one paragraph or list item, found by its opening words, through its closing tag."""
    i = t.find(start)
    assert i >= 0 and t.count(start) == 1, ("opening not found once", start[:70])
    j = min(k for k in (t.find("</p>", i), t.find("</li>", i)) if k > 0)
    return t[:i] + new + t[j:]


def words(html):
    body = html[html.index("<body"):]
    body = re.sub(r"<(script|style)\b.*?</\1>|<!--.*?-->", " ", body, flags=re.S)
    return re.sub(r"<[^>]+>", " ", body).split()


def headings(html, levels="12"):
    return [(m.group(1), re.sub(r"<[^>]+>", "", m.group(2)).strip())
            for m in re.finditer(r"<h([%s])[^>]*>(.*?)</h\1>" % levels, html, re.S)]


def dates(html):
    return re.findall(r'<p class="date">(.*?)</p>', html)


# ------------------------------------------------------------------ Full --

def full(src):
    t = src
    if not t.lstrip().lower().startswith("<!doctype"):
        t = "<!DOCTYPE html>\n" + t
    t = rep(t, OLD_JS, LIVE_JS)
    css = '    <link rel="stylesheet" href="https://smokinnotes.s3.us-east-1.amazonaws.com/content/sn25-v6.css">\n'
    t = rep(t, css, "")
    t = rep(t, '    <link rel="preconnect" href="https://fonts.googleapis.com">\n',
            css + '    <link rel="preconnect" href="https://fonts.googleapis.com">\n')
    t = re.sub(r"<!-- [A-Z ]+AUDIT:.*?-->\n?", "", t)
    t = re.sub(r"\n{3,}", "\n\n", t)
    # The 11/11 and 11/13 dates sat inside the muscularis-externa bullet; they go out to the page with
    # the two paragraphs they start, and the list of layers resumes at the serosa.
    t = rep(t, """carried out by the stomach.</p>

        <p class="date">Wednesday, 11/11/26</p>

        <p><em>There was no class on Wednesday, November 11th, due to the Veterans Day holiday.</em></p>

        <p class="date">Friday, 11/13/26</p>

        <p>Dr. Ahlgren noted that the mucosal epithelium""", """carried out by the stomach.</p>
    </li>
</ul>

<p class="date">Wednesday, 11/11/26</p>

<p><em>There was no class on Wednesday, November 11th, due to the Veterans Day holiday.</em></p>

<p class="date">Friday, 11/13/26</p>

<p>Dr. Ahlgren noted that the mucosal epithelium""")
    t = rep(t, """rather than by surface movement.</p>
    </li>
    <li>
        <p>The <strong>serosa</strong>""", """rather than by surface movement.</p>

<ul>
    <li>
        <p>The <strong>serosa</strong>""")
    # The 11/16 date closed the fungiform bullet; it starts the filiform one, where that day began.
    t = rep(t, """look like mushrooms.</p>

                <p class="date">Monday, 11/16/26</p>
            </li>
            <li>
                <p><strong>Filiform papillae</strong>""", """look like mushrooms.</p>
            </li>
            <li>
                <p class="date">Monday, 11/16/26</p>

                <p><strong>Filiform papillae</strong>""")
    assert words(t) == words(src), "the Full's wording changed"
    return t


# -------------------------------------------------------------- Balanced --
# About half the Full, the length and approach of the API Balanced editions Ian sends (Ian,
# 2026-11-20): each paragraph cut to its definition and the facts the exam needs, the analogies and
# asides dropped, every heading, image, list, box and class date kept. {IMG0}..{IMG9} are the Full's
# own image tags, in order.

BALANCED_BODY = """
<h1>Introduction to the Digestive System</h1>

<p>The <strong>digestive system</strong> consists of the alimentary canal and accessory digestive organs. It plays the following roles in the body:</p>

<ul>
    <li>
        <p><strong>Ingestion</strong> – Food is taken in through the mouth.</p>
    </li>
    <li>
        <p><strong>Propulsion</strong> – Material is moved along the tube, voluntarily (swallowing) or involuntarily (<strong>peristalsis</strong>). The upper esophagus is skeletal muscle, so it is also under voluntary control: a bite just swallowed can come back up, but a pill farther down cannot.</p>
    </li>
    <li>
        <p><strong>Digestion</strong> – Food is broken down into nutrients the body can absorb, starting in the mouth, by mechanical and chemical processes.</p>
        <ul>
            <li>
                <p><strong>Mechanical digestion</strong> is any physical breakdown, all along the canal: chewing, churning in the stomach, and <strong>segmentation</strong> in the intestines, a rhythmic back-and-forth squeezing that mixes food with digestive juices.</p>
            </li>
            <li>
                <p><strong>Chemical digestion</strong> uses enzymes from the stomach, pancreas, and small intestine to split carbohydrates, proteins, and fats into absorbable units.</p>
            </li>
        </ul>
    </li>
    <li>
        <p><strong>Absorption</strong> – Nutrients pass into the blood, mostly in the small intestine, though the stomach and large intestine absorb some substances. (Fats travel through lymphatic vessels, not a focus here.)</p>
    </li>
    <li>
        <p><strong>Elimination</strong> – What cannot be digested leaves as waste through <strong>defecation</strong>, a job of the large intestine.</p>
    </li>
</ul>

<p>The two major functional divisions of the digestive system are:</p>

<ul>
    <li>
        <p>The <strong>alimentary canal</strong> (also called the <strong>gastrointestinal tract</strong> or <strong>GI tract</strong>) is a muscular tube from the mouth to the anus: mouth, pharynx, esophagus, stomach, small intestine, large intestine, and anus. Its contents are technically outside the body until nutrients cross the epithelial lining into blood vessels.</p>
    </li>
    <li>
        <p>The <strong>accessory digestive organs</strong> lie outside the canal and add materials to it: the teeth and tongue (physical breakdown and propulsion), and the salivary glands, gallbladder, liver, and pancreas (<em>chemical</em> breakdown). The pancreas adds enzymes and the liver adds bile to the small intestine; the salivary glands add saliva to the mouth.</p>
    </li>
</ul>

<p>The following diagram shows an overview of the digestive organs:</p>

{IMG0}

<h2>Abdominal Quadrants and Regions</h2>

<p>Clinicians divide the abdomen into <strong>four quadrants</strong>:</p>
{IMG1}

<ul>
    <li>
        <p>The <strong>right upper quadrant</strong> contains the liver, gallbladder, duodenum, and common bile duct.</p>
    </li>
    <li>
        <p>The <strong>left upper quadrant</strong> contains the pancreas, stomach, and pancreatic duct.</p>
    </li>
    <li>
        <p>The <strong>right lower quadrant</strong> contains the ascending colon, appendix, and small intestine.</p>
    </li>
    <li>
        <p>The <strong>left lower quadrant</strong> contains part of the large and small intestine.</p>
    </li>
</ul>

<p>Quadrants give a quick starting point for assessing pain: right lower quadrant pain probably does not involve the stomach or liver, and marked tenderness there suggests appendicitis.</p>

<p>Anatomists divide the abdomen into <strong>nine regions</strong> on a 3×3 grid. The center is the <strong>umbilical region</strong>; above it is the <strong>epigastric region</strong> and below it the <strong>hypogastric region</strong> (also called the <strong>pubic region</strong>). Beside the epigastric region are the <strong>left and right hypochondriac regions</strong>, beside the umbilical region the <strong>left and right lumbar regions</strong>, and beside the hypogastric region the <strong>left and right iliac (inguinal) regions</strong>.</p>
{IMG2}

<p>The names come from landmarks: <em>hypo-</em> (below) + <em>chondr-</em> (cartilage) places the hypochondriac regions under the costal cartilages; the lumbar regions are level with the lumbar vertebrae; the iliac regions lie over the ilia.</p>

<p>Learn to derive the grid rather than memorize organ lists. Organs often straddle borders (the gallbladder sits at the epigastric/right hypochondriac border, the cecum and appendix near the lower right borders). Know roughly where each organ lies: the liver far upper right, the urinary bladder low and central. A bladder extending above the hypogastric region is pathologically overdistended, possibly an emergency.</p>

<p>Clinicians use quadrants to locate symptoms quickly; anatomists use the nine regions to map where organs actually lie.</p>

<h2>Layers of the Alimentary Canal Wall</h2>

<p>The image below shows the structures of the alimentary canal wall:</p>

{IMG3}

<div class="exam-tip">
    <h4>EXAM TIP: Alimentary Canal Wall</h4>

    <p>Be sure that you know the various structures in this image relatively well.</p>
</div>
<p>The wall has four layers. From deep to superficial:</p>

<ul>
    <li>
        <p>The <strong>mucosa</strong> lines the lumen and has three layers (deep to superficial):</p>

        <ul>
            <li>
                <p>The <strong>epithelium</strong>: simple columnar from the stomach through the intestines; nonkeratinized stratified squamous in the mouth and esophagus, which handle rough, unprocessed food. It is continuous with the ducts emptying into the lumen.</p>
            </li>
            <li>
                <p>The <strong>lamina propria</strong>, areolar (loose) connective tissue that supplies the vessels for absorption.</p>
            </li>
            <li>
                <p>The <strong>muscularis mucosae</strong>, a very thin layer of smooth muscle that twitches to dislodge particles stuck in the epithelium.</p>
            </li>
        </ul>
    </li>
    <li>
        <p>The <strong>submucosa</strong> is connective tissue rich in elastic fibers, so the wall distends and recoils. It holds larger glands, blood and lymphatic vessels, and nerves.</p>
    </li>
    <li>
        <p>The <strong>muscularis externa</strong> has an inner circular layer of smooth muscle (narrows the lumen) and an outer longitudinal layer (shortens the tube). Together they produce peristalsis and segmentation from the esophagus onward. The stomach adds a third, oblique layer, and its churning is essentially segmentation.</p>
    </li>
</ul>

<p class="date">Wednesday, 11/11/26</p>

<p><em>There was no class on Wednesday, November 11th, due to the Veterans Day holiday.</em></p>

<p class="date">Friday, 11/13/26</p>

<p>The GI mucosa is not ciliated: the muscular wall provides all the propulsion needed, as in the heart.</p>

<ul>
    <li>
        <p>The <strong>serosa</strong> is the visceral peritoneum, a serous membrane (simple squamous epithelium on thin connective tissue) like the pleura and pericardium. Where it folds back to meet the parietal peritoneum, it forms a mesentery. Retroperitoneal organs have an <strong>adventitia</strong>, a thicker connective tissue layer, instead of a serosa.</p>

        <p>The <strong>visceral peritoneum</strong> touches the organs; the <strong>parietal peritoneum</strong> lines the body wall. They are one continuous membrane, and any peritoneum not touching an organ, including the mesenteries, counts as parietal.</p>
    </li>
</ul>

<h2>Mesenteries</h2>

<p><strong>Mesenteries</strong> are double layers of parietal peritoneum that connect digestive organs to the body wall and suspend them so they do not sag. Each is a sheet, not a tube, carrying vessels, nerves, lymphatics, and fat between its layers, and is named for the organ it attaches to.</p>

<p>Mesenteries serve three important functions:</p>

<ul>
    <li>They anchor organs in place.</li>
    <li>They store adipose.</li>
    <li>They provide a route for vessels to extend to and from the digestive organs.</li>
</ul>

<p>A <strong>dorsal mesentery</strong> (the most common type) runs from the organ to the posterior abdominal wall; a <strong>ventral mesentery</strong> runs to the anterior wall. Both form as the peritoneum wraps the embryonic gut tube. Development is not covered; know the ventral/dorsal and intraperitoneal/retroperitoneal distinctions.</p>

<p>The following are the major <strong>dorsal mesenteries</strong>:</p>

<ul>
    <li>The <strong>greater omentum</strong>, from the greater curvature of the stomach to the posterior abdominal wall. It is the most ventral structure in the abdominal cavity yet a dorsal mesentery, because it hangs down, folds back, and runs dorsally. It is the largest mesentery, a lacy sheet of fat over the other organs, and the first thing seen when the abdomen is opened.</li>
    <li>The <strong>mesentery proper</strong>, for most of the small intestine, attached to the dorsal body wall.</li>
    <li>The <strong>transverse mesocolon</strong>, for the transverse colon, attached to the dorsal body wall.</li>
    <li>The <strong>sigmoid mesocolon</strong>, which connects the sigmoid colon to the body wall.</li>
</ul>

<p>The following are the two <strong>ventral mesenteries</strong>:</p>

<ul>
    <li>The <strong>falciform ligament</strong>, which connects the liver to the anterior abdominal wall and diaphragm (not a bone-to-bone ligament).</li>
    <li>The <strong>lesser omentum</strong>, which connects the liver to the lesser curvature of the stomach and the first part of the duodenum.</li>
</ul>

<p>Together, these two mesenteries anchor the liver and stomach to the ventral body wall near the xiphoid process.</p>

<p><strong>Intraperitoneal organs</strong> have mesenteries and are surrounded by the <strong>peritoneal cavity</strong> (the space between the visceral and parietal layers); <strong>retroperitoneal organs</strong> have none and lie behind the peritoneum against the dorsal body wall. The major intraperitoneal organs (and their mesenteries) are:</p>

<ul>
    <li>Liver – Lesser omentum and falciform ligament</li>
    <li>Stomach – Greater and lesser omentum</li>
    <li>Ileum and jejunum – Mesentery proper</li>
    <li>Transverse colon – Transverse mesocolon</li>
    <li>Sigmoid colon – Sigmoid mesocolon</li>
</ul>

<p>From stomach to rectum, the organs alternate between intraperitoneal and retroperitoneal, counting the jejunum and ileum as one unit:</p>

<ul>
    <li>Stomach – intraperitoneal</li>
    <li>Duodenum – retroperitoneal</li>
    <li>Jejunum and ileum – intraperitoneal</li>
    <li>Ascending colon – retroperitoneal</li>
    <li>Transverse colon – intraperitoneal</li>
    <li>Descending colon – retroperitoneal</li>
    <li>Sigmoid colon – intraperitoneal</li>
    <li>Rectum – retroperitoneal</li>
</ul>

<p>The pancreas is also retroperitoneal. (The ileum is the last part of the small intestine, leading through the ileocecal valve into the cecum.)</p>

<p>The mnemonic "SAD PUCKER" can help you remember the retroperitoneal organs:</p>

<ul>
    <li>Suprarenal glands</li>
    <li>Aorta/IVC</li>
    <li>Duodenum (2nd-4th parts)</li>
    <li>Pancreas (except tail)</li>
    <li>Ureters</li>
    <li>Colon (ascending &amp; descending)</li>
    <li>Kidneys</li>
    <li>Esophagus (lower thoracic part)</li>
    <li>Rectum (lower 2/3)</li>
</ul>

<p><strong>Primarily retroperitoneal organs</strong>, such as the kidneys, develop behind the peritoneal cavity. <strong>Secondarily retroperitoneal organs</strong>, such as the pancreas, duodenum, and colon, start inside it and are pressed against the dorsal wall as the gut folds, losing their mesentery; this is why parts of the duodenum and colon are fixed in place.</p>

<h1>The Mouth, Pharynx, and Esophagus</h1>

<p>The <strong>oral cavity</strong> (or <strong>mouth</strong>) is lined with thick, nonkeratinized stratified squamous epithelium and bounded by the labia (lips), cheeks, palate, and tongue.</p>

<p>The <strong>tongue</strong> is mostly skeletal muscle: voluntary for speaking and moving food, reflexive during much of chewing and swallowing. It is nicknamed the "Great Dodger" because it is rarely bitten.</p>

<p>The basic anatomy of the oral cavity is shown below, with these features to note:</p>
{IMG4}

<ul>
    <li>
        <p>The <strong>uvula</strong> swings back to close the opening between the oropharynx and nasopharynx, keeping liquids out of the nasal cavity, and plays a role in the gag reflex. It is covered by nonkeratinized stratified squamous epithelium.</p>
    </li>
    <li>
        <p>The <strong>fauces</strong> are the archways from the mouth to the pharynx, between the base of the tongue and the soft palate, with the palatine tonsils on their sides. They are the oral counterpart of the internal nares. You do not need the names of the individual arches.</p>
    </li>
    <li>
        <p>The <strong>hard palate</strong>, the anterior roof of the mouth, is four bones (the right and left maxillae and palatine bones), with the <strong>palatine raphe</strong> marking its midline fusion. Behind it the muscular <strong>soft palate</strong> ends as the uvula. Together they separate the oral and nasal cavities.</p>
    </li>
    <li>
        <p>The <strong>labial frenulum</strong> connects the lips to the gums, the <strong>gingiva</strong> (singular) or <strong>gingivae</strong> (plural). The teeth sit in sockets called <strong>alveoli</strong> in the maxilla and mandible.</p>
    </li>
    <li>
        <p>The <strong>lingual frenulum</strong> anchors the tongue to the floor of the mouth. If it reaches too far toward the tip, it limits protrusion: <strong>ankyloglossia</strong> ("tongue-tied"), which can interfere with nursing and is corrected by clipping the frenulum.</p>
    </li>
    <li>
        <p>The <strong>oral vestibule</strong> is the space between the teeth and the cheeks or lips.</p>
    </li>
    <li>
        <p>At the base of the lingual frenulum are the <strong>openings of the submandibular ducts</strong>, with the <strong>openings of the sublingual ducts</strong> lateral to them, so saliva pools under the tongue. The submandibular glands sit near the angle of the mandible; the sublingual glands lie beneath each side of the tongue and drain through many small ducts.</p>

        <p>Forcing a stream of saliva from these ducts, by compressing the submandibular ducts with the floor-of-mouth muscles, is called <strong>gleeking</strong>.</p>
    </li>
    <li>
        <p>The <strong>parotid gland</strong>, the largest salivary gland, sits superficially in front of the ear. The <strong>parotid duct</strong> crosses the cheek, pierces the buccinator, and opens on the inner cheek beside the upper teeth (the upper second molar in anatomy references; Dr. Ahlgren placed it near the upper premolars).</p>
    </li>
    <li>
        <p>The <strong>salivary glands</strong> are accessory digestive organs. Saliva is water-based, with enzymes that aid taste and digestion, and it protects the teeth. They produce approximately 1.5 liters a day, most of it swallowed and reabsorbed.</p>
    </li>
</ul>

<h2>The Tongue</h2>

<p>The <strong>tongue</strong> is the first major muscular organ of mechanical digestion: two kinds of muscle covered by epithelium carrying taste buds. The epithelium regenerates well, for example after a burn.</p>

<p>Its surface is divided into two parts:</p>

<ul>
    <li>
        <p><strong>The posterior one-third of the tongue</strong> lies in the oropharynx, behind the V-shaped <strong>sulcus terminalis</strong> (terminal sulcus) that marks the boundary with the oral cavity. Its bumps are the <strong>lingual tonsil</strong>, a collection of lymphatic tissue, not papillae or taste buds. It is not normally visible, since the tongue turns roughly 90 degrees there to run down the throat.</p>
    </li>
    <li>
        <p><strong>The anterior two-thirds of the tongue</strong> lie in the oral cavity proper and carry visible bumps called <strong>papillae</strong>. Taste buds are microscopic and sit mostly on the sides of the papillae, so food must dissolve in saliva to reach them; where a papilla sits determines which cranial nerve carries its signal.</p>

        <div class="exam-tip">
            <h4>EXAM TIP: Papillae vs. Taste Buds</h4>

            <p>Remember that papillae are NOT taste buds.</p>
        </div>

        <p>Three different kinds of papillae are as follows:</p>

        <ul>
            <li>
                <p><strong>Vallate papillae</strong> (also called circumvallate papillae) are a few very large papillae forming a V in front of the sulcus terminalis, with taste buds on their sides and some on top.</p>
            </li>
            <li>
                <p><strong>Fungiform papillae</strong> are pinkish/reddish, mushroom-shaped papillae with taste buds.</p>
            </li>
            <li>
                <p class="date">Monday, 11/16/26</p>

                <p><strong>Filiform papillae</strong> are white and have no taste buds. The most abundant papillae, they give the tongue its whitish look and form posterior-pointing spikes that hold what you lick (they are especially large in cats).</p>
{IMG5}
            </li>
        </ul>
    </li>
</ul>

<p>Three cranial nerves carry taste: the facial nerve (cranial nerve VII) from the anterior two-thirds, the glossopharyngeal nerve (cranial nerve IX) from the posterior one-third, and the vagus nerve (cranial nerve X) from the epiglottis and throat. (Dr. Ahlgren's boundary at the terminal sulcus gives the vallate papillae to the facial nerve; anatomy references give them to the glossopharyngeal.)</p>

<p>The "tongue map" of separate taste regions is incorrect: every area of the tongue, and the epiglottis, detects every basic taste.</p>

<p>The two kinds of muscles in the tongue are as follows:</p>

<ul>
    <li>
        <p>The <strong>internal muscles of the tongue</strong> attach to the external muscles, not to bone or cartilage, and change its <strong>shape</strong> (curling).</p>
    </li>
    <li>
        <p>The <strong>external muscles of the tongue</strong> attach to the hyoid bone and the skull and change its <strong>position</strong>.</p>

        <p>The <strong>genioglossus muscle</strong> is external, anchored to the mandible and fanning back toward the epiglottis. Its constant tone holds the tongue out of the airway; if it relaxes too much in sleep, the tongue falls back and blocks the airway, causing repeated partial arousals, as in sleep apnea. Be ready to classify it from an image.</p>
    </li>
</ul>

<h2>Pharynx</h2>

<p>The pharynx moves food from the oral cavity to the esophagus. Of its three sections (nasopharynx, oropharynx, laryngopharynx), digestion uses only the oropharynx and the laryngopharynx. Their stratified squamous epithelium protects against rough food.</p>

<p>Swallowing is a sequence: muscles lift the larynx beneath the epiglottis to close the airway, others squeeze the pharyngeal walls to push the bolus into the esophagus, and others lower the larynx to reopen the airway. The airway is sealed mainly by this lifting, which tips the epiglottis posteriorly, rather than by food bending the epiglottis down.</p>

<h2>The Esophagus</h2>

<p>The <strong>esophagus</strong> is a collapsible muscular tube from the laryngopharynx to the stomach, running through the thoracic cavity. Most of it is covered by an <strong>adventitia</strong>; only the short abdominal part has a serosa.</p>

<p>At rest it is collapsed, and its mucosa is folded into rugae that unfold as it distends during swallowing.</p>

<p>Its muscle changes along its length: the top one-third is mainly skeletal muscle (voluntary), the middle one-third mixed, and the bottom one-third only smooth muscle (involuntary).</p>

<p>So food that has not gone far can be brought back up voluntarily, but not once it reaches the smooth muscle. The gag reflex is triggered in the pharynx, especially the oropharynx, not in the esophagus.</p>

<p>The esophagus is lined with nonkeratinized stratified squamous epithelium. At the <strong>cardiac sphincter</strong>, where it enters the stomach, the lining changes abruptly to simple columnar epithelium.</p>

<p>In the mediastinum it lies against the trachealis muscle at the back of the trachea, which stretches to let a large bolus bulge forward.</p>

<p>The esophagus passes through the diaphragm at the <strong>esophageal hiatus</strong>. (The diaphragm also has the aortic hiatus and the vena caval hiatus.)</p>

<h1>The Stomach</h1>

<p>The <strong>stomach</strong>, the widest part of the alimentary canal, lies in the abdominal cavity and is the first site of protein breakdown (saliva starts on carbohydrates but cannot digest protein). It holds food for about four hours, churning it against the acid-secreting lining into <strong>chyme</strong>, a thick, partly digested paste.</p>

<h2>Gross Anatomy</h2>

<p>The stomach is J-shaped, with a concave <strong>lesser curvature</strong> and a convex <strong>greater curvature</strong>. The <strong>cardiac region</strong> surrounds the cardiac sphincter, which controls flow from the esophagus; the dome-shaped <strong>fundus</strong> rises above it.</p>
{IMG6}

<p>The fundus has a high density of enzyme-producing gastric glands, whose secretions run down over the food below.</p>

<p>Toward the duodenum the stomach narrows into the <strong>pyloric region</strong>, ending in the <strong>pyloric canal</strong>. The <strong>pyloric sphincter</strong> controls flow into the duodenum. Both sphincters are thickened rings of the circular smooth muscle and close while the stomach churns. The pyloric sphincter is a sphincter, not a true valve.</p>

<p>If the cardiac sphincter does not close tightly, acid flows back into the esophagus: <strong>gastroesophageal reflux disease (GERD)</strong>, felt as "heartburn" in the chest. The esophageal lining, unlike the stomach's, cannot withstand acid.</p>

<p><strong>Rugae</strong> are temporary (i.e., non-permanent) mucosal folds that flatten as the stomach fills, letting non-stretchy epithelium expand without tearing; they appear in any distensible part of the GI tract. (The small intestine's plicae circulares are permanent.) They are irregular in the body but run in parallel ridges in the pyloric canal, channeling chyme to the duodenum.</p>

<p>The stomach wall has the usual four layers, but its muscularis externa has <strong>three</strong> layers of muscle: an <strong>oblique layer</strong> is added inside the circular layer, so from the serosa inward the order is longitudinal, circular, oblique. The extra layer strengthens churning.</p>

<p>The stomach hangs more vertically in people with long torsos and more horizontally in those with short ones, with no functional effect.</p>

<h2>Tissue Transition at the Cardiac Sphincter</h2>

<p>The epithelium changes sharply at the cardiac sphincter, from the esophagus's protective non-keratinized stratified squamous epithelium to the stomach's simple columnar epithelium, suited to secretion and absorption. Elsewhere in the tract such changes are gradual.</p>

<h2>Production of Pepsin</h2>

<p>The stomach's surface epithelium has <strong>gastric pits</strong>, ducts leading to <strong>gastric glands</strong> that make <strong>gastric juices</strong>. These exocrine glands reach deep into the lamina propria. A <strong>gastric pore</strong> is the surface opening; the gastric pit beneath it only carries secretions, and the secreting part of the gland lies below the pit.</p>

<p><strong>Chief cells</strong> deep in the gland make an inactive precursor, <strong>pepsinogen</strong>. It meets hydrochloric acid (HCl) from <strong>parietal cells</strong>, which line the gland's side walls above the chief cells (<em>pariet-</em> means wall), and becomes <strong>pepsin</strong>, the active protein-digesting (proteolytic) enzyme.</p>

<p>The esophagus and mouth cannot handle acid, so repeated reflux or vomiting, as in bulimia, damages them.</p>

<h1>The Small Intestine</h1>

<p>The <strong>small intestine</strong>, the longest part of the alimentary canal, is the site of most enzymatic digestion and nearly all nutrient absorption. Most of its digestive enzymes come from the pancreas. (It is the small intestine, singular; <em>intestines</em> means the small and large intestine together.)</p>

<p>It looks longer after death, because its smooth muscle loses tone.</p>

<p>Nutrients become part of the internal environment only when they cross its epithelial lining into the blood, which makes that lining a critical boundary.</p>

<p>Chyme enters through the pyloric sphincter and moves through three segments:</p>

<ul>
    <li>
        <p>The <strong>duodenum</strong>, the first and shortest part, is C-shaped and retroperitoneal, running back from the stomach against the posterior body wall. (The jejunum and ileum are intraperitoneal, hanging from the mesentery proper.)</p>
    </li>
    <li>
        <p>The <strong>jejunum</strong> is the middle part of the small intestine, which is typically located in the upper-left portion.</p>
    </li>
    <li>
        <p>The <strong>ileum</strong> is the final, longest part of the small intestine, which is typically located in the lower-right portion and leads into the large intestine. (The ileum is located close to the ilium bone in the pelvis, though the two are spelled differently.)</p>
    </li>
</ul>

<p>Contents move through the small intestine via two mechanisms:</p>

<ul>
    <li>
        <p><strong>Segmentation</strong> – Rhythmic, segmented contractions that mix chyme and move it along.</p>
    </li>
    <li>
        <p><strong>Peristalsis</strong> – Waves of contraction and relaxation that propel material down the tube.</p>
    </li>
</ul>

<p>As the primary site of absorption, the small intestine increases its surface area with:</p>

<ul>
    <li>
        <p><strong>Plicae circulares</strong>, permanent circular mucosal folds whose spiral helps direct chyme (segmentation itself is done by the muscularis). (The term also appears as <em>plicae circularis</em>.)</p>

        <p>Unlike rugae, they do not flatten when the intestine stretches.</p>
    </li>
    <li>
        <p><strong>Villi</strong>, finger-like projections about 1 mm tall, visible to the eye and covered with simple columnar epithelium, giving the lining a shag-carpet look. Capillary beds and lacteals (lymphatic vessels) run up their middle to take up absorbed nutrients.</p>
    </li>
    <li>
        <p><strong>Microvilli</strong>, microscopic projections on the apical side of each epithelial cell on the villi, which increase the surface further.</p>
    </li>
</ul>

<h1>Accessory Organs: The Liver, Gallbladder, and Pancreas</h1>

<p>The <strong>accessory digestive organs</strong> covered here, the liver, gallbladder, and pancreas, aid digestion but lie outside the alimentary canal.</p>

<h2>The Liver and Gallbladder</h2>

<p>The <strong>liver</strong> is the largest gland in the body. It makes <strong>bile</strong>, a green liquid that emulsifies fats. Bile is stored in the <strong>gallbladder</strong>, a green, muscular sac on the underside of the liver's right lobe whose rugae let it expand as it fills.</p>
{IMG7}

<p>The liver is made mostly of <strong>hepatocytes</strong> (epithelial-derived cells) that regenerate rapidly, so it heals exceptionally well.</p>

<p>The liver has <strong>four lobes</strong>: the large left and right lobes and the smaller quadrate and caudate lobes. The <strong>ligamentum teres hepatis</strong> divides the left part into medial and lateral sections, and the <strong>falciform ligament</strong> attaches the liver to the anterior body wall.</p>

<p>Bile leaves the left and right lobes through the left and right <strong>hepatic ducts</strong>, which join as the <strong>common hepatic duct</strong>. That joins the <strong>cystic duct</strong> to form the <strong>common bile duct</strong>, which meets the pancreatic duct and empties into the duodenum at the <strong>major duodenal papilla</strong>, a small bump on the duodenal wall. A sphincter there controls the release of bile and pancreatic secretions.</p>

<p>When the small intestine does not need bile, the sphincter closes and bile backs up the <strong>cystic duct</strong> into the <strong>gallbladder</strong>; a one-way valve keeps it from returning to the liver. Smooth muscle in the bile duct walls moves bile the right way when the gallbladder contracts, releasing it into the duodenum when chyme arrives.</p>

<p>Gallstones (crystallized salts) blocking the cystic duct cause pain, especially as the gallbladder contracts after a fatty meal, but are not usually life-threatening. A stone blocking the major duodenal papilla is far more dangerous, because it also blocks the pancreatic enzymes. Without a gallbladder, fat digestion is less efficient, although the part of the cystic duct left behind stores a little bile.</p>

<p><strong>Primary biliary cholangitis</strong> is an autoimmune disease that slowly destroys the bile ducts within the liver, so bile builds up, leading to liver damage and cirrhosis.</p>

<h2>The Pancreas</h2>

<p>The <strong>pancreas</strong> is a <strong>gland</strong> with an <strong>exocrine function</strong> (producing most of the enzymes for chemical digestion) and an <strong>endocrine function</strong> (secreting the blood-glucose hormones insulin and glucagon).</p>
{IMG8}

<p>It has a large <strong>head</strong> in the curve of the duodenum, an elongated <strong>body</strong>, and a pointed <strong>tail</strong> against the spleen.</p>

<p>The <strong>pancreatic duct</strong> runs through its middle, collecting secretions from smaller ducts and carrying them to the major duodenal papilla, which regulates secretions from both the pancreatic and common bile ducts.</p>

<p>A smaller <strong>accessory duct</strong> gives enzymes a backup route into the duodenum if the main route is blocked, for example by a gallstone.</p>

<p>Without enough pancreatic enzymes, as in pancreatic cancer, food cannot be digested and patients quickly become emaciated.</p>

<h1>The Large Intestine</h1>

<p>The <strong>large intestine</strong> (commonly called the <strong>colon</strong>, though strictly the colon is only part of it) receives what the small intestine did not absorb and reabsorbs water and electrolytes. Material entering the cecum through the <strong>ileocecal valve</strong> is liquid; feces leave far more solid. Without this, we would have constant diarrhea and dehydration.</p>

<p>Chyme thins in the small intestine because enzymes and bile arrive in watery fluid, and the large intestine must recover that water. When it cannot, as in diarrhea, the body loses fluid that would have returned to the blood.</p>

<p class="date">Wednesday, 11/18/26</p>

<p>The large intestine has no constant peristalsis. Instead, an infrequent <strong>mass peristaltic movement</strong> purges material that has collected there.</p>

<p>Mass peristaltic movement starts when the cecum is distended: the stretch triggers the nervous system to send a coordinated wave toward the rectum.</p>

<h2>Gross Anatomy of the Large Intestine</h2>

<p>The diagram below labels the major portions of the gross anatomy of the colon:</p>

{IMG9}

<p>Chyme from the ileum enters the cecum through the <strong>ileocecal valve</strong>, which is stretch-dependent: as the cecum fills, its distension squeezes the valve shut. The <strong>vermiform appendix</strong> is attached to the cecum by a little mesentery.</p>

<p>From the cecum, contents travel up the <strong>ascending colon</strong>, around the <strong>right colic flexure</strong> (or <strong>right hepatic flexure</strong>, beside the liver), across the <strong>transverse colon</strong>, around the <strong>left colic flexure</strong> (or <strong>left splenic flexure</strong>, beside the spleen), down the <strong>descending colon</strong>, and through the S-shaped <strong>sigmoid colon</strong> into the <strong>rectum</strong>. The rectum funnels into the <strong>anal canal</strong>, which ends at the <strong>anus</strong>, controlled by the <strong>anal sphincters</strong>.</p>

<p>The large intestine has several specialized features:</p>

<ul>
    <li>
        <p><strong>Teniae coli</strong> are three stripes of thickened longitudinal muscle along the outside of the colon. Their contraction shortens it and forms haustra.</p>
    </li>
    <li>
        <p>A <strong>haustrum</strong> (plural <em>haustra</em>) is a bulge formed by the taut teniae coli, giving the colon its bumpy look.</p>
    </li>
    <li>
        <p><strong>Epiploic appendages</strong> are fat-filled pouches of visceral peritoneum found only on the intestines; their function is not well understood.</p>
    </li>
</ul>

<p><strong>Goblet cells</strong> make mucus that lubricates waste. They become more numerous distally as material solidifies, protecting the wall from tearing.</p>

<p>Intense endurance exercise speeds intestinal motility and cuts water reabsorption, which can cause a sudden urge and loose stool.</p>

<h2>The Rectum, Anus, and Anal Sphincters</h2>

<p>The <strong>rectum</strong> is retroperitoneal (it has no mesentery). It narrows into the <strong>anal canal</strong>, where a distinct line, the <strong>pectinate line</strong>, lies just below the last ridges. Inside the distal rectum, longitudinal ridges called <strong>anal columns</strong> guide waste toward the exit.</p>

<p>The <strong>rectal valves</strong> are transverse folds of mucosa and muscle inside the rectum that let gas pass while holding back solid waste, which helps maintain continence.</p>

<p>The <strong>anus</strong> is the transition from mucous membrane to skin (cutaneous membrane): simple columnar epithelium becomes keratinized stratified squamous epithelium.</p>

<p>A set of two sphincters control the movement of materials out of the anal canal:</p>

<ul>
    <li>The <strong>internal anal sphincter</strong> is a thickening of the circularly arranged portion of the muscularis externa. It consists of smooth muscle, so we have no volitional control over it.</li>
    <li>The <strong>external anal sphincter</strong> consists of skeletal muscle that we can control.</li>
</ul>

<p>The <strong>levator ani muscle</strong> lifts the anus during defecation, so it occurs more smoothly.</p>

<p>When the rectum fills, stretch receptors trigger a spinal reflex that contracts the rectal walls and relaxes the internal anal sphincter, creating the urge. Defecation happens when you voluntarily inhibit the motor neurons to the external anal sphincter.</p>

<div class="other-box">
    <h4>Clinical Correlation: Hemorrhoids</h4>

    <p>A <strong>hemorrhoid</strong> is a swollen varicose vein (weakened walls and valves) in the mucosal lining or submucosa of the anus. Two types of hemorrhoid are as follows:</p>

    <ul>
        <li><strong>External hemorrhoids</strong> are inferior to the pectinate line: very painful, little bleeding.</li>
        <li><strong>Internal hemorrhoids</strong> are superior to the pectinate line: less pain, heavy bleeding.</li>
    </ul>

    <p>Symptomatic internal hemorrhoids are often treated by rubber-band ligation, which cuts off the vein's blood supply so it shrivels and falls off.</p>

    <p>Bright red blood in stool points to bleeding in the distal large intestine or rectum (undigested blood); black, tarry stool points to bleeding higher in the GI tract (digested blood).</p>
</div>
"""


def balanced(f):
    imgs = re.findall(r"<img\b.*?/>", f, re.S)
    assert len(imgs) == 10, len(imgs)
    body = BALANCED_BODY
    for k, tag in enumerate(imgs):
        body = rep(body, "{IMG%d}" % k, tag)
    t = f[:f.index("<body>") + len("<body>")] + "\n" + body + "\n</body>\n</html>\n"
    assert re.findall(r"<img\b.*?/>", t, re.S) == imgs
    for tag in ('class="exam-tip"', 'class="other-box"'):
        assert t.count(tag) == f.count(tag), tag
    assert headings(t, "1234") == headings(f, "1234") and dates(t) == dates(f)
    for n in re.findall(r"\d[\d,.%×/-]*", re.sub(r"<[^>]+>", " ", f[f.index("<body"):])):
        assert n.rstrip(".,") in t, ("number lost", n)
    share = len(words(t)) / len(words(f))
    assert 0.40 <= share <= 0.55, share   # the API Balanced's length, about half (Ian, 2026-11-20)
    return t


# --------------------------------------------------------------- Concise --
# Laid out like the API Concise editions (Ian, 2026-11-20).

IMG_WALL = ('<img src="https://smokinnotes.s3.us-east-1.amazonaws.com/public/apk2100-253-exam4-chapter23-04-alimentary-canal-wall.png" '
            'alt="Cross-sectional diagram of alimentary canal wall showing serosa with connective tissue and epithelium, muscularis with longitudinal and circular muscle, submucosa, mucosa with muscularis mucosae, connective tissue, and epithelium, plus artery, vein, nerve, and lumen" '
            'class="image-wide-70 content-image" loading="lazy" width="auto" height="auto" />')

CONCISE_BODY = """
<h1>Introduction to the Digestive System</h1>

<p>The <strong>digestive system</strong> = the alimentary canal + the accessory digestive organs.</p>

<table>
  <thead>
    <tr><th>Function</th><th>What happens</th></tr>
  </thead>
  <tbody>
    <tr><td><b>Ingestion</b></td><td>Food taken in through the mouth.</td></tr>
    <tr><td><b>Propulsion</b></td><td>Voluntary (swallowing) or involuntary (<b>peristalsis</b>); upper esophagus is skeletal muscle (voluntary).</td></tr>
    <tr><td><b>Mechanical digestion</b></td><td>Chewing, churning, intestinal <b>segmentation</b> (rhythmic mixing), along the whole canal.</td></tr>
    <tr><td><b>Chemical digestion</b></td><td>Enzymes (stomach, pancreas, small intestine) split carbohydrates, proteins, fats into absorbable units.</td></tr>
    <tr><td><b>Absorption</b></td><td>Nutrients → blood; mostly in the small intestine (fats go via lymphatics, not a focus).</td></tr>
    <tr><td><b>Elimination</b></td><td>Undigested waste leaves by <b>defecation</b> (large intestine).</td></tr>
  </tbody>
</table>

<ul>
  <li><b>Alimentary canal</b> (GI tract): muscular tube, mouth → pharynx → esophagus → stomach → small intestine → large intestine → anus. Its contents are technically <b>outside</b> the body until they cross the epithelial lining.</li>
  <li><b>Accessory organs</b>: outside the tube; they <b>add materials</b> to it. Teeth and tongue (physical breakdown); salivary glands, liver, gallbladder, pancreas (chemical breakdown).</li>
</ul>

<h2>Abdominal Quadrants and Regions</h2>

<table>
  <thead>
    <tr><th>Quadrant</th><th>Contents</th></tr>
  </thead>
  <tbody>
    <tr><td><b>Right upper</b></td><td>Liver, gallbladder, duodenum, common bile duct</td></tr>
    <tr><td><b>Left upper</b></td><td>Pancreas, stomach, pancreatic duct</td></tr>
    <tr><td><b>Right lower</b></td><td>Ascending colon, appendix, small intestine</td></tr>
    <tr><td><b>Left lower</b></td><td>Parts of the large and small intestine</td></tr>
  </tbody>
</table>

<ul>
  <li><b>Quadrants</b> = clinical: where symptoms appear (right lower quadrant pain + tenderness → suspect appendicitis).</li>
  <li><b>Nine regions</b> = anatomical: where organs actually lie, on a 3×3 grid.</li>
</ul>

<ul>
  <li>Center: <b>umbilical</b>; above it <b>epigastric</b>; below it <b>hypogastric (pubic)</b>.</li>
  <li>Beside epigastric: <b>hypochondriac</b> (<em>hypo-</em> below + <em>chondr-</em> cartilage → under the costal cartilages).</li>
  <li>Beside umbilical: <b>lumbar</b> (level with the lumbar vertebrae). Beside hypogastric: <b>iliac (inguinal)</b> (over the ilia).</li>
  <li>Know rough positions, not organ lists: liver far upper right; bladder low and central (above the hypogastric region = overdistension).</li>
</ul>

<h2>Layers of the Alimentary Canal Wall</h2>

""" + IMG_WALL + """

<div class="exam-tip">
<h4>EXAM TIP: Alimentary Canal Wall</h4>
<p>Know the structures in this cross section well.</p>
</div>

<table>
  <thead>
    <tr><th>Layer (deep → superficial)</th><th>Key features</th></tr>
  </thead>
  <tbody>
    <tr><td><b>Mucosa</b></td><td>Three layers: <b>epithelium</b> (simple columnar stomach → intestines; nonkeratinized stratified squamous in mouth and esophagus, for rough food; not ciliated), <b>lamina propria</b> (areolar tissue, vessels for absorption), <b>muscularis mucosae</b> (thin smooth muscle; twitches to dislodge stuck fragments).</td></tr>
    <tr><td><b>Submucosa</b></td><td>Elastic connective tissue → wall distends and recoils; larger glands, blood and lymphatic vessels, nerves.</td></tr>
    <tr><td><b>Muscularis externa</b></td><td>Inner circular (narrows lumen) + outer longitudinal (shortens tube) smooth muscle → peristalsis and segmentation. Stomach adds an oblique layer.</td></tr>
    <tr><td><b>Serosa</b></td><td>Visceral peritoneum (simple squamous on thin connective tissue). Retroperitoneal organs have an <b>adventitia</b> instead.</td></tr>
  </tbody>
</table>

<ul>
  <li><b>Visceral peritoneum</b> touches organs; <b>parietal peritoneum</b> lines the body wall. One continuous membrane; any peritoneum not touching an organ (including the mesenteries) counts as parietal.</li>
</ul>

<h2>Mesenteries</h2>

<ul>
  <li><b>Mesentery</b>: double sheet of parietal peritoneum carrying vessels, nerves, lymphatics, and fat between its layers; named for the organ it attaches to.</li>
  <li>Functions: <b>anchor</b> organs (and suspend them so they do not sag), <b>store adipose</b>, <b>route vessels</b> to and from the organs.</li>
  <li><b>Dorsal</b> → posterior wall (most common); <b>ventral</b> → anterior wall.</li>
</ul>

<table>
  <thead>
    <tr><th>Type</th><th>Mesentery</th><th>Connects</th></tr>
  </thead>
  <tbody>
    <tr><td rowspan="4"><b>Dorsal</b></td><td><b>Greater omentum</b></td><td>Greater curvature of stomach → posterior wall; largest; most ventral structure, yet dorsal.</td></tr>
    <tr><td><b>Mesentery proper</b></td><td>Most of the small intestine → dorsal wall</td></tr>
    <tr><td><b>Transverse mesocolon</b></td><td>Transverse colon → dorsal wall</td></tr>
    <tr><td><b>Sigmoid mesocolon</b></td><td>Sigmoid colon → body wall</td></tr>
    <tr><td rowspan="2"><b>Ventral</b></td><td><b>Falciform ligament</b></td><td>Liver → anterior wall and diaphragm (not a bone-to-bone ligament)</td></tr>
    <tr><td><b>Lesser omentum</b></td><td>Liver → lesser curvature and first part of the duodenum</td></tr>
  </tbody>
</table>

<h3>Intraperitoneal vs. Retroperitoneal:</h3>
<ul>
  <li><b>Intraperitoneal</b>: has a mesentery, surrounded by the peritoneal cavity. <b>Retroperitoneal</b>: no mesentery, pressed against the dorsal wall.</li>
  <li>Stomach → rectum alternates (jejunum + ileum count as one): stomach (intra) → duodenum (retro) → jejunum/ileum (intra) → ascending colon (retro) → transverse colon (intra) → descending colon (retro) → sigmoid colon (intra) → rectum (retro). The pancreas is also retroperitoneal.</li>
  <li>Mnemonic <b>SAD PUCKER</b>: Suprarenal glands, Aorta/IVC, Duodenum (2nd-4th parts), Pancreas (except tail), Ureters, Colon (ascending &amp; descending), Kidneys, Esophagus (lower thoracic part), Rectum (lower 2/3).</li>
  <li><b>Primarily</b> retroperitoneal (never enclosed; kidneys) vs. <b>secondarily</b> (start inside, pressed back and fused as the gut folds; pancreas, duodenum, colon).</li>
</ul>

<h1>The Mouth, Pharynx, and Esophagus</h1>

<ul>
  <li><b>Oral cavity</b>: lined with thick nonkeratinized stratified squamous epithelium; bounded by lips, cheeks, palate, tongue.</li>
</ul>

<table>
  <thead>
    <tr><th>Feature</th><th>Key points</th></tr>
  </thead>
  <tbody>
    <tr><td><b>Uvula</b></td><td>Swings back to seal the nasopharynx (keeps liquids out of the nose); gag reflex.</td></tr>
    <tr><td><b>Fauces</b></td><td>Archway from mouth to oropharynx (palatine tonsils at the sides); the oral counterpart of the internal nares.</td></tr>
    <tr><td><b>Hard / soft palate</b></td><td>Hard: four bones (maxillae + palatine bones), <b>palatine raphe</b> on the midline. Soft: muscular, ends as the uvula.</td></tr>
    <tr><td><b>Labial frenulum</b></td><td>Lips → gums (<b>gingivae</b>); teeth sit in <b>alveoli</b>.</td></tr>
    <tr><td><b>Lingual frenulum</b></td><td>Tongue → floor of mouth; too long → <b>ankyloglossia</b> ("tongue-tied"), fixed by clipping.</td></tr>
    <tr><td><b>Oral vestibule</b></td><td>Space between teeth and cheeks or lips.</td></tr>
    <tr><td><b>Salivary ducts</b></td><td>Submandibular openings at the frenulum base; sublingual openings lateral to them.</td></tr>
    <tr><td><b>Parotid gland</b></td><td>Largest salivary gland, in front of the ear; duct pierces the buccinator, opens beside the upper teeth.</td></tr>
    <tr><td><b>Saliva</b></td><td>Water-based, with enzymes; about 1.5 liters a day, mostly reabsorbed.</td></tr>
  </tbody>
</table>

<h2>The Tongue</h2>

<ul>
  <li><b>Posterior one-third</b>: in the oropharynx, behind the V-shaped <b>sulcus terminalis</b>; its bumps are the <b>lingual tonsil</b> (lymphatic tissue), not papillae.</li>
  <li><b>Anterior two-thirds</b>: in the oral cavity; visible <b>papillae</b>. Taste buds are microscopic and sit mostly on the sides of papillae, so food must dissolve in saliva to reach them.</li>
</ul>

<div class="exam-tip">
<h4>EXAM TIP: Papillae vs. Taste Buds</h4>
<p>Papillae are NOT taste buds.</p>
</div>

<table>
  <thead>
    <tr><th>Papillae</th><th>Taste buds?</th><th>Notes</th></tr>
  </thead>
  <tbody>
    <tr><td><b>Vallate</b> (circumvallate)</td><td>Yes (sides, some on top)</td><td>Few, very large; V-shape in front of the sulcus terminalis.</td></tr>
    <tr><td><b>Fungiform</b></td><td>Yes</td><td>Pinkish/reddish, mushroom-shaped.</td></tr>
    <tr><td><b>Filiform</b></td><td>No</td><td>Most abundant, white; posterior-pointing spikes grip what you lick (ice cream); large in cats.</td></tr>
  </tbody>
</table>

<ul>
  <li>Taste nerves: <b>facial (VII)</b> anterior two-thirds; <b>glossopharyngeal (IX)</b> posterior one-third; <b>vagus (X)</b> epiglottis and throat.</li>
  <li>The "tongue map" is wrong: every area detects every basic taste.</li>
  <li><b>Internal muscles</b>: not attached to bone; change <b>shape</b> (curling). <b>External muscles</b>: attached to hyoid and skull; change <b>position</b>.</li>
  <li><b>Genioglossus</b> (external, anchored to the mandible): constant tone holds the tongue out of the airway; relaxed in sleep → airway occluded → partial arousals (sleep apnea).</li>
</ul>

<h2>Pharynx</h2>

<ul>
  <li>Digestion uses the <b>oropharynx</b> and <b>laryngopharynx</b> (not the nasopharynx). Stratified squamous lining resists rough food.</li>
  <li>Swallowing: larynx lifts (epiglottis tips back, sealing the airway) → constrictors push the bolus into the esophagus → larynx lowers.</li>
</ul>

<h2>The Esophagus</h2>

<ul>
  <li>Collapsible muscular tube, laryngopharynx → stomach; mostly covered by <b>adventitia</b> (serosa only on the short abdominal part).</li>
  <li>Collapsed at rest; mucosa folded into rugae so it can unfold, not tear.</li>
  <li>Muscle: top one-third skeletal (voluntary), middle one-third mixed, bottom one-third smooth (involuntary). The gag reflex is in the pharynx, not the esophagus.</li>
  <li>Enters the stomach through the <b>cardiac sphincter</b>; passes the diaphragm at the <b>esophageal hiatus</b> (also the aortic and vena caval hiatuses).</li>
</ul>

<h1>The Stomach</h1>

<ul>
  <li>Widest part of the canal; first site of <b>protein</b> breakdown (saliva starts on carbohydrates but cannot digest protein).</li>
  <li>Holds food about four hours, churning it into <b>chyme</b> (thick, partly digested paste).</li>
</ul>

<h2>Gross Anatomy</h2>

<ul>
  <li>J-shaped: <b>lesser curvature</b> (concave) and <b>greater curvature</b> (convex).</li>
  <li><b>Cardiac region</b> (near the cardiac sphincter) → <b>fundus</b> (dome above it; dense gastric glands whose secretions "rain down") → body → <b>pyloric region</b> → <b>pyloric canal</b> → <b>pyloric sphincter</b> → duodenum.</li>
  <li>Both sphincters are thickened circular smooth muscle and close during churning; the pyloric sphincter is not a true valve.</li>
  <li><b>GERD</b>: a loose cardiac sphincter lets acid into the esophagus → "heartburn."</li>
  <li><b>Rugae</b>: temporary mucosal folds that flatten as the stomach fills (in any distensible part of the tract); straight ridges in the pyloric canal.</li>
  <li>Muscularis externa has <b>three</b> layers; from the serosa inward: longitudinal, circular, <b>oblique</b> (deepest) → stronger churning.</li>
</ul>

<h2>Tissue Transition at the Cardiac Sphincter</h2>

<ul>
  <li>Abrupt change: esophagus nonkeratinized stratified squamous (abrasion) → stomach simple columnar (secretion and absorption). Gradual elsewhere.</li>
</ul>

<h2>Production of Pepsin</h2>

<ul>
  <li><b>Gastric pore</b> (surface opening) → <b>gastric pit</b> (duct; secretes nothing) → <b>gastric gland</b> (exocrine; in the lamina propria) → <b>gastric juices</b>.</li>
  <li><b>Chief cells</b> (deep) make <b>pepsinogen</b> + <b>parietal cells</b> (side walls) make <b>HCl</b> → <b>pepsin</b>, the active protein-digesting enzyme.</li>
</ul>

<h1>The Small Intestine</h1>

<ul>
  <li>Longest part of the canal; most enzymatic digestion and nearly all absorption; most enzymes come from the pancreas.</li>
  <li>Segments: <b>duodenum</b> (first, shortest, C-shaped, retroperitoneal) → <b>jejunum</b> (middle, upper left) → <b>ileum</b> (last, longest, lower right; joins the large intestine).</li>
  <li>Movement: <b>segmentation</b> (mixing, some propulsion) and <b>peristalsis</b>.</li>
</ul>

<table>
  <thead>
    <tr><th>Surface-area feature</th><th>Key points</th></tr>
  </thead>
  <tbody>
    <tr><td><b>Plicae circulares</b></td><td>Permanent circular mucosal folds (unlike rugae); spiral directs chyme.</td></tr>
    <tr><td><b>Villi</b></td><td>About 1 mm, visible to the eye ("shag carpet"); capillary beds and lacteals inside.</td></tr>
    <tr><td><b>Microvilli</b></td><td>On each epithelial cell's apical side; microscopic.</td></tr>
  </tbody>
</table>

<h1>Accessory Organs: The Liver, Gallbladder, and Pancreas</h1>

<h2>The Liver and Gallbladder</h2>

<ul>
  <li><b>Liver</b>: largest gland; <b>hepatocytes</b> regenerate rapidly. Makes <b>bile</b> (green; emulsifies fats).</li>
  <li><b>Four lobes</b>: left, right, quadrate, caudate. <b>Ligamentum teres hepatis</b> divides the left part; <b>falciform ligament</b> attaches to the anterior wall.</li>
  <li><b>Gallbladder</b>: muscular sac under the right lobe; stores bile; rugae let it expand.</li>
  <li>Bile route: hepatic ducts → <b>common hepatic duct</b> + <b>cystic duct</b> → <b>common bile duct</b> → joins the pancreatic duct → <b>major duodenal papilla</b> (sphincter-controlled) → duodenum.</li>
  <li>Sphincter closed → bile backs up the cystic duct into the gallbladder (a one-way valve blocks the liver).</li>
  <li><b>Gallstones</b>: in the cystic duct → painful, not usually life-threatening; at the major duodenal papilla → dangerous (blocks pancreatic enzymes). No gallbladder → poorer fat digestion.</li>
  <li><b>Primary biliary cholangitis</b>: autoimmune destruction of the liver's bile ducts → bile buildup, cirrhosis.</li>
</ul>

<h2>The Pancreas</h2>

<ul>
  <li>Gland with <b>exocrine</b> (most digestive enzymes) and <b>endocrine</b> (insulin, glucagon) functions.</li>
  <li><b>Head</b> in the curve of the duodenum, <b>body</b>, <b>tail</b> against the spleen.</li>
  <li><b>Pancreatic duct</b> → major duodenal papilla; <b>accessory duct</b> = backup route if the main one is blocked.</li>
</ul>

<h1>The Large Intestine</h1>

<ul>
  <li>Receives what the small intestine did not absorb; <b>reabsorbs water and electrolytes</b> (liquid in, solid feces out). Failure → diarrhea and dehydration.</li>
  <li>No constant peristalsis: infrequent <b>mass peristaltic movement</b>, triggered by stretch of the cecum.</li>
</ul>

<h2>Gross Anatomy of the Large Intestine</h2>

<ul>
  <li>Route: ileum → <b>ileocecal valve</b> (stretch-dependent; closes as the cecum fills) → <b>cecum</b> (with the <b>vermiform appendix</b>) → <b>ascending colon</b> → <b>right colic (hepatic) flexure</b> → <b>transverse colon</b> → <b>left colic (splenic) flexure</b> → <b>descending colon</b> → <b>sigmoid colon</b> (S-curve) → <b>rectum</b> → <b>anal canal</b> → <b>anus</b>.</li>
  <li><b>Teniae coli</b>: three stripes of thickened longitudinal muscle; shorten the colon and form <b>haustra</b> (bulges).</li>
  <li><b>Epiploic appendages</b>: fat-filled pouches of visceral peritoneum; function unknown.</li>
  <li><b>Goblet cells</b> increase distally as waste solidifies (mucus prevents tearing).</li>
</ul>

<h2>The Rectum, Anus, and Anal Sphincters</h2>

<ul>
  <li><b>Rectum</b>: retroperitoneal; <b>anal columns</b> channel waste down; <b>rectal valves</b> hold stool while letting gas pass; the <b>pectinate line</b> lies just below the ridges at the end of the anal canal.</li>
  <li><b>Anus</b>: mucous → cutaneous membrane (simple columnar → keratinized stratified squamous).</li>
  <li><b>Internal anal sphincter</b>: smooth muscle, involuntary. <b>External anal sphincter</b>: skeletal, voluntary. <b>Levator ani</b> lifts the anus during defecation.</li>
  <li>Defecation reflex: rectal stretch → spinal reflex contracts the rectum and relaxes the internal sphincter → you choose when to relax the external sphincter.</li>
</ul>

<h3>Hemorrhoids:</h3>
<ul>
  <li>Swollen varicose veins in the anal mucosa or submucosa. <b>External</b> (below the pectinate line): painful, little bleeding. <b>Internal</b> (above it): little pain, heavy bleeding; treated by rubber-band ligation.</li>
  <li>Bright red blood in stool → distal source (undigested); black, tarry stool → higher source (digested).</li>
</ul>

<h2>Glossary</h2>

<table>
  <thead>
    <tr><th>Term</th><th>Definition</th></tr>
  </thead>
  <tbody>
    <tr><td><b>Alimentary canal</b></td><td>The muscular tube from mouth to anus (GI tract).</td></tr>
    <tr><td><b>Peristalsis</b></td><td>Involuntary waves of contraction that propel material.</td></tr>
    <tr><td><b>Segmentation</b></td><td>Rhythmic back-and-forth squeezing that mixes intestinal contents.</td></tr>
    <tr><td><b>Adventitia</b></td><td>Connective tissue covering in place of a serosa.</td></tr>
    <tr><td><b>Mesentery</b></td><td>Double sheet of peritoneum that anchors organs and carries vessels.</td></tr>
    <tr><td><b>Ankyloglossia</b></td><td>A lingual frenulum that limits tongue protrusion ("tongue-tied").</td></tr>
    <tr><td><b>Chyme</b></td><td>The thick, partly digested paste the stomach produces.</td></tr>
    <tr><td><b>Rugae</b></td><td>Temporary mucosal folds that let a distensible organ expand.</td></tr>
    <tr><td><b>Pepsinogen</b></td><td>Inactive precursor from chief cells, activated by HCl to pepsin.</td></tr>
    <tr><td><b>Plicae circulares</b></td><td>Permanent circular folds of the small intestine's mucosa.</td></tr>
    <tr><td><b>Villi / microvilli</b></td><td>Projections of the mucosa / of each epithelial cell that increase absorptive surface.</td></tr>
    <tr><td><b>Bile</b></td><td>Green liquid from the liver that emulsifies fats.</td></tr>
    <tr><td><b>Major duodenal papilla</b></td><td>Shared opening of the bile and pancreatic ducts into the duodenum.</td></tr>
    <tr><td><b>Haustra</b></td><td>Bulges of the colon formed by the teniae coli.</td></tr>
    <tr><td><b>Pectinate line</b></td><td>Line in the anal canal dividing external from internal hemorrhoids.</td></tr>
  </tbody>
</table>

<h2>Key Takeaways</h2>

<ul>
  <li>Quadrants are clinical; the nine regions (3×3 grid) are anatomical. Derive the regions from the landmarks.</li>
  <li>Wall layers, deep → superficial: mucosa, submucosa, muscularis externa, serosa (or adventitia).</li>
  <li>Greater omentum: the most ventral structure, yet a dorsal mesentery. Ventral mesenteries: falciform ligament and lesser omentum.</li>
  <li>Stomach to rectum alternates intraperitoneal / retroperitoneal; SAD PUCKER lists the retroperitoneal organs.</li>
  <li>Papillae are not taste buds; filiform papillae have none. The tongue map is a myth.</li>
  <li>Stomach muscle adds an innermost oblique layer; chief cells + parietal cells → pepsin.</li>
  <li>A gallstone at the major duodenal papilla is more dangerous than one in the cystic duct.</li>
  <li>Internal anal sphincter involuntary, external voluntary; hemorrhoids are named by the pectinate line.</li>
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
    assert "Ahlgren" not in t and t.count("<img") == 1 and t.count('class="exam-tip"') == 2
    for n in ("1.5 liters", "four hours", "1 mm", "3×3", "2nd-4th", "lower 2/3", "VII", "IX", "(X)"):
        assert n in t, n
    share = len(words(t)) / len(words(f))
    assert 0.18 <= share <= 0.28, share   # the API Concise editions run about a fifth of the Full
    return t


def main(src, out):
    out = pathlib.Path(out)
    out.mkdir(parents=True, exist_ok=True)
    f = full(open(src, encoding="utf-8").read())
    b = balanced(f)
    c = concise(f)
    base = "APK2100-263-Exam4-Chapter23-"
    for name, html in (("Full", f), ("Balanced", b), ("Concise", c)):
        (out / f"{base}{name}.html").write_text(html, encoding="utf-8")
        print(f"{base}{name}.html: {len(words(html))} words ({len(words(html)) / len(words(f)):.0%})")


if __name__ == "__main__":
    main(*sys.argv[1:3])
