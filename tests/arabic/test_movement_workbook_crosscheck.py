"""مصنَّفُ الحركة: عددان يُعادان، وعددٌ يُخفي سياسةً، وفحوصٌ لا تسقط.

يُثبِت هذا الاختبارُ تسعةَ أشياء: أنّ 4,562 يُعاد اشتقاقُه من البايتات المُودَعة
بالضبط، وأنّه **يفكَّك** إلى ثلاثيٍّ 4,087 ومضاعفٍ 419 ومعتلٍّ 56 فيزيد على
عدّ الشجرة المُجمَّد 475 جذرًا، وأنّ تفكيكًا لا يجمع إلى كلّه يُرفَض عند
الإنشاء، وأنّ الحواملَ 32 خامًا و**29** بعد الطيّ المُودَع فالفضاءُ 116 لا 128،
وأنّ المقاعدَ المطويّةَ هي «أ ئ ى» بأعيانها، وأنّ أربعةً من خمسةِ فحوصٍ حسابيّةٍ
تمرّ و**الخامسَ يسقط** (مقامُ المقاطع يتجاوز فضاءَ الرموز)، وأنّ الفجوةَ 372
و380، وأنّ **اثنين فقط** من سبعةِ فحوصٍ في البطّاريّة الأولى كان يمكن أن يسقطا،
وأنّ ما لا يُفحَص هنا يُقيَّد «لا يُفحَص» لا «صحيح».
"""

from __future__ import annotations

import pytest

from alghanem.arabic.movement_workbook_crosscheck import (
    REPORTED_BATTERY_ONE_CHECKS,
    REPORTED_FIGURES,
    WORKBOOK_CROSSCHECK_NAMED_RESIDUALS,
    CheckKind,
    ClaimVerdict,
    PopulationDecomposition,
    WorkbookCrosscheckError,
    carrier_census,
    check_reported_arithmetic,
    derive_denominator_gap,
    falsifiable_check_share,
    population_decomposition,
    read_claim_verdicts,
)


def test_the_row_count_is_reproduced_from_deposited_bytes() -> None:
    """4,562 يُعاد اشتقاقُه بالضبط؛ فالخلافُ ليس في القراءة."""

    decomposition = population_decomposition()
    assert decomposition.total_distinct_length_three == REPORTED_FIGURES.root_slot_rows
    assert decomposition.total_distinct_length_three == 4562


def test_the_row_count_merges_three_root_types() -> None:
    """يضمّ ثلاثيًّا ومضاعفًا ومعتلًّا، فيزيد 475 على عدّ الشجرة المُجمَّد."""

    decomposition = population_decomposition()
    assert decomposition.sound_trilateral == 4087
    assert decomposition.doubled == 419
    assert decomposition.weak_trilateral == 56
    assert decomposition.tree_frozen_trilateral == 4087
    assert decomposition.merged_beyond_the_frozen_rule == 475
    assert decomposition.verdict is ClaimVerdict.CONFLICTS_WITH_THE_TREE


def test_a_decomposition_that_does_not_sum_is_refused() -> None:
    """تفكيكٌ لا يجمع إلى كلّه يُرَدُّ عند الإنشاء ولا يُقرَّب."""

    with pytest.raises(WorkbookCrosscheckError):
        PopulationDecomposition(
            total_distinct_length_three=4562,
            sound_trilateral=4087,
            doubled=419,
            weak_trilateral=0,
            tree_frozen_trilateral=4087,
        )


def test_the_carriers_are_seats_not_letters() -> None:
    """32 خامًا و29 بعد الطيّ؛ والمطويُّ «أ ئ ى» بأعيانه."""

    census = carrier_census()
    assert census.raw_carriers == 32
    assert census.folded_carriers == 29
    assert census.seats_folded_away == ("أ", "ئ", "ى")
    assert census.raw_states == 128
    assert census.folded_states == 116


def test_the_state_space_must_be_carriers_times_four() -> None:
    """الحالاتُ حاصلُ ضربِ الحواملِ في أربع؛ وإلّا فالعددان من فضاءين."""

    assert REPORTED_FIGURES.carriers * 4 == REPORTED_FIGURES.states


def test_four_arithmetic_checks_pass_and_one_fails() -> None:
    """الحسابُ المذكورُ متّسقٌ إلّا في المقام: 77,783 فوق 77,411."""

    checks = check_reported_arithmetic()
    assert len(checks) == 5
    assert sum(1 for value in checks.values() if value) == 4
    assert checks["مقامُ المقاطع ≤ فضاء الرموز"] is False
    assert checks["F+D+K+S = الصريح"] is True


def test_the_denominator_gap_is_measured() -> None:
    """الفجوةُ 372 عن الرموز و380 عن المحاذى معجميًّا."""

    assert derive_denominator_gap() == (372, 380)


def test_only_two_of_seven_checks_could_have_failed() -> None:
    """خمسةٌ من سبعةٍ تعريفٌ لا يسقط، فخضرتُها ليست خبرًا."""

    falsifiable, total = falsifiable_check_share()
    assert (falsifiable, total) == (2, 7)
    kinds = {kind for _name, kind in REPORTED_BATTERY_ONE_CHECKS}
    assert kinds == {CheckKind.FALSIFIABLE, CheckKind.DEFINITIONAL}


def test_what_cannot_be_checked_is_recorded_as_such() -> None:
    """ما لا يُفحَص يُقيَّد «لا يُفحَص»، لا «صحيح» ولا «مردود»."""

    verdicts = read_claim_verdicts()
    assert verdicts["مجاميعُ Function_Evidence"] is ClaimVerdict.NOT_VERIFIABLE_HERE
    assert verdicts["البطّاريّةُ الرابعة"] is ClaimVerdict.NOT_VERIFIABLE_HERE
    assert (
        sum(
            1
            for value in verdicts.values()
            if value is ClaimVerdict.NOT_VERIFIABLE_HERE
        )
        == 3
    )
    assert len(WORKBOOK_CROSSCHECK_NAMED_RESIDUALS) == 6
    assert len(set(WORKBOOK_CROSSCHECK_NAMED_RESIDUALS)) == 6
