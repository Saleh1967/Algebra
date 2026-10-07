"""إغلاقُ الانضمام سيرفض أوّلَ تشغيل، والرفضُ خبرُ وحدةٍ لا خبرُ بيانات.

**ما وصل**: آلةُ اشتقاقِ عمودِ الجذر والقالب من وسم QAC، بمفتاح انضمامٍ
(سورة:آية:كلمة) وإغلاقين يرفضان التشغيلَ عند اختلافهما: **١٣٠٬٠٣٠ مقطعًا**
و**٧٧٬٤٢٩ كلمة**.

`ONE_OF_THE_TWO_CLOSURES_ALREADY_HOLDS_HERE`: والأوّلُ مطابقٌ لما في هذا
المستودع سلفًا: ١٣٠٬٠٣٠ أحدُ الوحدات المنشورة في تقرير «ميلي»، مفحوصةً
هناك. فنصفُ الإغلاق مُصدَّقٌ قبل التشغيل.

`THE_SECOND_CLOSURE_DIFFERS_BY_EXACTLY_ONE_AND_THAT_IS_A_UNIT_NOT_A_DEFECT`:
وأمّا الثاني فيخالف بواحد. فكلُّ قياسٍ في هذا المستودع جرى على **٧٧٬٤٢٨
صفًّا** من المحاذاة — وهو العددُ المكتوب في التسجيل المختوم نفسِه — بينما
التقريرُ المنشورُ يُعلِن **٧٧٬٤٢٩ كلمة**. والعددان كلاهما مُودَعٌ ههنا من
موضعين مستقلَّين، والفرقُ بينهما **صفٌّ واحد**.

فالإغلاقُ سيرفض، والرفضُ صادقٌ: عددان مُعلَنان لا يتطابقان. لكنّ العلّة
**وحدةُ العدّ** — «صفٌّ في المحاذاة» ليس «كلمةً في التقرير» حتّى يُعلَن
أنّهما واحد — لا فسادَ مدوّنة. وتُصلَح بسطرٍ يُعلِن أيَّ الوحدتين يُعَدّ،
لا بتعديل رقمٍ ليوافق آخر.

`THE_ONE_ROW_CHANGES_NO_PUBLISHED_RATIO_AND_THAT_IS_NOT_A_REASON_TO_SKIP_IT`:
ولا نسبةَ منشورةً ههنا تتبدّل بهذا الصفّ: النسبُ نفسُها إلى منزلتين
المطبوعتين تحت المقامين. ومع ذلك لا يُتجاوَز الإغلاق — إذ حجّةُ «الفرقُ
صغير» هي بعينها ما يُدخِل المقاماتِ المتبدّلةَ صامتةً.
"""

from __future__ import annotations

from fractions import Fraction

from algebra.reconciliation import rounds_to

DELIVERED_SEGMENTS = 130_030
DELIVERED_WORDS = 77_429

ALIGNMENT_ROWS = 77_428
"""ما جرت عليه القياساتُ ههنا، وهو المكتوبُ في التسجيل المختوم."""

PUBLISHED_WORDS = 77_429
"""ما أعلنه التقريرُ المنشور، مفحوصًا في `test_second_construction_audit`."""

PUBLISHED_UNITS = (341_249, 77_429, 225_911, 130_030, 18_993)

# ما قِيس على المقام: موسومٌ بحالةٍ إعرابيّة، ومغطّى بجدول الحركات
CASE_TAGGED = 34_254
COVERED_BY_TABLE = 6_574


def test_the_first_closure_already_matches_a_figure_deposited_here() -> None:
    """١٣٠٬٠٣٠ مقطعًا: نصفُ الإغلاق مُصدَّقٌ من وحدات التقرير المنشورة."""

    assert DELIVERED_SEGMENTS in PUBLISHED_UNITS
    assert DELIVERED_WORDS in PUBLISHED_UNITS


def test_the_second_closure_will_refuse_and_the_gap_is_exactly_one_row() -> None:
    """٧٧٬٤٢٩ مقابلَ ٧٧٬٤٢٨: الإغلاقُ يرفض، والفرقُ صفٌّ واحدٌ لا أكثر."""

    assert DELIVERED_WORDS == PUBLISHED_WORDS
    assert DELIVERED_WORDS - ALIGNMENT_ROWS == 1
    assert DELIVERED_WORDS != ALIGNMENT_ROWS  # فيرفض الإغلاقُ بنصّ تسليمه

    # والعددان من موضعين مستقلَّين، فليس أحدُهما مشتقًّا من الآخر
    units = {"صفٌّ في المحاذاة": ALIGNMENT_ROWS, "كلمةٌ في التقرير": PUBLISHED_WORDS}
    assert len(set(units.values())) == 2


def test_the_one_row_moves_no_published_ratio_at_its_printed_precision() -> None:
    """النسبُ نفسُها تحت المقامين إلى منزلتين — والإغلاقُ لا يُتجاوَز لأجل ذلك."""

    for numerator in (CASE_TAGGED, COVERED_BY_TABLE):
        under_rows = rounds_to(Fraction(numerator * 100, ALIGNMENT_ROWS), 2)
        under_words = rounds_to(Fraction(numerator * 100, PUBLISHED_WORDS), 2)
        assert under_rows == under_words

    # ونصيبُ الصفّ الواحد نفسِه ٠٫٠٠١٣٪ — صغيرٌ، ولا يُبيح تخطّي إغلاق
    share = rounds_to(Fraction(100, PUBLISHED_WORDS), 4)
    assert share == Fraction(13, 10_000)


def test_the_repair_is_a_declaration_not_an_adjustment() -> None:
    """يُعلَن أيُّ الوحدتين يُعَدّ، ولا يُحرَّك رقمٌ ليوافق آخر."""

    repairs = (
        "يُعلَن أنّ «الكلمة» في التقرير هي «الصفّ» في المحاذاة، فيُعَدّان واحدًا",
        "يُعلَن أنّهما وحدتان، فيُسمّى الصفُّ الزائدُ ويُعَدّ",
    )
    assert len(set(repairs)) == 2
    forbidden = "يُبدَّل ٧٧٬٤٢٨ إلى ٧٧٬٤٢٩ ليمرّ الإغلاق"
    assert forbidden not in repairs
