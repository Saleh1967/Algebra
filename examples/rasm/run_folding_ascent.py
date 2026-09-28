"""صعودُ الطيّ: الوحدةُ ← اللفظُ ← السطرُ، **بالتقابل نفسِه، بلا طولٍ مستعار**.

**العطلُ الذي يُصلَحه**: `run_folding_proof.py` يطوي السطرَ ثمّ يفكُّه
**بطولٍ يُمرَّر من خارج** (`unfold(shape, index, len(word))`). فالاسترجاعُ
كان **بدليلٍ وطول**، لا بدليلٍ وحدَه — **والطولُ معلومةٌ لم تُحسَب في
الثمن**.

**وههنا `fold_any`** (المبرهنة ٤): `off(n) + fold(w)` تقابلٌ على `ℕ`
كلِّها، **فالطولُ يُقرَأ من العدد نفسِه**.

**والصعودُ يتركّب** (المبرهنة ٥): كلُّ لفظٍ يصير عددًا في
`{0,…,A(L)−1}`، **فمتتاليةُ الألفاظ كلمةٌ على أبجديّةٍ سعتُها `A(L)`
بلا حارس**، فتُطوى بالتقابل نفسِه. **فالسطرُ عددٌ واحدٌ يُفَكّ فيرجع
ألفاظًا ثمّ حالاتٍ.**
"""

from __future__ import annotations

import argparse
import importlib.util
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


def lines_of_tokens(text: str) -> list[list[list[str]]]:
    """سطرٌ ← ألفاظٌ ← حالاتُ مواضع الرسم.

    **واللفظُ ما بين فراغين** (حدُّ `494465d1…`)، ويُقشَّر كلُّ لفظٍ وحدَه
    فـ**الجوارُ لا يعبر الفاصل** — وذلك شرطُ الحارس في المستوى الأوّل.
    """

    audit = _audit()
    found: list[list[list[str]]] = []
    for line in text.replace(MARKUP, " ").splitlines():
        if not line.strip():
            continue
        words: list[list[str]] = []
        for piece in line.split():
            units = audit.rasm_units(piece)  # type: ignore[attr-defined]
            if units:
                words.append([state for _letter, state in units])
        if words:
            found.append(words)
    return found


def largest_blocked(
    states: list[str], seen: Counter[tuple[str, str]]
) -> tuple[str, ...]:
    """أكبرُ طائفةٍ لا انتقالَ بين أيّ اثنين منها — **بعَدٍّ تامٍّ لا جشع**."""

    if len(states) > 20:
        raise SystemExit(f"أبجديّةٌ أكبرُ من أن تُعَدّ طوائفُها: {len(states)}")
    for size in range(len(states), 0, -1):
        for group in combinations(states, size):
            inside = set(group)
            if not any(one in inside and two in inside for one, two in seen):
                return group
    return ()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", type=Path, required=True)
    given = parser.parse_args()

    folding = _folding()
    lines = lines_of_tokens(given.text.read_text(encoding="utf-8"))
    tokens = [one for row in lines for one in row]
    states = sorted({one for word in tokens for one in word})
    places = sum(len(one) for one in tokens)
    print(f"— الأسطر: {len(lines)} | الألفاظ: {len(tokens)} | الحالات: {places}")
    print(f"— أبجديّةُ الحالات: {len(states)}")

    # الحارسُ **داخلَ اللفظ**: الجوارُ لا يعبر الفاصلَ البنيويّ
    seen: Counter[tuple[str, str]] = Counter()
    for word in tokens:
        for one, two in zip(word, word[1:]):
            seen[(one, two)] += 1
    blocked = largest_blocked(states, seen)
    free = [one for one in states if one not in set(blocked)]
    order = free + list(blocked)
    place = {one: index for index, one in enumerate(order)}
    unit = folding.Guarded(free=len(free), blocked=len(blocked))  # type: ignore[attr-defined]
    print(f"— محجورةٌ داخلَ اللفظ: {len(blocked)} | وحرّةٌ: {len(free)}")
    print(f"  والمحجورةُ بعينها: {' · '.join(blocked) if blocked else '—'}")
    print(f"  فالمتتالية: x² = {unit.free}x + {unit.free * unit.blocked}")
    print()

    print("═══ المستوى ١: اللفظُ عددًا واحدًا — والطولُ من العدد لا من خارج ═══")
    longest_word = max(len(one) for one in tokens)
    word_radix = folding.offset(unit, longest_word + 1)  # type: ignore[attr-defined]
    folded_words: list[list[int]] = []
    word_recovered = 0
    for row in lines:
        here: list[int] = []
        for word in row:
            letters = tuple(place[one] for one in word)
            index = folding.fold_any(unit, letters)  # type: ignore[attr-defined]
            if folding.unfold_any(unit, index) != letters:  # type: ignore[attr-defined]
                raise SystemExit("فكُّ اللفظ لا يُطابِق طيَّه")
            if index >= word_radix:
                raise SystemExit("دليلُ لفظٍ فوق سعةِ الأبجديّة العُليا")
            word_recovered += 1
            here.append(index)
        folded_words.append(here)
    print(f"  ألفاظٌ طُوِيت واسترجعت تامّةً: {word_recovered} من {len(tokens)}")
    print(f"  أطولُ لفظٍ: {longest_word} حالة")
    print(f"  فسعةُ أبجديّةِ الألفاظ A(L) = {word_radix}")
    print(f"  وعرضُها: {word_radix.bit_length()} بتّة")
    print()

    print("═══ المستوى ٢: السطرُ عددًا واحدًا — على أبجديّةِ الألفاظ ═══")
    line_shape = folding.Guarded(free=word_radix, blocked=0)  # type: ignore[attr-defined]
    line_recovered = 0
    line_bits = 0
    biggest = 0
    longest_line = max(len(one) for one in folded_words)
    for row, original in zip(folded_words, lines):
        index = folding.fold_any(line_shape, tuple(row))  # type: ignore[attr-defined]
        back = folding.unfold_any(line_shape, index)  # type: ignore[attr-defined]
        if list(back) != row:
            raise SystemExit("فكُّ السطر لا يُطابِق طيَّه")
        # **والاسترجاعُ إلى الحالات لا إلى الأعداد**: يُنزَل مستوًى ثانيًا
        rebuilt = [
            [order[one] for one in folding.unfold_any(unit, two)]  # type: ignore[attr-defined]
            for two in back
        ]
        if rebuilt != original:
            raise SystemExit("الاسترجاعُ لا يُطابِق الأصلَ حالةً بحالة")
        line_recovered += 1
        line_bits += max(index.bit_length(), 1)
        biggest = max(biggest, index)
    print(f"  أسطرٌ طُوِيت واسترجعت تامّةً **إلى الحالات**: {line_recovered}")
    print(f"  أطولُ سطرٍ: {longest_line} لفظًا")
    print(f"  وأكبرُ دليلِ سطرٍ: {biggest.bit_length()} بتّة")
    print("  ومخالفاتٌ: 0 — **الاسترجاعُ تامٌّ أو يسقط التشغيل**")
    print()

    print("═══ ثمنُ كلّ مستوًى — وما يُسمّى شفرةً وما لا يُسمّى ═══")
    # **قيدٌ رياضيٌّ يُقال قبل الأرقام**: `bit_length` عددٍ واحدٍ طولُه
    # بالضبط؛ **ومجموعُ أطوالِ أعدادٍ كثيرةٍ ليس طولَ شفرةٍ لمجراها** —
    # فلا يُفَكّ تلاصقُها بلا فواصلَ أو عرضٍ ثابت. فيُطبَع الأمران
    # مفصولين، **ولا يُقارَن عرضٌ ثابتٌ بمجموع أطوال**.
    straight = 0
    for row in lines:
        whole = tuple(place[two] for one in row for two in one)
        index = folding.fold_any(unit, whole)  # type: ignore[attr-defined]
        if folding.unfold_any(unit, index) != whole:  # type: ignore[attr-defined]
            raise SystemExit("الطيُّ المباشرُ لا يُفَكّ")
        straight += max(index.bit_length(), 1)
    word_width = max(word_radix.bit_length(), 1)
    fixed_words = word_width * len(tokens)
    print("— شفراتٌ تُفَكّ بلا استعارة (عرضٌ ثابتٌ أو عددٌ واحد)")
    print(f"  اللفظُ بعرضٍ ثابتٍ {word_width} بتّة × {len(tokens)}: {fixed_words} بتّة")
    print(f"  والسطرُ عددًا واحدًا فوق الألفاظ: {line_bits} بتّة")
    print(f"  والسطرُ عددًا واحدًا على الحالات مباشرةً: {straight} بتّة")
    print()
    print("— فثمنُ حملِ حدودِ الألفاظ، عددًا")
    print(f"  {line_bits} − {straight} = {line_bits - straight} بتّة")
    print(f"  وللفظِ الواحد: {(line_bits - straight) / len(tokens):.4f} بتّة")
    print()
    print("— ومجموعُ أطوالِ الأعداد — **وليس طولَ شفرةٍ لمجرًى**")
    print(
        f"  أطوالُ أدلّةِ الألفاظ مجموعةً: {any_bits_of(folding, lines, place, unit)} بتّة"
    )
    print("  ولا يُفَكّ تلاصقُها بلا فاصل، **فلا تُقرَأ شفرةً**؛ وتُطبَع")
    print("  كي يُرى الفرقُ بينها وبين العرض الثابت، لا لتُقارَن به.")
    print()

    print("— وما يلزم عن هذا")
    print("  **الحدودُ ثمنٌ**: طيُّ السطر فوق الألفاظ أغلى من طيّه على")
    print("  الحالات مباشرةً بالعدد المطبوع أعلاه — **وذلك ثمنُ التقطيع**،")
    print("  يُدفَع بتًّا ولا يُوهَب. فمن قسَّم مجرًى إلى ألفاظٍ **زاد**")
    print("  ما يُكتَب، ولم يُنقِصه؛ والزيادةُ هي حدودُ الألفاظ نفسُها.")
    print("  **والصعودُ يتركّب**: السطرُ عددٌ واحدٌ يُفَكّ فيرجع ألفاظًا ثمّ")
    print("  حالاتٍ، **ولا يُمرَّر طولٌ في مستوًى من المستويات** (المبرهنة ٤).")
    print("  ولا يُسمّى المحجورُ سكونًا ولا الحرُّ حركةً — صنفان بالانتقالات")
    print("  المشهودة **داخلَ اللفظ**، والجوارُ لا يعبر الفاصلَ البنيويّ.")
    print("  **ولا يقول الطيُّ إنّ البنيةَ مفهومة** — يقول إنّها مُستَرجَعة.")
    return 0


def any_bits_of(
    folding: object,
    lines: list[list[list[str]]],
    place: dict[str, int],
    unit: object,
) -> int:
    """مجموعُ أطوالِ أدلّةِ الألفاظ — **ويُسمّى مجموعَ أطوالٍ لا شفرة**."""

    total = 0
    for row in lines:
        for word in row:
            letters = tuple(place[one] for one in word)
            index = folding.fold_any(unit, letters)  # type: ignore[attr-defined]
            total += max(index.bit_length(), 1)
    return total


if __name__ == "__main__":
    sys.exit(main())
