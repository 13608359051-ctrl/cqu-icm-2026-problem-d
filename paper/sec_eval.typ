#import "layout.typ": *
#import "tables.typ": *

= Model Evaluation

== Strengths

*The analysis separates what is observed from what is inferred.* Map claims, subscription counts
and road signals are used as three different kinds of evidence, and the reclassification result
is reported as a bounded exposure set with explicit scenarios rather than as a point forecast.
This is the main reason the Task 1 conclusion is robust: even the most favorable challenge
outcome does not unlock funding under the current rule. #cite("1", "3")

*Infeasibility is attributed to a specific constraint.* Rather than reporting a failed solve,
the model identifies the township-wide eligibility veto as the binding constraint, proves that
budget increases cannot repair it, and then evaluates the two rule changes that would. This
lets the county distinguish a legal barrier from a fiscal one.

*The mechanisms are compared on identical terms.* The same budget, period, service standard,
eligibility and equity floor are applied to all three approaches, and the lease treatment in
the partnership is explicit: gross cost must fit the budget and rents are credited afterward.
Differences in coverage can therefore be attributed to the mechanism rather than to
bookkeeping.

*Uncertainty is tested where it matters.* The plan is re-solved over plausible ranges of the
two engineering parameters, the maintenance rate and the budget, and the procurement ranking is
checked against hub cost, budget and maintenance variations. The dominant parameter,
fixed-wireless serviceability, is identified and translated into a concrete measurement
recommendation.

*The results are reproducible.* All inputs are checked for key uniqueness, byte-identical
duplicates and field ranges; the mixed-integer programs are solved to zero optimality gap; and
the deployment and mechanism results are independently rebuilt, including a separate Pareto
enumeration by township and hand-solvable test cases. #cite("13")

== Weaknesses and limitations

*The data are synthetic and spatially coarse.* There are no coordinates, routes, tower sites or
address records, so distances are radial proxies and service paths are schematic. Cost
coefficients are regional benchmarks, not local quotes. The model is a planning tool; it is
not a substitute for engineering design.

*Households are treated as homogeneous within a block.* A block is credited as covered when the
model selects a project, even though some addresses inside it may remain unserviceable. The
fixed-wireless serviceability probabilities are assumptions supported by the literature, not
measurements, and the address audit in Task 1 is the natural remedy. #cite("7")

*Benefit is measured as orderable opportunities, not welfare.* The model does not include
take-up, retail prices, consumer surplus or the value of specific work and school activities.
The effective-use framework in Section 8 is deliberately separate from the optimization
because the files cannot support it. A use-based or subscription-based equity floor would
change which township is binding, as the South Hollow comparison shows.

*Several policy inputs are scenarios rather than facts.* The budget, the 25\% floor, the lease
rate and the verified-overlay assumption are all stated explicitly and varied where possible,
but the county must confirm them before the recommendation is executed. The bidder cost
multipliers (70\%/90\% and 75\%/95\% of direct cost) determine who wins which project and could
not be varied without observed bid data; they are the largest untested assumption in Task 3.

*The model is static and single-period.* It does not represent construction sequencing,
inflation, technological change, competitive entry or the county's cost of capital, and it
treats providers' bids as parametric. A dynamic or auction-based extension is left for future
work.

== Validation and reproducibility

We verify four things independently. First, every reported township count and rate is
recomputed from the raw block file. Second, each mixed-integer solution is checked for
eligibility, budget and floor compliance directly from its vector, not from solver status.
Third, the main deployment and mechanism results are rebuilt by an independent solver script;
the direct result is also cross-checked by enumeration of township-level Pareto points. Fourth,
small cases constructed by hand exercise the budget, equity and tie-breaking constraints. The
reported optimality gaps are zero for all feasible runs. The parameter registers, result
tables and scripts are supplied with the submission so that a reviewer can reproduce every
number. #cite("13")

Two extensions would strengthen the analysis most. The first is an explicit value-of-information
calculation for the address audit (Section 4), which would price the evidence as an option rather
than as a cost. The second is a subscription-based or use-based equity constraint, which would
reallocate the plan toward South Hollow and test whether the county's stated floor is measuring
what the problem intends.
