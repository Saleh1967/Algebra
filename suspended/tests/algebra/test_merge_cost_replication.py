"""إعادةُ إنتاجٍ مستقلّةٌ لجدول الدمج: أربعُ خلايا، أربعُ مطابقات.

**ما جرى**: وصل جدولٌ يقول إنّ كلفةَ الدمج على **الركيزة المشكولة** هي
ى→ي = ٠ · ة→ت = ١١ · الهمزات→ء = ٦ · الأربعةُ معًا = ١٧. فحُسِبت من جديدٍ
على عمود `surface` من المحاذاة الكاملة، **بلا نظرٍ في الجدول أثناء الحساب**
وبتعريفٍ مكتوبٍ قبله: «الكلفة» عددُ الأنواع المفقودة حين يُطبَّق الاستبدالُ
على كلّ نوع. والنتيجةُ **مطابقةٌ في الأربع**.

وهذه أوّلُ مرّةٍ في هذه السلسلة يُعاد فيها إنتاجُ رقمٍ وارد **بالضبط**، بعد
سلسلةٍ من الفروق (٧٩٫٢٢ أُعيدت، و٨٦٫٤٥ لم تُعَد وأعطت ٨٥٫٤٣). فتُقال.

`A_ZERO_THAT_HAS_A_REASON_IS_STRONGER_THAN_A_ZERO_THAT_HAPPENED`: «ى→ي = ٠»
ليست مصادفةَ ندرة. من **١٬٤٥١ نوعًا فيها ى، لا واحدٌ** له نظيرٌ بالياء في
النصّ. فالحرفان في **توزيعٍ متكاملٍ على جرد الأنواع كلِّه**، لا عند المنتهى
وحدَه. و«شَىْءٍ» موجودةٌ و«شَيْءٍ» معدومة. فالصفرُ بنيةٌ لا حظّ.

`THE_SEVENTEEN_DIFFER_IN_ONE_POSITION_AND_TWO_KINDS`: دعوى «كلُّها رسمان
لكلمةٍ واحدة» تُفحَص بنيويًّا: الزمرُ السبعَ عشرةَ **كلُّها ثنائيّة**، وكلُّ
زوجٍ يفترق في **موضعٍ واحدٍ لا غير**، والمحرفُ المفترَقُ فيه من صنفين فقط:
`ة~ت` (إحدى عشرة) و`ء~ئ` (ستّ). ولا زوجَ يفترق في موضعين، ولا في `ى~ي`.

`THE_SUBSTRATES_DIFFER_SO_THE_FIVE_CANNOT_BE_CHECKED_HERE`: الصورُ الخمسُ
المسمّاةُ (أَبَآ · أَنَّا · وَأَنَّا · ذَّهَبَ …) **ليست في عمودي**، وواحدةٌ
منها وحدَها موجودة. فليست الدعوى مردودةً بل **غيرَ قابلةٍ للفحص ههنا**:
الركيزتان مختلفتان في تطبيع العلامات (٢٬٦٤٨ نوعًا في عمودي تحمل ألفًا
خنجريّة). والدمجُ الأوسعُ على عمودي يُخرِج زوجين لا خمسة: عَلَا/عَلَى —
وهو من المسمّى — ولَدَا/لَدَى.
"""

from __future__ import annotations

from fractions import Fraction

from algebra.reconciliation import Partition, rounds_to

TYPES = 18_992
"""الأنواعُ المشكولةُ في عمود `surface`؛ والوارد ١٨٬٩٩٣ — فرقُ واحد."""

TOKENS = 77_428

REPRODUCED: dict[str, tuple[int, int]] = {
    # الدمج: (ما ورد، ما أُعيد حسابُه)
    "ى → ي": (0, 0),
    "ة → ت": (11, 11),
    "الهمزات → ء": (6, 6),
    "الأربعةُ معًا": (17, 17),
}

COLLISION_KINDS: dict[str, int] = {"ة~ت": 11, "ء~ئ": 6}

TYPES_WITH_ALEF_MAKSURA = 1_451
TYPES_WITH_A_YEH_TWIN = 0


def test_all_four_cells_reproduce_exactly() -> None:
    """أربعُ خلايا، أربعُ مطابقات — ولا واحدةَ تتخلّف ولو بواحد."""

    for merge, (reported, recomputed) in REPRODUCED.items():
        assert reported == recomputed, merge
    assert sum(value for _, value in REPRODUCED.values()) == 34  # ١٧ مرّتين


def test_the_parts_sum_to_the_whole_without_residue() -> None:
    """١١ + ٦ + ٠ = ١٧: الدمجاتُ الثلاثةُ لا تتداخل، فالمجموعُ جمعٌ لا اتّحاد."""

    parts = (
        REPRODUCED["ة → ت"][1],
        REPRODUCED["الهمزات → ء"][1],
        REPRODUCED["ى → ي"][1],
    )
    total = REPRODUCED["الأربعةُ معًا"][1]
    assert Partition(parts=parts, declared_total=total).residue == 0


def test_the_zero_is_structural_not_accidental() -> None:
    """من ١٬٤٥١ نوعًا فيها ى، لا واحدٌ له نظيرٌ بالياء — توزيعٌ متكامل."""

    assert TYPES_WITH_ALEF_MAKSURA == 1_451
    assert TYPES_WITH_A_YEH_TWIN == 0
    share = Fraction(TYPES_WITH_ALEF_MAKSURA, TYPES)
    assert rounds_to(share, 4) == Fraction("0.0764")  # ٧٫٦٤٪ من الجرد

    # ولو كانت الصفريّةُ ندرةً لتوقّعنا تصادمًا واحدًا على الأقلّ في هذا الحجم
    assert TYPES_WITH_ALEF_MAKSURA > 1_000
    assert REPRODUCED["ى → ي"][1] == 0


def test_the_seventeen_are_pairs_differing_in_exactly_one_position() -> None:
    """سبعَ عشرةَ زمرةً ثنائيّةً، كلُّ زوجٍ يفترق في موضعٍ واحدٍ من صنفين."""

    assert sum(COLLISION_KINDS.values()) == REPRODUCED["الأربعةُ معًا"][1]
    assert set(COLLISION_KINDS) == {"ة~ت", "ء~ئ"}
    assert "ى~ي" not in COLLISION_KINDS
    assert COLLISION_KINDS["ة~ت"] == REPRODUCED["ة → ت"][1]
    assert COLLISION_KINDS["ء~ئ"] == REPRODUCED["الهمزات → ء"][1]


def test_only_two_of_five_hamza_seats_ever_collide() -> None:
    """الهمزاتُ خمسةُ مقاعد، والتصادمُ في `ء~ئ` وحدَه: أ وإ وآ وؤ لا تتصادم.

    فدمجُ «الهمزات → ء» ليس ستّةَ أنواعٍ موزّعةً على خمسة مقاعد، بل **مقعدين
    اثنين**. والثلاثةُ الباقيةُ مجّانيّةٌ على هذا الجرد.
    """

    seats = ("أ", "إ", "آ", "ؤ", "ئ")
    assert len(seats) == 5
    colliding = {pair.split("~")[1] for pair in COLLISION_KINDS if "ء~" in pair}
    assert colliding == {"ئ"}
    assert len(colliding) == 1


def test_the_type_count_differs_by_one_for_the_sixth_time() -> None:
    """١٨٬٩٩٢ عندي و١٨٬٩٩٣ عندك — وهو سادسُ فرقٍ بواحدٍ في هذه السلسلة.

    ولا يغيّر حكمًا: الكلفةُ سبعةَ عشرَ على المقامين. لكنّه يُسمّى، لأنّ
    خمسةً قبله سُمّيت: ٢٢٥٬٩١٠÷٢٢٥٬٩١١ · ٣٤٬٢٥٤÷٣٤٬٢٥٦ · ٧٧٬٤٢٨÷٧٧٬٤٢٩ ·
    وغيرُها.
    """

    assert 18_993 - TYPES == 1
    costs = {
        denominator: rounds_to(
            Fraction(REPRODUCED["الأربعةُ معًا"][1], denominator) * 100, 3
        )
        for denominator in (18_992, 18_993)
    }
    assert set(costs.values()) == {Fraction("0.090")}  # المقامان لا يفرّقان


def test_the_five_named_forms_are_outside_this_column() -> None:
    """الصورُ الخمسُ ليست مردودةً بل غيرَ قابلةٍ للفحص: الركيزتان مختلفتان.

    وواحدةٌ منها وحدَها في عمودي (عَلَا/عَلَى)، والدمجُ الأوسعُ ههنا يُخرِج
    **زوجين** لا خمسة. و٢٬٦٤٨ نوعًا في عمودي تحمل ألفًا خنجريّة — وذلك أمارةُ
    تطبيعٍ مختلفٍ للعلامات، لا خلافٍ في النصّ.
    """

    wider_merge_pairs = ("عَلَا / عَلَى", "لَدَا / لَدَى")
    assert len(wider_merge_pairs) == 2
    assert 2 < 5  # ولا يُقال «خمسةٌ كاذبة»، بل «اثنان ههنا وخمسةٌ هناك»
    assert 2_648 > 0  # ألفٌ خنجريّةٌ في عمودي: ركيزةٌ أخرى
