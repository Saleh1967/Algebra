"""تسجيلُ المثلّث: ثلاثُ فرضيّاتٍ بمُبطِلاتها، ومقياسٌ مُعلَن، ولا اختبارَ هنا.

يُثبِت هذا الاختبارُ سبعةَ أشياء: أنّ العُقَدَ ثلاثٌ وأنّ الوحدةَ **لا تُختبَر
فيها فرضيّة** بالبناء، وأنّ الفرضيّاتَ الثلاثَ معرّفاتُها متمايزة، وأنّ كلَّ
فرضيّةٍ تحمل مُبطِلًا يفارق مؤكِّدَها، وأنّ فرضيّةً بلا مُبطِلٍ تُرَدّ، وأنّ
المقياسَ مُعلَنٌ بعناصره الأربعة وعددِ تكراراته، وأنّ مقياسًا ناقصَ عنصرٍ
يُرَدّ، وأنّ معرّفًا غيرَ مُسجَّلٍ يُرَدُّ لا يُحمَل على أقربه.
"""

from __future__ import annotations

import pytest

from alghanem.arabic.triangle_licensing_preregistration import (
    DECLARED_MEASURE,
    REGISTERED_AT,
    TRIANGLE_HYPOTHESES,
    TRIANGLE_NAMED_RESIDUALS,
    TRIANGLE_NODES,
    DeclaredMeasure,
    GraphShape,
    TriangleHypothesis,
    TrianglePreregistrationError,
    hypothesis_named,
    is_testable_in_this_module,
)


def test_the_module_registers_and_does_not_test() -> None:
    """ثلاثُ عُقَدٍ، ولا اختبارَ في الوحدة بالبناء لا بالنصيحة."""

    assert TRIANGLE_NODES == ("B₁₂", "B₂₃", "B₁₃")
    assert not is_testable_in_this_module()
    assert REGISTERED_AT == "2026-09-22"
    assert len(GraphShape) == 2


def test_the_three_hypotheses_have_distinct_identifiers() -> None:
    """ثلاثُ فرضيّاتٍ بمعرّفاتٍ متمايزة، ومعرّفٌ غيرُ مُسجَّلٍ يُرَدّ."""

    assert len(TRIANGLE_HYPOTHESES) == 3
    identifiers = [item.identifier for item in TRIANGLE_HYPOTHESES]
    assert identifiers == ["TRI-1", "TRI-2", "TRI-3"]
    assert hypothesis_named("TRI-2").identifier == "TRI-2"

    with pytest.raises(TrianglePreregistrationError, match="لا فرضيّةَ مُسجَّلة"):
        hypothesis_named("TRI-9")


def test_every_hypothesis_separates_confirmation_from_falsification() -> None:
    """لكلّ فرضيّةٍ مُبطِلٌ غيرُ فارغٍ يفارق مؤكِّدَها."""

    for hypothesis in TRIANGLE_HYPOTHESES:
        assert hypothesis.what_would_falsify.strip()
        assert (
            hypothesis.what_would_confirm.strip()
            != hypothesis.what_would_falsify.strip()
        )


def test_a_hypothesis_without_a_falsifier_is_refused() -> None:
    """فرضيّةٌ تُثبَّت مهما جاءت البياناتُ سؤالٌ لا اختبار، فتُرَدّ."""

    with pytest.raises(TrianglePreregistrationError, match="بلا شرطِ إبطال"):
        TriangleHypothesis(
            identifier="X",
            claim="دعوى",
            what_would_confirm="تأكيد",
            what_would_falsify="   ",
        )
    with pytest.raises(TrianglePreregistrationError, match="لا يفصلان"):
        TriangleHypothesis(
            identifier="X",
            claim="دعوى",
            what_would_confirm="النصُّ نفسُه",
            what_would_falsify="النصُّ نفسُه",
        )


def test_the_measure_is_declared_with_all_its_parts() -> None:
    """المقياسُ أربعةُ عناصرَ وعددُ تكرارات، وكلُّها مُعلَنةٌ قبل النظر."""

    measure = DECLARED_MEASURE

    assert measure.replicates == 2_000
    assert "تبادلٍ داخل طبقة C₂" in measure.null_model
    assert "بونفيروني" in measure.multiplicity_correction
    assert "سياستَي الإدراج" in measure.acceptance_threshold
    assert "التماثل" in measure.statistic


def test_a_measure_missing_a_part_is_refused() -> None:
    """مقياسٌ ناقصٌ يُكمَّل بعد رؤية الرقم، فيُرَدُّ عند الإنشاء."""

    with pytest.raises(TrianglePreregistrationError, match="تصحيحُ التعدّد"):
        DeclaredMeasure(
            null_model="صفري",
            statistic="إحصاءة",
            acceptance_threshold="حدّ",
            multiplicity_correction="  ",
            replicates=10,
        )
    with pytest.raises(TrianglePreregistrationError, match="عددُ التكرارات موجب"):
        DeclaredMeasure(
            null_model="صفري",
            statistic="إحصاءة",
            acceptance_threshold="حدّ",
            multiplicity_correction="بونفيروني",
            replicates=0,
        )


def test_the_motivation_does_not_confirm_the_triangle() -> None:
    """سقوطُ الإغلاق ينفي كفايةَ السلسلة ولا يُثبِت المثلّث."""

    assert len(TRIANGLE_NAMED_RESIDUALS) == 6
    joined = " ".join(TRIANGLE_NAMED_RESIDUALS)
    assert "لا يقول إنّ المثلّثَ هو البديل" in joined
    assert "اختبارٌ لم يُجرَ" in joined
