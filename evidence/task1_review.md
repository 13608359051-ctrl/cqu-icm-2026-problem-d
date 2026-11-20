# Independent review of Task 1

Author A. Reviewer B. Review date 2026-11-20.

I first read all four pages of the D statement and extracted the original CSVs independently with Python. Before seeing A's tables, I obtained the two matching SHA-256 pairs, township household and subscription totals, terrestrial status counts and six zero strict eligibility flags. The second check loads raw records into SQLite. It groups households by township and technology before any road join. It computes surveyed lengths in a separate joined query, then compares the complete published category rows and all four result files. The challenge counts and arithmetic use decimal numbers and half-up rounding. The reviewer did not import A's analysis code.

| Item | Expected | Observed | Evidence | Result |
|---|---|---|---|---|
| Original/V2, keys, links and field ranges | Two identical file pairs, 120 blocks and 248 matched roads | Both SHA-256 pairs and byte comparisons agree, no empty/duplicate IDs or missing links, 37/38/45 blocks have 1/2/3 roads. All reported ranges and categories agree. | `task1_independent_recalculation.json`, `analysis/review_task1.py` | Pass |
| Subscriptions and strict eligibility | Household-weighted rates across six towns, 0 eligible | All rows matched. County 6,591 / 14,496 = 45.47%. Map-unserved blocks contain 2,293 subscriptions. | Same calculation | Pass |
| North Ridge discrepancy | Twenty blocks including 17 flags, counts at one row per block | 2,135 households, 1,177 subscriptions, 1,908 under map flags, 377 under the terrestrial proxy, 1,531 satellite-coded, 227 already unserved. | Same calculation | Pass |
| Roads and uncertainty | Length-weighted road diagnostics independent of household denominator | All five technology groups matched at all thresholds. Satellite group 25.61 mi overall and 5.86 / 2.61 / 0.05 mi at or below −105 / −110 / −115 dBm. Cable group 3.40 mi and zero under all cutoffs. | Same calculation | Pass |
| Challenge counts, expense and timing | Scenario counts and totals recoverable from stated arithmetic | 0/383/766/1,531 potential cases, $12,585.12 ($6,292.56–$25,170.24), analogous 120/270 calendar days excluding intake/publication. Four unchallenged North Ridge terrestrial blocks keep the township ineligible in all rows. | Same calculation and source review below | Pass |
| Reproducibility | A's analysis regenerates its result set | Re-ran into a fresh temporary directory. Independent checks passed and all four published result files were byte-identical to regenerated files. | Commands below | Pass |

The FCC March 2024 Section 706 announcement supports 100/20 Mbps as the U.S. fixed benchmark. Hallowell's satellite treatment is separately identified as a terrestrial expansion goal, with the raw satellite flags retained under the problem rule. December 2025 U.S. BLS ECEC Table 1 supports $65.68 per hour total compensation for state and local government. 47 CFR (2024) §1.7006(d)(3),(6) support the 60-day reply, 30-day correction, 60-day dispute resolution and 90-day review windows for the historical federal analogy. FCC BDC guide supports dated order requests, installation quotes and provider-specific eligibility proof. Verified expense and timing are calculations conditional on declared assumptions. Actual households lack installation and service-tier evidence in the synthetic inputs. I found no claim of measured availability, definitive cabler footprint, or measured workload in A's results.

- [FCC March 2024 benchmark](https://docs.fcc.gov/public/attachments/DOC-401205A1.pdf)
- [BLS December 2025 ECEC release](https://www.bls.gov/news.release/archives/ecec_03202026.htm)
- [47 CFR §1.7006 (2024)](https://www.govinfo.gov/content/pkg/CFR-2024-title47-vol1/pdf/CFR-2024-title47-vol1-sec1-7006.pdf)
- [FCC fixed challenge evidence](https://help.bdc.fcc.gov/hc/en-us/articles/12000296843291-How-to-Submit-a-Successful-Fixed-Availability-Challenge)

```powershell
$data = (Get-ChildItem '..' -Directory -Filter '*秋季赛题目').FullName + '\2026_CQU_ICM_Problem_D_DATA'
$out = Join-Path ([System.IO.Path]::GetTempPath()) ('cqu-d-task1-review-' + [guid]::NewGuid().ToString('n'))
python analysis/task1.py --data $data --out $out
python analysis/review_task1.py --data $data --results $out
Get-ChildItem $out -File | ForEach-Object {
    if ((Get-FileHash $_.FullName).Hash -ne (Get-FileHash (Join-Path 'results' $_.Name)).Hash) {
        throw "Mismatch on $($_.Name)"
    }
}
```
