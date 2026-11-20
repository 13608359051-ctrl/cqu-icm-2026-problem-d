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

#fig(tornado-fig, 5, width: 94%)[Sensitivity of new qualifying household opportunities to four uncertain inputs.
Bars show the change from the 4,213-opportunity base plan over each plausible range.]

*The dominant parameter is fixed-wireless serviceability.* Figure 5 plots the comparison: a
±10 percentage-point change
moves new coverage from 3,892 to 4,553 households, a range of 661. The full fiber-cost range,
from the aerial first quartile (\$4.90 per foot, or \$25,872 per mile) to the underground median
(\$18 per foot, or \$95,040 per mile), moves coverage from 4,342 to 4,047, a range of 295. The
two ranges are not directly comparable, because serviceability is varied by 20 percentage
points while fiber cost spans a 3.7-fold price range, yet serviceability still moves coverage
more than twice as much. Its influence is also comparable to raising the budget from \$8
million to \$14 million (a 598-household range). In marginal terms, 661 households are worth
roughly \$3.3 million of additional budget at the observed program rate of about 200 households
per million dollars. #cite("7", "8")

The technology mix responds in an economically sensible way. Lower fiber cost switches the
East Corridor block 420010000027 from fixed wireless to fiber; higher wireless serviceability
switches block 420010000024 in the other direction. The coverage-maximal plan keeps the same
minimum township access rate of 28.10\% in most runs because the floor is not binding at the
margin, but the underground-median and $-10$ point wireless cases lower it to 26.89\% and
27.54\%, respectively, which shows where the floor starts to matter. Maintenance cost has the
smallest effect: a 25\% change in the maintenance rate moves coverage by only 49 to 46
households, because discounted maintenance is a modest share of life-cycle cost.

The sensitivity has a clear policy reading. Because wireless serviceability is the largest
source of plan uncertainty, the county should measure it directly before awarding construction
contracts: a small installation and line-of-sight survey costs far less than the 661-household
swing it resolves. Fiber price uncertainty is better managed through competitive bidding, and
budget uncertainty through staged awards. The procurement ranking in Task 3 is stable across
the tested budget and maintenance ranges, so it is not driven by the most fragile parameter;
Figure 8 reports that ranking across scenarios. #cite("7", "8")

*How much does the last household cost?* Figure 6 turns the budget runs into a coverage-cost
frontier. Coverage rises from 3,836 opportunities at \$8 million to 4,213 at \$11 million and
4,434 at \$14 million. The marginal cost is #value("marginal_8_11") per added household between
\$8 and \$11 million and #value("marginal_11_14") between \$11 and \$14 million, against an
average life-cycle cost of #value("average_cost") per household. The last few hundred
households therefore cost about five times the average, which is the quantitative answer to
whether the county needs "a little more money": beyond roughly \$11 million, additional funds
buy progressively fewer new connections, so the case for more budget is weaker than the case
for changing the eligibility rule. At the recommended budget the plan reaches
#value("pool_share") of the 5,414-household block-eligible pool.

#fig(pareto-fig, 6)[(a) Coverage-cost frontier of the block-reform plan and (b) marginal cost per
added household for the two budget segments, compared with the average life-cycle cost.]

#answer[Fixed-wireless serviceability is the uncertain parameter that most strongly affects
the deployment plan: a plausible ±10 percentage-point range changes coverage by 661
households, versus 295 for the full fiber-cost range and 95 for a 25\% change in maintenance.
The county should therefore verify wireless serviceability first, and treat fiber cost as a
bidding outcome rather than a planning assumption.]
