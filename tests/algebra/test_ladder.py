"""السُّلَّمُ يُعدّ ويُوجَّه: الارتفاعُ من الأبجديّة، والاتّجاهُ من الذروة.

يُثبِت هذا الاختبارُ سلوكَ الوحدة على تجريداتٍ مصنوعة، ثمّ يُقيم التجريدَ
الوارد — ١١٣ ذرّةً على ثلاثة أصناف — فيُخرِج منه **ارتفاعًا مقروءًا لا
مختارًا** (n = ٢)، و**اتّجاهًا مشتقًّا لا مُصادَرًا** (رمزُ الذروة V أعلى)،
والجردَ الأربعةَ لزومًا عنهما. ويُثبِت أنّ الناقضَ قائم: درجةٌ زائدةٌ تُوجب
جردًا من ثمانية، وصنفٌ بلا صورةٍ لا يرفع السُّلَّمَ وإن كبر عددُه.
"""

from __future__ import annotations

import pytest

from algebra.ladder import (
    LADDER_NAMED_RESIDUALS,
    Abstraction,
    AtomClass,
    LadderError,
)

# التجريدُ الوارد: Σ = ٢٨ حرفًا × ٤ حالاتٍ ∪ {M} = ١١٣ ذرّة
VOWELLED = AtomClass(name="حرفٌ بحركةٍ قصيرة", image="CV", size=28 * 3)
SILENT = AtomClass(name="حرفٌ بسكون", image="C", size=28)
LENGTHENER = AtomClass(name="علامةُ المدّ M", image="V", size=1)
PI = Abstraction(classes=(VOWELLED, SILENT, LENGTHENER), head=VOWELLED.name)

# الحرفُ العاطلُ من كلّ علامة: حالةٌ خامسةٌ خارجَ Σ، وهي أسماءُ الحروف في الفواتح
BARE = AtomClass(name="حرفٌ بلا علامةٍ في الرسم", image="", size=28)

INVENTORY = frozenset({"CV", "CVC", "CVV", "CVVC"})


def test_the_alphabet_counts_come_out_of_the_classes() -> None:
    """١١٣ ذرّةً مجموعَ الأصناف، و٨٤ صدرًا و٢٨ عَجُزًا وسعةً ٢٣٥٢."""

    assert PI.atom_count == 28 * 4 + 1 == 113
    assert VOWELLED.size == 84
    assert SILENT.size == 28
    assert VOWELLED.size * SILENT.size == 2_352


def test_the_height_is_read_off_the_alphabet_not_chosen() -> None:
    """`n` عددُ الأصناف التي صورتُها رمزٌ واحد: صنفان، فالارتفاعُ اثنان."""

    assert {atom.name for atom in PI.rungs} == {SILENT.name, LENGTHENER.name}
    assert PI.height == 2
    assert PI.predicted_size == 4


def test_the_direction_is_the_peaks_own_symbol_so_no_bit_is_spent() -> None:
    """رمزُ الذروة V، فهو أعلى الدرجتين — والاتّجاهُ مشتقٌّ لا مُصادَر."""

    assert PI.head_image == "CV"
    assert PI.peak_symbol == "V"
    assert PI.ladder() == ("V", "C")


def test_the_inventory_follows_from_the_height_and_the_direction() -> None:
    """الجردُ يلزم عن السُّلَّم وحدَه، وعددُه `2**n` لا استقراءً."""

    assert PI.tails() == frozenset({"", "V", "C", "VC"})
    assert PI.inventory() == INVENTORY
    assert len(PI.inventory()) == PI.predicted_size == 4


def test_flipping_the_ladder_gives_a_different_inventory() -> None:
    """لو كان السكونُ أعلى لخرج جردٌ آخر، فالاتّجاهُ ليس اصطلاحَ كتابة."""

    flipped = Abstraction(classes=PI.classes, head=PI.head, declared_order=("C", "V"))
    assert flipped.inventory() != INVENTORY
    assert "CVCV" in flipped.inventory()
    assert "CVVC" not in flipped.inventory()
    assert len(flipped.inventory()) == 4


def test_an_extra_rung_must_double_the_inventory_wherever_it_sits() -> None:
    """الناقضُ قائمٌ: درجةٌ ثالثةٌ تُوجب ثمانيةً — في المواضع الثلاثة كلِّها.

    وموضعُها مُعلَنٌ لا مُشتَقّ (فالسُّلَّمُ بثلاثٍ لا يرتّب نفسَه)، والمُدَّعى
    لا يتعلّق بالموضع: العددُ `2**n` أينما وُضِعت. فثباتُ الأربعة مع درجةٍ
    ثالثةٍ نقضٌ للقول لا تقييدٌ له.
    """

    for position in (0, 1, 2):
        widened = PI.with_extra_rung("درجةٌ مفترَضةٌ ثالثة", "X", position=position)
        assert widened.height == 3
        assert widened.predicted_size == 8
        assert len(widened.inventory()) == 8
    bottom = PI.with_extra_rung("درجةٌ مفترَضةٌ ثالثة", "X")
    assert bottom.ladder() == ("V", "C", "X")
    assert INVENTORY < bottom.inventory()
    with pytest.raises(LadderError):
        PI.with_extra_rung("خارجَ السُّلَّم", "X", position=3)


def test_a_class_without_an_image_raises_nothing_however_many_it_holds() -> None:
    """الحرفُ العاطلُ ٢٨ ذرّةً، ولا يرفع السُّلَّمَ ولا يدخل الجرد."""

    widened = Abstraction(classes=(*PI.classes, BARE), head=PI.head)
    assert widened.atom_count == 113 + 28 == 141
    assert widened.imageless == (BARE,)
    assert widened.height == PI.height == 2
    assert widened.inventory() == INVENTORY


def test_three_rungs_will_not_order_themselves() -> None:
    """بثلاث درجاتٍ يبقى الترتيبُ مصادرةً تُعلَن، ولا يُخترَع صمتًا."""

    unordered = Abstraction(
        classes=(*PI.classes, AtomClass(name="درجةٌ ثالثة", image="X")),
        head=PI.head,
    )
    assert unordered.height == 3
    with pytest.raises(LadderError):
        unordered.ladder()
    ordered = Abstraction(
        classes=unordered.classes, head=PI.head, declared_order=("V", "X", "C")
    )
    assert len(ordered.inventory()) == 8
    assert "CVVXC" in ordered.inventory()


def test_what_does_not_yield_a_ladder_is_refused() -> None:
    """حاملٌ برمزٍ واحد، وأسماءٌ مكرّرة، وحاملٌ غائب، وترتيبٌ ناقص — كلُّها تُرَدّ."""

    with pytest.raises(LadderError):
        Abstraction(classes=(AtomClass("درجة", "V"),), head="درجة")
    with pytest.raises(LadderError):
        Abstraction(classes=PI.classes, head="ليس فيها")
    with pytest.raises(LadderError):
        Abstraction(classes=(VOWELLED, SILENT, SILENT), head=VOWELLED.name)
    with pytest.raises(LadderError):
        Abstraction(classes=PI.classes, head=PI.head, declared_order=("V",))
    with pytest.raises(LadderError):
        PI.with_extra_rung("مكرّرة", "C")
    with pytest.raises(LadderError):
        AtomClass(name="بلا حجم", image="C", size=0)
    with pytest.raises(LadderError):
        Abstraction(classes=(), head="لا شيء")


def test_a_peak_that_is_not_a_rung_will_not_orient_the_ladder() -> None:
    """إن لم يكن رمزُ الذروة درجةً فلا يُشتَقّ الاتّجاهُ، ويُعلَن أو يُرَدّ."""

    stranger = Abstraction(
        classes=(
            AtomClass("حامل", "AB"),
            AtomClass("أولى", "C"),
            AtomClass("ثانية", "D"),
        ),
        head="حامل",
    )
    assert stranger.peak_symbol == "B"
    with pytest.raises(LadderError):
        stranger.ladder()


def test_the_named_residuals_are_five_and_distinct() -> None:
    """البواقي المُسمّاةُ خمسٌ، ولا تكرارَ فيها."""

    assert len(LADDER_NAMED_RESIDUALS) == 5
    assert len(set(LADDER_NAMED_RESIDUALS)) == 5
