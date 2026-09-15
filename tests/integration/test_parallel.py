"""Behavioral tests for bible_grammar.intertextuality.parallel (/parallel),
requiring real corpus data — data/processed/words.parquet, lxx.parquet, and
translations.parquet.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.intertextuality.parallel import (
    parallel_passage, print_parallel, parallel_words,
)

_WORDS_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "words.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _WORDS_PARQUET.exists():
        pytest.skip(f"Data file not found: {_WORDS_PARQUET}")


class TestParallelPassage:
    def test_genesis_1_1_3_has_hebrew_lxx_and_kjv_columns(self) -> None:
        _skip_if_missing()
        df = parallel_passage('Gen', 1, 1, end_verse=3)
        assert len(df) == 3
        for col in ('reference', 'hebrew', 'lxx', 'kjv'):
            assert col in df.columns
        first = df.iloc[0]
        assert first['reference'] == 'Gen 1:1'
        assert 'God' in first['kjv']

    def test_nt_passage_uses_greek_and_kjv_columns_not_hebrew_lxx(self) -> None:
        # NT passages show Greek (TAGNT) | KJV — a different column shape
        # from OT passages ('greek_nt'/'kjv', no 'hebrew'/'lxx' columns).
        _skip_if_missing()
        df = parallel_passage('Jhn', 1, 1, end_verse=1)
        assert len(df) == 1
        assert 'greek_nt' in df.columns
        assert 'hebrew' not in df.columns
        assert 'Word' in df.iloc[0]['kjv']


class TestParallelWords:
    def test_genesis_1_1_word_level_detail(self) -> None:
        # Observed: Gen 1:1 has 7 Hebrew word-tokens and 10 LXX Greek
        # word-tokens (function words split differently).
        _skip_if_missing()
        result = parallel_words('Gen', 1, 1)
        assert result['reference'] == 'Gen 1:1'
        assert len(result['hebrew']) >= 6
        assert len(result['lxx']) >= 8

    def test_bara_is_tagged_qal_perfect_verb(self) -> None:
        # בָּרָא ("created") in Gen 1:1 should carry real morphological
        # tags: Qal stem, Perfect conjugation, Verb part of speech.
        _skip_if_missing()
        result = parallel_words('Gen', 1, 1)
        heb = result['hebrew']
        verb_row = heb[heb['part_of_speech'] == 'Verb'].iloc[0]
        assert verb_row['stem'] == 'Qal'
        assert verb_row['conjugation'] == 'Perfect'


class TestPrintParallel:
    def test_prints_real_output(self, capsys) -> None:
        _skip_if_missing()
        print_parallel('Gen', 1, 1, end_verse=3)
        out = capsys.readouterr().out
        assert 'Gen 1:1' in out
        assert len(out.strip()) > 100
