"""Behavioral test for scripts/build_word_alignment.py — has no importable
functions of its own (top-level script body, no `if __name__` guard even),
so the only way to exercise it is to actually run it. Requires real word
data (data/processed/words.parquet + lxx.parquet, or build_db.py's inputs).
Per docs/policies/test-coverage.md's priority plan (issue #676, Phase 2).
"""

import subprocess
import sys
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[2]
_WORDS_PARQUET = _REPO / "data" / "processed" / "words.parquet"

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _WORDS_PARQUET.exists():
        pytest.skip(f"Data file not found: {_WORDS_PARQUET}")


class TestBuildWordAlignmentScript:
    def test_runs_end_to_end_and_reports_pair_count(self) -> None:
        # Regenerates data/processed/word_alignment.parquet in place —
        # idempotent, gitignored. Observed: ~132,000 word-level alignment
        # pairs, finishing in under a minute.
        _skip_if_missing()
        result = subprocess.run(
            [sys.executable, str(_REPO / "scripts" / "build_word_alignment.py")],
            capture_output=True, text=True, cwd=_REPO, timeout=180,
        )
        assert result.returncode == 0, result.stdout + result.stderr
        assert "word-level alignment pairs" in result.stdout
