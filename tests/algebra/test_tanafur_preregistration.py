"""المرحلةُ الأولى مختومةً: ثلاثةُ أزواجِ تنافرٍ وملتقى النون، قبل أيّ عدّ.

**لماذا تُختَم هذه وحدَها**: مادّتُها عمودٌ واحدٌ من المحاذاة، ولا تنتظر
تفريغًا ولا محاذاةً زمنيّة. وختمُ مرحلتين معًا يقتضي كتابةَ حدودٍ لقياسٍ
لم تُعرَف وحدتُه بعد (زمنُ الغنّة بالمِلّي؟ نصيبُ طاقةٍ؟) — وحدٌّ يُكتَب
على قياسٍ مجهول الوحدة ليس حدًّا. فتُختَم الأولى الآن وتُختَم الثانيةُ حين
تُسمّى وحدتُها.

`THE_SUKUN_IS_A_READING_AND_THE_STAMP_MUST_NAME_IT`: وملتقى النون الساكنة
**ليس في الرسم المجرَّد**: السكونُ صفةُ قراءةٍ لا رسم. فإن قُرِئ من العمود
المشكول فهو مشكولٌ **برواية**، وتُسمّى الروايةُ في الختم. ومن قاس عليه
ولم يُسمِّها قاس رواةً وسمّاهم لغةً. وشرطُ ن٥ يمنع التشغيل بدون التسمية.

`TANAFUR_PREDICTS_A_SHORTFALL_NOT_A_DEVIATION`: والتنافرُ دعوًى **باتّجاه**:
أن يقلَّ اللقاءُ عن المتوقَّع، لا أن يخالفه. فحدُّ ن١ «لا يجاوز» لا «يبلغ»؛
وزوجٌ يجاوز متوقَّعَه بكثيرٍ **يُسقِط الدعوى ولا يؤيّدها**، وإن كان انحرافُه
أبلغَ. وهذا ما يفرّق الشرطَ عن الصيد.

`THE_MARGINS_COME_FROM_THE_POSITIONS_THAT_CAN_CARRY_THE_PAIR`: ودرسُ جدول
الجوار مكتوبٌ شرطًا ههنا لا نصيحةً: الهامشان يُحسَبان من المواضع التي
تحمل الزوج فعلًا، وإلّا ضُخِّم المتوقَّعُ الضِّعفَ (٣٨١ صارت ٢١٤). وسياسةُ
الطيّ تُنشَر بالوجهين، إذ بدّلت الجوابَ من ١٤٤ خانةً خاليةً إلى ٣٧٤.

`THEIR_THREE_VERDICTS_LIVE_ON_TWO_AXES_HERE`: وأحكامُهم الثلاثةُ —
مستخرجةٌ، ونادرةٌ، ووضعيّة — ليست ثلاثةَ أعضاءٍ في مفردةٍ واحدةٍ عندنا:
الأولى `Evidence.ATTESTED`، والثالثةُ `Evidence.STIPULATED`، وأمّا
**النادرة** فليست جنسَ دليلٍ بل **مآلَ قياسٍ جرى**: `Vacancy.REFUSED`.
فمحوران لا محور، وخلطُهما يجعل «رُدَّت بصفريّ» نوعًا من أنواع الشهادة.
"""

from __future__ import annotations

from fractions import Fraction

from algebra.attainability import governing_floor, permutation_floor
from algebra.results import Evidence, Vacancy
from algebra.signified import Direction, Oracle, Prediction, Verdict, seal

TANAFUR = Oracle(
    name="تنافرُ ثلاثة أزواجٍ داخلَ الكلمة على المصحف",
    source=(
        "عمودُ الرسم من المحاذاة الكاملة ببصمته وإغلاقه؛ والعمودُ المشكولُ "
        "لملتقى النون وحدَه، بروايةٍ مُسمّاةٍ في الختم"
    ),
    extraction=(
        "يُعَدّ اللقاءُ **داخلَ الكلمة** ولا يعبر فراغًا، والهامشان من "
        "المواضع التي تحمل الزوج فعلًا لا من الحروف كلِّها. والسياسةُ "
        "تُشغَّل بوجهيها — مطويًّا ومفصولًا — ويُنشَر الوجهان"
    ),
)

REPLICATES = 2_000
SEED = 20_260_924
FAMILY = 5

PAIRS: tuple[tuple[str, str], ...] = (("ق", "ك"), ("س", "ش"), ("ب", "ف"))

PREDICTIONS = (
    Prediction(
        identifier="ن١ نقصُ اللقاء عن المتوقَّع",
        statistic=(
            "المرصودُ مقسومًا على المتوقَّع تحت الاستقلال، لكلّ زوجٍ من "
            "الثلاثة، داخلَ الكلمة، بهامشين موضعيّين"
        ),
        threshold=Fraction(80, 100),
        direction=Direction.AT_MOST,
        falsifies=(
            "دعوى التنافر عند هذا المقياس؛ وزوجٌ يجاوز متوقَّعَه يُسقِطها "
            "ولا يؤيّدها مهما بلغ انحرافُه"
        ),
    ),
    Prediction(
        identifier="ن٢ الصفريُّ يحفظ الهامشين الموضعيّين",
        statistic="عددُ الصفريّات التي تحفظ هامشَي المواضع الحاملة للزوج",
        threshold=Fraction(REPLICATES),
        direction=Direction.AT_LEAST,
        falsifies=(
            "قابليّةَ قراءة ن١؛ فصفريٌّ يحفظ هامشًا محسوبًا على الحروف "
            "كلِّها يضخّم المتوقَّع فيصنع تنافرًا حيث لا تنافر"
        ),
    ),
    Prediction(
        identifier="ن٣ مقامٌ منشورٌ لكلّ زوج",
        statistic="أقلُّ عددِ لقاءٍ مرصودٍ في أزواج المقارنة الثلاثة",
        threshold=Fraction(12),
        direction=Direction.AT_LEAST,
        falsifies="قابليّةَ قراءة الزوج الذي وقع دونه؛ ويُعلَن ضعيفَ الشهادة",
    ),
    Prediction(
        identifier="ن٤ سياسةُ الطيّ تُنشَر بوجهيها",
        statistic="عددُ سياسات الطيّ المنشورةِ نتائجُها مع الرقم",
        threshold=Fraction(2),
        direction=Direction.AT_LEAST,
        falsifies=(
            "لا شيء؛ وهو بندُ إعلانٍ لزم من تبدُّل الجواب بالسياسة "
            "(١٤٤ خانةً خاليةً مطويًّا، و٣٧٤ مفصولًا)"
        ),
    ),
    Prediction(
        identifier="ن٥ ملتقى النون لا يُقاس بلا روايةٍ مُسمّاة",
        statistic="عددُ الروايات المُسمّاةِ في ختم العمود المشكول",
        threshold=Fraction(1),
        direction=Direction.AT_LEAST,
        falsifies=(
            "نسبةَ ملتقى النون إلى «العربيّة»؛ فالسكونُ صفةُ قراءةٍ، ومن "
            "لم يُسمِّ روايتَه قاس رواةً وسمّاهم لغةً"
        ),
    ),
)

TANAFUR_SEAL = seal(TANAFUR, PREDICTIONS)

SEALED_DIGEST = "d44f23ce1dfae719efa9a13acada7ba0bfad44c77fb7df9271d26f62353169cf"
"""البصمةُ مكتوبةٌ في المتن؛ فتبديلُ حدٍّ أو أوراكلَ يُسقِط الفحصَ لا يمرّ."""


def test_the_seal_is_stable_and_a_moved_threshold_changes_it() -> None:
    """بصمةٌ ثابتةٌ تُعاد من مكوّناتها، وتبديلُ حدٍّ يُعرَف بتغيُّرها."""

    assert TANAFUR_SEAL == SEALED_DIGEST
    assert len(TANAFUR_SEAL) == 64
    assert set(TANAFUR_SEAL) <= set("0123456789abcdef")
    assert TANAFUR_SEAL == seal(TANAFUR, PREDICTIONS)

    easier = (
        Prediction(
            identifier=PREDICTIONS[0].identifier,
            statistic=PREDICTIONS[0].statistic,
            threshold=Fraction(99, 100),
            direction=PREDICTIONS[0].direction,
            falsifies=PREDICTIONS[0].falsifies,
        ),
        *PREDICTIONS[1:],
    )
    assert seal(TANAFUR, easier) != TANAFUR_SEAL


def test_the_claim_has_a_direction_and_an_excess_falsifies_it() -> None:
    """التنافرُ نقصٌ لا انحراف: ١٫٥ تُسقِط الدعوى، و٠٫٦ تحقّقها."""

    first = PREDICTIONS[0]
    assert first.direction is Direction.AT_MOST
    assert first.verdict(Fraction(60, 100)) is Verdict.MET
    assert first.verdict(Fraction(150, 100)) is Verdict.FALSIFIED
    assert first.verdict(first.threshold) is Verdict.MET

    # ولا زوجَ يُقرَأ بالقيمة المطلقة للانحراف
    assert "مهما بلغ انحرافُه" in first.falsifies


def test_the_three_pairs_are_named_before_the_count() -> None:
    """ثلاثةُ أزواجٍ مُسمّاةٌ، ولا رابعَ يُضاف بعد رؤية الأرقام."""

    assert len(PAIRS) == 3
    assert len({frozenset(pair) for pair in PAIRS}) == 3
    letters = {one for pair in PAIRS for one in pair}
    assert len(letters) == 6  # ولا حرفَ يدخل زوجين


def test_the_junction_condition_forbids_an_unnamed_reading() -> None:
    """ن٥ يشترط روايةً مُسمّاةً، وصفرُ رواياتٍ يُسقِط القياسَ لا يُضعِفه."""

    fifth = PREDICTIONS[4]
    assert fifth.verdict(Fraction(0)) is Verdict.FALSIFIED
    assert fifth.verdict(Fraction(1)) is Verdict.MET
    assert "قاس رواةً وسمّاهم لغةً" in fifth.falsifies


def test_the_family_is_five_and_one_of_them_is_an_announcement() -> None:
    """خمسةٌ مُعلَنةٌ قبل العدّ، وواحدٌ منها بندُ إعلانٍ لا شرطُ سقوط."""

    assert FAMILY == len(PREDICTIONS) == 5
    assert len({one.identifier for one in PREDICTIONS}) == FAMILY
    announcements = [one for one in PREDICTIONS if one.falsifies.startswith("لا شيء")]
    assert len(announcements) == 1
    assert announcements[0].identifier.startswith("ن٤")


def test_the_floor_here_is_the_machine_not_the_material() -> None:
    """أزواجُ الحروف بالآلاف، فأرضيّةُ المادّة تهبط وتحكم أرضيّةُ الآلة."""

    machine = permutation_floor(REPLICATES)
    assert machine == Fraction(1, 2_001)
    assert governing_floor(14, 28, REPLICATES) == machine
    assert SEED == 20_260_924


def test_their_three_verdicts_map_onto_two_axes_here() -> None:
    """مستخرجةٌ ووضعيّةٌ جنسا دليل، والنادرةُ مآلُ قياسٍ — محوران لا محور."""

    extracted, stipulated = Evidence.ATTESTED, Evidence.STIPULATED
    assert extracted is not stipulated
    assert Vacancy.REFUSED.value == "رُدَّت بقياسٍ جرى"

    axes = {"جنسُ الدليل": {extracted, stipulated}, "مآلُ القياس": {Vacancy.REFUSED}}
    assert len(axes) == 2
    assert not isinstance(Vacancy.REFUSED, Evidence)
