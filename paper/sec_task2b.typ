#import "layout.typ": *
#import "tables.typ": *

= Task 2(b): Sensitivity analysis

The deployment plan depends on parameters that the files do not contain and that field work
would have to confirm. We vary one parameter at a time from the block-eligibility, 25\%-floor
base case, holding every other assumption fixed, and re-solve the full model. Two of the
parameters are engineering quantities: the fiber route cost and the share of households that a
fixed-wireless site can actually connect. Two are financial or policy quantities: maintenance
cost and the size of the remaining budget. Table 6 reports the resulting plan size,
life-cycle cost, technology mix and minimum township access rate.

#tabblock(6, [One-at-a-time sensitivity of the block-reform plan under the 25\% floor. F/W counts
selected fiber and fixed-wireless projects; the change is new household opportunities relative
to the base plan.], (2.2fr, .8fr, .92fr, .88fr, .82fr, 1.02fr), ([Changed input], [New HH], [Life-cycle cost], [F / W], [Min. \%], [Change vs base]), rows("sensitivity"))

#fig(tornado-fig, 5, width: 94%)[Change in new qualifying opportunities from the direct
base plan at the tested endpoints. A higher route or maintenance cost reduces coverage.
A higher budget or wireless serviceability increases it.]

*Wireless serviceability produces the largest coverage range in these tests.* Shifting each
terrain class by ±10 percentage points changes the optimum from 3,892 to 4,553 opportunities,
a span of #value("wireless_span"). The local shares are unknown. The range represents a
possible change in field conditions and has no assigned probability. Changing the fiber
route cost from the aerial first quartile (\$4.90/ft) to the underground median (\$18/ft)
changes coverage from 4,342 to 4,047, a span of #value("fiber_span"). These two cost
benchmarks represent different construction methods. #cite("7", "8")

The engineering choices change as well. With low fiber costs, East Corridor block
420010000027 switches from wireless to fiber. With higher wireless serviceability, block
420010000024 switches from fiber to wireless. At the underground median, the minimum
township rate falls to 26.89\%. With wireless serviceability reduced by ten points it is
27.54\%. Both exceed the 25\% floor. Scaling direct-plan maintenance costs from 75\% to
125\% of base changes coverage by 95 opportunities across the two endpoints.

*What additional budget buys.* At budgets of \$8, \$11 and \$14 million, the optimized
direct plans add 3,836, #value("t2_main_hh") and 4,434 opportunities, respectively.
Each additional million dollars of budget therefore buys 125.7 opportunities on average
in the first interval and 73.7 in the second. Using actual plan expenditures, the
corresponding incremental costs per added opportunity are #value("marginal_8_11") and
#value("marginal_11_14"). The base plan reaches #value("pool_share") of the 5,414
households in the block-eligible pool.

#fig(pareto-fig, 6)[(a) Each point is a separately optimized direct plan at the indicated
budget. (b) Actual incremental expenditure per added household across
each budget interval, with the base plan's average cost for comparison.]

#answer[Field installation and line-of-sight checks would help narrow the largest tested
engineering uncertainty. Obtain route quotes for fiber at the same time. Section 7 tests
whether revised wireless serviceability and hub route lengths change procurement choices.]
