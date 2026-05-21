# Stem Change Drill

*Chapter 20 — Verbal Roots (Patterns 2–4)*

[Full screen](ch20-stem-change-drill.html){.md-button}  [Markdown](ch20-stem-change-drill.md){.md-button}  [Print (PDF)](ch20-stem-change-drill.pdf){.md-button}

<style>

  body { font-family: Georgia, serif;    color: #222; }
  h1 { font-size: 1.4em; }
  p.subtitle { color: #555; font-style: italic; }
  .controls { margin: 1em 0; display: flex; gap: 0.6em; flex-wrap: wrap; }
  .controls button { padding: 0.4em 1em; font-size: 0.9em; cursor: pointer; border: 1px solid #888; border-radius: 4px; background: #f5f5f5; }
  .controls button:hover { background: #e0e0e0; }
  table { border-collapse: collapse; width: 100%; font-size: 0.88em; }
  th { background: #3a5a8a; color: #fff; padding: 0.5em 0.4em; text-align: left; }
  td { border: 1px solid #ccc; padding: 0.35em 0.4em; vertical-align: middle; }
  tr:nth-child(even) td { background: #f8f8f8; }
  .greek { font-size: 1.1em; font-weight: bold; }
  input.parse-field {
    width: 100%;
    min-width: 70px;
    border: none;
    border-bottom: 1px solid #999;
    background: transparent;
    font-size: 0.88em;
    padding: 1px 2px;
    box-sizing: border-box;
  }
  input.parse-field:focus { outline: none; border-bottom-color: #3a5a8a; }
  .btn-answer { padding: 0.2em 0.5em; font-size: 0.78em; cursor: pointer; border: 1px solid #aaa; border-radius: 3px; background: #fff; white-space: nowrap; }
  .btn-answer:hover { background: #f0f0f0; }
  tr.answer-row td { background: #d4edda !important; font-size: 0.85em; color: #155724; }
  tr.answer-row { display: none; }
  tr.answer-row.visible { display: table-row; }
  .num-col { width: 2.5em; text-align: center; }
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

<h1>Ch20 — Verbal Roots: Stem Change Drill</h1>
<p class="subtitle">BBG Chapter 20 · Mounce 4th Edition — Provide: Verbal Root · Pattern (2/3/4) · Subtype · Future Form</p>

<div class="controls">
  <button onclick="showAll()">Show All Answers</button>
  <button onclick="hideAll()">Hide All Answers</button>
  <button onclick="clearAll()">Clear All Inputs</button>
</div>

<table>
<thead>
  <tr>
    <th class="num-col">#</th>
    <th class="form-col">Present Form</th>
    <th>Verbal Root</th>
    <th>Pattern</th>
    <th>Subtype</th>
    <th>Future Form</th>
    <th></th>
  </tr>
</thead>
<tbody id="drillBody">
</tbody>
</table>

<script>
const items = [
  { num:1,  form:"γράφω",     root:"γραφ-",             pattern:"2", sub:"Labial stop (φ+σ→ψ)",          future:"γράψω" },
  { num:2,  form:"βλέπω",     root:"βλεπ-",             pattern:"2", sub:"Labial stop (π+σ→ψ)",          future:"βλέψω" },
  { num:3,  form:"πέμπω",     root:"πεμπ-",             pattern:"2", sub:"Labial stop (π+σ→ψ)",          future:"πέμψω" },
  { num:4,  form:"λείπω",     root:"λειπ-",             pattern:"2", sub:"Labial stop (π+σ→ψ); 2nd aor.",future:"λείψω" },
  { num:5,  form:"ἄγω",       root:"ἀγ-",               pattern:"2", sub:"Velar stop (γ+σ→ξ)",           future:"ἄξω" },
  { num:6,  form:"ἄρχω",      root:"ἀρχ-",              pattern:"2", sub:"Velar stop (χ+σ→ξ)",           future:"ἄρξω" },
  { num:7,  form:"διώκω",     root:"διωκ-",             pattern:"2", sub:"Velar stop (κ+σ→ξ)",           future:"διώξω" },
  { num:8,  form:"κηρύσσω",   root:"κηρυκ-",            pattern:"2", sub:"Velar stop (κ+σ→ξ)",           future:"κηρύξω" },
  { num:9,  form:"πείθω",     root:"πειθ-",             pattern:"2", sub:"Dental stop (θ+σ→σ)",          future:"πείσω" },
  { num:10, form:"σῴζω",      root:"σῳδ-",              pattern:"2", sub:"Dental stop (δ+σ→σ)",          future:"σώσω" },
  { num:11, form:"βαπτίζω",   root:"βαπτιδ-",           pattern:"2", sub:"Dental stop (δ+σ→σ)",          future:"βαπτίσω" },
  { num:12, form:"λαμβάνω",   root:"λαβ-",              pattern:"3", sub:"Nasal infix (αμβ in pres.)",   future:"λήμψομαι" },
  { num:13, form:"μανθάνω",   root:"μαθ-",              pattern:"3", sub:"Nasal infix (αν in pres.)",    future:"(no future; aor. ἔμαθον)" },
  { num:14, form:"ἁμαρτάνω",  root:"ἁμαρτ-",           pattern:"3", sub:"Nasal infix (αν in pres.)",    future:"ἁμαρτήσω" },
  { num:15, form:"τυγχάνω",   root:"τυχ-",              pattern:"3", sub:"Nasal infix (αν in pres.)",    future:"τεύξομαι" },
  { num:16, form:"λανθάνω",   root:"λαθ-",              pattern:"3", sub:"Nasal infix (αν in pres.)",    future:"λήσω" },
  { num:17, form:"ὁράω",      root:"ὁρ-/ὀπ-/ἰδ-",      pattern:"4", sub:"Suppletive",                   future:"ὄψομαι (deponent)" },
  { num:18, form:"ἔρχομαι",   root:"ἐρχ-/ἐλευθ-/ἐλθ-", pattern:"4", sub:"Suppletive",                   future:"ἐλεύσομαι (deponent)" },
  { num:19, form:"φέρω",      root:"φερ-/οἰ-/ἐνεγκ-",  pattern:"4", sub:"Suppletive",                   future:"οἴσω" },
  { num:20, form:"λέγω",      root:"λεγ-/ἐρ-/εἰπ-",    pattern:"4", sub:"Suppletive",                   future:"ἐρῶ (liquid future)" },
];

const fieldKeys = ["root","pattern","sub","future"];
const fieldLabels = ["Verbal Root","Pattern","Subtype","Future Form"];

function buildTable() {
  const tbody = document.getElementById("drillBody");
  items.forEach(item => {
    const inputRow = document.createElement("tr");
    inputRow.id = "row-" + item.num;
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
    ansCells += `<td>${item.root}</td><td>${item.pattern}</td><td>${item.sub}</td><td class="greek">${item.future}</td><td></td>`;
    ansRow.innerHTML = ansCells;
    tbody.appendChild(ansRow);
  });
}

function toggleAnswer(num) {
  document.getElementById("ans-" + num).classList.toggle("visible");
}
function showAll() { document.querySelectorAll(".answer-row").forEach(r => r.classList.add("visible")); }
function hideAll() { document.querySelectorAll(".answer-row").forEach(r => r.classList.remove("visible")); }
function clearAll() { document.querySelectorAll("input.parse-field").forEach(i => i.value = ""); }

buildTable();
</script>

