"""أرقامُ ستيرلنغ وصيغتُه — مبرهناتٌ تُفحَص بأنفسها لا بجدولٍ مُودَع.

**ما يُفحَص ههنا**: أنّ التعدادين **يُغلِقان على مطابقاتٍ معروفة** بلا أن
يُستورَد رقمٌ من خارج: مجموعُ الأولى `n!`، ومجموعُ الثانية `B(n)`،
وضربُهما **المطابقة**؛ وأنّ حدّي روبنز **يكتنفان `log₂ n!` من الطرفين**.

`THE_TABLE_IS_NOT_DEPOSITED_IT_IS_DERIVED`: ولا جدولَ أرقامٍ في الشجرة —
كلُّ عددٍ يُبنى بقاعدة النمط من أصغرَ منه. **فما يُفحَص هو الاتّساق، لا
مطابقةُ نسخة.**
"""

from __future__ import annotations

import math

import pytest

from algebra.stirling import (
    StirlingError,
    bell,
    cycles,
    factorial_bounds,
    gap_in_bits,
    inversion_closes,
    subsets,
    unsearched,
)

WITNESSABLE = 16
"""كم خطوةً من خطوات العائم يلزم عرضُ الكُنف ليُشهَد عليه.

**وليست مبرهنةً بل حدُّ آلة**: `lgamma` نفسُها تحمل خطأً بضعَ خطوات،
فلا يصحّ الحكمُ بالحصر الصارم حين يقارب العرضُ ذلك الخطأ. **والحدُّ
مُعلَنٌ ههنا كي يُرى، لا مخبوءٌ في مقارنة.**
"""


def test_the_first_kind_sums_to_the_factorial() -> None:
    """`Σ_k c(n,k) = n!` — كلُّ تبديلةٍ لها عددُ دوراتٍ واحدٌ لا غير."""

    for whole in range(12):
        assert sum(cycles(whole, one) for one in range(whole + 1)) == math.factorial(
            whole
        )
    assert cycles(4, 2) == 11
    assert cycles(5, 1) == 24  # الدوراتُ الوحيدةُ على خمسةٍ: (n−1)!


def test_the_second_kind_sums_to_the_bell_number() -> None:
    """`Σ_k S(n,k) = B(n)` — وكلُّ قسمةٍ لها عددُ كتلٍ واحدٌ لا غير."""

    assert [bell(one) for one in range(8)] == [1, 1, 2, 5, 15, 52, 203, 877]
    assert subsets(4, 2) == 7 and subsets(4, 3) == 6 and subsets(4, 4) == 1
    for whole in range(10):
        assert bell(whole) == sum(subsets(whole, one) for one in range(whole + 1))


def test_the_two_kinds_are_inverse_matrices() -> None:
    """ضربُ المصفوفتين يعطي المطابقة — اختبارُ تصحيحٍ ذاتيٍّ بلا جدول."""

    for whole in range(14):
        assert inversion_closes(whole), whole


def test_robbins_brackets_the_factorial_while_the_machine_can_see_it() -> None:
    """حدّان مبرهَنان يكتنفان `log₂ n!` — **ما دامت الآلةُ تُفرّق بينهما**.

    **وحدُّ الفحص آلةٌ لا مبرهنة**: عرضُ الكُنف `log₂e / (12n(12n+1))`
    ينكمش كمربّع `n`، وخطوةُ العائم عند تلك القيمة تكبر بها. فيأتي `n`
    **يصير فيه الحدّان عددًا واحدًا في الآلة** — والمبرهنةُ قائمةٌ
    والفحصُ يعمى. **فيُسمّى موضعُ العمى ولا يُحذَف من الجدول.**
    """

    blind: list[int] = []
    for whole in (1, 2, 5, 20, 100, 1_000, 10_000, 100_000):
        low, high = factorial_bounds(whole)
        exact = math.lgamma(whole + 1) / math.log(2)
        if high - low <= WITNESSABLE * math.ulp(exact):
            blind.append(whole)
            assert low <= exact <= high, whole  # يبقى محصورًا وإن تساويا
            continue
        assert low < exact < high, whole
        assert high - low < 1 / whole
    assert blind == [10_000, 100_000]
    low, high = factorial_bounds(1_000)
    seen = math.lgamma(1_001) / math.log(2)
    assert (high - low) / math.ulp(seen) > 5_000  # ألفٌ يُرى بوضوح
    low, high = factorial_bounds(10_000)
    tight = math.lgamma(10_001) / math.log(2)
    assert 6 < (high - low) / math.ulp(tight) < 8  # سبعُ خطواتٍ لا غير
    with pytest.raises(StirlingError):
        factorial_bounds(0)


def test_the_gap_is_never_negative_and_grows_with_the_alphabet() -> None:
    """فجوةُ ستيرلنغ غيرُ سالبة، وتكبر بعدد الأصناف على المقام نفسِه."""

    assert gap_in_bits((10,)) == 0.0  # كتلةٌ نقيّةٌ: الكمُّ وحدُّه صفران
    assert math.copysign(1.0, gap_in_bits((10,))) > 0  # ولا سالبَ صفرٍ يُطبَع
    narrow = gap_in_bits((50, 50))
    wide = gap_in_bits((25, 25, 25, 25))
    assert 0 < narrow < wide
    for counts in ((34, 166), (2, 121), (4, 38), (65, 232)):
        assert gap_in_bits(counts) > 0
    with pytest.raises(StirlingError):
        gap_in_bits(())


def test_the_space_a_greedy_ladder_does_not_search_is_counted() -> None:
    """`S(n,k)` يُسعِّر دعوى «الجشعُ غيرُ مبرهَن» عددًا لا قولًا."""

    space = unsearched(4)
    assert space == {2: 7, 3: 6, 4: 1}
    assert sum(space.values()) == bell(4) - 1
    visited = 4 - 1  # الجشعُ يزور قسمةً واحدةً عند كلّ درجة
    assert visited < sum(space.values())
    assert unsearched(8)[2] == 127
    assert sum(unsearched(8).values()) == bell(8) - 1 == 4_139


def test_nothing_is_imported_and_the_recurrences_are_the_only_source() -> None:
    """لا جدولَ مُودَعٌ: الأعدادُ تُبنى بقاعدة النمط من أصغرَ منها."""

    from pathlib import Path

    source = (
        Path(__file__).resolve().parents[2] / "src" / "algebra" / "stirling.py"
    ).read_text(encoding="utf-8")
    assert "c(n−1, k−1) + (n−1)·c(n−1, k)" in source.replace(
        "c(n−1,k−1) + (n−1)·c(n−1,k)", "c(n−1, k−1) + (n−1)·c(n−1, k)"
    )
    assert "k·S(n−1,k) + S(n−1,k−1)" in source
    assert "import" in source and "from functools import cache" in source
    for astray in ("11", "52", "203", "877"):
        assert f"= {astray}" not in source  # ولا رقمٌ معروفٌ مكتوبٌ نتيجةً


def test_negative_arguments_are_refused_not_silently_zeroed() -> None:
    """المدخلُ خارجَ الحدّ يُردّ — ولا يُصفَّر صامتًا."""

    for call in (cycles, subsets):
        with pytest.raises(StirlingError):
            call(-1, 0)
        with pytest.raises(StirlingError):
            call(3, -2)
        assert call(3, 9) == 0  # وما فوق الحدّ خلوٌّ مشروعٌ لا خطأ
