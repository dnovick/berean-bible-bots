# Construct Chain

*Chapter 10 — Hebrew Construct Chain*

[Full screen](ch10-construct-chain.html){.md-button}  [Markdown](ch10-construct-chain.md){.md-button}  [Print (PDF)](ch10-construct-chain.pdf){.md-button}

<style>

  body { font-family: Georgia, serif;    color: #222; line-height: 1.6; }
  h1 { font-size: 1.45rem; border-bottom: 2px solid #555; padding-bottom: .4rem; }
  h2 { font-size: 1.05rem; margin-top: 2.2rem; color: #333; border-bottom: 1px solid #ddd; padding-bottom: .25rem; }
  .subtitle { color: #666; font-style: italic; margin-top: -.4rem; margin-bottom: .5rem; }
  .instructions { background: #f8f8f0; border-left: 4px solid #bbb; padding: .75rem 1rem; margin: 1rem 0; font-size: .92rem; }
  table { border-collapse: collapse; width: 100%; margin: .4rem 0 1rem; font-size: .9rem; }
  th { background: #e0e8f0; padding: .4rem .55rem; border: 1px solid #bbb; text-align: left; font-size: .83rem; }
  td { padding: .32rem .45rem; border: 1px solid #ddd; vertical-align: middle; }
  td.num { text-align: center; font-weight: bold; color: #666; width: 2rem; }
  td.heb {
    font-size: 1.8em;
    direction: rtl;
    unicode-bidi: embed;
    font-weight: bold;
    width: 13rem;
    padding: .2rem .5rem;
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
  .ans-heb {
    font-size: 1.6em;
    direction: rtl;
    unicode-bidi: embed;
    width: 13rem;
  }
  .ans-cstr {
    font-size: 1.3em;
    direction: rtl;
    unicode-bidi: embed;
  }
  button.rbtn {
    font-size: .76rem;
    padding: .14rem .5rem;
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
    padding: .38rem .9rem;
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
  .reflect { background: #f4f0ff; border-left: 4px solid #9b7ecb; padding: .75rem 1rem; margin: 1.5rem 0; font-size: .93rem; }
  .reflect ol { margin: .5rem 0 0; padding-left: 1.3rem; }
  .reflect li { margin-bottom: .5rem; }
  @media print {
    .controls, button.rbtn { display: none; }
    input.f { border: none; border-bottom: 1px solid #aaa; border-radius: 0; background: transparent; }
    .answer-row { display: none !important; }
    h1 { font-size: 1.2rem; }
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

<h1>Ch10 Construct Chain Drill</h1>
<p class="subtitle">BBH Chapter 10 · 25 construct chains</p>

<div class="instructions">
  <strong>Instructions:</strong> For each Hebrew construct chain, fill in: (a) <em>Construct Noun</em> — give the Hebrew word and note its form type; (b) <em>Absolute Noun</em> — the governing noun; (c) <em>Definite?</em> — Yes or No; (d) <em>Translation</em> — natural English.<br>
  Use <strong>▶ Answer</strong> to reveal the answer for any row, or use the buttons below to show/hide/clear all at once.
</div>

<div class="controls">
  <button onclick="showAll()">Show All Answers</button>
  <button onclick="hideAll()">Hide All Answers</button>
  <button class="clr" onclick="clearAll()">Clear All Inputs</button>
</div>

<!-- PART A -->
<h2>Part A — Simple 2-Link Chains (Indefinite)</h2>
<p style="font-size:.9rem; color:#555;">The absolute noun has no article and is not a proper noun. The whole chain is indefinite.</p>
<table>
  <tr>
    <th>#</th>
    <th>Hebrew</th>
    <th>Construct Noun</th>
    <th>Absolute Noun</th>
    <th>Definite?</th>
    <th>Translation</th>
    <th></th>
  </tr>

  <tr>
    <td class="num">1</td>
    <td class="heb">דְּבַר מֶלֶךְ</td>
    <td><input class="parse-field" id="1-c" placeholder="construct noun + form"></td>
    <td><input class="parse-field" id="1-a" placeholder="absolute noun"></td>
    <td><input class="parse-field" id="1-d" placeholder="Yes / No"></td>
    <td><input class="parse-field" id="1-t" placeholder="translation"></td>
    <td><button class="rbtn" onclick="tog(1)">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="ans-1">
    <td class="ans-lbl">✓</td>
    <td class="ans-heb">דְּבַר מֶלֶךְ</td>
    <td class="ans-cstr">דְּבַר (ms cstr; propretonic reduction)</td>
    <td class="ans-cstr">מֶלֶךְ</td>
    <td>No</td>
    <td>a word of a king</td>
    <td></td>
  </tr>

  <tr>
    <td class="num">2</td>
    <td class="heb">בֵּית אִישׁ</td>
    <td><input class="parse-field" id="2-c" placeholder="construct noun + form"></td>
    <td><input class="parse-field" id="2-a" placeholder="absolute noun"></td>
    <td><input class="parse-field" id="2-d" placeholder="Yes / No"></td>
    <td><input class="parse-field" id="2-t" placeholder="translation"></td>
    <td><button class="rbtn" onclick="tog(2)">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="ans-2">
    <td class="ans-lbl">✓</td>
    <td class="ans-heb">בֵּית אִישׁ</td>
    <td class="ans-cstr">בֵּית (ms cstr of בַּיִת)</td>
    <td class="ans-cstr">אִישׁ</td>
    <td>No</td>
    <td>a man's house</td>
    <td></td>
  </tr>

  <tr>
    <td class="num">3</td>
    <td class="heb">כְּבוֹד עָם</td>
    <td><input class="parse-field" id="3-c" placeholder="construct noun + form"></td>
    <td><input class="parse-field" id="3-a" placeholder="absolute noun"></td>
    <td><input class="parse-field" id="3-d" placeholder="Yes / No"></td>
    <td><input class="parse-field" id="3-t" placeholder="translation"></td>
    <td><button class="rbtn" onclick="tog(3)">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="ans-3">
    <td class="ans-lbl">✓</td>
    <td class="ans-heb">כְּבוֹד עָם</td>
    <td class="ans-cstr">כְּבוֹד (ms cstr of כָּבוֹד)</td>
    <td class="ans-cstr">עָם</td>
    <td>No</td>
    <td>glory of a people</td>
    <td></td>
  </tr>

  <tr>
    <td class="num">4</td>
    <td class="heb">עֶבֶד מֶלֶךְ</td>
    <td><input class="parse-field" id="4-c" placeholder="construct noun + form"></td>
    <td><input class="parse-field" id="4-a" placeholder="absolute noun"></td>
    <td><input class="parse-field" id="4-d" placeholder="Yes / No"></td>
    <td><input class="parse-field" id="4-t" placeholder="translation"></td>
    <td><button class="rbtn" onclick="tog(4)">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="ans-4">
    <td class="ans-lbl">✓</td>
    <td class="ans-heb">עֶבֶד מֶלֶךְ</td>
    <td class="ans-cstr">עֶבֶד (ms cstr; segolate, unchanged)</td>
    <td class="ans-cstr">מֶלֶךְ</td>
    <td>No</td>
    <td>a servant of a king</td>
    <td></td>
  </tr>

  <tr>
    <td class="num">5</td>
    <td class="heb">בְּנֵי אָדָם</td>
    <td><input class="parse-field" id="5-c" placeholder="construct noun + form"></td>
    <td><input class="parse-field" id="5-a" placeholder="absolute noun"></td>
    <td><input class="parse-field" id="5-d" placeholder="Yes / No"></td>
    <td><input class="parse-field" id="5-t" placeholder="translation"></td>
    <td><button class="rbtn" onclick="tog(5)">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="ans-5">
    <td class="ans-lbl">✓</td>
    <td class="ans-heb">בְּנֵי אָדָם</td>
    <td class="ans-cstr">בְּנֵי (mp cstr of בֵּן; ִים → ֵי)</td>
    <td class="ans-cstr">אָדָם</td>
    <td>No</td>
    <td>sons of man / humankind</td>
    <td></td>
  </tr>

  <tr>
    <td class="num">6</td>
    <td class="heb">סֵפֶר תּוֹרָה</td>
    <td><input class="parse-field" id="6-c" placeholder="construct noun + form"></td>
    <td><input class="parse-field" id="6-a" placeholder="absolute noun"></td>
    <td><input class="parse-field" id="6-d" placeholder="Yes / No"></td>
    <td><input class="parse-field" id="6-t" placeholder="translation"></td>
    <td><button class="rbtn" onclick="tog(6)">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="ans-6">
    <td class="ans-lbl">✓</td>
    <td class="ans-heb">סֵפֶר תּוֹרָה</td>
    <td class="ans-cstr">סֵפֶר (ms cstr; segolate, unchanged)</td>
    <td class="ans-cstr">תּוֹרָה</td>
    <td>No</td>
    <td>a book of the law</td>
    <td></td>
  </tr>

  <tr>
    <td class="num">7</td>
    <td class="heb">כֹּהֵן אֱלֹהִים</td>
    <td><input class="parse-field" id="7-c" placeholder="construct noun + form"></td>
    <td><input class="parse-field" id="7-a" placeholder="absolute noun"></td>
    <td><input class="parse-field" id="7-d" placeholder="Yes / No"></td>
    <td><input class="parse-field" id="7-t" placeholder="translation"></td>
    <td><button class="rbtn" onclick="tog(7)">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="ans-7">
    <td class="ans-lbl">✓</td>
    <td class="ans-heb">כֹּהֵן אֱלֹהִים</td>
    <td class="ans-cstr">כֹּהֵן (ms cstr; unchanged)</td>
    <td class="ans-cstr">אֱלֹהִים</td>
    <td>No</td>
    <td>a priest of God</td>
    <td></td>
  </tr>

  <tr>
    <td class="num">8</td>
    <td class="heb">רוּחַ אָדָם</td>
    <td><input class="parse-field" id="8-c" placeholder="construct noun + form"></td>
    <td><input class="parse-field" id="8-a" placeholder="absolute noun"></td>
    <td><input class="parse-field" id="8-d" placeholder="Yes / No"></td>
    <td><input class="parse-field" id="8-t" placeholder="translation"></td>
    <td><button class="rbtn" onclick="tog(8)">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="ans-8">
    <td class="ans-lbl">✓</td>
    <td class="ans-heb">רוּחַ אָדָם</td>
    <td class="ans-cstr">רוּחַ (fs cstr; unchanged)</td>
    <td class="ans-cstr">אָדָם</td>
    <td>No</td>
    <td>the spirit of man</td>
    <td></td>
  </tr>
</table>

<hr class="sec">

<!-- PART B -->
<h2>Part B — Simple 2-Link Chains (Definite)</h2>
<p style="font-size:.9rem; color:#555;">The absolute noun has the definite article <strong>הַ</strong> or is a proper noun. The whole chain is definite.</p>
<table>
  <tr>
    <th>#</th>
    <th>Hebrew</th>
    <th>Construct Noun</th>
    <th>Absolute Noun</th>
    <th>Definite?</th>
    <th>Translation</th>
    <th></th>
  </tr>

  <tr>
    <td class="num">9</td>
    <td class="heb">דְּבַר יְהוָה</td>
    <td><input class="parse-field" id="9-c" placeholder="construct noun + form"></td>
    <td><input class="parse-field" id="9-a" placeholder="absolute noun"></td>
    <td><input class="parse-field" id="9-d" placeholder="Yes / No"></td>
    <td><input class="parse-field" id="9-t" placeholder="translation"></td>
    <td><button class="rbtn" onclick="tog(9)">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="ans-9">
    <td class="ans-lbl">✓</td>
    <td class="ans-heb">דְּבַר יְהוָה</td>
    <td class="ans-cstr">דְּבַר (ms cstr; propretonic reduction)</td>
    <td class="ans-cstr">יְהוָה (proper noun)</td>
    <td>Yes — proper noun</td>
    <td>the word of the LORD</td>
    <td></td>
  </tr>

  <tr>
    <td class="num">10</td>
    <td class="heb">בֵּית יְהוָה</td>
    <td><input class="parse-field" id="10-c" placeholder="construct noun + form"></td>
    <td><input class="parse-field" id="10-a" placeholder="absolute noun"></td>
    <td><input class="parse-field" id="10-d" placeholder="Yes / No"></td>
    <td><input class="parse-field" id="10-t" placeholder="translation"></td>
    <td><button class="rbtn" onclick="tog(10)">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="ans-10">
    <td class="ans-lbl">✓</td>
    <td class="ans-heb">בֵּית יְהוָה</td>
    <td class="ans-cstr">בֵּית (ms cstr of בַּיִת)</td>
    <td class="ans-cstr">יְהוָה (proper noun)</td>
    <td>Yes — proper noun</td>
    <td>the house of the LORD</td>
    <td></td>
  </tr>

  <tr>
    <td class="num">11</td>
    <td class="heb">כְּבוֹד יְהוָה</td>
    <td><input class="parse-field" id="11-c" placeholder="construct noun + form"></td>
    <td><input class="parse-field" id="11-a" placeholder="absolute noun"></td>
    <td><input class="parse-field" id="11-d" placeholder="Yes / No"></td>
    <td><input class="parse-field" id="11-t" placeholder="translation"></td>
    <td><button class="rbtn" onclick="tog(11)">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="ans-11">
    <td class="ans-lbl">✓</td>
    <td class="ans-heb">כְּבוֹד יְהוָה</td>
    <td class="ans-cstr">כְּבוֹד (ms cstr of כָּבוֹד)</td>
    <td class="ans-cstr">יְהוָה (proper noun)</td>
    <td>Yes — proper noun</td>
    <td>the glory of the LORD</td>
    <td></td>
  </tr>

  <tr>
    <td class="num">12</td>
    <td class="heb">שֵׁם יְהוָה</td>
    <td><input class="parse-field" id="12-c" placeholder="construct noun + form"></td>
    <td><input class="parse-field" id="12-a" placeholder="absolute noun"></td>
    <td><input class="parse-field" id="12-d" placeholder="Yes / No"></td>
    <td><input class="parse-field" id="12-t" placeholder="translation"></td>
    <td><button class="rbtn" onclick="tog(12)">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="ans-12">
    <td class="ans-lbl">✓</td>
    <td class="ans-heb">שֵׁם יְהוָה</td>
    <td class="ans-cstr">שֵׁם (ms cstr; unchanged)</td>
    <td class="ans-cstr">יְהוָה (proper noun)</td>
    <td>Yes — proper noun</td>
    <td>the name of the LORD</td>
    <td></td>
  </tr>

  <tr>
    <td class="num">13</td>
    <td class="heb">בֵּית הַמֶּלֶךְ</td>
    <td><input class="parse-field" id="13-c" placeholder="construct noun + form"></td>
    <td><input class="parse-field" id="13-a" placeholder="absolute noun"></td>
    <td><input class="parse-field" id="13-d" placeholder="Yes / No"></td>
    <td><input class="parse-field" id="13-t" placeholder="translation"></td>
    <td><button class="rbtn" onclick="tog(13)">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="ans-13">
    <td class="ans-lbl">✓</td>
    <td class="ans-heb">בֵּית הַמֶּלֶךְ</td>
    <td class="ans-cstr">בֵּית (ms cstr of בַּיִת)</td>
    <td class="ans-cstr">הַמֶּלֶךְ (definite article)</td>
    <td>Yes — article on absolute</td>
    <td>the king's house</td>
    <td></td>
  </tr>

  <tr>
    <td class="num">14</td>
    <td class="heb">מֶלֶךְ יִשְׂרָאֵל</td>
    <td><input class="parse-field" id="14-c" placeholder="construct noun + form"></td>
    <td><input class="parse-field" id="14-a" placeholder="absolute noun"></td>
    <td><input class="parse-field" id="14-d" placeholder="Yes / No"></td>
    <td><input class="parse-field" id="14-t" placeholder="translation"></td>
    <td><button class="rbtn" onclick="tog(14)">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="ans-14">
    <td class="ans-lbl">✓</td>
    <td class="ans-heb">מֶלֶךְ יִשְׂרָאֵל</td>
    <td class="ans-cstr">מֶלֶךְ (ms cstr; segolate, unchanged)</td>
    <td class="ans-cstr">יִשְׂרָאֵל (proper noun)</td>
    <td>Yes — proper noun</td>
    <td>the king of Israel</td>
    <td></td>
  </tr>

  <tr>
    <td class="num">15</td>
    <td class="heb">עִיר דָּוִד</td>
    <td><input class="parse-field" id="15-c" placeholder="construct noun + form"></td>
    <td><input class="parse-field" id="15-a" placeholder="absolute noun"></td>
    <td><input class="parse-field" id="15-d" placeholder="Yes / No"></td>
    <td><input class="parse-field" id="15-t" placeholder="translation"></td>
    <td><button class="rbtn" onclick="tog(15)">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="ans-15">
    <td class="ans-lbl">✓</td>
    <td class="ans-heb">עִיר דָּוִד</td>
    <td class="ans-cstr">עִיר (fs cstr; unchanged)</td>
    <td class="ans-cstr">דָּוִד (proper noun)</td>
    <td>Yes — proper noun</td>
    <td>the city of David</td>
    <td></td>
  </tr>

  <tr>
    <td class="num">16</td>
    <td class="heb">בְּנֵי יִשְׂרָאֵל</td>
    <td><input class="parse-field" id="16-c" placeholder="construct noun + form"></td>
    <td><input class="parse-field" id="16-a" placeholder="absolute noun"></td>
    <td><input class="parse-field" id="16-d" placeholder="Yes / No"></td>
    <td><input class="parse-field" id="16-t" placeholder="translation"></td>
    <td><button class="rbtn" onclick="tog(16)">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="ans-16">
    <td class="ans-lbl">✓</td>
    <td class="ans-heb">בְּנֵי יִשְׂרָאֵל</td>
    <td class="ans-cstr">בְּנֵי (mp cstr of בֵּן; ִים → ֵי)</td>
    <td class="ans-cstr">יִשְׂרָאֵל (proper noun)</td>
    <td>Yes — proper noun</td>
    <td>the sons / children of Israel</td>
    <td></td>
  </tr>
</table>

<hr class="sec">

<!-- PART C -->
<h2>Part C — Extended 3-Link Chains</h2>
<p style="font-size:.9rem; color:#555;">Each chain has three nouns. Identify all construct nouns (there will be two) and the single absolute noun.</p>
<table>
  <tr>
    <th>#</th>
    <th>Hebrew</th>
    <th>Construct Nouns (both)</th>
    <th>Absolute Noun</th>
    <th>Definite?</th>
    <th>Translation</th>
    <th></th>
  </tr>

  <tr>
    <td class="num">17</td>
    <td class="heb">דְּבַר תּוֹרַת יְהוָה</td>
    <td><input class="parse-field" id="17-c" placeholder="both construct nouns"></td>
    <td><input class="parse-field" id="17-a" placeholder="absolute noun"></td>
    <td><input class="parse-field" id="17-d" placeholder="Yes / No"></td>
    <td><input class="parse-field" id="17-t" placeholder="translation"></td>
    <td><button class="rbtn" onclick="tog(17)">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="ans-17">
    <td class="ans-lbl">✓</td>
    <td class="ans-heb">דְּבַר תּוֹרַת יְהוָה</td>
    <td class="ans-cstr">דְּבַר (ms cstr) + תּוֹרַת (fs cstr)</td>
    <td class="ans-cstr">יְהוָה (proper noun)</td>
    <td>Yes — proper noun</td>
    <td>the word of the law of the LORD</td>
    <td></td>
  </tr>

  <tr>
    <td class="num">18</td>
    <td class="heb">בֵּית אֱלֹהֵי יִשְׂרָאֵל</td>
    <td><input class="parse-field" id="18-c" placeholder="both construct nouns"></td>
    <td><input class="parse-field" id="18-a" placeholder="absolute noun"></td>
    <td><input class="parse-field" id="18-d" placeholder="Yes / No"></td>
    <td><input class="parse-field" id="18-t" placeholder="translation"></td>
    <td><button class="rbtn" onclick="tog(18)">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="ans-18">
    <td class="ans-lbl">✓</td>
    <td class="ans-heb">בֵּית אֱלֹהֵי יִשְׂרָאֵל</td>
    <td class="ans-cstr">בֵּית (ms cstr) + אֱלֹהֵי (mp cstr; ִים → ֵי)</td>
    <td class="ans-cstr">יִשְׂרָאֵל (proper noun)</td>
    <td>Yes — proper noun</td>
    <td>the house of the God of Israel</td>
    <td></td>
  </tr>

  <tr>
    <td class="num">19</td>
    <td class="heb">מֶלֶךְ מַלְכֵי הַמְּלָכִים</td>
    <td><input class="parse-field" id="19-c" placeholder="both construct nouns"></td>
    <td><input class="parse-field" id="19-a" placeholder="absolute noun"></td>
    <td><input class="parse-field" id="19-d" placeholder="Yes / No"></td>
    <td><input class="parse-field" id="19-t" placeholder="translation"></td>
    <td><button class="rbtn" onclick="tog(19)">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="ans-19">
    <td class="ans-lbl">✓</td>
    <td class="ans-heb">מֶלֶךְ מַלְכֵי הַמְּלָכִים</td>
    <td class="ans-cstr">מֶלֶךְ (ms cstr) + מַלְכֵי (mp cstr; ִים → ֵי)</td>
    <td class="ans-cstr">הַמְּלָכִים (definite article)</td>
    <td>Yes — article on absolute</td>
    <td>king of kings of the kings (= king of all kings)</td>
    <td></td>
  </tr>

  <tr>
    <td class="num">20</td>
    <td class="heb">שֵׁם יְהוָה אֱלֹהֵינוּ</td>
    <td><input class="parse-field" id="20-c" placeholder="both construct nouns"></td>
    <td><input class="parse-field" id="20-a" placeholder="absolute noun"></td>
    <td><input class="parse-field" id="20-d" placeholder="Yes / No"></td>
    <td><input class="parse-field" id="20-t" placeholder="translation"></td>
    <td><button class="rbtn" onclick="tog(20)">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="ans-20">
    <td class="ans-lbl">✓</td>
    <td class="ans-heb">שֵׁם יְהוָה אֱלֹהֵינוּ</td>
    <td class="ans-cstr">שֵׁם (ms cstr); אֱלֹהֵינוּ is appositive</td>
    <td class="ans-cstr">יְהוָה (proper noun) + אֱלֹהֵינוּ (appositive)</td>
    <td>Yes — proper noun</td>
    <td>the name of the LORD our God</td>
    <td></td>
  </tr>

  <tr>
    <td class="num">21</td>
    <td class="heb">עֶבֶד עַבְדֵי הַמֶּלֶךְ</td>
    <td><input class="parse-field" id="21-c" placeholder="both construct nouns"></td>
    <td><input class="parse-field" id="21-a" placeholder="absolute noun"></td>
    <td><input class="parse-field" id="21-d" placeholder="Yes / No"></td>
    <td><input class="parse-field" id="21-t" placeholder="translation"></td>
    <td><button class="rbtn" onclick="tog(21)">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="ans-21">
    <td class="ans-lbl">✓</td>
    <td class="ans-heb">עֶבֶד עַבְדֵי הַמֶּלֶךְ</td>
    <td class="ans-cstr">עֶבֶד (ms cstr) + עַבְדֵי (mp cstr; ִים → ֵי)</td>
    <td class="ans-cstr">הַמֶּלֶךְ (definite article)</td>
    <td>Yes — article on absolute</td>
    <td>servant of the servants of the king</td>
    <td></td>
  </tr>
</table>

<hr class="sec">

<!-- PART D -->
<h2>Part D — Feminine Construct Nouns (ַת ending)</h2>
<p style="font-size:.9rem; color:#555;">Each chain uses a feminine singular noun in the construct state. Note the characteristic <strong>ָה → ַת</strong> change.</p>
<table>
  <tr>
    <th>#</th>
    <th>Hebrew</th>
    <th>Construct Noun</th>
    <th>Absolute Noun</th>
    <th>Definite?</th>
    <th>Translation</th>
    <th></th>
  </tr>

  <tr>
    <td class="num">22</td>
    <td class="heb">תּוֹרַת מֹשֶׁה</td>
    <td><input class="parse-field" id="22-c" placeholder="construct noun + form"></td>
    <td><input class="parse-field" id="22-a" placeholder="absolute noun"></td>
    <td><input class="parse-field" id="22-d" placeholder="Yes / No"></td>
    <td><input class="parse-field" id="22-t" placeholder="translation"></td>
    <td><button class="rbtn" onclick="tog(22)">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="ans-22">
    <td class="ans-lbl">✓</td>
    <td class="ans-heb">תּוֹרַת מֹשֶׁה</td>
    <td class="ans-cstr">תּוֹרַת (fs cstr; תּוֹרָה → תּוֹרַת)</td>
    <td class="ans-cstr">מֹשֶׁה (proper noun)</td>
    <td>Yes — proper noun</td>
    <td>the law / Torah of Moses</td>
    <td></td>
  </tr>

  <tr>
    <td class="num">23</td>
    <td class="heb">תּוֹרַת יְהוָה</td>
    <td><input class="parse-field" id="23-c" placeholder="construct noun + form"></td>
    <td><input class="parse-field" id="23-a" placeholder="absolute noun"></td>
    <td><input class="parse-field" id="23-d" placeholder="Yes / No"></td>
    <td><input class="parse-field" id="23-t" placeholder="translation"></td>
    <td><button class="rbtn" onclick="tog(23)">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="ans-23">
    <td class="ans-lbl">✓</td>
    <td class="ans-heb">תּוֹרַת יְהוָה</td>
    <td class="ans-cstr">תּוֹרַת (fs cstr; תּוֹרָה → תּוֹרַת)</td>
    <td class="ans-cstr">יְהוָה (proper noun)</td>
    <td>Yes — proper noun</td>
    <td>the law / Torah of the LORD</td>
    <td></td>
  </tr>

  <tr>
    <td class="num">24</td>
    <td class="heb">מַלְכַּת שְׁבָא</td>
    <td><input class="parse-field" id="24-c" placeholder="construct noun + form"></td>
    <td><input class="parse-field" id="24-a" placeholder="absolute noun"></td>
    <td><input class="parse-field" id="24-d" placeholder="Yes / No"></td>
    <td><input class="parse-field" id="24-t" placeholder="translation"></td>
    <td><button class="rbtn" onclick="tog(24)">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="ans-24">
    <td class="ans-lbl">✓</td>
    <td class="ans-heb">מַלְכַּת שְׁבָא</td>
    <td class="ans-cstr">מַלְכַּת (fs cstr; מַלְכָּה → מַלְכַּת)</td>
    <td class="ans-cstr">שְׁבָא (proper noun)</td>
    <td>Yes — proper noun</td>
    <td>the queen of Sheba</td>
    <td></td>
  </tr>

  <tr>
    <td class="num">25</td>
    <td class="heb">בִּרְכַּת יְהוָה</td>
    <td><input class="parse-field" id="25-c" placeholder="construct noun + form"></td>
    <td><input class="parse-field" id="25-a" placeholder="absolute noun"></td>
    <td><input class="parse-field" id="25-d" placeholder="Yes / No"></td>
    <td><input class="parse-field" id="25-t" placeholder="translation"></td>
    <td><button class="rbtn" onclick="tog(25)">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="ans-25">
    <td class="ans-lbl">✓</td>
    <td class="ans-heb">בִּרְכַּת יְהוָה</td>
    <td class="ans-cstr">בִּרְכַּת (fs cstr; בְּרָכָה → בִּרְכַּת)</td>
    <td class="ans-cstr">יְהוָה (proper noun)</td>
    <td>Yes — proper noun</td>
    <td>the blessing of the LORD</td>
    <td></td>
  </tr>
</table>

<hr class="sec">

<div class="reflect">
  <strong>Reflection Questions</strong>
  <ol>
    <li>In items 5 and 16, both chains contain בְּנֵי. What morphological change marks this word as a construct plural rather than an absolute plural? What is the absolute form of this noun?</li>
    <li>Why can't the definite article appear on the construct noun? In item 13 (בֵּית הַמֶּלֶךְ), which noun carries the article — and what does that tell us about the definiteness of the entire chain?</li>
    <li>In item 17 (דְּבַר תּוֹרַת יְהוָה), two nouns are in the construct state. How do you know תּוֹרַת is in the construct state? What would the absolute form of that noun look like, and what ending would it have?</li>
  </ol>
</div>

<script>
  function tog(n) {
    const row = document.getElementById('ans-' + n);
    const btn = event.currentTarget;
    if (row.style.display === 'table-row') {
      row.style.display = 'none';
      btn.classList.remove('on');
      btn.textContent = '▶ Answer';
    } else {
      row.style.display = 'table-row';
      btn.classList.add('on');
      btn.textContent = '▼ Hide';
    }
  }

  function showAll() {
    document.querySelectorAll('.answer-row').forEach(r => r.style.display = 'table-row');
    document.querySelectorAll('.rbtn').forEach(b => { b.classList.add('on'); b.textContent = '▼ Hide'; });
  }

  function hideAll() {
    document.querySelectorAll('.answer-row').forEach(r => r.style.display = 'none');
    document.querySelectorAll('.rbtn').forEach(b => { b.classList.remove('on'); b.textContent = '▶ Answer'; });
  }

  function clearAll() {
    document.querySelectorAll('input.f').forEach(i => i.value = '');
    hideAll();
  }
</script>

