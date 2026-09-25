"""أرضيّةُ الرسم — تشغيلُ ختم `f43b9095…`.

**المبرهنة**: لأيّ مُرمِّزٍ لا يرى إلّا رسمَ الكلمة W، متوسّطُ طولِ الشفرة
لتسلسل الحالات S على هذه المدوّنة **لا ينزل عن H(S | W)** — بحدّ شانون
لترميز المصدر؛ وأدنى ما يبلغه هو H(S | W) بعينها. وعلى مجمَّدٍ متناهٍ
المقدارُ **يُحسَب بالضبط**، فالحدُّ لازمٌ لا مقدَّر.

**قيدُها المعلن**: قارئُ **الكلمة وحدَها**. ومَن رأى ما حولَها قد ينزل
عنها، فالأرضيّةُ أرضيّةُ صنفٍ من القرّاء لا أرضيّةُ كلّ قارئ.

**وثلاثةٌ تُعرَض معها**: التفكيكُ التامُّ لـΔضبط على قسمةٍ دالّةٍ في الحرف
(إعادةُ تجميعٍ لا تقريب)؛ ونسخةٌ **محجوزةٌ** من الأرضيّة؛ وشواهدُ الالتباس
**بأسمائها** — فالعددُ وحدَه لا يُري ما الذي التبس.
"""

from __future__ import annotations

import argparse
import importlib.util
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[2]
AUDIT = REPOSITORY / "examples" / "rasm" / "run_encoding_audit.py"
MADD = "اوي"
MARKUP = "<sel>"
Word = tuple[tuple[str, ...], tuple[str, ...]]


def _audit() -> object:
    spec = importlib.util.spec_from_file_location("run_encoding_audit", AUDIT)
    if spec is None or spec.loader is None:
        raise RuntimeError("لا قارئَ للمواصفة")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def words(text: str) -> list[Word]:
    """كلُّ كلمةٍ زوجًا: رسمُها وتسلسلُ حالاتها."""

    audit = _audit()
    found: list[Word] = []
    for token in text.replace(MARKUP, " ").split():
        units = audit.rasm_units(token)  # type: ignore[attr-defined]
        if units:
            found.append(
                (
                    tuple(letter for letter, _ in units),
                    tuple(state for _, state in units),
                )
            )
    return found


def entropy(counts: Counter[tuple[str, ...]]) -> float:
    total = sum(counts.values())
    if not total:
        return 0.0
    return -math.fsum(
        (number / total) * math.log2(number / total) for number in counts.values()
    )


def floor_of(seen: list[Word]) -> tuple[float, int, int, int]:
    """(الأرضيّةُ بتًّا للموضع، البتّاتُ جملةً، المواضعُ، الوقوعاتُ الملتبسة)."""

    table: dict[tuple[str, ...], Counter[tuple[str, ...]]] = defaultdict(Counter)
    for rasm, states in seen:
        table[rasm][states] += 1
    charge = 0.0
    ambiguous = 0
    positions = 0
    for rasm, spread in table.items():
        mass = sum(spread.values())
        charge += mass * entropy(spread)
        positions += mass * len(rasm)
        if len(spread) > 1:
            ambiguous += mass
    return (charge / positions, int(charge), positions, ambiguous)


def held_out_floor(seen: list[Word]) -> tuple[float, float]:
    """(المحجوزةُ، نصيبُ المرتدّ) — ورقمٌ بلا نصيبِ مرتدِّه غيرُ مقروء."""

    even = [one for index, one in enumerate(seen) if index % 2 == 0]
    odd = [one for index, one in enumerate(seen) if index % 2]
    first = _cross(even, odd)
    second = _cross(odd, even)
    return ((first[0] + second[0]) / 2, (first[1] + second[1]) / 2)


def _cross(support: list[Word], measure: list[Word]) -> tuple[float, float]:
    table: dict[tuple[str, ...], Counter[tuple[str, ...]]] = defaultdict(Counter)
    shapes: set[tuple[str, ...]] = set()
    for rasm, states in support:
        table[rasm][states] += 1
        shapes.add(states)
    alphabet = max(len(shapes), 1)
    charge = 0.0
    positions = 0
    fallen = 0
    for rasm, states in measure:
        spread = table.get(rasm)
        if spread is None:
            chance = 1 / alphabet
            fallen += 1
        else:
            chance = (spread.get(states, 0) + 1) / (sum(spread.values()) + alphabet)
        charge -= math.log2(chance)
        positions += len(rasm)
    return (charge / positions, fallen / len(measure))


def decompose(text: str) -> tuple[float, dict[str, tuple[float, float]]]:
    """H(S|L) وتفكيكُها على قسمةٍ دالّةٍ في الحرف — إعادةُ تجميعٍ لا تقريب."""

    audit = _audit()
    units = audit.rasm_units(text.replace(MARKUP, " "))  # type: ignore[attr-defined]
    by_letter: dict[str, Counter[str]] = defaultdict(Counter)
    for letter, state in units:
        by_letter[letter][state] += 1
    total = len(units)
    direct = math.fsum(
        (sum(counts.values()) / total)
        * -math.fsum(
            (number / sum(counts.values())) * math.log2(number / sum(counts.values()))
            for number in counts.values()
        )
        for counts in by_letter.values()
    )
    parts: dict[str, tuple[float, float]] = {}
    for name, members in (
        ("مدّ (ا و ي)", set(MADD)),
        ("لام", {"ل"}),
        ("نون", {"ن"}),
        ("سائرُ الحروف", set(by_letter) - set(MADD) - {"ل", "ن"}),
    ):
        mass = sum(sum(by_letter[one].values()) for one in members if one in by_letter)
        share = mass / total
        inside = (
            math.fsum(
                (sum(by_letter[one].values()) / mass)
                * -math.fsum(
                    (number / sum(by_letter[one].values()))
                    * math.log2(number / sum(by_letter[one].values()))
                    for number in by_letter[one].values()
                )
                for one in members
                if one in by_letter
            )
            if mass
            else 0.0
        )
        parts[name] = (share, inside)
    return (direct, parts)


def witnesses(seen: list[Word], limit: int = 6) -> list[tuple[str, int, int]]:
    """أكثرُ الرسوم التباسًا — بأسمائها لا بعددها."""

    table: dict[tuple[str, ...], Counter[tuple[str, ...]]] = defaultdict(Counter)
    for rasm, states in seen:
        table[rasm][states] += 1
    ranked = sorted(
        ((rasm, spread) for rasm, spread in table.items() if len(spread) > 1),
        key=lambda pair: -sum(pair[1].values()) * (len(pair[1]) - 1),
    )
    return [
        ("".join(rasm), len(spread), sum(spread.values()))
        for rasm, spread in ranked[:limit]
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", type=Path, required=True)
    given = parser.parse_args()

    text = given.text.read_text(encoding="utf-8")
    seen = words(text)
    level, bits, positions, ambiguous = floor_of(seen)
    print(f"كلمات: {len(seen)} | مواضعُ الرسم: {positions}")
    print(f"**أرضيّةُ الرسم H(S|W)**: {level:.4f} بت/موضع ({bits} بتًّا جملةً)")
    outside, fallen = held_out_floor(seen)
    print(f"محجوزةً: {outside:.4f} | نصيبُ الرسمِ غيرِ المرئيّ: {fallen:.4f}")
    print(f"وقوعاتٌ ملتبسةٌ رسمًا: {ambiguous} ({ambiguous / len(seen):.4f})")

    direct, parts = decompose(text)
    rebuilt = math.fsum(share * inside for share, inside in parts.values())
    print(f"\nΔضبط = H(S|L) = {direct:.4f} | التفكيكُ مجموعًا = {rebuilt:.4f}")
    for name, (share, inside) in parts.items():
        print(f"  {name:>16}: نصيبٌ {share:.4f} × h {inside:.4f} = {share * inside:.4f}")

    print("\nشواهدُ الالتباس (رسمٌ | ضبطاتٌ | وقوعات):")
    for rasm, shapes, mass in witnesses(seen):
        print(f"  {rasm} | {shapes} | {mass}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
