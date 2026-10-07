"""ضمُّ الدَّين محسوبًا: التجانسُ مفحوصٌ، والرأسُ أعلى السلسلة، والثمنُ يهبط.

يُثبِت هذا الاختبارُ الدفترَ كاملًا على ذرّة العربيّة كما وردت، ويُثبِت معه
**حدَّين مضادَّين** لئلّا يُقرَأ الضمُّ سدادًا: أنّ التجانسَ وحدَه قد يُوسِّع
العائلةَ لا يضيّقها، وأنّ الترتيبَ لا يُشتَقّ إن بقي تعادلٌ بعد الشرطين.
"""

from __future__ import annotations

import pytest

from algebra.consolidation import (
    CONSOLIDATION_NAMED_RESIDUALS,
    ConsolidationError,
    Homomorphism,
    bits,
    chains_with_maximum,
    derive_order,
    inventory_size_from_arity,
)

# ذرّةُ العربيّة مكوّناتٍ: حاملٌ وعلامة
GENERATORS = (("حرف", "C"), ("حركةٌ قصيرة", "V"), ("سكون", ""), ("مدّ M", "V"))
CLASSES = {
    "حرفٌ بحركةٍ قصيرة": ("حرف", "حركةٌ قصيرة"),
    "حرفٌ بسكون": ("حرف", "سكون"),
    "علامةُ المدّ M": ("مدّ M",),
}
OBSERVED = {"حرفٌ بحركةٍ قصيرة": "CV", "حرفٌ بسكون": "C", "علامةُ المدّ M": "V"}
LEVELS = ("CV", "V", "C")
ARITY = {"CV": 2, "V": 1, "C": 1}
PEAK = "V"
INVENTORY = frozenset({"CV", "CVC", "CVV", "CVVC"})

STRINGS_UP_TO_TWO = 7  # ε · C · V · CC · CV · VC · VV


def test_the_assignment_is_a_homomorphism_on_every_class() -> None:
    """صورةُ كلّ صنفٍ حاصلُ وصلِ صور مكوّناته — مفحوصًا لا مُدَّعًى."""

    pi = Homomorphism(generators=GENERATORS)
    assert pi.agrees_with(CLASSES, OBSERVED)
    assert pi.image_of(("حرف", "حركةٌ قصيرة")) == "CV"
    assert pi.image_of(("حرف", "سكون")) == "C"
    assert pi.image_of(("مدّ M",)) == "V"
    assert pi.image_of(()) == ""


def test_one_dissenting_class_sinks_the_whole_claim() -> None:
    """صنفٌ واحدٌ يخالف يُسقِط الدعوى، ولا تُصلَح باستثناء."""

    pi = Homomorphism(generators=GENERATORS)
    assert not pi.agrees_with(CLASSES, {**OBSERVED, "حرفٌ بسكون": "CC"})
    with pytest.raises(ConsolidationError):
        pi.agrees_with(CLASSES, {"حرفٌ بسكون": "C"})
    with pytest.raises(ConsolidationError):
        pi.image_of(("مكوّنٌ ليس مولِّدًا",))


def test_the_homomorphism_alone_widens_the_family_and_the_constraint_narrows_it() -> (
    None
):
    """حدٌّ مضادّ: التجانسُ وحدَه **أوسعُ**، والقيدُ المقطعيُّ هو الموفِّر.

    ثلاثةُ أصنافٍ حرّةٍ على سلاسلَ ≤ ٢ = ٣٤٣ (٨٫٤٢ بت). وتجانسٌ بأربعة
    مولِّداتٍ بالحرّيّة نفسِها = ٢٬٤٠١ (١١٫٢٣ بت) — أي **أسوأ**. وبقيدِ
    «المولِّدُ مقطعٌ واحدٌ على الأكثر» = ٨١ (٦٫٣٤ بت). فالموفِّرُ القيدُ لا
    الكلمة.
    """

    free = STRINGS_UP_TO_TWO**3
    homomorphic_free = STRINGS_UP_TO_TWO**4
    homomorphic_segmental = 3**4
    assert (free, homomorphic_free, homomorphic_segmental) == (343, 2_401, 81)
    assert round(bits(free), 3) == 8.422
    assert round(bits(homomorphic_free), 3) == 11.229
    assert round(bits(homomorphic_segmental), 3) == 6.340
    assert bits(homomorphic_free) > bits(free)
    assert bits(homomorphic_segmental) < bits(free)
    assert Homomorphism(generators=GENERATORS).is_segmental
    assert not Homomorphism(generators=(("أ", "CV"),)).is_segmental


def test_the_segmental_homomorphism_identifies_the_observed_table() -> None:
    """واحدٌ من الـ٨١ يُصيب المرصودَ — فالنقلُ بلا فقدِ خبر."""

    from itertools import product

    names = tuple(name for name, _ in GENERATORS)
    hits = [
        values
        for values in product(("", "C", "V"), repeat=len(names))
        if Homomorphism(generators=tuple(zip(names, values, strict=True))).agrees_with(
            CLASSES, OBSERVED
        )
    ]
    assert len(hits) == 1
    assert hits[0] == tuple(image for _, image in GENERATORS)


def test_the_head_is_the_maximum_of_one_chain_not_a_second_stipulation() -> None:
    """المقطعُ سلسلةٌ هابطةٌ تحوي أعلاها، فلا يُفرَض رأسٌ على حدة.

    والعائلةُ ستّةُ ترتيباتٍ (٢٫٥٨٥ بت) يُصيب منها **واحد**. وقبلَه كان
    الثمنُ رأسًا يُختار من سبعِ سلاسلَ (٢٫٨٠٧ بت) زائدَ اتّجاهٍ (١ بت) =
    ٣٫٨٠٧ بت. فالضمُّ يوفّر ١٫٢٢ بت ويُلغي مصادرةً كاملة.
    """

    from itertools import permutations

    hits = [
        order
        for order in permutations(LEVELS)
        if chains_with_maximum(order) == INVENTORY
    ]
    assert hits == [("CV", "V", "C")]
    assert round(bits(6), 3) == 2.585
    assert round(bits(STRINGS_UP_TO_TWO) + 1, 3) == 3.807
    assert bits(6) < bits(STRINGS_UP_TO_TWO) + 1


def test_the_order_is_derived_from_arity_then_peak_at_no_cost() -> None:
    """الترتيبُ مشتقٌّ: الأتمُّ مكوّناتٍ أعلى، وعند التساوي حاملُ رمزِ الذروة."""

    assert derive_order(LEVELS, ARITY, PEAK) == ("CV", "V", "C")
    assert chains_with_maximum(derive_order(LEVELS, ARITY, PEAK)) == INVENTORY
    # ولو كانت الذروةُ C لانقلب الجرد — فالاشتقاقُ يعتمد على «الصائتُ ذروة»
    flipped = derive_order(LEVELS, ARITY, "C")
    assert flipped == ("CV", "C", "V")
    assert chains_with_maximum(flipped) != INVENTORY


def test_a_remaining_tie_refuses_to_be_broken_silently() -> None:
    """حدٌّ مضادّ: تعادلٌ يبقى بعد الشرطين يُرَدّ، ولا يُخترَع له كسر."""

    with pytest.raises(ConsolidationError):
        derive_order(("A", "B", "C"), {"A": 1, "B": 1, "C": 1}, "A")
    with pytest.raises(ConsolidationError):
        derive_order(("A", "B"), {"A": 1}, "A")
    with pytest.raises(ConsolidationError):
        derive_order(("A", "A"), {"A": 1}, "A")


def test_the_count_is_two_to_the_arity_and_it_predicts() -> None:
    """`2**k` تنبّؤٌ لا وصف: ذرّةٌ بثلاثة مكوّناتٍ توجب ثمانيةً."""

    assert inventory_size_from_arity(2) == len(INVENTORY) == 4
    assert [inventory_size_from_arity(k) for k in (1, 2, 3, 4)] == [2, 4, 8, 16]
    assert len(chains_with_maximum(("W", "X", "Y", "Z"))) == 8  # ‎2**(4-1)
    with pytest.raises(ConsolidationError):
        inventory_size_from_arity(0)
    with pytest.raises(ConsolidationError):
        chains_with_maximum(())


def test_the_whole_ledger_falls_and_what_remains_is_named() -> None:
    """الدفترُ: ٨٫٤٢ + ٣٫٨١ ← ٦٫٣٤ + ٢٫٥٩ ← ٦٫٣٤ + ٠٫٠٠، والباقي ثلاثُ عباراتٍ.

    ولا يُقرَأ هذا سدادًا: `A_CONSOLIDATED_DEBT_IS_STILL_A_DEBT`. الباقي
    ثلاثٌ من جنسٍ **واحد** — «الصائتُ ذروة»، و«السكونُ غيابٌ لا مقطع»،
    و«المقطعُ يهبط عن ذروته» — وكلُّها أوجهُ مقياسِ بروزٍ يُقاس من خارج النصّ.
    """

    before = bits(STRINGS_UP_TO_TWO**3) + bits(STRINGS_UP_TO_TWO) + 1
    after_homomorphism = bits(3**4) + bits(6)
    assert round(before, 3) == 12.229
    assert round(after_homomorphism, 3) == 8.925
    assert after_homomorphism < before
    # والاتّجاهُ مشتقٌّ، فيسقط نصيبُ الترتيب كلُّه
    assert derive_order(LEVELS, ARITY, PEAK)[0] == "CV"
    assert len(CONSOLIDATION_NAMED_RESIDUALS) == 5
    assert len(set(CONSOLIDATION_NAMED_RESIDUALS)) == 5
