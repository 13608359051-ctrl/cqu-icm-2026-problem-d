"""Cross-check Task 2 with a raw-data multiple-choice knapsack, without importing its MILP."""

import argparse
import csv
import json
from collections import Counter, defaultdict
from fractions import Fraction
from math import ceil
from pathlib import Path


BUDGET = 11_000_000
CASES = {
    "strict": ("strict", 25, 42240, 0, 100, False),
    "strict_without_floor": ("strict", 0, 42240, 0, 100, False),
    "block_50pct": ("block", 50, 42240, 0, 100, False),
    "block_base": ("block", 25, 42240, 0, 100, False),
    "block_min_budget": ("block", 25, 42240, 0, 100, True),
    "verified_50pct": ("verified", 50, 42240, 0, 100, False),
    "verified_50pct_min_budget": ("verified", 50, 42240, 0, 100, True),
    "verified_base": ("verified", 25, 42240, 0, 100, False),
    "fiber_aerial_q1": ("block", 25, 25872, 0, 100, False),
    "fiber_underground_median": ("block", 25, 95040, 0, 100, False),
    "wireless_pass_minus10pp": ("block", 25, 42240, -10, 100, False),
    "wireless_pass_plus10pp": ("block", 25, 42240, 10, 100, False),
    "block_budget_8m": ("block", 25, 42240, 0, 100, False),
    "block_budget_14m": ("block", 25, 42240, 0, 100, False),
    "block_om_75pct": ("block", 25, 42240, 0, 100, False),
    "block_om_125pct": ("block", 25, 42240, 0, 100, False),
    "block_baseline_75pct": ("block", 25, 42240, 0, 75, False),
}
BUDGET_LIMITS = {"block_budget_8m": 8_000_000, "block_budget_14m": 14_000_000}
MAINTENANCE_SCALES = {"block_om_75pct": .75, "block_om_125pct": 1.25}


def read(path):
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def prune(costs):
    previous = float("inf")
    keep = {}
    for gain in sorted(costs, reverse=True):
        if costs[gain] < previous:
            previous = costs[gain]
            keep[gain] = previous
    return keep


def merge(left, right, budget):
    out = {}
    for left_gain, left_cost in left.items():
        for right_gain, right_cost in right.items():
            gain = left_gain + right_gain
            cost = left_cost + right_cost
            if cost <= budget and cost < out.get(gain, budget + 1):
                out[gain] = cost
    return prune(out)


def appraise(row, tech, line_cost, pass_shift, om_scale):
    distance = Fraction(row["distance_to_fiber_backbone_miles"])
    houses = int(row["total_households"])
    steps = int(row["terrain_difficulty"]) - 1
    annuity = (1 - (100 / 103) ** 10) / .03
    if tech == "F":
        gain = houses
        capital_backhaul = round(line_cost * distance * Fraction(100 + 16 * steps, 100))
        capital_last = round(980 * gain * Fraction(100 + 10 * steps, 100))
        operating_rate = .018
    else:
        gain = houses * ((80, 75, 70, 62, 55)[steps] + pass_shift) // 100
        capital_backhaul = round(5500 * distance * Fraction(100 + 10 * steps, 100))
        capital_last = round(28000 * Fraction(100 + 8 * steps, 100) + 480 * gain)
        operating_rate = .035
    maintenance = round((capital_backhaul + capital_last) * operating_rate * annuity * om_scale)
    return gain, capital_backhaul, capital_last, maintenance


def independent(blocks):
    homes, claims = Counter(), Counter()
    for row in blocks:
        homes[row["township"]] += int(row["total_households"])
        claims[row["township"]] += int(row["provider_served"])
    expected = {}
    for case, (rule, floor, line_cost, pass_shift, scale, min_cost) in CASES.items():
        budget = BUDGET_LIMITS.get(case, BUDGET)
        om_scale = MAINTENANCE_SCALES.get(case, 1)
        base, allowed = Counter(), {}
        for row in blocks:
            town = row["township"]
            hh = int(row["total_households"])
            tech = row["provider_technology"]
            served = int(row["provider_served"])
            if served and tech in ("fiber", "cable", "fixed_wireless"):
                base[town] += hh * scale // 100
            north_certificate = rule == "verified" and town == "North Ridge" and tech == "satellite"
            permit = not claims[town] if rule == "strict" else not served or north_certificate
            if permit:
                allowed[row["block_id"]] = town, {
                    t: appraise(row, t, line_cost, pass_shift, om_scale) for t in ("F", "W")
                }
        town_frontiers = {town: {0: 0} for town in homes}
        for town, plans in allowed.values():
            choices = {0: 0}
            for gain, *costs in plans.values():
                choices[gain] = min(choices.get(gain, budget + 1), sum(costs))
            town_frontiers[town] = merge(town_frontiers[town], choices, budget)
        county_frontier = {0: 0}
        required = {town: ceil(Fraction(count * floor, 100)) for town, count in homes.items()}
        for town, options in town_frontiers.items():
            adequate = {added: cost for added, cost in options.items() if base[town] + added >= required[town]}
            county_frontier = merge(county_frontier, adequate, budget)
        if county_frontier:
            gain, spending = (
                min(county_frontier.items(), key=lambda pair: (pair[1], -pair[0])) if min_cost
                else (max(county_frontier), county_frontier[max(county_frontier)])
            )
            optimum = ("optimal", gain, spending)
        else:
            optimum = ("infeasible", None, None)
        expected[case] = optimum, base, required, allowed
    return expected, homes, claims


def audit(path, expected, homes, claims):
    scenarios = read(path / "task2_scenarios.csv")
    projects = defaultdict(list)
    for row in read(path / "task2_projects.csv"):
        projects[row["scenario"]].append(row)
    town_rows = {(r["scenario"], r["township"]): r for r in read(path / "task2_townships.csv")}
    solver_rows = {r["scenario"]: r for r in json.loads((path / "task2_solver.json").read_text())["cases"]}
    assert len(scenarios) == len(expected)
    assert {row["scenario"] for row in scenarios} == set(expected)
    for row in scenarios:
        case = row["scenario"]
        rule, floor, line_cost, pass_shift, scale, min_cost = CASES[case]
        budget = BUDGET_LIMITS.get(case, BUDGET)
        assert row["rule"] == rule and float(row["floor_pct"]) == floor and int(row["budget_usd"]) == budget
        assert int(row["fiber_usd_per_mile"]) == line_cost and int(row["wireless_pass_shift_pp"]) == pass_shift
        assert float(row["om_scale"]) == MAINTENANCE_SCALES.get(case, 1)
        assert float(row["baseline_scale"]) == scale / 100
        assert row["objective"] == ("min_cost" if min_cost else "coverage")
        optimum, base, required, allowed = expected[case]
        assert optimum == (row["status"], int(row["new_hh"] or 0) if row["new_hh"] else None,
                           int(row["lifecycle_usd"] or 0) if row["lifecycle_usd"] else None), (case, optimum)
        assert len(allowed) == int(row["eligible_blocks"])
        selected, added, components, technologies = set(), Counter(), Counter(), Counter()
        for project in projects[case]:
            block = project["block"]
            assert block not in selected and block in allowed
            town, offers = allowed[block]
            technology = project["technology"]
            fields = ("hh", "backhaul", "last_mile", "o_and_m")
            quoted = tuple(int(project[field]) for field in fields)
            assert quoted == offers[technology] and project["township"] == town
            added[town] += quoted[0]
            components.update(dict(zip(fields[1:], quoted[1:])))
            technologies[technology] += 1
            selected.add(block)
        status, gain, cost = optimum
        if status == "optimal":
            assert sum(added.values()) == gain and sum(components.values()) == cost <= budget
            assert all(required[t] <= base[t] + added[t] <= homes[t] for t in homes)
            assert solver_rows[case]["cost_gap"] == 0
            assert solver_rows[case]["gap"] == (None if min_cost else 0)
            if solver_rows[case]["solver"] != "analytic":
                assert abs(solver_rows[case]["cost_bound"] - cost) < 1e-6
                if min_cost:
                    assert solver_rows[case]["gap_bound"] is None
                else:
                    assert abs(solver_rows[case]["gap_bound"] - gain) < 1e-6
        else:
            assert not selected
            assert solver_rows[case]["gap"] is None and solver_rows[case]["cost_gap"] is None
        for field, summary_field in zip(("backhaul", "last_mile", "o_and_m"),
                                         ("backhaul_usd", "last_mile_usd", "o_and_m_pv_usd")):
            assert components[field] == int(row[summary_field])
        assert technologies["F"] == int(row["fiber_blocks"]) and technologies["W"] == int(row["wireless_blocks"])
        for town in homes:
            observed = town_rows[case, town]
            modeled = {
                "households": homes[town], "served_blocks": claims[town], "baseline": base[town],
                "minimum": required[town], "new_hh": added[town], "post": base[town] + added[town],
                "deficit": max(0, required[town] - base[town] - added[town]),
            }
            assert all(int(observed[key]) == value for key, value in modeled.items())
            assert abs(float(observed["post_pct"]) - 100 * modeled["post"] / homes[town]) < 1e-12
        print(f"{case} compared: {len(selected)} distinct qualifying blocks, all cost and coverage fields match")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--results", type=Path, default=Path("results"))
    args = parser.parse_args()
    # Hand example: block A (0,0)/(3,4)/(5,8), block B (0,0)/(4,5), cap 9.
    # The best gain with both eligible is 7, and a separate hard floor of 4 in A leaves only (5,8).
    assert merge({0: 0, 3: 4, 5: 8}, {0: 0, 4: 5}, 9) == {7: 9, 5: 8, 4: 5, 3: 4, 0: 0}
    assert merge({5: 8}, {0: 0, 4: 5}, 9) == {5: 8}
    blocks = read(args.data / "blocks.csv")
    assert len(blocks) == len({row["block_id"] for row in blocks}) == 120
    expected, homes, claims = independent(blocks)
    print("Raw-reading strict served-block counts:", dict(claims))
    print("Independent dynamic-programming results before CSV comparison")
    for case, (optimum, *_) in expected.items():
        print(case, *optimum)
    audit(args.results, expected, homes, claims)
    print(f"Passed independent hand check, exact optimization and row audit of {len(expected)} cases.")


if __name__ == "__main__":
    main()
