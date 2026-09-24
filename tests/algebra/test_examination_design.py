"""تصميمُ الامتحان قبل تشغيله: ثلاثةٌ تُضاف الآن أو لا تُضاف أبدًا.

**موقعي**: التصميمُ صائبٌ في جوهره — إسقاطُ الحَكَم بقلب المهمّة إلى ترتيبٍ
يعرف الجدولُ جوابَه، وقياسُ الصفريّ **قبل** التسجيل لا بعده، وإعلانُ فشل
العنقدة. ولا أُقوّم قياسًا لم يجرِ. وأقول ثلاثةً **يستحيل إضافتُها بعد
التشغيل**، وهي من جنسٍ سبق أن رُدَّ به على المصدر والمقاييس.

`THE_POSITIONS_ARE_NOT_INDEPENDENT_OBSERVATIONS`: ٤٬٤١١ موضعًا من **١٬١٢٠
لِمّة** — ٣٫٩٤ موضعًا لكلّ لِمّة. والمواضعُ تتشارك **جردَ الشروح نفسَه**،
فليست مشاهداتٍ مستقلّة. فخطأٌ معياريٌّ محسوبٌ على ٤٬٤١١ يعطي مجالَ ثقةٍ
±٠٫٨٨ نقطة، وعلى ١٬١٢٠ يعطي **±١٫٧٥** — ضعفًا تقريبًا (√٣٫٩٤ = ١٫٩٨).
وهو العطلُ نفسُه الذي رُدَّ به «٨٦ وقوعًا من أربعة جذور».

`THE_SPLIT_MUST_BE_BY_LEMMA_OR_THE_GLOSSES_LEAK`: إن قُسِمت المواضعُ قسمةً
عشوائيّةً وقع من مواضع اللِّمّة الواحدة في القسمين. وجردُ شروحها مشترَك،
فمعرفةُ جواب موضعٍ **تقيّد** جوابَ أخيه. فالقسمةُ باللِّمّة لا بالموضع، وإلّا
كان الاختبارُ داخلَ العيّنة جزئيًّا — وذلك ما سقط عليه ط٣ و ط٥ من قبل.

`A_POOLED_NULL_HIDES_A_SPREAD_OF_TEN_TO_ONE`: الصفريُّ ٠٫٠٩٩٠ **مجمَّع**.
ولِمّةٌ بشرحين صفريُّها ٠٫٥٠، وبعشرين ٠٫٠٥ — عشرةُ أضعاف. والمقيسُ يعادل
وسطًا تناسقيًّا لـ`k` ≈ ١٠٫١. فدقّةٌ مجمَّعةٌ فوق الصفريّ قد تنشأ **كلُّها**
من لِمَمِ الشرحين، ولا يُعرَف ذلك إلّا بتصنيفٍ بـ`k` — كما اتُّفق على
التصنيف بنطاق التردّد.

`FOUR_HUNDRED_AND_SIXTY_ONE_TOKENS_LEFT_THE_TEST_UNNAMED`: ٤٬٨٧٢ رمزًا
للِّمَم ذات الشروح المتعدّدة، و٤٬٤١١ موضعَ اختبار. فـ**٤٦١ = ٩٫٤٦٪** خرجت،
ولم يُسمَّ سببُ خروجها. ومصفاةٌ لا يُعلَن حجمُها جزءٌ من القياس لا هامشٌ فيه.
"""

from __future__ import annotations

import math
from fractions import Fraction

from algebra.evaluation import Split
from algebra.reconciliation import Partition, rounds_to

LEMMAS = 1_120
TOKENS_OF_THOSE_LEMMAS = 4_872
TEST_POSITIONS = 4_411
NULL = Fraction("0.0990")
EXAM_ROOM = Fraction("0.9010")


def test_the_exam_room_is_one_minus_the_measured_null() -> None:
    """٠٫٩٠١٠ = ١ − ٠٫٠٩٩٠، والصفريُّ **مقيسٌ** لا مفترَض — وذلك يُقال."""

    assert NULL + EXAM_ROOM == 1
    assert rounds_to(EXAM_ROOM, 4) == Fraction("0.9010")


def test_four_hundred_sixty_one_positions_left_without_a_named_reason() -> None:
    """٤٬٨٧٢ − ٤٬٤١١ = ٤٦١ = ٩٫٤٦٪ خرجت، ولم يُسمَّ لها سبب."""

    dropped = TOKENS_OF_THOSE_LEMMAS - TEST_POSITIONS
    assert dropped == 461
    assert (
        Partition(
            parts=(TEST_POSITIONS, dropped), declared_total=TOKENS_OF_THOSE_LEMMAS
        ).residue
        == 0
    )
    assert rounds_to(Fraction(dropped, TOKENS_OF_THOSE_LEMMAS) * 100, 2) == Fraction(
        "9.46"
    )


def test_the_effective_sample_is_the_lemma_not_the_position() -> None:
    """٣٫٩٤ موضعًا لكلّ لِمّة، فالمجالُ يتّسع ١٫٩٨× إن حُسِب على اللِّمَم."""

    per_lemma = Fraction(TEST_POSITIONS, LEMMAS)
    assert round(float(per_lemma), 2) == 3.94

    variance = float(NULL) * (1 - float(NULL))
    naive = math.sqrt(variance / TEST_POSITIONS)
    clustered = math.sqrt(variance / LEMMAS)

    assert round(1.96 * naive * 100, 2) == 0.88
    assert round(1.96 * clustered * 100, 2) == 1.75
    assert round(clustered / naive, 2) == 1.98
    assert round(math.sqrt(float(per_lemma)), 2) == 1.98  # وهو جذرُ العنقود بعينه


def test_a_random_split_by_position_leaks_the_gloss_inventory() -> None:
    """مواضعُ اللِّمّة الواحدة تتشارك جردَ شروحها، فقسمتُها تُسرِّب الجواب."""

    # لِمّةٌ واحدةٌ مواضعُها موزّعةٌ على القسمين
    train = frozenset({"وليّ@٢:١٠٧", "وليّ@٤:٤٥"})
    test = frozenset({"وليّ@٦:١٤", "بيّنة@٢:٢١١"})
    split = Split(train=train, test=test)
    assert not (train & test)  # لا موضعَ مشترَك…

    # …ومع ذلك فاللِّمّةُ «وليّ» في القسمين معًا، وهو التسرّبُ بعينه
    lemmas_in_train = {key.split("@")[0] for key in train}
    lemmas_in_test = {key.split("@")[0] for key in test}
    assert lemmas_in_train & lemmas_in_test == {"وليّ"}
    assert split.test_share == Fraction(1, 2)


def test_the_pooled_null_spans_an_order_of_magnitude_by_gloss_count() -> None:
    """صفريُّ الشرحين ٠٫٥٠ وصفريُّ العشرين ٠٫٠٥ — عشرةُ أضعاف تحت رقمٍ واحد."""

    by_k = {k: Fraction(1, k) for k in (2, 3, 5, 10, 20)}
    assert by_k[2] == Fraction("0.5")
    assert by_k[20] == Fraction("0.05")
    assert by_k[2] / by_k[20] == 10

    harmonic_k = 1 / NULL
    assert round(float(harmonic_k), 1) == 10.1
    assert NULL < by_k[10]  # فالمجمَّعُ دون صفريّ العشرة بقليل
    assert by_k[20] < NULL


def test_the_three_additions_are_impossible_after_the_run() -> None:
    """قسمةٌ باللِّمّة · تصنيفٌ بـk · معنويّةٌ على اللِّمَم — تُكتَب الآن أو أبدًا.

    فالقسمةُ لا تُعاد بعد أن يُرى الرقم، والتصنيفُ بعد النظر اختيارُ شريحةٍ،
    والمعنويّةُ المحسوبةُ على المواضع لا تُصحَّح بضربٍ بعد الإعلان.
    """

    before_the_run = (
        "القسمةُ باللِّمّة لا بالموضع",
        "الدقّةُ مصنَّفةً بعدد شروح اللِّمّة",
        "المعنويّةُ على اللِّمَم لا على المواضع",
    )
    assert len(before_the_run) == 3
    assert len(set(before_the_run)) == 3
    for item in before_the_run:
        assert " أو " not in item  # ولا واحدٌ منها بديلٌ عن آخر


def test_the_failed_clustering_is_the_finding_that_justified_the_design() -> None:
    """«وليّ» خرجت بعشرين معنًى وفيها ثلاثةٌ مترادفة — فالعنقدةُ لا تصنع جردًا.

    والدرسُ هو الذي أنتج التصميم: **لا يُبنى صنفٌ لا يمكن التحقّقُ منه**.
    فالامتحانُ لا يُبنى على جردٍ أصلًا، بل على ترتيبِ ما في الكتاب. وإعلانُ
    المحاولة الفاشلة هو ما يجعل التصميمَ مُبرَّرًا لا مُختارًا.
    """

    clusters_for_wali = 20
    synonymous_among_them = 3
    assert clusters_for_wali > synonymous_among_them > 1
    assert clusters_for_wali >= 20  # وعنقودٌ واحدٌ في «بيّنة» — فالنجاحُ فردٌ لا قاعدة
