"""المحورُ الثاني: وسعٌ مقيسٌ في المخرَج، وكسبُ فصلٍ مطروحٌ فيخرج صفرًا.

يُثبِت هذا الاختبارُ ثمانيةَ أشياء: أنّ عرضَ المتّجه مجموعُ عرضَي محورَيه لا
رقمًا مكتوبًا، وأنّ فضاءَه ممسوحٌ كاملًا بلا نمطٍ مرفوض، وأنّ المخرَجَ صار
وحدةً مشكولةً من نقطتَين مستقرّةً تحت NFC، وأنّ الغيابَ عضوٌ في المفردة لا
سكونٌ مُضمَر، وأنّ **كسبَ الفصل صفرٌ مطروحًا** فالحركةُ توسّع ولا تحسم، وأنّ
الترميزَ ثمّ الفكَّ يُرجِع الخانةَ مشكولةً بعلامتها، وأنّ علامةً أو عرضًا خارجَ
الشرط يُرَدُّ ولا يُصفَّر صمتًا، وأنّ حاجزَ جدول الصفة لم يُمسّ.
"""

from __future__ import annotations

import unicodedata

import pytest

from alghanem.arabic.classical_makharij_table import CLASSICAL_ORDINAL
from alghanem.arabic.gflk_feature_table_import_barrier import ImportBarrierStanding
from alghanem.arabic.makhraj_bit_decoder import (
    MAKHRAJ_BIT_WIDTH,
    DecodeOutcome,
    MakhrajBitError,
    sifat_barrier_standing,
)
from alghanem.arabic.makhraj_bit_decoder import census as makhraj_census
from alghanem.arabic.makhraj_haraka_bit_decoder import (
    HARAKA_ABSENT,
    HARAKA_ALPHABET,
    HARAKA_BIT_WIDTH,
    THE_ABSENCE_NAME,
    VECTOR_BIT_WIDTH,
    bits_of_haraka,
    census,
    decode_vector,
    encode_unit,
    haraka_of_bits,
    render_unit,
    split_vector,
)
from alghanem.arabic.written_haraka_mark import THE_IMPORTED_HARAKAT

_FATHA = "َ"
_SUKUN = "ْ"


def test_the_vector_width_is_the_sum_of_its_two_axes() -> None:
    """عرضُ المتّجه مشتقٌّ من حجمَي المفردتَين، والحركةُ تملأ بتّاتها بلا فضلة."""

    assert HARAKA_ALPHABET[0] == HARAKA_ABSENT
    assert len(HARAKA_ALPHABET) == len(THE_IMPORTED_HARAKAT) + 1
    assert 2**HARAKA_BIT_WIDTH == len(HARAKA_ALPHABET)
    assert VECTOR_BIT_WIDTH == MAKHRAJ_BIT_WIDTH + HARAKA_BIT_WIDTH


def test_every_vector_decodes_and_the_space_is_swept() -> None:
    """فضاءُ المحورَين ممسوحٌ كاملًا: لا نمطَ بلا قراءة."""

    reading = census()

    assert reading.patterns == 2**VECTOR_BIT_WIDTH
    assert reading.determined_patterns + reading.underdetermined_patterns == 128
    assert reading.units_total == len(CLASSICAL_ORDINAL) * len(HARAKA_ALPHABET)


def test_the_axis_widens_the_output_and_gains_no_separation() -> None:
    """كسبُ الفصل مطروحٌ فيخرج صفرًا: الحركةُ تضاعف الأنماطَ ولا تحسم حرفًا."""

    reading = census()
    before = makhraj_census()

    assert reading.patterns == before.patterns * len(HARAKA_ALPHABET)
    assert reading.unresolved_letters_before_axis == 20
    assert reading.unresolved_letters_after_axis == 20
    assert reading.separation_gain == 0


def test_a_vocalized_unit_is_two_stable_codepoints() -> None:
    """المخرَجُ وحدةٌ مشكولةٌ من نقطتَين لا تتحرّكان تحت NFC."""

    readout = decode_vector(encode_unit("ق", _FATHA))

    assert readout.outcome is DecodeOutcome.DETERMINED
    assert readout.units == ("قَ",)
    assert readout.codepoints == (("U+0642", "U+064E"),)
    assert unicodedata.normalize("NFC", readout.units[0]) == readout.units[0]


def test_the_absence_is_a_member_and_is_not_named_a_sukun() -> None:
    """الغيابُ عضوٌ مُسمًّى بذاته، والسكونُ عضوٌ آخرُ بنقطته."""

    absent = decode_vector(encode_unit("ق", HARAKA_ABSENT))
    silent = decode_vector(encode_unit("ق", _SUKUN))

    assert absent.haraka_name == THE_ABSENCE_NAME
    assert absent.units == ("ق",)
    assert silent.units == ("قْ",)
    assert absent.bits != silent.bits
    assert HARAKA_ABSENT not in THE_IMPORTED_HARAKAT


def test_an_underdetermined_class_comes_back_vocalized_whole() -> None:
    """خانةٌ غيرُ معيَّنةٍ تخرج بحروفها كلِّها مشكولةً بعلامةٍ واحدة."""

    readout = decode_vector(encode_unit("ت", _FATHA))

    assert readout.outcome is DecodeOutcome.UNDERDETERMINED
    assert readout.units == ("طَ", "دَ", "تَ")
    assert readout.unresolved_letters == 2


def test_encode_then_decode_returns_the_class_with_its_mark() -> None:
    """الترميزُ ثمّ الفكُّ يُرجِع العلامةَ بعينها والحرفَ في خانته."""

    for letter in sorted(CLASSICAL_ORDINAL):
        for mark in HARAKA_ALPHABET:
            readout = decode_vector(encode_unit(letter, mark))
            assert readout.haraka == mark
            assert render_unit(letter, mark) in readout.units


def test_a_mark_or_width_outside_the_condition_is_refused() -> None:
    """علامةٌ خارجَ المفردة أو عرضٌ ناقصٌ يُرَدّ، ولا يُحمَل على أقرب عضو."""

    with pytest.raises(MakhrajBitError, match="خارجَ المفردة"):
        bits_of_haraka("ّ")
    with pytest.raises(MakhrajBitError, match="عرضُ محور الحركة"):
        haraka_of_bits("0" * (HARAKA_BIT_WIDTH - 1))
    with pytest.raises(MakhrajBitError, match="غيرُ الصفر والواحد"):
        haraka_of_bits("0" * (HARAKA_BIT_WIDTH - 1) + "2")
    with pytest.raises(MakhrajBitError, match="عرضُ المتّجه"):
        split_vector("0" * (VECTOR_BIT_WIDTH - 1))


def test_the_second_axis_leaves_the_sifat_barrier_untouched() -> None:
    """المحورُ الثاني مأخوذٌ من مُودَعٍ قائم، فحاجزُ جدول الصفة باقٍ كما كان."""

    assert sifat_barrier_standing() is ImportBarrierStanding.OPEN
