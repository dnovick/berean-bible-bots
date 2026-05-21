# Pronoun Parsing

*Chapter 11 — First and Second Person Personal Pronouns*

[Full screen](ch11-pronoun-parsing.html){.md-button}  [Markdown](ch11-pronoun-parsing.md){.md-button}  [Print (PDF)](ch11-pronoun-parsing.pdf){.md-button}

<style>

  body { font-family: Georgia, serif;    color: #222; }
  h1 { font-size: 1.4em; border-bottom: 2px solid #444; padding-bottom: .4em; }
  .subtitle { color: #666; font-style: italic; margin-top: -.3em; }
  table { border-collapse: collapse; width: 100%; margin: 1em 0; }
  th { background: #2a4a6e; color: #fff; padding: .5em .7em; text-align: left; font-size: .9em; }
  td { border: 1px solid #ccc; padding: .4em .6em; font-size: .9em; vertical-align: top; }
  tr:nth-child(even) td { background: #f7f7f7; }
  .gk { font-size: 1.15em; }
  .parse-field { width: 92%; font-size: .85em; border: 1px solid #aaa; border-radius: 3px; padding: 2px 4px; }
  .parse-field-lg { width: 97%; font-size: .85em; border: 1px solid #aaa; border-radius: 3px; padding: 2px 4px; }
  .answer-row td { background: #f0faf0 !important; color: #2a6e2a; font-size: .85em; }
  .answer-row { display: none; }
  button.reveal-btn { font-size: .8em; padding: 2px 8px; cursor: pointer; border: 1px solid #888; border-radius: 3px; background: #fff; white-space: nowrap; }
  .controls { margin: 1em 0; display: flex; gap: .6em; flex-wrap: wrap; }
  .controls button { padding: .4em .9em; font-size: .9em; cursor: pointer; border: 1px solid #555; border-radius: 4px; background: #f0f0f0; }
  .controls button:hover { background: #ddd; }
  .tip { background: #fffbe6; border-left: 4px solid #d4a017; padding: .6em 1em; margin: 1em 0; font-size: .9em; }
  @media print {
    button, .controls { display: none !important; }
    .parse-field, .parse-field-lg { border: none; border-bottom: 1px solid #000; background: transparent; }
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

<h1>Chapter 11 — Personal Pronoun Parsing Drill</h1>
<p class="subtitle">BBG Chapter 11 · First and Second Person Personal Pronouns</p>

<p>Parse each pronoun: <strong>Person</strong> (1st/2nd), <strong>Case</strong> (Nom/Gen/Dat/Acc), <strong>Number</strong> (Sg/Pl), and <strong>Translation</strong>.</p>

<div class="tip">
  <strong>Reminder:</strong> 1st person singular: ἐγώ / ἐμοῦ (μου) / ἐμοί (μοι) / ἐμέ (με). Plural: ἡμεῖς / ἡμῶν / ἡμῖν / ἡμᾶς. 2nd person singular: σύ / σοῦ (σου) / σοί (σοι) / σέ (σε). Plural: ὑμεῖς / ὑμῶν / ὑμῖν / ὑμᾶς. Accented forms are emphatic; unaccented (enclitic) are unemphatic.
</div>

<div class="controls">
  <button onclick="showAll()">Show All Answers</button>
  <button onclick="hideAll()">Hide All Answers</button>
  <button onclick="clearAll()">Clear All Inputs</button>
</div>

<table>
  <tr><th>#</th><th>Greek Form</th><th>Person</th><th>Case</th><th>Number</th><th>Translation</th><th></th></tr>

  <tr>
    <td>1</td><td class="gk">ἐγώ</td>
    <td><input class="parse-field" id="p1" placeholder="1st/2nd"></td>
    <td><input class="parse-field" id="c1" placeholder="Nom/Gen/Dat/Acc"></td>
    <td><input class="parse-field" id="n1" placeholder="Sg/Pl"></td>
    <td><input class="parse-field-lg" id="t1" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('r1')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r1"><td colspan="7"><strong>1st · Nom · Sg</strong> — "I" (emphatic subject)</td></tr>

  <tr>
    <td>2</td><td class="gk">μου</td>
    <td><input class="parse-field" id="p2" placeholder="1st/2nd"></td>
    <td><input class="parse-field" id="c2" placeholder="Nom/Gen/Dat/Acc"></td>
    <td><input class="parse-field" id="n2" placeholder="Sg/Pl"></td>
    <td><input class="parse-field-lg" id="t2" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('r2')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r2"><td colspan="7"><strong>1st · Gen · Sg</strong> — "my" / "of me" (enclitic)</td></tr>

  <tr>
    <td>3</td><td class="gk">σύ</td>
    <td><input class="parse-field" id="p3" placeholder="1st/2nd"></td>
    <td><input class="parse-field" id="c3" placeholder="Nom/Gen/Dat/Acc"></td>
    <td><input class="parse-field" id="n3" placeholder="Sg/Pl"></td>
    <td><input class="parse-field-lg" id="t3" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('r3')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r3"><td colspan="7"><strong>2nd · Nom · Sg</strong> — "you" (emphatic subject)</td></tr>

  <tr>
    <td>4</td><td class="gk">ἡμεῖς</td>
    <td><input class="parse-field" id="p4" placeholder="1st/2nd"></td>
    <td><input class="parse-field" id="c4" placeholder="Nom/Gen/Dat/Acc"></td>
    <td><input class="parse-field" id="n4" placeholder="Sg/Pl"></td>
    <td><input class="parse-field-lg" id="t4" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('r4')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r4"><td colspan="7"><strong>1st · Nom · Pl</strong> — "we"</td></tr>

  <tr>
    <td>5</td><td class="gk">ὑμῶν</td>
    <td><input class="parse-field" id="p5" placeholder="1st/2nd"></td>
    <td><input class="parse-field" id="c5" placeholder="Nom/Gen/Dat/Acc"></td>
    <td><input class="parse-field" id="n5" placeholder="Sg/Pl"></td>
    <td><input class="parse-field-lg" id="t5" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('r5')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r5"><td colspan="7"><strong>2nd · Gen · Pl</strong> — "your (pl.)" / "of you (pl.)"</td></tr>

  <tr>
    <td>6</td><td class="gk">μοι</td>
    <td><input class="parse-field" id="p6" placeholder="1st/2nd"></td>
    <td><input class="parse-field" id="c6" placeholder="Nom/Gen/Dat/Acc"></td>
    <td><input class="parse-field" id="n6" placeholder="Sg/Pl"></td>
    <td><input class="parse-field-lg" id="t6" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('r6')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r6"><td colspan="7"><strong>1st · Dat · Sg</strong> — "to/for me" (enclitic)</td></tr>

  <tr>
    <td>7</td><td class="gk">σοί</td>
    <td><input class="parse-field" id="p7" placeholder="1st/2nd"></td>
    <td><input class="parse-field" id="c7" placeholder="Nom/Gen/Dat/Acc"></td>
    <td><input class="parse-field" id="n7" placeholder="Sg/Pl"></td>
    <td><input class="parse-field-lg" id="t7" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('r7')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r7"><td colspan="7"><strong>2nd · Dat · Sg</strong> — "to/for you" (emphatic)</td></tr>

  <tr>
    <td>8</td><td class="gk">ἡμᾶς</td>
    <td><input class="parse-field" id="p8" placeholder="1st/2nd"></td>
    <td><input class="parse-field" id="c8" placeholder="Nom/Gen/Dat/Acc"></td>
    <td><input class="parse-field" id="n8" placeholder="Sg/Pl"></td>
    <td><input class="parse-field-lg" id="t8" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('r8')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r8"><td colspan="7"><strong>1st · Acc · Pl</strong> — "us"</td></tr>

  <tr>
    <td>9</td><td class="gk">σε</td>
    <td><input class="parse-field" id="p9" placeholder="1st/2nd"></td>
    <td><input class="parse-field" id="c9" placeholder="Nom/Gen/Dat/Acc"></td>
    <td><input class="parse-field" id="n9" placeholder="Sg/Pl"></td>
    <td><input class="parse-field-lg" id="t9" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('r9')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r9"><td colspan="7"><strong>2nd · Acc · Sg</strong> — "you" (enclitic)</td></tr>

  <tr>
    <td>10</td><td class="gk">ἐμέ</td>
    <td><input class="parse-field" id="p10" placeholder="1st/2nd"></td>
    <td><input class="parse-field" id="c10" placeholder="Nom/Gen/Dat/Acc"></td>
    <td><input class="parse-field" id="n10" placeholder="Sg/Pl"></td>
    <td><input class="parse-field-lg" id="t10" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('r10')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r10"><td colspan="7"><strong>1st · Acc · Sg</strong> — "me" (emphatic)</td></tr>

  <tr>
    <td>11</td><td class="gk">ὑμεῖς</td>
    <td><input class="parse-field" id="p11" placeholder="1st/2nd"></td>
    <td><input class="parse-field" id="c11" placeholder="Nom/Gen/Dat/Acc"></td>
    <td><input class="parse-field" id="n11" placeholder="Sg/Pl"></td>
    <td><input class="parse-field-lg" id="t11" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('r11')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r11"><td colspan="7"><strong>2nd · Nom · Pl</strong> — "you (pl.)"</td></tr>

  <tr>
    <td>12</td><td class="gk">ἡμῖν</td>
    <td><input class="parse-field" id="p12" placeholder="1st/2nd"></td>
    <td><input class="parse-field" id="c12" placeholder="Nom/Gen/Dat/Acc"></td>
    <td><input class="parse-field" id="n12" placeholder="Sg/Pl"></td>
    <td><input class="parse-field-lg" id="t12" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('r12')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r12"><td colspan="7"><strong>1st · Dat · Pl</strong> — "to/for us"</td></tr>

  <tr>
    <td>13</td><td class="gk">σου</td>
    <td><input class="parse-field" id="p13" placeholder="1st/2nd"></td>
    <td><input class="parse-field" id="c13" placeholder="Nom/Gen/Dat/Acc"></td>
    <td><input class="parse-field" id="n13" placeholder="Sg/Pl"></td>
    <td><input class="parse-field-lg" id="t13" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('r13')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r13"><td colspan="7"><strong>2nd · Gen · Sg</strong> — "your" / "of you" (enclitic)</td></tr>

  <tr>
    <td>14</td><td class="gk">ὑμᾶς</td>
    <td><input class="parse-field" id="p14" placeholder="1st/2nd"></td>
    <td><input class="parse-field" id="c14" placeholder="Nom/Gen/Dat/Acc"></td>
    <td><input class="parse-field" id="n14" placeholder="Sg/Pl"></td>
    <td><input class="parse-field-lg" id="t14" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('r14')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r14"><td colspan="7"><strong>2nd · Acc · Pl</strong> — "you (pl.)"</td></tr>

  <tr>
    <td>15</td><td class="gk">ἐμοῦ</td>
    <td><input class="parse-field" id="p15" placeholder="1st/2nd"></td>
    <td><input class="parse-field" id="c15" placeholder="Nom/Gen/Dat/Acc"></td>
    <td><input class="parse-field" id="n15" placeholder="Sg/Pl"></td>
    <td><input class="parse-field-lg" id="t15" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('r15')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r15"><td colspan="7"><strong>1st · Gen · Sg</strong> — "my" / "of me" (emphatic)</td></tr>

  <tr>
    <td>16</td><td class="gk">ὑμῖν</td>
    <td><input class="parse-field" id="p16" placeholder="1st/2nd"></td>
    <td><input class="parse-field" id="c16" placeholder="Nom/Gen/Dat/Acc"></td>
    <td><input class="parse-field" id="n16" placeholder="Sg/Pl"></td>
    <td><input class="parse-field-lg" id="t16" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('r16')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r16"><td colspan="7"><strong>2nd · Dat · Pl</strong> — "to/for you (pl.)"</td></tr>

  <tr>
    <td>17</td><td class="gk">με</td>
    <td><input class="parse-field" id="p17" placeholder="1st/2nd"></td>
    <td><input class="parse-field" id="c17" placeholder="Nom/Gen/Dat/Acc"></td>
    <td><input class="parse-field" id="n17" placeholder="Sg/Pl"></td>
    <td><input class="parse-field-lg" id="t17" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('r17')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r17"><td colspan="7"><strong>1st · Acc · Sg</strong> — "me" (enclitic)</td></tr>

  <tr>
    <td>18</td><td class="gk">σοῦ</td>
    <td><input class="parse-field" id="p18" placeholder="1st/2nd"></td>
    <td><input class="parse-field" id="c18" placeholder="Nom/Gen/Dat/Acc"></td>
    <td><input class="parse-field" id="n18" placeholder="Sg/Pl"></td>
    <td><input class="parse-field-lg" id="t18" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('r18')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r18"><td colspan="7"><strong>2nd · Gen · Sg</strong> — "your" / "of you" (emphatic)</td></tr>

  <tr>
    <td>19</td><td class="gk">ἡμῶν</td>
    <td><input class="parse-field" id="p19" placeholder="1st/2nd"></td>
    <td><input class="parse-field" id="c19" placeholder="Nom/Gen/Dat/Acc"></td>
    <td><input class="parse-field" id="n19" placeholder="Sg/Pl"></td>
    <td><input class="parse-field-lg" id="t19" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('r19')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r19"><td colspan="7"><strong>1st · Gen · Pl</strong> — "our" / "of us"</td></tr>

  <tr>
    <td>20</td><td class="gk">ἐμοί</td>
    <td><input class="parse-field" id="p20" placeholder="1st/2nd"></td>
    <td><input class="parse-field" id="c20" placeholder="Nom/Gen/Dat/Acc"></td>
    <td><input class="parse-field" id="n20" placeholder="Sg/Pl"></td>
    <td><input class="parse-field-lg" id="t20" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('r20')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r20"><td colspan="7"><strong>1st · Dat · Sg</strong> — "to/for me" (emphatic)</td></tr>

</table>

<script>
function toggle(id) {
  var row = document.getElementById(id);
  row.style.display = (row.style.display === 'table-row') ? 'none' : 'table-row';
}
function showAll() {
  document.querySelectorAll('.answer-row').forEach(function(r){ r.style.display='table-row'; });
}
function hideAll() {
  document.querySelectorAll('.answer-row').forEach(function(r){ r.style.display='none'; });
}
function clearAll() {
  document.querySelectorAll('.parse-field, .parse-field-lg').forEach(function(i){ i.value=''; });
}
</script>

