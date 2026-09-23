"""جدولُ الاقتران: كلُّ رقمٍ يُعاد اشتقاقُه، والمتطابقةُ تكشف ما لا يُعاد.

يُثبِت هذا الاختبارُ عشرةَ أشياء على الجدول الوارد (٢٢٥٬٩١٠ مقطعًا): أنّ
`G = 43,686.2` و`z ≈ 209` **يُعادان بالضبط**، وأنّ الاحتمالين الشرطيّين
`0.409139` و`0.002102` ونسبتَهما `194.7` ونسبةَ الأرجحيّة `0.00304` كذلك،
وأنّ **المتطابقة** `فرقُ البتّات = G/(2N ln2)` تصدق على الحساب الداخليّ،
وأنّ النموذجَ المستقلَّ **أسوأُ** بمعالمَ أقلّ، وأنّ أرقامَ البتّات الثلاثةَ
الواردةَ **لا تُعاد** من هذا الجدول — وذلك متوقَّعٌ لأنّ نصَّها يقول إنّها على
بياناتٍ محجوبة، والفرقُ بينهما دون ٠٫٨٪ — وأنّ التوقّعاتِ تُشتَقُّ من الهوامش،
وأنّ الخليّةَ الصفرَ تُبطِل الأرجحيّةَ ولا تُبطِل `G`، وأنّ هامشًا صفرًا يُرَدّ.
"""

from __future__ import annotations

import math
from fractions import Fraction

import pytest

from algebra.contingency import (
    CONTINGENCY_NAMED_RESIDUALS,
    ContingencyError,
    Table2x2,
)

# (لا مدّ، لا عَجُز) (لا مدّ، عَجُز) (مدّ، لا عَجُز) (مدّ، عَجُز)
RECEIVED = Table2x2(103_682, 71_794, 50_328, 106)
REPORTED_FREE_BITS = 1.527039
REPORTED_INDEPENDENT_BITS = 1.665476
REPORTED_EXCESS_BITS = 0.138437


def test_the_totals_and_margins_are_derived() -> None:
    """المجموعُ والهوامشُ مُشتَقّةٌ من الخلايا، لا مكتوبةٌ إلى جانبها."""

    assert RECEIVED.total == 225_910
    assert RECEIVED.first_row == 175_476
    assert RECEIVED.second_row == 50_434
    assert RECEIVED.second_column == 71_900


def test_the_g_statistic_reproduces_exactly() -> None:
    """`G = 43,686.2` و`z ≈ 209` — يُعادان من الجدول وحدَه."""

    assert round(RECEIVED.g_statistic(), 1) == 43_686.2
    assert round(RECEIVED.z_equivalent()) == 209


def test_the_conditional_probabilities_reproduce() -> None:
    """`0.409139` و`0.002102`، ونسبتُهما `194.7` — بكسورٍ صحيحةٍ أوّلًا."""

    assert RECEIVED.column_given_no_row() == Fraction(71_794, 175_476)
    assert RECEIVED.column_given_row() == Fraction(106, 50_434)
    assert round(float(RECEIVED.column_given_no_row()), 6) == 0.409139
    assert round(float(RECEIVED.column_given_row()), 6) == 0.002102
    assert round(float(RECEIVED.risk_ratio()), 1) == 194.7


def test_the_odds_ratio_reproduces() -> None:
    """نسبةُ الأرجحيّة `0.00304` كسرًا صحيحًا ثمّ مقرَّبة."""

    assert RECEIVED.odds_ratio() == Fraction(103_682 * 106, 71_794 * 50_328)
    assert round(float(RECEIVED.odds_ratio()), 5) == 0.00304


def test_the_bits_identity_holds_in_sample() -> None:
    """فرقُ البتّات يساوي `G/(2N ln2)` — متطابقةٌ مفحوصةٌ لا مذكورة."""

    cost = RECEIVED.model_cost()
    assert cost.identity_holds
    assert math.isclose(
        cost.excess_bits,
        RECEIVED.g_statistic() / (2 * RECEIVED.total * math.log(2)),
        rel_tol=1e-12,
    )


def test_the_independent_model_costs_more_with_fewer_parameters() -> None:
    """الشجرةُ بحافّتين مستقلّتين أسوأُ من المتعدّد الحرّ — والاتّجاهُ مُعاد."""

    cost = RECEIVED.model_cost()
    assert cost.independent_model_is_worse
    assert cost.excess_bits > 0


def test_the_reported_bits_do_not_reproduce_from_this_table() -> None:
    """أرقامُ البتّات الثلاثةُ **لا تُعاد** من هذا الجدول، والفرقُ دون ٠٫٨٪.

    ونصُّها يقول إنّها على **بياناتٍ محجوبة**، فعدمُ إعادتها من الجدول الكامل
    متوقَّعٌ لا مناقِض؛ وقربُ الرقمين يشهد أنّ النموذجَ لا يحفظ العيّنةَ —
    وهو ما يُنتظَر بمَعلَمتين أو ثلاث. والمُقيَّدُ ههنا أنّ الفرقَ **مقيسٌ
    ومحدود**، لا أنّه مقبولٌ أو مردود.
    """

    cost = RECEIVED.model_cost()
    assert round(cost.free_multinomial_bits, 6) != REPORTED_FREE_BITS
    assert round(cost.independent_bits, 6) != REPORTED_INDEPENDENT_BITS
    for measured, reported in (
        (cost.free_multinomial_bits, REPORTED_FREE_BITS),
        (cost.independent_bits, REPORTED_INDEPENDENT_BITS),
        (cost.excess_bits, REPORTED_EXCESS_BITS),
    ):
        assert abs(measured - reported) / reported < 0.008
    assert not math.isclose(REPORTED_EXCESS_BITS, cost.excess_bits, rel_tol=1e-6)


def test_the_expected_counts_are_derived_from_the_margins() -> None:
    """التوقّعاتُ كسورٌ صحيحةٌ من الهوامش، ومجموعُها المجموعُ نفسُه."""

    expected = RECEIVED.expected()
    assert sum(expected) == RECEIVED.total
    assert expected[3] == Fraction(50_434 * 71_900, 225_910)
    assert float(expected[3]) > 16_000


def test_a_zero_cell_kills_the_odds_ratio_but_not_the_g() -> None:
    """الخليّةُ الصفرُ لا تُسهِم في `G`، وتُبطِل نسبةَ الأرجحيّة فتُرَدّ."""

    sparse = Table2x2(10, 0, 5, 7)
    assert sparse.g_statistic() > 0
    with pytest.raises(ContingencyError):
        sparse.odds_ratio()
    with pytest.raises(ContingencyError):
        Table2x2(10, 5, 0, 0).column_given_row()


def test_degenerate_tables_are_refused() -> None:
    """هامشٌ صفرٌ أو خليّةٌ سالبةٌ يُرَدّان، والبواقي المُسمّاةُ ثلاث."""

    with pytest.raises(ContingencyError):
        Table2x2(0, 0, 5, 7)
    with pytest.raises(ContingencyError):
        Table2x2(-1, 2, 3, 4)
    assert len(CONTINGENCY_NAMED_RESIDUALS) == 3
    assert len(set(CONTINGENCY_NAMED_RESIDUALS)) == 3
