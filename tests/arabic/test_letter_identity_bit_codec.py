"""مِرمازُ الهُويّة: تقابلٌ تامٌّ مفحوصٌ بالمسح، ورفضٌ لا لفّ، وخانةٌ باقيةٌ مفتوحة.

يُثبِت هذا الاختبارُ تسعةَ أشياء: أنّ مفردةَ الهُويّة هي حروفُ الجدول المُودَع
بترتيب المرور عليه، وأنّ فضاءَ البتّات أوسعُ من المفردة فتبقى أنماطٌ بلا حرف،
وأنّ تلك الأنماطَ تُرَدُّ ولا تُلَفّ على أوّل المفردة، وأنّ الترميزَ والفكَّ
تقابلٌ تامٌّ على الوحدات الأربعِ والعشرين ومئتين مسحًا لا عيّنة، وأنّ كلَّ نمطٍ
مُسنَدٍ يُخرِج وحدةً واحدةً معيَّنةً لا مجموعة، وأنّ السلسلةَ تُرمَّز وتُفَكّ
بطولٍ من مضاعفات عرض الوحدة ويُرَدُّ ما دونه، وأنّ حرفًا خارجَ المدى يُرَدُّ
باسمه، وأنّ **الخانةَ الصوتيّةَ باقيةٌ مفتوحةً** فهذا المِرمازُ تجاوزٌ للسؤال
لا جوابٌ له.
"""

from __future__ import annotations

import pytest

from alghanem.arabic.classical_makharij_table import CLASSICAL_ORDINAL
from alghanem.arabic.gflk_feature_table_import_barrier import ImportBarrierStanding
from alghanem.arabic.letter_identity_bit_codec import (
    IDENTITY_ALPHABET,
    IDENTITY_BIT_WIDTH,
    UNASSIGNED_PATTERNS,
    UNIT_BIT_WIDTH,
    codec_census,
    decode_stream,
    decode_unit,
    encode_stream,
    encode_unit,
    is_assigned,
)
from alghanem.arabic.makhraj_bit_decoder import MakhrajBitError, sifat_barrier_standing
from alghanem.arabic.makhraj_bit_decoder import census as makhraj_census
from alghanem.arabic.makhraj_haraka_bit_decoder import HARAKA_ALPHABET

_FATHA = "َ"


def test_the_alphabet_is_the_deposited_letters_in_traversal_order() -> None:
    """المفردةُ حروفُ الجدول المُودَع نفسُها، بلا زيادةٍ ولا نقصٍ ولا تكرار."""

    assert len(IDENTITY_ALPHABET) == len(CLASSICAL_ORDINAL)
    assert set(IDENTITY_ALPHABET) == set(CLASSICAL_ORDINAL)
    assert len(set(IDENTITY_ALPHABET)) == len(IDENTITY_ALPHABET)
    assert IDENTITY_ALPHABET[0] == "ء"


def test_the_space_is_wider_than_the_alphabet_and_the_excess_is_counted() -> None:
    """فضاءُ الهُويّة أوسعُ من مفردتها، والفضلةُ معدودةٌ لا مسكوتٌ عنها."""

    assert 2**IDENTITY_BIT_WIDTH > len(IDENTITY_ALPHABET)
    assert UNASSIGNED_PATTERNS == 2**IDENTITY_BIT_WIDTH - len(IDENTITY_ALPHABET)
    assert UNASSIGNED_PATTERNS == 4


def test_an_unassigned_pattern_is_refused_and_not_wrapped() -> None:
    """نمطٌ بلا حرفٍ يُرَدُّ صريحًا، ولا يُقرأ أوّلَ المفردة."""

    for value in range(len(IDENTITY_ALPHABET), 2**IDENTITY_BIT_WIDTH):
        identity = format(value, f"0{IDENTITY_BIT_WIDTH}b")
        assert not is_assigned(identity)
        with pytest.raises(MakhrajBitError, match="بلا حرفٍ في المفردة"):
            decode_unit(f"{identity}000")


def test_the_codec_is_a_bijection_swept_not_sampled() -> None:
    """مسحٌ كاملٌ للفضاء: المُسنَدُ حاصلُ ضرب المفردتين، والمردودُ ما بقي."""

    reading = codec_census()

    assert reading.unit_bit_width == UNIT_BIT_WIDTH == 8
    assert reading.patterns == 256
    assert reading.assigned_patterns == 224
    assert reading.refused_patterns == 32
    assert reading.assigned_patterns == reading.letters * reading.haraka_members


def test_every_unit_round_trips_exactly() -> None:
    """كلُّ وحدةٍ تعود بعينها: حرفُها وعلامتُها ونصُّها، بلا مجموعةِ احتمالات."""

    seen: set[str] = set()
    for letter in IDENTITY_ALPHABET:
        for mark in HARAKA_ALPHABET:
            bits = encode_unit(letter, mark)
            decoded = decode_unit(bits)
            assert decoded.letter == letter
            assert decoded.haraka == mark
            assert decoded.unit == f"{letter}{mark}"
            seen.add(bits)
    assert len(seen) == codec_census().assigned_patterns


def test_a_stream_encodes_and_decodes_as_one_text() -> None:
    """سلسلةُ وحداتٍ تُرمَّز وتُفَكّ نصًّا واحدًا بلا فقد."""

    units = (("ك", "ُ"), ("ت", "ِ"), ("ب", "ْ"))
    bits = encode_stream(units)

    assert len(bits) == len(units) * UNIT_BIT_WIDTH
    assert "".join(decoded.unit for decoded in decode_stream(bits)) == "كُتِبْ"


def test_a_stream_length_off_the_unit_width_is_refused() -> None:
    """طولٌ ليس من مضاعفات الوحدة يُرَدّ، ولا يُكمَّل بأصفارٍ ولا تُهمَل بقيّة."""

    with pytest.raises(MakhrajBitError, match="ليس من مضاعفات"):
        decode_stream(encode_unit("ب", _FATHA) + "0")


def test_a_letter_outside_the_range_is_refused_by_name() -> None:
    """الألفُ والفراغُ خارجَ مدى المِرماز، فيُرَدّان ولا يُمرَّران."""

    with pytest.raises(MakhrajBitError, match="خارجَ مفردة الهُويّة"):
        encode_unit("ا", _FATHA)
    with pytest.raises(MakhrajBitError, match="خارجَ مفردة الهُويّة"):
        encode_unit(" ", _FATHA)


def test_this_codec_does_not_close_the_phonetic_class() -> None:
    """التعيينُ هنا لا يحسم الخانةَ الصوتيّة: العشرون باقيةٌ والحاجزُ قائم."""

    assert makhraj_census().letters_in_underdetermined_patterns == 20
    assert sifat_barrier_standing() is ImportBarrierStanding.OPEN
