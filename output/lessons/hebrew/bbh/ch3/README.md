# BBH Chapter 3 — Syllabification and Pronunciation

---

## Files

### Exercises

| Exercise | Description |
|---|---|
| [exercises/ch3-syllable-division/](exercises/ch3-syllable-division/README.md) | 20-word syllable division drill — divide words, label syllable types, mark stress, identify Qamets Hatuf |

### Flashcards

| File | Format | Description |
|---|---|---|
| [ch3-vocab-deck.md](ch3-vocab-deck.md) | Markdown | Vocabulary deck — 20 common nouns (family, creation, society) with alternate forms and OT frequency |
| [ch3-vocab-deck.txt](ch3-vocab-deck.txt) | Anki import | Vocabulary deck — tab-separated, ready for Anki File → Import (20 cards) |
| [ch3-vocab-deck-fd.txt](ch3-vocab-deck-fd.txt) | Flashcards Deluxe | Vocabulary deck — tab-separated, ready for Flashcards Deluxe import (20 cards) |

---

*Basics of Biblical Hebrew, Pratico & Van Pelt*
*Chapter 3: Syllabification and Pronunciation*

---

## 1. Introduction

Syllabification is not a separate topic from grammar — it **is** grammar. In Biblical Hebrew, vowel length and syllable type are bound together by rule: open syllables typically take long vowels, closed syllables typically take short vowels. When word structure changes — by adding a suffix, constructing a genitive chain, or prefixing a preposition — stress shifts, and predictable vowel changes follow. You can only track those changes if you can identify syllable boundaries.

This is why BBH introduces syllabification before paradigms. Every vowel shift you will encounter in Chapters 13–35 (and throughout your translation career) traces back to the rules in this chapter.

**Practical consequences:**
- A qamets (ָ) and a qamets hatuf look **identical** on the page. Only syllable analysis tells you which one you are reading and therefore what vowel sound and word form you have.
- Vowel reduction chains (propretonic reduction, pretonic lengthening) are the engine of almost all paradigm variation. Understanding them now prevents dozens of "exceptions" later.
- Guttural behavior — why gutturals take hateph shevas, why Dagesh Forte is blocked — makes sense only against the background of syllable rules.

---

## 2. The Two Syllable Types

Every Hebrew syllable is one of two basic types:

| Type | Structure | Vowel Length | Example | Notes |
|---|---|---|---|---|
| **Open** | CV (ends in a vowel) | Typically **long** | דָּ in דָּבָר | The vowel has no following consonant to "close" it; it remains in the open air |
| **Closed** | CVC (ends in a consonant) | Typically **short** | דַּ in דַּרְכֶּךָ | The following consonant "closes" the syllable; long vowels in closed syllables are usually under stress |

**Important qualifications:**

- "Typically long in open / typically short in closed" is the default. There are exceptions:
  - A **closed, accented** syllable can carry a long vowel (e.g., ēt in בֵּית — the syllable is closed by the final taw, but the tsere is long because it is accented).
  - A **half-open** syllable (ending in a Dagesh Forte) has a short vowel even though the consonant appears to "close" one syllable and "open" the next simultaneously — see Rule 3 below.
- The **shewa** (ְ) is neither a full vowel nor purely the absence of a vowel. A **vocal shewa** (ְ under a consonant that opens a syllable) counts as an ultra-short vowel. A **silent shewa** marks the closure of the syllable before it.

---

## 3. Rules for Syllable Division

Apply these rules in order when you encounter an unfamiliar word.

### Rule 1 — Every syllable begins with a consonant

Hebrew has no vowel-initial syllables. Even when a word appears to begin with a vowel (like אֱלֹהִים), the initial consonant is aleph — it is silent, but it is there, and it opens the syllable.

> **Implication:** You never divide between a consonant and the vowel that follows it. A syllable break always falls *before* a consonant, never *after* a vowel alone.

### Rule 2 — Vocal shewa opens a new syllable; silent shewa closes the preceding syllable

The same sign (ְ) can function two ways:

| Function | Position | Effect |
|---|---|---|
| **Vocal shewa** | Under a consonant that opens a syllable | The consonant + shewa *begins* the next syllable |
| **Silent shewa** | Under a consonant that closes a syllable | The consonant closes the previous syllable; there is no new syllable |

**How to tell them apart:**

1. A shewa at the beginning of a word is always vocal.
2. A shewa after a long vowel (in an open syllable) is always vocal.
3. Two shevas in a row: the first is silent (closes the syllable), the second is vocal (opens the next).
4. A shewa under a Dagesh Forte consonant is always vocal.
5. A shewa at the end of a word is always silent.

**Example:** בְּרֵאשִׁית
- בְּ — vocal shewa (word-initial); opens syllable 1
- רֵא — long tsere (mater lectionis א); syllable 2 is open: רֵא
- שִׁי — hireq + yod; syllable 3 is open: שִׁי (the yod is a vowel letter)
- ת — final consonant; closes syllable 3
- Division: **בְּ-רֵא-שִׁית** (3 syllables)

### Rule 3 — Dagesh Forte doubles the consonant; it closes one syllable and opens the next

A Dagesh Forte inside a consonant indicates that consonant is **doubled**. The first instance closes the preceding syllable; the second instance opens the following syllable.

> **Mnemonic:** Think of the dagesh forte as a wall shared between two rooms — it belongs to both.

**Example:** שַׁבָּת
- שַׁ — patach; syllable 1 is closed by the doubled bet: שַׁב (closed)
- בָּ — qamets; syllable 2 is opened by the second instance of bet: בָּת (closed by final taw)
- Division: **שַׁב-בָּת** (written שַׁבָּת because the doubled consonant is written once with a dagesh)

### Rule 4 — When two consonants appear between vowels with no shewa, the first closes the syllable

If you have: vowel–C1–C2–vowel (with no shewa under C1 or C2), divide between C1 and C2.

**Example:** מַלְכֵּי
- מַ — patach; then לְ has a vocal shewa (so this is actually Rule 2 in action)
- More clearly: מֶלֶךְ — מֶ-לֶךְ; the final kaph closes the last syllable.

**Clearer example:** בַּרְזֶל (iron)
- בַּ — patach; then ר followed by ז — no shewa under ר; divide: בַּר-זֶל
- Syllable 1: **בַּר** (closed, short vowel) / Syllable 2: **זֶל** (closed, short vowel)

### Rule 5 — A word-final consonant always closes the final syllable

Every Hebrew word ends in a consonant (unless the word ends in a mater lectionis like ָה, in which case the he or he-mappiq closes it). The final consonant makes the final syllable closed.

**Example:** מֶלֶךְ
- מֶ — seghol; syllable 1 open? No — the next consonant (lamed) follows directly.
- Actually: מֶ-לֶךְ — divide between מֶ and לֶ? No: the lamed has a seghol vowel, so lamed opens syllable 2.
- Division: **מֶ-לֶךְ** — syllable 1 (מֶ) is open (ends in seghol), syllable 2 (לֶךְ) is closed by the final kaph (silent shewa).

---

### Step-by-Step Worked Examples

| Word | Division | Syllables | Notes |
|---|---|---|---|
| דָּבָר | דָּ-בָר | 2 | Both open; both long vowels (qamets) |
| שָׁמַיִם | שָׁ-מַ-יִם | 3 | שָׁ open; מַ open (short patach, then yod begins next syl.); יִם closed |
| יְרוּשָׁלַיִם | יְ-רוּ-שָׁ-לַ-יִם | 5 | Vocal shewa opens syl.1; each CV pair opens a syllable; final יִם closed |
| אֱלֹהִים | אֱ-לֹ-הִים | 3 | Hateph seghol (vocal composite) opens syl.1; לֹ open; הִים closed by final mem |
| מִשְׁפָּט | מִשׁ-פָּט | 2 | Silent shewa under shin (closes syl.1); Dagesh Forte in pe opens syl.2; final tet closes |
| נָבִיא | נָ-בִיא | 2 | נָ open; בִיא — yod is mater, aleph quiesces; syllable closes on aleph; open (aleph quiescent) |

---

## 4. Syllable Accent (Stress)

### Default: Milra (Ultimate Stress)

The great majority of Hebrew words are stressed on the **ultima** — the last syllable. This is called **milra** (מִלְרַע, "from below"). No special marking is needed; it is the default.

### Exception: Milel (Penultimate Stress)

Some words are stressed on the **penultima** — the second-to-last syllable. This is called **milel** (מִלְעֵיל, "from above"). Milel stress is marked in BHS by:
- A distinctive cantillation accent on the penultimate syllable, or
- The **Metheg** (see §5 below) placed to the left of the penultimate vowel.

**Common milel forms:**
- Many 2ms Qal perfect forms: שָׁמַ֫רְתָּ (stress on שָׁמַ, not on תָּ)
- Some nouns in construct or with suffixes
- Words before maqqef (conjunctive hyphen) lose their accent to the following word

### Cantillation Accents in BHS

The cantillation marks (טְעָמִים, *te'amim*) in a BHS text serve two functions:
1. They are **musical notation** for chanting the text in synagogue
2. They function as **syntactic punctuation** — disjunctive accents separate clauses and phrases; conjunctive accents join words within a phrase

The accent marks also indicate **stress position**. The disjunctive accents (silluq, atnah, zaqef, etc.) fall on the stressed syllable. When you see a disjunctive accent under a vowel, that vowel is in the stressed syllable.

| Accent | Symbol | Type | Position |
|---|---|---|---|
| Silluq | ֽ (vertical stroke below last word) | Disjunctive | End of verse; marks verse-final stress |
| Atnah | ֑ | Disjunctive | Major break within verse; marks mid-verse stress |
| Zaqef Qatan | ֔ | Disjunctive | Secondary break |
| Metheg | ֽ (left of vowel) | Secondary stress | Marks secondary or long vowel |

---

## 5. The Metheg

The **Metheg** (מֶתֶג, "bridle") is a small vertical stroke placed **to the left of a vowel**. It serves two related functions:

1. **Secondary stress marker:** In longer words, a syllable two or more positions before the main accent may carry secondary stress. The Metheg marks this secondary stress position.

2. **Long-vowel marker:** The Metheg can appear under a qamets (ָ) to indicate that the qamets is **long** (qamets gadol, = ā) and should **not** be read as qamets hatuf (= ŏ). This is its most practically important function for students.

**Example:** כָּל-הָאָרֶץ
- The qamets in הָ has a Metheg: הָ֮אָרֶץ — this tells you the qamets is long ā ("the"), not short ŏ.

**Rule of thumb:** If you see a qamets in a closed, unaccented syllable and are unsure whether it is qamets gadol or qamets hatuf, look for a Metheg to its left. If the Metheg is present, read it as long ā.

---

## 6. Qamets vs. Qamets Hatuf

The **qamets gadol** (ָ, long ā) and the **qamets hatuf** (ָ, short ŏ) are written with the same symbol. This is the most frequent disambiguation challenge for beginning students. The following rules resolve the ambiguity:

### Rule 1 — Open or accented syllable → Qamets Gadol (long ā)

If the syllable is open (ends in a vowel) or if it carries the main accent (even if closed), the qamets is long ā.

- דָּבָר: Both syllables have qamets. Both syllables are open and the ultima is accented → both are long ā.

### Rule 2 — Closed, unaccented syllable → Qamets Hatuf (short ŏ)

If the syllable is closed **and** unaccented, and there is no Metheg, the qamets is likely qamets hatuf.

- כָּל (all): The lamed closes the syllable; the word is often unaccented (especially before maqqef) → the qamets is qamets hatuf = ŏ. But when כֹּל appears with holem, the disambiguation is built into the spelling.

### Rule 3 — Before Metheg → Long ā

A Metheg to the left of the qamets always signals qamets gadol (even in a closed syllable).

### Summary Table

| Condition | Reading | Sound |
|---|---|---|
| Open syllable | Qamets Gadol | long ā |
| Accented closed syllable | Qamets Gadol | long ā |
| Unaccented closed syllable, no Metheg | Qamets Hatuf | short ŏ |
| Any syllable with Metheg | Qamets Gadol | long ā |
| Before Dagesh Forte (doubled consonant follows) | Usually Qamets Gadol | long ā |

> **Practical note:** Qamets Hatuf is relatively rare. The most common context is words like הָלְכוּ (they walked) where the heh-qamets stands in a closed, unaccented syllable. Lexicons and most textbooks will indicate qamets hatuf explicitly in their entries.

---

## 7. Vowel Reduction

When stress shifts, the vowels in pre-stress syllables **reduce**. This is the engine of most paradigm variation you will encounter throughout BBH.

### Two critical positions

| Position | Name | What happens |
|---|---|---|
| One syllable before stress | **Pretonic** | Long vowels often *retain* their value; reducible vowels shorten |
| Two syllables before stress | **Propretonic** | Long vowels regularly **reduce to simple vocal shewa** (ְ) |

### Why this matters

Consider the Qal Perfect paradigm (Ch13). The 3ms is קָטַל (stress on ultima, qamets under R1 in open pretonic syllable). When you add the 3cp suffix -וּ, the stress stays on the ultima but R1 is now *two* syllables before the new suffix: קָ-טְ-לוּ → the qamets reduces to shewa: קָטְלוּ.

When you add the 2mp suffix -תֶּם, R1 is propretonic: the qamets reduces to shewa and R1 gets a shewa: קְטַלְתֶּם.

### Reduction chain

```
Propretonic syllable:  long vowel → simple vocal shewa (ְ)
Pretonic syllable:     long vowel → often retained, or shortens
Tonic syllable:        fully stressed; vowel is at full length
Post-tonic syllable:   reduced (e.g., final closed syllable with short vowel)
```

### Gutturals and reduction

Gutturals (א ה ח ע) and resh cannot take a simple vocal shewa. When reduction would produce a shewa under a guttural, it takes a **composite shewa (hateph vowel)** instead:
- Hateph Patach (ֲ) — the most common, under א and ע
- Hateph Seghol (ֱ) — under א especially (e.g., אֱלֹהִים)
- Hateph Qamets (ֳ) — relatively rare

This is not an exception to reduction — it is reduction adapted for guttural phonology.

---

## 8. Guttural Exceptions

Gutturals introduce the most frequent apparent exceptions to syllable rules. The underlying logic, however, is consistent.

### Gutturals cannot take Dagesh Forte

When a rule would require doubling a guttural (Rule 3 above), the doubling is blocked. Two outcomes are possible:

| Outcome | Description | Example |
|---|---|---|
| **Compensatory lengthening** | The preceding vowel lengthens to compensate for the missing doubling | Patach → Qamets; Hireq → Tsere |
| **Virtual doubling** | The Dagesh Forte is simply omitted with no lengthening | Some contexts with resh and occasionally ayin |

### Gutturals take composite (hateph) shevas

Where a simple vocal shewa (ְ) would appear under a non-guttural, a guttural takes a composite shewa:

| Letter | Preferred hateph |
|---|---|
| א | Hateph Seghol (ֱ) most common; also Hateph Patach |
| ה | Hateph Patach (ֲ) |
| ח | Hateph Patach (ֲ) |
| ע | Hateph Patach (ֲ) |

### Gutturals prefer a-class vowels

Gutturals tend to attract patach (a-class vowels) in adjacent positions. This is why you often see patach furtive before a final guttural (e.g., רוּחַ, שָׁמַע 3fs: שָׁמְעָה → shama'ah with patach).

> **Bottom line:** When you encounter what appears to be a syllable rule violation near a guttural, ask: "Would doubling or simple shewa be expected here?" If yes, the guttural is simply adapting the rule to its phonological constraints — it is not a true exception.

---

## 9. Practical Pronunciation Checklist

Use this checklist every time you encounter a new Hebrew word:

**Step 1 — Identify the consonants**
Read right to left. Name each consonant. Note any sofit forms, begadkephat letters, and gutturals.

**Step 2 — Mark syllable boundaries**
Apply Rules 1–5 in order:
- Every syllable begins with a consonant (Rule 1)
- Vocal shewa opens a syllable; silent shewa closes the preceding one (Rule 2)
- Dagesh Forte splits between two syllables (Rule 3)
- Two consonants between vowels: divide between them (Rule 4)
- Word-final consonant closes the last syllable (Rule 5)

**Step 3 — Identify the stressed syllable**
- Default: ultima (milra)
- Check for distinctive cantillation accents or Metheg on the penultima (milel)

**Step 4 — Read each syllable's vowel**
Work left to right through the syllables (even though Hebrew writes right to left, syllables are pronounced in sequence from the beginning of the word):
- Open syllable: expect a long vowel
- Closed syllable: expect a short vowel (or a long vowel under accent)
- Shewa: vocal = ultra-short; silent = no vowel

**Step 5 — Handle special cases**
- If you see a qamets in a closed, unaccented syllable with no Metheg: read it as ŏ (qamets hatuf)
- If you see a guttural where a Dagesh Forte or simple shewa was expected: apply compensatory lengthening or hateph rules
- If a consonant looks like a begadkephat with a dot but the dot is in the wrong position: it may be a dagesh forte (inside the letter, not just the begadkephat position) — check context

**Step 6 — Pronounce left to right**
Combine syllables in order. In most academic traditions (Tiberian/Sephardic blend): long ā = "ah"; long ē = "ay"; long ō = "oh"; short ĕ = "eh"; short ĭ = "ih"; shewa = schwa ("uh") or silent.

---

## 10. Key Terms

| Term | Definition |
|---|---|
| **Open syllable** | A syllable ending in a vowel (CV); typically carries a long vowel |
| **Closed syllable** | A syllable ending in a consonant (CVC); typically carries a short vowel |
| **Vocal shewa** | A shewa (ְ) that represents an ultra-short vowel and opens a new syllable |
| **Silent shewa** | A shewa (ְ) that marks the end of a syllable with no vowel sound |
| **Dagesh Forte** | A dot inside a consonant indicating it is doubled; the doubling closes one syllable and opens the next |
| **Dagesh Lene** | A dot inside a begadkephat letter indicating its hard pronunciation; does not double the consonant |
| **Milra** | Stress on the ultima (last syllable); the default in Biblical Hebrew |
| **Milel** | Stress on the penultima (second-to-last syllable); marked by distinctive accents or Metheg |
| **Metheg** | A vertical stroke to the left of a vowel; marks secondary stress or a long qamets |
| **Qamets Gadol** | The long ā vowel; written ָ |
| **Qamets Hatuf** | The short ŏ vowel; written identically to qamets gadol (ָ); determined by syllable analysis |
| **Propretonic** | Two syllables before the stressed syllable; long vowels regularly reduce to shewa here |
| **Pretonic** | One syllable before the stressed syllable; long vowels may retain or shorten here |
| **Compensatory lengthening** | Lengthening of a vowel to compensate for a missing Dagesh Forte (blocked by a guttural) |
| **Composite shewa (hateph)** | A shewa combined with a short vowel (ֲ ֱ ֳ); appears under gutturals in place of simple vocal shewa |
| **Cantillation (te'amim)** | The system of musical/syntactic accent marks in BHS; indicate stress position and syntactic structure |

---

## 11. Practice

| Resource | Description |
|---|---|
| [Syllable Division Exercise](exercises/ch3-syllable-division/README.md) | 20 Hebrew words — divide syllables, label types (O/C), mark stress, identify any Qamets Hatuf. Answer key included. |
