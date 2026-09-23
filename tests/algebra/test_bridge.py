"""الجسرُ يوازن أو يُرَدّ، والسُّلَّمُ يفصل «مبنيًّا» عن «مبلوغ».

يُثبِت هذا الاختبارُ أربعةَ أشياءَ حاملة: أنّ عبورًا لا يوازن **يُرَدّ في
الإنشاء** لا يُلاحَظ بعدَه؛ وأنّ المردودَ يُسمّى سببُه ويُعَدّ به؛ وأنّ جسرًا
غيرَ مبنيٍّ يُسمّي أوراكلَه؛ وأنّ السيرَ من الأسفل يقف عند أوّل فجوةٍ مهما
صحّ ما فوقها.
"""

from __future__ import annotations

import pytest

from algebra.bridge import (
    BRIDGE_NAMED_RESIDUALS,
    Bridge,
    BridgeError,
    Crossing,
    Ladder,
    Level,
)

BYTES = Level("الشيفرة")
CODEPOINTS = Level("اليونيكود")
SPELLING = Level("الإملاء", ("حامل", "حركة", "سكون", "شدّة"))
MORPHOLOGY = Level("الاشتقاق")
CLASS = Level("اسمٌ وفعلٌ وحرف", ("اسم", "فعل", "حرف"))


def _ladder() -> Ladder:
    return Ladder(
        bridges=(
            Bridge("فكُّ الترميز", BYTES, CODEPOINTS),
            Bridge("التجزئة", CODEPOINTS, SPELLING),
            Bridge("الاشتقاق", SPELLING, MORPHOLOGY, oracle="محلِّلٌ صرفيٌّ مُعلَن"),
            Bridge("القسمة", MORPHOLOGY, CLASS),
        )
    )


def test_a_crossing_that_does_not_balance_is_refused_at_construction() -> None:
    """١٣٦ مدخلًا تختفي: يُرَدّ العبورُ كلُّه، ويُسمّى الفرقُ في الرسالة."""

    with pytest.raises(BridgeError) as raised:
        Crossing(bridge="التجزئة", given=34_406, mapped=34_270)
    assert "136" in str(raised.value)
    balanced = Crossing(
        bridge="التجزئة",
        given=34_406,
        mapped=34_270,
        refused=(("محرفٌ خارجَ جرد المحلِّل", 136),),
    )
    assert balanced.balances
    assert balanced.refused_total == 136


def test_a_refusal_carries_a_reason_and_reasons_do_not_repeat() -> None:
    """المردودُ يُسمّى، ولا يُجمَع صنفان في اسمٍ واحد."""

    with pytest.raises(BridgeError):
        Crossing(bridge="ج", given=1, mapped=0, refused=(("  ", 1),))
    with pytest.raises(BridgeError):
        Crossing(bridge="ج", given=2, mapped=0, refused=(("س", 1), ("س", 1)))
    with pytest.raises(BridgeError):
        Crossing(bridge="ج", given=1, mapped=-1, refused=(("س", 2),))
    assert Crossing(bridge="ج", given=0, mapped=0).balances


def test_an_unbuilt_bridge_names_its_oracle() -> None:
    """أوراكلٌ فارغٌ يُرَدّ، والمبنيُّ ما لا ينتظر معطًى من خارج."""

    assert Bridge("مبنيّ", BYTES, CODEPOINTS).is_built
    assert not Bridge("غير", BYTES, CODEPOINTS, oracle="معجم").is_built
    with pytest.raises(BridgeError):
        Bridge("غير", BYTES, CODEPOINTS, oracle="   ")


def test_a_gap_between_two_bridges_is_refused() -> None:
    """الجسورُ تتّصل طرفًا بطرف، وإلّا فليست سُلَّمًا."""

    with pytest.raises(BridgeError) as raised:
        Ladder(
            bridges=(
                Bridge("أ", BYTES, CODEPOINTS),
                Bridge("ب", SPELLING, MORPHOLOGY),
            )
        )
    assert "فجوة" in str(raised.value)
    with pytest.raises(BridgeError):
        Ladder(bridges=())


def test_built_is_not_reached_and_the_difference_is_printed() -> None:
    """السيرُ يقف عند أوّل فجوة، وما فوقها مبنيٌّ غيرُ مبلوغ."""

    ladder = _ladder()
    assert len(ladder.built) == 3
    assert len(ladder.unbuilt) == 1
    assert ladder.oracles_required() == ("محلِّلٌ صرفيٌّ مُعلَن",)
    assert not ladder.is_traversable
    assert ladder.first_gap is not None and ladder.first_gap.name == "الاشتقاق"
    assert [level.name for level in ladder.reachable_levels()] == [
        "الشيفرة",
        "اليونيكود",
        "الإملاء",
    ]
    assert [bridge.name for bridge in ladder.built_but_unreached()] == ["القسمة"]


def test_a_level_is_closed_only_by_a_listed_inventory() -> None:
    """الانغلاقُ بجردٍ مسرود، والخالي ليس انغلاقًا، والمفتوحُ لا حجمَ له."""

    assert SPELLING.is_closed and SPELLING.size == 4
    assert not BYTES.is_closed
    with pytest.raises(BridgeError):
        BYTES.size
    with pytest.raises(BridgeError):
        Level("مدّعًى", ())
    with pytest.raises(BridgeError):
        Level("مكرّر", ("أ", "أ"))
    with pytest.raises(BridgeError):
        Level("  ")


def test_the_named_residuals_are_five_and_distinct() -> None:
    """البواقي المُسمّاةُ خمسٌ، ولا تكرارَ فيها."""

    assert len(BRIDGE_NAMED_RESIDUALS) == 5
    assert len(set(BRIDGE_NAMED_RESIDUALS)) == 5
