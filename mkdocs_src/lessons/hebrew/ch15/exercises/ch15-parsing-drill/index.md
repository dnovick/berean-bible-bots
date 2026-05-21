# Parsing Drill

*Chapter 15 — Qal Imperfect Strong Verbs*

[Full screen](ch15-parsing-drill.html){.md-button}  [Markdown](ch15-parsing-drill.md){.md-button}  [Print (PDF)](ch15-parsing-drill.pdf){.md-button}

<style>

  body { font-family: Georgia, serif;    color: #222; line-height: 1.6; }
  h1 { font-size: 1.45rem; border-bottom: 2px solid #555; padding-bottom: .4rem; }
  h2 { font-size: 1.05rem; margin-top: 2rem; color: #333; border-bottom: 1px solid #ddd; padding-bottom: .2rem; }
  .subtitle { color: #666; font-style: italic; margin-top: -.4rem; }
  .instructions { background: #f8f8f0; border-left: 4px solid #bbb; padding: .75rem 1rem; margin: 1rem 0; font-size: .92rem; }
  .note-box { background: #fff8e8; border-left: 3px solid #d4a017; padding: .5rem .9rem; margin: .6rem 0; font-size: .88rem; }
  table { border-collapse: collapse; width: 100%; margin: .4rem 0; font-size: .91rem; }
  th { background: #e0e8f0; padding: .38rem .5rem; border: 1px solid #bbb; text-align: left; font-size: .83rem; }
  td { padding: .28rem .4rem; border: 1px solid #ddd; vertical-align: middle; }
  td.num { text-align: center; font-weight: bold; color: #666; width: 2rem; }
  td.heb { font-size: 1.12rem; direction: rtl; unicode-bidi: embed; font-weight: bold; width: 8.5rem; }
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
  select.parse-field { font-size: .9em; padding: 2px 4px; border: 1px solid #aaa; border-radius: 3px; min-width: 80px; }

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

<h1>Ch15 Parsing Drill — Qal Imperfect Strong Verbs</h1>
<p class="subtitle">BBH Chapter 15 · 25 forms</p>
<div class="instructions">
<strong>Instructions:</strong> For each form, give: (a) Person, (b) Number, (c) Gender, (d) Root (3ms lexical form).<br/>
<em>Part C only: also identify whether the form is a Jussive or Cohortative.</em>
</div>
<div class="controls">
<button onclick="showAll()">Show All Answers</button>
<button onclick="hideAll()">Hide All Answers</button>
<button class="clr" onclick="clearAll()">Clear All Inputs</button>
</div>
<!-- PART A -->
<h2>Part A — A-Class (Holem): Clear Prefix Pattern</h2>
<table>
<tr><th>#</th><th>Form</th><th>Person</th><th>Number</th><th>Gender</th><th>Root</th><th></th></tr>
<tr>
<td class="num">1</td><td class="heb">יִשְׁמֹר</td>
<td><select class="parse-field" id="1-p"><option value="">—</option><option value="1">1</option><option value="2">2</option><option value="3">3</option></select></td><td><select class="parse-field" id="1-n"><option value="">—</option><option value="s">s</option><option value="p">p</option><option value="du">du</option></select></td><td><select class="parse-field" id="1-g"><option value="">—</option><option value="m">m</option><option value="f">f</option><option value="c">c</option></select></td><td><input class="parse-field" id="1-r" placeholder="root"/></td>
<td><button class="rbtn" onclick="tog(1)">▶ Answer</button></td>
</tr>
<tr class="ans-row" id="ans-1"><td class="ans-lbl">✓</td><td class="ans-heb">יִשְׁמֹר</td><td>3</td><td>s</td><td>m</td><td class="ans-heb">שמר</td><td></td></tr>
<tr>
<td class="num">2</td><td class="heb">תִּכְתְּבוּ</td>
<td><select class="parse-field" id="2-p"><option value="">—</option><option value="1">1</option><option value="2">2</option><option value="3">3</option></select></td><td><select class="parse-field" id="2-n"><option value="">—</option><option value="s">s</option><option value="p">p</option><option value="du">du</option></select></td><td><select class="parse-field" id="2-g"><option value="">—</option><option value="m">m</option><option value="f">f</option><option value="c">c</option></select></td><td><input class="parse-field" id="2-r" placeholder="root"/></td>
<td><button class="rbtn" onclick="tog(2)">▶ Answer</button></td>
</tr>
<tr class="ans-row" id="ans-2"><td class="ans-lbl">✓</td><td class="ans-heb">תִּכְתְּבוּ</td><td>2</td><td>p</td><td>m</td><td class="ans-heb">כתב</td><td></td></tr>
<tr>
<td class="num">3</td><td class="heb">נִפְקֹד</td>
<td><select class="parse-field" id="3-p"><option value="">—</option><option value="1">1</option><option value="2">2</option><option value="3">3</option></select></td><td><select class="parse-field" id="3-n"><option value="">—</option><option value="s">s</option><option value="p">p</option><option value="du">du</option></select></td><td><select class="parse-field" id="3-g"><option value="">—</option><option value="m">m</option><option value="f">f</option><option value="c">c</option></select></td><td><input class="parse-field" id="3-r" placeholder="root"/></td>
<td><button class="rbtn" onclick="tog(3)">▶ Answer</button></td>
</tr>
<tr class="ans-row" id="ans-3"><td class="ans-lbl">✓</td><td class="ans-heb">נִפְקֹד</td><td>1</td><td>p</td><td>c</td><td class="ans-heb">פקד</td><td></td></tr>
<tr>
<td class="num">4</td><td class="heb">תִּלְמְדִי</td>
<td><select class="parse-field" id="4-p"><option value="">—</option><option value="1">1</option><option value="2">2</option><option value="3">3</option></select></td><td><select class="parse-field" id="4-n"><option value="">—</option><option value="s">s</option><option value="p">p</option><option value="du">du</option></select></td><td><select class="parse-field" id="4-g"><option value="">—</option><option value="m">m</option><option value="f">f</option><option value="c">c</option></select></td><td><input class="parse-field" id="4-r" placeholder="root"/></td>
<td><button class="rbtn" onclick="tog(4)">▶ Answer</button></td>
</tr>
<tr class="ans-row" id="ans-4"><td class="ans-lbl">✓</td><td class="ans-heb">תִּלְמְדִי</td><td>2</td><td>s</td><td>f</td><td class="ans-heb">למד</td><td></td></tr>
<tr>
<td class="num">5</td><td class="heb">יִזְכְּרוּ</td>
<td><select class="parse-field" id="5-p"><option value="">—</option><option value="1">1</option><option value="2">2</option><option value="3">3</option></select></td><td><select class="parse-field" id="5-n"><option value="">—</option><option value="s">s</option><option value="p">p</option><option value="du">du</option></select></td><td><select class="parse-field" id="5-g"><option value="">—</option><option value="m">m</option><option value="f">f</option><option value="c">c</option></select></td><td><input class="parse-field" id="5-r" placeholder="root"/></td>
<td><button class="rbtn" onclick="tog(5)">▶ Answer</button></td>
</tr>
<tr class="ans-row" id="ans-5"><td class="ans-lbl">✓</td><td class="ans-heb">יִזְכְּרוּ</td><td>3</td><td>p</td><td>m</td><td class="ans-heb">זכר</td><td></td></tr>
<tr>
<td class="num">6</td><td class="heb">אֶשְׁמֹר</td>
<td><select class="parse-field" id="6-p"><option value="">—</option><option value="1">1</option><option value="2">2</option><option value="3">3</option></select></td><td><select class="parse-field" id="6-n"><option value="">—</option><option value="s">s</option><option value="p">p</option><option value="du">du</option></select></td><td><select class="parse-field" id="6-g"><option value="">—</option><option value="m">m</option><option value="f">f</option><option value="c">c</option></select></td><td><input class="parse-field" id="6-r" placeholder="root"/></td>
<td><button class="rbtn" onclick="tog(6)">▶ Answer</button></td>
</tr>
<tr class="ans-row" id="ans-6"><td class="ans-lbl">✓</td><td class="ans-heb">אֶשְׁמֹר</td><td>1</td><td>s</td><td>c</td><td class="ans-heb">שמר</td><td></td></tr>
<tr>
<td class="num">7</td><td class="heb">תִּמְשֹׁל</td>
<td><select class="parse-field" id="7-p"><option value="">—</option><option value="1">1</option><option value="2">2</option><option value="3">3</option></select></td><td><select class="parse-field" id="7-n"><option value="">—</option><option value="s">s</option><option value="p">p</option><option value="du">du</option></select></td><td><select class="parse-field" id="7-g"><option value="">—</option><option value="m">m</option><option value="f">f</option><option value="c">c</option></select></td><td><input class="parse-field" id="7-r" placeholder="root"/></td>
<td><button class="rbtn" onclick="tog(7)">▶ Answer</button></td>
</tr>
<tr class="ans-row" id="ans-7"><td class="ans-lbl">✓</td><td class="ans-heb">תִּמְשֹׁל</td><td>3/2</td><td>s</td><td>f/m</td><td class="ans-heb">משל</td><td>Ambiguous: 3fs or 2ms</td></tr>
<tr>
<td class="num">8</td><td class="heb">יִכְתְּבוּ</td>
<td><select class="parse-field" id="8-p"><option value="">—</option><option value="1">1</option><option value="2">2</option><option value="3">3</option></select></td><td><select class="parse-field" id="8-n"><option value="">—</option><option value="s">s</option><option value="p">p</option><option value="du">du</option></select></td><td><select class="parse-field" id="8-g"><option value="">—</option><option value="m">m</option><option value="f">f</option><option value="c">c</option></select></td><td><input class="parse-field" id="8-r" placeholder="root"/></td>
<td><button class="rbtn" onclick="tog(8)">▶ Answer</button></td>
</tr>
<tr class="ans-row" id="ans-8"><td class="ans-lbl">✓</td><td class="ans-heb">יִכְתְּבוּ</td><td>3</td><td>p</td><td>m</td><td class="ans-heb">כתב</td><td></td></tr>
<tr>
<td class="num">9</td><td class="heb">תִּשְׁמֹרְנָה</td>
<td><select class="parse-field" id="9-p"><option value="">—</option><option value="1">1</option><option value="2">2</option><option value="3">3</option></select></td><td><select class="parse-field" id="9-n"><option value="">—</option><option value="s">s</option><option value="p">p</option><option value="du">du</option></select></td><td><select class="parse-field" id="9-g"><option value="">—</option><option value="m">m</option><option value="f">f</option><option value="c">c</option></select></td><td><input class="parse-field" id="9-r" placeholder="root"/></td>
<td><button class="rbtn" onclick="tog(9)">▶ Answer</button></td>
</tr>
<tr class="ans-row" id="ans-9"><td class="ans-lbl">✓</td><td class="ans-heb">תִּשְׁמֹרְנָה</td><td>3/2</td><td>p</td><td>f</td><td class="ans-heb">שמר</td><td>נָה- suffix marks 3/2fp</td></tr>
<tr>
<td class="num">10</td><td class="heb">אֶבְחַר</td>
<td><select class="parse-field" id="10-p"><option value="">—</option><option value="1">1</option><option value="2">2</option><option value="3">3</option></select></td><td><select class="parse-field" id="10-n"><option value="">—</option><option value="s">s</option><option value="p">p</option><option value="du">du</option></select></td><td><select class="parse-field" id="10-g"><option value="">—</option><option value="m">m</option><option value="f">f</option><option value="c">c</option></select></td><td><input class="parse-field" id="10-r" placeholder="root"/></td>
<td><button class="rbtn" onclick="tog(10)">▶ Answer</button></td>
</tr>
<tr class="ans-row" id="ans-10"><td class="ans-lbl">✓</td><td class="ans-heb">אֶבְחַר</td><td>1</td><td>s</td><td>c</td><td class="ans-heb">בחר</td><td>B-class patach under R2</td></tr>
</table>
<hr class="sec"/>
<!-- PART B -->
<h2>Part B — B-Class (Patach) and Disambiguation</h2>
<table>
<tr><th>#</th><th>Form</th><th>Person</th><th>Number</th><th>Gender</th><th>Root</th><th>Notes</th><th></th></tr>
<tr>
<td class="num">11</td><td class="heb">יִשְׁמַע</td>
<td><select class="parse-field" id="11-p"><option value="">—</option><option value="1">1</option><option value="2">2</option><option value="3">3</option></select></td><td><select class="parse-field" id="11-n"><option value="">—</option><option value="s">s</option><option value="p">p</option><option value="du">du</option></select></td><td><select class="parse-field" id="11-g"><option value="">—</option><option value="m">m</option><option value="f">f</option><option value="c">c</option></select></td><td><input class="parse-field" id="11-r" placeholder="root"/></td><td></td>
<td><button class="rbtn" onclick="tog(11)">▶ Answer</button></td>
</tr>
<tr class="ans-row" id="ans-11"><td class="ans-lbl">✓</td><td class="ans-heb">יִשְׁמַע</td><td>3</td><td>s</td><td>m</td><td class="ans-heb">שמע</td><td colspan="2">B-class patach under R2</td></tr>
<tr>
<td class="num">12</td><td class="heb">תִּשְׁמַע</td>
<td><select class="parse-field" id="12-p"><option value="">—</option><option value="1">1</option><option value="2">2</option><option value="3">3</option></select></td><td><select class="parse-field" id="12-n"><option value="">—</option><option value="s">s</option><option value="p">p</option><option value="du">du</option></select></td><td><select class="parse-field" id="12-g"><option value="">—</option><option value="m">m</option><option value="f">f</option><option value="c">c</option></select></td><td><input class="parse-field" id="12-r" placeholder="root"/></td><td style="font-size:.82rem;color:#888"><em>3fs or 2ms?</em></td>
<td><button class="rbtn" onclick="tog(12)">▶ Answer</button></td>
</tr>
<tr class="ans-row" id="ans-12"><td class="ans-lbl">✓</td><td class="ans-heb">תִּשְׁמַע</td><td>3/2</td><td>s</td><td>f/m</td><td class="ans-heb">שמע</td><td colspan="2">Ambiguous: 3fs or 2ms — context required</td></tr>
<tr>
<td class="num">13</td><td class="heb">תִּשְׁמְעִי</td>
<td><select class="parse-field" id="13-p"><option value="">—</option><option value="1">1</option><option value="2">2</option><option value="3">3</option></select></td><td><select class="parse-field" id="13-n"><option value="">—</option><option value="s">s</option><option value="p">p</option><option value="du">du</option></select></td><td><select class="parse-field" id="13-g"><option value="">—</option><option value="m">m</option><option value="f">f</option><option value="c">c</option></select></td><td><input class="parse-field" id="13-r" placeholder="root"/></td><td></td>
<td><button class="rbtn" onclick="tog(13)">▶ Answer</button></td>
</tr>
<tr class="ans-row" id="ans-13"><td class="ans-lbl">✓</td><td class="ans-heb">תִּשְׁמְעִי</td><td>2</td><td>s</td><td>f</td><td class="ans-heb">שמע</td><td colspan="2">Hireq-yod suffix disambiguates 2fs</td></tr>
<tr>
<td class="num">14</td><td class="heb">יִכְבַּד</td>
<td><select class="parse-field" id="14-p"><option value="">—</option><option value="1">1</option><option value="2">2</option><option value="3">3</option></select></td><td><select class="parse-field" id="14-n"><option value="">—</option><option value="s">s</option><option value="p">p</option><option value="du">du</option></select></td><td><select class="parse-field" id="14-g"><option value="">—</option><option value="m">m</option><option value="f">f</option><option value="c">c</option></select></td><td><input class="parse-field" id="14-r" placeholder="root"/></td><td></td>
<td><button class="rbtn" onclick="tog(14)">▶ Answer</button></td>
</tr>
<tr class="ans-row" id="ans-14"><td class="ans-lbl">✓</td><td class="ans-heb">יִכְבַּד</td><td>3</td><td>s</td><td>m</td><td class="ans-heb">כבד</td><td colspan="2">Stative; patach under R2</td></tr>
<tr>
<td class="num">15</td><td class="heb">תִּגְדַּל</td>
<td><select class="parse-field" id="15-p"><option value="">—</option><option value="1">1</option><option value="2">2</option><option value="3">3</option></select></td><td><select class="parse-field" id="15-n"><option value="">—</option><option value="s">s</option><option value="p">p</option><option value="du">du</option></select></td><td><select class="parse-field" id="15-g"><option value="">—</option><option value="m">m</option><option value="f">f</option><option value="c">c</option></select></td><td><input class="parse-field" id="15-r" placeholder="root"/></td><td></td>
<td><button class="rbtn" onclick="tog(15)">▶ Answer</button></td>
</tr>
<tr class="ans-row" id="ans-15"><td class="ans-lbl">✓</td><td class="ans-heb">תִּגְדַּל</td><td>3/2</td><td>s</td><td>f/m</td><td class="ans-heb">גדל</td><td colspan="2">Stative patach; ambiguous 3fs/2ms</td></tr>
<tr>
<td class="num">16</td><td class="heb">יִכְבְּדוּ</td>
<td><select class="parse-field" id="16-p"><option value="">—</option><option value="1">1</option><option value="2">2</option><option value="3">3</option></select></td><td><select class="parse-field" id="16-n"><option value="">—</option><option value="s">s</option><option value="p">p</option><option value="du">du</option></select></td><td><select class="parse-field" id="16-g"><option value="">—</option><option value="m">m</option><option value="f">f</option><option value="c">c</option></select></td><td><input class="parse-field" id="16-r" placeholder="root"/></td><td></td>
<td><button class="rbtn" onclick="tog(16)">▶ Answer</button></td>
</tr>
<tr class="ans-row" id="ans-16"><td class="ans-lbl">✓</td><td class="ans-heb">יִכְבְּדוּ</td><td>3</td><td>p</td><td>m</td><td class="ans-heb">כבד</td><td colspan="2">3mp</td></tr>
<tr>
<td class="num">17</td><td class="heb">תִּשְׁמַעְנָה</td>
<td><select class="parse-field" id="17-p"><option value="">—</option><option value="1">1</option><option value="2">2</option><option value="3">3</option></select></td><td><select class="parse-field" id="17-n"><option value="">—</option><option value="s">s</option><option value="p">p</option><option value="du">du</option></select></td><td><select class="parse-field" id="17-g"><option value="">—</option><option value="m">m</option><option value="f">f</option><option value="c">c</option></select></td><td><input class="parse-field" id="17-r" placeholder="root"/></td><td></td>
<td><button class="rbtn" onclick="tog(17)">▶ Answer</button></td>
</tr>
<tr class="ans-row" id="ans-17"><td class="ans-lbl">✓</td><td class="ans-heb">תִּשְׁמַעְנָה</td><td>3/2</td><td>p</td><td>f</td><td class="ans-heb">שמע</td><td colspan="2">נָה- ending; B-class</td></tr>
<tr>
<td class="num">18</td><td class="heb">אֶשְׁמַע</td>
<td><select class="parse-field" id="18-p"><option value="">—</option><option value="1">1</option><option value="2">2</option><option value="3">3</option></select></td><td><select class="parse-field" id="18-n"><option value="">—</option><option value="s">s</option><option value="p">p</option><option value="du">du</option></select></td><td><select class="parse-field" id="18-g"><option value="">—</option><option value="m">m</option><option value="f">f</option><option value="c">c</option></select></td><td><input class="parse-field" id="18-r" placeholder="root"/></td><td></td>
<td><button class="rbtn" onclick="tog(18)">▶ Answer</button></td>
</tr>
<tr class="ans-row" id="ans-18"><td class="ans-lbl">✓</td><td class="ans-heb">אֶשְׁמַע</td><td>1</td><td>s</td><td>c</td><td class="ans-heb">שמע</td><td colspan="2">Patach under prefix (1cs) + B-class patach</td></tr>
<tr>
<td class="num">19</td><td class="heb">נִשְׁמַע</td>
<td><select class="parse-field" id="19-p"><option value="">—</option><option value="1">1</option><option value="2">2</option><option value="3">3</option></select></td><td><select class="parse-field" id="19-n"><option value="">—</option><option value="s">s</option><option value="p">p</option><option value="du">du</option></select></td><td><select class="parse-field" id="19-g"><option value="">—</option><option value="m">m</option><option value="f">f</option><option value="c">c</option></select></td><td><input class="parse-field" id="19-r" placeholder="root"/></td><td></td>
<td><button class="rbtn" onclick="tog(19)">▶ Answer</button></td>
</tr>
<tr class="ans-row" id="ans-19"><td class="ans-lbl">✓</td><td class="ans-heb">נִשְׁמַע</td><td>1</td><td>p</td><td>c</td><td class="ans-heb">שמע</td><td colspan="2">1cp nun prefix</td></tr>
<tr>
<td class="num">20</td><td class="heb">יִגְדַּל</td>
<td><select class="parse-field" id="20-p"><option value="">—</option><option value="1">1</option><option value="2">2</option><option value="3">3</option></select></td><td><select class="parse-field" id="20-n"><option value="">—</option><option value="s">s</option><option value="p">p</option><option value="du">du</option></select></td><td><select class="parse-field" id="20-g"><option value="">—</option><option value="m">m</option><option value="f">f</option><option value="c">c</option></select></td><td><input class="parse-field" id="20-r" placeholder="root"/></td><td></td>
<td><button class="rbtn" onclick="tog(20)">▶ Answer</button></td>
</tr>
<tr class="ans-row" id="ans-20"><td class="ans-lbl">✓</td><td class="ans-heb">יִגְדַּל</td><td>3</td><td>s</td><td>m</td><td class="ans-heb">גדל</td><td colspan="2">Stative patach</td></tr>
</table>
<hr class="sec"/>
<!-- PART C -->
<h2>Part C — Jussive and Cohortative Forms</h2>
<div class="note-box">For most <strong>strong verbs</strong>, the Jussive 3ms is identical in form to the regular Imperfect 3ms — no shortening occurs. Only weak verbs (especially III-ה) show a distinct Jussive shape. Items 23–24 test this awareness.</div>
<table>
<tr><th>#</th><th>Form</th><th>Person</th><th>Number</th><th>Gender</th><th>Root</th><th>Form Type</th><th></th></tr>
<tr>
<td class="num">21</td><td class="heb">יִשְׁמְרָה</td>
<td><select class="parse-field" id="21-p"><option value="">—</option><option value="1">1</option><option value="2">2</option><option value="3">3</option></select></td><td><select class="parse-field" id="21-n"><option value="">—</option><option value="s">s</option><option value="p">p</option><option value="du">du</option></select></td><td><select class="parse-field" id="21-g"><option value="">—</option><option value="m">m</option><option value="f">f</option><option value="c">c</option></select></td><td><input class="parse-field" id="21-r" placeholder="root"/></td>
<td><input class="parse-field" id="21-t" placeholder="Jussive/Cohortative"/></td>
<td><button class="rbtn" onclick="tog(21)">▶ Answer</button></td>
</tr>
<tr class="ans-row" id="ans-21"><td class="ans-lbl">✓</td><td class="ans-heb">יִשְׁמְרָה</td><td>3</td><td>s</td><td>m</td><td class="ans-heb">שמר</td><td colspan="2">Unusual ָה- on 3ms — energic-nun form; standard Jussive 3ms = יִשְׁמֹר (no shortening for strong verb)</td></tr>
<tr>
<td class="num">22</td><td class="heb">נִשְׁמְרָה</td>
<td><select class="parse-field" id="22-p"><option value="">—</option><option value="1">1</option><option value="2">2</option><option value="3">3</option></select></td><td><select class="parse-field" id="22-n"><option value="">—</option><option value="s">s</option><option value="p">p</option><option value="du">du</option></select></td><td><select class="parse-field" id="22-g"><option value="">—</option><option value="m">m</option><option value="f">f</option><option value="c">c</option></select></td><td><input class="parse-field" id="22-r" placeholder="root"/></td>
<td><input class="parse-field" id="22-t" placeholder="Jussive/Cohortative"/></td>
<td><button class="rbtn" onclick="tog(22)">▶ Answer</button></td>
</tr>
<tr class="ans-row" id="ans-22"><td class="ans-lbl">✓</td><td class="ans-heb">נִשְׁמְרָה</td><td>1</td><td>p</td><td>c</td><td class="ans-heb">שמר</td><td colspan="2">Cohortative — ָה- on 1cp; "Let us keep"</td></tr>
<tr>
<td class="num">23</td><td class="heb">יִשְׁמֹר</td>
<td><select class="parse-field" id="23-p"><option value="">—</option><option value="1">1</option><option value="2">2</option><option value="3">3</option></select></td><td><select class="parse-field" id="23-n"><option value="">—</option><option value="s">s</option><option value="p">p</option><option value="du">du</option></select></td><td><select class="parse-field" id="23-g"><option value="">—</option><option value="m">m</option><option value="f">f</option><option value="c">c</option></select></td><td><input class="parse-field" id="23-r" placeholder="root"/></td>
<td><input class="parse-field" id="23-t" placeholder="Jussive/Cohortative"/></td>
<td><button class="rbtn" onclick="tog(23)">▶ Answer</button></td>
</tr>
<tr class="ans-row" id="ans-23"><td class="ans-lbl">✓</td><td class="ans-heb">יִשְׁמֹר</td><td>3</td><td>s</td><td>m</td><td class="ans-heb">שמר</td><td colspan="2">Jussive (or Imperfect) — strong root: Jussive = Imperfect in form; context determines</td></tr>
<tr>
<td class="num">24</td><td class="heb">תִּשְׁמֹר</td>
<td><select class="parse-field" id="24-p"><option value="">—</option><option value="1">1</option><option value="2">2</option><option value="3">3</option></select></td><td><select class="parse-field" id="24-n"><option value="">—</option><option value="s">s</option><option value="p">p</option><option value="du">du</option></select></td><td><select class="parse-field" id="24-g"><option value="">—</option><option value="m">m</option><option value="f">f</option><option value="c">c</option></select></td><td><input class="parse-field" id="24-r" placeholder="root"/></td>
<td><input class="parse-field" id="24-t" placeholder="Jussive/Cohortative"/></td>
<td><button class="rbtn" onclick="tog(24)">▶ Answer</button></td>
</tr>
<tr class="ans-row" id="ans-24"><td class="ans-lbl">✓</td><td class="ans-heb">תִּשְׁמֹר</td><td>3/2</td><td>s</td><td>f/m</td><td class="ans-heb">שמר</td><td colspan="2">Jussive (or Imperfect) — same: no form distinction for strong roots</td></tr>
<tr>
<td class="num">25</td><td class="heb">אֶשְׁמְרָה</td>
<td><select class="parse-field" id="25-p"><option value="">—</option><option value="1">1</option><option value="2">2</option><option value="3">3</option></select></td><td><select class="parse-field" id="25-n"><option value="">—</option><option value="s">s</option><option value="p">p</option><option value="du">du</option></select></td><td><select class="parse-field" id="25-g"><option value="">—</option><option value="m">m</option><option value="f">f</option><option value="c">c</option></select></td><td><input class="parse-field" id="25-r" placeholder="root"/></td>
<td><input class="parse-field" id="25-t" placeholder="Jussive/Cohortative"/></td>
<td><button class="rbtn" onclick="tog(25)">▶ Answer</button></td>
</tr>
<tr class="ans-row" id="ans-25"><td class="ans-lbl">✓</td><td class="ans-heb">אֶשְׁמְרָה</td><td>1</td><td>s</td><td>c</td><td class="ans-heb">שמר</td><td colspan="2">Cohortative — ָה- on 1cs; "Let me keep"</td></tr>
</table>
<script>
  const ids = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25];
  function tog(id) { const r=document.getElementById('ans-'+id); const b=r.previousElementSibling.querySelector('button'); const v=r.style.display==='table-row'; r.style.display=v?'none':'table-row'; b.textContent=v?'▶ Answer':'▼ Hide'; b.classList.toggle('on',!v); }
  function showAll() { ids.forEach(id=>{const r=document.getElementById('ans-'+id);const b=r.previousElementSibling.querySelector('button');r.style.display='table-row';b.textContent='▼ Hide';b.classList.add('on');}); }
  function hideAll() { ids.forEach(id=>{const r=document.getElementById('ans-'+id);const b=r.previousElementSibling.querySelector('button');r.style.display='none';b.textContent='▶ Answer';b.classList.remove('on');}); }
  function clearAll() { document.querySelectorAll('.parse-field').forEach(e=>e.value=''); }
</script>

