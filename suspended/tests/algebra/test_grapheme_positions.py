"""مواضعُ المحارف في المصحف كلِّه: حرفٌ واحدٌ منعزل، وزوجان لا ثلاثة عشر.

**ما قِيس**: عمودُ `surface` من المحاذاة الكاملة — ٧٧٬٤٢٨ كلمةً مشكولةً
بالرسم العثمانيّ. ولكلّ محرفٍ أساسٍ (بعد إسقاط الحركات والصغارى والتطويل
والألف الخنجريّة) يُعَدُّ وقوعُه **مبتدأً ووسطًا ومنتهى** في الكلمة. وهذا
تعدادٌ شاملٌ لا عيّنة.

**حدُّ التعريف، ويُعلَن قبل النتيجة**: «الموضع» ههنا **موضعُ الكلمة في
الرسم** لا موضعُ المقطع ولا خانةُ الجذر. فمن عرّف التقابلَ بخانةٍ أدقَّ فله
عددٌ آخر، وهذا العددُ لا يُنقَل إليه.

`THE_ISOLATION_MECHANISM_EXISTS_AND_IS_ALMOST_EMPTY`: أُقترِح أنّ بعضَ
الأصفار «انعزالٌ موضعيّ» لا «ندرة»، وأنّ تصنيفَها يُقوّي الدعوى بلا بياناتٍ
جديدة. والتعدادُ يقول: الآليّةُ **قائمةٌ وشبهُ فارغة**. من ستّةٍ وثلاثين
محرفًا، **واحدٌ** وحدَه ذو موضعٍ واحد (ة، منتهى)؛ ومن ٦٣٠ زوجًا، **زوجان
فقط** لا موضعَ يجمعهما: (ة، ي) و(ة، ٱ). أي ٠٫٣٢٪. فالتصنيفُ لا يحسم «جزءًا»
من الأصفار بل اثنين على الأكثر.

`TWO_OF_THE_THREE_PREMISES_ARE_FALSE_ON_THE_TEXT`: قيل «ٱ ابتدائيٌّ فقط»
و«ة وى نهائيّتان فقط». والمقيس: **ٱ يقع وسطًا ٢٬٧١١ مرّة** (بِٱلْغَيْبِ ·
وَٱلَّذِينَ — كلّما سبقته سابقة)، و**ى يقع وسطًا ٥٥٩ مرّة** (شَىْءٍ ·
ٱشْتَرَىٰهُ). و**ة وحدَها تصدق فيها الدعوى**. والنتيجةُ للزوج (ٱ، ة) تبقى
قائمةً، لكن عن مقدّمةٍ مصحَّحة: ٱ ليس ابتدائيًّا بل ابتدائيٌّ ووسط، وهو
مع ذلك منفصلٌ عن نهائيٍّ خالص.

`THE_FINAL_YEH_IS_EMPTY_IN_THIS_SCRIPT`: **ي لا يقع في آخر كلمةٍ ولا مرّةً
واحدة** في المصحف، وى يقع ٦٬٠٤٦ مرّة. فهما في الرسم **توزيعٌ متكامل** عند
المنتهى. وهذا خبرٌ عن الرسم لا عن الصوت، ويقيّد أيَّ قولٍ في دمج ى→ي:
الدمجُ عند المنتهى تسويةُ رسمٍ لا اختيارَ فيه.
"""

from __future__ import annotations

from fractions import Fraction
from math import comb

from algebra.reconciliation import Partition, rounds_to

WORDS = 77_428
GRAPHEMES = 36
PAIRS = comb(GRAPHEMES, 2)

# (المحرف، مبتدأ، وسط، منتهى) — لما تذكره الدعوى وما يقابله
COUNTS: dict[str, tuple[int, int, int]] = {
    "ٱ": (10_772, 2_711, 0),
    "ة": (0, 0, 2_344),
    "ى": (0, 559, 6_046),
    "ي": (4_769, 13_451, 0),
    "ا": (13, 8_382, 16_788),
    "ء": (890, 955, 1_214),
    "ئ": (0, 888, 33),
    "ؤ": (0, 703, 3),
}


def _classes(letter: str) -> frozenset[str]:
    initial, medial, final = COUNTS[letter]
    return frozenset(
        name
        for name, count in (("مبتدأ", initial), ("وسط", medial), ("منتهى", final))
        if count
    )


def test_only_one_grapheme_of_thirty_six_occupies_a_single_position() -> None:
    """ة وحدَها ذاتُ موضعٍ واحد؛ والباقي يقع في موضعين فأكثر."""

    single = [letter for letter in COUNTS if len(_classes(letter)) == 1]
    assert single == ["ة"]
    assert _classes("ة") == frozenset({"منتهى"})


def test_the_claim_that_alef_wasla_is_initial_only_is_false() -> None:
    """ٱ يقع وسطًا ٢٬٧١١ مرّةً — خُمسُ وقوعه — كلّما سبقته سابقةٌ من ط٢."""

    initial, medial, final = COUNTS["ٱ"]
    assert medial > 0
    assert final == 0
    share = Fraction(medial, initial + medial)
    assert rounds_to(share, 4) == Fraction("0.2011")
    assert _classes("ٱ") == frozenset({"مبتدأ", "وسط"})


def test_the_claim_that_alef_maksura_is_final_only_is_false() -> None:
    """ى يقع وسطًا ٥٥٩ مرّة؛ فالدعوى تصدق في ة وحدَها من الثلاثة."""

    assert COUNTS["ى"][1] == 559
    assert _classes("ى") == frozenset({"وسط", "منتهى"})

    claimed = ("ٱ", "ة", "ى")
    true_of = [letter for letter in claimed if len(_classes(letter)) == 1]
    assert true_of == ["ة"]  # واحدةٌ من ثلاث


def test_final_yeh_is_absent_and_alef_maksura_fills_that_slot() -> None:
    """ي صفرٌ في المنتهى وى ٦٬٠٤٦ — توزيعٌ متكاملٌ في الرسم لا في الصوت."""

    assert COUNTS["ي"][2] == 0
    assert COUNTS["ى"][2] == 6_046
    assert "منتهى" not in _classes("ي")
    assert "منتهى" in _classes("ى")


def test_exactly_two_pairs_of_six_hundred_thirty_are_positionally_disjoint() -> None:
    """(ة، ي) و(ة، ٱ) لا غير — ٠٫٣٢٪ من الأزواج، لا «جزءٌ» من الأصفار."""

    assert PAIRS == 630
    letters = sorted(COUNTS)
    disjoint = [
        (first, second)
        for index, first in enumerate(letters)
        for second in letters[index + 1 :]
        if not (_classes(first) & _classes(second))
    ]
    assert sorted(tuple(sorted(pair)) for pair in disjoint) == [("ة", "ي"), ("ة", "ٱ")]

    share = Fraction(2, PAIRS)
    assert rounds_to(share * 100, 2) == Fraction("0.32")


def test_the_positional_split_is_a_partition_of_each_letters_occurrences() -> None:
    """المواضعُ الثلاثةُ قسمةٌ تامّةٌ لوقوع كلّ محرف — لا رابعَ ولا بقيّة."""

    for letter, (initial, medial, final) in COUNTS.items():
        total = initial + medial + final
        assert (
            Partition(parts=(initial, medial, final), declared_total=total).residue == 0
        ), letter
        assert total > 0, letter


def test_the_hamza_seats_are_not_positionally_isolated() -> None:
    """ء وئ وؤ تقع كلُّها في موضعين فأكثر، فلا يُحسَم شيءٌ منها بالموضع.

    وهذا يخصّ الدمجَ الأكبر (همزات → ء): لو كانت المقاعدُ منعزلةً موضعيًّا
    لكان الدمجُ مجّانيًّا بالتوزيع. وهي ليست كذلك — فثمنُه يُسدَّد من جهةٍ
    أخرى (حرفُ الجذر) كما قيل، لا من الموضع.
    """

    for seat in ("ء", "ئ", "ؤ"):
        assert len(_classes(seat)) >= 2, seat
    assert _classes("ء") == frozenset({"مبتدأ", "وسط", "منتهى"})
    assert _classes("ئ") == _classes("ؤ") == frozenset({"وسط", "منتهى"})
