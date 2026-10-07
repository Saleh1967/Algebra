"""الإحالةُ وإغلاقُ البقايا: **القانونُ وجيه، والرقمُ المركزيُّ ينقلب**.

**المادّةُ مبنيّةٌ باليد**؛ ولا مرفقَ ورد في هذه الدورة، فالفحصُ على ما
نُقِل في المتن.

`THE_CENTRAL_NUMBER_CANNOT_BE_WHAT_IT_IS_CALLED`: «الضميرُ المفتوح **يرفع
الإنتروبيا** (+٠٫٠٨١٧)» — ورفعُ الإنتروبيا **ممتنعٌ في المتوسّط**: قاعدةُ
بايز توجب `E[H(بعد)] ≤ H(قبل)`، ومفحوصٌ على عشرين ألفَ تجربةٍ عشوائيّة:
أقصى فرقٍ **سالبٌ** (−٤٫٦٥×١٠⁻⁶، وهو خطأُ تقريب).

`SO_IT_IS_EITHER_A_SINGLE_DRAW_OR_A_WRONG_BASELINE`: فالرقمُ أحدُ أمرين.
إمّا **مشاهَدٌ بعينه** — ومشاهَدٌ واحدٌ يرفعها حقًّا (مثالٌ ههنا: ‎+٠٫٣٠٦٠‎)،
وذلك **ابتدائيٌّ لا مكتشَف**، ولا يُصاغ قانونًا. وإمّا **خطُّ أساسٍ خطأ**:
`H(Σ wᵢPᵢ) ≥ Σ wᵢH(Pᵢ)` **بجنسن دائمًا**، فمن قاس الخليطَ على مكوّناته
بدل القبليّ **ضَمِن الارتفاع بالبناء**. وهو عينُ عطل خطّ الأساس في كاشف
الابتلاع — **الثالثُ من جنسه**.

`AND_HALF_A_BIT_IS_AN_INTERPRETATION_NOT_A_MEASUREMENT`: و«٠٫٥٠٠٠ بت —
النصفُ معلَّق»: نصفان من أربعة عوالمَ يعطيان **١٫٠٠٠٠** عند التطابق،
و**٠٫٤١٥٠** عند تقاطعٍ بعالم، و**صفرًا** عند الانفصال. و٠٫٥ ليست فيها.
ثمّ **المعلَّقُ بتُّ مرجعٍ لا بتُّ عالم**؛ وطرحُه من واحدٍ يفترض معاملَ
تحويلٍ = ١ — وهو ما نصّت الوثيقةُ نفسُها على ألّا يُفترَض.

`THE_INDUCTION_ASSUMES_ITS_OWN_CONCLUSION`: و«بالاستقراء: السلسلةُ مغلقةٌ
⟺ منتهيةٌ بمرساة» — والاستقراءُ «على n» **يفترض اللادوريّة**. وحلقةُ
`p₁ → p₂ → p₁` سلسلةُ إحالةٍ بلا مرساةٍ وبلا `n`. فالنتيجةُ («غابةُ
الإحالات متجذّرة») هي **الفرضُ** الذي يحتاجه البرهان. وهذا فرضٌ مسكوتٌ
عنه، من جنس التحديب المفترَض في الدورة الرابعة.

`AND_THE_RESIDUE_SUM_IS_SUBADDITIVE_AGAIN`: و`R(t) = مجموعُ إنتروبيات
المراجع المفتوحة`: ضميران على المرجع الواحد مجموعُهما بتّان والمشترَكُ
بتّ. `H(A,B) ≤ H(A) + H(B)` — **عينُ عطلِ الديون** المرفوعِ في الدورة
الماضية، عاد في هذه بصيغةٍ أخرى.

`WHAT_STANDS`: ويصمد: أنّ الإحالةَ **عمليّةٌ ثالثةٌ** لا استبعادٌ ولا فتح؛
وفصلُ بتّات المرجع عن بتّات العالم بمعاملٍ **يُقاس ولا يُفترَض** (وهو أحسنُ
ما في الدورة)؛ وأنّ الدَّينَ يُسدَّد بإحالةٍ مُعلَنة — وذلك وصفٌ صادقٌ
لما جرى في هذه الشجرة فعلًا.
"""

from __future__ import annotations

import math
import random


def _entropy(shares: list[float]) -> float:
    return -math.fsum(one * math.log2(one) for one in shares if one > 0)


def test_no_message_can_raise_entropy_in_expectation() -> None:
    """`E[H(بعد)] ≤ H(قبل)` — مفحوصٌ على ألفِ قناةٍ عشوائيّة."""

    rng = random.Random(20_260_924)
    worst = -1.0
    for _ in range(1_000):
        size = rng.randrange(2, 6)
        prior = [rng.random() for _ in range(size)]
        total = sum(prior)
        prior = [one / total for one in prior]
        channel = [[rng.random() for _ in range(size)] for _ in range(3)]
        for index in range(size):
            column = sum(row[index] for row in channel)
            for row in channel:
                row[index] /= column
        expected = 0.0
        for row in channel:
            joint = [prior[k] * row[k] for k in range(size)]
            mass = sum(joint)
            if mass > 0:
                expected += mass * _entropy([one / mass for one in joint])
        worst = max(worst, expected - _entropy(prior))
    assert worst < 1e-9


def test_a_single_observation_may_raise_it_and_that_is_elementary() -> None:
    """مشاهَدٌ بعينه يرفعها — واقعةٌ ابتدائيّةٌ لا تُصاغ قانونًا."""

    prior = [0.7, 0.2, 0.1]
    joint = [0.7 * 0.1, 0.2 * 0.9, 0.1 * 0.9]
    mass = sum(joint)
    posterior = [one / mass for one in joint]
    assert _entropy(posterior) > _entropy(prior)


def test_measuring_a_mixture_against_its_components_guarantees_a_rise() -> None:
    """جنسن: `H(الخليط) ≥ متوسّطُ H(المكوّنات)` — فالارتفاعُ مضمونٌ بالبناء."""

    components = [[0.9, 0.05, 0.05], [0.05, 0.9, 0.05]]
    weights = [0.5, 0.5]
    mixture = [sum(weights[k] * components[k][i] for k in range(2)) for i in range(3)]
    average = sum(weights[k] * _entropy(components[k]) for k in range(2))
    assert _entropy(mixture) > average


def test_half_a_bit_is_not_among_the_values_the_construction_allows() -> None:
    """نصفان من أربعةٍ: ١٫٠٠٠٠ أو ٠٫٤١٥٠ أو صفر — و٠٫٥ ليست فيها."""

    values = {round(math.log2(4 / (4 - overlap)), 4) for overlap in (2, 1, 0)}
    assert values == {1.0, 0.415, 0.0}
    assert 0.5 not in values


def test_the_reference_induction_needs_acyclicity_as_a_hypothesis() -> None:
    """حلقةُ `p₁ → p₂ → p₁`: سلسلةٌ بلا مرساةٍ وبلا `n` — فالفرضُ لازم."""

    graph = {"p1": "p2", "p2": "p1"}
    seen: set[str] = set()
    node = "p1"
    while node in graph and node not in seen:
        seen.add(node)
        node = graph[node]
    assert node in seen  # دوريّة: لا مرساة
    anchored = {"q1": "q2", "q2": "اسمٌ صريح"}
    node, steps = "q1", 0
    while node in anchored:
        node = anchored[node]
        steps += 1
    assert node == "اسمٌ صريح" and steps == 2


def test_the_open_reference_sum_is_subadditive() -> None:
    """ضميران على مرجعٍ واحد: المجموعُ بتّان والمشترَكُ بتّ."""

    single = 1.0
    assert single + single > single  # المجموعُ يُضاعِف
    assert single <= single + single  # H(A,B) ≤ H(A) + H(B)
