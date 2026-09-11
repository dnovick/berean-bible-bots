"""Behavioral tests for bible_grammar.reporting.theological_reports, requiring
the word-level Hebrew<->LXX alignment (data/processed/word_alignment.parquet,
built via scripts/build_word_alignment.py).
Per docs/policies/test-coverage.md's priority plan (issue #662, item 4).
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.reporting.theological_reports import theological_summary_table

_WORD_ALIGNMENT_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "word_alignment.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _WORD_ALIGNMENT_PARQUET.exists():
        pytest.skip(f"Data file not found: {_WORD_ALIGNMENT_PARQUET}")


class TestTheologicalSummaryTable:
    def test_shalom_row_matches_trajectory_ground_truth(self) -> None:
        # Cross-verification: shalom's ot_total here must match
        # word_trajectory('H7965') directly (tests/integration/
        # test_trajectory.py) and word_study('H7965') (tests/integration/
        # test_wordstudy.py) — all three independent code paths over the
        # same underlying corpus. Observed: 237, continuity 'high'.
        _skip_if_missing()
        df = theological_summary_table()
        row = df[df['strongs'] == 'H7965'].iloc[0]
        assert row['ot_total'] == 237
        assert row['continuity'] == 'high'

    def test_tsedeq_has_medium_continuity(self) -> None:
        # Cross-verification with the divergent-LXX-rendering case found
        # in test_lxx_consistency.py (H6664/tsedeq diverges in Deu/Job) —
        # the trajectory-based continuity assessment should independently
        # agree this word has less-than-perfect continuity, not 'high'.
        _skip_if_missing()
        df = theological_summary_table()
        row = df[df['strongs'] == 'H6664'].iloc[0]
        assert row['continuity'] == 'medium'
