# Pronoun Identification

*Chapter 8 — Hebrew Pronouns*

[Full screen](ch8-pronoun-identification.html){.md-button}  [Markdown](ch8-pronoun-identification.md){.md-button}  [Print (PDF)](ch8-pronoun-identification.pdf){.md-button}

<style>

  body { font-family: Georgia, serif;    color: #222; line-height: 1.6; }
  h1 { font-size: 1.45rem; border-bottom: 2px solid #555; padding-bottom: .4rem; }
  h2 { font-size: 1.05rem; margin-top: 2rem; color: #333; border-bottom: 1px solid #ddd; padding-bottom: .2rem; }
  .subtitle { color: #666; font-style: italic; margin-top: -.4rem; }
  .instructions { background: #f8f8f0; border-left: 4px solid #bbb; padding: .75rem 1rem; margin: 1rem 0; font-size: .92rem; }
  table { border-collapse: collapse; width: 100%; margin: .4rem 0; font-size: .91rem; }
  th { background: #e0e8f0; padding: .4rem .55rem; border: 1px solid #bbb; text-align: left; font-size: .84rem; }
  td { padding: .3rem .45rem; border: 1px solid #ddd; vertical-align: middle; }
  td.num { text-align: center; font-weight: bold; color: #666; width: 2rem; }
  td.heb {
    font-size: 1.8em;
    direction: rtl;
    unicode-bidi: embed;
    font-weight: bold;
    min-width: 14rem;
  }
  td.heb-sm {
    font-size: 1.8em;
    direction: rtl;
    unicode-bidi: embed;
    min-width: 6rem;
  }
  input.f {
    width: 100%;
    box-sizing: border-box;
    border: 1px solid #bbb;
    border-radius: 3px;
    padding: .22rem .4rem;
    font-family: Georgia, serif;
    font-size: .87rem;
    background: #fafff8;
  }
  input.f:focus { outline: none; border-color: #5a9; box-shadow: 0 0 0 2px #c8ecd4; }
  .answer-row { display: none; background: #f0faf0; }
  .answer-row td { font-size: .87rem; color: #2a6e2a; padding: .28rem .45rem; }
  .ans-lbl { font-weight: bold; color: #1a5c1a; width: 2rem; text-align: center; }
  button.rbtn {
    font-size: .76rem;
    padding: .14rem .48rem;
    cursor: pointer;
    background: #e8f4ec;
    border: 1px solid #7bba8f;
    border-radius: 3px;
    color: #2a6e2a;
    white-space: nowrap;
  }
  button.rbtn:hover, button.rbtn.on { background: #c8ecd4; }
  .controls { display: flex; gap: .7rem; flex-wrap: wrap; margin: 1rem 0 1.5rem; }
  .controls button {
    padding: .38rem .85rem;
    cursor: pointer;
    border-radius: 4px;
    font-size: .88rem;
    border: 1px solid #999;
    background: #f0f0f0;
    color: #333;
  }
  .controls button:hover { background: #ddd; }
  .clr { border-color: #c06060 !important; color: #8b0000 !important; background: #fff0f0 !important; }
  .clr:hover { background: #ffd8d8 !important; }
  hr.sec { border: none; border-top: 2px dashed #ccc; margin: 2rem 0; }
  .note-box { background: #fafaf0; border: 1px solid #d8d8a0; border-radius: 4px; padding: .7rem 1rem; margin: 1.2rem 0; font-size: .9rem; }
  .note-box strong { color: #555; }
  .reflect { margin-top: 2.5rem; }
  .reflect ol { padding-left: 1.4rem; }
  .reflect li { margin-bottom: .7rem; font-size: .92rem; }
  @media print {
    .controls, button.rbtn { display: none; }
    input.f { border: none; border-bottom: 1px solid #aaa; border-radius: 0; background: transparent; }
    .answer-row { display: none !important; }
  }

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

<h1>Ch8 Pronoun Identification Drill</h1>
<p class="subtitle">BBH Chapter 8 — Hebrew Pronouns &nbsp;·&nbsp; 25 items</p>

<div class="instructions">
  <strong>Instructions:</strong> For each item:<br>
  (1) <strong>Pronoun Type</strong> — Personal / Demonstrative / Relative / Interrogative<br>
  (2) <strong>Pronoun</strong> — write out the Hebrew pronoun<br>
  (3) <strong>Parse (PGN)</strong> — give Person, Gender, Number where applicable; for Relative and Interrogative write <em>indecl.</em><br>
  (4) <strong>Translation</strong> — translate the full phrase
</div>

<div class="controls">
  <button onclick="showAll()">Show All Answers</button>
  <button onclick="hideAll()">Hide All Answers</button>
  <button class="clr" onclick="clearAll()">Clear All Inputs</button>
</div>

<!-- ITEMS 1–8: Independent Personal Pronouns -->
<h2>Items 1–8 — Independent Personal Pronouns</h2>
<table>
  <tr><th>#</th><th>Hebrew</th><th>Pronoun Type</th><th>Pronoun</th><th>Parse (PGN)</th><th>Translation</th><th></th></tr>

  <tr>
    <td class="num">1</td>
    <td class="heb">אֲנִי יְהוָה אֱלֹהֵיכֶם</td>
    <td><input class="parse-field" id="1-t" placeholder="Type"></td>
    <td><input class="parse-field" id="1-pr" placeholder="Pronoun"></td>
    <td><input class="parse-field" id="1-pg" placeholder="PGN"></td>
    <td><input class="parse-field" id="1-tr" placeholder="Translation"></td>
    <td><button class="rbtn" onclick="tog(1)">&#9654; Answer</button></td>
  </tr>
  <tr class="answer-row" id="ans-1">
    <td class="ans-lbl">&#10003;</td>
    <td class="heb-sm">אֲנִי</td>
    <td>Personal</td>
    <td class="heb-sm">אֲנִי</td>
    <td>1cs</td>
    <td>"I am the LORD your God"</td>
    <td></td>
  </tr>

  <tr>
    <td class="num">2</td>
    <td class="heb">אַתָּה עַבְדִּי</td>
    <td><input class="parse-field" id="2-t" placeholder="Type"></td>
    <td><input class="parse-field" id="2-pr" placeholder="Pronoun"></td>
    <td><input class="parse-field" id="2-pg" placeholder="PGN"></td>
    <td><input class="parse-field" id="2-tr" placeholder="Translation"></td>
    <td><button class="rbtn" onclick="tog(2)">&#9654; Answer</button></td>
  </tr>
  <tr class="answer-row" id="ans-2">
    <td class="ans-lbl">&#10003;</td>
    <td class="heb-sm">אַתָּה</td>
    <td>Personal</td>
    <td class="heb-sm">אַתָּה</td>
    <td>2ms</td>
    <td>"You are my servant"</td>
    <td></td>
  </tr>

  <tr>
    <td class="num">3</td>
    <td class="heb">הוּא הַכֹּהֵן</td>
    <td><input class="parse-field" id="3-t" placeholder="Type"></td>
    <td><input class="parse-field" id="3-pr" placeholder="Pronoun"></td>
    <td><input class="parse-field" id="3-pg" placeholder="PGN"></td>
    <td><input class="parse-field" id="3-tr" placeholder="Translation"></td>
    <td><button class="rbtn" onclick="tog(3)">&#9654; Answer</button></td>
  </tr>
  <tr class="answer-row" id="ans-3">
    <td class="ans-lbl">&#10003;</td>
    <td class="heb-sm">הוּא</td>
    <td>Personal</td>
    <td class="heb-sm">הוּא</td>
    <td>3ms</td>
    <td>"He is the priest"</td>
    <td></td>
  </tr>

  <tr>
    <td class="num">4</td>
    <td class="heb">הִיא הַמַּלְכָּה</td>
    <td><input class="parse-field" id="4-t" placeholder="Type"></td>
    <td><input class="parse-field" id="4-pr" placeholder="Pronoun"></td>
    <td><input class="parse-field" id="4-pg" placeholder="PGN"></td>
    <td><input class="parse-field" id="4-tr" placeholder="Translation"></td>
    <td><button class="rbtn" onclick="tog(4)">&#9654; Answer</button></td>
  </tr>
  <tr class="answer-row" id="ans-4">
    <td class="ans-lbl">&#10003;</td>
    <td class="heb-sm">הִיא</td>
    <td>Personal</td>
    <td class="heb-sm">הִיא</td>
    <td>3fs</td>
    <td>"She is the queen"</td>
    <td></td>
  </tr>

  <tr>
    <td class="num">5</td>
    <td class="heb">אֲנַחְנוּ עֲבָדֶיךָ</td>
    <td><input class="parse-field" id="5-t" placeholder="Type"></td>
    <td><input class="parse-field" id="5-pr" placeholder="Pronoun"></td>
    <td><input class="parse-field" id="5-pg" placeholder="PGN"></td>
    <td><input class="parse-field" id="5-tr" placeholder="Translation"></td>
    <td><button class="rbtn" onclick="tog(5)">&#9654; Answer</button></td>
  </tr>
  <tr class="answer-row" id="ans-5">
    <td class="ans-lbl">&#10003;</td>
    <td class="heb-sm">אֲנַחְנוּ</td>
    <td>Personal</td>
    <td class="heb-sm">אֲנַחְנוּ</td>
    <td>1cp</td>
    <td>"We are your servants"</td>
    <td></td>
  </tr>

  <tr>
    <td class="num">6</td>
    <td class="heb">אַתֶּם עֵדַי</td>
    <td><input class="parse-field" id="6-t" placeholder="Type"></td>
    <td><input class="parse-field" id="6-pr" placeholder="Pronoun"></td>
    <td><input class="parse-field" id="6-pg" placeholder="PGN"></td>
    <td><input class="parse-field" id="6-tr" placeholder="Translation"></td>
    <td><button class="rbtn" onclick="tog(6)">&#9654; Answer</button></td>
  </tr>
  <tr class="answer-row" id="ans-6">
    <td class="ans-lbl">&#10003;</td>
    <td class="heb-sm">אַתֶּם</td>
    <td>Personal</td>
    <td class="heb-sm">אַתֶּם</td>
    <td>2mp</td>
    <td>"You are my witnesses"</td>
    <td></td>
  </tr>

  <tr>
    <td class="num">7</td>
    <td class="heb">אָנֹכִי הָאִישׁ</td>
    <td><input class="parse-field" id="7-t" placeholder="Type"></td>
    <td><input class="parse-field" id="7-pr" placeholder="Pronoun"></td>
    <td><input class="parse-field" id="7-pg" placeholder="PGN"></td>
    <td><input class="parse-field" id="7-tr" placeholder="Translation"></td>
    <td><button class="rbtn" onclick="tog(7)">&#9654; Answer</button></td>
  </tr>
  <tr class="answer-row" id="ans-7">
    <td class="ans-lbl">&#10003;</td>
    <td class="heb-sm">אָנֹכִי</td>
    <td>Personal</td>
    <td class="heb-sm">אָנֹכִי</td>
    <td>1cs (archaic)</td>
    <td>"I am the man"</td>
    <td></td>
  </tr>

  <tr>
    <td class="num">8</td>
    <td class="heb">הֵם הַכֹּהֲנִים</td>
    <td><input class="parse-field" id="8-t" placeholder="Type"></td>
    <td><input class="parse-field" id="8-pr" placeholder="Pronoun"></td>
    <td><input class="parse-field" id="8-pg" placeholder="PGN"></td>
    <td><input class="parse-field" id="8-tr" placeholder="Translation"></td>
    <td><button class="rbtn" onclick="tog(8)">&#9654; Answer</button></td>
  </tr>
  <tr class="answer-row" id="ans-8">
    <td class="ans-lbl">&#10003;</td>
    <td class="heb-sm">הֵם</td>
    <td>Personal</td>
    <td class="heb-sm">הֵם</td>
    <td>3mp</td>
    <td>"They are the priests"</td>
    <td></td>
  </tr>
</table>

<hr class="sec">

<!-- ITEMS 9–15: Demonstrative Pronouns -->
<h2>Items 9–15 — Demonstrative Pronouns</h2>
<table>
  <tr><th>#</th><th>Hebrew</th><th>Pronoun Type</th><th>Pronoun</th><th>Parse (PGN)</th><th>Translation</th><th></th></tr>

  <tr>
    <td class="num">9</td>
    <td class="heb">הָאִישׁ הַזֶּה</td>
    <td><input class="parse-field" id="9-t" placeholder="Type"></td>
    <td><input class="parse-field" id="9-pr" placeholder="Pronoun"></td>
    <td><input class="parse-field" id="9-pg" placeholder="PGN"></td>
    <td><input class="parse-field" id="9-tr" placeholder="Translation"></td>
    <td><button class="rbtn" onclick="tog(9)">&#9654; Answer</button></td>
  </tr>
  <tr class="answer-row" id="ans-9">
    <td class="ans-lbl">&#10003;</td>
    <td class="heb-sm">הַזֶּה</td>
    <td>Demonstrative</td>
    <td class="heb-sm">הַזֶּה</td>
    <td>ms (near, attributive)</td>
    <td>"this man"</td>
    <td></td>
  </tr>

  <tr>
    <td class="num">10</td>
    <td class="heb">הָאִשָּׁה הַזֹּאת</td>
    <td><input class="parse-field" id="10-t" placeholder="Type"></td>
    <td><input class="parse-field" id="10-pr" placeholder="Pronoun"></td>
    <td><input class="parse-field" id="10-pg" placeholder="PGN"></td>
    <td><input class="parse-field" id="10-tr" placeholder="Translation"></td>
    <td><button class="rbtn" onclick="tog(10)">&#9654; Answer</button></td>
  </tr>
  <tr class="answer-row" id="ans-10">
    <td class="ans-lbl">&#10003;</td>
    <td class="heb-sm">הַזֹּאת</td>
    <td>Demonstrative</td>
    <td class="heb-sm">הַזֹּאת</td>
    <td>fs (near, attributive)</td>
    <td>"this woman"</td>
    <td></td>
  </tr>

  <tr>
    <td class="num">11</td>
    <td class="heb">הַדְּבָרִים הָאֵלֶּה</td>
    <td><input class="parse-field" id="11-t" placeholder="Type"></td>
    <td><input class="parse-field" id="11-pr" placeholder="Pronoun"></td>
    <td><input class="parse-field" id="11-pg" placeholder="PGN"></td>
    <td><input class="parse-field" id="11-tr" placeholder="Translation"></td>
    <td><button class="rbtn" onclick="tog(11)">&#9654; Answer</button></td>
  </tr>
  <tr class="answer-row" id="ans-11">
    <td class="ans-lbl">&#10003;</td>
    <td class="heb-sm">הָאֵלֶּה</td>
    <td>Demonstrative</td>
    <td class="heb-sm">הָאֵלֶּה</td>
    <td>cp (near, attributive)</td>
    <td>"these words/things"</td>
    <td></td>
  </tr>

  <tr>
    <td class="num">12</td>
    <td class="heb">זֶה הָאִישׁ</td>
    <td><input class="parse-field" id="12-t" placeholder="Type"></td>
    <td><input class="parse-field" id="12-pr" placeholder="Pronoun"></td>
    <td><input class="parse-field" id="12-pg" placeholder="PGN"></td>
    <td><input class="parse-field" id="12-tr" placeholder="Translation"></td>
    <td><button class="rbtn" onclick="tog(12)">&#9654; Answer</button></td>
  </tr>
  <tr class="answer-row" id="ans-12">
    <td class="ans-lbl">&#10003;</td>
    <td class="heb-sm">זֶה</td>
    <td>Demonstrative</td>
    <td class="heb-sm">זֶה</td>
    <td>ms (near, predicate)</td>
    <td>"This is the man"</td>
    <td></td>
  </tr>

  <tr>
    <td class="num">13</td>
    <td class="heb">זֹאת הָאָרֶץ</td>
    <td><input class="parse-field" id="13-t" placeholder="Type"></td>
    <td><input class="parse-field" id="13-pr" placeholder="Pronoun"></td>
    <td><input class="parse-field" id="13-pg" placeholder="PGN"></td>
    <td><input class="parse-field" id="13-tr" placeholder="Translation"></td>
    <td><button class="rbtn" onclick="tog(13)">&#9654; Answer</button></td>
  </tr>
  <tr class="answer-row" id="ans-13">
    <td class="ans-lbl">&#10003;</td>
    <td class="heb-sm">זֹאת</td>
    <td>Demonstrative</td>
    <td class="heb-sm">זֹאת</td>
    <td>fs (near, predicate)</td>
    <td>"This is the land"</td>
    <td></td>
  </tr>

  <tr>
    <td class="num">14</td>
    <td class="heb">בַּיּוֹם הַהוּא</td>
    <td><input class="parse-field" id="14-t" placeholder="Type"></td>
    <td><input class="parse-field" id="14-pr" placeholder="Pronoun"></td>
    <td><input class="parse-field" id="14-pg" placeholder="PGN"></td>
    <td><input class="parse-field" id="14-tr" placeholder="Translation"></td>
    <td><button class="rbtn" onclick="tog(14)">&#9654; Answer</button></td>
  </tr>
  <tr class="answer-row" id="ans-14">
    <td class="ans-lbl">&#10003;</td>
    <td class="heb-sm">הַהוּא</td>
    <td>Demonstrative</td>
    <td class="heb-sm">הַהוּא</td>
    <td>ms (far, attributive)</td>
    <td>"on that day"</td>
    <td></td>
  </tr>

  <tr>
    <td class="num">15</td>
    <td class="heb">בָּעֵת הַהִיא</td>
    <td><input class="parse-field" id="15-t" placeholder="Type"></td>
    <td><input class="parse-field" id="15-pr" placeholder="Pronoun"></td>
    <td><input class="parse-field" id="15-pg" placeholder="PGN"></td>
    <td><input class="parse-field" id="15-tr" placeholder="Translation"></td>
    <td><button class="rbtn" onclick="tog(15)">&#9654; Answer</button></td>
  </tr>
  <tr class="answer-row" id="ans-15">
    <td class="ans-lbl">&#10003;</td>
    <td class="heb-sm">הַהִיא</td>
    <td>Demonstrative</td>
    <td class="heb-sm">הַהִיא</td>
    <td>fs (far, attributive)</td>
    <td>"at that time"</td>
    <td></td>
  </tr>
</table>

<hr class="sec">

<!-- ITEMS 16–21: Relative Pronoun אֲשֶׁר -->
<h2>Items 16–21 — Relative Pronoun אֲשֶׁר</h2>
<table>
  <tr><th>#</th><th>Hebrew</th><th>Pronoun Type</th><th>Pronoun</th><th>Parse (PGN)</th><th>Translation</th><th></th></tr>

  <tr>
    <td class="num">16</td>
    <td class="heb">הָאִישׁ אֲשֶׁר בָּא</td>
    <td><input class="parse-field" id="16-t" placeholder="Type"></td>
    <td><input class="parse-field" id="16-pr" placeholder="Pronoun"></td>
    <td><input class="parse-field" id="16-pg" placeholder="PGN"></td>
    <td><input class="parse-field" id="16-tr" placeholder="Translation"></td>
    <td><button class="rbtn" onclick="tog(16)">&#9654; Answer</button></td>
  </tr>
  <tr class="answer-row" id="ans-16">
    <td class="ans-lbl">&#10003;</td>
    <td class="heb-sm">אֲשֶׁר</td>
    <td>Relative</td>
    <td class="heb-sm">אֲשֶׁר</td>
    <td>indecl. (subject rel.)</td>
    <td>"the man who came"</td>
    <td></td>
  </tr>

  <tr>
    <td class="num">17</td>
    <td class="heb">הָאִשָּׁה אֲשֶׁר רָאִיתִי</td>
    <td><input class="parse-field" id="17-t" placeholder="Type"></td>
    <td><input class="parse-field" id="17-pr" placeholder="Pronoun"></td>
    <td><input class="parse-field" id="17-pg" placeholder="PGN"></td>
    <td><input class="parse-field" id="17-tr" placeholder="Translation"></td>
    <td><button class="rbtn" onclick="tog(17)">&#9654; Answer</button></td>
  </tr>
  <tr class="answer-row" id="ans-17">
    <td class="ans-lbl">&#10003;</td>
    <td class="heb-sm">אֲשֶׁר</td>
    <td>Relative</td>
    <td class="heb-sm">אֲשֶׁר</td>
    <td>indecl. (object rel.)</td>
    <td>"the woman whom I saw"</td>
    <td></td>
  </tr>

  <tr>
    <td class="num">18</td>
    <td class="heb">הָאָרֶץ אֲשֶׁר נָתַן יְהוָה לָנוּ</td>
    <td><input class="parse-field" id="18-t" placeholder="Type"></td>
    <td><input class="parse-field" id="18-pr" placeholder="Pronoun"></td>
    <td><input class="parse-field" id="18-pg" placeholder="PGN"></td>
    <td><input class="parse-field" id="18-tr" placeholder="Translation"></td>
    <td><button class="rbtn" onclick="tog(18)">&#9654; Answer</button></td>
  </tr>
  <tr class="answer-row" id="ans-18">
    <td class="ans-lbl">&#10003;</td>
    <td class="heb-sm">אֲשֶׁר</td>
    <td>Relative</td>
    <td class="heb-sm">אֲשֶׁר</td>
    <td>indecl. (object rel.)</td>
    <td>"the land that the LORD gave to us"</td>
    <td></td>
  </tr>

  <tr>
    <td class="num">19</td>
    <td class="heb">הָאִישׁ אֲשֶׁר עָבַד אֶת יְהוָה</td>
    <td><input class="parse-field" id="19-t" placeholder="Type"></td>
    <td><input class="parse-field" id="19-pr" placeholder="Pronoun"></td>
    <td><input class="parse-field" id="19-pg" placeholder="PGN"></td>
    <td><input class="parse-field" id="19-tr" placeholder="Translation"></td>
    <td><button class="rbtn" onclick="tog(19)">&#9654; Answer</button></td>
  </tr>
  <tr class="answer-row" id="ans-19">
    <td class="ans-lbl">&#10003;</td>
    <td class="heb-sm">אֲשֶׁר</td>
    <td>Relative</td>
    <td class="heb-sm">אֲשֶׁר</td>
    <td>indecl. (subject rel.)</td>
    <td>"the man who served the LORD"</td>
    <td></td>
  </tr>

  <tr>
    <td class="num">20</td>
    <td class="heb">הַמִּצְוָה אֲשֶׁר צִוִּיתִיךָ</td>
    <td><input class="parse-field" id="20-t" placeholder="Type"></td>
    <td><input class="parse-field" id="20-pr" placeholder="Pronoun"></td>
    <td><input class="parse-field" id="20-pg" placeholder="PGN"></td>
    <td><input class="parse-field" id="20-tr" placeholder="Translation"></td>
    <td><button class="rbtn" onclick="tog(20)">&#9654; Answer</button></td>
  </tr>
  <tr class="answer-row" id="ans-20">
    <td class="ans-lbl">&#10003;</td>
    <td class="heb-sm">אֲשֶׁר</td>
    <td>Relative</td>
    <td class="heb-sm">אֲשֶׁר</td>
    <td>indecl. (object rel.)</td>
    <td>"the commandment that I commanded you"</td>
    <td></td>
  </tr>

  <tr>
    <td class="num">21</td>
    <td class="heb">הַדָּבָר אֲשֶׁר שָׁמַעְתָּ</td>
    <td><input class="parse-field" id="21-t" placeholder="Type"></td>
    <td><input class="parse-field" id="21-pr" placeholder="Pronoun"></td>
    <td><input class="parse-field" id="21-pg" placeholder="PGN"></td>
    <td><input class="parse-field" id="21-tr" placeholder="Translation"></td>
    <td><button class="rbtn" onclick="tog(21)">&#9654; Answer</button></td>
  </tr>
  <tr class="answer-row" id="ans-21">
    <td class="ans-lbl">&#10003;</td>
    <td class="heb-sm">אֲשֶׁר</td>
    <td>Relative</td>
    <td class="heb-sm">אֲשֶׁר</td>
    <td>indecl. (object rel.)</td>
    <td>"the word/thing that you heard"</td>
    <td></td>
  </tr>
</table>

<hr class="sec">

<!-- ITEMS 22–25: Interrogative Pronouns -->
<h2>Items 22–25 — Interrogative Pronouns (מִי / מַה)</h2>
<table>
  <tr><th>#</th><th>Hebrew</th><th>Pronoun Type</th><th>Pronoun</th><th>Parse (PGN)</th><th>Translation</th><th></th></tr>

  <tr>
    <td class="num">22</td>
    <td class="heb">מִי אַתָּה</td>
    <td><input class="parse-field" id="22-t" placeholder="Type"></td>
    <td><input class="parse-field" id="22-pr" placeholder="Pronoun"></td>
    <td><input class="parse-field" id="22-pg" placeholder="PGN"></td>
    <td><input class="parse-field" id="22-tr" placeholder="Translation"></td>
    <td><button class="rbtn" onclick="tog(22)">&#9654; Answer</button></td>
  </tr>
  <tr class="answer-row" id="ans-22">
    <td class="ans-lbl">&#10003;</td>
    <td class="heb-sm">מִי</td>
    <td>Interrogative</td>
    <td class="heb-sm">מִי</td>
    <td>indecl. (persons)</td>
    <td>"Who are you?"</td>
    <td></td>
  </tr>

  <tr>
    <td class="num">23</td>
    <td class="heb">מַה זֶּה</td>
    <td><input class="parse-field" id="23-t" placeholder="Type"></td>
    <td><input class="parse-field" id="23-pr" placeholder="Pronoun"></td>
    <td><input class="parse-field" id="23-pg" placeholder="PGN"></td>
    <td><input class="parse-field" id="23-tr" placeholder="Translation"></td>
    <td><button class="rbtn" onclick="tog(23)">&#9654; Answer</button></td>
  </tr>
  <tr class="answer-row" id="ans-23">
    <td class="ans-lbl">&#10003;</td>
    <td class="heb-sm">מַה</td>
    <td>Interrogative</td>
    <td class="heb-sm">מַה</td>
    <td>indecl. (things)</td>
    <td>"What is this?"</td>
    <td></td>
  </tr>

  <tr>
    <td class="num">24</td>
    <td class="heb">מִי הָאִישׁ הַזֶּה</td>
    <td><input class="parse-field" id="24-t" placeholder="Type"></td>
    <td><input class="parse-field" id="24-pr" placeholder="Pronoun"></td>
    <td><input class="parse-field" id="24-pg" placeholder="PGN"></td>
    <td><input class="parse-field" id="24-tr" placeholder="Translation"></td>
    <td><button class="rbtn" onclick="tog(24)">&#9654; Answer</button></td>
  </tr>
  <tr class="answer-row" id="ans-24">
    <td class="ans-lbl">&#10003;</td>
    <td class="heb-sm">מִי</td>
    <td>Interrogative</td>
    <td class="heb-sm">מִי</td>
    <td>indecl. (persons)</td>
    <td>"Who is this man?"</td>
    <td></td>
  </tr>

  <tr>
    <td class="num">25</td>
    <td class="heb">מַה עָשִׂיתָ</td>
    <td><input class="parse-field" id="25-t" placeholder="Type"></td>
    <td><input class="parse-field" id="25-pr" placeholder="Pronoun"></td>
    <td><input class="parse-field" id="25-pg" placeholder="PGN"></td>
    <td><input class="parse-field" id="25-tr" placeholder="Translation"></td>
    <td><button class="rbtn" onclick="tog(25)">&#9654; Answer</button></td>
  </tr>
  <tr class="answer-row" id="ans-25">
    <td class="ans-lbl">&#10003;</td>
    <td class="heb-sm">מַה</td>
    <td>Interrogative</td>
    <td class="heb-sm">מַה</td>
    <td>indecl. (things)</td>
    <td>"What have you done?"</td>
    <td></td>
  </tr>
</table>

<hr class="sec">

<!-- Notes -->
<h2>Notes on Selected Items</h2>
<div class="note-box">
  <strong>Items 1–8 (Personal pronouns):</strong> All function as the copula in verbless predicative clauses — Hebrew has no present-tense form of "to be." The pronoun stands between subject and predicate noun/adjective.
</div>
<div class="note-box">
  <strong>Item 7:</strong> <span style="direction:rtl; unicode-bidi:embed; font-size:1.3em">אָנֹכִי</span> is the archaic/literary variant of <span style="direction:rtl; unicode-bidi:embed; font-size:1.3em">אֲנִי</span>. Both are 1cs; <span style="direction:rtl; unicode-bidi:embed; font-size:1.3em">אָנֹכִי</span> appears in the Decalogue (Exo 20:2) and poetic contexts.
</div>
<div class="note-box">
  <strong>Items 9–11 (Near demonstrative, attributive):</strong> Both the noun and the demonstrative carry the definite article: <span style="direction:rtl; unicode-bidi:embed; font-size:1.3em">הָאִישׁ הַזֶּה</span>. The article on the demonstrative is required — attributive demonstratives must match the definiteness of the noun.
</div>
<div class="note-box">
  <strong>Items 12–13 (Demonstrative, predicate):</strong> Without the article on the demonstrative, the construction means "this is the X" — a predicate use.
</div>
<div class="note-box">
  <strong>Items 14–15 (Far demonstrative, attributive):</strong> <span style="direction:rtl; unicode-bidi:embed; font-size:1.3em">הַהוּא / הַהִיא</span> are the 3rd-person pronouns with the article prefixed. Context and the presence of a modified noun distinguishes them from personal pronouns.
</div>
<div class="note-box">
  <strong>Items 16–21 (Relative <span style="direction:rtl; unicode-bidi:embed; font-size:1.2em">אֲשֶׁר</span>):</strong> <span style="direction:rtl; unicode-bidi:embed; font-size:1.3em">אֲשֶׁר</span> never changes form. It is strictly indeclinable regardless of the gender, number, or syntactic role of its antecedent.
</div>
<div class="note-box">
  <strong>Items 22–25 (Interrogative <span style="direction:rtl; unicode-bidi:embed; font-size:1.2em">מִי / מַה</span>):</strong> <span style="direction:rtl; unicode-bidi:embed; font-size:1.3em">מִי</span> always refers to persons; <span style="direction:rtl; unicode-bidi:embed; font-size:1.3em">מַה</span> to things. Item 25 <span style="direction:rtl; unicode-bidi:embed; font-size:1.3em">מַה עָשִׂיתָ</span> is one of the most frequent question patterns in the OT (Gen 3:13; 4:10; 12:18).
</div>

<hr class="sec">

<!-- Reflection Questions -->
<div class="reflect">
  <h2>Reflection Questions</h2>
  <ol>
    <li>In items 1–8, why does Hebrew use an independent personal pronoun even though no verb is present? What grammatical function does the pronoun serve in each verbless clause?</li>
    <li>Compare items 9 (<span style="direction:rtl; unicode-bidi:embed; font-size:1.1em">הָאִישׁ הַזֶּה</span>) and 12 (<span style="direction:rtl; unicode-bidi:embed; font-size:1.1em">זֶה הָאִישׁ</span>). What is the structural difference, and how does it change the meaning from attributive ("this man") to predicate ("this is the man")?</li>
    <li>In items 16–21, <span style="direction:rtl; unicode-bidi:embed; font-size:1.1em">אֲשֶׁר</span> introduces relative clauses with different grammatical functions (subject, object, etc.). For each item, identify whether the antecedent functions as the <em>subject</em> or <em>object</em> within the relative clause. How would you signal a possessive relative clause in Hebrew? (Hint: resumptive pronoun)</li>
  </ol>
</div>

<script>
  var ansStates = {};
  function tog(n) {
    var row = document.getElementById('ans-' + n);
    var btn = row.previousElementSibling.cells[6].querySelector('button');
    if (!row) return;
    if (ansStates[n]) {
      row.style.display = 'none';
      ansStates[n] = false;
      if (btn) { btn.classList.remove('on'); btn.textContent = '▶ Answer'; }
    } else {
      row.style.display = 'table-row';
      ansStates[n] = true;
      if (btn) { btn.classList.add('on'); btn.textContent = '▼ Answer'; }
    }
  }
  function showAll() {
    for (var i = 1; i <= 25; i++) {
      var row = document.getElementById('ans-' + i);
      if (row) {
        row.style.display = 'table-row';
        ansStates[i] = true;
        var prev = row.previousElementSibling;
        if (prev) {
          var btn = prev.cells[6] ? prev.cells[6].querySelector('button') : null;
          if (btn) { btn.classList.add('on'); btn.textContent = '▼ Answer'; }
        }
      }
    }
  }
  function hideAll() {
    for (var i = 1; i <= 25; i++) {
      var row = document.getElementById('ans-' + i);
      if (row) {
        row.style.display = 'none';
        ansStates[i] = false;
        var prev = row.previousElementSibling;
        if (prev) {
          var btn = prev.cells[6] ? prev.cells[6].querySelector('button') : null;
          if (btn) { btn.classList.remove('on'); btn.textContent = '▶ Answer'; }
        }
      }
    }
  }
  function clearAll() {
    var inputs = document.querySelectorAll('input.f');
    for (var i = 0; i < inputs.length; i++) { inputs[i].value = ''; }
  }
</script>

