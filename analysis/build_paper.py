"""Compile the review edition of the paper and check its format invariants.

The review edition contains the solution and the AI report but no school cover.
The final submission, which adds the cover, is produced by
``analysis/build_submission.py``.
"""

import argparse
import re
from pathlib import Path

from build_submission import compile_documents, validate

ROOT = Path(__file__).resolve().parents[1]
PLACEHOLDER = "TEAM REQUIRED"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--team", default=PLACEHOLDER,
                        help="Confirmed control number; omit for the review draft.")
    parser.add_argument("--output", type=Path, default=ROOT / "output/pdf/Problem-D-review.pdf")
    args = parser.parse_args(argv)
    if args.team != PLACEHOLDER and not re.fullmatch(r"[A-Za-z0-9-]{1,20}", args.team):
        parser.error("team number must be letters, digits or hyphens")
    tmp = ROOT / "private" / "build"
    tmp.mkdir(parents=True, exist_ok=True)
    solution, ai = compile_documents(tmp, args.team)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    from pypdf import PdfReader, PdfWriter

    writer = PdfWriter()
    for source in (solution, ai):
        for page in PdfReader(source).pages:
            writer.add_page(page)
    with args.output.open("wb") as stream:
        writer.write(stream)
    validate(None, solution, ai, args.output, args.team)
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

