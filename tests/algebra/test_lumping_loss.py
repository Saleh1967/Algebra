"""الهويّةُ تُغلِق، والأمثلُ يُبلَغ في `3ⁿ`، **وdalّةُ الكتلة ليست submodular**.

**ما يحرسه**: أنّ `Σ_u w_u·KL(P_u‖P_c)` و`Σ_c W_c·H(P_c) − Σ_u w_u·H(P_u)`
**مقدارٌ واحد** — يُقابَلان على قسماتٍ كثيرةٍ لا على واحدة. وأنّ البرمجةَ
الديناميكيّةَ على الجزئيّات **تبلغ الأمثلَ يقينًا**: تُقابَل بتعدادٍ تامٍّ
لكلّ قسمات المجموعة عند `n` صغير، **فالحجّةُ عدٌّ لا ثقة**.

**والتصحيح**: الحاجزُ **`3ⁿ` لا `B(n)`**. وقد وُصِف قبلُ بأنّ تعدادَ
القسمات يمنع التحقّق، **وذلك وصفٌ خاطئٌ للحاجز** — والفرقُ يُفحَص عددًا
ههنا بـ`algebra.stirling.bell`.

**وأمّا الضمانُ للجشع بدعوى `submodular` فمردود**: يُطلَب النقضُ فيُوجَد،
**ومقدارُه يُسمّى بالنسبة إلى ضجيج الآلة** كي لا يُقرَأ نقضًا عائمًا. فمن
أراد للجشع ضمانًا فليأتِ به من طريقٍ آخر — **وهذا الطريقُ مقطوع**.
"""

from __future__ import annotations

import math
import random
from itertools import combinations

import pytest

from algebra.lumping_loss import (
    TOLERANCE,
    LumpingLossError,
    best_partition,
    block_cost,
    constant_term,
    entropy_of,
    greedy_partition,
    identity_drift,
    loss_by_blocks,
    loss_by_divergence,
    submodularity_violation,
)
from algebra.stirling import bell

WITNESSED = 200
NOISE = 2**-52


def _counts(many: int, wide: int, seed: int) -> list[list[int]]:
    stream = random.Random(seed)
    return [[stream.randint(1, 40) for _ in range(wide)] for _ in range(many)]


def _partitions(many: int) -> list[list[list[int]]]:
    """كلُّ قسمات المجموعة — تعدادٌ تامٌّ للمقابلة، لا للاستعمال."""

    if many == 1:
        return [[[0]]]
    found: list[list[list[int]]] = []
    for smaller in _partitions(many - 1):
        for index in range(len(smaller)):
            found.append(
                [
                    [*block, many - 1] if index == place else list(block)
                    for place, block in enumerate(smaller)
                ]
            )
        found.append([list(block) for block in smaller] + [[many - 1]])
    return found


def test_the_identity_closes_on_many_partitions_not_one() -> None:
    """الصيغتان مقدارٌ واحد — على مئتي قسمةٍ عشوائيّة، لا على واحدة."""

    counts = _counts(8, 4, seed=7)
    stream = random.Random(11)
    worst = 0.0
    for _ in range(WITNESSED):
        blocks = stream.randint(2, 5)
        labels = [stream.randrange(blocks) for _ in range(len(counts))]
        parts = [
            [one for one in range(len(counts)) if labels[one] == which]
            for which in range(blocks)
        ]
        parts = [one for one in parts if one]
        worst = max(worst, identity_drift(counts, parts))
    assert worst < 1e-9, worst
    assert worst / sum(sum(one) for one in counts) < NOISE * 1_000


def test_the_constant_term_does_not_depend_on_the_partition() -> None:
    """`Σ_u w_u·H(P_u)` ثابتٌ — وهو مدارُ الهويّة كلِّها."""

    counts = _counts(6, 3, seed=13)
    fixed = constant_term(counts)
    for parts in _partitions(6)[:40]:
        left = loss_by_divergence(counts, parts)
        right = loss_by_blocks(counts, parts)
        assert abs((right - left) - fixed) < 1e-9
    # والقسمةُ الأدقُّ خسارتُها صفرٌ، فالطرفان يتساويان بالثابت
    finest = [[one] for one in range(6)]
    assert loss_by_divergence(counts, finest) < 1e-9
    assert abs(loss_by_blocks(counts, finest) - fixed) < 1e-9


def test_the_dynamic_programme_reaches_the_optimum_by_full_count() -> None:
    """الأمثلُ المُدَّعى **يُقابَل بتعدادٍ تامٍّ** — فالحجّةُ عدٌّ لا ثقة."""

    for seed, many, wide in ((3, 6, 3), (5, 7, 4)):
        counts = _counts(many, wide, seed=seed)
        every = _partitions(many)
        for blocks in range(1, many + 1):
            here = [one for one in every if len(one) == blocks]
            lowest = min(loss_by_blocks(counts, one) for one in here)
            found, parts = best_partition(counts, blocks)
            assert abs(found - lowest) < 1e-9, (seed, blocks)
            assert len(parts) == blocks
            assert (
                abs(loss_by_blocks(counts, [list(one) for one in parts]) - found) < 1e-9
            )


def test_the_barrier_is_three_to_the_n_and_not_the_bell_number() -> None:
    """`3ⁿ` دون `B(n)` عند الأربعةَ عشرةَ — والفرقُ يُعَدّ لا يُوصَف."""

    assert 3**14 < bell(14)
    assert bell(14) // 3**14 >= 39
    assert 3**14 == 4_782_969
    assert bell(14) == 190_899_322
    # وعند ١١٢ يبقى ممتنعًا — والامتناعُ يُقال عددًا لا ظنًّا
    assert math.log10(3**112) > 53
    assert __doc__ is not None
    assert "**وذلك وصفٌ خاطئٌ للحاجز**" in " ".join(__doc__.split())


def test_the_greedy_never_beats_the_optimum_and_sometimes_ties_it() -> None:
    """الجشعُ لا ينزل دون الأمثل — وقد يطابقه، **ولا يُضمَن أنّه يطابقه**."""

    tied = 0
    tried = 0
    for seed in (7, 19, 23, 31):
        counts = _counts(8, 4, seed=seed)
        for blocks in (2, 3, 4, 6):
            exact, _ = best_partition(counts, blocks)
            rough, parts = greedy_partition(counts, blocks)
            assert rough >= exact - 1e-9, (seed, blocks, rough, exact)
            assert len(parts) == blocks
            tried += 1
            tied += abs(rough - exact) < 1e-9
    assert tried == 16
    assert tied >= 1  # يطابق أحيانًا
    assert __doc__ is not None
    assert "فالحجّةُ عدٌّ لا ثقة" in " ".join(__doc__.split())


def test_the_block_function_is_not_submodular_and_the_gap_dwarfs_the_noise() -> None:
    """**النقضُ موجودٌ ومقدارُه فوق الضجيج بأربعةَ عشرةَ رتبة** — فلا ضمان."""

    counts = _counts(8, 4, seed=7)
    where = submodularity_violation(counts)
    assert where is not None, "لا نقضَ — فالدعوى تحتاج فحصًا آخر"
    lowest = None
    for size in range(1, len(counts) - 1):
        for base in combinations(range(len(counts)), size):
            here = block_cost(counts, base)
            rest = [one for one in range(len(counts)) if one not in base]
            for first, second in combinations(rest, 2):
                gap = (
                    block_cost(counts, (*base, first))
                    + block_cost(counts, (*base, second))
                ) - (block_cost(counts, (*base, first, second)) + here)
                if lowest is None or gap < lowest:
                    lowest = gap
    assert lowest is not None and lowest < 0
    scale = max(block_cost(counts, (one,)) for one in range(len(counts)))
    assert abs(lowest) > scale * NOISE * 1e12, (lowest, scale)
    assert abs(lowest) > TOLERANCE * 1e12


def test_a_partition_that_is_not_a_partition_is_refused() -> None:
    """قسمةٌ تُكرِّر أو تُسقِط تُردّ — ولا تُحسَب خسارةٌ على ناقص."""

    counts = _counts(4, 3, seed=2)
    for bad in ([[0, 1], [1, 2, 3]], [[0, 1]], [[0, 1, 2, 3, 3]]):
        with pytest.raises(LumpingLossError):
            loss_by_blocks(counts, bad)
    with pytest.raises(LumpingLossError):
        best_partition(counts, 0)
    with pytest.raises(LumpingLossError):
        best_partition(counts, 5)
    with pytest.raises(LumpingLossError):
        block_cost(counts, [])
    with pytest.raises(LumpingLossError):
        loss_by_blocks([[1, 0], [0, 0]], [[0], [1]])
    with pytest.raises(LumpingLossError):
        loss_by_blocks([[1, -1]], [[0]])


def test_the_entropy_of_an_empty_row_needs_no_guard() -> None:
    """المرشِّحُ يُخلي المولِّدَ فيردُّ صفرًا — والبنيةُ تحرس لا سطرٌ يُكتَب."""

    assert entropy_of([0, 0, 0]) == 0
    assert entropy_of([5]) == 0
    assert abs(entropy_of([1, 1]) - 1) < 1e-12
    assert abs(entropy_of([1, 1, 1, 1]) - 2) < 1e-12
