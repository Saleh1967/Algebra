"""اختزالُ الإغلاق: صيغةٌ شفّافة، وتطابقٌ تامّ، وترقيةٌ محدودةٌ بحدّها.

يُثبِت هذا الاختبارُ ثمانيةَ أشياء: أنّ `s` يُحسَب بنصّ تعريف ٥م ويُرَدُّ مدخلٌ
خارج شرطه، وأنّ القوالبَ الستّةَ تخرج بـ`s` من صفرٍ إلى ثلاثة، وأنّ ثلاثةً
تُغلِق وثلاثةً تسقط، وأنّ قسمةَ القيد **تطابق** قسمةَ أحكام ٥هـ تطابقًا تامًّا،
وأنّ نصيبَ المقاطع الساقطةِ مُشتَقٌّ من الأعداد لا مكتوب، وأنّ حكمَ إغلاقٍ لا
يطابق `s ≤ 1` يُرَدُّ عند الإنشاء، وأنّ المقيسَ صار ثلاثةً من أربعةٍ وأنّ
الترقيةَ تحمل حدَّها، وأنّ للاختزال شروطَ إبطالٍ مكتوبةً.
"""

from __future__ import annotations

import pytest

from alghanem.arabic.closure_window_reduction import (
    CLOSURE_THRESHOLD,
    TEMPLATES,
    WHAT_WOULD_FALSIFY_THE_REDUCTION,
    ClosureReadout,
    TemplateVerdict,
    UpgradedStanding,
    derive_closure_readouts,
    derive_partition_coincidence,
    derive_upgraded_standing,
    window_saturation,
)
from alghanem.arabic.slgae_deposit import SlgaeDepositError


def test_the_saturation_follows_the_published_definition() -> None:
    """`s = (k−1) + الطول`، و`k` إغلاقُ القالب مع بدايةِ ما يليه."""

    assert window_saturation(coda=0, long_nucleus=0) == 0
    assert window_saturation(coda=0, long_nucleus=1) == 1
    assert window_saturation(coda=1, long_nucleus=0) == 1
    assert window_saturation(coda=2, long_nucleus=1) == 3
    assert window_saturation(coda=1, long_nucleus=0, following_onset=2) == 2


def test_an_input_outside_its_condition_is_refused() -> None:
    """إغلاقٌ سالبٌ أو طولٌ غيرُ ثنائيٍّ أو نافذةٌ بلا بدايةٍ بعدها تُرَدّ."""

    with pytest.raises(SlgaeDepositError, match="الإغلاقُ غيرُ سالب"):
        window_saturation(coda=-1, long_nucleus=0)
    with pytest.raises(SlgaeDepositError, match="الإغلاقُ غيرُ سالب"):
        window_saturation(coda=1, long_nucleus=0, following_onset=0)
    with pytest.raises(SlgaeDepositError, match="طولُ النواة"):
        window_saturation(coda=1, long_nucleus=2)


def test_the_six_templates_span_saturation_zero_to_three() -> None:
    """القوالبُ الستّةُ تخرج بـ`s` من صفرٍ إلى ثلاثةٍ بلا فجوة."""

    readouts = derive_closure_readouts()

    assert len(readouts) == len(TEMPLATES) == 6
    assert sorted(item.saturation for item in readouts) == [0, 1, 1, 2, 2, 3]
    assert {item.name for item in readouts if item.saturation == 0} == {"CV"}


def test_three_close_and_three_fall() -> None:
    """ثلاثةٌ تُغلِق وثلاثةٌ تسقط، والحدُّ واحدٌ كما في ٥م."""

    coincidence = derive_partition_coincidence()

    assert CLOSURE_THRESHOLD == 1
    assert coincidence.closing == ("CV", "CVV", "CVC")
    assert coincidence.failing == ("CVVC", "CVCC", "CVVCC")


def test_the_two_partitions_coincide_exactly() -> None:
    """قسمةُ القيد تطابق قسمةَ أحكام ٥هـ، وهما قسمان مستقلّان في الوثيقة."""

    coincidence = derive_partition_coincidence()

    assert coincidence.coincides
    assert set(coincidence.failing) == set(coincidence.edge_recycled)
    assert set(coincidence.closing) == set(coincidence.not_edge_recycled)
    verdicts = {
        row.name: row.verdict for row in TEMPLATES if row.name in coincidence.closing
    }
    assert TemplateVerdict.RECYCLED_AT_EDGE not in verdicts.values()


def test_the_failing_share_is_derived_from_the_counts() -> None:
    """نصيبُ الساقطةِ قسمةُ عدّادين، لا رقمٌ مكتوبٌ بجانبهما."""

    coincidence = derive_partition_coincidence()

    assert coincidence.failing_syllables == 8_036 + 755 + 5
    assert coincidence.total_syllables == sum(row.syllables for row in TEMPLATES)
    assert coincidence.failing_share == pytest.approx(0.0419, abs=0.0001)


def test_a_closure_verdict_that_contradicts_the_threshold_is_refused() -> None:
    """حكمٌ يُكتَب ولا يُشتَقّ من `s ≤ 1` دعوى لا حساب، فيُرَدّ."""

    with pytest.raises(SlgaeDepositError, match="لا يطابق"):
        ClosureReadout(
            name="قالب",
            saturation=3,
            closes=True,
            verdict=TemplateVerdict.BORN,
            syllables=1,
        )


def test_the_upgrade_is_three_of_four_and_carries_its_cap() -> None:
    """المقيسُ 2 ← 3 من 4، والمُرقَّى هو Closure، والحدُّ مكتوبٌ معه."""

    standing = derive_upgraded_standing()

    assert (standing.measurable_before, standing.measurable_after) == (2, 3)
    assert standing.total == 4
    assert "Closure" in standing.upgraded_condition
    assert "الإمكان لا" in standing.capped_by
    assert len(WHAT_WOULD_FALSIFY_THE_REDUCTION) == 4

    with pytest.raises(SlgaeDepositError, match="بلا حدٍّ مكتوب"):
        UpgradedStanding(
            measurable_before=2,
            measurable_after=3,
            total=4,
            upgraded_condition="Closure(C, H)",
            capped_by="   ",
        )
