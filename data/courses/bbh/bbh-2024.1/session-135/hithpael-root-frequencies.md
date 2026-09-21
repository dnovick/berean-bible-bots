<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+Hebrew:wght@400;600&display=swap">

<style>
.hf-intro { margin-bottom: 1.25rem; }
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
#hf-table td { padding: 8px 10px; vertical-align: middle; }
.hf-root-cell { display: flex; flex-direction: column; gap: 1px; min-width: 80px; }
.hf-heb {
  font-family: 'Noto Serif Hebrew', 'SBL Hebrew', 'Times New Roman', serif;
  direction: rtl; unicode-bidi: embed;
}
.hf-root { font-size: 20px; font-weight: 600; line-height: 1.15; }
.hf-lemma { font-size: 13px; color: var(--md-default-fg-color--light, #777); }
.hf-perfect {
  font-family: 'Noto Serif Hebrew', 'SBL Hebrew', 'Times New Roman', serif;
  font-size: 16px; font-weight: 400;
  direction: rtl; unicode-bidi: embed;
  white-space: nowrap;
}
.hf-count { font-size: 14px; font-variant-numeric: tabular-nums; }
.hf-pct { font-size: 13px; font-variant-numeric: tabular-nums; color: var(--md-default-fg-color--light, #777); }
.hf-gloss { font-style: italic; color: var(--md-default-fg-color--light, #555); font-size: 13px; }
.hf-ref { font-size: 12px; color: var(--md-default-fg-color--light, #777); white-space: nowrap; }
</style>

<p class="hf-intro">Top 20 Biblical Hebrew roots in the Hithpael stem by frequency. The 3ms perfect is the paradigm form.</p>

<div style="overflow-x:auto">
<table id="hf-table">
  <thead>
    <tr>
      <th>Root</th>
      <th>3ms Perfect</th>
      <th>Count</th>
      <th>%</th>
      <th>Gloss</th>
      <th>Example</th>
    </tr>
  </thead>
  <tbody id="hf-body"></tbody>
</table>
</div>

<script>
(function(){
var DATA=[
  {r:"פלל",l:"פָּלַל",p:"הִתְפַּלֵּל",c:80,pct:11.0,g:"pray",ref:"1 Sam 1:10"},
  {r:"חוה",l:"חוה",p:"הִשְׁתַּחֲוָה",c:77,pct:10.6,g:"worship",ref:"Gen 22:5"},
  {r:"הלך",l:"הָלַךְ",p:"הִתְהַלֵּךְ",c:64,pct:8.8,g:"walk",ref:"Gen 5:22"},
  {r:"יצב",l:"יָצַב",p:"הִתְיַצֵּב",c:48,pct:6.6,g:"stand",ref:"Num 22:22"},
  {r:"נבא",l:"נָבָא",p:"הִתְנַבֵּא",c:28,pct:3.9,g:"prophesy",ref:"1 Sam 10:11"},
  {r:"חזק",l:"חָזַק",p:"הִתְחַזַּק",c:27,pct:3.7,g:"strengthen oneself",ref:"Josh 1:6"},
  {r:"הלל",l:"הָלַל",p:"הִתְהַלֵּל",c:25,pct:3.4,g:"boast",ref:"Ps 52:3"},
  {r:"קדש",l:"קָדַשׁ",p:"הִתְקַדֵּשׁ",c:24,pct:3.3,g:"consecrate oneself",ref:"Exod 19:22"},
  {r:"יחש",l:"יָחַשׂ",p:"הִתְיַחֵשׂ",c:20,pct:2.8,g:"enroll by genealogy",ref:"Ezra 2:62"},
  {r:"טהר",l:"טָהֵר",p:"הִטַּהֵר",c:20,pct:2.8,g:"cleanse oneself",ref:"Lev 14:7"},
  {r:"אבל",l:"אָבַל",p:"הִתְאַבֵּל",c:19,pct:2.6,g:"mourn",ref:"Gen 37:34"},
  {r:"חנן",l:"חָנַן",p:"הִתְחַנֵּן",c:17,pct:2.3,g:"plead for favor",ref:"1 Kgs 8:33"},
  {r:"אוה",l:"אָוָה",p:"הִתְאַוָּה",c:16,pct:2.2,g:"desire",ref:"Num 11:4"},
  {r:"טמא",l:"טָמֵא",p:"הִטַּמֵּא",c:15,pct:2.1,g:"defile oneself",ref:"Lev 11:43"},
  {r:"נדב",l:"נָדַב",p:"הִתְנַדֵּב",c:14,pct:1.9,g:"offer willingly",ref:"Judg 5:9"},
  {r:"גרה",l:"גָּרָה",p:"הִתְגָּרָה",c:11,pct:1.5,g:"provoke",ref:"Deut 2:5"},
  {r:"ידה",l:"יָדָה",p:"הִתְוַדָּה",c:11,pct:1.5,g:"confess",ref:"Lev 5:5"},
  {r:"חתן",l:"חָתַן",p:"הִתְחַתֵּן",c:11,pct:1.5,g:"become a son-in-law",ref:"1 Kgs 3:1"},
  {r:"חבא",l:"חָבָא",p:"הִתְחַבֵּא",c:10,pct:1.4,g:"hide oneself",ref:"Gen 3:8"},
  {r:"חטא",l:"חָטָא",p:"הִתְחַטֵּא",c:9,pct:1.2,g:"purify oneself",ref:"Num 19:12"}
];
var tbody=document.getElementById('hf-body');
DATA.forEach(function(d){
  var tr=document.createElement('tr');
  tr.innerHTML=
    '<td><div class="hf-root-cell">'
    +'<span class="hf-heb hf-root">'+d.r+'</span>'
    +'<span class="hf-heb hf-lemma">'+d.l+'</span>'
    +'</div></td>'
    +'<td><span class="hf-perfect">'+d.p+'</span></td>'
    +'<td><span class="hf-count">'+d.c+'</span></td>'
    +'<td><span class="hf-pct">'+d.pct.toFixed(1)+'%</span></td>'
    +'<td><span class="hf-gloss">'+d.g+'</span></td>'
    +'<td><span class="hf-ref">'+d.ref+'</span></td>';
  tbody.appendChild(tr);
});
})();
</script>
