"""تدرُّجُ التعريب: الاتّجاهُ يصمد، والمقدارُ يَرِدُ عليه ثلاثةُ قيودٍ تُحسَب.

**ما يُقاس ههنا**: أرقامُ التقرير تُعاد، ويُحسَب ما يلزم منها وما يَرِد عليها.
ولا مدوّنةَ تُقرَأ ولا نموذجَ يُشغَّل؛ والأرقامُ المحسوبةُ **عن أرقامه** لا عن
المصحف.

`THE_LOAD_BEARING_CONTRAST_IS_NOT_THE_ONE_AGAINST_THE_BASELINE`: دعوى الكتاب
عن **الصياغة** — «تُصاغ اللفظةُ بالوزن العربيّ» — فالفحصُ الذي يعزلها هو
«معرَّبٌ مصوغٌ مقابلَ معرَّبٍ غيرِ مصوغ»، لا «معرَّبٌ مقابلَ أصيل». والمقارنةُ
الأولى تشترك فيها المجموعتان في كونهما دخيلتين، فيسقط ما يشتركان فيه.
وقدرُها **+٠٫٧٨٦٢** بتّ عند رتبة ١ و**+٢٫٤٦٦٥** عند رتبة ٢.

`A_THOUSAND_TOKENS_FROM_FOUR_TYPES_ARE_FOUR_OBSERVATIONS`: ١٬٠٦٧ وقوعًا في
المجموعة التي أسماؤها أربعة؛ فالمشاهداتُ المستقلّةُ أربعٌ، والخطأُ المعياريُّ
يتّسع **١٦٫٣×**. وهو العطلُ نفسُه الذي رُدَّ به «٨٦ وقوعًا من أربعة جذور»،
وذلك **سابعَ عشرَ موضعٍ** من جنس المجال غيرِ المُعدَّد.

`AT_RANK_TWO_AT_MOST_HALF_THE_SYMBOLS_CARRY_THEIR_CONTEXT`: والأطوالُ من
واحدٍ إلى أربعة. ووحدةٌ طولُها `L` تُخرِج `L − 2` رمزًا ذا سياقٍ تامٍّ عند
رتبة ٢: فصفرٌ للطولين ١ و٢، وثلثٌ للطول ٣، ونصفٌ للطول ٤. **فالحدُّ الأعلى
نصفٌ، وقد يكون صفرًا.** وأرقامُ رتبة ٢ هي أكبرُ الفروق (+٣٫٩٨)، وهي في الوقت
نفسِه **أشدُّها تعلّقًا بالطول** — والدخيلُ أطولُ من الأصيل عادةً. فالطولُ
متغيّرٌ خفيٌّ يجري مع المجموعة.

`THE_GROUPING_IS_NOT_INDEPENDENT_BUT_THE_MEASURE_IS`: و«أُعطيَ جذرًا» حكمٌ
صرفيٌّ قد يُعطى **لأنّ** اللفظةَ على وزنٍ عربيّ — فالمتغيّرُ المصنِّفُ ليس
مستقلًّا عن الدعوى. **لكنّ المقياسَ مستقلٌّ عن التصنيف**: سلسلةُ الرموز لا
ترى وسمَ الجذر ألبتّة. فهذا **اتّفاقُ مصدرين** — حكمُ واسمٍ ونموذجُ رموز —
لا برهانٌ من مصدرٍ واحد. وهو ثاني موضعٍ في المشروع يجتمع فيه شاهدان.

`THE_DEFECT_HE_CAUGHT_REMOVED_NINE_TENTHS_OF_HIS_SET`: وأوّلُ تشغيلٍ أعطى
١٠٬١٧١ رمزًا فصارت ١٬٠٦٧ — **٨٩٫٥١٪ خرجت**. ومصفاةٌ بهذا القدر ليست تنقيحًا
بل **إعادةَ تعريفٍ للمجموعة**؛ وإعلانُها قبل النشر هو ما يجعل الباقيَ يُقرَأ.

`THE_ARGUMENT_WITHDRAWS_THE_NUMBER_THAT_FOLLOWS_IT`: والمصفاةُ **لم تُخرِج
الأعلام**: «وما بقي فيها أعلامٌ أعجميّة — موسى وفرعون وإبراهيم وجهنّم —
والكتابُ يُخرجها بنفسِه: التعريبُ خاصٌّ بأسماء الأشياء». ثمّ: «فلو نشرتُ
الـ+١٫٣٦ **لنسبتُ إلى التعريب ما هو عن الأعلام**». ثمّ نُشِر +١٫٣٦٨ في
الفقرة التالية. **والحجّةُ تسبق الرقمَ وتسقطه**، فيُسجَّل مسحوبًا ههنا.
وهذا سحبٌ للنسبة لا للقياس: الرقمُ صحيحٌ عن مجموعته، ومجموعتُه ليست
التعريب.
"""

from __future__ import annotations

from fractions import Fraction

import pytest

from algebra.evaluation import (
    ClusteredSample,
    EvaluationError,
    full_context_share,
    units_that_carry_no_context,
)
from algebra.reconciliation import Partition, rounds_to

# مفاجأةٌ بالبتّ لكلّ وحدة، كما نُشِرت
BASELINE = {1: Fraction("3.9267"), 2: Fraction("3.1386")}
SHAPED = {1: Fraction("4.8516"), 2: Fraction("4.6510")}
UNSHAPED = {1: Fraction("5.6378"), 2: Fraction("7.1175")}

SHAPED_TYPES = ("قسطاس", "سجّيل", "مشكاة", "رقيم", "أباريق", "مرجان", "سرادق", "قرطاس")
UNSHAPED_TYPES = ("إستبرق", "سندس", "زنجبيل", "فردوس")

BY_TYPE_AT_RANK_TWO = {
    "قسطاس": Fraction("3.23"),
    "مرجان": Fraction("3.44"),
    "رقيم": Fraction("3.49"),
    "إستبرق": Fraction("6.84"),
    "سندس": Fraction("7.06"),
    "فردوس": Fraction("8.78"),
}

FIRST_RUN, AFTER_THE_FILTER = 10_171, 1_067
HEADLINE, MATCHED_NULL = Fraction("1.368"), Fraction("0.10")


def test_the_four_published_gaps_recompute() -> None:
    """+٠٫٩٢ و+١٫٥١ و+١٫٧١ و+٣٫٩٨ — أربعةٌ من أربعة."""

    assert rounds_to(SHAPED[1] - BASELINE[1], 2) == Fraction("0.92")
    assert rounds_to(SHAPED[2] - BASELINE[2], 2) == Fraction("1.51")
    assert rounds_to(UNSHAPED[1] - BASELINE[1], 2) == Fraction("1.71")
    assert rounds_to(UNSHAPED[2] - BASELINE[2], 2) == Fraction("3.98")

    # والترتيبُ نظيفٌ في الرتبتين معًا: أصيلٌ < مصوغٌ < غيرُ مصوغ
    for rank in (1, 2):
        assert BASELINE[rank] < SHAPED[rank] < UNSHAPED[rank]


def test_the_contrast_that_isolates_the_book_is_within_the_loans() -> None:
    """+٠٫٧٨٦٢ و+٢٫٤٦٦٥ — وهما الرقمان اللذان يختبران «الصياغة» وحدَها."""

    assert rounds_to(UNSHAPED[1] - SHAPED[1], 4) == Fraction("0.7862")
    assert rounds_to(UNSHAPED[2] - SHAPED[2], 4) == Fraction("2.4665")

    # وهما دون الفرقين عن خطّ الأساس، فالمشترَكُ بين الدخيلتين يسقط
    assert UNSHAPED[1] - SHAPED[1] < UNSHAPED[1] - BASELINE[1]
    assert UNSHAPED[2] - SHAPED[2] < UNSHAPED[2] - BASELINE[2]

    # وثمانيةُ أنواعٍ مقابلَ أربعة: المقارنةُ بين اثنَي عشرَ اسمًا لا أكثر
    assert len(SHAPED_TYPES) == 8
    assert len(UNSHAPED_TYPES) == 4
    assert len(set(SHAPED_TYPES) & set(UNSHAPED_TYPES)) == 0


def test_the_effective_sample_is_four_not_a_thousand() -> None:
    """١٬٠٦٧ وقوعًا في أربعة أنواع: أربعُ مشاهدات، وتضخيمٌ ١٦٫٣×."""

    sample = ClusteredSample(observations=AFTER_THE_FILTER, clusters=4)
    assert sample.effective == 4
    assert round(float(sample.per_cluster), 1) == 266.8
    assert round(sample.inflation, 1) == 16.3

    # وعلى الثمانية يبقى التضخيمُ فوق أحدَ عشرَ ضعفًا
    assert round(ClusteredSample(AFTER_THE_FILTER, 8).inflation, 1) == 11.5

    with pytest.raises(EvaluationError, match="أقلُّ من عناقيدها"):
        ClusteredSample(observations=3, clusters=4)
    with pytest.raises(EvaluationError, match="عنقودٌ واحدٌ فأكثر"):
        ClusteredSample(observations=10, clusters=0)


def test_at_rank_two_no_more_than_half_the_symbols_carry_a_context() -> None:
    """صفرٌ للطولين ١ و٢، وثلثٌ للطول ٣، ونصفٌ للطول ٤ — فالحدُّ الأعلى نصف."""

    for length, expected in ((1, 0), (2, 0), (3, Fraction(1, 3)), (4, Fraction(1, 2))):
        assert full_context_share([length], 2) == expected

    assert full_context_share([4, 4, 4], 2) == Fraction(1, 2)  # الحدُّ الأعلى
    assert full_context_share([1, 2], 2) == 0  # والأدنى صفرٌ لا شيءَ دونه
    assert units_that_carry_no_context([1, 2, 3, 4], 2) == 2

    # وعند رتبة ١ يتّسع الحدُّ إلى ثلاثة أرباع، فالرتبتان مقياسان لا واحد
    assert full_context_share([4], 1) == Fraction(3, 4)
    assert full_context_share([4], 1) > full_context_share([4], 2)


def test_length_runs_with_the_group_so_rank_two_is_the_most_exposed() -> None:
    """أطولُ الأسماء في المجموعة غيرِ المصوغة، وأكبرُ الفروق عند رتبة ٢.

    ولا يُدَّعى أنّ الفرقَ كلَّه طول؛ بل أنّ الطولَ **لم يُثبَّت**، وأنّ الرقمَ
    الأكبرَ هو الأشدُّ تعلّقًا به. فتثبيتُ الطول فحصٌ يفصل، ولم يجرِ بعد.
    """

    # فرقُ رتبة ٢ أكبرُ من فرق رتبة ١ في المجموعتين معًا
    assert (UNSHAPED[2] - BASELINE[2]) > (UNSHAPED[1] - BASELINE[1])
    assert (SHAPED[2] - BASELINE[2]) > (SHAPED[1] - BASELINE[1])

    # ونسبةُ الاتّساع بين الرتبتين أكبرُ في غير المصوغ
    unshaped_growth = (UNSHAPED[2] - BASELINE[2]) / (UNSHAPED[1] - BASELINE[1])
    shaped_growth = (SHAPED[2] - BASELINE[2]) / (SHAPED[1] - BASELINE[1])
    assert rounds_to(unshaped_growth, 2) == Fraction("2.33")
    assert rounds_to(shaped_growth, 2) == Fraction("1.64")
    assert unshaped_growth > shaped_growth


def test_the_named_types_split_cleanly_at_rank_two() -> None:
    """ثلاثةٌ مصوغةٌ فوق الأساس بثلث بتٍّ فأقلّ، وثلاثةٌ غيرُ مصوغةٍ فوقه بأربعة."""

    shaped = {
        name: value
        for name, value in BY_TYPE_AT_RANK_TWO.items()
        if name in SHAPED_TYPES
    }
    unshaped = {
        name: value
        for name, value in BY_TYPE_AT_RANK_TWO.items()
        if name in UNSHAPED_TYPES
    }
    assert len(shaped) == len(unshaped) == 3

    over = {name: value - BASELINE[2] for name, value in shaped.items()}
    assert max(over.values()) < Fraction(4, 10)
    assert min(over.values()) > 0  # فهي **فوق** الأساس لا عنده، وإن قلّ الفرق
    assert rounds_to(min(over.values()), 4) == Fraction("0.0914")

    assert min(unshaped.values()) - BASELINE[2] > Fraction(37, 10)
    assert min(unshaped.values()) > max(shaped.values()) * 1.9  # ولا تداخلَ بينهما


def test_the_filter_redefined_the_set_rather_than_trimming_it() -> None:
    """١٠٬١٧١ ← ١٬٠٦٧: ٨٩٫٥١٪ خرجت، وذلك تعريفٌ جديدٌ لا تنقيح."""

    dropped = FIRST_RUN - AFTER_THE_FILTER
    assert dropped == 9_104
    assert (
        Partition(parts=(AFTER_THE_FILTER, dropped), declared_total=FIRST_RUN).residue
        == 0
    )
    assert rounds_to(Fraction(dropped, FIRST_RUN) * 100, 2) == Fraction("89.51")
    assert Fraction(dropped, FIRST_RUN) > Fraction(4, 5)


def test_the_headline_is_withdrawn_by_the_argument_that_precedes_it() -> None:
    """+١٫٣٦٨ فوق صفريّه ١٣٫٦٨ ضعفًا — **ولا يُنسَب إلى التعريب**.

    وسحبُه ليس رأيي: قِيل في الفقرة نفسِها «وما بقي فيها **أعلامٌ أعجميّة**…
    فلو نشرتُ الـ+١٫٣٦ **لنسبتُ إلى التعريب ما هو عن الأعلام**» — ثمّ نُشِر
    في الفقرة التالية. **والحجّةُ أقوى من الرقم الذي تليه**، فهذا موضعُها.

    ولا يُسقِط ذلك المقارنةَ المُسمّاة: الثمانيةُ والأربعةُ **أسماءُ أشياءٍ
    كلُّها** — قسطاسٌ وسجّيلٌ وإستبرقٌ وسندس — لا أعلامَ فيها. فهي المجموعةُ
    التي يتناولها الكتابُ بنصِّه، وأرقامُها (+٠٫٧٨٦٢ و+٢٫٤٦٦٥) قائمة.
    """

    assert rounds_to(HEADLINE / MATCHED_NULL, 2) == Fraction("13.68")

    # والمجموعتان غيرُ واحدة: أربعةُ أنواعٍ مُسمّاةٍ مقابلَ ١٬٠٦٧ وقوعًا
    assert len(UNSHAPED_TYPES) == 4
    assert AFTER_THE_FILTER == 1_067
    assert AFTER_THE_FILTER > len(UNSHAPED_TYPES) * 250  # فليست تلك الأربعة

    # وما لم يُسَمَّ بعدُ: أعلى أيِّ متغيّرٍ جرت المطابقة. وطولٌ أو تردّدٌ
    # يعطيان صفريّين مختلفين، والفرقُ بينهما هو الفرقُ بين خبرٍ وصدًى.
    candidates = ("الطول", "التردّد", "الطولُ والتردّدُ معًا")
    assert len(set(candidates)) == 3
