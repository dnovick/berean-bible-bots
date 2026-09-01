# Report Standards

This document specifies the required structure and conventions for all reports, charts, and word/phrase studies produced by this project.

## Contents

- [Build Script Requirement](#build-script-requirement)
- [Output Directory Layout](#output-directory-layout)
- [CSV Exports](#csv-exports)
- [README Indexes](#readme-indexes)
- [Long Report Structure](#long-report-structure)
- [Overview Page Registration](#overview-page-registration)
- [Notebooks](#notebooks)
- [Code Quality in Build Scripts](#code-quality-in-build-scripts)

---

## Build Script Requirement

Every report must have a reproducible build script. **Never produce a report file without a build script that generates it.**

| What | Where |
|---|---|
| Build script | `scripts/build_<term>_report.py` |
| Generated report | `mkdocs_src/reports/<corpus>/<category>/<term>/` |
| Generated charts | `mkdocs_src/reports/<corpus>/<category>/<term>/` or `charts/<corpus>/<category>/<term>/` |
| Generated CSVs | Same directory as the report |

Running the build script from repo root must regenerate all charts, CSVs, and the report `.md` file from scratch.

---

## Output Directory Layout

Every word/phrase study lives in its own named subdirectory — never flat in the parent category folder.

```
mkdocs_src/reports/
    both/
        word_studies/
            fasting/
                fasting_word_study.md
                fasting-ot-distribution.png
                fasting-nt-distribution.png
                fasting-data.csv
                README.md   ← index for this study
        index.md            ← corpus-level index
    ot/
        ...
    nt/
        ...
    index.md                ← top-level quick links
```

---

## CSV Exports

Every report build script must export the underlying data as CSV alongside the report. The CSV filename should match the report name:

```
fasting_word_study.md  →  fasting-data.csv   (or fasting_word_study.csv)
```

CSVs are the portable, tool-agnostic record of the data. They must be committed alongside the report.

---

## README Indexes

Every output directory (`reports/`, `charts/`, sub-categories) must have a `README.md` with:

- A brief description of what the directory contains
- A table of contents with links to all files/subdirectories

This is for non-technical users who browse the repository directly on GitHub.

---

## Long Report Structure

Any report with more than approximately five `##` sections must open with:

1. `## Contents` — a TOC with anchor links to every `##` section
2. `## Key Observations` — a brief executive summary of the most important findings

Both sections appear **before** the body sections.

```markdown
## Contents

- [Distribution by Book](#distribution-by-book)
- [Collocations](#collocations)
- ...

## Key Observations

- The term appears 58× in the OT, concentrated in Psalms (14×) and Isaiah (9×).
- ...

## Distribution by Book
...
```

---

## Overview Page Registration

When adding a new report, register it in **all three** of the following places (never just one or two):

1. **`mkdocs_src/reports/index.md`** — the top-level Quick Links list, under the appropriate section heading
2. **`mkdocs_src/reports/<corpus>/index.md`** — the corpus-level index table (e.g. `both/index.md`, `ot/index.md`, `nt/index.md`)
3. **`mkdocs_src/reports/<corpus>/<category>/index.md`** — the category index table (e.g. `both/word_studies/index.md`)

Also add an entry to `mkdocs_nav.yml` under the correct nav section.

---

## Notebooks

When adding a new feature or data source, update the relevant Jupyter notebook(s) to demonstrate the feature. Notebooks live in `notebooks/` and are the primary interactive exploration surface.

---

## Code Quality in Build Scripts

- **No lint directives in output strings.** Never place `# noqa`, `# type: ignore`, or any other tool comment inside a string literal that gets written to a file — they become literal text in the output. Instead, add the script to `per-file-ignores` in `setup.cfg` to suppress linter warnings on long string literals.
- All build scripts must pass `flake8` and `mypy` before commit.
