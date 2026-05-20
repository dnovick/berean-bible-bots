# Relative Parsing

*Chapter 14 — Relative Pronoun*

[Full screen](ch14-relative-parsing.html){.md-button}  [Markdown](ch14-relative-parsing.md){.md-button}  [Print (PDF)](ch14-relative-parsing.pdf){.md-button}

<style>

  body { font-family: Georgia, serif;    color: #222; }
  h1 { font-size: 1.4em; border-bottom: 2px solid #444; padding-bottom: 0.3em; }
  p.instructions { font-style: italic; color: #555; }
  table { border-collapse: collapse; width: 100%; margin: 1.5em 0; font-size: 0.9em; }
  th { background: #2c5282; color: #fff; padding: 0.45em 0.6em; text-align: left; }
  td { padding: 0.35em 0.6em; border-bottom: 1px solid #ddd; vertical-align: top; }
  tr:nth-child(even) td { background: #f7f7f7; }
  .greek { font-size: 1.1em; font-family: "New Athena Unicode", "Gentium Plus", "SBL Greek", serif; }
  input.parse-field {
    border: none; border-bottom: 1px solid #888; width: 100%; min-width: 55px;
    background: transparent; font-size: 0.88em; padding: 2px 4px; box-sizing: border-box;
  }
  input.parse-field:focus { outline: none; border-bottom: 2px solid #2c5282; }
  input.wide { min-width: 110px; }
  .answer-row td { background: #d4edda !important; color: #155724; font-size: 0.88em; }
  .answer-row { display: none; }
  .answer-row.visible { display: table-row; }
  button.reveal-btn {
    background: #2c5282; color: #fff; border: none; border-radius: 3px;
    padding: 3px 10px; cursor: pointer; font-size: 0.82em; white-space: nowrap;
  }
  button.reveal-btn:hover { background: #1a365d; }
  .controls { margin: 1em 0 1.5em 0; display: flex; gap: 0.7em; flex-wrap: wrap; }
  .controls button {
    background: #4a5568; color: #fff; border: none; border-radius: 4px;
    padding: 0.5em 1.2em; cursor: pointer; font-size: 0.88em;
  }
  .controls button:hover { background: #2d3748; }
  .note { background: #fffbea; border-left: 4px solid #d69e2e; padding: 0.6em 1em; margin: 1em 0; font-size: 0.9em; }
  @media print {
    .controls, button.reveal-btn { display: none !important; }
    .answer-row { display: none !important; }
    input.parse-field { border-bottom: 1px solid #000; background: transparent; }
    body {  }
  }

</style>

<h1>BBG Chapter 14 — Relative Pronoun Parsing Drill</h1>
<p class="instructions">For each item: (1) parse the relative pronoun (gender, case, number), (2) identify its antecedent, and (3) translate the phrase. Click ▶ Answer to check your work.</p>

<div class="controls">
  <button onclick="showAll()">Show All Answers</button>
  <button onclick="hideAll()">Hide All Answers</button>
  <button onclick="clearAll()">Clear All Inputs</button>
</div>

<table>
  <thead>
    <tr>
      <th>#</th>
      <th>Phrase / Clause</th>
      <th>Rel. pron.</th>
      <th>Gender</th>
      <th>Case</th>
      <th>Number</th>
      <th>Antecedent</th>
      <th>Translation</th>
      <th></th>
    </tr>
  </thead>
  <tbody>

    <tr class="question-row" data-id="1">
      <td>1</td>
      <td class="greek">ὁ ἄνθρωπος <strong>ὃν</strong> εἶδον</td>
      <td class="greek">ὃν</td>
      <td><input class="parse-field" type="text" placeholder="gender"></td>
      <td><input class="parse-field" type="text" placeholder="case"></td>
      <td><input class="parse-field" type="text" placeholder="number"></td>
      <td><input class="parse-field wide" type="text" placeholder="antecedent"></td>
      <td><input class="parse-field wide" type="text" placeholder="translation"></td>
      <td><button class="reveal-btn" onclick="toggle(1)">▶ Answer</button></td>
    </tr>
    <tr class="answer-row" id="ans-1">
      <td></td>
      <td colspan="8"><strong>Masculine · Accusative · Singular</strong> | Antecedent: ὁ ἄνθρωπος | "the man <em>whom</em> I saw" — direct object of εἶδον</td>
    </tr>

    <tr class="question-row" data-id="2">
      <td>2</td>
      <td class="greek">ἡ γυνή <strong>ἣν</strong> ἀγαπᾷς</td>
      <td class="greek">ἣν</td>
      <td><input class="parse-field" type="text" placeholder="gender"></td>
      <td><input class="parse-field" type="text" placeholder="case"></td>
      <td><input class="parse-field" type="text" placeholder="number"></td>
      <td><input class="parse-field wide" type="text" placeholder="antecedent"></td>
      <td><input class="parse-field wide" type="text" placeholder="translation"></td>
      <td><button class="reveal-btn" onclick="toggle(2)">▶ Answer</button></td>
    </tr>
    <tr class="answer-row" id="ans-2">
      <td></td>
      <td colspan="8"><strong>Feminine · Accusative · Singular</strong> | Antecedent: ἡ γυνή | "the woman <em>whom</em> you love" — direct object of ἀγαπᾷς</td>
    </tr>

    <tr class="question-row" data-id="3">
      <td>3</td>
      <td class="greek">τὸ τέκνον <strong>ὃ</strong> εἶχεν</td>
      <td class="greek">ὃ</td>
      <td><input class="parse-field" type="text" placeholder="gender"></td>
      <td><input class="parse-field" type="text" placeholder="case"></td>
      <td><input class="parse-field" type="text" placeholder="number"></td>
      <td><input class="parse-field wide" type="text" placeholder="antecedent"></td>
      <td><input class="parse-field wide" type="text" placeholder="translation"></td>
      <td><button class="reveal-btn" onclick="toggle(3)">▶ Answer</button></td>
    </tr>
    <tr class="answer-row" id="ans-3">
      <td></td>
      <td colspan="8"><strong>Neuter · Accusative · Singular</strong> | Antecedent: τὸ τέκνον | "the child <em>that</em> he had" — direct object of εἶχεν</td>
    </tr>

    <tr class="question-row" data-id="4">
      <td>4</td>
      <td class="greek">οἱ μαθηταί <strong>οἳ</strong> ἤκουσαν</td>
      <td class="greek">οἳ</td>
      <td><input class="parse-field" type="text" placeholder="gender"></td>
      <td><input class="parse-field" type="text" placeholder="case"></td>
      <td><input class="parse-field" type="text" placeholder="number"></td>
      <td><input class="parse-field wide" type="text" placeholder="antecedent"></td>
      <td><input class="parse-field wide" type="text" placeholder="translation"></td>
      <td><button class="reveal-btn" onclick="toggle(4)">▶ Answer</button></td>
    </tr>
    <tr class="answer-row" id="ans-4">
      <td></td>
      <td colspan="8"><strong>Masculine · Nominative · Plural</strong> | Antecedent: οἱ μαθηταί | "the disciples <em>who</em> heard" — subject of ἤκουσαν</td>
    </tr>

    <tr class="question-row" data-id="5">
      <td>5</td>
      <td class="greek">ἡ ὥρα <strong>ἐν ᾗ</strong> ἀκούσουσιν</td>
      <td class="greek">ᾗ</td>
      <td><input class="parse-field" type="text" placeholder="gender"></td>
      <td><input class="parse-field" type="text" placeholder="case"></td>
      <td><input class="parse-field" type="text" placeholder="number"></td>
      <td><input class="parse-field wide" type="text" placeholder="antecedent"></td>
      <td><input class="parse-field wide" type="text" placeholder="translation"></td>
      <td><button class="reveal-btn" onclick="toggle(5)">▶ Answer</button></td>
    </tr>
    <tr class="answer-row" id="ans-5">
      <td></td>
      <td colspan="8"><strong>Feminine · Dative · Singular</strong> | Antecedent: ἡ ὥρα | "the hour <em>in which</em> they will hear" — dative object of ἐν (John 5:28)</td>
    </tr>

    <tr class="question-row" data-id="6">
      <td>6</td>
      <td class="greek">ὁ λόγος <strong>οὗ</strong> ἤκουσας</td>
      <td class="greek">οὗ</td>
      <td><input class="parse-field" type="text" placeholder="gender"></td>
      <td><input class="parse-field" type="text" placeholder="case"></td>
      <td><input class="parse-field" type="text" placeholder="number"></td>
      <td><input class="parse-field wide" type="text" placeholder="antecedent"></td>
      <td><input class="parse-field wide" type="text" placeholder="translation"></td>
      <td><button class="reveal-btn" onclick="toggle(6)">▶ Answer</button></td>
    </tr>
    <tr class="answer-row" id="ans-6">
      <td></td>
      <td colspan="8"><strong>Masculine · Genitive · Singular</strong> | Antecedent: ὁ λόγος | "the word <em>that</em> you heard" — genitive of content</td>
    </tr>

    <tr class="question-row" data-id="7">
      <td>7</td>
      <td class="greek">τὰ ἔργα <strong>ἃ</strong> ποιεῖ</td>
      <td class="greek">ἃ</td>
      <td><input class="parse-field" type="text" placeholder="gender"></td>
      <td><input class="parse-field" type="text" placeholder="case"></td>
      <td><input class="parse-field" type="text" placeholder="number"></td>
      <td><input class="parse-field wide" type="text" placeholder="antecedent"></td>
      <td><input class="parse-field wide" type="text" placeholder="translation"></td>
      <td><button class="reveal-btn" onclick="toggle(7)">▶ Answer</button></td>
    </tr>
    <tr class="answer-row" id="ans-7">
      <td></td>
      <td colspan="8"><strong>Neuter · Accusative · Plural</strong> | Antecedent: τὰ ἔργα | "the works <em>that</em> he does" — direct object of ποιεῖ</td>
    </tr>

    <tr class="question-row" data-id="8">
      <td>8</td>
      <td class="greek">ὁ ἄγγελος <strong>ᾧ</strong> ἐλάλησεν</td>
      <td class="greek">ᾧ</td>
      <td><input class="parse-field" type="text" placeholder="gender"></td>
      <td><input class="parse-field" type="text" placeholder="case"></td>
      <td><input class="parse-field" type="text" placeholder="number"></td>
      <td><input class="parse-field wide" type="text" placeholder="antecedent"></td>
      <td><input class="parse-field wide" type="text" placeholder="translation"></td>
      <td><button class="reveal-btn" onclick="toggle(8)">▶ Answer</button></td>
    </tr>
    <tr class="answer-row" id="ans-8">
      <td></td>
      <td colspan="8"><strong>Masculine · Dative · Singular</strong> | Antecedent: ὁ ἄγγελος | "the angel <em>to whom</em> he spoke" — indirect object of ἐλάλησεν</td>
    </tr>

    <tr class="question-row" data-id="9">
      <td>9</td>
      <td class="greek">αἱ γυναῖκες <strong>αἷς</strong> εἶπεν</td>
      <td class="greek">αἷς</td>
      <td><input class="parse-field" type="text" placeholder="gender"></td>
      <td><input class="parse-field" type="text" placeholder="case"></td>
      <td><input class="parse-field" type="text" placeholder="number"></td>
      <td><input class="parse-field wide" type="text" placeholder="antecedent"></td>
      <td><input class="parse-field wide" type="text" placeholder="translation"></td>
      <td><button class="reveal-btn" onclick="toggle(9)">▶ Answer</button></td>
    </tr>
    <tr class="answer-row" id="ans-9">
      <td></td>
      <td colspan="8"><strong>Feminine · Dative · Plural</strong> | Antecedent: αἱ γυναῖκες | "the women <em>to whom</em> he said (it)" — indirect object of εἶπεν</td>
    </tr>

    <tr class="question-row" data-id="10">
      <td>10</td>
      <td class="greek">ὁ πατήρ <strong>οὗ</strong> ὁ υἱός ἐστιν</td>
      <td class="greek">οὗ</td>
      <td><input class="parse-field" type="text" placeholder="gender"></td>
      <td><input class="parse-field" type="text" placeholder="case"></td>
      <td><input class="parse-field" type="text" placeholder="number"></td>
      <td><input class="parse-field wide" type="text" placeholder="antecedent"></td>
      <td><input class="parse-field wide" type="text" placeholder="translation"></td>
      <td><button class="reveal-btn" onclick="toggle(10)">▶ Answer</button></td>
    </tr>
    <tr class="answer-row" id="ans-10">
      <td></td>
      <td colspan="8"><strong>Masculine · Genitive · Singular</strong> | Antecedent: ὁ πατήρ | "the father <em>whose</em> son he is" — genitive of possession</td>
    </tr>

    <tr class="question-row" data-id="11">
      <td>11</td>
      <td class="greek">τὸ ῥῆμα <strong>ὃ</strong> εἶπεν αὐτοῖς</td>
      <td class="greek">ὃ</td>
      <td><input class="parse-field" type="text" placeholder="gender"></td>
      <td><input class="parse-field" type="text" placeholder="case"></td>
      <td><input class="parse-field" type="text" placeholder="number"></td>
      <td><input class="parse-field wide" type="text" placeholder="antecedent"></td>
      <td><input class="parse-field wide" type="text" placeholder="translation"></td>
      <td><button class="reveal-btn" onclick="toggle(11)">▶ Answer</button></td>
    </tr>
    <tr class="answer-row" id="ans-11">
      <td></td>
      <td colspan="8"><strong>Neuter · Accusative · Singular</strong> | Antecedent: τὸ ῥῆμα | "the word <em>that</em> he said to them" — direct object of εἶπεν</td>
    </tr>

    <tr class="question-row" data-id="12">
      <td>12</td>
      <td class="greek">πᾶς <strong>ὃς</strong> πιστεύει εἰς αὐτόν</td>
      <td class="greek">ὃς</td>
      <td><input class="parse-field" type="text" placeholder="gender"></td>
      <td><input class="parse-field" type="text" placeholder="case"></td>
      <td><input class="parse-field" type="text" placeholder="number"></td>
      <td><input class="parse-field wide" type="text" placeholder="antecedent"></td>
      <td><input class="parse-field wide" type="text" placeholder="translation"></td>
      <td><button class="reveal-btn" onclick="toggle(12)">▶ Answer</button></td>
    </tr>
    <tr class="answer-row" id="ans-12">
      <td></td>
      <td colspan="8"><strong>Masculine · Nominative · Singular</strong> | Antecedent: πᾶς | "everyone <em>who</em> believes in him" — subject of πιστεύει; indefinite/universal sense</td>
    </tr>

    <tr class="question-row" data-id="13">
      <td>13</td>
      <td class="greek">ἡ βασιλεία <strong>ἧς</strong> οὐκ ἔσται τέλος</td>
      <td class="greek">ἧς</td>
      <td><input class="parse-field" type="text" placeholder="gender"></td>
      <td><input class="parse-field" type="text" placeholder="case"></td>
      <td><input class="parse-field" type="text" placeholder="number"></td>
      <td><input class="parse-field wide" type="text" placeholder="antecedent"></td>
      <td><input class="parse-field wide" type="text" placeholder="translation"></td>
      <td><button class="reveal-btn" onclick="toggle(13)">▶ Answer</button></td>
    </tr>
    <tr class="answer-row" id="ans-13">
      <td></td>
      <td colspan="8"><strong>Feminine · Genitive · Singular</strong> | Antecedent: ἡ βασιλεία | "the kingdom <em>of which</em> there will be no end" — genitive of relation (Luke 1:33)</td>
    </tr>

    <tr class="question-row" data-id="14">
      <td>14</td>
      <td class="greek">οἱ νόμοι <strong>οἷς</strong> πιστεύετε</td>
      <td class="greek">οἷς</td>
      <td><input class="parse-field" type="text" placeholder="gender"></td>
      <td><input class="parse-field" type="text" placeholder="case"></td>
      <td><input class="parse-field" type="text" placeholder="number"></td>
      <td><input class="parse-field wide" type="text" placeholder="antecedent"></td>
      <td><input class="parse-field wide" type="text" placeholder="translation"></td>
      <td><button class="reveal-btn" onclick="toggle(14)">▶ Answer</button></td>
    </tr>
    <tr class="answer-row" id="ans-14">
      <td></td>
      <td colspan="8"><strong>Masculine · Dative · Plural</strong> | Antecedent: οἱ νόμοι | "the laws <em>in which</em> / <em>that</em> you believe" — dative with πιστεύετε</td>
    </tr>

    <tr class="question-row" data-id="15">
      <td>15</td>
      <td class="greek">τὰ τέκνα <strong>ὧν</strong> ὁ πατήρ ἐστιν</td>
      <td class="greek">ὧν</td>
      <td><input class="parse-field" type="text" placeholder="gender"></td>
      <td><input class="parse-field" type="text" placeholder="case"></td>
      <td><input class="parse-field" type="text" placeholder="number"></td>
      <td><input class="parse-field wide" type="text" placeholder="antecedent"></td>
      <td><input class="parse-field wide" type="text" placeholder="translation"></td>
      <td><button class="reveal-btn" onclick="toggle(15)">▶ Answer</button></td>
    </tr>
    <tr class="answer-row" id="ans-15">
      <td></td>
      <td colspan="8"><strong>Neuter · Genitive · Plural</strong> | Antecedent: τὰ τέκνα | "the children <em>whose</em> father he is" — genitive of possession</td>
    </tr>

    <tr class="question-row" data-id="16">
      <td>16</td>
      <td class="greek">ὁ τόπος <strong>εἰς ὃν</strong> πορεύεται</td>
      <td class="greek">ὃν</td>
      <td><input class="parse-field" type="text" placeholder="gender"></td>
      <td><input class="parse-field" type="text" placeholder="case"></td>
      <td><input class="parse-field" type="text" placeholder="number"></td>
      <td><input class="parse-field wide" type="text" placeholder="antecedent"></td>
      <td><input class="parse-field wide" type="text" placeholder="translation"></td>
      <td><button class="reveal-btn" onclick="toggle(16)">▶ Answer</button></td>
    </tr>
    <tr class="answer-row" id="ans-16">
      <td></td>
      <td colspan="8"><strong>Masculine · Accusative · Singular</strong> | Antecedent: ὁ τόπος | "the place <em>to which</em> he is going" — object of εἰς</td>
    </tr>

    <tr class="question-row" data-id="17">
      <td>17</td>
      <td class="greek">ἡ ἡμέρα <strong>ἐν ᾗ</strong> ἦλθεν</td>
      <td class="greek">ᾗ</td>
      <td><input class="parse-field" type="text" placeholder="gender"></td>
      <td><input class="parse-field" type="text" placeholder="case"></td>
      <td><input class="parse-field" type="text" placeholder="number"></td>
      <td><input class="parse-field wide" type="text" placeholder="antecedent"></td>
      <td><input class="parse-field wide" type="text" placeholder="translation"></td>
      <td><button class="reveal-btn" onclick="toggle(17)">▶ Answer</button></td>
    </tr>
    <tr class="answer-row" id="ans-17">
      <td></td>
      <td colspan="8"><strong>Feminine · Dative · Singular</strong> | Antecedent: ἡ ἡμέρα | "the day <em>on which</em> he came" — dative of time with ἐν</td>
    </tr>

    <tr class="question-row" data-id="18">
      <td>18</td>
      <td class="greek">οἱ ἄνθρωποι <strong>οὓς</strong> ἀπέστειλεν</td>
      <td class="greek">οὓς</td>
      <td><input class="parse-field" type="text" placeholder="gender"></td>
      <td><input class="parse-field" type="text" placeholder="case"></td>
      <td><input class="parse-field" type="text" placeholder="number"></td>
      <td><input class="parse-field wide" type="text" placeholder="antecedent"></td>
      <td><input class="parse-field wide" type="text" placeholder="translation"></td>
      <td><button class="reveal-btn" onclick="toggle(18)">▶ Answer</button></td>
    </tr>
    <tr class="answer-row" id="ans-18">
      <td></td>
      <td colspan="8"><strong>Masculine · Accusative · Plural</strong> | Antecedent: οἱ ἄνθρωποι | "the men <em>whom</em> he sent" — direct object of ἀπέστειλεν</td>
    </tr>

    <tr class="question-row" data-id="19">
      <td>19</td>
      <td class="greek"><strong>ὃ</strong> ποιεῖς, ποίησον τάχιον</td>
      <td class="greek">ὃ</td>
      <td><input class="parse-field" type="text" placeholder="gender"></td>
      <td><input class="parse-field" type="text" placeholder="case"></td>
      <td><input class="parse-field" type="text" placeholder="number"></td>
      <td><input class="parse-field wide" type="text" placeholder="antecedent"></td>
      <td><input class="parse-field wide" type="text" placeholder="translation"></td>
      <td><button class="reveal-btn" onclick="toggle(19)">▶ Answer</button></td>
    </tr>
    <tr class="answer-row" id="ans-19">
      <td></td>
      <td colspan="8"><strong>Neuter · Accusative · Singular</strong> | Antecedent: none (noun clause) | "<em>What</em> you are doing, do quickly" — noun clause as object; John 13:27</td>
    </tr>

    <tr class="question-row" data-id="20">
      <td>20</td>
      <td class="greek">ἡ ἀλήθεια <strong>ἣν</strong> ἀκούετε</td>
      <td class="greek">ἣν</td>
      <td><input class="parse-field" type="text" placeholder="gender"></td>
      <td><input class="parse-field" type="text" placeholder="case"></td>
      <td><input class="parse-field" type="text" placeholder="number"></td>
      <td><input class="parse-field wide" type="text" placeholder="antecedent"></td>
      <td><input class="parse-field wide" type="text" placeholder="translation"></td>
      <td><button class="reveal-btn" onclick="toggle(20)">▶ Answer</button></td>
    </tr>
    <tr class="answer-row" id="ans-20">
      <td></td>
      <td colspan="8"><strong>Feminine · Accusative · Singular</strong> | Antecedent: ἡ ἀλήθεια | "the truth <em>that</em> you hear" — direct object of ἀκούετε</td>
    </tr>

  </tbody>
</table>

<div class="note">
  <strong>Key Rule:</strong> The relative pronoun agrees with its <strong>antecedent in gender and number</strong>. Its <strong>case</strong> is determined by its function inside the relative clause — not by the case of the antecedent.
</div>

<script>
function toggle(id) {
  const row = document.getElementById('ans-' + id);
  const btn = document.querySelector('[data-id="' + id + '"] button.reveal-btn');
  if (row.classList.contains('visible')) {
    row.classList.remove('visible');
    if (btn) btn.textContent = '▶ Answer';
  } else {
    row.classList.add('visible');
    if (btn) btn.textContent = '▼ Hide';
  }
}
function showAll() {
  document.querySelectorAll('.answer-row').forEach(r => r.classList.add('visible'));
  document.querySelectorAll('button.reveal-btn').forEach(b => b.textContent = '▼ Hide');
}
function hideAll() {
  document.querySelectorAll('.answer-row').forEach(r => r.classList.remove('visible'));
  document.querySelectorAll('button.reveal-btn').forEach(b => b.textContent = '▶ Answer');
}
function clearAll() {
  document.querySelectorAll('input.parse-field').forEach(i => i.value = '');
}
</script>

