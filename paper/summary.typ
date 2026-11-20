#import "layout.typ": *
#import "tables.typ": value, rows

#let team = sys.inputs.at("team", default: "TEAM NUMBER REQUIRED")

// COMAP-style summary sheet. The three-column box identifies the problem,
// contest year and control number; it replaces the running header on page 1.
#grid(
  columns: (1fr, 1fr, 1fr),
  align: (left, center, right),
  [*Problem Chosen*], [*2026*], [*Team Control Number*],
)
#v(2pt)
#grid(
  columns: (1fr, 1fr, 1fr),
  align: (left, center, right),
  [#text(size: 15pt, weight: "bold", fill: red, hyphenate: false)[D]], [*ICM*], [#text(size: if team == "TEAM REQUIRED" { 11pt } else { 15pt }, weight: "bold", fill: red, hyphenate: false)[#team]],
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

Hallowell County should hold construction awards under the current township rule. Each of
the six townships contains a block marked served, and three fall below the proposed 25\%
access floor even when every address in a terrestrial-flagged block receives full credit.
We count household opportunities to order fixed terrestrial service at 100/20 Mbps.

*Mapping.* The North Ridge map flags blocks containing 1,908 of 2,135 households. Only 377
households are in terrestrial-coded blocks. One block, containing 68 households, is labeled
cable. Across its three road segments, 0 of 3.40 surveyed miles registered at or below
−110 dBm. Road signals cannot establish whether an address can order cable. An address
audit, budgeted at #value("audit_cost"), could reclassify *0 to 1,531 households* in 13
satellite-coded blocks. Even if every household lacks a qualifying terrestrial offer, four
other flagged blocks still prevent a township award.

*Deployment.* With approval to fund map-unserved blocks, the county could start with 47
eligible blocks. At the assumed #value("budget") budget and 25\% township floor, the direct
plan adds *#value("t2_main_hh") qualifying household opportunities* at #value("t2_main_cost")
in ten-year life-cycle costs. It uses 12 fiber and 32 fixed-wireless projects. Across the
tested ranges, wireless serviceability changes coverage by #value("wireless_span") households
and fiber route cost by #value("fiber_span").

*Procurement.* On the same terms, a county-owned backhaul partnership (PPP) adds
*#value("ppp_hh") opportunities*, compared with #value("coop_hh") for a sole cooperative
award and #value("tender_hh") for competitive bidding. Seven modeled leases cover
#value("om_recovery") of hub maintenance and 11.51\% of hub capital plus maintenance in
present value. If all 13 northern blocks are verified and admitted, a 50\% floor is feasible
for direct deployment (5,311) and PPP (#value("override_count")). The tender misses that floor.

*Decision.* Seek authority for block-level awards. Before choosing PPP, survey the hub
routes and obtain bids and lease commitments. Adding three hypothetical miles to each hub
lateral reduces PPP coverage to #rows("route_stress").at(3).at(1), below the cooperative's #value("coop_hh").
Reoptimize with field quotes and select the feasible offer that reaches more households.
In the base PPP plan, #value("best_name") gains the most (#value("best_hh") opportunities)
with or without the 25\% floor. In the south, measure address orderability, price,
busy-hour performance and successful school or work use before expanding idle stations.

#v(4pt)
*Keywords:* rural broadband, coverage mapping, mixed-integer optimization, public-private
partnership, digital equity
