"""Behavioral tests for bible_grammar.verbal_syntax.relative_clauses,
requiring real corpus data — data/processed/macula_syntax_ot.parquet.
Per docs/policies/test-coverage.md's priority plan (issue #662, item 4).
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.verbal_syntax.relative_clauses import relative_clauses, relative_clause_summary

_MACULA_OT_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "macula_syntax_ot.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _MACULA_OT_PARQUET.exists():
        pytest.skip(f"Data file not found: {_MACULA_OT_PARQUET}")


class TestRelativeClauses:
    def test_genesis_total(self) -> None:
        _skip_if_missing()
        assert len(relative_clauses('Gen')) >= 390   # observed: 412


class TestRelativeClauseSummary:
    def test_object_qatal_is_the_top_combination(self) -> None:
        # Relative clauses with an object-role gap filled by a qatal
        # (perfect) verb form is the single most common pattern in
        # Genesis. Observed: count 155, 37.6%.
        _skip_if_missing()
        df = relative_clause_summary('Gen')
        top = df.sort_values('count', ascending=False).iloc[0]
        assert top['inferred_role'] == 'object'
        assert top['rel_verb_form'] == 'qatal'
        assert top['pct'] >= 30.0
