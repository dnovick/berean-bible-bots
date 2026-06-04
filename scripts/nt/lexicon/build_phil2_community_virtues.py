"""Build Phil 2:1 Community Virtues word study.

The five nouns in Paul's four conditional clauses (εἴ τις…) in Phil 2:1:
  παράκλησις (G3874) — consolation / exhortation
  παραμύθιον (G3890) — comfort
  κοινωνία   (G2842) — fellowship / participation
  σπλάγχνα   (G4698) — tender mercies / compassionate affection
  οἰκτιρμός  (G3628) — mercy / compassion

Cross-corpus study: NT · LXX · Biblical Hebrew backgrounds.

Outputs:
  output/reports/nt/lexicon/phil2-community-virtues/
    phil2-community-virtues.md
    phil2-nt-heatmap.png
    phil2-lxx-distribution.png
    phil2-community-virtues.csv
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

sys.path.insert(0, '.')
from src.bible_grammar.core import db as _db  # noqa: E402

REPORT_DIR = Path('output/reports/nt/lexicon/phil2-community-virtues')
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# ── Data ──────────────────────────────────────────────────────────────────────

_words = _db.load()
_lxx_df = _db.load_lxx()
_trans = _db.load_translations()
_kjv = _trans[_trans['translation'] == 'KJV']

nt = _words[_words['source'] == 'TAGNT'].copy()
ot = _words[_words['source'] == 'TAHOT'].copy()
lxx_canon = _lxx_df[~_lxx_df['is_deuterocanon']].copy()


def get_hroot(s: str) -> str:
    if not isinstance(s, str):
        return ''
    m = re.search(r'\{(H\d+)[A-Z]?\}', s)
    return m.group(1) if m else ''


def kjv_text(book: str, ch: int, vs: int) -> str:
    r = _kjv[
        (_kjv['book_id'] == book) & (_kjv['chapter'] == ch) &
        (_kjv['verse'] == vs)
    ]
    t = r['text'].values[0] if len(r) else ''
    return (t[:120] + '…') if len(t) > 120 else t


# ── Term catalogue ─────────────────────────────────────────────────────────────

# Each entry: (strongs, lemma, translit, gloss, clause, kjv_render,
#              etymology, semantic_note, ot_concept, theological_note,
#              heb_roots)
TERMS = [
    {
        'strongs': 'G3874',
        'lemma': 'παράκλησις',
        'translit': 'paraklēsis',
        'gloss': 'consolation, exhortation, encouragement',
        'clause': 1,
        'kjv_render': 'consolation',
        'etymology': (
            'From παρακαλέω (παρά + καλέω, "call alongside"). '
            'The noun covers a broad range: urgent appeal/exhortation, '
            'comfort in distress, and encouragement. The same root produces '
            'παράκλητος (the Paraclete/Advocate, John 14:16).'
        ),
        'semantic_note': (
            'In the NT παράκλησις carries two primary senses that overlap: '
            '(1) *exhortation* — earnest appeal or urging toward action '
            '(Acts 13:15; 1 Tim 4:13; Heb 12:5); '
            '(2) *consolation/comfort* — the encouragement given to the '
            'suffering (2 Cor 1:3–7, where it appears 10 times in five verses; '
            'Luke 2:25 — Simeon awaiting "the consolation of Israel"). '
            'Paul\'s usage in Phil 2:1 ("consolation in Christ") leans toward '
            'the comfort-sense: *if the believer has experienced any encouragement '
            'that comes from being in Christ*.'
        ),
        'ot_concept': (
            'The LXX uses παράκλησις 11 times in canonical books, '
            'primarily rendering Hebrew **נֶחָמָה/תַּנְחוּמִים** — '
            'derivatives of נָחַם (H5162, 108× OT), the core OT word for '
            'divine or human comfort. Isa 40:1 ("Comfort, comfort my people") '
            'uses the verb נָחַם; the LXX uses παρακαλέω. '
            'The noun appears in Isa 66:11 (LXX παράκλησις for תַּנְחוּמִים). '
            'Isa 57:18 and Jer 16:7 are key LXX occurrences. '
            'The Psalms of consolation (Ps 94 MT) and the "Book of Comfort" '
            '(Jer 30–31) supply the OT background for this vocabulary.'
        ),
        'theological_note': (
            'Paul places παράκλησις first — and qualifies it "in Christ" '
            '(ἐν Χριστῷ). The consolation is not generic; it is the specific '
            'encouragement that flows from union with the risen Lord. '
            'The πάρα- prefix ("alongside") is significant: this is comfort '
            'that comes *to* someone in their need, not merely an abstract '
            'quality. Cf. 2 Cor 1:3–7, where Paul constructs a whole theology '
            'of suffering and comfort around this word group: God is the "Father '
            'of mercies and God of all παράκλησις," who comforts us so that we '
            'may comfort others.'
        ),
        'heb_roots': [
            ('H5162', 'נָחַם', 'to comfort, console; Niphal = be comforted', 108),
            ('H8575', 'תַּנְחוּמִים', 'consolations, comforts (pl noun)', 5),
            ('H5165', 'נֶחָמָה', 'comfort, consolation (noun)', 2),
        ],
    },
    {
        'strongs': 'G3890',
        'lemma': 'παραμύθιον',
        'translit': 'paramythion',
        'gloss': 'comfort, consolation, encouragement',
        'clause': 2,
        'kjv_render': 'comfort',
        'etymology': (
            'From παραμυθέομαι (παρά + μῦθος, "speak alongside, address '
            'gently"). The word denotes warm, gentle consolation — comfort '
            'that comes through personal address and presence rather than '
            'theological declaration. It is softer and more intimate than '
            'παράκλησις.'
        ),
        'semantic_note': (
            'παραμύθιον is extremely rare: this is its **only NT occurrence**. '
            'The related verb παραμυθέομαι appears 4× (John 11:19, 31; '
            '1 Thess 2:11; 1 Thess 5:14), always in contexts of personal '
            'consolation to the bereaved or discouraged. '
            'Paul pairs it with ἀγάπης (genitive: "comfort of love") — '
            'the consolation that love gives, or perhaps the consolation that '
            'only love can give. The pairing contrasts with the preceding '
            'clause: παράκλησις is "in Christ" (objective, positional); '
            'παραμύθιον is "of love" (relational, interpersonal).'
        ),
        'ot_concept': (
            'παραμύθιον has no canonical LXX occurrences. The related verb '
            'παραμυθέομαι appears occasionally in the LXX deuterocanon '
            '(e.g., Job 2:11 in some traditions), but the noun itself '
            'is essentially a NT coinage. The concept is covered in Hebrew '
            'by נָחַם (H5162) and נִחוּם (H5150, "comfort/compassion"). '
            'The intimacy implied by the Greek word finds its Hebrew parallel '
            'in the consolation scenes of Ruth, Lamentations, and Job\'s '
            'comforters — the human act of sitting with and speaking to '
            'the suffering (Job 2:11).'
        ),
        'theological_note': (
            'The hapax nature of παραμύθιον is significant. Paul reaches for '
            'a word that appears nowhere else in the NT to name a quality of '
            'community life that is almost impossible to legislate: the gentle, '
            'love-motivated consolation that believers bring to one another '
            'simply by being present and speaking words of warmth. '
            'Alongside the churchly/liturgical resonance of παράκλησις, '
            'παραμύθιον names the small, private, relational comfort — '
            'the word of a friend, not a sermon.'
        ),
        'heb_roots': [
            ('H5162', 'נָחַם', 'to comfort, console (primary root)', 108),
            ('H5150', 'נִחוּם', 'comfort, compassion (noun)', 3),
        ],
    },
    {
        'strongs': 'G2842',
        'lemma': 'κοινωνία',
        'translit': 'koinōnia',
        'gloss': 'fellowship, participation, sharing, communion',
        'clause': 3,
        'kjv_render': 'fellowship',
        'etymology': (
            'From κοινωνός (sharer, partner) → κοινός (common, shared). '
            'The word-group covers everything held or experienced in common: '
            'financial partnership (Phil 4:15), participation in sacraments '
            '(1 Cor 10:16), the church\'s common life (Acts 2:42), and '
            'shared suffering or ministry (Phil 3:10; Phm 6).'
        ),
        'semantic_note': (
            'κοινωνία is one of Paul\'s most theologically dense terms. '
            'Its 18 NT occurrences cluster in Paul (especially 2 Cor and Phil) '
            'and 1 John. The full semantic range: '
            '(1) *participation in* something — "fellowship of his Son" '
            '(1 Cor 1:9), "fellowship of the Spirit" (Phil 2:1), "fellowship '
            'of his sufferings" (Phil 3:10); '
            '(2) *contribution/sharing of resources* — "contribution for the '
            'poor saints" (Rom 15:26); '
            '(3) *ecclesial community* — "they continued in the fellowship" '
            '(Acts 2:42); '
            '(4) *sacramental participation* — "communion of the blood/body '
            'of Christ" (1 Cor 10:16). '
            'In Phil 2:1 the genitive πνεύματος is ambiguous: '
            '"fellowship *with* the Spirit" (subjective) or "fellowship '
            '*produced by* the Spirit" (source).'
        ),
        'ot_concept': (
            'κοινωνία has minimal LXX presence (1 canonical occurrence, '
            'Lev 14:37 in a technical sense). The concept is largely '
            'Hellenistic — the Greek business and philosophical vocabulary '
            'of partnership (κοινωνός = business partner). '
            'In Hebrew the nearest concepts are expressed through: '
            'חָבַר (H2266, "join/associate," 29× OT — Ps 94:20 "partnership '
            'with wickedness") and יַחַד (H3162, "togetherness/unity"). '
            'The OT develops the *content* of covenant community without a '
            'single term for it: Israel\'s shared life before YHWH, expressed '
            'in the cult, Sabbath, and covenant meals.'
        ),
        'theological_note': (
            'κοινωνία in Paul is never mere social togetherness. '
            'It is always grounded in a shared *object* — the Son, the Spirit, '
            'the gospel, suffering, or sacrament. The phrase "fellowship of '
            'the Spirit" (Phil 2:1) became foundational for trinitarian '
            'liturgy: 2 Cor 13:14 pairs "the grace of the Lord Jesus Christ, '
            'the love of God, and the fellowship of the Holy Spirit" — '
            'possibly the earliest triadic benediction in the NT. '
            'This gives the term in Phil 2:1 its weight: Paul is not merely '
            'asking whether the Philippians have experienced religious '
            'community, but whether they have truly participated in the '
            'Spirit who makes such community possible.'
        ),
        'heb_roots': [
            ('H2266', 'חָבַר', 'to join, associate; partner (noun חָבֵר)', 29),
            ('H3162', 'יַחַד', 'togetherness, unity, all together', 96),
        ],
    },
    {
        'strongs': 'G4698',
        'lemma': 'σπλάγχνα',
        'translit': 'splanchna',
        'gloss': 'bowels, tender mercies, deep compassion (pl)',
        'clause': 4,
        'kjv_render': 'bowels',
        'etymology': (
            'Plural of σπλάγχνον (the inward parts, viscera). '
            'In the ancient world the viscera — especially the lower abdominal '
            'organs — were the seat of the deepest emotions, just as the '
            'heart is in modern English. The verb σπλαγχνίζομαι ("to be '
            'moved with compassion") is used exclusively of Jesus in the '
            'Synoptics (Matt 9:36; 14:14; 15:32; 20:34; Mark 1:41; 6:34; '
            'Luke 7:13; 10:33; 15:20).'
        ),
        'semantic_note': (
            'In the NT σπλάγχνα shifts from anatomical to emotional meaning. '
            'It denotes the deepest, most visceral compassion — love felt '
            'in the gut. Paul uses it 7× (2 Cor 6:12; 7:15; Php 1:8; 2:1; '
            'Col 3:12; Phm 7, 12, 20). '
            'In Php 1:8 Paul says he longs for the Philippians "in the '
            'σπλάγχνα of Jesus Christ" — the most tender expression in '
            'his letters. In Phm 12 Onesimus himself is Paul\'s σπλάγχνα. '
            'In Phil 2:1, paired with οἰκτιρμοί, σπλάγχνα points to the '
            'deeply felt, not merely socially expressed, dimension of '
            'Christian affection.'
        ),
        'ot_concept': (
            'The LXX uses σπλάγχνα sparingly in canonical books (3 occurrences: '
            'Prov 12:10; 26:22; Jer 31:20). The Hebrew background is '
            'רַחֲמִים (H7356, "mercy/womb-love," 45×) and the verb '
            'רָחַם (H7355, "to show mercy/love tenderly," 47×). '
            'Both derive from the root רֶחֶם (womb) — making the anatomical '
            'dimension explicit in Hebrew as well: God\'s mercy is womb-love, '
            'the love of a mother for the child she bore (cf. Isa 49:15). '
            'LXX more often renders רַחֲמִים with ἔλεος or οἰκτιρμός; '
            'σπλάγχνα is the more vivid Greek equivalent of the physical '
            'feeling implied by the Hebrew root.'
        ),
        'theological_note': (
            'The NT\'s use of σπλαγχνίζομαι exclusively for Jesus\' compassion '
            '(never for human compassion in the Synoptics) and Paul\'s use of '
            'σπλάγχνα to describe both Christ\'s affection (Phil 1:8) and '
            'the community\'s desired affection (Phil 2:1; Col 3:12) creates '
            'a striking connection: believers are called to embody the very '
            'gut-level compassion that characterizes Jesus. '
            'Col 3:12 makes this explicit: "Put on, as God\'s chosen ones, '
            'σπλάγχνα οἰκτιρμοῦ" — the same pairing as Phil 2:1, '
            'presented there as a christological imperative.'
        ),
        'heb_roots': [
            ('H7356', 'רַחֲמִים', 'mercy, tender love, womb-compassion (pl)', 45),
            ('H7355', 'רָחַם', 'to show mercy, have compassion; related to רֶחֶם (womb)', 47),
        ],
    },
    {
        'strongs': 'G3628',
        'lemma': 'οἰκτιρμός',
        'translit': 'oiktirmos',
        'gloss': 'mercy, compassion, pity (often plural)',
        'clause': 4,
        'kjv_render': 'mercies',
        'etymology': (
            'From οἰκτίρω ("to pity, feel compassion"), related to '
            'οἶκτος ("pity, compassion for suffering"). '
            'The word denotes the outward movement of compassion — '
            'pity that responds to visible suffering. '
            'It often appears in plural (οἰκτιρμοί) in the LXX and '
            'NT, matching the Hebrew tendency to use רַחֲמִים in plural.'
        ),
        'semantic_note': (
            'οἰκτιρμός appears 5× in the NT, always in contexts emphasizing '
            'God\'s character as the ground for human behavior: '
            'Rom 12:1 ("by the mercies of God … present your bodies"); '
            '2 Cor 1:3 ("Father of mercies and God of all comfort"); '
            'Phil 2:1 (paired with σπλάγχνα); '
            'Col 3:12 ("Put on σπλάγχνα οἰκτιρμοῦ"); '
            'Heb 10:28 (mercy withheld under Moses\' law). '
            'The LXX has 26 canonical occurrences, concentrated in Psalms '
            '(12×) where it renders Hebrew רַחֲמִים and חֶסֶד — '
            'God\'s covenant love and tender compassion toward Israel.'
        ),
        'ot_concept': (
            'The LXX uses οἰκτιρμός to render primarily רַחֲמִים (H7356) '
            'and occasionally חֶסֶד (H2617, 247× OT). '
            'The distinction matters: חֶסֶד is covenantal loyalty/steadfast '
            'love (translated ἔλεος, "mercy/lovingkindness" in the LXX); '
            'רַחֲמִים is visceral, womb-love compassion. '
            'Ps 25:6 LXX: "Remember, O LORD, your οἰκτιρμοί and your ἔλεος." '
            'Ps 51:1 LXX: "Have mercy on me, O God, according to your ἔλεος; '
            'according to the fullness of your οἰκτιρμῶν, blot out my '
            'transgressions." The pairing is standard: '
            'covenant loyalty (חֶסֶד/ἔλεος) + compassionate mercy '
            '(רַחֲמִים/οἰκτιρμός).'
        ),
        'theological_note': (
            '2 Cor 1:3 is the key theological location: Paul calls God '
            '"the Father of οἰκτιρμοί and God of all παράκλησις." '
            'This verse ties together two of the four Phil 2:1 terms '
            'and grounds them in the divine character. '
            'The logic of Phil 2:1 follows: *because* believers have '
            'experienced God\'s compassionate mercy (οἰκτιρμοί), '
            'they are now called to embody it toward one another. '
            'Col 3:12 makes this explicit as christological imperative: '
            '"clothe yourselves with σπλάγχνα οἰκτιρμοῦ" — '
            'the compassion that is as visceral as the inner organs, '
            'as outward-moving as pity. '
            'Both words together capture the full range: '
            'felt deeply (σπλάγχνα) and expressed actively (οἰκτιρμός).'
        ),
        'heb_roots': [
            ('H7356', 'רַחֲמִים', 'mercy, compassion (pl of רֶחֶם, womb)', 45),
            ('H2617', 'חֶסֶד', 'steadfast love, covenant loyalty (LXX ἔλεος)', 247),
        ],
    },
]

NT_BOOK_ORDER = [
    'Mat', 'Mrk', 'Luk', 'Jhn', 'Act', 'Rom', '1Co', '2Co', 'Gal', 'Eph',
    'Php', 'Col', '1Th', '2Th', '1Ti', '2Ti', 'Tit', 'Phm', 'Heb',
    'Jas', '1Pe', '2Pe', '1Jn', '2Jn', '3Jn', 'Jud', 'Rev',
]
NT_BOOK_NAMES = {
    'Mat': 'Matthew', 'Mrk': 'Mark', 'Luk': 'Luke', 'Jhn': 'John',
    'Act': 'Acts', 'Rom': 'Romans', '1Co': '1 Cor', '2Co': '2 Cor',
    'Gal': 'Galatians', 'Eph': 'Ephesians', 'Php': 'Philippians',
    'Col': 'Colossians', '1Th': '1 Thess', '2Th': '2 Thess',
    '1Ti': '1 Tim', '2Ti': '2 Tim', 'Tit': 'Titus', 'Phm': 'Philemon',
    'Heb': 'Hebrews', 'Jas': 'James', '1Pe': '1 Peter', '2Pe': '2 Peter',
    '1Jn': '1 John', '2Jn': '2 John', '3Jn': '3 John', 'Jud': 'Jude',
    'Rev': 'Revelation',
}
OT_BOOK_NAMES = {
    'Gen': 'Genesis', 'Exo': 'Exodus', 'Lev': 'Leviticus', 'Num': 'Numbers',
    'Deu': 'Deuteronomy', 'Jos': 'Joshua', 'Jdg': 'Judges', 'Rut': 'Ruth',
    '1Sa': '1 Sam', '2Sa': '2 Sam', '1Ki': '1 Kgs', '2Ki': '2 Kgs',
    '1Ch': '1 Chr', '2Ch': '2 Chr', 'Ezr': 'Ezra', 'Neh': 'Nehemiah',
    'Est': 'Esther', 'Job': 'Job', 'Psa': 'Psalms', 'Pro': 'Proverbs',
    'Ecc': 'Ecclesiastes', 'Sng': 'Song', 'Isa': 'Isaiah', 'Jer': 'Jeremiah',
    'Lam': 'Lamentations', 'Ezk': 'Ezekiel', 'Dan': 'Daniel', 'Hos': 'Hosea',
    'Jol': 'Joel', 'Amo': 'Amos', 'Oba': 'Obadiah', 'Jon': 'Jonah',
    'Mic': 'Micah', 'Nam': 'Nahum', 'Hab': 'Habakkuk', 'Zep': 'Zephaniah',
    'Hag': 'Haggai', 'Zec': 'Zechariah', 'Mal': 'Malachi',
}

TERM_COLORS = {
    'παράκλησις': '#2166ac',
    'παραμύθιον': '#4dac26',
    'κοινωνία':   '#d6604d',
    'σπλάγχνα':  '#8856a7',
    'οἰκτιρμός': '#e07b39',
}


# ── Chart 1: NT heatmap ───────────────────────────────────────────────────────

def chart_nt_heatmap() -> Path:
    lemmas = [t['lemma'] for t in TERMS]
    books_hit: set[str] = set()
    data: dict[str, dict[str, int]] = {lem: {} for lem in lemmas}

    for term in TERMS:
        for book, cnt in (
            nt[nt['strongs'] == term['strongs']]
            .groupby('book_id').size().items()
        ):
            data[term['lemma']][book] = int(cnt)
            books_hit.add(book)

    books = [b for b in NT_BOOK_ORDER if b in books_hit]
    book_labels = [NT_BOOK_NAMES.get(b, b) for b in books]
    mat = np.zeros((len(lemmas), len(books)), dtype=int)
    for i, lem in enumerate(lemmas):
        for j, b in enumerate(books):
            mat[i, j] = data[lem].get(b, 0)

    fig, ax = plt.subplots(figsize=(max(10, len(books) * 0.75 + 2),
                                    len(lemmas) * 0.65 + 2))
    im = ax.imshow(mat, aspect='auto', cmap='YlOrRd', vmin=0)

    ax.set_xticks(range(len(books)))
    ax.set_xticklabels(book_labels, rotation=45, ha='right', fontsize=8.5)
    ax.set_yticks(range(len(lemmas)))
    ax.set_yticklabels(lemmas, fontsize=10)

    for i in range(len(lemmas)):
        for j in range(len(books)):
            v = mat[i, j]
            if v > 0:
                mx = mat[i].max() or 1
                color = 'white' if v / mx > 0.55 else '#333'
                ax.text(j, i, str(v), ha='center', va='center',
                        fontsize=9, color=color, fontweight='bold')

    ax.set_title('Phil 2:1 Community Virtues — NT Distribution',
                 fontsize=11, fontweight='bold', pad=10)
    plt.colorbar(im, ax=ax, shrink=0.55, label='Occurrences')
    plt.tight_layout()
    out = REPORT_DIR / 'phil2-nt-heatmap.png'
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'  Chart: {out}')
    return out


# ── Chart 2: LXX canonical distribution ──────────────────────────────────────

def chart_lxx_distribution() -> Path:
    # Only terms with enough LXX data to chart
    chartable = [t for t in TERMS
                 if len(lxx_canon[lxx_canon['strongs'] == t['strongs']]) >= 3]
    if not chartable:
        return None  # type: ignore[return-value]

    n = len(chartable)
    fig, axes = plt.subplots(1, n, figsize=(5 * n, 4.5))
    if n == 1:
        axes = [axes]

    for ax, term in zip(axes, chartable):
        sub = lxx_canon[lxx_canon['strongs'] == term['strongs']]
        by_book = sub.groupby('book_id').size().sort_values(ascending=False)
        labels = [OT_BOOK_NAMES.get(b, b) for b in by_book.index]
        color = TERM_COLORS.get(term['lemma'], '#4472C4')
        bars = ax.bar(range(len(labels)), by_book.values, color=color, alpha=0.9)
        for bar, v in zip(bars, by_book.values):
            ax.text(bar.get_x() + bar.get_width() / 2, v + 0.1,
                    str(v), ha='center', va='bottom', fontsize=8.5)
        ax.set_xticks(range(len(labels)))
        ax.set_xticklabels(labels, rotation=45, ha='right', fontsize=8.5)
        ax.set_title(f'{term["lemma"]}\n(canonical LXX, {len(sub)}×)',
                     fontsize=9, fontweight='bold')
        ax.set_ylabel('Occurrences')
        ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))

    plt.suptitle('Phil 2:1 Terms — LXX Canonical Distribution by Book',
                 fontsize=11, fontweight='bold')
    plt.tight_layout()
    out = REPORT_DIR / 'phil2-lxx-distribution.png'
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'  Chart: {out}')
    return out


# ── Report ────────────────────────────────────────────────────────────────────

def build_report() -> Path:
    lines = [
        '# Phil 2:1 — Community Virtues Word Study',
        '',
        '**Anchor text:** Philippians 2:1 (KJV) — *"If there be therefore any '
        'consolation in Christ, if any comfort of love, if any fellowship of '
        'the Spirit, if any bowels and mercies"*',
        '',
        '**Greek text:**',
        '> Εἴ τις οὖν **παράκλησις** ἐν Χριστῷ, εἴ τι **παραμύθιον** ἀγάπης, '
        'εἴ τις **κοινωνία** πνεύματος, εἴ τις **σπλάγχνα** καὶ **οἰκτιρμοί**',
        '',
        '**Corpora:** NT Greek (TAGNT) · LXX Greek · Biblical Hebrew (TAHOT)',
        '',
        '## Contents',
        '',
        '- [Overview](#overview)',
        '- [Key Observations](#key-observations)',
    ]
    for t in TERMS:
        anchor = t['lemma'].lower().replace('/', '').replace(' ', '-')
        lines.append(f'- [{t["lemma"]} — {t["gloss"].split(",")[0]}](#{anchor})')
    lines += [
        '- [Distribution Charts](#distribution-charts)',
        '- [Cross-Term Connections](#cross-term-connections)',
        '- [Summary Table](#summary-table)',
        '',
        '---',
        '',
        '## Overview',
        '',
        'Philippians 2:1 opens with a rhetorical masterpiece: four conditional '
        'clauses, each beginning εἴ τις/τι ("if there is any…"). '
        'Paul is not expressing doubt — he is employing a *conditional of '
        'certainty* to draw out the consequences of what the Philippians '
        'already possess. The structure is: *"Since all of these things are '
        'true of you — and they are — then let your community life reflect it."*',
        '',
        'The verse names five nouns across the four clauses:',
        '',
        '| Clause | Greek | KJV | Paul\'s qualifier |',
        '|---|---|---|---|',
        '| 1 | παράκλησις | consolation | ἐν Χριστῷ (in Christ) |',
        '| 2 | παραμύθιον | comfort | ἀγάπης (of love) |',
        '| 3 | κοινωνία | fellowship | πνεύματος (of the Spirit) |',
        '| 4a | σπλάγχνα | bowels | — (paired with οἰκτιρμοί) |',
        '| 4b | οἰκτιρμοί | mercies | — (paired with σπλάγχνα) |',
        '',
        'Each term is anchored to a source: the first three have '
        'explicitly theological genitives (Christ, love, Spirit); the fourth '
        'pair stands alone — the bare visceral reality of compassionate mercy.',
        '',
        '---',
        '',
        '## Key Observations',
        '',
        '- **παράκλησις (29 NT occurrences) is Paul\'s dominant comfort term**, '
        'concentrated in 2 Corinthians (11×) where he develops a full theology '
        'of suffering and consolation. Its pairing with ἐν Χριστῷ grounds all '
        'community encouragement in union with the risen Lord.',
        '',
        '- **παραμύθιον is a NT hapax** — appearing only here. Its rareness '
        'is likely deliberate: Paul reaches for an intimate, non-technical word '
        'for the gentle comfort that love alone provides, distinct from the '
        'more "official" encouragement of παράκλησις.',
        '',
        '- **κοινωνία (18 NT occurrences) carries both vertical and horizontal '
        'dimensions**: participation *in* Christ/Spirit (vertical, Phil 2:1; '
        '1 Cor 1:9) and the shared common life of the community (horizontal, '
        'Acts 2:42). The Phil 2:1 qualifier πνεύματος links community to its '
        'divine source — fellowship is possible only because the Spirit creates it.',
        '',
        '- **σπλάγχνα and οἰκτιρμοί are paired here and in Col 3:12**, '
        'suggesting this was a fixed Pauline dyad for "deeply felt compassion." '
        'Both words are also used of God (2 Cor 1:3; Luke 1:78), making the '
        'community\'s compassion a reflection of the divine character.',
        '',
        '- **The Hebrew backgrounds reveal the depth of the imagery**: '
        'נָחַם (comfort), רַחֲמִים (womb-love), and חֶסֶד (covenant loyalty) '
        'are among the most theologically rich OT terms — all pointing to '
        'God\'s character as the ultimate ground for human community.',
        '',
        '---',
        '',
    ]

    for term in TERMS:
        s = term['strongs']
        nt_hits = nt[nt['strongs'] == s]
        lxx_hits = lxx_canon[lxx_canon['strongs'] == s]
        nt_ct = len(nt_hits)
        lxx_ct = len(lxx_hits)

        by_book = nt_hits.groupby('book_id').size().sort_values(ascending=False)

        clause_str = (f'Clause {term["clause"]}' +
                      (' (paired with σπλάγχνα)'
                       if term['lemma'] == 'οἰκτιρμός' else
                       ' (paired with οἰκτιρμοί)'
                       if term['lemma'] == 'σπλάγχνα' else ''))

        lines += [
            f'## {term["lemma"]}',
            '',
            f'**Strongs:** {s}  ',
            f'**Transliteration:** {term["translit"]}  ',
            f'**Gloss:** {term["gloss"]}  ',
            f'**Phil 2:1 KJV:** "{term["kjv_render"]}"  ',
            f'**Phil 2:1 position:** {clause_str}  ',
            f'**NT occurrences:** {nt_ct}  ',
            f'**LXX canonical:** {lxx_ct}',
            '',
            '**NT distribution:**  ',
            ', '.join(
                f'{NT_BOOK_NAMES.get(b, b)} ({c})'
                for b, c in by_book.items()
            ) if len(by_book) else '*Only Phil 2:1*',
            '',
            '---',
            '',
            '### Etymology and Semantic Range',
            '',
            term['etymology'],
            '',
            term['semantic_note'],
            '',
            '---',
            '',
            '### OT / LXX Background',
            '',
            term['ot_concept'],
            '',
        ]

        # Hebrew roots table
        if term['heb_roots']:
            lines += [
                '| Hebrew root | Transliteration | Gloss | OT occurrences |',
                '|---|---|---|---:|',
            ]
            for root, heb, gloss, _ in term['heb_roots']:
                ct = len(ot[ot['strongs'].apply(get_hroot) == root])
                lines.append(f'| {root} | {heb} | {gloss} | {ct} |')
            lines.append('')

        # LXX book distribution if available
        if lxx_ct > 0:
            by_book_lxx = lxx_hits.groupby('book_id').size().sort_values(ascending=False)
            lxx_str = ', '.join(
                f'{OT_BOOK_NAMES.get(b, b)} ({c})'
                for b, c in by_book_lxx.items()
            )
            lines += [f'**LXX canonical distribution:** {lxx_str}', '']

        lines += [
            '---',
            '',
            '### Theological Note',
            '',
            term['theological_note'],
            '',
            '---',
            '',
            '### NT Occurrences (KJV)',
            '',
            '| Reference | KJV text |',
            '|---|---|',
        ]

        refs = nt_hits[['book_id', 'chapter', 'verse']].drop_duplicates()
        for _, r in refs.sort_values(['book_id', 'chapter', 'verse']).iterrows():
            bname = NT_BOOK_NAMES.get(r['book_id'], r['book_id'])
            t_text = kjv_text(r['book_id'], int(r['chapter']), int(r['verse']))
            lines.append(f'| {bname} {r["chapter"]}:{r["verse"]} | {t_text} |')

        lines += ['', '---', '']

    lines += [
        '## Distribution Charts',
        '',
        '![NT Distribution Heatmap](phil2-nt-heatmap.png)',
        '',
        '![LXX Distribution](phil2-lxx-distribution.png)',
        '',
        '---',
        '',
        '## Cross-Term Connections',
        '',
        '### The σπλάγχνα + οἰκτιρμοί Dyad',
        '',
        'These two terms appear together in both Phil 2:1 and Col 3:12 '
        '("σπλάγχνα οἰκτιρμοῦ, kindness, humility…"). The pairing is '
        'likely a fixed Pauline formula for the complete expression of '
        'compassion: felt viscerally (σπλάγχνα) and expressed outwardly '
        'toward others (οἰκτιρμός). 2 Cor 1:3 titles God as '
        '"Father of mercies (οἰκτιρμῶν) and God of all comfort (παράκλησις)," '
        'linking two of the five Phil 2:1 terms in a divine epithet.',
        '',
        '### The Triadic Structure of Clauses 1–3',
        '',
        'The qualifiers reveal a Pauline triad: '
        '*in Christ* (παράκλησις) · *of love* (παραμύθιον) · '
        '*of the Spirit* (κοινωνία). '
        'This is not a formal trinitarian formula, but it anticipates the '
        'structure of 2 Cor 13:14 ("grace of the Lord Jesus Christ, love of '
        'God, fellowship of the Holy Spirit") — suggesting that for Paul the '
        'resources of community life are inseparably christological, '
        'agapic, and pneumatological.',
        '',
        '### Paul and Philippians',
        '',
        'Four of the five terms recur elsewhere in Philippians itself:',
        '',
        '| Term | Other Phil reference |',
        '|---|---|',
        '| παράκλησις | Phil 2:1 only in Phil |',
        '| κοινωνία | Phil 1:5; 3:10; 4:15 (3× more in Phil) |',
        '| σπλάγχνα | Phil 1:8 ("σπλάγχνα of Jesus Christ") |',
        '| οἰκτιρμός | Phil 2:1 only in Phil |',
        '',
        '---',
        '',
        '## Summary Table',
        '',
        '| Term | Strongs | NT | LXX (canonical) | Hebrew background | Phil 2:1 qualifier |',
        '|---|---|---:|---:|---|---|',
    ]

    for term in TERMS:
        nt_ct = len(nt[nt['strongs'] == term['strongs']])
        lxx_ct = len(lxx_canon[lxx_canon['strongs'] == term['strongs']])
        heb = '; '.join(f'{r} {h}' for r, h, _, _ in term['heb_roots'])
        qual_map = {
            'G3874': 'ἐν Χριστῷ',
            'G3890': 'ἀγάπης',
            'G2842': 'πνεύματος',
            'G4698': '— (paired w/ οἰκτιρμοί)',
            'G3628': '— (paired w/ σπλάγχνα)',
        }
        lines.append(
            f'| {term["lemma"]} | {term["strongs"]} | {nt_ct} | {lxx_ct} '
            f'| {heb} | {qual_map.get(term["strongs"], "—")} |'
        )

    lines += [
        '',
        '---',
        '',
        '*Greek NT data: TAGNT (Byzantine/Textus Receptus, STEPBible CC BY 4.0).*  ',
        '*LXX data: CenterBLC LXX (CC BY 4.0).*  ',
        '*Hebrew data: TAHOT (STEPBible CC BY 4.0).*  ',
        '*Generated by [scripts/nt/lexicon/build_phil2_community_virtues.py]'
        '(../../../../scripts/nt/lexicon/build_phil2_community_virtues.py).*',
    ]

    out = REPORT_DIR / 'phil2-community-virtues.md'
    out.write_text('\n'.join(lines), encoding='utf-8')
    print(f'  Report: {out}')
    return out


def build_csv() -> Path:
    rows = []
    for term in TERMS:
        for _, r in (
            nt[nt['strongs'] == term['strongs']]
            [['book_id', 'chapter', 'verse', 'word']]
            .drop_duplicates(subset=['book_id', 'chapter', 'verse'])
            .iterrows()
        ):
            rows.append({
                'lemma': term['lemma'], 'strongs': term['strongs'],
                'gloss': term['gloss'], 'clause': term['clause'],
                'book': r['book_id'], 'chapter': r['chapter'], 'verse': r['verse'],
                'word': r['word'],
            })
    out = REPORT_DIR / 'phil2-community-virtues.csv'
    pd.DataFrame(rows).to_csv(out, index=False)
    print(f'  CSV: {out}')
    return out


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    print('Building charts...')
    chart_nt_heatmap()
    chart_lxx_distribution()

    print('Building report...')
    build_report()

    print('Building CSV...')
    build_csv()

    print('Done.')
