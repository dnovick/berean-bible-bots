# BBA Chapter 3 — Syllabification

---

## Files

### Reference Files

*(No separate reference files for this chapter — full content is in this README.)*

### Vocabulary Decks

| File | Use |
|---|---|
| [ch3-vocab-deck.md](ch3-vocab-deck.md) | Reference list with glosses |
| [ch3-vocab-deck.txt](ch3-vocab-deck.txt) | Anki import (tab-separated) |
| [ch3-vocab-deck-fd.txt](ch3-vocab-deck-fd.txt) | Flashcards Deluxe import |

### Exercises

| Exercise | Description |
|---|---|
| [exercises/ch3-syllabification-drill/](exercises/ch3-syllabification-drill/index.md) | 20-item syllable division and accent drill — open/closed syllables, stress rules, and vowel reduction patterns |

---

*Basics of Biblical Aramaic, Van Pelt*
*Chapter 3: Syllabification*

---

## 1. Introduction

Before you can read or parse Aramaic words fluently, you need to understand how syllables work. The rules of syllabification govern which vowels can appear in which contexts, explain why vowels change (shorten, lengthen, or reduce) in different forms, and give you a framework for predicting and understanding vowel patterns across the entire language.

The Aramaic syllable system parallels Biblical Hebrew almost exactly. Students who have worked through BBH chapters 3 and 4 will find this material reinforcing rather than new.

---

## 2. Basic Syllable Rules

Every Aramaic syllable follows these principles:

1. **Every syllable begins with a consonant.** (Except at the very beginning of a word where the first consonant opens the syllable.)
2. **Every syllable contains exactly one vowel** (which may be long, short, or reduced).
3. **A syllable may be open or closed.**

| Syllable Type | Structure | Example (in transliteration) |
|---|---|---|
| Open | CV (consonant + vowel) | *ma-* in מַלְכָּא (*mal-kāʾ*) |
| Closed | CVC (consonant + vowel + consonant) | *mal-* in מַלְכָּא |

> **Key rule:** A syllable is **open** when it ends with a vowel. It is **closed** when it ends with a consonant.

---

## 3. Syllable Division Rules

To divide an Aramaic word into syllables:

1. **Identify each vowel** (every vowel = one syllable nucleus).
2. **One consonant between two vowels goes with the second vowel** — i.e., it opens the next syllable.
   - Example: *malakā* divides as *ma-la-kā*
3. **Two consonants between vowels split**: the first closes the previous syllable, the second opens the next.
   - Example: *malkāʾ* divides as *mal-kāʾ*
4. **A Dagesh Forte doubles a consonant**: treat the doubled consonant as two — the first closes the syllable, the second opens the next.
   - Example: בַּשְּׁמַיָּא (*baš-šə-may-yāʾ*): the Shin with Dagesh counts as two consonants.
5. **Silent Sheva** closes a syllable (it is not a vowel and does not open a new syllable).
6. **Vocal Sheva** opens a new syllable but counts as a very short vowel.

---

## 4. Identifying Vocal vs. Silent Sheva

The sheva (ְ) can be either vocal or silent. Use these rules:

| Rule | Sheva is... | Explanation |
|---|---|---|
| First letter of a word | Vocal | e.g., בְּ = *bə-* |
| After a long vowel | Vocal | The syllable is open; sheva carries momentum |
| After a short vowel in a closed syllable | Silent | The syllable is closed by the consonant |
| Two shevas in a row | First = Silent, Second = Vocal | The first closes, the second opens |
| Under a consonant with Dagesh Forte | Vocal | The doubled consonant opens a new syllable |
| Final consonant of a word | Silent | The word-final consonant has a silent sheva |

---

## 5. Stress (Accent)

In Biblical Aramaic (as in Hebrew), **primary stress falls on the last syllable (ultima)** in most verb and noun forms. There are exceptions — notably certain construct and prefix forms — but the default is **ultima stress**.

| Position | Name | Default? |
|---|---|---|
| Last syllable | Ultima | Yes — default for most forms |
| Second-to-last | Penultima | Some noun and verb forms |
| Third-to-last | Antepenultima | Rare; specific forms only |

---

## 6. Vowel Changes Related to Syllable Structure

Understanding syllable type explains many vowel changes in Aramaic grammar:

### 6.1 Open Syllable → Long Vowel
Vowels in **open syllables** tend to be **long** (or stay long). When a syllable becomes open (e.g., by adding a suffix), a short vowel often lengthens.

### 6.2 Closed Syllable → Short Vowel
Vowels in **closed, unaccented syllables** tend to be **short**. A long vowel in a syllable that becomes closed may shorten.

### 6.3 Propretonic Reduction
The vowel **two syllables before the stress** (*propretonic* position) often reduces to a sheva or hateph. This is the same phenomenon seen in Hebrew when words take suffixes that shift the accent forward.

| Position | Tendency |
|---|---|
| Stressed syllable (ultima) | Long vowel preferred |
| Pretonic (one before stress) | Long vowel often retained |
| Propretonic (two before stress) | Short vowel reduces to sheva |

---

## 7. Special Cases

### 7.1 Gutturals
Gutturals (א ה ח ע) cannot take Dagesh Forte (they resist doubling). When a rule would require doubling a guttural, one of two things happens:
- **Compensatory lengthening**: the preceding vowel lengthens to compensate
- **Virtual doubling**: the guttural is treated as doubled for syllable purposes, but the vowel does not lengthen (less common)

### 7.2 Aleph Quiescence
In Aramaic, Aleph (א) frequently **quiesces** (loses its consonantal force) in the middle of a word, especially at the end of a syllable. When Aleph quiesces, the preceding vowel often lengthens:
- Example: מַלְאַךְ (*malʾak*) → in some Aramaic forms, the Aleph quiesces and the *a* may lengthen

### 7.3 He Quiescence
Final ה in Aramaic (especially as a mater) is typically quiescent and does not form a new syllable. The Aleph suffix of the determined state (א) is similarly quiescent.

---

## 8. Worked Examples

### מַלְכָּא (*malkāʾ*, "the king")

| Syllable | Type | Vowel | Notes |
|---|---|---|---|
| מַל- | Closed | Patach (a) | Short vowel; closed, unstressed |
| -כָּא | Closed (final) | Qamets (ā) | Long vowel; stressed ultima; א is quiescent mater |

Division: **מַל | כָּא** → *mal-kāʾ*

---

### מַלְכִין (*malkîn*, "kings" — emphatic plural)

| Syllable | Type | Vowel | Notes |
|---|---|---|---|
| מַל- | Closed | Patach (a) | Short vowel; closed, pretonic |
| -כִין | Closed | Hireq Gadol (ī) | Long vowel; stressed ultima; Yod is mater |

Division: **מַל | כִין** → *mal-kîn*

---

### בְּיוֹם (*bəyôm*, "on the day")

| Syllable | Type | Vowel | Notes |
|---|---|---|---|
| בְּ- | Open | Vocal Sheva (ə) | Brief; opens syllable after prefix |
| -יוֹם | Closed | Holem (ō) | Long vowel; stressed; Waw is mater |

Division: **בְּ | יוֹם** → *bə-yôm*

---

## Summary

| Rule | Key Point |
|---|---|
| Syllable types | Open (CV) or closed (CVC) |
| Division rule | One consonant between vowels → goes with second syllable |
| Division rule | Two consonants → first closes, second opens |
| Dagesh Forte | = two consonants for syllable purposes |
| Default accent | Ultima (last syllable) |
| Open syllable | Favors long vowels |
| Closed unaccented | Favors short vowels |
| Propretonic | Vowel reduces to sheva |
| Guttural | No Dagesh Forte → compensatory lengthening |
| Aleph/He final | Quiescent; does not form syllable |
