"""Recalculate the case, independently verify the results, and build the paper."""

import argparse
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, required=True)
    data = str(parser.parse_args().data.resolve(strict=True))
    commands = [
        ("analysis/task1.py", "--data", data, "--out", "results"),
        ("analysis/task2.py", "--data", data, "--out", "results"),
        ("analysis/task3.py", "--data-dir", data, "--out", "results"),
        ("analysis/review_task1.py", "--data", data, "--results", "results"),
        ("analysis/verify_task2.py", "--data", data, "--results", "results"),
        ("evidence/task3_independent.py", "--data", data, "--out", "evidence/task3_independent.json", "--compare", "results"),
        ("analysis/paper_data.py",),
        ("analysis/build_paper.py",),
    ]
    for command in commands:
        print(command[0], flush=True)
        subprocess.run((sys.executable, *command), cwd=ROOT, check=True)
