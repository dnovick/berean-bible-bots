# Nom Acc Parsing

*Chapter 6 — Nominative and Accusative; Article*

[Full screen](ch6-nom-acc-parsing.html){.md-button}  [Markdown](ch6-nom-acc-parsing.md){.md-button}  [Print (PDF)](ch6-nom-acc-parsing.pdf){.md-button}

<style>

body{font-family:Georgia,serif;color:#222}
h1{font-size:1.4em;border-bottom:2px solid #333;padding-bottom:.3em}
h2{font-size:1.15em;margin-top:2em;color:#444}
p.sub{font-style:italic;margin:.3em 0 .7em;font-size:.9em;color:#555}
table{border-collapse:collapse;width:100%;margin:.8em 0}
th{background:#1a4a7a;color:#fff;padding:.45em .6em;text-align:left;font-size:.85em}
td{padding:.35em .6em;border:1px solid #ccc;font-size:.9em;vertical-align:top}
tr:nth-child(even){background:#f7f7f7}
.greek{font-size:1.3em;font-weight:bold}
input.parse-field{width:90%;border:none;border-bottom:1px solid #999;background:transparent;font-size:.88em;font-family:inherit;padding:1px 2px}
input.parse-field:focus{outline:none;border-bottom:2px solid #1a4a7a}
.answer-row td{background:#e8f0fb;font-size:.85em}
.answer-row{display:none}
.toggle-btn{background:#1a4a7a;color:#fff;border:none;border-radius:3px;padding:2px 8px;cursor:pointer;font-size:.8em}
.toggle-btn:hover{background:#0e2f52}
.controls{margin:.8em 0 1.2em;display:flex;gap:.6em;flex-wrap:wrap}
.ctrl-btn{background:#555;color:#fff;border:none;border-radius:4px;padding:.4em .9em;cursor:pointer;font-size:.85em}
.ctrl-btn:hover{background:#333}
.note-box{background:#fff8dc;border-left:4px solid #c8a800;padding:.6em .9em;margin:.8em 0;font-size:.9em}
@media print{
  .controls,.toggle-btn{display:none}
  input.parse-field{border-bottom:1px solid #000;min-width:60px}
  .answer-row{display:none!important}
}

</style>

<div class="download-links" style="margin:1rem 0 .5rem;font-size:.85rem;">
  <strong>Also available:</strong>
  <a href="ch6-nom-acc-parsing.md" style="margin-left:.5rem;">&#128196; Markdown</a>
  <span style="margin:0 .3rem;color:#aaa;">|</span>
  <a href="ch6-nom-acc-parsing.pdf">&#128209; PDF</a>
</div>

<h1>Chapter 6 — Nominative and Accusative Parsing Drill</h1>
<p><em>For each form, give: (a) Case, (b) Number, (c) Gender, (d) Lexical form (nom. sg.), (e) Function (subject / direct object / predicate nominative / article). Click <strong>▶ Answer</strong> to reveal.</em></p>

<div class="controls">
  <button class="ctrl-btn" onclick="showAll()">Show All Answers</button>
  <button class="ctrl-btn" onclick="hideAll()">Hide All Answers</button>
  <button class="ctrl-btn" onclick="clearAll()">Clear All Inputs</button>
</div>

<div class="note-box"><strong>Key reminder — Neuter Rule:</strong> In neuter nouns, nominative = accusative = vocative (both singular and plural). Context must determine function. · <strong>Article nom. forms:</strong> ὁ, ἡ, οἱ, αἱ — these four do <em>not</em> begin with τ. All others do.</div>

<h2>Part A — Masculine Nouns and Article</h2>
<p class="sub">Parse each form and state its function in a sentence.</p>
<table>
<tr><th>#</th><th>Form</th><th>Case</th><th>Number</th><th>Gender</th><th>Lexical Form</th><th>Function</th><th></th></tr>

<tr><td>1</td><td class="greek">λόγος</td><td><input class="parse-field" id="1-cs"></td><td><input class="parse-field" id="1-nb"></td><td><input class="parse-field" id="1-gn"></td><td><input class="parse-field" id="1-lx"></td><td><input class="parse-field" id="1-fn"></td><td><button class="toggle-btn" onclick="tog('a1')">▶ Answer</button></td></tr>
<tr class="answer-row" id="a1"><td colspan="8">Nominative · Singular · Masculine · λόγος · Subject (or predicate nominative)</td></tr>

<tr><td>2</td><td class="greek">λόγον</td><td><input class="parse-field" id="2-cs"></td><td><input class="parse-field" id="2-nb"></td><td><input class="parse-field" id="2-gn"></td><td><input class="parse-field" id="2-lx"></td><td><input class="parse-field" id="2-fn"></td><td><button class="toggle-btn" onclick="tog('a2')">▶ Answer</button></td></tr>
<tr class="answer-row" id="a2"><td colspan="8">Accusative · Singular · Masculine · λόγος · Direct object</td></tr>

<tr><td>3</td><td class="greek">λόγοι</td><td><input class="parse-field" id="3-cs"></td><td><input class="parse-field" id="3-nb"></td><td><input class="parse-field" id="3-gn"></td><td><input class="parse-field" id="3-lx"></td><td><input class="parse-field" id="3-fn"></td><td><button class="toggle-btn" onclick="tog('a3')">▶ Answer</button></td></tr>
<tr class="answer-row" id="a3"><td colspan="8">Nominative · Plural · Masculine · λόγος · Subject</td></tr>

<tr><td>4</td><td class="greek">λόγους</td><td><input class="parse-field" id="4-cs"></td><td><input class="parse-field" id="4-nb"></td><td><input class="parse-field" id="4-gn"></td><td><input class="parse-field" id="4-lx"></td><td><input class="parse-field" id="4-fn"></td><td><button class="toggle-btn" onclick="tog('a4')">▶ Answer</button></td></tr>
<tr class="answer-row" id="a4"><td colspan="8">Accusative · Plural · Masculine · λόγος · Direct object</td></tr>

<tr><td>5</td><td class="greek">ὁ</td><td><input class="parse-field" id="5-cs"></td><td><input class="parse-field" id="5-nb"></td><td><input class="parse-field" id="5-gn"></td><td><input class="parse-field" id="5-lx"></td><td><input class="parse-field" id="5-fn"></td><td><button class="toggle-btn" onclick="tog('a5')">▶ Answer</button></td></tr>
<tr class="answer-row" id="a5"><td colspan="8">Nominative · Singular · Masculine · ὁ (definite article) · Article modifying a masculine singular nominative noun — e.g., ὁ λόγος</td></tr>

<tr><td>6</td><td class="greek">τόν</td><td><input class="parse-field" id="6-cs"></td><td><input class="parse-field" id="6-nb"></td><td><input class="parse-field" id="6-gn"></td><td><input class="parse-field" id="6-lx"></td><td><input class="parse-field" id="6-fn"></td><td><button class="toggle-btn" onclick="tog('a6')">▶ Answer</button></td></tr>
<tr class="answer-row" id="a6"><td colspan="8">Accusative · Singular · Masculine · ὁ (article) · Article modifying a masculine singular accusative noun — e.g., τὸν κόσμον</td></tr>

<tr><td>7</td><td class="greek">οἱ</td><td><input class="parse-field" id="7-cs"></td><td><input class="parse-field" id="7-nb"></td><td><input class="parse-field" id="7-gn"></td><td><input class="parse-field" id="7-lx"></td><td><input class="parse-field" id="7-fn"></td><td><button class="toggle-btn" onclick="tog('a7')">▶ Answer</button></td></tr>
<tr class="answer-row" id="a7"><td colspan="8">Nominative · Plural · Masculine · ὁ (article) · Article modifying masculine plural nominative noun — note: οἱ does NOT begin with τ</td></tr>

<tr><td>8</td><td class="greek">τούς</td><td><input class="parse-field" id="8-cs"></td><td><input class="parse-field" id="8-nb"></td><td><input class="parse-field" id="8-gn"></td><td><input class="parse-field" id="8-lx"></td><td><input class="parse-field" id="8-fn"></td><td><button class="toggle-btn" onclick="tog('a8')">▶ Answer</button></td></tr>
<tr class="answer-row" id="a8"><td colspan="8">Accusative · Plural · Masculine · ὁ (article) · Article modifying masculine plural accusative noun</td></tr>

<tr><td>9</td><td class="greek">κύριον</td><td><input class="parse-field" id="9-cs"></td><td><input class="parse-field" id="9-nb"></td><td><input class="parse-field" id="9-gn"></td><td><input class="parse-field" id="9-lx"></td><td><input class="parse-field" id="9-fn"></td><td><button class="toggle-btn" onclick="tog('a9')">▶ Answer</button></td></tr>
<tr class="answer-row" id="a9"><td colspan="8">Accusative · Singular · Masculine · κύριος · Direct object — "Lord" as receiver of action</td></tr>

<tr><td>10</td><td class="greek">κύριοι</td><td><input class="parse-field" id="10-cs"></td><td><input class="parse-field" id="10-nb"></td><td><input class="parse-field" id="10-gn"></td><td><input class="parse-field" id="10-lx"></td><td><input class="parse-field" id="10-fn"></td><td><button class="toggle-btn" onclick="tog('a10')">▶ Answer</button></td></tr>
<tr class="answer-row" id="a10"><td colspan="8">Nominative · Plural · Masculine · κύριος · Subject — "lords/masters" as doers of action</td></tr>
</table>

<h2>Part B — Neuter Nouns, Article, and Mixed</h2>
<p class="sub">Remember: neuter nominative = neuter accusative. Context decides function.</p>
<table>
<tr><th>#</th><th>Form</th><th>Case</th><th>Number</th><th>Gender</th><th>Lexical Form</th><th>Function / Notes</th><th></th></tr>

<tr><td>11</td><td class="greek">ἔργον</td><td><input class="parse-field" id="11-cs"></td><td><input class="parse-field" id="11-nb"></td><td><input class="parse-field" id="11-gn"></td><td><input class="parse-field" id="11-lx"></td><td><input class="parse-field" id="11-fn"></td><td><button class="toggle-btn" onclick="tog('a11')">▶ Answer</button></td></tr>
<tr class="answer-row" id="a11"><td colspan="8">Nom. or Acc. · Singular · Neuter · ἔργον · Subject or direct object — neuter sg. nom. and acc. are identical (-ον)</td></tr>

<tr><td>12</td><td class="greek">ἔργα</td><td><input class="parse-field" id="12-cs"></td><td><input class="parse-field" id="12-nb"></td><td><input class="parse-field" id="12-gn"></td><td><input class="parse-field" id="12-lx"></td><td><input class="parse-field" id="12-fn"></td><td><button class="toggle-btn" onclick="tog('a12')">▶ Answer</button></td></tr>
<tr class="answer-row" id="a12"><td colspan="8">Nom. or Acc. · Plural · Neuter · ἔργον · Subject or direct object — neuter pl. nom. and acc. are identical (-α)</td></tr>

<tr><td>13</td><td class="greek">τό</td><td><input class="parse-field" id="13-cs"></td><td><input class="parse-field" id="13-nb"></td><td><input class="parse-field" id="13-gn"></td><td><input class="parse-field" id="13-lx"></td><td><input class="parse-field" id="13-fn"></td><td><button class="toggle-btn" onclick="tog('a13')">▶ Answer</button></td></tr>
<tr class="answer-row" id="a13"><td colspan="8">Nom. or Acc. · Singular · Neuter · ὁ (article) · Article modifying neuter singular noun — nom. and acc. identical: τό</td></tr>

<tr><td>14</td><td class="greek">τά</td><td><input class="parse-field" id="14-cs"></td><td><input class="parse-field" id="14-nb"></td><td><input class="parse-field" id="14-gn"></td><td><input class="parse-field" id="14-lx"></td><td><input class="parse-field" id="14-fn"></td><td><button class="toggle-btn" onclick="tog('a14')">▶ Answer</button></td></tr>
<tr class="answer-row" id="a14"><td colspan="8">Nom. or Acc. · Plural · Neuter · ὁ (article) · Article modifying neuter plural noun — nom. and acc. identical: τά</td></tr>

<tr><td>15</td><td class="greek">εὐαγγέλιον</td><td><input class="parse-field" id="15-cs"></td><td><input class="parse-field" id="15-nb"></td><td><input class="parse-field" id="15-gn"></td><td><input class="parse-field" id="15-lx"></td><td><input class="parse-field" id="15-fn"></td><td><button class="toggle-btn" onclick="tog('a15')">▶ Answer</button></td></tr>
<tr class="answer-row" id="a15"><td colspan="8">Nom. or Acc. · Singular · Neuter · εὐαγγέλιον · Subject or direct object — "gospel" — 2nd declension neuter</td></tr>

<tr><td>16</td><td class="greek">εὐαγγέλια</td><td><input class="parse-field" id="16-cs"></td><td><input class="parse-field" id="16-nb"></td><td><input class="parse-field" id="16-gn"></td><td><input class="parse-field" id="16-lx"></td><td><input class="parse-field" id="16-fn"></td><td><button class="toggle-btn" onclick="tog('a16')">▶ Answer</button></td></tr>
<tr class="answer-row" id="a16"><td colspan="8">Nom. or Acc. · Plural · Neuter · εὐαγγέλιον · Subject or direct object — "gospels"</td></tr>

<tr><td>17</td><td class="greek">θεός</td><td><input class="parse-field" id="17-cs"></td><td><input class="parse-field" id="17-nb"></td><td><input class="parse-field" id="17-gn"></td><td><input class="parse-field" id="17-lx"></td><td><input class="parse-field" id="17-fn"></td><td><button class="toggle-btn" onclick="tog('a17')">▶ Answer</button></td></tr>
<tr class="answer-row" id="a17"><td colspan="8">Nominative · Singular · Masculine · θεός · Subject or predicate nominative — without article: qualitative or indefinite (context decides); John 1:1 uses anarthrous θεός as predicate nominative</td></tr>

<tr><td>18</td><td class="greek">θεόν</td><td><input class="parse-field" id="18-cs"></td><td><input class="parse-field" id="18-nb"></td><td><input class="parse-field" id="18-gn"></td><td><input class="parse-field" id="18-lx"></td><td><input class="parse-field" id="18-fn"></td><td><button class="toggle-btn" onclick="tog('a18')">▶ Answer</button></td></tr>
<tr class="answer-row" id="a18"><td colspan="8">Accusative · Singular · Masculine · θεός · Direct object — "God" receiving the action; e.g., ἀγαπῶμεν τὸν θεόν</td></tr>

<tr><td>19</td><td class="greek">κόσμοι</td><td><input class="parse-field" id="19-cs"></td><td><input class="parse-field" id="19-nb"></td><td><input class="parse-field" id="19-gn"></td><td><input class="parse-field" id="19-lx"></td><td><input class="parse-field" id="19-fn"></td><td><button class="toggle-btn" onclick="tog('a19')">▶ Answer</button></td></tr>
<tr class="answer-row" id="a19"><td colspan="8">Nominative · Plural · Masculine · κόσμος · Subject — rare in NT (κόσμος almost always singular), but grammatically valid</td></tr>

<tr><td>20</td><td class="greek">ἔργα</td><td><input class="parse-field" id="20-cs"></td><td><input class="parse-field" id="20-nb"></td><td><input class="parse-field" id="20-gn"></td><td><input class="parse-field" id="20-lx"></td><td><input class="parse-field" id="20-fn"></td><td><button class="toggle-btn" onclick="tog('a20')">▶ Answer</button></td></tr>
<tr class="answer-row" id="a20"><td colspan="8">Nom. or Acc. · Plural · Neuter · ἔργον · Subject or direct object — same form as #12; reinforces that neuter plural -α is ambiguous without context</td></tr>
</table>

<h2>Part C — Context Sentences</h2>
<p class="sub">Parse the bold form and translate the whole sentence.</p>
<table>
<tr><th>#</th><th>Sentence</th><th>Bold Form: Parse</th><th>Translation</th><th></th></tr>

<tr><td>C1</td><td>ὁ θεὸς ἀγαπᾷ <strong>τὸν κόσμον</strong></td><td><input class="parse-field" id="c1-parse" style="width:98%"></td><td><input class="parse-field" id="c1-trans" style="width:98%"></td><td><button class="toggle-btn" onclick="tog('ac1')">▶ Answer</button></td></tr>
<tr class="answer-row" id="ac1"><td colspan="5">τὸν κόσμον: Accusative singular masculine — article + noun, direct object of ἀγαπᾷ · Translation: "God loves the world" (cf. John 3:16)</td></tr>

<tr><td>C2</td><td>ὁ λόγος <strong>θεὸς</strong> ἦν</td><td><input class="parse-field" id="c2-parse" style="width:98%"></td><td><input class="parse-field" id="c2-trans" style="width:98%"></td><td><button class="toggle-btn" onclick="tog('ac2')">▶ Answer</button></td></tr>
<tr class="answer-row" id="ac2"><td colspan="5">θεός: Nominative singular masculine — predicate nominative; no article = qualitative ("what the Word is in nature/character") · Translation: "The Word was God" (John 1:1)</td></tr>

<tr><td>C3</td><td>βλέπω <strong>τὰ ἔργα</strong></td><td><input class="parse-field" id="c3-parse" style="width:98%"></td><td><input class="parse-field" id="c3-trans" style="width:98%"></td><td><button class="toggle-btn" onclick="tog('ac3')">▶ Answer</button></td></tr>
<tr class="answer-row" id="ac3"><td colspan="5">τὰ ἔργα: Accusative plural neuter — article + noun, direct object of βλέπω · Translation: "I see the works/deeds"</td></tr>
</table>

<script>
function tog(id){
  var r=document.getElementById(id);
  var b=r.previousElementSibling.querySelector('.toggle-btn');
  if(r.style.display==='table-row'){r.style.display='none';b.textContent='▶ Answer';}
  else{r.style.display='table-row';b.textContent='▼ Hide';}
}
function showAll(){document.querySelectorAll('.answer-row').forEach(function(r){r.style.display='table-row';});document.querySelectorAll('.toggle-btn').forEach(function(b){b.textContent='▼ Hide';});}
function hideAll(){document.querySelectorAll('.answer-row').forEach(function(r){r.style.display='none';});document.querySelectorAll('.toggle-btn').forEach(function(b){b.textContent='▶ Answer';});}
function clearAll(){document.querySelectorAll('input.parse-field').forEach(function(i){i.value='';});}
</script>

