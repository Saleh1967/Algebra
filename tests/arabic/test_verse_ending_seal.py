"""**ختمٌ قبل النظر**: حدُّ الآية **شرطًا** لا أبجديّة — والعدُّ المعروضُ يُعَدّ.

**لم يُشغَّل شيءٌ بعد**، ولا على شريحة: هذا قياسُ توزيعاتٍ لا تصعيدٌ،
فلا آلةَ تُجرَّب. **فلم أرَ رقمًا من أرقامه قبل الختم.**

**الخللُ المعروض**: في `248f10df…` قِستُ مستوى السطر **أبجديّةً** — كلُّ
آيةٍ رمزٌ — فخرج ثمنُه المحجوزُ ٦٫٩٣٦٩ ومرتدُّه ٠٫٩٦٩٩، فقلتُ إنّه أسوأُ
الدرجات. **وذاك قياسُ الشيء في غير بابه**: خبرُ حدِّ الآية ليس في جعلها
ذرّةً تُشفَّر، بل في كونها **شرطًا** يقع عنده حقلُ الحال على توزيعٍ آخر.
**والعتبةُ تمنع الترخيص ولا تمنع القياس** — وهذا نصُّ التصحيح، وأقبله.

**والعدّةُ المعروضةُ تُعَدّ**: فتحةٌ ٠٫٤٩٢٩ ⟷ ٠٫٢٦٥٩، وتنوينٌ ٠٫١٧٦١ ⟷
٠٫٠٧٣٨، وإنتروبيا ٢٫٢٠٨٤ ⟷ ٢٫٤٧٠٢؛ و«بسم» أربعٌ لا خمس؛ وآياتٌ وحيدةُ
الكلمة ثمانٍ وعشرون، عشرٌ منها تبدأ هيكليًّا بـ«ال».

**والتعريفُ آليٌّ ومُعلَن**: العلامةُ الأخيرةُ هي آخرُ محرفٍ من صنف `Mn`
في الكلمة، وأصنافُها: فتحةٌ وضمّةٌ وكسرةٌ وسكونٌ وشدّةٌ وألفٌ فوقيّةٌ
و**تنوينٌ** (الثلاثةُ مجموعة) و«بلا علامة» لِما خُتِم بحرف. والوسومُ
`<sel>` تُزال، والفصلُ بالفراغ.

**ولا فهرسَ سورٍ مُودَعٌ**: فالمواضعُ **بأرقام الأسطر** لا بسورةٍ وآية.
وما نُسِب في العرض إلى `1:1` و`95/97` و`11:41` و`27:30` **لا أستطيع
مقابلتَه**، لأنّ ترقيمَ السور لا يُشتَقّ من البايتات — **ويُقال ولا
يُخمَّن**.

**و«بوّابة A» ليست عندي**: هي آلةُ صاحب المستودع، فلا أقيس عماها. وأقيس
ما يُشتَقّ: كم من الآيات وحيدةِ الكلمة تبدأ بوحدتَي ا+ل.

**ولا اسمٌ لصنفٍ يدخل**: علاماتٌ ومواضعُ وبتّات.
"""

from __future__ import annotations

from fractions import Fraction

from algebra.signified import Direction, Oracle, Prediction, seal

VERSES = 6_236
TIGHT = Fraction(1, 20_000)

ORACLE = Oracle(
    name="خاتمةُ الآية شرطًا على حقل الحال",
    source="quran-simple-enhanced.txt — البصمة 37633090…",
    extraction=(
        "تُزال وسومُ `<sel>` ويُفصَل بالفراغ؛ ولكلّ كلمةٍ صنفُ آخرِ محرفٍ "
        "من `Mn` فيها (فتحة، ضمّة، كسرة، سكون، شدّة، ألفٌ فوقيّة، تنوينٌ "
        "بثلاثته مجموعًا، وبلا علامة). فيُقارَن توزيعُ خاتمة الآية بتوزيع "
        "خاتمة الكلمة، وتُحسَب إنتروبيا كلٍّ، والمعلوماتُ المتبادلةُ بين "
        "الحال وكونِ الموضع خاتمةَ آية؛ وتُعَدّ مواضعُ هيكل «بسم» "
        "والآياتُ وحيدةُ الكلمة بأرقام الأسطر"
    ),
)

PREDICTIONS = (
    Prediction(
        identifier="خ١",
        statistic="|عددُ الأسطر − ٦٬٢٣٦|",
        threshold=Fraction(0),
        direction=Direction.AT_MOST,
        falsifies=(
            "المدوّنةَ نفسَها: تبدُّلُ عدد الأسطر يعني أنّ البايتاتِ غيرُ "
            "المُجمَّدة، ويُردّ التشغيلُ قبل أن يبدأ"
        ),
    ),
    Prediction(
        identifier="خ٢",
        statistic="|نصيبُ الفتحة عند خاتمة الآية − ٠٫٤٩٢٩|",
        threshold=TIGHT,
        direction=Direction.AT_MOST,
        falsifies="العددَ المعروضَ على تعريفي للعلامة الأخيرة",
    ),
    Prediction(
        identifier="خ٣",
        statistic="|نصيبُ التنوين عند خاتمة الآية − ٠٫١٧٦١|",
        threshold=TIGHT,
        direction=Direction.AT_MOST,
        falsifies="العددَ المعروضَ للتنوين عند الخاتمة",
    ),
    Prediction(
        identifier="خ٤",
        statistic="|نصيبُ الفتحة عند خاتمة الكلمة − ٠٫٢٦٥٩|",
        threshold=TIGHT,
        direction=Direction.AT_MOST,
        falsifies="العددَ المعروضَ عند خاتمة الكلمة — وقد يفترق بالفصل لا بالعلامة",
    ),
    Prediction(
        identifier="خ٥",
        statistic="|نصيبُ التنوين عند خاتمة الكلمة − ٠٫٠٧٣٨|",
        threshold=TIGHT,
        direction=Direction.AT_MOST,
        falsifies="العددَ المعروضَ للتنوين عند خاتمة الكلمة",
    ),
    Prediction(
        identifier="خ٦",
        statistic="|إنتروبيا خاتمة الآية − ٢٫٢٠٨٤| (بتًّا)",
        threshold=TIGHT,
        direction=Direction.AT_MOST,
        falsifies="العددَ المعروضَ — وهو رهنُ عدد الأصناف، فقد يفترق بها وحدَها",
    ),
    Prediction(
        identifier="خ٧",
        statistic="|إنتروبيا خاتمة الكلمة − ٢٫٤٧٠٢| (بتًّا)",
        threshold=TIGHT,
        direction=Direction.AT_MOST,
        falsifies="العددَ المعروضَ عند خاتمة الكلمة",
    ),
    Prediction(
        identifier="خ٨",
        statistic="إنتروبيا خاتمة الآية − إنتروبيا خاتمة الكلمة (بتًّا)",
        threshold=Fraction(0),
        direction=Direction.AT_MOST,
        falsifies=(
            "**جوهرَ العرض**: أنّ خاتمةَ الآية **مكثَّفةٌ** عن خاتمة "
            "الكلمة. وهذا يصمد أو يسقط **وإن اختلفت الأرقامُ الأربعةُ "
            "قبله**، فهو المقارنةُ لا المقدار"
        ),
    ),
    Prediction(
        identifier="خ٩",
        statistic="I(الحال ؛ كونِ الموضع خاتمةَ آية) (بتًّا للموضع)",
        threshold=Fraction(1, 10_000),
        direction=Direction.AT_LEAST,
        falsifies=(
            "أنّ الحدَّ الآييَّ يترك أثرًا في حقل الحال أصلًا: وصفرٌ ههنا "
            "يعني استقلالًا تامًّا، فلا شيءَ يُرخَّص ولا يُقاس"
        ),
    ),
    Prediction(
        identifier="خ١٠",
        statistic="أقصى (H(الحال|شرط) − H(الحال)) على الشرطين (بتًّا)",
        threshold=Fraction(0),
        direction=Direction.AT_MOST,
        falsifies=(
            "متراجحةً مبرهَنة: الشرطُ لا يرفع الإنتروبيا في المتوسّط. "
            "وارتفاعُها عطلُ حسابٍ لا اكتشاف — **وهي `induction on` ههنا**"
        ),
    ),
    Prediction(
        identifier="خ١١",
        statistic="|عددُ مواضع هيكل «بسم» − ٤|",
        threshold=Fraction(0),
        direction=Direction.AT_MOST,
        falsifies=(
            "العددَ المعروضَ: أربعٌ لا خمس. وتعريفي الهيكلَ حروفًا بلا "
            "علامات قد يجمع ما فرّقه العرضُ أو يفرّق ما جمعه، ويُنشَر "
            "كلُّ موضعٍ برقم سطره وصورته"
        ),
    ),
    Prediction(
        identifier="خ١٢",
        statistic="|عددُ الآيات وحيدةِ الكلمة − ٢٨|",
        threshold=Fraction(0),
        direction=Direction.AT_MOST,
        falsifies="العددَ المعروضَ على الفصل بالفراغ بعد إزالة الوسوم",
    ),
    Prediction(
        identifier="خ١٣",
        statistic="|ما يبدأ منها هيكليًّا بـ«ال» − ١٠|",
        threshold=Fraction(0),
        direction=Direction.AT_MOST,
        falsifies=(
            "العددَ المعروضَ لِما تعمى عنه بوّابةُ صاحب المستودع؛ وأنا لا "
            "أقيس عماها بل أقيس **هذا الوصفَ المشتَقّ** وحدَه"
        ),
    ),
)

DIGEST = "26ae5b5b11df1d6ef3cdf59ac28008de6958873c84f62fa398c3f6b81f3381f2"
"""يُثبَّت بعد أوّل اشتقاق، ولا يُمَسّ بعدَه."""


def test_the_seal_is_recomputed_from_the_written_conditions() -> None:
    """البصمةُ تُشتَقّ من الشروط لا تُنقَل."""

    assert seal(ORACLE, PREDICTIONS) == DIGEST


def test_the_flaw_is_owned_before_the_numbers() -> None:
    """قياسُ السطر أبجديّةً خطأُ بابٍ — والعتبةُ تمنع الترخيص لا القياس."""

    assert __doc__ is not None
    assert "قياسُ الشيء في غير بابه" in __doc__
    assert "والعتبةُ تمنع الترخيص ولا تمنع القياس" in __doc__
    assert "248f10df" in __doc__


def test_the_substance_is_separable_from_the_four_numbers() -> None:
    """خ٨ يصمد أو يسقط وإن اختلفت الأرقام — فهو المقارنة لا المقدار."""

    core = next(one for one in PREDICTIONS if one.identifier == "خ٨")
    assert core.threshold == Fraction(0)
    assert "وإن اختلفت الأرقامُ الأربعةُ قبله" in core.falsifies
    assert len(PREDICTIONS) == 13


def test_what_cannot_be_derived_is_declared_not_guessed() -> None:
    """لا فهرسَ سورٍ، ولا بوّابةَ صاحب المستودع — ويُقال ولا يُخمَّن."""

    assert __doc__ is not None
    assert "لا فهرسَ سورٍ مُودَعٌ" in __doc__
    assert "ويُقال ولا\nيُخمَّن" in __doc__ or "يُقال ولا" in __doc__
    assert "ليست عندي" in __doc__
    blind = next(one for one in PREDICTIONS if one.identifier == "خ١٣")
    assert "لا\nأقيس عماها" in blind.falsifies or "أقيس" in blind.falsifies


def test_one_condition_is_a_proven_inequality() -> None:
    """خ١٠ — الشرطُ لا يرفع الإنتروبيا، وهي `induction on` ههنا."""

    one = next(item for item in PREDICTIONS if item.identifier == "خ١٠")
    assert one.threshold == Fraction(0)
    assert "متراجحةً مبرهَنة" in one.falsifies
    assert "`induction on`" in one.falsifies
