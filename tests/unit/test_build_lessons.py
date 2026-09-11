"""Tests for scripts/build_lessons.py's pure helpers and file-reading
functions (against tmp fixtures, not real repo content). Per
docs/policies/test-coverage.md's priority plan (issue #676, Phase 2).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

import build_lessons as bl  # noqa: E402


class TestSortedChapters:
    def test_sorts_numerically_not_lexicographically(self) -> None:
        # "ch10" must sort after "ch2", not before it (lexicographic sort
        # would put "ch10" second).
        assert bl.sorted_chapters({"ch2": "a", "ch10": "b", "ch1": "c"}) == ["ch1", "ch2", "ch10"]


class TestSlugify:
    def test_strips_chapter_prefix_and_title_cases(self) -> None:
        assert bl.slugify("ch26-hophal-strong-drill") == "Hophal Strong Drill"

    def test_no_chapter_prefix_still_title_cases(self) -> None:
        assert bl.slugify("passage-exercise") == "Passage Exercise"


class TestStripTags:
    def test_removes_html_tags_and_collapses_whitespace(self) -> None:
        assert bl._strip_tags("<p>Hello  <b>world</b></p>") == "Hello world"

    def test_plain_text_unchanged_except_whitespace(self) -> None:
        assert bl._strip_tags("already   plain") == "already plain"


class TestMdTitle:
    def test_extracts_first_h1_heading(self, tmp_path: Path) -> None:
        md = tmp_path / "ch26.md"
        md.write_text("# Chapter 26 — Hophal Strong\n\nBody text.\n")
        assert bl._md_title(md) == "Chapter 26 — Hophal Strong"

    def test_falls_back_to_filename_when_no_heading(self, tmp_path: Path) -> None:
        md = tmp_path / "some-file_name.md"
        md.write_text("No heading here.\n")
        assert bl._md_title(md) == "Some File Name"

    def test_falls_back_to_filename_when_file_missing(self, tmp_path: Path) -> None:
        assert bl._md_title(tmp_path / "missing-file.md") == "Missing File"


class TestReadChapterYml:
    def test_reads_real_yaml_file(self, tmp_path: Path, monkeypatch) -> None:
        monkeypatch.setattr(bl, "_LESSONS", tmp_path)
        ch_dir = tmp_path / "bbh" / "ch26"
        ch_dir.mkdir(parents=True)
        (ch_dir / "chapter.yml").write_text("chapter: 26\ntitle: Hophal Strong\n")

        data = bl._read_chapter_yml("bbh", "ch26")
        assert data == {"chapter": 26, "title": "Hophal Strong"}

    def test_missing_file_returns_empty_dict(self, tmp_path: Path, monkeypatch) -> None:
        monkeypatch.setattr(bl, "_LESSONS", tmp_path)
        assert bl._read_chapter_yml("bbh", "ch99") == {}


class TestReadmeDescription:
    def test_extracts_description_before_first_section_heading(self, tmp_path: Path) -> None:
        readme = tmp_path / "README.md"
        readme.write_text(
            "# Chapter 26\n\n"
            "*BBH — Hophal Strong*\n\n"
            "---\n\n"
            "## Description\n\n"
            "This chapter covers the Hophal strong verb paradigm.\n\n"
            "## Files\n\n"
            "Some file table.\n"
        )
        desc = bl._readme_description(readme)
        assert "Hophal strong verb paradigm" in desc
        assert "Files" not in desc

    def test_missing_file_returns_empty_string(self, tmp_path: Path) -> None:
        assert bl._readme_description(tmp_path / "missing.md") == ""
