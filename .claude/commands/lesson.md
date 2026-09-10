# Lesson Syllabus Prep

Generate a complete lesson package for a Biblical Hebrew (or Greek) grammar chapter.
Pulls frequency/morphology data from MACULA, writes structured Markdown to the correct
output path, and generates supporting files (paradigm reference, passage exercise, Anki deck).

**Usage:** `/lesson <language> <textbook> <chapter> <stem-or-topic>`

- `language` — `hebrew`, `greek`, or `aramaic`
- `textbook` — textbook abbreviation: `bbh` (Basics of Biblical Hebrew), `mounce`, etc.
- `chapter` — chapter number, e.g. `26`
- `stem-or-topic` — the grammatical topic, e.g. `"Hiphil Strong Verbs"`, `"Niphal"`, `"Piel"`

**Output paths (all files go in the same chapter directory):**
- `output/lessons/<language>/<textbook>/ch<N>/ch<N>-<slug>.md` — main lesson
- `output/lessons/<language>/<textbook>/ch<N>/<stem>-paradigms.md` — full paradigm tables
Each exercise gets its own named subdirectory under `exercises/`:
- `output/lessons/<language>/<textbook>/ch<N>/exercises/<exercise-name>/` — one directory per exercise
  - `<exercise-name>.md` — Markdown version with answer key
  - `<exercise-name>.html` — interactive HTML with fillable fields and inline answer reveal
  - `<exercise-name>.pdf` — fillable PDF with AcroForm text fields (generated via `exercise_pdf.py`)

Example: `exercises/ch26-passage-exercise/ch26-passage-exercise.{md,html,pdf}`
- `output/lessons/<language>/<textbook>/ch<N>/ch<N>-anki-deck.md` — morphology flashcard list
- `output/lessons/<language>/<textbook>/ch<N>/ch<N>-anki-deck.txt` — Anki import file (tab-separated)
- `output/lessons/<language>/<textbook>/ch<N>/README.md` — link index (main lesson listed first)

**Examples:**
- `/lesson hebrew bbh 26 "Hiphil Strong Verbs"`
- `/lesson hebrew bbh 27 "Hiphil Weak Verbs"`
- `/lesson hebrew bbh 14 "Niphal"`
- `/lesson hebrew bbh 15 "Piel and Pual"`

---

## What the lesson file must contain

### 1. Function (BBH §X.2 or equivalent)
A table with columns: **Function | Description | Example**.
Rows: Causative, Declarative, Factitive, Simple action, Denominative (mark *(not in BBH)* if absent from the textbook).
Include a "Key diagnostic" callout block.

### 2. Form — Diagnostic Markers
Bullet list of the prefix/vowel pattern for each conjugation:
Perfect, Imperfect, Wayyiqtol, Imperative, Infinitive Construct, Infinitive Absolute, Participle.

### 3. Paradigm Table
Links to the paradigm file sections. Columns: **Conjugation (linked) | 3ms Form | BBH § | Notes**.
- Conjugation name is a Markdown link: `[Perfect (qatal)](paradigm-file.md#perfect-qatal)`
- Use `—` for BBH § when no section exists (wayyiqtol, weqatal).
- Use GitHub auto-generated anchors (lowercase, spaces→hyphens, strip punctuation).

### 4. Real Forms Table — a single high-frequency root
Show Perfect, Wayyiqtol, Imperfect, Imperative, Participle for one well-known root (e.g. בּוֹא for Hiphil).
Include a note about weak-root behavior if applicable.

### 5. Most Common Lemmas (Torah / Pentateuch)
Query `hiphil_data()` (or the appropriate stem function) filtered to Genesis–Deuteronomy.
Table: **Root | Lemma | Torah (×) | Hiphil/Stem Meaning | Function Type**.
Top 15 lemmas minimum.

### 6. Example Passages
**One example per semantic function × conjugation form** (where the combination exists in the OT).
- Organize by function type with `### Causative`, `### Declarative`, `### Factitive`, `### Simple Action` subsections.
- Prefer Torah (Gen→Exo→Lev→Num→Deu); fall back to Psa/Pro/Job, then any OT book.
- Note explicitly when a function × form combination has zero OT attestations.
- Each entry format:
  ```
  **Conjugation — Ref** — Hebrew text
  *"English translation."*
  → Root Stem+conjugation+PGN; one sentence of grammatical/contextual explanation.
  ```

### 7. Conjugation Distribution (OT-wide)
Table: **Conjugation | Count | % of all [stem]**.
Pull from `hiphil_conjugation_profile()` or equivalent.
Include a teaching note callout about the most notable distribution patterns.

---

## Paradigm file structure

One section per conjugation with a full person/number/gender table plus a `> Key marker:` callout.
Use plain heading text (no `{#id}` tags) so GitHub auto-anchors work correctly.

Sections in order: Perfect (Qatal), Imperfect (Yiqtol), Wayyiqtol, Weqatal, Imperative, Infinitive Construct, Infinitive Absolute, Participle (Active/Passive as appropriate).

Close with a **Summary** table: Conjugation | Prefix | Final vowel | Quick ID.

---

## Passage exercise file structure

Always generate **all three formats** — `.md`, `.html`, and `.pdf` — for every exercise, without exception.

### HTML exercise format

The `.html` file is self-contained (no external dependencies) and is the primary classroom tool. Structure:

- `<input class="parse-field">` in every parse cell (Conjugation, PGN, Root, Function)
- A `▶ Answer` button on each verb row — clicking reveals a green `<tr class="answer-row">` inline with the correct parsing; clicking again hides it and toggles to `▼ Hide`
- Three global controls at the top: **Show All Answers**, **Hide All Answers**, **Clear All Inputs**
- Hebrew text in `<div class="hebrew">` with `direction:rtl; unicode-bidi:embed` — no bidi issues
- A `@media print` block that hides buttons and makes input fields show as underlines
- All answers, styles, and scripts are embedded inline — file opens with a double-click in any browser

Title: `Chapter N — "Spot the [Stem]" Passage Exercise`

- Select 3 contiguous OT passages rich in the target stem (prefer Torah, narrative + prophecy)
- Present 12–16 individual verbs for parsing, one table row per verb
- Each row: `# | Verb | Stem? (Y/N) | Conjugation | PGN | Root | Function`
- Include a complete answer key at the end
- Close with 3 reflection questions connecting grammar to theological/narrative significance

---

## Morphology Anki deck file structure

Two files: a human-readable `.md` and a tab-separated `.txt` import file.

**`.txt` file header directives (required for correct import):**
```
#separator:tab
#html:false
#notetype:Basic
#deck:BBH Chapter N — [Stem]
#tags column:3
```

**Card format:** `Hebrew form<TAB>root + conjugation + PGN + gloss + function<TAB>tags`

- 4 roots × 8 conjugations = 32 cards (adjust for roots with unattested forms)
- Choose roots that are high-frequency and cover all 4 semantic function types
- Tags: `<stem>-<conjugation>`, `<stem>-<function>`, `bbh-ch<N>`

---

## Data queries to run

**CRITICAL:** Use `df[df['stem'] == '<stem_name>']` to filter by stem — NOT `df['morph'].str.startswith('V<x>')`.
The `morph` column prefix filter returns 0 results; the `stem` column is the correct field.

**Book names use title case:** `Gen`, `Exo`, `Lev`, `Num`, `Deu` — NOT `GEN`, `EXO` etc.

```python
import sys
sys.path.insert(0, 'src')
import pandas as pd
from bible_grammar import hiphil_data, hiphil_conjugation_profile

# All tokens for the target stem — adapt import and function name per stem:
#   Hiphil:  from bible_grammar.hiphil import hiphil_data, hiphil_conjugation_profile
#   Niphal:  from bible_grammar.niphal import niphal_data, niphal_conjugation_profile
#   Piel:    from bible_grammar.piel   import piel_data,   piel_conjugation_profile
# (or filter the full DataFrame: df[df['stem'] == 'niphal'] etc.)
df = hiphil_data()

# Torah subset for lemma frequency table — book names MUST be title case
torah = ['Gen','Exo','Lev','Num','Deu']
torah_df = df[df['book'].isin(torah)]

# Conjugation morph code maps by stem:
# Hiphil:  Vhq=Perfect, Vhw=Wayyiqtol, Vhi=Imperfect, Vhp=Weqatal,
#          Vhv=Imperative, Vhc=Inf. Construct, Vha=Inf. Absolute, Vhrm=Participle
# Niphal:  VNq, VNw, VNi, VNp, VNv, VNc, VNa, VNrm
# Piel:    Vpq, Vpw, Vpi, Vpp, Vpv, Vpc, Vpa, Vprm
conj_map = {
    'Vhq': 'Perfect', 'Vhw': 'Wayyiqtol', 'Vhi': 'Imperfect',
    'Vhp': 'Weqatal',  'Vhv': 'Imperative', 'Vhc': 'Inf. Construct',
    'Vha': 'Inf. Absolute', 'Vhrm': 'Participle',
}

def morph_to_conj(m):
    for code, name in conj_map.items():
        if m.startswith(code): return name
    return None

df['conj'] = df['morph'].apply(morph_to_conj)

# Canonical book order for best-example selection (Torah-first)
canon = ['Gen','Exo','Lev','Num','Deu','Jos','Jdg','Rut','1Sa','2Sa',
         '1Ki','2Ki','1Ch','2Ch','Ezr','Neh','Est','Job','Psa','Pro',
         'Ecc','Sng','Isa','Jer','Lam','Ezk','Dan','Hos','Jol','Amo',
         'Oba','Jon','Mic','Nah','Hab','Zep','Hag','Zec','Mal']
book_pri = {b: i for i, b in enumerate(canon)}
df['book_pri'] = df['book'].map(book_pri).fillna(99)
```

---

## README structure

### Chapter-level README.md

Four sections in order, each with its own `## Heading` and table:

1. **Main Lesson** — single row: the primary `.md` lesson file
2. **Reference Files** — paradigm file(s) only
3. **Exercises** — one row per exercise; link target is the exercise's own `README.md`, not individual files:
   `| [exercises/ch26-foo/](exercises/ch26-foo/README.md) | one-line description |`
4. **Flashcards** — all Anki decks: morphology deck (.md + .txt + .csv if present) followed by vocab deck (.md + .txt)

Omit sections that have no files yet (e.g. no Flashcards section until deck files exist).

### Exercise-level README.md

Every exercise subdirectory (`exercises/<name>/`) must have its own `README.md` containing:
- `# "<Exercise Title>" — <subtitle>`
- `## Description` — 2–3 sentences on what the exercise covers, passages used, and what students parse
- `### Conjugation coverage` table (Conjugation | Count | Verbs)
- `## Files` table with three rows: `.md` / `.html` / `.pdf`, each with a one-line use description:
  - `.md` — "Reference copy — static answer key at bottom"
  - `.html` — "Classroom use — fillable fields, per-verb ▶ Answer reveal, Show/Hide/Clear All controls"
  - `.pdf` — "Print or tablet use — AcroForm text fields, answer rows always visible"

---

## After generating files

1. Verify all paradigm links resolve correctly (heading text → GitHub anchor slug).
2. Verify the README lists all files in the chapter directory.
3. Commit with message: `Add BBH Ch<N> lesson: <Topic>`.
4. Offer to commit and push.
