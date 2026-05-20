# Function Sort

*Chapter 30 — Piel Strong*

[Full screen](ch30-function-sort.html){.md-button}  [Markdown](ch30-function-sort.md){.md-button}  [Print (PDF)](ch30-function-sort.pdf){.md-button}

<style>

  body { font-family: Georgia, serif;    color: #222; }
  h1 { font-size: 1.4em; border-bottom: 2px solid #444; padding-bottom: .4em; }
  h2 { font-size: 1.1em; margin-top: 2em; color: #444; }
  .subtitle { color: #666; font-style: italic; margin-top: -.3em; }
  table { border-collapse: collapse; width: 100%; margin: 1em 0; }
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

<h1>Chapter 30 — Piel Semantic Function Sorting</h1>
<p class="subtitle">BBH Chapter 30 · Piel Strong Verbs</p>

<p>Classify each Piel verb as <strong>I</strong> (Intensive), <strong>F</strong> (Factitive), <strong>D</strong> (Declarative), <strong>SA</strong> (Simple Action), or <strong>DN</strong> (Denominative). Type your answer in the Function column, then click <strong>▶ Answer</strong> to check.</p>

<table class="ref-table">
  <tr><th>Code</th><th>Function</th><th>Key diagnostic question</th></tr>
  <tr><td><strong>I</strong></td><td>Intensive</td><td>Does the subject do the Qal action more forcefully, completely, or repeatedly?</td></tr>
  <tr><td><strong>F</strong></td><td>Factitive</td><td>Does the subject cause an object to <em>enter</em> a state? (Stative Qal root.)</td></tr>
  <tr><td><strong>D</strong></td><td>Declarative</td><td>Does the subject <em>pronounce or treat</em> something as being in a state?</td></tr>
  <tr><td><strong>SA</strong></td><td>Simple Action</td><td>Is the Piel the standard form with no common Qal equivalent?</td></tr>
  <tr><td><strong>DN</strong></td><td>Denominative</td><td>Is the Piel verb built on a <em>noun</em> and performs that noun's characteristic action?</td></tr>
</table>

<div class="tip">
  <strong>Tip:</strong> Stative root (to be X) + Piel = Piel <em>causes</em> X → <strong>Factitive</strong>.
  Active root (to do X) + Piel = Piel does X more intensely → <strong>Intensive</strong>.
  Legal / evaluative pronouncement → <strong>Declarative</strong>.
  No common Qal → <strong>Simple Action</strong>.
  Verb built on a noun → <strong>Denominative</strong>.
</div>

<div class="controls">
  <button onclick="showAll()">Show All Answers</button>
  <button onclick="hideAll()">Hide All Answers</button>
  <button onclick="clearAll()">Clear All Inputs</button>
</div>

<table>
  <tr>
    <th>#</th><th>Hebrew Form</th><th>Conjugation</th><th>Root</th><th>Ref</th><th>Contextual Gloss</th><th>Function</th><th></th>
  </tr>

  <tr>
    <td>1</td>
    <td><span class="heb">יְבָרֶךְ</span></td>
    <td>Wayyiqtol 3ms</td>
    <td><span class="heb">בָּרַךְ</span></td>
    <td>Gen 1:22</td>
    <td>"God blessed them"</td>
    <td><select class="parse-field" id="f1"><option value="">—</option><option>I</option><option>F</option><option>D</option><option>SA</option><option>DN</option></select></td>
    <td><button class="reveal-btn" onclick="toggle('r1')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r1">
    <td colspan="8"><strong>SA — Simple Action</strong> · Root: <span class="heb">בָּרַךְ</span> (Qal: to kneel/bless — rare) · Blessing is the Piel's primary function; no intensification of a common Qal is intended</td>
  </tr>

  <tr>
    <td>2</td>
    <td><span class="heb">יְקַדֵּשׁ</span></td>
    <td>Wayyiqtol 3ms</td>
    <td><span class="heb">קָדַשׁ</span></td>
    <td>Gen 2:3</td>
    <td>"he set it apart as holy"</td>
    <td><select class="parse-field" id="f2"><option value="">—</option><option>I</option><option>F</option><option>D</option><option>SA</option><option>DN</option></select></td>
    <td><button class="reveal-btn" onclick="toggle('r2')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r2">
    <td colspan="8"><strong>F — Factitive</strong> · Root: <span class="heb">קָדַשׁ</span> (Qal: to be holy — stative) · God caused the Sabbath day to enter the state of holiness</td>
  </tr>

  <tr>
    <td>3</td>
    <td><span class="heb">יְכַל</span></td>
    <td>Wayyiqtol 3ms</td>
    <td><span class="heb">כָּלָה</span></td>
    <td>Gen 2:2</td>
    <td>"he finished all his work"</td>
    <td><select class="parse-field" id="f3"><option value="">—</option><option>I</option><option>F</option><option>D</option><option>SA</option><option>DN</option></select></td>
    <td><button class="reveal-btn" onclick="toggle('r3')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r3">
    <td colspan="8"><strong>F — Factitive</strong> · Root: <span class="heb">כָּלָה</span> (Qal: to be complete, finished — stative) · God caused his work to reach completion; Piel = bring something to its finished state</td>
  </tr>

  <tr>
    <td>4</td>
    <td><span class="heb">שַׁחֵת</span></td>
    <td>Inf. Construct</td>
    <td><span class="heb">שָׁחַת</span></td>
    <td>Gen 6:17</td>
    <td>"to destroy all flesh"</td>
    <td><select class="parse-field" id="f4"><option value="">—</option><option>I</option><option>F</option><option>D</option><option>SA</option><option>DN</option></select></td>
    <td><button class="reveal-btn" onclick="toggle('r4')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r4">
    <td colspan="8"><strong>I — Intensive</strong> · Root: <span class="heb">שָׁחַת</span> (Qal: to ruin, be corrupt) · Piel = destroy utterly; not mere ruin but total annihilation — the intensification is cosmic in scope</td>
  </tr>

  <tr>
    <td>5</td>
    <td><span class="heb">יְצַו</span></td>
    <td>Wayyiqtol 3ms</td>
    <td><span class="heb">צָוָה</span></td>
    <td>Gen 2:16</td>
    <td>"the LORD God commanded the man"</td>
    <td><select class="parse-field" id="f5"><option value="">—</option><option>I</option><option>F</option><option>D</option><option>SA</option><option>DN</option></select></td>
    <td><button class="reveal-btn" onclick="toggle('r5')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r5">
    <td colspan="8"><strong>SA — Simple Action</strong> · Root: <span class="heb">צָוָה</span> (no common Qal) · Commanding is the Piel's own basic function; there is no Qal "command" to intensify</td>
  </tr>

  <tr>
    <td>6</td>
    <td><span class="heb">יְגָרֶשׁ</span></td>
    <td>Wayyiqtol 3ms</td>
    <td><span class="heb">גָּרַשׁ</span></td>
    <td>Gen 3:24</td>
    <td>"he drove out the man"</td>
    <td><select class="parse-field" id="f6"><option value="">—</option><option>I</option><option>F</option><option>D</option><option>SA</option><option>DN</option></select></td>
    <td><button class="reveal-btn" onclick="toggle('r6')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r6">
    <td colspan="8"><strong>I — Intensive</strong> · Root: <span class="heb">גָּרַשׁ</span> (Qal: to drive out) · Piel = forcible, emphatic expulsion; Adam is driven out completely and definitively</td>
  </tr>

  <tr>
    <td>7</td>
    <td><span class="heb">חַיּוֹת</span></td>
    <td>Inf. Construct</td>
    <td><span class="heb">חָיָה</span></td>
    <td>Gen 7:3</td>
    <td>"to keep offspring alive on the earth"</td>
    <td><select class="parse-field" id="f7"><option value="">—</option><option>I</option><option>F</option><option>D</option><option>SA</option><option>DN</option></select></td>
    <td><button class="reveal-btn" onclick="toggle('r7')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r7">
    <td colspan="8"><strong>F — Factitive</strong> · Root: <span class="heb">חָיָה</span> (Qal: to live, be alive — stative) · Piel = cause to be alive = preserve alive; God causes Noah to keep seed in the state of living</td>
  </tr>

  <tr>
    <td>8</td>
    <td><span class="heb">יְשַׁלַּח</span></td>
    <td>Wayyiqtol 3ms</td>
    <td><span class="heb">שָׁלַח</span></td>
    <td>Gen 8:7</td>
    <td>"he sent out a raven"</td>
    <td><select class="parse-field" id="f8"><option value="">—</option><option>I</option><option>F</option><option>D</option><option>SA</option><option>DN</option></select></td>
    <td><button class="reveal-btn" onclick="toggle('r8')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r8">
    <td colspan="8"><strong>I — Intensive</strong> · Root: <span class="heb">שָׁלַח</span> (Qal: to send) · Piel = send away / release completely; the bird is let go on its own; thorough dispatching</td>
  </tr>

  <tr>
    <td>9</td>
    <td><span class="heb">יְכַסּוּ</span></td>
    <td>Wayyiqtol 3mp</td>
    <td><span class="heb">כָּסָה</span></td>
    <td>Gen 9:23</td>
    <td>"they covered their father's nakedness"</td>
    <td><select class="parse-field" id="f9"><option value="">—</option><option>I</option><option>F</option><option>D</option><option>SA</option><option>DN</option></select></td>
    <td><button class="reveal-btn" onclick="toggle('r9')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r9">
    <td colspan="8"><strong>I — Intensive</strong> · Root: <span class="heb">כָּסָה</span> (Qal: to cover) · Piel = cover thoroughly / completely conceal; the act of covering is emphatic and complete</td>
  </tr>

  <tr>
    <td>10</td>
    <td><span class="heb">יְדַבֵּר</span></td>
    <td>Wayyiqtol 3ms</td>
    <td><span class="heb">דָּבַר</span></td>
    <td>Gen 8:15</td>
    <td>"God spoke to Noah"</td>
    <td><select class="parse-field" id="f10"><option value="">—</option><option>I</option><option>F</option><option>D</option><option>SA</option><option>DN</option></select></td>
    <td><button class="reveal-btn" onclick="toggle('r10')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r10">
    <td colspan="8"><strong>SA — Simple Action</strong> · Root: <span class="heb">דָּבַר</span> (Qal: to speak — exceedingly rare) · Speaking is the Piel's standard meaning; the Qal is functionally absent; no intensification is in view</td>
  </tr>

  <tr>
    <td>11</td>
    <td><span class="heb">יְשָׁרֶת</span></td>
    <td>Wayyiqtol 3ms</td>
    <td><span class="heb">שָׁרַת</span></td>
    <td>Gen 39:4</td>
    <td>"he served him / ministered to him"</td>
    <td><select class="parse-field" id="f11"><option value="">—</option><option>I</option><option>F</option><option>D</option><option>SA</option><option>DN</option></select></td>
    <td><button class="reveal-btn" onclick="toggle('r11')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r11">
    <td colspan="8"><strong>SA — Simple Action</strong> · Root: <span class="heb">שָׁרַת</span> (no common Qal) · Service/ministry is the Piel's own function; no Qal counterpart in general use</td>
  </tr>

  <tr>
    <td>12</td>
    <td><span class="heb">אֲגַדְּלָה</span></td>
    <td>Yiqtol 1cs</td>
    <td><span class="heb">גָּדַל</span></td>
    <td>Gen 12:2</td>
    <td>"I will make your name great"</td>
    <td><select class="parse-field" id="f12"><option value="">—</option><option>I</option><option>F</option><option>D</option><option>SA</option><option>DN</option></select></td>
    <td><button class="reveal-btn" onclick="toggle('r12')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r12">
    <td colspan="8"><strong>F — Factitive</strong> · Root: <span class="heb">גָּדַל</span> (Qal: to be great — stative) · God will cause Abram's name to enter the state of greatness = make great, magnify</td>
  </tr>

  <tr>
    <td>13</td>
    <td><span class="heb">מְקַלֵּל</span></td>
    <td>Participle ms</td>
    <td><span class="heb">קָלַל</span></td>
    <td>Gen 12:3</td>
    <td>"the one who treats you lightly / curses you"</td>
    <td><select class="parse-field" id="f13"><option value="">—</option><option>I</option><option>F</option><option>D</option><option>SA</option><option>DN</option></select></td>
    <td><button class="reveal-btn" onclick="toggle('r13')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r13">
    <td colspan="8"><strong>D — Declarative</strong> · Root: <span class="heb">קָלַל</span> (Qal: to be small, light, of little account — stative) · Piel Declarative = pronounce someone accursed / treat as contemptible; the subject makes a verbal declaration of the other's diminishment</td>
  </tr>

  <tr>
    <td>14</td>
    <td><span class="heb">יְנַגַּע</span></td>
    <td>Wayyiqtol 3ms</td>
    <td><span class="heb">נָגַע</span></td>
    <td>Gen 12:17</td>
    <td>"the LORD afflicted Pharaoh with plagues"</td>
    <td><select class="parse-field" id="f14"><option value="">—</option><option>I</option><option>F</option><option>D</option><option>SA</option><option>DN</option></select></td>
    <td><button class="reveal-btn" onclick="toggle('r14')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r14">
    <td colspan="8"><strong>I — Intensive</strong> · Root: <span class="heb">נָגַע</span> (Qal: to touch, strike) · Piel = strike repeatedly, afflict with plague; not a single touch but sustained divine striking</td>
  </tr>

  <tr>
    <td>15</td>
    <td><span class="heb">וְקִדַּשְׁתָּ</span></td>
    <td>Weqatal 2ms</td>
    <td><span class="heb">קָדַשׁ</span></td>
    <td>Exo 19:10</td>
    <td>"you shall consecrate them today and tomorrow"</td>
    <td><select class="parse-field" id="f15"><option value="">—</option><option>I</option><option>F</option><option>D</option><option>SA</option><option>DN</option></select></td>
    <td><button class="reveal-btn" onclick="toggle('r15')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r15">
    <td colspan="8"><strong>F — Factitive</strong> · Root: <span class="heb">קָדַשׁ</span> (Qal: to be holy — stative) · Moses will cause the people to enter a state of ritual holiness; same Factitive function as #2</td>
  </tr>

  <tr>
    <td>16</td>
    <td><span class="heb">וְכִבְּסוּ</span></td>
    <td>Weqatal 3cp</td>
    <td><span class="heb">כָּבַס</span></td>
    <td>Exo 19:10</td>
    <td>"they shall wash their garments"</td>
    <td><select class="parse-field" id="f16"><option value="">—</option><option>I</option><option>F</option><option>D</option><option>SA</option><option>DN</option></select></td>
    <td><button class="reveal-btn" onclick="toggle('r16')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r16">
    <td colspan="8"><strong>I — Intensive</strong> · Root: <span class="heb">כָּבַס</span> (Qal: to wash) · Piel = wash thoroughly; in a ritual preparation context the washing is complete and thorough</td>
  </tr>

  <tr>
    <td>17</td>
    <td><span class="heb">יְהַלֲלוּ</span></td>
    <td>Wayyiqtol 3mp</td>
    <td><span class="heb">הָלַל</span></td>
    <td>Gen 12:15</td>
    <td>"Pharaoh's officials praised her"</td>
    <td><select class="parse-field" id="f17"><option value="">—</option><option>I</option><option>F</option><option>D</option><option>SA</option><option>DN</option></select></td>
    <td><button class="reveal-btn" onclick="toggle('r17')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r17">
    <td colspan="8"><strong>SA — Simple Action</strong> · Root: <span class="heb">הָלַל</span> (Qal: to shine, be bright — rare in this sense) · Praising is the Piel's primary meaning; Qal use is functionally unrelated; no intensification model works</td>
  </tr>

  <tr>
    <td>18</td>
    <td><span class="heb">יְבַקֵּשׁ</span></td>
    <td>Wayyiqtol 3ms</td>
    <td><span class="heb">בָּקַשׁ</span></td>
    <td>Gen 37:15</td>
    <td>"what are you seeking?"</td>
    <td><select class="parse-field" id="f18"><option value="">—</option><option>I</option><option>F</option><option>D</option><option>SA</option><option>DN</option></select></td>
    <td><button class="reveal-btn" onclick="toggle('r18')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r18">
    <td colspan="8"><strong>I — Intensive</strong> · Root: <span class="heb">בָּקַשׁ</span> (Qal: to seek — uncommon) · Piel = seek diligently/earnestly; intensive searching is the standard Piel nuance for this root</td>
  </tr>

  <tr>
    <td>19</td>
    <td><span class="heb">לְנַחֵם</span></td>
    <td>Inf. Construct</td>
    <td><span class="heb">נָחַם</span></td>
    <td>Gen 37:35</td>
    <td>"he refused to be comforted"</td>
    <td><select class="parse-field" id="f19"><option value="">—</option><option>I</option><option>F</option><option>D</option><option>SA</option><option>DN</option></select></td>
    <td><button class="reveal-btn" onclick="toggle('r19')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r19">
    <td colspan="8"><strong>I/SA — Intensive or Simple Action</strong> · Root: <span class="heb">נָחַם</span> (Qal: to be sorry, regret; Niphal: to be comforted) · Piel = actively comfort another person; whether this is "intensified comforting" or the Piel's own action is debated</td>
  </tr>

  <tr>
    <td>20</td>
    <td><span class="heb">צִוָּה</span></td>
    <td>Perfect 3ms</td>
    <td><span class="heb">צָוָה</span></td>
    <td>Gen 6:22</td>
    <td>"God had commanded him"</td>
    <td><select class="parse-field" id="f20"><option value="">—</option><option>I</option><option>F</option><option>D</option><option>SA</option><option>DN</option></select></td>
    <td><button class="reveal-btn" onclick="toggle('r20')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r20">
    <td colspan="8"><strong>SA — Simple Action</strong> · Root: <span class="heb">צָוָה</span> (no common Qal) · Same root as #5; commanding is always the Piel's standard function</td>
  </tr>

  <tr>
    <td>21</td>
    <td><span class="heb">לְכַפֵּר</span></td>
    <td>Inf. Construct</td>
    <td><span class="heb">כָּפַר</span></td>
    <td>Lev 4:20</td>
    <td>"to make atonement for them"</td>
    <td><select class="parse-field" id="f21"><option value="">—</option><option>I</option><option>F</option><option>D</option><option>SA</option><option>DN</option></select></td>
    <td><button class="reveal-btn" onclick="toggle('r21')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r21">
    <td colspan="8"><strong>DN — Denominative</strong> · Root: <span class="heb">כָּפַר</span> · Derived from noun <span class="heb">כֹּפֶר</span> ("ransom, covering, pitch") · The Piel performs the act of covering/ransoming = make atonement; the noun explains the theology</td>
  </tr>

  <tr>
    <td>22</td>
    <td><span class="heb">יְחַלֵּל</span></td>
    <td>Wayyiqtol 3ms</td>
    <td><span class="heb">חָלַל</span></td>
    <td>Lev 21:12</td>
    <td>"he shall not profane the sanctuary"</td>
    <td><select class="parse-field" id="f22"><option value="">—</option><option>I</option><option>F</option><option>D</option><option>SA</option><option>DN</option></select></td>
    <td><button class="reveal-btn" onclick="toggle('r22')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r22">
    <td colspan="8"><strong>F — Factitive</strong> · Root: <span class="heb">חָלַל</span> (Qal: to be profane, common — stative) · Piel = cause the sanctuary to enter the state of profaneness = desecrate</td>
  </tr>

  <tr>
    <td>23</td>
    <td><span class="heb">בִּקֵּשׁ</span></td>
    <td>Perfect 3ms</td>
    <td><span class="heb">בָּקַשׁ</span></td>
    <td>Gen 43:30</td>
    <td>"he sought a place to weep"</td>
    <td><select class="parse-field" id="f23"><option value="">—</option><option>I</option><option>F</option><option>D</option><option>SA</option><option>DN</option></select></td>
    <td><button class="reveal-btn" onclick="toggle('r23')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r23">
    <td colspan="8"><strong>I — Intensive</strong> · Root: <span class="heb">בָּקַשׁ</span> (Qal: to seek) · Same analysis as #18; diligent seeking is the Piel's standard nuance for this root</td>
  </tr>

  <tr>
    <td>24</td>
    <td><span class="heb">יְנַחֵם</span></td>
    <td>Yiqtol 3ms</td>
    <td><span class="heb">נָחַם</span></td>
    <td>Gen 5:29</td>
    <td>"this one will comfort us"</td>
    <td><select class="parse-field" id="f24"><option value="">—</option><option>I</option><option>F</option><option>D</option><option>SA</option><option>DN</option></select></td>
    <td><button class="reveal-btn" onclick="toggle('r24')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r24">
    <td colspan="8"><strong>I/SA — Intensive or Simple Action</strong> · Root: <span class="heb">נָחַם</span> (Qal: to be sorry; Niphal: to be comforted) · Same analysis as #19; the Piel = actively comfort, console; Niphal = be comforted (passive/reflexive)</td>
  </tr>

  <tr>
    <td>25</td>
    <td><span class="heb">לְהַלֵּל</span></td>
    <td>Inf. Construct</td>
    <td><span class="heb">הָלַל</span></td>
    <td>Psa 113:1</td>
    <td>"praise the name of the LORD"</td>
    <td><select class="parse-field" id="f25"><option value="">—</option><option>I</option><option>F</option><option>D</option><option>SA</option><option>DN</option></select></td>
    <td><button class="reveal-btn" onclick="toggle('r25')">▶ Answer</button></td>
  </tr>
  <tr class="answer-row" id="r25">
    <td colspan="8"><strong>SA — Simple Action</strong> · Root: <span class="heb">הָלַל</span> · Same analysis as #17; praise is always the Piel's function; Qal "shine" is semantically remote</td>
  </tr>

</table>

<h2>Discussion Questions</h2>
<div class="discussion">
  <ol class="disc">
    <li>Items 1, 5, 10, 17, 20 are all classified as Simple Action. What do these roots share? Why is a Qal→Piel intensification analysis not helpful for them?</li>
    <li>Items 2, 12, 15, 22: these Factitive Piels all involve stative roots. What is the Qal meaning of each root, and how does the Piel "factitivize" it — that is, how does it cause the object to enter the state the Qal describes?</li>
    <li>Items 16 and 9 (<span class="heb">כָּבַס</span> "wash" and <span class="heb">כָּסָה</span> "cover"): both are Intensive. What does the intensification add for a washing verb vs. a covering verb? Is "wash thoroughly" or "wash repeatedly" a better description for <span class="heb">כָּבַס</span>? Does the same choice apply to <span class="heb">כָּסָה</span>?</li>
    <li>Item 21 (<span class="heb">לְכַפֵּר</span>): if this is Denominative, what noun is it derived from? How does knowing that noun illuminate the theological significance of <span class="heb">כִּפֶּר</span> in Leviticus?</li>
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

