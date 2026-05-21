# Parsing Drill

*Chapter 18 — Qal Imperative*

[Full screen](ch18-parsing-drill.html){.md-button}  [Markdown](ch18-parsing-drill.md){.md-button}  [Print (PDF)](ch18-parsing-drill.pdf){.md-button}

<style>

body{font-family:Georgia,serif;color:#222}
h1{font-size:1.4em;border-bottom:2px solid #333;padding-bottom:.3em}
h2{font-size:1.15em;margin-top:2em;color:#444}
h3{font-size:1em;color:#555;margin-top:1.5em}
table{border-collapse:collapse;width:100%;margin:.8em 0}
th{background:#2c5f2e;color:#fff;padding:.45em .6em;text-align:left;font-size:.85em}
td{padding:.35em .6em;border:1px solid #ccc;font-size:.9em;vertical-align:top}
tr:nth-child(even){background:#f7f7f7}
.hebrew{font-size:1.3em;direction:rtl;unicode-bidi:embed}
input.f{width:90%;border:none;border-bottom:1px solid #999;background:transparent;font-size:.88em;font-family:inherit;padding:1px 2px}
input.f:focus{outline:none;border-bottom:2px solid #2c5f2e}
.answer-row td{background:#e8f5e9;font-size:.85em}
.answer-row{display:none}
.toggle-btn{background:#2c5f2e;color:#fff;border:none;border-radius:3px;padding:2px 8px;cursor:pointer;font-size:.8em}
.toggle-btn:hover{background:#1e4220}
.controls{margin:.8em 0 1.2em;display:flex;gap:.6em;flex-wrap:wrap}
.ctrl-btn{background:#555;color:#fff;border:none;border-radius:4px;padding:.4em .9em;cursor:pointer;font-size:.85em}
.ctrl-btn:hover{background:#333}
.note-box{background:#fff8dc;border-left:4px solid #c8a800;padding:.6em .9em;margin:.8em 0;font-size:.9em}
@media print{
  .controls,.toggle-btn{display:none}
  input.f{border-bottom:1px solid #000;min-width:60px}
  .answer-row{display:none!important}
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

<h1>Chapter 18 — Qal Imperative Parsing Drill</h1>
<p><em>For each form: (a) Conjugation, (b) Person, (c) Number, (d) Gender, (e) Root. Click <strong>▶ Answer</strong> to reveal; click again to hide.</em></p>

<div class="controls">
  <button class="ctrl-btn" onclick="showAll()">Show All Answers</button>
  <button class="ctrl-btn" onclick="hideAll()">Hide All Answers</button>
  <button class="ctrl-btn" onclick="clearAll()">Clear All Inputs</button>
</div>

<h2>Part A — Strong and Common Roots</h2>
<p><em>All forms are Qal Imperative. Parse the PGN and identify the root.</em></p>
<table>
<tr><th>#</th><th>Form</th><th>Conjugation</th><th>Person</th><th>Number</th><th>Gender</th><th>Root</th><th></th></tr>
<tr><td>1</td><td class="hebrew">שְׁמֹר</td><td><input class="parse-field" id="1-c"></td><td><input class="parse-field" id="1-p"></td><td><input class="parse-field" id="1-n"></td><td><input class="parse-field" id="1-g"></td><td><input class="parse-field" id="1-r"></td><td><button class="toggle-btn" onclick="tog('a1')">▶ Answer</button></td></tr>
<tr class="answer-row" id="a1"><td colspan="8">Imperative · 2nd · Singular · Masculine · שמר — Strong A-class; shewa + holem; "Guard!"</td></tr>

<tr><td>2</td><td class="hebrew">שִׁמְרִי</td><td><input class="parse-field" id="2-c"></td><td><input class="parse-field" id="2-p"></td><td><input class="parse-field" id="2-n"></td><td><input class="parse-field" id="2-g"></td><td><input class="parse-field" id="2-r"></td><td><button class="toggle-btn" onclick="tog('a2')">▶ Answer</button></td></tr>
<tr class="answer-row" id="a2"><td colspan="8">Imperative · 2nd · Singular · Feminine · שמר — + ִי suffix (hireq-yod)</td></tr>

<tr><td>3</td><td class="hebrew">שִׁמְרוּ</td><td><input class="parse-field" id="3-c"></td><td><input class="parse-field" id="3-p"></td><td><input class="parse-field" id="3-n"></td><td><input class="parse-field" id="3-g"></td><td><input class="parse-field" id="3-r"></td><td><button class="toggle-btn" onclick="tog('a3')">▶ Answer</button></td></tr>
<tr class="answer-row" id="a3"><td colspan="8">Imperative · 2nd · Plural · Masculine · שמר — + וּ suffix (shureq)</td></tr>

<tr><td>4</td><td class="hebrew">שְׁמֹרְנָה</td><td><input class="parse-field" id="4-c"></td><td><input class="parse-field" id="4-p"></td><td><input class="parse-field" id="4-n"></td><td><input class="parse-field" id="4-g"></td><td><input class="parse-field" id="4-r"></td><td><button class="toggle-btn" onclick="tog('a4')">▶ Answer</button></td></tr>
<tr class="answer-row" id="a4"><td colspan="8">Imperative · 2nd · Plural · Feminine · שמר — + נָה suffix</td></tr>

<tr><td>5</td><td class="hebrew">שְׁמַע</td><td><input class="parse-field" id="5-c"></td><td><input class="parse-field" id="5-p"></td><td><input class="parse-field" id="5-n"></td><td><input class="parse-field" id="5-g"></td><td><input class="parse-field" id="5-r"></td><td><button class="toggle-btn" onclick="tog('a5')">▶ Answer</button></td></tr>
<tr class="answer-row" id="a5"><td colspan="8">Imperative · 2nd · Singular · Masculine · שמע — B-class; gutt. R3 forces patach instead of holem; "Hear!"</td></tr>

<tr><td>6</td><td class="hebrew">שִׁמְעוּ</td><td><input class="parse-field" id="6-c"></td><td><input class="parse-field" id="6-p"></td><td><input class="parse-field" id="6-n"></td><td><input class="parse-field" id="6-g"></td><td><input class="parse-field" id="6-r"></td><td><button class="toggle-btn" onclick="tog('a6')">▶ Answer</button></td></tr>
<tr class="answer-row" id="a6"><td colspan="8">Imperative · 2nd · Plural · Masculine · שמע — B-class 2mp; + וּ suffix</td></tr>

<tr><td>7</td><td class="hebrew">זְכֹר</td><td><input class="parse-field" id="7-c"></td><td><input class="parse-field" id="7-p"></td><td><input class="parse-field" id="7-n"></td><td><input class="parse-field" id="7-g"></td><td><input class="parse-field" id="7-r"></td><td><button class="toggle-btn" onclick="tog('a7')">▶ Answer</button></td></tr>
<tr class="answer-row" id="a7"><td colspan="8">Imperative · 2nd · Singular · Masculine · זכר — Strong A-class; "Remember!" — frequent in Deuteronomy</td></tr>

<tr><td>8</td><td class="hebrew">חֲזַק</td><td><input class="parse-field" id="8-c"></td><td><input class="parse-field" id="8-p"></td><td><input class="parse-field" id="8-n"></td><td><input class="parse-field" id="8-g"></td><td><input class="parse-field" id="8-r"></td><td><button class="toggle-btn" onclick="tog('a8')">▶ Answer</button></td></tr>
<tr class="answer-row" id="a8"><td colspan="8">Imperative · 2nd · Singular · Masculine · חזק — I-gutt. chateph under ח; B-class patach; "Be strong!" (Deu 31:6)</td></tr>

<tr><td>9</td><td class="hebrew">כְּתֹב</td><td><input class="parse-field" id="9-c"></td><td><input class="parse-field" id="9-p"></td><td><input class="parse-field" id="9-n"></td><td><input class="parse-field" id="9-g"></td><td><input class="parse-field" id="9-r"></td><td><button class="toggle-btn" onclick="tog('a9')">▶ Answer</button></td></tr>
<tr class="answer-row" id="a9"><td colspan="8">Imperative · 2nd · Singular · Masculine · כתב — Strong A-class; "Write!"</td></tr>

<tr><td>10</td><td class="hebrew">קְרָא</td><td><input class="parse-field" id="10-c"></td><td><input class="parse-field" id="10-p"></td><td><input class="parse-field" id="10-n"></td><td><input class="parse-field" id="10-g"></td><td><input class="parse-field" id="10-r"></td><td><button class="toggle-btn" onclick="tog('a10')">▶ Answer</button></td></tr>
<tr class="answer-row" id="a10"><td colspan="8">Imperative · 2nd · Singular · Masculine · קרא — III-א; qamets before quiescent aleph; "Call / Read!"</td></tr>
</table>

<h2>Part B — Weak Root Imperatives</h2>
<table>
<tr><th>#</th><th>Form</th><th>Conjugation</th><th>Person</th><th>Number</th><th>Gender</th><th>Root</th><th>Weak Class</th><th></th></tr>
<tr><td>11</td><td class="hebrew">לֵךְ</td><td><input class="parse-field" id="11-c"></td><td><input class="parse-field" id="11-p"></td><td><input class="parse-field" id="11-n"></td><td><input class="parse-field" id="11-g"></td><td><input class="parse-field" id="11-r"></td><td><input class="parse-field" id="11-w"></td><td><button class="toggle-btn" onclick="tog('b11')">▶ Answer</button></td></tr>
<tr class="answer-row" id="b11"><td colspan="9">Imperative · 2nd · Singular · Masculine · הלך · I-י — Extremely short; tsere; ה of הלך absent; "Go!"</td></tr>

<tr><td>12</td><td class="hebrew">לְכוּ</td><td><input class="parse-field" id="12-c"></td><td><input class="parse-field" id="12-p"></td><td><input class="parse-field" id="12-n"></td><td><input class="parse-field" id="12-g"></td><td><input class="parse-field" id="12-r"></td><td><input class="parse-field" id="12-w"></td><td><button class="toggle-btn" onclick="tog('b12')">▶ Answer</button></td></tr>
<tr class="answer-row" id="b12"><td colspan="9">Imperative · 2nd · Plural · Masculine · הלך · I-י — + וּ; shewa under ל</td></tr>

<tr><td>13</td><td class="hebrew">עֲשֵׂה</td><td><input class="parse-field" id="13-c"></td><td><input class="parse-field" id="13-p"></td><td><input class="parse-field" id="13-n"></td><td><input class="parse-field" id="13-g"></td><td><input class="parse-field" id="13-r"></td><td><input class="parse-field" id="13-w"></td><td><button class="toggle-btn" onclick="tog('b13')">▶ Answer</button></td></tr>
<tr class="answer-row" id="b13"><td colspan="9">Imperative · 2nd · Singular · Masculine · עשה · III-ה + I-gutt. — ה retained in 2ms; chateph under ע; "Do / Make!"</td></tr>

<tr><td>14</td><td class="hebrew">עֲשׂוּ</td><td><input class="parse-field" id="14-c"></td><td><input class="parse-field" id="14-p"></td><td><input class="parse-field" id="14-n"></td><td><input class="parse-field" id="14-g"></td><td><input class="parse-field" id="14-r"></td><td><input class="parse-field" id="14-w"></td><td><button class="toggle-btn" onclick="tog('b14')">▶ Answer</button></td></tr>
<tr class="answer-row" id="b14"><td colspan="9">Imperative · 2nd · Plural · Masculine · עשה · III-ה + I-gutt. — ה drops before -וּ</td></tr>

<tr><td>15</td><td class="hebrew">רְאֵה</td><td><input class="parse-field" id="15-c"></td><td><input class="parse-field" id="15-p"></td><td><input class="parse-field" id="15-n"></td><td><input class="parse-field" id="15-g"></td><td><input class="parse-field" id="15-r"></td><td><input class="parse-field" id="15-w"></td><td><button class="toggle-btn" onclick="tog('b15')">▶ Answer</button></td></tr>
<tr class="answer-row" id="b15"><td colspan="9">Imperative · 2nd · Singular · Masculine · ראה · III-ה — ה retained; tsere before ה; "See!"</td></tr>

<tr><td>16</td><td class="hebrew">קוּם</td><td><input class="parse-field" id="16-c"></td><td><input class="parse-field" id="16-p"></td><td><input class="parse-field" id="16-n"></td><td><input class="parse-field" id="16-g"></td><td><input class="parse-field" id="16-r"></td><td><input class="parse-field" id="16-w"></td><td><button class="toggle-btn" onclick="tog('b16')">▶ Answer</button></td></tr>
<tr class="answer-row" id="b16"><td colspan="9">Imperative · 2nd · Singular · Masculine · קום · Biconsonantal — Full shureq vowel retained; "Arise!"</td></tr>

<tr><td>17</td><td class="hebrew">קוּמִי</td><td><input class="parse-field" id="17-c"></td><td><input class="parse-field" id="17-p"></td><td><input class="parse-field" id="17-n"></td><td><input class="parse-field" id="17-g"></td><td><input class="parse-field" id="17-r"></td><td><input class="parse-field" id="17-w"></td><td><button class="toggle-btn" onclick="tog('b17')">▶ Answer</button></td></tr>
<tr class="answer-row" id="b17"><td colspan="9">Imperative · 2nd · Singular · Feminine · קום · Biconsonantal — + ִי suffix</td></tr>

<tr><td>18</td><td class="hebrew">בֹּא</td><td><input class="parse-field" id="18-c"></td><td><input class="parse-field" id="18-p"></td><td><input class="parse-field" id="18-n"></td><td><input class="parse-field" id="18-g"></td><td><input class="parse-field" id="18-r"></td><td><input class="parse-field" id="18-w"></td><td><button class="toggle-btn" onclick="tog('b18')">▶ Answer</button></td></tr>
<tr class="answer-row" id="b18"><td colspan="9">Imperative · 2nd · Singular · Masculine · בוא · Biconsonantal — Holem-waw; aleph quiesces; "Come / Enter!"</td></tr>

<tr><td>19</td><td class="hebrew">שׁוּב</td><td><input class="parse-field" id="19-c"></td><td><input class="parse-field" id="19-p"></td><td><input class="parse-field" id="19-n"></td><td><input class="parse-field" id="19-g"></td><td><input class="parse-field" id="19-r"></td><td><input class="parse-field" id="19-w"></td><td><button class="toggle-btn" onclick="tog('b19')">▶ Answer</button></td></tr>
<tr class="answer-row" id="b19"><td colspan="9">Imperative · 2nd · Singular · Masculine · שוב · Biconsonantal — Full shureq retained; "Return!"</td></tr>

<tr><td>20</td><td class="hebrew">שֵׁב</td><td><input class="parse-field" id="20-c"></td><td><input class="parse-field" id="20-p"></td><td><input class="parse-field" id="20-n"></td><td><input class="parse-field" id="20-g"></td><td><input class="parse-field" id="20-r"></td><td><input class="parse-field" id="20-w"></td><td><button class="toggle-btn" onclick="tog('b20')">▶ Answer</button></td></tr>
<tr class="answer-row" id="b20"><td colspan="9">Imperative · 2nd · Singular · Masculine · ישב · I-י — Short form; tsere; yod absent; "Sit / Dwell!"</td></tr>

<tr><td>21</td><td class="hebrew">צֵא</td><td><input class="parse-field" id="21-c"></td><td><input class="parse-field" id="21-p"></td><td><input class="parse-field" id="21-n"></td><td><input class="parse-field" id="21-g"></td><td><input class="parse-field" id="21-r"></td><td><input class="parse-field" id="21-w"></td><td><button class="toggle-btn" onclick="tog('b21')">▶ Answer</button></td></tr>
<tr class="answer-row" id="b21"><td colspan="9">Imperative · 2nd · Singular · Masculine · יצא · I-י + III-א — Tsere; aleph quiesces at R3; "Go out!"</td></tr>

<tr><td>22</td><td class="hebrew">תֵּן</td><td><input class="parse-field" id="22-c"></td><td><input class="parse-field" id="22-p"></td><td><input class="parse-field" id="22-n"></td><td><input class="parse-field" id="22-g"></td><td><input class="parse-field" id="22-r"></td><td><input class="parse-field" id="22-w"></td><td><button class="toggle-btn" onclick="tog('b22')">▶ Answer</button></td></tr>
<tr class="answer-row" id="b22"><td colspan="9">Imperative · 2nd · Singular · Masculine · נתן · I-נ — Both nuns drop/assimilate; very short; "Give!"</td></tr>

<tr><td>23</td><td class="hebrew">תְּנוּ</td><td><input class="parse-field" id="23-c"></td><td><input class="parse-field" id="23-p"></td><td><input class="parse-field" id="23-n"></td><td><input class="parse-field" id="23-g"></td><td><input class="parse-field" id="23-r"></td><td><input class="parse-field" id="23-w"></td><td><button class="toggle-btn" onclick="tog('b23')">▶ Answer</button></td></tr>
<tr class="answer-row" id="b23"><td colspan="9">Imperative · 2nd · Plural · Masculine · נתן · I-נ — + וּ suffix</td></tr>

<tr><td>24</td><td class="hebrew">אֱמֹר</td><td><input class="parse-field" id="24-c"></td><td><input class="parse-field" id="24-p"></td><td><input class="parse-field" id="24-n"></td><td><input class="parse-field" id="24-g"></td><td><input class="parse-field" id="24-r"></td><td><input class="parse-field" id="24-w"></td><td><button class="toggle-btn" onclick="tog('b24')">▶ Answer</button></td></tr>
<tr class="answer-row" id="b24"><td colspan="9">Imperative · 2nd · Singular · Masculine · אמר · I-aleph — Hateph-seghol under aleph; "Say!"</td></tr>

<tr><td>25</td><td class="hebrew">קַח</td><td><input class="parse-field" id="25-c"></td><td><input class="parse-field" id="25-p"></td><td><input class="parse-field" id="25-n"></td><td><input class="parse-field" id="25-g"></td><td><input class="parse-field" id="25-r"></td><td><input class="parse-field" id="25-w"></td><td><button class="toggle-btn" onclick="tog('b25')">▶ Answer</button></td></tr>
<tr class="answer-row" id="b25"><td colspan="9">Imperative · 2nd · Singular · Masculine · לקח · I-י — Short form; from יִקַּח; "Take!"</td></tr>
</table>

<h2>Part C — Disambiguation: Imperative, Imperfect, or Jussive?</h2>

<div class="note-box"><strong>Key rule:</strong> Positive commands use the <strong>Imperative</strong> (no prefix). Negative commands <em>never</em> use the Imperative — they use <strong>אַל + Jussive</strong> (immediate prohibition) or <strong>לֹא + Imperfect</strong> (permanent prohibition).</div>

<table>
<tr><th>#</th><th>Form</th><th>Form Type</th><th>Person</th><th>Number</th><th>Gender</th><th>Root</th><th></th></tr>
<tr><td>26</td><td class="hebrew">שְׁמֹר</td><td><input class="parse-field" id="26-t"></td><td><input class="parse-field" id="26-p"></td><td><input class="parse-field" id="26-n"></td><td><input class="parse-field" id="26-g"></td><td><input class="parse-field" id="26-r"></td><td><button class="toggle-btn" onclick="tog('c26')">▶ Answer</button></td></tr>
<tr class="answer-row" id="c26"><td colspan="8">Imperative · 2nd · Singular · Masculine · שמר — No prefix; direct positive command</td></tr>

<tr><td>27</td><td class="hebrew">יִשְׁמֹר</td><td><input class="parse-field" id="27-t"></td><td><input class="parse-field" id="27-p"></td><td><input class="parse-field" id="27-n"></td><td><input class="parse-field" id="27-g"></td><td><input class="parse-field" id="27-r"></td><td><button class="toggle-btn" onclick="tog('c27')">▶ Answer</button></td></tr>
<tr class="answer-row" id="c27"><td colspan="8">Imperfect · 3rd · Singular · Masculine · שמר — יִ– prefix; not a command; "he will keep"</td></tr>

<tr><td>28</td><td class="hebrew">אַל־יִשְׁמֹר</td><td><input class="parse-field" id="28-t"></td><td><input class="parse-field" id="28-p"></td><td><input class="parse-field" id="28-n"></td><td><input class="parse-field" id="28-g"></td><td><input class="parse-field" id="28-r"></td><td><button class="toggle-btn" onclick="tog('c28')">▶ Answer</button></td></tr>
<tr class="answer-row" id="c28"><td colspan="8">Jussive (with אַל) · 3rd · Singular · Masculine · שמר — אַל + Jussive = negative prohibition; "let him not keep"</td></tr>

<tr><td>29</td><td class="hebrew">לְכוּ</td><td><input class="parse-field" id="29-t"></td><td><input class="parse-field" id="29-p"></td><td><input class="parse-field" id="29-n"></td><td><input class="parse-field" id="29-g"></td><td><input class="parse-field" id="29-r"></td><td><button class="toggle-btn" onclick="tog('c29')">▶ Answer</button></td></tr>
<tr class="answer-row" id="c29"><td colspan="8">Imperative · 2nd · Plural · Masculine · הלך — No prefix; I-י imperative 2mp; "Go!" (pl.)</td></tr>

<tr><td>30</td><td class="hebrew">יֵלְכוּ</td><td><input class="parse-field" id="30-t"></td><td><input class="parse-field" id="30-p"></td><td><input class="parse-field" id="30-n"></td><td><input class="parse-field" id="30-g"></td><td><input class="parse-field" id="30-r"></td><td><button class="toggle-btn" onclick="tog('c30')">▶ Answer</button></td></tr>
<tr class="answer-row" id="c30"><td colspan="8">Imperfect · 3rd · Plural · Masculine · הלך — יֵ– prefix; I-י imperfect 3mp; "they will go"</td></tr>

<tr><td>31</td><td class="hebrew">עֲשֵׂה</td><td><input class="parse-field" id="31-t"></td><td><input class="parse-field" id="31-p"></td><td><input class="parse-field" id="31-n"></td><td><input class="parse-field" id="31-g"></td><td><input class="parse-field" id="31-r"></td><td><button class="toggle-btn" onclick="tog('c31')">▶ Answer</button></td></tr>
<tr class="answer-row" id="c31"><td colspan="8">Imperative · 2nd · Singular · Masculine · עשה — No prefix; III-ה 2ms; ה retained; "Do / Make!"</td></tr>

<tr><td>32</td><td class="hebrew">יַעַשׂ</td><td><input class="parse-field" id="32-t"></td><td><input class="parse-field" id="32-p"></td><td><input class="parse-field" id="32-n"></td><td><input class="parse-field" id="32-g"></td><td><input class="parse-field" id="32-r"></td><td><button class="toggle-btn" onclick="tog('c32')">▶ Answer</button></td></tr>
<tr class="answer-row" id="c32"><td colspan="8">Jussive / Imperfect · 3rd · Singular · Masculine · עשה — III-ה short form; context determines Jussive vs. Imperfect; "he will do / let him do"</td></tr>

<tr><td>33</td><td class="hebrew">אַל־תַּעַשׂ</td><td><input class="parse-field" id="33-t"></td><td><input class="parse-field" id="33-p"></td><td><input class="parse-field" id="33-n"></td><td><input class="parse-field" id="33-g"></td><td><input class="parse-field" id="33-r"></td><td><button class="toggle-btn" onclick="tog('c33')">▶ Answer</button></td></tr>
<tr class="answer-row" id="c33"><td colspan="8">Jussive (with אַל) · 2nd · Singular · Masculine · עשה — אַל + Jussive 2ms; "Do not do!" — note: NOT Imperative; Hebrew uses Jussive for negated commands</td></tr>

<tr><td>34</td><td class="hebrew">בֹּא</td><td><input class="parse-field" id="34-t"></td><td><input class="parse-field" id="34-p"></td><td><input class="parse-field" id="34-n"></td><td><input class="parse-field" id="34-g"></td><td><input class="parse-field" id="34-r"></td><td><button class="toggle-btn" onclick="tog('c34')">▶ Answer</button></td></tr>
<tr class="answer-row" id="c34"><td colspan="8">Imperative · 2nd · Singular · Masculine · בוא — No prefix; biconsonantal 2ms; "Come / Enter!"</td></tr>

<tr><td>35</td><td class="hebrew">יָבֹא</td><td><input class="parse-field" id="35-t"></td><td><input class="parse-field" id="35-p"></td><td><input class="parse-field" id="35-n"></td><td><input class="parse-field" id="35-g"></td><td><input class="parse-field" id="35-r"></td><td><button class="toggle-btn" onclick="tog('c35')">▶ Answer</button></td></tr>
<tr class="answer-row" id="c35"><td colspan="8">Imperfect · 3rd · Singular · Masculine · בוא — יָ– prefix; biconsonantal imperfect; "he will come"</td></tr>
</table>

<script>
function tog(id){
  var r=document.getElementById(id);
  var btn=r.previousElementSibling.querySelector('.toggle-btn');
  if(r.style.display==='table-row'){r.style.display='none';btn.textContent='▶ Answer';}
  else{r.style.display='table-row';btn.textContent='▼ Hide';}
}
function showAll(){
  document.querySelectorAll('.answer-row').forEach(function(r){r.style.display='table-row';});
  document.querySelectorAll('.toggle-btn').forEach(function(b){b.textContent='▼ Hide';});
}
function hideAll(){
  document.querySelectorAll('.answer-row').forEach(function(r){r.style.display='none';});
  document.querySelectorAll('.toggle-btn').forEach(function(b){b.textContent='▶ Answer';});
}
function clearAll(){
  document.querySelectorAll('input.f').forEach(function(i){i.value='';});
}
</script>

