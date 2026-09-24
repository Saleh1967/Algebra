"""التجربةُ المعلَّقةُ شُغِّلت: قراران في التعريف يقلبان الحكمَ من ٣١٪ إلى ٧٠٪.

**ما جرى**: سُئل «أتجه لإعدادها الآن؟» — والمحاذاةُ مشكولةٌ وتحمل الحالةَ في
عمود `gold`، فشُغِّلت ولم تُعَدّ. والبصمةُ `46b4393fdb3a0920…`.

`THE_LABEL_IS_NOT_READ_OFF_THE_VOWEL_SO_THE_TEST_IS_NOT_CIRCULAR`: وأوّلُ
ما يُفحَص **الدائريّة**: لو كانت الحالةُ مقروءةً من الحركة لكانت
`H(الحركة | الحالة)` صفرًا بالبناء. وهي **١٫٧٧ بت** على التعريف الخام —
فالوسمُ مستقلٌّ عن الحركة، والتجربةُ سليمةٌ من هذا الوجه.

`BUT_THE_EXPECTED_RESULT_IS_REFUTED_BY_THE_RAW_DEFINITION`: ومع ذلك فالحكمُ
المنتظَر — «تخرج من الضعيف المشهود إلى الكامل المقيس» — **يسقط على التعريف
كما صيغ**: الحالةُ تُزيل **٣٠٫٩٪** لا أكثر، وأغلبُ حركةٍ لكلّ حالةٍ ٤٦–٥٥٪.
ولو نُشِر هكذا لقيل «الإعرابُ ضعيفٌ في الصوت أيضًا» — وذلك **غلطٌ في المقياس
لا خبرٌ عن العربيّة**.

`TWO_UNDECLARED_DECISIONS_CARRY_THE_WHOLE_HEADLINE`: والقراران:

* **اللاحقة**: «الحركةُ الأخيرة» ليست «علامةَ الإعراب» متى لحقت لاحقة —
  فعلامةُ ٱلْعَٰلَمِينَ على النون لا على ما قبلها. و**٣٦٫٦٪** من الموسوم
  بحالةٍ يحمل لاحقة. وبإخراجها: ٣٠٫٩٪ ← **٤٥٫٨٪**.
* **التنوين**: عَدُّ «تنوين الضمّ» قيمةً غيرَ «الضمّة» يجعل المفردةَ سبعًا،
  والحالةُ لا تفرّق بينهما أصلًا. وبردّه إلى أصله: ٤٥٫٨٪ ← **٦٩٫٨٪**.

فالقراران معًا يرفعان المُزال **من ٣٠٫٩٪ إلى ٦٩٫٨٪**، وأغلبَ حركةٍ لكلّ
حالةٍ **من ٤٦–٥٥٪ إلى ٩٠–٩٣٪**. **وكلاهما غيرُ مُعلَنٍ في التصميم المقترَح.**

`AND_THE_RESIDUE_IS_THE_REAL_FINDING_AT_EIGHT_PERCENT_NOT_FIFTY`: وما يبقى
بعدهما **٠٫٤٧ بت** ونحوُ ثُمنٍ من الوقوعات لا تأخذ حركةَ حالتها — وفيه
الممنوعُ من الصرف والمقدَّرُ والساكن. فـ«الإعرابُ ليس تامًّا في الصوت» خبرٌ
صحيح، **ومقدارُه ثمانيةٌ بالمئة لا خمسةٌ وخمسون**.

`THE_RASM_SIGNAL_REPRODUCES_EXACTLY_AND_IS_TINY_AS_HE_SAID`: وشاهدُ المثنّى
والجمع يُعاد إلى آخر رقم: ٤٢٫١٪ مقابل ٣٠٫٧٪، `z = +٦٫٧١`، `MI = ٠٫٠٠٣٦` بت
— أي **٠٫٣٩٪** من إنتروبيا النهاية. ونسبةُ الأرجحيّة ١٫٦٤×. فدالٌّ وضئيلُ
الأثر معًا، وقولُه «الضعفُ نفسُه الخبر» صوابٌ بعينه.
"""

from __future__ import annotations

import math
from fractions import Fraction

from algebra.reconciliation import Partition, rounds_to

SOURCE_DIGEST = "46b4393fdb3a09208ecb96fbbac990a150e4374f82d7940c655430cd1b1611ae"

CASED_TOKENS = 34_254
WITH_SUFFIX = 12_545
WITHOUT_SUFFIX = 21_709

# (اسمُ التعريف، المقام، H غيرَ مشروطة، H|الحالة)
READINGS: dict[str, tuple[int, float, float]] = {
    "خامٌّ — سبعُ قيمٍ وكلُّ الوقوعات": (34_254, 2.5664, 1.7728),
    "بإخراج اللاحقة": (21_709, 2.4716, 1.3387),
    "وبردّ التنوين — وكلُّ الوقوعات": (34_254, 1.7761, 1.0463),
    "بالقرارين معًا": (21_709, 1.5713, 0.4738),
}

MODAL_RAW = {"raf'": 46.0, "nasb": 54.4, "jarr": 55.4}
MODAL_CLEAN = {"raf'": 92.4, "nasb": 93.3, "jarr": 90.1}

# شاهدُ الرسم: (ان/ون، ين)
AFTER_JARR, OTHERWISE = (479, 349), (5_476, 2_430)


def test_the_case_label_is_independent_of_the_vowel() -> None:
    """`H(الحركة | الحالة)` ليست صفرًا، فالوسمُ ليس مقروءًا من الحركة."""

    _, _, conditioned = READINGS["خامٌّ — سبعُ قيمٍ وكلُّ الوقوعات"]
    assert conditioned > 1.5  # ولو كان دائريًّا لقارب الصفر
    assert conditioned > 0

    # والحالاتُ الثلاثُ تقسم الموسومَ بلا بقيّة
    assert (
        Partition(parts=(8_806, 12_824, 12_624), declared_total=CASED_TOKENS).residue
        == 0
    )


def test_the_raw_definition_would_have_refuted_the_expected_result() -> None:
    """٣٠٫٩٪ فقط، وأغلبُ حركةٍ ٤٦–٥٥٪ — ولو نُشِرت لقيل «الإعرابُ ضعيف»."""

    total, free, conditioned = READINGS["خامٌّ — سبعُ قيمٍ وكلُّ الوقوعات"]
    assert total == CASED_TOKENS
    removed = (free - conditioned) / free
    assert round(removed * 100, 1) == 30.9

    assert max(MODAL_RAW.values()) < 60
    assert min(MODAL_RAW.values()) < 50
    # فالحكمُ المنتظَر («الكاملُ المقيس») ساقطٌ على هذا التعريف
    assert removed < Fraction(1, 2)


def test_two_decisions_move_the_headline_by_thirty_nine_points() -> None:
    """٣٠٫٩٪ ← ٤٥٫٨٪ بإخراج اللاحقة ← ٦٩٫٨٪ بردّ التنوين."""

    def removed(name: str) -> float:
        _, free, conditioned = READINGS[name]
        return (free - conditioned) / free * 100

    assert round(removed("خامٌّ — سبعُ قيمٍ وكلُّ الوقوعات"), 1) == 30.9
    assert round(removed("بإخراج اللاحقة"), 1) == 45.8
    assert round(removed("وبردّ التنوين — وكلُّ الوقوعات"), 1) == 41.1
    assert round(removed("بالقرارين معًا"), 1) == 69.8

    swing = removed("بالقرارين معًا") - removed("خامٌّ — سبعُ قيمٍ وكلُّ الوقوعات")
    assert round(swing, 1) == 38.9

    # ولا يكفي أحدُهما: كلٌّ وحدَه دون النصف أو قريبٌ منه
    assert removed("بإخراج اللاحقة") < removed("بالقرارين معًا")
    assert removed("وبردّ التنوين — وكلُّ الوقوعات") < removed("بالقرارين معًا")


def test_the_suffix_share_explains_why_the_last_mark_is_not_the_case_mark() -> None:
    """٣٦٫٦٪ من الموسوم بحالةٍ يحمل لاحقةً، فعلامتُه ليست آخرَ علامةٍ فيه."""

    assert (
        Partition(
            parts=(WITH_SUFFIX, WITHOUT_SUFFIX), declared_total=CASED_TOKENS
        ).residue
        == 0
    )
    assert rounds_to(Fraction(WITH_SUFFIX, CASED_TOKENS) * 100, 1) == Fraction("36.6")

    _, free_with, cond_with = 0, 2.4179, 2.0389
    _, free_without, cond_without = READINGS["بإخراج اللاحقة"]
    with_suffix = (free_with - cond_with) / free_with
    without_suffix = (free_without - cond_without) / free_without
    assert round(with_suffix * 100, 1) == 15.7
    assert round(without_suffix * 100, 1) == 45.8
    assert without_suffix > with_suffix * 2  # فاللاحقةُ تحجب العلامةَ لا تزيدها


def test_the_residue_after_both_corrections_is_the_real_finding() -> None:
    """٩٠–٩٣٪ تأخذ حركةَ حالتها، فالنقصُ ثُمنٌ لا نصف."""

    assert min(MODAL_CLEAN.values()) > 90
    assert max(MODAL_CLEAN.values()) < 94
    for case, share in MODAL_CLEAN.items():
        assert share > MODAL_RAW[case] * 1.6, case

    _, _, conditioned = READINGS["بالقرارين معًا"]
    assert round(conditioned, 2) == 0.47
    assert conditioned > 0  # فليس تامًّا، والنقصُ مقيسٌ لا مقدَّر

    shortfall = 100 - sum(MODAL_CLEAN.values()) / 3
    assert round(shortfall, 1) == 8.1


def test_the_rasm_signal_reproduces_to_the_last_digit() -> None:
    """٤٢٫١٪ مقابل ٣٠٫٧٪ · z = +٦٫٧١ · MI = ٠٫٠٠٣٦ بت = ٠٫٣٩٪."""

    after, otherwise = AFTER_JARR, OTHERWISE
    first = otherwise[1] / sum(otherwise)
    jarred = after[1] / sum(after)
    assert round(jarred * 100, 1) == 42.1
    assert round(first * 100, 1) == 30.7

    total = sum(after) + sum(otherwise)
    pooled = (after[1] + otherwise[1]) / total
    spread = math.sqrt(pooled * (1 - pooled) * (1 / sum(after) + 1 / sum(otherwise)))
    assert round((jarred - first) / spread, 2) == 6.71

    mutual = 0.0
    for row, counts in ((sum(after), after), (sum(otherwise), otherwise)):
        for index, value in enumerate(counts):
            column = (after[index] + otherwise[index]) / total
            mutual += (value / total) * math.log2(
                (value / total) / ((row / total) * column)
            )
    assert round(mutual, 4) == 0.0036

    shares = [(after[i] + otherwise[i]) / total for i in (0, 1)]
    ending_entropy = -sum(one * math.log2(one) for one in shares)
    assert round(mutual / ending_entropy * 100, 2) == 0.39
    assert SOURCE_DIGEST[:8] == "46b4393f"


def test_significant_and_slight_are_two_readings_of_one_table() -> None:
    """`z = +٦٫٧١` دالٌّ، و`MI = ٠٫٣٩٪` ضئيل — وكلاهما صادقٌ على الجدول."""

    odds = (0.421 / 0.579) / (0.307 / 0.693)
    assert round(odds, 2) == 1.64
    assert round((0.421 - 0.307) * 100, 1) == 11.4

    # والدلالةُ من الحجم (٨٬٧٣٤ صفًّا) والضآلةُ من الأثر — ولا تُطرَح إحداهما
    assert sum(AFTER_JARR) + sum(OTHERWISE) == 8_734
    assert 1 < odds < 2
