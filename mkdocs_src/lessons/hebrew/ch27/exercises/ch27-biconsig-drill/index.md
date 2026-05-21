# Biconsig Drill

*Chapter 27 — Hiphil Weak*

[Full screen](ch27-biconsig-drill.html){.md-button}  [Markdown](ch27-biconsig-drill.md){.md-button}  [Print (PDF)](ch27-biconsig-drill.pdf){.md-button}

<style>

  body { font-family: Georgia, serif;    color: #222; }
  h1 { font-size: 1.4em; border-bottom: 2px solid #444; padding-bottom: .4em; }
  h2 { font-size: 1.1em; margin-top: 2em; color: #444; }
  .subtitle { color: #666; font-style: italic; margin-top: -.3em; }
  table { border-collapse: collapse;  margin: 1em 0; }
  th { background: #2a4a6e; color: #fff; padding: .5em .7em; text-align: left; font-size: .85em; }
  td { border: 1px solid #ccc; padding: .4em .6em; font-size: .85em; vertical-align: top; }
  tr:nth-child(even) td { background: #f7f7f7; }
  .heb { font-size: 1.2em; direction: rtl; unicode-bidi: embed; }
  input.parse-field { width: 100%; box-sizing: border-box; font-size: .85em; padding: 3px 5px; border: 1px solid #aaa; border-radius: 3px; }
  .answer-row td { background: #f0faf0 !important; color: #2a6e2a; font-size: .82em; }
  .answer-row { display: none; }
  button.reveal-btn { font-size: .78em; padding: 2px 7px; cursor: pointer; border: 1px solid #888; border-radius: 3px; background: #fff; white-space: nowrap; }
  .controls { margin: 1em 0; display: flex; gap: .6em; flex-wrap: wrap; }
  .controls button { padding: .4em .9em; font-size: .9em; cursor: pointer; border: 1px solid #555; border-radius: 4px; background: #f0f0f0; }
  .controls button:hover { background: #ddd; }
  .tip { background: #fffbe6; border-left: 4px solid #d4a017; padding: .5em 1em; margin: 1em 0; font-size: .88em; }
  .discussion { background: #f0f4ff; border-left: 4px solid #2a4a6e; padding: .6em 1em; margin: 1em 0; font-size: .88em; }
  ol.disc { margin: .4em 0 0 1.2em; padding: 0; }
  ol.disc li { margin-bottom: .5em; }
  .diag-table td, .diag-table th { font-size: .82em; }
  @media print {
    button, .controls { display: none !important; }
    input.parse-field { border: none; border-bottom: 1px solid #000; background: transparent; }
    .answer-row { display: table-row !important; }
  }

</style>

<h1>Chapter 27 — Biconsonantal / Geminate Disambiguation Drill</h1>
<p class="subtitle">BBH Chapters 25 &amp; 27 · Niphal and Hiphil Weak Verbs</p>

<p>For each form: (1) <strong>identify the stem</strong> (Niphal or Hiphil), (2) <strong>parse</strong> (conjugation + PGN), (3) <strong>identify the weak class</strong> (Biconsonantal or Geminate), (4) <strong>give the root and translate</strong>.</p>

<div class="tip">
<strong>Key diagnostic:</strong> Biconsonantal and Geminate forms are vocally identical in Niphal and Hiphil.
<div style="overflow-x:auto;max-width:100%;"><table class="diag-table" style="margin:.6em 0 0 0;">
  <tr><th>Feature</th><th>Biconsonantal (II-י/ו)</th><th>Geminate (R2=R3)</th></tr>
  <tr><td>Root</td><td>R1-ו/י-R3 (e.g. קוּם, שׁוּב)</td><td>R1-R2-R2 (e.g. סָבַב, שָׁלַל)</td></tr>
  <tr><td>Niphal perfect 3ms</td><td>נָקִים (נָ qamets)</td><td>נָסַב (נָ qamets) — identical</td></tr>
  <tr><td>Hiphil perfect 3ms</td><td>הֵקִים (הֵ tsere)</td><td>הֵסֵב (הֵ tsere) — identical</td></tr>
  <tr><td>Hiphil imperfect 3ms</td><td>יָקִים (יָ qamets)</td><td>יָסֵב (יָ qamets) — identical</td></tr>
  <tr><td><strong>Distinguisher</strong></td><td>Medial vowel letter ו/י in stem</td><td>Dagesh forte in R2 when doubled</td></tr>
</table></div>
</div>

<div class="controls">
  <button onclick="showAll()">Show All Answers</button>
  <button onclick="hideAll()">Hide All Answers</button>
  <button onclick="clearAll()">Clear All Inputs</button>
</div>

<!-- PART A -->
<h2>Part A — Niphal: Biconsonantal vs. Geminate</h2>

<div style="overflow-x:auto;max-width:100%;"><table>
  <tr><th>#</th><th>Form</th><th>Reference</th><th>Context</th><th>Stem</th><th>Conjugation</th><th>PGN</th><th>Class</th><th>Root</th><th></th></tr>

  <tr><td>1</td><td><span class="heb">נָכוֹן</span></td><td>Gen 41:32</td><td>"the thing is ___ by God"</td>
    <td><input class="parse-field" id="a1s"></td><td><input class="parse-field" id="a1c"></td><td><input class="parse-field" id="a1p"></td><td><input class="parse-field" id="a1k"></td><td><input class="parse-field" id="a1r"></td>
    <td><button class="reveal-btn" onclick="toggle('r1')">▶</button></td></tr>
  <tr class="answer-row" id="r1"><td colspan="10"><strong>Niphal · Perfect/Participle · 3ms/ms · Biconsonantal · כּוּן</strong> — "is established / firm"; נָ prefix (qamets) = Niphal Biconsonantal; medial ו vowel letter identifies Biconsonantal, not Geminate</td></tr>

  <tr><td>2</td><td><span class="heb">נָסַב</span></td><td>1 Kgs 7:24</td><td>"the gourds ___ it, ten to a cubit"</td>
    <td><input class="parse-field" id="a2s"></td><td><input class="parse-field" id="a2c"></td><td><input class="parse-field" id="a2p"></td><td><input class="parse-field" id="a2k"></td><td><input class="parse-field" id="a2r"></td>
    <td><button class="reveal-btn" onclick="toggle('r2')">▶</button></td></tr>
  <tr class="answer-row" id="r2"><td colspan="10"><strong>Niphal · Perfect · 3ms · Geminate · סָבַב</strong> — "encircled / went around"; נָ prefix (qamets) = Niphal; R2=R3=ב identifies Geminate; compare Biconsonantal נָכוֹן (medial ו) vs. Geminate נָסַב (no medial vowel letter)</td></tr>

  <tr><td>3</td><td><span class="heb">יִכּוֹן</span></td><td>Psa 93:2</td><td>"your throne ___ from of old"</td>
    <td><input class="parse-field" id="a3s"></td><td><input class="parse-field" id="a3c"></td><td><input class="parse-field" id="a3p"></td><td><input class="parse-field" id="a3k"></td><td><input class="parse-field" id="a3r"></td>
    <td><button class="reveal-btn" onclick="toggle('r3')">▶</button></td></tr>
  <tr class="answer-row" id="r3"><td colspan="10"><strong>Niphal · Imperfect · 3ms · Biconsonantal · כּוּן</strong> — "is established"; יִ prefix + dagesh in כּ (Niphal pattern) + holem-vav = Biconsonantal; the dagesh here is Niphal's assimilation pattern, not R2=R3 doubling</td></tr>

  <tr><td>4</td><td><span class="heb">יִסֹּב</span></td><td>Num 21:4</td><td>"they traveled ___ Mount Edom"</td>
    <td><input class="parse-field" id="a4s"></td><td><input class="parse-field" id="a4c"></td><td><input class="parse-field" id="a4p"></td><td><input class="parse-field" id="a4k"></td><td><input class="parse-field" id="a4r"></td>
    <td><button class="reveal-btn" onclick="toggle('r4')">▶</button></td></tr>
  <tr class="answer-row" id="r4"><td colspan="10"><strong>Niphal · Imperfect · 3ms · Geminate · סָבַב</strong> — "went around"; יִ prefix + dagesh in סּ (R2=R3 doubled) + holem = Geminate; contrast Biconsonantal יִכּוֹן which retains medial ו vowel letter</td></tr>

  <tr><td>5</td><td><span class="heb">הֵכּוֹן</span></td><td>Psa 57:8</td><td>"my heart is ___, O God"</td>
    <td><input class="parse-field" id="a5s"></td><td><input class="parse-field" id="a5c"></td><td><input class="parse-field" id="a5p"></td><td><input class="parse-field" id="a5k"></td><td><input class="parse-field" id="a5r"></td>
    <td><button class="reveal-btn" onclick="toggle('r5')">▶</button></td></tr>
  <tr class="answer-row" id="r5"><td colspan="10"><strong>Niphal · Perfect · 3ms · Biconsonantal · כּוּן</strong> — "is ready / prepared"; הֵ + dagesh + holem-vav = Niphal Biconsonantal perfect variant; context (readied heart) confirms passive sense</td></tr>

  <tr><td>6</td><td><span class="heb">הֵסֹּב</span></td><td>Num 34:4</td><td>"your border ___ from the south"</td>
    <td><input class="parse-field" id="a6s"></td><td><input class="parse-field" id="a6c"></td><td><input class="parse-field" id="a6p"></td><td><input class="parse-field" id="a6k"></td><td><input class="parse-field" id="a6r"></td>
    <td><button class="reveal-btn" onclick="toggle('r6')">▶</button></td></tr>
  <tr class="answer-row" id="r6"><td colspan="10"><strong>Niphal · Perfect · 3ms · Geminate · סָבַב</strong> — "turned / went around"; הֵ + dagesh in סּ (R2=R3) + holem = Niphal Geminate perfect; contrast Biconsonantal הֵכּוֹן (medial ו retained)</td></tr>

  <tr><td>7</td><td><span class="heb">נָשׁוּב</span></td><td>Lam 3:40</td><td>"let us examine and ___ to the LORD"</td>
    <td><input class="parse-field" id="a7s"></td><td><input class="parse-field" id="a7c"></td><td><input class="parse-field" id="a7p"></td><td><input class="parse-field" id="a7k"></td><td><input class="parse-field" id="a7r"></td>
    <td><button class="reveal-btn" onclick="toggle('r7')">▶</button></td></tr>
  <tr class="answer-row" id="r7"><td colspan="10"><strong>Niphal · Cohortative · 1cp · Biconsonantal · שׁוּב</strong> — "let us return"; נָ prefix + medial ו vowel letter = Niphal Biconsonantal; cohortative sense from context (exhortation to repentance)</td></tr>

  <tr><td>8</td><td><span class="heb">נָתֹם</span></td><td>1 Sam 3:12</td><td>"when I ___ what I have spoken"</td>
    <td><input class="parse-field" id="a8s"></td><td><input class="parse-field" id="a8c"></td><td><input class="parse-field" id="a8p"></td><td><input class="parse-field" id="a8k"></td><td><input class="parse-field" id="a8r"></td>
    <td><button class="reveal-btn" onclick="toggle('r8')">▶</button></td></tr>
  <tr class="answer-row" id="r8"><td colspan="10"><strong>Niphal · Infinitive Construct · — · Geminate · תָּמַם</strong> — "to be completed / finished"; נָ prefix + holem = Niphal Geminate inf. construct; root תָּמַם has R2=R3=מ</td></tr>
</table></div>

<div class="tip"><strong>Key diagnostic — Part A (Niphal):</strong> Both Biconsonantal and Geminate use נָ (qamets) in the perfect/participle. In the imperfect both use יִ with dagesh. The dagesh in Biconsonantal (יִכּוֹן) is the Niphal pattern; in Geminate (יִסֹּב) it represents doubled R2=R3. The only reliable distinguisher is root structure: Biconsonantal medial = ו/י; Geminate medial = same consonant as R3.</div>

<!-- PART B -->
<h2>Part B — Hiphil: Biconsonantal vs. Geminate</h2>

<div style="overflow-x:auto;max-width:100%;"><table>
  <tr><th>#</th><th>Form</th><th>Reference</th><th>Context</th><th>Stem</th><th>Conjugation</th><th>PGN</th><th>Class</th><th>Root</th><th></th></tr>

  <tr><td>9</td><td><span class="heb">הֵקִים</span></td><td>Gen 6:18</td><td>"I will ___ my covenant with you"</td>
    <td><input class="parse-field" id="b9s"></td><td><input class="parse-field" id="b9c"></td><td><input class="parse-field" id="b9p"></td><td><input class="parse-field" id="b9k"></td><td><input class="parse-field" id="b9r"></td>
    <td><button class="reveal-btn" onclick="toggle('r9')">▶</button></td></tr>
  <tr class="answer-row" id="r9"><td colspan="10"><strong>Hiphil · Perfect · 3ms · Biconsonantal · קוּם</strong> — "established / raised up"; הֵ prefix (tsere) = Hiphil; medial ו vowel letter = Biconsonantal; contrast Geminate הֵסֵב</td></tr>

  <tr><td>10</td><td><span class="heb">הֵסֵב</span></td><td>2 Sam 2:22</td><td>"___ from following me"</td>
    <td><input class="parse-field" id="b10s"></td><td><input class="parse-field" id="b10c"></td><td><input class="parse-field" id="b10p"></td><td><input class="parse-field" id="b10k"></td><td><input class="parse-field" id="b10r"></td>
    <td><button class="reveal-btn" onclick="toggle('r10')">▶</button></td></tr>
  <tr class="answer-row" id="r10"><td colspan="10"><strong>Hiphil · Perfect · 3ms · Geminate · סָבַב</strong> — "turned aside"; הֵ prefix (tsere) = Hiphil; no medial vowel letter, R2=R3=ב = Geminate; הֵקִים retains medial ו, הֵסֵב does not</td></tr>

  <tr><td>11</td><td><span class="heb">יָקִים</span></td><td>Deut 18:15</td><td>"the LORD your God will ___ a prophet"</td>
    <td><input class="parse-field" id="b11s"></td><td><input class="parse-field" id="b11c"></td><td><input class="parse-field" id="b11p"></td><td><input class="parse-field" id="b11k"></td><td><input class="parse-field" id="b11r"></td>
    <td><button class="reveal-btn" onclick="toggle('r11')">▶</button></td></tr>
  <tr class="answer-row" id="r11"><td colspan="10"><strong>Hiphil · Imperfect · 3ms · Biconsonantal · קוּם</strong> — "will raise up"; יָ prefix (qamets) = Hiphil Biconsonantal imperfect; medial ו vowel letter retained; contrast Geminate יָסֵב (no medial vowel letter)</td></tr>

  <tr><td>12</td><td><span class="heb">יָסֵב</span></td><td>Eccl 1:6</td><td>"the wind ___ to the south"</td>
    <td><input class="parse-field" id="b12s"></td><td><input class="parse-field" id="b12c"></td><td><input class="parse-field" id="b12p"></td><td><input class="parse-field" id="b12k"></td><td><input class="parse-field" id="b12r"></td>
    <td><button class="reveal-btn" onclick="toggle('r12')">▶</button></td></tr>
  <tr class="answer-row" id="r12"><td colspan="10"><strong>Hiphil · Imperfect · 3ms · Geminate · סָבַב</strong> — "causes to go around / turns"; יָ prefix (qamets) = Hiphil; no medial vowel letter = Geminate; contrast Biconsonantal יָקִים (medial ו retained)</td></tr>

  <tr><td>13</td><td><span class="heb">הָקֵם</span></td><td>Deut 27:26</td><td>"\'___ the words of this law\'"</td>
    <td><input class="parse-field" id="b13s"></td><td><input class="parse-field" id="b13c"></td><td><input class="parse-field" id="b13p"></td><td><input class="parse-field" id="b13k"></td><td><input class="parse-field" id="b13r"></td>
    <td><button class="reveal-btn" onclick="toggle('r13')">▶</button></td></tr>
  <tr class="answer-row" id="r13"><td colspan="10"><strong>Hiphil · Imperative · 2ms · Biconsonantal · קוּם</strong> — "raise up! / confirm!"; הָ prefix (qamets) = Hiphil imperative; tsere vowel in stem + no doubling = Biconsonantal; contrast Geminate הָסֵב</td></tr>

  <tr><td>14</td><td><span class="heb">הָסֵב</span></td><td>2 Sam 2:22</td><td>"___ from following me"</td>
    <td><input class="parse-field" id="b14s"></td><td><input class="parse-field" id="b14c"></td><td><input class="parse-field" id="b14p"></td><td><input class="parse-field" id="b14k"></td><td><input class="parse-field" id="b14r"></td>
    <td><button class="reveal-btn" onclick="toggle('r14')">▶</button></td></tr>
  <tr class="answer-row" id="r14"><td colspan="10"><strong>Hiphil · Imperative · 2ms · Geminate · סָבַב</strong> — "turn aside!"; הָ prefix (qamets) = Hiphil imperative; same form as Biconsonantal הָקֵם except root is R2=R3=ב (Geminate); tsere vowel = contracted Geminate stem</td></tr>

  <tr><td>15</td><td><span class="heb">מֵקִים</span></td><td>1 Sam 2:8</td><td>"He ___ the poor from the dust"</td>
    <td><input class="parse-field" id="b15s"></td><td><input class="parse-field" id="b15c"></td><td><input class="parse-field" id="b15p"></td><td><input class="parse-field" id="b15k"></td><td><input class="parse-field" id="b15r"></td>
    <td><button class="reveal-btn" onclick="toggle('r15')">▶</button></td></tr>
  <tr class="answer-row" id="r15"><td colspan="10"><strong>Hiphil · Participle · ms · Biconsonantal · קוּם</strong> — "one who raises up"; מֵ prefix (tsere) = Hiphil participle; medial ו retained = Biconsonantal; contrast Geminate מֵסֵב (no medial vowel letter)</td></tr>

  <tr><td>16</td><td><span class="heb">מֵסֵב</span></td><td>Ezek 41:7</td><td>"the structure surrounding the house ___ upward"</td>
    <td><input class="parse-field" id="b16s"></td><td><input class="parse-field" id="b16c"></td><td><input class="parse-field" id="b16p"></td><td><input class="parse-field" id="b16k"></td><td><input class="parse-field" id="b16r"></td>
    <td><button class="reveal-btn" onclick="toggle('r16')">▶</button></td></tr>
  <tr class="answer-row" id="r16"><td colspan="10"><strong>Hiphil · Participle · ms · Geminate · סָבַב</strong> — "going around / surrounding"; מֵ prefix (tsere) = Hiphil participle; no medial vowel letter, tsere stem vowel = Geminate contracted form; compare Biconsonantal מֵקִים</td></tr>
</table></div>

<div class="tip"><strong>Key diagnostic — Part B (Hiphil):</strong> Hiphil Biconsonantal and Geminate are vocally identical across all conjugations: הֵ perfect, יָ imperfect, הָ imperative, מֵ participle. The only distinguisher is root structure — whether the medial position contains a vowel letter (ו/י = Biconsonantal) or a repeated consonant (= Geminate). Context usually confirms the meaning once the root is identified.</div>

<!-- PART C -->
<h2>Part C — Mixed: Stem and Class Both Unknown</h2>
<p>Identify stem (Niphal or Hiphil) <em>and</em> class (Biconsonantal or Geminate) from the form and context alone.</p>

<div style="overflow-x:auto;max-width:100%;"><table>
  <tr><th>#</th><th>Form</th><th>Reference</th><th>Context</th><th>Stem</th><th>Conjugation</th><th>PGN</th><th>Class</th><th>Root</th><th></th></tr>

  <tr><td>17</td><td><span class="heb">נָמֹוג</span></td><td>Isa 14:31</td><td>"all Philistia ___"</td>
    <td><input class="parse-field" id="c17s"></td><td><input class="parse-field" id="c17c"></td><td><input class="parse-field" id="c17p"></td><td><input class="parse-field" id="c17k"></td><td><input class="parse-field" id="c17r"></td>
    <td><button class="reveal-btn" onclick="toggle('r17')">▶</button></td></tr>
  <tr class="answer-row" id="r17"><td colspan="10"><strong>Niphal · Perfect · 3ms · Biconsonantal · מוּג</strong> — "melted / dissolved"; נָ prefix + medial ו = Niphal Biconsonantal; root מוּג = to melt/dissolve</td></tr>

  <tr><td>18</td><td><span class="heb">הֵמַס</span></td><td>Josh 2:11</td><td>"the LORD ___ our hearts"</td>
    <td><input class="parse-field" id="c18s"></td><td><input class="parse-field" id="c18c"></td><td><input class="parse-field" id="c18p"></td><td><input class="parse-field" id="c18k"></td><td><input class="parse-field" id="c18r"></td>
    <td><button class="reveal-btn" onclick="toggle('r18')">▶</button></td></tr>
  <tr class="answer-row" id="r18"><td colspan="10"><strong>Hiphil · Perfect · 3ms · Geminate · מסס</strong> — "caused to melt"; הֵ prefix (tsere) = Hiphil; no medial vowel letter, R2=R3=ס = Geminate; patach under R2 in contracted stem</td></tr>

  <tr><td>19</td><td><span class="heb">יָרֻם</span></td><td>Isa 52:13</td><td>"my servant shall be high and ___ up"</td>
    <td><input class="parse-field" id="c19s"></td><td><input class="parse-field" id="c19c"></td><td><input class="parse-field" id="c19p"></td><td><input class="parse-field" id="c19k"></td><td><input class="parse-field" id="c19r"></td>
    <td><button class="reveal-btn" onclick="toggle('r19')">▶</button></td></tr>
  <tr class="answer-row" id="r19"><td colspan="10"><strong>Niphal · Imperfect · 3ms · Biconsonantal · רוּם</strong> — "will be exalted / lifted up"; יָ prefix + qibbutz under R2 (passive nuance) = Niphal Biconsonantal imperfect; contrast Hiphil יָרִים (chiriq under R2)</td></tr>

  <tr><td>20</td><td><span class="heb">יָרֹם</span></td><td>Psa 99:2</td><td>"great is the LORD, and ___ above all peoples"</td>
    <td><input class="parse-field" id="c20s"></td><td><input class="parse-field" id="c20c"></td><td><input class="parse-field" id="c20p"></td><td><input class="parse-field" id="c20k"></td><td><input class="parse-field" id="c20r"></td>
    <td><button class="reveal-btn" onclick="toggle('r20')">▶</button></td></tr>
  <tr class="answer-row" id="r20"><td colspan="10"><strong>Niphal · Imperfect · 3ms · Biconsonantal · רוּם</strong> — "is exalted / high"; יָ prefix + holem under R2 = Niphal Biconsonantal imperfect; compare Hiphil יָרִים (chiriq = causative)</td></tr>

  <tr><td>21</td><td><span class="heb">הֵרִים</span></td><td>Gen 14:22</td><td>"I have ___ my hand to the LORD"</td>
    <td><input class="parse-field" id="c21s"></td><td><input class="parse-field" id="c21c"></td><td><input class="parse-field" id="c21p"></td><td><input class="parse-field" id="c21k"></td><td><input class="parse-field" id="c21r"></td>
    <td><button class="reveal-btn" onclick="toggle('r21')">▶</button></td></tr>
  <tr class="answer-row" id="r21"><td colspan="10"><strong>Hiphil · Perfect · 3ms · Biconsonantal · רוּם</strong> — "lifted up"; הֵ prefix (tsere) + chiriq-yod in stem = Hiphil Biconsonantal perfect; causative: caused the hand to rise = swore an oath</td></tr>

  <tr><td>22</td><td><span class="heb">הוּרַם</span></td><td>Lev 4:10</td><td>"just as it is ___ from the ox of peace offerings"</td>
    <td><input class="parse-field" id="c22s"></td><td><input class="parse-field" id="c22c"></td><td><input class="parse-field" id="c22p"></td><td><input class="parse-field" id="c22k"></td><td><input class="parse-field" id="c22r"></td>
    <td><button class="reveal-btn" onclick="toggle('r22')">▶</button></td></tr>
  <tr class="answer-row" id="r22"><td colspan="10"><strong>Hophal · Perfect · 3ms · Biconsonantal · רוּם</strong> — "was lifted off / removed"; הוּ prefix (holem-vav) = Hophal (passive of Hiphil), not Hiphil or Niphal; Biconsonantal root רוּם; Hophal Biconsonantal prefix = הוּ</td></tr>

  <tr><td>23</td><td><span class="heb">יָשׁוּב</span></td><td>Hos 14:8</td><td>"they ___ in the shade"</td>
    <td><input class="parse-field" id="c23s"></td><td><input class="parse-field" id="c23c"></td><td><input class="parse-field" id="c23p"></td><td><input class="parse-field" id="c23k"></td><td><input class="parse-field" id="c23r"></td>
    <td><button class="reveal-btn" onclick="toggle('r23')">▶</button></td></tr>
  <tr class="answer-row" id="r23"><td colspan="10"><strong>Qal · Imperfect · 3ms · Biconsonantal · שׁוּב</strong> — "will dwell / return"; יָ prefix + שׁוּב in Qal (no Niphal נ-prefix assimilation, no Hiphil causative marker); Biconsonantal medial ו retained; reminder: not every Biconsonantal form is Niphal or Hiphil</td></tr>

  <tr><td>24</td><td><span class="heb">יָשֹׁב</span></td><td>Lam 1:11</td><td>"all her people ___ to find bread"</td>
    <td><input class="parse-field" id="c24s"></td><td><input class="parse-field" id="c24c"></td><td><input class="parse-field" id="c24p"></td><td><input class="parse-field" id="c24k"></td><td><input class="parse-field" id="c24r"></td>
    <td><button class="reveal-btn" onclick="toggle('r24')">▶</button></td></tr>
  <tr class="answer-row" id="r24"><td colspan="10"><strong>Qal · Imperfect · 3ms · Biconsonantal · שׁוּב</strong> — "returned / went around searching"; holem vowel in stem (יָשֹׁב) vs. shureq in יָשׁוּב; both are Qal Biconsonantal but with different vowel grades; neither is Niphal or Hiphil — no נ/הֵ/הָ prefix marker</td></tr>
</table></div>

<h2>Discussion Questions</h2>
<div class="discussion">
  <ol class="disc">
    <li>Items 1 (<span class="heb">נָכוֹן</span>) and 2 (<span class="heb">נָסַב</span>) have the same prefix vowel (נָ, qamets) and nearly identical shapes. What is the only reliable way to know that <span class="heb">נָכוֹן</span> is Biconsonantal (root <span class="heb">כּוּן</span>) and <span class="heb">נָסַב</span> is Geminate (root <span class="heb">סָבַב</span>)?</li>
    <li>Items 9 (<span class="heb">הֵקִים</span>) and 10 (<span class="heb">הֵסֵב</span>) both have הֵ prefix (tsere). One retains a medial vowel letter; the other shows a contracted stem. Describe precisely what the medial position of each form looks like and how that reflects the underlying root structure.</li>
    <li>Items 11 (<span class="heb">יָקִים</span>) and 12 (<span class="heb">יָסֵב</span>) are both Hiphil imperfect 3ms with the same prefix vowel. A student encounters an unknown form <span class="heb">יָדֵל</span>. What question must they ask to determine whether it is Biconsonantal or Geminate, and what would each answer imply about the root?</li>
    <li>In Part C, items 19 (<span class="heb">יָרֻם</span>) and 21 (<span class="heb">הֵרִים</span>) come from the same root (<span class="heb">רוּם</span>) but differ in stem. What vowel under R2 distinguishes the Niphal imperfect from the Hiphil perfect, and what does that difference in vowel reflect about the function of each stem?</li>
    <li>Item 22 (<span class="heb">הוּרַם</span>) was classified as Hophal, not Niphal or Hiphil. After working through this drill, how would you describe a quick rule for identifying the Hophal Biconsonantal perfect, and how does its prefix vowel differ from both Niphal (נָ) and Hiphil (הֵ)?</li>
  </ol>
</div>

<script>
function toggle(id) {
  const row = document.getElementById(id);
  row.style.display = (row.style.display === 'table-row') ? 'none' : 'table-row';
}
function showAll() {
  document.querySelectorAll('.answer-row').forEach(r => r.style.display = 'table-row');
}
function hideAll() {
  document.querySelectorAll('.answer-row').forEach(r => r.style.display = 'none');
}
function clearAll() {
  document.querySelectorAll('input.parse-field').forEach(i => i.value = '');
}
</script>

