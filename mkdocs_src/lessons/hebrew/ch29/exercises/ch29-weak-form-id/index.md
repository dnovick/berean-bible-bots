# Weak Form Id

*Chapter 29 — Hophal Weak*

[Full screen](ch29-weak-form-id.html){.md-button}  [Markdown](ch29-weak-form-id.md){.md-button}  [Print (PDF)](ch29-weak-form-id.pdf){.md-button}

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

<h1>Chapter 29 — Hophal Weak-Form Identification Drill</h1>
<p class="subtitle">BBH Chapter 29 · Hophal Weak Verbs</p>

<p>For each form: (1) <strong>identify the weak class</strong>, (2) <strong>parse</strong> (conjugation + PGN), (3) <strong>identify the root</strong>.</p>

<div class="legend">
  <table>
    <tr><th>Class</th><th>Key diagnostic signal</th></tr>
    <tr><td><strong>I-yod/vav</strong></td><td>שׁוּרֶק prefix (הוּ / יוּ / מוּ); R1 yod/vav quiesces and disappears</td></tr>
    <tr><td><strong>Biconsonantal (hollow)</strong></td><td>שׁוּרֶק prefix (הוּ / יוּ) — same as I-yod; medial root vowel is the key to distinguishing: hollow root has vav/yod as R2</td></tr>
    <tr><td><strong>I-nun</strong></td><td>קִבּוּץ prefix (הֻ / יֻּ) + dagesh forte in R2 throughout — נ has assimilated into R2</td></tr>
    <tr><td><strong>III-he</strong></td><td>קִבּוּץ prefix (הֻ) + qamets-he ending (perfect 3ms); וּ plural (perfect 3cp); seghol-he (imperfect/participle)</td></tr>
    <tr><td><strong>I-guttural</strong></td><td>קִבּוּץ or שׁוּרֶק prefix; composite shewa (hateph vowel) under R1 guttural throughout</td></tr>
    <tr><td><strong>Geminate</strong></td><td>שׁוּרֶק or קִבּוּץ prefix; dagesh forte in final root consonant (R2=R3 contraction); root has identical R2 and R3</td></tr>
  </table>
</div>

<div class="tip">
  <strong>Key distinction:</strong> I-yod/vav and Biconsonantal (hollow) roots <em>both</em> use שׁוּרֶק as their Hophal prefix vowel — unlike most other weak classes which retain קִבּוּץ. The reason: in both classes R1 is a quiescent consonant (yod/vav), so the vowel lengthens to compensate.
</div>

<div class="controls">
  <button onclick="showAll()">Show All Answers</button>
  <button onclick="hideAll()">Hide All Answers</button>
  <button onclick="clearAll()">Clear All Inputs</button>
</div>

<!-- PART A -->
<h2>Part A — By Class</h2>

<div class="section-label">Group 1 — I-yod / I-vav</div>
<table>
  <tr><th>#</th><th>Form</th><th>Reference</th><th>Conjugation</th><th>PGN</th><th>Root</th><th></th></tr>

  <tr><td>1</td><td><span class="heb">הוּרַד</span></td><td>Gen 39:1</td>
    <td><input class="parse-field" id="a1g"></td><td><input class="parse-field" id="a1p"></td><td><input class="parse-field" id="a1r"></td>
    <td><button class="reveal-btn" onclick="toggle('r1')">▶</button></td></tr>
  <tr class="answer-row" id="r1"><td colspan="7"><strong>Perfect · 3ms · יָרַד</strong> — he was brought down; שׁוּרֶק prefix (הוּ) is the I-yod/vav Hophal marker; R1 yod has quiesced</td></tr>

  <tr><td>2</td><td><span class="heb">יוּרַד</span></td><td>Gen 44:29</td>
    <td><input class="parse-field" id="a2g"></td><td><input class="parse-field" id="a2p"></td><td><input class="parse-field" id="a2r"></td>
    <td><button class="reveal-btn" onclick="toggle('r2')">▶</button></td></tr>
  <tr class="answer-row" id="r2"><td colspan="7"><strong>Imperfect · 3ms · יָרַד</strong> — he will be brought down; שׁוּרֶק under imperfect prefix consonant (יוּ) — I-yod/vav pattern</td></tr>

  <tr><td>3</td><td><span class="heb">הוּבָא</span></td><td>Lev 4:4</td>
    <td><input class="parse-field" id="a3g"></td><td><input class="parse-field" id="a3p"></td><td><input class="parse-field" id="a3r"></td>
    <td><button class="reveal-btn" onclick="toggle('r3')">▶</button></td></tr>
  <tr class="answer-row" id="r3"><td colspan="7"><strong>Perfect · 3ms · בּוֹא</strong> — it was brought; הוּ prefix; root בּוֹא is I-vav (hollow); III-aleph: silent final א</td></tr>

  <tr><td>4</td><td><span class="heb">הוּבְאוּ</span></td><td>Gen 43:18</td>
    <td><input class="parse-field" id="a4g"></td><td><input class="parse-field" id="a4p"></td><td><input class="parse-field" id="a4r"></td>
    <td><button class="reveal-btn" onclick="toggle('r4')">▶</button></td></tr>
  <tr class="answer-row" id="r4"><td colspan="7"><strong>Perfect · 3cp · בּוֹא</strong> — they were brought; הוּ prefix + וּ plural ending; I-vav root</td></tr>

  <tr><td>5</td><td><span class="heb">מוּבָאִים</span></td><td>Gen 43:18</td>
    <td><input class="parse-field" id="a5g"></td><td><input class="parse-field" id="a5p"></td><td><input class="parse-field" id="a5r"></td>
    <td><button class="reveal-btn" onclick="toggle('r5')">▶</button></td></tr>
  <tr class="answer-row" id="r5"><td colspan="7"><strong>Participle · mp · בּוֹא</strong> — being brought; מוּ prefix (שׁוּרֶק under מ) is the I-yod/vav Hophal participle marker; ים plural</td></tr>
</table>

<div class="section-label">Group 2 — Biconsonantal (Hollow)</div>
<table>
  <tr><th>#</th><th>Form</th><th>Reference</th><th>Conjugation</th><th>PGN</th><th>Root</th><th></th></tr>

  <tr><td>6</td><td><span class="heb">הוּקַם</span></td><td>Exo 40:17</td>
    <td><input class="parse-field" id="a6g"></td><td><input class="parse-field" id="a6p"></td><td><input class="parse-field" id="a6r"></td>
    <td><button class="reveal-btn" onclick="toggle('r6')">▶</button></td></tr>
  <tr class="answer-row" id="r6"><td colspan="7"><strong>Perfect · 3ms · קוּם</strong> — it was set up/erected; הוּ prefix; hollow biconsonantal root (medial וּ vowel letter)</td></tr>

  <tr><td>7</td><td><span class="heb">יוּמַת</span></td><td>Gen 26:11</td>
    <td><input class="parse-field" id="a7g"></td><td><input class="parse-field" id="a7p"></td><td><input class="parse-field" id="a7r"></td>
    <td><button class="reveal-btn" onclick="toggle('r7')">▶</button></td></tr>
  <tr class="answer-row" id="r7"><td colspan="7"><strong>Imperfect · 3ms · מוּת</strong> — he shall be put to death; יוּ prefix — biconsonantal Hophal imperfect; hollow root מוּת</td></tr>

  <tr><td>8</td><td><span class="heb">הוּסַר</span></td><td>Lev 4:31</td>
    <td><input class="parse-field" id="a8g"></td><td><input class="parse-field" id="a8p"></td><td><input class="parse-field" id="a8r"></td>
    <td><button class="reveal-btn" onclick="toggle('r8')">▶</button></td></tr>
  <tr class="answer-row" id="r8"><td colspan="7"><strong>Perfect · 3ms · סוּר</strong> — it was removed; הוּ prefix; hollow root סוּר; "the fat was removed"</td></tr>

  <tr><td>9</td><td><span class="heb">הוּשַׁב</span></td><td>Gen 42:28</td>
    <td><input class="parse-field" id="a9g"></td><td><input class="parse-field" id="a9p"></td><td><input class="parse-field" id="a9r"></td>
    <td><button class="reveal-btn" onclick="toggle('r9')">▶</button></td></tr>
  <tr class="answer-row" id="r9"><td colspan="7"><strong>Perfect · 3ms · שׁוּב</strong> — it was returned/restored; הוּ prefix; hollow root שׁוּב; "my silver was returned"</td></tr>

  <tr><td>10</td><td><span class="heb">יּוּשַׂם</span></td><td>Gen 24:33</td>
    <td><input class="parse-field" id="a10g"></td><td><input class="parse-field" id="a10p"></td><td><input class="parse-field" id="a10r"></td>
    <td><button class="reveal-btn" onclick="toggle('r10')">▶</button></td></tr>
  <tr class="answer-row" id="r10"><td colspan="7"><strong>Wayyiqtol · 3ms · שִׂים</strong> — and food was set before him; יּוּ prefix (wayyiqtol) — dagesh in יּ + שׁוּרֶק; hollow/biconsonantal root שִׂים</td></tr>
</table>

<div class="section-label">Group 3 — I-nun</div>
<table>
  <tr><th>#</th><th>Form</th><th>Reference</th><th>Conjugation</th><th>PGN</th><th>Root</th><th></th></tr>

  <tr><td>11</td><td><span class="heb">וַיֻּגַּד</span></td><td>Gen 22:20</td>
    <td><input class="parse-field" id="a11g"></td><td><input class="parse-field" id="a11p"></td><td><input class="parse-field" id="a11r"></td>
    <td><button class="reveal-btn" onclick="toggle('r11')">▶</button></td></tr>
  <tr class="answer-row" id="r11"><td colspan="7"><strong>Wayyiqtol · 3ms · נָגַד</strong> — and it was told; וַיֻּ prefix (wayyiqtol) + קִבּוּץ + dagesh forte in R2 (ג) — נ has assimilated</td></tr>

  <tr><td>12</td><td><span class="heb">יֻּגַּד</span></td><td>Gen 38:13</td>
    <td><input class="parse-field" id="a12g"></td><td><input class="parse-field" id="a12p"></td><td><input class="parse-field" id="a12r"></td>
    <td><button class="reveal-btn" onclick="toggle('r12')">▶</button></td></tr>
  <tr class="answer-row" id="r12"><td colspan="7"><strong>Imperfect · 3ms · נָגַד</strong> — it was told to Tamar; קִבּוּץ under prefix (יֻּ) + dagesh in R2 (ג) — I-nun assimilation</td></tr>

  <tr><td>13</td><td><span class="heb">יֻּכּוּ</span></td><td>Exo 5:14</td>
    <td><input class="parse-field" id="a13g"></td><td><input class="parse-field" id="a13p"></td><td><input class="parse-field" id="a13r"></td>
    <td><button class="reveal-btn" onclick="toggle('r13')">▶</button></td></tr>
  <tr class="answer-row" id="r13"><td colspan="7"><strong>Wayyiqtol · 3mp · נָכָה</strong> — and they were beaten; קִבּוּץ + dagesh in R2 (כּ) — I-nun; III-he root; וּ plural ending; "the taskmasters beat the Israelite foremen"</td></tr>

  <tr><td>14</td><td><span class="heb">יֻּתַּן</span></td><td>Lev 11:38</td>
    <td><input class="parse-field" id="a14g"></td><td><input class="parse-field" id="a14p"></td><td><input class="parse-field" id="a14r"></td>
    <td><button class="reveal-btn" onclick="toggle('r14')">▶</button></td></tr>
  <tr class="answer-row" id="r14"><td colspan="7"><strong>Imperfect · 3ms · נָתַן</strong> — if water is put on the seed; קִבּוּץ prefix + dagesh in R2 (תּ) — I-nun; the second נ of נָתַן also assimilates, causing extra dagesh in R3</td></tr>

  <tr><td>15</td><td><span class="heb">יֻּקַּם</span></td><td>Gen 4:15</td>
    <td><input class="parse-field" id="a15g"></td><td><input class="parse-field" id="a15p"></td><td><input class="parse-field" id="a15r"></td>
    <td><button class="reveal-btn" onclick="toggle('r15')">▶</button></td></tr>
  <tr class="answer-row" id="r15"><td colspan="7"><strong>Imperfect · 3ms · נָקַם</strong> — he will be avenged; קִבּוּץ + dagesh in R2 (קּ) — I-nun: נ of נָקַם has assimilated; "Cain will be avenged sevenfold"</td></tr>
</table>

<div class="section-label">Group 4 — III-he</div>
<table>
  <tr><th>#</th><th>Form</th><th>Reference</th><th>Conjugation</th><th>PGN</th><th>Root</th><th></th></tr>

  <tr><td>16</td><td><span class="heb">הֻגְלָה</span></td><td>Amos 1:5</td>
    <td><input class="parse-field" id="a16g"></td><td><input class="parse-field" id="a16p"></td><td><input class="parse-field" id="a16r"></td>
    <td><button class="reveal-btn" onclick="toggle('r16')">▶</button></td></tr>
  <tr class="answer-row" id="r16"><td colspan="7"><strong>Perfect · 3ms · גָּלָה</strong> — the people of Aram were exiled; קִבּוּץ under הֻ + III-he: qamets-he ending</td></tr>

  <tr><td>17</td><td><span class="heb">הֻגְלוּ</span></td><td>Jer 29:1</td>
    <td><input class="parse-field" id="a17g"></td><td><input class="parse-field" id="a17p"></td><td><input class="parse-field" id="a17r"></td>
    <td><button class="reveal-btn" onclick="toggle('r17')">▶</button></td></tr>
  <tr class="answer-row" id="r17"><td colspan="7"><strong>Perfect · 3cp · גָּלָה</strong> — those who were exiled from Jerusalem; קִבּוּץ under הֻ + וּ plural (III-he 3cp Qatal pattern: ה→ וּ)</td></tr>

  <tr><td>18</td><td><span class="heb">מוּכָּה</span></td><td>Deut 28:27</td>
    <td><input class="parse-field" id="a18g"></td><td><input class="parse-field" id="a18p"></td><td><input class="parse-field" id="a18r"></td>
    <td><button class="reveal-btn" onclick="toggle('r18')">▶</button></td></tr>
  <tr class="answer-row" id="r18"><td colspan="7"><strong>Participle · fs · נָכָה</strong> — stricken (with); מוּ prefix (I-yod/nun in participle); dagesh in R2 (כּ) — I-nun; III-he: ה ending on feminine participle</td></tr>

  <tr><td>19</td><td><span class="heb">יֻּכֶּה</span></td><td>Exo 21:20</td>
    <td><input class="parse-field" id="a19g"></td><td><input class="parse-field" id="a19p"></td><td><input class="parse-field" id="a19r"></td>
    <td><button class="reveal-btn" onclick="toggle('r19')">▶</button></td></tr>
  <tr class="answer-row" id="r19"><td colspan="7"><strong>Imperfect · 3ms · נָכָה</strong> — if he is struck/beaten; קִבּוּץ prefix + dagesh in R2 (כּ) — I-nun; III-he: seghol-he ending in imperfect</td></tr>

  <tr><td>20</td><td><span class="heb">הֻלַּד</span></td><td>Exo 1:22</td>
    <td><input class="parse-field" id="a20g"></td><td><input class="parse-field" id="a20p"></td><td><input class="parse-field" id="a20r"></td>
    <td><button class="reveal-btn" onclick="toggle('r20')">▶</button></td></tr>
  <tr class="answer-row" id="r20"><td colspan="7"><strong>Perfect · 3ms · יָלַד</strong> — every son who is born; קִבּוּץ under הֻ + dagesh in R2 (לּ); root יָלַד is I-yod; the dagesh assimilates the yod's behavior in Hophal</td></tr>
</table>

<div class="section-label">Group 5 — I-guttural</div>
<table>
  <tr><th>#</th><th>Form</th><th>Reference</th><th>Conjugation</th><th>PGN</th><th>Root</th><th></th></tr>

  <tr><td>21</td><td><span class="heb">הוּחַל</span></td><td>Gen 4:26</td>
    <td><input class="parse-field" id="a21g"></td><td><input class="parse-field" id="a21p"></td><td><input class="parse-field" id="a21r"></td>
    <td><button class="reveal-btn" onclick="toggle('r21')">▶</button></td></tr>
  <tr class="answer-row" id="r21"><td colspan="7"><strong>Perfect · 3ms · חָלַל</strong> — it was begun/profaned; הוּ prefix; guttural ח: no dagesh, takes full vowel (patach under ח); "then it was begun to call on the name of YHWH"</td></tr>

  <tr><td>22</td><td><span class="heb">יָחֳרַם</span></td><td>Ezr 10:8</td>
    <td><input class="parse-field" id="a22g"></td><td><input class="parse-field" id="a22p"></td><td><input class="parse-field" id="a22r"></td>
    <td><button class="reveal-btn" onclick="toggle('r22')">▶</button></td></tr>
  <tr class="answer-row" id="r22"><td colspan="7"><strong>Imperfect · 3ms · חָרַם</strong> — his property will be forfeited/devoted; I-guttural: hateph-qamets under ח (יָ + חֳ); "all his property will be devoted to destruction"</td></tr>

  <tr><td>23</td><td><span class="heb">הֻחְלָה</span></td><td>1 Sam 21:6</td>
    <td><input class="parse-field" id="a23g"></td><td><input class="parse-field" id="a23p"></td><td><input class="parse-field" id="a23r"></td>
    <td><button class="reveal-btn" onclick="toggle('r23')">▶</button></td></tr>
  <tr class="answer-row" id="r23"><td colspan="7"><strong>Perfect · 3fs · חָלָה</strong> — it had been set apart/consecrated; קִבּוּץ under הֻ + shewa under guttural ח + III-he ה ending (fs suffix)</td></tr>

  <tr><td>24</td><td><span class="heb">הֻאֲמַן</span></td><td>2 Chr 9:8</td>
    <td><input class="parse-field" id="a24g"></td><td><input class="parse-field" id="a24p"></td><td><input class="parse-field" id="a24r"></td>
    <td><button class="reveal-btn" onclick="toggle('r24')">▶</button></td></tr>
  <tr class="answer-row" id="r24"><td colspan="7"><strong>Perfect · 3ms · אָמַן</strong> — he was found faithful/established; קִבּוּץ under הֻ + hateph-patach under guttural א — I-aleph (I-guttural); "because your God has set you…on his throne"</td></tr>

  <tr><td>25</td><td><span class="heb">יֶֽחֱטָא</span></td><td>Num 15:28</td>
    <td><input class="parse-field" id="a25g"></td><td><input class="parse-field" id="a25p"></td><td><input class="parse-field" id="a25r"></td>
    <td><button class="reveal-btn" onclick="toggle('r25')">▶</button></td></tr>
  <tr class="answer-row" id="r25"><td colspan="7"><strong>Imperfect · 3ms · חָטָא</strong> — he will be cleansed/pardoned; I-guttural: hateph-seghol under ח; III-aleph: silent final א; "the priest shall make atonement and he will be forgiven"</td></tr>
</table>

<div class="section-label">Group 6 — Geminate</div>
<table>
  <tr><th>#</th><th>Form</th><th>Reference</th><th>Conjugation</th><th>PGN</th><th>Root</th><th></th></tr>

  <tr><td>26</td><td><span class="heb">הוּסַב</span></td><td>2 Sam 3:12</td>
    <td><input class="parse-field" id="a26g"></td><td><input class="parse-field" id="a26p"></td><td><input class="parse-field" id="a26r"></td>
    <td><button class="reveal-btn" onclick="toggle('r26')">▶</button></td></tr>
  <tr class="answer-row" id="r26"><td colspan="7"><strong>Perfect · 3ms · סָבַב</strong> — the kingdom was turned over; הוּ prefix; geminate root ס-ב-ב (R2=R3); שׁוּרֶק form of Hophal geminate</td></tr>

  <tr><td>27</td><td><span class="heb">מוּסַבּוֹת</span></td><td>Num 32:38</td>
    <td><input class="parse-field" id="a27g"></td><td><input class="parse-field" id="a27p"></td><td><input class="parse-field" id="a27r"></td>
    <td><button class="reveal-btn" onclick="toggle('r27')">▶</button></td></tr>
  <tr class="answer-row" id="r27"><td colspan="7"><strong>Participle · fp · סָבַב</strong> — their names having been changed/surrounded; מוּ prefix + dagesh forte in R3 (בּ) — geminate contraction; feminine plural וֹת ending</td></tr>

  <tr><td>28</td><td><span class="heb">הֻסַּב</span></td><td>1 Kgs 2:15</td>
    <td><input class="parse-field" id="a28g"></td><td><input class="parse-field" id="a28p"></td><td><input class="parse-field" id="a28r"></td>
    <td><button class="reveal-btn" onclick="toggle('r28')">▶</button></td></tr>
  <tr class="answer-row" id="r28"><td colspan="7"><strong>Perfect · 3ms · סָבַב</strong> — the kingdom was turned over; קִבּוּץ under הֻ + dagesh forte in R2 (סּ) — alternate geminate Hophal form; contrast הוּסַב (item 26) which uses שׁוּרֶק</td></tr>

  <tr><td>29</td><td><span class="heb">יֻּתַּם</span></td><td>2 Sam 20:18</td>
    <td><input class="parse-field" id="a29g"></td><td><input class="parse-field" id="a29p"></td><td><input class="parse-field" id="a29r"></td>
    <td><button class="reveal-btn" onclick="toggle('r29')">▶</button></td></tr>
  <tr class="answer-row" id="r29"><td colspan="7"><strong>Imperfect · 3ms · תָּמַם</strong> — a matter will be completed/finished; קִבּוּץ + dagesh in R2 (תּ) — geminate root ת-מ-מ (R2=R3)</td></tr>

  <tr><td>30</td><td><span class="heb">יֻּכַּל</span></td><td>Num 13:30</td>
    <td><input class="parse-field" id="a30g"></td><td><input class="parse-field" id="a30p"></td><td><input class="parse-field" id="a30r"></td>
    <td><button class="reveal-btn" onclick="toggle('r30')">▶</button></td></tr>
  <tr class="answer-row" id="r30"><td colspan="7"><strong>Imperfect · 3ms · כָּלַל</strong> — it will be completed/able to be done; קִבּוּץ + dagesh in R2 (כּ) — geminate root כ-ל-ל; "we are well able to overcome it"</td></tr>
</table>

<!-- PART B -->
<h2>Part B — Mixed</h2>
<p>Identify the weak class first, then parse fully.</p>

<table>
  <tr><th>#</th><th>Form</th><th>Reference</th><th>Weak class</th><th>Conjugation</th><th>PGN</th><th>Root</th><th></th></tr>

  <tr><td>31</td><td><span class="heb">הוּבָא</span></td><td>Gen 33:11</td>
    <td><input class="parse-field" id="b31c"></td><td><input class="parse-field" id="b31g"></td><td><input class="parse-field" id="b31p"></td><td><input class="parse-field" id="b31r"></td>
    <td><button class="reveal-btn" onclick="toggle('rb31')">▶</button></td></tr>
  <tr class="answer-row" id="rb31"><td colspan="8"><strong>I-vav / Biconsonantal · Perfect · 3ms · בּוֹא</strong> — the gift was brought to him; הוּ prefix; root בּוֹא is I-vav and hollow</td></tr>

  <tr><td>32</td><td><span class="heb">יֻּגַּד</span></td><td>Gen 48:2</td>
    <td><input class="parse-field" id="b32c"></td><td><input class="parse-field" id="b32g"></td><td><input class="parse-field" id="b32p"></td><td><input class="parse-field" id="b32r"></td>
    <td><button class="reveal-btn" onclick="toggle('rb32')">▶</button></td></tr>
  <tr class="answer-row" id="rb32"><td colspan="8"><strong>I-nun · Imperfect · 3ms · נָגַד</strong> — it was told to Jacob; קִבּוּץ + dagesh in R2 (ג) — נ of נָגַד has assimilated</td></tr>

  <tr><td>33</td><td><span class="heb">יוּמַת</span></td><td>Lev 20:2</td>
    <td><input class="parse-field" id="b33c"></td><td><input class="parse-field" id="b33g"></td><td><input class="parse-field" id="b33p"></td><td><input class="parse-field" id="b33r"></td>
    <td><button class="reveal-btn" onclick="toggle('rb33')">▶</button></td></tr>
  <tr class="answer-row" id="rb33"><td colspan="8"><strong>Biconsonantal · Imperfect · 3ms · מוּת</strong> — he shall be put to death; יוּ prefix — hollow biconsonantal Hophal imperfect</td></tr>

  <tr><td>34</td><td><span class="heb">הֻגְלוּ</span></td><td>2 Kgs 17:23</td>
    <td><input class="parse-field" id="b34c"></td><td><input class="parse-field" id="b34g"></td><td><input class="parse-field" id="b34p"></td><td><input class="parse-field" id="b34r"></td>
    <td><button class="reveal-btn" onclick="toggle('rb34')">▶</button></td></tr>
  <tr class="answer-row" id="rb34"><td colspan="8"><strong>III-he · Perfect · 3cp · גָּלָה</strong> — Israel was exiled from its land; קִבּוּץ under הֻ + וּ plural ending (III-he 3cp: ה drops, וּ takes its place)</td></tr>

  <tr><td>35</td><td><span class="heb">הוּקַם</span></td><td>Num 7:1</td>
    <td><input class="parse-field" id="b35c"></td><td><input class="parse-field" id="b35g"></td><td><input class="parse-field" id="b35p"></td><td><input class="parse-field" id="b35r"></td>
    <td><button class="reveal-btn" onclick="toggle('rb35')">▶</button></td></tr>
  <tr class="answer-row" id="rb35"><td colspan="8"><strong>Biconsonantal · Perfect · 3ms · קוּם</strong> — the tabernacle was erected; הוּ prefix; hollow root קוּם; medial vav vowel letter is the biconsonantal marker</td></tr>

  <tr><td>36</td><td><span class="heb">הוּסַר</span></td><td>Lev 6:4</td>
    <td><input class="parse-field" id="b36c"></td><td><input class="parse-field" id="b36g"></td><td><input class="parse-field" id="b36p"></td><td><input class="parse-field" id="b36r"></td>
    <td><button class="reveal-btn" onclick="toggle('rb36')">▶</button></td></tr>
  <tr class="answer-row" id="rb36"><td colspan="8"><strong>Biconsonantal · Perfect · 3ms · סוּר</strong> — the ashes shall be removed; הוּ prefix; hollow root סוּר; distinguish from Geminate: no R2=R3</td></tr>

  <tr><td>37</td><td><span class="heb">יֻּכּוּ</span></td><td>Num 14:12</td>
    <td><input class="parse-field" id="b37c"></td><td><input class="parse-field" id="b37g"></td><td><input class="parse-field" id="b37p"></td><td><input class="parse-field" id="b37r"></td>
    <td><button class="reveal-btn" onclick="toggle('rb37')">▶</button></td></tr>
  <tr class="answer-row" id="rb37"><td colspan="8"><strong>I-nun + III-he · Wayyiqtol · 3mp · נָכָה</strong> — and they were struck; קִבּוּץ + dagesh in R2 (כּ) — I-nun; III-he root; וּ plural; note both weak classes interact</td></tr>

  <tr><td>38</td><td><span class="heb">הוּרַד</span></td><td>1 Sam 30:24</td>
    <td><input class="parse-field" id="b38c"></td><td><input class="parse-field" id="b38g"></td><td><input class="parse-field" id="b38p"></td><td><input class="parse-field" id="b38r"></td>
    <td><button class="reveal-btn" onclick="toggle('rb38')">▶</button></td></tr>
  <tr class="answer-row" id="rb38"><td colspan="8"><strong>I-yod · Perfect · 3ms · יָרַד</strong> — the share of the one who stayed with the baggage; הוּ prefix; R1 yod has quiesced; "so his share shall be equal"</td></tr>

  <tr><td>39</td><td><span class="heb">הוּחַל</span></td><td>Gen 4:26</td>
    <td><input class="parse-field" id="b39c"></td><td><input class="parse-field" id="b39g"></td><td><input class="parse-field" id="b39p"></td><td><input class="parse-field" id="b39r"></td>
    <td><button class="reveal-btn" onclick="toggle('rb39')">▶</button></td></tr>
  <tr class="answer-row" id="rb39"><td colspan="8"><strong>I-guttural · Perfect · 3ms · חָלַל</strong> — it was begun; הוּ prefix; guttural ח: no dagesh, full vowel (patach) replaces shewa under R1</td></tr>

  <tr><td>40</td><td><span class="heb">הוּסַב</span></td><td>Josh 15:3</td>
    <td><input class="parse-field" id="b40c"></td><td><input class="parse-field" id="b40g"></td><td><input class="parse-field" id="b40p"></td><td><input class="parse-field" id="b40r"></td>
    <td><button class="reveal-btn" onclick="toggle('rb40')">▶</button></td></tr>
  <tr class="answer-row" id="rb40"><td colspan="8"><strong>Geminate · Perfect · 3ms · סָבַב</strong> — it turned/went around; הוּ prefix; root ס-ב-ב has R2=R3 (geminate) — this is the only reliable distinguisher from biconsonantal הוּסַר (root סוּר: hollow, not geminate)</td></tr>
</table>

<h2>Discussion Questions</h2>
<div class="discussion">
  <ol class="disc">
    <li>The I-yod/vav Hophal (e.g., <span class="heb">הוּרַד</span>, <span class="heb">הוּבָא</span>) and the Biconsonantal (hollow) Hophal (e.g., <span class="heb">הוּקַם</span>, <span class="heb">הוּסַר</span>) both use שׁוּרֶק as the prefix vowel. What phonological principle explains why <em>both</em> classes abandon the usual קִבּוּץ prefix of the strong Hophal? What happens to R1 in each class?</li>
    <li>Compare <span class="heb">וַיֻּגַּד</span> (I-nun Hophal wayyiqtol, item 11) and <span class="heb">יֻּכּוּ</span> (I-nun Hophal, item 13). Both have dagesh forte in R2. What caused that dagesh? What happened to the נ of each root? Does anything else unusual happen to <span class="heb">יֻּכּוּ</span> beyond the I-nun assimilation?</li>
    <li>Items 16–17 (<span class="heb">הֻגְלָה</span> / <span class="heb">הֻגְלוּ</span>) and items 18–19 (<span class="heb">מוּכָּה</span> / <span class="heb">יֻּכֶּה</span>) all come from III-he roots. How does the III-he ending manifest in the Hophal perfect 3ms vs. 3cp? How does it appear in the participle vs. imperfect?</li>
    <li>Items 26 and 28 (<span class="heb">הוּסַב</span> and <span class="heb">הֻסַּב</span>) are both Hophal forms of the same geminate root סָבַב but have different prefix vowels. What accounts for this variation? How do you distinguish the Geminate Hophal from the Biconsonantal Hophal when both may display שׁוּרֶק?</li>
    <li>Write out the Hophal paradigm for <span class="heb">מוּת</span> (Biconsonantal hollow): Perfect 3ms, Imperfect 3ms, Wayyiqtol 3ms, Participle ms. For each form, identify the prefix vowel and explain how it differs from the strong Hophal (<span class="heb">הֻקְטַל</span> pattern).</li>
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

