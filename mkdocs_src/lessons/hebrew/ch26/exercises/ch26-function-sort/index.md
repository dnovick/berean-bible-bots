# Function Sort

*Chapter 26 — Hiphil Strong*

[Full screen](ch26-function-sort.html){.md-button}  [Markdown](ch26-function-sort.md){.md-button}  [Print (PDF)](ch26-function-sort.pdf){.md-button}

<style>

  body { font-family: Georgia, serif;    color: #222; }
  h1 { font-size: 1.4em; border-bottom: 2px solid #444; padding-bottom: .4em; }
  h2 { font-size: 1.1em; margin-top: 2em; color: #444; }
  .subtitle { color: #666; font-style: italic; margin-top: -.3em; }
  table { border-collapse: collapse;  margin: 1em 0; }
  th { background: #2a4a6e; color: #fff; padding: .5em .7em; text-align: left; font-size: .85em; }
  td { border: 1px solid #ccc; padding: .4em .6em; font-size: .88em; vertical-align: top; }
  tr:nth-child(even) td { background: #f7f7f7; }
  .heb { font-size: 1.25em; direction: rtl; unicode-bidi: embed; }
  select.parse-field { font-size: .88em; padding: 2px 4px; border: 1px solid #aaa; border-radius: 3px; min-width: 70px; }
  input.parse-field { width: 100%; box-sizing: border-box; font-size: .88em; padding: 3px 5px; border: 1px solid #aaa; border-radius: 3px; }
  .answer-row td { background: #f0faf0 !important; color: #2a6e2a; font-size: .85em; }
  .answer-row { display: none; }
  button.reveal-btn { font-size: .78em; padding: 2px 7px; cursor: pointer; border: 1px solid #888; border-radius: 3px; background: #fff; white-space: nowrap; }
  .controls { margin: 1em 0; display: flex; gap: .6em; flex-wrap: wrap; }
  .controls button { padding: .4em .9em; font-size: .9em; cursor: pointer; border: 1px solid #555; border-radius: 4px; background: #f0f0f0; }
  .controls button:hover { background: #ddd; }
  .tip { background: #fffbe6; border-left: 4px solid #d4a017; padding: .6em 1em; margin: 1em 0; font-size: .88em; }
  .ref-table td, .ref-table th { font-size: .85em; }
  .discussion { background: #f0f4ff; border-left: 4px solid #2a4a6e; padding: .6em 1em; margin: 1em 0; font-size: .88em; }
  ol.disc { margin: .4em 0 0 1.2em; padding: 0; }
  ol.disc li { margin-bottom: .4em; }
  @media print {
    button, .controls { display: none !important; }
    select.parse-field { font-size: .88em; padding: 2px 4px; border: 1px solid #aaa; border-radius: 3px; min-width: 70px; }
  input.parse-field { border: none; border-bottom: 1px solid #000; background: transparent; }
    .answer-row { display: table-row !important; }
  }

</style>

<h1>Chapter 26 — Semantic Function Sorting</h1>
<p class="subtitle">BBH Chapter 26 · Hiphil Strong Verbs</p>

<p>Classify each Hiphil verb as <strong>C</strong> (Causative), <strong>F</strong> (Factitive), <strong>D</strong> (Declarative), <strong>SA</strong> (Simple Action), or <strong>DN</strong> (Denominative). Type your answer in the Function column, then click <strong>▶ Answer</strong> to check.</p>

<div style="overflow-x:auto;max-width:100%;"><table class="ref-table">
  <tr>
    <th>Label</th><th>Function</th><th>Key diagnostic question</th>
  </tr>
  <tr><td><strong>C</strong></td><td>Causative</td><td>Does the subject <em>cause</em> someone/something else to do or experience the action?</td></tr>
  <tr><td><strong>F</strong></td><td>Factitive</td><td>Does the subject cause an object to <em>be in</em> a certain state? (From a stative root.)</td></tr>
  <tr><td><strong>D</strong></td><td>Declarative</td><td>Does the subject <em>declare or treat</em> something as being in a state?</td></tr>
  <tr><td><strong>SA</strong></td><td>Simple Action</td><td>Is the Hiphil the standard form of the verb with no Qal counterpart in normal usage?</td></tr>
  <tr><td><strong>DN</strong></td><td>Denominative</td><td>Is the Hiphil derived from a <em>noun</em>, performing an action related to that noun? <em>(not in BBH)</em></td></tr>
</table></div>

<div class="tip">
  <strong>Tip:</strong> Motion verb (go → bring) → <strong>Causative</strong>.
  Stative verb (be heavy → make heavy) → <strong>Factitive</strong>.
  Legal / evaluative declaration → <strong>Declarative</strong>.
  No common Qal counterpart → <strong>Simple Action</strong>.
  Hiphil built from a noun → <strong>Denominative</strong>.
</div>

<div class="controls">
  <button onclick="showAll()">Show All Answers</button>
  <button onclick="hideAll()">Hide All Answers</button>
  <button onclick="clearAll()">Clear All Inputs</button>
</div>

<div style="overflow-x:auto;max-width:100%;"><table>
  <tr>
    <th>#</th><th>Hebrew Form</th><th>Conjugation</th><th>Ref</th><th>Contextual Gloss</th><th>Function</th><th></th>
  </tr>

  <tr>
    <td>1</td>
    <td><span class="heb">וַיָּבֵא</span></td>
    <td>Wayyiqtol 3ms</td>
    <td>Gen 2:19</td>
    <td>"he brought them to the man"</td>
    <td><select class="parse-field" id="f1"><option value="">—</option><option>C</option><option>F</option><option>D</option><option>SA</option><option>DN</option></select></td>
    <td><button class="reveal-btn" onclick="toggle('r1')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r1">
    <td colspan="7"><strong>C — Causative</strong> · Root: <span class="heb">בּוֹא</span> (Qal: to come/go) · God caused the animals to come to Adam</td>
  </tr>

  <tr>
    <td>2</td>
    <td><span class="heb">וַתּוֹצֵא</span></td>
    <td>Wayyiqtol 3fs</td>
    <td>Gen 1:12</td>
    <td>"the earth brought forth vegetation"</td>
    <td><select class="parse-field" id="f2"><option value="">—</option><option>C</option><option>F</option><option>D</option><option>SA</option><option>DN</option></select></td>
    <td><button class="reveal-btn" onclick="toggle('r2')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r2">
    <td colspan="7"><strong>C — Causative</strong> · Root: <span class="heb">יָצָא</span> (Qal: to go out) · The earth caused vegetation to come out</td>
  </tr>

  <tr>
    <td>3</td>
    <td><span class="heb">וַיָּשֶׁב</span></td>
    <td>Wayyiqtol 3ms</td>
    <td>Gen 14:16</td>
    <td>"he brought back his brother Lot"</td>
    <td><select class="parse-field" id="f3"><option value="">—</option><option>C</option><option>F</option><option>D</option><option>SA</option><option>DN</option></select></td>
    <td><button class="reveal-btn" onclick="toggle('r3')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r3">
    <td colspan="7"><strong>C — Causative</strong> · Root: <span class="heb">שׁוּב</span> (Qal: to return) · Abraham caused Lot to return</td>
  </tr>

  <tr>
    <td>4</td>
    <td><span class="heb">הִשְׁקָה</span></td>
    <td>Perfect 3ms</td>
    <td>Gen 2:6</td>
    <td>"a mist watered the whole surface"</td>
    <td><select class="parse-field" id="f4"><option value="">—</option><option>C</option><option>F</option><option>D</option><option>SA</option><option>DN</option></select></td>
    <td><button class="reveal-btn" onclick="toggle('r4')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r4">
    <td colspan="7"><strong>C — Causative</strong> · Root: <span class="heb">שָׁקָה</span> (Qal: to drink) · The mist caused the ground to receive water</td>
  </tr>

  <tr>
    <td>5</td>
    <td><span class="heb">וַיּוֹלֶד</span></td>
    <td>Wayyiqtol 3ms</td>
    <td>Gen 5:3</td>
    <td>"Adam fathered a son"</td>
    <td><select class="parse-field" id="f5"><option value="">—</option><option>C</option><option>F</option><option>D</option><option>SA</option><option>DN</option></select></td>
    <td><button class="reveal-btn" onclick="toggle('r5')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r5">
    <td colspan="7"><strong>C — Causative</strong> · Root: <span class="heb">יָלַד</span> (Qal: to give birth) · Adam caused a son to be born</td>
  </tr>

  <tr>
    <td>6</td>
    <td><span class="heb">הַעֲלֵה</span></td>
    <td>Imperative 2ms</td>
    <td>Gen 22:2</td>
    <td>"offer him as a burnt offering"</td>
    <td><select class="parse-field" id="f6"><option value="">—</option><option>C</option><option>F</option><option>D</option><option>SA</option><option>DN</option></select></td>
    <td><button class="reveal-btn" onclick="toggle('r6')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r6">
    <td colspan="7"><strong>C — Causative</strong> · Root: <span class="heb">עָלָה</span> (Qal: to go up) · Cause Isaac to go up as an offering</td>
  </tr>

  <tr>
    <td>7</td>
    <td><span class="heb">וַתֹּרֶד</span></td>
    <td>Wayyiqtol 3fs</td>
    <td>Gen 24:18</td>
    <td>"she lowered her jar to give him a drink"</td>
    <td><select class="parse-field" id="f7"><option value="">—</option><option>C</option><option>F</option><option>D</option><option>SA</option><option>DN</option></select></td>
    <td><button class="reveal-btn" onclick="toggle('r7')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r7">
    <td colspan="7"><strong>C — Causative</strong> · Root: <span class="heb">יָרַד</span> (Qal: to go down) · Rebekah caused the jar to go down</td>
  </tr>

  <tr>
    <td>8</td>
    <td><span class="heb">וַיָּסַר</span></td>
    <td>Wayyiqtol 3ms</td>
    <td>Gen 30:35</td>
    <td>"he removed the streaked goats"</td>
    <td><select class="parse-field" id="f8"><option value="">—</option><option>C</option><option>F</option><option>D</option><option>SA</option><option>DN</option></select></td>
    <td><button class="reveal-btn" onclick="toggle('r8')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r8">
    <td colspan="7"><strong>C — Causative</strong> · Root: <span class="heb">סוּר</span> (Qal: to turn aside, depart) · Caused the goats to depart/move away</td>
  </tr>

  <tr>
    <td>9</td>
    <td><span class="heb">וַיַּגֵּד</span></td>
    <td>Wayyiqtol 3ms</td>
    <td>Gen 9:22</td>
    <td>"Ham told his two brothers"</td>
    <td><select class="parse-field" id="f9"><option value="">—</option><option>C</option><option>F</option><option>D</option><option>SA</option><option>DN</option></select></td>
    <td><button class="reveal-btn" onclick="toggle('r9')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r9">
    <td colspan="7"><strong>SA — Simple Action</strong> · Root: <span class="heb">נָגַד</span> (rare Qal) · Hiphil = standard form; to tell/report is the basic meaning</td>
  </tr>

  <tr>
    <td>10</td>
    <td><span class="heb">הִגִּיד</span></td>
    <td>Weqatal 3ms</td>
    <td>Gen 3:11</td>
    <td>"who told you that you were naked?"</td>
    <td><select class="parse-field" id="f10"><option value="">—</option><option>C</option><option>F</option><option>D</option><option>SA</option><option>DN</option></select></td>
    <td><button class="reveal-btn" onclick="toggle('r10')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r10">
    <td colspan="7"><strong>SA — Simple Action</strong> · Root: <span class="heb">נָגַד</span> · Same root as #9; Hiphil is the operative form</td>
  </tr>

  <tr>
    <td>11</td>
    <td><span class="heb">וַתַּשְׁלֵךְ</span></td>
    <td>Wayyiqtol 3fs</td>
    <td>Gen 21:15</td>
    <td>"she threw the child under one of the bushes"</td>
    <td><select class="parse-field" id="f11"><option value="">—</option><option>C</option><option>F</option><option>D</option><option>SA</option><option>DN</option></select></td>
    <td><button class="reveal-btn" onclick="toggle('r11')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r11">
    <td colspan="7"><strong>SA — Simple Action</strong> · Root: <span class="heb">שָׁלַךְ</span> (no common Qal) · To throw/cast; Hiphil is the primary form</td>
  </tr>

  <tr>
    <td>12</td>
    <td><span class="heb">הִזְכַּרְתָּ</span></td>
    <td>Perfect 2ms</td>
    <td>Gen 40:14</td>
    <td>"mention me to Pharaoh"</td>
    <td><select class="parse-field" id="f12"><option value="">—</option><option>C</option><option>F</option><option>D</option><option>SA</option><option>DN</option></select></td>
    <td><button class="reveal-btn" onclick="toggle('r12')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r12">
    <td colspan="7"><strong>C — Causative</strong> · Root: <span class="heb">זָכַר</span> (Qal: to remember) · Cause Pharaoh to remember; bring to his mind</td>
  </tr>

  <tr>
    <td>13</td>
    <td><span class="heb">מַזְכִּיר</span></td>
    <td>Participle ms</td>
    <td>Gen 41:9</td>
    <td>"I am bringing my faults to mind"</td>
    <td><select class="parse-field" id="f13"><option value="">—</option><option>C</option><option>F</option><option>D</option><option>SA</option><option>DN</option></select></td>
    <td><button class="reveal-btn" onclick="toggle('r13')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r13">
    <td colspan="7"><strong>C — Causative</strong> · Root: <span class="heb">זָכַר</span> · Causing something to be remembered; same Causative pattern</td>
  </tr>

  <tr>
    <td>14</td>
    <td><span class="heb">הָמִית</span></td>
    <td>Inf. Construct</td>
    <td>Gen 18:25</td>
    <td>"Far be it from you to put the righteous to death"</td>
    <td><select class="parse-field" id="f14"><option value="">—</option><option>C</option><option>F</option><option>D</option><option>SA</option><option>DN</option></select></td>
    <td><button class="reveal-btn" onclick="toggle('r14')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r14">
    <td colspan="7"><strong>C — Causative</strong> · Root: <span class="heb">מוּת</span> (Qal: to die) · To cause to die = put to death</td>
  </tr>

  <tr>
    <td>15</td>
    <td><span class="heb">הַכּוֹת</span></td>
    <td>Inf. Construct</td>
    <td>Gen 4:15</td>
    <td>"lest anyone who found him strike him"</td>
    <td><select class="parse-field" id="f15"><option value="">—</option><option>C</option><option>F</option><option>D</option><option>SA</option><option>DN</option></select></td>
    <td><button class="reveal-btn" onclick="toggle('r15')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r15">
    <td colspan="7"><strong>SA — Simple Action</strong> · Root: <span class="heb">נָכָה</span> (no Qal) · To strike; Hiphil is the primary and standard form</td>
  </tr>

  <tr>
    <td>16</td>
    <td><span class="heb">הִשְׁמַדְתִּי</span></td>
    <td>Perfect 1cs</td>
    <td>Lev 26:30</td>
    <td>"I will destroy your high places"</td>
    <td><select class="parse-field" id="f16"><option value="">—</option><option>C</option><option>F</option><option>D</option><option>SA</option><option>DN</option></select></td>
    <td><button class="reveal-btn" onclick="toggle('r16')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r16">
    <td colspan="7"><strong>SA — Simple Action</strong> · Root: <span class="heb">שָׁמַד</span> (no Qal) · To destroy; the Niphal of this root means "to be destroyed"</td>
  </tr>

  <tr>
    <td>17</td>
    <td><span class="heb">תַּשְׁמִידוּ</span></td>
    <td>Imperfect 2mp</td>
    <td>Num 33:52</td>
    <td>"you shall demolish all their figured stones"</td>
    <td><select class="parse-field" id="f17"><option value="">—</option><option>C</option><option>F</option><option>D</option><option>SA</option><option>DN</option></select></td>
    <td><button class="reveal-btn" onclick="toggle('r17')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r17">
    <td colspan="7"><strong>SA — Simple Action</strong> · Root: <span class="heb">שָׁמַד</span> · Same root as #16; conquest context</td>
  </tr>

  <tr>
    <td>18</td>
    <td><span class="heb">וַיַּכְבֵּד</span></td>
    <td>Wayyiqtol 3ms</td>
    <td>Exo 8:32</td>
    <td>"Pharaoh hardened his heart this time also"</td>
    <td><select class="parse-field" id="f18"><option value="">—</option><option>C</option><option>F</option><option>D</option><option>SA</option><option>DN</option></select></td>
    <td><button class="reveal-btn" onclick="toggle('r18')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r18">
    <td colspan="7"><strong>F — Factitive</strong> · Root: <span class="heb">כָּבֵד</span> (Qal: to be heavy/honored) · Pharaoh caused his heart to be in a state of heaviness/stubbornness</td>
  </tr>

  <tr>
    <td>19</td>
    <td><span class="heb">וְהַכְבֵּד</span></td>
    <td>Inf. Absolute</td>
    <td>Exo 8:15</td>
    <td>"he made his heart stubborn" (intensified)</td>
    <td><select class="parse-field" id="f19"><option value="">—</option><option>C</option><option>F</option><option>D</option><option>SA</option><option>DN</option></select></td>
    <td><button class="reveal-btn" onclick="toggle('r19')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r19">
    <td colspan="7"><strong>F — Factitive</strong> · Root: <span class="heb">כָּבֵד</span> · Same Factitive force; Inf. Absolute here intensifies the action (made it truly heavy)</td>
  </tr>

  <tr>
    <td>20</td>
    <td><span class="heb">וַתַּגְדֵּל</span></td>
    <td>Wayyiqtol 2ms</td>
    <td>Gen 19:19</td>
    <td>"you have shown great kindness to me"</td>
    <td><select class="parse-field" id="f20"><option value="">—</option><option>C</option><option>F</option><option>D</option><option>SA</option><option>DN</option></select></td>
    <td><button class="reveal-btn" onclick="toggle('r20')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r20">
    <td colspan="7"><strong>F — Factitive</strong> · Root: <span class="heb">גָּדַל</span> (Qal: to be great) · Caused your kindness to be great; to magnify or make great</td>
  </tr>

  <tr>
    <td>21</td>
    <td><span class="heb">הִרְשִׁיעוּ</span></td>
    <td>Perfect 3cp</td>
    <td>Deu 25:1</td>
    <td>"they shall acquit the innocent and condemn the guilty"</td>
    <td><select class="parse-field" id="f21"><option value="">—</option><option>C</option><option>F</option><option>D</option><option>SA</option><option>DN</option></select></td>
    <td><button class="reveal-btn" onclick="toggle('r21')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r21">
    <td colspan="7"><strong>D — Declarative</strong> · Root: <span class="heb">רָשָׁע</span> (Qal: to be wicked) · Legal verdict: the judges declare someone to be in the state of guilt (not <em>making</em> them wicked)</td>
  </tr>

  <tr>
    <td>22</td>
    <td><span class="heb">יַרְשִׁיעֻ</span></td>
    <td>Imperfect 3mp</td>
    <td>Exo 22:8</td>
    <td>"the judges shall declare him guilty"</td>
    <td><select class="parse-field" id="f22"><option value="">—</option><option>C</option><option>F</option><option>D</option><option>SA</option><option>DN</option></select></td>
    <td><button class="reveal-btn" onclick="toggle('r22')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r22">
    <td colspan="7"><strong>D — Declarative</strong> · Root: <span class="heb">רָשָׁע</span> · Same root and function as #21; a judicial pronouncement</td>
  </tr>

  <tr>
    <td>23</td>
    <td><span class="heb">וַיַּעַל</span></td>
    <td>Wayyiqtol 3ms</td>
    <td>Gen 8:20</td>
    <td>"Noah offered burnt offerings on the altar"</td>
    <td><select class="parse-field" id="f23"><option value="">—</option><option>C</option><option>F</option><option>D</option><option>SA</option><option>DN</option></select></td>
    <td><button class="reveal-btn" onclick="toggle('r23')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r23">
    <td colspan="7"><strong>C — Causative</strong> · Root: <span class="heb">עָלָה</span> (Qal: to go up) · Noah caused the offerings to go up (on the altar)</td>
  </tr>

  <tr>
    <td>24</td>
    <td><span class="heb">הָמִית</span></td>
    <td>Inf. Construct</td>
    <td>Gen 37:18</td>
    <td>"they conspired against him to kill him"</td>
    <td><select class="parse-field" id="f24"><option value="">—</option><option>C</option><option>F</option><option>D</option><option>SA</option><option>DN</option></select></td>
    <td><button class="reveal-btn" onclick="toggle('r24')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r24">
    <td colspan="7"><strong>C — Causative</strong> · Root: <span class="heb">מוּת</span> (Qal: to die) · To cause to die = kill; same form as #14, different context</td>
  </tr>

  <tr>
    <td>25</td>
    <td><span class="heb">מַמְטִיר</span></td>
    <td>Participle ms</td>
    <td>Gen 7:4</td>
    <td>"I am about to send rain on the earth"</td>
    <td><select class="parse-field" id="f25"><option value="">—</option><option>C</option><option>F</option><option>D</option><option>SA</option><option>DN</option></select></td>
    <td><button class="reveal-btn" onclick="toggle('r25')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r25">
    <td colspan="7"><strong>DN — Denominative</strong> · Root: <span class="heb">מָטַר</span> · From noun <span class="heb">מָטָר</span> ("rain") — the Hiphil performs the action of rain; to send/cause rain</td>
  </tr>

  <tr>
    <td>26</td>
    <td><span class="heb">וַיַּשְׁכֵּם</span></td>
    <td>Wayyiqtol 3ms</td>
    <td>Gen 22:3</td>
    <td>"Abraham rose early in the morning"</td>
    <td><select class="parse-field" id="f26"><option value="">—</option><option>C</option><option>F</option><option>D</option><option>SA</option><option>DN</option></select></td>
    <td><button class="reveal-btn" onclick="toggle('r26')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r26">
    <td colspan="7"><strong>DN — Denominative</strong> · Root: <span class="heb">שָׁכַם</span> · From noun <span class="heb">שְׁכֶם</span> ("shoulder") — to shoulder up early = to rise early / start at dawn</td>
  </tr>

  <tr>
    <td>27</td>
    <td><span class="heb">הַאְזִינוּ</span></td>
    <td>Imperative 2mp</td>
    <td>Deu 32:1</td>
    <td>"give ear, O heavens, and I will speak"</td>
    <td><select class="parse-field" id="f27"><option value="">—</option><option>C</option><option>F</option><option>D</option><option>SA</option><option>DN</option></select></td>
    <td><button class="reveal-btn" onclick="toggle('r27')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r27">
    <td colspan="7"><strong>DN — Denominative</strong> · Root: <span class="heb">אָזַן</span> · From noun <span class="heb">אֹזֶן</span> ("ear") — to ear = to give ear / listen attentively</td>
  </tr>

</table></div>

<h2>Discussion Questions</h2>
<div class="discussion">
  <ol class="disc">
    <li>Items 18–19 both come from <span class="heb">כָּבֵד</span> (Exo 8:32, 8:15). The root means "to be heavy." How does the Hiphil meaning connect to that? Is this Factitive or Causative — and why?</li>
    <li>Items 21–22 both use <span class="heb">רָשָׁע</span> and both classify as Declarative. Compare Deu 25:1 (a judicial verdict) with Exo 22:8 (a court decision). What do they have in common that makes both Declarative rather than Factitive?</li>
    <li>Items 12–13 (<span class="heb">זָכַר</span>, "to remember") might seem like Simple Action, but they are classified as Causative. What is the Causative reading? Does it make the translation different?</li>
    <li>Items 25–27 are Denominative. For each one, identify the underlying noun. How does knowing the noun make the Hiphil meaning immediately transparent?</li>
  </ol>
</div>

<script>
function toggle(id) {
  const row = document.getElementById(id);
  const btn = row.previousElementSibling.querySelector('.reveal-btn');
  if (row.style.display === 'table-row') {
    row.style.display = 'none';
    btn.textContent = '▶ Answer';
  } else {
    row.style.display = 'table-row';
    btn.textContent = '▼ Hide';
  }
}
function showAll() {
  document.querySelectorAll('.answer-row').forEach(r => r.style.display = 'table-row');
  document.querySelectorAll('.reveal-btn').forEach(b => b.textContent = '▼ Hide');
}
function hideAll() {
  document.querySelectorAll('.answer-row').forEach(r => r.style.display = 'none');
  document.querySelectorAll('.reveal-btn').forEach(b => b.textContent = '▶ Answer');
}
function clearAll() {
  document.querySelectorAll('.parse-field').forEach(i => i.value = '');
}
</script>

