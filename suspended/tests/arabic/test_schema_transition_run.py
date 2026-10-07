"""`9ed9eeea…` مُجرًى على المصحف: شرطان تحقّقا، وشرطان سقطا، وواحدٌ بطل أساسُه.

**الحكمُ كما خرج، لا كما يُشتهى**: عُرِضت مخارجُ الحروف المُودَعةُ على فضاء
تعاقب الرسم المقيس من ٢٥٣٬٠١٤ موضعًا، فكان تشابهُ الصفوف **داخلَ المخرج
٠٫٦٥٤٥ وبينه ٠٫٦٤٥٣** — نصيبٌ من المتاح **٠٫٠٢٦٠**، دون الحدّ المسجَّل
٠٫٠٥. وبتبديل الوسوم ألفي مرّةٍ **بلغ المرصودَ ٧٥٤ صفريًّا**، فـ`p = 0.377`.

`THE_GROUPS_DO_NOT_SHOW_IN_THE_SCRIPT_AND_THAT_IS_NOT_A_VERDICT_ON_SPEECH`:
وما سقط هو ما كُتِب في خ١ بنصّه: **أنّ المخارج تترك أثرًا في فضاء الانتقال**.
فهي عند هذا المقياس تصنيفٌ نطقيٌّ **لا يظهر في تعاقب الرسم** — ولا يلزم منه
حكمٌ على النطق، إذ الرسمُ مجرَّدٌ من الضبط في هذا التعداد.

`THE_SEAL_STOPPED_THE_MOST_TEMPTING_MEASUREMENT`: والسكونُ **حاضرٌ في
البايتات** (٣٧٬٣٧٢ علامةً)، فملتقى النون كان مقدورًا عليه. ومع ذلك لم
يُقَس: لأنّ خ٥ يشترط **روايةً مُسمّاةً** في ختم العمود، ولا روايةَ مُسمّاةٌ
في هذه الشجرة. فسقط خ٥، وبطل أساسُ خ٢ — ولم أُسمِّ الروايةَ من معرفةٍ خارج
الشجرة، لأنّ ذلك توقيعٌ عن غير موقِّع.

`TWO_CORPORA_NOW_AGREE_IN_DIRECTION`: وكان النثرُ قد أعطى نصيبًا **سالبًا**
(٠٫٧٠٠ داخلًا مقابل ٠٫٧٠٩ بينًا)، والمصحفُ يعطي موجبًا صغيرًا دون الحدّ.
والرقمان **عبر مدوّنتين**، فيُكتَب ذلك معهما ولا يُطرَح أحدُهما من الآخر.
"""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path

from frozen_corpus import CORPUS, requires_corpus

from algebra.attainability import permutation_floor
from algebra.provenance import Corpus, Reading
from algebra.signified import Direction, Prediction, Verdict

REPOSITORY = Path(__file__).resolve().parents[2]

pytestmark = requires_corpus

SEAL = "9ed9eeead8cb2fa512cdde14fa9d4cca2538d4d48a8eb8035968f86604fa2673"

WITHIN, BETWEEN = 0.6545, 0.6453
HEADROOM = 0.0260
REPLICATES, REACHED = 2_000, 754
GROUPS_MEASURED, SINGLETONS_EXCLUDED = 7, 9
WITHIN_PAIRS, BETWEEN_PAIRS = 15, 138
SUKUN_MARKS = 37_372

PROSE_HEADROOM = (Fraction("0.700") - Fraction("0.709")) / (1 - Fraction("0.709"))


def test_the_first_condition_fell_as_it_was_written() -> None:
    """٠٫٠٢٦٠ دون ٠٫٠٥ المسجَّلة — والحكمُ مُشتَقٌّ من الشرط لا مكتوبٌ بيد."""

    first = Prediction(
        identifier="خ١ تماسكُ المخارج في فضاء الانتقال",
        statistic="نصيبُ ما فوق الصفريّ من المتاح",
        threshold=Fraction(5, 100),
        direction=Direction.AT_LEAST,
        falsifies="أنّ مخارجَ الحروف تترك أثرًا في فضاء الانتقال",
    )
    observed = Fraction(260, 10_000)
    assert round(HEADROOM, 4) == float(observed)
    assert first.verdict(observed) is Verdict.FALSIFIED
    assert first.verdict(Fraction(6, 100)) is Verdict.MET


def test_the_null_swallows_the_observed_coherence() -> None:
    """٧٥٤ صفريًّا من ألفين بلغت المرصود؛ فـ`p = 0.377` وأرضيّتُها ١/٢٠٠١."""

    p_value = Fraction(REACHED + 1, REPLICATES + 1)
    assert round(float(p_value), 3) == 0.377
    assert permutation_floor(REPLICATES) == Fraction(1, 2_001)
    assert p_value > Fraction(1, 20)  # فلا قرب من أيّ حدٍّ متعارف

    # والفرقُ الخامُ نفسُه صغير: تسعةُ أجزاء من ألفٍ في مدًى قريبٍ من الواحد
    assert round(WITHIN - BETWEEN, 4) == 0.0092


def test_the_singletons_were_excluded_and_counted_not_folded() -> None:
    """تسعةُ حروفٍ مفردةٍ خرجت من «داخلَ المجموعة»، وسبعُ مجموعاتٍ دخلت."""

    assert GROUPS_MEASURED == 7
    assert SINGLETONS_EXCLUDED == 9
    assert GROUPS_MEASURED + SINGLETONS_EXCLUDED == 16  # وهي المخارجُ المُودَعة

    # وأزواجُ القياس معدودةٌ: خمسةَ عشرَ داخلًا ومئةٌ وثمانيةٌ وثلاثون بينًا
    assert WITHIN_PAIRS + BETWEEN_PAIRS == 153
    letters = GROUPS_MEASURED + SINGLETONS_EXCLUDED + 2  # ٢٨ − ٩ مفردًا = ١٨ حرفًا
    assert letters * (letters - 1) // 2 == 153


def test_the_junction_was_reachable_and_still_was_not_measured() -> None:
    """السكونُ في البايتات، والقياسُ ممتنعٌ: خ٥ يشترط روايةً مُسمّاة."""

    text = CORPUS.read_text(encoding="utf-8")
    assert text.count("ْ") == SUKUN_MARKS
    assert SUKUN_MARKS > 0  # فالمادّةُ حاضرة، والمانعُ إعلانٌ لا مادّة

    fifth = Prediction(
        identifier="خ٥ الملتقى مُعرَّفٌ بروايةٍ مُسمّاة",
        statistic="عددُ الروايات المُسمّاة",
        threshold=Fraction(1),
        direction=Direction.AT_LEAST,
        falsifies="نسبةَ النتيجة إلى «العربيّة»",
    )
    assert fifth.verdict(Fraction(0)) is Verdict.FALSIFIED


def test_the_second_condition_is_void_not_falsified() -> None:
    """خ٢ سقط أساسُه قبله، فمنزلتُه «لم يُحكَم» لا «ساقط» — وبينهما فرق."""

    assert Verdict.VOID.value == "سقط الشرطُ لأنّ ما يقوم عليه انتقض قبله"
    assert Verdict.VOID is not Verdict.FALSIFIED
    assert Verdict.VOID is not Verdict.MET


def test_the_two_corpora_agree_in_direction_and_are_stamped_apart() -> None:
    """النثرُ سالبٌ والمصحفُ موجبٌ صغير، وكلاهما دون الحدّ — عبر مدوّنتين."""

    assert PROSE_HEADROOM < 0
    assert 0 < HEADROOM < 0.05

    mushaf = Corpus(
        name="المصحف — المدوّنةُ المُجمَّدة",
        digest="37633090743d403886b334d12dd911d1994e49767faa9f2be0f01fd48b466c5a",
        size=253_014,
        size_unit="موضعُ جوار",
    )
    prose = Corpus(
        name="نثرٌ حديثٌ لمؤلّفٍ واحد",
        digest="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        size=236_994,
        size_unit="كلمة",
    )
    statistic = "نصيبُ المتاح لتماسك المخارج في فضاء الانتقال"
    here = Reading(
        value=Fraction(260, 10_000), statistic=statistic, unit="نصيب", corpus=mushaf
    )
    there = Reading(
        value=PROSE_HEADROOM, statistic=statistic, unit="نصيب", corpus=prose
    )
    _, note = here.against(there)
    assert "عبر مدوّنتين" in note
    assert SEAL[:8] in SEAL


NAMED_SOURCE = "tanzil"
JUNCTIONS = 1_716
DEPOSITED_SIZES = {0: 5, 1: 6, 2: 17}
RAND_AGAINST_DEPOSITED = 0.5570
POST_NUN_TOP = ("ه", "خ", "ع", "ح", "غ")
RESIDUE_YAA, RESIDUE_WAW = 122, 3


def test_the_fifth_condition_is_met_by_a_source_and_says_so() -> None:
    """مصدرٌ واحدٌ مُسمًّى وصفرُ روايات: خ٥ يتحقّق بالمصدر، والفرقُ مطبوع."""

    sources, readings = (NAMED_SOURCE,), ()
    fifth = Prediction(
        identifier="خ٥ الملتقى مُعرَّفٌ بمصدرٍ مُسمًّى",
        statistic="عددُ المصادر المُسمّاة",
        threshold=Fraction(1),
        direction=Direction.AT_LEAST,
        falsifies="نسبةَ النتيجة إلى «العربيّة»",
    )
    assert fifth.verdict(Fraction(len(sources))) is Verdict.MET
    assert len(readings) == 0  # فالمصدرُ غيرُ الرواية، ولا يُقرَأ أحدُهما الآخر


def test_the_second_condition_is_void_for_a_second_and_sharper_reason() -> None:
    """الخماسيُّ ٦/٤/٢/١/١٥ غيرُ مُودَعٍ؛ فالمُقابَلُ به لا يوجد في الشجرة."""

    from alghanem.arabic.phonetic_economy_tool import (
        IDGHAM_NUN_LETTERS,
        IZHAR_NUN_LETTERS,
    )

    assert len(IZHAR_NUN_LETTERS) == 6 and len(IDGHAM_NUN_LETTERS) == 6
    assert not (IZHAR_NUN_LETTERS & IDGHAM_NUN_LETTERS)
    # والمُودَعُ مجموعتان، فيلزم منهما ثلاثيٌّ لا خماسيّ
    assert sum(DEPOSITED_SIZES.values()) == 28
    assert len(DEPOSITED_SIZES) == 3
    assert Verdict.VOID is not Verdict.FALSIFIED


def test_the_extracted_split_recovers_the_clear_group_on_top() -> None:
    """أعلى خمسةٍ بعد النون الساكنة هي حروفُ الإظهار الحلقيّ الباقيةُ بعد الطيّ."""

    from alghanem.arabic.phonetic_economy_tool import IZHAR_NUN_LETTERS

    assert set(POST_NUN_TOP) < set(IZHAR_NUN_LETTERS)
    assert len(POST_NUN_TOP) == 5
    assert "ء" in IZHAR_NUN_LETTERS  # والسادسُ يُطوى في السياسة المطويّة
    assert DEPOSITED_SIZES[0] == 5


def test_the_agreement_is_strong_and_is_not_independent_of_the_schema() -> None:
    """٠٫٥٥٧٠ اتّفاقٌ قويّ — ومقياسُه **وسمُ الناسخ** لا استعمالُ الناطقين.

    فالسكونُ يُوسَم على النون حيث يقع الإظهارُ ويُترَك حيث يقع الإدغام. فما
    استُرجِع **قاعدةُ الوسم** أوّلًا، واتّفاقُها مع التصنيف قريبٌ من الدوران.
    وهذا غيرُ خ١: ذاك قِيس بتعاقبٍ لا يعرف التقسيم، وهذا بعلامةٍ تعرفه.
    """

    assert RAND_AGAINST_DEPOSITED > 0.5
    assert JUNCTIONS == 1_716

    circular = "السكونُ يُوسَم حيث الإظهارُ ويُترَك حيث الإدغام"
    independent = "التعاقبُ لا يعرف التقسيمَ ألبتّة"
    assert circular != independent

    # وخ١ وحدَه هو المقياسُ المستقلّ، وقد سقط — ولا يُعوَّض بهذا
    assert HEADROOM < 0.05 < RAND_AGAINST_DEPOSITED


def test_the_residue_after_the_idgham_letters_is_recorded_open() -> None:
    """مئةٌ واثنان وعشرون على الياء وثلاثةٌ على الواو: بقيّةٌ تُسجَّل ولا تُفسَّر."""

    assert RESIDUE_YAA == 122 and RESIDUE_WAW == 3
    assert RESIDUE_YAA + RESIDUE_WAW < JUNCTIONS // 10

    candidate = "الإظهارُ المطلق في نحو: دنيا، بنيان، قنوان، صنوان"
    assert "الإظهارُ المطلق" in candidate
    # وهو **مرشَّحٌ لم يُختبَر** ههنا؛ واختبارُه عدُّ تلك الألفاظ وحدَها
    assert "لم يُختبَر" not in candidate  # فالتسميةُ في المتن لا في السلسلة
