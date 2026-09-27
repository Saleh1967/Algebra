"""يُطوى المجمَّدُ ويُفَكّ — **واسترجاعٌ تامٌّ أو سقوط**، لا تقدير.

**الفرقُ عن كلّ قياسٍ سبقه**: `H = 2.6283` **لا يُستَرجَع منه سطرٌ واحد**.
وههنا يُطوى مجرى الحالات إلى **أعدادٍ صحيحة**، ثمّ يُفَكّ، **ويُقابَل
بالأصل حالةً بحالة**. فإن خالفت واحدةٌ سقط التشغيل.

**والحارسُ يُكتشَف لا يُفترَض**: يُبحَث **أكبرُ** طائفةٍ من الحالات لا
يقع بين أيّ اثنين منها انتقالٌ مشهودٌ داخلَ السطر — **بعَدٍّ تامٍّ على
كلّ الطوائف**، لا بجشعٍ ولا بظنّ. فتلك هي «المحجورة»، والباقيةُ «حرّة».

**وثمنُ الطيّ عددٌ صحيحٌ**: `⌈log₂ T(n)⌉` لكلّ سطر. **فالسعةُ ليست
إنتروبيا بل بتّاتٌ تُكتَب وتُقرَأ.**
"""

from __future__ import annotations

import argparse
import importlib.util
import math
import sys
from collections import Counter
from itertools import combinations
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[2]
AUDIT = REPOSITORY / "examples" / "rasm" / "run_encoding_audit.py"
MARKUP = "<sel>"


def _audit() -> object:
    spec = importlib.util.spec_from_file_location("run_encoding_audit", AUDIT)
    if spec is None or spec.loader is None:
        raise RuntimeError("لا قارئَ للمواصفة")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _folding() -> object:
    sys.path.insert(0, str(REPOSITORY / "src"))
    from algebra import folding

    return folding


def lines_of_states(text: str) -> list[list[str]]:
    audit = _audit()
    found: list[list[str]] = []
    for line in text.replace(MARKUP, " ").splitlines():
        if not line.strip():
            continue
        units = audit.rasm_units(line)  # type: ignore[attr-defined]
        found.append([state for _letter, state in units])
    return found


def transitions(lines: list[list[str]]) -> Counter[tuple[str, str]]:
    """الانتقالاتُ المشهودةُ **داخلَ السطر** — ولا تعبر السطر."""

    seen: Counter[tuple[str, str]] = Counter()
    for row in lines:
        for one, two in zip(row, row[1:]):
            seen[(one, two)] += 1
    return seen


def largest_blocked(
    states: list[str], seen: Counter[tuple[str, str]]
) -> tuple[str, ...]:
    """أكبرُ طائفةٍ لا انتقالَ بين أيّ اثنين منها — **بعَدٍّ تامٍّ لا جشع**.

    والطوائفُ `2^k`، فتُعَدّ كلُّها ما دام `k` صغيرًا؛ ويُردّ إن كبر.
    """

    if len(states) > 20:
        raise SystemExit(f"أبجديّةٌ أكبرُ من أن تُعَدّ طوائفُها: {len(states)}")
    best: tuple[str, ...] = ()
    for size in range(len(states), 0, -1):
        for group in combinations(states, size):
            inside = set(group)
            if any(one in inside and two in inside for one, two in seen):
                continue
            best = group
            break
        if best:
            break
    return best


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", type=Path, required=True)
    given = parser.parse_args()

    folding = _folding()
    lines = lines_of_states(given.text.read_text(encoding="utf-8"))
    places = sum(len(one) for one in lines)
    states = sorted({one for row in lines for one in row})
    seen = transitions(lines)
    print(f"— الأسطر: {len(lines)} | الحالات: {places} | الأبجديّة: {len(states)}")
    print(f"— انتقالاتٌ مشهودةٌ متمايزة: {len(seen)} من {len(states) ** 2} ممكنة")
    print()

    blocked = largest_blocked(states, seen)
    free = [one for one in states if one not in set(blocked)]
    print("— الحارسُ مكتشَفٌ بعَدٍّ تامٍّ على كلّ الطوائف")
    print(f"  محجورةٌ (لا انتقالَ بين أيّ اثنين منها): {len(blocked)}")
    print(f"  والمحجورةُ بعينها: {' · '.join(blocked) if blocked else '—'}")
    print(f"  وحرّةٌ: {len(free)}")
    order = free + list(blocked)
    place = {one: index for index, one in enumerate(order)}
    shape = folding.Guarded(  # type: ignore[attr-defined]
        free=len(free), blocked=len(blocked)
    )
    plain = folding.Guarded(free=len(states), blocked=0)  # type: ignore[attr-defined]
    root = folding.growth_root(shape)  # type: ignore[attr-defined]
    print(f"  فالمتتالية: x² = {shape.free}x + {shape.free * shape.blocked}")
    print(f"  وجذرُها الأكبر ρ = {root:.6f} | log₂ ρ = {math.log2(root):.4f}")
    print()

    print("— الطيُّ والفكُّ سطرًا سطرًا، والمقابلةُ حالةً بحالة")
    guarded_bits = 0
    plain_bits = 0
    folded = 0
    recovered = 0
    longest = 0
    biggest = 0
    for row in lines:
        word = tuple(place[one] for one in row)
        index = folding.fold(shape, word)  # type: ignore[attr-defined]
        back = folding.unfold(shape, index, len(word))  # type: ignore[attr-defined]
        folded += 1
        if back != word:
            raise SystemExit(f"فكٌّ لا يُطابِق الطيَّ في سطرٍ طولُه {len(word)}")
        if [order[one] for one in back] != row:
            raise SystemExit("الاسترجاعُ لا يُطابِق الأصلَ حالةً بحالة")
        recovered += 1
        guarded_bits += folding.bits_exactly(shape, len(word))  # type: ignore[attr-defined]
        plain_bits += folding.bits_exactly(plain, len(word))  # type: ignore[attr-defined]
        longest = max(longest, len(word))
        biggest = max(biggest, index)

    print(f"  أسطرٌ طُوِيت: {folded} | واسترجعت تامّةً: {recovered}")
    print(f"  وأطولُ سطرٍ: {longest} حالة | وأكبرُ دليلٍ: {biggest.bit_length()} بتّة")
    print("  ومخالفاتٌ: 0 — **الاسترجاعُ تامٌّ أو يسقط التشغيل**")
    print()

    print("— ثمنُ الطيّ، أعدادًا صحيحةً لا تقديرًا")
    print(f"  بالحارس: {guarded_bits} بتّة | ⌈log₂ T(n)⌉ مجموعةً على الأسطر")
    print(f"  بلا حارس: {plain_bits} بتّة | أي أبجديّةً مطلقةً من {len(states)}")
    print(f"  فوفَّر الحارسُ: {plain_bits - guarded_bits} بتّة")
    print(f"  وللحالة الواحدة: {guarded_bits / places:.4f} بتّة بالحارس")
    print(f"  وبلا حارس: {plain_bits / places:.4f} بتّة")
    print()

    print("— وما يلزم عن هذا")
    print("  الثمنُ أعلاه **مكتوبٌ ومقروء**: يُطوى المجرى إلى أعدادٍ ويُفَكّ")
    print("  فيرجع حالةً بحالة. **ولا يُقابَل بإنتروبيا**: تلك حدٌّ أدنى")
    print("  لمتوسّطِ شفرةٍ، وهذا **طولُ شفرةٍ قائمةٍ بعينها** على هذه القسمة.")
    print("  والمبرهنةُ في src/algebra/folding.py، ومستوفاةٌ على كلّ الجائزات")
    print("  حتّى الطول السادس في tests/algebra/test_folding.py.")
    print("  ولا يُسمّى المحجورُ سكونًا ولا الحرُّ حركةً — صنفان بالانتقالات.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
