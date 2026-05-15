# Lesson Packages

Complete lesson packages for all chapters of *Basics of Biblical Hebrew* (Pratico & Van Pelt),
*Basics of Biblical Greek* (Mounce, 4th ed.), and *Basics of Biblical Aramaic* (Van Pelt)
are in [`output/lessons/`](../output/lessons/README.md).
Each chapter contains a full lesson in `README.md`, paradigm reference files (where applicable),
Anki and Flashcards Deluxe decks, and interactive exercises.

| Textbook | Chapters | Index |
|---|---|---|
| Basics of Biblical Hebrew (BBH) | Ch 1–35 | [output/lessons/hebrew/bbh/](../output/lessons/hebrew/bbh/README.md) |
| Basics of Biblical Greek (BBG) | Ch 1–36 | [output/lessons/greek/bbg/](../output/lessons/greek/bbg/README.md) |
| Basics of Biblical Aramaic (BBA) | Ch 1–22 | [output/lessons/aramaic/bba/](../output/lessons/aramaic/bba/README.md) |

## Student Downloads

Pre-built zip packages for students who are not working directly in this repository.
Each zip includes all lessons (rendered as HTML), interactive and printable exercises,
flashcard decks, and relevant analysis charts. Everything opens in a web browser or
PDF viewer — no installation required beyond unzipping.

To regenerate: `python scripts/build_student_packs.py`

| Package | Contents | Output |
|---|---|---|
| **BBH.zip** | BBH Ch 1–35 · lessons · exercises · flashcards · OT charts | `output/student-packs/BBH.zip` |
| **BBG.zip** | BBG Ch 1–36 · lessons · exercises · flashcards · NT + cross-testament charts | `output/student-packs/BBG.zip` |
| **BBA.zip** | BBA Ch 1–22 · lessons · exercises · flashcards | `output/student-packs/BBA.zip` |

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
