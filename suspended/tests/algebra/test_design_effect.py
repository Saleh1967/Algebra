"""بوّابةُ أثر التصميم: تُرَدّ قراءةٌ تخالف اشتقاقَها، و«مردود» لا يُبلَغ من z.

**ما تفحصه هذه الوحدة**: أنّ المنزلةَ **مُشتَقّةٌ** لا مكتوبة، وأنّ بابَ
الردّ مغلقٌ إلّا بهامشٍ مُعلَنٍ ومجالٍ مقيس، وأنّ سؤالَ حجم العنقود يُرَدّ
ما لم يُعلَن نصيبُ المعزولات.
"""

from __future__ import annotations

from fractions import Fraction

import pytest

from algebra.design_effect import (
    DESIGN_EFFECT_NAMED_RESIDUALS,
    ClusterProfile,
    DesignEffectError,
    EffectReading,
    EffectStanding,
    conventional_threshold,
    deflate,
    design_effect,
    read_effect,
    refuted_against,
)


def test_the_profile_refuses_an_undeclared_or_impossible_isolated_share() -> None:
    """نصيبُ المعزولات في [٠، ١)؛ وواحدٌ صحيحٌ يعني ألّا عنقودَ يُسهم."""

    for isolated in (Fraction(1), Fraction(-1, 10), Fraction(3, 2)):
        with pytest.raises(DesignEffectError):
            ClusterProfile(observations=10, clusters=5, isolated=isolated)

    with pytest.raises(DesignEffectError):
        ClusterProfile(observations=10, clusters=0, isolated=Fraction(0))
    with pytest.raises(DesignEffectError):
        ClusterProfile(observations=-1, clusters=5, isolated=Fraction(0))


def test_the_two_means_differ_whenever_anything_is_isolated() -> None:
    """المتوسّطُ على الكلّ غيرُ المتوسّط على ذوي الشاهد — والثاني يدخل الأثر."""

    none_isolated = ClusterProfile(observations=10, clusters=5, isolated=Fraction(0))
    assert none_isolated.mean_over_all == none_isolated.mean_over_active == 2

    half = ClusterProfile(observations=10, clusters=5, isolated=Fraction(1, 2))
    assert half.mean_over_all == 2
    assert half.mean_over_active == 4


def test_the_design_effect_is_one_at_zero_correlation_and_the_mean_at_one() -> None:
    """`DEFF = 1 + (m̄ − 1)ρ`: طرفاه الواحدُ والمتوسّطُ، وخارجُ [٠، ١] يُرَدّ."""

    assert design_effect(Fraction(5), Fraction(0)) == 1
    assert design_effect(Fraction(5), Fraction(1)) == 5
    assert design_effect(Fraction(5), Fraction(1, 2)) == 3

    for correlation in (Fraction(-1, 100), Fraction(101, 100)):
        with pytest.raises(DesignEffectError):
            design_effect(Fraction(5), correlation)
    with pytest.raises(DesignEffectError):
        design_effect(Fraction(1, 2), Fraction(1, 2))
    with pytest.raises(DesignEffectError):
        deflate(2.0, Fraction(1, 2))


def test_the_standing_is_derived_and_a_contradicting_reading_is_refused() -> None:
    """قراءةٌ تُعلِن «بلغ» ومقسومُها دون الحدّ تُرَدّ في المُنشئ."""

    with pytest.raises(DesignEffectError):
        EffectReading(
            raw=1.0,
            deflated=1.0,
            effect=Fraction(1),
            correlation=None,
            threshold=conventional_threshold(),
            standing=EffectStanding.ESTABLISHED,
        )

    # و«مردود» لا يُبنى من قراءةِ z ألبتّة
    with pytest.raises(DesignEffectError):
        EffectReading(
            raw=1.0,
            deflated=1.0,
            effect=Fraction(1),
            correlation=None,
            threshold=conventional_threshold(),
            standing=EffectStanding.REFUTED,
        )


def test_an_unmeasured_correlation_is_read_as_a_bound_at_its_extreme() -> None:
    """`ρ` غيرُ مُعلَنٍ ⇒ الأثرُ عند أقصاه، والقراءةُ تُسمّي نفسَها حدًّا."""

    profile = ClusterProfile(observations=20, clusters=5, isolated=Fraction(0))
    bound = read_effect(4.0, profile)
    assert bound.is_a_bound_not_an_estimate
    assert bound.effect == profile.mean_over_active == 4
    assert bound.deflated == 2.0
    assert bound.standing is EffectStanding.ESTABLISHED

    estimate = read_effect(4.0, profile, correlation=Fraction(0))
    assert not estimate.is_a_bound_not_an_estimate
    assert estimate.effect == 1 and estimate.deflated == 4.0


def test_refutation_needs_a_margin_written_before_the_look() -> None:
    """مجالٌ أعلاه دون الهامش يردّ، ومجالٌ يشمله لا يردّ ولا يُثبِت."""

    margin = Fraction(1, 10)
    assert refuted_against((Fraction(1, 100), Fraction(9, 100)), margin) is (
        EffectStanding.REFUTED
    )
    assert refuted_against((Fraction(1, 100), Fraction(11, 100)), margin) is (
        EffectStanding.UNESTABLISHED
    )

    with pytest.raises(DesignEffectError):
        refuted_against((Fraction(2, 10), Fraction(1, 10)), margin)
    with pytest.raises(DesignEffectError):
        refuted_against((Fraction(0), Fraction(1, 10)), Fraction(0))


def test_the_named_residuals_are_three_and_distinct() -> None:
    """ثلاثةُ بواقٍ مُسمّاة، ولا اسمَ يتكرّر."""

    assert len(DESIGN_EFFECT_NAMED_RESIDUALS) == 3
    assert len(set(DESIGN_EFFECT_NAMED_RESIDUALS)) == 3
    joined = " ".join(DESIGN_EFFECT_NAMED_RESIDUALS)
    assert "TheSquareRootRuleFixesTheCorrelationAtOne" in joined
    assert "AConservativeBoundCannotRefute" in joined
    assert "TheMeanOverAllIsNotTheMeanOverThoseThatHaveAny" in joined
