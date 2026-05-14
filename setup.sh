#!/usr/bin/env bash
# One-command setup for Berean Bible Bots notebooks.
# Usage (from the project root): bash setup.sh
set -e

echo ""
echo "=== Berean Bible Bots — Notebook Setup ==="
echo ""

# ── 1. Locate Python 3.11+ ────────────────────────────────────────────────────
PYTHON=""
for candidate in python3 python3.14 python3.13 python3.12 python3.11; do
    if command -v "$candidate" &>/dev/null; then
        ver=$("$candidate" -c "import sys; print(sys.version_info >= (3,11))" 2>/dev/null)
        if [ "$ver" = "True" ]; then
            PYTHON="$candidate"
            break
        fi
    fi
done

if [ -z "$PYTHON" ]; then
    echo "ERROR: Python 3.11 or later is required but was not found."
    echo "Download it from https://www.python.org/downloads/ and re-run this script."
    exit 1
fi

echo "Using $($PYTHON --version)"

# ── 2. Create virtual environment ─────────────────────────────────────────────
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment (.venv)..."
    "$PYTHON" -m venv .venv
else
    echo "Virtual environment already exists — skipping creation."
fi

# ── 3. Activate ───────────────────────────────────────────────────────────────
# shellcheck disable=SC1091
source .venv/bin/activate

echo "Virtual environment activated."

# ── 4. Upgrade pip silently ───────────────────────────────────────────────────
pip install --upgrade pip --quiet

# ── 5. Install dependencies ───────────────────────────────────────────────────
echo "Installing dependencies (this may take a few minutes the first time)..."
pip install -r requirements-notebooks.txt --quiet

# ── 6. Register Jupyter kernel ────────────────────────────────────────────────
echo "Registering Jupyter kernel..."
python -m ipykernel install --user \
    --name berean-bible-bots \
    --display-name "Berean Bible Bots"

# ── Done ──────────────────────────────────────────────────────────────────────
echo ""
echo "=== Setup complete! ==="
echo ""
echo "Next steps:"
echo "  1. Open VS Code and install the Jupyter extension if you haven't"
echo "     (search 'Jupyter' in the Extensions panel)."
echo "  2. Open any notebook in notebooks/ — e.g. notebooks/ot/verbs/qal.ipynb"
echo "  3. Click 'Select Kernel' (top-right) → Jupyter Kernel → Berean Bible Bots"
echo "  4. Click 'Run All'."
echo ""
echo "If you open a new terminal later, activate the venv first:"
echo "  source .venv/bin/activate"
echo ""
