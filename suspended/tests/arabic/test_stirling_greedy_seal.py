"""**ختمٌ قبل النظر**: ستيرلنغ مع الجشع **وقت الحساب** — أتعود البتّةُ المفقودة؟

**لم يُشغَّل شيءٌ بعد. ولم يُحسَب شيءٌ بعد.**

**العطلُ المرصود**: في `6d6fd210…` صرف التصعيدُ الجشعُ **ثلاثَ بتّاتٍ**
على أربع خاناتٍ **والسقفُ الخام بتّتان**. وفي `447bd783…` صرف **بتّتين**
على أربعٍ فوافق السقف. **فالإسرافُ ليس في الجشع مطلقًا بل في حالٍ منه.**

**والدعوى المطروحة**: أنّ **المعيارَ نفسَه** هو العطل. فالجشعُ يسجّل
**بالإنتروبيا**، والإنتروبيا **حدُّ ستيرلنغ** لعدد التباديل المتمايزة لا
العددُ نفسُه:

    log₂ C(n ؛ n₁…n_k) ≤ n·H     — والفرقُ **فجوةُ ستيرلنغ**

وقد قِيس في `ca75f300…` أنّ هذه الفجوةَ **تكبر بعدد الرموز** (٠٫٠٠٢ ⟶
٠٫٠٥٩ للرمز). **فالقسمةُ تُغيِّر الفجوة**، والمعياران قد يرتّبان الأسئلةَ
ترتيبين. **والمقترَح**: أن يُحسَب **عددُ التباديل نفسُه وقت الاختيار** لا
حدُّه، فينظر الجشعُ في الكمّيّة لا في نهايتها.

**وهويّةٌ تُحسَب لا تُظَنّ**: لأيّ قسمةٍ، فرقُ الكسبين **مُعيَّنٌ تمامًا**:

    كسبُ التباديل − كسبُ الإنتروبيا = Σ فجواتِ الكتل − فجوةُ الجذر

**فليست مصادفةً ولا تقريبًا**، ويُفحَص أنّها تُغلِق إلى آخر رقم.

**والمقامان مُودَعان**: جدولُ `deposits/hasr_rule_note.md` وجدولُ
`deposits/number_rule_note.md`. **ولا قياسَ جديدًا على المصحف ههنا** —
المقيسُ **أثرُ المعيار على الجشع**، لا اللغةُ ولا المادّة.

**وما لا يُدَّعى**: أنّ الجشعَ بالتباديل **مبرهَن**. **ليس كذلك**: أفضلُ
سؤالٍ عند درجةٍ ليس أفضلَ سلّمٍ في النهاية بأيّ معيار. **فإن عادت البتّةُ
فقد عادت بالحساب لا بالبرهان**، وما يُبلَغ **حدٌّ أدنى**.
"""

from __future__ import annotations

from fractions import Fraction

from algebra.signified import Direction, Oracle, Prediction, seal

ORACLE = Oracle(
    name="ستيرلنغ مع الجشع وقت الحساب — معياران على سلّمين مُودَعين",
    source="deposits/hasr_rule_note.md و deposits/number_rule_note.md",
    extraction=(
        "الخاناتُ تُقرأ من جدولَي الإيداع بنمطٍ لا كتابةً، والبقيّةُ غيرُ "
        "المنشورة تُحمَل خانةً واحدة. والكتلةُ (n ؛ عددُ كلّ صنفٍ فيها)، "
        "وثمنُها بالإنتروبيا `n·H` وبالتباديل `log₂ n! − Σ log₂ nᵢ!` "
        "بدالّة `lgamma`. والتصعيدُ سؤالٌ ثنائيٌّ واحدٌ في كلّ درجةٍ "
        "يُختار من كلّ قسمةٍ ثنائيّةٍ غيرِ تافهةٍ للخانات، بأكبرِ كسبٍ "
        "**بالمعيار المعمول به في ذلك الذراع**، ويقف حين لا يربح سؤال. "
        "وذراعان: الإنتروبيا والتباديل، على المقامين كليهما. وفجوةُ كتلةٍ "
        "`n·H − log₂ التباديل`"
    ),
)

PREDICTIONS = (
    Prediction(
        identifier="غ١",
        statistic="|مجموعُ مقامَي الإيداعين − (٦٦٢ + ٣٥)|",
        threshold=Fraction(0),
        direction=Direction.AT_MOST,
        falsifies=(
            "الآلةَ لا المادّة: الجدولان مُودَعان بأعدادهما، فتبدّلُ مقامٍ "
            "يعني أنّ القراءةَ تقرأ غيرَ ما أُودِع"
        ),
    ),
    Prediction(
        identifier="غ٢",
        statistic="أقصى (log₂ التباديل − n·H) على الكتل كلِّها (بت)",
        threshold=Fraction(0),
        direction=Direction.AT_MOST,
        falsifies=(
            "الآلةَ أيضًا: عددُ التباديل المتمايزة دون `n·H` مبرهنةً، "
            "فتجاوزُه عطلُ حسابٍ يردُّ الذراعين معًا"
        ),
    ),
    Prediction(
        identifier="غ٣",
        statistic="أقصى |فرقُ الكسبين − (Σ فجواتِ الكتل − فجوةُ الجذر)| (بت)",
        threshold=Fraction(1, 1_000_000_000),
        direction=Direction.AT_MOST,
        falsifies=(
            "هويّةً تُحسَب لا تُظَنّ: الفرقُ مُعيَّنٌ تمامًا بالفجوات؛ "
            "فتخلّفُه يعني أنّ أحدَ الثمنين ليس ما سُمّي"
        ),
    ),
    Prediction(
        identifier="غ٤",
        statistic="عددُ البتّات التي يصرفها الجشعُ **بالتباديل** في مقام الحصر",
        threshold=Fraction(2),
        direction=Direction.AT_MOST,
        falsifies=(
            "دعوايَ أنّ المعيارَ هو العطل: أنّ الحسابَ بالتباديل يبلغ "
            "الكتلَ الأربعَ ببتّتين فتعود البتّةُ المفقودة. فإن صرف ثلاثًا "
            "كالإنتروبيا فالإسرافُ **ليس أثرَ المعيار**، ويُنشَر ذلك — "
            "وهو أنفعُ من تصديق دعوايَ"
        ),
    ),
    Prediction(
        identifier="غ٥",
        statistic="حجمُ أصغرِ كتلةٍ في السؤال الأوّل بالتباديل في مقام الحصر",
        threshold=Fraction(2),
        direction=Direction.AT_LEAST,
        falsifies=(
            "دعوايَ أنّ التباديلَ تدفع إلى قسمةٍ **متوازنة** (٢–٢) لا "
            "(١–٣)، لأنّ فجوةَ ستيرلنغ تثقل بكثرة الكتل الصغيرة؛ فإن بقي "
            "السؤالُ الأوّلُ واحدًا ضدّ الباقي فتعليلي ساقطٌ وإن عاد العدد"
        ),
    ),
    Prediction(
        identifier="غ٦",
        statistic="عددُ البتّات التي يصرفها الجشعُ **بالتباديل** في مقام العدد",
        threshold=Fraction(2),
        direction=Direction.AT_MOST,
        falsifies=(
            "دعوايَ أنّ المعيارَ الجديدَ **لا يُفسِد ما كان سليمًا**: مقامُ "
            "العدد بلغ السقفَ بالإنتروبيا، فإن جاوزه بالتباديل فالمعيارُ "
            "يشفي موضعًا ويُمرِض آخر، ويُنشَر كذلك"
        ),
    ),
    Prediction(
        identifier="غ٧",
        statistic="عددُ الدرجات التي يفترق فيها سؤالُ المعيارين (المقامان معًا)",
        threshold=Fraction(1),
        direction=Direction.AT_LEAST,
        falsifies=(
            "دعوايَ أنّ المعيارين **يرتّبان الأسئلةَ ترتيبين**؛ فإن اتّفقا "
            "في كلّ درجةٍ فحدُّ ستيرلنغ **لا يُزحزح الاختيار** وإن أزاح "
            "المقدار، وذلك نفيٌ مقيسٌ يُنشَر"
        ),
    ),
    Prediction(
        identifier="غ٨",
        statistic="مجموعُ الكسب بالتباديل − مجموعُه بالإنتروبيا، في مقام الحصر (بت)",
        threshold=Fraction(0),
        direction=Direction.AT_LEAST,
        falsifies=(
            "دعوًى مُشتَقّةٌ لا مقيسة: فجوةُ الجذر أصغرُ من مجموع فجوات "
            "الكتل، فالكسبُ بالتباديل أوفر. فإن نزل عنه فحسابُ الفجوات "
            "مقلوبٌ عندي، ويُصحَّح بالنشر لا بالكتمان"
        ),
    ),
    Prediction(
        identifier="غ٩",
        statistic="أدنى (n·H − log₂ التباديل) على الكتل كلِّها (بت)",
        threshold=Fraction(0),
        direction=Direction.AT_LEAST,
        falsifies=(
            "الآلةَ ثالثةً: الفجوةُ غيرُ سالبةٍ بحكم المبرهنة نفسِها، " "وسالبُها يردُّ الجدول"
        ),
    ),
    Prediction(
        identifier="غ١٠",
        statistic="أيتّفق المعياران على السؤال الأوّل في مقام العدد (١ نعم، ٠ لا)",
        threshold=Fraction(1),
        direction=Direction.AT_LEAST,
        falsifies=(
            "دعوايَ أنّ الخلافَ يقع حيث الإسرافُ لا حيث السلامة؛ فإن "
            "اختلفا في مقام العدد أيضًا فأثرُ المعيار **أوسعُ ممّا قدّرت**، "
            "ويُنشَر باتّساعه"
        ),
    ),
)

DIGEST = "62495099154b7a2fd7ac1f0600fa4c7340c2ab1580ee4dbeb0106577ac8f14a8"
"""يُثبَّت بعد أوّل اشتقاق، ولا يُمَسّ بعدَه."""


def test_the_seal_is_recomputed_from_the_written_conditions() -> None:
    """البصمةُ تُشتَقّ من الشروط لا تُنقَل."""

    assert seal(ORACLE, PREDICTIONS) == DIGEST


def test_the_identity_between_the_two_criteria_is_declared_before_looking() -> None:
    """فرقُ الكسبين مُعيَّنٌ بالفجوات — هويّةٌ تُحسَب لا تُظَنّ."""

    assert __doc__ is not None
    text = " ".join(__doc__.split())
    assert "كسبُ التباديل − كسبُ الإنتروبيا = Σ فجواتِ الكتل − فجوةُ الجذر" in text
    assert "فليست مصادفةً ولا تقريبًا" in text
    third = next(one for one in PREDICTIONS if one.identifier == "غ٣")
    assert third.threshold == Fraction(1, 1_000_000_000)


def test_the_new_criterion_is_not_claimed_proven() -> None:
    """الجشعُ بالتباديل غيرُ مبرهَن أيضًا — وما يُبلَغ حدٌّ أدنى."""

    assert __doc__ is not None
    text = " ".join(__doc__.split())
    assert "أنّ الجشعَ بالتباديل **مبرهَن**. **ليس كذلك**" in text
    assert "فقد عادت بالحساب لا بالبرهان" in text
    assert "وما يُبلَغ **حدٌّ أدنى**" in text


def test_nothing_new_is_measured_on_the_corpus() -> None:
    """المقيسُ أثرُ المعيار على الجشع — لا اللغةُ ولا المادّة."""

    assert __doc__ is not None
    text = " ".join(__doc__.split())
    assert "ولا قياسَ جديدًا على المصحف ههنا" in text
    assert "deposits/hasr_rule_note.md" in ORACLE.source
    assert "deposits/number_rule_note.md" in ORACLE.source


def test_four_conditions_are_machine_or_identity_and_six_are_exposed() -> None:
    """أربعةٌ تردُّ الآلةَ أو هويّة، وستٌّ دعاوٍ لي معرَّضةٌ للسقوط."""

    machine = {"غ١", "غ٢", "غ٣", "غ٩"}
    mine = {one.identifier for one in PREDICTIONS} - machine
    assert len(mine) == 6
    for one in PREDICTIONS:
        if one.identifier in mine:
            assert "دعواي" in one.falsifies or "دعوًى" in one.falsifies, one.identifier
