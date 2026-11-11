"""REE3043 Chapter 17: the Balanced and Concise editions of both versions (regular and charts), 2026-11-09.

Balanced keeps every section, example and box of the Full edition, with long paragraphs cut to their point
(about 80% of the Full's words). Concise is rewritten as tables, short bullets, a glossary and key takeaways;
in its charts version each chart stands in for the table that would carry the same numbers, never beside it.
Every figure in either edition is one the Full prints.

    python scripts/ree3043/chapter17_editions.py SRC.html OUTDIR
"""
import sys, os, re
sys.path.insert(0, os.path.dirname(__file__))
import chapter17 as C

PHONE_TABLES = '<style>@media (max-width:600px){table{display:block;overflow-x:auto !important;-webkit-overflow-scrolling:touch}}</style>'

def rep(t, prefix, new):
    """Replace the whole <p> or <li> text that starts with `prefix` (up to its closing tag or first nested block)."""
    assert t.count(prefix) == 1, (prefix[:60], t.count(prefix))
    i = t.index(prefix)
    if t.rfind("<p", 0, i) > t.rfind("<li", 0, i):
        j = t.index("</p>", i)
    else:
        j = min(x for x in (t.find("</li>", i), t.find("<ul>", i), t.find("<p>", i), t.find("<div", i), t.find("\n\n", i)) if x > 0)
        new = new + ("" if t[j:j + 2] != "\n\n" else "")
    return t[:i] + new + t[j:]

def drop_p(t, prefix):
    assert t.count(prefix) == 1, prefix[:60]
    i = t.index(prefix); s = t.rindex("<p>", 0, i); e = t.index("</p>", i) + 4
    while t[e:e + 1] == "\n": e += 1
    return t[:s] + t[e:]

# ---------------------------------------------------------------- Balanced
CUTS = [
 ("The figures below are year-end 2024 estimates.",
  "The figures below are year-end 2024 estimates; know the relative size of each asset class rather than the exact amounts. The value of investible commercial real estate in the U.S. is about $17.8 trillion, against about $70 trillion in corporate stocks, $48 trillion in owner-occupied housing and $28 trillion in U.S. Treasury securities. The total leaves out real estate owned by governments and by corporations outside the real estate business, such as an office tower a bank owns and occupies, because it is not available for investors to buy."),
 ("Dr. Ling does not expect you to remember these numbers specifically.",
  "Remember the relative importance of each category rather than the numbers: private equity and private debt together far exceed the two public quadrants, private equity is the largest category, and public equity (mostly listed REITs) is relatively small."),
 ("Dr. Ling noted that commercial real estate in the U.S. is financed",
  "U.S. commercial real estate is financed with roughly 38% debt and 62% equity, so the average loan-to-value ratio is about 38%. Many investors, such as pension funds, own properties free and clear of debt, which is why equity makes up the majority of the market's value."),
 ("Pooling equity allows investors to take advantage of economies of scale.",
  "Pooling equity allows investors to take advantage of economies of scale: the per-property cost of acquiring, managing and disposing of many properties is far lower than for one."),
 ("The sponsor or organizer has to be compensated",
  "The sponsor or organizer has to be compensated with fees, a salary, or a disproportionately large share of the cash flows (for example, 20% of the cash flows for 5% of the equity). That lowers the passive investors' return for a given property, but it gives the sponsor an incentive to perform."),
 ("Other considerations include management control issues",
  "Other considerations include management control, access to additional debt or equity, the ability to share risk with other investors (including <em>special allocations</em>, distributions not proportional to equity contributed), and the ability to dispose of an interest. Equity investments in commercial real estate are very illiquid: investors should expect to wait several years for their capital."),
 ("In a general partnership, all partners can make operating decisions",
  "<p>All general partners can make operating decisions (leverage, when to buy and sell), and because they both own and control the business there is no principal-agent conflict.</p>"),
 ("The partnership agreement specifies how the partners' shares",
  "The partnership agreement sets each partner's share of the cash flows, which may be proportional to ownership or may include \"special allocations\" that create multiple classes of investors."),
 ("The most significant disadvantage of a general partnership",
  "The most significant disadvantage is <strong>unlimited liability</strong>: if the partnership cannot pay a debt or a court judgment, creditors can claim the general partners' personal assets. That is why general partnerships are uncommon for pooled real estate equity, and when they are used there are usually only two partners."),
 ("Dr. Ling pointed out that general partners can be entities",
  "The general partner can itself be an entity, such as a corporation or an LLC, which shields that entity's owners from personal liability."),
 ("A partnership agreement (usually written by the general partner)",
  "A partnership agreement, usually written by the general partner, sets out how the partnership is managed and how its cash flows are divided. The general partner usually receives a larger share than its equity alone would suggest, a \"special allocation\" that compensates it for organizing the venture."),
 ("The operating decisions of C corporations are made by managers",
  "Managers who often own little of the firm make the operating decisions, which brings in expertise but also creates agency problems."),
 ("While many large C corporations (like McDonald's and Microsoft)",
  "Many large C corporations own a great deal of real estate, but double taxation makes the form unattractive for pooling equity when other forms offer limited liability without it."),
 ("Federal law prohibits S corporations from having more than 100 shareholders",
  "An S corporation may have no more than 100 shareholders, all of them individuals. Cash flows and taxable income must be distributed <em>pro rata</em>, with one class of stock and no special allocations. These limits, and the popularity of LLCs, mean real estate sponsors rarely use S corporations, though some families that own commercial real estate do."),
 ("While we've discussed these ownership forms separately",
  "In practice, most commercial real estate investments involve several levels of ownership, usually to limit liability. An office building might be owned by an LLC whose two members are <em>another</em> LLC (the sponsor's management team, as managing member) and a pension fund (the non-managing member)."),
 ("While direct investment gives the investors the ability to control the asset",
  "Direct investment gives the investor control but requires it to supply the expertise, either in-house or hired. These investments are highly illiquid, so the required rate of return has to be higher to compensate."),
 ("Direct ownership makes sense as the size of an investor's portfolio increases.",
  "Direct ownership makes more sense as a portfolio grows: a pension fund with billions to invest can afford in-house staff or consultants, and real estate adds diversification to its overall portfolio."),
 ("The use of intermediaries to make indirect equity investments is popular",
  "Intermediaries are popular because they supply expertise, improve liquidity and let investors diversify and share risk; the cost is their management fees and possible conflicts of interest. Investments through intermediaries are usually <strong>securitized investments</strong>, shares in a pool of assets bought in public markets (like the NYSE) or private markets. Public markets offer more liquidity and lower transaction costs."),
 ("Managers are usually paid a front-end fee for acquiring the properties",
  "Managers earn a front-end fee for acquiring properties, a back-end fee on disposition, and a percentage of assets under management (most typically 1.5% a year, usually 1% to 2%); they typically invest none of their own equity. Because the fee grows with assets, managers may hold properties they should sell. Performance fees would align interests better but are not common in open-end funds."),
 ("Open-end funds have a potentially infinite life",
  "Open-end funds have a potentially infinite life, typically hold high-quality properties, and let investors buy in or redeem periodically, such as quarterly. In tough markets, many investors try to redeem at once and a \"redemption queue\" forms."),
 ("The minimum required equity investment in a closed-end private equity fund",
  "The minimum investment is typically $1 million or more. The limited partners usually earn a <em>preferred return</em> (or <em>hurdle rate</em>) before the general partner shares in distributions; above it, the general partner receives a disproportionate share, its <em>carried interest</em> or <em>promote</em>. For example, the limited partners might receive an 8% preferred return and the general partner 20% of cash flows above it. The general partner also earns management, leasing, acquisition and disposition fees."),
 ("The fee structure described above is desirable",
  "This structure aligns the general partner's interests with the limited partners' and shares risk appropriately: the limited partners get some downside protection, and the general partner gets more of the upside when things go well."),
 ("Organizing a closed-end fund gives the sponsor discretionary capital",
  "A closed-end fund gives the sponsor discretionary capital (\"dry powder\"): once investors commit, it can issue binding capital calls and close deals quickly, rather than raising money deal by deal. The trade-off is a longer, more expensive fundraising process. Most funds qualify as private placements under the SEC's Regulation D."),
 ("Pension funds invest in commercial real estate because these are relatively long-term assets",
  "Pension funds invest in commercial real estate because its long-term assets match their long-term liabilities. This applies to <em>defined benefit</em> plans, which promise retirees a set payment; in a <em>defined contribution</em> plan, the employer simply contributes to an account the employee manages. Pension funds buy directly or through open-end and closed-end funds."),
 ("In many cases, a small-scale investment owned by local real estate syndicates",
  "Small-scale investments are often single-asset LLCs organized by local syndicates, with minimum investments as low as $50,000 to $100,000. Sponsors raise the money from friends, business associates and former investors (\"country club money\"), and crowdfunding now offers another way to raise it."),
 ("In terms of the number of units, the majority of commercial properties",
  "By number of properties, most U.S. commercial real estate is owned by \"the great investor masses\": individuals with money to invest who are not high-net-worth investors, pooling their capital in modest local deals. Listed REITs are another option for smaller investors because shares require relatively little capital."),
 ("Approximately $1.5 trillion of commercial real estate in the U.S. is financed by equity capital",
  "About $1.5 trillion of U.S. commercial real estate is financed with the equity of publicly traded real estate companies, chiefly exchange-traded REITs. A <strong>real estate investment trust (REIT)</strong> is a special corporation under the U.S. tax code: shareholders get the limited liability of a C corporation, but the REIT is not taxed at the entity level as long as it keeps meeting requirements such as having at least 100 shareholders and paying out at least 90% of its taxable income as dividends. REITs are the form to use when shares are to trade on a public exchange."),
 ("Private credit debt funds have rapidly expanded",
  "Private credit debt funds have grown quickly as banks pulled back from transitional assets. Their typical loan is a bridge loan (often a three-year term with extensions), non-recourse, floating-rate, at 70% to 80% LTV and a higher cost, used for repositioning, lease-up or heavy capital spending."),
 ("Recall that the development and construction of commercial properties",
  "Development and construction are usually financed with short-term loans, which are risky because the project may not finish on time and on budget (developer execution, materials inflation, permitting). Construction lenders reduce that risk by requiring recourse or a commitment from a long-term lender to pay off the loan once the property is built. They also need the engineering expertise to inspect draws and monitor progress, which is why commercial banks dominate the market; savings institutions, credit agencies and private equity lenders also lend."),
]
DROPS = ["Direct ownership is frequently used for small-scale investments,"]

def balanced(full_normal):
    t = full_normal
    for a, b in CUTS: t = rep(t, a, b)
    for a in DROPS: t = drop_p(t, a)
    return t

# ---------------------------------------------------------------- the charts, placed by keyword so the shorter text can carry them
def place(t, key, end, html, inside=False):
    assert t.count(key) == 1, (key, t.count(key))
    i = t.index(key); j = t.index(end, i)
    if not inside: j += len(end)
    return t[:j] + "\n\n" + html + "\n\n" + t[j:]

def add_charts(t, which):
    # the asset-class chart follows the sentence that introduces it, as in the Full
    t = C.split_after(t, "know the relative size of each asset class rather than the exact amounts.", C.CSS + "\n" + C.asset_classes())
    first = [False]
    def css(h):
        out = (C.CSS + "\n" if first[0] else "") + h; first[0] = False; return out
    for name, key, end, fn, inside in which:
        t = place(t, key, end, css(fn()), inside)
    return C.sub1(t, "</body>", C.RUNTIME + "\n</body>", "runtime")

BALANCED_CHARTS = [
    ("quadrants", "8% in publicly traded mortgage debt</li>", "</ul>", C.quadrants, False),
    ("tree", "do not trade on a stock exchange", "</p>", C.tree, False),
    ("life", "<h4>Life-Cycle of a Closed-End Fund</h4>", "</div>", C.lifecycle, True),
    ("waterfall", "The ordered rules for distributing cash", "</p>", C.waterfall, False),
    ("risk", "<em>Opportunistic funds</em>", "</ul>", C.risk_return, False),
    ("private", "Institutional vs. Noninstitutional Equity Investors</h2>", "</p>", C.private_split, False),
    ("debt", "EXAM TIP: Commercial Debt Structure", "</div>", C.debt_holders, False),
]

# ---------------------------------------------------------------- Concise
QUADRANT_TABLE = '''<table>
    <thead><tr><th>Quadrant</th><th>Share of $17.8T</th><th>Note</th></tr></thead>
    <tbody>
        <tr><td><b>Private equity</b></td><td>54%</td><td>Largest category of CRE ownership</td></tr>
        <tr><td><b>Private debt</b></td><td>30%</td><td>Mortgages held by banks, life insurers, others</td></tr>
        <tr><td><b>Public equity</b></td><td>8%</td><td>Mostly listed REITs; smaller than once predicted</td></tr>
        <tr><td><b>Public debt</b></td><td>8%</td><td>CMBS and REIT unsecured debt</td></tr>
    </tbody>
</table>'''

DEBT_LIST = '''<ul>
    <li><b>Banks and savings associations</b>: about 57% of private and 45% of all CRE debt (plus most construction loans)</li>
    <li><b>Life insurance companies</b>: about 12% of all CRE debt</li>
    <li>Others: GSEs (Fannie Mae, Freddie Mac; multifamily), mortgage REITs, governments, pension funds, debt funds</li>
    <li><b>Public</b>: CMBS (about 15% of all CRE debt; GSE-backed CMBS are all multifamily, private-label CMBS come from large banks) and REIT unsecured bonds (about one-third of public CRE debt)</li>
</ul>'''

def concise_body(with_charts):
    q = "<!--QUADRANTS-->" if with_charts else QUADRANT_TABLE
    life = "<!--LIFE-->" if with_charts else ""
    wf = "<!--WATERFALL-->" if with_charts else ""
    priv = "<!--PRIVATE-->" if with_charts else ""
    tree = "<!--TREE-->" if with_charts else ""
    debt = "<!--DEBT-->" if with_charts else DEBT_LIST
    return f'''<p class="date">Monday, 11/9/26</p>

<h1>Introduction</h1>

<ul>
    <li>U.S. investible commercial real estate (CRE): about <b>$17.8 trillion</b> (year-end 2024), against about $70 trillion in stocks, $48 trillion in owner-occupied housing and $28 trillion in Treasuries.</li>
    <li>Excludes real estate owned by governments and by companies outside the real estate business, which investors cannot buy.</li>
    <li>Know each category's <b>relative</b> size, not the exact numbers.</li>
</ul>

<p><b>The "four quadrants" of CRE value:</b></p>
{q}

<p><b>Leverage:</b> about <b>38% debt, 62% equity</b> (average LTV about 38%); many owners, such as pension funds, hold properties free and clear.</p>

<div class="exam-tip">
    <h4>EXAM TIP: Equity Financing Dominance</h4>
    <p>The majority of commercial real estate value is financed with equity, not debt.</p>
</div>

<h1>Forms of Ownership for Pooled Equity Investments</h1>

<table>
    <thead><tr><th>Advantages of pooling</th><th>Disadvantages of pooling</th></tr></thead>
    <tbody>
        <tr><td>Buy larger properties; diversify; economies of scale; cheaper debt; a sponsor's expertise</td><td>Passive investors cede control to the sponsor, who is paid fees, a salary or a disproportionate share of cash flows (e.g., 5% of equity, 20% of cash flows)</td></tr>
    </tbody>
</table>

<h2>Choosing an Ownership Form</h2>

<p>The two deciding issues: avoiding <b>double taxation</b> and securing <b>limited liability</b>. Others: management control, access to capital, risk sharing (<em>special allocations</em>), and the ability to exit (CRE equity is illiquid).</p>

<table>
    <thead><tr><th>Form</th><th>Taxation</th><th>Liability</th><th>Key points</th></tr></thead>
    <tbody>
        <tr><td><b>General partnership</b></td><td>Pass-through</td><td>Unlimited for all partners</td><td>All partners manage; special allocations allowed; rare, usually two partners</td></tr>
        <tr><td><b>Limited partnership</b></td><td>Pass-through</td><td>GP unlimited (GP may be an entity); LPs limited</td><td>LPs are passive; principal-agent issues; used by PERE funds and large private funds</td></tr>
        <tr><td><b>C corporation</b></td><td>Double taxation</td><td>Limited</td><td>Ownership separate from control; unattractive for CRE investing</td></tr>
        <tr><td><b>S corporation</b></td><td>Pass-through</td><td>Limited</td><td>No more than 100 individual shareholders; pro rata only, one class of stock; used by some families</td></tr>
        <tr><td><b>LLC</b></td><td>Pass-through</td><td>Limited for all members</td><td>Members may manage; managing member files articles and writes the operating agreement</td></tr>
        <tr><td><b>REIT</b></td><td>No entity-level tax if requirements met</td><td>Limited</td><td>At least 100 shareholders; pays out at least 90% of taxable income; for exchange-listed shares</td></tr>
    </tbody>
</table>

<div class="exam-tip">
    <h4>EXAM TIP: Preferred Ownership Form</h4>
    <p>LLCs are the preferred form of ownership for private real estate investors, and they are the largest holders of commercial real estate in the U.S.</p>
</div>

<ul>
    <li>A <strong>joint venture</strong> is not a form of ownership: its parties still choose one, usually an LLC.</li>
    <li>With pass-through entities and special allocations, investor-level cash flows must be estimated beyond the property's.</li>
    <li>Structures are often nested: an office LLC whose members are the sponsor's LLC (managing member) and a pension fund.</li>
</ul>

<h1>Ultimate Equity Investors in Commercial Real Estate</h1>

<ul>
    <li>Investors own CRE <b>directly</b> (control) or through <strong>intermediaries</strong> (expertise, diversification, shared risk, for fees).</li>
    <li>CRE is an <em>alternative</em> asset class; about <b>85% to 90%</b> of CRE equity is held by vehicles that do not trade on an exchange.</li>
</ul>
{tree}

<h2>Direct Investment</h2>

<ul>
    <li>Used mainly by large institutions and high-net-worth investors, often through their own LLC or LP for limited liability.</li>
    <li>Full control, but the investor supplies the expertise; highly illiquid, so required returns are higher.</li>
    <li>Major direct investors: <b>pension funds</b> (under 10% of CRE equity), <b>life insurers</b> (long-term liabilities), foreign investors, banks (mostly foreclosed <em>REO</em> property).</li>
</ul>

<h2>Indirect Investment</h2>

<ul>
    <li><strong>Securitized investments</strong> pool many investors' money, in public or private markets; public markets are more liquid and cheaper to trade.</li>
    <li><strong>Syndication</strong>: pooling equity to buy in the private market, forming a <strong>real estate syndicate</strong> (an LP or LLC).</li>
</ul>

<table>
    <thead><tr><th></th><th>Separate account</th><th>Open-end fund</th><th>Closed-end PERE fund</th></tr></thead>
    <tbody>
        <tr><td><b>Life</b></td><td>Per client</td><td>Potentially infinite</td><td>7 to 10 years (+1 to 2)</td></tr>
        <tr><td><b>Liquidity</b></td><td>That of the property market</td><td>Quarterly buy-ins and redemptions; queues in bad markets</td><td>Very illiquid; no secondary market</td></tr>
        <tr><td><b>Manager's equity</b></td><td>None</td><td>None</td><td>1% to 5%, as GP and LP</td></tr>
        <tr><td><b>Fees</b></td><td>Customized</td><td>Front- and back-end fees; about 1.5% of AUM a year</td><td>Preferred return to LPs, then about 20% carried interest to the GP</td></tr>
        <tr><td><b>Typical use</b></td><td>Customized mandates; no diversification</td><td>Core properties</td><td>Value-added and opportunistic; $1M+ minimum</td></tr>
    </tbody>
</table>

<p><b>Distribution waterfall:</b> (1) 100% to LPs until their capital is returned; (2) 100% to LPs until their IRR reaches the preferred return (commonly 7% to 8%); (3) the rest split, often 80% LPs / 20% GP.</p>
{wf}

<p><b>Closed-end fund life cycle:</b> about a year of fundraising, a 2- to 3-year investment period with <em>capital calls</em> (e.g., 10 days' notice), then harvesting. Committed capital is "dry powder"; most funds qualify as Regulation D private placements.</p>
{life}

<table>
    <thead><tr><th>Strategy</th><th>Risk and return</th><th>Typical properties</th><th>Fund type</th></tr></thead>
    <tbody>
        <tr><td><b>Core</b></td><td>Lowest; about 8% to 9% required</td><td>Stabilized, high-quality, strong leases, large metros</td><td>Open-end</td></tr>
        <tr><td><b>Core-plus</b></td><td>Slightly higher</td><td>Core with added risk (vacancy, weaker tenants)</td><td>&mdash;</td></tr>
        <tr><td><b>Value-added</b></td><td>Intermediate</td><td>Need renovation or re-leasing</td><td>Closed-end</td></tr>
        <tr><td><b>Opportunistic</b></td><td>Highest; 20%+ possible</td><td>Development, distressed situations</td><td>Closed-end</td></tr>
    </tbody>
</table>

<h2>Institutional vs. Noninstitutional Equity Investors</h2>

<ul>
    <li><b>Institutional-quality</b> property: stabilized, low vacancy, in the top 50 to 60 metros, usually $30 million or more.</li>
    <li>Of $9.6 trillion in private CRE equity, <b>29%</b> ($2.8T) is institutional and <b>71%</b> ($6.9T) non-institutional.</li>
    <li><b>Institutional investors</b>: pension funds (defined benefit plans), foreign investors, life insurers, banks (REO), endowments, family offices (patient; fund mezzanine debt and bridge loans).</li>
    <li><b>Non-institutional</b>: high-net-worth investors and "the great investor masses," often through local single-asset LLCs ($50,000 to $100,000 minimums, "country club money," crowdfunding) or listed REITs.</li>
</ul>
{priv}

<h2>Real Estate Investment Trusts</h2>

<p>About <b>$1.5 trillion</b> of CRE is financed with public equity, mainly exchange-traded REITs: limited liability like a C corporation, but no entity-level tax while the REIT keeps meeting its requirements.</p>

<h1>Sources of Commercial Real Estate Debt</h1>

<p>Of about <b>$6.7 trillion</b> in CRE debt, <b>78%</b> is held privately and <b>22%</b> trades publicly (holdings, not originations).</p>

<div class="exam-tip">
    <h4>EXAM TIP: Commercial Debt Structure</h4>
    <p>78% of the debt that finances commercial real estate is privately held. Banks and savings associations are the largest private source.</p>
</div>
{debt}

<p><b>Private debt funds</b> have grown as banks pulled back: bridge loans (often three years plus extensions), non-recourse, floating-rate, 70% to 80% LTV, higher cost, for transitional properties.</p>

<h2>Comparing the Five Primary Sources of Debt</h2>

<table>
    <thead><tr><th>Source</th><th>Recourse</th><th>Rate</th><th>Max LTV</th><th>Term</th><th>Prepayment and rate lock</th></tr></thead>
    <tbody>
        <tr><td><b>CMBS</b></td><td>Nonrecourse</td><td>Fixed</td><td>65% to 70%</td><td>5 or 10 yrs</td><td>Very costly (defeasance, yield maintenance); rate set at closing; poor for transitional property</td></tr>
        <tr><td><b>Life insurers</b></td><td>Nonrecourse</td><td>Fixed</td><td>60% or less</td><td>10+ yrs</td><td>Strict; rate locked at application; slower closing</td></tr>
        <tr><td><b>Agency (GSEs)</b></td><td>Nonrecourse</td><td>Fixed, lower</td><td>About 75%</td><td>&mdash;</td><td>Strict; rate set at closing; multifamily only</td></tr>
        <tr><td><b>Banks, credit unions</b></td><td>Often recourse</td><td>&mdash;</td><td>65% or less</td><td>5 to 7 yrs</td><td>Negotiable, often declining; rate locked at application</td></tr>
        <tr><td><b>Debt funds</b></td><td>Nonrecourse</td><td>Floating</td><td>Highest (transitional)</td><td>Bridge</td><td>Much higher rates and loan costs</td></tr>
    </tbody>
</table>

<h1>Development and Construction Lending</h1>

<ul>
    <li>Short-term and risky: the project may not finish on time and on budget.</li>
    <li>Lenders require <b>recourse</b> or a long-term lender's <b>takeout commitment</b>, and need inspection expertise, so <b>commercial banks dominate</b>.</li>
</ul>

<p class="date">Wednesday, 11/11/26</p>

<p><em>There was no class on Wednesday, November 11th, due to the Veterans Day holiday.</em></p>

<h2>Glossary</h2>

<table>
    <thead><tr><th>Term</th><th>Definition</th></tr></thead>
    <tbody>
        <tr><td><b>Four quadrants</b></td><td>CRE value split into private equity, private debt, public equity and public debt</td></tr>
        <tr><td><b>Double taxation</b></td><td>Profits taxed at the corporation and again as shareholders' dividends</td></tr>
        <tr><td><b>Pass-through taxation</b></td><td>Income and losses flow to the owners' own tax returns</td></tr>
        <tr><td><b>Special allocation</b></td><td>A cash flow share not proportional to the equity contributed</td></tr>
        <tr><td><b>Limited liability company (LLC)</b></td><td>Pass-through entity with limited liability for all members; preferred form for private CRE</td></tr>
        <tr><td><b>Syndication</b></td><td>Pooling equity to buy real estate in the private market</td></tr>
        <tr><td><b>Intermediary</b></td><td>An entity that invests in real estate and sells partial claims to it</td></tr>
        <tr><td><b>Open-end fund</b></td><td>Commingled fund with no fixed end, quarterly buy-ins and redemptions</td></tr>
        <tr><td><b>Closed-end PERE fund</b></td><td>Finite-life private equity real estate fund, usually an LP</td></tr>
        <tr><td><b>Preferred return</b></td><td>The return LPs receive before the GP shares in distributions (the hurdle rate)</td></tr>
        <tr><td><b>Carried interest</b></td><td>The GP's disproportionate share of cash flows above the preferred return (the promote)</td></tr>
        <tr><td><b>Waterfall</b></td><td>The ordered rules for distributing a fund's cash</td></tr>
        <tr><td><b>Capital call</b></td><td>A notice requiring investors to supply committed capital within a short window</td></tr>
        <tr><td><b>Institutional-quality property</b></td><td>Stabilized property in a top 50 to 60 metro, usually $30 million or more</td></tr>
        <tr><td><b>REIT</b></td><td>Tax-advantaged corporation that pays out at least 90% of taxable income</td></tr>
        <tr><td><b>CMBS</b></td><td>Securities backed by a pool of commercial mortgages or a single large loan</td></tr>
    </tbody>
</table>

<h2>Key Takeaways</h2>

<ul>
    <li>U.S. investible CRE is about $17.8 trillion, far smaller than the stock market.</li>
    <li>Private equity is the largest quadrant; the public quadrants are about 8% each.</li>
    <li>CRE is financed with about 38% debt and 62% equity.</li>
    <li>The choice of ownership form turns on double taxation and limited liability.</li>
    <li>LLCs and LPs dominate private CRE; LLCs are the largest holders of U.S. CRE.</li>
    <li>A joint venture is not an ownership form; its parties still choose one.</li>
    <li>About 85% to 90% of CRE equity is held privately.</li>
    <li>Open-end funds: infinite life, quarterly liquidity, AUM fees, core properties.</li>
    <li>Closed-end funds: 7 to 10 years, illiquid, sponsor co-investment, preferred return then carried interest.</li>
    <li>Only 29% of private CRE equity is in institutional-quality property.</li>
    <li>78% of CRE debt is privately held; banks and savings associations hold the most.</li>
    <li>Commercial banks dominate construction lending.</li>
</ul>
'''

def concise(full_normal, with_charts):
    head = full_normal[:full_normal.index("<body>") + len("<body>")]
    head = C.sub1(head, "</head>", "    " + PHONE_TABLES + "\n</head>", "phone tables")
    body = concise_body(with_charts)
    t = head + "\n\n" + body + "\n</body>\n</html>\n"
    if with_charts:
        first = [True]
        def css(h):
            out = (C.CSS + "\n" if first[0] else "") + h; first[0] = False; return out
        for mark, fn in (("<!--QUADRANTS-->", C.quadrants), ("<!--TREE-->", C.tree), ("<!--WATERFALL-->", C.waterfall),
                         ("<!--LIFE-->", C.lifecycle), ("<!--PRIVATE-->", C.private_split), ("<!--DEBT-->", C.debt_holders)):
            t = C.sub1(t, mark, css(fn()), mark)
        t = C.sub1(t, "</body>", C.RUNTIME + "\n</body>", "runtime")
    assert "<!--" not in t.split("<body>")[1].replace("<!-- ", "")
    return t

def words(t):
    b = t.split("<body>")[1]
    b = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", b, flags=re.S); b = re.sub(r'<div class="crev".*?\n</div>', " ", b, flags=re.S)
    return len(re.sub(r"<[^>]+>", " ", b).split())

def build(src, outdir):
    raw = open(src, encoding="utf-8").read(); full = C.normal(raw)
    out = {("Normal", "Balanced"): balanced(full),
           ("Charts", "Balanced"): add_charts(balanced(full), BALANCED_CHARTS),
           ("Normal", "Concise"): concise(full, False),
           ("Charts", "Concise"): concise(full, True)}
    for (ver, ed), t in out.items():
        d = os.path.join(outdir, f"REE3043-Ch17-{ver}"); os.makedirs(d, exist_ok=True)
        p = os.path.join(d, f"REE3043-Fall26-Chapter17-{ed}.html"); open(p, "w", encoding="utf-8").write(t)
        print(f"wrote {ver}/{ed}: {words(t)} words (Full {words(full)}, {100 * words(t) // words(full)}%)")

if __name__ == "__main__":
    build(*sys.argv[1:3])
