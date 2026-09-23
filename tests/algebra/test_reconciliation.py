"""مطابقةُ الأرقام: المجالُ مُشتَقٌّ، والاصطلاحُ مُعلَن، والرفضُ مفحوص.

يُثبِت هذا الاختبارُ سلوكَ الوحدة على أرقامٍ مصنوعةٍ لا مأخوذةٍ من نصّ: أنّ
دقّةَ الطباعة تُقرأ من النصّ لا من القيمة، وأنّ المجال نصفُ مفتوحٍ بالاصطلاح
المُعلَن، وأنّ فرقَ رقمَين يجمع العرضَين، وأنّ حاصلًا بمقامٍ خشنٍ **لا يحدَّد**
وإن كان بسطُه دقيقًا، وأنّ المقامَ المُستلزَمَ يُحسَب فيُحكَم به، وأنّ البقيّةَ
تُعلَن ولا تُوزَّع، وأنّ ما لا يُحسَب يُرَدّ لا يُحمَل على أقرب مقبول.
"""

from __future__ import annotations

from fractions import Fraction

import pytest

from algebra.reconciliation import (
    RECONCILIATION_NAMED_RESIDUALS,
    Difference,
    Partition,
    PrintedFigure,
    Quotient,
    ReconciliationError,
    rounds_alike,
    rounds_to,
)


def test_the_precision_is_read_from_the_text_not_from_the_value() -> None:
    """«٠٫٠٠٠٤» و«٠٫٠٠٠٤٠٠» قيمةٌ واحدةٌ وإعلانان، والنصُّ يفرّق بينهما."""

    coarse = PrintedFigure("0.0004")
    fine = PrintedFigure("0.000400")
    assert coarse.value == fine.value
    assert (coarse.places, coarse.significant_digits) == (4, 1)
    assert (fine.places, fine.significant_digits) == (6, 3)
    assert coarse.half_width == Fraction(1, 20_000)
    assert fine.half_width == Fraction(1, 2_000_000)


def test_the_interval_is_half_open_by_the_declared_convention() -> None:
    """المنتصفُ الأدنى داخلٌ والأعلى خارج — اصطلاحٌ مُعلَنٌ لا مضمَر."""

    figure = PrintedFigure("1.2")
    low, high = figure.interval()
    assert (low, high) == (Fraction(115, 100), Fraction(125, 100))
    assert figure.prints(low)
    assert not figure.prints(high)
    assert rounds_to(Fraction(125, 100), 1) == Fraction(13, 10)
    assert rounds_to(Fraction(-125, 100), 1) == Fraction(-12, 10)


def test_rounding_alike_sees_a_gap_that_a_reader_of_percentages_cannot() -> None:
    """رقمان مختلفان يُطبَعان بصورةٍ واحدة، فالفرقُ مستورٌ بالتقريب."""

    assert rounds_alike(Fraction(74_206, 100_000), Fraction(74_234, 100_000), 3)
    assert not rounds_alike(Fraction(74_206, 100_000), Fraction(74_234, 100_000), 4)
    assert rounds_to(Fraction(1_949), -1) == rounds_to(Fraction(1_951), -1)


def test_a_difference_adds_the_two_widths_it_came_from() -> None:
    """فرقُ رقمَين ليس رقمًا مطبوعًا واحدًا: عرضُه مجموعُ عرضَيهما."""

    gap = Difference(PrintedFigure("18.08"), PrintedFigure("17.00"))
    low, high = gap.interval()
    assert gap.value == Fraction(108, 100)
    assert (low, high) == (Fraction(107, 100), Fraction(109, 100))
    assert high - low == 2 * PrintedFigure("18.08").half_width * 2


def test_a_coarse_denominator_determines_almost_nothing() -> None:
    """بسطٌ بستّ خاناتٍ على مقامٍ بخانةٍ واحدة: الحاصلُ غيرُ محدَّدٍ البتّة."""

    quotient = Quotient(PrintedFigure("0.778835"), PrintedFigure("0.0004"))
    low, high = quotient.interval()
    assert low < quotient.nominal() < high
    assert quotient.determined_significant_digits == 0
    assert round(float(high / low), 2) == 1.29
    claim = quotient.claim("1947.1")
    assert claim.lies_in_interval
    assert claim.digits_announced == 5
    assert claim.is_over_announced


def test_two_different_reports_of_one_measurement_can_both_be_consistent() -> None:
    """رقمان مختلفان عن قياسٍ واحدٍ يقعان كلاهما في المجال — فالخلافُ في النشر."""

    quotient = Quotient(PrintedFigure("0.778835"), PrintedFigure("0.0004"))
    first, second = quotient.claim("1900.0"), quotient.claim("2100.0")
    assert first.lies_in_interval and second.lies_in_interval
    assert first.implied_denominator_prints_as_declared
    assert second.implied_denominator_prints_as_declared
    assert first.implied_denominator() != second.implied_denominator()


def test_a_report_outside_the_interval_is_not_a_precision_question() -> None:
    """ما خرج عن المجال لا يُعلَّل بالتقريب: مقامُه المُستلزَمُ يُطبَع بغير صورته."""

    quotient = Quotient(PrintedFigure("0.778835"), PrintedFigure("0.0004"))
    stray = quotient.claim("3000.0")
    assert not stray.lies_in_interval
    assert not stray.implied_denominator_prints_as_declared


def test_a_partition_names_its_residue_and_can_hide_it_in_a_share() -> None:
    """البقيّةُ تُعلَن عددًا؛ وقد تكون مستورةً في النسبة المطبوعة."""

    balanced = Partition(parts=(10_784, 3_743), declared_total=14_527)
    assert balanced.balances and balanced.residue == 0
    short = Partition(parts=(10_780, 3_743), declared_total=14_527)
    assert short.residue == 4
    assert short.residue_is_hidden_in_share(base=14_527, places=3)
    assert not short.residue_is_hidden_in_share(base=14_527, places=5)


def test_what_cannot_be_computed_is_refused() -> None:
    """نصٌّ ليس رقمًا، ومقامٌ يعبر الصفر، وأساسٌ صفرٌ، وتجزئةٌ خاليةٌ — كلُّها تُرَدّ."""

    for text in ("١٫٢", "1,2", "1e3", "", " 1.2"):
        with pytest.raises(ReconciliationError):
            PrintedFigure(text)
    with pytest.raises(ReconciliationError):
        Quotient(PrintedFigure("1.0"), PrintedFigure("0.0"))
    with pytest.raises(ReconciliationError):
        Partition(parts=(), declared_total=0)
    with pytest.raises(ReconciliationError):
        Partition(parts=(1,), declared_total=1).residue_is_hidden_in_share(0, 2)
    with pytest.raises(ReconciliationError):
        PrintedFigure("0.0").relative_half_width


def test_the_named_residuals_are_five_and_distinct() -> None:
    """البواقي المُسمّاةُ خمسٌ، ولا تكرارَ فيها."""

    assert len(RECONCILIATION_NAMED_RESIDUALS) == 5
    assert len(set(RECONCILIATION_NAMED_RESIDUALS)) == 5
