#import "layout.typ": *
#import "tables.typ": *

#pagebreak()
= Task 3. Choosing a procurement mechanism

== Common comparison

The common objective, 100/20 fixed terrestrial benchmark, 25% floor, ten-year period, 3% real rate and #value("budget") gross budget are as in Task 2. Gross resource cost is charged to the budget before crediting any lease receipts. The original map rule yields no funded action and an infeasible floor under all three mechanisms. The following portfolios are computed under the same block reform and conditional verified overlay.

*Cooperative award.* The cooperative controls the entire grant allocation and can offer the direct packages in Task 2. The ceiling is reserved to it, with any residual unspent. The case assumes countywide construction capacity by the cooperative and does not infer it from the observed end of its network. Its result is exactly the direct benchmark.

*Competitive tender.* The board considers offers inside each bidder's assumed footprint. The cooperative offers both technologies within 13 backbone miles. The cable operator offers fiber within 6 miles in towns with a cable claim. The wireless entrant offers W within 9 miles in towns with a W claim. The cable bidder's backhaul and last-mile capital are 70% and 90% of the common direct coefficients. The wireless bidder's factors are 75% and 95%. These footprint and cost factors are scenarios for existing assets and procurement efficiencies. No bidder must serve outside its modeled footprint. For identical service bundles we retain the lowest conforming lifecycle bid; the board chooses the most households it can afford, then the lowest total requested cost at that coverage. At a fixed coverage, this also minimizes requested dollars per household. A greedy ranking of individual bids could violate the township floor. Actual procurement needs verified bidder footprints and binding offers. #cite("15")

*County partnership (PPP).* The county commissions common backhaul and leases it under published terms to qualified providers. The direct menu remains available. A town hub is placed at the median backbone distance $d_j$ of its originally unserved blocks, with median terrain $g_j$. Its capital is \$25,000 plus the fiber backhaul rate applied to $d_j$ and $g_j$. The rural lateral proxy is $abs(d_i - d_j) + 0.5$ miles and substitutes for $d_i$ on the tenant spur. Through a hub, the co-op can serve within 6 lateral miles, cable can offer fiber within 4, and the entrant can offer wireless within 5. Cable retains the 90% last-mile factor and the wireless entrant retains 95%. The link proxies have no bearing, easements or congestion information. #cite("10", "16")

The model needs at least one commissioned hub and two leased service blocks per commissioned hub. For each hub-dependent offer, use $x_a <= y_(j(a))$, $sum_(a : j(a)=j) x_a >= 2 y_j$ and $sum_j y_j >= 1$. The hub's O&M uses the fiber rate. The rent scenario is \$4,800 per provider–hub lease per year with one lease per distinct provider at each open hub. Rent is a transfer from provider to county. It neither increases the gross resource cost nor relaxes the common budget. The literature on shared rural wireless infrastructure and local loop access motivates testing this ownership model, while its costs and benefits here follow the specified scenario. #cite("10", "11", "16")

#pagebreak()
== Matched results and cost incidence

#tab((1.74fr, .84fr, 1fr, 1.04fr, .85fr, .75fr), ([Mechanism], [New HH], [Gross PV], [USD / HH], [Min. %], [F / W]), rows("mechanisms"))
#caption[*Table 4.* Block reform results at the common budget, period and 25% floor. USD/HH is gross lifecycle cost per new qualifying household opportunity.]

#tab((1.77fr, 1fr, 1fr, 1fr, 1fr), ([Mechanism], [Backhaul], [Last mile], [O&M PV], [Net outlay]), rows("lifecycle"))
#caption[*Table 5.* Cost components and county net outlay, million 2026 US dollars. Net outlay applies modeled lease credits after the gross budget check.]

The county PPP reaches #value("advantage") more households than the cooperative and #value("tender_gap") more than the tender. The cooperative gives a higher minimum township rate (#value("coop_min") versus #value("ppp_min")). A two-mile increase in all direct radii lifts tender coverage to 4,031. Shrinking the radii by two miles makes West Plains' floor infeasible. PPP reaches 4,381 at twice the hub capital rate and 4,883 at 75% of it. The PPP leads at both tested common budgets of \$9m and \$13m, adding 4,362 and 5,110 opportunities, respectively. It also leads when O&M is 75% or 150% of the base rates.

The base PPP opens hubs in East Corridor, West Plains, Central Town and River Bend. County hub capital is #value("ppp_capex"), with #value("ppp_om") discounted county O&M. Seven leases pay \$33,600 annually, or #value("ppp_rent") discounted. This covers #value("om_recovery") of county hub O&M, leaving \$44,981 in discounted operating costs plus the capital to fund. With seven leases, the operating break-even fee is about \$5,553 per lease-year. Gross costs assume the grant can finance the full modeled lifecycle. If realized, rents reduce county net outlay to #value("net_outlay"). Operators pay rents and manage retail service. The county bears renewal and vacancy risk. Retail fees, take-up and operator margins require actual offers and financing terms.

The eastern logistics corridor is a candidate anchor, given the narrative's nearby fiber termination. An employer or anchor institution could contract for shift-timed service or Wi-Fi after site verification. Workers, waiting drivers and warehouse tenants are outside the residential household objective. A separate agreement should specify who funds any anchor connection and what service the people on site receive. #cite("1")

#pagebreak()
== If verified county evidence can override provider claims

#image(tradeoff-fig, width: 100%)
#caption[*Figure 3.* New qualifying household opportunities under the same gross budget and first-phase floor. The overlay conditionally admits 13 North Ridge blocks.]

#tab((1.83fr, 1fr, 1.16fr, 1fr, .69fr), ([Mechanism], [New HH], [Gross PV], [Min. %], [Hubs]), rows("verified"))
#caption[*Table 6.* Verified overlay. The only changes to the comparison are eligible block membership and the availability of the corresponding projects.]

The overlay shifts a hub from East Corridor to North Ridge and raises PPP coverage to #value("override_count"). The county PPP still leads the cooperative by 439 households and the tender by 916. If the overlay is paired with a 50% floor, the cooperative and PPP still attain 5,311 and 5,750. The tender cannot reach the West Plains floor even before the budget binds (767 modeled opportunities versus 1,048 required). A county decision to recognize new proof needs an address record, an appeal process and a way to publish corrected eligibility without exposing personal information. A satellite-only correction under the township veto still leaves North Ridge ineligible. #cite("1", "5")

In the base PPP allocation, cable wins projects covering 3,760 households and the wireless entrant wins 1,005. The cooperative wins none in this scenario, although it can use the same published terms to bid. Under its sole award the cooperative takes responsibility for all 4,213 households and the cable operator receives no grant. These modeled bidder shares depend on the footprints and relative costs. The county should reopen the comparison when it receives conforming offers and signed commitments. #cite("10", "11", "16")

