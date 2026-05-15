# ── Core data access ──────────────────────────────────────────────────────────
from .core.query import query, translation_query, lxx_query
from .nt.greek_prepositions import (
    greek_prep_frequency, greek_prep_by_book, greek_prep_distribution_table,
    greek_prep_cases, greek_prep_collocates, compare_greek_preps, nt_lxx_compare,
    print_greek_prep_frequency, print_greek_prep_by_book, print_greek_prep_distribution,
    print_greek_prep_cases, print_greek_prep_collocates,
    print_compare_greek_preps, print_nt_lxx_compare,
    NT_MAJOR_PREPS, LXX_MAJOR_PREPS, NT_BOOK_GROUPS, LXX_BOOK_GROUPS,
)
from .ot.prepositions import (
    prep_frequency, prep_by_book, prep_distribution_table,
    prep_collocates, prep_object_types, compare_preps,
    print_prep_frequency, print_prep_by_book, print_prep_distribution,
    print_prep_collocates, print_compare_preps,
    MAJOR_PREPS, PREP_GLOSS, BOOK_GROUPS,
)
from .lexical.stats import freq_table
from .core.alignment import translation_equivalents, hebrew_sources
from .core.ibm_align import translation_equivalents_w, hebrew_sources_w
from .intertextuality.quotations import nt_quotations, verse_comparison, quotation_table, quotation_summary
from .intertextuality.lxx_consistency import lxx_consistency, print_lxx_consistency, consistency_heatmap, batch_consistency  # noqa: E501
from .lexical.concordance import concordance, lemma_frequency, top_lemmas
from .reporting.profiles import book_profile, print_profile, save_profile_report, batch_profiles
from .lexical.wordstudy import word_study, print_word_study, word_study_table, resolve_strongs
from .intertextuality.parallel import parallel_passage, print_parallel, parallel_words
from .lexical.hapax import hapax_legomena, hapax_table, hapax_summary
from .lexical.termmap import term_map, print_term_map, term_map_table, THEOLOGICAL_TERMS
from .lexical.phrase import phrase_search, print_phrase_results, proximity_search, print_proximity_results
from .lexical.collocation import collocations, print_collocations, collocation_network
from .lexical.morph_chart import morph_distribution, print_morph_distribution, morph_chart
from .lexical.semantic_profile import semantic_profile, print_semantic_profile, save_semantic_profile
from .lexical.synonym import compare_synonyms, print_synonym_comparison, synonym_table
from .intertextuality.quotation_align import quotation_align, print_quotation_align, batch_align
from .names.divine_names import (divine_name_table, divine_name_summary, divine_name_by_section,
                           print_divine_names, divine_names_chart, divine_names_report,
                           OT_DIVINE_NAMES, NT_DIVINE_NAMES, LXX_DIVINE_NAMES)
from .discourse.genre_compare import (genre_compare, print_genre_compare, genre_heatmap, genre_report,
                            OT_GENRES, NT_GENRES)
from .intertextuality.intertextuality import (intertextuality, print_intertextuality,
                              intertextuality_graph, intertextuality_report)
from .names.christological_titles import (title_counts, print_title_counts,
                                    title_chart, title_verses, title_report,
                                    TITLE_REGISTRY)
# ── Syntax trees & role search ────────────────────────────────────────────────
from .core.syntax import (load_syntax, query_syntax, speech_verbs, referent_chain,
                     clause_roles, jesus_speaking_verses, MACULA_BOOK_MAP)
from .core.syntax_ot import (load_syntax_ot, query_syntax_ot, lxx_alignment,
                        clause_roles_ot, MACULA_OT_BOOK_MAP)
from .names.role_search import (subject_verbs, verb_subjects, print_role_summary,
                          subject_objects, object_verbs, print_object_summary,
                          role_chart, divine_action_comparison, role_report,
                          GOD_OT, GOD_NT, JESUS_NT)
from .core.lxx_query import (load_lxx_data, query_lxx, lxx_freq_table,
                        lxx_concordance, lxx_verb_stats, lxx_by_book,
                        print_lxx_query, LXX_BOOK_ORDER)
from .ot.ot_speaker import (speaker_verses, divine_speech_by_book, who_speaks,
                         divine_speech_verses, print_speaker_summary,
                         print_divine_speech_by_book, speaker_report,
                         GOD_OT_SPEECH, SPEECH_VERB_STRONGS)
from .lexical.domain_search import (query_domain, top_domain_words, domain_profile,
                            domain_role_search, domain_comparison,
                            print_domain_summary, print_domain_role,
                            DOMAIN_NAMES, THEOLOGY_DOMAINS)
from .lexical.trajectory import (word_trajectory, print_trajectory,
                         trajectory_chart, save_trajectory_report,
                         batch_trajectories)
from .reporting.theological_reports import (run_theological_report, run_all_theological_reports,
                                  print_all_trajectories, theological_summary_table,
                                  print_theological_summary,
                                  THEOLOGICAL_TRAJECTORIES)
# ── OT Hebrew poetry & verbal syntax ─────────────────────────────────────────
from .ot.poetry import (split_cola, verse_cola, verse_parallel_pairs,
                     book_word_pairs, parallelism_type,
                     book_parallelism_stats, compare_poetry_books,
                     print_verse_analysis, print_book_pairs,
                     print_parallelism_stats, poetry_report,
                     is_superscription, POETRY_BOOKS,
                     detect_chiasm, print_chiasm,
                     detect_acrostic, print_acrostic,
                     acrostic_known, KNOWN_ACROSTICS,
                     verse_meter, book_meter_stats,
                     print_meter_stats, print_verse_meter)
from .verbal_syntax import (
    verb_form_profile, print_verb_form_profile, verb_form_chart,
    wayyiqtol_chains, print_wayyiqtol_chains,
    infinitive_usage, print_infinitive_usage,
    clause_type_profile, print_clause_type_profile,
    stem_distribution, print_stem_distribution, stem_chart,
    verbal_syntax_report,
    VERB_FORM_ORDER, VERB_FORM_LABELS,
    disjunctive_clauses, print_disjunctive_clauses,
    disjunctive_in_chains, print_disjunctive_in_chains,
    conditional_clauses, print_conditional_clauses,
    conditional_summary, print_conditional_summary,
    relative_clauses, print_relative_clauses,
    relative_clause_summary, print_relative_summary,
    aspect_comparison, print_aspect_comparison,
    aspect_comparison_chart, GENRE_SETS,
    discourse_particles, print_discourse_particles,
    discourse_particle_summary, print_particle_summary,
)
# ── OT Hebrew verb stems ──────────────────────────────────────────────────────
from .stems.qal import (
    qal_data, qal_conjugation_profile, qal_top_roots,
    qal_root_conjugation, qal_book_distribution,
    qal_stem_comparison, qal_dominant_roots,
    qal_semantic_categories,
    print_qal_overview, print_qal_conjugation,
    print_qal_top_roots, print_qal_root_conjugation,
    print_qal_book_distribution, print_qal_dominant_roots,
    print_qal_semantic_categories,
    qal_conjugation_chart, qal_book_chart,
    qal_stem_chart, qal_root_heatmap,
    qal_semantic_chart, qal_top_roots_chart,
    qal_report,
)
from .stems.hophal import (
    hophal_data, hophal_conjugation_profile, hophal_top_roots,
    hophal_root_conjugation, hophal_book_distribution,
    hophal_stem_comparison, hophal_dominant_roots,
    hophal_semantic_categories,
    print_hophal_overview, print_hophal_conjugation,
    print_hophal_top_roots, print_hophal_root_conjugation,
    print_hophal_book_distribution, print_hophal_dominant_roots,
    print_hophal_semantic_categories,
    hophal_conjugation_chart, hophal_book_chart,
    hophal_stem_chart, hophal_root_heatmap,
    hophal_semantic_chart, hophal_top_roots_chart,
    hophal_report,
)
from .stems.hiphil import (
    hiphil_data, hiphil_conjugation_profile, hiphil_top_roots,
    hiphil_root_conjugation, hiphil_book_distribution,
    hiphil_stem_comparison, hiphil_dominant_roots,
    hiphil_semantic_categories,
    print_hiphil_overview, print_hiphil_conjugation,
    print_hiphil_top_roots, print_hiphil_root_conjugation,
    print_hiphil_book_distribution, print_hiphil_dominant_roots,
    print_hiphil_semantic_categories,
    hiphil_conjugation_chart, hiphil_book_chart,
    hiphil_stem_chart, hiphil_root_heatmap,
    hiphil_semantic_chart, hiphil_top_roots_chart,
    hiphil_report,
)
from .stems.niphal import (
    niphal_data, niphal_conjugation_profile, niphal_top_roots,
    niphal_root_conjugation, niphal_book_distribution,
    niphal_stem_comparison, niphal_dominant_roots,
    niphal_semantic_categories,
    print_niphal_overview, print_niphal_conjugation,
    print_niphal_top_roots, print_niphal_root_conjugation,
    print_niphal_book_distribution, print_niphal_dominant_roots,
    print_niphal_semantic_categories,
    niphal_conjugation_chart, niphal_book_chart,
    niphal_stem_chart, niphal_root_heatmap,
    niphal_semantic_chart, niphal_top_roots_chart,
    niphal_report,
)
from .stems.piel import (
    piel_data, piel_conjugation_profile, piel_top_roots,
    piel_root_conjugation, piel_book_distribution,
    piel_stem_comparison, piel_dominant_roots,
    piel_semantic_categories,
    print_piel_overview, print_piel_conjugation,
    print_piel_top_roots, print_piel_root_conjugation,
    print_piel_book_distribution, print_piel_dominant_roots,
    print_piel_semantic_categories,
    piel_conjugation_chart, piel_book_chart,
    piel_stem_chart, piel_root_heatmap,
    piel_semantic_chart, piel_top_roots_chart,
    piel_report,
)
from .stems.pual import (
    pual_data, pual_conjugation_profile, pual_top_roots,
    pual_root_conjugation, pual_book_distribution,
    pual_stem_comparison, pual_dominant_roots,
    pual_semantic_categories,
    print_pual_overview, print_pual_conjugation,
    print_pual_top_roots, print_pual_root_conjugation,
    print_pual_book_distribution, print_pual_dominant_roots,
    print_pual_semantic_categories,
    pual_conjugation_chart, pual_book_chart,
    pual_stem_chart, pual_root_heatmap,
    pual_semantic_chart, pual_top_roots_chart,
    pual_report,
)
from .stems.hithpael import (
    hithpael_data, hithpael_conjugation_profile, hithpael_top_roots,
    hithpael_root_conjugation, hithpael_book_distribution,
    hithpael_stem_comparison, hithpael_dominant_roots,
    hithpael_semantic_categories,
    print_hithpael_overview, print_hithpael_conjugation,
    print_hithpael_top_roots, print_hithpael_root_conjugation,
    print_hithpael_book_distribution, print_hithpael_dominant_roots,
    print_hithpael_semantic_categories,
    hithpael_conjugation_chart, hithpael_book_chart,
    hithpael_stem_chart, hithpael_root_heatmap,
    hithpael_semantic_chart, hithpael_top_roots_chart,
    hithpael_report,
)
# ── Biblical Aramaic ──────────────────────────────────────────────────────────
from .ot.aramaic_profile import (
    aramaic_data, aramaic_verb_data,
    aramaic_stem_profile, aramaic_conj_profile, aramaic_stem_conj,
    aramaic_top_roots, aramaic_book_distribution, aramaic_stem_by_book,
    print_aramaic_overview, print_aramaic_stem_profile, print_aramaic_conj_profile,
    print_aramaic_stem_conj, print_aramaic_top_roots, print_aramaic_book_distribution,
    aramaic_stem_chart, aramaic_conj_chart, aramaic_stem_book_chart,
    STEM_ORDER as ARAMAIC_STEM_ORDER, CONJ_ORDER as ARAMAIC_CONJ_ORDER,
)
from .ot.aramaic_nominal import (
    aramaic_noun_data, aramaic_pron_data, aramaic_prep_data, aramaic_adj_data,
    aramaic_noun_state_profile, aramaic_noun_gender_profile, aramaic_noun_number_profile,
    aramaic_noun_gender_state, aramaic_noun_top_lemmas, aramaic_noun_state_by_book,
    aramaic_pron_type_profile, aramaic_prep_frequency, aramaic_class_distribution,
    print_aramaic_nominal_overview, print_aramaic_noun_state, print_aramaic_noun_gender,
    print_aramaic_noun_top_lemmas, print_aramaic_noun_state_by_book,
    print_aramaic_pron_profile, print_aramaic_prep_frequency,
    aramaic_noun_state_chart, aramaic_noun_state_book_chart, aramaic_prep_chart,
)
# ── OT Hebrew morphology & lexical analysis ───────────────────────────────────
from .ot.ot_noun_profile import (
    ot_noun_data, ot_adj_data,
    ot_noun_gender_profile, ot_noun_number_profile, ot_noun_state_profile,
    ot_noun_gender_state, ot_noun_top_lemmas, ot_noun_lemma_state,
    ot_noun_book_distribution, ot_noun_genre_profile,
    ot_article_usage, ot_construct_top_lemmas,
    print_ot_noun_overview, print_ot_noun_gender, print_ot_noun_state,
    print_ot_noun_top_lemmas, print_ot_construct_top_lemmas,
    print_ot_noun_genre_profile, print_ot_noun_book_distribution, print_ot_article_usage,
    ot_noun_state_chart, ot_noun_gender_chart, ot_noun_genre_heatmap, ot_noun_book_chart,
    OT_BOOK_GROUPS as OT_NOUN_BOOK_GROUPS, OT_BOOK_ORDER as OT_NOUN_BOOK_ORDER,
    STATE_ORDER as OT_NOUN_STATE_ORDER, GENDER_ORDER as OT_NOUN_GENDER_ORDER,
)
# ── NT Greek morphology & syntax ─────────────────────────────────────────────
from .nt.nt_participles import (
    nt_participle_data, nt_participle_tense_profile, nt_participle_voice_profile,
    nt_participle_tense_voice, nt_participle_role_profile,
    nt_participle_top_lemmas, nt_participle_book_distribution, nt_participle_genre_profile,
    nt_genitive_absolutes, nt_perfect_participles,
    print_nt_participle_overview, print_nt_participle_tense, print_nt_participle_voice,
    print_nt_participle_tense_voice, print_nt_participle_role,
    print_nt_participle_top_lemmas, print_nt_participle_genre_profile,
    print_nt_genitive_absolutes, print_nt_perfect_participles,
    print_nt_participle_book_distribution,
    nt_participle_tense_chart, nt_participle_genre_heatmap, nt_participle_book_chart,
)
from .nt.nt_discourse import (
    nt_particle_frequency, nt_particle_by_book, nt_particle_genre_profile,
    nt_hina_profile, nt_hoti_profile,
    print_nt_particle_overview, print_nt_particle_frequency,
    print_nt_particle_genre_profile, print_nt_hina_profile, print_nt_hoti_profile,
    nt_particle_frequency_chart, nt_particle_genre_heatmap, nt_particle_book_chart,
    PARTICLE_REGISTRY,
)
from .nt.nt_noun_profile import (
    nt_noun_data, nt_noun_case_profile, nt_noun_gender_profile, nt_noun_number_profile,
    nt_noun_case_gender, nt_noun_top_lemmas, nt_noun_lemma_case,
    nt_noun_book_distribution, nt_noun_genre_profile, nt_article_stats,
    print_nt_noun_overview, print_nt_noun_case, print_nt_noun_gender,
    print_nt_noun_case_gender, print_nt_noun_top_lemmas,
    print_nt_noun_genre_profile, print_nt_noun_book_distribution, print_nt_article_stats,
    nt_noun_case_chart, nt_noun_gender_chart, nt_noun_genre_heatmap,
    nt_noun_case_gender_heatmap, nt_noun_book_chart,
    CASE_ORDER, GENDER_ORDER,
)
from .nt.nt_verb_profile import (
    nt_verb_data, nt_verb_tense_profile, nt_verb_voice_profile, nt_verb_mood_profile,
    nt_verb_tense_voice, nt_verb_tense_mood,
    nt_verb_top_lemmas, nt_verb_lemma_tense,
    nt_verb_book_distribution, nt_verb_genre_profile,
    print_nt_verb_overview, print_nt_verb_tense, print_nt_verb_voice, print_nt_verb_mood,
    print_nt_verb_tense_voice, print_nt_verb_top_lemmas,
    print_nt_verb_genre_profile, print_nt_verb_book_distribution,
    nt_verb_tense_chart, nt_verb_voice_chart, nt_verb_mood_chart,
    nt_verb_genre_heatmap, nt_verb_book_chart, nt_verb_tense_voice_heatmap,
    TENSE_ORDER, VOICE_ORDER, MOOD_ORDER,
)
from .nt.nt_moods import (
    nt_mood_data, nt_mood_profile,
    nt_subjunctive_profile, nt_infinitive_profile, nt_imperative_profile,
    nt_subjunctive_constructions, nt_infinitive_constructions,
    nt_imperative_tense_comparison, nt_mood_genre_profile, nt_mood_book_distribution,
    print_nt_mood_overview, print_nt_subjunctive_profile,
    print_nt_infinitive_profile, print_nt_imperative_profile,
    print_nt_subjunctive_constructions, print_nt_infinitive_constructions,
    print_nt_imperative_tense_comparison, print_nt_mood_genre_profile,
    nt_mood_chart, nt_subjunctive_chart, nt_imperative_chart, nt_mood_genre_heatmap,
    PURPOSE_PARTICLES, COND_PARTICLES, PROHIB_STRONGS,
)
from .ot.ot_numbers import (
    ot_number_data, ot_number_frequency, ot_top_number_lemmas,
    ot_number_gender_profile, ot_number_state_profile,
    ot_number_book_distribution, ot_number_genre_profile, ot_number_polarity_table,
    print_ot_number_overview, print_ot_number_frequency,
    print_ot_number_gender, print_ot_number_state,
    print_ot_number_book_distribution, print_ot_number_genre_profile,
    print_ot_number_polarity,
    ot_number_frequency_chart, ot_number_genre_chart, ot_number_book_chart,
    CARDINALS_1_10,
)
from .nt.nt_louw_nida import (
    nt_ln_data, nt_ln_subdomain_frequency, nt_ln_top_lemmas,
    nt_ln_book_distribution, nt_ln_genre_profile,
    nt_ln_domain_breakdown, nt_ln_comparison,
    print_nt_ln_overview, print_nt_ln_subdomain_frequency,
    print_nt_ln_top_lemmas, print_nt_ln_book_distribution,
    print_nt_ln_domain_breakdown, print_nt_ln_comparison,
    nt_ln_subdomain_chart, nt_ln_book_chart, nt_ln_genre_heatmap,
    LN_DOMAIN_NAMES,
)
from .nt.nt_coreference import (
    nt_referent_data, nt_referent_frequency, nt_entity_chain,
    nt_pronoun_referents, nt_book_entity_density, nt_entity_chapter_distribution,
    print_nt_referent_overview, print_nt_referent_frequency,
    print_nt_entity_chain, print_nt_pronoun_referents, print_nt_book_entity_density,
    nt_referent_book_chart, nt_entity_density_chart,
    KNOWN_ENTITIES,
)
from .ot.ot_predicate_args import (
    ot_frame_data, ot_agent_verbs, ot_patient_verbs,
    ot_verb_agents, ot_verb_patients, ot_frame_pairs,
    print_ot_frame_overview, print_ot_agent_verbs, print_ot_patient_verbs,
    print_ot_verb_agents, print_ot_verb_patients, print_ot_frame_pairs,
    ot_agent_verbs_chart, ot_patient_verbs_chart,
)
from .ot.ot_semantic_domains import (
    ot_domain_data, ot_domain_frequency, ot_top_domain_lemmas,
    ot_domain_book_distribution, ot_domain_genre_profile,
    ot_domain_comparison, ot_coredomain_profile, ot_theology_profile,
    print_ot_domain_overview, print_ot_domain_frequency,
    print_ot_top_lemmas, print_ot_domain_book_distribution,
    print_ot_domain_genre_profile, print_ot_domain_comparison,
    print_ot_theology_profile,
    ot_domain_frequency_chart, ot_domain_book_chart,
    ot_domain_genre_chart, ot_domain_heatmap,
    COREDOMAIN_NAMES, LEXDOMAIN_TOP, THEOLOGY_COREDOMAINS,
)
# ── Stylistics, discourse & speech acts ──────────────────────────────────────
from .discourse.speech_acts import (
    SPEECH_ACT_TYPES,
    ot_speech_act_data, ot_speech_act_profile,
    nt_speech_act_data, nt_speech_act_profile,
    ot_speech_act_comparison, nt_speech_act_comparison,
    print_ot_speech_act_profile, print_nt_speech_act_profile,
    print_speech_act_comparison,
    speech_act_chart, speech_act_heatmap,
)
from .discourse.information_structure import (
    ot_information_profile, nt_information_profile,
    ot_clause_linking_comparison, nt_clause_linking_comparison,
    print_ot_information_profile, print_nt_information_profile,
    print_ot_clause_linking_comparison, print_nt_clause_linking_comparison,
    nt_clause_linking_chart, nt_information_heatmap, ot_clause_linking_chart,
)
from .ot.ot_participant import (
    KNOWN_OT_PARTICIPANTS,
    ot_participant_data, ot_participant_subject_verbs, ot_participant_object_verbs,
    ot_participant_chain, ot_entity_density, ot_participant_compare,
    print_ot_participant_profile, print_ot_participant_chain, print_ot_participant_compare,
    ot_participant_chain_chart, ot_entity_density_chart,
)
from .discourse.stylometrics import (
    msttr, book_style_profile, style_comparison,
    print_style_profile, print_style_comparison,
    style_radar_chart, style_heatmap,
)
from .discourse.formulaic import (
    HEBREW_FORMULAS, GREEK_FORMULAS,
    ot_formula_frequency, nt_formula_frequency,
    ot_formula_search, nt_formula_search,
    formula_book_distribution,
    ot_formula_profile, nt_formula_profile,
    print_formula_concordance, print_formula_book_distribution,
    print_ot_formula_profile, print_nt_formula_profile,
    print_ot_top_ngrams, print_nt_top_ngrams,
    formula_book_chart, formula_chapter_chart,
)
from .ot.ot_discourse import (
    ot_discourse_wayyiqtol_density, ot_discourse_speech_density,
    ot_discourse_lexical_diversity, ot_discourse_peak_score,
    ot_discourse_episode_boundaries, ot_discourse_narrative_profile,
    print_ot_discourse_overview, print_ot_wayyiqtol_density,
    print_ot_speech_density, print_ot_peak_score, print_ot_episode_boundaries,
    ot_discourse_density_chart, ot_discourse_peak_chart,
    SCENE_SETTING_LEMMAS,
)
from .nt.nt_demonstratives import (
    nt_demo_data, nt_demo_frequency, nt_demo_case_profile,
    nt_demo_gender_profile, nt_demo_use_profile,
    nt_demo_book_distribution, nt_demo_genre_profile,
    nt_demo_near_far_comparison, nt_demo_top_cooccurrences,
    print_nt_demo_overview, print_nt_demo_frequency,
    print_nt_demo_case, print_nt_demo_gender, print_nt_demo_use,
    print_nt_demo_book_distribution, print_nt_demo_genre_profile,
    print_nt_demo_near_far,
    nt_demo_frequency_chart, nt_demo_case_chart,
    nt_demo_genre_heatmap, nt_demo_book_chart,
    OUTOS, EKEINOS,
)
# ── Utilities & low-level helpers ────────────────────────────────────────────
from .discourse.speaker import (is_jesus_speaking, jesus_speaking_verse_set,
                      filter_to_jesus_speech, ALLOWLIST_VERSES)
from .lexical.lexicon import lookup, search_gloss, lex_entry, lemma_index
from .reporting.export import (export_csv, export_html_page,
                     export_word_study, export_semantic_profile,
                     export_genre_compare, export_divine_names, export_all)
from .reporting import charts
