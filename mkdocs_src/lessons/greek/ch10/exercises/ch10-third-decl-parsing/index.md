# Third Decl Parsing

*Chapter 10 — Third Declension*

[Full screen](ch10-third-decl-parsing.html){.md-button}  [Markdown](ch10-third-decl-parsing.md){.md-button}  [Print (PDF)](ch10-third-decl-parsing.pdf){.md-button}

<style>

  body { font-family: Georgia, serif;    color: #222; }
  h1 { font-size: 1.4em; border-bottom: 2px solid #444; padding-bottom: .4em; }
  .subtitle { color: #666; font-style: italic; margin-top: -.3em; }
  table { border-collapse: collapse; width: 100%; margin: 1em 0; }
  th { background: #2a4a6e; color: #fff; padding: .5em .7em; text-align: left; font-size: .9em; }
  td { border: 1px solid #ccc; padding: .4em .6em; font-size: .9em; vertical-align: top; }
  tr:nth-child(even) td { background: #f7f7f7; }
  .gk { font-size: 1.15em; }
  .parse-field { width: 90%; font-size: .85em; border: 1px solid #aaa; border-radius: 3px; padding: 2px 4px; }
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

</style>

<h1>Chapter 10 — Third Declension Parsing Drill</h1>
<p class="subtitle">BBG Chapter 10 · Third Declension</p>

<p>Parse each form: <strong>Case</strong> (N/G/D/A), <strong>Number</strong> (S/P), <strong>Gender</strong> (M/F/N), <strong>Lexical Form</strong>, and <strong>Translation</strong>.</p>

<div class="tip">
  <strong>Tip:</strong> Find the stem by removing -ος from the genitive singular. Key endings: Gen Sg = -ος; Dat Sg = -ι; Nom/Acc Pl (neut.) = -α; Dat Pl = -σι(ν). The article disambiguates when forms are identical.
</div>

<div class="controls">
  <button onclick="showAll()">Show All Answers</button>
  <button onclick="hideAll()">Hide All Answers</button>
  <button onclick="clearAll()">Clear All Inputs</button>
</div>

<table>
  <tr><th>#</th><th>Greek Form</th><th>Case</th><th>Number</th><th>Gender</th><th>Lexical Form</th><th>Translation</th><th></th></tr>

  <tr>
    <td>1</td><td class="gk">τοῦ πνεύματος</td>
    <td><input class="parse-field" id="c1" placeholder="N/G/D/A"></td>
    <td><input class="parse-field" id="n1" placeholder="S/P"></td>
    <td><input class="parse-field" id="g1" placeholder="M/F/N"></td>
    <td><input class="parse-field" id="l1" placeholder="lexical form"></td>
    <td><input class="parse-field-lg" id="t1" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('r1')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r1"><td colspan="8"><strong>G · S · N · πνεῦμα</strong> — "of the spirit"</td></tr>

  <tr>
    <td>2</td><td class="gk">τῇ χάριτι</td>
    <td><input class="parse-field" id="c2" placeholder="N/G/D/A"></td>
    <td><input class="parse-field" id="n2" placeholder="S/P"></td>
    <td><input class="parse-field" id="g2" placeholder="M/F/N"></td>
    <td><input class="parse-field" id="l2" placeholder="lexical form"></td>
    <td><input class="parse-field-lg" id="t2" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('r2')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r2"><td colspan="8"><strong>D · S · F · χάρις</strong> — "to/by grace"</td></tr>

  <tr>
    <td>3</td><td class="gk">σώματα</td>
    <td><input class="parse-field" id="c3" placeholder="N/G/D/A"></td>
    <td><input class="parse-field" id="n3" placeholder="S/P"></td>
    <td><input class="parse-field" id="g3" placeholder="M/F/N"></td>
    <td><input class="parse-field" id="l3" placeholder="lexical form"></td>
    <td><input class="parse-field-lg" id="t3" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('r3')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r3"><td colspan="8"><strong>N or A · P · N · σῶμα</strong> — "bodies" (neut. nom./acc. pl. identical)</td></tr>

  <tr>
    <td>4</td><td class="gk">τοὺς αἰῶνας</td>
    <td><input class="parse-field" id="c4" placeholder="N/G/D/A"></td>
    <td><input class="parse-field" id="n4" placeholder="S/P"></td>
    <td><input class="parse-field" id="g4" placeholder="M/F/N"></td>
    <td><input class="parse-field" id="l4" placeholder="lexical form"></td>
    <td><input class="parse-field-lg" id="t4" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('r4')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r4"><td colspan="8"><strong>A · P · M · αἰών</strong> — "the ages"</td></tr>

  <tr>
    <td>5</td><td class="gk">τῆς σαρκός</td>
    <td><input class="parse-field" id="c5" placeholder="N/G/D/A"></td>
    <td><input class="parse-field" id="n5" placeholder="S/P"></td>
    <td><input class="parse-field" id="g5" placeholder="M/F/N"></td>
    <td><input class="parse-field" id="l5" placeholder="lexical form"></td>
    <td><input class="parse-field-lg" id="t5" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('r5')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r5"><td colspan="8"><strong>G · S · F · σάρξ</strong> — "of the flesh"</td></tr>

  <tr>
    <td>6</td><td class="gk">τῷ ὀνόματι</td>
    <td><input class="parse-field" id="c6" placeholder="N/G/D/A"></td>
    <td><input class="parse-field" id="n6" placeholder="S/P"></td>
    <td><input class="parse-field" id="g6" placeholder="M/F/N"></td>
    <td><input class="parse-field" id="l6" placeholder="lexical form"></td>
    <td><input class="parse-field-lg" id="t6" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('r6')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r6"><td colspan="8"><strong>D · S · N · ὄνομα</strong> — "in/by the name"</td></tr>

  <tr>
    <td>7</td><td class="gk">πνεύματα</td>
    <td><input class="parse-field" id="c7" placeholder="N/G/D/A"></td>
    <td><input class="parse-field" id="n7" placeholder="S/P"></td>
    <td><input class="parse-field" id="g7" placeholder="M/F/N"></td>
    <td><input class="parse-field" id="l7" placeholder="lexical form"></td>
    <td><input class="parse-field-lg" id="t7" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('r7')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r7"><td colspan="8"><strong>N or A · P · N · πνεῦμα</strong> — "spirits"</td></tr>

  <tr>
    <td>8</td><td class="gk">αἰῶσιν</td>
    <td><input class="parse-field" id="c8" placeholder="N/G/D/A"></td>
    <td><input class="parse-field" id="n8" placeholder="S/P"></td>
    <td><input class="parse-field" id="g8" placeholder="M/F/N"></td>
    <td><input class="parse-field" id="l8" placeholder="lexical form"></td>
    <td><input class="parse-field-lg" id="t8" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('r8')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r8"><td colspan="8"><strong>D · P · M · αἰών</strong> — "to/in the ages"</td></tr>

  <tr>
    <td>9</td><td class="gk">τὴν πόλιν</td>
    <td><input class="parse-field" id="c9" placeholder="N/G/D/A"></td>
    <td><input class="parse-field" id="n9" placeholder="S/P"></td>
    <td><input class="parse-field" id="g9" placeholder="M/F/N"></td>
    <td><input class="parse-field" id="l9" placeholder="lexical form"></td>
    <td><input class="parse-field-lg" id="t9" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('r9')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r9"><td colspan="8"><strong>A · S · F · πόλις</strong> — "the city"</td></tr>

  <tr>
    <td>10</td><td class="gk">χαρίτων</td>
    <td><input class="parse-field" id="c10" placeholder="N/G/D/A"></td>
    <td><input class="parse-field" id="n10" placeholder="S/P"></td>
    <td><input class="parse-field" id="g10" placeholder="M/F/N"></td>
    <td><input class="parse-field" id="l10" placeholder="lexical form"></td>
    <td><input class="parse-field-lg" id="t10" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('r10')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r10"><td colspan="8"><strong>G · P · F · χάρις</strong> — "of graces"</td></tr>

  <tr>
    <td>11</td><td class="gk">τοῦ σώματος</td>
    <td><input class="parse-field" id="c11" placeholder="N/G/D/A"></td>
    <td><input class="parse-field" id="n11" placeholder="S/P"></td>
    <td><input class="parse-field" id="g11" placeholder="M/F/N"></td>
    <td><input class="parse-field" id="l11" placeholder="lexical form"></td>
    <td><input class="parse-field-lg" id="t11" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('r11')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r11"><td colspan="8"><strong>G · S · N · σῶμα</strong> — "of the body"</td></tr>

  <tr>
    <td>12</td><td class="gk">ταῖς σαρξίν</td>
    <td><input class="parse-field" id="c12" placeholder="N/G/D/A"></td>
    <td><input class="parse-field" id="n12" placeholder="S/P"></td>
    <td><input class="parse-field" id="g12" placeholder="M/F/N"></td>
    <td><input class="parse-field" id="l12" placeholder="lexical form"></td>
    <td><input class="parse-field-lg" id="t12" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('r12')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r12"><td colspan="8"><strong>D · P · F · σάρξ</strong> — "in/to the flesh"</td></tr>

  <tr>
    <td>13</td><td class="gk">τὰ ὀνόματα</td>
    <td><input class="parse-field" id="c13" placeholder="N/G/D/A"></td>
    <td><input class="parse-field" id="n13" placeholder="S/P"></td>
    <td><input class="parse-field" id="g13" placeholder="M/F/N"></td>
    <td><input class="parse-field" id="l13" placeholder="lexical form"></td>
    <td><input class="parse-field-lg" id="t13" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('r13')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r13"><td colspan="8"><strong>N or A · P · N · ὄνομα</strong> — "the names"</td></tr>

  <tr>
    <td>14</td><td class="gk">τῆς πόλεως</td>
    <td><input class="parse-field" id="c14" placeholder="N/G/D/A"></td>
    <td><input class="parse-field" id="n14" placeholder="S/P"></td>
    <td><input class="parse-field" id="g14" placeholder="M/F/N"></td>
    <td><input class="parse-field" id="l14" placeholder="lexical form"></td>
    <td><input class="parse-field-lg" id="t14" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('r14')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r14"><td colspan="8"><strong>G · S · F · πόλις</strong> — "of the city" (i-stem; gen = -εως)</td></tr>

  <tr>
    <td>15</td><td class="gk">χάριτα</td>
    <td><input class="parse-field" id="c15" placeholder="N/G/D/A"></td>
    <td><input class="parse-field" id="n15" placeholder="S/P"></td>
    <td><input class="parse-field" id="g15" placeholder="M/F/N"></td>
    <td><input class="parse-field" id="l15" placeholder="lexical form"></td>
    <td><input class="parse-field-lg" id="t15" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('r15')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r15"><td colspan="8"><strong>A · S · F · χάρις</strong> — "grace" (direct object)</td></tr>

  <tr>
    <td>16</td><td class="gk">τῶν πνευμάτων</td>
    <td><input class="parse-field" id="c16" placeholder="N/G/D/A"></td>
    <td><input class="parse-field" id="n16" placeholder="S/P"></td>
    <td><input class="parse-field" id="g16" placeholder="M/F/N"></td>
    <td><input class="parse-field" id="l16" placeholder="lexical form"></td>
    <td><input class="parse-field-lg" id="t16" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('r16')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r16"><td colspan="8"><strong>G · P · N · πνεῦμα</strong> — "of the spirits"</td></tr>

  <tr>
    <td>17</td><td class="gk">αἰών</td>
    <td><input class="parse-field" id="c17" placeholder="N/G/D/A"></td>
    <td><input class="parse-field" id="n17" placeholder="S/P"></td>
    <td><input class="parse-field" id="g17" placeholder="M/F/N"></td>
    <td><input class="parse-field" id="l17" placeholder="lexical form"></td>
    <td><input class="parse-field-lg" id="t17" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('r17')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r17"><td colspan="8"><strong>N · S · M · αἰών</strong> — "age / eternity"</td></tr>

  <tr>
    <td>18</td><td class="gk">τοῖς σώμασιν</td>
    <td><input class="parse-field" id="c18" placeholder="N/G/D/A"></td>
    <td><input class="parse-field" id="n18" placeholder="S/P"></td>
    <td><input class="parse-field" id="g18" placeholder="M/F/N"></td>
    <td><input class="parse-field" id="l18" placeholder="lexical form"></td>
    <td><input class="parse-field-lg" id="t18" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('r18')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r18"><td colspan="8"><strong>D · P · N · σῶμα</strong> — "in/with the bodies"</td></tr>

  <tr>
    <td>19</td><td class="gk">πόλεις</td>
    <td><input class="parse-field" id="c19" placeholder="N/G/D/A"></td>
    <td><input class="parse-field" id="n19" placeholder="S/P"></td>
    <td><input class="parse-field" id="g19" placeholder="M/F/N"></td>
    <td><input class="parse-field" id="l19" placeholder="lexical form"></td>
    <td><input class="parse-field-lg" id="t19" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('r19')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r19"><td colspan="8"><strong>N or A · P · F · πόλις</strong> — "cities"</td></tr>

  <tr>
    <td>20</td><td class="gk">τὴν χάριτα</td>
    <td><input class="parse-field" id="c20" placeholder="N/G/D/A"></td>
    <td><input class="parse-field" id="n20" placeholder="S/P"></td>
    <td><input class="parse-field" id="g20" placeholder="M/F/N"></td>
    <td><input class="parse-field" id="l20" placeholder="lexical form"></td>
    <td><input class="parse-field-lg" id="t20" placeholder="translation"></td>
    <td><button class="reveal-btn" onclick="toggle('r20')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r20"><td colspan="8"><strong>A · S · F · χάρις</strong> — "grace" (direct object, with article)</td></tr>

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

