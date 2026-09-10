"""Behavioral tests for bible_grammar.exercise_pdf — the PDF generation
package that produces the actual downloadable exercise files students use.
Per docs/policies/test-coverage.md's priority plan (issue #662): this was
the highest-stakes zero-coverage gap in the codebase.

PDF generation depends on macOS system fonts (_register_fonts() in
exercise_pdf/_base.py hardcodes '/System/Library/Fonts/ArialHB.ttc', with no
fallback for other platforms) and on reportlab, which is deliberately not
installed in CI (see review-pr.yml's install-step comment) since it's a
heavy, platform-coupled dependency. Marked integration so it's skipped
wherever that environment isn't available, same as the data/processed/
guard used elsewhere.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

pytestmark = pytest.mark.integration

_MACOS_HEBREW_FONT = Path("/System/Library/Fonts/ArialHB.ttc")

try:
    import reportlab  # noqa: F401
    _REPORTLAB_AVAILABLE = True
except ImportError:
    _REPORTLAB_AVAILABLE = False


def _skip_if_missing() -> None:
    if not _REPORTLAB_AVAILABLE:
        pytest.skip("reportlab not installed")
    if not _MACOS_HEBREW_FONT.exists():
        pytest.skip(f"Required font not found: {_MACOS_HEBREW_FONT} (macOS only)")


def _assert_real_pdf(path: str, *, min_pages: int = 1, min_bytes: int = 5000) -> None:
    p = Path(path)
    assert p.exists(), f"builder did not produce a file at {path}"
    assert p.stat().st_size >= min_bytes, f"{path} is suspiciously small ({p.stat().st_size}B)"
    with open(p, "rb") as f:
        assert f.read(5) == b"%PDF-", f"{path} does not start with a PDF header"

    pymupdf = pytest.importorskip("pymupdf")
    doc = pymupdf.open(p)
    try:
        assert doc.page_count >= min_pages
    finally:
        doc.close()


class TestBBHExercisePDF:
    def test_ch1_letter_recognition_generates_a_real_pdf(self, tmp_path) -> None:
        _skip_if_missing()
        from bible_grammar.exercise_pdf.bbh import build_ch1_letter_recognition
        path = build_ch1_letter_recognition(out_dir=str(tmp_path))
        _assert_real_pdf(path)


class TestBBGExercisePDF:
    def test_ch3_alphabet_drill_generates_a_real_pdf(self, tmp_path) -> None:
        _skip_if_missing()
        from bible_grammar.exercise_pdf.bbg import build_bbg_ch3_alphabet_drill
        path = build_bbg_ch3_alphabet_drill(out_dir=str(tmp_path))
        _assert_real_pdf(path)


class TestBBAExercisePDF:
    def test_ch1_letter_recognition_generates_a_real_pdf(self, tmp_path) -> None:
        _skip_if_missing()
        from bible_grammar.exercise_pdf.bba import build_bba_ch1_letter_recognition
        path = build_bba_ch1_letter_recognition(out_dir=str(tmp_path))
        _assert_real_pdf(path)


class TestForceRebuildBehavior:
    def test_skips_regeneration_when_file_exists(self, tmp_path, monkeypatch) -> None:
        # _build_exercise_pdf's documented behavior: skip regeneration if the
        # file already exists and PDF_FORCE_REBUILD is not set — this is how
        # the batch rebuild in __main__.py avoids redoing all ~200 PDFs
        # every run. Verify the skip path actually returns the existing file
        # unchanged, not a silent no-op producing nothing.
        _skip_if_missing()
        monkeypatch.delenv("PDF_FORCE_REBUILD", raising=False)
        from bible_grammar.exercise_pdf.bbh import build_ch1_letter_recognition

        first_path = build_ch1_letter_recognition(out_dir=str(tmp_path))
        first_mtime = Path(first_path).stat().st_mtime_ns

        second_path = build_ch1_letter_recognition(out_dir=str(tmp_path))
        assert second_path == first_path
        assert Path(second_path).stat().st_mtime_ns == first_mtime
