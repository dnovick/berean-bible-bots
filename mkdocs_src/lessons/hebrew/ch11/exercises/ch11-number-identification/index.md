# Number Identification

*Chapter 11 — Hebrew Numbers*

[Full screen](ch11-number-identification.html){.md-button}  [Markdown](ch11-number-identification.md){.md-button}  [Print (PDF)](ch11-number-identification.pdf){.md-button}

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
  td.heb { font-size: 1.8em; direction: rtl; unicode-bidi: embed; font-weight: bold; min-width: 12rem; }
  td.heb-ans { font-size: 1.4em; direction: rtl; unicode-bidi: embed; }
  input.f { width: 100%; box-sizing: border-box; border: 1px solid #bbb; border-radius: 3px; padding: .22rem .4rem; font-family: Georgia, serif; font-size: .87rem; background: #fafff8; }
  input.f:focus { outline: none; border-color: #5a9; box-shadow: 0 0 0 2px #c8ecd4; }
  input.f-heb { font-size: 1.2em; direction: rtl; unicode-bidi: embed; width: 100%; box-sizing: border-box; border: 1px solid #bbb; border-radius: 3px; padding: .22rem .4rem; background: #fafff8; }
  input.f-heb:focus { outline: none; border-color: #5a9; box-shadow: 0 0 0 2px #c8ecd4; }
  .ans-row { display: none; background: #f0faf0; }
  .ans-row td { font-size: .87rem; color: #2a6e2a; padding: .28rem .45rem; }
  .ans-lbl { font-weight: bold; color: #1a5c1a; width: 2rem; text-align: center; }
  button.rbtn { font-size: .76rem; padding: .14rem .48rem; cursor: pointer; background: #e8f4ec; border: 1px solid #7bba8f; border-radius: 3px; color: #2a6e2a; white-space: nowrap; }
  button.rbtn:hover, button.rbtn.on { background: #c8ecd4; }
  .controls { display: flex; gap: .7rem; flex-wrap: wrap; margin: 1rem 0 1.5rem; }
  .controls button { padding: .38rem .85rem; cursor: pointer; border-radius: 4px; font-size: .88rem; border: 1px solid #999; background: #f0f0f0; color: #333; }
  .controls button:hover { background: #ddd; }
  .clr { border-color: #c06060 !important; color: #8b0000 !important; background: #fff0f0 !important; }
  .clr:hover { background: #ffd8d8 !important; }
  hr.sec { border: none; border-top: 2px dashed #ccc; margin: 2rem 0; }
  .notes { background: #fffbe8; border-left: 4px solid #d4b800; padding: .7rem 1rem; margin: 1rem 0; font-size: .9rem; }
  .notes h3 { font-size: .95rem; margin: 0 0 .4rem 0; color: #6a5700; }
  .note-item { margin: .4rem 0; }
  .reflect { background: #f4f0fc; border-left: 4px solid #9070cc; padding: .7rem 1rem; margin: 1rem 0; font-size: .9rem; }
  .reflect h3 { font-size: .95rem; margin: 0 0 .4rem 0; color: #4a2a8a; }
  .reflect ol { margin: .4rem 0; padding-left: 1.4rem; }
  .reflect li { margin-bottom: .35rem; }
  .ans-block { display: none; background: #eef6e8; border: 1px solid #9bd09b; border-radius: 4px; padding: .6rem .9rem; margin-top: .5rem; font-size: .89rem; }
  button.toggle-ans { font-size: .8rem; padding: .18rem .55rem; cursor: pointer; background: #e8f4ec; border: 1px solid #7bba8f; border-radius: 3px; color: #2a6e2a; margin-top: .3rem; }
  button.toggle-ans:hover { background: #c8ecd4; }
  @media print {
    .controls, button.rbtn, button.toggle-ans { display: none; }
    input.f, input.f-heb { border: none; border-bottom: 1px solid #aaa; border-radius: 0; background: transparent; }
    .ans-row { display: none !important; }
    .ans-block { display: none !important; }
  }

</style>

<h1>Ch11 Number Identification Drill — Hebrew Numbers</h1>
<p class="subtitle">BBH Chapter 11 · 20 items</p>

<div class="instructions">
  <strong>Instructions:</strong> For each Hebrew number-noun phrase, fill in: (a) the number word, (b) its numeric value, (c) whether gender polarity applies and how, (d) an English translation.<br>
  <em>Gender Polarity: note "yes — [noun gender] noun + [form used]" for cardinals 3–10, "N/A" for 1–2, tens, and ordinals.</em>
</div>

<div class="controls">
  <button onclick="showAll()">Show All Answers</button>
  <button onclick="hideAll()">Hide All Answers</button>
  <button class="clr" onclick="clearAll()">Clear All Inputs</button>
</div>

<!-- PART A: Cardinals 1–10 -->
<h2>Part A — Cardinal Numbers 1–10 (Gender Polarity)</h2>
<table>
  <tr>
    <th>#</th>
    <th>Hebrew Phrase</th>
    <th>Number Word</th>
    <th>Value</th>
    <th>Gender Polarity?</th>
    <th>Translation</th>
    <th></th>
  </tr>

  <!-- Item 1 -->
  <tr>
    <td class="num">1</td>
    <td class="heb">שִׁבְעָה יָמִים</td>
    <td><input class="f-heb" id="1-nw" placeholder="Hebrew number word"></td>
    <td><input class="parse-field" id="1-v" placeholder="number"></td>
    <td><input class="parse-field" id="1-gp" placeholder="yes/N/A + explanation"></td>
    <td><input class="parse-field" id="1-tr" placeholder="English translation"></td>
    <td><button class="rbtn" onclick="tog(1)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-1">
    <td class="ans-lbl">✓</td>
    <td class="heb-ans">שִׁבְעָה יָמִים</td>
    <td class="heb-ans">שִׁבְעָה</td>
    <td>7</td>
    <td>Yes — masc. noun (יָמִים) + ה-form</td>
    <td>seven days</td>
    <td></td>
  </tr>

  <!-- Item 2 -->
  <tr>
    <td class="num">2</td>
    <td class="heb">שָׁלֹשׁ נָשִׁים</td>
    <td><input class="f-heb" id="2-nw" placeholder="Hebrew number word"></td>
    <td><input class="parse-field" id="2-v" placeholder="number"></td>
    <td><input class="parse-field" id="2-gp" placeholder="yes/N/A + explanation"></td>
    <td><input class="parse-field" id="2-tr" placeholder="English translation"></td>
    <td><button class="rbtn" onclick="tog(2)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-2">
    <td class="ans-lbl">✓</td>
    <td class="heb-ans">שָׁלֹשׁ נָשִׁים</td>
    <td class="heb-ans">שָׁלֹשׁ</td>
    <td>3</td>
    <td>Yes — fem. noun (נָשִׁים) + non-ה-form</td>
    <td>three women</td>
    <td></td>
  </tr>

  <!-- Item 3 -->
  <tr>
    <td class="num">3</td>
    <td class="heb">אַרְבָּעִים שָׁנָה</td>
    <td><input class="f-heb" id="3-nw" placeholder="Hebrew number word"></td>
    <td><input class="parse-field" id="3-v" placeholder="number"></td>
    <td><input class="parse-field" id="3-gp" placeholder="yes/N/A + explanation"></td>
    <td><input class="parse-field" id="3-tr" placeholder="English translation"></td>
    <td><button class="rbtn" onclick="tog(3)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-3">
    <td class="ans-lbl">✓</td>
    <td class="heb-ans">אַרְבָּעִים שָׁנָה</td>
    <td class="heb-ans">אַרְבָּעִים</td>
    <td>40</td>
    <td>N/A — tens are invariable (no polarity)</td>
    <td>forty years</td>
    <td></td>
  </tr>

  <!-- Item 4 -->
  <tr>
    <td class="num">4</td>
    <td class="heb">שְׁנֵי אֲנָשִׁים</td>
    <td><input class="f-heb" id="4-nw" placeholder="Hebrew number word"></td>
    <td><input class="parse-field" id="4-v" placeholder="number"></td>
    <td><input class="parse-field" id="4-gp" placeholder="yes/N/A + explanation"></td>
    <td><input class="parse-field" id="4-tr" placeholder="English translation"></td>
    <td><button class="rbtn" onclick="tog(4)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-4">
    <td class="ans-lbl">✓</td>
    <td class="heb-ans">שְׁנֵי אֲנָשִׁים</td>
    <td class="heb-ans">שְׁנֵי</td>
    <td>2</td>
    <td>N/A — 1–2 agree normally; construct form שְׁנֵי</td>
    <td>two men</td>
    <td></td>
  </tr>

  <!-- Item 5 -->
  <tr>
    <td class="num">5</td>
    <td class="heb">עֶשֶׂר עָרִים</td>
    <td><input class="f-heb" id="5-nw" placeholder="Hebrew number word"></td>
    <td><input class="parse-field" id="5-v" placeholder="number"></td>
    <td><input class="parse-field" id="5-gp" placeholder="yes/N/A + explanation"></td>
    <td><input class="parse-field" id="5-tr" placeholder="English translation"></td>
    <td><button class="rbtn" onclick="tog(5)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-5">
    <td class="ans-lbl">✓</td>
    <td class="heb-ans">עֶשֶׂר עָרִים</td>
    <td class="heb-ans">עֶשֶׂר</td>
    <td>10</td>
    <td>Yes — fem. noun (עָרִים) + non-ה-form</td>
    <td>ten cities</td>
    <td></td>
  </tr>

  <!-- Item 6 -->
  <tr>
    <td class="num">6</td>
    <td class="heb">חֲמִשָּׁה שְׁבָטִים</td>
    <td><input class="f-heb" id="6-nw" placeholder="Hebrew number word"></td>
    <td><input class="parse-field" id="6-v" placeholder="number"></td>
    <td><input class="parse-field" id="6-gp" placeholder="yes/N/A + explanation"></td>
    <td><input class="parse-field" id="6-tr" placeholder="English translation"></td>
    <td><button class="rbtn" onclick="tog(6)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-6">
    <td class="ans-lbl">✓</td>
    <td class="heb-ans">חֲמִשָּׁה שְׁבָטִים</td>
    <td class="heb-ans">חֲמִשָּׁה</td>
    <td>5</td>
    <td>Yes — masc. noun (שְׁבָטִים) + ה-form</td>
    <td>five tribes</td>
    <td></td>
  </tr>

  <!-- Item 7 -->
  <tr>
    <td class="num">7</td>
    <td class="heb">שְׁתַּיִם עֶשְׂרֵה שָׁנָה</td>
    <td><input class="f-heb" id="7-nw" placeholder="Hebrew number word"></td>
    <td><input class="parse-field" id="7-v" placeholder="number"></td>
    <td><input class="parse-field" id="7-gp" placeholder="yes/N/A + explanation"></td>
    <td><input class="parse-field" id="7-tr" placeholder="English translation"></td>
    <td><button class="rbtn" onclick="tog(7)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-7">
    <td class="ans-lbl">✓</td>
    <td class="heb-ans">שְׁתַּיִם עֶשְׂרֵה שָׁנָה</td>
    <td class="heb-ans">שְׁתַּיִם עֶשְׂרֵה</td>
    <td>12</td>
    <td>N/A (12 uses dual; עֶשְׂרֵה agrees fem. with שָׁנָה)</td>
    <td>twelve years</td>
    <td></td>
  </tr>

  <!-- Item 8 -->
  <tr>
    <td class="num">8</td>
    <td class="heb">שִׁשָּׁה בָּנִים</td>
    <td><input class="f-heb" id="8-nw" placeholder="Hebrew number word"></td>
    <td><input class="parse-field" id="8-v" placeholder="number"></td>
    <td><input class="parse-field" id="8-gp" placeholder="yes/N/A + explanation"></td>
    <td><input class="parse-field" id="8-tr" placeholder="English translation"></td>
    <td><button class="rbtn" onclick="tog(8)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-8">
    <td class="ans-lbl">✓</td>
    <td class="heb-ans">שִׁשָּׁה בָּנִים</td>
    <td class="heb-ans">שִׁשָּׁה</td>
    <td>6</td>
    <td>Yes — masc. noun (בָּנִים) + ה-form</td>
    <td>six sons</td>
    <td></td>
  </tr>
</table>

<hr class="sec">

<!-- PART B: Tens and Teens -->
<h2>Part B — Tens and Additional Cardinals</h2>
<table>
  <tr>
    <th>#</th>
    <th>Hebrew Phrase</th>
    <th>Number Word</th>
    <th>Value</th>
    <th>Gender Polarity?</th>
    <th>Translation</th>
    <th></th>
  </tr>

  <!-- Item 9 -->
  <tr>
    <td class="num">9</td>
    <td class="heb">שְׁלֹשִׁים אִישׁ</td>
    <td><input class="f-heb" id="9-nw" placeholder="Hebrew number word"></td>
    <td><input class="parse-field" id="9-v" placeholder="number"></td>
    <td><input class="parse-field" id="9-gp" placeholder="yes/N/A + explanation"></td>
    <td><input class="parse-field" id="9-tr" placeholder="English translation"></td>
    <td><button class="rbtn" onclick="tog(9)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-9">
    <td class="ans-lbl">✓</td>
    <td class="heb-ans">שְׁלֹשִׁים אִישׁ</td>
    <td class="heb-ans">שְׁלֹשִׁים</td>
    <td>30</td>
    <td>N/A — tens are invariable (no polarity)</td>
    <td>thirty men</td>
    <td></td>
  </tr>

  <!-- Item 10 -->
  <tr>
    <td class="num">10</td>
    <td class="heb">תִּשְׁעָה אֲנָשִׁים</td>
    <td><input class="f-heb" id="10-nw" placeholder="Hebrew number word"></td>
    <td><input class="parse-field" id="10-v" placeholder="number"></td>
    <td><input class="parse-field" id="10-gp" placeholder="yes/N/A + explanation"></td>
    <td><input class="parse-field" id="10-tr" placeholder="English translation"></td>
    <td><button class="rbtn" onclick="tog(10)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-10">
    <td class="ans-lbl">✓</td>
    <td class="heb-ans">תִּשְׁעָה אֲנָשִׁים</td>
    <td class="heb-ans">תִּשְׁעָה</td>
    <td>9</td>
    <td>Yes — masc. noun (אֲנָשִׁים) + ה-form</td>
    <td>nine men</td>
    <td></td>
  </tr>

  <!-- Item 11 -->
  <tr>
    <td class="num">11</td>
    <td class="heb">שְׁנֵים עָשָׂר שֵׁבֶט</td>
    <td><input class="f-heb" id="11-nw" placeholder="Hebrew number word"></td>
    <td><input class="parse-field" id="11-v" placeholder="number"></td>
    <td><input class="parse-field" id="11-gp" placeholder="yes/N/A + explanation"></td>
    <td><input class="parse-field" id="11-tr" placeholder="English translation"></td>
    <td><button class="rbtn" onclick="tog(11)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-11">
    <td class="ans-lbl">✓</td>
    <td class="heb-ans">שְׁנֵים עָשָׂר שֵׁבֶט</td>
    <td class="heb-ans">שְׁנֵים עָשָׂר</td>
    <td>12</td>
    <td>N/A (12 uses dual; עָשָׂר = masc. form of ten with masc. noun שֵׁבֶט)</td>
    <td>twelve tribes</td>
    <td></td>
  </tr>

  <!-- Item 12 -->
  <tr>
    <td class="num">12</td>
    <td class="heb">אַרְבַּע בָּנוֹת</td>
    <td><input class="f-heb" id="12-nw" placeholder="Hebrew number word"></td>
    <td><input class="parse-field" id="12-v" placeholder="number"></td>
    <td><input class="parse-field" id="12-gp" placeholder="yes/N/A + explanation"></td>
    <td><input class="parse-field" id="12-tr" placeholder="English translation"></td>
    <td><button class="rbtn" onclick="tog(12)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-12">
    <td class="ans-lbl">✓</td>
    <td class="heb-ans">אַרְבַּע בָּנוֹת</td>
    <td class="heb-ans">אַרְבַּע</td>
    <td>4</td>
    <td>Yes — fem. noun (בָּנוֹת) + non-ה-form</td>
    <td>four daughters</td>
    <td></td>
  </tr>

  <!-- Item 13 -->
  <tr>
    <td class="num">13</td>
    <td class="heb">חֲמִשָּׁה עָשָׂר אִישׁ</td>
    <td><input class="f-heb" id="13-nw" placeholder="Hebrew number word"></td>
    <td><input class="parse-field" id="13-v" placeholder="number"></td>
    <td><input class="parse-field" id="13-gp" placeholder="yes/N/A + explanation"></td>
    <td><input class="parse-field" id="13-tr" placeholder="English translation"></td>
    <td><button class="rbtn" onclick="tog(13)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-13">
    <td class="ans-lbl">✓</td>
    <td class="heb-ans">חֲמִשָּׁה עָשָׂר אִישׁ</td>
    <td class="heb-ans">חֲמִשָּׁה עָשָׂר</td>
    <td>15</td>
    <td>Yes (unit portion) — masc. noun (אִישׁ) + ה-form unit + עָשָׂר</td>
    <td>fifteen men</td>
    <td></td>
  </tr>

  <!-- Item 14 -->
  <tr>
    <td class="num">14</td>
    <td class="heb">שִׁבְעִים זָקֵן</td>
    <td><input class="f-heb" id="14-nw" placeholder="Hebrew number word"></td>
    <td><input class="parse-field" id="14-v" placeholder="number"></td>
    <td><input class="parse-field" id="14-gp" placeholder="yes/N/A + explanation"></td>
    <td><input class="parse-field" id="14-tr" placeholder="English translation"></td>
    <td><button class="rbtn" onclick="tog(14)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-14">
    <td class="ans-lbl">✓</td>
    <td class="heb-ans">שִׁבְעִים זָקֵן</td>
    <td class="heb-ans">שִׁבְעִים</td>
    <td>70</td>
    <td>N/A — tens are invariable (no polarity)</td>
    <td>seventy elders</td>
    <td></td>
  </tr>

  <!-- Item 15 -->
  <tr>
    <td class="num">15</td>
    <td class="heb">שֵׁשׁ שָׁנִים</td>
    <td><input class="f-heb" id="15-nw" placeholder="Hebrew number word"></td>
    <td><input class="parse-field" id="15-v" placeholder="number"></td>
    <td><input class="parse-field" id="15-gp" placeholder="yes/N/A + explanation"></td>
    <td><input class="parse-field" id="15-tr" placeholder="English translation"></td>
    <td><button class="rbtn" onclick="tog(15)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-15">
    <td class="ans-lbl">✓</td>
    <td class="heb-ans">שֵׁשׁ שָׁנִים</td>
    <td class="heb-ans">שֵׁשׁ</td>
    <td>6</td>
    <td>Yes — fem. noun (שָׁנִים) + non-ה-form</td>
    <td>six years</td>
    <td></td>
  </tr>

  <!-- Item 16 -->
  <tr>
    <td class="num">16</td>
    <td class="heb">שְׁלֹשׁ עֶשְׂרֵה עִיר</td>
    <td><input class="f-heb" id="16-nw" placeholder="Hebrew number word"></td>
    <td><input class="parse-field" id="16-v" placeholder="number"></td>
    <td><input class="parse-field" id="16-gp" placeholder="yes/N/A + explanation"></td>
    <td><input class="parse-field" id="16-tr" placeholder="English translation"></td>
    <td><button class="rbtn" onclick="tog(16)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-16">
    <td class="ans-lbl">✓</td>
    <td class="heb-ans">שְׁלֹשׁ עֶשְׂרֵה עִיר</td>
    <td class="heb-ans">שְׁלֹשׁ עֶשְׂרֵה</td>
    <td>13</td>
    <td>Yes (unit portion) — fem. noun (עִיר) + non-ה-form unit + עֶשְׂרֵה; noun in singular</td>
    <td>thirteen cities</td>
    <td></td>
  </tr>
</table>

<hr class="sec">

<!-- PART C: Ordinals -->
<h2>Part C — Ordinal Numbers</h2>
<table>
  <tr>
    <th>#</th>
    <th>Hebrew Phrase</th>
    <th>Number Word</th>
    <th>Value</th>
    <th>Gender Polarity?</th>
    <th>Translation</th>
    <th></th>
  </tr>

  <!-- Item 17 -->
  <tr>
    <td class="num">17</td>
    <td class="heb">בַּיּוֹם הַשְּׁבִיעִי</td>
    <td><input class="f-heb" id="17-nw" placeholder="Hebrew number word"></td>
    <td><input class="parse-field" id="17-v" placeholder="number"></td>
    <td><input class="parse-field" id="17-gp" placeholder="yes/N/A + explanation"></td>
    <td><input class="parse-field" id="17-tr" placeholder="English translation"></td>
    <td><button class="rbtn" onclick="tog(17)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-17">
    <td class="ans-lbl">✓</td>
    <td class="heb-ans">בַּיּוֹם הַשְּׁבִיעִי</td>
    <td class="heb-ans">הַשְּׁבִיעִי</td>
    <td>7th</td>
    <td>N/A — ordinals agree normally as adjectives; no polarity</td>
    <td>on the seventh day</td>
    <td></td>
  </tr>

  <!-- Item 18 -->
  <tr>
    <td class="num">18</td>
    <td class="heb">בַּחֹדֶשׁ הָרִאשׁוֹן</td>
    <td><input class="f-heb" id="18-nw" placeholder="Hebrew number word"></td>
    <td><input class="parse-field" id="18-v" placeholder="number"></td>
    <td><input class="parse-field" id="18-gp" placeholder="yes/N/A + explanation"></td>
    <td><input class="parse-field" id="18-tr" placeholder="English translation"></td>
    <td><button class="rbtn" onclick="tog(18)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-18">
    <td class="ans-lbl">✓</td>
    <td class="heb-ans">בַּחֹדֶשׁ הָרִאשׁוֹן</td>
    <td class="heb-ans">הָרִאשׁוֹן</td>
    <td>1st</td>
    <td>N/A — ordinals agree normally as adjectives; no polarity</td>
    <td>in the first month</td>
    <td></td>
  </tr>

  <!-- Item 19 -->
  <tr>
    <td class="num">19</td>
    <td class="heb">הַשַּׁעַר הַשֵּׁנִי</td>
    <td><input class="f-heb" id="19-nw" placeholder="Hebrew number word"></td>
    <td><input class="parse-field" id="19-v" placeholder="number"></td>
    <td><input class="parse-field" id="19-gp" placeholder="yes/N/A + explanation"></td>
    <td><input class="parse-field" id="19-tr" placeholder="English translation"></td>
    <td><button class="rbtn" onclick="tog(19)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-19">
    <td class="ans-lbl">✓</td>
    <td class="heb-ans">הַשַּׁעַר הַשֵּׁנִי</td>
    <td class="heb-ans">הַשֵּׁנִי</td>
    <td>2nd</td>
    <td>N/A — ordinals agree normally as adjectives; no polarity</td>
    <td>the second gate</td>
    <td></td>
  </tr>

  <!-- Item 20 -->
  <tr>
    <td class="num">20</td>
    <td class="heb">הַיּוֹם הָעֲשִׂירִי</td>
    <td><input class="f-heb" id="20-nw" placeholder="Hebrew number word"></td>
    <td><input class="parse-field" id="20-v" placeholder="number"></td>
    <td><input class="parse-field" id="20-gp" placeholder="yes/N/A + explanation"></td>
    <td><input class="parse-field" id="20-tr" placeholder="English translation"></td>
    <td><button class="rbtn" onclick="tog(20)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-20">
    <td class="ans-lbl">✓</td>
    <td class="heb-ans">הַיּוֹם הָעֲשִׂירִי</td>
    <td class="heb-ans">הָעֲשִׂירִי</td>
    <td>10th</td>
    <td>N/A — ordinals agree normally as adjectives; no polarity</td>
    <td>the tenth day</td>
    <td></td>
  </tr>
</table>

<hr class="sec">

<!-- Notes -->
<div class="notes">
  <h3>Notes on Selected Items</h3>
  <div class="note-item"><strong>Item 1 (שִׁבְעָה יָמִים):</strong> יָמִים is the masculine plural of יוֹם ("day"). Because the noun is masculine, we use שִׁבְעָה (the ה-form). Classic gender polarity.</div>
  <div class="note-item"><strong>Item 2 (שָׁלֹשׁ נָשִׁים):</strong> נָשִׁים is the suppletive plural of אִשָּׁה ("woman") — a feminine noun. Because the noun is feminine, the non-ה-form שָׁלֹשׁ is used. The "masculine-looking" form goes with the feminine noun.</div>
  <div class="note-item"><strong>Item 5 (עֶשֶׂר עָרִים):</strong> עָרִים is feminine plural (from עִיר, "city"). The non-ה-form עֶשֶׂר is therefore used; עֲשָׂרָה (ה-form) would go with masculine nouns.</div>
  <div class="note-item"><strong>Items 7 &amp; 11 (12 with שָׁנָה / שֵׁבֶט):</strong> The number 12 uses the dual of שְׁנַיִם for its unit portion rather than the standard polarity pattern. The "ten" element still agrees: עָשָׂר with masculine nouns, עֶשְׂרֵה with feminine nouns.</div>
  <div class="note-item"><strong>Item 16 (שְׁלֹשׁ עֶשְׂרֵה עִיר):</strong> A teen number with a feminine noun. Note that עִיר appears in the <em>singular</em> (standard after teens). The unit שְׁלֹשׁ is the non-ה-form because the noun is feminine; עֶשְׂרֵה is the feminine form of "ten."</div>
  <div class="note-item"><strong>Items 17–20 (ordinals):</strong> Ordinals function as attributive adjectives — they follow the noun and take the definite article when the noun is definite. No gender polarity applies; they agree in gender normally.</div>
</div>

<!-- Reflection Questions -->
<div class="reflect">
  <h3>Reflection Questions</h3>
  <ol>
    <li>A student writes <span style="font-size:1.2em; direction:rtl; unicode-bidi:embed">שָׁלֹשׁ אֲנָשִׁים</span> for "three men." What is wrong, and what is the correct form?</li>
    <li>How do you determine whether to use <span style="font-size:1.2em; direction:rtl; unicode-bidi:embed">שִׁבְעָה</span> or <span style="font-size:1.2em; direction:rtl; unicode-bidi:embed">שֶׁבַע</span> when translating "seven cities" (<span style="font-size:1.2em; direction:rtl; unicode-bidi:embed">עָרִים</span>)?</li>
    <li>
      What is the difference between <span style="font-size:1.2em; direction:rtl; unicode-bidi:embed">שִׁשָּׁה</span> ("six," with a masculine noun) and <span style="font-size:1.2em; direction:rtl; unicode-bidi:embed">שִׁשִּׁי</span> ("sixth")? How does their syntactic behavior differ?
    </li>
  </ol>
  <button class="toggle-ans" onclick="toggleReflect()">▶ Show Answers</button>
  <div class="ans-block" id="reflect-ans">
    <p><strong>1.</strong> The student used the non-ה-form (שָׁלֹשׁ), which is used with <em>feminine</em> nouns. Since אֲנָשִׁים is <em>masculine</em> plural, the correct form is שְׁלֹשָׁה (the ה-form): <span style="font-size:1.2em; direction:rtl; unicode-bidi:embed">שְׁלֹשָׁה אֲנָשִׁים</span>.</p>
    <p><strong>2.</strong> עָרִים (cities) is the plural of עִיר, which is a <em>feminine</em> noun. Because the noun is feminine, gender polarity requires the non-ה-form: <span style="font-size:1.2em; direction:rtl; unicode-bidi:embed">שֶׁבַע עָרִים</span> ("seven cities").</p>
    <p><strong>3.</strong> שִׁשָּׁה is a <em>cardinal number</em> ("six") expressing quantity; it may precede or follow the noun and shows gender polarity (the ה-form is used with masculine nouns). שִׁשִּׁי is an <em>ordinal number</em> ("sixth"); it functions as an attributive adjective, always follows its noun, takes the definite article when the noun is definite, and agrees normally in gender — no polarity (e.g., <span style="font-size:1.2em; direction:rtl; unicode-bidi:embed">בַּיּוֹם הַשִּׁשִּׁי</span>, "on the sixth day").</p>
  </div>
</div>

<script>
function tog(n) {
  var row = document.getElementById('ans-' + n);
  var btn = event.target;
  if (row.style.display === 'table-row') {
    row.style.display = 'none';
    btn.textContent = '▶ Answer';
    btn.classList.remove('on');
  } else {
    row.style.display = 'table-row';
    btn.textContent = '▼ Hide';
    btn.classList.add('on');
  }
}
function showAll() {
  for (var i = 1; i <= 20; i++) {
    var row = document.getElementById('ans-' + i);
    if (row) row.style.display = 'table-row';
  }
  document.querySelectorAll('button.rbtn').forEach(function(b) {
    b.textContent = '▼ Hide';
    b.classList.add('on');
  });
}
function hideAll() {
  for (var i = 1; i <= 20; i++) {
    var row = document.getElementById('ans-' + i);
    if (row) row.style.display = 'none';
  }
  document.querySelectorAll('button.rbtn').forEach(function(b) {
    b.textContent = '▶ Answer';
    b.classList.remove('on');
  });
  var ra = document.getElementById('reflect-ans');
  if (ra) ra.style.display = 'none';
  var rb = document.querySelector('button.toggle-ans');
  if (rb) rb.textContent = '▶ Show Answers';
}
function clearAll() {
  document.querySelectorAll('input.f, input.f-heb').forEach(function(el) {
    el.value = '';
  });
}
function toggleReflect() {
  var block = document.getElementById('reflect-ans');
  var btn = document.querySelector('button.toggle-ans');
  if (block.style.display === 'block') {
    block.style.display = 'none';
    btn.textContent = '▶ Show Answers';
  } else {
    block.style.display = 'block';
    btn.textContent = '▼ Hide Answers';
  }
}
</script>

