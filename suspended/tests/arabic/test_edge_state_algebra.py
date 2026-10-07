"""جبرُ الحوافّ: ثلاثٌ لا رابعةَ لها، وأعدادٌ تُشتَقّ، ووقفٌ محجوبٌ لا مُقدَّر.

يُثبِت هذا الاختبارُ ثمانيةَ أشياء: أنّ الحوافَّ ثلاثٌ ولكلٍّ بوّابتُها، وأنّ
بوّابةً بلا بايتاتٍ منزلتُها «غيرُ محسوم»، وأنّ أعدادَ الوصل الثلاثةَ تُشتَقّ
فتطابق المنشور، وأنّ فضاءَ `CV-112` يُشتَقّ بالضرب، وأنّ الابتداءَ لا يُنقِص
عضوًا وصنفَ الإصلاح منفصلٌ عن الأساس، وأنّ بنيةً مخالفةً بلا إصلاحٍ مُسمًّى
تُرَدّ كما تُرَدُّ مستقيمةٌ بإصلاحٍ مذكور، وأنّ قسمةً متقاطعةً تُرَدّ، وأنّ
عددَ الوقف يرفع الحجبَ باسم `ق-4` ولا يُرجِع رقمًا.

**وموضعُ تشغيله**: نسخةٌ كاملةٌ من `Saleh1967/Alghanem` كما ينصّ
`src/alghanem/TRANSFER_NOTICE.md`؛ فـ`tests/arabic` ليست في `testpaths` ههنا.
"""

from __future__ import annotations

import pytest

from alghanem.arabic.decision_register import (
    DecisionRegisterError,
    blockers_of,
    pending_decisions,
)
from alghanem.arabic.edge_state_algebra import (
    CONSONANT_CARRIERS,
    EDGE_STATE_NAMED_RESIDUALS,
    FROZEN_GATES,
    INITIAL_REPAIR_CLASS,
    PUBLISHED_CV_CELLS,
    REAL_VOWELS,
    WAQF_BLOCKED_ITEM,
    Certification,
    Edge,
    EdgeStateError,
    InitialShape,
    Mark,
    OnsetPartition,
    OnsetStanding,
    derive_cv_cells,
    derive_onset_partition,
    derive_wasl_counts,
    gate_of,
    waqf_count,
)


def test_the_edges_are_three_and_each_carries_its_gate() -> None:
    """ثلاثُ حوافَّ، ولكلٍّ بوّابةٌ مُسمّاةٌ بمعرِّفها المُجمَّد."""

    assert len(Edge) == 3
    assert len(FROZEN_GATES) == 3
    assert gate_of(Edge.IBTIDA).identifier == "IBTIDA-SUKUN-EXCLUSION-AR-1"
    assert gate_of(Edge.WASL).identifier == "WASL-HAMZA-ELISION-AR-1"
    assert gate_of(Edge.WAQF).identifier == "WAQF-TANWEEN-CARRIER-AR-1"
    assert len(EDGE_STATE_NAMED_RESIDUALS) == 7


def test_a_gate_without_its_bytes_is_undetermined() -> None:
    """بايتاتُ البوّابات ليست ههنا، فمنزلتُها غيرُ محسومٍ بنصّ القاعدة."""

    for gate in FROZEN_GATES:
        assert not gate.bytes_present
        assert gate.certification is Certification.UNDETERMINED

    with pytest.raises(EdgeStateError, match="نصُّ البوّابة"):
        type(FROZEN_GATES[0])(
            edge=Edge.WASL, identifier="X-AR-1", statement="  ", bytes_present=False
        )


def test_the_wasl_counts_are_derived_and_match_what_was_published() -> None:
    """أعدادُ الوصل الثلاثةُ تُشتَقّ ضربًا فتطابق ٨٤ و٢٣٥٢ و٦٥٨٥٦."""

    counts = derive_wasl_counts()
    assert [count.derived for count in counts] == [84, 2_352, 65_856]
    assert all(count.matches_published for count in counts)
    assert all(count.edge is Edge.WASL for count in counts)
    assert counts[0].derived == CONSONANT_CARRIERS * len(REAL_VOWELS)


def test_the_cv_space_is_derived_and_the_base_is_it_without_the_sukun() -> None:
    """١١٢ = حاملٌ × علامة، و٨٤ هو هو بعد إخراج عمود السكون."""

    assert derive_cv_cells() == PUBLISHED_CV_CELLS
    assert len(REAL_VOWELS) == len(Mark) - 1
    assert derive_cv_cells() - CONSONANT_CARRIERS == derive_wasl_counts()[0].derived


def test_the_onset_gate_partitions_and_subtracts_nothing() -> None:
    """صنفُ الإصلاح منفصلٌ عن الأساس، والأساسُ باقٍ بلا نقصان."""

    partition = derive_onset_partition()
    assert partition.overlap_with_base == 0
    assert partition.base_is_unchanged
    assert partition.base_after == 84
    assert partition.repair_members == len(INITIAL_REPAIR_CLASS) == 3
    for shape in INITIAL_REPAIR_CLASS:
        assert shape.standing is OnsetStanding.NEEDS_INITIAL_REPAIR
        assert shape.repair.strip()


def test_a_violating_shape_without_a_named_repair_is_refused() -> None:
    """مخالفةٌ بلا إصلاحٍ مُسمًّى تُرَدّ، ومستقيمةٌ بإصلاحٍ مذكورٍ تُرَدّ كذلك."""

    with pytest.raises(EdgeStateError, match="بلا إصلاحٍ مُسمًّى"):
        InitialShape(label="مخالفة", example="اُنْصُرْ", first_mark=Mark.SUKUN)

    with pytest.raises(EdgeStateError, match="بإصلاحٍ مذكور"):
        InitialShape(
            label="مستقيمة",
            example="نَصَرَ",
            first_mark=Mark.FATHA,
            repair="همزةُ وصل",
        )

    assert (
        InitialShape(label="مستقيمة", example="نَصَرَ", first_mark=Mark.FATHA).standing
        is OnsetStanding.WELL_FORMED_ONSET
    )


def test_an_overlapping_partition_is_refused() -> None:
    """قسمةٌ يتقاطع فيها الإصلاحُ مع الأساس تُرَدّ ولا تُقرَّب."""

    with pytest.raises(EdgeStateError, match="يتقاطع مع الأساس"):
        OnsetPartition(
            base_before=84, base_after=83, repair_members=3, overlap_with_base=1
        )

    with pytest.raises(EdgeStateError, match="صنفُ إصلاحٍ فارغ"):
        OnsetPartition(
            base_before=84, base_after=84, repair_members=0, overlap_with_base=0
        )


def test_the_waqf_count_is_blocked_by_a_pending_decision() -> None:
    """عددُ الوقف يرفع الحجبَ باسم ق-4، ولا يُرجِع رقمًا تقديريًّا."""

    blockers = blockers_of(WAQF_BLOCKED_ITEM)
    assert [decision.identifier for decision in blockers] == ["ق-4 حركةُ الوقف"]
    assert blockers[0] in pending_decisions()
    assert len(blockers[0].branches) == 4

    with pytest.raises(DecisionRegisterError, match="ق-4"):
        waqf_count()
