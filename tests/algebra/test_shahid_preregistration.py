"""تسجيلُ «الشاهد» على المصحف مختومًا قبل أن تصل مادّتُه.

**حالُ هذا الملفّ**: لا رقمَ مقيسٌ فيه، ولا بايتَ مدوّنةٍ يُقرَأ. يحمل
الأوراكلَ مُعلَنًا، وخمسةَ شروطٍ بحدودٍ عدديّة، وبصمتَها. ويُودَع **قبل**
أن يُشغَّل الأنبوبُ على المصحف — وقد أُودِع وأرقامُ النموذج الأوّليّ على
النثر معروفةٌ، وذلك مقصود: الحدودُ تُشتَقّ من مدوّنةٍ ثمّ تُختبَر على أخرى،
ولا تُبدَّل بعد النظر. وتبديلُها يُعرَف بتغيُّر البصمة.

`THE_PROTOTYPE_SETS_THE_EXPECTATION_AND_THE_SEAL_SETS_THE_THRESHOLD`: أعطى
النموذجُ على النثر نصيبًا من المتاح قدرُه ٥٢٫٦٪. والحدُّ المسجَّلُ ههنا
**٣٠٪** — دونه بمسافةٍ مُعلَنة، لأنّ المصحفَ مدوّنةٌ أخرى ولأنّ حدًّا
مفصَّلًا على مقاس رقمٍ رآه صاحبُه ليس حدًّا. ولو خرج ٤٠٪ لكان الشرطُ
متحقّقًا والدعوى أضعفَ ممّا في النثر — والأمران يُنشَران معًا.

`THE_CLUSTER_IS_THE_NODE_AND_THE_EDGE_IS_NOT_AN_OBSERVATION`: وبندُ الإعلان
ههنا ليس تجميلًا: عُدَّت حوافُّ الجيرة مشاهداتٍ مستقلّةً في النموذج الأوّليّ،
وحدُّ تعادل `z = 19.6` **مئةُ حافّةٍ للعقدة**. فيُعلَن العددُ ويُنشَر `z`
مقسومًا على جذره، أو لا يُنشَر.

`THE_SIGNATURE_IS_REGISTERED_AS_A_JOINT_NOT_AS_TWO_MARGINS`: وشرطُ ش٥ يمنع
أن يُقرأ كسبُ التنبّؤ من هامشين: يُشغَّل على الجدول المشترَك (خمسٍ وعشرين
خانة) ويُنشَر الفرقُ بين القراءتين. فإن ذاب الكسبُ فالجيرةُ لا تعرف بعضَها
خارج محلّ اللقاء، وذلك يُسقِط ت٣ لا يُضعِفه.

`THE_LEXICON_TAG_IS_A_NARRATION_AND_IS_NEVER_BUILT_UPON`: والأوسمةُ من
معجم الاستعمال **تُعلَّق على الفرق بعد استخراجها**، ولا تدخل في استخراجها
ولا في أيّ شرطٍ من هذه الخمسة. وهذا مكتوبٌ في الأوراكل نفسِه، فإن دخلت
تبدّلت البصمة.
"""

from __future__ import annotations

from fractions import Fraction

from algebra.attainability import (
    governing_floor,
    permutation_floor,
)
from algebra.signified import (
    Direction,
    Oracle,
    Prediction,
    Verdict,
    seal,
)

SHAHID = Oracle(
    name="فرقُ الإحلال على المصحف، مستخرَجةً من الرسم وحدَه",
    source=(
        "عمودُ `surface` من المحاذاة الكاملة بمفتاح (سورة:آية:كلمة)، "
        "وإغلاقُه مُعلَنٌ قبل التشغيل؛ ولا مدخلَ غيرُه"
    ),
    extraction=(
        "العقدةُ لفظٌ مشهود، والحافّةُ تقاسُمُ إطارٍ محليٍّ واحدٍ (السابقُ "
        "واللاحقُ أنفسُهما)، والفرقةُ تجمّعُ جيرةٍ عند تشابه التوقيع. "
        "والتوقيعُ يُحسَب على الجدول المشترَك لصنفَي السابق واللاحق. "
        "وأوسمةُ المعجم تُعلَّق على الفرق بعد استخراجها ولا تدخل فيه"
    ),
)

REPLICATES = 2_000
SEED = 20_260_924
FAMILY = 5

PREDICTIONS = (
    Prediction(
        identifier="ش١ انتقالُ الفرق إلى النصف المحجوب",
        statistic=(
            "نصيبُ ما فوق الصفريّ من المتاح: (المرصودُ − الصفريّ) ÷ (١ − الصفريّ)، "
            "لتشابه توقيعات الجيران في نصف المدوّنة المحجوب"
        ),
        threshold=Fraction(30, 100),
        direction=Direction.AT_LEAST,
        falsifies=(
            "أنّ الفرقَ وضعٌ قائمٌ في النصّ؛ فدونه هي قسمةُ نصفٍ واحدٍ " "لا تعبر إلى غيره"
        ),
    ),
    Prediction(
        identifier="ش٢ الحوافُّ للعقدة مُعلَنة",
        statistic="عددُ حوافّ الجيرة مقسومًا على عدد العقد، ويُنشَر مع كلّ z",
        threshold=Fraction(1),
        direction=Direction.AT_LEAST,
        falsifies="لا شيء؛ وهو بندُ إعلانٍ يُنشَر مع كلّ رقمٍ أعلاه",
    ),
    Prediction(
        identifier="ش٣ الصنفُ الجامعُ لا يبتلع الجيرة",
        statistic="نصيبُ «سواه» من مواضع السابق واللاحق مجتمعةً",
        threshold=Fraction(50, 100),
        direction=Direction.AT_MOST,
        falsifies=(
            "أنّ التوقيعَ عشرةُ أبعاد؛ فإن جاوزها فأكثرُ الجيرة بتّةٌ واحدةٌ "
            "اسمُها «ليس من الأربعة»"
        ),
    ),
    Prediction(
        identifier="ش٤ مقامٌ منشورٌ لكلّ فرقة",
        statistic="عددُ العقد في أصغر فرقةٍ تدخل القراءة",
        threshold=Fraction(12),
        direction=Direction.AT_LEAST,
        falsifies="قابليّةَ قراءة تلك الفرقة؛ ودونه تُعلَن ضعيفةَ الشهادة",
    ),
    Prediction(
        identifier="ش٥ الكسبُ من الاقتران لا من الهامشين",
        statistic=(
            "الفرقُ بين كسب التنبّؤ محسوبًا على الجدول المشترَك (٢٥ خانة) "
            "وكسبِه على الهامشين (١٠ أبعاد)"
        ),
        threshold=Fraction(1, 100),
        direction=Direction.AT_LEAST,
        falsifies=(
            "دعوى «الجيرانُ يعرفون بعضَهم خارج محلّ اللقاء»؛ فإن ذاب الفرقُ "
            "فالكسبُ من الهامشين وقد حُسِبا مرّتين"
        ),
    ),
)

SHAHID_SEAL = seal(SHAHID, PREDICTIONS)

SEALED_DIGEST = "df8fe34a88bbf641e554f2ca923ac17f8c4c355691a109261bbe3a9b8c06ba07"
"""البصمةُ مكتوبةً في المتن: فأيُّ تبديلٍ في الأوراكل أو الشروط يُسقِط الفحص."""

PROTOTYPE_HEADROOM = Fraction("0.526")
"""ما أعطاه النموذجُ على النثر؛ منقولٌ للمقارنة، وليس حدًّا ولا مقيسًا ههنا."""


def test_the_seal_is_stable_and_a_moved_threshold_changes_it() -> None:
    """بصمةٌ ثابتةٌ، وتبديلُ حدٍّ بعد النظر يُعرَف بتغيُّرها."""

    assert SHAHID_SEAL == SEALED_DIGEST
    assert len(SHAHID_SEAL) == 64
    assert set(SHAHID_SEAL) <= set("0123456789abcdef")
    assert SHAHID_SEAL == seal(SHAHID, PREDICTIONS)

    easier = (
        Prediction(
            identifier=PREDICTIONS[0].identifier,
            statistic=PREDICTIONS[0].statistic,
            threshold=Fraction(10, 100),
            direction=PREDICTIONS[0].direction,
            falsifies=PREDICTIONS[0].falsifies,
        ),
        *PREDICTIONS[1:],
    )
    assert seal(SHAHID, easier) != SHAHID_SEAL


def test_the_threshold_sits_below_the_prototype_by_a_declared_margin() -> None:
    """٣٠٪ مسجَّلةٌ و٥٢٫٦٪ مرصودةٌ على مدوّنةٍ أخرى — والمسافةُ مُعلَنةٌ لا مخفيّة."""

    registered = PREDICTIONS[0].threshold
    assert registered == Fraction(30, 100)
    assert registered < PROTOTYPE_HEADROOM

    # ولو خرج ٤٠٪ لتحقّق الشرطُ ولكانت الدعوى أضعفَ من النثر: الأمران يُنشَران
    assert PREDICTIONS[0].verdict(Fraction(40, 100)) is Verdict.MET
    assert Fraction(40, 100) < PROTOTYPE_HEADROOM
    assert PREDICTIONS[0].verdict(Fraction(29, 100)) is Verdict.FALSIFIED


def test_the_catch_all_condition_runs_the_other_way() -> None:
    """ش٣ اتّجاهُه «لا يجاوز»: صنفٌ جامعٌ يبتلع الجيرةَ يُسقِط التوقيعَ لا يُقوّيه."""

    assert PREDICTIONS[2].direction is Direction.AT_MOST
    assert PREDICTIONS[2].verdict(Fraction(45, 100)) is Verdict.MET
    assert PREDICTIONS[2].verdict(Fraction(70, 100)) is Verdict.FALSIFIED

    at_most = [one for one in PREDICTIONS if one.direction is Direction.AT_MOST]
    assert len(at_most) == 1


def test_the_family_is_five_and_declared_before_the_count() -> None:
    """خمسةُ شروطٍ مُسمّاةٌ قبل التشغيل، وبذرةٌ مكتوبةٌ تجعله مُعادًا لا مُقلَّدًا."""

    assert FAMILY == len(PREDICTIONS) == 5
    assert len({one.identifier for one in PREDICTIONS}) == FAMILY
    assert SEED == 20_260_924

    announcements = [one for one in PREDICTIONS if one.falsifies.startswith("لا شيء")]
    assert len(announcements) == 1  # ش٢ بندُ إعلانٍ لا شرطُ سقوط


def test_the_governing_floor_is_computed_over_nodes_not_edges() -> None:
    """أرضيّةُ المادّة تُحسَب على العقد؛ فإن كانت العقدُ كثيرةً حكمت أرضيّةُ الآلة."""

    machine = permutation_floor(REPLICATES)
    assert machine == Fraction(1, 2_001)

    # ومع عقدٍ بالآلاف تصير أرضيّةُ المادّة أدنى من أرضيّة الآلة، فتحكم الآلةُ
    nodes = 4_000
    assert governing_floor(nodes // 2, nodes, REPLICATES) == machine

    # وهذا عكسُ حال التعريب: خمسةٌ هناك، فحكمت المادّةُ بـ١/١٠
    assert governing_floor(2, 5, REPLICATES) == Fraction(1, 10)


def test_the_lexicon_tags_enter_no_condition() -> None:
    """الأوسمةُ رواية: لا تدخل استخراجًا ولا شرطًا، وذلك مكتوبٌ في الأوراكل."""

    assert "تُعلَّق على الفرق بعد استخراجها ولا تدخل فيه" in SHAHID.extraction
    for one in PREDICTIONS:
        assert "معجم" not in one.statistic
        assert "وسم" not in one.statistic
