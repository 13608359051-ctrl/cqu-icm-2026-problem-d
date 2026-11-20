# Clean-environment reproduction

Run November 20, 2026. The clean checkout came from the staged project files in a new temporary directory. The Python 3.12 environment was created there and installed from `requirements.txt`. After the first full success, the staged results directory and PDF were moved aside and the workflow was rerun from the original contest data with no output directory or PDF present.

```text
python analysis/reproduce.py --data <official attachment directory>
120 unique blocks, 248 unique roads, 6 townships. Both V2 files match byte for byte.
Passed independent hand check, exact optimization and row audit of 17 cases.
PASS: matching status and outputs for all 31 Task 3 runs.
15 solution pages + 5 AI pages, memo page 14, 448,798 bytes
```

The process exited 0. All 20 files under `results/` and the independently generated Task 3 JSON matched the project copies byte-for-byte. The clean PDF rebuilt all 20 pages. Each page's extracted text and each Poppler raster at 86 DPI matched exactly. The PDF containers have distinct trailer IDs and distinct SHA-256 values, so use the reviewed PDF as the exact review artifact.

| Artifact | SHA-256 |
|---|---|
| Reviewed PDF | `1332252fbc30453c55f79c5fed0f760a2ff33ede1bbfa1c72689c0bc46c4ff01` |
| Cleanly regenerated PDF | `692a1a3019f40439467c4474bcd49557f928d4a7cbdb612c10518628d48a4973` |
| Task 2 case table | `26a53dbd0c76b859bb57b718b35c6cb58ec99930883045e5a3665237cbb923c5` |
| Task 3 case table | `c8f88348c298db230d1caa497af02107350d57fe018cbf064d2eab80a839d9af` |
| Table and text inputs | `53c83a6b4b7a79f4a25fa1382326c1248648c0014aac5e6d158fdf0b7cb5bc8a` |

The Windows test used the installed Microsoft YaHei font for Chinese prompt excerpts. A different CJK fallback may affect the appendix's line breaks. Numerical outputs apply to the supplied synthetic input and stated scenarios.
