"""جبرُ الحقوق: ثلاثُ طبقاتٍ، ومبرهنتان مفحوصتان، وسياسةٌ تقلب حكمًا.

يُثبِت هذا الاختبارُ عشرةَ أشياء: أنّ منازلَ الحقّ ثلاثٌ ولا «ممنوع» فيها،
وأنّ الخلايا الأربعَ والثمانين مشهودةٌ في السياسات الثلاث بعد الطيّ المُودَع،
وأنّ المُسقَطَ لحرفٍ غيرِ مرقَّمٍ معدودٌ لا مطويٌّ صمتًا، وأنّ مبرهنة ح١
رتيبةٌ بالتشغيل، وأنّ طرفَي التركيب متطابقان وأنّ التطابقَ مع `P₁₂₃` مكافئٌ
لانعدام المعلومة الشرطيّة، وأنّ تبديلَ الأعمدة مستقلًّا يولّد مكرَّرًا فلا
يحفظ وحدةَ التحليل، وأنّ خليّةَ التماثل مفرَدةٌ عن خليّة التجانس، وأنّ حكمَ
`C2C3` **ينقلب** بسياسة الإدراج وحدَها، وأنّ وسمَ التصديق يُرَدُّ عن مصدرٍ
واحد، وأنّ حدَّ التباديل حدٌّ لا قيمة.
"""

from __future__ import annotations

import pytest

from alghanem.arabic.maqayis_root_table_deposit import root_table_digest
from alghanem.arabic.slot_rights_algebra import (
    PERMUTATIONS,
    RANKED_LETTERS,
    SLOTS,
    Certification,
    InclusionPolicy,
    RelationType,
    RightsCensus,
    RightStanding,
    SlotAlgebraError,
    compositions_are_identical,
    derive_class_cells,
    derive_identity_cells,
    derive_policy_sensitivity,
    derive_rights_census,
    duplicates_under_column_permutation,
    monotonicity_holds,
    permutation_floor,
    read_roots,
    triple_equals_composition_iff_cmi_vanishes,
)


def test_the_standings_are_three_and_none_is_forbidden() -> None:
    """ثلاثُ منازلَ ولا «ممنوع»؛ فالغيابُ وحدَه لا يُثبِت منعًا."""

    assert len(RightStanding) == 3
    assert "FORBIDDEN" not in RightStanding.__members__
    assert {member.name for member in RightStanding} == {
        "ATTESTED",
        "PREVENTION_CANDIDATE",
        "UNDETERMINED",
    }


def test_all_eighty_four_cells_are_attested_under_every_policy() -> None:
    """الخلايا 28×3 مشهودةٌ كلُّها، ولا مرشَّحَ للمنع، في السياسات الثلاث."""

    for policy in InclusionPolicy:
        census = derive_rights_census(policy)
        assert census.cells == len(RANKED_LETTERS) * len(SLOTS) == 84
        assert census.attested == 84
        assert census.prevention_candidates == ()
        assert census.source_digest == root_table_digest()


def test_the_dropped_roots_are_counted_not_folded_silently() -> None:
    """المُسقَطُ لحرفٍ غيرِ مرقَّمٍ — والألفُ منه — معدودٌ في كلّ قراءة."""

    for policy in InclusionPolicy:
        roots, dropped = read_roots(policy)
        assert roots
        assert dropped > 0
        assert derive_rights_census(policy).dropped_for_unranked == dropped


def test_attestation_is_monotone() -> None:
    """مبرهنة ح١ بالتشغيل: المشهودُ على نصف الجذور مشهودٌ على كلّها."""

    assert monotonicity_holds()
    assert monotonicity_holds(InclusionPolicy.TRILATERAL_ONLY)


def test_the_two_compositions_are_identical() -> None:
    """مبرهنة ت١، الشطرُ الأوّل: الطرفان متساويان تطابقًا لا تقريبًا."""

    assert compositions_are_identical()

    with pytest.raises(SlotAlgebraError, match="عددُ المحاولات موجب"):
        compositions_are_identical(trials=0)


def test_the_triple_matches_the_composition_iff_the_cmi_vanishes() -> None:
    """مبرهنة ت١، الشطرُ الثاني: المكافأةُ في الاتّجاهين مفحوصةٌ عدديًّا."""

    assert triple_equals_composition_iff_cmi_vanishes()


def test_an_independent_column_permutation_generates_duplicates() -> None:
    """شطرُ ت٢ المفحوص: النموذجُ يولّد مكرَّرًا، فلا يحفظ وحدةَ التحليل."""

    duplicates = duplicates_under_column_permutation()

    assert duplicates > 0


def test_the_identity_cell_is_separated_from_the_class_cell() -> None:
    """ثلاثُ خلايا تماثلٍ وثلاثُ خلايا تجانس، ولا تخالط بينهما."""

    identity = derive_identity_cells(InclusionPolicy.WITH_DOUBLED)
    classes = derive_class_cells(InclusionPolicy.WITH_DOUBLED)

    assert len(identity) == len(classes) == len(RelationType) == 3
    assert all(cell.is_identity_cell for cell in identity)
    assert not any(cell.is_identity_cell for cell in classes)
    assert all(cell.is_suppressed for cell in classes)
    doubled_identity = next(
        cell for cell in identity if cell.relation is RelationType.C2C3
    )
    doubled_class = next(cell for cell in classes if cell.relation is RelationType.C2C3)
    assert not doubled_identity.is_suppressed
    assert doubled_class.is_suppressed


def test_the_inclusion_policy_flips_one_verdict() -> None:
    """حكمُ `C2C3` ينقلب بإدراج المضاعف وحدَه، والآخران لا ينقلبان."""

    sensitivity = {item.relation: item for item in derive_policy_sensitivity()}

    flipping = [item for item in sensitivity.values() if item.sign_flips]
    assert len(flipping) == 1
    assert flipping[0].relation is RelationType.C2C3
    assert flipping[0].under_trilateral_only < 1.0 < flipping[0].under_with_doubled
    assert not sensitivity[RelationType.C1C2].sign_flips
    assert not sensitivity[RelationType.C1C3].sign_flips


def test_certification_over_one_source_is_refused() -> None:
    """التصديقُ اتّفاقُ مصدرين؛ ووسمُه عن واحدٍ يُرَدُّ عند الإنشاء."""

    census = derive_rights_census(InclusionPolicy.WITH_DOUBLED)

    assert census.certification is Certification.UNDETERMINED

    with pytest.raises(SlotAlgebraError, match="لا يصدر وسمُ التصديق"):
        RightsCensus(
            policy=InclusionPolicy.WITH_DOUBLED,
            roots=1,
            dropped_for_unranked=0,
            cells=1,
            attested=1,
            prevention_candidates=(),
            undetermined=(),
            source_digest="x",
            certification=Certification.CERTIFIED,
        )


def test_the_permutation_floor_is_one_over_b_plus_one() -> None:
    """حدُّ التباديل `1/(B+1)`، وعددٌ غيرُ موجبٍ يُرَدّ."""

    assert permutation_floor() == pytest.approx(1 / (PERMUTATIONS + 1))
    assert permutation_floor(2000) == pytest.approx(0.0004997, abs=1e-7)

    with pytest.raises(SlotAlgebraError, match="عددُ التباديل موجب"):
        permutation_floor(0)
