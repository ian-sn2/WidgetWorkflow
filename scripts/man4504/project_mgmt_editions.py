"""MAN4504 Exam 3, Chapter 3 (Rest of Project Management): Balanced and Concise editions from the finished Full.

    python scripts/man4504/project_mgmt_editions.py FULL.html OUTDIR

Balanced: the Full with repetition trimmed (a table printed three times, lists the tables repeat, side remarks),
every figure kept. Concise: rewritten as tables and bullets, with the two widgets the text cannot do without
(the forward and backward passes: four times per node, worked node by node). Every number is the Full's.
"""
import os, re, sys

sys.path.insert(0, os.path.dirname(__file__))
from project_mgmt import ES, EF, LS, LF, CRIT, PATH_LEN, PERT, T_PRINT, V_PRINT, PER_WEEK, CRASH, XCRIT  # noqa: E402


def rep(t, old, new, n=1):
    assert t.count(old) == n, (old[:90], t.count(old))
    return t.replace(old, new)


def cut_between(t, start, end, new="", keep_end=True):
    a = t.index(start); b = t.index(end, a)
    assert t.count(start) == 1, start[:60]
    return t[:a] + new + t[b if keep_end else b + len(end):]


def words(html):
    body = html[html.index("<body>"):]
    body = re.sub(r"<script.*?</script>|<style>.*?</style>|<svg.*?</svg>", " ", body, flags=re.S)
    return len(re.sub(r"<[^>]+>", " ", body).split())


# ------------------------------------------------------------------ Balanced
def balanced(t):
    t = rep(t, "For example, Dr. Munson mentioned some projects undertaken by Bechtel Corporation, the largest construction and engineering company in the U.S. Bechtel projects range from building a natural gas pipeline in Thailand to constructing 30 high-security data centers worldwide. Most projects mentioned lasted multiple years and cost millions or billions of dollars.",
            "Bechtel Corporation, the largest construction and engineering company in the U.S., runs projects such as a natural gas pipeline in Thailand and 30 high-security data centers, most lasting years and costing millions or billions of dollars.")
    t = rep(t, "Projects are not just building construction. A large proportion are research projects, such as finding a vaccine, sending an unmanned probe to Mars, developing software, or consulting. Dr. Munson emphasized that, regardless of the magnitude of a project, and across different fields and industries, project management uses a universal language and the same underlying calculations.",
            "Many projects are research rather than construction: a vaccine, a Mars probe, software, or consulting. Dr. Munson emphasized that, whatever the size or field, project management uses the same language and the same calculations.")
    t = rep(t, " It is useful to determine whether it is more important to be on time or on budget. Often, there is a tradeoff between <em>time deadlines</em>, <em>cost limitations</em>, and <em>performance scope</em> (sometimes called the project management triangle). The project manager should keep this in mind at the outset.",
            " There is often a tradeoff between <em>time deadlines</em>, <em>cost limitations</em>, and <em>performance scope</em> (the project management triangle), so decide at the outset whether being on time or on budget matters more.")
    t = rep(t, "This basically divides projects into a number of smaller tasks. For example, a project may be broken down into 3 major tasks, which are each divided into several major subtasks, which are each divided into several activities (or \"work packages\"). The key purpose of the work breakdown structure is that it divides the project into smaller tasks, which are easier to estimate the time and cost for.",
            "It divides the project into major tasks, then subtasks, then activities (or \"work packages\"), which are small enough to estimate the time and cost of.")
    t = rep(t, " Project scheduling techniques allow the project manager to plan for all activities, taking into account the order in which they must occur and the amount of time they will require. This allows the manager to estimate the overall project time.",
            " These let the manager plan every activity in order and estimate the overall project time.")
    t = rep(t, " These all help determine whether the project is on track.", "")
    t = rep(t, " At large companies, it is not uncommon for an individual to work with new team members from project to project. At smaller companies, project team members often find themselves working together project after project.", "")
    t = rep(t, "<p>Projects almost always require the specialized expertise of workers from multiple disciplines. (If the work can be contained within a single department, a project organization is probably not necessary.) For example, a project team might include a project manager who oversees a mechanical engineer from the design department, a test engineer from the quality management department, and a technician from the production department.</p>",
            "<p>If the work fits within a single department, a project organization is probably not necessary.</p>")
    t = rep(t, " In many cases, project managers have to pass a test and become certified to take on certain positions.", "")
    t = rep(t, "<p>Project managers are highly visible individuals who have to organize individuals and activities across a variety of disciplines. They also have to be effective coaches and communicators, as they are the link between clients, managers, and workers on the ground.</p>\n", "")
    t = rep(t, " Client satisfaction is the number one metric by which success of a project is measured.", "")
    t = rep(t, "<p>In some fields, project managers often make use of computer programs that assist in project management. Software development tools like Agile Project Management are useful for smaller projects. Some other software packages used for project management in the business world include Primavera, MacProject, MindView, HP Project, Fast Track, and Microsoft Project. Additionally, many companies use proprietary internal software that is directly connected to the firm's own accounting software.</p>",
            "<p>Software such as Microsoft Project, Primavera, and Agile tools (for smaller projects) supports project management, and many firms use internal software tied to their accounting systems.</p>")
    t = rep(t, "<p>Young project managers often make the mistake of not taking enough time for project planning and project scheduling. Additionally, young project managers tend to underestimate activity times, and thus underestimate costs (particularly for very time-dependent costs) for a project, and they tend to overestimate the amount of materials necessary. For the purposes of this class, we will spend most of our time discussing <em>project scheduling</em>.</p>",
            "<p>New project managers tend to spend too little time on planning and scheduling, underestimate activity times (and so costs), and overestimate materials. This class focuses on <em>project scheduling</em>.</p>")
    t = rep(t, " We will discuss each of these project management tools in greater detail, particularly the two main quantitative ones, PERT and CPM.", "")
    t = rep(t, " The prototype can start to be tested in April. As testing occurs, revisions to the product design will occur. Finally, in June, production can begin. Note that the different activities in this Gantt chart have some overlap. That is, we engage in developing the prototype, testing, and revising the product during the time allotted for design. This indicates that these activities occur simultaneously and often are interrelated.",
            " Testing and revision run from April into June, and production begins in June. The bars overlap because prototyping, testing, and revising happen during the design period: these activities run at the same time and depend on each other.")
    t = rep(t, " DuPont developed CPM for its chemical plants in 1957, and Booz, Allen, and Hamilton developed PERT with the U.S. Navy for the Polaris missile project in 1958.",
            " (CPM at DuPont in 1957; PERT for the U.S. Navy's Polaris missile in 1958.)")
    # Step 1 lists the activities the Step 2 table names again; Step 2 lists the relationships the table states
    t = cut_between(t, "<p>We assume that the project has already been defined and broken down into specific activities.",
                    "<h2>Step 2:", "<p>We assume the project has already been broken into the eight activities A through H in the table below.</p>\n\n")
    t = cut_between(t, "<p>Next, we determine which activities must come before other activities.",
                    "<table>", "<p>Next, we determine which activities must come before others:</p>\n\n")
    t = rep(t, "<p>Note that some projects have more than one final node, meaning that there is more than one activity that is not a predecessor for any subsequent activities. It is important to remember that the project's late finish time is equal only to the <em>latest</em> early finish time of all activities in the project.</p>\n\n<p>When doing a backward pass with more than one final node, you move from right to left starting with the late finish time of the project (i.e. the largest early finish time) on each final node. If there is more than one activity that doesn't precede any other activities (i.e., the last activity is different on different paths) it may be helpful to use an \"end\" node (with activity time zero, similar to the \"start\" node); this will allow you to connect all final activities and be sure you're doing the backward pass correctly.</p>",
            "<p>Some projects have more than one final activity. The project's late finish is then the <em>largest</em> early finish of all activities, and the backward pass starts every final activity from that value. Adding an \"End\" node with a duration of zero, like the Start node, connects the final activities and makes this easy to get right.</p>")
    t = rep(t, "<p>An activity is on the critical path if there is no slack time. That is, if there is no slack time associated with an activity, delaying that activity by even a little will delay the entire project.</p>",
            "<p>An activity with no slack is on the critical path: delaying it at all delays the project.</p>")
    t = rep(t, "<p>Given the early start times, early finish times, late start times, and late finish times we calculated, we can determine which activities have slack and which activities are on the critical path. (Note that it is theoretically possible to have more than one critical path if multiple paths have the same cumulative activity times.)</p>",
            "<p>From the four times, we can find each activity's slack. (A project can have more than one critical path if several paths tie for the longest.)</p>")
    t = rep(t, "<p>Now that we have fully developed our network, we can plan, monitor, and control the project to make sure that things get done on time. It is important that we have identified the critical path because any delay in the activities along that path will ultimately delay the entire project.</p>\n\n", "")
    t = rep(t, " These charts could graphically show the earliest and the latest that each activity could begin and finish for the project to get done on time.", "")
    t = rep(t, " The distribution is skewed right because, usually, things can get a lot worse, but they can't get that much better: If everything goes perfectly smooth and we are able to get done early, it will probably not be much earlier than the most likely time, but if something goes terribly wrong, the activity could take a lot longer than the most likely time.",
            " It is skewed right because an activity can run far longer than expected but rarely finishes much earlier.")
    t = rep(t, "<p>You probably have been exposed to a normal distribution in an introductory statistics class. A normal distribution is as follows, and some notable characteristics are below:</p>",
            "<p>A normal distribution has these notable characteristics:</p>")
    t = rep(t, "<p>We are obviously concerned with completion time for critical path activities because any delay in those activities will definitely delay the entire project. However, activities along a non-critical path can delay the entire project as well, if they are delayed long enough. Therefore, variability of times for activities on non-critical paths must be considered when finding the probability of finishing in a specified time. From a project management perspective, we should consider the standard deviation of activities not on the critical path, relative to the amount of slack available.</p>",
            "<p>A non-critical activity can still delay the project if it runs long enough to use up its slack. So when finding the probability of finishing on time, compare the standard deviation of non-critical activities with the slack they have.</p>")
    t = rep(t, "<p>We now have a detailed picture of how the project will be completed, with a detailed schedule of when each activity should begin and end.</p>\n", "")
    t = rep(t, "<p>Project managers may decide to crash a project for reasons other than being behind schedule or moving the deadline forward. It may make financial sense to crash a project so that project managers can eliminate some of the fixed costs of operation. If the manager can reduce the completion time, he or she can also reduce the fixed costs that the project requires. Therefore, even if there is no change in deadline, there is always an incentive to get the job done early.</p>",
            "<p>Crashing can pay even without a deadline change: finishing sooner cuts the project's fixed costs.</p>")
    t = rep(t, "<p>Milwaukee has already computed crash cost per period, using the following equation:</p>\n\n<p>\\[\n\\text{Crash Cost per Time Period} = \\frac{\\text{Crash cost} - \\text{Normal cost}}{\\text{Normal time} - \\text{Crash time}}\n\\]</p>\n\n",
            "<p>The last column uses the crash-cost-per-period formula from step 1.</p>\n\n")
    t = rep(t, "<li>It can be used in a wide variety of projects, from construction to research and development. Even though projects may be different in substance, the language used to manage them and the way success is measured are similar across industries.</li>",
            "<li>They work across a wide variety of projects, from construction to research and development.</li>")
    t = rep(t, " Company culture may sometimes foster an environment in which people think that they have to build in a \"buffer\" of slack time so they can get the job done on time.", "")
    t = rep(t, " An activity with only one day of slack time may not be on the critical path, but failing to ensure that it gets done on time (or underestimating how long it will take to complete) can severely impact the project nonetheless.",
            " An activity with only a day of slack can still delay the project if it is neglected or underestimated.")
    return t


# ------------------------------------------------------------------ Concise
def widget(t, title):
    a = t.index(f'<p class="pm-title">{title}</p>'); a = t.rindex('<div class="pmw', 0, a)
    b = t.index("</script>\n</div>", a) + len("</script>\n</div>")
    return t[a:b]


def table(head, rows):
    h = "".join(f"<th>{c}</th>" for c in head)
    r = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>\n" for row in rows)
    return f"<table>\n<thead><tr>{h}</tr></thead>\n<tbody>\n{r}</tbody>\n</table>"


def concise_body(full):
    acts = ["A", "B", "C", "D", "E", "F", "G", "H"]
    desc = {"A": "Build internal components", "B": "Modify roof and floor", "C": "Construct collection stack",
            "D": "Pour concrete and install frame", "E": "Build high-temperature burner", "F": "Install pollution control system",
            "G": "Install air pollution device", "H": "Inspect and test"}
    pred = {"A": "—", "B": "—", "C": "A", "D": "A, B", "E": "C", "F": "C", "G": "D, E", "H": "F, G"}
    dur = {"A": 2, "B": 3, "C": 2, "D": 4, "E": 4, "F": 3, "G": 5, "H": 2}
    slack = {a: LS[a] - ES[a] for a in acts}
    assert [a for a in acts if slack[a] == 0] == CRIT
    paths = sorted(PATH_LEN.items(), key=lambda kv: -kv[1])
    fwd, bwd = widget(full, "The Forward Pass"), widget(full, "The Backward Pass")
    mu = sum(T_PRINT[a] for a in CRIT); assert mu == 15

    return f"""
<h1>Introduction to Projects</h1>

<ul>
<li><strong>Project</strong>: a series of related tasks aimed at a major output, with a distinct start, a distinct end, and a defined budget. Research (a vaccine, software) counts as well as construction.</li>
<li>Project management has three steps:</li>
</ul>

{table(["Step", "Manager's tasks", "Useful tools"], [
    ["<b>Planning</b>", "Set time, cost, and performance objectives; organize the team; build the <strong>work breakdown structure</strong> (tasks → subtasks → activities, small enough to estimate)", "Time/cost estimates, budgets, engineering diagrams, cash flow charts"],
    ["<b>Scheduling</b>", "Sequence activities; assign people; schedule resources and deliverables", "CPM, PERT, Gantt charts, milestone charts"],
    ["<b>Controlling</b>", "Monitor cost, resources, and quality; revise plans; shift resources", "Budgets, delayed-activity and slack-activity reports"]])}

<ul>
<li><b>Project management triangle</b>: time, cost, and performance scope trade off against each other.</li>
<li><b>Project organization</b> (a temporary, cross-functional team) works best for a specific goal and deadline; unfamiliar, complex, interrelated work; many functions involved; and important but temporary projects.</li>
<li><strong>Project manager</strong>: coordinates and monitors the project; responsible for quality, schedule, budget, and the people on it.</li>
<li>Ethics questions (PMI code): gifts from contractors, false expense or status reports, pressure to cut quality to stay on schedule.</li>
</ul>

<div class="exam-tip">
<h4>EXAM TIP: Client Satisfaction</h4>
<p><b>Client satisfaction</b> is the most important measure of a project's success, ahead of schedule and budget.</p>
</div>

<h1>Project Scheduling Techniques</h1>

<ul>
<li><strong>Gantt chart</strong>: one bar per activity, from its start to its finish; overlapping bars are activities running at the same time.</li>
<li><strong>CPM</strong> (Critical Path Method): activity times are known with fair certainty.</li>
<li><strong>PERT</strong> (Program Evaluation and Review Technique): activity times vary, so it can give the probability of finishing by a date.</li>
<li>Both show where each activity fits, set precedence (what must come first), force realistic time and cost estimates, and expose bottlenecks.</li>
<li>Six steps: define the activities; set precedence; draw the network; estimate times; compute the critical path; use the network to schedule and control.</li>
<li><strong>Activity-on-node (AON)</strong>: nodes are activities. <strong>Activity-on-arrow (AOA)</strong>: arrows are activities, and may need dashed <em>dummy</em> activities.</li>
</ul>

<div class="exam-tip">
<h4>EXAM TIP: Activity-on-Node Method</h4>
<p>The exam uses activity-on-node networks only.</p>
</div>

<h1>CPM Example: Milwaukee Paper Manufacturing</h1>

<p>The EPA gives Milwaukee Paper 16 weeks to install pollution control equipment.</p>

{table(["Activity", "Description", "Immediate predecessors", "Duration (weeks)"], [[a, desc[a], pred[a], dur[a]] for a in acts])}

<h3>The Four Times</h3>

{table(["Time", "Meaning", "Rule"], [
    ["<b>ES</b> (early start)", "Earliest an activity can begin", "= EF of its predecessor; with several, the <b>largest</b> EF"],
    ["<b>EF</b> (early finish)", "Earliest it can end", "= ES + duration"],
    ["<b>LF</b> (late finish)", "Latest it can end without delaying the project", "= LS of its follower; with several, the <b>smallest</b> LS; the last activity's LF = its EF"],
    ["<b>LS</b> (late start)", "Latest it can begin", "= LF − duration"]])}

<p>Each node shows ES top-left, EF top-right, LS bottom-left, and LF bottom-right. The <b>forward pass</b> works left to right for ES and EF:</p>

{fwd}

<p>The <b>backward pass</b> works right to left for LF and LS, always computing LF first:</p>

{bwd}

<h3>Slack and the Critical Path</h3>

<ul>
<li><strong>Slack</strong> = LS − ES = LF − EF: how long an activity can slip without delaying the project.</li>
<li><strong>Critical path</strong>: the longest path, made of the zero-slack activities; its length is the shortest possible project time.</li>
</ul>

{table(["Activity"] + acts, [["ES"] + [ES[a] for a in acts], ["EF"] + [EF[a] for a in acts], ["LS"] + [LS[a] for a in acts],
                             ["LF"] + [LF[a] for a in acts], ["<b>Slack</b>"] + [f"<b>{slack[a]}</b>" for a in acts]])}

{table(["Path", "Weeks"], [[k.replace("→", " → "), f"<b>{v}</b> (critical)" if v == 15 else v] for k, v in paths])}

<ul>
<li>B and D share 1 week of slack on B → D → G → H: <em>either</em> can slip a week, not both.</li>
</ul>

<div class="exam-tip">
<h4>EXAM TIP: CPM Questions</h4>
<p>Expect a diagram or just a table (draw the network yourself), and questions on the project's length (the critical path) or one activity's slack.</p>
</div>

<h1>PERT and Variability in Activity Times</h1>

<ul>
<li>Each activity's time follows a right-skewed <b>beta distribution</b> with three estimates: <strong>optimistic (a)</strong>, <strong>most likely (m)</strong>, <strong>pessimistic (b)</strong>.</li>
<li>The project's completion time follows a <b>normal distribution</b>; activity times are assumed independent.</li>
</ul>

<p style="text-align: center;"><strong>\\( t = \\frac{{a + 4m + b}}{{6}} \\qquad v = \\left(\\frac{{b - a}}{{6}}\\right)^2 \\)</strong></p>
<p style="text-align: center;"><strong>\\( \\mu = \\Sigma\\, t_{{\\text{{critical}}}} \\qquad \\sigma_p^2 = \\Sigma\\, v_{{\\text{{critical}}}} \\qquad z = \\frac{{\\text{{Due date}} - \\mu}}{{\\sigma_p}} \\)</strong></p>

<div class="exam-tip">
<h4>EXAM TIP: Critical Path Calculations</h4>
<p>Add expected times and variances along the <b>critical path only</b>. You cannot add standard deviations: square each to a variance, add, then take the square root.</p>
</div>

<h3>PERT Example</h3>

{table(["Activity", "a", "m", "b", "t", "v"], [[a, *PERT[a], T_PRINT[a], V_PRINT[a]] for a in acts])}

<ul>
<li>Critical path A → C → E → G → H: μ = 2 + 2 + 4 + 5 + 2 = <b>15 weeks</b>; σ² = 0.11 + 0.11 + 1.00 + 1.78 + 0.11 = <b>3.11</b>; σ = √3.11 = <b>1.76 weeks</b>.</li>
<li>By the 16-week deadline: z = (16 − 15) ÷ 1.76 = 0.57 → P = <b>0.71566</b>, a 71.57% chance (Excel: =NORM.S.DIST(0.57, TRUE)).</li>
<li>For a 99% chance: z = 2.33 (P = 0.9901), so x = zσ + μ = (2.33)(1.76) + 15 = <b>19.10 weeks</b>.</li>
<li>Normal rules of thumb: about 68%, 95%, and 99.7% fall within ±1, ±2, and ±3 standard deviations.</li>
<li>Non-critical paths matter too: an activity whose variability is large next to its slack can still delay the project.</li>
</ul>

<h1>Project Crashing</h1>

<ul>
<li><strong>Crashing</strong>: shortening the project by spending more on some activities, because it is behind schedule, the deadline moved up, or finishing early saves fixed costs.</li>
<li>Crash only critical-path activities that can actually be shortened, at the lowest cost.</li>
</ul>

<p style="text-align: center;"><strong>\\( \\text{{Crash cost per period}} = \\frac{{\\text{{Crash cost}} - \\text{{Normal cost}}}}{{\\text{{Normal time}} - \\text{{Crash time}}}} \\)</strong></p>

<ol>
<li>Find each activity's crash cost per period.</li>
<li>Find the critical path(s) with current times.</li>
<li>One critical path: crash its cheapest crashable activity. Several: crash an activity common to all of them, or one on each.</li>
<li>Update the times; stop at the due date, otherwise return to step 2. Crash <b>one period at a time</b>, since the critical path can change.</li>
</ol>

{table(["Activity", "Normal weeks", "Crash weeks", "Crash cost per week", "Critical?"],
       [[a, CRASH[a][0], CRASH[a][1], f"${PER_WEEK[a]:,}", "Yes" if a in CRIT else "No"] for a in acts])}

<ul>
<li>15 → 14 weeks: crash <b>A</b> ($750, the cheapest critical activity). Now two critical paths: A → C → E → G → H and B → D → G → H.</li>
<li>14 → 13 weeks: A is used up. Options: G ($1,500) or H ($3,000), common to both paths; or one on each path: C + D or E + D ($2,000), C + B or E + B ($3,000). Crash <b>G</b>; both paths stay critical at 13 weeks.</li>
</ul>

<h1>Advantages and Disadvantages of PERT and CPM</h1>

{table(["Advantages", "Limitations"], [
    ["Useful for large projects; simple math", "Activities must be clearly defined, independent, and stable"],
    ["Networks anyone can read", "Precedence relationships must be specified and networked"],
    ["Show which activities to watch (critical path)", "Time estimates are subjective and often padded"],
    ["Document who is responsible for what; track schedule and cost", "Too much focus on the critical path can neglect near-critical activities"]])}

<h2>Glossary</h2>

{table(["Term", "Definition"], [
    ["<b>Project</b>", "Related tasks aimed at a major output, with a distinct start, end, and budget"],
    ["<b>Work breakdown structure</b>", "Division of a project into tasks, subtasks, and activities small enough to estimate"],
    ["<b>Gantt chart</b>", "Bars showing when each activity starts and finishes"],
    ["<b>CPM</b>", "Critical Path Method; network scheduling with known activity times"],
    ["<b>PERT</b>", "Program Evaluation and Review Technique; network scheduling with variable activity times"],
    ["<b>Activity-on-node (AON)</b>", "Network in which nodes are activities and arrows are precedence"],
    ["<b>Activity-on-arrow (AOA)</b>", "Network in which arrows are activities; may need dummy activities"],
    ["<b>Forward pass</b>", "Left-to-right calculation of early start and early finish"],
    ["<b>Backward pass</b>", "Right-to-left calculation of late finish and late start"],
    ["<b>Slack</b>", "LS − ES: how long an activity can slip without delaying the project"],
    ["<b>Critical path</b>", "Longest path through the network; zero slack; sets the project's length"],
    ["<b>Crashing</b>", "Shortening a project by spending more on critical activities"]])}

<h2>Key Takeaways</h2>

<ul>
<li>Client satisfaction is the top measure of project success.</li>
<li>Forward pass: ES = largest EF of the predecessors; EF = ES + duration.</li>
<li>Backward pass: LF = smallest LS of the followers; LS = LF − duration.</li>
<li>Slack = LS − ES; zero-slack activities form the critical path, the longest path and the shortest project time (15 weeks in the example).</li>
<li>PERT: t = (a + 4m + b)/6 and v = ((b − a)/6)²; add t and v along the critical path only, never standard deviations.</li>
<li>z = (due date − μ)/σ<sub>p</sub>; 16 weeks gives a 71.57% chance, and 99% needs 19.10 weeks.</li>
<li>Crash the cheapest critical activity one period at a time, and re-check the critical paths after each.</li>
</ul>
"""


def concise(full):
    head = full[:full.index("<body>") + len("<body>")]
    tail = full[full.index("<script>\n(function () {\n  var NS = 'http://www.w3.org/2000/svg', uid = 0;"):]
    return head + "\n" + concise_body(full) + "\n" + tail


if __name__ == "__main__":
    src, out = sys.argv[1:3]; os.makedirs(out, exist_ok=True)
    full = open(src, encoding="utf-8").read()
    b, c = balanced(full), concise(full)
    for name, t in (("Balanced", b), ("Concise", c)):
        p = os.path.join(out, f"MAN4504-263-Exam3-Chapter3-RestofProjectManagement-{name}.html")
        open(p, "w", encoding="utf-8").write(t)
        print(f"wrote {p}: {words(t)} words ({words(t) / words(full):.0%} of Full's {words(full)}), "
              f"{t.count('class=\"pmw')} figures")
