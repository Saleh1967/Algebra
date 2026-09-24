"""تسجيلٌ خَلَفٌ لخ٢: لا يُقاس عليه ما رُئي، بل **تكرارُه على نصفٍ محجوب**.

**لماذا تسجيلٌ ثانٍ لا تعديلُ الأوّل**: `9ed9eeea…` مختومٌ وقد شُغِّل،
وحكمُ خ٢ فيه «باطلُ الأساس» جزءٌ من السجلّ. وتعديلُه يمحو خبرًا صادقًا:
**أنّ ختمًا سمّى مُقابَلًا لا تحمله الشجرة**. فيبقى كما هو، ويُكتَب هذا
خَلَفًا له يُسمّيه.

`A_THRESHOLD_WRITTEN_AFTER_THE_NUMBER_IS_NOT_A_THRESHOLD`: وقد خرج مؤشّرُ
رَند المعدَّل على المدوّنة كلِّها **٠٫٥٥٧٠**. فلو كتبتُ حدًّا عليه الآن
لكنتُ أفصّل الحدَّ على مقاس رقمٍ رأيتُه — وهو عينُ ما تمنعه هذه الشجرة.
فالمسجَّلُ ههنا **ليس الرقمَ بل تكرارَه**: يُقسَم النصُّ نصفين، ويُستخرَج
التقسيمُ من الأوّل، ويُقابَل بالمُودَع **على الثاني وحدَه**. والنصفُ الثاني
لم يُنظَر إليه.

`THE_CIRCULARITY_IS_MEASURED_NOT_CONFESSED`: والاعترافُ بأنّ «السكونَ وسمٌ
يعرف التقسيم» لا يكفي — يُقاس. فيُشغَّل صفريٌّ يضع الوسمَ نفسَه في مواضعَ
**مُنتقاةٍ عشوائيًّا بعددها نفسِه**، ويُشتَرط ألّا يبلغ مؤشّرُه عُشرَ
الواحد. فإن بلغه فالمؤشّرُ يقيس كثرةَ الوسم لا موافقتَه.

`THE_COMPARISON_IS_THE_DEPOSITED_THREE_NOT_A_FIVE_WE_WROTE`: والمُقابَلُ به
**ثلاثيٌّ مُشتَقٌّ من المُودَع** وحدَه: إظهارٌ، وإدغامٌ، وما بقي. ولا
يُكتَب خماسيٌّ بيدٍ ههنا، فكتابتُه إيداعٌ والإيداعُ توقيع.
"""

from __future__ import annotations

from fractions import Fraction

from algebra.attainability import permutation_floor
from algebra.signified import Direction, Oracle, Prediction, Verdict, seal

SUPERSEDES = "9ed9eeead8cb2fa512cdde14fa9d4cca2538d4d48a8eb8035968f86604fa2673"
DISCOVERY_RAND = Fraction(557, 1_000)
"""ما خرج على المدوّنة كلِّها قبل هذا الختم؛ **اكتشافٌ لا حدّ**، ولا يُقاس عليه."""

REPLICATES = 2_000
SEED = 20_260_924
FAMILY = 5

NUN_REPLICATION = Oracle(
    name="تكرارُ استخراج تقسيم النون على نصفٍ محجوب من المصحف",
    source=(
        "المدوّنةُ المُجمَّدةُ ببصمتها، ومصدرُ ضبطها مُسمًّى؛ والتقسيمُ "
        "المُقابَلُ به مُشتَقٌّ من المُودَع وحدَه: إظهارٌ وإدغامٌ وما بقي"
    ),
    extraction=(
        "يُقسَم النصُّ نصفين بترتيب الأسطر. ويُستخرَج التقسيمُ من **النصف "
        "الأوّل وحدَه** بنصيب كلّ حرفٍ بعد نونٍ موسومةٍ بالسكون، ثمّ يُقابَل "
        "بالمُودَع **على النصف الثاني**. ولا يُنظَر في الثاني قبل ذلك"
    ),
)

PREDICTIONS = (
    Prediction(
        identifier="ص١ التكرارُ على النصف المحجوب",
        statistic=(
            "مؤشّرُ رَند المعدَّل بين التقسيم المُستخرَج من النصف الأوّل "
            "والمُودَع الثلاثيّ، محسوبًا على النصف الثاني"
        ),
        threshold=Fraction(40, 100),
        direction=Direction.AT_LEAST,
        falsifies=(
            "أنّ الاستخراجَ ظاهرةٌ في المدوّنة؛ فدونه هو قسمةُ نصفٍ واحدٍ " "لا تعبر إلى غيره"
        ),
    ),
    Prediction(
        identifier="ص٢ الصفريُّ لا يبلغ عُشرَ الواحد",
        statistic=(
            "أعلى مؤشّرِ رَند يبلغه وسمٌ موضوعٌ عشوائيًّا بالعدد نفسِه " "على المواضع نفسِها"
        ),
        threshold=Fraction(10, 100),
        direction=Direction.AT_MOST,
        falsifies=(
            "قابليّةَ قراءة ص١؛ فصفريٌّ يبلغ عُشرَ الواحد يعني أنّ المؤشّرَ "
            "يقيس كثرةَ الوسم لا موافقتَه"
        ),
    ),
    Prediction(
        identifier="ص٣ صدارةُ الإظهار مُسترجَعةٌ لا مفترضة",
        statistic=(
            "عددُ حروف الإظهار المُودَعةِ الواقعةِ في أعلى خمسةٍ بالنصيب " "في النصف الأوّل"
        ),
        threshold=Fraction(5),
        direction=Direction.AT_LEAST,
        falsifies=(
            "أنّ الاسترجاعَ عن الإظهار؛ فدونه يكون المؤشّرُ عن مجموعةٍ " "أخرى وقد نُسِب إليه"
        ),
    ),
    Prediction(
        identifier="ص٤ مقامُ الملتقى منشورٌ لكلّ نصف",
        statistic="أقلُّ عددِ ملتقًى موسومٍ بالسكون في نصفَي المدوّنة",
        threshold=Fraction(200),
        direction=Direction.AT_LEAST,
        falsifies=("قابليّةَ قراءة النصف الذي وقع دونه؛ ويُعلَن ضعيفَ الشهادة"),
    ),
    Prediction(
        identifier="ص٥ مصدرُ الضبط مُسمًّى",
        statistic="عددُ المصادر المُسمّاةِ في ختم العمود الذي يُقرأ منه السكون",
        threshold=Fraction(1),
        direction=Direction.AT_LEAST,
        falsifies=(
            "نسبةَ النتيجة إلى «العربيّة»؛ والمصدرُ غيرُ الرواية، ويُطبَعان " "حقلين لا حقلًا"
        ),
    ),
)

NUN_SEAL = seal(NUN_REPLICATION, PREDICTIONS)

SEALED_DIGEST = "85f59f23c39d3ded9d459a332c7df7587f13891d7e54d4fdad40f63dfb51a160"


def test_the_seal_is_stable_and_names_the_one_it_succeeds() -> None:
    """ختمٌ خَلَفٌ لا بديل: الأوّلُ يبقى بحكمه، وهذا يُسمّيه."""

    assert NUN_SEAL == SEALED_DIGEST
    assert len(NUN_SEAL) == 64
    assert NUN_SEAL != SUPERSEDES
    assert len(SUPERSEDES) == 64


def test_the_discovery_figure_is_not_the_threshold() -> None:
    """٠٫٥٥٧٠ اكتشافٌ رُئي، و٠٫٤٠ حدٌّ على **قياسٍ آخرَ لم يُرَ** بعدُ."""

    assert DISCOVERY_RAND > PREDICTIONS[0].threshold
    # والمقيسُ في ص١ غيرُ المقيس في الاكتشاف: نصفٌ محجوبٌ لا مدوّنةٌ كاملة
    assert "على النصف الثاني" in NUN_REPLICATION.extraction
    assert "محجوب" in PREDICTIONS[0].identifier


def test_the_second_condition_runs_the_other_way() -> None:
    """ص٢ اتّجاهُه «لا يجاوز»: صفريٌّ عالٍ يُسقِط القراءةَ لا يؤيّدها."""

    second = PREDICTIONS[1]
    assert second.direction is Direction.AT_MOST
    assert second.verdict(Fraction(5, 100)) is Verdict.MET
    assert second.verdict(Fraction(20, 100)) is Verdict.FALSIFIED


def test_the_family_is_five_and_the_floor_is_the_machine() -> None:
    """خمسةُ شروطٍ مُسمّاةٌ قبل العدّ، وأرضيّةُ ألفين ١/٢٠٠١."""

    assert FAMILY == len(PREDICTIONS) == 5
    assert len({one.identifier for one in PREDICTIONS}) == FAMILY
    assert permutation_floor(REPLICATES) == Fraction(1, 2_001)
    assert SEED == 20_260_924
