"""ذراعان في تشغيلٍ واحد — تشغيلُ ختم `2cd80c0f…`.

**العطلُ الذي يُصلَح**: ختمُ `89b59b10…` قال «التغييرُ واحدٌ لا غير»،
**وكان فيه متغيّران**: رفعُ الوسم **وحدُّ عمقِ البحث** (٢٤ في كلّ حال)،
بينما ذراعُ `69a1c10c…` كان بلا حدِّ عمقٍ في الحال الواحدة. فالمقابلةُ
بينهما **ملتبسةٌ**، ولا يُنسَب الفرقُ إلى الوسم وحدَه.

**فيُشغَّل الذراعان ههنا في آلةٍ واحدةٍ وبعمقٍ واحد** (`DEPTH`)، فلا يختلفان
إلّا في شيءٍ واحد: **أيبقى وسمُ المرفوض أم يُرفَع عند كلّ التزام**.

**والوقوفُ واحدٌ للذراعين**: حالٌ لا يربح فيها أعلى `DEPTH` مقترَحٍ متاح.
**وعمقُ البحث محدودٌ معلنٌ**، فما يُبلَغ **حدٌّ أدنى** لا أعلى.

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
LASTING = "أبديّ"
LIFTED = "مؤقّت"

Pair = tuple[int, int]
Arm = tuple[float, float, int, int, int, int, int, int, float, int, int, float]


def _load(path: Path, name: str) -> object:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"لا قارئَ لـ{name}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def ascend(
    marking: str,
    source: list[list[int]],
    heads: list[list[bool]],
    alphabet: int,
    ascent: object,
    huffman: object,
    licence: object,
) -> Arm:
    """ذراعٌ واحد — والوسمُ وحدَه يفرّق بينهما."""

    verses = [list(row) for row in source]
    widths: dict[int, int] = {index: 1 for index in range(alphabet)}
    spelling: dict[int, tuple[int, ...]] = {
        index: (index,) for index in range(alphabet)
    }
    even: Counter[int] = Counter()
    odd: Counter[int] = Counter()
    for index, row in enumerate(verses):
        (even if index % 2 == 0 else odd).update(row)
    here = licence.cost_of(even, odd, widths)  # type: ignore[attr-defined]
    start = here
    worst = abs(here[0] - huffman.cost_now(verses, widths)[0])  # type: ignore[attr-defined]
    marked: set[Pair] = set()
    commits = proposals = refusals = rises = revived = 0
    next_id = alphabet

    print(f"\n— ذراعُ الوسم الـ{marking} (عمقٌ {DEPTH})")
    while proposals < MOST_PROPOSALS:
        raw, exact_even, exact_odd = licence.census(verses)  # type: ignore[attr-defined]
        ranking = [
            pair
            for pair, number in raw.most_common()
            if number > 1 and (marking == LIFTED or pair not in marked)
        ]
        if not ranking:
            break
        took = False
        for pair in ranking[:DEPTH]:
            proposals += 1
            widths[next_id] = widths[pair[0]] + widths[pair[1]]
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
                worst = max(worst, abs(here[0] - seen[0]))
                print(
                    f"    بعد {commits}: الجملة {here[0]:.0f} "
                    f"| أبجديّة {here[4]} | ملحَقة {here[5]:.0f} "
                    f"| نسبةٌ {here[0] / start[0]:.4f} | مرفوضاتٌ {refusals} "
                    f"| وسومٌ مرفوعة {revived}"
                )
            break
        if not took:
            break

    mismatch = 0
    for row, original in zip(verses, source):
        laid: list[int] = []
        for symbol in row:
            laid.extend(spelling[symbol])
        mismatch += abs(len(laid) - len(original))
        mismatch += sum(1 for one, two in zip(laid, original) if one != two)
    crossing, total = ascent.straddles(verses, heads, widths)  # type: ignore[attr-defined]
    spread: Counter[int] = Counter()
    for row in verses:
        spread.update(row)
    print(
        f"    الوقوف: التزاماتٌ {commits} | اقتراحاتٌ {proposals} "
        f"| مرفوضاتٌ {refusals} | وسومٌ رُفِعت ثمّ التُزِمت {revived}"
    )
    print(
        f"    الجملة {here[0]:.0f} | النسبةُ إلى L₀ {here[0] / start[0]:.4f} "
        f"| الملحَقة {here[5]:.0f} | رموزٌ {len(spread)}"
    )
    print(
        f"    بلا نزولٍ {rises} | رجعةٌ {mismatch} | انحرافٌ {worst:.9f} "
        f"| لا يعبر الفراغَ {(total - crossing) / total:.4f}"
    )
    return (
        here[0],
        here[0] / start[0],
        commits,
        proposals,
        refusals,
        revived,
        rises,
        mismatch,
        worst,
        len(spread),
        total - crossing,
        (total - crossing) / total,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", type=Path, required=True)
    given = parser.parse_args()

    ascent = _load(ASCENT, "run_discovered_ascent")
    huffman = _load(HUFFMAN, "run_huffman_ascent")
    licence = _load(LICENCE, "run_greedy_licence")
    verses, heads, order, _lines, _reach = ascent.corpus_of(  # type: ignore[attr-defined]
        given.text.read_text(encoding="utf-8")
    )
    units = sum(len(one) for one in verses)
    print(f"L₀: {units} وحدةً | أبجديّة {len(order)} | آيات {len(verses)}")
    print(f"الذراعان يختلفان في الوسم وحدَه، والعمقُ {DEPTH} لكليهما")

    lasting = ascend(LASTING, verses, heads, len(order), ascent, huffman, licence)
    lifted = ascend(LIFTED, verses, heads, len(order), ascent, huffman, licence)

    print("\n— المقابلةُ عند عمقٍ واحد")
    print(f"  جملةُ الأبديّ {lasting[0]:.0f} | جملةُ المؤقّت {lifted[0]:.0f}")
    print(f"  المؤقّتُ − الأبديّ = {lifted[0] - lasting[0]:+.0f} بتًّا")
    print(f"  التزاماتُ الأبديّ {lasting[2]} | التزاماتُ المؤقّت {lifted[2]}")
    print(f"  أدنى الذراعين {min(lasting[0], lifted[0]):.0f}")
    print(f"  أقصى انحرافٍ في الذراعين {max(lasting[8], lifted[8]):.9f}")
    print(f"  رجعةُ الذراعين {lasting[7]} و{lifted[7]}")
    print(f"  بلا نزولٍ في الذراعين {lasting[6]} و{lifted[6]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
