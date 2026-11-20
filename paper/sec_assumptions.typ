#import "layout.typ": *
#import "tables.typ": *

= Assumptions and Justifications

The files provide block records. The budget, planning horizon, serviceability rates and physical
network are county planning scenarios. Sections 5–7 identify the inputs varied in each test.

+ *Service standard.* We use the FCC's 2024 benchmark of 100 Mbps downstream and 20 Mbps
  upstream for a fixed terrestrial offer. The undated county data are evaluated in an
  assumed 2026 planning year. #cite("2")
+ *Satellite treatment.* Satellite is not a qualifying planning technology because its
  capacity, latency and data allowances are not described in the files, but a satellite flag
  still counts in the original provider map when the strict eligibility rule is applied. This
  is deliberately conservative: it preserves the rule the county is actually bound by.
+ *Block-level homogeneity.* Households inside a census block are assumed to share a
  provider's availability status. The files report only block-level claims, so an address-level
  audit is treated as a future verification step rather than as an available input.
+ *Distance proxy.* Reported distance to the backbone approximates a direct route. The files
  contain no coordinates or route endpoints. Differences in direction or detours can change
  project costs, bidder reach and the mechanism ranking.
+ *Terrain costs.* For each step above terrain class 1, we assume increases of 16\% for
  fiber backhaul and 10\% for its last mile. Wireless backhaul increases by 10\% and its
  fixed site cost by 8\% per step. Section 5 gives the full cost equations.
+ *Fixed-wireless serviceability.* We assume that 80\%, 75\%, 70\%, 62\% and 55\% of
  households can receive the design tier across the five terrain classes. Installation
  obstructions observed in a rural study motivate this ordering. The assumed county
  percentages and their ±10 percentage-point range need field testing. #cite("7")
+ *Capital costs.* Fiber backhaul costs \$42,240 per mile, the 2025 U.S. aerial-construction
  median of \$8 per foot. We assume \$980 per household for local fiber distribution and
  the drop, \$5,500 per wireless backhaul mile and \$28,000 per wireless site. The 2026
  planning scenario carries survey prices forward without an inflation adjustment. #cite("8")
+ *Operating costs.* Annual maintenance allowances are 1.8\% of capital for fiber and 3.5\%
  for wireless. We use a ten-year horizon and a 3\% real discount rate as common planning
  assumptions. Direct-plan tests scale maintenance by 0.75–1.25 and mechanism comparisons
  by 0.75–1.50. #cite("9")
+ *Remaining budget.* The grant balance is unknown. We test a common \$11 million budget
  for capital and discounted maintenance. Direct-plan budget tests span \$8–14 million,
  with matched procurement comparisons at \$9 million and \$13 million.
+ *Township access floor.* Every township must reach at least 25\% household access in the
  first phase. The floor lifts the three lowest modeled baselines and stays below the 28.29\%
  ceiling that is attainable in North Ridge after a block-level reform, so it is feasible in
  the reform scenario; a 50\% higher target is also tested.
+ *Eligibility scenarios.* We evaluate the strict township-wide veto exactly as stated, a
  block-level reform in which only blocks marked served are excluded, and a verified overlay
  in which county evidence can override an incorrect flag. These are policy scenarios, not
  claims about the organizer's final rule.
+ *Lease economics.* Wholesale access to a county hub is priced at \$4,800 per provider-hub
  year as a scenario assumption. Its share of maintenance depends on lease uptake. Open-access middle-mile
  guidance motivates the arrangement but does not provide Hallowell's price. #cite("16")
+ *Demand and benefit.* Subscriptions and household counts are static, so benefit is measured
  as new qualifying household opportunities. Effective use is treated separately, because the
  files contain no usage, price or device information. #cite("7", "14")
+ *Tie-breaking.* The deployment model maximizes qualifying coverage and then minimizes
  life-cycle cost among coverage-maximal plans. Portfolios tied on both quantities would
  be equally optimal.
