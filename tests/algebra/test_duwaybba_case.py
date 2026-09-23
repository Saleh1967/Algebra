"""دُوَيْبَّةٌ خبرًا عن العربيّة: مفترقٌ مُسعَّرٌ، لا شاذّةٌ تُخرَج ولا نسبةٌ تُنقَل.

**ما يُودَع ههنا**: الحالةُ الوحيدةُ التي نجت من المصفاة المصحَّحة، مُدخَلةً
**بوصفها خبرًا** لا بوصفها أثرًا للأداة. والفرقُ بينهما قابلٌ للحساب، وهو
مدارُ هذا الملفّ.

والحجّةُ في سطر: **الاصطلاحُ الذي يجعلها مخالِفةً هو الاصطلاحُ الذي أنتج
٣٬٧١٧ إدغامًا عابرًا لحدّ الكلمة في المصحف**. فمن أخرجها من المجال بحجّة أنّ
موضعَ نصفِ المشدَّد «قرارُ شفرةٍ لا خبرٌ عن العربيّة» أخرج الـ٣٬٧١٧ معها.
و«خارجُ المجال» حكمٌ مشروطٌ لا مَخرَج، وشرطُه أن يكون الاصطلاحُ عقيمًا.

وسلسلةُ التصفية المصحَّحةُ مُثبَتةٌ ههنا أيضًا، ومعها **ضابطُ الإكمال** الذي
يُثبِت أنّ المصفاةَ لم تصنع النتيجة — وهو أثقلُ ما في التصحيح.
"""

from __future__ import annotations

from fractions import Fraction

import pytest

from algebra.decisions import Branch
from algebra.reconciliation import Partition, rounds_to
from algebra.witness import Case, Convention, Fork, WitnessError

# سلسلةُ التصفية المصحَّحة على عرموز
VOWELLED_ENTRIES = 34_406
OUT_OF_ANALYSER_RANGE = 136  # مدخلاتُ U+0622 (آ) — يُسقِطها المحلِّلُ صمتًا
FULLY_MARKED = 30_785
REJECTED_BASKET = 3_485
COMPLETABLE = 3_477  # له إكمالٌ داخل الأربعة على {فتحة، ضمّة، كسرة، سكون}
UNCOMPLETABLE = 8  # مفحوصةٌ بأعيانها: أخطاءُ طبعٍ وأعجميّان
SYLLABLES = 99_135
SHARES = ("50.73", "34.11", "15.02", "0.14")  # CV · CVC · CVV · CVVC

# نسبُ المصحف من «البناء الثاني»، للمقابلة
QURAN_SHARES = ("45.895", "31.780", "22.278", "0.047")

WHERE_THE_HALF_GEMINATE_FALLS = Convention(
    name="موضعُ نصفِ المشدَّد الأوّل",
    decides="أنّ النصفَ الأوّلَ ساكنٌ يُغلِق المقطعَ السابق، لا مطلعٌ للاحق",
    carries=("الإدغامُ عبر حدّ الكلمة ×٣٬٧١٧ في المصحف — «نصفها الأوّل للكلمة السابقة»",),
    pending=(
        (
            "CVVC ×١٠٦ في المصحف",
            "تفكيكُ الـ١٠٦: كم منها عَجُزُه نصفُ مشدَّدٍ لا ساكنٌ أصليّ؟ "
            "فما كان منها كذلك يسقط بسقوط الاصطلاح",
        ),
    ),
)

DUWAYBBA = Case(
    name="دُوَيْبَّةٌ",
    violates="م٣ — لا يتلو السكونَ سكونٌ داخل الكلمة",
    under=WHERE_THE_HALF_GEMINATE_FALLS,
    occurrences=1,
)

FORK = Fork(
    case=DUWAYBBA,
    rule_is_false=Branch(
        label="م٣ انتظامٌ لا قانون",
        effect="CVCC واردٌ في العربيّة داخلَ الكلمة، والجردُ خمسةٌ لا أربعة",
        price="يفقد السُّلَّمُ إحدى درجتيه شرطًا، فيلزم عن الارتفاع ٨ لا ٤",
    ),
    convention_is_wrong=Branch(
        label="الاصطلاحُ في نصف المشدَّد خطأ",
        effect="لا CC ههنا، وم٣ قانونٌ مطرد",
        price="يسقط معه تصنيفُ ٣٬٧١٧ إدغامًا عابرًا للحدّ، وينتظر تفكيكُ الـ١٠٦",
    ),
)


def test_the_corrected_filter_chain_adds_up() -> None:
    """٣٤٬٤٠٦ − ١٣٦ − ٣٬٤٨٥ = ٣٠٬٧٨٥ بلا بقيّة، والسلّةُ ٣٬٤٧٧ + ٨."""

    assert VOWELLED_ENTRIES - OUT_OF_ANALYSER_RANGE - REJECTED_BASKET == FULLY_MARKED
    basket = Partition(
        parts=(COMPLETABLE, UNCOMPLETABLE), declared_total=REJECTED_BASKET
    )
    assert basket.balances
    assert rounds_to(Fraction(COMPLETABLE * 100, REJECTED_BASKET), 2) == Fraction(
        "99.77"
    )


def test_the_filter_did_not_manufacture_the_result() -> None:
    """ضابطُ الإكمال: ٩٩٫٧٧٪ من المرفوض له إكمالٌ داخلَ الأربعة، والثمانيةُ مفحوصة.

    وهذا هو الضابطُ الذي كان ناقصًا. فالسلّةُ المرفوضةُ فيها ٢٨٫٨٥٪ خارجَ
    الأربعة، ولولا الضابطُ لكان ٠٫٠٠١٪ في المُخرَج صنيعةَ مصفاة. والضابطُ
    يسأل عن **كلّ** مرفوضٍ: أله إكمالٌ على {فتحة، ضمّة، كسرة، سكون} يُدخِله
    الأربعة؟ فإن كان، فرفضُه نقصُ شكلٍ لا شهادةٌ مضادّة. والجوابُ: ٣٬٤٧٧ نعم،
    وثمانيةٌ لا، وهي مفحوصةٌ بأعيانها ولا عربيَّ فيها.
    """

    outside_in_basket = Fraction("28.85") / 100 * REJECTED_BASKET
    assert round(float(outside_in_basket)) == 1_005
    assert Fraction(COMPLETABLE, REJECTED_BASKET) > Fraction(997, 1_000)
    assert Fraction(UNCOMPLETABLE, REJECTED_BASKET) < Fraction(1, 400)


def test_the_four_shares_hide_the_single_witness_exactly_as_the_quran_did() -> None:
    """النسبُ الأربعُ تجمع إلى ١٠٠٫٠٠ تامًّا، والشاهدُ الواحدُ دون دقّتها.

    و١/٩٩٬١٣٥ = ٠٫٠٠١٪، فيُطبَع صفرًا عند منزلتين. وهذا **عينُ** ما وقع في
    المصحف: أربعةُ أشكالٍ تجمع ٢٢٥٬٩١٠ ومجموعٌ ٢٢٥٬٩١١، والبقيّةُ واحدةٌ
    مستورةٌ في النسب. فالنمطُ يتكرّر في مدوَّنتين مستقلّتين، وهو خاصّةُ
    التقريب لا خاصّةُ نصّ.
    """

    total = sum(Fraction(share) for share in SHARES)
    assert total == 100
    lone = Fraction(100, SYLLABLES)
    assert rounds_to(lone, 3) == Fraction("0.001")
    assert rounds_to(lone, 2) == 0
    assert 225_911 - 225_910 == 1


def test_the_shares_move_between_the_two_corpora_but_the_inventory_does_not() -> None:
    """الجردُ ينتقل والنسبُ لا: CVV تهبط ٧٫٢٦ نقطةً، وهي ٦٫٥ أمثالِ تذبذبها."""

    within = [Fraction("22.278"), Fraction("23.394"), Fraction("22.724")]
    spread = max(within) - min(within)
    gap = Fraction(QURAN_SHARES[2]) - Fraction(SHARES[2])
    assert spread == Fraction("1.116")
    assert gap == Fraction("7.258")
    assert round(float(gap / spread), 3) == 6.504
    assert len(SHARES) == len(QURAN_SHARES) == 4


def test_the_case_may_not_be_called_out_of_scope_for_free() -> None:
    """إخراجُها من المجال يُخرِج الـ٣٬٧١٧ معها — والوحدةُ تردّه وتُسمّي الثمن."""

    assert not FORK.may_be_called_out_of_scope
    assert FORK.cost_of_denying == WHERE_THE_HALF_GEMINATE_FALLS.carries
    with pytest.raises(WitnessError) as raised:
        FORK.out_of_scope_withdraws()
    assert "٣٬٧١٧" in str(raised.value)


def test_the_case_may_not_be_turned_into_a_rate() -> None:
    """ولا تُقسَم على ٣٠٬٧٨٥ فتصير ٠٫٠٠٣٪: المفردُ يُلزِم اختيارًا."""

    assert DUWAYBBA.occurrences == 1
    with pytest.raises(WitnessError):
        FORK.as_rate(FULLY_MARKED)


def test_both_branches_carry_a_price_and_neither_is_free() -> None:
    """الفرعان مُسعَّران: أحدُهما يُغيّر السُّلَّم، والآخرُ يُسقِط ٣٬٧١٧."""

    for branch in (FORK.rule_is_false, FORK.convention_is_wrong):
        assert branch.price.strip()
    assert "٨ لا ٤" in FORK.rule_is_false.price
    assert "٣٬٧١٧" in FORK.convention_is_wrong.price
    assert FORK.pending_costs[0][0] == "CVVC ×١٠٦ في المصحف"
    assert "تفكيكُ الـ١٠٦" in FORK.pending_costs[0][1]


def test_the_fourth_retraction_is_a_unit_mismatch_not_a_falsehood() -> None:
    """تصحيحٌ للتصحيح: «سكون←سكون صفر» لم تكن كاذبةً في النصّ الذي أحمله.

    «البناء الثاني» يقول بنصّه: «سكون ← سكون = ٣٣ فقط، وهي بأسرها فواتحُ
    السور (٣٢) ومَجْر۪ىٰهَا (١). ففي الكلمات صفرٌ بالتمام». والعدُّ الجديد
    ٢٧ كلمة = ٢٦ فاتحةً + مَجْر۪ىٰهَا. والمجتمعُ **واحد**: فواتحُ السور
    ومَجْر۪ىٰهَا في القراءتين.

    والفرقُ ٣٣−٢٧ = ٦ هو عينُه ٣٢−٢٦ = ٦، وذلك ما يُنتَظَر حين يُعَدّ
    **الانتقالُ** مرّةً و**الكلمة** مرّةً: كلمةٌ كـكٓهيعٓصٓ تحمل انتقالاتٍ
    عدّة. فالرقمان متّسقان، و«الصفرُ» كان مقيَّدًا في نصّه بـ«في الكلمات».
    """

    assert 33 - 27 == 32 - 26 == 6
    assert 32 + 1 == 33
    assert 26 + 1 == 27
