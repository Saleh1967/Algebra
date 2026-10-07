"""الترتيبُ بالتردّد المقيس — تشغيلُ ختم `c8602c00…`.

**السؤالُ المعزول**: الاقتراحُ في الترخيص يُرتَّب بـ**عدد الوقوع الخام**،
والحكمُ يكون بـ**التكلفة الهوفمانيّة**. فهل يعيد هوفمانُ — مقيسًا على
ترددات الحالة — **ترتيبَ الجشع نفسَه**؟ أي: هل **الأكثرُ وقوعًا** هو
**الأكبرُ ربحًا** دائمًا؟

**فيُقاس ذلك مباشرةً**: في كلّ حالٍ تُحسَب `Δ` لأعلى `DEPTH` مقترَحٍ متاح،
ثمّ:

- يُسجَّل هل **أكبرُ ربحٍ** هو **الأوّلُ وقوعًا** (توافقُ الرتبة الأولى)،
- ويُسجَّل هل قاعدةُ «**أوّلُ رابح**» تلتزم ما تلتزمه قاعدةُ «**أكبرُ
  ربحًا**» (توافقُ القرار)،
- **ويُلتزَم أكبرُ ربحًا** — فالمسارُ بالتردّد المقيس لا بالخام.

**والضابطُ ذراعُ الوسم الأبديّ من `2cd80c0f…`** بعمقه نفسِه ووسمِه نفسِه
(١٬٤٠٨٬٥٨١ في ٢٬٣٠٨ التزامًا)، فلا يفترقان إلّا في **قاعدة الاختيار**.

**ويُطبَع `H` و`L` عند كلّ نقطة فحص** — إنتروبيا الحال وطولُ شفرتها
المقيسان على المُجمَّد — فيُرى `H ≤ L < H+1` أو يُرى انكسارُه.

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
MOST_PROPOSALS = 200_000

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
    here = licence.cost_of(even, odd, widths)  # type: ignore[attr-defined]
    start = here

    units = sum(len(one) for one in verses)
    print(f"L₀: {units} وحدةً | أبجديّة {len(order)} | آيات {len(verses)}")
    print(f"القاعدة: يُلتزَم **أكبرُ ربحٍ** من أعلى {DEPTH} مقترَحٍ متاح")
    whole = even + odd
    first_h = huffman.entropy(whole)  # type: ignore[attr-defined]
    first_l = licence.coded(whole, whole)[0]  # type: ignore[attr-defined]
    print(
        f"نقطةُ الصفر: الجملة {here[0]:.0f} | ملحَقة {here[5]:.0f} "
        f"| H {first_h:.4f} | L {first_l:.4f} | L−H {first_l - first_h:+.4f}"
    )

    marked: set[Pair] = set()
    commits = proposals = refusals = rises = 0
    states = top_agree = choice_agree = 0
    gaps: list[float] = [first_l - first_h]
    next_id = len(order)
    stop = "حالٌ لا يربح فيها مقترَح"

    while proposals < MOST_PROPOSALS:
        raw, exact_even, exact_odd = licence.census(verses)  # type: ignore[attr-defined]
        ranking = [
            pair
            for pair, number in raw.most_common()
            if number > 1 and pair not in marked
        ]
        if not ranking:
            stop = "الأزواجُ نفدت"
            break
        looked = ranking[:DEPTH]
        deltas: list[float] = []
        for pair in looked:
            proposals += 1
            widths[next_id] = widths[pair[0]] + widths[pair[1]]
            after_even = licence.moved(  # type: ignore[attr-defined]
                even, pair, next_id, exact_even.get(pair, 0)
            )
            after_odd = licence.moved(  # type: ignore[attr-defined]
                odd, pair, next_id, exact_odd.get(pair, 0)
            )
            there = licence.cost_of(after_even, after_odd, widths)  # type: ignore[attr-defined]
            del widths[next_id]
            deltas.append(there[0] - here[0])
        best = min(range(len(deltas)), key=lambda one: deltas[one])
        paying = [one for one, delta in enumerate(deltas) if delta < 0]
        if not paying:
            for pair in looked:
                marked.add(pair)
            refusals += len(looked)
            stop = f"حالٌ لا يربح فيها أعلى {DEPTH} مقترَحٍ"
            break
        states += 1
        if best == 0:
            top_agree += 1
        if best == paying[0]:
            choice_agree += 1
        for index, pair in enumerate(looked):
            if deltas[index] >= 0:
                marked.add(pair)
                refusals += 1
        chosen = looked[best]
        widths[next_id] = widths[chosen[0]] + widths[chosen[1]]
        even = licence.moved(  # type: ignore[attr-defined]
            even, chosen, next_id, exact_even.get(chosen, 0)
        )
        odd = licence.moved(  # type: ignore[attr-defined]
            odd, chosen, next_id, exact_odd.get(chosen, 0)
        )
        spelling[next_id] = spelling[chosen[0]] + spelling[chosen[1]]
        ascent.apply_merge(verses, chosen, next_id)  # type: ignore[attr-defined]
        here = licence.cost_of(even, odd, widths)  # type: ignore[attr-defined]
        if deltas[best] >= 0:
            rises += 1
        marked.discard(chosen)
        next_id += 1
        commits += 1
        if commits % CHECK_EVERY == 0:
            seen = huffman.cost_now(verses, widths)  # type: ignore[attr-defined]
            whole = even + odd
            level = huffman.entropy(whole)  # type: ignore[attr-defined]
            length = licence.coded(whole, whole)[0]  # type: ignore[attr-defined]
            gaps.append(length - level)
            print(
                f"  بعد {commits}: الجملة {here[0]:.0f} | أبجديّة {here[4]} "
                f"| ملحَقة {here[5]:.0f} | نسبةٌ {here[0] / start[0]:.4f} "
                f"| H {level:.4f} | L {length:.4f} | L−H {length - level:+.4f} "
                f"| انحرافٌ {abs(here[0] - seen[0]):.9f} "
                f"| رتبةٌ {top_agree}/{states} | قرارٌ {choice_agree}/{states}"
            )

    print(f"\nالوقوف: {stop}")
    print(
        f"  اقتراحاتٌ {proposals} | التزاماتٌ {commits} | مرفوضاتٌ {refusals} "
        f"| حالاتٌ {states}"
    )
    print(f"  التزاماتٌ بفرقٍ غيرِ سالب: {rises}")
    print(
        f"  توافقُ الرتبة الأولى: {top_agree} من {states} = "
        f"{top_agree / max(states, 1):.4f}"
    )
    print(
        f"  توافقُ القرار: {choice_agree} من {states} = "
        f"{choice_agree / max(states, 1):.4f}"
    )
    print(f"  أدنى L−H {min(gaps):+.4f} | أقصى L−H {max(gaps):+.4f}")
    print(
        f"  الجملة {here[0]:.0f} | النسبةُ إلى L₀ {here[0] / start[0]:.4f} "
        f"| الملحَقة {here[5]:.0f} | فرقٌ {here[0] - here[5]:+.0f}"
    )

    mismatch = 0
    for row, source in zip(verses, origin):
        laid: list[int] = []
        for symbol in row:
            laid.extend(spelling[symbol])
        mismatch += abs(len(laid) - len(source))
        mismatch += sum(1 for one, two in zip(laid, source) if one != two)
    print(f"  الرجعة: مواضعُ الخلاف بين بسطِ الرموز ومجرى L₀ = {mismatch}")

    crossing, total = ascent.straddles(verses, heads, widths)  # type: ignore[attr-defined]
    print(
        f"  لا يعبر الفراغَ: {total - crossing} من {total} = "
        f"{(total - crossing) / total:.4f}"
    )

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
