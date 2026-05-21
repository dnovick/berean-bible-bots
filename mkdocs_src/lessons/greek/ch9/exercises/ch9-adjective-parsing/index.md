# Adjective Parsing

*Chapter 9 — Adjectives*

[Full screen](ch9-adjective-parsing.html){.md-button}  [Markdown](ch9-adjective-parsing.md){.md-button}  [Print (PDF)](ch9-adjective-parsing.pdf){.md-button}

<style>

  body { font-family: Georgia, serif;    color: #222; }
  h1 { font-size: 1.4em; border-bottom: 2px solid #444; padding-bottom: .4em; }
  .subtitle { color: #666; font-style: italic; margin-top: -.3em; }
  table { border-collapse: collapse;  margin: 1em 0; }
  th { background: #2a4a6e; color: #fff; padding: .5em .7em; text-align: left; font-size: .9em; }
  td { border: 1px solid #ccc; padding: .4em .6em; font-size: .9em; vertical-align: top; }
  tr:nth-child(even) td { background: #f7f7f7; }
  .gk { font-size: 1.15em; }
  .parse-field { width: 90%; font-size: .85em; border: 1px solid #aaa; border-radius: 3px; padding: 2px 4px; }
  .parse-field-lg { width: 95%; font-size: .85em; border: 1px solid #aaa; border-radius: 3px; padding: 2px 4px; }
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

<h1>Chapter 9 — Adjective Parsing Drill</h1>
<p class="subtitle">BBG Chapter 9 · Adjectives</p>

<p>For each phrase, parse the adjective: <strong>Case</strong> (N/G/D/A), <strong>Number</strong> (S/P), <strong>Gender</strong> (M/F/N), and <strong>Position</strong> (Attr / Pred / Sub).</p>

<div class="tip">
  <strong>Key rule:</strong> If the article precedes the adjective directly → attributive or substantival. If the noun has an article but the adjective does not → predicate. If article + adjective but no noun → substantival.
</div>

<div class="controls">
  <button onclick="showAll()">Show All Answers</button>
  <button onclick="hideAll()">Hide All Answers</button>
  <button onclick="clearAll()">Clear All Inputs</button>
</div>

<div style="overflow-x:auto;max-width:100%;"><table>
  <tr><th>#</th><th>Greek Phrase</th><th>Case</th><th>Number</th><th>Gender</th><th>Position</th><th></th></tr>

  <tr>
    <td>1</td><td class="gk">ὁ ἀγαθὸς δοῦλος</td>
    <td><input class="parse-field" id="c1" placeholder="N/G/D/A"></td>
    <td><input class="parse-field" id="n1" placeholder="S/P"></td>
    <td><input class="parse-field" id="g1" placeholder="M/F/N"></td>
    <td><input class="parse-field-lg" id="p1" placeholder="Attr/Pred/Sub"></td>
    <td><button class="reveal-btn" onclick="toggle('r1')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r1"><td colspan="7"><strong>N · S · M · Attributive</strong> — art-adj-noun; "the good slave"</td></tr>

  <tr>
    <td>2</td><td class="gk">ὁ δοῦλος ἀγαθός</td>
    <td><input class="parse-field" id="c2" placeholder="N/G/D/A"></td>
    <td><input class="parse-field" id="n2" placeholder="S/P"></td>
    <td><input class="parse-field" id="g2" placeholder="M/F/N"></td>
    <td><input class="parse-field-lg" id="p2" placeholder="Attr/Pred/Sub"></td>
    <td><button class="reveal-btn" onclick="toggle('r2')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r2"><td colspan="7"><strong>N · S · M · Predicate</strong> — noun has art; adj has none; "The slave is good."</td></tr>

  <tr>
    <td>3</td><td class="gk">οἱ ἀγαθοί</td>
    <td><input class="parse-field" id="c3" placeholder="N/G/D/A"></td>
    <td><input class="parse-field" id="n3" placeholder="S/P"></td>
    <td><input class="parse-field" id="g3" placeholder="M/F/N"></td>
    <td><input class="parse-field-lg" id="p3" placeholder="Attr/Pred/Sub"></td>
    <td><button class="reveal-btn" onclick="toggle('r3')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r3"><td colspan="7"><strong>N · P · M · Substantival</strong> — art + adj; no noun; "the good people"</td></tr>

  <tr>
    <td>4</td><td class="gk">τὸν πιστὸν λόγον</td>
    <td><input class="parse-field" id="c4" placeholder="N/G/D/A"></td>
    <td><input class="parse-field" id="n4" placeholder="S/P"></td>
    <td><input class="parse-field" id="g4" placeholder="M/F/N"></td>
    <td><input class="parse-field-lg" id="p4" placeholder="Attr/Pred/Sub"></td>
    <td><button class="reveal-btn" onclick="toggle('r4')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r4"><td colspan="7"><strong>A · S · M · Attributive</strong> — "the faithful word" (direct object)</td></tr>

  <tr>
    <td>5</td><td class="gk">ὁ λόγος πιστός</td>
    <td><input class="parse-field" id="c5" placeholder="N/G/D/A"></td>
    <td><input class="parse-field" id="n5" placeholder="S/P"></td>
    <td><input class="parse-field" id="g5" placeholder="M/F/N"></td>
    <td><input class="parse-field-lg" id="p5" placeholder="Attr/Pred/Sub"></td>
    <td><button class="reveal-btn" onclick="toggle('r5')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r5"><td colspan="7"><strong>N · S · M · Predicate</strong> — "The word is faithful."</td></tr>

  <tr>
    <td>6</td><td class="gk">τῆς καλῆς ὁδοῦ</td>
    <td><input class="parse-field" id="c6" placeholder="N/G/D/A"></td>
    <td><input class="parse-field" id="n6" placeholder="S/P"></td>
    <td><input class="parse-field" id="g6" placeholder="M/F/N"></td>
    <td><input class="parse-field-lg" id="p6" placeholder="Attr/Pred/Sub"></td>
    <td><button class="reveal-btn" onclick="toggle('r6')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r6"><td colspan="7"><strong>G · S · F · Attributive</strong> — "of the beautiful road"</td></tr>

  <tr>
    <td>7</td><td class="gk">ἡ ὁδὸς καλή</td>
    <td><input class="parse-field" id="c7" placeholder="N/G/D/A"></td>
    <td><input class="parse-field" id="n7" placeholder="S/P"></td>
    <td><input class="parse-field" id="g7" placeholder="M/F/N"></td>
    <td><input class="parse-field-lg" id="p7" placeholder="Attr/Pred/Sub"></td>
    <td><button class="reveal-btn" onclick="toggle('r7')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r7"><td colspan="7"><strong>N · S · F · Predicate</strong> — "The road is beautiful."</td></tr>

  <tr>
    <td>8</td><td class="gk">τὰ ἀγαθά</td>
    <td><input class="parse-field" id="c8" placeholder="N/G/D/A"></td>
    <td><input class="parse-field" id="n8" placeholder="S/P"></td>
    <td><input class="parse-field" id="g8" placeholder="M/F/N"></td>
    <td><input class="parse-field-lg" id="p8" placeholder="Attr/Pred/Sub"></td>
    <td><button class="reveal-btn" onclick="toggle('r8')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r8"><td colspan="7"><strong>N · P · N · Substantival</strong> — art + adj; no noun; "the good things"</td></tr>

  <tr>
    <td>9</td><td class="gk">τοῖς πιστοῖς δούλοις</td>
    <td><input class="parse-field" id="c9" placeholder="N/G/D/A"></td>
    <td><input class="parse-field" id="n9" placeholder="S/P"></td>
    <td><input class="parse-field" id="g9" placeholder="M/F/N"></td>
    <td><input class="parse-field-lg" id="p9" placeholder="Attr/Pred/Sub"></td>
    <td><button class="reveal-btn" onclick="toggle('r9')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r9"><td colspan="7"><strong>D · P · M · Attributive</strong> — "to/for the faithful slaves"</td></tr>

  <tr>
    <td>10</td><td class="gk">ἡ πιστή</td>
    <td><input class="parse-field" id="c10" placeholder="N/G/D/A"></td>
    <td><input class="parse-field" id="n10" placeholder="S/P"></td>
    <td><input class="parse-field" id="g10" placeholder="M/F/N"></td>
    <td><input class="parse-field-lg" id="p10" placeholder="Attr/Pred/Sub"></td>
    <td><button class="reveal-btn" onclick="toggle('r10')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r10"><td colspan="7"><strong>N · S · F · Substantival</strong> — "the faithful woman"</td></tr>

  <tr>
    <td>11</td><td class="gk">τοῦ ἀγαθοῦ ἔργου</td>
    <td><input class="parse-field" id="c11" placeholder="N/G/D/A"></td>
    <td><input class="parse-field" id="n11" placeholder="S/P"></td>
    <td><input class="parse-field" id="g11" placeholder="M/F/N"></td>
    <td><input class="parse-field-lg" id="p11" placeholder="Attr/Pred/Sub"></td>
    <td><button class="reveal-btn" onclick="toggle('r11')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r11"><td colspan="7"><strong>G · S · N · Attributive</strong> — "of the good work"</td></tr>

  <tr>
    <td>12</td><td class="gk">τὸ ἔργον ἀγαθόν</td>
    <td><input class="parse-field" id="c12" placeholder="N/G/D/A"></td>
    <td><input class="parse-field" id="n12" placeholder="S/P"></td>
    <td><input class="parse-field" id="g12" placeholder="M/F/N"></td>
    <td><input class="parse-field-lg" id="p12" placeholder="Attr/Pred/Sub"></td>
    <td><button class="reveal-btn" onclick="toggle('r12')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r12"><td colspan="7"><strong>N · S · N · Predicate</strong> — "The work is good."</td></tr>

  <tr>
    <td>13</td><td class="gk">ὁ πονηρὸς ἄνθρωπος</td>
    <td><input class="parse-field" id="c13" placeholder="N/G/D/A"></td>
    <td><input class="parse-field" id="n13" placeholder="S/P"></td>
    <td><input class="parse-field" id="g13" placeholder="M/F/N"></td>
    <td><input class="parse-field-lg" id="p13" placeholder="Attr/Pred/Sub"></td>
    <td><button class="reveal-btn" onclick="toggle('r13')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r13"><td colspan="7"><strong>N · S · M · Attributive</strong> — "the evil man"</td></tr>

  <tr>
    <td>14</td><td class="gk">οἱ πιστοὶ ἀπόστολοι</td>
    <td><input class="parse-field" id="c14" placeholder="N/G/D/A"></td>
    <td><input class="parse-field" id="n14" placeholder="S/P"></td>
    <td><input class="parse-field" id="g14" placeholder="M/F/N"></td>
    <td><input class="parse-field-lg" id="p14" placeholder="Attr/Pred/Sub"></td>
    <td><button class="reveal-btn" onclick="toggle('r14')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r14"><td colspan="7"><strong>N · P · M · Attributive</strong> — "the faithful apostles"</td></tr>

  <tr>
    <td>15</td><td class="gk">τοὺς δικαίους</td>
    <td><input class="parse-field" id="c15" placeholder="N/G/D/A"></td>
    <td><input class="parse-field" id="n15" placeholder="S/P"></td>
    <td><input class="parse-field" id="g15" placeholder="M/F/N"></td>
    <td><input class="parse-field-lg" id="p15" placeholder="Attr/Pred/Sub"></td>
    <td><button class="reveal-btn" onclick="toggle('r15')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r15"><td colspan="7"><strong>A · P · M · Substantival</strong> — "the righteous ones"</td></tr>

  <tr>
    <td>16</td><td class="gk">ἀγαθὴ ἡ ὁδός</td>
    <td><input class="parse-field" id="c16" placeholder="N/G/D/A"></td>
    <td><input class="parse-field" id="n16" placeholder="S/P"></td>
    <td><input class="parse-field" id="g16" placeholder="M/F/N"></td>
    <td><input class="parse-field-lg" id="p16" placeholder="Attr/Pred/Sub"></td>
    <td><button class="reveal-btn" onclick="toggle('r16')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r16"><td colspan="7"><strong>N · S · F · Predicate</strong> — adj before art-noun; "The road is good."</td></tr>

  <tr>
    <td>17</td><td class="gk">τῷ ἀγαθῷ νόμῳ</td>
    <td><input class="parse-field" id="c17" placeholder="N/G/D/A"></td>
    <td><input class="parse-field" id="n17" placeholder="S/P"></td>
    <td><input class="parse-field" id="g17" placeholder="M/F/N"></td>
    <td><input class="parse-field-lg" id="p17" placeholder="Attr/Pred/Sub"></td>
    <td><button class="reveal-btn" onclick="toggle('r17')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r17"><td colspan="7"><strong>D · S · M · Attributive</strong> — "by/in the good law"</td></tr>

  <tr>
    <td>18</td><td class="gk">τὸ πονηρόν</td>
    <td><input class="parse-field" id="c18" placeholder="N/G/D/A"></td>
    <td><input class="parse-field" id="n18" placeholder="S/P"></td>
    <td><input class="parse-field" id="g18" placeholder="M/F/N"></td>
    <td><input class="parse-field-lg" id="p18" placeholder="Attr/Pred/Sub"></td>
    <td><button class="reveal-btn" onclick="toggle('r18')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r18"><td colspan="7"><strong>N · S · N · Substantival</strong> — "the evil thing"</td></tr>

  <tr>
    <td>19</td><td class="gk">τῶν πιστῶν ἔργων</td>
    <td><input class="parse-field" id="c19" placeholder="N/G/D/A"></td>
    <td><input class="parse-field" id="n19" placeholder="S/P"></td>
    <td><input class="parse-field" id="g19" placeholder="M/F/N"></td>
    <td><input class="parse-field-lg" id="p19" placeholder="Attr/Pred/Sub"></td>
    <td><button class="reveal-btn" onclick="toggle('r19')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r19"><td colspan="7"><strong>G · P · N · Attributive</strong> — "of the faithful works"</td></tr>

  <tr>
    <td>20</td><td class="gk">ὁ νόμος ἅγιος</td>
    <td><input class="parse-field" id="c20" placeholder="N/G/D/A"></td>
    <td><input class="parse-field" id="n20" placeholder="S/P"></td>
    <td><input class="parse-field" id="g20" placeholder="M/F/N"></td>
    <td><input class="parse-field-lg" id="p20" placeholder="Attr/Pred/Sub"></td>
    <td><button class="reveal-btn" onclick="toggle('r20')">&#9658; Answer</button></td>
  </tr>
  <tr class="answer-row" id="r20"><td colspan="7"><strong>N · S · M · Predicate</strong> — "The law is holy." (cf. Rom 7:12)</td></tr>

</table></div>

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

