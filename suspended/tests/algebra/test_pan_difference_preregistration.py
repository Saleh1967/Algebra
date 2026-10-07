"""الختمُ الرابع: مئينٌ بدل الأقصى، وحدودٌ من الصفريّ لا من رقمٍ رُئي.

**تسجيلٌ محض: لا رقمَ مقيسٌ فيه.** وأوراكلُه يستشهد بالسجلّ البايتيّ
`30c7e393…` وحدَه.

`THE_THREE_DEFECTS_THIS_SEAL_ANSWERS`: يجمع إصلاحَ ثلاثةٍ ظهرت بتشغيل
`6a584a5a…`:

1. **الأقصى سُئِل مسلكَ مئين.** كان الحدُّ على «أعلى ألفي سحبة»، والأقصى
   مرتفعٌ بالبناء. فصار على **المئين الخامس والتسعين**.
2. **حدُّ التكرار كان رقمًا مُخمَّنًا** (٠٫٣٥) فسقط عند ٠٫٢٨٥٣. فلا يُكتَب
   ههنا رقمٌ مُخمَّنٌ ثانيةً، ولا رقمٌ رُئي: **الحدُّ من الصفريّ نفسِه** —
   أن يعلوَ المرصودُ مئينَه الخامسَ والتسعين. فالبارُّ مشتقٌّ من المادّة لا
   من ظنّي.
3. **فرقُ الكفّتين كان بندَ إعلان** فلا يسقط بشيء. فصار **شرطًا يُقاس**
   بصفريٍّ يخلط العلامات.

`THE_DIRECTION_OF_THE_SPLIT_WAS_NEVER_NAMED_AND_NOW_IT_IS_BOTH`: وقُسِم
النصُّ نصفين فتُعُلِّم من الأوّل واختُبِر على الثاني. ولم يُسمَّ لِمَ هذا
الاتّجاهُ دون عكسه. فيُشتَرَط ههنا **الاتّجاهان معًا**، ويُشتَرَط
**تقاربُهما**: فارقٌ كبيرٌ بينهما يعني أنّ النصفين ليسا من مادّةٍ واحدة،
لا أنّ أحدَهما أصدق.

`THE_DENOMINATORS_MUST_CLOSE_INCLUDING_WHAT_THE_CUT_TAKES`: وموضعٌ واحدٌ
ضاع على القطع في التشغيل السابق (١٦٬٩٥٦ + ١٠٬٤٢٥ = ٢٧٬٣٨١ والكلُّ
٢٧٬٣٨٢). فيُشتَرَط أن **تُغلِق المقاماتُ**: نصفان + المفقودُ على القطع =
الكلّ. والمفقودُ يُعَدّ ولا يُطرَح صامتًا.
"""

from __future__ import annotations

from fractions import Fraction

from algebra.attainability import permutation_floor
from algebra.signified import Direction, Oracle, Prediction, Verdict, seal

CORPUS_RECORD = "30c7e393eff12641e27802dbfc38c51e7171ed873bfd2f78dc889de2fad7a359"
SUPERSEDED = "6a584a5a1254329445f8a8c5dcc5b52303155fe9c13cafb9dd844a3abf36c1d3"

REPLICATES = 2_000
SEED = 20_260_924
FAMILY = 5
QUANTILE = Fraction(95, 100)

PAN_DIFFERENCE = Oracle(
    name="فرقُ كفّتَي الرسم والضبط، وتكرارُ التقسيم في الاتّجاهين",
    source=(
        f"السجلُّ البايتيُّ {CORPUS_RECORD[:16]}… وحدَه: المدوّنةُ ببصمتها "
        "وطولها وأسطرها، ومصدرُها الموقَّع، وروايتُها بمنزلتها وعددِ فوارقها"
    ),
    extraction=(
        "التباينُ داخلَ مواضع النون كما في سابقه. ويُقسَم النصُّ نصفين "
        "فيُتعلَّم من كلٍّ ويُختبَر على الآخر — **اتّجاهان لا اتّجاه**. "
        "وكفّةُ الضبط صفوفُها على الرمز (حرفٌ + صنفُ علامته)، وصفريُّها "
        "**خلطُ أصناف العلامات** على مواضعها مع بقاء الحروف. وسياسةُ الجوار "
        "تُسمّى في المخرَج: داخلَ الكلمة أم عابرًا حدَّها"
    ),
)

PREDICTIONS = (
    Prediction(
        identifier="م١ المئينُ لا الأقصى",
        statistic=(
            "المئينُ الخامسُ والتسعون لمؤشّر رَند تحت تبديل وسمَي الموسومة " "وغيرِ الموسومة"
        ),
        threshold=Fraction(10, 100),
        direction=Direction.AT_MOST,
        falsifies=(
            "أنّ المقياسَ سالمٌ من أثر الوسم؛ ومئينٌ مرتفعٌ يعني العطلَ في "
            "المقياس، بخلاف أقصى سحبةٍ فهو مرتفعٌ بالبناء"
        ),
    ),
    Prediction(
        identifier="م٢ الاتّجاهان فوق مئين صفريّهما",
        statistic=(
            "عددُ اتّجاهَي التعلّم اللذين يعلو مؤشّرُهما المئينَ الخامسَ " "والتسعين لصفريّهما"
        ),
        threshold=Fraction(2),
        direction=Direction.AT_LEAST,
        falsifies=(
            "أنّ الاسترجاعَ ظاهرةٌ في المادّة؛ والبارُّ ههنا **من الصفريّ** "
            "لا من رقمٍ مُخمَّنٍ ولا من رقمٍ رُئي"
        ),
    ),
    Prediction(
        identifier="م٣ الاتّجاهان متقاربان",
        statistic="القيمةُ المطلقةُ لفرق مؤشّرَي الاتّجاهين",
        threshold=Fraction(10, 100),
        direction=Direction.AT_MOST,
        falsifies=(
            "أنّ النصفين من مادّةٍ واحدة؛ وفارقٌ كبيرٌ يعني اختلافَ النصفين " "لا صدقَ أحدهما"
        ),
    ),
    Prediction(
        identifier="م٤ فرقُ الكفّتين يُقاس لا يُعلَن",
        statistic=(
            "نصيبُ كفّة الضبط من المتاح مطروحًا منه المئينُ الخامسُ والتسعون "
            "لصفريّ خلطِ أصناف العلامات"
        ),
        threshold=Fraction(0),
        direction=Direction.AT_LEAST,
        falsifies=(
            "أنّ للضبط أثرًا في تماسك المخارج؛ فدونه يكون ارتفاعُ كفّة "
            "الضبط أثرَ توسيعِ الرمز لا أثرَ الضبط"
        ),
    ),
    Prediction(
        identifier="م٥ المقاماتُ تُغلِق والسياسةُ تُسمّى",
        statistic=(
            "عددُ الإغلاقات المفحوصة: نصفان زائدَ المفقودِ على القطع يساوي "
            "الكلّ، وسياستا الجوار منشورتان للرسم"
        ),
        threshold=Fraction(2),
        direction=Direction.AT_LEAST,
        falsifies=(
            "قابليّةَ قراءة ما سبقه؛ فمقامٌ لا يُغلِق أو سياسةٌ لا تُسمّى "
            "تجعل الرقمَ عن مجالٍ لم يُعدَّد"
        ),
    ),
)

PAN_SEAL = seal(PAN_DIFFERENCE, PREDICTIONS)

SEALED_DIGEST = "81884f7ea02235c37ef6edac5d555418924e9f0acd54bf1793fb5d2afb12e8eb"


def test_the_seal_is_stable_and_names_the_one_it_repairs() -> None:
    """ختمٌ رابعٌ يُسمّي سابقَه ولا يمحوه؛ وحكمُ ذاك باقٍ بسقوطه."""

    assert PAN_SEAL == SEALED_DIGEST
    assert len(PAN_SEAL) == 64
    assert PAN_SEAL != SUPERSEDED and len(SUPERSEDED) == 64
    assert CORPUS_RECORD[:16] in PAN_DIFFERENCE.source


def test_the_first_condition_asks_a_quantile_not_a_maximum() -> None:
    """م١ على المئين؛ والأقصى مرتفعٌ بالبناء فلا يُسأل مسلكَ مئين."""

    first = PREDICTIONS[0]
    assert first.direction is Direction.AT_MOST
    assert "المئينُ الخامسُ والتسعون" in first.statistic
    assert "أقصى" not in first.statistic
    assert first.verdict(Fraction(9, 100)) is Verdict.MET
    assert first.verdict(Fraction(30, 100)) is Verdict.FALSIFIED


def test_the_second_condition_takes_its_bar_from_the_null() -> None:
    """البارُّ من الصفريّ لا من ظنّي: عددُ الاتّجاهات التي تعلو مئينَها."""

    second = PREDICTIONS[1]
    assert "المئينَ الخامسَ" in second.statistic
    assert second.verdict(Fraction(2)) is Verdict.MET
    assert second.verdict(Fraction(1)) is Verdict.FALSIFIED
    # ولا رقمَ مُخمَّنٌ ولا رقمٌ رُئي في أيّ حدٍّ من الخمسة
    joined = " ".join(str(one.threshold) for one in PREDICTIONS)
    assert "0.35" not in joined and "0.2853" not in joined


def test_the_pan_difference_became_a_condition_with_a_null() -> None:
    """م٤ يُقاس بصفريٍّ يخلط العلامات، فلم يعد بندَ إعلانٍ لا يسقط."""

    fourth = PREDICTIONS[3]
    assert "خلطِ أصناف العلامات" in fourth.statistic
    assert fourth.verdict(Fraction(1, 100)) is Verdict.MET
    assert fourth.verdict(Fraction(-1, 100)) is Verdict.FALSIFIED

    announcements = [one for one in PREDICTIONS if one.falsifies.startswith("لا شيء")]
    assert announcements == []  # ولا بندَ إعلانٍ في هذا الختم ألبتّة


def test_the_family_is_five_and_the_floor_is_the_machine() -> None:
    """خمسةٌ مُسمّاةٌ قبل العدّ، وأرضيّةُ ألفين ١/٢٠٠١، والمئينُ مُعلَن."""

    assert FAMILY == len(PREDICTIONS) == 5
    assert len({one.identifier for one in PREDICTIONS}) == FAMILY
    assert permutation_floor(REPLICATES) == Fraction(1, 2_001)
    assert QUANTILE == Fraction(95, 100)
    assert SEED == 20_260_924
