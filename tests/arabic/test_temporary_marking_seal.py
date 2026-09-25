"""**ختمٌ قبل النظر**: عزلُ **الوسم الأبديّ** — أهو سببُ خسارة الترخيص؟

**لم يُشغَّل شيءٌ على المدوّنة بعد.** والآلةُ جُرّبت على شريحةٍ من ثمانين
سطرًا فقط (رُفِعت وسومٌ والتُزِمت بعد رفعها)، **ولا يُستخرَج منها شيءٌ عن
أرقام المدوّنة**.

**ما يُعزَل**: في `69a1c10c…` خسر الترخيصُ بتّةً بتّة **٥٬٧٥٤** بتًّا عن
الكتليّ، وكتبتُ أنّ السببَ المقترَح **الوسمُ الأبديُّ للمرفوض** — وكتبتُ
معه أنّه **غيرُ معزولٍ بعد**، وأنّه يُوسَم كذلك **حتّى يُعزَل بختمٍ خاصّ**.
وهذا هو.

**والتغييرُ واحدٌ لا غير**: الوسمُ **يُرفَع عند كلّ التزام**، فالزوجُ الذي
لا يربح في حالٍ يُعاد اقتراحُه في حالٍ أخرى. وما عدا ذلك — القسمةُ
والترميزُ والتكلفةُ والمحجوزةُ والشفعُ والوتر — **هو هو**.

**وعمقُ البحث محدودٌ معلنٌ** (أعلى ٢٤ مقترَحًا في كلّ حال): فما يُبلَغ
**حدٌّ أدنى** لِما يبلغه بحثٌ أعمق. فإن بلغ التكلفةَ الكتليّةَ فالعزلُ تامّ،
وإن لم يبلغها **فلا يُقال إنّها لا تُبلَغ** بل إنّها لم تُبلَغ عند هذا العمق.

**والزوجُ المرصود** هو الذي رُفِض أوّلًا في `69a1c10c…` — يُعرَف برقمه في
ترتيب الأبجديّة نفسِه، ولا يُسمّى بغيره.

**ولا اسمَ لغويٌّ يدخل**: بتّاتٌ وعَرضٌ ووقوعاتٌ وتكلفةٌ فقط.
"""

from __future__ import annotations

from fractions import Fraction

from algebra.signified import Direction, Oracle, Prediction, seal

BY_PERMANENT = 1_400_392
BY_BLOCK = 1_394_638

ORACLE = Oracle(
    name="عزلُ الوسم الأبديّ عن خسارة الترخيص بتّةً بتّة",
    source="quran-simple-enhanced.txt — البصمة 37633090…",
    extraction=(
        "آلةُ `69a1c10c…` بعينها، وفيها تغييرٌ واحد: الوسمُ يُرفَع عند كلّ "
        "التزامٍ فيُعاد اقتراحُ المرفوض في حالٍ أخرى؛ ويُبحَث في كلّ حالٍ "
        "أعلى ٢٤ مقترَحًا فقط، ويُوقَف عند حالٍ لا يربح فيها واحدٌ منها. "
        "وتُقابَل العدّاداتُ بآلة `34133d54…` كلَّ خمس مئةِ التزام"
    ),
)

PREDICTIONS = (
    Prediction(
        identifier="س١",
        statistic=("أقصى |الجملة من العدّادات − الجملة من الآيات| عند نقاط الفحص (بتًّا)"),
        threshold=Fraction(1, 1000),
        direction=Direction.AT_MOST,
        falsifies=(
            "الآلةَ لا المادّة: العدّاداتُ اختصارُ حسابٍ لا تعريفٌ جديد، "
            "فانحرافُها يردّ التشغيلَ كلَّه"
        ),
    ),
    Prediction(
        identifier="س٢",
        statistic="مواضعُ الخلاف بين بسطِ الرموز بالهجاء ومجرى L₀",
        threshold=Fraction(0),
        direction=Direction.AT_MOST,
        falsifies="الرجعةَ: أيُّ خلافٍ ضياعٌ لا ضغط",
    ),
    Prediction(
        identifier="س٣",
        statistic="عددُ الالتزامات التي لم تنزل عندها التكلفةُ المحجوزة",
        threshold=Fraction(0),
        direction=Direction.AT_MOST,
        falsifies=(
            "أنّ الرخصةَ بقيت للدمجة الواحدة: رفعُ الوسم يوسّع البحثَ "
            "ولا يرخّص خاسرًا، فالتزامٌ بلا نزولٍ عطلُ آلة"
        ),
    ),
    Prediction(
        identifier="س٤",
        statistic="عددُ الالتزامات عند الوقوف",
        threshold=Fraction(2_663),
        direction=Direction.AT_LEAST,
        falsifies=(
            "دعوايَ أنّ الوسمَ الأبديَّ كان يُنفِد الأزواجَ مبكّرًا؛ فإن لم "
            "يتجاوز رفعُ الوسم ٢٬٦٦٢ فالوقوفُ ليس من الوسم بل من الرخصة"
        ),
    ),
    Prediction(
        identifier="س٥",
        statistic="الجملةُ المحجوزةُ عند الوقوف (بتًّا)",
        threshold=Fraction(BY_PERMANENT - 1),
        direction=Direction.AT_MOST,
        falsifies=(
            "أنّ رفعَ الوسم يُحسِّن شيئًا أصلًا؛ فإن لم ينزل عن ١٬٤٠٠٬٣٩٢ "
            "فالوسمُ الأبديُّ لم يكن يكلّف شيئًا، وتسقط دعوايَ كلُّها"
        ),
    ),
    Prediction(
        identifier="س٦",
        statistic="الجملةُ المحجوزةُ عند الوقوف (بتًّا) — مقابلَ الكتليّ",
        threshold=Fraction(BY_BLOCK),
        direction=Direction.AT_MOST,
        falsifies=(
            "أنّ الوسمَ الأبديَّ **وحدَه** سببُ الخسارة؛ فإن لم تُبلَغ "
            "التكلفةُ الكتليّةُ فالخسارةُ من الترخيص نفسِه — أي أنّ الجشعَ "
            "المحلّيَّ يردّ درجاتٍ يحتاجها ما فوقها — لا من الوسم. "
            "ولا يُقال حينئذٍ إنّها لا تُبلَغ، بل إنّها لم تُبلَغ عند عمق ٢٤"
        ),
    ),
    Prediction(
        identifier="س٧",
        statistic="عددُ الأزواج التي رُفِضت ثمّ التُزِمت بعد رفع وسمها",
        threshold=Fraction(1),
        direction=Direction.AT_LEAST,
        falsifies=(
            "أنّ رفعَ الوسم يفعل شيئًا: فإن لم يُلتزَم مرفوضٌ قطُّ فالوسمُ "
            "الأبديُّ والمؤقّتُ سواءٌ، والتشغيلان نسخةٌ واحدة"
        ),
    ),
    Prediction(
        identifier="س٨",
        statistic="رتبةُ الالتزام التي التُزِم عندها الزوجُ المرصود",
        threshold=Fraction(1),
        direction=Direction.AT_LEAST,
        falsifies=(
            "أنّ الزوجَ الذي رُفِض أوّلًا يصير رابحًا في حالٍ أخرى؛ فإن لم "
            "يُلتزَم قطُّ فرفضُه لم يكن من الحال بل من الزوج، وصفرٌ ههنا "
            "يُقرأ «لم يُبلَغ» لا «ممتنع» لأنّ البحثَ محدودُ العمق"
        ),
    ),
)

DIGEST = "89b59b10009e801a150822cdd9e40ce572bbe6ccd65ada9cb44c700fa1789d92"
"""يُثبَّت بعد أوّل اشتقاق، ولا يُمَسّ بعدَه."""


def test_the_seal_is_recomputed_from_the_written_conditions() -> None:
    """البصمةُ تُشتَقّ من الشروط لا تُنقَل."""

    assert seal(ORACLE, PREDICTIONS) == DIGEST


def test_the_isolation_changes_exactly_one_thing() -> None:
    """رفعُ الوسم وحدَه — وما عداه منقولٌ بنصّه من الختم السابق."""

    assert "تغييرٌ واحد" in ORACLE.extraction
    assert "الوسمُ يُرفَع عند كلّ التزام" in ORACLE.extraction
    assert len(PREDICTIONS) == 8


def test_the_crux_is_the_sixth_and_it_can_fall_either_way() -> None:
    """س٦ هو العزلُ نفسُه: أيُبلَغ الكتليُّ برفع الوسم أم لا؟"""

    crux = next(one for one in PREDICTIONS if one.identifier == "س٦")
    assert crux.threshold == Fraction(BY_BLOCK)
    assert crux.direction is Direction.AT_MOST
    assert "لم تُبلَغ عند عمق ٢٤" in crux.falsifies


def test_a_limited_search_reports_a_floor_not_a_ceiling() -> None:
    """عمقُ البحث محدودٌ معلن — فالمبلوغُ حدٌّ أدنى، ولا يُقال «ممتنع»."""

    for identifier in ("س٦", "س٨"):
        one = next(item for item in PREDICTIONS if item.identifier == identifier)
        assert "لم تُبلَغ" in one.falsifies or "لم يُبلَغ" in one.falsifies
