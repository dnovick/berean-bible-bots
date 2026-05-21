# Perfect Parsing

*Chapter 25 — Perfect Indicative*

[Full screen](ch25-perfect-parsing.html){.md-button}  [Markdown](ch25-perfect-parsing.md){.md-button}  [Print (PDF)](ch25-perfect-parsing.pdf){.md-button}

<style>

  body { font-family: Georgia, serif;    color: #222; }
  h1 { font-size: 1.4em; }
  p.subtitle { color: #555; font-style: italic; }
  .note { background: #fff3cd; border-left: 4px solid #ffc107; padding: 0.5em 0.8em; margin: 0.8em 0; font-size: 0.9em; }
  .tip { background: #e8f4f8; border-left: 4px solid #3a5a8a; padding: 0.5em 0.8em; margin: 0.8em 0; font-size: 0.9em; }
  .controls { margin: 1em 0; display: flex; gap: 0.6em; flex-wrap: wrap; }
  .controls button { padding: 0.4em 1em; font-size: 0.9em; cursor: pointer; border: 1px solid #888; border-radius: 4px; background: #f5f5f5; }
  .controls button:hover { background: #e0e0e0; }
  table { border-collapse: collapse; width: 100%; font-size: 0.85em; }
  th { background: #3a5a8a; color: #fff; padding: 0.5em 0.4em; text-align: left; }
  td { border: 1px solid #ccc; padding: 0.3em 0.35em; vertical-align: middle; }
  tr:nth-child(even) td { background: #f8f8f8; }
  .greek { font-size: 1.1em; font-weight: bold; }
  input.parse-field {
    width: 100%;
    min-width: 60px;
    border: none;
    border-bottom: 1px solid #999;
    background: transparent;
    font-size: 0.85em;
    padding: 1px 2px;
    box-sizing: border-box;
  }
  input.parse-field:focus { outline: none; border-bottom-color: #3a5a8a; }
  .btn-answer { padding: 0.2em 0.5em; font-size: 0.78em; cursor: pointer; border: 1px solid #aaa; border-radius: 3px; background: #fff; white-space: nowrap; }
  .btn-answer:hover { background: #f0f0f0; }
  tr.answer-row td { background: #d4edda !important; font-size: 0.83em; color: #155724; }
  tr.answer-row { display: none; }
  tr.answer-row.visible { display: table-row; }
  tr.distractor td { background: #fff8e1 !important; }
  tr.theological td { background: #e8f0ff !important; }
  .num-col { width: 2.2em; text-align: center; }
  .form-col { width: 9em; }
  @media print {
    .controls, .btn-answer { display: none !important; }
    input.parse-field { border-bottom: 1px solid #555; background: transparent; }
    tr.answer-row { display: none !important; }
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

<h1>Ch25 — Perfect Indicative Parsing Drill</h1>
<p class="subtitle">BBG Chapter 25 · Mounce 4th Edition — Parse each form: Tense · Voice · Mood · Person · Number · Reduplication Type · Lexical Form · Translation</p>
<div class="tip">&#128218; <strong>Aspect reminder:</strong> Translate perfect forms with "have ___-ed" to capture the past event + present ongoing result.</div>
<div class="note">&#9888; Items 19 and 20 are <strong>aorist distractors</strong> — distinguish them from perfect forms by checking for reduplication vs. simple ε- augment.</div>

<div class="controls">
  <button onclick="showAll()">Show All Answers</button>
  <button onclick="hideAll()">Hide All Answers</button>
  <button onclick="clearAll()">Clear All Inputs</button>
</div>

<table>
<thead>
  <tr>
    <th class="num-col">#</th>
    <th class="form-col">Form</th>
    <th>Tense</th>
    <th>Voice</th>
    <th>Mood</th>
    <th>Person</th>
    <th>Number</th>
    <th>Reduplication</th>
    <th>Lexical Form</th>
    <th>Translation</th>
    <th></th>
  </tr>
</thead>
<tbody id="drillBody">
</tbody>
</table>

<script>
const items = [
  { num:1,  form:"λέλυκα",      tense:"Perfect",       voice:"Active",        mood:"Indicative", person:"1st", number:"Singular", reduplic:"λ+ε (consonant)",      lexical:"λύω",       trans:"I have loosed",                         distractor:false, theol:false },
  { num:2,  form:"λέλυκας",     tense:"Perfect",       voice:"Active",        mood:"Indicative", person:"2nd", number:"Singular", reduplic:"λ+ε (consonant)",      lexical:"λύω",       trans:"You have loosed",                       distractor:false, theol:false },
  { num:3,  form:"λέλυκεν",     tense:"Perfect",       voice:"Active",        mood:"Indicative", person:"3rd", number:"Singular", reduplic:"λ+ε (consonant)",      lexical:"λύω",       trans:"He/she has loosed",                     distractor:false, theol:false },
  { num:4,  form:"λελύκαμεν",   tense:"Perfect",       voice:"Active",        mood:"Indicative", person:"1st", number:"Plural",   reduplic:"λ+ε (consonant)",      lexical:"λύω",       trans:"We have loosed",                        distractor:false, theol:false },
  { num:5,  form:"λελύκατε",    tense:"Perfect",       voice:"Active",        mood:"Indicative", person:"2nd", number:"Plural",   reduplic:"λ+ε (consonant)",      lexical:"λύω",       trans:"You (pl) have loosed",                  distractor:false, theol:false },
  { num:6,  form:"λελύκασιν",   tense:"Perfect",       voice:"Active",        mood:"Indicative", person:"3rd", number:"Plural",   reduplic:"λ+ε (consonant)",      lexical:"λύω",       trans:"They have loosed",                      distractor:false, theol:false },
  { num:7,  form:"πεπίστευκα",  tense:"Perfect",       voice:"Active",        mood:"Indicative", person:"1st", number:"Singular", reduplic:"π+ε (consonant)",      lexical:"πιστεύω",   trans:"I have believed (remain in faith)",     distractor:false, theol:false },
  { num:8,  form:"πεποίηκεν",   tense:"Perfect",       voice:"Active",        mood:"Indicative", person:"3rd", number:"Singular", reduplic:"π+ε (consonant)",      lexical:"ποιέω",     trans:"He/she has done/made",                  distractor:false, theol:false },
  { num:9,  form:"ἀκήκοεν",     tense:"Perfect",       voice:"Active",        mood:"Indicative", person:"3rd", number:"Singular", reduplic:"ἀκ+η (vowel cluster)", lexical:"ἀκούω",     trans:"He/she has heard",                      distractor:false, theol:false },
  { num:10, form:"γέγραφεν",    tense:"Perfect",       voice:"Active",        mood:"Indicative", person:"3rd", number:"Singular", reduplic:"γ+ε; no κ (2nd perf.)",lexical:"γράφω",     trans:"He/she has written",                    distractor:false, theol:false },
  { num:11, form:"γέγονεν",     tense:"Perfect",       voice:"Active",        mood:"Indicative", person:"3rd", number:"Singular", reduplic:"γ+ε; no κ (2nd perf.)",lexical:"γίνομαι",   trans:"It has become / it has happened",       distractor:false, theol:false },
  { num:12, form:"ἐγήγερται",   tense:"Perfect",       voice:"Middle/Passive",mood:"Indicative", person:"3rd", number:"Singular", reduplic:"ε+γ (cluster)",        lexical:"ἐγείρω",    trans:"He/she has been raised",                distractor:false, theol:false },
  { num:13, form:"γέγραπται",   tense:"Perfect",       voice:"Middle/Passive",mood:"Indicative", person:"3rd", number:"Singular", reduplic:"γ+ε (consonant)",      lexical:"γράφω",     trans:"It has been written / it stands written",distractor:false, theol:true  },
  { num:14, form:"τετέλεσται",  tense:"Perfect",       voice:"Middle/Passive",mood:"Indicative", person:"3rd", number:"Singular", reduplic:"τ+ε (consonant)",      lexical:"τελέω",     trans:"It has been completed / It is finished",distractor:false, theol:true  },
  { num:15, form:"λέλυμαι",     tense:"Perfect",       voice:"Middle/Passive",mood:"Indicative", person:"1st", number:"Singular", reduplic:"λ+ε (consonant)",      lexical:"λύω",       trans:"I have been loosed / I stand loosed",   distractor:false, theol:false },
  { num:16, form:"λέλυται",     tense:"Perfect",       voice:"Middle/Passive",mood:"Indicative", person:"3rd", number:"Singular", reduplic:"λ+ε (consonant)",      lexical:"λύω",       trans:"He/she has been loosed",                distractor:false, theol:false },
  { num:17, form:"λελύμεθα",    tense:"Perfect",       voice:"Middle/Passive",mood:"Indicative", person:"1st", number:"Plural",   reduplic:"λ+ε (consonant)",      lexical:"λύω",       trans:"We have been loosed",                   distractor:false, theol:false },
  { num:18, form:"λέλυνται",    tense:"Perfect",       voice:"Middle/Passive",mood:"Indicative", person:"3rd", number:"Plural",   reduplic:"λ+ε (consonant)",      lexical:"λύω",       trans:"They have been loosed",                 distractor:false, theol:false },
  { num:19, form:"ἔλυσεν",      tense:"Aorist (1st)",  voice:"Active",        mood:"Indicative", person:"3rd", number:"Singular", reduplic:"ε- augment, NOT reduplicated", lexical:"λύω", trans:"He loosed (AORIST distractor)",         distractor:true,  theol:false },
  { num:20, form:"ἔγραψεν",     tense:"Aorist (1st)",  voice:"Active",        mood:"Indicative", person:"3rd", number:"Singular", reduplic:"ε- augment, NOT reduplicated", lexical:"γράφω",trans:"He wrote (AORIST distractor)",         distractor:true,  theol:false },
];

const fieldKeys = ["tense","voice","mood","person","number","reduplic","lexical","trans"];

function buildTable() {
  const tbody = document.getElementById("drillBody");
  items.forEach(item => {
    const inputRow = document.createElement("tr");
    inputRow.id = "row-" + item.num;
    if (item.distractor) inputRow.className = "distractor";
    else if (item.theol) inputRow.className = "theological";
    let cells = `<td class="num-col">${item.num}</td><td class="form-col greek">${item.form}</td>`;
    fieldKeys.forEach(f => {
      cells += `<td><input class="parse-field" type="text" aria-label="${f}"></td>`;
    });
    cells += `<td><button class="btn-answer" onclick="toggleAnswer(${item.num})">&#9658; Answer</button></td>`;
    inputRow.innerHTML = cells;
    tbody.appendChild(inputRow);

    const ansRow = document.createElement("tr");
    ansRow.id = "ans-" + item.num;
    ansRow.className = "answer-row";
    let ansCells = `<td class="num-col"></td><td class="form-col greek">${item.form}</td>`;
    ansCells += `<td>${item.tense}</td><td>${item.voice}</td><td>${item.mood}</td>`;
    ansCells += `<td>${item.person}</td><td>${item.number}</td>`;
    ansCells += `<td>${item.reduplic}</td><td>${item.lexical}</td><td>${item.trans}</td><td></td>`;
    ansRow.innerHTML = ansCells;
    tbody.appendChild(ansRow);
  });
}

function toggleAnswer(num) { document.getElementById("ans-" + num).classList.toggle("visible"); }
function showAll() { document.querySelectorAll(".answer-row").forEach(r => r.classList.add("visible")); }
function hideAll() { document.querySelectorAll(".answer-row").forEach(r => r.classList.remove("visible")); }
function clearAll() { document.querySelectorAll("input.parse-field").forEach(i => i.value = ""); }

buildTable();
</script>

