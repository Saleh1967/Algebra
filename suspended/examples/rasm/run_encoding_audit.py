"""تدقيقُ Δرقمي على المواصفة المُصلَحة — تُشغَّل على البايتات، ويُعَدُّ الساقط.

**الفرقُ عن `run_unit_coverage.py`**: ذاك عرض المواصفةَ **كما وردت** فأحصى
ما يسقط عنها. وهذا يُشغِّل المواصفةَ **بعد الإصلاح الثلاثيّ** المقترَح في
الردّ على `f2f9d38`، ويسأل سؤالَ الدَّين الأوّل وحدَه: **كم موضعًا يسقط؟**

**الإصلاحُ مُعلَنٌ قبل التشغيل، وهو من عندي لا من الإيداع**:

1. **الحالاتُ ثمانٍ**: الأربعُ الأصليّةُ وثلاثةُ التنوين **و«عُرْي»** —
   حالةٌ **مصنَّفةٌ لا خالية**، لأنّها **مرصودة**؛ والخاليةُ ما لم يُرصَد.
2. **الحروفُ اثنان وثلاثون**: الثمانيةُ والعشرون، والهمزةُ (وكراسيها
   أ إ ؤ ئ تُطبَّع إليها بنصّ R2)، **وة وى وآ**.
3. **الشدّةُ تُوسَّع** ساكنًا ومتحرّكًا (R5)، **وصورُ العرض تُطبَّع** (R7).

والتنوينُ **يبقى حالةً ولا يُوسَّع** ههنا خلافًا لـR4: لأنّ R3 تعدّه في
السبع، والتوسيعُ يُخرجه منها — فالإيداعُ يعدّه مرّتين، ويُقرأ ههنا على R3.

**والمُعلَنُ قبل النظر**: إن كان الإصلاحُ تامًّا فالساقطُ **صفر**. وكلُّ
ساقطٍ يُطبَع بحرفه وعلامته وعدده — **لا يُجمَع في «أخرى»**.

**وΔضبط يُحسَب على مواضع الرسم لا على الموسَّع**، لأنّ المجرّدَ لا شدّةَ فيه
فلا توسيعَ له: Δضبط = H(حالة | حرف) على ٣٣٢٬٨٣٧ موضعًا. وهو **حدٌّ أعلى**
لما يضيفه الضبطُ فعلًا، إذ الشرطُ على السياق لا يزيد الإنتروبيا.
"""

from __future__ import annotations

import argparse
import math
import sys
import unicodedata
from collections import Counter
from pathlib import Path

HIJAI = "ابتثجحخدذرزسشصضطظعغفقكلمنهوي"
HAMZA = "ء"
SEATS = "أإؤئ"
EXTRA = "ةىآ"
DECLARED_LETTERS = frozenset(HIJAI + HAMZA + EXTRA)

FATHA, DAMMA, KASRA, SUKUN = "َ", "ُ", "ِ", "ْ"
TANWIN = ("ً", "ٌ", "ٍ")
SHADDA = "ّ"
BARE = ""
DECLARED_STATES = frozenset({FATHA, DAMMA, KASRA, SUKUN, *TANWIN, BARE})

MARK_POINTS = frozenset({0x64B, 0x64C, 0x64D, 0x64E, 0x64F, 0x650, 0x651, 0x652, 0x670})
MARKUP = "<sel>"


def normalise(letter: str) -> str:
    """R7 ثمّ R2: صورةُ العرض إلى أصلها، وكرسيُّ الهمزة إلى الهمزة."""

    if 0xFE70 <= ord(letter) <= 0xFEFC:
        folded = unicodedata.normalize("NFKD", letter)
        letter = folded[0] if folded else letter
    return HAMZA if letter in SEATS else letter


def emit(text: str) -> list[tuple[str, str]]:
    """وحداتُ (حرف، حالة) بعد التطبيع وتوسيع الشدّة."""

    units: list[tuple[str, str]] = []
    index = 0
    length = len(text)
    while index < length:
        letter = text[index]
        if letter.isspace() or ord(letter) in MARK_POINTS:
            index += 1
            continue
        if not (0x600 <= ord(letter) <= 0x6FF or 0xFE70 <= ord(letter) <= 0xFEFC):
            index += 1
            continue
        after = index + 1
        tail: list[str] = []
        while after < length and ord(text[after]) in MARK_POINTS:
            tail.append(text[after])
            after += 1
        base = normalise(letter)
        doubled = SHADDA in tail
        rest = [one for one in tail if one != SHADDA]
        state = rest[0] if rest else BARE
        if doubled:  # R5: المشدّدُ وحدتان — ساكنٌ ثمّ متحرّك
            units.append((base, SUKUN))
        units.append((base, state))
        index = after
    return units


def fallout(units: list[tuple[str, str]]) -> Counter[tuple[str, str]]:
    """كلُّ وحدةٍ خارج الفضاء المعلن، بحرفها وحالتها — لا تُجمَع في «أخرى»."""

    return Counter(
        (letter, state)
        for letter, state in units
        if letter not in DECLARED_LETTERS or state not in DECLARED_STATES
    )


def rasm_units(text: str) -> list[tuple[str, str]]:
    """مواضعُ الرسم بحالاتها كاملةً — بلا توسيعٍ، ليقابلَها المجرّد."""

    found: list[tuple[str, str]] = []
    index = 0
    length = len(text)
    while index < length:
        letter = text[index]
        if letter.isspace() or ord(letter) in MARK_POINTS:
            index += 1
            continue
        if not (0x600 <= ord(letter) <= 0x6FF or 0xFE70 <= ord(letter) <= 0xFEFC):
            index += 1
            continue
        after = index + 1
        tail: list[str] = []
        while after < length and ord(text[after]) in MARK_POINTS:
            tail.append(text[after])
            after += 1
        found.append((normalise(letter), "".join(tail)))
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

    units = emit(given.text.read_text(encoding="utf-8").replace(MARKUP, " "))
    missed = fallout(units)
    space = len(DECLARED_LETTERS) * len(DECLARED_STATES)
    seen = Counter(units)

    print(f"الفضاءُ المعلن: {len(DECLARED_LETTERS)} × {len(DECLARED_STATES)} = {space}")
    print(f"وحداتٌ مُخرَجة: {len(units)}")
    print(f"**الساقط**: {sum(missed.values())}")
    if missed:
        print("  وتفصيلُه:", dict(missed.most_common()))
    print(f"أزواجٌ مرصودة: {len(seen)} من {space}")
    print(f"H(حرف،حالة) المرصودة: {entropy(seen):.4f}")
    print(f"سقفُ الفضاء المعلن log2({space}): {math.log2(space):.4f}")

    rasm = rasm_units(given.text.read_text(encoding="utf-8").replace(MARKUP, " "))
    joint = entropy(Counter(rasm))
    alone = entropy(Counter((letter, "") for letter, _ in rasm))
    print(f"مواضعُ الرسم: {len(rasm)}")
    print(f"H(حرف): {alone:.4f}")
    print(f"H(حرف،حالة): {joint:.4f}")
    print(f"**Δضبط = H(حالة|حرف)**: {joint - alone:.4f} بت/موضع (حدًّا أعلى)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
