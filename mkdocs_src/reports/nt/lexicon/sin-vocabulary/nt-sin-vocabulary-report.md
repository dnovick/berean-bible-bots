# Sin Vocabulary in the Greek New Testament

**Corpus:** Greek New Testament (TAGNT)  
**Method:** Strong's-based lemma grouping across 11 sin-vocabulary stems  
**Two metrics:** (1) sin-vocabulary words as % of total words; (2) verses containing ≥1 sin-vocabulary word as % of total verses  
<!-- Build script: scripts/nt/lexicon/build_sin_vocabulary_report.py (repo link omitted from web) -->

---

## Contents

1. [Key Observations](#key-observations)
2. [Vocabulary Scope](#vocabulary-scope)
3. [Metrics Comparison Overview](#metrics-comparison-overview)
4. [Metric 1 — Word Frequency](#metric-1--word-frequency)
   - [By Book](#by-book-word-frequency)
   - [Word Group Heatmap](#word-group-heatmap)
   - [By Corpus Section](#by-corpus-section-word-frequency)
5. [Metric 2 — Verse Coverage](#metric-2--verse-coverage)
   - [By Book](#by-book-verse-coverage)
   - [By Corpus Section](#by-corpus-section-verse-coverage)
6. [High-Density Verses](#high-density-verses)
7. [Data Tables](#data-tables)
8. [Methodological Notes](#methodological-notes)

---

## Key Observations

### Word Frequency (Metric 1)
- **1 John has the highest sin-vocabulary word density in the NT (1.41%)** — more than any Pauline letter, despite being far shorter than Romans. Its sustained focus on sin, confession, propitiation, and the nature of righteous living accounts for the concentration.
- **Romans is second (1.18%)**, reflecting Paul's systematic argument about universal sin and guilt in chapters 1–3 and 5–8.
- **The Gospels and Acts are strikingly low (0.07–0.19%)**. Jesus consistently uses narrative and parable rather than the hamartia word group.
- **Acts is the lowest in the entire NT (0.07%)** — its theological center is proclamation and the movement of the Spirit, not doctrinal elaboration of sin.
- **Revelation is near-zero (0.04%)** despite containing the NT's most intense judgment scenes. It uses *different* vocabulary — θηρίον, πόρνη, δράκων — rather than the hamartia/adikia cluster.
- **The Pauline and General Epistles converge at nearly identical word-density averages** (0.44% and 0.42%).

### Verse Coverage (Metric 2)
- **1 John has the highest verse coverage in the NT (15.2%)**: more than 1 in 6 verses explicitly uses sin-vocabulary language, confirming its unique preoccupation with the topic.
- **Romans ranks second (14.9%)** but the verse metric reveals that nearly 1 in 7 verses touches the sin-vocabulary cluster — a far more striking picture than the word metric alone suggests.
- **2 Thessalonians rises sharply (10.6%)** under the verse metric — its verses on the "man of lawlessness" (2:3–12) are long on ἀνομία vocabulary but not numerous, so the verse metric captures them better than word density.
- **The General Epistles (6.4%) now clearly outpace the Pauline Epistles (5.5%)** in verse coverage, while the two sections were nearly tied on the word metric. This suggests the General Epistles address sin in more verses but with less concentrated vocabulary per verse.
- **The Gospels remain the lowest section (2.4%)** under both metrics — sin vocabulary appears in roughly 1 in 40 Gospel verses.

---

## Vocabulary Scope

The analysis covers 11 Strong's lemma groups spanning the main Greek word families used for sin and moral failure:

| Strong's | Lemma | Gloss | Count (NT) |
|----------|-------|-------|-----------|
| G0266 | ἁμαρτία | sin (noun) | 174 |
| G0264 | ἁμαρτάνω | to sin (verb) | 43 |
| G0268 | ἁμαρτωλός | sinner | 48 |
| G0265 | ἁμάρτημα | sinful act | 5 |
| G0458 | ἀνομία | lawlessness / iniquity | 16 |
| G0459 | ἄνομος | lawless | 10 |
| G3900 | παράπτωμα | trespass / transgression | 22 |
| G3847 | παράβασις | transgression (of law) | 7 |
| G3848 | παραβάτης | transgressor | 5 |
| G0093 | ἀδικία | unrighteousness / iniquity | 25 |
| G4189 | πονηρία | wickedness / evil | 7 |

**Total occurrences:** 362 across 141,746 NT words (0.26% of NT words); found in 369 distinct verses out of 7,957 total NT verses (4.6% of NT verses).

---

## Metrics Comparison Overview

The two charts below are displayed together for easy comparison. The *shape* of the distribution is similar under both metrics, but the *scale* reveals different things: the word metric captures how intensively a book uses sin vocabulary; the verse metric captures how *broadly* across the book the topic is addressed.

![Two-metric comparison — word frequency and verse coverage by NT book](../nt-sin-vocabulary-metrics-comparison.png)

**Notable divergences between the two metrics:**

| Book | Word % | Verse % | Interpretation |
|------|:------:|:-------:|----------------|
| Romans | 1.18% | 14.9% | Very high on both — sin is a sustained, word-intensive theme |
| 2 Thessalonians | 0.60% | 10.6% | High verse coverage from ἀνομία cluster (ch. 2) but short book |
| Hebrews | 0.70% | 9.9% | Long verses dilute word density; verse coverage better reflects reach |
| Luke | 0.19% | 3.3% | Consistent with Gospels narrative pattern — sin words scattered broadly |
| Revelation | 0.04% | 1.0% | Both metrics confirm near-absence of hamartia vocabulary |

---

## Metric 1 — Word Frequency

**Definition:** (sin-vocabulary word tokens) ÷ (total word tokens in book) × 100

This metric measures how *intensively* sin vocabulary is used relative to a book's total word count. A book with many words about sin packed into a few passages will score high.

### By Book — Word Frequency

![Sin vocabulary word frequency by NT book](../nt-sin-vocabulary-by-book.png)

### Word Group Heatmap

This heatmap breaks the total sin vocabulary into five word-group clusters and shows occurrences per 1,000 words for each book × group cell.

![Sin vocabulary word group heatmap by NT book](../nt-sin-vocabulary-heatmap.png)

Key patterns:
- **ἁμαρτία** (the hamartia cluster) dominates across all sections — it is the NT's primary term for sin
- **ἀνομία** (lawlessness) appears most in Matthew (5:23), 2 Thessalonians (2:3 — "man of lawlessness"), and 1 John (3:4 — "sin is lawlessness")
- **παράπτωμα** (trespass) is concentrated in Romans and Ephesians — Paul's preferred term for the specific act of transgression (Rom 5:15–20; Eph 2:1)
- **ἀδικία** (unrighteousness) is primarily Pauline and Johannine; Romans 1:18–32 accounts for much of its concentration
- **πονηρία** (wickedness) appears scattershot — not dominant in any single book

### By Corpus Section — Word Frequency

![Sin vocabulary word density by NT corpus section](../nt-sin-vocabulary-by-section.png)

| Corpus Section | Total Words | Sin-Vocab Words | Word Frequency |
|----------------|:-----------:|:---------------:|:--------------:|
| Gospels & Acts | 85,889 | 121 | 0.14% |
| Pauline Epistles | 32,124 | 140 | 0.44% |
| General Epistles | 23,733 | 100 | 0.42% |

---

## Metric 2 — Verse Coverage

**Definition:** (verses containing ≥1 sin-vocabulary word) ÷ (total verses in book) × 100

This metric measures how *broadly* sin vocabulary is distributed across a book's verses. A book that mentions sin in many separate verses — even just once per verse — will score high regardless of how concentrated the words are.

### By Book — Verse Coverage

![Sin vocabulary verse coverage by NT book](../nt-sin-vocabulary-verses-by-book.png)

### By Corpus Section — Verse Coverage

![Sin vocabulary verse coverage by NT corpus section](../nt-sin-vocabulary-verses-by-section.png)

| Corpus Section | Total Verses | Sin-Vocab Verses | Verse Coverage |
|----------------|:------------:|:----------------:|:--------------:|
| Gospels & Acts | 4,785 | 114 | 2.4% |
| Pauline Epistles | 1,741 | 95 | 5.5% |
| General Epistles | 1,431 | 92 | 6.4% |

The General Epistles pull ahead of the Pauline Epistles under the verse metric (6.4% vs 5.5%), reversing the near-tie seen in word density. This suggests that books like Hebrews, James, 1 Peter, 1 John, and 2 Peter spread their sin vocabulary more broadly across their verses, while Pauline letters like Romans concentrate it in dense theological argument sections.

---

## High-Density Verses

The following verses contain the highest concentration of sin-vocabulary words (4 occurrences per verse):

**1 John 3:4** — πᾶς ὁ ποιῶν τὴν **ἁμαρτίαν** καὶ τὴν **ἀνομίαν** ποιεῖ, καὶ ἡ **ἁμαρτία** ἐστὶν ἡ **ἀνομία**  
*"Everyone who makes a practice of sinning also practices lawlessness; sin is lawlessness."* — the only verse in the NT that explicitly equates ἁμαρτία with ἀνομία.

**Romans 7:13** — ἵνα γένηται καθ᾽ ὑπερβολὴν **ἁμαρτωλὸς** ἡ **ἁμαρτία** διὰ τῆς ἐντολῆς… ἡ **ἁμαρτία** διὰ τῆς ἐντολῆς κατεργάζηται … **ἁμαρτία**  
*The densest single verse in Romans' treatment of the Law-sin dynamic (ch. 7).*

**1 Corinthians 9:21** — τοῖς **ἀνόμοις** ὡς **ἄνομος**, μὴ ὢν **ἄνομος** θεοῦ ἀλλ᾽ ἔννομος Χριστοῦ, ἵνα κερδάνω τοὺς **ἀνόμους**  
*Paul's "all things to all people" — 4× ἄνομος in one sentence as rhetorical wordplay, not theological elaboration.*

**1 John 5:16–17** — three sin-vocabulary words across two related verses on mortal and non-mortal sin.

---

## Data Tables

### Metric 1 — Word Frequency

| Book | Total Words | Sin Words | Word Frequency |
|------|:-----------:|:---------:|:--------------:|
| Matthew | 18,882 | 24 | 0.13% |
| Mark | 11,865 | 19 | 0.16% |
| Luke | 20,119 | 39 | 0.19% |
| John | 16,069 | 26 | 0.16% |
| Acts | 18,954 | 13 | 0.07% |
| Romans | 7,180 | 85 | 1.18% |
| 1 Corinthians | 6,986 | 18 | 0.26% |
| 2 Corinthians | 4,497 | 6 | 0.13% |
| Galatians | 2,268 | 8 | 0.35% |
| Ephesians | 2,470 | 6 | 0.24% |
| Philippians | 1,628 | 0 | 0.00% |
| Colossians | 1,631 | 4 | 0.25% |
| 1 Thessalonians | 1,502 | 1 | 0.07% |
| 2 Thessalonians | 839 | 5 | 0.60% |
| 1 Timothy | 1,623 | 7 | 0.43% |
| 2 Timothy | 1,273 | 2 | 0.16% |
| Titus | 680 | 2 | 0.29% |
| Philemon | 349 | 0 | 0.00% |
| Hebrews | 5,026 | 35 | 0.70% |
| James | 1,779 | 12 | 0.67% |
| 1 Peter | 1,729 | 8 | 0.46% |
| 2 Peter | 1,112 | 6 | 0.54% |
| 1 John | 2,191 | 31 | 1.41% |
| 2 John | 249 | 0 | 0.00% |
| 3 John | 210 | 0 | 0.00% |
| Jude | 468 | 1 | 0.21% |
| Revelation | 10,167 | 4 | 0.04% |
| **NT Total** | **141,746** | **362** | **0.26%** |

### Metric 2 — Verse Coverage

| Book | Total Verses | Sin Verses | Verse Coverage |
|------|:------------:|:----------:|:--------------:|
| Matthew | 1,071 | 23 | 2.1% |
| Mark | 678 | 18 | 2.7% |
| Luke | 1,151 | 38 | 3.3% |
| John | 878 | 22 | 2.5% |
| Acts | 1,007 | 13 | 1.3% |
| Romans | 430 | 64 | 14.9% |
| 1 Corinthians | 437 | 11 | 2.5% |
| 2 Corinthians | 255 | 5 | 2.0% |
| Galatians | 149 | 7 | 4.7% |
| Ephesians | 155 | 5 | 3.2% |
| Philippians | 102 | 0 | 0.0% |
| Colossians | 95 | 3 | 3.2% |
| 1 Thessalonians | 89 | 1 | 1.1% |
| 2 Thessalonians | 47 | 5 | 10.6% |
| 1 Timothy | 113 | 6 | 5.3% |
| 2 Timothy | 83 | 2 | 2.4% |
| Titus | 46 | 2 | 4.3% |
| Philemon | 25 | 0 | 0.0% |
| Hebrews | 303 | 30 | 9.9% |
| James | 108 | 9 | 8.3% |
| 1 Peter | 105 | 7 | 6.7% |
| 2 Peter | 61 | 6 | 9.8% |
| 1 John | 105 | 16 | 15.2% |
| 2 John | 13 | 0 | 0.0% |
| 3 John | 14 | 0 | 0.0% |
| Jude | 25 | 1 | 4.0% |
| Revelation | 404 | 4 | 1.0% |
| **NT Total** | **7,957** | **369** | **4.6%** |

---

## Methodological Notes

- **Data source:** TAGNT (The Apostolic Greek New Testament) morphological database via the `bible_grammar` query API
- **Lemma matching:** Strong's prefix matching (e.g., all forms tagged G0266 match ἁμαρτία regardless of case/number ending)
- **Metric 1 scaling:** Raw word counts divided by total word tokens per book, expressed as percentage
- **Metric 2 scaling:** A verse is counted once even if it contains multiple sin-vocabulary words; divided by total verse count per book
- **Excluded terms:** πονηρός (G4190, 79×), ὀφειλέτης (G3781), and αἰτία (G0156) were excluded to keep the analysis focused on direct sin terminology
- **Revelation caveat:** Revelation's near-zero scores under both metrics do not mean it is unconcerned with evil — it uses apocalyptic imagery (θηρίον, πόρνη, δράκων, εἴδωλον) to encode moral failure symbolically rather than lexically
- **CSV exports:** Word-frequency data in `nt-sin-vocabulary-by-book.csv`; verse-coverage data in `nt-sin-vocabulary-by-verse.csv`
