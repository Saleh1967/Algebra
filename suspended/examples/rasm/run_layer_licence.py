"""البناءُ الصاعدُ برخصةٍ مقيسة — تشغيلُ ختم `73cc5b24…`.

**لا صعودَ إلّا بأربع**: الدالّيةُ والانغلاقُ والتمامُ والرجعة. وتُفحَص كلُّ
طبقةٍ عليها **قبل** التي فوقها، ويُوقَف البناءُ عند أوّل رخصةٍ تسقط.

**L₀** الوحدةُ (١١٢، من `c5a1e18`) ⟶ **L₁** المقطعُ (تقطيعٌ لا تخشين، فالرجعةُ
بلا بقيّة) ⟶ **L₂** شكلُ الكلمة (تسلسلُ الأنواع — تخشينٌ ببقيّة) ⟶ **L₃**
الوزنُ الكمّيّ (خفيفٌ/ثقيل).

**قاعدةُ المقطع المختومة**: داخلَ الكلمة، الوحدةُ ذاتُ الحركة القصيرة تفتح
مقطعًا، والساكنةُ التالية تُغلِقه **قيدًا واحدًا**؛ ونوعُه `CV` بلا غلق،
و`CVV` إن وافق حرفُ المدّ الحركةَ، و`CVC` فيما سواه. وساكنٌ بلا مقطعٍ
مفتوحٍ قبله **غيرُ مُرخَّصٍ ويُعَدّ باسمه**.
"""

from __future__ import annotations

import argparse
import importlib.util
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[2]
PEEL = REPOSITORY / "examples" / "rasm" / "run_cv_peel.py"
FATHA, DAMMA, KASRA, SUKUN = "َ", "ُ", "ِ", "ْ"
SHORT = (FATHA, DAMMA, KASRA)
MATCHING = {FATHA: "ا", DAMMA: "و", KASRA: "ي"}
LIGHT = "CV"
Unit = tuple[str, str]
Syllable = tuple[Unit, ...]


def _peel() -> object:
    spec = importlib.util.spec_from_file_location("run_cv_peel", PEEL)
    if spec is None or spec.loader is None:
        raise RuntimeError("لا قارئَ للتقشير")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def words_of(text: str) -> list[list[Unit]]:
    """كلماتُ L₀ — والبنيويُّ يفصل ولا يدخل."""

    peeler = _peel()
    units, _ = peeler.peel(text)  # type: ignore[attr-defined]
    found: list[list[Unit]] = []
    current: list[Unit] = []
    for base, value in units:
        if base == peeler.STRUCTURE:  # type: ignore[attr-defined]
            if current:
                found.append(current)
                current = []
        else:
            current.append((base, value))
    if current:
        found.append(current)
    return found


def syllabify(word: list[Unit]) -> tuple[list[Syllable], int]:
    """(مقاطعُ الكلمة، عددُ الوحدات غيرِ المُرخَّصة) — بالقاعدة المختومة."""

    built: list[Syllable] = []
    refused = 0
    index = 0
    while index < len(word):
        base, value = word[index]
        if value in SHORT:
            after = index + 1
            if after < len(word) and word[after][1] == SUKUN:
                built.append((word[index], word[after]))
                index = after + 1
            else:
                built.append((word[index],))
                index = after
        else:
            refused += 1
            index += 1
    return (built, refused)


def kind(syllable: Syllable) -> str:
    """نوعُ المقطع — CV أو CVV أو CVC."""

    if len(syllable) == 1:
        return "CV"
    vowel = syllable[0][1]
    return "CVV" if syllable[1][0] == MATCHING.get(vowel) else "CVC"


def weight(one: str) -> str:
    return "خفيف" if one == LIGHT else "ثقيل"


def entropy(counts: Counter[str]) -> float:
    total = sum(counts.values())
    if not total:
        return 0.0
    return -math.fsum(
        (number / total) * math.log2(number / total) for number in counts.values()
    )


def descend(pairs: list[tuple[str, str]]) -> tuple[float, float]:
    """(بقيّةُ الرجعة محجوزةً، الملحَقة) — H(الأدنى | الأعلى) بتًّا للعنصر."""

    even = [one for index, one in enumerate(pairs) if index % 2 == 0]
    odd = [one for index, one in enumerate(pairs) if index % 2]
    return ((_cross(even, odd) + _cross(odd, even)) / 2, _inside(pairs))


def _cross(support: list[tuple[str, str]], measure: list[tuple[str, str]]) -> float:
    table: dict[str, Counter[str]] = defaultdict(Counter)
    plain: Counter[str] = Counter()
    for upper, lower in support:
        table[upper][lower] += 1
        plain[lower] += 1
    alphabet = max(len(plain), 1)
    base = sum(plain.values())
    charge = 0.0
    for upper, lower in measure:
        counts = table.get(upper)
        mass = sum(counts.values()) if counts else base
        counts = counts if counts else plain
        charge -= math.log2((counts.get(lower, 0) + 1) / (mass + alphabet))
    return charge / max(len(measure), 1)


def _inside(pairs: list[tuple[str, str]]) -> float:
    table: dict[str, Counter[str]] = defaultdict(Counter)
    for upper, lower in pairs:
        table[upper][lower] += 1
    mass = len(pairs)
    return math.fsum(sum(one.values()) / mass * entropy(one) for one in table.values())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", type=Path, required=True)
    given = parser.parse_args()

    words = words_of(given.text.read_text(encoding="utf-8"))
    units = sum(len(one) for one in words)
    syllables: list[Syllable] = []
    shapes: list[tuple[str, ...]] = []
    refused = 0
    covered = 0
    for word in words:
        built, missed = syllabify(word)
        refused += missed
        covered += sum(len(one) for one in built)
        syllables.extend(built)
        shapes.append(tuple(kind(one) for one in built))
    kinds = [kind(one) for one in syllables]
    weights = [tuple(weight(one) for one in shape) for shape in shapes]

    print(f"L₀: {units} وحدةً في {len(words)} كلمة")
    print("\n— L₁ المقطع")
    print(f"  الدالّية: غيرُ مُسنَدٍ {refused} ({refused / units:.4f})")
    print(f"  الانغلاق: أنواعٌ {len(set(kinds))} | مقاطعُ متمايزة {len(set(syllables))}")
    print(f"  التمام: {covered} + {refused} = {covered + refused} (وL₀ {units})")
    print(
        f"  الرجعة: التقطيعُ يُعيد الوحداتِ بلا بقيّة — "
        f"{'**مطابق**' if covered + refused == units else 'ناقص'}"
    )
    print(
        f"  مقاطعُ: {len(syllables)} | H = {entropy(Counter(map(str, syllables))):.4f}"
    )
    print(f"  توزيعُ الأنواع: {Counter(kinds).most_common()}")

    print("\n— L₂ شكلُ الكلمة")
    print(f"  الانغلاق: أشكالٌ متمايزة {len(set(shapes))}")
    pairs = [(kind(one), str(one)) for one in syllables]
    outside, plugged = descend(pairs)
    print(
        f"  الرجعة (نوعٌ ⟶ مقطع): محجوزةً {outside:.4f} | ملحَقةً {plugged:.4f} "
        f"| {outside * len(pairs):.0f} بتًّا"
    )
    print(f"  H(الشكل) = {entropy(Counter(map(str, shapes))):.4f}")

    print("\n— L₃ الوزنُ الكمّيّ")
    print(f"  الانغلاق: أوزانٌ متمايزة {len(set(weights))}")
    lower = [(str(a), str(b)) for a, b in zip(weights, shapes)]
    outside3, plugged3 = descend(lower)
    print(
        f"  الرجعة (وزنٌ ⟶ شكل): محجوزةً {outside3:.4f} | ملحَقةً {plugged3:.4f} "
        f"| {outside3 * len(lower):.0f} بتًّا"
    )
    print(f"  H(الوزن) = {entropy(Counter(map(str, weights))):.4f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
