"""Audit the supplied CSVs and reproduce the Task 1 tables."""

import argparse
import csv
import hashlib
import json
from collections import Counter
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path


def table(path, primary_key):
    with path.open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    keys = {row[primary_key] for row in rows}
    if len(rows) != len(keys) or "" in keys:
        raise ValueError(f"{path.name}: duplicate or empty {primary_key}")
    return rows, keys


def households(rows):
    return sum(int(row["total_households"]) for row in rows)


def subscriptions(rows):
    return sum(int(row["subscription_households"]) for row in rows)


def write(path, rows):
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, rows[0])
        writer.writeheader()
        writer.writerows(rows)


def run(data, out):
    blocks, block_ids = table(data / "blocks.csv", "block_id")
    roads, _ = table(data / "road_segments.csv", "road_segment_id")
    road_counts = Counter(row["block_id"] for row in roads)
    if road_counts.keys() != block_ids:
        raise ValueError("Road-to-block join has orphan roads or unmeasured blocks.")
    if any(not (0 <= int(row["subscription_households"])
                <= int(row["total_households"]) and int(row["total_households"]) > 0
                and 0 <= float(row["senior_share"]) <= 1
                and int(row["median_income"]) > 0
                and float(row["distance_to_fiber_backbone_miles"]) > 0
                and 1 <= int(row["terrain_difficulty"]) <= 5
                and (row["provider_served"], row["provider_technology"]) in {
                    ("0", "none"), ("1", "satellite"), ("1", "cable"),
                    ("1", "fiber"), ("1", "fixed_wireless")
                }) for row in blocks):
        raise ValueError("Invalid block range or inconsistent served/technology field.")
    if any(not (float(row["road_length_miles"]) > 0
                and float(row["signal_strength_dbm"]) < 0
                and row["road_type"] in {"paved", "unpaved"}) for row in roads):
        raise ValueError("Invalid road measurement.")

    hashes = {}
    versions_equal = {}
    for stem in ("blocks", "road_segments"):
        original, v2 = f"{stem}.csv", f"{stem}V2.csv"
        raw, alternate = (data / original).read_bytes(), (data / v2).read_bytes()
        hashes[original] = hashlib.sha256(raw).hexdigest()
        hashes[v2] = hashlib.sha256(alternate).hexdigest()
        versions_equal[stem] = raw == alternate
    if not all(versions_equal.values()):
        raise ValueError("At least one original/V2 file pair differs. Review the sources.")

    townships = []
    for name in sorted({row["township"] for row in blocks}):
        group = [row for row in blocks if row["township"] == name]
        served = [row for row in group if row["provider_served"] == "1"]
        terrestrial = [row for row in served if row["provider_technology"] != "satellite"]
        total, subs = households(group), subscriptions(group)
        townships.append({
            "township": name, "blocks": len(group), "households": total,
            "subscriptions": subs, "subscription_rate": round(subs / total, 8),
            "reported_served_blocks": len(served),
            "reported_served_block_households": households(served),
            "terrestrial_coded_blocks": len(terrestrial),
            "terrestrial_coded_block_households": households(terrestrial),
            "satellite_coded_block_households": households(served) - households(terrestrial),
            "map_unserved_block_households": total - households(served),
            "strictly_eligible": int(not served),
        })

    north = [row for row in blocks if row["township"] == "North Ridge"]
    diagnostics = []
    for tech in sorted({row["provider_technology"] for row in north}):
        group = [row for row in north if row["provider_technology"] == tech]
        ids = {row["block_id"] for row in group}
        segments = [row for row in roads if row["block_id"] in ids]
        diagnostics.append({
            "provider_technology": tech, "blocks": len(group),
            "households": households(group), "subscriptions": subscriptions(group),
            "subscription_rate": round(subscriptions(group) / households(group), 8),
            "surveyed_segments": len(segments),
            "surveyed_road_miles": round(sum(float(row["road_length_miles"]) for row in segments), 2),
            **{f"miles_at_or_below_{threshold}_dbm": round(sum(
                float(row["road_length_miles"]) for row in segments
                if float(row["signal_strength_dbm"]) <= threshold), 2)
               for threshold in (-105, -110, -115)},
        })

    satellite_count = sum(row["households"] for row in diagnostics
                          if row["provider_technology"] == "satellite")
    north_reported = households(row for row in north if row["provider_served"] == "1")
    labor_hours = 128 + 32 + 24
    cost = Decimal(labor_hours) * Decimal("65.68") + 500
    scenarios = []
    for policy, fraction, prep, fast, dispute in (
        ("accept", "0", 0, 0, 0), ("challenge_none_upheld", "0", 30, 120, 270),
        ("challenge_quarter_upheld", "0.25", 30, 120, 270),
        ("challenge_half_upheld", "0.50", 30, 120, 270),
        ("challenge_all_upheld", "1", 30, 120, 270),
    ):
        converted = int((satellite_count * Decimal(fraction)).quantize(
            Decimal("1"), rounding=ROUND_HALF_UP))
        admin_cost = cost if prep else Decimal(0)
        remaining_terrestrial = sum(row["provider_technology"] in
                                    {"cable", "fiber", "fixed_wireless"} for row in north)
        scenarios.append({
            "scenario": policy, "share_substantiated": fraction,
            "households_reclassified": converted,
            "households_retaining_original_north_served_treatment": north_reported - converted,
            "unchallenged_terrestrial_coded_blocks": remaining_terrestrial,
            "north_strictly_eligible": int(not remaining_terrestrial and converted == north_reported),
            "admin_cost_usd": f"{admin_cost:.2f}",
            "admin_cost_low_usd": f"{admin_cost / 2:.2f}",
            "admin_cost_high_usd": f"{admin_cost * 2:.2f}",
            "illustrative_prep_days": prep,
            "conceded_scenario_max_days_from_prep_start": fast,
            "contested_scenario_max_days_from_prep_start": dispute,
        })

    audit = {
        "sha256": hashes, "original_equals_v2_bytewise": versions_equal,
        "rows": {"blocks": len(blocks), "road_segments": len(roads)},
        "primary_keys_unique_nonempty": {"block_id": True, "road_segment_id": True},
        "orphan_road_segments": 0, "blocks_without_road_measurements": 0,
        "road_segments_per_block": dict(sorted(Counter(road_counts.values()).items())),
        "households_counted_once_in_block_table": households(blocks),
        "subscriptions_counted_once_in_block_table": subscriptions(blocks),
        "subscriptions_in_map_unserved_blocks": subscriptions(
            row for row in blocks if row["provider_served"] == "0"),
        "observed_ranges": {
            key: [min(float(row[key]) for row in rows), max(float(row[key]) for row in rows)]
            for rows, keys in (
                (blocks, ["total_households", "subscription_households", "median_income",
                          "senior_share", "provider_served", "distance_to_fiber_backbone_miles",
                          "terrain_difficulty"]),
                (roads, ["signal_strength_dbm", "road_length_miles"]),
            )
            for key in keys
        },
        "observed_categories": {
            key: sorted({row[key] for row in rows})
            for rows, key in ((blocks, "provider_technology"), (roads, "road_type"))
        },
    }
    assert sum(row["households"] for row in townships) == households(blocks)
    assert sum(row["surveyed_segments"] for row in diagnostics) == sum(
        road_counts[row["block_id"]] for row in north)
    assert scenarios[-1]["households_reclassified"] == satellite_count

    county_groups = {
        "satellite": [row for row in blocks if row["provider_served"] == "1"
                      and row["provider_technology"] == "satellite"],
        "terrestrial": [row for row in blocks if row["provider_served"] == "1"
                        and row["provider_technology"] != "satellite"],
        "unserved": [row for row in blocks if row["provider_served"] == "0"],
    }
    audit["county_claim_decomposition"] = {
        name: {"blocks": len(group), "households": households(group)}
        for name, group in county_groups.items()
    }

    out.mkdir(parents=True, exist_ok=True)
    write(out / "task1_blocks.csv", [{
        "block_id": row["block_id"],
        "township": row["township"],
        "households": int(row["total_households"]),
        "subscriptions": int(row["subscription_households"]),
        "provider_served": int(row["provider_served"]),
        "provider_technology": row["provider_technology"],
        "median_income": int(row["median_income"]),
        "senior_share": float(row["senior_share"]),
        "distance_miles": float(row["distance_to_fiber_backbone_miles"]),
        "terrain": int(row["terrain_difficulty"]),
    } for row in blocks])
    write(out / "task1_townships.csv", townships)
    write(out / "task1_north_diagnostics.csv", diagnostics)
    write(out / "task1_challenge.csv", scenarios)
    (out / "task1_data_audit.json").write_text(json.dumps(audit, indent=2) + "\n", encoding="utf-8")
    print(f"{len(blocks)} unique blocks, {len(roads)} unique roads, "
          f"{len(townships)} townships. Both V2 files match byte for byte.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    run(args.data, args.out)
