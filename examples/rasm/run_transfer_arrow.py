"""النقلُ وسهمُ الزمن بين مجرى الحال ومجرى الحرف — تشغيلُ ختم `4289fc6c…`.

**ولا اسمَ يدخل السجلّ**: المحرفُ **شريحةٌ ونقطةُ ترميز**، والمجريان
مأخوذان من المجمَّد وحدَه.
"""

from __future__ import annotations

import argparse
import math
import random
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

VERSES = 6_236
BARE = "·"
START = "⊢"
SHUFFLES = 20
WITNESS = 1_000
SEED = 20_260_925

Stream = list[list[tuple[str, str]]]


def marked(one: str) -> bool:
    return unicodedata.category(one) == "Mn"


def arabic(one: str) -> bool:
    return any("ARABIC" in unicodedata.name(two, "") for two in one)


def ending(one: str) -> str:
    return one[-1] if one and marked(one[-1]) else BARE


def final_letter(one: str) -> str:
    for two in reversed(one):
        if not marked(two):
            return two
    return BARE


def shown(one: str) -> str:
    """صورةُ المحرف: شريحتُه ونقطةُ ترميزه — **ولا اسمَ يونيكود**."""

    return one if one in (BARE, START) else f"{one} U+{ord(one):04X}"


def entropy(counts: Counter[str]) -> float:
    total = sum(counts.values())
    if total == 0:
        return 0.0
    return -math.fsum(
        (one / total) * math.log2(one / total) for one in counts.values() if one
    )


def arrangements(counts: Counter[str]) -> float:
    total = sum(counts.values())
    if total == 0:
        return 0.0
    return (
        math.lgamma(total + 1)
        - math.fsum(math.lgamma(one + 1) for one in counts.values())
    ) / math.log(2)


def rows(lines: Stream, target: int, past: tuple[int, ...]) -> list[tuple[str, str]]:
    """(مفتاحُ الماضي، الهدف) لكلّ موضعٍ له سابقٌ داخلَ السطر."""

    out: list[tuple[str, str]] = []
    for line in lines:
        for place in range(1, len(line)):
            key = "|".join(line[place - 1][one] for one in past)
            out.append((key, line[place][target]))
    return out


def conditional(pairs: list[tuple[str, str]]) -> float:
    """H(الهدف | المفتاح) بالتقدير الساذج."""

    blocks: defaultdict[str, Counter[str]] = defaultdict(Counter)
    for key, value in pairs:
        blocks[key][value] += 1
    total = len(pairs)
    if total == 0:
        return 0.0
    return math.fsum(
        sum(one.values()) / total * entropy(one) for one in blocks.values()
    )


def price(
    taught: list[tuple[str, str]], asked: list[tuple[str, str]], width: int
) -> float:
    """ثمنُ الهدف على المحجوز بشفرةٍ قُدِّرت على الآخر — تنعيمُ لابلاس."""

    blocks: defaultdict[str, Counter[str]] = defaultdict(Counter)
    for key, value in taught:
        blocks[key][value] += 1
    if not asked:
        return 0.0
    cost = 0.0
    for key, value in asked:
        seen = blocks.get(key, Counter())
        cost -= math.log2((seen.get(value, 0) + 1) / (sum(seen.values()) + width))
    return cost / len(asked)


def halves(lines: Stream) -> tuple[Stream, Stream]:
    return (
        [one for index, one in enumerate(lines) if index % 2 == 0],
        [one for index, one in enumerate(lines) if index % 2 == 1],
    )


def held(
    lines: Stream,
    target: int,
    narrow: tuple[int, ...],
    wide: tuple[int, ...],
    width: int,
) -> float:
    """النقلُ محجوزًا: فرقُ ثمنين على شقٍّ لم يُقدَّر عليه، بالتبادل."""

    even, odd = halves(lines)
    gained = 0.0
    for taught, asked in ((even, odd), (odd, even)):
        narrow_cost = price(
            rows(taught, target, narrow), rows(asked, target, narrow), width
        )
        wide_cost = price(rows(taught, target, wide), rows(asked, target, wide), width)
        gained += narrow_cost - wide_cost
    return gained / 2


def plain(
    lines: Stream, target: int, narrow: tuple[int, ...], wide: tuple[int, ...]
) -> float:
    """النقلُ ملحَقًا: فرقُ إنتروبيتين شرطيّتين على العيّنة نفسِها."""

    return conditional(rows(lines, target, narrow)) - conditional(
        rows(lines, target, wide)
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", type=Path, required=True)
    given = parser.parse_args()

    raw = [
        one
        for one in given.text.read_text(encoding="utf-8").splitlines()
        if one.strip()
    ]
    if len(raw) != VERSES:
        raise SystemExit(f"المدوّنةُ تبدّلت: {len(raw)} لا {VERSES}")
    print(f"— الأسطر: {len(raw)}")
    print("— حدُّ اللفظ: فيه حرفٌ عربيّ (المُصحَّح من 494465d1…)")
    print("— المجريان: حالُ الخاتمة، وحرفُ الخاتمة — من المجمَّد وحدَه")

    forward: Stream = []
    states: Counter[str] = Counter()
    letters: Counter[str] = Counter()
    counted = 0
    most_slack = -float("inf")
    for line in raw:
        cells = [
            (ending(one), final_letter(one)) for one in line.split() if arabic(one)
        ]
        forward.append(cells)
        for state, letter in cells:
            states[state] += 1
            letters[letter] += 1
            counted += 1
        if counted >= WITNESS:
            most_slack = max(
                most_slack, arrangements(states) - counted * entropy(states)
            )
    tokens = sum(len(one) for one in forward)
    print(f"— الألفاظ: {tokens} | وعبرَ العدّادات {counted}")
    print(f"— خاناتُ الحال: {len(states)} | H = {entropy(states):.4f}")
    print(f"— خاناتُ الحرف: {len(letters)} | H = {entropy(letters):.4f}")

    backward: Stream = [list(reversed(one)) for one in forward]
    wide_state = len(states)
    wide_letter = len(letters)

    names = {
        "ح⟵ح": (0, (0,), (0,), wide_state),
        "ر⟶ح": (0, (0,), (0, 1), wide_state),
        "ر⟵ر": (1, (1,), (1,), wide_letter),
        "ح⟶ر": (1, (1,), (1, 0), wide_letter),
    }

    def gauge(lines: Stream, key: str) -> tuple[float, float]:
        target, narrow, wide, width = names[key]
        if narrow == wide:  # معلوماتُ الجار نفسِه: بلا شرطٍ مقابلَ الشرط
            inside = entropy(states if target == 0 else letters) - conditional(
                rows(lines, target, narrow)
            )
            even, odd = halves(lines)
            gained = 0.0
            for taught, asked in ((even, odd), (odd, even)):
                flat = price(
                    [("", two) for _, two in rows(taught, target, narrow)],
                    [("", two) for _, two in rows(asked, target, narrow)],
                    width,
                )
                given_past = price(
                    rows(taught, target, narrow), rows(asked, target, narrow), width
                )
                gained += flat - given_past
            return inside, gained / 2
        return plain(lines, target, narrow, wide), held(
            lines, target, narrow, wide, width
        )

    print("\n— المقاييسُ الأربعةُ أمامًا ومقلوبًا (بت)")
    print("   المقياس     ملحَقٌ أمامًا  محجوزٌ أمامًا  ملحَقٌ مقلوبًا  محجوزٌ مقلوبًا")
    measured: dict[str, tuple[float, float, float, float]] = {}
    for key in names:
        ahead_in, ahead_out = gauge(forward, key)
        back_in, back_out = gauge(backward, key)
        measured[key] = (ahead_in, ahead_out, back_in, back_out)
        print(
            f"   {key:8s}  {ahead_in:+.6f}    {ahead_out:+.6f}"
            f"     {back_in:+.6f}     {back_out:+.6f}"
        )

    print(f"\n— الصفريُّ المُبدَّل: {SHUFFLES} تبديلًا يحفظ الهوامشَ ويهدم الجوار")
    chance = random.Random(SEED)
    flat = [cell for line in forward for cell in line]
    nulls: defaultdict[str, list[float]] = defaultdict(list)
    for _ in range(SHUFFLES):
        chance.shuffle(flat)
        cut = 0
        mixed: Stream = []
        for line in forward:
            mixed.append(flat[cut : cut + len(line)])
            cut += len(line)
        for key in names:
            nulls[key].append(gauge(mixed, key)[1])
    for key in names:
        row = sorted(nulls[key])
        low, high = row[0], row[-1]
        middle = math.fsum(row) / len(row)
        print(
            f"   {key:8s}  وسطٌ {middle:+.6f} | مجالٌ [{low:+.6f} , {high:+.6f}]"
            f" | المقيسُ {measured[key][1]:+.6f}"
        )

    print("\n— الحكم")
    state_h = entropy(states)
    letter_h = entropy(letters)
    to_state = measured["ر⟶ح"][1]
    to_letter = measured["ح⟶ر"][1]
    lead = to_state / state_h - to_letter / letter_h
    print(f"  نصيبُ «ر⟶ح» من H(ح): {to_state / state_h:.6f}")
    print(f"  نصيبُ «ح⟶ر» من H(ر): {to_letter / letter_h:.6f}")
    print(f"  الفرقُ (القيادة): {lead:+.6f}")
    arrow = max(abs(measured[one][1] - measured[one][3]) for one in names)
    print(f"  أقصى |أمامًا − مقلوبًا| محجوزًا: {arrow:.6f}")
    print(f"  «ر⟶ح» أمامًا − مقلوبًا: {measured['ر⟶ح'][1] - measured['ر⟶ح'][3]:+.6f}")
    print(f"  «ح⟵ح» محجوزًا: {measured['ح⟵ح'][1]:.6f}")
    above = min(measured[one][1] - max(nulls[one]) for one in names)
    print(f"  أدنى (المقيس − أعلى الصفريّ): {above:+.6f}")
    print(f"  أدنى مقياسٍ ملحَق: {min(measured[one][0] for one in names):+.6f}")
    print(
        "  أدنى (ملحَق − محجوز): "
        f"{min(measured[one][0] - measured[one][1] for one in names):+.6f}"
    )
    print(f"  أقصى (log₂ التباديل − N·H) بعد ألف = {most_slack:+.6f}")

    print("\n— ما لا يُدَّعى")
    print("  النقلُ ليس السببيّة: لا تدخّلَ في نصٍّ مجمَّد، فلا تُشتَقّ")
    print("  سببيّةٌ من ارتباطٍ مهما بلغ — وهذا مكتوبٌ قبل النظر لا بعده")
    print("  ولا اسمَ بابٍ ولا علامةٍ ولا يونيكود — شريحةٌ ونقطةُ ترميز")
    print(f"  ومن الشرائح: {shown(states.most_common(2)[1][0])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
