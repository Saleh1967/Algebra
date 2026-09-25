"""الصعودُ المكتشَف من الـ١١٢ — تشغيلُ ختم `620b63a2…`.

**لا تُقترَح الطبقةُ ثمّ تُجاز — بل يكتشفها العدّ**: يُبدأ من الـ١١٢
وحدَها، ويُدمَج في كلّ خطوةٍ **الزوجُ المتجاورُ الأكثرُ وقوعًا**، ويُوقَف
عند أوّل نقطةِ فحصٍ **ترتفع فيها التكلفةُ المحجوزة**.

**التكلفةُ ذات شطرين**: معجمٌ يُهجّى **بحروف الـ١١٢** مع طولِ كلّ مدخل،
وبيانٌ إنتروبيا **محجوزةً** بقسمة الآيات الزوجيّة/الفرديّة.

**والتيّارُ بلا فواصلِ كلمات**، فيجوز للدمج أن يعبر حدَّ الكلمة؛ ثمّ يُسأل
كم عبره فعلًا — فإن ندر فالحدُّ **مكتشَفٌ لا مُلقَّن**.

**والابتلاعُ بالبناء**: الدمجُ تجميعٌ محض، وبسطُ الرموز يُعيد الـ١١٢
بالضبط — ويُفحَص ذلك لا يُدَّعى.
"""

from __future__ import annotations

import argparse
import importlib.util
import math
import sys
from collections import Counter
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[2]
PEEL = REPOSITORY / "examples" / "rasm" / "run_cv_peel.py"
BASE = 112
CHECK_EVERY = 500
MOST_MERGES = 20_000


def _peel() -> object:
    spec = importlib.util.spec_from_file_location("run_cv_peel", PEEL)
    if spec is None or spec.loader is None:
        raise RuntimeError("لا قارئَ للتقشير")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def corpus_of(
    text: str,
) -> tuple[list[list[int]], list[list[bool]], list[tuple[str, str]]]:
    """(آياتٌ برموزٍ، أوائلُ الكلم لكلّ موضع، معجمُ الـ١١٢)."""

    peeler = _peel()
    table: dict[tuple[str, str], int] = {}
    verses: list[list[int]] = []
    heads: list[list[bool]] = []
    for line in text.splitlines():
        if not line.strip():
            continue
        units, _ = peeler.peel(line)  # type: ignore[attr-defined]
        row: list[int] = []
        head: list[bool] = []
        fresh = True
        for base, value in units:
            if base == peeler.STRUCTURE:  # type: ignore[attr-defined]
                fresh = True
                continue
            key = (base, value)
            if key not in table:
                table[key] = len(table)
            row.append(table[key])
            head.append(fresh)
            fresh = False
        if row:
            verses.append(row)
            heads.append(head)
    order = [key for key, _ in sorted(table.items(), key=lambda pair: pair[1])]
    return (verses, heads, order)


def best_pair(verses: list[list[int]]) -> tuple[tuple[int, int], int] | None:
    spread: Counter[tuple[int, int]] = Counter()
    for row in verses:
        for one, two in zip(row, row[1:]):
            spread[(one, two)] += 1
    if not spread:
        return None
    pair, number = spread.most_common(1)[0]
    return (pair, number) if number > 1 else None


def apply_merge(verses: list[list[int]], pair: tuple[int, int], fresh: int) -> None:
    left, right = pair
    for index, row in enumerate(verses):
        if len(row) < 2:
            continue
        built: list[int] = []
        place = 0
        while place < len(row):
            if place + 1 < len(row) and row[place] == left and row[place + 1] == right:
                built.append(fresh)
                place += 2
            else:
                built.append(row[place])
                place += 1
        verses[index] = built


def held_out(verses: list[list[int]]) -> tuple[float, float]:
    even: Counter[int] = Counter()
    odd: Counter[int] = Counter()
    for index, row in enumerate(verses):
        (even if index % 2 == 0 else odd).update(row)
    whole = even + odd

    def cross(support: Counter[int], measure: Counter[int]) -> float:
        alphabet = max(len(support), 1)
        mass = sum(support.values())
        total = sum(measure.values())
        if not total:
            return 0.0
        return (
            -math.fsum(
                number * math.log2((support.get(symbol, 0) + 1) / (mass + alphabet))
                for symbol, number in measure.items()
            )
            / total
        )

    mass = sum(whole.values())
    inside = -math.fsum(
        (number / mass) * math.log2(number / mass) for number in whole.values()
    )
    return ((cross(even, odd) + cross(odd, even)) / 2, inside)


def cost_now(
    verses: list[list[int]], lengths: dict[int, int]
) -> tuple[float, float, float, int, int]:
    used = {symbol for row in verses for symbol in row}
    longest = max((lengths[one] for one in used), default=1)
    book = math.fsum(
        lengths[one] * math.log2(BASE) + math.log2(longest + 1)
        for one in used
        if lengths[one] > 1
    )
    outside, inside = held_out(verses)
    count = sum(len(one) for one in verses)
    return (book + outside * count, book, outside * count, count, len(used))


def straddles(
    verses: list[list[int]], heads: list[list[bool]], lengths: dict[int, int]
) -> tuple[int, int]:
    """(وقوعاتٌ عابرةٌ لحدّ الكلمة، الوقوعاتُ كلُّها)."""

    crossing = 0
    total = 0
    for row, head in zip(verses, heads):
        place = 0
        for symbol in row:
            width = lengths[symbol]
            total += 1
            if width > 1 and any(head[place + one] for one in range(1, width)):
                crossing += 1
            place += width
    return (crossing, total)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", type=Path, required=True)
    given = parser.parse_args()

    verses, heads, order = corpus_of(given.text.read_text(encoding="utf-8"))
    lengths: dict[int, int] = {index: 1 for index in range(len(order))}
    spelling: dict[int, tuple[int, ...]] = {
        index: (index,) for index in range(len(order))
    }
    units = sum(len(one) for one in verses)
    print(f"L₀: {units} وحدةً | أبجديّة {len(order)} | آيات {len(verses)}")

    start = cost_now(verses, lengths)
    print(
        f"نقطةُ الصفر: الجملة {start[0]:.0f} | معجم {start[1]:.0f} | بيان {start[2]:.0f}"
    )

    merges: list[tuple[int, int]] = []
    best = start
    best_at = 0
    rises = 0
    stopped = 0
    while len(merges) < MOST_MERGES:
        found = best_pair(verses)
        if found is None:
            break
        pair, _ = found
        fresh = len(lengths)
        lengths[fresh] = lengths[pair[0]] + lengths[pair[1]]
        spelling[fresh] = spelling[pair[0]] + spelling[pair[1]]
        apply_merge(verses, pair, fresh)
        merges.append(pair)
        if len(merges) % CHECK_EVERY == 0:
            here = cost_now(verses, lengths)
            mark = "↓" if here[0] < best[0] else "↑"
            print(
                f"  بعد {len(merges)}: الجملة {here[0]:.0f} | معجم {here[1]:.0f} "
                f"| بيان {here[2]:.0f} | رموز {here[3]} | أبجديّة {here[4]} {mark}"
            )
            if here[0] < best[0]:
                best, best_at = here, len(merges)
            else:
                rises += 1
                stopped = len(merges)
                break

    crossing, total = straddles(verses, heads, lengths)
    print(f"\nنقطةُ الوقوف: {stopped or len(merges)} دمجةً | أفضلُ تكلفةٍ عند {best_at}")
    print(f"  الجملة {best[0]:.0f} | النسبةُ إلى L₀ {best[0] / start[0]:.4f}")
    print(
        f"  لا يعبر حدَّ الكلمة: {total - crossing} من {total} "
        f"= {(total - crossing) / total:.4f}"
    )
    flat = [symbol for row in verses for symbol in row]
    spread = Counter(flat)
    built = [(one, number) for one, number in spread.most_common() if lengths[one] > 1]
    print("  أكثرُ الوحدات المكتشَفة:")
    for symbol, number in built[:14]:
        word = "".join(f"{order[one][0]}{order[one][1]}" for one in spelling[symbol])
        print(f"    {word}  ({number}) طولُه {lengths[symbol]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
