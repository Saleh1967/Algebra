"""**ختمٌ قبل النظر**: أين تقع فجوةُ العبور؟ — قسمتُها بالعَرض.

**لم يُشغَّل شيءٌ بعد.**

**النقص**: نُشِر أنّ **٠٫٨٣٧٩** من الوقوعات لا تعبر الفراغ — أي أنّ
**٠٫١٦٢١** تعبره. **ولم يُقَل أين تقع**. ورقمٌ جملةً بلا قسمةٍ يُخفي موضعَه.

**والقسمةُ صوريّةٌ كالتي قبلها**: بالعَرض — عددِ وحدات ١١٢ في الرمز. فلكلّ
مجموعةٍ **نصيبُها من العبور** و**معدّلُ عبورها داخلَ نفسها**، وهما رقمان
مختلفان لا يُخلَطان:

- **النصيبُ**: كم من العابرات كلِّها يقع في هذه المجموعة.
- **المعدّلُ**: كم من وقوعات هذه المجموعة يعبر.

**ومجموعةُ العَرض ١ لا تعبر بالبناء**: رمزٌ بوحدةٍ واحدةٍ لا جَوفَ له
يُشقّ بفراغ. فتُعَدّ صفرًا **ويُعلَن أنّه صفرٌ لازمٌ لا مرصود**.

**ولا اسمَ لغويٌّ يدخل**: بتّاتٌ وعَرضٌ ووقوعاتٌ فقط.
"""

from __future__ import annotations

from fractions import Fraction

from algebra.signified import Direction, Oracle, Prediction, seal

ORACLE = Oracle(
    name="قسمةُ العبور بالعَرض على المجموعة المولَّدة",
    source="quran-simple-enhanced.txt — البصمة 37633090…",
    extraction=(
        "على حالة أفضل نقطةٍ من `34133d54…` (٤٬٥٠٠ دمجة)، يُعَدّ لكلّ "
        "مجموعةِ عَرضٍ عددُ وقوعاتها العابرةِ لفراغٍ داخلَ الرمز، ويُنشَر "
        "نصيبُها من جملة العابرات ومعدّلُ عبورها داخلَ نفسها؛ ومجموعُ "
        "العابرات يُطابِق المنشورَ جملةً"
    ),
)

PREDICTIONS = (
    Prediction(
        identifier="ف١",
        statistic="|مجموعُ العابرات بالقسمة − المنشورِ جملةً| (وقوعات)",
        threshold=Fraction(0),
        direction=Direction.AT_MOST,
        falsifies=(
            "الحسابَ لا المادّة: القسمةُ إعادةُ تجميعٍ تامّة، فاختلافُ "
            "مجموعها عن الجملة عطلُ آلةٍ يردّ الجدولَ كلَّه"
        ),
    ),
    Prediction(
        identifier="ف٢",
        statistic="نصيبُ مجموعتَي العَرض ٢ و٣ من جملة العابرات",
        threshold=Fraction(1, 2),
        direction=Direction.AT_LEAST,
        falsifies=(
            "دعوايَ أنّ الفجوةَ تقع حيث الكتلةُ لا حيث كثرةُ المفاصل؛ "
            "فإن نزل النصيبُ عن النصف فالعبورُ في الرموز العريضة، "
            "ويُنشَر ذلك بلا تجميل"
        ),
    ),
    Prediction(
        identifier="ف٣",
        statistic=(
            "أدنى (معدّلُ عبورِ عَرضٍ أعلى − معدّلُ عبورِ ما دونه) "
            "على المجموعات الثماني الأولى"
        ),
        threshold=Fraction(0),
        direction=Direction.AT_LEAST,
        falsifies=(
            "دعوى أنّ المعدّلَ يطّرد بالعَرض لكثرة المفاصل؛ فإن انكسر "
            "الاطّرادُ فثمّ بنيةٌ لا يفسّرها عددُ المفاصل وحدَه، وتُوسَم"
        ),
    ),
    Prediction(
        identifier="ف٤",
        statistic="معدّلُ عبورِ مجموعة العَرض ١",
        threshold=Fraction(0),
        direction=Direction.AT_MOST,
        falsifies=(
            "الحسابَ: رمزٌ بوحدةٍ واحدةٍ لا جَوفَ له يُشقّ بفراغ، فعبورُه "
            "ممتنعٌ بالبناء لا نادرٌ بالرصد"
        ),
    ),
)

DIGEST = "0b8eae7649735dc0a719c6c9946dfedfe9ceee6184d054d749c4c79d452978a0"
"""يُثبَّت بعد أوّل اشتقاق، ولا يُمَسّ بعدَه."""


def test_the_seal_is_recomputed_from_the_written_conditions() -> None:
    """البصمةُ تُشتَقّ من الشروط لا تُنقَل."""

    assert seal(ORACLE, PREDICTIONS) == DIGEST


def test_the_share_and_the_rate_are_two_numbers_not_one() -> None:
    """النصيبُ من الجملة غيرُ المعدّل داخلَ المجموعة — وخلطُهما عطلُ وحدات."""

    share = next(one for one in PREDICTIONS if one.identifier == "ف٢")
    rate = next(one for one in PREDICTIONS if one.identifier == "ف٣")
    assert "نصيب" in share.statistic and "معدّل" in rate.statistic
    assert len(PREDICTIONS) == 4


def test_one_condition_is_structural_and_must_be_exactly_zero() -> None:
    """ف٤: العَرضُ ١ لا يعبر بالبناء — صفرٌ لازمٌ لا مرصود."""

    built = next(one for one in PREDICTIONS if one.identifier == "ف٤")
    assert built.threshold == Fraction(0)
    assert "ممتنعٌ بالبناء" in built.falsifies
