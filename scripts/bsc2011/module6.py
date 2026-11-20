#!/usr/bin/env python3
"""BSC2011 Exam 3, Module 6 (conservation biology): the Full reformatted, and its Balanced and Concise.

    python scripts/bsc2011/module6.py SOURCE_FULL.html OUTDIR

* Full: formatting only (asserted word for word apart from two added spaces): the live house script and
  head order, a doctype, the AUDIT notes out, a stray <br> out, wide equations scrolling in their own
  line on a phone, and quiz answer boxes that sit beside a floated image rather than under it (Ian's
  readme, 2026-11-20).
* Balanced: the Full with checked cuts (each must match once); every box, quiz, image, number and date kept.
* Concise: bullets and tables on the Full's own h1/h2 headings, then Glossary and Key Takeaways.
"""
import re
import sys
import pathlib

OLD_JS = "https://smokinnotes.s3.us-east-1.amazonaws.com/content/sn25-v5.js"
LIVE_JS = "https://smokinnotes.s3.us-east-1.amazonaws.com/studyguide/sn25-v2.js"
FONTS = '''    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Red+Hat+Display:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
'''
CSS = '''    <link rel="stylesheet" href="https://smokinnotes.s3.us-east-1.amazonaws.com/content/sn25-v6.css">
'''
PHONE = '''    <style>
    /* phones: a wide equation scrolls in its own line instead of pushing the page sideways */
    @media (max-width: 600px) {
      mjx-container { overflow-x: auto; overflow-y: hidden; max-width: 100%; }
      mjx-container:not([display="true"]) { display: inline-block; vertical-align: middle; }
    }
    </style>
</head>'''
TABLES = "      mjx-container:not([display=\"true\"]) { display: inline-block; vertical-align: middle; }\n"


def rep(t, a, b):
    n = t.count(a)
    assert n == 1, (n, a[:100])
    return t.replace(a, b)


def words(html):
    body = html[html.index("<body"):]
    body = re.sub(r"<(script|style)\b.*?</\1>|<!--.*?-->", " ", body, flags=re.S)
    return re.sub(r"<[^>]+>", " ", body).split()


def headings(html):
    return [(m.group(1), re.sub(r"<[^>]+>", "", m.group(2)).strip())
            for m in re.finditer(r"<h([12])[^>]*>(.*?)</h\1>", html, re.S)]


def dates(html):
    return re.findall(r'class="date">([^<]*)', html)


# ------------------------------------------------------------------ Full --

def full(src):
    t = "<!DOCTYPE html>\n" + src if not src.lstrip().lower().startswith("<!doctype") else src
    t = rep(t, OLD_JS, LIVE_JS)
    t = rep(t, FONTS + CSS, CSS + FONTS)
    t = re.sub(r"<!-- [A-Z ]+AUDIT:.*?-->\n?", "", t)
    t = rep(t, '<p class="date">Monday, 11/30/26</p>\n<br>\n', '<p class="date">Monday, 11/30/26</p>\n\n')
    t = rep(t, "\\(N_m\\)= The number", "\\(N_m\\) = The number")
    t = rep(t, "\\(N_f\\)= The number", "\\(N_f\\) = The number")
    t = rep(t, ".qb-interactive .qb-options { margin: 0.6em 0; }",
            ".qb-interactive .qb-options { margin: 0.6em 0; display: flow-root; } /* beside a floated image, never under it */")
    t = rep(t, "</head>", PHONE)
    norm = lambda w: [x.replace("\\(N_m\\)=", "\\(N_m\\)").replace("\\(N_f\\)=", "\\(N_f\\)") for x in w if x != "="]
    assert norm(words(t)) == norm(words(src)), "the Full's wording changed"
    return t


# -------------------------------------------------------------- Balanced --

CUTS = [
    ("—a staggering figure.", "."),
    (" Even though the population has grown in size, its genetic health may still be compromised because it was founded by so few individuals.", ""),
    (" This example illustrates how species that evolve in isolated environments can be especially vulnerable to sudden ecological changes caused by human activity.", ""),
    ("<p>This is just a handful of relevant facts that a conservation biologist might want to know when developing a plan to save the cheetahs. Some other important questions are as follows:</p>",
     "<p>Other questions a conservation biologist would want answered before planning to save the cheetah:</p>"),
    ("""<p>Species that are the targets of conservation efforts, such as the cheetah, tend to share several issues or problems. Biological issues relating to conservation ecology include the need to preserve diversity, the problems that arise in small populations, and the impact of competition.</p>

""", ""),
    (" Through an understanding of these biological issues relating to conservation ecology, biologists can better direct their efforts toward saving endangered and threatened species.", ""),
    ("""<p>A real-world analogy of inbreeding can be seen in historical royal families, as well as in fictional examples like <em>Game of Thrones</em>, where repeated intermarriage among close relatives leads to the expression of harmful genetic traits due to reduced genetic diversity.</p>

""", ""),
    (" This creates a skew in reproductive success, meaning that fewer individuals are contributing genes to the next generation.", ""),
    ("""<p>Ideally, ecologists could find ways to promote dispersal of individuals from source populations to sink populations in order to keep those populations from dwindling and eventually disappearing.</p>

""", ""),
    (" Some scientists refer to this as the sixth mass extinction.</li>", "</li>"),
    (" This explains why people spend so much time looking at Internet pictures of cute animals.", ""),
    (" Other threatened species include short-beaked dolphins, leatherback turtles, and forest elephants.", ""),
    (" That is, there will be some individuals who—for whatever reason—never pass on their genes to future generations.", ""),
    ("<p>This example highlights a major issue with small founding populations: low genetic diversity and inbreeding. Because", "<p>Because"),
    (" In a small population, even a minor change in the gene pool can have a large cumulative impact.", ""),
    (" Even if the total headcount seems fairly large, unequal reproductive success can make the population genetically fragile.", ""),
    (" Genetic diversity is a major issue for conservation biologists because when populations dwindle and genetic diversity falls, extinction is more likely.", ""),
]


# ---- Balanced, second pass: condense paragraphs to about 75% of the Full (Ian, 2026-11-20) --------
# Each entry replaces one paragraph or list item, found by its opening words, with a tighter version
# that keeps every fact and number.

def para(t, start, new):
    i = t.find(start)
    assert i >= 0 and t.count(start) == 1, ("condense: opening not found once", start[:70])
    j = min(k for k in (t.find("</p>", i), t.find("</li>", i)) if k > 0)
    return t[:i] + new + t[j:]


CONDENSE = [
    ("<strong>Invasive and introduced species</strong> – Invasive",
     "<strong>Invasive and introduced species</strong> – Invasive (introduced) species are moved by humans, intentionally or not, into regions where they did not previously exist. Often lacking natural predators there, they spread rapidly, outcompete native species, and disrupt food webs and ecosystem structure. Zebra mussels, for example, reached the Great Lakes by accident and now smother native mussels and encrust pipes, docks, and boats."),
    ("A well-known example of an invasive species is the Burmese python",
     "The Burmese python, introduced to the Florida Everglades through the pet trade, now has large wild populations; as an apex predator it has sharply reduced native small mammals and other species."),
    ("The extinction of the dodo is often mistakenly attributed",
     "The dodo was not wiped out for being unintelligent or poorly adapted: it was well suited to an island with no natural predators. Its extinction came mainly from invasive species that humans introduced (rats, pigs, and monkeys), which ate its eggs and competed for resources."),
    ("<strong>Climate change</strong> – Human activities have also contributed",
     "<strong>Climate change</strong> – Human activities have contributed to global warming, a problem for species that cannot shift their home range fast enough. Few extinctions can yet be attributed to it with certainty; the open question is whether species can adapt as quickly as temperatures climb."),
    ("A key issue with modern climate change is not just",
     "The key issue is the speed of the change. For the last ~10,000 years, climate was relatively stable, letting human civilization and many ecosystems develop under predictable conditions. Rising atmospheric carbon dioxide is now rapidly shifting temperature and precipitation, and because evolutionary adaptation usually takes far longer, many species may not adjust in time."),
    ("<strong>A system-level approach</strong> – This approach does not limit",
     "<strong>A system-level approach</strong> – This more recent strategy, adopted by The Nature Conservancy (TNC), tries to save all the species within an ecosystem, for example by preserving entire sections of the Everglades or the Afromontane forests."),
    ("The benefit of this approach is that many species converge",
     "Because many species converge in one place, it saves many at once. But it is hard to \"sell\" to the public, some biodiversity \"hotspots\" are in countries whose governments resist conservation, and its success is harder to gauge than a species-specific approach's."),
    ("Conservationists are facing some tough choices.",
     "Conservationists face tough choices. Dr. Dutton showed a magazine article entitled, \"It's Time to Let Certain Animals Go Extinct,\" arguing that we must decide which species to focus on and which to let die out, an approach called <strong>species triage</strong>. It has been used in Australia and New Zealand but not yet in the United States. Supporters say dropping expensive, losing battles would free money to recover more species; critics note that under triage no one would have attempted the successful rescue of the California condor."),
    ("Global cheetah populations have low genetic diversity.",
     "Global cheetah populations have low genetic diversity. (Researchers found this when skin transplanted between an East African and a South African cheetah was not rejected.) The cause is a bottleneck late in the Pleistocene, when a warmer, drier climate shrank the cheetah's range; numbers recovered, but the lost alleles did not. The result can be inbreeding depression, low sperm counts and motility, low female fertility, poor offspring survival, and less evolutionary potential to cope with environmental change."),
    ("<strong>A species-specific approach</strong> – This approach attempts",
     "<strong>A species-specific approach</strong> – This approach tries to save individual species from extinction, such as the black rhino, the manatee, and the black-footed ferret. The Endangered Species Act (ESA) and the Convention on International Trade in Endangered Species (CITES) embrace it."),
    ("The species-specific approach to conservation is popular among donors",
     "It is popular with donors, who feel connected to charismatic species such as cheetahs or koalas, but many of the species that need the most help, such as insects, are not charismatic, and forests draw few donations either."),
    ("Genetic diversity comes down to <strong>alleles</strong>",
     "Genetic diversity comes down to <strong>alleles</strong>, the alternative versions of a gene. The more a population holds, the better its odds that some individuals can withstand a new disease, climate shift, or altered habitat, and a lost allele returns only through a new mutation or an immigrant. Our food supply shows the danger: roughly 95% of the U.S. apple varieties grown in 1900 no longer exist, and in 1970 a single fungus devastated the U.S. corn crop because most fields were genetically too similar to resist it."),
    ("Moving animals does not always rescue a population.",
     "Moving animals does not always rescue a population. According to a study published in November 2026, a Eurasian lynx population started in northeastern Switzerland in the early 2000s from just 12 animals included three healthy carriers of a harmful recessive allele of the gene FGF23. Drift and inbreeding raised the share of carriers from roughly 10% in the source population to about half, and lynx with two copies die young as minerals build up in their organs."),
    ("A well-known example of genetic rescue involves the Florida panther",
     "A well-known example of genetic rescue is the Florida panther. By the 1990s only about 20–30 remained, and severe inbreeding was causing genetic defects and poor survival. In 1995, conservationists introduced eight female pumas from Texas; the added gene flow reduced inbreeding depression, and the population has rebounded to about 200."),
    ("<strong>Pollution</strong> – As human populations have grown",
     "<strong>Pollution</strong> – Exponential human population growth and fossil fuel use have caused heavy air pollution, which may disrupt nutrient cycles and drive extinctions at very high rates. The pesticide DDT polluted ecosystems and whole food webs and pushed the bald eagle toward extinction; Rachel Carson's book <em>Silent Spring</em> publicized the damage, and the public reaction helped lead to the creation of the U.S. Environmental Protection Agency (EPA). The drugs we take are also excreted and can pollute waterways."),
    ("<strong>Biological diversity financially benefits humans.</strong>",
     "<strong>Biological diversity financially benefits humans.</strong> It has yielded many commercial chemicals, foods, and medicines: 70% of the medicines developed in the last 25 years have come from nature. <strong>Bioprospecting</strong> is the search for organisms that can be commercialized for medical or industrial use; the rosy periwinkle, a threatened plant from Madagascar, produces compounds used to treat leukemia and Hodgkin's lymphoma."),
    ("Many organisms live in habitat patches separated by unsuitable",
     "Many organisms live in habitat patches separated by unsuitable environments, forming subpopulations linked by dispersal; together they make up a <strong>metapopulation</strong>. Southern Africa's 33 remaining cheetah subpopulations are an example: some are close enough for cheetahs to move between them, producing gene flow."),
    ("Another problem facing cheetah populations is the \"supermom\"",
     "Cheetahs also show the \"supermom\" phenomenon, in which a few females produce a disproportionate share of offspring; in the southern Serengeti, a single mother was responsible for 10% of all the cheetahs living there. This shrinks the effective population size below what the total suggests, lowering genetic diversity and raising the risk of inbreeding and drift."),
    ("Removing old-growth forest reduces the ecosystem's ability",
     "Removing old-growth forest reduces carbon storage, weakening the forest's role in regulating climate; disrupts food webs, often causing trophic downgrading as top predators and key species are lost; and weakens watershed regulation. Recovery is slow and dominated by early successional species, not a rapid return to the original community."),
    ("In any given population, not all individuals will breed.",
     "Not every individual breeds. In some species, a few highly territorial males breed with many females while many \"weaker\" males do not breed at all. Sex ratios may also be skewed: there are generally more female deer than male deer because hunters target large males."),
    ("The rate of extinction in recent decades has been",
     "Extinction in recent decades has run as much as 1,000 times the \"natural\" (background) rate seen over Earth's history, so many scientists call the current loss of species the \"sixth mass extinction.\""),
    ("In the 1980s, Colombian drug lord Pablo Escobar",
     "In the 1980s, Colombian drug lord Pablo Escobar illegally imported four hippos to his private zoo at Hacienda Nápoles. After his death in 1993, the other animals were mostly relocated, but the hippos were too hard to move; they escaped into nearby rivers and now number over 100."),
]


def balanced(f):
    t = f
    for a, b in CUTS:
        t = rep(t, a, b)
    for start, new in CONDENSE:
        t = para(t, start, new)
    assert t.count("<img") == f.count("<img")
    assert t.count('class="question-box"') == f.count('class="question-box"')
    assert t.count('class="other-box"') == f.count('class="other-box"')
    assert headings(t) == headings(f) and dates(t) == dates(f)
    for n in re.findall(r"\d[\d,.]*", re.sub(r"<[^>]+>", " ", f[f.index("<body"):])):
        assert n.rstrip(".,") in t, ("number lost", n)
    share = len(words(t)) / len(words(f))
    assert 0.70 <= share <= 0.80, share   # about 75% (Ian, 2026-11-20)
    return t


# --------------------------------------------------------------- Concise --

CONCISE_BODY = r"""
<p class="date">Friday, 11/20/26</p>

<h1>Conservation Biology</h1>

<ul>
  <li><b>Conservation biology</b>: an integrated science drawing on many branches of biology to sustain biodiversity at every level; a "discipline with a deadline" because many species need help urgently.</li>
  <li>It is concerned with <b>species</b>, <b>genetic</b> and <b>ecosystem diversity</b>. Falling genetic diversity makes extinction more likely.</li>
  <li><b>Genetic diversity = alleles.</b> More alleles, better odds that some individuals survive a new disease, climate shift or habitat change. A lost allele returns only through a new mutation or an immigrant.</li>
  <li>Food crops show the risk: about 95% of the U.S. apple varieties grown in 1900 no longer exist, and in 1970 one fungus devastated a genetically uniform U.S. corn crop.</li>
</ul>

<h3>Why Small, Isolated Populations Go Extinct:</h3>
<ul>
  <li><b>Genetic drift</b> (alleles lost by chance) and <b>inbreeding depression</b> (offspring of relatives survive and reproduce poorly)</li>
  <li>A small effective population size</li>
  <li>Chance (stochastic) events such as storms or disease outbreaks, and greater vulnerability to disease</li>
  <li>Too little genetic variation to adapt</li>
</ul>

<h3>Founders and Genetic Rescue:</h3>
<table>
  <thead><tr><th>Case</th><th>What happened</th><th>Lesson</th></tr></thead>
  <tbody>
    <tr><td><b>Florida panther</b></td><td>About 20–30 inbred animals by the 1990s; 8 female Texas pumas added in 1995; now about 200.</td><td>New individuals restore alleles (genetic rescue).</td></tr>
    <tr><td><b>Swiss lynx</b></td><td>Founded in the early 2000s with 12 animals, 3 carrying a harmful recessive FGF23 allele; carriers rose from about 10% to about half. Slovenia and Croatia are adding 18 lynx from the Carpathians instead.</td><td>Small founder groups concentrate harmful alleles; founders should be many and varied.</td></tr>
    <tr><td><b>Escobar's hippos</b></td><td>4 hippos imported in the 1980s, left behind after 1993; now over 100 in Colombia's rivers.</td><td>Large population, low genetic diversity; hippos are also ecosystem engineers that disrupt what they invade.</td></tr>
  </tbody>
</table>

<h2>Major Threats to Biodiversity</h2>

<ul>
  <li>Animal populations have fallen by about half in the last 48 years (one estimate).</li>
  <li>Extinction is running up to 1,000 times the natural (background) rate: the "sixth mass extinction."</li>
</ul>

<table>
  <thead><tr><th>Threat</th><th>Key points and examples</th></tr></thead>
  <tbody>
    <tr><td><b>Habitat destruction</b></td><td>The most important threat. About 40–50% of Earth's land habitats degraded; an acre of rainforest lost every 2 minutes.</td></tr>
    <tr><td><b>Invasive (introduced) species</b></td><td>Moved by humans, often with no predators; outcompete natives and disrupt food webs. Zebra mussels (Great Lakes), Burmese pythons (Everglades); the dodo died out from introduced rats, pigs and monkeys, not from being poorly adapted.</td></tr>
    <tr><td><b>Overexploitation</b></td><td>Overharvesting: tuna overfishing (about 14% of fisheries collapsed); ivory hunting of African elephants.</td></tr>
    <tr><td><b>Pollution</b></td><td>Fossil-fuel air pollution; DDT nearly wiped out the bald eagle (<em>Silent Spring</em> → the EPA); excreted drugs in waterways.</td></tr>
    <tr><td><b>Climate change</b></td><td>The danger is the speed: after about 10,000 stable years, rising CO₂ is changing climate faster than many species can adapt or move. Few extinctions are yet attributed to it with certainty.</td></tr>
  </tbody>
</table>

<h2>Case Study: Cheetahs</h2>

<ul>
  <li>Down more than 90% since 1900; about 7,100 remain, almost all in Africa (a tiny remnant in Iran).</li>
  <li><b>Low genetic diversity</b>: skin grafted between East and South African cheetahs was not rejected. Cause: a late-Pleistocene bottleneck; numbers recovered, alleles did not.</li>
  <li>Consequences: inbreeding depression, low sperm count and motility, low female fertility, poor cub survival, and less evolutionary potential.</li>
  <li><b>"Supermoms"</b>: in the southern Serengeti one mother produced 10% of all cheetahs, so fewer animals pass on genes and the effective population size shrinks.</li>
  <li>Lions and hyenas kill many cubs (up to 95% die); the legal and illegal wildlife trade (cheetahs as pets) adds pressure.</li>
  <li>Basic facts (range, diet, disease, genetics, growth rate, extinction risk) are largely unknown, which makes conservation a "crisis science."</li>
</ul>

<h2>Effective Population Size</h2>

<ul>
  <li><b>Effective population size</b> (\(N_e\)): how many individuals are, in effect, sharing equally in passing on genes. It counts breeders only.</li>
  <li>It falls below the census size when reproduction is uneven (a few dominant males), the sex ratio is skewed (hunters take large male deer), or the population went through a bottleneck.</li>
</ul>

\[
N_e = \frac{4N_mN_f}{N_m + N_f}
\]

<table>
  <thead><tr><th>Breeders</th><th>Calculation</th><th>\(N_e\)</th></tr></thead>
  <tbody>
    <tr><td>5 males, 2 females (of 16)</td><td>4(5)(2) ÷ (5 + 2) = 40 ÷ 7</td><td>5.71</td></tr>
    <tr><td>8 males, 8 females (of 16)</td><td>4(8)(8) ÷ (8 + 8) = 256 ÷ 16</td><td>16 (equals the census)</td></tr>
    <tr><td>1 male, any number of females</td><td>—</td><td>Always below 4</td></tr>
  </tbody>
</table>

<h2>Metapopulations</h2>

<ul>
  <li>A <b>metapopulation</b> is a set of subpopulations in habitat patches linked by dispersal (for example, 33 cheetah subpopulations in southern Africa).</li>
  <li>Each subpopulation is <b>open</b>, so it follows the <b>BIDE</b> model (births, immigration, deaths, emigration), not the closed BD model.</li>
  <li>Colonization depends mainly on distance from a source; extinction mainly on patch size.</li>
</ul>

<table>
  <thead><tr><th>Subpopulation</th><th>Births vs. deaths</th><th>Growth rate</th></tr></thead>
  <tbody>
    <tr><td><b>Source</b></td><td>Births exceed deaths</td><td>Positive</td></tr>
    <tr><td><b>Sink</b></td><td>Deaths exceed births; kept going by immigrants</td><td>Negative</td></tr>
  </tbody>
</table>

<ul>
  <li>With limited money, protect sources first. A sink people created can sometimes be turned back into a source.</li>
  <li>Protecting habitat that can never sustain a population creates an <b>ecological trap</b>: animals keep arriving and dying.</li>
</ul>

<h2>Two Approaches to Conservation</h2>

<table>
  <thead><tr><th>Approach</th><th>Examples</th><th>Strength</th><th>Weakness</th></tr></thead>
  <tbody>
    <tr><td><b>Species-specific</b></td><td>Black rhino, manatee, black-footed ferret; the ESA and CITES</td><td>Donors connect with charismatic species</td><td>Many species most in need are not charismatic</td></tr>
    <tr><td><b>System-level</b></td><td>The Everglades, Afromontane forests; The Nature Conservancy</td><td>Saves many species at once</td><td>Hard to "sell," some hotspots have unreceptive governments, success is hard to measure</td></tr>
  </tbody>
</table>

<h2>The Problem</h2>

<ul>
  <li>Almost half of Earth's land surface is degraded or altered; extinction runs up to 1,000 times the background rate.</li>
  <li>Endangered or threatened: nearly 25% of mammals, 13% of birds, 18% of fish and 42% of amphibians.</li>
  <li><b>Species triage</b>: choosing which species to save and letting others go. Used in Australia and New Zealand, not yet the U.S. Supporters: money goes further. Critics: rescues like the California condor's would never have been tried.</li>
</ul>

<h2>Why Should You Care about Conservation Biology?</h2>

<table>
  <thead><tr><th>Reason</th><th>Key points</th></tr></thead>
  <tbody>
    <tr><td><b>Financial benefit</b></td><td>70% of medicines developed in the last 25 years came from nature. <b>Bioprospecting</b>: searching nature for useful organisms (the rosy periwinkle of Madagascar treats leukemia and Hodgkin's lymphoma).</td></tr>
    <tr><td><b>Ecosystem services</b></td><td>Provisioning (food, water, fiber, medicine), regulating (climate, air and water quality, floods) and cultural (recreation, beauty, study); valued at about $44 trillion a year.</td></tr>
    <tr><td><b>Aesthetics</b></td><td>Biodiversity is beautiful.</td></tr>
  </tbody>
</table>

<h3>Conservation Can Work:</h3>
<ul>
  <li>Florida panthers: fewer than 30 → about 200.</li>
  <li>Bald eagles: 417 nesting pairs in the lower 48 states (1963) → roughly 71,400 (2020).</li>
  <li>California condors: 22 birds (1982) → more than 500.</li>
</ul>

<p class="date">Monday, 11/30/26</p>

<p><em>Exam 3 review in class on Monday.</em></p>

<h2>Glossary</h2>

<table>
  <thead><tr><th>Term</th><th>Definition</th></tr></thead>
  <tbody>
    <tr><td><b>Conservation biology</b></td><td>Integrated science aimed at sustaining biodiversity at every level.</td></tr>
    <tr><td><b>Allele</b></td><td>An alternative version of a gene.</td></tr>
    <tr><td><b>Genetic drift</b></td><td>Chance loss or change of alleles, strongest in small populations.</td></tr>
    <tr><td><b>Inbreeding depression</b></td><td>Poorer survival and reproduction in offspring of related parents.</td></tr>
    <tr><td><b>Genetic rescue</b></td><td>Adding unrelated individuals to restore genetic variation.</td></tr>
    <tr><td><b>Invasive species</b></td><td>A species moved by humans into a region where it did not exist.</td></tr>
    <tr><td><b>Overexploitation</b></td><td>Harvesting a species faster than it can recover.</td></tr>
    <tr><td><b>Bottleneck</b></td><td>A sharp drop in population size that permanently removes alleles.</td></tr>
    <tr><td><b>Effective population size</b></td><td>The number of individuals effectively sharing equally in breeding.</td></tr>
    <tr><td><b>Metapopulation</b></td><td>Subpopulations in separate patches linked by dispersal.</td></tr>
    <tr><td><b>Source / sink population</b></td><td>A subpopulation that grows (births exceed deaths) / shrinks (deaths exceed births).</td></tr>
    <tr><td><b>Ecological trap</b></td><td>Poor habitat that keeps attracting animals that then die there.</td></tr>
    <tr><td><b>Species triage</b></td><td>Deciding which species to save and which to let go.</td></tr>
    <tr><td><b>Bioprospecting</b></td><td>Searching for organisms with medical or industrial uses.</td></tr>
    <tr><td><b>Ecosystem services</b></td><td>Benefits ecosystems provide people: provisioning, regulating and cultural.</td></tr>
  </tbody>
</table>

<h2>Key Takeaways</h2>

<ul>
  <li>Genetic diversity is held in alleles; once lost, only mutation or immigration restores them.</li>
  <li>Small, isolated populations face drift, inbreeding, chance events and disease.</li>
  <li>Adding new individuals can rescue a population (Florida panthers), but small founder groups can concentrate harmful alleles (Swiss lynx).</li>
  <li>Habitat destruction is the most important threat; the others are invasive species, overexploitation, pollution and climate change.</li>
  <li>Cheetahs have very low genetic diversity from a late-Pleistocene bottleneck.</li>
  <li>\(N_e = 4N_mN_f / (N_m + N_f)\); it equals the census size only with equal numbers of breeding males and females.</li>
  <li>Source populations grow, sink populations shrink; protect sources first.</li>
  <li>Species-specific conservation draws donors; system-level conservation saves more species but is harder to sell and measure.</li>
  <li>Extinction is up to 1,000 times the background rate; species triage is one controversial response.</li>
  <li>Biodiversity pays: medicines, ecosystem services (about $44 trillion a year) and beauty; and conservation can work.</li>
</ul>
"""


def concise(f):
    head = f[:f.index("<body>") + len("<body>")]
    head = rep(head, TABLES, TABLES + "      table { display: block; overflow-x: auto !important; max-width: 100%; }\n")
    t = head + "\n" + CONCISE_BODY + "\n</body>\n</html>\n"
    assert headings(t) == headings(f) + [("2", "Glossary"), ("2", "Key Takeaways")], headings(t)
    for h3 in re.findall(r"<h3>(.*?)</h3>", t):
        assert h3.endswith(":"), h3
    assert dates(t) == dates(f) and "Dutton" not in t and "<img" not in t
    for n in ("95%", "1970", "20–30", "1995", "about 200", "12 animals", "10%", "18 lynx", "over 100", "48 years", "1,000 times",
              "40–50%", "2 minutes", "14%", "10,000", "90%", "7,100", "up to 95%", "5.71", "256", "33 cheetah", "25%", "13%",
              "18%", "42%", "70%", "$44 trillion", "417", "71,400", "22 birds", "500"):
        assert n in t, n
    assert abs(4 * 5 * 2 / (5 + 2) - 5.71) < 0.005 and 4 * 8 * 8 / (8 + 8) == 16
    return t


def main(src, out):
    out = pathlib.Path(out)
    out.mkdir(parents=True, exist_ok=True)
    f = full(open(src, encoding="utf-8").read())
    b, c = balanced(f), concise(f)
    for name, html in (("Full", f), ("Balanced", b), ("Concise", c)):
        p = out / f"BSC2011-263-Exam3-Module6-{name}.html"
        p.write_text(html, encoding="utf-8")
        print(f"{p.name}: {len(words(html))} words")


if __name__ == "__main__":
    main(*sys.argv[1:3])
