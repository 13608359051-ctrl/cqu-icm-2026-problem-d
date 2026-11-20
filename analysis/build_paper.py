"""Compile the editable paper and check its submission-format invariants."""

import argparse
import json
import re
from pathlib import Path

from pypdf import PdfReader
import typst


ROOT = Path(__file__).resolve().parents[1]
PLACEHOLDER = "TEAM NUMBER REQUIRED"


def validate(path, team):
    reader = PdfReader(path)
    pages = [re.sub(r"\s+", " ", p.extract_text()).strip() for p in reader.pages]
    total = len(pages)
    for i, page in enumerate(pages, start=1):
        assert page.startswith(f"Team # {team} Problem D Page {i} of {total}"), page[:120]
        assert len(page) > 250 and "\ufffd" not in page, (i, len(page))
    assert "Summary Sheet The Last Mile of Broadband" in pages[0]
    assert pages[1].split(" of ", 1)[1].startswith(f"{total} Contents")
    assert all(label in " ".join(pages[:-1]) for label in (
        "Executive Summary", "Task 1.", "Task 2.", "Task 3.", "Share Your Insights"))
    memo, = [i for i, page in enumerate(pages) if "To Hallowell County Board of Commissioners" in page]
    assert "Conditions before construction" in pages[memo]
    appendix, = [i for i, page in enumerate(pages) if re.search(r"of \d+ \d+ Report on Use of AI Tools Tool", page)]
    assert 0 < memo < appendix <= 25
    assert "References" in pages[memo + 1]
    assert not (reader.metadata.author or "").strip()
    assert not any(re.search(r"github\.com/|[A-Z]:\\\\|Users[/\\\\]", page) for page in pages), "Identifying path in PDF"
    assert path.stat().st_size < 25_000_000

    expected = json.loads((ROOT / "results/paper_data.json").read_text(encoding="utf-8"))["values"]
    for key in ("ppp_hh", "coop_hh", "advantage", "override_count"):
        assert expected[key] in pages[0] and expected[key] in pages[memo], key
    print(f"{appendix} solution pages + {total - appendix} AI pages, memo page {memo + 1}, {path.stat().st_size:,} bytes")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--team", default=PLACEHOLDER, help="Confirmed control number. Omit for the marked review draft.")
    parser.add_argument("--output", type=Path, default=ROOT / "output/pdf/Problem-D-review.pdf")
    args = parser.parse_args()
    if args.team != PLACEHOLDER and not re.fullmatch(r"[A-Za-z0-9-]{1,20}", args.team):
        parser.error("Enter the control number issued by the organizer.")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    typst.compile(ROOT / "paper/main.typ", args.output, root=ROOT, sys_inputs={"team": args.team})
    validate(args.output, args.team)
