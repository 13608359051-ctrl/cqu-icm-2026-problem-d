#import "layout.typ": *
#import "tables.typ": *

= Executive Summary

One reported service flag bars an entire township from receiving funds. The county also needs to distinguish households that can order a qualifying connection from those that can afford and use it for school or work. The files contain block claims and subscriptions, without individual service offers or records of effective use. #cite("1")

We count households once, use road observations as a diagnostic, and solve the grant allocation problem with and without the township veto. The alternative is a staged program for unserved blocks, with a 25% per-township access floor in the first phase. #value("executive_mechanism") The board can begin by collecting verifiable evidence while preserving the budget for legally eligible construction. The memo on page #context counter(page).at(<memo>).first() specifies the decision conditions.

OpenAI Codex was used for modeling, code, calculations, figures, drafting and independent subagent checks. The appended report documents the scope and the team review status. #cite("12")

= Data and service definition

We model a fixed terrestrial offer capable of at least 100 Mbps down and 20 Mbps up. The speed benchmark follows the FCC's 2024 fixed broadband report. The planning reference year and dollar basis are 2026. The provided synthetic file has no observation dates. Satellite is excluded from the qualifying planning proxy because local offer, capacity and performance data are missing, while its original flag remains binding under the problem's strict rule. This is a modeling convention for a terrestrial deployment program. #cite("1", "2")

For township $t$, $H_t$ is the sum of block households and $S_t$ is the sum of block subscription households. Its subscription rate is $S_t / H_t$. Surveyed roads join many-to-one to blocks and are aggregated separately by block; joining first and summing household columns would weight blocks by the number of observed segments.

#tab((1.7fr, 1fr, 1fr, .95fr, .88fr, 1.08fr), ([Township], [Total HH], [Subscribed], [Sub. %], [Served blocks], [Terrest. HH]), rows("townships"))
#caption[*Table 1.* Households (HH), subscriptions, original map flags and baseline terrestrial-claim proxy. All six townships are strictly ineligible.]

The two original/V2 pairs are byte-identical. Primary keys are unique and all 248 roads link to the 120 blocks, with one to three roads per block. Each block contains 15–219 households. Subscriptions remain within household totals. Backbone distances are 0.5–18.0 miles and terrain is ordinal (1–5). The files contain no coordinates or route endpoints.

#pagebreak()
= Task 1. Assessing the maps

#image(coverage-fig, width: 100%)
#caption[*Figure 1.* Township household shares computed from the block CSV. Flagged and terrestrial shares assign the indicated technology to each household in the flagged block. Subscriptions include all technologies.]

North Ridge has 17 flagged blocks. Thirteen are coded as satellite (1,531 households) and four as cable, fiber or fixed wireless (377 households). The all-technology map-imputed rate is 89.37%. The terrestrial-claim proxy is 17.66%, giving a 71.71 percentage-point discrepancy. Subscriptions reach 55.13%, and the file does not identify their speeds, providers or technology. Road signal at or below −110 dBm accounts for only 2.61 of 25.61 observed road-miles in satellite-coded blocks. The sample illustrates how a roadside reading can coexist with a satellite label. It cannot establish continuity of a wired network or service at a residence. #cite("1")

No provider identifier links the narrative's national cable operator to individual records. In the one North Ridge block coded cable (68 households), zero of 3.40 observed road-miles meet the weak-signal diagnostic. This does not validate the cable claim. North Ridge is the only explicitly northern-named township. The data do not locate any other blocks geographically, so this estimate refers to North Ridge alone. Major, Teixeira and Mayer found historical map overstatement using independent address-level ISP queries across nine US states. Their study supports the verification method. Its error rates are not transferred to this synthetic county. #cite("3")

The 1,531 households are the exposure within the satellite-coded group. For a fraction $q$ eventually verified to lack a qualifying alternative, round $1531 q$ to the nearest household, with half rounded up. The 0%, 25%, 50% and 100% scenarios yield 0, 383, 766 and 1,531 households. These conditional counts have no associated probabilities or statistical confidence interval. Across all flagged North Ridge blocks, only the uninformative range of 0–1,908 is supportable without more evidence.

#pagebreak()
== Accept the map or file a challenge?

#tab((1.18fr, 1.7fr, 2.15fr), ([Scenario], [County cost / elapsed], [Expected grant consequence]), rows("challenge"), left-columns: (0, 1, 2))
#caption[*Table 2.* Challenge outcomes refer to a documented correction in the targeted satellite-coded group. Cost and time are planning assumptions.]

A base audit of 184 staff hours at \$65.68 per hour plus \$500 cash costs \$12,585.12. A half-to-double workload and cash envelope gives \$6,292.56–\$25,170.24. The hourly benchmark includes employer benefits and is the US December 2025 state and local government average. The labor and cash quantities are scenario inputs. #cite("4")

We allow 30 days to assemble evidence. For timing context, the FCC process provides an initial 60 days for the provider, up to 60 more for disputed cases, adjudication and a map-revision step. Our routine and contested cases allow up to about 120 and 270 days from preparation, respectively, before extra publication or screening lag. These durations are for planning and do not confer authority under the problem's grant rules. Obtain address-level order denials, service quotes, installation dates, products and speeds. Invite the provider to correct errors or produce installation records before escalation. #cite("5")

- *Residents.* Accepting the map avoids delay and administrative cost, but excludes households whose service options are overstated. A challenge requires time and documentation and can bring those households into a queue once the rules permit funding.
- *Regional cooperative.* Corrected records expose potential projects. The cooperative would still need eligibility and funding before making commitments. Large, unresolved challenges add bid risk.
- *National cable provider.* Keeping the map protects its existing grant boundary. A challenge imposes evidence and response costs, and success can expose unserved areas to competing offers. Address-level review protects service that the provider can substantiate.
- *County government.* Holding the map saves administrative expense now and preserves the blocked allocation. Verification improves targeting and supplies an auditable record. Even a full satellite-only correction releases no funds under the township veto. The county should finance the audit separately or explicitly reserve its cost before making awards.

