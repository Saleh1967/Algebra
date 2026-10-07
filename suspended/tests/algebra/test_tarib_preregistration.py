"""تسجيلٌ مختومٌ قبل النظر: العددُ الذي يفصل التعريبَ عن الندرة والطول.

**حالُ هذا الملفّ**: لا رقمَ مقيسٌ فيه. يحمل **الأوراكلَ مُعلَنًا** و**خمسةَ
شروطٍ بحدودٍ عدديّة** و**بصمتَها**، ويُودَع **قبل** أن يُشغَّل القياس. فإن جاء
بعدُ فحُكمُه عليه، ولا تُبدَّل الحدودُ لتوافقَه — وتبديلُها يُعرَف بتغيُّر
البصمة.

`THE_ONE_NUMBER_THAT_SEPARATES_TWO_EXPLANATIONS`: قيل إنّ المعرَّبَ غيرَ
المصوغ أعلى مفاجأةً من الأصيل بـ**+١٫٧١** بتّ. ولذلك تفسيران لا ثالثَ لهما
ههنا: **أنّ الصياغةَ تركت أثرًا**، أو **أنّ الدخيلَ نادرٌ وطويلٌ فحسب**. ولا
يفصلهما رقمُ دقّةٍ واحد؛ يفصلهما **صفريٌّ مطابقٌ في الطول والتردّد**. فإن بقي
الفارقُ بعد المطابقة فالأوّل، وإن ذاب فالثاني.

`THE_MATCHING_VARIABLE_IS_NAMED_BEFORE_THE_RUN_NOT_AFTER`: و«صفريٌّ مطابق»
عبارةٌ تحتمل ثلاثةً: مطابقةً في الطول، أو في التردّد، أو فيهما معًا. وثلاثتُها
تعطي ثلاثةَ أرقام. فيُسمّى المتغيَّرُ **قبل** التشغيل، ويُشغَّل الثلاثةُ
جميعًا ويُنشَر الثلاثة — لا يُختار أحدُها بعد رؤيته.

`THE_LOAD_BEARING_CONTRAST_IS_INSIDE_THE_LOANS`: والمقارنةُ المسجَّلةُ ههنا
**بين المعرَّبات أنفسِها** — مصوغٌ مقابلَ غيرِ مصوغ — لا بين المعرَّب والأصيل.
إذ الدخولُ مشترَكٌ بين المجموعتين فيسقط ما يشتركان فيه، والصياغةُ وحدَها
تفترق. وهذا هو الشرطُ الذي تُحمَل عليه دعوى الكتاب.

`THE_PROPER_NAMES_ARE_OUT_BY_THE_BOOK_S_OWN_WORD`: وتُخرَج الأعلامُ الأعجميّة
قبل العدّ، لا لأنّي أستبعدها بل لأنّ الكتابَ يُخرجها: «التعريبُ خاصٌّ بأسماء
الأشياء». وإخراجُها **شرطُ تشغيلٍ مسجَّلٌ ههنا**، لا مصفاةٌ تُضاف بعد أن
يُرى الرقم.

`A_SIXTY_REPLICATE_DESIGN_IS_REFUSED_HERE`: وأرضُ التصميم تُسجَّل: ألفان
تكرارًا، فأدنى `p` تبلغها **١/٢٠٠١**. ولا يُنشَر رقمٌ أصغرُ منها ولو أعطاه
حسابُ السويّة — وذلك درسُ الفصل الحادي والستّين مُطبَّقًا **قبل** القياس لا
بعده.
"""

from __future__ import annotations

from fractions import Fraction

import pytest

from algebra.attainability import permutation_floor
from algebra.signified import (
    Direction,
    Oracle,
    Prediction,
    SignifiedError,
    Verdict,
    seal,
)

TARIB = Oracle(
    name="المعرَّباتُ في المصحف، مقسومةً بوسم الجذر",
    source=(
        "المحاذاةُ الكاملةُ (٧٧٬٤٢٨ رمزًا) مع وسم QAC الصرفيّ؛ والقائمةُ "
        "المرجعيّةُ «المهذَّب فيما وقع في القرآن من المعرَّب» للسيوطيّ"
    ),
    extraction=(
        "يُقسَم المعرَّبُ قسمين بوسم QAC وحدَه: ما أُعطيَ جذرًا وقالبًا، وما "
        "لم يُعطَ. وتُخرَج الأعلامُ الأعجميّةُ بوسم QAC نفسِه لا بقائمةٍ "
        "باليد. وتُخرَج المبنيّاتُ كذلك. والمقياسُ مفاجأةُ سلسلةٍ بالبتّ "
        "لكلّ وحدة، برتبةٍ مُعلَنةٍ واحدة"
    ),
)

REPLICATES = 2_000
SEED = 20_260_924
FAMILY = 5

MATCHING_VARIABLES: tuple[str, ...] = ("الطول", "التردّد", "الطولُ والتردّدُ معًا")
"""متغيّراتُ المطابقة الثلاثة؛ تُشغَّل كلُّها ويُنشَر الثلاثة."""

PREDICTIONS = (
    Prediction(
        identifier="ع١ أثرُ الصياغة بعد مطابقة الطول",
        statistic=(
            "فارقُ المفاجأة بين المعرَّب غيرِ المصوغ والمعرَّب المصوغ، "
            "بالبتّ للوحدة، على صفريٍّ مطابقٍ في الطول"
        ),
        threshold=Fraction(30, 100),
        direction=Direction.AT_LEAST,
        falsifies="أنّ للصياغة أثرًا يزيد على أثر الطول وحدَه",
    ),
    Prediction(
        identifier="ع٢ أثرُ الصياغة بعد مطابقة التردّد",
        statistic=("الفارقُ نفسُه على صفريٍّ مطابقٍ في تردّد الوقوع"),
        threshold=Fraction(30, 100),
        direction=Direction.AT_LEAST,
        falsifies="أنّ للصياغة أثرًا يزيد على أثر الندرة وحدَها",
    ),
    Prediction(
        identifier="ع٣ أثرُ الصياغة بعد مطابقتهما معًا",
        statistic="الفارقُ نفسُه على صفريٍّ مطابقٍ في الطول والتردّد معًا",
        threshold=Fraction(20, 100),
        direction=Direction.AT_LEAST,
        falsifies=(
            "دعوى الكتاب بتمامها: إن ذاب الفارقُ ههنا فالتعريبُ عند هذا "
            "المقياس ندرةٌ وطولٌ لا صياغة"
        ),
    ),
    Prediction(
        identifier="ع٤ مقامٌ منشورٌ لكلّ خانة",
        statistic="عددُ الأنواع في أصغر خانةٍ من خانات المقارنة",
        threshold=Fraction(12),
        direction=Direction.AT_LEAST,
        falsifies="قابليّةَ القراءة أصلًا؛ فدونه يُعلَن القياسُ ضعيفَ الشهادة",
    ),
    Prediction(
        identifier="ع٥ العنقدةُ معلَنة",
        statistic=(
            "نسبةُ الوقوعات إلى الأنواع في المجموعة غير المصوغة، "
            "مضروبًا بها اتّساعُ الخطأ المعياريّ"
        ),
        threshold=Fraction(1),
        direction=Direction.AT_LEAST,
        falsifies="لا شيء؛ وهو بندُ إعلانٍ يُنشَر مع كلّ رقمٍ أعلاه",
    ),
)

TARIB_SEAL = seal(TARIB, PREDICTIONS)


def test_the_seal_is_stable_and_named() -> None:
    """بصمةُ التسجيل ثابتةٌ، وتبديلُ حدٍّ بعد النظر يُعرَف بتغيُّرها."""

    assert len(TARIB_SEAL) == 64
    assert TARIB_SEAL == seal(TARIB, PREDICTIONS)

    moved = (
        Prediction(
            identifier=PREDICTIONS[0].identifier,
            statistic=PREDICTIONS[0].statistic,
            threshold=Fraction(10, 100),  # حدٌّ أسهل
            direction=PREDICTIONS[0].direction,
            falsifies=PREDICTIONS[0].falsifies,
        ),
        *PREDICTIONS[1:],
    )
    assert seal(TARIB, moved) != TARIB_SEAL


def test_the_matching_variable_is_enumerated_not_chosen() -> None:
    """ثلاثةُ متغيّراتٍ مُسمّاة، وثلاثةُ شروطٍ تقابلها — ولا يُختار واحد."""

    assert len(MATCHING_VARIABLES) == 3
    assert len(set(MATCHING_VARIABLES)) == 3

    matched = [one for one in PREDICTIONS if "مطابق" in one.statistic]
    assert len(matched) == 3
    assert len({one.identifier for one in matched}) == 3

    # والحدُّ في الثالث أدنى، لأنّ ضبطَ متغيّرين يترك أثرًا أصغر
    assert PREDICTIONS[2].threshold < PREDICTIONS[0].threshold
    assert PREDICTIONS[2].threshold < PREDICTIONS[1].threshold


def test_the_contrast_is_inside_the_loans_not_against_the_native() -> None:
    """المقارنةُ مصوغٌ مقابلَ غيرِ مصوغ؛ فالدخولُ مشترَكٌ ويسقط."""

    for one in PREDICTIONS[:3]:
        assert "المصوغ" in one.statistic or "الفارقُ نفسُه" in one.statistic
    assert "غيرِ المصوغ والمعرَّب المصوغ" in PREDICTIONS[0].statistic
    assert "الأصيل" not in PREDICTIONS[0].statistic


def test_the_third_prediction_carries_the_whole_claim() -> None:
    """ع٣ وحدَه يُسقِط دعوى الكتاب عند هذا المقياس إن ذاب فارقُه."""

    assert "بتمامها" in PREDICTIONS[2].falsifies
    assert "ندرةٌ وطولٌ لا صياغة" in PREDICTIONS[2].falsifies

    # ولا يُسقِط غيرُه الدعوى كلَّها: الأوّلان يُسقِطان تفسيرًا واحدًا
    whole = [one for one in PREDICTIONS if "بتمامها" in one.falsifies]
    assert len(whole) == 1


def test_the_design_floor_is_registered_before_the_measurement() -> None:
    """ألفان تكرارًا ⇒ أدنى `p` = ١/٢٠٠١؛ ولا يُنشَر أصغرُ منها."""

    floor = permutation_floor(REPLICATES)
    assert floor == Fraction(1, 2_001)
    assert round(float(floor), 4) == 0.0005

    # وستّون تكرارًا مردودةٌ ههنا: أرضُها أعلى بأكثر من ثلاثين ضعفًا
    assert permutation_floor(60) / floor > 32


def test_the_verdicts_are_derived_from_the_thresholds_not_written() -> None:
    """الحكمُ يُشتَقّ من الحدّ والاتّجاه؛ ولا يُكتَب «تحقّق» بجانب رقم."""

    first = PREDICTIONS[0]
    assert first.direction is Direction.AT_LEAST
    assert first.verdict(Fraction(40, 100)) is Verdict.MET
    assert first.verdict(Fraction(20, 100)) is Verdict.FALSIFIED
    assert first.verdict(first.threshold) is Verdict.MET

    with pytest.raises(SignifiedError):
        seal(TARIB, ())


def test_the_family_size_is_declared_before_the_count() -> None:
    """خمسةُ شروطٍ مُعلَنةٌ قبل العدّ، فلا يُضاف سادسٌ بعد رؤية الأرقام."""

    assert FAMILY == len(PREDICTIONS) == 5
    assert len({one.identifier for one in PREDICTIONS}) == FAMILY
    assert SEED == 20_260_924  # وبذرةٌ مكتوبةٌ تجعل التشغيلَ مُعادًا لا مُقلَّدًا
