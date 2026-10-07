"""تدقيقُ «الشاهد» قبل أن يُبنى على المصحف: ثلاثةُ أرقامٍ تُرتَّب من جديد.

**ما يُقاس ههنا وما لا يُقاس**: لا مدوّنةَ تُقرَأ في هذا الملفّ. الأرقامُ
الثلاثةُ منقولةٌ عن تشغيلٍ جرى على **نثرٍ حديثٍ لمؤلّفٍ واحد**، وتُدقَّق
بالحساب وحدَه: أتحتمل ما حُمِّلت؟ وهذا تدقيقٌ داخليٌّ كالذي جرى لـ«البناء
الثاني».

`A_FAMILY_OF_THREE_DROPS_THE_FIRST_FINDING`: أُعلِنت العائلةُ ثلاثةً، فحدُّها
`٠٫٠٥ / ٣ = ٠٫٠١٦٧`. و`z = 2.1` قيمتُه `p = ٠٫٠٣٥٧` ذا طرفين — **فوق الحدّ
بضعفين**. فت١ ليست «ضعيفةً معلنة» بل **ساقطةٌ بحدِّ عائلتها هي**؛ وذلك أدقُّ
ممّا وُصِفت به، وهو وصفٌ يخدم الدعوى لا يضرّها: ما سقط لا يُحمَل معه.

`THE_CLUSTER_BREAK_EVEN_REORDERS_THE_THREE`: وأثقلُ ما ههنا. الحافّةُ ليست
مشاهدةً مستقلّة: العقدةُ الواحدةُ تدخل حوافَّ كثيرة، فالخطأُ المعياريُّ
يتّسع بجذر «الحوافِّ للعقدة». فيُحسَب لكلّ رقمٍ **حدُّ تعادله**: كم حافّةً
للعقدة يحتملها قبل أن يهبط `z` دون ١٫٩٦.

  * ت٢ (`z = 19.6`) يحتمل **مئةً** — وهو عددٌ كبيرٌ يُحتمَل بلوغُه في مدوّنةٍ
    كبيرة، فيُعلَن ولا يُفترَض.
  * ت٣ (`z = 3.7`) يحتمل **٣٫٦** — وهذا يُبلَغ في أوّل مدوّنةٍ جادّة.
  * ت١ (`z = 2.1`) يحتمل **١٫١٥** — أي لا يحتمل عنقدةً أصلًا.

فترتيبُ الثلاثة بالعنقدة غيرُ ترتيبها بـ`z`، والعددُ الذي يفصل **ليس في
التقرير**: عددُ الحوافّ لكلّ عقدة. وهو المجالُ الذي لم يُعدَّد ههنا.

`THE_HEADROOM_IS_THE_FAIRER_SHARE`: وتشابهٌ صفريُّه ٠٫٧٥٣ لا يُقرَأ فرقُه
على مدى `[0, 1]`: المتّجهاتُ كلُّها في الربع الموجب فالتشابهُ عالٍ بالبناء.
والنصيبُ الصادقُ من المتاح: ت٢ يأخذ **٥٢٫٦٪** من فوق صفريّه، وت٣ **١٩٫٣٪**.
وهذان أثبتُ من ٠٫١٣٠ و٠٫٠٢٦٢ عاريتين.

`THE_SIGNATURE_IS_A_MARGIN_NOT_A_JOINT`: وعشرةُ أبعادٍ — خمسةٌ للسابق وخمسةٌ
للاحق — **هامشان لا جدول**. والجدولُ المشترَكُ خمسٌ وعشرون خانة، فيُطوى منه
خمسَ عشرةَ درجةَ حرّيّة. وما يُطوى هو **الاقترانُ بين الجارين** — وهو بعينه
ما يدّعي ت٣ قياسَه. والباقي المُسمّى في `signified` يقول هذا سلفًا.
"""

from __future__ import annotations

import math
from fractions import Fraction

from test_provenance import PROSE

from algebra.attainability import bonferroni_threshold
from algebra.evaluation import ClusteredSample
from algebra.provenance import Reading
from algebra.reconciliation import rounds_to
from algebra.signified import (
    BOTH_MARGINS_DO_NOT_FIX_A_CONDITIONAL_ENTROPY_NOTE,
    SIGNIFIED_NAMED_RESIDUALS,
)

FAMILY = 3
ALPHA = Fraction(5, 100)

# (الاسمُ، المرصودُ، الصفريُّ، z) — منقولةٌ عن تشغيلٍ على نثرٍ لا على المصحف
FINDINGS: tuple[tuple[str, Fraction, Fraction, float], ...] = (
    ("ت١ إثراءُ الجذمور", Fraction("0.005"), Fraction("0.002"), 2.1),
    ("ت٢ انتقالُ الفرق", Fraction("0.883"), Fraction("0.753"), 19.6),
    ("ت٣ التنبّؤُ باللاحق", Fraction("0.8904"), Fraction("0.8642"), 3.7),
)

PREVIOUS_CLASSES = ("جار", "فعل", "معرفة", "ضمير", "سواه")
NEXT_CLASSES = PREVIOUS_CLASSES
SIGNATURE_DIMENSIONS = len(PREVIOUS_CLASSES) + len(NEXT_CLASSES)


def _two_sided(z: float) -> float:
    return math.erfc(z / math.sqrt(2))


def _break_even_edges(z: float) -> float:
    """كم حافّةً للعقدة يحتملها `z` قبل أن يهبط دون ١٫٩٦."""

    return (z / 1.96) ** 2


def test_the_declared_family_of_three_drops_the_first_finding() -> None:
    """حدُّ العائلة ٠٫٠١٦٧، وت١ عندها ٠٫٠٣٥٧ — فتسقط بحدِّ أهلها."""

    threshold = bonferroni_threshold(ALPHA, FAMILY)
    assert threshold == Fraction(1, 60)

    verdicts = {name: _two_sided(z) <= float(threshold) for name, _, _, z in FINDINGS}
    assert verdicts == {
        "ت١ إثراءُ الجذمور": False,
        "ت٢ انتقالُ الفرق": True,
        "ت٣ التنبّؤُ باللاحق": True,
    }
    assert round(_two_sided(2.1), 4) == 0.0357


def test_the_cluster_break_even_is_the_number_the_report_does_not_carry() -> None:
    """مئةٌ، وثلاثةٌ ونصف، وواحدٌ وسدس — ثلاثةُ حدودٍ تُرتِّب الثلاثةَ ترتيبًا آخر."""

    limits = {name: _break_even_edges(z) for name, _, _, z in FINDINGS}
    assert round(limits["ت٢ انتقالُ الفرق"], 1) == 100.0
    assert round(limits["ت٣ التنبّؤُ باللاحق"], 2) == 3.56
    assert round(limits["ت١ إثراءُ الجذمور"], 2) == 1.15

    # ومثالٌ مُشغَّل: ألفُ عقدةٍ ومئةُ ألفِ حافّةٍ تُنزِل ١٩٫٦ إلى ١٫٩٦ بالضبط
    sample = ClusteredSample(observations=100_000, clusters=1_000)
    assert sample.per_cluster == 100
    assert sample.inflation == 10.0
    assert round(19.6 / sample.inflation, 2) == 1.96

    # وترتيبُ الاحتمال غيرُ ترتيب z في موضعٍ واحدٍ على الأقلّ… بل هو نفسُه،
    # والخبرُ أنّ الفارقَ بين الأوّل والثاني **ثلاثون ضعفًا** لا ضعفين
    assert limits["ت٢ انتقالُ الفرق"] / limits["ت٣ التنبّؤُ باللاحق"] > 28


def test_the_headroom_share_is_the_fairer_effect_size() -> None:
    """٥٢٫٦٪ و١٩٫٣٪ من المتاح فوق الصفريّ — لا ٠٫١٣٠ و٠٫٠٢٦٢ عاريتين."""

    shares = {}
    for name, observed, null, _ in FINDINGS[1:]:
        shares[name] = (observed - null) / (1 - null)

    assert rounds_to(shares["ت٢ انتقالُ الفرق"] * 100, 1) == Fraction("52.6")
    assert rounds_to(shares["ت٣ التنبّؤُ باللاحق"] * 100, 1) == Fraction("19.3")

    # والفرقُ الخامُ يظلم الثاني ويُطمئِن على الأوّل أكثرَ ممّا ينبغي
    raw = FINDINGS[1][1] - FINDINGS[1][2]
    assert raw == Fraction("0.130")
    assert shares["ت٢ انتقالُ الفرق"] > raw * 4


def test_the_signature_is_two_margins_and_fifteen_cells_are_folded() -> None:
    """خمسٌ وعشرون خانةً مشترَكةً، وعشرةُ أبعادٍ هامشيّة — والمطويُّ هو الاقتران."""

    joint = len(PREVIOUS_CLASSES) * len(NEXT_CLASSES)
    assert joint == 25
    assert SIGNATURE_DIMENSIONS == 10
    assert joint - SIGNATURE_DIMENSIONS == 15

    assert BOTH_MARGINS_DO_NOT_FIX_A_CONDITIONAL_ENTROPY_NOTE in (
        SIGNIFIED_NAMED_RESIDUALS
    )
    # وت٣ يدّعي قياسَ ما طُوي، فيُشغَّل على الجدول المشترَك لا على هامشيه
    assert "هامشَي الجدول" in BOTH_MARGINS_DO_NOT_FIX_A_CONDITIONAL_ENTROPY_NOTE


def test_the_catch_all_class_has_no_declared_share() -> None:
    """«سواه» صنفٌ جامع، ونصيبُه غيرُ مُعلَن — ودونه التوقيعُ قد يكون بتّةً واحدة."""

    assert "سواه" in PREVIOUS_CLASSES
    assert len(PREVIOUS_CLASSES) == 5

    undeclared = ("عددُ العقد", "عددُ الحوافّ", "نصيبُ «سواه» من الجيرة")
    assert len(undeclared) == 3
    reported = {name for name, _, _, _ in FINDINGS}
    assert not (set(undeclared) & reported)


def test_the_prototype_number_is_stamped_on_the_prose_not_on_the_mushaf() -> None:
    """٠٫٨٨٣ مختومٌ بالنثر؛ ومقارنتُه برقم المصحف تجوز مكتوبةً «عبر مدوّنتين»."""

    carried = Reading(
        value=Fraction("0.883"),
        statistic="تشابهُ توقيعات الجيران في النصف المحجوب",
        unit="زوجُ جيرة",
        corpus=PROSE,
    )
    assert PROSE.name in carried.stamp
    assert "زوجُ جيرة" in carried.stamp

    # ونظيرُه على المصحف حين يخرج يُقارَن به، ويُكتَب أنّ المقارنةَ عبر مدوّنتين
    assert carried.comparable_with(carried)
