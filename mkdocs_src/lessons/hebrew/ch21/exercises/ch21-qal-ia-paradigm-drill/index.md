# Qal Ia Paradigm Drill

*Chapter 21 — Qal Infinitive Absolute*

[Full screen](ch21-qal-ia-paradigm-drill.html){.md-button}  [Markdown](ch21-qal-ia-paradigm-drill.md){.md-button}  [Print (PDF)](ch21-qal-ia-paradigm-drill.pdf){.md-button}

<style>

  body { font-family: Georgia, serif;    color: #222; line-height: 1.6; }
  h1 { font-size: 1.45rem; border-bottom: 2px solid #555; padding-bottom: .4rem; }
  h2 { font-size: 1.05rem; margin-top: 2rem; color: #333; border-bottom: 1px solid #ddd; padding-bottom: .2rem; }
  .subtitle { color: #666; font-style: italic; margin-top: -.4rem; }
  .instructions { background: #f8f8f0; border-left: 4px solid #bbb; padding: .75rem 1rem; margin: 1rem 0; font-size: .92rem; }
  table { border-collapse: collapse;  margin: .4rem 0; font-size: .91rem; }
  th { background: #e0e8f0; padding: .4rem .55rem; border: 1px solid #bbb; text-align: left; font-size: .84rem; }
  td { padding: .3rem .45rem; border: 1px solid #ddd; vertical-align: middle; }
  td.num { text-align: center; font-weight: bold; color: #666; width: 2.2rem; }
  td.pgn { font-weight: bold; color: #333; width: 8rem; }
  td.root { font-size: 1.1rem; direction: rtl; unicode-bidi: embed; font-family: 'Arial Hebrew', Arial, sans-serif; font-weight: bold; width: 4rem; }
  td.heb-ans { font-size: 1.25rem; direction: rtl; unicode-bidi: embed; font-family: 'Arial Hebrew', Arial, sans-serif; color: #2a6e2a; min-width: 6rem; }
  td.heb-ref { font-size: 1.1rem; direction: rtl; unicode-bidi: embed; font-family: 'Arial Hebrew', Arial, sans-serif; color: #555; }
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

</style>

<h1>Ch21 Qal Infinitive Absolute Paradigm Drill</h1>
<p class="subtitle">BBH Chapter 21 · 6 root classes · Infinitive Absolute forms</p>

<div class="instructions">
  <strong>Instructions:</strong> Give the Qal Infinitive Absolute for each root class.
  Compare with the Infinitive Construct reference table at the bottom.
</div>

<div class="controls">
  <button onclick="showAll()">Show All Answers</button>
  <button onclick="hideAll()">Hide All Answers</button>
  <button class="clr" onclick="clearAll()">Clear All Inputs</button>
</div>

<div style="overflow-x:auto;max-width:100%;"><table>
  <tr><th>#</th><th>Root class</th><th>Root</th><th>Infinitive Absolute</th><th></th></tr>

  <tr>
    <td class="num">1</td>
    <td class="pgn">Strong A</td>
    <td class="root">שמר</td>
    <td><input class="parse-field" id="f-1" placeholder="כתוב..."></td>
    <td><button class="rbtn" onclick="tog(1)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-1">
    <td class="ans-lbl">✓</td>
    <td class="pgn">Strong A</td>
    <td class="root">שמר</td>
    <td class="heb-ans">שָׁמוֹר</td>
    <td></td>
  </tr>

  <tr>
    <td class="num">2</td>
    <td class="pgn">III-ה</td>
    <td class="root">ראה</td>
    <td><input class="parse-field" id="f-2" placeholder="כתוב..."></td>
    <td><button class="rbtn" onclick="tog(2)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-2">
    <td class="ans-lbl">✓</td>
    <td class="pgn">III-ה</td>
    <td class="root">ראה</td>
    <td class="heb-ans">רָאֹה</td>
    <td></td>
  </tr>

  <tr>
    <td class="num">3</td>
    <td class="pgn">Biconsonantal</td>
    <td class="root">מות</td>
    <td><input class="parse-field" id="f-3" placeholder="כתוב..."></td>
    <td><button class="rbtn" onclick="tog(3)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-3">
    <td class="ans-lbl">✓</td>
    <td class="pgn">Biconsonantal</td>
    <td class="root">מות</td>
    <td class="heb-ans">מוֹת</td>
    <td></td>
  </tr>

  <tr>
    <td class="num">4</td>
    <td class="pgn">I-י</td>
    <td class="root">הלך</td>
    <td><input class="parse-field" id="f-4" placeholder="כתוב..."></td>
    <td><button class="rbtn" onclick="tog(4)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-4">
    <td class="ans-lbl">✓</td>
    <td class="pgn">I-י</td>
    <td class="root">הלך</td>
    <td class="heb-ans">הָלוֹךְ</td>
    <td></td>
  </tr>

  <tr>
    <td class="num">5</td>
    <td class="pgn">I-נ</td>
    <td class="root">נתן</td>
    <td><input class="parse-field" id="f-5" placeholder="כתוב..."></td>
    <td><button class="rbtn" onclick="tog(5)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-5">
    <td class="ans-lbl">✓</td>
    <td class="pgn">I-נ</td>
    <td class="root">נתן</td>
    <td class="heb-ans">נָתוֹן</td>
    <td></td>
  </tr>

  <tr>
    <td class="num">6</td>
    <td class="pgn">I-aleph</td>
    <td class="root">אכל</td>
    <td><input class="parse-field" id="f-6" placeholder="כתוב..."></td>
    <td><button class="rbtn" onclick="tog(6)">▶ Answer</button></td>
  </tr>
  <tr class="ans-row" id="ans-6">
    <td class="ans-lbl">✓</td>
    <td class="pgn">I-aleph</td>
    <td class="root">אכל</td>
    <td class="heb-ans">אָכוֹל</td>
    <td></td>
  </tr>

</table></div>

<hr class="sec">

<h2>Reference: Infinitive Absolute vs. Infinitive Construct</h2>
<div style="overflow-x:auto;max-width:100%;"><table>
  <tr><th>Root class</th><th>Root</th><th>Inf. Absolute</th><th>Inf. Construct</th></tr>
  <tr><td class="pgn">Strong A</td><td class="root">שמר</td><td class="heb-ref">שָׁמוֹר</td><td class="heb-ref">שְׁמֹר</td></tr>
  <tr><td class="pgn">III-ה</td><td class="root">ראה</td><td class="heb-ref">רָאֹה</td><td class="heb-ref">רְאוֹת</td></tr>
  <tr><td class="pgn">Biconsonantal</td><td class="root">מות</td><td class="heb-ref">מוֹת</td><td class="heb-ref">מוּת</td></tr>
  <tr><td class="pgn">I-י</td><td class="root">הלך</td><td class="heb-ref">הָלוֹךְ</td><td class="heb-ref">לֶכֶת</td></tr>
  <tr><td class="pgn">I-נ</td><td class="root">נתן</td><td class="heb-ref">נָתוֹן</td><td class="heb-ref">תֵּת</td></tr>
  <tr><td class="pgn">I-aleph</td><td class="root">אכל</td><td class="heb-ref">אָכוֹל</td><td class="heb-ref">אֱכֹל</td></tr>
</table></div>

<script>
function tog(n){var r=document.getElementById('ans-'+n);r.style.display=r.style.display==='table-row'?'none':'table-row';}
function showAll(){document.querySelectorAll('.ans-row').forEach(r=>r.style.display='table-row');}
function hideAll(){document.querySelectorAll('.ans-row').forEach(r=>r.style.display='none');}
function clearAll(){document.querySelectorAll('input.f').forEach(i=>i.value='');}
</script>

