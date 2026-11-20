#import "layout.typ": *
#import "tables.typ": *

= Task 2(a): Deployment optimization

== Inputs and engineering cost model

Each block $i$ reports $H_i$ households, a backbone distance $d_i$ in miles and a terrain
index $g_i = 1, dots, 5$; we write $u_i = g_i - 1$. The recorded distance is used as a radial
route proxy because the files contain no coordinates, route endpoints, adjacent-block
relations or tower sites. Engineering siting, pole access, spectrum and usable line of sight
still require field work, and no route mileage is obtained by summing road segments. #cite("1", "6")

A fiber project serves $h_(i F) = H_i$ households. A fixed-wireless project is assumed to
qualify $h_(i W) = floor(p_(g_i) H_i)$ households, with $p = (0.80, 0.75, 0.70, 0.62, 0.55)$
from the easiest to the hardest terrain. The qualifying locations are assumed to meet the same
100/20 standard. There are no line-of-sight surveys or site-loading data for the county; a
rural wireless study found that installation obstructions blocked some willing households,
which is why serviceability is modeled below one. #cite("7")

Backhaul capital $K^B$ and last-mile capital $K^L$ in 2026 U.S. dollars follow (3)-(4):

$ K^B_(i F) = 42,240 d_i (1 + 0.16 u_i), quad K^L_(i F) = 980 H_i (1 + 0.10 u_i), $
$ K^B_(i W) = 5,500 d_i (1 + 0.10 u_i), quad K^L_(i W) = 28,000 (1 + 0.08 u_i) + 480 h_(i W). $

The fiber route rate is \$8 per foot, the 2025 U.S. aerial-construction median, converted at
5,280 feet per mile and expressed in 2026 dollars. The \$980 per-household allowance covers
local distribution and the drop; it exceeds the drop-only medians in the same survey. The
wireless site and backhaul values assume suitable mounting sites and need local quotes. The
parameter register records the basis of every scenario input. #cite("8", "9")

As a check, fiber to North Ridge block 420010000008 uses $H_i = 85$, $d_i = 1.1$ miles and
$g_i = 2$: backhaul is \$53,898, last mile is \$91,630 and discounted maintenance adds
\$22,345, for a life-cycle cost of \$167,873 over 85 modeled opportunities. The selected direct
portfolio includes this block. Figure 4 shows the two service paths schematically; the cost of
each path is driven by distance and terrain as in (3)-(4).

#fig(model-fig, 4)[Candidate service paths. The links and hub are schematic: the attachment has no
coordinates, tower locations or route endpoints.]

== Decision variables, objective and constraints

For each action $a$ (a technology in a block, or a hub-dependent offer) let $x_a in {0,1}$
indicate selection and let $h_a$ be its modeled qualifying household count. A county-hub offer
also specifies a provider and hub $j(a)$, with $y_j in {0,1}$ for hub commissioning. Total
coverage and life-cycle cost are $G = sum_a h_a x_a$ and $C = sum_a c_a x_a + sum_j c_j y_j$.
The objective is lexicographic: first maximize $G$ to find $G^*$, then minimize $C$ subject to
$G = G^*$. This ordering matches the county's stated coverage goal, uses cost only to break
coverage ties, and avoids trading households for dollars at an arbitrary exchange rate. The
minimum-budget variant instead minimizes $C$ subject to the access floor, allowing coverage to
vary, which answers whether the requirements can be met at all. #cite("6")

With budget $B$, annuity factor $A = sum_(s=1)^(10) (1.03)^(-s)$, maintenance rate $r_a$ and
eligible set $E_i$ per block, the model is (5)-(7):

$ A = sum_(s=1)^(10) (1.03)^(-s), quad c_a = K^B_a + K^L_a + A r_a (K^B_a + K^L_a), $
$ C <= B, quad sum_(a : i(a)=i) x_a <= E_i quad forall i, $
$ G_t = sum_(a : i(a) in t) h_a x_a, quad L_t = ceil(theta H_t), quad b_t + G_t >= L_t quad forall t. $

The scenario uses $B = 11$ million 2026 dollars, a ten-year horizon, a 3\% real discount rate,
and annual maintenance of 1.8\% of capital for fiber and 3.5\% for wireless. The floor is
$theta = 0.25$ in the first phase and $theta = 0.50$ in the higher-target test. The
terrestrial-claim proxy $b_t$ is disjoint from newly eligible projects, so the post-plan access
fraction is $(b_t + G_t)/H_t$ and the remaining shortfall is $max(0, L_t - b_t - G_t)$; $b_t$ is
a claimed-availability baseline and is not a subscription rate. The inputs specify neither a
budget nor a floor, which is why both are treated as policy scenarios.

The 25\% phase-one floor is a policy target rather than an estimate. It lies above the three
lowest claimed-access baselines (17.66\%, 17.84\% and 19.27\%) and below the 28.29\% ceiling
that North Ridge can reach after block reform, so it is binding but attainable. We also solve
the model with a 0\% floor and a 50\% floor to show how the choice changes the answer. Only one
technology is allowed per block: if a block is eligible for both fiber and fixed wireless, the
lower cost per qualifying household dominates, and splitting a project between technologies
only adds duplicate backhaul, so a single-technology choice is without loss of generality at
this scale.

The eligibility ceiling is $E_i = 1 - max_(k in t(i)) M_k$ under the strict township-wide
rule; the block reform uses $E_i = 1 - M_i$; the verified overlay uses
$E_i = max(1 - M_i, V_i)$, where $V_i = 1$ for the 13 North Ridge satellite-coded blocks in
the scenario. Under the original rule, even correcting all 13 flags leaves a veto from the
remaining four blocks.

== Solution method and verification

The model is a mixed-integer linear program. Under the block reform it has at most 94 direct
action variables, and under the verified overlay at most 120; each stage solves in seconds with
SciPy's HiGHS solver, which reports zero applicable optimality gaps for every feasible run. We
verify eligibility, the budget and township totals directly from each solution vector, and a
separate enumeration of township-level Pareto points independently reproduces the direct
results. Small hand-solvable cases exercise the budget, equity and tie-break logic. #cite("13")

== Feasibility under the strict rule

Under the strict rule the six townships have 17, 12, 13, 7, 15 and 9 served blocks, so every
$E_i$ group is zero and the only feasible construction allocation is zero coverage. At the
25\% floor that allocation is also insufficient: North Ridge is short 157 households, West
Plains is short 120 and River Bend is short 204, while the other three townships clear the
floor at baseline. Raising the construction budget alone cannot remove the shortfall because
the binding constraint is eligibility, not money. With the floor removed, the strict solution
is feasible and adds zero households. The infeasibility therefore has a single identified
source: the township-wide veto converts one served flag into a zero ceiling for every block
in the township. #cite("5")

== Eligibility reform and the deployment plan

Block-level eligibility makes the 25\% floor feasible. The least-cost feasible package adds
#value("min_funding_new") opportunities for #value("min_funding"), which is the minimum
public outlay that satisfies every township floor. The largest affordable coverage-maximal
package adds #value("t2_main_hh") opportunities at a life-cycle cost of #value("t2_main_cost")
using 12 fiber and 32 fixed-wireless projects. The township gains, in Table 2 order, are 223,
912, 260, 920, 816 and 1,082 households, and the minimum post-deployment access proxy is
28.10\%, in North Ridge. Table 4 summarizes the feasibility tests across rules and floors.

#tabblock(4, [Feasibility and optimal plans by eligibility rule and access floor. F/W is the
number of selected fiber and fixed-wireless projects; minimum access includes the
terrestrial-claim proxy.], (2.05fr, .62fr, .75fr, 1.02fr, 1.05fr, .7fr, .72fr), ([Rule], [Floor], [Status], [New HH], [Lifecycle cost], [F/W], [Min. \%]), rows("feasibility"))

Block reform alone cannot reach the 50\% target. Even fiber to all 227 map-unserved North Ridge
households gives only $(377+227)/2135 = 28.29\%$. If the 13 satellite-coded blocks become
eligible through verified evidence, the 50\% floor becomes feasible: the minimum outlay is
#value("verified_50_min_funding"), while at the full budget the model adds 5,311 opportunities
and every township reaches at least 52.13\%. A stress test that credits only 75\% of the
households in a credited block leaves North Ridge with at most 509 qualifying opportunities
after block reform, against 534 needed for the floor, so the plan becomes infeasible; this is
the quantitative form of the uncertainty carried over from Task 1.

*The recommended portfolio.* Table 5 disaggregates the 4,213-opportunity partnership plan by
township and technology, including each town's share of county hub capital and discounted hub
maintenance. The plan uses 28 fiber and 12 fixed-wireless projects. West Plains carries the
highest cost per household (\$2,881) because its eligible blocks are distant and numerous, yet
it also receives the largest share of the coverage; the objective is total qualifying coverage
under the equity floor, not cost-efficiency within each township.

#tabblock(5, [Recommended county partnership portfolio by township. F / W counts fiber and
fixed-wireless projects; gross present value includes each town's hub capital and discounted
hub maintenance; USD/HH is gross cost per new qualifying household.], (1.5fr, .78fr, .85fr, .92fr, .95fr, .95fr), ([Township], [F / W], [Fiber HH], [Wireless HH], [Gross PV], [USD / HH]), rows("deployment"))

#answer[The budget, eligibility and equity requirements *cannot be met simultaneously under
the strict rule*, and the source of infeasibility is the township-wide eligibility veto, not
the budget. Block-level eligibility plus the 25\% floor is feasible with a minimum outlay of
#value("min_funding") and can add up to #value("t2_main_hh") opportunities at
#value("t2_main_cost") under an #value("budget") budget. A 50\% floor requires verified
coverage evidence; with it, the plan reaches 5,311 opportunities.]
