# Slash Command Cheat Sheet

One line per command — what it does and how to call it. For full API docs with
runnable code examples (not just the slash-command form), see
[docs/features.md](features.md). Each command's own `.claude/commands/<name>.md`
file has the fullest detail (multiple examples, output description).

## Cross-Corpus Query API

| Command | What it does | Usage |
|---|---|---|
| `/word-study` | Full profile for a Hebrew/Greek term — lexicon, frequency, morphology, LXX equivalents, example verses | `/word-study <term>` |
| `/semantic-profile` | Combined semantic profile for a root (lexicon + stats + morphology + collocations) | `/semantic-profile <strongs>` |
| `/collocations` | Words that significantly co-occur with a root (PMI + log-likelihood) | `/collocations <strongs> [window=5] [corpus=OT\|NT]` |
| `/phrase-search` | Search for a consecutive word sequence (Strong's, lemma, or `*` wildcard) | `/phrase-search <token1> <token2> [...] [in <book>] [corpus <OT\|NT\|LXX>]` |
| `/synonym` | Compare two or more near-synonym roots side by side | `/synonym <term1> <term2> [term3 ...]` |
| `/morph-chart` | Morphological form distribution across books — table + stacked bar chart | `/morph-chart <strongs>` |
| `/lxx-query` | Query the full LXX corpus (Rahlfs 1935, CenterBLC) | `/lxx-query <Strong's-or-lemma> [book_or_group]` |
| `/export` | Export any analysis as a styled HTML report and/or CSV | `/export <type> [args]` |

## Hebrew OT Analysis

| Command | What it does | Usage |
|---|---|---|
| `/verbal-syntax` | Verb form distribution, wayyiqtol chains, clause types, stem distribution, conditionals, relatives, discourse particles | `/verbal-syntax <command> [args]` |
| `/verb-prep` | Which preposition (if any) governs a verb's complement, vs. direct object, vs. none — clause-scoped, accepts a Hebrew root or Strong's number | `/verb-prep <Strong's or root> [stem] [book]` |
| `/hiphil` | Statistical/morphological analysis of the Hiphil (causative) stem | `/hiphil <command> [args]` |
| `/poetry` | Cola splitting, parallelism, chiasm detection, acrostic detection, meter | `/poetry <command> [args]` |
| `/role-search` | Find verbs by grammatical subject (MACULA `subjref` links) | `/role-search <Strong's> [corpus] [book...]` |
| `/object-search` | Find grammatical objects of verbs whose subject is a given entity | `/object-search <Strong's> [corpus] [book...]` |
| `/ot-speaker` | Speech-verb tokens by grammatical subject — who says what | `/ot-speaker <Strong's> [book...]` |

## Greek NT Analysis

| Command | What it does | Usage |
|---|---|---|
| `/domain-search` | Query the Greek NT by Louw-Nida semantic domain | `/domain-search <domain> [subject] [book...]` |

## LXX (Septuagint)

| Command | What it does | Usage |
|---|---|---|
| `/lxx-consistency` | How uniformly LXX translators render a Hebrew root across books | `/lxx-consistency <strongs> [strongs2 ...]` |

## Cross-Corpus and Thematic

| Command | What it does | Usage |
|---|---|---|
| `/divine-names` | Divine names and christological titles across OT/NT/LXX | `/divine-names [OT\|NT\|LXX\|all]` |
| `/christological-titles` | Frequency table of titles Jesus used for Himself in the Gospels | `/christological-titles [scope] [filter]` |
| `/genre-compare` | Morphological patterns across literary genres (narrative, poetry, prophecy, epistle) | `/genre-compare [OT\|NT\|all] [feature]` |
| `/intertextuality` | NT verses that quote or allude to a given OT verse/chapter/book | `/intertextuality <OT-ref> [min_votes]` |
| `/trajectory` | Trace a word OT → LXX → NT, showing continuity/drift | `/trajectory <Strong's> [report]` |
| `/term-map` | Theological term mapping: Hebrew root → LXX equivalent → NT counts | `/term-map [theme]` |

## Teaching Platform (BBH / BBG / BBA)

| Command | What it does | Usage |
|---|---|---|
| `/lesson` | Generate a complete lesson package for a chapter (README, exercises, decks) | `/lesson <language> <textbook> <chapter> <stem-or-topic>` |
| `/vocab` | Build Anki vocabulary decks for a chapter from a word list | `/vocab <language> <textbook> <chapter>` |
| `/nugget` | Generate one daily SMS-ready example sentence for the stem being studied | `/nugget <stem> [subtype]` |

## Workflow

| Command | What it does | Usage |
|---|---|---|
| `/lint` | Run flake8 + mypy on the source tree before committing | `/lint` |
