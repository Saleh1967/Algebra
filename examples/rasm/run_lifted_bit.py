"""رفعُ بتّةٍ واحدة — تشغيلُ ختم `0c070831…`.

**ما بقي غيرَ معزول**: كُتِب في `docs/الترخيص-بتّةً-بتّة.md` أنّ نسبةَ
الفرق إلى **دمجةٍ بعينها** استنتاجٌ لا قياس، وأنّها تُوسَم كذلك حتّى
تُعزَل. **وهذا عزلُها.**

**البتّةُ المرفوعةُ تُختار بالآلة لا باليد**: هي التي التُزِمت في **أوّل
حالٍ يختلف فيها** «أكبرُ ربحًا» عن «أوّلِ رابح» — أي **أوّلُ بتّةٍ صعدت
بسبب الانقلاب نفسِه**، لا بتّةٌ تُنتقى بعد النظر.

**ثمّ ذراعان**: الأوّلُ كما في `c8602c00…` بلا تبديل، والثاني **كهو إلّا
أنّ تلك البتّةَ ممنوعةٌ من الاقتراح طولَ التشغيل**. فلا يفترقان إلّا في
**بتّةٍ واحدة**، والفرقُ بينهما **أثرُها معزولًا**.

**وتُرفَع مكشوفةً**: تُطبَع وقوعاتُها وطرفاها ببايتاتهما من المصحف،
و`PMI` والربحُ المشتَقُّ بالتباديل والربحُ المقيس ورتبتُها الخام — فلا
يُقال «بتّة» ويُقصَد مجهول.

**ولا اسمَ لغويٌّ يدخل**: بتّاتٌ ووقوعاتٌ وتكلفةٌ فقط.
"""

from __future__ import annotations

import argparse
import importlib.util
import math
import sys
from collections import Counter
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[2]
ASCENT = REPOSITORY / "examples" / "rasm" / "run_discovered_ascent.py"
HUFFMAN = REPOSITORY / "examples" / "rasm" / "run_huffman_ascent.py"
LICENCE = REPOSITORY / "examples" / "rasm" / "run_greedy_licence.py"
ALGEBRA = REPOSITORY / "examples" / "rasm" / "run_greedy_algebra.py"
CHECK_EVERY = 500
DEPTH = 24
MOST_PROPOSALS = 200_000
LOG2E = math.log2(math.e)

Pair = tuple[int, int]
Arm = tuple[float, int, int, int, int, float, int, float]


def _load(path: Path, name: str) -> object:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"لا قارئَ لـ{name}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def displayed(shapes: dict[int, str], symbol: int) -> str:
    """صورةُ الوحدة، أو **تصريحٌ بأنّ مداها صفر** — ولا تُطبَع فارغةً قطّ.

    بعضُ وحدات الـ١١٢ **لا بايتاتِ لها في المصحف**: مداها في السطر صفرٌ
    وبايتاتُها في شريكتها. فطبعُها فراغًا يُقرَأ صورةً وليس بصورة، وهو
    عطلُ عرضٍ من صنف الأوّل في `docs/سجل-الأعطال.md`.
    """

    shape = shapes.get(symbol)
    if shape is None:
        return "«لا شاهدَ»"
    return shape if shape else "«مدًى صفرٌ في البايتات»"


def ascend(
    forbidden: Pair | None,
    verses0: list[list[int]],
    heads: list[list[bool]],
    order: list[str],
    lines: list[str],
    reach: object,
    ascent: object,
    huffman: object,
    licence: object,
    algebra: object,
    label: str,
) -> tuple[Arm, Pair | None]:
    """ذراعٌ واحد — و`forbidden` بتّةٌ ممنوعةٌ من الاقتراح طولَ التشغيل."""

    verses = [list(row) for row in verses0]
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
    worst = abs(here[0] - huffman.cost_now(verses, widths)[0])  # type: ignore[attr-defined]
    marked: set[Pair] = set()
    commits = proposals = refusals = rises = 0
    parted = 0
    split: Pair | None = None
    nid = len(order)

    print(f"\n— {label}")
    while proposals < MOST_PROPOSALS:
        raw, exact_even, exact_odd = licence.census(verses)  # type: ignore[attr-defined]
        ranking = [
            pair
            for pair, number in raw.most_common()
            if number > 1 and pair not in marked and pair != forbidden
        ]
        if not ranking:
            break
        looked = ranking[:DEPTH]
        deltas: list[float] = []
        for pair in looked:
            proposals += 1
            widths[nid] = widths[pair[0]] + widths[pair[1]]
            after_even = licence.moved(  # type: ignore[attr-defined]
                even, pair, nid, exact_even.get(pair, 0)
            )
            after_odd = licence.moved(  # type: ignore[attr-defined]
                odd, pair, nid, exact_odd.get(pair, 0)
            )
            there = licence.cost_of(after_even, after_odd, widths)  # type: ignore[attr-defined]
            del widths[nid]
            deltas.append(there[0] - here[0])
        paying = [one for one, delta in enumerate(deltas) if delta < 0]
        if not paying:
            for pair in looked:
                marked.add(pair)
            refusals += len(looked)
            break
        best = min(range(len(deltas)), key=lambda one: deltas[one])
        if best != paying[0]:
            parted += 1
            if split is None and forbidden is None:
                split = looked[best]
                whole = even + odd
                total = sum(whole.values())
                number = exact_even.get(split, 0) + exact_odd.get(split, 0)
                left, right = whole[split[0]], whole[split[1]]
                excess = algebra.pointwise(total, left, right, number)  # type: ignore[attr-defined]
                shown = ascent.shapes_of(  # type: ignore[attr-defined]
                    verses, lines, reach, widths, list(split)
                )
                print("  البتّةُ المرفوعةُ — أوّلُ حالٍ يختلف فيه الحكمان:")
                print(f"    عند الالتزام {commits + 1} | رتبتُها الخام {best + 1}")
                print(
                    f"    طرفاها ببايتاتهما: {displayed(shown, split[0])} + "
                    f"{displayed(shown, split[1])}"
                )
                print(f"    وقوعُ الطرفين {left} و{right} | استبدالاتُها {number}")
                print(f"    عَرضُها {widths[split[0]] + widths[split[1]]}")
                print(f"    PMI {excess:+.4f} | PMI − log₂e {excess - LOG2E:+.4f}")
                derived = algebra.gain_exact(  # type: ignore[attr-defined]
                    total, left, right, number, split[0] == split[1]
                )
                print(f"    الربحُ المشتَقُّ بالتباديل {derived:+.2f}")
                print(f"    الربحُ المقيس {-deltas[best]:+.2f}")
                print(
                    f"    وما كان «أوّلُ رابح» يأخذه: رتبةٌ {paying[0] + 1} "
                    f"بربحٍ {-deltas[paying[0]]:+.2f}"
                )
        chosen = looked[best]
        widths[nid] = widths[chosen[0]] + widths[chosen[1]]
        even = licence.moved(  # type: ignore[attr-defined]
            even, chosen, nid, exact_even.get(chosen, 0)
        )
        odd = licence.moved(  # type: ignore[attr-defined]
            odd, chosen, nid, exact_odd.get(chosen, 0)
        )
        spelling[nid] = spelling[chosen[0]] + spelling[chosen[1]]
        ascent.apply_merge(verses, chosen, nid)  # type: ignore[attr-defined]
        here = licence.cost_of(even, odd, widths)  # type: ignore[attr-defined]
        if deltas[best] >= 0:
            rises += 1
        for index, pair in enumerate(looked):
            if deltas[index] >= 0:
                marked.add(pair)
                refusals += 1
        marked.discard(chosen)
        nid += 1
        commits += 1
        if commits % CHECK_EVERY == 0:
            seen = huffman.cost_now(verses, widths)  # type: ignore[attr-defined]
            worst = max(worst, abs(here[0] - seen[0]))
            print(
                f"    بعد {commits}: الجملة {here[0]:.0f} | أبجديّة {here[4]} "
                f"| نسبةٌ {here[0] / start[0]:.4f} | اختلافاتٌ {parted}"
            )

    mismatch = 0
    for row, source in zip(verses, verses0):
        laid: list[int] = []
        for symbol in row:
            laid.extend(spelling[symbol])
        mismatch += abs(len(laid) - len(source))
        mismatch += sum(1 for one, two in zip(laid, source) if one != two)
    crossing, total_units = ascent.straddles(verses, heads, widths)  # type: ignore[attr-defined]
    spread: Counter[int] = Counter()
    for row in verses:
        spread.update(row)
    print(
        f"    الوقوف: التزاماتٌ {commits} | اقتراحاتٌ {proposals} "
        f"| مرفوضاتٌ {refusals} | اختلافاتٌ {parted}"
    )
    print(
        f"    الجملة {here[0]:.0f} | النسبةُ إلى L₀ {here[0] / start[0]:.4f} "
        f"| رموزٌ {len(spread)}"
    )
    print(
        f"    بلا نزولٍ {rises} | رجعةٌ {mismatch} | انحرافٌ {worst:.9f} "
        f"| لا يعبر الفراغَ {(total_units - crossing) / total_units:.4f}"
    )
    return (
        (here[0], commits, proposals, rises, mismatch, worst, len(spread), parted),
        split,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", type=Path, required=True)
    given = parser.parse_args()

    ascent = _load(ASCENT, "run_discovered_ascent")
    huffman = _load(HUFFMAN, "run_huffman_ascent")
    licence = _load(LICENCE, "run_greedy_licence")
    algebra = _load(ALGEBRA, "run_greedy_algebra")
    verses, heads, order, lines, reach = ascent.corpus_of(  # type: ignore[attr-defined]
        given.text.read_text(encoding="utf-8")
    )
    print(f"L₀: {sum(len(one) for one in verses)} وحدةً | أبجديّة {len(order)}")
    print(f"العمقُ {DEPTH} للذراعين، ولا يفترقان إلّا في بتّةٍ واحدة")

    whole, lifted = ascend(
        None,
        verses,
        heads,
        order,
        lines,
        reach,
        ascent,
        huffman,
        licence,
        algebra,
        "الذراعُ كما هو",
    )
    if lifted is None:
        print("\nلم يقع اختلافٌ بين الحكمين — فلا بتّةَ تُرفَع")
        return 0
    without, _ = ascend(
        lifted,
        verses,
        heads,
        order,
        lines,
        reach,
        ascent,
        huffman,
        licence,
        algebra,
        "الذراعُ وقد رُفِعت البتّة",
    )

    print("\n— أثرُ البتّة الواحدة معزولًا")
    print(f"  الجملةُ كما هي {whole[0]:.0f} | وقد رُفِعت {without[0]:.0f}")
    print(f"  الفرقُ (مرفوعةً − كما هي) {without[0] - whole[0]:+.0f} بتًّا")
    print(f"  النسبةُ إلى الجملة {abs(without[0] - whole[0]) / whole[0]:.6f}")
    print(f"  التزاماتٌ {whole[1]} ⟶ {without[1]} ({without[1] - whole[1]:+d})")
    print(f"  رموزٌ {whole[6]} ⟶ {without[6]} ({without[6] - whole[6]:+d})")
    print(f"  رجعةُ الذراعين {whole[4]} و{without[4]}")
    print(f"  بلا نزولٍ في الذراعين {whole[3]} و{without[3]}")
    print(f"  أقصى انحرافٍ في الذراعين {max(whole[5], without[5]):.9f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
