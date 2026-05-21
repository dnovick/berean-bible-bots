# Preposition Parsing

*Chapter 8 — Prepositions and εἰμί*

[Full screen](ch8-preposition-parsing.html){.md-button}  [Markdown](ch8-preposition-parsing.md){.md-button}  [Print (PDF)](ch8-preposition-parsing.pdf){.md-button}

<style>

  body { font-family: Georgia, serif;    color: #222; }
  h1 { font-size: 1.4em; border-bottom: 2px solid #444; padding-bottom: .4em; }
  .subtitle { color: #666; font-style: italic; margin-top: -.3em; }
  table { border-collapse: collapse; width: 100%; margin: 1em 0; }
  th { background: #2a4a6e; color: #fff; padding: .5em .7em; text-align: left; font-size: .9em; }
  td { border: 1px solid #ccc; padding: .4em .6em; font-size: .9em; vertical-align: top; }
  tr:nth-child(even) td { background: #f7f7f7; }
  .gk { font-size: 1.15em; }
  .parse-field { width: 95%; font-size: .88em; border: 1px solid #aaa; border-radius: 3px; padding: 2px 4px; }
  .parse-field-lg { width: 97%; font-size: .88em; border: 1px solid #aaa; border-radius: 3px; padding: 2px 4px; }
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

<h1>Chapter 8 — Preposition Parsing Drill</h1>
<p class="subtitle">BBG Chapter 8 · Prepositions and εἰμί</p>

<p>For each prepositional phrase, identify: (1) the <strong>preposition</strong>, (2) the <strong>case</strong> it governs (Gen / Dat / Acc), and (3) an English <strong>translation</strong> of the phrase.</p>

<div class="tip">
  <strong>Reminder:</strong> Some prepositions take different cases with different meanings. Use the article to confirm case: τοῦ / τῆς / τῶν = Gen; τῷ / τῇ / τοῖς / ταῖς = Dat; τόν / τήν / τό / τούς / τάς / τά = Acc.
</div>

<div class="controls">
  <button onclick="showAll()">Show All Answers</button>
  <button onclick="hideAll()">Hide All Answers</button>
  <button onclick="clearAll()">Clear All Inputs</button>
</div>

<table>
  <tr><th>#</th><th>Greek Phrase</th><th>Preposition</th><th>Case</th><th>Translation</th><th></th></tr>

  <tr>
    <td>1</td><td class="gk">ἐν τῷ κόσμῳ</td>
    <td><input class="parse-field" id="p1" placeholder="preposition"></td>
    <td><input class="parse-field" id="c1" placeholder="Gen/Dat/Acc"></td>
    <td><input class="parse-field-lg" id="t1" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('r1')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r1"><td colspan="6"><strong>ἐν · Dat</strong> — "in the world"</td></tr>

  <tr>
    <td>2</td><td class="gk">εἰς τὴν βασιλείαν</td>
    <td><input class="parse-field" id="p2" placeholder="preposition"></td>
    <td><input class="parse-field" id="c2" placeholder="Gen/Dat/Acc"></td>
    <td><input class="parse-field-lg" id="t2" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('r2')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r2"><td colspan="6"><strong>εἰς · Acc</strong> — "into the kingdom"</td></tr>

  <tr>
    <td>3</td><td class="gk">ἐκ τοῦ οὐρανοῦ</td>
    <td><input class="parse-field" id="p3" placeholder="preposition"></td>
    <td><input class="parse-field" id="c3" placeholder="Gen/Dat/Acc"></td>
    <td><input class="parse-field-lg" id="t3" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('r3')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r3"><td colspan="6"><strong>ἐκ · Gen</strong> — "out of heaven"</td></tr>

  <tr>
    <td>4</td><td class="gk">ἀπὸ θεοῦ</td>
    <td><input class="parse-field" id="p4" placeholder="preposition"></td>
    <td><input class="parse-field" id="c4" placeholder="Gen/Dat/Acc"></td>
    <td><input class="parse-field-lg" id="t4" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('r4')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r4"><td colspan="6"><strong>ἀπό · Gen</strong> — "from God"</td></tr>

  <tr>
    <td>5</td><td class="gk">πρὸς τὸν πατέρα</td>
    <td><input class="parse-field" id="p5" placeholder="preposition"></td>
    <td><input class="parse-field" id="c5" placeholder="Gen/Dat/Acc"></td>
    <td><input class="parse-field-lg" id="t5" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('r5')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r5"><td colspan="6"><strong>πρός · Acc</strong> — "toward/to the Father"</td></tr>

  <tr>
    <td>6</td><td class="gk">διὰ τοῦ νόμου</td>
    <td><input class="parse-field" id="p6" placeholder="preposition"></td>
    <td><input class="parse-field" id="c6" placeholder="Gen/Dat/Acc"></td>
    <td><input class="parse-field-lg" id="t6" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('r6')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r6"><td colspan="6"><strong>διά · Gen</strong> — "through the law"</td></tr>

  <tr>
    <td>7</td><td class="gk">διὰ τοῦτο</td>
    <td><input class="parse-field" id="p7" placeholder="preposition"></td>
    <td><input class="parse-field" id="c7" placeholder="Gen/Dat/Acc"></td>
    <td><input class="parse-field-lg" id="t7" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('r7')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r7"><td colspan="6"><strong>διά · Acc</strong> — "because of this" / "therefore"</td></tr>

  <tr>
    <td>8</td><td class="gk">κατὰ σάρκα</td>
    <td><input class="parse-field" id="p8" placeholder="preposition"></td>
    <td><input class="parse-field" id="c8" placeholder="Gen/Dat/Acc"></td>
    <td><input class="parse-field-lg" id="t8" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('r8')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r8"><td colspan="6"><strong>κατά · Acc</strong> — "according to the flesh"</td></tr>

  <tr>
    <td>9</td><td class="gk">κατὰ τῶν ἐχθρῶν</td>
    <td><input class="parse-field" id="p9" placeholder="preposition"></td>
    <td><input class="parse-field" id="c9" placeholder="Gen/Dat/Acc"></td>
    <td><input class="parse-field-lg" id="t9" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('r9')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r9"><td colspan="6"><strong>κατά · Gen</strong> — "against the enemies"</td></tr>

  <tr>
    <td>10</td><td class="gk">μετὰ τῶν μαθητῶν</td>
    <td><input class="parse-field" id="p10" placeholder="preposition"></td>
    <td><input class="parse-field" id="c10" placeholder="Gen/Dat/Acc"></td>
    <td><input class="parse-field-lg" id="t10" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('r10')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r10"><td colspan="6"><strong>μετά · Gen</strong> — "with the disciples"</td></tr>

  <tr>
    <td>11</td><td class="gk">μετὰ ταῦτα</td>
    <td><input class="parse-field" id="p11" placeholder="preposition"></td>
    <td><input class="parse-field" id="c11" placeholder="Gen/Dat/Acc"></td>
    <td><input class="parse-field-lg" id="t11" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('r11')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r11"><td colspan="6"><strong>μετά · Acc</strong> — "after these things"</td></tr>

  <tr>
    <td>12</td><td class="gk">ἐπὶ τῆς γῆς</td>
    <td><input class="parse-field" id="p12" placeholder="preposition"></td>
    <td><input class="parse-field" id="c12" placeholder="Gen/Dat/Acc"></td>
    <td><input class="parse-field-lg" id="t12" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('r12')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r12"><td colspan="6"><strong>ἐπί · Gen</strong> — "on the earth"</td></tr>

  <tr>
    <td>13</td><td class="gk">ἐπὶ τὴν θάλασσαν</td>
    <td><input class="parse-field" id="p13" placeholder="preposition"></td>
    <td><input class="parse-field" id="c13" placeholder="Gen/Dat/Acc"></td>
    <td><input class="parse-field-lg" id="t13" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('r13')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r13"><td colspan="6"><strong>ἐπί · Acc</strong> — "onto/toward the sea"</td></tr>

  <tr>
    <td>14</td><td class="gk">παρὰ τοῦ πατρός</td>
    <td><input class="parse-field" id="p14" placeholder="preposition"></td>
    <td><input class="parse-field" id="c14" placeholder="Gen/Dat/Acc"></td>
    <td><input class="parse-field-lg" id="t14" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('r14')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r14"><td colspan="6"><strong>παρά · Gen</strong> — "from the Father"</td></tr>

  <tr>
    <td>15</td><td class="gk">παρὰ τῷ κυρίῳ</td>
    <td><input class="parse-field" id="p15" placeholder="preposition"></td>
    <td><input class="parse-field" id="c15" placeholder="Gen/Dat/Acc"></td>
    <td><input class="parse-field-lg" id="t15" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('r15')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r15"><td colspan="6"><strong>παρά · Dat</strong> — "beside/with the Lord"</td></tr>

  <tr>
    <td>16</td><td class="gk">περὶ τῆς ἁμαρτίας</td>
    <td><input class="parse-field" id="p16" placeholder="preposition"></td>
    <td><input class="parse-field" id="c16" placeholder="Gen/Dat/Acc"></td>
    <td><input class="parse-field-lg" id="t16" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('r16')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r16"><td colspan="6"><strong>περί · Gen</strong> — "concerning sin"</td></tr>

  <tr>
    <td>17</td><td class="gk">ὑπὸ τοῦ θεοῦ</td>
    <td><input class="parse-field" id="p17" placeholder="preposition"></td>
    <td><input class="parse-field" id="c17" placeholder="Gen/Dat/Acc"></td>
    <td><input class="parse-field-lg" id="t17" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('r17')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r17"><td colspan="6"><strong>ὑπό · Gen</strong> — "by God" (agent of passive)</td></tr>

  <tr>
    <td>18</td><td class="gk">σὺν αὐτῷ</td>
    <td><input class="parse-field" id="p18" placeholder="preposition"></td>
    <td><input class="parse-field" id="c18" placeholder="Gen/Dat/Acc"></td>
    <td><input class="parse-field-lg" id="t18" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('r18')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r18"><td colspan="6"><strong>σύν · Dat</strong> — "with him"</td></tr>

  <tr>
    <td>19</td><td class="gk">ἀντὶ πολλῶν</td>
    <td><input class="parse-field" id="p19" placeholder="preposition"></td>
    <td><input class="parse-field" id="c19" placeholder="Gen/Dat/Acc"></td>
    <td><input class="parse-field-lg" id="t19" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('r19')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r19"><td colspan="6"><strong>ἀντί · Gen</strong> — "in place of / for many"</td></tr>

  <tr>
    <td>20</td><td class="gk">ἐν ἀρχῇ</td>
    <td><input class="parse-field" id="p20" placeholder="preposition"></td>
    <td><input class="parse-field" id="c20" placeholder="Gen/Dat/Acc"></td>
    <td><input class="parse-field-lg" id="t20" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('r20')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r20"><td colspan="6"><strong>ἐν · Dat</strong> — "in the beginning"</td></tr>

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

