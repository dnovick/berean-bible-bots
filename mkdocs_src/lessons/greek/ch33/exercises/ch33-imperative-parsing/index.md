# Imperative Parsing

*Chapter 33 — Imperative*

[Full screen](ch33-imperative-parsing.html){.md-button}  [Markdown](ch33-imperative-parsing.md){.md-button}  [Print (PDF)](ch33-imperative-parsing.pdf){.md-button}

<style>

  body { font-family: Georgia, serif;    color: #222; }
  h1 { font-size: 1.4em; border-bottom: 2px solid #333; padding-bottom: .3em; }
  h2 { font-size: 1.1em; margin-top: 1.8em; border-bottom: 1px solid #aaa; }
  .subtitle { color: #555; font-style: italic; }
  .instructions { background: #f9f9f0; border-left: 3px solid #c8a000; padding: .7em 1em; margin: 1em 0 1.5em; font-size: .93em; }
  table { border-collapse: collapse; width: 100%; margin-bottom: 1em; font-size: .88em; }
  th { background: #880e4f; color: #fff; padding: .4em .5em; text-align: left; }
  td { padding: .38em .5em; vertical-align: top; border-bottom: 1px solid #ddd; }
  tr:nth-child(even) td { background: #fce4ec; }
  .greek { font-size: 1.08em; font-weight: bold; }
  .parse-field { width: 93%; border: none; border-bottom: 1px solid #888; background: transparent; font-family: inherit; font-size: .87em; padding: 2px 0; }
  .parse-field:focus { outline: none; border-bottom: 2px solid #880e4f; }
  .answer-row { display: none; background: #f8bbd0 !important; }
  .answer-row td { color: #560027; font-style: italic; font-size: .87em; }
  .btn-reveal { background: #880e4f; color: #fff; border: none; border-radius: 3px; padding: .22em .6em; cursor: pointer; font-size: .82em; }
  .btn-reveal:hover { background: #560027; }
  .controls { margin: 1em 0 1.5em; display: flex; gap: .7em; flex-wrap: wrap; }
  .btn-ctrl { background: #555; color: #fff; border: none; border-radius: 4px; padding: .4em 1em; cursor: pointer; font-size: .9em; }
  .btn-ctrl:hover { background: #333; }
  @media print { .btn-reveal, .controls { display: none !important; } .answer-row { display: none !important; } .parse-field { border-bottom: 1px solid #999; } }

</style>

<div class="download-links" style="margin:1rem 0 .5rem;font-size:.85rem;">
  <strong>Also available:</strong>
  <a href="ch33-imperative-parsing.md" style="margin-left:.5rem;">&#128196; Markdown</a>
  <span style="margin:0 .3rem;color:#aaa;">|</span>
  <a href="ch33-imperative-parsing.pdf">&#128209; PDF</a>
</div>

<h1>BBG Chapter 33 — Imperative Parsing</h1>
<p class="subtitle"><em>Basics of Biblical Greek Grammar, Mounce, 4th Edition</em></p>
<div class="instructions">
  Parse the underlined imperative (tense / voice / person / number / lexical form), note the aspect (ongoing or simple), and translate.
</div>
<div class="controls">
  <button class="btn-ctrl" onclick="showAll()">Show All Answers</button>
  <button class="btn-ctrl" onclick="hideAll()">Hide All Answers</button>
  <button class="btn-ctrl" onclick="clearAll()">Clear All Inputs</button>
</div>

<h2>Part A — Present Active Imperative (1–5)</h2>
<table>
<thead><tr><th>#</th><th>Greek Text</th><th>Tense</th><th>Voice</th><th>Person</th><th>Num</th><th>Lexical</th><th>Aspect</th><th>Translation</th><th></th></tr></thead>
<tbody>
<tr class="question-row" data-id="1"><td><b>1</b></td><td class="greek"><u>ἀγαπᾶτε</u> τοὺς ἐχθροὺς ὑμῶν.</td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><button class="btn-reveal" onclick="toggleAnswer(1)">▶ Answer</button></td></tr>
<tr class="answer-row" id="ans-1"><td></td><td colspan="8">Pres · Act · 2nd · Pl · ἀγαπάω · Ongoing · "Love your enemies." (Matt 5:44)</td><td></td></tr>

<tr class="question-row" data-id="2"><td><b>2</b></td><td class="greek"><u>μετανοεῖτε</u> καὶ πιστεύετε ἐν τῷ εὐαγγελίῳ.</td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><button class="btn-reveal" onclick="toggleAnswer(2)">▶ Answer</button></td></tr>
<tr class="answer-row" id="ans-2"><td></td><td colspan="8">Pres · Act · 2nd · Pl · μετανοέω · Ongoing · "Repent and believe in the gospel." (Mark 1:15)</td><td></td></tr>

<tr class="question-row" data-id="3"><td><b>3</b></td><td class="greek"><u>χαίρετε</u> ἐν κυρίῳ πάντοτε.</td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><button class="btn-reveal" onclick="toggleAnswer(3)">▶ Answer</button></td></tr>
<tr class="answer-row" id="ans-3"><td></td><td colspan="8">Pres · Act · 2nd · Pl · χαίρω · Ongoing · "Rejoice in the Lord always." (Phil 4:4)</td><td></td></tr>

<tr class="question-row" data-id="4"><td><b>4</b></td><td class="greek"><u>πρόσεχε</u> δὲ σεαυτῷ καὶ τῇ διδασκαλίᾳ.</td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><button class="btn-reveal" onclick="toggleAnswer(4)">▶ Answer</button></td></tr>
<tr class="answer-row" id="ans-4"><td></td><td colspan="8">Pres · Act · 2nd · Sg · προσέχω · Ongoing · "Pay attention to yourself and to the teaching." (1 Tim 4:16)</td><td></td></tr>

<tr class="question-row" data-id="5"><td><b>5</b></td><td class="greek"><u>αἴρετε</u> τὸν ζυγόν μου ἐφ᾽ ὑμᾶς.</td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><button class="btn-reveal" onclick="toggleAnswer(5)">▶ Answer</button></td></tr>
<tr class="answer-row" id="ans-5"><td></td><td colspan="8">Pres · Act · 2nd · Pl · αἴρω · Ongoing · "Take my yoke upon you." (Matt 11:29)</td><td></td></tr>
</tbody>
</table>

<h2>Part B — Present Middle/Passive Imperative (6–8)</h2>
<table>
<thead><tr><th>#</th><th>Greek Text</th><th>Tense</th><th>Voice</th><th>Person</th><th>Num</th><th>Lexical</th><th>Aspect</th><th>Translation</th><th></th></tr></thead>
<tbody>
<tr class="question-row" data-id="6"><td><b>6</b></td><td class="greek">μὴ <u>κλαίου</u>· ἰδοὺ ἐνίκησεν ὁ λέων.</td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><button class="btn-reveal" onclick="toggleAnswer(6)">▶ Answer</button></td></tr>
<tr class="answer-row" id="ans-6"><td></td><td colspan="8">Pres · Mid · 2nd · Sg · κλαίω · Stop (ongoing prohib.) · "Stop weeping! Behold, the Lion has conquered." (Rev 5:5)</td><td></td></tr>

<tr class="question-row" data-id="7"><td><b>7</b></td><td class="greek"><u>προσεύχεσθε</u> ἀδιαλείπτως.</td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><button class="btn-reveal" onclick="toggleAnswer(7)">▶ Answer</button></td></tr>
<tr class="answer-row" id="ans-7"><td></td><td colspan="8">Pres · Mid · 2nd · Pl · προσεύχομαι · Ongoing · "Pray without ceasing." (1 Thess 5:17)</td><td></td></tr>

<tr class="question-row" data-id="8"><td><b>8</b></td><td class="greek"><u>ἔρχου</u> καὶ ἴδε.</td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><button class="btn-reveal" onclick="toggleAnswer(8)">▶ Answer</button></td></tr>
<tr class="answer-row" id="ans-8"><td></td><td colspan="8">Pres · Mid · 2nd · Sg · ἔρχομαι · Ongoing · "Come and see." (John 1:46)</td><td></td></tr>
</tbody>
</table>

<h2>Part C — First Aorist Active Imperative (9–12)</h2>
<table>
<thead><tr><th>#</th><th>Greek Text</th><th>Tense</th><th>Voice</th><th>Person</th><th>Num</th><th>Lexical</th><th>Aspect</th><th>Translation</th><th></th></tr></thead>
<tbody>
<tr class="question-row" data-id="9"><td><b>9</b></td><td class="greek"><u>πορεύθητε</u> οὖν καὶ μαθητεύσατε πάντα τὰ ἔθνη.</td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><button class="btn-reveal" onclick="toggleAnswer(9)">▶ Answer</button></td></tr>
<tr class="answer-row" id="ans-9"><td></td><td colspan="8">Aor · Pass · 2nd · Pl · πορεύομαι · Simple · "Go therefore and make disciples of all nations." (Matt 28:19)</td><td></td></tr>

<tr class="question-row" data-id="10"><td><b>10</b></td><td class="greek"><u>μαθητεύσατε</u> πάντα τὰ ἔθνη.</td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><button class="btn-reveal" onclick="toggleAnswer(10)">▶ Answer</button></td></tr>
<tr class="answer-row" id="ans-10"><td></td><td colspan="8">Aor · Act · 2nd · Pl · μαθητεύω · Simple · "Make disciples of all nations." (Matt 28:19)</td><td></td></tr>

<tr class="question-row" data-id="11"><td><b>11</b></td><td class="greek"><u>ὑπόστρεψον</u> εἰς τὸν οἶκόν σου.</td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><button class="btn-reveal" onclick="toggleAnswer(11)">▶ Answer</button></td></tr>
<tr class="answer-row" id="ans-11"><td></td><td colspan="8">Aor · Act · 2nd · Sg · ὑποστρέφω · Simple · "Return to your house." (Luke 8:39)</td><td></td></tr>

<tr class="question-row" data-id="12"><td><b>12</b></td><td class="greek"><u>πίστευσον</u> ἐπὶ τὸν κύριον Ἰησοῦν.</td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><button class="btn-reveal" onclick="toggleAnswer(12)">▶ Answer</button></td></tr>
<tr class="answer-row" id="ans-12"><td></td><td colspan="8">Aor · Act · 2nd · Sg · πιστεύω · Simple · "Believe on the Lord Jesus." (Acts 16:31)</td><td></td></tr>
</tbody>
</table>

<h2>Part D — Second Aorist Active Imperative (13–15)</h2>
<table>
<thead><tr><th>#</th><th>Greek Text</th><th>Tense</th><th>Voice</th><th>Person</th><th>Num</th><th>Lexical</th><th>Aspect</th><th>Translation</th><th></th></tr></thead>
<tbody>
<tr class="question-row" data-id="13"><td><b>13</b></td><td class="greek"><u>ἐλθέ</u> καὶ ἴδε.</td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><button class="btn-reveal" onclick="toggleAnswer(13)">▶ Answer</button></td></tr>
<tr class="answer-row" id="ans-13"><td></td><td colspan="8">Aor · Act · 2nd · Sg · ἔρχομαι · Simple · "Come and see." (John 11:34)</td><td></td></tr>

<tr class="question-row" data-id="14"><td><b>14</b></td><td class="greek"><u>λάβε</u> τὸ παιδίον καὶ τὴν μητέρα αὐτοῦ.</td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><button class="btn-reveal" onclick="toggleAnswer(14)">▶ Answer</button></td></tr>
<tr class="answer-row" id="ans-14"><td></td><td colspan="8">Aor · Act · 2nd · Sg · λαμβάνω · Simple · "Take the child and his mother." (Matt 2:13)</td><td></td></tr>

<tr class="question-row" data-id="15"><td><b>15</b></td><td class="greek"><u>εἰπέ</u> μοι ἐν ποίᾳ ἐξουσίᾳ ταῦτα ποιεῖς.</td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><button class="btn-reveal" onclick="toggleAnswer(15)">▶ Answer</button></td></tr>
<tr class="answer-row" id="ans-15"><td></td><td colspan="8">Aor · Act · 2nd · Sg · λέγω · Simple · "Tell me by what authority you do these things." (Luke 20:2)</td><td></td></tr>
</tbody>
</table>

<h2>Part E — Aorist Passive and Third Person Imperatives (16–20)</h2>
<table>
<thead><tr><th>#</th><th>Greek Text</th><th>Tense</th><th>Voice</th><th>Person</th><th>Num</th><th>Lexical</th><th>Aspect</th><th>Translation</th><th></th></tr></thead>
<tbody>
<tr class="question-row" data-id="16"><td><b>16</b></td><td class="greek"><u>λύθητι</u> ἀπὸ τοῦ δεσμοῦ τούτου.</td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><button class="btn-reveal" onclick="toggleAnswer(16)">▶ Answer</button></td></tr>
<tr class="answer-row" id="ans-16"><td></td><td colspan="8">Aor · Pass · 2nd · Sg · λύω · Simple · "Be loosed from this bond."</td><td></td></tr>

<tr class="question-row" data-id="17"><td><b>17</b></td><td class="greek">μὴ <u>φοβήθητε</u> ἀπὸ τῶν ἀποκτενόντων τὸ σῶμα.</td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><button class="btn-reveal" onclick="toggleAnswer(17)">▶ Answer</button></td></tr>
<tr class="answer-row" id="ans-17"><td></td><td colspan="8">Aor · Pass · 2nd · Pl · φοβέομαι · Simple (prohib.) · "Do not fear those who kill the body." (Matt 10:28)</td><td></td></tr>

<tr class="question-row" data-id="18"><td><b>18</b></td><td class="greek">ὁ ἔχων ὦτα <u>ἀκουέτω</u>.</td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><button class="btn-reveal" onclick="toggleAnswer(18)">▶ Answer</button></td></tr>
<tr class="answer-row" id="ans-18"><td></td><td colspan="8">Pres · Act · 3rd · Sg · ἀκούω · Ongoing · "The one who has ears, let him hear." (Matt 13:9)</td><td></td></tr>

<tr class="question-row" data-id="19"><td><b>19</b></td><td class="greek"><u>ἔστω</u> δὲ ὑμῶν τὸ ναί, ναί.</td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><button class="btn-reveal" onclick="toggleAnswer(19)">▶ Answer</button></td></tr>
<tr class="answer-row" id="ans-19"><td></td><td colspan="8">Pres · Act · 3rd · Sg · εἰμί · Ongoing · "But let your yes be yes." (Matt 5:37)</td><td></td></tr>

<tr class="question-row" data-id="20"><td><b>20</b></td><td class="greek"><u>ἴσθι</u> ἐνδυναμούμενος ἐν τῇ χάριτι.</td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><button class="btn-reveal" onclick="toggleAnswer(20)">▶ Answer</button></td></tr>
<tr class="answer-row" id="ans-20"><td></td><td colspan="8">Pres · Act · 2nd · Sg · εἰμί · Ongoing · "Be strengthened in grace." (2 Tim 2:1)</td><td></td></tr>
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

