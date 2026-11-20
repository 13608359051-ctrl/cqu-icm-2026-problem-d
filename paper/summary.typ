#import "layout.typ": *
#import "tables.typ": value

#let team = sys.inputs.at("team", default: "TEAM NUMBER REQUIRED")

// COMAP-style summary sheet. The three-column box identifies the problem,
// contest year and control number; it replaces the running header on page 1.
#grid(
  columns: (1fr, 1fr, 1fr),
  align: (left, center, right),
  [*Problem Chosen*], [*2027*], [*Team Control Number*],
)
#v(2pt)
#grid(
  columns: (1fr, 1fr, 1fr),
  align: (left, center, right),
  [#text(size: 15pt, weight: "bold", fill: red, hyphenate: false)[D]], [*MCM/ICM*], [#text(size: if team == "TEAM REQUIRED" { 11pt } else { 15pt }, weight: "bold", fill: red, hyphenate: false)[#team]],
)
#v(1pt)
#align(center)[*Summary Sheet*]
#v(3pt)
#line(length: 100%, stroke: .8pt)
#v(12pt)

#align(center)[
  #set text(hyphenate: false)
  #text(size: 16pt, weight: "bold")[The Last Mile of Broadband] \
  #v(3pt)
  #text(size: 13pt)[A Cost-Effective, Equitable Investment Plan]
]
#v(10pt)
#align(center)[#text(size: 12.5pt, weight: "bold")[Summary]]
#v(2pt)

#set par(leading: .35em, spacing: .6em)

Rural broadband programs spend public money against provider coverage maps that do not
always describe service a household can actually buy. Hallowell County, about 48,000
residents across 620 square miles, must allocate its remaining broadband funds while the map
classification of its northern townships is disputed. We combine the supplied block,
subscription and road-signal files into an explicit evidence audit, a mixed-integer
deployment model and a matched comparison of three procurement mechanisms.

*Task 1.* The block file covers 14,496 households. County-wide, 31 satellite-coded blocks
contain 4,095 households, but every township also contains at least one terrestrial-flagged
block. In North Ridge the provider map flags 1,908 of 2,135 households, yet only 377 of them
sit in blocks with a terrestrial claim. Road signals at the one cable-coded block fall below
the weak-signal cutoff on every surveyed segment. Depending on address-level verification, *0
to 1,531 households could be reclassified*, and our scenarios use 0, 383, 766 and 1,531. A
targeted audit costs about \$12,600; even a fully successful correction leaves four flagged
blocks, so *no township becomes eligible under the current township-wide rule*.

*Task 2.* We solve a binary deployment model that selects fiber and fixed-wireless projects
by block, with distance- and terrain-dependent capital costs and ten years of discounted
maintenance, under an \$11.0 million budget and a 25\% township access floor. Strict
eligibility makes the model *infeasible for every township*, and additional budget cannot
repair a zero eligibility ceiling. After a block-level reform, the optimal plan adds *4,213
qualifying household opportunities at a life-cycle cost of \$10.98 million*, with a minimum
township access rate of 28.10\%. A 50\% floor needs verified coverage evidence; with a
verified North Ridge overlay the plan reaches *5,750* opportunities. Fixed-wireless
serviceability is the dominant uncertainty: ±10 percentage points move coverage by 661
households, versus 295 across the full fiber-cost range.

*Task 3.* Under the same budget, period, standard and equity floor, a sole cooperative award
delivers 4,213 opportunities, a lowest-cost-per-household tender 3,521, and a *county-owned
backhaul partnership with open-access leases 4,765* — 552 more than the cooperative and 1,244
more than the tender — at the lowest cost per household (\$2,306). Its four hubs cost \$2.16
million; seven leases recover 86.4\% of the county's discounted hub maintenance. With a
verified coverage override the partnership remains first at 5,750.

*Recommendation.* Hold construction awards until the eligibility rule is amended and the
disputed addresses are audited, then adopt the county partnership, which gives residents the
most usable connections per dollar and keeps both incumbents competing for leases. West
Plains benefits most from the first phase (1,367 opportunities), and removing the equity floor
selects the same portfolio, so the floor costs nothing in this scenario. For the southern
fixed-wireless stations, the county should measure orderability, busy-hour performance, total
price, device access and successful work or school tasks rather than subscription counts.
Because the same map-based veto appears in many rural counties, the framework — audit the
claims, price the evidence, reform the eligibility unit, then procure open access — transfers
beyond Hallowell County.

#v(4pt)
*Keywords:* rural broadband, coverage mapping, mixed-integer optimization, public-private
partnership, digital equity
