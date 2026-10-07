"""فكُّ البتّات إلى يونيكود: فضاءٌ ممسوحٌ كاملًا، وفقدٌ مقيسٌ، وحاجزٌ مقروءٌ حيًّا.

يُثبِت هذا الاختبارُ سبعةَ أشياء: أنّ كلَّ نمطٍ بعرضِ الجدول يُفَكُّ ولا يُرَدُّ
واحدٌ لخروجه عن المجال، وأنّ نصفَ الأنماط يُعيّن حرفًا ونصفَها لا يُعيّن فيخرج
بخانته كاملةً، وأنّ الترميزَ ثمّ الفكَّ يُرجِع خانةَ الحرف لا الحرفَ — وذلك فقدٌ
معدودٌ لا عيبٌ يُداوى بالاختيار، وأنّ حرفًا بلا رتبةٍ يُرَدُّ باسمه، وأنّ عرضًا
أو رمزًا خارجَ الشرط يُرَدُّ ولا يُصفَّر صمتًا، وأنّ كلَّ حرفٍ مرقَّمٍ نقطةُ
يونيكود واحدةٌ مستقرّةٌ تحت NFC، وأنّ حاجزَ جدول الصفة يُقرأ من موضعه فيبقى
ادّعاءُ «الإغلاقُ ممنوعٌ لا مفقود» صادقًا بالتشغيل لا بالنثر.
"""

from __future__ import annotations

import unicodedata

import pytest

from alghanem.arabic.classical_makharij_table import (
    CLASSICAL_ORDINAL,
    CLASSICAL_TABLE_DIGEST,
)
from alghanem.arabic.gflk_feature_table_import_barrier import ImportBarrierStanding
from alghanem.arabic.makhraj_bit_decoder import (
    MAKHRAJ_BIT_WIDTH,
    MAKHRAJ_LETTERS,
    DecodeOutcome,
    MakhrajBitError,
    bits_of_value,
    census,
    codepoint_of,
    decode_bits,
    decode_value,
    encode_letter,
    sifat_barrier_standing,
    value_of_bits,
)


def _every_pattern() -> list[str]:
    return [
        format(value, f"0{MAKHRAJ_BIT_WIDTH}b") for value in range(2**MAKHRAJ_BIT_WIDTH)
    ]


def test_every_pattern_decodes_and_none_is_out_of_range() -> None:
    """فضاءُ البتّات ممسوحٌ كاملًا: لا نمطَ بلا مخرجٍ ولا مخرجَ بلا نمط."""

    readouts = [decode_bits(bits) for bits in _every_pattern()]

    assert len(readouts) == 2**MAKHRAJ_BIT_WIDTH
    assert {r.value for r in readouts} == set(MAKHRAJ_LETTERS)
    assert all(r.letters for r in readouts)


def test_half_the_patterns_name_a_letter_and_half_do_not() -> None:
    """نصفُ الأنماط يُعيّن حرفًا، ونصفُها يُخرِج خانتَه كاملةً بلا اختيار."""

    reading = census()

    assert reading.determined_patterns == 8
    assert reading.underdetermined_patterns == 8
    assert reading.letters_in_determined_patterns == 8
    assert reading.letters_in_underdetermined_patterns == 20
    assert reading.letters_total == len(CLASSICAL_ORDINAL)
    assert reading.largest_class_size == 3
    assert reading.table_digest == CLASSICAL_TABLE_DIGEST


def test_a_determined_pattern_yields_one_codepoint() -> None:
    """خانةٌ فيها حرفٌ واحدٌ تخرج بنقطةِ يونيكود واحدةٍ وحالٍ معيَّنة."""

    readout = decode_bits(encode_letter("ق"))

    assert readout.outcome is DecodeOutcome.DETERMINED
    assert readout.letters == ("ق",)
    assert readout.codepoints == ("U+0642",)
    assert readout.unresolved_letters == 0


def test_an_underdetermined_pattern_yields_its_whole_class() -> None:
    """خانةٌ فيها ثلاثةُ حروفٍ تخرج بثلاثتها، ولا يُنتقى منها واحد."""

    readout = decode_bits(encode_letter("ت"))

    assert readout.outcome is DecodeOutcome.UNDERDETERMINED
    assert readout.letters == ("ط", "د", "ت")
    assert readout.codepoints == ("U+0637", "U+062F", "U+062A")
    assert readout.unresolved_letters == 2


def test_encode_then_decode_returns_the_class_not_the_letter() -> None:
    """الترميزُ ثمّ الفكُّ يُرجِع خانةَ الحرف؛ والفقدُ معدودٌ على الحروف كلِّها."""

    recovered_exactly = 0
    for letter in sorted(CLASSICAL_ORDINAL):
        readout = decode_bits(encode_letter(letter))
        assert letter in readout.letters
        if readout.letters == (letter,):
            recovered_exactly += 1

    assert recovered_exactly == census().letters_in_determined_patterns


def test_a_letter_without_a_rank_is_refused_by_name() -> None:
    """الألفُ خارجَ ترقيم الجدول قصدًا، فتُرَدُّ ولا تُلحَق بأقرب خانة."""

    with pytest.raises(MakhrajBitError, match="لا رتبةَ له"):
        encode_letter("ا")


def test_a_width_or_symbol_outside_the_condition_is_refused() -> None:
    """عرضٌ ناقصٌ أو رمزٌ غيرُ ثنائيٍّ يُرَدُّ، ولا يُصفَّر النقصُ صمتًا."""

    with pytest.raises(MakhrajBitError, match="عرضُ المتّجه"):
        value_of_bits("0" * (MAKHRAJ_BIT_WIDTH - 1))
    with pytest.raises(MakhrajBitError, match="غيرُ الصفر والواحد"):
        value_of_bits("0" * (MAKHRAJ_BIT_WIDTH - 1) + "2")
    with pytest.raises(MakhrajBitError, match="خارجَ الجدول"):
        decode_value(len(MAKHRAJ_LETTERS) + 1)
    with pytest.raises(MakhrajBitError, match="خارجَ الجدول"):
        bits_of_value(0)


def test_every_ranked_letter_is_one_stable_codepoint() -> None:
    """كلُّ حرفٍ مرقَّمٍ نقطةٌ واحدةٌ لا تتحرّك تحت NFC؛ والمركَّبُ يُرَدّ."""

    for letter in CLASSICAL_ORDINAL:
        assert unicodedata.normalize("NFC", letter) == letter
        assert codepoint_of(letter) == f"U+{ord(letter):04X}"

    with pytest.raises(MakhrajBitError, match="نقطةٍ"):
        codepoint_of("لا")


def test_the_closure_is_barred_and_the_barrier_is_read_live() -> None:
    """منزلةُ حاجزِ جدول الصفة تُقرأ من موضعها، فادّعاءُ المنعِ يُشغَّل لا يُنقَل."""

    assert sifat_barrier_standing() is ImportBarrierStanding.OPEN
    assert census().sifat_barrier is ImportBarrierStanding.OPEN
