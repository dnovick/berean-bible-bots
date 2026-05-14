# Features

## Contents

- [Query API](#query-api)
- [Word Study](#word-study)
- [Semantic Profile](#semantic-profile)
- [Concordance](#concordance)
- [Frequency Statistics](#frequency-statistics)
- [Book Profiles](#book-profiles)
- [Translation Equivalents (IBM Model 1)](#translation-equivalents-ibm-model-1)
- [Collocation Statistics](#collocation-statistics)
- [Morphological Distribution](#morphological-distribution)
- [LXX Translation Consistency](#lxx-translation-consistency)
- [NT Quotations](#nt-quotations)
- [NT Quotation Word Alignment](#nt-quotation-word-alignment)
- [Intertextuality Network](#intertextuality-network)
- [NT Greek Syntax (MACULA)](#nt-greek-syntax-macula)
- [OT Hebrew Syntax (MACULA)](#ot-hebrew-syntax-macula)
- [Speaker Attribution](#speaker-attribution)
- [Lexicon API](#lexicon-api)
- [Christological Titles](#christological-titles)
- [Syntactic Role Search](#syntactic-role-search)
- [Object / Argument Search](#object--argument-search)
- [LXX as a Queryable Corpus](#lxx-as-a-queryable-corpus)
- [OT Speaker Attribution](#ot-speaker-attribution)
- [Louw-Nida Domain Search](#louw-nida-domain-search)
- [Cross-Testament Trajectory](#cross-testament-trajectory)
- [Theological Term Reports](#theological-term-reports)
- [Hebrew Poetry Analysis](#hebrew-poetry-analysis)
- [Hebrew Verbal Syntax Analysis](#hebrew-verbal-syntax-analysis)
- [Theological Term Map](#theological-term-map)
- [Synonym Comparison](#synonym-comparison)
- [Phrase & Proximity Search](#phrase--proximity-search)
- [Divine Names Analysis](#divine-names-analysis)
- [Genre Comparison](#genre-comparison)
- [Hapax Legomena](#hapax-legomena)
- [Parallel Passages](#parallel-passages)
- [HTML & CSV Export](#html--csv-export)
- [Charts](#charts)
- [Hiphil (הִפְעִיל) Verb Morphology](#hiphil-הפעיל-verb-morphology)
- [Hebrew Preposition Analysis](#hebrew-preposition-analysis)
- [Greek Preposition Analysis](#greek-preposition-analysis)
- [Derived Stem Verb Morphology](#derived-stem-verb-morphology)
- [OT Noun Morphology](#ot-noun-morphology)
- [OT Number Morphology](#ot-number-morphology)
- [NT Noun Morphology](#nt-noun-morphology)
- [NT Participle Analysis](#nt-participle-analysis)
- [NT Mood Usage](#nt-mood-usage)
- [NT Discourse Particles](#nt-discourse-particles)
- [Greek Demonstratives](#greek-demonstratives)
- [NT Coreference & Anaphora](#nt-coreference--anaphora)
- [OT Participant Tracking](#ot-participant-tracking)
- [OT Predicate-Argument Structure](#ot-predicate-argument-structure)
- [OT Discourse Structure](#ot-discourse-structure)
- [Speech Act Classification](#speech-act-classification)
- [Information Structure](#information-structure)
- [Stylometrics & Register Analysis](#stylometrics--register-analysis)
- [Formulaic Language](#formulaic-language)
- [Biblical Aramaic Verb Morphology](#biblical-aramaic-verb-morphology)
- [Biblical Aramaic Nominal System](#biblical-aramaic-nominal-system)
- [Slash Commands (Claude Code Skills)](#slash-commands-claude-code-skills)

---

## Query API

The `query()` function is the core access point for morphological data.

```python
from bible_grammar import query

# Niphal perfect verbs in Genesis
query(book='Gen', stem='Niphal', conjugation='Perfect')

# All verbs in the Torah
query(book_group='torah', part_of_speech='Verb')

# Greek aorist passive indicatives in Paul's letters
query(book_group='pauline', tense='Aorist', voice='Passive', mood='Indicative')
```

**Available filters:** `source`, `book`, `testament`, `book_group` (torah/prophets/writings/
gospels/pauline/general), `chapter`, `verse`, `part_of_speech`, `stem`, `conjugation`,
`tense`, `voice`, `mood`, `person`, `number`, `gender`, `case_`, `state`

```python
from bible_grammar import translation_query

# KJV verses containing "grace" in Paul's letters
translation_query(translation='KJV', book_group='pauline', search='grace')

# Latin Vulgate — first chapter of Romans
translation_query(translation='VulgClementine', book='Rom', chapter=1)

# Syriac Peshitta NT — John 1
translation_query(translation='Peshitta', book='Jhn', chapter=1)
```

---

## Peshitta NT — Syriac Morphology

Word-level Syriac morphology for all 27 NT books via the ETCBC/syrnt dataset (Text-Fabric).
109,640 tokens with part of speech, gender, number, person, state, verbal stem, tense/aspect,
and Sedra transliterated root and lemma.

```python
from bible_grammar.peshitta_query import query_peshitta

df = query_peshitta()
# Filter by verbal stem (peal, pael, aphel, ethpeel, ethpaal, ettaphal)
peal_verbs = df[(df['sp'] == 'verb') & (df['vs'] == 'peal')]
# Search by Sedra root
write_root = df[df['root_sedra'] == 'CTB']   # CTB = write
```

Notebook: `notebooks/nt/peshitta/peshitta_morphology.ipynb`

---

## Targumim — Aramaic OT Translations

Verse-level Aramaic text for the major Targumim, downloaded from Sefaria.

| Targum | Books |
|---|---|
| Onkelos | Gen, Exo, Lev, Num, Deu |
| Jonathan | Jos, Jdg, Isa, Jer, Ezk, Hos, Amo, Mic, Nah, Hab, Zec |
| Psalms | Psa |

**Setup:** `python scripts/fetch_targum_data.py` (one-time download, ~14,000 verses)

```python
from bible_grammar.targum_query import load_targum

# All targumim
tg = load_targum()
# Filter
onkelos = load_targum(targum='Onkelos')
tj_isa = load_targum(targum='Jonathan', book_id='Isa')
# Search for Memra (divine word hypostasis)
memra = tg[tg['text'].str.contains('מֵימְרָא')]
```

Notebook: `notebooks/ot/targumim/targumim_overview.ipynb`

---

## Word Study

Complete lexical and statistical profile for any Hebrew or Greek word.

```python
from bible_grammar import word_study, print_word_study

# Full word study dict
ws = word_study('H7307')   # רוּחַ spirit/wind
ws = word_study('G3056')   # λόγος word

# Formatted report to stdout
print_word_study('H1254')  # בָּרָא to create
print_word_study('G4160')  # ποιέω to do/make
```

Each study includes: lemma, transliteration, gloss, definition, total occurrences,
distribution by book, morphological forms breakdown, LXX translation equivalents
(Hebrew only, word-level IBM Model 1 alignment), and the OT→LXX→NT trajectory.

Lemmas can be resolved to Strong's numbers by name:

```python
from bible_grammar import resolve_strongs

resolve_strongs('שָׁלוֹם')   # → 'H7965'
resolve_strongs('λόγος')    # → 'G3056'
```

---

## Semantic Profile

A unified full-profile report combining lexicon entry, frequency, morphology, LXX equivalents,
collocations, and example verses into a single analysis.

```python
from bible_grammar import semantic_profile, print_semantic_profile, save_semantic_profile

# Terminal report
print_semantic_profile('H7965')   # שָׁלוֹם peace
print_semantic_profile('G3056')   # λόγος word

# Save as Markdown + PNG chart (OT → output/reports/ot/lexicon/, NT → output/reports/nt/lexicon/)
save_semantic_profile('H1285')    # בְּרִית covenant
save_semantic_profile('H7307')    # רוּחַ spirit/wind
```

Pre-generated profiles: בְּרִית, רוּחַ, שָׁלוֹם in `output/reports/ot/lexicon/`; λόγος in `output/reports/nt/lexicon/`.

---

## Concordance

```python
from bible_grammar import concordance, lemma_frequency, top_lemmas

# All occurrences of H7307 with KJV context
concordance(strongs='H7307', context='KJV')

# Frequency table for all lemmas in Psalms
lemma_frequency(book='Psa', corpus='OT')

# Top 20 lemmas in Romans
top_lemmas(book='Rom', n=20)
```

---

## Frequency Statistics

```python
from bible_grammar import freq_table
from bible_grammar import query

df = query(book_group='torah', part_of_speech='Verb')
freq_table(df, 'stem')           # Count by binyan (Qal, Piel, Niphal…)
freq_table(df, ['stem', 'book_id'])  # Cross-tab
```

---

## Book Profiles

Morphological fingerprint for any OT or NT book.

```python
from bible_grammar import book_profile, print_profile, batch_profiles

print_profile('Gen')   # Genesis: verb stems, top lemmas, morph breakdown
print_profile('Rom')   # Romans: tense/voice/mood distribution

# Compare multiple books
batch_profiles(['Gen', 'Exo', 'Lev', 'Num', 'Deu'])
```

---

## Translation Equivalents (IBM Model 1)

Statistical word-level alignment between the Hebrew OT and the LXX, trained using
IBM Model 1. Answers: *which Greek word does the LXX use to translate this Hebrew root?*

```python
from bible_grammar import translation_equivalents_w, hebrew_sources_w

# Top Greek renderings for H1285 (בְּרִית covenant)
translation_equivalents_w(heb_strongs='H1285')

# Top Hebrew sources for G1242 (διαθήκη covenant)
hebrew_sources_w(lxx_strongs='G1242')
```

---

## Collocation Statistics

Identifies words that co-occur with a target root significantly more than chance, scored
by Pointwise Mutual Information (PMI) and log-likelihood ratio (G²).

```python
from bible_grammar import collocations, print_collocations, collocation_network

# Top collocates of שָׁלוֹם (peace) in the OT
print_collocations('H7965', corpus='OT', window=5)

# Top collocates of εἰρήνη (peace) in the NT
print_collocations('G1515', corpus='NT', window=5)

# Heatmap comparing collocate overlap for multiple roots
collocation_network(['H7965', 'H2617', 'H6666'], output_path='output/charts/ot/lexicon/peace-network.png')
```

---

## Morphological Distribution

Per-book distribution of morphological forms for any root — Hebrew stem × conjugation,
Greek tense × voice, or Greek case.

```python
from bible_grammar import morph_distribution, print_morph_distribution, morph_chart

# OT verb — stem breakdown across books
print_morph_distribution('H1696')    # דָּבַר to speak
morph_chart('H1696', chart_type='stacked_bar',
            output_path='output/charts/ot/lexicon/dabar-stems.png')

# NT verb — tense × voice per book
morph_chart('G3004', chart_type='heatmap',
            output_path='output/charts/nt/lexicon/lego-tense.png')
```

---

## LXX Translation Consistency

Measures how uniformly each LXX book/translator renders a given Hebrew root.
High consistency (>90%) means one dominant Greek equivalent; low consistency or
divergent books may indicate semantic range, translation philosophy differences,
or recensional variation.

```python
from bible_grammar import lxx_consistency, print_lxx_consistency
from bible_grammar import consistency_heatmap, batch_consistency

# Per-book rendering profile for רוּחַ (spirit/wind)
print_lxx_consistency('H7307')

# Heatmap: rows=LXX lemmas, cols=OT books, cells=% usage
consistency_heatmap('H7307', output_path='output/charts/ot/lexicon/ruach-consistency.png')

# Batch summary across multiple roots
batch_consistency(['H7307', 'H1697', 'H2617', 'H6944'])
```

The `batch_consistency()` result across the full theological terms list shows:
- **100% consistent:** בְּרִית (covenant), שָׁלוֹם (peace), קֹדֶשׁ (holiness), חֶסֶד (lovingkindness)
- **Most divergent:** דָּבָר (word, 9 divergent books), מִשְׁפָּט (justice, 8 books), שׁוּב (return, 6 books)

---

## NT Quotations

Cross-reference database linking NT verses to their OT sources (scrollmapper,
vote-weighted confidence scores).

```python
from bible_grammar import nt_quotations, verse_comparison, quotation_table

# All NT quotations of Isaiah
nt_quotations(ot_book='Isa', min_votes=50)

# All OT quotations in Hebrews
nt_quotations(nt_book='Heb', min_votes=30)

# Side-by-side verse text comparison
verse_comparison(nt_book='Mat', nt_chapter=4, nt_verse=4)
```

---

## NT Quotation Word Alignment

For each NT→OT quotation, analyses whether the NT author's Greek vocabulary follows
the LXX wording or diverges toward the Hebrew MT. Per-word verdicts:

| Verdict | Meaning |
|---|---|
| `LXX` | NT word's Strong's number appears in the LXX rendering of the OT verse |
| `LXX+MT` | Matches LXX and the Hebrew root is also present in the OT verse |
| `MT-diverge` | NT word's Hebrew root is in the OT verse but the LXX used a different Greek word |
| `neutral` | Function word or no alignment data |

```python
from bible_grammar import quotation_align, print_quotation_align, batch_align

# Word-level analysis for a single NT verse
print_quotation_align('Mat', 4, 4)   # Deut 8:3 — "man shall not live by bread alone"

# Batch summary across all high-confidence quotations in Hebrews
df = batch_align(nt_book='Heb', min_votes=50)
```

---

## Intertextuality Network

Given any OT verse, chapter, or book, finds all NT verses that quote or allude to it,
scored by community vote confidence (scrollmapper / OpenBible.info). Produces a bipartite
network graph (OT verses on the left, NT books/verses on the right) and a full report.

```python
from bible_grammar import intertextuality, print_intertextuality
from bible_grammar import intertextuality_graph, intertextuality_report

# Chapter scope — Isaiah 53 → all NT citations
print_intertextuality('Isa', chapter=53, min_votes=20)

# Single verse — Psalm 22:1 ("My God, my God…")
print_intertextuality('Psa', chapter=22, verse=1, min_votes=15)

# Full book — all Isaiah links at high confidence
print_intertextuality('Isa', min_votes=50)

# Network graph PNG
intertextuality_graph('Isa', chapter=53, min_votes=20,
                      output_path='output/charts/both/intertextuality/isa53-network.png')

# Markdown report + CSV
intertextuality_report('Psa', chapter=22)
```

Vote scores reflect how many independent scholars have identified the connection;
scores ≥50 are strong explicit quotations, 20–49 are probable allusions, 10–19 are
possible echoes. Pre-generated reports for Isaiah 53, Psalm 22, and full Isaiah
are in `output/reports/both/intertextuality/`.

---

## NT Greek Syntax (MACULA)

`syntax.py` wraps the MACULA Greek Nestle1904 data (137,779 word tokens) with a
query API that exposes syntactic roles, participant referents, English glosses,
and Louw-Nida semantic domains. Each word token carries a `subjref` attribute
pointing to the xml_id of its grammatical subject.

```python
from bible_grammar import load_syntax, query_syntax, speech_verbs

df = load_syntax()    # 137,779 rows; cached as Parquet after first load

# John 1:1 with roles and glosses
query_syntax(book='Jhn', chapter=1, verse=1)[
    ['text', 'lemma', 'role', 'gloss', 'case_', 'tense']
]

# All aorist passive verbs in Romans
query_syntax(book='Rom', tense='aorist', voice='passive')

# Speech verbs (λέγω, φημί, λαλέω…) where Jesus is the grammatical subject
speech_verbs('Mat', subject_strong='2424')

# All Gospel verses where Jesus is the speaking subject
from bible_grammar import jesus_speaking_verses
gospel_books = ['Mat', 'Mrk', 'Luk', 'Jhn']
speaking = jesus_speaking_verses(gospel_books)   # set of (book, ch, vs) tuples
```

Available filters: `book`, `chapter`, `verse`, `strong`, `lemma`, `role`,
`class_`, `tense`, `voice`, `mood`, `case_`, `person`, `number`, `gender`,
`has_subjref`, `has_referent`.

---

## OT Hebrew Syntax (MACULA)

`syntax_ot.py` wraps the MACULA Hebrew WLC data (475k word tokens, 930
per-chapter lowfat XML files) with the same query API as `syntax.py` for
the NT.  Each word carries syntactic role, stem, clause type, and an inline
LXX alignment — the Greek word and Strong's number that translates this
specific token in the Septuagint.

```python
from bible_grammar import load_syntax_ot, query_syntax_ot, lxx_alignment

df = load_syntax_ot()     # 475,911 rows; cached as Parquet after first load

# Gen 1:1 with syntactic roles and LXX words
query_syntax_ot(book='Gen', chapter=1, verse=1)[
    ['text','lemma','strong_h','role','gloss','greek','greek_g','stem','type_']
]

# All wayyiqtol (narrative past) verbs in Genesis
query_syntax_ot(book='Gen', tense='wayyiqtol')     # 2,105 tokens

# Niphal perfects in Isaiah
query_syntax_ot(book='Isa', stem='niphal', tense='qatal')   # 97 tokens

# Aramaic sections (Daniel, Ezra, 2 words in Gen/Jer)
query_syntax_ot(lang='A')                          # 7,549 Aramaic tokens

# How does the LXX translate שָׁלוֹם?
lxx_alignment('H7965')
# → εἰρήνη 98%, σωτηρίας 2%

# How does the LXX translate רוּחַ?
lxx_alignment('H7307')
# → πνεῦμα 94%, ἄνεμος 5%
```

The inline LXX alignment in MACULA Hebrew is word-level, derived from the
actual syntax tree — a higher-precision source than the IBM Model 1 alignment
in `ibm_align.py`, complementing it for detailed OT↔LXX studies.

Available filters: `book`, `chapter`, `verse`, `strong_h`, `lemma`, `role`,
`stem`, `pos`, `lang`, `tense` (wayyiqtol/qatal/yiqtol/…), `person`, `gender`,
`number`, `state`, `greekstrong`, `has_subjref`, `has_participantref`.

---

## Speaker Attribution

`speaker.py` identifies which NT verses contain Jesus speaking, using two
complementary strategies that combine into a single `is_jesus_speaking()` predicate:

1. **Curated allowlists** — hand-curated frozensets of (book, chapter, verse) triples
   for Son of Man sayings (74 Gospel verses), all seven Johannine I AM declarations,
   and Bridegroom parables. Confidence is 100%.
2. **MACULA subjref detection** — speech verbs (λέγω, φημί, λαλέω, ἀποκρίνομαι,
   εἶπεν, ὁμολογέω, κράζω) whose `subjref` resolves to Iesous (G2424) in the
   MACULA Greek syntax tree.

```python
from bible_grammar import is_jesus_speaking, jesus_speaking_verse_set, ALLOWLIST_VERSES

# Is Jesus the speaking subject in this verse?
is_jesus_speaking('Mat', 16, 13)   # True  — "Who do people say the Son of Man is?"
is_jesus_speaking('Jhn', 8, 58)    # True  — "Before Abraham was born, I AM"
is_jesus_speaking('Mat', 3, 17)    # False — God speaks, not Jesus

# Full set of Gospel verses where Jesus speaks
speaking_set = jesus_speaking_verse_set(['Mat', 'Mrk', 'Luk', 'Jhn'])

# View curated allowlists
print(list(ALLOWLIST_VERSES.keys()))
# ['Son of Man', 'I AM', 'Bridegroom']
```

---

## Lexicon API

`lexicon.py` provides a clean public API for the TBESH (Hebrew) and TBESG (Greek)
Translators Brief lexicons from STEPBible, centralizing parsing that was previously
duplicated. Each entry includes Strong's number, lemma, transliteration, POS code,
gloss, and full definition.

```python
from bible_grammar import lookup, search_gloss, lex_entry, lemma_index

# Dict lookup by Strong's number
lookup('H7965')    # {'strongs': 'H7965', 'lemma': 'שָׁלוֹם', 'gloss': 'peace', ...}
lookup('G3056')    # {'strongs': 'G3056', 'lemma': 'λόγος', 'gloss': 'word', ...}

# Pretty-print a full lexicon article
lex_entry('H2617')    # חֶסֶד — lovingkindness / steadfast love
lex_entry('G26')      # ἀγάπη — love

# Search by English gloss keyword
search_gloss('covenant', lang='H')   # → H1285 בְּרִית, H6194 עָרֵם, …
search_gloss('faith', lang='G')      # → G4102 πίστις, G4100 πιστεύω, …

# Reverse lookup: lemma → Strong's number
heb_idx = lemma_index('H')
heb_idx['שָׁלוֹם']   # → 'H7965'
```

---

## Christological Titles

`christological_titles.py` counts how frequently Jesus used various titles to
refer to Himself across the four Gospels. An optional **speaker filter** restricts
counts to verses where Jesus is the grammatical speaking subject, removing narrator
references and other characters' uses of the titles.

```python
from bible_grammar import title_counts, print_title_counts, title_chart, title_verses

# All Gospel occurrences (unfiltered)
print_title_counts(scope='gospels', speaker_filter=False)

# Only where Jesus is the speaking subject (more precise)
print_title_counts(scope='gospels', speaker_filter=True)

# Bar chart
title_chart(scope='gospels', speaker_filter=True,
            output_path='output/charts/nt/names/christological-titles.png')

# All (book, ch, vs) tuples for a specific title
title_verses('I AM')          # 7 Johannine I AM sayings
title_verses('Son of Man')    # 76 filtered occurrences across the Gospels
```

**Effect of speaker filter:** Son of Man 88→76, Son of God 42→7, Kyrios 244→16.
The filter removes instances where the narrator, disciples, or opponents use the
title — leaving only Jesus' direct self-references.

Pre-generated report: `output/reports/nt/names/christological-titles.md`.

---

## Syntactic Role Search

`role_search.py` answers "who does what to whom" by following MACULA `subjref`
links. Given one or more Strong's numbers, it finds all verb tokens whose
grammatical subject resolves to those entities — for both OT Hebrew and NT Greek.

```python
from bible_grammar import subject_verbs, verb_subjects, print_role_summary
from bible_grammar import role_chart, divine_action_comparison, role_report
from bible_grammar import GOD_OT, GOD_NT, JESUS_NT

# What does God (YHWH + Elohim) do in the OT?
print_role_summary(['H3068', 'H0430'], corpus='OT', top_n=20, label='YHWH+Elohim')

# What does God do in the NT?
print_role_summary(['G2316'], corpus='NT', top_n=20, label='Theos')

# What does Jesus do in the Gospels?
print_role_summary(['G2424'], corpus='NT', books=['Mat', 'Mrk', 'Luk', 'Jhn'],
                   label='Iesous')

# YHWH's verbs in Isaiah only
print_role_summary(['H3068'], corpus='OT', books=['Isa'])

# Who takes בָּרָא (bara, create) as their grammatical subject?
# Result: exclusively divine entities (plus 2 edge cases)
verb_subjects('H1254', corpus='OT')

# Side-by-side OT/NT chart: God's top verbs in each corpus
ot_df, nt_df, chart_path = divine_action_comparison()

# Full Markdown report with book distribution and cross-testament comparison
role_report(['H3068', 'H0430'], corpus='OT', label='YHWH+Elohim',
            include_cross_testament=True)
```

Pre-generated report: `output/reports/ot/names/role-yhwh-elohim-ot.md`.

**Slash command:** `/role-search H3068,H0430` or `/role-search G2424 NT Mat Mrk Luk Jhn`

---

## Object / Argument Search

`role_search.py` also provides the *symmetric* direction: given an entity's Strong's
number(s), find what verbs are performed *on* that entity, and what objects verbs
with that subject act upon — the patient/object slots of the predicate.

**OT method:** parses the MACULA Hebrew verb `frame` column (`A0`=agent, `A1`=patient)
to find verb→object triples where `A0` resolves to the target entity.

**NT method:** finds verbs with the target as `subjref` subject, then collects
co-verse tokens tagged `role='o'` or `role='o2'`.

```python
from bible_grammar import subject_objects, object_verbs, print_object_summary

# What does YHWH+Elohim act upon in the OT?
print_object_summary(['H3068', 'H0430'], corpus='OT', top_n=20)

# What does Jesus act upon in the Gospels?
print_object_summary(['G2424'], corpus='NT', books=['Mat', 'Mrk', 'Luk', 'Jhn'])

# What verbs are performed ON Israel?
object_verbs('H3478', corpus='OT')

# What is done TO the disciples (G3101) in the NT?
object_verbs('G3101', corpus='NT')

# Get raw verb+object pairs as a DataFrame
df = subject_objects(['H3068'], corpus='OT', books=['Isa'])
```

**Slash command:** `/object-search H3068,H0430` or `/object-search G2424 NT Mat Mrk Luk Jhn`

---

## LXX as a Queryable Corpus

`lxx_query.py` exposes the full Septuagint (Rahlfs 1935, CenterBLC edition,
623,693 tokens) as a first-class queryable corpus with the same filter API
as `query.py` and `syntax.py`. Covers all 39 canonical OT books plus
deuterocanonical books; filters for canonical-only are on by default.

Each token carries: word form, lemma, transliteration, gloss, Strong's number,
part of speech, tense, voice, mood, case, number, gender, person.

```python
from bible_grammar import (query_lxx, lxx_by_book, lxx_freq_table,
                            lxx_concordance, lxx_verb_stats, print_lxx_query)

# Word query — all occurrences of διαθήκη (covenant) in the LXX
query_lxx(strongs='G1242')

# Restrict to a book or group
query_lxx(strongs='G2316', book='Isa')          # θεός in Isaiah
query_lxx(strongs='G4151', book_group='prophets')  # πνεῦμα in Prophets
query_lxx(lemma='εἰρήνη')                       # all peace occurrences

# Per-book counts
lxx_by_book(strongs='G1242')     # διαθήκη in canonical order

# Verb morphology breakdown
lxx_verb_stats(strongs='G4160')  # ποιέω tense/voice/mood

# Frequency table of any column
lxx_freq_table('tense', part_of_speech='Verb', book_group='prophets')
lxx_freq_table(['book_id', 'part_of_speech'])

# Concordance (one row per occurrence)
lxx_concordance('G2316', book='Isa')

# Formatted terminal summary
print_lxx_query(strongs='G1242')   # by-book table + verb breakdown
print_lxx_query(strongs='G2316', book_group='prophets')

# Deuterocanonical books (excluded by default)
query_lxx(strongs='G4678', include_deuterocanon=True)  # Wisdom books
```

The LXX corpus completes the **OT → LXX → NT pipeline**:
- `lxx_alignment()` (MACULA Hebrew) gives word-level Hebrew→LXX alignment
- `lxx_query()` / `lxx_by_book()` give LXX morphology and distribution
- `query()` / `query_syntax()` (TAGNT / MACULA Greek) give NT usage

**Slash command:** `/lxx-query G1242` or `/lxx-query G2316 prophets`

---

## OT Speaker Attribution

`ot_speaker.py` identifies who speaks in the Hebrew Bible by resolving MACULA
Hebrew `subjref` links on speech-verb tokens (אָמַר, דָּבַר, קָרָא, עָנָה,
צָוָה, שָׁלַח, נָאַם) to their grammatical subjects.

```python
from bible_grammar import (speaker_verses, divine_speech_by_book, who_speaks,
                            divine_speech_verses, print_speaker_summary,
                            print_divine_speech_by_book, speaker_report,
                            GOD_OT_SPEECH)

# What does YHWH+Elohim say in Isaiah?
print_speaker_summary(['H3068', 'H0430'], books=['Isa'], label='YHWH+Elohim')

# Per-book divine speech counts with percentage of all speech in that book
print_divine_speech_by_book()
# → Lamentations 31.8% | Psalms 25.9% | Leviticus 22.0% | …

# Who speaks in Job? (character breakdown)
who_speaks('Job')
# → Job 47 tokens | Elihu 10 | El 7 | Satan 5 | YHWH 5 | Eliphaz 4 | …

# List all verses where YHWH speaks in Jeremiah
divine_speech_verses('Jer')   # → ['JER 1:5!...', 'JER 1:7!...', ...]

# Full Markdown report with by-book table and character breakdown
speaker_report(['H3068', 'H0430'], books=['Isa'], label='YHWH+Elohim',
               output_dir='output/reports')
```

**Slash command:** `/ot-speaker H3068,H0430 Isa` or `/ot-speaker who Job`

---

## Louw-Nida Domain Search

`domain_search.py` queries the Greek NT by Louw-Nida semantic domain. Each
MACULA Greek token carries a `domain` code (e.g. `033006`) and an `ln` reference
(e.g. `33.69`), covering all 93 top-level Louw-Nida domains.

```python
from bible_grammar import (query_domain, top_domain_words, domain_profile,
                            domain_role_search, domain_comparison,
                            print_domain_summary, print_domain_role,
                            DOMAIN_NAMES, THEOLOGY_DOMAINS)

# Top words in the Communication domain (33)
print_domain_summary(33, top_n=15)

# Supernatural Beings domain (12) in Revelation
print_domain_summary(12, book='Rev')

# Communication-domain verbs where God (Theos) is the subject
print_domain_role(33, ['G2316'], subject_label='Theos')
# → λέγω 33.69 (say), καλέω 33.312 (call), ἐπαγγέλλομαι 33.286 (promise) …

# Religious Activity domain (53) where Jesus acts in the Gospels
print_domain_role(53, ['G2424'], books=['Mat', 'Mrk', 'Luk', 'Jhn'])

# Semantic domain profile of a NT book
domain_profile('Rom', top_n=15)

# Compare domain profiles across books
domain_comparison(['Rom', 'Heb', 'Rev'], top_n=12)
# → Romans: Communication 11.5%, Supernatural 7.1%, Affirmation 6.4%
# → Revelation: Geographical 6.8%, Number/Quantity 6.7%, Artifacts 5.9%

# Theological domain groupings
print(THEOLOGY_DOMAINS)
# → {'God / Supernatural': [12], 'Communication': [33], 'Forgiveness': [39,40], …}
```

**Slash command:** `/domain-search 33` · `/domain-search 33 G2316` · `/domain-search compare Rom Heb Rev`

---

## Cross-Testament Trajectory

`trajectory.py` stitches together the full lexical journey of a word from Hebrew OT
→ LXX Septuagint → Greek NT, assessing whether the NT adopts the LXX's vocabulary
(high continuity) or diverges to new word choices.

**Pipeline stages:**
1. OT Hebrew stats (`word_study`)
2. OT → LXX alignment (MACULA Hebrew inline Greek — word-level precision)
3. LXX corpus distribution (`lxx.parquet`)
4. NT usage (TAGNT parquet)
5. Continuity assessment: `high | medium | low | none`

```python
from bible_grammar import print_trajectory, save_trajectory_report, word_trajectory

# Terminal report: shalom OT → LXX εἰρήνη → NT
print_trajectory('H7965')

# Terminal report: ruach/spirit OT → LXX πνεῦμα → NT
print_trajectory('H7307')

# Terminal report: berith/covenant OT → LXX διαθήκη → NT
print_trajectory('H1285')

# Start from Greek side
print_trajectory('G1515')    # eirene in NT/LXX

# Full Markdown report + 3-panel chart (OT blue | LXX green | NT red)
path = save_trajectory_report('H7965')

# Full pipeline dict (all stages accessible programmatically)
t = word_trajectory('H7965')
print(t['continuity'])        # 'high'
print(t['continuity_note'])   # explanation
print(t['lxx_total'])         # tokens in LXX
print(t['nt_total'])          # tokens in NT
```

Continuity levels:
- **high** — NT uses the same Greek word as the LXX's dominant rendering (≥80% consistent)
- **medium** — same word, but LXX rendering is split (<80% consistent) or vice versa
- **low** — NT uses a different word than the LXX primary rendering
- **none** — insufficient data

**Slash command:** `/trajectory H7965` · `/trajectory H7307 report` · `/trajectory summary` · `/trajectory all`

---

## Theological Term Reports

`theological_reports.py` provides 14 pre-built cross-testament trajectory studies for
key Hebrew theological terms. Each generates a Markdown + chart report and contributes
to a summary comparison table.

**Terms covered:**

| Key | Hebrew | Gloss | Theme |
|---|---|---|---|
| `bara` | בָּרָא | create | Creation |
| `berith` | בְּרִית | covenant | Covenant |
| `ruach` | רוּחַ | spirit/wind | Spirit |
| `shalom` | שָׁלוֹם | peace/welfare | Peace |
| `tsedeq` | צֶדֶק | righteousness | Righteousness |
| `hesed` | חֶסֶד | lovingkindness | Covenant Love |
| `yeshua` | יְשׁוּעָה | salvation | Salvation |
| `kavod` | כָּבוֹד | glory | Glory |
| `ahav` | אָהַב | love | Love |
| `emunah` | אֱמוּנָה | faithfulness | Faith |
| `torah` | תּוֹרָה | law/instruction | Law |
| `padah` | פָּדָה | redeem | Redemption |
| `kaphar` | כָּפַר | atone | Atonement |
| `qadosh` | קָדוֹשׁ | holy | Holiness |

```python
from bible_grammar import (print_theological_summary, run_theological_report,
                            run_all_theological_reports, THEOLOGICAL_TRAJECTORIES)

# Compact overview: OT total | LXX total | NT total | continuity
print_theological_summary()

# Full report for one term → Markdown + chart
r = run_theological_report('hesed', output_dir='output/reports/ot/lexicon')
print(r['trajectory']['continuity_note'])

# Batch: generate all 14 reports
run_all_theological_reports(output_dir='output/reports/ot/lexicon')
```

**Slash command:** `/trajectory summary` · `/trajectory all` · `/trajectory hesed`

---

## Hebrew Poetry Analysis

`poetry.py` analyzes the structure of Hebrew poetry using the cantillation accent
system embedded in the Masoretic Text. The **Etnahta** (U+0591) marks the primary
mid-verse division (end of A-colon); **Zaqef Gadol/Revia** may mark a C-colon.

**Features:**
- **Cola splitting** — every verse split into 2 or 3 cola by accent detection
- **Parallel word pairs** — content words (nouns, verbs, adjectives) paired across
  A/B cola; aggregated across a whole book to reveal canonical word pairs
- **Parallelism classification** — heuristic classifier: synonymous (high
  lexical/domain overlap) · antithetic (negation in B-colon) · synthetic (default)
- **Book statistics** — type distribution and cross-book comparison

```python
from bible_grammar import print_verse_analysis, print_book_pairs, print_parallelism_stats

# Cola split + parallelism type for one verse
print_verse_analysis('Psa', 19, 2)
# → Colon A: "The heavens declare the glory of God"
# → Colon B: "and the work of his hands"
# → Colon C: "the firmament shows"
# → Parallelism: SYNTHETIC

print_verse_analysis('Pro', 10, 1)
# → Colon A: "A wise son makes a father glad"  (+ superscription)
# → Colon C: "the grief of his mother" (shared lemma: בֵּן son)

# Most frequent A/B parallel word pairs in Proverbs
print_book_pairs('Pro', top_n=20, min_count=2)
# → חׇכְמָה/דַּעַת (wisdom/knowledge) × 4
# → מֶלֶךְ/רָזַן (kings/rulers) × 3
# → פֶּה/שָׂפָה (mouth/lips) × 3

# Parallelism type breakdown
print_parallelism_stats('Pro')
```

Primary poetry books: `Psa` · `Pro` · `Job` · `Sng` · `Lam` · `Ecc`

**Slash commands:**
`/poetry verse Psa 19:2` · `/poetry pairs Pro` · `/poetry stats Psa` · `/poetry compare Psa Pro Job`

### Chiasm Detection

Identifies A B … B' A' mirror structure across a verse range using lemma-level
Jaccard similarity between mirrored verse pairs. Each verse's content-word lemmas
are compared against its structural mirror.

```python
from bible_grammar import print_chiasm, detect_chiasm

# Psalm 8 — framed by "how majestic is your name" (vv. 1, 9)
print_chiasm('Psa', 8, 1, 9)

# Programmatic access: get raw scores and pattern labels
result = detect_chiasm('Psa', 23, 1, 6)
print(result['pattern'])       # ['A', 'B', 'C', "C'", "B'", "A'"]
print(result['mean_score'])    # average Jaccard across mirror pairs
print(result['is_chiasm'])     # True if mean_score >= 0.10
```

**Slash command:** `/poetry chiasm <book> <ch> <vs1> <vs2>`
- `/poetry chiasm Psa 8 1 9`   — Psalm 8 frame
- `/poetry chiasm Psa 23 1 6`  — Psalm 23

### Acrostic Detection

Checks whether successive verses begin with successive letters of the Hebrew
alphabet (א through ת = 22 letters). Supports stanza acrostics where groups of
verses share the same opening letter (e.g. Psalm 119: 8 verses per letter).

```python
from bible_grammar import print_acrostic, acrostic_known, KNOWN_ACROSTICS

# Lamentations 1 — 100% match (all 22 letters)
print_acrostic('Lam', 1, 1, 22)

# Psalm 119 — stanza acrostic: 8 verses per letter, 176 verses total
print_acrostic('Psa', 119, 1, 176, stanza_size=8)

# Check what acrostics are known for a book
print(acrostic_known('Psa'))   # [9, 10, 25, 34, 37, 111, 112, 119, 145]
print(KNOWN_ACROSTICS)         # full registry: Psa, Pro, Lam, Nah
```

**Slash command:** `/poetry acrostic <book> <ch> <vs1> <vs2> [stanza]`
- `/poetry acrostic Lam 1 1 22`        — Lamentations 1
- `/poetry acrostic Psa 25 1 22`       — Psalm 25
- `/poetry acrostic Psa 119 1 176 8`   — Psalm 119 (stanza=8)

### Meter Analysis

Estimates the stress pattern per colon using content-word counting (heuristic
approximation of classical Hebrew stress-counting meter). Syllables are estimated
from vowel-point counts in the MT. The qinah (3+2) pattern characteristic of
lament poetry is flagged automatically.

```python
from bible_grammar import print_verse_meter, print_meter_stats, verse_meter

# Single verse — stress count + syllable estimate per colon
print_verse_meter('Lam', 1, 1)
# → Colon A: 3 stresses, ~10 syllables
# → Colon B: 2 stresses, ~7 syllables
# → pattern=3+2  type=qinah(3+2)

# Meter distribution across a whole book
print_meter_stats('Lam')

# Programmatic access
m = verse_meter('Psa', 23, 1)
print(m['pattern'])     # e.g. '3+3'
print(m['meter_type'])  # 'balanced(3+3)'
```

**Slash command:** `/poetry meter <book> <ch>:<vs>` · `/poetry meterstats <book>`
- `/poetry meter Lam 1:1`    — qinah pattern
- `/poetry meterstats Lam`   — distribution across Lamentations

---

## Hebrew Verbal Syntax Analysis

`verbal_syntax.py` provides five analysis tools for studying the Hebrew verb system
at the syntactic and discourse level — designed for 2nd-year Biblical Hebrew study.

### Verb Form Profile

Distribution of all eleven Hebrew verb conjugation types for a book or chapter.
Immediately reveals the text-type: narrative is wayyiqtol-heavy; poetry is
yiqtol/qatal-heavy; prophecy blends qatal (certainty) with yiqtol (future).

```python
from bible_grammar import print_verb_form_profile, verb_form_chart

# Genesis: 42% wayyiqtol (narrative prose)
print_verb_form_profile('Gen')

# Psalms: 31% yiqtol, 25% qatal, 6% wayyiqtol (poetry)
print_verb_form_profile('Psa')

# Chapter-level profile
print_verb_form_profile('Gen', chapter=1)

# Save a bar chart PNG
verb_form_chart('Gen', output_path='output/charts/ot/verbs/verb-forms-gen.png')
```

### Wayyiqtol Chain Analysis

Identifies consecutive wayyiqtol sequences (the "and he did X, and he did Y"
narrative backbone) and reports what breaks each chain — whether a jussive,
qatal summary, participle, or direct speech marker.

```python
from bible_grammar import print_wayyiqtol_chains, wayyiqtol_chains

# Genesis 1: 15 chains, longest = 7 verbs; chains break on God's speech (jussive)
print_wayyiqtol_chains('Gen', 1)

# Programmatic access
chains = wayyiqtol_chains('Ruth', 1)
for c in chains:
    print(c['length'], c['break_type'])
```

### Infinitive Usage

Analyses infinitive construct (with governing preposition) and infinitive absolute
(with paronomastic detection). Shows whether inf-construct follows לְ (purpose),
בְּ/כ (temporal), אחרי (sequence), or serves as subject/object.

```python
from bible_grammar import print_infinitive_usage

# Genesis: 66% lamed (purpose), detects Gen 2:16-17 paronomastic inf-abs
print_infinitive_usage('Gen')

# Deuteronomy: rich in inf-construct (legal instructions)
print_infinitive_usage('Deut')
```

Key findings for teaching:
- Gen 2:16 `אָכֹל תֹּאכַל` — paronomastic inf-abs ⟦you may freely eat⟧
- Gen 2:17 `מוֹת תָּמוּת` — paronomastic inf-abs ⟦you shall surely die⟧
- ~66% of all inf-construct in Genesis governed by לְ (purpose/result clauses)

### Clause Type Profile

Counts verbal vs. nominal clauses, plus negation tokens, conditional markers
(אִם, לוּ), relative clauses (אֲשֶׁר), and interrogatives.

```python
from bible_grammar import print_clause_type_profile

# Genesis: 95% verbal clauses (prose narrative — almost always finite verb)
print_clause_type_profile('Gen')

# Proverbs: more nominal clauses (aphorisms, stative descriptions)
print_clause_type_profile('Pro')
```

### Stem (Binyan) Distribution

Frequency of each binyan — Qal, Niphal, Piel, Pual, Hiphil, Hophal, Hithpael,
and rarer stems. Useful for asking: where does the author concentrate Hiphil
(causative) vs. Piel (intensive)?

```python
from bible_grammar import print_stem_distribution, stem_chart

# Genesis: Qal 77%, Hiphil 10%, Piel 7%
print_stem_distribution('Gen')

# Save horizontal bar chart
stem_chart('Gen')
```

**Slash command:** `/verbal-syntax <command> <book> [args]`
- `/verbal-syntax forms Gen`      — verb form profile
- `/verbal-syntax forms Gen 1`    — chapter-level profile
- `/verbal-syntax chains Gen 1`   — wayyiqtol chain analysis
- `/verbal-syntax inf Gen`        — infinitive usage
- `/verbal-syntax clauses Gen`    — clause type profile
- `/verbal-syntax stems Gen`      — stem distribution
- `/verbal-syntax report Gen`     — full Markdown report
- `/verbal-syntax disj Gen 37`    — disjunctive clauses in Gen 37
- `/verbal-syntax disjchains Gen 37` — chains + disjunctive interruptions

### Disjunctive Clause Analysis

A **disjunctive clause** opens with a noun, pronoun, or adjective rather than a
verb — subject-first word order that signals a departure from the main narrative
line. Discourse grammarians (Longacre, Niccacci, Waltke-O'Connor) identify these
functions: circumstantial background, contrastive, resumptive, flashback, and
summary/comment.

```python
from bible_grammar import (print_disjunctive_clauses, print_disjunctive_in_chains,
                            disjunctive_clauses, disjunctive_in_chains)

# Survey disjunctives in a chapter
print_disjunctive_clauses('Gen', 1)
# → Gen 1:1  noun/qatal  — circumstantial / background
# → Gen 1:2  noun/qatal  — circumstantial / background (וְהָאָרֶץ הָיְתָה תֹהוּ)

print_disjunctive_clauses('Gen', 37)
# → Gen 37:3  noun/qatal  — "Israel loved Joseph" (contrastive with brothers)
# → Gen 37:36 noun/qatal  — Midianites subplot (new background thread)

# Cross-reference with wayyiqtol chains to see flow interruptions
print_disjunctive_in_chains('Gen', 37)
# → Chain 14 [vv34-35] terminated by disjunctive at v36 (subplot begins)

# Whole-book survey
df = disjunctive_clauses('Gen')
print(df['discourse_function'].value_counts())
```

**Slash commands:**
- `/verbal-syntax disj <book> [ch]`      — list all disjunctive clauses
- `/verbal-syntax disjchains <book> <ch>` — chains + interruption annotations

### Conditional Clause Analysis

Detects אִם (real conditions), לוּ (wish/irreal), and לוּלֵא (counterfactual), and
classifies each by protasis verb form:

| Type | Particle | Protasis verb | Meaning |
|---|---|---|---|
| Real — open future | אִם | yiqtol | "if you do X" (most common) |
| Real — past/present | אִם | qatal | "if you have done X" |
| Real — stative | אִם | participle | habitual/general truth |
| Irreal — wish | לוּ | yiqtol | "if only…" |
| Irreal — counterfactual | לוּ / לוּלֵא | qatal | "had it not been…" |

```python
from bible_grammar import (print_conditional_clauses, print_conditional_summary,
                            conditional_clauses, conditional_summary)

# Chapter-level: Gen 18 Abraham bargaining (4× אִם + yiqtol, 1× אִם + qatal)
print_conditional_clauses('Gen', 18)

# Whole-book summary
print_conditional_summary('Gen')
# → 45% real-future (אִם + yiqtol)
# → 20% real-past (אִם + qatal)
# → irreal לוּ/לוּלֵא: Gen 17:18, 31:42, 43:10, 50:15 etc.

print_conditional_summary('Deu')
# → 50% real-future — Deuteronomy's legal conditional style

# Get raw DataFrame for custom analysis
df = conditional_clauses('Gen')
irreal = df[df['condition_type'].str.startswith('irreal')]
```

Note: MACULA uses `Deu` (not `Deut`) as the book ID for Deuteronomy.

**Slash commands:**
- `/verbal-syntax cond <book> [ch]`   — list conditionals with type classification
- `/verbal-syntax condsum <book>`      — summary distribution for a whole book

### Relative Clause Analysis

Detects אֲשֶׁר, שֶׁ, and דִּי relative markers and infers the syntactic role of
the relative pronoun within its clause using a three-step heuristic:

| Inferred role | Heuristic |
|---|---|
| **subject** | No overt subject in relative clause — אֲשֶׁר fills the slot |
| **object** | Rel clause has own subject, OR resumptive pronoun (role=o) |
| **oblique** | Resumptive pronoun with role=p (prepositional) |
| **verbless** | No verb in relative clause (predicate nominal / headless) |

Also classifies antecedent by semantic category: person / place / time / thing.

```python
from bible_grammar import (print_relative_clauses, print_relative_summary,
                            relative_clauses, relative_clause_summary)

# Chapter detail
print_relative_clauses('Gen', 3)
# → 5 object relatives (qatal), 1 subject relative

# Whole-book role × verb-form breakdown
print_relative_summary('Gen')
# Gen: 62% object, 34% subject; qatal dominates (57%)

# Cross-book comparison
import pandas as pd
books = ['Gen', 'Rut', 'Psa', 'Pro']
dfs = {b: relative_clauses(b) for b in books}
pivot = pd.DataFrame(
    {b: df['inferred_role'].value_counts() for b, df in dfs.items()}
).fillna(0).astype(int)
```

**Slash commands:**
- `/verbal-syntax rel <book> [ch]`   — relative clauses with role inference
- `/verbal-syntax relsum <book>`      — role/verb-form/antecedent summary

### Aspect Comparison Across Genres

Hebrew verb form distribution is one of the clearest markers of genre.
`aspect_comparison` builds a side-by-side percentage table; `aspect_comparison_chart`
saves a grouped bar chart PNG.

| Genre | Dominant forms | Signature |
|---|---|---|
| Narrative (Gen, Josh…) | wayyiqtol ~41% | Sequential foreground action |
| Legal (Deu, Lev) | weqatal 18% + yiqtol 28% | Future obligation sequences |
| Prophecy (Isa, Jer) | qatal + yiqtol balanced | Prophetic perfect; vision participles |
| Poetry (Psa, Pro) | yiqtol 31–36% + ptc.act 13–26% | Petition, habitual truth |

```python
from bible_grammar import (print_aspect_comparison, aspect_comparison_chart,
                            aspect_comparison, GENRE_SETS)

# Side-by-side percentage table
print_aspect_comparison(['Gen', 'Psa', 'Isa', 'Deu'])
# wayyiqtol: Gen 41.8% / Psa 5.8% / Isa 5.0% / Deu 7.3%  ← narrative marker
# yiqtol:    Gen 10.7% / Psa 30.9% / Isa 29.6% / Deu 27.6% ← poetry/law
# weqatal:   Gen  3.3% / Psa  0.8% / Isa  9.4% / Deu 18.0% ← Deu legal sequences

# Save grouped bar chart
path = aspect_comparison_chart(['Gen', 'Psa', 'Isa', 'Deu', 'Pro'])
# → output/charts/ot/verbs/aspect_comparison_Gen_Psa_Isa_Deu_Pro.png

# Raw DataFrame for custom analysis
df = aspect_comparison(['Gen', 'Psa', 'Isa', 'Deu'])
# MultiIndex columns: (book, 'count') and (book, 'pct')

# Use pre-defined genre book lists
print(GENRE_SETS['narrative'])  # ['Gen', 'Exod', 'Num', 'Josh', ...]
print(GENRE_SETS['poetry'])     # ['Psa', 'Pro', 'Job', 'Sng', 'Lam']
```

**Slash command:**
- `/verbal-syntax aspect <book1> [book2 ...]` — side-by-side comparison + saves PNG

### Discourse Particle Tagging

Seven key Hebrew discourse particles classified by discourse function using
MACULA's English gloss annotations:

| Particle | Category | Functions |
|---|---|---|
| הִנֵּה | presentative | attention-getter ("behold/look") |
| כִּי | connective | causal · content · adversative · conditional · asseverative · temporal |
| וְ | connective | sequential · adversative · logical · emphatic · temporal |
| לָכֵן | consequence | "therefore / so" |
| עַתָּה | temporal | discourse "now" (logical pivot) |
| גַּם | additive | "also / even" |
| אַךְ | restrictive | "only / surely / but" |

```python
from bible_grammar import (print_discourse_particles, print_particle_summary,
                            discourse_particles, discourse_particle_summary)

# Chapter detail — Isaiah 40 has three הִנֵּה presentatives + כִּי clauses
print_discourse_particles('Isa', 40)

# Book summary — Genesis כִּי breakdown
print_particle_summary('Gen')
# כִּי: 55.2% causal · 28.6% content · 4.8% temporal · 4.1% adversative

# Deuteronomy: more conditional כִּי (legal "if…then" protases)
print_particle_summary('Deu')

# Cross-book כִּי comparison
from bible_grammar import discourse_particle_summary
import pandas as pd
frames = {b: discourse_particle_summary(b) for b in ['Gen', 'Deu', 'Isa', 'Psa']}
```

**Slash commands:**
- `/verbal-syntax particles <book> [ch]` — per-verse particle listing with function
- `/verbal-syntax ptclsum <book>` — summary per particle type for a whole book

---

## Theological Term Map

Traces key theological concepts across OT Hebrew → LXX Greek → NT Greek,
showing whether NT authors adopt LXX vocabulary or use fresh terminology.

```python
from bible_grammar import term_map, print_term_map, THEOLOGICAL_TERMS

# Built-in theological domains
print(list(THEOLOGICAL_TERMS.keys()))
# ['Covenant / Faithfulness', 'Holiness / Purity', 'Righteousness / Justice', ...]

# Full trajectory for "Covenant / Faithfulness"
print_term_map('Covenant / Faithfulness')

# Custom term set
term_map(['H7965', 'G1515'])   # שָׁלוֹם / εἰρήνη (peace)
```

---

## Synonym Comparison

Side-by-side comparison of near-synonym Hebrew or Greek roots.

```python
from bible_grammar import compare_synonyms, print_synonym_comparison

# אָהַב vs חָשַׁק (love vs desire)
print_synonym_comparison(['H157', 'H2836'])

# NT love words
print_synonym_comparison(['G26', 'G5368'])   # ἀγάπη vs φιλέω

# Uses Hebrew/Greek lemmas directly (auto-resolved to Strong's)
print_synonym_comparison(['שָׁלוֹם', 'εἰρήνη'])
```

Output includes: frequency comparison with bars, LXX translation equivalents
(shared renderings marked †), OT→LXX→NT trajectory, book distribution, and
morphological form breakdown.

---

## Phrase & Proximity Search

Search for consecutive word sequences or statistically proximate words in the
Hebrew OT, Greek NT, or LXX.

```python
from bible_grammar import phrase_search, print_phrase_results
from bible_grammar import proximity_search, print_proximity_results

# Consecutive phrase search — tokens can be Strong's numbers, lemmas, or '*' wildcard
results = phrase_search(['H3068', 'H559'], corpus='OT')   # יְהוָה + אָמַר
print_phrase_results(results)

# "word" near "spirit" within 5 words (ordered, any direction)
results = proximity_search(['H1697', 'H7307'], within=5, corpus='OT')
print_proximity_results(results)

# Cross-verse proximity is supported; distance is in word tokens
results = proximity_search(['G3056', 'G2316'], within=10, corpus='NT')
```

Token types:
- Strong's number string: `'H7307'`, `'G3056'`
- Hebrew/Greek lemma (auto-resolved): `'רוּחַ'`, `'λόγος'`
- Wildcard: `'*'` matches any word
- Constraint dict: `{'strongs': 'H7307', 'stem': 'Qal'}` for morphological filtering

---

## Divine Names Analysis

Tracks the major divine names and christological titles across three corpora with
frequency tables, per-section breakdowns, stacked bar charts, and heatmaps.

**OT Hebrew:** YHWH (H3068G), Elohim (H0430), Adonai (H0136), El (H0410), Yah (H3050), Shaddai (H7706)  
**LXX Greek:** Kyrios (G2962), Theos (G2316)  
**NT Greek:** Theos (G2316), Kyrios (G2962), Iesous (G2424G), Christos (G5547), Pater (G3962), Pneuma (G4151)

```python
from bible_grammar import print_divine_names, divine_name_table
from bible_grammar import divine_name_by_section, divine_names_chart, divine_names_report

# Terminal summary
print_divine_names('OT')    # YHWH 65.8% | Elohim 26.3% | Adonai 4.4% …
print_divine_names('NT')    # Theos 30.2% | Iesous 22.1% | Kyrios 16.9% …

# Distribution by canonical section
divine_name_by_section('OT')   # Torah / Historical / Wisdom / Prophets

# Charts
divine_names_chart('NT', chart_type='stacked_bar')
divine_names_chart('OT', chart_type='heatmap')

# Full Markdown report (OT + LXX + NT)
divine_names_report()
```

Notable finding: **Adonai** is overwhelmingly a prophetic title (343 of 440 OT occurrences
are in the Prophets, 222 in Ezekiel alone). **Christos** concentrates heavily in Paul
(403 of 571 NT occurrences), while **Iesous** dominates the Gospels & Acts.

---

## Genre Comparison

Compares morphological patterns across the literary genres of the OT and NT —
verb stems, conjugations, tense, voice, mood, and part-of-speech distribution.

```python
from bible_grammar import genre_compare, print_genre_compare
from bible_grammar import genre_heatmap, genre_report

# OT: verb stem distribution across Torah / Historical / Wisdom / Prophets
print_genre_compare('OT', feature='verb_stem')
print_genre_compare('OT', feature='verb_conjugation')

# NT: verb tense/mood distribution across Gospels / Pauline / General
print_genre_compare('NT', feature='verb_tense')
print_genre_compare('NT', feature='verb_mood')

# Heatmap chart
genre_heatmap('OT', feature='verb_stem',
              output_path='output/charts/both/genre/ot-genre-verb-stem.png')

# Full Markdown report (OT + NT, all features)
genre_report()
```

Key findings:
- **Consecutive Perfect (wayyiqtol)** dominates Historical prose (36% of verbs) vs. Wisdom (5%) — narrative drive vs. reflection
- **Imperfect** dominates Wisdom poetry (31%) — habitual, timeless, or ongoing action
- **Paul** has the highest Present tense ratio (55%) in the NT — characteristic of didactic/hortatory style
- **Revelation/General letters** have the highest participle density (28%)

---

## Hapax Legomena

Words occurring only once in a given corpus or book.

```python
from bible_grammar import hapax_legomena, hapax_table, hapax_summary

# All hapax in Job
hapax_legomena(book='Job')

# Summary counts per book across the OT
hapax_summary(corpus='OT')
```

---

## Parallel Passages

Compare parallel passages between books (e.g. Samuel/Kings vs Chronicles,
Synoptic parallels).

```python
from bible_grammar import parallel_passage, print_parallel

print_parallel('2Sa', 22, 'Psa', 18)   # Psalm 18 = 2 Samuel 22
print_parallel('Mat', 5, 'Luk', 6)     # Sermon on the Mount / Plain
```

---

## HTML & CSV Export

Export any analysis as a self-contained HTML report (inline CSS and embedded charts,
ready to open in a browser or share) plus companion CSV data files.

```python
from bible_grammar import (export_word_study, export_semantic_profile,
                            export_genre_compare, export_divine_names, export_all)

# Word study → HTML + CSV
export_word_study('H7965')        # output/exports/html/h7965-word-study.html

# Semantic profile → HTML + CSV
export_semantic_profile('G3056')  # output/exports/html/g3056-semantic-profile.html

# Genre comparison → HTML + CSV (all features for one corpus)
export_genre_compare('OT')
export_genre_compare('NT')

# Divine names → HTML + CSV (all three corpora)
export_divine_names()

# Run all exporters at once
export_all()
```

Output directories:
- `output/exports/html/` — standalone HTML files (gitignored, regenerated on demand)
- `output/exports/csv/`  — raw CSV files organised by analysis type (gitignored)

---

## Charts

```python
from bible_grammar import charts

# Bar chart from any DataFrame
charts.bar_chart(df, x='stem', title='Verb Stems in Isaiah',
                 output_path='output/charts/ot/verbs/isaiah_stems.png')

# Heatmap (e.g. tense × voice)
charts.heatmap(df, index='tense', columns='voice', title='Tense × Voice in John')

# Grouped bar (e.g. stems per book)
charts.grouped_bar(df, x='book_id', hue='stem', title='Stems by Book')

# LXX consistency heatmap
from bible_grammar import consistency_heatmap
consistency_heatmap(['H7307', 'H2617'], output_path='output/charts/ot/lexicon/consistency.png')
```

---

## Hiphil (הִפְעִיל) Verb Morphology

Dedicated analysis module for teaching the Hiphil stem. Covers conjugation
distribution, most frequent roots, root × conjugation heatmap, book distribution,
Hiphil-dominant roots, and semantic function categories. Generates a full
Markdown report with 6 charts.

```python
from bible_grammar import (
    print_hiphil_overview, print_hiphil_conjugation,
    print_hiphil_top_roots, print_hiphil_root_conjugation,
    print_hiphil_book_distribution, print_hiphil_dominant_roots,
    print_hiphil_semantic_categories,
    hiphil_conjugation_chart, hiphil_book_chart,
    hiphil_stem_chart, hiphil_root_heatmap,
    hiphil_semantic_chart, hiphil_report,
    hiphil_data, hiphil_dominant_roots,
)

# Quick statistics
print_hiphil_overview()
# → 9,409 tokens · 12.9% of all OT verbs · 479 unique roots · 39 books

# Conjugation distribution
print_hiphil_conjugation()
# → yiqtol 21.5% · qatal 19.1% · wayyiqtol 18.6% · inf.cst 10.0%

print_hiphil_conjugation('Gen')   # Genesis only
print_hiphil_conjugation('Psa')   # Psalms only

# Top roots
print_hiphil_top_roots(25)
# → בּוֹא 548 (bring) · נָכָה 481 (strike) · שׁוּב 357 (restore)

# Root × conjugation cross-table
print_hiphil_root_conjugation(top_n=15)
# נָכָה: wayyiqtol-heavy (combat) · יָסַף: yiqtol-heavy (do again) · etc.

# Book distribution (top 20 + % of book's verbs)
print_hiphil_book_distribution()

# Hiphil-dominant roots (≥70% of their occurrences are Hiphil)
print_hiphil_dominant_roots()
# שָׁכַם 100% · נָבַט 98.6% · נָכָה 96.2% · קָשַׁב 97.8%

# Semantic function categories
print_hiphil_semantic_categories()
# causative motion 30.8% · violent/lethal 8.6% · declaration 7.5%

# Generate full report + 6 PNG charts
path = hiphil_report()
# Saves output/reports/ot/verbs/hiphil_report.md + output/charts/ot/verbs/hiphil_*.png
```

**Slash commands:**
- `/hiphil overview` — key OT-wide statistics
- `/hiphil conj [book]` — conjugation distribution
- `/hiphil roots [n]` — top n roots
- `/hiphil roottable [n]` — root × conjugation frequency table
- `/hiphil books` — distribution across all books
- `/hiphil dominant` — Hiphil-only roots
- `/hiphil semantic` — semantic function distribution
- `/hiphil report` — full report + all charts

---

## Hebrew Preposition Analysis

`prepositions.py` provides frequency, collocate, and object-type analysis for
Biblical Hebrew prepositions using the MACULA OT syntax data (~64,000 prep tokens,
46 unique lemmas). Inseparable prepositions (בְּ, לְ, כְּ) are tokenized as
separate rows with clean pointed lemmas.

```python
from bible_grammar import (prep_frequency, prep_by_book, prep_distribution_table,
                            prep_collocates, prep_object_types, compare_preps,
                            MAJOR_PREPS, PREP_GLOSS, BOOK_GROUPS)

# OT-wide frequency table
prep_frequency(top_n=15)
# → לְ 31.4% · בְּ 24.7% · מִן 12.3% · עַל 9.0% · אֶל 8.9% …

# Torah subset
prep_frequency(book_group='Torah', top_n=10)

# Distribution of לְ across all OT books
prep_by_book('לְ')

# Side-by-side count of major prepositions by book group
prep_distribution_table()

# Top noun collocates of לְ (purpose / indirect object)
prep_collocates('לְ', pos='noun', top_n=20)

# Top noun collocates of בְּ in Genesis
prep_collocates('בְּ', pos='noun', top_n=15, book='Gen')

# Grammatical types of what follows מִן
prep_object_types('מִן')

# Side-by-side collocate comparison: לְ vs אֶל (both mark direction)
compare_preps('לְ', 'אֶל', pos='noun', top_n=20)
```

**Book groups:** Torah · Former Prophets · Writings · Latter Prophets

**Notebook:** `notebooks/both/syntax/12_preposition_analysis.ipynb`

---

## Greek Preposition Analysis

`greek_prepositions.py` provides frequency, case-binding, and collocate analysis for
Greek prepositions in both the NT (MACULA Nestle1904, ~10,900 tokens) and the LXX
(CenterBLC Rahlfs 1935, ~55,000 tokens).

**Case binding** — Greek prepositions govern one or more cases depending on meaning.
Case is not stored on the preposition token; it is determined by an adjacency join
to the immediately following word (`word_num + 1`), normalized to Title case
(Accusative, Genitive, Dative).

```python
from bible_grammar import (
    greek_prep_frequency, greek_prep_by_book, greek_prep_distribution_table,
    greek_prep_cases, greek_prep_collocates, compare_greek_preps, nt_lxx_compare,
    NT_MAJOR_PREPS, LXX_MAJOR_PREPS, PREP_GLOSS,
)

# Frequency tables
greek_prep_frequency(corpus='nt', top_n=15)    # NT: ἐν 22%, εἰς 14%, ἐπί 8%…
greek_prep_frequency(corpus='lxx', top_n=15)   # LXX: ἐν 24%, εἰς 13%, ἐπί 13%…

# Distribution by book group
greek_prep_distribution_table(corpus='nt')   # Gospels / Acts / Pauline / …
greek_prep_distribution_table(corpus='lxx')  # Torah / Historical / Wisdom / …

# Case-binding profiles
greek_prep_cases('ἐν', corpus='nt')    # 98.6% Dative (monocase)
greek_prep_cases('εἰς', corpus='nt')   # 99.5% Accusative (monocase)
greek_prep_cases('διά', corpus='nt')   # 57.3% Genitive (through) · 41.2% Accusative (because of)
greek_prep_cases('ἐπί', corpus='nt')   # tricase: Accusative / Genitive / Dative

# NT vs. LXX case-binding comparison
nt_lxx_compare('ἐπί')   # Does ἐπί shift between LXX (translated from Hebrew) and NT?
nt_lxx_compare('διά')

# Collocates — filtered by case
greek_prep_collocates('ἐν', corpus='nt', case='Dative', top_n=15)
greek_prep_collocates('διά', corpus='nt', case='Genitive', top_n=15)   # through/by means of
greek_prep_collocates('διά', corpus='nt', case='Accusative', top_n=15) # because of

# Side-by-side comparison of two prepositions sharing semantic space
compare_greek_preps('εἰς', 'πρός', corpus='nt', top_n=20)   # both mark direction/goal
compare_greek_preps('ἀπό', 'ἐκ', corpus='nt', top_n=20)     # both mark separation/source

# Book-scoped queries
greek_prep_frequency(corpus='nt', book='Rom', top_n=12)
greek_prep_cases('διά', corpus='nt', book='Rom')
greek_prep_collocates('διά', corpus='nt', case='Genitive', book_group='Pauline', top_n=10)

# Distribution across all books
greek_prep_by_book('ἐν', corpus='nt')
greek_prep_by_book('ἐν', corpus='lxx')
```

**Notebook:** `notebooks/both/syntax/13_greek_preposition_analysis.ipynb`

---

## Derived Stem Verb Morphology

Dedicated analysis modules for each of the seven major derived Hebrew verb stems
(Niphal, Piel, Pual, Hophal, Hiphil, Hithpael — Hiphil documented separately above).
Each module provides the same analysis pattern: conjugation distribution, top roots,
root × conjugation cross-table, book distribution, stem-dominant roots, and semantic
function categories, plus a full Markdown report with charts.

### Niphal (נִפְעַל) — Reflexive-Passive

Typical functions: passive of Qal, reflexive, reciprocal, tolerative, middle/stative.

```python
from bible_grammar import (
    niphal_data, niphal_conjugation_profile, niphal_top_roots,
    niphal_root_conjugation, niphal_book_distribution, niphal_dominant_roots,
    niphal_semantic_categories,
    print_niphal_overview, print_niphal_conjugation, print_niphal_top_roots,
    print_niphal_root_conjugation, print_niphal_book_distribution,
    print_niphal_dominant_roots, print_niphal_semantic_categories,
    niphal_conjugation_chart, niphal_book_chart, niphal_stem_chart,
    niphal_root_heatmap, niphal_report,
)

print_niphal_overview()
# → 4,139 tokens · 5.7% of all OT verbs · 410 unique roots

niphal_report()
# → output/reports/ot/verbs/niphal_report.md + charts
```

### Piel (פִּעֵל) — Intensive-Active

Typical functions: intensive, factitive (makes a state into an action), declarative,
denominative.

```python
from bible_grammar import (
    piel_data, piel_conjugation_profile, piel_top_roots,
    piel_root_conjugation, piel_book_distribution, piel_dominant_roots,
    piel_semantic_categories,
    print_piel_overview, print_piel_conjugation, print_piel_top_roots,
    print_piel_root_conjugation, print_piel_book_distribution,
    print_piel_dominant_roots, print_piel_semantic_categories,
    piel_conjugation_chart, piel_book_chart, piel_stem_chart,
    piel_root_heatmap, piel_report,
)

print_piel_overview()

piel_report()
# → output/reports/ot/verbs/piel_report.md + charts
```

### Pual (פֻּעַל) — Intensive-Passive

Passive counterpart of the Piel. Less common than the Niphal passive.

```python
from bible_grammar import (
    pual_data, pual_conjugation_profile, pual_top_roots,
    pual_root_conjugation, pual_book_distribution, pual_dominant_roots,
    pual_semantic_categories,
    print_pual_overview, print_pual_conjugation, print_pual_top_roots,
    print_pual_root_conjugation, print_pual_book_distribution,
    print_pual_dominant_roots, print_pual_semantic_categories,
    pual_conjugation_chart, pual_book_chart, pual_stem_chart,
    pual_root_heatmap, pual_report,
)

print_pual_overview()

pual_report()
# → output/reports/ot/verbs/pual_report.md + charts
```

### Hophal (הָפְעַל) — Causative-Passive

Passive of the Hiphil causative (~480 tokens — least common major stem). Restricted
to roots where the Hiphil causative is established.

```python
from bible_grammar import (
    hophal_data, hophal_conjugation_profile, hophal_top_roots,
    hophal_root_conjugation, hophal_book_distribution, hophal_dominant_roots,
    hophal_semantic_categories,
    print_hophal_overview, print_hophal_conjugation, print_hophal_top_roots,
    print_hophal_root_conjugation, print_hophal_book_distribution,
    print_hophal_dominant_roots, print_hophal_semantic_categories,
    hophal_conjugation_chart, hophal_book_chart, hophal_stem_chart,
    hophal_root_heatmap, hophal_report,
)

print_hophal_overview()
# → ~480 tokens · least common major stem

hophal_report()
# → output/reports/ot/verbs/hophal_report.md + charts
```

### Hithpael (הִתְפַּעֵל) — Reflexive-Intensive

Typical functions: reflexive of the Piel, reciprocal, iterative, tolerative.

```python
from bible_grammar import (
    hithpael_data, hithpael_conjugation_profile, hithpael_top_roots,
    hithpael_root_conjugation, hithpael_book_distribution, hithpael_dominant_roots,
    hithpael_semantic_categories,
    print_hithpael_overview, print_hithpael_conjugation, print_hithpael_top_roots,
    print_hithpael_root_conjugation, print_hithpael_book_distribution,
    print_hithpael_dominant_roots, print_hithpael_semantic_categories,
    hithpael_conjugation_chart, hithpael_book_chart, hithpael_stem_chart,
    hithpael_root_heatmap, hithpael_report,
)

print_hithpael_overview()

hithpael_report()
# → output/reports/ot/verbs/hithpael_report.md + charts
```

All derived-stem modules share the same pattern:

| Function pattern | Description |
|---|---|
| `*_overview()` | Total tokens, % of OT verbs, unique roots, books |
| `*_conjugation(book=None)` | Distribution by conjugation type |
| `*_top_roots(n, book=None)` | Most frequent roots with gloss |
| `*_root_conjugation()` | Root × conjugation frequency heatmap data |
| `*_book_distribution()` | Count + % per OT book |
| `*_dominant_roots(min_pct=70)` | Roots ≥70% stem-specific |
| `*_semantic_categories()` | Semantic function distribution |
| `*_report()` | Full Markdown report + charts |

---

## OT Noun Morphology

`ot_noun_profile.py` provides state, gender, number, and article statistics for
Hebrew nouns across the OT, backed by the MACULA Hebrew WLC dataset.

Key teaching point (BBH Ch4, Ch10): the three noun **states** — absolute (free form),
construct (bound to following noun in a chain), and determined (with definite article
or pronominal suffix) — each have distinct forms and functions.

```python
from bible_grammar import (
    ot_noun_data, ot_adj_data,
    ot_noun_gender_profile, ot_noun_number_profile, ot_noun_state_profile,
    ot_noun_gender_state, ot_noun_top_lemmas, ot_noun_lemma_state,
    ot_noun_book_distribution, ot_noun_genre_profile,
    ot_article_usage, ot_construct_top_lemmas,
    print_ot_noun_overview, print_ot_noun_gender, print_ot_noun_state,
    print_ot_noun_top_lemmas, print_ot_construct_top_lemmas,
    print_ot_noun_genre_profile, print_ot_noun_book_distribution,
    print_ot_article_usage,
    ot_noun_state_chart, ot_noun_gender_chart,
    ot_noun_genre_heatmap, ot_noun_book_chart,
)

# OT-wide noun state distribution
print_ot_noun_state()
# → absolute 64.5% · construct 19.3% · determined 16.2%

# Top construct-state nouns (identify key construct chains)
print_ot_construct_top_lemmas(20)
# → דְּבַר 1,632 (word of) · בֵּן 1,503 (son of) · עֶבֶד 853 (servant of) …

# Article usage statistics (article vs. anarthrous)
print_ot_article_usage()

# State distribution across Torah / Historical / Wisdom / Prophets
print_ot_noun_genre_profile()

# Top 20 nouns in Genesis
print_ot_noun_top_lemmas(20, book='Gen')
```

**Notebook:** `notebooks/ot/nouns/01_ot_noun_profile.ipynb`

---

## OT Number Morphology

`ot_numbers.py` analyses the 6,881 Hebrew number tokens (class_='num') in the MACULA
Hebrew WLC dataset, covering cardinals, ordinals, gender polarity, construct chains,
and distribution across the corpus.

**Key pedagogical point (BBH Ch11):** the gender-polarity rule — cardinal numbers 3–10
take the *opposite* gender of the noun they count. Numbers 1–2 agree normally; 11–19
use both forms; 20+ are invariable.

```python
from bible_grammar import (
    ot_number_data, ot_number_frequency,
    ot_number_gender_profile, ot_number_state_profile,
    ot_number_book_distribution, ot_number_genre_profile,
    ot_number_polarity_table, ot_top_number_lemmas,
    print_ot_number_overview, print_ot_number_frequency,
    print_ot_number_gender, print_ot_number_state,
    print_ot_number_book_distribution, print_ot_number_genre_profile,
    print_ot_number_polarity,
    ot_number_frequency_chart, ot_number_genre_chart, ot_number_book_chart,
)

# OT-wide overview
print_ot_number_overview()
# → 6,881 number tokens · 39 books · Torah 41% of total

# Gender polarity demonstration for cardinals 3–10
print_ot_number_polarity()
# → שָׁלֹשׁ (three): masc form counts fem nouns, fem form counts masc nouns

# Books with concentrated number usage (census, chronology, temple dimensions)
print_ot_number_book_distribution()
# → Numbers 17% · 1 Chr 11% · 2 Chr 9% · Exodus 8%

# Genre distribution
print_ot_number_genre_profile()
```

**Notebook:** `notebooks/ot/numbers/01_ot_numbers.ipynb`

---

## NT Noun Morphology

`nt_noun_profile.py` provides case, gender, number, and article co-occurrence statistics
for Greek nouns across the GNT, backed by MACULA Greek syntax data.

```python
from bible_grammar import (
    nt_noun_data,
    nt_noun_case_profile, nt_noun_gender_profile, nt_noun_number_profile,
    nt_noun_case_gender, nt_noun_top_lemmas, nt_noun_lemma_case,
    nt_noun_book_distribution, nt_noun_genre_profile, nt_article_stats,
    print_nt_noun_overview, print_nt_noun_case, print_nt_noun_gender,
    print_nt_noun_case_gender, print_nt_noun_top_lemmas,
    print_nt_noun_genre_profile, print_nt_noun_book_distribution,
    print_nt_article_stats,
    nt_noun_case_chart, nt_noun_gender_chart,
    nt_noun_genre_heatmap, nt_noun_case_gender_heatmap, nt_noun_book_chart,
)

# GNT-wide case distribution
print_nt_noun_case()
# → nominative 33% · accusative 28% · genitive 25% · dative 13% · vocative 1%

# Article statistics (with/without the article)
print_nt_article_stats()

# Top 20 noun lemmas in John
print_nt_noun_top_lemmas(20, book='Jhn')

# Case × genre heatmap
print_nt_noun_genre_profile()

# Lemma × case crosstab for key theological terms
nt_noun_lemma_case(['θεός', 'κύριος', 'Χριστός', 'πνεῦμα'])
```

**Notebook:** `notebooks/nt/nouns/01_nt_noun_profile.ipynb`

---

## NT Participle Analysis

`nt_participles.py` provides tense × voice profiles, syntactic role classification
(adverbial/adjectival/substantival), genitive absolute counts, and perfect participle
statistics for the GNT.

Key teaching points (BBG Ch26–30): participles agree with their head noun in case,
gender, and number; genitive absolutes have no grammatical connection to the main
clause; perfect participles express abiding state.

```python
from bible_grammar import (
    nt_participle_data,
    nt_participle_tense_profile, nt_participle_voice_profile,
    nt_participle_tense_voice, nt_participle_role_profile,
    nt_participle_top_lemmas, nt_participle_book_distribution,
    nt_participle_genre_profile, nt_genitive_absolutes, nt_perfect_participles,
    print_nt_participle_overview, print_nt_participle_tense,
    print_nt_participle_voice, print_nt_participle_tense_voice,
    print_nt_participle_role, print_nt_participle_top_lemmas,
    print_nt_participle_genre_profile, print_nt_genitive_absolutes,
    print_nt_perfect_participles, print_nt_participle_book_distribution,
    nt_participle_tense_chart, nt_participle_genre_heatmap, nt_participle_book_chart,
)

# GNT-wide overview
print_nt_participle_overview()

# Tense distribution for the whole GNT
print_nt_participle_tense()
# → present 49.2% · aorist 39.1% · perfect 6.4% · future 0.1%

# Tense × voice crosstab in Romans
print_nt_participle_tense_voice(book='Rom')

# Syntactic role classification (adverbial/adjectival/substantival)
print_nt_participle_role()

# Genitive absolutes — no grammatical connection to the main clause
print_nt_genitive_absolutes()
# → concentrated in Matthew (Acts 27%) and Luke (24%)

# Perfect participles (abiding state)
print_nt_perfect_participles(20)

# Genre comparison (Gospels / Acts / Pauline / General)
print_nt_participle_genre_profile()
```

**Notebook:** `notebooks/nt/participles/01_nt_participle_analysis.ipynb`

---

## NT Mood Usage

`nt_moods.py` analyses the three non-indicative moods taught in BBG Ch31–33:
subjunctive, infinitive, and imperative — covering construction types,
tense profiles, and genre comparison.

```python
from bible_grammar import (
    nt_mood_data, nt_mood_profile,
    nt_subjunctive_profile, nt_infinitive_profile, nt_imperative_profile,
    nt_subjunctive_constructions, nt_infinitive_constructions,
    nt_imperative_tense_comparison, nt_mood_genre_profile,
    nt_mood_book_distribution,
    print_nt_mood_overview,
    print_nt_subjunctive_profile, print_nt_infinitive_profile,
    print_nt_imperative_profile,
    print_nt_subjunctive_constructions, print_nt_infinitive_constructions,
    print_nt_imperative_tense_comparison, print_nt_mood_genre_profile,
    nt_mood_chart, nt_subjunctive_chart, nt_imperative_chart, nt_mood_genre_heatmap,
)

# All mood distribution for the GNT
print_nt_mood_overview()
# → indicative 55% · subjunctive 13% · participle 22% · infinitive 8% · imperative 6%

# Subjunctive construction types (purpose / conditional / hortatory / prohibitive)
print_nt_subjunctive_constructions()
# → ἵνα + subj: purpose/content clauses dominate (52%)
# → ἐάν + subj: conditional (24%)
# → μή + subj: prohibitive (8%)

# Infinitive construction types (complementary / articular / indirect discourse)
print_nt_infinitive_constructions()

# Imperative: present vs. aorist — key teaching distinction
print_nt_imperative_tense_comparison()
# → present imperative 55% (ongoing / habitual command)
# → aorist imperative 45% (specific / punctiliar command)

# Subjunctive profile scoped to John
print_nt_subjunctive_profile(book='Jhn')

# Genre heatmap (which genres favour which moods?)
print_nt_mood_genre_profile()
```

**Notebook:** `notebooks/nt/moods/01_nt_mood_analysis.ipynb`

---

## NT Discourse Particles

`nt_discourse.py` analyses the distribution and function of major Greek discourse
particles (καί, δέ, ὅτι, ἵνα, γάρ, οὖν, ἀλλά, μή, οὐ, εἰ) across the GNT.

```python
from bible_grammar import (
    nt_particle_frequency, nt_particle_by_book, nt_particle_genre_profile,
    nt_hina_profile, nt_hoti_profile,
    print_nt_particle_overview, print_nt_particle_frequency,
    print_nt_particle_genre_profile, print_nt_hina_profile, print_nt_hoti_profile,
    nt_particle_frequency_chart, nt_particle_genre_heatmap, nt_particle_book_chart,
)

# GNT-wide particle overview
print_nt_particle_overview()
# → καί 32.1% (coordinative) · δέ 11.8% (continuative) · ὅτι 8.4% (content/causal)

# Particle frequency scoped to Romans
print_nt_particle_frequency(book='Rom')

# Particle % by genre group (Gospels / Acts / Pauline / General)
print_nt_particle_genre_profile()

# ἵνα clause function classification (purpose / content / result / epexegetic)
print_nt_hina_profile()
# → purpose 68% · content 28% · result 3% · epexegetic 1%

# ἵνα classification in John
print_nt_hina_profile(book='Jhn')

# ὅτι function classification (recitative / causal / content)
print_nt_hoti_profile()

# Bar chart of δέ across all NT books
nt_particle_book_chart('δέ')
```

**Notebook:** `notebooks/nt/discourse/01_nt_discourse_particles.ipynb`

---

## Greek Demonstratives

`nt_demonstratives.py` analyses the 1,709 demonstrative tokens in the GNT,
covering οὗτος (this/these, 1,388), ἐκεῖνος (that/those, 244), τοιοῦτος (such, 57),
and τοσοῦτος (so great, 20).

Key teaching points (BBG Ch13): near demonstrative οὗτος vs. far demonstrative ἐκεῖνος;
three uses: attributive (article-noun-demonstrative), substantival (noun slot), predicate
(with copula).

```python
from bible_grammar import (
    nt_demo_data, nt_demo_frequency,
    nt_demo_case_profile, nt_demo_gender_profile, nt_demo_use_profile,
    nt_demo_book_distribution, nt_demo_genre_profile,
    nt_demo_near_far_comparison, nt_demo_top_cooccurrences,
    print_nt_demo_overview, print_nt_demo_frequency,
    print_nt_demo_case, print_nt_demo_gender, print_nt_demo_use,
    print_nt_demo_book_distribution, print_nt_demo_genre_profile,
    print_nt_demo_near_far,
    nt_demo_frequency_chart, nt_demo_case_chart,
    nt_demo_genre_heatmap, nt_demo_book_chart,
)

# Overall frequency
print_nt_demo_frequency()
# → οὗτος 81% · ἐκεῖνος 14% · τοιοῦτος 3% · τοσοῦτος 1%

# Case distribution for οὗτος
print_nt_demo_case(lemma='οὗτος')

# Near vs. far demonstrative by genre
print_nt_demo_near_far()
# → John: ἐκεῖνος 19% (Jesus referring to the Spirit / another person)
# → Revelation: οὗτος 97% (this beast, this vision…)

# Attributive vs. substantival usage
print_nt_demo_use()

# Most common nouns co-occurring with οὗτος in context
nt_demo_top_cooccurrences('οὗτος', n=15)
```

**Notebook:** `notebooks/nt/demonstratives/01_nt_demonstratives.ipynb`

---

## NT Coreference & Anaphora

`nt_coreference.py` tracks pronominal reference chains using the MACULA Greek NT
`referent` column (~14,471 tokens), which links pronouns and relative clauses back
to their antecedent by xml_id.

```python
from bible_grammar import (
    nt_referent_data, nt_referent_frequency,
    nt_entity_chain, nt_pronoun_referents, nt_book_entity_density,
    print_nt_referent_overview, print_nt_referent_frequency,
    print_nt_entity_chain, print_nt_pronoun_referents,
    print_nt_book_entity_density,
    nt_referent_book_chart, nt_entity_density_chart,
    KNOWN_ENTITIES,
)

# Most-referenced antecedents across the whole GNT
print_nt_referent_frequency(top_n=15)

# How often is Jesus referenced by pronoun per book?
print_nt_referent_frequency(book='Jhn', top_n=10)

# All tokens that refer to Jesus in Matthew (full coreference chain)
print_nt_entity_chain(KNOWN_ENTITIES['Jesus (Mat)'], book='Mat')

# What does αὐτός refer to in each Gospel?
print_nt_pronoun_referents('αὐτός', book='Jhn', top_n=10)

# Participant density per chapter (who appears most?)
print_nt_book_entity_density('Jhn', top_n=10)
# → Jesus: every chapter · Peter ch13–21 · Thomas ch11,14,20 …

# Pre-identified participants include:
print(list(KNOWN_ENTITIES.keys()))
# ['Jesus (Mat)', 'Jesus (Mrk)', …, 'Paul (Rom)', …, 'Peter (Jhn)',
#  'Disciples (Mat)', 'Brothers (2Co)']
```

**Notebook:** `notebooks/nt/coreference/01_nt_coreference.ipynb`

---

## OT Participant Tracking

`ot_participant.py` follows 19 pre-identified named participants (YHWH, Abraham, Moses,
David, etc.) through OT narrative: what they do as grammatical subject, what is done to
them as object, and where they appear chapter by chapter.

```python
from bible_grammar import (
    KNOWN_OT_PARTICIPANTS,
    ot_participant_data, ot_participant_subject_verbs,
    ot_participant_object_verbs, ot_participant_chain,
    ot_entity_density, ot_participant_compare,
    print_ot_participant_profile, print_ot_participant_chain,
    print_ot_participant_compare,
    ot_participant_chain_chart, ot_entity_density_chart,
)

# Pre-identified participants
print(list(KNOWN_OT_PARTICIPANTS.keys()))
# YHWH, Elohim, Abraham, Isaac, Jacob, Joseph, Moses, Aaron,
# Joshua, David, Solomon, Elijah, Isaiah, Jeremiah, Daniel,
# Ruth, Esther, Saul, Jonah

# What verbs does Abraham appear as subject of?
print_ot_participant_profile('אַבְרָהָם', book='Gen')

# What is done to Moses (as object) in Exodus?
ot_participant_object_verbs('מֹשֶׁה', book='Exo')

# Chapter-by-chapter appearance of Jacob in Genesis
print_ot_participant_chain('Gen', 'יַעֲקֹב')

# Compare subject-verb profiles of Abraham vs. Moses
print_ot_participant_compare(['אַבְרָהָם', 'מֹשֶׁה'])

# Entity co-presence density heatmap for Genesis
ot_entity_density('Gen')
```

**Notebook:** `notebooks/ot/participants/01_ot_participant_tracking.ipynb`

---

## OT Predicate-Argument Structure

`ot_predicate_args.py` exposes the MACULA Hebrew PropBank-style `frame` column —
68,207 verb tokens annotated with semantic roles A0 (agent) and A1 (patient).

```python
from bible_grammar import (
    ot_frame_data, ot_agent_verbs, ot_patient_verbs,
    ot_verb_agents, ot_verb_patients, ot_frame_pairs,
    print_ot_agent_verbs, print_ot_patient_verbs,
    print_ot_verb_agents, print_ot_verb_patients, print_ot_frame_pairs,
    ot_agent_verbs_chart, ot_patient_verbs_chart,
)

# What does YHWH (A0) do most in the Torah?
print_ot_agent_verbs('יְהוָה', book_group='Torah', top_n=20)
# → אָמַר 4,832 (said) · נָתַן 847 (gave) · צָוָה 712 (commanded) …

# What gets created/destroyed/given (A1) in Genesis?
print_ot_patient_verbs('Gen', top_n=20)

# Who are the agents (A0) of בָּרָא (bara, create)?
print_ot_verb_agents('בָּרָא')
# → exclusively divine subjects (אֱלֹהִים, יְהוָה)

# Who or what does יָצַא (go out) take as A0?
print_ot_verb_agents('יָצַא', top_n=15)

# Most common A0 → verb → A1 triples in Genesis
print_ot_frame_pairs(book='Gen', top_n=20)
```

**Notebook:** `notebooks/ot/predicate_args/01_ot_predicate_args.ipynb`

---

## OT Discourse Structure

`ot_discourse.py` provides narrative peak and episode boundary detection for OT
narrative, based on the Longacre (1983) discourse grammar model.

**Metrics:**
- **Wayyiqtol density** — narrative backbone concentration by chapter
- **Speech density** — direct speech clustering by chapter
- **Peak score** — climax detection: dense wayyiqtol + speech + rare lexis + short clauses
- **Episode boundaries** — disjunctive clauses, וַיְהִי scene-setting formulas, chain gaps

```python
from bible_grammar import (
    ot_discourse_wayyiqtol_density, ot_discourse_speech_density,
    ot_discourse_peak_score, ot_discourse_episode_boundaries,
    ot_discourse_narrative_profile,
    print_ot_discourse_overview, print_ot_wayyiqtol_density,
    print_ot_speech_density, print_ot_peak_score, print_ot_episode_boundaries,
    ot_discourse_density_chart, ot_discourse_peak_chart,
)

# Wayyiqtol density by chapter in Genesis
print_ot_wayyiqtol_density('Gen')

# Where is the narrative peak of Genesis 22?
print_ot_peak_score('Gen')
# → ch22 peak score highest — the binding of Isaac

# Episode boundaries in Ruth
print_ot_episode_boundaries('Rut')

# Chapters with most direct speech in 1 Samuel
print_ot_speech_density('1Sa')

# Full discourse overview for a book
print_ot_discourse_overview('Exo')

# Combined metrics as a dict
profile = ot_discourse_narrative_profile('Gen')
```

**Notebook:** `notebooks/ot/discourse/01_ot_discourse_structure.ipynb`

---

## Speech Act Classification

`speech_acts.py` applies a rule-based Searle (1969) speech act classifier to biblical
direct discourse for both OT Hebrew and NT Greek. Morphological and lexical cues
determine which speech act type wins.

| Type | Definition | Hebrew cues | Greek cues |
|---|---|---|---|
| **Assertive** | claims a state of affairs | predicate nominals, "I am YHWH" | εἰμί + predicate, οὗτός ἐστιν |
| **Directive** | commands/requests | imperative, cohortative, negated yiqtol | imperative, ἵνα clause |
| **Commissive** | commits to future action | שָׁבַע (swear), נָדַר (vow), כִּי | future indicative, ἐγώ + promise |
| **Expressive** | praise, lament, thanks | הָלַל, אוֹי, אֵיכָה, בָּכָה | εὐχαριστέω, δοξάζω, αἰνέω |
| **Declarative** | changes reality by utterance | בָּרַךְ (bless), אָרַר (curse), קָרָא (name) | forgiveness, naming, pronouncement |

```python
from bible_grammar import (
    SPEECH_ACT_TYPES,
    ot_speech_act_data, ot_speech_act_profile,
    nt_speech_act_data, nt_speech_act_profile,
    print_ot_speech_act_profile, print_nt_speech_act_profile,
    print_speech_act_comparison,
    speech_act_chart, speech_act_heatmap,
)

# YHWH's speech act profile in Isaiah
print_ot_speech_act_profile('יְהוָה', book='Isa')
# → directive 44% · assertive 31% · commissive 14% · declarative 8%

# Compare YHWH's speech in Isaiah vs. Jeremiah
print_speech_act_comparison(['Isa', 'Jer'], lang='OT')

# Jesus's speech acts in the Gospels
print_nt_speech_act_profile(book='Jhn')
# → assertive 38% ("I AM" sayings) · directive 30% · expressive 16%

# Which Pauline letters have most commissive (promise) content?
print_speech_act_comparison(['Rom', 'Gal', '2Co', 'Eph'], lang='NT')
```

**Notebook:** `notebooks/both/speech_acts/01_speech_act_analysis.ipynb`

---

## Information Structure

`information_structure.py` analyses clause-linking strategies, parataxis/hypotaxis
ratios, fronted elements, and postpositive particle profiles for OT Hebrew and NT Greek.

**Hebrew metrics:** parataxis ratio (wayyiqtol/waw chains), hypotaxis ratio (כִּי/אֲשֶׁר
subordination), fronted element ratio (non-verb-initial clauses), nominal clause %.

**Greek metrics:** δέ/γάρ/οὖν/μέν density per 1,000 tokens, asyndeton %, explicit
subject-pronoun %.

```python
from bible_grammar import (
    ot_information_profile, nt_information_profile,
    ot_clause_linking_comparison, nt_clause_linking_comparison,
    print_ot_information_profile, print_nt_information_profile,
    print_ot_clause_linking_comparison, print_nt_clause_linking_comparison,
    nt_clause_linking_chart, nt_information_heatmap, ot_clause_linking_chart,
)

# Is Deuteronomy more hypotactic than Genesis?
print_ot_clause_linking_comparison(['Gen', 'Deu', 'Isa', 'Psa'])
# → Deuteronomy hypotaxis 28% (legal if…then) vs. Genesis 14% (narrative)

# Which NT book uses most γάρ (Paul is dominant)?
print_nt_clause_linking_comparison(['Rom', 'Gal', 'Mrk', 'Jhn', 'Rev'])
# → Romans γάρ density 9.2 / 1k · Mark 1.1 / 1k

# Full profile for a single book
print_ot_information_profile('Gen')
print_nt_information_profile('Rom')

# NT heatmap: particle density across books
nt_information_heatmap(['Mat', 'Mrk', 'Luk', 'Jhn', 'Rom', 'Heb', 'Rev'])
```

**Notebook:** `notebooks/both/information_structure/01_information_structure.ipynb`

---

## Stylometrics & Register Analysis

`stylometrics.py` computes quantitative style metrics that capture lexical richness,
syntactic register, and morphological fingerprints for individual books or proposed
authorial units.

| Hebrew metric | Description |
|---|---|
| `ttr` | Type-token ratio (unique lemmas / total tokens) |
| `msttr` | Mean segmental TTR — fair cross-length comparison |
| `hapax_density` | Hapax tokens / total (%) |
| `wayyiqtol_density` | Narrative backbone ratio (%) |
| `inf_construct_density` | Inf. constructs per 1,000 tokens |
| `asher_density` | אֲשֶׁר relative markers per 1,000 |

| Greek metric | Description |
|---|---|
| `ttr` / `msttr` | Vocabulary richness |
| `ptc_to_finite_ratio` | Participial style marker |
| `optative_density` | Optative per 1,000 (rare; high in Luke/Acts) |
| `hina_density` | ἵνα per 1,000 tokens |
| `inf_density` | Infinitives per 1,000 |

```python
from bible_grammar import (
    book_style_profile, style_comparison, msttr,
    print_style_profile, print_style_comparison,
    style_radar_chart, style_heatmap,
)

# Full style metrics for a single book
print_style_profile('Gen', lang='H')
print_style_profile('Rom', lang='G')

# Side-by-side comparison of proposed Deutero-Isaiah
print_style_comparison(['Isa'], lang='H')   # vs. chapters 1-39 / 40-66 (split internally)

# Which Pauline letters cluster together by style?
print_style_comparison(['Rom', 'Gal', '1Co', '2Co', 'Eph', 'Col', 'Php', 'Phm'], lang='G')

# Compare Mark vs. Luke participle usage
print_style_comparison(['Mrk', 'Luk', 'Jhn', 'Act'], lang='G')

# MSTTR for a single book (window=1000 tokens)
score = msttr('Job', lang='H', window=1000)

# Visual comparison
style_radar_chart(['Rom', 'Heb', 'Rev'], lang='G')
style_heatmap(['Gen', 'Deu', 'Isa', 'Psa', 'Pro', 'Job'], lang='H')
```

**Notebook:** `notebooks/both/stylometrics/01_stylometrics.ipynb`

---

## Formulaic Language

`formulaic.py` detects and analyses fixed biblical expressions — prophetic formulas,
doxological phrases, oath/blessing/curse formulas, and epistolary greetings — using
lemma-sequence matching with optional wildcard support.

**Curated Hebrew formulas** include: כֹּה אָמַר יְהוָה (thus says YHWH), נְאֻם יְהוָה
(oracle of YHWH), דְּבַר יְהוָה (word of YHWH), and more.

**Curated Greek formulas** include: ἀμὴν λέγω ὑμῖν (truly I say to you), χάρις ὑμῖν
καὶ εἰρήνη (grace to you and peace), and more.

```python
from bible_grammar import (
    HEBREW_FORMULAS, GREEK_FORMULAS,
    ot_formula_frequency, nt_formula_frequency,
    ot_formula_search, nt_formula_search,
    formula_book_distribution, ot_formula_profile, nt_formula_profile,
    print_formula_concordance, print_formula_book_distribution,
    print_ot_formula_profile, print_nt_formula_profile,
    print_ot_top_ngrams, print_nt_top_ngrams,
    formula_book_chart, formula_chapter_chart,
)

# How often does כֹּה אָמַר יְהוָה appear and where?
print_formula_book_distribution(['כֹּה', 'אָמַר', 'יְהוָה'], lang='OT')
# → Jeremiah 159 · Ezekiel 125 · Amos 25 · Isaiah 21 …

# Where does ἀμὴν λέγω ὑμῖν cluster?
print_formula_concordance(['ἀμήν', 'λέγω', 'ὑμῖν'], lang='NT')

# Top-30 Hebrew bigrams in the Psalms
print_ot_top_ngrams(n=2, min_count=5, top_n=30)

# All curated formula profile at once
print_ot_formula_profile()
print_nt_formula_profile()

# Wildcard search: כֹּה אָמַר <any> (any speaker, not just YHWH)
ot_formula_search(['כֹּה', 'אָמַר', '*'])

# Chapter distribution of ἀμὴν λέγω ὑμῖν in John
formula_chapter_chart('Jhn', 'amen_lego', lang='NT')
```

**Notebook:** `notebooks/both/formulaic/01_formulaic_language.ipynb`

---

## Biblical Aramaic Verb Morphology

`aramaic_profile.py` analyses the ~1,800 Aramaic verb tokens in the Daniel and Ezra
sections of the MACULA Hebrew WLC dataset. Covers all Aramaic stems (Peal, Haphel,
Pael, Peil, Hithpeel, etc.) with conjugation profiles, top roots, and book comparison.

```python
from bible_grammar import (
    aramaic_data, aramaic_verb_data,
    aramaic_stem_profile, aramaic_conj_profile, aramaic_stem_conj,
    aramaic_top_roots, aramaic_book_distribution, aramaic_stem_by_book,
    print_aramaic_overview, print_aramaic_stem_profile,
    print_aramaic_conj_profile, print_aramaic_stem_conj,
    print_aramaic_top_roots, print_aramaic_book_distribution,
    aramaic_stem_chart, aramaic_conj_chart, aramaic_stem_book_chart,
)

# Overview of all Aramaic tokens
print_aramaic_overview()
# → 7,549 total Aramaic tokens (Daniel + Ezra + scattered Gen/Jer)

# Verb stem distribution
print_aramaic_stem_profile()
# → Peal 63% · Haphel 14% · Pael 12% · Peil 5% · Hithpeel 4%

# Conjugation profile (across all stems)
print_aramaic_conj_profile()
# → qatal 27% · participle active 25% · yiqtol 22% · imperative 8%

# Stem × conjugation cross-table
print_aramaic_stem_conj()

# Daniel vs. Ezra stem comparison
print_aramaic_book_distribution()

# Top 20 Aramaic roots in Daniel
print_aramaic_top_roots(20, book='Dan')
# → אָמַר 97 (say) · הֲוָה 87 (be) · מְלַךְ 51 (reign) …

# Haphel (causative) profile in detail
print_aramaic_stem_conj(stem='haphel')
```

**Notebook:** `notebooks/ot/aramaic/01_aramaic_verb_profile.ipynb`

---

## Biblical Aramaic Nominal System

`aramaic_nominal.py` covers Aramaic noun states (absolute / construct / determined),
gender, number, pronouns, prepositions, and adjectives in Daniel and Ezra.

Key teaching point (BBA Ch4–6): Biblical Aramaic nouns have three states just like
Hebrew, but the **determined state** (-ָא suffix) is by far the most common in Aramaic
prose (often >70% of noun tokens), unlike Hebrew where the definite article is separate.

```python
from bible_grammar import (
    aramaic_noun_data, aramaic_pron_data, aramaic_prep_data, aramaic_adj_data,
    aramaic_noun_state_profile, aramaic_noun_gender_profile,
    aramaic_noun_number_profile, aramaic_noun_gender_state,
    aramaic_noun_top_lemmas, aramaic_noun_state_by_book,
    aramaic_pron_type_profile, aramaic_prep_frequency,
    aramaic_class_distribution,
    print_aramaic_nominal_overview, print_aramaic_noun_state,
    print_aramaic_noun_gender, print_aramaic_noun_top_lemmas,
    print_aramaic_noun_state_by_book, print_aramaic_pron_profile,
    print_aramaic_prep_frequency,
    aramaic_noun_state_chart, aramaic_noun_state_book_chart, aramaic_prep_chart,
)

# Noun state distribution (determined state dominates in Aramaic)
print_aramaic_noun_state()
# → determined 71% · absolute 17% · construct 12%

# Daniel vs. Ezra noun state comparison
print_aramaic_noun_state_by_book()

# Top 20 Aramaic noun lemmas
print_aramaic_noun_top_lemmas(20)
# → מֶלֶךְ 180 (king) · אֱלָהּ 95 (God) · בַּר 88 (son) …

# Pronoun type profile (personal / demonstrative / interrogative)
print_aramaic_pron_profile()

# Preposition frequency
print_aramaic_prep_frequency(15)
# → לְ 28% · בְּ 22% · מִן 18% · עַל 12% · עַד 7%

# Full word class breakdown
aramaic_class_distribution()
```

**Notebook:** `notebooks/ot/aramaic/02_aramaic_nominal_profile.ipynb`

---

## Slash Commands (Claude Code Skills)

When using this project with [Claude Code](https://claude.ai/code), the following
slash commands are available:

| Command | Description |
|---|---|
| `/word-study <strongs>` | Full word study for any Hebrew or Greek root |
| `/semantic-profile <strongs>` | Unified report: lexicon + freq + morph + LXX + collocations |
| `/synonym <term1> <term2>` | Side-by-side near-synonym comparison |
| `/lxx-consistency <strongs>` | LXX rendering consistency by book |
| `/collocations <strongs>` | Statistically significant collocates (PMI / G²) |
| `/morph-chart <strongs>` | Morphological distribution chart by book |
| `/term-map <domain>` | Theological term trajectory OT→LXX→NT |
| `/phrase-search <token1> <token2>` | Consecutive phrase or proximity search |
| `/divine-names [OT\|NT\|LXX\|all]` | Divine name / christological title frequency |
| `/genre-compare [OT\|NT] [feature]` | Morphological patterns across literary genres |
| `/intertextuality <OT-ref>` | OT verse/chapter/book → NT citation network |
| `/christological-titles [scope] [filter]` | Titles Jesus used to refer to Himself across the Gospels |
| `/role-search <Strong's> [corpus] [book...]` | Verbs with given entity as grammatical subject (OT + NT) |
| `/object-search <Strong's> [corpus] [book...]` | Objects acted upon by a given entity; verbs performed on an entity |
| `/lxx-query <Strong's> [book_or_group]` | LXX word query: per-book counts, verb morphology, concordance |
| `/ot-speaker <Strong's> [book...]` | OT speech-verb tokens with given entity as subject; character dialogue breakdown |
| `/domain-search <domain> [subject] [book...]` | Louw-Nida domain query; cross-book domain profile comparison |
| `/trajectory <Strong's> [report]` | Cross-testament word trajectory OT → LXX → NT with continuity assessment |
| `/poetry verse <book> <ch>:<vs>` | Hebrew poetry cola split + parallelism classification |
| `/poetry pairs <book>` | Most frequent A/B parallel word pairs in a poetry book |
| `/poetry stats <book>` | Parallelism type distribution (synonymous/antithetic/synthetic) |
| `/poetry chiasm <book> <ch> <vs1> <vs2>` | Chiasm (A B B' A') detection across a verse range |
| `/poetry acrostic <book> <ch> <vs1> <vs2> [stanza]` | Alphabetic acrostic detection |
| `/poetry meter <book> <ch>:<vs>` | Stress/syllable count and meter type for one verse |
| `/poetry meterstats <book>` | Meter pattern distribution for an entire book |
| `/verbal-syntax forms <book> [ch]` | Verb conjugation type distribution (wayyiqtol/qatal/yiqtol/…) |
| `/verbal-syntax chains <book> <ch>` | Wayyiqtol narrative chain analysis with break-type classification |
| `/verbal-syntax inf <book>` | Infinitive construct (+ governing prep) and absolute (paronomastic) |
| `/verbal-syntax clauses <book>` | Verbal/nominal clause ratio; negation, conditional, relative counts |
| `/verbal-syntax stems <book>` | Verb stem (binyan) distribution: Qal/Niphal/Piel/Hiphil/Hitpael |
| `/verbal-syntax disj <book> [ch]` | Disjunctive (noun/subject-first) clauses with discourse function |
| `/verbal-syntax disjchains <book> <ch>` | Wayyiqtol chains annotated with disjunctive interruptions |
| `/verbal-syntax cond <book> [ch]` | Conditional clauses (אִם/לוּ/לוּלֵא) with real/irreal classification |
| `/verbal-syntax condsum <book>` | Conditional type distribution summary for a whole book |
| `/verbal-syntax rel <book> [ch]` | Relative clauses (אֲשֶׁר/שֶׁ/דִּי) with inferred subject/object/oblique role |
| `/verbal-syntax relsum <book>` | Relative clause role × verb-form × antecedent summary |
| `/verbal-syntax aspect <book1> [book2...]` | Side-by-side verb form % comparison across genres; saves PNG chart |
| `/verbal-syntax particles <book> [ch]` | Discourse particles (הִנֵּה/כִּי/וְ/לָכֵן/עַתָּה/גַּם/אַךְ) with function classification |
| `/verbal-syntax ptclsum <book>` | Discourse particle function distribution for a whole book |
| `/verbal-syntax report <book>` | Full Markdown verbal syntax report |
| `/hiphil overview` | Hiphil OT-wide statistics (9,409 tokens, 12.9% of verbs) |
| `/hiphil conj [book]` | Hiphil conjugation distribution (whole OT or one book) |
| `/hiphil roots [n]` | Top n Hiphil roots with counts and primary gloss |
| `/hiphil roottable [n]` | Root × conjugation frequency cross-table |
| `/hiphil books` | Hiphil count and % per OT book |
| `/hiphil dominant` | Roots ≥70% Hiphil — functionally Hiphil-only verbs |
| `/hiphil semantic` | Semantic function category distribution |
| `/hiphil report` | Full Markdown report + 6 PNG charts saved to output/ |
| `/export <type> [args]` | Export any analysis to HTML + CSV |
| `/lesson <lang> <textbook> <ch> <topic>` | Generate a complete BBH lesson package (README + paradigms + exercises + Anki decks) |

### Examples

```
/word-study H7307
/semantic-profile H7965
/synonym H157 H2836
/lxx-consistency H1697
/collocations H7965
/morph-chart H1696
/term-map "Covenant / Faithfulness"
/phrase-search H3068 H559
/divine-names OT
/genre-compare OT verb_stem
/intertextuality Isa 53
/christological-titles gospels filter
/role-search H3068,H0430
/role-search G2424 NT Mat Mrk Luk Jhn
/object-search H3068,H0430
/object-search G2424 NT Mat Mrk Luk Jhn
/lxx-query G1242
/lxx-query G2316 prophets
/ot-speaker H3068,H0430 Isa
/ot-speaker who Job
/domain-search 33
/domain-search 33 G2316
/domain-search compare Rom Heb Rev
/trajectory H7965
/trajectory H7307 report
/trajectory summary
/trajectory all
/poetry verse Psa 19:2
/poetry verse Pro 10:1
/poetry pairs Pro
/poetry stats Psa
/export word-study G3056
```
