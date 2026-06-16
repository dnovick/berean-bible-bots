"""
Generate the BBH Ch29 Hophal Weak morphology deck (all three formats).

Output: data/lessons/bbh/ch29/ch29-morphology-deck.[md,txt,-fd.txt]

44 cards covering all eight weak root classes:
  Biconsonantal (II-ו/י)  ·  Pe-Nun (I-נ)  ·  Lamed-He (III-ה)
  Pe-Yod/Vav (I-י/ו)     ·  Geminate       ·  Pe-Guttural (I-ע/ח)
  Lamed-Guttural (III-ח/ע)  ·  Contrast / Diagnostic

Primary roots chosen for maximum OT attestation:
  Biconsonantal: קום (set up), שׁוב (return), מות (die/put to death)
  Pe-Nun:        נגד (tell/report), נכה (strike — also III-ה)
  Lamed-He:      גלה (exile)
  Pe-Yod/Vav:    ילד (bear/beget), בוא (come/bring), ירד (go/bring down)
  Geminate:      נקם (avenge — Pe-Nun assimilation creates geminate-looking form)
  Pe-Guttural:   עמד (stand/station)
  Lamed-Guttural: שׁלח (send/release)
  Lamed-Aleph:   קרא (call)
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from bible_grammar.morphology_deck import (  # noqa: E402
    DeckCard, DeckConfig, MorphologyDeckWriter,
)

OUT_DIR = Path("data/lessons/bbh/ch29")
PREFIX = "ch29-morphology-deck"
DECK = "BBH Chapter 29 — Hophal Weak"

# ── Card definitions ──────────────────────────────────────────────────────────

CARDS = [

    # ── BICONSONANTAL (II-ו/י) ────────────────────────────────────────────────
    # Key pattern: Shureq (וּ) under prefix consonant; only two root consonants
    # visible between prefix and ending.

    DeckCard(
        num=1, front="הוּקַם", ref="Exo 40:17",
        root="קום", stem="Hophal", conj="Perfect", pgn="3ms",
        gloss="the tabernacle was set up",
        section="BICONSONANTAL (II-ו/י)",
        tag="hophal-perfect hophal-biconsonantal bbh-ch29",
        back_txt=(
            "קום Hophal+Perfect+3ms — \"the tabernacle was set up\" — "
            "הוּ prefix (Shureq); biconsonantal: only ק + מ visible; "
            "Patach under R2 (ק); tabernacle dedication narrative; "
            "Hiphil הֵקִים = \"Moses set up [the tabernacle]\" (v.18)"
        ),
        back_fd=(
            "Root: קום | Hophal | Perfect 3ms | the tabernacle was set up — "
            "הוּ prefix (Shureq); 2 root consonants (ק + מ); contrast Hiphil הֵקִים"
        ),
    ),

    DeckCard(
        num=2, front="הוּשַׁב", ref="Gen 43:12",
        root="שׁוב", stem="Hophal", conj="Perfect", pgn="3ms",
        gloss="the silver was returned",
        section="BICONSONANTAL (II-ו/י)",
        tag="hophal-perfect hophal-biconsonantal bbh-ch29",
        back_txt=(
            "שׁוב Hophal+Perfect+3ms — \"the silver that was returned in your bags\" — "
            "הוּ prefix (Shureq); biconsonantal: only שׁ + ב visible; "
            "Patach under R2; Jacob's sons on second journey to Egypt"
        ),
        back_fd=(
            "Root: שׁוב | Hophal | Perfect 3ms | the silver was returned — "
            "הוּ prefix (Shureq); 2 root consonants (שׁ + ב)"
        ),
    ),

    DeckCard(
        num=3, front="הֻמְתוּ", ref="2Sa 21:9",
        root="מות", stem="Hophal", conj="Perfect", pgn="3cp",
        gloss="they were put to death",
        section="BICONSONANTAL (II-ו/י)",
        tag="hophal-perfect hophal-biconsonantal bbh-ch29",
        back_txt=(
            "מות Hophal+Perfect+3cp — \"they were put to death\" — "
            "הֻ prefix (Qibbuts, not Shureq — variant spelling before suffix); "
            "מְ + vocal shewa under מ; Gibeah, David hands over Saul's sons to the Gibeonites; "
            "note: Qibbuts (הֻ) rather than Shureq (הוּ) in this attested form"
        ),
        back_fd=(
            "Root: מות | Hophal | Perfect 3cp | they were put to death — "
            "הֻ prefix (Qibbuts before suffix); 2 root consonants"
        ),
    ),

    DeckCard(
        num=4, front="יוּקַם", ref="Num 9:15",
        root="קום", stem="Hophal", conj="Imperfect", pgn="3ms",
        gloss="the tabernacle was set up (on that day)",
        section="BICONSONANTAL (II-ו/י)",
        tag="hophal-imperfect hophal-biconsonantal bbh-ch29",
        back_txt=(
            "קום Hophal+Imperfect+3ms — \"on the day the tabernacle was set up\" — "
            "יוּ prefix (yod + Shureq); biconsonantal: ק + מ only; "
            "Patach under R2 (ק); same tabernacle event from Num 9 (cloud/pillar)"
        ),
        back_fd=(
            "Root: קום | Hophal | Imperfect 3ms | the tabernacle was set up — "
            "יוּ prefix (Shureq under yod); 2 root consonants"
        ),
    ),

    DeckCard(
        num=5, front="יוּמַת", ref="Exo 31:14",
        root="מות", stem="Hophal", conj="Imperfect", pgn="3ms",
        gloss="shall be put to death",
        section="BICONSONANTAL (II-ו/י)",
        tag="hophal-imperfect hophal-biconsonantal bbh-ch29",
        back_txt=(
            "מות Hophal+Imperfect+3ms — \"whoever does any work on it shall be put to death\" — "
            "יוּ prefix (Shureq); מ + Patach + ת; Sabbath death-penalty legislation; "
            "the most common Hophal form in the OT (~50+ tokens in legal texts); "
            "cf. מוֹת יוּמַת formula (cards 9)"
        ),
        back_fd=(
            "Root: מות | Hophal | Imperfect 3ms | shall be put to death — "
            "יוּ prefix (Shureq); the most common Hophal form in the OT"
        ),
    ),

    DeckCard(
        num=6, front="וַיּוּקַם", ref="Exo 40:18",
        root="קום", stem="Hophal", conj="Wayyiqtol", pgn="3ms",
        gloss="and it was set up / erected",
        section="BICONSONANTAL (II-ו/י)",
        tag="hophal-wayyiqtol hophal-biconsonantal bbh-ch29",
        back_txt=(
            "קום Hophal+Wayyiqtol+3ms — \"Moses set up [the tabernacle]... and it was erected\" — "
            "וַיּוּ prefix: Waw + Patach + Yod+Dagesh + Shureq; "
            "Dagesh forte in yod from Wayyiqtol assimilation; "
            "Patach under R2; tabernacle narrative (Exo 40:18)"
        ),
        back_fd=(
            "Root: קום | Hophal | Wayyiqtol 3ms | and it was set up — "
            "וַיּוּ prefix (Dagesh forte in yod + Shureq)"
        ),
    ),

    DeckCard(
        num=7, front="וַיּוּשַׁב", ref="Exo 10:8",
        root="שׁוב", stem="Hophal", conj="Wayyiqtol", pgn="3ms",
        gloss="and he was brought back",
        section="BICONSONANTAL (II-ו/י)",
        tag="hophal-wayyiqtol hophal-biconsonantal bbh-ch29",
        back_txt=(
            "שׁוב Hophal+Wayyiqtol+3ms — \"Moses and Aaron were brought back to Pharaoh\" — "
            "וַיּוּ prefix; Dagesh forte in yod + Shureq; Patach under שׁ; "
            "Plague of Locusts negotiation; Pharaoh summons Moses back after driving them out"
        ),
        back_fd=(
            "Root: שׁוב | Hophal | Wayyiqtol 3ms | and he was brought back — "
            "וַיּוּ prefix; Patach under R2 (שׁ)"
        ),
    ),

    DeckCard(
        num=8, front="מוּקָם", ref="paradigm",
        root="קום", stem="Hophal", conj="Participle", pgn="ms",
        gloss="(being) set up / established",
        section="BICONSONANTAL (II-ו/י)",
        tag="hophal-participle hophal-biconsonantal bbh-ch29",
        back_txt=(
            "קום Hophal+Participle+ms — \"being set up / established\" — "
            "מוּ prefix (Mem + Shureq); Qamets under R2 (ק) — "
            "Participle signature vowel; only 2 root consonants visible (ק + מ)"
        ),
        back_fd=(
            "Root: קום | Hophal | Participle ms | (being) set up — "
            "מוּ prefix (Shureq); Qamets under R2"
        ),
    ),

    DeckCard(
        num=9, front="מוֹת יוּמַת", ref="Exo 21:12",
        root="מות", stem="Hophal", conj="Formula", pgn="—",
        gloss="\"shall surely be put to death\"",
        section="BICONSONANTAL (II-ו/י)",
        tag="hophal-imperfect hophal-biconsonantal hophal-diagnostic bbh-ch29",
        back_txt=(
            "מות — capital punishment formula: "
            "מוֹת = Qal Infinitive Absolute (\"dying / certainly\"); "
            "יוּמַת = Hophal Imperfect 3ms (\"shall be put to death\"); "
            "together: Inf.Abs. + finite verb intensifies — \"shall surely/certainly be put to death\"; "
            "appears 35+ times in Torah law (Exo 21, Lev 20, Num 35, Deu 13, 17)"
        ),
        back_fd=(
            "Root: מות | Formula: Inf.Abs. + Hophal Imperfect | "
            "מוֹת (Qal Inf.Abs.) + יוּמַת (Hophal Impf. 3ms) = \"shall surely be put to death\""
        ),
    ),

    # ── PE-NUN (I-נ) ──────────────────────────────────────────────────────────
    # Key pattern: root נ assimilates into R2 (Dagesh forte in R2 in prefix conjugations)
    # Hophal u-class prefix + Dagesh in R2 = unmistakable Pe-Nun Hophal signature

    DeckCard(
        num=10, front="הֻגַּד", ref="Deu 17:4",
        root="נגד", stem="Hophal", conj="Perfect", pgn="3ms",
        gloss="it has been told / reported",
        section="PE-NUN (I-נ)",
        tag="hophal-perfect hophal-pe-nun bbh-ch29",
        back_txt=(
            "נגד Hophal+Perfect+3ms — \"and it has been told to you\" — "
            "הֻ prefix (Qibbuts); Dagesh forte in ג (R2) from Pe-Nun assimilation; "
            "no trace of root נ visible; legal context: reporting idolatry to judges; "
            "compare Hiphil הִגִּיד \"to declare, report\" (active)"
        ),
        back_fd=(
            "Root: נגד | Hophal | Perfect 3ms | it has been told/reported — "
            "הֻ prefix (Qibbuts); Dagesh forte in ג from Pe-Nun (נ) assimilation"
        ),
    ),

    DeckCard(
        num=11, front="וְהֻגַּד", ref="Deu 17:4",
        root="נגד", stem="Hophal", conj="Weqatal", pgn="3ms",
        gloss="and it has been told / reported to you",
        section="PE-NUN (I-נ)",
        tag="hophal-weqatal hophal-pe-nun bbh-ch29",
        back_txt=(
            "נגד Hophal+Weqatal+3ms — \"and it has been told to you\" — "
            "וְ + Hophal Perfect form (הֻגַּד unchanged); "
            "Weqatal = Waw + Shewa + Perfect base; "
            "same verse as card 10 (Deu 17:4); both perfect and weqatal in one verse"
        ),
        back_fd=(
            "Root: נגד | Hophal | Weqatal 3ms | and it has been told — "
            "וְ + הֻגַּד; Waw + Shewa prefixed to Hophal Perfect form"
        ),
    ),

    DeckCard(
        num=12, front="יֻגַּד", ref="paradigm",
        root="נגד", stem="Hophal", conj="Imperfect", pgn="3ms",
        gloss="it shall be told / reported",
        section="PE-NUN (I-נ)",
        tag="hophal-imperfect hophal-pe-nun bbh-ch29",
        back_txt=(
            "נגד Hophal+Imperfect+3ms — \"it shall be told\" — "
            "יֻ prefix (Qibbuts); Dagesh forte in ג (R2) from Pe-Nun assimilation; "
            "Patach under R2; no trace of root נ; "
            "contrast Hiphil Imperfect יַגִּיד (yod + Patach, lengthened vowel under R2)"
        ),
        back_fd=(
            "Root: נגד | Hophal | Imperfect 3ms | it shall be told — "
            "יֻ prefix (Qibbuts); Dagesh forte in R2 (ג)"
        ),
    ),

    DeckCard(
        num=13, front="וַיֻּגַּד", ref="Gen 22:20",
        root="נגד", stem="Hophal", conj="Wayyiqtol", pgn="3ms",
        gloss="and it was told to (Abraham)",
        section="PE-NUN (I-נ)",
        tag="hophal-wayyiqtol hophal-pe-nun bbh-ch29",
        back_txt=(
            "נגד Hophal+Wayyiqtol+3ms — \"and it was told to Abraham\" — "
            "וַיֻּ prefix (Waw + Patach + Yod + Dagesh + Qibbuts); "
            "Dagesh forte in ג from Pe-Nun assimilation; "
            "one of the most common narrative formulas in Genesis and historical books: "
            "וַיֻּגַּד לְ = \"and it was told to [person]\" (Gen 22:20, 27:42, 38:13, etc.)"
        ),
        back_fd=(
            "Root: נגד | Hophal | Wayyiqtol 3ms | and it was told to... — "
            "וַיֻּ prefix + Dagesh in R2; common narrative reporting formula"
        ),
    ),

    DeckCard(
        num=14, front="הֻגֵּד", ref="paradigm",
        root="נגד", stem="Hophal", conj="Inf. Absolute", pgn="—",
        gloss="to be declared / reported",
        section="PE-NUN (I-נ)",
        tag="hophal-infinitive hophal-pe-nun bbh-ch29",
        back_txt=(
            "נגד Hophal+Infinitive Absolute — \"to be declared\" — "
            "הֻ prefix (Qibbuts); Tsere (ֵ) under R2 (ג) distinguishes Inf.Abs. from Perfect (Patach ַ); "
            "Dagesh forte in ג from Pe-Nun assimilation retained; "
            "Inf.Abs. always shows Tsere under R2 in Hophal regardless of weak class"
        ),
        back_fd=(
            "Root: נגד | Hophal | Inf. Absolute | to be declared — "
            "הֻ prefix; Tsere under R2 (ג) = Inf.Abs. signature; Dagesh forte in R2"
        ),
    ),

    DeckCard(
        num=15, front="הֻכָּה", ref="Num 25:14",
        root="נכה", stem="Hophal", conj="Perfect", pgn="3ms",
        gloss="was struck down (in the plague)",
        section="PE-NUN (I-נ)",
        tag="hophal-perfect hophal-pe-nun hophal-lamed-he bbh-ch29",
        back_txt=(
            "נכה Hophal+Perfect+3ms — \"the one who was struck\" — "
            "doubly weak: I-נ (Pe-Nun) + III-ה (Lamed-He); "
            "הֻ prefix (Qibbuts); Dagesh forte in כ from נ assimilation; "
            "Qamets + ה marks III-ה Perfect ending; "
            "Num 25: Israelite killed at Peor; cf. מֻכֶּה (Participle) in Isa 53:4"
        ),
        back_fd=(
            "Root: נכה | Hophal | Perfect 3ms | was struck down — "
            "הֻ prefix; Dagesh in כ (Pe-Nun); Qamets+ה ending (Lamed-He); doubly weak"
        ),
    ),

    DeckCard(
        num=16, front="יֻכֶּה", ref="Deu 25:2",
        root="נכה", stem="Hophal", conj="Imperfect", pgn="3ms",
        gloss="the guilty man shall be beaten",
        section="PE-NUN (I-נ)",
        tag="hophal-imperfect hophal-pe-nun hophal-lamed-he bbh-ch29",
        back_txt=(
            "נכה Hophal+Imperfect+3ms — \"the guilty man shall be beaten\" — "
            "doubly weak: I-נ (Pe-Nun) + III-ה (Lamed-He); "
            "יֻ prefix (Qibbuts); Dagesh forte in כ (Pe-Nun assimilation); "
            "Seghol + ה marks III-ה Imperfect ending (contraction of strong -יֻכַּ-ת); "
            "corporal punishment regulations: flogging in the presence of a judge"
        ),
        back_fd=(
            "Root: נכה | Hophal | Imperfect 3ms | shall be beaten — "
            "יֻ prefix; Dagesh in כ (Pe-Nun); Seghol+ה ending (Lamed-He); doubly weak"
        ),
    ),

    # ── LAMED-HE (III-ה) ─────────────────────────────────────────────────────
    # Key pattern: u-class prefix unchanged; endings contract;
    # Wayyiqtol apocopates (final ה drops)

    DeckCard(
        num=17, front="הֻגְלָה", ref="Amos 1:5",
        root="גלה", stem="Hophal", conj="Perfect", pgn="3ms",
        gloss="was exiled / sent into exile",
        section="LAMED-HE (III-ה)",
        tag="hophal-perfect hophal-lamed-he bbh-ch29",
        back_txt=(
            "גלה Hophal+Perfect+3ms — \"the people of Aram shall go into exile to Kir\" — "
            "הֻ prefix (Qibbuts); Qamets + ה mater (III-ה Perfect ending); "
            "vocal shewa under R1 (ג); the Hophal of Hiphil הֶגְלָה \"to exile/deport\"; "
            "Amos's oracles against the nations use this formula repeatedly (1:5, 6, 9, 15; 5:5)"
        ),
        back_fd=(
            "Root: גלה | Hophal | Perfect 3ms | was exiled — "
            "הֻ prefix (Qibbuts); Qamets + ה = III-ה Perfect ending"
        ),
    ),

    DeckCard(
        num=18, front="הֻגְלוּ", ref="Amos 1:6",
        root="גלה", stem="Hophal", conj="Perfect", pgn="3cp",
        gloss="they were exiled (a whole people)",
        section="LAMED-HE (III-ה)",
        tag="hophal-perfect hophal-lamed-he bbh-ch29",
        back_txt=(
            "גלה Hophal+Perfect+3cp — \"they delivered up a whole exile\" — "
            "הֻ prefix (Qibbuts); plural -וּ suffix added directly to contracted III-ה stem; "
            "no trace of final ה before the suffix; "
            "Amos 1:6 oracle against Gaza for delivering people to Edom"
        ),
        back_fd=(
            "Root: גלה | Hophal | Perfect 3cp | they were exiled — "
            "הֻ prefix; plural -וּ suffix; final ה absorbed before suffix"
        ),
    ),

    DeckCard(
        num=19, front="יֻגְלֶה", ref="paradigm",
        root="גלה", stem="Hophal", conj="Imperfect", pgn="3ms",
        gloss="shall be exiled",
        section="LAMED-HE (III-ה)",
        tag="hophal-imperfect hophal-lamed-he bbh-ch29",
        back_txt=(
            "גלה Hophal+Imperfect+3ms — \"shall be exiled\" — "
            "יֻ prefix (Qibbuts); Seghol + ה mater (III-ה Imperfect ending); "
            "compare strong Hophal Imperfect יֻקְטַל (Patach + final consonant); "
            "III-ה contracts: the final ה becomes a mater for Seghol"
        ),
        back_fd=(
            "Root: גלה | Hophal | Imperfect 3ms | shall be exiled — "
            "יֻ prefix; Seghol + ה = III-ה Imperfect ending"
        ),
    ),

    DeckCard(
        num=20, front="וַיֻּגֶל", ref="paradigm",
        root="גלה", stem="Hophal", conj="Wayyiqtol", pgn="3ms",
        gloss="and he was exiled (apocopated form)",
        section="LAMED-HE (III-ה)",
        tag="hophal-wayyiqtol hophal-lamed-he bbh-ch29",
        back_txt=(
            "גלה Hophal+Wayyiqtol+3ms — apocopated: final ה drops entirely — "
            "וַיֻּ prefix (Waw + Patach + Yod + Dagesh + Qibbuts); "
            "Seghol under R2 (ל) from apocopation; no final ה; "
            "apocopation in Wayyiqtol is the defining III-ה feature: "
            "יֻגְלֶה (Imperfect) → וַיֻּגֶל (Wayyiqtol, ה dropped)"
        ),
        back_fd=(
            "Root: גלה | Hophal | Wayyiqtol 3ms | and he was exiled — "
            "וַיֻּ prefix; final ה dropped (apocopation); Seghol under R2"
        ),
    ),

    DeckCard(
        num=21, front="מֻגְלֶה", ref="paradigm",
        root="גלה", stem="Hophal", conj="Participle", pgn="ms",
        gloss="(one) being exiled",
        section="LAMED-HE (III-ה)",
        tag="hophal-participle hophal-lamed-he bbh-ch29",
        back_txt=(
            "גלה Hophal+Participle+ms — \"(one) being exiled\" — "
            "מֻ prefix (Mem + Qibbuts); Seghol + ה mater (III-ה Participle ending); "
            "same Seghol+ה pattern as Imperfect 3ms; "
            "compare מֻקְטָל (strong Hophal Ptc.: Qamets under R2 + final consonant)"
        ),
        back_fd=(
            "Root: גלה | Hophal | Participle ms | (one) being exiled — "
            "מֻ prefix; Seghol + ה = III-ה Participle ending"
        ),
    ),

    # ── PE-YOD/VAV (I-י/ו) ───────────────────────────────────────────────────
    # Key pattern: Pe-Yod/Vav quiesces into prefix; Hophal Qibbuts lengthens to Shureq (וּ)
    # Same Shureq pattern as Biconsonantal, but 3 root consonants visible

    DeckCard(
        num=22, front="הוּלַד", ref="Gen 21:5",
        root="ילד", stem="Hophal", conj="Perfect", pgn="3ms",
        gloss="was born / begotten",
        section="PE-YOD/VAV (I-י/ו)",
        tag="hophal-perfect hophal-pe-yod bbh-ch29",
        back_txt=(
            "ילד Hophal+Perfect+3ms — \"when Isaac was born to him\" — "
            "הוּ prefix (Shureq): Pe-Yod י quiesces into prefix, Qibbuts lengthens to Shureq; "
            "Patach under R2 (ל); R2 + R3 (ל + ד) visible; "
            "Abraham was 100 years old; the genealogical passive of birth"
        ),
        back_fd=(
            "Root: ילד | Hophal | Perfect 3ms | was born/begotten — "
            "הוּ prefix (Shureq, from Pe-Yod quiescence); Patach under R2"
        ),
    ),

    DeckCard(
        num=23, front="יוּלַד", ref="paradigm",
        root="ילד", stem="Hophal", conj="Imperfect", pgn="3ms",
        gloss="shall be born",
        section="PE-YOD/VAV (I-י/ו)",
        tag="hophal-imperfect hophal-pe-yod bbh-ch29",
        back_txt=(
            "ילד Hophal+Imperfect+3ms — \"shall be born\" — "
            "יוּ prefix: yod (prefix consonant) + Shureq (Pe-Yod quiescence + Hophal u-vowel); "
            "Patach under R2 (ל); visually identical prefix pattern to Biconsonantal (יוּקַם) — "
            "distinguished by the presence of 3 root consonants (י-ל-ד → ל-ד visible)"
        ),
        back_fd=(
            "Root: ילד | Hophal | Imperfect 3ms | shall be born — "
            "יוּ prefix (Shureq); 3 root consonants (ל + ד visible after prefix)"
        ),
    ),

    DeckCard(
        num=24, front="וַיּוּלַד", ref="Gen 4:26",
        root="ילד", stem="Hophal", conj="Wayyiqtol", pgn="3ms",
        gloss="and a son was born (to Seth)",
        section="PE-YOD/VAV (I-י/ו)",
        tag="hophal-wayyiqtol hophal-pe-yod bbh-ch29",
        back_txt=(
            "ילד Hophal+Wayyiqtol+3ms — \"and to Seth also a son was born\" — "
            "וַיּוּ prefix: Waw + Patach + Yod+Dagesh + Shureq; "
            "Dagesh forte in prefix yod (Wayyiqtol assimilation); "
            "appears dozens of times in Gen 4–11 genealogies: וַיּוּלַד = passive genealogical formula; "
            "Hiphil active הוֹלִיד = \"he begat\""
        ),
        back_fd=(
            "Root: ילד | Hophal | Wayyiqtol 3ms | and a son was born — "
            "וַיּוּ prefix; standard genealogical passive (Gen 4–11)"
        ),
    ),

    DeckCard(
        num=25, front="מוּלָד", ref="paradigm",
        root="ילד", stem="Hophal", conj="Participle", pgn="ms",
        gloss="(one) being born / newborn",
        section="PE-YOD/VAV (I-י/ו)",
        tag="hophal-participle hophal-pe-yod bbh-ch29",
        back_txt=(
            "ילד Hophal+Participle+ms — \"(one) being born / newborn\" — "
            "מוּ prefix (Mem + Shureq); Qamets under R2 (ל) = Participle signature; "
            "Pe-Yod quiescence causes Qibbuts → Shureq; "
            "compare Biconsonantal Ptc. מוּקָם — same מוּ prefix but only 2 root consonants visible"
        ),
        back_fd=(
            "Root: ילד | Hophal | Participle ms | (one) being born — "
            "מוּ prefix (Shureq); Qamets under R2"
        ),
    ),

    DeckCard(
        num=26, front="הוּבָא", ref="Lev 10:18",
        root="בוא", stem="Hophal", conj="Perfect", pgn="3ms",
        gloss="was brought in (to the sanctuary)",
        section="PE-YOD/VAV (I-י/ו)",
        tag="hophal-perfect hophal-pe-yod bbh-ch29",
        back_txt=(
            "בוא Hophal+Perfect+3ms — \"its blood was not brought into the sanctuary\" — "
            "I-ו (Pe-Vav) root: ו quiesces into prefix → Shureq; "
            "also III-א: final א quiesces → Qamets under R2 (ב) compensatory lengthening; "
            "doubly weak (I-ו + III-א): הוּ prefix + Qamets + silent א; "
            "Levitical purity law; Hiphil הֵבִיא = \"to bring\" (active)"
        ),
        back_fd=(
            "Root: בוא | Hophal | Perfect 3ms | was brought in — "
            "הוּ prefix (Shureq, I-ו); Qamets + silent א (III-א); doubly weak"
        ),
    ),

    DeckCard(
        num=27, front="יוּבָא", ref="Lev 6:30",
        root="בוא", stem="Hophal", conj="Imperfect", pgn="3ms",
        gloss="shall be brought in (as a sin offering)",
        section="PE-YOD/VAV (I-י/ו)",
        tag="hophal-imperfect hophal-pe-yod bbh-ch29",
        back_txt=(
            "בוא Hophal+Imperfect+3ms — \"any sin offering whose blood is brought into the tent\" — "
            "יוּ prefix (Shureq); Qamets under ב (III-א compensatory); silent final א; "
            "sacrificial legislation: the sin offering that enters the sanctuary cannot be eaten; "
            "cf. הוּבָא (Perfect, card 26)"
        ),
        back_fd=(
            "Root: בוא | Hophal | Imperfect 3ms | shall be brought in — "
            "יוּ prefix (Shureq); Qamets + silent א"
        ),
    ),

    DeckCard(
        num=28, front="הוּרַד", ref="Gen 39:1",
        root="ירד", stem="Hophal", conj="Perfect", pgn="3ms",
        gloss="was brought down (to Egypt)",
        section="PE-YOD/VAV (I-י/ו)",
        tag="hophal-perfect hophal-pe-yod bbh-ch29",
        back_txt=(
            "ירד Hophal+Perfect+3ms — \"Joseph was brought down to Egypt\" — "
            "I-י root: yod quiesces → Shureq; הוּ prefix; Patach under R2 (ר); "
            "Gen 39:1 uses both Hophal of ירד (הוּרַד \"was brought down\") and "
            "Hiphil of ירד (הוֹרִידֻהוּ \"they had brought him down\") — "
            "passive victim vs. active agents in same verse"
        ),
        back_fd=(
            "Root: ירד | Hophal | Perfect 3ms | was brought down — "
            "הוּ prefix (Pe-Yod quiescence → Shureq); Patach under R2"
        ),
    ),

    # ── GEMINATE / PE-NUN OVERLAP ─────────────────────────────────────────────
    # נקם: technically Pe-Nun (R1=נ assimilates), but Dagesh in ק creates
    # a geminate-looking form; BBH Ch29 treats this in the Geminate section.

    DeckCard(
        num=29, front="יֻקַּם", ref="Gen 4:15",
        root="נקם", stem="Hophal", conj="Imperfect", pgn="3ms",
        gloss="shall be avenged (sevenfold)",
        section="GEMINATE / PE-NUN OVERLAP",
        tag="hophal-imperfect hophal-pe-nun hophal-geminate bbh-ch29",
        back_txt=(
            "נקם Hophal+Imperfect+3ms — \"Cain shall be avenged sevenfold\" — "
            "Pe-Nun (נ) assimilates: יֻ + ק+Dagesh (Dagesh = assimilated נ); "
            "the Dagesh forte in ק makes this look like a Geminate form; "
            "Gen 4:15: the LORD sets a protective sign on Cain; "
            "Gen 4:24: same form used again in Lamech's boast (יֻקַּם שִׁבְעָתַיִם ... שִׁבְעִים וְשִׁבְעָה)"
        ),
        back_fd=(
            "Root: נקם | Hophal | Imperfect 3ms | shall be avenged — "
            "יֻ prefix (Qibbuts); Dagesh forte in ק (Pe-Nun assimilation); Gen 4 avenging formula"
        ),
    ),

    DeckCard(
        num=30, front="הֻקַּם", ref="paradigm",
        root="נקם", stem="Hophal", conj="Perfect", pgn="3ms",
        gloss="was avenged",
        section="GEMINATE / PE-NUN OVERLAP",
        tag="hophal-perfect hophal-pe-nun hophal-geminate bbh-ch29",
        back_txt=(
            "נקם Hophal+Perfect+3ms — \"was avenged\" — "
            "הֻ prefix (Qibbuts); Dagesh forte in ק (Pe-Nun assimilation); "
            "Patach under R2 (ק); note: in the Perfect, the assimilation produces Dagesh "
            "even though the Pe-Nun is not in the usual assimilation environment — "
            "the Hophal paradigm treats this consistently across all conjugations"
        ),
        back_fd=(
            "Root: נקם | Hophal | Perfect 3ms | was avenged — "
            "הֻ prefix; Dagesh forte in ק (Pe-Nun assimilation)"
        ),
    ),

    DeckCard(
        num=31, front="וַיֻּקַּם", ref="paradigm",
        root="נקם", stem="Hophal", conj="Wayyiqtol", pgn="3ms",
        gloss="and he/it was avenged",
        section="GEMINATE / PE-NUN OVERLAP",
        tag="hophal-wayyiqtol hophal-pe-nun hophal-geminate bbh-ch29",
        back_txt=(
            "נקם Hophal+Wayyiqtol+3ms — \"and he/it was avenged\" — "
            "וַיֻּ prefix (Waw + Patach + Yod+Dagesh + Qibbuts); "
            "Dagesh forte in ק (Pe-Nun assimilation) on top of Wayyiqtol prefix doubling; "
            "two Dagheshes: one in yod (Wayyiqtol), one in ק (Pe-Nun)"
        ),
        back_fd=(
            "Root: נקם | Hophal | Wayyiqtol 3ms | and he was avenged — "
            "וַיֻּ prefix; two Dagheshes: yod (Wayyiqtol) + ק (Pe-Nun)"
        ),
    ),

    DeckCard(
        num=32, front="מֻקָּם", ref="paradigm",
        root="נקם", stem="Hophal", conj="Participle", pgn="ms",
        gloss="(one who is) avenged",
        section="GEMINATE / PE-NUN OVERLAP",
        tag="hophal-participle hophal-pe-nun hophal-geminate bbh-ch29",
        back_txt=(
            "נקם Hophal+Participle+ms — \"(one who is) avenged\" — "
            "מֻ prefix (Mem + Qibbuts); Dagesh forte in ק (Pe-Nun assimilation); "
            "Qamets under R2 (ק) = Participle signature; "
            "compare מֻגָּד (Pe-Nun Participle, card 14) — same pattern: מֻ + R2+Dagesh + Qamets"
        ),
        back_fd=(
            "Root: נקם | Hophal | Participle ms | (one who is) avenged — "
            "מֻ prefix; Dagesh forte in ק (Pe-Nun); Qamets under R2"
        ),
    ),

    # ── PE-GUTTURAL (I-ע/ח/א/ה) ──────────────────────────────────────────────
    # Key pattern: Hophal u-class prefix unaffected; guttural at R1 takes
    # composite shewa (hateph-patach/hateph-seghol) instead of plain vocal shewa

    DeckCard(
        num=33, front="הֻעֲמַד", ref="paradigm",
        root="עמד", stem="Hophal", conj="Perfect", pgn="3ms",
        gloss="was stationed / made to stand",
        section="PE-GUTTURAL (I-ע/ח)",
        tag="hophal-perfect hophal-pe-guttural bbh-ch29",
        back_txt=(
            "עמד Hophal+Perfect+3ms — \"was stationed / made to stand\" — "
            "הֻ prefix (Qibbuts); guttural ע at R1 cannot take plain vocal shewa — "
            "takes hateph-patach (ֲ) instead; u-class prefix vowel entirely unaffected; "
            "compare Hophal Strong הֻקְטַד (plain shewa under R1) vs. הֻעֲמַד (composite shewa); "
            "Hiphil הֶעֱמִיד = \"to station, appoint\" (active)"
        ),
        back_fd=(
            "Root: עמד | Hophal | Perfect 3ms | was stationed — "
            "הֻ prefix (Qibbuts); hateph-patach under ע (guttural cannot take plain shewa)"
        ),
    ),

    DeckCard(
        num=34, front="יֻעֲמַד", ref="paradigm",
        root="עמד", stem="Hophal", conj="Imperfect", pgn="3ms",
        gloss="shall be stationed / set in place",
        section="PE-GUTTURAL (I-ע/ח)",
        tag="hophal-imperfect hophal-pe-guttural bbh-ch29",
        back_txt=(
            "עמד Hophal+Imperfect+3ms — \"shall be stationed\" — "
            "יֻ prefix (Qibbuts); hateph-patach under ע (composite shewa); "
            "Patach under R2 (מ); the Hophal u-prefix is never affected by the guttural — "
            "the guttural influence is strictly local to R1's shewa position"
        ),
        back_fd=(
            "Root: עמד | Hophal | Imperfect 3ms | shall be stationed — "
            "יֻ prefix; hateph-patach under ע; Patach under R2"
        ),
    ),

    DeckCard(
        num=35, front="מֻעֲמָד", ref="paradigm",
        root="עמד", stem="Hophal", conj="Participle", pgn="ms",
        gloss="(one who is) stationed / appointed",
        section="PE-GUTTURAL (I-ע/ח)",
        tag="hophal-participle hophal-pe-guttural bbh-ch29",
        back_txt=(
            "עמד Hophal+Participle+ms — \"(one who is) stationed\" — "
            "מֻ prefix (Qibbuts); hateph-patach under ע; Qamets under R2 (מ) = Participle; "
            "compare מֻקְטָל (strong Participle) — identical except plain shewa under R1 becomes hateph-patach"
        ),
        back_fd=(
            "Root: עמד | Hophal | Participle ms | (one who is) stationed — "
            "מֻ prefix; hateph-patach under ע; Qamets under R2"
        ),
    ),

    # ── LAMED-GUTTURAL (III-ח/ע) ─────────────────────────────────────────────
    # Key pattern: Patach furtive before word-final ח/ע in stressed open syllable

    DeckCard(
        num=36, front="יֻשְׁלַח", ref="Job 18:8",
        root="שׁלח", stem="Hophal", conj="Imperfect", pgn="3ms",
        gloss="he is cast into a net by his own feet",
        section="LAMED-GUTTURAL (III-ח/ע)",
        tag="hophal-imperfect hophal-lamed-guttural bbh-ch29",
        back_txt=(
            "שׁלח Hophal+Imperfect+3ms — \"he is cast into a net by his own feet\" — "
            "יֻ prefix (Qibbuts); Patach under R2 (שׁ); final ח with Patach furtive; "
            "Patach furtive: the glide vowel inserted before word-final guttural (ח) in open syllable — "
            "written below/right of ח, but pronounced BEFORE it; "
            "Bildad's speech to Job about the fate of the wicked"
        ),
        back_fd=(
            "Root: שׁלח | Hophal | Imperfect 3ms | is cast into a net — "
            "יֻ prefix; Patach furtive before final ח"
        ),
    ),

    DeckCard(
        num=37, front="מֻשְׁלָח", ref="Isa 27:10",
        root="שׁלח", stem="Hophal", conj="Participle", pgn="ms",
        gloss="forsaken / deserted (city)",
        section="LAMED-GUTTURAL (III-ח/ע)",
        tag="hophal-participle hophal-lamed-guttural bbh-ch29",
        back_txt=(
            "שׁלח Hophal+Participle+ms — \"a forsaken and deserted city\" — "
            "מֻ prefix (Qibbuts); Qamets under R2 (שׁ) = Participle signature; "
            "final ח with Patach furtive; "
            "Isa 27:10 eschatological vision: the fortified city left empty and abandoned; "
            "Hiphil שָׁלַח = \"to send, release\" → Hophal = \"to be sent/released/forsaken\""
        ),
        back_fd=(
            "Root: שׁלח | Hophal | Participle ms | forsaken — "
            "מֻ prefix; Qamets under R2; Patach furtive before final ח"
        ),
    ),

    # ── LAMED-ALEPH (III-א) ───────────────────────────────────────────────────
    # Key pattern: final א quiesces (silent); preceding vowel lengthens compensatorily
    # (Patach → Qamets under R2 in most forms)

    DeckCard(
        num=38, front="הֻמְצָא", ref="paradigm",
        root="מצא", stem="Hophal", conj="Perfect", pgn="3ms",
        gloss="was found / presented",
        section="LAMED-ALEPH (III-א)",
        tag="hophal-perfect hophal-lamed-aleph bbh-ch29",
        back_txt=(
            "מצא Hophal+Perfect+3ms — \"was found / presented\" — "
            "הֻ prefix (Qibbuts); Qamets under R2 (מ) — compensatory lengthening before quiesced final א; "
            "Patach → Qamets because silent א can no longer close the syllable; "
            "u-class prefix vowel unaffected; "
            "context: legal and wisdom texts where something is \"found to be\" the case"
        ),
        back_fd=(
            "Root: מצא | Hophal | Perfect 3ms | was found — "
            "הֻ prefix; Qamets + silent א (compensatory lengthening for III-א)"
        ),
    ),

    DeckCard(
        num=39, front="וַיֻּקְרָא", ref="Num 21:3",
        root="קרא", stem="Hophal", conj="Wayyiqtol", pgn="3ms",
        gloss="and the place was called (Hormah)",
        section="LAMED-ALEPH (III-א)",
        tag="hophal-wayyiqtol hophal-lamed-aleph bbh-ch29",
        back_txt=(
            "קרא Hophal+Wayyiqtol+3ms — \"and he called the name of that place Hormah\" — "
            "וַיֻּ prefix (Waw + Patach + Yod+Dagesh + Qibbuts); "
            "Qamets under R2 (ר) — compensatory lengthening before quiesced final א; "
            "Num 21:3: Israel defeats Canaanites, devotes them to destruction, "
            "names the place חׇרְמָה (Hormah = \"destruction\")"
        ),
        back_fd=(
            "Root: קרא | Hophal | Wayyiqtol 3ms | and it was called — "
            "וַיֻּ prefix; Qamets + silent א; name-giving formula"
        ),
    ),

    # ── CONTRAST / DIAGNOSTIC ─────────────────────────────────────────────────

    DeckCard(
        num=40, front="הוּקַם (Biconsonantal) vs. הוּלַד (Pe-Yod)",
        ref="—",
        root="—", stem="Hophal", conj="Perfect", pgn="3ms",
        gloss="both show Shureq prefix — how to tell them apart?",
        section="CONTRAST / DIAGNOSTIC",
        tag="hophal-diagnostic bbh-ch29",
        back_txt=(
            "Both use הוּ prefix (Shureq) — the diagnostic is ROOT CONSONANT COUNT: "
            "Biconsonantal הוּקַם: only 2 root consonants between prefix and ending (ק + מ); "
            "Pe-Yod הוּלַד: 3 root consonants — initial י quiesced, but ל + ד both visible; "
            "rule: Shureq + 2 visible root consonants = Biconsonantal; "
            "Shureq + 3 root consonants (first quiesced) = Pe-Yod/Vav"
        ),
        back_fd=(
            "Biconsonantal vs. Pe-Yod — count root consonants: "
            "הוּקַם = 2 visible (ק+מ); הוּלַד = 3 with first quiesced (י-ל-ד)"
        ),
    ),

    DeckCard(
        num=41, front="וַיֻּגַּד (Pe-Nun) vs. וַיֻּגְלָה (Lamed-He)",
        ref="—",
        root="—", stem="Hophal", conj="Wayyiqtol", pgn="3ms",
        gloss="same prefix — what distinguishes them?",
        section="CONTRAST / DIAGNOSTIC",
        tag="hophal-diagnostic bbh-ch29",
        back_txt=(
            "Same וַיֻּ prefix (Qibbuts) — the root tells the story: "
            "Pe-Nun וַיֻּגַּד: Dagesh forte in R2 (ג) reveals assimilated נ; "
            "Lamed-He וַיֻּגֶל: NO Dagesh in R2; final ה apocopated — Seghol under last consonant; "
            "rule: Dagesh in R2 → Pe-Nun; Seghol at end, no Dagesh → Lamed-He apocopation"
        ),
        back_fd=(
            "Pe-Nun (וַיֻּגַּד): Dagesh forte in R2 from assimilation · "
            "Lamed-He (וַיֻּגֶל): Seghol at end, ה apocopated — no Dagesh"
        ),
    ),

    DeckCard(
        num=42, front="What is the u-class prefix vowel in each weak class?",
        ref="—",
        root="—", stem="Hophal", conj="—", pgn="—",
        gloss="match each weak class to its prefix vowel pattern",
        section="CONTRAST / DIAGNOSTIC",
        tag="hophal-diagnostic bbh-ch29",
        back_txt=(
            "All Hophal weak forms preserve u-class under the prefix — what changes is the FORM: "
            "Strong / Pe-Guttural / Pe-Nun / Lamed-weak: Qibbuts (הֻ / יֻ / מֻ); "
            "Biconsonantal / Pe-Yod/Vav: Shureq (הוּ / יוּ / מוּ) — "
            "medial/initial vowel letter merges with Hophal u-vowel producing Shureq; "
            "KEY RULE: Qibbuts = u-class explicit; Shureq = u-class contracted/merged"
        ),
        back_fd=(
            "Strong/Pe-Nun/Lamed-weak → Qibbuts (הֻ/יֻ/מֻ) · "
            "Biconsonantal/Pe-Yod → Shureq (הוּ/יוּ/מוּ)"
        ),
    ),

    DeckCard(
        num=43, front="מֻכֶּה (Isa 53:4) — what two weak classes combine here?",
        ref="Isa 53:4",
        root="נכה", stem="Hophal", conj="Participle", pgn="ms",
        gloss="stricken (by God) — Isaiah 53 Servant Song",
        section="CONTRAST / DIAGNOSTIC",
        tag="hophal-diagnostic hophal-pe-nun hophal-lamed-he bbh-ch29",
        back_txt=(
            "נכה Hophal+Participle+ms — \"stricken by God\" (Isa 53:4) — "
            "DOUBLY WEAK: I-נ (Pe-Nun) + III-ה (Lamed-He); "
            "מֻ prefix (Qibbuts); Dagesh forte in כ (Pe-Nun assimilation); "
            "Seghol + ה = III-ה Participle ending (cf. Qamets in strong Ptc.); "
            "Isaiah 53:4 — the Servant Song: \"surely he has borne our griefs... yet we esteemed him stricken\"; "
            "Hiphil נָכָה = \"to strike\" (active); Hophal = \"to be struck\""
        ),
        back_fd=(
            "Root: נכה | Hophal | Participle ms | stricken — "
            "doubly weak: I-נ (Dagesh in כ) + III-ה (Seghol+ה ending); Isa 53:4"
        ),
    ),

    DeckCard(
        num=44, front="וַיּוּלַד vs. הוּלַד vs. יוּלַד — how do you distinguish?",
        ref="—",
        root="ילד", stem="Hophal", conj="—", pgn="—",
        gloss="three Pe-Yod forms from the same root",
        section="CONTRAST / DIAGNOSTIC",
        tag="hophal-diagnostic hophal-pe-yod bbh-ch29",
        back_txt=(
            "ילד Hophal — three forms, all Shureq prefix: "
            "הוּלַד: He prefix → Perfect 3ms (\"was born/begotten\"); "
            "יוּלַד: Yod prefix → Imperfect 3ms (\"shall be born\"); "
            "וַיּוּלַד: Waw + Patach + Yod+Dagesh → Wayyiqtol 3ms (\"and ... was born\") — narrative past; "
            "RULE: prefix consonant identifies tense; Dagesh forte in the yod = Wayyiqtol; "
            "all three appear in Gen 4–11 genealogies"
        ),
        back_fd=(
            "ילד Hophal: הוּ- = Perfect · יוּ- = Imperfect · וַיּוּ- (Dagesh in yod) = Wayyiqtol"
        ),
    ),
]

# ── Configuration ─────────────────────────────────────────────────────────────

CONFIG = DeckConfig(
    chapter=29,
    stem="Hophal",
    quality="Weak",
    deck_name=DECK,
    description="""\
*44 cards covering all eight Hophal weak root classes.*
*The u-class prefix vowel (Shureq וּ or Qibbuts ֻ) is present in every card — \
the weak class only changes what happens to the root consonants around it.*

*Primary roots: **קום** (set up) · **מות** (die/put to death) · **שׁוב** (return) · \
**נגד** (tell/report) · **גלה** (exile) · **ילד** (bear/beget) · **בוא** (bring) · **ירד** (bring down)*
*Import `ch29-morphology-deck.txt` directly into Anki (File → Import).*""",
    diagnostics=[
        ("What prefix vowel is present in EVERY Hophal form regardless of weak class?",
         "u-class: **Qibbuts (ֻ)** for strong, Pe-Nun, Lamed-weak, Pe-Guttural — "
         "**Shureq (וּ)** for Biconsonantal and Pe-Yod/Vav"),
        ("Biconsonantal הוּקַם vs. Pe-Yod הוּלַד — both show Shureq; how to tell apart?",
         "Count root consonants: 2 visible (ק+מ) = Biconsonantal; 3 with first quiesced (ל+ד) = Pe-Yod"),
        ("What does Dagesh forte in R2 signal in a Hophal prefix conjugation?",
         "Pe-Nun assimilation — root נ has assimilated into R2; e.g., יֻגַּד (נגד), יֻכֶּה (נכה)"),
        ("What happened to the ה in וַיֻּגֶל (Lamed-He Wayyiqtol)?",
         "Apocopation — final ה drops in Wayyiqtol; Seghol under last root consonant remains"),
        ("What is מוֹת יוּמַת and why does it have two verb forms?",
         "Legal formula: מוֹת = Qal Inf.Abs. (intensifier) + יוּמַת = Hophal Impf. 3ms; "
         "together = \"shall SURELY be put to death\""),
        ("Pe-Guttural: what changes when R1 is ע or ח?",
         "Vocal shewa under R1 becomes composite shewa (hateph-patach ֲ for ע/ח); "
         "Hophal u-prefix is entirely unaffected"),
    ],
    coverage=[
        {"conj": "Perfect", "detail": "Biconsonantal (קום, שׁוב, מות) · Pe-Nun (נגד, נכה) · Lamed-He (גלה) · Pe-Yod (ילד, בוא, ירד) · Geminate (נקם) · Pe-Guttural (עמד) · Lamed-Aleph (מצא)", "cards": "1–3, 10–11, 15, 17–18, 22, 26, 28, 30, 33, 38"},  # noqa: E501
        {"conj": "Imperfect", "detail": "Biconsonantal (קום, מות) · Pe-Nun (נגד, נכה) · Lamed-He (גלה) · Pe-Yod (ילד, בוא) · Geminate (נקם) · Pe-Guttural (עמד) · Lamed-Guttural (שׁלח)", "cards": "4–5, 12, 16, 19, 23, 27, 29, 34, 36"},  # noqa: E501
        {"conj": "Wayyiqtol", "detail": "Biconsonantal (קום, שׁוב) · Pe-Nun (נגד) · Lamed-He (גלה, apocopated) · Pe-Yod (ילד, בוא) · Geminate (נקם) · Lamed-Aleph (קרא)", "cards": "6–7, 13, 20, 24, 31, 39"},  # noqa: E501
        {"conj": "Weqatal", "detail": "Pe-Nun (נגד)", "cards": "11"},
        {"conj": "Inf. Absolute", "detail": "Pe-Nun (נגד)", "cards": "14"},
        {"conj": "Participle ms", "detail": "Biconsonantal (קום) · Pe-Nun (נכה) · Lamed-He (גלה) · Pe-Yod (ילד) · Geminate (נקם) · Pe-Guttural (עמד) · Lamed-Guttural (שׁלח)", "cards": "8, 15, 21, 25, 32, 35, 37"},  # noqa: E501
        {"conj": "Formula", "detail": "מוֹת יוּמַת (Inf.Abs. + Hophal Impf.)", "cards": "9"},
        {"conj": "Contrast / Diagnostic", "detail": "Biconsonantal vs. Pe-Yod · Pe-Nun vs. Lamed-He Wayyiqtol · u-class prefix survey · doubly weak נכה (Isa 53:4) · Pe-Yod tense identification", "cards": "40–44"},  # noqa: E501
    ],
)

# ── Run ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    writer = MorphologyDeckWriter(CONFIG, CARDS)
    writer.write_all(OUT_DIR, PREFIX)
