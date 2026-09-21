# Hithpael Root Frequencies

<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+Hebrew:wght@400;600&display=swap">

<style>
.hf-intro { margin-bottom: 1.25rem; }
.hf-search-wrap { margin-bottom: 1rem; }
#hf-search {
  width: 100%; max-width: 320px;
  padding: 7px 12px;
  border: 1.5px solid var(--md-default-fg-color--lightest, #e0e0e0);
  border-radius: 6px;
  font-size: 14px;
  background: var(--md-default-bg-color, #fff);
  color: var(--md-default-fg-color, #333);
}
#hf-search:focus { outline: none; border-color: var(--md-accent-fg-color, #7b5abf); }
#hf-table { width: 100%; border-collapse: collapse; font-size: 14px; }
#hf-table thead th {
  text-align: left; padding: 6px 10px;
  border-bottom: 2px solid var(--md-default-fg-color--lightest, #ddd);
  font-size: 11px; font-weight: 600;
  letter-spacing: 0.08em; text-transform: uppercase;
  color: var(--md-default-fg-color--light, #777);
  white-space: nowrap;
}
#hf-table tbody tr { border-bottom: 1px solid var(--md-default-fg-color--lightest, #eee); }
#hf-table tbody tr:hover { background: var(--md-accent-fg-color--transparent, #f3f0fa); }
#hf-table td { padding: 8px 10px; vertical-align: middle; }
.hf-rank {
  font-size: 11px; font-weight: 600;
  color: var(--md-accent-fg-color, #5f3ea8);
  background: var(--md-accent-fg-color--transparent, #eee8f8);
  border-radius: 4px; padding: 2px 6px;
  font-variant-numeric: tabular-nums;
}
.hf-root-cell { display: flex; flex-direction: column; gap: 1px; min-width: 80px; }
.hf-root {
  font-family: 'Noto Serif Hebrew', 'SBL Hebrew', 'Times New Roman', serif;
  font-size: 22px; font-weight: 600; line-height: 1.1;
  direction: rtl; unicode-bidi: embed;
}
.hf-lemma {
  font-family: 'Noto Serif Hebrew', 'SBL Hebrew', 'Times New Roman', serif;
  font-size: 13px; color: var(--md-default-fg-color--light, #777);
  direction: rtl; unicode-bidi: embed;
}
.hf-count {
  font-size: 16px; font-weight: 700;
  font-variant-numeric: tabular-nums; min-width: 40px;
}
.hf-bar-track {
  height: 5px; background: var(--md-default-fg-color--lightest, #e5e0f0);
  border-radius: 3px; overflow: hidden; min-width: 80px;
}
.hf-bar-fill { height: 100%; background: var(--md-accent-fg-color, #7b5abf); border-radius: 3px; }
.hf-pct { font-size: 11px; color: var(--md-default-fg-color--light, #777); margin-top: 2px; font-variant-numeric: tabular-nums; }
.hf-gloss { font-style: italic; color: var(--md-default-fg-color--light, #555); }
#hf-no-results { display: none; padding: 20px; text-align: center; color: var(--md-default-fg-color--light, #777); }
@media (max-width: 480px) {
  .hf-bar-track { display: none; }
  .hf-root { font-size: 18px; }
}
</style>

<p class="hf-intro">Top 50 Biblical Hebrew roots appearing in the Hithpael stem, ordered by frequency across the Hebrew Bible. The Hithpael is the reflexive/reciprocal stem.</p>

<div class="hf-search-wrap">
  <input type="search" id="hf-search" placeholder="Search roots or glosses…" aria-label="Filter roots">
</div>

<div style="overflow-x:auto">
<table id="hf-table">
  <thead>
    <tr>
      <th>#</th>
      <th>Root</th>
      <th>Count</th>
      <th>Frequency</th>
      <th>Gloss</th>
    </tr>
  </thead>
  <tbody id="hf-body"></tbody>
</table>
<p id="hf-no-results">No roots match your search.</p>
</div>

<script>
(function(){
var DATA=[
  {r:"פלל",l:"פָּלַל",c:80,p:11.0,g:"pray"},
  {r:"חוה",l:"חוה",c:77,p:10.6,g:"worship"},
  {r:"הלך",l:"הָלַךְ",c:64,p:8.8,g:"walk"},
  {r:"יצב",l:"יָצַב",c:48,p:6.6,g:"stand"},
  {r:"נבא",l:"נָבָא",c:28,p:3.9,g:"prophesy"},
  {r:"חזק",l:"חָזַק",c:27,p:3.7,g:"strengthen oneself"},
  {r:"הלל",l:"הָלַל",c:25,p:3.4,g:"boast"},
  {r:"קדש",l:"קָדַשׁ",c:24,p:3.3,g:"consecrate oneself"},
  {r:"יחש",l:"יָחַשׂ",c:20,p:2.8,g:"enroll by genealogy"},
  {r:"טהר",l:"טָהֵר",c:20,p:2.8,g:"cleanse oneself"},
  {r:"אבל",l:"אָבַל",c:19,p:2.6,g:"mourn"},
  {r:"חנן",l:"חָנַן",c:17,p:2.3,g:"plead for favor"},
  {r:"אוה",l:"אָוָה",c:16,p:2.2,g:"desire"},
  {r:"טמא",l:"טָמֵא",c:15,p:2.1,g:"defile oneself"},
  {r:"נדב",l:"נָדַב",c:14,p:1.9,g:"offer willingly"},
  {r:"גרה",l:"גָּרָה",c:11,p:1.5,g:"provoke"},
  {r:"ידה",l:"יָדָה",c:11,p:1.5,g:"confess"},
  {r:"חתן",l:"חָתַן",c:11,p:1.5,g:"become a son-in-law"},
  {r:"חבא",l:"חָבָא",c:10,p:1.4,g:"hide oneself"},
  {r:"חטא",l:"חָטָא",c:9,p:1.2,g:"purify oneself"},
  {r:"ענג",l:"עָנֹג",c:9,p:1.2,g:"delight oneself"},
  {r:"נשא",l:"נָשָׂא",c:8,p:1.1,g:"exalt oneself"},
  {r:"קבץ",l:"קָבַץ",c:8,p:1.1,g:"gather together"},
  {r:"כסה",l:"כָּסָה",c:8,p:1.1,g:"cover oneself"},
  {r:"חפש",l:"חָפַשׂ",c:8,p:1.1,g:"disguise oneself"},
  {r:"עבר",l:"עָבַר",c:8,p:1.1,g:"become angry"},
  {r:"אפק",l:"אָפַק",c:7,p:1.0,g:"restrain oneself"},
  {r:"פאר",l:"פָּאַר",c:7,p:1.0,g:"glorify oneself"},
  {r:"עלל",l:"עָלַל",c:7,p:1.0,g:"deal with"},
  {r:"ערב",l:"עָרַב",c:7,p:1.0,g:"associate with"},
  {r:"נחם",l:"נָחַם",c:7,p:1.0,g:"have compassion"},
  {r:"נחל",l:"נָחַל",c:7,p:1.0,g:"take as inheritance"},
  {r:"ברך",l:"בָּרַךְ",c:7,p:1.0,g:"bless oneself"},
  {r:"עלם",l:"עָלַם",c:6,p:0.8,g:"ignore"},
  {r:"ענה",l:"עָנָה",c:6,p:0.8,g:"humble oneself"},
  {r:"עטף",l:"עָטַף",c:6,p:0.8,g:"grow faint"},
  {r:"אנף",l:"אָנַף",c:6,p:0.8,g:"be angry"},
  {r:"סתר",l:"סָתַר",c:5,p:0.7,g:"hide oneself"},
  {r:"ראה",l:"רָאָה",c:5,p:0.7,g:"appear"},
  {r:"געש",l:"גָּעַשׁ",c:5,p:0.7,g:"quake"},
  {r:"נקם",l:"נָקַם",c:5,p:0.7,g:"avenge oneself"},
  {r:"נפל",l:"נָפַל",c:5,p:0.7,g:"prostrate oneself"},
  {r:"פרד",l:"פָּרַד",c:4,p:0.6,g:"scatter"},
  {r:"רגז",l:"רָגַז",c:4,p:0.6,g:"rage"},
  {r:"מכר",l:"מָכַר",c:4,p:0.6,g:"sell oneself"},
  {r:"חרה",l:"חָרָה",c:4,p:0.6,g:"fret"},
  {r:"הפך",l:"הָפַךְ",c:4,p:0.6,g:"turn oneself"},
  {r:"פקד",l:"פָּקַד",c:4,p:0.6,g:"muster"},
  {r:"חבר",l:"חָבַר",c:4,p:0.6,g:"join oneself"},
  {r:"פלש",l:"פָּלַשׁ",c:4,p:0.6,g:"roll in grief"}
];
var MAX=DATA[0].c;
var tbody=document.getElementById('hf-body');
DATA.forEach(function(d,i){
  var bw=((d.c/MAX)*100).toFixed(1);
  var tr=document.createElement('tr');
  tr.dataset.root=d.r;
  tr.dataset.gloss=d.g.toLowerCase();
  tr.innerHTML='<td><span class="hf-rank">'+(i+1)+'</span></td>'
    +'<td><div class="hf-root-cell"><span class="hf-root">'+d.r+'</span><span class="hf-lemma">'+d.l+'</span></div></td>'
    +'<td><span class="hf-count">'+d.c+'</span></td>'
    +'<td><div class="hf-bar-track"><div class="hf-bar-fill" style="width:'+bw+'%"></div></div>'
    +'<div class="hf-pct">'+d.p.toFixed(1)+'%</div></td>'
    +'<td><span class="hf-gloss">'+d.g+'</span></td>';
  tbody.appendChild(tr);
});
document.getElementById('hf-search').addEventListener('input',function(){
  var q=this.value.trim().toLowerCase();
  var rows=tbody.querySelectorAll('tr');
  var vis=0;
  rows.forEach(function(tr){
    var show=!q||tr.dataset.root.includes(q)||tr.dataset.gloss.includes(q);
    tr.style.display=show?'':'none';
    if(show)vis++;
  });
  document.getElementById('hf-no-results').style.display=vis===0?'block':'none';
});
})();
</script>
