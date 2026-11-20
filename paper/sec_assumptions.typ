#import "layout.typ": *
#import "tables.typ": *

= Assumptions and Justifications

The problem supplies block-level records but no individual addresses, no local prices and no
budget. Every quantitative assumption below is therefore stated explicitly so that a reviewer
can replace it with local data and rerun the model. Values marked as scenarios are varied in
Task 2(b).

+ *Service standard.* A qualifying connection provides at least 100 Mbps downstream and
  20 Mbps upstream over a fixed terrestrial network, in the 2026 planning year. The threshold
  follows the FCC's 2024 fixed-broadband benchmark and the county's stated planning horizon.
  #cite("2")
+ *Satellite treatment.* Satellite is not a qualifying planning technology because its
  capacity, latency and data allowances are not described in the files, but a satellite flag
  still counts in the original provider map when the strict eligibility rule is applied. This
  is deliberately conservative: it preserves the rule the county is actually bound by.
+ *Block-level homogeneity.* Households inside a census block are assumed to share a
  provider's availability status. The files report only block-level claims, so an address-level
  audit is treated as a future verification step rather than as an available input.
+ *Distance proxy.* The reported backbone distance $d_i$ is used as a radial proxy for route
  length, because the files contain no coordinates or route endpoints. Capital costs are
  proportional to this distance, which makes the proxy neutral when projects are ranked.
+ *Terrain cost factor.* The ordinal terrain index $g_i in {1, dots, 5}$ enters cost as
  $u_i = g_i - 1$ with a 10\% to 16\% uplift per level. The values are planning rates applied
  uniformly to both technologies; they preserve the ordering of blocks by construction cost.
+ *Fixed-wireless serviceability.* The share of households that a fixed-wireless site can
  actually connect falls linearly from 80\% on the easiest terrain to 55\% on the hardest.
  An independent rural study reports that installation obstructions block some willing
  households, which supports modeling serviceability below 100\%. #cite("7")
+ *Capital costs.* Fiber backhaul costs \$42,240 per mile, the 2025 U.S. aerial-construction
  median of \$8 per foot, with \$980 per household for last-mile distribution. Fixed wireless
  uses \$5,500 per backhaul mile and \$28,000 per site. All values are expressed in 2026
  dollars. #cite("8")
+ *Operating costs.* Annual maintenance is 1.8\% of fiber capital and 3.5\% of wireless
  capital; it is discounted over ten years at a 3\% real rate. The rates follow county
  broadband planning practice and are varied from 75\% to 150\% in the sensitivity analysis.
  #cite("9")
+ *Remaining budget.* The county has \$11.0 million of remaining broadband funds, the scale
  that the problem narrative implies. Because no budget is supplied, we report plans at
  \$8, \$9, \$11 and \$13 million so that the recommendation is not an artifact of this
  value.
+ *Township access floor.* Every township must reach at least 25\% household access in the
  first phase. The floor lifts the three lowest modeled baselines and stays below the 28.29\%
  ceiling that is attainable in North Ridge after a block-level reform, so it is feasible in
  the reform scenario; a 50\% higher target is also tested.
+ *Eligibility scenarios.* We evaluate the strict township-wide veto exactly as stated, a
  block-level reform in which only blocks marked served are excluded, and a verified overlay
  in which county evidence can override an incorrect flag. These are policy scenarios, not
  claims about the organizer's final rule.
+ *Lease economics.* Wholesale access to a county hub is priced at \$4,800 per provider-hub
  year, which is the revenue needed to recover most hub maintenance. Open-access middle-mile
  guidance motivates the arrangement but does not provide Hallowell's price. #cite("16")
+ *Demand and benefit.* Subscriptions and household counts are static, so benefit is measured
  as new qualifying household opportunities. Effective use is treated separately, because the
  files contain no usage, price or device information. #cite("7", "14")
+ *Tie-breaking.* The deployment model maximizes qualifying coverage and then minimizes
  life-cycle cost among coverage-maximal plans, so results do not depend on arbitrary solver
  tie-breaking.
