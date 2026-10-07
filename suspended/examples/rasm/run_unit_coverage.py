"""عرضُ نظام (حرف × حالة) المُعلَن على بايتات المدوّنة — تغطيةً وإفادة.

**المُودَع** (`algebraic_recovery_proof.md`): الوحدةُ = حرفٌ من ٢٨ × حالةٍ من
سبع (أربعٌ أصليّةٌ وثلاثةُ تنوين) = ١٩٦؛ والتنوينُ يُوسَّع (R4)، والشدّةُ
تُوسَّع (R5)، وصورُ العرض تُطبَّع (R7).

**ما يُقاس ههنا**: كم موضعَ حرفٍ في المدوّنة **يقع في الفضاء المعلن**، وكم
يقع خارجَه — بحرفٍ ليس من الثمانية والعشرين، أو **بحالةٍ ليست من السبع**.
والسقفُ المعلن log₂(١٩٦) يُقابَل بالإنتروبيا **المرصودة** وبسقف الأبجديّة
المرصودة — فالسقفُ يُختبَر من فوقُ ومن تحت.
"""

from __future__ import annotations

import argparse
import math
import sys
from collections import Counter
from pathlib import Path

HIJAI = "ابتثجحخدذرزسشصضطظعغفقكلمنهوي"
HAMZA_SEATS = "ءأإؤئ"
DECLARED_STATES = 7
DECLARED_UNITS = 28 * DECLARED_STATES
MARK_POINTS = frozenset({0x64B, 0x64C, 0x64D, 0x64E, 0x64F, 0x650, 0x651, 0x652, 0x670})
MARKUP = "<sel>"


def units(text: str) -> list[tuple[str, str]]:
    """كلُّ موضعِ حرفٍ ومعه ما لحقه من علامات."""

    found: list[tuple[str, str]] = []
    index = 0
    length = len(text)
    while index < length:
        letter = text[index]
        if letter.isspace() or ord(letter) in MARK_POINTS:
            index += 1
            continue
        if not 0x600 <= ord(letter) <= 0x6FF:
            index += 1
            continue
        after = index + 1
        tail: list[str] = []
        while after < length and ord(text[after]) in MARK_POINTS:
            tail.append(text[after])
            after += 1
        found.append((letter, "".join(tail)))
        index = after
    return found


def entropy(counts: Counter[tuple[str, str]]) -> float:
    total = sum(counts.values())
    return -math.fsum(
        (number / total) * math.log2(number / total) for number in counts.values()
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", type=Path, required=True)
    given = parser.parse_args()

    found = units(given.text.read_text(encoding="utf-8").replace(MARKUP, " "))
    letters = Counter(letter for letter, _ in found)
    states = Counter(state for _, state in found)
    outside_letters = {
        letter: number
        for letter, number in letters.items()
        if letter not in HIJAI and letter not in HAMZA_SEATS
    }
    bare = states[""]

    print(f"مواضعُ الحروف: {len(found)}")
    print(f"بلا علامةٍ ألبتّة: {bare}")
    print(f"حروفٌ خارج الثمانيةِ والعشرين وكراسي الهمزة: {outside_letters}")
    print(f"الحالاتُ المرصودة: {len(states)} (والمعلنةُ {DECLARED_STATES})")
    print(f"أزواجٌ مرصودة: {len(Counter(found))} (والمعلنةُ {DECLARED_UNITS})")
    print(f"H(حرف،حالة) المرصودة: {entropy(Counter(found)):.4f}")
    print(f"السقفُ المعلن log2(196): {math.log2(DECLARED_UNITS):.4f}")
    print(f"سقفُ الأبجديّة المرصودة: {math.log2(len(Counter(found))):.4f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
