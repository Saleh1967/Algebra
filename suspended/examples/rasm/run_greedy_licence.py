"""الترخيصُ الجشع بتّةً بتّة — تشغيلُ ختم `69a1c10c…`.

**النقصُ الذي يُكمَّل**: في `34133d54…` كانت الرخصةُ تُمنَح **كتلةً** — كلَّ
خمسِ مئةِ دمجة. فالكتلةُ التي تربح تمرّ **بما فيها من دمجاتٍ لا تربح**،
والكتلةُ التي تخسر تُردّ **بما فيها من دمجاتٍ تربح**. والقولُ «لا يبقى بتٌّ
إلّا ليسهم بإفادة» لا يتحقّق بكتلة.

**فالرخصةُ هنا للدمجة الواحدة**: تُقترَح الدمجةُ الجشعة، وتُقاس التكلفةُ
**المحجوزة** قبلها وبعدها، فإن نزلت **التُزِمت**، وإن لم تنزل **رُفِضت
ووُسِمت ولم تُعَد أبدًا** — تُعَدّ ولا تُبتَلع.

**وشطرا الجشع على حالهما**: القسمةُ جشعٌ **غيرُ مبرهَن** (الزوجُ الأكثرُ
وقوعًا) ⟹ حدٌّ أعلى؛ والترميزُ جشعٌ **مبرهَن** (هوفمان) ⟹ أمثلُ رمزًا رمزًا.

**والوقوفُ مختومٌ سلفًا**: خمسُ مئةِ رفضٍ متوالية، أو ثلاثون ألفَ اقتراح،
أو نفادُ الأزواج. وأيُّها بلغ أوّلًا **يُسمّى في السجلّ**.

**ولا اسمَ لغويٌّ يدخل**: بتّاتٌ وعَرضٌ ووقوعاتٌ وتكلفةٌ فقط.
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
HUFFMAN = REPOSITORY / "examples" / "rasm" / "run_huffman_ascent.py"
BASE = 112
CHECK_EVERY = 500
PATIENCE = 500
MOST_PROPOSALS = 30_000

Pair = tuple[int, int]
Cost = tuple[float, float, float, int, int, float, float]


def _load(path: Path, name: str) -> object:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"لا قارئَ لـ{name}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def huffman_lengths(counts: Counter[int]) -> dict[int, int]:
    """أطوالُ هوفمان بآباءٍ لا بأعضاء — نفسُ الشجرة، وأسرعُ مشيًا.

    ترتيبُ الدفع والفصلُ عند التساوي كما في `run_huffman_ascent`، فتخرج
    الأطوالُ **مطابقةً** لا مقاربة؛ ويُتحقَّق من ذلك عند نقاط الفحص.
    """

    if not counts:
        return {}
    if len(counts) == 1:
        return {symbol: 1 for symbol in counts}
    parent: dict[int, int] = {}
    heap: list[tuple[int, int]] = [
        (number, symbol) for symbol, number in counts.items()
    ]
    heapq.heapify(heap)
    fresh = -1
    while len(heap) > 1:
        first_mass, first = heapq.heappop(heap)
        second_mass, second = heapq.heappop(heap)
        parent[first] = fresh
        parent[second] = fresh
        heapq.heappush(heap, (first_mass + second_mass, fresh))
        fresh -= 1
    above: dict[int, int] = {}
    depth: dict[int, int] = {}
    for symbol in counts:
        walk = symbol
        path: list[int] = []
        while walk in parent and walk not in above:
            path.append(walk)
            walk = parent[walk]
        steps = above.get(walk, 0)
        for one in reversed(path):
            steps += 1
            above[one] = steps
        depth[symbol] = above.get(symbol, 0)
    return depth


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


def cost_of(even: Counter[int], odd: Counter[int], widths: dict[int, int]) -> Cost:
    """(الجملة، المعجم، البيان، العدد، الأبجديّة، الملحَقة، المرتدّ).

    من **العدّادات وحدَها** — فلا تُمَسّ الآياتُ لأجل اقتراحٍ قد يُرفَض.
    """

    whole = even + odd
    used = [symbol for symbol, number in whole.items() if number > 0]
    longest = max((widths[one] for one in used), default=1)
    book = math.fsum(
        widths[one] * math.log2(BASE) + math.log2(longest + 1)
        for one in used
        if widths[one] > 1
    )
    first = coded(even, odd)
    second = coded(odd, even)
    inside = coded(whole, whole)
    outside = (first[0] + second[0]) / 2
    missing = (first[1] + second[1]) / 2
    count = sum(whole.values())
    return (
        book + outside * count,
        book,
        outside * count,
        count,
        len(used),
        book + inside[0] * count,
        missing,
    )


def census(
    verses: list[list[int]],
) -> tuple[Counter[Pair], Counter[Pair], Counter[Pair]]:
    """(الوقوعاتُ خامًا للترتيب، الاستبدالاتُ في الشفع، في الوتر).

    الخامُ متداخلٌ كما في `best_pair` فيُطابِقها الترتيب؛ والاستبدالاتُ
    **غيرُ متداخلة** كما يفعل `apply_merge`، فتُطابِقها العدّادات.
    """

    raw: Counter[Pair] = Counter()
    even: Counter[Pair] = Counter()
    odd: Counter[Pair] = Counter()
    for index, row in enumerate(verses):
        here = even if index % 2 == 0 else odd
        for one, two in zip(row, row[1:]):
            raw[(one, two)] += 1
            if one != two:
                here[(one, two)] += 1
        place = 0
        while place < len(row):
            stop = place
            while stop + 1 < len(row) and row[stop + 1] == row[place]:
                stop += 1
            paired = (stop - place + 1) // 2
            if paired:
                here[(row[place], row[place])] += paired
            place = stop + 1
    return (raw, even, odd)


def moved(counts: Counter[int], pair: Pair, fresh: int, number: int) -> Counter[int]:
    """عدّادٌ جديدٌ بعد الدمجة — ولا يُمَسّ الأصلُ حتّى تُرخَّص."""

    if not number:
        return counts.copy()
    after = counts.copy()
    after[pair[0]] -= number
    after[pair[1]] -= number
    after[fresh] = after.get(fresh, 0) + number
    for one in pair:
        if after.get(one, 0) <= 0:
            after.pop(one, None)
    return after


def _say(mark: str, at: int, here: Cost, start: Cost, refused: int) -> None:
    print(
        f"  {mark} {at}: الجملة {here[0]:.0f} | معجم {here[1]:.0f} "
        f"| بيان {here[2]:.0f} | رموز {here[3]} | أبجديّة {here[4]} "
        f"| ملحَقة {here[5]:.0f} | مرتدّ {here[6]:.4f} "
        f"| نسبةٌ {here[0] / start[0]:.4f} | مرفوضاتٌ {refused}"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", type=Path, required=True)
    given = parser.parse_args()

    ascent = _load(ASCENT, "run_discovered_ascent")
    huffman = _load(HUFFMAN, "run_huffman_ascent")
    verses, heads, order, lines, reach = ascent.corpus_of(  # type: ignore[attr-defined]
        given.text.read_text(encoding="utf-8")
    )
    origin = [list(row) for row in verses]
    widths: dict[int, int] = {index: 1 for index in range(len(order))}
    spelling: dict[int, tuple[int, ...]] = {
        index: (index,) for index in range(len(order))
    }
    even: Counter[int] = Counter()
    odd: Counter[int] = Counter()
    for index, row in enumerate(verses):
        (even if index % 2 == 0 else odd).update(row)

    units = sum(len(one) for one in verses)
    print(f"L₀: {units} وحدةً | أبجديّة {len(order)} | آيات {len(verses)}")
    here = cost_of(even, odd, widths)
    against = huffman.cost_now(verses, widths)  # type: ignore[attr-defined]
    drift = abs(here[0] - against[0])
    print(
        f"نقطةُ الصفر: الجملة {here[0]:.0f} | معجم {here[1]:.0f} "
        f"| بيان {here[2]:.0f} | ملحَقة {here[5]:.0f} | انحرافُ الآلتين {drift:.9f}"
    )
    start = here

    banned: set[Pair] = set()
    ranking: list[Pair] = []
    pointer = 0
    exact_even: Counter[Pair] = Counter()
    exact_odd: Counter[Pair] = Counter()
    commits = 0
    proposals = 0
    refusals = 0
    first_refusal = 0
    streak = 0
    worst_drift = drift
    rises = 0
    refused_width: Counter[int] = Counter()
    refused_mass: list[int] = []
    stop = "الأزواجُ نفدت"
    next_id = len(order)

    while True:
        if proposals >= MOST_PROPOSALS:
            stop = "بلغ سقفَ الاقتراحات"
            break
        if streak >= PATIENCE:
            stop = f"توالى {PATIENCE} رفضًا"
            break
        if pointer >= len(ranking):
            raw, exact_even, exact_odd = census(verses)
            ranking = [
                pair
                for pair, number in raw.most_common()
                if number > 1 and pair not in banned
            ]
            pointer = 0
            if not ranking:
                break
        pair = ranking[pointer]
        pointer += 1
        if pair in banned:
            continue
        proposals += 1
        left, right = pair
        width = widths[left] + widths[right]
        widths[next_id] = width
        after_even = moved(even, pair, next_id, exact_even.get(pair, 0))
        after_odd = moved(odd, pair, next_id, exact_odd.get(pair, 0))
        there = cost_of(after_even, after_odd, widths)
        if there[0] < here[0]:
            if there[0] >= here[0]:
                rises += 1
            spelling[next_id] = spelling[left] + spelling[right]
            ascent.apply_merge(verses, pair, next_id)  # type: ignore[attr-defined]
            even, odd, here = after_even, after_odd, there
            next_id += 1
            commits += 1
            streak = 0
            ranking = []
            pointer = 0
            if commits % CHECK_EVERY == 0:
                mirror = huffman.cost_now(verses, widths)  # type: ignore[attr-defined]
                worst_drift = max(worst_drift, abs(here[0] - mirror[0]))
                _say("بعد", commits, here, start, refusals)
        else:
            del widths[next_id]
            banned.add(pair)
            refusals += 1
            streak += 1
            refused_width[width] += 1
            refused_mass.append(exact_even.get(pair, 0) + exact_odd.get(pair, 0))
            if refusals == 1:
                first_refusal = commits + 1
                print(
                    f"  أوّلُ رفضٍ عند الاقتراح {proposals} "
                    f"(بعد {commits} التزامًا) | عَرضُ المرفوض {width} "
                    f"| استبدالاتُه {refused_mass[0]} "
                    f"| الصعودُ لو التُزِم {there[0] - here[0]:+.2f}"
                )

    print(f"\nالوقوف: {stop}")
    print(
        f"  اقتراحاتٌ {proposals} | التزاماتٌ {commits} | مرفوضاتٌ {refusals} "
        f"| أوّلُ رفضٍ بعد {first_refusal - 1 if first_refusal else 0} التزامًا"
    )
    before = first_refusal - 1 if first_refusal else commits
    print(f"  التزاماتٌ بفرقٍ غيرِ سالب: {rises}")
    print(f"  التزاماتٌ بعد أوّل رفض: {commits - before}")
    print(f"  أقصى انحرافٍ بين الآلتين عند نقاط الفحص: {worst_drift:.9f}")
    print(
        f"  الجملة {here[0]:.0f} | النسبةُ إلى L₀ {here[0] / start[0]:.4f} "
        f"| الملحَقة {here[5]:.0f} | فرقٌ {here[0] - here[5]:+.0f}"
    )

    spread: Counter[int] = Counter()
    for row in verses:
        spread.update(row)
    mismatch = 0
    for source, row in zip(origin, verses):
        laid: list[int] = []
        for symbol in row:
            laid.extend(spelling[symbol])
        if len(laid) != len(source):
            mismatch += abs(len(laid) - len(source))
        mismatch += sum(1 for one, two in zip(laid, source) if one != two)
    print(f"  الرجعة: مواضعُ الخلاف بين بسطِ الرموز ومجرى L₀ = {mismatch}")

    crossing, total = ascent.straddles(verses, heads, widths)  # type: ignore[attr-defined]
    clean = total - crossing
    print(f"  لا يعبر الفراغَ: {clean} من {total} = {clean / total:.4f}")

    kinds: Counter[int] = Counter()
    mass: Counter[int] = Counter()
    for symbol, number in spread.items():
        kinds[widths[symbol]] += 1
        mass[widths[symbol]] += number
    print("\n  المجموعةُ المولَّدةُ مقسومةً بالعَرض:")
    for width in sorted(kinds):
        print(
            f"    عَرضُ {width}: رموزٌ {kinds[width]} | وقوعاتٌ {mass[width]} "
            f"| نصيبٌ {mass[width] / sum(mass.values()):.4f}"
        )
    print(f"    الجملة: رموزٌ {sum(kinds.values())} | وقوعاتٌ {sum(mass.values())}")

    print("\n  المرفوضاتُ مقسومةً بالعَرض:")
    for width in sorted(refused_width):
        print(f"    عَرضُ {width}: مرفوضاتٌ {refused_width[width]}")
    if refused_mass:
        ordered = sorted(refused_mass)
        middle = ordered[len(ordered) // 2]
        print(
            f"    استبدالاتُ المرفوض: أدنى {ordered[0]} | وسيطٌ {middle} "
            f"| أعلى {ordered[-1]}"
        )

    built = [one for one, _ in spread.most_common() if widths[one] > 1]
    shown = ascent.shapes_of(verses, lines, reach, widths, built[:14])  # type: ignore[attr-defined]
    print("\n  أكثرُ الرموز وقوعًا (ببايتاتها من المصحف):")
    for symbol in built[:14]:
        print(
            f"    {shown.get(symbol, '—')}  ({spread[symbol]}) وحداتُه {widths[symbol]}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
