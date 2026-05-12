# Getting Started

## Prerequisites

- Python 3.11+
- Git (with submodule support)
- Jupyter Notebook or JupyterLab

## Installation

```bash
# 1. Clone the repository with all submodules
git clone --recurse-submodules https://github.com/dnovick/berean-bible-bots.git
cd berean-bible-bots

# 2. One-command setup (virtual environment + dependencies + Jupyter kernel)
bash setup.sh          # Mac / Linux
# setup.bat            # Windows

# 3. Build the processed data cache (one-time, ~5–30 seconds)
source .venv/bin/activate     # Mac / Linux  (.venv\Scripts\activate on Windows)
python scripts/build_db.py

# 4. (Optional) Build the IBM Model 1 word alignment (~30 seconds)
python scripts/build_word_alignment.py
```

If you cloned without `--recurse-submodules`:

```bash
git submodule update --init --recursive
```

For notebook usage in VS Code, see [notebooks/SETUP.md](../notebooks/SETUP.md).

### Using notebooks without VS Code

If you prefer the classic Jupyter interface in a browser:

```bash
source .venv/bin/activate
jupyter lab notebooks/
```
