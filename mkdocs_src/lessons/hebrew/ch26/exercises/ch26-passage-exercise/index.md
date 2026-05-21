# Passage Exercise

*Chapter 26 — Hiphil Strong*

[Full screen](ch26-passage-exercise.html){.md-button}  [Markdown](ch26-passage-exercise.md){.md-button}  [Print (PDF)](ch26-passage-exercise.pdf){.md-button}

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
  .watchout { background: #fff8e1; border-left: 3px solid #f0a500; padding: .5rem .75rem; margin: .4rem 0; font-size: .9rem; }
  table { border-collapse: collapse;  margin: .5rem 0; font-size: .92rem; }
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
  .answer-row td .answer-hebrew { font-size: 1rem; direction: rtl; unicode-bidi: embed; }
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
  .coverage-table th { background: #ddeeff; }
  .note-box { background: #fff8e8; border: 1px solid #e0c060; border-radius: 4px; padding: .6rem .9rem; margin: 1rem 0; font-size: .88rem; }
  .reflection { margin-top: 1.5rem; }
  .reflection ol li { margin-bottom: .75rem; }
  @media print {
    .controls, button.reveal-btn { display: none; }
    input.parse-field { border: none; border-bottom: 1px solid #aaa; border-radius: 0; background: transparent; }
    .answer-row { display: none !important; }
  }

</style>

<h1>Chapter 26 — "Spot the Hiphil" Passage Exercise</h1>
<p class="subtitle">Genesis 6–8 · Genesis 22 · Deuteronomy 7</p>

<div class="instructions">
  <strong>Instructions:</strong> For each numbered verb, answer <strong>Is it Hiphil? (Yes / No)</strong>. Then for every verb:
  <ol style="margin:.4rem 0 0">
    <li>Parse it — give the <strong>conjugation</strong>, <strong>PGN</strong> (use — for non-finite forms), and <strong>root</strong>.</li>
    <li>State the <strong>semantic function</strong> (Causative / Declarative / Factitive / Simple action — or "NOT Hiphil" for distractors).</li>
  </ol>
  Distractors (#1, #18, #22) include Niphal and Qal verbs from the same passages. Click <strong>▶ Answer</strong> on any row to reveal the correct parsing inline.
</div>

<div class="controls">
  <button onclick="showAll()">Show All Answers</button>
  <button onclick="hideAll()">Hide All Answers</button>
  <button class="clear-btn" onclick="clearAll()">Clear All Inputs</button>
</div>

<!-- ═══════════════════════════════════════════════════════ PASSAGE A -->
<h2>Passage A — Genesis 6:12–20</h2>

<!-- Verb 1 (distractor) + Verb 2 -->
<div class="passage-block">
  <span class="ref">6:12</span>
  <div class="hebrew">וַיַּ֧רְא אֱלֹהִ֛ים אֶת־הָאָ֖רֶץ וְהִנֵּ֣ה <strong>נִשְׁחָ֑תָה</strong> כִּֽי־<strong>הִשְׁחִ֧ית</strong> כָּל־בָּשָׂ֛ר אֶת־דַּרְכּ֖וֹ עַל־הָאָֽרֶץ</div>
  <div class="english">"And God saw the earth, and behold, it [1] ____; for all flesh had [2] ____ its way upon the earth."</div>
  <div style="overflow-x:auto;max-width:100%;"><table>
    <tr><th style="width:2.5rem">#</th><th style="width:8rem">Verb</th><th style="width:6rem">Hiphil?</th><th>Conjugation</th><th style="width:6rem">PGN</th><th style="width:7rem">Root</th><th>Stem / Function</th><th style="width:5.5rem"></th></tr>
    <tr>
      <td class="num-cell">1</td>
      <td class="verb-cell">נִשְׁחָתָה</td>
      <td><input class="parse-field" id="d1-hip" placeholder="Yes / No"></td>
      <td><input class="parse-field" id="d1-conj" placeholder="conjugation"></td>
      <td><input class="parse-field" id="d1-pgn" placeholder="PGN"></td>
      <td><input class="parse-field" id="d1-root" placeholder="root"></td>
      <td><input class="parse-field" id="d1-func" placeholder="function"></td>
      <td><button class="reveal-btn" onclick="toggle('d1')">▶ Answer</button></td>
    </tr>
    <tr class="answer-row wrong" id="ans-d1">
      <td class="answer-label">✗</td>
      <td class="answer-hebrew">נִשְׁחָתָה</td>
      <td colspan="6">✗ <strong>No — Niphal</strong> | Weqatal 3fs | שָׁחַת | NOT Hiphil — Niphal passive: <em>was corrupt</em>; נ assimilates: Niphal weqatal passive</td>
    </tr>
    <tr>
      <td class="num-cell">2</td>
      <td class="verb-cell">הִשְׁחִית</td>
      <td><input class="parse-field" id="2-hip" placeholder="Yes / No"></td>
      <td><input class="parse-field" id="2-conj" placeholder="conjugation"></td>
      <td><input class="parse-field" id="2-pgn" placeholder="PGN"></td>
      <td><input class="parse-field" id="2-root" placeholder="root"></td>
      <td><input class="parse-field" id="2-func" placeholder="function"></td>
      <td><button class="reveal-btn" onclick="toggle(2)">▶ Answer</button></td>
    </tr>
    <tr class="answer-row" id="ans-2">
      <td class="answer-label">✓</td>
      <td class="answer-hebrew">הִשְׁחִית</td>
      <td colspan="6">✓ <strong>Yes — Hiphil</strong> | Perfect (qatal) 3ms | שָׁחַת | Causative — <em>had corrupted</em></td>
    </tr>
  </table></div>
</div>

<!-- Verb 3 -->
<div class="passage-block">
  <span class="ref">6:13</span>
  <div class="hebrew">הִנְנִ֤י <strong>מַשְׁחִיתָם֙</strong> עִם־הָאָ֔רֶץ</div>
  <div class="english">"Behold, I am [3] ____ them with the earth."</div>
  <div style="overflow-x:auto;max-width:100%;"><table>
    <tr><th style="width:2.5rem">#</th><th style="width:8rem">Verb</th><th style="width:6rem">Hiphil?</th><th>Conjugation</th><th style="width:6rem">PGN</th><th style="width:7rem">Root</th><th>Stem / Function</th><th style="width:5.5rem"></th></tr>
    <tr>
      <td class="num-cell">3</td>
      <td class="verb-cell">מַשְׁחִיתָם</td>
      <td><input class="parse-field" id="3-hip" placeholder="Yes / No"></td>
      <td><input class="parse-field" id="3-conj" placeholder="conjugation"></td>
      <td><input class="parse-field" id="3-pgn" placeholder="PGN"></td>
      <td><input class="parse-field" id="3-root" placeholder="root"></td>
      <td><input class="parse-field" id="3-func" placeholder="function"></td>
      <td><button class="reveal-btn" onclick="toggle(3)">▶ Answer</button></td>
    </tr>
    <tr class="answer-row" id="ans-3">
      <td class="answer-label">✓</td>
      <td class="answer-hebrew">מַשְׁחִיתָם</td>
      <td colspan="6">✓ <strong>Yes — Hiphil</strong> | Participle + 3mp suffix ms | שָׁחַת | Causative — <em>destroying them</em></td>
    </tr>
  </table></div>
</div>

<!-- Verb 4 -->
<div class="passage-block">
  <span class="ref">6:17</span>
  <div class="hebrew">וַאֲנִ֗י הִנְנִ֤י <strong>מֵבִיא֙</strong> אֶת־הַמַּבּ֣וּל מַ֔יִם עַל־הָאָ֖רֶץ</div>
  <div class="english">"As for me, behold, I am [4] ____ the flood of waters upon the earth."</div>
  <div style="overflow-x:auto;max-width:100%;"><table>
    <tr><th style="width:2.5rem">#</th><th style="width:8rem">Verb</th><th style="width:6rem">Hiphil?</th><th>Conjugation</th><th style="width:6rem">PGN</th><th style="width:7rem">Root</th><th>Stem / Function</th><th style="width:5.5rem"></th></tr>
    <tr>
      <td class="num-cell">4</td>
      <td class="verb-cell">מֵבִיא</td>
      <td><input class="parse-field" id="4-hip" placeholder="Yes / No"></td>
      <td><input class="parse-field" id="4-conj" placeholder="conjugation"></td>
      <td><input class="parse-field" id="4-pgn" placeholder="PGN"></td>
      <td><input class="parse-field" id="4-root" placeholder="root"></td>
      <td><input class="parse-field" id="4-func" placeholder="function"></td>
      <td><button class="reveal-btn" onclick="toggle(4)">▶ Answer</button></td>
    </tr>
    <tr class="answer-row" id="ans-4">
      <td class="answer-label">✓</td>
      <td class="answer-hebrew">מֵבִיא</td>
      <td colspan="6">✓ <strong>Yes — Hiphil</strong> | Participle ms | בּוֹא | Causative — <em>bringing</em></td>
    </tr>
  </table></div>
</div>

<!-- Verb 5 -->
<div class="passage-block">
  <span class="ref">6:18</span>
  <div class="hebrew">וַהֲקִמֹתִ֥י אֶת־בְּרִיתִ֖י אִתָּ֑ךְ</div>
  <div class="english">"But I will [5] ____ my covenant with you."</div>
  <div style="overflow-x:auto;max-width:100%;"><table>
    <tr><th style="width:2.5rem">#</th><th style="width:8rem">Verb</th><th style="width:6rem">Hiphil?</th><th>Conjugation</th><th style="width:6rem">PGN</th><th style="width:7rem">Root</th><th>Stem / Function</th><th style="width:5.5rem"></th></tr>
    <tr>
      <td class="num-cell">5</td>
      <td class="verb-cell">וַהֲקִמֹתִי</td>
      <td><input class="parse-field" id="5-hip" placeholder="Yes / No"></td>
      <td><input class="parse-field" id="5-conj" placeholder="conjugation"></td>
      <td><input class="parse-field" id="5-pgn" placeholder="PGN"></td>
      <td><input class="parse-field" id="5-root" placeholder="root"></td>
      <td><input class="parse-field" id="5-func" placeholder="function"></td>
      <td><button class="reveal-btn" onclick="toggle(5)">▶ Answer</button></td>
    </tr>
    <tr class="answer-row" id="ans-5">
      <td class="answer-label">✓</td>
      <td class="answer-hebrew">וַהֲקִמֹתִי</td>
      <td colspan="6">✓ <strong>Yes — Hiphil</strong> | Weqatal 1cs | קוּם | Factitive — <em>I will establish</em></td>
    </tr>
  </table></div>
</div>

<!-- Verb 6 -->
<div class="passage-block">
  <span class="ref">6:19</span>
  <div class="hebrew">מִכָּל־בָּשָׂר֙ שְׁנַ֣יִם מִכֹּ֔ל <strong>תָּבִ֥יא</strong> אֶל־הַתֵּבָ֖ה</div>
  <div class="english">"Of every living thing of all flesh, you shall [6] ____ two of every kind into the ark."</div>
  <div style="overflow-x:auto;max-width:100%;"><table>
    <tr><th style="width:2.5rem">#</th><th style="width:8rem">Verb</th><th style="width:6rem">Hiphil?</th><th>Conjugation</th><th style="width:6rem">PGN</th><th style="width:7rem">Root</th><th>Stem / Function</th><th style="width:5.5rem"></th></tr>
    <tr>
      <td class="num-cell">6</td>
      <td class="verb-cell">תָּבִיא</td>
      <td><input class="parse-field" id="6-hip" placeholder="Yes / No"></td>
      <td><input class="parse-field" id="6-conj" placeholder="conjugation"></td>
      <td><input class="parse-field" id="6-pgn" placeholder="PGN"></td>
      <td><input class="parse-field" id="6-root" placeholder="root"></td>
      <td><input class="parse-field" id="6-func" placeholder="function"></td>
      <td><button class="reveal-btn" onclick="toggle(6)">▶ Answer</button></td>
    </tr>
    <tr class="answer-row" id="ans-6">
      <td class="answer-label">✓</td>
      <td class="answer-hebrew">תָּבִיא</td>
      <td colspan="6">✓ <strong>Yes — Hiphil</strong> | Imperfect 2ms | בּוֹא | Causative — <em>you shall bring</em></td>
    </tr>
  </table></div>
</div>

<!-- Verbs 7–8 -->
<div class="passage-block">
  <span class="ref">6:19–20</span>
  <div class="hebrew">לְ<strong>הַחֲיֹת֙</strong> אִתָּֽךְ … לְ<strong>הַחֲיֽוֹת</strong></div>
  <div class="english">"to [7] ____ them alive with you … to [8] ____ them"</div>
  <div style="overflow-x:auto;max-width:100%;"><table>
    <tr><th style="width:2.5rem">#</th><th style="width:8rem">Verb</th><th style="width:6rem">Hiphil?</th><th>Conjugation</th><th style="width:6rem">PGN</th><th style="width:7rem">Root</th><th>Stem / Function</th><th style="width:5.5rem"></th></tr>
    <tr>
      <td class="num-cell">7</td>
      <td class="verb-cell">לְהַחֲיֹת</td>
      <td><input class="parse-field" id="7-hip" placeholder="Yes / No"></td>
      <td><input class="parse-field" id="7-conj" placeholder="conjugation"></td>
      <td><input class="parse-field" id="7-pgn" placeholder="PGN"></td>
      <td><input class="parse-field" id="7-root" placeholder="root"></td>
      <td><input class="parse-field" id="7-func" placeholder="function"></td>
      <td><button class="reveal-btn" onclick="toggle(7)">▶ Answer</button></td>
    </tr>
    <tr class="answer-row" id="ans-7">
      <td class="answer-label">✓</td>
      <td class="answer-hebrew">לְהַחֲיֹת</td>
      <td colspan="6">✓ <strong>Yes — Hiphil</strong> | Inf. Construct — | חָיָה | Causative — <em>to keep alive</em></td>
    </tr>
    <tr>
      <td class="num-cell">8</td>
      <td class="verb-cell">לְהַחֲיוֹת</td>
      <td><input class="parse-field" id="8-hip" placeholder="Yes / No"></td>
      <td><input class="parse-field" id="8-conj" placeholder="conjugation"></td>
      <td><input class="parse-field" id="8-pgn" placeholder="PGN"></td>
      <td><input class="parse-field" id="8-root" placeholder="root"></td>
      <td><input class="parse-field" id="8-func" placeholder="function"></td>
      <td><button class="reveal-btn" onclick="toggle(8)">▶ Answer</button></td>
    </tr>
    <tr class="answer-row" id="ans-8">
      <td class="answer-label">✓</td>
      <td class="answer-hebrew">לְהַחֲיוֹת</td>
      <td colspan="6">✓ <strong>Yes — Hiphil</strong> | Inf. Construct — | חָיָה | Causative — <em>to keep alive</em></td>
    </tr>
  </table></div>
</div>

<hr class="section-break">

<!-- ═══════════════════════════════════════════════════════ PASSAGE B -->
<h2>Passage B — Genesis 7:4</h2>

<div class="passage-block">
  <span class="ref">7:4</span>
  <div class="hebrew">כִּ֣י לְיָמִ֗ים ע֚וֹד שִׁבְעָ֔ה אָנֹכִ֥י <strong>מַמְטִ֣יר</strong> עַל־הָאָ֑רֶץ אַרְבָּעִ֣ים י֔וֹם</div>
  <div class="english">"For in seven days I will [9] ____ rain on the earth forty days."</div>
  <div style="overflow-x:auto;max-width:100%;"><table>
    <tr><th style="width:2.5rem">#</th><th style="width:8rem">Verb</th><th style="width:6rem">Hiphil?</th><th>Conjugation</th><th style="width:6rem">PGN</th><th style="width:7rem">Root</th><th>Stem / Function</th><th style="width:5.5rem"></th></tr>
    <tr>
      <td class="num-cell">9</td>
      <td class="verb-cell">מַמְטִיר</td>
      <td><input class="parse-field" id="9-hip" placeholder="Yes / No"></td>
      <td><input class="parse-field" id="9-conj" placeholder="conjugation"></td>
      <td><input class="parse-field" id="9-pgn" placeholder="PGN"></td>
      <td><input class="parse-field" id="9-root" placeholder="root"></td>
      <td><input class="parse-field" id="9-func" placeholder="function"></td>
      <td><button class="reveal-btn" onclick="toggle(9)">▶ Answer</button></td>
    </tr>
    <tr class="answer-row" id="ans-9">
      <td class="answer-label">✓</td>
      <td class="answer-hebrew">מַמְטִיר</td>
      <td colspan="6">✓ <strong>Yes — Hiphil</strong> | Participle ms | מָטַר | Causative/Denominative — <em>causing rain to fall</em></td>
    </tr>
  </table></div>
</div>

<hr class="section-break">

<!-- ═══════════════════════════════════════════════════════ PASSAGE C -->
<h2>Passage C — Genesis 8:1–21</h2>

<div class="passage-block">
  <span class="ref">8:1</span>
  <div class="hebrew">וַיַּ֤עֲבֵר אֱלֹהִים֙ ר֣וּחַ עַל־הָאָ֔רֶץ</div>
  <div class="english">"And God [10] ____ a wind over the earth."</div>
  <div style="overflow-x:auto;max-width:100%;"><table>
    <tr><th style="width:2.5rem">#</th><th style="width:8rem">Verb</th><th style="width:6rem">Hiphil?</th><th>Conjugation</th><th style="width:6rem">PGN</th><th style="width:7rem">Root</th><th>Stem / Function</th><th style="width:5.5rem"></th></tr>
    <tr>
      <td class="num-cell">10</td>
      <td class="verb-cell">וַיַּעֲבֵר</td>
      <td><input class="parse-field" id="10-hip" placeholder="Yes / No"></td>
      <td><input class="parse-field" id="10-conj" placeholder="conjugation"></td>
      <td><input class="parse-field" id="10-pgn" placeholder="PGN"></td>
      <td><input class="parse-field" id="10-root" placeholder="root"></td>
      <td><input class="parse-field" id="10-func" placeholder="function"></td>
      <td><button class="reveal-btn" onclick="toggle(10)">▶ Answer</button></td>
    </tr>
    <tr class="answer-row" id="ans-10">
      <td class="answer-label">✓</td>
      <td class="answer-hebrew">וַיַּעֲבֵר</td>
      <td colspan="6">✓ <strong>Yes — Hiphil</strong> | Wayyiqtol 3ms | עָבַר | Causative — <em>caused to pass over</em></td>
    </tr>
  </table></div>
</div>

<div class="passage-block">
  <span class="ref">8:9</span>
  <div class="hebrew">וַיָּבֵ֥א אֹתָ֛הּ אֵלָ֖יו אֶל־הַתֵּבָ֑ה</div>
  <div class="english">"And he [11] ____ her back to him into the ark."</div>
  <div style="overflow-x:auto;max-width:100%;"><table>
    <tr><th style="width:2.5rem">#</th><th style="width:8rem">Verb</th><th style="width:6rem">Hiphil?</th><th>Conjugation</th><th style="width:6rem">PGN</th><th style="width:7rem">Root</th><th>Stem / Function</th><th style="width:5.5rem"></th></tr>
    <tr>
      <td class="num-cell">11</td>
      <td class="verb-cell">וַיָּבֵא</td>
      <td><input class="parse-field" id="11-hip" placeholder="Yes / No"></td>
      <td><input class="parse-field" id="11-conj" placeholder="conjugation"></td>
      <td><input class="parse-field" id="11-pgn" placeholder="PGN"></td>
      <td><input class="parse-field" id="11-root" placeholder="root"></td>
      <td><input class="parse-field" id="11-func" placeholder="function"></td>
      <td><button class="reveal-btn" onclick="toggle(11)">▶ Answer</button></td>
    </tr>
    <tr class="answer-row" id="ans-11">
      <td class="answer-label">✓</td>
      <td class="answer-hebrew">וַיָּבֵא</td>
      <td colspan="6">✓ <strong>Yes — Hiphil</strong> | Wayyiqtol 3ms | בּוֹא | Causative — <em>brought</em></td>
    </tr>
  </table></div>
</div>

<div class="passage-block">
  <span class="ref">8:13</span>
  <div class="hebrew">וַיָּ֤סַר נֹ֙חַ֙ אֶת־מִכְסֵ֣ה הַתֵּבָ֔ה</div>
  <div class="english">"And Noah [12] ____ the covering of the ark."</div>
  <div style="overflow-x:auto;max-width:100%;"><table>
    <tr><th style="width:2.5rem">#</th><th style="width:8rem">Verb</th><th style="width:6rem">Hiphil?</th><th>Conjugation</th><th style="width:6rem">PGN</th><th style="width:7rem">Root</th><th>Stem / Function</th><th style="width:5.5rem"></th></tr>
    <tr>
      <td class="num-cell">12</td>
      <td class="verb-cell">וַיָּסַר</td>
      <td><input class="parse-field" id="12-hip" placeholder="Yes / No"></td>
      <td><input class="parse-field" id="12-conj" placeholder="conjugation"></td>
      <td><input class="parse-field" id="12-pgn" placeholder="PGN"></td>
      <td><input class="parse-field" id="12-root" placeholder="root"></td>
      <td><input class="parse-field" id="12-func" placeholder="function"></td>
      <td><button class="reveal-btn" onclick="toggle(12)">▶ Answer</button></td>
    </tr>
    <tr class="answer-row" id="ans-12">
      <td class="answer-label">✓</td>
      <td class="answer-hebrew">וַיָּסַר</td>
      <td colspan="6">✓ <strong>Yes — Hiphil</strong> | Wayyiqtol 3ms | סוּר | Causative — <em>removed</em></td>
    </tr>
  </table></div>
</div>

<div class="passage-block">
  <span class="ref">8:17</span>
  <div class="hebrew"><strong>הַיְצֵ֣א</strong> אִתָּ֗ךְ כָּל־הַחַיָּ֤ה</div>
  <div class="english">"[13] ____ with you every living thing."</div>
  <div style="overflow-x:auto;max-width:100%;"><table>
    <tr><th style="width:2.5rem">#</th><th style="width:8rem">Verb</th><th style="width:6rem">Hiphil?</th><th>Conjugation</th><th style="width:6rem">PGN</th><th style="width:7rem">Root</th><th>Stem / Function</th><th style="width:5.5rem"></th></tr>
    <tr>
      <td class="num-cell">13</td>
      <td class="verb-cell">הַיְצֵא</td>
      <td><input class="parse-field" id="13-hip" placeholder="Yes / No"></td>
      <td><input class="parse-field" id="13-conj" placeholder="conjugation"></td>
      <td><input class="parse-field" id="13-pgn" placeholder="PGN"></td>
      <td><input class="parse-field" id="13-root" placeholder="root"></td>
      <td><input class="parse-field" id="13-func" placeholder="function"></td>
      <td><button class="reveal-btn" onclick="toggle(13)">▶ Answer</button></td>
    </tr>
    <tr class="answer-row" id="ans-13">
      <td class="answer-label">✓</td>
      <td class="answer-hebrew">הַיְצֵא</td>
      <td colspan="6">✓ <strong>Yes — Hiphil</strong> | Imperative 2ms | יָצָא | Causative — <em>bring out!</em></td>
    </tr>
  </table></div>
</div>

<div class="passage-block">
  <span class="ref">8:20</span>
  <div class="hebrew">וַיַּ֥עַל עֹלֹ֖ת בַּמִּזְבֵּֽחַ</div>
  <div class="english">"And he [14] ____ burnt offerings on the altar."</div>
  <div style="overflow-x:auto;max-width:100%;"><table>
    <tr><th style="width:2.5rem">#</th><th style="width:8rem">Verb</th><th style="width:6rem">Hiphil?</th><th>Conjugation</th><th style="width:6rem">PGN</th><th style="width:7rem">Root</th><th>Stem / Function</th><th style="width:5.5rem"></th></tr>
    <tr>
      <td class="num-cell">14</td>
      <td class="verb-cell">וַיַּעַל</td>
      <td><input class="parse-field" id="14-hip" placeholder="Yes / No"></td>
      <td><input class="parse-field" id="14-conj" placeholder="conjugation"></td>
      <td><input class="parse-field" id="14-pgn" placeholder="PGN"></td>
      <td><input class="parse-field" id="14-root" placeholder="root"></td>
      <td><input class="parse-field" id="14-func" placeholder="function"></td>
      <td><button class="reveal-btn" onclick="toggle(14)">▶ Answer</button></td>
    </tr>
    <tr class="answer-row" id="ans-14">
      <td class="answer-label">✓</td>
      <td class="answer-hebrew">וַיַּעַל</td>
      <td colspan="6">✓ <strong>Yes — Hiphil</strong> | Wayyiqtol 3ms | עָלָה | Causative — <em>offered up</em></td>
    </tr>
  </table></div>
</div>

<div class="passage-block">
  <span class="ref">8:21</span>
  <div class="hebrew">לֹֽא־אֹ֠סִף לְ<strong>הַכֹּ֨ת</strong> אֶת־כָּל־חַ֜י</div>
  <div class="english">"I will never again [15] ____ every living thing."</div>
  <div style="overflow-x:auto;max-width:100%;"><table>
    <tr><th style="width:2.5rem">#</th><th style="width:8rem">Verb</th><th style="width:6rem">Hiphil?</th><th>Conjugation</th><th style="width:6rem">PGN</th><th style="width:7rem">Root</th><th>Stem / Function</th><th style="width:5.5rem"></th></tr>
    <tr>
      <td class="num-cell">15</td>
      <td class="verb-cell">לְהַכֹּת</td>
      <td><input class="parse-field" id="15-hip" placeholder="Yes / No"></td>
      <td><input class="parse-field" id="15-conj" placeholder="conjugation"></td>
      <td><input class="parse-field" id="15-pgn" placeholder="PGN"></td>
      <td><input class="parse-field" id="15-root" placeholder="root"></td>
      <td><input class="parse-field" id="15-func" placeholder="function"></td>
      <td><button class="reveal-btn" onclick="toggle(15)">▶ Answer</button></td>
    </tr>
    <tr class="answer-row" id="ans-15">
      <td class="answer-label">✓</td>
      <td class="answer-hebrew">לְהַכֹּת</td>
      <td colspan="6">✓ <strong>Yes — Hiphil</strong> | Inf. Construct — | נָכָה | Causative — <em>to strike down</em></td>
    </tr>
  </table></div>
</div>

<hr class="section-break">

<!-- ═══════════════════════════════════════════════════════ PASSAGE D -->
<h2>Passage D — Genesis 22:17 <span style="font-weight:normal;font-size:.9rem">(Infinitive Absolute)</span></h2>

<div class="passage-block">
  <span class="ref">22:17</span>
  <div class="hebrew">כִּי בָרֵ֣ךְ אֲבָרֶכְךָ֗ <strong>וְהַרְבָּ֨ה</strong> <strong>אַרְבֶּ֤ה</strong> אֶת־זַרְעֲךָ֙ כְּכוֹכְבֵ֣י הַשָּׁמַ֔יִם</div>
  <div class="english">"For I will surely bless you, and I will [16] ____ [17] ____ your offspring as the stars of heaven."</div>
  <div class="watchout">⚠ <strong>Watch out:</strong> בָּרֵךְ and אֲבָרֶכְךָ are Piel forms of בָּרַךְ ("to bless") — not Hiphil. Parse only the two bolded verbs.</div>
  <div style="overflow-x:auto;max-width:100%;"><table>
    <tr><th style="width:2.5rem">#</th><th style="width:8rem">Verb</th><th style="width:6rem">Hiphil?</th><th>Conjugation</th><th style="width:6rem">PGN</th><th style="width:7rem">Root</th><th>Stem / Function</th><th style="width:5.5rem"></th></tr>
    <tr>
      <td class="num-cell">16</td>
      <td class="verb-cell">וְהַרְבָּה</td>
      <td><input class="parse-field" id="16-hip" placeholder="Yes / No"></td>
      <td><input class="parse-field" id="16-conj" placeholder="conjugation"></td>
      <td><input class="parse-field" id="16-pgn" placeholder="PGN"></td>
      <td><input class="parse-field" id="16-root" placeholder="root"></td>
      <td><input class="parse-field" id="16-func" placeholder="function"></td>
      <td><button class="reveal-btn" onclick="toggle(16)">▶ Answer</button></td>
    </tr>
    <tr class="answer-row" id="ans-16">
      <td class="answer-label">✓</td>
      <td class="answer-hebrew">וְהַרְבָּה</td>
      <td colspan="6">✓ <strong>Yes — Hiphil</strong> | Inf. Absolute — | רָבָה | Causative — emphatic modifier (<em>multiplying / surely</em>)</td>
    </tr>
    <tr>
      <td class="num-cell">17</td>
      <td class="verb-cell">אַרְבֶּה</td>
      <td><input class="parse-field" id="17-hip" placeholder="Yes / No"></td>
      <td><input class="parse-field" id="17-conj" placeholder="conjugation"></td>
      <td><input class="parse-field" id="17-pgn" placeholder="PGN"></td>
      <td><input class="parse-field" id="17-root" placeholder="root"></td>
      <td><input class="parse-field" id="17-func" placeholder="function"></td>
      <td><button class="reveal-btn" onclick="toggle(17)">▶ Answer</button></td>
    </tr>
    <tr class="answer-row" id="ans-17">
      <td class="answer-label">✓</td>
      <td class="answer-hebrew">אַרְבֶּה</td>
      <td colspan="6">✓ <strong>Yes — Hiphil</strong> | Imperfect 1cs | רָבָה | Causative — <em>I will multiply</em></td>
    </tr>
  </table></div>
</div>

<hr class="section-break">

<!-- ═══════════════════════════════════════════════════════ PASSAGE E -->
<h2>Passage E — Deuteronomy 7:2 <span style="font-weight:normal;font-size:.9rem">(Weqatal + Emphatic Pair)</span></h2>

<div class="passage-block">
  <span class="ref">7:2</span>
  <div class="hebrew"><strong>וּנְתָנָ֞ם</strong> יְהוָ֤ה אֱלֹהֶ֙יךָ֙ לְפָנֶ֔יךָ <strong>וְהִכִּיתָ֖ם</strong> <strong>הַכֵּ֣ה</strong> <strong>תַכֶּ֑ה</strong> לֹא־<strong>תִכְרֹ֥ת</strong> לָהֶ֛ם בְּרִ֖ית</div>
  <div class="english">"When the LORD your God [18] ____ them over to you, you shall [19] ____ them — [20] ____ [21] ____ them — you shall [22] ____ no covenant with them."</div>
  <div style="overflow-x:auto;max-width:100%;"><table>
    <tr><th style="width:2.5rem">#</th><th style="width:8rem">Verb</th><th style="width:6rem">Hiphil?</th><th>Conjugation</th><th style="width:6rem">PGN</th><th style="width:7rem">Root</th><th>Stem / Function</th><th style="width:5.5rem"></th></tr>
    <tr>
      <td class="num-cell">18</td>
      <td class="verb-cell">וּנְתָנָם</td>
      <td><input class="parse-field" id="d2-hip" placeholder="Yes / No"></td>
      <td><input class="parse-field" id="d2-conj" placeholder="conjugation"></td>
      <td><input class="parse-field" id="d2-pgn" placeholder="PGN"></td>
      <td><input class="parse-field" id="d2-root" placeholder="root"></td>
      <td><input class="parse-field" id="d2-func" placeholder="function"></td>
      <td><button class="reveal-btn" onclick="toggle('d2')">▶ Answer</button></td>
    </tr>
    <tr class="answer-row wrong" id="ans-d2">
      <td class="answer-label">✗</td>
      <td class="answer-hebrew">וּנְתָנָם</td>
      <td colspan="6">✗ <strong>No — Qal</strong> | Perfect + 3mp suffix 3ms | נָתַן | NOT Hiphil — Qal: <em>gives them over</em>; Qal perfect of נָתַן with object suffix</td>
    </tr>
    <tr>
      <td class="num-cell">19</td>
      <td class="verb-cell">וְהִכִּיתָם</td>
      <td><input class="parse-field" id="19-hip" placeholder="Yes / No"></td>
      <td><input class="parse-field" id="19-conj" placeholder="conjugation"></td>
      <td><input class="parse-field" id="19-pgn" placeholder="PGN"></td>
      <td><input class="parse-field" id="19-root" placeholder="root"></td>
      <td><input class="parse-field" id="19-func" placeholder="function"></td>
      <td><button class="reveal-btn" onclick="toggle(19)">▶ Answer</button></td>
    </tr>
    <tr class="answer-row" id="ans-19">
      <td class="answer-label">✓</td>
      <td class="answer-hebrew">וְהִכִּיתָם</td>
      <td colspan="6">✓ <strong>Yes — Hiphil</strong> | Weqatal 2ms | נָכָה | Causative — <em>and you shall strike them</em></td>
    </tr>
    <tr>
      <td class="num-cell">20</td>
      <td class="verb-cell">הַכֵּה</td>
      <td><input class="parse-field" id="20-hip" placeholder="Yes / No"></td>
      <td><input class="parse-field" id="20-conj" placeholder="conjugation"></td>
      <td><input class="parse-field" id="20-pgn" placeholder="PGN"></td>
      <td><input class="parse-field" id="20-root" placeholder="root"></td>
      <td><input class="parse-field" id="20-func" placeholder="function"></td>
      <td><button class="reveal-btn" onclick="toggle(20)">▶ Answer</button></td>
    </tr>
    <tr class="answer-row" id="ans-20">
      <td class="answer-label">✓</td>
      <td class="answer-hebrew">הַכֵּה</td>
      <td colspan="6">✓ <strong>Yes — Hiphil</strong> | Inf. Absolute — | נָכָה | Causative — emphatic modifier (<em>striking / certainly</em>)</td>
    </tr>
    <tr>
      <td class="num-cell">21</td>
      <td class="verb-cell">תַכֶּה</td>
      <td><input class="parse-field" id="21-hip" placeholder="Yes / No"></td>
      <td><input class="parse-field" id="21-conj" placeholder="conjugation"></td>
      <td><input class="parse-field" id="21-pgn" placeholder="PGN"></td>
      <td><input class="parse-field" id="21-root" placeholder="root"></td>
      <td><input class="parse-field" id="21-func" placeholder="function"></td>
      <td><button class="reveal-btn" onclick="toggle(21)">▶ Answer</button></td>
    </tr>
    <tr class="answer-row" id="ans-21">
      <td class="answer-label">✓</td>
      <td class="answer-hebrew">תַכֶּה</td>
      <td colspan="6">✓ <strong>Yes — Hiphil</strong> | Imperfect 2ms | נָכָה | Causative — <em>you shall strike</em></td>
    </tr>
    <tr>
      <td class="num-cell">22</td>
      <td class="verb-cell">תִכְרֹת</td>
      <td><input class="parse-field" id="d3-hip" placeholder="Yes / No"></td>
      <td><input class="parse-field" id="d3-conj" placeholder="conjugation"></td>
      <td><input class="parse-field" id="d3-pgn" placeholder="PGN"></td>
      <td><input class="parse-field" id="d3-root" placeholder="root"></td>
      <td><input class="parse-field" id="d3-func" placeholder="function"></td>
      <td><button class="reveal-btn" onclick="toggle('d3')">▶ Answer</button></td>
    </tr>
    <tr class="answer-row wrong" id="ans-d3">
      <td class="answer-label">✗</td>
      <td class="answer-hebrew">תִכְרֹת</td>
      <td colspan="6">✗ <strong>No — Qal</strong> | Imperfect 2ms | כָּרַת | NOT Hiphil — Qal: <em>you shall make</em> (covenant); plain Qal imperfect; no הִ prefix</td>
    </tr>
  </table></div>
</div>

<hr class="section-break">

<!-- ═══════════════════════════════════════════════════════ BONUS -->
<h2>Bonus — Genesis 6:1, 6:10</h2>

<div class="passage-block">
  <span class="ref">6:1</span>
  <div class="hebrew">כִּֽי־<strong>הֵחֵ֣ל</strong> הָאָדָ֔ם לָרֹ֖ב</div>
  <div class="english">"When man began to multiply…"</div>
  <span class="ref" style="margin-top:.8rem">6:10</span>
  <div class="hebrew">וַיּ֥וֹלֶד נֹ֖חַ שְׁלֹשָׁ֣ה בָנִ֑ים</div>
  <div class="english">"And Noah fathered three sons."</div>
  <div style="overflow-x:auto;max-width:100%;"><table>
    <tr><th style="width:2.5rem">#</th><th style="width:8rem">Verb</th><th style="width:6rem">Hiphil?</th><th>Conjugation</th><th style="width:6rem">PGN</th><th style="width:7rem">Root</th><th>Stem / Function</th><th style="width:5.5rem"></th></tr>
    <tr>
      <td class="num-cell">B1</td>
      <td class="verb-cell">הֵחֵל</td>
      <td><input class="parse-field" id="b1-hip" placeholder="Yes / No"></td>
      <td><input class="parse-field" id="b1-conj" placeholder="conjugation"></td>
      <td><input class="parse-field" id="b1-pgn" placeholder="PGN"></td>
      <td><input class="parse-field" id="b1-root" placeholder="root"></td>
      <td><input class="parse-field" id="b1-func" placeholder="function"></td>
      <td><button class="reveal-btn" onclick="toggle('b1')">▶ Answer</button></td>
    </tr>
    <tr class="answer-row" id="ans-b1">
      <td class="answer-label">✓</td>
      <td class="answer-hebrew">הֵחֵל</td>
      <td colspan="6">✓ <strong>Yes — Hiphil</strong> | Perfect (qatal) 3ms | חָלַל | Causative — <em>began</em> (Hiphil of חָלַל = "to begin"; idiomatic)</td>
    </tr>
    <tr>
      <td class="num-cell">B2</td>
      <td class="verb-cell">וַיּוֹלֶד</td>
      <td><input class="parse-field" id="b2-hip" placeholder="Yes / No"></td>
      <td><input class="parse-field" id="b2-conj" placeholder="conjugation"></td>
      <td><input class="parse-field" id="b2-pgn" placeholder="PGN"></td>
      <td><input class="parse-field" id="b2-root" placeholder="root"></td>
      <td><input class="parse-field" id="b2-func" placeholder="function"></td>
      <td><button class="reveal-btn" onclick="toggle('b2')">▶ Answer</button></td>
    </tr>
    <tr class="answer-row" id="ans-b2">
      <td class="answer-label">✓</td>
      <td class="answer-hebrew">וַיּוֹלֶד</td>
      <td colspan="6">✓ <strong>Yes — Hiphil</strong> | Wayyiqtol 3ms | יָלַד | Causative — <em>fathered / begat</em></td>
    </tr>
  </table></div>
</div>

<hr class="section-break">

<!-- ═══════════════════════════════════════════════════════ NOTES & COVERAGE -->
<div class="note-box">
  <strong>Answer-key notes:</strong><br>
  • #2 הִשְׁחִית and B1 הֵחֵל are <strong>Perfect (qatal)</strong>, not Weqatal — both follow כִּי with no waw prefix.<br>
  • #1 נִשְׁחָתָה is Niphal (passive); #2 הִשְׁחִית is Hiphil (active causative) — same root שָׁחַת, different stems in the same verse.<br>
  • #16–17 and #20–21 illustrate the <strong>emphatic inf. absolute + imperfect</strong> construction: the inf. absolute intensifies the following finite verb ("shall <em>certainly</em> strike").
</div>

<div class="score-box">
  <strong>Score:</strong> 19 Hiphil + 3 non-Hiphil + 2 bonus = 24 total (distractors #1, #18, #22 are unscored practice). &nbsp;
  21–24 = excellent &nbsp;|&nbsp; 16–20 = review the paradigm &nbsp;|&nbsp; below 16 = revisit §26.3–26.13
</div>

<h2>Conjugation Coverage</h2>
<div style="overflow-x:auto;max-width:100%;"><table class="coverage-table">
  <tr><th>Conjugation</th><th>Verbs</th></tr>
  <tr><td>Wayyiqtol (5)</td><td>#10, #11, #12, #14, B2</td></tr>
  <tr><td>Inf. Construct (3)</td><td>#7, #8, #15</td></tr>
  <tr><td>Participle (3)</td><td>#3, #4, #9</td></tr>
  <tr><td>Imperfect (3)</td><td>#6, #17, #21</td></tr>
  <tr><td>Perfect / qatal (2)</td><td>#2, B1</td></tr>
  <tr><td>Weqatal (2)</td><td>#5, #19</td></tr>
  <tr><td>Inf. Absolute (2)</td><td>#16, #20</td></tr>
  <tr><td>Imperative (1)</td><td>#13</td></tr>
  <tr><td>Non-Hiphil (3)</td><td>#1 (Niphal Weqatal 3fs), #18 (Qal Weqatal 3ms), #22 (Qal Imperfect 2ms)</td></tr>
</table></div>

<!-- ═══════════════════════════════════════════════════════ REFLECTION -->
<div class="reflection">
  <h2>Reflection Questions</h2>
  <ol>
    <li>Wayyiqtol dominates in Gen 6–8 but is absent from Passages D and E. What does this tell you about how genre — narrative vs. divine oracle (Gen 22) vs. legal instruction (Deut 7) — shapes conjugation choice in the Hiphil?</li>
    <li>Both Passage D (Gen 22:17) and Passage E (Deut 7:2) use the emphatic inf. absolute + imperfect pattern. What does the inf. absolute add beyond a plain imperfect? Are the two contexts — promise and command — using the emphasis for the same rhetorical purpose?</li>
    <li>In Gen 6–8, God is the subject of nearly every Hiphil; Noah appears as subject only at #12 and #14. What does this distribution of agency tell you about the theological architecture of the flood narrative?</li>
  </ol>
</div>

<script>
  const ids = [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,19,20,21,'b1','b2','d1','d2','d3'];

  function toggle(id) {
    const row = document.getElementById('ans-' + id);
    const btn = row.previousElementSibling.querySelector('button');
    const visible = row.style.display === 'table-row';
    row.style.display = visible ? 'none' : 'table-row';
    btn.textContent = visible ? '▶ Answer' : '▼ Hide';
    btn.classList.toggle('active', !visible);
  }

  function showAll() {
    ids.forEach(id => {
      const row = document.getElementById('ans-' + id);
      const btn = row.previousElementSibling.querySelector('button');
      row.style.display = 'table-row';
      btn.textContent = '▼ Hide';
      btn.classList.add('active');
    });
  }

  function hideAll() {
    ids.forEach(id => {
      const row = document.getElementById('ans-' + id);
      const btn = row.previousElementSibling.querySelector('button');
      row.style.display = 'none';
      btn.textContent = '▶ Answer';
      btn.classList.remove('active');
    });
  }

  function clearAll() {
    document.querySelectorAll('input.parse-field').forEach(el => el.value = '');
  }
</script>

