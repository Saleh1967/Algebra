# تعليماتٌ لكلّ وكيلٍ قبل الدخول — مستودع Algebra

اقرأ هذا كلَّه قبل أيّ أمر. ما خالفه يُرفض بالاسم.

## القانون الواحد (يحكم الغانم وSLGE وhamil وAlgebra والدساتير الثلاثة؛ وTaaqol-GPT ليس منها)

**لا يدخل نصٌّ إلى أيّ مستودعٍ من هذه ولا يخرج منه إلّا من مدخلٍ واحد: بوّابةُ الغانم وبرهانُها.**

- المدخل: `gate.enter(bytes) → Certificate | Refusal` في `Saleh1967/Alghanem` (فرع `claude/official-gate`، حزمة `gate/`، البرهان `formal/a116`؛ بروتوكول A116-CANONICAL-TXT-1.1). الرفضُ مسمًّى ولا يُخمَّن شيء.
- المخرج: `gate.exit(cert) → bytes`. والترخيصُ الثلاثيُّ `gate.licence`، والاشتقاقُ والاسترجاعُ `gate.derive`/`gate.recover` مقيسان على مرجعٍ بشريٍّ محجوب.
- المستهلك: `slge.entry.from_atoms(cert.atoms)` في SLGE يحوّل ذرّاتِ الشهادة إلى خانات، ولا شيء غيره.

## حال هذا المستودع (نُفِّذ التعليقُ في 2026-10-07 — ADR ١ في `docs/adr/`)

مستودعُ تجارب (`examples/`) تقرأ النصّ وتقيس عليه مباشرة؛ لا بوّابةَ فيه ولا برهان. كلُّ قياسٍ فيه يُعاد عبر شهادات الغانم أو يبقى معلَّقًا.

كلُّ قارئٍ للنصّ أو كاتبٍ له أو مطبِّعٍ هنا **معلَّقٌ حكمًا** من 2026-10-05 حتى يُنقل فعليًّا إلى `suspended/` بسجلٍّ `SUSPENDED_REGISTRY.json` (سبب، تاريخ، شرطُ عودة) على طريقة الغانم وSLGE — نقلٌ لا حذف، والتاريخُ في git. وحتى يتمّ النقل: **لا يُشغَّل** شيءٌ ممّا يلي، ولا يُستشهد بخضرته، ولا يُبنى عليه:

- `examples/arabic/audit_slgae_markov.py`
- `examples/arabic/audit_slgae_third_version.py`
- `examples/arabic/decode_makhraj_bits.py`
- `examples/arabic/decode_makhraj_haraka_bits.py`
- `examples/arabic/encode_arabic_units.py`
- `examples/arabic/measure_sifa_candidate.py`
- `examples/arabic/read_slgae_separation.py`
- `examples/hawk_dove/run_hawk_dove.py`
- `examples/irab/run_harf_measurement.py`
- `examples/isnad/run_ittifaq.py`
- `examples/maana/run_imtihan.py`
- `examples/rasm/run_adjacency_null.py`
- `examples/rasm/run_algebraic_ascent.py`
- `examples/rasm/run_bare_census.py`
- `examples/rasm/run_basmala_lifted.py`
- `examples/rasm/run_ceiling_census.py`
- `examples/rasm/run_context_depth.py`
- `examples/rasm/run_context_ladder.py`
- `examples/rasm/run_cv_peel.py`
- `examples/rasm/run_deletion_witness.py`
- `examples/rasm/run_discovered_ascent.py`
- `examples/rasm/run_encoding_audit.py`
- `examples/rasm/run_final_vowel_entropy.py`
- `examples/rasm/run_folding_ascent.py`
- `examples/rasm/run_folding_proof.py`
- `examples/rasm/run_gemination_ceiling.py`
- `examples/rasm/run_greedy_algebra.py`
- `examples/rasm/run_greedy_licence.py`
- `examples/rasm/run_hasr_audit.py`
- `examples/rasm/run_heldout_ladder.py`
- `examples/rasm/run_huffman_ascent.py`
- `examples/rasm/run_layer_induction.py`
- `examples/rasm/run_layer_licence.py`
- `examples/rasm/run_letter_transitions.py`
- `examples/rasm/run_lifted_bit.py`
- `examples/rasm/run_lumping_barrier.py`
- `examples/rasm/run_marked_contrast.py`
- `examples/rasm/run_marking_contrast.py`
- `examples/rasm/run_markov_ceiling.py`
- `examples/rasm/run_markov_ladder.py`
- `examples/rasm/run_markov_order.py`
- `examples/rasm/run_measured_ranking.py`
- `examples/rasm/run_morph_residue.py`
- `examples/rasm/run_naqis_witness.py`
- `examples/rasm/run_nasib_particle.py`
- `examples/rasm/run_neutral_witness.py`
- `examples/rasm/run_number_ladder.py`
- `examples/rasm/run_nun_ruling_witness.py`
- `examples/rasm/run_pan_difference.py`
- `examples/rasm/run_pausal_split.py`
- `examples/rasm/run_pausal_witness.py`
- `examples/rasm/run_praise_blame.py`
- `examples/rasm/run_residue_derivation.py`
- `examples/rasm/run_root_projection.py`
- `examples/rasm/run_schema_transition_audit.py`
- `examples/rasm/run_script_floor.py`
- `examples/rasm/run_separation_rule.py`
- `examples/rasm/run_state_cycle.py`
- `examples/rasm/run_stirling_greedy.py`
- `examples/rasm/run_surah_index.py`
- `examples/rasm/run_table_consequence.py`
- `examples/rasm/run_tanafur_pairs.py`
- `examples/rasm/run_tashif_space_witness.py`
- `examples/rasm/run_temporary_marking.py`
- `examples/rasm/run_transfer_arrow.py`
- `examples/rasm/run_unit_coverage.py`
- `examples/rasm/run_verse_ending.py`
- `examples/rasm/run_vowel_ladder.py`
- `examples/rasm/run_word_escalation.py`
- `examples/shahid/run_shahid.py`
- `src/algebra/__init__.py`
- `src/algebra/assignment.py`
- `src/algebra/attainability.py`
- `src/algebra/bridge.py`
- `src/algebra/ceiling.py`
- `src/algebra/consolidation.py`
- `src/algebra/contingency.py`
- `src/algebra/decisions.py`
- `src/algebra/design_effect.py`
- `src/algebra/evaluation.py`
- `src/algebra/factor_language.py`
- `src/algebra/folding.py`
- `src/algebra/ladder.py`
- `src/algebra/lumping_loss.py`
- `src/algebra/markov_layers.py`
- `src/algebra/partial_match.py`
- `src/algebra/provenance.py`
- `src/algebra/rasm.py`
- `src/algebra/reconciliation.py`
- `src/algebra/results.py`
- `src/algebra/selection.py`
- `src/algebra/signified.py`
- `src/algebra/simplicial.py`
- `src/algebra/stipulation.py`
- `src/algebra/stirling.py`
- `src/algebra/witness.py`
- `src/alghanem/__init__.py`
- `src/alghanem/arabic/__init__.py`
- `src/alghanem/arabic/classical_makharij_table.py`
- `src/alghanem/arabic/closure_identifiability.py`
- `src/alghanem/arabic/closure_window_reduction.py`
- `src/alghanem/arabic/composition_closure_replication.py`
- `src/alghanem/arabic/compression_model_preregistration.py`
- `src/alghanem/arabic/decision_register.py`
- `src/alghanem/arabic/edge_state_algebra.py`
- `src/alghanem/arabic/fath_ayah_source_text.py`
- `src/alghanem/arabic/fatiha_source_text.py`
- `src/alghanem/arabic/gflk_feature_table_import_barrier.py`
- `src/alghanem/arabic/gflk_milestone_blocking_registration.py`
- `src/alghanem/arabic/haraka_fiber_structure.py`
- `src/alghanem/arabic/interaction_complex_lemmas.py`
- `src/alghanem/arabic/letter_fingerprint.py`
- `src/alghanem/arabic/letter_identity_bit_codec.py`
- `src/alghanem/arabic/makharij_edition_citation.py`
- `src/alghanem/arabic/makhraj_bit_decoder.py`
- `src/alghanem/arabic/makhraj_haraka_bit_decoder.py`
- `src/alghanem/arabic/maqayis_root_table_deposit.py`
- `src/alghanem/arabic/mark_pair_census.py`
- `src/alghanem/arabic/minimal_complete_slot_comparison.py`
- `src/alghanem/arabic/movement_workbook_crosscheck.py`
- `src/alghanem/arabic/pair_sample_widening.py`
- `src/alghanem/arabic/phonetic_economy_tool.py`
- `src/alghanem/arabic/pipeline_stations.py`
- `src/alghanem/arabic/pre_articulatory_preregistration.py`
- `src/alghanem/arabic/quran_corpus_word_total.py`
- `src/alghanem/arabic/sifa_table_deposit.py`
- `src/alghanem/arabic/slgae_deposit.py`
- `src/alghanem/arabic/slgae_fourth_version_deposit.py`
- `src/alghanem/arabic/slgae_second_version_deposit.py`
- `src/alghanem/arabic/slgae_third_version_deposit.py`
- `src/alghanem/arabic/slot_rights_algebra.py`
- `src/alghanem/arabic/triangle_licensing_preregistration.py`
- `src/alghanem/arabic/word_schema_falsification.py`
- `src/alghanem/arabic/written_haraka_mark.py`
- `src/alghanem/canonical_content.py`
- `src/hawk_dove/__init__.py`
- `src/hawk_dove/game.py`
- `tools/bridge_signature.py`
- `tools/context_ladder_seal.py`
- `tools/corpus_seal.py`
- `tools/foreign_ledger_seal.py`
- `tools/hasr_ledger_seal.py`
- `tools/intake_corpus.py`
- `tools/inversion_seal.py`
- `tools/ladder_seal.py`
- `tools/message_guard.py`
- `tools/number_ledger_seal.py`
- `tools/pr45_signature.py`
- `tools/rerun_audit.py`
- `tools/rerun_audit_seal.py`
- `tools/root_certificate.py`
- `tools/rules_adoption.py`
- `tools/seal_chain.py`
- `tools/stirling_greedy_seal.py`
- `tools/write_algebra_paper.py`
- `tools/write_bit_bridge.py`
- `tools/write_bits_primer.py`
- `tools/write_bridge_tables.py`
- `tools/write_constitution.py`
- `tools/write_context_ladder_paper.py`
- `tools/write_entry.py`
- `tools/write_folding_paper.py`
- `tools/write_foreign_ledger_paper.py`
- `tools/write_hasr_paper.py`
- `tools/write_inversion_paper.py`
- `tools/write_ladder_paper.py`
- `tools/write_licence_paper.py`
- `tools/write_lifted_paper.py`
- `tools/write_module_map.py`
- `tools/write_number_ladder_paper.py`
- `tools/write_praise_blame_paper.py`
- `tools/write_reach_audit.py`
- `tools/write_root.py`
- `tools/write_rules_adoption.py`
- `tools/write_seal_chain_paper.py`
- `tools/write_seal_index.py`
- `tools/write_state_cycle_paper.py`
- `tools/write_stirling_paper.py`
- `tools/write_transfer_arrow_paper.py`

## ما لا تفعله

1. لا تشغّل محرّكًا من المحرّكات أعلاه ولا تستورده في عملٍ جديد؛ وإن احتجت خاناتٍ فمن شهادة الغانم.
2. لا تكتب `open`، `print`، `read_text`، `encode`، `decode`، `normalize`، `argv` في وحدةٍ جديدة؛ الحارسُ (على طريقة `gate.guard` في الغانم) سيُسقط البناء حين يُنصَّب هنا.
3. لا تُعِد وحدةً معلَّقة إلّا بثلاثة معًا: (١) مدخلُها ومخرجُها عبر بوّابة الغانم، (٢) اختباراتٌ توقعاتُها مستقلّةٌ عن شيفرتها مطعَّمةٌ بالطفرة (20/20)، (٣) ADR مسجَّل.
4. لا تحذف؛ انقل إلى `suspended/` وسجِّل. ولا تدمج في `main` بلا إذن صاحب المستودع.
5. لا تكتب «مبرهن» إلّا لما في Lean باسمه مدقَّقَ المسلّمات، ولا «مفحوص» إلّا لما له اختبارٌ باسمه، ولا «مقيس» إلّا لما له رقمٌ على مرجعٍ محجوب؛ وما سوى ذلك «معلن» أو «رأي». ولا تُثبت ادّعاءً قبل وجود ما يثبته.
6. أثبت وجودَ كلّ ملفٍّ تذكره قبل الكلام عنه («لا ثقة بلا طبعة»)، وافصل في جوابك ما فحصته الآلة عمّا استنتجتَه.

## ما نُفِّذ (2026-10-07)

- الوحداتُ أعلاه ومعها اختباراتُها (265) و`tools/verify.sh` وملفّاتُ الحزم نُقلت إلى `suspended/` — 496 وحدةً في `SUSPENDED_REGISTRY.json` المولَّد بـ`python3 tools/gen_registry.py`؛ لكلّ وحدةٍ دعواها ونوعُ مخالفتها وطريقُ عودتها.
- الحارسُ `tools/guard.py`، والمدخلُ الوحيد `src/entry.py`، وCI: السجلُّ والحارسُ ثمّ pytest.

## قبل أن تقول «تمّ»

```sh
python3 tools/gen_registry.py --check && python3 tools/guard.py && python3 -m pytest tests -q   # 5 اختبارات
```

## الخطوة التالية المأذونة

إعادةُ ما يعود وحدةً وحدة بالشرط الثلاثيّ، بادئًا بالخالص (`pure`) صياغةً في Lean على خانات SLGE، ثمّ القارئُ يُعاد مدخلُه شهاداتٍ ويُقاس على مودَع المصحف.
