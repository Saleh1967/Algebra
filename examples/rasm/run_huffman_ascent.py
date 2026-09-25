"""الصعودُ المكتشَف ببيانٍ هوفمانيّ — تشغيلُ ختم `34133d54…`.

**الفرقُ عن `620b63a2…`**: شطرُ البيان كان **إنتروبيا × عدد**، والإنتروبيا
**حدٌّ أدنى لا تبلغه شفرةٌ رمزًا رمزًا**. فيُستبدَل بـ**طولِ شفرة هوفمان
الفعليّ** — وهو الجشعُ **المبرهَن**: «ادمج أقلَّ رمزين احتمالًا، وكرّر»،
ويلزم منه `H ≤ L < H + 1`.

**فيصير الشطران معًا**: القسمةُ جشعٌ **غيرُ مبرهَن** (الزوجُ الأكثرُ وقوعًا)
⟹ حدٌّ أعلى؛ والترميزُ جشعٌ **مبرهَن** ⟹ أمثلُ رمزًا رمزًا.

**والآلةُ مشتركةٌ** مع `run_discovered_ascent.py` — القشرُ والدمجُ والمدى —
فلا يُعاد بناؤها ولا تتفرّق النتيجتان في تفصيلٍ غيرِ مقصود.
"""

from __future__ import annotations

import argparse
import heapq
import importlib.util
import math
import sys
from collections import Counter
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[2]
ASCENT = REPOSITORY / "examples" / "rasm" / "run_discovered_ascent.py"
BASE = 112
CHECK_EVERY = 500
MOST_MERGES = 20_000


def _ascent() -> object:
    spec = importlib.util.spec_from_file_location("run_discovered_ascent", ASCENT)
    if spec is None or spec.loader is None:
        raise RuntimeError("لا قارئَ للصعود")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def huffman_lengths(counts: Counter[int]) -> dict[int, int]:
    """أطوالُ شفرة هوفمان — الجشعُ المبرهَن: أقلُّ رمزين احتمالًا يُدمَجان."""

    if not counts:
        return {}
    if len(counts) == 1:
        return {symbol: 1 for symbol in counts}
    depth: dict[int, int] = {symbol: 0 for symbol in counts}
    members: dict[int, list[int]] = {symbol: [symbol] for symbol in counts}
    heap: list[tuple[int, int]] = [
        (number, symbol) for symbol, number in counts.items()
    ]
    heapq.heapify(heap)
    fresh = -1
    while len(heap) > 1:
        first_mass, first = heapq.heappop(heap)
        second_mass, second = heapq.heappop(heap)
        joined = members.pop(first) + members.pop(second)
        for symbol in joined:
            depth[symbol] += 1
        members[fresh] = joined
        heapq.heappush(heap, (first_mass + second_mass, fresh))
        fresh -= 1
    return depth


def entropy(counts: Counter[int]) -> float:
    mass = sum(counts.values())
    if not mass:
        return 0.0
    return -math.fsum(
        (number / mass) * math.log2(number / mass) for number in counts.values()
    )


def coded(support: Counter[int], measure: Counter[int]) -> tuple[float, float]:
    """(متوسّطُ طولِ الشفرة على المقيس، نصيبُ الرمز غيرِ المرئيّ)."""

    lengths = huffman_lengths(support)
    if not lengths:
        return (0.0, 1.0)
    longest = max(lengths.values())
    total = sum(measure.values())
    if not total:
        return (0.0, 0.0)
    charge = 0
    missing = 0
    for symbol, number in measure.items():
        width = lengths.get(symbol)
        if width is None:
            width = longest + 1
            missing += number
        charge += width * number
    return (charge / total, missing / total)


def held_out(verses: list[list[int]]) -> tuple[float, float, float]:
    """(الطولُ محجوزًا، نصيبُ المرتدّ، الطولُ ملحَقًا)."""

    even: Counter[int] = Counter()
    odd: Counter[int] = Counter()
    for index, row in enumerate(verses):
        (even if index % 2 == 0 else odd).update(row)
    whole = even + odd
    first = coded(even, odd)
    second = coded(odd, even)
    inside = coded(whole, whole)
    return ((first[0] + second[0]) / 2, (first[1] + second[1]) / 2, inside[0])


def cost_now(
    verses: list[list[int]], lengths: dict[int, int]
) -> tuple[float, float, float, int, int, float, float, float]:
    """(الجملة، المعجم، البيان، العدد، الأبجديّة، الملحَقة، المرتدّ، H)."""

    used = {symbol for row in verses for symbol in row}
    longest = max((lengths[one] for one in used), default=1)
    book = math.fsum(
        lengths[one] * math.log2(BASE) + math.log2(longest + 1)
        for one in used
        if lengths[one] > 1
    )
    outside, missing, inside = held_out(verses)
    count = sum(len(one) for one in verses)
    spread: Counter[int] = Counter(one for row in verses for one in row)
    return (
        book + outside * count,
        book,
        outside * count,
        count,
        len(used),
        book + inside * count,
        missing,
        entropy(spread),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", type=Path, required=True)
    given = parser.parse_args()

    ascent = _ascent()
    verses, heads, order, lines, reach = ascent.corpus_of(  # type: ignore[attr-defined]
        given.text.read_text(encoding="utf-8")
    )
    widths: dict[int, int] = {index: 1 for index in range(len(order))}
    spelling: dict[int, tuple[int, ...]] = {
        index: (index,) for index in range(len(order))
    }
    units = sum(len(one) for one in verses)
    print(f"L₀: {units} وحدةً | أبجديّة {len(order)}")
    start = cost_now(verses, widths)
    print(
        f"نقطةُ الصفر: الجملة {start[0]:.0f} | بيانٌ هوفمانيّ {start[2]:.0f} "
        f"| H {start[7]:.4f} | الفرقُ للرمز {start[2] / start[3] - start[7]:+.4f} "
        f"| ملحَقة {start[5]:.0f}"
    )

    merges = 0
    best = start
    best_at = 0
    keep = [list(row) for row in verses]
    stopped = 0
    while merges < MOST_MERGES:
        found = ascent.best_pair(verses)  # type: ignore[attr-defined]
        if found is None:
            break
        pair, _number = found
        fresh = len(widths)
        widths[fresh] = widths[pair[0]] + widths[pair[1]]
        spelling[fresh] = spelling[pair[0]] + spelling[pair[1]]
        ascent.apply_merge(verses, pair, fresh)  # type: ignore[attr-defined]
        merges += 1
        if merges % CHECK_EVERY == 0:
            here = cost_now(verses, widths)
            gap = here[2] / here[3] - here[7]
            mark = "↓" if here[0] < best[0] else "↑"
            print(
                f"  بعد {merges}: الجملة {here[0]:.0f} | معجم {here[1]:.0f} "
                f"| بيان {here[2]:.0f} | رموز {here[3]} | أبجديّة {here[4]} "
                f"| H {here[7]:.4f} | L−H {gap:+.4f} | مرتدّ {here[6]:.4f} "
                f"| ملحَقة {here[5]:.0f} | فرق {here[0] - here[5]:+.0f} {mark}"
            )
            if here[0] < best[0]:
                best, best_at = here, merges
                keep = [list(row) for row in verses]
            else:
                stopped = merges
                break

    crossing, total = ascent.straddles(keep, heads, widths)  # type: ignore[attr-defined]
    print(f"\nنقطةُ الوقوف: {stopped or merges} | أفضلُ تكلفةٍ عند {best_at}")
    print(f"  الجملة {best[0]:.0f} | النسبةُ إلى L₀ {best[0] / start[0]:.4f}")
    clean = total - crossing
    print(f"  لا يعبر الفراغَ: {clean} من {total} = {clean / total:.4f}")
    spread = Counter(one for row in keep for one in row)
    kinds = Counter(widths[one] for one in spread)
    mass: Counter[int] = Counter()
    for symbol, number in spread.items():
        mass[widths[symbol]] += number
    print("\n  المجموعةُ المولَّدةُ مقسومةً بالعَرض:")
    for width in sorted(kinds):
        print(
            f"    عَرضُ {width}: رموزٌ {kinds[width]} | وقوعاتٌ {mass[width]} "
            f"| نصيبٌ {mass[width] / sum(mass.values()):.4f}"
        )
    print(f"    الجملة: رموزٌ {sum(kinds.values())} | وقوعاتٌ {sum(mass.values())}")
    built = [one for one, _ in spread.most_common() if widths[one] > 1]
    shown = ascent.shapes_of(keep, lines, reach, widths, built[:14])  # type: ignore[attr-defined]
    print("\n  أكثرُ الرموز وقوعًا (ببايتاتها):")
    for symbol in built[:14]:
        print(
            f"    {shown.get(symbol, '—')}  ({spread[symbol]}) وحداتُه {widths[symbol]}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
