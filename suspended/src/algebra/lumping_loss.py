"""خسارةُ التكتيل **مجموعُ دالّةِ كتلةٍ** — فالأمثلُ يُبلَغ في `3ⁿ` لا `B(n)`.

**الهويّةُ المبرهنة**، وهي أصلُ كلّ ما بعدها:

    Σ_u w_u·KL(P_u ‖ P_c(u))  =  Σ_c W_c·H(P_c)  −  Σ_u w_u·H(P_u)

**وبرهانُها سطران**: `KL(P_u‖P_c) = −H(P_u) − Σ_s P_u(s)·log P_c(s)`؛
فإذا جُمِع الحدُّ الثاني على كتلةٍ صار
`Σ_s log P_c(s) · Σ_{u∈c} w_u P_u(s) = Σ_s log P_c(s) · W_c·P_c(s)`
وهو `−W_c·H(P_c)`. **والطرفُ الثاني لا يتعلّق بالقسمة ألبتّة.**

`AND_THE_CONSEQUENCE_IS_A_SMALLER_BARRIER_NOT_A_SMALLER_PROBLEM`: فمتى
كانت الدالّةُ **مجموعَ دالّةٍ على الكتل** جاز بلوغُ الأمثل ببرمجةٍ
ديناميكيّةٍ على المجموعات الجزئيّة: `O(k·3ⁿ)`. **والحاجزُ `3ⁿ` لا
`B(n)`** — وذلك تصحيحٌ لوصفٍ سابق. عند `n = 14`: `B(14)` مئةٌ وتسعون
مليونًا، و`3¹⁴` أربعةُ ملايينٍ وثمانُ مئةِ ألفٍ تقريبًا. **وعند `n = 112`
يبقى ممتنعًا**، لكنّ المسألةَ انتقلت من «لا يُعرَف» إلى **«يُعرَف تحت
عتبةٍ محسوبة»**.

`AND_THE_WEIGHTS_ARE_COUNTS_NOT_FLOATS`: الأوزانُ والتوزيعاتُ تُمرَّر
**أعدادًا صحيحةً** (عدّاداتٍ)، فلا يدخل الحسابَ عائمٌ إلّا عند
اللوغاريتم. **وما يُجمَع يُجمَع بـ`math.fsum`** لا بجمعٍ متسلسل.

`AND_NOTHING_HERE_IS_A_CLAIM_ABOUT_ANY_CORPUS`: هذه رياضيّاتٌ تامّةٌ على
أيّ مُدخَل، **وليست دعوًى عن مدوّنةٍ ولا عن لغة**.
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from itertools import combinations
from typing import Final

TOLERANCE: Final[float] = 1e-12
"""تسامحُ مقارنةٍ بين عائمين — لا مقدارٌ يدخل حسابًا."""


class LumpingLossError(ValueError):
    """رُدَّ مُدخَلٌ لا يحمل شكلَ المسألة."""


def _check(counts: Sequence[Sequence[int]]) -> None:
    if not counts:
        raise LumpingLossError("لا وحداتَ تُكتَّل.")
    width = len(counts[0])
    if width == 0:
        raise LumpingLossError("وحدةٌ بلا خانات.")
    for row in counts:
        if len(row) != width:
            raise LumpingLossError("صفوفٌ مختلفةُ العرض.")
        if any(one < 0 for one in row):
            raise LumpingLossError("عدّادٌ سالب.")
        if sum(row) == 0:
            raise LumpingLossError("وحدةٌ بلا وقوعات.")


def entropy_of(row: Sequence[int]) -> float:
    """`H` لصفّ عدّاداتٍ — والقسمةُ عند اللوغاريتم وحدَه.

    **ولا حاجةَ إلى حرَسٍ للصفر**: المرشِّحُ `if one` يُخلي المولِّدَ
    فيردُّ `fsum` صفرًا **بلا قسمةٍ على صفر** — فالبنيةُ تحرس لا سطرٌ
    يُكتَب.
    """

    whole = sum(row)
    return -math.fsum((one / whole) * math.log2(one / whole) for one in row if one)


def block_cost(counts: Sequence[Sequence[int]], block: Sequence[int]) -> float:
    """`W_c·H(P_c)` لكتلةٍ — **دالّةُ مجموعةٍ لا تتعلّق بسائر الكتل**."""

    if not block:
        raise LumpingLossError("كتلةٌ خالية.")
    merged = [0] * len(counts[0])
    for one in block:
        for index, value in enumerate(counts[one]):
            merged[index] += value
    return sum(merged) * entropy_of(merged)


def loss_by_blocks(
    counts: Sequence[Sequence[int]], partition: Sequence[Sequence[int]]
) -> float:
    """`Σ_c W_c·H(P_c)` — الطرفُ الذي يتعلّق بالقسمة، بلا تطبيعٍ."""

    _check(counts)
    seen = sorted(one for block in partition for one in block)
    if seen != list(range(len(counts))):
        raise LumpingLossError("القسمةُ ليست قسمةً تامّةً بلا تكرار.")
    return math.fsum(block_cost(counts, block) for block in partition)


def loss_by_divergence(
    counts: Sequence[Sequence[int]], partition: Sequence[Sequence[int]]
) -> float:
    """`Σ_u w_u·KL(P_u‖P_c)` — محسوبةً تعريفًا، لتُقابَل بالصيغة الأخرى."""

    _check(counts)

    def _block(block: Sequence[int]) -> float:
        merged = [0] * len(counts[0])
        for one in block:
            for index, value in enumerate(counts[one]):
                merged[index] += value
        weight = sum(merged)
        return math.fsum(
            value * math.log2((value / sum(counts[one])) / (merged[index] / weight))
            for one in block
            for index, value in enumerate(counts[one])
            if value
        )

    return math.fsum(_block(block) for block in partition)


def constant_term(counts: Sequence[Sequence[int]]) -> float:
    """`Σ_u w_u·H(P_u)` — **ثابتٌ لا يتعلّق بالقسمة**، وهو مدارُ الهويّة."""

    _check(counts)
    return math.fsum(sum(row) * entropy_of(row) for row in counts)


def identity_drift(
    counts: Sequence[Sequence[int]], partition: Sequence[Sequence[int]]
) -> float:
    """|الصيغتان مطروحتان| — وصفرُها برهانٌ عدديٌّ على الهويّة."""

    left = loss_by_divergence(counts, partition)
    right = loss_by_blocks(counts, partition) - constant_term(counts)
    return abs(left - right)


def _subsets(many: int) -> list[int]:
    return list(range(1, 1 << many))


def best_partition(
    counts: Sequence[Sequence[int]], blocks: int
) -> tuple[float, tuple[tuple[int, ...], ...]]:
    """الأمثلُ **يقينًا** في `O(k·3ⁿ)` — برمجةٌ ديناميكيّةٌ على الجزئيّات.

    والعائدُ `(Σ_c W_c·H(P_c)، القسمة)`. **ولا تعدادَ لـ`B(n)`**: يُمَرّ
    على كلّ مجموعةٍ جزئيّةٍ وعلى جزئيّاتها، وذلك `3ⁿ` لا أكثر.
    """

    _check(counts)
    many = len(counts)
    if not 1 <= blocks <= many:
        raise LumpingLossError(f"عددُ الكتل بين واحدٍ و{many}.")
    cost: dict[int, float] = {}
    for mask in _subsets(many):
        cost[mask] = block_cost(counts, [one for one in range(many) if mask >> one & 1])
    whole = (1 << many) - 1
    best: list[dict[int, float]] = [{} for _ in range(blocks + 1)]
    came: list[dict[int, int]] = [{} for _ in range(blocks + 1)]
    best[1] = dict(cost)
    for depth in range(2, blocks + 1):
        for mask in _subsets(many):
            lowest: float | None = None
            chosen = 0
            piece = mask
            while piece:
                rest = mask ^ piece
                if rest and rest in best[depth - 1]:
                    here = cost[piece] + best[depth - 1][rest]
                    if lowest is None or here < lowest:
                        lowest, chosen = here, piece
                piece = (piece - 1) & mask
            if lowest is not None:
                best[depth][mask] = lowest
                came[depth][mask] = chosen
    if whole not in best[blocks]:
        raise LumpingLossError("لا قسمةَ بهذا العدد من الكتل.")
    found: list[tuple[int, ...]] = []
    mask, depth = whole, blocks
    while depth > 1:
        piece = came[depth][mask]
        found.append(tuple(one for one in range(many) if piece >> one & 1))
        mask ^= piece
        depth -= 1
    found.append(tuple(one for one in range(many) if mask >> one & 1))
    return best[blocks][whole], tuple(sorted(found))


def greedy_partition(
    counts: Sequence[Sequence[int]], blocks: int
) -> tuple[float, tuple[tuple[int, ...], ...]]:
    """دمجٌ جشعٌ من أسفل: أرخصُ زوجٍ في كلّ خطوة — **وليس مبرهَنًا**."""

    _check(counts)
    many = len(counts)
    if not 1 <= blocks <= many:
        raise LumpingLossError(f"عددُ الكتل بين واحدٍ و{many}.")
    parts: list[tuple[int, ...]] = [(one,) for one in range(many)]
    while len(parts) > blocks:
        lowest: float | None = None
        pair = (0, 1)
        for first, second in combinations(range(len(parts)), 2):
            joined = block_cost(counts, parts[first] + parts[second])
            here = (
                joined
                - block_cost(counts, parts[first])
                - block_cost(counts, parts[second])
            )
            if lowest is None or here < lowest:
                lowest, pair = here, (first, second)
        first, second = pair
        merged = tuple(sorted(parts[first] + parts[second]))
        parts = [one for index, one in enumerate(parts) if index not in (first, second)]
        parts.append(merged)
    return loss_by_blocks(counts, parts), tuple(sorted(parts))


def submodularity_violation(
    counts: Sequence[Sequence[int]],
) -> tuple[int, int, int] | None:
    """أوّلُ نقضٍ لـ`f(S∪{a})+f(S∪{b}) ≥ f(S∪{a,b})+f(S)` — أو `None`.

    **والنقضُ يُطلَب لا يُفترَض غيابُه**: من ادّعى للجشع ضمانًا بدعوى
    `submodular` فعليه أن يأتي بها، **وهذا يفحصها على المُدخَل نفسِه**.
    """

    _check(counts)
    many = len(counts)
    for size in range(1, many - 1):
        for base in combinations(range(many), size):
            rest = [one for one in range(many) if one not in base]
            here = block_cost(counts, base)
            for first, second in combinations(rest, 2):
                one = block_cost(counts, (*base, first))
                two = block_cost(counts, (*base, second))
                both = block_cost(counts, (*base, first, second))
                if one + two < both + here - TOLERANCE:
                    return (len(base), first, second)
    return None
