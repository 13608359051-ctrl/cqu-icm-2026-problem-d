#import "layout.typ": *
#import "tables.typ": *

= Task 1: The northern coverage discrepancy

== Observations and inferred availability

The national cable provider's map flags 17 of the 20 North Ridge blocks, containing 1,908 of
the township's 2,135 households, for a map-imputed rate of 89.37\%. Only four of those blocks
are coded as a terrestrial technology, however: one cable block (68 households), one fiber
block (130) and two fixed-wireless blocks (179), for 377 households and a terrestrial-claim
rate of 17.66\%. The remaining 13 blocks, containing 1,531 households, carry a satellite flag.
The reported claim-rate gap is therefore 71.71 percentage points, and subscriptions, which
include every technology, reach only 55.13\%. The map describes what a provider reports; it
does not establish that a qualifying connection can be ordered at each address. #cite("1", "3")

The pattern is not confined to North Ridge. County-wide the map flags 42 terrestrial-coded
blocks containing 4,987 households, 31 satellite-coded blocks containing 4,095 households
(28.25\% of all households) and 47 unserved blocks containing 5,414 households. Every township
retains at least one terrestrial-flagged block (4, 6, 12, 4, 13 and 3 blocks, respectively),
so *a satellite-only correction cannot make any township fully eligible*; North Ridge is
simply the case where the discrepancy is largest. Figure 2 shows the block-level composition
and Figure 3(a) summarizes the road evidence.

The road file provides independent observations. For a group of surveyed segments $G$ with
lengths $ell_r$ and signal strengths $s_r$ in dBm, the weak-signal share at cutoff $tau$ is
given by (1):

$ w(G, tau) = (sum_(r in G : s_r <= tau) ell_r) / (sum_(r in G) ell_r). $
This statistic never assigns wired availability and never weights households. It measures
only how much of the road mileage in a group is consistent with a terrestrial signal at or
below the cutoff. At $-110$ dBm, the 25.61 surveyed miles in the satellite-coded blocks
include 2.61 miles at or below the cutoff (a weak-signal share of 10.2\%); the 3.40 surveyed
miles in the cable-coded block include none. The map-unserved blocks in North Ridge have a
share of 12.0\%, so the diagnostic is at best weakly informative and is never used to
reclassify individual addresses. It cannot prove that service is absent, and it does not
corroborate the cable claim. #cite("1")

#fig(signal-fig, 3)[Left: surveyed road mileage at or below each weak-signal cutoff, by provider
technology of the containing block. Right: households reclassified under the four challenge
outcomes; even full success leaves four served North Ridge flags.]

North Ridge is the only township explicitly identified as northern, and the files contain no
coordinates that would let us extend the estimate to other blocks. The result is a North Ridge
estimate, not a county-wide correction. Independent address-level ISP queries in nine U.S.
states found that provider maps overstate availability more often than they understate it,
which supports the direction and the verification method of our estimate, but that study's
error rates are not transferred to this synthetic county. #cite("3")

== How many households could be reclassified?

Observed flags and inferred availability must be separated. A satellite flag does not prove
that no terrestrial service exists, and it does not prove that satellite works, so the
reclassifiable population is an exposure set rather than a count. Within the 1,531 households
in satellite-coded blocks, we let $q$ be the share of addresses that an address-level audit
ultimately verifies as having no qualifying terrestrial alternative. The implied
reclassification, shown in (2), is

$ N(q) = floor(1531 q + 1/2). $

At 0\%, 25\%, 50\% and 100\%, this gives 0, 383, 766 and 1,531 households. These are rounded
scenarios, not probability-weighted forecasts: the files contain no address records, no
speeds, no prices and no test of actual availability, so a statistical confidence interval
cannot be computed from the supplied data. The observational bound across all flagged North
Ridge blocks is 0 to 1,908 households, and the plausible bound under the satellite-only
mechanism is 0 to 1,531. The uncertainty is resolved by collecting evidence, not by assuming
a distribution.

== Accept the map or file a challenge?

Accepting the map costs nothing and keeps the county's allocation blocked. Filing a challenge
costs time and money but creates a documented record that can support a later rule change or a
reallocation once the rule is amended. Table 3 compares the two paths under five outcomes.

#tabblock(3, [Challenge outcomes. Cost and time are planning assumptions; the grant consequence
assumes the township-wide eligibility rule is unchanged.], (1.18fr, 1.7fr, 2.15fr), ([Scenario], [County cost / elapsed time], [Expected grant consequence]), rows("challenge"), left-columns: (0, 1, 2))
The base audit uses 128 hours for address queries, 32 hours for preparation and 24 hours for
follow-up. At \$65.68 per hour plus \$500 in cash costs, the administrative cost is
$65.68(128+32+24)+500 = 12,585.12$ dollars; halving or doubling the hours and cash yields
\$6,292.56 to \$25,170.24. The hourly benchmark includes benefits and is the December 2025
U.S. state and local government average. #cite("4")

We allow 30 days to assemble evidence and include up to about 120 days for conceded cases and
270 days for contested cases before publication lag. For context, the FCC's challenge process
provides an initial 60-day provider response period, up to 60 more days for disputed cases, and
then adjudication and a map-revision step. Our durations are planning assumptions and do not
confer any authority under the grant rules assumed here. #cite("5")

The consequences differ by party:

- *Residents.* Accepting the map avoids delay and administrative cost but leaves households
  whose service options are overstated outside any funded plan. A challenge requires time and
  documentation but can put those households in line for funding once the rule permits it.
- *Regional cooperative.* A corrected record exposes projects it could serve. The cooperative
  would still need eligibility and funding before committing capital, and large unresolved
  challenges add bid risk.
- *National cable provider.* Keeping the map protects its existing grant boundary. A challenge
  imposes evidence and response costs, and success can expose unserved areas to competing
  offers; address-level review protects the service the provider can substantiate.
- *County government.* Holding the map saves money now and preserves the blocked allocation.
  Verification improves targeting and creates an auditable record. Even a full satellite-only
  correction leaves four flagged blocks and therefore releases no construction funds under the
  township-wide rule; the county should fund the audit separately or reserve its cost.

The audit is cheap relative to what it can unlock. Its \$12,585 cost is 0.11\% of the \$11.0
million budget, yet under the current township rule it has zero expected effect on awards.
Only when the rule is amended does the satellite evidence raise North Ridge from 211 to 1,675
modeled opportunities under the recommended partnership, a 1,464-household swing. The audit is
therefore best justified as cheap insurance against a wrong eligibility map rather than as a
stand-alone investment. #cite("3", "5")

#answer[Between *0 and 1,531 households* in North Ridge could be reclassified, with scenario
values of 0, 383, 766 and 1,531. Under the assumed eligibility rule, *no township becomes
eligible for construction funds even after a fully successful satellite-only challenge*,
because four North Ridge blocks remain flagged. The audit is nevertheless worth funding: it is
cheap relative to the budget, it is a prerequisite for any rule change or future funding
round, and it converts a disputed map into an address-level record.]
