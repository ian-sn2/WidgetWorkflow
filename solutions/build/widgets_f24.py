# Widgets for ECO2023 Fall 2024 Midterm 1. Key: question number -> (where, cfg).
# where = "stem" replaces the question's own figure; "solution" goes under the
# answer letter. Every number is the exam's or the written solution's.

def shift(curve, d, title, lede, steps):
    return {"preset": "shift", "shift": curve, "dir": d, "title": title, "lede": lede, "steps": steps}

W = {}

W[2] = ("solution", {
 "title": "The Midpoint Formula Between Two Points",
 "lede": "Each change is measured against the middle of its own interval.",
 "axes": {"xmax": 62, "ymax": 25, "money": True},
 "curves": [{"id": "D", "label": "D", "pts": [[40, 22.5], [58, 18]], "ldx": 6, "ldy": -8}],
 "points": [{"q": 46, "p": 21, "label": "A", "dx": 9, "dy": -9},
            {"q": 54, "p": 19, "label": "B", "dx": 9, "dy": 16}],
 "braces": [{"p": 0, "q1": 46, "q2": 54, "label": "8 more, a 16% rise", "below": True, "at": 1}],
 "vbraces": [{"p1": 19, "p2": 21, "q": 46, "label": "$2 less, a 10% fall", "side": "left", "at": 2}],
 "calcs": [{"text": "%ΔQ = 8 ÷ 50 = 16%", "at": 1},
           {"text": "%ΔP = $2 ÷ $20 = 10%", "at": 2},
           {"text": "Elasticity = 16% ÷ 10% = 1.60", "at": 2}],
 "steps": ["A is 46 pizzas at $21 and B is 54 pizzas at $19. The midpoint method divides each change by the middle of its interval, so the answer is the same in either direction.",
           "Quantity rises by 8 on a midpoint of 50, a 16% rise.",
           "Price falls by $2 on a midpoint of $20, a 10% fall. Dividing 16% by 10% gives 1.60, so demand is elastic between A and B."]})

W[3] = ("solution", shift("S", "left", "The Market for Potato Chips",
 "Potatoes are an input, so their price moves the supply curve.",
 ["The chip market starts in equilibrium at P₁ and Q₁. Incomes have not changed, so demand stays put.",
  "Dearer potatoes raise the cost of making chips, so supply shifts left, from S₁ to S₂.",
  "At the old price P₁ buyers want more chips than sellers now offer, a shortage, so the price is bid up.",
  "The market settles at P₂ and Q₂: a higher price and a smaller quantity."]))

W[5] = ("solution", {
 "title": "Complements in Production: Gasoline and Diesel",
 "lede": "One barrel yields both, so a change in one market reaches the other through the refinery.",
 "panels": [
  {"heading": "The Market for Gasoline", "axes": {"xmax": 110, "ymax": 110},
   "curves": [{"id": "S", "label": "S", "pts": [[8, 8], [100, 100]]},
              {"id": "D1", "label": "D₁", "pts": [[8, 92], [95, 5]], "ldx": 6, "ldy": -8},
              {"id": "D2", "label": "D₂", "pts": [[8, 68], [71, 5]], "color": "red", "from": "D1", "at": 1, "arrowP": 60, "ldx": 6, "ldy": -8}],
   "points": [{"q": 50, "p": 50, "pl": "P₁", "ql": "Q₁"},
              {"q": 38, "p": 38, "pl": "P₂", "ql": "Q₂", "color": "red", "at": 2}]},
  {"heading": "The Market for Diesel", "axes": {"xmax": 110, "ymax": 110},
   "curves": [{"id": "D", "label": "D", "pts": [[8, 92], [95, 5]], "ldx": 6, "ldy": -8},
              {"id": "S1", "label": "S₁", "pts": [[8, 8], [100, 100]]},
              {"id": "S2", "label": "S₂", "pts": [[8, 32], [76, 100]], "color": "red", "from": "S1", "at": 3, "arrowP": 88}],
   "points": [{"q": 50, "p": 50, "pl": "P₁", "ql": "Q₁"},
              {"q": 38, "p": 62, "pl": "P₂", "ql": "Q₂", "color": "red", "at": 4}]}],
 "steps": ["Both markets start at their own equilibrium, P₁ and Q₁.",
           "The demand for gasoline decreases: its demand curve shifts left, from D₁ to D₂.",
           "Gasoline settles at a lower price and a smaller quantity, so fewer barrels of oil are refined.",
           "Refining less oil means less diesel comes out as well, so the supply of diesel shifts left, from S₁ to S₂.",
           "Diesel settles at P₂ and Q₂: a higher price and a smaller quantity."]})

W[7] = ("solution", {
 "preset": "double", "demand": "left", "supply": "right", "compare": True, "big": 30, "small": 12, "arrowD": 12,
 "title": "Both Curves Shift: Oil Expected to Be Cheaper Next Month",
 "lede": "The two panels differ only in which shift is larger.",
 "headings": ["Larger Shift of Supply", "Larger Shift of Demand"],
 "steps": ["Oil starts at Point 1 in both panels. Buyers and sellers alike expect a lower price next month.",
           "Buyers put off purchases, so today's demand shifts left, from D₁ to D₂.",
           "Sellers would rather sell now, while the price is high, so today's supply shifts right, from S₁ to S₂.",
           "Both shifts lower the price, so it falls in either panel. Quantity rises when the supply shift is larger and falls when the demand shift is larger, so it cannot be determined."]})

W[9] = ("solution", {
 "title": "The Total Revenue Test With Inelastic Demand",
 "lede": "Revenue is price times quantity: the rectangle under each point.",
 "axes": {"xmax": 130, "ymax": 14, "money": True},
 "curves": [{"id": "D", "label": "D", "pts": [[85, 13], [125, 5]], "ldx": -14, "ldy": 14}],
 "areas": [{"pts": [[0, 0], [100, 0], [100, 10], [0, 10]], "label": "TR = $1,000", "color": "teal", "lp": [50, 5], "at": 1, "until": 2},
           {"pts": [[0, 0], [110, 0], [110, 8], [0, 8]], "label": "TR = $880", "color": "orange", "lp": [55, 4], "at": 2}],
 "points": [{"q": 100, "p": 10}, {"q": 110, "p": 8, "at": 1}],
 "calcs": [{"text": "Elasticity = 10% ÷ 20% = 0.5", "at": 1},
           {"text": "Total revenue at $10 = $10 × 100 = $1,000", "at": 1},
           {"text": "Total revenue at $8 = $8 × 110 = $880", "at": 2}],
 "steps": ["Take a price of $10 at which 100 units sell. A 20% fall in price, to $8, raises the quantity by only 10%, to 110 units.",
           "Quantity responds less than price, so elasticity is 10% ÷ 20% = 0.5 and demand is inelastic. At $10 total revenue is the rectangle under the point: $1,000.",
           "At $8 the rectangle is $8 × 110 = $880. The extra units do not make up for the lower price, so total revenue falls, as it always does when the price of an inelastic good falls."]})

W[11] = ("solution", shift("D", "right", "The Market for Hamburgers",
 "Hot dogs are a substitute, so their price moves the demand for hamburgers.",
 ["The hamburger market starts in equilibrium at P₁ and Q₁.",
  "Hot dogs get dearer, so some buyers switch to hamburgers: demand shifts right, from D₁ to D₂.",
  "At the old price P₁ buyers want more hamburgers than sellers offer, a shortage, so the price is bid up.",
  "The market settles at P₂ and Q₂: a higher price and a larger quantity."]))

W[13] = ("solution", {
 "title": "Opportunity Cost Along Sweet-Tooth Land's Frontier",
 "lede": "Read the move from B to C off the two axes.",
 "axes": {"x": "Chocolate\nBars", "y": "Cans of Cola", "xmax": 56, "ymax": 112, "xticks": [0, 10, 20, 30, 40], "yticks": [0, 40, 70, 90, 100]},
 "curves": [{"id": "PPF", "label": "", "pts": [[0, 100], [10, 90], [20, 70], [30, 40], [40, 0]], "curved": True}],
 "points": [{"q": 0, "p": 100, "label": "A", "dx": 8, "dy": -6, "guides": False},
            {"q": 10, "p": 90, "label": "B", "dx": -22, "dy": 15},
            {"q": 20, "p": 70, "label": "C", "dx": -22, "dy": 15},
            {"q": 30, "p": 40, "label": "D", "dx": -22, "dy": 15},
            {"q": 40, "p": 0, "label": "E", "dx": 8, "dy": -6, "guides": False}],
 "moves": [{"from": [10, 90], "to": [20, 70], "at": 1, "offset": -15}],
 "braces": [{"p": 5, "q1": 10, "q2": 20, "label": "10 bars gained", "below": True, "at": 1}],
 "vbraces": [{"p1": 70, "p2": 90, "label": "20 cans given up", "left": True, "at": 2}],
 "calcs": [{"text": "Cost of one bar = 20 cans ÷ 10 bars = 2 cans of cola", "at": 2}],
 "steps": ["The five points of the table lie on the frontier. B is 10 bars and 90 cans; C is 20 bars and 70 cans.",
           "Moving from B to C, chocolate output rises from 10 bars to 20, a gain of 10 bars.",
           "Cola output falls from 90 cans to 70, so those 10 bars cost 20 cans. Each bar costs 20 ÷ 10 = 2 cans of cola."]})

W[14] = ("solution", {
 "title": "Perfectly Elastic Demand",
 "lede": "Kisha's wheat is the same as everyone else's, so buyers pay the going price and not a cent more.",
 "axes": {"xmax": 110, "ymax": 110},
 "curves": [{"id": "D", "label": "D", "pts": [[8, 50], [100, 50]]}],
 "points": [{"q": 50, "p": 50, "dot": False, "pl": "P₁", "guides": "p", "showQ": False}],
 "caption": "Any quantity sells at P₁, and none above it: an infinite elasticity."})

W[16] = ("solution", shift("D", "right", "The Market for Bus Travel",
 "Bus travel is an inferior good, so demand moves against income.",
 ["The bus-travel market starts in equilibrium at P₁ and Q₁.",
  "Incomes fall, and for an inferior good that raises demand: the curve shifts right, from D₁ to D₂.",
  "At the old price P₁ riders want more trips than are offered, a shortage, so the price is bid up.",
  "The market settles at P₂ and Q₂: a higher price and a larger quantity."]))

W[17] = ("solution", {
 "title": "A Larger Capital Stock Shifts the PPF Outward",
 "lede": "More resources mean more of both goods can be produced.",
 "axes": {"x": "Good X", "y": "Good Y", "xmax": 125, "ymax": 125},
 "curves": [{"id": "PPF1", "label": "PPF₁", "pts": [[0, 90], [90, 0]], "ldx": -30, "ldy": 15},
            {"id": "PPF2", "label": "PPF₂", "pts": [[0, 115], [115, 0]], "color": "red", "from": "PPF1", "at": 1, "arrowP": 45, "ldx": 9, "ldy": -8}],
 "steps": ["The nation can produce any combination on its current frontier, PPF₁.",
           "With more capital, every combination it could reach before and more is attainable: the frontier shifts outward to PPF₂. That is economic growth, not a move along the frontier."]})

W[18] = ("solution", shift("D", "right", "The Market for Tacos",
 "Soda is a complement, so a cheaper soda raises the demand for tacos.",
 ["The taco market starts in equilibrium at P₁ and Q₁.",
  "Soda gets cheaper, people buy more of it, and they want tacos to go with it: demand shifts right, from D₁ to D₂.",
  "At the old price P₁ buyers want more tacos than sellers offer, a shortage, so the price is bid up.",
  "The market settles at P₂ and Q₂: a higher price and a larger quantity."]))

W[19] = ("solution", shift("D", "right", "The Market for Potato Chips",
 "A change in preferences moves the demand curve.",
 ["The chip market starts in equilibrium at P₁ and Q₁.",
  "People now think chips are healthier, so they want more at every price: demand shifts right, from D₁ to D₂.",
  "At the old price P₁ buyers want more chips than sellers offer, a shortage, so the price is bid up.",
  "The market settles at P₂ and Q₂: a higher price and a larger quantity."]))

W[21] = ("solution", shift("S", "left", "The Market for Houses",
 "Plywood is an input, so its price moves the supply of houses.",
 ["The housing market starts in equilibrium at P₁ and Q₁.",
  "Dearer plywood raises the cost of building, so supply shifts left, from S₁ to S₂.",
  "At the old price P₁ buyers want more houses than builders now offer, a shortage, so the price is bid up.",
  "The market settles at P₂ and Q₂: a higher price and a smaller quantity."]))

W[24] = ("stem", {
 "preset": "shift", "static": True,
 "title": "The Market for Pizza",
 "lede": "Pick a figure. Each shows one curve moving and the equilibrium it leads to.",
 "scenarios": {
  "A": {"label": "Figure A", "shift": "D", "dir": "right", "caption": "Demand shifts right, from D₁ to D₂, and the equilibrium moves up along S."},
  "B": {"label": "Figure B", "shift": "D", "dir": "left", "caption": "Demand shifts left, from D₁ to D₂, and the equilibrium moves down along S."},
  "C": {"label": "Figure C", "shift": "S", "dir": "left", "caption": "Supply shifts left, from S₁ to S₂, and the equilibrium moves up along D."},
  "D": {"label": "Figure D", "shift": "S", "dir": "right", "caption": "Supply shifts right, from S₁ to S₂, and the equilibrium moves down along D."}}})

W[25] = ("solution", {
 "preset": "double", "demand": "left", "supply": "left", "compare": True, "big": 30, "small": 12, "arrowD": 12,
 "title": "Both Curves Shift: Dearer Feed and Cheaper Fish",
 "lede": "The two panels differ only in which shift is larger.",
 "headings": ["Larger Shift of Supply", "Larger Shift of Demand"],
 "steps": ["The chicken market starts at Point 1 in both panels.",
           "Fish, a substitute, gets cheaper, so some buyers switch away from chicken: demand shifts left, from D₁ to D₂.",
           "Dearer feed raises the cost of raising chickens, so supply shifts left, from S₁ to S₂.",
           "Both shifts cut the quantity, so it falls in either panel. Price rises when the supply shift is larger and falls when the demand shift is larger, so it cannot be determined."]})

W[27] = ("solution", shift("S", "left", "The Market for Automobiles",
 "Computer chips are an input, so dearer chips move the supply of cars.",
 ["The car market starts in equilibrium at P₁ and Q₁.",
  "Supply-chain trouble makes chips dearer, raising the cost of building a car: supply shifts left, from S₁ to S₂.",
  "At the old price P₁ buyers want more cars than makers now offer, a shortage, so the price is bid up.",
  "The market settles at P₂ and Q₂: a higher price and a smaller quantity."]))
