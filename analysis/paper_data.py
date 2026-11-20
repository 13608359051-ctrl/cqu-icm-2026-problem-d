"""Format verified analysis outputs for the paper and regenerate its figures."""

import argparse
import csv
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Patch
import numpy as np


TOWNS = ("North Ridge", "East Corridor", "South Hollow", "West Plains", "Central Town", "River Bend")
MECHANISMS = {"cooperative": "Cooperative", "competitive": "Competitive tender", "county PPP": "County PPP"}
COLORS = ("#26456b", "#2e7d7b", "#c08a3e")
GREY = "#b9c4d1"


def read(path):
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def count(x):
    return f"{int(x):,}"


def dollars(x):
    return f"${int(round(float(x))):,}"


def million(x):
    return f"${float(x) / 1e6:.3f}m"


def pct(x):
    return f"{float(x):.2f}%"


def save(fig, dest):
    fig.savefig(dest, bbox_inches="tight", pad_inches=.08, metadata={"Date": None})
    plt.close(fig)


def style():
    plt.rcParams.update({
        "font.family": "serif",
        "font.serif": ["Times New Roman", "Liberation Serif", "DejaVu Serif"],
        "mathtext.fontset": "stix",
        "font.size": 9.5,
        "axes.labelsize": 9.5,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "legend.fontsize": 8.5,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.axisbelow": True,
    })


def schematic(out):
    fig, ax = plt.subplots(figsize=(8.1, 2.8), layout="constrained")
    ax.set(xlim=(0, 8.2), ylim=(0, 2.7))
    ax.set_axis_off()
    for xy, label in [
        ((.12, 1.02), "Existing fiber\nbackbone"),
        ((3.0, .15), "Optional county\nwholesale hub"),
        ((6.0, 1.02), "Households in an\neligible block"),
    ]:
        x, y = xy
        ax.add_patch(FancyBboxPatch(xy, 2, .79, boxstyle="round,pad=.04",
                                    fc="#eef1f4", ec=COLORS[0], lw=1.2))
        ax.text(x + 1, y + .395, label, ha="center", va="center", fontsize=13)
    for start, end in [((2.15, 1.57), (5.95, 1.57)),
                       ((2.15, 1.17), (2.95, .58)),
                       ((5.05, .58), (5.95, 1.17))]:
        ax.annotate("", xy=end, xytext=start, arrowprops={"arrowstyle": "->", "color": COLORS[1], "lw": 1.5})
    ax.text(4.1, 1.82, "Direct backhaul + last mile", ha="center", fontsize=13)
    ax.text(1.93, .47, "County spur", ha="right", fontsize=12)
    ax.text(6.08, .47, "Tenant lateral + last mile", ha="left", fontsize=12)
    ax.text(.08, 2.42, "SERVICE PATHS  -  SCHEMATIC, NOT TO SCALE", color=COLORS[0], fontsize=11, weight="bold")
    save(fig, out / "fig_model.svg")


def workflow(out):
    fig, ax = plt.subplots(figsize=(8.1, 4.3), layout="constrained")
    ax.set_axis_off()
    ax.set(xlim=(0, 8), ylim=(0, 4.12))
    steps = [
        (.08, 2.99, "1  Audit the inputs", "Flags, subscriptions and\nroad evidence"),
        (4.40, 2.99, "2  Apply the strict rule", "All six towns ineligible.\nHold construction awards."),
        (4.40, 1.55, "3  Test rule changes", "Allow unserved blocks and\ncheck a verified override"),
        (.08, 1.55, "4  Optimize deployment", "Budget, terrain, distance\nand a township floor"),
        (.08, .11, "5  Compare procurement", "Cooperative, tender and\ncounty partnership"),
        (4.40, .11, "6  Evaluate and decide", "Remove the floor as a test.\nMeasure work and school use."),
    ]
    for x, y, title, label in steps:
        ax.add_patch(FancyBboxPatch((x, y), 3.5, .98, boxstyle="round,pad=.035",
                                    fc="#f0ede6" if title.startswith("2") else "#eef1f4",
                                    ec=COLORS[0], lw=1.15))
        ax.text(x + .15, y + .74, title, color=COLORS[0], fontsize=14, weight="bold", va="center")
        ax.text(x + .15, y + .37, label, color="#19272c", fontsize=13, va="center", linespacing=1.15)
    for start, end in [((3.65, 3.48), (4.33, 3.48)), ((6.15, 2.94), (6.15, 2.60)),
                       ((4.34, 2.04), (3.65, 2.04)), ((1.83, 1.49), (1.83, 1.16)),
                       ((3.65, .60), (4.33, .60))]:
        ax.annotate("", xy=end, xytext=start, arrowprops={"arrowstyle": "->", "color": COLORS[1], "lw": 1.75})
    save(fig, out / "fig_workflow.svg")


def charts(out, data, mechanisms, towns, recommended, t2):
    style()
    navy, teal, gold = COLORS

    # Figure 2: block-level claim map and township household shares.
    blocks = read(out / "task1_blocks.csv")
    fig, (axg, axb) = plt.subplots(1, 2, figsize=(6.6, 2.9), layout="constrained",
                                   gridspec_kw={"width_ratios": [1.3, 1.0]})
    class_color = {"terrestrial": navy, "satellite": teal, "unserved": GREY}
    for row, town in enumerate(TOWNS):
        group = sorted((b for b in blocks if b["township"] == town), key=lambda b: b["block_id"])
        for col, block in enumerate(group):
            if block["provider_served"] == "0":
                cls = "unserved"
            elif block["provider_technology"] == "satellite":
                cls = "satellite"
            else:
                cls = "terrestrial"
            axg.add_patch(plt.Rectangle((col, row), .9, .8, fc=class_color[cls],
                                        ec="white", lw=.6))
        axg.text(20.6, row + .4, f"{sum(b['provider_served'] == '1' for b in group)}/20",
                 va="center", fontsize=7.5)
    axg.set_xlim(-.2, 22.4)
    axg.set_ylim(len(TOWNS) - .1, -.1)
    axg.set_yticks(np.arange(len(TOWNS)) + .4)
    axg.set_yticklabels(TOWNS, fontsize=8)
    axg.set_xticks([])
    axg.tick_params(length=0)
    for spine in axg.spines.values():
        spine.set_visible(False)
    axg.set_title("(a) Census blocks by reported claim", fontsize=9, pad=2)
    handles = [Patch(facecolor=class_color[k], edgecolor="none", label=lab)
               for k, lab in (("terrestrial", "Terrestrial claim"),
                              ("satellite", "Satellite claim"), ("unserved", "Map-unserved"))]
    fig.legend(handles=handles, loc="outside upper center", ncol=3, frameon=False, fontsize=8)

    y = np.arange(len(TOWNS))
    terr = np.array([100 * int(data[t]["terrestrial_coded_block_households"]) / int(data[t]["households"]) for t in TOWNS])
    sat = np.array([100 * int(data[t]["satellite_coded_block_households"]) / int(data[t]["households"]) for t in TOWNS])
    uns = np.array([100 * int(data[t]["map_unserved_block_households"]) / int(data[t]["households"]) for t in TOWNS])
    axb.barh(y, terr, height=.54, color=navy)
    axb.barh(y, sat, height=.54, left=terr, color=teal)
    axb.barh(y, uns, height=.54, left=terr + sat, color=GREY)
    subs = [100 * float(data[t]["subscription_rate"]) for t in TOWNS]
    axb.scatter(subs, y, marker="o", color="black", s=16, zorder=5)
    axb.set(yticks=y, yticklabels=TOWNS, xlim=(0, 104),
            xlabel="Share of households (%)")
    axb.invert_yaxis()
    axb.grid(axis="x", alpha=.3)
    axb.set_title("(b) Claimed coverage vs subscriptions", fontsize=9, pad=2)
    save(fig, out / "fig_coverage.svg")

    # Figure 3: road-signal diagnostic and reclassification scenarios.
    diag = {r["provider_technology"]: r for r in read(out / "task1_north_diagnostics.csv")}
    order = ["cable", "fiber", "fixed_wireless", "none", "satellite"]
    names = ["Cable", "Fiber", "Fixed wireless", "No claim", "Satellite"]
    weak = [float(diag[k]["miles_at_or_below_-110_dbm"]) for k in order]
    strong = [float(diag[k]["surveyed_road_miles"]) - w for k, w in zip(order, weak)]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.5, 2.6), layout="constrained",
                                   gridspec_kw={"width_ratios": [1.35, 1]})
    yy = np.arange(len(order))
    ax1.barh(yy, strong, color=GREY, label="above -110 dBm")
    ax1.barh(yy, weak, left=strong, color=navy, label="at or below -110 dBm")
    for i, (s, w) in enumerate(zip(strong, weak)):
        if w > .3:
            ax1.text(s + w + .5, i, f"{w:.2f} mi", va="center", fontsize=8.5, color=navy)
    ax1.set(yticks=yy, yticklabels=names, xlabel="Surveyed road miles", xlim=(0, 30))
    ax1.invert_yaxis()
    ax1.set_title("(a) Road-signal evidence", fontsize=9.5)
    ax1.legend(loc="upper right", frameon=False)
    ax1.grid(axis="x", alpha=.3)

    challenge = {r["scenario"]: r for r in read(out / "task1_challenge.csv")}
    keys = ("challenge_none_upheld", "challenge_quarter_upheld",
            "challenge_half_upheld", "challenge_all_upheld")
    vals = [int(challenge[k]["households_reclassified"]) for k in keys]
    ax2.bar(["0%", "25%", "50%", "100%"], vals, color=[GREY, gold, teal, navy])
    ax2.bar_label(ax2.containers[0], labels=[f"{v:,}" for v in vals], fontsize=8.5, padding=2)
    ax2.set(title="(b) North Ridge reclassification", ylabel="Households",
            xlabel="Share of satellite-only addresses verified")
    ax2.set_ylim(0, 1750)
    ax2.grid(axis="y", alpha=.3)
    save(fig, out / "fig_signal.svg")

    # Figure 5: tornado sensitivity of new coverage.
    base = int(t2["block_base"]["new_hh"])
    params = (
        ("Wireless serviceability", "wireless_pass_minus10pp", "wireless_pass_plus10pp"),
        ("Budget", "block_budget_8m", "block_budget_14m"),
        ("Fiber route cost", "fiber_underground_median", "fiber_aerial_q1"),
        ("Maintenance rate", "block_om_125pct", "block_om_75pct"),
    )
    lows = [int(t2[k]["new_hh"]) - base for _, k, _ in params]
    highs = [int(t2[k]["new_hh"]) - base for _, _, k in params]
    labels = [p[0] for p in params]
    yy = np.arange(len(params))
    fig, ax = plt.subplots(figsize=(6.5, 2.5), layout="constrained")
    ax.barh(yy, lows, color=teal, height=.52, label="low end of range")
    ax.barh(yy, highs, color=navy, height=.52, label="high end of range")
    for i, (lo, hi) in enumerate(zip(lows, highs)):
        ax.text(lo - 12, i, f"{lo:+d}", va="center", ha="right", fontsize=8.5, color=teal)
        ax.text(hi + 12, i, f"{hi:+d}", va="center", ha="left", fontsize=8.5, color=navy)
    ax.axvline(0, color="black", lw=.8)
    ax.set(yticks=yy, yticklabels=labels, xlabel="Change in new household opportunities from the 4,213 base")
    ax.invert_yaxis()
    ax.set_xlim(-480, 480)
    ax.legend(loc="lower right", frameon=False)
    ax.grid(axis="x", alpha=.3)
    save(fig, out / "fig_tornado.svg")

    # Figure 6: budget-coverage frontier and marginal cost.
    t3 = {(r["scenario"], r["mechanism"]): r for r in read(out / "task3_summary.csv")}
    frontier = [(float(t2["block_budget_8m"]["budget_usd"]) / 1e6, int(t2["block_budget_8m"]["new_hh"])),
                (9.0, int(t3["budget-9m", "cooperative"]["new_hh"])),
                (float(t2["block_base"]["budget_usd"]) / 1e6, int(t2["block_base"]["new_hh"])),
                (13.0, int(t3["budget-13m", "cooperative"]["new_hh"])),
                (float(t2["block_budget_14m"]["budget_usd"]) / 1e6, int(t2["block_budget_14m"]["new_hh"]))]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.5, 2.6), layout="constrained",
                                   gridspec_kw={"width_ratios": [1.2, 1]})
    xs = [p[0] for p in frontier]
    ys = [p[1] for p in frontier]
    ax1.plot(xs, ys, marker="o", color=navy, lw=1.3, ms=4.5)
    for x, y in frontier:
        ax1.annotate(f"{y:,}", (x, y), textcoords="offset points", xytext=(2, 8), fontsize=8, ha="center")
    ax1.set(xlabel="Budget (million 2026 USD)", ylabel="New household opportunities",
            xticks=[8, 9, 11, 13, 14], ylim=(3700, 4600))
    ax1.set_title("(a) Budget-coverage frontier", fontsize=9.5)
    ax1.grid(alpha=.3)
    marginal = [(8, 11, (int(t2["block_base"]["new_hh"]) - int(t2["block_budget_8m"]["new_hh"])) / 3.0),
                (11, 14, (int(t2["block_budget_14m"]["new_hh"]) - int(t2["block_base"]["new_hh"])) / 3.0)]
    seg = [f"{a}-{b}m" for a, b, _ in marginal]
    cost_per = [(int(t2["block_base"]["lifecycle_usd"]) - int(t2["block_budget_8m"]["lifecycle_usd"]))
                / (int(t2["block_base"]["new_hh"]) - int(t2["block_budget_8m"]["new_hh"])),
                (int(t2["block_budget_14m"]["lifecycle_usd"]) - int(t2["block_base"]["lifecycle_usd"]))
                / (int(t2["block_budget_14m"]["new_hh"]) - int(t2["block_base"]["new_hh"]))]
    average = int(t2["block_base"]["lifecycle_usd"]) / int(t2["block_base"]["new_hh"])
    ax2.bar(seg + ["average"], cost_per + [average], color=[teal, navy, GREY])
    ax2.bar_label(ax2.containers[0], labels=[f"${c:,.0f}" for c in cost_per] + [f"${average:,.0f}"],
                  fontsize=8.5, padding=2)
    ax2.set(ylabel="Cost per added household (USD)", ylim=(0, 16000))
    ax2.set_title("(b) Marginal cost of coverage", fontsize=9.5)
    ax2.grid(axis="y", alpha=.3)
    save(fig, out / "fig_pareto.svg")

    # Figure 7: life-cycle cost structure of the mechanisms.
    mk = ("cooperative", "competitive", "county PPP")
    block3 = {m: t3[("block", m)] for m in mk}
    bh = np.array([float(block3[m]["backhaul_capex"]) for m in mk]) / 1e6
    lm = np.array([float(block3[m]["last_mile_capex"]) for m in mk]) / 1e6
    om = np.array([float(block3[m]["o_and_m_pv"]) for m in mk]) / 1e6
    net = np.array([float(block3[m]["net_county_outlay"]) for m in mk]) / 1e6
    x = np.arange(len(mk))
    fig, ax = plt.subplots(figsize=(6.5, 2.6), layout="constrained")
    ax.bar(x, bh, width=.5, color=navy, label="Backhaul")
    ax.bar(x, lm, width=.5, bottom=bh, color=teal, label="Last mile")
    ax.bar(x, om, width=.5, bottom=bh + lm, color=gold, label="O&M (present value)")
    ax.scatter(x, net, marker="D", s=34, color="black", zorder=5, label="County net outlay")
    for i in range(len(mk)):
        ax.text(i, bh[i] + lm[i] + om[i] + .28, f"${bh[i] + lm[i] + om[i]:.2f}m",
                ha="center", fontsize=8.5)
        ax.text(i + .26, net[i] - .42, f"${net[i]:.2f}m", ha="center", fontsize=8, color="black")
    ax.set(xticks=x, xticklabels=[MECHANISMS[m] for m in mk], ylabel="Million 2026 USD",
           ylim=(0, 12.6))
    ax.legend(loc="upper center", bbox_to_anchor=(.5, 1.15), ncol=4, frameon=False, fontsize=8)
    ax.grid(axis="y", alpha=.3)
    save(fig, out / "fig_cost.svg")

    # Figure 8: mechanism ranking across tested scenarios.
    scenarios = (("Base", "block"), ("Budget $9m", "budget-9m"), ("Budget $13m", "budget-13m"),
                 ("O&M 75%", "low-maintenance"), ("O&M 125%", "high-maintenance"),
                 ("Verified overlay", "verified"))
    x = np.arange(len(scenarios))
    fig, ax = plt.subplots(figsize=(6.5, 2.6), layout="constrained")
    for offset, mechanism, color, label in zip((-.25, 0, .25), mk, COLORS,
                                               ("Cooperative", "Competitive tender", "County PPP")):
        values = [int(t3[(scene, mechanism)]["new_hh"]) for _, scene in scenarios]
        ax.bar(x + offset, values, width=.24, color=color, label=label)
    ax.set(xticks=x, xticklabels=[name for name, _ in scenarios], ylim=(0, 6400),
           ylabel="New household opportunities")
    ax.grid(axis="y", alpha=.3)
    ax.legend(loc="upper center", bbox_to_anchor=(.5, 1.15), ncol=3, frameon=False)
    save(fig, out / "fig_robust.svg")

    # Figure 9: who gains access, and how measurement changes the answer.
    subs_rate = {r["township"]: 100 * float(r["subscription_rate"])
                 for r in read(out / "task1_townships.csv")}
    y = np.arange(len(TOWNS))
    gain = [100 * float(towns["block", recommended, t]["new_share"]) for t in TOWNS]
    subs = [subs_rate[t] for t in TOWNS]
    post = [100 * float(towns["block", recommended, t]["post_rate"]) for t in TOWNS]
    fig, ax = plt.subplots(figsize=(6.5, 2.05), layout="constrained")
    ax.barh(y - .22, gain, height=.2, color=navy, label="New households gaining access (% of town)")
    ax.barh(y, subs, height=.2, color=teal, label="Baseline subscription rate (%)")
    ax.barh(y + .22, post, height=.2, color=GREY, label="Post-plan access on the claim proxy (%)")
    ax.set(yticks=y, yticklabels=TOWNS, xlim=(0, 104), xlabel="Percent")
    ax.invert_yaxis()
    ax.grid(axis="x", alpha=.3)
    ax.legend(loc="upper center", bbox_to_anchor=(.5, 1.17), ncol=2, frameon=False, fontsize=7.8)
    save(fig, out / "fig_benefit.svg")

    schematic(out)
    workflow(out)


def build(out):
    t1 = {r["township"]: r for r in read(out / "task1_townships.csv")}
    challenges = read(out / "task1_challenge.csv")
    t2 = {r["scenario"]: r for r in read(out / "task2_scenarios.csv")}
    m3 = {(r["scenario"], r["mechanism"]): r for r in read(out / "task3_summary.csv")}
    t3 = {(r["scenario"], r["mechanism"], r["town"]): r for r in read(out / "task3_towns.csv")}
    audit = json.loads((out / "task1_data_audit.json").read_text(encoding="utf-8"))
    assert set(t1) == set(TOWNS) and all(r["strictly_eligible"] == "0" for r in t1.values())
    assert t2["strict"]["status"] == "infeasible" and t2["strict_without_floor"]["new_hh"] == "0"
    assert all(m3["strict", m]["status"] == "infeasible" for m in MECHANISMS)
    accept, denied, partial_low, partial_high, full = challenges
    assert all(r["north_strictly_eligible"] == "0" for r in challenges)
    challenge_fee = dollars(round(float(full["admin_cost_usd"])))
    timing = (f'{full["conceded_scenario_max_days_from_prep_start"]} d conceded / '
              f'{full["contested_scenario_max_days_from_prep_start"]} d contested')

    base = t2["block_base"]
    base_hh = int(base["new_hh"])
    outcome = ("block", "county PPP")
    ranking = sorted(MECHANISMS, key=lambda m: int(m3["block", m]["new_hh"]), reverse=True)
    assert ranking == ["county PPP", "cooperative", "competitive"]
    assert ranking == sorted(MECHANISMS, key=lambda m: int(m3["verified", m]["new_hh"]), reverse=True)
    ppp, coop, tender = (m3["block", m] for m in ranking)
    override = m3["verified", "county PPP"]
    assert base["new_hh"] == coop["new_hh"] and base["lifecycle_usd"] == coop["gross_cost"]

    def by_town(scene):
        return sorted(TOWNS, key=lambda t: int(t3[scene, ranking[0], t]["new_hh"]), reverse=True)

    best, counterfactual, certified = (by_town(s)[0] for s in ("block", "no-equity", "verified"))
    assert best == counterfactual
    assert all(t3[*outcome, t]["new_hh"] == t3["no-equity", ranking[0], t]["new_hh"] for t in TOWNS)
    best_hh = count(t3[*outcome, best]["new_hh"])
    advantage = count(int(ppp["new_hh"]) - int(coop["new_hh"]))
    lead_vs_tender = count(int(ppp["new_hh"]) - int(tender["new_hh"]))
    ppp_count, coop_count, tender_count = (count(r["new_hh"]) for r in (ppp, coop, tender))
    override_count = count(override["new_hh"])

    def delta_label(r):
        if r["new_hh"] in ("", None):
            return "-"
        d = int(r["new_hh"]) - base_hh
        return "0" if d == 0 else f"{d:+d}"

    scenarios = (
        ("Base", "block_base"),
        ("Fiber, aerial Q1", "fiber_aerial_q1"),
        ("Fiber, underground median", "fiber_underground_median"),
        ("Wireless serviceability -10 pp", "wireless_pass_minus10pp"),
        ("Wireless serviceability +10 pp", "wireless_pass_plus10pp"),
        ("Budget $8m", "block_budget_8m"),
        ("Budget $14m", "block_budget_14m"),
        ("O&M 75% of base", "block_om_75pct"),
        ("O&M 125% of base", "block_om_125pct"),
    )
    fiber_span = int(t2["fiber_aerial_q1"]["new_hh"]) - int(t2["fiber_underground_median"]["new_hh"])
    wireless_span = int(t2["wireless_pass_plus10pp"]["new_hh"]) - int(t2["wireless_pass_minus10pp"]["new_hh"])

    def feas(label, key, floor):
        r = t2[key]
        if r["status"] == "infeasible":
            return [label, floor, "Infeasible", "-", "-", "-", "-"]
        return [label, floor, "Optimal", count(r["new_hh"]), million(r["lifecycle_usd"]),
                r["fiber_blocks"] + " / " + r["wireless_blocks"], pct(r["min_town_pct"])]

    # Deployment table for the recommended county partnership.
    actions = [r for r in read(out / "task3_actions.csv")
               if r["scenario"] == "block" and r["mechanism"] == "county PPP"]
    hubs = {r["town"]: r for r in read(out / "task3_hubs.csv") if r["scenario"] == "block"}
    deployment = []
    fibers = [r for r in actions if r["technology"] == "F"]
    wireless = [r for r in actions if r["technology"] == "W"]
    for town in TOWNS:
        acts = [r for r in actions if r["town"] == town]
        act_f = [r for r in acts if r["technology"] == "F"]
        act_w = [r for r in acts if r["technology"] == "W"]
        hh_f = sum(int(r["hh"]) for r in act_f)
        hh_w = sum(int(r["hh"]) for r in act_w)
        gross = sum(int(r["backhaul"]) + int(r["last_mile"]) + int(r["o_and_m"]) for r in acts)
        if town in hubs:
            gross += int(hubs[town]["capex"]) + int(hubs[town]["o_and_m_pv"])
        deployment.append([town, f"{len(act_f)} / {len(act_w)}", count(hh_f), count(hh_w),
                           million(gross), f"${round(gross / max(1, hh_f + hh_w)):,}"])
    gross_total = (sum(int(r["backhaul"]) + int(r["last_mile"]) + int(r["o_and_m"]) for r in actions)
                   + sum(int(r["capex"]) + int(r["o_and_m_pv"]) for r in hubs.values()))
    hh_total = sum(int(r["hh"]) for r in actions)
    deployment.append(["Total", f"{len(fibers)} / {len(wireless)}",
                       count(sum(int(r["hh"]) for r in fibers)),
                       count(sum(int(r["hh"]) for r in wireless)),
                       million(gross_total), f"${round(gross_total / hh_total):,}"])

    county = audit["county_claim_decomposition"]
    pool = int(county["unserved"]["households"])
    verified_pool = pool + int(t1["North Ridge"]["satellite_coded_block_households"])
    post_rates = [float(t3[*outcome, t]["post_rate"]) for t in TOWNS]
    min_gap = 100 * (max(post_rates) - min(post_rates))
    values = {
        "budget": million(base["budget_usd"]),
        "t2_main_hh": count(base["new_hh"]),
        "t2_main_cost": million(base["lifecycle_usd"]),
        "sensitivity_summary": f"Across the tested ranges, wireless serviceability shifts new coverage by {wireless_span} households, versus {fiber_span} for the fiber route cost.",
        "recommendation_summary": f"County-owned backhaul with open-access leases adds {ppp_count} opportunities, {advantage} more than the next-best cooperative award.",
        "override_summary": f"With a verified North Ridge override the county partnership stays first at {override_count} additions.",
        "equity_summary": f"{best} gains the most from the first-phase partnership ({best_hh} households), with or without the floor in this scenario.",
        "executive_mechanism": f"The county partnership delivers {ppp_count} new opportunities under this reform. The cooperative can deliver {coop_count} and is the best fallback if lease commitments or route costs defeat the case for a public backbone.",
        "ppp_hh": ppp_count, "coop_hh": coop_count, "tender_hh": tender_count,
        "advantage": advantage, "tender_gap": lead_vs_tender,
        "ppp_cost": million(ppp["gross_cost"]), "coop_cost": million(coop["gross_cost"]),
        "ppp_min": pct(float(ppp["min_access_rate"]) * 100),
        "coop_min": pct(float(coop["min_access_rate"]) * 100),
        "ppp_capex": dollars(ppp["county_backhaul_capex"]),
        "ppp_om": dollars(ppp["county_o_and_m_pv"]),
        "ppp_rent": dollars(ppp["lease_received_pv"]),
        "net_outlay": million(ppp["net_county_outlay"]),
        "om_recovery": pct(100 * int(ppp["lease_received_pv"]) / int(ppp["county_o_and_m_pv"])),
        "override_count": override_count,
        "best_name": best, "best_hh": best_hh,
        "best_share": pct(100 * float(t3[*outcome, best]["new_share"])),
        "verified_best_name": certified,
        "verified_best_hh": count(t3["verified", ranking[0], certified]["new_hh"]),
        "min_funding": dollars(t2["block_min_budget"]["lifecycle_usd"]),
        "min_funding_new": count(t2["block_min_budget"]["new_hh"]),
        "verified_50_min_funding": dollars(t2["verified_50pct_min_budget"]["lifecycle_usd"]),
        "wireless_span": count(wireless_span),
        "fiber_span": count(fiber_span),
        "county_sat_blocks": count(county["satellite"]["blocks"]),
        "county_sat_hh": count(county["satellite"]["households"]),
        "county_terr_blocks": count(county["terrestrial"]["blocks"]),
        "county_unserved_hh": count(pool),
        "county_sat_share": pct(100 * county["satellite"]["households"] / 14496),
        "pool_share": pct(100 * base_hh / pool),
        "verified_pool_share": pct(100 * int(override["new_hh"]) / verified_pool),
        "marginal_8_11": dollars((int(base["lifecycle_usd"]) - int(t2["block_budget_8m"]["lifecycle_usd"]))
                                 / (base_hh - int(t2["block_budget_8m"]["new_hh"]))),
        "marginal_11_14": dollars((int(t2["block_budget_14m"]["lifecycle_usd"]) - int(base["lifecycle_usd"]))
                                  / (int(t2["block_budget_14m"]["new_hh"]) - base_hh)),
        "average_cost": dollars(int(base["lifecycle_usd"]) / base_hh),
        "audit_cost": dollars(round(float(full["admin_cost_usd"]))),
        "audit_share": pct(100 * float(full["admin_cost_usd"]) / 11_000_000),
        "audit_unlock": count(int(t3["verified", ranking[0], "North Ridge"]["new_hh"])
                              - int(t3["block", ranking[0], "North Ridge"]["new_hh"])),
        "floor_slack": "2.54 pp",
        "min_gap": f"{min_gap:.2f} pp",
        "south_claim": pct(100 * int(t1["South Hollow"]["terrestrial_coded_block_households"])
                           / int(t1["South Hollow"]["households"])),
        "south_sub": pct(100 * float(t1["South Hollow"]["subscription_rate"])),
        "south_gain": count(int(t3[*outcome, "South Hollow"]["new_hh"])),
        "county_sub_rate": pct(100 * 6591 / 14496),
    }
    rows = {
        "townships": [
            [t, count(r["households"]), count(r["subscriptions"]), pct(float(r["subscription_rate"]) * 100),
             r["reported_served_blocks"], r["terrestrial_coded_blocks"],
             count(r["satellite_coded_block_households"]), count(r["map_unserved_block_households"])]
            for t in TOWNS for r in [t1[t]]
        ] + [["County total", count(sum(int(r["households"]) for r in t1.values())),
              count(sum(int(r["subscriptions"]) for r in t1.values())),
              pct(100 * sum(int(r["subscriptions"]) for r in t1.values())
                  / sum(int(r["households"]) for r in t1.values())),
              sum(int(r["reported_served_blocks"]) for r in t1.values()),
              sum(int(r["terrestrial_coded_blocks"]) for r in t1.values()),
              count(sum(int(r["satellite_coded_block_households"]) for r in t1.values())),
              count(sum(int(r["map_unserved_block_households"]) for r in t1.values()))]],
        "challenge": [
            ["Accept", f'{dollars(round(float(accept["admin_cost_usd"])))} / no extra delay',
             "No reclassification. No town eligible."],
            ["Challenge fails", challenge_fee + " / timing varies",
             f'{denied["households_reclassified"]} households reclassified. No town eligible.'],
            ["25% verified", challenge_fee + " / " + timing,
             f'{count(partial_low["households_reclassified"])} households. No town eligible.'],
            ["50% verified", challenge_fee + " / " + timing,
             f'{count(partial_high["households_reclassified"])} households. No town eligible.'],
            ["Full targeted success", challenge_fee + " / " + timing,
             f'{count(full["households_reclassified"])} households. Four North Ridge flags still block funding.'],
        ],
        "feasibility": [
            feas("Strict township rule", "strict", "25%"),
            feas("Strict, floor removed", "strict_without_floor", "0%"),
            feas("Block eligibility", "block_base", "25%"),
            feas("Block eligibility, min. outlay", "block_min_budget", "25%"),
            feas("Block eligibility", "block_50pct", "50%"),
            feas("Verified overlay", "verified_base", "25%"),
            feas("Verified overlay, min. outlay", "verified_50pct_min_budget", "50%"),
        ],
        "deployment": deployment,
        "sensitivity": [
            [label, count(t2[key]["new_hh"]), million(t2[key]["lifecycle_usd"]),
             t2[key]["fiber_blocks"] + " / " + t2[key]["wireless_blocks"],
             pct(t2[key]["min_town_pct"]), delta_label(t2[key])]
            for label, key in scenarios
        ],
        "mechanisms": [
            [MECHANISMS[m], count(r["new_hh"]), million(r["gross_cost"]),
             dollars(round(float(r["cost_per_new_hh"]))), pct(float(r["min_access_rate"]) * 100),
             r["fiber_blocks"] + " / " + r["wireless_blocks"]]
            for m in MECHANISMS for r in [m3["block", m]]
        ],
        "verified": [
            [MECHANISMS[m], count(r["new_hh"]), million(r["gross_cost"]),
             pct(float(r["min_access_rate"]) * 100), r["open_hubs"]]
            for m in MECHANISMS for r in [m3["verified", m]]
        ],
        "benefits": [
            [t, count(t3[*outcome, t]["new_hh"]),
             pct(100 * int(t3[*outcome, t]["new_hh"]) / int(t1[t]["map_unserved_block_households"])),
             pct(100 * float(t3[*outcome, t]["post_rate"])), pct(100 * float(t1[t]["subscription_rate"]))]
            for t in TOWNS
        ],
    }
    (out / "paper_data.json").write_text(json.dumps({"values": values, "rows": rows}, indent=2,
                                                  ensure_ascii=False) + "\n", encoding="utf-8")
    charts(out, t1, m3, t3, ranking[0], t2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path("results"))
    build(parser.parse_args().out)
