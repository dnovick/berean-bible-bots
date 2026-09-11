"""Tests for scripts/index_research_library.py's pure/tmp-fixture helpers.
Per docs/policies/test-coverage.md's priority plan (issue #676, Phase 2).
The chromadb/openai client code (_get_collection) needs real API
credentials and isn't tested here — only the manifest and chunking logic.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

import index_research_library as irl  # noqa: E402


class TestSha256:
    def test_returns_a_20_char_hex_digest(self, tmp_path: Path) -> None:
        f = tmp_path / "doc.pdf"
        f.write_bytes(b"some pdf content")
        digest = irl._sha256(f)
        assert len(digest) == 20
        assert all(c in "0123456789abcdef" for c in digest)

    def test_same_content_gives_same_digest(self, tmp_path: Path) -> None:
        f1 = tmp_path / "a.pdf"
        f2 = tmp_path / "b.pdf"
        f1.write_bytes(b"identical content")
        f2.write_bytes(b"identical content")
        assert irl._sha256(f1) == irl._sha256(f2)

    def test_different_content_gives_different_digest(self, tmp_path: Path) -> None:
        f1 = tmp_path / "a.pdf"
        f2 = tmp_path / "b.pdf"
        f1.write_bytes(b"content one")
        f2.write_bytes(b"content two")
        assert irl._sha256(f1) != irl._sha256(f2)


class TestChunkText:
    def test_splits_long_text_into_overlapping_chunks(self) -> None:
        # CHUNK_SIZE=900, CHUNK_OVERLAP=120 — observed: a 2000-char text
        # splits into 3 chunks of sizes [900, 900, 440].
        text = "x" * 2000
        chunks = irl._chunk_text(text)
        assert [len(c) for c in chunks] == [900, 900, 440]

    def test_empty_text_returns_no_chunks(self) -> None:
        assert irl._chunk_text("") == []

    def test_short_text_returns_single_unchanged_chunk(self) -> None:
        assert irl._chunk_text("short") == ["short"]


class TestManifest:
    def test_load_missing_manifest_returns_empty_dict(self, tmp_path: Path, monkeypatch) -> None:
        monkeypatch.setattr(irl, "_MANIFEST_PATH", tmp_path / "manifest.json")
        assert irl._load_manifest() == {}

    def test_save_then_load_roundtrips(self, tmp_path: Path, monkeypatch) -> None:
        monkeypatch.setattr(irl, "_MANIFEST_PATH", tmp_path / "manifest.json")
        data = {"doc.pdf": {"hash": "abc123", "chunks": 5}}
        irl._save_manifest(data)
        assert irl._load_manifest() == data
