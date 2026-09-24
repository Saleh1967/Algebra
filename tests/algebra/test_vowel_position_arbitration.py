"""شاهدٌ ثالثٌ في نزاع أرقام الحركات: عمودٌ يُطابَق، وعمودان لا.

**موقعي من النزاع**: لم أكتب في الوظائف الثلاث ولا في الحكمين، ولا أُقوّمهما.
وإنّما أملك **الركيزةَ** — عمود `surface` من المحاذاة الكاملة، ٧٧٬٤٢٨ وقوعًا
مشكولًا — فأعُدّ الحركةَ الأولى والأخيرة بثلاث قراءاتٍ مُعلَنةٍ للمقام.

**التعريفُ قبل النتيجة**: «الحركةُ الأولى» أوّلُ علامةِ ضبطٍ في الكلمة،
و«الأخيرة» آخرُها؛ والعلاماتُ ستُّ حركاتٍ (بتنوينها) والسكون. والوحدةُ
**وقوعٌ** لا نوع. وثلاثون وقوعًا من ٧٧٬٤٢٨ بلا علامةٍ ألبتّة.

`THE_CORRECTED_COLUMN_REPRODUCES_AND_THE_OTHER_TWO_DO_NOT`: عمودُ «بإخراج
السكون» يطابق قراءتي الثالثةَ بفروقِ **٠٫٣٧ · ٠٫٢٠ · ١٫٣١** نقطة. وعمودُ
«التقرير» يزيد عنها **٢٫٠ · ١٫٢ · ٥٫٤** نقطة، وعمودُ «عندي» ينقص **١٣٫٥ ·
١٫٨ · ٧٫٦**. فالتصحيحُ مُصدَّقٌ بشاهدٍ ثالثٍ لم يشارك في النزاع.

`THE_DENOMINATOR_IS_THE_WHOLE_DISPUTE`: الفرقُ بين ٦٥٫٦٩٪ و٧٠٫١٧٪ ليس عدًّا
مختلفًا بل **مقامًا مختلفًا**: إدخالُ السكون أو إخراجُه. وثلاثُ قراءاتٍ
للمقام تُعطي ثلاثةَ أرقامٍ **كلُّها صادقة**. فمن نقل رقمًا بلا مقامه نقل نصفَ
خبر — وهذا تاسعُ موضعٍ في هذه السلسلة.

`THE_DIRECTION_SURVIVES_ALL_THREE_COLUMNS`: ونصيبُ الضمّة في الآخر إلى
نصيبها في الأوّل: **٢٫٢١×** عندي، و٢٫٠٥× في العمود المصحَّح، و٢٫٤٦× في
التقرير — **و١٫٧٨× في العمود غير المصحَّح وحدَه**. فخمسُ قراءاتٍ من ستٍّ
تتّفق على «ضعفان فأكثر»، والسادسةُ هي بعينها التي سُحِبت.
"""

from __future__ import annotations

from fractions import Fraction

from algebra.reconciliation import Partition, rounds_to

TOKENS = 77_428
UNMARKED = 30
FIRST_SUKUN_DENOMINATOR = 72_453
LAST_SUKUN_DENOMINATOR = 68_383

# قراءاتي الثلاثُ للمقام: (فتحةٌ أولى، ضمّةٌ أولى، ضمّةٌ أخيرة)
MINE: dict[str, tuple[str, str, str]] = {
    "كلُّ الوقوعات": ("65.66", "9.64", "20.14"),
    "ما فيه علامة": ("65.69", "9.64", "20.15"),
    "بلا سكون": ("70.17", "10.30", "22.81"),
}

DISPUTED: dict[str, tuple[str, str, str]] = {
    "التقرير": ("72.22", "11.48", "28.21"),
    "عندي": ("56.72", "8.52", "15.20"),
    "بإخراج السكون": ("69.80", "10.50", "21.50"),
}


def _gap(one: tuple[str, str, str], other: tuple[str, str, str]) -> tuple[float, ...]:
    return tuple(
        round(abs(float(Fraction(a)) - float(Fraction(b))), 2)
        for a, b in zip(one, other, strict=True)
    )


def test_the_first_vowel_distribution_is_a_partition_without_residue() -> None:
    """الحركاتُ الثلاثُ والسكونُ قسمةٌ تامّةٌ لما فيه علامة — لا خامسَ ولا بقيّة."""

    marked = TOKENS - UNMARKED
    assert marked == 77_398
    # فتحة ٦٥٫٦٩ · ضمّة ٩٫٦٤ · كسرة ١٨٫٢٨ · سكون ٦٫٣٩ على المقام المعلَّم
    parts = (6_569, 964, 1_828, 639)
    assert Partition(parts=parts, declared_total=10_000).residue == 0

    # ومقامُ «بلا سكون» هو المعلَّمُ ناقصَ ساكني الأوّل
    assert FIRST_SUKUN_DENOMINATOR < marked
    assert LAST_SUKUN_DENOMINATOR < FIRST_SUKUN_DENOMINATOR


def test_the_corrected_column_reproduces_within_one_and_a_third_points() -> None:
    """«بإخراج السكون» يطابق قراءتي الثالثة: ٠٫٣٧ · ٠٫٢٠ · ١٫٣١ نقطة."""

    gaps = _gap(DISPUTED["بإخراج السكون"], MINE["بلا سكون"])
    assert gaps == (0.37, 0.20, 1.31)
    assert max(gaps) < 1.5


def test_the_two_disputed_columns_do_not_reproduce() -> None:
    """«التقرير» يزيد على أقرب قراءاتي، و«عندي» ينقص عنها — وكلاهما بعيد."""

    report_gap = _gap(DISPUTED["التقرير"], MINE["بلا سكون"])
    his_gap = _gap(DISPUTED["عندي"], MINE["ما فيه علامة"])

    assert report_gap == (2.05, 1.18, 5.40)
    assert his_gap == (8.97, 1.12, 4.95)
    assert max(report_gap) > 1.5
    assert max(his_gap) > 1.5


def test_the_denominator_is_the_whole_dispute() -> None:
    """ثلاثُ قراءاتٍ للمقام تُعطي ثلاثةَ أرقامٍ كلُّها صادقة على مقامها."""

    all_tokens = Fraction(MINE["كلُّ الوقوعات"][0])
    marked_only = Fraction(MINE["ما فيه علامة"][0])
    no_sukun = Fraction(MINE["بلا سكون"][0])

    assert all_tokens < marked_only < no_sukun
    assert rounds_to(no_sukun - all_tokens, 2) == Fraction("4.51")
    assert rounds_to(marked_only - all_tokens, 2) == Fraction("0.03")

    # فثلاثون وقوعًا بلا علامةٍ لا تحرّك شيئًا، والسكونُ يحرّك أربعَ نقاطٍ ونصفًا
    assert UNMARKED < 100


def test_the_direction_survives_every_column() -> None:
    """الضمّةُ أخيرًا ضعفا نصيبها أوّلًا — في خمسِ قراءاتٍ من ستّ.

    والاستثناءُ عمودُ «عندي» غيرُ المصحَّح: ١٫٧٨× وحدَه دون الضعفين. فسقوطُ
    ذلك العمود في المقدار يسقطه في الاتّجاه أيضًا — وهو ما يقوّي تصحيحَه.
    """

    ratios = {}
    for name, (_, first_damma, last_damma) in {**MINE, **DISPUTED}.items():
        ratios[name] = Fraction(last_damma) / Fraction(first_damma)

    assert rounds_to(ratios["بلا سكون"], 2) == Fraction("2.21")
    assert rounds_to(ratios["بإخراج السكون"], 2) == Fraction("2.05")
    assert rounds_to(ratios["التقرير"], 2) == Fraction("2.46")
    above_two = [name for name, value in ratios.items() if value > 2]
    assert len(above_two) == 5
    assert set(ratios) - set(above_two) == {"عندي"}
    assert rounds_to(ratios["عندي"], 2) == Fraction("1.78")

    # والدعوى القائمةُ على الاتّجاه لا تسقط بسقوط المقدار
    assert max(ratios.values()) - min(ratios.values()) < Fraction(1)


def test_the_last_vowel_is_flatter_than_the_first() -> None:
    """الأولى فتحةٌ في سبعين بالمئة، والأخيرة تتوزّع على الثلاث تقريبًا سواء.

    ٥٣٫٣١ · ٢٢٫٨١ · ٢٣٫٨٨ في الآخر مقابل ٧٠٫١٧ · ١٠٫٣٠ · ١٩٫٥٣ في الأوّل.
    فموضعُ الإعراب **أقلُّ تحيّزًا** من موضع البنية — وذلك خبرٌ عن العربيّة
    يلزم من الجدول نفسِه، ولا يحتاج إلى نزاعٍ في المقام.
    """

    first = (Fraction("70.17"), Fraction("10.30"), Fraction("19.53"))
    last = (Fraction("53.31"), Fraction("22.81"), Fraction("23.88"))

    assert sum(first) == Fraction(100)
    assert sum(last) == Fraction(100)
    assert max(first) - min(first) == Fraction("59.87")
    assert max(last) - min(last) == Fraction("30.50")
    assert max(last) - min(last) < max(first) - min(first)
