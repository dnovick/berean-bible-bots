# Passage Exercise

*Chapter 24 — Niphal Strong*

[Full screen](ch24-passage-exercise.html){.md-button}  [Markdown](ch24-passage-exercise.md){.md-button}  [Print (PDF)](ch24-passage-exercise.pdf){.md-button}

<style>

  body { font-family: Georgia, serif;    color: #222; line-height: 1.6; }
  h1 { font-size: 1.5rem; border-bottom: 2px solid #555; padding-bottom: .4rem; }
  h2 { font-size: 1.15rem; margin-top: 2rem; color: #333; }
  .subtitle { color: #666; font-style: italic; margin-top: -.5rem; }
  .instructions { background: #f8f8f0; border-left: 4px solid #bbb; padding: .75rem 1rem; margin: 1rem 0; }
  .passage-block { margin: 1.5rem 0; }
  .ref { font-weight: bold; font-size: 1rem; color: #444; display: block; margin-bottom: .3rem; }
  .hebrew { font-size: 1.25rem; direction: rtl; unicode-bidi: embed; line-height: 2; margin: .3rem 0; }
  .english { color: #555; font-style: italic; margin: .2rem 0 .6rem; }
  table { border-collapse: collapse; width: 100%; margin: .5rem 0; font-size: .92rem; }
  th { background: #e8e8e8; padding: .4rem .6rem; border: 1px solid #ccc; text-align: left; }
  td { padding: .35rem .5rem; border: 1px solid #ddd; vertical-align: middle; }
  td.verb-cell { font-size: 1.1rem; direction: rtl; unicode-bidi: embed; font-weight: bold; }
  td.num-cell { text-align: center; font-weight: bold; color: #666; width: 2rem; }
  input.parse-field {
    width: 100%; box-sizing: border-box; border: 1px solid #bbb; border-radius: 3px;
    padding: .25rem .4rem; font-family: Georgia, serif; font-size: .88rem;
    background: #fafff8;
  }
  input.parse-field:focus { outline: none; border-color: #5a9; box-shadow: 0 0 0 2px #c8ecd4; }
  .answer-row { display: none; background: #f0faf0; }
  .answer-row td { border-top: none; font-size: .88rem; color: #2a6e2a; padding: .3rem .5rem; }
  .answer-row.wrong td { background: #fff0f0; color: #8b0000; }
  .answer-row td.answer-label { font-weight: bold; color: #1a5c1a; }
  .answer-row.wrong td.answer-label { color: #8b0000; }
  button.reveal-btn {
    font-size: .78rem; padding: .15rem .5rem; cursor: pointer;
    background: #e8f4ec; border: 1px solid #7bba8f; border-radius: 3px; color: #2a6e2a;
    white-space: nowrap;
  }
  button.reveal-btn:hover { background: #c8ecd4; }
  button.reveal-btn.active { background: #c8ecd4; }
  .controls { display: flex; gap: .75rem; flex-wrap: wrap; margin: 1rem 0 1.5rem; }
  .controls button {
    padding: .4rem .9rem; cursor: pointer; border-radius: 4px; font-size: .88rem;
    border: 1px solid #999; background: #f0f0f0; color: #333;
  }
  .controls button:hover { background: #ddd; }
  .controls button.clear-btn { border-color: #c06060; color: #8b0000; background: #fff0f0; }
  .controls button.clear-btn:hover { background: #ffd8d8; }
  .section-break { border: none; border-top: 2px dashed #ccc; margin: 2rem 0; }
  .score-box { background: #f5f0ff; border: 1px solid #c0a8e8; border-radius: 6px; padding: .75rem 1rem; margin: 1.5rem 0; font-size: .92rem; }
  .reflection { margin-top: 1.5rem; }
  .reflection ol li { margin-bottom: .75rem; }
  @media print {
    .controls, button.reveal-btn { display: none; }
    input.parse-field { border: none; border-bottom: 1px solid #aaa; border-radius: 0; background: transparent; }
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

<h1>Chapter 24 — "Spot the Niphal" Passage Exercise</h1>
<p class="subtitle">Genesis 37, 44, 45, 47, 49 · The Joseph Narrative</p>

<div class="instructions">
  <strong>Instructions:</strong> For each numbered verb, answer <strong>Is it Niphal? (Yes / No)</strong>. Then for every verb:
  <ol style="margin:.4rem 0 0">
    <li>Parse it — give <strong>conjugation</strong>, <strong>person-gender-number</strong>, and <strong>root</strong>.</li>
    <li>State the <strong>semantic function</strong> (Passive / Reflexive / Simple action — or "NOT Niphal" for distractors).</li>
  </ol>
  Three verbs in this exercise are not Niphal — drawn from Qal already studied. Click <strong>▶ Answer</strong> on any row to reveal the correct parsing inline.
</div>

<div class="controls">
  <button onclick="showAll()">Show All Answers</button>
  <button onclick="hideAll()">Hide All Answers</button>
  <button class="clear-btn" onclick="clearAll()">Clear All Inputs</button>
</div>

<h2>Passage A — Genesis 37:7, 36</h2>

<div class="passage-block">
  <span class="ref">37:7</span>
  <div class="hebrew">וְהִנֵּה <strong>קָ֣מָה</strong> אֲלֻמָּתִ֗י וְגַם <strong>נִצָּ֑בָה</strong></div>
  <div class="english">"and behold, my sheaf [1] ____ and [2] ____."</div>
  <table>
    <tr>
      <th class="num-cell">#</th><th>Verb</th><th>Niphal?</th><th>Conjugation</th><th>PGN</th><th>Root</th><th>Stem / Function</th><th></th>
    </tr>
    <tr>
      <td class="num-cell">1</td>
      <td class="verb-cell">קָמָה</td>
      <td><input class="parse-field" id="f1-nip" placeholder="Yes / No"></td>
      <td><input class="parse-field" id="f1-conj" placeholder="conjugation"></td>
      <td><input class="parse-field" id="f1-pgn" placeholder="PGN"></td>
      <td><input class="parse-field" id="f1-root" placeholder="root"></td>
      <td><input class="parse-field" id="f1-func" placeholder="function"></td>
      <td><button class="reveal-btn" onclick="toggleAnswer('a1',this)">▶ Answer</button></td>
    </tr>
    <tr class="answer-row wrong" id="a1">
      <td class="answer-label">✗</td>
      <td class="verb-cell">קָמָה</td>
      <td colspan="6">✗ <strong>No — Qal</strong> | Perfect 3fs | קוּם | NOT Niphal — Qal: <em>arose</em>; biconsonantal Qal perfect 3fs; no נ prefix or dagesh forte</td>
    </tr>
    <tr>
      <td class="num-cell">2</td>
      <td class="verb-cell">נִצָּבָה</td>
      <td><input class="parse-field" id="f2-nip" placeholder="Yes / No"></td>
      <td><input class="parse-field" id="f2-conj" placeholder="conjugation"></td>
      <td><input class="parse-field" id="f2-pgn" placeholder="PGN"></td>
      <td><input class="parse-field" id="f2-root" placeholder="root"></td>
      <td><input class="parse-field" id="f2-func" placeholder="function"></td>
      <td><button class="reveal-btn" onclick="toggleAnswer('a2',this)">▶ Answer</button></td>
    </tr>
    <tr class="answer-row" id="a2">
      <td class="answer-label">✓</td>
      <td class="verb-cell">נִצָּבָה</td>
      <td colspan="6">✓ <strong>Yes — Niphal</strong> | Perfect 3fs | נָצַב | Reflexive — <em>it stood upright</em> (the sheaf stationed itself)</td>
    </tr>
  </table>
</div>

<div class="passage-block">
  <span class="ref">37:36</span>
  <div class="hebrew">וְהַ֨מְּדָנִ֔ים <strong>מָכְר֥וּ</strong> אֹת֖וֹ … <strong>וַיִּמָּכֵ֤ר</strong> יוֹסֵף֙ אֶל־מִצְרָ֔יִם</div>
  <div class="english">"Now the Midianites [3] ____ him … and Joseph [4] ____ into Egypt."</div>
  <table>
    <tr>
      <th class="num-cell">#</th><th>Verb</th><th>Niphal?</th><th>Conjugation</th><th>PGN</th><th>Root</th><th>Stem / Function</th><th></th>
    </tr>
    <tr>
      <td class="num-cell">3</td>
      <td class="verb-cell">מָכְרוּ</td>
      <td><input class="parse-field" id="f3-nip" placeholder="Yes / No"></td>
      <td><input class="parse-field" id="f3-conj" placeholder="conjugation"></td>
      <td><input class="parse-field" id="f3-pgn" placeholder="PGN"></td>
      <td><input class="parse-field" id="f3-root" placeholder="root"></td>
      <td><input class="parse-field" id="f3-func" placeholder="function"></td>
      <td><button class="reveal-btn" onclick="toggleAnswer('a3',this)">▶ Answer</button></td>
    </tr>
    <tr class="answer-row wrong" id="a3">
      <td class="answer-label">✗</td>
      <td class="verb-cell">מָכְרוּ</td>
      <td colspan="6">✗ <strong>No — Qal</strong> | Perfect 3cp | מָכַר | NOT Niphal — Qal: <em>had sold</em>; active Qal; contrast with #4 Niphal passive of the same root</td>
    </tr>
    <tr>
      <td class="num-cell">4</td>
      <td class="verb-cell">וַיִּמָּכֵר</td>
      <td><input class="parse-field" id="f4-nip" placeholder="Yes / No"></td>
      <td><input class="parse-field" id="f4-conj" placeholder="conjugation"></td>
      <td><input class="parse-field" id="f4-pgn" placeholder="PGN"></td>
      <td><input class="parse-field" id="f4-root" placeholder="root"></td>
      <td><input class="parse-field" id="f4-func" placeholder="function"></td>
      <td><button class="reveal-btn" onclick="toggleAnswer('a4',this)">▶ Answer</button></td>
    </tr>
    <tr class="answer-row" id="a4">
      <td class="answer-label">✓</td>
      <td class="verb-cell">וַיִּמָּכֵר</td>
      <td colspan="6">✓ <strong>Yes — Niphal</strong> | Wayyiqtol 3ms | מָכַר | Passive — <em>he was sold</em></td>
    </tr>
  </table>
</div>

<hr class="section-break">
<h2>Passage B — Genesis 44:9–20</h2>

<div class="passage-block">
  <span class="ref">44:9</span>
  <div class="hebrew">אֲשֶׁ֨ר <strong>יִמָּצֵ֥א</strong> אִתּ֛וֹ מֵעֲבָדֶ֖יךָ וָמֵ֑ת</div>
  <div class="english">"With whichever of your servants [5] ____ [the cup] shall die."</div>
  <table>
    <tr>
      <th class="num-cell">#</th><th>Verb</th><th>Niphal?</th><th>Conjugation</th><th>PGN</th><th>Root</th><th>Stem / Function</th><th></th>
    </tr>
    <tr>
      <td class="num-cell">5</td>
      <td class="verb-cell">יִמָּצֵא</td>
      <td><input class="parse-field" id="f5-nip" placeholder="Yes / No"></td>
      <td><input class="parse-field" id="f5-conj" placeholder="conjugation"></td>
      <td><input class="parse-field" id="f5-pgn" placeholder="PGN"></td>
      <td><input class="parse-field" id="f5-root" placeholder="root"></td>
      <td><input class="parse-field" id="f5-func" placeholder="function"></td>
      <td><button class="reveal-btn" onclick="toggleAnswer('a5',this)">▶ Answer</button></td>
    </tr>
    <tr class="answer-row" id="a5">
      <td class="answer-label">✓</td>
      <td class="verb-cell">יִמָּצֵא</td>
      <td colspan="6">✓ <strong>Yes — Niphal</strong> | Imperfect 3ms | מָצָא | Passive — <em>is found</em></td>
    </tr>
  </table>
</div>

<div class="passage-block">
  <span class="ref">44:12</span>
  <div class="hebrew"><strong>וַיִּמָּצֵא֙</strong> הַגָּבִ֔יעַ בְּאַמְתַּ֖חַת בִּנְיָמִֽן</div>
  <div class="english">"And the cup [6] ____ in Benjamin's sack."</div>
  <table>
    <tr>
      <th class="num-cell">#</th><th>Verb</th><th>Niphal?</th><th>Conjugation</th><th>PGN</th><th>Root</th><th>Stem / Function</th><th></th>
    </tr>
    <tr>
      <td class="num-cell">6</td>
      <td class="verb-cell">וַיִּמָּצֵא</td>
      <td><input class="parse-field" id="f6-nip" placeholder="Yes / No"></td>
      <td><input class="parse-field" id="f6-conj" placeholder="conjugation"></td>
      <td><input class="parse-field" id="f6-pgn" placeholder="PGN"></td>
      <td><input class="parse-field" id="f6-root" placeholder="root"></td>
      <td><input class="parse-field" id="f6-func" placeholder="function"></td>
      <td><button class="reveal-btn" onclick="toggleAnswer('a6',this)">▶ Answer</button></td>
    </tr>
    <tr class="answer-row" id="a6">
      <td class="answer-label">✓</td>
      <td class="verb-cell">וַיִּמָּצֵא</td>
      <td colspan="6">✓ <strong>Yes — Niphal</strong> | Wayyiqtol 3ms | מָצָא | Passive — <em>was found</em></td>
    </tr>
  </table>
</div>

<div class="passage-block">
  <span class="ref">44:20</span>
  <div class="hebrew">יֶ֣שׁ לָ֜נוּ אָ֣ב זָקֵ֗ן וְיֶ֤לֶד זְקֻנִים֙ קָטָ֔ן וְאָחִ֥יו מֵ֖ת <strong>וַיִּוָּתֵ֣ר</strong> ה֑וּא</div>
  <div class="english">"We have an aged father and a young child of his old age … and he alone [7] ____."</div>
  <table>
    <tr>
      <th class="num-cell">#</th><th>Verb</th><th>Niphal?</th><th>Conjugation</th><th>PGN</th><th>Root</th><th>Stem / Function</th><th></th>
    </tr>
    <tr>
      <td class="num-cell">7</td>
      <td class="verb-cell">וַיִּוָּתֵר</td>
      <td><input class="parse-field" id="f7-nip" placeholder="Yes / No"></td>
      <td><input class="parse-field" id="f7-conj" placeholder="conjugation"></td>
      <td><input class="parse-field" id="f7-pgn" placeholder="PGN"></td>
      <td><input class="parse-field" id="f7-root" placeholder="root"></td>
      <td><input class="parse-field" id="f7-func" placeholder="function"></td>
      <td><button class="reveal-btn" onclick="toggleAnswer('a7',this)">▶ Answer</button></td>
    </tr>
    <tr class="answer-row" id="a7">
      <td class="answer-label">✓</td>
      <td class="verb-cell">וַיִּוָּתֵר</td>
      <td colspan="6">✓ <strong>Yes — Niphal</strong> | Wayyiqtol 3ms | יָתַר | Passive/Middle — <em>was left, remained</em></td>
    </tr>
  </table>
</div>

<hr class="section-break">
<h2>Passage C — Genesis 45:1, 16</h2>

<div class="passage-block">
  <span class="ref">45:1</span>
  <div class="hebrew">וְלֹא־<strong>יָכֹל֩</strong> יוֹסֵ֨ף לְהִתְאַפֵּ֜ק לְכֹ֣ל <strong>הַנִּצָּבִ֣ים</strong> עָלָ֗יו</div>
  <div class="english">"Joseph [8] ____ no longer control himself before all those [9] ____ near him."</div>
  <table>
    <tr>
      <th class="num-cell">#</th><th>Verb</th><th>Niphal?</th><th>Conjugation</th><th>PGN</th><th>Root</th><th>Stem / Function</th><th></th>
    </tr>
    <tr>
      <td class="num-cell">8</td>
      <td class="verb-cell">יָכֹל</td>
      <td><input class="parse-field" id="f8-nip" placeholder="Yes / No"></td>
      <td><input class="parse-field" id="f8-conj" placeholder="conjugation"></td>
      <td><input class="parse-field" id="f8-pgn" placeholder="PGN"></td>
      <td><input class="parse-field" id="f8-root" placeholder="root"></td>
      <td><input class="parse-field" id="f8-func" placeholder="function"></td>
      <td><button class="reveal-btn" onclick="toggleAnswer('a8',this)">▶ Answer</button></td>
    </tr>
    <tr class="answer-row wrong" id="a8">
      <td class="answer-label">✗</td>
      <td class="verb-cell">יָכֹל</td>
      <td colspan="6">✗ <strong>No — Qal</strong> | Perfect 3ms | יָכֹל | NOT Niphal — Qal: <em>was able / could</em>; Qal stative with no Niphal counterpart</td>
    </tr>
    <tr>
      <td class="num-cell">9</td>
      <td class="verb-cell">הַנִּצָּבִים</td>
      <td><input class="parse-field" id="f9-nip" placeholder="Yes / No"></td>
      <td><input class="parse-field" id="f9-conj" placeholder="conjugation"></td>
      <td><input class="parse-field" id="f9-pgn" placeholder="PGN"></td>
      <td><input class="parse-field" id="f9-root" placeholder="root"></td>
      <td><input class="parse-field" id="f9-func" placeholder="function"></td>
      <td><button class="reveal-btn" onclick="toggleAnswer('a9',this)">▶ Answer</button></td>
    </tr>
    <tr class="answer-row" id="a9">
      <td class="answer-label">✓</td>
      <td class="verb-cell">הַנִּצָּבִים</td>
      <td colspan="6">✓ <strong>Yes — Niphal</strong> | Participle mp | נָצַב | Reflexive — <em>those standing</em> (having stationed themselves)</td>
    </tr>
  </table>
</div>

<div class="passage-block">
  <span class="ref">45:16</span>
  <div class="hebrew">וְהַקֹּ֣ל <strong>נִשְׁמַ֗ע</strong> בֵּ֤ית פַּרְעֹה֙ לֵאמֹ֔ר בָּ֥אוּ אֲחֵֽי־יוֹסֵ֖ף</div>
  <div class="english">"And the report [10] ____ in Pharaoh's household, 'Joseph's brothers have come.'"</div>
  <table>
    <tr>
      <th class="num-cell">#</th><th>Verb</th><th>Niphal?</th><th>Conjugation</th><th>PGN</th><th>Root</th><th>Stem / Function</th><th></th>
    </tr>
    <tr>
      <td class="num-cell">10</td>
      <td class="verb-cell">נִשְׁמַע</td>
      <td><input class="parse-field" id="f10-nip" placeholder="Yes / No"></td>
      <td><input class="parse-field" id="f10-conj" placeholder="conjugation"></td>
      <td><input class="parse-field" id="f10-pgn" placeholder="PGN"></td>
      <td><input class="parse-field" id="f10-root" placeholder="root"></td>
      <td><input class="parse-field" id="f10-func" placeholder="function"></td>
      <td><button class="reveal-btn" onclick="toggleAnswer('a10',this)">▶ Answer</button></td>
    </tr>
    <tr class="answer-row" id="a10">
      <td class="answer-label">✓</td>
      <td class="verb-cell">נִשְׁמַע</td>
      <td colspan="6">✓ <strong>Yes — Niphal</strong> | Perfect 3ms | שָׁמַע | Passive — <em>was heard</em></td>
    </tr>
  </table>
</div>

<hr class="section-break">
<h2>Passage D — Genesis 47:14, 31</h2>

<div class="passage-block">
  <span class="ref">47:14</span>
  <div class="hebrew">וַיְלַקֵּ֨ט יוֹסֵ֜ף אֶת־כָּל־הַכֶּ֗סֶף <strong>הַנִּמְצָ֤א</strong> בְאֶֽרֶץ־מִצְרַ֙יִם֙</div>
  <div class="english">"And Joseph collected all the silver [11] ____ in the land of Egypt."</div>
  <table>
    <tr>
      <th class="num-cell">#</th><th>Verb</th><th>Niphal?</th><th>Conjugation</th><th>PGN</th><th>Root</th><th>Stem / Function</th><th></th>
    </tr>
    <tr>
      <td class="num-cell">11</td>
      <td class="verb-cell">הַנִּמְצָא</td>
      <td><input class="parse-field" id="f11-nip" placeholder="Yes / No"></td>
      <td><input class="parse-field" id="f11-conj" placeholder="conjugation"></td>
      <td><input class="parse-field" id="f11-pgn" placeholder="PGN"></td>
      <td><input class="parse-field" id="f11-root" placeholder="root"></td>
      <td><input class="parse-field" id="f11-func" placeholder="function"></td>
      <td><button class="reveal-btn" onclick="toggleAnswer('a11',this)">▶ Answer</button></td>
    </tr>
    <tr class="answer-row" id="a11">
      <td class="answer-label">✓</td>
      <td class="verb-cell">הַנִּמְצָא</td>
      <td colspan="6">✓ <strong>Yes — Niphal</strong> | Participle ms | מָצָא | Passive — <em>that was found / which was found</em></td>
    </tr>
  </table>
</div>

<div class="passage-block">
  <span class="ref">47:31</span>
  <div class="hebrew"><strong>הִשָּׁ֣בְעָה</strong> לִ֔י <strong>וַיִּשָּׁבַ֖ע</strong> ל֑וֹ</div>
  <div class="english">"[12] ____ to me." And he [13] ____ to him."</div>
  <table>
    <tr>
      <th class="num-cell">#</th><th>Verb</th><th>Niphal?</th><th>Conjugation</th><th>PGN</th><th>Root</th><th>Stem / Function</th><th></th>
    </tr>
    <tr>
      <td class="num-cell">12</td>
      <td class="verb-cell">הִשָּׁבְעָה</td>
      <td><input class="parse-field" id="f12-nip" placeholder="Yes / No"></td>
      <td><input class="parse-field" id="f12-conj" placeholder="conjugation"></td>
      <td><input class="parse-field" id="f12-pgn" placeholder="PGN"></td>
      <td><input class="parse-field" id="f12-root" placeholder="root"></td>
      <td><input class="parse-field" id="f12-func" placeholder="function"></td>
      <td><button class="reveal-btn" onclick="toggleAnswer('a12',this)">▶ Answer</button></td>
    </tr>
    <tr class="answer-row" id="a12">
      <td class="answer-label">✓</td>
      <td class="verb-cell">הִשָּׁבְעָה</td>
      <td colspan="6">✓ <strong>Yes — Niphal</strong> | Imperative 2ms | שָׁבַע | Reflexive — <em>swear!</em> (bind yourself by oath)</td>
    </tr>
    <tr>
      <td class="num-cell">13</td>
      <td class="verb-cell">וַיִּשָּׁבַע</td>
      <td><input class="parse-field" id="f13-nip" placeholder="Yes / No"></td>
      <td><input class="parse-field" id="f13-conj" placeholder="conjugation"></td>
      <td><input class="parse-field" id="f13-pgn" placeholder="PGN"></td>
      <td><input class="parse-field" id="f13-root" placeholder="root"></td>
      <td><input class="parse-field" id="f13-func" placeholder="function"></td>
      <td><button class="reveal-btn" onclick="toggleAnswer('a13',this)">▶ Answer</button></td>
    </tr>
    <tr class="answer-row" id="a13">
      <td class="answer-label">✓</td>
      <td class="verb-cell">וַיִּשָּׁבַע</td>
      <td colspan="6">✓ <strong>Yes — Niphal</strong> | Wayyiqtol 3ms | שָׁבַע | Reflexive — <em>he swore</em> (bound himself by oath)</td>
    </tr>
  </table>
</div>

<hr class="section-break">
<h2>Passage E — Genesis 49:1–2, 29, 33</h2>

<div class="passage-block">
  <span class="ref">49:1</span>
  <div class="hebrew"><strong>הֵאָֽסְפוּ֙</strong> וְאַגִּ֣ידָה לָכֶ֔ם</div>
  <div class="english">"[14] ____ and I will tell you."</div>
  <table>
    <tr>
      <th class="num-cell">#</th><th>Verb</th><th>Niphal?</th><th>Conjugation</th><th>PGN</th><th>Root</th><th>Stem / Function</th><th></th>
    </tr>
    <tr>
      <td class="num-cell">14</td>
      <td class="verb-cell">הֵאָסְפוּ</td>
      <td><input class="parse-field" id="f14-nip" placeholder="Yes / No"></td>
      <td><input class="parse-field" id="f14-conj" placeholder="conjugation"></td>
      <td><input class="parse-field" id="f14-pgn" placeholder="PGN"></td>
      <td><input class="parse-field" id="f14-root" placeholder="root"></td>
      <td><input class="parse-field" id="f14-func" placeholder="function"></td>
      <td><button class="reveal-btn" onclick="toggleAnswer('a14',this)">▶ Answer</button></td>
    </tr>
    <tr class="answer-row" id="a14">
      <td class="answer-label">✓</td>
      <td class="verb-cell">הֵאָסְפוּ</td>
      <td colspan="6">✓ <strong>Yes — Niphal</strong> | Imperative 2mp | אָסַף | Passive — <em>gather yourselves!</em></td>
    </tr>
  </table>
</div>

<div class="passage-block">
  <span class="ref">49:29</span>
  <div class="hebrew">אֲנִ֖י <strong>נֶאֱסָ֣ף</strong> אֶל־עַמִּ֑י</div>
  <div class="english">"I am [15] ____ to my people."</div>
  <table>
    <tr>
      <th class="num-cell">#</th><th>Verb</th><th>Niphal?</th><th>Conjugation</th><th>PGN</th><th>Root</th><th>Stem / Function</th><th></th>
    </tr>
    <tr>
      <td class="num-cell">15</td>
      <td class="verb-cell">נֶאֱסָף</td>
      <td><input class="parse-field" id="f15-nip" placeholder="Yes / No"></td>
      <td><input class="parse-field" id="f15-conj" placeholder="conjugation"></td>
      <td><input class="parse-field" id="f15-pgn" placeholder="PGN"></td>
      <td><input class="parse-field" id="f15-root" placeholder="root"></td>
      <td><input class="parse-field" id="f15-func" placeholder="function"></td>
      <td><button class="reveal-btn" onclick="toggleAnswer('a15',this)">▶ Answer</button></td>
    </tr>
    <tr class="answer-row" id="a15">
      <td class="answer-label">✓</td>
      <td class="verb-cell">נֶאֱסָף</td>
      <td colspan="6">✓ <strong>Yes — Niphal</strong> | Participle ms | אָסַף | Passive — <em>am about to be gathered</em> (euphemism for dying)</td>
    </tr>
  </table>
</div>

<div class="passage-block">
  <span class="ref">49:33</span>
  <div class="hebrew"><strong>וַיֵּאָ֥סֶף</strong> אֶל־עַמָּיו֙</div>
  <div class="english">"and he was [16] ____ to his people."</div>
  <table>
    <tr>
      <th class="num-cell">#</th><th>Verb</th><th>Niphal?</th><th>Conjugation</th><th>PGN</th><th>Root</th><th>Stem / Function</th><th></th>
    </tr>
    <tr>
      <td class="num-cell">16</td>
      <td class="verb-cell">וַיֵּאָסֶף</td>
      <td><input class="parse-field" id="f16-nip" placeholder="Yes / No"></td>
      <td><input class="parse-field" id="f16-conj" placeholder="conjugation"></td>
      <td><input class="parse-field" id="f16-pgn" placeholder="PGN"></td>
      <td><input class="parse-field" id="f16-root" placeholder="root"></td>
      <td><input class="parse-field" id="f16-func" placeholder="function"></td>
      <td><button class="reveal-btn" onclick="toggleAnswer('a16',this)">▶ Answer</button></td>
    </tr>
    <tr class="answer-row" id="a16">
      <td class="answer-label">✓</td>
      <td class="verb-cell">וַיֵּאָסֶף</td>
      <td colspan="6">✓ <strong>Yes — Niphal</strong> | Wayyiqtol 3ms | אָסַף | Passive — <em>was gathered</em> (died and joined his ancestors)</td>
    </tr>
  </table>
</div>

<hr class="section-break">
<h2>Bonus — Exodus 19:12</h2>

<div class="passage-block">
  <span class="ref">19:12</span>
  <div class="hebrew"><strong>וְהִשָּׁמַרְתֶּ֥ם</strong> … <strong>הִשָּׁמְר֥וּ</strong> לָכֶ֛ם</div>
  <div class="english">"And you shall [B1] ____ … [B2] ____ for yourselves."</div>
  <table>
    <tr>
      <th class="num-cell">#</th><th>Verb</th><th>Niphal?</th><th>Conjugation</th><th>PGN</th><th>Root</th><th>Stem / Function</th><th></th>
    </tr>
    <tr>
      <td class="num-cell">B1</td>
      <td class="verb-cell">וְהִשָּׁמַרְתֶּם</td>
      <td><input class="parse-field" id="fb1-nip" placeholder="Yes / No"></td>
      <td><input class="parse-field" id="fb1-conj" placeholder="conjugation"></td>
      <td><input class="parse-field" id="fb1-pgn" placeholder="PGN"></td>
      <td><input class="parse-field" id="fb1-root" placeholder="root"></td>
      <td><input class="parse-field" id="fb1-func" placeholder="function"></td>
      <td><button class="reveal-btn" onclick="toggleAnswer('ab1',this)">▶ Answer</button></td>
    </tr>
    <tr class="answer-row" id="ab1">
      <td class="answer-label">✓</td>
      <td class="verb-cell">וְהִשָּׁמַרְתֶּם</td>
      <td colspan="6">✓ <strong>Yes — Niphal</strong> | Weqatal 2mp | שָׁמַר | Reflexive — <em>take heed for yourselves</em></td>
    </tr>
    <tr>
      <td class="num-cell">B2</td>
      <td class="verb-cell">הִשָּׁמְרוּ</td>
      <td><input class="parse-field" id="fb2-nip" placeholder="Yes / No"></td>
      <td><input class="parse-field" id="fb2-conj" placeholder="conjugation"></td>
      <td><input class="parse-field" id="fb2-pgn" placeholder="PGN"></td>
      <td><input class="parse-field" id="fb2-root" placeholder="root"></td>
      <td><input class="parse-field" id="fb2-func" placeholder="function"></td>
      <td><button class="reveal-btn" onclick="toggleAnswer('ab2',this)">▶ Answer</button></td>
    </tr>
    <tr class="answer-row" id="ab2">
      <td class="answer-label">✓</td>
      <td class="verb-cell">הִשָּׁמְרוּ</td>
      <td colspan="6">✓ <strong>Yes — Niphal</strong> | Imperative 2mp | שָׁמַר | Reflexive — <em>take heed!</em> (guard yourselves)</td>
    </tr>
  </table>
</div>

<div class="score-box">
  <strong>Score guide:</strong> 13 Niphal + 3 non-Niphal + 2 bonus = 18 total. 15–18 = excellent; 11–14 = review the paradigm; below 11 = revisit §24.3–24.13 before the next class.<br>
  <strong>Non-Niphal (3):</strong> #1 (Qal Perf 3fs), #3 (Qal Perf 3cp), #8 (Qal Perf 3ms)<br>
  <strong>Niphal pairs to note:</strong> #15–16 (נֶאֱסָף / וַיֵּאָסֶף), #12–13 (הִשָּׁבְעָה / וַיִּשָּׁבַע)
</div>

<div class="reflection">
  <strong>Reflection Questions</strong>
  <ol>
    <li>Several Niphal forms of אָסַף in this passage describe Jacob's death (Gen 49:29, 33). What does the passive "to be gathered to one's people" suggest about ancient Israelite views of death?</li>
    <li>In Gen 47:31, both הִשָּׁ֣בְעָה (#12, imperative) and וַיִּשָּׁבַע (#13, wayyiqtol) appear together. How does the narrative sequence reinforce the solemnity of Jacob's deathbed request?</li>
    <li>Compare נִצָּבָה (#2, Gen 37:7 — Reflexive: sheaf stands itself upright) with הַנִּצָּבִים (#9, Gen 45:1 — Reflexive participle: servants stationed before Joseph). Is the reflexive force the same in both? What does each communicate about agency?</li>
  </ol>
</div>

<script>
function toggleAnswer(id, btn) {
  const row = document.getElementById(id);
  const visible = row.style.display === 'table-row';
  row.style.display = visible ? 'none' : 'table-row';
  btn.textContent = visible ? '▶ Answer' : '▼ Answer';
  btn.classList.toggle('active', !visible);
}
function showAll() {
  document.querySelectorAll('.answer-row').forEach(r => r.style.display = 'table-row');
  document.querySelectorAll('.reveal-btn').forEach(b => { b.textContent = '▼ Answer'; b.classList.add('active'); });
}
function hideAll() {
  document.querySelectorAll('.answer-row').forEach(r => r.style.display = 'none');
  document.querySelectorAll('.reveal-btn').forEach(b => { b.textContent = '▶ Answer'; b.classList.remove('active'); });
}
function clearAll() {
  document.querySelectorAll('input.parse-field').forEach(i => i.value = '');
}
</script>

