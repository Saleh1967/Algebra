"""الشاهدُ المفرد: المفترقُ مُسعَّرٌ، و«خارجُ المجال» غيرُ مجّانيّ.

يُثبِت هذا الاختبارُ أربعةَ أشياءَ حاملة: أنّ فرعًا بلا ثمنٍ لا يُقيَّد؛ وأنّ
قسمةَ شاهدٍ مفردٍ على مجتمعٍ **مردودةٌ في المتن**؛ وأنّ «خارجَ المجال» يُرَدّ
ما دام اصطلاحُها يحمل غيرَها، ويُقبَل إن كان عقيمًا؛ وأنّ المظنونَ يُسمّى مع
فحصه الفاصل ولا يُخلَط بما ثبت.
"""

from __future__ import annotations

import pytest

from algebra.decisions import Branch, DecisionError
from algebra.witness import (
    WITNESS_NAMED_RESIDUALS,
    Case,
    Convention,
    Fork,
    WitnessError,
)

BARREN = Convention(name="اصطلاحٌ عقيم", decides="أمرًا لا يقوم عليه سواه")
LOADED = Convention(
    name="اصطلاحٌ حامل",
    decides="أمرًا يقوم عليه غيرُه",
    carries=("قياسٌ أوّل", "قياسٌ ثانٍ"),
    pending=(("قياسٌ مظنون", "الفحصُ الفاصلُ الذي يحسمه"),),
)


def _fork(convention: Convention) -> Fork:
    return Fork(
        case=Case(name="حالة", violates="قاعدة", under=convention),
        rule_is_false=Branch("القاعدةُ باطلة", "تسقط", "ما يلزم عنها"),
        convention_is_wrong=Branch("الاصطلاحُ باطل", "يُبدَّل", "ما يحمله"),
    )


def test_a_branch_without_a_price_is_refused_at_construction() -> None:
    """الفرعُ يرث شرطَ `decisions`: بلا ثمنٍ لا يُقيَّد."""

    with pytest.raises(DecisionError):
        Branch("الاصطلاحُ باطل", "يُبدَّل", "")


def test_a_single_witness_will_not_become_a_rate() -> None:
    """القسمةُ مردودةٌ في المتن، لا منهيٌّ عنها في تعليق."""

    with pytest.raises(WitnessError):
        _fork(LOADED).as_rate(30_785)
    with pytest.raises(WitnessError):
        _fork(BARREN).as_rate(1_000_000)


def test_out_of_scope_is_free_only_for_a_barren_convention() -> None:
    """يُقبَل الإخراجُ إن كان الاصطلاحُ عقيمًا، ويُرَدّ إن حمل غيرَها."""

    barren = _fork(BARREN)
    assert barren.may_be_called_out_of_scope
    assert barren.out_of_scope_withdraws() == ()
    loaded = _fork(LOADED)
    assert not loaded.may_be_called_out_of_scope
    assert loaded.cost_of_denying == ("قياسٌ أوّل", "قياسٌ ثانٍ")
    with pytest.raises(WitnessError) as raised:
        loaded.out_of_scope_withdraws()
    assert "قياسٌ أوّل" in str(raised.value)


def test_the_pending_cost_is_named_with_its_deciding_test() -> None:
    """المظنونُ يُسمّى مع فحصه، ولا يُعَدّ في الثابت."""

    fork = _fork(LOADED)
    assert fork.pending_costs == (("قياسٌ مظنون", "الفحصُ الفاصلُ الذي يحسمه"),)
    assert "قياسٌ مظنون" not in fork.cost_of_denying
    with pytest.raises(WitnessError):
        Convention(name="أ", decides="ب", pending=(("مظنون", "   "),))
    with pytest.raises(WitnessError):
        Convention(name="أ", decides="ب", carries=("س",), pending=(("س", "فحص"),))


def test_what_is_not_a_case_is_refused() -> None:
    """حالةٌ بلا اسمٍ أو بلا قاعدةٍ أو بلا وقوعٍ، واصطلاحٌ بلا قرار — تُرَدّ."""

    with pytest.raises(WitnessError):
        Case(name="  ", violates="قاعدة", under=BARREN)
    with pytest.raises(WitnessError):
        Case(name="حالة", violates="", under=BARREN)
    with pytest.raises(WitnessError):
        Case(name="حالة", violates="قاعدة", under=BARREN, occurrences=0)
    with pytest.raises(WitnessError):
        Convention(name="أ", decides="   ")


def test_the_named_residuals_are_five_and_distinct() -> None:
    """البواقي المُسمّاةُ خمسٌ، ولا تكرارَ فيها."""

    assert len(WITNESS_NAMED_RESIDUALS) == 5
    assert len(set(WITNESS_NAMED_RESIDUALS)) == 5
