"""ستيرلنغ مع الجشع وقت الحساب — تشغيلُ ختم `62495099…`.

**ذراعان على مقامين**: الجشعُ يسجّل **بالإنتروبيا** مرّةً و**بعدد التباديل
المتمايزة** مرّة. **والمقيسُ أثرُ المعيار على الاختيار**، لا اللغةُ ولا
المادّة.
"""

from __future__ import annotations

import argparse
import itertools
import math
import re
import sys
from pathlib import Path

EASTERN = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")
Block = tuple[int, ...]
"""كتلةٌ: أعدادُ أصنافها — والمجموعُ حجمُها."""


def western(one: str) -> str:
    return one.translate(EASTERN)


def entropy_cost(block: Block) -> float:
    """ثمنُ الكتلة بالإنتروبيا: `n·H` — وهو **حدُّ ستيرلنغ** لا العدد."""

    total = sum(block)
    if total == 0:
        return 0.0
    found = -math.fsum(one * math.log2(one / total) for one in block if one)
    return 0.0 if found == 0.0 else found


def permutation_cost(block: Block) -> float:
    """ثمنُ الكتلة بالتباديل: `log₂ n! − Σ log₂ nᵢ!` — العددُ نفسُه."""

    total = sum(block)
    if total == 0:
        return 0.0
    return (
        math.lgamma(total + 1) - math.fsum(math.lgamma(one + 1) for one in block)
    ) / math.log(2)


COSTS = {"إنتروبيا": entropy_cost, "تباديل": permutation_cost}


def subsets(whole: int, parts: int) -> int:
    """رقمُ ستيرلنغ من النوع الثاني `S(n,k)` — بقاعدة النمط لا بجدول.

    `S(n,k) = k·S(n−1,k) + S(n−1,k−1)`: إمّا في صندوقٍ قائمٍ أو في جديد.
    وهو **عددُ قسمات** مجموعةٍ من `n` خانةً إلى `k` كتلةً غيرِ فارغة —
    أي **سَعةُ الفضاء الذي لم يبحثه الجشع** عند تلك الدرجة.
    """

    if parts < 0 or parts > whole:
        return 0
    if whole == parts:
        return 1
    if parts == 0:
        return 0
    return parts * subsets(whole - 1, parts) + subsets(whole - 1, parts - 1)


def merged(cells: list[Block], chosen: frozenset[int]) -> Block:
    return tuple(
        sum(cells[index][side] for index in chosen) for side in range(len(cells[0]))
    )


def spend(
    cells: list[Block], names: list[str], how: str
) -> tuple[list[tuple[str, float, int]], float]:
    """يصعّد بتّةً بتّة بالمعيار المعطى؛ ويردّ الدرجاتِ ومجموعَ الكسب."""

    cost = COSTS[how]
    groups: list[frozenset[int]] = [frozenset(range(len(cells)))]
    here = cost(merged(cells, groups[0]))
    asked_before: list[frozenset[int]] = []
    steps: list[tuple[str, float, int]] = []
    while len(asked_before) < len(cells):
        best: tuple[float, frozenset[int], list[frozenset[int]]] | None = None
        for size in range(1, len(cells)):
            for pick in itertools.combinations(range(len(cells)), size):
                asked = frozenset(pick)
                whole = frozenset(range(len(cells)))
                if asked in asked_before or whole - asked in asked_before:
                    continue
                fresh = [
                    part
                    for group in groups
                    for part in (group & asked, group - asked)
                    if part
                ]
                after = math.fsum(cost(merged(cells, one)) for one in fresh)
                if best is None or here - after > best[0]:
                    best = (here - after, asked, fresh)
        if best is None or best[0] <= 1e-12:
            break
        gain, asked, fresh = best
        groups = fresh
        asked_before.append(asked)
        here -= gain
        steps.append(
            (
                " و".join(names[index] for index in sorted(asked)),
                gain,
                len(groups),
            )
        )
    return steps, math.fsum(one for _, one, _ in steps)


def blocks_of(cells: list[Block], names: list[str], how: str) -> list[Block]:
    """كتلُ السلّم عند وقوفه — لحساب الفجوات."""

    cost = COSTS[how]
    groups: list[frozenset[int]] = [frozenset(range(len(cells)))]
    here = cost(merged(cells, groups[0]))
    asked_before: list[frozenset[int]] = []
    while len(asked_before) < len(cells):
        best: tuple[float, frozenset[int], list[frozenset[int]]] | None = None
        for size in range(1, len(cells)):
            for pick in itertools.combinations(range(len(cells)), size):
                asked = frozenset(pick)
                whole = frozenset(range(len(cells)))
                if asked in asked_before or whole - asked in asked_before:
                    continue
                fresh = [
                    part
                    for group in groups
                    for part in (group & asked, group - asked)
                    if part
                ]
                after = math.fsum(cost(merged(cells, one)) for one in fresh)
                if best is None or here - after > best[0]:
                    best = (here - after, asked, fresh)
        if best is None or best[0] <= 1e-12:
            break
        here -= best[0]
        groups = best[2]
        asked_before.append(best[1])
    return [merged(cells, one) for one in groups]


def read_hasr(deposit: Path) -> tuple[list[Block], list[str], int]:
    text = deposit.read_text(encoding="utf-8")
    (whole,) = re.findall(r"من \*\*([٠-٩]+)\*\*", text)
    total = int(western(whole))
    (row,) = re.findall(r"م٢ حالةُ التالي \| [٠٫\d]+ \| (.+?) \|", text)
    cells: list[Block] = []
    names: list[str] = []
    for piece in row.split("·"):
        hit = re.search(r"(\S+)\s+([٠-٩]+)/([٠-٩]+)", piece.strip())
        if hit:
            size, astray = int(western(hit.group(3))), int(western(hit.group(2)))
            cells.append((astray, size - astray))
            names.append(hit.group(1))
    seen = sum(sum(one) for one in cells)
    left = total - seen
    (astray_all,) = re.findall(r"\*\*([٠-٩]+) استثناءً\*\*", text)
    rest = int(western(astray_all)) - sum(one[0] for one in cells)
    cells.append((rest, left - rest))
    names.append("بقيّة")
    return cells, names, total


def read_numbers(deposit: Path) -> tuple[list[Block], list[str], int]:
    text = deposit.read_text(encoding="utf-8")
    rows = re.findall(r"^\| (\S+) \| ([٠-٩]+) \| ([٠-٩]+) \|$", text, re.MULTILINE)
    expected = {"٣–١٠": 0, "١١–١٩": 1, "عقود": 1, "مئة/ألف": 2}
    cells: list[Block] = []
    names: list[str] = []
    for name, places, right in rows:
        size, hit = int(western(places)), int(western(right))
        table = [0, 0, 0]
        table[expected[name]] += hit
        table[2] += size - hit  # المخالفُ مخرجُه `مجرور-مفرد` بنصّ الإيداع
        cells.append(tuple(table))
        names.append(name)
    return cells, names, sum(sum(one) for one in cells)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--hasr", type=Path, required=True)
    parser.add_argument("--numbers", type=Path, required=True)
    given = parser.parse_args()

    stands = [
        ("الحصر", *read_hasr(given.hasr)),
        ("العدد", *read_numbers(given.numbers)),
    ]
    print("— لا قياسَ جديدًا على المصحف: المقيسُ أثرُ المعيار على الجشع")
    print(f"— مجموعُ المقامين: {sum(one[3] for one in stands)}")

    worst_over = -float("inf")
    least_gap = float("inf")
    worst_identity = 0.0
    least_real = float("inf")
    disagree = 0
    spent: dict[tuple[str, str], int] = {}
    first: dict[tuple[str, str], tuple[str, int]] = {}
    totals: dict[tuple[str, str], float] = {}

    for stand, cells, names, total in stands:
        print(
            f"\n═══ مقامُ {stand}: {total} موضعًا | خاناتٌ {len(cells)}"
            f" | أصنافٌ {len(cells[0])}"
        )
        for one, name in zip(cells, names):
            print(f"    {name:10s} حجمٌ {sum(one):4d} | أصنافُه {one}")
        for how in COSTS:
            steps, whole = spend(cells, names, how)
            spent[(stand, how)] = len(steps)
            totals[(stand, how)] = whole
            print(
                f"\n  — بمعيار {how}: بتّاتٌ {len(steps)}" f" | مجموعُ الكسب {whole:+.6f}"
            )
            for index, (label, gain, count) in enumerate(steps, start=1):
                if index == 1:
                    sizes = sorted(
                        (
                            len([one for one in label.split(" و")]),
                            len(cells) - len(label.split(" و")),
                        )
                    )
                    first[(stand, how)] = (label, sizes[0])
                print(
                    f"      د{index} «أمن {label}؟»: ربحٌ {gain:+.6f}" f" | كتلٌ {count}"
                )
            for one in blocks_of(cells, names, how):
                gap = entropy_cost(one) - permutation_cost(one)
                worst_over = max(worst_over, permutation_cost(one) - entropy_cost(one))
                least_gap = min(least_gap, gap)
                if sum(1 for two in one if two) > 1:  # كتلةٌ فيها صنفان فأكثر
                    least_real = min(least_real, gap)
        one_step = [first[(stand, how)][0] for how in COSTS]
        same = one_step[0] == one_step[1]
        space = sum(subsets(len(cells), one) for one in range(2, len(cells) + 1))
        print(
            f"\n  قسماتُ {len(cells)} خاناتٍ (بِلّ ناقصَ الواحدة): {space}"
            f" | وزارها الجشعُ {len(cells) - 1}"
        )
        for parts in range(2, len(cells) + 1):
            print(
                f"      إلى {parts} كتلًا: S({len(cells)},{parts}) ="
                f" {subsets(len(cells), parts)}"
            )
        print(f"  أيتّفق المعياران على السؤال الأوّل؟ {same}")
        if not same:
            disagree += 1
        root = merged(cells, frozenset(range(len(cells))))
        leaves = blocks_of(cells, names, "تباديل")
        identity = (totals[(stand, "تباديل")] - totals[(stand, "إنتروبيا")]) - (
            math.fsum(entropy_cost(one) - permutation_cost(one) for one in leaves)
            - (entropy_cost(root) - permutation_cost(root))
        )
        worst_identity = max(worst_identity, abs(identity))
        print(f"  الهويّة: فرقُ الكسبين − (Σ فجوات − فجوةُ الجذر) = {identity:+.3e}")

    print("\n═══ الحكم")
    for stand, _, _, _ in stands:
        for how in COSTS:
            print(
                f"  {stand} بمعيار {how}: بتّاتٌ {spent[(stand, how)]}"
                f" | أوّلُ سؤالٍ أصغرُ كتلةٍ فيه {first[(stand, how)][1]}"
            )
    print(f"  أقصى (log₂ التباديل − n·H): {worst_over:+.6f}")
    print(f"  أدنى فجوةِ ستيرلنغ على الكتل: {least_gap:+.6f}")
    print(f"  وأدناها على كتلةٍ غيرِ نقيّة: {least_real:+.6f}")
    print("  والطرفُ الأوّلُ يقع عند كتلةٍ نقيّةٍ صنفُها واحد — وثمناها")
    print("  صفران، فالشرطُ يمرُّ بطرفٍ تافهٍ ويُقال ذلك")
    print(f"  أقصى انحرافٍ عن الهويّة: {worst_identity:.3e}")
    print(f"  درجاتٌ يفترق فيها السؤالُ الأوّل: {disagree}")
    print(
        f"  مجموعُ الكسب في الحصر: تباديلُ {totals[('الحصر', 'تباديل')]:+.6f}"
        f" | إنتروبيا {totals[('الحصر', 'إنتروبيا')]:+.6f}"
        f" | فرقٌ {totals[('الحصر', 'تباديل')] - totals[('الحصر', 'إنتروبيا')]:+.6f}"
    )

    print("\n— ما لا يُدَّعى")
    print("  الجشعُ بالتباديل غيرُ مبرهَنٍ أيضًا: أفضلُ سؤالٍ عند درجةٍ ليس")
    print("  أفضلَ سلّمٍ في النهاية بأيّ معيار — وما يُبلَغ حدٌّ أدنى")
    print("  ولا قياسَ على المصحف ههنا، ولا يُوقَّع تأويلُ أنبوبٍ خارجيّ")
    return 0


if __name__ == "__main__":
    sys.exit(main())
