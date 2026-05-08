# CLAUDE.md

## Project
A project that generates and maintains statistics for Old Testament Hebrew/Aramaic and New Testament Greek grammatical constructs.

- For example, I want to be able to know how many niphal perfect verbs are in a particular book.
- I also want to be able to create charts that summarize the data.
- I want to be able to ask questions about the data and have results presented to me in a format I can share with others.

## Things to note
- I started doing this myself with Excel and my Bible software programs. However, it is very manual and time consuming.
- I use Logos and Accordance. Both are on my laptop. Unfortunately, although Logos provides good analysis tools, if results are too large, I can't get the data I need without a multi-step copy/paste into Excel.
- Thee are numerous online resources that you can consult.
- This project is in a git repository. As you write code, generate data, etc. I need you to keep the files organized and do periodic commits and pushes. 
- I will look to Claude to make incremental improvements, suggest new features, and implement them.

## BBH Chapter Map — Full Syllabus

| Chapter | Topic |
|---|---|
| Ch1 | Hebrew Alphabet |
| Ch2 | Hebrew Vowels |
| Ch3 | Syllabification and Pronunciation |
| Ch4 | Hebrew Nouns |
| Ch5 | Definite Article and Conjunction ו |
| Ch6 | Hebrew Prepositions |
| Ch7 | Hebrew Adjectives |
| Ch8 | Hebrew Pronouns |
| Ch9 | Hebrew Pronominal Suffixes |
| Ch10 | Hebrew Construct Chain |
| Ch11 | Hebrew Numbers |
| Ch12 | Introduction to Hebrew Verbs |
| Ch13 | Qal Perfect Strong Verbs |
| Ch14 | Qal Perfect Weak Verbs |
| Ch15 | Qal Imperfect Strong Verbs |
| Ch16 | Qal Imperfect Weak Verbs |
| Ch17 | Waw-Consecutive |
| Ch18 | Qal Imperative |
| Ch19 | Qal Pronominal Suffixes on Verbs |
| Ch20 | Qal Infinitive Construct |
| Ch21 | Qal Infinitive Absolute |
| Ch22 | Qal Participle |
| Ch23 | Sentence Syntax |
| Ch24 | Niphal Strong |
| Ch25 | Niphal Weak |
| Ch26 | Hiphil Strong |
| Ch27 | Hiphil Weak |
| Ch28 | Hophal Strong |
| Ch29 | Hophal Weak |
| Ch30 | Piel Strong |
| Ch31 | Piel Weak |
| Ch32 | Pual Strong |
| Ch33 | Pual Weak |
| Ch34 | Hithpael Strong |
| Ch35 | Hithpael Weak |

Always verify chapter number against this table before generating any lesson for Ch28 and above.

---

## BBG Chapter Map — Full Syllabus (Mounce, 4th Edition)

| Chapter | Topic |
|---|---|
| Ch1 | The Greek Language |
| Ch2 | Learning Greek |
| Ch3 | The Alphabet and Pronunciation |
| Ch4 | Punctuation and Syllabification |
| Ch5 | Introduction to English Nouns |
| Ch6 | Nominative and Accusative; Article |
| Ch7 | Genitive and Dative |
| Ch8 | Prepositions and εἰμί |
| Ch9 | Adjectives |
| Ch10 | Third Declension |
| Ch11 | First and Second Person Personal Pronouns |
| Ch12 | αὐτός |
| Ch13 | Demonstrative Pronouns/Adjectives |
| Ch14 | Relative Pronoun |
| Ch15 | Introduction to Verbs |
| Ch16 | Present Active Indicative |
| Ch17 | Contract Verbs |
| Ch18 | Present Middle/Passive Indicative |
| Ch19 | Future Active and Middle Indicative |
| Ch20 | Verbal Roots (Patterns 2–4) |
| Ch21 | Imperfect Indicative |
| Ch22 | Second Aorist Active and Middle Indicative |
| Ch23 | First Aorist Active and Middle Indicative |
| Ch24 | Aorist and Future Passive Indicative |
| Ch25 | Perfect Indicative |
| Ch26 | Introduction to Participles |
| Ch27 | Imperfective (Present) Adverbial Participles |
| Ch28 | Perfective (Aorist) Adverbial Participles |
| Ch29 | Adjectival Participles |
| Ch30 | Combinative (Perfect) Participles and Genitive Absolutes |
| Ch31 | Subjunctive |
| Ch32 | Infinitive |
| Ch33 | Imperative |
| Ch34 | Indicative of δίδωμι |
| Ch35 | Nonindicative of δίδωμι and Conditional Sentences |
| Ch36 | ἵστημι, τίθημι, δείκνυμι and Odds 'n Ends |

BBG lessons live under `output/lessons/greek/bbg/ch<N>/`.

---

## BBA Chapter Map — Full Syllabus (Basics of Biblical Aramaic)

### Aramaic Phonological System
| Chapter | Topic |
|---|---|
| Ch1 | Alphabet |
| Ch2 | Vowels |
| Ch3 | Syllabification |

### Aramaic Nominal System
| Chapter | Topic |
|---|---|
| Ch4 | Nouns: Absolute State |
| Ch5 | Nouns: Determined State |
| Ch6 | Nouns: Construct State |
| Ch7 | Conjunctions and Prepositions |
| Ch8 | Pronominal Suffixes |
| Ch9 | Pronouns |
| Ch10 | Adjectives and Numbers |
| Ch11 | Adverbs and Particles |

### Aramaic Verbal System: Peal
| Chapter | Topic |
|---|---|
| Ch12 | Introduction to Aramaic Verbs |
| Ch13 | Peal Perfect |
| Ch14 | Peal Imperfect |
| Ch15 | Peal Imperative |
| Ch16 | Peal Infinitive Construct |
| Ch17 | Peal Participle |

### Aramaic Verbal System: Derived Stems
| Chapter | Topic |
|---|---|
| Ch18 | The Peil, Hithpeel, and Ithpeel Stems |
| Ch19 | The Pael Stem |
| Ch20 | The Hithpaal and Ithpaal Stems |
| Ch21 | The Haphel Stem |
| Ch22 | The Aphel, Shaphel, and Hophal Stems |

Always verify chapter number against this table before generating any BBA lesson.

BBA lessons live under `output/lessons/aramaic/bba/ch<N>/`.

---

## Lesson Output Structure

Lessons live under `output/lessons/hebrew/bbh/ch<N>/`. Every chapter directory contains:

- **`README.md`** — the full lesson (no separate lesson `.md` file; README is the lesson)
- **Paradigm files** (e.g. `qal-perfect-paradigm.md`) — where applicable
- **Anki decks** — `ch<N>-morphology-deck.{md,txt,-fd.txt}` and `ch<N>-vocab-deck.{md,txt,-fd.txt}`
- **`exercises/`** — one subdirectory per exercise

Each exercise subdirectory (`exercises/<name>/`) contains exactly **three formats**:
- `<name>.md` — static reference copy with answer key at the bottom
- `<name>.html` — self-contained interactive HTML (fillable fields, ▶ Answer per row, Show All / Hide All / Clear All)
- `<name>.pdf` — AcroForm fillable PDF (generated by `src/bible_grammar/exercise_pdf.py`)
- `README.md` — exercise description, conjugation coverage table, files table

**Every exercise must always have all three formats.** Never create an exercise without generating the PDF.

---

## Exercise PDF Generation

All PDFs are generated by `src/bible_grammar/exercise_pdf.py`.

- **Ch24+ passage exercises** use the `PassageExercise` base class (Template Method pattern). Subclasses implement `_render_passages(show_answers: bool)`.
- **Ch1–Ch23 exercises** use plain `ExercisePDF` subclasses with `add_generic_table()` for arbitrary column layouts.
- Each exercise has a `build_ch<N>_<exercise>()` function that saves the PDF to the correct output path.
- All builders are called from the `if __name__ == '__main__':` block.
- To regenerate all PDFs: `python3 src/bible_grammar/exercise_pdf.py`

Key data classes: `VerbEntry` (6 fields: num, verb, conj, pgn, root, func), `PassageBlock` (ref, hebrew, english, watchout).

---

## Distractor Policy for Passage Exercises (Ch24+)

Every "Spot the [Stem]" passage exercise must include distractor verbs from ALL stems learned before the target chapter's stem (per the chapter order above). Students answer "[Stem]? Yes / No" for every numbered verb. Distractors should be drawn from real verbs in the same passage quotations where possible.

---

## HTML Exercise Format

The `.html` exercise file is self-contained (no external dependencies):
- `<input class="parse-field">` in every parse cell
- `▶ Answer` button per verb row — clicking reveals a green answer row; clicking again hides it
- Three global controls: **Show All Answers**, **Hide All Answers**, **Clear All Inputs**
- Hebrew text: `direction:rtl; unicode-bidi:embed` — never put a verse range and Hebrew on the same line (RTL reordering renders it backwards)
- `@media print` block hides buttons, makes inputs show as underlines
- All answers, styles, and scripts embedded inline
