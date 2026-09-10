"""Behavioral tests for bible_grammar.ot.ot_semantic_domains, requiring real
corpus data — data/processed/macula_syntax_ot.parquet.
Per docs/policies/test-coverage.md's priority plan (issue #662, item 4).
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.ot.ot_semantic_domains import ot_domain_data, ot_top_domain_lemmas

_MACULA_OT_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "macula_syntax_ot.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _MACULA_OT_PARQUET.exists():
        pytest.skip(f"Data file not found: {_MACULA_OT_PARQUET}")


class TestSpeechDomain:
    def test_domain_41_total(self) -> None:
        # Coredomain 41 = Speech/Utterance. Observed: 12,461 tokens.
        _skip_if_missing()
        assert len(ot_domain_data(41)) >= 12000

    def test_amar_leads_speech_domain(self) -> None:
        # אָמַר ("said") dominates the Speech/Utterance domain, as expected
        # for the OT's single most common speech verb. Observed: count
        # 2,127 for the "he.said" gloss variant alone.
        _skip_if_missing()
        df = ot_top_domain_lemmas(41, top_n=5)
        top = df.iloc[0]
        assert top['lemma'] == 'אָמַר'
        assert top['strong_h'] == 'H559'
        assert top['count'] >= 2000
