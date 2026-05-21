# Stem Id Drill

*Chapter 32 — Pual Strong*

[Full screen](ch32-stem-id-drill.html){.md-button}  [Markdown](ch32-stem-id-drill.md){.md-button}  [Print (PDF)](ch32-stem-id-drill.pdf){.md-button}

<style>

  body { font-family: Georgia, serif;    color: #222; }
  h1 { font-size: 1.4em; border-bottom: 2px solid #444; padding-bottom: .4em; }
  h2 { font-size: 1.15em; margin-top: 2em; color: #444; }
  .subtitle { color: #666; font-style: italic; margin-top: -.3em; }
  table { border-collapse: collapse; width: 100%; margin: 1em 0; }
  th { background: #2a4a6e; color: #fff; padding: .5em .7em; text-align: left; font-size: .85em; }
  td { border: 1px solid #ccc; padding: .4em .6em; font-size: .85em; vertical-align: top; }
  tr:nth-child(even) td { background: #f7f7f7; }
  .heb { font-size: 1.25em; direction: rtl; unicode-bidi: embed; }
  input.parse-field { width: 100%; box-sizing: border-box; font-size: .85em; padding: 3px 5px; border: 1px solid #aaa; border-radius: 3px; }
  .answer-row td { background: #f0faf0 !important; color: #2a6e2a; font-size: .82em; }
  .answer-row { display: none; }
  button.reveal-btn { font-size: .78em; padding: 2px 7px; cursor: pointer; border: 1px solid #888; border-radius: 3px; background: #fff; white-space: nowrap; }
  .controls { margin: 1em 0; display: flex; gap: .6em; flex-wrap: wrap; }
  .controls button { padding: .4em .9em; font-size: .9em; cursor: pointer; border: 1px solid #555; border-radius: 4px; background: #f0f0f0; }
  .controls button:hover { background: #ddd; }
  .tip { background: #fffbe6; border-left: 4px solid #d4a017; padding: .5em 1em; margin: 1em 0; font-size: .88em; }
  .legend { border: 1px solid #ccc; border-radius: 4px; padding: .6em 1em; margin: 1em 0; font-size: .88em; }
  .legend table { margin: .3em 0; }
  .legend th { background: #555; font-size: .82em; }
  @media print {
    button, .controls { display: none !important; }
    input.parse-field { border: none; border-bottom: 1px solid #000; background: transparent; }
    .answer-row { display: table-row !important; }
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

<h1>Chapter 32 — Stem-ID Drill (Strong Roots)</h1>
<p class="subtitle">BBH Chapter 32 · Pual Strong Verbs</p>

<p>For each of the 24 forms, identify the stem (Qal / Piel / Pual), parse fully, and translate.</p>

<div class="legend">
  <table>
    <tr><th>Stem</th><th>Perfect 3ms</th><th>Imperfect 3ms</th><th>Participle ms</th></tr>
    <tr><td><strong>Qal</strong></td><td>qamets–patach (דָּבַר)</td><td>hiriq + shewa (יִדְבַּר)</td><td>holem + tsere (דֹּבֵר)</td></tr>
    <tr><td><strong>Piel</strong></td><td>hiriq + dagesh in R2 (דִּבֶּר)</td><td>shewa + patach + dagesh (יְדַבֵּר)</td><td>מְ + patach + dagesh (מְדַבֵּר)</td></tr>
    <tr><td><strong>Pual</strong></td><td>qibbuts + dagesh in R2 (דֻּבַּר)</td><td>shewa + qibbuts + dagesh (יְדֻבַּר)</td><td>מְ + qibbuts + qamets (מְדֻבָּר)</td></tr>
  </table>
</div>

<div class="tip"><strong>Quick test:</strong> Does R1 have qibbuts (ֻ) or holem where a guttural R2 blocks dagesh? → Pual. Does R1 have hiriq/tsere with dagesh forte in R2? → Piel. Plain vowel, no dagesh forte in R2? → Qal.</div>

<div class="controls">
  <button onclick="showAll()">Show All Answers</button>
  <button onclick="hideAll()">Hide All Answers</button>
  <button onclick="clearAll()">Clear All Inputs</button>
</div>

<table>
  <tr><th>#</th><th>Form</th><th>Stem</th><th>Conjugation</th><th>PGN</th><th>Root</th><th>Translation</th><th></th></tr>

  <tr><td>1</td><td><span class="heb">דָּבַר</span></td>
    <td><input class="parse-field" id="s1"></td><td><input class="parse-field" id="g1"></td><td><input class="parse-field" id="p1"></td><td><input class="parse-field" id="rt1"></td><td><input class="parse-field" id="t1"></td>
    <td><button class="reveal-btn" onclick="toggle('r1')">▶ Answer</button></td></tr>
  <tr class="answer-row" id="r1"><td colspan="8"><strong>Qal · Perfect · 3ms · דבר · "he spoke" (rare)</strong> — qamets under ד; patach under ב; no dagesh in ב</td></tr>

  <tr><td>2</td><td><span class="heb">דִּבֶּר</span></td>
    <td><input class="parse-field" id="s2"></td><td><input class="parse-field" id="g2"></td><td><input class="parse-field" id="p2"></td><td><input class="parse-field" id="rt2"></td><td><input class="parse-field" id="t2"></td>
    <td><button class="reveal-btn" onclick="toggle('r2')">▶ Answer</button></td></tr>
  <tr class="answer-row" id="r2"><td colspan="8"><strong>Piel · Perfect · 3ms · דבר · "he spoke"</strong> — hiriq under ד + dagesh forte in ב + tsere theme vowel</td></tr>

  <tr><td>3</td><td><span class="heb">דֻּבַּר</span></td>
    <td><input class="parse-field" id="s3"></td><td><input class="parse-field" id="g3"></td><td><input class="parse-field" id="p3"></td><td><input class="parse-field" id="rt3"></td><td><input class="parse-field" id="t3"></td>
    <td><button class="reveal-btn" onclick="toggle('r3')">▶ Answer</button></td></tr>
  <tr class="answer-row" id="r3"><td colspan="8"><strong>Pual · Perfect · 3ms · דבר · "it was spoken"</strong> — qibbuts under ד + dagesh forte in ב + patach theme vowel</td></tr>

  <tr><td>4</td><td><span class="heb">שָׁלַח</span></td>
    <td><input class="parse-field" id="s4"></td><td><input class="parse-field" id="g4"></td><td><input class="parse-field" id="p4"></td><td><input class="parse-field" id="rt4"></td><td><input class="parse-field" id="t4"></td>
    <td><button class="reveal-btn" onclick="toggle('r4')">▶ Answer</button></td></tr>
  <tr class="answer-row" id="r4"><td colspan="8"><strong>Qal · Perfect · 3ms · שׁלח · "he sent"</strong> — qamets under שׁ; patach under ל; ח at end (guttural, no dagesh issue)</td></tr>

  <tr><td>5</td><td><span class="heb">שִׁלַּח</span></td>
    <td><input class="parse-field" id="s5"></td><td><input class="parse-field" id="g5"></td><td><input class="parse-field" id="p5"></td><td><input class="parse-field" id="rt5"></td><td><input class="parse-field" id="t5"></td>
    <td><button class="reveal-btn" onclick="toggle('r5')">▶ Answer</button></td></tr>
  <tr class="answer-row" id="r5"><td colspan="8"><strong>Piel · Perfect · 3ms · שׁלח · "he sent away / released"</strong> — hiriq under שׁ + dagesh forte in ל + patach</td></tr>

  <tr><td>6</td><td><span class="heb">שֻׁלַּח</span></td>
    <td><input class="parse-field" id="s6"></td><td><input class="parse-field" id="g6"></td><td><input class="parse-field" id="p6"></td><td><input class="parse-field" id="rt6"></td><td><input class="parse-field" id="t6"></td>
    <td><button class="reveal-btn" onclick="toggle('r6')">▶ Answer</button></td></tr>
  <tr class="answer-row" id="r6"><td colspan="8"><strong>Pual · Perfect · 3ms · שׁלח · "he was sent away"</strong> — qibbuts under שׁ + dagesh forte in ל + patach</td></tr>

  <tr><td>7</td><td><span class="heb">כָּבֵד</span></td>
    <td><input class="parse-field" id="s7"></td><td><input class="parse-field" id="g7"></td><td><input class="parse-field" id="p7"></td><td><input class="parse-field" id="rt7"></td><td><input class="parse-field" id="t7"></td>
    <td><button class="reveal-btn" onclick="toggle('r7')">▶ Answer</button></td></tr>
  <tr class="answer-row" id="r7"><td colspan="8"><strong>Qal · Perfect · 3ms · כבד · "he was heavy / honored"</strong> — stative; qamets under כ + tsere theme vowel; no dagesh in ב</td></tr>

  <tr><td>8</td><td><span class="heb">כִּבֵּד</span></td>
    <td><input class="parse-field" id="s8"></td><td><input class="parse-field" id="g8"></td><td><input class="parse-field" id="p8"></td><td><input class="parse-field" id="rt8"></td><td><input class="parse-field" id="t8"></td>
    <td><button class="reveal-btn" onclick="toggle('r8')">▶ Answer</button></td></tr>
  <tr class="answer-row" id="r8"><td colspan="8"><strong>Piel · Perfect · 3ms · כבד · "he honored"</strong> — hiriq under כ + dagesh forte in ב + tsere</td></tr>

  <tr><td>9</td><td><span class="heb">כֻּבַּד</span></td>
    <td><input class="parse-field" id="s9"></td><td><input class="parse-field" id="g9"></td><td><input class="parse-field" id="p9"></td><td><input class="parse-field" id="rt9"></td><td><input class="parse-field" id="t9"></td>
    <td><button class="reveal-btn" onclick="toggle('r9')">▶ Answer</button></td></tr>
  <tr class="answer-row" id="r9"><td colspan="8"><strong>Pual · Perfect · 3ms · כבד · "he was honored"</strong> — qibbuts under כ + dagesh forte in ב + patach</td></tr>

  <tr><td>10</td><td><span class="heb">יְדַבֵּר</span></td>
    <td><input class="parse-field" id="s10"></td><td><input class="parse-field" id="g10"></td><td><input class="parse-field" id="p10"></td><td><input class="parse-field" id="rt10"></td><td><input class="parse-field" id="t10"></td>
    <td><button class="reveal-btn" onclick="toggle('r10')">▶ Answer</button></td></tr>
  <tr class="answer-row" id="r10"><td colspan="8"><strong>Piel · Imperfect · 3ms · דבר · "he will speak"</strong> — יְ prefix + patach + dagesh in ב + tsere</td></tr>

  <tr><td>11</td><td><span class="heb">יִדְבַּר</span></td>
    <td><input class="parse-field" id="s11"></td><td><input class="parse-field" id="g11"></td><td><input class="parse-field" id="p11"></td><td><input class="parse-field" id="rt11"></td><td><input class="parse-field" id="t11"></td>
    <td><button class="reveal-btn" onclick="toggle('r11')">▶ Answer</button></td></tr>
  <tr class="answer-row" id="r11"><td colspan="8"><strong>Qal · Imperfect · 3ms · דבר · "he will speak" (rare)</strong> — יִ prefix (hiriq) + shewa under ד + patach; no dagesh in ב</td></tr>

  <tr><td>12</td><td><span class="heb">יְדֻבַּר</span></td>
    <td><input class="parse-field" id="s12"></td><td><input class="parse-field" id="g12"></td><td><input class="parse-field" id="p12"></td><td><input class="parse-field" id="rt12"></td><td><input class="parse-field" id="t12"></td>
    <td><button class="reveal-btn" onclick="toggle('r12')">▶ Answer</button></td></tr>
  <tr class="answer-row" id="r12"><td colspan="8"><strong>Pual · Imperfect · 3ms · דבר · "it will be spoken"</strong> — יְ prefix + qibbuts under ד + dagesh in ב</td></tr>

  <tr><td>13</td><td><span class="heb">יְשַׁלַּח</span></td>
    <td><input class="parse-field" id="s13"></td><td><input class="parse-field" id="g13"></td><td><input class="parse-field" id="p13"></td><td><input class="parse-field" id="rt13"></td><td><input class="parse-field" id="t13"></td>
    <td><button class="reveal-btn" onclick="toggle('r13')">▶ Answer</button></td></tr>
  <tr class="answer-row" id="r13"><td colspan="8"><strong>Piel · Imperfect · 3ms · שׁלח · "he will send away"</strong> — יְ prefix + patach + dagesh in ל; characteristic Piel imperfect</td></tr>

  <tr><td>14</td><td><span class="heb">יִשְׁלַח</span></td>
    <td><input class="parse-field" id="s14"></td><td><input class="parse-field" id="g14"></td><td><input class="parse-field" id="p14"></td><td><input class="parse-field" id="rt14"></td><td><input class="parse-field" id="t14"></td>
    <td><button class="reveal-btn" onclick="toggle('r14')">▶ Answer</button></td></tr>
  <tr class="answer-row" id="r14"><td colspan="8"><strong>Qal · Imperfect · 3ms · שׁלח · "he will send"</strong> — יִ prefix + shewa under שׁ + patach; no dagesh in ל</td></tr>

  <tr><td>15</td><td><span class="heb">יְשֻׁלַּח</span></td>
    <td><input class="parse-field" id="s15"></td><td><input class="parse-field" id="g15"></td><td><input class="parse-field" id="p15"></td><td><input class="parse-field" id="rt15"></td><td><input class="parse-field" id="t15"></td>
    <td><button class="reveal-btn" onclick="toggle('r15')">▶ Answer</button></td></tr>
  <tr class="answer-row" id="r15"><td colspan="8"><strong>Pual · Imperfect · 3ms · שׁלח · "he will be sent"</strong> — יְ prefix + qibbuts under שׁ + dagesh in ל</td></tr>

  <tr><td>16</td><td><span class="heb">וַיְדַבֵּר</span></td>
    <td><input class="parse-field" id="s16"></td><td><input class="parse-field" id="g16"></td><td><input class="parse-field" id="p16"></td><td><input class="parse-field" id="rt16"></td><td><input class="parse-field" id="t16"></td>
    <td><button class="reveal-btn" onclick="toggle('r16')">▶ Answer</button></td></tr>
  <tr class="answer-row" id="r16"><td colspan="8"><strong>Piel · Wayyiqtol · 3ms · דבר · "and he spoke"</strong> — וַ + יְ prefix + patach + dagesh in ב; same stem markers as imperfect</td></tr>

  <tr><td>17</td><td><span class="heb">וַיִּדְבַּר</span></td>
    <td><input class="parse-field" id="s17"></td><td><input class="parse-field" id="g17"></td><td><input class="parse-field" id="p17"></td><td><input class="parse-field" id="rt17"></td><td><input class="parse-field" id="t17"></td>
    <td><button class="reveal-btn" onclick="toggle('r17')">▶ Answer</button></td></tr>
  <tr class="answer-row" id="r17"><td colspan="8"><strong>Qal · Wayyiqtol · 3ms · דבר · "and he spoke" (rare)</strong> — וַיִּ (dagesh forte in י = wayyiqtol marker) + shewa + patach; no dagesh in ב</td></tr>

  <tr><td>18</td><td><span class="heb">וַיְדֻבַּר</span></td>
    <td><input class="parse-field" id="s18"></td><td><input class="parse-field" id="g18"></td><td><input class="parse-field" id="p18"></td><td><input class="parse-field" id="rt18"></td><td><input class="parse-field" id="t18"></td>
    <td><button class="reveal-btn" onclick="toggle('r18')">▶ Answer</button></td></tr>
  <tr class="answer-row" id="r18"><td colspan="8"><strong>Pual · Wayyiqtol · 3ms · דבר · "and it was spoken"</strong> — וַ + יְ prefix + qibbuts under ד + dagesh in ב</td></tr>

  <tr><td>19</td><td><span class="heb">דַּבֵּר</span></td>
    <td><input class="parse-field" id="s19"></td><td><input class="parse-field" id="g19"></td><td><input class="parse-field" id="p19"></td><td><input class="parse-field" id="rt19"></td><td><input class="parse-field" id="t19"></td>
    <td><button class="reveal-btn" onclick="toggle('r19')">▶ Answer</button></td></tr>
  <tr class="answer-row" id="r19"><td colspan="8"><strong>Piel · Imperative · 2ms · דבר · "speak!"</strong> — dagesh forte in ב + tsere; characteristic Piel imperative pattern</td></tr>

  <tr><td>20</td><td><span class="heb">דְּבַר</span></td>
    <td><input class="parse-field" id="s20"></td><td><input class="parse-field" id="g20"></td><td><input class="parse-field" id="p20"></td><td><input class="parse-field" id="rt20"></td><td><input class="parse-field" id="t20"></td>
    <td><button class="reveal-btn" onclick="toggle('r20')">▶ Answer</button></td></tr>
  <tr class="answer-row" id="r20"><td colspan="8"><strong>Qal · Imperative · 2ms · דבר · "speak!" (rare)</strong> — shewa under ד + patach under ב; no dagesh; plain Qal imperative</td></tr>

  <tr><td>21</td><td><span class="heb">מְדַבֵּר</span></td>
    <td><input class="parse-field" id="s21"></td><td><input class="parse-field" id="g21"></td><td><input class="parse-field" id="p21"></td><td><input class="parse-field" id="rt21"></td><td><input class="parse-field" id="t21"></td>
    <td><button class="reveal-btn" onclick="toggle('r21')">▶ Answer</button></td></tr>
  <tr class="answer-row" id="r21"><td colspan="8"><strong>Piel · Participle · ms · דבר · "speaking / one who speaks"</strong> — מְ prefix + patach under ד + dagesh in ב + tsere</td></tr>

  <tr><td>22</td><td><span class="heb">דֹּבֵר</span></td>
    <td><input class="parse-field" id="s22"></td><td><input class="parse-field" id="g22"></td><td><input class="parse-field" id="p22"></td><td><input class="parse-field" id="rt22"></td><td><input class="parse-field" id="t22"></td>
    <td><button class="reveal-btn" onclick="toggle('r22')">▶ Answer</button></td></tr>
  <tr class="answer-row" id="r22"><td colspan="8"><strong>Qal · Participle · ms · דבר · "speaking / one who speaks"</strong> — holem under ד (Qal active ptcp pattern) + tsere; no prefix מ, no dagesh in ב</td></tr>

  <tr><td>23</td><td><span class="heb">מְדֻבָּר</span></td>
    <td><input class="parse-field" id="s23"></td><td><input class="parse-field" id="g23"></td><td><input class="parse-field" id="p23"></td><td><input class="parse-field" id="rt23"></td><td><input class="parse-field" id="t23"></td>
    <td><button class="reveal-btn" onclick="toggle('r23')">▶ Answer</button></td></tr>
  <tr class="answer-row" id="r23"><td colspan="8"><strong>Pual · Participle · ms · דבר · "being spoken / what is spoken"</strong> — מְ prefix + qibbuts under ד + dagesh + qamets in ב</td></tr>

  <tr><td>24</td><td><span class="heb">סֻפַּר</span></td>
    <td><input class="parse-field" id="s24"></td><td><input class="parse-field" id="g24"></td><td><input class="parse-field" id="p24"></td><td><input class="parse-field" id="rt24"></td><td><input class="parse-field" id="t24"></td>
    <td><button class="reveal-btn" onclick="toggle('r24')">▶ Answer</button></td></tr>
  <tr class="answer-row" id="r24"><td colspan="8"><strong>Pual · Perfect · 3ms · ספר · "it was told / recounted"</strong> — qibbuts under ס + dagesh forte in פ + patach; confirm pattern from new root</td></tr>

</table>

<script>
function toggle(id) {
  var row = document.getElementById(id);
  row.style.display = (row.style.display === 'table-row') ? 'none' : 'table-row';
}
function showAll() {
  document.querySelectorAll('.answer-row').forEach(function(r){ r.style.display = 'table-row'; });
}
function hideAll() {
  document.querySelectorAll('.answer-row').forEach(function(r){ r.style.display = 'none'; });
}
function clearAll() {
  document.querySelectorAll('input.parse-field').forEach(function(i){ i.value = ''; });
}
</script>

