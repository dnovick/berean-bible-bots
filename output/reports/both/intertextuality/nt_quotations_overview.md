# NT Quotations of the OT — Overview

*Build script: [scripts/both/intertextuality/build_nt_quotations_overview.py](../../../../scripts/both/intertextuality/build_nt_quotations_overview.py)*

---

*Generated from OpenBible.info cross-reference data (CC-BY) via scrollmapper.*  
*Vote scores reflect community consensus: higher = stronger connection.*

---

## NT Books by OT Reference Density (votes ≥ 25)

| NT Book | Total Refs | Unique NT Verses | Unique OT Verses | Top OT Source |
|---------|-----------|-----------------|-----------------|---------------|
| Mat | 246 | 44 | 33 | Psa |
| Jhn | 148 | 40 | 37 | Isa |
| Rom | 131 | 33 | 40 | Psa |
| Heb | 127 | 20 | 34 | Psa |
| Luk | 96 | 34 | 27 | Psa |
| 2Co | 90 | 15 | 32 | Isa |
| Eph | 76 | 18 | 31 | Isa |
| Jas | 59 | 14 | 26 | Pro |
| 1Co | 58 | 18 | 25 | Psa |
| Rev | 57 | 16 | 22 | Isa |
| 1Pe | 55 | 13 | 25 | Psa |
| Php | 43 | 7 | 23 | Psa |
| Act | 42 | 21 | 25 | Psa |
| Mrk | 34 | 17 | 18 | Isa |
| Col | 23 | 12 | 17 | Psa |
| Gal | 23 | 9 | 16 | Pro |

---

## Highest-Confidence NT→OT Pairs (votes ≥ 100)

| NT Ref | OT Ref | Votes |
|--------|--------|-------|
| Rom 8:29 | Jer 1:5 | 1143 |
| Php 4:13 | Isa 41:10 | 905 |
| Php 4:13 | Isa 40:29 | 498 |
| Mat 24:35 | Isa 40:8 | 421 |
| 2Co 5:17 | Ezk 36:26 | 383 |
| Php 4:6 | Pro 3:5 | 353 |
| Mat 4:4 | Deu 8:3 | 349 |
| 2Co 6:16 | Exo 29:45 | 340 |
| Heb 8:10 | Ezk 36:26 | 321 |
| Rom 8:28 | Gen 50:20 | 320 |
| Mat 6:33 | Psa 34:9 | 312 |
| Heb 13:6 | Psa 118:6 | 299 |
| 1Co 2:9 | Isa 64:4 | 298 |
| 1Pe 5:7 | Psa 55:22 | 295 |
| Jhn 1:1 | Gen 1:1 | 276 |

---

## Example Three-Way Comparison: Matt 4:4 → Deut 8:3

**NT (Matthew 4:4 Greek):**
> Ὁ δὲ ἀποκριθεὶς εἶπεν· γέγραπται· οὐκ ἐπ᾽ ἄρτῳ μόνῳ ζήσεται ὁ ἄνθρωπος, ἀλλ᾽ ἐπὶ παντὶ ῥήματι ἐκπορευομένῳ διὰ στόματος θεοῦ.

**OT (Deuteronomy 8:3 Hebrew MT):**
> וַֽיְעַנְּךָ וַיַּרְעִבֶךָ וַיַּאֲכִלְךָ אֶת הַמָּן ... כִּי לֹא עַל הַלֶּחֶם לְבַדּוֹ יִחְיֶה הָאָדָם כִּי עַל כָּל מוֹצָא פִי יְהוָה יִחְיֶה הָאָדָם

**LXX (Deuteronomy 8:3 Greek):**
> καὶ ἐκάκωσέν σε καὶ ἐλιμαγχόνησέν σε καὶ ἐψώμισέν σε τὸ μαννα ... ὅτι οὐκ ἐπ᾽ ἄρτῳ μόνῳ ζήσεται ὁ ἄνθρωπος ἀλλ᾽ ἐπὶ παντὶ ῥήματι τῷ ἐκπορευομένῳ διὰ στόματος θεοῦ ζήσεται ὁ ἄνθρωπος

**Observation:** Matthew's citation follows the LXX almost verbatim (παντὶ ῥήματι ἐκπορευομένῳ διὰ στόματος θεοῦ), consistent with the NT's general preference for the LXX in OT quotations.

---

## How to Use

```python
from bible_grammar.quotations import nt_quotations, quotation_table, quotation_summary, verse_comparison

# Summary: OT reference density per NT book
quotation_summary(min_votes=25)

# All high-confidence NT→OT quotations
nt_quotations(min_votes=100)

# References in Hebrews
nt_quotations(nt_book='Heb', min_votes=50)

# References to Isaiah from Paul's letters
nt_quotations(nt_book=['Rom','Gal','Eph','1Co','2Co'], ot_book='Isa', min_votes=25)

# Three-way text comparison for a specific verse
quotation_table('Heb', 1, 5, min_votes=5)

# Word-level structured data
verse_comparison('Mat', 4, 4, min_votes=50)
```

See `notebooks/04_nt_quotations.ipynb` for full interactive examples.
