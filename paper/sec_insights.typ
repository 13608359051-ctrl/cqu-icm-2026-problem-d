#import "layout.typ": *
#import "tables.typ": *

= Share Your Insights

== Defining benefit and identifying the benefiting township

The primary benefit measure is the number of new qualifying household opportunities created
by the recommended plan in township $t$, $G_t = sum_(a : i(a) in t) h_a x_a$. The plan is the
county partnership from Section 7. We also report three checks: the share of each township's
eligible pool that is connected, the post-plan access rate $(b_t + G_t)/H_t$ on the claim
proxy, and the baseline subscription rate. Table 9 reports them; Figure 9 shows the contrast
between claim-based access and subscriptions.

#fig(benefit-fig, 9)[New households gaining access, baseline subscription rates and post-plan
claimed access by township. The gap between the bars is the measurement problem at the center
of this problem.]

#tabblock(9, [Recommended county partnership under the block reform. Pool covered is new
qualifying opportunities as a share of the township's map-unserved households; post access
uses the terrestrial-claim proxy; subscription rate is the observed baseline.], (1.55fr, .9fr, 1.05fr, 1.05fr, 1fr), ([Township], [New HH], [Pool covered], [Post access], [Sub. rate]), rows("benefits"))

*West Plains* benefits most: it gains 1,367 new qualifying opportunities, which is 91.19\% of
its 1,499 eligible households, and its post-plan access rate rises to 84.49\%. The pattern
follows the eligible pool: West Plains, River Bend and East Corridor combine large unserved
populations with moderate construction costs, while Central Town is fully covered and South
Hollow is limited by its small remaining pool and its terrain.

== Does the same township benefit most without the equity constraint?

We reran the partnership model with only the 25\% floor removed, holding the budget, costs,
eligibility and all other constraints constant. The unrestricted optimum selects the same
four hubs, the same projects and the same providers; the minimum post-plan access rate is
27.54\%, which is #value("floor_slack") above the floor. *West Plains remains the
most-benefiting township.* The equality of the two portfolios is a property of a slack
constraint, not evidence that equity never matters: the coverage objective spends first where
the marginal cost per household is lowest, and at this budget those projects already lift
every township above 25\%. At a 50\% floor the block-eligibility plan becomes infeasible, and
under the verified overlay the largest beneficiary shifts to North Ridge (1,675
opportunities), which is exactly what an evidence-based rule change is intended to do.

== Measurement determines equity

The apparent fairness of the plan depends on which access measure the county uses. South
Hollow has the lowest subscription rate in the county (21.96\%) and the highest share of
senior residents, yet its terrestrial-claim proxy is 68.54\%, so on the claim proxy it looks
better served than North Ridge, West Plains or River Bend. As a result the recommended plan
connects only 174 of its 415 eligible households (41.93\%), and its post-plan claimed access
is 78.15\% even though fewer than one household in four subscribes. The post-plan access
rates across townships still span #value("min_gap") (90.53\% in Central Town against 27.54\% in
North Ridge), so the 25\% floor guarantees a minimum claimed coverage, not a minimum level of
actual use. A use-based or subscription-based floor would make South Hollow, not North Ridge,
the binding township — a change the county can evaluate with the measurement framework below.
#cite("7", "14")

== From tower availability to usable service

South Hollow is the only township explicitly named for the south. It has 398 subscriptions for
1,812 households (21.96\%); its five fixed-wireless-coded blocks have 99 subscriptions for 491
households (20.16\%). Both rates include every subscription technology, and the files contain
no technology-specific subscriptions, no load by hour and no reasons for low use. The
recommended plan adds 174 modeled opportunities in South Hollow, but before expanding the
existing stations the county should test whether they have spare capacity and whether
households can actually use them. #cite("1")

The county should measure three stages with separate denominators.

+ *Orderability and installation.* Sample addresses across served and unserved map categories,
  tower sectors, terrain and income strata, including non-subscribers. Record the product and
  full price quoted, the installation decision and time to activate, technician line of sight,
  and the reason for refusals or failed appointments.
+ *Reliable access.* Collect router-based downstream and upstream tests, round-trip latency,
  packet loss, outages and sector loads by hour, including school and work hours and evening
  peaks. Adapting the FCC's high-cost testing rule, require at least 80\% of measurements in
  each direction to meet at least 80\% of the 100/20 tier and at least 95\% of latency readings
  to be at or below 100 ms; report full attainment and failed sessions separately and compare
  wired-at-router with Wi-Fi results. #cite("14")
+ *Adoption and effective use.* Divide the number of households that report a remote work or
  school need and can reliably complete a video session and upload work by all households
  reporting that need. Include non-subscribers and failed installations in the denominator.
  Collect baseline, 30-day and 90-day surveys and brief standardized tasks, and ask about
  cost, devices, skills, accessibility, competing offers and schedules. #cite("17")

The evidence distinguishes the two explanations for low utilization. Low traffic with
installation failures or missing coverage signals a supply barrier. Measured service that meets
the standard, combined with reported need and few orders, signals price, equipment, activation
or skills barriers. If use remains low even when an affordable offer, working devices and
reliable service are in place, limited local demand becomes the more plausible explanation. A
randomized pilot that offers a bill credit or device-and-installation help to willing eligible
households can test whether those offers raise activation and task completion. Consent,
comparison-group support and restricted address records are required. The rural deployment
literature finds better service and quality-of-life associations without a comparable
attributable increase in work or school use, which is why the county should measure activities
rather than subscriptions alone. #cite("7")

#answer[West Plains benefits most from the recommended plan, with 1,367 new opportunities
(65.22\% of its households); reoptimizing without the equity constraint selects the same
portfolio, so the same township still benefits most. To judge whether funded projects serve
intended users, the county should combine an address-level orderability audit, router-based
performance testing and a work/school task survey, then use a randomized support pilot to
separate limited demand from price, device and installation barriers.]
