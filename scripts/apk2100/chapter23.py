#!/usr/bin/env python3
"""APK2100 Exam 4, Chapter 23 (the digestive system): the Full reformatted, and its Balanced and Concise.

    python scripts/apk2100/chapter23.py SOURCE_FULL.html OUTDIR

* Full: formatting only, the wording untouched (asserted word for word): a doctype, the live house
  script, the stylesheet ahead of the fonts, the pipeline's AUDIT notes out, and the two class dates
  that sat inside the muscularis-externa bullet moved out to the page beside the paragraphs they
  start (the wall-layers list then resumes at the serosa).
* Balanced: about 75% of the Full (Ian, 2026-11-20): long paragraphs condensed; every image, exam
  tip, box, number and date kept.
* Concise: in the layout of the API Concise editions Ian sends (Ian, 2026-11-20): definition tables,
  short fragment bullets, a Glossary table and Key Takeaways, about a fifth of the Full; the Full's
  own h1/h2 headings, and only the two figures the chapter tells students to know by sight.

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
# Each entry replaces one paragraph or list item, found by its opening words, with a tighter version
# that keeps every fact and number.

CONDENSE = [
    ("<strong>Propulsion</strong> – Material has to keep moving",
     "<strong>Propulsion</strong> – Material keeps moving along the tube, voluntarily (as in swallowing) or involuntarily, by <strong>peristalsis</strong>. The upper (proximal) end of the esophagus is skeletal rather than smooth muscle, so it is also under voluntary control: that is why something just swallowed can sometimes be brought back up, while a pill that has traveled farther down cannot."),
    ("<strong>Digestion</strong> – The digestive system breaks food down",
     "<strong>Digestion</strong> – Food is broken down into smaller nutrients the body can absorb and use, starting in the mouth, by both mechanical and chemical processes."),
    ("<strong>Mechanical digestion</strong> includes several types",
     "<strong>Mechanical digestion</strong> is any physical breakdown, and it happens along the whole canal: chewing in the mouth, churning in the stomach (which presses the contents against its own walls), and <strong>segmentation</strong> in the intestines, a rhythmic back-and-forth squeezing that mixes food with digestive juices and enhances absorption. Dr. Ahlgren's analogy: knead mashed potatoes and gravy sealed in a plastic bag, and the two blend together."),
    ("<strong>Chemical digestion</strong> breaks down food even further",
     "<strong>Chemical digestion</strong> uses enzymes from the stomach, pancreas, and small intestine to split carbohydrates, proteins, and fats into units small enough to cross the intestinal wall."),
    ("<strong>Absorption</strong> – The body absorbs small nutrients",
     "<strong>Absorption</strong> – Small nutrients pass into the blood, which carries them where they are needed. Most absorption is in the small intestine, though the stomach and large intestine absorb certain substances. (Fats travel through lymphatic vessels, which will not be a focus.)"),
    ("<strong>Elimination</strong> – Some of the things that we ingest",
     "<strong>Elimination</strong> – What cannot be digested and absorbed leaves as waste through <strong>defecation</strong>, a job of the large intestine."),
    ("Note that the contents of the alimentary canal are technically",
     "Its contents are technically outside the body: nutrients become part of the body only once they cross the canal's epithelial lining and move into blood vessels."),
    ("The <strong>accessory digestive organs</strong> include organs",
     "The <strong>accessory digestive organs</strong> aid digestion but lie outside the canal: the teeth and tongue (physical breakdown and propulsion of food into the GI tract) and the organs of <em>chemical</em> breakdown (the salivary glands, gallbladder, liver, and pancreas)."),
    ("Dr. Ahlgren emphasized that accessory organs are not part",
     "They are not part of the continuous tube; they add materials to it. The pancreas releases digestive enzymes into the small intestine, the salivary glands add saliva to the mouth, and the liver, which is not tubular, makes bile and delivers it into the small intestine."),
    ("This provides a useful starting point for an initial assessment",
     "Quadrants are a starting point for assessing an injury: pain in the right lower quadrant probably does not involve the stomach or liver, which lie in other quadrants. (Extreme tenderness there might suggest appendicitis.)"),
    ("The names make sense once you know the landmarks.",
     "The names follow landmarks. <em>Hypo-</em> means below and <em>chondr-</em> refers to cartilage, so the hypochondriac regions sit beneath the costal cartilages; because the diaphragm domes upward, that space belongs to the abdominal cavity. The lumbar regions are level with the lumbar vertebrae at the navel, and straight below them lie the ilia, which name the iliac regions."),
    ("Dr. Ahlgren emphasized that students should focus on understanding",
     "Focus on deriving the nine regions visually: picture the 3×3 grid with the umbilicus at the center and the costal cartilages above, and each region's position follows."),
    ("Remember that these regions include all of the organs",
     "The regions include the organs within the body, not just its surface, and because many organs span more than one region, their locations are approximate: the gallbladder typically lies at the border of the epigastric and right hypochondriac regions, and the cecum (with its appendix) near the border of the lower right regions."),
    ("Dr. Ahlgren said you do not need to memorize a region-by-region",
     "You do not need a region-by-region list of organs, only a general sense of where each sits: the liver as far to the upper right as possible, the urinary bladder low and in the center. Practice locating the small intestine, colon, stomach, spleen, and liver."),
    ("Clinicians use quadrants to diagnose pain or injury quickly.",
     "Clinicians use quadrants to diagnose pain or injury quickly, by where symptoms appear; anatomists use the nine regions to map where organs actually lie. The urinary bladder, for example, normally sits only in the hypogastric (pubic) region, and if it extends higher it is pathologically overdistended, possibly a medical emergency."),
    ("The innermost lining is made of epithelium that varies",
     "The innermost lining is epithelium that varies along the tract: simple columnar from the stomach through the intestines, but nonkeratinized stratified squamous in the mouth and esophagus, which need a more protective lining for rough, unprocessed food pushed down a narrow tube. It is continuous with the ducts that empty into the lumen."),
    ("The <strong>muscularis mucosae</strong> is a very thin layer",
     "The <strong>muscularis mucosae</strong> is a very thin layer of smooth muscle forming the outermost part of the mucosa. It moves the mucosa to dislodge small, hard fragments lodged between epithelial cells, twitching rhythmically to protect the delicate surface, much as you work loose a popcorn kernel caught between your gum and tooth."),
    ("The <strong>submucosa</strong> consists primarily of connective tissue",
     "The <strong>submucosa</strong> is mainly connective tissue rich in elastic fibers, which let the wall distend as material fills it and recoil after it passes, without permanent deformation. It also holds larger glands (their secretory portions sit here and their ducts cross the mucosa to the luminal surface) and extensive blood vessels, lymphatic vessels, and nerves."),
    ("The <strong>muscularis externa</strong> is the outermost layer of muscle",
     "The <strong>muscularis externa</strong> is the outermost muscle layer: an inner circular layer of smooth muscle, nearest the lumen, and an outer longitudinal layer. Circular contraction narrows the lumen and longitudinal contraction shortens the tube; alternating, they create the \"squeeze, shrink, squeeze, shrink\" motion that pushes material forward and mixes it. Present from the esophagus onward, the two layers drive both peristalsis and segmentation. The stomach adds a third, oblique layer (discussed later), and its mixing action, churning, is essentially segmentation carried out by the stomach."),
    ("Dr. Ahlgren noted that the mucosal epithelium of the GI tract",
     "The mucosal epithelium of the GI tract is not ciliated: the thick muscular wall already provides strong propulsion, just as the heart, which also lacks cilia, moves blood by muscular contraction rather than surface movement."),
    ("The <strong>serosa</strong> is the outermost layer",
     "The <strong>serosa</strong>, the outermost layer, is the visceral peritoneum, a serous membrane like the pleura (around the lungs) and the pericardium (around the heart): simple squamous epithelium on a thin layer of connective tissue. Where the visceral peritoneum folds back to meet the parietal peritoneum, it forms the mesentery, a double layer that suspends digestive organs and carries blood vessels, lymphatics, and nerves. Retroperitoneal organs (discussed below) are not covered by peritoneum and have an <strong>adventitia</strong> in place of a serosa, a thicker connective tissue layer like the one seen in blood vessels."),
    ("Dr. Ahlgren emphasized the difference between the two layers",
     "The <strong>visceral peritoneum</strong> touches the organ surfaces; the <strong>parietal peritoneum</strong> does not, lining the inner body wall instead. They are one continuous membrane folding back on itself to form the mesenteries, and by Dr. Ahlgren's definition any peritoneum not touching an organ, including the layers of the mesenteries, counts as parietal."),
    ("Several digestive organs are connected to the body wall",
     "Several digestive organs are connected to the body wall by <strong>mesenteries</strong>, double layers of parietal peritoneum. Besides anchoring the organs, they suspend them within the abdominal cavity; without them, the organs would sag toward the lower abdomen and bulge the body wall like a \"spare tire.\""),
    ("To picture how a mesentery forms",
     "Picture the peritoneum wrapping a section of gut tube. Because vessels and nerves reach the tube from the back, the membrane cannot close behind it; its two sides meet around those vessels and nerves and run back to the body wall as a pair before spreading out along it. That paired sheet, with vessels, nerves, lymphatics, and fat between its layers, is the mesentery. Mesenteries are sheets, not tubes, and each is named for the organ it attaches to."),
    ("Two types of mesenteries are <strong>dorsal</strong>",
     "<strong>Dorsal</strong> and <strong>ventral mesenteries</strong> are named for the side of the abdominal cavity they reach. A <strong>dorsal mesentery</strong> (the most common type) runs from the organ to the posterior abdominal wall; a <strong>ventral mesentery</strong> runs from the organ to the anterior abdominal wall."),
    ("Both ventral and dorsal mesenteries originate during embryonic",
     "Both form during embryonic development: the peritoneum wraps the primitive gut from both sides, and where its layers meet in front of the tube they create the ventral mesentery, behind it the dorsal mesentery, which is why each region of the tract hangs from the anterior or posterior body wall. The developmental images need not be memorized, since development is not covered in this course; the takeaways are the ventral versus dorsal and the intraperitoneal versus retroperitoneal distinctions."),
    ("The <strong>greater omentum</strong>, which connects",
     "The <strong>greater omentum</strong>, which connects the greater curvature (the inferior aspect) of the stomach to the abdomen's posterior wall. Unusually, it is the most ventral structure in the abdominal cavity yet a dorsal mesentery: it hangs from the greater curvature, folds back on itself, and runs dorsally. By far the largest mesentery, it looks like a lacy sheet of fat draped over the other organs and is the first thing seen when the abdomen is opened."),
    ("Note that not all digestive organs have a mesentery.",
     "Not all digestive organs have a mesentery: <strong>intraperitoneal organs</strong> do and <strong>retroperitoneal organs</strong> do not. The <strong>peritoneal cavity</strong> is the space between the visceral and parietal layers. Intraperitoneal organs are completely surrounded by it, while retroperitoneal organs lie behind (dorsal to) the peritoneum, pressed against the dorsal body wall. The major intraperitoneal organs (and their mesenteries) are:"),
    ("Dr. Ahlgren offered a trick for the digestive organs",
     "A trick: from the stomach to the rectum, the organs alternate between intraperitoneal and retroperitoneal, counting the jejunum and ileum as one unit and the duodenum on its own."),
    ("Retroperitoneal organs can be classified as either primarily",
     "Retroperitoneal organs are either primarily or secondarily so. <strong>Primarily retroperitoneal organs</strong>, such as the kidneys, develop behind the peritoneal cavity and were never enclosed by it. <strong>Secondarily retroperitoneal organs</strong>, such as the pancreas, duodenum, and colon, begin inside it but are pressed against the dorsal body wall as the gut elongates and folds, losing their mesentery and fusing to the wall, which is why parts of the duodenum and colon are fixed in place rather than freely suspended."),
    ("The <strong>tongue</strong> is composed primarily of skeletal muscle",
     "The <strong>tongue</strong> is mostly skeletal muscle, so it moves voluntarily for speaking and handling food, yet many of its movements in chewing and swallowing are reflexive, which makes it highly coordinated. Nicknamed the \"Great Dodger,\" it is rarely bitten despite sitting between the teeth."),
    ("The <strong>uvula</strong> functions much like the epiglottis",
     "The <strong>uvula</strong> works much like the epiglottis, swinging back to close the opening between the oropharynx and the nasopharynx so liquids do not enter the nasal cavity; it also plays a role in the gag reflex. Its nonkeratinized stratified squamous epithelium protects it from acidic or abrasive foods and liquids."),
    ("The <strong>fauces</strong> are the archways",
     "The <strong>fauces</strong> are the archways forming a narrow passage from the mouth to the pharynx, between the base of the tongue and the soft palate, with the palatine tonsils on their sides; you do not need the names of the individual arches. Think of them as the oral counterpart of the internal nares: the passage from the oral cavity into the oropharynx."),
    ("The <strong>lingual frenulum</strong> is a small fold",
     "The <strong>lingual frenulum</strong> anchors the tongue to the floor of the mouth. If it extends too far toward the tip, it limits protrusion, a condition called <strong>ankyloglossia</strong> (\"tongue-tied\") that can interfere with nursing in newborns and is easily corrected by clipping the frenulum."),
    ("At the base of the lingual frenulum are the",
     "At the base of the lingual frenulum are the <strong>openings of the submandibular ducts</strong>, which secrete saliva, and lateral to them the <strong>openings of the sublingual ducts</strong>. The submandibular glands sit near the angle of the mandible and send their ducts forward to this spot; the sublingual glands lie beneath each side of the tongue and drain through many small ducts. With so many glands draining there, saliva pools under the tongue, which is why dental hygienists place suction there."),
    ("Some people can voluntarily force saliva to spray",
     "Some people can force a small stream of saliva from these ducts, called <strong>gleeking</strong>, when the floor-of-mouth muscles compress the submandibular ducts, usually triggered by something spicy or sour. It serves no purpose, and not everyone can do it."),
    ("The <strong>parotid gland</strong> is the largest salivary gland.",
     "The <strong>parotid gland</strong>, the largest salivary gland, is flat and broad and sits superficially just in front of the ear, for which it is named. The long <strong>parotid duct</strong> crosses the cheek, pierces the buccinator muscle, and opens on the inner cheek beside the upper teeth: next to the upper second molar in anatomy references, near the upper premolars in Dr. Ahlgren's description."),
    ("The <strong>salivary glands</strong> are accessory digestive organs.",
     "The <strong>salivary glands</strong> are accessory digestive organs. Saliva is water-based, carries enzymes that help us taste and digest food, and protects the teeth from sugar and other substances that stick to them. Healthy glands produce approximately 1.5 liters a day, most of it swallowed and reabsorbed."),
    ("<strong>The posterior one-third of the tongue</strong> – The posterior",
     "<strong>The posterior one-third of the tongue</strong> – This part lies outside the oral cavity, in the oropharynx, behind the V-shaped <strong>sulcus terminalis</strong> (terminal sulcus), the tongue's final groove and the boundary between the two. Its bumps are not taste buds or papillae but the <strong>lingual tonsil</strong>, a collection of lymphatic tissue. It is not normally visible, because it lies deep in the oropharynx and the tongue turns roughly 90 degrees behind the groove to run down the throat."),
    ("<strong>The anterior two-thirds of the tongue</strong> – The anterior",
     "<strong>The anterior two-thirds of the tongue</strong> – This part lies in the oral cavity proper and carries visible bumps called <strong>papillae</strong>, which are not taste buds: taste buds are microscopic. A taste bud is a modified epithelial cell wired to a sensory neuron, and where its papilla sits determines which cranial nerve carries the signal. Most sit on the sides of the papillae, in the creases between them, so food must be broken down and dissolved in saliva well enough to slip in and reach them."),
    ("<strong>Filiform papillae</strong> are white papillae",
     "<strong>Filiform papillae</strong> are white and have no taste buds. The most abundant papillae, they give the tongue its whitish look. Rather than tasting, these projection papillae form spikes pointing posteriorly, so that what you lick stays on the tongue."),
    ("Cats have particularly large filiform papillae",
     "Cats have particularly large filiform papillae, which make their tongues rough enough for constantly cleaning dead skin, hair, and debris from themselves."),
    ("Taste information from the tongue is carried to the brain",
     "Three cranial nerves carry taste to the brain: the facial nerve (cranial nerve VII) from the anterior two-thirds, the glossopharyngeal nerve (cranial nerve IX) from the posterior one-third, and the vagus nerve (cranial nerve X) from the epiglottis and nearby throat. Dr. Ahlgren drew the boundary at the terminal sulcus, which puts the vallate papillae in facial nerve territory; anatomy references assign them to the glossopharyngeal nerve."),
    ("Dr. Ahlgren emphasized that the classic \"tongue map\"",
     "The classic \"tongue map\" of separate sweet, salty, sour, and bitter regions is wrong: every area of the tongue, and even the epiglottis, has receptors for every basic taste. What differs is which compounds activate which receptors, not where the receptors are."),
    ("One external muscle is the <strong>genioglossus muscle</strong>",
     "One external muscle is the <strong>genioglossus muscle</strong>, which always has a bit of tone. Its front end is anchored to the mandible, making it external, and it fans back through the tongue toward the epiglottis; be ready to classify it from an image. Its steady tone holds the tongue forward and out of the airway. If it relaxes too much during sleep, the tongue slides back and occludes the airway, and the body rouses just enough to restore tone. These repeated partial arousals break up sleep without fully waking the person, who believes they slept through the night; people with sleep apnea commonly have this problem."),
    ("Dr. Ahlgren pointed out that the stratified squamous epithelium",
     "The stratified squamous epithelium of the oral cavity and esophagus protects them from rough foods, such as crunchy, triangle-shaped chips like Doritos that can scrape the mouth or throat."),
    ("The muscles in the pharynx and neck contract",
     "Swallowing is a sequence of muscle actions in the pharynx and neck: one group lifts the larynx beneath the epiglottis to close off the airway, a second squeezes the pharyngeal walls to push food into the esophagus, and a third lowers the larynx to reopen the airway once the bolus has passed. The first step, elevation of the pharynx, folds the epiglottis down over the airway. The epiglottis is elastic cartilage, but food does not simply bend it down: the airway is sealed mainly by lifting, as the epiglottis tips posteriorly while the structures beneath it are pulled up, and the pharyngeal constrictor muscles then squeeze the bolus past."),
    ("At rest the esophagus is collapsed",
     "At rest the esophagus is collapsed, its lumen flat and closed; it is distensible and opens only during swallowing. Its mucosa is folded into rugae, extra lining that lets the non-stretchy epithelium unfold rather than tear as the wall expands, like an elastic waistband's fabric, bunched when relaxed and flat when pulled."),
    ("As you move down the esophagus, the muscular portion",
     "Its muscle changes from skeletal to smooth along its length: the top one-third is mainly skeletal muscle under conscious control (used to swallow food and start its propulsion), the middle one-third a mixture of skeletal and smooth muscle, and the bottom one-third only smooth muscle, which we cannot voluntarily control."),
    ("Because the upper portion of the esophagus contains skeletal",
     "So food that has not traveled too far can sometimes be voluntarily moved back into the mouth, but not once it reaches the smooth muscle portion. The gag reflex is triggered in the pharynx (especially the oropharynx), not in the esophagus."),
    ("In the mediastinum, the esophagus lies directly behind",
     "In the mediastinum, the esophagus lies directly behind the trachea, against the trachealis muscle spanning the open backs of the tracheal cartilages; because muscle can stretch, the esophagus can bulge forward as a large bolus passes. The uncomfortable \"lump\" of swallowing something too big comes partly from pressure on the trachealis."),
    ("The <strong>stomach</strong>, which is the widest portion",
     "The <strong>stomach</strong>, the widest part of the alimentary canal, lies in the abdominal cavity and is the first site of protein breakdown. It stores food for about four hours (the figure varies with the person and the meal), churning it against the lining where stomach acid is secreted. Chemical digestion starts earlier, since saliva works on carbohydrates (and arguably some fats) from the mouth onward, but saliva cannot break down protein. Physical and chemical breakdown turn the food into <strong>chyme</strong>, a thick, sticky, partly digested paste."),
    ("The stomach is an interesting organ to observe during dissections",
     "In dissections, the stomach shows whether the animal or person had just eaten a large meal: if so, it is distended and puffy; if not, small and shriveled."),
    ("The fundus has functional significance beyond its shape.",
     "The fundus has a high density of enzyme-producing gastric glands, and because it lies above the rest of the stomach, its secretions \"rain down\" onto the food below and mix thoroughly with it, much as tears from the lacrimal glands wash down over the eye."),
    ("As the stomach approaches the duodenum, it funnels down.",
     "Toward the duodenum the stomach funnels down: the narrowing is the <strong>pyloric region</strong> and its final stretch the <strong>pyloric canal</strong>. The <strong>pyloric sphincter</strong> controls flow from the stomach into the duodenum. The pyloric and cardiac sphincters both close when the stomach churns, and both are rings of smooth muscle where the circular layer of the muscularis externa thickens. The pyloric sphincter is sometimes labeled a valve, but it is a sphincter, not a true valve."),
    ("When the cardiac sphincter fails to close tightly",
     "When the cardiac sphincter fails to close tightly, stomach acid flows back into the esophagus: <strong>gastroesophageal reflux disease (GERD)</strong>. Because the esophagus lies directly behind the heart, the burning pain is felt in the chest as \"heartburn\"; the stomach's simple columnar epithelium withstands the acid, but the esophageal lining cannot."),
    ("<strong>Rugae</strong> are temporary (i.e., non-permanent) folds",
     "<strong>Rugae</strong> are temporary (i.e., non-permanent) folds of mucosal lining that stretch out and disappear as the stomach fills. (The small intestine's plicae circulares, discussed later, are similar but permanent.) Rugae appear in any distensible part of the GI tract: because epithelium is not stretchy, they let organs such as the stomach, bladder, and parts of the intestines expand and recoil without tearing. In the stomach's body and most of the pyloric region they are irregular, but in the pyloric canal they straighten into parallel ridges that channel chyme toward the duodenum."),
    ("The stomach's walls contain all four layers",
     "The stomach wall has all four typical layers (mucosa, submucosa, muscularis externa, and serosa), but its muscularis externa has <strong>three</strong> layers of muscle rather than two: besides the longitudinal and circular layers, an <strong>oblique layer</strong> forms its deepest layer. The extra layer is added on the inside, so from the serosa toward the lumen the order is longitudinal, circular, oblique. It optimizes the stomach's mechanical churning (Dr. Ahlgren compared it to churning butter, a surprisingly accurate analogy)."),
    ("The orientation of the stomach can vary from person to person.",
     "Stomach orientation varies: it hangs more vertically in people with long torsos and lies more horizontally in those with shorter ones, with the lesser curvature above the greater. The difference has no functional impact."),
    ("The surface epithelium of the stomach contains <strong>gastric pits</strong>",
     "The stomach's surface epithelium contains <strong>gastric pits</strong>, ducts leading to <strong>gastric glands</strong> that produce <strong>gastric juices</strong> for chemical digestion. These exocrine glands secrete into ducts that empty into the stomach lumen, and they reach deep into the lamina propria. A <strong>gastric pore</strong> is the opening on the surface; the gastric pit is the wide duct beneath it, which carries secretions but makes none, and the secreting part of the gland lies below the pit. The glands are the surface's simple columnar epithelium dipping down into tubes, which is why the stomach's mucosa is so thick."),
    ("The <strong>small intestine</strong> is the longest part",
     "The <strong>small intestine</strong>, the longest part of the alimentary canal, is the site of most enzymatic digestion and nearly all nutrient absorption; its length maximizes the time available to pull nutrients from food. Most of its digestive enzymes are secreted by the pancreas. (The organ is the small intestine, not the small intestines; <em>intestines</em> means the small and large intestine together.)"),
    ("Dr. Ahlgren mentioned that, interestingly, the small intestine",
     "The small intestine appears longer after death, because the smooth muscle in its walls loses tone and relaxes."),
    ("Recall that the contents of the lumen of the gastrointestinal",
     "Its lumen is technically part of the external environment; nutrients join the internal environment only after crossing its epithelial lining into the bloodstream, which makes that epithelium a critical boundary for absorption."),
    ("The <strong>duodenum</strong> is the first part",
     "The <strong>duodenum</strong> is the first and shortest part, a C-shaped retroperitoneal organ. Diagrams make it look as though it swings out beside the stomach, but it runs back from the stomach and lies against the posterior body wall. (The jejunum and ileum are intraperitoneal and hang from the mesentery proper, sometimes simply called \"the mesentery.\")"),
    ("<strong>Plicae circulares</strong> are permanent circular folds",
     "<strong>Plicae circulares</strong> are permanent circular folds in the mucosa that greatly increase surface area for absorption. Their spiral arrangement helps direct chyme distally, but segmentation is performed by the muscularis, not caused by the folds. (In this course the term also appears as <em>plicae circularis</em>.)"),
    ("The plicae circulares are kind of like the rugae",
     "Unlike the stomach's rugae, they are permanent: no matter how much you stretch the small intestine, they will not go away."),
    ("<strong>Villi</strong> are finger-like projections",
     "<strong>Villi</strong> are finger-like projections of the mucosa, covered with simple columnar epithelium, that increase the surface area for absorption. About 1 mm tall, they can be seen without a microscope and give the lining a fuzzy, shag-carpet look. Capillary beds and lacteals (structures of the lymph vessel system) run up the middle of each villus, so nutrients that cross its epithelial wall diffuse into the capillary beds."),
    ("Before moving on to the large intestine, we will look",
     "Before the large intestine come three <strong>accessory digestive organs</strong>, which aid digestion but lie outside the alimentary canal: the liver, gallbladder, and pancreas."),
    ("The <strong>liver</strong> is the largest gland in the body.",
     "The <strong>liver</strong> is the largest gland in the body. It produces <strong>bile</strong>, a green liquid that aids digestion by emulsifying fats, stored in the <strong>gallbladder</strong>, a muscular sac on the underside of the liver's right lobe. The gallbladder's lining has rugae that let it expand as it fills, and it looks green because of the bile it stores."),
    ("The common bile duct and the pancreatic duct join together",
     "The common bile duct and pancreatic duct join before entering the duodenum at this shared opening, where a sphincter controls when bile and pancreatic secretions are released into the small intestine."),
    ("The distal sphincters of the bile duct are closed",
     "When the small intestine no longer needs bile, the distal sphincters of the bile duct close, and bile backs up the <strong>cystic duct</strong> into the <strong>gallbladder</strong> for storage. A small unidirectional valve keeps it from flowing back into the liver."),
    ("People sometimes have to have their gallbladders removed",
     "Gallbladders are sometimes removed because crystallized salts form gallstones that block the cystic duct, causing pain, especially as the gallbladder contracts against the obstruction during a fatty meal. This is very painful but not typically life-threatening. A gallstone obstructing the major duodenal papilla is far more dangerous, because it can block the release of pancreatic enzymes, which are essential for digestion and nutrient absorption. Without a gallbladder, people digest fat less efficiently, although surgeons usually leave part of the cystic duct, which can act as a small \"mini gallbladder\" with limited bile storage."),
    ("Dr. Ahlgren mentioned that <strong>primary biliary cholangitis</strong>",
     "<strong>Primary biliary cholangitis</strong> is an autoimmune condition in which the body slowly destroys the bile ducts within the liver over many years, so bile accumulates and causes liver damage and cirrhosis, showing how much digestion and liver function depend on intact bile ducts."),
    ("The <strong>pancreatic duct</strong> runs through the middle",
     "The <strong>pancreatic duct</strong> runs through the middle of the pancreas, collects secretions from smaller ducts throughout it, and carries them to the major duodenal papilla, the interface with the duodenum, which acts as a sphincter for both the pancreatic duct and the common bile duct."),
    ("Note that there is also a smaller <strong>accessory duct</strong>",
     "A smaller <strong>accessory duct</strong>, above or below the pancreatic duct, gives enzymes and other secretions an alternative route into the duodenum. This functional redundancy is a backup if the primary route through the major duodenal papilla becomes obstructed, for example by a gallstone."),
    ("Pancreatic enzymes play a crucial role in digestion",
     "Pancreatic enzymes are crucial: people with pancreatic cancer often become extremely emaciated very quickly, because their pancreases no longer make enough enzymes to digest food and they suffer from malnutrition."),
    ("The <strong>large intestine</strong> (commonly called",
     "The <strong>large intestine</strong> (commonly called the <strong>colon</strong>, though strictly the colon is only part of it; everyday speech uses the terms interchangeably) receives whatever the small intestine does not absorb, and its major function is reabsorbing water and electrolytes. Chyme entering the cecum through the <strong>ileocecal valve</strong> is relatively liquid; feces leaving the GI tract are much more solid. Without this reabsorption we would be in a constant state of diarrhea and dehydration."),
    ("Chyme leaves the stomach thick and pasty.",
     "Chyme leaves the stomach thick and pasty and thins in the small intestine, because enzymes and bile arrive suspended in water-based fluid, so what reaches the large intestine is essentially liquid. The large intestine must reabsorb that water and its dissolved electrolytes before waste is eliminated. When it cannot, as in diarrhea, the body loses fluid that would return to the bloodstream, reducing the water in the blood and impairing the delivery of nutrients and other substances."),
    ("Peristalsis constantly moves materials along the stomach",
     "Peristalsis constantly moves material through the stomach and small intestine, but not the large intestine, which instead uses infrequent <strong>mass peristaltic movement</strong> to purge material that has sat there for quite a while. (Constant peristalsis there would mean pooping all the time!)"),
    ("Chyme from the ileum of the small intestine enters the cecum",
     "Chyme from the ileum enters the cecum through the <strong>ileocecal valve</strong>, a stretch-dependent, \"sphincterish type valve\": as the cecum fills and distends, it compresses the opening until it closes, preventing more material from entering. The <strong>vermiform appendix</strong> is attached to the cecum and suspended by a little bit of mesentery."),
    ("<strong>Epiploic appendages</strong> are pouches",
     "<strong>Epiploic appendages</strong> are fat-filled pouches of visceral peritoneum that hang from the intestines of humans and animals and are found nowhere else in the body; although prominent, their function is largely unknown."),
    ("The large intestine also has many <strong>goblet cells</strong>",
     "The large intestine also has many <strong>goblet cells</strong>, whose mucus lubricates the passage of waste. They increase distally as material becomes more solid, reducing friction and protecting the wall from tearing, which matters most in the distal large intestine, where a rupture could expose blood vessels to fecal material."),
    ("Intense endurance exercise can sometimes trigger",
     "Intense endurance exercise can trigger an urgent need to defecate: prolonged running increases intestinal motility and shortens the time for water reabsorption, which can lead to the sudden passage of loose stool."),
    ("The <strong>rectum</strong> is a retroperitoneal organ",
     "The <strong>rectum</strong> is retroperitoneal, lacking the extra layer of mesentery. Distally it narrows into the <strong>anal canal</strong>, where ridges form at the last part and a very distinct line, the <strong>pectinate line</strong>, lies just below them. Inside the distal rectum, longitudinal mucosal ridges called <strong>anal columns</strong> channel material downward toward the anal canal."),
    ("The <strong>rectal valves</strong> are internal folds",
     "The <strong>rectal valves</strong> are transverse folds of mucosa and muscle inside the rectum that help regulate the passage of fecal matter and gas and maintain continence. By forming partial barriers, they let gas pass while holding back solid waste, which is how healthy people can pass gas without releasing stool."),
    ("Normal adults can obviously control when and where",
     "Normal adults control when and where they defecate. When the rectum fills, stretch (distention) receptors signal neurons in the spinal cord, triggering a spinal reflex that contracts the rectal walls and relaxes the internal anal sphincter; this is the urge to defecate. When the time is right, you voluntarily inhibit the motor neurons to the external anal sphincter, and feces pass out of the rectum (hopefully into the toilet)."),
    ("Note that the color of blood in stool",
     "The color of blood in stool hints at where bleeding is: bright red blood usually comes from the distal large intestine or rectum, such as from hemorrhoids, because it has not been digested, while black or tarry stool suggests bleeding higher in the GI tract, where the blood has been digested."),
]


def balanced(f):
    t = f
    for start, new in CONDENSE:
        t = para(t, start, new)
    for tag in ("<img", 'class="exam-tip"', 'class="other-box"'):
        assert t.count(tag) == f.count(tag), tag
    assert headings(t, "1234") == headings(f, "1234") and dates(t) == dates(f)
    for n in re.findall(r"\d[\d,.%×/-]*", re.sub(r"<[^>]+>", " ", f[f.index("<body"):])):
        assert n.rstrip(".,") in t, ("number lost", n)
    share = len(words(t)) / len(words(f))
    assert 0.70 <= share <= 0.80, share   # about 75% (Ian, 2026-11-20)
    return t


# --------------------------------------------------------------- Concise --
# Laid out like the API Concise editions (Ian, 2026-11-20).

IMG_REGIONS = ('<img src="https://smokinnotes.s3.us-east-1.amazonaws.com/public/apk2100-253-exam4-chapter23-03-nine-abdominal-regions.png" '
               'alt="Diagram showing the nine abdominal regions including right hypochondriac, epigastric, left hypochondriac, right lumbar, umbilical, left lumbar, right iliac, hypogastric, and left iliac regions with associated organs listed" '
               'class="image-wide-70 content-image" loading="lazy" width="auto" height="auto" />')
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
    <tr><td><b>Propulsion</b></td><td>Voluntary (swallowing) or involuntary (<b>peristalsis</b>). The upper esophagus is skeletal muscle, so a just-swallowed bite can come back up; a pill farther down cannot.</td></tr>
    <tr><td><b>Mechanical digestion</b></td><td>Any physical breakdown, along the whole canal: chewing, stomach churning, intestinal <b>segmentation</b> (rhythmic back-and-forth squeezing that mixes food with juices).</td></tr>
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

""" + IMG_REGIONS + """

<ul>
  <li>Center: <b>umbilical</b>; above it <b>epigastric</b>; below it <b>hypogastric (pubic)</b>.</li>
  <li>Beside epigastric: <b>hypochondriac</b> (<em>hypo-</em> below + <em>chondr-</em> cartilage → under the costal cartilages).</li>
  <li>Beside umbilical: <b>lumbar</b> (level with the lumbar vertebrae). Beside hypogastric: <b>iliac (inguinal)</b> (over the ilia).</li>
  <li>Locations are approximate: the gallbladder sits at the epigastric/right hypochondriac border; the cecum and appendix near the lower right borders.</li>
  <li>No region-by-region organ list needed: know the liver far upper right, the bladder low and central (a bladder rising above the hypogastric region = overdistension, possibly an emergency).</li>
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
  <li><b>Dorsal</b> → posterior wall (most common); <b>ventral</b> → anterior wall. (Development is not covered.)</li>
</ul>

<table>
  <thead>
    <tr><th>Type</th><th>Mesentery</th><th>Connects</th></tr>
  </thead>
  <tbody>
    <tr><td rowspan="4"><b>Dorsal</b></td><td><b>Greater omentum</b></td><td>Greater curvature of stomach → posterior wall. Largest; the most ventral structure yet dorsal; lacy fat drape seen first on opening the abdomen.</td></tr>
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
    <tr><td><b>Salivary ducts</b></td><td>Submandibular duct openings at the frenulum base; sublingual openings lateral to them (saliva pools under the tongue). <b>Gleeking</b> = forced spray from submandibular ducts.</td></tr>
    <tr><td><b>Parotid gland</b></td><td>Largest salivary gland, in front of the ear; duct pierces the buccinator, opens beside the upper teeth (second molar in references, premolars in this course).</td></tr>
    <tr><td><b>Saliva</b></td><td>Water-based, with enzymes; protects teeth; about 1.5 liters a day, mostly reabsorbed.</td></tr>
  </tbody>
</table>

<h2>The Tongue</h2>

<ul>
  <li>Mostly skeletal muscle, voluntary and reflexive; the "Great Dodger" (rarely bitten). Epithelium regenerates well.</li>
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
  <li>Taste nerves: <b>facial (VII)</b> anterior two-thirds; <b>glossopharyngeal (IX)</b> posterior one-third; <b>vagus (X)</b> epiglottis and throat. (Vallate papillae: facial by the sulcus boundary used here; glossopharyngeal in references.)</li>
  <li>The "tongue map" is wrong: every area detects every basic taste.</li>
  <li><b>Internal muscles</b>: not attached to bone; change <b>shape</b> (curling). <b>External muscles</b>: attached to hyoid and skull; change <b>position</b>.</li>
  <li><b>Genioglossus</b> (external, anchored to the mandible): constant tone holds the tongue out of the airway; relaxed in sleep → airway occluded → partial arousals (sleep apnea).</li>
</ul>

<h2>Pharynx</h2>

<ul>
  <li>Digestion uses the <b>oropharynx</b> and <b>laryngopharynx</b> (not the nasopharynx). Stratified squamous lining resists rough food.</li>
  <li>Swallowing: muscles lift the larynx under the epiglottis (airway sealed mainly by <b>lifting</b>, epiglottis tips back) → constrictors squeeze the bolus into the esophagus → larynx lowers to reopen the airway.</li>
</ul>

<h2>The Esophagus</h2>

<ul>
  <li>Collapsible muscular tube, laryngopharynx → stomach; mostly covered by <b>adventitia</b> (serosa only on the short abdominal part).</li>
  <li>Collapsed at rest; mucosa folded into rugae so it can unfold, not tear.</li>
  <li>Muscle: top one-third skeletal (voluntary), middle one-third mixed, bottom one-third smooth (involuntary). The gag reflex is in the pharynx, not the esophagus.</li>
  <li>Lies behind the trachea against the stretchy trachealis (a big bolus presses on it).</li>
  <li>Enters the stomach through the <b>cardiac sphincter</b>; passes the diaphragm at the <b>esophageal hiatus</b> (also the aortic and vena caval hiatuses).</li>
</ul>

<h1>The Stomach</h1>

<ul>
  <li>Widest part of the canal; first site of <b>protein</b> breakdown (saliva starts on carbohydrates but cannot digest protein).</li>
  <li>Holds food about four hours, churning it into <b>chyme</b> (thick, partly digested paste).</li>
</ul>

<h2>Gross Anatomy</h2>

<ul>
  <li>J-shaped: <b>lesser curvature</b> (concave) and <b>greater curvature</b> (convex). Orientation varies with torso length.</li>
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
  <li>The esophagus and mouth cannot handle acid (damaged by reflux or bulimia).</li>
</ul>

<h1>The Small Intestine</h1>

<ul>
  <li>Longest part of the canal; most enzymatic digestion and nearly all absorption; most enzymes come from the pancreas. Looks longer after death (muscle relaxes).</li>
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
  <li>Pancreatic cancer → too few enzymes → rapid emaciation.</li>
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
  <li><b>Goblet cells</b> increase distally as waste solidifies (mucus prevents tearing). Endurance running → faster motility → loose stool.</li>
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
    <tr><td><b>Accessory digestive organs</b></td><td>Organs outside the canal that add materials to it.</td></tr>
    <tr><td><b>Peristalsis</b></td><td>Involuntary waves of contraction that propel material.</td></tr>
    <tr><td><b>Segmentation</b></td><td>Rhythmic back-and-forth squeezing that mixes intestinal contents.</td></tr>
    <tr><td><b>Lamina propria</b></td><td>Areolar connective tissue of the mucosa, carrying vessels for absorption.</td></tr>
    <tr><td><b>Muscularis mucosae</b></td><td>Thin smooth muscle of the mucosa that dislodges trapped particles.</td></tr>
    <tr><td><b>Adventitia</b></td><td>Connective tissue covering in place of a serosa.</td></tr>
    <tr><td><b>Mesentery</b></td><td>Double sheet of peritoneum that anchors organs and carries vessels.</td></tr>
    <tr><td><b>Retroperitoneal</b></td><td>Behind the peritoneum, with no mesentery.</td></tr>
    <tr><td><b>Ankyloglossia</b></td><td>A lingual frenulum that limits tongue protrusion ("tongue-tied").</td></tr>
    <tr><td><b>Papillae</b></td><td>Visible bumps on the tongue; not taste buds.</td></tr>
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
  <li>Six functions: ingestion, propulsion, mechanical and chemical digestion, absorption, elimination.</li>
  <li>Quadrants are clinical; the nine regions (3×3 grid) are anatomical. Derive the regions from the landmarks.</li>
  <li>Wall layers, deep → superficial: mucosa, submucosa, muscularis externa, serosa (or adventitia).</li>
  <li>Greater omentum: the most ventral structure, yet a dorsal mesentery. Ventral mesenteries: falciform ligament and lesser omentum.</li>
  <li>Stomach to rectum alternates intraperitoneal / retroperitoneal; SAD PUCKER lists the retroperitoneal organs.</li>
  <li>Papillae are not taste buds; filiform papillae have none. The tongue map is a myth.</li>
  <li>Esophagus: skeletal → mixed → smooth muscle by thirds; abrupt epithelial change at the cardiac sphincter.</li>
  <li>Stomach muscle adds an innermost oblique layer; chief cells + parietal cells → pepsin.</li>
  <li>Small intestine: plicae circulares, villi, microvilli maximize absorption.</li>
  <li>A gallstone at the major duodenal papilla is more dangerous than one in the cystic duct.</li>
  <li>The large intestine reabsorbs water; mass peristalsis, not constant peristalsis.</li>
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
    assert "Ahlgren" not in t and t.count("<img") == 2 and t.count('class="exam-tip"') == 2
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
