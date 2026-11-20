#import "layout.typ": *
#import "tables.typ": *

#pagebreak()
= Share Your Insights

== Who benefits from the recommended portfolio?

The primary benefit metric is $G_t = sum_(a : i(a) in t) h_a x_a$, the count of new qualifying household opportunities in $t$. We also report $G_t/H_t$, which accounts for township size. These metrics measure modeled orderability. The survey below measures effective use separately.

#tab((1.65fr, 1fr, 1.17fr, 1.17fr), ([Township], [New HH], [Gain / HH], [Post access]), rows("benefits"))
#caption[*Table 7.* Recommended county partnership under the block reform. Gain/HH is the increase in the township rate in percentage points. Post access includes the terrestrial-claim proxy.]

#image(benefit-fig, width: 100%)
#caption[*Figure 4.* New household opportunities by township, with and without the 25% floor. Equal bars reflect independent reoptimization.]

#value("best_name") gains the most by the primary metric, with #value("best_hh") opportunities, or #value("best_share") of its households. We reran the partnership with only the floor removed. The chosen hubs, projects and providers were identical. The unrestricted optimum still has a minimum post-access rate of #value("ppp_min"), so the original floor did not bind. West Plains remains first. This result is for the specified budget and claims. Under the distinct verified-overlay scenario with the floor, #value("verified_best_name") leads with #value("verified_best_hh") new opportunities.

#pagebreak()
== From tower availability to usable service

South Hollow is the only township explicitly named for the south. It has 398 subscriptions for 1,812 households (21.96%). Its five wireless-coded blocks have 99 subscriptions for 491 households (20.16%). Both rates include every subscription technology. The narrative describes idle stations. The files lack technology-specific subscriptions, load by hour and reasons for low use. The partnership adds 174 modeled opportunities in South Hollow. Test the existing stations' spare capacity before expanding them. #cite("1")

The county should measure the following stages with separate denominators.

1. *Orderability and installation.* Sample addresses across served and unserved map categories, tower sectors, terrain and income strata. Include non-subscribers. Record the product and full price quoted, the install decision and time to activate, technician line of sight, and the reason for refusals or failed appointments.
2. *Reliable access.* Collect router-based downstream and upstream tests, round-trip latency, packet loss, outages and sector loads by hour. Repeat during school and work hours and expected busy evenings. Adapt the FCC's high-cost testing rule by requiring at least 80% of measurements in each direction to meet or exceed 80% of the 100/20 tier. At least 95% of round-trip latency readings should be at or below 100 ms. Report full 100/20 attainment and failed sessions separately. Track power and equipment faults and compare wired-at-router with Wi-Fi results. #cite("14")
3. *Adoption and effective use.* Track subscriptions among orderable households. For effective use, divide the number of households reporting a remote work or school need that can reliably complete a video session and upload work by all households reporting that need. Include non-subscribers and failed installations in the denominator. Collect baseline, 30-day and 90-day surveys and brief standardized tasks. Ask about cost, devices, skills, accessibility, competing offers and schedules. Report nonresponse and uncertainty by stratum.

Low sector use with installation failures signals a supply barrier. Adequate measured service and high reported need alongside few orders suggests price, equipment or activation barriers. Randomly offering a bill credit or device-and-installation help to willing, eligible households could show whether those offers increase activation and task completion. Continued low use with an affordable offer, working devices and reliable service would make limited local demand more plausible. An installation or price pilot requires consent and a way for households in comparison groups to receive support. Store address records with restricted access and publish aggregates only. #cite("7", "17")

The rural Turney deployment found better service and quality-of-life associations without a corresponding attributable increase in work, school or health use. That finding supports measuring activities directly. It supplies neither a take-up assumption nor a causal effect for Hallowell. #cite("7")

