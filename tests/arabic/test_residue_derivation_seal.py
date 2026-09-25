"""**ختمٌ قبل النظر**: إعادةُ البناء من الـ١١٢ وحدَها — أيُّ بتٍّ يبقى؟

**لم يُشغَّل شيءٌ بعد.**

**الدعوى المفحوصة**: «لا بتَّ إلّا ويُسهم في الإفادة». وصورتُها القابلةُ
للقياس: **قنواتُ البقيّة ليست خبرًا مستقلًّا، بل مشتقَّةٌ من تيّار الـ١١٢
نفسِه**. فإن صدقت، نزلت بتّاتُها إلى الصفر كلّما اتّسع السياقُ المقروءُ من
التيّار؛ وما بقي بعد ذلك **هو الإفادةُ الخالصة**، لا اصطلاحًا زائدًا.

**والفارقُ عن قياسي السابق**: شرطتُ هناك على **(الحرف، حركته، حركةِ ما
قبل)** — وهو أقلُّ ما يملكه فاكُّ الشفرة. وفاكُّ الشفرة يملك **التيّارَ
كلَّه**، قبلَ الموضع وبعدَه. فالسياقُ ههنا **متناظر**: `k` وحدةً عن
اليمين و`k` عن الشمال.

**القراراتُ تُختَم معها**: مواضعُ القرار كما في `c5a1e18` (لا مواضعُ الوقوع
وحدَها)؛ والسياقُ داخلَ الآية لا يعبرها؛ والرتبُ ٠ و١ و٢ و٣؛ وكلُّ رقمٍ
**محجوزٌ** بقسمة الآيات الزوجيّة/الفرديّة وتنعيمِ لابلاس **على أبجديّة
القناة وحدَها** (لا على كلّ الأشكال — وهو العطلُ الذي أفسد قياسَ الأرضيّة
المحجوزة في `f43b9095…`)؛ ويُنشَر نصيبُ المرتدّ مع كلّ رقم.
"""

from __future__ import annotations

from fractions import Fraction

from algebra.signified import Direction, Oracle, Prediction, seal

ORACLE = Oracle(
    name="إعادةُ بناء قنوات البقيّة من تيّار الـ١١٢",
    source="quran-simple-enhanced.txt — البصمة 37633090…",
    extraction=(
        "على مواضع القرار الخمسة من `c5a1e18`، تُقدَّر قيمةُ القناة من "
        "سياقٍ متناظرٍ من وحدات CV قدرُه k يمينًا وk شمالًا داخلَ الآية، "
        "k ∈ {٠،١،٢،٣}؛ والرقمُ إنتروبيا متقاطعةٌ محجوزةٌ بقسمة الآيات "
        "الزوجيّة/الفرديّة والعكس، بتنعيم لابلاس على أبجديّة القناة "
        "وحدَها، مع إعلان نصيب المرتدّ"
    ),
)

PREDICTIONS = (
    Prediction(
        identifier="و١",
        statistic=(
            "أدنى (المحجوزة عند الرتبة صفر − المحجوزة عند " "الرتبة ٣) لكلّ قناة (بت)"
        ),
        threshold=Fraction(0),
        direction=Direction.AT_LEAST,
        falsifies=(
            "المقدِّرَ لا المادّة: اتّساعُ السياق لا يزيد الخبرَ اللازم؛ "
            "فارتفاعُ قناةٍ عند الرتبة ٣ يعني نفادَ المادّة لا استقلالَ القناة"
        ),
    ),
    Prediction(
        identifier="و٢",
        statistic="مجموعُ بتّات القنوات الخمس عند أفضل رتبةٍ محجوزة",
        threshold=Fraction(46_726),
        direction=Direction.AT_MOST,
        falsifies=(
            "دعوى أنّ البقيّةَ مشتقّةٌ من التيّار: إن لم تنزل عن نصف "
            "٩٣٬٤٥٣ فأكثرُها خبرٌ مستقلٌّ عن الـ١١٢، لا صدًى لها"
        ),
    ),
    Prediction(
        identifier="و٣",
        statistic="أدنى إنتروبيا محجوزةٍ لقناةٍ واحدة (بت)",
        threshold=Fraction(5, 100),
        direction=Direction.AT_MOST,
        falsifies=(
            "دعوى أنّ في البقايا ما هو **قاعدةٌ محضة**: إن لم تنزل قناةٌ "
            "واحدةٌ تحت خمسة من مئةٍ فليس في الخمس قاعدةٌ تُستغنى عنها"
        ),
    ),
    Prediction(
        identifier="و٤",
        statistic="إنتروبيا قناة (ة مقابل ه) المحجوزةُ عند أفضل رتبة (بت)",
        threshold=Fraction(20, 100),
        direction=Direction.AT_LEAST,
        falsifies=(
            "قولي إنّ التاءَ المربوطةَ معجميّةٌ لا تُشتَقّ: إن نزلت تحت "
            "خُمس البتّ فهي مشتقّةٌ من الجوار، ويسقط تصنيفي لها"
        ),
    ),
    Prediction(
        identifier="و٥",
        statistic="أدنى (المحجوزة − الملحَقة) على القنوات والرتب (بت)",
        threshold=Fraction(0),
        direction=Direction.AT_LEAST,
        falsifies=("اتّجاهَ الانتحال؛ وهو الدرسُ الذي سقطت به نتيجتي في `ca8fd2c`"),
    ),
)

DIGEST = "92b817964498403872723adb515e445b423c0286a5c994d5be0cbb7d0035b240"
"""يُثبَّت بعد أوّل اشتقاق، ولا يُمَسّ بعدَه."""


def test_the_seal_is_recomputed_from_the_written_conditions() -> None:
    """البصمةُ تُشتَقّ من الشروط لا تُنقَل."""

    assert seal(ORACLE, PREDICTIONS) == DIGEST


def test_two_conditions_pull_in_opposite_directions() -> None:
    """و٣ يطلب قناةً تنزل، وو٤ يطلب قناةً تثبت — فلا يُرضيان بتأويل."""

    down = next(one for one in PREDICTIONS if one.identifier == "و٣")
    up = next(one for one in PREDICTIONS if one.identifier == "و٤")
    assert down.direction is Direction.AT_MOST
    assert up.direction is Direction.AT_LEAST
    assert down.threshold < up.threshold


def test_the_halving_threshold_is_half_the_published_residue() -> None:
    """٤٦٬٧٢٦ هو نصفُ ٩٣٬٤٥٣ المنشورةِ في `c5a1e18`."""

    halving = next(one for one in PREDICTIONS if one.identifier == "و٢")
    assert halving.threshold == Fraction(46_726)
    assert 46_726 * 2 == 93_452  # والمنشورُ ٩٣٬٤٥٣، فالحدُّ أشدُّ بواحد
