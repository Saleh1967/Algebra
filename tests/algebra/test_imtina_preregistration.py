"""التسجيلُ الثالث قبل تشغيله: تنبّؤان مُشتَقّان، وتوسيعٌ بعد الختم.

**لم يُشغَّل**: لا مدوَّنةَ ههنا. وكلُّ ما في هذا الملفّ **سابقٌ على النظر**،
مُشتَقٌّ من أرقامٍ منشورةٍ قبله أو من قراءة الشيفرة الواردة.

`A_PREDICTION_DERIVABLE_BEFORE_THE_RUN_IS_NOT_A_PREDICTION`: أثقلُ ما ههنا.
التنبّؤان (أ) و(ب) **يُحسَبان من رقمين منشورين** قبل أن تدور الآلةُ دورةً:
نصيبُ «لا إعراب» هو ‎١ − ٣٤٬٢٥٤ ÷ ٧٧٬٤٢٨ = ٥٥٫٧٦٪ — وقد تنبّأ بـ[٥٠٪، ٦٠٪]؛
والرباعيُّ للنظام بلا امتناعٍ هو ‎٠٫٨٦٤٥ × ٣٤٬٢٥٤ ÷ ٧٧٬٤٢٨ = ٣٨٫٢٥٪ — وقد
تنبّأ بـ[٣٥٪، ٤٠٪]. فهما **ضابطا اتّساقٍ** لا اختباران، وتحقُّقُهما لا يشهد
للبناء بشيء. وهذا يُقال قبل التشغيل لا بعده، وإلّا صار عذرًا.

`A_SEALED_RULE_WIDENED_IS_A_DIFFERENT_RULE`: التسجيلُ يقول «إن كان الرمزُ عند
ط٧ **حرفاً (harf)**، أو كان في مكوّناته deictic». والشيفرةُ تقول
`pos in ("harf", "fi'l")`. والفعلُ **ليس في المختوم**، وحجمُه ٤٤٫٨٪ ممّا لا
يُسمّى بحالةٍ بشهادة الشيفرة نفسِها. والتوسيعُ صوابٌ نحويًّا — وهذا لا يجعله
مختومًا. فيُقاسان راية ً راية، ويُحكَم على (ج) **بالمختومة**.

`A_FIFTH_OUTCOME_IN_A_FOUR_WAY_MEASURE`: التسجيلُ يُعلن أربعةَ أصناف، والشيفرةُ
تُخرِج **خمسة**: `NONE` («لا إعراب» — حكمٌ) و`None` (defer — «لا أدري»)
حكمان مختلفان. ومصيرُ الخامس يغيّر (ج) في اتّجاهين، والتسجيلُ **لا يقول**.
فهذا قرارٌ يُعلَن قبل التشغيل، لا يُؤخَذ صمتًا بقيمةٍ افتراضيّة.

`THE_UNNAMED_MIDDLE_ZONE_IS_WHERE_THE_LAST_ONE_LANDED`: ثلاثةُ شروطٍ في
التسجيلين تُعلن حدَّ نجاحٍ وحدَّ إعلانٍ وتترك ما بينهما بلا حكم. وفي الدورة
الأولى **وقع المقيسُ في تلك المنطقة بعينها** (٨٦٫٤٥٪ بين ٨٨ و٨٥). فليست
هذه ملاحظةً صوريّة: هي الموضعُ الذي سقط فيه الحكمُ مرّةً.

`AN_INHERITED_ERROR_IS_NOT_THE_RULES_ERROR`: ق٥ تقرأ مخرَجَ ط٧، وط٧ يُعلن
`conf < 1.0` دائمًا. فحكمُ (ج) يخلط **تصميمَ ق٥** بدقّة ط٧، ولا يفصلهما إلّا
تشغيلٌ ثانٍ بوسمٍ صحيح: الفرقُ بينهما ثمنُ ط٧ مقيسًا لا مقدَّرًا.
"""

from __future__ import annotations

from fractions import Fraction

import pytest

from algebra.assignment import Assignment
from algebra.reconciliation import Partition, rounds_to
from algebra.signified import Direction, Oracle, Prediction, Verdict, seal

ALIGNED_TOKENS = 77_428  # كما أُعلن في هذا التسجيل
CASE_MARKED = 34_254
THREE_WAY = Fraction("0.8645")  # R0c على الموسوم
UNMARKED = ALIGNED_TOKENS - CASE_MARKED


def test_the_no_case_share_is_arithmetic_not_a_prediction() -> None:
    """(أ) تتنبّأ بـ[٥٠٪، ٦٠٪]، والقيمةُ ٥٥٫٧٦٪ تُشتَقّ من رقمين منشورين."""

    split = Partition(parts=(CASE_MARKED, UNMARKED), declared_total=ALIGNED_TOKENS)
    assert split.residue == 0

    share = Fraction(UNMARKED, ALIGNED_TOKENS)
    assert rounds_to(share, 4) == Fraction("0.5576")
    assert Fraction("0.50") < share < Fraction("0.60")


def test_the_four_way_score_of_the_current_system_is_arithmetic_too() -> None:
    """(ب) تتنبّأ بـ[٣٥٪، ٤٠٪]، والقيمةُ ٣٨٫٢٥٪ حاصلُ ضربٍ لا قياسٍ جديد.

    فنظامٌ يُسنِد حالةً لكلّ رمزٍ لا يصيب إلّا في الموسوم، ونصيبُه من الكلّ
    هو دقّتُه الثلاثيّةُ مضروبةً في نصيب الموسوم. ولا يحتاج ذلك تشغيلًا.
    """

    four_way = THREE_WAY * Fraction(CASE_MARKED, ALIGNED_TOKENS)
    assert rounds_to(four_way, 4) == Fraction("0.3825")
    assert Fraction("0.35") < four_way < Fraction("0.40")


def test_the_third_threshold_has_room_but_it_is_measured_against_a_ceiling() -> None:
    """(ج) عتبتُها ٧٠٫٧٦٪، وسقفُ الامتناع التامّ ٩٤٫٠١٪ — فالفسحةُ ٢٣٫٢٥ نقطة.

    والسقفُ يفترض شيئين لا يقعان معًا: أن يمتنع النظامُ عن **كلّ** غير
    الموسوم، وألّا يمتنع عن **شيءٍ** من الموسوم. وكلُّ خرقٍ لأحدهما ينزل به.
    """

    baseline = Fraction(UNMARKED, ALIGNED_TOKENS)
    threshold = baseline + Fraction("0.15")
    assert rounds_to(threshold, 4) == Fraction("0.7076")

    correct_on_marked = round(float(THREE_WAY * CASE_MARKED))
    assert correct_on_marked == 29_613
    ceiling = Fraction(UNMARKED + correct_on_marked, ALIGNED_TOKENS)
    assert rounds_to(ceiling, 4) == Fraction("0.9401")
    assert rounds_to(ceiling - threshold, 4) == Fraction("0.2325")


def test_the_token_total_disagrees_with_the_one_already_deposited() -> None:
    """٧٧٬٤٢٨ ههنا و٧٧٬٤٢٩ في «البناء الثاني» — واحدٌ، ويُسمّى لا يُطوى.

    ولا يغيّر الفرقُ حكمًا، لكنّه **يغيّر رقمًا منشورًا**: نصيبُ «لا إعراب»
    يثبت على المقامين عند ٥٥٫٧٦٪، والرباعيُّ يتحرّك ٣٨٫٢٥٪ ← ٣٨٫٢٤٪. فالمنزلةُ
    الرابعةُ ليست محدَّدةً بمقامٍ فيه خلافُ واحد، وذلك يُعلَن لا يُدفَن.

    وهو ثالثُ فرقٍ من هذا الجنس بعد ٢٢٥٬٩١٠ ÷ ٢٢٥٬٩١١ و٣٤٬٢٥٤ ÷ ٣٤٬٢٥٦.
    """

    assert 77_429 - ALIGNED_TOKENS == 1
    shares = {
        total: rounds_to(Fraction(total - CASE_MARKED, total), 4)
        for total in (77_428, 77_429)
    }
    assert set(shares.values()) == {Fraction("0.5576")}

    quotients = {
        total: rounds_to(THREE_WAY * Fraction(CASE_MARKED, total), 4)
        for total in (77_428, 77_429)
    }
    assert quotients == {77_428: Fraction("0.3825"), 77_429: Fraction("0.3824")}
    for value in quotients.values():
        assert Fraction("0.35") < value < Fraction("0.40")  # والحكمُ واحدٌ رغم ذلك


# ===================== ق٥ كما خُتِمت وق٥ كما نُفِّذت — راية ً راية
SEALED_SCOPE = ("حرفٌ عند ط٧", "مبنيُّ إحالة من معاجم ط٣")
IMPLEMENTED_SCOPE = ("حرفٌ عند ط٧", "فعلٌ عند ط٧", "مبنيُّ إحالة من معاجم ط٣")


def test_the_implemented_rule_is_wider_than_the_sealed_one() -> None:
    """الفعلُ في الشيفرة وليس في المختوم، وهو ٤٤٫٨٪ ممّا لا يُسمّى بحالة."""

    added = tuple(one for one in IMPLEMENTED_SCOPE if one not in SEALED_SCOPE)
    assert added == ("فعلٌ عند ط٧",)
    verbs_of_the_unmarked = Fraction("0.448")
    assert round(float(verbs_of_the_unmarked * UNMARKED)) == 19_342
    assert rounds_to(verbs_of_the_unmarked * Fraction(UNMARKED, ALIGNED_TOKENS), 4) == (
        Fraction("0.2498")
    )


def test_the_widening_alone_can_carry_a_quarter_of_the_whole_measure() -> None:
    """التوسيعُ غيرُ المختومِ يمسّ ٢٤٫٩٨٪ من المقام الرباعيّ — لا هامشًا.

    فإن قِيس (ج) بالشيفرة كما هي، لم يُحكَم على ما خُتِم بل على غيره؛ والفرقُ
    بينهما يبلغ ربعَ المقياس. ولذلك يُشغَّل الاثنان.
    """

    reach = Fraction("0.448") * Fraction(UNMARKED, ALIGNED_TOKENS)
    assert reach > Fraction("0.15")  # أكبرُ من الفارق الذي يطلبه (ج) نفسُه


# ================ المناطقُ الوسطى — شبكةٌ تامّةٌ على الشروط ذات الحدّين
TWO_THRESHOLD_PREDICTIONS = (
    "ج — التسجيل الأوّل: الدقّةُ الكلّيّة",
    "د — التسجيل الثالث: استردادُ صنف الممنوع",
    "هـ — التسجيل الثالث: انخفاضُ الثلاثيّ",
)
ZONE_COLUMNS = ("حدُّ النجاح", "حدُّ الإعلان", "ما بينهما")

MIDDLE_ZONES = Assignment(
    rows=TWO_THRESHOLD_PREDICTIONS,
    columns=ZONE_COLUMNS,
    cells=(
        ("ج — التسجيل الأوّل: الدقّةُ الكلّيّة", "حدُّ النجاح", "≥ ٨٨٪"),
        ("ج — التسجيل الأوّل: الدقّةُ الكلّيّة", "حدُّ الإعلان", "< ٨٥٪"),
        (
            "ج — التسجيل الأوّل: الدقّةُ الكلّيّة",
            "ما بينهما",
            "بلا حكم — ووقع المقيسُ فيها: ٨٦٫٤٥٪",
        ),
        ("د — التسجيل الثالث: استردادُ صنف الممنوع", "حدُّ النجاح", "≥ ٣٠٪"),
        ("د — التسجيل الثالث: استردادُ صنف الممنوع", "حدُّ الإعلان", "< ١٠٪"),
        (
            "د — التسجيل الثالث: استردادُ صنف الممنوع",
            "ما بينهما",
            "بلا حكم — عرضُها ٢٠ نقطة",
        ),
        ("هـ — التسجيل الثالث: انخفاضُ الثلاثيّ", "حدُّ النجاح", "< ٣ نقاط"),
        ("هـ — التسجيل الثالث: انخفاضُ الثلاثيّ", "حدُّ الإعلان", "> ٧ نقاط"),
        ("هـ — التسجيل الثالث: انخفاضُ الثلاثيّ", "ما بينهما", "بلا حكم — عرضُها ٤ نقاط"),
    ),
)


def test_three_predictions_leave_an_unnamed_middle_and_one_already_landed_there() -> (
    None
):
    """ثلاثةُ شروطٍ بحدّين، ومنطقةٌ وسطى في كلٍّ — وواحدةٌ وقع فيها المقيسُ فعلًا."""

    assert MIDDLE_ZONES.covers_the_grid()
    assert MIDDLE_ZONES.filled == 9
    landed = [
        row
        for row in TWO_THRESHOLD_PREDICTIONS
        if "وقع المقيسُ" in MIDDLE_ZONES.value_at(row, "ما بينهما")
    ]
    assert landed == ["ج — التسجيل الأوّل: الدقّةُ الكلّيّة"]
    assert MIDDLE_ZONES.indistinguishable_rows() == ()


def test_the_middle_zone_of_prediction_c_is_where_the_first_run_fell() -> None:
    """٨٦٫٤٥٪ بين ٨٥ و٨٨ — فلا التنبّؤُ صحّ ولا بندُ الإعلان لزم."""

    measured = Fraction("0.8645")
    assert Fraction("0.85") <= measured < Fraction("0.88")


# ============================== المخرجُ الخامس — قرارٌ يُعلَن لا يُؤخَذ صمتًا
DECLARED_CLASSES = ("raf'", "nasb", "jarr", "لا إعراب")
CODE_OUTCOMES = ("raf'", "nasb", "jarr", "لا إعراب", "لم يُحسَم")


def test_the_code_emits_one_more_outcome_than_the_registry_declares() -> None:
    """أربعةٌ مُعلَنةٌ وخمسةٌ مُخرَجة؛ و«لا حالةَ له» غيرُ «لا أدري»."""

    extra = tuple(one for one in CODE_OUTCOMES if one not in DECLARED_CLASSES)
    assert extra == ("لم يُحسَم",)
    assert len(CODE_OUTCOMES) == len(DECLARED_CLASSES) + 1


def test_the_fifth_outcome_moves_prediction_c_in_both_directions() -> None:
    """حسابُه «لا إعراب» يرفع (ج) بلا استحقاق، وحسابُه خطأً يخفضه — والفرقُ مقيس.

    وههنا يُقاس أثرُ القرار على مثالٍ مُعلَنٍ: لو امتنع النظامُ عن ألفِ رمزٍ
    «لا أدري»، وكانت كلُّها في غير الموسوم، لبلغ الفرقُ ١٫٢٩ نقطةً كاملة —
    أي أكثرَ من ثُمن ما يطلبه (ج). فليس القرارُ تفصيلًا.
    """

    deferred = 1_000
    swing = Fraction(deferred, ALIGNED_TOKENS)
    assert rounds_to(swing, 4) == Fraction("0.0129")
    assert swing > Fraction("0.15") / 12


# ====================================== شرطان يُضافان قبل التشغيل لا بعده
ORACLE = Oracle(
    name="QAC — الحالةُ الإعرابيّة على الرموز المحاذاة",
    source="quran-morphology، المصحفُ كلُّه",
    extraction="٧٧٬٤٢٨ رمزًا محاذًى؛ NOM/ACC/GEN وإلّا «لا إعراب»",
)

EXTRA = (
    Prediction(
        identifier="و — ق٥ المختومةُ وحدَها",
        statistic="الرباعيُّ بـ«حرف» و«مبنيّ الإحالة» دون الفعل",
        threshold=Fraction("0.7076"),
        direction=Direction.AT_LEAST,
        falsifies="دعوى (ج) على ما خُتِم، لا على ما نُفِّذ",
    ),
    Prediction(
        identifier="ز — ثمنُ ط٧",
        statistic="الفرقُ بين ق٥ على مخرَج ط٧ وعلى وسمٍ صحيح",
        threshold=Fraction("0.05"),
        direction=Direction.AT_MOST,
        falsifies="دعوى أنّ حكمَ (ج) حكمٌ على ق٥ لا على ط٧",
    ),
)

THIRD_SEAL = "ee1f32efb07d9718591f63f977faa1b0da4f08f59dee767a145f4648d5a7c797"


def test_the_two_added_conditions_are_sealed_now() -> None:
    """شرطان يفصلان ما خُتِم عمّا نُفِّذ، وق٥ عن ط٧ — ويُختَمان قبل التشغيل."""

    assert len(EXTRA) == 2
    fingerprint = seal(ORACLE, EXTRA)
    assert len(fingerprint) == 64
    assert fingerprint == THIRD_SEAL


def test_the_price_of_layer_seven_is_a_ceiling_question_not_an_excuse() -> None:
    """(ز) حدُّها أعلى لا أدنى: ثمنُ ط٧ **لا يتجاوز** ٥ نقاط، وإلّا فالحكمُ عليه."""

    assert EXTRA[1].direction is Direction.AT_MOST
    assert EXTRA[1].verdict(Fraction("0.03")) is Verdict.MET
    assert EXTRA[1].verdict(Fraction("0.09")) is Verdict.FALSIFIED


def test_nothing_here_is_a_measurement() -> None:
    """لا رقمَ ههنا من تشغيل: كلُّه مُشتَقٌّ أو منقولٌ أو مقروءٌ من الشيفرة."""

    with pytest.raises(AssertionError):
        assert False, "هذا الملفُّ يُحكَم به لا عليه، وأرقامُه سابقةٌ على النظر"
