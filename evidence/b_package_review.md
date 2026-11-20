# B's independent review of delivery instructions

The coordinating agent authored the README and release record. Subagent B checked the current files and official sources on 2026-11-20.

| Check | Method | Actual result | Status |
|---|---|---|---|
| README links | Extract the Markdown link targets and check them from the repository root. | All 16 local targets exist, including paper source, all three task scripts, the acceptance table and the release record. | Pass |
| README commands | Parse both PowerShell blocks, run the launcher and check the option names with both scripts' help, then resolve data input relative to the repository. | Both blocks parse. `py -3.12` resolves to 3.12.2 on the review host. The documented sibling path contains all four official D CSVs. Entrypoints recognize the documented options. | Pass |
| Team-specific compile path | Exercise `analysis/build_paper.py --team REVIEW-TEST --output <temporary path>` with a test identifier and the same source outputs. | Temporary build passed all built-in header, counts, memo, disclosure, metadata and size checks. The review PDF stayed separate. A real competition control number has yet to be supplied. | Pass |
| Local source and rules | Read the local statement and AI policy, recompute their SHA-256 hashes, and list the current organizer package. | The hashes match the release record. The statement/policy and source data are present. The package gives the paper and AI appendix requirements. A current CQU registration, upload or release notice was not found in that package. | Pass for recorded scope |
| External rules | Read live COMAP 2027 instructions and search official CQU channels for the current autumn event. | COMAP's rule covers the January 28–February 1, 2027 competition window. Its style limits and AI appendix guidance inform this paper. Its deadlines, filenames and prohibition on during-contest publication belong to that event. CQU notices located independently concern the past autumn cycle or spring 2026. The current CQU release, distribution terms, team number and submission details remain unconfirmed. | Local publication pending |

The original CQU contest input files are obtained separately as documented in README. The paper review for the final review-edition PDF is in `evidence/b_paper_review.md`.

- [COMAP 2027 contest instructions](https://contest.comap.com/undergraduate/contests/mcm/instructions.html)
- [CQU Mathematics Laboratory notices](https://sci.cqu.edu.cn/mathlab/sy/tzgg.htm)
- [CQU notice for the previous autumn cycle](https://sci.cqu.edu.cn/info/1176/8709.htm)
- [CQU 2026 spring contest requirements](https://sci.cqu.edu.cn/info/1176/8840.htm)
