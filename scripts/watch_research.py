#!/usr/bin/env python3
"""
Watch data/research/ for new PDFs and automatically run add_paper.py.

Usage
-----
    python scripts/watch_research.py           # interactive (prompts for metadata)
    python scripts/watch_research.py --yes     # auto-accept Claude-inferred metadata
    Ctrl-C to stop.

Install watchdog if needed:
    pip install watchdog
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
_RESEARCH_DIR = _REPO_ROOT / "data" / "research"
_SETTLE_SECONDS = 3   # wait after creation before processing (allow copy to finish)


def _process(pdf_path: Path, auto: bool) -> None:
    """Import and run add_paper.process_paper directly (same process)."""
    sys.path.insert(0, str(_REPO_ROOT / "scripts"))
    from add_paper import process_paper  # noqa: PLC0415
    process_paper(pdf_path, auto=auto)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Watch data/research/ for new PDFs and process them automatically.",
    )
    parser.add_argument(
        "--yes", "-y",
        action="store_true",
        help="Auto-accept Claude-inferred metadata without prompting",
    )
    args = parser.parse_args()

    try:
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler, FileCreatedEvent
    except ImportError:
        print("ERROR: watchdog not installed. Run: pip install watchdog", file=sys.stderr)
        sys.exit(1)

    auto = args.yes

    class _Handler(FileSystemEventHandler):
        def on_created(self, event: object) -> None:
            if not isinstance(event, FileCreatedEvent):
                return
            path = Path(getattr(event, "src_path", ""))
            if path.suffix.lower() != ".pdf":
                return
            print(f"\n[watch] New PDF detected: {path.name}")
            print(f"[watch] Waiting {_SETTLE_SECONDS}s for file to settle …")
            time.sleep(_SETTLE_SECONDS)
            if not path.exists():
                print("[watch] File disappeared — skipping.")
                return
            _process(path, auto=auto)

    observer = Observer()
    observer.schedule(_Handler(), str(_RESEARCH_DIR), recursive=False)
    observer.start()

    mode = "auto-accept" if auto else "interactive"
    print(f"[watch] Watching {_RESEARCH_DIR} for new PDFs … (mode: {mode})")
    print("[watch] Press Ctrl-C to stop.\n")

    try:
        while observer.is_alive():
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[watch] Stopping …")
    finally:
        observer.stop()
        observer.join()
        print("[watch] Done.")


if __name__ == "__main__":
    main()
