"""Widgets for the four earlier ECO2023 Exam 1 papers. Key: term code ->
{question: (where, cfg)}. Every number drawn is the exam's or the written
solution's; symbolic figures carry none."""
from widgets_lib import *

def ss(curve, d, good, title, lede, why):
    """Four captions for a single-shift preset."""
    D = curve == "D"; right = d == "right"
    short = (D and right) or (not D and not right)
    s2 = "At the old price P₁ buyers want more than sellers offer, a shortage, so the price is bid up." if short else \
         "At the old price P₁ sellers offer more than buyers want, a surplus, so the price falls."
    s3 = "The market settles at P₂ and Q₂: a %s price and a %s quantity." % ("higher" if short else "lower", "larger" if right else "smaller")
    return shift(curve, d, title, lede, ["The market for %s starts in equilibrium at P₁ and Q₁." % good,
        "%s %s shifts %s, from %s₁ to %s₂." % (why, "Demand" if D else "Supply", d, curve, curve), s2, s3])

TAX4 = ["The market starts at P₁ and Q₁ with no tax.",
        "A tax on sellers raises what they must collect at every quantity: the supply curve shifts up by the tax, to S + tax.",
        "Buyers now pay Pᵇ, sellers keep Pˢ, and the gap between them is the tax. The quantity falls to Q₂.",
        "The trades between Q₂ and Q₁ no longer happen, and the surplus they carried is the deadweight loss."]
TAX_SPLIT = ["Same supply curve, same tax; switch the buttons to change how steep demand is.",
             "The tax shifts the supply curve up by its full amount, to S + tax.",
             "Buyers pay Pᵇ and sellers keep Pˢ. On the steep curve most of the gap is above P₁, so buyers bear most of it; on the flat curve most is below, on sellers.",
             "The deadweight loss is the trades lost between Q₂ and Q₁, and it is larger on the flat curve, where quantity gives way more."]
TR4 = ["Along a straight demand curve elasticity falls from infinite at the top to zero at the bottom, and total revenue traces a hump.",
       "Revenue peaks where demand is unit elastic: a price change there leaves total revenue alone.",
       "Above that point demand is elastic, so raising the price loses more in quantity than it gains in price, and revenue falls.",
       "Below it demand is inelastic, so raising the price gains more in price than it loses in quantity, and revenue rises."]
IMPORTS3 = ["With no trade the market clears at P₁ and Q₁, consumers keeping CS and producers PS.",
            "The world price is below P₁. At that price domestic producers offer Qₛ and domestic buyers want Qᴅ.",
            "With trade the price falls to the world price and imports fill the gap. CS grows by more than PS shrinks, so total surplus rises."]
EXPORTS3 = ["With no trade the market clears at P₁ and Q₁, consumers keeping CS and producers PS.",
            "The world price is above P₁. At that price domestic producers offer Qₛ and domestic buyers want only Qᴅ.",
            "With trade the price rises to the world price and the difference is exported. PS grows by more than CS shrinks, so total surplus rises."]
TARIFF4 = ["At the world price Pᵂ domestic producers sell Qₛ, buyers take Qᴅ, and imports fill the gap.",
           "A tariff lifts the domestic price to Pᵀ. Producers sell more, Qₛ′, buyers take less, Qᴅ′, and imports shrink.",
           "Consumer surplus shrinks and producer surplus grows, but consumers lose more than producers gain.",
           "Of what consumers lose, the government collects the tariff revenue; the two red triangles are lost to everyone, the deadweight loss."]
QUOTA4 = ["At the world price Pᵂ domestic producers sell Qₛ, buyers take Qᴅ, and imports fill the gap.",
          "A quota caps imports, which lifts the domestic price to Pᵠ. Producers sell more, Qₛ′, and buyers take less, Qᴅ′.",
          "Consumer surplus shrinks and producer surplus grows, but consumers lose more than producers gain.",
          "The band over the remaining imports goes to whoever holds the import licences, and the two red triangles are the deadweight loss."]
PQUOTA4 = ["The market clears at P₁ and Q₁.",
           "A production quota below Q₁ caps output at Qᵠ, so the quantity falls to the quota.",
           "With less on offer, the price is read up to the demand curve: buyers pay P₂, above P₁.",
           "The trades between Qᵠ and Q₁ no longer happen, and their surplus is the deadweight loss."]
CEIL4 = ["The market clears at P₁ and Q₁.",
         "A price ceiling below P₁ binds: nobody may charge more than Pᶜ.",
         "At Pᶜ sellers offer Qₛ and buyers want Qᴅ, so there is a shortage.",
         "Only Qₛ is traded. The surplus on the units between Qₛ and Q₁ is lost to everyone: the deadweight loss."]
CEILD4 = ["With a ceiling below the market rent, only Qₛ apartments are rented and there is a shortage.",
          "The trades between Qₛ and Q₁ do not happen, so their surplus is the deadweight loss.",
          "Incomes rise and demand shifts right, from D₁ to D₂, but the rent may not rise, so landlords still offer Qₛ.",
          "The market would now clear at Q₂, further from Qₛ than Q₁ was, so more trades are lost and the deadweight loss grows."]
MSBC = "The efficient quantity is where marginal social benefit meets marginal social cost. Below it MSB exceeds MSC and more should be made; above it the reverse."

W = {}

# ------------------------------------------------------------ Fall 2023 ----
F = {}
F[2] = ("solution", tax("A Tax on Pizza Sellers", "The tax moves the market quantity; the efficient quantity, where MSB meets MSC, stays at Q₁.", TAX4, scenarios=False))
F[3] = ("solution", ss("S", "right", "electric vehicles", "The Market for Electric Vehicles", "Chips are an input, so cheaper chips move the supply curve.", "Cheaper chips lower the cost of building an EV."))
F[4] = ("solution", quota("A Production Quota Below the Equilibrium Quantity", "The quota caps output, and the price is read off demand.", PQUOTA4))
F[5] = ("solution", msb_msc("A Fall in the Marginal Social Cost of Wind Power", "The efficient quantity is where MSB meets MSC.", shift="MSCdown",
        steps=["Wind power's efficient quantity, Q₁, is where its marginal social benefit meets its marginal social cost.",
               "Cheaper generation lowers the marginal social cost at every quantity: MSC shifts right, from MSC₁ to MSC₂.",
               "MSC₂ meets the unchanged MSB curve further out, at Q₂, so the allocatively efficient quantity has increased."]))
F[6] = ("solution", midpoint(12, 18, 8, 22, "The Midpoint Formula Between Two Points", "Each change is measured against the middle of its own interval.",
        ["A is 12 million pizzas at $18 and B is 8 million at $22. The midpoint method divides each change by the middle of its interval.",
         "Quantity falls by 4 million on a midpoint of 10 million, a 40% fall.",
         "Price rises by $4 on a midpoint of $20, a 20% rise. Dividing 40% by 20% gives 2, so demand is elastic between A and B."], E=2.0))
F[7] = ("solution", ss("D", "left", "potato chips", "The Market for Potato Chips", "Chips are a normal good, so demand follows income.", "Incomes fall, and for a normal good that lowers demand."))
F[9] = ("solution", surplus_shift("D", "right", "TS", "Total Surplus When Demand Increases", "Total surplus is the area between demand and supply out to the quantity traded.",
        ["At P₁ and Q₁ consumers keep CS and producers PS. Together they are total surplus.",
         "Demand increases, from D₁ to D₂.",
         "The market settles at P₂ and Q₂: more is traded at a higher price.",
         "Between the higher demand curve and the same supply curve, out to the larger Q₂, the area is bigger: total surplus rises."]))
F[12] = ("solution", ss("S", "right", "pizza", "The Market for Pizza", "Cheese is an input, so its price moves the supply curve.", "Cheaper cheese lowers the cost of making a pizza."))
F[13] = ("solution", tax("Who Pays a Tax: Steep Demand Against Flat Demand", "Switch between the two demand curves to see how the same tax is shared.", TAX_SPLIT))
F[14] = ("solution", ceiling(30, "A Price Below the Market-Clearing Price", "Soaring resale prices are the sign of a shortage at the original price.",
        ["Tickets would clear at P₁, the price at which the quantity demanded equals the quantity supplied.",
         "The original price was set below P₁.",
         "At that price fans want Qᴅ tickets and only Qₛ exist: a shortage, which is what the resale market prices in."], dwl=False, tag="Original price", pl="P₀"))
F[16] = ("solution", dbl("right", "right", "Both Curves Shift: Tablets", "The two panels differ only in which shift is larger.",
        ["The tablet market starts at Point 1 in both panels.",
         "Tablets are a normal good and incomes rise, so demand shifts right, from D₁ to D₂.",
         "Better technology shifts supply right, from S₁ to S₂.",
         "Both shifts raise the quantity, so it increases in either panel. The price rises when the demand shift is larger and falls when the supply shift is, so it cannot be determined."]))
F[17] = ("solution", floor_labor("A Minimum Wage Above the Market Wage", "A price floor in the labor market.",
        ["Without a minimum wage the labor market clears at W₁ and L₁.",
         "A minimum wage above W₁ binds: no one may be paid less than Wᵐ.",
         "At Wᵐ firms hire only Lᴅ, so employment falls, while Lₛ people want work. The gap between them is the unemployed looking for a job."]))
F[19] = ("solution", ss("S", "left", "apples", "The Market for Apples", "A frost takes out part of the crop at every price.", "The frost destroys most of the crop, so fewer apples can be offered at any price."))
F[21] = ("solution", tr_test("The Total Revenue Test", "Revenue is highest where demand is unit elastic.", TR4))
F[22] = ("solution", ceiling_demand_up("A Rent Ceiling When Demand Rises", "The ceiling holds the rent, so landlords offer no more than before.", CEILD4))
F[23] = ("solution", ss("D", "right", "lithium", "The Market for Lithium", "More EVs sold means more batteries, and so more lithium wanted.", "Battery makers want more lithium at every price."))
F[25] = ("solution", ss("S", "left", "air travel", "The Market for Air Travel", "Jet fuel is an input, so its price moves the supply curve.", "Dearer jet fuel raises the cost of every flight."))
F[26] = ("stem", four("The Market for Delivered Pizza"))
F[27] = ("solution", trade("imports", "A Market That Imports", "The world price is below the no-trade price.", IMPORTS3))
F[28] = ("solution", movement("A Change in Price Moves Along the Curve", "A price change is a movement along the demand curve, not a shift of it.",
        ["At P₁ buyers take Q₁. The demand curve itself is fixed by incomes, related prices, tastes and expectations.",
         "A higher price moves buyers up along the same curve, to Q₂. Nothing has shifted."]))
F[29] = ("solution", dbl("right", "right", "Both Curves Shift: Pizza", "Cheaper sauce moves supply by more than rising incomes move demand.",
        ["The pizza market starts at Point 1.",
         "Pizza is a normal good and incomes rise, so demand shifts right, from D₁ to D₂.",
         "Cheaper tomato sauce shifts supply right, from S₁ to S₂, and by more.",
         "Both shifts raise the quantity. The larger supply shift wins on price, so the price falls and the quantity increases."], bigger="supply"))
F[30] = ("solution", tr_test("Unit Elastic Demand and Total Revenue", "At the unit-elastic point a price change leaves revenue unchanged.", TR4))
F[31] = ("solution", tariff("A Tariff on an Imported Good", "A tariff and a quota both raise the domestic price and cut imports.", TARIFF4))
F[32] = ("solution", dbl("left", "right", "Both Curves Shift: Electric Vehicles", "The fall in income moves demand by more than cheaper batteries move supply.",
        ["The EV market starts at Point 1.",
         "EVs are a normal good and incomes fall, so demand shifts left, from D₁ to D₂, and by more.",
         "Cheaper batteries shift supply right, from S₁ to S₂.",
         "Both shifts lower the price. The larger demand shift wins on quantity, so the price falls and the quantity decreases."], bigger="demand"))
F[33] = ("solution", tariff("What a Tariff Does to Total Surplus", "Consumers lose more than producers and the government gain together.", TARIFF4))
F[34] = ("solution", ss("S", "left", "cars", "The Market for Cars", "Wages are a cost of production, so they move the supply curve.", "Higher wages raise the cost of building a car."))
F[35] = ("solution", ss("S", "right", "computer chips", "The Market for Computer Chips", "Technology moves supply; it is not a demand shifter.", "A technological advance lowers the cost of making chips."))
F[36] = ("solution", msb_msc("The Efficient Quantity of Corn", "At 10 million bushels the benefit of one more exceeds its cost.", mark=(10, 8, 4),
        steps=["At the 10 millionth bushel the marginal social benefit is $8 and the marginal social cost is $4, so that bushel is worth $4 more than it costs.",
               "MSB falls and MSC rises as output grows, so they meet beyond 10 million. The allocatively efficient quantity is more than 10 million bushels."]))
F[37] = ("solution", ss("D", "left", "the illegal good", "Sanctions on Buyers", "A penalty on buyers lowers what they will pay a seller.", "The expected penalty comes off the most a buyer will pay."))
F[39] = ("solution", trade("exports", "A Market That Exports", "The world price is above the no-trade price.", EXPORTS3))
W["233"] = F

# ---------------------------------------------------------- Summer 2023 ----
U = {}
U[1] = ("solution", surplus_shift("S", "right", "CS", "Consumer Surplus When Costs Fall", "Consumer surplus is the area under demand and above the price.",
        ["At P₁ and Q₁ consumers keep CS, the area between the demand curve and the price.",
         "Cheaper production increases supply, from S₁ to S₂.",
         "The market settles at P₂ and Q₂: a lower price and a larger quantity.",
         "A lower price and more units both add to the area under demand and above the price, so consumer surplus definitely increases."]))
U[2] = ("solution", tr_test("The Total Revenue Test", "Revenue is highest where demand is unit elastic.", TR4))
U[4] = ("solution", two_market("The Market for Skim Milk", "Dright", "The Market for Cream", "right", "Complements in Production: Skim Milk and Cream",
        "One batch of milk yields both, so a change in one market reaches the other through the dairy.",
        ["Both markets start at their own equilibrium, P₁ and Q₁.",
         "The demand for skim milk increases: its demand curve shifts right, from D₁ to D₂.",
         "Skim milk settles at a higher price and a larger quantity, so more milk is separated.",
         "Separating more milk yields more cream as a by-product, so the supply of cream shifts right, from S₁ to S₂.",
         "Cream settles at P₂ and Q₂: a lower price and a larger quantity."]))
U[7] = ("solution", vertical_demand("Perfectly Inelastic Demand", "An elasticity of zero: the quantity does not respond to price at all.",
        caption="Buyers take Q₁ whatever the price, so the demand curve is a vertical line."))
U[8] = ("solution", ss("S", "right", "televisions", "The Market for Televisions", "A technological advance moves the supply curve.", "Better technology lowers the cost of making a television."))
U[9] = ("solution", movement("A Change in Price Moves Along the Curve", "A price change is a movement along the demand curve, not a shift of it.",
        ["At P₁ buyers take Q₁. The curve itself is fixed by incomes, related prices, tastes and expectations.",
         "A higher price of cookies moves buyers up along the same curve, to Q₂. Nothing has shifted."]))
U[11] = ("solution", dbl("right", "left", "Both Curves Shift: Oil Expected to Be Dearer", "The two panels differ only in which shift is larger.",
        ["Oil starts at Point 1 in both panels. Buyers and sellers alike expect a higher price after the hurricane.",
         "Buyers want to stock up now, so today's demand shifts right, from D₁ to D₂.",
         "Sellers would rather hold oil back for the higher price, so today's supply shifts left, from S₁ to S₂.",
         "Both shifts raise the price, so it rises in either panel. Quantity rises when the demand shift is larger and falls when the supply shift is, so it cannot be determined."]))
U[13] = ("solution", ss("S", "left", "airline travel", "The Market for Airline Travel", "Jet fuel is an input, so its price moves the supply curve.", "Dearer jet fuel raises the cost of every flight."))
U[15] = ("solution", dbl("left", "right", "Both Curves Shift: Used Cars", "The two panels differ only in which shift is larger.",
        ["The used-car market starts at Point 1 in both panels.",
         "Loans are a complement to used cars, so dearer loans shift demand left, from D₁ to D₂.",
         "More dealerships shift supply right, from S₁ to S₂.",
         "Both shifts lower the price, so it falls in either panel. Quantity rises when the supply shift is larger and falls when the demand shift is, so it cannot be determined."]))
U[16] = ("solution", ceilings_compare("Four Rent Ceilings Against a $1,500 Rent", "Pick a ceiling. The deadweight loss is the surplus on the apartments no longer rented."))
U[17] = ("solution", msb_msc("Too Many Tacos", "The last taco is worth less than it costs, so cut back toward the efficient quantity.", caption=MSBC))
U[18] = ("solution", midpoint(21, 1.40, 19, 1.80, "The Midpoint Formula Between Two Points", "Each change is measured against the middle of its own interval.",
        ["A is 21 million burritos at $1.40 and B is 19 million at $1.80. The midpoint method divides each change by the middle of its interval.",
         "Quantity falls by 2 million on a midpoint of 20 million, a 10% fall.",
         "Price rises by $0.40 on a midpoint of $1.60, a 25% rise. Dividing 10% by 25% gives 0.4, so demand is inelastic between A and B."], E=0.4))
U[19] = ("solution", ppf_shift("Good X", "Good Y", "A Larger Labor Force Shifts the PPF Outward", "More workers mean more of both goods can be produced.",
        ["The nation can produce any combination on its current frontier, PPF₁.",
         "Immigration adds workers, so every combination reachable before and more is attainable: the frontier shifts outward to PPF₂."]))
U[20] = ("solution", trade("imports", "A Market That Imports", "The world price is below the no-trade price.", IMPORTS3))
U[21] = ("solution", ss("D", "right", "solar panels", "The Market for Solar Panels", "Without externalities the efficient quantity is the equilibrium quantity.", "More buyers want panels at every price, so"))
U[23] = ("stem", four("The Market for Pizza"))
U[24] = ("solution", tariff("Who a Tariff Harms", "Producers and the government gain; consumers lose more than both together.", TARIFF4))
U[25] = ("solution", ss("D", "right", "lithium", "The Market for Lithium", "More EVs sold means more batteries, and so more lithium wanted.", "Battery makers want more lithium at every price."))
U[26] = ("solution", ppf_two((240, 60), (300, 30), "Loaves\nof Bread", "Gallons of Maple Syrup", "loaves", "gallons", "Opportunity Cost Between Two Points on the Frontier",
        "Read the move from A to B off the two axes.",
        ["A is 240 loaves and 60 gallons; B is 300 loaves and 30 gallons. Both lie on the frontier.",
         "Moving from A to B, bread output rises from 240 loaves to 300, a gain of 60 loaves.",
         "Syrup output falls from 60 gallons to 30, so those 60 loaves cost 30 gallons. Each loaf costs 30 ÷ 60 = 0.5 gallons of maple syrup."], 0.5))
U[27] = ("solution", ppf_bowed("Pizza", "Soda", "Rising Opportunity Cost Along a Bowed-Out Frontier", "Each extra batch of pizza costs more soda than the one before.",
        ["On a bowed-out frontier the slope steepens as more pizza is made. Compare two equal moves along it.",
         "From A to B the nation gains some pizza and gives up only a little soda: the first resources moved are the ones best suited to pizza.",
         "From B to C the same gain in pizza costs much more soda. The opportunity cost of pizza rises, and, read the other way, the cost of soda falls."]))
U[29] = ("solution", tax("Who Pays a Tax: Steep Demand Against Flat Demand", "Switch between the two demand curves to see how the same tax is shared.", TAX_SPLIT))
W["232"] = U

# ---------------------------------------------------------- Spring 2023 ----
P = {}
P[3] = ("solution", ss("S", "left", "automobiles", "The Market for Automobiles", "Chips are an input, so dearer chips move the supply curve.", "Supply-chain trouble raises the cost of the chips in every car."))
P[4] = ("solution", quota("A Production Quota Above the Equilibrium Quantity", "A cap the market never reaches changes nothing.",
        ["The market clears at P₁ and Q₁.",
         "A quota set above Q₁ does not bind: producers were never going to make that much, so P₁ and Q₁ prevail."], binding=False))
P[5] = ("solution", dbl("right", "right", "Both Curves Shift: Low-Carb Food", "More producers move supply by more than more buyers move demand.",
        ["The low-carb market starts at Point 1.",
         "More people want low-carb food, so demand shifts right, from D₁ to D₂.",
         "More firms make it, so supply shifts right, from S₁ to S₂, and by more.",
         "Both shifts raise the quantity. The larger supply shift wins on price, so the price falls and the quantity increases."], bigger="supply"))
P[6] = ("solution", midpoint(12, 19, 8, 21, "The Midpoint Formula Between Two Points", "Each change is measured against the middle of its own interval.",
        ["A is 12 million pizzas at $19 and B is 8 million at $21. The midpoint method divides each change by the middle of its interval.",
         "Quantity falls by 4 million on a midpoint of 10 million, a 40% fall.",
         "Price rises by $2 on a midpoint of $20, a 10% rise. Dividing 40% by 10% gives 4, so demand is elastic between A and B."], E=4.0))
P[7] = ("solution", ss("D", "right", "potato chips", "The Market for Potato Chips", "Chips are a normal good, so demand follows income.", "Incomes rise, and for a normal good that raises demand."))
P[9] = ("solution", two_market("The Market for Skim Milk", "Pup", "The Market for Cream", "right", "Complements in Production: Skim Milk and Cream",
        "One batch of milk yields both, so a change in one market reaches the other through the dairy.",
        ["Both markets start at their own equilibrium, P₁ and Q₁.",
         "The price of skim milk rises, from P₁ to P₂, and dairies respond by separating more: a movement up along the supply curve.",
         "More milk separated means more cream comes out with it, so the supply of cream shifts right, from S₁ to S₂.",
         "Cream settles at P₂ and Q₂: a lower price and a larger quantity."]))
P[12] = ("solution", ss("S", "right", "houses", "The Market for Houses", "Bricks are an input, so their price moves the supply curve.", "Cheaper bricks lower the cost of building a house."))
P[13] = ("solution", tax("Who Pays a Tax: Steep Demand Against Flat Demand", "Switch between the two demand curves to see how the same tax is shared.", TAX_SPLIT))
P[14] = ("solution", dbl("right", "left", "Both Curves Shift: Oil Expected to Be Dearer", "The two panels differ only in which shift is larger.",
        ["Oil starts at Point 1 in both panels. Buyers and sellers alike expect a higher price next month.",
         "Buyers want to buy now, so today's demand shifts right, from D₁ to D₂.",
         "Sellers would rather wait for the higher price, so today's supply shifts left, from S₁ to S₂.",
         "Both shifts raise the price, so it rises in either panel. Quantity rises when the demand shift is larger and falls when the supply shift is, so it cannot be determined."]))
P[15] = ("solution", ppf_shift("Good X", "Good Y", "Better Technology Shifts the PPF Outward", "The same resources now make more of both goods.",
        ["The nation can produce any combination on its current frontier, PPF₁.",
         "Better technology lets the same resources make more, so the frontier shifts outward to PPF₂. That is economic growth."]))
P[17] = ("solution", subsidy("A Subsidy to Sugar Producers", "A payment per unit to sellers shifts supply down by the subsidy.",
        ["The sugar market starts at P₁ and Q₁ with no subsidy.",
         "A subsidy lowers what sellers need from buyers at every quantity: the supply curve shifts down by the subsidy.",
         "Buyers now pay Pᶜ, below P₁, and sellers receive Pᵖ, which includes the subsidy, above P₁. The quantity rises to Q₂."]))
P[18] = ("solution", tax("A Tax Cuts Quantity More When Demand Is Elastic", "Switch between the two demand curves and watch Q₂.", TAX_SPLIT))
P[19] = ("solution", dbl("left", "left", "Both Curves Shift: Movie Tickets", "The two panels differ only in which shift is larger.",
        ["The movie market starts at Point 1 in both panels.",
         "Movies are a normal good and incomes fall, so demand shifts left, from D₁ to D₂.",
         "Fewer theaters shift supply left, from S₁ to S₂.",
         "Both shifts cut the quantity, so it falls in either panel. Price falls when the demand shift is larger and rises when the supply shift is, so it cannot be determined."]))
P[22] = ("solution", ss("S", "right", "ethanol", "The Market for Ethanol", "New technology moves the supply curve.", "A new production technology lowers the cost of making ethanol."))
P[23] = ("solution", ss("D", "right", "isopropyl alcohol", "The Market for Isopropyl Alcohol", "More sanitizer made means more alcohol wanted.", "Sanitizer makers want more alcohol at every price, so"))
P[24] = ("stem", four("The Market for Pizza"))
P[25] = ("solution", ceiling_demand_up("A Rent Ceiling When Income Rises", "The ceiling holds the rent, so landlords offer no more than before.", CEILD4))
P[26] = ("solution", ss("S", "left", "potato chips", "The Market for Potato Chips", "Without externalities the efficient quantity moves with the equilibrium.", "Dearer potatoes raise the cost of making chips."))
P[27] = ("solution", along_line("Elasticity Along a Straight-Line Demand Curve", "One curve, three points, three different elasticities.",
        ["A straight demand curve has one slope but a different elasticity at every point.",
         "High on the curve, where the price is high, demand is elastic: a small percentage price change moves quantity by a large percentage.",
         "At the midpoint demand is unit elastic.",
         "Low on the curve, where the price is low, demand is inelastic. So the higher the price, the larger the elasticity."]))
P[29] = ("solution", ppf_points("Points On, Inside and Beyond the Frontier", "The frontier is the outer limit of what the resources can produce.",
        "A point inside the frontier is attainable but wastes resources; a point on it is production efficient; a point beyond it cannot be reached."))
P[31] = ("solution", tariff("A Tariff on Solar Panels", "Consumers lose more than producers and the government gain together.", TARIFF4))
P[32] = ("solution", dbl("left", "right", "Both Curves Shift: Electric Vehicles", "The fall in income moves demand by more than cheaper batteries move supply.",
        ["The EV market starts at Point 1.",
         "EVs are a normal good and incomes fall, so demand shifts left, from D₁ to D₂, and by more.",
         "Cheaper batteries shift supply right, from S₁ to S₂.",
         "Both shifts lower the price. The larger demand shift wins on quantity, so the price falls and the quantity decreases."], bigger="demand"))
P[34] = ("solution", surplus_shift("D", "right", "PS", "Producer Surplus When Demand Increases", "Producer surplus is the area above supply and below the price.",
        ["At P₁ and Q₁ producers keep PS, the area between the price and the supply curve.",
         "Demand increases, from D₁ to D₂.",
         "The market settles at P₂ and Q₂: a higher price and a larger quantity.",
         "A higher price and more units both add to the area above the same supply curve, so producer surplus increases."]))
P[36] = ("solution", tax("Tax Revenue: Steep Demand Against Flat Demand", "Revenue is the tax times Q₂, so the curve on which quantity holds up best raises more.", TAX_SPLIT))
P[37] = ("solution", ss("D", "left", "new houses", "The Market for New Houses", "A home loan is a complement, so its price moves the demand for houses.", "Dearer loans mean fewer buyers at every price, so"))
P[38] = ("solution", ppf_table([(0, 40), (4, 36), (8, 28), (12, 16), (16, 0)], ["A", "B", "C", "D", "E"], 2, 3, "Hybrid\nCars", "Electric Vehicles", "hybrids", "EVs",
        "Opportunity Cost Along the Frontier", "Read the move from 8 hybrids to 12 off the two axes.",
        ["The five points of the table lie on the frontier. C is 8 hybrids and 28 EVs; D is 12 hybrids and 16 EVs.",
         "Moving from C to D, hybrid output rises from 8 to 12, a gain of 4 hybrids.",
         "EV output falls from 28 to 16, so those 4 hybrids cost 12 EVs. Each hybrid costs 12 ÷ 4 = 3 electric vehicles."], 3))
P[39] = ("solution", tariff("An Import Quota on Sugar", "A quota raises the domestic price the way a tariff does.", QUOTA4, kind="quota"))
W["231"] = P

# ---------------------------------------------------------- Summer 2022 ----
M = {}
imp = trade("imports", "", "", IMPORTS3); exp = trade("exports", "", "", EXPORTS3)
for c in (imp, exp):
    for k in ("title", "lede", "axes"): c.pop(k)
M[1] = ("solution", {"title": "Imports and Exports", "lede": "Pick a case. Trade moves the price to the world price and surplus with it.",
        "axes": {"xmax": 110, "ymax": 110}, "scenarios": {"imp": dict({"label": "A market that imports"}, **imp), "exp": dict({"label": "A market that exports"}, **exp)}})
M[2] = ("solution", tr_test("The Total Revenue Test", "Revenue is highest where demand is unit elastic.", TR4))
M[4] = ("solution", steep_vs_flat("A Cost Increase Against Steep and Flat Demand", "The same supply shift; switch the buttons to change how steep demand is.",
        ["Switch between the two demand curves. The supply curve and its shift are the same on both.",
         "Higher costs shift supply left, from S₁ to S₂.",
         "On the steep, inelastic curve the price climbs a long way to P₂; on the flat, elastic one it barely moves. The cost increase raises the price most when demand is inelastic."]))
M[5] = ("solution", ss("D", "left", "bacon", "The Market for Bacon", "A change in preferences moves the demand curve.", "People now think bacon is less healthy, so they want less at every price."))
M[6] = ("solution", surplus_shift("D", "left", "PS", "Producer Surplus When Demand Falls", "Producer surplus is the area above supply and below the price.",
        ["At P₁ and Q₁ producers keep PS, the area between the price and the supply curve.",
         "Demand decreases, from D₁ to D₂.",
         "The market settles at P₂ and Q₂: a lower price and a smaller quantity.",
         "A lower price and fewer units both cut the area above the same supply curve, so producer surplus definitely decreases."]))
M[7] = ("solution", ppf_points("Points On, Inside and Beyond the Frontier", "The frontier is the outer limit of what the resources can produce.",
        "A point inside the frontier is attainable but wastes resources; a point on it is production efficient; a point beyond it cannot be reached."))
M[8] = ("solution", ss("S", "right", "televisions", "The Market for Televisions", "A technological advance moves the supply curve.", "Better technology lowers the cost of making a television."))
M[9] = ("solution", ceiling(30, "A Price Ceiling on Gasoline", "Below the market price, the two quantities part company.", CEIL4))
M[10] = ("solution", tariff("A Tariff on Solar Panels", "Consumers lose more than producers and the government gain together.", TARIFF4))
M[11] = ("solution", dbl("left", "right", "Both Curves Shift: Smartphones", "The two panels differ only in which shift is larger.",
        ["The smartphone market starts at Point 1 in both panels.",
         "Smartphones are a normal good and incomes fall, so demand shifts left, from D₁ to D₂.",
         "Cheaper production shifts supply right, from S₁ to S₂.",
         "Both shifts lower the price, so it falls in either panel. Quantity rises when the supply shift is larger and falls when the demand shift is, so it cannot be determined."]))
M[12] = ("solution", msb_msc("Allocative Efficiency", "The efficient quantity is where MSB meets MSC.", caption=MSBC))
M[13] = ("solution", ss("S", "left", "bus travel", "The Market for Bus Travel", "Diesel is an input, so its price moves the supply curve.", "Dearer diesel raises the cost of every bus trip."))
M[14] = ("solution", ss("S", "right", "the good", "More Suppliers Enter the Market", "The number of sellers is a supply shifter.", "With more suppliers, more is offered at every price, so"))
M[15] = ("solution", tax("A 10¢ Tax on Gasoline", "Buyers and sellers share the tax, so the pump price rises by less than 10¢.",
        ["The gasoline market starts at P₁ and Q₁ with no tax.",
         "The tax raises what sellers must collect at every quantity: the supply curve shifts up by the full 10¢, to S + tax.",
         "Buyers pay Pᵇ and sellers keep Pˢ; the gap is the 10¢. Pᵇ is above P₁ by only part of it, because sellers absorb the rest.",
         "The trades between Q₂ and Q₁ no longer happen, and the surplus they carried is the deadweight loss."], scenarios=False))
M[16] = ("solution", ss("D", "right", "tropical fish", "The Market for Tropical Fish", "A change in preferences moves the demand curve.", "More people want an aquarium, so"))
M[17] = ("solution", tax("Who Pays a Tax: Steep Demand Against Flat Demand", "Switch between the two demand curves to see how the same tax is shared.", TAX_SPLIT))
M[18] = ("solution", midpoint(21, 1.40, 19, 1.80, "The Midpoint Formula Between Two Points", "Each change is measured against the middle of its own interval.",
        ["A is 21 million burritos at $1.40 and B is 19 million at $1.80. The midpoint method divides each change by the middle of its interval.",
         "Quantity falls by 2 million on a midpoint of 20 million, a 10% fall.",
         "Price rises by $0.40 on a midpoint of $1.60, a 25% rise. Dividing 10% by 25% gives 0.4, so demand is inelastic between A and B."], E=0.4))
M[20] = ("solution", tariff("A Tariff on Sugar", "Producers sell more at a higher price; consumers pay it.", TARIFF4))
M[21] = ("solution", ss("S", "left", "chicken", "The Market for Chicken", "Bird flu takes birds out of the market at every price.", "With many birds lost, fewer chickens can be offered at any price."))
M[22] = ("solution", ss("S", "left", "houses", "The Market for Houses", "Plywood is an input, so its price moves the supply curve.", "Dearer plywood raises the cost of building a house."))
M[23] = ("stem", four("The Market for Pizza"))
M[24] = ("solution", two_market("The Market for Chicken Wings", "Pup", "The Market for White Meat", "right", "Complements in Production: Wings and White Meat",
        "One bird yields both, so a change in one market reaches the other through the farm.",
        ["Both markets start at their own equilibrium, P₁ and Q₁.",
         "The price of wings rises, from P₁ to P₂, and farms respond by raising more birds: a movement up along the supply curve.",
         "More birds raised means more white meat comes with them, so the supply of white meat shifts right, from S₁ to S₂.",
         "White meat settles at P₂ and Q₂: a lower price and a larger quantity."]))
M[25] = ("solution", ss("D", "left", "pizza", "The Market for Pizza", "Soda is a complement, so its price moves the demand for pizza.", "Dearer soda means fewer pizza-and-soda meals, so"))
M[26] = ("solution", ppf_two((240, 90), (300, 30), "Loaves\nof Bread", "Gallons of Maple Syrup", "loaves", "gallons", "Opportunity Cost Between Two Points on the Frontier",
        "Read the move from A to B off the two axes.",
        ["A is 240 loaves and 90 gallons; B is 300 loaves and 30 gallons. Both lie on the frontier.",
         "Moving from A to B, bread output rises from 240 loaves to 300, a gain of 60 loaves.",
         "Syrup output falls from 90 gallons to 30, so those 60 loaves cost 60 gallons. Each loaf costs 60 ÷ 60 = 1 gallon of maple syrup."], 1))
M[27] = ("solution", quota("A Production Quota Below the Equilibrium Quantity", "The quota caps output, and the price is read off demand.", PQUOTA4))
M[29] = ("solution", vertical_demand("Insulin: Perfectly Inelastic Demand", "With an elasticity of zero, a supply shift moves only the price.",
        steps=["Insulin buyers take Q₁ whatever the price, so the demand curve is vertical.",
               "Higher production costs shift supply left, from S₁ to S₂.",
               "The quantity cannot change, so the whole adjustment is in the price: it rises to P₂ and Q₁ is unchanged."], shift=True))
W["222"] = M
