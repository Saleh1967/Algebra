"""**ختمٌ قبل النظر**: أرضيّةُ الرسم — أوّلُ حدٍّ **أدنى** في هذه السلسلة.

**لم يُشغَّل شيءٌ بعد.**

**العِلّة**: كلُّ ما قيس إلى الآن **حدودٌ عليا**: ١٫٩٥٥١ و١٫٥٦١٩ و١٫٣١٧٧ —
كلُّها تقول «لا يزيد»، ولا واحدةَ تقول «**لا ينزل**». وحدٌّ أعلى وحدَه لا
يُبرهن أنّ في الضبط خبرًا؛ يُبرهنه **حدٌّ أدنى**.

**المبرهنة المقصودة** (حدُّ شانون لترميز المصدر، مشروطًا بالبايتات):

> ليكن W رسمُ الكلمة كاملًا (تسلسلُ حروفها بعد التطبيع)، وS تسلسلُ حالاتها.
> فلأيّ مُرمِّزٍ **لا يرى إلّا W**، متوسّطُ طولِ الشفرة على هذه المدوّنة
> **لا ينزل عن H(S | W)**؛ وأدنى ما يبلغه هو H(S | W) بعينها.

وهذه **مبرهنةٌ لا تقدير**: على مجمَّدٍ متناهٍ، H(S|W) مقدارٌ يُحسَب بالضبط،
والحدُّ يلزم عنه بالمبرهنة. وقيدُها المعلن: **قارئُ الكلمة وحدَها**؛ ومَن
رأى ما حولَها قد ينزل عنها.

**والتفكيكُ التامّ**: H(S|L) = Σ_c P(c)·H(S|L، c) على قسمةٍ c دالّةٍ في
الحرف — **إعادةُ تجميعٍ لا تقريب**، فيجب أن تُطابق المجموعَ إلى حدّ
الفاصلة العائمة. فإن لم تُطابق فالخللُ في الحساب لا في المادّة.

**القراراتُ تُختَم معها**: الكلمةُ ما فصلته الفراغات بعد طرح الوسم؛ والرسمُ
حروفُ π_إملائي المطبَّعة؛ والحالةُ تسلسلُ العلامات بلا توسيعِ شدّة؛
والأرضيّةُ تُقسَّم على **مواضع الرسم** لتُقارَن بـ١٫٣١٧٧؛ وتُنشَر معها
**نسخةٌ محجوزةٌ** بالقسمة الزوجيّة/الفرديّة؛ وشواهدُ الالتباس **تُعرَض
بأسمائها** ولا تُختصَر في عدد.
"""

from __future__ import annotations

from fractions import Fraction

from algebra.signified import Direction, Oracle, Prediction, seal

ORACLE = Oracle(
    name="أرضيّةُ الرسم — H(الضبط | رسمِ الكلمة)",
    source="quran-simple-enhanced.txt — البصمة 37633090…",
    extraction=(
        "الكلمةُ ما فصلته الفراغاتُ بعد طرح الوسم؛ وW تسلسلُ حروفها بعد "
        "تطبيع π_إملائي؛ وS تسلسلُ حالاتها بلا توسيعِ شدّة؛ "
        "H(S|W) = Σ_w P(w)·H(p_w) موزونةً بتكرار الكلمة ومقسومةً على "
        "مواضع الرسم؛ ومعها نسخةٌ محجوزةٌ بقسمةِ الأسطر الزوجيّة/الفرديّة "
        "وتنعيمِ لابلاس؛ والتفكيكُ H(S|L) = Σ_c P(c)·H(S|L،c) على قسمةٍ "
        "دالّةٍ في الحرف"
    ),
)

PREDICTIONS = (
    Prediction(
        identifier="ج١",
        statistic="|تفكيكُ H(S|L) مجموعًا − H(S|L) مباشرةً| (بت)",
        threshold=Fraction(1, 1_000_000),
        direction=Direction.AT_MOST,
        falsifies=(
            "الحسابَ لا المادّة: التفكيكُ إعادةُ تجميعٍ تُوجبها قاعدةُ "
            "السلسلة، فاختلافُه عن المجموع عطلُ آلةٍ يردّ الجدولَ كلَّه"
        ),
    ),
    Prediction(
        identifier="ج٢",
        statistic="أرضيّةُ الرسم H(S|W) (بت/موضع)",
        threshold=Fraction(0),
        direction=Direction.AT_LEAST,
        falsifies=(
            "دعوى وجودِ الأرضيّة أصلًا: إن كانت صفرًا فرسمُ الكلمة يعيّن "
            "ضبطَها تعيينًا تامًّا في هذه المدوّنة، ولا خبرَ في الشكل البتّة"
        ),
    ),
    Prediction(
        identifier="ج٣",
        statistic="أرضيّةُ الرسم H(S|W) (بت/موضع)",
        threshold=Fraction(1, 2),
        direction=Direction.AT_MOST,
        falsifies=(
            "قولي إنّ رسمَ الكلمة يعيّن أكثرَ ضبطِها: إن جاوزت الأرضيّةُ "
            "نصفَ البتّ فالالتباسُ بنيويٌّ واسع، ولا يكفي السياقُ لردّه"
        ),
    ),
    Prediction(
        identifier="ج٤",
        statistic="نصيبُ وقوعاتِ الكلم التي رسمُها ملتبسٌ في المدوّنة",
        threshold=Fraction(1, 10),
        direction=Direction.AT_LEAST,
        falsifies=(
            "دعوى أنّ الالتباسَ ظاهرةٌ عامّةٌ لا شاذّة: إن نزل عن العُشر "
            "فالأرضيّةُ أثرُ قلّةٍ نادرةٍ وتُنسَب إليها لا إلى الخطّ"
        ),
    ),
    Prediction(
        identifier="ج٥",
        statistic="المحجوزةُ على مستوى الكلمة − الملحَقة (بت/موضع)",
        threshold=Fraction(0),
        direction=Direction.AT_LEAST,
        falsifies=(
            "اتّجاهَ الانتحال: التقديرُ داخلَ العيّنة لا يَزيد على المحجوز، "
            "وهو الدرسُ الذي سقطت به نتيجتي في `ca8fd2c`"
        ),
    ),
)

DIGEST = "f43b9095125dc2d6ef08cbeb45593f23ca4a58efe1dfe46392af850979dad2d3"
"""يُثبَّت بعد أوّل اشتقاق، ولا يُمَسّ بعدَه."""


def test_the_seal_is_recomputed_from_the_written_conditions() -> None:
    """البصمةُ تُشتَقّ من الشروط لا تُنقَل."""

    assert seal(ORACLE, PREDICTIONS) == DIGEST


def test_this_is_the_first_lower_bound_in_the_series() -> None:
    """ج٢ وج٣ يحاصران الأرضيّةَ من تحتُ ومن فوق — ولم يسبق حدٌّ أدنى."""

    floor = [one for one in PREDICTIONS if one.statistic.startswith("أرضيّةُ")]
    assert len(floor) == 2
    assert {one.direction for one in floor} == {
        Direction.AT_LEAST,
        Direction.AT_MOST,
    }
    assert {one.identifier for one in floor} == {"ج٢", "ج٣"}


def test_two_conditions_guard_the_machine_and_three_the_claim() -> None:
    """ج١ وج٥ عن الآلة، وج٢ وج٣ وج٤ عن المادّة."""

    machine = {"ج١", "ج٥"}
    matter = {"ج٢", "ج٣", "ج٤"}
    assert machine | matter == {one.identifier for one in PREDICTIONS}
    assert not machine & matter
    for one in PREDICTIONS:
        assert one.falsifies.strip()
