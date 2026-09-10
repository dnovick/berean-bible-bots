#!/usr/bin/env python3
"""Enforce the "coverage must not decrease" policy — docs/policies/test-coverage.md.

Runs pytest with coverage over src/bible_grammar/ and scripts/, compares the
result against the floor recorded in coverage-baseline.json, and exits 1 if
coverage has dropped below it.

Two modes, because integration tests need data/processed/*.parquet built
locally and CI never builds that data (see docs/policies/capability-development.md):

  --unit (default): runs `pytest tests/ -m "not integration"` — what CI can
                     always run, checked against coverage-baseline.json's
                     unit_min_percent. This is the mode review-pr.yml runs.
  --full          : runs the complete suite, including integration tests —
                     what a developer runs locally before a substantial PR,
                     checked against full_min_percent. Skips (exit 0, with a
                     warning) if data/processed/ isn't built, rather than
                     failing on a misleadingly low number.

Usage:
    python scripts/check_coverage.py                    # unit-only, CI mode
    python scripts/check_coverage.py --full              # full suite, local mode
    python scripts/check_coverage.py --update-baseline   # after a deliberate
                                                          # coverage improvement,
                                                          # rewrite the floor to
                                                          # match what was just measured
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import date
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent
_BASELINE_FILE = _REPO / "coverage-baseline.json"
_DATA_PROCESSED = _REPO / "data" / "processed"
_COV_SOURCES = ["src/bible_grammar", "scripts"]

# A drop this small is measurement noise (line-count rounding), not a real
# regression — only fail below floor - TOLERANCE.
_TOLERANCE = 0.1


def _load_baseline() -> dict:
    with open(_BASELINE_FILE) as f:
        return json.load(f)


def _run_coverage(full: bool) -> float:
    json_out = _REPO / f"coverage-{'full' if full else 'unit'}.json"
    cmd = [sys.executable, "-m", "pytest", "tests/"]
    if not full:
        cmd += ["-m", "not integration"]
    for src in _COV_SOURCES:
        cmd += [f"--cov={src}"]
    cmd += ["--cov-report=term", f"--cov-report=json:{json_out}", "-q"]

    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=_REPO)
    if result.returncode not in (0, 1):
        # 1 = pytest ran but some tests failed; still produces a usable
        # coverage report. Anything else (2+) means pytest itself errored.
        print(f"pytest exited {result.returncode} — aborting coverage check.")
        sys.exit(result.returncode)

    with open(json_out) as f:
        data = json.load(f)
    json_out.unlink()
    return data["totals"]["percent_covered"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full", action="store_true",
                        help="Run the full suite (including integration tests).")
    parser.add_argument("--update-baseline", action="store_true",
                        help="Rewrite coverage-baseline.json to the just-measured percentage.")
    args = parser.parse_args()

    if args.full and not any(_DATA_PROCESSED.glob("*.parquet")):
        print(f"--full requested but {_DATA_PROCESSED} has no built data — "
              "integration tests would all skip, giving a misleadingly low "
              "number. Build it first (see docs/policies/capability-development.md) "
              "or drop --full. Not failing the check.")
        sys.exit(0)

    baseline = _load_baseline()
    key = "full_min_percent" if args.full else "unit_min_percent"
    floor = baseline[key]

    percent = _run_coverage(full=args.full)
    print(f"\nMeasured coverage ({'full' if args.full else 'unit'}): {percent:.2f}%")
    print(f"Floor ({key}): {floor:.2f}%")

    if args.update_baseline:
        baseline[key] = round(percent, 2)
        baseline["updated"] = date.today().isoformat()
        with open(_BASELINE_FILE, "w") as f:
            json.dump(baseline, f, indent=2)
            f.write("\n")
        print(f"Updated {_BASELINE_FILE.name}: {key} -> {percent:.2f}%")
        return

    if percent < floor - _TOLERANCE:
        print(f"\nFAIL: coverage dropped below the floor "
              f"({percent:.2f}% < {floor:.2f}%). "
              "Add tests, or if this drop is deliberate and reviewed "
              "(e.g. removing dead code), rerun with --update-baseline.")
        sys.exit(1)

    print("\nOK: coverage at or above floor.")


if __name__ == "__main__":
    main()
