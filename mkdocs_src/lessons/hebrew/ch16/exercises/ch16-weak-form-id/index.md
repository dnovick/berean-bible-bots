# Weak Form Id

*Chapter 16 — Qal Imperfect Weak Verbs*

[Full screen](ch16-weak-form-id.html){.md-button}  [Markdown](ch16-weak-form-id.md){.md-button}  [Print (PDF)](ch16-weak-form-id.pdf){.md-button}

<style>

  body { font-family: Georgia, serif;    color: #222; line-height: 1.6; }
  h1 { font-size: 1.45rem; border-bottom: 2px solid #555; padding-bottom: .4rem; }
  h2 { font-size: 1.05rem; margin-top: 2rem; color: #333; border-bottom: 1px solid #ddd; padding-bottom: .2rem; }
  h3 { font-size: .97rem; margin-top: 1.5rem; color: #445; }
  .subtitle { color: #666; font-style: italic; margin-top: -.4rem; }
  .instructions { background: #f8f8f0; border-left: 4px solid #bbb; padding: .75rem 1rem; margin: 1rem 0; font-size: .92rem; }
  .hint { background: #fff8e8; border-left: 3px solid #d4a017; padding: .35rem .75rem; margin: .4rem 0 .6rem; font-size: .86rem; color: #5a3e00; }
  table { border-collapse: collapse; width: 100%; margin: .4rem 0; font-size: .89rem; }
  th { background: #e0e8f0; padding: .36rem .45rem; border: 1px solid #bbb; text-align: left; font-size: .82rem; }
  td { padding: .26rem .38rem; border: 1px solid #ddd; vertical-align: middle; }
  td.num { text-align: center; font-weight: bold; color: #666; width: 2rem; }
  td.heb { font-size: 1.12rem; direction: rtl; unicode-bidi: embed; font-weight: bold; width: 8rem; }
  input.f { width: 100%; box-sizing: border-box; border: 1px solid #bbb; border-radius: 3px; padding: .2rem .35rem; font-family: Georgia, serif; font-size: .85rem; background: #fafff8; }
  input.f:focus { outline: none; border-color: #5a9; box-shadow: 0 0 0 2px #c8ecd4; }
  .ans-row { display: none; background: #f0faf0; }
  .ans-row td { font-size: .85rem; color: #2a6e2a; padding: .24rem .38rem; }
  .ans-lbl { font-weight: bold; color: #1a5c1a; width: 2rem; text-align: center; }
  .ans-heb { font-size: 1rem; direction: rtl; unicode-bidi: embed; }
  button.rbtn { font-size: .74rem; padding: .12rem .44rem; cursor: pointer; background: #e8f4ec; border: 1px solid #7bba8f; border-radius: 3px; color: #2a6e2a; white-space: nowrap; }
  button.rbtn:hover, button.rbtn.on { background: #c8ecd4; }
  .controls { display: flex; gap: .7rem; flex-wrap: wrap; margin: 1rem 0 1.5rem; }
  .controls button { padding: .38rem .85rem; cursor: pointer; border-radius: 4px; font-size: .88rem; border: 1px solid #999; background: #f0f0f0; color: #333; }
  .controls button:hover { background: #ddd; }
  .clr { border-color: #c06060 !important; color: #8b0000 !important; background: #fff0f0 !important; }
  .clr:hover { background: #ffd8d8 !important; }
  hr.sec { border: none; border-top: 2px dashed #ccc; margin: 2rem 0; }
  .disc { background: #f4f4ff; border-left: 4px solid #99a; padding: .75rem 1rem; margin: 1.5rem 0; font-size: .9rem; }
  .disc ol { margin: .4rem 0; padding-left: 1.4rem; }
  .disc li { margin-bottom: .5rem; }
  @media print { .controls, button.rbtn { display: none; } input.f { border: none; border-bottom: 1px solid #aaa; border-radius: 0; background: transparent; } .ans-row { display: none !important; } }

/* ── inline-embed overrides ── */
table { table-layout: fixed !important; width: 100% !important; }
th, td { word-break: break-word; overflow-wrap: break-word; }
th { font-size: .78rem !important; white-space: normal !important; }
td { font-size: .82rem !important; }
td.num, td.num-cell, td.ans-lbl { width: 1.8rem !important; }
td.heb { font-size: 1.2em !important; width: auto !important; }
button.rbtn, button.reveal-btn, button.btn-answer, button.btn-reveal,
button.tog { white-space: normal !important; font-size: .72rem !important;
  padding: .1rem .3rem !important; }
input.parse-field, input.f { font-size: .8rem !important; }
select.parse-field { font-size: .8rem !important; }

</style>

<h1>Ch16 Weak Form ID Drill — Qal Imperfect Weak Verbs</h1>
<p class="subtitle">BBH Chapter 16 · 50 forms</p>

<div class="instructions">
  <strong>Instructions:</strong> For each form, identify: (a) Weak Class, (b) Person, (c) Number, (d) Gender, (e) Root.<br>
  <em>Part A: forms are grouped by class with a diagnostic hint. Part B: mixed — identify the class first.</em>
</div>

<div class="controls">
  <button onclick="showAll()">Show All Answers</button>
  <button onclick="hideAll()">Hide All Answers</button>
  <button class="clr" onclick="clearAll()">Clear All Inputs</button>
</div>

<!-- PART A -->
<h2>Part A — By Weak Class</h2>

<!-- GROUP 1 -->
<h3>Group 1: III-ה (Lamed-He)</h3>
<div class="hint">Diagnostic: long form ends in -ֶה (seghol + he); short Jussive drops the ה.</div>
<table>
  <tr><th>#</th><th>Form</th><th>Weak Class</th><th>Pers.</th><th>Num.</th><th>Gen.</th><th>Root</th><th></th></tr>
  <tr>
    <td class="num">1</td><td class="heb">יִבְנֶה</td>
    <td><input class="parse-field" id="1-wc" placeholder="class"></td><td><input class="parse-field" id="1-p" placeholder="1/2/3"></td><td><input class="parse-field" id="1-n" placeholder="s/p"></td><td><input class="parse-field" id="1-g" placeholder="m/f/c"></td><td><input class="parse-field" id="1-r" placeholder="root"></td>
    <td><button class="rbtn" onclick="tog(1)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-1"><td class="ans-lbl">✓</td><td class="ans-heb">יִבְנֶה</td><td>III-ה</td><td>3</td><td>s</td><td>m</td><td class="ans-heb">בָּנָה</td><td>Seghol-he ending; long form</td></tr>
  <tr>
    <td class="num">2</td><td class="heb">תַּעֲשֶׂה</td>
    <td><input class="parse-field" id="2-wc" placeholder="class"></td><td><input class="parse-field" id="2-p" placeholder="1/2/3"></td><td><input class="parse-field" id="2-n" placeholder="s/p"></td><td><input class="parse-field" id="2-g" placeholder="m/f/c"></td><td><input class="parse-field" id="2-r" placeholder="root"></td>
    <td><button class="rbtn" onclick="tog(2)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-2"><td class="ans-lbl">✓</td><td class="ans-heb">תַּעֲשֶׂה</td><td>III-ה</td><td>3/2</td><td>s</td><td>f/m</td><td class="ans-heb">עָשָׂה</td><td>I-gutt. (ע) also; chateph prefix</td></tr>
  <tr>
    <td class="num">3</td><td class="heb">יִהְיֶה</td>
    <td><input class="parse-field" id="3-wc" placeholder="class"></td><td><input class="parse-field" id="3-p" placeholder="1/2/3"></td><td><input class="parse-field" id="3-n" placeholder="s/p"></td><td><input class="parse-field" id="3-g" placeholder="m/f/c"></td><td><input class="parse-field" id="3-r" placeholder="root"></td>
    <td><button class="rbtn" onclick="tog(3)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-3"><td class="ans-lbl">✓</td><td class="ans-heb">יִהְיֶה</td><td>III-ה</td><td>3</td><td>s</td><td>m</td><td class="ans-heb">הָיָה</td><td>Most common III-ה Imperfect</td></tr>
  <tr>
    <td class="num">4</td><td class="heb">תִּרְאֶה</td>
    <td><input class="parse-field" id="4-wc" placeholder="class"></td><td><input class="parse-field" id="4-p" placeholder="1/2/3"></td><td><input class="parse-field" id="4-n" placeholder="s/p"></td><td><input class="parse-field" id="4-g" placeholder="m/f/c"></td><td><input class="parse-field" id="4-r" placeholder="root"></td>
    <td><button class="rbtn" onclick="tog(4)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-4"><td class="ans-lbl">✓</td><td class="ans-heb">תִּרְאֶה</td><td>III-ה</td><td>3/2</td><td>s</td><td>f/m</td><td class="ans-heb">רָאָה</td><td>III-ה + I-gutt. (ר light); seghol-he</td></tr>
  <tr>
    <td class="num">5</td><td class="heb">יִבֶּן</td>
    <td><input class="parse-field" id="5-wc" placeholder="class"></td><td><input class="parse-field" id="5-p" placeholder="1/2/3"></td><td><input class="parse-field" id="5-n" placeholder="s/p"></td><td><input class="parse-field" id="5-g" placeholder="m/f/c"></td><td><input class="parse-field" id="5-r" placeholder="root"></td>
    <td><button class="rbtn" onclick="tog(5)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-5"><td class="ans-lbl">✓</td><td class="ans-heb">יִבֶּן</td><td>III-ה</td><td>3</td><td>s</td><td>m</td><td class="ans-heb">בָּנָה</td><td>Short Jussive — ה dropped, vowel shortens to seghol</td></tr>
</table>

<!-- GROUP 2 -->
<h3>Group 2: III-א (Lamed-Aleph)</h3>
<div class="hint">Diagnostic: form ends in silent א; preceding vowel is often qamets.</div>
<table>
  <tr><th>#</th><th>Form</th><th>Weak Class</th><th>Pers.</th><th>Num.</th><th>Gen.</th><th>Root</th><th></th></tr>
  <tr>
    <td class="num">6</td><td class="heb">יִמְצָא</td>
    <td><input class="parse-field" id="6-wc" placeholder="class"></td><td><input class="parse-field" id="6-p" placeholder="1/2/3"></td><td><input class="parse-field" id="6-n" placeholder="s/p"></td><td><input class="parse-field" id="6-g" placeholder="m/f/c"></td><td><input class="parse-field" id="6-r" placeholder="root"></td>
    <td><button class="rbtn" onclick="tog(6)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-6"><td class="ans-lbl">✓</td><td class="ans-heb">יִמְצָא</td><td>III-א</td><td>3</td><td>s</td><td>m</td><td class="ans-heb">מָצָא</td><td>Silent aleph; preceding qamets</td></tr>
  <tr>
    <td class="num">7</td><td class="heb">תִּקְרָא</td>
    <td><input class="parse-field" id="7-wc" placeholder="class"></td><td><input class="parse-field" id="7-p" placeholder="1/2/3"></td><td><input class="parse-field" id="7-n" placeholder="s/p"></td><td><input class="parse-field" id="7-g" placeholder="m/f/c"></td><td><input class="parse-field" id="7-r" placeholder="root"></td>
    <td><button class="rbtn" onclick="tog(7)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-7"><td class="ans-lbl">✓</td><td class="ans-heb">תִּקְרָא</td><td>III-א</td><td>3/2</td><td>s</td><td>f/m</td><td class="ans-heb">קָרָא</td><td>Silent aleph; qamets before א</td></tr>
  <tr>
    <td class="num">8</td><td class="heb">אֶמְצָא</td>
    <td><input class="parse-field" id="8-wc" placeholder="class"></td><td><input class="parse-field" id="8-p" placeholder="1/2/3"></td><td><input class="parse-field" id="8-n" placeholder="s/p"></td><td><input class="parse-field" id="8-g" placeholder="m/f/c"></td><td><input class="parse-field" id="8-r" placeholder="root"></td>
    <td><button class="rbtn" onclick="tog(8)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-8"><td class="ans-lbl">✓</td><td class="ans-heb">אֶמְצָא</td><td>III-א</td><td>1</td><td>s</td><td>c</td><td class="ans-heb">מָצָא</td><td>1cs prefix (aleph) + silent final aleph</td></tr>
  <tr>
    <td class="num">9</td><td class="heb">יִמְצְאוּ</td>
    <td><input class="parse-field" id="9-wc" placeholder="class"></td><td><input class="parse-field" id="9-p" placeholder="1/2/3"></td><td><input class="parse-field" id="9-n" placeholder="s/p"></td><td><input class="parse-field" id="9-g" placeholder="m/f/c"></td><td><input class="parse-field" id="9-r" placeholder="root"></td>
    <td><button class="rbtn" onclick="tog(9)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-9"><td class="ans-lbl">✓</td><td class="ans-heb">יִמְצְאוּ</td><td>III-א</td><td>3</td><td>p</td><td>m</td><td class="ans-heb">מָצָא</td><td>3mp -וּ suffix; aleph visible</td></tr>
  <tr>
    <td class="num">10</td><td class="heb">נִקְרָא</td>
    <td><input class="parse-field" id="10-wc" placeholder="class"></td><td><input class="parse-field" id="10-p" placeholder="1/2/3"></td><td><input class="parse-field" id="10-n" placeholder="s/p"></td><td><input class="parse-field" id="10-g" placeholder="m/f/c"></td><td><input class="parse-field" id="10-r" placeholder="root"></td>
    <td><button class="rbtn" onclick="tog(10)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-10"><td class="ans-lbl">✓</td><td class="ans-heb">נִקְרָא</td><td>III-א</td><td>1</td><td>p</td><td>c</td><td class="ans-heb">קָרָא</td><td>1cp nun prefix; qamets-aleph ending</td></tr>
</table>

<!-- GROUP 3 -->
<h3>Group 3: III-ח/ע (Lamed-Guttural)</h3>
<div class="hint">Diagnostic: long 3ms/3fs ends in patach furtive before ח or ע; short/wayyiqtol: closed syllable, no furtive.</div>
<table>
  <tr><th>#</th><th>Form</th><th>Weak Class</th><th>Pers.</th><th>Num.</th><th>Gen.</th><th>Root</th><th></th></tr>
  <tr>
    <td class="num">11</td><td class="heb">יִשְׁלַחַ</td>
    <td><input class="parse-field" id="11-wc" placeholder="class"></td><td><input class="parse-field" id="11-p" placeholder="1/2/3"></td><td><input class="parse-field" id="11-n" placeholder="s/p"></td><td><input class="parse-field" id="11-g" placeholder="m/f/c"></td><td><input class="parse-field" id="11-r" placeholder="root"></td>
    <td><button class="rbtn" onclick="tog(11)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-11"><td class="ans-lbl">✓</td><td class="ans-heb">יִשְׁלַחַ</td><td>III-ח</td><td>3</td><td>s</td><td>m</td><td class="ans-heb">שָׁלַח</td><td>Patach furtive before ח; long form</td></tr>
  <tr>
    <td class="num">12</td><td class="heb">תִּשְׁמַעַ</td>
    <td><input class="parse-field" id="12-wc" placeholder="class"></td><td><input class="parse-field" id="12-p" placeholder="1/2/3"></td><td><input class="parse-field" id="12-n" placeholder="s/p"></td><td><input class="parse-field" id="12-g" placeholder="m/f/c"></td><td><input class="parse-field" id="12-r" placeholder="root"></td>
    <td><button class="rbtn" onclick="tog(12)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-12"><td class="ans-lbl">✓</td><td class="ans-heb">תִּשְׁמַעַ</td><td>III-ע</td><td>3/2</td><td>s</td><td>f/m</td><td class="ans-heb">שָׁמַע</td><td>Patach furtive before ע; long form</td></tr>
  <tr>
    <td class="num">13</td><td class="heb">וַיִּשְׁמַע</td>
    <td><input class="parse-field" id="13-wc" placeholder="class"></td><td><input class="parse-field" id="13-p" placeholder="1/2/3"></td><td><input class="parse-field" id="13-n" placeholder="s/p"></td><td><input class="parse-field" id="13-g" placeholder="m/f/c"></td><td><input class="parse-field" id="13-r" placeholder="root"></td>
    <td><button class="rbtn" onclick="tog(13)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-13"><td class="ans-lbl">✓</td><td class="ans-heb">וַיִּשְׁמַע</td><td>III-ע</td><td>3</td><td>s</td><td>m</td><td class="ans-heb">שָׁמַע</td><td>Wayyiqtol short form; no furtive; syllable closed</td></tr>
  <tr>
    <td class="num">14</td><td class="heb">יִשְׁלְחוּ</td>
    <td><input class="parse-field" id="14-wc" placeholder="class"></td><td><input class="parse-field" id="14-p" placeholder="1/2/3"></td><td><input class="parse-field" id="14-n" placeholder="s/p"></td><td><input class="parse-field" id="14-g" placeholder="m/f/c"></td><td><input class="parse-field" id="14-r" placeholder="root"></td>
    <td><button class="rbtn" onclick="tog(14)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-14"><td class="ans-lbl">✓</td><td class="ans-heb">יִשְׁלְחוּ</td><td>III-ח</td><td>3</td><td>p</td><td>m</td><td class="ans-heb">שָׁלַח</td><td>3mp; no furtive before suffix</td></tr>
  <tr>
    <td class="num">15</td><td class="heb">אֶשְׁמַע</td>
    <td><input class="parse-field" id="15-wc" placeholder="class"></td><td><input class="parse-field" id="15-p" placeholder="1/2/3"></td><td><input class="parse-field" id="15-n" placeholder="s/p"></td><td><input class="parse-field" id="15-g" placeholder="m/f/c"></td><td><input class="parse-field" id="15-r" placeholder="root"></td>
    <td><button class="rbtn" onclick="tog(15)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-15"><td class="ans-lbl">✓</td><td class="ans-heb">אֶשְׁמַע</td><td>III-ע</td><td>1</td><td>s</td><td>c</td><td class="ans-heb">שָׁמַע</td><td>1cs; B-class patach; guttural at R3 closes syllable</td></tr>
</table>

<!-- GROUP 4 -->
<h3>Group 4: I-Guttural (Pe-Guttural)</h3>
<div class="hint">Diagnostic: patach under prefix consonant (not hireq); chateph-patach under R1 guttural.</div>
<table>
  <tr><th>#</th><th>Form</th><th>Weak Class</th><th>Pers.</th><th>Num.</th><th>Gen.</th><th>Root</th><th></th></tr>
  <tr>
    <td class="num">16</td><td class="heb">יַעֲמֹד</td>
    <td><input class="parse-field" id="16-wc" placeholder="class"></td><td><input class="parse-field" id="16-p" placeholder="1/2/3"></td><td><input class="parse-field" id="16-n" placeholder="s/p"></td><td><input class="parse-field" id="16-g" placeholder="m/f/c"></td><td><input class="parse-field" id="16-r" placeholder="root"></td>
    <td><button class="rbtn" onclick="tog(16)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-16"><td class="ans-lbl">✓</td><td class="ans-heb">יַעֲמֹד</td><td>I-gutt.</td><td>3</td><td>s</td><td>m</td><td class="ans-heb">עָמַד</td><td>Patach prefix; chateph-patach under ע</td></tr>
  <tr>
    <td class="num">17</td><td class="heb">תַּחֲלֹם</td>
    <td><input class="parse-field" id="17-wc" placeholder="class"></td><td><input class="parse-field" id="17-p" placeholder="1/2/3"></td><td><input class="parse-field" id="17-n" placeholder="s/p"></td><td><input class="parse-field" id="17-g" placeholder="m/f/c"></td><td><input class="parse-field" id="17-r" placeholder="root"></td>
    <td><button class="rbtn" onclick="tog(17)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-17"><td class="ans-lbl">✓</td><td class="ans-heb">תַּחֲלֹם</td><td>I-gutt.</td><td>3/2</td><td>s</td><td>f/m</td><td class="ans-heb">חָלַם</td><td>Patach prefix; chateph under ח</td></tr>
  <tr>
    <td class="num">18</td><td class="heb">יֹאמַר</td>
    <td><input class="parse-field" id="18-wc" placeholder="class"></td><td><input class="parse-field" id="18-p" placeholder="1/2/3"></td><td><input class="parse-field" id="18-n" placeholder="s/p"></td><td><input class="parse-field" id="18-g" placeholder="m/f/c"></td><td><input class="parse-field" id="18-r" placeholder="root"></td>
    <td><button class="rbtn" onclick="tog(18)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-18"><td class="ans-lbl">✓</td><td class="ans-heb">יֹאמַר</td><td>I-gutt. (א)</td><td>3</td><td>s</td><td>m</td><td class="ans-heb">אָמַר</td><td>Holem prefix (special for aleph); must memorize</td></tr>
  <tr>
    <td class="num">19</td><td class="heb">תַּעַמְדוּ</td>
    <td><input class="parse-field" id="19-wc" placeholder="class"></td><td><input class="parse-field" id="19-p" placeholder="1/2/3"></td><td><input class="parse-field" id="19-n" placeholder="s/p"></td><td><input class="parse-field" id="19-g" placeholder="m/f/c"></td><td><input class="parse-field" id="19-r" placeholder="root"></td>
    <td><button class="rbtn" onclick="tog(19)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-19"><td class="ans-lbl">✓</td><td class="ans-heb">תַּעַמְדוּ</td><td>I-gutt.</td><td>2</td><td>p</td><td>m</td><td class="ans-heb">עָמַד</td><td>Patach prefix; chateph resolves before suffix</td></tr>
  <tr>
    <td class="num">20</td><td class="heb">נַעֲמֹד</td>
    <td><input class="parse-field" id="20-wc" placeholder="class"></td><td><input class="parse-field" id="20-p" placeholder="1/2/3"></td><td><input class="parse-field" id="20-n" placeholder="s/p"></td><td><input class="parse-field" id="20-g" placeholder="m/f/c"></td><td><input class="parse-field" id="20-r" placeholder="root"></td>
    <td><button class="rbtn" onclick="tog(20)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-20"><td class="ans-lbl">✓</td><td class="ans-heb">נַעֲמֹד</td><td>I-gutt.</td><td>1</td><td>p</td><td>c</td><td class="ans-heb">עָמַד</td><td>1cp nun prefix + patach/chateph pattern</td></tr>
</table>

<!-- GROUP 5 -->
<h3>Group 5: I-נ (Pe-Nun)</h3>
<div class="hint">Diagnostic: unexpected dagesh forte in R2 (nun assimilated); tsere or holem in root.</div>
<table>
  <tr><th>#</th><th>Form</th><th>Weak Class</th><th>Pers.</th><th>Num.</th><th>Gen.</th><th>Root</th><th></th></tr>
  <tr>
    <td class="num">21</td><td class="heb">יִתֵּן</td>
    <td><input class="parse-field" id="21-wc" placeholder="class"></td><td><input class="parse-field" id="21-p" placeholder="1/2/3"></td><td><input class="parse-field" id="21-n" placeholder="s/p"></td><td><input class="parse-field" id="21-g" placeholder="m/f/c"></td><td><input class="parse-field" id="21-r" placeholder="root"></td>
    <td><button class="rbtn" onclick="tog(21)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-21"><td class="ans-lbl">✓</td><td class="ans-heb">יִתֵּן</td><td>I-נ</td><td>3</td><td>s</td><td>m</td><td class="ans-heb">נָתַן</td><td>Nun assimilated → dagesh forte in ת; tsere</td></tr>
  <tr>
    <td class="num">22</td><td class="heb">תִּתֵּן</td>
    <td><input class="parse-field" id="22-wc" placeholder="class"></td><td><input class="parse-field" id="22-p" placeholder="1/2/3"></td><td><input class="parse-field" id="22-n" placeholder="s/p"></td><td><input class="parse-field" id="22-g" placeholder="m/f/c"></td><td><input class="parse-field" id="22-r" placeholder="root"></td>
    <td><button class="rbtn" onclick="tog(22)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-22"><td class="ans-lbl">✓</td><td class="ans-heb">תִּתֵּן</td><td>I-נ</td><td>3/2</td><td>s</td><td>f/m</td><td class="ans-heb">נָתַן</td><td>Same assimilation pattern</td></tr>
  <tr>
    <td class="num">23</td><td class="heb">וַיִּתֵּן</td>
    <td><input class="parse-field" id="23-wc" placeholder="class"></td><td><input class="parse-field" id="23-p" placeholder="1/2/3"></td><td><input class="parse-field" id="23-n" placeholder="s/p"></td><td><input class="parse-field" id="23-g" placeholder="m/f/c"></td><td><input class="parse-field" id="23-r" placeholder="root"></td>
    <td><button class="rbtn" onclick="tog(23)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-23"><td class="ans-lbl">✓</td><td class="ans-heb">וַיִּתֵּן</td><td>I-נ</td><td>3</td><td>s</td><td>m</td><td class="ans-heb">נָתַן</td><td>Wayyiqtol; dagesh in ת still present</td></tr>
  <tr>
    <td class="num">24</td><td class="heb">יִפֹּל</td>
    <td><input class="parse-field" id="24-wc" placeholder="class"></td><td><input class="parse-field" id="24-p" placeholder="1/2/3"></td><td><input class="parse-field" id="24-n" placeholder="s/p"></td><td><input class="parse-field" id="24-g" placeholder="m/f/c"></td><td><input class="parse-field" id="24-r" placeholder="root"></td>
    <td><button class="rbtn" onclick="tog(24)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-24"><td class="ans-lbl">✓</td><td class="ans-heb">יִפֹּל</td><td>I-נ</td><td>3</td><td>s</td><td>m</td><td class="ans-heb">נָפַל</td><td>Nun assimilation → dagesh in פ; holem</td></tr>
  <tr>
    <td class="num">25</td><td class="heb">תִּתְּנוּ</td>
    <td><input class="parse-field" id="25-wc" placeholder="class"></td><td><input class="parse-field" id="25-p" placeholder="1/2/3"></td><td><input class="parse-field" id="25-n" placeholder="s/p"></td><td><input class="parse-field" id="25-g" placeholder="m/f/c"></td><td><input class="parse-field" id="25-r" placeholder="root"></td>
    <td><button class="rbtn" onclick="tog(25)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-25"><td class="ans-lbl">✓</td><td class="ans-heb">תִּתְּנוּ</td><td>I-נ</td><td>2</td><td>p</td><td>m</td><td class="ans-heb">נָתַן</td><td>Dagesh in ת; reduced vowel before plural suffix</td></tr>
</table>

<!-- GROUP 6 -->
<h3>Group 6: I-י (Pe-Yod)</h3>
<div class="hint">Diagnostic: tsere under the prefix consonant instead of hireq; R1 yod absent from the form.</div>
<table>
  <tr><th>#</th><th>Form</th><th>Weak Class</th><th>Pers.</th><th>Num.</th><th>Gen.</th><th>Root</th><th></th></tr>
  <tr>
    <td class="num">26</td><td class="heb">יֵדַע</td>
    <td><input class="parse-field" id="26-wc" placeholder="class"></td><td><input class="parse-field" id="26-p" placeholder="1/2/3"></td><td><input class="parse-field" id="26-n" placeholder="s/p"></td><td><input class="parse-field" id="26-g" placeholder="m/f/c"></td><td><input class="parse-field" id="26-r" placeholder="root"></td>
    <td><button class="rbtn" onclick="tog(26)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-26"><td class="ans-lbl">✓</td><td class="ans-heb">יֵדַע</td><td>I-י</td><td>3</td><td>s</td><td>m</td><td class="ans-heb">יָדַע</td><td>Tsere prefix (not hireq); yod R1 absent</td></tr>
  <tr>
    <td class="num">27</td><td class="heb">תֵּשֵׁב</td>
    <td><input class="parse-field" id="27-wc" placeholder="class"></td><td><input class="parse-field" id="27-p" placeholder="1/2/3"></td><td><input class="parse-field" id="27-n" placeholder="s/p"></td><td><input class="parse-field" id="27-g" placeholder="m/f/c"></td><td><input class="parse-field" id="27-r" placeholder="root"></td>
    <td><button class="rbtn" onclick="tog(27)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-27"><td class="ans-lbl">✓</td><td class="ans-heb">תֵּשֵׁב</td><td>I-י</td><td>3/2</td><td>s</td><td>f/m</td><td class="ans-heb">יָשַׁב</td><td>Tsere prefix; tsere under R2 (seghol class)</td></tr>
  <tr>
    <td class="num">28</td><td class="heb">וַיֵּלֶד</td>
    <td><input class="parse-field" id="28-wc" placeholder="class"></td><td><input class="parse-field" id="28-p" placeholder="1/2/3"></td><td><input class="parse-field" id="28-n" placeholder="s/p"></td><td><input class="parse-field" id="28-g" placeholder="m/f/c"></td><td><input class="parse-field" id="28-r" placeholder="root"></td>
    <td><button class="rbtn" onclick="tog(28)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-28"><td class="ans-lbl">✓</td><td class="ans-heb">וַיֵּלֶד</td><td>I-י</td><td>3</td><td>s</td><td>m</td><td class="ans-heb">יָלַד</td><td>Wayyiqtol; tsere prefix + waw-consecutive</td></tr>
  <tr>
    <td class="num">29</td><td class="heb">יֵצֵא</td>
    <td><input class="parse-field" id="29-wc" placeholder="class"></td><td><input class="parse-field" id="29-p" placeholder="1/2/3"></td><td><input class="parse-field" id="29-n" placeholder="s/p"></td><td><input class="parse-field" id="29-g" placeholder="m/f/c"></td><td><input class="parse-field" id="29-r" placeholder="root"></td>
    <td><button class="rbtn" onclick="tog(29)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-29"><td class="ans-lbl">✓</td><td class="ans-heb">יֵצֵא</td><td>I-י</td><td>3</td><td>s</td><td>m</td><td class="ans-heb">יָצָא</td><td>Tsere prefix; III-א also in play (aleph at R3)</td></tr>
  <tr>
    <td class="num">30</td><td class="heb">אֵלֵד</td>
    <td><input class="parse-field" id="30-wc" placeholder="class"></td><td><input class="parse-field" id="30-p" placeholder="1/2/3"></td><td><input class="parse-field" id="30-n" placeholder="s/p"></td><td><input class="parse-field" id="30-g" placeholder="m/f/c"></td><td><input class="parse-field" id="30-r" placeholder="root"></td>
    <td><button class="rbtn" onclick="tog(30)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-30"><td class="ans-lbl">✓</td><td class="ans-heb">אֵלֵד</td><td>I-י</td><td>1</td><td>s</td><td>c</td><td class="ans-heb">יָלַד</td><td>1cs; aleph prefix takes tsere (not seghol)</td></tr>
</table>

<!-- GROUP 7 -->
<h3>Group 7: Biconsonantal (II-י/ו)</h3>
<div class="hint">Diagnostic: qamets under prefix consonant; no R2 consonant visible; ו or י as middle element.</div>
<table>
  <tr><th>#</th><th>Form</th><th>Weak Class</th><th>Pers.</th><th>Num.</th><th>Gen.</th><th>Root</th><th></th></tr>
  <tr>
    <td class="num">31</td><td class="heb">יָקוּם</td>
    <td><input class="parse-field" id="31-wc" placeholder="class"></td><td><input class="parse-field" id="31-p" placeholder="1/2/3"></td><td><input class="parse-field" id="31-n" placeholder="s/p"></td><td><input class="parse-field" id="31-g" placeholder="m/f/c"></td><td><input class="parse-field" id="31-r" placeholder="root"></td>
    <td><button class="rbtn" onclick="tog(31)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-31"><td class="ans-lbl">✓</td><td class="ans-heb">יָקוּם</td><td>Biconsonantal</td><td>3</td><td>s</td><td>m</td><td class="ans-heb">קוּם</td><td>Qamets under prefix; shureq as middle vowel</td></tr>
  <tr>
    <td class="num">32</td><td class="heb">תָּבוֹא</td>
    <td><input class="parse-field" id="32-wc" placeholder="class"></td><td><input class="parse-field" id="32-p" placeholder="1/2/3"></td><td><input class="parse-field" id="32-n" placeholder="s/p"></td><td><input class="parse-field" id="32-g" placeholder="m/f/c"></td><td><input class="parse-field" id="32-r" placeholder="root"></td>
    <td><button class="rbtn" onclick="tog(32)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-32"><td class="ans-lbl">✓</td><td class="ans-heb">תָּבוֹא</td><td>Biconsonantal</td><td>3/2</td><td>s</td><td>f/m</td><td class="ans-heb">בּוֹא</td><td>Qamets prefix; holem-vav as middle vowel</td></tr>
  <tr>
    <td class="num">33</td><td class="heb">וַיָּבֹא</td>
    <td><input class="parse-field" id="33-wc" placeholder="class"></td><td><input class="parse-field" id="33-p" placeholder="1/2/3"></td><td><input class="parse-field" id="33-n" placeholder="s/p"></td><td><input class="parse-field" id="33-g" placeholder="m/f/c"></td><td><input class="parse-field" id="33-r" placeholder="root"></td>
    <td><button class="rbtn" onclick="tog(33)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-33"><td class="ans-lbl">✓</td><td class="ans-heb">וַיָּבֹא</td><td>Biconsonantal</td><td>3</td><td>s</td><td>m</td><td class="ans-heb">בּוֹא</td><td>Wayyiqtol; qamets under prefix</td></tr>
  <tr>
    <td class="num">34</td><td class="heb">יָמוּת</td>
    <td><input class="parse-field" id="34-wc" placeholder="class"></td><td><input class="parse-field" id="34-p" placeholder="1/2/3"></td><td><input class="parse-field" id="34-n" placeholder="s/p"></td><td><input class="parse-field" id="34-g" placeholder="m/f/c"></td><td><input class="parse-field" id="34-r" placeholder="root"></td>
    <td><button class="rbtn" onclick="tog(34)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-34"><td class="ans-lbl">✓</td><td class="ans-heb">יָמוּת</td><td>Biconsonantal</td><td>3</td><td>s</td><td>m</td><td class="ans-heb">מוּת</td><td>Qamets prefix; shureq middle; stative sense</td></tr>
  <tr>
    <td class="num">35</td><td class="heb">וַיָּקׇם</td>
    <td><input class="parse-field" id="35-wc" placeholder="class"></td><td><input class="parse-field" id="35-p" placeholder="1/2/3"></td><td><input class="parse-field" id="35-n" placeholder="s/p"></td><td><input class="parse-field" id="35-g" placeholder="m/f/c"></td><td><input class="parse-field" id="35-r" placeholder="root"></td>
    <td><button class="rbtn" onclick="tog(35)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-35"><td class="ans-lbl">✓</td><td class="ans-heb">וַיָּקׇם</td><td>Biconsonantal</td><td>3</td><td>s</td><td>m</td><td class="ans-heb">קוּם</td><td>Wayyiqtol; short form — qamets hatuf in root syllable</td></tr>
</table>

<!-- GROUP 8 -->
<h3>Group 8: Geminate (Ayin-Doubled)</h3>
<div class="hint">Diagnostic: dagesh forte in R2 (= R3); or short contracted form with qamets prefix. Root knowledge needed to distinguish from Biconsonantal.</div>
<table>
  <tr><th>#</th><th>Form</th><th>Weak Class</th><th>Pers.</th><th>Num.</th><th>Gen.</th><th>Root</th><th></th></tr>
  <tr>
    <td class="num">36</td><td class="heb">יָסֹב</td>
    <td><input class="parse-field" id="36-wc" placeholder="class"></td><td><input class="parse-field" id="36-p" placeholder="1/2/3"></td><td><input class="parse-field" id="36-n" placeholder="s/p"></td><td><input class="parse-field" id="36-g" placeholder="m/f/c"></td><td><input class="parse-field" id="36-r" placeholder="root"></td>
    <td><button class="rbtn" onclick="tog(36)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-36"><td class="ans-lbl">✓</td><td class="ans-heb">יָסֹב</td><td>Geminate</td><td>3</td><td>s</td><td>m</td><td class="ans-heb">סָבַב</td><td>Qamets prefix; holem; R2=R3 (dagesh absorbed)</td></tr>
  <tr>
    <td class="num">37</td><td class="heb">יִסֹּב</td>
    <td><input class="parse-field" id="37-wc" placeholder="class"></td><td><input class="parse-field" id="37-p" placeholder="1/2/3"></td><td><input class="parse-field" id="37-n" placeholder="s/p"></td><td><input class="parse-field" id="37-g" placeholder="m/f/c"></td><td><input class="parse-field" id="37-r" placeholder="root"></td>
    <td><button class="rbtn" onclick="tog(37)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-37"><td class="ans-lbl">✓</td><td class="ans-heb">יִסֹּב</td><td>Geminate</td><td>3</td><td>s</td><td>m</td><td class="ans-heb">סָבַב</td><td>Hireq prefix + holem + dagesh forte in ב (R2=R3)</td></tr>
  <tr>
    <td class="num">38</td><td class="heb">וַיָּסׇּב</td>
    <td><input class="parse-field" id="38-wc" placeholder="class"></td><td><input class="parse-field" id="38-p" placeholder="1/2/3"></td><td><input class="parse-field" id="38-n" placeholder="s/p"></td><td><input class="parse-field" id="38-g" placeholder="m/f/c"></td><td><input class="parse-field" id="38-r" placeholder="root"></td>
    <td><button class="rbtn" onclick="tog(38)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-38"><td class="ans-lbl">✓</td><td class="ans-heb">וַיָּסׇּב</td><td>Geminate</td><td>3</td><td>s</td><td>m</td><td class="ans-heb">סָבַב</td><td>Wayyiqtol; qamets prefix + dagesh forte in root</td></tr>
  <tr>
    <td class="num">39</td><td class="heb">תָּסֹב</td>
    <td><input class="parse-field" id="39-wc" placeholder="class"></td><td><input class="parse-field" id="39-p" placeholder="1/2/3"></td><td><input class="parse-field" id="39-n" placeholder="s/p"></td><td><input class="parse-field" id="39-g" placeholder="m/f/c"></td><td><input class="parse-field" id="39-r" placeholder="root"></td>
    <td><button class="rbtn" onclick="tog(39)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-39"><td class="ans-lbl">✓</td><td class="ans-heb">תָּסֹב</td><td>Geminate</td><td>3/2</td><td>s</td><td>f/m</td><td class="ans-heb">סָבַב</td><td>Qamets prefix; holem; same as יָסֹב pattern</td></tr>
  <tr>
    <td class="num">40</td><td class="heb">יִסֹּבּוּ</td>
    <td><input class="parse-field" id="40-wc" placeholder="class"></td><td><input class="parse-field" id="40-p" placeholder="1/2/3"></td><td><input class="parse-field" id="40-n" placeholder="s/p"></td><td><input class="parse-field" id="40-g" placeholder="m/f/c"></td><td><input class="parse-field" id="40-r" placeholder="root"></td>
    <td><button class="rbtn" onclick="tog(40)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-40"><td class="ans-lbl">✓</td><td class="ans-heb">יִסֹּבּוּ</td><td>Geminate</td><td>3</td><td>p</td><td>m</td><td class="ans-heb">סָבַב</td><td>3mp; dagesh forte in ב; -וּ suffix</td></tr>
</table>

<hr class="sec">

<!-- PART B -->
<h2>Part B — Mixed Forms</h2>
<div class="hint">Identify the weak class first, then parse the form completely.</div>
<table>
  <tr><th>#</th><th>Form</th><th>Weak Class</th><th>Pers.</th><th>Num.</th><th>Gen.</th><th>Root</th><th></th></tr>
  <tr>
    <td class="num">41</td><td class="heb">וַיָּקׇם</td>
    <td><input class="parse-field" id="41-wc" placeholder="class"></td><td><input class="parse-field" id="41-p" placeholder="1/2/3"></td><td><input class="parse-field" id="41-n" placeholder="s/p"></td><td><input class="parse-field" id="41-g" placeholder="m/f/c"></td><td><input class="parse-field" id="41-r" placeholder="root"></td>
    <td><button class="rbtn" onclick="tog(41)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-41"><td class="ans-lbl">✓</td><td class="ans-heb">וַיָּקׇם</td><td>Biconsonantal</td><td>3</td><td>s</td><td>m</td><td class="ans-heb">קוּם</td><td>Gen 22:3 — Abraham arising</td></tr>
  <tr>
    <td class="num">42</td><td class="heb">יִבְנֶה</td>
    <td><input class="parse-field" id="42-wc" placeholder="class"></td><td><input class="parse-field" id="42-p" placeholder="1/2/3"></td><td><input class="parse-field" id="42-n" placeholder="s/p"></td><td><input class="parse-field" id="42-g" placeholder="m/f/c"></td><td><input class="parse-field" id="42-r" placeholder="root"></td>
    <td><button class="rbtn" onclick="tog(42)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-42"><td class="ans-lbl">✓</td><td class="ans-heb">יִבְנֶה</td><td>III-ה</td><td>3</td><td>s</td><td>m</td><td class="ans-heb">בָּנָה</td><td>Long Imperfect; seghol-he ending</td></tr>
  <tr>
    <td class="num">43</td><td class="heb">יִתֵּן</td>
    <td><input class="parse-field" id="43-wc" placeholder="class"></td><td><input class="parse-field" id="43-p" placeholder="1/2/3"></td><td><input class="parse-field" id="43-n" placeholder="s/p"></td><td><input class="parse-field" id="43-g" placeholder="m/f/c"></td><td><input class="parse-field" id="43-r" placeholder="root"></td>
    <td><button class="rbtn" onclick="tog(43)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-43"><td class="ans-lbl">✓</td><td class="ans-heb">יִתֵּן</td><td>I-נ</td><td>3</td><td>s</td><td>m</td><td class="ans-heb">נָתַן</td><td>Dagesh in ת from assimilated nun</td></tr>
  <tr>
    <td class="num">44</td><td class="heb">יַעֲשֶׂה</td>
    <td><input class="parse-field" id="44-wc" placeholder="class"></td><td><input class="parse-field" id="44-p" placeholder="1/2/3"></td><td><input class="parse-field" id="44-n" placeholder="s/p"></td><td><input class="parse-field" id="44-g" placeholder="m/f/c"></td><td><input class="parse-field" id="44-r" placeholder="root"></td>
    <td><button class="rbtn" onclick="tog(44)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-44"><td class="ans-lbl">✓</td><td class="ans-heb">יַעֲשֶׂה</td><td>III-ה + I-gutt.</td><td>3</td><td>s</td><td>m</td><td class="ans-heb">עָשָׂה</td><td>III-ה + I-gutt. ע (chateph prefix)</td></tr>
  <tr>
    <td class="num">45</td><td class="heb">תֵּדַע</td>
    <td><input class="parse-field" id="45-wc" placeholder="class"></td><td><input class="parse-field" id="45-p" placeholder="1/2/3"></td><td><input class="parse-field" id="45-n" placeholder="s/p"></td><td><input class="parse-field" id="45-g" placeholder="m/f/c"></td><td><input class="parse-field" id="45-r" placeholder="root"></td>
    <td><button class="rbtn" onclick="tog(45)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-45"><td class="ans-lbl">✓</td><td class="ans-heb">תֵּדַע</td><td>I-י</td><td>3/2</td><td>s</td><td>f/m</td><td class="ans-heb">יָדַע</td><td>Tsere prefix; I-י diagnostic</td></tr>
  <tr>
    <td class="num">46</td><td class="heb">וַיִּשְׁמַע</td>
    <td><input class="parse-field" id="46-wc" placeholder="class"></td><td><input class="parse-field" id="46-p" placeholder="1/2/3"></td><td><input class="parse-field" id="46-n" placeholder="s/p"></td><td><input class="parse-field" id="46-g" placeholder="m/f/c"></td><td><input class="parse-field" id="46-r" placeholder="root"></td>
    <td><button class="rbtn" onclick="tog(46)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-46"><td class="ans-lbl">✓</td><td class="ans-heb">וַיִּשְׁמַע</td><td>III-ע</td><td>3</td><td>s</td><td>m</td><td class="ans-heb">שָׁמַע</td><td>III-guttural wayyiqtol (no furtive)</td></tr>
  <tr>
    <td class="num">47</td><td class="heb">יִמְצָא</td>
    <td><input class="parse-field" id="47-wc" placeholder="class"></td><td><input class="parse-field" id="47-p" placeholder="1/2/3"></td><td><input class="parse-field" id="47-n" placeholder="s/p"></td><td><input class="parse-field" id="47-g" placeholder="m/f/c"></td><td><input class="parse-field" id="47-r" placeholder="root"></td>
    <td><button class="rbtn" onclick="tog(47)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-47"><td class="ans-lbl">✓</td><td class="ans-heb">יִמְצָא</td><td>III-א</td><td>3</td><td>s</td><td>m</td><td class="ans-heb">מָצָא</td><td>Silent aleph; qamets</td></tr>
  <tr>
    <td class="num">48</td><td class="heb">וַיָּבֹאוּ</td>
    <td><input class="parse-field" id="48-wc" placeholder="class"></td><td><input class="parse-field" id="48-p" placeholder="1/2/3"></td><td><input class="parse-field" id="48-n" placeholder="s/p"></td><td><input class="parse-field" id="48-g" placeholder="m/f/c"></td><td><input class="parse-field" id="48-r" placeholder="root"></td>
    <td><button class="rbtn" onclick="tog(48)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-48"><td class="ans-lbl">✓</td><td class="ans-heb">וַיָּבֹאוּ</td><td>Biconsonantal</td><td>3</td><td>p</td><td>m</td><td class="ans-heb">בּוֹא</td><td>Wayyiqtol 3mp; qamets + -וּ</td></tr>
  <tr>
    <td class="num">49</td><td class="heb">תִּתֵּן</td>
    <td><input class="parse-field" id="49-wc" placeholder="class"></td><td><input class="parse-field" id="49-p" placeholder="1/2/3"></td><td><input class="parse-field" id="49-n" placeholder="s/p"></td><td><input class="parse-field" id="49-g" placeholder="m/f/c"></td><td><input class="parse-field" id="49-r" placeholder="root"></td>
    <td><button class="rbtn" onclick="tog(49)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-49"><td class="ans-lbl">✓</td><td class="ans-heb">תִּתֵּן</td><td>I-נ</td><td>3/2</td><td>s</td><td>f/m</td><td class="ans-heb">נָתַן</td><td>Dagesh in ת; same assimilation pattern</td></tr>
  <tr>
    <td class="num">50</td><td class="heb">יֵצֵא</td>
    <td><input class="parse-field" id="50-wc" placeholder="class"></td><td><input class="parse-field" id="50-p" placeholder="1/2/3"></td><td><input class="parse-field" id="50-n" placeholder="s/p"></td><td><input class="parse-field" id="50-g" placeholder="m/f/c"></td><td><input class="parse-field" id="50-r" placeholder="root"></td>
    <td><button class="rbtn" onclick="tog(50)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-50"><td class="ans-lbl">✓</td><td class="ans-heb">יֵצֵא</td><td>I-י</td><td>3</td><td>s</td><td>m</td><td class="ans-heb">יָצָא</td><td>Tsere prefix; I-י (+ III-א at R3)</td></tr>
</table>

<hr class="sec">

<!-- DISCUSSION QUESTIONS -->
<div class="disc">
  <strong>Discussion Questions</strong>
  <ol>
    <li><strong>Biconsonantal vs. Geminate:</strong> Both classes can show qamets under the prefix consonant (יָסֹב / יָקוּם). What distinguishes them? What additional information do you need to tell them apart?</li>
    <li><strong>I-נ in Perfect vs. Imperfect:</strong> Why is I-נ essentially invisible in the Perfect (Ch14) but produces a dramatic change in the Imperfect? What is happening phonologically?</li>
    <li><strong>The III-ה Jussive:</strong> How does a III-ה Jussive form (e.g. יִבֶּן) differ from the long Imperfect (יִבְנֶה)? What changes, and why does this matter for reading narrative?</li>
    <li><strong>I-י prefix pattern:</strong> Why does I-י show tsere under the prefix consonant instead of hireq? Trace what happens to the yod at R1 when the imperfect prefix is added.</li>
    <li><strong>Wayyiqtol identification:</strong> What morphological feature is shared by <em>all</em> wayyiqtol forms across all weak classes? How does recognizing this feature help you identify a wayyiqtol even in an unfamiliar weak root?</li>
  </ol>
</div>

<script>
  const ids = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50];
  function tog(id) { const r=document.getElementById('ans-'+id); const b=r.previousElementSibling.querySelector('button'); const v=r.style.display==='table-row'; r.style.display=v?'none':'table-row'; b.textContent=v?'▶ Answer':'▼ Hide'; b.classList.toggle('on',!v); }
  function showAll() { ids.forEach(id=>{const r=document.getElementById('ans-'+id);const b=r.previousElementSibling.querySelector('button');r.style.display='table-row';b.textContent='▼ Hide';b.classList.add('on');}); }
  function hideAll() { ids.forEach(id=>{const r=document.getElementById('ans-'+id);const b=r.previousElementSibling.querySelector('button');r.style.display='none';b.textContent='▶ Answer';b.classList.remove('on');}); }
  function clearAll() { document.querySelectorAll('input.f').forEach(e=>e.value=''); }
</script>

