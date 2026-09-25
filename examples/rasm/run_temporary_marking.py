"""الوسمُ المؤقّتُ مقابلَ الأبديّ — تشغيلُ ختم `89b59b10…`.

**ما يُعزَل**: في `69a1c10c…` رُفِض الزوجُ **ووُسِم أبدًا**، فانتهى الترخيصُ
عند ٢٬٦٦٢ التزامًا بتكلفةٍ **أغلى** من الكتليّ بـ٥٬٧٥٤ بتًّا. وقلتُ إنّ
السببَ المقترَحَ **الوسمُ الأبديّ** — **ولم يُعزَل**.

**فيُعزَل ههنا بتغييرٍ واحدٍ لا غير**: الوسمُ **يُرفَع عند كلّ التزام**.
فالزوجُ الذي لا يربح في حالٍ **يُعاد اقتراحُه** في حالٍ أخرى، ولا يُبتلَع
ولا يُنسى. وما عدا ذلك — القسمةُ والترميزُ والتكلفةُ والمحجوزةُ — **هو هو**.

**والوقوفُ مختومٌ سلفًا**: حالٌ يُمسَح فيها أعلى `DEPTH` مقترَحٍ فلا يربح
واحدٌ منها، أو بلوغُ سقف الاقتراحات. **وعمقُ البحث محدودٌ معلنٌ**: فما
يُبلَغ **حدٌّ أدنى** لِما يبلغه بحثٌ أعمق، لا حدٌّ أعلى.

**ولا اسمَ لغويٌّ يدخل**: بتّاتٌ وعَرضٌ ووقوعاتٌ وتكلفةٌ فقط.
"""

from __future__ import annotations

import argparse
import importlib.util
import sys
from collections import Counter
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[2]
ASCENT = REPOSITORY / "examples" / "rasm" / "run_discovered_ascent.py"
HUFFMAN = REPOSITORY / "examples" / "rasm" / "run_huffman_ascent.py"
LICENCE = REPOSITORY / "examples" / "rasm" / "run_greedy_licence.py"
CHECK_EVERY = 500
DEPTH = 24
MOST_PROPOSALS = 120_000
WATCHED = (30, 3)

Pair = tuple[int, int]


def _load(path: Path, name: str) -> object:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"لا قارئَ لـ{name}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", type=Path, required=True)
    given = parser.parse_args()

    ascent = _load(ASCENT, "run_discovered_ascent")
    huffman = _load(HUFFMAN, "run_huffman_ascent")
    licence = _load(LICENCE, "run_greedy_licence")
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
    here = licence.cost_of(even, odd, widths)  # type: ignore[attr-defined]
    start = here
    mirror = huffman.cost_now(verses, widths)  # type: ignore[attr-defined]
    print(f"L₀: {units} وحدةً | أبجديّة {len(order)} | آيات {len(verses)}")
    print(
        f"نقطةُ الصفر: الجملة {here[0]:.0f} | ملحَقة {here[5]:.0f} "
        f"| انحرافُ الآلتين {abs(here[0] - mirror[0]):.9f} | عمقُ البحث {DEPTH}"
    )

    commits = 0
    proposals = 0
    refusals = 0
    rises = 0
    revived = 0
    watched_at = 0
    worst_drift = abs(here[0] - mirror[0])
    next_id = len(order)
    marked: set[Pair] = set()
    stop = "حالٌ لا يربح فيها مقترَح"

    while proposals < MOST_PROPOSALS:
        raw, exact_even, exact_odd = licence.census(verses)  # type: ignore[attr-defined]
        ranking = [pair for pair, number in raw.most_common() if number > 1]
        if not ranking:
            stop = "الأزواجُ نفدت"
            break
        took = False
        for pair in ranking[:DEPTH]:
            proposals += 1
            width = widths[pair[0]] + widths[pair[1]]
            widths[next_id] = width
            after_even = licence.moved(  # type: ignore[attr-defined]
                even, pair, next_id, exact_even.get(pair, 0)
            )
            after_odd = licence.moved(  # type: ignore[attr-defined]
                odd, pair, next_id, exact_odd.get(pair, 0)
            )
            there = licence.cost_of(after_even, after_odd, widths)  # type: ignore[attr-defined]
            delta = there[0] - here[0]
            if delta >= 0:
                del widths[next_id]
                marked.add(pair)
                refusals += 1
                continue
            if pair in marked:
                revived += 1
                marked.discard(pair)
                print(
                    f"  وسمٌ يُرفَع عند الالتزام {commits + 1}: عَرضُه {width} "
                    f"| ربحُه {here[0] - there[0]:.2f}"
                )
            if pair == WATCHED and not watched_at:
                watched_at = commits + 1
                print(f"  الزوجُ المرصود التُزِم عند {watched_at}")
            spelling[next_id] = spelling[pair[0]] + spelling[pair[1]]
            ascent.apply_merge(verses, pair, next_id)  # type: ignore[attr-defined]
            even, odd, here = after_even, after_odd, there
            next_id += 1
            commits += 1
            if delta >= 0:
                rises += 1
            took = True
            if commits % CHECK_EVERY == 0:
                seen = huffman.cost_now(verses, widths)  # type: ignore[attr-defined]
                worst_drift = max(worst_drift, abs(here[0] - seen[0]))
                print(
                    f"  بعد {commits}: الجملة {here[0]:.0f} | معجم {here[1]:.0f} "
                    f"| رموز {here[3]} | أبجديّة {here[4]} "
                    f"| ملحَقة {here[5]:.0f} | نسبةٌ {here[0] / start[0]:.4f} "
                    f"| مرفوضاتٌ {refusals} | وسومٌ مرفوعة {revived}"
                )
            break
        if not took:
            stop = f"حالٌ لا يربح فيها أعلى {DEPTH} مقترَحٍ"
            break
    else:
        stop = "بلغ سقفَ الاقتراحات"

    print(f"\nالوقوف: {stop}")
    print(
        f"  اقتراحاتٌ {proposals} | التزاماتٌ {commits} | مرفوضاتٌ {refusals} "
        f"| وسومٌ رُفِعت ثمّ التُزِمت {revived}"
    )
    print(f"  التزاماتٌ بفرقٍ غيرِ سالب: {rises}")
    print(f"  الزوجُ المرصودُ التُزِم عند: {watched_at}")
    print(f"  أقصى انحرافٍ بين الآلتين عند نقاط الفحص: {worst_drift:.9f}")
    print(
        f"  الجملة {here[0]:.0f} | النسبةُ إلى L₀ {here[0] / start[0]:.4f} "
        f"| الملحَقة {here[5]:.0f} | فرقٌ {here[0] - here[5]:+.0f}"
    )

    mismatch = 0
    for source, row in zip(origin, verses):
        laid: list[int] = []
        for symbol in row:
            laid.extend(spelling[symbol])
        mismatch += abs(len(laid) - len(source))
        mismatch += sum(1 for one, two in zip(laid, source) if one != two)
    print(f"  الرجعة: مواضعُ الخلاف بين بسطِ الرموز ومجرى L₀ = {mismatch}")

    crossing, total = ascent.straddles(verses, heads, widths)  # type: ignore[attr-defined]
    clean = total - crossing
    print(f"  لا يعبر الفراغَ: {clean} من {total} = {clean / total:.4f}")

    spread: Counter[int] = Counter()
    for row in verses:
        spread.update(row)
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
