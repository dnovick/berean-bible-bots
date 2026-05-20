"""Inject (or update) a Colab setup cell into every notebook.

The cell is inserted as the second cell (index 1), after the title/intro
markdown cell.  It is skipped entirely when not running in Colab, so local
execution is unaffected.

Run from the repo root:
    python scripts/inject_colab_setup.py
"""
import json
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = Path(__file__).resolve().parent.parent
NOTEBOOKS_DIR = REPO_ROOT / "notebooks"

# ── setup cell source ────────────────────────────────────────────────────────

SETUP_SOURCE = """\
# @title Colab setup (runs only on Google Colab)
import sys
IN_COLAB = "google.colab" in sys.modules
if IN_COLAB:
    import subprocess, os
    # Clone the repo so all source and data paths work
    if not os.path.isdir("/content/berean-bible-bots"):
        subprocess.run(
            ["git", "clone", "--depth", "1",
             "https://github.com/dnovick/berean-bible-bots.git",
             "/content/berean-bible-bots"],
            check=True,
        )
    os.chdir("/content/berean-bible-bots")
    sys.path.insert(0, "/content/berean-bible-bots/src")
    # Install Python dependencies
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "-q", "-r",
         "binder/requirements.txt"],
        check=True,
    )
    # Download processed data files (~295 MB, one-time)
    subprocess.run(["bash", "binder/postBuild"], check=True)
    print("Colab environment ready.")
"""

SETUP_CELL: Dict[str, Any] = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {"cellView": "form", "id": "colab-setup"},
    "outputs": [],
    "source": SETUP_SOURCE,
}

MARKER = "colab-setup"


def _has_setup_cell(cells: List[Dict[str, Any]]) -> int:
    """Return index of existing setup cell, or -1."""
    for i, cell in enumerate(cells):
        meta = cell.get("metadata", {})
        if meta.get("id") == MARKER:
            return i
    return -1


def process_notebook(path: Path) -> bool:
    """Insert or update the setup cell. Returns True if modified."""
    with path.open(encoding="utf-8") as f:
        nb = json.load(f)

    cells = nb.get("cells", [])
    idx = _has_setup_cell(cells)

    if idx >= 0:
        if cells[idx]["source"] == SETUP_SOURCE:
            return False
        cells[idx] = SETUP_CELL
        action = "updated"
    else:
        insert_at = 1 if cells and cells[0]["cell_type"] == "markdown" else 0
        cells.insert(insert_at, SETUP_CELL)
        action = "inserted"

    nb["cells"] = cells
    with path.open("w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(f"  {action}: {path.relative_to(REPO_ROOT)}")
    return True


def main() -> None:
    notebooks = sorted(
        p for p in NOTEBOOKS_DIR.rglob("*.ipynb")
        if ".ipynb_checkpoints" not in p.parts
    )
    modified = 0
    for nb_path in notebooks:
        if process_notebook(nb_path):
            modified += 1
    print(f"\nDone — {modified}/{len(notebooks)} notebooks updated.")


if __name__ == "__main__":
    main()
