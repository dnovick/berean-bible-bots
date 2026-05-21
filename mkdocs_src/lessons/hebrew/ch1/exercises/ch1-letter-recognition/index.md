# Letter Recognition

*Chapter 1 — Hebrew Alphabet*

[Full screen](ch1-letter-recognition.html){.md-button}  [Markdown](ch1-letter-recognition.md){.md-button}  [Print (PDF)](ch1-letter-recognition.pdf){.md-button}

<style>

  body { font-family: Georgia, serif;    color: #222; line-height: 1.6; }
  h1 { font-size: 1.45rem; border-bottom: 2px solid #555; padding-bottom: .4rem; }
  h2 { font-size: 1.05rem; margin-top: 2rem; color: #333; border-bottom: 1px solid #ddd; padding-bottom: .2rem; }
  .subtitle { color: #666; font-style: italic; margin-top: -.4rem; }
  .instructions { background: #f8f8f0; border-left: 4px solid #bbb; padding: .75rem 1rem; margin: 1rem 0; font-size: .92rem; }
  table { border-collapse: collapse;  margin: .4rem 0; font-size: .91rem; }
  th { background: #e0e8f0; padding: .4rem .55rem; border: 1px solid #bbb; text-align: left; font-size: .84rem; }
  td { padding: .3rem .45rem; border: 1px solid #ddd; vertical-align: middle; }
  td.num { text-align: center; font-weight: bold; color: #666; width: 2.2rem; }
  td.heb { direction: rtl; unicode-bidi: embed; font-size: 2em; font-weight: bold; width: 3.5rem; text-align: center; }
  input.f { width: 100%; box-sizing: border-box; border: 1px solid #bbb; border-radius: 3px; padding: .22rem .4rem; font-family: Georgia, serif; font-size: .87rem; background: #fafff8; }
  input.f:focus { outline: none; border-color: #5a9; box-shadow: 0 0 0 2px #c8ecd4; }
  .ans-row { display: none; background: #f0faf0; }
  .ans-row td { font-size: .87rem; color: #2a6e2a; padding: .28rem .45rem; }
  .ans-lbl { font-weight: bold; color: #1a5c1a; width: 2.2rem; text-align: center; }
  .ans-heb { direction: rtl; unicode-bidi: embed; font-size: 1.5em; font-weight: bold; width: 3.5rem; text-align: center; }
  button.rbtn { font-size: .76rem; padding: .14rem .48rem; cursor: pointer; background: #e8f4ec; border: 1px solid #7bba8f; border-radius: 3px; color: #2a6e2a; white-space: nowrap; }
  button.rbtn:hover, button.rbtn.on { background: #c8ecd4; }
  .controls { display: flex; gap: .7rem; flex-wrap: wrap; margin: 1rem 0 1.5rem; }
  .controls button { padding: .38rem .85rem; cursor: pointer; border-radius: 4px; font-size: .88rem; border: 1px solid #999; background: #f0f0f0; color: #333; }
  .controls button:hover { background: #ddd; }
  .clr { border-color: #c06060 !important; color: #8b0000 !important; background: #fff0f0 !important; }
  .clr:hover { background: #ffd8d8 !important; }
  hr.sec { border: none; border-top: 2px dashed #ccc; margin: 2rem 0; }
  .reflect { background: #f4f0ff; border-left: 4px solid #9988cc; padding: .75rem 1rem; margin: 1.5rem 0; font-size: .92rem; }
  .reflect ol { margin: .4rem 0 0 1.2rem; padding: 0; }
  .reflect li { margin-bottom: .5rem; }
  @media print {
    .controls, button.rbtn { display: none; }
    input.f { border: none; border-bottom: 1px solid #aaa; border-radius: 0; background: transparent; }
    .ans-row { display: none !important; }
  }

</style>

<h1>Chapter 1 — Hebrew Letter Recognition Exercise</h1>
<p class="subtitle">BBH Chapter 1 · Hebrew Alphabet · 30 items</p>

<div class="instructions">
  <strong>Instructions:</strong> For each Hebrew letter shown, identify: (1) Letter Name, (2) Transliteration, (3) Sound, (4) Special Category (guttural / begadkephat / sofit form / normal).<br>
  <em>Parts A–B: standard letters and sofit forms. Part C: begadkephat letters shown with dagesh lene — describe the hard pronunciation.</em>
</div>

<div class="controls">
  <button onclick="showAll()">Show All Answers</button>
  <button onclick="hideAll()">Hide All Answers</button>
  <button class="clr" onclick="clearAll()">Clear All Inputs</button>
</div>

<!-- PART A -->
<h2>Part A — Standard Letters (1–22)</h2>
<div style="overflow-x:auto;max-width:100%;"><table>
  <tr><th>#</th><th>Letter</th><th>Name</th><th>Transliteration</th><th>Sound</th><th>Special Category</th><th></th></tr>

  <tr><td class="num">1</td><td class="heb">א</td><td><input class="parse-field" id="1-name" placeholder="letter name"></td><td><input class="parse-field" id="1-trans" placeholder="transliteration"></td><td><input class="parse-field" id="1-sound" placeholder="sound"></td><td><input class="parse-field" id="1-cat" placeholder="category"></td><td><button class="rbtn" onclick="tog(1)">▶ Answer</button></td></tr>
  <tr class="ans-row" id="ans-1"><td class="ans-lbl">✓</td><td class="ans-heb">א</td><td colspan="5">Aleph · ʾ · Silent / glottal stop · <strong>Guttural; quiescent</strong></td></tr>

  <tr><td class="num">2</td><td class="heb">ב</td><td><input class="parse-field" id="2-name" placeholder="letter name"></td><td><input class="parse-field" id="2-trans" placeholder="transliteration"></td><td><input class="parse-field" id="2-sound" placeholder="sound"></td><td><input class="parse-field" id="2-cat" placeholder="category"></td><td><button class="rbtn" onclick="tog(2)">▶ Answer</button></td></tr>
  <tr class="ans-row" id="ans-2"><td class="ans-lbl">✓</td><td class="ans-heb">ב</td><td colspan="5">Beth · b / v · b (hard) or v (soft) · <strong>Begadkephat</strong> (soft form — no dagesh)</td></tr>

  <tr><td class="num">3</td><td class="heb">ג</td><td><input class="parse-field" id="3-name" placeholder="letter name"></td><td><input class="parse-field" id="3-trans" placeholder="transliteration"></td><td><input class="parse-field" id="3-sound" placeholder="sound"></td><td><input class="parse-field" id="3-cat" placeholder="category"></td><td><button class="rbtn" onclick="tog(3)">▶ Answer</button></td></tr>
  <tr class="ans-row" id="ans-3"><td class="ans-lbl">✓</td><td class="ans-heb">ג</td><td colspan="5">Gimel · g / gh · g (hard) or gh (soft) · <strong>Begadkephat</strong> (soft rarely distinguished today)</td></tr>

  <tr><td class="num">4</td><td class="heb">ד</td><td><input class="parse-field" id="4-name" placeholder="letter name"></td><td><input class="parse-field" id="4-trans" placeholder="transliteration"></td><td><input class="parse-field" id="4-sound" placeholder="sound"></td><td><input class="parse-field" id="4-cat" placeholder="category"></td><td><button class="rbtn" onclick="tog(4)">▶ Answer</button></td></tr>
  <tr class="ans-row" id="ans-4"><td class="ans-lbl">✓</td><td class="ans-heb">ד</td><td colspan="5">Dalet · d / dh · d (hard) or dh (soft) · <strong>Begadkephat</strong> (soft rarely distinguished today)</td></tr>

  <tr><td class="num">5</td><td class="heb">ה</td><td><input class="parse-field" id="5-name" placeholder="letter name"></td><td><input class="parse-field" id="5-trans" placeholder="transliteration"></td><td><input class="parse-field" id="5-sound" placeholder="sound"></td><td><input class="parse-field" id="5-cat" placeholder="category"></td><td><button class="rbtn" onclick="tog(5)">▶ Answer</button></td></tr>
  <tr class="ans-row" id="ans-5"><td class="ans-lbl">✓</td><td class="ans-heb">ה</td><td colspan="5">He · h · h · <strong>Guttural</strong>; often quiescent word-finally</td></tr>

  <tr><td class="num">6</td><td class="heb">ו</td><td><input class="parse-field" id="6-name" placeholder="letter name"></td><td><input class="parse-field" id="6-trans" placeholder="transliteration"></td><td><input class="parse-field" id="6-sound" placeholder="sound"></td><td><input class="parse-field" id="6-cat" placeholder="category"></td><td><button class="rbtn" onclick="tog(6)">▶ Answer</button></td></tr>
  <tr class="ans-row" id="ans-6"><td class="ans-lbl">✓</td><td class="ans-heb">ו</td><td colspan="5">Waw · w · w (consonantal) · <strong>Normal</strong>; also mater lectionis (vowel letter for ō, û)</td></tr>

  <tr><td class="num">7</td><td class="heb">ז</td><td><input class="parse-field" id="7-name" placeholder="letter name"></td><td><input class="parse-field" id="7-trans" placeholder="transliteration"></td><td><input class="parse-field" id="7-sound" placeholder="sound"></td><td><input class="parse-field" id="7-cat" placeholder="category"></td><td><button class="rbtn" onclick="tog(7)">▶ Answer</button></td></tr>
  <tr class="ans-row" id="ans-7"><td class="ans-lbl">✓</td><td class="ans-heb">ז</td><td colspan="5">Zayin · z · z · <strong>Normal</strong></td></tr>

  <tr><td class="num">8</td><td class="heb">ח</td><td><input class="parse-field" id="8-name" placeholder="letter name"></td><td><input class="parse-field" id="8-trans" placeholder="transliteration"></td><td><input class="parse-field" id="8-sound" placeholder="sound"></td><td><input class="parse-field" id="8-cat" placeholder="category"></td><td><button class="rbtn" onclick="tog(8)">▶ Answer</button></td></tr>
  <tr class="ans-row" id="ans-8"><td class="ans-lbl">✓</td><td class="ans-heb">ח</td><td colspan="5">Cheth · ḥ · ch as in German Bach · <strong>Guttural</strong>; cannot take Dagesh Forte</td></tr>

  <tr><td class="num">9</td><td class="heb">ט</td><td><input class="parse-field" id="9-name" placeholder="letter name"></td><td><input class="parse-field" id="9-trans" placeholder="transliteration"></td><td><input class="parse-field" id="9-sound" placeholder="sound"></td><td><input class="parse-field" id="9-cat" placeholder="category"></td><td><button class="rbtn" onclick="tog(9)">▶ Answer</button></td></tr>
  <tr class="ans-row" id="ans-9"><td class="ans-lbl">✓</td><td class="ans-heb">ט</td><td colspan="5">Teth · ṭ · emphatic t (no English equivalent) · <strong>Normal</strong> (emphatic series)</td></tr>

  <tr><td class="num">10</td><td class="heb">י</td><td><input class="parse-field" id="10-name" placeholder="letter name"></td><td><input class="parse-field" id="10-trans" placeholder="transliteration"></td><td><input class="parse-field" id="10-sound" placeholder="sound"></td><td><input class="parse-field" id="10-cat" placeholder="category"></td><td><button class="rbtn" onclick="tog(10)">▶ Answer</button></td></tr>
  <tr class="ans-row" id="ans-10"><td class="ans-lbl">✓</td><td class="ans-heb">י</td><td colspan="5">Yod · y · y as in yes (consonantal) · <strong>Normal</strong>; also mater lectionis (vowel letter for ī, ê)</td></tr>

  <tr><td class="num">11</td><td class="heb">כ</td><td><input class="parse-field" id="11-name" placeholder="letter name"></td><td><input class="parse-field" id="11-trans" placeholder="transliteration"></td><td><input class="parse-field" id="11-sound" placeholder="sound"></td><td><input class="parse-field" id="11-cat" placeholder="category"></td><td><button class="rbtn" onclick="tog(11)">▶ Answer</button></td></tr>
  <tr class="ans-row" id="ans-11"><td class="ans-lbl">✓</td><td class="ans-heb">כ</td><td colspan="5">Kaph · k / kh · k (hard) or kh as in Bach (soft) · <strong>Begadkephat</strong>; has sofit form (ך)</td></tr>

  <tr><td class="num">12</td><td class="heb">ל</td><td><input class="parse-field" id="12-name" placeholder="letter name"></td><td><input class="parse-field" id="12-trans" placeholder="transliteration"></td><td><input class="parse-field" id="12-sound" placeholder="sound"></td><td><input class="parse-field" id="12-cat" placeholder="category"></td><td><button class="rbtn" onclick="tog(12)">▶ Answer</button></td></tr>
  <tr class="ans-row" id="ans-12"><td class="ans-lbl">✓</td><td class="ans-heb">ל</td><td colspan="5">Lamed · l · l · <strong>Normal</strong></td></tr>

  <tr><td class="num">13</td><td class="heb">מ</td><td><input class="parse-field" id="13-name" placeholder="letter name"></td><td><input class="parse-field" id="13-trans" placeholder="transliteration"></td><td><input class="parse-field" id="13-sound" placeholder="sound"></td><td><input class="parse-field" id="13-cat" placeholder="category"></td><td><button class="rbtn" onclick="tog(13)">▶ Answer</button></td></tr>
  <tr class="ans-row" id="ans-13"><td class="ans-lbl">✓</td><td class="ans-heb">מ</td><td colspan="5">Mem · m · m · <strong>Normal</strong>; has sofit form (ם)</td></tr>

  <tr><td class="num">14</td><td class="heb">נ</td><td><input class="parse-field" id="14-name" placeholder="letter name"></td><td><input class="parse-field" id="14-trans" placeholder="transliteration"></td><td><input class="parse-field" id="14-sound" placeholder="sound"></td><td><input class="parse-field" id="14-cat" placeholder="category"></td><td><button class="rbtn" onclick="tog(14)">▶ Answer</button></td></tr>
  <tr class="ans-row" id="ans-14"><td class="ans-lbl">✓</td><td class="ans-heb">נ</td><td colspan="5">Nun · n · n · <strong>Normal</strong>; has sofit form (ן)</td></tr>

  <tr><td class="num">15</td><td class="heb">ס</td><td><input class="parse-field" id="15-name" placeholder="letter name"></td><td><input class="parse-field" id="15-trans" placeholder="transliteration"></td><td><input class="parse-field" id="15-sound" placeholder="sound"></td><td><input class="parse-field" id="15-cat" placeholder="category"></td><td><button class="rbtn" onclick="tog(15)">▶ Answer</button></td></tr>
  <tr class="ans-row" id="ans-15"><td class="ans-lbl">✓</td><td class="ans-heb">ס</td><td colspan="5">Samech · s · s · <strong>Normal</strong></td></tr>

  <tr><td class="num">16</td><td class="heb">ע</td><td><input class="parse-field" id="16-name" placeholder="letter name"></td><td><input class="parse-field" id="16-trans" placeholder="transliteration"></td><td><input class="parse-field" id="16-sound" placeholder="sound"></td><td><input class="parse-field" id="16-cat" placeholder="category"></td><td><button class="rbtn" onclick="tog(16)">▶ Answer</button></td></tr>
  <tr class="ans-row" id="ans-16"><td class="ans-lbl">✓</td><td class="ans-heb">ע</td><td colspan="5">Ayin · ʿ · Silent / pharyngeal (distinct from Aleph) · <strong>Guttural</strong>; cannot take Dagesh Forte</td></tr>

  <tr><td class="num">17</td><td class="heb">פ</td><td><input class="parse-field" id="17-name" placeholder="letter name"></td><td><input class="parse-field" id="17-trans" placeholder="transliteration"></td><td><input class="parse-field" id="17-sound" placeholder="sound"></td><td><input class="parse-field" id="17-cat" placeholder="category"></td><td><button class="rbtn" onclick="tog(17)">▶ Answer</button></td></tr>
  <tr class="ans-row" id="ans-17"><td class="ans-lbl">✓</td><td class="ans-heb">פ</td><td colspan="5">Pe · p / f · p (hard) or f (soft) · <strong>Begadkephat</strong>; has sofit form (ף)</td></tr>

  <tr><td class="num">18</td><td class="heb">צ</td><td><input class="parse-field" id="18-name" placeholder="letter name"></td><td><input class="parse-field" id="18-trans" placeholder="transliteration"></td><td><input class="parse-field" id="18-sound" placeholder="sound"></td><td><input class="parse-field" id="18-cat" placeholder="category"></td><td><button class="rbtn" onclick="tog(18)">▶ Answer</button></td></tr>
  <tr class="ans-row" id="ans-18"><td class="ans-lbl">✓</td><td class="ans-heb">צ</td><td colspan="5">Tsade · ṣ · emphatic ts · <strong>Normal</strong> (emphatic series); has sofit form (ץ)</td></tr>

  <tr><td class="num">19</td><td class="heb">ק</td><td><input class="parse-field" id="19-name" placeholder="letter name"></td><td><input class="parse-field" id="19-trans" placeholder="transliteration"></td><td><input class="parse-field" id="19-sound" placeholder="sound"></td><td><input class="parse-field" id="19-cat" placeholder="category"></td><td><button class="rbtn" onclick="tog(19)">▶ Answer</button></td></tr>
  <tr class="ans-row" id="ans-19"><td class="ans-lbl">✓</td><td class="ans-heb">ק</td><td colspan="5">Qoph · q · q (uvular, deeper than k) · <strong>Normal</strong></td></tr>

  <tr><td class="num">20</td><td class="heb">ר</td><td><input class="parse-field" id="20-name" placeholder="letter name"></td><td><input class="parse-field" id="20-trans" placeholder="transliteration"></td><td><input class="parse-field" id="20-sound" placeholder="sound"></td><td><input class="parse-field" id="20-cat" placeholder="category"></td><td><button class="rbtn" onclick="tog(20)">▶ Answer</button></td></tr>
  <tr class="ans-row" id="ans-20"><td class="ans-lbl">✓</td><td class="ans-heb">ר</td><td colspan="5">Resh · r · r (uvular) · <strong>Behaves like guttural</strong> in some contexts; resists Dagesh Forte</td></tr>

  <tr><td class="num">21</td><td class="heb">שׁ</td><td><input class="parse-field" id="21-name" placeholder="letter name"></td><td><input class="parse-field" id="21-trans" placeholder="transliteration"></td><td><input class="parse-field" id="21-sound" placeholder="sound"></td><td><input class="parse-field" id="21-cat" placeholder="category"></td><td><button class="rbtn" onclick="tog(21)">▶ Answer</button></td></tr>
  <tr class="ans-row" id="ans-21"><td class="ans-lbl">✓</td><td class="ans-heb">שׁ</td><td colspan="5">Shin · š · sh as in sheep · <strong>Normal</strong> (shin dot on right; sin dot on left = שׂ = s)</td></tr>

  <tr><td class="num">22</td><td class="heb">ת</td><td><input class="parse-field" id="22-name" placeholder="letter name"></td><td><input class="parse-field" id="22-trans" placeholder="transliteration"></td><td><input class="parse-field" id="22-sound" placeholder="sound"></td><td><input class="parse-field" id="22-cat" placeholder="category"></td><td><button class="rbtn" onclick="tog(22)">▶ Answer</button></td></tr>
  <tr class="ans-row" id="ans-22"><td class="ans-lbl">✓</td><td class="ans-heb">ת</td><td colspan="5">Taw · t / th · t (hard) or th as in the (soft) · <strong>Begadkephat</strong></td></tr>
</table></div>

<hr class="sec">

<!-- PART B -->
<h2>Part B — Final (Sofit) Forms (23–27)</h2>
<p style="font-size:.9rem;color:#444">Each of these letters appears only at the end of a word. Identify the letter, give its name (include "sofit"), its transliteration, sound, and note it as a sofit form.</p>
<div style="overflow-x:auto;max-width:100%;"><table>
  <tr><th>#</th><th>Letter</th><th>Name</th><th>Transliteration</th><th>Sound</th><th>Special Category</th><th></th></tr>

  <tr><td class="num">23</td><td class="heb">ך</td><td><input class="parse-field" id="23-name" placeholder="letter name"></td><td><input class="parse-field" id="23-trans" placeholder="transliteration"></td><td><input class="parse-field" id="23-sound" placeholder="sound"></td><td><input class="parse-field" id="23-cat" placeholder="category"></td><td><button class="rbtn" onclick="tog(23)">▶ Answer</button></td></tr>
  <tr class="ans-row" id="ans-23"><td class="ans-lbl">✓</td><td class="ans-heb">ך</td><td colspan="5">Kaph sofit · k / kh · k (hard) or kh (soft) · <strong>Sofit form</strong> of כ — word-final only</td></tr>

  <tr><td class="num">24</td><td class="heb">ם</td><td><input class="parse-field" id="24-name" placeholder="letter name"></td><td><input class="parse-field" id="24-trans" placeholder="transliteration"></td><td><input class="parse-field" id="24-sound" placeholder="sound"></td><td><input class="parse-field" id="24-cat" placeholder="category"></td><td><button class="rbtn" onclick="tog(24)">▶ Answer</button></td></tr>
  <tr class="ans-row" id="ans-24"><td class="ans-lbl">✓</td><td class="ans-heb">ם</td><td colspan="5">Mem sofit · m · m · <strong>Sofit form</strong> of מ — word-final only; closed square shape</td></tr>

  <tr><td class="num">25</td><td class="heb">ן</td><td><input class="parse-field" id="25-name" placeholder="letter name"></td><td><input class="parse-field" id="25-trans" placeholder="transliteration"></td><td><input class="parse-field" id="25-sound" placeholder="sound"></td><td><input class="parse-field" id="25-cat" placeholder="category"></td><td><button class="rbtn" onclick="tog(25)">▶ Answer</button></td></tr>
  <tr class="ans-row" id="ans-25"><td class="ans-lbl">✓</td><td class="ans-heb">ן</td><td colspan="5">Nun sofit · n · n · <strong>Sofit form</strong> of נ — word-final only; long descending stroke</td></tr>

  <tr><td class="num">26</td><td class="heb">ף</td><td><input class="parse-field" id="26-name" placeholder="letter name"></td><td><input class="parse-field" id="26-trans" placeholder="transliteration"></td><td><input class="parse-field" id="26-sound" placeholder="sound"></td><td><input class="parse-field" id="26-cat" placeholder="category"></td><td><button class="rbtn" onclick="tog(26)">▶ Answer</button></td></tr>
  <tr class="ans-row" id="ans-26"><td class="ans-lbl">✓</td><td class="ans-heb">ף</td><td colspan="5">Pe sofit · p / f · p (hard) or f (soft) · <strong>Sofit form</strong> of פ — word-final only; also begadkephat</td></tr>

  <tr><td class="num">27</td><td class="heb">ץ</td><td><input class="parse-field" id="27-name" placeholder="letter name"></td><td><input class="parse-field" id="27-trans" placeholder="transliteration"></td><td><input class="parse-field" id="27-sound" placeholder="sound"></td><td><input class="parse-field" id="27-cat" placeholder="category"></td><td><button class="rbtn" onclick="tog(27)">▶ Answer</button></td></tr>
  <tr class="ans-row" id="ans-27"><td class="ans-lbl">✓</td><td class="ans-heb">ץ</td><td colspan="5">Tsade sofit · ṣ · emphatic ts · <strong>Sofit form</strong> of צ — word-final only; long descending tail</td></tr>
</table></div>

<hr class="sec">

<!-- PART C -->
<h2>Part C — Begadkephat Letters with Dagesh Lene (28–30)</h2>
<p style="font-size:.9rem;color:#444">Each letter below carries a dagesh lene (dot inside). Identify the letter name, transliteration, sound (hard pronunciation), and note it as begadkephat with dagesh lene.</p>
<div style="overflow-x:auto;max-width:100%;"><table>
  <tr><th>#</th><th>Letter</th><th>Name</th><th>Transliteration</th><th>Sound</th><th>Special Category</th><th></th></tr>

  <tr><td class="num">28</td><td class="heb">בּ</td><td><input class="parse-field" id="28-name" placeholder="letter name"></td><td><input class="parse-field" id="28-trans" placeholder="transliteration"></td><td><input class="parse-field" id="28-sound" placeholder="sound"></td><td><input class="parse-field" id="28-cat" placeholder="category"></td><td><button class="rbtn" onclick="tog(28)">▶ Answer</button></td></tr>
  <tr class="ans-row" id="ans-28"><td class="ans-lbl">✓</td><td class="ans-heb">בּ</td><td colspan="5">Beth (with dagesh lene) · b · b as in boy — hard stop · <strong>Begadkephat</strong> — dagesh lene = hard pronunciation</td></tr>

  <tr><td class="num">29</td><td class="heb">כּ</td><td><input class="parse-field" id="29-name" placeholder="letter name"></td><td><input class="parse-field" id="29-trans" placeholder="transliteration"></td><td><input class="parse-field" id="29-sound" placeholder="sound"></td><td><input class="parse-field" id="29-cat" placeholder="category"></td><td><button class="rbtn" onclick="tog(29)">▶ Answer</button></td></tr>
  <tr class="ans-row" id="ans-29"><td class="ans-lbl">✓</td><td class="ans-heb">כּ</td><td colspan="5">Kaph (with dagesh lene) · k · k as in king — hard stop · <strong>Begadkephat</strong> — dagesh lene = hard pronunciation</td></tr>

  <tr><td class="num">30</td><td class="heb">פּ</td><td><input class="parse-field" id="30-name" placeholder="letter name"></td><td><input class="parse-field" id="30-trans" placeholder="transliteration"></td><td><input class="parse-field" id="30-sound" placeholder="sound"></td><td><input class="parse-field" id="30-cat" placeholder="category"></td><td><button class="rbtn" onclick="tog(30)">▶ Answer</button></td></tr>
  <tr class="ans-row" id="ans-30"><td class="ans-lbl">✓</td><td class="ans-heb">פּ</td><td colspan="5">Pe (with dagesh lene) · p · p as in pan — hard stop · <strong>Begadkephat</strong> — dagesh lene = hard pronunciation</td></tr>
</table></div>

<hr class="sec">

<!-- Reflection -->
<h2>Reflection Questions</h2>
<div class="reflect">
  <ol>
    <li><strong>Sofit recognition:</strong> You encounter a word ending in what looks like an unfamiliar letter — a long downward stroke. How do you determine whether this is a final nun (ן) or final kaph (ך), and what does your identification tell you about the letter's base form?</li>
    <li><strong>Guttural behavior preview:</strong> Your textbook states that א and ע "cannot take Dagesh Forte." Based on what you know about guttural letters, why do you think a guttural would resist the doubling that dagesh forte produces? How might this affect vowel patterns in surrounding syllables?</li>
    <li><strong>Consonant vs. vowel letter:</strong> The letter ו appears in the middle of a word carrying a shureq dot (וּ). Is ו functioning as a consonant or as a mater lectionis in that position? What clue does the placement of the dot give you?</li>
  </ol>
</div>

<script>
  const ids = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30];
  function tog(id) {
    const r = document.getElementById('ans-' + id);
    const b = r.previousElementSibling.querySelector('button');
    const v = r.style.display === 'table-row';
    r.style.display = v ? 'none' : 'table-row';
    b.textContent = v ? '▶ Answer' : '▼ Hide';
    b.classList.toggle('on', !v);
  }
  function showAll() {
    ids.forEach(id => {
      const r = document.getElementById('ans-' + id);
      const b = r.previousElementSibling.querySelector('button');
      r.style.display = 'table-row';
      b.textContent = '▼ Hide';
      b.classList.add('on');
    });
  }
  function hideAll() {
    ids.forEach(id => {
      const r = document.getElementById('ans-' + id);
      const b = r.previousElementSibling.querySelector('button');
      r.style.display = 'none';
      b.textContent = '▶ Answer';
      b.classList.remove('on');
    });
  }
  function clearAll() {
    document.querySelectorAll('input.f').forEach(e => e.value = '');
  }
</script>

