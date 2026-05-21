# Gen Dat Parsing

*Chapter 7 — Genitive and Dative*

[Full screen](ch7-gen-dat-parsing.html){.md-button}  [Markdown](ch7-gen-dat-parsing.md){.md-button}  [Print (PDF)](ch7-gen-dat-parsing.pdf){.md-button}

<style>

  body { font-family: Georgia, serif;    color: #222; }
  h1 { font-size: 1.4em; border-bottom: 2px solid #444; padding-bottom: .4em; }
  .subtitle { color: #666; font-style: italic; margin-top: -.3em; }
  table { border-collapse: collapse; width: 100%; margin: 1em 0; }
  th { background: #2a4a6e; color: #fff; padding: .5em .7em; text-align: left; font-size: .9em; }
  td { border: 1px solid #ccc; padding: .4em .6em; font-size: .9em; vertical-align: top; }
  tr:nth-child(even) td { background: #f7f7f7; }
  .gk { font-size: 1.15em; }
  .parse-field { width: 90%; font-size: .88em; border: 1px solid #aaa; border-radius: 3px; padding: 2px 4px; }
  .answer-row td { background: #f0faf0 !important; color: #2a6e2a; font-size: .85em; }
  .answer-row { display: none; }
  button.reveal-btn { font-size: .8em; padding: 2px 8px; cursor: pointer; border: 1px solid #888; border-radius: 3px; background: #fff; white-space: nowrap; }
  .controls { margin: 1em 0; display: flex; gap: .6em; flex-wrap: wrap; }
  .controls button { padding: .4em .9em; font-size: .9em; cursor: pointer; border: 1px solid #555; border-radius: 4px; background: #f0f0f0; }
  .controls button:hover { background: #ddd; }
  .tip { background: #fffbe6; border-left: 4px solid #d4a017; padding: .6em 1em; margin: 1em 0; font-size: .9em; }
  @media print {
    button, .controls { display: none !important; }
    .parse-field { border: none; border-bottom: 1px solid #000; background: transparent; }
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

<h1>Chapter 7 — Genitive and Dative Parsing Drill</h1>
<p class="subtitle">BBG Chapter 7 · 2nd-Declension Genitive and Dative Forms</p>

<p>Parse each Greek form: <strong>Case</strong> (G/D), <strong>Number</strong> (S/P), <strong>Gender</strong> (M/N), <strong>Lexical Form</strong>, and a brief <strong>Translation Note</strong>.</p>

<div class="tip">
  <strong>Reminder:</strong> The dative singular ends in <strong>-ῳ</strong> (omega with iota subscript); the genitive singular ends in <strong>-ου</strong>. The article is your best guide: τοῦ = genitive singular; τῷ = dative singular; τῶν = genitive plural; τοῖς = dative plural.
</div>

<div class="controls">
  <button onclick="showAll()">Show All Answers</button>
  <button onclick="hideAll()">Hide All Answers</button>
  <button onclick="clearAll()">Clear All Inputs</button>
</div>

<table>
  <tr>
    <th>#</th><th>Greek Form</th><th>Case</th><th>Number</th><th>Gender</th><th>Lexical Form</th><th>Translation Note</th><th></th>
  </tr>

  <tr>
    <td>1</td><td class="gk">τοῦ θεοῦ</td>
    <td><input class="parse-field" id="c1" placeholder="G/D"></td>
    <td><input class="parse-field" id="n1" placeholder="S/P"></td>
    <td><input class="parse-field" id="g1" placeholder="M/N"></td>
    <td><input class="parse-field" id="l1" placeholder="lexical form"></td>
    <td><input class="parse-field" id="t1" placeholder="translation note"></td>
    <td><button class="reveal-btn" onclick="toggle('r1')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r1">
    <td colspan="8"><strong>G · S · M · θεός</strong> — "of God" / "God's"</td>
  </tr>

  <tr>
    <td>2</td><td class="gk">τῷ κυρίῳ</td>
    <td><input class="parse-field" id="c2" placeholder="G/D"></td>
    <td><input class="parse-field" id="n2" placeholder="S/P"></td>
    <td><input class="parse-field" id="g2" placeholder="M/N"></td>
    <td><input class="parse-field" id="l2" placeholder="lexical form"></td>
    <td><input class="parse-field" id="t2" placeholder="translation note"></td>
    <td><button class="reveal-btn" onclick="toggle('r2')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r2">
    <td colspan="8"><strong>D · S · M · κύριος</strong> — "to/for the Lord"</td>
  </tr>

  <tr>
    <td>3</td><td class="gk">λόγων</td>
    <td><input class="parse-field" id="c3" placeholder="G/D"></td>
    <td><input class="parse-field" id="n3" placeholder="S/P"></td>
    <td><input class="parse-field" id="g3" placeholder="M/N"></td>
    <td><input class="parse-field" id="l3" placeholder="lexical form"></td>
    <td><input class="parse-field" id="t3" placeholder="translation note"></td>
    <td><button class="reveal-btn" onclick="toggle('r3')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r3">
    <td colspan="8"><strong>G · P · M · λόγος</strong> — "of words"</td>
  </tr>

  <tr>
    <td>4</td><td class="gk">τοῖς δούλοις</td>
    <td><input class="parse-field" id="c4" placeholder="G/D"></td>
    <td><input class="parse-field" id="n4" placeholder="S/P"></td>
    <td><input class="parse-field" id="g4" placeholder="M/N"></td>
    <td><input class="parse-field" id="l4" placeholder="lexical form"></td>
    <td><input class="parse-field" id="t4" placeholder="translation note"></td>
    <td><button class="reveal-btn" onclick="toggle('r4')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r4">
    <td colspan="8"><strong>D · P · M · δοῦλος</strong> — "to/for the slaves"</td>
  </tr>

  <tr>
    <td>5</td><td class="gk">τοῦ ἔργου</td>
    <td><input class="parse-field" id="c5" placeholder="G/D"></td>
    <td><input class="parse-field" id="n5" placeholder="S/P"></td>
    <td><input class="parse-field" id="g5" placeholder="M/N"></td>
    <td><input class="parse-field" id="l5" placeholder="lexical form"></td>
    <td><input class="parse-field" id="t5" placeholder="translation note"></td>
    <td><button class="reveal-btn" onclick="toggle('r5')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r5">
    <td colspan="8"><strong>G · S · N · ἔργον</strong> — "of the work"</td>
  </tr>

  <tr>
    <td>6</td><td class="gk">τῷ νόμῳ</td>
    <td><input class="parse-field" id="c6" placeholder="G/D"></td>
    <td><input class="parse-field" id="n6" placeholder="S/P"></td>
    <td><input class="parse-field" id="g6" placeholder="M/N"></td>
    <td><input class="parse-field" id="l6" placeholder="lexical form"></td>
    <td><input class="parse-field" id="t6" placeholder="translation note"></td>
    <td><button class="reveal-btn" onclick="toggle('r6')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r6">
    <td colspan="8"><strong>D · S · M · νόμος</strong> — "in/by the law"</td>
  </tr>

  <tr>
    <td>7</td><td class="gk">ἀδελφῶν</td>
    <td><input class="parse-field" id="c7" placeholder="G/D"></td>
    <td><input class="parse-field" id="n7" placeholder="S/P"></td>
    <td><input class="parse-field" id="g7" placeholder="M/N"></td>
    <td><input class="parse-field" id="l7" placeholder="lexical form"></td>
    <td><input class="parse-field" id="t7" placeholder="translation note"></td>
    <td><button class="reveal-btn" onclick="toggle('r7')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r7">
    <td colspan="8"><strong>G · P · M · ἀδελφός</strong> — "of brothers"</td>
  </tr>

  <tr>
    <td>8</td><td class="gk">τοῖς ἔργοις</td>
    <td><input class="parse-field" id="c8" placeholder="G/D"></td>
    <td><input class="parse-field" id="n8" placeholder="S/P"></td>
    <td><input class="parse-field" id="g8" placeholder="M/N"></td>
    <td><input class="parse-field" id="l8" placeholder="lexical form"></td>
    <td><input class="parse-field" id="t8" placeholder="translation note"></td>
    <td><button class="reveal-btn" onclick="toggle('r8')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r8">
    <td colspan="8"><strong>D · P · N · ἔργον</strong> — "by/with the works"</td>
  </tr>

  <tr>
    <td>9</td><td class="gk">τοῦ υἱοῦ</td>
    <td><input class="parse-field" id="c9" placeholder="G/D"></td>
    <td><input class="parse-field" id="n9" placeholder="S/P"></td>
    <td><input class="parse-field" id="g9" placeholder="M/N"></td>
    <td><input class="parse-field" id="l9" placeholder="lexical form"></td>
    <td><input class="parse-field" id="t9" placeholder="translation note"></td>
    <td><button class="reveal-btn" onclick="toggle('r9')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r9">
    <td colspan="8"><strong>G · S · M · υἱός</strong> — "of the Son"</td>
  </tr>

  <tr>
    <td>10</td><td class="gk">τῷ οἴκῳ</td>
    <td><input class="parse-field" id="c10" placeholder="G/D"></td>
    <td><input class="parse-field" id="n10" placeholder="S/P"></td>
    <td><input class="parse-field" id="g10" placeholder="M/N"></td>
    <td><input class="parse-field" id="l10" placeholder="lexical form"></td>
    <td><input class="parse-field" id="t10" placeholder="translation note"></td>
    <td><button class="reveal-btn" onclick="toggle('r10')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r10">
    <td colspan="8"><strong>D · S · M · οἶκος</strong> — "in/to the house"</td>
  </tr>

  <tr>
    <td>11</td><td class="gk">εὐαγγελίων</td>
    <td><input class="parse-field" id="c11" placeholder="G/D"></td>
    <td><input class="parse-field" id="n11" placeholder="S/P"></td>
    <td><input class="parse-field" id="g11" placeholder="M/N"></td>
    <td><input class="parse-field" id="l11" placeholder="lexical form"></td>
    <td><input class="parse-field" id="t11" placeholder="translation note"></td>
    <td><button class="reveal-btn" onclick="toggle('r11')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r11">
    <td colspan="8"><strong>G · P · N · εὐαγγέλιον</strong> — "of gospels"</td>
  </tr>

  <tr>
    <td>12</td><td class="gk">τοῖς λόγοις</td>
    <td><input class="parse-field" id="c12" placeholder="G/D"></td>
    <td><input class="parse-field" id="n12" placeholder="S/P"></td>
    <td><input class="parse-field" id="g12" placeholder="M/N"></td>
    <td><input class="parse-field" id="l12" placeholder="lexical form"></td>
    <td><input class="parse-field" id="t12" placeholder="translation note"></td>
    <td><button class="reveal-btn" onclick="toggle('r12')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r12">
    <td colspan="8"><strong>D · P · M · λόγος</strong> — "in/with the words"</td>
  </tr>

  <tr>
    <td>13</td><td class="gk">τοῦ ἀνθρώπου</td>
    <td><input class="parse-field" id="c13" placeholder="G/D"></td>
    <td><input class="parse-field" id="n13" placeholder="S/P"></td>
    <td><input class="parse-field" id="g13" placeholder="M/N"></td>
    <td><input class="parse-field" id="l13" placeholder="lexical form"></td>
    <td><input class="parse-field" id="t13" placeholder="translation note"></td>
    <td><button class="reveal-btn" onclick="toggle('r13')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r13">
    <td colspan="8"><strong>G · S · M · ἄνθρωπος</strong> — "of the man"</td>
  </tr>

  <tr>
    <td>14</td><td class="gk">τῷ ἀποστόλῳ</td>
    <td><input class="parse-field" id="c14" placeholder="G/D"></td>
    <td><input class="parse-field" id="n14" placeholder="S/P"></td>
    <td><input class="parse-field" id="g14" placeholder="M/N"></td>
    <td><input class="parse-field" id="l14" placeholder="lexical form"></td>
    <td><input class="parse-field" id="t14" placeholder="translation note"></td>
    <td><button class="reveal-btn" onclick="toggle('r14')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r14">
    <td colspan="8"><strong>D · S · M · ἀπόστολος</strong> — "to/for the apostle"</td>
  </tr>

  <tr>
    <td>15</td><td class="gk">δούλου</td>
    <td><input class="parse-field" id="c15" placeholder="G/D"></td>
    <td><input class="parse-field" id="n15" placeholder="S/P"></td>
    <td><input class="parse-field" id="g15" placeholder="M/N"></td>
    <td><input class="parse-field" id="l15" placeholder="lexical form"></td>
    <td><input class="parse-field" id="t15" placeholder="translation note"></td>
    <td><button class="reveal-btn" onclick="toggle('r15')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r15">
    <td colspan="8"><strong>G · S · M · δοῦλος</strong> — "of a slave"</td>
  </tr>

  <tr>
    <td>16</td><td class="gk">τῶν τέκνων</td>
    <td><input class="parse-field" id="c16" placeholder="G/D"></td>
    <td><input class="parse-field" id="n16" placeholder="S/P"></td>
    <td><input class="parse-field" id="g16" placeholder="M/N"></td>
    <td><input class="parse-field" id="l16" placeholder="lexical form"></td>
    <td><input class="parse-field" id="t16" placeholder="translation note"></td>
    <td><button class="reveal-btn" onclick="toggle('r16')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r16">
    <td colspan="8"><strong>G · P · N · τέκνον</strong> — "of the children"</td>
  </tr>

  <tr>
    <td>17</td><td class="gk">τῷ εὐαγγελίῳ</td>
    <td><input class="parse-field" id="c17" placeholder="G/D"></td>
    <td><input class="parse-field" id="n17" placeholder="S/P"></td>
    <td><input class="parse-field" id="g17" placeholder="M/N"></td>
    <td><input class="parse-field" id="l17" placeholder="lexical form"></td>
    <td><input class="parse-field" id="t17" placeholder="translation note"></td>
    <td><button class="reveal-btn" onclick="toggle('r17')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r17">
    <td colspan="8"><strong>D · S · N · εὐαγγέλιον</strong> — "in/by the gospel"</td>
  </tr>

  <tr>
    <td>18</td><td class="gk">κυρίων</td>
    <td><input class="parse-field" id="c18" placeholder="G/D"></td>
    <td><input class="parse-field" id="n18" placeholder="S/P"></td>
    <td><input class="parse-field" id="g18" placeholder="M/N"></td>
    <td><input class="parse-field" id="l18" placeholder="lexical form"></td>
    <td><input class="parse-field" id="t18" placeholder="translation note"></td>
    <td><button class="reveal-btn" onclick="toggle('r18')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r18">
    <td colspan="8"><strong>G · P · M · κύριος</strong> — "of lords"</td>
  </tr>

  <tr>
    <td>19</td><td class="gk">τοῦ ἱεροῦ</td>
    <td><input class="parse-field" id="c19" placeholder="G/D"></td>
    <td><input class="parse-field" id="n19" placeholder="S/P"></td>
    <td><input class="parse-field" id="g19" placeholder="M/N"></td>
    <td><input class="parse-field" id="l19" placeholder="lexical form"></td>
    <td><input class="parse-field" id="t19" placeholder="translation note"></td>
    <td><button class="reveal-btn" onclick="toggle('r19')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r19">
    <td colspan="8"><strong>G · S · N · ἱερόν</strong> — "of the temple"</td>
  </tr>

  <tr>
    <td>20</td><td class="gk">τοῖς ἀδελφοῖς</td>
    <td><input class="parse-field" id="c20" placeholder="G/D"></td>
    <td><input class="parse-field" id="n20" placeholder="S/P"></td>
    <td><input class="parse-field" id="g20" placeholder="M/N"></td>
    <td><input class="parse-field" id="l20" placeholder="lexical form"></td>
    <td><input class="parse-field" id="t20" placeholder="translation note"></td>
    <td><button class="reveal-btn" onclick="toggle('r20')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r20">
    <td colspan="8"><strong>D · P · M · ἀδελφός</strong> — "to/for the brothers"</td>
  </tr>

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
  document.querySelectorAll('.parse-field').forEach(function(i){ i.value=''; });
}
</script>

