"""Behavioral tests for bible_grammar.names.christological_titles
(/christological-titles), requiring real corpus data — data/processed/words.parquet.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.names.christological_titles import (
    title_counts,
    print_title_counts,
    title_chart,
    title_verses,
    title_report,
)

_WORDS_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "words.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _WORDS_PARQUET.exists():
        pytest.skip(f"Data file not found: {_WORDS_PARQUET}")


class TestTitleCountsGospels:
    def test_son_of_man_is_high_confidence_and_frequent(self) -> None:
        # "Son of Man" (ὁ υἱὸς τοῦ ἀνθρώπου) is Jesus's own most
        # characteristic self-designation in the Gospels — the paradigm
        # high-confidence self-referential title. Observed: 88 occurrences.
        _skip_if_missing()
        df = title_counts(scope='gospels')
        row = df[df['title'] == 'Son of Man'].iloc[0]
        assert row['confidence'] == 'high'
        assert row['Total'] >= 80

    def test_kyrios_is_the_most_frequent_title(self) -> None:
        # "Lord" (κύριος) is the single most common title applied to
        # Jesus in the Gospels, though low self-reference confidence
        # (it's mostly applied by others, not self-claimed).
        _skip_if_missing()
        df = title_counts(scope='gospels')
        top = df.sort_values('Total', ascending=False).iloc[0]
        assert top['title'] == 'Lord (Kyrios)'
        assert top['Total'] >= 200


class TestPrintTitleCounts:
    def test_prints_real_output(self, capsys) -> None:
        _skip_if_missing()
        print_title_counts(scope='gospels')
        out = capsys.readouterr().out
        assert 'Son of Man' in out
        assert len(out.strip()) > 100


class TestTitleChart:
    def test_produces_a_real_png(self, tmp_path: Path) -> None:
        _skip_if_missing()
        out = title_chart(scope='gospels', output_path=str(tmp_path / 'titles.png'))
        assert Path(out).exists()
        assert Path(out).stat().st_size > 0


class TestTitleVerses:
    def test_son_of_man_verses_match_kjv_text(self) -> None:
        # Observed: 96 verses total across the Gospels, each with real KJV
        # text attached (not just a bare reference).
        _skip_if_missing()
        df = title_verses('Son of Man')
        assert len(df) >= 90
        assert (df['kjv_text'].str.len() > 0).all()

    def test_unknown_title_raises_value_error(self) -> None:
        _skip_if_missing()
        with pytest.raises(ValueError):
            title_verses('Not A Real Title')


class TestTitleReport:
    def test_writes_a_real_markdown_report(self, tmp_path: Path) -> None:
        _skip_if_missing()
        out = title_report(output_dir=str(tmp_path))
        assert Path(out).exists()
        text = Path(out).read_text(encoding='utf-8')
        assert 'Son of Man' in text
        assert len(text) > 500
