"""Concise edition of MAR3023 Exam 3 Chapter 2 Part 1 (2026-11-04): the Full file's
head, the prose rewritten as tables and short lists, formulas and tips kept, the
curves dropped (simple diagrams the text explains), Glossary and Key Takeaways.
    python concise2.py FULL.html OUT.html [--bcg-svg]   (keep the drawn BCG matrix)"""
import sys, re
src, out = sys.argv[1:3]; keep_svg = "--bcg-svg" in sys.argv
t = open(src, encoding="utf-8").read()
head = t[:t.index("<body>") + len("<body>")]
videos = re.findall(r"<details class=\"video-section\">.*?</details>", t, re.S); assert len(videos) == 2
vstyle = re.search(r"<style>\n\.video-section \{.*?</style>", t, re.S).group(0)
bcg_svg = re.search(r'<figure class="sk-fig[^"]*"[^>]*><svg[^>]*aria-label="The BCG matrix.*?</figure>', t, re.S)
figcss = re.search(r"<style>\n  \.sk-fig \{.*?</style>", t, re.S)
BCG_TABLE = '''<table>
  <thead><tr><th></th><th>Low RMS (&lt; 1)</th><th>High RMS (&gt; 1)</th></tr></thead>
  <tbody>
    <tr><td><b>High growth</b> (&gt; 10%)</td><td><b>Question Mark</b> – invest heavily to build share; most new products start here</td><td><b>Star</b> – market leader; keep investing to defend, matures into a cash cow</td></tr>
    <tr><td><b>Low growth</b> (&lt; 10%)</td><td><b>Dog</b> – minimize investment or divest</td><td><b>Cash Cow</b> – "milk" for profit and fund new question marks</td></tr>
  </tbody>
</table>'''
bcg_block = ((figcss.group(0) if figcss else "") + bcg_svg.group(0)) if (keep_svg and bcg_svg) else BCG_TABLE
body = f'''
<p id="intro-note"><i>We have finished the 4 P's and now move on to corporate strategy and marketing planning—material from the start of the text, covered last because it ties everything together.</i></p>

<h1>Organizational Structure</h1>

<p>An <strong>industry</strong> is a group of organizations producing similar products; an <strong>organization</strong> is a legal entity of people working toward a shared mission. A <strong>strategy</strong> is a long-term plan of action that delivers customer value while meeting the organization's goals.</p>

<table>
  <thead><tr><th>Type</th><th>Serves customers to…</th><th>Examples</th></tr></thead>
  <tbody>
    <tr><td><b>For-profit</b></td><td>Earn a profit (revenues − expenses)</td><td>Nike, Target, Spotify</td></tr>
    <tr><td><b>Nonprofit</b></td><td>Advance a cause or community need</td><td>Habitat for Humanity, Teach For America</td></tr>
    <tr><td><b>Government agency</b></td><td>Provide public services</td><td>U.S. Census Bureau</td></tr>
  </tbody>
</table>

<h2>Levels Within Organizations</h2>

<table>
  <thead><tr><th>Level</th><th>Who</th><th>Role</th></tr></thead>
  <tbody>
    <tr><td><b>Corporate</b></td><td>Top management, CEO, CMO</td><td>Sets overall strategy; the CMO develops marketing strategy and sees it carried out</td></tr>
    <tr><td><b>Strategic Business Unit (SBU)</b></td><td>Division or subsidiary managers</td><td>Related products for a defined customer group (P&amp;G, Disney have many; small firms merge this with corporate)</td></tr>
    <tr><td><b>Functional</b></td><td>Marketing, finance, operations specialists</td><td>Turn strategy into action; <b>cross-functional teams</b> share responsibility for a common objective</td></tr>
  </tbody>
</table>

<div class="exam-tip">
    <h4>EXAM TIP: Value Creation</h4>
    <p>Groups of specialists actually create value at the functional level.</p>
</div>

<h1>Strategy in Visionary Organizations</h1>

<p>A visionary organization defines a <b>foundation</b> (why), sets a <b>direction</b> (what), and formulates <b>strategies</b> (how).</p>

<h2>Organizational Foundation (Why)</h2>

<table>
  <thead><tr><th>Element</th><th>Meaning</th></tr></thead>
  <tbody>
    <tr><td><b>Purpose</b></td><td>Why the organization exists and the problems it solves; the base for everything else</td></tr>
    <tr><td><b>Core values</b></td><td>Timeless principles set by founders or top leaders; the "heart and soul," unmoved by short-term pressure</td></tr>
    <tr><td><b>Mission</b></td><td>Scope: customers, markets, offerings; often includes social responsibility</td></tr>
    <tr><td><b>Culture</b></td><td>Shared values, ideas, and attitudes shaping how people interact and decide</td></tr>
  </tbody>
</table>

<h2>Organizational Direction (What)</h2>

<ul>
  <li><em>The business the firm is in</em> – what business, which customers, how value is created.</li>
  <li><em>Specific goals</em> – <strong>Goals</strong> (<strong>objectives</strong>) convert the mission into targeted, often deadlined, performance at corporate, SBU, and functional levels; lower goals feed higher ones. Kinds: profit, sales, market share, quality, customer satisfaction, employee welfare, social responsibility.</li>
</ul>

<h2>Organizational Strategies (How)</h2>

<ul>
  <li><em>By level</em> – strategies get more detailed, operational, and short-term moving down the organization.</li>
  <li><em>By product</em> – strategies differ for a physical good, a service, or an idea.</li>
  <li>A <strong>marketing plan</strong> is the road map for a firm's marketing actions over a set period.</li>
</ul>

<h2>Tracking Strategic Performance</h2>

<p>A <strong>marketing dashboard</strong> is the visual display of the essential information for a marketing objective, now fed real-time data by business-intelligence and AI tools. It displays <strong>marketing metrics</strong>—quantitative measures of a marketing activity or result (sales, percent margin, cost of sales, dollar market share):</p>

<p>\\[
\\text{{Dollar market share}} = \\frac{{\\text{{Company sales (\\$)}}}}{{\\text{{Total industry sales (\\$)}}}}
\\]</p>

<div class="exam-tip">
    <h4>EXAM TIP: Marketing Dashboard</h4>
    <p>A marketing dashboard is a visual display on a computer showing essential information about a marketing objective.</p>
</div>

<h1>Corporate-Level Strategy</h1>

<p>A <strong>corporate mission</strong> defines the markets a firm competes in and the value it delivers: whom it serves and how it adds value, which requires knowing its core competencies.</p>

<table>
  <thead><tr><th>Company</th><th>Mission</th><th>Whom and how</th></tr></thead>
  <tbody>
    <tr><td><b>Google</b></td><td>"Organizing the world's information and making it universally accessible and useful."</td><td>Everyone; the value is ranking information (paid for with your data)</td></tr>
    <tr><td><b>CVS Health</b></td><td>"Helping people on a path to better health."</td><td>Anyone who cares about health; the reason CVS stopped selling tobacco</td></tr>
    <tr><td><b>Boston Beer</b></td><td>"We make the best beer in America."</td><td>Americans who want premium craft beer, not Bud or Miller drinkers</td></tr>
    <tr><td><b>YouTube</b></td><td>"Give everyone a voice and show them the world."</td><td>A global market; the place for video</td></tr>
    <tr><td><b>Lego</b></td><td>"Inspire and develop the builders of tomorrow."</td><td>Learning to visualize and build, not just toys</td></tr>
    <tr><td><b>Tesla</b></td><td>"To accelerate the world's transition to sustainable energy."</td><td>A battery and energy company; cars are one application</td></tr>
  </tbody>
</table>

<p>The Louisville Redbirds found their mission in what fans said they came for—baseball, cheap tickets, autographs, food, fireworks, a picnic area: <b>affordable family entertainment built around baseball</b>. Google (Alphabet) and Facebook (Meta) restructured and renamed so their missions stayed clear as their holdings grew.</p>

<p><strong>Marketing myopia</strong> is defining the firm by its current products instead of the customer need it satisfies:</p>

<table>
  <thead><tr><th>Company</th><th>Saw itself as</th><th>Should have been</th></tr></thead>
  <tbody>
    <tr><td><b>Railroads</b></td><td>Railroads</td><td>Transportation providers (lost to 1930s roads, cars, trucks)</td></tr>
    <tr><td><b>Pickett Slide Rules</b></td><td>Slide rules (80–90% share; flew on Apollo)</td><td>Making complex calculations easier (lost to calculators)</td></tr>
    <tr><td><b>Kodak</b></td><td>Film photography (shelved its own digital camera)</td><td>Photography</td></tr>
  </tbody>
</table>

<p>A mission can also be too broad to guide anything (Microsoft's "Empower every person and organization on the planet to achieve more"). Nike's steers without being myopic or meaningless: inspiration and innovation for every athlete—and if you have a body, you are an athlete.</p>

<h2>Setting Corporate Goals</h2>

<p>A <strong>corporate goal</strong> is a specific, measurable objective (revenue, profit, sales, market share, quality, customer satisfaction): an aspiration and a yardstick. Two goal-setting techniques: <b>portfolio analysis</b> and <b>diversification analysis</b>.</p>

<h2>Portfolio Analysis with the BCG Matrix</h2>

<p><strong>Business (product) portfolio analysis</strong>, from the Boston Consulting Group, analyzes a firm's SBUs as a collection of separate investments. Because every product eventually matures and declines, a lasting firm needs products at different life-cycle stages. The <strong>BCG growth-share matrix</strong> uses 2 dimensions:</p>

<ul>
  <li><b>Market growth rate</b> – high if the market grows 10% or more per year, low if less.</li>
  <li><b>Relative market share (RMS)</b> – the firm's share divided by its largest competitor's share; above 1 the firm is dominant, below 1 it is not.</li>
</ul>

<p>\\[
\\text{{Relative Market Share (RMS)}} = \\frac{{\\text{{Firm's raw market share}}}}{{\\text{{Raw market share of firm's largest competitor}}}}
\\]</p>

<div class="exam-tip">
    <h4>EXAM TIP: Business Portfolio Analysis</h4>
    <p>Business portfolio analysis is used to analyze a firm's SBUs as a collection of separate investments.</p>
</div>

{bcg_block}

<ul>
  <li><b>Success sequence:</b> question mark → star → cash cow. <b>Failure sequence:</b> a product that never leads before growth slows becomes a dog.</li>
  <li>Only one firm per market can hold the dominant star or cash cow position (RMS &gt; 1); most products are question marks or dogs.</li>
</ul>

{videos[0]}

<table>
  <thead><tr><th>Market (growth)</th><th>Raw shares</th><th>RMS</th><th>Position</th></tr></thead>
  <tbody>
    <tr><td><b>Toothpaste</b> (4.6%/yr, low)</td><td>Crest 32.8%, Colgate 22.3%, Arm &amp; Hammer 9.4%, Aquafresh 8.2%</td><td>Crest 32.8 ÷ 22.3 = 1.47; Colgate 22.3 ÷ 32.8 = 0.68</td><td>Crest cash cow; the other three dogs</td></tr>
    <tr><td><b>Toothbrushes</b> (13.1%/yr, high)</td><td>Oral-B 22.3%, Reach 17.6%, Colgate 16.0%, Crest Complete 12.1%</td><td>Oral-B &gt; 1 (largest share)</td><td>Oral-B star; the other three question marks</td></tr>
    <tr><td><b>Apple</b></td><td colspan="3">Vision Pro = question mark; iPhone = star (heading to cash cow); iPad = cash cow; iTunes Store = dog</td></tr>
  </tbody>
</table>

{videos[1]}

{vstyle}

<h2>Diversification Analysis</h2>

<table>
  <thead><tr><th></th><th>Current products</th><th>New products</th></tr></thead>
  <tbody>
    <tr><td><b>Current markets</b></td><td><b>Market penetration</b> – sell more units or raise prices</td><td><b>Product development</b></td></tr>
    <tr><td><b>New markets</b></td><td><b>Market development</b> – new region or country</td><td><b>Diversification</b></td></tr>
  </tbody>
</table>

<h2>Importance of Market Growth Rate</h2>

<p>Growth rate, not size, shows where opportunities are headed. Soft drinks were the largest U.S. beverage category in 2005 yet shrank about 17% over 2001–2011 while bottled water grew about 55%; water is now what most adults drink regularly (63% versus 56%). The roughly $3 billion the beverage market added from 2024 to 2025 came from non-alcoholic drinks, while alcohol slipped and wine stayed flat.</p>

<h2>Importance of Market Share</h2>

<p>Market share is <strong>"the master marketing variable"</strong> for 2 reasons:</p>

<ul>
  <li><b>Market power rises through barriers to entry</b> – a dominant brand directs its channel and sets the prices others follow, and loyalty makes it hard to displace.</li>
  <li><b>Production costs fall along the experience curve</b> – each doubling of cumulative production cuts unit cost by a fixed percentage (10%, say), through economies of scale, learning, and technology. Example: $1 million fixed cost + 1 million units at $1 = $2 per unit; at 2 million units, $3 million ÷ 2 million = $1.50 per unit. A rival selling fewer units sits higher on the curve and must charge more—another barrier to entry.</li>
</ul>

<div class="exam-tip">
    <h4>EXAM TIP: Experience Curve</h4>
    <p>The <b>experience curve</b> suggests that as the total number of units produced increases, the cost to produce an additional unit falls due to economies of scale and increased efficiency.</p>
</div>

<p>U.S. smartphones show both forces: Apple held roughly 60–69% in 2024–25 at premium prices, Samsung slipped from about 18% to 13%, and the rest stayed flat. High share also invites antitrust scrutiny, as in the government's suit accusing Apple of monopolizing the smartphone market.</p>

<h1>Marketing Strategy Formulation</h1>

<p>Long-term success depends less on management tools than on strong strategy, execution, culture, and structure:</p>

<table>
  <thead><tr><th>Trait</th><th>Example</th></tr></thead>
  <tbody>
    <tr><td><b>Clear strategy</b></td><td>Costco: wider selection in the categories shoppers buy in bulk</td></tr>
    <tr><td><b>Operational excellence</b></td><td>Toyota: continuous improvement in quality and speed</td></tr>
    <tr><td><b>Performance-driven culture</b></td><td>Google: innovation and employee engagement</td></tr>
    <tr><td><b>Agile structure</b></td><td>Fast, flexible organizations adapt quickly</td></tr>
  </tbody>
</table>

<h2>Allocating Marketing Resources Using Sales Response Functions</h2>

<ul>
  <li>The <strong>sales response function</strong> relates marketing spending to results such as sales revenue; allocate where <strong>incremental revenue</strong> exceeds <strong>incremental cost</strong> by the widest margin.</li>
  <li>The relationship is an <strong>S-shaped curve</strong>: slow growth at first, rapid gains at moderate spending, flattening returns at high levels.</li>
  <li><strong>Share point analysis</strong>: one <strong>share point</strong> is one percentage point of market share; the revenue, profit, and cannibalization tied to each decide whether more investment is justified.</li>
</ul>

<h2>Strategic Marketing Process</h2>

<p>The <strong>strategic marketing process</strong> allocates marketing mix resources to reach target markets in three steps: <b>planning</b> (goals, strategies, the written marketing plan), <b>implementation</b> (acting on the plan and tracking results), and <b>evaluation/control</b> (comparing results to goals and correcting course). Planning is covered in the rest of this chapter; the other two come in a later chapter.</p>

<h2>Glossary</h2>

<table>
  <thead><tr><th>Term</th><th>Definition</th></tr></thead>
  <tbody>
    <tr><td><b>Strategy</b></td><td>Long-term plan of action delivering customer value while achieving the organization's goals</td></tr>
    <tr><td><b>SBU</b></td><td>Division or subsidiary offering related products to a defined customer group</td></tr>
    <tr><td><b>Cross-functional team</b></td><td>People from different departments sharing responsibility for a common objective</td></tr>
    <tr><td><b>Marketing plan</b></td><td>Road map for a firm's marketing actions over a set period</td></tr>
    <tr><td><b>Marketing dashboard</b></td><td>Visual display of the essential information for a marketing objective</td></tr>
    <tr><td><b>Marketing metrics</b></td><td>Quantitative measures of a marketing activity or result</td></tr>
    <tr><td><b>Corporate mission</b></td><td>Statement of the markets a firm competes in and the value it delivers</td></tr>
    <tr><td><b>Marketing myopia</b></td><td>Defining the firm by current products rather than the customer need it satisfies</td></tr>
    <tr><td><b>Corporate goal</b></td><td>Specific, measurable objective used to assess performance</td></tr>
    <tr><td><b>Business portfolio analysis</b></td><td>Analyzing a firm's SBUs as a collection of separate investments (the BCG matrix)</td></tr>
    <tr><td><b>Relative market share</b></td><td>Firm's share divided by its largest competitor's share</td></tr>
    <tr><td><b>Experience curve</b></td><td>Unit cost falls by a fixed percentage each time cumulative production doubles</td></tr>
    <tr><td><b>Sales response function</b></td><td>How marketing spending affects results such as sales revenue</td></tr>
    <tr><td><b>Share point</b></td><td>One percentage point of market share</td></tr>
  </tbody>
</table>

<h2>Key Takeaways</h2>

<ul>
  <li>Value is created at the functional level; the corporate level sets direction and the SBU level focuses it on markets.</li>
  <li>Foundation (purpose, values, mission, culture) answers why; direction answers what; strategies answer how.</li>
  <li>A mission names whom the firm serves and how it adds value—neither myopic (railroads, Pickett, Kodak) nor meaningless (Microsoft).</li>
  <li>BCG: growth above 10% is high; RMS above 1 is dominant. Question mark → star → cash cow is the success sequence; dogs are divested.</li>
  <li>Only the share leader can be a star or cash cow; everyone else is a question mark or a dog.</li>
  <li>Growth rate, not size, shows where a market is going (soft drinks versus bottled water).</li>
  <li>Market share is the master marketing variable: it builds barriers to entry and lowers unit cost along the experience curve.</li>
  <li>Spend marketing dollars where incremental revenue most exceeds incremental cost; the sales response curve is S-shaped.</li>
</ul>

<p style="text-align: center; font-size: 125%;"><strong>Dr. Cooke will wrap up the material for this chapter in class on Thursday. This page will be updated with that material by the weekend!</strong></p>
</body>
</html>
'''
open(out, "w", encoding="utf-8").write(head + body); print("written", out)
