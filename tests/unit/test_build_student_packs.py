"""Tests for scripts/build_student_packs.py's pure title-extraction
helpers. Per docs/policies/test-coverage.md's priority plan (issue #676,
Phase 2).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

import build_student_packs as bsp  # noqa: E402


class TestChapterTitle:
    def test_extracts_h1_from_readme(self, tmp_path: Path) -> None:
        readme = tmp_path / "README.md"
        readme.write_text("# BBH Chapter 26 — Hiphil Strong\n\nBody.\n")
        assert bsp._chapter_title(readme) == "BBH Chapter 26 — Hiphil Strong"

    def test_falls_back_to_parent_dir_name_when_no_h1(self, tmp_path: Path) -> None:
        ch_dir = tmp_path / "ch26"
        ch_dir.mkdir()
        readme = ch_dir / "README.md"
        readme.write_text("No heading here.\n")
        assert bsp._chapter_title(readme) == "ch26"


class TestTopic:
    def test_extracts_portion_after_em_dash(self) -> None:
        assert bsp._topic("BBH Chapter 26 — Hiphil Strong") == "Hiphil Strong"

    def test_no_em_dash_returns_full_title(self) -> None:
        assert bsp._topic("Untitled Chapter") == "Untitled Chapter"
