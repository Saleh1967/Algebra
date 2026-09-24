"""تسجيلُ تدقيقِ المخطّط بالسلوك، مختومًا قبل أن يُقاس رقمٌ على المصحف.

**ما يُسجَّل ههنا**: أن تُعرَض مجموعاتُ التراث المُودَعة — مخارجُ الحروف
وأحكامُ النون — على **فضاء الانتقال المقيس**، فتُسأل: أتتماسك فيه؟ أيُستخرَج
تقسيمُها منه؟ وهذا هو الفرقُ بين تراثٍ مختومٍ وفرضيّةٍ تحت النار.

`THE_SCHEMA_WAS_BEING_MEASURED_BY_A_RULER_TAKEN_FROM_ITSELF`: وما كان يجري
قبلَه أنّ المخطّطَ يُقاس **بمقياسٍ من المخطّط نفسِه** (الرتبةُ من الجدول
المُودَع). وذلك يُصدِّق نفسَه بنفسه مهما كان. فيُشترَط ههنا أن يكون المقياسُ
**من مادّةٍ خارجةٍ عنه**: صفوفُ `P(اللاحق | السابق)` من تعدادٍ لم يرَ
التقسيمَ ألبتّة.

`THE_PROSE_RUN_ALREADY_REFUTED_THE_EASY_VERSION_AND_THAT_IS_WHY_خ٥_EXISTS`:
وقد جرى القياسُ على نثرٍ حديثٍ فخرج **سالبًا**: تماسكُ المجموعات داخلَها
٠٫٧٠٠ مقابلَ ٠٫٧٠٩ بينها، `z = −0.5`. ولم يكن ذلك فشلَ آلةٍ بل **فشلَ مقامٍ
عُرِضت عليه**: الأحكامُ معرَّفةٌ عند نونٍ **ساكنة**، والسكونُ صفةُ قراءةٍ
لا رسم، والنثرُ مدوّنةٌ غيرُ التي صِيغت لها. فصار شرطًا: يُقاس عند الملتقى
المُعرَّف بروايةٍ مُسمّاة، أو لا يُقاس.

`A_DISAGREEMENT_IS_PUBLISHED_ABOUT_BOTH_SIDES_NOT_FOLDED_INTO_A_FIX`: وإن
خالف التقسيمُ المستخرَجُ التقسيمَ الكلاسيكيَّ فالخلافُ **خبرٌ يُنشَر عن
الطرفين معًا** — عن المخطّط وعن المقياس — ولا يُحوَّل «تصحيحًا» للمخطّط
ولا «معايرةً» للمقياس بعد النظر.
"""

from __future__ import annotations

from fractions import Fraction

from algebra.attainability import governing_floor, permutation_floor
from algebra.provenance import Corpus, Reading
from algebra.signified import Direction, Oracle, Prediction, Verdict, seal

SCHEMA = Oracle(
    name="تدقيقُ مجموعات التراث في فضاء انتقال الحروف على المصحف",
    source=(
        "صفوفُ `P(اللاحق | السابق)` من تعداد الانتقالات على عمود الرسم "
        "ببصمته وإغلاقه وسياسته؛ والمجموعاتُ من الجداول المُودَعة: مخارجُ "
        "الحروف، وأحكامُ النون الساكنة"
    ),
    extraction=(
        "التعدادُ لا يرى التقسيمَ ألبتّة: يُبنى أوّلًا وحدَه، ثمّ تُعرَض "
        "عليه المجموعاتُ. والتماسكُ تشابهُ الصفوف داخلَ المجموعة مقابلَ "
        "بينها، والاستخراجُ تقسيمٌ يُشتَقّ من الصفوف ثمّ يُقابَل بالكلاسيكيّ "
        "بمؤشّرِ رَند المعدَّل. ولا تُعدَّل حدودٌ بعد النظر"
    ),
)

REPLICATES = 2_000
SEED = 20_260_924
FAMILY = 5

CLASSICAL_PARTS = (6, 4, 2, 1, 15)
ALPHABET = 28

PREDICTIONS = (
    Prediction(
        identifier="خ١ تماسكُ المخارج في فضاء الانتقال",
        statistic=(
            "نصيبُ ما فوق الصفريّ من المتاح لتشابه صفوف الانتقال: "
            "(داخلَ المخرج − بينه) ÷ (١ − بينه)"
        ),
        threshold=Fraction(5, 100),
        direction=Direction.AT_LEAST,
        falsifies=(
            "أنّ مخارجَ الحروف تترك أثرًا في فضاء الانتقال؛ فدونه هي تصنيفٌ "
            "نطقيٌّ لا يظهر في تعاقب الرسم"
        ),
    ),
    Prediction(
        identifier="خ٢ استخراجُ تقسيم أحكام النون",
        statistic=(
            "مؤشّرُ رَند المعدَّل بين التقسيم المُشتَقّ من بروفايل ما بعد "
            "النون الساكنة والتقسيم الكلاسيكيّ ٦/٤/٢/١/١٥"
        ),
        threshold=Fraction(20, 100),
        direction=Direction.AT_LEAST,
        falsifies=(
            "دعوى «الأحكامُ مستخرَجةٌ من العدّ»؛ فدونه هي وضعٌ مدرسيٌّ "
            "لا يُستخرَج من تعاقب الرسم عند هذا المقياس"
        ),
    ),
    Prediction(
        identifier="خ٣ الصفريُّ يحفظ الهامشين الموضعيّين",
        statistic="عددُ الصفريّات التي تحفظ هامشَي المواضع الحاملة للزوج",
        threshold=Fraction(REPLICATES),
        direction=Direction.AT_LEAST,
        falsifies=(
            "قابليّةَ قراءة خ١ وخ٢؛ فصفريٌّ بهامشٍ عامٍّ يضخّم المتوقَّعَ "
            "فيصنع تماسكًا حيث لا تماسك"
        ),
    ),
    Prediction(
        identifier="خ٤ مقامٌ منشورٌ لكلّ مجموعة",
        statistic="عددُ الحروف في أصغر مجموعةٍ تدخل القراءة",
        threshold=Fraction(2),
        direction=Direction.AT_LEAST,
        falsifies=(
            "قابليّةَ قراءة تلك المجموعة؛ ومجموعةُ حرفٍ واحدٍ لا تشابهَ " "داخلَها يُقاس أصلًا"
        ),
    ),
    Prediction(
        identifier="خ٥ الملتقى مُعرَّفٌ بروايةٍ مُسمّاة",
        statistic="عددُ الروايات المُسمّاةِ في ختم العمود الذي يُقرأ منه السكون",
        threshold=Fraction(1),
        direction=Direction.AT_LEAST,
        falsifies=(
            "نسبةَ النتيجة إلى «العربيّة»؛ وقد خرجت على النثر سالبةً لأنّ "
            "النونَ قِيست مطلقةً لا ساكنة"
        ),
    ),
)

SCHEMA_SEAL = seal(SCHEMA, PREDICTIONS)

SEALED_DIGEST = "9ed9eeead8cb2fa512cdde14fa9d4cca2538d4d48a8eb8035968f86604fa2673"
"""البصمةُ مكتوبةٌ في المتن؛ فتبديلُ حدٍّ أو أوراكلَ يُسقِط الفحصَ لا يمرّ."""

# ما جرى على النثر: منقولٌ بختمه، ولا يُقارَن برقم المصحف إلّا مكتوبًا
PROSE = Corpus(
    name="نثرٌ حديثٌ لمؤلّفٍ واحد",
    digest="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    size=236_994,
    size_unit="كلمة",
)
PROSE_WITHIN = Fraction("0.700")
PROSE_BETWEEN = Fraction("0.709")


def test_the_seal_is_stable_and_a_moved_threshold_changes_it() -> None:
    """بصمةٌ تُعاد من مكوّناتها، وتبديلُ حدٍّ بعد النظر يُعرَف بتغيُّرها."""

    assert SCHEMA_SEAL == SEALED_DIGEST
    assert len(SCHEMA_SEAL) == 64
    assert set(SCHEMA_SEAL) <= set("0123456789abcdef")
    assert SCHEMA_SEAL == seal(SCHEMA, PREDICTIONS)

    easier = (
        Prediction(
            identifier=PREDICTIONS[0].identifier,
            statistic=PREDICTIONS[0].statistic,
            threshold=Fraction(-1, 100),
            direction=PREDICTIONS[0].direction,
            falsifies=PREDICTIONS[0].falsifies,
        ),
        *PREDICTIONS[1:],
    )
    assert seal(SCHEMA, easier) != SCHEMA_SEAL


def test_the_prose_result_falsifies_the_first_condition_as_written() -> None:
    """٠٫٧٠٠ داخلَها و٠٫٧٠٩ بينها: نصيبٌ سالبٌ، فخ١ ساقطٌ على تلك المدوّنة.

    وذلك مسجَّلٌ لا مطويّ: الشرطُ يُقرَأ على المصحف، وسقوطُه على النثر
    **خبرٌ عن النثر** يُنشَر معه لا بدله.
    """

    headroom = (PROSE_WITHIN - PROSE_BETWEEN) / (1 - PROSE_BETWEEN)
    assert headroom < 0
    assert PREDICTIONS[0].verdict(headroom) is Verdict.FALSIFIED
    assert PREDICTIONS[0].verdict(Fraction(6, 100)) is Verdict.MET


def test_the_prose_figure_is_stamped_and_not_comparable_across_statistics() -> None:
    """رقمُ النثر مختومٌ بمدوّنته؛ ولا يُطرَح من رقمٍ آخرَ مقياسُه مختلف."""

    carried = Reading(
        value=PROSE_WITHIN,
        statistic="تشابهُ صفوف الانتقال داخلَ مجموعات المخارج",
        unit="زوجُ حروف",
        corpus=PROSE,
    )
    same = Reading(
        value=PROSE_BETWEEN,
        statistic=carried.statistic,
        unit=carried.unit,
        corpus=PROSE,
    )
    gap, note = carried.against(same)
    assert gap == Fraction("-0.009")
    assert "مدوّنةٌ واحدة" in note
    assert PROSE.name in carried.stamp


def test_the_classical_partition_is_total_and_is_what_خ٢_is_measured_against() -> None:
    """٦+٤+٢+١+١٥ = ٢٨؛ فالمقابلةُ تقسيمٌ بتقسيمٍ لا حرفٌ بحرف."""

    assert sum(CLASSICAL_PARTS) == ALPHABET
    assert len(CLASSICAL_PARTS) == 5
    assert "٦/٤/٢/١/١٥" in PREDICTIONS[1].statistic


def test_the_ruler_comes_from_outside_the_schema() -> None:
    """المقياسُ من تعدادٍ لم يرَ التقسيم؛ وهو شرطٌ مكتوبٌ في الأوراكل نفسِه."""

    assert "لا يرى التقسيمَ ألبتّة" in SCHEMA.extraction
    assert "يُبنى أوّلًا وحدَه" in SCHEMA.extraction
    for one in PREDICTIONS[:2]:
        assert "الرتبة" not in one.statistic


def test_the_family_is_five_and_none_of_them_is_a_free_announcement() -> None:
    """خمسةٌ مُعلَنةٌ قبل العدّ، ولا واحدَ منها بندُ إعلانٍ بلا سقوط."""

    assert FAMILY == len(PREDICTIONS) == 5
    assert len({one.identifier for one in PREDICTIONS}) == FAMILY
    announcements = [one for one in PREDICTIONS if one.falsifies.startswith("لا شيء")]
    assert announcements == []
    assert SEED == 20_260_924


def test_the_floor_is_the_machine_because_the_material_is_large() -> None:
    """خاناتُ الجدول بالمئات، فتحكم أرضيّةُ الآلة لا أرضيّةُ المادّة."""

    machine = permutation_floor(REPLICATES)
    assert machine == Fraction(1, 2_001)
    assert governing_floor(ALPHABET // 2, ALPHABET, REPLICATES) == machine
