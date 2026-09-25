"""**ختمٌ قبل النظر**: أيعيد هوفمانُ — بالتردّد المقيس — ترتيبَ الجشع؟

**لم يُشغَّل شيءٌ على المدوّنة بعد.** والآلةُ جُرّبت على شريحةٍ من ثمانين
سطرًا، **وجاء فيها توافقُ الرتبة الأولى ٠٫٢٢٤٥ وتوافقُ القرار ٠٫٢٢٤٥**؛
ويُعلَن ذلك ههنا فما رأيتُه قبل الختم لا يُخفى. **ولا يُستخرَج من شريحةٍ
بهذا الصغر شيءٌ عن أرقام المدوّنة** — فالأزواجُ فيها تُعَدّ بالآحاد،
وفي المُجمَّد بالمئات والألوف، والاقتصادُ يختلف.

**السؤالُ المعزول**: الاقتراحُ في `69a1c10c…` يُرتَّب بـ**عدد الوقوع
الخام**، والحكمُ بـ**التكلفة الهوفمانيّة**. فإن قِيست `H` على المُجمَّد،
**أيعيد هوفمانُ ترتيبَ الجشع نفسَه**؟ أي: أيكون **الأكثرُ وقوعًا** هو
**الأكبرَ ربحًا**؟

**والمتغيّرُ واحد**: الضابطُ ذراعُ الوسم الأبديّ من `2cd80c0f…` بعمقه
نفسِه (٢٤) ووسمِه نفسِه ومدوّنته نفسِها — ولا يفترقان إلّا في **قاعدة
الاختيار**: «أوّلُ رابح» ههنا تصير «**أكبرُ ربحًا**».

**ورقمان لا رقمٌ واحد**: **توافقُ الرتبة** (أكبرُ ربحٍ هو الأوّلُ وقوعًا)
غيرُ **توافقِ القرار** (القاعدتان تلتزمان الزوجَ نفسَه)، ولا يُخلَطان.

**وعمقُ البحث محدودٌ معلنٌ**: فما يُبلَغ **حدٌّ أدنى** لا أعلى.

**ولا اسمَ لغويٌّ يدخل**: بتّاتٌ وعَرضٌ ووقوعاتٌ وتكلفةٌ فقط.
"""

from __future__ import annotations

from fractions import Fraction

from algebra.signified import Direction, Oracle, Prediction, seal

BY_CONTROL = 1_408_581
CONTROL_COMMITS = 2_308
BY_BLOCK = 1_394_638

ORACLE = Oracle(
    name="الترتيبُ بالتردّد المقيس فوق ١١٢ — أيعيد هوفمانُ ترتيبَ الجشع؟",
    source="quran-simple-enhanced.txt — البصمة 37633090…",
    extraction=(
        "آلةُ `69a1c10c…` بعمق `2cd80c0f…` (أعلى ٢٤ مقترَحًا متاحًا) "
        "ووسمِه الأبديّ؛ وفي كلّ حالٍ تُحسَب `Δ` للمقترَحات كلِّها ثمّ "
        "يُلتزَم **أكبرُها ربحًا** لا أوّلُها ربحًا. ويُسجَّل لكلّ حالٍ "
        "هل أكبرُ ربحٍ هو الأوّلُ وقوعًا، وهل تلتزم القاعدتان الزوجَ "
        "نفسَه؛ وتُطبَع `H` و`L` للحال عند كلّ نقطة فحص"
    ),
)

PREDICTIONS = (
    Prediction(
        identifier="ت١",
        statistic=("أقصى |الجملة من العدّادات − الجملة من الآيات| عند نقاط الفحص (بتًّا)"),
        threshold=Fraction(1, 1000),
        direction=Direction.AT_MOST,
        falsifies="الآلةَ لا المادّة: انحرافُ العدّادات يردّ التشغيلَ كلَّه",
    ),
    Prediction(
        identifier="ت٢",
        statistic="مواضعُ الخلاف بين بسطِ الرموز بالهجاء ومجرى L₀",
        threshold=Fraction(0),
        direction=Direction.AT_MOST,
        falsifies="الرجعةَ: أيُّ خلافٍ ضياعٌ لا ضغط",
    ),
    Prediction(
        identifier="ت٣",
        statistic="عددُ الالتزامات التي لم تنزل عندها التكلفةُ المحجوزة",
        threshold=Fraction(0),
        direction=Direction.AT_MOST,
        falsifies="أنّ الرخصةَ بقيت للدمجة الواحدة مع تبدّل قاعدة الاختيار",
    ),
    Prediction(
        identifier="ت٤",
        statistic="نسبةُ الحالات التي يكون فيها الأكبرُ ربحًا هو الأوّلَ وقوعًا",
        threshold=Fraction(1, 2),
        direction=Direction.AT_LEAST,
        falsifies=(
            "الدعوى المسؤولَ عنها: أنّ هوفمانَ بالتردّد المقيس يعيد ترتيبَ "
            "الجشع. فإن نزلت النسبةُ عن النصف فالعددُ الخامُ **ليس** وكيلًا "
            "عن الربح، والترتيبُ الذي بُني عليه الصعودُ كلُّه ترتيبُ عدٍّ "
            "لا ترتيبُ اقتصاد — ويُنشَر ذلك بلا تجميل"
        ),
    ),
    Prediction(
        identifier="ت٥",
        statistic="عددُ الحالات التي يخالف فيها «أوّلُ رابح» «أكبرَ ربحًا»",
        threshold=Fraction(0),
        direction=Direction.AT_MOST,
        falsifies=(
            "الصورةَ القويّةَ من الدعوى: أن تكون القاعدتان واحدةً في الأثر. "
            "وحالٌ واحدةٌ تختلفان فيها تكفي لإسقاطها، ويكون الترتيبُ "
            "بالتردّد المقيس **مسارًا آخرَ** لا صياغةً أخرى للمسار نفسِه"
        ),
    ),
    Prediction(
        identifier="ت٦",
        statistic="الجملةُ المحجوزةُ عند الوقوف (بتًّا)",
        threshold=Fraction(BY_CONTROL),
        direction=Direction.AT_MOST,
        falsifies=(
            "أنّ أخذَ أكبرِ ربحٍ في كلّ حالٍ لا يكون أسوأَ من أخذِ أوّلِ "
            "رابح؛ فإن جاء أغلى فالأمثلُ محلّيًّا **أضرُّ** من الكافي "
            "محلّيًّا، وهو خبرٌ عن الجشع لا عن المادّة"
        ),
    ),
    Prediction(
        identifier="ت٧",
        statistic="الجملةُ المحجوزةُ عند الوقوف (بتًّا) — مقابلَ الكتليّ",
        threshold=Fraction(BY_BLOCK + 1),
        direction=Direction.AT_LEAST,
        falsifies=(
            "دعوى أنّ الترخيصَ بتّةً بتّة لا يبلغ الكتليَّ بأيّ قاعدةِ "
            "اختيار؛ فإن بلغه الترتيبُ بالتردّد المقيس فالخسارةُ كانت من "
            "**قاعدة الترتيب** لا من الترخيص، وتُعاد قراءةُ الأختام الثلاثة"
        ),
    ),
    Prediction(
        identifier="ت٨",
        statistic="أدنى (L − H) على نقاط الفحص بالتردّد المقيس (بتًّا للرمز)",
        threshold=Fraction(0),
        direction=Direction.AT_LEAST,
        falsifies=(
            "مبرهنةَ شانون: شفرةٌ فكّها ممكنٌ لا تنزل تحت الإنتروبيا، "
            "فنزولٌ ههنا عطلُ قياسٍ لا اكتشاف"
        ),
    ),
    Prediction(
        identifier="ت٩",
        statistic="أقصى (L − H) على نقاط الفحص بالتردّد المقيس (بتًّا للرمز)",
        threshold=Fraction(999, 1000),
        direction=Direction.AT_MOST,
        falsifies=(
            "حدَّ هوفمان الأعلى `L < H + 1`؛ فتجاوزُه يعني أنّ المبنيَّ "
            "ليس شفرةَ هوفمان، وتسقط دعوى «الجشعُ المبرهَن» في شطر الترميز"
        ),
    ),
)

DIGEST = "c8602c000f5a52a7804628644f5dd19d1edee25d74332fe40731d7b5622a9b8e"
"""يُثبَّت بعد أوّل اشتقاق، ولا يُمَسّ بعدَه."""


def test_the_seal_is_recomputed_from_the_written_conditions() -> None:
    """البصمةُ تُشتَقّ من الشروط لا تُنقَل."""

    assert seal(ORACLE, PREDICTIONS) == DIGEST


def test_the_rank_and_the_decision_are_two_numbers_not_one() -> None:
    """توافقُ الرتبة غيرُ توافقِ القرار — وخلطُهما خلطُ مقياسين."""

    rank = next(one for one in PREDICTIONS if one.identifier == "ت٤")
    choice = next(one for one in PREDICTIONS if one.identifier == "ت٥")
    assert "الأوّلَ وقوعًا" in rank.statistic
    assert "«أوّلُ رابح»" in choice.statistic
    assert rank.direction is Direction.AT_LEAST
    assert choice.direction is Direction.AT_MOST
    assert len(PREDICTIONS) == 9


def test_the_isolation_changes_only_the_choice_rule() -> None:
    """العمقُ والوسمُ والمدوّنةُ من `2cd80c0f…` — والقاعدةُ وحدَها تتبدّل."""

    assert "أعلى ٢٤ مقترَحًا متاحًا" in ORACLE.extraction
    assert "ووسمِه الأبديّ" in ORACLE.extraction
    assert "أكبرُها ربحًا** لا أوّلُها ربحًا" in ORACLE.extraction


def test_two_conditions_are_shannon_and_huffman_not_claims_of_mine() -> None:
    """ت٨ وت٩ حدّان مبرهَنان — وسقوطُ أحدهما عطلُ قياس."""

    low = next(one for one in PREDICTIONS if one.identifier == "ت٨")
    high = next(one for one in PREDICTIONS if one.identifier == "ت٩")
    assert low.threshold == Fraction(0)
    assert high.threshold < Fraction(1)
    assert "شانون" in low.falsifies and "هوفمان" in high.falsifies


def test_the_slice_i_saw_before_sealing_is_declared() -> None:
    """ما رأيتُه قبل الختم مكتوبٌ فيه — ولا يُخفى بعد النظر."""

    assert __doc__ is not None
    assert "٠٫٢٢٤٥" in __doc__
    assert "ثمانين" in __doc__
