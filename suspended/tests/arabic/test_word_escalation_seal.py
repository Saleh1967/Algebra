"""**ختمٌ قبل النظر**: الوحدةُ تنتهي عند حدّ الكلمة — عدًّا وتصعيدًا.

**لم يُشغَّل شيءٌ على المدوّنة بعد.** والآلةُ جُرّبت على شريحةٍ من ثمانين
سطرًا: ١٬١٧١ كلمة، ٦٧٨ هيكلًا، غامضُها ٠٫٠٥٠١ بكتلةٍ ٠٫١٦٦٥؛ والدَّينُ على
المشهود ٧٫٠٩١٦ بلا سياقٍ و٧٫٦٠٠٣ بسياق (الفرقُ **+٠٫٥٠٨٧**)؛ ونصيبُ الكلم
التي صارت رمزًا واحدًا ٠٫١٥٩٧، والعابرُ صفرٌ، والانحرافُ صفر. **ويُعلَن ذلك
ههنا** فما رأيتُه قبل الختم لا يُخفى. **ولا يُستخرَج من شريحةٍ بهذا الصغر
شيءٌ عن أرقام المدوّنة** — ولا سيّما الغموضُ والدَّين، فهما يكبران بالمادّة.

**الدعوى المعروضةُ للعدّ**: الجشعُ المُرخَّصُ من `69a1c10c…` إلى
`0c070831…` جشعُ **مواضع** — يرخّص وحداتِ (حرفٍ × حال). والعضويّةُ
الصنفيّةُ خاصّةُ **كلمةٍ** لا موضع. فالوحدةُ تنتهي عند حدّ الكلمة،
والصنفُ يقف فوقها. **وأربعةُ أعدادٍ تُعرَض فتُعَدّ**: ٧٧٬٨٠١ كلمة،
و١٤٬٨٧٠ هيكلًا، و٢٬٠٩٩ غامضًا، بكتلةٍ ٣٧٬٥٤١.

**والهيكلُ مُعرَّفٌ آليًّا**: وحداتُ الكلمة **بلا حالها** — لا حرفَ يُسمّى
ولا حالَ تُفسَّر. والغامضُ ما حمل أكثرَ من صورةٍ مضبوطةٍ واحدة.

**والتصعيدُ**: آلةُ `69a1c10c…` بقيدٍ واحد — **لا دمجةَ تعبر حدَّ الكلمة**.

**والدَّينان يُسعَّران محجوزَين**، ويُفصَل فيهما ثمنُ **غموضِ** المفتاح عن
ثمنِ **غيابِه**، فلا يُضخَّم الدَّينُ بما ليس منه.

**ولا اسمٌ لصنفٍ يدخل**: لا يُقال اسمٌ ولا فعلٌ ولا حرف — تُعَدّ الصورُ
على الهيكل الواحد وتُعرَض **ببايتاتها**، ولا يُسمّى فرقُها.
"""

from __future__ import annotations

from fractions import Fraction

from algebra.signified import Direction, Oracle, Prediction, seal

BY_LICENCE = 1_400_392
TOKENS = 77_801
SKELETONS = 14_870
VAGUE = 2_099
VAGUE_MASS = 37_541
EXEMPLAR = 22

ORACLE = Oracle(
    name="حدُّ الكلمة سقفًا للجشع — عدُّ الهياكل وتسعيرُ الدَّينين",
    source="quran-simple-enhanced.txt — البصمة 37633090…",
    extraction=(
        "من التقشير إلى ١١٢: تُبنى الكلمُ بالفصل عند البنيويّ، والهيكلُ "
        "وحداتُها بلا حالها؛ فيُعَدّ الكلمُ والهياكلُ والغامضُ منها "
        "وكتلتُه. ثمّ تُعاد آلةُ `69a1c10c…` بقيدٍ واحدٍ — لا دمجةَ تعبر "
        "حدَّ الكلمة — ويُقاس ما صار من الكلم رمزًا واحدًا. ويُسعَّر "
        "`H(الصورة | الهيكل)` و`H(الصورة | الهيكل، هيكلِ ما قبلها)` "
        "محجوزَين بلابلاس شطرًا بشطر، مفصولًا فيهما المشهودُ مفتاحُه "
        "عن غيره"
    ),
)

PREDICTIONS = (
    Prediction(
        identifier="ك١",
        statistic="مواضعُ الخلاف بين بسطِ الرموز بالهجاء ومجرى L₀",
        threshold=Fraction(0),
        direction=Direction.AT_MOST,
        falsifies="الرجعةَ: أيُّ خلافٍ ضياعٌ لا ضغط",
    ),
    Prediction(
        identifier="ك٢",
        statistic="عددُ الالتزامات التي لم تنزل عندها التكلفةُ المحجوزة",
        threshold=Fraction(0),
        direction=Direction.AT_MOST,
        falsifies="أنّ الرخصةَ بقيت للدمجة الواحدة تحت القيد",
    ),
    Prediction(
        identifier="ك٣",
        statistic="أقصى |الجملة من العدّادات − الجملة من الآيات| (بتًّا)",
        threshold=Fraction(1, 1000),
        direction=Direction.AT_MOST,
        falsifies=(
            "الآلةَ لا المادّة: عدُّ الأزواج تحت القيد أدقُّ موضعًا، "
            "وانحرافُه عن الآيات عطلُ آلةٍ يردّ التشغيل"
        ),
    ),
    Prediction(
        identifier="ك٤",
        statistic="وقوعاتٌ عابرةٌ لحدّ الكلمة عند الوقوف",
        threshold=Fraction(0),
        direction=Direction.AT_MOST,
        falsifies=(
            "الحسابَ: القيدُ يمنع العبورَ بالبناء، فوقوعُ عابرٍ واحدٍ "
            "يعني أنّ القيدَ لم يُطبَّق، ويُردّ الشطرُ كلُّه"
        ),
    ),
    Prediction(
        identifier="ك٥",
        statistic="|عددُ الكلم − ٧٧٬٨٠١|",
        threshold=Fraction(0),
        direction=Direction.AT_MOST,
        falsifies=(
            "العددَ المعروضَ لا الدعوى: فإن خالف فالفصلُ عند البنيويّ "
            "غيرُ الفصل الذي عُدَّ به، ويُنشَر تعريفي وعددُه بلا تجميل"
        ),
    ),
    Prediction(
        identifier="ك٦",
        statistic="|عددُ الهياكل المتمايزة − ١٤٬٨٧٠|",
        threshold=Fraction(0),
        direction=Direction.AT_MOST,
        falsifies=(
            "تعريفَ الهيكل: وحداتُ الكلمة بلا حالها. وتوسيعُ الشدّة "
            "يُضاعِف وحدةً، فقد يفترق العدّان لذلك وحدَه — ويُقال"
        ),
    ),
    Prediction(
        identifier="ك٧",
        statistic="|عددُ الهياكل الغامضة − ٢٬٠٩٩|",
        threshold=Fraction(0),
        direction=Direction.AT_MOST,
        falsifies="العددَ المعروضَ للغموض على تعريفي للهيكل والصورة",
    ),
    Prediction(
        identifier="ك٨",
        statistic="|كتلةُ الهياكل الغامضة من الكلم − ٣٧٬٥٤١|",
        threshold=Fraction(0),
        direction=Direction.AT_MOST,
        falsifies=(
            "الدعوى الكبرى في العرض: أنّ نصفَ الكلم يقف على هياكلَ لا "
            "تعيّن حروفُها ضبطَها. وخلافُ الكتلة يُنشَر برقمه"
        ),
    ),
    Prediction(
        identifier="ك٩",
        statistic="|كلمُ الهيكل ذي الوحدات الثلاث المعروض − ٢٢|",
        threshold=Fraction(0),
        direction=Direction.AT_MOST,
        falsifies=(
            "المثالَ المعروضَ نفسَه: فإن خالف عددُه فالهيكلُ المعدودُ "
            "غيرُ الهيكل المعروض، ويُعرَض ما عندي بصوره وبايتاتها"
        ),
    ),
    Prediction(
        identifier="ك١٠",
        statistic="الجملةُ المحجوزةُ عند الوقوف تحت القيد (بتًّا)",
        threshold=Fraction(BY_LICENCE),
        direction=Direction.AT_LEAST,
        falsifies=(
            "أنّ منعَ العبور يكلّف ولا يوفّر؛ فإن نزلت الجملةُ تحت "
            "١٬٤٠٠٬٣٩٢ فحدُّ الكلمة **يُعين** الضغطَ لا يقيّده، وذلك "
            "خبرٌ يقلب قراءةَ العبور في `0b8eae76…` كلَّها"
        ),
    ),
    Prediction(
        identifier="ك١١",
        statistic="نصيبُ الكلم التي صارت رمزًا واحدًا عند الوقوف",
        threshold=Fraction(1, 10),
        direction=Direction.AT_LEAST,
        falsifies=(
            "أنّ التصعيدَ يبلغ الكلمةَ في شيءٍ يُعتدّ به؛ فإن نزل النصيبُ "
            "عن العُشر فالجشعُ **لا يبلغ الكلمةَ** أصلًا، فضلًا عمّا فوقها"
        ),
    ),
    Prediction(
        identifier="ك١٢",
        statistic="الدَّينُ المعجميُّ محجوزًا على ما شُهِد مفتاحُه (بتًّا للكلمة)",
        threshold=Fraction(1, 1000),
        direction=Direction.AT_LEAST,
        falsifies=(
            "أنّ ثَمَّ دَينًا أصلًا: فإن كان صفرًا فالهيكلُ يعيّن الصورةَ "
            "على المشهود، ويسقط العرضُ كلُّه"
        ),
    ),
    Prediction(
        identifier="ك١٣",
        statistic="الدَّينُ بسياقٍ − الدَّينُ بلا سياق، على المشهود (بتًّا)",
        threshold=Fraction(0),
        direction=Direction.AT_LEAST,
        falsifies=(
            "قولَ العرض إنّ السياقَ **دَينٌ أعلى**؛ فإن نزل الدَّينُ "
            "بسياقٍ فهيكلُ ما قبلها **يشتري** شيئًا محجوزًا، ويكون "
            "السياقُ خصمًا لا دَينًا — على هذا التشكيل وحدَه"
        ),
    ),
)

DIGEST = "2a849c9a192037ad5ca0876f431ac2a028c7f6778e00b123a0c8e46e8eebd8a5"
"""يُثبَّت بعد أوّل اشتقاق، ولا يُمَسّ بعدَه."""


def test_the_seal_is_recomputed_from_the_written_conditions() -> None:
    """البصمةُ تُشتَقّ من الشروط لا تُنقَل."""

    assert seal(ORACLE, PREDICTIONS) == DIGEST


def test_the_presented_count_is_tested_not_argued() -> None:
    """أربعةُ أعدادٍ عُرِضت، فأربعةُ شروطٍ تُقابِلها بالمساواة."""

    counted = [one for one in PREDICTIONS if one.identifier in {"ك٥", "ك٦", "ك٧", "ك٨"}]
    assert len(counted) == 4
    for one in counted:
        assert one.threshold == Fraction(0)
        assert one.direction is Direction.AT_MOST
    assert len(PREDICTIONS) == 13


def test_no_class_is_named_anywhere_in_the_seal() -> None:
    """لا اسمَ ولا فعلَ ولا حرف — تُعَدّ الصورُ وتُعرَض ببايتاتها."""

    assert __doc__ is not None
    for one in PREDICTIONS:
        body = f"{one.statistic} {one.falsifies}"
        assert "اسمٌ أم" not in body
    assert "ولا يُسمّى فرقُها" in __doc__
    assert "ببايتاتها" in __doc__


def test_the_two_debts_are_priced_apart_from_absence() -> None:
    """ثمنُ غموضِ المفتاح غيرُ ثمنِ غيابِه — ولا يُخلَطان."""

    assert "المشهودُ مفتاحُه" in ORACLE.extraction
    debt = next(one for one in PREDICTIONS if one.identifier == "ك١٢")
    context = next(one for one in PREDICTIONS if one.identifier == "ك١٣")
    assert "شُهِد مفتاحُه" in debt.statistic
    assert "على المشهود" in context.statistic
    assert "دَينٌ أعلى" in context.falsifies


def test_the_slice_i_saw_before_sealing_is_declared() -> None:
    """ما رأيتُه قبل الختم مكتوبٌ فيه — ولا يُخفى بعد النظر."""

    assert __doc__ is not None
    for one in ("١٬١٧١", "٠٫٠٥٠١", "+٠٫٥٠٨٧", "٠٫١٥٩٧", "ثمانين"):
        assert one in __doc__, one
