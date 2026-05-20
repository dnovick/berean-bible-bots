# Future Parsing

*Chapter 19 — Future Active and Middle Indicative*

[Full screen](ch19-future-parsing.html){.md-button}  [Markdown](ch19-future-parsing.md){.md-button}  [Print (PDF)](ch19-future-parsing.pdf){.md-button}

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
    min-width: 80px;
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
  .form-col { width: 8em; }
  @media print {
    .controls, .btn-answer { display: none !important; }
    input.parse-field { border-bottom: 1px solid #555; background: transparent; }
    tr.answer-row { display: none !important; }
  }

</style>

<h1>Ch19 — Future Active/Middle Parsing Drill</h1>
<p class="subtitle">BBG Chapter 19 · Mounce 4th Edition — Parse each form: Tense · Voice · Mood · Person · Number · Lexical Form · Translation</p>

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
  { num: 1,  form: "λύσω",       tense:"Future", voice:"Active",  mood:"Indicative", person:"1st", number:"Singular", lexical:"λύω",    trans:"I will loose" },
  { num: 2,  form: "λύσεις",     tense:"Future", voice:"Active",  mood:"Indicative", person:"2nd", number:"Singular", lexical:"λύω",    trans:"You will loose" },
  { num: 3,  form: "λύσει",      tense:"Future", voice:"Active",  mood:"Indicative", person:"3rd", number:"Singular", lexical:"λύω",    trans:"He/she/it will loose" },
  { num: 4,  form: "λύσομεν",    tense:"Future", voice:"Active",  mood:"Indicative", person:"1st", number:"Plural",   lexical:"λύω",    trans:"We will loose" },
  { num: 5,  form: "λύσετε",     tense:"Future", voice:"Active",  mood:"Indicative", person:"2nd", number:"Plural",   lexical:"λύω",    trans:"You (pl) will loose" },
  { num: 6,  form: "λύσουσιν",   tense:"Future", voice:"Active",  mood:"Indicative", person:"3rd", number:"Plural",   lexical:"λύω",    trans:"They will loose" },
  { num: 7,  form: "γράψω",      tense:"Future", voice:"Active",  mood:"Indicative", person:"1st", number:"Singular", lexical:"γράφω",  trans:"I will write" },
  { num: 8,  form: "ἄξει",       tense:"Future", voice:"Active",  mood:"Indicative", person:"3rd", number:"Singular", lexical:"ἄγω",    trans:"He/she/it will lead" },
  { num: 9,  form: "πείσομεν",   tense:"Future", voice:"Active",  mood:"Indicative", person:"1st", number:"Plural",   lexical:"πείθω",  trans:"We will persuade" },
  { num: 10, form: "βλέψετε",    tense:"Future", voice:"Active",  mood:"Indicative", person:"2nd", number:"Plural",   lexical:"βλέπω",  trans:"You (pl) will see" },
  { num: 11, form: "ἀγαπήσω",    tense:"Future", voice:"Active",  mood:"Indicative", person:"1st", number:"Singular", lexical:"ἀγαπάω", trans:"I will love" },
  { num: 12, form: "ποιήσει",    tense:"Future", voice:"Active",  mood:"Indicative", person:"3rd", number:"Singular", lexical:"ποιέω",  trans:"He/she/it will do/make" },
  { num: 13, form: "πληρώσομεν", tense:"Future", voice:"Active",  mood:"Indicative", person:"1st", number:"Plural",   lexical:"πληρόω", trans:"We will fill/fulfill" },
  { num: 14, form: "μενῶ",       tense:"Future", voice:"Active",  mood:"Indicative", person:"1st", number:"Singular", lexical:"μένω",   trans:"I will remain (liquid future)" },
  { num: 15, form: "μενεῖς",     tense:"Future", voice:"Active",  mood:"Indicative", person:"2nd", number:"Singular", lexical:"μένω",   trans:"You will remain (liquid future)" },
  { num: 16, form: "ἐγερεῖ",     tense:"Future", voice:"Active",  mood:"Indicative", person:"3rd", number:"Singular", lexical:"ἐγείρω", trans:"He/she/it will raise (liquid future)" },
  { num: 17, form: "λύσομαι",    tense:"Future", voice:"Middle",  mood:"Indicative", person:"1st", number:"Singular", lexical:"λύω",    trans:"I will loose (for myself)" },
  { num: 18, form: "λύσεται",    tense:"Future", voice:"Middle",  mood:"Indicative", person:"3rd", number:"Singular", lexical:"λύω",    trans:"He/she will loose (for himself/herself)" },
  { num: 19, form: "λύσονται",   tense:"Future", voice:"Middle",  mood:"Indicative", person:"3rd", number:"Plural",   lexical:"λύω",    trans:"They will loose (for themselves)" },
  { num: 20, form: "ὄψομαι",     tense:"Future", voice:"Middle",  mood:"Indicative", person:"1st", number:"Singular", lexical:"ὁράω",   trans:"I will see (deponent)" },
];

const fields = ["tense","voice","mood","person","number","lexical","trans"];

function buildTable() {
  const tbody = document.getElementById("drillBody");
  items.forEach(item => {
    const inputRow = document.createElement("tr");
    inputRow.id = "row-" + item.num;
    let cells = `<td class="num-col">${item.num}</td><td class="form-col greek">${item.form}</td>`;
    fields.forEach(f => {
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
    ansCells += `<td>${item.lexical}</td><td>${item.trans}</td><td></td>`;
    ansRow.innerHTML = ansCells;
    tbody.appendChild(ansRow);
  });
}

function toggleAnswer(num) {
  const row = document.getElementById("ans-" + num);
  row.classList.toggle("visible");
}
function showAll() {
  document.querySelectorAll(".answer-row").forEach(r => r.classList.add("visible"));
}
function hideAll() {
  document.querySelectorAll(".answer-row").forEach(r => r.classList.remove("visible"));
}
function clearAll() {
  document.querySelectorAll("input.parse-field").forEach(i => i.value = "");
}

buildTable();
</script>

