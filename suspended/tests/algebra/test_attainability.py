"""بلوغُ الحدّ: حدٌّ لا يُبلَغ، وحدٌّ على السكّين، وحدٌّ فيه سعة.

يُثبِت هذا الاختبارُ تسعةَ أشياء: أنّ أرضيّةَ التباديل `1/(B+1)` بكسورٍ صحيحة،
وأنّ حدًّا دون الأرضيّة **لا يُبلَغ** فمخارجُه صفرٌ، وأنّ `α = 0.05/75` مع
2,000 تكرارٍ يعطي **مخرجًا واحدًا** — أي أنّ تجاوزًا واحدًا يُسقِط الأثر —
وأنّ 20,000 تعطي ثلاثةَ عشرَ مخرجًا، وأنّ أدنى تكرارٍ لعشرةِ مخارجَ 14,999،
وأنّ المنازلَ ثلاثٌ مغلقة، وأنّ حدَّ السعة مُعلَنٌ معطًى لا مخفيًّا، وأنّ
المداخلَ خارجَ المجال تُرَدّ، وأنّ قراءةً بلا مخرجٍ لا تُسمّى إلّا «لا يُبلَغ».
"""

from __future__ import annotations

from fractions import Fraction

import pytest

from algebra.attainability import (
    ATTAINABILITY_NAMED_RESIDUALS,
    Attainability,
    AttainabilityError,
    AttainabilityReading,
    attainable_rejection_outcomes,
    bonferroni_threshold,
    minimum_replicates_for,
    permutation_floor,
    read_attainability,
)

ALPHA = Fraction(5, 100)


def test_the_permutation_floor_is_exact() -> None:
    """`1/(B+1)` كسرًا صحيحًا لا عائمًا."""

    assert permutation_floor(2000) == Fraction(1, 2001)
    assert permutation_floor(1) == Fraction(1, 2)
    with pytest.raises(AttainabilityError):
        permutation_floor(0)


def test_bonferroni_divides_by_the_declared_family() -> None:
    """`α/m`؛ وعددُ العائلة يُعلَن قبل العدّ."""

    assert bonferroni_threshold(ALPHA, 75) == Fraction(1, 1500)
    assert bonferroni_threshold(ALPHA, 1) == ALPHA
    with pytest.raises(AttainabilityError):
        bonferroni_threshold(ALPHA, 0)
    with pytest.raises(AttainabilityError):
        bonferroni_threshold(Fraction(0), 5)


def test_a_threshold_below_the_floor_is_never_reached() -> None:
    """حدٌّ دون الأرضيّة مخارجُه صفرٌ، ومنزلتُه «لا يُبلَغ»."""

    threshold = Fraction(1, 100_000)
    assert attainable_rejection_outcomes(threshold, 100) == 0
    assert read_attainability(threshold, 100).standing is Attainability.UNREACHABLE


def test_the_knife_edge_case_is_measured() -> None:
    """`α = 0.05/75` مع 2,000: مخرجٌ **واحد** — تجاوزٌ واحدٌ يُسقِط الأثر."""

    threshold = bonferroni_threshold(ALPHA, 75)
    assert attainable_rejection_outcomes(threshold, 2000) == 1
    assert Fraction(2, 2001) > threshold
    assert read_attainability(threshold, 2000).standing is Attainability.KNIFE_EDGE


def test_raising_the_replicates_buys_room() -> None:
    """20,000 تكرارًا تعطي ثلاثةَ عشرَ مخرجًا، فتصير القراءةُ سعةً."""

    threshold = bonferroni_threshold(ALPHA, 75)
    assert attainable_rejection_outcomes(threshold, 20_000) == 13
    assert read_attainability(threshold, 20_000).standing is Attainability.ROOMY


def test_the_minimum_replicates_are_derived() -> None:
    """أدنى تكرارٍ لعشرةِ مخارجَ 14,999، ويُفحَص بأنّ ما دونه لا يكفي."""

    threshold = bonferroni_threshold(ALPHA, 75)
    needed = minimum_replicates_for(threshold, 10)
    assert needed == 14_999
    assert attainable_rejection_outcomes(threshold, needed) >= 10
    assert attainable_rejection_outcomes(threshold, needed - 1) < 10


def test_the_standing_type_is_closed_and_the_room_is_declared() -> None:
    """ثلاثُ منازلَ، وحدُّ السعة معطًى مُعلَنٌ لا مخفيّ."""

    assert [standing.name for standing in Attainability] == [
        "UNREACHABLE",
        "KNIFE_EDGE",
        "ROOMY",
    ]
    threshold = bonferroni_threshold(ALPHA, 75)
    assert read_attainability(threshold, 20_000, roomy_at=20).standing is (
        Attainability.KNIFE_EDGE
    )
    with pytest.raises(AttainabilityError):
        read_attainability(threshold, 100, roomy_at=1)


def test_a_reading_without_outcomes_can_only_be_unreachable() -> None:
    """قراءةٌ بلا مخرجٍ تُسمّى «لا يُبلَغ» أو تُرَدّ."""

    with pytest.raises(AttainabilityError):
        AttainabilityReading(
            threshold=Fraction(1, 10),
            replicates=10,
            floor=Fraction(1, 11),
            outcomes=0,
            standing=Attainability.ROOMY,
        )


def test_named_residuals_are_deposited() -> None:
    """الباقيان المُسمّيان، ولا مكرَّرَ فيهما."""

    assert len(ATTAINABILITY_NAMED_RESIDUALS) == 3
    assert len(set(ATTAINABILITY_NAMED_RESIDUALS)) == 3


def test_a_reading_may_not_contradict_what_it_was_derived_from() -> None:
    """حقلٌ مُشتَقٌّ يُخالف اشتقاقَه ليس قراءةً بل دعوًى ثانيةً تُرَدّ.

    وكان البناءُ يقبل قراءةً كاذبةً في نفسها: حدٌّ ½ وتكرارٌ ١٠ مع أرضيّةٍ
    ⅓ ومخارجَ ٩٩ — والمشتقُّ منهما ١⁄١١ وخمسة. فالقراءةُ تُصدَّق بما اشتُقّت
    منه لا بمن كتبها.
    """

    sound = read_attainability(Fraction(1, 2), 10)
    assert sound.floor == Fraction(1, 11)
    assert sound.outcomes == 5

    for wrong in (
        {"floor": Fraction(1, 3)},
        {"outcomes": 99},
        {"outcomes": 0, "standing": Attainability.UNREACHABLE},
    ):
        with pytest.raises(AttainabilityError):
            AttainabilityReading(
                **{
                    "threshold": Fraction(1, 2),
                    "replicates": 10,
                    "floor": Fraction(1, 11),
                    "outcomes": 5,
                    "standing": Attainability.ROOMY,
                    **wrong,
                }
            )

    # و«لا يُبلَغ» مع مخارجَ مُعلَنةٍ تناقضٌ كذلك
    with pytest.raises(AttainabilityError):
        AttainabilityReading(
            threshold=Fraction(1, 2),
            replicates=10,
            floor=Fraction(1, 11),
            outcomes=5,
            standing=Attainability.UNREACHABLE,
        )
