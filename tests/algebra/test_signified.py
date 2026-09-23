"""المدلولُ محسوبًا: الإنتروبيا بكسورٍ، والصفريُّ ببذرةٍ، والتلوّثُ مقيسٌ.

يُثبِت هذا الاختبارُ أربعةَ أشياءَ حاملة: أنّ المعلومةَ المتبادلةَ تُحسَب
بالمتطابقة لا بالتقريب؛ وأنّ **الخامَ موجبٌ على بياناتٍ مستقلّةٍ تمامًا**
فلا يُقرَأ وحدَه البتّة؛ وأنّ التبديلَ يحفظ الهامشين وبذرتُه معطًى يُعاد به
الرقمُ حرفًا؛ وأنّ الشرطَ المُسجَّلَ يُحكَم به ولا يُحكَم عليه.
"""

from __future__ import annotations

from fractions import Fraction

import pytest

from algebra.signified import (
    Direction,
    NullReading,
    Oracle,
    Prediction,
    SignifiedError,
    Verdict,
    contamination_share,
    entropy,
    mutual_information,
    permutation_null,
    seal,
)

PERFECT = [("a", "x"), ("a", "x"), ("b", "y"), ("b", "y"), ("c", "z"), ("c", "z")]
INDEPENDENT = [(form, sense) for form in "abc" for sense in "xyz"]


def test_entropy_is_computed_on_exact_probabilities() -> None:
    """احتمالاتٌ كسورٌ صحيحة، والعائمُ عند اللوغاريتم وحدَه."""

    assert entropy([1, 1]) == 1.0
    assert entropy([1, 1, 1, 1]) == 2.0
    assert entropy([5]) == 0.0
    assert round(entropy([1, 1, 2]), 4) == 1.5
    assert entropy([3, 0, 1]) == entropy([3, 1])  # الصفرُ لا يُسهِم


def test_a_perfect_map_carries_the_whole_entropy() -> None:
    """إسنادٌ تامٌّ: `I = H(الصورة) = H(المدلول)` = log₂٣."""

    assert round(mutual_information(PERFECT), 4) == round(entropy([2, 2, 2]), 4)
    assert round(mutual_information(PERFECT), 3) == 1.585


def test_the_raw_number_is_positive_even_on_independent_data() -> None:
    """الخامُ صفرٌ ههنا والصفريُّ **موجبٌ** — فالخامُ وحدَه يُضلّل لا يُخبر.

    وهذا هو الباقي `A_SPARSE_MUTUAL_INFORMATION_IS_BIASED_UPWARD` مفحوصًا:
    تسعةُ أزواجٍ مستقلّةٍ تمامًا يعطي تبديلُها متوسّطًا موجبًا بأربعة أعشار
    البتّ. فمن قارن خامًّا بصفرٍ حكم بالانحياز لا بالبيانات.
    """

    reading = permutation_null(INDEPENDENT, replicates=200, seed=7)
    assert reading.observed == 0.0
    assert reading.null_mean > 0.4
    assert reading.excess < 0


def test_the_null_preserves_both_margins_and_repeats_with_its_seed() -> None:
    """التبديلُ يخلط المدلولَ وحدَه، والبذرةُ تُعيد الرقمَ حرفًا."""

    first = permutation_null(PERFECT, replicates=50, seed=11)
    again = permutation_null(PERFECT, replicates=50, seed=11)
    other = permutation_null(PERFECT, replicates=50, seed=12)
    assert first == again
    assert first.null_mean != other.null_mean
    assert first.observed == other.observed  # المقيسُ لا يتغيّر بالبذرة
    assert first.excess > 0
    assert first.deviations > 1


def test_contamination_is_a_fraction_not_a_verdict() -> None:
    """نصيبُ التلوّث كسرٌ صحيحٌ يُعلَن، ولا يُقال «ضئيلٌ فيُهمَل»."""

    pairs = [("كتب", "الكتابة"), ("أجج", "الحفيف"), ("شدد", "الشدّة")]
    share = contamination_share(
        pairs, lambda form, sense: all(letter in sense for letter in form)
    )
    assert share == Fraction(2, 3)
    assert contamination_share(pairs, lambda form, sense: False) == 0


def test_a_prediction_is_judged_by_not_judged_against() -> None:
    """الشرطُ يُحكَم به: بلوغُ الحدّ MET، ودونَه FALSIFIED، وسقوطُ أساسه VOID."""

    at_least = Prediction(
        identifier="ش١",
        statistic="فائضٌ بالبتّات",
        threshold=Fraction(1, 100),
        direction=Direction.AT_LEAST,
        falsifies="دعوى التقييد",
    )
    assert at_least.verdict(Fraction(2, 100)) is Verdict.MET
    assert at_least.verdict(Fraction(1, 100)) is Verdict.MET
    assert at_least.verdict(Fraction(0)) is Verdict.FALSIFIED
    assert at_least.verdict(Fraction(9, 10), void=True) is Verdict.VOID


def test_the_seal_moves_when_any_letter_of_a_threshold_moves() -> None:
    """بصمةٌ تتغيّر بتغيُّر حدٍّ واحد، فلا يُبدَّل شرطٌ بعد النظر صمتًا."""

    oracle = Oracle(name="أ", source="ب", extraction="ج")
    first = Prediction(
        identifier="ش١",
        statistic="م",
        threshold=Fraction(1, 100),
        direction=Direction.AT_LEAST,
        falsifies="ق",
    )
    moved = Prediction(
        identifier="ش١",
        statistic="م",
        threshold=Fraction(1, 1_000),
        direction=Direction.AT_LEAST,
        falsifies="ق",
    )
    flipped = Prediction(
        identifier="ش١",
        statistic="م",
        threshold=Fraction(1, 100),
        direction=Direction.AT_MOST,
        falsifies="ق",
    )
    assert seal(oracle, [first]) != seal(oracle, [moved])
    assert seal(oracle, [first]) != seal(oracle, [flipped])
    assert seal(oracle, [first]) == seal(oracle, [first])


def test_what_cannot_be_computed_is_refused() -> None:
    """إسنادٌ خالٍ، وتبديلٌ واحد، وانحرافٌ صفر، وأوراكلُ بلا مصدر — تُرَدّ."""

    with pytest.raises(SignifiedError):
        mutual_information([])
    with pytest.raises(SignifiedError):
        entropy([])
    with pytest.raises(SignifiedError):
        entropy([-1, 2])
    with pytest.raises(SignifiedError):
        permutation_null(PERFECT, replicates=1, seed=1)
    with pytest.raises(SignifiedError):
        NullReading(1.0, 0.5, 0.0, 10, 1).deviations
    with pytest.raises(SignifiedError):
        Oracle(name="أ", source="  ", extraction="ج")
    with pytest.raises(SignifiedError):
        contamination_share([], lambda form, sense: True)
    with pytest.raises(SignifiedError):
        seal(Oracle(name="أ", source="ب", extraction="ج"), [])
