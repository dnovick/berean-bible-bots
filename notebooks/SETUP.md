# Notebook Setup Guide

**Prerequisites:** Python 3.11 or later and VS Code must be installed.
- Python: https://www.python.org/downloads/
- VS Code: https://code.visualstudio.com/

---

## Quick setup — one command

Open a terminal in the project root folder and run:

**Mac / Linux:**
```bash
bash setup.sh
```

**Windows:**
```bat
setup.bat
```

The script creates the virtual environment, installs all dependencies, and
registers the Jupyter kernel. It takes 2–5 minutes on first run.

---

## After the script finishes

1. Open VS Code. If you haven't already, install the **Jupyter** extension
   (click the Extensions icon in the left sidebar, search "Jupyter", install
   the one published by Microsoft).

2. Open any notebook — for example `notebooks/ot/verbs/qal.ipynb`.

3. Click **Select Kernel** in the top-right corner of the notebook, choose
   **Jupyter Kernel**, then select **Berean Bible Bots**.

4. Click **Run All** (or press `Shift+Enter` to run cells one at a time).

The first cell loads the MACULA data and may take 10–20 seconds. Subsequent
cells run much faster.

---

## Opening a new terminal later

VS Code auto-activates the `.venv` when it detects it in the workspace root.
If you open a standalone terminal outside VS Code, re-activate manually:

**Mac / Linux:**
```bash
source .venv/bin/activate
```

**Windows:**
```bat
.venv\Scripts\activate
```

---

## What the script does (for reference)

| Step | Command |
|---|---|
| Create virtual environment | `python3 -m venv .venv` |
| Activate | `source .venv/bin/activate` |
| Install dependencies | `pip install -r requirements-notebooks.txt` |
| Register Jupyter kernel | `python -m ipykernel install --user --name berean-bible-bots --display-name "Berean Bible Bots"` |

Running the script again is safe — it skips the venv creation if `.venv`
already exists and re-installs/upgrades packages as needed.

---

## Troubleshooting

**"Python 3.11 or later is required" error:**
Install Python 3.11+ from https://www.python.org/downloads/ and re-run
the script.

**The kernel "Berean Bible Bots" doesn't appear in the kernel picker:**
Make sure the script completed without errors. Click the kernel picker
again — VS Code may need a moment to refresh. If it still doesn't appear,
reload VS Code (`Cmd+Shift+P` → "Reload Window").

**"Module not found" error when running a cell:**
You selected a different kernel. Click the kernel name in the top-right
corner and switch to **Berean Bible Bots**.

**Text-Fabric data download prompt on first run:**
Some notebooks use MACULA Hebrew/Greek data via Text-Fabric. On first use
it will ask to download the dataset (~200 MB). Follow the prompt — it only
downloads once and caches locally.

---

## Notebook index

See [README.md](README.md) for a full table of all notebooks and what each
one covers.
