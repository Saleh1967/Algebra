"""سجلُّ القرارات: فرعٌ بلا ثمنٍ يُرَدّ، ومُفوَّضٌ يُفرَّق عن متَّخَذ.

يُثبِت هذا الاختبارُ عشرةَ أشياء: أنّ المنازلَ أربعٌ مغلقة، وأنّ فرعًا بلا ثمنٍ
يُرفَض، وأنّ قرارًا بفرعٍ واحدٍ أو بلا محجوبٍ يُرفَض، وأنّ معلَّقًا بفرعٍ مُختارٍ
أو بسلطةٍ يُرفَض، وأنّ محسومًا بلا سلطةٍ أو بلا تاريخٍ يُرفَض، وأنّ مُفوَّضًا بلا
وكيلٍ يُرفَض وأنّ وكيلًا في غيرِ مُفوَّضٍ يُرفَض، وأنّ الوكيلَ لا يكون الموكِّلَ،
وأنّ **السلطاتِ المرفوضةَ معطًى للسجلّ** يُرَدُّ من وقّع بها، وأنّ المحجوبَ
يُرَدُّ إعلانُ تمامه ويُسمّى حاجبُه، وأنّ البصمةَ تتحرّك بتبدُّل قرار.
"""

from __future__ import annotations

from datetime import date

import pytest

from algebra.decisions import (
    DECISIONS_NAMED_RESIDUALS,
    Branch,
    Decision,
    DecisionError,
    Register,
    Standing,
)

BRANCHES = (
    Branch(label="أ", effect="يتغيّر كذا", price="ويُدفع كذا"),
    Branch(label="ب", effect="يتغيّر غيرُه", price="ويُدفع غيرُه"),
)
TODAY = date(2026, 9, 22)


def _pending() -> Decision:
    return Decision(
        identifier="ق-1",
        question="أيُحسَم؟",
        blocks=("شيءٌ محجوب",),
        branches=BRANCHES,
    )


def test_the_standing_type_is_closed() -> None:
    """أربعُ منازلَ لا خامسةَ لها، ولا «مفترَض» فيها."""

    assert [standing.name for standing in Standing] == [
        "PENDING",
        "TAKEN",
        "DELEGATED",
        "DECLINED",
    ]


def test_a_branch_without_a_price_is_refused() -> None:
    """فرعٌ بلا ثمنٍ يُختار مجّانًا، فلا يُقيَّد."""

    with pytest.raises(DecisionError):
        Branch(label="أ", effect="يتغيّر", price="  ")
    with pytest.raises(DecisionError):
        Branch(label="", effect="يتغيّر", price="ثمن")


def test_a_decision_needs_two_branches_and_something_blocked() -> None:
    """فرعٌ واحدٌ إعلانٌ لا قرار، وقرارٌ لا يحجُب شيئًا لا يُقيَّد."""

    with pytest.raises(DecisionError):
        Decision("ق", "أيُحسَم؟", ("س",), (BRANCHES[0],))
    with pytest.raises(DecisionError):
        Decision("ق", "أيُحسَم؟", (), BRANCHES)
    with pytest.raises(DecisionError):
        Decision("ق", "أيُحسَم؟", ("س",), (BRANCHES[0], BRANCHES[0]))


def test_a_pending_decision_carries_no_choice() -> None:
    """معلَّقٌ بفرعٍ أو سلطةٍ أو تاريخٍ يُرفَض."""

    for extra in (
        {"chosen_branch": "أ"},
        {"authority": "المالك"},
        {"decided_on": TODAY},
    ):
        with pytest.raises(DecisionError):
            Decision("ق", "أيُحسَم؟", ("س",), BRANCHES, **extra)  # type: ignore[arg-type]


def test_a_settled_decision_needs_an_authority_and_a_date() -> None:
    """محسومٌ بلا مَن حَسَم أو بلا متى يُرفَض."""

    with pytest.raises(DecisionError):
        Decision("ق", "س؟", ("س",), BRANCHES, Standing.TAKEN, "أ", None, None, TODAY)
    with pytest.raises(DecisionError):
        Decision("ق", "س؟", ("س",), BRANCHES, Standing.TAKEN, "أ", "المالك")


def test_delegation_names_a_delegate_apart_from_the_authority() -> None:
    """مُفوَّضٌ بلا وكيلٍ يُرفَض، ووكيلٌ في غيرِ مُفوَّضٍ يُرفَض، ولا يتّحدان."""

    delegated = Decision(
        "ق", "س؟", ("س",), BRANCHES, Standing.DELEGATED, "أ", "المالك", "وكيل", TODAY
    )
    assert delegated.standing is Standing.DELEGATED
    with pytest.raises(DecisionError):
        Decision(
            "ق", "س؟", ("س",), BRANCHES, Standing.DELEGATED, "أ", "المالك", None, TODAY
        )
    with pytest.raises(DecisionError):
        Decision(
            "ق", "س؟", ("س",), BRANCHES, Standing.TAKEN, "أ", "المالك", "وكيل", TODAY
        )
    with pytest.raises(DecisionError):
        Decision(
            "ق", "س؟", ("س",), BRANCHES, Standing.DELEGATED, "أ", "هو", "هو", TODAY
        )


def test_a_refused_authority_cannot_sign_the_register() -> None:
    """السلطاتُ المرفوضةُ معطًى للسجلّ، ومن وقّع بها رُدّ."""

    signed = Decision(
        "ق", "س؟", ("س",), BRANCHES, Standing.TAKEN, "أ", "الكاتب", None, TODAY
    )
    with pytest.raises(DecisionError):
        Register((signed,), frozenset({"الكاتب"}))
    assert Register((signed,), frozenset({"غيرُه"})).pending() == ()


def test_a_blocked_item_is_not_reportable_as_done() -> None:
    """المحجوبُ يُرَدُّ عند الاستدعاء ويُسمّى حاجبُه؛ وغيرُه يمرّ."""

    register = Register((_pending(),))
    assert register.blocked_items() == ("شيءٌ محجوب",)
    assert len(register.blockers_of("شيءٌ محجوب")) == 1
    with pytest.raises(DecisionError) as caught:
        register.assert_not_reportable_as_done("شيءٌ محجوب")
    assert "ق-1" in str(caught.value)
    register.assert_not_reportable_as_done("شيءٌ آخر")


def test_the_digest_moves_when_a_decision_moves() -> None:
    """البصمةُ ثابتةٌ على الحال، متحرّكةٌ بتبدُّل المنزلة."""

    register = Register((_pending(),))
    assert len(register.digest()) == 64
    assert register.digest() == Register((_pending(),)).digest()
    settled = Decision(
        "ق-1",
        "أيُحسَم؟",
        ("شيءٌ محجوب",),
        BRANCHES,
        Standing.TAKEN,
        "أ",
        "المالك",
        None,
        TODAY,
    )
    assert Register((settled,)).digest() != register.digest()
    assert Register((settled,)).blocked_items() == ()


def test_an_empty_or_duplicated_register_is_refused() -> None:
    """سجلٌّ بلا قرارٍ أو بمعرِّفَين متكرّرَين يُرفَض، والبواقي أربعة."""

    with pytest.raises(DecisionError):
        Register(())
    with pytest.raises(DecisionError):
        Register((_pending(), _pending()))
    assert len(DECISIONS_NAMED_RESIDUALS) == 4
    assert len(set(DECISIONS_NAMED_RESIDUALS)) == 4
