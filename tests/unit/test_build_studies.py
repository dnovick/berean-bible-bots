"""Tests for scripts/build_studies.py's nav-block builder and the
sentinel-based nav updater. Per docs/policies/test-coverage.md's priority
plan (issue #676, Phase 2). _update_nav() is tested against a tmp copy of
mkdocs_nav.yml (via monkeypatching _NAV_PATH), never the real tracked file.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

import build_studies as bs  # noqa: E402


class TestBuildPsalm119Nav:
    def test_includes_the_fixed_top_level_structure(self) -> None:
        nav = bs._build_psalm119_nav()
        assert nav.startswith("- Studies:\n")
        assert "  - Psalm 119:\n" in nav
        assert "studies/psalm-119/analysis/psalm-119-report.md" in nav
        assert "- The Armor of God — Ephesians 6:10–18:\n" in nav

    def test_only_lists_stanzas_whose_memorization_dir_exists(self, monkeypatch, tmp_path) -> None:
        # With no memorization directories at all, no per-stanza lines
        # should appear — just the fixed structure.
        monkeypatch.setattr(bs, "_MKDOCS_STUDIES", tmp_path)
        nav = bs._build_psalm119_nav()
        assert "Alef" not in nav
        assert "- Studies:\n" in nav


class TestUpdateNav:
    def test_replaces_content_between_sentinels(self, tmp_path, monkeypatch) -> None:
        nav_file = tmp_path / "mkdocs_nav.yml"
        nav_file.write_text(
            "- Home: index.md\n"
            f"{bs.NAV_START}\n"
            "- Studies:\n  - Old: studies/old.md\n"
            f"{bs.NAV_END}\n"
            "- API Reference: reference/index.md\n"
        )
        monkeypatch.setattr(bs, "_NAV_PATH", nav_file)

        bs._update_nav("- Studies:\n  - New: studies/new.md\n")

        result = nav_file.read_text()
        assert "studies/new.md" in result
        assert "studies/old.md" not in result
        assert "- Home: index.md" in result
        assert "- API Reference: reference/index.md" in result

    def test_inserts_before_api_reference_when_sentinel_absent(self, tmp_path, monkeypatch) -> None:
        # Simulates the nav having just been rewritten by build_mkdocs.py,
        # which strips the sentinel markers along with everything else.
        nav_file = tmp_path / "mkdocs_nav.yml"
        nav_file.write_text(
            "- Home: index.md\n"
            "- API Reference: reference/index.md\n"
        )
        monkeypatch.setattr(bs, "_NAV_PATH", nav_file)

        bs._update_nav("- Studies:\n  - New: studies/new.md\n")

        result = nav_file.read_text()
        assert result.index("studies/new.md") < result.index("API Reference")
        assert bs.NAV_START in result
        assert bs.NAV_END in result
