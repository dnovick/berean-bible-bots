"""Behavioral tests for bible_grammar.intertextuality.intertextuality
(/intertextuality), requiring the scrollmapper cross-reference data —
scrollmapper-data/sources_backup/extras/cross_references.txt (a git submodule).
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from bible_grammar.intertextuality.intertextuality import (
    intertextuality,
    print_intertextuality,
    intertextuality_graph,
    intertextuality_report,
)

_XREF_FILE = (
    Path(__file__).resolve().parents[2] / "scrollmapper-data" / "sources_backup"
    / "extras" / "cross_references.txt"
)

pytestmark = pytest.mark.integration


def _skip_if_missing() -> None:
    if not _XREF_FILE.exists():
        pytest.skip(f"Data file not found: {_XREF_FILE}")


class TestIntertextuality:
    def test_psalm_110_1_is_the_most_quoted_verse(self) -> None:
        # Psalm 110:1 ("The LORD said unto my Lord...") is the single
        # most-quoted OT verse in the NT — cited in Matthew, Mark
        # (twice), Luke, Acts, and Hebrews. Observed: 6 links at
        # min_votes=20, with Matthew 22:44 the top-voted (34).
        _skip_if_missing()
        df = intertextuality('Psa', chapter=110, min_votes=20, include_kjv=False)
        assert len(df) >= 5
        assert (df['ot_ref'] == 'Psalms 110:1').any()
        top = df.iloc[0]
        assert top['nt_ref'] == 'Matthew 22:44'
        assert top['votes'] >= 30


class TestPrintIntertextuality:
    def test_prints_real_output(self, capsys) -> None:
        _skip_if_missing()
        print_intertextuality('Psa', chapter=110, min_votes=20)
        out = capsys.readouterr().out
        assert 'Psalms 110' in out
        assert 'Matthew 22:44' in out
        assert 'Hebrews' in out

    def test_empty_result_prints_a_clear_message(self, capsys) -> None:
        # An absurdly high min_votes threshold should print the "no
        # citations found" fallback rather than crash on an empty df.
        _skip_if_missing()
        print_intertextuality('Psa', chapter=110, min_votes=100000)
        out = capsys.readouterr().out
        assert 'No citations found' in out


class TestIntertextualityGraph:
    def test_produces_a_real_png(self, tmp_path: Path) -> None:
        _skip_if_missing()
        out = intertextuality_graph(
            'Psa', chapter=110, min_votes=20, output_path=str(tmp_path / 'net.png'))
        assert Path(out).exists()
        assert Path(out).stat().st_size > 0

    def test_empty_result_still_produces_a_placeholder_png(self, tmp_path: Path) -> None:
        _skip_if_missing()
        out = intertextuality_graph(
            'Psa', chapter=110, min_votes=100000, output_path=str(tmp_path / 'empty.png'))
        assert Path(out).exists()
        assert Path(out).stat().st_size > 0


class TestIntertextualityReport:
    def test_writes_a_real_markdown_report_with_chart_and_csv(self, tmp_path: Path) -> None:
        _skip_if_missing()
        out = intertextuality_report(
            'Psa', chapter=110, min_votes=20, output_dir=str(tmp_path))
        assert Path(out).exists()
        text = Path(out).read_text(encoding='utf-8')
        assert 'Psalms 110' in text
        assert 'Matthew 22:44' in text
        csv_files = list(tmp_path.glob('*.csv'))
        png_files = list(tmp_path.glob('*.png'))
        assert len(csv_files) == 1
        assert len(png_files) == 1
