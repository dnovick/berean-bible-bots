# Suffix Parsing

*Chapter 9 — Hebrew Pronominal Suffixes*

[Full screen](ch9-suffix-parsing.html){.md-button}  [Markdown](ch9-suffix-parsing.md){.md-button}  [Print (PDF)](ch9-suffix-parsing.pdf){.md-button}

<style>

  body { font-family: Georgia, serif;    color: #222; line-height: 1.6; }
  h1 { font-size: 1.4em; border-bottom: 2px solid #444; padding-bottom: 0.3em; }
  h2 { font-size: 1.15em; margin-top: 1.8em; color: #333; }
  h3 { font-size: 1em; margin-top: 1.2em; color: #555; font-style: italic; }
  p { margin: 0.5em 0; }
  .hebrew-item { font-size: 1.8em; direction: rtl; unicode-bidi: embed; font-family: "SBL Hebrew", "Ezra SIL", "Times New Roman", serif; }
  .hebrew-small { font-size: 1.3em; direction: rtl; unicode-bidi: embed; font-family: "SBL Hebrew", "Ezra SIL", "Times New Roman", serif; }
  table { border-collapse: collapse; width: 100%; margin: 0.8em 0 1.2em; font-size: 0.92em; }
  th { background: #eee; border: 1px solid #ccc; padding: 6px 10px; text-align: left; }
  td { border: 1px solid #ccc; padding: 5px 9px; vertical-align: middle; }
  td.num { width: 3%; text-align: center; font-weight: bold; color: #555; }
  td.heb-cell { width: 14%; }
  input.parse-field { width: 96%; border: none; border-bottom: 1px solid #aaa; background: transparent; font-size: 0.88em; padding: 2px 3px; font-family: inherit; }
  input.parse-field:focus { outline: none; border-bottom: 2px solid #5b7dc8; }
  .answer-row { display: none; background: #eaf5ea; }
  .answer-row td { border-top: none; color: #1a5c1a; font-size: 0.88em; padding: 5px 9px; }
  .answer-row.visible { display: table-row; }
  .reveal-btn { font-size: 0.78em; padding: 2px 7px; background: #ddeeff; border: 1px solid #99b; border-radius: 3px; cursor: pointer; white-space: nowrap; }
  .reveal-btn:hover { background: #c5deff; }
  .controls { margin: 1.2em 0 1.6em; display: flex; gap: 0.7em; flex-wrap: wrap; }
  .controls button { padding: 6px 16px; border: 1px solid #aaa; border-radius: 4px; background: #f0f0f0; cursor: pointer; font-size: 0.92em; }
  .controls button:hover { background: #ddd; }
  .note-box { background: #fffbe6; border: 1px solid #e0c84b; border-radius: 4px; padding: 0.7em 1em; margin: 1em 0; font-size: 0.9em; }
  .section-label { background: #e8edf8; border-left: 4px solid #5b7dc8; padding: 0.4em 0.9em; margin: 1.5em 0 0.5em; font-weight: bold; font-size: 0.95em; border-radius: 0 3px 3px 0; }
  .reflection { margin-top: 1.8em; padding: 0.9em 1.2em; background: #f0f5ff; border-radius: 4px; border: 1px solid #b0c4e8; }
  .reflection ol { margin: 0.5em 0; padding-left: 1.5em; }
  .reflection li { margin-bottom: 0.6em; }
  .parsing-notes { margin-top: 1.8em; padding: 0.8em 1.2em; background: #f8f5ee; border-radius: 4px; border: 1px solid #d4c48a; }
  .parsing-notes h2 { margin-top: 0.2em; }
  .parsing-notes ul { margin: 0.3em 0; padding-left: 1.4em; }
  .parsing-notes li { margin-bottom: 0.4em; }
  @media print {
    .controls, .reveal-btn { display: none !important; }
    .answer-row { display: none !important; }
    input.parse-field { border: none; border-bottom: 1px solid #999; }
    .note-box { border: 1px solid #ccc; background: #fff; }
  }

</style>

<h1>Chapter 9 — Hebrew Pronominal Suffix Parsing Drill</h1>
<p><strong>Topic:</strong> Pronominal Suffixes on Nouns, Prepositions, and the Direct Object Marker &nbsp;|&nbsp; <strong>BBH Chapter 9</strong></p>

<p><strong>Instructions:</strong> For each Hebrew form, fill in: (1) Base Word — the lexical/absolute form of the underlying noun, preposition, or particle; (2) Suffix — the suffix element only; (3) Parse — Person–Gender–Number of the suffix; (4) Translation — the full translated phrase. Click <strong>▶ Answer</strong> to reveal the key for that item.</p>

<div class="controls">
  <button onclick="showAll()">Show All Answers</button>
  <button onclick="hideAll()">Hide All Answers</button>
  <button onclick="clearAll()">Clear All Inputs</button>
</div>

<!-- ============================================================ -->
<!-- SECTION 1: Nouns with Suffixes (#1–10) -->
<!-- ============================================================ -->

<div class="section-label">Items 1–10 &nbsp;·&nbsp; Nouns with Pronominal Suffixes</div>

<table>
  <tr>
    <th>#</th>
    <th>Hebrew</th>
    <th>Base Word</th>
    <th>Suffix</th>
    <th>Parse (PGN)</th>
    <th>Translation</th>
    <th></th>
  </tr>

  <!-- Item 1 -->
  <tr id="r1">
    <td class="num">1</td>
    <td class="heb-cell"><span class="hebrew-item">סוּסוֹ</span></td>
    <td><input class="parse-field" placeholder="base word"></td>
    <td><input class="parse-field" placeholder="suffix"></td>
    <td><input class="parse-field" placeholder="PGN"></td>
    <td><input class="parse-field" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('a1',this)">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="a1">
    <td colspan="7">✓ <strong>Base:</strong> סוּס (horse, ms) &nbsp;|&nbsp; <strong>Suffix:</strong> וֹ &nbsp;|&nbsp; <strong>Parse:</strong> 3ms &nbsp;|&nbsp; <strong>Translation:</strong> his horse &nbsp;·&nbsp; <em>The Holem (וֹ) at the end of an otherwise complete noun-stem is the 3ms possessive suffix — one of the most common morphological elements in the OT.</em></td>
  </tr>

  <!-- Item 2 -->
  <tr id="r2">
    <td class="num">2</td>
    <td class="heb-cell"><span class="hebrew-item">דְּבָרִי</span></td>
    <td><input class="parse-field" placeholder="base word"></td>
    <td><input class="parse-field" placeholder="suffix"></td>
    <td><input class="parse-field" placeholder="PGN"></td>
    <td><input class="parse-field" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('a2',this)">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="a2">
    <td colspan="7">✓ <strong>Base:</strong> דָּבָר (word, ms) &nbsp;|&nbsp; <strong>Suffix:</strong> ִי &nbsp;|&nbsp; <strong>Parse:</strong> 1cs &nbsp;|&nbsp; <strong>Translation:</strong> my word &nbsp;·&nbsp; <em>The absolute דָּבָר has two Qamets vowels; before the 1cs suffix ִי, both reduce (Shewa + Patach). Standard vowel-reduction pattern when the accent shifts to the suffix.</em></td>
  </tr>

  <!-- Item 3 -->
  <tr id="r3">
    <td class="num">3</td>
    <td class="heb-cell"><span class="hebrew-item">מַלְכְּכֶם</span></td>
    <td><input class="parse-field" placeholder="base word"></td>
    <td><input class="parse-field" placeholder="suffix"></td>
    <td><input class="parse-field" placeholder="PGN"></td>
    <td><input class="parse-field" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('a3',this)">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="a3">
    <td colspan="7">✓ <strong>Base:</strong> מֶלֶךְ (king, ms) &nbsp;|&nbsp; <strong>Suffix:</strong> כֶם &nbsp;|&nbsp; <strong>Parse:</strong> 2mp &nbsp;|&nbsp; <strong>Translation:</strong> your (mp) king &nbsp;·&nbsp; <em>מֶלֶךְ reduces to מַלְכּ- before Type 1 suffixes. Note the Dagesh Forte in the כּ before the suffix.</em></td>
  </tr>

  <!-- Item 4 -->
  <tr id="r4">
    <td class="num">4</td>
    <td class="heb-cell"><span class="hebrew-item">אָחִיהָ</span></td>
    <td><input class="parse-field" placeholder="base word"></td>
    <td><input class="parse-field" placeholder="suffix"></td>
    <td><input class="parse-field" placeholder="PGN"></td>
    <td><input class="parse-field" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('a4',this)">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="a4">
    <td colspan="7">✓ <strong>Base:</strong> אָח (brother, ms) &nbsp;|&nbsp; <strong>Suffix:</strong> הָ &nbsp;|&nbsp; <strong>Parse:</strong> 3fs &nbsp;|&nbsp; <strong>Translation:</strong> her brother &nbsp;·&nbsp; <em>אָח is irregular; it takes the form אָחִי- before suffixes (like the plural stem אַחִים). The 3fs suffix הָ (Qamets + He) then follows.</em></td>
  </tr>

  <!-- Item 5 -->
  <tr id="r5">
    <td class="num">5</td>
    <td class="heb-cell"><span class="hebrew-item">בֵּיתְךָ</span></td>
    <td><input class="parse-field" placeholder="base word"></td>
    <td><input class="parse-field" placeholder="suffix"></td>
    <td><input class="parse-field" placeholder="PGN"></td>
    <td><input class="parse-field" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('a5',this)">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="a5">
    <td colspan="7">✓ <strong>Base:</strong> בַּיִת (house, ms) &nbsp;|&nbsp; <strong>Suffix:</strong> ְךָ &nbsp;|&nbsp; <strong>Parse:</strong> 2ms &nbsp;|&nbsp; <strong>Translation:</strong> your (ms) house &nbsp;·&nbsp; <em>בַּיִת shifts to בֵּית- before Type 1 suffixes. The 2ms suffix ְךָ attaches with a silent Shewa under the kaf.</em></td>
  </tr>

  <!-- Item 6 -->
  <tr id="r6">
    <td class="num">6</td>
    <td class="heb-cell"><span class="hebrew-item">עַמֵּנוּ</span></td>
    <td><input class="parse-field" placeholder="base word"></td>
    <td><input class="parse-field" placeholder="suffix"></td>
    <td><input class="parse-field" placeholder="PGN"></td>
    <td><input class="parse-field" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('a6',this)">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="a6">
    <td colspan="7">✓ <strong>Base:</strong> עַם (people, ms) &nbsp;|&nbsp; <strong>Suffix:</strong> ֵנוּ &nbsp;|&nbsp; <strong>Parse:</strong> 1cp &nbsp;|&nbsp; <strong>Translation:</strong> our people &nbsp;·&nbsp; <em>The final מ of עַם doubles (Dagesh Forte) before the suffix. Compare עִמָּנוּ אֵל ("God with us," Immanuel), which uses the same doubling pattern on the preposition עִם.</em></td>
  </tr>

  <!-- Item 7 -->
  <tr id="r7">
    <td class="num">7</td>
    <td class="heb-cell"><span class="hebrew-item">אֲדֹנֵיכֶם</span></td>
    <td><input class="parse-field" placeholder="base word"></td>
    <td><input class="parse-field" placeholder="suffix"></td>
    <td><input class="parse-field" placeholder="PGN"></td>
    <td><input class="parse-field" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('a7',this)">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="a7">
    <td colspan="7">✓ <strong>Base:</strong> אָדוֹן (lord/master, ms) &nbsp;|&nbsp; <strong>Suffix:</strong> ֵיכֶם &nbsp;|&nbsp; <strong>Parse:</strong> 2mp &nbsp;|&nbsp; <strong>Translation:</strong> your (mp) lord/masters &nbsp;·&nbsp; <em>The Type 2 suffix ֵיכֶם is used here. The base אֲדֹנֵי- is the construct plural form used with suffixes ("my lords" → אֲדֹנַי). This is a "plural of majesty" / dignity form common with titles of authority.</em></td>
  </tr>

  <!-- Item 8 -->
  <tr id="r8">
    <td class="num">8</td>
    <td class="heb-cell"><span class="hebrew-item">בְּנָהּ</span></td>
    <td><input class="parse-field" placeholder="base word"></td>
    <td><input class="parse-field" placeholder="suffix"></td>
    <td><input class="parse-field" placeholder="PGN"></td>
    <td><input class="parse-field" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('a8',this)">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="a8">
    <td colspan="7">✓ <strong>Base:</strong> בֵּן (son, ms) &nbsp;|&nbsp; <strong>Suffix:</strong> הָ (with He mappiq: ָהּ) &nbsp;|&nbsp; <strong>Parse:</strong> 3fs &nbsp;|&nbsp; <strong>Translation:</strong> her son &nbsp;·&nbsp; <em>בֵּן reduces to בְּנ- before suffixes. The 3fs suffix appears as ָהּ (Qamets + He with mappiq dot). The mappiq dot shows the He is a consonant, not a vowel letter — it marks 3fs possession.</em></td>
  </tr>

  <!-- Item 9 -->
  <tr id="r9">
    <td class="num">9</td>
    <td class="heb-cell"><span class="hebrew-item">שְׁמֵיהֶם</span></td>
    <td><input class="parse-field" placeholder="base word"></td>
    <td><input class="parse-field" placeholder="suffix"></td>
    <td><input class="parse-field" placeholder="PGN"></td>
    <td><input class="parse-field" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('a9',this)">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="a9">
    <td colspan="7">✓ <strong>Base:</strong> שָׁמַיִם (heavens/sky, mp) &nbsp;|&nbsp; <strong>Suffix:</strong> ֵיהֶם &nbsp;|&nbsp; <strong>Parse:</strong> 3mp &nbsp;|&nbsp; <strong>Translation:</strong> their (m) heavens &nbsp;·&nbsp; <em>שָׁמַיִם is an inherently plural (or dual) noun. It takes Type 2 suffixes. The base reduces to שְׁמֵי- before Type 2 suffixes.</em></td>
  </tr>

  <!-- Item 10 -->
  <tr id="r10">
    <td class="num">10</td>
    <td class="heb-cell"><span class="hebrew-item">אַרְצָם</span></td>
    <td><input class="parse-field" placeholder="base word"></td>
    <td><input class="parse-field" placeholder="suffix"></td>
    <td><input class="parse-field" placeholder="PGN"></td>
    <td><input class="parse-field" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('a10',this)">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="a10">
    <td colspan="7">✓ <strong>Base:</strong> אֶרֶץ (land/earth, fs) &nbsp;|&nbsp; <strong>Suffix:</strong> ָם &nbsp;|&nbsp; <strong>Parse:</strong> 3mp &nbsp;|&nbsp; <strong>Translation:</strong> their (m) land &nbsp;·&nbsp; <em>אֶרֶץ reduces to אַרְצ- before Type 1 suffixes. The 3mp suffix ָם is the short form (alongside the fuller form הֶם). Context distinguishes ָם (suffix) from ָם elsewhere.</em></td>
  </tr>
</table>

<!-- ============================================================ -->
<!-- SECTION 2: Prepositions with Suffixes (#11–20) -->
<!-- ============================================================ -->

<div class="section-label">Items 11–20 &nbsp;·&nbsp; Prepositions with Pronominal Suffixes</div>

<div class="note-box"><strong>Note:</strong> Prepositions typically take Type 2 (plural-style) suffix forms. Each preposition has its own vowel pattern before the suffix attaches — learn each paradigm individually. The identity of the suffix element itself (וֹ, ִי, ְךָ, etc.) remains constant across prepositions.</div>

<table>
  <tr>
    <th>#</th>
    <th>Hebrew</th>
    <th>Base Word</th>
    <th>Suffix</th>
    <th>Parse (PGN)</th>
    <th>Translation</th>
    <th></th>
  </tr>

  <!-- Item 11 -->
  <tr id="r11">
    <td class="num">11</td>
    <td class="heb-cell"><span class="hebrew-item">לִי</span></td>
    <td><input class="parse-field" placeholder="base word"></td>
    <td><input class="parse-field" placeholder="suffix"></td>
    <td><input class="parse-field" placeholder="PGN"></td>
    <td><input class="parse-field" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('a11',this)">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="a11">
    <td colspan="7">✓ <strong>Base:</strong> לְ (to/for) &nbsp;|&nbsp; <strong>Suffix:</strong> ִי &nbsp;|&nbsp; <strong>Parse:</strong> 1cs &nbsp;|&nbsp; <strong>Translation:</strong> to/for me &nbsp;·&nbsp; <em>לְ + 1cs = לִי (Hiriq lengthens). The Shewa of לְ does not appear in this contracted form.</em></td>
  </tr>

  <!-- Item 12 -->
  <tr id="r12">
    <td class="num">12</td>
    <td class="heb-cell"><span class="hebrew-item">לְךָ</span></td>
    <td><input class="parse-field" placeholder="base word"></td>
    <td><input class="parse-field" placeholder="suffix"></td>
    <td><input class="parse-field" placeholder="PGN"></td>
    <td><input class="parse-field" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('a12',this)">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="a12">
    <td colspan="7">✓ <strong>Base:</strong> לְ (to/for) &nbsp;|&nbsp; <strong>Suffix:</strong> ְךָ &nbsp;|&nbsp; <strong>Parse:</strong> 2ms &nbsp;|&nbsp; <strong>Translation:</strong> to/for you (ms) &nbsp;·&nbsp; <em>לְ + 2ms = לְךָ (Shewa under the lamed retained). The kaf carries a Qamets (ָ) — compare the 2fs לָךְ where the kaf has a final silent shewa.</em></td>
  </tr>

  <!-- Item 13 -->
  <tr id="r13">
    <td class="num">13</td>
    <td class="heb-cell"><span class="hebrew-item">לָהּ</span></td>
    <td><input class="parse-field" placeholder="base word"></td>
    <td><input class="parse-field" placeholder="suffix"></td>
    <td><input class="parse-field" placeholder="PGN"></td>
    <td><input class="parse-field" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('a13',this)">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="a13">
    <td colspan="7">✓ <strong>Base:</strong> לְ (to/for) &nbsp;|&nbsp; <strong>Suffix:</strong> הָ (He mappiq: ָהּ) &nbsp;|&nbsp; <strong>Parse:</strong> 3fs &nbsp;|&nbsp; <strong>Translation:</strong> to/for her &nbsp;·&nbsp; <em>לְ + 3fs = לָהּ. The lamed takes a Qamets (ָ), and the He is pronounced (mappiq dot). This form is extremely frequent in narrative Hebrew.</em></td>
  </tr>

  <!-- Item 14 -->
  <tr id="r14">
    <td class="num">14</td>
    <td class="heb-cell"><span class="hebrew-item">לָנוּ</span></td>
    <td><input class="parse-field" placeholder="base word"></td>
    <td><input class="parse-field" placeholder="suffix"></td>
    <td><input class="parse-field" placeholder="PGN"></td>
    <td><input class="parse-field" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('a14',this)">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="a14">
    <td colspan="7">✓ <strong>Base:</strong> לְ (to/for) &nbsp;|&nbsp; <strong>Suffix:</strong> ֵנוּ → here ָנוּ &nbsp;|&nbsp; <strong>Parse:</strong> 1cp &nbsp;|&nbsp; <strong>Translation:</strong> to/for us &nbsp;·&nbsp; <em>לְ + 1cp = לָנוּ. The Qamets under the lamed (ָ) is characteristic of 1cp and 3p suffixes on לְ. "Unto us a child is born" (Isaiah 9:5) — לָנוּ יֻלַּד.</em></td>
  </tr>

  <!-- Item 15 -->
  <tr id="r15">
    <td class="num">15</td>
    <td class="heb-cell"><span class="hebrew-item">לָכֶם</span></td>
    <td><input class="parse-field" placeholder="base word"></td>
    <td><input class="parse-field" placeholder="suffix"></td>
    <td><input class="parse-field" placeholder="PGN"></td>
    <td><input class="parse-field" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('a15',this)">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="a15">
    <td colspan="7">✓ <strong>Base:</strong> לְ (to/for) &nbsp;|&nbsp; <strong>Suffix:</strong> כֶם &nbsp;|&nbsp; <strong>Parse:</strong> 2mp &nbsp;|&nbsp; <strong>Translation:</strong> to/for you (mp) &nbsp;·&nbsp; <em>לְ + 2mp = לָכֶם. Lamed takes Qamets (ָ). This is the same suffix element כֶם seen on nouns (מַלְכְּכֶם, item 3), showing that the suffix paradigm is consistent across different word types.</em></td>
  </tr>

  <!-- Item 16 -->
  <tr id="r16">
    <td class="num">16</td>
    <td class="heb-cell"><span class="hebrew-item">בָּהּ</span></td>
    <td><input class="parse-field" placeholder="base word"></td>
    <td><input class="parse-field" placeholder="suffix"></td>
    <td><input class="parse-field" placeholder="PGN"></td>
    <td><input class="parse-field" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('a16',this)">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="a16">
    <td colspan="7">✓ <strong>Base:</strong> בְּ (in/at/with) &nbsp;|&nbsp; <strong>Suffix:</strong> הָ (He mappiq: ָהּ) &nbsp;|&nbsp; <strong>Parse:</strong> 3fs &nbsp;|&nbsp; <strong>Translation:</strong> in/with her (or: in it, referring to a fs noun) &nbsp;·&nbsp; <em>בְּ + 3fs = בָּהּ. The bet takes a Qamets (ָ) before 3fs. Compare לָהּ (item 13) — the suffix ָהּ is identical; only the preposition differs.</em></td>
  </tr>

  <!-- Item 17 -->
  <tr id="r17">
    <td class="num">17</td>
    <td class="heb-cell"><span class="hebrew-item">בָּם</span></td>
    <td><input class="parse-field" placeholder="base word"></td>
    <td><input class="parse-field" placeholder="suffix"></td>
    <td><input class="parse-field" placeholder="PGN"></td>
    <td><input class="parse-field" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('a17',this)">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="a17">
    <td colspan="7">✓ <strong>Base:</strong> בְּ (in/at/with) &nbsp;|&nbsp; <strong>Suffix:</strong> ָם &nbsp;|&nbsp; <strong>Parse:</strong> 3mp &nbsp;|&nbsp; <strong>Translation:</strong> in/with them (m) &nbsp;·&nbsp; <em>בְּ + 3mp = בָּם (short form) or בָּהֶם (fuller form). Both are attested; בָּם is more common in poetry. The bet takes Qamets before 3mp as well.</em></td>
  </tr>

  <!-- Item 18 -->
  <tr id="r18">
    <td class="num">18</td>
    <td class="heb-cell"><span class="hebrew-item">עִמִּי</span></td>
    <td><input class="parse-field" placeholder="base word"></td>
    <td><input class="parse-field" placeholder="suffix"></td>
    <td><input class="parse-field" placeholder="PGN"></td>
    <td><input class="parse-field" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('a18',this)">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="a18">
    <td colspan="7">✓ <strong>Base:</strong> עִם (with, together with) &nbsp;|&nbsp; <strong>Suffix:</strong> ִי &nbsp;|&nbsp; <strong>Parse:</strong> 1cs &nbsp;|&nbsp; <strong>Translation:</strong> with me &nbsp;·&nbsp; <em>עִם + 1cs = עִמִּי. The mem doubles (Dagesh Forte) before the suffix — this is characteristic of עִם with suffixes. Compare Immanuel: עִמָּנוּ אֵל, "God with us" (עִם + 1cp with Qamets).</em></td>
  </tr>

  <!-- Item 19 -->
  <tr id="r19">
    <td class="num">19</td>
    <td class="heb-cell"><span class="hebrew-item">אֵלֶיךָ</span></td>
    <td><input class="parse-field" placeholder="base word"></td>
    <td><input class="parse-field" placeholder="suffix"></td>
    <td><input class="parse-field" placeholder="PGN"></td>
    <td><input class="parse-field" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('a19',this)">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="a19">
    <td colspan="7">✓ <strong>Base:</strong> אֶל (to/toward) &nbsp;|&nbsp; <strong>Suffix:</strong> ְךָ &nbsp;|&nbsp; <strong>Parse:</strong> 2ms &nbsp;|&nbsp; <strong>Translation:</strong> to/toward you (ms) &nbsp;·&nbsp; <em>אֶל + suffixes uses the extended form אֵלֵי- (Tsere + yod). This yod is the Type 2 connector. The base expands before every suffix: אֵלַי (to me), אֵלֶיךָ (to you ms), אֵלָיו (to him), etc.</em></td>
  </tr>

  <!-- Item 20 -->
  <tr id="r20">
    <td class="num">20</td>
    <td class="heb-cell"><span class="hebrew-item">עָלָיו</span></td>
    <td><input class="parse-field" placeholder="base word"></td>
    <td><input class="parse-field" placeholder="suffix"></td>
    <td><input class="parse-field" placeholder="PGN"></td>
    <td><input class="parse-field" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('a20',this)">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="a20">
    <td colspan="7">✓ <strong>Base:</strong> עַל (upon/over/concerning) &nbsp;|&nbsp; <strong>Suffix:</strong> ָיו &nbsp;|&nbsp; <strong>Parse:</strong> 3ms &nbsp;|&nbsp; <strong>Translation:</strong> upon/over him (or: on it) &nbsp;·&nbsp; <em>עַל + 3ms = עָלָיו. The Type 2 3ms suffix is ָיו (Qamets + yod + vav). The base עַל → עָלָי- before this suffix. עָלָיו is extremely common in narrative and legal texts.</em></td>
  </tr>
</table>

<!-- ============================================================ -->
<!-- SECTION 3: Direct Object Marker with Suffixes (#21–25) -->
<!-- ============================================================ -->

<div class="section-label">Items 21–25 &nbsp;·&nbsp; Direct Object Marker (אֵת) with Pronominal Suffixes</div>

<div class="note-box"><strong>Note:</strong> When the direct object marker אֵת takes suffixes, the vowel shifts from Tsere (ֵ) to Holem (ֹ): אֹת- appears before most suffixes. This suffixed form expresses the pronoun as a direct object ("me, you, him, her, us, them"). The Holem is your diagnostic clue.</div>

<table>
  <tr>
    <th>#</th>
    <th>Hebrew</th>
    <th>Base Word</th>
    <th>Suffix</th>
    <th>Parse (PGN)</th>
    <th>Translation</th>
    <th></th>
  </tr>

  <!-- Item 21 -->
  <tr id="r21">
    <td class="num">21</td>
    <td class="heb-cell"><span class="hebrew-item">אֹתִי</span></td>
    <td><input class="parse-field" placeholder="base word"></td>
    <td><input class="parse-field" placeholder="suffix"></td>
    <td><input class="parse-field" placeholder="PGN"></td>
    <td><input class="parse-field" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('a21',this)">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="a21">
    <td colspan="7">✓ <strong>Base:</strong> אֵת (DOM — direct object marker) &nbsp;|&nbsp; <strong>Suffix:</strong> ִי &nbsp;|&nbsp; <strong>Parse:</strong> 1cs &nbsp;|&nbsp; <strong>Translation:</strong> me (as direct object) &nbsp;·&nbsp; <em>אֵת + 1cs = אֹתִי. The Tsere shifts to Holem. E.g., בָּרַךְ אֹתִי — "he blessed me." Very common in prayers and narratives.</em></td>
  </tr>

  <!-- Item 22 -->
  <tr id="r22">
    <td class="num">22</td>
    <td class="heb-cell"><span class="hebrew-item">אֹתוֹ</span></td>
    <td><input class="parse-field" placeholder="base word"></td>
    <td><input class="parse-field" placeholder="suffix"></td>
    <td><input class="parse-field" placeholder="PGN"></td>
    <td><input class="parse-field" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('a22',this)">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="a22">
    <td colspan="7">✓ <strong>Base:</strong> אֵת (DOM) &nbsp;|&nbsp; <strong>Suffix:</strong> וֹ &nbsp;|&nbsp; <strong>Parse:</strong> 3ms &nbsp;|&nbsp; <strong>Translation:</strong> him (as direct object) &nbsp;·&nbsp; <em>אֵת + 3ms = אֹתוֹ. Holem vowel in base + 3ms suffix וֹ. Among the most common DOM forms in the OT. E.g., וַיִּשְׁמַע אֱלֹהִים אֹתוֹ — "and God heard him."</em></td>
  </tr>

  <!-- Item 23 -->
  <tr id="r23">
    <td class="num">23</td>
    <td class="heb-cell"><span class="hebrew-item">אֹתָהּ</span></td>
    <td><input class="parse-field" placeholder="base word"></td>
    <td><input class="parse-field" placeholder="suffix"></td>
    <td><input class="parse-field" placeholder="PGN"></td>
    <td><input class="parse-field" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('a23',this)">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="a23">
    <td colspan="7">✓ <strong>Base:</strong> אֵת (DOM) &nbsp;|&nbsp; <strong>Suffix:</strong> הָ (He mappiq: ָהּ) &nbsp;|&nbsp; <strong>Parse:</strong> 3fs &nbsp;|&nbsp; <strong>Translation:</strong> her (as direct object) &nbsp;·&nbsp; <em>אֵת + 3fs = אֹתָהּ. The Qamets + He mappiq marks 3fs. E.g., אָהַב אֹתָהּ — "he loved her."</em></td>
  </tr>

  <!-- Item 24 -->
  <tr id="r24">
    <td class="num">24</td>
    <td class="heb-cell"><span class="hebrew-item">אֹתָנוּ</span></td>
    <td><input class="parse-field" placeholder="base word"></td>
    <td><input class="parse-field" placeholder="suffix"></td>
    <td><input class="parse-field" placeholder="PGN"></td>
    <td><input class="parse-field" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('a24',this)">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="a24">
    <td colspan="7">✓ <strong>Base:</strong> אֵת (DOM) &nbsp;|&nbsp; <strong>Suffix:</strong> ָנוּ &nbsp;|&nbsp; <strong>Parse:</strong> 1cp &nbsp;|&nbsp; <strong>Translation:</strong> us (as direct object) &nbsp;·&nbsp; <em>אֵת + 1cp = אֹתָנוּ. Note: on the DOM the 1cp suffix is ָנוּ (Qamets + nun + vav), not ֵנוּ (Tsere + nun + vav) as on some prepositions. E.g., שָׁלַח אֹתָנוּ — "he sent us."</em></td>
  </tr>

  <!-- Item 25 -->
  <tr id="r25">
    <td class="num">25</td>
    <td class="heb-cell"><span class="hebrew-item">אֹתָם</span></td>
    <td><input class="parse-field" placeholder="base word"></td>
    <td><input class="parse-field" placeholder="suffix"></td>
    <td><input class="parse-field" placeholder="PGN"></td>
    <td><input class="parse-field" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('a25',this)">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="a25">
    <td colspan="7">✓ <strong>Base:</strong> אֵת (DOM) &nbsp;|&nbsp; <strong>Suffix:</strong> ָם &nbsp;|&nbsp; <strong>Parse:</strong> 3mp &nbsp;|&nbsp; <strong>Translation:</strong> them (m, as direct object) &nbsp;·&nbsp; <em>אֵת + 3mp = אֹתָם. Short 3mp suffix ָם on the Holem base. E.g., וַיִּבְרָא אֱלֹהִים אֹתָם (Gen 1:27) — "and God created them."</em></td>
  </tr>
</table>

<!-- ============================================================ -->
<!-- Parsing Notes -->
<!-- ============================================================ -->

<div class="parsing-notes">
<h2>Quick Reference: Identifying Suffixes in Context</h2>
<p>Follow this four-step procedure for any unfamiliar suffixed form:</p>
<ol>
  <li><strong>Identify the base word type.</strong> Is it a preposition, a noun, or the DOM אֵת?</li>
  <li><strong>Strip the suffix.</strong> Working right to left, peel off the suffix element. What remains should be a recognizable (reduced) form of the base.</li>
  <li><strong>Parse the base independently.</strong> Identify the noun (gender, number, state) or preposition.</li>
  <li><strong>Match the suffix to the paradigm.</strong> Check both Type 1 and Type 2 columns if uncertain.</li>
</ol>
<p><strong>Common pitfalls:</strong></p>
<ul>
  <li>3ms suffix וֹ vs. plural ending ּוֹת: ּוֹת is always followed by ת; the suffix וֹ never has a following consonant.</li>
  <li>2ms ְךָ vs. 2fs ֵךְ: 2ms has Qamets under the kaf (ָ); 2fs has a final silent shewa and no vowel letter after the kaf.</li>
  <li>3fs suffix ָהּ vs. the definite article הַ: the suffix ָהּ is always word-final; the article is always word-initial.</li>
  <li>Type 1 vs. Type 2: if you see a yod (י) before the suffix element, it is almost certainly Type 2.</li>
</ul>
</div>

<!-- ============================================================ -->
<!-- Reflection Questions -->
<!-- ============================================================ -->

<div class="reflection">
<h2>Reflection Questions</h2>
<ol>
  <li>In items 7 (אֲדֹנֵיכֶם) and 9 (שְׁמֵיהֶם), the suffix set used is Type 2 (with a yod connector). Both base nouns are plural or plural in form. How does this confirm the rule that Type 2 suffixes attach to plural nouns?</li>
  <li>Compare לָהּ (item 13) with בָּהּ (item 16). Both end in ָהּ (Qamets + He mappiq). What is different between them, and how do you know which preposition each is built on?</li>
  <li>Items 21–25 all use אֵת (DOM) + suffix. What vowel change occurs in אֵת when a suffix attaches, and why does recognizing this change matter for reading Hebrew narrative?</li>
</ol>
</div>

<script>
function toggle(id, btn) {
  var row = document.getElementById(id);
  if (row.classList.contains('visible')) {
    row.classList.remove('visible');
    btn.textContent = '▶ Answer';
  } else {
    row.classList.add('visible');
    btn.textContent = '▼ Hide';
  }
}

function showAll() {
  var rows = document.querySelectorAll('.answer-row');
  var btns = document.querySelectorAll('.reveal-btn');
  rows.forEach(function(r) { r.classList.add('visible'); });
  btns.forEach(function(b) { b.textContent = '▼ Hide'; });
}

function hideAll() {
  var rows = document.querySelectorAll('.answer-row');
  var btns = document.querySelectorAll('.reveal-btn');
  rows.forEach(function(r) { r.classList.remove('visible'); });
  btns.forEach(function(b) { b.textContent = '▶ Answer'; });
}

function clearAll() {
  var inputs = document.querySelectorAll('input.parse-field');
  inputs.forEach(function(i) { i.value = ''; });
}
</script>

