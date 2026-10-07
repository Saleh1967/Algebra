"""التسجيلُ الثالث: مقياسٌ لا تخدعه الندرة، ومُقابَلٌ مُودَعٌ لا مكتوبٌ بيد.

**هذه الوحدةُ تسجيلٌ محض**: لا رقمَ مقيسٌ فيها، والتشغيلُ في دفعةٍ تالية.
وأوراكلُها يستشهد بالختم البايتيّ `30c7e393…` وحدَه — لا بنثرٍ يصف مدوّنةً
ومصدرًا وروايةً، فالنثرُ يتبدّل ولا يُعرَف تبدّلُه.

`THE_OLD_STATISTIC_WAS_DRIVEN_BY_THE_CORPUS_NOT_BY_THE_MARKING`: وسبقَ أن
قِيس نصيبُ الحرف بعد نونٍ موسومةٍ بالسكون **منسوبًا إلى وقوعه في النصّ
كلِّه**. فدخل تردُّدُ الحرف في المقام، ووسمٌ عشوائيٌّ بالعدد نفسِه بلغ
مؤشّرُه **٠٫٢١٢٥** — أي أنّ خُمسَ الاتّفاق يأتي من كثرة الوسم لا من
موافقته. وذلك ما أسقط ص٢.

`THE_CORRECTED_STATISTIC_CONTRASTS_INSIDE_THE_NUN_SITES`: والمقياسُ
المُصحَّحُ **يقارن داخلَ مواضع النون نفسِها**: لكلّ حرفٍ لوغاريتمُ نسبة
حظِّه من الموسومة إلى حظِّه من غير الموسومة. فتردُّدُ الحرف في المدوّنة
يسقط من الطرفين معًا، ولا يبقى إلّا أثرُ الوسم. ولم يُحسَب هذا المقياسُ
بعدُ، فحدُّه مكتوبٌ على **غير مرئيّ**.

`THE_NULL_IS_A_LABEL_SWAP_INSIDE_THE_SAME_SITES`: وصفريُّه تبديلُ وسمَي
«موسومة/غير موسومة» على مواضع النون بأعدادها نفسِها. فتحت هذا الصفريّ
تستوي النسبةُ عند الواحد ويصير اللوغاريتمُ صفرًا لكلّ حرف — فإن بقي
مؤشّرٌ مرتفعٌ فالعلّةُ في المقياس لا في المادّة.

`THE_COMPARISON_IS_THE_DEPOSITED_THREE_AND_ITS_COUNT_IS_A_CONDITION`:
والمُقابَلُ به الثلاثيُّ المُشتَقُّ من المُودَع، **وعددُ مجموعاته شرطٌ**
يُفحَص — كيلا يُسمَّى خماسيٌّ لا تحمله الشجرة كما وقع في خ٢.

`TWO_PANS_ARE_PUBLISHED_TOGETHER_OR_NEITHER_IS_READ`: وكفّتان تُنشَران
معًا: تماسكُ المخارج على **رسمٍ مجرَّدٍ من الضبط** (كما سقط في خ١)، وعليه
**بالضبط المُسمّى روايتُه**. فالفرقُ بينهما أثرُ الضبط بعينه، ونشرُ واحدةٍ
دون أختها يُخفي أيَّهما حمل الأثر.
"""

from __future__ import annotations

from fractions import Fraction

from algebra.attainability import permutation_floor
from algebra.signified import Direction, Oracle, Prediction, Verdict, seal

CORPUS_RECORD = "30c7e393eff12641e27802dbfc38c51e7171ed873bfd2f78dc889de2fad7a359"
SUPERSEDED_GATE = "85f59f23c39d3ded9d459a332c7df7587f13891d7e54d4fdad40f63dfb51a160"
OLD_NULL_REACHED = Fraction(2_125, 10_000)

REPLICATES = 2_000
SEED = 20_260_924
FAMILY = 5
DEPOSITED_GROUPS = 3

MARKED_CONTRAST = Oracle(
    name="تباينُ الوسم داخلَ مواضع النون على المدوّنة المُقفَلة",
    source=(
        f"السجلُّ البايتيُّ {CORPUS_RECORD[:16]}… وحدَه: يحمل المدوّنةَ "
        "ببصمتها وطولها وأسطرها، ومصدرَها الموقَّع، وروايتَها بمنزلتها "
        "وعددِ فوارقها. ولا يُوصَف شيءٌ منها نثرًا ههنا"
    ),
    extraction=(
        "لكلّ حرفٍ: لوغاريتمُ نسبة حظِّه من مواضع النون **الموسومة** إلى "
        "حظِّه من مواضع النون **غير الموسومة**. فالمقامان من مواضع النون "
        "وحدَها، ويسقط تردُّدُ الحرف في المدوّنة من الطرفين. ثمّ يُقسَم "
        "الحروفُ على هذا البُعد، ويُقابَل التقسيمُ بالثلاثيّ المُودَع"
    ),
)

PREDICTIONS = (
    Prediction(
        identifier="ك١ الصفريُّ يهبط بالمقياس المُصحَّح",
        statistic=(
            "أعلى مؤشّرِ رَند يبلغه تبديلُ وسمَي الموسومة وغيرِ الموسومة "
            "على مواضع النون بأعدادها نفسِها"
        ),
        threshold=Fraction(10, 100),
        direction=Direction.AT_MOST,
        falsifies=(
            "أنّ التصحيحَ أصلح العطل؛ فبقاءُ الصفريّ مرتفعًا يعني أنّ "
            "العلّةَ في المقياس لا في كثرة الوسم، ويُبطِل قراءةَ ك٢"
        ),
    ),
    Prediction(
        identifier="ك٢ التكرارُ على النصف المحجوب بالمقياس المُصحَّح",
        statistic=(
            "مؤشّرُ رَند المعدَّل بين التقسيم المُستخرَج من النصف الأوّل "
            "بالمقياس المُصحَّح والثلاثيِّ المُودَع، محسوبًا على النصف الثاني"
        ),
        threshold=Fraction(35, 100),
        direction=Direction.AT_LEAST,
        falsifies=(
            "أنّ وسمَ السكون يحمل تقسيمَ الأحكام؛ فدونه لا يُسترجَع المُودَع "
            "من الوسم بعد إسقاط أثر التردّد"
        ),
    ),
    Prediction(
        identifier="ك٣ المُقابَلُ به مُودَعٌ وعددُ مجموعاته ثلاث",
        statistic="عددُ مجموعات التقسيم المُقابَل به، مُشتَقًّا من المُودَع",
        threshold=Fraction(DEPOSITED_GROUPS),
        direction=Direction.AT_MOST,
        falsifies=(
            "سلامةَ المقابلة؛ فتقسيمٌ أوسعُ من المُودَع يعني أنّ شيئًا منه "
            "كُتِب بيدٍ ههنا — وهي علّةُ خ٢ بعينها"
        ),
    ),
    Prediction(
        identifier="ك٤ الكفّتان تُنشَران معًا",
        statistic=(
            "عددُ قراءات تماسك المخارج المنشورة: على رسمٍ مجرَّد، وعلى " "ضبطٍ مُسمّاةٍ روايتُه"
        ),
        threshold=Fraction(2),
        direction=Direction.AT_LEAST,
        falsifies=(
            "لا شيء؛ وهو بندُ إعلانٍ يمنع نشرَ كفّةٍ دون أختها، فيُخفى " "أيُّهما حمل الأثر"
        ),
    ),
    Prediction(
        identifier="ك٥ مقامُ كلّ كفّةٍ منشور",
        statistic="أقلُّ عددِ موضعٍ داخلٍ في القياس من كفّتَي الرسم والضبط",
        threshold=Fraction(200),
        direction=Direction.AT_LEAST,
        falsifies="قابليّةَ قراءة الكفّة التي وقعت دونه؛ وتُعلَن ضعيفةَ الشهادة",
    ),
)

MARKED_SEAL = seal(MARKED_CONTRAST, PREDICTIONS)

SEALED_DIGEST = "6a584a5a1254329445f8a8c5dcc5b52303155fe9c13cafb9dd844a3abf36c1d3"


def test_the_seal_is_stable_and_cites_the_byte_record_alone() -> None:
    """أوراكلٌ يستشهد بالسجلّ المُقفَل لا بنثرٍ يصف مدوّنةً وروايةً."""

    assert MARKED_SEAL == SEALED_DIGEST
    assert len(MARKED_SEAL) == 64
    assert CORPUS_RECORD[:16] in MARKED_CONTRAST.source
    assert "نثرًا" in MARKED_CONTRAST.source  # وذلك نفيٌ مكتوبٌ لا مسكوتٌ عنه


def test_the_first_condition_answers_the_gate_that_fell() -> None:
    """ك١ يواجه ما أسقط ص٢: صفريٌّ بلغ ٠٫٢١٢٥، والحدُّ ههنا ٠٫١٠ «لا يجاوز»."""

    first = PREDICTIONS[0]
    assert first.direction is Direction.AT_MOST
    assert first.verdict(OLD_NULL_REACHED) is Verdict.FALSIFIED
    assert first.verdict(Fraction(5, 100)) is Verdict.MET
    assert len(SUPERSEDED_GATE) == 64 and SUPERSEDED_GATE != MARKED_SEAL


def test_the_threshold_of_the_second_is_written_on_an_unseen_measure() -> None:
    """المقياسُ المُصحَّحُ لم يُحسَب بعدُ، فحدُّه على غير مرئيّ لا على رقمٍ رُئي."""

    assert "لوغاريتمُ نسبة" in MARKED_CONTRAST.extraction
    assert "من الطرفين" in MARKED_CONTRAST.extraction
    assert PREDICTIONS[1].threshold == Fraction(35, 100)
    # ولا يُذكَر ٠٫٤٩٤٤ ولا ٠٫٥٥٧٠ في أيّ شرطٍ ههنا
    joined = " ".join(one.statistic + one.falsifies for one in PREDICTIONS)
    assert "0.4944" not in joined and "0.5570" not in joined


def test_the_third_condition_runs_the_other_way_to_catch_a_written_partition() -> None:
    """ك٣ «لا يجاوز» ثلاثًا: تقسيمٌ أوسعُ يعني أنّ شيئًا كُتِب بيد."""

    third = PREDICTIONS[2]
    assert third.direction is Direction.AT_MOST
    assert third.verdict(Fraction(3)) is Verdict.MET
    assert third.verdict(Fraction(5)) is Verdict.FALSIFIED
    assert "علّةُ خ٢ بعينها" in third.falsifies


def test_the_family_is_five_with_one_announcement_and_a_machine_floor() -> None:
    """خمسةٌ مُسمّاةٌ قبل العدّ، واحدٌ منها بندُ إعلان، والأرضيّةُ ١/٢٠٠١."""

    assert FAMILY == len(PREDICTIONS) == 5
    assert len({one.identifier for one in PREDICTIONS}) == FAMILY
    announcements = [one for one in PREDICTIONS if one.falsifies.startswith("لا شيء")]
    assert len(announcements) == 1 and announcements[0].identifier.startswith("ك٤")
    assert permutation_floor(REPLICATES) == Fraction(1, 2_001)
    assert SEED == 20_260_924
