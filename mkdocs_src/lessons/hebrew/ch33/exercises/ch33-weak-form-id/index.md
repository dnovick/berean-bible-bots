# Weak Form Id

*Chapter 33 — Pual Weak*

[Full screen](ch33-weak-form-id.html){.md-button}  [Markdown](ch33-weak-form-id.md){.md-button}  [Print (PDF)](ch33-weak-form-id.pdf){.md-button}

<style>

  body { font-family: Georgia, serif;    color: #222; }
  h1 { font-size: 1.4em; border-bottom: 2px solid #444; padding-bottom: .4em; }
  h2 { font-size: 1.15em; margin-top: 2em; color: #444; }
  h3 { font-size: 1em; margin-top: 1.5em; color: #555; }
  .subtitle { color: #666; font-style: italic; margin-top: -.3em; }
  table { border-collapse: collapse;  margin: 1em 0; }
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

<h1>Chapter 33 — Pual Weak-Form Identification Drill</h1>
<p class="subtitle">BBH Chapter 33 · Pual Weak Verbs</p>

<p>For each form: (1) <strong>identify the weak class</strong>, (2) <strong>parse</strong> (conjugation + PGN), (3) <strong>identify the root</strong>.</p>

<div class="legend">
  <div style="overflow-x:auto;max-width:100%;"><table>
    <tr><th>Class</th><th>Key diagnostic signal in Pual</th></tr>
    <tr><td><strong>III-he</strong></td><td>Pual qibbuts + dagesh in R2 preserved; III-he endings: qamets + ה (perfect 3ms); shureq (וּ) in 3mp; ה drops in apocopated forms</td></tr>
    <tr><td><strong>I-nun</strong></td><td>Nun (R1) assimilates into dagesh forte in R2 in the Pual — contrast Piel where nun stays; the dagesh in R2 serves double duty: Pual stem marker + assimilated nun</td></tr>
    <tr><td><strong>I-guttural</strong></td><td>Guttural R1 (א/ה/ח/ע) may reject simple shewa; holem (אֹ) or qamets (ָ) can appear through compensatory lengthening; dagesh forte in R2 retained when possible</td></tr>
    <tr><td><strong>Geminate</strong></td><td>R2=R3; Pual dagesh forte in R2 doubles the already-doubled consonant; pattern mirrors Piel Geminate; composite shewa before vocalic endings</td></tr>
  </table></div>
</div>

<div class="tip"><strong>Key distinction:</strong> In I-nun roots, the Piel retains the nun (יְנַחֵם — nun visible) but the Pual assimilates the nun into the dagesh in R2 (נֻכָּה — nun gone, dagesh in כ has double duty). The Pual follows the same assimilation rule as Qal/Hiphil.</div>

<div class="controls">
  <button onclick="showAll()">Show All Answers</button>
  <button onclick="hideAll()">Hide All Answers</button>
  <button onclick="clearAll()">Clear All Inputs</button>
</div>

<!-- PART A -->
<h2>Part A — By Class</h2>

<div class="section-label">Group 1 — III-he</div>
<div style="overflow-x:auto;max-width:100%;"><table>
  <tr><th>#</th><th>Form</th><th>Reference</th><th>Conjugation</th><th>PGN</th><th>Root</th><th></th></tr>

  <tr><td>1</td><td><span class="heb">יְכֻלּוּ</span></td><td>Gen 2:1</td>
    <td><input class="parse-field" id="a1g"></td><td><input class="parse-field" id="a1p"></td><td><input class="parse-field" id="a1r"></td>
    <td><button class="reveal-btn" onclick="toggle('r1')">▶</button></td></tr>
  <tr class="answer-row" id="r1"><td colspan="7"><strong>Wayyiqtol · 3mp · כָּלָה</strong> — were finished/completed; qibbuts under כ + dagesh forte in ל; III-he Pual 3mp shureq ending; "thus the heavens and earth were completed"</td></tr>

  <tr><td>2</td><td><span class="heb">יְכֻסּוּ</span></td><td>Gen 7:19</td>
    <td><input class="parse-field" id="a2g"></td><td><input class="parse-field" id="a2p"></td><td><input class="parse-field" id="a2r"></td>
    <td><button class="reveal-btn" onclick="toggle('r2')">▶</button></td></tr>
  <tr class="answer-row" id="r2"><td colspan="7"><strong>Wayyiqtol · 3mp · כָּסָה</strong> — were covered; qibbuts under כ + dagesh forte in ס; III-he Pual 3mp shureq ending; "all the high mountains were covered"</td></tr>

  <tr><td>3</td><td><span class="heb">כֻּסָּה</span></td><td>Exo 15:5</td>
    <td><input class="parse-field" id="a3g"></td><td><input class="parse-field" id="a3p"></td><td><input class="parse-field" id="a3r"></td>
    <td><button class="reveal-btn" onclick="toggle('r3')">▶</button></td></tr>
  <tr class="answer-row" id="r3"><td colspan="7"><strong>Perfect · 3ms · כָּסָה</strong> — it was covered; qibbuts under כ + dagesh forte in ס; III-he Pual perfect 3ms: qamets + ה ending; Song of the Sea</td></tr>

  <tr><td>4</td><td><span class="heb">צֻוֵּיתָ</span></td><td>Gen 45:19</td>
    <td><input class="parse-field" id="a4g"></td><td><input class="parse-field" id="a4p"></td><td><input class="parse-field" id="a4r"></td>
    <td><button class="reveal-btn" onclick="toggle('r4')">▶</button></td></tr>
  <tr class="answer-row" id="r4"><td colspan="7"><strong>Perfect · 2ms · צָוָה</strong> — you have been commanded; qibbuts under צ + dagesh forte in ו (R2); III-he Pual perfect 2ms: tsere-yod vowel letter before תָ suffix; Pharaoh to Joseph's brothers</td></tr>

  <tr><td>5</td><td><span class="heb">כֻּלָּה</span></td><td>Isa 24:10</td>
    <td><input class="parse-field" id="a5g"></td><td><input class="parse-field" id="a5p"></td><td><input class="parse-field" id="a5r"></td>
    <td><button class="reveal-btn" onclick="toggle('r5')">▶</button></td></tr>
  <tr class="answer-row" id="r5"><td colspan="7"><strong>Perfect · 3fs · כָּלָה</strong> — it was devastated/finished; qibbuts under כ + dagesh forte in ל; III-he Pual perfect 3fs: qamets + ה ending (same as 3ms for III-he roots — context/gender of subject determines)</td></tr>
</table></div>

<div class="section-label">Group 2 — I-nun</div>
<div style="overflow-x:auto;max-width:100%;"><table>
  <tr><th>#</th><th>Form</th><th>Reference</th><th>Conjugation</th><th>PGN</th><th>Root</th><th></th></tr>

  <tr><td>6</td><td><span class="heb">נֻכָּה</span></td><td>Exo 9:31</td>
    <td><input class="parse-field" id="a6g"></td><td><input class="parse-field" id="a6p"></td><td><input class="parse-field" id="a6r"></td>
    <td><button class="reveal-btn" onclick="toggle('r6')">▶</button></td></tr>
  <tr class="answer-row" id="r6"><td colspan="7"><strong>Perfect · 3fs · נָכָה</strong> — it was struck; nun assimilated → dagesh forte in כ (R2); qibbuts under נ position visible; III-he: qamets + ה ending; "the flax and barley were struck" (plague of hail)</td></tr>

  <tr><td>7</td><td><span class="heb">נֻכּוּ</span></td><td>Exo 9:32</td>
    <td><input class="parse-field" id="a7g"></td><td><input class="parse-field" id="a7p"></td><td><input class="parse-field" id="a7r"></td>
    <td><button class="reveal-btn" onclick="toggle('r7')">▶</button></td></tr>
  <tr class="answer-row" id="r7"><td colspan="7"><strong>Perfect · 3cp · נָכָה</strong> — they were not struck; nun assimilated → dagesh forte in כ; III-he Pual 3cp: shureq ending; "but the wheat and spelt were not struck"</td></tr>

  <tr><td>8</td><td><span class="heb">נֻתַּץ</span></td><td>Jdg 6:28</td>
    <td><input class="parse-field" id="a8g"></td><td><input class="parse-field" id="a8p"></td><td><input class="parse-field" id="a8r"></td>
    <td><button class="reveal-btn" onclick="toggle('r8')">▶</button></td></tr>
  <tr class="answer-row" id="r8"><td colspan="7"><strong>Perfect · 3ms · נָתַץ</strong> — was torn down/demolished; nun assimilated → dagesh forte in ת (R2); qibbuts under נ position; patach final — Pual perfect 3ms; Gideon's father's altar was demolished</td></tr>

  <tr><td>9</td><td><span class="heb">יֻכַּה</span></td><td>2 Sam 11:15</td>
    <td><input class="parse-field" id="a9g"></td><td><input class="parse-field" id="a9p"></td><td><input class="parse-field" id="a9r"></td>
    <td><button class="reveal-btn" onclick="toggle('r9')">▶</button></td></tr>
  <tr class="answer-row" id="r9"><td colspan="7"><strong>Imperfect · 3ms · נָכָה</strong> — let him be struck down; nun assimilated → dagesh forte in כ; qibbuts under יּ prefix; III-he Pual imperfect; David's command to expose Uriah in battle</td></tr>
</table></div>

<div class="section-label">Group 3 — I-guttural</div>
<div style="overflow-x:auto;max-width:100%;"><table>
  <tr><th>#</th><th>Form</th><th>Reference</th><th>Conjugation</th><th>PGN</th><th>Root</th><th></th></tr>

  <tr><td>10</td><td><span class="heb">עֻבַּד</span></td><td>Dan 3:12</td>
    <td><input class="parse-field" id="a10g"></td><td><input class="parse-field" id="a10p"></td><td><input class="parse-field" id="a10r"></td>
    <td><button class="reveal-btn" onclick="toggle('r10')">▶</button></td></tr>
  <tr class="answer-row" id="r10"><td colspan="7"><strong>Perfect · 3ms · עָבַד</strong> — it was served/worshipped; qibbuts under ע (I-guttural: ע accepts qibbuts); dagesh forte in ב (R2); patach final; the accusation: the idol was not served by these men</td></tr>

  <tr><td>11</td><td><span class="heb">אֹרָשָׂה</span></td><td>Exo 22:15</td>
    <td><input class="parse-field" id="a11g"></td><td><input class="parse-field" id="a11p"></td><td><input class="parse-field" id="a11r"></td>
    <td><button class="reveal-btn" onclick="toggle('r11')">▶</button></td></tr>
  <tr class="answer-row" id="r11"><td colspan="7"><strong>Perfect · 3fs · אָרַשׂ</strong> — she was betrothed; I-aleph + ר (both reject dagesh forte): chain compensatory lengthening produces holem (אֹ) under א; qamets under ר; III-he: qamets + ה fs ending</td></tr>

  <tr><td>12</td><td><span class="heb">הֻמַּת</span></td><td>Jdg 6:30</td>
    <td><input class="parse-field" id="a12g"></td><td><input class="parse-field" id="a12p"></td><td><input class="parse-field" id="a12r"></td>
    <td><button class="reveal-btn" onclick="toggle('r12')">▶</button></td></tr>
  <tr class="answer-row" id="r12"><td colspan="7"><strong>Hophal · Perfect · 3ms · מוּת</strong> — he must be put to death; qibbuts under הֻ (Hophal prefix); I-nun/biconsonantal: מ of מוּת is not standard R1 in Hophal; Hophal (not Pual): הֻ prefix identifies it as Hophal passive; compare Pual which has qibbuts under root R1 directly</td></tr>
</table></div>

<div class="section-label">Group 4 — Geminate</div>
<div style="overflow-x:auto;max-width:100%;"><table>
  <tr><th>#</th><th>Form</th><th>Reference</th><th>Conjugation</th><th>PGN</th><th>Root</th><th></th></tr>

  <tr><td>13</td><td><span class="heb">מְהֻלָּל</span></td><td>Ps 18:4</td>
    <td><input class="parse-field" id="a13g"></td><td><input class="parse-field" id="a13p"></td><td><input class="parse-field" id="a13r"></td>
    <td><button class="reveal-btn" onclick="toggle('r13')">▶</button></td></tr>
  <tr class="answer-row" id="r13"><td colspan="7"><strong>Participle · ms · הָלַל</strong> — worthy of praise; Pual passive participle: מְ + qibbuts under הֻ (R1) + dagesh forte in ל (R2=R3 Geminate) + tsere; "The LORD is worthy of praise"</td></tr>

  <tr><td>14</td><td><span class="heb">גֻּנַּב</span></td><td>Gen 40:15</td>
    <td><input class="parse-field" id="a14g"></td><td><input class="parse-field" id="a14p"></td><td><input class="parse-field" id="a14r"></td>
    <td><button class="reveal-btn" onclick="toggle('r14')">▶</button></td></tr>
  <tr class="answer-row" id="r14"><td colspan="7"><strong>Perfect · 3ms · גָּנַב</strong> — was stolen; qibbuts under ג + dagesh forte in נ (R2); patach final — Pual perfect 3ms; Joseph to the cupbearer: "I was indeed stolen from the land of the Hebrews"</td></tr>

  <tr><td>15</td><td><span class="heb">יְאֻשַּׁר</span></td><td>Ps 41:3</td>
    <td><input class="parse-field" id="a15g"></td><td><input class="parse-field" id="a15p"></td><td><input class="parse-field" id="a15r"></td>
    <td><button class="reveal-btn" onclick="toggle('r15')">▶</button></td></tr>
  <tr class="answer-row" id="r15"><td colspan="7"><strong>Imperfect · 3ms · אָשַׁר</strong> — he will be called blessed/happy; qibbuts under א (I-aleph accepts qibbuts); dagesh forte in שׁ (R2); patach final — Pual imperfect; "Happy is he who considers the poor"</td></tr>
</table></div>

<!-- PART B -->
<h2>Part B — Mixed</h2>
<p>Identify the weak class first, then parse fully.</p>

<div style="overflow-x:auto;max-width:100%;"><table>
  <tr><th>#</th><th>Form</th><th>Reference</th><th>Weak class</th><th>Conjugation</th><th>PGN</th><th>Root</th><th></th></tr>

  <tr><td>16</td><td><span class="heb">נֻכָּה</span></td><td>Exo 9:31</td>
    <td><input class="parse-field" id="b16c"></td><td><input class="parse-field" id="b16g"></td><td><input class="parse-field" id="b16p"></td><td><input class="parse-field" id="b16r"></td>
    <td><button class="reveal-btn" onclick="toggle('rb16')">▶</button></td></tr>
  <tr class="answer-row" id="rb16"><td colspan="8"><strong>I-nun + III-he · Perfect · 3fs · נָכָה</strong> — it was struck; nun assimilated → dagesh in כ; qibbuts under נ position; III-he qamets + ה fs ending</td></tr>

  <tr><td>17</td><td><span class="heb">יְכֻסּוּ</span></td><td>Gen 7:20</td>
    <td><input class="parse-field" id="b17c"></td><td><input class="parse-field" id="b17g"></td><td><input class="parse-field" id="b17p"></td><td><input class="parse-field" id="b17r"></td>
    <td><button class="reveal-btn" onclick="toggle('rb17')">▶</button></td></tr>
  <tr class="answer-row" id="rb17"><td colspan="8"><strong>III-he · Wayyiqtol · 3mp · כָּסָה</strong> — they were covered; qibbuts under כ; dagesh forte in ס; III-he Pual 3mp shureq ending</td></tr>

  <tr><td>18</td><td><span class="heb">כֻּלָּה</span></td><td>Isa 24:10</td>
    <td><input class="parse-field" id="b18c"></td><td><input class="parse-field" id="b18g"></td><td><input class="parse-field" id="b18p"></td><td><input class="parse-field" id="b18r"></td>
    <td><button class="reveal-btn" onclick="toggle('rb18')">▶</button></td></tr>
  <tr class="answer-row" id="rb18"><td colspan="8"><strong>III-he · Perfect · 3fs · כָּלָה</strong> — it was devastated; qibbuts under כ; dagesh forte in ל; III-he qamets + ה ending</td></tr>

  <tr><td>19</td><td><span class="heb">גֻּנַּב</span></td><td>Gen 40:15</td>
    <td><input class="parse-field" id="b19c"></td><td><input class="parse-field" id="b19g"></td><td><input class="parse-field" id="b19p"></td><td><input class="parse-field" id="b19r"></td>
    <td><button class="reveal-btn" onclick="toggle('rb19')">▶</button></td></tr>
  <tr class="answer-row" id="rb19"><td colspan="8"><strong>Strong · Perfect · 3ms · גָּנַב</strong> — was stolen; qibbuts under ג + dagesh forte in נ; standard strong Pual perfect 3ms</td></tr>

  <tr><td>20</td><td><span class="heb">יֻכַּה</span></td><td>2 Sam 11:15</td>
    <td><input class="parse-field" id="b20c"></td><td><input class="parse-field" id="b20g"></td><td><input class="parse-field" id="b20p"></td><td><input class="parse-field" id="b20r"></td>
    <td><button class="reveal-btn" onclick="toggle('rb20')">▶</button></td></tr>
  <tr class="answer-row" id="rb20"><td colspan="8"><strong>I-nun + III-he · Imperfect · 3ms · נָכָה</strong> — let him be struck; nun assimilated → dagesh in כ; qibbuts under prefix יּ; III-he Pual imperfect</td></tr>

  <tr><td>21</td><td><span class="heb">צֻוֵּיתָ</span></td><td>Gen 45:19</td>
    <td><input class="parse-field" id="b21c"></td><td><input class="parse-field" id="b21g"></td><td><input class="parse-field" id="b21p"></td><td><input class="parse-field" id="b21r"></td>
    <td><button class="reveal-btn" onclick="toggle('rb21')">▶</button></td></tr>
  <tr class="answer-row" id="rb21"><td colspan="8"><strong>III-he · Perfect · 2ms · צָוָה</strong> — you have been commanded; qibbuts under צ + dagesh forte in ו; III-he Pual perfect 2ms with tsere-yod before suffix</td></tr>

  <tr><td>22</td><td><span class="heb">מְהֻלָּל</span></td><td>Ps 18:4</td>
    <td><input class="parse-field" id="b22c"></td><td><input class="parse-field" id="b22g"></td><td><input class="parse-field" id="b22p"></td><td><input class="parse-field" id="b22r"></td>
    <td><button class="reveal-btn" onclick="toggle('rb22')">▶</button></td></tr>
  <tr class="answer-row" id="rb22"><td colspan="8"><strong>Geminate · Participle · ms · הָלַל</strong> — worthy of praise; Pual passive participle; מְ + qibbuts under ה (R1) + dagesh forte in ל (R2=R3); tsere final</td></tr>

  <tr><td>23</td><td><span class="heb">עֻבַּד</span></td><td>Dan 3:12</td>
    <td><input class="parse-field" id="b23c"></td><td><input class="parse-field" id="b23g"></td><td><input class="parse-field" id="b23p"></td><td><input class="parse-field" id="b23r"></td>
    <td><button class="reveal-btn" onclick="toggle('rb23')">▶</button></td></tr>
  <tr class="answer-row" id="rb23"><td colspan="8"><strong>I-guttural · Perfect · 3ms · עָבַד</strong> — was served/worshipped; qibbuts under ע (guttural accepts qibbuts); dagesh forte in ב; patach final</td></tr>

  <tr><td>24</td><td><span class="heb">נֻתַּץ</span></td><td>Jdg 6:28</td>
    <td><input class="parse-field" id="b24c"></td><td><input class="parse-field" id="b24g"></td><td><input class="parse-field" id="b24p"></td><td><input class="parse-field" id="b24r"></td>
    <td><button class="reveal-btn" onclick="toggle('rb24')">▶</button></td></tr>
  <tr class="answer-row" id="rb24"><td colspan="8"><strong>I-nun · Perfect · 3ms · נָתַץ</strong> — was torn down; nun assimilated → dagesh forte in ת; qibbuts under נ position; patach final</td></tr>

  <tr><td>25</td><td><span class="heb">כֻּסָּה</span></td><td>Exo 15:5</td>
    <td><input class="parse-field" id="b25c"></td><td><input class="parse-field" id="b25g"></td><td><input class="parse-field" id="b25p"></td><td><input class="parse-field" id="b25r"></td>
    <td><button class="reveal-btn" onclick="toggle('rb25')">▶</button></td></tr>
  <tr class="answer-row" id="rb25"><td colspan="8"><strong>III-he · Perfect · 3ms · כָּסָה</strong> — it was covered; qibbuts under כ + dagesh forte in ס; III-he qamets + ה ending</td></tr>
</table></div>

<h2>Discussion Questions</h2>
<div class="discussion">
  <ol class="disc">
    <li>Items 1–2 (<span class="heb">כָּלָה</span> and <span class="heb">כָּסָה</span>, both III-he Pual wayyiqtol 3mp) end in the shureq (וּ) plural ending. Compare these to the Piel wayyiqtol 3mp of the same roots. Does the Pual 3mp ending differ from the Piel 3mp ending? What changes between Piel and Pual in these III-he forms, and what stays the same?</li>
    <li>Items 6–9 (I-nun Pual) show nun assimilating into a dagesh forte in R2. In the Piel of the same I-nun roots (e.g., <span class="heb">יְנַחֵם</span> from נָחַם), the nun does NOT assimilate. Explain the difference in behavior. What is the structural reason the Piel retains the nun while the Pual allows assimilation?</li>
    <li>Item 11 (<span class="heb">אֹרָשָׂה</span>, I-aleph Pual): the expected Pual qibbuts under R1 does not appear in the expected place. Instead there is a holem (אֹ). Explain the chain of compensatory lengthening that produces this unusual vowel. Consider: what normally happens under R1 in the Pual, and then what happens when both R1 (aleph) and R2 (resh) reject the dagesh forte?</li>
    <li>How would you distinguish a Pual perfect 3ms (e.g., <span class="heb">כֻּסָּה</span> from כָּסָה) from a Niphal perfect 3ms (e.g., <span class="heb">נִגְלָה</span> from גָּלָה)? List two features that differentiate them, independent of root identification.</li>
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

