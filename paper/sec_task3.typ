#import "layout.typ": *
#import "tables.typ": *

= Task 3: Choosing a procurement mechanism

== Common comparison

The common objective, 100/20 fixed terrestrial benchmark, 25\% floor, ten-year period, 3\% real
rate and #value("budget") gross budget are those of Task 2. Gross resource cost is charged to
the budget before any lease receipts are credited, so a mechanism cannot borrow from future
rents to fund current construction. Under the original map rule every mechanism is infeasible,
for the same reason as the direct model. The portfolios below are computed under the same
block-level reform and, where stated, the same verified overlay.

*Cooperative award.* The cooperative controls the entire grant allocation and can offer the
direct packages of Task 2. The ceiling is reserved to it and any residual is unspent. The case
assumes countywide construction capacity by the cooperative and does not infer it from the
observed end of its network. Its result is exactly the direct benchmark.

*Competitive tender.* The cooperative offers both technologies within 13 backbone miles; the
cable provider offers fiber within 6 miles in towns with a cable claim; the wireless entrant
offers fixed wireless within 9 miles in towns with a wireless claim. Cable's capital cost is
70\% of the direct backhaul and 90\% of the direct last-mile cost; the entrant's is 75\% and
95\%. Maintenance is recalculated after repricing. No bidder must serve outside its footprint.
Among identical service bundles the lowest life-cycle bid per household, $c_a / h_a$, is kept.
At the same maximum coverage, minimizing total cost also minimizes $C/G$, but greedily ranking
individual bids could miss the floor, so the bid menu is optimized jointly. #cite("15")

*County partnership (PPP).* The direct tender menu remains available, and the county may build
and own backhaul hubs. A hub uses the median distance $d_j$ and terrain $g_j$ of its town's
originally unserved blocks. With $K_j$ its rounded capital and $ell_(i j)$ the lateral proxy in
miles,

$ K_j = "round"(25000 + 42240 d_j (1 + 0.16 (g_j-1))), quad ell_(i j) = abs(d_i - d_j) + 0.5. $

The hub costs $c_j = K_j + "round"(0.018 A K_j)$ in present value. Each spur's backhaul capital
is the rounded direct backhaul capital multiplied by $ell_(i j)/d_i$ and rounded again; cable
retains 90\% of direct last-mile capital and the wireless entrant 95\%, with maintenance
recalculated. Through a hub the cooperative serves within 6 lateral miles, cable within 4 and
the entrant within 5. The scenario assumes no measured routes or capacity. The eligible PPP
requires $sum_j y_j >= 1$; each hub-dependent offer satisfies $x_a <= y_(j(a))$ and each open
hub serves at least two actions, $sum_(a : j(a)=j) x_a >= 2 y_j$. Let $z_(p j) = 1$ when
provider $p$ serves at least one block through hub $j$. Discounted lease receipts and county
net outlay are

$ R = "round"(4800 A) sum_(p,j) z_(p j), quad C_"net" = C - R. $

Providers' payments equal county receipts, so the budget still applies to gross $C$; rent is
credited after selection. Shared-infrastructure and local-loop studies motivate the case but do
not supply Hallowell's costs or bidder choices. #cite("10", "11", "16")

== Matched results

Table 7 compares the mechanisms under the common budget, period and floor. The county
partnership reaches #value("ppp_hh") new household opportunities, #value("advantage") more than
the cooperative award (#value("coop_hh"), a 13.1\% gain) and #value("tender_gap") more than the
competitive tender (#value("tender_hh"), a 35.3\% gain). The cooperative delivers a slightly
higher minimum township rate (#value("coop_min") versus #value("ppp_min")), because dividing
the same budget among more projects concentrates the partnership's coverage in places where
marginal households are cheaper.

#tabblock(7, [Matched block-reform results at the common budget, ten-year period and 25\% floor.
USD/HH is gross life-cycle cost per new qualifying household opportunity.], (1.74fr, .76fr, .95fr, 1fr, .82fr, .72fr), ([Mechanism], [New HH], [Gross PV], [USD / HH], [Min. \%], [F / W]), rows("mechanisms"))

#fig(cost-fig, 7)[Life-cycle cost structure of the three mechanisms, in million 2026 U.S. dollars.
The diamond marks the county net outlay after modeled lease receipts for the partnership.]

The county partnership first leads on cost per household: \$2,306 per opportunity versus
\$2,606 for the cooperative and \$3,123 for the tender. Its four hubs open in East Corridor,
West Plains, Central Town and River Bend. County hub capital is #value("ppp_capex"), and
discounted county maintenance is #value("ppp_om"). Seven provider-hub leases pay \$33,600 per
year, or #value("ppp_rent") in present value, which covers #value("om_recovery") of the county's
discounted hub maintenance. That leaves \$44,981 of discounted operating cost plus the hub
capital to fund. With seven leases, the operating break-even fee is about \$5,553 per
lease-year. The gross plan assumes the grant can finance the full modeled life cycle; if the
leases are realized, county net outlay falls to #value("net_outlay"). Figure 7 shows the cost
structure and the net-outlay effect.

== Who benefits and who bears the cost

*Residents* gain the most connections under the partnership, but retail prices, installation
charges and device needs still determine whether those connections are used; the effective-use
framework in Section 8 is the check. The *regional cooperative* gains the option to bid for
last-mile work and to lease county capacity, but it loses the guaranteed award that the sole
award mechanism would give it. The *national cable provider* can bid or lease on the same
terms and keeps no exclusive territory under the partnership, while under the sole award it
receives no construction grant at all. The *county* bears four new hub assets, renewal and
vacancy risk, and the residual maintenance cost, but it also owns an asset that can be reused
and can reopen competition at each contract renewal. The eastern logistics corridor is a
candidate anchor: an employer or anchor institution could contract for shift-timed service or
Wi-Fi after site verification, but the workers and waiting drivers are outside the residential
household objective and should be covered by a separate agreement. #cite("1")

== If verified evidence can override provider claims

The verified overlay changes only eligible block membership and the availability of the
corresponding hub offers. It shifts one hub from East Corridor to North Ridge and raises
partnership coverage to #value("override_count"). The county partnership still leads the
cooperative by 439 households and the tender by 916 (Table 8). If the overlay is paired with a
50\% floor, the cooperative and the partnership still attain 5,311 and 5,750 opportunities,
while the tender cannot reach the West Plains floor even before the budget binds (767 modeled
opportunities against 1,048 required). Adopting the overlay requires an address record, an
appeal process and a way to publish corrected eligibility without exposing personal
information. A satellite-only correction under the township veto still leaves North Ridge
ineligible, so the overlay is useful only together with a rule change. #cite("1", "5")

#tabblock(8, [Verified-overlay comparison. The only changes from Table 7 are eligible block
membership and the corresponding hub offers.], (1.83fr, 1fr, 1.16fr, 1fr, .69fr), ([Mechanism], [New HH], [Gross PV], [Min. \%], [Hubs]), rows("verified"))

In the base partnership allocation, cable wins projects covering 3,760 households and the
wireless entrant wins 1,005; the cooperative wins none in this scenario, although it can use
the same published terms to bid. The incumbent is therefore the largest modeled beneficiary of
the partnership, which is acceptable only if the lease terms are non-discriminatory and the
eligibility audit remains an independent county function. Under a sole award the cooperative
would take responsibility for all 4,213 households and the cable provider would receive no
grant. These modeled bidder shares depend on the assumed footprints and relative costs and
should be reopened when conforming offers and signed commitments arrive.

*Is the ranking robust?* Figure 8 repeats the matched comparison across the tested budget,
maintenance and verified-coverage scenarios. The partnership leads in every case: at \$9
million and \$13 million it delivers 4,362 and 5,110 opportunities against 3,991 and 4,365 for
the cooperative and 3,380 and 3,645 for the tender; under low and high maintenance it delivers
4,845 and 4,609 against 4,259 and 4,164; and with verified coverage it leads by 439 and 916
households. The cooperative still leads the tender in every scenario. The only tested case
where the partnership's lead narrows is the doubled hub-capital rate, where it falls to 4,381
but still exceeds the cooperative's 4,213. The ranking is therefore stable across the tested
ranges, although the absolute advantage depends on the assumed bidder cost multipliers, which
we could not vary without observed bid data.

#fig(robust-fig, 8)[Mechanism comparison across the tested budget, maintenance and verified-coverage
scenarios. Bars are new household opportunities under the same budget, period and floor.]

#answer[The *county backhaul partnership* is the recommended mechanism. It adds #value("ppp_hh")
opportunities, #value("advantage") more than the next-best cooperative award, at the lowest
gross cost per household, and its ranking does not change under the verified overlay or across
the tested hub-cost, budget and maintenance ranges. The cooperative is the fallback if lease
commitments or route costs defeat the case for a public backbone.]
