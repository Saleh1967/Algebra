"""يُشغِّل مِرمازَ الهُويّة: نصٌّ مشكولٌ ← بتّات ← نصٌّ، وإحصاءُ الفضاء كلِّه."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from alghanem.arabic.letter_identity_bit_codec import (  # noqa: E402
    FOUR_PATTERNS_ARE_UNASSIGNED_NOTE,
    IDENTITY_ALPHABET,
    THE_ALPHABET_ORDER_IS_A_TRAVERSAL_NOTE,
    THE_CLASS_REMAINS_OPEN_NOTE,
    THE_IDENTITY_AXIS_DETERMINES_AND_MEANS_NOTHING_NOTE,
    THE_UNIT_IS_A_LETTER_AND_A_MARK_NOTE,
    codec_census,
    decode_stream,
    encode_stream,
    encode_unit,
)

_SAMPLE: tuple[tuple[str, str], ...] = (
    ("ك", "ُ"),
    ("ت", "ِ"),
    ("ب", "ْ"),
)


def main() -> None:
    reading = codec_census()
    print(
        f"عرضُ الوحدة {reading.unit_bit_width} بتّات، والأنماطُ "
        f"{reading.patterns}: مُسنَدٌ {reading.assigned_patterns} "
        f"ومردودٌ {reading.refused_patterns}"
    )
    print(f"الحروفُ {reading.letters}، والعلاماتُ {reading.haraka_members}")
    print(f"بصمةُ الجدول المُودَع = {reading.table_digest}")
    print()

    bits = encode_stream(_SAMPLE)
    decoded = decode_stream(bits)
    print("الوحدة | البتّات | النقاط")
    print("-" * 50)
    for unit in decoded:
        print(f"{unit.unit} | {unit.bits} | {' '.join(unit.codepoints)}")
    print()
    print(f"السلسلة = {bits}")
    print(f"النصُّ المُستَرجَع = {''.join(unit.unit for unit in decoded)}")
    print()

    print("أوائلُ المفردة بترتيب المرور على الجدول:")
    for index, letter in enumerate(IDENTITY_ALPHABET[:6]):
        print(f"  {index:>2} | {letter} | {encode_unit(letter, '')}")
    print()
    print(THE_IDENTITY_AXIS_DETERMINES_AND_MEANS_NOTHING_NOTE)
    print(THE_CLASS_REMAINS_OPEN_NOTE)
    print(FOUR_PATTERNS_ARE_UNASSIGNED_NOTE)
    print(THE_ALPHABET_ORDER_IS_A_TRAVERSAL_NOTE)
    print(THE_UNIT_IS_A_LETTER_AND_A_MARK_NOTE)


if __name__ == "__main__":
    main()
