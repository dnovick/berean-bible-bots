"""
Run all exercise PDF builders.

Usage:
    python3 -m bible_grammar.exercise_pdf           # skip existing PDFs
    python3 -m bible_grammar.exercise_pdf --force   # rebuild everything
"""
import os
import sys

if '--force' in sys.argv:
    os.environ['PDF_FORCE_REBUILD'] = '1'

from .bbh import (
    build_ch1_letter_recognition,
    build_ch2_vowel_identification,
    build_ch3_syllable_division,
    build_ch4_noun_parsing,
    build_ch5_article_and_vav,
    build_ch6_preposition_parsing,
    build_ch7_adjective_usage,
    build_ch8_pronoun_identification,
    build_ch9_suffix_parsing,
    build_ch10_construct_chain,
    build_ch11_number_identification,
    build_ch12_verb_overview,
    build_ch13_parsing_drill,
    build_ch13_passage_exercise,
    build_ch14_passage_exercise,
    build_ch14_weak_form_id,
    build_ch15_parsing_drill,
    build_ch15_passage_exercise,
    build_ch16_passage_exercise,
    build_ch16_weak_form_id,
    build_ch17_parsing_drill,
    build_ch17_passage_exercise,
    build_ch18_parsing_drill,
    build_ch18_passage_exercise,
    build_ch19_parsing_drill,
    build_ch19_passage_exercise,
    build_ch20_parsing_drill,
    build_ch20_passage_exercise,
    build_ch21_parsing_drill,
    build_ch21_passage_exercise,
    build_ch22_parsing_drill,
    build_ch22_passage_exercise,
    build_ch23_clause_analysis,
    build_ch23_passage_exercise,
    build_ch24_exercise,
    build_ch24_contrast_exercise,
    build_ch24_function_sort_exercise,
    build_ch25_exercise,
    build_ch25_weak_form_id_exercise,
    build_ch26_exercise,
    build_ch26_contrast_exercise,
    build_ch26_function_sort_exercise,
    build_ch26_stem_id_drill,
    build_ch27_exercise,
    build_ch27_weak_form_id_exercise,
    build_ch27_nh_contrast_exercise,
    build_ch27_bg_drill_exercise,
    build_ch27_contrast_exercise,
    build_ch27_function_sort_exercise,
    build_ch27_stem_id_drill,
    build_ch28_hophal_exercise,
    build_ch28_hophal_hiphil_contrast_exercise,
    build_ch29_hophal_weak_exercise,
    build_ch29_weak_form_id_exercise,
    build_ch30_exercise,
    build_ch30_function_sort_exercise,
    build_ch30_qal_piel_contrast_exercise,
    build_ch31_piel_weak_exercise,
    build_ch31_weak_form_id_exercise,
    build_ch32_exercise,
    build_ch32_piel_pual_contrast_exercise,
    build_ch32_function_sort_exercise,
    build_ch32_qal_piel_pual_contrast_exercise,
    build_ch32_stem_id_drill,
    build_ch33_exercise,
    build_ch33_weak_form_id_exercise,
    build_ch33_qal_piel_pual_contrast_exercise,
    build_ch33_function_sort_exercise,
    build_ch33_stem_id_drill,
    build_ch34_hithpael_exercise,
    build_ch34_function_sort_exercise,
    build_ch35_hithpael_weak_exercise,
    build_ch35_weak_form_id_exercise,
    build_ch13_qal_perfect_paradigm_drill,
    build_ch15_qal_imperfect_paradigm_drill,
    build_ch17_wayyiqtol_paradigm_drill,
    build_ch18_qal_imperative_paradigm_drill,
    build_ch19_verb_suffix_paradigm_drill,
    build_ch20_qal_ic_paradigm_drill,
    build_ch21_qal_ia_paradigm_drill,
    build_ch22_qal_participle_paradigm_drill,
    build_ch24_niphal_paradigm_drill,
    build_ch26_hiphil_paradigm_drill,
    build_ch28_hophal_paradigm_drill,
    build_ch29_hophal_weak_paradigm_drill,
    build_ch30_piel_paradigm_drill,
    build_ch31_piel_weak_paradigm_drill,
    build_ch32_pual_paradigm_drill,
    build_ch33_pual_weak_paradigm_drill,
    build_ch34_hithpael_paradigm_drill,
    build_ch35_hithpael_weak_paradigm_drill,
    build_ch24_stem_id_drill,
    build_ch25_niphal_weak_paradigm_drill,
    build_ch25_qal_niphal_contrast,
    build_ch25_function_sort,
    build_ch25_stem_id_drill,
    build_ch28_stem_id_drill,
    build_ch29_hiphil_passive_drill,
    build_ch29_qal_hiphil_hophal_contrast,
    build_ch29_stem_id_drill,
    build_ch30_stem_id_drill,
    build_ch31_qal_piel_contrast,
    build_ch31_function_sort,
    build_ch31_stem_id_drill,
    build_ch34_qal_piel_hithpael_contrast,
    build_ch34_stem_id_drill,
    build_ch35_qal_piel_hithpael_contrast,
    build_ch35_function_sort,
    build_ch35_stem_id_drill,
)
from .bbg import (
    build_bbg_ch3_alphabet_drill,
    build_bbg_ch4_syllable_drill,
    build_bbg_ch6_nom_acc_parsing,
    build_bbg_ch7_gen_dat_parsing,
    build_bbg_ch7_article_id,
    build_bbg_ch8_preposition_parsing,
    build_bbg_ch9_adjective_parsing,
    build_bbg_ch10_third_decl_parsing,
    build_bbg_ch11_pronoun_parsing,
    build_bbg_ch12_autos_parsing,
    build_bbg_ch13_demonstrative_parsing,
    build_bbg_ch14_relative_parsing,
    build_bbg_ch16_present_active_parsing,
    build_bbg_ch17_contract_verb_parsing,
    build_bbg_ch18_middle_passive_parsing,
    build_bbg_ch19_future_parsing,
    build_bbg_ch20_stem_change_drill,
    build_bbg_ch21_imperfect_parsing,
    build_bbg_ch22_second_aorist_parsing,
    build_bbg_ch22_aorist_contrast,
    build_bbg_ch23_first_aorist_parsing,
    build_bbg_ch24_aorist_future_passive_parsing,
    build_bbg_ch24_passive_formation,
    build_bbg_ch25_perfect_parsing,
    build_bbg_ch27_present_participle_parsing,
    build_bbg_ch27_participle_use_sort,
    build_bbg_ch28_aorist_participle_parsing,
    build_bbg_ch28_participle_tense_contrast,
    build_bbg_ch29_adjectival_participle_parsing,
    build_bbg_ch30_perfect_participle_genabs,
    build_bbg_ch31_subjunctive_parsing,
    build_bbg_ch31_subjunctive_use_sort,
    build_bbg_ch32_infinitive_parsing,
    build_bbg_ch33_imperative_parsing,
    build_bbg_ch33_prohibition_drill,
    build_bbg_ch34_didomi_parsing,
    build_bbg_ch35_conditionals_drill,
    build_bbg_ch36_mi_verbs_parsing,
)
from .bba import (
    build_bba_ch1_letter_recognition,
    build_bba_ch2_vowel_identification,
    build_bba_ch3_syllabification_drill,
    build_bba_ch4_noun_identification,
    build_bba_ch5_determined_state_drill,
    build_bba_ch6_construct_chain_drill,
    build_bba_ch7_preposition_drill,
    build_bba_ch8_suffix_drill,
    build_bba_ch9_pronoun_drill,
    build_bba_ch10_adjective_number_drill,
    build_bba_ch11_particle_drill,
    build_bba_ch12_verb_intro_drill,
    build_bba_ch13_peal_perfect_drill,
    build_bba_ch14_peal_imperfect_drill,
    build_bba_ch15_peal_imperative_drill,
    build_bba_ch16_peal_infinitive_drill,
    build_bba_ch17_peal_participle_drill,
    build_bba_ch13_peal_contrast,
    build_bba_ch18_passive_stems_drill,
    build_bba_ch18_stem_contrast,
    build_bba_ch19_pael_stem_drill,
    build_bba_ch19_pael_peal_contrast,
    build_bba_ch20_hithpaal_drill,
    build_bba_ch20_hithpaal_function_sort,
    build_bba_ch21_haphel_stem_drill,
    build_bba_ch21_haphel_peal_contrast,
    build_bba_ch22_causative_passive_drill,
)

# Ch1–Ch23 exercises (Hebrew BBH)
builders_ch1_23 = [
    build_ch1_letter_recognition,
    build_ch2_vowel_identification,
    build_ch3_syllable_division,
    build_ch4_noun_parsing,
    build_ch5_article_and_vav,
    build_ch6_preposition_parsing,
    build_ch7_adjective_usage,
    build_ch8_pronoun_identification,
    build_ch9_suffix_parsing,
    build_ch10_construct_chain,
    build_ch11_number_identification,
    build_ch12_verb_overview,
    build_ch13_parsing_drill,
    build_ch13_passage_exercise,
    build_ch14_passage_exercise,
    build_ch14_weak_form_id,
    build_ch15_parsing_drill,
    build_ch15_passage_exercise,
    build_ch16_passage_exercise,
    build_ch16_weak_form_id,
    build_ch17_parsing_drill,
    build_ch17_passage_exercise,
    build_ch18_parsing_drill,
    build_ch18_passage_exercise,
    build_ch19_parsing_drill,
    build_ch19_passage_exercise,
    build_ch20_parsing_drill,
    build_ch20_passage_exercise,
    build_ch21_parsing_drill,
    build_ch21_passage_exercise,
    build_ch22_parsing_drill,
    build_ch22_passage_exercise,
    build_ch23_clause_analysis,
    build_ch23_passage_exercise,
]
for fn in builders_ch1_23:
    try:
        fn()
    except Exception as exc:
        print(f'ERROR in {fn.__name__}: {exc}')

# Ch24+ exercises (existing)
build_ch24_exercise()
build_ch24_contrast_exercise()
build_ch24_function_sort_exercise()
build_ch25_exercise()
build_ch25_weak_form_id_exercise()
build_ch26_exercise()
build_ch26_contrast_exercise()
build_ch26_function_sort_exercise()
build_ch26_stem_id_drill()
build_ch27_exercise()
build_ch27_weak_form_id_exercise()
build_ch27_nh_contrast_exercise()
build_ch27_bg_drill_exercise()
build_ch27_contrast_exercise()
build_ch27_function_sort_exercise()
build_ch27_stem_id_drill()
build_ch28_hophal_exercise()
build_ch28_hophal_hiphil_contrast_exercise()
build_ch29_hophal_weak_exercise()
build_ch29_weak_form_id_exercise()
build_ch30_exercise()
build_ch30_function_sort_exercise()
build_ch30_qal_piel_contrast_exercise()
build_ch31_piel_weak_exercise()
build_ch31_weak_form_id_exercise()
build_ch32_exercise()
build_ch32_piel_pual_contrast_exercise()
build_ch32_function_sort_exercise()
build_ch32_qal_piel_pual_contrast_exercise()
build_ch32_stem_id_drill()
build_ch33_exercise()
build_ch33_weak_form_id_exercise()
build_ch33_qal_piel_pual_contrast_exercise()
build_ch33_function_sort_exercise()
build_ch33_stem_id_drill()
build_ch34_hithpael_exercise()
build_ch34_function_sort_exercise()
build_ch35_hithpael_weak_exercise()
build_ch35_weak_form_id_exercise()

# New stem-id, contrast, function-sort, and paradigm drills (Ch24–Ch35)
new_builders = [
    build_ch24_stem_id_drill,
    build_ch25_niphal_weak_paradigm_drill,
    build_ch25_qal_niphal_contrast,
    build_ch25_function_sort,
    build_ch25_stem_id_drill,
    build_ch28_stem_id_drill,
    build_ch29_hiphil_passive_drill,
    build_ch29_qal_hiphil_hophal_contrast,
    build_ch29_stem_id_drill,
    build_ch30_stem_id_drill,
    build_ch31_qal_piel_contrast,
    build_ch31_function_sort,
    build_ch31_stem_id_drill,
    build_ch34_qal_piel_hithpael_contrast,
    build_ch34_stem_id_drill,
    build_ch35_qal_piel_hithpael_contrast,
    build_ch35_function_sort,
    build_ch35_stem_id_drill,
]
for fn in new_builders:
    try:
        fn()
    except Exception as exc:
        print(f'ERROR in {fn.__name__}: {exc}')

# Paradigm completion exercises (BBH Ch13–Ch35)
paradigm_builders = [
    build_ch13_qal_perfect_paradigm_drill,
    build_ch15_qal_imperfect_paradigm_drill,
    build_ch17_wayyiqtol_paradigm_drill,
    build_ch18_qal_imperative_paradigm_drill,
    build_ch19_verb_suffix_paradigm_drill,
    build_ch20_qal_ic_paradigm_drill,
    build_ch21_qal_ia_paradigm_drill,
    build_ch22_qal_participle_paradigm_drill,
    build_ch24_niphal_paradigm_drill,
    build_ch26_hiphil_paradigm_drill,
    build_ch28_hophal_paradigm_drill,
    build_ch29_hophal_weak_paradigm_drill,
    build_ch30_piel_paradigm_drill,
    build_ch31_piel_weak_paradigm_drill,
    build_ch32_pual_paradigm_drill,
    build_ch33_pual_weak_paradigm_drill,
    build_ch34_hithpael_paradigm_drill,
    build_ch35_hithpael_weak_paradigm_drill,
]
for fn in paradigm_builders:
    try:
        fn()
    except Exception as exc:
        print(f'ERROR in {fn.__name__}: {exc}')

# BBG (Greek) exercises
bbg_builders = [
    build_bbg_ch3_alphabet_drill,
    build_bbg_ch4_syllable_drill,
    build_bbg_ch6_nom_acc_parsing,
    build_bbg_ch7_gen_dat_parsing,
    build_bbg_ch7_article_id,
    build_bbg_ch8_preposition_parsing,
    build_bbg_ch9_adjective_parsing,
    build_bbg_ch10_third_decl_parsing,
    build_bbg_ch11_pronoun_parsing,
    build_bbg_ch12_autos_parsing,
    build_bbg_ch13_demonstrative_parsing,
    build_bbg_ch14_relative_parsing,
    build_bbg_ch16_present_active_parsing,
    build_bbg_ch17_contract_verb_parsing,
    build_bbg_ch18_middle_passive_parsing,
    build_bbg_ch19_future_parsing,
    build_bbg_ch20_stem_change_drill,
    build_bbg_ch21_imperfect_parsing,
    build_bbg_ch22_second_aorist_parsing,
    build_bbg_ch22_aorist_contrast,
    build_bbg_ch23_first_aorist_parsing,
    build_bbg_ch24_aorist_future_passive_parsing,
    build_bbg_ch24_passive_formation,
    build_bbg_ch25_perfect_parsing,
    build_bbg_ch27_present_participle_parsing,
    build_bbg_ch27_participle_use_sort,
    build_bbg_ch28_aorist_participle_parsing,
    build_bbg_ch28_participle_tense_contrast,
    build_bbg_ch29_adjectival_participle_parsing,
    build_bbg_ch30_perfect_participle_genabs,
    build_bbg_ch31_subjunctive_parsing,
    build_bbg_ch31_subjunctive_use_sort,
    build_bbg_ch32_infinitive_parsing,
    build_bbg_ch33_imperative_parsing,
    build_bbg_ch33_prohibition_drill,
    build_bbg_ch34_didomi_parsing,
    build_bbg_ch35_conditionals_drill,
    build_bbg_ch36_mi_verbs_parsing,
]
for fn in bbg_builders:
    try:
        fn()
    except Exception as exc:
        print(f'ERROR in {fn.__name__}: {exc}')

# BBA (Biblical Aramaic) exercises
bba_builders = [
    build_bba_ch1_letter_recognition,
    build_bba_ch2_vowel_identification,
    build_bba_ch3_syllabification_drill,
    build_bba_ch4_noun_identification,
    build_bba_ch5_determined_state_drill,
    build_bba_ch6_construct_chain_drill,
    build_bba_ch7_preposition_drill,
    build_bba_ch8_suffix_drill,
    build_bba_ch9_pronoun_drill,
    build_bba_ch10_adjective_number_drill,
    build_bba_ch11_particle_drill,
    build_bba_ch12_verb_intro_drill,
    build_bba_ch13_peal_perfect_drill,
    build_bba_ch13_peal_contrast,
    build_bba_ch14_peal_imperfect_drill,
    build_bba_ch15_peal_imperative_drill,
    build_bba_ch16_peal_infinitive_drill,
    build_bba_ch17_peal_participle_drill,
    build_bba_ch18_passive_stems_drill,
    build_bba_ch18_stem_contrast,
    build_bba_ch19_pael_stem_drill,
    build_bba_ch19_pael_peal_contrast,
    build_bba_ch20_hithpaal_drill,
    build_bba_ch20_hithpaal_function_sort,
    build_bba_ch21_haphel_stem_drill,
    build_bba_ch21_haphel_peal_contrast,
    build_bba_ch22_causative_passive_drill,
]
for fn in bba_builders:
    try:
        fn()
    except Exception as exc:
        print(f'ERROR in {fn.__name__}: {exc}')
