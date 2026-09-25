"""**ختمٌ قبل النظر**: قاعدةُ الفصل المُودَعةُ تُقاس بالمحجوز، بلا شاهد.

**لم تُشغَّل على المدوّنة بعد.** والآلةُ جُرّبت على شريحةٍ من ثمانين سطرًا:
فُصِل **٠٫٦٠٥٥** من الألفاظ، والرجعةُ صفر. **ويُعلَن ذلك ههنا.** وأرقامُ
الثمن على الشريحة **لا تُقارَن بأرقام المدوّنة**، فقد قُورِنت في التجريب
بثوابتَ من المُجمَّد فخرجت مقابلةٌ بلا معنًى — وهي تجريبُ آلةٍ لا قياس.

**المواصفةُ غيرُ موقَّعة**: صاغتها الآلةُ مسوَّدةً في
`deposits/separation_rule.md`. **فتُقاس ولا تُرقّي مستوًى**: حالُ الكلمة
المفردة في `tools/ladder_seal.py` يبقى `UNCLASSIFIED` مهما كان الرقم،
والترقيةُ تحتاج توقيعًا على **القاعدة** لا على **قياسها**.

**وتُقرَأ القاعدةُ من المواصفة لا تُكتَب في الشفرة**: الأنماطُ تُستخرَج
من جداولها بنمطٍ صريح، فإن بُدِّلت تبدّل التشغيلُ ولا تفارقه صامتة.

**والحكمُ بالمحجوز لا بشاهد**: لا جردَ صحيحًا يُقابَل به، **فلا تُقاس
دقّتُها ولا يُدَّعى**. وتُقاس **منفعتُها**: إن التقط الفصلُ بنيةً تكرّرت
الأصولُ، فنقص نصيبُ المرتدّ ونزل الثمنُ المحجوز.

**وأخطاؤها متروكةٌ ظاهرة**: لا معجمَ ولا سياقَ ولا استثناءَ مسمّى — فما
يشبه الملتصقَ يُقشَر وإن لم يكن. **وذلك مقصودٌ**، لئلّا تُخفى بالاستثناء
حتّى تصدق.

**ولا اسمٌ لصنفٍ يدخل**: وحداتٌ وأصولٌ وبتّات.
"""

from __future__ import annotations

from fractions import Fraction

from algebra.signified import Direction, Oracle, Prediction, seal

BY_TOKEN = 4.2118
BY_SYMBOL = 3.6549
TOKEN_MISSING = 0.1972
TOKEN_KINDS = 17_909

ORACLE = Oracle(
    name="قاعدةُ الفصل المُودَعةُ مقيسةً بالمحجوز",
    source="quran-simple-enhanced.txt — البصمة 37633090…",
    extraction=(
        "تُقرأ الأنماطُ من جداول `deposits/separation_rule.md` ثمّ تُطبَّق "
        "على مجرى وحدات ١١٢ داخلَ كلّ لفظ: مقدّماتٌ بثلاث رتبٍ مرّةً "
        "لكلّ رتبة، ولاحقةٌ واحدة، بشرط ألّا تقلّ البقيّةُ عن وحدتين. "
        "ثمّ يُقاس المستوى المفصولُ بثمن هوفمان ملحَقًا ومحجوزًا (المرتدُّ "
        "يُشحَن هروبًا ثمّ هجاءً بالـ١١٢) ويُقابَل بمستوى اللفظ"
    ),
)

PREDICTIONS = (
    Prediction(
        identifier="ص١",
        statistic="عددُ الألفاظ التي لا يعيدها وصلُ كلماتها",
        threshold=Fraction(0),
        direction=Direction.AT_MOST,
        falsifies=(
            "الرجعةَ: الفصلُ تقطيعٌ لا تبديل، فلفظٌ واحدٌ لا يُستعاد "
            "عطلُ آلةٍ يردّ القاعدةَ وقياسَها معًا"
        ),
    ),
    Prediction(
        identifier="ص٢",
        statistic="أقصى (L − H) على المستوى المفصول (بتًّا للرمز)",
        threshold=Fraction(999, 1000),
        direction=Direction.AT_MOST,
        falsifies="حدَّ هوفمان الأعلى `L < H + 1` على هذا المستوى",
    ),
    Prediction(
        identifier="ص٣",
        statistic="نصيبُ الألفاظ التي فُصِلت إلى أكثر من كلمة",
        threshold=Fraction(1, 10),
        direction=Direction.AT_LEAST,
        falsifies=(
            "أنّ القاعدةَ تفعل شيئًا أصلًا: فإن فُصِل أقلُّ من العُشر "
            "فالمواصفةُ لا تمسّ المدوّنةَ، وقياسُها لغو"
        ),
    ),
    Prediction(
        identifier="ص٤",
        statistic="عددُ أنواع المستوى المفصول",
        threshold=Fraction(TOKEN_KINDS),
        direction=Direction.AT_MOST,
        falsifies=(
            "أنّ الفصلَ يجمع أصولًا: فإن لم تنقص الأنواعُ عن أنواع اللفظ "
            "فالقاعدةُ تُكثِّر ولا تجمع، ولا حاجةَ إلى قياسٍ بعدها"
        ),
    ),
    Prediction(
        identifier="ص٥",
        statistic="نصيبُ المرتدّ في المستوى المفصول",
        threshold=Fraction(1972, 10_000),
        direction=Direction.AT_MOST,
        falsifies=(
            "أنّ الفصلَ يُقلّل ما لم يُرَ: فإن ارتفع المرتدُّ فوق ٠٫١٩٧٢ "
            "فالتقطيعُ يولّد أنواعًا نادرةً بدل أن يجمع المتكرّرة"
        ),
    ),
    Prediction(
        identifier="ص٦",
        statistic="الثمنُ المحجوزُ للوحدة في المستوى المفصول (بتًّا)",
        threshold=Fraction(42_118, 10_000),
        direction=Direction.AT_MOST,
        falsifies=(
            "**الدعوى المسؤولَ عنها**: أنّ قاعدةَ الفصل تنفع محجوزًا. "
            "فإن جاء الثمنُ فوق ثمن اللفظ (٤٫٢١١٨) فالقاعدةُ **تقطيعٌ "
            "بلا بنية** على هذه المدوّنة، ويُنشَر ذلك بلا تجميل — ولا "
            "يُصلَح بإضافة استثناءٍ بعد النظر"
        ),
    ),
    Prediction(
        identifier="ص٧",
        statistic="الثمنُ المحجوزُ للوحدة − ثمنِ الرمز المُرخَّص (بتًّا)",
        threshold=Fraction(0),
        direction=Direction.AT_LEAST,
        falsifies=(
            "أنّ أرخصَ درجةٍ تبقى `م١`: فإن نزل المفصولُ تحت ٣٫٦٥٤٩ "
            "فالسلّمُ المُجمَّدُ في `426f7fc8…` **يُعاد فتحُه بدرجةٍ "
            "جديدة**، وذلك خبرٌ كبير"
        ),
    ),
)

DIGEST = "7bf3ccd8255dc4876ab0febc55ce3baf8ed6babb17022fb0f8001da581a4d0a5"
"""يُثبَّت بعد أوّل اشتقاق، ولا يُمَسّ بعدَه."""


def test_the_seal_is_recomputed_from_the_written_conditions() -> None:
    """البصمةُ تُشتَقّ من الشروط لا تُنقَل."""

    assert seal(ORACLE, PREDICTIONS) == DIGEST


def test_the_rule_is_read_from_the_deposit_not_written_in_code() -> None:
    """الأنماطُ من المواصفة — فإن بُدِّلت تبدّل التشغيل."""

    assert "تُقرأ الأنماطُ من جداول" in ORACLE.extraction
    assert __doc__ is not None
    assert "تُقرَأ القاعدةُ من المواصفة لا تُكتَب في الشفرة" in __doc__
    assert len(PREDICTIONS) == 7


def test_the_measurement_cannot_promote_an_unsigned_rule() -> None:
    """تُقاس ولا تُرقّي مستوًى — والترقيةُ على القاعدة لا على قياسها."""

    assert __doc__ is not None
    assert "غيرُ موقَّعة" in __doc__
    assert "يبقى `UNCLASSIFIED` مهما كان الرقم" in __doc__
    assert "توقيعًا على **القاعدة** لا على **قياسها**" in __doc__


def test_accuracy_is_declared_unmeasurable_and_utility_is_measured() -> None:
    """لا شاهدَ فتُقاس الدقّة — فيُقاس النفعُ، ويُقال ذلك."""

    assert __doc__ is not None
    assert "دقّتُها ولا يُدَّعى" in __doc__  # والسطرُ يلتفّ قبلها
    utility = next(one for one in PREDICTIONS if one.identifier == "ص٦")
    assert "الدعوى المسؤولَ عنها" in utility.falsifies
    assert "لا يُصلَح بإضافة استثناءٍ بعد النظر" in utility.falsifies


def test_the_slice_i_saw_before_sealing_is_declared() -> None:
    """ما رأيتُه قبل الختم مكتوبٌ فيه — والمقابلةُ الفاسدةُ مُعلَنة."""

    assert __doc__ is not None
    assert "٠٫٦٠٥٥" in __doc__
    assert "مقابلةٌ بلا معنًى" in __doc__
