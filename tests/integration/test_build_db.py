"""Behavioral tests for scripts/build_db.py and the core parsers it wraps
(bible_grammar.core.ingest, .translations, .lxx) — all previously untested.
Requires the stepbible-data and (for LXX) TextFabric-cached submodule data.
Per docs/policies/test-coverage.md's priority plan (issue #676, Phase 2).

Every expected value here was directly observed by running the real
parsers, not invented.
"""

import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

_REPO = Path(__file__).resolve().parents[2]
_STEPBIBLE_DIR = _REPO / "stepbible-data"

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _STEPBIBLE_DIR.exists() or not any(_STEPBIBLE_DIR.iterdir()):
        pytest.skip(f"stepbible-data submodule not checked out: {_STEPBIBLE_DIR}")


class TestLoadAll:
    def test_total_and_testament_split(self) -> None:
        # Observed: 447,398 total word tokens — 305,652 Hebrew/Aramaic OT
        # (TAHOT) + 141,746 Greek NT (TAGNT).
        _skip_if_missing()
        from bible_grammar.core.ingest import load_all
        df = load_all()
        assert len(df) >= 440000
        assert (df["source"] == "TAHOT").sum() >= 300000
        assert (df["source"] == "TAGNT").sum() >= 140000


class TestLoadTranslations:
    def test_total_and_columns(self) -> None:
        # Observed: 70,492 verses across KJV (31,102), Vulgate Clementine
        # (31,434), and Peshitta NT (7,956).
        _skip_if_missing()
        from bible_grammar.core.translations import load_translations
        tr = load_translations()
        assert len(tr) >= 68000
        assert set(tr.columns) >= {"translation", "language", "book_id", "chapter", "verse", "text"}
        assert set(tr["translation"].unique()) >= {"KJV", "VulgClementine", "Peshitta"}


class TestLoadLxx:
    def test_total_and_canon_split(self) -> None:
        # Observed: 623,693 total LXX words — 496,853 canonical OT,
        # 126,840 deuterocanonical.
        _skip_if_missing()
        from bible_grammar.core.lxx import load_lxx
        lxx = load_lxx()
        assert len(lxx) >= 600000
        assert (~lxx["is_deuterocanon"]).sum() >= 480000
        assert lxx["is_deuterocanon"].sum() >= 100000


class TestBuildDbScript:
    def test_runs_end_to_end_and_regenerates_processed_data(self) -> None:
        # build_db.py has no importable functions of its own — it's a
        # thin __main__-only orchestration script over the parsers tested
        # above, plus save()/save_translations()/save_lxx()/save_alignment().
        # The only way to exercise its own statements is to actually run
        # it. Regenerates data/processed/*.parquet in place — idempotent,
        # gitignored, harmless (a developer running this manually has the
        # same effect).
        _skip_if_missing()
        result = subprocess.run(
            [sys.executable, str(_REPO / "scripts" / "build_db.py")],
            capture_output=True, text=True, cwd=_REPO, timeout=120,
        )
        assert result.returncode == 0, result.stdout + result.stderr
        assert "All done in" in result.stdout
