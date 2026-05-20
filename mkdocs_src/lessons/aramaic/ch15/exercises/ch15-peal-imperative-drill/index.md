# Peal Imperative Drill

*Chapter 15 — Peal Imperative*

[Full screen](ch15-peal-imperative-drill.html){.md-button}  [Markdown](ch15-peal-imperative-drill.md){.md-button}  [Print (PDF)](ch15-peal-imperative-drill.pdf){.md-button}

<style>

  body { font-family: Georgia, serif;    color: #222; }
  h1 { font-size: 1.4em; border-bottom: 2px solid #444; padding-bottom: 0.3em; }
  h2 { font-size: 1.1em; margin-top: 1.6em; }
  p, li { line-height: 1.6; }
  .subtitle { color: #555; font-style: italic; margin-top: 0.2em; }
  .controls { margin: 1.2em 0; display: flex; gap: 0.6em; flex-wrap: wrap; }
  button.ctrl {
    padding: 0.4em 1em; font-size: 0.88em; cursor: pointer;
    background: #f0f0f0; border: 1px solid #999; border-radius: 3px;
  }
  button.ctrl:hover { background: #ddd; }
  table { border-collapse: collapse; width: 100%; margin-top: 0.8em; font-size: 0.92em; }
  th { background: #3a3a5c; color: #fff; padding: 0.5em 0.6em; text-align: left; }
  td { padding: 0.45em 0.6em; border-bottom: 1px solid #ddd; vertical-align: middle; }
  tr:nth-child(even) td { background: #f8f8f8; }
  .hebrew { direction: rtl; unicode-bidi: embed; font-size: 1.22em; line-height: 1.8; font-weight: bold; }
  .root-ans { direction: rtl; unicode-bidi: embed; font-size: 1.1em; }
  input.parse-field {
    width: 100%; box-sizing: border-box; border: 1px solid #aaa;
    border-radius: 2px; padding: 0.2em 0.3em; font-size: 0.88em;
    font-family: Georgia, serif;
  }
  button.reveal-btn {
    padding: 0.2em 0.6em; font-size: 0.82em; cursor: pointer;
    background: #e8e8e8; border: 1px solid #999; border-radius: 3px;
    white-space: nowrap;
  }
  button.reveal-btn:hover { background: #ccc; }
  tr.answer-row td { background: #d4edda; font-size: 0.88em; color: #155724; }
  tr.answer-row { display: none; }
  tr.answer-row.visible { display: table-row; }
  .answer-label { font-weight: bold; margin-right: 0.3em; }
  .reflection { background: #f5f5e8; border-left: 4px solid #b8860b; padding: 0.8em 1.1em; margin: 1.4em 0; border-radius: 0 4px 4px 0; }
  .reflection h3 { margin-top: 0; font-size: 1em; }
  @media print {
    button.ctrl, button.reveal-btn { display: none; }
    input.parse-field { border: none; border-bottom: 1px solid #000; background: transparent; }
    tr.answer-row { display: none !important; }
    .controls { display: none; }
  }

</style>

<h1>Chapter 15 — Peal Imperative Parsing Drill</h1>
<p class="subtitle"><em>Basics of Biblical Aramaic</em>, Van Pelt — Ch15: Peal Imperative</p>

<h2>Instructions</h2>
<p>For each numbered verb form, enter the <strong>Root</strong> (3 consonants, Peal perfect 3ms), <strong>PGN</strong> (person / gender / number), and <strong>Translation</strong> in the input fields. Click <strong>&#9654; Answer</strong> to reveal the answer key row. Items 17–20 are negative imperative constructions (אַל / לָא + imperfect).</p>

<div class="controls">
  <button class="ctrl" onclick="showAll()">Show All Answers</button>
  <button class="ctrl" onclick="hideAll()">Hide All Answers</button>
  <button class="ctrl" onclick="clearAll()">Clear All Inputs</button>
</div>

<table id="drill-table">
  <thead>
    <tr>
      <th style="width:2.5em">#</th>
      <th style="width:16%">Form</th>
      <th style="width:18%">Root</th>
      <th style="width:18%">PGN</th>
      <th style="width:28%">Translation</th>
      <th style="width:5.5em"></th>
    </tr>
  </thead>
  <tbody>

    <!-- 1 -->
    <tr id="q1">
      <td>1</td>
      <td><div class="hebrew">קוּם</div></td>
      <td><input class="parse-field" placeholder="root…"></td>
      <td><input class="parse-field" placeholder="PGN…"></td>
      <td><input class="parse-field" placeholder="translation…"></td>
      <td><button class="reveal-btn" onclick="toggle('a1',this)">&#9654; Answer</button></td>
    </tr>
    <tr class="answer-row" id="a1">
      <td></td>
      <td colspan="4"><span class="answer-label">Root:</span> <span class="root-ans">קום</span> &nbsp;|&nbsp; <span class="answer-label">PGN:</span> 2ms &nbsp;|&nbsp; <span class="answer-label">Translation:</span> Arise! / Stand up!</td>
      <td></td>
    </tr>

    <!-- 2 -->
    <tr id="q2">
      <td>2</td>
      <td><div class="hebrew">אֱמַר</div></td>
      <td><input class="parse-field" placeholder="root…"></td>
      <td><input class="parse-field" placeholder="PGN…"></td>
      <td><input class="parse-field" placeholder="translation…"></td>
      <td><button class="reveal-btn" onclick="toggle('a2',this)">&#9654; Answer</button></td>
    </tr>
    <tr class="answer-row" id="a2">
      <td></td>
      <td colspan="4"><span class="answer-label">Root:</span> <span class="root-ans">אמר</span> &nbsp;|&nbsp; <span class="answer-label">PGN:</span> 2ms &nbsp;|&nbsp; <span class="answer-label">Translation:</span> Say! / Tell!</td>
      <td></td>
    </tr>

    <!-- 3 -->
    <tr id="q3">
      <td>3</td>
      <td><div class="hebrew">כְּתֻב</div></td>
      <td><input class="parse-field" placeholder="root…"></td>
      <td><input class="parse-field" placeholder="PGN…"></td>
      <td><input class="parse-field" placeholder="translation…"></td>
      <td><button class="reveal-btn" onclick="toggle('a3',this)">&#9654; Answer</button></td>
    </tr>
    <tr class="answer-row" id="a3">
      <td></td>
      <td colspan="4"><span class="answer-label">Root:</span> <span class="root-ans">כתב</span> &nbsp;|&nbsp; <span class="answer-label">PGN:</span> 2ms &nbsp;|&nbsp; <span class="answer-label">Translation:</span> Write!</td>
      <td></td>
    </tr>

    <!-- 4 -->
    <tr id="q4">
      <td>4</td>
      <td><div class="hebrew">שְׁלַח</div></td>
      <td><input class="parse-field" placeholder="root…"></td>
      <td><input class="parse-field" placeholder="PGN…"></td>
      <td><input class="parse-field" placeholder="translation…"></td>
      <td><button class="reveal-btn" onclick="toggle('a4',this)">&#9654; Answer</button></td>
    </tr>
    <tr class="answer-row" id="a4">
      <td></td>
      <td colspan="4"><span class="answer-label">Root:</span> <span class="root-ans">שׁלח</span> &nbsp;|&nbsp; <span class="answer-label">PGN:</span> 2ms &nbsp;|&nbsp; <span class="answer-label">Translation:</span> Send!</td>
      <td></td>
    </tr>

    <!-- 5 -->
    <tr id="q5">
      <td>5</td>
      <td><div class="hebrew">עֲבֵד</div></td>
      <td><input class="parse-field" placeholder="root…"></td>
      <td><input class="parse-field" placeholder="PGN…"></td>
      <td><input class="parse-field" placeholder="translation…"></td>
      <td><button class="reveal-btn" onclick="toggle('a5',this)">&#9654; Answer</button></td>
    </tr>
    <tr class="answer-row" id="a5">
      <td></td>
      <td colspan="4"><span class="answer-label">Root:</span> <span class="root-ans">עבד</span> &nbsp;|&nbsp; <span class="answer-label">PGN:</span> 2ms &nbsp;|&nbsp; <span class="answer-label">Translation:</span> Do! / Serve! / Make!</td>
      <td></td>
    </tr>

    <!-- 6 -->
    <tr id="q6">
      <td>6</td>
      <td><div class="hebrew">שְׁמַע</div></td>
      <td><input class="parse-field" placeholder="root…"></td>
      <td><input class="parse-field" placeholder="PGN…"></td>
      <td><input class="parse-field" placeholder="translation…"></td>
      <td><button class="reveal-btn" onclick="toggle('a6',this)">&#9654; Answer</button></td>
    </tr>
    <tr class="answer-row" id="a6">
      <td></td>
      <td colspan="4"><span class="answer-label">Root:</span> <span class="root-ans">שׁמע</span> &nbsp;|&nbsp; <span class="answer-label">PGN:</span> 2ms &nbsp;|&nbsp; <span class="answer-label">Translation:</span> Hear! / Listen!</td>
      <td></td>
    </tr>

    <!-- 7 -->
    <tr id="q7">
      <td>7</td>
      <td><div class="hebrew">הַב</div></td>
      <td><input class="parse-field" placeholder="root…"></td>
      <td><input class="parse-field" placeholder="PGN…"></td>
      <td><input class="parse-field" placeholder="translation…"></td>
      <td><button class="reveal-btn" onclick="toggle('a7',this)">&#9654; Answer</button></td>
    </tr>
    <tr class="answer-row" id="a7">
      <td></td>
      <td colspan="4"><span class="answer-label">Root:</span> <span class="root-ans">יהב</span> &nbsp;|&nbsp; <span class="answer-label">PGN:</span> 2ms &nbsp;|&nbsp; <span class="answer-label">Translation:</span> Give!</td>
      <td></td>
    </tr>

    <!-- 8 -->
    <tr id="q8">
      <td>8</td>
      <td><div class="hebrew">פְּרֻק</div></td>
      <td><input class="parse-field" placeholder="root…"></td>
      <td><input class="parse-field" placeholder="PGN…"></td>
      <td><input class="parse-field" placeholder="translation…"></td>
      <td><button class="reveal-btn" onclick="toggle('a8',this)">&#9654; Answer</button></td>
    </tr>
    <tr class="answer-row" id="a8">
      <td></td>
      <td colspan="4"><span class="answer-label">Root:</span> <span class="root-ans">פרק</span> &nbsp;|&nbsp; <span class="answer-label">PGN:</span> 2ms &nbsp;|&nbsp; <span class="answer-label">Translation:</span> Deliver! / Atone!</td>
      <td></td>
    </tr>

    <!-- 9 -->
    <tr id="q9">
      <td>9</td>
      <td><div class="hebrew">בְּנוֹ</div></td>
      <td><input class="parse-field" placeholder="root…"></td>
      <td><input class="parse-field" placeholder="PGN…"></td>
      <td><input class="parse-field" placeholder="translation…"></td>
      <td><button class="reveal-btn" onclick="toggle('a9',this)">&#9654; Answer</button></td>
    </tr>
    <tr class="answer-row" id="a9">
      <td></td>
      <td colspan="4"><span class="answer-label">Root:</span> <span class="root-ans">בנה</span> &nbsp;|&nbsp; <span class="answer-label">PGN:</span> 2mp &nbsp;|&nbsp; <span class="answer-label">Translation:</span> Build! (to men)</td>
      <td></td>
    </tr>

    <!-- 10 -->
    <tr id="q10">
      <td>10</td>
      <td><div class="hebrew">הָבוּ</div></td>
      <td><input class="parse-field" placeholder="root…"></td>
      <td><input class="parse-field" placeholder="PGN…"></td>
      <td><input class="parse-field" placeholder="translation…"></td>
      <td><button class="reveal-btn" onclick="toggle('a10',this)">&#9654; Answer</button></td>
    </tr>
    <tr class="answer-row" id="a10">
      <td></td>
      <td colspan="4"><span class="answer-label">Root:</span> <span class="root-ans">יהב</span> &nbsp;|&nbsp; <span class="answer-label">PGN:</span> 2mp &nbsp;|&nbsp; <span class="answer-label">Translation:</span> Give! (to men)</td>
      <td></td>
    </tr>

    <!-- 11 -->
    <tr id="q11">
      <td>11</td>
      <td><div class="hebrew">אֱמַרוּ</div></td>
      <td><input class="parse-field" placeholder="root…"></td>
      <td><input class="parse-field" placeholder="PGN…"></td>
      <td><input class="parse-field" placeholder="translation…"></td>
      <td><button class="reveal-btn" onclick="toggle('a11',this)">&#9654; Answer</button></td>
    </tr>
    <tr class="answer-row" id="a11">
      <td></td>
      <td colspan="4"><span class="answer-label">Root:</span> <span class="root-ans">אמר</span> &nbsp;|&nbsp; <span class="answer-label">PGN:</span> 2mp &nbsp;|&nbsp; <span class="answer-label">Translation:</span> Say! (to men)</td>
      <td></td>
    </tr>

    <!-- 12 -->
    <tr id="q12">
      <td>12</td>
      <td><div class="hebrew">שְׁמַעוּ</div></td>
      <td><input class="parse-field" placeholder="root…"></td>
      <td><input class="parse-field" placeholder="PGN…"></td>
      <td><input class="parse-field" placeholder="translation…"></td>
      <td><button class="reveal-btn" onclick="toggle('a12',this)">&#9654; Answer</button></td>
    </tr>
    <tr class="answer-row" id="a12">
      <td></td>
      <td colspan="4"><span class="answer-label">Root:</span> <span class="root-ans">שׁמע</span> &nbsp;|&nbsp; <span class="answer-label">PGN:</span> 2mp &nbsp;|&nbsp; <span class="answer-label">Translation:</span> Hear! (to men)</td>
      <td></td>
    </tr>

    <!-- 13 -->
    <tr id="q13">
      <td>13</td>
      <td><div class="hebrew">כְּתֻבִי</div></td>
      <td><input class="parse-field" placeholder="root…"></td>
      <td><input class="parse-field" placeholder="PGN…"></td>
      <td><input class="parse-field" placeholder="translation…"></td>
      <td><button class="reveal-btn" onclick="toggle('a13',this)">&#9654; Answer</button></td>
    </tr>
    <tr class="answer-row" id="a13">
      <td></td>
      <td colspan="4"><span class="answer-label">Root:</span> <span class="root-ans">כתב</span> &nbsp;|&nbsp; <span class="answer-label">PGN:</span> 2fs &nbsp;|&nbsp; <span class="answer-label">Translation:</span> Write! (to a woman)</td>
      <td></td>
    </tr>

    <!-- 14 -->
    <tr id="q14">
      <td>14</td>
      <td><div class="hebrew">שִׁלְחוּ</div></td>
      <td><input class="parse-field" placeholder="root…"></td>
      <td><input class="parse-field" placeholder="PGN…"></td>
      <td><input class="parse-field" placeholder="translation…"></td>
      <td><button class="reveal-btn" onclick="toggle('a14',this)">&#9654; Answer</button></td>
    </tr>
    <tr class="answer-row" id="a14">
      <td></td>
      <td colspan="4"><span class="answer-label">Root:</span> <span class="root-ans">שׁלח</span> &nbsp;|&nbsp; <span class="answer-label">PGN:</span> 2mp &nbsp;|&nbsp; <span class="answer-label">Translation:</span> Send! (to men)</td>
      <td></td>
    </tr>

    <!-- 15 -->
    <tr id="q15">
      <td>15</td>
      <td><div class="hebrew">קוּמוּ</div></td>
      <td><input class="parse-field" placeholder="root…"></td>
      <td><input class="parse-field" placeholder="PGN…"></td>
      <td><input class="parse-field" placeholder="translation…"></td>
      <td><button class="reveal-btn" onclick="toggle('a15',this)">&#9654; Answer</button></td>
    </tr>
    <tr class="answer-row" id="a15">
      <td></td>
      <td colspan="4"><span class="answer-label">Root:</span> <span class="root-ans">קום</span> &nbsp;|&nbsp; <span class="answer-label">PGN:</span> 2mp &nbsp;|&nbsp; <span class="answer-label">Translation:</span> Arise! (to men)</td>
      <td></td>
    </tr>

    <!-- 16 -->
    <tr id="q16">
      <td>16</td>
      <td><div class="hebrew">עֲבֵדוּ</div></td>
      <td><input class="parse-field" placeholder="root…"></td>
      <td><input class="parse-field" placeholder="PGN…"></td>
      <td><input class="parse-field" placeholder="translation…"></td>
      <td><button class="reveal-btn" onclick="toggle('a16',this)">&#9654; Answer</button></td>
    </tr>
    <tr class="answer-row" id="a16">
      <td></td>
      <td colspan="4"><span class="answer-label">Root:</span> <span class="root-ans">עבד</span> &nbsp;|&nbsp; <span class="answer-label">PGN:</span> 2mp &nbsp;|&nbsp; <span class="answer-label">Translation:</span> Do! / Serve! (to men)</td>
      <td></td>
    </tr>

    <!-- 17 -->
    <tr id="q17">
      <td>17</td>
      <td><div class="hebrew">אַל תִּסְגֻּד</div></td>
      <td><input class="parse-field" placeholder="root…"></td>
      <td><input class="parse-field" placeholder="PGN…"></td>
      <td><input class="parse-field" placeholder="translation…"></td>
      <td><button class="reveal-btn" onclick="toggle('a17',this)">&#9654; Answer</button></td>
    </tr>
    <tr class="answer-row" id="a17">
      <td></td>
      <td colspan="4"><span class="answer-label">Root:</span> <span class="root-ans">סגד</span> &nbsp;|&nbsp; <span class="answer-label">PGN:</span> 2ms (neg) &nbsp;|&nbsp; <span class="answer-label">Translation:</span> Do not bow down! (urgent — אַל + jussive)</td>
      <td></td>
    </tr>

    <!-- 18 -->
    <tr id="q18">
      <td>18</td>
      <td><div class="hebrew">לָא תִּכְתֻּב</div></td>
      <td><input class="parse-field" placeholder="root…"></td>
      <td><input class="parse-field" placeholder="PGN…"></td>
      <td><input class="parse-field" placeholder="translation…"></td>
      <td><button class="reveal-btn" onclick="toggle('a18',this)">&#9654; Answer</button></td>
    </tr>
    <tr class="answer-row" id="a18">
      <td></td>
      <td colspan="4"><span class="answer-label">Root:</span> <span class="root-ans">כתב</span> &nbsp;|&nbsp; <span class="answer-label">PGN:</span> 2ms (neg) &nbsp;|&nbsp; <span class="answer-label">Translation:</span> You shall not write (general prohibition — לָא + imperfect)</td>
      <td></td>
    </tr>

    <!-- 19 -->
    <tr id="q19">
      <td>19</td>
      <td><div class="hebrew">אַל תֵּאמְרוּן</div></td>
      <td><input class="parse-field" placeholder="root…"></td>
      <td><input class="parse-field" placeholder="PGN…"></td>
      <td><input class="parse-field" placeholder="translation…"></td>
      <td><button class="reveal-btn" onclick="toggle('a19',this)">&#9654; Answer</button></td>
    </tr>
    <tr class="answer-row" id="a19">
      <td></td>
      <td colspan="4"><span class="answer-label">Root:</span> <span class="root-ans">אמר</span> &nbsp;|&nbsp; <span class="answer-label">PGN:</span> 2mp (neg) &nbsp;|&nbsp; <span class="answer-label">Translation:</span> Do not say! (urgent, to men — אַל + jussive)</td>
      <td></td>
    </tr>

    <!-- 20 -->
    <tr id="q20">
      <td>20</td>
      <td><div class="hebrew">לָא תִּסְגְּדוּן</div></td>
      <td><input class="parse-field" placeholder="root…"></td>
      <td><input class="parse-field" placeholder="PGN…"></td>
      <td><input class="parse-field" placeholder="translation…"></td>
      <td><button class="reveal-btn" onclick="toggle('a20',this)">&#9654; Answer</button></td>
    </tr>
    <tr class="answer-row" id="a20">
      <td></td>
      <td colspan="4"><span class="answer-label">Root:</span> <span class="root-ans">סגד</span> &nbsp;|&nbsp; <span class="answer-label">PGN:</span> 2mp (neg) &nbsp;|&nbsp; <span class="answer-label">Translation:</span> You shall not bow down (general, to men — לָא + imperfect)</td>
      <td></td>
    </tr>

  </tbody>
</table>

<div class="reflection">
  <h3>Reflection Questions</h3>
  <ol>
    <li>Items 1 (קוּם) and 3 (כְּתֻב) are both 2ms imperatives, yet item 1 begins with a long ū vowel while item 3 has a shewa under the first radical. What accounts for this difference? What root type is each?</li>
    <li>Item 2 (אֱמַר) begins with aleph + hateph-seghol. Is this the root aleph of אמר, or something else? Why does this form not follow the standard קְטֻל pattern?</li>
    <li>Items 7 (הַב) and 10 (הָבוּ) come from root יהב. Where did the initial yod go? Does the imperative use the same suppletive form as the imperfect (יִנְתֵּן)?</li>
    <li>Item 9 (בְּנוֹ) is the 2mp imperative of בנה. Strong-verb 2mp ends in וּ- (shureq); this form ends in וֹ- (holem). What root class is בנה, and why is the 2mp ending different?</li>
    <li>Items 17–20 are prohibitions using אַל or לָא + imperfect. What is the difference in meaning or usage between אַל + jussive (items 17, 19) and לָא + imperfect (items 18, 20)?</li>
  </ol>
</div>

<script>
function toggle(id, btn) {
  var row = document.getElementById(id);
  if (row.classList.contains('visible')) {
    row.classList.remove('visible');
    btn.textContent = '▶ Answer';
  } else {
    row.classList.add('visible');
    btn.textContent = '▼ Hide';
  }
}
function showAll() {
  document.querySelectorAll('tr.answer-row').forEach(function(r) { r.classList.add('visible'); });
  document.querySelectorAll('button.reveal-btn').forEach(function(b) { b.textContent = '▼ Hide'; });
}
function hideAll() {
  document.querySelectorAll('tr.answer-row').forEach(function(r) { r.classList.remove('visible'); });
  document.querySelectorAll('button.reveal-btn').forEach(function(b) { b.textContent = '▶ Answer'; });
}
function clearAll() {
  document.querySelectorAll('input.parse-field').forEach(function(i) { i.value = ''; });
}
</script>

