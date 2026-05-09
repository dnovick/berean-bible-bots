# Notebooks Index

These notebooks demonstrate the full `bible_grammar` analysis toolkit across
the Hebrew Old Testament, Greek New Testament, and Septuagint (LXX). They cover
verb morphology, syntactic role search, speaker attribution, poetry analysis,
lexicon lookups, intertextuality, cross-testament trajectories, and more —
all backed by the MACULA Hebrew WLC and MACULA Greek Nestle1904 syntax trees.

---

## Old Testament (Hebrew)

### Lexicon

| Notebook | Description |
|---|---|
| [ot/lexicon/hapax_legomena.ipynb](ot/lexicon/hapax_legomena.ipynb) | Hapax legomena — words occurring once in the biblical text: OT and NT hapax counts by book, deep dives into Job (most OT hapaxes) and Leviticus (cultic vocabulary), NT hapaxes in Revelation, filtering by part of speech, rare words (max_count=3) |

### Verb Stems

| Notebook | Description |
|---|---|
| [ot/verbs/qal.ipynb](ot/verbs/qal.ipynb) | Qal (קַל) — base stem (~68% of all OT verbs): conjugation profile (incl. participle passive), top roots, root×conjugation heatmap, book distribution, stem comparison, dominant roots, semantic categories, full report |
| [ot/verbs/hiphil.ipynb](ot/verbs/hiphil.ipynb) | Hiphil (הִפְעִיל) — causative-active stem (BBH Ch26–27): conjugation profile, top roots, root×conjugation heatmap, book distribution, stem comparison, dominant roots, semantic categories, full report |
| [ot/verbs/niphal.ipynb](ot/verbs/niphal.ipynb) | Niphal (נִפְעַל) — reflexive/passive stem: same nine-section structure as Hiphil; covers passive, reflexive, reciprocal, middle/stative, and tolerative functions |
| [ot/verbs/hophal.ipynb](ot/verbs/hophal.ipynb) | Hophal (הָפְעַל) — causative-passive stem (BBH Ch28–29): passive of Hiphil; legal formulas (מוּת יוּמַת), physical transfer (was brought/led), speech reporting (was told); rarest of the seven stems (~419 tokens) |
| [ot/verbs/piel.ipynb](ot/verbs/piel.ipynb) | Piel (פִּעֵל) — intensive-active stem: intensive, factitive, declarative, denominative functions; top root דִּבֵּר (speak) dominates |
| [ot/verbs/pual.ipynb](ot/verbs/pual.ipynb) | Pual (פֻּעַל) — passive of Piel: passive intensive, factitive, declarative, and birth (יֻלַּד) functions |
| [ot/verbs/hithpael.ipynb](ot/verbs/hithpael.ipynb) | Hithpael (הִתְפַּעֵל) — reflexive-intensive stem: reflexive, reciprocal, iterative/frequentative, denominative; top root הִתְפַּלֵּל (pray) |
| [ot/verbs/stem_overview.ipynb](ot/verbs/stem_overview.ipynb) | Consolidated stem statistics: OT stem totals, Torah grouped bar, Niphal perfects by book, Greek tense×voice heatmap, Aorist passives, ad-hoc query examples, CSV export |

### Syntax & Verbal Analysis

| Notebook | Description |
|---|---|
| [ot/syntax/verbal_syntax.ipynb](ot/syntax/verbal_syntax.ipynb) | Hebrew verbal syntax: verb form profiles (wayyiqtol/qatal/yiqtol), wayyiqtol narrative chains, infinitive usage, clause type profiles, stem distribution, disjunctive clauses, conditional clauses, relative clauses, aspect comparison across genres |
| [ot/syntax/poetry.ipynb](ot/syntax/poetry.ipynb) | Hebrew poetry analysis: cola splitting (Etnahta-based), parallel word pairs, parallelism type statistics (synonymous/antithetic/synthetic), chiasm detection, acrostic detection (Lamentations, Psalms), meter analysis (qinah 3+2) |
| [ot/syntax/prepositions.ipynb](ot/syntax/prepositions.ipynb) | Hebrew preposition analysis: governing prepositions on infinitive constructs, preposition distribution by book |

### Speaker & Role Analysis

| Notebook | Description |
|---|---|
| [ot/speakers/speaker_attribution.ipynb](ot/speakers/speaker_attribution.ipynb) | OT speaker attribution: who speaks in each book, divine speech by book, YHWH speech verse refs, speaker report generation; discourse particle tagging (הִנֵּה, כִּי, לָכֵן, etc.) with cross-book כִּי comparison |
| [ot/speakers/syntactic_roles_ot.ipynb](ot/speakers/syntactic_roles_ot.ipynb) | OT syntactic roles: loading OT syntax data (load_syntax_ot), wayyiqtol in Genesis, Aramaic sections; what YHWH+Elohim does (subject_verbs), what YHWH acts upon (object_verbs), who does bara (create), role charts and reports |

---

## New Testament (Greek)

### Syntax & Roles

| Notebook | Description |
|---|---|
| [nt/syntax/syntactic_roles_nt.ipynb](nt/syntax/syntactic_roles_nt.ipynb) | NT syntactic roles: loading NT syntax data (load_syntax), Jesus speaking verses (MACULA + allowlists), what Theos does in NT, what Jesus does in Gospels, object/argument search, syntactic role charts |
| [nt/syntax/prepositions.ipynb](nt/syntax/prepositions.ipynb) | Greek preposition analysis: preposition distribution in the NT, governing constructions |

### Discourse

*(No notebooks yet — add NT discourse particle analysis here when ready.)*

---

## Cross-Testament

### Survey

| Notebook | Description |
|---|---|
| [both/survey/data_exploration.ipynb](both/survey/data_exploration.ipynb) | Initial data exploration: corpus sizes, token distributions, available columns |
| [both/survey/book_profiles.ipynb](both/survey/book_profiles.ipynb) | Per-book profiles: verb stem breakdown, tense distributions, genre classification |
| [both/survey/christological_titles.ipynb](both/survey/christological_titles.ipynb) | Christological title frequency in the Gospels: unfiltered vs. speaker-filtered counts; title chart; I AM sayings; Son of Man sayings |
| [both/survey/divine_names.ipynb](both/survey/divine_names.ipynb) | Divine names and christological titles: OT (YHWH/Elohim/Adonai/Yah/Shaddai/El) and NT (Theos/Kyrios/Iesous/Christos/Pater/Pneuma) frequency by book and canonical section, stacked bar charts, full report |
| [both/survey/genre_compare.ipynb](both/survey/genre_compare.ipynb) | Genre comparison — morphological patterns by literary section: OT verb stem/conjugation/POS by Torah/Historical/Wisdom/Prophets; NT verb tense/voice/mood by Gospels/Pauline/General; heatmaps; full report |

### Lexicon

| Notebook | Description |
|---|---|
| [both/lexicon/word_study.ipynb](both/lexicon/word_study.ipynb) | Word study API: OT and NT concordance, semantic range, usage statistics |
| [both/lexicon/concordance.ipynb](both/lexicon/concordance.ipynb) | Concordance generation for Hebrew and Greek words across both corpora |
| [both/lexicon/language_analysis.ipynb](both/lexicon/language_analysis.ipynb) | Cross-language analysis: lexicon API (TBESH/TBESG), LXX consistency, domain search |
| [both/lexicon/morph_distribution.ipynb](both/lexicon/morph_distribution.ipynb) | Morphological distribution — how a root's forms spread across books: Hebrew (dabar/amar/bara stem profiles), Greek (lego/pisteuo tense×voice, logos case distribution); stacked bar charts; print helper |
| [both/lexicon/collocation_and_phrase.ipynb](both/lexicon/collocation_and_phrase.ipynb) | Collocations and phrase search: PMI/G² collocation statistics for ruach/hesed/logos/pistis; phrase search (dabar YHWH, kyrios Iesous); wildcard patterns; proximity search (ruach within 5 of Elohim) |

### Intertextuality

| Notebook | Description |
|---|---|
| [both/intertextuality/lxx_analysis.ipynb](both/intertextuality/lxx_analysis.ipynb) | LXX as a queryable corpus: load/query, key theological words (diatheke, eirene, theos), verb morphology, word distribution, frequency tables, OT→LXX→NT pipeline (lxx_alignment) |
| [both/intertextuality/theological_trajectories.ipynb](both/intertextuality/theological_trajectories.ipynb) | Cross-testament trajectories: print_trajectory for shalom/berith/ruach; starting from Greek (agape); trajectory reports; 14 pre-built theological term reports (bara, berith, ruach, shalom, tsedeq, hesed, yeshua, kavod, ahav, emunah, torah, padah, kaphar, qadosh) |
| [both/intertextuality/nt_quotations.ipynb](both/intertextuality/nt_quotations.ipynb) | NT quotations from the OT: detecting explicit citations and allusions |
| [both/intertextuality/parallel_passage.ipynb](both/intertextuality/parallel_passage.ipynb) | Synoptic parallel passage comparison |


---

## Developer / QA

| Notebook | Description |
|---|---|
| [dev/test_lowfat_integrity.ipynb](dev/test_lowfat_integrity.ipynb) | Data integrity tests for the MACULA lowfat XML corpus: token counts, column completeness, subjref coverage |
| [dev/advanced_analysis_retired.ipynb](dev/advanced_analysis_retired.ipynb) | Retired experimental analyses (kept for reference) |

---

## Path Conventions

All notebooks use `sys.path.insert(0, '<depth>/src')` to locate the `bible_grammar` package:

| Location | sys.path depth |
|---|---|
| `notebooks/ot/verbs/` | `'../../../src'` |
| `notebooks/ot/syntax/` | `'../../../src'` |
| `notebooks/ot/speakers/` | `'../../../src'` |
| `notebooks/ot/lexicon/` | `'../../../src'` |
| `notebooks/nt/syntax/` | `'../../../src'` |
| `notebooks/nt/discourse/` | `'../../../src'` |
| `notebooks/both/survey/` | `'../../../src'` |
| `notebooks/both/lexicon/` | `'../../../src'` |
| `notebooks/both/intertextuality/` | `'../../../src'` |
| `notebooks/both/syntax/` | `'../../../src'` |
| `notebooks/both/verbs/` | `'../../../src'` |
| `notebooks/dev/` | `'../../src'` |

## Output Paths

Charts are saved to `output/charts/<corpus>/<category>/`.
Reports are saved to `output/reports/<corpus>/<category>/`.
Exports (CSV) are saved to `output/exports/`.
All paths are relative to the repository root.
