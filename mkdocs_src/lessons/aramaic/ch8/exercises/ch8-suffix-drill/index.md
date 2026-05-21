# Suffix Drill

*Chapter 8 — Pronominal Suffixes*

[Full screen](ch8-suffix-drill.html){.md-button}  [Markdown](ch8-suffix-drill.md){.md-button}  [Print (PDF)](ch8-suffix-drill.pdf){.md-button}

<style>

  body { font-family: Arial, sans-serif;    }
  h1 { font-size: 1.3em; }
  p.instructions { background: #f5f5f5; border-left: 4px solid #888; padding: .6em 1em; }
  table { border-collapse: collapse; width: 100%; margin-bottom: 1.5em; }
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

<h1>BBA Chapter 8 — Suffix Drill</h1>
<p class="instructions"><strong>Instructions:</strong> For each form, identify the base form (noun or preposition), the pronominal suffix (person, gender, number), and give the English translation.</p>

<div class="global-btns">
  <button class="btn" onclick="showAll()">Show All Answers</button>
  <button class="btn" onclick="hideAll()">Hide All Answers</button>
  <button class="btn" onclick="clearAll()">Clear All Inputs</button>
</div>

<script>
// [num, form, baseForm, suffix, translation]
var rows = [
  [1,  "מַלְכִּי",       "מֶלֶךְ (king, ms)",          "1cs",  "my king"],
  [2,  "אֱלָהֲנָא",     "אֱלָה (God, ms)",             "1cp",  "our God"],
  [3,  "אַבוּהִי",       "אַב (father, ms)",             "3ms",  "his father"],
  [4,  "עַלַיְכוֹן",    "עַל (upon, prep)",             "2mp",  "upon you (mp)"],
  [5,  "בֵּיתֵהּ",       "בַּיִת (house, ms)",           "3ms",  "his house"],
  [6,  "לְמַלְכָּה",    "לְ- (to/for, prep)",           "3fs",  "to/for her"],
  [7,  "מִנִּי",         "מִן (from, prep)",             "1cs",  "from me"],
  [8,  "עַבְדֵיהוֹן",   "עֶבֶד (servant, ms pl)",       "3mp",  "their servants"],
  [9,  "אַנְפּוֹהִי",   "אַנְפִּין (face, mp)",         "3ms",  "his face"],
  [10, "יְדֵהּ",         "יַד (hand, fs)",               "3ms",  "his hand"],
  [11, "עֲלֵיהוֹן",     "עַל (upon, prep)",             "3mp",  "upon them (mp)"],
  [12, "לְהוֹן",         "לְ- (to/for, prep)",           "3mp",  "to/for them"],
  [13, "אֱלָהֵהּ",       "אֱלָה (God, ms)",             "3ms",  "his God"],
  [14, "מַלְכוּתִי",    "מַלְכוּ (kingdom, fs)",        "1cs",  "my kingdom"],
  [15, "עִמֵּהּ",         "עִם (with, prep)",            "3ms",  "with him"],
  [16, "רֵאשֵׁהּ",       "רֵאשׁ (head, ms)",            "3ms",  "his head"],
  [17, "קֳדָמַי",        "קֳדָם (before, prep)",         "1cs",  "before me"],
  [18, "שְׁמֵהּ",         "שֵׁם (name, ms)",             "3ms",  "his name"],
  [19, "בָּנַיְכוֹן",   "בַּר (son → pl. בָּנִין)",     "2mp",  "your (mp) sons"],
  [20, "מִנְּהוֹן",      "מִן (from, prep)",             "3mp",  "from them"]
];

document.addEventListener("DOMContentLoaded", function() {
  var t = document.createElement("table"); document.body.appendChild(t);
  var thead = document.createElement("thead");
  var hr = document.createElement("tr");
  ["#","Form","Base Form","Suffix (PGN)","Translation",""].forEach(function(h){
    var th = document.createElement("th"); th.textContent = h; hr.appendChild(th);
  });
  thead.appendChild(hr); t.appendChild(thead);

  var tbody = document.createElement("tbody");
  rows.forEach(function(row) {
    var num = row[0], form = row[1], base = row[2], suf = row[3], trans = row[4];

    var qrow = document.createElement("tr");
    qrow.innerHTML =
      '<td>' + num + '</td>' +
      '<td class="aram">' + form + '</td>' +
      '<td><input class="parse-field" type="text" placeholder="base form"></td>' +
      '<td><input class="parse-field" type="text" placeholder="person-gender-number"></td>' +
      '<td><input class="parse-field" type="text" placeholder="translation"></td>' +
      '<td><button class="btn btn-ans" onclick="toggle(\'a'+num+'\')">▶ Answer</button></td>';
    tbody.appendChild(qrow);

    var arow = document.createElement("tr");
    arow.id = "a" + num; arow.className = "answer-row";
    arow.innerHTML =
      '<td></td>' +
      '<td class="aram">' + form + '</td>' +
      '<td>' + base + '</td>' +
      '<td>' + suf + '</td>' +
      '<td colspan="2">' + trans + '</td>';
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

