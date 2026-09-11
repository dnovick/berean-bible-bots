"""Tests for scripts/build_mkdocs.py's pure helpers and build_reports().
Per docs/policies/test-coverage.md's priority plan (issue #676, Phase 2).

build_reports() (not build_mkdocs.py's main()) is the safe, narrow entry
point already used by review-pr.yml's CI step and documented there: it
only writes mkdocs_src/reports/ (gitignored) from output/reports/, and
never touches mkdocs_nav.yml — unlike main(), which also clears and
rebuilds the Courses nav section and unconditionally wipes the
hand-maintained Standards & Policies section. Requires output/reports/
to exist (built by the various scripts/build_*_report.py scripts).
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

import build_mkdocs as bm  # noqa: E402

_REPO = Path(__file__).resolve().parents[2]
_OUTPUT_REPORTS = _REPO / "output" / "reports"
_MKDOCS_SRC_REPORTS = _REPO / "mkdocs_src" / "reports"


class TestRewriteChartPaths:
    def test_rewrites_relative_prefix_to_given_depth(self) -> None:
        content = "![chart](../../../charts/nt/verbs/foo.png)"
        result = bm._rewrite_chart_paths(content, depth=2)
        assert result == "![chart](../../charts/nt/verbs/foo.png)"

    def test_leaves_unrelated_paths_alone(self) -> None:
        content = "See [here](../../other/page.md) for details."
        assert bm._rewrite_chart_paths(content, depth=1) == content


class TestMdTitle:
    def test_extracts_first_h1_heading(self, tmp_path: Path) -> None:
        md = tmp_path / "report.md"
        md.write_text("# Hiphil Verb Density in Proverbs\n\nBody.\n")
        assert bm._md_title(md) == "Hiphil Verb Density in Proverbs"

    def test_falls_back_to_filename_when_no_heading(self, tmp_path: Path) -> None:
        md = tmp_path / "some-report.md"
        md.write_text("No heading.\n")
        assert bm._md_title(md) == "Some Report"


@pytest.mark.integration
class TestBuildReportsBehavioral:
    def test_produces_a_real_nav_tree_and_index_files(self) -> None:
        if not _OUTPUT_REPORTS.exists() or not any(_OUTPUT_REPORTS.iterdir()):
            pytest.skip(f"No built reports found: {_OUTPUT_REPORTS}")
        result = bm.build_reports()
        assert len(result) == 1
        top = result[0]
        assert "Reports" in top
        # Every real category this project ships reports under.
        section_names = [
            next(iter(entry)) for entry in top["Reports"] if isinstance(entry, dict)
        ]
        assert "Old Testament (Hebrew)" in section_names
        assert "New Testament (Greek)" in section_names
        assert (_MKDOCS_SRC_REPORTS / "index.md").exists()
