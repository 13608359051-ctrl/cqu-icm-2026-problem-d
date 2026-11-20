"""Independent reconstruction of Task 3 from the raw blocks and the model specification."""

import argparse
import csv
import json
import math
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path
from statistics import median
from typing import NamedTuple

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp


BUDGET = 11_000_000
ANNUITY = sum(1.03 ** -year for year in range(1, 11))
TERRESTRIAL = {"fiber", "cable", "fixed_wireless"}
STRESS = {
    "budget-9m": {"budget": 9_000_000},
    "budget-13m": {"budget": 13_000_000},
    "low-maintenance": {"maintenance_factor": .75},
    "high-maintenance": {"maintenance_factor": 1.5},
    "verified-50pct": {"floor": .50},
}


class Block(NamedTuple):
    bid: str
    town: str
    hh: int
    subs: int
    served: bool
    tech: str
    dist: float
    terrain: int


class Action(NamedTuple):
    block: Block
    tech: str
    operator: str
    hub: str
    hh: int
    backhaul: int
    last_mile: int
    maintenance: int


def operating_value(tech, capex):
    return round(ANNUITY * (0.018 if tech == "fiber" else 0.035) * capex)


def offer(block, tech, operator, hub="", backhaul_scale=1, last_mile_scale=1):
    grade = block.terrain - 1
    if tech == "fiber":
        hh = block.hh
        backhaul = round(42240 * block.dist * (1 + .16 * grade))
        last_mile = round(980 * hh * (1 + .10 * grade))
    else:
        hh = block.hh * (80, 75, 70, 62, 55)[grade] // 100
        backhaul = round(5500 * block.dist * (1 + .10 * grade))
        last_mile = round(28000 * (1 + .08 * grade) + 480 * hh)
    backhaul, last_mile = round(backhaul * backhaul_scale), round(last_mile * last_mile_scale)
    return Action(block, tech, operator, hub, hh, backhaul, last_mile,
                  operating_value(tech, backhaul + last_mile))


def cost_of(action):
    return action.backhaul + action.last_mile + action.maintenance


def solve(rows, mechanism, regime, equity=True, footprint_delta=0, hub_factor=1,
          budget=BUDGET, maintenance_factor=1, floor=.25):
    by_town = defaultdict(list)
    for entry in rows:
        by_town[entry.town].append(entry)
    totals = {town: sum(b.hh for b in bs) for town, bs in by_town.items()}
    baseline = {town: sum(b.hh for b in bs if b.tech in TERRESTRIAL)
                for town, bs in by_town.items()}
    deficits = {town: max(0, math.ceil(floor * totals[town]) - baseline[town])
                if equity else 0 for town in by_town}
    hub_spec = {}
    actions = []
    for town, bs in by_town.items():
        mapped_out = [b for b in bs if not b.served]
        cable_town = any(b.tech == "cable" for b in bs)
        wireless_town = any(b.tech == "fixed_wireless" for b in bs)
        if regime == "strict":
            candidates = [] if any(b.served for b in bs) else mapped_out
        else:
            candidates = mapped_out + [b for b in bs if regime == "verified"
                                       and b.town == "North Ridge" and b.tech == "satellite"]
        if mechanism == "ppp" and candidates:
            hub_dist = median(b.dist for b in mapped_out)
            hub_grade = median(b.terrain for b in mapped_out) - 1
            hub_capex = round(hub_factor * (25000 + 42240 * hub_dist * (1 + .16 * hub_grade)))
            hub_spec[town] = (hub_dist, hub_capex,
                              round(maintenance_factor * operating_value("fiber", hub_capex)))
        for b in candidates:
            feasible = defaultdict(list)
            if mechanism == "coop" or b.dist <= 13 + footprint_delta:
                for tech in ("fiber", "wireless"):
                    feasible[tech, ""].append(offer(b, tech, "coop"))
            if mechanism != "coop":
                if cable_town and b.dist <= 6 + footprint_delta:
                    feasible["fiber", ""].append(offer(b, "fiber", "cable", "", .70, .90))
                if wireless_town and b.dist <= 9 + footprint_delta:
                    feasible["wireless", ""].append(offer(b, "wireless", "startup", "", .75, .95))
            if mechanism == "ppp":
                lateral = abs(b.dist - hub_spec[town][0]) + .5
                for operator, technologies, radius, discount in (
                    ("coop", ("fiber", "wireless"), 6, 1),
                    ("cable", ("fiber",), 4, .90), ("startup", ("wireless",), 5, .95),
                ):
                    if lateral <= radius + footprint_delta:
                        for tech in technologies:
                            feasible[tech, town].append(offer(
                                b, tech, operator, town, lateral / b.dist, discount))
            for options in feasible.values():
                action = min(options, key=cost_of)
                actions.append(action._replace(maintenance=round(maintenance_factor * action.maintenance)))

    if not actions:
        assert regime == "strict" and all(any(b.served for b in bs) for bs in by_town.values())
        return {"status": "infeasible" if any(deficits.values()) else "optimal",
                "eligible_actions": 0, "town_deficits": deficits,
                "new_households_under_eligibility": 0}

    hubs = list(hub_spec)
    n = len(actions)
    costs = np.array([cost_of(a) for a in actions] + [sum(hub_spec[t][1:]) for t in hubs])
    gains = np.array([a.hh for a in actions] + [0] * len(hubs))
    matrix = []
    lower = []
    upper = []

    def constraint(values, lo=-np.inf, hi=np.inf):
        matrix.append(values)
        lower.append(lo)
        upper.append(hi)

    constraint(costs, hi=budget)
    for bid in {a.block.bid for a in actions}:
        constraint([int(a.block.bid == bid) for a in actions] + [0] * len(hubs), hi=1)
    for town, deficit in deficits.items():
        constraint([a.hh if a.block.town == town else 0 for a in actions] + [0] * len(hubs),
                   lo=deficit)
    if hubs:
        constraint([0] * n + [1] * len(hubs), lo=1)
    for j, town in enumerate(hubs):
        loads = [int(a.hub == town) for a in actions]
        flag = [int(k == j) for k in range(len(hubs))]
        constraint(loads + [-2 * x for x in flag], lo=0)
        constraint(loads + [-sum(loads) * x for x in flag], hi=0)

    def optimize(objective):
        return milp(objective, integrality=np.ones(len(costs)), bounds=Bounds(0, 1),
                    constraints=LinearConstraint(np.asarray(matrix), lower, upper),
                    options={"mip_rel_gap": 0, "time_limit": 80})

    coverage = optimize(-gains)
    if coverage.status == 2:
        return {"status": "infeasible", "eligible_actions": n, "town_deficits": deficits}
    assert coverage.status == 0, (mechanism, regime, coverage.message)
    constraint(gains, lo=round(-coverage.fun), hi=round(-coverage.fun))
    expense = optimize(costs)
    assert expense.status == 0, (mechanism, regime, expense.message)
    picks = [a for a, use in zip(actions, expense.x[:n]) if use > .5]
    open_hubs = [town for town, use in zip(hubs, expense.x[n:]) if use > .5]
    township_gains = {t: sum(a.hh for a in picks if a.block.town == t) for t in totals}
    by_tech = Counter(a.tech for a in picks)
    leases = sorted({(a.hub, a.operator) for a in picks if a.hub})
    hub_capex = sum(hub_spec[t][1] for t in open_hubs)
    hub_maintenance = sum(hub_spec[t][2] for t in open_hubs)
    backhaul = sum(a.backhaul for a in picks)
    last_mile = sum(a.last_mile for a in picks)
    last_mile_maintenance = sum(a.maintenance for a in picks)
    gross = backhaul + last_mile + last_mile_maintenance + hub_capex + hub_maintenance
    assert len({a.block.bid for a in picks}) == len(picks)
    assert all(township_gains[t] >= deficits[t] for t in totals)
    assert gross == round(expense.fun) <= budget
    assert sum(township_gains.values()) == round(-coverage.fun)
    assert all(a.hub in open_hubs for a in picks if a.hub)
    assert all(sum(a.hub == t for a in picks) >= 2 for t in open_hubs)
    return {
        "status": "optimal", "coverage_gap": coverage.mip_gap, "cost_gap": expense.mip_gap,
        "new_households": sum(township_gains.values()), "gross_pv_usd": gross,
        "township_gains": township_gains,
        "post_access": {t: (baseline[t] + township_gains[t]) / totals[t] for t in totals},
        "technology_counts": dict(by_tech), "opened_hubs": open_hubs,
        "leases": leases, "lease_pv_usd": len(leases) * round(ANNUITY * 4800),
        "provider_backhaul_capex": backhaul, "last_mile_capex": last_mile,
        "provider_maintenance_pv": last_mile_maintenance,
        "county_backhaul_capex": hub_capex, "county_maintenance_pv": hub_maintenance,
        "pick_keys": sorted((a.block.bid, a.tech, a.operator, bool(a.hub)) for a in picks),
    }


def compare(results, directory):
    def read(name):
        with (directory / f"task3_{name}.csv").open(encoding="utf-8-sig", newline="") as source:
            return list(csv.DictReader(source))

    summary, actions, towns, hubs, providers, finance = map(
        read, ("summary", "actions", "towns", "hubs", "providers", "finance")
    )
    model_names = {"cooperative": "coop", "competitive": "tender", "county PPP": "ppp"}
    operators = {"regional cooperative": "coop", "national cable operator": "cable",
                 "fixed wireless entrant": "startup"}
    assert len(summary) == len(results) - 1 == 31
    for author in summary:
        model = model_names[author["mechanism"]]
        case = author["scenario"]
        delta = {"narrow-footprints": -2, "wide-footprints": 2}.get(case, 0)
        factor = {"low-hub-cost": .75, "high-hub-cost": 2}.get(case, 1)
        key = (f"{model}/{author['rule']}/equity={case != 'no-equity'}"
               f"/footprint={delta}/hub={factor}")
        if case in STRESS:
            key += f"/{case}"
        check = results[key]
        assert check["status"] == author["status"], key

        def relevant(rows):
            return [r for r in rows if r["scenario"] == case
                    and r["mechanism"] == author["mechanism"]]

        selected = relevant(actions)
        if check["status"] == "infeasible":
            assert not selected and not relevant(hubs), key
            assert {r["town"]: int(r["equity_deficit_hh"]) for r in relevant(towns)} == (
                check["town_deficits"]
            ), key
            continue
        expected = {
            "new_hh": check["new_households"], "gross_cost": check["gross_pv_usd"],
            "backhaul_capex": check["provider_backhaul_capex"] + check["county_backhaul_capex"],
            "last_mile_capex": check["last_mile_capex"],
            "o_and_m_pv": check["provider_maintenance_pv"] + check["county_maintenance_pv"],
            "county_backhaul_capex": check["county_backhaul_capex"],
            "county_o_and_m_pv": check["county_maintenance_pv"],
            "lease_received_pv": check["lease_pv_usd"], "lease_paid_pv": check["lease_pv_usd"],
            "net_county_outlay": check["gross_pv_usd"] - check["lease_pv_usd"],
            "open_hubs": len(check["opened_hubs"]),
            "fiber_blocks": check["technology_counts"].get("fiber", 0),
            "wireless_blocks": check["technology_counts"].get("wireless", 0),
        }
        assert {k: int(author[k]) for k in expected} == expected, key
        assert float(author["gap"]) == check["coverage_gap"] == 0, key
        if author.get("cost_gap"):
            assert float(author["cost_gap"]) == check["cost_gap"] == 0, key
        assert math.isclose(float(author["min_access_rate"]), min(check["post_access"].values())), key
        keys = sorted((r["block"], {"F": "fiber", "W": "wireless"}[r["technology"]],
                       operators[r["provider"]], bool(r["hub"])) for r in selected)
        assert keys == check["pick_keys"], key
        assert {r["town"]: int(r["new_hh"]) for r in relevant(towns)} == check["township_gains"], key
        assert {r["town"] for r in relevant(hubs)} == set(check["opened_hubs"]), key
        assert sum(int(r["lease_paid_pv"]) for r in relevant(providers)) == check["lease_pv_usd"], key
    print(f"PASS: matching status and outputs for all {len(summary)} Task 3 runs.")

    # An exact rational discount factor verifies the rounded financing rows independently.
    annuity = sum(Fraction(100, 103) ** year for year in range(1, 11))
    fees = (0, 2400, 4800, 7200)
    assert len(finance) == 8 and {
        (row["scenario"], int(row["fee_per_lease_year"])) for row in finance
    } == {(scenario, fee) for scenario in ("block", "verified") for fee in fees}
    for row in finance:
        check = results[f"ppp/{row['scenario']}/equity=True/footprint=0/hub=1"]
        count = len(check["leases"])
        op_cost = check["county_maintenance_pv"]
        payment = count * round(annuity * int(row["fee_per_lease_year"]))
        expected = {
            "leases": count, "lease_pv": payment, "county_o_and_m_pv": op_cost,
            "county_om_funding_gap_pv": op_cost - payment,
            "net_county_outlay": check["gross_pv_usd"] - payment,
        }
        assert all(int(row[key]) == value for key, value in expected.items()), row
        assert math.isclose(float(row["om_break_even_fee_per_lease_year"]),
                            op_cost / (annuity * count)), row
    print("PASS: all 8 lease-price rows match exact rational discounting.")


def main(data, out, compare_dir):
    with (data / "blocks.csv").open(encoding="utf-8-sig", newline="") as source:
        rows = [Block(r["block_id"], r["township"], int(r["total_households"]),
                      int(r["subscription_households"]), r["provider_served"] == "1",
                      r["provider_technology"], float(r["distance_to_fiber_backbone_miles"]),
                      int(r["terrain_difficulty"])) for r in csv.DictReader(source)]
    assert len({r.bid for r in rows}) == len(rows) == 120
    hand = offer(Block("demo", "demo", 100, 0, False, "none", 2, 1), "wireless", "coop")
    assert hand.hh == 80 and hand.backhaul == 11000 and hand.last_mile == 66400
    assert offer(Block("demo", "demo", 90, 0, False, "none", 2, 3), "wireless", "coop").hh == 63
    models = ("coop", "tender", "ppp")
    cases = [(m, r, True, 0, 1, "") for m in models
             for r in ("strict", "block", "verified")]
    cases += [(m, "block", False, 0, 1, "") for m in models]
    cases += [("tender", "block", True, delta, 1, "") for delta in (-2, 2)]
    cases += [("ppp", "block", True, 0, factor, "") for factor in (.75, 2)]
    cases += [(m, "verified" if case == "verified-50pct" else "block", True, 0, 1, case)
              for m in models for case in STRESS]
    results = {}
    for m, r, equity, delta, factor, stress in cases:
        key = f"{m}/{r}/equity={equity}/footprint={delta}/hub={factor}"
        if stress:
            key += f"/{stress}"
        results[key] = solve(rows, m, r, equity, delta, factor, **STRESS.get(stress, {}))
        x = results[key]
        print(key, x["status"], x.get("new_households"), x.get("gross_pv_usd"), flush=True)
        out.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    south = [x for x in rows if x.town == "South Hollow"]
    fwa = [x for x in south if x.tech == "fixed_wireless"]
    results["south_raw_subscriptions"] = {
        "households": sum(x.hh for x in south), "subscriptions": sum(x.subs for x in south),
        "fixed_wireless_coded_blocks": len(fwa),
        "fixed_wireless_coded_households": sum(x.hh for x in fwa),
        "fixed_wireless_coded_subscriptions_all_technologies": sum(x.subs for x in fwa),
    }
    out.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    if compare_dir:
        compare(results, compare_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--compare", type=Path, help="Task 3 results folder for the post-solve comparison")
    args = parser.parse_args()
    main(args.data, args.out, args.compare)
