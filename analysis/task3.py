"""Run the three procurement mechanisms using Task 2's common planning model."""

import argparse
import csv
from collections import Counter, defaultdict
from dataclasses import asdict, replace
from math import ceil
from pathlib import Path
from statistics import median

from task2 import ANNUITY, BUDGET, FIBER_RATE, FLOOR, Hub, load_blocks, make_actions, om_pv, solve


COOP = "regional cooperative"
CABLE = "national cable operator"
STARTUP = "fixed wireless entrant"
MECHANISMS = ("cooperative", "competitive", "county PPP")
LEASE_PER_YEAR = 4800
WIRELESS_SHIFTS = {"wireless-minus10pp": -10, "wireless-plus10pp": 10}
LATERAL_OFFSETS = {f"lateral-plus-{miles}mi": miles for miles in (1, 2, 3)}


def repriced(action, provider, backhaul_factor=1, last_mile_factor=1, hub=None):
    backhaul = round(action.backhaul * backhaul_factor)
    last_mile = round(action.last_mile * last_mile_factor)
    return replace(
        action, provider=provider, hub=hub, backhaul=backhaul, last_mile=last_mile,
        o_and_m=om_pv(action.technology, backhaul, last_mile),
    )


def portfolio_menu(blocks, actions, mechanism, footprint_shift=0, hub_multiplier=1, lateral_offset=0):
    if mechanism == "cooperative":
        return [replace(a, provider=COOP) for a in actions], []
    technologies = defaultdict(set)
    unserved = defaultdict(list)
    for block in blocks.values():
        if block.served:
            technologies[block.town].add(block.technology)
        else:
            unserved[block.town].append(block)
    hub_data = {
        town: (median(b.distance for b in rows), median(b.terrain for b in rows))
        for town, rows in unserved.items()
    }
    offers = []
    ppp = mechanism == "county PPP"
    for action in actions:
        block = blocks[action.block]
        town = block.town
        distance = block.distance
        if distance <= 13 + footprint_shift:
            offers.append(replace(action, provider=COOP))
        if action.technology == "F" and "cable" in technologies[town] and distance <= 6 + footprint_shift:
            offers.append(repriced(action, CABLE, 0.70, 0.90))
        if action.technology == "W" and "fixed_wireless" in technologies[town] and distance <= 9 + footprint_shift:
            offers.append(repriced(action, STARTUP, 0.75, 0.95))

        if ppp:
            anchor_distance, _ = hub_data[town]
            # shortcut: radial distance proxy only; replace with engineered routes and capacity before procurement.
            lateral_miles = abs(distance - anchor_distance) + 0.5 + lateral_offset
            if lateral_miles <= 6:
                lateral_factor = lateral_miles / distance
                offers.append(repriced(action, COOP, lateral_factor, hub=town))
                if action.technology == "F" and lateral_miles <= 4:
                    offers.append(repriced(action, CABLE, lateral_factor, 0.90, town))
                if action.technology == "W" and lateral_miles <= 5:
                    offers.append(repriced(action, STARTUP, lateral_factor, 0.95, town))

    # Same block, technology, and hub gives equal coverage, so only the lowest conforming offer is needed.
    lowest = {}
    for action in offers:
        key = action.block, action.technology, action.hub
        old = lowest.get(key)
        if old is None or (action.cost, action.provider) < (old.cost, old.provider):
            lowest[key] = action

    clients = defaultdict(set)
    for action in lowest.values():
        if action.hub:
            clients[action.hub].add(action.block)
    hubs = []
    for town, client_blocks in clients.items():
        if len(client_blocks) >= 2:
            distance, terrain = hub_data[town]
            capex = round(hub_multiplier * (25000 + FIBER_RATE * distance * (1 + 0.16 * (terrain - 1))))
            hubs.append(Hub(town, capex, om_pv("F", capex, 0)))
    active_hubs = {hub.town for hub in hubs}
    return [a for a in lowest.values() if not a.hub or a.hub in active_hubs], hubs


def summarize(blocks, menu, result, scenario, rule, mechanism, equity, budget):
    picked, hubs = result["selected"], result["hubs"]
    feasible = result["status"] in ("optimal", "limit-feasible")
    service = Counter()
    base, hh = Counter(), Counter()
    provider_actions = defaultdict(list)
    block_rows = []
    for block in blocks.values():
        hh[block.town] += block.hh
        if block.served and block.technology in ("fiber", "cable", "fixed_wireless"):
            base[block.town] += block.hh
    for action in picked:
        town = blocks[action.block].town
        service[town] += action.hh
        provider_actions[action.provider].append(action)
        block_rows.append(dict(scenario=scenario, rule=rule, mechanism=mechanism, town=town, **asdict(action)))
    best_by_block = Counter()
    for action in menu:
        best_by_block[action.block] = max(best_by_block[action.block], action.hh)
    ceiling = Counter()
    for block, gain in best_by_block.items():
        ceiling[blocks[block].town] += gain
    totals = Counter(a.technology for a in picked)
    county_backhaul = sum(h.backhaul for h in hubs)
    county_om = sum(h.o_and_m for h in hubs)
    private_backhaul = sum(a.backhaul for a in picked)
    private_om = sum(a.o_and_m for a in picked)
    last_mile = sum(a.last_mile for a in picked)
    provider_rows = []
    for provider, actions in sorted(provider_actions.items()):
        leases = {a.hub for a in actions if a.hub}
        rent_pv = len(leases) * round(LEASE_PER_YEAR * ANNUITY)
        provider_rows.append(dict(
            scenario=scenario, rule=rule, mechanism=mechanism, provider=provider,
            new_hh=sum(a.hh for a in actions),
            network_cost=sum(a.cost for a in actions),
            leases=len(leases), annual_lease_payment=len(leases) * LEASE_PER_YEAR,
            lease_paid_pv=rent_pv,
        ))
    lease = sum(row["lease_paid_pv"] for row in provider_rows)
    gross = county_backhaul + county_om + private_backhaul + private_om + last_mile
    new_hh = sum(service.values())
    town_rows = [
        dict(scenario=scenario, rule=rule, mechanism=mechanism, town=town, total_hh=n,
             baseline_hh=base[town], new_hh=service[town] if feasible else None,
             post_hh=base[town] + service[town] if feasible else None,
             new_share=service[town] / n if feasible else None,
             post_rate=(base[town] + service[town]) / n if feasible else None,
             footprint_upper_hh=base[town] + ceiling[town],
             equity_deficit_hh=max(0, ceil(equity*n) - base[town] - service[town]))
        for town, n in sorted(hh.items())
    ]
    hub_rows = [
        dict(scenario=scenario, rule=rule, mechanism=mechanism, town=hub.town,
             capex=hub.backhaul, o_and_m_pv=hub.o_and_m,
             tenant_blocks=sum(a.hub == hub.town for a in picked),
             tenants=len({a.provider for a in picked if a.hub == hub.town}))
        for hub in hubs
    ]
    if feasible:
        assert gross == result["cost"] <= budget and new_hh == result["new_hh"]
        assert len({a.block for a in picked}) == len(picked)
        assert all(r["equity_deficit_hh"] == 0 for r in town_rows)
        assert all(r["tenant_blocks"] >= 2 for r in hub_rows)
        assert all(a.hub is None or a.hub in {h.town for h in hubs} for a in picked)
        assert rule != "strict" or all(not b.served for b in blocks.values() if b.town in service)
    else:
        assert not picked and not hubs
    min_access = min(row["post_rate"] for row in town_rows) if feasible else None
    summary = dict(
        scenario=scenario, rule=rule, mechanism=mechanism, equity_floor=equity, budget_usd=budget,
        status=result["status"], new_hh=new_hh if feasible else None,
        gross_cost=gross if feasible else None, cost_per_new_hh=gross/new_hh if new_hh else None,
        backhaul_capex=county_backhaul + private_backhaul if feasible else None,
        last_mile_capex=last_mile if feasible else None,
        o_and_m_pv=county_om + private_om if feasible else None,
        county_backhaul_capex=county_backhaul if feasible else None,
        county_o_and_m_pv=county_om if feasible else None,
        lease_received_pv=lease if feasible else None, lease_paid_pv=lease if feasible else None,
        net_county_outlay=gross - lease if feasible else None,
        open_hubs=len(hubs) if feasible else None,
        fiber_blocks=totals["F"] if feasible else None, wireless_blocks=totals["W"] if feasible else None,
        min_access_rate=min_access, gap=result["gap"], cost_gap=result["cost_gap"], solver=result["solver"],
    )
    return summary, town_rows, provider_rows, block_rows, hub_rows


def export(path, rows):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def southern_indicators(blocks):
    south = [b for b in blocks.values() if b.town == "South Hollow"]
    groups = {
        "all South Hollow blocks": south,
        "fixed-wireless claim": [b for b in south if b.technology == "fixed_wireless"],
        "other South Hollow blocks": [b for b in south if b.technology != "fixed_wireless"],
    }
    rows = []
    for group, homes in groups.items():
        total = sum(block.hh for block in homes)
        subscribers = sum(block.subscriptions for block in homes)
        if total:
            rows.append(dict(group=group, blocks=len(homes), total_hh=total,
                             any_subscription_hh=subscribers, any_subscription_rate=subscribers / total))
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", required=True, type=Path)
    parser.add_argument("--out", default=Path("results"), type=Path)
    args = parser.parse_args()
    blocks = load_blocks(args.data_dir)
    tables = {name: [] for name in ("summary", "towns", "providers", "actions", "hubs", "finance")}
    experiments = [
        (rule, rule, mechanism, FLOOR, BUDGET, 0, 1, 1)
        for rule in ("strict", "block", "verified") for mechanism in MECHANISMS
    ]
    experiments.extend([
        ("narrow-footprints", "block", "competitive", FLOOR, BUDGET, -2, 1, 1),
        ("wide-footprints", "block", "competitive", FLOOR, BUDGET, 2, 1, 1),
        ("low-hub-cost", "block", "county PPP", FLOOR, BUDGET, 0, .75, 1),
        ("high-hub-cost", "block", "county PPP", FLOOR, BUDGET, 0, 2, 1),
    ])
    # Rerun each comparison under identical eligibility and costs; any recommended mechanism has a matching row.
    experiments.extend(("no-equity", "block", m, 0, BUDGET, 0, 1, 1) for m in MECHANISMS)
    experiments.extend((case, "block", "county PPP", FLOOR, BUDGET, 0, 1, 1) for case in LATERAL_OFFSETS)
    for mechanism in MECHANISMS:
        experiments.extend((case, "block", mechanism, FLOOR, BUDGET, 0, 1, 1) for case in WIRELESS_SHIFTS)
        experiments.extend([
            ("budget-9m", "block", mechanism, FLOOR, 9_000_000, 0, 1, 1),
            ("budget-13m", "block", mechanism, FLOOR, 13_000_000, 0, 1, 1),
            ("low-maintenance", "block", mechanism, FLOOR, BUDGET, 0, 1, .75),
            ("high-maintenance", "block", mechanism, FLOOR, BUDGET, 0, 1, 1.5),
            ("verified-50pct", "verified", mechanism, .50, BUDGET, 0, 1, 1),
        ])
    for scenario, rule, mechanism, equity, budget, footprint_shift, hub_multiplier, om_scale in experiments:
        menu = make_actions(blocks, rule, wireless_shift=WIRELESS_SHIFTS.get(scenario, 0))
        actions, hubs = portfolio_menu(blocks, menu, mechanism, footprint_shift, hub_multiplier,
                                       LATERAL_OFFSETS.get(scenario, 0))
        if om_scale != 1:
            actions = [replace(a, o_and_m=round(a.o_and_m * om_scale)) for a in actions]
            hubs = [replace(h, o_and_m=round(h.o_and_m * om_scale)) for h in hubs]
        min_hubs = int(mechanism == "county PPP" and rule != "strict")
        result = solve(blocks, actions, budget=budget, floor=equity, hubs=hubs, min_hubs=min_hubs)
        summary, towns, providers, picked, commissioned = summarize(
            blocks, actions, result, scenario, rule, mechanism, equity, budget,
        )
        for name, rows in zip(tables, ([summary], towns, providers, picked, commissioned)):
            tables[name].extend(rows)
        if mechanism == "county PPP" and scenario in ("block", "verified") and commissioned:
            leases = sum(provider["leases"] for provider in providers)
            county_om = summary["county_o_and_m_pv"]
            for annual_rate in (0, 2400, LEASE_PER_YEAR, 7200):
                revenue = leases * round(ANNUITY * annual_rate)
                tables["finance"].append(dict(
                    scenario=scenario, leases=leases, fee_per_lease_year=annual_rate, lease_pv=revenue,
                    county_o_and_m_pv=county_om, county_om_funding_gap_pv=county_om - revenue,
                    om_break_even_fee_per_lease_year=county_om / (ANNUITY * leases),
                    net_county_outlay=summary["gross_cost"] - revenue,
                ))
        print(scenario, mechanism, summary["status"], summary["new_hh"], summary["gross_cost"], flush=True)
    args.out.mkdir(parents=True, exist_ok=True)
    for name, rows in tables.items():
        if rows:
            export(args.out / f"task3_{name}.csv", rows)
    rows = southern_indicators(blocks)
    if rows:
        export(args.out / "task3_southern_indicators.csv", rows)


if __name__ == "__main__":
    main()
