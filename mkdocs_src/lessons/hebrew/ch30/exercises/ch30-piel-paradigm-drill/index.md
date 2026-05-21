# Piel Paradigm Drill

*Chapter 30 — Piel Strong*

[Full screen](ch30-piel-paradigm-drill.html){.md-button}  [Markdown](ch30-piel-paradigm-drill.md){.md-button}  [Print (PDF)](ch30-piel-paradigm-drill.pdf){.md-button}

<style>

body { font-family: Georgia, serif;    color: #222; line-height: 1.6; }
h1 { font-size: 1.45rem; border-bottom: 2px solid #555; padding-bottom: .4rem; }
h2 { font-size: 1.05rem; margin-top: 2rem; color: #333; border-bottom: 1px solid #ddd; padding-bottom: .2rem; }
.subtitle { color: #666; font-style: italic; margin-top: -.4rem; }
.instructions { background: #f8f8f0; border-left: 4px solid #bbb; padding: .75rem 1rem; margin: 1rem 0; font-size: .92rem; }
table { border-collapse: collapse; width: 100%; margin: .4rem 0; font-size: .91rem; }
th { background: #e0e8f0; padding: .4rem .55rem; border: 1px solid #bbb; text-align: left; font-size: .84rem; }
td { padding: .3rem .45rem; border: 1px solid #ddd; vertical-align: middle; }
td.num { text-align: center; font-weight: bold; color: #666; width: 2.2rem; }
td.pgn { font-weight: bold; color: #333; width: 5rem; }
td.heb-ans { font-size: 1.25rem; direction: rtl; unicode-bidi: embed; font-family: 'Arial Hebrew', Arial, sans-serif; color: #2a6e2a; min-width: 7rem; }
input.f { width: 100%; box-sizing: border-box; border: 1px solid #bbb; border-radius: 3px; padding: .22rem .4rem; font-family: 'Arial Hebrew', Arial, sans-serif; font-size: 1.05rem; direction: rtl; background: #fafff8; }
input.f:focus { outline: none; border-color: #5a9; box-shadow: 0 0 0 2px #c8ecd4; }
.ans-row { display: none; background: #f0faf0; }
.ans-row td { font-size: .87rem; color: #2a6e2a; padding: .28rem .45rem; }
.ans-lbl { font-weight: bold; color: #1a5c1a; width: 2.2rem; text-align: center; }
button.rbtn { font-size: .76rem; padding: .14rem .48rem; cursor: pointer; background: #e8f4ec; border: 1px solid #7bba8f; border-radius: 3px; color: #2a6e2a; white-space: nowrap; }
button.rbtn:hover, button.rbtn.on { background: #c8ecd4; }
.controls { display: flex; gap: .7rem; flex-wrap: wrap; margin: 1rem 0 1.5rem; }
.controls button { padding: .38rem .85rem; cursor: pointer; border-radius: 4px; font-size: .88rem; border: 1px solid #999; background: #f0f0f0; color: #333; }
.controls button:hover { background: #ddd; }
.clr { border-color: #c06060 !important; color: #8b0000 !important; background: #fff0f0 !important; }
.clr:hover { background: #ffd8d8 !important; }
hr.sec { border: none; border-top: 2px dashed #ccc; margin: 2rem 0; }
@media print { .controls, button.rbtn { display: none; } input.f { border: none; border-bottom: 1px solid #aaa; border-radius: 0; background: transparent; direction: rtl; } .ans-row { display: none !important; } }

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

<h1>Ch30 Piel Paradigm Drill</h1>
<p class="subtitle">Root: דבר &nbsp;|&nbsp; Stem: Piel</p>
<div class="instructions">Write the complete Piel paradigm for the root דבר. Key marker: dagesh forte in R2 throughout.</div>

<div class="controls">
  <button onclick="showAll()">Show All Answers</button>
  <button onclick="hideAll()">Hide All Answers</button>
  <button class="clr" onclick="clearAll()">Clear All Inputs</button>
</div>

<h2>Part A — Perfect (9 forms)</h2>
<table>
<thead><tr><th>#</th><th>PGN</th><th>Form</th><th></th></tr></thead>
<tbody>
<tr><td class="num">1</td><td class="pgn">3ms</td><td><input class="parse-field" id="f-a1" placeholder="כתוב..."></td><td><button class="rbtn" onclick="tog('a1')">▶ Answer</button></td></tr>
<tr class="ans-row" id="ans-a1"><td class="ans-lbl">✓</td><td class="pgn">3ms</td><td class="heb-ans">דִּבֵּר</td><td></td></tr>
<tr><td class="num">2</td><td class="pgn">3fs</td><td><input class="parse-field" id="f-a2" placeholder="כתוב..."></td><td><button class="rbtn" onclick="tog('a2')">▶ Answer</button></td></tr>
<tr class="ans-row" id="ans-a2"><td class="ans-lbl">✓</td><td class="pgn">3fs</td><td class="heb-ans">דִּבְּרָה</td><td></td></tr>
<tr><td class="num">3</td><td class="pgn">2ms</td><td><input class="parse-field" id="f-a3" placeholder="כתוב..."></td><td><button class="rbtn" onclick="tog('a3')">▶ Answer</button></td></tr>
<tr class="ans-row" id="ans-a3"><td class="ans-lbl">✓</td><td class="pgn">2ms</td><td class="heb-ans">דִּבַּרְתָּ</td><td></td></tr>
<tr><td class="num">4</td><td class="pgn">2fs</td><td><input class="parse-field" id="f-a4" placeholder="כתוב..."></td><td><button class="rbtn" onclick="tog('a4')">▶ Answer</button></td></tr>
<tr class="ans-row" id="ans-a4"><td class="ans-lbl">✓</td><td class="pgn">2fs</td><td class="heb-ans">דִּבַּרְתְּ</td><td></td></tr>
<tr><td class="num">5</td><td class="pgn">1cs</td><td><input class="parse-field" id="f-a5" placeholder="כתוב..."></td><td><button class="rbtn" onclick="tog('a5')">▶ Answer</button></td></tr>
<tr class="ans-row" id="ans-a5"><td class="ans-lbl">✓</td><td class="pgn">1cs</td><td class="heb-ans">דִּבַּרְתִּי</td><td></td></tr>
<tr><td class="num">6</td><td class="pgn">3cp</td><td><input class="parse-field" id="f-a6" placeholder="כתוב..."></td><td><button class="rbtn" onclick="tog('a6')">▶ Answer</button></td></tr>
<tr class="ans-row" id="ans-a6"><td class="ans-lbl">✓</td><td class="pgn">3cp</td><td class="heb-ans">דִּבְּרוּ</td><td></td></tr>
<tr><td class="num">7</td><td class="pgn">2mp</td><td><input class="parse-field" id="f-a7" placeholder="כתוב..."></td><td><button class="rbtn" onclick="tog('a7')">▶ Answer</button></td></tr>
<tr class="ans-row" id="ans-a7"><td class="ans-lbl">✓</td><td class="pgn">2mp</td><td class="heb-ans">דִּבַּרְתֶּם</td><td></td></tr>
<tr><td class="num">8</td><td class="pgn">2fp</td><td><input class="parse-field" id="f-a8" placeholder="כתוב..."></td><td><button class="rbtn" onclick="tog('a8')">▶ Answer</button></td></tr>
<tr class="ans-row" id="ans-a8"><td class="ans-lbl">✓</td><td class="pgn">2fp</td><td class="heb-ans">דִּבַּרְתֶּן</td><td></td></tr>
<tr><td class="num">9</td><td class="pgn">1cp</td><td><input class="parse-field" id="f-a9" placeholder="כתוב..."></td><td><button class="rbtn" onclick="tog('a9')">▶ Answer</button></td></tr>
<tr class="ans-row" id="ans-a9"><td class="ans-lbl">✓</td><td class="pgn">1cp</td><td class="heb-ans">דִּבַּרְנוּ</td><td></td></tr>
</tbody>
</table>

<hr class="sec">

<h2>Part B — Imperfect (10 forms)</h2>
<table>
<thead><tr><th>#</th><th>PGN</th><th>Form</th><th></th></tr></thead>
<tbody>
<tr><td class="num">1</td><td class="pgn">3ms</td><td><input class="parse-field" id="f-b1" placeholder="כתוב..."></td><td><button class="rbtn" onclick="tog('b1')">▶ Answer</button></td></tr>
<tr class="ans-row" id="ans-b1"><td class="ans-lbl">✓</td><td class="pgn">3ms</td><td class="heb-ans">יְדַבֵּר</td><td></td></tr>
<tr><td class="num">2</td><td class="pgn">3fs</td><td><input class="parse-field" id="f-b2" placeholder="כתוב..."></td><td><button class="rbtn" onclick="tog('b2')">▶ Answer</button></td></tr>
<tr class="ans-row" id="ans-b2"><td class="ans-lbl">✓</td><td class="pgn">3fs</td><td class="heb-ans">תְּדַבֵּר</td><td></td></tr>
<tr><td class="num">3</td><td class="pgn">2ms</td><td><input class="parse-field" id="f-b3" placeholder="כתוב..."></td><td><button class="rbtn" onclick="tog('b3')">▶ Answer</button></td></tr>
<tr class="ans-row" id="ans-b3"><td class="ans-lbl">✓</td><td class="pgn">2ms</td><td class="heb-ans">תְּדַבֵּר</td><td></td></tr>
<tr><td class="num">4</td><td class="pgn">2fs</td><td><input class="parse-field" id="f-b4" placeholder="כתוב..."></td><td><button class="rbtn" onclick="tog('b4')">▶ Answer</button></td></tr>
<tr class="ans-row" id="ans-b4"><td class="ans-lbl">✓</td><td class="pgn">2fs</td><td class="heb-ans">תְּדַבְּרִי</td><td></td></tr>
<tr><td class="num">5</td><td class="pgn">1cs</td><td><input class="parse-field" id="f-b5" placeholder="כתוב..."></td><td><button class="rbtn" onclick="tog('b5')">▶ Answer</button></td></tr>
<tr class="ans-row" id="ans-b5"><td class="ans-lbl">✓</td><td class="pgn">1cs</td><td class="heb-ans">אֲדַבֵּר</td><td></td></tr>
<tr><td class="num">6</td><td class="pgn">3mp</td><td><input class="parse-field" id="f-b6" placeholder="כתוב..."></td><td><button class="rbtn" onclick="tog('b6')">▶ Answer</button></td></tr>
<tr class="ans-row" id="ans-b6"><td class="ans-lbl">✓</td><td class="pgn">3mp</td><td class="heb-ans">יְדַבְּרוּ</td><td></td></tr>
<tr><td class="num">7</td><td class="pgn">3fp</td><td><input class="parse-field" id="f-b7" placeholder="כתוב..."></td><td><button class="rbtn" onclick="tog('b7')">▶ Answer</button></td></tr>
<tr class="ans-row" id="ans-b7"><td class="ans-lbl">✓</td><td class="pgn">3fp</td><td class="heb-ans">תְּדַבֵּרְנָה</td><td></td></tr>
<tr><td class="num">8</td><td class="pgn">2mp</td><td><input class="parse-field" id="f-b8" placeholder="כתוב..."></td><td><button class="rbtn" onclick="tog('b8')">▶ Answer</button></td></tr>
<tr class="ans-row" id="ans-b8"><td class="ans-lbl">✓</td><td class="pgn">2mp</td><td class="heb-ans">תְּדַבְּרוּ</td><td></td></tr>
<tr><td class="num">9</td><td class="pgn">2fp</td><td><input class="parse-field" id="f-b9" placeholder="כתוב..."></td><td><button class="rbtn" onclick="tog('b9')">▶ Answer</button></td></tr>
<tr class="ans-row" id="ans-b9"><td class="ans-lbl">✓</td><td class="pgn">2fp</td><td class="heb-ans">תְּדַבֵּרְנָה</td><td></td></tr>
<tr><td class="num">10</td><td class="pgn">1cp</td><td><input class="parse-field" id="f-b10" placeholder="כתוב..."></td><td><button class="rbtn" onclick="tog('b10')">▶ Answer</button></td></tr>
<tr class="ans-row" id="ans-b10"><td class="ans-lbl">✓</td><td class="pgn">1cp</td><td class="heb-ans">נְדַבֵּר</td><td></td></tr>
</tbody>
</table>

<hr class="sec">

<h2>Part C — Imperative (4 forms)</h2>
<table>
<thead><tr><th>#</th><th>PGN</th><th>Form</th><th></th></tr></thead>
<tbody>
<tr><td class="num">1</td><td class="pgn">2ms</td><td><input class="parse-field" id="f-c1" placeholder="כתוב..."></td><td><button class="rbtn" onclick="tog('c1')">▶ Answer</button></td></tr>
<tr class="ans-row" id="ans-c1"><td class="ans-lbl">✓</td><td class="pgn">2ms</td><td class="heb-ans">דַּבֵּר</td><td></td></tr>
<tr><td class="num">2</td><td class="pgn">2fs</td><td><input class="parse-field" id="f-c2" placeholder="כתוב..."></td><td><button class="rbtn" onclick="tog('c2')">▶ Answer</button></td></tr>
<tr class="ans-row" id="ans-c2"><td class="ans-lbl">✓</td><td class="pgn">2fs</td><td class="heb-ans">דַּבְּרִי</td><td></td></tr>
<tr><td class="num">3</td><td class="pgn">2mp</td><td><input class="parse-field" id="f-c3" placeholder="כתוב..."></td><td><button class="rbtn" onclick="tog('c3')">▶ Answer</button></td></tr>
<tr class="ans-row" id="ans-c3"><td class="ans-lbl">✓</td><td class="pgn">2mp</td><td class="heb-ans">דַּבְּרוּ</td><td></td></tr>
<tr><td class="num">4</td><td class="pgn">2fp</td><td><input class="parse-field" id="f-c4" placeholder="כתוב..."></td><td><button class="rbtn" onclick="tog('c4')">▶ Answer</button></td></tr>
<tr class="ans-row" id="ans-c4"><td class="ans-lbl">✓</td><td class="pgn">2fp</td><td class="heb-ans">דַּבֵּרְנָה</td><td></td></tr>
</tbody>
</table>

<hr class="sec">

<h2>Part D — Infinitive Construct (2 forms)</h2>
<table>
<thead><tr><th>#</th><th>Description</th><th>Form</th><th></th></tr></thead>
<tbody>
<tr><td class="num">1</td><td class="pgn">Base</td><td><input class="parse-field" id="f-d1" placeholder="כתוב..."></td><td><button class="rbtn" onclick="tog('d1')">▶ Answer</button></td></tr>
<tr class="ans-row" id="ans-d1"><td class="ans-lbl">✓</td><td class="pgn">Base</td><td class="heb-ans">דַּבֵּר</td><td></td></tr>
<tr><td class="num">2</td><td class="pgn">With לְ</td><td><input class="parse-field" id="f-d2" placeholder="כתוב..."></td><td><button class="rbtn" onclick="tog('d2')">▶ Answer</button></td></tr>
<tr class="ans-row" id="ans-d2"><td class="ans-lbl">✓</td><td class="pgn">With לְ</td><td class="heb-ans">לְדַבֵּר</td><td></td></tr>
</tbody>
</table>

<hr class="sec">

<h2>Part E — Infinitive Absolute (1 form)</h2>
<table>
<thead><tr><th>#</th><th>Description</th><th>Form</th><th></th></tr></thead>
<tbody>
<tr><td class="num">1</td><td class="pgn">Inf. Absolute</td><td><input class="parse-field" id="f-e1" placeholder="כתוב..."></td><td><button class="rbtn" onclick="tog('e1')">▶ Answer</button></td></tr>
<tr class="ans-row" id="ans-e1"><td class="ans-lbl">✓</td><td class="pgn">Inf. Absolute</td><td class="heb-ans">דַּבֵּר</td><td></td></tr>
</tbody>
</table>

<hr class="sec">

<h2>Part F — Participle (4 forms)</h2>
<table>
<thead><tr><th>#</th><th>PGN</th><th>Form</th><th></th></tr></thead>
<tbody>
<tr><td class="num">1</td><td class="pgn">ms</td><td><input class="parse-field" id="f-f1" placeholder="כתוב..."></td><td><button class="rbtn" onclick="tog('f1')">▶ Answer</button></td></tr>
<tr class="ans-row" id="ans-f1"><td class="ans-lbl">✓</td><td class="pgn">ms</td><td class="heb-ans">מְדַבֵּר</td><td></td></tr>
<tr><td class="num">2</td><td class="pgn">fs</td><td><input class="parse-field" id="f-f2" placeholder="כתוב..."></td><td><button class="rbtn" onclick="tog('f2')">▶ Answer</button></td></tr>
<tr class="ans-row" id="ans-f2"><td class="ans-lbl">✓</td><td class="pgn">fs</td><td class="heb-ans">מְדַבֶּרֶת</td><td></td></tr>
<tr><td class="num">3</td><td class="pgn">mp</td><td><input class="parse-field" id="f-f3" placeholder="כתוב..."></td><td><button class="rbtn" onclick="tog('f3')">▶ Answer</button></td></tr>
<tr class="ans-row" id="ans-f3"><td class="ans-lbl">✓</td><td class="pgn">mp</td><td class="heb-ans">מְדַבְּרִים</td><td></td></tr>
<tr><td class="num">4</td><td class="pgn">fp</td><td><input class="parse-field" id="f-f4" placeholder="כתוב..."></td><td><button class="rbtn" onclick="tog('f4')">▶ Answer</button></td></tr>
<tr class="ans-row" id="ans-f4"><td class="ans-lbl">✓</td><td class="pgn">fp</td><td class="heb-ans">מְדַבְּרוֹת</td><td></td></tr>
</tbody>
</table>

<script>
function tog(n){var r=document.getElementById('ans-'+n);r.style.display=r.style.display==='table-row'?'none':'table-row';}
function showAll(){document.querySelectorAll('.ans-row').forEach(r=>r.style.display='table-row');}
function hideAll(){document.querySelectorAll('.ans-row').forEach(r=>r.style.display='none');}
function clearAll(){document.querySelectorAll('input.f').forEach(i=>i.value='');}
</script>

