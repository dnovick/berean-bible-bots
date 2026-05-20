# Infinitive Parsing

*Chapter 32 — Infinitive*

[Full screen](ch32-infinitive-parsing.html){.md-button}  [Markdown](ch32-infinitive-parsing.md){.md-button}  [Print (PDF)](ch32-infinitive-parsing.pdf){.md-button}

<style>

  body { font-family: Georgia, serif;    color: #222; }
  h1 { font-size: 1.4em; border-bottom: 2px solid #333; padding-bottom: .3em; }
  h2 { font-size: 1.1em; margin-top: 1.8em; border-bottom: 1px solid #aaa; }
  .subtitle { color: #555; font-style: italic; }
  .instructions { background: #f9f9f0; border-left: 3px solid #c8a000; padding: .7em 1em; margin: 1em 0 1.5em; font-size: .93em; }
  table { border-collapse: collapse; width: 100%; margin-bottom: 1em; font-size: .88em; }
  th { background: #2e7d32; color: #fff; padding: .4em .5em; text-align: left; }
  td { padding: .38em .5em; vertical-align: top; border-bottom: 1px solid #ddd; }
  tr:nth-child(even) td { background: #f1f8f1; }
  .greek { font-size: 1.08em; font-weight: bold; }
  .parse-field { width: 93%; border: none; border-bottom: 1px solid #888; background: transparent; font-family: inherit; font-size: .87em; padding: 2px 0; }
  .parse-field:focus { outline: none; border-bottom: 2px solid #2e7d32; }
  .answer-row { display: none; background: #e8f5e9 !important; }
  .answer-row td { color: #1b5e20; font-style: italic; font-size: .87em; }
  .btn-reveal { background: #2e7d32; color: #fff; border: none; border-radius: 3px; padding: .22em .6em; cursor: pointer; font-size: .82em; }
  .btn-reveal:hover { background: #1b5e20; }
  .controls { margin: 1em 0 1.5em; display: flex; gap: .7em; flex-wrap: wrap; }
  .btn-ctrl { background: #555; color: #fff; border: none; border-radius: 4px; padding: .4em 1em; cursor: pointer; font-size: .9em; }
  .btn-ctrl:hover { background: #333; }
  @media print { .btn-reveal, .controls { display: none !important; } .answer-row { display: none !important; } .parse-field { border-bottom: 1px solid #999; } }

</style>

<h1>BBG Chapter 32 — Infinitive Parsing</h1>
<p class="subtitle"><em>Basics of Biblical Greek Grammar, Mounce, 4th Edition</em></p>
<div class="instructions">
  Parse the underlined infinitive (tense / voice / lexical form), identify the use, and translate.
</div>
<div class="controls">
  <button class="btn-ctrl" onclick="showAll()">Show All Answers</button>
  <button class="btn-ctrl" onclick="hideAll()">Hide All Answers</button>
  <button class="btn-ctrl" onclick="clearAll()">Clear All Inputs</button>
</div>

<h2>Part A — Complementary (1–5)</h2>
<table>
<thead><tr><th>#</th><th>Greek Text</th><th>Tense</th><th>Voice</th><th>Lexical Form</th><th>Use</th><th>Translation</th><th></th></tr></thead>
<tbody>
<tr class="question-row" data-id="1"><td><b>1</b></td><td class="greek">θέλω <u>λύειν</u> τοὺς δούλους.</td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><button class="btn-reveal" onclick="toggleAnswer(1)">▶ Answer</button></td></tr>
<tr class="answer-row" id="ans-1"><td></td><td colspan="6">Pres · Act · λύω · Complementary · "I want to loose the slaves."</td><td></td></tr>

<tr class="question-row" data-id="2"><td><b>2</b></td><td class="greek">οὐκ εἰμὶ ἱκανὸς <u>λῦσαι</u> τὸν ἱμάντα τοῦ ὑποδήματος αὐτοῦ.</td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><button class="btn-reveal" onclick="toggleAnswer(2)">▶ Answer</button></td></tr>
<tr class="answer-row" id="ans-2"><td></td><td colspan="6">Aor · Act · λύω · Complementary · "I am not worthy to loose the strap of his sandal." (cf. Mark 1:7)</td><td></td></tr>

<tr class="question-row" data-id="3"><td><b>3</b></td><td class="greek">ἤρξατο <u>διδάσκειν</u> αὐτοὺς πολλά.</td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><button class="btn-reveal" onclick="toggleAnswer(3)">▶ Answer</button></td></tr>
<tr class="answer-row" id="ans-3"><td></td><td colspan="6">Pres · Act · διδάσκω · Complementary · "He began to teach them many things."</td><td></td></tr>

<tr class="question-row" data-id="4"><td><b>4</b></td><td class="greek">δύνασαι <u>ποιεῖν</u> τοῦτο;</td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><button class="btn-reveal" onclick="toggleAnswer(4)">▶ Answer</button></td></tr>
<tr class="answer-row" id="ans-4"><td></td><td colspan="6">Pres · Act · ποιέω · Complementary · "Are you able to do this?"</td><td></td></tr>

<tr class="question-row" data-id="5"><td><b>5</b></td><td class="greek">μέλλει γὰρ Ἡρῴδης <u>ζητεῖν</u> τὸ παιδίον.</td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><button class="btn-reveal" onclick="toggleAnswer(5)">▶ Answer</button></td></tr>
<tr class="answer-row" id="ans-5"><td></td><td colspan="6">Pres · Act · ζητέω · Complementary · "For Herod is about to seek the child." (cf. Matt 2:13)</td><td></td></tr>
</tbody>
</table>

<h2>Part B — Articular Infinitives (6–8)</h2>
<table>
<thead><tr><th>#</th><th>Greek Text</th><th>Tense</th><th>Voice</th><th>Lexical Form</th><th>Use</th><th>Translation</th><th></th></tr></thead>
<tbody>
<tr class="question-row" data-id="6"><td><b>6</b></td><td class="greek">τὸ <u>ζῆν</u> ἐμοὶ Χριστὸς καὶ τὸ ἀποθανεῖν κέρδος.</td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><button class="btn-reveal" onclick="toggleAnswer(6)">▶ Answer</button></td></tr>
<tr class="answer-row" id="ans-6"><td></td><td colspan="6">Pres · Act · ζάω · Articular (subject) · "For me to live is Christ and to die is gain." (Phil 1:21)</td><td></td></tr>

<tr class="question-row" data-id="7"><td><b>7</b></td><td class="greek">ἐξῆλθεν ὁ σπείρων τοῦ <u>σπεῖραι</u>.</td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><button class="btn-reveal" onclick="toggleAnswer(7)">▶ Answer</button></td></tr>
<tr class="answer-row" id="ans-7"><td></td><td colspan="6">Aor · Act · σπείρω · Articular — purpose (τοῦ) · "The sower went out to sow." (Matt 13:3)</td><td></td></tr>

<tr class="question-row" data-id="8"><td><b>8</b></td><td class="greek">ἐν τῷ <u>εἶναι</u> αὐτὸν ἐν τόπῳ τινί.</td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><button class="btn-reveal" onclick="toggleAnswer(8)">▶ Answer</button></td></tr>
<tr class="answer-row" id="ans-8"><td></td><td colspan="6">Pres · Act · εἰμί · Articular — temporal (ἐν τῷ) · "While he was in a certain place." (Luke 11:1)</td><td></td></tr>
</tbody>
</table>

<h2>Part C — Purpose (9–12)</h2>
<table>
<thead><tr><th>#</th><th>Greek Text</th><th>Tense</th><th>Voice</th><th>Lexical Form</th><th>Use</th><th>Translation</th><th></th></tr></thead>
<tbody>
<tr class="question-row" data-id="9"><td><b>9</b></td><td class="greek">εἰσῆλθεν εἰς τὸ <u>σπεῖραι</u> τὸν λόγον.</td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><button class="btn-reveal" onclick="toggleAnswer(9)">▶ Answer</button></td></tr>
<tr class="answer-row" id="ans-9"><td></td><td colspan="6">Aor · Act · σπείρω · Purpose (εἰς τό) · "He went in to sow the word."</td><td></td></tr>

<tr class="question-row" data-id="10"><td><b>10</b></td><td class="greek">πρὸς τὸ <u>θεαθῆναι</u> αὐτοῖς.</td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><button class="btn-reveal" onclick="toggleAnswer(10)">▶ Answer</button></td></tr>
<tr class="answer-row" id="ans-10"><td></td><td colspan="6">Aor · Pass · θεάομαι · Purpose (πρός τό) · "So as to be seen by them." (Matt 6:1)</td><td></td></tr>

<tr class="question-row" data-id="11"><td><b>11</b></td><td class="greek">ἦλθεν εἰς τὸ <u>βαπτισθῆναι</u> ὑπ᾽ αὐτοῦ.</td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><button class="btn-reveal" onclick="toggleAnswer(11)">▶ Answer</button></td></tr>
<tr class="answer-row" id="ans-11"><td></td><td colspan="6">Aor · Pass · βαπτίζω · Purpose (εἰς τό) · "He came to be baptized by him." (cf. Matt 3:13)</td><td></td></tr>

<tr class="question-row" data-id="12"><td><b>12</b></td><td class="greek">τοῦ <u>γνῶναι</u> αὐτὸν καὶ τὴν δύναμιν τῆς ἀναστάσεως αὐτοῦ.</td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><button class="btn-reveal" onclick="toggleAnswer(12)">▶ Answer</button></td></tr>
<tr class="answer-row" id="ans-12"><td></td><td colspan="6">Aor · Act · γινώσκω · Purpose (τοῦ) · "To know him and the power of his resurrection." (Phil 3:10)</td><td></td></tr>
</tbody>
</table>

<h2>Part D — Result (13–15)</h2>
<table>
<thead><tr><th>#</th><th>Greek Text</th><th>Tense</th><th>Voice</th><th>Lexical Form</th><th>Use</th><th>Translation</th><th></th></tr></thead>
<tbody>
<tr class="question-row" data-id="13"><td><b>13</b></td><td class="greek">ὥστε τοὺς ὄχλους <u>θαυμάζειν</u>.</td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><button class="btn-reveal" onclick="toggleAnswer(13)">▶ Answer</button></td></tr>
<tr class="answer-row" id="ans-13"><td></td><td colspan="6">Pres · Act · θαυμάζω · Result (ὥστε) · "So that the crowds marveled." (Matt 15:31)</td><td></td></tr>

<tr class="question-row" data-id="14"><td><b>14</b></td><td class="greek">ὥστε μηκέτι αὐτὸν δύνασθαι εἰς πόλιν <u>εἰσελθεῖν</u>.</td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><button class="btn-reveal" onclick="toggleAnswer(14)">▶ Answer</button></td></tr>
<tr class="answer-row" id="ans-14"><td></td><td colspan="6">Aor · Act · εἰσέρχομαι · Complementary within result clause (ὥστε) · "So that he was no longer able to enter a city." (cf. Mark 2:2)</td><td></td></tr>

<tr class="question-row" data-id="15"><td><b>15</b></td><td class="greek">ὥστε τὸ πλοῖον <u>καλύπτεσθαι</u> ὑπὸ τῶν κυμάτων.</td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><button class="btn-reveal" onclick="toggleAnswer(15)">▶ Answer</button></td></tr>
<tr class="answer-row" id="ans-15"><td></td><td colspan="6">Pres · Pass · καλύπτω · Result (ὥστε) · "So that the boat was being covered by the waves." (Matt 8:24)</td><td></td></tr>
</tbody>
</table>

<h2>Part E — Indirect Discourse and Temporal (16–20)</h2>
<table>
<thead><tr><th>#</th><th>Greek Text</th><th>Tense</th><th>Voice</th><th>Lexical Form</th><th>Use</th><th>Translation</th><th></th></tr></thead>
<tbody>
<tr class="question-row" data-id="16"><td><b>16</b></td><td class="greek">νομίζουσιν αὐτὸν <u>εἶναι</u> ἐν τῇ συνοδίᾳ.</td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><button class="btn-reveal" onclick="toggleAnswer(16)">▶ Answer</button></td></tr>
<tr class="answer-row" id="ans-16"><td></td><td colspan="6">Pres · Act · εἰμί · Indirect discourse · "They suppose him to be in the traveling company." (Luke 2:44)</td><td></td></tr>

<tr class="question-row" data-id="17"><td><b>17</b></td><td class="greek">λέγουσιν αὐτὸν <u>ἐγηγέρθαι</u> ἐκ νεκρῶν.</td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><button class="btn-reveal" onclick="toggleAnswer(17)">▶ Answer</button></td></tr>
<tr class="answer-row" id="ans-17"><td></td><td colspan="6">Perf · Pass · ἐγείρω · Indirect discourse · "They say that he has been raised from the dead." (cf. Matt 28:7)</td><td></td></tr>

<tr class="question-row" data-id="18"><td><b>18</b></td><td class="greek">πιστεύομεν τὸν Ἰησοῦν <u>ἀποθανεῖν</u> καὶ ἀναστῆναι.</td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><button class="btn-reveal" onclick="toggleAnswer(18)">▶ Answer</button></td></tr>
<tr class="answer-row" id="ans-18"><td></td><td colspan="6">Aor · Act · ἀποθνῄσκω · Indirect discourse · "We believe that Jesus died and rose again." (1 Thess 4:14)</td><td></td></tr>

<tr class="question-row" data-id="19"><td><b>19</b></td><td class="greek">ἐν τῷ <u>σπείρειν</u> αὐτόν, ἃ μὲν ἔπεσεν παρὰ τὴν ὁδόν.</td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><button class="btn-reveal" onclick="toggleAnswer(19)">▶ Answer</button></td></tr>
<tr class="answer-row" id="ans-19"><td></td><td colspan="6">Pres · Act · σπείρω · Temporal (ἐν τῷ) · "While he was sowing, some fell along the path." (Matt 13:4)</td><td></td></tr>

<tr class="question-row" data-id="20"><td><b>20</b></td><td class="greek">ἐν τῷ <u>κατεβαίνειν</u> αὐτὸν εἰς τὴν Ἰεριχώ, τυφλοί τινες ἐκάθηντο.</td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><button class="btn-reveal" onclick="toggleAnswer(20)">▶ Answer</button></td></tr>
<tr class="answer-row" id="ans-20"><td></td><td colspan="6">Pres · Act · καταβαίνω · Temporal (ἐν τῷ) · "As he was going down to Jericho, some blind men were sitting there."</td><td></td></tr>
</tbody>
</table>

<script>
function toggleAnswer(id) {
  const row = document.getElementById('ans-' + id);
  const btn = document.querySelector('[data-id="' + id + '"] .btn-reveal');
  if (row.style.display === 'table-row') { row.style.display = 'none'; if (btn) btn.textContent = '▶ Answer'; }
  else { row.style.display = 'table-row'; if (btn) btn.textContent = '▼ Answer'; }
}
function showAll() { document.querySelectorAll('.answer-row').forEach(r => r.style.display = 'table-row'); document.querySelectorAll('.btn-reveal').forEach(b => b.textContent = '▼ Answer'); }
function hideAll() { document.querySelectorAll('.answer-row').forEach(r => r.style.display = 'none'); document.querySelectorAll('.btn-reveal').forEach(b => b.textContent = '▶ Answer'); }
function clearAll() { document.querySelectorAll('.parse-field').forEach(f => f.value = ''); }
</script>

