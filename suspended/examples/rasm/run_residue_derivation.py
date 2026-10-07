"""إعادةُ بناء البقايا من تيّار الـ١١٢ — تشغيلُ ختم `92b81796…`.

**السؤال**: أفي البقايا خبرٌ مستقلٌّ عن الـ١١٢، أم هي **صدًى** له؟ فإن كانت
صدًى نزلت بتّاتُها كلّما اتّسع ما يُقرأ من التيّار، وما بقي بعد ذلك **هو
الإفادةُ الخالصة**.

**السياقُ متناظر**: `k` وحدةً عن اليمين و`k` عن الشمال، داخلَ الآية لا
يعبرها — لأنّ فاكَّ الشفرة يملك التيّارَ كلَّه، قبلَ الموضع وبعدَه.

**وكلُّ رقمٍ محجوز**: الآياتُ الزوجيّةُ سندًا والفرديّةُ قياسًا ثمّ بالعكس،
بتنعيم لابلاس **على أبجديّة القناة وحدَها** — وهو تصحيحُ العطل الذي أفسد
قياسَ الأرضيّة المحجوزة في `f43b9095…`، إذ وُزِّعت الكتلةُ هناك على ٣٬٩٠٦
شكلًا أكثرُها مستحيل.
"""

from __future__ import annotations

import argparse
import importlib.util
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[2]
PEEL = REPOSITORY / "examples" / "rasm" / "run_cv_peel.py"
CHANNELS = ("حامل", "مربوطة", "سكون", "تنوين", "شدّة")
ORDERS = (0, 1, 2, 3)


def _peel() -> object:
    spec = importlib.util.spec_from_file_location("run_cv_peel", PEEL)
    if spec is None or spec.loader is None:
        raise RuntimeError("لا قارئَ للتقشير")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def verses(text: str) -> list[tuple[list[tuple[str, str]], list[dict[str, str]]]]:
    """كلُّ آيةٍ مقشَّرةً وحدَها — فالسياقُ لا يعبر الآية."""

    peeler = _peel()
    found = []
    for line in text.splitlines():
        if line.strip():
            found.append(peeler.peel(line))  # type: ignore[attr-defined]
    return found


def decisions(
    verse: tuple[list[tuple[str, str]], list[dict[str, str]]], key: str
) -> list[tuple[int, str]]:
    peeler = _peel()
    return peeler.sites(verse[0], verse[1], key)  # type: ignore[attr-defined,no-any-return]


def window(units: list[tuple[str, str]], place: int, order: int) -> tuple[str, ...]:
    """سياقٌ متناظرٌ من وحدات CV — والحافّةُ تُملأ بعلامةِ طرف."""

    edge = ("^", "^")
    picked = [
        units[one] if 0 <= one < len(units) else edge
        for one in range(place - order, place + order + 1)
    ]
    return tuple(f"{base}{value}" for base, value in picked)


def cross(
    support: list[tuple[list[tuple[str, str]], list[dict[str, str]]]],
    measure: list[tuple[list[tuple[str, str]], list[dict[str, str]]]],
    key: str,
    order: int,
) -> tuple[float, float, int]:
    """(الإنتروبيا المتقاطعة، نصيبُ المرتدّ، عددُ المواضع)."""

    table: dict[tuple[str, ...], Counter[str]] = defaultdict(Counter)
    plain: Counter[str] = Counter()
    for verse in support:
        for place, value in decisions(verse, key):
            table[window(verse[0], place, order)][value] += 1
            plain[value] += 1
    alphabet = len(plain)
    if not alphabet:
        return (0.0, 0.0, 0)
    base = sum(plain.values())
    charge = 0.0
    total = 0
    fallen = 0
    for verse in measure:
        for place, value in decisions(verse, key):
            counts = table.get(window(verse[0], place, order))
            if counts is None:
                counts, mass = plain, base
                fallen += 1
            else:
                mass = sum(counts.values())
            charge -= math.log2((counts.get(value, 0) + 1) / (mass + alphabet))
            total += 1
    if not total:
        return (0.0, 0.0, 0)
    return (charge / total, fallen / total, total)


def held_out(
    corpus: list[tuple[list[tuple[str, str]], list[dict[str, str]]]],
    key: str,
    order: int,
) -> tuple[float, float, int]:
    even = [one for index, one in enumerate(corpus) if index % 2 == 0]
    odd = [one for index, one in enumerate(corpus) if index % 2]
    first = cross(even, odd, key, order)
    second = cross(odd, even, key, order)
    return (
        (first[0] + second[0]) / 2,
        (first[1] + second[1]) / 2,
        first[2] + second[2],
    )


def inside(
    corpus: list[tuple[list[tuple[str, str]], list[dict[str, str]]]],
    key: str,
    order: int,
) -> float:
    """الملحَقةُ — للمقارنة باتّجاه الانتحال وحدَه."""

    table: dict[tuple[str, ...], Counter[str]] = defaultdict(Counter)
    for verse in corpus:
        for place, value in decisions(verse, key):
            table[window(verse[0], place, order)][value] += 1
    mass = sum(sum(one.values()) for one in table.values())
    return math.fsum(sum(one.values()) / mass * _entropy(one) for one in table.values())


def _entropy(counts: Counter[str]) -> float:
    total = sum(counts.values())
    if not total:
        return 0.0
    return -math.fsum(
        (number / total) * math.log2(number / total) for number in counts.values()
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", type=Path, required=True)
    given = parser.parse_args()

    corpus = verses(given.text.read_text(encoding="utf-8"))
    print(f"آيات: {len(corpus)}")
    print("\nالقناة | رتبة | مواضع | ملحَقة | محجوزة | مرتدّ | بتّات")
    best: dict[str, tuple[int, float, int]] = {}
    for key in CHANNELS:
        for order in ORDERS:
            outside, fallen, places = held_out(corpus, key, order)
            plugged = inside(corpus, key, order)
            bits = outside * places
            if key not in best or outside < best[key][1]:
                best[key] = (order, outside, places)
            print(
                f"  {key} | {order} | {places} | {plugged:.4f} | {outside:.4f} "
                f"| {fallen:.4f} | {bits:.0f}"
            )
    total = sum(value * places for _, value, places in best.values())
    print("\nأفضلُ رتبةٍ لكلّ قناة:")
    for key, (order, value, places) in best.items():
        print(f"  {key}: رتبة {order} | {value:.4f} بت | {value * places:.0f} بتًّا")
    print(f"\nمجموعُ البقايا عند أفضل رتبة: {total:.0f} بتًّا (والمنشورُ ٩٣٬٤٥٣)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
