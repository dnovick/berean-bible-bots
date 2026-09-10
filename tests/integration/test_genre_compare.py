"""Behavioral tests for bible_grammar.discourse.genre_compare (/genre-compare),
requiring real corpus data — data/processed/words.parquet.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.discourse.genre_compare import genre_compare

_WORDS_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "words.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _WORDS_PARQUET.exists():
        pytest.skip(f"Data file not found: {_WORDS_PARQUET}")


class TestGenreCompareOT:
    def test_wisdom_has_lowest_qal_share(self) -> None:
        # Qal (the base/unmarked stem) dominates every OT genre, but least
        # in Wisdom literature, which favors more varied stem usage.
        # Observed: Torah 72.4% Qal vs Wisdom 64.9% Qal.
        _skip_if_missing()
        df = genre_compare('OT', 'verb_stem')
        assert df.loc['Wisdom', 'Qal'] < df.loc['Torah', 'Qal']
        assert df.loc['Torah', 'total'] >= 15000


class TestGenreCompareNT:
    def test_gospels_favor_aorist_narrative_tense(self) -> None:
        # Gospels & Acts is narrative prose — dominated by the aorist
        # (simple past narrative tense). Pauline literature is
        # argumentative/present-tense-heavy by contrast.
        # Observed: Gospels & Acts 45.7% Aorist vs Pauline 30.0% Aorist;
        # Pauline leads on Present (55.5% vs 35.8%).
        _skip_if_missing()
        df = genre_compare('NT', 'verb_tense')
        assert df.loc['Gospels & Acts', 'Aorist'] > df.loc['Pauline', 'Aorist']
        assert df.loc['Pauline', 'Present'] > df.loc['Gospels & Acts', 'Present']
