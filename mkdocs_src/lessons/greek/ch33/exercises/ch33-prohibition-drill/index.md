# Prohibition Drill

*Chapter 33 — Imperative*

[Full screen](ch33-prohibition-drill.html){.md-button}  [Markdown](ch33-prohibition-drill.md){.md-button}  [Print (PDF)](ch33-prohibition-drill.pdf){.md-button}

<style>

  body { font-family: Georgia, serif;    color: #222; }
  h1 { font-size: 1.4em; border-bottom: 2px solid #333; padding-bottom: .3em; }
  h2 { font-size: 1.1em; margin-top: 1.8em; border-bottom: 1px solid #aaa; padding-bottom: .2em; }
  .subtitle { color: #555; font-style: italic; margin: .3em 0 1em; }
  .instructions { background: #f9f9f0; border-left: 3px solid #c8a000; padding: .7em 1em; margin-bottom: 1.5em; font-size: .95em; }
  table { border-collapse: collapse;  margin-bottom: 1em; font-size: .93em; }
  th { background: #3a5a8a; color: #fff; padding: .45em .6em; text-align: left; }
  td { padding: .4em .6em; vertical-align: top; border-bottom: 1px solid #ddd; }
  tr:nth-child(even) td { background: #f5f7fb; }
  .greek { font-size: 1.15em; font-weight: bold; }
  .parse-field { width: 95%; border: none; border-bottom: 1px solid #888; background: transparent; font-family: inherit; font-size: .92em; padding: 2px 0; }
  .parse-field:focus { outline: none; border-bottom: 2px solid #3a5a8a; }
  .answer-row { display: none; background: #e8f5e9 !important; }
  .answer-row td { color: #2e7d32; font-style: italic; font-size: .9em; }
  .btn-reveal { background: #3a5a8a; color: #fff; border: none; border-radius: 3px; padding: .25em .7em; cursor: pointer; font-size: .85em; white-space: nowrap; }
  .btn-reveal:hover { background: #2c4470; }
  .controls { margin: 1em 0 1.5em; display: flex; gap: .7em; flex-wrap: wrap; }
  .btn-ctrl { background: #555; color: #fff; border: none; border-radius: 4px; padding: .4em 1em; cursor: pointer; font-size: .9em; }
  .btn-ctrl:hover { background: #333; }
  .item-num { font-weight: bold; min-width: 1.5em; }
  @media print {
    .btn-reveal, .controls { display: none !important; }
    .answer-row { display: none !important; }
    .parse-field { border-bottom: 1px solid #999; }
    body {  }
  }

</style>

<h1>BBG Chapter 33 — Prohibition Pattern Drill</h1>
<p class="subtitle"><em>BBG Chapter 33 · μή + Present Imperative vs. μή + Aorist Subjunctive</em></p>

<div class="instructions">
  <strong>Instructions:</strong> For each item, (1) classify the prohibition as STOP (μή + present imperative = stop an ongoing action)
  or DONT (μή + aorist subjunctive = do not begin), (2) give the tense and mood of the verbal form,
  (3) give the lexical form (1st sg present active indicative), and (4) translate.
  Click <strong>▶ Answer</strong> to reveal the answer for that row.
</div>

<div class="controls">
  <button class="btn-ctrl" onclick="showAll()">Show All Answers</button>
  <button class="btn-ctrl" onclick="hideAll()">Hide All Answers</button>
  <button class="btn-ctrl" onclick="clearAll()">Clear All Inputs</button>
</div>

<div style="overflow-x:auto;max-width:100%;"><table>
<thead>
  <tr><th>#</th><th>Greek Sentence</th><th>Pattern (STOP/DONT)</th><th>Tense</th><th>Mood</th><th>Lexical Form</th><th>Translation</th><th></th></tr>
</thead>
<tbody>

<tr class="question-row" data-id="1">
  <td class="item-num">1</td>
  <td class="greek">μὴ κλαίετε</td>
  <td><input class="parse-field" placeholder="STOP/DONT"></td>
  <td><input class="parse-field" placeholder="tense"></td>
  <td><input class="parse-field" placeholder="mood"></td>
  <td><input class="parse-field" placeholder="lexical form"></td>
  <td><input class="parse-field" placeholder="translation"></td>
  <td><button class="btn-reveal" onclick="toggleAnswer(1)">▶ Answer</button></td>
</tr>
<tr class="answer-row" id="ans-1">
  <td></td>
  <td colspan="6">STOP · Present · Imperative · κλαίω · Stop weeping</td>
  <td></td>
</tr>

<tr class="question-row" data-id="2">
  <td class="item-num">2</td>
  <td class="greek">μὴ φοβηθῇς</td>
  <td><input class="parse-field" placeholder="STOP/DONT"></td>
  <td><input class="parse-field" placeholder="tense"></td>
  <td><input class="parse-field" placeholder="mood"></td>
  <td><input class="parse-field" placeholder="lexical form"></td>
  <td><input class="parse-field" placeholder="translation"></td>
  <td><button class="btn-reveal" onclick="toggleAnswer(2)">▶ Answer</button></td>
</tr>
<tr class="answer-row" id="ans-2">
  <td></td>
  <td colspan="6">DONT · Aorist · Subjunctive · φοβέομαι · Do not be afraid (don't start)</td>
  <td></td>
</tr>

<tr class="question-row" data-id="3">
  <td class="item-num">3</td>
  <td class="greek">μὴ νομίζετε ὅτι ἦλθον</td>
  <td><input class="parse-field" placeholder="STOP/DONT"></td>
  <td><input class="parse-field" placeholder="tense"></td>
  <td><input class="parse-field" placeholder="mood"></td>
  <td><input class="parse-field" placeholder="lexical form"></td>
  <td><input class="parse-field" placeholder="translation"></td>
  <td><button class="btn-reveal" onclick="toggleAnswer(3)">▶ Answer</button></td>
</tr>
<tr class="answer-row" id="ans-3">
  <td></td>
  <td colspan="6">STOP · Present · Imperative · νομίζω · Do not think (stop thinking) that I came</td>
  <td></td>
</tr>

<tr class="question-row" data-id="4">
  <td class="item-num">4</td>
  <td class="greek">μὴ εἰσέλθῃς εἰς πειρασμόν</td>
  <td><input class="parse-field" placeholder="STOP/DONT"></td>
  <td><input class="parse-field" placeholder="tense"></td>
  <td><input class="parse-field" placeholder="mood"></td>
  <td><input class="parse-field" placeholder="lexical form"></td>
  <td><input class="parse-field" placeholder="translation"></td>
  <td><button class="btn-reveal" onclick="toggleAnswer(4)">▶ Answer</button></td>
</tr>
<tr class="answer-row" id="ans-4">
  <td></td>
  <td colspan="6">DONT · Aorist · Subjunctive · εἰσέρχομαι · Do not enter into temptation</td>
  <td></td>
</tr>

<tr class="question-row" data-id="5">
  <td class="item-num">5</td>
  <td class="greek">μὴ μεριμνᾶτε</td>
  <td><input class="parse-field" placeholder="STOP/DONT"></td>
  <td><input class="parse-field" placeholder="tense"></td>
  <td><input class="parse-field" placeholder="mood"></td>
  <td><input class="parse-field" placeholder="lexical form"></td>
  <td><input class="parse-field" placeholder="translation"></td>
  <td><button class="btn-reveal" onclick="toggleAnswer(5)">▶ Answer</button></td>
</tr>
<tr class="answer-row" id="ans-5">
  <td></td>
  <td colspan="6">STOP · Present · Imperative · μεριμνάω · Stop worrying</td>
  <td></td>
</tr>

<tr class="question-row" data-id="6">
  <td class="item-num">6</td>
  <td class="greek">μὴ λαλήσῃς κακόν</td>
  <td><input class="parse-field" placeholder="STOP/DONT"></td>
  <td><input class="parse-field" placeholder="tense"></td>
  <td><input class="parse-field" placeholder="mood"></td>
  <td><input class="parse-field" placeholder="lexical form"></td>
  <td><input class="parse-field" placeholder="translation"></td>
  <td><button class="btn-reveal" onclick="toggleAnswer(6)">▶ Answer</button></td>
</tr>
<tr class="answer-row" id="ans-6">
  <td></td>
  <td colspan="6">DONT · Aorist · Subjunctive · λαλέω · Do not speak evil</td>
  <td></td>
</tr>

<tr class="question-row" data-id="7">
  <td class="item-num">7</td>
  <td class="greek">μὴ θαυμάζετε</td>
  <td><input class="parse-field" placeholder="STOP/DONT"></td>
  <td><input class="parse-field" placeholder="tense"></td>
  <td><input class="parse-field" placeholder="mood"></td>
  <td><input class="parse-field" placeholder="lexical form"></td>
  <td><input class="parse-field" placeholder="translation"></td>
  <td><button class="btn-reveal" onclick="toggleAnswer(7)">▶ Answer</button></td>
</tr>
<tr class="answer-row" id="ans-7">
  <td></td>
  <td colspan="6">STOP · Present · Imperative · θαυμάζω · Stop marveling</td>
  <td></td>
</tr>

<tr class="question-row" data-id="8">
  <td class="item-num">8</td>
  <td class="greek">μὴ πορευθῇς</td>
  <td><input class="parse-field" placeholder="STOP/DONT"></td>
  <td><input class="parse-field" placeholder="tense"></td>
  <td><input class="parse-field" placeholder="mood"></td>
  <td><input class="parse-field" placeholder="lexical form"></td>
  <td><input class="parse-field" placeholder="translation"></td>
  <td><button class="btn-reveal" onclick="toggleAnswer(8)">▶ Answer</button></td>
</tr>
<tr class="answer-row" id="ans-8">
  <td></td>
  <td colspan="6">DONT · Aorist · Subjunctive · πορεύομαι · Do not go</td>
  <td></td>
</tr>

<tr class="question-row" data-id="9">
  <td class="item-num">9</td>
  <td class="greek">μὴ λέγε τοῦτο</td>
  <td><input class="parse-field" placeholder="STOP/DONT"></td>
  <td><input class="parse-field" placeholder="tense"></td>
  <td><input class="parse-field" placeholder="mood"></td>
  <td><input class="parse-field" placeholder="lexical form"></td>
  <td><input class="parse-field" placeholder="translation"></td>
  <td><button class="btn-reveal" onclick="toggleAnswer(9)">▶ Answer</button></td>
</tr>
<tr class="answer-row" id="ans-9">
  <td></td>
  <td colspan="6">STOP · Present · Imperative · λέγω · Stop saying this</td>
  <td></td>
</tr>

<tr class="question-row" data-id="10">
  <td class="item-num">10</td>
  <td class="greek">μὴ ἅψῃ</td>
  <td><input class="parse-field" placeholder="STOP/DONT"></td>
  <td><input class="parse-field" placeholder="tense"></td>
  <td><input class="parse-field" placeholder="mood"></td>
  <td><input class="parse-field" placeholder="lexical form"></td>
  <td><input class="parse-field" placeholder="translation"></td>
  <td><button class="btn-reveal" onclick="toggleAnswer(10)">▶ Answer</button></td>
</tr>
<tr class="answer-row" id="ans-10">
  <td></td>
  <td colspan="6">DONT · Aorist · Subjunctive · ἅπτω · Do not touch</td>
  <td></td>
</tr>

<tr class="question-row" data-id="11">
  <td class="item-num">11</td>
  <td class="greek">μὴ φοβεῖσθε</td>
  <td><input class="parse-field" placeholder="STOP/DONT"></td>
  <td><input class="parse-field" placeholder="tense"></td>
  <td><input class="parse-field" placeholder="mood"></td>
  <td><input class="parse-field" placeholder="lexical form"></td>
  <td><input class="parse-field" placeholder="translation"></td>
  <td><button class="btn-reveal" onclick="toggleAnswer(11)">▶ Answer</button></td>
</tr>
<tr class="answer-row" id="ans-11">
  <td></td>
  <td colspan="6">STOP · Present · Imperative · φοβέομαι · Stop being afraid</td>
  <td></td>
</tr>

<tr class="question-row" data-id="12">
  <td class="item-num">12</td>
  <td class="greek">μὴ ἀποκτείνῃς</td>
  <td><input class="parse-field" placeholder="STOP/DONT"></td>
  <td><input class="parse-field" placeholder="tense"></td>
  <td><input class="parse-field" placeholder="mood"></td>
  <td><input class="parse-field" placeholder="lexical form"></td>
  <td><input class="parse-field" placeholder="translation"></td>
  <td><button class="btn-reveal" onclick="toggleAnswer(12)">▶ Answer</button></td>
</tr>
<tr class="answer-row" id="ans-12">
  <td></td>
  <td colspan="6">DONT · Aorist · Subjunctive · ἀποκτείνω · Do not kill</td>
  <td></td>
</tr>

<tr class="question-row" data-id="13">
  <td class="item-num">13</td>
  <td class="greek">μὴ κρίνετε</td>
  <td><input class="parse-field" placeholder="STOP/DONT"></td>
  <td><input class="parse-field" placeholder="tense"></td>
  <td><input class="parse-field" placeholder="mood"></td>
  <td><input class="parse-field" placeholder="lexical form"></td>
  <td><input class="parse-field" placeholder="translation"></td>
  <td><button class="btn-reveal" onclick="toggleAnswer(13)">▶ Answer</button></td>
</tr>
<tr class="answer-row" id="ans-13">
  <td></td>
  <td colspan="6">STOP · Present · Imperative · κρίνω · Do not judge (stop judging)</td>
  <td></td>
</tr>

<tr class="question-row" data-id="14">
  <td class="item-num">14</td>
  <td class="greek">μὴ ἁμάρτῃς</td>
  <td><input class="parse-field" placeholder="STOP/DONT"></td>
  <td><input class="parse-field" placeholder="tense"></td>
  <td><input class="parse-field" placeholder="mood"></td>
  <td><input class="parse-field" placeholder="lexical form"></td>
  <td><input class="parse-field" placeholder="translation"></td>
  <td><button class="btn-reveal" onclick="toggleAnswer(14)">▶ Answer</button></td>
</tr>
<tr class="answer-row" id="ans-14">
  <td></td>
  <td colspan="6">DONT · Aorist · Subjunctive · ἁμαρτάνω · Do not sin</td>
  <td></td>
</tr>

<tr class="question-row" data-id="15">
  <td class="item-num">15</td>
  <td class="greek">μὴ κατεσθίετε τοὺς πτωχούς</td>
  <td><input class="parse-field" placeholder="STOP/DONT"></td>
  <td><input class="parse-field" placeholder="tense"></td>
  <td><input class="parse-field" placeholder="mood"></td>
  <td><input class="parse-field" placeholder="lexical form"></td>
  <td><input class="parse-field" placeholder="translation"></td>
  <td><button class="btn-reveal" onclick="toggleAnswer(15)">▶ Answer</button></td>
</tr>
<tr class="answer-row" id="ans-15">
  <td></td>
  <td colspan="6">STOP · Present · Imperative · κατεσθίω · Stop devouring the poor</td>
  <td></td>
</tr>

<tr class="question-row" data-id="16">
  <td class="item-num">16</td>
  <td class="greek">μὴ ἄρῃς τὸ σκεῦος</td>
  <td><input class="parse-field" placeholder="STOP/DONT"></td>
  <td><input class="parse-field" placeholder="tense"></td>
  <td><input class="parse-field" placeholder="mood"></td>
  <td><input class="parse-field" placeholder="lexical form"></td>
  <td><input class="parse-field" placeholder="translation"></td>
  <td><button class="btn-reveal" onclick="toggleAnswer(16)">▶ Answer</button></td>
</tr>
<tr class="answer-row" id="ans-16">
  <td></td>
  <td colspan="6">DONT · Aorist · Subjunctive · αἴρω · Do not take the vessel</td>
  <td></td>
</tr>

<tr class="question-row" data-id="17">
  <td class="item-num">17</td>
  <td class="greek">μὴ ἐπιθυμεῖτε</td>
  <td><input class="parse-field" placeholder="STOP/DONT"></td>
  <td><input class="parse-field" placeholder="tense"></td>
  <td><input class="parse-field" placeholder="mood"></td>
  <td><input class="parse-field" placeholder="lexical form"></td>
  <td><input class="parse-field" placeholder="translation"></td>
  <td><button class="btn-reveal" onclick="toggleAnswer(17)">▶ Answer</button></td>
</tr>
<tr class="answer-row" id="ans-17">
  <td></td>
  <td colspan="6">STOP · Present · Imperative · ἐπιθυμέω · Stop desiring (do not covet)</td>
  <td></td>
</tr>

<tr class="question-row" data-id="18">
  <td class="item-num">18</td>
  <td class="greek">μὴ πιστεύσῃς</td>
  <td><input class="parse-field" placeholder="STOP/DONT"></td>
  <td><input class="parse-field" placeholder="tense"></td>
  <td><input class="parse-field" placeholder="mood"></td>
  <td><input class="parse-field" placeholder="lexical form"></td>
  <td><input class="parse-field" placeholder="translation"></td>
  <td><button class="btn-reveal" onclick="toggleAnswer(18)">▶ Answer</button></td>
</tr>
<tr class="answer-row" id="ans-18">
  <td></td>
  <td colspan="6">DONT · Aorist · Subjunctive · πιστεύω · Do not believe</td>
  <td></td>
</tr>

<tr class="question-row" data-id="19">
  <td class="item-num">19</td>
  <td class="greek">μὴ δίδοτε τὸ ἅγιον τοῖς κυσίν</td>
  <td><input class="parse-field" placeholder="STOP/DONT"></td>
  <td><input class="parse-field" placeholder="tense"></td>
  <td><input class="parse-field" placeholder="mood"></td>
  <td><input class="parse-field" placeholder="lexical form"></td>
  <td><input class="parse-field" placeholder="translation"></td>
  <td><button class="btn-reveal" onclick="toggleAnswer(19)">▶ Answer</button></td>
</tr>
<tr class="answer-row" id="ans-19">
  <td></td>
  <td colspan="6">STOP · Present · Imperative · δίδωμι · Do not give what is holy to dogs</td>
  <td></td>
</tr>

<tr class="question-row" data-id="20">
  <td class="item-num">20</td>
  <td class="greek">μὴ ποιήσῃς τοῦτο</td>
  <td><input class="parse-field" placeholder="STOP/DONT"></td>
  <td><input class="parse-field" placeholder="tense"></td>
  <td><input class="parse-field" placeholder="mood"></td>
  <td><input class="parse-field" placeholder="lexical form"></td>
  <td><input class="parse-field" placeholder="translation"></td>
  <td><button class="btn-reveal" onclick="toggleAnswer(20)">▶ Answer</button></td>
</tr>
<tr class="answer-row" id="ans-20">
  <td></td>
  <td colspan="6">DONT · Aorist · Subjunctive · ποιέω · Do not do this</td>
  <td></td>
</tr>

</tbody>
</table></div>

<h2>Discussion Questions</h2>
<ol>
  <li>The rule "μή + present imperative = stop; μή + aorist subjunctive = don't begin" is a useful teaching heuristic. Give two items from the exercise where the "stop" nuance is clearly supported by the context and two where it seems more like a general prohibition. What does this tell you about how absolute the rule is?</li>
  <li>Item 19 uses δίδοτε — a present imperative of δίδωμι (a μι-verb). How does the form differ from a standard ω-verb present imperative? What is the 2nd plural present imperative ending for μι-verbs?</li>
  <li>Items 2 and 11 both use φοβέομαι — one is STOP (μή + present imperative) and one is DONT (μή + aorist subjunctive). Write both out with glosses and explain the pragmatic difference in context: when would a speaker choose each form?</li>
</ol>

<script>
function toggleAnswer(id) {
  const row = document.getElementById('ans-' + id);
  const btn = document.querySelector('[data-id="' + id + '"] .btn-reveal');
  if (row.style.display === 'table-row') {
    row.style.display = 'none';
    if (btn) btn.textContent = '▶ Answer';
  } else {
    row.style.display = 'table-row';
    if (btn) btn.textContent = '▼ Answer';
  }
}
function showAll() {
  document.querySelectorAll('.answer-row').forEach(r => r.style.display = 'table-row');
  document.querySelectorAll('.btn-reveal').forEach(b => b.textContent = '▼ Answer');
}
function hideAll() {
  document.querySelectorAll('.answer-row').forEach(r => r.style.display = 'none');
  document.querySelectorAll('.btn-reveal').forEach(b => b.textContent = '▶ Answer');
}
function clearAll() {
  document.querySelectorAll('.parse-field').forEach(f => f.value = '');
}
</script>

