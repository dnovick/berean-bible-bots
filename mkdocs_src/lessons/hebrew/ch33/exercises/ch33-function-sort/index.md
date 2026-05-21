# Function Sort

*Chapter 33 — Pual Weak*

[Full screen](ch33-function-sort.html){.md-button}  [Markdown](ch33-function-sort.md){.md-button}  [Print (PDF)](ch33-function-sort.pdf){.md-button}

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

<h1>Chapter 33 — Pual Function Sort (Weak Roots)</h1>
<p class="subtitle">BBH Chapter 33 · Pual Weak Verbs</p>

<p>The Pual is <strong>always</strong> the passive of the Piel. For each of the 18 weak-root Pual forms: (1) give the <strong>Piel active meaning</strong>; (2) translate the <strong>Pual passive form</strong>.</p>

<div class="tip">
  <strong>III-ה endings:</strong>
  Perfect 3ms: <span class="heb">ָּה</span> (qamets-heh, e.g., גֻּלָּה) ·
  Imperfect 3ms: <span class="heb">ֶּה</span> (tsere-heh, e.g., יְגֻלֶּה) ·
  Participle ms: <span class="heb">ֶּה</span> (e.g., מְגֻלֶּה)<br>
  <strong>ברך (R2 = ר):</strong> ר rejects dagesh forte → qibbuts lengthens to holem (בֹּרַךְ, יְבֹרַךְ, מְבֹרָךְ)
</div>

<div class="controls">
  <button onclick="showAll()">Show All Answers</button>
  <button onclick="hideAll()">Hide All Answers</button>
  <button onclick="clearAll()">Clear All Inputs</button>
</div>

<div style="overflow-x:auto;max-width:100%;"><table>
  <tr>
    <th>#</th><th>Form</th><th>Root</th><th>Weak Type</th><th>Conjugation</th><th>Piel Active Meaning</th><th>Pual Passive Translation</th><th></th>
  </tr>

  <tr>
    <td>1</td><td><span class="heb">גֻּלָּה</span></td><td><span class="heb">גלה</span></td><td>III-ה</td><td>Perfect 3ms</td>
    <td><input class="parse-field" id="i1a"></td>
    <td><input class="parse-field" id="i1b"></td>
    <td><button class="reveal-btn" onclick="toggle('r1')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r1"><td colspan="8"><strong>Piel active:</strong> to reveal / uncover &nbsp;|&nbsp; <strong>Pual passive:</strong> it was revealed &nbsp;·&nbsp; <em>Qibbuts under ג + dagesh in ל + final ָּה (III-ה pattern)</em></td></tr>

  <tr>
    <td>2</td><td><span class="heb">כֻּלָּה</span></td><td><span class="heb">כלה</span></td><td>III-ה</td><td>Perfect 3ms</td>
    <td><input class="parse-field" id="i2a"></td>
    <td><input class="parse-field" id="i2b"></td>
    <td><button class="reveal-btn" onclick="toggle('r2')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r2"><td colspan="8"><strong>Piel active:</strong> to complete / destroy &nbsp;|&nbsp; <strong>Pual passive:</strong> it was finished / consumed &nbsp;·&nbsp; <em>Qibbuts under כ + dagesh in ל + final ָּה</em></td></tr>

  <tr>
    <td>3</td><td><span class="heb">בֹּרַךְ</span></td><td><span class="heb">ברך</span></td><td>R2 = ר</td><td>Perfect 3ms</td>
    <td><input class="parse-field" id="i3a"></td>
    <td><input class="parse-field" id="i3b"></td>
    <td><button class="reveal-btn" onclick="toggle('r3')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r3"><td colspan="8"><strong>Piel active:</strong> to bless &nbsp;|&nbsp; <strong>Pual passive:</strong> he was blessed &nbsp;·&nbsp; <em>Holem under ב (qibbuts lengthened; ר rejects dagesh) + patach under ר</em></td></tr>

  <tr>
    <td>4</td><td><span class="heb">עֻנָּה</span></td><td><span class="heb">ענה</span></td><td>III-ה, I-gutt</td><td>Perfect 3ms</td>
    <td><input class="parse-field" id="i4a"></td>
    <td><input class="parse-field" id="i4b"></td>
    <td><button class="reveal-btn" onclick="toggle('r4')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r4"><td colspan="8"><strong>Piel active:</strong> to afflict / humble &nbsp;|&nbsp; <strong>Pual passive:</strong> he was afflicted &nbsp;·&nbsp; <em>Qibbuts under ע (guttural accepts qibbuts) + dagesh in ן + final ָּה</em></td></tr>

  <tr>
    <td>5</td><td><span class="heb">חֻיָּה</span></td><td><span class="heb">חיה</span></td><td>III-ה</td><td>Perfect 3ms</td>
    <td><input class="parse-field" id="i5a"></td>
    <td><input class="parse-field" id="i5b"></td>
    <td><button class="reveal-btn" onclick="toggle('r5')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r5"><td colspan="8"><strong>Piel active:</strong> to keep alive &nbsp;|&nbsp; <strong>Pual passive:</strong> he was kept alive &nbsp;·&nbsp; <em>Qibbuts under ח + dagesh forte in י + final ָּה</em></td></tr>

  <tr>
    <td>6</td><td><span class="heb">יְגֻלֶּה</span></td><td><span class="heb">גלה</span></td><td>III-ה</td><td>Imperfect 3ms</td>
    <td><input class="parse-field" id="i6a"></td>
    <td><input class="parse-field" id="i6b"></td>
    <td><button class="reveal-btn" onclick="toggle('r6')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r6"><td colspan="8"><strong>Piel active:</strong> to reveal &nbsp;|&nbsp; <strong>Pual passive:</strong> it will be revealed &nbsp;·&nbsp; <em>Prefix יְ + qibbuts under ג + dagesh in ל + final ֶּה (imperfect III-ה ending)</em></td></tr>

  <tr>
    <td>7</td><td><span class="heb">יְכֻלֶּה</span></td><td><span class="heb">כלה</span></td><td>III-ה</td><td>Imperfect 3ms</td>
    <td><input class="parse-field" id="i7a"></td>
    <td><input class="parse-field" id="i7b"></td>
    <td><button class="reveal-btn" onclick="toggle('r7')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r7"><td colspan="8"><strong>Piel active:</strong> to complete / destroy &nbsp;|&nbsp; <strong>Pual passive:</strong> it will be finished &nbsp;·&nbsp; <em>Prefix יְ + qibbuts under כ + dagesh in ל + final ֶּה</em></td></tr>

  <tr>
    <td>8</td><td><span class="heb">יְבֹרַךְ</span></td><td><span class="heb">ברך</span></td><td>R2 = ר</td><td>Imperfect 3ms</td>
    <td><input class="parse-field" id="i8a"></td>
    <td><input class="parse-field" id="i8b"></td>
    <td><button class="reveal-btn" onclick="toggle('r8')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r8"><td colspan="8"><strong>Piel active:</strong> to bless &nbsp;|&nbsp; <strong>Pual passive:</strong> he will be blessed &nbsp;·&nbsp; <em>Prefix יְ + holem under ב (ר rejects dagesh) + patach under ר</em></td></tr>

  <tr>
    <td>9</td><td><span class="heb">יְעֻנֶּה</span></td><td><span class="heb">ענה</span></td><td>III-ה, I-gutt</td><td>Imperfect 3ms</td>
    <td><input class="parse-field" id="i9a"></td>
    <td><input class="parse-field" id="i9b"></td>
    <td><button class="reveal-btn" onclick="toggle('r9')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r9"><td colspan="8"><strong>Piel active:</strong> to afflict &nbsp;|&nbsp; <strong>Pual passive:</strong> he will be afflicted &nbsp;·&nbsp; <em>Prefix יְ + qibbuts under ע + dagesh in ן + final ֶּה</em></td></tr>

  <tr>
    <td>10</td><td><span class="heb">יְחֻיֶּה</span></td><td><span class="heb">חיה</span></td><td>III-ה</td><td>Imperfect 3ms</td>
    <td><input class="parse-field" id="i10a"></td>
    <td><input class="parse-field" id="i10b"></td>
    <td><button class="reveal-btn" onclick="toggle('r10')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r10"><td colspan="8"><strong>Piel active:</strong> to keep alive &nbsp;|&nbsp; <strong>Pual passive:</strong> he will be kept alive &nbsp;·&nbsp; <em>Prefix יְ + qibbuts under ח + dagesh in י + final ֶּה</em></td></tr>

  <tr>
    <td>11</td><td><span class="heb">מְגֻלֶּה</span></td><td><span class="heb">גלה</span></td><td>III-ה</td><td>Participle ms</td>
    <td><input class="parse-field" id="i11a"></td>
    <td><input class="parse-field" id="i11b"></td>
    <td><button class="reveal-btn" onclick="toggle('r11')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r11"><td colspan="8"><strong>Piel active:</strong> to reveal &nbsp;|&nbsp; <strong>Pual passive:</strong> one being revealed &nbsp;·&nbsp; <em>Prefix מְ + qibbuts under ג + dagesh in ל + final ֶּה (Pual participle III-ה)</em></td></tr>

  <tr>
    <td>12</td><td><span class="heb">מְכֻלֶּה</span></td><td><span class="heb">כלה</span></td><td>III-ה</td><td>Participle ms</td>
    <td><input class="parse-field" id="i12a"></td>
    <td><input class="parse-field" id="i12b"></td>
    <td><button class="reveal-btn" onclick="toggle('r12')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r12"><td colspan="8"><strong>Piel active:</strong> to complete / destroy &nbsp;|&nbsp; <strong>Pual passive:</strong> one being consumed &nbsp;·&nbsp; <em>Prefix מְ + qibbuts under כ + dagesh in ל + final ֶּה</em></td></tr>

  <tr>
    <td>13</td><td><span class="heb">מְבֹרָךְ</span></td><td><span class="heb">ברך</span></td><td>R2 = ר</td><td>Participle ms</td>
    <td><input class="parse-field" id="i13a"></td>
    <td><input class="parse-field" id="i13b"></td>
    <td><button class="reveal-btn" onclick="toggle('r13')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r13"><td colspan="8"><strong>Piel active:</strong> to bless &nbsp;|&nbsp; <strong>Pual passive:</strong> one being blessed &nbsp;·&nbsp; <em>Prefix מְ + holem under ב (ר rejects dagesh) + qamets under ר (participle theme vowel)</em></td></tr>

  <tr>
    <td>14</td><td><span class="heb">גֻּלְתָּה</span></td><td><span class="heb">גלה</span></td><td>III-ה</td><td>Perfect 3fs</td>
    <td><input class="parse-field" id="i14a"></td>
    <td><input class="parse-field" id="i14b"></td>
    <td><button class="reveal-btn" onclick="toggle('r14')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r14"><td colspan="8"><strong>Piel active:</strong> to reveal &nbsp;|&nbsp; <strong>Pual passive:</strong> it was revealed (3fs) &nbsp;·&nbsp; <em>Qibbuts under ג + shewa under ל + תָּה suffix (3fs replaces the ָּה of 3ms)</em></td></tr>

  <tr>
    <td>15</td><td><span class="heb">בֹּרֲכוּ</span></td><td><span class="heb">ברך</span></td><td>R2 = ר</td><td>Perfect 3cp</td>
    <td><input class="parse-field" id="i15a"></td>
    <td><input class="parse-field" id="i15b"></td>
    <td><button class="reveal-btn" onclick="toggle('r15')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r15"><td colspan="8"><strong>Piel active:</strong> to bless &nbsp;|&nbsp; <strong>Pual passive:</strong> they were blessed &nbsp;·&nbsp; <em>Holem under ב + hateph-patach under ר (guttural reduced vowel before suffix) + וּ</em></td></tr>

  <tr>
    <td>16</td><td><span class="heb">כֻּלּוּ</span></td><td><span class="heb">כלה</span></td><td>III-ה</td><td>Perfect 3cp</td>
    <td><input class="parse-field" id="i16a"></td>
    <td><input class="parse-field" id="i16b"></td>
    <td><button class="reveal-btn" onclick="toggle('r16')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r16"><td colspan="8"><strong>Piel active:</strong> to complete / destroy &nbsp;|&nbsp; <strong>Pual passive:</strong> they were consumed / finished &nbsp;·&nbsp; <em>Qibbuts under כ + dagesh forte in ל + וּ suffix (III-ה 3cp: ָּה → וּ)</em></td></tr>

  <tr>
    <td>17</td><td><span class="heb">צֻוָּה</span></td><td><span class="heb">צוה</span></td><td>III-ה</td><td>Perfect 3ms</td>
    <td><input class="parse-field" id="i17a"></td>
    <td><input class="parse-field" id="i17b"></td>
    <td><button class="reveal-btn" onclick="toggle('r17')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r17"><td colspan="8"><strong>Piel active:</strong> to command &nbsp;|&nbsp; <strong>Pual passive:</strong> he was commanded &nbsp;·&nbsp; <em>Qibbuts under צ + dagesh forte in ו + final ָּה; III-ה Pual pattern with וו as R2</em></td></tr>

  <tr>
    <td>18</td><td><span class="heb">שֻׁנָּה</span></td><td><span class="heb">שׁנה</span></td><td>III-ה</td><td>Perfect 3ms</td>
    <td><input class="parse-field" id="i18a"></td>
    <td><input class="parse-field" id="i18b"></td>
    <td><button class="reveal-btn" onclick="toggle('r18')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r18"><td colspan="8"><strong>Piel active:</strong> to change &nbsp;|&nbsp; <strong>Pual passive:</strong> it was changed &nbsp;·&nbsp; <em>Qibbuts under שׁ + dagesh forte in ן + final ָּה; III-ה Pual perfect 3ms</em></td></tr>

</table></div>

<div class="note">
  <strong>Conjugation pattern review for III-ה Pual:</strong><br>
  Perfect 3ms: <span class="heb">גֻּלָּה</span> (qibbuts–R1 + dagesh–R2 + ָּה)<br>
  Perfect 3fs: <span class="heb">גֻּלְתָּה</span> (qibbuts–R1 + shewa–R2 + תָּה)<br>
  Perfect 3cp: <span class="heb">כֻּלּוּ</span> (qibbuts–R1 + dagesh–R2 + וּ)<br>
  Imperfect 3ms: <span class="heb">יְגֻלֶּה</span> (יְ + qibbuts–R1 + dagesh–R2 + ֶּה)<br>
  Participle ms: <span class="heb">מְגֻלֶּה</span> (מְ + qibbuts–R1 + dagesh–R2 + ֶּה)
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

