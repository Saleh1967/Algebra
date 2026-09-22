"""يُشغِّل خطَّ البتّات إلى يونيكود العربيّة: كلُّ نمطٍ، وخانتُه، وما بقي معلَّقًا."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from alghanem.arabic.makhraj_bit_decoder import (  # noqa: E402
    EVERY_PATTERN_IS_A_MAKHRAJ_NOTE,
    FOUR_BITS_DO_NOT_NAME_A_LETTER_NOTE,
    MAKHRAJ_LETTERS,
    THE_BIT_ORDER_IS_A_DECLARED_CONVENTION_NOTE,
    THE_CLOSURE_IS_BARRED_NOT_MISSING_NOTE,
    THE_JAWF_AND_THE_KHAYSHUM_ARE_OUTSIDE_THE_RANGE_NOTE,
    DecodeOutcome,
    census,
    decode_value,
)


def main() -> None:
    reading = census()

    print(
        f"عرضُ المتّجه {reading.bit_width} بتّات، والأنماطُ {reading.patterns}، "
        f"والمخارجُ {reading.makharij}، والحروفُ {reading.letters_total}"
    )
    print(f"بصمةُ الجدول المُودَع = {reading.table_digest}")
    print()

    print("البتّات | الرتبة | المخرج | الحروف | نقاطُ يونيكود | الحال")
    print("-" * 78)
    for value in sorted(MAKHRAJ_LETTERS):
        readout = decode_value(value)
        mark = "معيَّن" if readout.outcome is DecodeOutcome.DETERMINED else "غيرُ معيَّن"
        print(
            f"{readout.bits} | {readout.value:>2} | {readout.makhraj_name} | "
            f"{' '.join(readout.letters)} | {' '.join(readout.codepoints)} | {mark}"
        )

    print()
    print(
        f"الأنماطُ المعيَّنة: {reading.determined_patterns}، "
        f"وحروفُها: {reading.letters_in_determined_patterns}"
    )
    print(
        f"الأنماطُ غيرُ المعيَّنة: {reading.underdetermined_patterns}، "
        f"وحروفُها: {reading.letters_in_underdetermined_patterns}"
    )
    print(f"أكبرُ خانةٍ: {reading.largest_class_size}")
    print(f"حاجزُ جدول الصفة: {reading.sifat_barrier.value}")
    print()
    print(THE_BIT_ORDER_IS_A_DECLARED_CONVENTION_NOTE)
    print(EVERY_PATTERN_IS_A_MAKHRAJ_NOTE)
    print(FOUR_BITS_DO_NOT_NAME_A_LETTER_NOTE)
    print(THE_CLOSURE_IS_BARRED_NOT_MISSING_NOTE)
    print(THE_JAWF_AND_THE_KHAYSHUM_ARE_OUTSIDE_THE_RANGE_NOTE)


if __name__ == "__main__":
    main()
