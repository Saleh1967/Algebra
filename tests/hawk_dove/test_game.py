"""لعبةُ الصقر والحمامة: توازنٌ مُشتَقٌّ بالكسور، ودينامِكا تلتقي، وأمثلٌ لا يُبلَغ.

يُثبِت هذا الاختبارُ ثمانيةَ أشياء: أنّ مصفوفةَ العوائد هي الكلاسيكيّةَ بحدودها
الأربعة، وأنّ العائدَين يتساويان عند التوازن تساويًا تامًّا بالكسور لا تقريبًا،
وأنّ نسبةَ الصقور `V/C` حين تزيد الكلفةُ على القيمة، وأنّ الصقرَ الخالصَ هو
المستقرُّ حين لا تزيد، وأنّ دينامِكا المُماثلة تلتقي عند التوازن من أعلاه ومن
أدناه، وأنّ فرقَ الأمثليّة موجبٌ في المجالين كليهما فالاستقرارُ ليس صلاحًا،
وأنّ مدخلًا خارج شرطه يُرَدُّ ولا يُقرَّب، وأنّ خطوةً أكبرَ من أن تُحاكي
تُرَدُّ ولا تُقصَر صمتًا.
"""

from __future__ import annotations

from fractions import Fraction

import pytest

from hawk_dove.game import (
    EquilibriumKind,
    HawkDoveError,
    HawkDoveGame,
    Strategy,
)

_COSTLY = HawkDoveGame(value=Fraction(2), cost=Fraction(10))
_CHEAP = HawkDoveGame(value=Fraction(10), cost=Fraction(2))


def test_the_payoff_matrix_is_the_classical_one() -> None:
    """الحدودُ الأربعة: اقتسامُ القيمة والكلفة، والقيمةُ كاملةً، وصفرٌ، ونصفٌ."""

    assert _COSTLY.payoff(Strategy.HAWK, Strategy.HAWK) == Fraction(-4)
    assert _COSTLY.payoff(Strategy.HAWK, Strategy.DOVE) == Fraction(2)
    assert _COSTLY.payoff(Strategy.DOVE, Strategy.HAWK) == Fraction(0)
    assert _COSTLY.payoff(Strategy.DOVE, Strategy.DOVE) == Fraction(1)


def test_the_two_strategies_are_exactly_indifferent_at_equilibrium() -> None:
    """التساوي تامٌّ بالكسور لا تقريبًا، وهو شرطُ اشتقاق النسبة لا نتيجةٌ بعده."""

    share = _COSTLY.equilibrium().hawk_share

    assert _COSTLY.expected_payoff(Strategy.HAWK, share) == _COSTLY.expected_payoff(
        Strategy.DOVE, share
    )
    assert _COSTLY.is_equilibrium(share)
    assert not _COSTLY.is_equilibrium(Fraction(1, 2))


def test_the_mixed_share_is_the_value_over_the_cost() -> None:
    """حين تزيد الكلفةُ على القيمة يكون التوازنُ خليطًا نسبتُه V/C."""

    equilibrium = _COSTLY.equilibrium()

    assert equilibrium.kind is EquilibriumKind.MIXED
    assert equilibrium.hawk_share == Fraction(1, 5)
    assert equilibrium.hawk_share == _COSTLY.value / _COSTLY.cost


def test_a_cheap_fight_makes_the_pure_hawk_stable() -> None:
    """حين لا تزيد الكلفةُ على القيمة فلا خليط: الصقرُ الخالصُ هو المستقرّ."""

    equilibrium = _CHEAP.equilibrium()

    assert equilibrium.kind is EquilibriumKind.PURE_HAWK
    assert equilibrium.hawk_share == Fraction(1)

    equal = HawkDoveGame(value=Fraction(6), cost=Fraction(6)).equilibrium()

    assert equal.kind is EquilibriumKind.PURE_HAWK
    assert equal.hawk_share == Fraction(1)


def test_the_replicator_dynamics_converge_from_both_sides() -> None:
    """الدينامِكا تلتقي عند التوازن صاعدةً من أدناه وهابطةً من أعلاه."""

    target = float(_COSTLY.equilibrium().hawk_share)

    for start in (0.02, 0.9):
        path = _COSTLY.simulate(start, 600, 0.5)
        assert abs(path[-1] - target) < 1e-6
        assert abs(path[-1] - target) < abs(path[0] - target)


def test_the_stable_state_is_never_the_group_optimum() -> None:
    """فرقُ الأمثليّة موجبٌ في المجالين: أعلى متوسّطٍ لا يبلغه مجتمعٌ فيه صقر."""

    for game in (_COSTLY, _CHEAP):
        equilibrium = game.equilibrium()
        assert equilibrium.all_dove_payoff == game.value / 2
        assert equilibrium.optimality_gap > 0
        assert equilibrium.mean_payoff < equilibrium.all_dove_payoff


def test_an_input_outside_its_condition_is_refused() -> None:
    """قيمةٌ أو كلفةٌ غيرُ موجبةٍ أو عائمٌ يُرَدّ، ونسبةٌ خارج المجال تُرَدّ."""

    with pytest.raises(HawkDoveError, match="موجبٌ شرطَ إنشاء"):
        HawkDoveGame(value=Fraction(0), cost=Fraction(4))
    with pytest.raises(HawkDoveError, match="موجبٌ شرطَ إنشاء"):
        HawkDoveGame(value=Fraction(4), cost=Fraction(-1))
    with pytest.raises(HawkDoveError, match="كسرٌ صحيحٌ لا عائم"):
        HawkDoveGame(value=0.5, cost=Fraction(4))  # type: ignore[arg-type]
    with pytest.raises(HawkDoveError, match="بين الصفر والواحد"):
        _COSTLY.expected_payoff(Strategy.HAWK, Fraction(3, 2))


def test_a_step_too_large_to_simulate_is_refused_not_clamped() -> None:
    """خطوةٌ تُخرِج النسبةَ عن مجالها تُرَدُّ بخطوتها، ولا تُقصَر صمتًا."""

    with pytest.raises(HawkDoveError, match="أخرجت النسبةَ عن مجالها"):
        _CHEAP.simulate(0.5, 5, 100.0)
    with pytest.raises(HawkDoveError, match="طولُ الخطوة موجب"):
        _COSTLY.replicator_step(0.5, 0.0)
