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

BBG lessons live under `data/lessons/bbg/ch<N>/`.

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

BBA lessons live under `data/lessons/bba/ch<N>/`.

---

## Lesson Output Structure

Full specification: **[`mkdocs_src/standards/lessons.md`](mkdocs_src/standards/lessons.md)**

Key rules (always enforced):
- `README.md` **is** the lesson — no separate `lesson.md`
- Anki decks: `ch<N>-morphology-deck.{md,txt,-fd.txt}` and `ch<N>-vocab-deck.{md,txt,-fd.txt}`
- Exercises live in `exercises/<name>/` — see exercise standards below
- Use `scripts/new_session.py` to scaffold sessions — never hand-write `session.yml`
- Run `scripts/validate_courses.py` before committing course content changes
- No inline Vocabulary or Practice section on the lesson page itself — those live in the vocab Anki deck and `exercises.md`, respectively (see full spec)

## Exercise Standards

Full specification: **[`mkdocs_src/standards/exercises.md`](mkdocs_src/standards/exercises.md)**

Key rules (always enforced):
- **Every exercise must have all three formats:** `.md`, `.html`, `.pdf` — never create one without all three
- Stem, Conjugation, PGN, Yes/No, and Function fields use `<select>` dropdowns, not free-text inputs
- Every `.answer-row td` aligns cell-for-cell with table columns — no colspan, no bunched cells
- No verse range and Hebrew text on the same line in HTML (RTL reordering renders it backwards)
- Ch24+ "Spot the [Stem]" exercises include distractor verbs from all previously learned stems
- Regenerate all PDFs: `python3 src/bible_grammar/exercise_pdf.py`

---

## Autonomous Action Policy

Agent session behavior is governed by `mkdocs_src/policies/autonomous-actions.md`, which defines the Phase 1/2/3 trust matrix for this project (aligned with Foundry OA §6). Read it to understand which actions require owner approval (Phase 1) vs. proceed-then-review (Phase 2). Key points:

- **Phase 1 (always ask first):** PR creation, AI code review, PR merge, branch deletion, any action affecting billing/secrets/permissions.
- **Phase 2 (proceed, owner reviews after):** content file writes, script execution, git staging/commit/push on feature branches, branch creation, GitHub issue creation.
- **Permanently owner-only:** pushing to `main`, merging without both status checks green.

---

## Git Workflow

- **All changes go on a feature branch + PR.** Never push directly to main — branch protection is enabled.
- **Before every commit:** run `python -m flake8 src/` and `python -m mypy src/ --ignore-missing-imports`. Fix all errors before committing.
- **After non-trivial changes:** commit and push automatically — do not ask first.
- **GitHub issues:** always create with `--assignee dnovick`.

### Agent Commit Identity

Commits made by Claude or another agent must use the author bot identity so they appear as `bbb-author-01[bot]` on GitHub rather than David Novick:

```bash
# Get the --author string:
BOT_AUTHOR=$(python scripts/github_app_token.py --role author --git-author)

# Use it when committing:
git commit --author="$BOT_AUTHOR" -m "$(cat <<'EOF'
Commit message here.
EOF
)"
```

This works because GitHub maps the noreply email (`<installation-id>+<slug>[bot]@users.noreply.github.com`) to the App installation. Owner-made commits (outside agent sessions) use the default git config and correctly show as David Novick.

### PR Workflow (GitHub App identities)

PRs are created by `bbb-author-01[bot]` and reviewed by `bbb-reviewer-01[bot]`.

**Opening a PR:**
```bash
GH_TOKEN=$(python scripts/github_app_token.py --role author) \
  gh pr create --title "..." --body "..."
```

**Automated review:** The `.github/workflows/review-pr.yml` action runs automatically on every PR.
It runs validate_courses and validate_lessons. If all pass, `bbb-reviewer-01[bot]`
approves the PR. If any fail, it requests changes with details. The reviewer bot's approval is
informational — the actual merge gate is the **`review` required status check** (GitHub Apps on
personal repos cannot be granted collaborator status, so their reviews do not count toward
required-approval counts).

**AI code review (manual):** Run `scripts/ai_review.py` against the PR before merging.
It sends the diff to Claude Opus 5, checks nine project-specific rules, posts a review comment
via `bbb-reviewer-01[bot]`, and posts a `codex-review` commit status (success or failure).
Branch protection requires this status to be green before merging.
```bash
source .venv/bin/activate
env -u ANTHROPIC_API_KEY python scripts/ai_review.py --pr <n>                        # uses claude-opus-5 by default
env -u ANTHROPIC_API_KEY python scripts/ai_review.py --pr <n> --model claude-sonnet-5  # use a different model
```
Credentials: uses Anthropic SDK auto-discovery (Claude Code installation). Do NOT set `ANTHROPIC_API_KEY` if you have an identity-linked key — unset it with `env -u ANTHROPIC_API_KEY`.

**Merging** (after both `review` and `codex-review` status checks pass):
```bash
# When merging as an agent (squash commit shows as bbb-author-01[bot]):
GH_TOKEN=$(python scripts/github_app_token.py --role author) \
  gh pr merge <n> --squash
git checkout main && git pull
```
Do not use `--admin` — branch protection enforces `enforce_admins: true`.
Owner-initiated merges (from the GitHub UI or using the personal token) will show as David Novick, which is correct.

**Repo secrets** (set in GitHub → Settings → Secrets → Actions):
- `AUTHOR_01_APP_ID`, `AUTHOR_01_PRIVATE_KEY`, `AUTHOR_01_INSTALLATION_ID`
- `REVIEWER_01_APP_ID`, `REVIEWER_01_PRIVATE_KEY`, `REVIEWER_01_INSTALLATION_ID`

**Local setup required** (one-time, outside the repo):
- `~/.config/berean-bots/github-apps.json` — app IDs and installation IDs
- `~/.config/berean-bots/author-01-app.pem` — author app private key
- `~/.config/berean-bots/reviewer-01-app.pem` — reviewer app private key

See `scripts/github_app_token.py` for the config file format.

---

## Language and Display Standards

Full specification: **[`mkdocs_src/standards/language.md`](mkdocs_src/standards/language.md)**

Key rules (always enforced):
- **No transliterations** for Hebrew, Aramaic, or Greek in any output — except a brief illustrative English sound-alike when a lesson is specifically teaching a pronunciation concept (e.g. "the AY diphthong sounds like the *oy* in *boy*"), which is a pronunciation aid tied to one point, not a systematic transliteration column
- **Tables:** GitHub-Flavored Markdown — never ASCII art or terminal output
- **NT text:** Byzantine/TR (STEPBible TAGNT); KJV translation — label deviations inline
- **BBH names:** use exact Pratico & Van Pelt spellings (Alef, Bet, Ḥet, Pathach, Shewa, etc.)
- **Matplotlib bidi:** pass the entire mixed-direction string to `get_display()` — never split Hebrew out and concatenate

## Report Standards

Full specification: **[`mkdocs_src/standards/reports.md`](mkdocs_src/standards/reports.md)**

Key rules (always enforced):
- Every report needs a `scripts/build_<term>_report.py` — never produce output without a build script
- Every report script exports a CSV alongside the report
- Every word/phrase study gets its own named subdirectory, never flat in the parent folder
- Long reports (5+ `##` sections) open with `## Contents` TOC then `## Key Observations`
- New reports register in all three index pages + `mkdocs_nav.yml`
- Every output directory has a `README.md` index
