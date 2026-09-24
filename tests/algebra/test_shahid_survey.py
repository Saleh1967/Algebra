"""استطلاعا النثر مقروءَين ثانيةً: ت٢ قائمة، وت٣ **غيرُ مُثبَتةٍ لا ساقطة**.

**تصويبُ ما كتبتُه في الجولة السابقة**: قلتُ «ت٣ ساقطةٌ بقاعدة ش٢». وذلك
تجاوزٌ في اللفظ وفي الحساب معًا، وأصحّحه ههنا بثلاثة أشياء:

`THE_SQUARE_ROOT_RULE_IS_THE_EXTREME_NOT_A_NEUTRAL_CORRECTION`: القسمةُ على
`√m̄` تكافئ `ρ = 1` في `DEFF = 1 + (m̄ − 1)ρ`. و`ρ` **لم يُقَس**. وعند قيمٍ
أدنى يبلغ ت٣ الحدَّ: عند ٠٫٥ يعطي ٢٫٣٨٨، وعند ٠٫٢ يعطي ٢٫٩٦٢، وعند ٠٫٠٥
يعطي ٣٫٤٦٥. فالحكمُ السابقُ كان قائمًا على معاملٍ مفروضٍ عند أقصاه.

`A_CONSERVATIVE_BOUND_CANNOT_REFUTE`: ومن لم يبلغ حدًّا محافظًا فهو **غيرُ
مُثبَت**، لا مردود. والحدُّ المحافظ يضخّم الخطأ عمدًا، فمن بلغه ثبت رغم
التضخيم، ومن لم يبلغه لم يُقَل فيه شيء. و«ساقطة» تمنح الحدَّ سلطةَ نفيٍ لا
يملكها.

`THE_ZERO_MEDIAN_INVALIDATES_THE_VERY_MEAN_IT_WAS_READ_WITH`: وأشدُّها: إن
كان نصفُ العقد بلا حافّةٍ فمتوسّطُ **ذوي الحافّة** ٧٫٦٠ لا ٣٫٨٠. فالعددُ
الذي قسمتُ به مأخوذٌ على جمهورٍ نصفُه لا يُسهم. والاتّجاهُ لا ينقلب —
ت٣ تصير ١٫٣٤٢ وت٢ ٧٫١١ — لكنّ **حدَّ التعادل ٣٫٥٦ يفقد معناه**، إذ قِيس
على مقامٍ غيرِ الذي يُقارَن به.

`THE_BREAK_EVEN_WAS_NEVER_AN_INDEPENDENT_PATH`: وقلتُ «التقديرُ والقياسُ
التقيا من طريقين»، وذلك غيرُ صحيح. فـ`(3.7/1.96)² = 3.5636` مشتقٌّ جبريًّا
من ٣٫٧ و١٫٩٦، و«٣٫٨ > ٣٫٥٦» هي **نفسُها** «٣٫٧/√٣٫٨ < ١٫٩٦» مرتَّبةً. طريقٌ
واحدٌ كُتِب مرّتين، لا طريقان التقيا.

`ONE_ESTIMATOR_FOR_BOTH_CLAIMS_OR_NEITHER`: وبقي أعدلُ ما في النقد: حُكِم
لـت٢ **بالمعاودة المجمَّعة** وعلى ت٣ **بالحدّ المحافظ** — مكيالان. والأداةُ
مبنيّةٌ سلفًا، فصارت تُشغَّل على كسب ش٥ كما تُشغَّل على فرق ت٢، ويُطبَع مع
كلّ مجالٍ **عددُ معاوداته**؛ فمجالٌ بلا `B` لا تُعرَف أرضيّتُه.
"""

from __future__ import annotations

import math
from fractions import Fraction

from algebra.attainability import permutation_floor
from algebra.design_effect import (
    ClusterProfile,
    EffectStanding,
    design_effect,
    read_effect,
    refuted_against,
)
from algebra.reconciliation import rounds_to
from algebra.results import Vacancy

# منقولةٌ عن النثر: (المرصودُ المقترن، أدنى المجال، أعلاه، z)
PAIRED = (Fraction("0.1342"), Fraction("0.122"), Fraction("0.147"), 21.1)

DEGREE_MEDIAN, DEGREE_P90, DEGREE_MEAN, DEGREE_MAX = 0, 8, Fraction(19, 5), 341
ISOLATED = Fraction(1, 2)
"""حدٌّ أدنى يلزم عن وسيطٍ صفر؛ والنصيبُ الحقيقيُّ يُعلَن ولا يُقدَّر."""

RAW_Z = {"ت٢": 19.6, "ت٣": 3.7}
CONVENTIONAL = Fraction(49, 25)


def _profile(isolated: Fraction) -> ClusterProfile:
    return ClusterProfile(observations=19, clusters=5, isolated=isolated)


def test_the_square_root_rule_is_the_correlation_fixed_at_one() -> None:
    """القسمةُ على √٣٫٨ هي `DEFF` عند `ρ = 1` — لا تصحيحٌ محايد."""

    assert design_effect(DEGREE_MEAN, Fraction(1)) == DEGREE_MEAN
    assert math.isclose(
        RAW_Z["ت٣"] / math.sqrt(float(DEGREE_MEAN)), 1.8981, abs_tol=1e-4
    )

    table = {
        Fraction(1): Fraction(19, 5),
        Fraction(1, 2): Fraction(12, 5),
        Fraction(1, 5): Fraction(39, 25),
        Fraction(1, 20): Fraction(57, 50),
    }
    for correlation, effect in table.items():
        assert design_effect(DEGREE_MEAN, correlation) == effect


def test_at_lower_correlations_the_third_finding_reaches_the_threshold() -> None:
    """٢٫٣٨٨ و٢٫٩٦٢ و٣٫٤٦٥ — ثلاثُ قيمٍ تبلغ الحدَّ، والحكمُ السابقُ فرض أقصاها."""

    outcomes = {}
    for correlation in (Fraction(1), Fraction(1, 2), Fraction(1, 5), Fraction(1, 20)):
        reading = read_effect(
            RAW_Z["ت٣"], _profile(Fraction(0)), correlation=correlation
        )
        outcomes[correlation] = (round(reading.deflated, 3), reading.standing)

    assert outcomes[Fraction(1)] == (1.898, EffectStanding.UNESTABLISHED)
    assert outcomes[Fraction(1, 2)] == (2.388, EffectStanding.ESTABLISHED)
    assert outcomes[Fraction(1, 5)] == (2.962, EffectStanding.ESTABLISHED)
    assert outcomes[Fraction(1, 20)] == (3.465, EffectStanding.ESTABLISHED)


def test_not_reaching_a_conservative_bound_is_not_a_refutation() -> None:
    """«لم يُثبَت» منزلةٌ، و«مردود» بابُه هامشٌ مُعلَنٌ ومجالٌ مقيس."""

    bound = read_effect(RAW_Z["ت٣"], _profile(Fraction(0)))
    assert bound.standing is EffectStanding.UNESTABLISHED
    assert bound.standing is not EffectStanding.REFUTED
    assert bound.is_a_bound_not_an_estimate

    # والردُّ لا يُبلَغ إلّا بمجالٍ أعلاه دون هامشٍ كُتِب قبل النظر
    margin = Fraction(5, 100)
    assert refuted_against((Fraction(1, 100), Fraction(2, 100)), margin) is (
        EffectStanding.REFUTED
    )
    assert refuted_against((Fraction(1, 100), Fraction(9, 100)), margin) is (
        EffectStanding.UNESTABLISHED
    )

    # ومنزلةُ ت٣ الآن `UNRUN` لا `REFUSED`: فحصُها مُعيَّنٌ ولم يُجرَ بعدُ
    assert Vacancy.UNRUN.value == "فحصُها مُعيَّنٌ ولم يُجرَ"
    assert Vacancy.UNRUN is not Vacancy.REFUSED


def test_a_zero_median_moves_the_mean_that_the_rule_divides_by() -> None:
    """٣٫٨ على الكلّ و٧٫٦٠ على ذوي الشاهد — والقسمةُ تكون بالثاني."""

    profile = _profile(ISOLATED)
    assert profile.mean_over_all == DEGREE_MEAN
    assert profile.mean_over_active == Fraction(38, 5)

    third = read_effect(RAW_Z["ت٣"], profile)
    second = read_effect(RAW_Z["ت٢"], profile)
    assert round(third.deflated, 3) == 1.342
    assert round(second.deflated, 2) == 7.11
    assert second.standing is EffectStanding.ESTABLISHED
    assert third.standing is EffectStanding.UNESTABLISHED

    assert DEGREE_MEDIAN == 0
    assert DEGREE_MAX > DEGREE_P90 * 40


def test_the_break_even_is_the_same_inequality_rearranged() -> None:
    """`(z/c)² < m̄` و`z/√m̄ < c` قولٌ واحد — فلا طريقين التقيا."""

    z, threshold = RAW_Z["ت٣"], float(CONVENTIONAL)
    break_even = (z / threshold) ** 2
    assert round(break_even, 4) == 3.5636
    same = z / math.sqrt(float(DEGREE_MEAN)) < threshold
    assert (break_even < float(DEGREE_MEAN)) is same

    # وليس ٣٫٥٦ قياسًا مستقلًّا: مقامُه ٣٫٧ و١٫٩٦ لا بياناتٌ أخرى
    assert break_even != float(DEGREE_MEAN)


def test_an_interval_without_its_replicate_count_has_no_floor() -> None:
    """مجالٌ بلا `B` لا تُعرَف أرضيّتُه، كما لا تُقرأ `p` بلا عدد التباديل."""

    mean, low, high, _ = PAIRED
    assert low < mean < high and low > 0
    assert rounds_to((high - low) * 1_000, 0) == 25

    declared = 1_000
    assert permutation_floor(declared) == Fraction(1, 1_001)
    # والمنشورُ في الجولة السابقة كان بلا `B`؛ وقد صار يُطبَع مع كلّ مجال
    assert permutation_floor(declared) > 0
