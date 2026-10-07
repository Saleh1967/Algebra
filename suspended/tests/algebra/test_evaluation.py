"""التقويم: التسرّبُ يُرَدّ، والامتناعُ يُفصَل، وخطُّ الأساس على مجموعته.

يُثبِت هذا الاختبارُ أربعةً: أنّ قسمةً متقاطعةً تُرَدّ في الإنشاء؛ وأنّ
مجموعةَ قرارٍ لمست الاختبار **لا تُسمّى خارج العيّنة** وإن صحّ حسابُها؛ وأنّ
الامتناعَ يُخرِج ثلاثةَ أرقامٍ لا واحدًا؛ وأنّ خطَّ الأساس يتغيّر بتغيّر
المجموعة التي يُحسَب عليها.
"""

from __future__ import annotations

from fractions import Fraction

import pytest

from algebra.evaluation import (
    EVALUATION_NAMED_RESIDUALS,
    DecisionSet,
    EvaluationError,
    Split,
    Tally,
    majority_baseline,
)

SPLIT = Split(train=frozenset("abcde"), test=frozenset("fghij"))


def test_a_split_with_any_overlap_is_refused() -> None:
    """مفتاحٌ واحدٌ في الجهتين يُبطِل القسمة، ولا يُغتفَر بصغره."""

    with pytest.raises(EvaluationError) as raised:
        Split(train=frozenset("abc"), test=frozenset("cde"))
    assert "تقاطع" in str(raised.value)
    with pytest.raises(EvaluationError):
        Split(train=frozenset(), test=frozenset("a"))
    assert SPLIT.test_share == Fraction(1, 2)


def test_a_decision_set_that_touched_the_test_may_not_claim_to_be_outside_it() -> None:
    """المبنيّةُ على المدوَّنة كلِّها تُرَدّ، والمبنيّةُ على التدريب تمرّ."""

    leaky = DecisionSet(
        name="القائمةُ المغلقة",
        members=frozenset({"س"}),
        built_from=frozenset("abcdefghij"),
    )
    clean = DecisionSet(
        name="القائمةُ المغلقة", members=frozenset({"س"}), built_from=frozenset("abcde")
    )
    assert leaky.is_leaky(SPLIT)
    assert len(leaky.leaked_keys(SPLIT)) == 5
    with pytest.raises(EvaluationError):
        leaky.assert_out_of_sample(SPLIT)
    assert not clean.is_leaky(SPLIT)
    clean.assert_out_of_sample(SPLIT)


def test_a_decision_set_must_say_what_it_was_built_from() -> None:
    """مجموعةٌ لا تقول أصلَها لا يُعرَف أخارجَ العيّنة هي أم داخلها."""

    with pytest.raises(EvaluationError):
        DecisionSet(name="س", members=frozenset({"x"}), built_from=frozenset())
    with pytest.raises(EvaluationError):
        DecisionSet(name="  ", members=frozenset({"x"}), built_from=frozenset("a"))


def test_abstention_yields_three_numbers_not_one() -> None:
    """سعةٌ وصوابٌ ودقّةٌ بحساب الامتناع خطأً — والفرقُ بينها يُعلَن."""

    tally = Tally(correct=70, wrong=10, abstained=20)
    assert tally.total == 100
    assert tally.fired == 80
    assert tally.coverage == Fraction(4, 5)
    assert tally.precision_where_it_fires == Fraction(7, 8)
    assert tally.accuracy_charging_abstention == Fraction(7, 10)
    assert tally.abstention_inflates_the_error_by == Fraction(7, 40)
    assert tally.precision_where_it_fires > tally.accuracy_charging_abstention


def test_a_rule_that_never_fires_has_no_precision() -> None:
    """قاعدةٌ لم تنطبق قطُّ لا صوابَ لها، ولا يُقال «صفر» ولا «مئة»."""

    never = Tally(correct=0, wrong=0, abstained=9)
    assert never.coverage == 0
    assert never.accuracy_charging_abstention == 0
    assert never.abstention_inflates_the_error_by == 0
    with pytest.raises(EvaluationError):
        never.precision_where_it_fires
    with pytest.raises(EvaluationError):
        Tally(correct=0, wrong=0, abstained=0)
    with pytest.raises(EvaluationError):
        Tally(correct=-1, wrong=0, abstained=1)


def test_the_baseline_moves_with_the_set_it_is_computed_on() -> None:
    """خطُّ أساسٍ من التدريب ليس خطَّ الاختبار، والفرقُ بينهما ليس قدرةً."""

    train_labels = ["N"] * 90 + ["V"] * 10
    test_labels = ["N"] * 60 + ["V"] * 40
    assert majority_baseline(train_labels) == Fraction(9, 10)
    assert majority_baseline(test_labels) == Fraction(3, 5)
    assert majority_baseline(train_labels) != majority_baseline(test_labels)
    with pytest.raises(EvaluationError):
        majority_baseline([])


def test_the_named_residuals_are_seven_and_distinct() -> None:
    """البواقي المُسمّاةُ سبعٌ، ولا تكرارَ فيها — وكانت خمسًا.

    والزائدتان: أنّ ألفَ وقوعٍ من أربعة أنواعٍ أربعُ مشاهدات، وأنّ مقياسًا
    برتبةٍ لا يقيس شيئًا على وحدةٍ أقصرَ منها.
    """

    assert len(EVALUATION_NAMED_RESIDUALS) == 7
    assert len(set(EVALUATION_NAMED_RESIDUALS)) == 7
