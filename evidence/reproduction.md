# Clean-environment reproduction

Run November 20, 2026. A temporary checkout and Python 3.12 environment were created and the pinned requirements installed. The first draft was reproduced, then revised with additional equations and the workflow diagram. The final revision was copied from the stage to a new temporary checkout. The staged results directory and PDF were moved aside, and the same clean environment regenerated every output from the organizer-supplied data.

```text
python analysis/reproduce.py --data <official attachment directory>
120 unique blocks, 248 unique roads, 6 townships. Both V2 files match byte for byte.
Passed independent hand check, exact optimization and row audit of 17 cases.
PASS: matching status and outputs for all 31 Task 3 runs.
PASS: all 8 lease-price rows match exact rational discounting.
16 solution pages + 5 AI pages, memo page 15, 492,717 bytes
```

The process exited 0. All 21 files under `results/` and the independently generated Task 3 JSON matched the project copies byte-for-byte. Each of the 21 PDF pages produced identical extracted text and identical Poppler rasters at 86 DPI. The PDF containers have distinct trailer IDs and SHA-256 values, so use the reviewed PDF as the exact review artifact.

| Artifact | SHA-256 |
|---|---|
| Reviewed PDF | `2be03233a3f3d36758668253d1d775ff71f0a8e75b1b87e0584c8a445f0358f3` |
| Cleanly regenerated PDF | `47e1053383f5756b8871f6fba8b5a5c639a69b80554f3062ba20c845d256a896` |
| Workflow diagram | `9b62a841fa009941ea5b2f2af9ada2e40c1daed0b7d7462f5b89790fa84818ca` |
| Task 2 case table | `26a53dbd0c76b859bb57b718b35c6cb58ec99930883045e5a3665237cbb923c5` |
| Task 3 case table | `c8f88348c298db230d1caa497af02107350d57fe018cbf064d2eab80a839d9af` |
| Table and text inputs | `53c83a6b4b7a79f4a25fa1382326c1248648c0014aac5e6d158fdf0b7cb5bc8a` |

The Windows test used the installed Microsoft YaHei font for Chinese prompt excerpts. A different CJK fallback may affect the appendix's line breaks. Numerical outputs apply to the supplied synthetic input and stated scenarios.
