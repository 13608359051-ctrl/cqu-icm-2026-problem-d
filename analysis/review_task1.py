"""Independently recompute Task 1 from the original data, then compare outputs."""
import argparse
import csv
import hashlib
import json
import sqlite3
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path


def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as source:
        return list(csv.DictReader(source))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--results", type=Path, default=Path("results"))
    args = parser.parse_args()
    db = sqlite3.connect(":memory:")
    db.row_factory = sqlite3.Row
    hashes = {}
    ranges = {}
    raw_inputs = {}
    for table, fields, numeric_fields in (
        ("blocks", "block_id,township,total_households,subscription_households,provider_served,provider_technology",
         ("total_households", "subscription_households", "median_income", "senior_share", "provider_served",
          "distance_to_fiber_backbone_miles", "terrain_difficulty")),
        ("road_segments", "road_segment_id,block_id,signal_strength_dbm,road_length_miles",
         ("signal_strength_dbm", "road_length_miles")),
    ):
        inputs = [(args.data / f"{table}{suffix}.csv") for suffix in ("", "V2")]
        assert inputs[0].read_bytes() == inputs[1].read_bytes()
        hashes.update({path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in inputs})
        records = read_csv(inputs[0])
        raw_inputs[table] = records
        columns = fields.split(",")
        ranges.update({name: [min(vals), max(vals)] for name in numeric_fields
                       for vals in [[float(row[name]) for row in records]]})
        db.execute(f"CREATE TABLE {table} ({','.join(name + (' REAL' if name in numeric_fields else ' TEXT') for name in columns)})")
        db.executemany(f"INSERT INTO {table} VALUES ({','.join('?' for _ in columns)})",
                       ([row[name] for name in columns] for row in records))
    unique_blocks = db.execute("SELECT COUNT(*),COUNT(DISTINCT block_id) FROM blocks").fetchone()
    unique_roads = db.execute("SELECT COUNT(*),COUNT(DISTINCT road_segment_id) FROM road_segments").fetchone()
    assert tuple(unique_blocks) == (120, 120) and tuple(unique_roads) == (248, 248)
    assert all(row["block_id"].strip() for row in raw_inputs["blocks"])
    assert all(row["road_segment_id"].strip() for row in raw_inputs["road_segments"])
    assert all(int(b["subscription_households"]) <= int(b["total_households"]) for b in raw_inputs["blocks"])
    missing = db.execute("SELECT COUNT(*) FROM road_segments WHERE block_id NOT IN (SELECT block_id FROM blocks)").fetchone()[0]
    multiplicity = dict(db.execute("SELECT segments, COUNT(*) FROM (SELECT block_id,COUNT(*) AS segments FROM road_segments GROUP BY block_id) GROUP BY segments"))
    assert missing == 0 and sum(multiplicity.values()) == 120
    towns = {r["township"]: dict(r) for r in db.execute("""
        SELECT township, COUNT(*) AS blocks, SUM(total_households) AS households,
               SUM(subscription_households) AS subscriptions,
               SUM(subscription_households) / SUM(total_households) AS subscription_rate,
               SUM(provider_served) AS reported_served_blocks,
               SUM(total_households*provider_served) AS reported_served_block_households,
               SUM(provider_technology IN ('cable','fiber','fixed_wireless')) AS terrestrial_coded_blocks,
               SUM(total_households*(provider_technology IN ('cable','fiber','fixed_wireless'))) AS terrestrial_coded_block_households,
               SUM(total_households*(provider_technology='satellite')) AS satellite_coded_block_households,
               SUM(total_households*(provider_served=0)) AS map_unserved_block_households,
               MAX(provider_served)=0 AS strictly_eligible
        FROM blocks GROUP BY township
    """)}
    diagnostics = {r[0]: dict(r) for r in db.execute("""
        WITH net AS (
            SELECT provider_technology, COUNT(*) AS blocks, SUM(total_households) AS households,
                   SUM(subscription_households) AS subscriptions,
                   SUM(subscription_households) / SUM(total_households) AS subscription_rate
            FROM blocks WHERE township='North Ridge' GROUP BY provider_technology
        ), surveyed AS (
            SELECT provider_technology, COUNT(*) AS surveyed_segments,
                   SUM(road_length_miles) AS surveyed_road_miles,
                   SUM(road_length_miles*(signal_strength_dbm<=-105)) AS 'miles_at_or_below_-105_dbm',
                   SUM(road_length_miles*(signal_strength_dbm<=-110)) AS 'miles_at_or_below_-110_dbm',
                   SUM(road_length_miles*(signal_strength_dbm<=-115)) AS 'miles_at_or_below_-115_dbm'
            FROM road_segments JOIN blocks USING (block_id) WHERE township='North Ridge'
            GROUP BY provider_technology
        )
        SELECT * FROM net JOIN surveyed USING (provider_technology)
    """)}
    county_totals = tuple(db.execute("SELECT SUM(total_households), SUM(subscription_households), SUM(subscription_households*(provider_served=0)) FROM blocks").fetchone())
    north = towns["North Ridge"]
    administered = sum([128, 32, 24]) * Decimal("65.68") + 500
    ceiling_group = north["satellite_coded_block_households"]
    count_reclass = [int((Decimal(ceiling_group) * share).quantize(Decimal(1), rounding=ROUND_HALF_UP))
                     for share in (Decimal(0), Decimal("0.25"), Decimal("0.50"), Decimal(1))]

    def compare(tbl, independent, key):
        report = read_csv(args.results / tbl)
        assert {r[key] for r in report} == set(independent)
        for row in report:
            expected = independent[row[key]]
            assert set(row) == set(expected)
            for column, value in expected.items():
                assert row[column] == value if column == key else abs(float(row[column]) - value) < 1e-7

    compare("task1_townships.csv", towns, "township")
    compare("task1_north_diagnostics.csv", diagnostics, "provider_technology")
    with (args.results / "task1_data_audit.json").open(encoding="utf-8") as stream:
        audit = json.load(stream)
    assert audit["sha256"] == hashes and all(audit["original_equals_v2_bytewise"].values())
    assert audit["rows"] == {"blocks": unique_blocks[0], "road_segments": unique_roads[0]}
    assert all(audit["primary_keys_unique_nonempty"].values()) and audit["orphan_road_segments"] == missing
    assert audit["blocks_without_road_measurements"] == 120 - sum(multiplicity.values())
    assert audit["road_segments_per_block"] == {str(key): val for key, val in multiplicity.items()}
    assert audit["observed_ranges"] == ranges
    assert audit["observed_categories"] == {
        "provider_technology": sorted({r["provider_technology"] for r in raw_inputs["blocks"]}),
        "road_type": sorted({r["road_type"] for r in raw_inputs["road_segments"]}),
    }
    assert county_totals == tuple(audit[key] for key in ("households_counted_once_in_block_table",
                                                          "subscriptions_counted_once_in_block_table",
                                                          "subscriptions_in_map_unserved_blocks"))
    challenge = read_csv(args.results / "task1_challenge.csv")
    assert len(challenge) == 5 and challenge[0]["scenario"] == "accept"
    assert [int(r["households_reclassified"]) for r in challenge] == [0] + count_reclass
    assert all(int(r["households_retaining_original_north_served_treatment"]) ==
               north["reported_served_block_households"] - int(r["households_reclassified"]) for r in challenge)
    assert all(int(r["unchallenged_terrestrial_coded_blocks"]) == north["terrestrial_coded_blocks"]
               and int(r["north_strictly_eligible"]) == 0 for r in challenge)
    fields = ("admin_cost_usd", "admin_cost_low_usd", "admin_cost_high_usd",
              "illustrative_prep_days", "conceded_scenario_max_days_from_prep_start",
              "contested_scenario_max_days_from_prep_start")
    for row in challenge:
        expected_cost = (0,) * 6 if row["scenario"] == "accept" else (
            administered, administered / 2, administered * 2, 30, 30 + 60 + 30, 30 + 60 + 60 + 90 + 30)
        assert tuple(Decimal(row[key]) for key in fields) == expected_cost
    print(json.dumps({"status": "passed", "county_hh_sub_unserved_sub": county_totals,
                      "hashes": hashes, "townships": towns, "north_road_diagnostics": diagnostics,
                      "challenge_usd": str(administered), "reclassified_hh": count_reclass}, indent=2))


if __name__ == "__main__":
    main()
