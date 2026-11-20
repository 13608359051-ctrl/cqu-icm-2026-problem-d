#import "layout.typ": *
#import "tables.typ": *

= Model Evaluation

== Strengths and limits of the evidence

*Eligibility.* All six townships have a served flag and three fall below the modeled floor
before construction. Additional capital cannot fix that legal conflict. Block-level reform
opens 47 originally unserved blocks, while any extension to the disputed northern blocks
requires separate authorization and address evidence. #cite("1", "3")

*Engineering.* The data identify neither routes, tower sites nor individual addresses.
Regional unit costs and terrain-specific wireless shares define planning scenarios. Fiber
offers aim to serve a full block and wireless offers credit a terrain-dependent fraction;
either requires field verification. Wireless serviceability produces the largest coverage
range among the engineering inputs tested in Task 2. Under shared backhaul the lateral proxy
also determines which providers can reach a block, and a longer route can reverse the
procurement recommendation. #cite("7")

*Finance and bidding.* The comparison holds the budget, service standard, horizon and floor
constant. The \$11 million ceiling, ten-year horizon, lease fee, reach limits and bidder
discounts are planning assumptions. Results reflect both ownership and the offers available
under each mechanism. Confirm voluntary bidding areas, actual build costs, signed leases and
the maintenance reserve before award.

*Household benefit.* The objective counts additional opportunities to order 100/20 service.
Prices, installation, adoption and effective use determine the benefit realized at home.
The South Hollow data motivate collecting those outcomes before choosing a use-based
equity floor. The present-value model also omits construction sequencing and future entries
or exits by operators.

== Validation and reproducibility

We verify four things independently. First, every reported township count and rate is
recomputed from the raw block file. Second, each mixed-integer solution is checked for
eligibility, budget and floor compliance directly from its vector, not from solver status.
Third, the main deployment and mechanism results are rebuilt by an independent solver script;
the direct result is also cross-checked by enumeration of township-level Pareto points. Fourth,
small cases constructed by hand exercise the budget, equity and tie-breaking constraints. The
reported optimality gaps are zero for all feasible runs. Independent numerical checks establish consistency within these scenarios. Field surveys
and binding offers are needed to test the inputs that drive the procurement ranking. #cite("13")
