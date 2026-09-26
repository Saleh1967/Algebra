"""أرقامُ ستيرلنغ وصيغتُه: تصحيحُ **البنية** وتصحيحُ **الكمّ**، مفصولين.

**ولمَ الوحدةُ**: الحزمةُ تحسب التباديلَ في `attainability` وتقسم الأصنافَ
في غيرها، **والمقداران أخوان لا واحد**:

- **صيغةُ ستيرلنغ** تُقارِب `n!` — فتصحّح **الكمّ** حين ينفجر العدد.
  **وههنا لا تُستعمَل تقريبًا**: تُستعمَل **حدّين مبرهَنين** (روبنز)
  يكتنفان `n!` من فوقُ ومن تحت، **فيُقال «بين كذا وكذا» لا «نحوَ كذا»**.
- **أرقامُ ستيرلنغ** تُحوِّل بين قاعدتين للتعداد — فتصحّح **البنية**:
  الأولى تعدّ التباديلَ بعدد دوراتها، والثانيةُ تعدّ **قسماتِ مجموعةٍ إلى
  كتل**. وهما **مصفوفتان متعاكستان**، فضربُهما يعطي المطابقة — **واختبارُ
  تصحيحٍ ذاتيٍّ لا يحتاج جدولًا مُودَعًا**.

`WHY_THE_SECOND_KIND_MATTERS_TO_A_GREEDY_LADDER`: وسلّمُ التصعيد يقسم
خاناتٍ إلى كتل. **فعددُ ما كان يمكن أن يبلغه** عند `k` كتلةً هو `S(n,k)`
بعينه، **وما زاره الجشعُ واحدٌ من ذلك**. فرقمُ ستيرلنغ الثاني **يُسعِّر
دعوى «الجشعُ غيرُ مبرهَن» عددًا** بدل أن تبقى قولًا.

`NOTHING_HERE_IS_IMPORTED`: كلُّ عددٍ يُبنى بقاعدة النمط من أصغرَ منه،
**ولا جدولَ مكتوبٌ ولا تابعٌ خارجيّ**.
"""

from __future__ import annotations

import math
from functools import cache
from typing import Final

TWO_PI: Final[float] = 2 * math.pi


class StirlingError(ValueError):
    """رُدَّ مدخلٌ خارجَ حدّ التعريف، أو حسابٌ نقض مطابقتَه."""


@cache
def cycles(whole: int, parts: int) -> int:
    """`c(n,k)` — التباديلُ التي لها `k` دورة (ستيرلنغ الأولى، غيرَ مُوقَّعة).

    `c(n,k) = c(n−1,k−1) + (n−1)·c(n−1,k)`: الرأسُ الجديدُ **دورةٌ وحدَه**،
    أو **يُزرَع داخلَ دورةٍ قائمة** في `n−1` موضعًا.
    """

    if whole < 0 or parts < 0:
        raise StirlingError(f"لا تعدادَ لسالب: ({whole}، {parts})")
    if whole == parts:
        return 1
    if parts == 0 or parts > whole:
        return 0
    return cycles(whole - 1, parts - 1) + (whole - 1) * cycles(whole - 1, parts)


@cache
def subsets(whole: int, parts: int) -> int:
    """`S(n,k)` — قسماتُ مجموعةٍ إلى `k` كتلةً غيرِ فارغة (ستيرلنغ الثانية).

    `S(n,k) = k·S(n−1,k) + S(n−1,k−1)`: العنصرُ الجديدُ **في صندوقٍ قائم**
    (وهي `k` وجهًا) أو **في صندوقٍ جديد**.
    """

    if whole < 0 or parts < 0:
        raise StirlingError(f"لا تعدادَ لسالب: ({whole}، {parts})")
    if whole == parts:
        return 1
    if parts == 0 or parts > whole:
        return 0
    return parts * subsets(whole - 1, parts) + subsets(whole - 1, parts - 1)


def bell(whole: int) -> int:
    """`B(n) = Σ S(n,k)` — كلُّ قسمات المجموعة، الواحدةُ منها والتامّة."""

    return sum(subsets(whole, one) for one in range(whole + 1))


def unsearched(cells: int) -> dict[int, int]:
    """قسماتُ `cells` خانةً إلى كتلتين فأكثر — **فضاءُ ما لم يُبحَث**.

    والجشعُ يزور منها **واحدةً عند كلّ درجة**، فلا يبلغ إلّا `cells − 1`
    قسمةً مهما طال. **فالنسبةُ تُسعِّر الدعوى ولا تُبقيها قولًا.**
    """

    return {one: subsets(cells, one) for one in range(2, cells + 1)}


def inversion_closes(whole: int) -> bool:
    """`Σ_k (−1)^(n−k) c(n,k) S(k,m) = δ(n,m)` — اختبارُ تصحيحٍ ذاتيّ.

    **فالمصفوفتان متعاكستان**، وضربُ إحداهما في الأخرى يُعيد المطابقة.
    **وإن لم تُعِدها فالتعدادُ الخامُ فيه خلل** — ولا يحتاج كشفُه جدولًا
    من خارج.
    """

    for low in range(whole + 1):
        found = sum(
            (-1) ** (whole - one) * cycles(whole, one) * subsets(one, low)
            for one in range(whole + 1)
        )
        if found != (1 if whole == low else 0):
            return False
    return True


def factorial_bounds(whole: int) -> tuple[float, float]:
    """حدّا روبنز لـ`log₂ n!` — **مبرهنان من الطرفين**، لا تقريبٌ واحد.

    `√(2πn)(n/e)ⁿ · e^(1/(12n+1)) < n! < √(2πn)(n/e)ⁿ · e^(1/(12n))`

    **فيُقال «بين كذا وكذا»** ولا يُقال «نحوَ كذا». وحدُّ التعريف `n ≥ 1`.
    """

    if whole < 1:
        raise StirlingError(f"حدّا روبنز لِما دون الواحد غيرُ معرَّفين: {whole}")
    stem = (
        math.log2(TWO_PI * whole) / 2
        + whole * math.log2(whole)
        - whole * math.log2(math.e)
    )
    return (
        stem + math.log2(math.e) / (12 * whole + 1),
        stem + math.log2(math.e) / (12 * whole),
    )


def gap_in_bits(counts: tuple[int, ...]) -> float:
    """فجوةُ ستيرلنغ: `n·H − log₂ التباديل المتمايزة` — وهي **غيرُ سالبة**.

    وهي الفرقُ بين **الكمّ** (عددُ التباديل) و**حدّه** (الإنتروبيا)، وقد
    قِيس في `ca75f300…` أنّها **تكبر بعدد الرموز**.
    """

    total = sum(counts)
    if total == 0:
        raise StirlingError("لا فجوةَ لكتلةٍ فارغة — والخلوُّ يُردّ لا يُصفَّر")
    height = -math.fsum(one * math.log2(one / total) for one in counts if one)
    exact = (
        math.lgamma(total + 1) - math.fsum(math.lgamma(one + 1) for one in counts)
    ) / math.log(2)
    return (height - exact) + 0  # وجمعُ الصحيح يردّ سالبَ الصفر صفرًا
