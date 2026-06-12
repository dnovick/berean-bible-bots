# Lesson Packages

Complete lesson packages for all chapters of *Basics of Biblical Hebrew* (Pratico & Van Pelt),
*Basics of Biblical Greek* (Mounce, 4th ed.), and *Basics of Biblical Aramaic* (Van Pelt)
are in [`data/lessons/`](../data/lessons/).
Each chapter directory contains a full lesson in `README.md`, paradigm reference files (where applicable),
Anki and Flashcards Deluxe decks, and interactive exercises.

| Textbook | Chapters | Index |
|---|---|---|
| Basics of Biblical Hebrew (BBH) | Ch 1–35 | [data/lessons/bbh/](../data/lessons/bbh/README.md) |
| Basics of Biblical Greek (BBG) | Ch 1–36 | [data/lessons/bbg/](../data/lessons/bbg/README.md) |
| Basics of Biblical Aramaic (BBA) | Ch 1–22 | [data/lessons/bba/](../data/lessons/bba/README.md) |

## Exercise Formats

Every exercise ships in three formats:

| Format | Use |
|---|---|
| `.md` | Static reference copy — full answer key at the bottom |
| `.html` | Classroom use — fillable fields, per-verb ▶ Answer reveal, Show All / Hide All / Clear All controls; fully self-contained, opens with a double-click |
| `.pdf` | Print or tablet use — AcroForm text fields; answers always visible in the answer rows |

## Distractor Policy (BBH Ch24+)

The "Spot the [Stem]" passage exercises for derived stems (Ch24–Ch35) include distractor
verbs drawn from all previously-learned stems. Every numbered verb has a "[Stem]? Yes / No"
column, so students must actively discriminate the target stem from Qal, Niphal, Hiphil, etc.

## Generating PDFs

All PDFs are produced by `src/bible_grammar/exercise_pdf.py`. To regenerate all PDFs:

```bash
python3 src/bible_grammar/exercise_pdf.py
```

## Daily Grammar Nuggets

Short, focused grammar observations — one example per day highlighting a specific
grammatical form in a familiar OT or NT text. Designed for ongoing reinforcement
alongside textbook study.

| File | Topic |
|---|---|
| [output/nuggets/hiphil-strong-nuggets.md](../output/nuggets/hiphil-strong-nuggets.md) | Hiphil Strong verb — daily examples from Deuteronomy, Psalms, Proverbs |
