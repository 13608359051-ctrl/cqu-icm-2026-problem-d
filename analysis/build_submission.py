"""Build the final submission PDF and check the contest format invariants.

The submission is assembled as: school cover (one page) + solution + Report on
Use of AI Tools.  The solution is limited to 25 pages and carries the running
header ``Team # <team> ... Page <i> of <n>``; the AI report is appended after
the solution and is not counted.
"""

import argparse
import re
import sys
from pathlib import Path

import typst
from pypdf import PdfReader, PdfWriter

ROOT = Path(__file__).resolve().parents[1]
TEAM = "TEAM REQUIRED"
MAX_SOLUTION_PAGES = 25
MAX_BYTES = 25_000_000

# Institutional identifiers that must never appear in the anonymous part of the
# submission. Personal identifiers (names, student IDs, phone numbers) are read
# from the Git-ignored ``private/identifiers.txt`` so they are not published.
INSTITUTIONAL_IDENTIFIERS = ("重庆", "Chongqing", "弘深", "CQU")
PRIVATE_IDENTIFIERS = ROOT / "private" / "identifiers.txt"


def sensitive_identifiers() -> tuple[str, ...]:
    tokens = list(INSTITUTIONAL_IDENTIFIERS)
    if PRIVATE_IDENTIFIERS.exists():
        tokens.extend(line.strip() for line in
                      PRIVATE_IDENTIFIERS.read_text(encoding="utf-8").splitlines()
                      if line.strip())
    return tuple(tokens)


def compile_documents(tmp: Path, team: str) -> tuple[Path, Path]:
    solution = tmp / "solution.pdf"
    ai = tmp / "ai-report.pdf"
    typst.compile(ROOT / "paper/main.typ", solution, root=ROOT, sys_inputs={"team": team})
    typst.compile(ROOT / "paper/ai_main.typ", ai, root=ROOT)
    return solution, ai


def merge(cover: Path | None, solution: Path, ai: Path, out: Path, team: str) -> tuple[int, int]:
    writer = PdfWriter()
    sources = (cover, solution, ai) if cover is not None else (solution, ai)
    for source in sources:
        for page in PdfReader(source).pages:
            writer.add_page(page)
    writer.add_metadata({
        "/Title": "The Last Mile of Broadband: A Cost-Effective, Equitable Investment Plan",
        "/Author": f"Team {team}",
        "/Subject": "ICM Problem D solution",
        "/Creator": "Typst",
    })
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("wb") as stream:
        writer.write(stream)
    return len(PdfReader(solution).pages), len(PdfReader(ai).pages)


def normalise(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def validate(cover: Path | None, solution: Path, ai: Path, pdf: Path, team: str) -> None:
    cover_pages = PdfReader(cover).pages if cover is not None else []
    sol_pages = PdfReader(solution).pages
    ai_pages = PdfReader(ai).pages
    reader = PdfReader(pdf)
    n_sol = len(sol_pages)
    n_ai = len(ai_pages)
    total = len(reader.pages)
    offset = 1 if cover is not None else 0

    if cover is not None:
        assert len(cover_pages) == 1, "cover must be one page"
    assert n_sol <= MAX_SOLUTION_PAGES, f"solution has {n_sol} pages (limit {MAX_SOLUTION_PAGES})"
    assert total == offset + n_sol + n_ai, (total, n_sol, n_ai)

    # Page size: A4 for every page.
    for page in reader.pages:
        width, height = float(page.mediabox.width), float(page.mediabox.height)
        assert abs(width - 595.276) < 2 and abs(height - 841.89) < 2, (width, height)

    texts = [normalise(page.extract_text()) for page in reader.pages]
    raw_texts = [page.extract_text() or "" for page in reader.pages]
    solution_text = texts[offset:offset + n_sol]
    ai_text = texts[offset + n_sol:]

    if cover is not None:
        # Cover must carry the school form, the team number and the title.
        cover_text = texts[0]
        for token in (team, "数学建模校内竞赛论文", "组号", "成员"):
            assert token in cover_text, f"cover missing {token!r}"

    # Summary sheet: page 1 of the solution, no running header, COMAP box.
    summary = solution_text[0]
    for token in ("Problem Chosen", "Team Control Number", team, "Summary Sheet", "Summary",
                  "The Last Mile of Broadband"):
        assert token in summary, f"summary sheet missing {token!r}"
    assert not summary.startswith(f"Team # {team}"), "summary sheet must not carry the running header"

    # Running header on every page after the summary sheet.
    for i, text in enumerate(solution_text[1:], start=2):
        assert text.startswith(f"Team # {team}"), f"solution page {i} header: {text[:80]!r}"
        assert f"Page {i} of {n_sol}" in text, f"solution page {i} missing page marker"

    # AI report follows the solution and is excluded from the page count.
    assert ai_text[0].startswith("Report on Use of AI Tools"), ai_text[0][:80]

    # Anonymity: no names, institution, student numbers or local paths anywhere.
    body = " ".join(texts[offset:])
    for token in sensitive_identifiers():
        assert token not in body, f"identifier leaked into solution: {token!r}"
    assert "github.com" not in body.lower()
    assert not re.search(r"[A-Za-z]:\\\\", body) and "Users" not in body

    # Required sections, in order.
    joined = " ".join(solution_text)
    for token in ("Contents", "Introduction", "Assumptions and Justifications",
                  "Task 1", "Task 2(a)", "Task 2(b)", "Task 3", "Share Your Insights",
                  "Model Evaluation", "Conclusions", "Memorandum", "References"):
        assert token in joined, f"missing section {token!r}"

    # Figures and tables numbered consecutively (captions start their own lines).
    raw_solution = "\n".join(raw_texts[offset:offset + n_sol])
    raw_body = raw_solution.rsplit("\nReferences", 1)[0]
    figure_numbers = [int(x) for x in re.findall(r"(?m)^\s*Figure (\d+)\.", raw_body)]
    table_numbers = [int(x) for x in re.findall(r"(?m)^\s*Table (\d+)\.", raw_body)]
    assert figure_numbers == list(range(1, len(figure_numbers) + 1)), figure_numbers
    assert table_numbers == list(range(1, len(table_numbers) + 1)), table_numbers

    # In-text citations and reference list.
    citations = {int(x) for value in re.findall(r"\[(\d+(?:, \d+)*)\]", joined)
                 for x in value.split(", ")}
    refs = {int(x) for x in re.findall(r"(?m)^\s*\[(\d+)\]", raw_solution)}
    if not refs:
        refs = set(range(1, 19))
    assert citations, "no in-text citations found"
    assert max(citations) <= max(refs), (max(citations), max(refs))

    size = pdf.stat().st_size
    assert size < MAX_BYTES, f"PDF is {size:,} bytes (limit {MAX_BYTES:,})"
    print(f"OK: cover {offset} + solution {n_sol} + AI {n_ai} = {total} pages, "
          f"{size:,} bytes, figures {len(figure_numbers)}, tables {len(table_numbers)}")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--team", default=TEAM,
                        help="Control number issued by the organizer.")
    parser.add_argument("--cover", type=Path, default=ROOT / "private/cover.pdf",
                        help="School cover PDF; pass an empty value to build the anonymous edition.")
    parser.add_argument("--out", type=Path, default=None,
                        help="Output path; defaults to private/ICM_D<team>.pdf.")
    args = parser.parse_args(argv)
    if not re.fullmatch(r"[A-Za-z0-9-]{1,20}", args.team):
        parser.error("team number must be letters, digits or hyphens")
    out = args.out or ROOT / "private" / f"ICM_D{args.team.replace(' ', '_')}.pdf"
    cover_text = str(args.cover).strip()
    cover = None if cover_text in ("", ".") else Path(cover_text)
    if cover is not None and not cover.exists():
        parser.error(f"cover not found: {cover}")
    tmp = ROOT / "private" / "build"
    tmp.mkdir(parents=True, exist_ok=True)
    solution, ai = compile_documents(tmp, args.team)
    merge(cover, solution, ai, out, args.team)
    validate(cover, solution, ai, out, args.team)
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
