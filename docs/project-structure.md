# Project Structure

```
berean-bible-bots/
├── src/bible_grammar/          # Core Python library
│   ├── query.py                # Filtered morphology + translation query API
│   ├── wordstudy.py            # Word study: lexicon + stats + LXX equivalents
│   ├── semantic_profile.py     # Unified semantic range report (lexicon+stats+collocations)
│   ├── concordance.py          # Concordance, lemma frequency, top lemmas
│   ├── stats.py                # Frequency tables, aggregation helpers
│   ├── charts.py               # Matplotlib/seaborn chart helpers
│   ├── profiles.py             # Per-book morphological profiles
│   ├── ibm_align.py            # IBM Model 1 word-level Hebrew↔LXX alignment
│   ├── lxx_consistency.py      # LXX translation consistency by book
│   ├── collocation.py          # PMI and G² collocate scoring
│   ├── morph_chart.py          # Morphological distribution charts by book
│   ├── quotations.py           # NT→OT cross-references (scrollmapper)
│   ├── quotation_align.py      # NT quotation word alignment (LXX vs MT)
│   ├── intertextuality.py      # OT verse/chapter/book → NT citation network
│   ├── termmap.py              # Theological term mapping OT→LXX→NT
│   ├── synonym.py              # Near-synonym comparison
│   ├── phrase.py               # Phrase search and proximity search
│   ├── divine_names.py         # Divine name / christological title frequency
│   ├── genre_compare.py        # Morphological patterns across literary genres
│   ├── hapax.py                # Hapax legomena analysis
│   ├── parallel.py             # Parallel passage comparison
│   ├── export.py               # HTML and CSV export for all analyses
│   ├── syntax.py               # MACULA Greek NT syntax query API (roles, subjref)
│   ├── syntax_ot.py            # MACULA Hebrew OT syntax query API (roles, LXX alignment)
│   ├── speaker.py              # NT speaker attribution (allowlists + MACULA subjref)
│   ├── lexicon.py              # TBESH/TBESG public API (lookup, search_gloss, lex_entry)
│   ├── christological_titles.py # Christological title frequency with speaker filter
│   ├── prepositions.py         # Hebrew preposition frequency, collocates, object types
│   ├── greek_prepositions.py   # Greek preposition frequency, case binding, collocates (NT + LXX)
│   ├── alignment.py            # Verse-level Hebrew↔Greek alignment
│   ├── morphology.py           # Decode Hebrew/Greek morphology codes
│   ├── reference.py            # Book metadata: names, testament, order
│   ├── db.py                   # SQLite + Parquet persistence
│   └── ingest.py               # Parse STEPBible TSV files
│
├── scripts/
│   └── build_db.py             # Build data/processed/ from scratch
│
├── notebooks/                  # Jupyter notebooks (both/ot/nt × topic)
├── output/
│   ├── reports/                # Markdown reports (both/ot/nt × topic)
│   ├── charts/                 # Generated PNG chart files (both/ot/nt × topic)
│   └── exports/                # Generated CSV exports (gitignored)
├── .claude/commands/           # Claude Code slash command skills
├── stepbible-data/             # Git submodule: STEPBible/STEPBible-Data
├── scrollmapper-data/          # Git submodule: scrollmapper/bible_databases
├── macula-greek/               # Git submodule: Clear-Bible/macula-greek (NT syntax trees)
├── macula-hebrew/              # Git submodule: Clear-Bible/macula-hebrew (OT syntax trees)
└── data/processed/             # Generated files (gitignored)
    ├── bible_grammar.db        # SQLite database
    ├── words.parquet           # Hebrew/Greek word data (STEPBible)
    ├── translations.parquet    # KJV + Vulgate verse data
    ├── word_alignment.parquet  # IBM Model 1 alignment data
    ├── macula_syntax.parquet   # MACULA Greek NT syntax (137k tokens, cached)
    └── macula_syntax_ot.parquet # MACULA Hebrew OT syntax (475k tokens, cached)
```
