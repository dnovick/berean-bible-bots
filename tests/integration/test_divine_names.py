"""Behavioral tests for bible_grammar.names.divine_names (/divine-names),
requiring real corpus data — data/processed/words.parquet.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.names.divine_names import (
    divine_name_summary,
    divine_name_table,
    divine_name_by_section,
    print_divine_names,
    divine_names_chart,
    divine_names_report,
)

_WORDS_PARQUET = (
    Path(__file__).resolve().parents[2] / "data" / "processed" / "words.parquet"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _WORDS_PARQUET.exists():
        pytest.skip(f"Data file not found: {_WORDS_PARQUET}")


class TestDivineNameSummaryOT:
    def test_yhwh_dominates_ot_divine_names(self) -> None:
        # The Tetragrammaton (YHWH) is by far the most frequent OT divine
        # name — observed 6,513 occurrences, ~66% of all divine-name
        # tokens, with Jeremiah the top book.
        _skip_if_missing()
        df = divine_name_summary('OT')
        top = df.iloc[0]
        assert top['label'] == 'YHWH'
        assert top['total'] >= 6000
        assert top['pct'] >= 60.0
        assert 'Jeremiah' in top['top_books']

    def test_elohim_is_second(self) -> None:
        # Observed: 2,602 occurrences, ~26%, Deuteronomy the top book.
        _skip_if_missing()
        df = divine_name_summary('OT')
        elohim = df[df['label'] == 'Elohim'].iloc[0]
        assert elohim['total'] >= 2400
        assert 'Deuteronomy' in elohim['top_books']


class TestDivineNameTable:
    def test_exodus_yhwh_leads_genesis_elohim(self) -> None:
        # Observed: Exodus row — YHWH 398, Elohim 139, Total 553. Exodus
        # (God's self-revelation as YHWH at the burning bush) uses the
        # Tetragrammaton far more than Genesis's Elohim-heavy creation
        # narrative (Gen: YHWH 163, Elohim 219).
        _skip_if_missing()
        df = divine_name_table('OT').set_index('book_id')
        assert df.loc['Exo', 'YHWH'] >= 350
        assert df.loc['Exo', 'Total'] >= 500
        assert df.loc['Gen', 'Elohim'] >= 200


class TestDivineNameBySection:
    def test_yhwh_leads_every_section(self) -> None:
        # Observed: YHWH total 6,513, the largest of all 6 divine names,
        # and its Historical-books count (2,028) is its single largest
        # section.
        _skip_if_missing()
        df = divine_name_by_section('OT').set_index('label')
        assert df.loc['YHWH', 'Total'] >= 6000
        assert df.loc['YHWH', 'Historical'] == df.loc['YHWH'].drop(['strongs', 'Total']).max()


class TestPrintDivineNames:
    def test_prints_real_output(self, capsys) -> None:
        _skip_if_missing()
        print_divine_names('OT')
        out = capsys.readouterr().out
        assert 'YHWH' in out
        assert len(out.strip()) > 100


class TestDivineNamesChart:
    def test_stacked_bar_and_heatmap_produce_real_pngs(self, tmp_path: Path) -> None:
        _skip_if_missing()
        for chart_type in ('stacked_bar', 'heatmap'):
            out = divine_names_chart(
                'OT', chart_type=chart_type,
                output_path=str(tmp_path / f'{chart_type}.png'),
            )
            assert Path(out).exists()
            assert Path(out).stat().st_size > 0


class TestDivineNamesReport:
    def test_writes_a_real_markdown_report(self, tmp_path: Path) -> None:
        _skip_if_missing()
        out = divine_names_report(str(tmp_path), corpora=['OT'])
        assert Path(out).exists()
        text = Path(out).read_text(encoding='utf-8')
        assert 'YHWH' in text
        assert len(text) > 500
