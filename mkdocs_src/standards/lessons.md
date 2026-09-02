# Lesson Standards

This document specifies the required structure and conventions for all lesson content (BBH, BBG, BBA). See `CLAUDE.md` for the full chapter maps and chapter-numbering verification rules.

## Contents

- [Directory Layout](#directory-layout)
- [README.md — The Lesson File](#readmemd--the-lesson-file)
- [Paradigm Files](#paradigm-files)
- [Anki Decks](#anki-decks)
- [Exercises](#exercises)
- [Course and Session Management](#course-and-session-management)

---

## Directory Layout

```
data/lessons/
    bbh/ch<N>/          ← BBH (Hebrew) chapters
    bbg/ch<N>/          ← BBG (Greek) chapters
    bba/ch<N>/          ← BBA (Aramaic) chapters
```

Every chapter directory contains:

| File/Dir | Required | Notes |
|---|---|---|
| `README.md` | Yes | The full lesson text (see below) |
| `<stem>-paradigm.md` | Where applicable | e.g. `qal-perfect-paradigm.md` |
| `chapter.yml` | Yes | Must list every flashcard slug and exercise name actually present on disk — see below |
| `flashcards/morphology/` | Yes | Anki morphology deck — `ch<N>-morphology-deck.{md,txt,-fd.txt}` + `deck.yml` |
| `flashcards/vocab/` | When vocab is available | Anki vocab deck — `ch<N>-vocab-deck.{md,txt,-fd.txt}` + `deck.yml` |
| `exercises/` | Yes | One subdirectory per exercise |

---

## README.md — The Lesson File

The `README.md` **is** the lesson — there is no separate lesson `.md` file. The README contains:

1. Chapter title and overview
2. Learning objectives
3. Grammatical exposition with examples
4. Paradigm tables (may link to paradigm files)

Do not create a separate `lesson.md` alongside `README.md`. If a `lesson.md` exists from earlier work, its content should be merged into `README.md`.

**Never include an inline Vocabulary section on the lesson page itself.** Chapter vocabulary lives only in the vocab Anki deck (`ch<N>-vocab-deck.*`, linked from the lesson's Flashcard Decks resource) — duplicating it as a table on the lesson page is redundant and drifts out of sync with the deck.

**Never include an inline Practice section (a table of exercise links) on the lesson page itself.** Exercises already have their own listing at `exercises.md`, linked from the lesson's Exercises resource — duplicating the list on the lesson page is redundant.

---

## Paradigm Files

Paradigm files are standalone Markdown tables for a single grammatical paradigm (e.g. all Qal Perfect forms). Name them `<stem>-<conjugation>-paradigm.md`. The `README.md` links to them and may also embed abbreviated versions inline.

---

## Anki Decks

### Morphology decks

Cover grammatical forms introduced in the chapter. Each card front shows a Hebrew/Greek/Aramaic form; the back shows the full parse.

### Vocab decks

Cover vocabulary words assigned for the chapter. Each card front shows the word; the back shows gloss and parsing notes.

### File naming

| Format | Filename |
|---|---|
| Markdown (readable) | `ch<N>-morphology-deck.md` / `ch<N>-vocab-deck.md` |
| Plain text (Anki import) | `ch<N>-morphology-deck.txt` / `ch<N>-vocab-deck.txt` |
| FastDrill format | `ch<N>-morphology-deck-fd.txt` / `ch<N>-vocab-deck-fd.txt` |

### Registering a deck

Every deck lives in `flashcards/<slug>/` (e.g. `flashcards/morphology/`, `flashcards/vocab/`), and **every slug present on disk must also appear in `chapter.yml`'s `flashcards:` list.** `build_lessons.py` only builds declared slugs — a `flashcards:` list with one entry (e.g. just `vocab`) silently skips any other deck directory that exists on disk, even a fully-authored one, and it never appears on the built site. This exact bug shipped to production for ch34 and ch35: both had a complete, correct morphology deck sitting unbuilt for over a week because only `vocab` was declared.

`scripts/validate_lessons.py` warns when a `flashcards/<slug>/` directory has real deck content but isn't listed in `flashcards:` — treat that warning as a real bug, not noise. After adding or renaming a deck directory, always run `python scripts/validate_lessons.py` and confirm the deck actually appears under the built `mkdocs_src/lessons/<course>/ch<N>/flashcards/` before considering the work done.

---

## Exercises

See [`docs/standards/exercises.md`](exercises.md) for the full exercise specification. Every exercise lives in `exercises/<name>/` under the chapter directory and must have all three formats (`.md`, `.html`, `.pdf`).

---

## Course and Session Management

### Creating a new session

Always use `scripts/new_session.py` — never create `session.yml` files by hand:

```bash
python scripts/new_session.py <course-id> \
    --date YYYY-MM-DD --focus "Session topic" \
    [--session N] [--chapter N] [--instructor "Name"]
```

The script auto-numbers sessions from existing directories when `--session` is omitted. It refuses to overwrite an existing session.

### Session agenda items

Use `duration: "X min"` as a separate YAML field on each agenda item. Never embed the duration inside the title string.

### Content validation

Run before committing any course content changes:

```bash
python scripts/validate_courses.py          # errors fail; warnings do not
python scripts/validate_courses.py --strict # warnings also fail
```

**ERRORs** (break CI): missing `date`/`focus`, bad date format, chapter out of range, missing download files referenced in `files:`.

**WARNs** (do not break CI): section content files not yet written, exercise directory missing a standalone `.md`.
