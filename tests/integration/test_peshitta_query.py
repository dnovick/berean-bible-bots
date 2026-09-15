"""Behavioral tests for bible_grammar.core.peshitta_query, requiring the
optional text-fabric package (not in CI's install line) plus the syrnt/tf
Text-Fabric dataset. Uses the collection-safety guard pattern (try/except
import at module scope) since text-fabric being absent must not crash
pytest collection — same pattern as tests/integration/test_exercise_pdf.py.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

try:
    from bible_grammar.core.peshitta_query import query_peshitta
    _AVAILABLE = True
except ImportError:
    query_peshitta = None  # type: ignore[assignment]
    _AVAILABLE = False

_SYRNT_TF = Path(__file__).resolve().parents[2] / "syrnt" / "tf" / "0.1"

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _AVAILABLE:
        pytest.skip("text-fabric not installed")
    if not _SYRNT_TF.exists():
        pytest.skip(f"Data file not found: {_SYRNT_TF}")


class TestQueryPeshitta:
    def test_returns_real_peshitta_tokens(self) -> None:
        # Observed: 109,640 Syriac word tokens across the Peshitta NT.
        _skip_if_missing()
        df = query_peshitta()
        assert len(df) >= 100000
        for col in ('book', 'chapter', 'verse', 'word', 'sp'):
            assert col in df.columns

    def test_acts_luke_matthew_are_the_longest_books(self) -> None:
        # Observed: Act (15,383), Luk (15,234), Mat (13,979) lead by token
        # count — the longest NT narrative books.
        _skip_if_missing()
        df = query_peshitta()
        top3 = set(df['book'].value_counts().head(3).index)
        assert top3 == {'Act', 'Luk', 'Mat'}

    def test_noun_and_verb_are_the_dominant_parts_of_speech(self) -> None:
        # Observed: noun 33,717, verb 30,441 — the two largest 'sp' values.
        _skip_if_missing()
        df = query_peshitta()
        top2 = set(df['sp'].value_counts().head(2).index)
        assert top2 == {'noun', 'verb'}
