"""Behavioral tests for bible_grammar.lexical.semantic_profile (/semantic-profile),
requiring real corpus data — data/processed/ plus the word-level Hebrew<->LXX
alignment (data/processed/word_alignment.parquet, built via
scripts/build_word_alignment.py).
"""

import sys
import unicodedata
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.lexical.semantic_profile import (
    semantic_profile, print_semantic_profile, save_semantic_profile,
)

_WORD_ALIGNMENT_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "word_alignment.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _WORD_ALIGNMENT_PARQUET.exists():
        pytest.skip(f"Data file not found: {_WORD_ALIGNMENT_PARQUET}")


class TestSemanticProfile:
    def test_shalom_profile_shape(self) -> None:
        _skip_if_missing()
        sp = semantic_profile('H7965')
        for key in ('word_study', 'lxx_consistency', 'collocations', 'morph'):
            assert key in sp

    def test_shalom_lxx_consistency_is_perfect(self) -> None:
        # שָׁלוֹם renders as εἰρήνη with 100% consistency across every
        # aligned book — no divergent books. Observed: 116 aligned pairs.
        _skip_if_missing()
        sp = semantic_profile('H7965')
        lc = sp['lxx_consistency']
        # NFC-normalize — the corpus stores this lemma in a polytonic (non-NFC) form.
        assert unicodedata.normalize('NFC', lc['corpus_primary']) == unicodedata.normalize('NFC', 'εἰρήνη')
        assert lc['overall_consistency'] == 100.0
        assert lc['divergent_books'] == []
        assert lc['total_aligned'] >= 100

    def test_shalom_collocations_non_empty(self) -> None:
        # Regression guard: this key was silently empty before the
        # collocation.py homonym-letter fix (see test_collocation.py).
        _skip_if_missing()
        sp = semantic_profile('H7965')
        assert not sp['collocations'].empty


class TestPrintSemanticProfile:
    def test_prints_real_output(self, capsys) -> None:
        _skip_if_missing()
        print_semantic_profile('H7965')
        out = capsys.readouterr().out
        assert 'H7965' in out
        assert 'peace' in out
        assert len(out.strip()) > 200


class TestSaveSemanticProfile:
    def test_writes_a_real_markdown_report_with_chart(self, tmp_path: Path) -> None:
        # save_semantic_profile defaults to output/reports/ (git-tracked) —
        # always redirect via output_dir in tests.
        _skip_if_missing()
        out = save_semantic_profile('H7965', output_dir=str(tmp_path))
        assert Path(out).exists()
        text = Path(out).read_text(encoding='utf-8')
        assert 'H7965' in text
        assert len(text) > 1000
        # A chart PNG should also have been written alongside the report.
        pngs = list(tmp_path.glob('*.png'))
        assert len(pngs) == 1
        assert pngs[0].stat().st_size > 0
