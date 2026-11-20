"""Task 2 access planning and shared Task 3 optimization."""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from dataclasses import asdict, dataclass
from math import ceil, floor as round_down, isfinite
from pathlib import Path

import numpy as np
from scipy import __version__ as scipy_version
from scipy.optimize import Bounds, LinearConstraint, milp


BUDGET = 11_000_000
FLOOR = 0.25
YEARS = 10
DISCOUNT_RATE = 0.03
ANNUITY = sum((1 + DISCOUNT_RATE) ** -year for year in range(1, YEARS + 1))
FIBER_RATE = 42_240
WIRELESS_RATE = 5_500
PASS_PCT = (80, 75, 70, 62, 55)
O_AND_M = {"F": 0.018, "W": 0.035}
TERRESTRIAL = {"fiber", "fixed_wireless", "cable"}


@dataclass(frozen=True)
class Block:
    id: str
    town: str
    hh: int
    subscriptions: int
    served: int
    technology: str
    distance: float
    terrain: int


@dataclass(frozen=True)
class Action:
    block: str
    technology: str
    hh: int
    backhaul: int
    last_mile: int
    o_and_m: int
    hub: str | None = None
    provider: str = ""

    @property
    def cost(self):
        return self.backhaul + self.last_mile + self.o_and_m


@dataclass(frozen=True)
class Hub:
    town: str
    backhaul: int
    o_and_m: int

    @property
    def cost(self):
        return self.backhaul + self.o_and_m


def load_blocks(data_dir):
    path = Path(data_dir) / "blocks.csv"
    with path.open(encoding="utf-8-sig", newline="") as stream:
        blocks = {}
        for row in csv.DictReader(stream):
            block = Block(
                row["block_id"], row["township"], int(row["total_households"]),
                int(row["subscription_households"]), int(row["provider_served"]),
                row["provider_technology"], float(row["distance_to_fiber_backbone_miles"]),
                int(row["terrain_difficulty"]),
            )
            if (not block.id or block.id in blocks or not block.town
                    or not 0 <= block.subscriptions <= block.hh
                    or block.hh <= 0 or not isfinite(block.distance) or block.distance < 0
                    or not 1 <= block.terrain <= 5 or block.served not in (0, 1)
                    or block.technology not in TERRESTRIAL | {"none", "satellite"}
                    or block.served != int(block.technology != "none")):
                raise ValueError(f"Invalid block row {row}")
            blocks[block.id] = block
    if not blocks:
        raise ValueError(f"No blocks in {path}")
    return blocks


def eligible_blocks(blocks, rule):
    if rule == "strict":
        excluded_towns = {b.town for b in blocks.values() if b.served}
        return {b.id for b in blocks.values() if b.town not in excluded_towns}
    if rule == "block":
        return {b.id for b in blocks.values() if not b.served}
    if rule == "verified":
        return eligible_blocks(blocks, "block") | {
            b.id for b in blocks.values()
            if b.town == "North Ridge" and b.technology == "satellite"
        }
    raise ValueError(f"Unknown eligibility rule {rule}")


def om_pv(tech, backhaul, last_mile, scale=1.0):
    return round(ANNUITY * O_AND_M[tech] * scale * (backhaul + last_mile))


def make_actions(blocks, rule="block", fiber_rate=FIBER_RATE,
                 wireless_rate=WIRELESS_RATE, wireless_shift=0, om_scale=1.0):
    # shortcut: backbone distance proxies each block's route, replace with surveyed links when available.
    allowed = eligible_blocks(blocks, rule)
    actions = []
    for b in blocks.values():
        if b.id not in allowed:
            continue
        terrain_steps = b.terrain - 1
        fiber_hh = b.hh
        wireless_hh = b.hh * (PASS_PCT[terrain_steps] + wireless_shift) // 100
        for tech, households, backhaul, last_mile in (
            ("F", fiber_hh, fiber_rate * b.distance * (1 + 0.16 * terrain_steps),
             980 * fiber_hh * (1 + 0.10 * terrain_steps)),
            ("W", wireless_hh, wireless_rate * b.distance * (1 + 0.10 * terrain_steps),
             28_000 * (1 + 0.08 * terrain_steps) + 480 * wireless_hh),
        ):
            capex_b, capex_l = round(backhaul), round(last_mile)
            if households > 0:
                actions.append(Action(b.id, tech, households, capex_b, capex_l,
                                      om_pv(tech, capex_b, capex_l, om_scale)))
    return actions


def town_coverage(blocks, selected=(), floor=FLOOR, baseline_scale=1.0):
    totals = Counter()
    proxy = Counter()
    claims = Counter()
    added = Counter()
    for b in blocks.values():
        totals[b.town] += b.hh
        if b.technology in TERRESTRIAL and b.served:
            proxy[b.town] += round_down(b.hh * baseline_scale)
        claims[b.town] += b.served
    for action in selected:
        added[blocks[action.block].town] += action.hh
    coverage = {}
    for town, hh in totals.items():
        baseline, gain = proxy[town], added[town]
        required = ceil(floor * hh)
        coverage[town] = {
            "households": hh, "baseline": baseline, "minimum": required,
            "new_hh": gain, "post": baseline + gain, "post_pct": 100 * (baseline + gain) / hh,
            "deficit": max(0, required - baseline - gain), "served_blocks": claims[town],
        }
    return coverage


def solve(blocks, actions, budget=BUDGET, floor=FLOOR, hubs=(), min_hubs=0,
          baseline_scale=1.0, objective="coverage"):
    """Optimize lexicographically by coverage and resource cost, or minimize cost."""
    actions, hubs = tuple(actions), tuple(hubs)
    base = town_coverage(blocks, floor=floor, baseline_scale=baseline_scale)
    count = len(actions)
    size = count + len(hubs)
    result = {"status": "infeasible", "selected": (), "hubs": (), "coverage": base,
              "cost": None, "new_hh": None, "gap": None, "cost_gap": None,
              "gap_bound": None, "cost_bound": None, "solver": "analytic"}
    if not size:
        if not min_hubs and all(row["deficit"] == 0 for row in base.values()):
            result.update(status="optimal", cost=0, new_hh=0, gap=0.0, cost_gap=0.0)
        return result

    costs = np.array([a.cost for a in actions] + [h.cost for h in hubs], dtype=float)
    gains = np.array([a.hh for a in actions] + [0] * len(hubs), dtype=float)
    rows, lower, upper = [costs], [0], [budget]

    def add_row(entries, lb, ub):
        row = np.zeros(size)
        for index, value in entries:
            row[index] = value
        rows.append(row)
        lower.append(lb)
        upper.append(ub)

    for block in dict.fromkeys(a.block for a in actions):
        add_row(((i, 1) for i, a in enumerate(actions) if a.block == block), 0, 1)
    for town, values in base.items():
        add_row(((i, a.hh) for i, a in enumerate(actions) if blocks[a.block].town == town),
                values["deficit"], np.inf)
    for j, hub in enumerate(hubs, start=count):
        dependent = [i for i, a in enumerate(actions) if a.hub == hub.town]
        for i in dependent:
            add_row([(i, 1), (j, -1)], -np.inf, 0)
        add_row([(i, 1) for i in dependent] + [(j, -2)], 0, np.inf)
    if min_hubs:
        add_row(((i, 1) for i in range(count, size)), min_hubs, np.inf)

    def run(c):
        return milp(c, integrality=np.ones(size), bounds=Bounds(0, 1),
                    constraints=LinearConstraint(np.array(rows), lower, upper),
                    options={"mip_rel_gap": 0.0, "time_limit": 60.0})

    result["solver"] = f"SciPy {scipy_version} milp/HiGHS"
    if objective == "coverage":
        primary = run(-gains)
        if primary.status == 2:
            return result
        if primary.x is None or primary.status not in (0, 1):
            raise RuntimeError(primary.message)
        result["gap"] = primary.mip_gap
        result["gap_bound"] = -primary.mip_dual_bound
        total = int(round(gains @ primary.x))
        add_row(((i, a.hh) for i, a in enumerate(actions)), total, total)
    elif objective != "min_cost":
        raise ValueError(f"Unknown objective {objective}")

    secondary = run(costs)
    if secondary.status == 2 and objective == "min_cost":
        return result
    if secondary.x is None or secondary.status not in (0, 1):
        raise RuntimeError(secondary.message)
    chosen = tuple(a for a, x in zip(actions, secondary.x[:count]) if x > 0.5)
    built = tuple(h for h, x in zip(hubs, secondary.x[count:]) if x > 0.5)
    coverage = town_coverage(blocks, chosen, floor, baseline_scale)
    cost = sum(a.cost for a in chosen) + sum(h.cost for h in built)
    total_hh = sum(a.hh for a in chosen)
    optimal = secondary.status == 0 and (objective != "coverage" or primary.status == 0)
    assert all(abs(x - round(x)) < 1e-6 for x in secondary.x)
    assert cost == round(secondary.fun) and cost <= budget
    assert len({a.block for a in chosen}) == len(chosen)
    assert all(0 < a.hh <= blocks[a.block].hh for a in chosen)
    assert not any(row["deficit"] or row["post"] > row["households"] for row in coverage.values())
    assert len(built) >= min_hubs
    assert set(a.hub for a in chosen if a.hub) == {h.town for h in built}
    assert all(sum(a.hub == h.town for a in chosen) >= 2 for h in built)
    if objective == "coverage":
        assert total_hh == total
    result.update(status="optimal" if optimal else "limit-feasible",
                  selected=chosen, hubs=built, coverage=coverage, cost=cost,
                  new_hh=total_hh, cost_gap=secondary.mip_gap,
                  cost_bound=secondary.mip_dual_bound)
    return result


def self_check():
    blocks = {"test": Block("test", "Test", 100, 30, 0, "none", 1.0, 1)}
    options = [Action("test", "F", 100, 30, 50, 10), Action("test", "W", 50, 10, 20, 10),
               Action("test", "W", 50, 9, 19, 10)]
    feasible = solve(blocks, options, budget=45, floor=0.50)
    assert (feasible["status"], feasible["new_hh"], feasible["cost"]) == ("optimal", 50, 38)
    assert solve(blocks, options, budget=45, floor=0.51)["status"] == "infeasible"
    assert solve(blocks, options, budget=100, floor=0.50)["new_hh"] == 100


def write_csv(path, rows):
    if rows:
        with path.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, required=True, help="Directory containing blocks.csv")
    parser.add_argument("--out", type=Path, default=Path("results"))
    args = parser.parse_args()
    self_check()
    blocks = load_blocks(args.data)
    cases = (
        ("strict", "strict", FLOOR, BUDGET, {}, {}, "coverage"),
        ("strict_without_floor", "strict", 0, BUDGET, {}, {}, "coverage"),
        ("block_50pct", "block", 0.50, BUDGET, {}, {}, "coverage"),
        ("block_base", "block", FLOOR, BUDGET, {}, {}, "coverage"),
        ("block_min_budget", "block", FLOOR, BUDGET, {}, {}, "min_cost"),
        ("verified_50pct", "verified", 0.50, BUDGET, {}, {}, "coverage"),
        ("verified_50pct_min_budget", "verified", 0.50, BUDGET, {}, {}, "min_cost"),
        ("verified_base", "verified", FLOOR, BUDGET, {}, {}, "coverage"),
        ("fiber_aerial_q1", "block", FLOOR, BUDGET, {"fiber_rate": 25_872}, {}, "coverage"),
        ("fiber_underground_median", "block", FLOOR, BUDGET, {"fiber_rate": 95_040}, {}, "coverage"),
        ("wireless_pass_minus10pp", "block", FLOOR, BUDGET, {"wireless_shift": -10}, {}, "coverage"),
        ("wireless_pass_plus10pp", "block", FLOOR, BUDGET, {"wireless_shift": 10}, {}, "coverage"),
        ("block_budget_8m", "block", FLOOR, 8_000_000, {}, {}, "coverage"),
        ("block_budget_14m", "block", FLOOR, 14_000_000, {}, {}, "coverage"),
        ("block_om_75pct", "block", FLOOR, BUDGET, {"om_scale": 0.75}, {}, "coverage"),
        ("block_om_125pct", "block", FLOOR, BUDGET, {"om_scale": 1.25}, {}, "coverage"),
        ("block_baseline_75pct", "block", FLOOR, BUDGET, {}, {"baseline_scale": 0.75}, "coverage"),
    )
    args.out.mkdir(parents=True, exist_ok=True)
    scenarios, town_rows, project_rows, evidence = [], [], [], []
    base_pairs = None
    for name, rule, floor, budget, menu_options, solver_options, objective in cases:
        options = make_actions(blocks, rule, **menu_options)
        outcome = solve(blocks, options, budget, floor, objective=objective, **solver_options)
        assert {a.block for a in outcome["selected"]} <= eligible_blocks(blocks, rule)
        if name == "strict":
            assert not eligible_blocks(blocks, rule) and outcome["status"] == "infeasible"
        projects = outcome["selected"]
        values = outcome["coverage"]
        pairs = {(a.block, a.technology) for a in projects}
        if name == "block_base":
            base_pairs = pairs
        summary = {
            "scenario": name, "rule": rule, "floor_pct": 100 * floor, "budget_usd": budget,
            "fiber_usd_per_mile": menu_options.get("fiber_rate", FIBER_RATE),
            "wireless_pass_shift_pp": menu_options.get("wireless_shift", 0),
            "om_scale": menu_options.get("om_scale", 1.0),
            "baseline_scale": solver_options.get("baseline_scale", 1.0),
            "objective": objective, "status": outcome["status"],
            "eligible_blocks": len(eligible_blocks(blocks, rule)),
            "new_hh": outcome["new_hh"], "lifecycle_usd": outcome["cost"],
            "backhaul_usd": sum(a.backhaul for a in projects),
            "last_mile_usd": sum(a.last_mile for a in projects),
            "o_and_m_pv_usd": sum(a.o_and_m for a in projects),
            "fiber_blocks": sum(a.technology == "F" for a in projects),
            "wireless_blocks": sum(a.technology == "W" for a in projects),
            "min_town_pct": min(row["post_pct"] for row in values.values()),
            "project_technology_pairs_added_vs_base": len(pairs - base_pairs) if base_pairs is not None and projects else None,
            "project_technology_pairs_removed_vs_base": len(base_pairs - pairs) if base_pairs is not None and projects else None,
        }
        scenarios.append(summary)
        town_rows.extend({"scenario": name, "township": town, **row} for town, row in values.items())
        project_rows.extend({"scenario": name, "township": blocks[a.block].town, **asdict(a)}
                            for a in projects)
        evidence.append({**summary, **{key: outcome[key] for key in (
            "solver", "gap", "cost_gap", "gap_bound", "cost_bound",
        )}})
        print(f"{name}: {outcome['status']}; added={outcome['new_hh']}; cost={outcome['cost']}", flush=True)
    write_csv(args.out / "task2_scenarios.csv", scenarios)
    write_csv(args.out / "task2_townships.csv", town_rows)
    write_csv(args.out / "task2_projects.csv", project_rows)
    (args.out / "task2_solver.json").write_text(json.dumps({
        "self_check": "Passed three hand-solvable assertions",
        "solver_options": {"mip_rel_gap": 0.0, "time_limit_per_stage_seconds": 60.0},
        "annuity": ANNUITY, "cases": evidence,
    }, indent=2, allow_nan=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
