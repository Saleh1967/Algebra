"""إعادةُ إنتاج سقوطِ إغلاق التركيب على المقاييس، بنموذجٍ صفريٍّ يحفظ شرطَيه.

**ما تفعله هذه الوحدة**: تُشغّل الاختبارَ الذي أعلن صاحبُ الجبر سقوطَه —
«الجذرُ الثلاثيُّ ليس تركيبًا للرابطتين المتجاورتين» — على المصدر الوحيد الذي
بايتاتُه في هذه الشجرة، بنموذجٍ صفريٍّ **يثبّت جدولَي (C₁,C₂) و(C₂,C₃)
ويحفظ تمايزَ الجذور معًا**. والحفظان **مفحوصان في كلّ تكرار**، لا مفترَضان.

`THE_NULL_MUST_PRESERVE_BOTH_TABLES_AND_DISTINCTNESS`: النموذجُ الذي يبدّل
الأعمدةَ مستقلًّا يُفسِد الجدولين ويولّد جذورًا مكرَّرة — وذلك عينُ ما نقده
صاحبُ الجبر في مبرهنته الثانية. والنموذجُ ههنا سلسلةُ تبادلٍ **داخل طبقة
`C₂`**: تبديلُ طرفَي `C₃` بين جذرين لهما الوسطُ نفسُه يُبقي الجدولين كما هما
بحكم البناء، ويُرفَض كلُّ تبديلٍ يولّد زوجًا مكرَّرًا. فالشرطان محفوظان معًا،
وكلٌّ منهما يُتحقَّق منه بالمقابلة في كلّ تكرار.

`THE_REPLICATION_AGREES_IN_DIRECTION_AND_DIFFERS_IN_MAGNITUDE`: والنتيجةُ
تُعيد إنتاج الاتّجاه: اجتماعُ `C₁` و`C₃` من كتلةٍ واحدةٍ **دون** ما يولّده
الصفريّ، وتماثلُهما دونه أيضًا. وتماثلُ `C₁C₃` يُطابِق المنشورَ مطابقةً قريبة،
أمّا التجانسُ فأعلى عندي منه في المنشور؛ والفرقُ يُسجَّل ولا يُسوّى.

`ONE_SOURCE_YIELDS_UNDETERMINED_NOT_CERTIFIED`: والمصدرُ واحد، فالحكمُ **غيرُ
محسوم** بنصّ قاعدة التصديق، ولو اتّفق اتّجاهُه مع المنشور. فاتّفاقُ اتّجاهٍ
ليس اتّفاقَ مصدرين.

`THE_PERMUTATION_FLOOR_IS_A_FLOOR_NOT_A_VALUE`: القيمةُ المُخرَجة حدٌّ أدنى
`1/(B+1)`، لا قيمةً مقيسة.

`THIS_IS_REGISTRATION_NOT_AUTHORITY`: لا ولادةَ هنا، ولا حكمَ ولادة، ولا
تجميدَ `E0`، ولا استيرادَ من `kernel/`.
"""

from __future__ import annotations

import random
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Final

from .slgae_deposit import BORN_BLOCKS
from .slot_rights_algebra import (
    Certification,
    InclusionPolicy,
    SlotAlgebraError,
    permutation_floor,
    read_roots,
)

__all__ = [
    "CLOSURE_REPLICATION_NAMED_RESIDUALS",
    "ONE_SOURCE_YIELDS_UNDETERMINED_NOTE",
    "PUBLISHED_HOMOGENEITY_RATIO",
    "PUBLISHED_IDENTITY_RATIOS",
    "THE_NULL_MUST_PRESERVE_BOTH_NOTE",
    "THE_REPLICATION_DIFFERS_IN_MAGNITUDE_NOTE",
    "ClosureStatistic",
    "ReplicationReading",
    "bigram_tables",
    "closure_statistic",
    "derive_replication",
    "resample_under_null",
]

PUBLISHED_HOMOGENEITY_RATIO: Final[float] = 0.48
"""ما نُشر لاجتماع `C₁` و`C₃` من كتلةٍ واحدة، منسوبًا لا مُعادَ اشتقاقه هنا."""

PUBLISHED_IDENTITY_RATIOS: Final[tuple[float, float]] = (0.14, 0.12)
"""ما نُشر لتماثل `C₁C₃` في المصدرين، منسوبًا لا مُعادَ اشتقاقه هنا."""


def bigram_tables(
    triples: tuple[str, ...],
) -> tuple[Counter[tuple[str, str]], Counter[tuple[str, str]]]:
    """جدولا `(C₁,C₂)` و`(C₂,C₃)`؛ وهما ما يجب أن يحفظه الصفريّ."""

    if not triples:
        raise SlotAlgebraError("لا جذورَ، فلا جدولَين.")
    return (
        Counter((item[0], item[1]) for item in triples),
        Counter((item[1], item[2]) for item in triples),
    )


@dataclass(frozen=True, slots=True)
class ClosureStatistic:
    """إحصاءةُ الإغلاق: اجتماعُ الكتلة الواحدة، وتماثلُ الطرفين."""

    same_block: int
    identical: int

    def __post_init__(self) -> None:
        if self.same_block < 0 or self.identical < 0:
            raise SlotAlgebraError("العدّادان غيرُ سالبين.")


def closure_statistic(triples: tuple[str, ...]) -> ClosureStatistic:
    """احسب الإحصاءةَ على الطرفين `C₁` و`C₃`، مع إفراد التماثل عن الكتلة."""

    block_of = {char: name for name, chars in BORN_BLOCKS for char in chars}
    same = sum(
        1
        for item in triples
        if item[0] != item[2]
        and block_of.get(item[0]) is not None
        and block_of.get(item[0]) == block_of.get(item[2])
    )
    return ClosureStatistic(
        same_block=same,
        identical=sum(1 for item in triples if item[0] == item[2]),
    )


def resample_under_null(
    triples: tuple[str, ...], rng: random.Random, sweeps: int = 4
) -> tuple[str, ...]:
    """أعِد التعيينَ تحت الصفريّ: تبديلٌ داخل طبقة `C₂` برفضِ المكرَّر.

    ويُبقي البناءُ جدولَي الثنائيّات كما هما: تبديلُ طرفَي `C₃` بين جذرين
    لهما الوسطُ نفسُه لا يغيّر `(C₁,C₂)` ولا كثرةَ أزواج `(C₂,C₃)`. وكلُّ
    تبديلٍ يولّد زوجًا مكرَّرًا **يُرفَض**، فتمايزُ الجذور محفوظ.
    """

    if sweeps < 1:
        raise SlotAlgebraError("عددُ الجولات موجب.")
    strata: dict[str, list[list[str]]] = defaultdict(list)
    for item in triples:
        strata[item[1]].append([item[0], item[2]])
    for pairs in strata.values():
        size = len(pairs)
        if size < 2:
            continue
        used = {(first, second) for first, second in pairs}
        for _ in range(sweeps * size):
            one, two = rng.randrange(size), rng.randrange(size)
            if one == two:
                continue
            left, right = pairs[one], pairs[two]
            if left[1] == right[1]:
                continue
            fresh_one, fresh_two = (left[0], right[1]), (right[0], left[1])
            if fresh_one in used or fresh_two in used:
                continue
            used.discard((left[0], left[1]))
            used.discard((right[0], right[1]))
            used.add(fresh_one)
            used.add(fresh_two)
            left[1], right[1] = right[1], left[1]
    return tuple(
        f"{first}{middle}{second}"
        for middle, pairs in strata.items()
        for first, second in pairs
    )


@dataclass(frozen=True, slots=True)
class ReplicationReading:
    """حصادُ الإعادة: المرصودُ، ومتوسّطُ الصفريّ، والحدُّ الأدنى للقيمة."""

    policy: InclusionPolicy
    roots: int
    replicates: int
    observed: ClosureStatistic
    null_mean_same_block: float
    null_mean_identical: float
    p_floor: float
    tables_preserved_every_replicate: bool
    distinctness_preserved_every_replicate: bool
    certification: Certification

    def __post_init__(self) -> None:
        if not self.tables_preserved_every_replicate:
            raise SlotAlgebraError(
                "الصفريُّ لم يحفظ الجدولين في كلّ تكرار؛ ونموذجٌ يُفسِدهما "
                "يقيس فسادَه لا فرضيّةً."
            )
        if not self.distinctness_preserved_every_replicate:
            raise SlotAlgebraError(
                "الصفريُّ ولّد جذرًا مكرَّرًا؛ ونموذجٌ لا يحفظ وحدةَ التحليل "
                "لا يصلح صفرًا لمعجمِ أنواع."
            )
        if self.certification is Certification.CERTIFIED:
            raise SlotAlgebraError(
                "لا تصديقَ عن مصدرٍ واحد، ولو اتّفق الاتّجاهُ مع المنشور."
            )

    @property
    def same_block_ratio(self) -> float:
        """`O/E` للكتلة الواحدة، بمتوسّط الصفريّ مقامًا لا بالهوامش."""

        return self.observed.same_block / self.null_mean_same_block

    @property
    def identity_ratio(self) -> float:
        """`O/E` للتماثل، بمتوسّط الصفريّ مقامًا."""

        return self.observed.identical / self.null_mean_identical

    @property
    def closure_fails(self) -> bool:
        """أيسقط إغلاقُ التركيب؟ مُشتَقٌّ من النسبتين لا مكتوبٌ في حقل."""

        return self.same_block_ratio < 1.0 and self.identity_ratio < 1.0


def derive_replication(
    policy: InclusionPolicy = InclusionPolicy.WITH_DOUBLED,
    replicates: int = 500,
    seed: int = 20260922,
    root: Path | None = None,
) -> ReplicationReading:
    """شغِّل الإعادةَ، وتحقّقْ من حفظَي الصفريّ في **كلّ** تكرار لا في واحد."""

    if replicates < 1:
        raise SlotAlgebraError("عددُ التكرارات موجب.")
    triples, _dropped = read_roots(policy, root)
    if not triples:
        raise SlotAlgebraError("لا جذورَ في هذه السياسة.")
    observed = closure_statistic(triples)
    first, second = bigram_tables(triples)
    rng = random.Random(seed)
    total_same = 0
    total_identical = 0
    tables_ok = True
    distinct_ok = True
    for _ in range(replicates):
        simulated = resample_under_null(triples, rng)
        if bigram_tables(simulated) != (first, second):
            tables_ok = False
        if len(set(simulated)) != len(simulated):
            distinct_ok = False
        statistic = closure_statistic(simulated)
        total_same += statistic.same_block
        total_identical += statistic.identical
    return ReplicationReading(
        policy=policy,
        roots=len(triples),
        replicates=replicates,
        observed=observed,
        null_mean_same_block=total_same / replicates,
        null_mean_identical=total_identical / replicates,
        p_floor=permutation_floor(replicates),
        tables_preserved_every_replicate=tables_ok,
        distinctness_preserved_every_replicate=distinct_ok,
        certification=Certification.UNDETERMINED,
    )


THE_NULL_MUST_PRESERVE_BOTH_NOTE: Final[str] = (
    "TheNullMustPreserveBothTablesAndDistinctness: تبديلُ الأعمدة مستقلًّا "
    "يُفسِد الجدولين ويولّد مكرَّرًا؛ والصفريُّ ههنا تبادلٌ داخل طبقة C₂ "
    "برفضِ المكرَّر، والحفظان مفحوصان في كلّ تكرار لا مفترَضان"
)

THE_REPLICATION_DIFFERS_IN_MAGNITUDE_NOTE: Final[str] = (
    "TheReplicationAgreesInDirectionAndDiffersInMagnitude: الاتّجاهُ يُعاد "
    "إنتاجُه، وتماثلُ C₁C₃ يُطابِق المنشورَ مطابقةً قريبة، والتجانسُ أعلى "
    "ههنا منه في المنشور؛ والفرقُ يُسجَّل ولا يُسوّى"
)

ONE_SOURCE_YIELDS_UNDETERMINED_NOTE: Final[str] = (
    "OneSourceYieldsUndeterminedNotCertified: اتّفاقُ اتّجاهٍ ليس اتّفاقَ "
    "مصدرين؛ فالحكمُ غيرُ محسومٍ ولو وافق المنشور"
)

CLOSURE_REPLICATION_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    THE_NULL_MUST_PRESERVE_BOTH_NOTE,
    THE_REPLICATION_DIFFERS_IN_MAGNITUDE_NOTE,
    ONE_SOURCE_YIELDS_UNDETERMINED_NOTE,
)
"""البواقي المُسمّاةُ لهذه الوحدة، مرتّبةً كما تُرتَّب في بقيّة الطبقة."""
