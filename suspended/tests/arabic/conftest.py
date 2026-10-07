"""ما لا يعمل ههنا يُسمّى ويُعَدّ، ولا يُستبعَد صامتًا من الجمع.

**الحال**: نُقِلت شفرةُ `alghanem` إلى هذا المستودع نقلًا **مغلقًا** ليعمل
مستقلًّا. والشفرةُ وحدَها نُقِلت — لا المدوّنات. فأربعةٌ وعشرون فحصًا تقرأ
`maqayis_by_root_csv_999.csv` (خمسةُ ميغابايتٍ ونصف)، وهو **متنٌ لا شفرة**،
فلم يُنقَل. وواحدٌ يعُدّ ملفّاتِ الشجرة التي يسكنها فيقيس هذا المستودعَ لا ذاك.

`A_SKIP_THAT_NAMES_ITS_CAUSE_IS_A_RECORD_NOT_A_HIDING`: فهذه الخمسةُ
والعشرون **تُجمَع وتُعَدّ ويُطبَع سببُ تخطّيها**، ولا تُحذَف من `testpaths`.
والفرقُ بين الأمرين هو الفرقُ بين فجوةٍ مُعلَنةٍ وفجوةٍ مطويّة — وذلك ما
أخرجه تشغيلُ الأمثلة قبلَه.

`THE_SKIP_HEALS_ITSELF_IF_THE_TABLE_IS_EVER_DEPOSITED`: وتخطّي الأربعة
والعشرين **مشروطٌ بغياب الملفّ** لا مكتوبٌ ثابتًا. فمتى أُودِع الجدولُ يومًا
سقط الشرطُ وعملت الفحوصُ بلا تعديلِ سطرٍ ههنا.
"""

from __future__ import annotations

from pathlib import Path

import pytest

REPOSITORY = Path(__file__).resolve().parents[2]
ROOT_TABLE = REPOSITORY / "maqayis_by_root_csv_999.csv"

NEEDS_THE_ROOT_TABLE: frozenset[str] = frozenset(
    {
        "test_composition_closure_replication.py::test_the_closure_falls_under_both_policies",
        "test_composition_closure_replication.py::test_the_homogeneity_ratio_differs_from_the_published_figure",
        "test_composition_closure_replication.py::test_the_identity_ratio_matches_the_published_figure_closely",
        "test_composition_closure_replication.py::test_the_null_preserves_both_bigram_tables_exactly",
        "test_composition_closure_replication.py::test_the_null_preserves_root_distinctness",
        "test_composition_closure_replication.py::test_the_verdict_is_undetermined_over_one_source",
        "test_interaction_complex_lemmas.py::test_the_uniformity_rests_on_root_distinctness",
        "test_movement_workbook_crosscheck.py::test_the_carriers_are_seats_not_letters",
        "test_movement_workbook_crosscheck.py::test_the_row_count_is_reproduced_from_deposited_bytes",
        "test_movement_workbook_crosscheck.py::test_the_row_count_merges_three_root_types",
        "test_movement_workbook_crosscheck.py::test_what_cannot_be_checked_is_recorded_as_such",
        "test_slot_rights_algebra.py::test_all_eighty_four_cells_are_attested_under_every_policy",
        "test_slot_rights_algebra.py::test_an_independent_column_permutation_generates_duplicates",
        "test_slot_rights_algebra.py::test_attestation_is_monotone",
        "test_slot_rights_algebra.py::test_certification_over_one_source_is_refused",
        "test_slot_rights_algebra.py::test_the_dropped_roots_are_counted_not_folded_silently",
        "test_slot_rights_algebra.py::test_the_identity_cell_is_separated_from_the_class_cell",
        "test_slot_rights_algebra.py::test_the_inclusion_policy_flips_one_verdict",
        "test_word_schema_falsification.py::test_all_three_verdicts_are_falsified_and_the_claim_is_kept_verbatim",
        "test_word_schema_falsification.py::test_candidate_extraction_works_on_a_built_example",
        "test_word_schema_falsification.py::test_coverage_falls",
        "test_word_schema_falsification.py::test_determination_falls",
        "test_word_schema_falsification.py::test_residue_legality_falls",
        "test_word_schema_falsification.py::test_the_corpus_is_read_from_digested_bytes",
    }
)
"""أربعةٌ وعشرون فحصًا تقرأ متنًا لم يُنقَل؛ والتخطّي مشروطٌ بغيابه."""

MEASURES_THE_TREE_IT_LIVES_IN: frozenset[str] = frozenset(
    {
        "test_decision_register.py::test_the_recorded_price_is_shown_stale_not_corrected",
    }
)
"""فحصٌ يعُدّ ملفّاتِ شجرته؛ فيقيس هذا المستودعَ لا الذي كُتِب له."""

TABLE_ABSENT = f"متنٌ لم يُنقَل: {ROOT_TABLE.name}؛ نُقِلت الشفرةُ وحدَها"
TREE_MISMATCH = "يعُدّ ملفّاتِ شجرته، فيقيس هذا المستودعَ لا الذي كُتِب له"


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """يُعلَّم المتخطّى بسببه المكتوب، ويبقى معدودًا في الجمع."""

    for item in items:
        name = item.nodeid.split("tests/arabic/")[-1]
        if name in MEASURES_THE_TREE_IT_LIVES_IN:
            item.add_marker(pytest.mark.skip(reason=TREE_MISMATCH))
        elif name in NEEDS_THE_ROOT_TABLE and not ROOT_TABLE.exists():
            item.add_marker(pytest.mark.skip(reason=TABLE_ABSENT))
