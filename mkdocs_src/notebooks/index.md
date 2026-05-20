# Notebooks

Interactive analysis notebooks covering the full `bible_grammar` toolkit — Hebrew OT, Greek NT, Septuagint, Peshitta, and Targumim.

Each notebook below is rendered statically with its outputs. Click the **Open in Colab** badge on any notebook page to run it interactively in Google Colab — no local installation required.

!!! tip "New to Jupyter or this project?"
    Start with the [**Getting Started**](tutorial/getting_started.ipynb) notebook —
    it walks through running cells, filtering the dataset, and generating charts,
    no prior Python experience needed.

## Running in Google Colab

Click the **Open in Colab** badge at the top of any notebook page. On first run, execute the **Colab setup** cell (cell 2), which will:

1. Clone the repository into `/content/berean-bible-bots`
2. Install Python dependencies from `binder/requirements.txt`
3. Download the processed data files (~295 MB) from `bereanbiblebots.com/data/`

Subsequent cells run normally once the setup cell completes (~2–3 minutes on first run; data is cached for the session).

## Running Locally

To execute notebooks on your own machine:

```bash
git clone https://github.com/dnovick/berean-bible-bots.git
cd berean-bible-bots
python -m venv .venv && source .venv/bin/activate
pip install -r binder/requirements.txt
# Download processed data (one-time, ~295 MB)
bash binder/postBuild
jupyter lab
```

Then open any notebook from the `notebooks/` directory.
