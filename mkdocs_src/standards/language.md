# Language and Display Standards

This document specifies conventions for displaying biblical language text (Hebrew, Aramaic, Greek) and for selecting source texts and translations.

## Contents

- [No Transliterations](#no-transliterations)
- [Table Format](#table-format)
- [RTL Text and Bidi Rendering](#rtl-text-and-bidi-rendering)
- [NT Text Tradition](#nt-text-tradition)
- [BBH Consonant Names](#bbh-consonant-names)
- [BBH Vowel Names](#bbh-vowel-names)

---

## No Transliterations

**Never include transliteration columns or inline transliterations** for Hebrew, Aramaic, or Greek in any report, table, lesson, chart, flashcard deck, or PDF. Show the native script only.

This applies to all output surfaces: Markdown files, HTML exercises, PDFs, Matplotlib chart labels, and Anki decks.

---

## Table Format

Always render data tables as **GitHub-Flavored Markdown tables**. Never use ASCII art (`+---+---+`) or Python `print()` output formatted for a terminal.

```markdown
| Word | Count | Books |
|---|---|---|
| צוּם | 58 | Psalms, Isaiah … |
```

---

## RTL Text and Bidi Rendering

### In HTML

Apply `direction:rtl; unicode-bidi:embed` to any element containing Hebrew, Aramaic, or Greek text displayed right-to-left.

**Never put a verse range and Hebrew/Aramaic text on the same line.** RTL reordering will reverse the display order. Put the verse reference in its own `<td>` or on a separate line:

```html
<!-- Wrong: -->
<td>Gen 1:1 בְּרֵאשִׁית</td>

<!-- Right: -->
<td>Gen 1:1</td><td dir="rtl">בְּרֵאשִׁית</td>
```

### In Matplotlib

Pass the **entire mixed-direction string** to `get_display()` from `python-bidi`. Never split out the Hebrew fragment, apply `get_display()` to it alone, and concatenate:

```python
# Wrong:
title = "Distribution of " + get_display("צוּם") + " by Book"

# Right:
title = get_display("Distribution of צוּם by Book")
```

Always start Matplotlib title strings with LTR text so bidi base direction is LTR.

---

## NT Text Tradition

| | Default | Label required for deviations |
|---|---|---|
| Greek text | Byzantine / Textus Receptus (STEPBible TAGNT) | Yes — label inline at point of citation |
| English translation | KJV | Yes — label inline (e.g. "ESV:") |

Examples of labeled deviations:
- `(NA28) Ἰησοῦς Χριστός` — when citing the critical text
- `ESV: "in Christ Jesus"` — when quoting a non-KJV translation

---

## BBH Consonant Names

Always use the exact Pratico & Van Pelt (BBH) spellings in all exercises, lessons, flashcard decks, and PDFs. Never use variant spellings.

| Letter | BBH Name | Letter | BBH Name |
|---|---|---|---|
| א | Alef | נ | Nun |
| ב | Bet | ס | Samek |
| ג | Gimel | ע | Ayin |
| ד | Dalet | פ | Pe |
| ה | He | צ | Tsade |
| ו | Waw | ק | Qof |
| ז | Zayin | ר | Resh |
| ח | Ḥet | שׁ | Shin |
| ט | Tet | שׂ | Sin |
| י | Yod | ת | Taw |
| כ | Kaf | | |
| ל | Lamed | | |
| מ | Mem | | |

**Key spelling changes from common alternatives:**

| Common | BBH (required) |
|---|---|
| Aleph | Alef |
| Beth | Bet |
| Chet / Het | Ḥet |
| Teth | Tet |
| Kaph | Kaf |
| Samekh | Samek |
| Qoph | Qof |
| Tav | Taw |

---

## BBH Vowel Names

| Symbol | BBH Name | Symbol | BBH Name |
|---|---|---|---|
| בָּ | Qamets | בַּ | Pathach |
| בֵּ | Tsere | בֶּ | Seghol |
| בֹּ | Holem | בִּ | Hireq |
| | | בָּ (closed, unaccented) | Qamets Hatuf |
| | | בֻּ | Qibbuts |
| בּוּ | Shureq | | |
| בּוֹ | Holem Waw | | |
| בֵּי | Tsere Yod | | |
| בִּי | Hireq Yod | | |
| בָּה | Qamets He | בֹּה | Holem He |
| בֵּה | Tsere He | בֶּה | Seghol He |
| מְ | Shewa | | |
| מֲ | Hateph Pathach | מֱ | Hateph Seghol |
| מֳ | Hateph Qamets | | |

**Key spelling changes from common alternatives:**

| Common | BBH (required) |
|---|---|
| Patah | Pathach |
| Hatef (prefix) | Hateph |
| Holem Vav | Holem Waw |
| Sheva | Shewa |
