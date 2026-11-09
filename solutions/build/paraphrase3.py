"""ECO2023 Exam 3: every question restated in our own words, and its topic.

Same rules as Exam 1 (Ian, 2026-11-02): nothing is copied from the papers.
The numbers, the count of choices and their order are kept exactly, because
the written solutions refer to them by letter and value. A stem may carry a
short <ol class="sol-sub" type="i"> for the i / ii / iii statement questions.
A short-answer question has None for its choices.

TOPIC is assigned by hand rather than by keyword: Exam 3 spans eight chapters
whose vocabulary overlaps (a monopoly question mentions costs, an externality
question mentions taxes), and a keyword rule misfiles them."""

def SUB(*items):
    return '<ol class="sol-sub" type="i">' + "".join("<li>%s</li>" % i for i in items) + "</ol>"

NONE = "None of these"

_P = {"r": "Price rises", "f": "Price falls", "s": "Price does not change", "?": "The price change is ambiguous"}
_Pp = {"r": "Price rose", "f": "Price fell", "s": "Price did not change", "?": "The price change is ambiguous"}
_Q = {"i": "quantity increases", "d": "quantity decreases", "s": "quantity does not change", "?": "the quantity change is ambiguous"}
_Qp = {"i": "quantity increased", "d": "quantity decreased", "s": "quantity did not change", "?": "the quantity change is ambiguous"}

def pq(*codes, past=False):
    """'ri' -> 'Price rises and quantity increases'; '?' on either side reads as ambiguous."""
    P, Q = (_Pp, _Qp) if past else (_P, _Q)
    out = []
    for c in codes:
        if c == "none": out.append(NONE); continue
        a, b = c[0], c[1]
        out.append(P[a] + ("; " if "?" in (a, b) or b == "s" or a == "s" else " and ") + Q[b])
    return out

FIGS = ["Figure A", "Figure B", "Figure C", "Figure D"]

def GAME(extra_none):
    stem = ("Target and Walmart are each deciding whether to cut their prices. The table "
            "gives each firm's economic profit for every combination of choices (T is "
            "Target's profit, W is Walmart's). Which firm, if either, has a dominant strategy?")
    ch = ["Walmart does; Target does not", "Target does; Walmart does not", "Both firms do", "Neither firm does"]
    return (stem, ch + [NONE] if extra_none else ch)

def SHUTDOWN(five):
    stem = ("Thomas owns a monopoly restaurant, Thomas's Triple Treat, known for hot dogs "
            "topped with chicken ice cream and caramel sauce. His price is below both his "
            "average total cost and his average variable cost. What should he do?")
    ch = ["Shut down at once, because price is below average total cost",
          "Stay open as long as price is below average total cost",
          "Shut down at once, because price is below average variable cost"]
    if five:
        ch += ["Stay open, because he is earning an economic profit",
               "Stay open as long as price is below average variable cost"]
    else:
        ch += ["Stay open as long as price is below average variable cost"]
    return (stem, ch)

TARIFF = ("Which groups does a tariff harm?" + SUB("Domestic producers", "Domestic consumers", "The domestic government"),
          ["i alone", "ii alone", "iii alone", "i and iii", "i, ii and iii"])
VARIETY = ("Which market structure gives consumers the benefit of product variety?",
           ["Perfect competition", "Oligopoly", "Monopoly", "Monopolistic competition"])
CHEAT = ("How does an oligopolist cheat on a price-fixing agreement?",
         ["It charges less and produces less than agreed", "It charges more and produces more than agreed",
          "It charges more and produces less than agreed", "It charges less and produces more than agreed"])
CARS = ("New cars are a normal good, and people's incomes fall. What happens to the equilibrium price and quantity of new cars?",
        pq("ri", "rd", "fd", "fi") + ["Price does not change and quantity increases"])

P = {}

# --------------------------------------------------------- Summer 2021 ----
P["212"] = {
 1: ("Once restaurants were allowed to reopen, many of their workers feared catching COVID-19 from diners. Because of that fear:"
     '<ol class="sol-sub" type="a"><li>Does the demand curve for restaurant workers move right, move left, or stay put?</li>'
     "<li>Does the supply curve of restaurant workers move right, move left, or stay put?</li>"
     "<li>What happens to the equilibrium wage and to the number of restaurant workers employed?</li></ol>", None),
 2: ("Knight's dog-vacuuming service is a firm in monopolistic competition that cleans 50 dogs each week. It charges $40, its marginal cost is $45, and its average total cost is $45. Which describes the firm?",
     ["It may be maximizing profit, and it is taking an economic loss", "It is certainly not maximizing profit, yet it earns an economic profit",
      "It is certainly maximizing profit, and it earns a normal profit", "It is certainly not maximizing profit, and it earns a normal profit", NONE]),
 3: ("Which statements hold for a monopoly in the long run?" + SUB("It may earn an economic profit.", "Its price equals its marginal revenue.", "It always produces the output that minimizes its average total cost."),
     ["i alone", "ii alone", "iii alone", "ii and iii only", NONE]),
 4: ("The firms in an oligopoly have formed a cartel. When is the industry's total profit lowest?",
     ["When every firm keeps to the agreement", "When one firm breaks the agreement and the rest keep to it",
      "When every firm breaks the agreement", "When the firms act together as a single monopoly"]),
 5: ("Regulators require a natural monopoly to charge a price equal to its average total cost. The firm then",
     ["takes an economic loss", "earns a normal profit, but total surplus is not maximized", "earns an economic profit",
      "maximizes total surplus, but earns less than a normal profit", "earns a normal profit and maximizes total surplus"]),
 6: ("A good's marginal external cost is equal to its",
     ["marginal social cost less its marginal social benefit", "marginal social benefit less its marginal social cost",
      "marginal social benefit less its marginal external benefit", "marginal private cost less its marginal private benefit", NONE]),
 7: ("What does the Clayton Act of 1914 outlaw?",
     ["Price discrimination where it substantially reduces competition or tends to create a monopoly",
      "Unfair methods of competition and deceptive business practices",
      "Combinations, trusts or conspiracies that restrain trade between states or with other countries",
      "Price fixing", "Any practice that lets a monopoly profit at another firm's expense"]),
 8: ("Tomato sauce, an input into pizza, becomes more expensive. What happens to the price and quantity of pizza?", pq("ri", "rd", "fi", "fd")),
 9: ("Compared with a perfectly competitive market that has the same costs, how much does a single-price monopoly produce, and what does it charge?",
     ["More output at a higher price", "More output at a lower price", "Less output at a lower price", "Less output at a higher price"]),
 10: ("An unregulated competitive market produces a good that creates an external benefit. Why is the outcome inefficient?",
      ["People consume too much of the good", "People consume too little of the good", "The market price is too high", "The good costs too much to produce"]),
 11: GAME(True),
 12: ("How price elastic is the demand for one particular luxury car model, such as the Cadillac Escalade, likely to be?",
      ["Elastic, though not perfectly elastic", "Inelastic, though not perfectly inelastic", "Zero", "Infinite"]),
 13: ("Computerization raises the demand for workers with a lot of human capital and lowers the demand for workers with little. Its effect on the distribution of income is to",
      ["make it more equal", "leave it unchanged", "make it less equal", "change it in a direction that cannot be determined"]),
 14: ("Zucchini turns out to help prevent tooth decay, and at the same time zucchini pickers win a higher wage. What happens to the price and quantity of zucchini?",
      pq("ri", "rd", "f?", "r?", "?d")),
 15: ("When the wage rate goes up, which way do the income effect and the substitution effect push the number of hours people choose to work?",
      ["Income effect toward more hours; substitution effect toward fewer", "Both toward more hours",
       "Both toward fewer hours", "Income effect toward fewer hours; substitution effect toward more"]),
 16: ("A perfectly competitive market starts in long-run equilibrium, and then demand for its product rises for good. Compared with before, the new long-run equilibrium has",
      ["fewer firms", "more firms", "the same number of firms", "a different number of firms, but whether more or fewer cannot be determined"]),
 17: CARS,
 18: TARIFF,
 19: ("What does public choice theory predict?",
      ["Unregulated competitive markets produce more than the allocatively efficient quantity", "Common resources will be used too little",
       "Natural monopolies need no regulation", "Government may supply more public goods than the allocatively efficient quantity", NONE]),
 20: ("Which of these products is most likely to create an external benefit?",
      ["A slice of pizza", "A diamond ring", "A COVID-19 vaccination", "A web page", "A magazine"]),
 21: VARIETY,
 22: ("Every firm in a perfectly competitive market is taking an economic loss. If some of the firms leave the market, then",
      ["the market supply curve shifts right", "the product's price falls", "the remaining firms' losses shrink", "the remaining firms' losses grow", NONE]),
 23: SHUTDOWN(True),
 24: ("Pizza and soda are complements, and the price of soda falls. What happens to the price and quantity of pizza slices?", pq("ri", "rd", "fd", "fi", "none")),
 25: ("What lets which kind of firm earn an economic profit in the long run?",
      ["Differentiated products, for a firm in monopolistic competition", "Barriers to entry, for a firm in monopolistic competition",
       "A downward-sloping marginal revenue curve, for a monopoly", "A downward-sloping demand curve, for a monopoly", "Barriers to entry, for a monopoly"]),
 26: ("A profit-maximizing firm keeps raising its output as long as its",
      ["price is above its average total cost", "average total revenue is above its average variable cost",
       "marginal cost is above its marginal revenue", "marginal revenue is above its marginal cost",
       "None of these, since no general rule says when a firm keeps expanding"]),
 27: ("Fewer Mexican restaurants are open for business. What happens to the price and quantity of Mexican food?",
      ["Price rises and quantity increases", "Both the price change and the quantity change are ambiguous",
       "Price rises and quantity decreases", "Price falls and quantity increases", "Price falls and quantity decreases"]),
 28: ("The price of salt drops 15 percent, and the quantity of salt demanded rises 5 percent. What is the price elasticity of demand for salt?",
      ["0.33", "3.0", "0.75", "75.0"]),
 29: ("Which kind of good is rival but not excludable?", ["A public good", "A natural monopoly", "A private good", "A common resource"]),
 30: GAME(False),
}

# --------------------------------------------------------- Spring 2021 ----
P["211"] = {
 1: ("Last fall a fire destroyed the country's largest chlorine plant, which made about 10% of the national supply. What happened to the price and quantity of chlorine?",
     pq("ri", "rd", "fi", "fd", past=True) + ["Price did not change and quantity increased"]),
 2: ("Can a monopoly earn an economic profit in the short run? Can it in the long run?",
     ["Yes in the short run, and yes in the long run", "Yes in the short run, but not in the long run",
      "Not in the short run, but yes in the long run", "In neither the short run nor the long run"]),
 3: GAME(True),
 4: ("A country's Lorenz curve moves further away from the line of equality. Which of these must be true of the country's income?"
     + SUB("It has fallen.", "It has risen.", "It is shared less equally.", "It is shared more equally."),
     ["ii alone", "iii alone", "i and iii", "ii and iv", NONE]),
 5: ("Demand for a firm's product rises, so its price and its marginal revenue both go up. What happens to the firm's demand for labor?",
     ["It decreases", "It increases", "It does not change", "It cannot be determined without more information"]),
 6: ("The table gives the demand schedule for ribs at Billy Bob's BBQ. Between $11 and $9 a pound, the demand for these ribs is",
     ["perfectly elastic", "elastic", "unit elastic", "inelastic"]),
 7: ("Producing lumber pollutes the air and the water. Left unregulated, the lumber market would",
     ["produce more lumber than is efficient", "produce less lumber than is efficient",
      "sometimes produce more and sometimes less than is efficient", "create an external benefit from producing lumber"]),
 8: ("How has the distribution of income in the United States changed from 1979 to today?",
     ["It has become more equal", "It has become less equal", "It first grew more equal and then less equal",
      "None of these, because 1979 and today cannot be compared"]),
 9: ("Where does the supply curve of high-skilled labor lie compared with that of low-skilled labor, and why?",
     ["To the right, because more people want high-skilled jobs", "To the left, because more people want high-skilled jobs",
      "To the left, because skills are costly to acquire", "To the right, because fewer high-skilled workers will accept a low wage"]),
 10: ("The price elasticity of demand for gasoline is 0.2. If the quantity of gasoline falls by 2 percent, by how much does the price of a gallon rise?",
      ["10 percent", "4 percent", "2 percent", "1 percent", NONE]),
 11: ("The metal that trumpets are made from gets cheaper, while more people take up the trumpet. The change in supply is larger than the change in demand. What happens to the price and quantity of trumpets?",
      pq("ri", "f?", "fi", "?i", "none")),
 12: ("More drivers scrap their gasoline cars and buy battery-powered ones. What happens to the price and quantity of gasoline?",
      pq("ri", "rd", "fd", "fi") + ["Price does not change and quantity decreases"]),
 13: ("Where voters are rationally ignorant, public choice theory predicts that government supplies public goods in",
      ["more than the efficient quantity", "exactly the efficient quantity", "less than the efficient quantity", "a quantity that bureaucrats do not affect"]),
 14: ("A common resource is used efficiently when it is used so that",
      ["its use is as large as possible", "marginal social benefit equals marginal social cost",
       "marginal private benefit equals marginal cost", "marginal social benefit is as large as possible", NONE]),
 15: ("Bob's Lawn Care Services, a perfectly competitive firm, mows 22 lawns each week. Its marginal cost is above the price it charges and climbs with each extra lawn. How can Bob raise his profit?",
      ["Charge a higher price", "Charge a lower price", "Mow fewer than 22 lawns a week", "Mow more than 22 lawns a week"]),
 16: ("Which statements hold for a firm in monopolistic competition in the long run?"
      + SUB("It can earn an economic profit.", "It can earn a normal profit.", "Its price equals its marginal cost."),
      ["i, ii and iii", "i and ii only", "ii and iii only", "i and iii only", NONE]),
 17: ("The sales tax on shirts goes up. What happens to the price buyers pay for a shirt and to the price sellers receive and keep?",
      ["Buyers pay more; sellers keep more", "Buyers pay more; sellers keep less", "Buyers pay less; sellers keep less",
       "Buyers pay more; what sellers keep is ambiguous", "What buyers pay is ambiguous; sellers keep less"]),
 18: ("Knight's medicinal wheat company, a firm in monopolistic competition, grows 40 bushels. Its marginal cost is $45, its price is $55, and its average total cost is $40. The company",
      ["is certainly maximizing profit, and it earns an economic profit", "is certainly not maximizing profit, yet it earns an economic profit",
       "may be maximizing profit, and it earns a normal profit", "is certainly not maximizing profit, and it takes an economic loss", NONE]),
 19: CHEAT,
 20: ("Which describes the labor supply curve?",
      ["It always slopes upward", "It slopes downward only where the income effect outweighs the substitution effect",
       "It slopes upward only where the income effect outweighs the substitution effect", "It always slopes downward"]),
 21: ("What best explains why externalities exist?",
      ["Marginal social cost cannot be estimated", "Marginal social benefit cannot be estimated",
       "Property rights are missing", "Marketable permits exist"]),
 22: ("A natural monopoly is regulated with a marginal-cost pricing rule. Which statement about that rule is FALSE?",
      ["It maximizes total surplus in the industry", "The firm produces the efficient quantity",
       "The firm's price equals its marginal cost", "The firm earns a normal profit"]),
 23: ("A rent ceiling below the equilibrium rent has what effect on producer surplus?",
      ["It raises it", "It lowers it", "It leaves it unchanged", "It could raise or lower it"]),
 24: ("People learn that eating more fish is good for their health. What happens to the price and quantity of fish?", pq("rd", "ri", "fd", "fi")),
 25: ("The four figures show the market for beef. Chicken and beef are substitutes, and chicken gets cheaper. Which figure shows the effect on the beef market?", FIGS),
 26: ("Three large companies sell cell phone service in the United States, and when one changes its prices the others' profits change too. Which best describes this industry?",
      ["Perfect competition", "Monopolistic competition", "Oligopoly", "Monopoly", "A shared monopoly"]),
 27: ("A point on the production possibilities frontier means that",
      ["resources are being used inefficiently", "society cannot produce that combination with its present resources and technology",
       "the nation is production efficient", "both goods have increasing costs"]),
 28: GAME(False),
 29: SHUTDOWN(False),
}

# ----------------------------------------------------------- Fall 2020 ----
P["203"] = {
 1: ("The pandemic raised the demand for face masks. If the supply of masks is elastic, though not perfectly elastic, what happened to the equilibrium price and quantity of masks?",
     pq("ri", "rd", "fd", "fi", past=True) + [NONE]),
 2: ("At a market's equilibrium, marginal external cost is equal to",
     ["marginal private benefit less marginal private cost", "marginal external benefit",
      "marginal social cost less marginal private cost", "marginal social cost plus marginal private cost", NONE]),
 3: ("The four figures show the market for pizza. During the pandemic, more people want to eat pizza. Which figure shows the change?", FIGS),
 4: ("Perfectly competitive firms earn zero economic profit in the long run. Which assumption mainly explains that?",
     ["There are few buyers and sellers", "There are no barriers to entry", "Firms are price takers", "Each firm's supply curve slopes upward"]),
 5: ("A tax is placed on sales of a good. If neither supply nor demand is perfectly elastic or perfectly inelastic, the price buyers pay",
     ["falls", "does not change", "rises by the full amount of the tax", "rises by less than the tax", "rises by more than the tax"]),
 6: ("Consumers treat beef and pork as substitutes. A drought hits the regions where cattle graze. Allowing for what the drought does to the price of beef, what happens in the pork market?",
     ["Pork supply shifts right", "Pork supply shifts left", "Pork demand shifts right", "Pork demand shifts left"]),
 7: ("A public good is one that can be consumed",
     ["by one person only, without paying", "by one person only, who has to pay",
      "by many people at once, as long as each one pays", "by many people at once, whether or not they pay"]),
 8: ("When new firms join a monopolistically competitive industry, what happens to each firm already in it?",
     ["Its demand curve shifts right", "Its demand curve shifts left", "Its marginal cost curve shifts right", "Its marginal cost curve shifts left"]),
 9: ("What does the capture theory of regulation assume?",
     ["Regulation maximizes consumer surplus", "Regulation sets price equal to average total revenue",
      "Regulators aim to minimize deadweight loss", "Regulation serves the interests of the regulated firms and their managers"]),
 10: ("Flour, which bagels are baked from, becomes more expensive. What happens to the equilibrium price and quantity of bagels?", pq("ri", "rd", "fi", "fd")),
 11: GAME(False),
 12: ("A 10 percent rise in the price of pizza cuts the quantity sold by 15 percent. What is the price elasticity of demand for pizza?",
      ["1.50", "0.67", "150", "5.0", NONE]),
 13: ("Pork is sold in a perfectly competitive market, and hog farmers are earning a normal profit. Market demand for pork then rises. An individual hog farmer",
      ["produces more and takes an economic loss", "produces more and earns an economic profit", "produces the same amount and earns an economic profit",
       "produces less and earns an economic profit", "produces less and takes an economic loss"]),
 14: ("A natural monopoly regulated under a marginal-cost pricing rule will",
      ["take an economic loss", "earn an economic profit", "earn zero economic profit, which is a normal profit",
       "leave a deadweight loss, with its profit or loss uncertain"]),
 15: ("Consuming a good creates an external benefit. An unregulated market for it fails because",
      ["too much of the good is produced", "too little of the good is produced", "the good's price is too high", "the good costs too much to produce"]),
 16: ("The six firms in an industry know that their production pollutes. Their top executives agree that each firm will raise its price by 3% and spend the extra revenue on pollution control. This agreement is",
      ["always legal", "legal only because the increase is below 5%", "legal only because the extra revenue pays for pollution control", "always illegal", NONE]),
 17: ("Thomas's Magical Mystical Medicinal Wheat, a monopoly, grows 40 bushels a year. Its marginal cost, its price and its average total cost are all $40. Thomas",
      ["is maximizing profit, and earns a normal profit", "is not maximizing profit, and earns an economic profit",
       "may be maximizing profit, and earns a normal profit", "is not maximizing profit, and earns a normal profit", NONE]),
 18: ("In which market structures can a firm earn an economic profit in the short run?" + SUB("Perfect competition", "Monopolistic competition", "Monopoly"),
      ["i alone", "ii alone", "iii alone", "i and ii", "i, ii and iii"]),
 19: ("The nearer a Lorenz curve lies to the 45-degree line of equality, the",
      ["larger the nation's income", "smaller the nation's income", "more equally the nation's income is shared", "less equally the nation's income is shared"]),
 20: ("For a tax to remove the deadweight loss that pollution causes, it must equal the",
      ["marginal private cost", "marginal external cost", "marginal social cost", "marginal private benefit", "marginal social benefit"]),
 21: ("A new fertilizer lets farmers grow more oats, while incomes fall and oats are a normal good. Supply and demand shift by the same amount. What happens to the equilibrium price and quantity of oats?",
      pq("si", "rd", "fs", "?d", "f?")),
 22: ("More farmers start growing tomatoes. What happens to the price and quantity of tomatoes?", pq("ri", "rd", "fi", "fd")),
 23: ("Which is the best example of a natural monopoly?",
      ["The Pittsburgh Penguins, a National Hockey League team", "General Motors, the large carmaker",
       "Florida Power and Light, an electric utility in Florida", "Sony, the Japanese maker of the PlayStation"]),
 24: ("A firm in monopolistic competition can sell 10 units at $21 each, but to sell 11 it must cut its price to $20. What is the marginal revenue from the 11th unit?",
      ["$21", "$20", "$10", "$1", NONE]),
 25: ("Which statement about the production possibilities frontier is true?",
      ["Points outside the frontier cannot be attained", "Points inside the frontier cannot be attained",
       "Points on the frontier are less efficient than points inside it", "None of these, because all three are false"]),
 26: ("I buy fireworks and set them off at home on the Fourth of July, and my neighbors watch from their own yards. The display is",
      ["a private good, since I paid for the fireworks", "a common resource, since too many are set off",
       "a public good, since my neighbors watched it too", "a common resource or a public good, depending on whether too many are set off"]),
 27: ("Bicycles are built from steel, and a tariff pushes up the price of steel. What happens to the equilibrium price and quantity of bicycles?",
      pq("fd", "ri", "rs", "sd", "rd")),
 28: ("A single-price monopoly faces a downward-sloping demand curve and produces where MR = MC. Is there a deadweight loss?",
      ["Yes, there is", "No, there is not", "There might be"]),
 29: GAME(False),
}

# --------------------------------------------------------- Spring 2020 ----
P["201"] = {
 1: ("Fewer firms make tomato sauce. What happens to the equilibrium price and quantity of tomato sauce?", pq("ri", "rd", "fd", "fi")),
 2: ("Firms in a perfectly competitive market are earning economic profits. Which of these happen as time goes on?"
     + SUB("New firms enter the market.", "The market price falls.", "Existing firms' economic profits shrink."),
     ["i, ii and iii", "i and ii only", "ii and iii only", "i only", "i and iii only"]),
 3: ("The four figures show the market for pizza. Hamburgers and hot dogs, both substitutes for pizza, become more expensive. Which figure shows the effect?", FIGS),
 4: ("A movie ticket's price goes up 6 percent and the quantity of movies demanded drops 9 percent, other things the same. What is the price elasticity of demand?",
     ["6.0", "9.0", "0.67", "1.5", NONE]),
 5: TARIFF,
 6: ("New cars are a normal good, and layoffs caused by COVID-19 cut people's incomes. What happens to the equilibrium price and quantity of new cars?", CARS[1]),
 7: ("Which of these is an example of an external cost?",
     ["Bad weather shrinks the wheat harvest", "Higher demand for cheese pushes up the price pizza buyers pay, leaving them worse off",
      "Smoking damages the smoker's own health", "Smoking damages the health of non-smokers nearby"]),
 8: ("In the United States, taxes and income redistribution programs",
     ["generally move income from the poor to the rich", "have no overall effect on the distribution of income",
      "generally move income from the rich to the poor", "are small next to programs that provide goods and services below cost"]),
 9: VARIETY,
 10: ("The technology for making solar cells improves. What happens to the price and quantity of solar cells?", pq("ri", "rd", "fi", "fd")),
 11: GAME(False),
 12: ("Salsa and chips are complements, and salsa gets cheaper. What happens to the equilibrium price and quantity of chips?",
      pq("ri", "rd", "fd", "fi") + ["Price does not change and quantity increases"]),
 13: ("A sales tax is placed on purses. The share of the tax that sellers bear grows when",
      ["purses are a normal good", "purses are an inferior good", "the supply of purses becomes more elastic",
       "the demand for purses becomes more elastic", "purses are a complement to shoes"]),
 14: ("Under the Coase theorem, private bargaining reaches an efficient outcome",
      ["only if the property right goes to whoever bears the external cost", "only if the property right goes to whoever creates the external cost",
       "whether the property right goes to whoever creates the external cost or to whoever bears it",
       "only if property rights are removed wherever an external cost or benefit arises"]),
 15: ("What is the opportunity cost of leisure, the time someone spends not working?",
      ["The substitution effect", "The income effect", "The person's wealth", "The person's wage rate", NONE]),
 16: ("Tomato pickers win a higher wage. What happens to the price and quantity of tomatoes?",
      ["Price rises and quantity increases", "Price rises and quantity decreases",
       "Price falls; quantity probably changes, but in an ambiguous direction",
       "Price rises; quantity probably changes, but in an ambiguous direction", NONE]),
 17: ("Jane's Garage Cleaning, a perfectly competitive firm, cleans 40 garages a week. Its marginal cost is $35, its price is $35, and its average total cost is $40. Jane",
      ["is maximizing profit, and earns an economic profit", "is not maximizing profit, yet earns an economic profit",
       "may be maximizing profit, and earns a normal profit", "is not maximizing profit, and takes an economic loss", NONE]),
 18: ("Which is the best example of a common resource?", ["A house", "The Internet", "Air traffic control", "Fish in the ocean", "A lighthouse"]),
 19: ("You have just become Taco Bell's vice president for advertising, and your next campaign will go after the fast-food rival whose product is the closest substitute for Taco Bell's tacos. Which rival is that?",
      ["One whose cross elasticity of demand with Taco Bell tacos is −2", "One whose cross elasticity of demand with Taco Bell tacos is 2",
       "One whose price elasticity of demand is 2", "One whose income elasticity of demand is −2"]),
 20: ("For a good that creates an external cost, the marginal social cost curve",
      ["slopes upward and lies above the marginal private cost curve", "slopes upward and coincides with the marginal private cost curve",
       "slopes downward and coincides with the marginal private cost curve", "slopes upward and lies below the marginal private cost curve",
       "slopes downward and lies above the marginal private cost curve"]),
 21: ("Why can private firms not usually produce the efficient quantity of a public good?",
      ["They could, but the government bans private firms from producing public goods", "Production costs too much for private firms to manage",
       "Because of free riders, the firms would earn no revenue from it", NONE]),
 22: CHEAT,
 23: ("When the demand for a good rises, the demand for the labor that produces it",
      ["rises", "falls", "stays the same", "could rise, fall or stay the same"]),
 24: ("Since around 1979, the distribution of income in the United States has",
      ["grown more equal", "grown less equal", "kept the same degree of inequality", "changed so much that 1979 cannot be compared with today"]),
 25: ("A production point beyond the production possibilities frontier is",
      ["a point where resources are not being used efficiently", "a combination society cannot produce with its present resources and technology",
       "a sign that resources are being used very efficiently", "a sign that both goods have increasing costs"]),
 26: ("A rise in the wage rate will do which of these only if the substitution effect outweighs the income effect?",
      ["Raise the quantity of labor supplied", "Lower the quantity of labor supplied", "Raise the quantity of labor demanded",
       "Lower the quantity of labor demanded", "Both the first and the fourth"]),
 27: ("The equilibrium wage for low-skilled labor is $13.25. The federal government lifts the minimum wage from $8.25 to $15.00 an hour. The result is",
      ["less unemployment", "more unemployment", "a shortage of low-skilled labor", "neither a shortage nor a surplus of low-skilled labor"]),
 28: ("A new fertilizer lets farmers grow more barley, while research finds that eating barley can cause severe headaches. Supply and demand shift by the same amount. What happens to the equilibrium price and quantity of barley?",
      pq("f?", "?d", "fs", "fi", "s?")),
 29: GAME(False),
}

# ---------------------------------------------------------------- topics ----
SD, EL, GI, IT, PPF = "Supply and Demand", "Elasticity", "Government Intervention", "International Trade", "The PPF"
PC, MO, MC, OL = "Perfect Competition", "Monopoly", "Monopolistic Competition", "Oligopoly"
EX, PG, LA, IN = "Externalities", "Public Goods and Common Resources", "Labor Markets", "Inequality"

TOPIC = {
 "212": {1: LA, 2: MC, 3: MO, 4: OL, 5: MO, 6: EX, 7: OL, 8: SD, 9: MO, 10: EX, 11: OL, 12: EL, 13: IN, 14: SD, 15: LA,
         16: PC, 17: SD, 18: IT, 19: PG, 20: EX, 21: MC, 22: PC, 23: MO, 24: SD, 25: MO, 26: PC, 27: SD, 28: EL, 29: PG, 30: OL},
 "211": {1: SD, 2: MO, 3: OL, 4: IN, 5: LA, 6: EL, 7: EX, 8: IN, 9: LA, 10: EL, 11: SD, 12: SD, 13: PG, 14: PG, 15: PC,
         16: MC, 17: GI, 18: MC, 19: OL, 20: LA, 21: EX, 22: MO, 23: GI, 24: SD, 25: SD, 26: OL, 27: PPF, 28: OL, 29: MO},
 "203": {1: SD, 2: EX, 3: SD, 4: PC, 5: GI, 6: SD, 7: PG, 8: MC, 9: MO, 10: SD, 11: OL, 12: EL, 13: PC, 14: MO, 15: EX,
         16: OL, 17: MO, 18: PC, 19: IN, 20: EX, 21: SD, 22: SD, 23: MO, 24: MC, 25: PPF, 26: PG, 27: SD, 28: MO, 29: OL},
 "201": {1: SD, 2: PC, 3: SD, 4: EL, 5: IT, 6: SD, 7: EX, 8: IN, 9: MC, 10: SD, 11: OL, 12: SD, 13: GI, 14: EX, 15: LA,
         16: SD, 17: PC, 18: PG, 19: EL, 20: EX, 21: PG, 22: OL, 23: LA, 24: IN, 25: PPF, 26: LA, 27: GI, 28: SD, 29: OL},
}
FREE = {"212": 31, "211": 30, "203": 30, "201": 30}   # the "answer A" point each paper ends with
