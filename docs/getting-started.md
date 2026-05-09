# Getting Started

## Prerequisites

- Python 3.11+
- Git (with submodule support)
- Jupyter Notebook or JupyterLab

## Installation

```bash
# 1. Clone the repository with all submodules
git clone --recurse-submodules <repo-url>
cd berean-bible-bots

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Build the processed database (one-time, ~5 seconds)
python scripts/build_db.py

# 4. (Optional) Build the IBM Model 1 word alignment (~30 seconds)
python -c "from bible_grammar.ibm_align import build_alignment; build_alignment()"

# 5. Launch Jupyter
jupyter notebook notebooks/
```

If you cloned without `--recurse-submodules`:

```bash
git submodule update --init --recursive
```
