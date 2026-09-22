"""مقابلةُ الخانة الدنيا: اسمٌ واحدٌ لمُسمَّيين، واثنتا عشرةَ وقوعةً لإحدى عشرةَ خليّة.

يُثبِت هذا الاختبارُ ثمانيةَ أشياء: أنّ حجمَ فضاء (C,H) مُشتَقٌّ من الجدول
المُبصَّم لا مكتوبًا، وأنّ قنوات ٥د الأربعَ تجمع إلى حجم الفضاء بلا فضلة، وأنّ
غيرَ المولود اثنتا عشرةَ وقوعةً وإحدى عشرةَ خليّةً متمايزةً مشترَكُها `خْ`،
وأنّ الوثيقةَ عدّت الوقوعاتِ لا الخلايا، وأنّ محورَ الصامت 28 في ٥د و26 في
٥ي و٥ك بشاهدٍ مقروءٍ من القائمة، وأنّ المقيسَ اليومَ اثنان من أربعة، وأنّ
حقولَ الصياغتين مختلفةُ العدد والمجال فلا يلتقيان بالاسم، وأنّ فرقًا بلا
مشترَكٍ يُرَدُّ عند الإنشاء.
"""

from __future__ import annotations

import pytest

from alghanem.arabic.classical_makharij_table import CLASSICAL_ORDINAL
from alghanem.arabic.minimal_complete_slot_comparison import (
    BASIC_STATES,
    CHANNELS,
    MCU_CONDITIONS,
    PROPOSED_FIELDS,
    STANDING_FIELDS,
    TWO_OBJECTS_UNDER_ONE_NAME_NOTE,
    Measurability,
    UnbornCellCount,
    derive_channel_arithmetic,
    derive_inventory_conflict_inside_the_document,
    derive_measurable_today,
    derive_unborn_cell_count,
    slot_space_size,
)
from alghanem.arabic.slgae_deposit import SlgaeDepositError


def test_the_slot_space_is_derived_from_the_frozen_table() -> None:
    """112 = حروفُ الجدول × الحالاتِ الأربع، مُشتَقًّا لا مكتوبًا."""

    assert slot_space_size() == len(CLASSICAL_ORDINAL) * len(BASIC_STATES)
    assert slot_space_size() == 112
    assert len(BASIC_STATES) == 4


def test_every_channel_sums_to_the_space_without_remainder() -> None:
    """القنواتُ الأربعُ تجمع إلى حجم الفضاء، بلا فضلةٍ ولا نقص."""

    arithmetic = derive_channel_arithmetic()

    assert len(arithmetic) == 4
    assert all(matches for _name, _total, matches in arithmetic)
    assert all(total == 112 for _name, total, _matches in arithmetic)


def test_twelve_occurrences_are_eleven_distinct_cells() -> None:
    """المشترَكُ `خْ` يجعل الاتّحادَ أحدَ عشرَ، والجمعَ اثني عشر."""

    count = derive_unborn_cell_count()

    assert count.occurrences == 12
    assert count.distinct_cells == 11
    assert count.shared_cells == ("خْ",)
    assert count.document_says == 12
    assert count.document_counts_occurrences


def test_a_difference_without_a_shared_cell_is_refused() -> None:
    """فرقُ الوقوعات عن الخلايا يساوي عددَ المشترَك، وإلّا رُدّ البناء."""

    with pytest.raises(SlgaeDepositError, match="لا يطابق عددَ المشترَك"):
        UnbornCellCount(
            occurrences=12,
            distinct_cells=11,
            shared_cells=(),
            document_says=12,
        )


def test_the_axis_carries_two_inventories_inside_one_document() -> None:
    """28 في ٥د و26 في ٥ي و٥ك، وشاهدُ الأولى مقروءٌ من قائمتها."""

    conflict = derive_inventory_conflict_inside_the_document()

    assert conflict.in_cv112 == 28
    assert conflict.in_markov_and_vowel_first == 26
    assert "وْ" in conflict.witness
    syntactic = next(channel for channel in CHANNELS if channel.name == "نحويّة")
    assert any(cell.startswith("و") for cell in syntactic.unborn_cells)


def test_the_compatibility_condition_never_refuses_in_two_channels() -> None:
    """الجذعيّةُ والصوتيّةُ بلا خليّةٍ غيرِ مولودة، فالشرطُ هناك لا يرفض."""

    for name in ("جذعيّة", "صوتيّة"):
        channel = next(row for row in CHANNELS if row.name == name)
        assert channel.unborn_cells == ()
        assert channel.born == slot_space_size()


def test_two_of_the_four_conditions_are_measurable_here() -> None:
    """يُقاس اثنان من بايتات الشجرة، وواحدٌ منقولٌ وواحدٌ يحتاج طبقةً لم تُبنَ."""

    measurable, total = derive_measurable_today()

    assert (measurable, total) == (2, 4)
    standings = [condition.standing for condition in MCU_CONDITIONS]
    assert standings.count(Measurability.MEASURABLE_HERE) == 2
    assert standings.count(Measurability.TRANSCRIBED_ONLY) == 1
    assert standings.count(Measurability.NEEDS_A_LAYER_NOT_BUILT) == 1
    assert all(condition.what_it_rests_on.strip() for condition in MCU_CONDITIONS)


def test_the_two_formulations_differ_in_arity_and_domain() -> None:
    """أربعةُ حقولٍ إسناديّةٍ مقابل ثلاثةٍ مقطعيّة، فلا يلتقيان بالاسم."""

    assert len(STANDING_FIELDS) == 4
    assert len(PROPOSED_FIELDS) == 3
    assert {name for name, _gloss in STANDING_FIELDS} == {"a", "g", "p", "r"}
    assert {name for name, _gloss in PROPOSED_FIELDS} == {"C", "H", "B"}
    assert "لا يلتقيان بالاسم" in TWO_OBJECTS_UNDER_ONE_NAME_NOTE
