# Data Sources

| Submodule | Contents | License |
|---|---|---|
| `stepbible-data/` | Hebrew OT (TAHOT, ~284k words) and Greek NT (TAGNT, ~142k words) with full morphological tagging; LXX Greek (TALXX); lexicons TBESH/TBESG; NT→OT cross-references | CC BY 4.0 — Tyndale House Cambridge |
| `scrollmapper-data/` | KJV English (24,570 verses), Latin Vulgate Clementine (24,909 verses), and Syriac Peshitta NT (7,956 verses) | MIT — scrollmapper |
| `syrnt/` | ETCBC Peshitta NT word-level morphology (109,640 words) — sp, gn, nu, ps, st, verbal stem (vs), tense/aspect (vt), Sedra root and lemma | MIT — ETCBC |
| `macula-greek/` | MACULA Greek NT (Nestle1904, 137k words) with syntax trees, semantic roles (`role`), participant referents (`subjref`/`referent`), English glosses, and Louw-Nida semantic domains | CC BY 4.0 — Clear Bible / Tyndale House |
| `macula-hebrew/` | MACULA Hebrew OT (WLC, 475k words) with syntax trees, semantic roles, LXX alignment per word (`greek`/`greekstrong`), stem, clause type (wayyiqtol/qatal/etc.), and Aramaic sections | CC BY 4.0 — Clear Bible |

## Morphological Coverage

**Hebrew/Aramaic (TAHOT):** Every word tagged with stem (Qal, Niphal, Piel, Hiphil, etc.),
conjugation (Perfect, Imperfect, Imperative, Participle, Infinitive), person, gender, number,
state (absolute/construct), and Strong's number. Aramaic words (Daniel, Ezra) are tagged
separately as `language=Aramaic`.

**Greek (TAGNT):** Every word tagged with part of speech, tense, voice, mood, person, number,
gender, case, and Strong's number.

**LXX (TALXX):** Greek Septuagint with Strong's numbers, used for Hebrew→Greek translation
alignment and NT quotation analysis.

**Lexicons:** TBESH (Hebrew) and TBESG (Greek) — Translators Brief lexicons with lemma,
transliteration, gloss, definition, and POS code for every Strong's number.

> **ESV note:** The ESV text is under copyright by Crossway and cannot be included. If you
> obtain a Crossway license, adding ESV support is straightforward — the STEPBible tagging
> file is already present in the submodule.

## Data Notes

- **Aramaic:** Daniel 2:4–7:28 and Ezra 4:8–6:18, 7:12–26 are tagged `language=Aramaic`.
- **Pronominal suffixes:** Hebrew pronominal suffixes are encoded as separate word tokens
  (own `word_num` row). When using proximity search, add ~30% to your mental window size
  to account for suffix tokens.
- **Untagged tokens:** Some morphology fields are blank for prefix tokens (conjunction ו,
  preposition ב, etc.) attached to a word where STEPBible encodes the prefix separately.
- **Versification:** TAHOT follows NRSV versification; some chapter/verse numbers differ
  from KJV (especially in Psalms and some prophetic books).
- **Strong's normalization:** The library normalizes Strong's numbers throughout —
  zero-padding (H530 ↔ H0530) and variant suffixes (H1697A → H1697) are handled
  transparently.
- **Word counts:** TAHOT ~284k words, TAGNT ~142k words, LXX ~480k words,
  KJV 24,570 verses, Vulgate Clementine 24,909 verses, Peshitta NT 7,956 verses.
- **Peshitta NT morphology:** 109,640 Syriac words via ETCBC/syrnt (Text-Fabric).
  Access via ``peshitta_query.query_peshitta()``.
- **Targumim:** Verse-level Aramaic for Onkelos (Torah), Targum Jonathan (Former &
  Latter Prophets), and Targum to Psalms. Downloaded from Sefaria — run
  ``python scripts/fetch_targum_data.py`` to populate ``data/processed/targum.parquet``.
  Access via ``targum_query.load_targum()``.
