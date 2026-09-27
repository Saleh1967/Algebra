"""**ختمٌ قبل النظر**: رتبةُ ماركوف ٠..٦ **محجوزةً**، وحاجزُ ستيرلنغ فوقها.

**لم يُشغَّل شيءٌ بعد. ولم يُعَدّ محجوزٌ واحد.**

**لِمَ هذا التشغيل**: سلّمُ الضبط المُودَع (`9034199d…`) يقيس الرتبَ ٠..٣
**ملحَقةً** وبأرضيّةِ ثلاثين وقوعًا، فنصيبُ المقروء ينزل إلى **٠٫٤١٨٤**
عند الرتبة الثالثة. **فالنزولُ من ١٫٩٥٢٥ إلى ٠٫٧٥٣٧ نزولٌ على أربعين
بالمئة من المواضع لا على المدوّنة** — والأرضيّةُ تخفي الانتحالَ ولا تمنعه.
**وليس في الشجرة ثمنٌ محجوزٌ للرتبة ألبتّة.**

`SO_THE_HONEST_LADDER_IS_HELD_OUT_AND_UNFLOORED`: فههنا **لا أرضيّة**:
كلُّ موضعٍ يدخل المقام، وما لم يُرَ سياقُه **يُشحَن بلابلاس ولا
يُستبعَد**. والقسمةُ زوجيٌّ وفرديٌّ **بالسطر** وبالتبادل، والحكمُ على
**الثمن المحجوز** لا على الإنتروبيا الملحَقة. **فإن ارتفع المحجوزُ عند
رتبةٍ فتلك رتبةُ الانتحال، وتُسمّى بعينها.**

`AND_STIRLING_IS_THE_CEILING_ABOVE_THE_ORDER_NOT_INSIDE_IT`: وستيرلنغُ
ههنا **ليس مقياسًا للمادّة** بل **حاجزًا على ما يُمكِن بحثُه**: سياقُ
الرتبة `n` فضاؤه `k^n` حالةً، وتكتيلاتُه `Bell(k^n)`. **فيُعَدّ ولا
يُوصَف**: عند أيّ رتبةٍ يفوق عددُ التكتيلات الممكنةِ عددَ المواضع
المقيسة؟ **فمن تلك الرتبة فصاعدًا لا تكفي المادّةُ لاختيار تكتيلٍ**، ولو
كان الأمثلُ موجودًا — **وذلك حدٌّ على المعرفة لا على الحساب**.

`AND_THE_DP_BARRIER_IS_NAMED_TOO`: وأمثلُ تكتيلٍ يُحسَب في `O(k·3^m)` على
`m` سياقًا (وذلك مُودَعٌ في `algebra.lumping_loss`). **فيُسأل: أكبرُ رتبةٍ
فضاءُ تكتيلها دون ٢^٥٠؟** — وما فوقها **متعذّرٌ بالبناء لا بالآلة**.

**وinduction on**: الإنتروبيا الملحَقةُ **لا ترتفع** برفع الرتبة (شرطٌ
مبرهَن: `H(X|Y,Z) ≤ H(X|Y)`)، فإن ارتفعت **فالحسابُ عطلٌ لا خبر**.
**وinduction FOR**: الحلقةُ تشهد رتبةً رتبةً، والمحجوزُ **حرٌّ أن يرتفع**
— وارتفاعُه هو المقصود.

**وما لا يُدَّعى**: القناةُ **حالُ موضع الرسم** لا اللفظ ولا الجملة. ولا
يُقال إنّ رتبةَ الانتحال **حدُّ العربيّة** — يُقال: **هذه الرتبةُ التي
ينقلب عندها الثمنُ المحجوز على هذه القناة في هذا المجمَّد بهذه القسمة**.
وقناةٌ أخرى قد تنقلب في غيرها.
"""

from __future__ import annotations

from fractions import Fraction

from algebra.signified import Direction, Oracle, Prediction, seal

ORACLE = Oracle(
    name="رتبةُ ماركوف محجوزةً بلا أرضيّة، وحاجزُ ستيرلنغ فوقها",
    source="quran-simple-enhanced.txt — البصمة 37633090…",
    extraction=(
        "موضعُ الرسم وحالُه من `examples/rasm/run_encoding_audit.py` "
        "(`rasm_units`) كما في ختم `9034199d…`، والسياقُ **داخلَ السطر "
        "ولا يعبره**. ورتبةُ `n` سياقُها الحالاتُ `n` السابقةُ في السطر، "
        "وأوّلُ السطر يُحشى بحالةِ بدءٍ مُعلَنة **فلا يُستبعَد موضع**. "
        "والقسمةُ زوجيٌّ وفرديٌّ بالسطر: يُبنى الجدولُ من نصفٍ ويُسعَّر "
        "النصفُ الآخر، ثمّ بالعكس، والمأخوذُ متوسّطُ الاتّجاهين. والثمنُ "
        "`−log2((c+1)/(n+k))` بلابلاس على أبجديّة الحالات، **ولا أرضيّةَ "
        "ولا استبعاد**. والإنتروبيا الملحَقةُ مصحَّحةٌ بميلر–مادو. "
        "وفضاءُ الرتبة `k^n`، وتكتيلاتُه `Bell(k^n)` من `algebra.stirling`"
    ),
)

PREDICTIONS = (
    Prediction(
        identifier="ض١",
        statistic="|عددُ الأسطر − ٦٬٢٣٦|",
        threshold=Fraction(0),
        direction=Direction.AT_MOST,
        falsifies="الآلةَ لا المادّة: المدوّنةُ مُجمَّدةٌ ببصمةٍ مُودَعة",
    ),
    Prediction(
        identifier="ض٢",
        statistic="مواضعُ الرسم",
        threshold=Fraction(300_000),
        direction=Direction.AT_LEAST,
        falsifies=(
            "الآلةَ: التقشيرُ هو تقشيرُ ختم `9034199d…`، فإن نقصت المواضعُ "
            "عن ثلاث مئة ألفٍ فالقناةُ غيرُ التي قِيست ثمّة"
        ),
    ),
    Prediction(
        identifier="ض٣",
        statistic="أبجديّةُ الحالات (الحدُّ الأعلى)",
        threshold=Fraction(12),
        direction=Direction.AT_MOST,
        falsifies=(
            "الآلةَ: الحالُ علامةٌ واحدةٌ أو عُريٌ، فإن زادت الأبجديّةُ على "
            "اثنتَي عشرةَ فالتقشيرُ يخلط شيئًا آخر"
        ),
    ),
    Prediction(
        identifier="ض٤",
        statistic="رتباتٌ ارتفعت فيها الإنتروبيا الملحَقةُ برفع الرتبة",
        threshold=Fraction(0),
        direction=Direction.AT_MOST,
        falsifies=(
            "الآلةَ لا المادّة: `H(X|Y,Z) ≤ H(X|Y)` مبرهَنةٌ، فارتفاعُها "
            "**عطلُ حسابٍ لا خبرُ مادّة**"
        ),
    ),
    Prediction(
        identifier="ض٥",
        statistic="أوّلُ رتبةٍ ارتفع فيها الثمنُ المحجوز",
        threshold=Fraction(2),
        direction=Direction.AT_LEAST,
        falsifies=(
            "دعوايَ أنّ الرتبتين الأولى والثانية **تشتريان محجوزًا**؛ فإن "
            "انقلب المحجوزُ عند الأولى **فالسياقُ لا يشتري شيئًا أصلًا على "
            "هذه القناة**، وذلك خبرٌ عن المادّة يُنشَر"
        ),
    ),
    Prediction(
        identifier="ض٦",
        statistic="أوّلُ رتبةٍ ارتفع فيها الثمنُ المحجوز (الحدُّ الأعلى)",
        threshold=Fraction(5),
        direction=Direction.AT_MOST,
        falsifies=(
            "دعوايَ أنّ الانقلابَ يقع عند الخامسة أو قبلها؛ فإن لم يقع "
            "**فالرتبةُ تشتري إلى السادسة**، والسقفُ المادّيُّ فوق ما قِسته"
        ),
    ),
    Prediction(
        identifier="ض٧",
        statistic="أدنى ثمنٍ محجوزٍ تبلغه الرتب، بتًّا",
        threshold=Fraction(90, 100),
        direction=Direction.AT_LEAST,
        falsifies=(
            "دعوايَ أنّ المحجوزَ لا ينزل دون ٠٫٩٠ بتًّا؛ فإن نزل **فالسياقُ "
            "أخبرُ ممّا قدَّرت**، ويُقال بمقداره"
        ),
    ),
    Prediction(
        identifier="ض٨",
        statistic="ربحُ الرتبة الأولى محجوزًا على الصفر، بتًّا",
        threshold=Fraction(30, 100),
        direction=Direction.AT_LEAST,
        falsifies=(
            "دعوايَ أنّ الرتبةَ الأولى وحدَها تشتري ثلاثةَ أعشارِ البتّة "
            "فأكثر؛ فإن نقصت **فأكبرُ ما يفيده السياقُ أقلُّ ممّا ظننت**"
        ),
    ),
    Prediction(
        identifier="ض٩",
        statistic="ربحُ الرتبة الثالثة محجوزًا على الثانية، بتًّا",
        threshold=Fraction(10, 100),
        direction=Direction.AT_MOST,
        falsifies=(
            "دعوايَ أنّ الربحَ يضمر بسرعةٍ فلا تبلغ الثالثةُ عُشرَ بتّة؛ "
            "فإن بلغته **فالرتبُ العُليا أنفعُ ممّا قدَّرت**، ويُنشَر"
        ),
    ),
    Prediction(
        identifier="ض١٠",
        statistic="نصيبُ مواضع المحجوز التي لم يُرَ سياقُها عند الرتبة السادسة",
        threshold=Fraction(30, 100),
        direction=Direction.AT_LEAST,
        falsifies=(
            "دعوايَ أنّ الرقّةَ تعضّ: ثلاثةُ أعشارِ المواضع فأكثرُ سياقُها "
            "غيرُ مشهودٍ عند السادسة؛ فإن نقصت **فالمدوّنةُ أكثفُ ممّا "
            "قدَّرت** عند تلك الرتبة"
        ),
    ),
    Prediction(
        identifier="ض١١",
        statistic="أصغرُ رتبةٍ يفوق فيها عددُ التكتيلات الممكنة عددَ المواضع",
        threshold=Fraction(2),
        direction=Direction.AT_MOST,
        falsifies=(
            "دعوايَ أنّ حاجزَ ستيرلنغ يسبق الرتبةَ الثالثة: من الثانية "
            "فصاعدًا **التكتيلاتُ أكثرُ من المواضع**، فلا تكفي المادّةُ "
            "لاختيار واحدٍ منها. فإن تأخّر **فالبحثُ ممكنٌ أوسعَ ممّا قلت**"
        ),
    ),
    Prediction(
        identifier="ض١٢",
        statistic="أكبرُ رتبةٍ فضاءُ تكتيلها دون ٢^٥٠ من العمليّات",
        threshold=Fraction(1),
        direction=Direction.AT_MOST,
        falsifies=(
            "دعوايَ أنّ أمثلَ تكتيلٍ في `O(k·3^m)` لا يُحسَب فوق الرتبة "
            "الأولى؛ فإن أمكن عند الثانية **فالحاجزُ أوسعُ ممّا قلت**، "
            "ويُعاد النظرُ في دعوى التعذّر"
        ),
    ),
)

DIGEST = "0fdd08b281f99471a1adbe7a72ef814b86bf60976edfa158afb9da609d0f1396"
"""ختمُ التسجيل، مثبَّتٌ في المتن؛ وتبديلُ شرطٍ بعد النظر يُعرَف بتغيُّره."""

THE_FLOOR_IS_REMOVED_AND_THAT_IS_THE_POINT = (
    "سلّمُ الضبط المُودَع يستبعد ما دون ثلاثين وقوعًا، فنصيبُ المقروء "
    "٠٫٤١٨٤ عند الثالثة. **وههنا لا أرضيّة**: كلُّ موضعٍ يدخل المقام، "
    "وغيرُ المشهود **يُشحَن بلابلاس**. فالرقمان لا يُقابَلان: **ذاك على "
    "أربعين بالمئة ملحَقًا، وهذا على الكلّ محجوزًا**"
)
"""ولا يُطرَح رقمٌ من رقمٍ بين المسندين — العطل ٢٤ مكتوبًا قبل النظر."""

STIRLING_BOUNDS_KNOWLEDGE_NOT_COMPUTATION = (
    "حاجزُ ستيرلنغ **حدٌّ على ما تستطيع المادّةُ ترجيحَه**، لا على ما "
    "تستطيع الآلةُ حسابَه. فعددُ التكتيلات إذا فاق عددَ المواضع **لم "
    "يبقَ في المادّة ما يختار**، ولو كان الحسابُ رخيصًا"
)
"""وهذا هو الفرقُ بين حدِّ الحساب وحدِّ المعرفة — ويُقال قبل النظر."""

ONE_CHANNEL_IS_NOT_A_LANGUAGE = (
    "القناةُ **حالُ موضع الرسم** — لا اللفظ ولا الجملة. ورتبةُ الانتحال "
    "ههنا **رتبةُ هذه القناة في هذا المجمَّد بهذه القسمة**، ولا تُقرَأ "
    "حدًّا للعربيّة"
)
"""حدُّ التشغيل الأعلى، مكتوبًا قبل العدّ."""


def test_the_seal_is_derived_from_the_conditions() -> None:
    """البصمةُ تُشتَقّ من الشروط لا تُنقَل."""

    assert seal(ORACLE, PREDICTIONS) == DIGEST


def test_nothing_has_been_run_yet() -> None:
    """يُعلَن في المتن أنّ الختمَ سبق النظر — والترتيبُ في التاريخ."""

    assert __doc__ is not None
    assert "**لم يُشغَّل شيءٌ بعد. ولم يُعَدّ محجوزٌ واحد.**" in __doc__


def test_the_deposited_ladder_is_named_as_a_different_support() -> None:
    """ولا يُطرَح رقمُ الملحَق المُؤرَّض من رقم المحجوز — العطل ٢٤."""

    assert "٠٫٤١٨٤" in THE_FLOOR_IS_REMOVED_AND_THAT_IS_THE_POINT
    assert "لا يُقابَلان" in THE_FLOOR_IS_REMOVED_AND_THAT_IS_THE_POINT
    assert __doc__ is not None
    text = " ".join(__doc__.split())
    assert "فههنا **لا أرضيّة**" in text
    assert "ولا يُستبعَد" in text


def test_the_proved_inequality_is_a_machine_condition_not_a_claim() -> None:
    """`H(X|Y,Z) ≤ H(X|Y)` مبرهَنةٌ، فارتفاعُها عطلُ حسابٍ لا خبرُ مادّة."""

    proved = next(one for one in PREDICTIONS if one.identifier == "ض٤")
    assert proved.threshold == Fraction(0)
    assert "مبرهَنةٌ" in proved.falsifies
    assert "عطلُ حسابٍ لا خبرُ مادّة" in proved.falsifies
    assert __doc__ is not None
    assert "والمحجوزُ **حرٌّ أن يرتفع**" in " ".join(__doc__.split())


def test_stirling_bounds_knowledge_not_computation() -> None:
    """حاجزُ ستيرلنغ حدٌّ على ما تُرجِّحه المادّةُ لا على ما تحسبه الآلة."""

    assert "حدٌّ على ما تستطيع المادّةُ" in STIRLING_BOUNDS_KNOWLEDGE_NOT_COMPUTATION
    assert "ولو كان الحسابُ رخيصًا" in STIRLING_BOUNDS_KNOWLEDGE_NOT_COMPUTATION
    assert any(one.identifier == "ض١١" for one in PREDICTIONS)
    assert any(one.identifier == "ض١٢" for one in PREDICTIONS)


def test_one_channel_is_not_a_language() -> None:
    """رتبةُ الانتحال رتبةُ هذه القناة — ولا تُقرَأ حدًّا للعربيّة."""

    assert "لا تُقرَأ حدًّا للعربيّة" in ONE_CHANNEL_IS_NOT_A_LANGUAGE
    assert __doc__ is not None
    assert "وقناةٌ أخرى قد تنقلب في غيرها" in " ".join(__doc__.split())


def test_four_refute_the_machine_and_eight_are_claims_of_mine() -> None:
    """أربعٌ تردُّ الآلةَ، وثمانٍ **دعاوٍ لي** تسقط بأرقامها."""

    machine = {"ض١", "ض٢", "ض٣", "ض٤"}
    mine = {one.identifier for one in PREDICTIONS} - machine
    assert len(mine) == 8
    for one in PREDICTIONS:
        if one.identifier in mine:
            assert "دعوايَ" in one.falsifies, one.identifier
        else:
            assert "الآلةَ" in one.falsifies, one.identifier
