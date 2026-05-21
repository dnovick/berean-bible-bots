# Function Sort

*Chapter 32 — Pual Strong*

[Full screen](ch32-function-sort.html){.md-button}  [Markdown](ch32-function-sort.md){.md-button}  [Print (PDF)](ch32-function-sort.pdf){.md-button}

<style>

  body { font-family: Georgia, serif;    color: #222; }
  h1 { font-size: 1.4em; border-bottom: 2px solid #444; padding-bottom: .4em; }
  h2 { font-size: 1.15em; margin-top: 2em; color: #444; }
  .subtitle { color: #666; font-style: italic; margin-top: -.3em; }
  table { border-collapse: collapse;  margin: 1em 0; }
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
  .note { background: #f0f4ff; border-left: 4px solid #2a4a6e; padding: .6em 1em; margin: 1em 0; font-size: .88em; }
  @media print {
    button, .controls { display: none !important; }
    input.parse-field { border: none; border-bottom: 1px solid #000; background: transparent; }
    .answer-row { display: table-row !important; }
  }

</style>

<h1>Chapter 32 — Pual Function Sort</h1>
<p class="subtitle">BBH Chapter 32 · Pual Strong Verbs</p>

<p>The Pual is <strong>always</strong> the passive of the Piel. For each of the 20 Pual forms: (1) give the <strong>Piel active meaning</strong>; (2) translate the <strong>Pual passive form</strong>.</p>

<div class="tip"><strong>Pual diagnostic:</strong> Qibbuts (ֻ) or holem (ֹ) under R1 + Dagesh Forte in R2.<br>
Note: When R2 is a guttural (ר, ח, ע, etc.), dagesh forte is rejected and the preceding vowel lengthens — qibbuts → holem (e.g., בֹּרַךְ not בֻּרַּךְ).</div>

<div class="controls">
  <button onclick="showAll()">Show All Answers</button>
  <button onclick="hideAll()">Hide All Answers</button>
  <button onclick="clearAll()">Clear All Inputs</button>
</div>

<div style="overflow-x:auto;max-width:100%;"><table>
  <tr>
    <th>#</th><th>Form</th><th>Root</th><th>Conjugation</th><th>Piel Active Meaning</th><th>Pual Passive Translation</th><th></th>
  </tr>

  <tr>
    <td>1</td><td><span class="heb">קֻטַּל</span></td><td><span class="heb">קטל</span></td><td>Perfect 3ms</td>
    <td><input class="parse-field" id="i1a"></td>
    <td><input class="parse-field" id="i1b"></td>
    <td><button class="reveal-btn" onclick="toggle('r1')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r1"><td colspan="7"><strong>Piel active:</strong> to kill (intensively) &nbsp;|&nbsp; <strong>Pual passive:</strong> he was killed &nbsp;·&nbsp; <em>Paradigm form; qibbuts under ק + dagesh in ט</em></td></tr>

  <tr>
    <td>2</td><td><span class="heb">כֻּבַּד</span></td><td><span class="heb">כבד</span></td><td>Perfect 3ms</td>
    <td><input class="parse-field" id="i2a"></td>
    <td><input class="parse-field" id="i2b"></td>
    <td><button class="reveal-btn" onclick="toggle('r2')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r2"><td colspan="7"><strong>Piel active:</strong> to honor &nbsp;|&nbsp; <strong>Pual passive:</strong> he was honored &nbsp;·&nbsp; <em>Qibbuts under כ + dagesh in ב</em></td></tr>

  <tr>
    <td>3</td><td><span class="heb">בֹּרַךְ</span></td><td><span class="heb">ברך</span></td><td>Perfect 3ms</td>
    <td><input class="parse-field" id="i3a"></td>
    <td><input class="parse-field" id="i3b"></td>
    <td><button class="reveal-btn" onclick="toggle('r3')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r3"><td colspan="7"><strong>Piel active:</strong> to bless &nbsp;|&nbsp; <strong>Pual passive:</strong> he was blessed &nbsp;·&nbsp; <em>ר rejects dagesh; qibbuts lengthens to holem → בֹּרַךְ</em></td></tr>

  <tr>
    <td>4</td><td><span class="heb">שֻׁלַּח</span></td><td><span class="heb">שׁלח</span></td><td>Perfect 3ms</td>
    <td><input class="parse-field" id="i4a"></td>
    <td><input class="parse-field" id="i4b"></td>
    <td><button class="reveal-btn" onclick="toggle('r4')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r4"><td colspan="7"><strong>Piel active:</strong> to send away / release &nbsp;|&nbsp; <strong>Pual passive:</strong> he was sent away &nbsp;·&nbsp; <em>Qibbuts under שׁ + dagesh in ל</em></td></tr>

  <tr>
    <td>5</td><td><span class="heb">דֻּבַּר</span></td><td><span class="heb">דבר</span></td><td>Perfect 3ms</td>
    <td><input class="parse-field" id="i5a"></td>
    <td><input class="parse-field" id="i5b"></td>
    <td><button class="reveal-btn" onclick="toggle('r5')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r5"><td colspan="7"><strong>Piel active:</strong> to speak &nbsp;|&nbsp; <strong>Pual passive:</strong> it was spoken &nbsp;·&nbsp; <em>Qibbuts under ד + dagesh in ב; ר at end = no issue</em></td></tr>

  <tr>
    <td>6</td><td><span class="heb">שֻׁמַּר</span></td><td><span class="heb">שׁמר</span></td><td>Perfect 3ms</td>
    <td><input class="parse-field" id="i6a"></td>
    <td><input class="parse-field" id="i6b"></td>
    <td><button class="reveal-btn" onclick="toggle('r6')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r6"><td colspan="7"><strong>Piel active:</strong> to guard / watch &nbsp;|&nbsp; <strong>Pual passive:</strong> he was guarded &nbsp;·&nbsp; <em>Qibbuts under שׁ + dagesh in מ</em></td></tr>

  <tr>
    <td>7</td><td><span class="heb">גֹּרַשׁ</span></td><td><span class="heb">גרשׁ</span></td><td>Perfect 3ms</td>
    <td><input class="parse-field" id="i7a"></td>
    <td><input class="parse-field" id="i7b"></td>
    <td><button class="reveal-btn" onclick="toggle('r7')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r7"><td colspan="7"><strong>Piel active:</strong> to drive out / expel &nbsp;|&nbsp; <strong>Pual passive:</strong> he was driven out &nbsp;·&nbsp; <em>ר rejects dagesh; qibbuts lengthens to holem → גֹּרַשׁ</em></td></tr>

  <tr>
    <td>8</td><td><span class="heb">סֻפַּר</span></td><td><span class="heb">ספר</span></td><td>Perfect 3ms</td>
    <td><input class="parse-field" id="i8a"></td>
    <td><input class="parse-field" id="i8b"></td>
    <td><button class="reveal-btn" onclick="toggle('r8')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r8"><td colspan="7"><strong>Piel active:</strong> to recount / tell &nbsp;|&nbsp; <strong>Pual passive:</strong> it was told / recounted &nbsp;·&nbsp; <em>Qibbuts under ס + dagesh in פ</em></td></tr>

  <tr>
    <td>9</td><td><span class="heb">כֻּסָּה</span></td><td><span class="heb">כסה</span></td><td>Perfect 3ms</td>
    <td><input class="parse-field" id="i9a"></td>
    <td><input class="parse-field" id="i9b"></td>
    <td><button class="reveal-btn" onclick="toggle('r9')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r9"><td colspan="7"><strong>Piel active:</strong> to cover &nbsp;|&nbsp; <strong>Pual passive:</strong> it was covered &nbsp;·&nbsp; <em>III-ה root; qibbuts under כ + dagesh in ס; final ה quiesces</em></td></tr>

  <tr>
    <td>10</td><td><span class="heb">יְקֻטַּל</span></td><td><span class="heb">קטל</span></td><td>Imperfect 3ms</td>
    <td><input class="parse-field" id="i10a"></td>
    <td><input class="parse-field" id="i10b"></td>
    <td><button class="reveal-btn" onclick="toggle('r10')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r10"><td colspan="7"><strong>Piel active:</strong> to kill &nbsp;|&nbsp; <strong>Pual passive:</strong> he will be killed &nbsp;·&nbsp; <em>Pual imperfect prefix יְ + qibbuts under R1 + dagesh in R2</em></td></tr>

  <tr>
    <td>11</td><td><span class="heb">יְבֹרַךְ</span></td><td><span class="heb">ברך</span></td><td>Imperfect 3ms</td>
    <td><input class="parse-field" id="i11a"></td>
    <td><input class="parse-field" id="i11b"></td>
    <td><button class="reveal-btn" onclick="toggle('r11')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r11"><td colspan="7"><strong>Piel active:</strong> to bless &nbsp;|&nbsp; <strong>Pual passive:</strong> he will be blessed &nbsp;·&nbsp; <em>ר rejects dagesh; holem under ב in imperfect</em></td></tr>

  <tr>
    <td>12</td><td><span class="heb">יְשֻׁלַּח</span></td><td><span class="heb">שׁלח</span></td><td>Imperfect 3ms</td>
    <td><input class="parse-field" id="i12a"></td>
    <td><input class="parse-field" id="i12b"></td>
    <td><button class="reveal-btn" onclick="toggle('r12')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r12"><td colspan="7"><strong>Piel active:</strong> to send / release &nbsp;|&nbsp; <strong>Pual passive:</strong> he will be sent &nbsp;·&nbsp; <em>Prefix יְ + qibbuts under שׁ + dagesh in ל</em></td></tr>

  <tr>
    <td>13</td><td><span class="heb">יְכֻבַּד</span></td><td><span class="heb">כבד</span></td><td>Imperfect 3ms</td>
    <td><input class="parse-field" id="i13a"></td>
    <td><input class="parse-field" id="i13b"></td>
    <td><button class="reveal-btn" onclick="toggle('r13')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r13"><td colspan="7"><strong>Piel active:</strong> to honor &nbsp;|&nbsp; <strong>Pual passive:</strong> he will be honored &nbsp;·&nbsp; <em>Prefix יְ + qibbuts under כ + dagesh in ב</em></td></tr>

  <tr>
    <td>14</td><td><span class="heb">יְסֻפַּר</span></td><td><span class="heb">ספר</span></td><td>Imperfect 3ms</td>
    <td><input class="parse-field" id="i14a"></td>
    <td><input class="parse-field" id="i14b"></td>
    <td><button class="reveal-btn" onclick="toggle('r14')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r14"><td colspan="7"><strong>Piel active:</strong> to recount / tell &nbsp;|&nbsp; <strong>Pual passive:</strong> it will be told &nbsp;·&nbsp; <em>Prefix יְ + qibbuts under ס + dagesh in פ</em></td></tr>

  <tr>
    <td>15</td><td><span class="heb">יְגֹרַשׁ</span></td><td><span class="heb">גרשׁ</span></td><td>Imperfect 3ms</td>
    <td><input class="parse-field" id="i15a"></td>
    <td><input class="parse-field" id="i15b"></td>
    <td><button class="reveal-btn" onclick="toggle('r15')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r15"><td colspan="7"><strong>Piel active:</strong> to drive out &nbsp;|&nbsp; <strong>Pual passive:</strong> he will be driven out &nbsp;·&nbsp; <em>ר rejects dagesh; holem under ג in imperfect</em></td></tr>

  <tr>
    <td>16</td><td><span class="heb">מְקֻטָּל</span></td><td><span class="heb">קטל</span></td><td>Participle ms</td>
    <td><input class="parse-field" id="i16a"></td>
    <td><input class="parse-field" id="i16b"></td>
    <td><button class="reveal-btn" onclick="toggle('r16')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r16"><td colspan="7"><strong>Piel active:</strong> to kill &nbsp;|&nbsp; <strong>Pual passive:</strong> one being killed &nbsp;·&nbsp; <em>Pual participle: מְ prefix + qibbuts under R1 + qamets under R2</em></td></tr>

  <tr>
    <td>17</td><td><span class="heb">מְבֹרָךְ</span></td><td><span class="heb">ברך</span></td><td>Participle ms</td>
    <td><input class="parse-field" id="i17a"></td>
    <td><input class="parse-field" id="i17b"></td>
    <td><button class="reveal-btn" onclick="toggle('r17')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r17"><td colspan="7"><strong>Piel active:</strong> to bless &nbsp;|&nbsp; <strong>Pual passive:</strong> one being blessed &nbsp;·&nbsp; <em>ר rejects dagesh; holem under ב; qamets under ר</em></td></tr>

  <tr>
    <td>18</td><td><span class="heb">מְשֻׁלָּח</span></td><td><span class="heb">שׁלח</span></td><td>Participle ms</td>
    <td><input class="parse-field" id="i18a"></td>
    <td><input class="parse-field" id="i18b"></td>
    <td><button class="reveal-btn" onclick="toggle('r18')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r18"><td colspan="7"><strong>Piel active:</strong> to send / release &nbsp;|&nbsp; <strong>Pual passive:</strong> one being sent &nbsp;·&nbsp; <em>מְ prefix + qibbuts under שׁ + dagesh + qamets in ל</em></td></tr>

  <tr>
    <td>19</td><td><span class="heb">כֻּבְּדוּ</span></td><td><span class="heb">כבד</span></td><td>Perfect 3cp</td>
    <td><input class="parse-field" id="i19a"></td>
    <td><input class="parse-field" id="i19b"></td>
    <td><button class="reveal-btn" onclick="toggle('r19')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r19"><td colspan="7"><strong>Piel active:</strong> to honor &nbsp;|&nbsp; <strong>Pual passive:</strong> they were honored &nbsp;·&nbsp; <em>3cp suffix וּ; shewa under ב (vowel reduces before vocalic suffix)</em></td></tr>

  <tr>
    <td>20</td><td><span class="heb">שֻׁלְּחוּ</span></td><td><span class="heb">שׁלח</span></td><td>Perfect 3cp</td>
    <td><input class="parse-field" id="i20a"></td>
    <td><input class="parse-field" id="i20b"></td>
    <td><button class="reveal-btn" onclick="toggle('r20')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r20"><td colspan="7"><strong>Piel active:</strong> to send away &nbsp;|&nbsp; <strong>Pual passive:</strong> they were sent away &nbsp;·&nbsp; <em>3cp suffix וּ; shewa under ל before vocalic suffix</em></td></tr>

</table></div>

<div class="note">
  <strong>Pattern summary:</strong><br>
  Perfect 3ms: qibbuts/holem under R1 + dagesh + patach in R2 (e.g., קֻטַּל, בֹּרַךְ)<br>
  Imperfect 3ms: יְ prefix + same pattern (e.g., יְקֻטַּל, יְבֹרַךְ)<br>
  Participle ms: מְ prefix + qibbuts/holem under R1 + dagesh + qamets in R2 (e.g., מְקֻטָּל, מְבֹרָךְ)<br>
  Perfect 3cp: qibbuts under R1 + shewa in R2 + וּ suffix (e.g., כֻּבְּדוּ, שֻׁלְּחוּ)
</div>

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

