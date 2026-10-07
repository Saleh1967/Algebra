"""R0d قبل تشغيلها: شبكةُ استئصالٍ تامّة، وسبعةُ شروطٍ مختومة.

**لم تُشغَّل بعد**: لا مدوَّنةَ ههنا ولا مخرَجَ ط٢ ولا وسمَ QAC. فما في هذا
الملفّ **سابقٌ على النظر** بتمامه: سقوفٌ تُشتَقّ من جدول البقايا المنشور،
وشروطٌ بحدودٍ واتّجاهاتٍ تُختَم الآن، وشبكةٌ تجعل الشرط (هـ) من التسجيل
الأوّل — «كلُّ قاعدةٍ تُقاس على حدة وبالترتيب» — **شرطَ إنشاءٍ لا وعدًا**.

`A_CONDITION_BROKEN_ONCE_IS_MADE_STRUCTURAL_NOT_PROMISED_AGAIN`: سقط (هـ)
في الدورة الأولى فنُشرت زيادتان مجموعتان لا ستّ، وبطل بسقوطه حكمُ شرطين.
فلا يُعاد الوعدُ به: يُقام جدولُ الاستئصال كاملًا (`assignment.Assignment`)،
سبعُ قواعدَ في أربعة أعمدة، وتمامُه مفحوص. وخانةُ «زيادتُها وحدَها» **تُملأ
سبعَ مرّات** وإلّا لم يُنشَر شيء.

`SIX_OF_SEVEN_INCREMENTS_WERE_NEVER_PUBLISHED`: ما يُخرِجه التعدادُ ولا يظهر
في السرد: قاعدةٌ واحدةٌ فقط من السبع نُشرت زيادتُها وحدَها (ق٣ حركةُ الحامل،
+٤٤٫٦٧). والستُّ الباقياتُ مجموعةٌ في رقمٍ واحد.

`A_PATCH_MAY_LOWER_WHAT_IT_FIXES`: ق٤ تُبدِّل **خطأً منتظمًا** (كلُّ منصوبٍ
من جمع المؤنّث يُقرَأ مجرورًا بالبناء) **بتمييزٍ يخطئ**: ومجرورُ الإضافة
سيُقرَأ منصوبًا. فأثرُها الصافي غيرُ معروفٍ قبل القياس، وحدُّها المختومُ صفرٌ
— «لا تُنقِص» — لا مكسبٌ مفترض.

`ABSTENTION_IS_THREE_NUMBERS_AND_ITS_EFFECT_HERE_IS_BOUNDED_NOT_KNOWN`: ق٦
تنقل المبنيَّ إلى عمودٍ ثالث. وسقفُها بالنقاط **صفرٌ بالبناء**: الامتناعُ لا
يُصيب. وكم يُزيل من الخطأ؟ ≤ ١٬٤٤٨؛ وكم يُزيل من الصواب؟ ≥ ٠. والصافي
**غيرُ محدَّدٍ** بلا حجم صنف المبنيّ — وهو رقمٌ لم يُنشَر.
"""

from __future__ import annotations

from fractions import Fraction

import pytest

from algebra.assignment import Assignment, AssignmentError
from algebra.evaluation import Tally
from algebra.reconciliation import rounds_to
from algebra.signified import Direction, Oracle, Prediction, Verdict, seal

MARKED_WORDS = 34_254
R0C_FINAL = Fraction("0.8645")
TASHKIL_ONLY = Fraction("0.7922")

# أصنافُ البقايا كما نُشِرت، والسقفُ نصيبُ الصنف من المقام
RESIDUAL_CLASSES = {
    "ضميرٌ متّصل": 3_015,
    "جمعُ مذكّرٍ سالم": 2_072,
    "جمعُ مؤنّثٍ سالم": 606,
    "علمٌ وممنوعٌ من الصرف": 482,
    "مثنّى": 229,
    "سواها": 714,
}


def ceiling(*classes: str) -> Fraction:
    """سقفُ قاعدةٍ: نصيبُ أصنافها من المقام — لو أصابت كلَّ ما تستهدفه."""

    return Fraction(sum(RESIDUAL_CLASSES[name] for name in classes), MARKED_WORDS)


# ============================================ شبكةُ الاستئصال — سبعٌ في أربع
RULES = (
    "ق٠ تقشيرُ الضمير",
    "ق١ لاحقةٌ بالحرف — ون وين وان",
    "ق٢ فضُّ الالتباس",
    "ق٣ حركةُ الحرف الحامل",
    "ق٤ جمعُ المؤنّث — ات",
    "ق٥ الممنوعُ من الصرف",
    "ق٦ امتناعُ المبنيّ",
)
COLUMNS = (
    "الصنفُ المستهدَف",
    "سقفُ النقاط",
    "حالُها في R0c",
    "زيادتُها المنشورةُ وحدَها",
)

ABLATION = Assignment(
    rows=RULES,
    columns=COLUMNS,
    forbidden=(("ق٢ فضُّ الالتباس", "سقفُ النقاط"),),
    cells=(
        ("ق٠ تقشيرُ الضمير", "الصنفُ المستهدَف", "ضميرٌ متّصل"),
        ("ق٠ تقشيرُ الضمير", "سقفُ النقاط", "٨٫٨٠"),
        ("ق٠ تقشيرُ الضمير", "حالُها في R0c", "منفَّذة"),
        ("ق٠ تقشيرُ الضمير", "زيادتُها المنشورةُ وحدَها", "غيرُ منشورة"),
        ("ق١ لاحقةٌ بالحرف — ون وين وان", "الصنفُ المستهدَف", "جمعُ مذكّرٍ سالم ومثنّى"),
        ("ق١ لاحقةٌ بالحرف — ون وين وان", "سقفُ النقاط", "٦٫٧٢"),
        ("ق١ لاحقةٌ بالحرف — ون وين وان", "حالُها في R0c", "منفَّذة"),
        (
            "ق١ لاحقةٌ بالحرف — ون وين وان",
            "زيادتُها المنشورةُ وحدَها",
            "غيرُ منشورة",
        ),
        ("ق٢ فضُّ الالتباس", "الصنفُ المستهدَف", "كلُّ ملتبسٍ بين نصبٍ وجرّ"),
        ("ق٢ فضُّ الالتباس", "حالُها في R0c", "منفَّذةٌ داخل ق١ وحدَها"),
        ("ق٢ فضُّ الالتباس", "زيادتُها المنشورةُ وحدَها", "غيرُ منشورة"),
        ("ق٣ حركةُ الحرف الحامل", "الصنفُ المستهدَف", "كلُّ مضبوطٍ في آخره"),
        ("ق٣ حركةُ الحرف الحامل", "سقفُ النقاط", "٤٤٫٦٧ مقيسةً لا مقدَّرة"),
        ("ق٣ حركةُ الحرف الحامل", "حالُها في R0c", "منفَّذة"),
        (
            "ق٣ حركةُ الحرف الحامل",
            "زيادتُها المنشورةُ وحدَها",
            "‎+٤٤٫٦٧ نقطة — وهي الوحيدةُ المنشورة",
        ),
        ("ق٤ جمعُ المؤنّث — ات", "الصنفُ المستهدَف", "جمعُ مؤنّثٍ سالم"),
        ("ق٤ جمعُ المؤنّث — ات", "سقفُ النقاط", "١٫٧٧"),
        ("ق٤ جمعُ المؤنّث — ات", "حالُها في R0c", "غيرُ منفَّذة — «ات» تسقط من الفرع"),
        ("ق٤ جمعُ المؤنّث — ات", "زيادتُها المنشورةُ وحدَها", "غيرُ منشورة"),
        ("ق٥ الممنوعُ من الصرف", "الصنفُ المستهدَف", "علمٌ وممنوعٌ من الصرف"),
        ("ق٥ الممنوعُ من الصرف", "سقفُ النقاط", "١٫٤١"),
        ("ق٥ الممنوعُ من الصرف", "حالُها في R0c", "غيرُ منفَّذةٍ بتمامها"),
        ("ق٥ الممنوعُ من الصرف", "زيادتُها المنشورةُ وحدَها", "غيرُ منشورة"),
        ("ق٦ امتناعُ المبنيّ", "الصنفُ المستهدَف", "المبنيُّ كما يسمه L3"),
        ("ق٦ امتناعُ المبنيّ", "سقفُ النقاط", "صفرٌ بالبناء — الامتناعُ لا يُصيب"),
        ("ق٦ امتناعُ المبنيّ", "حالُها في R0c", "غيرُ موجودة"),
        ("ق٦ امتناعُ المبنيّ", "زيادتُها المنشورةُ وحدَها", "غيرُ منشورة"),
    ),
)


def test_the_ablation_grid_is_total_and_one_cell_is_a_declared_impossibility() -> None:
    """سبعٌ في أربعٍ = ٢٨، منها ٢٧ مملوءةٌ وواحدةٌ ممتنعةٌ مُعلَنة."""

    assert len(RULES) * len(COLUMNS) == 28
    assert ABLATION.covers_the_grid()
    assert ABLATION.filled == 27
    assert ABLATION.forbidden_count == 1
    with pytest.raises(AssignmentError):
        ABLATION.value_at("ق٢ فضُّ الالتباس", "سقفُ النقاط")


def test_the_enabler_has_no_ceiling_of_its_own_and_that_is_a_claim() -> None:
    """فضُّ الالتباس لا يُطبَّق إلّا داخل قاعدةٍ أخرى، فسقفُه وحدَه ممتنعٌ.

    وإعلانُ الامتناع دعوًى تُنقَض: ينقضها تشغيلٌ يُظهِر لـق٢ زيادةً وهي
    وحدَها دون ق١ ودون ق٤ — وذلك محالٌ بالبناء في R0d، فيُفحَص بالحذف.
    """

    assert ("ق٢ فضُّ الالتباس", "سقفُ النقاط") in ABLATION.forbidden
    assert ABLATION.value_at("ق٢ فضُّ الالتباس", "حالُها في R0c").startswith("منفَّذةٌ داخل")


def test_six_of_seven_increments_were_never_published() -> None:
    """قاعدةٌ واحدةٌ نُشرت زيادتُها وحدَها، والستُّ الباقياتُ في رقمٍ مجموع."""

    published = [
        rule
        for rule in RULES
        if ABLATION.value_at(rule, "زيادتُها المنشورةُ وحدَها") != "غيرُ منشورة"
    ]
    assert len(published) == 1
    assert published[0] == "ق٣ حركةُ الحرف الحامل"


def test_two_of_the_seven_rules_were_declared_and_never_implemented() -> None:
    """ق٤ وق٥ مُسجَّلتان وغائبتان، وق٦ لم تُسجَّل أصلًا وهي علاجُ أكبر صنف."""

    absent = [
        rule
        for rule in RULES
        if "غيرُ منفَّذة" in ABLATION.value_at(rule, "حالُها في R0c")
        or ABLATION.value_at(rule, "حالُها في R0c") == "غيرُ موجودة"
    ]
    assert absent == [
        "ق٤ جمعُ المؤنّث — ات",
        "ق٥ الممنوعُ من الصرف",
        "ق٦ امتناعُ المبنيّ",
    ]


def test_the_ceilings_are_derived_from_the_published_residual_table() -> None:
    """السقوفُ ليست تقديرًا: نصيبُ كلّ صنفٍ من المقام، وأربعتُها تُعاد."""

    assert rounds_to(ceiling("ضميرٌ متّصل"), 4) == Fraction("0.0880")
    assert rounds_to(ceiling("جمعُ مذكّرٍ سالم", "مثنّى"), 4) == Fraction("0.0672")
    assert rounds_to(ceiling("جمعُ مؤنّثٍ سالم"), 4) == Fraction("0.0177")
    assert rounds_to(ceiling("علمٌ وممنوعٌ من الصرف"), 4) == Fraction("0.0141")


def test_the_bundle_realised_a_fraction_of_its_own_ceiling() -> None:
    """سقفُ الحزمة المنفَّذة ١٨٫٧٠ نقطةً، والمقيسُ +٧٫٢٣ — أي ٣٨٫٧٪ منه.

    وهذا وجهٌ ثالثٌ للحكم على (أ) و(ب): ليست الحزمةُ عاجزةً عن ١٠ نقاطٍ لأنّ
    اللغةَ تأبى، بل لأنّها بلغت أقلَّ من خُمسَي ما تستهدفه.
    """

    reachable = ceiling(
        "ضميرٌ متّصل", "جمعُ مذكّرٍ سالم", "مثنّى", "جمعُ مؤنّثٍ سالم", "علمٌ وممنوعٌ من الصرف"
    )
    assert rounds_to(reachable, 4) == Fraction("0.1870")

    realised = R0C_FINAL - TASHKIL_ONLY
    assert rounds_to(realised, 4) == Fraction("0.0723")
    assert round(float(realised / reachable), 3) == 0.387


def test_abstention_on_the_built_in_class_is_bounded_not_known() -> None:
    """ق٦ تُزيل ≤١٬٤٤٨ خطأً و≥٠ صوابًا؛ والصافي مجهولٌ بلا حجم الصنف.

    والثلاثةُ التي تلزم عند الامتناع محسوبةٌ ههنا على **الحدّ الأقصى** وحدَه،
    وتُعلَن حدًّا لا تقديرًا: التغطيةُ ≥ ٩٥٫٧٧٪، والدقّةُ حيث تُسنَد ≤ ٩٠٫٢٧٪.
    """

    errors = round(float((1 - R0C_FINAL) * MARKED_WORDS))
    assert errors == 4_641
    mabni_errors = round(errors * 0.312)
    assert mabni_errors == 1_448

    best = Tally(
        correct=MARKED_WORDS - errors,
        wrong=errors - mabni_errors,
        abstained=mabni_errors,
    )
    assert round(float(best.coverage), 4) == 0.9577
    assert round(float(best.precision_where_it_fires), 4) == 0.9027
    assert best.accuracy_charging_abstention == Fraction(
        MARKED_WORDS - errors, MARKED_WORDS
    )
    assert rounds_to(best.accuracy_charging_abstention, 4) == R0C_FINAL


# ====================================== التسجيلُ الثاني — يُختَم قبل التشغيل
ORACLE = Oracle(
    name="QAC — الحالةُ الإعرابيّة",
    source="quran-morphology، المصحفُ كلُّه",
    extraction="٣٤٬٢٥٤ كلمةً موسومةً بحالة؛ والوحدةُ كلمةٌ لا مقطع",
)


def _at_least(name: str, statistic: str, threshold: str, falsifies: str) -> Prediction:
    return Prediction(
        identifier=name,
        statistic=statistic,
        threshold=Fraction(threshold),
        direction=Direction.AT_LEAST,
        falsifies=falsifies,
    )


REGISTRY = (
    _at_least(
        "أ' — ق٠ وحدَها، بالحدّ الأصليّ",
        "زيادةُ الدقّة عند حذف ق٠ وحدَها",
        "0.05",
        "الحكمَ المعلَّقَ على (أ) في التسجيل الأوّل، وقد كان VOID لتعذُّر القياس",
    ),
    _at_least(
        "ب' — ق١ وق٢ وق٤ معًا، بالحدّ الأصليّ",
        "زيادةُ الدقّة بعد ق٠",
        "0.05",
        "الحكمَ المعلَّقَ على (ب)، وقد كان VOID للسبب نفسِه",
    ),
    _at_least(
        "ك١ — ق٥ الممنوعُ من الصرف",
        "زيادةُ الدقّة عند حذف ق٥ وحدَها",
        "0.01",
        "دعوى أنّ الفتحةَ الخالصةَ بعد حرف الجرّ علامةٌ كافيةٌ للمنع من الصرف",
    ),
    _at_least(
        "ك٢ — ق٤ لا تُنقِص",
        "فرقُ الدقّة الكلّيّة عند حذف ق٤ وحدَها",
        "0",
        "دعوى أنّ تمييزًا يخطئ خيرٌ من خطأٍ منتظمٍ ههنا",
    ),
    _at_least(
        "ك٣ — R0d الكلّيّة",
        "دقّةٌ كلّيّةٌ على المُسنَد وغيرِ المُسنَد معًا",
        "0.88",
        "دعوى أنّ تنفيذَ ما سُجّل يبلغ الحدَّ الذي سقط عليه (ج) في R0c",
    ),
    _at_least(
        "ك٤ — الدقّةُ حيث تُسنَد",
        "الإصابةُ في المُسنَد وحدَه بعد ق٦",
        "0.90",
        "دعوى أنّ الامتناعَ عن المبنيّ يُنقّي المُسنَد",
    ),
    _at_least(
        "ك٥ — التغطية",
        "نصيبُ المُسنَد من المقام بعد ق٦",
        "0.93",
        "دعوى أنّ ثمنَ ذلك التنقية محتمَل",
    ),
)

SECOND_SEAL = "ff690f9f6ab3135c95c825bc1ea2841b4c77e9129840b00a314b06d732abe1e8"


def test_the_second_registry_is_sealed_before_anything_is_run() -> None:
    """سبعةُ شروطٍ بحدودٍ واتّجاهاتٍ، وبصمتُها تُثبَّت في التزامٍ لا رقمَ فيه."""

    assert len(REGISTRY) == 7
    assert len({one.identifier for one in REGISTRY}) == 7
    fingerprint = seal(ORACLE, REGISTRY)
    assert len(fingerprint) == 64
    assert fingerprint == SECOND_SEAL


def test_the_two_revived_predictions_keep_their_original_thresholds() -> None:
    """أ' وب' بحدّ ٠٫٠٥ نفسِه: لا يُخفَّض حدٌّ سقط، وإنّما يُجعَل قابلًا للقياس.

    وهذا هو الفرقُ بين إعادة السؤال وبين تليين الشرط: الحدُّ واحدٌ، والذي
    تغيّر هو **آلةُ القياس** — شبكةُ الاستئصال تعطي زيادةَ كلِّ قاعدةٍ وحدَها.
    """

    revived = [one for one in REGISTRY if one.identifier.startswith(("أ'", "ب'"))]
    assert len(revived) == 2
    assert all(one.threshold == Fraction("0.05") for one in revived)


def test_a_lowered_threshold_would_be_caught_by_the_seal() -> None:
    """تليينُ حدٍّ بعد النظر يُعرَف بتغيُّر البصمة، لا بحسن الظنّ."""

    softened = Prediction(
        identifier=REGISTRY[4].identifier,
        statistic=REGISTRY[4].statistic,
        threshold=Fraction("0.865"),
        direction=REGISTRY[4].direction,
        falsifies=REGISTRY[4].falsifies,
    )
    changed = (*REGISTRY[:4], softened, *REGISTRY[5:])
    assert seal(ORACLE, changed) != SECOND_SEAL
    assert softened.verdict(R0C_FINAL) is Verdict.FALSIFIED  # ولا ينجو حتى بالتليين


def test_the_dropped_rules_alone_could_carry_the_failed_threshold() -> None:
    """ق٥ وق٤ سقفُهما معًا ٣٫١٨ نقطةً، والفجوةُ إلى ٨٨٪ ١٫٥٥ — فالحدُّ في مداهما.

    وهذا لا يقول إنّهما ستبلغانه، بل إنّ الحكمَ «القواعدُ لا تكفي» **سابقٌ
    لأوانه** ما دام المُسجَّلُ لم يُنفَّذ. وك٣ هو ما يحسمه.
    """

    reachable = ceiling("جمعُ مؤنّثٍ سالم", "علمٌ وممنوعٌ من الصرف")
    assert rounds_to(reachable, 4) == Fraction("0.0318")
    gap = Fraction("0.88") - R0C_FINAL
    assert rounds_to(gap, 4) == Fraction("0.0155")
    assert reachable > gap
