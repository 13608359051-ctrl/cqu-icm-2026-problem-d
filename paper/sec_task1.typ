#import "layout.typ": *
#import "tables.typ": *

= Task 1: The northern coverage discrepancy

== Observations and inferred availability

Residents dispute the national cable provider's map, according to the problem statement.
The block file records an aggregate flag and a technology label without identifying the
provider that filed a claim. In North Ridge, 17 of 20 blocks are flagged, representing
1,908 of 2,135 households (89.37\%). One cable-coded block contains 68 households, one
fiber-coded block 130, and two fixed-wireless blocks 179. Those four terrestrial-coded
blocks contain 377 households (17.66\%). The 13 satellite-coded blocks account for the
71.71 percentage-point difference. Subscriptions across all technologies reach 55.13\%.
An address-level check is needed to identify the available offer and its provider. #cite("1", "3")

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
At a cutoff of −110 dBm, satellite-coded blocks account for 2.61 weak miles out of
25.61 surveyed (10.2\%). The three segments in cable-coded block 420010000004 registered
−79.3, −89.8 and −81.1 dBm. Thus 0 of its 3.40 surveyed miles met the weak-signal
criterion. The corresponding share in map-unserved blocks was 12.0\%. These observations
describe surveyed roads and cannot establish cable or fiber orderability at an address.
#cite("1")

#fig(signal-fig, 3)[Left: surveyed road miles above and at or below −110 dBm, grouped by
block technology label in North Ridge. Right: reclassification scenarios for households in
the satellite-coded blocks. Four other North Ridge blocks retain their served flags.]

North Ridge is the only township explicitly identified as northern, and the files contain no
coordinates that would let us extend the estimate to other blocks. The result is a North Ridge
estimate, not a county-wide correction. Independent address-level ISP queries in nine U.S.
states found that provider maps overstate availability more often than they understate it,
which supports checking individual addresses. Rates from those states cannot quantify errors
in this synthetic county. #cite("3")

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
mechanism is 0 to 1,531. Verified order denials, quotes and installation records would narrow the bounds.

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

The comparison funds the \$12,585.12 audit from a separate administrative account. If it
must come from the construction grant, reserve its cost and reoptimize the smaller budget.
Under the current veto even a successful targeted audit releases no construction funds.
A change to block eligibility would admit 47 already-unserved blocks without awaiting this
audit. If the authority also admits all 13 disputed blocks after verification, the PPP
reoptimization increases northern opportunities from 211 to 1,675 (+1,464). The other five
townships lose 479 in aggregate, giving a countywide increase of 985. A partial finding
requires its own eligibility map and reoptimization. #cite("1", "5")

#answer[An estimated *0 to 1,531 households* could be reclassified within the northern
satellite-coded blocks. The audit can document which addresses qualify if funding rules
change. Even full success leaves four served blocks and the existing township veto intact.]
