#import "layout.typ": *
#import "tables.typ": *

= Notations and Data

== Notation

#tabblock(1, [Notation used throughout the paper. Costs are in 2026 U.S. dollars.], (0.9fr, 4.6fr), ([Symbol], [Meaning]), (
  [$H_i, S_i$], [Households and subscription households in block $i$],
  [$M_i, T_i$], [Original served flag and technology label of block $i$],
  [$t = 1, dots, 6$], [Township index],
  [$H_t, S_t$], [Households and subscription households in township $t$],
  [$m_t, b_t$], [Households in served blocks; households in served terrestrial-coded blocks],
  [$r_t$], [Subscription rate $S_t / H_t$],
  [$d_i, g_i$], [Backbone distance (miles) and terrain index (1-5) of block $i$],
  [$a$], [A deployment action: technology $times$ block, or a hub-dependent offer],
  [$h_a$], [Qualifying household opportunities created by action $a$],
  [$x_a, y_j$], [Binary action choice; binary county-hub commissioning choice],
  [$K^B_a, K^L_a$], [Backhaul and last-mile capital cost of action $a$],
  [$A$], [Ten-year annuity factor at a 3\% real discount rate],
  [$c_a$], [Life-cycle cost of action $a$, including discounted maintenance],
  [$B, theta$], [Budget (2026 dollars) and minimum township access floor],
  [$E_i$], [Eligibility ceiling of block $i$ under a given rule],
  [$G_t, G, C$], [New township coverage, total coverage and total life-cycle cost],
  [$R, C_"net"$], [Discounted lease receipts and county net outlay],
), left-columns: (0, 1))

== Data audit and service definition

The attached files describe 120 census blocks in six townships and 248 road segments that
link to the blocks. Each block reports households, subscriptions, a served flag, a technology
label, distance to backbone and terrain. Road segments report signal strength in dBm. Table 1
collects the notation used throughout the paper. The ``V2'' versions
of both files are byte-identical to the originals; primary keys are unique;
all road segments join to exactly one block; each block contains 15 to 219 households;
subscriptions never exceed households; distances range from 0.5 to 18.0 miles; and terrain is
ordinal from 1 to 5. There are no coordinates, adjacent-block relations, tower locations or
route endpoints. #cite("1")

A qualifying offer is modeled as a fixed terrestrial connection of at least 100 Mbps down and
20 Mbps up in the 2026 planning year, as stated in Section 2. Satellite remains in the raw
served flag for the strict rule but is excluded from the qualifying technology set. Let
$cal(T) = {"fiber", "cable", "fixed wireless"}$. Township counts and rates are computed by
$H_t = sum_(i in t) H_i$, $S_t = sum_(i in t) S_i$, $r_t = S_t / H_t$. The household count in
all served blocks is $m_t = sum_(i in t) H_i M_i$, while the narrower terrestrial-claim proxy
is $b_t = sum_(i in t : T_i in cal(T)) H_i M_i$; the difference $(m_t - b_t)/H_t$ is the
claim-rate gap. The full household count of a flagged terrestrial block is credited to the
proxy, which assumes that those claims meet the service threshold; this gives the most favorable count inside
those blocks. Eligibility under the strict rule follows the original flags regardless of the count. Road evidence is aggregated
separately and is never joined to households, so a block intersected by three roads is not
counted three times.

#fig(coverage-fig, 2)[(a) The 20 census blocks of each township by reported claim. (b) Household
shares by claim type, with the observed subscription rate marked as a dot. The subscription dot includes
all technologies and measures adoption, while the bars describe map claims.]

#tabblock(2, [Household counts, subscriptions, original map flags and the composition of the
claimed coverage. Served and terrestrial columns count blocks; satellite and unserved columns
count households. Every township contains at least one terrestrial-flagged block.], (1.4fr, .78fr, .82fr, .7fr, .66fr, .7fr, .76fr, .78fr), ([Township], [HH], [Subscribed], [Sub. \%], [Served blk], [Terrest blk], [Satellite HH], [Unserved HH]), rows("townships"))

Observed subscription rates range from 21.96\% in South Hollow to 77.65\% in Central Town. The
terrestrial-claim proxy $b_t/H_t$ is a claimed-availability measure, not a subscription rate;
Figure 2(b) places the two side by side so the distinction stays visible. County-wide the map
flags 73 blocks: 42 terrestrial-coded blocks containing 4,987 households, 31 satellite-coded
blocks containing 4,095 households (28.25\% of all households), and 47 map-unserved blocks
containing the 5,414-household eligible pool. The six townships retain 4, 6, 12, 4, 13 and 3
terrestrial-flagged blocks respectively, so a satellite-only correction can never make a
township fully eligible. Figure 2(a) shows the block-level pattern: every township row
contains at least one dark terrestrial cell.
