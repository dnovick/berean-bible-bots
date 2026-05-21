# Pronoun Drill

*Chapter 9 — Pronouns*

[Full screen](ch9-pronoun-drill.html){.md-button}  [Markdown](ch9-pronoun-drill.md){.md-button}  [Print (PDF)](ch9-pronoun-drill.pdf){.md-button}

<style>

  body { font-family: Arial, sans-serif;    }
  h1 { font-size: 1.3em; }
  p.instructions { background: #f5f5f5; border-left: 4px solid #888; padding: .6em 1em; }
  table { border-collapse: collapse;  margin-bottom: 1.5em; }
  th, td { border: 1px solid #ccc; padding: .35em .5em; text-align: left; vertical-align: top; }
  th { background: #e8e8e8; }
  td.aram { font-size: 1.4em; text-align: center; font-family: "SBL Hebrew", "Ezra SIL", serif; direction: rtl; min-width: 100px; }
  input.parse-field { width: 95%; border: none; border-bottom: 1px solid #999; font-size: .9em; }
  .answer-row td { background: #e6ffe6; font-size: .85em; }
  .answer-row { display: none; }
  .btn { padding: .25em .6em; margin: .2em; cursor: pointer; font-size: .85em; }
  .btn-ans { background: #e0e0e0; border: 1px solid #aaa; border-radius: 3px; }
  .global-btns { margin-bottom: 1em; }
  @media print {
    .btn, .global-btns { display: none; }
    input.parse-field { border-bottom: 1px solid #555; }
    .answer-row { display: none !important; }
  }

</style>

<h1>BBA Chapter 9 — Pronoun Drill</h1>
<p class="instructions"><strong>Instructions:</strong> For each form, identify the pronoun type (personal, demonstrative, interrogative, existential, indefinite, relative/compound), give the PGN where applicable, and give the English gloss or translation.</p>

<div class="global-btns">
  <button class="btn" onclick="showAll()">Show All Answers</button>
  <button class="btn" onclick="hideAll()">Hide All Answers</button>
  <button class="btn" onclick="clearAll()">Clear All Inputs</button>
</div>

<script>
// [num, form, type, pgn, gloss]
var rows = [
  [1,  "אֲנָה",        "personal",                       "1cs",   "I"],
  [2,  "דְּנָה",       "demonstrative (near)",           "ms",    "this"],
  [3,  "אִיתַי",       "existential",                    "—",     "there is / there are"],
  [4,  "מַן",          "interrogative",                  "—",     "who?"],
  [5,  "הוּא",         "personal",                       "3ms",   "he, it"],
  [6,  "כֹּל-אַרְעָא","indefinite (כֹּל)",              "—",     "all the earth / the whole earth"],
  [7,  "לֵית",         "existential (negative)",         "—",     "there is not / there are not"],
  [8,  "אִלֵּין",      "demonstrative (near)",           "pl.",   "these"],
  [9,  "מָה",          "interrogative",                  "—",     "what?"],
  [10, "הִמּוֹ",        "personal",                       "3mp",   "they"],
  [11, "דָּא",          "demonstrative (near)",           "fs",    "this"],
  [12, "אֲנַחְנָה",    "personal",                       "1cp",   "we"],
  [13, "הָדֵין",       "demonstrative (near/far)",       "ms",    "this / that"],
  [14, "מִנְדַּעַם",  "indefinite",                     "—",     "something, anything"],
  [15, "הִיא",         "personal",                       "3fs",   "she, it"],
  [16, "אַנְתְּ",      "personal",                       "2ms",   "you"],
  [17, "כִּדְנָה",     "demonstrative idiom",            "—",     "thus, in this way"],
  [18, "מַן דִּי",     "relative/interrogative compound","—",     "whoever, the one who"],
  [19, "אִיתַיְכוֹן", "existential + 2mp suffix",       "2mp",   "you are / there are you"],
  [20, "הָדָא",        "demonstrative (near/far)",       "fs",    "this / that"]
];

document.addEventListener("DOMContentLoaded", function() {
  var t = document.createElement("table"); document.body.appendChild(t);
  var thead = document.createElement("thead");
  var hr = document.createElement("tr");
  ["#","Form","Type","PGN","Gloss / Translation",""].forEach(function(h){
    var th = document.createElement("th"); th.textContent = h; hr.appendChild(th);
  });
  thead.appendChild(hr); t.appendChild(thead);

  var tbody = document.createElement("tbody");
  rows.forEach(function(row) {
    var num = row[0], form = row[1], type = row[2], pgn = row[3], gloss = row[4];

    var qrow = document.createElement("tr");
    qrow.innerHTML =
      '<td>' + num + '</td>' +
      '<td class="aram">' + form + '</td>' +
      '<td><input class="parse-field" type="text" placeholder="pronoun type"></td>' +
      '<td><input class="parse-field" type="text" placeholder="PGN"></td>' +
      '<td><input class="parse-field" type="text" placeholder="gloss / translation"></td>' +
      '<td><button class="btn btn-ans" onclick="toggle(\'a'+num+'\')">▶ Answer</button></td>';
    tbody.appendChild(qrow);

    var arow = document.createElement("tr");
    arow.id = "a" + num; arow.className = "answer-row";
    arow.innerHTML =
      '<td></td>' +
      '<td class="aram">' + form + '</td>' +
      '<td>' + type + '</td>' +
      '<td>' + pgn + '</td>' +
      '<td colspan="2">' + gloss + '</td>';
    tbody.appendChild(arow);
  });
  t.appendChild(tbody);
});

function toggle(id) {
  var el = document.getElementById(id);
  el.style.display = (el.style.display === "table-row") ? "none" : "table-row";
}
function showAll() { document.querySelectorAll(".answer-row").forEach(function(r){ r.style.display="table-row"; }); }
function hideAll() { document.querySelectorAll(".answer-row").forEach(function(r){ r.style.display="none"; }); }
function clearAll() { document.querySelectorAll("input.parse-field").forEach(function(i){ i.value=""; }); }
</script>

