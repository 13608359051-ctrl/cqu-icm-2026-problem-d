#import "layout.typ": *
#import "tables.typ": *

#pagebreak()
= Task 2. Deployment optimization

== Inputs and engineering assumptions

Each block $i$ has $H_i$ households, a reported distance $d_i$ to the backbone in miles and terrain difficulty $g_i = 1, dots, 5$. We use the recorded distance as a radial route proxy and write $u_i = g_i - 1$. Figure 2 shows the modeled links. Blocks are candidate service areas. Engineering sites, routes, pole access, spectrum and usable line of sight still need field work. No route mileage is measured by summing surveyed road segments. #cite("1", "6")

#image(model-fig, width: 100%)
#caption[*Figure 2.* Candidate service paths. The links and hub are schematic. The attachments have no coordinates, adjacent blocks, towers or route endpoints.]

A fiber project passes $h_(i F) = H_i$ households. Fixed wireless (W) qualifies $h_(i W) = floor(p_(g_i) H_i)$, with $p = (0.80, 0.75, 0.70, 0.62, 0.55)$ from easiest to hardest terrain. The code multiplies by integer percentages and divides by 100, rounding down. The qualifying locations are assumed to meet the same 100/20 standard. The county has no line-of-sight surveys or site loading data. A rural Missouri wireless study found that installation obstructions blocked some willing households, supporting separate measurement of serviceability and demand. #cite("7")

For a direct connection, backhaul capital $K^B$ and last-mile capital $K^L$ in 2026 US dollars are

$ K^B_(i F) = 42,240 d_i (1 + 0.16 u_i), quad
  K^L_(i F) = 980 H_i (1 + 0.10 u_i). $
$ K^B_(i W) = 5,500 d_i (1 + 0.10 u_i), quad
  K^L_(i W) = 28,000 (1 + 0.08 u_i) + 480 h_(i W). $

The fiber route benchmark is \$8/ft, the 2025 US aerial-construction median, converted at 5,280 ft/mi and carried into the 2026 price basis. The \$980 last-mile allowance includes local distribution as well as the drop. It exceeds that survey's drop-only medians. Wireless backhaul and site costs assume suitable mounting sites and equipment and need local quotes. The cost register gives the basis for each scenario input. #cite("8", "9")

For example, fiber to North Ridge block 420010000008 uses $H_i=85$, $d_i=1.1$ mi and $g_i=2$. The rounded backhaul cost is \$53,898 and the rounded last-mile cost is \$91,630. Discounted O&M adds \$22,345, giving \$167,873 for 85 modeled opportunities. The selected direct portfolio includes this block.

#pagebreak()
== Decisions, objective and constraints

For action $a$ in block $i(a)$, let $x_a in {0, 1}$ denote selection and $h_a$ its modeled qualifying household count. A partnership offer can also specify a provider and a county hub $j(a)$. Let $y_j in {0,1}$ indicate hub commissioning. Write $G = sum_a h_a x_a$ and total lifecycle cost $C = sum_a c_a x_a + sum_j c_j y_j$. First find $G^* = max G$. Then minimize $C$ with $G=G^*$ to break coverage ties. The minimum-budget test instead minimizes $C$ under the same access and eligibility constraints, allowing the number covered to vary.

The scenario uses $B = 11$ million 2026 dollars. Year-zero capital and ten years of operating and maintenance costs (O&M) are discounted at 3% real. Annual O&M is assumed to be 1.8% of capital for fiber and 3.5% for wireless, reflecting site, equipment and maintenance costs. These are scenario rates. The 25% floor improves the three lowest modeled baselines while keeping the target below the North Ridge block-reform ceiling of 28.29%. The inputs specify neither a budget nor a minimum floor. #cite("9")

$ A = sum_(s=1)^10 (1.03)^(-s), quad
  c_a = K^B_a + K^L_a + A r_a (K^B_a + K^L_a). $
$ C <= B, quad sum_(a : i(a)=i) x_a <= E_i quad forall i. $
$ G_t = sum_(a : i(a) in t) h_a x_a, quad
  L_t = ceil(theta H_t), quad b_t + G_t >= L_t quad forall t. $

The code rounds capital components to whole dollars, then calculates and rounds O&M PV from those values. $b_t$ is the terrestrial-claim proxy in Table 1 and is disjoint from eligible projects. The access fraction is $(b_t+G_t)/H_t$ and the remaining shortfall is $max(0, L_t-b_t-G_t)$. We use $theta=0.25$ in the first phase and $theta=0.50$ for the higher target. The equity counterfactual removes only the floor inequality.

The strict rule uses $E_i=1 - max_(k in t(i)) M_k$, including satellite flags. The block reform sets $E_i=1-M_i$. For the verified overlay, $E_i=max(1-M_i,V_i)$, where $V_i=1$ for the 13 North Ridge satellite blocks in the scenario. Verification assumes authoritative address evidence and permission to apply it. Under the original rule, even updating those 13 flags leaves a veto from the remaining four.

The block reform starts with at most 94 direct action variables and the verified overlay at most 120. SciPy's HiGHS MILP solver reports zero applicable optimality gaps for the feasible runs. We check eligibility, the budget and township totals from the solution vectors. A separate Pareto enumeration by township independently checks direct results. Small cases exercise the budget, equity and tie-break logic. #cite("13")

#pagebreak()
== Feasibility and the effect of rule changes

Under the strict rule, the six served-block counts are 17, 12, 13, 7, 15 and 9 in Table 1 order. All six $E_i$ groups are zero, so the only possible construction allocation is zero. At the 25% floor that allocation is insufficient even under the full-block proxy. North Ridge is short 157 households, West Plains 120 and River Bend 204. The other three clear the floor at baseline. Raising the construction budget alone cannot remove these deficits. With the floor removed, the strict solution is feasible and adds zero households.

Under block eligibility the 25% floor becomes feasible. The least-cost feasible package adds #value("min_funding_new") opportunities at #value("min_funding"). The largest affordable direct package adds #value("t2_main_hh") for #value("t2_main_cost") using 12 fiber and 32 wireless projects. The township gains in Table 1 order are 223, 912, 260, 920, 816 and 1,082. The minimum post-deployment access proxy is 28.10%, in North Ridge.

Block reform alone cannot reach 50%. Even fiber to all 227 map-unserved North Ridge households would yield $(377 + 227) / 2135 = 28.29%$. If the 13 satellite-coded blocks become eligible, the higher floor is feasible at #value("verified_50_min_funding"). At the full budget the model adds 5,311 and each township reaches at least 52.13%. In the 75% baseline stress, replace each credited block count $H_i$ in $b_t$ with $floor(0.75 H_i)$. This leaves North Ridge with at most 509 qualifying opportunities after block reform, against 534 needed.

== Sensitivity to build conditions

#tab((2.95fr, 1fr, 1.05fr, .78fr, .98fr, 1fr), ([Changed input], [New HH], [Gross PV], [F / W], [Min. %], [Moves]), rows("sensitivity"))
#caption[*Table 3.* Block eligibility, 25% floor, one change at a time. Gross PV is lifecycle present value in 2026 dollars. F/W counts projects. Moves are block–technology pairs added and removed relative to the direct base; the project CSV provides exact locations.]

The fiber range uses the aerial first quartile (\$4.90/ft or \$25,872/mi) and underground median (\$18/ft or \$95,040/mi). Wireless serviceability shifts by ten percentage points each way. This changes coverage by 661 households, versus 295 across the fiber range. Fiber cost has the larger effect on the technology mix: low fiber cost switches East Corridor block 420010000027 from wireless to fiber. At higher wireless serviceability, block 420010000024 switches from fiber to wireless. Separate \$8–14m budget and 0.75–1.25 O&M stress runs shift coverage by 598 and 95, respectively. #cite("7", "8")

