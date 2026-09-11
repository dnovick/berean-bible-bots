"""Tests for scripts/build_courses.py's pure formatting/slug helpers, plus a
real behavioral test of load_all_instances() against the actual
data/courses/ tree. Per docs/policies/test-coverage.md's priority plan
(issue #676, Phase 2).
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

import build_courses as bc  # noqa: E402

_COURSES_DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "courses"


class TestHeadingAnchor:
    def test_produces_mkdocs_compatible_slug(self) -> None:
        assert bc.heading_anchor("Hophal Strong Verbs (Ch28)") == "hophal-strong-verbs-ch28"

    def test_collapses_repeated_separators(self) -> None:
        assert bc.heading_anchor("Foo   Bar -- Baz") == "foo-bar-baz"


class TestContentSlug:
    def test_uses_file_stem_when_file_given(self) -> None:
        assert bc.content_slug({"file": "readings/ch1.md"}) == "ch1"

    def test_falls_back_to_heading_anchor(self) -> None:
        assert bc.content_slug({"heading": "Session Overview"}) == "session-overview"


class TestFormatDate:
    def test_formats_iso_date_string(self) -> None:
        assert bc.format_date("2026-01-15") == "Jan 15, 2026"

    def test_blank_value_is_empty_string(self) -> None:
        assert bc.format_date("") == ""
        assert bc.format_date(None) == ""

    def test_unparseable_value_passed_through(self) -> None:
        assert bc.format_date("not-a-date") == "not-a-date"


class TestChapterUrlAndLabel:
    # Real textbook key from data/courses/bbh/*/instance.yml — not the
    # short code 'bbh' (that's the derived instance_group() output, not
    # the _TEXTBOOK_META lookup key).
    _TB = "Basics of Biblical Hebrew"

    def test_chapter_url(self) -> None:
        assert bc.chapter_url(self._TB, 28) == "/lessons/hebrew/ch28/"

    def test_chapter_label_includes_topic_title(self) -> None:
        assert bc.chapter_label(self._TB, 28) == "BBH Ch28 — Hophal Strong"

    def test_chapter_link_md_empty_for_falsy_chapter(self) -> None:
        assert bc.chapter_link_md(self._TB, 0) == ""

    def test_instance_group_derives_short_code(self) -> None:
        assert bc.instance_group({"textbook": self._TB}) == "bbh"

    def test_unknown_textbook_group_is_other(self) -> None:
        assert bc.instance_group({"textbook": "Some Unknown Book"}) == "other"


class TestSessionHelpers:
    def test_session_slug_prefers_dir_over_number(self) -> None:
        assert bc.session_slug({"_dir": "session-05", "number": 5}) == "session-05"

    def test_session_slug_falls_back_to_number(self) -> None:
        assert bc.session_slug({"number": 7}) == "session-07"

    def test_session_filename(self) -> None:
        assert bc.session_filename({"_dir": "session-05"}) == "session-05.md"

    def test_session_title(self) -> None:
        assert bc.session_title({"number": 5, "focus": "Hophal Verbs"}) == "Session 5 — Hophal Verbs"


@pytest.mark.integration
class TestLoadAllInstancesBehavioral:
    def test_finds_both_real_bbh_instances(self) -> None:
        # Observed: 2 real course instances under data/courses/bbh/ —
        # bbh-2024.1 (37 sessions) and bbh-2026.1 (46 sessions).
        if not _COURSES_DATA_DIR.exists():
            pytest.skip(f"Data directory not found: {_COURSES_DATA_DIR}")
        courses = bc.load_all_instances()
        by_id = {c["id"]: c for c in courses}
        assert "bbh-2024.1" in by_id
        assert "bbh-2026.1" in by_id
        assert len(by_id["bbh-2024.1"]["sessions"]) >= 35
        assert len(by_id["bbh-2026.1"]["sessions"]) >= 44
