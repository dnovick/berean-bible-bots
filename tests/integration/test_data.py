"""
Integration smoke tests — require processed data files in data/processed/.
Run with: pytest -m integration
Skip with: pytest -m "not integration"
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

_PROCESSED = Path(__file__).resolve().parents[2] / "data" / "processed"
_WORDS_PARQUET = _PROCESSED / "words.parquet"
_LXX_PARQUET = _PROCESSED / "lxx.parquet"
_MACULA_OT_PARQUET = _PROCESSED / "macula_syntax_ot.parquet"

pytestmark = pytest.mark.integration


def _skip_if_missing(path: Path) -> None:
    if not path.exists():
        pytest.skip(f"Data file not found: {path}")


# ── db / words corpus ─────────────────────────────────────────────────────────

class TestWordsCorpus:
    def test_words_parquet_loads(self) -> None:
        _skip_if_missing(_WORDS_PARQUET)
        import pandas as pd
        df = pd.read_parquet(_WORDS_PARQUET)
        assert len(df) > 400_000, "Expected >400k word tokens"

    def test_tahot_present(self) -> None:
        _skip_if_missing(_WORDS_PARQUET)
        import pandas as pd
        df = pd.read_parquet(_WORDS_PARQUET)
        assert "TAHOT" in df["source"].values

    def test_tagnt_present(self) -> None:
        _skip_if_missing(_WORDS_PARQUET)
        import pandas as pd
        df = pd.read_parquet(_WORDS_PARQUET)
        assert "TAGNT" in df["source"].values

    def test_gen_1_1_exists(self) -> None:
        _skip_if_missing(_WORDS_PARQUET)
        import pandas as pd
        df = pd.read_parquet(_WORDS_PARQUET)
        gen1 = df[(df["book_id"] == "Gen") & (df["chapter"] == 1) & (df["verse"] == 1)
                  & (df["source"] == "TAHOT")]
        assert len(gen1) >= 7, "Gen 1:1 should have at least 7 Hebrew words"

    def test_strongs_column_exists(self) -> None:
        _skip_if_missing(_WORDS_PARQUET)
        import pandas as pd
        df = pd.read_parquet(_WORDS_PARQUET)
        assert "strongs" in df.columns


# ── concordance ───────────────────────────────────────────────────────────────

class TestConcordance:
    def test_bara_ot_count(self) -> None:
        _skip_if_missing(_WORDS_PARQUET)
        from bible_grammar.lexical.concordance import concordance
        result = concordance(strongs="H1254", corpus="OT", context=None)
        assert len(result) > 40, "H1254 (bara) should appear >40 times in OT"

    def test_logos_nt_count(self) -> None:
        _skip_if_missing(_WORDS_PARQUET)
        from bible_grammar.lexical.concordance import concordance
        result = concordance(strongs="G3056", corpus="NT", context=None)
        assert len(result) > 300, "G3056 (logos) should appear >300 times in NT"

    def test_concordance_columns_ot(self) -> None:
        _skip_if_missing(_WORDS_PARQUET)
        from bible_grammar.lexical.concordance import concordance
        result = concordance(strongs="H1254", corpus="OT", context=None)
        for col in ("reference", "book_id", "chapter", "verse", "word", "strongs"):
            assert col in result.columns, f"Missing column: {col}"

    def test_concordance_book_filter(self) -> None:
        _skip_if_missing(_WORDS_PARQUET)
        from bible_grammar.lexical.concordance import concordance
        result = concordance(strongs="H1254", corpus="OT", book="Gen", context=None)
        assert all(result["book_id"] == "Gen")

    def test_kjv_context_non_empty(self) -> None:
        _skip_if_missing(_WORDS_PARQUET)
        from bible_grammar.lexical.concordance import concordance
        result = concordance(strongs="H1254", corpus="OT", book="Gen", context="KJV")
        assert result["context_text"].str.len().sum() > 0


# ── lemma frequency ───────────────────────────────────────────────────────────

class TestLemmaFrequency:
    def test_bara_by_book(self) -> None:
        _skip_if_missing(_WORDS_PARQUET)
        from bible_grammar.lexical.concordance import lemma_frequency
        result = lemma_frequency(strongs="H1254", corpus="OT")
        assert "book_id" in result.columns
        assert "count" in result.columns
        assert len(result) > 0
        assert result["count"].sum() > 40

    def test_pct_sums_to_100(self) -> None:
        _skip_if_missing(_WORDS_PARQUET)
        from bible_grammar.lexical.concordance import lemma_frequency
        result = lemma_frequency(strongs="H1254", corpus="OT")
        assert abs(result["pct"].sum() - 100.0) < 1.0


# ── stats aggregation ─────────────────────────────────────────────────────────

class TestStatsAggregation:
    def test_niphal_perfects_by_book(self) -> None:
        _skip_if_missing(_WORDS_PARQUET)
        from bible_grammar.lexical.stats import niphal_perfects_by_book
        result = niphal_perfects_by_book()
        assert len(result) > 0
        assert "book_id" in result.columns
        assert "count" in result.columns

    def test_verb_stems_by_book_has_qal(self) -> None:
        _skip_if_missing(_WORDS_PARQUET)
        from bible_grammar.lexical.stats import verb_stems_by_book
        result = verb_stems_by_book(book="Gen")
        stems = result["stem"].tolist()
        assert "Qal" in stems

    def test_pos_distribution_tahot(self) -> None:
        _skip_if_missing(_WORDS_PARQUET)
        from bible_grammar.lexical.stats import pos_distribution
        result = pos_distribution(source="TAHOT")
        pos_values = result["part_of_speech"].tolist()
        assert "Verb" in pos_values
        assert "Noun" in pos_values


# ── MACULA OT syntax ──────────────────────────────────────────────────────────

class TestMaculaOT:
    def test_parquet_loads(self) -> None:
        _skip_if_missing(_MACULA_OT_PARQUET)
        from bible_grammar.core.syntax_ot import load_syntax_ot
        df = load_syntax_ot()
        assert len(df) > 400_000

    def test_required_columns_present(self) -> None:
        _skip_if_missing(_MACULA_OT_PARQUET)
        from bible_grammar.core.syntax_ot import load_syntax_ot
        df = load_syntax_ot()
        for col in ("book", "chapter", "verse", "lemma", "strong_h", "stem", "role"):
            assert col in df.columns, f"Missing column: {col}"

    def test_query_by_strongs(self) -> None:
        _skip_if_missing(_MACULA_OT_PARQUET)
        from bible_grammar.core.syntax_ot import query_syntax_ot
        result = query_syntax_ot(strong_h="H1254")
        assert len(result) > 40

    def test_query_by_stem(self) -> None:
        _skip_if_missing(_MACULA_OT_PARQUET)
        from bible_grammar.core.syntax_ot import query_syntax_ot
        result = query_syntax_ot(stem="niphal", book="Isa")
        assert len(result) > 0
        assert all(result["stem"].str.lower() == "niphal")

    def test_gen_1_1_roles(self) -> None:
        _skip_if_missing(_MACULA_OT_PARQUET)
        from bible_grammar.core.syntax_ot import query_syntax_ot
        result = query_syntax_ot(book="Gen", chapter=1, verse=1)
        assert len(result) >= 7


# ── LXX ──────────────────────────────────────────────────────────────────────

class TestLXX:
    def test_lxx_parquet_loads(self) -> None:
        _skip_if_missing(_LXX_PARQUET)
        import pandas as pd
        df = pd.read_parquet(_LXX_PARQUET)
        assert len(df) > 300_000

    def test_concordance_lxx_poieo(self) -> None:
        _skip_if_missing(_LXX_PARQUET)
        from bible_grammar.lexical.concordance import concordance
        result = concordance(strongs="G4160", corpus="LXX", context=None)
        assert len(result) > 500, "ποιέω should appear many times in LXX"
