# Parsing Drill

*Chapter 17 — Waw-Consecutive*

[Full screen](ch17-parsing-drill.html){.md-button}  [Markdown](ch17-parsing-drill.md){.md-button}  [Print (PDF)](ch17-parsing-drill.pdf){.md-button}

<style>

  body { font-family: Georgia, serif;    color: #222; line-height: 1.6; }
  h1 { font-size: 1.45rem; border-bottom: 2px solid #555; padding-bottom: .4rem; }
  h2 { font-size: 1.05rem; margin-top: 2rem; color: #333; border-bottom: 1px solid #ddd; padding-bottom: .2rem; }
  .subtitle { color: #666; font-style: italic; margin-top: -.4rem; }
  .instructions { background: #f8f8f0; border-left: 4px solid #bbb; padding: .75rem 1rem; margin: 1rem 0; font-size: .92rem; }
  .note-box { background: #fff8e8; border-left: 3px solid #d4a017; padding: .5rem .9rem; margin: .6rem 0; font-size: .88rem; }
  table { border-collapse: collapse; width: 100%; margin: .4rem 0; font-size: .9rem; }
  th { background: #e0e8f0; padding: .38rem .5rem; border: 1px solid #bbb; text-align: left; font-size: .83rem; }
  td { padding: .28rem .4rem; border: 1px solid #ddd; vertical-align: middle; }
  td.num { text-align: center; font-weight: bold; color: #666; width: 2rem; }
  td.heb { font-size: 1.12rem; direction: rtl; unicode-bidi: embed; font-weight: bold; width: 9rem; }
  input.f { width: 100%; box-sizing: border-box; border: 1px solid #bbb; border-radius: 3px; padding: .2rem .38rem; font-family: Georgia, serif; font-size: .86rem; background: #fafff8; }
  input.f:focus { outline: none; border-color: #5a9; box-shadow: 0 0 0 2px #c8ecd4; }
  .ans-row { display: none; background: #f0faf0; }
  .ans-row td { font-size: .86rem; color: #2a6e2a; padding: .25rem .4rem; }
  .ans-lbl { font-weight: bold; color: #1a5c1a; width: 2rem; text-align: center; }
  .ans-heb { font-size: 1rem; direction: rtl; unicode-bidi: embed; }
  button.rbtn { font-size: .75rem; padding: .13rem .46rem; cursor: pointer; background: #e8f4ec; border: 1px solid #7bba8f; border-radius: 3px; color: #2a6e2a; white-space: nowrap; }
  button.rbtn:hover, button.rbtn.on { background: #c8ecd4; }
  .controls { display: flex; gap: .7rem; flex-wrap: wrap; margin: 1rem 0 1.5rem; }
  .controls button { padding: .38rem .85rem; cursor: pointer; border-radius: 4px; font-size: .88rem; border: 1px solid #999; background: #f0f0f0; color: #333; }
  .controls button:hover { background: #ddd; }
  .clr { border-color: #c06060 !important; color: #8b0000 !important; background: #fff0f0 !important; }
  .clr:hover { background: #ffd8d8 !important; }
  hr.sec { border: none; border-top: 2px dashed #ccc; margin: 2rem 0; }
  @media print { .controls, button.rbtn { display: none; } input.f { border: none; border-bottom: 1px solid #aaa; border-radius: 0; background: transparent; } .ans-row { display: none !important; } }

</style>

<h1>Ch17 Parsing Drill — Wayyiqtol and Weqatal</h1>
<p class="subtitle">BBH Chapter 17 · 30 forms</p>

<div class="instructions">
  <strong>Instructions:</strong> For each form, give: (a) Form Type (Wayyiqtol / Weqatal / Imperfect / Perfect), (b) Person, (c) Number, (d) Gender, (e) Root (3ms lexical form).<br>
  <em>Part B: also identify the Weak Class. Part C: disambiguation — determine whether each form is Weqatal, Perfect, or Imperfect.</em>
</div>

<div class="controls">
  <button onclick="showAll()">Show All Answers</button>
  <button onclick="hideAll()">Hide All Answers</button>
  <button class="clr" onclick="clearAll()">Clear All Inputs</button>
</div>

<!-- PART A -->
<h2>Part A — Wayyiqtol: Strong and Common Weak Roots</h2>
<div class="note-box">All forms in Part A are Wayyiqtol. Parse the PGN and identify the root.</div>
<table>
  <tr><th>#</th><th>Form</th><th>Form Type</th><th>Pers.</th><th>Num.</th><th>Gen.</th><th>Root</th><th></th></tr>
  <tr>
    <td class="num">1</td><td class="heb">וַיֹּאמֶר</td>
    <td><input class="parse-field" id="1-ft" placeholder="type"></td><td><input class="parse-field" id="1-p" placeholder="1/2/3"></td><td><input class="parse-field" id="1-n" placeholder="s/p"></td><td><input class="parse-field" id="1-g" placeholder="m/f/c"></td><td><input class="parse-field" id="1-r" placeholder="root"></td>
    <td><button class="rbtn" onclick="tog(1)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-1"><td class="ans-lbl">✓</td><td class="ans-heb">וַיֹּאמֶר</td><td>Wayyiqtol</td><td>3</td><td>s</td><td>m</td><td class="ans-heb">אמר</td><td>Most frequent verb form in the OT; I-aleph holem prefix</td></tr>
  <tr>
    <td class="num">2</td><td class="heb">וַתֹּאמֶר</td>
    <td><input class="parse-field" id="2-ft" placeholder="type"></td><td><input class="parse-field" id="2-p" placeholder="1/2/3"></td><td><input class="parse-field" id="2-n" placeholder="s/p"></td><td><input class="parse-field" id="2-g" placeholder="m/f/c"></td><td><input class="parse-field" id="2-r" placeholder="root"></td>
    <td><button class="rbtn" onclick="tog(2)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-2"><td class="ans-lbl">✓</td><td class="ans-heb">וַתֹּאמֶר</td><td>Wayyiqtol</td><td>3</td><td>s</td><td>f</td><td class="ans-heb">אמר</td><td>3fs; תּ prefix with dagesh forte</td></tr>
  <tr>
    <td class="num">3</td><td class="heb">וַיֵּלֶךְ</td>
    <td><input class="parse-field" id="3-ft" placeholder="type"></td><td><input class="parse-field" id="3-p" placeholder="1/2/3"></td><td><input class="parse-field" id="3-n" placeholder="s/p"></td><td><input class="parse-field" id="3-g" placeholder="m/f/c"></td><td><input class="parse-field" id="3-r" placeholder="root"></td>
    <td><button class="rbtn" onclick="tog(3)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-3"><td class="ans-lbl">✓</td><td class="ans-heb">וַיֵּלֶךְ</td><td>Wayyiqtol</td><td>3</td><td>s</td><td>m</td><td class="ans-heb">הלך</td><td>I-י: tsere prefix; root ה absent; behaves as I-י</td></tr>
  <tr>
    <td class="num">4</td><td class="heb">וַיִּקְטֹל</td>
    <td><input class="parse-field" id="4-ft" placeholder="type"></td><td><input class="parse-field" id="4-p" placeholder="1/2/3"></td><td><input class="parse-field" id="4-n" placeholder="s/p"></td><td><input class="parse-field" id="4-g" placeholder="m/f/c"></td><td><input class="parse-field" id="4-r" placeholder="root"></td>
    <td><button class="rbtn" onclick="tog(4)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-4"><td class="ans-lbl">✓</td><td class="ans-heb">וַיִּקְטֹל</td><td>Wayyiqtol</td><td>3</td><td>s</td><td>m</td><td class="ans-heb">קטל</td><td>Strong paradigm model; dagesh forte in יּ</td></tr>
  <tr>
    <td class="num">5</td><td class="heb">וַיִּכְתְּבוּ</td>
    <td><input class="parse-field" id="5-ft" placeholder="type"></td><td><input class="parse-field" id="5-p" placeholder="1/2/3"></td><td><input class="parse-field" id="5-n" placeholder="s/p"></td><td><input class="parse-field" id="5-g" placeholder="m/f/c"></td><td><input class="parse-field" id="5-r" placeholder="root"></td>
    <td><button class="rbtn" onclick="tog(5)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-5"><td class="ans-lbl">✓</td><td class="ans-heb">וַיִּכְתְּבוּ</td><td>Wayyiqtol</td><td>3</td><td>p</td><td>m</td><td class="ans-heb">כתב</td><td>3mp; dagesh in יּ; shureq suffix</td></tr>
  <tr>
    <td class="num">6</td><td class="heb">וַתִּשְׁמֹרְנָה</td>
    <td><input class="parse-field" id="6-ft" placeholder="type"></td><td><input class="parse-field" id="6-p" placeholder="1/2/3"></td><td><input class="parse-field" id="6-n" placeholder="s/p"></td><td><input class="parse-field" id="6-g" placeholder="m/f/c"></td><td><input class="parse-field" id="6-r" placeholder="root"></td>
    <td><button class="rbtn" onclick="tog(6)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-6"><td class="ans-lbl">✓</td><td class="ans-heb">וַתִּשְׁמֹרְנָה</td><td>Wayyiqtol</td><td>3/2</td><td>p</td><td>f</td><td class="ans-heb">שמר</td><td>נָה suffix marks 3/2fp</td></tr>
  <tr>
    <td class="num">7</td><td class="heb">וָאֶקְטֹל</td>
    <td><input class="parse-field" id="7-ft" placeholder="type"></td><td><input class="parse-field" id="7-p" placeholder="1/2/3"></td><td><input class="parse-field" id="7-n" placeholder="s/p"></td><td><input class="parse-field" id="7-g" placeholder="m/f/c"></td><td><input class="parse-field" id="7-r" placeholder="root"></td>
    <td><button class="rbtn" onclick="tog(7)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-7"><td class="ans-lbl">✓</td><td class="ans-heb">וָאֶקְטֹל</td><td>Wayyiqtol</td><td>1</td><td>s</td><td>c</td><td class="ans-heb">קטל</td><td>1cs: waw → וָ (qamets) before aleph; aleph cannot take dagesh</td></tr>
  <tr>
    <td class="num">8</td><td class="heb">וַנִּקְטֹל</td>
    <td><input class="parse-field" id="8-ft" placeholder="type"></td><td><input class="parse-field" id="8-p" placeholder="1/2/3"></td><td><input class="parse-field" id="8-n" placeholder="s/p"></td><td><input class="parse-field" id="8-g" placeholder="m/f/c"></td><td><input class="parse-field" id="8-r" placeholder="root"></td>
    <td><button class="rbtn" onclick="tog(8)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-8"><td class="ans-lbl">✓</td><td class="ans-heb">וַנִּקְטֹל</td><td>Wayyiqtol</td><td>1</td><td>p</td><td>c</td><td class="ans-heb">קטל</td><td>1cp; nun prefix with dagesh forte in נּ</td></tr>
  <tr>
    <td class="num">9</td><td class="heb">וַיִּתֵּן</td>
    <td><input class="parse-field" id="9-ft" placeholder="type"></td><td><input class="parse-field" id="9-p" placeholder="1/2/3"></td><td><input class="parse-field" id="9-n" placeholder="s/p"></td><td><input class="parse-field" id="9-g" placeholder="m/f/c"></td><td><input class="parse-field" id="9-r" placeholder="root"></td>
    <td><button class="rbtn" onclick="tog(9)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-9"><td class="ans-lbl">✓</td><td class="ans-heb">וַיִּתֵּן</td><td>Wayyiqtol</td><td>3</td><td>s</td><td>m</td><td class="ans-heb">נתן</td><td>I-נ: nun assimilated; dagesh forte in תּ; tsere</td></tr>
  <tr>
    <td class="num">10</td><td class="heb">וַיָּבֹא</td>
    <td><input class="parse-field" id="10-ft" placeholder="type"></td><td><input class="parse-field" id="10-p" placeholder="1/2/3"></td><td><input class="parse-field" id="10-n" placeholder="s/p"></td><td><input class="parse-field" id="10-g" placeholder="m/f/c"></td><td><input class="parse-field" id="10-r" placeholder="root"></td>
    <td><button class="rbtn" onclick="tog(10)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-10"><td class="ans-lbl">✓</td><td class="ans-heb">וַיָּבֹא</td><td>Wayyiqtol</td><td>3</td><td>s</td><td>m</td><td class="ans-heb">בוא</td><td>Biconsonantal; qamets prefix; short form</td></tr>
</table>

<hr class="sec">

<!-- PART B -->
<h2>Part B — Wayyiqtol with Weak Roots: III-ה, Biconsonantal, I-י</h2>
<table>
  <tr><th>#</th><th>Form</th><th>Form Type</th><th>Pers.</th><th>Num.</th><th>Gen.</th><th>Root</th><th>Weak Class</th><th></th></tr>
  <tr>
    <td class="num">11</td><td class="heb">וַיַּרְא</td>
    <td><input class="parse-field" id="11-ft" placeholder="type"></td><td><input class="parse-field" id="11-p" placeholder="1/2/3"></td><td><input class="parse-field" id="11-n" placeholder="s/p"></td><td><input class="parse-field" id="11-g" placeholder="m/f/c"></td><td><input class="parse-field" id="11-r" placeholder="root"></td><td><input class="parse-field" id="11-wc" placeholder="class"></td>
    <td><button class="rbtn" onclick="tog(11)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-11"><td class="ans-lbl">✓</td><td class="ans-heb">וַיַּרְא</td><td>Wayyiqtol</td><td>3</td><td>s</td><td>m</td><td class="ans-heb">ראה</td><td>III-ה</td><td>Short form: ה dropped; "and he/God saw"</td></tr>
  <tr>
    <td class="num">12</td><td class="heb">וַיְהִי</td>
    <td><input class="parse-field" id="12-ft" placeholder="type"></td><td><input class="parse-field" id="12-p" placeholder="1/2/3"></td><td><input class="parse-field" id="12-n" placeholder="s/p"></td><td><input class="parse-field" id="12-g" placeholder="m/f/c"></td><td><input class="parse-field" id="12-r" placeholder="root"></td><td><input class="parse-field" id="12-wc" placeholder="class"></td>
    <td><button class="rbtn" onclick="tog(12)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-12"><td class="ans-lbl">✓</td><td class="ans-heb">וַיְהִי</td><td>Wayyiqtol</td><td>3</td><td>s</td><td>m</td><td class="ans-heb">היה</td><td>III-ה</td><td>Short jussive of היה; hireq-yod ending; narrative episode opener</td></tr>
  <tr>
    <td class="num">13</td><td class="heb">וַיַּעַשׂ</td>
    <td><input class="parse-field" id="13-ft" placeholder="type"></td><td><input class="parse-field" id="13-p" placeholder="1/2/3"></td><td><input class="parse-field" id="13-n" placeholder="s/p"></td><td><input class="parse-field" id="13-g" placeholder="m/f/c"></td><td><input class="parse-field" id="13-r" placeholder="root"></td><td><input class="parse-field" id="13-wc" placeholder="class"></td>
    <td><button class="rbtn" onclick="tog(13)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-13"><td class="ans-lbl">✓</td><td class="ans-heb">וַיַּעַשׂ</td><td>Wayyiqtol</td><td>3</td><td>s</td><td>m</td><td class="ans-heb">עשה</td><td>III-ה + I-gutt.</td><td>Short form; patach prefix (ע causes chateph); ה dropped</td></tr>
  <tr>
    <td class="num">14</td><td class="heb">וַיָּקׇם</td>
    <td><input class="parse-field" id="14-ft" placeholder="type"></td><td><input class="parse-field" id="14-p" placeholder="1/2/3"></td><td><input class="parse-field" id="14-n" placeholder="s/p"></td><td><input class="parse-field" id="14-g" placeholder="m/f/c"></td><td><input class="parse-field" id="14-r" placeholder="root"></td><td><input class="parse-field" id="14-wc" placeholder="class"></td>
    <td><button class="rbtn" onclick="tog(14)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-14"><td class="ans-lbl">✓</td><td class="ans-heb">וַיָּקׇם</td><td>Wayyiqtol</td><td>3</td><td>s</td><td>m</td><td class="ans-heb">קום</td><td>Biconsonantal</td><td>Short form: qamets hatuf in root vs. שּׁוּרֶק in imperfect יָקוּם</td></tr>
  <tr>
    <td class="num">15</td><td class="heb">וַיָּבֹאוּ</td>
    <td><input class="parse-field" id="15-ft" placeholder="type"></td><td><input class="parse-field" id="15-p" placeholder="1/2/3"></td><td><input class="parse-field" id="15-n" placeholder="s/p"></td><td><input class="parse-field" id="15-g" placeholder="m/f/c"></td><td><input class="parse-field" id="15-r" placeholder="root"></td><td><input class="parse-field" id="15-wc" placeholder="class"></td>
    <td><button class="rbtn" onclick="tog(15)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-15"><td class="ans-lbl">✓</td><td class="ans-heb">וַיָּבֹאוּ</td><td>Wayyiqtol</td><td>3</td><td>p</td><td>m</td><td class="ans-heb">בוא</td><td>Biconsonantal</td><td>3mp; qamets prefix + -וּ suffix</td></tr>
  <tr>
    <td class="num">16</td><td class="heb">וַיָּסׇּב</td>
    <td><input class="parse-field" id="16-ft" placeholder="type"></td><td><input class="parse-field" id="16-p" placeholder="1/2/3"></td><td><input class="parse-field" id="16-n" placeholder="s/p"></td><td><input class="parse-field" id="16-g" placeholder="m/f/c"></td><td><input class="parse-field" id="16-r" placeholder="root"></td><td><input class="parse-field" id="16-wc" placeholder="class"></td>
    <td><button class="rbtn" onclick="tog(16)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-16"><td class="ans-lbl">✓</td><td class="ans-heb">וַיָּסׇּב</td><td>Wayyiqtol</td><td>3</td><td>s</td><td>m</td><td class="ans-heb">סבב</td><td>Geminate</td><td>Qamets prefix + dagesh forte in ב (R2=R3)</td></tr>
  <tr>
    <td class="num">17</td><td class="heb">וַיֵּדַע</td>
    <td><input class="parse-field" id="17-ft" placeholder="type"></td><td><input class="parse-field" id="17-p" placeholder="1/2/3"></td><td><input class="parse-field" id="17-n" placeholder="s/p"></td><td><input class="parse-field" id="17-g" placeholder="m/f/c"></td><td><input class="parse-field" id="17-r" placeholder="root"></td><td><input class="parse-field" id="17-wc" placeholder="class"></td>
    <td><button class="rbtn" onclick="tog(17)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-17"><td class="ans-lbl">✓</td><td class="ans-heb">וַיֵּדַע</td><td>Wayyiqtol</td><td>3</td><td>s</td><td>m</td><td class="ans-heb">ידע</td><td>I-י</td><td>Tsere prefix (יֵ–); yod at R1 contracted</td></tr>
  <tr>
    <td class="num">18</td><td class="heb">וַיֵּצֵא</td>
    <td><input class="parse-field" id="18-ft" placeholder="type"></td><td><input class="parse-field" id="18-p" placeholder="1/2/3"></td><td><input class="parse-field" id="18-n" placeholder="s/p"></td><td><input class="parse-field" id="18-g" placeholder="m/f/c"></td><td><input class="parse-field" id="18-r" placeholder="root"></td><td><input class="parse-field" id="18-wc" placeholder="class"></td>
    <td><button class="rbtn" onclick="tog(18)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-18"><td class="ans-lbl">✓</td><td class="ans-heb">וַיֵּצֵא</td><td>Wayyiqtol</td><td>3</td><td>s</td><td>m</td><td class="ans-heb">יצא</td><td>I-י + III-א</td><td>Tsere prefix; aleph quiesces at R3; compound weak class</td></tr>
  <tr>
    <td class="num">19</td><td class="heb">וַיִּבֶן</td>
    <td><input class="parse-field" id="19-ft" placeholder="type"></td><td><input class="parse-field" id="19-p" placeholder="1/2/3"></td><td><input class="parse-field" id="19-n" placeholder="s/p"></td><td><input class="parse-field" id="19-g" placeholder="m/f/c"></td><td><input class="parse-field" id="19-r" placeholder="root"></td><td><input class="parse-field" id="19-wc" placeholder="class"></td>
    <td><button class="rbtn" onclick="tog(19)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-19"><td class="ans-lbl">✓</td><td class="ans-heb">וַיִּבֶן</td><td>Wayyiqtol</td><td>3</td><td>s</td><td>m</td><td class="ans-heb">בנה</td><td>III-ה</td><td>Short form: ה dropped; dagesh in נּ; seghol under נ</td></tr>
  <tr>
    <td class="num">20</td><td class="heb">וַיָּשׇׁב</td>
    <td><input class="parse-field" id="20-ft" placeholder="type"></td><td><input class="parse-field" id="20-p" placeholder="1/2/3"></td><td><input class="parse-field" id="20-n" placeholder="s/p"></td><td><input class="parse-field" id="20-g" placeholder="m/f/c"></td><td><input class="parse-field" id="20-r" placeholder="root"></td><td><input class="parse-field" id="20-wc" placeholder="class"></td>
    <td><button class="rbtn" onclick="tog(20)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-20"><td class="ans-lbl">✓</td><td class="ans-heb">וַיָּשׇׁב</td><td>Wayyiqtol</td><td>3</td><td>s</td><td>m</td><td class="ans-heb">שוב</td><td>Biconsonantal</td><td>Short form; qamets prefix + qamets hatuf in root</td></tr>
</table>

<hr class="sec">

<!-- PART C -->
<h2>Part C — Weqatal and Disambiguation</h2>
<div class="note-box">Identify whether each form is <strong>Wayyiqtol</strong>, <strong>Weqatal</strong>, <strong>Perfect</strong>, or <strong>Imperfect</strong>, then parse completely.</div>
<table>
  <tr><th>#</th><th>Form</th><th>Form Type</th><th>Pers.</th><th>Num.</th><th>Gen.</th><th>Root</th><th></th></tr>
  <tr>
    <td class="num">21</td><td class="heb">וְשָׁמַרְתָּ</td>
    <td><input class="parse-field" id="21-ft" placeholder="type"></td><td><input class="parse-field" id="21-p" placeholder="1/2/3"></td><td><input class="parse-field" id="21-n" placeholder="s/p"></td><td><input class="parse-field" id="21-g" placeholder="m/f/c"></td><td><input class="parse-field" id="21-r" placeholder="root"></td>
    <td><button class="rbtn" onclick="tog(21)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-21"><td class="ans-lbl">✓</td><td class="ans-heb">וְשָׁמַרְתָּ</td><td>Weqatal</td><td>2</td><td>s</td><td>m</td><td class="ans-heb">שמר</td><td>Follows imperfect/command; stress on -tā; future chain</td></tr>
  <tr>
    <td class="num">22</td><td class="heb">וְאָהַבְתָּ</td>
    <td><input class="parse-field" id="22-ft" placeholder="type"></td><td><input class="parse-field" id="22-p" placeholder="1/2/3"></td><td><input class="parse-field" id="22-n" placeholder="s/p"></td><td><input class="parse-field" id="22-g" placeholder="m/f/c"></td><td><input class="parse-field" id="22-r" placeholder="root"></td>
    <td><button class="rbtn" onclick="tog(22)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-22"><td class="ans-lbl">✓</td><td class="ans-heb">וְאָהַבְתָּ</td><td>Weqatal</td><td>2</td><td>s</td><td>m</td><td class="ans-heb">אהב</td><td>Deu 6:5; follows שְׁמַע (imperative); classic weqatal command chain</td></tr>
  <tr>
    <td class="num">23</td><td class="heb">שָׁמַרְתָּ</td>
    <td><input class="parse-field" id="23-ft" placeholder="type"></td><td><input class="parse-field" id="23-p" placeholder="1/2/3"></td><td><input class="parse-field" id="23-n" placeholder="s/p"></td><td><input class="parse-field" id="23-g" placeholder="m/f/c"></td><td><input class="parse-field" id="23-r" placeholder="root"></td>
    <td><button class="rbtn" onclick="tog(23)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-23"><td class="ans-lbl">✓</td><td class="ans-heb">שָׁמַרְתָּ</td><td>Perfect</td><td>2</td><td>s</td><td>m</td><td class="ans-heb">שמר</td><td>No waw; completed past action; penultimate stress</td></tr>
  <tr>
    <td class="num">24</td><td class="heb">וּשְׁמַרְתֶּם</td>
    <td><input class="parse-field" id="24-ft" placeholder="type"></td><td><input class="parse-field" id="24-p" placeholder="1/2/3"></td><td><input class="parse-field" id="24-n" placeholder="s/p"></td><td><input class="parse-field" id="24-g" placeholder="m/f/c"></td><td><input class="parse-field" id="24-r" placeholder="root"></td>
    <td><button class="rbtn" onclick="tog(24)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-24"><td class="ans-lbl">✓</td><td class="ans-heb">וּשְׁמַרְתֶּם</td><td>Weqatal</td><td>2</td><td>p</td><td>m</td><td class="ans-heb">שמר</td><td>Waw → וּ before shewa; 2mp; future chain</td></tr>
  <tr>
    <td class="num">25</td><td class="heb">וְנָתַתָּ</td>
    <td><input class="parse-field" id="25-ft" placeholder="type"></td><td><input class="parse-field" id="25-p" placeholder="1/2/3"></td><td><input class="parse-field" id="25-n" placeholder="s/p"></td><td><input class="parse-field" id="25-g" placeholder="m/f/c"></td><td><input class="parse-field" id="25-r" placeholder="root"></td>
    <td><button class="rbtn" onclick="tog(25)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-25"><td class="ans-lbl">✓</td><td class="ans-heb">וְנָתַתָּ</td><td>Weqatal</td><td>2</td><td>s</td><td>m</td><td class="ans-heb">נתן</td><td>I-נ regular in perfect/weqatal; legal/instructional context</td></tr>
  <tr>
    <td class="num">26</td><td class="heb">יִשְׁמֹר</td>
    <td><input class="parse-field" id="26-ft" placeholder="type"></td><td><input class="parse-field" id="26-p" placeholder="1/2/3"></td><td><input class="parse-field" id="26-n" placeholder="s/p"></td><td><input class="parse-field" id="26-g" placeholder="m/f/c"></td><td><input class="parse-field" id="26-r" placeholder="root"></td>
    <td><button class="rbtn" onclick="tog(26)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-26"><td class="ans-lbl">✓</td><td class="ans-heb">יִשְׁמֹר</td><td>Imperfect</td><td>3</td><td>s</td><td>m</td><td class="ans-heb">שמר</td><td>No waw; simple imperfect (future/habitual) or Jussive</td></tr>
  <tr>
    <td class="num">27</td><td class="heb">וְשָׁמְרוּ</td>
    <td><input class="parse-field" id="27-ft" placeholder="type"></td><td><input class="parse-field" id="27-n" placeholder="s/p"></td><td><input class="parse-field" id="27-n2" placeholder="s/p" style="display:none"></td><td><input class="parse-field" id="27-g" placeholder="m/f/c"></td><td><input class="parse-field" id="27-r" placeholder="root"></td>
    <td><button class="rbtn" onclick="tog(27)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-27"><td class="ans-lbl">✓</td><td class="ans-heb">וְשָׁמְרוּ</td><td>Weqatal</td><td>3</td><td>p</td><td>c</td><td class="ans-heb">שמר</td><td>3cp perfect form + וְ; future-chain or commanded result</td></tr>
  <tr>
    <td class="num">28</td><td class="heb">שָׁמְרוּ</td>
    <td><input class="parse-field" id="28-ft" placeholder="type"></td><td><input class="parse-field" id="28-p" placeholder="1/2/3"></td><td><input class="parse-field" id="28-n" placeholder="s/p"></td><td><input class="parse-field" id="28-g" placeholder="m/f/c"></td><td><input class="parse-field" id="28-r" placeholder="root"></td>
    <td><button class="rbtn" onclick="tog(28)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-28"><td class="ans-lbl">✓</td><td class="ans-heb">שָׁמְרוּ</td><td>Perfect</td><td>3</td><td>p</td><td>c</td><td class="ans-heb">שמר</td><td>No waw; completed past action (3cp)</td></tr>
  <tr>
    <td class="num">29</td><td class="heb">וְעָשִׂיתָ</td>
    <td><input class="parse-field" id="29-ft" placeholder="type"></td><td><input class="parse-field" id="29-p" placeholder="1/2/3"></td><td><input class="parse-field" id="29-n" placeholder="s/p"></td><td><input class="parse-field" id="29-g" placeholder="m/f/c"></td><td><input class="parse-field" id="29-r" placeholder="root"></td>
    <td><button class="rbtn" onclick="tog(29)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-29"><td class="ans-lbl">✓</td><td class="ans-heb">וְעָשִׂיתָ</td><td>Weqatal</td><td>2</td><td>s</td><td>m</td><td class="ans-heb">עשה</td><td>III-ה perfect 2ms + וְ; hireq-yod before suffix</td></tr>
  <tr>
    <td class="num">30</td><td class="heb">וָאֹמַר</td>
    <td><input class="parse-field" id="30-ft" placeholder="type"></td><td><input class="parse-field" id="30-p" placeholder="1/2/3"></td><td><input class="parse-field" id="30-n" placeholder="s/p"></td><td><input class="parse-field" id="30-g" placeholder="m/f/c"></td><td><input class="parse-field" id="30-r" placeholder="root"></td>
    <td><button class="rbtn" onclick="tog(30)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-30"><td class="ans-lbl">✓</td><td class="ans-heb">וָאֹמַר</td><td>Wayyiqtol</td><td>1</td><td>s</td><td>c</td><td class="ans-heb">אמר</td><td>1cs; holem prefix of אמר; waw → וָ (qamets) before aleph</td></tr>
</table>

<script>
  const ids = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30];
  function tog(id) { const r=document.getElementById('ans-'+id); const b=r.previousElementSibling.querySelector('button'); const v=r.style.display==='table-row'; r.style.display=v?'none':'table-row'; b.textContent=v?'▶ Answer':'▼ Hide'; b.classList.toggle('on',!v); }
  function showAll() { ids.forEach(id=>{const r=document.getElementById('ans-'+id);const b=r.previousElementSibling.querySelector('button');r.style.display='table-row';b.textContent='▼ Hide';b.classList.add('on');}); }
  function hideAll() { ids.forEach(id=>{const r=document.getElementById('ans-'+id);const b=r.previousElementSibling.querySelector('button');r.style.display='none';b.textContent='▶ Answer';b.classList.remove('on');}); }
  function clearAll() { document.querySelectorAll('input.f').forEach(e=>e.value=''); }
</script>

