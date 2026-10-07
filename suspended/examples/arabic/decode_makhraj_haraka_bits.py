"""يُشغِّل المحورَين معًا: وحداتٌ مشكولةٌ خارجة، وكسبُ فصلٍ مطروحٌ أمامَ العين."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from alghanem.arabic.makhraj_bit_decoder import DecodeOutcome  # noqa: E402
from alghanem.arabic.makhraj_haraka_bit_decoder import (  # noqa: E402
    A_HARAKA_AXIS_WIDENS_THE_OUTPUT_NOTE,
    EIGHT_MEMBERS_FILL_THREE_BITS_NOTE,
    HARAKA_ALPHABET,
    THE_ABSENCE_IS_A_MEMBER_NOT_A_SUKUN_NOTE,
    THE_AXIS_IS_A_MARK_SLOT_NOT_A_MEASURED_DURATION_NOTE,
    THE_ORDER_WITHIN_THE_UNIT_CARRIES_NO_BIT_NOTE,
    bits_of_haraka,
    census,
    decode_vector,
    encode_unit,
)

_SAMPLE_LETTERS: tuple[str, ...] = ("ق", "ت", "ج", "ب")


def main() -> None:
    reading = census()

    print(
        f"عرضُ المتّجه {reading.vector_bit_width} بتّات = "
        f"مخرجٌ + حركة، والأنماطُ {reading.patterns}، "
        f"والوحداتُ المكتوبة {reading.units_total}"
    )
    print()

    print("المتّجه | المخرج | الحركة | الوحدات | الحال")
    print("-" * 78)
    for letter in _SAMPLE_LETTERS:
        for mark in HARAKA_ALPHABET:
            readout = decode_vector(encode_unit(letter, mark))
            mark_bits = bits_of_haraka(mark)
            state = (
                "معيَّن" if readout.outcome is DecodeOutcome.DETERMINED else "غيرُ معيَّن"
            )
            print(
                f"{readout.bits} | {readout.makhraj.makhraj_name} | "
                f"{mark_bits} {readout.haraka_name} | "
                f"{' '.join(readout.units)} | {state}"
            )
        print("-" * 78)

    print(
        f"الأنماطُ المعيَّنة: {reading.determined_patterns}، "
        f"وغيرُ المعيَّنة: {reading.underdetermined_patterns}"
    )
    print(
        f"الحروفُ غيرُ المعيَّنة قبل المحور: {reading.unresolved_letters_before_axis}، "
        f"وبعده: {reading.unresolved_letters_after_axis}"
    )
    print(f"كسبُ الفصل = {reading.separation_gain}")
    print()
    print(A_HARAKA_AXIS_WIDENS_THE_OUTPUT_NOTE)
    print(THE_ABSENCE_IS_A_MEMBER_NOT_A_SUKUN_NOTE)
    print(EIGHT_MEMBERS_FILL_THREE_BITS_NOTE)
    print(THE_AXIS_IS_A_MARK_SLOT_NOT_A_MEASURED_DURATION_NOTE)
    print(THE_ORDER_WITHIN_THE_UNIT_CARRIES_NO_BIT_NOTE)


if __name__ == "__main__":
    main()
