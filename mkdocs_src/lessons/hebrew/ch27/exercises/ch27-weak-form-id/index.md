# Weak Form Id

*Chapter 27 — Hiphil Weak*

[Full screen](ch27-weak-form-id.html){.md-button}  [Markdown](ch27-weak-form-id.md){.md-button}  [Print (PDF)](ch27-weak-form-id.pdf){.md-button}

<style>

  body { font-family: Georgia, serif;    color: #222; }
  h1 { font-size: 1.4em; border-bottom: 2px solid #444; padding-bottom: .4em; }
  h2 { font-size: 1.15em; margin-top: 2em; color: #444; }
  h3 { font-size: 1em; margin-top: 1.5em; color: #555; }
  .subtitle { color: #666; font-style: italic; margin-top: -.3em; }
  table { border-collapse: collapse; width: 100%; margin: 1em 0; }
  th { background: #2a4a6e; color: #fff; padding: .5em .7em; text-align: left; font-size: .85em; }
  td { border: 1px solid #ccc; padding: .4em .6em; font-size: .85em; vertical-align: top; }
  tr:nth-child(even) td { background: #f7f7f7; }
  .heb { font-size: 1.2em; direction: rtl; unicode-bidi: embed; }
  input.parse-field { width: 100%; box-sizing: border-box; font-size: .85em; padding: 3px 5px; border: 1px solid #aaa; border-radius: 3px; }
  .answer-row td { background: #f0faf0 !important; color: #2a6e2a; font-size: .82em; }
  .answer-row { display: none; }
  button.reveal-btn { font-size: .78em; padding: 2px 7px; cursor: pointer; border: 1px solid #888; border-radius: 3px; background: #fff; white-space: nowrap; }
  .controls { margin: 1em 0; display: flex; gap: .6em; flex-wrap: wrap; }
  .controls button { padding: .4em .9em; font-size: .9em; cursor: pointer; border: 1px solid #555; border-radius: 4px; background: #f0f0f0; }
  .controls button:hover { background: #ddd; }
  .legend { border: 1px solid #ccc; border-radius: 4px; padding: .6em 1em; margin: 1em 0; font-size: .88em; }
  .legend table { margin: .3em 0; }
  .legend th { background: #555; font-size: .82em; }
  .tip { background: #fffbe6; border-left: 4px solid #d4a017; padding: .5em 1em; margin: 1em 0; font-size: .88em; }
  .discussion { background: #f0f4ff; border-left: 4px solid #2a4a6e; padding: .6em 1em; margin: 1em 0; font-size: .88em; }
  ol.disc { margin: .4em 0 0 1.2em; padding: 0; }
  ol.disc li { margin-bottom: .5em; }
  .section-label { background: #e8eef8; border-left: 4px solid #2a4a6e; padding: .3em .8em; font-weight: bold; font-size: .9em; margin: 1.5em 0 .5em; }
  @media print {
    button, .controls { display: none !important; }
    input.parse-field { border: none; border-bottom: 1px solid #000; background: transparent; }
    .answer-row { display: table-row !important; }
  }

</style>

<h1>Chapter 27 — Hiphil Weak-Form Identification Drill</h1>
<p class="subtitle">BBH Chapter 27 · Hiphil Weak Verbs</p>

<p>For each form: (1) <strong>identify the weak class</strong>, (2) <strong>parse</strong> (conjugation + PGN), (3) <strong>identify the root</strong>.</p>

<div class="legend">
  <table>
    <tr><th>Class</th><th>Key diagnostic signal</th></tr>
    <tr><td><strong>I-guttural</strong></td><td>הֶ prefix (perfect); composite shewa under R1; no dagesh in R1 throughout</td></tr>
    <tr><td><strong>III-ח/ע</strong></td><td>Patach furtive before final ח/ע (open syllable); patach (not tsere) in wayyiqtol/imperative before final guttural</td></tr>
    <tr><td><strong>III-א</strong></td><td>Silent final א; chiriq-yod before silent א (perfect/imperfect/inf.); tsere before silent א (wayyiqtol/imperative)</td></tr>
    <tr><td><strong>III-ה</strong></td><td>Qamets + ה (perfect 3ms); seghol + ה (imperfect/participle); apocopated wayyiqtol (ה dropped); וֹת (inf. construct)</td></tr>
    <tr><td><strong>I-נ</strong></td><td>Dagesh forte in R2 throughout entire paradigm; root נ invisible</td></tr>
    <tr><td><strong>I-י</strong></td><td>הוֹ prefix (perfect/imperative/inf.); יוֹ/תּוֹ/אוֹ/נוֹ prefix (imperfect); וַיּוֹ (wayyiqtol); מוֹ (participle)</td></tr>
    <tr><td><strong>Biconsonantal</strong></td><td>הֵ prefix (perfect); qamets under prefix consonant (imperfect/wayyiqtol); הָ prefix (imperative/inf. construct); מֵ prefix (participle ms)</td></tr>
    <tr><td><strong>Geminate</strong></td><td>הֵ prefix (perfect); qamets under prefix (imperfect/wayyiqtol); הָ prefix (imperative/inf. construct); מֵ prefix (participle) — nearly identical to Biconsonantal; root identification (R2=R3) is the only reliable distinguisher</td></tr>
  </table>
</div>

<div class="controls">
  <button onclick="showAll()">Show All Answers</button>
  <button onclick="hideAll()">Hide All Answers</button>
  <button onclick="clearAll()">Clear All Inputs</button>
</div>

<!-- PART A -->
<h2>Part A — By Class</h2>

<div class="section-label">Group 1 — I-guttural</div>
<table>
  <tr><th>#</th><th>Form</th><th>Reference</th><th>Conjugation</th><th>PGN</th><th>Root</th><th></th></tr>

  <tr><td>1</td><td><span class="heb">הֶעֱמִיד</span></td><td>1 Kgs 7:21</td>
    <td><input class="parse-field" id="a1g"></td><td><input class="parse-field" id="a1p"></td><td><input class="parse-field" id="a1r"></td>
    <td><button class="reveal-btn" onclick="toggle('r1')">▶</button></td></tr>
  <tr class="answer-row" id="r1"><td colspan="7"><strong>Perfect · 3ms · עָמַד</strong> — he set up; seghol under הֶ + hateph-seghol under ע are the twin I-guttural markers</td></tr>

  <tr><td>2</td><td><span class="heb">וַיַּעֲמֵד</span></td><td>2 Chr 4:4</td>
    <td><input class="parse-field" id="a2g"></td><td><input class="parse-field" id="a2p"></td><td><input class="parse-field" id="a2r"></td>
    <td><button class="reveal-btn" onclick="toggle('r2')">▶</button></td></tr>
  <tr class="answer-row" id="r2"><td colspan="7"><strong>Wayyiqtol · 3ms · עָמַד</strong> — and he set it; patach prefix (standard Hiphil) + hateph-patach under ע + tsere final</td></tr>

  <tr><td>3</td><td><span class="heb">יַעֲמִיד</span></td><td>Psa 107:29</td>
    <td><input class="parse-field" id="a3g"></td><td><input class="parse-field" id="a3p"></td><td><input class="parse-field" id="a3r"></td>
    <td><button class="reveal-btn" onclick="toggle('r3')">▶</button></td></tr>
  <tr class="answer-row" id="r3"><td colspan="7"><strong>Imperfect · 3ms · עָמַד</strong> — he causes to stand still; patach prefix + composite shewa under ע; no dagesh in R1</td></tr>

  <tr><td>4</td><td><span class="heb">הַעֲמֵד</span></td><td>Num 27:19</td>
    <td><input class="parse-field" id="a4g"></td><td><input class="parse-field" id="a4p"></td><td><input class="parse-field" id="a4r"></td>
    <td><button class="reveal-btn" onclick="toggle('r4')">▶</button></td></tr>
  <tr class="answer-row" id="r4"><td colspan="7"><strong>Imperative · 2ms · עָמַד</strong> — set him before; הַ + composite shewa under ע + tsere</td></tr>

  <tr><td>5</td><td><span class="heb">מַעֲמִיד</span></td><td>Neh 4:7</td>
    <td><input class="parse-field" id="a5g"></td><td><input class="parse-field" id="a5p"></td><td><input class="parse-field" id="a5r"></td>
    <td><button class="reveal-btn" onclick="toggle('r5')">▶</button></td></tr>
  <tr class="answer-row" id="r5"><td colspan="7"><strong>Participle · ms · עָמַד</strong> — one who stations; מַ + composite shewa under ע + chiriq</td></tr>
</table>

<div class="section-label">Group 2 — III-ח/ע</div>
<table>
  <tr><th>#</th><th>Form</th><th>Reference</th><th>Conjugation</th><th>PGN</th><th>Root</th><th></th></tr>

  <tr><td>6</td><td><span class="heb">הִשְׁמִיעַ</span></td><td>Isa 48:6</td>
    <td><input class="parse-field" id="a6g"></td><td><input class="parse-field" id="a6p"></td><td><input class="parse-field" id="a6r"></td>
    <td><button class="reveal-btn" onclick="toggle('r6')">▶</button></td></tr>
  <tr class="answer-row" id="r6"><td colspan="7"><strong>Perfect · 3ms · שָׁמַע</strong> — he caused to hear; patach furtive written below the chiriq-yod, before final ע</td></tr>

  <tr><td>7</td><td><span class="heb">וַיַּשְׁלַח</span></td><td>Gen 3:23</td>
    <td><input class="parse-field" id="a7g"></td><td><input class="parse-field" id="a7p"></td><td><input class="parse-field" id="a7r"></td>
    <td><button class="reveal-btn" onclick="toggle('r7')">▶</button></td></tr>
  <tr class="answer-row" id="r7"><td colspan="7"><strong>Wayyiqtol · 3ms · שָׁלַח</strong> — and he sent out; patach (not tsere) before final ח — guttural forces vowel lowering in the shortened wayyiqtol form</td></tr>

  <tr><td>8</td><td><span class="heb">יַשְׁמִיעַ</span></td><td>Isa 42:2</td>
    <td><input class="parse-field" id="a8g"></td><td><input class="parse-field" id="a8p"></td><td><input class="parse-field" id="a8r"></td>
    <td><button class="reveal-btn" onclick="toggle('r8')">▶</button></td></tr>
  <tr class="answer-row" id="r8"><td colspan="7"><strong>Imperfect · 3ms · שָׁמַע</strong> — he will cause to hear; patach furtive before final ע in open syllable</td></tr>

  <tr><td>9</td><td><span class="heb">הַשְׁמַע</span></td><td>Deu 4:10</td>
    <td><input class="parse-field" id="a9g"></td><td><input class="parse-field" id="a9p"></td><td><input class="parse-field" id="a9r"></td>
    <td><button class="reveal-btn" onclick="toggle('r9')">▶</button></td></tr>
  <tr class="answer-row" id="r9"><td colspan="7"><strong>Imperative · 2ms · שָׁמַע</strong> — make them hear; patach before final ע (not tsere) — shortened form before guttural</td></tr>

  <tr><td>10</td><td><span class="heb">מַשְׁמִיעַ</span></td><td>Isa 41:26</td>
    <td><input class="parse-field" id="a10g"></td><td><input class="parse-field" id="a10p"></td><td><input class="parse-field" id="a10r"></td>
    <td><button class="reveal-btn" onclick="toggle('r10')">▶</button></td></tr>
  <tr class="answer-row" id="r10"><td colspan="7"><strong>Participle · ms · שָׁמַע</strong> — one who announces; מַ + chiriq-yod + patach furtive before final ע</td></tr>
</table>

<div class="section-label">Group 3 — III-א</div>
<table>
  <tr><th>#</th><th>Form</th><th>Reference</th><th>Conjugation</th><th>PGN</th><th>Root</th><th></th></tr>

  <tr><td>11</td><td><span class="heb">הִמְצִיא</span></td><td>Neh 9:15</td>
    <td><input class="parse-field" id="a11g"></td><td><input class="parse-field" id="a11p"></td><td><input class="parse-field" id="a11r"></td>
    <td><button class="reveal-btn" onclick="toggle('r11')">▶</button></td></tr>
  <tr class="answer-row" id="r11"><td colspan="7"><strong>Perfect · 3ms · מָצָא</strong> — he provided / caused to find; chiriq-yod + silent final א</td></tr>

  <tr><td>12</td><td><span class="heb">וַיַּמְצֵא</span></td><td>2 Chr 2:13</td>
    <td><input class="parse-field" id="a12g"></td><td><input class="parse-field" id="a12p"></td><td><input class="parse-field" id="a12r"></td>
    <td><button class="reveal-btn" onclick="toggle('r12')">▶</button></td></tr>
  <tr class="answer-row" id="r12"><td colspan="7"><strong>Wayyiqtol · 3ms · מָצָא</strong> — and he provided; tsere + silent final א (standard Hiphil wayyiqtol vowel + silent R3)</td></tr>

  <tr><td>13</td><td><span class="heb">יַמְצִיא</span></td><td>Pro 8:35</td>
    <td><input class="parse-field" id="a13g"></td><td><input class="parse-field" id="a13p"></td><td><input class="parse-field" id="a13r"></td>
    <td><button class="reveal-btn" onclick="toggle('r13')">▶</button></td></tr>
  <tr class="answer-row" id="r13"><td colspan="7"><strong>Imperfect · 3ms · מָצָא</strong> — he will cause to find; chiriq-yod + silent final א</td></tr>

  <tr><td>14</td><td><span class="heb">וַיַּקְרֵא</span></td><td>Gen 1:5</td>
    <td><input class="parse-field" id="a14g"></td><td><input class="parse-field" id="a14p"></td><td><input class="parse-field" id="a14r"></td>
    <td><button class="reveal-btn" onclick="toggle('r14')">▶</button></td></tr>
  <tr class="answer-row" id="r14"><td colspan="7"><strong>Wayyiqtol · 3ms · קָרָא</strong> — and he called; tsere + silent final א; one of the most frequent forms in Genesis 1</td></tr>

  <tr><td>15</td><td><span class="heb">מַקְרִיא</span></td><td>Neh 8:3</td>
    <td><input class="parse-field" id="a15g"></td><td><input class="parse-field" id="a15p"></td><td><input class="parse-field" id="a15r"></td>
    <td><button class="reveal-btn" onclick="toggle('r15')">▶</button></td></tr>
  <tr class="answer-row" id="r15"><td colspan="7"><strong>Participle · ms · קָרָא</strong> — one who reads aloud; מַ + chiriq-yod + silent final א</td></tr>
</table>

<div class="section-label">Group 4 — III-ה</div>
<table>
  <tr><th>#</th><th>Form</th><th>Reference</th><th>Conjugation</th><th>PGN</th><th>Root</th><th></th></tr>

  <tr><td>16</td><td><span class="heb">הֶעֱלָה</span></td><td>Gen 8:20</td>
    <td><input class="parse-field" id="a16g"></td><td><input class="parse-field" id="a16p"></td><td><input class="parse-field" id="a16r"></td>
    <td><button class="reveal-btn" onclick="toggle('r16')">▶</button></td></tr>
  <tr class="answer-row" id="r16"><td colspan="7"><strong>Perfect · 3ms · עָלָה</strong> — he offered up; qamets + ה ending; also I-guttural: seghol under הֶ + hateph-seghol under ע</td></tr>

  <tr><td>17</td><td><span class="heb">וַיַּעַל</span></td><td>Gen 22:2</td>
    <td><input class="parse-field" id="a17g"></td><td><input class="parse-field" id="a17p"></td><td><input class="parse-field" id="a17r"></td>
    <td><button class="reveal-btn" onclick="toggle('r17')">▶</button></td></tr>
  <tr class="answer-row" id="r17"><td colspan="7"><strong>Wayyiqtol · 3ms · עָלָה</strong> — and he went up / offered up; apocopated — ה dropped; short patach under R2 (ע)</td></tr>

  <tr><td>18</td><td><span class="heb">יַעֲלֶה</span></td><td>Lev 14:20</td>
    <td><input class="parse-field" id="a18g"></td><td><input class="parse-field" id="a18p"></td><td><input class="parse-field" id="a18r"></td>
    <td><button class="reveal-btn" onclick="toggle('r18')">▶</button></td></tr>
  <tr class="answer-row" id="r18"><td colspan="7"><strong>Imperfect · 3ms · עָלָה</strong> — he shall offer up; seghol + ה ending; composite shewa under ע (I-guttural interaction)</td></tr>

  <tr><td>19</td><td><span class="heb">הַרְאֵה</span></td><td>Exo 33:18</td>
    <td><input class="parse-field" id="a19g"></td><td><input class="parse-field" id="a19p"></td><td><input class="parse-field" id="a19r"></td>
    <td><button class="reveal-btn" onclick="toggle('r19')">▶</button></td></tr>
  <tr class="answer-row" id="r19"><td colspan="7"><strong>Imperative · 2ms · רָאָה</strong> — show me; tsere + ה retained (not apocopated in imperative)</td></tr>

  <tr><td>20</td><td><span class="heb">לְהַעֲלוֹת</span></td><td>Exo 3:17</td>
    <td><input class="parse-field" id="a20g"></td><td><input class="parse-field" id="a20p"></td><td><input class="parse-field" id="a20r"></td>
    <td><button class="reveal-btn" onclick="toggle('r20')">▶</button></td></tr>
  <tr class="answer-row" id="r20"><td colspan="7"><strong>Inf. Construct · — · עָלָה</strong> — to bring up; ends in וֹת — the most reliable III-ה Hiphil inf. construct marker</td></tr>
</table>

<div class="section-label">Group 5 — I-נ</div>
<table>
  <tr><th>#</th><th>Form</th><th>Reference</th><th>Conjugation</th><th>PGN</th><th>Root</th><th></th></tr>

  <tr><td>21</td><td><span class="heb">הִפִּיל</span></td><td>Gen 2:21</td>
    <td><input class="parse-field" id="a21g"></td><td><input class="parse-field" id="a21p"></td><td><input class="parse-field" id="a21r"></td>
    <td><button class="reveal-btn" onclick="toggle('r21')">▶</button></td></tr>
  <tr class="answer-row" id="r21"><td colspan="7"><strong>Perfect · 3ms · נָפַל</strong> — he caused to fall; dagesh forte in R2 (פ) — נ has assimilated; root נָפַל</td></tr>

  <tr><td>22</td><td><span class="heb">וַיַּפֵּל</span></td><td>Gen 2:21</td>
    <td><input class="parse-field" id="a22g"></td><td><input class="parse-field" id="a22p"></td><td><input class="parse-field" id="a22r"></td>
    <td><button class="reveal-btn" onclick="toggle('r22')">▶</button></td></tr>
  <tr class="answer-row" id="r22"><td colspan="7"><strong>Wayyiqtol · 3ms · נָפַל</strong> — and he cast; patach prefix + dagesh in R2 (פ) + tsere final</td></tr>

  <tr><td>23</td><td><span class="heb">יַפִּיל</span></td><td>Pro 19:15</td>
    <td><input class="parse-field" id="a23g"></td><td><input class="parse-field" id="a23p"></td><td><input class="parse-field" id="a23r"></td>
    <td><button class="reveal-btn" onclick="toggle('r23')">▶</button></td></tr>
  <tr class="answer-row" id="r23"><td colspan="7"><strong>Imperfect · 3ms · נָפַל</strong> — causes to fall; patach prefix + dagesh in R2 + chiriq</td></tr>

  <tr><td>24</td><td><span class="heb">הַגֵּשׁ</span></td><td>Gen 27:25</td>
    <td><input class="parse-field" id="a24g"></td><td><input class="parse-field" id="a24p"></td><td><input class="parse-field" id="a24r"></td>
    <td><button class="reveal-btn" onclick="toggle('r24')">▶</button></td></tr>
  <tr class="answer-row" id="r24"><td colspan="7"><strong>Imperative · 2ms · נָגַשׁ</strong> — bring near; הַ + dagesh forte in R2 (ג) + tsere</td></tr>

  <tr><td>25</td><td><span class="heb">מַגִּישׁ</span></td><td>Mal 1:7</td>
    <td><input class="parse-field" id="a25g"></td><td><input class="parse-field" id="a25p"></td><td><input class="parse-field" id="a25r"></td>
    <td><button class="reveal-btn" onclick="toggle('r25')">▶</button></td></tr>
  <tr class="answer-row" id="r25"><td colspan="7"><strong>Participle · ms · נָגַשׁ</strong> — one who brings near; מַ + dagesh in R2 + chiriq</td></tr>
</table>

<div class="section-label">Group 6 — I-י</div>
<table>
  <tr><th>#</th><th>Form</th><th>Reference</th><th>Conjugation</th><th>PGN</th><th>Root</th><th></th></tr>

  <tr><td>26</td><td><span class="heb">הוֹצִיא</span></td><td>Gen 15:7</td>
    <td><input class="parse-field" id="a26g"></td><td><input class="parse-field" id="a26p"></td><td><input class="parse-field" id="a26r"></td>
    <td><button class="reveal-btn" onclick="toggle('r26')">▶</button></td></tr>
  <tr class="answer-row" id="r26"><td colspan="7"><strong>Perfect · 3ms · יָצָא</strong> — he brought out; הוֹ prefix (holem-vav) — the signature I-י/ו Hiphil marker</td></tr>

  <tr><td>27</td><td><span class="heb">וַיּוֹצֵא</span></td><td>Gen 1:12</td>
    <td><input class="parse-field" id="a27g"></td><td><input class="parse-field" id="a27p"></td><td><input class="parse-field" id="a27r"></td>
    <td><button class="reveal-btn" onclick="toggle('r27')">▶</button></td></tr>
  <tr class="answer-row" id="r27"><td colspan="7"><strong>Wayyiqtol · 3ms · יָצָא</strong> — and it brought forth; וַיּוֹ prefix — dagesh in יּ + holem-vav</td></tr>

  <tr><td>28</td><td><span class="heb">יוֹרִיד</span></td><td>1 Sam 2:6</td>
    <td><input class="parse-field" id="a28g"></td><td><input class="parse-field" id="a28p"></td><td><input class="parse-field" id="a28r"></td>
    <td><button class="reveal-btn" onclick="toggle('r28')">▶</button></td></tr>
  <tr class="answer-row" id="r28"><td colspan="7"><strong>Imperfect · 3ms · יָרַד</strong> — he brings down; יוֹ prefix (holem-vav under imperfect prefix consonant)</td></tr>

  <tr><td>29</td><td><span class="heb">הוֹרֵד</span></td><td>Gen 42:38</td>
    <td><input class="parse-field" id="a29g"></td><td><input class="parse-field" id="a29p"></td><td><input class="parse-field" id="a29r"></td>
    <td><button class="reveal-btn" onclick="toggle('r29')">▶</button></td></tr>
  <tr class="answer-row" id="r29"><td colspan="7"><strong>Imperative · 2ms · יָרַד</strong> — bring down; הוֹ prefix (not הַ) + tsere final — distinguishes I-י from strong Hiphil imperative</td></tr>

  <tr><td>30</td><td><span class="heb">מוֹצִיא</span></td><td>Deu 8:14</td>
    <td><input class="parse-field" id="a30g"></td><td><input class="parse-field" id="a30p"></td><td><input class="parse-field" id="a30r"></td>
    <td><button class="reveal-btn" onclick="toggle('r30')">▶</button></td></tr>
  <tr class="answer-row" id="r30"><td colspan="7"><strong>Participle · ms · יָצָא</strong> — the one who brings out; מוֹ prefix (holem-vav under מ) — not מַ of the strong Hiphil</td></tr>
</table>

<div class="section-label">Group 7 — Biconsonantal</div>
<table>
  <tr><th>#</th><th>Form</th><th>Reference</th><th>Conjugation</th><th>PGN</th><th>Root</th><th></th></tr>

  <tr><td>31</td><td><span class="heb">הֵקִים</span></td><td>Gen 6:18</td>
    <td><input class="parse-field" id="a31g"></td><td><input class="parse-field" id="a31p"></td><td><input class="parse-field" id="a31r"></td>
    <td><button class="reveal-btn" onclick="toggle('r31')">▶</button></td></tr>
  <tr class="answer-row" id="r31"><td colspan="7"><strong>Perfect · 3ms · קוּם</strong> — he established; הֵ prefix (tsere) instead of הִ (hiriq) — the primary biconsonantal marker</td></tr>

  <tr><td>32</td><td><span class="heb">וַיָּקֶם</span></td><td>Gen 23:20</td>
    <td><input class="parse-field" id="a32g"></td><td><input class="parse-field" id="a32p"></td><td><input class="parse-field" id="a32r"></td>
    <td><button class="reveal-btn" onclick="toggle('r32')">▶</button></td></tr>
  <tr class="answer-row" id="r32"><td colspan="7"><strong>Wayyiqtol · 3ms · קוּם</strong> — and it was confirmed/set; qamets under prefix consonant + apocopated seghol final</td></tr>

  <tr><td>33</td><td><span class="heb">יָקִים</span></td><td>Deu 18:15</td>
    <td><input class="parse-field" id="a33g"></td><td><input class="parse-field" id="a33p"></td><td><input class="parse-field" id="a33r"></td>
    <td><button class="reveal-btn" onclick="toggle('r33')">▶</button></td></tr>
  <tr class="answer-row" id="r33"><td colspan="7"><strong>Imperfect · 3ms · קוּם</strong> — he will raise up; qamets under prefix consonant (יָ) — not the patach of the strong Hiphil (יַ)</td></tr>

  <tr><td>34</td><td><span class="heb">הָקֵם</span></td><td>Exo 40:2</td>
    <td><input class="parse-field" id="a34g"></td><td><input class="parse-field" id="a34p"></td><td><input class="parse-field" id="a34r"></td>
    <td><button class="reveal-btn" onclick="toggle('r34')">▶</button></td></tr>
  <tr class="answer-row" id="r34"><td colspan="7"><strong>Imperative · 2ms · קוּם</strong> — set up; הָ prefix (qamets) + tsere; contrast with strong הַקְטֵל (patach prefix)</td></tr>

  <tr><td>35</td><td><span class="heb">מֵקִים</span></td><td>1 Sam 2:8</td>
    <td><input class="parse-field" id="a35g"></td><td><input class="parse-field" id="a35p"></td><td><input class="parse-field" id="a35r"></td>
    <td><button class="reveal-btn" onclick="toggle('r35')">▶</button></td></tr>
  <tr class="answer-row" id="r35"><td colspan="7"><strong>Participle · ms · קוּם</strong> — one who raises up; מֵ prefix (tsere) — not מַ (patach) of the strong/most-weak-class Hiphil participle</td></tr>
</table>

<div class="section-label">Group 8 — Geminate</div>
<table>
  <tr><th>#</th><th>Form</th><th>Reference</th><th>Conjugation</th><th>PGN</th><th>Root</th><th></th></tr>

  <tr><td>36</td><td><span class="heb">הֵסֵב</span></td><td>1 Kgs 21:4</td>
    <td><input class="parse-field" id="a36g"></td><td><input class="parse-field" id="a36p"></td><td><input class="parse-field" id="a36r"></td>
    <td><button class="reveal-btn" onclick="toggle('r36')">▶</button></td></tr>
  <tr class="answer-row" id="r36"><td colspan="7"><strong>Perfect · 3ms · סָבַב</strong> — he turned his face; הֵ prefix (tsere) — same as Biconsonantal הֵקִים; root ס-ב-ב has R2=R3 (Geminate)</td></tr>

  <tr><td>37</td><td><span class="heb">וַיָּסֶב</span></td><td>Josh 6:14</td>
    <td><input class="parse-field" id="a37g"></td><td><input class="parse-field" id="a37p"></td><td><input class="parse-field" id="a37r"></td>
    <td><button class="reveal-btn" onclick="toggle('r37')">▶</button></td></tr>
  <tr class="answer-row" id="r37"><td colspan="7"><strong>Wayyiqtol · 3ms · סָבַב</strong> — and they marched around; qamets under prefix + apocopated seghol final — same pattern as Biconsonantal וַיָּקֶם</td></tr>

  <tr><td>38</td><td><span class="heb">יָסֵב</span></td><td>Isa 44:20</td>
    <td><input class="parse-field" id="a38g"></td><td><input class="parse-field" id="a38p"></td><td><input class="parse-field" id="a38r"></td>
    <td><button class="reveal-btn" onclick="toggle('r38')">▶</button></td></tr>
  <tr class="answer-row" id="r38"><td colspan="7"><strong>Imperfect · 3ms · סָבַב</strong> — it leads astray; qamets under prefix consonant (יָ) — same as Biconsonantal יָקִים; root knowledge required to distinguish</td></tr>

  <tr><td>39</td><td><span class="heb">הָסֵב</span></td><td>2 Sam 2:22</td>
    <td><input class="parse-field" id="a39g"></td><td><input class="parse-field" id="a39p"></td><td><input class="parse-field" id="a39r"></td>
    <td><button class="reveal-btn" onclick="toggle('r39')">▶</button></td></tr>
  <tr class="answer-row" id="r39"><td colspan="7"><strong>Imperative · 2ms · סָבַב</strong> — turn aside!; הָ prefix (qamets) — same as Biconsonantal הָקֵם; only root identity (ס-ב-ב vs. hollow) distinguishes</td></tr>

  <tr><td>40</td><td><span class="heb">מֵסֵב</span></td><td>(expected)</td>
    <td><input class="parse-field" id="a40g"></td><td><input class="parse-field" id="a40p"></td><td><input class="parse-field" id="a40r"></td>
    <td><button class="reveal-btn" onclick="toggle('r40')">▶</button></td></tr>
  <tr class="answer-row" id="r40"><td colspan="7"><strong>Participle · ms · סָבַב</strong> — one who surrounds; מֵ prefix (tsere) — same as Biconsonantal מֵקִים; Geminate class requires root knowledge</td></tr>
</table>

<!-- PART B -->
<h2>Part B — Mixed</h2>
<p>Identify the weak class first, then parse fully.</p>

<table>
  <tr><th>#</th><th>Form</th><th>Reference</th><th>Weak class</th><th>Conjugation</th><th>PGN</th><th>Root</th><th></th></tr>

  <tr><td>41</td><td><span class="heb">וַיַּשְׁמַע</span></td><td>1 Sam 15:14</td>
    <td><input class="parse-field" id="b41c"></td><td><input class="parse-field" id="b41g"></td><td><input class="parse-field" id="b41p"></td><td><input class="parse-field" id="b41r"></td>
    <td><button class="reveal-btn" onclick="toggle('rb41')">▶</button></td></tr>
  <tr class="answer-row" id="rb41"><td colspan="8"><strong>III-ח/ע · Wayyiqtol · 3ms · שָׁמַע</strong> — and he made heard; patach (not tsere) before final ע — guttural forces vowel lowering in shortened form</td></tr>

  <tr><td>42</td><td><span class="heb">הֵשִׂים</span></td><td>Gen 45:9</td>
    <td><input class="parse-field" id="b42c"></td><td><input class="parse-field" id="b42g"></td><td><input class="parse-field" id="b42p"></td><td><input class="parse-field" id="b42r"></td>
    <td><button class="reveal-btn" onclick="toggle('rb42')">▶</button></td></tr>
  <tr class="answer-row" id="rb42"><td colspan="8"><strong>Biconsonantal · Perfect · 3ms · שִׂים</strong> — he made / placed; הֵ prefix (tsere) identifies biconsonantal Hiphil perfect; root שׂ-י-מ contains medial hireq-yod vowel letter = Biconsonantal</td></tr>

  <tr><td>43</td><td><span class="heb">וַיַּעַל</span></td><td>Gen 22:2</td>
    <td><input class="parse-field" id="b43c"></td><td><input class="parse-field" id="b43g"></td><td><input class="parse-field" id="b43p"></td><td><input class="parse-field" id="b43r"></td>
    <td><button class="reveal-btn" onclick="toggle('rb43')">▶</button></td></tr>
  <tr class="answer-row" id="rb43"><td colspan="8"><strong>III-ה · Wayyiqtol · 3ms · עָלָה</strong> — and he went up / offered; apocopated: ה dropped, short patach under R2; also I-guttural interaction visible</td></tr>

  <tr><td>44</td><td><span class="heb">הִגִּישׁ</span></td><td>Amos 9:13</td>
    <td><input class="parse-field" id="b44c"></td><td><input class="parse-field" id="b44g"></td><td><input class="parse-field" id="b44p"></td><td><input class="parse-field" id="b44r"></td>
    <td><button class="reveal-btn" onclick="toggle('rb44')">▶</button></td></tr>
  <tr class="answer-row" id="rb44"><td colspan="8"><strong>I-נ · Perfect · 3ms · נָגַשׁ</strong> — he drew near / brought near; dagesh forte in R2 (ג); hiriq prefix (הִ) + dagesh identifies I-נ Hiphil perfect</td></tr>

  <tr><td>45</td><td><span class="heb">הָסֵב</span></td><td>2 Sam 5:23</td>
    <td><input class="parse-field" id="b45c"></td><td><input class="parse-field" id="b45g"></td><td><input class="parse-field" id="b45p"></td><td><input class="parse-field" id="b45r"></td>
    <td><button class="reveal-btn" onclick="toggle('rb45')">▶</button></td></tr>
  <tr class="answer-row" id="rb45"><td colspan="8"><strong>Geminate · Imperative · 2ms · סָבַב</strong> — circle around behind them; הָ prefix (qamets) looks exactly like Biconsonantal הָקֵם; only root knowledge (ס-ב-ב has R2=R3) identifies it as Geminate</td></tr>

  <tr><td>46</td><td><span class="heb">הֶרְאָה</span></td><td>Exo 25:9</td>
    <td><input class="parse-field" id="b46c"></td><td><input class="parse-field" id="b46g"></td><td><input class="parse-field" id="b46p"></td><td><input class="parse-field" id="b46r"></td>
    <td><button class="reveal-btn" onclick="toggle('rb46')">▶</button></td></tr>
  <tr class="answer-row" id="rb46"><td colspan="8"><strong>III-ה · Perfect · 3ms · רָאָה</strong> — he showed; qamets + ה ending; seghol under הֶ (guttural ר causes compensatory lengthening)</td></tr>

  <tr><td>47</td><td><span class="heb">וַיּוֹרֶד</span></td><td>Gen 42:38</td>
    <td><input class="parse-field" id="b47c"></td><td><input class="parse-field" id="b47g"></td><td><input class="parse-field" id="b47p"></td><td><input class="parse-field" id="b47r"></td>
    <td><button class="reveal-btn" onclick="toggle('rb47')">▶</button></td></tr>
  <tr class="answer-row" id="rb47"><td colspan="8"><strong>I-י · Wayyiqtol · 3ms · יָרַד</strong> — and he brought down; וַיּוֹ prefix (dagesh in יּ + holem-vav) uniquely identifies I-י/ו Hiphil wayyiqtol</td></tr>

  <tr><td>48</td><td><span class="heb">מַעֲמִידִים</span></td><td>Neh 4:7</td>
    <td><input class="parse-field" id="b48c"></td><td><input class="parse-field" id="b48g"></td><td><input class="parse-field" id="b48p"></td><td><input class="parse-field" id="b48r"></td>
    <td><button class="reveal-btn" onclick="toggle('rb48')">▶</button></td></tr>
  <tr class="answer-row" id="rb48"><td colspan="8"><strong>I-guttural · Participle · mp · עָמַד</strong> — those who station; מַ + composite shewa under ע + chiriq + ים plural ending</td></tr>

  <tr><td>49</td><td><span class="heb">הַמְצֵא</span></td><td>(†)</td>
    <td><input class="parse-field" id="b49c"></td><td><input class="parse-field" id="b49g"></td><td><input class="parse-field" id="b49p"></td><td><input class="parse-field" id="b49r"></td>
    <td><button class="reveal-btn" onclick="toggle('rb49')">▶</button></td></tr>
  <tr class="answer-row" id="rb49"><td colspan="8"><strong>III-א · Imperative · 2ms · מָצָא</strong> — cause to find; tsere + silent final א; הַ prefix (patach) — compare הִמְצִיא (perfect) which has hiriq under הִ</td></tr>

  <tr><td>50</td><td><span class="heb">וָאָקִים</span></td><td>Exo 6:4</td>
    <td><input class="parse-field" id="b50c"></td><td><input class="parse-field" id="b50g"></td><td><input class="parse-field" id="b50p"></td><td><input class="parse-field" id="b50r"></td>
    <td><button class="reveal-btn" onclick="toggle('rb50')">▶</button></td></tr>
  <tr class="answer-row" id="rb50"><td colspan="8"><strong>Biconsonantal · Wayyiqtol · 1cs · קוּם</strong> — and I established; וָאָ prefix (1cs wayyiqtol) + qamets + chiriq-yod medial; "I also established my covenant with them"</td></tr>
</table>

<h2>Discussion Questions</h2>
<div class="discussion">
  <ol class="disc">
    <li>Compare <span class="heb">הִמְצִיא</span> (III-א perfect 3ms) and <span class="heb">הַמְצֵא</span> (III-א imperative 2ms). Both end with silent final א. How do you distinguish them? What is the key difference in the prefix vowel?</li>
    <li><span class="heb">הַשְׁמַע</span> (III-ח/ע imperative) and <span class="heb">הַעֲמֵד</span> (I-guttural imperative) both begin with הַ. How does the vowel under R1 differ? What does that tell you about the class?</li>
    <li><span class="heb">וַיַּשְׁלַח</span> (III-ח/ע wayyiqtol) and <span class="heb">וַיַּקְרֵא</span> (III-א wayyiqtol) both have patach under וַיַּ. The difference is in the final vowel. Explain what happens to the Hiphil tsere in each case and why.</li>
    <li>Compare <span class="heb">הוֹרֵד</span> (I-י imperative 2ms) and <span class="heb">הָקֵם</span> (Biconsonantal imperative 2ms). Both have a long prefix vowel rather than the patach (הַ) of the strong Hiphil imperative. What prefix vowel does each use, and how can you tell them apart?</li>
    <li>Items 36–40 (Geminate) and items 31–35 (Biconsonantal) share nearly identical vowel patterns in every conjugation: הֵ perfect, יָ/תָּ imperfect, הָ imperative, מֵ participle. What is the <strong>only</strong> reliable way to determine whether a Hiphil form belongs to the Geminate class or the Biconsonantal class? Why can the vocalization alone not always resolve this question?</li>
  </ol>
</div>

<script>
function toggle(id) {
  const row = document.getElementById(id);
  row.style.display = (row.style.display === 'table-row') ? 'none' : 'table-row';
}
function showAll() {
  document.querySelectorAll('.answer-row').forEach(r => r.style.display = 'table-row');
}
function hideAll() {
  document.querySelectorAll('.answer-row').forEach(r => r.style.display = 'none');
}
function clearAll() {
  document.querySelectorAll('input.parse-field').forEach(i => i.value = '');
}
</script>

