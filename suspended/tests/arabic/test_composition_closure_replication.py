"""إعادةُ إنتاج سقوط الإغلاق: صفريٌّ يحفظ شرطَيه، واتّجاهٌ يُعاد ومقدارٌ يفترق.

يُثبِت هذا الاختبارُ ثمانيةَ أشياء: أنّ الصفريَّ يحفظ جدولَي الثنائيّات
تطابقًا، وأنّه يحفظ تمايزَ الجذور، وأنّ الإحصاءةَ تُفرِد التماثلَ عن التجانس،
وأنّ الإغلاقَ **يسقط** في سياستَي الإدراج كلتيهما، وأنّ تماثلَ C1C3 يُطابِق
المنشورَ مطابقةً قريبة، وأنّ التجانسَ يفترق عن المنشور مقدارًا، وأنّ الحكمَ
غيرُ محسومٍ لأنّ المصدرَ واحد، وأنّ صفريًّا لا يحفظ شرطًا يُرَدُّ عند الإنشاء.
"""

from __future__ import annotations

import random

import pytest

from alghanem.arabic.composition_closure_replication import (
    PUBLISHED_HOMOGENEITY_RATIO,
    PUBLISHED_IDENTITY_RATIOS,
    ClosureStatistic,
    ReplicationReading,
    bigram_tables,
    closure_statistic,
    derive_replication,
    resample_under_null,
)
from alghanem.arabic.slot_rights_algebra import (
    Certification,
    InclusionPolicy,
    SlotAlgebraError,
    read_roots,
)

_REPLICATES = 30


def test_the_null_preserves_both_bigram_tables_exactly() -> None:
    """تبديلُ طرفَي C₃ داخل طبقة C₂ لا يغيّر الجدولين، والمقابلةُ تطابقيّة."""

    roots, _dropped = read_roots(InclusionPolicy.WITH_DOUBLED)
    before = bigram_tables(roots)
    rng = random.Random(7)

    for _ in range(3):
        after = bigram_tables(resample_under_null(roots, rng))
        assert after == before


def test_the_null_preserves_root_distinctness() -> None:
    """كلُّ تبديلٍ يولّد مكرَّرًا يُرفَض، فالمُخرَجُ متمايزٌ كالمدخل."""

    roots, _dropped = read_roots(InclusionPolicy.WITH_DOUBLED)
    rng = random.Random(11)

    for _ in range(3):
        simulated = resample_under_null(roots, rng)
        assert len(simulated) == len(roots)
        assert len(set(simulated)) == len(simulated)


def test_the_statistic_separates_identity_from_homogeneity() -> None:
    """التجانسُ يستثني المتماثلين، فالعدّادان لا يتداخلان."""

    statistic = closure_statistic(("بتد", "ببب", "كتب"))

    assert statistic.identical == 1
    assert statistic.same_block >= 0

    with pytest.raises(SlotAlgebraError, match="غيرُ سالبين"):
        ClosureStatistic(same_block=-1, identical=0)


def test_the_closure_falls_under_both_policies() -> None:
    """الإغلاقُ يسقط في السياستين: النسبتان دون الواحد معًا."""

    for policy in (InclusionPolicy.TRILATERAL_ONLY, InclusionPolicy.WITH_DOUBLED):
        reading = derive_replication(policy, replicates=_REPLICATES)
        assert reading.closure_fails
        assert reading.same_block_ratio < 1.0
        assert reading.identity_ratio < 1.0


def test_the_identity_ratio_matches_the_published_figure_closely() -> None:
    """تماثلُ C1C3 عندي قريبٌ من المنشور، والمقارنةُ على المنشور لا عليه."""

    reading = derive_replication(
        InclusionPolicy.TRILATERAL_ONLY, replicates=_REPLICATES
    )

    assert PUBLISHED_IDENTITY_RATIOS == (0.14, 0.12)
    assert abs(reading.identity_ratio - PUBLISHED_IDENTITY_RATIOS[0]) < 0.03


def test_the_homogeneity_ratio_differs_from_the_published_figure() -> None:
    """التجانسُ أعلى عندي من المنشور، والفرقُ يُسجَّل ولا يُسوّى."""

    reading = derive_replication(InclusionPolicy.WITH_DOUBLED, replicates=_REPLICATES)

    assert PUBLISHED_HOMOGENEITY_RATIO == 0.48
    assert reading.same_block_ratio > PUBLISHED_HOMOGENEITY_RATIO
    assert reading.same_block_ratio < 1.0


def test_the_verdict_is_undetermined_over_one_source() -> None:
    """اتّفاقُ الاتّجاه ليس اتّفاقَ مصدرين، فالحكمُ غيرُ محسوم."""

    reading = derive_replication(InclusionPolicy.WITH_DOUBLED, replicates=_REPLICATES)

    assert reading.certification is Certification.UNDETERMINED
    assert reading.p_floor == pytest.approx(1 / (_REPLICATES + 1))


def test_a_null_that_breaks_a_guarantee_is_refused() -> None:
    """قراءةٌ تُعلِن سقوطَ حفظٍ تُرَدُّ عند الإنشاء، ولا تُقرأ نتيجةً."""

    observed = ClosureStatistic(same_block=1, identical=1)

    with pytest.raises(SlotAlgebraError, match="لم يحفظ الجدولين"):
        ReplicationReading(
            policy=InclusionPolicy.WITH_DOUBLED,
            roots=1,
            replicates=1,
            observed=observed,
            null_mean_same_block=1.0,
            null_mean_identical=1.0,
            p_floor=0.5,
            tables_preserved_every_replicate=False,
            distinctness_preserved_every_replicate=True,
            certification=Certification.UNDETERMINED,
        )
    with pytest.raises(SlotAlgebraError, match="جذرًا مكرَّرًا"):
        ReplicationReading(
            policy=InclusionPolicy.WITH_DOUBLED,
            roots=1,
            replicates=1,
            observed=observed,
            null_mean_same_block=1.0,
            null_mean_identical=1.0,
            p_floor=0.5,
            tables_preserved_every_replicate=True,
            distinctness_preserved_every_replicate=False,
            certification=Certification.UNDETERMINED,
        )
