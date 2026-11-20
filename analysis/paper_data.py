"""Format verified analysis outputs for the paper and regenerate its figures."""

import argparse
import csv
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np


TOWNS = ("North Ridge", "East Corridor", "South Hollow", "West Plains", "Central Town", "River Bend")
MECHANISMS = {"cooperative": "Cooperative", "competitive": "Competitive tender", "county PPP": "County PPP"}
COLORS = ("#1e4665", "#178078", "#d28b36")


def read(path):
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def count(x):
    return f"{int(x):,}"


def dollars(x):
    return f"${int(x):,}"


def million(x):
    return f"${float(x) / 1e6:.3f}m"


def pct(x):
    return f"{float(x):.2f}%"


def save(fig, dest):
    fig.savefig(dest, bbox_inches="tight", pad_inches=.08, metadata={"Date": None})
    plt.close(fig)


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
                                    fc="#eef5f5", ec=COLORS[0], lw=1.2))
        ax.text(x + 1, y + .395, label, ha="center", va="center", fontsize=13)
    for start, end in [((2.15, 1.57), (5.95, 1.57)),
                       ((2.15, 1.17), (2.95, .58)),
                       ((5.05, .58), (5.95, 1.17))]:
        ax.annotate("", xy=end, xytext=start, arrowprops={"arrowstyle": "->", "color": COLORS[1], "lw": 1.5})
    ax.text(4.1, 1.82, "Direct backhaul + last mile", ha="center", fontsize=13)
    ax.text(1.93, .47, "County spur", ha="right", fontsize=12)
    ax.text(6.08, .47, "Tenant lateral + last mile", ha="left", fontsize=12)
    ax.text(.08, 2.42, "SERVICE PATHS  •  SCHEMATIC, NOT TO SCALE", color=COLORS[0], fontsize=11, weight="bold")
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
                                    fc="#fdf2e3" if title.startswith("2") else "#eef5f5",
                                    ec=COLORS[0], lw=1.15))
        ax.text(x + .15, y + .74, title, color=COLORS[0], fontsize=14, weight="bold", va="center")
        ax.text(x + .15, y + .37, label, color="#19272c", fontsize=13, va="center", linespacing=1.15)
    for start, end in [((3.65, 3.48), (4.33, 3.48)), ((6.15, 2.94), (6.15, 2.60)),
                       ((4.34, 2.04), (3.65, 2.04)), ((1.83, 1.49), (1.83, 1.16)),
                       ((3.65, .60), (4.33, .60))]:
        ax.annotate("", xy=end, xytext=start, arrowprops={"arrowstyle": "->", "color": COLORS[1], "lw": 1.75})
    save(fig, out / "fig_workflow.svg")


def charts(out, data, mechanisms, towns, recommended):
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 12, "svg.hashsalt": "cqu-d-2026",
                         "axes.spines.top": False, "axes.spines.right": False, "axes.axisbelow": True})
    fig, ax = plt.subplots(figsize=(8.1, 3.3), layout="constrained")
    y = np.arange(len(TOWNS))
    for offset, col, label, color in zip((-.22, 0, .22),
            ("reported_served_block_households", "terrestrial_coded_block_households", "subscriptions"),
            ("Any served flag", "Terrestrial claim", "Subscription"), COLORS):
        ax.barh(y + offset, [100 * int(data[t][col]) / int(data[t]["households"]) for t in TOWNS],
                height=.19, color=color, label=label)
    ax.set(yticks=y, yticklabels=TOWNS, xlim=(0, 100), xlabel="Share of township households (%)")
    ax.invert_yaxis()
    ax.grid(axis="x", alpha=.25)
    ax.legend(loc="lower center", bbox_to_anchor=(.5, 1.01), ncol=3, frameon=False)
    save(fig, out / "fig_coverage.svg")

    fig, ax = plt.subplots(figsize=(8.1, 3.1), layout="constrained")
    x = np.arange(3)
    for offset, scene, color, label in zip((-.18, .18), ("block", "verified"), COLORS,
                                             ("Block reform", "Verified North Ridge overlay")):
        hh = [int(mechanisms[scene, m]["new_hh"]) for m in MECHANISMS]
        ax.bar_label(ax.bar(x + offset, hh, width=.34, color=color, label=label),
                     labels=[f"{n:,}" for n in hh], padding=4, fontsize=11)
    ax.set(xticks=x, xticklabels=list(MECHANISMS.values()), ylim=(0, 6700),
           ylabel="New household opportunities")
    ax.grid(axis="y", alpha=.25)
    ax.legend(loc="lower center", bbox_to_anchor=(.5, 1.01), ncol=2, frameon=False)
    save(fig, out / "fig_tradeoff.svg")

    fig, ax = plt.subplots(figsize=(8.1, 3.1), layout="constrained")
    for offset, scene, color, label in zip((-.18, .18), ("block", "no-equity"), COLORS,
                                          ("25% floor", "Floor removed")):
        hh = [int(towns[scene, recommended, town]["new_hh"]) for town in TOWNS]
        ax.barh(y + offset, hh, height=.32, color=color, label=label)
    ax.set(yticks=y, yticklabels=TOWNS, xlabel="New household opportunities", xlim=(0, 1500))
    ax.invert_yaxis()
    ax.grid(axis="x", alpha=.25)
    ax.legend(loc="lower center", bbox_to_anchor=(.5, 1.01), ncol=2, frameon=False)
    save(fig, out / "fig_benefit.svg")
    schematic(out)
    workflow(out)


def build(out):
    t1 = {r["township"]: r for r in read(out / "task1_townships.csv")}
    challenges = read(out / "task1_challenge.csv")
    t2 = {r["scenario"]: r for r in read(out / "task2_scenarios.csv")}
    m3 = {(r["scenario"], r["mechanism"]): r for r in read(out / "task3_summary.csv")}
    t3 = {(r["scenario"], r["mechanism"], r["town"]): r for r in read(out / "task3_towns.csv")}
    assert set(t1) == set(TOWNS) and all(r["strictly_eligible"] == "0" for r in t1.values())
    assert t2["strict"]["status"] == "infeasible" and t2["strict_without_floor"]["new_hh"] == "0"
    assert all(m3["strict", m]["status"] == "infeasible" for m in MECHANISMS)
    accept, denied, partial_low, partial_high, full = challenges
    assert all(r["north_strictly_eligible"] == "0" for r in challenges)
    challenge_fee = dollars(round(float(full["admin_cost_usd"])))
    timing = (f'{full["conceded_scenario_max_days_from_prep_start"]} d conceded / '
              f'{full["contested_scenario_max_days_from_prep_start"]} d contested')

    base = t2["block_base"]
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
    costs = (
        ("Fiber, aerial Q1", "fiber_aerial_q1"),
        ("Base", "block_base"),
        ("Fiber, underground median", "fiber_underground_median"),
        ("Wireless pass −10 pp", "wireless_pass_minus10pp"),
        ("Wireless pass +10 pp", "wireless_pass_plus10pp"),
    )
    fiber_span = int(t2["fiber_aerial_q1"]["new_hh"]) - int(t2["fiber_underground_median"]["new_hh"])
    wireless_span = int(t2["wireless_pass_plus10pp"]["new_hh"]) - int(t2["wireless_pass_minus10pp"]["new_hh"])
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
    }
    rows = {
        "townships": [
            [t, count(r["households"]), count(r["subscriptions"]), pct(float(r["subscription_rate"]) * 100),
             r["reported_served_blocks"], count(r["terrestrial_coded_block_households"])]
            for t in TOWNS for r in [t1[t]]
        ],
        "challenge": [
            ["Accept", f'{dollars(round(float(accept["admin_cost_usd"])))} / no extra delay',
             "No reclassification. No town eligible."],
            ["Challenge fails", challenge_fee + " / timing varies",
             f'{denied["households_reclassified"]} households reclassified. No town eligible.'],
            ["Partial success", challenge_fee + " / " + timing,
             f'{count(partial_low["households_reclassified"])} or {count(partial_high["households_reclassified"])} households. No town eligible.'],
            ["Full targeted success", challenge_fee + " / " + timing,
             f'{count(full["households_reclassified"])} households. Four North Ridge flags still block funding.'],
        ],
        "sensitivity": [
            [label, count(r["new_hh"]), million(r["lifecycle_usd"]),
             r["fiber_blocks"] + " / " + r["wireless_blocks"], pct(r["min_town_pct"]),
             "+" + r["project_technology_pairs_added_vs_base"] + " / −" + r["project_technology_pairs_removed_vs_base"]]
            for label, key in costs for r in [t2[key]]
        ],
        "mechanisms": [
            [MECHANISMS[m], count(r["new_hh"]), million(r["gross_cost"]),
             dollars(round(float(r["cost_per_new_hh"]))), pct(float(r["min_access_rate"]) * 100),
             r["fiber_blocks"] + " / " + r["wireless_blocks"]]
            for m in MECHANISMS for r in [m3["block", m]]
        ],
        "lifecycle": [
            [MECHANISMS[m], million(r["backhaul_capex"]), million(r["last_mile_capex"]),
             million(r["o_and_m_pv"]), million(r["net_county_outlay"])]
            for m in MECHANISMS for r in [m3["block", m]]
        ],
        "verified": [
            [MECHANISMS[m], count(r["new_hh"]), million(r["gross_cost"]),
             pct(float(r["min_access_rate"]) * 100), r["open_hubs"]]
            for m in MECHANISMS for r in [m3["verified", m]]
        ],
        "benefits": [
            [t, count(t3[*outcome, t]["new_hh"]), pct(100 * float(t3[*outcome, t]["new_share"])),
             pct(100 * float(t3[*outcome, t]["post_rate"]))]
            for t in TOWNS
        ],
    }
    (out / "paper_data.json").write_text(json.dumps({"values": values, "rows": rows}, indent=2,
                                                  ensure_ascii=False) + "\n", encoding="utf-8")
    charts(out, t1, m3, t3, ranking[0])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path("results"))
    build(parser.parse_args().out)
