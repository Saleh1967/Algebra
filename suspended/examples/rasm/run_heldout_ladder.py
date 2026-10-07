"""السلّمُ محجوزًا — تشغيلُ ختم `455167a5…`.

**الفرقُ عن `run_vowel_ladder.py`**: ذاك يقدّر التوزيعَ الشرطيَّ من المواضع
نفسِها التي يقيس عليها، فينتحل نزولًا كلّما كثرت السياقات. وهذا **يقدّره من
نصفٍ ويقيس على النصف الآخر**، فيعطي ما يتنبّأ به قارئٌ لم يرَ النصّ.

**القراراتُ المختومة**: الأسطرُ الزوجيّةُ سندًا والفرديّةُ قياسًا ثمّ بالعكس
والمتوسّط؛ تنعيمُ لابلاس على أبجديّة حالات السند؛ الارتدادُ إلى الرتبة صفر
لسياقٍ لم يُرَ **مع إعلان نصيبه**؛ الخطأُ المعياريُّ بإعادة معاينة الأسطر
أربعين سحبة؛ وإعادةُ السلّم على **سندٍ مشترك** هو المواضعُ المقروءةُ سياقًا
عند الرتبة الثالثة.
"""

from __future__ import annotations

import argparse
import importlib.util
import math
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[2]
LADDER = REPOSITORY / "examples" / "rasm" / "run_vowel_ladder.py"
ORDERS = (0, 1, 2)
RESAMPLES = 40
SEED = 20260925
CONTEXT_FLOOR = 30
Units = list[tuple[str, str]]


def _ladder() -> object:
    spec = importlib.util.spec_from_file_location("run_vowel_ladder", LADDER)
    if spec is None or spec.loader is None:
        raise RuntimeError("لا قارئَ للسلّم")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def keyed(units: Units, index: int, order: int, with_states: bool) -> tuple[str, ...]:
    """مفتاحُ السياق عند موضعٍ بعينه — كما في الختم الأوّل."""

    window = units[index - order : index + 1]
    key = [letter for letter, _ in window]
    if with_states and order:
        key.extend(state for _, state in window[:-1])
    return tuple(key)


def tabulate(
    lines: list[Units], order: int, with_states: bool
) -> tuple[dict[tuple[str, ...], Counter[str]], Counter[str]]:
    """جدولُ السند: توزيعُ الحالة لكلّ سياق، ومعه توزيعُ الرتبة صفر."""

    table: dict[tuple[str, ...], Counter[str]] = defaultdict(Counter)
    plain: Counter[str] = Counter()
    for units in lines:
        for index in range(order, len(units)):
            table[keyed(units, index, order, with_states)][units[index][1]] += 1
            plain[units[index][1]] += 1
    return (table, plain)


def cross_entropy(
    support: list[Units], measure: list[Units], order: int, with_states: bool
) -> tuple[float, float]:
    """(الإنتروبيا المتقاطعة بتًّا، نصيبُ المرتدّ) بتنعيم لابلاس."""

    table, plain = tabulate(support, order, with_states)
    alphabet = len(plain)
    if not alphabet:
        return (float("nan"), 1.0)
    base = sum(plain.values())
    total = 0
    fallen = 0
    charge = 0.0
    for units in measure:
        for index in range(order, len(units)):
            state = units[index][1]
            counts = table.get(keyed(units, index, order, with_states))
            if counts is None:
                counts, mass = plain, base
                fallen += 1
            else:
                mass = sum(counts.values())
            chance = (counts.get(state, 0) + 1) / (mass + alphabet)
            charge -= math.log2(chance)
            total += 1
    if not total:
        return (float("nan"), 1.0)
    return (charge / total, fallen / total)


def held_out(lines: list[Units], order: int, with_states: bool) -> tuple[float, float]:
    """المتوسّطُ على الاتّجاهين — كلُّ نصفٍ سندًا مرّةً وقياسًا مرّة."""

    even = [one for index, one in enumerate(lines) if index % 2 == 0]
    odd = [one for index, one in enumerate(lines) if index % 2]
    first = cross_entropy(even, odd, order, with_states)
    second = cross_entropy(odd, even, order, with_states)
    return ((first[0] + second[0]) / 2, (first[1] + second[1]) / 2)


def standard_error(lines: list[Units], order: int, with_states: bool) -> float:
    """تمهيدٌ بإعادة معاينة الأسطر — فرقمٌ بلا خطئه إدّعاءُ دقّة."""

    draw = random.Random(SEED)
    spread: list[float] = []
    for _ in range(RESAMPLES):
        sample = [draw.choice(lines) for _ in lines]
        spread.append(held_out(sample, order, with_states)[0])
    mean = math.fsum(spread) / len(spread)
    variance = math.fsum((one - mean) ** 2 for one in spread) / (len(spread) - 1)
    return math.sqrt(variance)


def common_support(lines: list[Units]) -> list[Units]:
    """المواضعُ التي سياقُها من الرتبة الثالثة مقروء — ليُقارَن مثلٌ بمثل."""

    table, _ = tabulate(lines, 3, with_states=False)
    readable = {
        key for key, counts in table.items() if sum(counts.values()) >= CONTEXT_FLOOR
    }
    kept: list[Units] = []
    for units in lines:
        window = [
            index
            for index in range(3, len(units))
            if keyed(units, index, 3, False) in readable
        ]
        kept.extend([units[index - 3 : index + 1] for index in window])
    return kept


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", type=Path, required=True)
    parser.add_argument("--errors", action="store_true")
    given = parser.parse_args()

    ladder = _ladder()
    lines = ladder.lines_of_units(given.text.read_text(encoding="utf-8"))  # type: ignore[attr-defined]
    print(f"أسطر: {len(lines)} | مواضع: {sum(len(one) for one in lines)}")
    print("\nالرتبة | سلّم |  مُبلَّغة | محجوزة | نصيبُ المرتدّ")
    for order in ORDERS:
        for name, with_states in (("رسم", False), ("فكّ", True)):
            inside = ladder.ladder_step(  # type: ignore[attr-defined]
                ladder.contexts(lines, order, with_states)  # type: ignore[attr-defined]
            )[0]
            outside, fallen = held_out(lines, order, with_states)
            row = f"{inside:7.4f} | {outside:6.4f} | {fallen:12.4f}"
            print(f"   {order}   | {name:>3} | {row}")

    shared = common_support(lines)
    print("\nعلى السند المشترك (سياقُ الرتبة ٣ مقروء):")
    print(f"  مواضع: {len(shared)}")
    for order in ORDERS:
        step = ladder.ladder_step(  # type: ignore[attr-defined]
            ladder.contexts(shared, order, with_states=False)  # type: ignore[attr-defined]
        )
        print(f"  الرتبة {order}: h = {step[0]:.4f} | نصيبُ المقروء {step[2]:.4f}")

    if given.errors:
        for name, with_states in (("رسم", False), ("فكّ", True)):
            error = standard_error(lines, 2, with_states)
            print(f"\nالخطأُ المعياريُّ عند الرتبة ٢ ({name}): {error:.4f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
