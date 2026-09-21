"""إيداعُ SLGAE: بصمةٌ من الملفّ، وتعارضان مُشتَقّان، وحصادٌ يُشغَّل على الخانات.

يُثبِت هذا الاختبارُ تسعةَ أشياء: أنّ بصمةَ الوثيقة تُقرأ من بايتاتها لا من
حقلٍ مكتوب، وأنّ الكتلَ المولودةَ تقسم مفردتَها بلا تكرارٍ وكلُّها في الجدول
المُجمَّد، وأنّ فرقَ المفردتين يُشتَقّ بالطرح فيخرج حرفَين بأعيانهما، وأنّ
أعدادَ القسمة الثلاثةَ تُسجَّل ولا تُدمَج، وأنّ تشغيلَ الصفات المولودة يحسم
أربعَ خاناتٍ ويُبقي ثلاثًا ويقف عند واحدة، وأنّ الحصادَ يوزّع العشرين بلا
بقيّة، وأنّ حرفًا خارجَ المفردة يُوقِف خانتَه ولا يُفرَد بغياب بيانه، وأنّ
شقَّين متداخلَين أو فارغَين يُرَدّان، وأنّ هذا الإيداعَ لا يرفع حاجزَ جدول
الصفة.
"""

from __future__ import annotations

import hashlib

import pytest

from alghanem.arabic.classical_makharij_table import CLASSICAL_ORDINAL
from alghanem.arabic.gflk_feature_table_import_barrier import ImportBarrierStanding
from alghanem.arabic.makhraj_bit_decoder import sifat_barrier_standing
from alghanem.arabic.slgae_deposit import (
    BORN_BLOCK_COUNT,
    BORN_BLOCKS,
    SPECIFICATION_CATEGORY_COUNT,
    BornSifaSplit,
    ClassOutcome,
    SlgaeDepositError,
    born_inventory,
    derive_class_readings,
    derive_division_conflict,
    derive_inventory_conflict,
    features_of,
    read_slgae_bytes,
    separation_reading,
    slgae_digest,
)


def test_the_digest_is_read_from_the_file_not_written_here() -> None:
    """البصمةُ تُشتَقّ من بايتات الوثيقة، فتُطابِق حسابًا مستقلًّا عليها."""

    payload = read_slgae_bytes()

    assert payload
    assert slgae_digest() == hashlib.sha256(payload).hexdigest()
    assert slgae_digest() == slgae_digest()


def test_the_born_blocks_partition_their_inventory() -> None:
    """الكتلُ الخمسُ تقسم ستًّا وعشرين حرفًا بلا تكرار، وكلُّها مرقَّمة."""

    inventory = born_inventory()

    assert BORN_BLOCK_COUNT == 5
    assert len(inventory) == 26
    assert len(inventory) == sum(len(chars) for _block, chars in BORN_BLOCKS)
    assert inventory <= set(CLASSICAL_ORDINAL)


def test_the_inventory_conflict_is_two_named_letters() -> None:
    """الفرقُ بين المفردتين يُشتَقّ بالطرح فيخرج حرفَين بأعيانهما."""

    conflict = derive_inventory_conflict()

    assert conflict.born_letters == 26
    assert conflict.frozen_letters == 28
    assert conflict.only_in_frozen == ("و", "ي")
    assert conflict.only_in_born == ()


def test_three_numbers_for_one_division_are_registered_not_merged() -> None:
    """خمسٌ وستَّ عشرةَ وثلاثَ عشرةَ: تُقرأ من مواضعها وتبقى ثلاثة."""

    conflict = derive_division_conflict()

    assert conflict.born_blocks == 5
    assert conflict.frozen_makharij == 16
    assert conflict.specification_categories == SPECIFICATION_CATEGORY_COUNT == 13
    assert len({conflict.born_blocks, conflict.frozen_makharij}) == 2


def test_the_born_features_resolve_four_classes_and_tie_three() -> None:
    """التشغيلُ يحسم الحلقيّتين والشفويّةَ ويُبقي الأسنانيّاتِ الثلاثَ متعادلة."""

    readings = {reading.makhraj_rank: reading for reading in derive_class_readings()}

    assert sorted(readings) == [1, 2, 3, 6, 11, 12, 13, 15]
    for rank in (1, 2, 3, 15):
        assert readings[rank].outcome is ClassOutcome.RESOLVED
        assert readings[rank].tied_groups == ()
    for rank in (11, 12, 13):
        assert readings[rank].outcome is ClassOutcome.TIED
        assert readings[rank].tied_groups == (readings[rank].letters,)
    assert readings[11].letters == ("ط", "د", "ت")


def test_the_harvest_divides_the_twenty_without_remainder() -> None:
    """العشرون موزّعةٌ: ثمانيةٌ محسومةٌ وتسعةٌ متعادلةٌ وثلاثةٌ موقوفة."""

    reading = separation_reading()

    assert reading.letters_unresolved_before == 20
    assert reading.resolved_letters == 8
    assert reading.tied_letters == 9
    assert reading.undecided_letters == 3
    assert reading.resolved_classes == 4
    assert reading.tied_classes == 3
    assert reading.undecided_classes == 1
    assert reading.document_digest == slgae_digest()


def test_a_letter_outside_the_born_inventory_halts_its_class() -> None:
    """الياءُ خارجَ المفردة المولودة، فخانتُها موقوفةٌ ولا تُحسَم بغياب بيانها."""

    assert features_of("ي") is None
    assert features_of("و") is None
    assert features_of("ط") is not None

    class_six = next(
        reading for reading in derive_class_readings() if reading.makhraj_rank == 6
    )

    assert class_six.outcome is ClassOutcome.UNDECIDED
    assert class_six.letters_outside_born == ("ي",)
    assert class_six.separated_letters == ()
    assert class_six.tied_groups == ()


def test_a_split_with_overlapping_or_empty_sides_is_refused() -> None:
    """شقّان متداخلان لا يفصلان، وشقٌّ فارغٌ ليس صفةً بل غيابُها."""

    with pytest.raises(SlgaeDepositError, match="شقَّي الصفة معًا"):
        BornSifaSplit(block="كتلة", side_a="تد", side_b="دط")
    with pytest.raises(SlgaeDepositError, match="شقٌّ فارغ"):
        BornSifaSplit(block="كتلة", side_a="تد", side_b="")


def test_this_deposit_does_not_lift_the_sifat_barrier() -> None:
    """الحاجزُ باقٍ قائمًا: الإيداعُ يُسجّل ويقيس ولا يرفع."""

    assert sifat_barrier_standing() is ImportBarrierStanding.OPEN
