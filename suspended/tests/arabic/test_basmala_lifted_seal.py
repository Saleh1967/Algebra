"""**ختمٌ قبل النظر**: الأرقامُ الكلميّةُ تُعاد مرفوعَ البسملات.

**لم يُشغَّل شيءٌ بعد.** والآلةُ مركَّبةٌ من آلاتٍ مُشغَّلةٍ من قبلُ، ولم
تُجرَّب على شريحة — **فلم أرَ رقمًا من أرقام هذا التشغيل**.

**ما يُعاد**: في `e453d16` تبيّن أنّ البسملةَ ملحقةٌ بأوّل آيةٍ من كلّ
سورة — **١١٢** سطرًا و**٤٤٨** كلمة — **ولم يُسجَّل ذلك قبلُ**. فكلُّ رقمٍ
كلميٍّ نُشِر يحمله؛ **فتُعاد الأرقامُ كلُّها على مدوّنةٍ مشتقّةٍ مرفوعة**.

**والمُجمَّدُ لا يُمَسّ**: تُبنى منه مدوّنةٌ مشتقّةٌ ببصمةٍ خاصّةٍ بها،
**ولا تُرفَع البسملةُ القائمةُ بنفسها** في السطر الأوّل. والرفعُ **قصٌّ
لا إعادةُ كتابة**: يُؤخَذ السطرُ من مبدأ كلمته الخامسة.

**ولا يُبدَّل سجلٌّ مُقفَل**: `426f7fc8…` قياسُ المُجمَّد كما هو ويبقى؛
وهذه أرقامٌ **موازيةٌ** تُنشَر باسمها. **و«قبلُ» يُقرأ من السجلّ المُقفَل
لا من الذاكرة.**

**والبسملةُ أكثرُ ما تكرّر في المدوّنة**، فرفعُها **يرفع تكرارًا**؛ فإن
ارتفع الثمنُ فذلك **متوقَّعٌ ولا يُقرأ خبرًا عن البنية**، وإن نزل فهو
خبر.

**ولا اسمٌ لصنفٍ يدخل**: ألفاظٌ وهياكلُ وأسطرٌ وبتّات.
"""

from __future__ import annotations

from fractions import Fraction

from algebra.signified import Direction, Oracle, Prediction, seal

LIFTED_LINES = 112
LIFTED_WORDS = 448
TOKENS_BEFORE = 78_245
TOKENS_AFTER = 77_797

ORACLE = Oracle(
    name="الأرقامُ الكلميّةُ مُعادةً مرفوعَ البسملات الملحقة",
    source="quran-simple-enhanced.txt — البصمة 37633090… ومشتقّتُها المرفوعة",
    extraction=(
        "يُرفَع من كلّ سطرٍ تبدأ هياكلُ كلماته الأربع الأولى بالبسملة "
        "وفيه زيادةٌ عليها أوّلُ أربعِ كلماتٍ منه، قصًّا من مبدأ الخامسة؛ "
        "ثمّ يُعاد على المشتقّة عدُّ الألفاظ والهياكل والغامض وكتلتِه، "
        "ودرجاتُ السلّم الأربع بثمنها ملحَقًا ومحجوزًا ومرتدِّها و`I`، "
        "وقاعدةُ الفصل بأنواعها ومرتدِّها وثمنها — ويُقابَل كلُّ رقمٍ "
        "بنظيره من السجلّ المُقفَل `426f7fc8…` والسجلّات المُودَعة"
    ),
)

PREDICTIONS = (
    Prediction(
        identifier="ر١",
        statistic="|عددُ الأسطر المرفوعة − ١١٢|",
        threshold=Fraction(0),
        direction=Direction.AT_MOST,
        falsifies=(
            "قاعدةَ الرفع: إن رُفِع غيرُ ١١٢ سطرًا فالقاعدةُ تمسّ ما ليس "
            "بسملةً ملحقة، ويُردّ التشغيلُ كلُّه"
        ),
    ),
    Prediction(
        identifier="ر٢",
        statistic="|عددُ الأسطر بعد الرفع − ٦٬٢٣٦|",
        threshold=Fraction(0),
        direction=Direction.AT_MOST,
        falsifies="أنّ الرفعَ قصٌّ لا حذفُ سطر: نقصُ سطرٍ عطلُ آلة",
    ),
    Prediction(
        identifier="ر٣",
        statistic="|عددُ الألفاظ بعد الرفع − ٧٧٬٧٩٧|",
        threshold=Fraction(0),
        direction=Direction.AT_MOST,
        falsifies=(
            "الحسابَ: ٧٨٬٢٤٥ − ٤٤٨ = ٧٧٬٧٩٧. وخلافُه يعني أنّ التقشير "
            "يفصل غيرَ ما يفصله الفراغ، ويُنشَر الفرقُ برقمه"
        ),
    ),
    Prediction(
        identifier="ر٤",
        statistic="عددُ الهياكل المتمايزة بعد الرفع",
        threshold=Fraction(15_472),
        direction=Direction.AT_MOST,
        falsifies=(
            "أنّ الرفعَ لا يزيد الهياكل: والبسملةُ أربعُ هياكلَ مكرّرة، "
            "فرفعُها لا يأتي بجديد. وزيادتُها عطلُ آلة"
        ),
    ),
    Prediction(
        identifier="ر٥",
        statistic="نصيبُ كتلة الهياكل الغامضة من الألفاظ بعد الرفع",
        threshold=Fraction(4_461, 10_000),
        direction=Direction.AT_LEAST,
        falsifies=(
            "أنّ الغموضَ لا ينقص برفع البسملات: فكلماتُها الأربعُ غيرُ "
            "غامضةٍ في الأغلب، فرفعُها يرفع من المقام غيرَ غامض. فإن نزل "
            "النصيبُ فبعضُها غامضٌ، وذلك خبر"
        ),
    ),
    Prediction(
        identifier="ر٦",
        statistic="أرخصُ درجةٍ محجوزًا في السلّم بعد الرفع (رتبتُها من صفر)",
        threshold=Fraction(1),
        direction=Direction.AT_MOST,
        falsifies=(
            "أنّ موضعَ الانقلاب لا يتحرّك برفع ٤٤٨ كلمة: فإن انتقل أرخصُ "
            "محجوزٍ عن الدرجة الثانية فالسلّمُ المُجمَّدُ رهنُ البسملات، "
            "وذلك خبرٌ كبيرٌ يُعاد له النظرُ كلُّه"
        ),
    ),
    Prediction(
        identifier="ر٧",
        statistic="الثمنُ المحجوزُ للوحدة عند م٠ بعد الرفع − قبلَه (بتًّا)",
        threshold=Fraction(0),
        direction=Direction.AT_LEAST,
        falsifies=(
            "دعوايَ أنّ رفعَ أكثرِ المكرّر **يغلي** المدوّنة: فإن نزل "
            "الثمنُ فالبسملاتُ كانت تُكلِّف أكثرَ ممّا توفّر، وهو عكسُ "
            "ما أتوقّع ويُنشَر كذلك"
        ),
    ),
    Prediction(
        identifier="ر٨",
        statistic="نصيبُ المرتدّ عند م٢ بعد الرفع",
        threshold=Fraction(1_972, 10_000),
        direction=Direction.AT_LEAST,
        falsifies=(
            "أنّ رفعَ مكرَّرٍ يرفع نصيبَ ما لم يُرَ: فإن نزل فالبسملاتُ "
            "كانت تُضخِّم المرتدَّ لا تُقلّله"
        ),
    ),
    Prediction(
        identifier="ر٩",
        statistic="انحرافُ الآلتين عند قيد الفاصل (بتًّا)",
        threshold=Fraction(1, 1000),
        direction=Direction.AT_MOST,
        falsifies="الآلةَ لا المادّة: انحرافُ العدّادات يردّ السلّمَ كلَّه",
    ),
    Prediction(
        identifier="ر١٠",
        statistic="حكمُ قاعدة الفصل بعد الرفع: ثمنُها المحجوز − ثمنِ اللفظ (بتًّا)",
        threshold=Fraction(0),
        direction=Direction.AT_LEAST,
        falsifies=(
            "أنّ حكمَ `7bf3ccd8…` لا ينقلب برفع البسملات: كان الفصلُ "
            "أغلى بـ٠٫٠٨٩٤. فإن صار أرخصَ فالحكمُ كان **رهنَ البسملات**، "
            "وتُعاد قراءةُ ذلك الختم"
        ),
    ),
)

DIGEST = "be03e5bece652be7868071a4099482c1667a0288478efa6fd9cd0744faf86c6a"
"""يُثبَّت بعد أوّل اشتقاق، ولا يُمَسّ بعدَه."""


def test_the_seal_is_recomputed_from_the_written_conditions() -> None:
    """البصمةُ تُشتَقّ من الشروط لا تُنقَل."""

    assert seal(ORACLE, PREDICTIONS) == DIGEST


def test_the_frozen_corpus_is_not_touched() -> None:
    """مدوّنةٌ مشتقّةٌ ببصمتها — والمُجمَّدُ يبقى، والسجلُّ المُقفَل يبقى."""

    assert __doc__ is not None
    assert "والمُجمَّدُ لا يُمَسّ" in __doc__
    assert "ولا يُبدَّل سجلٌّ مُقفَل" in __doc__
    assert "أرقامٌ **موازيةٌ**" in __doc__
    assert len(PREDICTIONS) == 10


def test_the_expected_direction_is_declared_before_the_number() -> None:
    """ر٧ ور٨: رفعُ أكثرِ المكرّر يُتوقَّع أن يُغلي ويرفع المرتدّ."""

    for identifier in ("ر٧", "ر٨"):
        one = next(item for item in PREDICTIONS if item.identifier == identifier)
        assert one.direction is Direction.AT_LEAST
    assert __doc__ is not None
    assert "لا يُقرأ خبرًا عن البنية" in __doc__


def test_the_two_crucial_reversals_are_named() -> None:
    """ر٦ موضعُ الانقلاب، ور١٠ حكمُ قاعدة الفصل — وكلاهما قد يقلب سابقًا."""

    rung = next(one for one in PREDICTIONS if one.identifier == "ر٦")
    rule = next(one for one in PREDICTIONS if one.identifier == "ر١٠")
    assert "426f7fc8" not in rung.falsifies and "السلّمُ المُجمَّدُ" in rung.falsifies
    assert "7bf3ccd8" in rule.falsifies
    assert "رهنَ البسملات" in rule.falsifies


def test_before_is_read_from_the_sealed_record() -> None:
    """«قبلُ» من السجلّ المُقفَل لا من الذاكرة."""

    assert "السجلّ المُقفَل `426f7fc8…`" in ORACLE.extraction
    assert TOKENS_BEFORE - LIFTED_WORDS == TOKENS_AFTER
    assert LIFTED_LINES * 4 == LIFTED_WORDS
