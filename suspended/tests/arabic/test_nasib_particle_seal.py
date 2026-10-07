"""**ختمٌ قبل النظر**: كم من أثر العامل تحمله الوحدةُ الأخيرة؟

**لم يُشغَّل شيءٌ بعد. ولم يُعَدّ عددٌ واحد.**

**لِمَ هذا التشغيل**: قيل — وهو صحيحٌ — إنّ العلامةَ على الوحدة **أثرٌ
يتركه عاملٌ يقع في لفظٍ آخر**، فالوحدةُ تحمل الأثرَ ولا تحمل ما أحدثه.
**وذلك قولٌ يُقاس لا يُقال**: فإن كان الأثرُ يقع على الوحدة فنصيبُه
**عددٌ**، وما لا يقع عليها **عددٌ آخر**. فيُقاس الاثنان.

`AND_THE_TARGET_IS_A_CODEPOINT_SEQUENCE_NOT_A_GRAMMATICAL_NAME`: والمقيسُ
**متتاليةُ نقاطٍ** لا اسمُ باب: `0625 0650 0646 0651 064E`. وعُيِّرت
أشكالُ الهيكل `0625 0646` في المجمَّد **قبل كتابة الشروط وبلا عدّ**،
فوُجِدت أربعةً: بلا علامةٍ، وبـ`0650`، وبـ`0652`، **وبـ`0651 064E`**.
**فالشدّةُ تفصل** — والفاصلُ **بايتٌ لا حكم**.

**ولا يُسمّى الشكلُ في السجلّ بابًا**، ولا يُقال إنّ ما يليه اسمٌ ولا خبر.
يُقال: **ما حالُ الوحدة الأخيرة من اللفظ الذي يلي هذا الشكل؟**

`AND_THE_THREE_BUCKETS_ARE_BYTE_PURE`: وتُقسَم الحالُ ثلاثًا **بالبايتات
وحدَها**: `064E` أو `064B` (وهما ما يُنتظَر أن يحمله الأثر)، وحالٌ أخرى
`Mn`، و**العُريُ `·`** — وهو ما لا تحمل الوحدةُ فيه شيئًا.

`AND_THE_BARE_BUCKET_IS_A_MIXTURE_THAT_THE_BYTES_DO_NOT_SEPARATE`: والعُريُ
**خليطٌ لا يفرزه البايت**: منه ما لا تتبدّل خاتمتُه، ومنه ما علامتُه
مقدَّرةٌ لا تُرى، ومنه ما كُتِب تنوينُه **على الألف الذي بعده** فعَرِي
الحرفُ قبله. **فحكمُه `UNCLASSIFIED`**: يُعَدّ ويُسمّى خليطًا، **ولا
يُفسَّر ولا يُصفَّر**، وفرزُه يحتاج جردًا مُودَعًا.

`AND_THE_ORDER_IS_NOT_MEASURED_HERE`: **ولا يُقاس ههنا تعيينُ الدور.** أنّ
الترتيبَ يحدّد أيَّ اللفظين هو الاسم **حقٌّ، وهو فوق هذا القياس**: المقيسُ
**الجارُ التالي** لا التركيب. **فما قدَّمه الترتيبُ يقع في العُري أو في
حالٍ أخرى ويُعَدّ فيهما**، ولا يُفرَز. وهذا **دَينٌ يُسمّى قبل النظر**، لا
نقصٌ يُكتشَف بعده.

**وinduction on**: مجموعُ النِّصب الثلاثة = الواحدُ بالضبط، وعددُ
الوقوعات = مجموعُ ما لها تالٍ وما لا تالٍ لها. **وinduction FOR**: يُفحَص
ذلك عند كلّ وقوعٍ لا في الجملة.

**وما لا يُدَّعى**: هذا **لفظٌ واحدٌ من العوامل**، والقياسُ عليه **لا
يُعمَّم**. ولا يُقال «هكذا الإعرابُ في العربيّة» — يُقال: **هذا ما تحمله
الوحدةُ بعد هذا الشكل في هذا المجمَّد**.
"""

from __future__ import annotations

from fractions import Fraction

from algebra.results import Vacancy
from algebra.signified import Direction, Oracle, Prediction, seal

ORACLE = Oracle(
    name="أثرُ العامل على الوحدة الأخيرة: ما بعد 0625 0650 0646 0651 064E",
    source="quran-simple-enhanced.txt — البصمة 37633090…",
    extraction=(
        "اللفظُ متتاليةٌ بلا فراغٍ فيها محرفٌ عربيٌّ واحدٌ على الأقلّ "
        "(حدُّ `494465d1…`). والشكلُ المقصودُ لفظٌ نقاطُه بترتيبها "
        "`0625 0650 0646 0651 064E` بالضبط. والتالي أوّلُ لفظٍ بعده "
        "**في السطر نفسِه**، ولا يعبر السطرَ. وحالُ اللفظ آخرُ نقطةٍ فيه "
        "إن كانت فئتُها `Mn` وإلّا `·`. والنِّصبُ ثلاثةٌ: `{064E, 064B}`، "
        "وحالٌ `Mn` غيرُهما، و`·`. والنصيبُ مقسومٌ على الوقوعات التي لها "
        "تالٍ في سطرها. والهيكلُ اللفظُ منقوصًا كلَّ نقطةٍ فئتُها `Mn`"
    ),
)

PREDICTIONS = (
    Prediction(
        identifier="غ١",
        statistic="|عددُ الأسطر غيرِ الفارغة − ٦٬٢٣٦|",
        threshold=Fraction(0),
        direction=Direction.AT_MOST,
        falsifies="الآلةَ لا المادّة: المدوّنةُ مُجمَّدةٌ ببصمةٍ مُودَعة",
    ),
    Prediction(
        identifier="غ٢",
        statistic="|عددُ الألفاظ − ٧٨٬٢٤٥|",
        threshold=Fraction(0),
        direction=Direction.AT_MOST,
        falsifies="الآلةَ أيضًا: حدُّ اللفظ المُصحَّحُ من `494465d1…`",
    ),
    Prediction(
        identifier="غ٣",
        statistic="أشكالٌ هيكلُها `0625 0646` وفيها `0651` وليست الشكلَ المقصود",
        threshold=Fraction(0),
        direction=Direction.AT_MOST,
        falsifies=(
            "الآلةَ: عُيِّر الشكلُ قبل الختم فوُجِد واحدًا بالشدّة، فإن "
            "ظهر ثانٍ **فالمعايرةُ ناقصةٌ والقسمةُ تخلط شكلين**"
        ),
    ),
    Prediction(
        identifier="غ٤",
        statistic="وقوعاتُ الشكل `0625 0650 0646 0651 064E`",
        threshold=Fraction(500),
        direction=Direction.AT_LEAST,
        falsifies=(
            "دعوايَ أنّ الشكلَ يقع خمسَ مئةٍ فأكثر؛ فإن نقص **فالمسندُ "
            "أرقُّ ممّا قدَّرت**، وكلُّ نصيبٍ بعده أوسعُ خطأً"
        ),
    ),
    Prediction(
        identifier="غ٥",
        statistic="وقوعاتُ الشكل (الحدُّ الأعلى)",
        threshold=Fraction(2_000),
        direction=Direction.AT_MOST,
        falsifies=(
            "دعوايَ نفسَها من الطرف الآخر؛ فإن زاد **فالشكلُ أكثرُ ورودًا "
            "ممّا قدَّرت**، ويُعَدّ ولا يُفسَّر"
        ),
    ),
    Prediction(
        identifier="غ٦",
        statistic="وقوعاتٌ لا تالٍ لها في سطرها",
        threshold=Fraction(5),
        direction=Direction.AT_MOST,
        falsifies=(
            "دعوايَ أنّ الشكلَ لا يقع آخرَ السطر إلّا نادرًا؛ فإن كثر "
            "**فالجارُ التالي غائبٌ في مواضعَ معتبرة**، ويُعَدّ"
        ),
    ),
    Prediction(
        identifier="غ٧",
        statistic="نصيبُ التالي وحالُه `064E` أو `064B`",
        threshold=Fraction(40, 100),
        direction=Direction.AT_LEAST,
        falsifies=(
            "دعوايَ أنّ الوحدةَ تحمل أثرَ العامل في أكثرِ من خُمسَي "
            "المواضع؛ فإن نقص **فالأثرُ يغيب عن الوحدة أكثرَ ممّا يقع "
            "عليها**، وذلك خبرٌ عن المادّة لا عن الآلة"
        ),
    ),
    Prediction(
        identifier="غ٨",
        statistic="نصيبُ التالي وحالُه `064E` وحدَه",
        threshold=Fraction(20, 100),
        direction=Direction.AT_LEAST,
        falsifies=(
            "دعوايَ أنّ `064E` وحدَها تبلغ خُمسَ المواضع؛ فإن نقصت "
            "**فحاملُ الأثر أكثرُه `064B` لا `064E`**، وذلك فرقُ رسمٍ "
            "يُقاس ولا يُؤوَّل"
        ),
    ),
    Prediction(
        identifier="غ٩",
        statistic="نصيبُ التالي وحالُه `064B` وحدَه",
        threshold=Fraction(5, 100),
        direction=Direction.AT_LEAST,
        falsifies=(
            "دعوايَ أنّ `064B` تبلغ نصفَ عُشرِ المواضع؛ فإن نقصت **فتنوينُ "
            "الفتح قليلٌ ههنا**، ويُعَدّ ولا يُعلَّل"
        ),
    ),
    Prediction(
        identifier="غ١٠",
        statistic="نصيبُ التالي وحالُه `·` (عارٍ)",
        threshold=Fraction(3_108, 10_000),
        direction=Direction.AT_MOST,
        falsifies=(
            "دعوايَ أنّ ما يلي الشكلَ **أقلُّ عُريًا من عامّة المدوّنة** "
            "(٠٫٣١٠٨ في `context_ladder_run.log`)؛ فإن زاد **فالعُريُ "
            "أكثرُ ههنا**، فيكون الشكلُ يقع قبل ما لا تحمل وحدتُه شيئًا "
            "أكثرَ من المعتاد — وذلك نقضٌ لظنّي"
        ),
    ),
    Prediction(
        identifier="غ١١",
        statistic="نصيبُ التالي وحالُه `064F`",
        threshold=Fraction(15, 100),
        direction=Direction.AT_MOST,
        falsifies=(
            "دعوايَ أنّ `064F` قليلةٌ فيما يلي الشكلَ؛ فإن كثرت **فأثرُ "
            "العامل لا يُميِّز حالَ التالي**، وتسقط الدعوى الأولى معها"
        ),
    ),
    Prediction(
        identifier="غ١٢",
        statistic="هياكلُ متمايزةٌ تلي الشكلَ",
        threshold=Fraction(200),
        direction=Direction.AT_LEAST,
        falsifies=(
            "دعوايَ أنّ التالي ليس لفظًا بعينه بل مئتين فأكثر؛ فإن نقص "
            "**فالمقيسُ خاصٌّ بألفاظٍ قليلة** لا عامٌّ في المسند"
        ),
    ),
)

DIGEST = "89cba549d90d587d63a564e6b0d7b471735b05a831769ce391be8b6b0119cb08"
"""ختمُ التسجيل، مثبَّتٌ في المتن؛ وتبديلُ شرطٍ بعد النظر يُعرَف بتغيُّره."""

THE_BARE_BUCKET_IS_A_MIXTURE = Vacancy.UNCLASSIFIED
"""العُريُ خليطٌ لا يفرزه البايت — **يُعَدّ ويُسمّى، ولا يُفسَّر ولا يُصفَّر**.

فيه ما لا تتبدّل خاتمتُه، وما علامتُه مقدَّرةٌ لا تُرى، وما كُتِب تنوينُه
**على الألف الذي بعده**. **وفرزُ هذه الثلاثة يحتاج جردًا مُودَعًا**، وليس
في الشجرة واحد.
"""

THE_ORDER_IS_ABOVE_THIS_MEASUREMENT = (
    "تعيينُ الدور — أيُّ اللفظين اسمٌ وأيُّهما خبر — **في مستوى التركيب**، "
    "وهذا القياسُ على **الجار التالي**. فما قدَّمه الترتيبُ يقع في العُري "
    "أو في حالٍ أخرى **ويُعَدّ فيهما ولا يُفرَز** — دَينٌ مُسمًّى قبل النظر"
)
"""حدُّ التشغيل الأعلى، مكتوبًا قبل العدّ كي لا يُقرَأ نقصًا مكتشَفًا."""

ONE_PARTICLE_IS_NOT_A_LANGUAGE = (
    "شكلٌ واحدٌ من العوامل، **والقياسُ عليه لا يُعمَّم**: يُقال ما تحمله "
    "الوحدةُ بعد هذا الشكل في هذا المجمَّد، ولا يُقال «هكذا الإعراب»"
)
"""وحدُّه الثاني: لا تعميمَ من لفظٍ واحد."""


def test_the_seal_is_derived_from_the_conditions() -> None:
    """البصمةُ تُشتَقّ من الشروط لا تُنقَل."""

    assert seal(ORACLE, PREDICTIONS) == DIGEST


def test_nothing_has_been_run_yet() -> None:
    """يُعلَن في المتن أنّ الختمَ سبق النظر — والترتيبُ في التاريخ."""

    assert __doc__ is not None
    assert "**لم يُشغَّل شيءٌ بعد. ولم يُعَدّ عددٌ واحد.**" in __doc__


def test_the_target_is_a_codepoint_sequence_not_a_ruling() -> None:
    """المقيسُ متتاليةُ نقاطٍ — ولا يُسمّى بابًا ولا اسمًا ولا خبرًا."""

    assert __doc__ is not None
    text = " ".join(__doc__.split())
    assert "`0625 0650 0646 0651 064E`" in text
    assert "**فالشدّةُ تفصل** — والفاصلُ **بايتٌ لا حكم**" in text
    assert "ولا يُسمّى الشكلُ في السجلّ بابًا" in text
    assert "0625 0650 0646 0651 064E" in " ".join(ORACLE.extraction.split())


def test_the_calibration_preceded_the_conditions_and_counted_nothing() -> None:
    """عُيِّر الشكلُ قبل الشروط **وبلا عدّ** — ويُقال ذلك لا يُفترَض."""

    assert __doc__ is not None
    text = " ".join(__doc__.split())
    assert "**قبل كتابة الشروط وبلا عدّ**" in text
    machine = next(one for one in PREDICTIONS if one.identifier == "غ٣")
    assert "عُيِّر الشكلُ قبل الختم" in machine.falsifies


def test_the_bare_bucket_is_classified_not_explained() -> None:
    """العُريُ `UNCLASSIFIED` — خليطٌ يُعَدّ ولا يُفسَّر."""

    assert THE_BARE_BUCKET_IS_A_MIXTURE is Vacancy.UNCLASSIFIED
    assert __doc__ is not None
    text = " ".join(__doc__.split())
    assert "**خليطٌ لا يفرزه البايت**" in text
    assert "**فحكمُه `UNCLASSIFIED`**" in text
    assert "ولا يُفسَّر ولا يُصفَّر" in text


def test_the_two_limits_are_written_before_the_count() -> None:
    """حدّان مكتوبان قبل العدّ: الترتيبُ فوق القياس، ولفظٌ ليس لغة."""

    assert "في مستوى التركيب" in THE_ORDER_IS_ABOVE_THIS_MEASUREMENT
    assert "دَينٌ مُسمًّى قبل النظر" in THE_ORDER_IS_ABOVE_THIS_MEASUREMENT
    assert "لا يُعمَّم" in ONE_PARTICLE_IS_NOT_A_LANGUAGE
    assert __doc__ is not None
    assert "**ولا يُقاس ههنا تعيينُ الدور.**" in " ".join(__doc__.split())


def test_three_refute_the_machine_and_nine_are_claims_of_mine() -> None:
    """ثلاثٌ تردُّ الآلةَ، وتسعٌ **دعاوٍ لي** تسقط بأرقامها."""

    machine = {"غ١", "غ٢", "غ٣"}
    mine = {one.identifier for one in PREDICTIONS} - machine
    assert len(mine) == 9
    for one in PREDICTIONS:
        if one.identifier in mine:
            assert "دعوايَ" in one.falsifies, one.identifier
        else:
            assert "الآلةَ" in one.falsifies, one.identifier
