# Delivery and release status

Updated 20 November 2026.

## Final school-qualifier edition

- File: `private/ICM_D13528张芯源郭康杰袁懋.pdf` (not committed; `private/` is Git-ignored).
- Structure: 1 school cover (A4) + 24 solution pages + 2 AI-report pages = 27 pages.
- Running header on every solution page after the summary sheet: `Team # 13528 ... Page X of 24`.
- Page 1 is the COMAP-style summary sheet (no running header); page 2 is the Contents; page 24 is References; the Report on Use of AI Tools follows the references with no running header and is excluded from the 25-page limit.
- Checked by `analysis/build_submission.py`: page count, A4 size, headers, summary-sheet contents, anonymity (no names, institution, student IDs or local paths in the solution and AI report), continuous figure/table numbering, in-text citation coverage, and PDF size (<25 MB).
- Fonts: `pdffonts` shows embedded Times New Roman for the body; Chinese characters occur only on the school cover (SimSun), never in the solution or AI report.

## Review edition (anonymous)

- File: `output/pdf/Problem-D-review.pdf`, committed for teammates.
- Same solution and AI report without the school cover; the team number is replaced by the placeholder `TEAM REQUIRED`.
- Build: `python analysis/build_paper.py` (optionally `--team` after confirmation).

## Anonymous COMAP-style edition

- Build with `python analysis/build_submission.py --team <number> --cover "" --out private/ICM_anonymous.pdf`.
- The school cover carries names and student IDs by school requirement; it must not be used in the COMAP submission.

## Rules checked on 20 November 2026

- Local problem statement: English, one PDF, summary sheet first, table of contents, complete solution, in-text citations and reference list, AI-use report appended after the 25-page solution and excluded from the page count, anonymity other than the control number.
- Local AI policy `Contest_AI_Policy.pdf` (COMAP v102025): disclose tools and versions, state purposes, keep prompt/output records, cite AI tools in text and references, append a separate report.
- The AI report is now two English pages with tool/version table, representative prompts and outputs, a work-product index, and a verification statement. It contains no repository sharing links, no institution name and no unfinished-review language.
- COMAP live instructions were not re-consulted for this local qualifier; the school's own notice governs submission mechanics and file naming.

## Git

- The revision is committed on a local branch; no public branch or PR was created, because the timing of releasing an improved solution during the qualification round is the team's decision.
- Push and PR remain with the team after they review the diff and the final PDF.
