# Peal Imperfect Drill

*Chapter 14 — Peal Imperfect*

[Full screen](ch14-peal-imperfect-drill.html){.md-button}  [Markdown](ch14-peal-imperfect-drill.md){.md-button}  [Print (PDF)](ch14-peal-imperfect-drill.pdf){.md-button}

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

<div class="download-links" style="margin:1rem 0 .5rem;font-size:.85rem;">
  <strong>Also available:</strong>
  <a href="ch14-peal-imperfect-drill.md" style="margin-left:.5rem;">&#128196; Markdown</a>
  <span style="margin:0 .3rem;color:#aaa;">|</span>
  <a href="ch14-peal-imperfect-drill.pdf">&#128209; PDF</a>
</div>


<h1>Chapter 14 — Peal Imperfect Parsing Drill</h1>
<p class="subtitle"><em>Basics of Biblical Aramaic</em>, Van Pelt — Ch14: Peal Imperfect</p>

<h2>Instructions</h2>
<p>For each numbered verb form, enter the <strong>Root</strong> (3 consonants, Peal perfect 3ms), <strong>PGN</strong> (person / gender / number), and <strong>Translation</strong> in the input fields. Click <strong>&#9654; Answer</strong> to reveal the answer key row. All forms are Peal imperfect.</p>

<div class="controls">
  <button class="ctrl" onclick="showAll()">Show All Answers</button>
  <button class="ctrl" onclick="hideAll()">Hide All Answers</button>
  <button class="ctrl" onclick="clearAll()">Clear All Inputs</button>
</div>

<table id="drill-table">
  <thead>
    <tr>
      <th style="width:2.5em">#</th>
      <th style="width:14%">Form</th>
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
      <td><div class="hebrew">יִכְתֻּב</div></td>
      <td><input class="parse-field" placeholder="root…"></td>
      <td><input class="parse-field" placeholder="PGN…"></td>
      <td><input class="parse-field" placeholder="translation…"></td>
      <td><button class="reveal-btn" onclick="toggle('a1',this)">&#9654; Answer</button></td>
    </tr>
    <tr class="answer-row" id="a1">
      <td></td>
      <td colspan="4"><span class="answer-label">Root:</span> <span class="root-ans">כתב</span> &nbsp;|&nbsp; <span class="answer-label">PGN:</span> 3ms &nbsp;|&nbsp; <span class="answer-label">Translation:</span> he will write</td>
      <td></td>
    </tr>

    <!-- 2 -->
    <tr id="q2">
      <td>2</td>
      <td><div class="hebrew">יֵאמַר</div></td>
      <td><input class="parse-field" placeholder="root…"></td>
      <td><input class="parse-field" placeholder="PGN…"></td>
      <td><input class="parse-field" placeholder="translation…"></td>
      <td><button class="reveal-btn" onclick="toggle('a2',this)">&#9654; Answer</button></td>
    </tr>
    <tr class="answer-row" id="a2">
      <td></td>
      <td colspan="4"><span class="answer-label">Root:</span> <span class="root-ans">אמר</span> &nbsp;|&nbsp; <span class="answer-label">PGN:</span> 3ms &nbsp;|&nbsp; <span class="answer-label">Translation:</span> he will say</td>
      <td></td>
    </tr>

    <!-- 3 -->
    <tr id="q3">
      <td>3</td>
      <td><div class="hebrew">יְקוּם</div></td>
      <td><input class="parse-field" placeholder="root…"></td>
      <td><input class="parse-field" placeholder="PGN…"></td>
      <td><input class="parse-field" placeholder="translation…"></td>
      <td><button class="reveal-btn" onclick="toggle('a3',this)">&#9654; Answer</button></td>
    </tr>
    <tr class="answer-row" id="a3">
      <td></td>
      <td colspan="4"><span class="answer-label">Root:</span> <span class="root-ans">קום</span> &nbsp;|&nbsp; <span class="answer-label">PGN:</span> 3ms &nbsp;|&nbsp; <span class="answer-label">Translation:</span> he will arise</td>
      <td></td>
    </tr>

    <!-- 4 -->
    <tr id="q4">
      <td>4</td>
      <td><div class="hebrew">יִפַּל</div></td>
      <td><input class="parse-field" placeholder="root…"></td>
      <td><input class="parse-field" placeholder="PGN…"></td>
      <td><input class="parse-field" placeholder="translation…"></td>
      <td><button class="reveal-btn" onclick="toggle('a4',this)">&#9654; Answer</button></td>
    </tr>
    <tr class="answer-row" id="a4">
      <td></td>
      <td colspan="4"><span class="answer-label">Root:</span> <span class="root-ans">נפל</span> &nbsp;|&nbsp; <span class="answer-label">PGN:</span> 3ms &nbsp;|&nbsp; <span class="answer-label">Translation:</span> he will fall</td>
      <td></td>
    </tr>

    <!-- 5 -->
    <tr id="q5">
      <td>5</td>
      <td><div class="hebrew">יֶהֱוֵא</div></td>
      <td><input class="parse-field" placeholder="root…"></td>
      <td><input class="parse-field" placeholder="PGN…"></td>
      <td><input class="parse-field" placeholder="translation…"></td>
      <td><button class="reveal-btn" onclick="toggle('a5',this)">&#9654; Answer</button></td>
    </tr>
    <tr class="answer-row" id="a5">
      <td></td>
      <td colspan="4"><span class="answer-label">Root:</span> <span class="root-ans">הוה</span> &nbsp;|&nbsp; <span class="answer-label">PGN:</span> 3ms &nbsp;|&nbsp; <span class="answer-label">Translation:</span> it will be / he will be</td>
      <td></td>
    </tr>

    <!-- 6 -->
    <tr id="q6">
      <td>6</td>
      <td><div class="hebrew">יִשְׁלַח</div></td>
      <td><input class="parse-field" placeholder="root…"></td>
      <td><input class="parse-field" placeholder="PGN…"></td>
      <td><input class="parse-field" placeholder="translation…"></td>
      <td><button class="reveal-btn" onclick="toggle('a6',this)">&#9654; Answer</button></td>
    </tr>
    <tr class="answer-row" id="a6">
      <td></td>
      <td colspan="4"><span class="answer-label">Root:</span> <span class="root-ans">שׁלח</span> &nbsp;|&nbsp; <span class="answer-label">PGN:</span> 3ms &nbsp;|&nbsp; <span class="answer-label">Translation:</span> he will send</td>
      <td></td>
    </tr>

    <!-- 7 -->
    <tr id="q7">
      <td>7</td>
      <td><div class="hebrew">תִּקְטֻל</div></td>
      <td><input class="parse-field" placeholder="root…"></td>
      <td><input class="parse-field" placeholder="PGN…"></td>
      <td><input class="parse-field" placeholder="translation…"></td>
      <td><button class="reveal-btn" onclick="toggle('a7',this)">&#9654; Answer</button></td>
    </tr>
    <tr class="answer-row" id="a7">
      <td></td>
      <td colspan="4"><span class="answer-label">Root:</span> <span class="root-ans">קטל</span> &nbsp;|&nbsp; <span class="answer-label">PGN:</span> 3fs / 2ms &nbsp;|&nbsp; <span class="answer-label">Translation:</span> she will kill / you (ms) will kill</td>
      <td></td>
    </tr>

    <!-- 8 -->
    <tr id="q8">
      <td>8</td>
      <td><div class="hebrew">יַעְבְּדוּן</div></td>
      <td><input class="parse-field" placeholder="root…"></td>
      <td><input class="parse-field" placeholder="PGN…"></td>
      <td><input class="parse-field" placeholder="translation…"></td>
      <td><button class="reveal-btn" onclick="toggle('a8',this)">&#9654; Answer</button></td>
    </tr>
    <tr class="answer-row" id="a8">
      <td></td>
      <td colspan="4"><span class="answer-label">Root:</span> <span class="root-ans">עבד</span> &nbsp;|&nbsp; <span class="answer-label">PGN:</span> 3mp &nbsp;|&nbsp; <span class="answer-label">Translation:</span> they (m) will serve / do</td>
      <td></td>
    </tr>

    <!-- 9 -->
    <tr id="q9">
      <td>9</td>
      <td><div class="hebrew">תִּבְנֵא</div></td>
      <td><input class="parse-field" placeholder="root…"></td>
      <td><input class="parse-field" placeholder="PGN…"></td>
      <td><input class="parse-field" placeholder="translation…"></td>
      <td><button class="reveal-btn" onclick="toggle('a9',this)">&#9654; Answer</button></td>
    </tr>
    <tr class="answer-row" id="a9">
      <td></td>
      <td colspan="4"><span class="answer-label">Root:</span> <span class="root-ans">בנה</span> &nbsp;|&nbsp; <span class="answer-label">PGN:</span> 3fs / 2ms &nbsp;|&nbsp; <span class="answer-label">Translation:</span> she/it will be built / you (ms) will build</td>
      <td></td>
    </tr>

    <!-- 10 -->
    <tr id="q10">
      <td>10</td>
      <td><div class="hebrew">יִסְגְּדוּן</div></td>
      <td><input class="parse-field" placeholder="root…"></td>
      <td><input class="parse-field" placeholder="PGN…"></td>
      <td><input class="parse-field" placeholder="translation…"></td>
      <td><button class="reveal-btn" onclick="toggle('a10',this)">&#9654; Answer</button></td>
    </tr>
    <tr class="answer-row" id="a10">
      <td></td>
      <td colspan="4"><span class="answer-label">Root:</span> <span class="root-ans">סגד</span> &nbsp;|&nbsp; <span class="answer-label">PGN:</span> 3mp &nbsp;|&nbsp; <span class="answer-label">Translation:</span> they (m) will bow down</td>
      <td></td>
    </tr>

    <!-- 11 -->
    <tr id="q11">
      <td>11</td>
      <td><div class="hebrew">נִזְכֻּר</div></td>
      <td><input class="parse-field" placeholder="root…"></td>
      <td><input class="parse-field" placeholder="PGN…"></td>
      <td><input class="parse-field" placeholder="translation…"></td>
      <td><button class="reveal-btn" onclick="toggle('a11',this)">&#9654; Answer</button></td>
    </tr>
    <tr class="answer-row" id="a11">
      <td></td>
      <td colspan="4"><span class="answer-label">Root:</span> <span class="root-ans">זכר</span> &nbsp;|&nbsp; <span class="answer-label">PGN:</span> 1cp &nbsp;|&nbsp; <span class="answer-label">Translation:</span> we will remember</td>
      <td></td>
    </tr>

    <!-- 12 -->
    <tr id="q12">
      <td>12</td>
      <td><div class="hebrew">יִנְתֵּן</div></td>
      <td><input class="parse-field" placeholder="root…"></td>
      <td><input class="parse-field" placeholder="PGN…"></td>
      <td><input class="parse-field" placeholder="translation…"></td>
      <td><button class="reveal-btn" onclick="toggle('a12',this)">&#9654; Answer</button></td>
    </tr>
    <tr class="answer-row" id="a12">
      <td></td>
      <td colspan="4"><span class="answer-label">Root:</span> <span class="root-ans">יהב</span> &nbsp;|&nbsp; <span class="answer-label">PGN:</span> 3ms &nbsp;|&nbsp; <span class="answer-label">Translation:</span> he will give (suppletive imperfect of יהב)</td>
      <td></td>
    </tr>

    <!-- 13 -->
    <tr id="q13">
      <td>13</td>
      <td><div class="hebrew">יִקְטֻל</div></td>
      <td><input class="parse-field" placeholder="root…"></td>
      <td><input class="parse-field" placeholder="PGN…"></td>
      <td><input class="parse-field" placeholder="translation…"></td>
      <td><button class="reveal-btn" onclick="toggle('a13',this)">&#9654; Answer</button></td>
    </tr>
    <tr class="answer-row" id="a13">
      <td></td>
      <td colspan="4"><span class="answer-label">Root:</span> <span class="root-ans">קטל</span> &nbsp;|&nbsp; <span class="answer-label">PGN:</span> 3ms &nbsp;|&nbsp; <span class="answer-label">Translation:</span> he will kill</td>
      <td></td>
    </tr>

    <!-- 14 -->
    <tr id="q14">
      <td>14</td>
      <td><div class="hebrew">יִשְׁמַע</div></td>
      <td><input class="parse-field" placeholder="root…"></td>
      <td><input class="parse-field" placeholder="PGN…"></td>
      <td><input class="parse-field" placeholder="translation…"></td>
      <td><button class="reveal-btn" onclick="toggle('a14',this)">&#9654; Answer</button></td>
    </tr>
    <tr class="answer-row" id="a14">
      <td></td>
      <td colspan="4"><span class="answer-label">Root:</span> <span class="root-ans">שׁמע</span> &nbsp;|&nbsp; <span class="answer-label">PGN:</span> 3ms &nbsp;|&nbsp; <span class="answer-label">Translation:</span> he will hear</td>
      <td></td>
    </tr>

    <!-- 15 -->
    <tr id="q15">
      <td>15</td>
      <td><div class="hebrew">אֶכְתֻּב</div></td>
      <td><input class="parse-field" placeholder="root…"></td>
      <td><input class="parse-field" placeholder="PGN…"></td>
      <td><input class="parse-field" placeholder="translation…"></td>
      <td><button class="reveal-btn" onclick="toggle('a15',this)">&#9654; Answer</button></td>
    </tr>
    <tr class="answer-row" id="a15">
      <td></td>
      <td colspan="4"><span class="answer-label">Root:</span> <span class="root-ans">כתב</span> &nbsp;|&nbsp; <span class="answer-label">PGN:</span> 1cs &nbsp;|&nbsp; <span class="answer-label">Translation:</span> I will write</td>
      <td></td>
    </tr>

    <!-- 16 -->
    <tr id="q16">
      <td>16</td>
      <td><div class="hebrew">תִּכְתְּבוּן</div></td>
      <td><input class="parse-field" placeholder="root…"></td>
      <td><input class="parse-field" placeholder="PGN…"></td>
      <td><input class="parse-field" placeholder="translation…"></td>
      <td><button class="reveal-btn" onclick="toggle('a16',this)">&#9654; Answer</button></td>
    </tr>
    <tr class="answer-row" id="a16">
      <td></td>
      <td colspan="4"><span class="answer-label">Root:</span> <span class="root-ans">כתב</span> &nbsp;|&nbsp; <span class="answer-label">PGN:</span> 2mp &nbsp;|&nbsp; <span class="answer-label">Translation:</span> you (mp) will write</td>
      <td></td>
    </tr>

    <!-- 17 -->
    <tr id="q17">
      <td>17</td>
      <td><div class="hebrew">תִּכְתְּבִין</div></td>
      <td><input class="parse-field" placeholder="root…"></td>
      <td><input class="parse-field" placeholder="PGN…"></td>
      <td><input class="parse-field" placeholder="translation…"></td>
      <td><button class="reveal-btn" onclick="toggle('a17',this)">&#9654; Answer</button></td>
    </tr>
    <tr class="answer-row" id="a17">
      <td></td>
      <td colspan="4"><span class="answer-label">Root:</span> <span class="root-ans">כתב</span> &nbsp;|&nbsp; <span class="answer-label">PGN:</span> 2fs &nbsp;|&nbsp; <span class="answer-label">Translation:</span> you (fs) will write</td>
      <td></td>
    </tr>

    <!-- 18 -->
    <tr id="q18">
      <td>18</td>
      <td><div class="hebrew">יִכְתְּבָן</div></td>
      <td><input class="parse-field" placeholder="root…"></td>
      <td><input class="parse-field" placeholder="PGN…"></td>
      <td><input class="parse-field" placeholder="translation…"></td>
      <td><button class="reveal-btn" onclick="toggle('a18',this)">&#9654; Answer</button></td>
    </tr>
    <tr class="answer-row" id="a18">
      <td></td>
      <td colspan="4"><span class="answer-label">Root:</span> <span class="root-ans">כתב</span> &nbsp;|&nbsp; <span class="answer-label">PGN:</span> 3fp &nbsp;|&nbsp; <span class="answer-label">Translation:</span> they (f) will write</td>
      <td></td>
    </tr>

    <!-- 19 -->
    <tr id="q19">
      <td>19</td>
      <td><div class="hebrew">תֵּאמְרוּן</div></td>
      <td><input class="parse-field" placeholder="root…"></td>
      <td><input class="parse-field" placeholder="PGN…"></td>
      <td><input class="parse-field" placeholder="translation…"></td>
      <td><button class="reveal-btn" onclick="toggle('a19',this)">&#9654; Answer</button></td>
    </tr>
    <tr class="answer-row" id="a19">
      <td></td>
      <td colspan="4"><span class="answer-label">Root:</span> <span class="root-ans">אמר</span> &nbsp;|&nbsp; <span class="answer-label">PGN:</span> 2mp &nbsp;|&nbsp; <span class="answer-label">Translation:</span> you (mp) will say</td>
      <td></td>
    </tr>

    <!-- 20 -->
    <tr id="q20">
      <td>20</td>
      <td><div class="hebrew">נֶהֱוֵא</div></td>
      <td><input class="parse-field" placeholder="root…"></td>
      <td><input class="parse-field" placeholder="PGN…"></td>
      <td><input class="parse-field" placeholder="translation…"></td>
      <td><button class="reveal-btn" onclick="toggle('a20',this)">&#9654; Answer</button></td>
    </tr>
    <tr class="answer-row" id="a20">
      <td></td>
      <td colspan="4"><span class="answer-label">Root:</span> <span class="root-ans">הוה</span> &nbsp;|&nbsp; <span class="answer-label">PGN:</span> 1cp &nbsp;|&nbsp; <span class="answer-label">Translation:</span> we will be</td>
      <td></td>
    </tr>

  </tbody>
</table>

<div class="reflection">
  <h3>Reflection Questions</h3>
  <ol>
    <li>Items 1 and 13 use the roots כתב and קטל (the abstract grammar root) for the same PGN. What tells you both are 3ms Peal imperfect, and how does the stem vowel differ from Hebrew?</li>
    <li>Items 2 and 19 share root אמר. What PGN is each, and what caused the prefix vowel change from יִ-/תִּ- to יֵ-/תֵּ-?</li>
    <li>Item 12 (יִנְתֵּן) is the Peal imperfect of יהב. Why doesn't it look like a normal imperfect of יהב? What phenomenon is at work?</li>
    <li>Compare item 4 (יִפַּל) with the Peal perfect of the same root (נְפַל). What happened to the first root consonant? How does this parallel Hebrew יִפֹּל?</li>
    <li>Items 16, 17, and 18 all come from root כתב but represent 2mp, 2fs, and 3fp. What suffix marks each, and how do these differ from the Hebrew Qal imperfect equivalents?</li>
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

