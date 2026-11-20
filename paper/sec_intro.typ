#import "layout.typ": *
#import "tables.typ": *

= Introduction

== Executive Summary

Hallowell County's broadband problem is not only a funding problem. Under the subsidy rules
assumed here, a single reported served flag makes an entire township ineligible, and the
county must also decide whether a household can actually order, afford and use a qualifying
connection. The supplied files contain block-level coverage claims and subscription counts;
they do not contain individual service offers or records of effective use. #cite("1")

We count each household once, use road-segment measurements only as a diagnostic, and solve
the grant allocation problem with and without the township-wide eligibility veto. The
alternative is a staged program for unserved blocks with a 25\% minimum township access floor
in the first phase. #value("executive_mechanism") The board can begin by collecting
verifiable evidence while it preserves the budget for legally eligible construction; the
memorandum in Section 11 states the decision conditions. Figure 1 summarizes the logic of the
analysis: the strict rule determines the current allocation, and every later result is
conditional on a rule change.

#fig(workflow-fig, 1)[Workflow of the analysis. The strict eligibility rule determines the current
allocation; the deployment and mechanism comparisons that follow are conditional on a
rule change.]

== Background

Broadband has become a prerequisite for work, schooling and health care, yet rural
households are still served by the technology that happens to reach them rather than by the
technology they need. In the problem, subsidy programs distribute
billions of dollars through grants and subsidized loans, and eligibility is decided by the
coverage maps that providers submit. When those maps overstate service, public money is
withheld from the places that need it most. Providers have an incentive to report service
they can technically offer, while residents experience the service they can actually buy.
#cite("1", "3")

Hallowell County illustrates the problem in a compact setting. The county has about 48,000
residents across 620 square miles of farmland and small towns. A regional cooperative, a
national cable provider and a fixed-wireless startup have all received support, yet reported
coverage and residential experience diverge. The dispute is concentrated in three places:
the northern townships, where the cable provider's map shows service but residents report
that only satellite is available; the eastern logistics corridor, where the cooperative's
fiber network ends near warehouses that employ shift workers; and the southern townships,
where publicly funded fixed-wireless stations sit idle for most of the day. #cite("1", "2", "3")

== Problem restatement

We use the supplied block, subscription and road files to answer five connected questions.

*Task 1.* Assess the discrepancy in the northern townships, estimate how many households
could be reclassified from served to unserved, separate observation from inference and
describe the uncertainty. Analyze the effect of misclassification on subsidy allocation and
on affected households, compare accepting the map with filing a challenge (including its
cost, timing and outcome), and explain the implications for residents, the cooperative, the
cable provider and the county government.

*Task 2.* (a) Build an optimization model that selects where to deploy fiber, fixed wireless
or both under limited funds, terrain- and distance-dependent costs, a minimum township access
level and the assumed eligibility rule. State and justify the objective and constraints,
propose a solution method for the problem's scale, test whether the budget, eligibility and
equity requirements can hold simultaneously, and diagnose any infeasibility. (b) Identify
the uncertain parameter that most strongly affects the plan, quantify plan and outcome changes
over a plausible range, and compare its influence with a second parameter.

*Task 3.* Compare a sole award to the regional cooperative, a competitive tender favoring the
lowest cost per household, and a county-owned backhaul partnership leased to any provider.
Use the Task 2 plan as the benchmark, apply the same budget, period, service standard and
eligibility requirements, include backhaul, last-mile and operating costs, address
infeasibility, recommend an approach, quantify the trade-offs and identify who benefits and
who pays. Test whether verified county evidence that can override provider claims changes the
recommendation.

*Share Your Insights.* Explain how the county should assess whether funded projects serve
their intended users, and what evidence would distinguish limited demand from barriers to
use. Define a benefit measure, identify the township that benefits most from the recommended
plan, and reoptimize without the equity constraint to test whether the same township still
benefits most.

*Memorandum.* Write a one-page memo to the Hallowell County Board of Commissioners comparing
the recommendation with the strongest alternative.

== Our approach and contributions

We build one consistent evidence chain from the raw files to a policy recommendation. The
main contributions are:

+ *A transparent map-versus-subscription audit.* We define township claim rates, separate
  satellite-coded from terrestrial-coded claims, and use the 248 road-segment measurements as
  an independent diagnostic. The result is a bounded reclassification estimate rather than a
  point guess. #cite("1", "3")
+ *An explicit separation of three failure modes.* The township veto precludes construction, while
  three towns fall short of the proposed access floor. We then test a
  block-level eligibility reform and a verified-coverage overlay, which lets the county see
  exactly which rule change unlocks which plan. #cite("5")
+ *A cost-based mixed-integer deployment model.* Fiber and fixed wireless are priced from
  distance, terrain, household counts and ten years of discounted maintenance; a lexicographic
  objective maximizes qualifying coverage and then minimizes life-cycle cost. The direct model has
  at most 120 binary variables in the tested scenarios and closes its optimality gap. #cite("6", "8", "13")
+ *A matched comparison of procurement mechanisms.* The cooperative award, the competitive
  tender and the county partnership are solved under identical budget, period, standard and
  equity constraints, while bidder footprints, relative costs and route assumptions
  determine which projects each mechanism can offer. #cite("10", "15", "16")
+ *A measurement framework for effective use.* Benefit is defined as new qualifying household
  opportunities, but the paper also specifies orderability, performance and adoption
  measurements that would show whether funded projects are used for work and school. #cite("7", "14")

The AI tools used in this work are disclosed in the reference list and in the separate Report
on Use of AI Tools appended after the body of the paper. #cite("12", "18")
