"""Tests for scripts/validate_links.py — relative markdown link resolution.
Known-good/known-bad, per docs/policies/test-coverage.md's priority plan
(issue #662).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

import validate_links  # noqa: E402


class TestCheckFile:
    def test_resolving_link_is_not_flagged(self, tmp_path: Path, monkeypatch) -> None:
        monkeypatch.setattr(validate_links, "_REPO", tmp_path)
        (tmp_path / "target.md").write_text("# Target\n")
        source = tmp_path / "source.md"
        source.write_text("See [the target](target.md) for details.\n")

        errors: list[str] = []
        warnings: list[str] = []
        validate_links._check_file(source, errors, warnings)
        assert errors == []
        assert warnings == []

    def test_broken_link_is_flagged(self, tmp_path: Path, monkeypatch) -> None:
        monkeypatch.setattr(validate_links, "_REPO", tmp_path)
        source = tmp_path / "source.md"
        source.write_text("See [nowhere](does-not-exist.md) for details.\n")

        errors: list[str] = []
        warnings: list[str] = []
        validate_links._check_file(source, errors, warnings)
        assert errors == []
        assert len(warnings) == 1
        assert "does-not-exist.md" in warnings[0]
        assert "broken link" in warnings[0]

    def test_external_and_anchor_links_are_skipped(self, tmp_path: Path, monkeypatch) -> None:
        monkeypatch.setattr(validate_links, "_REPO", tmp_path)
        source = tmp_path / "source.md"
        source.write_text(
            "[External](https://example.com/page)\n"
            "[Anchor](#some-heading)\n"
            "[Site-absolute](/reference/index.md)\n"
        )
        errors: list[str] = []
        warnings: list[str] = []
        validate_links._check_file(source, errors, warnings)
        assert errors == []
        assert warnings == []
