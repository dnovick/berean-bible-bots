# Mi Verbs Parsing

*Chapter 36 — ἵστημι, τίθημι, δείκνυμι and Odds 'n Ends*

[Full screen](ch36-mi-verbs-parsing.html){.md-button}  [Markdown](ch36-mi-verbs-parsing.md){.md-button}  [Print (PDF)](ch36-mi-verbs-parsing.pdf){.md-button}

<style>

  body { font-family: Georgia, serif;    color: #222; }
  h1 { font-size: 1.4em; border-bottom: 2px solid #333; padding-bottom: .3em; }
  h2 { font-size: 1.1em; margin-top: 1.8em; border-bottom: 1px solid #aaa; }
  .subtitle { color: #555; font-style: italic; }
  .instructions { background: #f9f9f0; border-left: 3px solid #c8a000; padding: .7em 1em; margin: 1em 0 1.5em; font-size: .93em; }
  table { border-collapse: collapse; width: 100%; margin-bottom: 1em; font-size: .88em; }
  th { background: #263238; color: #fff; padding: .4em .5em; text-align: left; }
  td { padding: .38em .5em; vertical-align: top; border-bottom: 1px solid #ddd; }
  tr:nth-child(even) td { background: #eceff1; }
  .greek { font-size: 1.08em; font-weight: bold; }
  .parse-field { width: 93%; border: none; border-bottom: 1px solid #888; background: transparent; font-family: inherit; font-size: .87em; padding: 2px 0; }
  .parse-field:focus { outline: none; border-bottom: 2px solid #263238; }
  .answer-row { display: none; background: #cfd8dc !important; }
  .answer-row td { color: #1c313a; font-style: italic; font-size: .87em; }
  .btn-reveal { background: #263238; color: #fff; border: none; border-radius: 3px; padding: .22em .6em; cursor: pointer; font-size: .82em; }
  .btn-reveal:hover { background: #1c313a; }
  .controls { margin: 1em 0 1.5em; display: flex; gap: .7em; flex-wrap: wrap; }
  .btn-ctrl { background: #555; color: #fff; border: none; border-radius: 4px; padding: .4em 1em; cursor: pointer; font-size: .9em; }
  .btn-ctrl:hover { background: #333; }
  @media print { .btn-reveal, .controls { display: none !important; } .answer-row { display: none !important; } .parse-field { border-bottom: 1px solid #999; } }

</style>

<h1>BBG Chapter 36 — μι-Verbs Parsing</h1>
<p class="subtitle"><em>Basics of Biblical Greek Grammar, Mounce, 4th Edition</em></p>
<div class="instructions">
  Parse the underlined form (tense / voice / person / number / mood / lexical form). For ἵστημι, note transitive or intransitive. Translate the sentence.
</div>
<div class="controls">
  <button class="btn-ctrl" onclick="showAll()">Show All Answers</button>
  <button class="btn-ctrl" onclick="hideAll()">Hide All Answers</button>
  <button class="btn-ctrl" onclick="clearAll()">Clear All Inputs</button>
</div>

<h2>Part A — ἵστημι (1–6)</h2>
<table>
<thead><tr><th>#</th><th>Greek Text</th><th>Tense</th><th>Voice</th><th>Person</th><th>Num</th><th>Lexical</th><th>Trans/Intrans</th><th>Translation</th><th></th></tr></thead>
<tbody>
<tr class="question-row" data-id="1"><td><b>1</b></td><td class="greek"><u>ἔστησεν</u> αὐτὸ ἐν μέσῳ αὐτῶν.</td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><button class="btn-reveal" onclick="toggleAnswer(1)">▶ Answer</button></td></tr>
<tr class="answer-row" id="ans-1"><td></td><td colspan="8">Aor (1st) · Act · 3rd · Sg · ἵστημι · Transitive · "He set it in their midst." (Matt 18:2)</td><td></td></tr>

<tr class="question-row" data-id="2"><td><b>2</b></td><td class="greek"><u>ἔστη</u> Ἰησοῦς εἰς τὸ μέσον καὶ λέγει αὐτοῖς· εἰρήνη ὑμῖν.</td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><button class="btn-reveal" onclick="toggleAnswer(2)">▶ Answer</button></td></tr>
<tr class="answer-row" id="ans-2"><td></td><td colspan="8">Aor (2nd) · Act · 3rd · Sg · ἵστημι · Intransitive · "Jesus stood in their midst and says: Peace to you." (John 20:19)</td><td></td></tr>

<tr class="question-row" data-id="3"><td><b>3</b></td><td class="greek"><u>ἕστηκεν</u> ἐν τῷ ἁγίῳ τόπῳ τὸ βδέλυγμα τῆς ἐρημώσεως.</td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><button class="btn-reveal" onclick="toggleAnswer(3)">▶ Answer</button></td></tr>
<tr class="answer-row" id="ans-3"><td></td><td colspan="8">Perf · Act · 3rd · Sg · ἵστημι · Intransitive (= is standing) · "The abomination of desolation is standing in the holy place." (Matt 24:15)</td><td></td></tr>

<tr class="question-row" data-id="4"><td><b>4</b></td><td class="greek"><u>ἵστησιν</u> αὐτοὺς ὁ θεὸς ἐνώπιον τοῦ θρόνου αὐτοῦ.</td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><button class="btn-reveal" onclick="toggleAnswer(4)">▶ Answer</button></td></tr>
<tr class="answer-row" id="ans-4"><td></td><td colspan="8">Pres · Act · 3rd · Sg · ἵστημι · Transitive · "God sets them before his throne."</td><td></td></tr>

<tr class="question-row" data-id="5"><td><b>5</b></td><td class="greek"><u>στῆθι</u> καὶ μὴ κινήσῃς.</td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><button class="btn-reveal" onclick="toggleAnswer(5)">▶ Answer</button></td></tr>
<tr class="answer-row" id="ans-5"><td></td><td colspan="8">Aor (2nd) · Act · 2nd · Sg · Imper · ἵστημι · Intransitive · "Stand still and do not move."</td><td></td></tr>

<tr class="question-row" data-id="6"><td><b>6</b></td><td class="greek">τί <u>ἑστήκατε</u> βλέποντες εἰς τὸν οὐρανόν;</td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><button class="btn-reveal" onclick="toggleAnswer(6)">▶ Answer</button></td></tr>
<tr class="answer-row" id="ans-6"><td></td><td colspan="8">Perf · Act · 2nd · Pl · Ind · ἵστημι · Intransitive (= are standing) · "Why are you standing looking into heaven?" (Acts 1:11)</td><td></td></tr>
</tbody>
</table>

<h2>Part B — τίθημι (7–10)</h2>
<table>
<thead><tr><th>#</th><th>Greek Text</th><th>Tense</th><th>Voice</th><th>Person</th><th>Num</th><th>Lexical</th><th>Translation</th><th></th></tr></thead>
<tbody>
<tr class="question-row" data-id="7"><td><b>7</b></td><td class="greek"><u>τίθησιν</u> αὐτὴν ἐπὶ τὴν λυχνίαν.</td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><button class="btn-reveal" onclick="toggleAnswer(7)">▶ Answer</button></td></tr>
<tr class="answer-row" id="ans-7"><td></td><td colspan="7">Pres · Act · 3rd · Sg · τίθημι · "He puts it on the lampstand." (Matt 5:15)</td><td></td></tr>

<tr class="question-row" data-id="8"><td><b>8</b></td><td class="greek">ψυχήν μου <u>τίθημι</u> ὑπὲρ τῶν προβάτων.</td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><button class="btn-reveal" onclick="toggleAnswer(8)">▶ Answer</button></td></tr>
<tr class="answer-row" id="ans-8"><td></td><td colspan="7">Pres · Act · 1st · Sg · τίθημι · "I lay down my life for the sheep." (John 10:15)</td><td></td></tr>

<tr class="question-row" data-id="9"><td><b>9</b></td><td class="greek">ὅπου <u>ἔθηκαν</u> αὐτόν.</td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><button class="btn-reveal" onclick="toggleAnswer(9)">▶ Answer</button></td></tr>
<tr class="answer-row" id="ans-9"><td></td><td colspan="7">Aor · Act · 3rd · Pl · τίθημι · "Where they had placed him." (John 20:2)</td><td></td></tr>

<tr class="question-row" data-id="10"><td><b>10</b></td><td class="greek"><u>θὲς</u> τὴν χεῖρά σου ἐπὶ αὐτήν.</td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><button class="btn-reveal" onclick="toggleAnswer(10)">▶ Answer</button></td></tr>
<tr class="answer-row" id="ans-10"><td></td><td colspan="7">Aor · Act · 2nd · Sg · Imper · τίθημι · "Put your hand on her." (Mark 5:23)</td><td></td></tr>
</tbody>
</table>

<h2>Part C — δείκνυμι (11–13)</h2>
<table>
<thead><tr><th>#</th><th>Greek Text</th><th>Tense</th><th>Voice</th><th>Person</th><th>Num</th><th>Lexical</th><th>Translation</th><th></th></tr></thead>
<tbody>
<tr class="question-row" data-id="11"><td><b>11</b></td><td class="greek"><u>δεῖξόν</u> μοι τὴν πίστιν σου χωρὶς τῶν ἔργων.</td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><button class="btn-reveal" onclick="toggleAnswer(11)">▶ Answer</button></td></tr>
<tr class="answer-row" id="ans-11"><td></td><td colspan="7">Aor · Act · 2nd · Sg · Imper · δείκνυμι · "Show me your faith apart from your works." (Jas 2:18)</td><td></td></tr>

<tr class="question-row" data-id="12"><td><b>12</b></td><td class="greek">ταῦτα πάντα σοι <u>δείξω</u>.</td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><button class="btn-reveal" onclick="toggleAnswer(12)">▶ Answer</button></td></tr>
<tr class="answer-row" id="ans-12"><td></td><td colspan="7">Fut · Act · 1st · Sg · Ind · δείκνυμι · "All these things I will show you." (Matt 4:9)</td><td></td></tr>

<tr class="question-row" data-id="13"><td><b>13</b></td><td class="greek"><u>δεικνύουσιν</u> αὐτῷ τὸ νόμισμα τοῦ κήνσου.</td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><button class="btn-reveal" onclick="toggleAnswer(13)">▶ Answer</button></td></tr>
<tr class="answer-row" id="ans-13"><td></td><td colspan="7">Pres · Act · 3rd · Pl · Ind · δείκνυμι · "They showed him the coin of the poll tax." (Matt 22:19)</td><td></td></tr>
</tbody>
</table>

<h2>Part D — ἀφίημι (14–16)</h2>
<table>
<thead><tr><th>#</th><th>Greek Text</th><th>Tense</th><th>Voice</th><th>Person</th><th>Num</th><th>Lexical</th><th>Translation</th><th></th></tr></thead>
<tbody>
<tr class="question-row" data-id="14"><td><b>14</b></td><td class="greek"><u>ἀφίεμεν</u> τοῖς ὀφειλέταις ἡμῶν.</td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><button class="btn-reveal" onclick="toggleAnswer(14)">▶ Answer</button></td></tr>
<tr class="answer-row" id="ans-14"><td></td><td colspan="7">Pres · Act · 1st · Pl · Ind · ἀφίημι · "We forgive our debtors." (Matt 6:12)</td><td></td></tr>

<tr class="question-row" data-id="15"><td><b>15</b></td><td class="greek">τίς δύναται <u>ἀφιέναι</u> ἁμαρτίας εἰ μὴ εἷς ὁ θεός;</td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><button class="btn-reveal" onclick="toggleAnswer(15)">▶ Answer</button></td></tr>
<tr class="answer-row" id="ans-15"><td></td><td colspan="7">Pres · Act · — · — · Inf · ἀφίημι · "Who is able to forgive sins except God alone?" (Mark 2:7)</td><td></td></tr>

<tr class="question-row" data-id="16"><td><b>16</b></td><td class="greek"><u>ἄφες</u> ἡμῖν τὰ ὀφειλήματα ἡμῶν.</td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><button class="btn-reveal" onclick="toggleAnswer(16)">▶ Answer</button></td></tr>
<tr class="answer-row" id="ans-16"><td></td><td colspan="7">Aor · Act · 2nd · Sg · Imper · ἀφίημι · "Forgive us our debts." (Matt 6:12)</td><td></td></tr>
</tbody>
</table>

<h2>Part E — ἀπόλλυμι and οἶδα (17–20)</h2>
<table>
<thead><tr><th>#</th><th>Greek Text</th><th>Tense</th><th>Voice</th><th>Person</th><th>Num</th><th>Lexical</th><th>Translation</th><th></th></tr></thead>
<tbody>
<tr class="question-row" data-id="17"><td><b>17</b></td><td class="greek"><u>ἀπολλύμεθα</u>· οὐ μέλει σοι ὅτι ἀπολλύμεθα;</td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><button class="btn-reveal" onclick="toggleAnswer(17)">▶ Answer</button></td></tr>
<tr class="answer-row" id="ans-17"><td></td><td colspan="7">Pres · Mid · 1st · Pl · Ind · ἀπόλλυμι · "We are perishing! Do you not care that we are perishing?" (Mark 4:38)</td><td></td></tr>

<tr class="question-row" data-id="18"><td><b>18</b></td><td class="greek">τὸ <u>ἀπολωλός</u> ζητῆσαι.</td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><input class="parse-field" placeholder="Perf. Act. Ptc."></td><td><input class="parse-field"></td>
  <td><button class="btn-reveal" onclick="toggleAnswer(18)">▶ Answer</button></td></tr>
<tr class="answer-row" id="ans-18"><td></td><td colspan="7">Perf · Act · Acc/Nom · Sg (Neut) · Ptc (substantival) · ἀπόλλυμι · "To seek the lost [= the thing that has perished]." (Luke 19:10)</td><td></td></tr>

<tr class="question-row" data-id="19"><td><b>19</b></td><td class="greek"><u>οἶδα</u> ὅτι Μεσσίας ἔρχεται.</td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><button class="btn-reveal" onclick="toggleAnswer(19)">▶ Answer</button></td></tr>
<tr class="answer-row" id="ans-19"><td></td><td colspan="7">Perf (pres. meaning) · Act · 1st · Sg · Ind · οἶδα · "I know that the Messiah is coming." (John 4:25)</td><td></td></tr>

<tr class="question-row" data-id="20"><td><b>20</b></td><td class="greek"><u>οἴδαμεν</u> ὅτι ὁ υἱὸς τοῦ θεοῦ ἥκει.</td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><input class="parse-field"></td><td><input class="parse-field"></td><td><input class="parse-field"></td>
  <td><button class="btn-reveal" onclick="toggleAnswer(20)">▶ Answer</button></td></tr>
<tr class="answer-row" id="ans-20"><td></td><td colspan="7">Perf (pres. meaning) · Act · 1st · Pl · Ind · οἶδα · "We know that the Son of God has come." (1 John 5:20)</td><td></td></tr>
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

