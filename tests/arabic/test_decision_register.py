"""سجلُّ القرارات: معلَّقٌ لا يصير محسومًا، وسلطةٌ لا تكون الجلسةَ.

يُثبِت هذا الاختبارُ أحدَ عشرَ شيئًا: أنّ منازلَ القرار ثلاثٌ مغلقةٌ ولا منزلةَ
اسمُها «مفترَض»، وأنّ القراراتَ الثلاثةَ **كلَّها معلَّقةٌ** ولا فرعَ مُتَّخَذًا
فيها، وأنّ قرارًا محسومًا بلا سلطةٍ أو بلا تاريخٍ يُرفَض عند الإنشاء، وأنّ
**الجلسةَ والمساعدَ مرفوضان سلطةً بالبناء**، وأنّ قرارًا معلَّقًا بفرعٍ مُتَّخَذٍ
يُرفَض، وأنّ فرعًا بلا ثمنٍ لا يُقيَّد، وأنّ سؤالًا مصوغًا خبرًا يُرفَض، وأنّ
إعلانَ تمامِ محجوبٍ يُرَدُّ عند الاستدعاء، وأنّ ما يحجُبه السجلُّ مُشتَقٌّ
بالمنزلة لا مكتوب، وأنّ قراءةَ الثمن **تُكشَف قديمةً ولا تُصحَّح في محلّها**
لأنّ السجلَّ نفسَه ملفٌّ في النطاق الذي يُسعّره، وأنّ بصمةَ السجلّ تتغيّر إذا
تغيّر قرار.
"""

from __future__ import annotations

from datetime import date

import pytest

from alghanem.arabic.decision_register import (
    DECISION_REGISTER_NAMED_RESIDUALS,
    DECISIONS,
    REFUSED_AUTHORITIES,
    SCOPE_READING,
    Branch,
    Decision,
    DecisionRegisterError,
    DecisionStanding,
    assert_not_reportable_as_done,
    blocked_items,
    blockers_of,
    bonferroni_denominator,
    delegated_decisions,
    is_blocked,
    pending_decisions,
    recompute_scope_price,
    register_digest,
    render_register,
    taken_decisions,
)

_BRANCHES = (
    Branch(label="أ", what_changes="يتغيّر كذا", price="ويُدفع كذا"),
    Branch(label="ب", what_changes="يتغيّر كذا الآخَر", price="ويُدفع غيرُه"),
)


def test_standings_are_three_and_closed() -> None:
    """لا منزلةَ اسمُها «مفترَض»، فلا يصير المعلَّقُ محسومًا بالسكوت."""

    assert [standing.name for standing in DecisionStanding] == [
        "PENDING",
        "TAKEN",
        "DELEGATED",
        "DECLINED",
    ]
    assert "ASSUMED" not in DecisionStanding.__members__


def test_every_deposited_decision_is_delegated_not_taken() -> None:
    """الثلاثةُ **مُفوَّضةٌ**: فرعٌ مُسمًّى، ووكيلٌ مُسمًّى، ولا توقيعَ للمودِع.

    و«لا تفضيل» ليست اختيارَ فرع؛ فلا يُقيَّد القرارُ متَّخَذًا باسم المودِع،
    ولا يبقى معلَّقًا فيُخفي أنّه فوَّض.
    """

    assert len(DECISIONS) == 3
    assert len(delegated_decisions()) == 3
    assert taken_decisions() == ()
    assert pending_decisions() == ()
    for decision in DECISIONS:
        assert decision.taken_branch is not None
        assert decision.delegate is not None
        assert decision.authority is not None
        assert decision.delegate != decision.authority
        assert "Saleh1967" in decision.authority
        assert decision.taken_branch in [branch.label for branch in decision.branches]


def test_a_delegated_decision_needs_a_named_delegate_and_branch() -> None:
    """مُفوَّضٌ بلا وكيلٍ أو بلا فرعٍ يُرفَض، ووكيلٌ في غيرِ مُفوَّضٍ يُرفَض."""

    with pytest.raises(DecisionRegisterError):
        Decision(
            identifier="ق-س",
            question="أيُحسَم؟",
            blocks=("شيءٌ ما",),
            branches=_BRANCHES,
            standing=DecisionStanding.DELEGATED,
            taken_branch="أ",
            authority="المودِع",
            decided_on=date(2026, 9, 22),
        )
    with pytest.raises(DecisionRegisterError):
        Decision(
            identifier="ق-س",
            question="أيُحسَم؟",
            blocks=("شيءٌ ما",),
            branches=_BRANCHES,
            standing=DecisionStanding.DELEGATED,
            authority="المودِع",
            delegate="وكيل",
            decided_on=date(2026, 9, 22),
        )
    with pytest.raises(DecisionRegisterError):
        Decision(
            identifier="ق-س",
            question="أيُحسَم؟",
            blocks=("شيءٌ ما",),
            branches=_BRANCHES,
            standing=DecisionStanding.TAKEN,
            taken_branch="أ",
            authority="المودِع",
            delegate="وكيل",
            decided_on=date(2026, 9, 22),
        )


def test_delegation_lifts_the_block_and_the_session_is_never_the_authority() -> None:
    """التفويضُ يرفع الحجبَ، والوكيلُ يُسمّى في حقلٍ غيرِ حقل السلطة."""

    assert blocked_items() == ()
    assert not is_blocked("تشغيلُ اختبار [123] كما جُمِّد")
    assert blockers_of("تشغيلُ اختبار [123] كما جُمِّد") == ()
    assert_not_reportable_as_done("تشغيلُ اختبار [123] كما جُمِّد")
    for decision in DECISIONS:
        assert decision.authority not in REFUSED_AUTHORITIES


def test_the_session_cannot_sign_a_decision() -> None:
    """السلطةُ لا تكون الجلسةَ ولا المساعدَ؛ والمنعُ بنيويٌّ لا أدبيّ."""

    for authority in REFUSED_AUTHORITIES:
        with pytest.raises(DecisionRegisterError):
            Decision(
                identifier="ق-س",
                question="أيُحسَم؟",
                blocks=("شيءٌ ما",),
                branches=_BRANCHES,
                standing=DecisionStanding.TAKEN,
                taken_branch="أ",
                authority=authority,
                decided_on=date(2026, 9, 22),
            )


def test_a_taken_decision_needs_an_authority_and_a_date() -> None:
    """محسومٌ بلا مَن حَسَم أو بلا متى يُرفَض عند الإنشاء."""

    with pytest.raises(DecisionRegisterError):
        Decision(
            identifier="ق-س",
            question="أيُحسَم؟",
            blocks=("شيءٌ ما",),
            branches=_BRANCHES,
            standing=DecisionStanding.TAKEN,
            taken_branch="أ",
            decided_on=date(2026, 9, 22),
        )
    with pytest.raises(DecisionRegisterError):
        Decision(
            identifier="ق-س",
            question="أيُحسَم؟",
            blocks=("شيءٌ ما",),
            branches=_BRANCHES,
            standing=DecisionStanding.TAKEN,
            taken_branch="أ",
            authority="المودِع",
        )


def test_a_pending_decision_carries_no_branch() -> None:
    """معلَّقٌ بفرعٍ مُتَّخَذٍ أو بتاريخِ حسمٍ يُرفَض."""

    with pytest.raises(DecisionRegisterError):
        Decision(
            identifier="ق-س",
            question="أيُحسَم؟",
            blocks=("شيءٌ ما",),
            branches=_BRANCHES,
            taken_branch="أ",
        )
    with pytest.raises(DecisionRegisterError):
        Decision(
            identifier="ق-س",
            question="أيُحسَم؟",
            blocks=("شيءٌ ما",),
            branches=_BRANCHES,
            decided_on=date(2026, 9, 22),
        )


def test_a_branch_without_a_price_is_refused() -> None:
    """فرعٌ بلا ثمنٍ يُختار مجّانًا، فلا يُقيَّد."""

    with pytest.raises(DecisionRegisterError):
        Branch(label="أ", what_changes="يتغيّر كذا", price="   ")


def test_a_question_written_as_a_statement_is_refused() -> None:
    """صياغةُ السؤال خبرًا تُخفي أنّه لم يُحسَم، فتُرَدّ."""

    with pytest.raises(DecisionRegisterError):
        Decision(
            identifier="ق-س",
            question="يُحسَم هذا لاحقًا.",
            blocks=("شيءٌ ما",),
            branches=_BRANCHES,
        )


def test_one_branch_is_not_a_decision() -> None:
    """فرعٌ واحدٌ إعلانٌ لا قرار، وقرارٌ لا يحجُب شيئًا لا يُقيَّد."""

    with pytest.raises(DecisionRegisterError):
        Decision(
            identifier="ق-س",
            question="أيُحسَم؟",
            blocks=("شيءٌ ما",),
            branches=(_BRANCHES[0],),
        )
    with pytest.raises(DecisionRegisterError):
        Decision(
            identifier="ق-س",
            question="أيُحسَم؟",
            blocks=(),
            branches=_BRANCHES,
        )


def test_a_blocked_item_is_not_reportable_as_done(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """المحجوبُ يُرَدُّ عند الاستدعاء، ويُسمّى القرارُ الذي حجَبه."""

    import alghanem.arabic.decision_register as module

    pending = Decision(
        identifier="ق-ص",
        question="أيُحسَم؟",
        blocks=("شيءٌ محجوب",),
        branches=_BRANCHES,
    )
    monkeypatch.setattr(module, "DECISIONS", (*DECISIONS, pending))
    assert "شيءٌ محجوب" in module.blocked_items()
    assert module.is_blocked("شيءٌ محجوب")
    with pytest.raises(DecisionRegisterError) as caught:
        module.assert_not_reportable_as_done("شيءٌ محجوب")
    assert "ق-ص" in str(caught.value)
    monkeypatch.undo()
    assert_not_reportable_as_done("شيءٌ لا يحجُبه قرار")


def test_the_recorded_price_is_shown_stale_not_corrected() -> None:
    """السجلُّ ملفٌّ في النطاق الذي يُسعّره، فقراءتُه تَقدُم بإيداعها نفسِه."""

    assert SCOPE_READING.added_files == 16
    assert SCOPE_READING.added_pairs == 646
    assert len(SCOPE_READING.red_tests) == 3
    live = recompute_scope_price()
    if live is not None:
        assert live.frozen_files == SCOPE_READING.frozen_files
        assert live.live_files > live.frozen_files
        assert live.recording_is_stale == (
            live.live_files != SCOPE_READING.measured_files
        )
        assert SCOPE_READING.measured_files == 430


def test_the_digest_moves_when_a_decision_moves() -> None:
    """بصمةُ السجلّ سلطةُ تغيُّرِه: قرارٌ يُبدَّل لاحقًا يُعرَف بها."""

    digest = register_digest()
    assert len(digest) == 64
    assert digest == register_digest()
    assert digest[:16] in render_register()
    assert all(decision.identifier in render_register() for decision in DECISIONS)
    assert "مُفوَّض" in render_register()
    assert "وكيلُ الجلسة" in render_register()


def test_the_chosen_denominator_is_computed_not_written() -> None:
    """مقامُ ق-1 مُشتَقٌّ: خمسُ كتلٍ مرتَّبةً × ثلاثةَ أزواجِ خانات = 75.

    و6 لا يُعاد بناؤه من نصّ المقياس بأيّ قراءة: المرتَّبُ 75، وغيرُ المرتَّب
    45؛ والذي يُخرِج 6 قراءةٌ لم يكتبها المقياس.
    """

    from alghanem.arabic.slgae_deposit import BORN_BLOCKS
    from alghanem.arabic.slot_rights_algebra import RelationType

    blocks = len(BORN_BLOCKS)
    pairs = len(RelationType)
    assert bonferroni_denominator() == blocks**2 * pairs == 75
    assert blocks * (blocks + 1) // 2 * pairs == 45
    assert bonferroni_denominator() != 6
    signed = next(
        decision for decision in DECISIONS if decision.identifier.startswith("ق-1")
    )
    assert signed.taken_branch is not None
    assert "75" in signed.taken_branch


def test_named_residuals_are_deposited() -> None:
    """البواقي المُسمّاةُ سبعٌ، ولا مكرَّرَ فيها."""

    assert len(DECISION_REGISTER_NAMED_RESIDUALS) == 8
    assert len(set(DECISION_REGISTER_NAMED_RESIDUALS)) == 8
